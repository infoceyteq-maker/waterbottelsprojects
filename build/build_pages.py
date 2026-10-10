#!/usr/bin/env python3
"""Emit the seven pages + the landing page. Run: python3 build/build_pages.py"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages_common import (OUT, PAGES, PAGE_CATEGORY, esc, kpi, m, shell, table)   # noqa: E402
from dashboard_model import build_model                       # noqa: E402


# =====================================================================
# PAGE 1 - SETUP BUDGET
# =====================================================================
def page1(M):
    s = []
    s.append('<h2 class="pg-title">💰 ආරම්භයේ සිට වැඩ පටන් ගන්න '
             'දවස වෙනකම් — සම්පූර්ණ අයවැය</h2>'
             '<p class="lead">ෆැක්ටරි එක ලියාපදිංචි කර, ගොඩනැඟිල්ල ඉදිකර, '
             'යන්ත්‍ර සවිකර, වැඩ පටන් ගන්න සූදානම් වන තෙක් · '
             '<b>Everything from day one until the plant is ready to run, '
             'office equipment included</b></p>')

    s.append('<div class="grid g4">')
    s.append(kpi("ලියාපදිංචි / Registration", "Rs " + m(M["doc_totals"]["registration"]),
                 "සමාගම්, WRB, FCAU, SLSI, CEA", "ol"))
    s.append(kpi("උපකරණ + ඉදිකිරීම් / Equipment", "Rs " + m(M["doc_totals"]["equipment"]),
                 "ගොඩනැඟිල්ල, plant, utilities", "am"))
    s.append(kpi("කාර්යාල උපකරණ / Office", "Rs " + m(M["office_total"]),
                 "furniture, computers, CCTV, software", "bl"))
    s.append(kpi("ප්‍රවාහන / Transport", "Rs " + m(M["doc_totals"]["transport"]),
                 "වාහන + ගබඩා උපකරණ"))
    s.append('</div>')

    # ---- registration ----
    rows = [[r[0], f'{r[1]:,}', r[2], f'{r[3]:,.0f}', f'{r[4]:,}', f'අදියර {r[7]}']
            for r in M["capex"] if r[8] == "registration"]
    s.append('<h3>📄 1. ලියාපදිංචි අයවැය / Registration Budget</h3>')
    s.append(table(["අයිතමය / Item", "Qty", "ඒකකය", "ඒකක මිල (Rs)", "මුදල (Rs)", "අදියර"],
                   rows, [f'{M["doc_totals"]["registration"]:,}', "", "", "", ""]))

    # ---- equipment ----
    rows = [[r[0], f'{r[1]:,}', r[2], f'{r[3]:,.0f}', f'{r[4]:,}', f'අදියර {r[7]}']
            for r in M["capex"] if r[8] == "equipment"]
    s.append('<h3>⚙️ 2. උපකරණ + ඉදිකිරීම් අයවැය / Equipment Budget</h3>')
    s.append(table(["අයිතමය / Item", "Qty", "ඒකකය", "ඒකක මිල (Rs)", "මුදල (Rs)", "අදියර"],
                   rows, [f'{M["doc_totals"]["equipment"]:,}', "", "", "", ""]))

    # ---- office equipment (new) ----
    rows = [[n, f'{q:,}', u, f'{r:,}', f'{q*r:,}'] for n, q, u, r in M["office_equipment"]]
    s.append('<h3>🖥️ 3. කාර්යාල උපකරණ අයවැය / Office Equipment Budget</h3>')
    s.append(table(["අයිතමය / Item", "Qty", "ඒකකය", "ඒකක මිල (Rs)", "මුදල (Rs)"],
                   rows, [f'{M["office_total"]:,}', "", "", ""]))

    # ---- transport ----
    rows = [[r[0], f'{r[1]:,}', r[2], f'{r[3]:,.0f}', f'{r[4]:,}']
            for r in M["capex"] if r[8] == "transport"]
    s.append('<h3>🚚 4. ප්‍රවාහන අයවැය / Transportation Budget</h3>')
    s.append(table(["අයිතමය / Item", "Qty", "ඒකකය", "ඒකක මිල (Rs)", "මුදල (Rs)"],
                   rows, [f'{M["doc_totals"]["transport"]:,}', "", "", ""]))

    # ---- miscellaneous ----
    rows = [[r[0], f'{r[1]:,}', r[2], f'{r[3]:,.0f}', f'{r[4]:,}']
            for r in M["capex"] if r[8] == "misc"]
    s.append('<h3>📦 5. විවිධ අයවැය / Miscellaneous Budget</h3>')
    s.append(table(["අයිතමය / Item", "Qty", "ඒකකය", "ඒකක මිල (Rs)", "මුදල (Rs)"],
                   rows, [f'{M["doc_totals"]["misc"]:,}', "", "", ""]))

    # ---- HR one-off ----
    rows = [[n, f'{q:,}', f'{r:,}', f'{q*r:,}'] for n, q, r in M["hr_one_off"]]
    s.append('<h3>👷 6. බඳවා ගැනීම + පුහුණුව (එක වර) / Recruitment & training</h3>')
    s.append(table(["අයිතමය / Item", "Qty", "ඒකක මිල (Rs)", "මුදල (Rs)"],
                   rows, [f'{M["hr_one_off_total"]:,}', "", ""]))

    # ---- the ladder ----
    A = M["doc_totals"]["registration"]
    B = M["doc_totals"]["equipment"]
    C = M["office_total"]
    D = M["doc_totals"]["transport"]
    E = M["doc_totals"]["misc"]
    F = M["hr_one_off_total"]
    sub = A + B + C + D + E + F
    cont = round(sub * 0.15)
    s.append('<h3>🧾 සම්පූර්ණ එකතුව / The full setup total</h3>')
    s.append(table(["", "මුදල (Rs)"], [
        ["A. ලියාපදිංචි / Registration", f'{A:,}'],
        ["B. උපකරණ + ඉදිකිරීම් / Equipment", f'{B:,}'],
        ["C. කාර්යාල උපකරණ / Office equipment", f'{C:,}'],
        ["D. ප්‍රවාහන / Transportation", f'{D:,}'],
        ["E. විවිධ / Miscellaneous", f'{E:,}'],
        ["F. බඳවා ගැනීම + පුහුණුව / Recruitment & training", f'{F:,}'],
    ], [f'{sub:,}'], "උප මුළු / SUBTOTAL"))
    s.append(table(["", "මුදල (Rs)"], [
        ["G. උප මුළු (A–F)", f'{sub:,}'],
        ["H. Contingency @ 15% — මිල ඉහළ යාමට ආරක්ෂාව", f'{cont:,}'],
    ], [f'{sub+cont:,}'], "මුළු CAPEX / TOTAL SETUP"))
    s.append(f'<div class="note ol"><b>🏞️ ඉඩම:</b> ඉඩම් වටිනාකම '
             f'<b>Rs {M["land_value"]:,}</b> Mr. Thilakarathna ගේ '
             '<b>in-kind දායකත්වයයි</b> — එය ඉහළ B අංශයේ ඇතුළත්ය, '
             'නමුත් මුදලින් ගෙවිය යුතු නැත.</div>')
    s.append(f'<div class="note"><b>💵 මුදලින් ගෙවිය යුතු මුළු ප්‍රමාණය / '
             f'TOTAL CASH REQUIRED:</b> <b style="font-size:17px">'
             f'Rs {sub+cont-M["land_value"]:,}</b> '
             f'(ඉඩම් වටිනාකම අඩු කිරීමෙන් පසු)</div>')
    s.append('<div class="note rd"><b>⚠️ මතක තබාගන්න:</b> මෙය <b>නිෂ්පාදනය '
             'ආරම්භ කරන තෙක්</b> වන පිරිවැයයි. පළමු නිෂ්පාදන කාණ්ඩයේ පිරිවැය '
             '<b>පිටුව 2</b> හි ඇත. යන්ත්‍ර සඳහා <b>quotation 3ක්</b> ලබාගෙන '
             'තහවුරු කරගන්න.</div>')
    return "".join(s)


# =====================================================================
# PAGE 2 - FIRST PRODUCTION BUDGET
# =====================================================================
def page2(M):
    s = []
    stock = dict(M["first_stock"])
    total_bottles = sum(stock.values())

    s.append('<h2 class="pg-title">🏭 නිෂ්පාදනය පටන් ගත් දවසේ සිට '
             'පළමු order stock එක ඉවර වෙනකම්</h2>'
             '<p class="lead">බෝතල්, ලේබල්, බෝතල් පිරවීම, සේවක පඩි — සියල්ල · '
             '<b>Bottles, labels, bottling, employee wages — everything in the '
             'first production run</b></p>')

    s.append('<div class="grid g4">')
    s.append(kpi("පළමු stock එක", f'{total_bottles:,}', "බෝතල් — නිෂ්පාදන 5ම", "ol"))
    s.append(kpi("අමුද්‍රව්‍ය / Raw material", "Rs " + m(M["fp_material"]),
                 "බෝතල්, මූඩි, ලේබල්, film", "am"))
    s.append(kpi("සේවක පඩි (මාස 1)", "Rs " + m(M["hr_month_total"]),
                 f'{M["hr_headcount"]} දෙනා · EPF/ETF සහිතව', "bl"))
    s.append(kpi("මුළු පළමු නිෂ්පාදන අයවැය", "Rs " + m(M["fp_total"]),
                 "සියල්ල එකතු කර", ""))
    s.append('</div>')

    # ---- raw materials for the first stock ----
    s.append('<h3>🧴 1. අමුද්‍රව්‍ය — පළමු stock එක සඳහා '
             '<span class="en">raw material for the first stock</span></h3>')
    s.append(table(["නිෂ්පාදනය", "බෝතල් Qty", "× 1.03", "මූඩි", "ලේබල් × 1.04",
                    "film × 1.05", "මුදල (Rs)"], M["fp_material_rows"],
                   [f'{total_bottles:,}', "", "", "", "", f'{M["fp_material"]:,.0f}']))
    s.append('<div class="note ol"><b>📌 Wastage:</b> බෝතල් × 1.03 · මූඩි × 1.03 · '
             'ලේබල් × 1.04 · shrink film × 1.05. පළමු නිෂ්පාදන කාණ්ඩයේ '
             'වැරදි වැඩි බැවින් මෙම අතිරික්තය අත්‍යවශ්‍යයි.</div>')

    # ---- operating costs for the run ----
    s.append('<h3>⚡ 2. නිෂ්පාදන ක්‍රියාත්මක කිරීමේ පිරිවැය '
             '<span class="en">operating cost of the run</span></h3>')
    s.append(table(["අයිතමය / Item", "පදනම / Basis", "මුදල (Rs)"],
                   M["fp_operating_rows"], [f'{M["fp_operating"]:,.0f}']))

    # ---- HR ----
    s.append('<h3>👷 3. සේවක පඩි — මාස 1ක් '
             '<span class="en">employee wages, one month</span></h3>')
    s.append(table(["තනතුර / Role", "සේවකයන්", "එකෙකුගේ වැටුප (Rs)", "මාසික (Rs)"],
                   [[r, f'{n}', f'{sal:,}', f'{n*sal:,}'] for r, n, sal in M["hr_plan"]],
                   [f'{M["hr_headcount"]}', "", f'{M["hr_gross"]:,.0f}'],
                   "දළ වැටුප් / Gross"))
    s.append(table(["", "මුදල (Rs)"], [
        ["දළ වැටුප් / Gross salaries", f'{M["hr_gross"]:,.0f}'],
        [f'EPF සේවාදායක {M["epf_er_pct"]*100:.0f}% + ETF {M["etf_pct"]*100:.0f}%',
         f'{M["hr_employer"]:,.0f}'],
    ], [f'{M["hr_month_total"]:,.0f}'], "මාසික මුළු / MONTHLY TOTAL"))

    # ---- the ladder ----
    s.append('<h3>🧾 පළමු නිෂ්පාදන කාණ්ඩයේ සම්පූර්ණ අයවැය</h3>')
    s.append(table(["", "මුදල (Rs)"], [
        ["A. අමුද්‍රව්‍ය (බෝතල්, මූඩි, ලේබල්, film)", f'{M["fp_material"]:,.0f}'],
        ["B. නිෂ්පාදන ක්‍රියාත්මක කිරීම (විදුලිය, ජලය, රසායන, QC)",
         f'{M["fp_operating"]:,.0f}'],
        ["C. සේවක පඩි — මාස 1ක් (EPF/ETF සහිතව)", f'{M["hr_month_total"]:,.0f}'],
    ], [f'{M["fp_subtotal"]:,.0f}'], "උප මුළු / SUBTOTAL"))
    s.append(table(["", "මුදල (Rs)"], [
        ["D. උප මුළු (A–C)", f'{M["fp_subtotal"]:,.0f}'],
        ["E. Contingency @ 10%", f'{M["fp_contingency"]:,.0f}'],
    ], [f'{M["fp_total"]:,.0f}'], "💰 මුළු / TOTAL"))
    s.append(f'<div class="note"><b>📊 එක බෝතලයකට සාමාන්‍ය පිරිවැය '
             f'(මෙම කාණ්ඩයේ):</b> <b style="font-size:17px">'
             f'Rs {M["fp_total"]/total_bottles:,.2f}</b> '
             f'(බෝතල් {total_bottles:,} සඳහා Rs {M["fp_total"]:,.0f}). '
             'කුඩා කාණ්ඩයක් බැවින් ඒකක පිරිවැය ඉහළය — සේවක පඩි සහ '
             'ස්ථාවර වියදම් බෝතල් ටිකක් මත බෙදී යයි.</div>')
    s.append('<div class="note rd"><b>⚠️ වැදගත්:</b> පළමු නිෂ්පාදන කාණ්ඩය '
             '<b>වෙළඳපොළට නිකුත් කිරීමට පෙර</b> FCAU තාවකාලික ලියාපදිංචිය සහ '
             'ලේබල් අනුමැතිය ලැබී තිබිය යුතුය. එසේ නොමැතිනම් '
             '<b>අලෙවි කළ නොහැක.</b></div>')
    return "".join(s)


# =====================================================================
# PAGE 3 - FIRST STOCK COST
# =====================================================================
def page3(M):
    s = []
    s.append('<h2 class="pg-title">🧮 පළමු stock එකේ බෝතල් පිරිවැය</h2>'
             '<p class="lead">ඔබ දුන් ප්‍රමාණ අනුව, නිෂ්පාදනය බැගින් වෙන වෙනම · '
             '<b>Your exact quantities, costed product by product</b></p>')

    s.append('<div class="grid g4">')
    s.append(kpi("මුළු බෝතල්", f'{M["fs_bottles"]:,}', "නිෂ්පාදන 5ම", "ol"))
    s.append(kpi("අමුද්‍රව්‍ය පිරිවැය", "Rs " + f'{M["fs_material_cost"]:,.0f}',
                 "බෝතල් + මූඩි + ලේබල් + film", "am"))
    s.append(kpi("සම්පූර්ණ නිෂ්පාදන පිරිවැය", "Rs " + f'{M["fs_full_cost"]:,.0f}',
                 "සියලු පිරිවැය ඇතුළුව", "bl"))
    s.append(kpi("අලෙවි වටිනාකම", "Rs " + f'{M["fs_retail_value"]:,.0f}',
                 "ex-factory මිලට"))
    s.append('</div>')

    s.append('<h3>📋 නිෂ්පාදනය අනුව සාරාංශය</h3>')
    s.append(table(["නිෂ්පාදනය", "Qty", "එකක පිරිවැය (Rs)", "මුළු පිරිවැය (Rs)",
                    "Ex-factory (Rs)", "අගය (Rs)", "ලාභය (Rs)"],
                   M["fs_summary_rows"],
                   [f'{M["fs_bottles"]:,}', "", f'{M["fs_full_cost"]:,.0f}', "",
                    f'{M["fs_retail_value"]:,.0f}', f'{M["fs_margin"]:,.0f}']))

    # per-product detail
    for row in M["fs_detail"]:
        s.append(f'<h3>{row["label"]}</h3>')
        s.append(table(["පිරිවැය අයිතමය", "එකකට (Rs)", f'Qty {row["qty"]:,} (Rs)'],
                       row["lines"], [f'{row["unit"]:.2f}', f'{row["total"]:,.0f}'],
                       f'මුළු / TOTAL ({row["sku"]})'))

    s.append('<div class="note ol"><b>📌 මෙහි ඇත්තේ variable cost පමණි</b> — '
             'එනම් බෝතලය සමඟ කෙලින්ම වෙනස් වන පිරිවැය (බෝතල්, මූඩි, ලේබල්, '
             'ජලය, විදුලිය, ශ්‍රමය, නඩත්තු). සේවක පඩි සහ ස්ථාවර වියදම් '
             '<b>පිටුව 2</b> හි වෙනම දක්වා ඇත.</div>')
    return "".join(s)


# =====================================================================
# PAGE 4 - PROCESS, DOCUMENTS, TIMELINE
# =====================================================================
def page4(M):
    s = []
    s.append('<h2 class="pg-title">🔄 ක්‍රියාවලිය — පියවරෙන් පියවර</h2>'
             '<p class="lead">සෑම පියවරකටම අවශ්‍ය ලේඛන සහ ගතවන කාලය · '
             '<b>Each step, the documents it needs, and how long it takes</b></p>')

    crit = sum(1 for st in M["process_steps"] if st[4])
    s.append('<div class="grid g4">')
    s.append(kpi("පියවර ගණන", f'{len(M["process_steps"])}', "ආරම්භයේ සිට නිෂ්පාදනය දක්වා", "ol"))
    s.append(kpi("මුළු කාලය", "මාස 14–20", "critical path එක අනුව", "am"))
    s.append(kpi("🔴 අනිවාර්ය GATE", f'{crit}', "මෙය අසමත් වුවහොත් ව්‍යාපෘතිය නවතී", "bl"))
    s.append(kpi("මුළු ලේඛන", "160", "checklist එකේ සම්පූර්ණ ලැයිස්තුව", ""))
    s.append('</div>')

    s.append('<h3>📋 සම්පූර්ණ පියවර ලැයිස්තුව</h3>')
    s.append(table(["#", "පියවර / Step", "අවශ්‍ය ලේඛන / Documents needed",
                    "කාලය / Duration", "අදියර"],
                   M["process_rows"]))
    s.append('<div class="note rd"><b>🔴 GATE — පියවර 7:</b> ළිඳ කණින්න '
             '<b>ගොඩනැඟිල්ල ඉදිකිරීමට පෙර.</b> ජලය SLS 614:2013 සමත් නොවුණොත් '
             'FCAU ලියාපදිංචිය <b>ප්‍රතික්ෂේප වේ</b> — එවිට කර්මාන්ත ශාලාවක් '
             'තිබී ප්‍රයෝජනයක් නැත. මෙය ව්‍යාපෘතියේ විශාලතම තනි අවදානමයි.</div>')
    s.append('<div class="note am"><b>⚠️ යන්ත්‍ර lead time:</b> විදේශ සැපයුම්කරුවන්ගෙන් '
             '<b>මාස 4–8</b>. ඇණවුම <b>පියවර 10</b> හිදී (මාස 5–6) කළ යුතුය — '
             'නොඑසේ නම් ගොඩනැඟිල්ල ඉවර වී යන්ත්‍ර නැතිව හිස්ව පවතී.</div>')

    s.append('<h3>💧 ජල පිරිපහදු ක්‍රියාවලිය '
             '<span class="en">the treatment train, in order</span></h3>')
    s.append('<div class="flow">')
    for i, st in enumerate(M["treatment_steps"]):
        if i:
            s.append('<span class="ar">→</span>')
        s.append(f'<div class="st {st[2]}">{st[0]}<br>'
                 f'<span style="font-size:10.5px;font-weight:500">{st[1]}</span></div>')
    s.append('</div>')
    s.append('<div class="note"><b>🔬 CCP 7ක්:</b> MGSF &lt;1 NTU · ACF free Cl '
             '&lt;0.1 ppm · RO conductivity/TDS · UV ≥40 mJ/cm² · '
             'ozone 0.2–0.4 ppm at filler · 0.2µm ΔP/integrity · '
             'filling cleanroom ΔP. වාර්තා <b>වසර 2ක්</b> තබාගන්න.</div>')
    return "".join(s)



# =====================================================================
# PAGE 5 - ORGANISATION CHART
# =====================================================================
def page5(M):
    s = []
    s.append('<h2 class="pg-title">🏛️ කර්මාන්ඩල සටහන — '
             'දෙපාර්තමේන්තු අනුව</h2>'
             '<p class="lead">රැකියා ධූරාවලිය, සෑම දෙපාර්තමේන්තුවකම වැටුප් සහ EPF/ETF · '
             '<b>The employment hierarchy, department by department, with salary '
             'and EPF</b></p>')

    s.append('<div class="grid g4">')
    s.append(kpi("මුළු සේවකයන්", f'{M["hr_headcount"]}',
                 "දෙපාර්තමේන්තු 4ක් + Plant Manager", "ol"))
    s.append(kpi("දළ වැටුප් / Gross", "Rs " + f'{M["hr_gross"]:,.0f}',
                 "මාසික · EPF/ETF ට පෙර", "am"))
    s.append(kpi("EPF 12% + ETF 3%", "Rs " + f'{M["hr_employer"]:,.0f}',
                 "සේවාදායක බර / employer burden", "bl"))
    s.append(kpi("මාසික මුළු / Monthly", "Rs " + f'{M["hr_month_total"]:,.0f}',
                 f'වාර්ෂික Rs {M["hr_year_total"]:,.0f}', ""))
    s.append('</div>')

    # ---- the chart itself ----
    s.append('<div class="org">')
    s.append('<div class="org-box org-board"><div class="t">🏛️ Board of Directors / '
             f'අධ්‍යක්ෂ මණ්ඩලය</div>'
             f'<div class="s">Investor / ආයෝජක: {M["investor"]}</div></div>')
    s.append('<div class="org-line"></div>')
    s.append(f'<div class="org-box org-mgr"><div class="t">👔 {M["top_role"][0]}</div>'
             f'<div class="s">{M["top_role"][1]} දෙනා · '
             f'Rs {M["top_role"][2]:,}/මාස · Level 1</div></div>')
    s.append('<div class="org-line"></div>')
    s.append('<div class="org-hline"></div>')
    s.append('<div class="org-depts">')
    for d in M["departments"]:
        hc = sum(r[1] for r in d["roles"])
        gross = sum(r[1] * r[3] for r in d["roles"])
        s.append(f'<div class="org-dept"><div class="hd">'
                 f'<div class="ic">{d["icon"]}</div>'
                 f'<div class="t">{d["si"]}</div>'
                 f'<div class="e">{html.escape(d["en"])}</div></div><div class="bd">')
        for name, n, lvl, sal in d["roles"]:
            lvcls = "l2" if lvl == 2 else ""
            s.append(f'<div class="org-role"><div class="rn">'
                     f'<span class="lv {lvcls}">L{lvl}</span>{name}</div>'
                     f'<div class="rv"><b>{n} × Rs {sal:,}</b>'
                     f'<span>= Rs {n*sal:,}</span></div></div>')
        s.append(f'</div><div class="ft"><span>{hc} දෙනා</span>'
                 f'<span>Rs {gross:,}/මාස</span></div></div>')
    s.append('</div></div>')

    # ---- payroll with EPF/ETF ----
    s.append('<h3>💵 සම්පූර්ණ වැටුප් ලැයිස්තුව — EPF/ETF සහිතව '
             '<span class="en">full payroll with EPF and ETF</span></h3>')
    rows = [[f'👔 {M["top_role"][0]}', "—", "1", "L1",
             f'{M["top_role"][2]:,}', f'{M["top_role"][2]:,}']]
    for d in M["departments"]:
        for name, n, lvl, sal in d["roles"]:
            rows.append([f'{d["icon"]} {name}', html.escape(d["en"]), f'{n}', f'L{lvl}',
                         f'{sal:,}', f'{n*sal:,}'])
    s.append(table(["තනතුර / Role", "දෙපාර්තමේන්තුව", "සේවකයන්", "මට්ටම",
                    "එකෙකුගේ වැටුප (Rs)", "මාසික මුළු (Rs)"],
                   rows, [f'{M["hr_headcount"]}', "", "", f'{M["hr_gross"]:,.0f}'],
                   "දළ වැටුප් / GROSS"))

    epf = round(M["hr_gross"] * M["epf_er_pct"])
    etf = round(M["hr_gross"] * M["etf_pct"])
    s.append('<h3>📋 EPF / ETF ගණනය කිරීම '
             '<span class="en">statutory calculation</span></h3>')
    s.append(table(["", "අනුපාතය", "මාසික (Rs)", "වාර්ෂික (Rs)"], [
        ["දළ වැටුප් / Gross salaries", "—", f'{M["hr_gross"]:,.0f}',
         f'{M["hr_gross"]*12:,.0f}'],
        ["EPF — සේවාදායක කොටස / employer",
         f'{M["epf_er_pct"]*100:.0f}%', f'{epf:,}', f'{epf*12:,}'],
        ["ETF — සේවාදායක කොටස / employer",
         f'{M["etf_pct"]*100:.0f}%', f'{etf:,}', f'{etf*12:,}'],
    ], [f'{M["hr_month_total"]:,.0f}', f'{M["hr_year_total"]:,.0f}'],
        "💰 මුළු සේවක පිරිවැය / TOTAL"))
    s.append('<div class="note rd"><b>⚠️ නීතිමය අවශ්‍යතා:</b> '
             'පළමු සේවකයා බඳවා ගත් දින <b>14ක් ඇතුළත</b> EPF Form D ඉදිරිපත් '
             'කළ යුතුය. සේවාදායකයා <b>EPF 12% + ETF 3% = 15%</b> ගෙවයි; '
             'සේවකයාගේ වැටුපෙන් <b>EPF 8%</b> අඩු කෙරේ. වැටුප් ගෙවීම '
             '<b>ඊළඟ මාසයේ අවසන් වැඩ කරන දිනයට</b> පෙර කළ යුතුය.</div>')
    s.append('<div class="note ol"><b>📌 දෙපාර්තමේන්තු 4:</b> '
             '🏭 නිෂ්පාදන සහ තත්ත්ව පාලනය (25) · '
             '💼 මානව සම්පත් සහ මුදල් (7) · '
             '📈 අලෙවි සහ නාමකරණ (2) · '
             '🚚 ප්‍රවාහන (8) · '
             '+ 👔 Plant Manager (1) = <b>43 දෙනා</b></div>')
    s.append('<div class="note"><b>💡 Phase 2 හිදී:</b> දෙවන shift එක ආරම්භ '
             'කරන විට නිෂ්පාදන සේවකයන් දළ වශයෙන් <b>දෙගුණ</b> කළ යුතුය '
             '(Machine Operator, Filling Line Worker, Water Treatment Operator). '
             'කළමනාකාරීය සහ QC තනතුරු එලෙසම පවතී.</div>')
    return "".join(s)



# =====================================================================
# PAGE 6 - SALES & MARKETING  (price ladder + first-stock profit margin)
# =====================================================================
def page6(M):
    t = M["sales_totals"]
    qty, cost, rev, mg, dist, ret, mpc = t
    s = []
    s.append('<h2 class="pg-title">📈 අලෙවි සහ නාමකරණ — '
             'මිල සහ ලාභය</h2>'
             '<p class="lead">Factory → Distributor → Retail මිල පඩිපෙළ සහ පළමු '
             'stock එකේ ලාභය · <b>The three-tier price ladder and the profit on '
             'the first stock</b></p>')

    s.append('<div class="grid g4">')
    s.append(kpi("පළමු stock එකේ ආදායම", "Rs " + f'{rev:,.0f}',
                 f'බෝතල් {qty:,} · Factory මිලට', "ol"))
    s.append(kpi("💰 අපේ ලාභය / Our margin", "Rs " + f'{mg:,.0f}',
                 f'Factory මිල − නිෂ්පාදන පිරිවැය', "am"))
    s.append(kpi("ලාභ ප්‍රතිශතය / Margin", f'{mpc:.1f}<em>%</em>',
                 "ආදායමෙන් ප්‍රතිශතයක් ලෙස", "bl"))
    s.append(kpi("සිල්ලට වටිනාකම / Retail value", "Rs " + f'{ret:,.0f}',
                 "පාරිභෝගිකයා ගෙවන මුළු මුදල", ""))
    s.append('</div>')

    # ---- 1. the price ladder ----
    s.append('<h3>💵 මිල පඩිපෙළ <span class="en">the price ladder</span></h3>')
    s.append(table(["නිෂ්පාදනය / Product", "Factory<br>(අපේ මිල)",
                    "Distributor<br>(බෙදාහරින්නා)", "Retail<br>(සිල්ල)",
                    "බෙදාහරින්නාගේ ලාභය", "සිල්ලර වෙළඳාගේ ලාභය"],
                   [[x[0], f'Rs {x[3]:,.0f}', f'Rs {x[4]:,.0f}', f'Rs {x[5]:,.0f}',
                     f'Rs {x[4]-x[3]:,.0f} ({(x[4]-x[3])/x[3]*100:.0f}%)',
                     f'Rs {x[5]-x[4]:,.0f} ({(x[5]-x[4])/x[4]*100:.0f}%)']
                    for x in M["sales_rows"]]))
    s.append('<div class="note ol"><b>📌 අපට ලාභය ලැබෙන්නේ '
             '<b>Factory මිල</b> එකෙනි.</b> Distributor සහ Retail මිල '
             'බෙදාහරින්නාගේ සහ සිල්ලර වෙළඳාගේ ලාභයයි — ඒවා අපේ ආදායම නොවේ.</div>')

    # ---- 2. margin per product ----
    s.append('<h3>🧮 නිෂ්පාදනය අනුව ලාභය '
             '<span class="en">margin per product</span></h3>')
    s.append(table(["නිෂ්පාදනය", "නිෂ්පාදන පිරිවැය", "Factory මිල",
                    "එකක ලාභය", "Margin %"],
                   [[x[0], f'Rs {x[2]:,.2f}', f'Rs {x[3]:,.0f}',
                     f'<b>Rs {x[3]-x[2]:,.2f}</b>', f'{x[9]:.1f}%']
                    for x in M["sales_rows"]],
                   [f'Rs {cost/qty:,.2f}', f'Rs {rev/qty:,.2f}',
                    f'<b>Rs {mg/qty:,.2f}</b>', f'{mpc:.1f}%'],
                   "සාමාන්‍ය / BLENDED"))

    # ---- 3. first stock profit ----
    s.append('<h3>📦 පළමු stock එකේ ලාභය '
             '<span class="en">profit on the first stock</span></h3>')
    s.append(table(["නිෂ්පාදනය", "Qty", "නිෂ්පාදන පිරිවැය (Rs)",
                    "Factory ආදායම (Rs)", "💰 අපේ ලාභය (Rs)", "Margin %"],
                   [[x[0], f'{x[1]:,}', f'{x[6]:,.0f}', f'{x[7]:,.0f}',
                     f'<b>{x[8]:,.0f}</b>', f'{x[9]:.1f}%'] for x in M["sales_rows"]],
                   [f'{qty:,}', f'{cost:,.0f}', f'{rev:,.0f}', f'<b>{mg:,.0f}</b>',
                    f'{mpc:.1f}%']))
    s.append(f'<div class="note"><b>💰 පළමු stock එකේ සාරාංශය:</b> '
             f'නිෂ්පාදන පිරිවැය <b>Rs {cost:,.0f}</b> · '
             f'Factory ආදායම <b>Rs {rev:,.0f}</b> · '
             f'<b>අපේ ලාභය Rs {mg:,.0f} ({mpc:.1f}%)</b></div>')

    # ---- 4. who earns what along the chain ----
    s.append('<h3>🔗 නාලිකාව දිගේ ලාභය බෙදී යන ආකාරය '
             '<span class="en">who earns what</span></h3>')
    s.append(table(["", "මුදල (Rs)", "%"], [
        ["🏭 අපේ නිෂ්පාදන පිරිවැය / Our production cost", f'{cost:,.0f}',
         f'{cost/ret*100:.1f}%'],
        ["🏭 <b>අපේ ලාභය / OUR MARGIN</b> (Factory − පිරිවැය)", f'{mg:,.0f}',
         f'{mg/ret*100:.1f}%'],
        ["🚚 බෙදාහරින්නාගේ ලාභය / Distributor margin", f'{dist-rev:,.0f}',
         f'{(dist-rev)/ret*100:.1f}%'],
        ["🏪 සිල්ලර වෙළඳාගේ ලාභය / Retailer margin", f'{ret-dist:,.0f}',
         f'{(ret-dist)/ret*100:.1f}%'],
    ], [f'{ret:,.0f}', "100%"], "🛒 සිල්ල වටිනාකම / RETAIL VALUE"))
    s.append('<div class="note rd"><b>⚠️ 500 ml ගැන සැලකිලිමත් වන්න:</b> '
             'Factory Rs 38 එකේ අපේ ලාභය <b>Rs 11.30 (29.7%)</b> පමණි — '
             'නිෂ්පාදන පිරිවැය Rs 26.70 නිසා. මෙය අඩුම margin එකයි. '
             '<b>5 L සහ 19 L වල margin 58–62%</b> බැවින් ඒවාට '
             'ප්‍රමුඛතාව දෙන්න. Phase 2 හි blow moulding එකතු කළවිට '
             'බෝතල් පිරිවැය 30–40% අඩු වී 500 ml margin එක සැලකිය යුතු ලෙස '
             'ඉහළ යයි.</div>')
    s.append('<div class="note ol"><b>📌 මතක තබාගන්න:</b> මෙම ලාභය '
             '<b>variable cost පමණක්</b> අඩු කිරීමෙන් පසු ලැබෙන්නයි. '
             'සේවක පඩි, විදුලිය සහ ස්ථාවර වියදම් ආවරණය කිරීමට '
             f'මාසිකව බෝතල් <b>~{M["final"]["be_bottles_m"]:,.0f}</b>ක් — '
             f'දවසට <b>{M["final"]["be_day"]:,.0f}</b>ක් (ධාරිතාවෙන් '
             f'{M["final"]["be_pct"]*100:.0f}%) අවශ්‍යයි. '
             'සම්පූර්ණ ගණනය <a href="7-final-summary.html">අවසන් '
             'සාරාංශය</a> පිටුවේ.</div>')
    return "".join(s)



# =====================================================================
# PAGE 7 - FINAL SUMMARY  (whole budget, break-even per day, payback)
# =====================================================================
def page7(M):
    F = M["final"]
    oy = F["one_year"]
    dt = M["doc_totals"]
    s = []
    s.append('<h2 class="pg-title">🎯 අවසන් සාරාංශය '
             '— ආයෝජනය, ලාභය, ආපසු ලැබෙන කාලය</h2>'
             '<p class="lead">මුළු අයවැය එක තැනක · දවසට විකුණිය යුතු '
             'ප්‍රමාණය · ආයෝජනය ආපසු ලැබෙන මාස · <b>the whole budget in '
             'one place, what must sell each day, and when the money comes '
             'back</b></p>')

    pb100 = F["payback_rows"][-1]
    s.append('<div class="grid g4">')
    s.append(kpi("💼 මුළු ආයෝජනය / Total investment", m(F["investment"]),
                 f'Rs {F["investment"]:,.0f}', "am"))
    s.append(kpi("💵 මුදලින් අවශ්‍ය / Cash to raise", m(F["cash"]),
                 "ඉඩම් Rs 12M in-kind දායකත්වයක්", "bl"))
    s.append(kpi("🔴 දවසට විකුණිය යුතු අවම", f'{F["be_day"]:,.0f}<em> බෝතල්</em>',
                 f'ධාරිතාවෙන් {F["be_pct"]*100:.0f}% · ලාභය Rs 0 වන තැන', "rd"))
    s.append(kpi("⏳ ආයෝජනය ආපසු / Payback", f'{pb100["months"]:.1f}<em> මාස</em>',
                 "100% ධාරිතාවේදී (බදු පෙර)", "ol"))
    s.append('</div>')

    # ---------- 1. the whole budget ----------
    s.append('<h3>🧾 සම්පූර්ණ අයවැජ සාරාංශය '
             '<span class="en">the whole budget, one table</span></h3>')
    s.append(table(["කොටස / Component", "පිටුව", "මුදල (Rs)"], [
        ["A. ලියාපදිංචි / Registration", "1", f'{dt["registration"]:,}'],
        ["B. උපකරණ + ඉදිකිරීම් / Equipment & construction", "1",
         f'{dt["equipment"]:,}'],
        ["C. කාර්යාල උපකරණ / Office equipment", "1",
         f'{M["office_total"]:,}'],
        ["D. ප්‍රවාහන / Transportation", "1", f'{dt["transport"]:,}'],
        ["E. විවිධ / Miscellaneous", "1", f'{dt["misc"]:,}'],
        ["F. බඳවා ගැනීම + පුහුණුව / Recruitment & training", "1",
         f'{M["hr_one_off_total"]:,}'],
    ], [f'{F["setup_sub"]:,}'], "උප මුළු / SUBTOTAL (පිටුව 1)"))
    s.append(table(["", "මුදල (Rs)"], [
        ["උප මුළු (A–F)", f'{F["setup_sub"]:,}'],
        ["G. Contingency @ 15% — මිල ඉහළ යාමට ආරක්ෂාව",
         f'{F["setup_cont"]:,}'],
        ["<b>ආරම්භක CAPEX / Total setup</b> (පිටුව 1)",
         f'<b>{F["setup_total"]:,}</b>'],
        ["H. පළමු නිෂ්පාදන අයවැය / First production run (පිටුව 2)",
         f'{F["first_prod"]:,}'],
    ], [f'{F["investment"]:,}'], "💼 මුළු ආයෝජනය / TOTAL INVESTMENT"))
    s.append(table(["", "මුදල (Rs)"], [
        ["💼 මුළු ආයෝජනය", f'{F["investment"]:,}'],
        ["🏞️ අඩු කරන්න: ඉඩම — Mr. Thilakarathna ගේ "
         "<b>in-kind</b> දායකත්වය", f'({F["land"]:,})'],
    ], [f'{F["cash"]:,}'], "💵 මුදලින් අවශ්‍ය / CASH REQUIRED"))
    s.append(f'<div class="note ol"><b>🏦 බැංකුවේ තිබිය යුතු මුදල:</b> '
             f'Rs {F["cash"]:,.0f} + නිර්දේශිත working capital buffer '
             f'Rs {F["buffer"]:,.0f} = <b>Rs {F["cash_with_buffer"]:,.0f}</b>. '
             'Buffer එක නිෂ්පාදනය ආරම්භ වන තෙක් දෛනික වියදම් ගෙවීමටයි.</div>')

    # ---------- 2. the earnings rate, off the first stock ----------
    s.append('<h3>📦 පළමු stock එකේ ලාභය '
             '<span class="en">the earnings rate</span></h3>')
    s.append(table(["", "ප්‍රමාණය / මුදල"], [
        ["පළමු stock එකේ බෝතල්", f'{F["fs_bottles"]:,}'],
        ["නිෂ්පාදන පිරිවැය / Production cost (පිටුව 3)",
         f'Rs {F["fs_cost"]:,.0f}'],
        ["Factory ආදායම / Revenue (පිටුව 6)", f'Rs {F["fs_revenue"]:,.0f}'],
        ["<b>💰 අපේ ලාභය / Our margin</b>", f'<b>Rs {F["fs_margin"]:,.0f}</b>'],
        ["ලාභ ප්‍රතිශතය / Margin %",
         f'{M["sales_totals"][6]:.1f}%'],
    ], [f'Rs {F["per_bottle"]:.2f}'], "🔑 එක් බෝතලයක ලාභය / PROFIT PER BOTTLE"))

    # ---------- 3. break-even per day (marked) ----------
    s.append('<h3>🔴 දවසට විකුණිය යුතු ප්‍රමාණය '
             '<span class="en">what MUST sell every day</span></h3>')
    s.append(table(["", "අගය"], [
        ["මාසික ස්ථාවර වියදම් / Monthly fixed cost "
         "(පඩි + EPF + විදුලිය + නඩත්තුව + ප්‍රවාහන + අලෙවි)",
         f'Rs {F["fixed"]:,.0f}'],
        ["එක් බෝතලයක ලාභය / Profit per bottle", f'Rs {F["per_bottle"]:.2f}'],
        ["= මාසිකව අවශ්‍ය බෝතල් / Bottles per month",
         f'<b>{F["be_bottles_m"]:,.0f}</b>'],
        ["= දවසකට (වැඩ කරන දින 25) / Per working day",
         f'<b>{F["be_day"]:,.0f} බෝතල්</b>'],
        ["ධාරිතාවෙන් ප්‍රතිශතය / % of capacity",
         f'{F["be_pct"]*100:.0f}% (ධාරිතාව '
         f'{F["nameplate_day"]:,.0f} බෝතල්/දවස)'],
        ["දවසට අවශ්‍ය ආදායම / Revenue needed per day",
         f'Rs {F["be_revenue_day"]:,.0f}'],
    ]))
    s.append(f'<div class="note rd"><b>🔴 මතක තබාගන්න:</b> දවසට බෝතල් '
             f'<b>{F["be_day"]:,.0f}</b>ක් විකුණා නොමැති නම් ඒ දවසේ '
             '<b>පාඩු</b>යි. එය ධාරිතාවෙන් <b>'
             f'{F["be_pct"]*100:.0f}%</b>ක් පමණි — එනම් කර්මාන්ත ශාලාවේ '
             '71%ක් හිස්ව තිබුණත් පාඩු නැත. ඉතිරි 71% තුළ ලාභය '
             'උපයනු ලැබේ.</div>')

    # ---------- 4. payback at each utilisation ----------
    s.append('<h3>⏳ ආයෝජනය ආපසු ලැබෙන කාලය '
             '<span class="en">how long until the investment comes back</span>'
             '</h3>')
    rows = []
    for r in F["payback_rows"]:
        mo = f'<b>{r["months"]:.1f} මාස</b>' if r["months"] else \
             '<span class="bad">❌ කිසිවිටෙකත් නැත</span>'
        mt = f'{r["months_tax"]:.1f} මාස' if r["months_tax"] else "—"
        rows.append([f'{r["util"]*100:.0f}%', f'{r["bottles_m"]:,}',
                     f'{r["bottles_day"]:,}', f'Rs {r["profit_m"]:,.0f}',
                     mo, mt])
    s.append(table(["ධාරිතාව", "බෝතල් / මාස", "බෝතල් / දවස",
                    "මාසික ලාභය", "ආයෝජනය ආපසු<br>(බදු පෙර)",
                    "ආයෝජනය ආපසු<br>(බදු 30% පසු)"], rows))
    s.append(f'<div class="note"><b>📌 කියවන ආකාරය:</b> ධාරිතාවෙන් 50%කින් '
             f'(දවසට බෝතල් 24,000) ක්‍රියාත්මක වුවහොත් මුළු ආයෝජනය '
             f'<b>මාස 29.7කින්</b> ආපසු ලැබේ. 100%කින් '
             f'<b>මාස {pb100["months"]:.1f}කින්</b>. 25%කින් '
             '<b>පාඩු</b>යි — ආයෝජනය කිසිවිටෙකත් ආපසු නොලැබේ.</div>')

    # ---------- 5. the one-year target (marked) ----------
    s.append('<h3>🎯 අවුරුද්දක් තුළ මුළු ආයෝජනයම ආපසු ලබා ගැනීමට '
             '<span class="en">to get it all back in ONE year</span></h3>')
    s.append(table(["", "අගය"], [
        ["මුළු ආයෝජනය / Investment to recover", f'Rs {oy["profit_y"]:,.0f}'],
        ["= අවශ්‍ය මාසික ලාභය / Required profit per month",
         f'Rs {oy["profit_m"]:,.0f}'],
        ["🏭 <b>දවසට නිෂ්පාදනය කළ යුතු / MAKE per day</b>",
         f'<b>{oy["bottles_day"]:,.0f} බෝතල්</b>'],
        ["🛒 <b>දවසට විකුණිය යුතු / SELL per day</b>",
         f'<b>{oy["bottles_day"]:,.0f} බෝතල්</b>'],
        ["= මාසිකව / per month", f'{oy["bottles_m"]:,.0f} බෝතල්'],
        ["ධාරිතාවෙන් / % of capacity", f'<b>{oy["util"]*100:.0f}%</b>'],
    ]))
    s.append(f'<div class="note ol"><b>✅ හැකියි.</b> දවසට බෝතල් '
             f'<b>{oy["bottles_day"]:,.0f}</b>ක් යනු ධාරිතාවෙන් '
             f'{oy["util"]*100:.0f}%කි — එක shift එකක ධාරිතාව බෝතල් '
             f'{F["nameplate_day"]:,.0f}/දවස බැවින් <b>අමතර යන්ත්‍රෝපකරණ '
             'අවශ්‍ය නැත</b>.</div>')
    s.append(f'<div class="note rd"><b>⚠️ බදු 30% සලකා බැලූ විට:</b> '
             f'අවශ්‍ය වන්නේ දවසට බෝතල් <b>{oy["bottles_day_tax"]:,.0f}</b>ක් '
             f'= ධාරිතාවෙන් <b>{oy["util_tax"]*100:.0f}%</b>. එය එක '
             'shift එකකින් <b>නොහැක</b>. විසඳුම: <b>shift 2ක්</b>, නැතහොත් '
             f'බදු පසු ආයෝජනය ආපසු ලැබෙන්නේ <b>මාස 15.8කින්</b>.</div>')

    # ---------- 6. notes ----------
    s.append('<h3>📝 උපකල්පන <span class="en">assumptions</span></h3>')
    s.append('<ul class="bullets">'
             f'<li>ධාරිතාව: {M["capacity_bph"]:,} බෝතල්/පැය × '
             f'{M["shift_hours"]} පැය × {F["days"]} දින = '
             f'<b>{F["nameplate"]:,} බෝතල්/මාස</b></li>'
             '<li>ලාභ වේගය <b>පළමු stock එකේ මිශ්‍රණය</b> මත පදනම් වේ '
             '(500 ml 5,000 · 1 L 3,000 · 1.5 L 3,000 · 5 L 1,000 · '
             '19 L 150). මිශ්‍රණය වෙනස් වුවහොත් බෝතලයක ලාභය වෙනස් වේ.</li>'
             '<li>ලාභය <b>Factory මිල</b> මත පමණි (පිටුව 6 බලන්න).</li>'
             f'<li>ස්ථාවර වියදම් Rs {F["fixed"]:,.0f}/මාස — 43 දෙනාගේ '
             'පඩි + EPF/ETF + විදුලිය + නඩත්තුව + ප්‍රවාහන + අලෙවි + '
             'අපහරණය.</li>'
             '<li>බදු පෙර අගයන් ඉහළ වගුවේ ද, බදු 30% පසු අගයන් අවසන් '
             'තීරුවේ ද දක්වා ඇත.</li>'
             '<li>ඉඩම මුදලින් ගෙවීමක් නොවේ — in-kind දායකත්වයකි.</li>'
             '<li>මෙය එක් කර්මාන්ත ශාලාවක් / shift එකක් සඳහායි. වසර '
             'කිහිපයක P&amp;L අනාවැකි ඉල්ලීමක් නොමැති බැවින් '
             'ඇතුළත් කර නැත.</li>'
             '</ul>')
    return "".join(s)


def main():
    M = build_model()
    os.makedirs(OUT, exist_ok=True)

    builders = {"1": page1, "2": page2, "3": page3, "4": page4, "5": page5, "6": page6,
            "7": page7}
    subs = {
        "1": '<span class="si">ෆැක්ටරි එක ලියාපදිංචි කර, ගොඩනැඟිල්ල ඉදිකර, යන්ත්‍ර සවිකර, '
             'වැඩ පටන් ගන්න දවස වෙනකම් වන සම්පූර්ණ පිරිවැය — කාර්යාල උපකරණ ද ඇතුළුව.</span>'
             '<span class="en">All costs from company registration through construction, equipment installation and factory readiness, including office equipment.</span>',
        "2": '<span class="si">නිෂ්පාදනය පටන් ගත් දවසේ සිට පළමු order stock එක ඉවර වෙනකම් — '
             'බෝතල්, ලේබල්, පිරවීම, සේවක පඩි.</span>'
             '<span class="en">From production start until the first order stock is complete: bottles, labels, filling and staff wages.</span>',
        "3": '<span class="si">ඔබ දුන් ප්‍රමාණ අනුව පළමු stock එකේ බෝතල් පිරිවැය: '
             '500 ml 5,000 · 1 L 3,000 · 1.5 L 3,000 · 5 L 1,000 · 19 L 150.</span>'
             '<span class="en">First-stock unit costs, calculated separately using your exact quantities for all five products.</span>',
        "4": '<span class="si">ක්‍රියාවලිය පියවරෙන් පියවර, සෑම පියවරකටම අවශ්‍ය ලේඛන සහ '
             'ගතවන කාලය.</span>'
             '<span class="en">A step-by-step process, the documents required at each step and the estimated time.</span>',
        "5": '<span class="si">රැකියා ධූරාවලිය දෙපාර්තමේන්තු 4ක් අනුව — සෑම තනතුරකම වැටුප, '
             'EPF 12% සහ ETF 3% සහිතව.</span>'
             '<span class="en">The four-department job hierarchy, with salary and employer EPF/ETF costs.</span>',
        "6": '<span class="si">Factory → Distributor → Retail මිල පඩිපෙළ, නිෂ්පාදනය අනුව ලාභය, '
             'සහ පළමු stock එකේ ලාභ ප්‍රතිශතය.</span>'
             '<span class="en">Factory-to-distributor-to-retail pricing, product margins and first-stock profit.</span>',
        "7": '<span class="si">සම්පූර්ණ ආයෝජනය, දවසට විකුණිය යුතු අවම ප්‍රමාණය, ආයෝජනය '
             'ආපසු ලැබෙන මාස, සහ අවුරුද්දක් තුළ ආපසු ලබා ගැනීමේ ඉලක්කය.</span>'
             '<span class="en">Total investment, daily break-even volume, payback period and the one-year recovery target.</span>',
    }
    written = []
    for fname, num, si, en in PAGES:
        body = builders[num](M)
        html = shell(M, num, si, en, subs[num], body)
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append((fname, os.path.getsize(os.path.join(OUT, fname))))
        print(f"[ok] {fname:<28} {os.path.getsize(os.path.join(OUT, fname))/1024:,.0f} KB")

    # ---- landing page ----
    cards = []
    for fname, num, si, en in PAGES:
        desc = {
            "1": "ලියාපදිංචිය → ගොඩනැඟිල්ල → යන්ත්‍ර → වැඩ පටන් ගන්න දවස. "
                 "කාර්යාල උපකරණ ද ඇතුළුව.",
            "2": "නිෂ්පාදනය පටන් ගත් දවසේ සිට පළමු order stock එක ඉවර වෙනකම්. "
                 "බෝතල්, ලේබල්, පිරවීම, සේවක පඩි.",
            "3": "500 ml 5,000 · 1 L 3,000 · 1.5 L 3,000 · 5 L 1,000 · 19 L 150 "
                 "— එකක පිරිවැය වෙන වෙනම.",
            "4": "ක්‍රියාවලිය පියවරෙන් පියවර · අවශ්‍ය ලේඛන · ගතවන කාලය.",
        "5": "රැකියා ධූරාවලිය — Manufacturing & Quality · HR & Finance · "
             "Sales & Marketing · Transportation. වැටුප් + EPF/ETF සහිතව.",
        "6": "Factory → Distributor → Retail මිල පඩිපෙළ · නිෂ්පාදනය අනුව ලාභය · "
             "පළමු stock එකේ ලාභය.",
        "7": "මුළු අයවැය · දවසට විකුණිය යුතු ප්‍රමාණය · ආයෝජනය ආපසු "
             "ලැබෙන කාලය · අවුරුද්දක ඉලක්කය.",
        }[num]
        desc_en = {
            "1": "Registration, construction, machinery and readiness to start production, including office equipment.",
            "2": "The first production run, from line start until the first order stock is complete.",
            "3": "A unit-cost breakdown for the specified launch quantities across all five products.",
            "4": "A step-by-step workflow with required documents and estimated processing times.",
            "5": "Roles, reporting lines and salaries across four departments, including EPF/ETF.",
            "6": "Factory, distributor and retail pricing with margins by product.",
            "7": "Investment summary, daily sales threshold and estimated payback targets.",
        }[num]
        head = {"1": f'Rs {m(M["doc_totals"]["registration"]+M["doc_totals"]["equipment"]+M["office_total"]+M["doc_totals"]["transport"]+M["doc_totals"]["misc"]+M["hr_one_off_total"])}',
                "2": f'Rs {m(M["fp_total"])}',
                "3": f'Rs {M["fs_full_cost"]:,.0f}',
                "4": f'{len(M["process_steps"])} පියවර',
                "5": f'{M["hr_headcount"]} දෙනා · Rs {m(M["hr_month_total"])}/මාස',
                "6": f'ලාභය Rs {M["sales_totals"][3]:,.0f} ({M["sales_totals"][6]:.1f}%)',
                "7": f'ආයෝජනය {m(M["final"]["investment"])} · දවසට '
                     f'{M["final"]["be_day"]:,.0f} බෝතල්'}[num]
        category_si, category_en = PAGE_CATEGORY[num]
        cards.append(
            f'<a class="pcard" href="{fname}">'
            f'<div class="pc-kicker"><span class="si">{esc(category_si)}</span><span class="en">{esc(category_en)}</span></div>'
            f'<h3 class="pc-title"><span class="si">{esc(si)}</span></h3>'
            f'<div class="pc-en en">{esc(en)}</div>'
            f'<div class="pc-desc"><span class="si">{desc}</span><span class="en">{desc_en}</span></div>'
            f'<div class="pc-head">{head}</div></a>')

    overview = (
        '<section class="executive-overview" id="project-sections">'
        '<div class="overview-heading"><div>'
        '<p class="section-kicker"><span class="si">ආයෝජන අවස්ථාව</span><span class="en">Investment snapshot</span></p>'
        '<h2><span class="si">ව්‍යාපෘතිය — එක බැල්මකින්</span><span class="en">The project, at a glance</span></h2>'
        '</div><a class="overview-link" href="dashboard.html"><span class="si">සම්පූර්ණ විශ්ලේෂණය</span><span class="en">Full analysis</span><b aria-hidden="true">→</b></a></div>'
        '<div class="landing-metrics">'
        f'<article class="landing-metric"><span class="metric-label"><span class="si">නිර්දේශිත මුළු ආයෝජනය</span><span class="en">Recommended investment</span></span><strong>Rs {m(M["recommended"]["total_investment"])}</strong><small><span class="si">CAPEX + වැඩකරන ප්‍රාග්ධනය</span><span class="en">CAPEX plus working capital</span></small></article>'
        f'<article class="landing-metric"><span class="metric-label"><span class="si">නිෂ්පාදන ධාරිතාව</span><span class="en">Plant capacity</span></span><strong>{M["capacity_bph"]:,} <em>BPH</em></strong><small><span class="si">RO + UV + Ozone line</span><span class="en">RO + UV + Ozone line</span></small></article>'
        f'<article class="landing-metric"><span class="metric-label"><span class="si">Break-even ප්‍රමාණය</span><span class="en">Break-even volume</span></span><strong>{M["breakeven_pet"]:,}</strong><small><span class="si">PET බෝතල් / මාසය</span><span class="en">PET bottles per month</span></small></article>'
        f'<article class="landing-metric"><span class="metric-label"><span class="si">බෝතලයක දායකත්වය</span><span class="en">Contribution per bottle</span></span><strong>Rs {M["blend_contribution"]:,.2f}</strong><small><span class="si">මිශ්‍ර නිෂ්පාදන ඇස්තමේන්තුව</span><span class="en">Blended product estimate</span></small></article>'
        '</div></section>'
    )
    body = (overview + '<h2 class="pg-title">📄 ව්‍යාපෘති කොටස් — වෙන වෙනම</h2>'
            '<p class="lead">ඔබ ඉල්ලූ පිළිවෙළින් · <b>Project sections, in the order '
            'you asked for</b></p>'
            '<div class="grid g3">' + "".join(cards) + '</div>'
            '<div class="note ol"><b>📊 සම්පූර්ණ Dashboard එක:</b> සියල්ල එක පිටුවක '
            '<a href="dashboard.html">dashboard.html</a> · '
            '<b>📚 ලේඛන 21:</b> <a href="docs.html">docs.html</a></div>')
    html = shell(M, "0", "බෝතල් ජල කර්මාන්ත ශාලාව", "Bottled Drinking Water Plant",
                 '<span class="si">Mr. Thilakarathna ආයෝජනය කරන, Bandarawela හි පිහිටි '
                 '6,000 BPH බෝතල් කළ පානීය ජල කර්මාන්ත ශාලාවක්. '
                 'නිෂ්පාදන 5ක්: 500 ml · 1 L · 1.5 L · 5 L · 19 L.</span>'
                 '<span class="en">A 6,000 BPH bottled drinking water plant in Bandarawela, funded by Mr. Thilakarathna. '
                 'Five products: 500 ml, 1 L, 1.5 L, 5 L and 19 L.</span>',
                 body)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"[ok] index.html (landing)          "
          f"{os.path.getsize(os.path.join(OUT,'index.html'))/1024:,.0f} KB")
    print("\n[ok] 7 pages + landing written into site/")


if __name__ == "__main__":
    main()
