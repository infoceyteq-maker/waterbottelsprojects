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
        "ex_factory_price": 38.00,   # factory price - OURS
        "distributor_price": 50.00,
        "retail_price": 80.00,
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
        "ex_factory_price": 55.00,   # factory price - OURS
        "distributor_price": 70.00,
        "retail_price": 120.00,
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
        "ex_factory_price": 65.00,   # factory price - OURS
        "distributor_price": 90.00,
        "retail_price": 150.00,
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
        "ex_factory_price": 200.00,   # factory price - OURS
        "distributor_price": 300.00,
        "retail_price": 400.00,
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
    "ex_factory_price": 200.00,   # factory price - OURS
    "distributor_price": 350.00,
        "retail_price": 550.00,
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

# Map every CAPEX line onto the six budget documents the user organises by.
BUDGET_DOC = {
    "land":      "equipment",     # shown in-kind inside the equipment budget
    "building":  "equipment",
    "plant":     "equipment",
    "utility":   "equipment",
    "env":       "misc",
    "logistics": "transport",
    "pre":       "registration",
    "hr":        "hr",
}
# These lines leave their category and join another budget document.
BUDGET_OVERRIDE = {
    "Staff training (SLSI, GMP, machine operation)": "hr",
}
BUDGET_DOCS = [
    ("registration",  "📄 ලියාපදිංචි අයවැය", "Registration Budget"),
    ("equipment",     "⚙️ උපකරණ + ඉදිකිරීම් අයවැය", "Equipment Budget"),
    ("raw_material",  "🧴 අමුද්‍රව්‍ය අයවැය", "Raw Material Budget"),
    ("transport",     "🚚 ප්‍රවාහන අයවැය", "Transportation Budget"),
    ("hr",            "👷 මානව සම්පත් අයවැය", "HR Budget"),
    ("misc",          "📦 විවිධ අයවැය", "Miscellaneous Budget"),
]

# ---------------------------------------------------------------- HR BUDGET
# Organisation, department by department, with reporting levels.
#   level 0 = Board / investor, 1 = Plant Manager,
#   2 = department head,        3 = senior staff, 4 = line staff
DEPARTMENTS = [
    {
        "key": "mfg", "icon": "🏭",
        "si": "නිෂ්පාදන සහ තත්ත්ව පාලනය", "en": "Manufacturing & Quality",
        "roles": [
            ("Production Supervisor / නිෂ්පාදන පර්යේෂක",        2, 2,  85000),
            ("QC Manager (Chemist) / තත්ත්ව පාලන කළමනාකරු",     1, 2, 110000),
            ("Water Treatment Operator / ජල පිරිපහදු ශිල්පී",   2, 3,  48000),
            ("Machine Operator / යන්ත්‍ර ක්‍රියාකරු",            6, 3,  45000),
            ("QC Technician / තත්ත්ව පාලන තාක්ෂණවේදී",          2, 3,  55000),
            ("Maintenance Technician / නඩත්තු ශිල්පී",          2, 3,  55000),
            ("Storekeeper / ගබඩා භාරකරු",                       2, 3,  38000),
            ("Filling Line Worker / පිරවීමේ රේඛා සේවක",         8, 4,  32000),
        ],
    },
    {
        "key": "hrf", "icon": "💼",
        "si": "මානව සම්පත් සහ මුදල්", "en": "HR & Finance",
        "roles": [
            ("Accountant / ගිණුම්කරු",                          1, 2,  85000),
            ("Admin / HR Officer / පරිපාලන නිලධාරී",            1, 2,  70000),
            ("Security / ආරක්ෂක",                                3, 3,  30000),
            ("Cleaner / පිරිසිදු කරන්නන්",                      2, 3,  25000),
        ],
    },
    {
        "key": "sales", "icon": "📈",
        "si": "අලෙවි සහ නාමකරණ", "en": "Sales & Marketing",
        "roles": [
            ("Sales & Marketing Officer / අලෙවි නිලධාරී",       2, 2,  65000),
        ],
    },
    {
        "key": "transport", "icon": "🚚",
        "si": "ප්‍රවාහන", "en": "Transportation",
        "roles": [
            ("Transport Supervisor / ප්‍රවාහන පර්යේෂක",         1, 2,  70000),
            ("Driver / රියදුරු",                                 3, 3,  42000),
            ("Loader / Helper / භාණ්ඩ කරුවන්",                   4, 3,  28000),
        ],
    },
]
LEVEL_NAMES = {0: "Board / ආයෝජක", 1: "Plant Manager", 2: "Department head",
               3: "Senior staff", 4: "Line staff"}

