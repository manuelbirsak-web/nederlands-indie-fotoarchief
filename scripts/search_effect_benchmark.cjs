'use strict';

// Live-source retrieval benchmark. This intentionally compares the previous one-query
// flow with the current multi-cluster retrieval under the same Wikimedia snapshot.
const fs = require('node:fs');
const vm = require('node:vm');

const HTML = fs.readFileSync('index.html', 'utf8');
const API = 'https://commons.wikimedia.org/w/api.php';
const VIEW_NAMES = ['home','indies','java','bandung','knil','bersiap','daily'];
const BASELINE_BATCH_LIMIT = 8;
const BASELINE_PHOTO_LIMIT = 8;
const EXPANDED_BATCH_LIMIT = 12;
const EXPANDED_PHOTO_LIMIT = 18;
const PAGE_SIZE = 50;
const ALLOWED_LICENSE = url =>
  url === 'https://creativecommons.org/publicdomain/mark/1.0/' ||
  url === 'https://creativecommons.org/publicdomain/zero/1.0/' ||
  /^https:\/\/creativecommons\.org\/licenses\/by(?:-sa)?\/(?:1\.0|2\.0|2\.5|3\.0|4\.0)\/$/.test(url);
const NON_PHOTO = /\b(wordmark|logo|map of|coat of arms|rank insignia|book cover|journal|magazine|newspaper|poster|stamp|flag icon|letter|lettre|envelope|postcard|post card|postage|philatel|postal|coin|banknote|ticket|manuscript|document scan)\b/i;
const HISTORICAL_CONTEXT = /dutch east indies|nederlands.?indi[eë]|nederlandsche oost.?indi[eë]n|netherlands east indies|netherlands indies|colonial|kolonial|koloniaal|koloniale|residentie|gouvernement|archipel|bersiap|knil|ml-knil|militaire luchtvaart|koninklijk nederlandsch.?indisch leger|nederlandsch.?indisch leger|indonesian national revolution|indonesian war of independence|nica|rapwi|apwi|seac|amacab|revolusi nasional indonesia|perang kemerdekaan indonesia|agresi militer|politionele actie|pemoeda|pemuda|bkr|tkr|tri|alri|romusha|heiho|kampong|pasar|sawah|aloen.?aloen|interneringskamp|burgerkamp|krijgsgevangenkamp|werkkamp|opvangkamp|republikeins kamp|kempeitai|krijgsgevangene|atjeh|aceh|koetaradja|mentawai|nias|papua|nieuw.?guinea|madoera|madura|molukken|buitengewesten|voc|cultuurstelsel|ethische politiek|slavernij|opium|specerijenhandel|adat|batik|gamelan|wajang|njai|mardijkers|mestiezen|krakatau|lahar|nootmuskaat|kruidnagel/i;
const VIEW_PATTERNS = {
 home: /dutch east indies|nederlands.?indi[eë]|nederlandsche oost.?indi[eë]n|netherlands east indies|netherlands indies|colonial|kolonial|koloniaal|koloniale|residentie|gouvernement|archipel|bersiap|knil|bandoeng|bandung|batavia|buitenzorg|java|sumatra|borneo|celebes|surabaya|soerabaja|semarang|yogyakarta|djokja|atjeh|aceh|koetaradja|kota radja|mentawai|nias|papua|nieuw.?guinea|madoera|madura|molukken|buitengewesten|voc|kamp|interneringskamp|burgerkamp|krijgsgevangenkamp|cultuurstelsel|ethische politiek|slavernij|opium|specerijenhandel/i,
 indies: /dutch east indies|nederlands.?indi[eë]|nederlandsche oost.?indi[eë]n|netherlands east indies|netherlands indies|colonial|kolonial|koloniaal|koloniale|residentie|gouvernement|archipel|bersiap|knil|bandoeng|bandung|batavia|buitenzorg|java|sumatra|borneo|celebes|surabaya|soerabaja|semarang|yogyakarta|djokja|atjeh|aceh|koetaradja|kota radja|mentawai|nias|papua|nieuw.?guinea|madoera|madura|molukken|buitengewesten|voc|kamp|interneringskamp|burgerkamp|krijgsgevangenkamp|peta|bkr|tkr|tri|tni|adat|repatriering/i,
 java: /java|djawa|bandoeng|bandung|batavia|djakarta|jakarta|buitenzorg|bogor|semarang|soerabaja|surabaya|djokja|djocja|yogyakarta|malang|tjimahi|cimahi|garoet|garut|soekaboemi|sukabumi|tjilatjap|cilacap|tasikmalaja|tasikmalaya|leles|cheribon|cirebon|ambarawa|banjoebiroe|magelang|tegal|pekalongan|tangerang|kesilir|bondowoso|ngawi|kediri|grissee|gresik|singosari|madoera|madura|kalidjati|kalibanteng|pakanbaroe|pekanbaru|soerakarta|surakarta|solo|kedoe|preanger|priangan|banten|bantam|tjiandjoer|pasoeroean|probolinggo|madioen|madiun|djember|jember|banjoemas|banyumas|kampong|aloen.?aloen|pasar|sawah|interneringskamp|krijgsgevangenkamp/i,
 bandung: /bandoeng|bandung|tjimahi|cimahi|lembang|dago|bragaweg|tjihapit|tjiboenoet|andir|technische hoogeschool|gedung sate|aloen.?aloen|kampong|karees|ramawijk|soekamiskin|lands opvoedings gesticht|depot mobiele artillerie|barosweg|leuwigadjah|tjimindi|kedoengbadak|kedoenghalang|palace hotel|zeelandia|stella maris|dick de hoogschool|bandung lautan api|gedung merdeka/i,
 knil: /knil|koninklijk nederlandsch.?indisch leger|nederlandsch.?indisch leger|royal netherlands east indies army|netherlands indies army|dutch east indies military|military.*dutch east indies|militair.*nederlands.?indi[eë]|soldier.*knil|soldaat.*knil|marechaussee|veldpolitie|garnizoen|kazerne|bivak|patrouille|infanterie|artillerie|cavalerie|veldgeschut|mitrailleur|klewang|karabijn|bajonet|pantserwagen|militaire expeditie|heiho|gurkha|bataljon|ml-knil|mld|militaire luchtvaart|koninklijke marine reserve|krijgsgevangene|krijgsgevangenkamp|kampement|werkkamp|stadswacht|landstormer|treinkampement|bergartillerie|luchtdoelartillerie|knil.?uniform|knil.?officier|peta|nefis|mariniersbrigade|stoottroepen|tijgerbrigade/i,
 bersiap: /bersiap|indonesian national revolution|indonesian war of independence|indonesian independence|indonesian independence struggle|revolusi nasional indonesia|perang kemerdekaan indonesia|perang revolusi indonesia|politionele actie|agresi militer|perang kemerdekaan|perang revolusi|pemuda|pemoeda|laskar|tentara keamanan rakyat|\btkr\b|tentara republik indonesia|\btri\b|\btni\b|republikeinse troepen|vrijheidsstrijd|onafhankelijkheidsstrijd|dekolonisatie|linggadjati|renville|rawagede|tentara keamanan rakjat|badan keamanan rakjat|\bbkr\b|angkatan laut republik indonesia|\balri\b|nica|rapwi|apwi|seac|amacab|zelfinternering|onafhankelijkheidsverklaring|evacuatie|vluchtelingen|brits-indische troepen|kempeitai|republikeins kamp|republikeinse kampen|madioen-opstand|soevereiniteitsoverdracht/i,
 daily: /dutch east indies|nederlands.?indi[eë]|nederlandsche oost.?indi[eë]n|netherlands indies|colonial|kolonial|koloniaal|daily life|everyday life|family life|kampong|desa|aloen.?aloen|pasar|waroeng|warung|sawah|ladang|pendopo|grobak|bengkel|gudang|romusha|village life|market scene|people of indonesia|school|onderwijs|hbs|mulo|ams|nias|adat|batik|gamelan|wajang|njai|plantation|onderneming|rubberplantage|koffieplantage|suikeronderneming|theeplantage|nootmuskaat|kruidnagel|mardijkers|mestiezen/i
};
function extractObject(name) {
  const marker = 'const ' + name + '=';
  const start = HTML.indexOf(marker);
  if (start < 0) throw new Error('Missing ' + marker);
  const objectStart = HTML.indexOf('{', start + marker.length);
  let depth = 0, quote = null, escaped = false;
  for (let i=objectStart; i<HTML.length; i++) {
    const ch = HTML[i];
    if (quote) {
      if (escaped) escaped=false;
      else if (ch==='\\') escaped=true;
      else if (ch===quote) quote=null;
      continue;
    }
    if (ch===String.fromCharCode(39) || ch==='"') { quote=ch; continue; }
    if (ch==='{') depth++;
    if (ch==='}') {
      depth--;
      if (depth===0) return vm.runInNewContext('(' + HTML.slice(objectStart,i+1) + ')');
    }
  }
  throw new Error('Unclosed object ' + name);
}
const views = extractObject('views');
const places = extractObject('places');
const viewTerms = extractObject('viewTerms');
const clusters = extractObject('viewQueryClusters');
const baselineBase = {
  home: views.home.query,
  indies: views.indies.query,
  java: places.all,
  bandung: views.bandung.query,
  knil: views.knil.query,
  bersiap: views.bersiap.query,
  daily: views.daily.query
};

