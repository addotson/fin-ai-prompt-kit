# Institutional Finance Charts: Multi-Stage Prompt Kit

Nov 23, 2026 · @Aaron

## How to use this kit

Run five prompts in order. Stage 2 produces a JSON database that Stages 4 and 5 read, so no stage after Stage 2 depends on the tool re-reading your PDFs or remembering a long conversation.

1. **Stage 1, inventory.** Upload all files, paste the Stage 1 prompt. The tool identifies each file and asks only the decisions the spec leaves open. Answer them.
2. **Stage 2, extraction.** Paste the Stage 2 prompt. The tool prints the database as JSON plus check results. Copy the JSON into a text file named `database.json` on your computer.
3. **Stage 3, review.** Spot-check the JSON against your PDFs using the checklist. Send corrections with the correction prompt. Save the corrected JSON.
4. **Stage 4, static charts.** Paste the Stage 4 prompt with the JSON at the bottom. The tool draws the 12 matplotlib charts and the data summary.
5. **Stage 5, dashboard.** Paste the Stage 5 prompt with the JSON at the bottom. The tool writes one interactive HTML file. Save it as `dashboard.html` and open it in a browser.

Rules for every platform: start a new chat for Stage 1; keep Stages 1–3 in the same chat; Stages 4 and 5 can run in a new chat, or a different tool, because they only need the JSON. Fill in the three blanks at the top of Stage 1 before sending.

### What changed from the original class prompt

The chart specifications, extraction rules, Sections A–F, checks, and CAGR formula are copied word for word. Only the lines below changed.

| Original line | Change | Reason |
| --- | --- | --- |
| "without stopping to ask me questions" | Stage 1 asks bounded questions, then stops | Your method: resolve judgment calls before extraction |
| "Never ask me to upload anything else" | Tool may list missing items once in Stage 1, but must proceed without them | Your method; still never blocks on, or invents, missing data |
| "Extract Sections A through F... Don't print them" | Stage 2 prints them as JSON | Portable database; lets a different tool chart it |
| "HOW TO WORK" steps 1–5 | Split across Stages 1, 2, 4 | Long single-pass tasks degrade on weaker tools (inference, not measured) |
| "Don't create files or documents" | Kept for Stage 4; Stage 5 creates one HTML file | Dashboard requirement |
| Page citation format unspecified | Defined as printed page number, with PDF page in brackets | Tools pick inconsistently; makes spot-checks possible |

The DATA SUMMARY still prints at the end of Stage 4. Stage 5 repeats it inside the dashboard.

## Stage 1 prompt: inventory and questions

Upload every file first, then paste this. Expect one response that ends with numbered questions.

