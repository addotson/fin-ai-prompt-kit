# Institutional Finance Charts: Multi-Stage Prompt Kit

Nov 23, 2026 · @Aaron

## How to use this kit

Run five stages in order, using only the AI tool and your files. Stage 2 extracts each uploaded file, a short part at a time, straight into one `database.json` by running code. Stages 4 and 5 read that file. Every JSON the tool creates is a file you download, not text you copy, and Stages 4 and 5 read `database.json` as an upload, not a paste. If your tool cannot create files, keep Stages 1 to 5 in one chat and it reads everything from the chat, so you still copy nothing. No stage after Stage 2 depends on the tool re-reading your PDFs or remembering a long conversation.

1. **Stage 1, inventory.** Upload all files, paste the Stage 1 prompt. The tool proves how much of each file it can read, maps every fiscal year from the column headings, and asks only the decisions the spec leaves open. If a file is too long for the tool, it lists the pages to keep instead; trim the PDF (see Trimming a PDF) and start again. Answer the questions, then save the STAGE 1 DECISIONS block it prints.
2. **Stage 2, extraction.** Paste the Stage 2 prompt. Each response extracts one short part of one file and adds it to `database.json` with code, giving you a fresh download link; type NEXT after each. Attach a PDF again if the tool says it can no longer see it. After the last part, type FINISH: the tool cross-checks every year that appears in two reports and gives you the final `database.json` with a MERGE SUMMARY.
3. **Stage 3, review.** Spot-check the MERGE SUMMARY and the JSON against your PDFs using the checklist. Send corrections, restated-figure choices, or different chart years with the correction prompt; the tool rebuilds `database.json`. Download the final file.
4. **Stage 4, static charts.** Upload `database.json` and paste the Stage 4 prompt. If your tool could not create files, run Stage 4 in the same chat as Stage 2 instead, with no upload. The tool draws the 12 matplotlib charts and the data summary.
5. **Stage 5, dashboard.** Upload `database.json` (or stay in the same chat) and paste the Stage 5 prompt. The tool writes one interactive HTML file for you to download. Save it as `dashboard.html` and open it in a browser.

Rules for every platform: start a new chat for Stage 1; keep Stages 1–3 in the same chat; Stages 4 and 5 can run in a new chat, or a different tool, because they only need `database.json`; if your tool could not create files, keep them in the same chat. Download every file the tool offers as soon as it appears; chat file links can expire. Fill in the three blanks at the top of Stage 1 before sending.

You can upload more than two years of audited statements. Every report adds its own year, and its comparative column becomes a cross-check on the year before. Upload consecutive reports (for example FY26 and FY25) to get the cross-check; reports with a gap between them (FY26 and FY22) add years but nothing to compare. The charts compare the oldest and newest years by default; name different years in the Stage 3 correction prompt.

### What changed from the original class prompt

The chart specifications, Sections A–F, checks, and CAGR formula come from the original class prompt. Only the lines below changed.

| Original line | Change | Reason |
| --- | --- | --- |
| "without stopping to ask me questions" | Stage 1 asks bounded questions, then stops | Your method: resolve judgment calls before extraction |
| "Never ask me to upload anything else" | Tool may list missing items once in Stage 1, but must proceed without them | Your method; still never blocks on, or invents, missing data |
| "Extract Sections A through F... Don't print them" | Stage 2 writes them into `database.json` by running code, one short part per response, and prints only a summary table | Portable database; short responses; no step retypes earlier data |
| "HOW TO WORK" steps 1–5 | Split across Stages 1, 2, 4 | Long single-pass tasks degrade on weaker tools (inference, not measured) |
| "Don't create files or documents" | Kept for Stage 4; Stage 5 creates one HTML file | Dashboard requirement |
| Page citation format unspecified | Defined as printed page number, with PDF page of the uploaded file in brackets | Tools pick inconsistently; makes spot-checks possible |
| (new) | Stage 1 must prove how much of each file it can read, and lists pages to keep if it cannot read all of it | Copilot silently read only the first ~129,000 characters of each report |
| "Use only the column for the fiscal year that file covers" | Kept as the primary value; the comparative column is also recorded, and every year is read from the printed column heading | The overlap becomes a cross-check; file names can be wrong |
| Two institution years and three unit years, fixed | Any number of years; the charts compare the oldest and newest unless you name others in Stage 3 | Use more data when it is provided |
| The tool compares and totals across files | Arithmetic checks run in code after every part; the cross-file comparison runs in code at FINISH | Tools skipped the check that would have failed, and a merge left to the end produced an empty file (observed in Copilot) |
| JSON printed in chat, then copied and pasted | `database.json` is a downloadable file updated after every part; Stages 4 and 5 read it as an upload, or from the same chat, and confirm it loaded completely | Copilot truncated a pasted `database.json` and refused a whole-file response as too large (observed) |
| Section F: most recent audited year | Optionally every year (Stage 1 question j) | Balance-sheet overlap check, at the cost of longer extractions |

The DATA SUMMARY still prints at the end of Stage 4. Stage 5 repeats it inside the dashboard.

## Stage 1 prompt: inventory, coverage, and questions

Upload every file first, then paste this. Expect one response that ends with numbered questions, or with a list of pages to keep if a file is too long for the tool. Check the quoted last-page text against your PDF: if the quote is not on that page, the tool is not reading the file, whatever it says.