# Top of the tree - not part of any department.
TOP_ROLE = ("Plant Manager / කර්මාන්ත ශාලා කළමනාකරු", 1, 175000)

# Flat (role, headcount, salary) list, derived from DEPARTMENTS so the payroll
# page and the org chart page always agree.
HR_PLAN = [(TOP_ROLE[0], TOP_ROLE[1], TOP_ROLE[2])] + [
    (r[0], r[1], r[3]) for d in DEPARTMENTS for r in d["roles"]
]

# ------------------------------------------------- OFFICE EQUIPMENT
# Requested: office equipment must appear in the setup budget too.
OFFICE_EQUIPMENT = [
    ("Office furniture - desks, chairs, cabinets",       1, "set",   850000),
    ("Computers + laptops",                              6, "units", 185000),
    ("Printer + multifunction + label printer",          1, "set",   320000),
    ("Networking - router, switch, cabling, Wi-Fi",      1, "lot",   250000),
    ("Telephone / intercom system",                      1, "lot",   180000),
    ("Office air conditioning",                          3, "units", 145000),
    ("CCTV (16 cameras) + access control",               1, "lot",   650000),
    ("Signage + branding boards",                        1, "lot",   280000),
    ("Pantry + water cooler + staff room",               1, "lot",   180000),
    ("Accounting / ERP software licence (year 1)",       1, "lot",   350000),
]

# ------------------------------------------------------- FIRST STOCK
# The investor's first order stock - the launch batch.
FIRST_STOCK = [
    ("500 ml", 5000),
    ("1 L",    3000),
    ("1.5 L",  3000),
    ("5 L",    1000),
    ("19 L",    150),
]

HR_ONE_OFF = [
    ("Recruitment + advertising / බඳවා ගැනීම",            1, 350000),
    ("Uniforms + PPE + safety shoes / නිල ඇඳුම් + ආරක්ෂක", 45,  18000),
    ("Initial training (SLSI, GMP, machines) / පුහුණුව",   1, 500000),
    ("Medical certificates / වෛද්‍ය සහතික",                45,   4500),
]

EPF_ER_PCT = 0.12          # employer EPF
ETF_PCT = 0.03             # employer ETF
HR_ONE_OFF = [
    ("Recruitment + advertising / බඳවා ගැනීම",            1, 350000),
    ("Uniforms + PPE + safety shoes / නිල ඇඳුම් + ආරක්ෂක", 45,  18000),
    ("Initial training (SLSI, GMP, machines) / පුහුණුව",   1, 500000),
    ("Medical certificates / වෛද්‍ය සහතික",                45,   4500),
]

STAGE_TITLES = {
    1: ("අදියර 1 — පටන් ගත් දවසේ සිට කර්මාන්ත ශාලාව විවෘත කරන තෙක්",
        "Stage 1 - From day one until the factory is open"),
    2: ("අදියර 2 — කර්මාන්ත ශාලාව විවෘත කළා සිට නිෂ්පාදනය ආරම්භ කරන තෙක්",
        "Stage 2 - From the open factory until it can manufacture"),
}


def capex_rows(items=None):
    """Normalise to (name, qty, unit, rate, amount, category, in_kind, stage, doc)."""
    rows = []
    for name, qty, unit, rate, cat, inkind in (items or CAPEX):
        stage = 1 if name in STAGE1_ITEMS else 2
        doc = BUDGET_OVERRIDE.get(name, BUDGET_DOC.get(cat, "misc"))
        rows.append((name, qty, unit, rate, qty * rate, cat, inkind, stage, doc))
    return rows


