#!/usr/bin/env python3
"""Write src/demo_fragments.json: SYNTHETIC fragments for the merge page demo and tests.

All names and numbers are made up. Deliberate problems for the merge page to catch:
- FY2025 "Federal grants & contracts": FY2025 report says 77.5M, FY2026 report's
  comparative column (marked restated) says 78.0M  -> MISMATCH.
- "Auxiliary enterprises" is category "Auxiliary enterprises" in FY2026, "Other" in FY2025
  -> classification difference.
- FY2024 and FY2020 appear only as comparative columns -> not used by default.
- The unit budget file also shows FY2025 and FY2023 actuals -> used for unit charts.
Run: python3 src/make_demo.py
"""
import json
from pathlib import Path

M = 1_000_000
NA = {"v": None, "src": "N/A"}


def n(v, src):
    return {"v": int(round(v)), "src": src}


def meta(unit=None):
    return {
        "institution": "Synthetic Test University (demo data)",
        "unit": unit,
        "unit_data_requested": "UPLOAD",
        "unit_data_applied": "UPLOAD",
        "unit_data_reason": "Unit budget file provided.",
        "basis": "GASB",
        "currency": "USD",
        "page_convention": "printed page [PDF page of the uploaded file]",
        "balance_sheet_years": "LATEST",
        "user_decisions": [{"question": "j. Balance sheet years", "answer": "LATEST"}],
    }


def col(key, ftype, role, end, heading, page, restated=False):
    return {"key": key, "fiscal_year": key.rstrip("AB"), "type": ftype, "role": role,
            "year_end": end, "heading_as_printed": heading, "heading_src": page, "restated": restated}


def inst(fname, units, own, comp, b_rows, d_rows, tuition, own_end, comp_end, f=None, restated=False):
    keys = [own, comp]
    b_lines = []
    for label, op, inc, reason, cat, vals in b_rows:
        b_lines.append({"label": label, "operating": op, "included": inc, "exclusion_reason": reason,
                        "category": cat,
                        "values": {k: n(vals[i], f"p. 14 [PDF {16 + i}]") for i, k in enumerate(keys)}})
    d_lines = []
    for label, bucket, vals in d_rows:
        d_lines.append({"label": label, "bucket": bucket, "interest_added_from_outside_operating": False,
                        "values": {k: n(vals[i], "p. 41 [PDF 43]") for i, k in enumerate(keys)}})
    tot_rev = {k: n(sum(r[5][i] for r in b_rows), "p. 14 [PDF 16]") for i, k in enumerate(keys)}
    tot_inc = {k: n(sum(r[5][i] for r in b_rows if r[2]), "p. 14 [PDF 16]") for i, k in enumerate(keys)}
    tot_d = {k: n(sum(r[2][i] for r in d_rows), "p. 41 [PDF 43]") for i, k in enumerate(keys)}
    return {
        "kit_schema": "fragment-v2",
        "file": {"file": fname, "kind": "institution", "what": "Audited financial statements (synthetic)",
                 "standard": "GASB", "audited": True, "units_in_source": units, "status": "OK",
                 "last_page_seen": "p. 60 [PDF 64]"},
        "meta": meta(),
        "columns": [col(own, "audited", "own", own_end, own_end[:4], "p. 12 [PDF 14]"),
                    col(comp, "audited", "comparative", comp_end, comp_end[:4] + (" (as restated)" if restated else ""),
                        "p. 12 [PDF 14]", restated)],
        "A_unit_expenses": None,
        "B_inst_revenue": {
            "lines": b_lines, "total_included": tot_inc, "statement_total_revenues": tot_rev,
            "tuition": {k: {"gross": n(tuition[i][0], "p. 30 [PDF 32]"),
                            "allowances": [{"label": "Scholarship allowances", "amount": n(tuition[i][1], "p. 30 [PDF 32]")}],
                            "allowances_cover_other_revenue": False,
                            "tuition_portion_of_allowances": n(tuition[i][1], "p. 30 [PDF 32]")}
                        for i, k in enumerate(keys)},
        },
        "C_unit_revenue": None,
        "D_inst_expenses": {"source_of_natural_classification": "Note 12, operating expenses by natural classification",
                            "lines": d_lines, "totals": tot_d, "statement_total_operating_expenses": tot_d},
        "E_unit_totals": None,
        "F_balance_sheet": f,
        "checks": [{"check": "Included plus excluded revenue lines equal total revenues", "column": own, "status": "PASS",
                    "detail": f"{tot_rev[own]['v']} = {tot_rev[own]['v']}"}],
        "judgment_calls": ["Capital appropriations excluded as capital revenue."],
        "not_found": [],
    }