```text
STAGE 1 OF 5: FILE INVENTORY, COVERAGE CHECK, AND QUESTIONS. Do not extract numbers or draw anything yet.

My institution: ________ My unit: ________
Unit data: ________ (write UPLOAD or SKIP)

This is the first of five stages. Later stages will extract each file into one JSON database, draw 12 charts, and build an HTML dashboard. In this stage you only identify files, prove what you can read, and ask me the decisions you need.

WHAT I'VE PROVIDED
- Audited financial statements for two or more of my institution's fiscal years. Each report usually
shows two years side by side: the year it covers and the year before.
- Optional: my institution's most recent bond rating report.
- If Unit data is UPLOAD: my unit's current budget and one or more years of its actuals, in one or
more files.
- If Unit data is SKIP: no unit data. Skip the five unit charts.

FISCAL YEARS COME FROM THE PAGE, NOT THE FILE NAME
Read every fiscal year from the column headings printed on the statement pages (for example "June 30, 2025" or "2025"). Never take a year from a file name, a cover page, or what I typed. Label each fiscal year "FY" plus the calendar year in which it ends: a year ending June 30, 2025 is FY2025.

DO THIS
1. Identify each file: what it is, its units (dollars, thousands, or millions), its accounting standard
(GASB, FASB, IFRS, or other), and whether it is audited. Use the names I typed above; if I left them
blank, use the names in the files.
2. PROVE WHAT YOU CAN READ. For each file, give the last printed page number you can actually see, with its PDF page in brackets, and quote the first full sentence or table row on that page word for word. Then give the file's last page according to its table of contents or page footers (for example "Page 98 of 98"), if shown. If you can see only part of the file, if the text stops partway, or if a page is a scanned image you cannot read reliably, mark the file TRUNCATED or UNREADABLE. Do not guess at anything you cannot see.
3. COVERAGE TABLE. For each institution report, print: Item | Printed page [PDF page], or NOT VISIBLE. Items:
   - Statement of net position (public) or statement of financial position (private)
   - Statement of revenues, expenses, and changes in net position (public) or statement of activities (private)
   - Statement of cash flows
   - Operating expenses by natural classification (statement or note)
   - Capital assets note
   - Long-term debt note (bonds, notes payable, leases)
   - Cash and investments note
   - Scholarship allowance disclosure (for example "net of scholarship allowances of $___")
   - Pension and OPEB note (public only)
   - Liquidity note (private only)
   - Discretely presented foundation statements, if any (public only)
   For each unit file, list the pages or sheets with the budget or actuals tables.
4. YEAR MAP. Print a table: File name | What it is | Own year (the year the file covers) | Comparative year | Column headings as printed, with page | Year-end | Units | Standard | Audited? | Status (OK, TRUNCATED, or UNREADABLE). Mark a comparative column "restated" if its heading says so. Then list each fiscal year found, the file that covers it (its primary source), and any other file that also shows it as a comparative column. Those overlaps will be cross-checked later. If no year appears in two files, say that the cross-check will not run because the reports are not consecutive.
5. IF ANY FILE IS TRUNCATED OR UNREADABLE, print PAGES TO KEEP for that file:
   - Use the file's table of contents to find the printed page ranges of the basic financial statements and of each note in the coverage list, and convert them to PDF page ranges.
   - List what can be removed, with page ranges: transmittal letters, management's discussion and analysis, required supplementary information schedules, combining and supplementary schedules, the statistical section, and single audit or federal awards reports.
   - Write one line I can type into a print dialog's page box, for example "PDF pages to keep: 18-24, 26-31, 40-44, 58-61".
   - If you cannot see the table of contents, say so and list the section names I should keep instead.
   Then tell me to save a trimmed copy with only those pages, upload it in place of the original, and paste this Stage 1 prompt again. Stop there. Do not ask the questions below until every file is OK.
6. State which unit years you have (actuals years and budget year), read from the column headings. If Unit data is UPLOAD but no unit files are present, say Unit data will be treated as SKIP.
7. List any item whose absence will prevent a specific chart, naming the chart. Do not ask me to upload it. Later stages will proceed without it.
8. State the page convention you will use: printed page number as shown on the page, followed by the PDF page of the uploaded file in brackets, for example "p. 23 [PDF 31]".
9. Ask me only the questions below that apply to these files, numbered, one line each, with your proposed default answer in brackets. Ask nothing else.
   a. Private (FASB): does the statement of activities present an operating measure (case a) or not (case b)? State which you found and ask me to confirm.
   b. Public (GASB): is there a discretely presented foundation that holds gifts and endowment? Confirm it should be included where the spec says.
   c. Are hospital or health system amounts in separate columns? Confirm you will use academic columns only. If a hospital or health system is consolidated with no separate columns, say so, give patient care revenue as a share of total operating revenue, and confirm that the charts will include it.
   d. Does the state pay pension or OPEB contributions on the institution's behalf (on-behalf payments)? If found, confirm exclusion.
   e. Scholarship allowances: are they combined with housing or other revenue? Is a tuition-only portion disclosed?
   f. Unit budget: list the current budget's expense categories and revenue categories as you found them. If there are more than 8, propose which to combine.
   g. Unit actuals: list any actuals line you cannot map to a current-budget category, with your proposed category.
   h. Any file whose fiscal year, read from its column headings, differs from its file name or from what I described.
   i. Two files that cover the same own year: which one to use.
   j. Balance sheet years: LATEST (most recent year only) or ALL (every year, which adds a balance-sheet cross-check but makes each extraction longer). [LATEST]
10. End with: "Answer the questions above, or reply DEFAULTS to accept all bracketed defaults." Then stop.
11. When I answer, reply only with a STAGE 1 DECISIONS block in a code block: institution, unit, Unit data applied, basis (GASB, FASB case a, FASB case b, IFRS, or other), currency, page convention, balance sheet years, the year map table, the unit categories, and every question with its final answer. After it, write: "Save this block. Then paste the Stage 2 prompt." Then stop.

Never invent, sample, or estimate any number. Never use an example or hypothetical institution or department.
```

### Trimming a PDF

If Stage 1 reports a file as TRUNCATED, make a copy with only the pages it lists. Use a tool on your own computer; do not upload institutional files to online PDF sites.

- **Any browser (Chrome, Edge, Safari):** open the PDF, choose Print, set the destination to Save as PDF, choose custom pages, and paste the page list from Stage 1 (for example `18-24, 26-31, 40-44`).
- **Mac Preview:** View > Thumbnails, select the pages to keep, then File > Print, choose "Selected Pages in Sidebar," and save as PDF.

Printed page numbers stay the same after trimming. PDF page numbers in later citations refer to the trimmed copy, so keep the trimmed copy for the Stage 3 spot-checks. Trimming helps even when Stage 1 reports OK: less text means less for the tool to misread, and on tools with file limits (Copilot in particular) it is the difference between reading the notes and not.

## Stage 2 prompt: extraction into database.json

Paste after Stage 1, in the same chat. Each response extracts one short part of one file (three parts per file) and adds it to `database.json` by running code; type NEXT after each. Download `database.json` whenever the tool offers it: each download is a backup you can attach if the tool loses the file. If the tool says it can no longer see a PDF, attach that PDF again. After the last part, type FINISH: the tool runs the cross-checks and gives you the final `database.json` with a MERGE SUMMARY. If the tool says NO CODE, it prints each part as a table instead and prints the whole database once at FINISH. The rules between the BEGIN and END markers are the original prompt, edited only to record every year column.

