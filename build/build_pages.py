#!/usr/bin/env python3
"""Emit the four pages + the landing page. Run: python3 build/build_pages.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages_common import (OUT, PAGES, kpi, m, shell, table)   # noqa: E402
from dashboard_model import build_model                       # noqa: E402


# =====================================================================
# PAGE 1 - SETUP BUDGET
# =====================================================================
def page1(M):
    s = []
    s.append('<h2 style="font-size:21px;margin:0 0 6px">💰 ආරම්භයේ සිට වැඩ පටන් ගන්න '
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

    s.append('<h2 style="font-size:21px;margin:0 0 6px">🏭 නිෂ්පාදනය පටන් ගත් දවසේ සිට '
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
    s.append('<h2 style="font-size:21px;margin:0 0 6px">🧮 පළමු stock එකේ බෝතල් පිරිවැය</h2>'
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
    s.append('<h2 style="font-size:21px;margin:0 0 6px">🔄 ක්‍රියාවලිය — පියවරෙන් පියවර</h2>'
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


def main():
    M = build_model()
    os.makedirs(OUT, exist_ok=True)

    builders = {"1": page1, "2": page2, "3": page3, "4": page4}
    subs = {
        "1": "ෆැක්ටරි එක ලියාපදිංචි කර, ගොඩනැඟිල්ල ඉදිකර, යන්ත්‍ර සවිකර, "
             "වැඩ පටන් ගන්න දවස වෙනකම් වන සම්පූර්ණ පිරිවැය — කාර්යාල උපකරණ ද ඇතුළුව.",
        "2": "නිෂ්පාදනය පටන් ගත් දවසේ සිට පළමු order stock එක ඉවර වෙනකම් — "
             "බෝතල්, ලේබල්, පිරවීම, සේවක පඩි.",
        "3": "ඔබ දුන් ප්‍රමාණ අනුව පළමු stock එකේ බෝතල් පිරිවැය: "
             "500 ml 5,000 · 1 L 3,000 · 1.5 L 3,000 · 5 L 1,000 · 19 L 150.",
        "4": "ක්‍රියාවලිය පියවරෙන් පියවර, සෑම පියවරකටම අවශ්‍ය ලේඛන සහ "
             "ගතවන කාලය.",
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
        }[num]
        head = {"1": f'Rs {m(M["doc_totals"]["registration"]+M["doc_totals"]["equipment"]+M["office_total"]+M["doc_totals"]["transport"]+M["doc_totals"]["misc"]+M["hr_one_off_total"])}',
                "2": f'Rs {m(M["fp_total"])}',
                "3": f'Rs {M["fs_full_cost"]:,.0f}',
                "4": f'{len(M["process_steps"])} පියවර'}[num]
        cards.append(
            f'<a class="card" href="{fname}" style="text-decoration:none;color:inherit;'
            f'display:block;transition:box-shadow .15s" '
            f'onmouseover="this.style.boxShadow=\'0 8px 24px rgba(0,0,0,.12)\'" '
            f'onmouseout="this.style.boxShadow=\'\'">'
            f'<div style="font-size:11px;font-weight:700;letter-spacing:1px;'
            f'text-transform:uppercase;color:var(--emerald-d)">පිටුව {num} · Page {num}</div>'
            f'<h3 style="margin:6px 0 4px;font-size:16px">{si}</h3>'
            f'<div style="font-size:12px;color:var(--muted);margin-bottom:10px">{en}</div>'
            f'<div style="font-size:13px;color:var(--ink2);line-height:1.55">{desc}</div>'
            f'<div style="margin-top:12px;font-size:20px;font-weight:750;'
            f'color:var(--olive-d)">{head}</div></a>')

    body = ('<h2 style="font-size:21px;margin:0 0 6px">📄 පිටු 4ක් — වෙන වෙනම</h2>'
            '<p class="lead">ඔබ ඉල්ලූ පිළිවෙළින් · <b>The four pages, in the order '
            'you asked for</b></p>'
            '<div class="grid g2">' + "".join(cards) + '</div>'
            '<div class="note ol"><b>📊 සම්පූර්ණ Dashboard එක:</b> සියල්ල එක පිටුවක '
            '<a href="dashboard.html">dashboard.html</a> · '
            '<b>📚 ලේඛන 21:</b> <a href="docs.html">docs.html</a></div>')
    html = shell(M, "0", "බෝතල් ජල කර්මාන්ත ශාලාව", "Bandarawela Bottled Water Plant",
                 "Mr. Thilakarathna ආයෝජනය කරන, Bandarawela හි පිහිටි "
                 "6,000 BPH බෝතල් කළ පානීය ජල කර්මාන්ත ශාලාවක්. "
                 "නිෂ්පාදන 5ක්: 500 ml · 1 L · 1.5 L · 5 L · 19 L.",
                 body)
    html = html.replace('පිටුව 0 &nbsp;·&nbsp; Page 0 of 4',
                        'බණ්ඩාරවෙල · ඌව කඳුකරය &nbsp;·&nbsp; Bandarawela, Uva Highlands')
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"[ok] index.html (landing)          "
          f"{os.path.getsize(os.path.join(OUT,'index.html'))/1024:,.0f} KB")
    print("\n[ok] 4 pages + landing written into site/")


if __name__ == "__main__":
    main()