```text
STAGE 1 OF 5: FILE INVENTORY AND QUESTIONS. Do not extract numbers or draw anything yet.

My institution: ________ My unit: ________
Unit data: ________ (write UPLOAD or SKIP)

This is the first of five stages. Later stages will extract data into a JSON database, draw 12 charts, and build an HTML dashboard. In this stage you only identify files and ask me the decisions you need.

WHAT I'VE PROVIDED
- Two years of my institution's audited financial statements: the most recent year, and one from
about three years earlier.
- Optional: my institution's most recent bond rating report.
- If Unit data is UPLOAD: my unit's current budget, its prior-year actuals, and its actuals from
about three years before the current budget, in one to three files.
- If Unit data is SKIP: no unit data. Skip the five unit charts.

DO THIS
1. Identify each file: what it is, the fiscal year it covers and its year-end, its units (dollars,
thousands, or millions), its accounting standard (GASB, FASB, IFRS, or other), and whether it is
audited. Use the names I typed above; if I left them blank, use the names in the files.
2. For each file, state whether you can read its text and tables. If a file is a scanned image you cannot read reliably, say so. Do not guess its contents.
3. State the page convention you will use: printed page number as shown on the page, followed by the PDF page in brackets, for example "p. 23 [PDF 31]".
4. Print a table: File name | What it is | Fiscal year | Year-end | Units | Standard | Audited? | Readable?
5. State which unit years you have (oldest actuals, prior-year actuals, current budget). If Unit data is UPLOAD but no unit files are present, say Unit data will be treated as SKIP.
6. List any item whose absence will prevent a specific chart, naming the chart. Do not ask me to upload it. Later stages will proceed without it.
7. Ask me only the questions below that apply to these files, numbered, one line each, with your proposed default answer in brackets. Ask nothing else.
   a. Private (FASB): does the statement of activities present an operating measure (case a) or not (case b)? State which you found and ask me to confirm.
   b. Public (GASB): is there a discretely presented foundation that holds gifts and endowment? Confirm it should be included where the spec says.
   c. Are hospital or health system amounts in separate columns? Confirm you will use academic columns only.
   d. Does the state pay pension or OPEB contributions on the institution's behalf (on-behalf payments)? If found, confirm exclusion.
   e. Scholarship allowances: are they combined with housing or other revenue? Is a tuition-only portion disclosed?
   f. Unit budget: list the current budget's expense categories and revenue categories as you found them. If there are more than 8, propose which to combine.
   g. Unit actuals: list any actuals line you cannot map to a current-budget category, with your proposed category.
   h. Any file whose fiscal year does not match what I described.
8. End with: "Answer the questions above, or reply DEFAULTS to accept all bracketed defaults. Then paste the Stage 2 prompt." Then stop.

Never invent, sample, or estimate any number. Never use an example or hypothetical institution or department.
```

## Stage 2 prompt: extraction to JSON

Paste after answering Stage 1, in the same chat. The rules between the BEGIN and END markers are the original prompt, unchanged. Save the final JSON as `database.json`.

