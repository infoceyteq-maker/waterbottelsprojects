#!/usr/bin/env python3
"""
Build the interactive project dashboard -> site/dashboard.html

Single self-contained HTML file (no CDN, no external JS) so it works offline
and inside the sandbox preview. Data is read from data/master-checklist.csv
and from the financial model defined below, so the dashboard can never drift
out of sync with the checklist.

Run:  python3 build/build_dashboard.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "dashboard.html")

# =============================================================================
# FINANCIAL MODEL
# =============================================================================
INVESTOR = "Mr. Thilakarathna"
LOCATION = "Bandarawela, Badulla District, Uva Province"

CAPACITY_BPH = 6000          # nameplate, PET line
SHIFT_HOURS = 8
WORK_DAYS_MONTH = 25
NAMEPLATE_MONTH = CAPACITY_BPH * SHIFT_HOURS * WORK_DAYS_MONTH   # 1,200,000 bottles

# SKU mix (share of PET bottle count) and unit economics in LKR
SKUS = [
    {
        "sku": "500 ml", "share": 0.40, "volume_l": 0.5,
        "costs": {
            "PET bottle (purchased, SLS 1336 marked)": 12.50,
            "Cap (PCO 1881)": 3.00,
            "Shrink sleeve label": 3.20,
            "Shrink film / packing": 1.20,
            "Water + treatment chemicals": 0.60,
            "Power": 1.80,
            "Consumables (filters, lab)": 0.50,
            "Direct labour": 2.20,
            "Maintenance & spares": 0.80,
            "Rejects & losses (3%)": 0.90,
        },
        "ex_factory_price": 48.00,
        "retail_price": 75.00,
    },
    {
        "sku": "1 L", "share": 0.25, "volume_l": 1.0,
        "costs": {
            "PET bottle (purchased, SLS 1336 marked)": 18.50,
            "Cap (PCO 1881)": 3.00,
            "Shrink sleeve label": 3.80,
            "Shrink film / packing": 1.40,
            "Water + treatment chemicals": 1.00,
            "Power": 2.60,
            "Consumables (filters, lab)": 0.70,
            "Direct labour": 2.60,
            "Maintenance & spares": 1.00,
            "Rejects & losses (3%)": 1.15,
        },
        "ex_factory_price": 65.00,
        "retail_price": 100.00,
    },
    {
        "sku": "1.5 L", "share": 0.20, "volume_l": 1.5,
        "costs": {
            "PET bottle (purchased, SLS 1336 marked)": 23.00,
            "Cap (PCO 1881)": 3.00,
            "Shrink sleeve label": 4.40,
            "Shrink film / packing": 1.60,
            "Water + treatment chemicals": 1.40,
            "Power": 3.20,
            "Consumables (filters, lab)": 0.85,
            "Direct labour": 2.80,
            "Maintenance & spares": 1.20,
            "Rejects & losses (3%)": 1.35,
        },
        "ex_factory_price": 82.00,
        "retail_price": 130.00,
    },
    {
        "sku": "5 L", "share": 0.15, "volume_l": 5.0,
        "costs": {
            "PET bottle (purchased, SLS 1336 marked)": 42.00,
            "Cap + handle (5 L screw cap)": 6.00,
            "Label (5 L)": 5.00,
            "Shrink film / packing": 2.20,
            "Water + treatment chemicals": 4.20,
            "Power": 7.50,
            "Consumables (filters, lab)": 2.00,
            "Direct labour": 3.20,
            "Maintenance & spares": 2.50,
            "Rejects & losses (3%)": 2.20,
        },
        "ex_factory_price": 200.00,
        "retail_price": 290.00,
    },
]

# 19 L returnable line (separate economics)
SKU_19L = {
    "sku": "19 L (returnable)", "volume_l": 19.0,
    "costs": {
        "PC bottle amortised (Rs 1,200 / 40 trips)": 30.00,
        "Cap amortised": 3.00,
        "Handle tag / label": 4.00,
        "Water + treatment chemicals": 6.00,
        "Power": 6.00,
        "Washing & sanitation chemicals": 4.00,
        "Labour + reverse logistics": 25.00,
        "Maintenance & spares": 5.00,
    },
    "ex_factory_price": 320.00,
    "retail_price": 420.00,
    "volume_month_y1": 20000,
}

# Fixed monthly operating costs, Year 1 (LKR)
FIXED_Y1 = {
    "Salaries (35 staff incl. sales team)": 2200000,
    "EPF 12% + ETF 3%": 330000,
    "Sales commission": 400000,
    "Marketing & trade promotion": 1500000,
    "Distribution (fuel, drivers, vehicle running)": 1800000,
    "Administration, office, IT, software": 250000,
    "Insurance (fire, product liability, transit)": 200000,
    "Maintenance contracts & spares": 350000,
    "Laboratory, calibration, external testing": 120000,
    "Pest control & waste disposal": 80000,
    "Utilities - non-production": 150000,
    "Depreciation (CAPEX / 10 years)": 1336000,
    "Working capital finance cost": 250000,
    "Professional fees (audit, CA, legal, secretarial)": 180000,
}

# CAPEX - everything needed up to the point of manufacturing (LKR)
# (name, qty, unit, unit_rate_lkr, category, in_kind)  ->  amount = qty * rate
# qty x rate is the source of truth for every amount, so the budget table can
# show Quantity | Unit | Rate | Amount and total itself.
CAPEX = [
    ("Land (Mr. Thilakarathna's contribution - in kind)",        400, "perches",    30000, "land",     True),
    ("Factory building shell + civil works (approx. 18,000 sq ft)", 1, "lot",    26000000, "building", False),
    ("Cleanroom filling room (ISO 8 / Class 100,000)",             1, "lot",      6000000, "building", False),
    ("Warehouse, offices, racking",                                1, "lot",      8000000, "building", False),
    ("Raw tank + sand filter (MGSF) + carbon filter (ACF) + softener", 1, "set",  4500000, "plant",    False),
    ("Reverse Osmosis plant (10 m3/hr) + membranes",               1, "plant",    9000000, "plant",    False),
    ("Ozone generator + UV sterilizer + 0.2 micron sterile filter", 1, "set",     2500000, "plant",    False),
    ("CIP system + SS316L piping + treated water tanks",           1, "lot",      4500000, "plant",    False),
    ("Re-mineralisation dosing + antiscalant dosing",              2, "skids",     350000, "plant",    False),
    ("Rinsing-Filling-Capping monoblock (6,000 BPH)",              1, "machine", 13000000, "plant",    False),
    ("Infeed conveyor + cap sorter + reject system",               1, "set",      2500000, "plant",    False),
    ("Date / batch coder (inkjet)",                                2, "units",     600000, "plant",    False),
    ("Shrink sleeve labelling machine + heat tunnel",              1, "line",     4500000, "plant",    False),
    ("Shrink wrap multi-packer",                                   1, "machine",  2800000, "plant",    False),
    ("Palletizer + stretch wrapper",                               1, "set",      1500000, "plant",    False),
    ("19 L / 5 gallon line (wash-fill-cap)",                       1, "line",     7000000, "plant",    False),
    ("Quality control laboratory (micro + chemical)",              1, "lab",      3500000, "plant",    False),
    ("CEB 3-phase connection + main panel + MCC",                  1, "lot",      3500000, "utility",  False),
    ("Oil-free food-grade air compressor + dryer",                 2, "units",    1600000, "utility",  False),
    ("Water chiller",                                              1, "unit",     2000000, "utility",  False),
    ("Standby generator 250 kVA",                                  1, "unit",     7500000, "utility",  False),
    ("Effluent treatment plant (ETP) + soakaway",                  1, "plant",    2200000, "env",      False),
    ("Fire systems, extinguishers, emergency lighting",            1, "lot",       900000, "env",      False),
    ("Pest control setup + waste management",                      1, "lot",       400000, "env",      False),
    ("Delivery vehicles (3 lorries / vans)",                       3, "vehicles", 6000000, "logistics", False),
    ("Forklift + pallets + pallet trucks",                         1, "set",      2500000, "logistics", False),
    ("Legal (NDA, MOU, shareholders agreement, land contracts)",   1, "lot",       900000, "pre",      False),
    ("Feasibility study + financial model",                        1, "study",     350000, "pre",      False),
    ("Hydrogeological survey + borewell drilling",                 2, "wells",    2250000, "pre",      False),
    ("Water testing (SLS 614 + bromide + heavy metals, 4 rounds)",  4, "rounds",    125000, "pre",      False),
    ("Architect + structural engineer + building approvals",       1, "lot",      1800000, "pre",      False),
    ("FCAU registration + SLSI audit + HACCP/GMP consultancy",     1, "lot",      1800000, "pre",      False),
    ("CEA EPL + environmental consultant",                         1, "lot",       600000, "pre",      False),
    ("Trademark + branding + label design",                        1, "lot",       900000, "pre",      False),
    ("Staff training (SLSI, GMP, machine operation)",              1, "lot",       500000, "pre",      False),
    ("Insurance + medical certificates + initial pest control",    1, "lot",       700000, "pre",      False),
]


# Stage 1 = from the day the project starts until the FACTORY IS OPEN
#           (land, building, civil, utilities to the building, approvals, well).
# Stage 2 = from the open factory until it is READY TO MANUFACTURE
#           (treatment train, filling line, packing, QC lab, product approvals).
# Anything not listed here is Stage 2.
STAGE1_ITEMS = {
    "Land (Mr. Thilakarathna's contribution - in kind)",
    "Factory building shell + civil works (approx. 18,000 sq ft)",
    "Cleanroom filling room (ISO 8 / Class 100,000)",
    "Warehouse, offices, racking",
    "CEB 3-phase connection + main panel + MCC",
    "Standby generator 250 kVA",
    "Effluent treatment plant (ETP) + soakaway",
    "Fire systems, extinguishers, emergency lighting",
    "Pest control setup + waste management",
    "Legal (NDA, MOU, shareholders agreement, land contracts)",
    "Feasibility study + financial model",
    "Hydrogeological survey + borewell drilling",
    "Water testing (SLS 614 + bromide + heavy metals, 4 rounds)",
    "Architect + structural engineer + building approvals",
    "CEA EPL + environmental consultant",
}

STAGE_TITLES = {
    1: ("අදියර 1 — පටන් ගත් දවසේ සිට කර්මාන්ත ශාලාව විවෘත කරන තෙක්",
        "Stage 1 - From day one until the factory is open"),
    2: ("අදියර 2 — කර්මාන්ත ශාලාව විවෘත කළා සිට නිෂ්පාදනය ආරම්භ කරන තෙක්",
        "Stage 2 - From the open factory until it can manufacture"),
}


def capex_rows(items=None):
    """Normalise to (name, qty, unit, rate, amount, category, in_kind, stage)."""
    rows = []
    for name, qty, unit, rate, cat, inkind in (items or CAPEX):
        stage = 1 if name in STAGE1_ITEMS else 2
        rows.append((name, qty, unit, rate, qty * rate, cat, inkind, stage))
    return rows
CONTINGENCY_PCT = 0.15
WORKING_CAPITAL = 28000000

# Capacity ramp - CONSERVATIVE. A brand-new bottled water brand does not hit
# A brand-new brand ramps. Year 1 averages 25% of nameplate, starting slow in
# Q1 and reaching roughly 40% by year end.
YEARS = [
    {"year": "Year 1", "utilisation": 0.25, "fixed_growth": 1.00, "v19l": 12000},
    {"year": "Year 2", "utilisation": 0.50, "fixed_growth": 1.18, "v19l": 30000},
    {"year": "Year 3", "utilisation": 0.75, "fixed_growth": 1.35, "v19l": 55000},
    {"year": "Year 4", "utilisation": 1.00, "fixed_growth": 1.55, "v19l": 80000},
]
TAX_RATE = 0.30

# Budget scenarios - line items deferred to a later phase to cut start-up cash.
SCENARIOS = [
    {
        "name": "Option A — Lean Start",
        "tag": "⭐ නිර්දේශිත / Recommended",
        "drop": ["Delivery vehicles (3 lorries / vans)",
                 "19 L / 5 gallon line (wash-fill-cap)",
                 "Forklift + pallets + pallet trucks",
                 "Palletizer + stretch wrapper",
                 "Shrink wrap multi-packer"],
        "reduce": {"Standby generator 250 kVA": 4500000,
                   "Rinsing-Filling-Capping monoblock (6,000 BPH)": 10500000},
        "wc": 20000000,
        "note": "වාහන වෙනුවට 3PL බෙදාහැරීම · 19L රේඛාව Phase 2 · අතින් pallet trucks · "
                "කුඩා generator · කුඩා monoblock. වෙළඳපොළ තහවුරු වූ පසු Phase 2 එකතු කරන්න.",
    },
    {
        "name": "Option B — Full Build",
        "tag": "සම්පූර්ණ / As costed",
        "drop": [],
        "reduce": {},
        "wc": 28000000,
        "note": "සියල්ල එකවර — වාහන, 19L රේඛාව, forklift, සම්පූර්ණ packing. "
                "ඉක්මන් වර්ධනයට හැකියි නමුත් ආරම්භක මුදල් අවශ්‍යතාව ඉහළයි.",
    },
    {
        "name": "Option C — Minimum Viable",
        "tag": "අවම / Smallest",
        "drop": ["Delivery vehicles (3 lorries / vans)",
                 "19 L / 5 gallon line (wash-fill-cap)",
                 "Forklift + pallets + pallet trucks",
                 "Palletizer + stretch wrapper",
                 "Shrink wrap multi-packer",
                 "Shrink sleeve labelling machine + heat tunnel",
                 "Warehouse, offices, racking"],
        "reduce": {"Standby generator 250 kVA": 3500000,
                   "Rinsing-Filling-Capping monoblock (6,000 BPH)": 7000000,
                   "Cleanroom filling room (ISO 8 / Class 100,000)": 4000000,
                   "Factory building shell + civil works (approx. 18,000 sq ft)": 18000000,
                   "Warehouse, offices, racking": 0,
                   "Quality control laboratory (micro + chemical)": 2500000},
        "wc": 14000000,
        "note": "කුඩා ගොඩනැඟිල්ල · self-adhesive ලේබල් (sleeve නොවේ) · සම්පූර්ණ 3PL · "
                "අවම QC lab. වේගයෙන් ආරම්භ කළ හැකි නමුත් ධාරිතාව සහ වර්ධන හැකියාව සීමිතයි.",
    },
]


def money(n, dp=0):
    return f"{n:,.{dp}f}"


def build_model():
    for s in SKUS:
        s["variable_cost"] = round(sum(s["costs"].values()), 2)
        s["contribution"] = round(s["ex_factory_price"] - s["variable_cost"], 2)
        s["margin_pct"] = round(s["contribution"] / s["ex_factory_price"] * 100, 1)
        s["label_qty_factor"] = 1.04          # 4% label wastage
        s["cap_qty_factor"] = 1.03            # 3% cap wastage
        s["bottle_qty_factor"] = 1.03         # 3% bottle wastage
        s["film_qty_factor"] = 1.05           # 5% shrink-film wastage

    SKU_19L["variable_cost"] = round(sum(SKU_19L["costs"].values()), 2)
    SKU_19L["contribution"] = round(SKU_19L["ex_factory_price"] - SKU_19L["variable_cost"], 2)
    SKU_19L["margin_pct"] = round(SKU_19L["contribution"] / SKU_19L["ex_factory_price"] * 100, 1)

    blend_variable = round(sum(s["share"] * s["variable_cost"] for s in SKUS), 2)
    blend_price = round(sum(s["share"] * s["ex_factory_price"] for s in SKUS), 2)
    blend_contribution = round(blend_price - blend_variable, 2)

    subtotal = sum(qty * rate for _, qty, _, rate, _, _ in CAPEX)
    land_value = sum(qty * rate for _, qty, _, rate, cat, _ in CAPEX if cat == "land")
    contingency = round(subtotal * CONTINGENCY_PCT)
    total_capex = subtotal + contingency
    cash_capex = total_capex - land_value
    total_investment = total_capex + WORKING_CAPITAL
    cash_investment = cash_capex + WORKING_CAPITAL

    dep_month = round(total_capex / 10 / 12)
    # keep depreciation in the fixed-cost block consistent with the actual CAPEX
    FIXED_Y1["Depreciation (CAPEX / 10 years)"] = dep_month

    # ---- budget scenarios ----
    scenarios = []
    for sc in SCENARIOS:
        items = []
        for name, qty, unit, rate, cat, inkind in CAPEX:
            if name in sc["drop"]:
                continue
            amt = qty * rate
            if name in sc["reduce"]:
                amt = sc["reduce"][name]
                if amt == 0:
                    continue
                rate = amt / qty          # qty is unchanged, so the rate moves
            items.append((name, qty, unit, rate, amt, cat, inkind))
        sub = sum(i[4] for i in items)
        cont = round(sub * CONTINGENCY_PCT)
        tc = sub + cont
        cc = tc - sum(i[4] for i in items if i[5] == "land")
        scenarios.append({
            "name": sc["name"], "tag": sc["tag"], "note": sc["note"],
            "subtotal": sub, "contingency": cont, "total_capex": tc,
            "working_capital": sc["wc"], "cash_capex": cc,
            "total_investment": tc + sc["wc"], "cash_investment": cc + sc["wc"],
            "items_dropped": len(sc["drop"]),
            "rows": items,
        })

    proj = []
    for y in YEARS:
        pet_bottles = round(NAMEPLATE_MONTH * y["utilisation"])
        pet_contribution = pet_bottles * blend_contribution
        v19 = y["v19l"]
        l19_contribution = v19 * SKU_19L["contribution"]
        revenue_pet = pet_bottles * blend_price
        revenue_19 = v19 * SKU_19L["ex_factory_price"]
        fixed = round(sum(FIXED_Y1.values()) * y["fixed_growth"])
        pbt_m = pet_contribution + l19_contribution - fixed
        pat_m = pbt_m * (1 - TAX_RATE)
        proj.append({
            "year": y["year"],
            "utilisation": y["utilisation"],
            "pet_bottles_m": pet_bottles,
            "pet_bottles_y": pet_bottles * 12,
            "v19_m": v19,
            "revenue_m": revenue_pet + revenue_19,
            "revenue_y": (revenue_pet + revenue_19) * 12,
            "variable_m": pet_bottles * blend_variable + v19 * SKU_19L["variable_cost"],
            "contribution_m": pet_contribution + l19_contribution,
            "fixed_m": fixed,
            "pbt_m": pbt_m,
            "pbt_y": pbt_m * 12,
            "pat_m": pat_m,
            "pat_y": pat_m * 12,
            "volume_l_m": round(pet_bottles * sum(s["share"] * s["volume_l"] for s in SKUS)
                                + v19 * 19),
        })

    fixed_base = sum(FIXED_Y1.values())
    breakeven_pet = round(fixed_base / blend_contribution)
    breakeven_pct = breakeven_pet / NAMEPLATE_MONTH

    # ---- sensitivity: net profit per year at different utilisations ----
    sensitivity = []
    for u in (0.15, 0.25, 0.35, 0.50, 0.70, 1.00):
        pb = round(NAMEPLATE_MONTH * u)
        c = pb * blend_contribution + 12000 * SKU_19L["contribution"] - fixed_base
        sensitivity.append({
            "util": u, "bottles": pb,
            "revenue_m": pb * blend_price + 12000 * SKU_19L["ex_factory_price"],
            "contribution_m": c + fixed_base,
            "pat_y": c * 12 * (1 - TAX_RATE),
        })

    # ---- sensitivity: price pressure on contribution ----
    price_sens = []
    for delta in (-0.15, -0.10, -0.05, 0.0, 0.05, 0.10):
        p = blend_price * (1 + delta)
        price_sens.append({
            "delta": delta, "price": p, "contribution": p - blend_variable,
            "margin": (p - blend_variable) / p * 100 if p else 0,
            "breakeven": round(fixed_base / (p - blend_variable)) if p > blend_variable else None,
        })

    # cumulative payback (on the recommended scenario = scenarios[0])
    target = scenarios[0]["cash_investment"]
    cumulative = 0.0
    payback_year = None
    payback_months = None
    for i, p in enumerate(proj, start=1):
        prev = cumulative
        cumulative += p["pat_y"]
        if cumulative >= target and payback_year is None:
            payback_year = i
            payback_months = round((target - prev) / p["pat_y"] * 12, 1) if p["pat_y"] > 0 else 0

    return {
        "investor": INVESTOR,
        "location": LOCATION,
        "capacity_bph": CAPACITY_BPH,
        "shift_hours": SHIFT_HOURS,
        "work_days": WORK_DAYS_MONTH,
        "nameplate_month": NAMEPLATE_MONTH,
        "skus": SKUS,
        "sku19": SKU_19L,
        "blend_variable": blend_variable,
        "blend_price": blend_price,
        "blend_contribution": blend_contribution,
        "blend_margin_pct": round(blend_contribution / blend_price * 100, 1),
        "fixed_y1": FIXED_Y1,
        "fixed_total_y1": sum(FIXED_Y1.values()),
        "capex": capex_rows(),
        "capex_subtotal": subtotal,
        "land_value": land_value,
        "contingency": contingency,
        "total_capex": total_capex,
        "cash_capex": cash_capex,
        "working_capital": WORKING_CAPITAL,
        "total_investment": total_investment,
        "cash_investment": cash_investment,
        "depreciation_month": dep_month,
        "stage_titles": STAGE_TITLES,
        "stage1_rows": [r for r in capex_rows() if r[7] == 1],
        "stage2_rows": [r for r in capex_rows() if r[7] == 2],
        "stage1_total": sum(r[4] for r in capex_rows() if r[7] == 1),
        "stage2_total": sum(r[4] for r in capex_rows() if r[7] == 2),
        "stage1_cash": sum(r[4] for r in capex_rows() if r[7] == 1 and not r[6]),
        "stage2_cash": sum(r[4] for r in capex_rows() if r[7] == 2 and not r[6]),
        "projection": proj,
        "scenarios": scenarios,
        "recommended": scenarios[0],
        "sensitivity": sensitivity,
        "price_sens": price_sens,
        "breakeven_pet": breakeven_pet,
        "breakeven_pct": breakeven_pct,
        "payback_year": payback_year,
        "payback_months": payback_months,
        "tax_rate": TAX_RATE,
    }


def load_checklist():
    with open(os.path.join(ROOT, "data", "master-checklist.csv"), newline="",
              encoding="utf-8") as fh:
        return list(csv.DictReader(fh))
