// Tests the merge logic shipped in merge.html, using the synthetic demo fragments.
// Run: node tests/test_merge.mjs   (exit code 0 = all pass)
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import assert from 'node:assert/strict';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'merge.html'), 'utf8');
const core = html.match(/<script id="merge-core">([\s\S]*?)<\/script>/)[1];
const KitMerge = new Function(core + '\nreturn KitMerge;')();
const demo = JSON.parse(readFileSync(join(root, 'src', 'demo_fragments.json'), 'utf8'));
const asInputs = (frags) => frags.map((f) => ({ name: f.file.file, text: JSON.stringify(f, null, 1) }));
const run = (frags, opts) => KitMerge.merge(KitMerge.parseInputs(asInputs(frags)).parsed, opts);

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log('PASS  ' + name); }
  catch (e) { failed++; console.log('FAIL  ' + name + '\n      ' + e.message.split('\n').join('\n      ')); }
}
const find = (db, pred) => db.overlap_checks.find(pred);

test('years: own columns only by default; chart years oldest to newest', () => {
  const { db } = run(demo);
  assert.deepEqual(db.meta.inst_years, ['FY2021', 'FY2025', 'FY2026']);
  assert.deepEqual(db.meta.chart_years, { earlier: 'FY2021', later: 'FY2026', years_between: 5 });
  assert.equal(db.kit_schema, 'database-v2');
});

test('unit columns: comparative-only unit columns used; oldest/prior/budget picked', () => {
  const { db } = run(demo);
  assert.deepEqual(db.meta.unit_chart_columns, { oldest: 'FY2023A', prior: 'FY2025A', budget: 'FY2026B', years_between_oldest_and_budget: 3 });
  assert.equal(db.meta.unit_data_applied, 'UPLOAD');
  assert.equal(db.E_unit_totals.FY2025A.revenue.v, 4840000);
});

test('primary values come from each year\'s own report, with file-prefixed src', () => {
  const { db } = run(demo);
  const fed = db.B_inst_revenue.lines.find((l) => KitMerge.normLabel(l.label) === 'federal grants and contracts');
  assert.equal(fed.values.FY2025.v, 77500000);
  assert.match(fed.values.FY2025.src, /^Synthetic_Audit_FY25\.pdf: /);
  assert.equal(fed.values.FY2026.v, 80000000);
  assert.ok(!('FY2024' in fed.values), 'FY2024 is comparative-only and must not be used by default');
});

test('overlap: restated mismatch detected; matching lines MATCH', () => {
  const { db } = run(demo);
  const fed = find(db, (o) => o.year === 'FY2025' && o.kind === 'line' && /Federal grants/.test(o.item));
  assert.equal(fed.status, 'MISMATCH');
  assert.equal(fed.difference, 500000);
  assert.equal(fed.comparative.restated, true);
  const tuition = find(db, (o) => o.year === 'FY2025' && /Tuition and fees/.test(o.item));
  assert.equal(tuition.status, 'MATCH');
  const dLines = db.overlap_checks.filter((o) => o.year === 'FY2025' && o.section === 'D_inst_expenses');
  assert.ok(dLines.length >= 7 && dLines.every((o) => o.status === 'MATCH'), 'all D lines, totals and buckets match');
});

test('classification difference reported', () => {
  const { db } = run(demo);
  const d = db.classification_differences.find((x) => x.line === 'Auxiliary enterprises' && x.attribute === 'category');
  assert.ok(d, 'expected a category difference for Auxiliary enterprises');
  assert.equal(d.kept, 'Auxiliary enterprises');
  assert.equal(d.other, 'Other');
});

test('arithmetic checks all pass on demo data', () => {
  const { db } = run(demo);
  const bad = db.checks.filter((c) => c.source === 'merge page' && !/^PASS/.test(c.status));
  assert.deepEqual(bad, []);
});

test('override uses comparative value, records it, and the line no longer foots', () => {
  const { db: d0 } = run(demo);
  const id = find(d0, (o) => o.year === 'FY2025' && o.kind === 'line' && /Federal grants/.test(o.item)).id;
  const { db } = run(demo, { overrides: [id] });
  const fed = db.B_inst_revenue.lines.find((l) => KitMerge.normLabel(l.label) === 'federal grants and contracts');
  assert.equal(fed.values.FY2025.v, 78000000);
  assert.match(fed.values.FY2025.src, /override/);
  assert.equal(db.overrides.length, 1);
  const foot = db.checks.find((c) => c.column === 'FY2025' && /included \+ excluded/.test(c.check));
  assert.equal(foot.status, 'FAIL', 'overriding a line without its totals must show up as a failed check');
});

