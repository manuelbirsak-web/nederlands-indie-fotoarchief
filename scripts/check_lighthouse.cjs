'use strict';

const fs = require('node:fs');
const report = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const thresholds = {
  performance: 0.70,
  accessibility: 0.90,
  'best-practices': 0.90,
  seo: 0.90
};
let failed = false;
for (const [name, minimum] of Object.entries(thresholds)) {
  const score = report.categories?.[name]?.score;
  if (typeof score !== 'number') {
    console.error('FAIL: Lighthouse category missing: ' + name);
    failed = true;
    continue;
  }
  console.log((score >= minimum ? 'PASS' : 'FAIL') + ' ' + name + ': ' + Math.round(score * 100) + '/100 (minimum ' + Math.round(minimum * 100) + ')');
  if (score < minimum) failed = true;
}
if (failed) process.exit(1);