def raw_material_rows(nameplate_month, skus, sku19, v19=80000):
    """Monthly purchase budget across all products, wastage included.
    Returns [(material, qty, unit, unit_rate, amount), ...]."""
    acc = {}
    for sk in skus:
        base = nameplate_month * sk["share"]
        factors = {
            "PET bottle (purchased, SLS 1336 marked)": ("bottle_qty_factor", "බෝතල්"),
            "Cap (PCO 1881)": ("cap_qty_factor", "මූඩි"),
            "Cap + handle (5 L screw cap)": ("cap_qty_factor", "මූඩි"),
            "Shrink sleeve label": ("label_qty_factor", "ලේබල්"),
            "Label (5 L)": ("label_qty_factor", "ලේබල්"),
            "Shrink film / packing": ("film_qty_factor", "shrink film"),
        }
        for ckey, (fkey, _unit) in factors.items():
            if ckey not in sk["costs"]:
                continue
            q = round(base * sk[fkey])
            r = sk["costs"][ckey]
            key = ("PET bottles (SLS 1336)" if "bottle" in ckey else
                   "Caps" if "Cap" in ckey else
                   "Labels / shrink sleeves" if "abel" in ckey else
                   "Shrink film")
            p = acc.setdefault(key, [0, 0.0])
            p[0] += q
            p[1] += q * r
    rows = [(k, v[0], "units", (v[1] / v[0] if v[0] else 0), v[1])
            for k, v in acc.items()]
    # 19 L line
    for ckey, unit, qty in [("Handle tag / label", "ලේබල්", v19 * 1.04),
                            ("Cap amortised", "මූඩි", v19 * 1.03),
                            ("Washing & sanitation chemicals", "බෝතල්", v19)]:
        r = sku19["costs"][ckey]
        rows.append((f"19 L — {ckey}", round(qty), unit, r, round(qty) * r))
    return rows


def hr_monthly():
    """(headcount, gross, employer EPF+ETF, total) per month."""
    hc = sum(r[1] for r in HR_PLAN)
    gross = sum(r[1] * r[2] for r in HR_PLAN)
    er = gross * (EPF_ER_PCT + ETF_PCT)
    return hc, gross, er, gross + er


def hr_one_off_total():
    return sum(q * r for _, q, r in HR_ONE_OFF)
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


# ---------------------------------------------------------------------------
# Page derivations
# ---------------------------------------------------------------------------
# Packaging cost keys -> the wastage factor to apply (None = returnable, no wastage)
PACK_KEYS = {
    "PET bottle (purchased, SLS 1336 marked)": "bottle_qty_factor",
    "Cap (PCO 1881)": "cap_qty_factor",
    "Cap + handle (5 L screw cap)": "cap_qty_factor",
    "Shrink sleeve label": "label_qty_factor",
    "Label (5 L)": "label_qty_factor",
    "Shrink film / packing": "film_qty_factor",
    # 19 L returnable line - bottles are capital, amortised over 40 trips
    "PC bottle amortised (Rs 1,200 / 40 trips)": None,
    "Cap amortised": None,
    "Handle tag / label": None,
}
UTIL_KEYS = ("Water + treatment chemicals", "Power", "Consumables (filters, lab)",
             "Maintenance & spares", "Rejects & losses (3%)")


def _sku(name, skus=SKUS, sku19=SKU_19L):
    for sk in skus:
        if sk["sku"] == name:
            return sk
    if name == "19 L":
        return sku19
    raise KeyError(name)


def first_stock_cost(first_stock, skus=SKUS, sku19=SKU_19L):
    """Packaging cost of the first stock, product by product."""
    rows, total = [], 0.0
    for name, qty in first_stock:
        sk = _sku(name, skus, sku19)
        costs = sk["costs"]
        pack = sum(v for k, v in costs.items() if k in PACK_KEYS)
        rows.append([name, f"{qty:,}", f"{pack:,.2f}", f"{qty*pack:,.0f}"])
        total += qty * pack
    return rows, total