```text
STAGE 2 OF 5: BUILD database.json ONE SHORT PART AT A TIME. Do not draw charts. Do not calculate CAGRs or ratios.

STAGE 1 DECISIONS: use the STAGE 1 DECISIONS block from this chat. If this is a new chat, I have pasted it here:
<paste the STAGE 1 DECISIONS block here, or leave this line as is in the same chat>

Never ask me to upload anything else, except as described under HOW THIS STAGE WORKS. If something
is missing, work with what you have, and never fill the gap with invented, sample, or example numbers.
Unit data comes only from my unit files. If Unit data is UPLOAD but no unit budget or actuals files
are among the uploads, treat Unit data as SKIP and say so. Never invent a unit, never use an
example or hypothetical department, and never use institution-wide numbers, or a share of them,
in place of unit data.

HOW THIS STAGE WORKS
- You build one file, database.json, a little at a time. Each response extracts one PART of one source file and adds it to database.json by running code. You never retype earlier parts.
- Order: the Stage 1 year map, newest institution report first, then older reports, then unit files. The bond rating report's three items go into the most recent institution report's PART 3.
- Parts. Institution report: PART 1 = Section B (revenue lines, totals, tuition detail). PART 2 = Section D. PART 3 = Section F if this file needs it, plus this file's judgment calls and not-found items. Unit file: PART 1 = Section A. PART 2 = Sections C and E. PART 3 = this file's judgment calls and not-found items. If your response limit comfortably allows it, you may do more than one part of the same file in one response.
- Before extracting a file, re-read the column headings on its statement pages. Each column's fiscal year comes from its printed heading, never from the file name. Label it "FY" plus the calendar year in which it ends.
- Read a part's source pages before writing any of its numbers.
- If you can no longer see the source file, say so in one line and ask me to attach it again. If database.json from your previous response is no longer available to your code, ask me to attach the latest database.json I downloaded. These are the only uploads you may ask for.

===== BEGIN ORIGINAL RULES (edited to record every year column) =====
EXTRACTION RULES
- Audited statements show two years side by side. Read each column's fiscal year from its printed
heading. The column for the fiscal year that file covers is its own column and supplies that
year's values. Also record the comparative column, labeled with its own fiscal year, for
cross-checking only. If its heading says "restated" or "as restated," record that.
- Convert all amounts to whole dollars.
- Record the page number, or the sheet and row, for every number.
- Never estimate. If you can't find an item, record NOT FOUND.
- Assign each line whole to one category or bucket. Don't split lines. One exception: if
depreciation and amortization are one line and the notes split them, use the notes' split.
- If the statements are reviewed or unaudited, add "(unaudited)" to every chart subtitle. If they
follow a non-US standard, map each line to the nearest category below and report in the
statements' currency.
- If the state pays pension or retiree health (OPEB) contributions on the institution's behalf and
records them as both revenue and expense, exclude those amounts from both totals.
- If the statements show the academic enterprise and a hospital or health system in separate
columns or segments, use only the academic columns.
SECTION A: UNIT OPERATING EXPENSES (every year column in the unit file, actuals or budget)
Every operating expense line, as labeled, with its amount in each year column. For each
line:
1. CATEGORY: no more than 8, using the current budget's own groupings. Assign the lines from
every actuals year to the same categories.
2. BUCKET: PEOPLE (salaries, wages, benefits, payroll taxes, stipends); SPACE (space or
occupancy charges, rent, utilities, maintenance and repairs, depreciation, interest); STUFF
(everything else).
Total operating expenses for each year column.
SECTION B: INSTITUTION REVENUES (the file's own year and its comparative year)
Every revenue line, operating and nonoperating, as labeled, with its amount. For each line:
1. INCLUDED or EXCLUDED. Exclude capital appropriations, capital gifts and grants, additions
to permanent endowments, and unrealized investment gains or losses. Include everything else
that supports operations.
Public (GASB): net investment income usually includes unrealized gains and losses. If realized
income isn't shown separately, exclude that line. If the notes disclose the endowment distribution
used for operations, include that amount instead, as its own line.
Private (FASB), one of two cases. (a) The statement of activities presents an operating measure,
such as "change in net assets from operating activities": use the revenue lines within that
measure, total column, and exclude everything below it. (b) There is no operating measure: use
only the without-donor-restrictions column, including net assets released from restrictions, and
include investment return only up to the endowment spending distribution, if disclosed; otherwise
exclude it. Say which case applies.
2. CATEGORY, for included lines: Net tuition and fees (after institutional aid and scholarship
allowances); Government appropriations; Grants and contracts (including research and Pell);
Gifts and contributions; Endowment and investment income used for operations; Auxiliary
enterprises; Patient care / hospital; Other.
Total included revenue for each year column.
TUITION DETAIL for each year column: gross tuition and fees before discounts; each scholarship
allowance or institutional aid line subtracted from tuition; and whether those allowances also
cover other revenue such as housing. If gross tuition isn't on the face of the statements, look in
the notes or for a phrase such as "net of scholarship allowances of $___."
SECTION C: UNIT REVENUES (every year column in the unit file)
Every revenue line, as labeled, with its amount in each year column, including allocations or
transfers from the central institution. Use the current budget's categories, no more than 8,
combining the smallest into "Other." Assign the lines from every actuals year to those categories;
put a line that fits none in "Other." Total revenue for each year column.
SECTION D: INSTITUTION EXPENSES (the file's own year and its comparative year)
Operating expenses by natural classification (salaries, benefits, supplies, depreciation, and so
on), not by function. If the main statements show only functions, use the notes or the statement of
functional expenses. Include interest expense on debt. If it is reported outside operating
expenses, add it; if it is already one of the operating expense lines, don't add it again. Assign
each line to one bucket:
- PEOPLE: salaries, wages, benefits, payroll taxes.
- SPACE: depreciation, interest, utilities, maintenance and repairs where reported separately, and
amortization of leased buildings.
- STUFF: everything else, including supplies and services, scholarships and fellowships, other
expenses, and amortization of software subscriptions. If amortization isn't split between leases
and subscriptions, put it in SPACE.
Total expenses for each year column.
SECTION E: UNIT TOTALS (every year column in the unit file)
Total revenue and total expenses for each year column, matching the totals in Sections A and C.
Record separately any transfers or allocations from the central institution, and any transfers out.
SECTION F: BALANCE SHEET AND FACILITIES (the most recent institution report's own year; if
balance sheet years is ALL, every report's own and comparative years)
- Cash and cash equivalents.
- Investments, current and noncurrent, with amounts labeled restricted or endowment shown
separately.
- Private (FASB) only: financial assets available for general expenditure within one year, from the
liquidity note.
- Total current assets and total current liabilities, or NOT PRESENTED.
- Net assets by class. Public: net investment in capital assets; restricted nonexpendable;
restricted expendable; unrestricted. Private: without donor restrictions; with donor restrictions,
split into held in perpetuity and not held in perpetuity.
- Property, plant, and equipment, net; accumulated depreciation (capital assets note);
depreciation expense.
- Purchases of capital assets, from the statement of cash flows.
- Long-term debt: bonds, notes payable, and lease liabilities (finance leases, for private
institutions), current and noncurrent. Exclude subscription-based IT (SBITA), pension, and OPEB
liabilities.
- Public only: net pension liability, net OPEB liability, and pension and OPEB deferred outflows
and deferred inflows.
- A discretely presented foundation that holds gifts and endowment for the institution: its total
expenses and net assets by class, kept separate. Never hospitals, health systems, or athletic
associations.
- From the bond rating report, if provided: agency, rating, and median days cash on hand for that
rating category.
CHECKS (do these before saving each part; no one else will check these numbers before the
charts are made)
- Each column's fiscal year was read from its printed heading, and each number comes from the
column for that year.
- Amounts reported "in thousands" or "in millions" were converted.
- Included plus excluded revenue lines equal the statement's total revenues, operating plus
nonoperating, in each column.
- Section D lines equal the statement's total operating expenses, plus any interest you added, in
each column.
- Net asset classes add up to total net assets.
- Unit lines add up to the stated totals in each unit year column.
- Record each column's year-end date as printed. The FINISH step counts the years between them.
If a check fails, re-read the source and correct it. If it still fails, continue, and report it in the
database checks.
===== END ORIGINAL RULES =====

EACH RESPONSE
1. Extract this part's values for every column in the file: the file's own year and its comparative year, or, for a unit file, every year column.
2. Run code (Python) that:
   a. loads database.json if it exists, or starts it from the DATABASE SCHEMA below;
   b. records this file in meta.files once, with its columns (key, fiscal year, type, role, year-end, heading as printed, heading page, restated);
   c. writes this part's values following the MERGE RULES, replacing any earlier values from the same file and part and leaving everything else untouched;
   d. re-runs every arithmetic CHECK the data now allows, for every column, and replaces this file's checks;
   e. saves database.json and prints one COUNT line for every section and column in the whole database, for example "B FY2026: 17 lines, total included $9,391,347,000; comparatives from FY26.pdf: FY2025 17 lines".
3. Give me the download link to the updated database.json.
4. Print only: a short table of what this part added (Label | Category or bucket | Value for each column | src), the COUNT lines, and any FAIL check. Do not print the JSON.
5. End with "<file name>: PART <n> of 3 saved to database.json. Type NEXT." After the last part of the last file, end with "All files extracted. Type FINISH to run the cross-checks." Then stop.
If you cannot run code or save files at all, say NO CODE once. Then in each response print this part as the table in item 4, with every value and src, and keep going; at FINISH, build database.json from those tables following the same rules and print it once, in one code block.
Never stop, shorten the extraction, or ask me how to proceed because of output size.

MERGE RULES (your code applies these every time it writes)
1. Values for a column key come only from the file where that column's role is "own". Every comparative column value goes into "comparatives" for cross-checking and never replaces an own value. If two files have the same own column, keep the more recent file's values and put the other file's values into "comparatives".
2. Match lines across files by label, ignoring case, punctuation, and "&" versus "and". The newest file's label, category, bucket, and included status apply to every year; record each difference in classification_differences.
3. Every "src" starts with its file name, for example "FY25 audit.pdf: p. 23 [PDF 31]".
4. Every number is {"v": <whole-dollar integer, or null if NOT FOUND>, "src": "<file name>: <page or sheet!row>"}. Negative numbers stay negative. Never write thousands or millions. Use null with src "N/A" for items that do not apply (for example, net_assets_private at a public institution). Every null whose src is not "N/A" also appears in not_found.

WHEN I TYPE FINISH (run code)
1. Unit columns that appear only as comparatives (for example, prior actuals shown in the budget file) are moved from "comparatives" into the unit sections and listed in meta.comparative_only_columns_used. Institution columns that appear only as comparatives are not used for charts.
2. OVERLAP CHECK. For every comparative whose column also has an own value, compare the two: every line, every total, gross tuition, each Section B category (included lines) and each Section A or D bucket, and every Section E and F number present in both. Status: MATCH (identical); ROUNDING (differs by no more than half the rounding unit of the coarser file, for example $500 when one file is in thousands; for a category or bucket, that amount times its number of lines); MISMATCH; ONE_NOT_FOUND (one side null); NO_MATCHING_LINE (a line in one file has no matching label in the other). Save every result in overlap_checks.
3. Chart years, unless I name others: earlier = oldest institution column used; later = newest. Unit: oldest = oldest actuals column; prior = newest actuals column before the budget year, or null if there is none besides oldest; budget = newest budget column. Years between two columns = months between their year-end dates ÷ 12. Fill meta.inst_years, unit_columns, year_ends, chart_years, and unit_chart_columns.
4. Re-run every arithmetic CHECK on every column, and add one check per column that its year came from a printed heading.
5. Save database.json, give me the link, and print the COUNT lines and a MERGE SUMMARY: each year used and its source file; years not used and why; chart years and years between; counts by overlap status; a table of every overlap row that is not MATCH or ROUNDING (Year | Item | Value used, with src | Comparative value, with src | Difference | Restated?); classification differences; every FAIL check. If no year appears in two files, say the cross-check could not run because the reports are not consecutive.
6. End with: "Stage 2 complete. Download database.json. Review it with the Stage 3 checklist." Then stop.

DATABASE SCHEMA (database.json; angle brackets describe the value; they are not data)
{
 "kit_schema": "database-v2",
 "meta": {
  "institution": "<name>", "unit": "<name or null>",
  "unit_data_requested": "UPLOAD|SKIP", "unit_data_applied": "UPLOAD|SKIP", "unit_data_reason": "<text>",
  "basis": "GASB|FASB_case_a|FASB_case_b|IFRS|other", "currency": "<ISO code>", "audited": <true only if every institution file is audited>,
  "page_convention": "file name: printed page [PDF page of the uploaded file]", "balance_sheet_years": "LATEST|ALL",
  "user_decisions": [{"question": "", "answer": ""}],
  "files": [{"file": "<file name as uploaded>", "kind": "institution|unit", "what": "", "standard": "GASB|FASB|IFRS|other", "audited": <bool>, "units_in_source": "dollars|thousands|millions", "status": "OK|TRUNCATED|UNREADABLE", "last_page_seen": "<printed page [PDF page]>",
   "columns": [{"key": "<institution: FY label, e.g. FY2025; unit: FY label plus A for actuals or B for budget, e.g. FY2025A, FY2026B>", "fiscal_year": "<FY label>", "type": "audited|actual|budget", "role": "own|comparative", "year_end": "<YYYY-MM-DD>", "heading_as_printed": "<column heading, word for word>", "heading_src": "<page>", "restated": <bool>, "used_as_primary": <bool>}]}],
  "inst_years": ["<institution column keys used, oldest first>"],
  "unit_columns": [{"key": "", "fiscal_year": "", "type": "actual|budget"}],
  "year_ends": {"<column key>": "<YYYY-MM-DD>"},
  "chart_years": {"earlier": "<key>", "later": "<key>", "years_between": <number>},
  "unit_chart_columns": {"oldest": "<key or null>", "prior": "<key or null>", "budget": "<key or null>", "years_between_oldest_and_budget": <number or null>},
  "comparative_only_columns_used": ["<key>"]
 },
 "A_unit_expenses": {
  "categories": ["<current-budget category names, max 8>"],
  "lines": [{"label": "<as labeled>", "category": "", "bucket": "PEOPLE|SPACE|STUFF", "values": {"<column key>": <num>}}],
  "totals": {"<column key>": <num>}
 },
 "B_inst_revenue": {
  "lines": [{"label": "", "operating": <bool>, "included": <bool>, "exclusion_reason": "<text or null>", "category": "<one of the 8 Section B categories, or null if excluded>", "values": {"<column key>": <num>}}],
  "total_included": {"<column key>": <num>},
  "statement_total_revenues": {"<column key>": <num>},
  "tuition": {"<column key>": {"gross": <num>, "allowances": [{"label": "", "amount": <num>}], "allowances_cover_other_revenue": <bool>, "tuition_portion_of_allowances": <num>}}
 },
 "C_unit_revenue": {
  "categories": ["<max 8, including Other if used>"],
  "lines": [{"label": "", "category": "", "is_central_allocation": <bool>, "values": {"<column key>": <num>}}],
  "totals": {"<column key>": <num>}
 },
 "D_inst_expenses": {
  "source_of_natural_classification": "<statement or note name>",
  "lines": [{"label": "", "bucket": "PEOPLE|SPACE|STUFF", "interest_added_from_outside_operating": <bool>, "values": {"<column key>": <num>}}],
  "totals": {"<column key>": <num>},
  "statement_total_operating_expenses": {"<column key>": <num>}
 },
 "E_unit_totals": {"<column key>": {"revenue": <num>, "expenses": <num>, "central_transfers_in": <num>, "transfers_out": <num>}},
 "F_balance_sheet": {"<column key>": {
  "cash_and_equivalents": <num>,
  "investments": [{"label": "", "current": <bool>, "restricted_or_endowment": <bool>, "held_by_foundation": <bool>, "amount": <num>}],
  "investments_only_in_notes": <bool>,
  "fasb_liquidity_available_within_one_year": <num>,
  "current_assets": <num>, "current_liabilities": <num>,
  "net_assets_public": {"net_investment_in_capital_assets": <num>, "restricted_nonexpendable": <num>, "restricted_expendable": <num>, "unrestricted": <num>},
  "net_assets_private": {"without_donor_restrictions": <num>, "with_donor_held_in_perpetuity": <num>, "with_donor_not_in_perpetuity": <num>},
  "total_net_assets": <num>,
  "ppe_net": <num>, "accumulated_depreciation": <num>, "depreciation_expense": <num>,
  "purchases_of_capital_assets": <num>,
  "long_term_debt": [{"label": "", "current": <bool>, "amount": <num>}],
  "net_pension_liability": <num>, "net_opeb_liability": <num>,
  "pension_opeb_deferred_outflows": <num>, "pension_opeb_deferred_inflows": <num>,
  "foundation": {"present": <bool>, "name": "", "total_expenses": <num>, "without_donor_restrictions": <num>, "with_donor_held_in_perpetuity": <num>, "with_donor_not_in_perpetuity": <num>},
  "rating": {"provided": <bool>, "agency": "", "rating": "", "median_days_cash": <num>}
 }},
 "comparatives": [{"file": "", "column": "<key>", "restated": <bool>, "section": "", "item": "<line label, or field such as total_included, tuition.gross, or F.cash_and_equivalents>", "value": <num>}],
 "overlap_checks": [{"year": "<key>", "section": "", "item": "", "status": "MATCH|ROUNDING|MISMATCH|ONE_NOT_FOUND|NO_MATCHING_LINE", "difference": <number or null>, "used": <num>, "comparative": <num>, "comparative_file": "", "restated": <bool>}],
 "overrides": [{"year": "<key>", "item": "", "replaced": <num>, "with": <num>}],
 "classification_differences": [{"section": "", "line": "", "attribute": "", "used": "", "used_from": "<file>", "other": "", "other_from": "<file>"}],
 "checks": [{"source": "<file name or FINISH>", "check": "", "column": "<key>", "status": "PASS|FAIL|N/A", "detail": "<the two numbers compared>"}],
 "judgment_calls": ["<file name>: <excluded revenue lines and why; lines that mix buckets; placement of amortization and scholarship allowances>"],
 "not_found": [{"file": "", "section": "", "column": "<key>", "item": ""}]
}
<num> means {"v": integer or null, "src": "file name: page or sheet!row"}. A section with no data is null. Every "values", "totals", and other object keyed by "<column key>" holds own values only.
```