```text
STAGE 2 OF 5: EXTRACT DATA INTO A JSON DATABASE. Do not draw charts. Do not calculate CAGRs or ratios.

Use the file identifications and my answers from Stage 1. If I replied DEFAULTS, use your bracketed defaults.

Never ask me to upload anything else. If something is missing, work with what you have, and
never fill the gap with invented, sample, or example numbers.
Unit data comes only from my unit files. If Unit data is UPLOAD but no unit budget or actuals files
are among the uploads, treat Unit data as SKIP and say so. Never invent a unit, never use an
example or hypothetical department, and never use institution-wide numbers, or a share of them,
in place of unit data. If the unit files have the current budget and the oldest actuals but not the
prior-year actuals, draw the unit charts with the two years you have and say so under each one.

===== BEGIN ORIGINAL RULES (unchanged) =====
EXTRACTION RULES
- Audited statements show two years side by side. Use only the column for the fiscal year that file
covers.
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
SECTION A: UNIT OPERATING EXPENSES (oldest actuals, prior-year actuals, current budget)
Every operating expense line, as labeled, with its amount in each of the three years. For each
line:
1. CATEGORY: no more than 8, using the current budget's own groupings. Assign the lines from
both actuals years to the same categories.
2. BUCKET: PEOPLE (salaries, wages, benefits, payroll taxes, stipends); SPACE (space or
occupancy charges, rent, utilities, maintenance and repairs, depreciation, interest); STUFF
(everything else).
Total operating expenses for each year.
SECTION B: INSTITUTION REVENUES (both audited years)
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
Total included revenue for each year.
TUITION DETAIL for each year: gross tuition and fees before discounts; each scholarship
allowance or institutional aid line subtracted from tuition; and whether those allowances also
cover other revenue such as housing. If gross tuition isn't on the face of the statements, look in
the notes or for a phrase such as "net of scholarship allowances of $___."
SECTION C: UNIT REVENUES (oldest actuals, prior-year actuals, current budget)
Every revenue line, as labeled, with its amount in each of the three years, including allocations or
transfers from the central institution. Use the current budget's categories, no more than 8,
combining the smallest into "Other." Assign the lines from both actuals years to those categories;
put a line that fits none in "Other." Total revenue for each year.
SECTION D: INSTITUTION EXPENSES (both audited years)
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
Total expenses for each year.
SECTION E: UNIT TOTALS (oldest actuals, prior-year actuals, current budget)
Total revenue and total expenses for each year, matching the totals in Sections A and C. Record
separately any transfers or allocations from the central institution, and any transfers out.
SECTION F: BALANCE SHEET AND FACILITIES (most recent audited year)
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
CHECKS (do these before drawing; no one else will check these numbers before the charts are
made)
- Each audited file's numbers come from the column for its own fiscal year.
- Amounts reported "in thousands" or "in millions" were converted.
- Included plus excluded revenue lines equal the statement's total revenues, operating plus
nonoperating.
- Section D lines equal the statement's total operating expenses, plus any interest you added.
- Net asset classes add up to total net assets.
- Unit lines add up to the stated totals in each unit year.
- Count the years between the two audited statements, and between the oldest unit actuals and
the current budget.
If a check fails, re-read the source and correct it. If it still fails, continue, and report it in the DATA
SUMMARY.
===== END ORIGINAL RULES =====

OUTPUT FORMAT FOR THIS STAGE (replaces "Don't print them")
1. Work one section at a time, in order A, B, C, D, E, F. Finish reading a section's source pages before writing its JSON.
2. Print a CHECKS table first: Check | PASS / FAIL / N/A | Detail (the two numbers compared). If Unit data is SKIP, mark unit checks N/A.
3. Then print the database as ONE JSON object in a code block, following the schema below exactly. Use the key names shown. Do not add commentary inside the JSON.
4. Every number is an object {"v": <whole-dollar integer, or null if NOT FOUND>, "src": "<page or sheet!row>"}. Negative numbers stay negative. Never write thousands or millions.
5. Every null value whose src is not "N/A" also appears in "not_found". "N/A" means the item does not apply to this institution; NOT FOUND means it applies but you could not find it.
6. If Unit data is SKIP, set A, C, and E to null.
7. If the JSON will not fit in one response, stop at the end of a complete line, write "Type continue for the rest of the JSON," and resume exactly where you stopped, so the blocks paste together into one valid JSON.
8. After the JSON, write: "Stage 2 complete. Save this JSON. Review it with the Stage 3 checklist." Then stop.

SCHEMA (angle brackets describe the value; they are not data)
{
 "meta": {
  "institution": "<name>", "unit": "<name or null>",
  "unit_data_requested": "UPLOAD|SKIP", "unit_data_applied": "UPLOAD|SKIP", "unit_data_reason": "<text>",
  "basis": "GASB|FASB_case_a|FASB_case_b|IFRS|other", "currency": "<ISO code>", "audited": <true|false>,
  "page_convention": "printed page [PDF page]",
  "files": [{"file": "", "what": "", "fiscal_year": "", "year_end": "", "units": "", "standard": "", "audited": <bool>, "readable": <bool>}],
  "inst_years": {"earlier": "<FY label>", "later": "<FY label>", "years_between": <number>},
  "unit_years": {"oldest": "<FY label or null>", "prior": "<FY label or null>", "budget": "<FY label or null>", "years_between_oldest_and_budget": <number or null>},
  "user_decisions": [{"question": "", "answer": ""}]
 },
 "A_unit_expenses": {
  "categories": ["<current-budget category names, max 8>"],
  "lines": [{"label": "<as labeled>", "category": "", "bucket": "PEOPLE|SPACE|STUFF", "oldest": <num>, "prior": <num>, "budget": <num>}],
  "totals": {"oldest": <num>, "prior": <num>, "budget": <num>}
 },
 "B_inst_revenue": {
  "lines": [{"label": "", "operating": <bool>, "included": <bool>, "exclusion_reason": "<text or null>", "category": "<one of the 8 Section B categories, or null if excluded>", "earlier": <num>, "later": <num>}],
  "total_included": {"earlier": <num>, "later": <num>},
  "statement_total_revenues": {"earlier": <num>, "later": <num>},
  "tuition": {
   "earlier": {"gross": <num>, "allowances": [{"label": "", "amount": <num>}], "allowances_cover_other_revenue": <bool>, "tuition_portion_of_allowances": <num>},
   "later": {"gross": <num>, "allowances": [{"label": "", "amount": <num>}], "allowances_cover_other_revenue": <bool>, "tuition_portion_of_allowances": <num>}
  }
 },
 "C_unit_revenue": {
  "categories": ["<max 8, including Other if used>"],
  "lines": [{"label": "", "category": "", "is_central_allocation": <bool>, "oldest": <num>, "prior": <num>, "budget": <num>}],
  "totals": {"oldest": <num>, "prior": <num>, "budget": <num>}
 },
 "D_inst_expenses": {
  "source_of_natural_classification": "<statement or note name>",
  "lines": [{"label": "", "bucket": "PEOPLE|SPACE|STUFF", "interest_added_from_outside_operating": <bool>, "earlier": <num>, "later": <num>}],
  "totals": {"earlier": <num>, "later": <num>},
  "statement_total_operating_expenses": {"earlier": <num>, "later": <num>}
 },
 "E_unit_totals": {
  "oldest": {"revenue": <num>, "expenses": <num>, "central_transfers_in": <num>, "transfers_out": <num>},
  "prior": {"revenue": <num>, "expenses": <num>, "central_transfers_in": <num>, "transfers_out": <num>},
  "budget": {"revenue": <num>, "expenses": <num>, "central_transfers_in": <num>, "transfers_out": <num>}
 },
 "F_balance_sheet": {
  "year": "<FY label>",
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
 },
 "checks": [{"check": "", "status": "PASS|FAIL|N/A", "detail": ""}],
 "judgment_calls": ["<excluded revenue lines and why; lines that mix buckets; placement of amortization and scholarship allowances>"],
 "not_found": [{"section": "", "item": ""}]
}
<num> means {"v": integer or null, "src": "page or sheet!row"}. Use null for <num> fields that do not apply (for example, net_assets_private at a public institution) and set src to "N/A".
```