def first_stock_full(first_stock, skus=SKUS, sku19=SKU_19L):
    """Full variable cost (packaging + utilities + labour) of the first stock."""
    rows, cost, value = [], 0.0, 0.0
    detail = []
    for name, qty in first_stock:
        sk = _sku(name, skus, sku19)
        unit = sum(sk["costs"].values())
        price = sk["ex_factory_price"]
        cost += qty * unit
        value += qty * price
        detail.append({
            "sku": name, "qty": qty, "unit": unit, "total": qty * unit,
            "label": f'{"🫙" if name == "19 L" else "💧"} {name} — බෝතල් {qty:,}',
            "lines": [[k, f"{v:,.2f}", f"{qty*v:,.0f}"] for k, v in sk["costs"].items()],
        })
        rows.append([name, f"{qty:,}", f"{unit:,.2f}", f"{qty*unit:,.0f}",
                     f"{price:,.0f}", f"{qty*price:,.0f}",
                     f"{qty*(price-unit):,.0f}"])
    return rows, cost, value, detail


def first_production(first_stock, hr_month_total, skus=SKUS, sku19=SKU_19L):
    """Cost of the first production run: material + operating + wages."""
    mat_rows, mat_total = [], 0.0
    util = {k: 0.0 for k in UTIL_KEYS}
    for name, qty in first_stock:
        sk = _sku(name, skus, sku19)
        c = sk["costs"]
        b = round(qty * sk.get("bottle_qty_factor", 1.0))
        cp = round(qty * sk.get("cap_qty_factor", 1.0))
        lb = round(qty * sk.get("label_qty_factor", 1.0))
        fm = round(qty * sk.get("film_qty_factor", 1.0))
        if name == "19 L":            # returnable: no PET bottle, no shrink film
            b, fm = 0, 0
        pack = sum(v for k, v in c.items() if k in PACK_KEYS)
        mat_rows.append([name, f"{qty:,}", f"{b:,}", f"{cp:,}", f"{lb:,}", f"{fm:,}",
                         f"{qty*pack:,.0f}"])
        mat_total += qty * pack
        for k in UTIL_KEYS:
            if k in c:
                util[k] += qty * c[k]

    op_rows = [["ජලය + පිරිපහදු රසායන / Water + treatment chemicals",
                "බෝතලයකට අනුව", f'{util["Water + treatment chemicals"]:,.0f}'],
               ["විදුලිය / Power", "බෝතලයකට අනුව", f'{util["Power"]:,.0f}'],
               ["පරිභෝජන (පෙරහන්, lab) / Consumables", "බෝතලයකට අනුව",
                f'{util["Consumables (filters, lab)"]:,.0f}'],
               ["නඩත්තු + spare parts / Maintenance", "බෝතලයකට අනුව",
                f'{util["Maintenance & spares"]:,.0f}'],
               ["ප්‍රතික්ෂේප + හානි 3% / Rejects & losses", "බෝතලයකට අනුව",
                f'{util["Rejects & losses (3%)"]:,.0f}'],
               ["QC lab පරීක්ෂණ (batch) / QC testing", "එක වර", "150,000"],
               ["බෙදාහැරීමේ ප්‍රවාහන + ඉන්ධන / Delivery", "එක වර", "120,000"]]
    op_total = sum(float(r[2].replace(",", "")) for r in op_rows)
    sub = mat_total + op_total + hr_month_total
    cont = round(sub * 0.10)
    return mat_rows, mat_total, op_rows, op_total, sub, cont, sub + cont


def sales_margin(first_stock, skus=SKUS, sku19=SKU_19L):
    """First-stock profit margin across the three price tiers.

    Returns (rows, totals) where rows are
    [product, qty, unit cost, factory, dist, retail, total cost,
     factory revenue, our margin, margin %, distributor value, retail value].
    """
    rows = []
    for name, qty in first_stock:
        sk = _sku(name, skus, sku19)
        cost = sum(sk["costs"].values())
        fac, dist, ret = (sk["ex_factory_price"], sk["distributor_price"],
                          sk["retail_price"])
        rows.append([name, qty, cost, fac, dist, ret,
                     qty * cost, qty * fac, qty * (fac - cost),
                     (fac - cost) / fac * 100, qty * dist, qty * ret])
    t = [sum(r[i] for r in rows) for i in (1, 6, 7, 8, 10, 11)]
    t.append(t[3] / t[2] * 100 if t[2] else 0)      # blended margin %
    return rows, t