## Stage 3: review and correct

This stage is you, not the tool. It takes about 15 to 30 minutes and is the main defense against a confident wrong number reaching a chart. Work from the MERGE SUMMARY the tool printed and the `database.json` you downloaded. First check the COUNT lines: every section you expect should have lines for every year. A section with zero lines means the data never reached the file, whatever the summary says. To see more, ask in the same chat, for example "Show every overlap_checks row for FY2025."

- [ ] Year headings: confirm each file's own year in the MERGE SUMMARY matches the column heading on its statement page, not the file name. Any file marked TRUNCATED or UNREADABLE: trim it and redo Stages 1 and 2.
- [ ] Overlap MISMATCH rows: open both cited pages. If one extraction is wrong, correct it. If the later report marks the column restated, decide which figure to use. By default each year comes from its own report, as originally reported; to use the restated figure, add a USE RESTATED line to the correction prompt, and include the affected totals too.
- [ ] NO_MATCHING_LINE rows: usually a renamed line. Correct the label so the line lines up across years.
- [ ] Classification differences: the same line got a different category, bucket, or included status in different files. Pick one and correct the other.
- [ ] Any check marked FAIL: open the cited page and find the error yourself before asking the tool.
- [ ] Five largest numbers (usually total revenue, total expenses, total net assets, salaries, net tuition): open each `src` page and confirm the amount and the year column.
- [ ] Units: pick one line from a statement reported in thousands and confirm the JSON value has three extra zeros.
- [ ] Excluded revenue lines: confirm each `exclusion_reason` matches the Section B rule.
- [ ] `not_found`: confirm each item is genuinely absent. A tool that missed a note page, or read a truncated file, will list it here.
- [ ] Unit data: confirm no unit value equals an institution value or a round share of one.
- [ ] Chart years: the charts compare the oldest and newest institution years by default. Name others in the correction prompt if you need them.
- [ ] JSON validity: open `database.json` in a browser (drag the file onto a browser window). If it shows an error instead of the data, the file is incomplete; ask the tool to rebuild it.