## Stage 3: review and correct

This stage is you, not the tool. It takes about 15 minutes and is the main defense against a confident wrong number reaching a chart.

- [ ] Any check marked FAIL: open the cited page and find the error yourself before asking the tool.
- [ ] Five largest numbers (usually total revenue, total expenses, total net assets, salaries, net tuition): open each `src` page and confirm the amount and the year column.
- [ ] Units: pick one line from a statement reported in thousands and confirm the JSON value has three extra zeros.
- [ ] Year columns: confirm the earlier-year file's values match that file's own year column, not the comparative column in the later file.
- [ ] Excluded revenue lines: confirm each `exclusion_reason` matches the Section B rule.
- [ ] `not_found`: confirm each item is genuinely absent. A tool that missed a note page will list it here.
- [ ] Unit data: confirm no unit value equals an institution value or a round share of one.
- [ ] JSON validity: paste the file into a JSON validator (any free online validator, or open it in a browser). Fix stray commas or truncation before Stage 4.

Correction prompt, same chat:

```text
STAGE 3 CORRECTIONS. Apply only these changes to the JSON database, re-run the CHECKS that the changes affect, and reprint the full corrected JSON in the same schema. Do not change any other value.

1. <field path, e.g. D_inst_expenses.lines["Supplies and services"].later> should be <amount> per <page>.
2. ...
```

If the tool changes values you did not list, compare the old and new JSON (a text diff tool works) and reject the extra changes.

## Stage 4 prompt: the 12 charts

Works in the same chat or a new one. Paste the full corrected JSON where marked. Everything between the markers is the original prompt, unchanged.