def f_sheet(src="p. 12 [PDF 14]"):
    s = lambda v: n(v, src)
    return {
        "cash_and_equivalents": s(50 * M),
        "investments": [{"label": "Investments", "current": False, "restricted_or_endowment": False,
                         "held_by_foundation": False, "amount": s(150 * M)}],
        "investments_only_in_notes": False,
        "fasb_liquidity_available_within_one_year": NA,
        "current_assets": s(120 * M), "current_liabilities": s(60 * M),
        "net_assets_public": {"net_investment_in_capital_assets": s(400 * M), "restricted_nonexpendable": s(50 * M),
                              "restricted_expendable": s(80 * M), "unrestricted": s(-20 * M)},
        "net_assets_private": {"without_donor_restrictions": NA, "with_donor_held_in_perpetuity": NA,
                               "with_donor_not_in_perpetuity": NA},
        "total_net_assets": s(510 * M),
        "ppe_net": s(600 * M), "accumulated_depreciation": n(500 * M, "p. 33 [PDF 35]"),
        "depreciation_expense": n(30 * M, "p. 33 [PDF 35]"),
        "purchases_of_capital_assets": n(35 * M, "p. 16 [PDF 18]"),
        "long_term_debt": [{"label": "Bonds payable", "current": False, "amount": n(200 * M, "p. 36 [PDF 38]")}],
        "net_pension_liability": n(150 * M, "p. 44 [PDF 46]"), "net_opeb_liability": n(40 * M, "p. 50 [PDF 52]"),
        "pension_opeb_deferred_outflows": s(30 * M), "pension_opeb_deferred_inflows": s(20 * M),
        "foundation": {"present": False, "name": "", "total_expenses": NA, "without_donor_restrictions": NA,
                       "with_donor_held_in_perpetuity": NA, "with_donor_not_in_perpetuity": NA},
        "rating": {"provided": False, "agency": "", "rating": "", "median_days_cash": NA},
    }