function sleep(ms) { return new Promise(resolve => setTimeout(resolve,ms)); }
async function fetchBatch(query, continuation) {
  const params = new URLSearchParams({
    action:'query', format:'json', origin:'*', generator:'search',
    gsrsearch:query, gsrnamespace:'6', gsrlimit:String(PAGE_SIZE),
    prop:'imageinfo', iiprop:'url|extmetadata|mime', iiurlwidth:'300'
  });
  if (continuation) for (const [key,value] of Object.entries(continuation)) params.set(key,String(value));
  let lastError;
  for (let attempt=0; attempt<3; attempt++) {
    try {
      const response = await fetch(API + '?' + params.toString(), {
        headers: { 'Accept':'application/json', 'User-Agent':'IndischBeeldarchiefSearchBenchmark/1.0 (public cultural heritage research)' }
      });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const data = await response.json();
      if (data.error) throw new Error(data.error.code + ': ' + data.error.info);
      return data;
    } catch (error) {
      lastError=error;
      await sleep(800*(attempt+1));
    }
  }
  throw lastError;
}
function metadataValue(meta,key) {
  const value=meta?.[key]?.value || '';
  return String(value).replace(/<[^>]*>/g,' ').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').trim();
}
function isEligible(page,view) {
  const info=page.imageinfo?.[0];
  if (!info || !info.url || !String(info.mime||'').startsWith('image/')) return {eligible:false,reason:'not-image'};
  const meta=info.extmetadata||{};
  const license=metadataValue(meta,'LicenseUrl');
  if (!ALLOWED_LICENSE(license)) return {eligible:false,reason:'license'};
  const text=[page.title,metadataValue(meta,'ObjectName'),metadataValue(meta,'ImageDescription'),metadataValue(meta,'Categories')].join(' ');
  if (NON_PHOTO.test(text)) return {eligible:false,reason:'non-photo'};
  if (!VIEW_PATTERNS[view]?.test(text)) return {eligible:false,reason:'tab-filter'};
  const date=metadataValue(meta,'DateTimeOriginal');
  const yearMatch=date.match(/(?:^|\D)((?:18|19|20)\d{2})(?:\D|$)/);
  const year=yearMatch?Number(yearMatch[1]):null;
  if (year!==null&&(year<1800||year>1959)) return {eligible:false,reason:'outside-period'};
  return {eligible:(year!==null||HISTORICAL_CONTEXT.test(text)),reason:year!==null?'dated':'context-undated',year,text,license,url:info.descriptionurl||''};
}
async function runFlow(name,view,queries,photoLimit,batchLimit) {
  const records=new Map(),errors=[],queryStats=[];
  let photos=0,batches=0;
  for (const query of queries) {
    if (photos>=photoLimit || batches>=batchLimit) break;
    let continuation=null;
    let queryBatches=0;
    do {
      const fullQuery=query+' filetype:bitmap';
      try {
        const data=await fetchBatch(fullQuery,continuation);
        const pages=Object.values(data.query?.pages||{}).sort((a,b)=>(a.index??0)-(b.index??0));
        let fresh=0,eligible=0;
        for (const page of pages) {
          const title=page.title||String(page.pageid);
          if (records.has(title)) continue;
          const result=isEligible(page,view);
          if (!result.eligible) continue;
          records.set(title,{title,...result,query});
          fresh++;eligible++;
        }
        photos=records.size;
        continuation=data.continue||null;
        queryBatches++;batches++;
        queryStats.push({query:query.slice(0,180),pages:pages.length,newUniqueEligible:fresh,continuation:Boolean(continuation)});
        await sleep(300);
      } catch (error) {
        errors.push({query:query.slice(0,160),error:String(error)});
        break;
      }
    } while (continuation && photos<photoLimit && batches<batchLimit);
  }
  const items=[...records.values()];
  return {
    name,queryCount:queries.length,batches,uniqueRightsEligibleFiles:items.length,
    datedFiles:items.filter(x=>x.reason==='dated').length,
    contextUndatedFiles:items.filter(x=>x.reason==='context-undated').length,
    errors,queryStats,
    sampleTitles:items.slice(0,12).map(x=>({title:x.title,year:x.year,query:x.query.slice(0,120),url:x.url}))
  };
}
async function main() {
  const report={
    generatedAt:new Date().toISOString(),
    source:'Wikimedia Commons API',
    method:'Live metadata retrieval snapshot. Counts are distinct image files with an allowlisted image licence and a historical date/context check; this is not a manual precision audit.',
    limits:{pageSize:PAGE_SIZE,baselineBatchLimit:BASELINE_BATCH_LIMIT,baselinePhotoLimit:BASELINE_PHOTO_LIMIT,expandedBatchLimit:EXPANDED_BATCH_LIMIT,expandedPhotoLimit:EXPANDED_PHOTO_LIMIT},
    tabs:{}
  };
  let failed=0;
  for (const view of VIEW_NAMES) {
    const baselineQueries=[baselineBase[view]+' '+(viewTerms[view]||'')];
    const expandedQueries=[baselineBase[view],...(clusters[view]||[]),...(viewTerms[view]?[viewTerms[view]]:[])];
    const baseline=await runFlow('baseline',view,baselineQueries,BASELINE_PHOTO_LIMIT,BASELINE_BATCH_LIMIT);
    const expanded=await runFlow('expanded',view,expandedQueries,EXPANDED_PHOTO_LIMIT,EXPANDED_BATCH_LIMIT);
    failed+=baseline.errors.length+expanded.errors.length;
    const delta=expanded.uniqueRightsEligibleFiles-baseline.uniqueRightsEligibleFiles;
    report.tabs[view]={
      baseline,expanded,
      deltaUniqueRightsEligibleFiles:delta,
      improvementRatio:baseline.uniqueRightsEligibleFiles?Number((expanded.uniqueRightsEligibleFiles/baseline.uniqueRightsEligibleFiles).toFixed(3)):null,
      result:'NEEDS_MANUAL_RELEVANCE_REVIEW'
    };
    console.log(view+': '+baseline.uniqueRightsEligibleFiles+' → '+expanded.uniqueRightsEligibleFiles+' eligible unique files (Δ '+delta+')');
  }
  const deltas=Object.values(report.tabs).map(x=>x.deltaUniqueRightsEligibleFiles);
  report.summary={
    tabs:VIEW_NAMES.length,
    tabsWithIncreasedEligibleFiles:deltas.filter(x=>x>0).length,
    tabsWithNoIncrease:deltas.filter(x=>x<=0).length,
    totalBaseline:VIEW_NAMES.reduce((n,v)=>n+report.tabs[v].baseline.uniqueRightsEligibleFiles,0),
    totalExpanded:VIEW_NAMES.reduce((n,v)=>n+report.tabs[v].expanded.uniqueRightsEligibleFiles,0),
    failedQueries:failed,
    manualPrecisionAuditRequired:true
  };
  report.status=failed?'INCONCLUSIVE_SOURCE_ERRORS':'MEASURED_NEEDS_MANUAL_PRECISION_REVIEW';
  fs.mkdirSync('artifacts',{recursive:true});
  fs.writeFileSync('artifacts/search-effect-benchmark.json',JSON.stringify(report,null,2)+'\n');
  if (failed) throw new Error('One or more live Wikimedia requests failed; benchmark is inconclusive.');
  console.log('Benchmark artifact written: artifacts/search-effect-benchmark.json');
}
main().catch(error=>{console.error(error);process.exitCode=1;});