Correction prompt, same chat as Stage 2. Delete the numbered lines you do not need:

```text
STAGE 3 CORRECTIONS. Apply only the changes below to database.json by running code (if you no longer have it, ask me to attach the latest copy). Then repeat the FINISH steps: re-run the checks and the overlap check, save database.json, give me the download link, and print the COUNT lines and the MERGE SUMMARY. Do not change any other value.

1. <field path, e.g. D_inst_expenses.lines["Supplies and services"].values.FY2025> should be <amount> per <file name and page>.
2. USE RESTATED: <item, e.g. B_inst_revenue line "Federal grants and contracts">, <year>. Use the later report's comparative value for that year from "comparatives" and record it in overrides.
3. CHART YEARS: earlier <FY____>, later <FY____>.
```

If the tool changes values you did not list, compare the old and new `database.json` (a text diff tool works) and reject the extra changes.

## Stage 4 prompt: the 12 charts

Works in the same chat or a new one. Upload `database.json` (rename it `database.txt` if the tool rejects `.json`), then paste the prompt. Do not paste the JSON into the message: long pastes get cut off. Everything between the markers is the original prompt, edited only so Chart 201.1 plots extra years and the DATA SUMMARY reports the overlap check.

```text
STAGE 4 OF 5: DRAW THE 12 CHARTS FROM THE JSON DATABASE BELOW.

DATA SOURCE: Use only the JSON database (kit_schema "database-v2", built at the end of Stage 2): the file database.json or database.txt I uploaded with this message, or, if I uploaded none and this is the same chat as Stage 2, the database.json built at the end of Stage 2 in this chat. Before drawing anything, load the whole database by running code and print one line: the institution, meta.inst_years, meta.chart_years, and the number of lines in Sections B and D. If it does not load as complete JSON, or you can see only part of it, stop and say so; do not draw from a partial database. Do not re-read the uploaded financial statements for numbers. Do not change any value in the JSON. Each "v" is whole dollars; each "src" is the citation, starting with the file name. Section names in the rules map to JSON keys: Section A = A_unit_expenses, B = B_inst_revenue, C = C_unit_revenue, D = D_inst_expenses, E = E_unit_totals, F = F_balance_sheet. Institution and unit names, basis (public GASB vs. private FASB), audited status, and Unit data choice are in "meta". A null value is NOT FOUND or N/A.

YEARS: Amounts are stored by column key under "values", "totals", and similar objects. "Earlier year," "later year," and "both audited years" mean meta.chart_years.earlier and meta.chart_years.later; the years between them is meta.chart_years.years_between. "Oldest actuals," "prior-year actuals," and "current budget" mean the column keys in meta.unit_chart_columns (oldest, prior, budget); the years between oldest and budget is meta.unit_chart_columns.years_between_oldest_and_budget. If meta.unit_chart_columns.prior is null, draw the unit charts with the two years you have and say so under each one. "Most recent audited year" means meta.chart_years.later, so Section F is F_balance_sheet[meta.chart_years.later]. meta.inst_years lists every institution year in the database.

Do not ask me questions in this stage. Extract nothing new: your job is to calculate and draw. Do not analyze or interpret.

===== BEGIN ORIGINAL RULES (edited for extra years) =====
Draw the 12 charts in order, following the CHART RULES. After the last chart, print the DATA SUMMARY.
If you run out of room in a response, stop after a complete chart and write "Type continue for the
next chart." Never stop partway through a chart.

CHART RULES (all charts)
- Draw every chart by running Python code with matplotlib, typing the values from your extracted
data directly into the code. Never use an image generator: it can't place exact numbers.
- Show each chart as an image in this chat. Don't create files or documents.
- If you can't run code, draw nothing. Instead, for each chart, print its number, its title and subtitle
filled in, and the table of values it would show.
- 6.5 inches wide, landscape, 200 dpi, white background, unless a chart says otherwise. No
gridlines, no 3D effects, no legend unless a chart asks for one.
- Dollar labels like $1.2M or $450K.
- CAGR = (later amount ÷ earlier amount)^(1 ÷ years between them) − 1, using dollars. For unit
charts, the CAGR always runs from the oldest actuals to the current budget; the prior-year
actuals are shown but not used in the CAGR. If either amount is zero or negative, show "n/m"
and explain under the chart. Write CAGRs as "+4.2%/yr" or "−1.8%/yr," always with the sign.
Revenue CAGRs: green for growth, red for decline. Expense CAGRs: red for growth, green for
decline. Discount CAGRs (101.4): gray.
- GROUPED BARS (101.2, 101.3, 101.5, 101.6): one group per category or bucket; bar length =
share of total, labeled with its percentage; the CAGR labeled to the right of each group; a legend
for the years only. Institution charts (101.2, 101.5): two bars, earlier year light gray, later year a
dark contrasting color. Unit charts (101.3, 101.6): three bars in this order, oldest actuals light gray,
prior-year actuals medium gray, current budget a dark contrasting color.
- Every chart carries its title and subtitle on the image itself: the title in bold at the top, the subtitle
in a smaller font directly under it. Fill in the institution name, unit name, fiscal years, and
calculated figures in every title and subtitle. Never leave a bracketed placeholder on an image.
- Before showing a chart, check that no titles, subtitles, labels, legends, or notes overlap or run off
the image. If they do, make the figure taller and redraw; don't shrink the text.
- Above each chart image, print one line of text with its number and title, for example "Chart
101.2: Where Example University's Revenue Comes From". Under each chart: the table of values
used, then the one sentence the chart asks for. Nothing else.
- Unit charts (101.1, 101.3, 101.6, 201.2, DEFENSE.1): if Unit data is SKIP, or you have no real
unit data, print one line with the chart's number and the name in its heading below, for example
"Chart 101.3 (Revenues, unit): Skipped: no unit data," and draw nothing. A unit chart drawn from
invented or institution-wide numbers is worse than no chart.
CHART 101.1: 10% OF OPERATING BUDGET (unit)
Data: Section A current-budget expenses by category. Calculate the total and 10% of it.
Horizontal bars, one per category, largest at top, in gray. Add a bar labeled "10% of our budget,"
in rank order, in a bold contrasting color. Label every bar with its dollars.
Title: "10% of [unit]'s Budget = $[amount]". Subtitle: "[budget fiscal year] budgeted operating
expenses by category".
Sentence: the categories smaller than the 10% amount.
CHART 101.2: REVENUES (institution)
Data: Section B included revenue by category, both audited years. Paired bars, sorted by
later-year share, largest at top; leave out categories that are zero in both years.
Title: "Where [institution]'s Revenue Comes From". Subtitle: "Share of total revenue, [earlier year]
vs. [later year]. Total revenue grew [total CAGR]."
Under the chart, the table shows each category's dollars and share in each year, and its CAGR.
Sentence: the categories that grew faster than total revenue and so gained share.
CHART 101.3: REVENUES (unit)
Same as 101.2, using Section C for all three unit years, with the unit's own categories. Three
bars per category; sort by current-budget share.
Title: "Where [unit]'s Revenue Comes From". Subtitle: "Share of total revenue, [oldest actuals
year] and [prior year] actuals vs. [budget year] budget. Total revenue grew [total CAGR]."
Under the chart, the table shows each category's dollars and share in each of the three years,
and its CAGR. Sentence: the categories that grew faster than total revenue.
CHART 101.4: TUITION DISCOUNT (institution)
Data: Section B tuition detail, both audited years. Discounts = allowances subtracted from tuition;
if combined with other revenue, use the tuition portion if disclosed, otherwise the combined
amount, and say so. Net tuition = gross − discounts. Discount rate = discounts ÷ gross. CAGRs
of gross tuition, discounts, and net tuition. If gross tuition is NOT FOUND, write "Chart 101.4 can't
be made: gross tuition not reported" and move on.
Two stacked columns, one per year. Full height = gross tuition, labeled at the top ("$412.6M
charged"). Bottom segment = net tuition, dark ("$238.1M collected"). Top segment = discounts,
light gray ("$174.5M discounted (42.3%)"). List the three CAGRs to the right.
Title: "What [institution] Charges vs. What It Collects". Subtitle: "Tuition and fees, [earlier year] vs.
[later year]. Discount rate went from [earlier rate] to [later rate]."
Public (GASB) only, small note at the bottom of the image: "Scholarship allowances at public
institutions include federal (Pell) and state grants applied to student bills, not only the institution's
own aid. The discount rate shown is therefore higher than the institution's own discount rate."
Sentence: "Net tuition grew [faster/slower] than gross tuition by [difference] percentage points per
year."
CHART 101.5: EXPENSES, PEOPLE, SPACE, AND STUFF (institution)
Data: Section D totals by bucket, both audited years. Paired bars, in this order from the top:
People, Space, Stuff.
Title: "Where [institution]'s Money Goes: People, Space, and Stuff". Subtitle: "Share of total
expenses, [earlier year] vs. [later year]. Total expenses grew [total CAGR]."
Small note at the bottom of the image: "People: [lines]. Space: [lines]. Stuff: [lines]." using the
source's line names. If a bucket has more than 6 lines, list the 5 largest, then "and [number]
others." Make the image taller if needed.
Under the chart, add a second table listing every line, its bucket, and its amounts. Sentence: any
bucket that grew faster than total expenses.
CHART 101.6: EXPENSES, PEOPLE, SPACE, AND STUFF (unit)
Same as 101.5, using Section A for all three unit years. Three bars per bucket. In the note at the
bottom, list the lines by current-budget amount.
Title: "Where [unit]'s Money Goes: People, Space, and Stuff". Subtitle: "Share of total expenses,
[oldest actuals year] and [prior year] actuals vs. [budget year] budget. Total expenses grew [total
CAGR]."
Under the chart, the tables show all three years.
CHART 201.1: REVENUE AND EXPENSE GROWTH / SURPLUS OR DEFICIT (institution)
Data: total included revenue (Section B) and total expenses (Section D), both audited years.
Surplus or deficit = revenue − expenses; margin = surplus or deficit ÷ revenue. CAGRs of
revenue and expenses. If meta.inst_years includes years between the earlier and later year, plot
those years too, spaced by the actual time between them, and add them to the table under the
chart; the CAGRs still use only the earlier and later year.
Two panels stacked, sharing a fiscal-year axis. Top (two-thirds of the height): revenue line in a
dark color and expense line in a contrasting color, neither red nor green; label each marker with
its dollars; label each line's CAGR at its right end; start the vertical axis just below the lowest
value. Bottom (one-third): one bar per year, green for surplus, red for deficit, with a clear zero
line, labeled "$12.3M (1.5%)".
Title: "Is [institution]'s Revenue Keeping Pace with Its Expenses?" Subtitle: "[earlier year] to [later
year]. Revenue grew [revenue CAGR]; expenses grew [expense CAGR]."
Sentence: "Expenses grew [faster/slower] than revenue by [difference] percentage points per
year."
CHART 201.2: REVENUE AND EXPENSE GROWTH / SURPLUS OR DEFICIT (unit)
Same as 201.1, using Section E for all three years: oldest actuals, prior-year actuals, current
budget. Space the years by the actual time between them, leaving gaps for missing years. Draw
actual years as solid lines with filled markers; draw the segment into the budget year dashed,
with hollow markers, labeled "Budget." Draw the budget-year bar lighter or hatched.
Title: "Is [unit]'s Revenue Keeping Pace with Its Expenses?" Subtitle: "[oldest actuals year]
actuals to [budget year] budget. Revenue grew [revenue CAGR]; expenses grew [expense
CAGR]."
Sentence as in 201.1. If Section E recorded central transfers or allocations, add one sentence
stating their amount in each year.
CHART OFFENSE.1: CUSHION AGAINST RISK + CAPACITY TO INVEST (institution)
Data: Section F and total expenses from Section D, most recent audited year. Use the
institution's own amounts only. For public institutions with a foundation, also show the
foundation's expendable net assets (without donor restrictions + with donor restrictions not held in
perpetuity) as a separate line in the table under the chart.
Calculate:
1. Days cash on hand = liquid resources ÷ ((total expenses − depreciation) ÷ 365). Private:
financial assets available within one year. Public: cash and cash equivalents plus investments,
current and noncurrent, from the statement of net position, excluding amounts labeled restricted,
endowment, or held by a foundation. If investments appear only in the notes, use the notes'
unrestricted total and say so under the chart.
2. Current ratio = current assets ÷ current liabilities, or "n/m" if NOT PRESENTED.
3. Expendable net assets. Public: unrestricted + restricted expendable. Private: without donor
restrictions + with donor restrictions not held in perpetuity − (net PP&E − long-term debt).
4. Public only, adjusted: replace unrestricted with unrestricted + net pension liability + net OPEB
liability − pension/OPEB deferred outflows + pension/OPEB deferred inflows.
5. Primary reserve ratio = expendable net assets ÷ total expenses, also in months (× 12).
6. Viability ratio = expendable net assets ÷ long-term debt, or "n/m: no debt."
Public: calculate 5 and 6 both as reported and adjusted.
A 2×2 grid of panels, each with its own axis starting at zero; negative bars extend below a clear
zero line. Put each row's label on its own line above the row, with clear space between it and the
panel titles. Top row, labeled "Cushion Against Risk": "Days Cash on Hand" ("How many days
could we pay our bills from cash?") and "Current Ratio" ("Can we cover the bills due this year?").
Bottom row, labeled "Capacity to Invest": "Primary Reserve Ratio" ("How long could reserves run
the institution?") and "Viability Ratio" ("Could reserves pay off our debt?"). One dark bar per
panel; for public institutions, the bottom panels get "As reported" (light) and "Adjusted for
pension/OPEB" (dark). Label every bar ("143 days," "1.8x," "0.52x (6.2 months)").
Dashed, labeled benchmark lines: primary reserve 0.40x (about 5 months); viability 1.25x; current
ratio 1.0x, labeled "1.0x = current assets equal current liabilities"; days cash at the
rating-category median from the rating report, labeled with agency and rating, or no line if none.
Image 6.5 inches wide and about 6 inches tall.
Title: "Cushion Against Risk + Capacity to Invest". Subtitle: "[institution], [most recent year]".
Small note at the bottom of the image: "Benchmarks: primary reserve (0.40) and viability (1.25)
from Strategic Financial Analysis for Higher Education, 7th ed. (KPMG; Prager, Sealy & Co.;
Attain). Current ratio of 1.0 is a general convention, not a higher education standard. Days cash:
[the rating-agency median from the institution's rating report, an approximate comparison
because agencies calculate liquidity differently / no benchmark shown because no rating report
was provided]."
Under the chart, the table shows each ratio, its components, and its benchmark. Sentence: which
ratios are at or above their benchmark and which are below.
CHART OFFENSE.2: NET ASSETS, HOW MUCH CAN WE USE? (institution)
Data: Section F net assets, most recent audited year. Public institutions: add the foundation's
amounts, sorted into the groups below.
Four groups, least to most flexible:
1. "Tied up in buildings and equipment." Public: net investment in capital assets. Private: net
PP&E − long-term debt.
2. "Restricted permanently (endowment principal)." Public: restricted nonexpendable + foundation
net assets held in perpetuity. Private: with donor restrictions held in perpetuity.
3. "Restricted to purposes set by donors or law." Public: restricted expendable + foundation
restricted net assets not held in perpetuity. Private: with donor restrictions not held in perpetuity.
4. "Unrestricted: available for any purpose." Public: unrestricted + foundation net assets without
donor restrictions. Private: without donor restrictions − group 1.
The groups must add up to total net assets. Public only: also show adjusted unrestricted,
calculated as in OFFENSE.1.
Horizontal bars in the order above, from the top: groups 1 to 3 in gray, group 4 in a bold
contrasting color, each labeled "$310.5M (41%)"; negative bars extend left of a clear zero line.
Public: group 4 as two bars, "As reported" and "Adjusted for pension/OPEB."
Title: "How Much of [institution]'s Net Assets Can It Actually Use?" Subtitle: "Net assets by
restriction, [most recent year]. Total net assets: $[total]."
Under the chart, the table shows each group, the lines it includes, its amount, and its share.
Sentence: "[share]% of total net assets is available for any purpose." Public: give both shares.
CHART OFFENSE.3: FACILITIES, AGE AND REINVESTMENT (institution)
Data: Section F. Average age (years) = accumulated depreciation ÷ depreciation expense.
Capital reinvestment ratio = purchases of capital assets ÷ depreciation expense. "n/m" if an input
is NOT FOUND.
Two panels side by side, axes starting at zero. Left: "Average Age of Facilities" ("Roughly how
many years old are our buildings and equipment?"), one dark bar labeled "[value] years." Right:
"Capital Reinvestment Ratio" ("Are we renewing facilities as fast as they wear out?"), one dark
bar labeled "[value]x," with a dashed line at 1.0x labeled "1.0x = spending keeps pace with
depreciation."
Title: "Is [institution] Keeping Up with Its Facilities?" Subtitle: "[most recent year]".
Small note at the bottom of the image: "Average age is an accounting estimate, not a measure of
physical condition. Capital spending includes new buildings as well as renewal, and can swing
widely from year to year because of a single large project. A facilities condition assessment, if
your institution has one, measures deferred maintenance directly."
Sentence: whether capital spending was above or below depreciation expense, and by how
much.
CHART DEFENSE.1: 10% EXPENSE REDUCTION (unit)
Data: Section A current-budget expenses by bucket. Calculate the total, 10% of it, each bucket's
share, and the 10% amount as a share of Stuff and of Space and Stuff combined.
Horizontal bars on one scale: People, Space, Stuff in gray, each labeled "$9.8M (72%)"; then a
bar labeled "10% cut" in a bold contrasting color, labeled with its dollars.
Title: "A 10% Cut to [unit]'s Budget = $[amount]". Subtitle: "[budget year] budget. A 10% cut
equals [share]% of everything the unit spends on Space and Stuff combined."
Sentence: "A 10% cut equals [a]% of Stuff and [b]% of Space and Stuff combined." If the cut is
larger than all of Stuff, say so.
DATA SUMMARY (after the last chart)
1. Each file: what it is, fiscal year, units, accounting standard, audited or not. Then the Unit data
choice you applied (UPLOAD or SKIP), and why, if it differs from what I wrote, and which unit
years you had.
2. Totals by year, with page citations: institution included revenue, total expenses, total net
assets; unit revenue and expenses.
3. Judgment calls: revenue lines you excluded, lines that mix buckets, and how you placed
amortization and scholarship allowances.
4. Anything NOT FOUND, any check that failed, any overlap mismatch between two reports of the
same year and how it was resolved, and anything you were unsure about.
5. The five largest numbers you used, with page citations, so I can spot-check them.
===== END ORIGINAL RULES =====

DATA SUMMARY SOURCE: take items 1–4 from the JSON's meta, checks, overlap_checks, overrides, classification_differences, judgment_calls, and not_found, and the citations from each value's "src".

JSON DATABASE: the uploaded file database.json (or database.txt), or the database.json built earlier in this chat.
Only if your tool cannot accept the upload, paste the complete file below this line.
```