PROCESS_STEPS = [
    # (step, documents, duration, stage, gate)
    ("1. ආයෝජක ගිවිසුම / Investor agreement (MOU)",
     "MOU, Shareholders Agreement, Board Resolution, NDA", "සති 2", "0", False),
    ("2. සමාගම් ලියාපදිංචිය / Company incorporation (eROC)",
     "Name reservation, Form 1, AoA, Form 18, Form 19, BR certificate",
     "සති 2–3", "1", False),
    ("3. TIN + බැංකු ගිණුම / TIN + bank account",
     "TIN certificate, BR copy, Board Resolution, KYC", "සතිය 1", "1", False),
    ("4. ඉඩම් title + zoning තහවුරු කිරීම / Land title + zoning",
     "Title report, survey plan, UDA/PS written zoning confirmation",
     "සති 2–4", "1", False),
    ("5. WRB ලියාපදිංචිය / Water Resources Board registration",
     "WRB application, site plan, land documents", "සති 2–3", "1", False),
    ("6. ළිඳ කැණීම / Borewell drilling",
     "Hydrogeological survey report, WRB-registered driller permit",
     "සති 2–3", "1", False),
    ("7. 🔴 ජල පරීක්ෂණ / Water testing (SLS 614:2013)",
     "Accredited lab report — SLS 614, bromide, heavy metals, dry+wet season",
     "සති 2", "1", True),
    ("8. ගොඩනැඟිලි අනුමැතිය / Building permit",
     "Architect + structural drawings, UDA Form B / PS approval, CoC later",
     "සති 4–8", "1", False),
    ("9. ඉදිකිරීම් / Construction",
     "Building plan approval, contractor agreement, progress certificates",
     "මාස 4–5", "1", False),
    ("10. යන්ත්‍ර quotation + ඇණවුම / Machinery quotations + PO",
     "3 quotations, proforma invoice, LC/PO, import documents",
     "සති 2 (lead time මාස 4–8)", "2", False),
    ("11. CEB 3-phase සම්බන්ධතාව / CEB connection",
     "CEB application, wiring diagram, test certificate", "සති 4–6", "1", False),
    ("12. ETP + ගිනි ආරක්ෂාව / ETP + fire systems",
     "ETP design, fire NOC, extinguisher certificates", "ඉදිකිරීම් සමඟ", "1", False),
    ("13. CoC + Trade Licence / Certificate of Conformity",
     "CoC (Form D), Annual/Trade Licence from local authority", "සති 2–3", "1", False),
    ("14. CEA EPL / Environmental Protection Licence",
     "EPL application, BR, land authorisation, abatement proposal", "සති 2–4", "1", False),
    ("15. යන්ත්‍ර සවි කිරීම + commissioning / Installation",
     "Installation certificates, commissioning report, calibration records",
     "සති 4–6", "2", False),
    ("16. සේවක බඳවා ගැනීම + පුහුණුව / Recruitment + training",
     "EPF Form D (දින 14ක් ඇතුළත), job descriptions, training records, "
     "medical certificates", "සති 4", "2", False),
    ("17. HACCP / GMP ලේඛන / Documentation",
     "HACCP plan, GMP manual, SOPs, CCP records, org chart, supervision schedules",
     "මාස 3 (සමාන්තරව)", "2", False),
    ("18. FCAU අයදුම්පත / FCAU application",
     "Location map, site plan, factory layout, source sketch, process flow chart, "
     "Trade Licence, 2 label specimens, org chart, training document",
     "සති 2", "2", False),
    ("19. SLSI Audit 1",
     "QMS documents, HACCP plan, lab records, SLSI recommendation letter",
     "සතිය 1 + වාර්තාව සති 2–3", "2", False),
    ("20. PHI / MOH / FDI පරීක්ෂණ / Inspections",
     "Inspection reports, corrective action records", "සති 1–2", "2", False),
    ("21. FCAU ස්ථාන පරීක්ෂණය / FCAU site inspection",
     "Site inspection report", "සතිය 1", "2", False),
    ("22. ⭐ තාවකාලික FCAU ලියාපදිංචිය / Temporary registration (1 yr)",
     "FCAU registration certificate", "නිකුත් වේ", "2", False),
    ("23. ලේබල් අනුමැතිය + මුද්‍රණය / Label approval + printing",
     "2 approved label specimens (Food Labelling & Advertising Regs 2005)",
     "සති 3–4", "2", False),
    ("24. 🎉 නිෂ්පාදනය ආරම්භයි / COMMERCIAL PRODUCTION",
     "Batch records, QC release certificates", "—", "2", False),
]

