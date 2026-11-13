'use strict';

const { chromium } = require('playwright');
const axe = require('axe-core');

const BASE = 'http://127.0.0.1:4173/';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const failures = [];

  try {
    await page.route('https://commons.wikimedia.org/w/api.php**', route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ batchcomplete: true, query: { pages: {} } })
      })
    );

    const response = await page.goto(BASE, { waitUntil: 'domcontentloaded', timeout: 45000 });
    if (!response || response.status() !== 200) throw new Error('Homepage did not return HTTP 200');
    await page.waitForFunction(
      () => document.querySelector('#results')?.getAttribute('aria-busy') === 'false',
      null,
      { timeout: 20000 }
    );

    if (!(await page.title()).includes('Indisch Beeldarchief')) failures.push('Homepage title missing');
    await page.waitForFunction(() => document.querySelectorAll('#results .photo').length > 0, null, { timeout: 20000 });
    const galleryViews = ['knil', 'bersiap', 'daily'];
    for (const view of galleryViews) {
      await page.locator('#nav [data-view="' + view + '"]').click();
      await page.waitForFunction(() => document.querySelector('#results')?.getAttribute('aria-busy') === 'false', null, { timeout: 20000 });
      await page.waitForFunction(() => document.querySelectorAll('#results .photo').length > 0, null, { timeout: 20000 });
      const visible = await page.locator('#results .photo').count();
      if (!visible) failures.push('No rights-cleared primary-gallery images for ' + view);
    }
    await page.locator('#nav [data-view="home"]').click();
    await page.waitForFunction(() => document.querySelector('#results')?.getAttribute('aria-busy') === 'false', null, { timeout: 20000 });


    await page.waitForFunction(() => /148 bronrecords/.test(document.querySelector('#knilWeaponsCount')?.textContent || ''), null, { timeout: 20000 });
    const knilInitial = await page.evaluate(() => ({
      cards: document.querySelectorAll('#knilWeaponsResults .record-card').length,
      images: document.querySelectorAll('#knilWeaponsResults img').length,
      cneLabels: [...document.querySelectorAll('#knilWeaponsResults .tag')].filter(x => x.textContent.includes('CNE · alleen metadata')).length,
      sourceLinks: [...document.querySelectorAll('#knilWeaponsResults a')].every(a => a.href.startsWith('https://proxy.handle.net/10648/'))
    }));
    if (knilInitial.cards !== 12 || knilInitial.images !== 0 || knilInitial.cneLabels !== 12 || !knilInitial.sourceLinks) {
      failures.push('KNIL metadata-only source index initial page failed: ' + JSON.stringify(knilInitial));
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