## Stage 5 prompt: interactive HTML dashboard

Run in the same chat as Stage 4 so the chart specifications are already present. In a new chat, upload `database.json` again and paste the Stage 4 block from BEGIN ORIGINAL RULES to END ORIGINAL RULES where marked. Download the HTML file the tool creates, save it as `dashboard.html`, and open it in a browser.

The dashboard calculates everything in the browser from the embedded JSON and can load a different `database.json`. Once one dashboard works, classmates can reuse it with their own JSON instead of regenerating it, which removes Stage 5 as a failure point on weaker tools.

```text
STAGE 5 OF 5: BUILD ONE STANDALONE INTERACTIVE HTML DASHBOARD.

GOAL: a single .html file that reproduces all 12 charts, their tables and sentences, and the DATA SUMMARY, as specified in the ORIGINAL RULES (CHART RULES, the 12 CHART sections, and DATA SUMMARY), using interactive JavaScript charts instead of matplotlib images.

[If this is a new chat, paste the Stage 4 block from "===== BEGIN ORIGINAL RULES" to "===== END ORIGINAL RULES =====" here.]

WHAT CARRIES OVER UNCHANGED from the ORIGINAL RULES: every title and subtitle wording, chart order, chart type, sort order, bar order, colors (including CAGR green/red/gray rules and light gray / medium gray / dark contrasting year colors), dollar label format ($1.2M, $450K), CAGR formula and "+4.2%/yr" format, n/m rules, notes at the bottom of charts, benchmark lines and their labels, the table and the one sentence under each chart, the unit-chart skip rule, "(unaudited)" subtitles, no gridlines, no 3D, legends only where specified, white background.

WHAT CHANGES for the web (these replace the matplotlib-specific lines only):
- Use Plotly.js loaded with exactly this tag in <head>: <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>. No other external files, libraries, fonts, or images.
- "6.5 inches wide, landscape, 200 dpi" becomes: each chart fills its container width up to 900px, with the same height-to-width ratio as the spec (about 0.62 for landscape; about 0.92 for OFFENSE.1). Taller where the spec says to make the image taller.
- "Show each chart as an image in this chat" and "Don't create files" do not apply to this stage.
- Hover on any bar, point, or segment shows its exact dollar value and the JSON "src" citation for each input.

DATA AND CALCULATION
1. Embed database.json (uploaded, or built earlier in this chat), unchanged, inside <script type="application/json" id="db">. If you can run code, write the HTML file with code that reads database.json and inserts its exact contents, so no number is retyped. First confirm it loads as complete JSON, as in the Stage 4 DATA SOURCE check.
2. Compute every total, share, CAGR, ratio, and sentence in JavaScript from that JSON at page load. Never type a computed value into the HTML. Never hard-code institution or unit names; read them from meta.
3. Write one function per chart, named render_101_1, render_101_2, ... render_DEFENSE_1, plus render_summary. Each reads only the JSON.
4. A JSON value of null is NOT FOUND or N/A. Apply the spec's n/m and "can't be made" rules; never substitute zero.
5. If meta.unit_data_applied is SKIP, each unit chart shows only the spec's skip line.
6. The JSON has kit_schema "database-v2". Amounts are stored by column key under "values", "totals", and similar objects. "Earlier year," "later year," and "both audited years" mean the selected earlier and later institution years, which default to meta.chart_years.earlier and meta.chart_years.later. "Oldest actuals," "prior-year actuals," and "current budget" mean the selected unit columns, which default to meta.unit_chart_columns (oldest, prior, budget). "Most recent audited year" means the selected later year, so Section F is F_balance_sheet[later year]. Years between two columns = the months between their meta.year_ends dates ÷ 12. Chart 201.1 also plots every year in meta.inst_years between the earlier and later year.

PAGE LAYOUT
- Top: institution name, unit name, fiscal years, and audited status from meta.
- Year selectors at the top: "Earlier year" and "Later year" dropdowns listing meta.inst_years, and "Oldest actuals," "Prior-year actuals" (with a None option), and "Current budget" dropdowns listing meta.unit_columns. Changing one recalculates and re-renders every chart, table, sentence, and the Calculation check. If no balance sheet exists for the selected later year, the OFFENSE charts say so instead of drawing.
- A left-side or top menu linking to each chart, the DATA SUMMARY, and the DATABASE panel.
- Each chart section: the one-line "Chart number: Title" text, the chart with its title and subtitle drawn inside the chart area, the table of values, then the one sentence. Nothing else.
- DATA SUMMARY section: items 1–5 from the spec, built from meta, checks, overlap_checks, overrides, classification_differences, judgment_calls, not_found, and src values.
- DATABASE panel: a read-only view of the JSON; a "Load database.json" file button that replaces the data and re-renders every chart (it accepts only kit_schema "database-v2"; for anything else it shows a message and keeps the current data); a "Download JSON" button.
- A "Calculation check" table listing every computed total, CAGR, and ratio, so I can compare it to Stage 4.
- Print: each chart section on its own page.

OUTPUT
- Save the complete HTML as a downloadable file named dashboard.html and give me the link. If your tool cannot create files but has a canvas or code document, put the complete HTML there.
- Otherwise print it in a single code block. If it will not fit, split it only between render functions, label each block "PART 1 OF N", "PART 2 OF N", and end each with "Type continue for PART n." The parts must paste together, in order, into one working file.
- Never abbreviate code with comments such as "...rest of charts here" or "similar to above". Every render function must be complete.
- After the HTML, list any spec item you could not reproduce in Plotly, with the reason. Then stop.

JSON DATABASE: the uploaded file database.json (or database.txt), or the database.json built earlier in this chat.
Only if your tool cannot accept the upload, paste the complete file below this line.
```