test('comparative-only institution years can be switched on', () => {
  const { db } = run(demo, { useComparativeOnly: { institution: true } });
  assert.deepEqual(db.meta.inst_years, ['FY2020', 'FY2021', 'FY2024', 'FY2025', 'FY2026']);
  assert.deepEqual(db.meta.comparative_only_columns_used.filter((k) => !/[AB]$/.test(k)).sort(), ['FY2020', 'FY2024']);
});

test('chart year selection is honored', () => {
  const { db } = run(demo, { chartYears: { earlier: 'FY2025', later: 'FY2026' } });
  assert.deepEqual(db.meta.chart_years, { earlier: 'FY2025', later: 'FY2026', years_between: 1 });
});

test('a fragment split across two files (with prose between) is joined', () => {
  const text = JSON.stringify(demo[0], null, 1);
  const lines = text.split('\n');
  const mid = Math.floor(lines.length / 2);
  const part1 = 'Here is fragment 1 of 4.\n```json\n' + lines.slice(0, mid).join('\n') + '\nType continue for the rest of the JSON,';
  const part2 = 'Continuing exactly where I stopped:\n' + lines.slice(mid).join('\n') + '\n```\nFragment 1 of 4 complete: Synthetic_Audit_FY26.pdf.';
  const p = KitMerge.parseInputs([{ name: 'part1.txt', text: part1 }, { name: 'part2.txt', text: part2 }]);
  assert.deepEqual(p.errors, []);
  assert.equal(p.parsed.length, 1);
  assert.deepEqual(p.parsed[0].obj, demo[0]);
});

test('two valid pieces of the same file (sections split) are combined', () => {
  const a = JSON.parse(JSON.stringify(demo[0])), b = JSON.parse(JSON.stringify(demo[0]));
  a.D_inst_expenses = null; a.F_balance_sheet = null;
  b.B_inst_revenue = null;
  const { db, notes } = run([a, b, demo[1], demo[2], demo[3]]);
  assert.ok(notes.some((n) => /Combined/.test(n)));
  assert.equal(db.D_inst_expenses.totals.FY2026.v, 445000000);
  assert.equal(db.B_inst_revenue.total_included.FY2026.v, 440000000);
  assert.ok(db.F_balance_sheet.FY2026);
});

test('rounding tolerance between a thousands report and a dollars report', () => {
  const fy25 = JSON.parse(JSON.stringify(demo[1]));
  fy25.file.units_in_source = 'dollars';
  fy25.B_inst_revenue.lines[0].values.FY2025.v = 115000400;
  const { db } = run([demo[0], fy25]);
  const t = find(db, (o) => o.year === 'FY2025' && o.kind === 'line' && /Tuition and fees/.test(o.item));
  assert.equal(t.status, 'ROUNDING');
});

test('renamed line reported as NO_MATCHING_LINE on both sides', () => {
  const fy25 = JSON.parse(JSON.stringify(demo[1]));
  fy25.D_inst_expenses.lines[2].label = 'Supplies, services and other';
  const { db } = run([demo[0], fy25]);
  const nm = db.overlap_checks.filter((o) => o.status === 'NO_MATCHING_LINE' && o.year === 'FY2025');
  assert.equal(nm.length, 2);
});

test('missing printed heading fails the heading check; file-name year conflict noted', () => {
  const f = JSON.parse(JSON.stringify(demo[2]));
  f.columns[0].heading_as_printed = '';
  f.file.file = 'Audit_FY2019.pdf';
  const r = run([demo[0], f]);
  const h = r.db.checks.find((c) => /printed column heading \(Audit_FY2019/.test(c.check) && c.column === 'FY2021');
  assert.equal(h.status, 'FAIL');
  assert.ok(r.info.some((m) => /file name suggests FY2019/.test(m)));
});

test('non-fragment input is rejected with a reason', () => {
  const r = KitMerge.merge([{ name: 'x.json', obj: { kit_schema: 'database-v2' } }]);
  assert.equal(r.db, null);
  assert.ok(r.warnings.some((w) => /merged database/.test(w)));
});

test('truncated file is flagged', () => {
  const f = JSON.parse(JSON.stringify(demo[1]));
  f.file.status = 'TRUNCATED';
  const r = run([demo[0], f]);
  assert.ok(r.warnings.some((w) => /TRUNCATED/.test(w)));
});

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