TREATMENT_STEPS = [
    ("🕳️ නළ ළිඳ", "deep tube well", ""),
    ("Raw tank", "ගබඩාව", ""),
    ("⭐ Sand filter", "MGSF · &lt;1 NTU", "key"),
    ("⭐ Carbon filter", "ACF · free Cl &lt;0.1", "key"),
    ("Softener", "කඨිනතාව", ""),
    ("Micron", "5 → 1 → 0.5 µm", ""),
    ("⭐⭐ RO", "recovery 65%", "star"),
    ("Re-mineralise", "TDS නැවත", ""),
    ("UV", "≥40 mJ/cm²", ""),
    ("⭐⭐ Ozone", "0.2–0.4 ppm", "star"),
    ("0.2 µm sterile", "අවසන් පෙරහන", ""),
    ("🍶 Filling", "cleanroom", ""),
]


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
        "doc_totals": {k: sum(r[4] for r in capex_rows() if r[8] == k)
                       for k in ("registration", "equipment", "transport",
                                 "misc", "hr", "raw_material")},
        "process_steps": PROCESS_STEPS,
        "process_rows": [[i, st[0], st[1], st[2],
                           f'අදියර {st[3]}' + (' 🔴' if st[4] else '')]
                          for i, st in enumerate(PROCESS_STEPS, 1)],
        "treatment_steps": TREATMENT_STEPS,
        "office_equipment": OFFICE_EQUIPMENT,
        "office_total": sum(q * r for _, q, _, r in OFFICE_EQUIPMENT),
        "first_stock": FIRST_STOCK,
        "fs_bottles": sum(q for _, q in FIRST_STOCK),
        "fs_summary_rows": first_stock_full(FIRST_STOCK)[0],
        "fs_full_cost": first_stock_full(FIRST_STOCK)[1],
        "fs_retail_value": first_stock_full(FIRST_STOCK)[2],
        "fs_detail": first_stock_full(FIRST_STOCK)[3],
        "fs_material_cost": first_stock_cost(FIRST_STOCK)[1],
        "fp_material_rows": first_production(FIRST_STOCK, 0)[0],
        "fp_material": first_production(FIRST_STOCK, 0)[1],
        "fp_operating_rows": first_production(FIRST_STOCK, 0)[2],
        "fp_operating": first_production(FIRST_STOCK, 0)[3],
        "fp_subtotal": first_production(FIRST_STOCK, hr_monthly()[3])[4],
        "fp_contingency": first_production(FIRST_STOCK, hr_monthly()[3])[5],
        "fp_total": first_production(FIRST_STOCK, hr_monthly()[3])[6],
        "fs_margin": first_stock_full(FIRST_STOCK)[2] - first_stock_full(FIRST_STOCK)[1],
        "sales_rows": sales_margin(FIRST_STOCK)[0],
        "sales_totals": sales_margin(FIRST_STOCK)[1],
        "budget_docs": BUDGET_DOCS,
        "hr_plan": HR_PLAN,
        "departments": DEPARTMENTS,
        "level_names": LEVEL_NAMES,
        "top_role": TOP_ROLE,
        "hr_one_off": HR_ONE_OFF,
        "hr_headcount": hr_monthly()[0],
        "hr_gross": hr_monthly()[1],
        "hr_employer": hr_monthly()[2],
        "hr_month_total": hr_monthly()[3],
        "hr_year_total": hr_monthly()[3] * 12,
        "hr_one_off_total": hr_one_off_total(),
        "rawmat_rows": raw_material_rows(NAMEPLATE_MONTH, SKUS, SKU_19L),
        "rawmat_month": sum(r[4] for r in raw_material_rows(NAMEPLATE_MONTH, SKUS, SKU_19L)),
        "epf_er_pct": EPF_ER_PCT,
        "etf_pct": ETF_PCT,
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
