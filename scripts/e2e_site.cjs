'use strict';

const { chromium } = require('playwright');
const axe = require('axe-core');

const BASE = 'http://127.0.0.1:4173/';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const failures = [];

  try {
    let commonsRequests = 0;
    const commonsQueries = [];
    await page.route('https://commons.wikimedia.org/w/api.php**', async route => {
      commonsRequests++;
      commonsQueries.push(new URL(route.request().url()).searchParams.get('gsrsearch') || '');
      const imageUrl = 'https://upload.wikimedia.org/wikipedia/commons/a/ab/indisch-beeldarchief-fixture.jpg';
      const fixture = {
        batchcomplete: true,
        query: { pages: { 1001: {
          pageid: 1001, index: 1,
          title: 'File:Dutch East Indies Java Bandoeng Bandung KNIL Bersiap 1946.jpg',
          imageinfo: [{
            url: imageUrl, thumburl: imageUrl,
            descriptionurl: 'https://commons.wikimedia.org/wiki/File:Indisch_beeldarchief_fixture.jpg',
            mime: 'image/jpeg',
            extmetadata: {
              LicenseUrl: { value: 'https://creativecommons.org/publicdomain/zero/1.0/' },
              LicenseShortName: { value: 'CC0 1.0' },
              DateTimeOriginal: { value: '1946-01-01 00:00:00' },
              ObjectName: { value: 'Dutch East Indies historical photograph' },
              Artist: { value: 'Test fixture' },
              ImageDescription: { value: 'Historical photograph of the Dutch East Indies, Java, Bandoeng Bandung, KNIL military soldier, Bersiap Indonesian National Revolution, daily life people, street building, railway transport, temple culture and landscape.' }
            }
          }]
        }}}
      };
      await route.fulfill({ status: 200, contentType: 'application/json', headers: { 'Access-Control-Allow-Origin': '*' }, body: JSON.stringify(fixture) });
    });
    await page.route('https://upload.wikimedia.org/**', route => route.fulfill({
      status: 200, contentType: 'image/png',
      body: Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j9ZkAAAAASUVORK5CYII=', 'base64')
    }));

    const response = await page.goto(BASE, { waitUntil: 'domcontentloaded', timeout: 45000 });
    if (!response || response.status() !== 200) throw new Error('Homepage did not return HTTP 200');
    await page.waitForFunction(
      () => document.querySelector('#results')?.getAttribute('aria-busy') === 'false',
      null,
      { timeout: 20000 }
    );

    if (!(await page.title()).includes('Indisch Beeldarchief')) failures.push('Homepage title missing');
    try {
      await page.waitForFunction(() => document.querySelectorAll('#results .photo').length > 0, null, { timeout: 20000 });
    } catch (error) {
      const state = await page.evaluate(() => ({
        mainCards: document.querySelectorAll('#results .photo').length,
        mainText: document.querySelector('#results')?.innerText?.slice(0, 500),
        rijksmuseumCount: document.querySelector('#rmCount')?.textContent,
        rijksmuseumCards: document.querySelectorAll('#rmResults .rm-record').length,
        rijksmuseumImages: document.querySelectorAll('#rmResults .rm-record img').length,
        knilCount: document.querySelector('#knilWeaponsCount')?.textContent
      }));
      throw new Error('Initial gallery did not render a photo: ' + JSON.stringify(state) + '; ' + error.message);
    }
    const waitForLoadedGallery = async () => page.waitForFunction(() => {
      const images = [...document.querySelectorAll('#results .photo img')];
      return document.querySelector('#results')?.getAttribute('aria-busy') === 'false' &&
        images.length > 0 && images.some(image => image.complete && image.naturalWidth > 0);
    }, null, { timeout: 20000 });

    for (const view of ['home', 'indies', 'java', 'bandung', 'knil', 'bersiap', 'daily']) {
      const requestsBefore = commonsRequests;
      await page.locator('#nav [data-view="' + view + '"]').click();
      await waitForLoadedGallery();
      const galleryCheck = await page.evaluate(() => ({
        cards: document.querySelectorAll('#results .photo').length,
        loadedImages: [...document.querySelectorAll('#results .photo img')].filter(img => img.complete && img.naturalWidth > 0).length
      }));
      if (commonsRequests <= requestsBefore) failures.push('Tab switch did not request fresh Commons results for ' + view);
      if (galleryCheck.cards < 1 || galleryCheck.loadedImages < 1) failures.push('Historical photos did not render/load for ' + view + ': ' + JSON.stringify(galleryCheck));
      const activeQuery = commonsQueries.at(-1) || '';
      if (view === 'knil' && (!/marechaussee/i.test(activeQuery) || !/klewang/i.test(activeQuery) || !/Nederlandsch-Indisch Leger/i.test(activeQuery) || !/ML-KNIL/i.test(activeQuery))) failures.push('KNIL search query is missing historically specific military terminology: ' + activeQuery);
      if (view === 'home' && (!/Nederlandsche Oost-Indiën/i.test(activeQuery) || !/gouvernement/i.test(activeQuery))) failures.push('Overview search query is missing colonial-era terminology: ' + activeQuery);
      if (view === 'indies' && (!/archipel/i.test(activeQuery) || !/residentie/i.test(activeQuery))) failures.push('Nederlands-Indië search query is missing regional/government terminology: ' + activeQuery);
      if (view === 'java' && (!/Tjimahi/i.test(activeQuery) || !/Soekaboemi/i.test(activeQuery))) failures.push('Java search query is missing historical place spellings: ' + activeQuery);
      if (view === 'bandung' && (!/Tjihapit/i.test(activeQuery) || !/Technische Hoogeschool/i.test(activeQuery))) failures.push('Bandoeng search query is missing local historical terminology: ' + activeQuery);
      if (view === 'daily' && (!/romusha/i.test(activeQuery) || !/pasar/i.test(activeQuery) || !/waroeng/i.test(activeQuery))) failures.push('Daily-life search query is missing Indonesian cultural and social vocabulary: ' + activeQuery);
      if (view === 'bersiap' && (!/pemuda/i.test(activeQuery) || !/laskar/i.test(activeQuery) || !/Politionele Actie/i.test(activeQuery) || !/NICA/i.test(activeQuery) || !/RAPWI/i.test(activeQuery))) failures.push('Bersiap search query is missing Indonesian independence-era terminology: ' + activeQuery);
    }

    await page.locator('#nav [data-view="home"]').click();
    await waitForLoadedGallery();
    let requestsBefore = commonsRequests;
    await page.locator('#period').selectOption('1945-1950');
    await waitForLoadedGallery();
    if (commonsRequests <= requestsBefore) failures.push('Changing the year filter did not reload photo results');

    for (const topic of ['city', 'people', 'military', 'transport', 'culture', 'nature']) {
      requestsBefore = commonsRequests;
      await page.locator('#topic').selectOption(topic);
      await waitForLoadedGallery();
      if (commonsRequests <= requestsBefore) failures.push('Changing topic filter did not reload photo results for ' + topic);
    }

    await page.locator('#nav [data-view="java"]').click();
    await page.locator('#places [data-place="bandung"]').click();
    await waitForLoadedGallery();
    await page.locator('#nav [data-view="bandung"]').click();
    await page.locator('#bandungTopics [data-term="Bragaweg"]').click();
    await waitForLoadedGallery();

    await page.locator('#nav [data-view="knil"]').click();
    await page.locator('#period').selectOption('1945-1950');
    await page.locator('#topic').selectOption('military');
    await page.locator('#q').fill('KNIL');
    await page.locator('#go').click();
    await waitForLoadedGallery();
    await page.reload({ waitUntil: 'domcontentloaded' });
    await waitForLoadedGallery();
    const restoredState = await page.evaluate(() => ({
      activeView: document.querySelector('#nav button[aria-current="page"]')?.dataset.view,
      period: document.querySelector('#period')?.value,
      topic: document.querySelector('#topic')?.value,
      query: document.querySelector('#q')?.value,
      saved: JSON.parse(localStorage.getItem('indisch-beeldarchief-ui-state-v1') || 'null')
    }));
    if (restoredState.activeView !== 'knil' || restoredState.period !== '1945-1950' ||
        restoredState.topic !== 'military' || restoredState.query !== 'KNIL' || restoredState.saved?.view !== 'knil') {
      failures.push('Browser refresh did not restore the selected tab and filters: ' + JSON.stringify(restoredState));
    }

    await page.locator('#nav [data-view="home"]').click();
    await page.locator('#reset').click();
    await waitForLoadedGallery();

    await page.waitForFunction(() => /136 bronrecords/.test(document.querySelector('#knilWeaponsCount')?.textContent || ''), null, { timeout: 20000 });
    const knilInitial = await page.evaluate(() => ({
      cards: document.querySelectorAll('#knilWeaponsResults .record-card').length,
      images: document.querySelectorAll('#knilWeaponsResults img').length,
      publicDomainLabels: [...document.querySelectorAll('#knilWeaponsResults .tag')].filter(x => x.textContent.includes('Publiek Domein · gecontroleerd')).length,
      sourceLinks: [...document.querySelectorAll('#knilWeaponsResults a')].every(a => a.href.startsWith('https://proxy.handle.net/10648/'))
    }));
    if (knilInitial.cards !== 12 || knilInitial.images !== 0 || knilInitial.publicDomainLabels !== 12 || !knilInitial.sourceLinks) {
      failures.push('KNIL rights-verified source index initial page failed: ' + JSON.stringify(knilInitial));
    }
    await page.locator('#knilWeaponsMore').click();
    const knilPaged = await page.locator('#knilWeaponsResults .record-card').count();
    if (knilPaged !== 24) failures.push('KNIL source index pagination expected 24 records, found ' + knilPaged);

    for (const width of [320, 360, 390, 768, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      await page.waitForTimeout(100);
      const dimensions = await page.evaluate(() => ({
        viewport: document.documentElement.clientWidth,
        document: document.documentElement.scrollWidth,
        body: document.body.scrollWidth
      }));
      if (dimensions.document > dimensions.viewport + 1 || dimensions.body > dimensions.viewport + 1) {
        failures.push('Horizontal overflow at ' + width + 'px: ' + JSON.stringify(dimensions));
      }
    }

    await page.setViewportSize({ width: 390, height: 844 });
    await page.locator('#nav [data-view="family"]').click();
    await page.locator('#familyBirsak').waitFor({ state: 'visible' });
    await page.locator('#deepSearch').waitFor({ state: 'visible' });
    await page.waitForFunction(() =>
      [...document.querySelectorAll('#familyBirsak img')].length === 2 &&
      [...document.querySelectorAll('#familyBirsak img')].every(img => img.complete && img.naturalWidth > 0),
      null,
      { timeout: 20000 }
    );

    const familyChecks = await page.evaluate(() => ({
      imageCount: document.querySelectorAll('#familyBirsak img').length,
      sourceLinks: document.querySelectorAll('#deepLinks a').length,
      hasPublicChangelogLink: [...document.querySelectorAll('footer a')].some(a => /CHANGELOG/i.test(a.href)),
      hasEditorialCorrectionNote: /eerdere lezing|correctiebericht|wijzigingsnotitie|de aangeleverde originele scan toont/i.test(document.querySelector('#familyBirsak').innerText)
    }));
    if (familyChecks.imageCount !== 2) failures.push('Both original family photos are not visible');
    if (familyChecks.sourceLinks !== 16) failures.push('Expected 16 Deep Search source links, found ' + familyChecks.sourceLinks);
    if (familyChecks.hasPublicChangelogLink) failures.push('Public website still exposes a change-log link');
    if (familyChecks.hasEditorialCorrectionNote) failures.push('Editorial correction note leaked into the family photo page');

    const rightsChecks = await page.evaluate(() => ({
      cc0: isReusableCommonsLicense({ LicenseUrl: { value: 'https://creativecommons.org/publicdomain/zero/1.0/' } }),
      publicDomainMark: isReusableCommonsLicense({ LicenseUrl: { value: 'https://creativecommons.org/publicdomain/mark/1.0/' } }),
      ccBySa: isReusableCommonsLicense({ LicenseUrl: { value: 'https://creativecommons.org/licenses/by-sa/4.0/' } }),
      copyrightNotEvaluated: isReusableCommonsLicense({ LicenseUrl: { value: 'http://rightsstatements.org/page/CNE/1.0/' } }),
      missing: isReusableCommonsLicense({})
    }));
    if (!rightsChecks.cc0 || !rightsChecks.publicDomainMark || !rightsChecks.ccBySa || rightsChecks.copyrightNotEvaluated || rightsChecks.missing) {
      failures.push('Commons image-rights allowlist failed: ' + JSON.stringify(rightsChecks));
    }

    await page.addScriptTag({ path: require.resolve('axe-core/axe.min.js') });
    for (const view of ['home', 'family']) {
      if (view === 'home') await page.locator('#nav [data-view="home"]').click();
      else await page.locator('#nav [data-view="family"]').click();
      const audit = await page.evaluate(async () => {
        const result = await axe.run(document, {
          runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] }
        });
        return result.violations
          .filter(item => ['critical', 'serious'].includes(item.impact))
          .map(item => ({
            id: item.id,
            impact: item.impact,
            description: item.description,
            nodes: item.nodes.map(node => ({
              target: node.target,
              html: node.html,
              summary: node.failureSummary
            }))
          }));
      });
      if (audit.length) failures.push('Axe serious/critical violations on ' + view + ': ' + JSON.stringify(audit));
    }

    if (failures.length) throw new Error(failures.join('\n'));
    console.log('PASS: desktop/mobile layout, family images, Deep Search links, clean public photo page, and axe WCAG checks.');
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