The Plotly script URL above was checked on Nov 23, 2026 and returned HTTP 200. If the page shows no charts, open the browser's developer console; a 404 on the script means the URL needs updating.

## Platform notes

The biggest cross-platform fixes are mechanical: send the tool fewer pages, one file per response, and move JSON as downloaded and uploaded files instead of copying and pasting it. Platform-specific claims below come from my general knowledge as of mid-2026 and from classroom runs, not systematic testing; features and limits change, so verify each in your own tool.

### Techniques for every platform

- **Trim long PDFs.** Keep only the statements and the notes Stage 1 lists (see Trimming a PDF). Check the last-page quote in Stage 1 against your PDF: a tool that claims to read the whole file but quotes the wrong text is reading part of it.
- **Short parts, saved by code.** Stage 2 extracts one part per response and adds it to `database.json` with code, so no response holds much and nothing is retyped. Check the COUNT lines each time: they show what is actually in the file.
- **Upload JSON; never paste it.** Stages 4 and 5 expect `database.json` as an upload and check that it loaded completely. Rename `.json` to `.txt` if the tool rejects the upload. If a tool cannot create downloadable files, run Stages 4 and 5 in the same chat as Stage 2; they read the database from the chat.
- **Split long prompts.** If a tool truncates or rejects a long message, send it in parts. Start Part 1 with: `This prompt arrives in 2 parts. After each part, reply only "Received part N." Begin work only after the final part.` Split Stage 2 after END ORIGINAL RULES; split Stage 4 after CHART 201.2.
- **Start fresh when the tool drifts.** Signs: bracketed placeholders on a chart, an example institution name, numbers that differ from the JSON. Open a new chat and resume from the latest `database.json`; that is what it is for.
- **Compare to the answer key** before trusting any platform (see Testing).