```text
STAGE 4 OF 5: DRAW THE 12 CHARTS FROM THE JSON DATABASE BELOW.

DATA SOURCE: Use only the JSON database pasted at the end of this message. Do not re-read the uploaded files for numbers. Do not change any value in the JSON. Each "v" is whole dollars; each "src" is the citation. Section names in the rules map to JSON keys: Section A = A_unit_expenses, B = B_inst_revenue, C = C_unit_revenue, D = D_inst_expenses, E = E_unit_totals, F = F_balance_sheet. Institution and unit names, fiscal years, basis (public GASB vs. private FASB), audited status, and Unit data choice are in "meta". A null value is NOT FOUND or N/A.

Do not ask me questions in this stage. Extract nothing new: your job is to calculate and draw. Do not analyze or interpret.

===== BEGIN ORIGINAL RULES (unchanged) =====
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
revenue and expenses.
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
4. Anything NOT FOUND, any check that failed, and anything you were unsure about.
5. The five largest numbers you used, with page citations, so I can spot-check them.
===== END ORIGINAL RULES =====

DATA SUMMARY SOURCE: take items 1–4 from the JSON's meta, checks, judgment_calls, and not_found, and the citations from each value's "src".

JSON DATABASE:
<paste the full corrected database.json here>
```

## Stage 5 prompt: interactive HTML dashboard

Run in the same chat as Stage 4 so the chart specifications are already present. In a new chat, paste the Stage 4 block from BEGIN ORIGINAL RULES to END ORIGINAL RULES where marked. Save the output as `dashboard.html` and open it in a browser.

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
1. Embed the JSON database below, unchanged, inside <script type="application/json" id="db">.
2. Compute every total, share, CAGR, ratio, and sentence in JavaScript from that JSON at page load. Never type a computed value into the HTML. Never hard-code institution or unit names; read them from meta.
3. Write one function per chart, named render_101_1, render_101_2, ... render_DEFENSE_1, plus render_summary. Each reads only the JSON.
4. A JSON value of null is NOT FOUND or N/A. Apply the spec's n/m and "can't be made" rules; never substitute zero.
5. If meta.unit_data_applied is SKIP, each unit chart shows only the spec's skip line.

PAGE LAYOUT
- Top: institution name, unit name, fiscal years, and audited status from meta.
- A left-side or top menu linking to each chart, the DATA SUMMARY, and the DATABASE panel.
- Each chart section: the one-line "Chart number: Title" text, the chart with its title and subtitle drawn inside the chart area, the table of values, then the one sentence. Nothing else.
- DATA SUMMARY section: items 1–5 from the spec, built from meta, checks, judgment_calls, not_found, and src values.
- DATABASE panel: a read-only view of the JSON; a "Load database.json" file button that replaces the data and re-renders every chart; a "Download JSON" button.
- A "Calculation check" table listing every computed total, CAGR, and ratio, so I can compare it to Stage 4.
- Print: each chart section on its own page.

OUTPUT
- If you can create a downloadable file or a canvas/code document, put the complete HTML there.
- Otherwise print it in a single code block. If it will not fit, split it only between render functions, label each block "PART 1 OF N", "PART 2 OF N", and end each with "Type continue for PART n." The parts must paste together, in order, into one working file.
- Never abbreviate code with comments such as "...rest of charts here" or "similar to above". Every render function must be complete.
- After the HTML, list any spec item you could not reproduce in Plotly, with the reason. Then stop.