def main():
    fy26 = inst(
        "Synthetic_Audit_FY26.pdf", "thousands", "FY2026", "FY2025",
        [("Tuition and fees, net of scholarship allowances", True, True, None, "Net tuition and fees", [120 * M, 115 * M]),
         ("State appropriations", False, True, None, "Government appropriations", [200 * M, 195 * M]),
         ("Federal grants and contracts", True, True, None, "Grants and contracts", [80 * M, 78 * M]),
         ("Auxiliary enterprises", True, True, None, "Auxiliary enterprises", [40 * M, 38 * M]),
         ("Capital appropriations", False, False, "Capital appropriation", None, [10 * M, 12 * M])],
        [("Salaries and wages", "PEOPLE", [250 * M, 240 * M]), ("Benefits", "PEOPLE", [90 * M, 86 * M]),
         ("Supplies and services", "STUFF", [60 * M, 58 * M]), ("Depreciation", "SPACE", [30 * M, 29 * M]),
         ("Scholarships and fellowships", "STUFF", [15 * M, 14 * M])],
        [(200 * M, 80 * M), (190 * M, 75 * M)], "2026-06-30", "2025-06-30",
        f={"FY2026": f_sheet()}, restated=True)
    fy25 = inst(
        "Synthetic_Audit_FY25.pdf", "thousands", "FY2025", "FY2024",
        [("Tuition and fees, net of scholarship allowances", True, True, None, "Net tuition and fees", [115 * M, 110 * M]),
         ("State appropriations", False, True, None, "Government appropriations", [195 * M, 190 * M]),
         ("Federal grants & contracts", True, True, None, "Grants and contracts", [77.5 * M, 75 * M]),
         ("Auxiliary enterprises", True, True, None, "Other", [38 * M, 36 * M]),
         ("Capital appropriations", False, False, "Capital appropriation", None, [12 * M, 8 * M])],
        [("Salaries and wages", "PEOPLE", [240 * M, 230 * M]), ("Benefits", "PEOPLE", [86 * M, 83 * M]),
         ("Supplies and services", "STUFF", [58 * M, 55 * M]), ("Depreciation", "SPACE", [29 * M, 28 * M]),
         ("Scholarships and fellowships", "STUFF", [14 * M, 13 * M])],
        [(190 * M, 75 * M), (180 * M, 70 * M)], "2025-06-30", "2024-06-30")
    fy21 = inst(
        "Synthetic_Audit_FY21.pdf", "dollars", "FY2021", "FY2020",
        [("Tuition and fees, net of scholarship allowances", True, True, None, "Net tuition and fees", [100_000_400, 98 * M]),
         ("State appropriations", False, True, None, "Government appropriations", [170 * M, 165 * M]),
         ("Federal grants and contracts", True, True, None, "Grants and contracts", [60 * M, 55 * M]),
         ("Auxiliary enterprises", True, True, None, "Auxiliary enterprises", [30 * M, 33 * M]),
         ("Capital appropriations", False, False, "Capital appropriation", None, [5 * M, 4 * M])],
        [("Salaries and wages", "PEOPLE", [210 * M, 205 * M]), ("Benefits", "PEOPLE", [75 * M, 72 * M]),
         ("Supplies and services", "STUFF", [50 * M, 48 * M]), ("Depreciation", "SPACE", [25 * M, 24 * M]),
         ("Scholarships and fellowships", "STUFF", [12 * M, 11 * M])],
        [(170 * M, 70 * M), (165 * M, 67 * M)], "2021-06-30", "2020-06-30")

    ukeys = ["FY2026B", "FY2025A", "FY2023A"]
    def uv(vals, src):
        return {k: n(vals[i], src) for i, k in enumerate(ukeys)}
    a_rows = [("Faculty salaries", "Personnel", "PEOPLE", [3_000_000, 2_900_000, 2_600_000]),
              ("Staff benefits", "Personnel", "PEOPLE", [1_000_000, 950_000, 850_000]),
              ("Supplies", "Operations", "STUFF", [400_000, 380_000, 350_000]),
              ("Space charges", "Facilities", "SPACE", [600_000, 580_000, 550_000])]
    c_rows = [("Central allocation", "Central allocation", True, [3_500_000, 3_400_000, 3_100_000]),
              ("Tuition revenue share", "Tuition share", False, [1_300_000, 1_250_000, 1_150_000]),
              ("Other income", "Other", False, [200_000, 190_000, 150_000])]
    a_tot = [sum(r[3][i] for r in a_rows) for i in range(3)]
    c_tot = [sum(r[3][i] for r in c_rows) for i in range(3)]
    unit = {
        "kit_schema": "fragment-v2",
        "file": {"file": "Synthetic_Unit_Budget_FY26.xlsx", "kind": "unit", "what": "Unit budget with prior actuals (synthetic)",
                 "standard": "other", "audited": False, "units_in_source": "dollars", "status": "OK",
                 "last_page_seen": "Budget!A1:F40"},
        "meta": meta("Department of Demo Studies (demo data)"),
        "columns": [col("FY2026B", "budget", "own", "2026-06-30", "FY26 Budget", "Budget!C3"),
                    col("FY2025A", "actual", "comparative", "2025-06-30", "FY25 Actual", "Budget!D3"),
                    col("FY2023A", "actual", "comparative", "2023-06-30", "FY23 Actual", "Budget!E3")],
        "A_unit_expenses": {"categories": ["Personnel", "Operations", "Facilities"],
                            "lines": [{"label": r[0], "category": r[1], "bucket": r[2],
                                       "values": uv(r[3], f"Budget!row{10 + i}")} for i, r in enumerate(a_rows)],
                            "totals": uv(a_tot, "Budget!row15")},
        "B_inst_revenue": None,
        "C_unit_revenue": {"categories": ["Central allocation", "Tuition share", "Other"],
                           "lines": [{"label": r[0], "category": r[1], "is_central_allocation": r[2],
                                      "values": uv(r[3], f"Budget!row{20 + i}")} for i, r in enumerate(c_rows)],
                           "totals": uv(c_tot, "Budget!row24")},
        "D_inst_expenses": None,
        "E_unit_totals": {k: {"revenue": n(c_tot[i], "Budget!row24"), "expenses": n(a_tot[i], "Budget!row15"),
                              "central_transfers_in": n(c_rows[0][3][i], "Budget!row20"),
                              "transfers_out": n(0, "Budget!row26")} for i, k in enumerate(ukeys)},
        "F_balance_sheet": None,
        "checks": [{"check": "Unit lines add up to stated totals", "column": "FY2026B", "status": "PASS", "detail": "5000000 = 5000000"}],
        "judgment_calls": [],
        "not_found": [],
    }
    out = Path(__file__).resolve().parent / "demo_fragments.json"
    out.write_text(json.dumps([fy26, fy25, fy21, unit], indent=1) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