### By platform

| Platform | Recommended setup | Expected weak point | Mitigation |
| --- | --- | --- | --- |
| Claude | Default chat with file creation enabled | Long Stage 4 output may need several "continue" turns | None beyond the kit |
| ChatGPT | A model with the data analysis / code tool on | Occasionally re-reads PDFs instead of the JSON | The DATA SOURCE line in Stage 4; check the Calculation check table |
| Gemini | Gemini app with the most capable model on your plan; Canvas for Stage 5. Google AI Studio is an alternative with adjustable output length (unverified for your account) | May describe code rather than run it, or show tables instead of chart images (unverified). May not keep or offer files between turns (unverified). Compared overlapping years inconsistently when it did the comparison itself (observed) | If Stage 2 says NO CODE, let it print each part as a table and the whole database once at FINISH; save that as `database.json`, or run Stages 4 and 5 in the same chat. If Stage 4 returns tables only, accept them and rely on Stage 5 |
| Microsoft 365 Copilot (work account) | Copilot Chat; it ran Python and offered downloads even on the Basic plan (observed). The Analyst agent, if your tenant offers it | Reads only the first ~129,000 characters of a long PDF (observed); loses an uploaded PDF after a few turns and asks for it again (observed); when parts were printed instead of saved, its end-of-stage merge wrote a nearly empty `database.json` and still reported success (observed); truncated a pasted `database.json` (observed) | Trim every report to the pages Stage 1 lists; attach the PDF again whenever it asks; check the COUNT lines after every part; attach the latest `database.json` if it loses the file; upload `database.json` in Stages 4 and 5 |
| Consumer Copilot | Not recommended | Limited file handling for multi-file financial statements (unverified) | Run Stages 1–3 elsewhere and use Copilot only for Stage 5 if needed |

### Gemini and Copilot test order

Run Stage 1 first and check the last-page quotes and the coverage table. Then run Stage 2 and score `database.json` against the answer key before spending time on charts. If extraction fails, the charts will fail too, and that tells you the tool's limit is reading financial statements, not drawing.

## Testing protocol

A platform passes only if its JSON matches a hand-verified answer key. Without the key you are comparing how plausible the outputs look, not whether they are right.

1. **Build the answer key once.** Run Stages 1–3 on your strongest tool with one institution's documents, including at least two consecutive reports so the overlap check runs. Verify every value in the merged JSON against its cited page, not just the Stage 3 sample. Save it as `answer_key.json`.
2. **Cover the code paths.** The rules branch on public vs. private and UPLOAD vs. SKIP. Test at least one GASB institution with unit data and one FASB institution with SKIP. A tool can pass one and fail the other.
3. **Test the reading limit.** Give each platform one untrimmed full report. It passes if Stage 1 marks the file TRUNCATED and lists pages to keep, or if its last-page quote is correct. It fails if it claims to read the whole file and the quote is wrong.
4. **Run each platform from a clean chat** with the same files and the same Stage 1 answers. Save each platform's final `database.json`.
5. **Compare** each merged JSON to the key with a text or JSON diff tool (VS Code's Compare, or a free online JSON diff).
6. **Score** with the table below.

| Measure | How to score | Pass |
| --- | --- | --- |
| Fabrication | Any value not traceable to a cited page, or any example/placeholder name | Zero. One instance fails the platform |
| Reading honesty | Stage 1 last-page quote matches the PDF, or the file is correctly marked TRUNCATED | Every file |
| Extraction accuracy | Share of key values matched exactly in whole dollars | 100% of totals; at least 95% of lines |
| Year-column and unit errors | Count values from the wrong year column, years taken from file names, or values not converted from thousands | Zero |
| Overlap agreement | MISMATCH rows in the MERGE SUMMARY that are extraction errors rather than restatements | Zero after Stage 3 |
| Citation accuracy | Check 10 random `src` values | 9 of 10 correct |
| Check honesty | Every FAIL in the key also reported as FAIL, not PASS | All |
| Chart compliance | For each chart: placeholders filled, sort and bar order, colors, CAGR sign and format, table and sentence present | 12 of 12 |
| Dashboard | Loads with no console errors; all 12 sections render; Calculation check matches Stage 4; loading the key JSON re-renders correctly | All four |
| Effort | Number of continue turns, trimmed files, and manual fixes needed | Record; no threshold |