JSON DATABASE:
<paste the full corrected database.json here>
```

The Plotly version and URL are from my training knowledge, not checked against the live CDN. If the page shows no charts, open the browser's developer console; a 404 on the script means the URL needs updating.

## Platform notes

The biggest cross-platform fix is mechanical: attach the JSON as a file instead of pasting it, and split long prompts. Platform-specific claims below come from my general knowledge as of mid-2026 and were not tested; features and limits change, so verify each in your own tool.

### Techniques for every platform

- **Attach the JSON as a file.** In Stages 4 and 5, replace the paste marker with: `The JSON database is the attached file database.txt. Use it as the only data source.` Rename `.json` to `.txt` if the tool rejects the upload.
- **Split long prompts.** If a tool truncates or rejects a long message, send it in parts. Start Part 1 with: `This prompt arrives in 2 parts. After each part, reply only "Received part N." Begin work only after the final part.` Split Stage 2 after END ORIGINAL RULES; split Stage 4 after CHART 201.2.
- **Start fresh when the tool drifts.** Signs: bracketed placeholders on a chart, an example institution name, numbers that differ from the JSON. Open a new chat and resume from the saved JSON; that is what the database is for.
- **Compare to the answer key** before trusting any platform (see Testing).

### By platform

| Platform | Recommended setup | Expected weak point | Mitigation |
| --- | --- | --- | --- |
| Claude | Default chat with file creation enabled | Long Stage 4 output may need several "continue" turns | None beyond the kit |
| ChatGPT | A model with the data analysis / code tool on | Occasionally re-reads PDFs instead of the JSON | The DATA SOURCE line in Stage 4; check the Calculation check table |
| Gemini | Gemini app with the most capable model on your plan; Canvas for Stage 5. Google AI Studio is an alternative with adjustable output length (unverified for your account) | May describe code rather than run it, or show tables instead of chart images (unverified) | If Stage 4 returns tables only, accept them and rely on Stage 5. Ask Stage 5 to use Canvas so the HTML previews |
| Microsoft 365 Copilot (work account) | Copilot Chat with file upload; the Analyst agent if your tenant offers it, for Python | Per-message length limit; Python execution may be unavailable; tenant policy may block uploads (all unverified, varies by organization) | Attach the JSON as a file; split prompts; if no Python, use Stage 4's table fallback and Stage 5 |
| Consumer Copilot | Not recommended | Limited file handling for multi-file financial statements (unverified) | Run Stages 1–3 elsewhere and use Copilot only for Stage 5 if needed |

### Gemini and Copilot test order

Run Stage 1 and Stage 2 first and score the JSON against the answer key before spending time on charts. If extraction fails, the charts will fail too, and that tells you the tool's limit is reading financial statements, not drawing.

## Testing protocol

A platform passes only if its JSON matches a hand-verified answer key. Without the key you are comparing how plausible the outputs look, not whether they are right.

1. **Build the answer key once.** Run Stages 1–3 on your strongest tool with one institution's documents. Verify every value in the JSON against its cited page, not just the Stage 3 sample. Save it as `answer_key.json`.
2. **Cover the code paths.** The rules branch on public vs. private and UPLOAD vs. SKIP. Test at least one GASB institution with unit data and one FASB institution with SKIP. A tool can pass one and fail the other.
3. **Run each platform from a clean chat** with the same files and the same Stage 1 answers. Save each platform's JSON.
4. **Compare** each JSON to the key with a text or JSON diff tool (VS Code's Compare, or a free online JSON diff).
5. **Score** with the table below.

| Measure | How to score | Pass |
| --- | --- | --- |
| Fabrication | Any value not traceable to a cited page, or any example/placeholder name | Zero. One instance fails the platform |
| Extraction accuracy | Share of key values matched exactly in whole dollars | 100% of totals; at least 95% of lines |
| Year-column and unit errors | Count values from the wrong year column or not converted from thousands | Zero |
| Citation accuracy | Check 10 random `src` values | 9 of 10 correct |
| Check honesty | Every FAIL in the key also reported as FAIL, not PASS | All |
| Chart compliance | For each chart: placeholders filled, sort and bar order, colors, CAGR sign and format, table and sentence present | 12 of 12 |
| Dashboard | Loads with no console errors; all 12 sections render; Calculation check matches Stage 4; loading the key JSON re-renders correctly | All four |
| Effort | Number of continue turns and manual fixes needed | Record; no threshold |

Record results per platform:

| Platform and model | Institution type | Fabrication | Lines matched | Totals matched | Year/unit errors | Citations | Charts compliant | Dashboard | Fixes needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude |  |  |  |  |  |  |  |  |  |
| ChatGPT |  |  |  |  |  |  |  |  |  |
| Gemini |  |  |  |  |  |  |  |  |  |
| Copilot |  |  |  |  |  |  |  |  |  |
