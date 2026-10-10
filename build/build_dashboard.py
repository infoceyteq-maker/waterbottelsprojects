#!/usr/bin/env python3
"""
Render site/dashboard.html from the model in build/dashboard_model.py.
Run:  python3 build/build_dashboard.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_model import build_model, load_checklist  # noqa: E402
from language_support import (LANGUAGE_BOOTSTRAP, LANGUAGE_JS, LANGUAGE_SWITCH,
                              fill_empty_table_cells, highlight_prompts,
                              mark_bilingual_pairs)  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "dashboard.html")

_STYLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
with open(_STYLE, encoding="utf-8") as _fh:
    CSS = _fh.read()


_EMOJI = re.compile(
    "["
    "\U0001F000-\U0001FAFF"
    "\u2600-\u260F\u2613-\u2712\u2718-\u27BF"
    "\u2B00-\u2BFF"
    "\uFE0F\uFE0E"
    "\u2049\u203C"
    "]+"
)


def plain(text):
    """Strip pictographs so the pages read like a report, not a storybook.

    Deliberately KEPT, because they carry meaning rather than decoration:
      U+2190-21FF  arrows      "Factory -> Distributor"
      U+2610-2612  ballot boxes  the master checklist tick boxes
      U+2713/2717  tick / cross  status marks
    """
    return _EMOJI.sub("", text)

JS = """
const KEY='wb-dash-v1';
let state={};
try{state=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){state={}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}}
function toggle(id,el){
  if(el.checked){state[id]=1}else{delete state[id]}
  save(); paintRow(id); updateProgress();
}
function paintRow(id){
  const tr=document.querySelector('tr[data-id="'+id+'"]');
  if(tr) tr.classList.toggle('done', !!state[id]);
  const cb=tr&&tr.querySelector('.chk'); if(cb) cb.checked=!!state[id];
}
function updateProgress(){
  const total=document.querySelectorAll('tr[data-id]').length;
  const done=document.querySelectorAll('tr[data-id].done').length;
  const pct=total?Math.round(done/total*100):0;
  const el=document.getElementById('progbar');
  if(el){el.style.width=pct+'%';}
  const tx=document.getElementById('progtxt');
  if(tx){tx.textContent=done+' / '+total+'  ('+pct+'%)';}
}
function filt(){
  const q=(document.getElementById('q').value||'').toLowerCase();
  const ph=document.getElementById('fphase').value;
  const pr=document.getElementById('fprio').value;
  const st=document.getElementById('fstatus').value;
  let shown=0;
  document.querySelectorAll('tr[data-id]').forEach(tr=>{
    const okQ=!q||tr.textContent.toLowerCase().indexOf(q)>-1;
    const okP=!ph||tr.dataset.phase===ph;
    const okR=!pr||tr.dataset.prio===pr;
    const isDone=tr.classList.contains('done');
    const okS=!st||(st==='done'&&isDone)||(st==='todo'&&!isDone);
    const show=okQ&&okP&&okR&&okS;
    tr.classList.toggle('hidden',!show); if(show)shown++;
  });
  const c=document.getElementById('count');
  if(c) c.textContent=document.documentElement.lang==='en' ? shown+' items shown' : shown+' අයිතම දැක්වේ';
}
function resetAll(){
  if(!confirm('සියලු ලකුණු ඉවත් කරන්නද? / Clear all ticks?'))return;
  state={};save();
  document.querySelectorAll('tr[data-id]').forEach(tr=>{tr.classList.remove('done');
    const cb=tr.querySelector('.chk'); if(cb)cb.checked=false;});
  updateProgress();
}
document.addEventListener('wb-language-change',()=>filt());
document.addEventListener('DOMContentLoaded',()=>{
  Object.keys(state).forEach(paintRow);
  updateProgress();
  const ids=document.querySelectorAll('select option[data-ph]');
  // nav scroll-spy
  const links=[...document.querySelectorAll('#nav a[href^="#"]')];
  const secs=links.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const spy=()=>{
    let cur=secs[0];
    secs.forEach(s=>{if(s.getBoundingClientRect().top<=120)cur=s;});
    links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+cur.id));
  };
  window.addEventListener('scroll',spy,{passive:true}); spy();
});
"""
JS += "\n" + LANGUAGE_JS

PAGE = """<!doctype html>
<html lang="si"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
__LANG_BOOTSTRAP__
<title>බෝතල් ජල කර්මාන්ත ශාලාව — ව්‍යාපෘති Dashboard | Bottled Drinking Water Plant</title>
<style>__CSS__</style>
</head><body class="dashboard-page">
<div id="wrap">
<nav id="nav">
  <div class="brand">
    <div class="logo">💧</div>
    <h1><span class="si">බෝතල් ජල කර්මාන්ත ශාලාව</span>
      <span class="en">Bottled Drinking Water Plant</span></h1>
    <p>__LOCATION__<br><b><span class="si">ආයෝජක</span><span class="en">Investor</span>: __INVESTOR__</b></p>
    __LANGUAGE_SWITCH__
  </div>
  <div class="nav-links">
  <div class="nsec"><span class="si">දළ විශ්ලේෂණය</span><span class="en">Overview</span></div>
  <a href="#dash"><span class="si">📊 සාරාංශය</span><span class="en">Summary &amp; the 5 products</span></a>
  <a href="#project"><span class="si">🏭 ව්‍යාපෘතිය</span><span class="en">What exists today</span></a>
  <a href="#process"><span class="si">💧 පිරිපහදු ක්‍රියාවලිය</span><span class="en">Treatment train</span></a>
  <a href="#production"><span class="si">📦 නිෂ්පාදන 5</span><span class="en">Bottle quantities</span></a>
  <div class="nsec"><span class="si">පිරිවැය</span><span class="en">The cost</span></div>
  <a href="#budgets"><span class="si">💰 අයවැය ලේඛන 6</span><span class="en">The six budget documents</span></a>
  <a href="#total"><span class="si">🧾 මුළු ආයෝජනය</span><span class="en">Everything added up</span></a>
  <a href="#unitcost"><span class="si">🧮 බෝතලයක පිරිවැය</span><span class="en">Cost per bottle, all 5</span></a>
  <div class="nsec"><span class="si">ව්‍යාපෘති කොටස්</span><span class="en">Project sections</span></div>
  <a href="index.html"><span class="si">📄 ව්‍යාපෘති කොටස් — වෙන වෙනම</span><span class="en">Budget · Process · Management · Sales · Summary</span></a>
  <div class="nsec"><span class="si">ක්‍රියාත්මක කිරීම</span><span class="en">Execution</span></div>
  <a href="#checklist"><span class="si">✅ ලේඛන ලැයිස්තුව</span><span class="en">160-item checklist</span></a>
  <a href="#timeline"><span class="si">🗓️ කාලසටහන</span><span class="en">Timeline</span></a>
  <a href="#risks"><span class="si">⚠️ අවදානම්</span><span class="en">Top risks</span></a>
  </div>
</nav>
<main id="main">
__HERO__
<div class="inner">
__BODY__
<footer>
  💧 බෝතල් කළ පානීය ජල කර්මාන්ත ශාලාව · Bottled Drinking Water Plant<br>
  __LOCATION__ · ආයෝජක / Investor: <b>__INVESTOR__</b><br>
  නිෂ්පාදනය / Product: <b>Bottled Drinking Water (SLS 894)</b> ·
  මූලාශ්‍රය / Source: නළ ළිඳ / deep tube well ·
  සම්පූර්ණ RO + UV + Ozone පිරිපහදුව / full RO + UV + ozone treatment<br>
  සියලු මුදල් අගයන් <b>උපකල්පිත (indicative)</b> — quotation 3ක් ලබාගෙන තහවුරු කරගන්න.<br>
  All monetary figures are indicative — confirm with three written quotations.<br>
  සකස් කළ දිනය / Prepared: 2026-10-10
</footer>
</div>
</main>
</div>
<script>__JS__</script>
</body></html>"""


def bilingual_label(label):
    """Split the existing ``Sinhala / English`` short labels for the switcher."""
    text = str(label)
    if " / " in text:
        si, en = text.split(" / ", 1)
        if re.search(r"[\u0D80-\u0DFF]", si):
            return f'<span class="si">{si}</span><span class="en">{en}</span>'
    return text


def kpi(label, value, hint="", cls=""):
    return (f'<div class="kpi {cls}"><div class="l">{bilingual_label(label)}</div>'
            f'<div class="v">{value}</div><div class="h">{hint}</div></div>')


def bar_chart(rows, cls=""):
    mx = max(v for _, v in rows) or 1
    out = ['<div class="bar-chart">']
    for lbl, v in rows:
        w = max(2, round(v / mx * 100))
        out.append(
            f'<div class="bc-row"><div class="lbl">{lbl}</div>'
            f'<div class="bar {cls}"><i style="width:{w}%"></i></div>'
            f'<div class="val">{v:,.0f}</div></div>')
    out.append('</div>')
    return "\n".join(out)


def m(n):
    """LKR in millions"""
    return f"{n/1_000_000:,.1f}M"


ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "assets")
HERO_ASSET = os.path.join(ASSET_DIR, "upcountry-hero.jpg")
FALLBACK_ASSET = os.path.join(ASSET_DIR, "cover.jpg")
# Keep the previous project cover as a safe fallback, while using the new
# Bandarawela highlands photograph whenever it is part of the source tree.
ASSET = HERO_ASSET if os.path.exists(HERO_ASSET) else FALLBACK_ASSET


def hero(M, n_items, rec):
    """Full-width Uva Highlands cover embedded as a self-contained asset."""
    style, art = "", '<div class="nofallback">💧🏔️</div>'
    if os.path.exists(ASSET):
        with open(ASSET, "rb") as fh:
            import base64
            b64 = base64.b64encode(fh.read()).decode("ascii")
        style = f'background-image:url("data:image/jpeg;base64,{b64}")'
        art = ""  # the fallback tile must NOT render over the real photo
    return f"""<div class="hero hero--upcountry" style="{style}">
  {art}
  <div class="hc">
    <div class="kicker"><span class="si">බණ්ඩාරවෙල · ඌව කඳුකරය</span><span class="en">Bandarawela · Uva Highlands</span></div>
    <h1><span class="si">කඳුකර නියම ජලයෙන් බෝතල් කරන ලද පානීය ජලය</span>
      <span class="en">Bottled Drinking Water from the Uva Highlands</span></h1>
    <p class="hsub">
      <span class="si">Mr. {M["investor"]} ආයෝජනය කරන, {M["location"]} හි පිහිටි,
      {M["capacity_bph"]:,} BPH ධාරිතාවේ සම්පූර්ණ RO + UV + Ozone පිරිපහදු කර්මාන්ත ශාලාවක්.</span>
      <span class="en">A {M["capacity_bph"]:,} BPH plant at {M["location"]}, funded by Mr. {M["investor"]}.
      Currently only the land exists — building, plant and every approval start from scratch.</span>
    </p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="#dash"><span class="si">ව්‍යාපෘති සාරාංශය බලන්න</span><span class="en">View project summary</span><b class="btn-arrow" aria-hidden="true">→</b></a>
      <a class="btn btn-secondary" href="index.html"><span class="si">කොටස් 7 වෙත යන්න</span><span class="en">Explore the seven sections</span></a>
    </div>
    <div class="chips">
      <span class="chip">🏞️ <span class="si">ඉඩම ඇත</span><span class="en"><b>Land owned</b></span></span>
      <span class="chip">🏗️ <span class="si">ගොඩනැඟිල්ල + යන්ත්‍ර = මුල සිට</span><span class="en"><b>From scratch</b></span></span>
      <span class="chip"><span class="si">💰 ආයෝජනය</span><span class="en"><b>Investment</b></span> <b>Rs {rec["total_investment"]/1e6:,.1f}M</b></span>
      <span class="chip"><span class="si">🧾 බෝතලයක ලාභය</span><span class="en"><b>Contribution per bottle</b></span> <b>Rs {M["blend_contribution"]:.2f}</b></span>
      <span class="chip"><span class="si">📄 ලේඛන</span><span class="en"><b>Documents</b></span> <b>{n_items}</b></span>
    </div>
  </div>
</div>"""


def build():
    M = build_model()
    CL = load_checklist()

    # ---------- phase summary ----------
    phases = []
    for r in CL:
        if r["phase"] not in [p[0] for p in phases]:
            phases.append((r["phase"], 0, 0))
    pmap = {p[0]: [p[1], p[2]] for p in phases}
    for r in CL:
        pmap[r["phase"]][0] += 1
        if r["priority"] in ("Critical", "Mandatory"):
            pmap[r["phase"]][1] += 1
    phases = [(p[0], pmap[p[0]][0], pmap[p[0]][1]) for p in phases]

    crit = sum(1 for r in CL if r["priority"] == "Critical")
    mand = sum(1 for r in CL if r["priority"] == "Mandatory")
    high = sum(1 for r in CL if r["priority"] == "High")

    y1, y2, y3, y4 = M["projection"]
    REC = M["recommended"]

    s = []

    # ================= 1. SUMMARY =================
    s.append('<section id="dash"><h2><span class="n">1</span>📊 <span class="si">සාරාංශය — එක බැල්මකින්</span><span class="en">Summary — at a glance</span></h2>'
             '<p class="lead">ආයෝජකයා, ඉඩම, නිෂ්පාදන 5 සහ ප්‍රධාන පිරිවැය · '
             '<b>The investor, the land, the five products, and the two headline costs</b></p>')
    s.append('<div class="grid g4">')
    s.append(kpi("අදියර 1 — ෆැක්ටරි එක ඕපන් කරන තෙක්",
                 "Rs " + m(M["stage1_total"]),
                 "පටන් ගත් දවසේ සිට · ඉඩම + ගොඩනැඟිල්ල + ළිඳ + අනුමැති", "ol"))
    s.append(kpi("අදියර 2 — නිෂ්පාදනයට සූදානම් වන තෙක්",
                 "Rs " + m(M["stage2_total"]),
                 "යන්ත්‍ර + පිරිපහදු පද්ධතිය + QC lab", "am"))
    s.append(kpi("මුළු ආයෝජනය / Total investment",
                 "Rs " + m(M["total_investment"]),
                 "CAPEX + contingency 15% + working capital"))
    s.append(kpi("Mr. Thilakarathna ගේ මුදල්",
                 "Rs " + m(M["cash_investment"]),
                 f'ඉඩම් වටිනාකම Rs {m(M["land_value"])} අඩු කිරීමෙන් පසු', "bl"))
    s.append('</div>')

    s.append('<h3><span class="si">🍶 නිෂ්පාදන 5ක් — වෙන වෙනම</span><span class="en">The five products, separately</span></h3>')
    s.append('<div class="tbl scroll"><table><thead><tr>'
             '<th>නිෂ්පාදනය / Product</th><th class="num">Mix %</th>'
             '<th class="num">එකක පිරිවැය / Cost</th>'
             '<th class="num">Ex-factory මිල</th>'
             '<th class="num">ලාභය / Margin</th>'
             '<th class="num">Margin %</th></tr></thead><tbody>')
    for sk in M["skus"]:
        c = sk["variable_cost"]
        mg = sk["ex_factory_price"] - c
        s.append(f'<tr><td><b>💧 {sk["sku"]}</b></td>'
                 f'<td class="num">{sk["share"]*100:.0f}%</td>'
                 f'<td class="num">Rs {c:,.2f}</td>'
                 f'<td class="num">Rs {sk["ex_factory_price"]:,.0f}</td>'
                 f'<td class="num">Rs {mg:,.2f}</td>'
                 f'<td class="num">{mg/sk["ex_factory_price"]*100:.1f}%</td></tr>')
    c19 = M["sku19"]["variable_cost"]
    mg19 = M["sku19"]["ex_factory_price"] - c19
    s.append(f'<tr><td><b>🫙 {M["sku19"]["sku"]}</b></td><td class="num">—</td>'
             f'<td class="num">Rs {c19:,.2f}</td>'
             f'<td class="num">Rs {M["sku19"]["ex_factory_price"]:,.0f}</td>'
             f'<td class="num">Rs {mg19:,.2f}</td>'
             f'<td class="num">{mg19/M["sku19"]["ex_factory_price"]*100:.1f}%</td></tr>')
    s.append('</tbody></table></div>')
    s.append('<div class="note ol"><b>📌 ඔබ ඉල්ලූ පරිදි:</b> මෙම dashboard එක '
             '<b>නිෂ්පාදනය ආරම්භ කරන තැනින් නවතී.</b> අවුරුදු ගණන් ලාභ/පාඩු '
             'ප්‍රක්ෂේපණ <b>මෙහි නැත</b> — ඒවා පසුව වෙනම සාදමු. '
             '<br><b>As you asked:</b> this stops at the point manufacturing begins. '
             'No multi-year profit projections here — we will do those separately later.</div>')
    s.append('</section>')
    # ================= PROJECT =================
    s.append('<section id="project"><h2><span class="n">2</span>🏭 <span class="si">ව්‍යාපෘතිය — දැන් තිබෙන්නේ මොනවාද?</span><span class="en">Project — what exists today?</span></h2>'
             '<p class="lead">දැනට ඇති දේ සහ මුල සිට ගොඩනැගිය යුතු දේ · <b>What exists today vs. what must be built from scratch</b></p>')
    s.append('<div class="grid g2">')
    s.append('<div class="card"><h3 style="margin-top:0">✅ දැනට තිබෙන දේ / What exists today</h3>'
             '<div class="tbl"><table>'
             '<tr><th>අයිතමය</th><th>තත්ත්වය</th></tr>'
             f'<tr class="land"><td><b>ඉඩම</b> — {M["location"]}</td>'
             f'<td><span class="pill p-ok">✓ ඇත</span> — {M["investor"]} සතු</td></tr>'
             '<tr><td>ආයෝජකයා</td><td><span class="pill p-ok">✓ සිටී</span> — '
             f'{M["investor"]}</td></tr>'
             '<tr><td>ව්‍යාපාර සංකල්පය</td><td><span class="pill p-ok">✓ පැහැදිලියි</span></td></tr>'
             '</table></div>'
             '<div class="note rd" style="margin-bottom:0"><b>⚠️ තහවුරු කළ යුතුයි:</b> '
             'ඉඩම <b>පර්චස් 160+</b> ද? කර්මාන්ත භාවිතයට <b>zoning අවසර</b> තිබේද? '
             'ඉඩම සමාගමට <b>හරවා දෙන්නේද / බදු දෙන්නේද?</b> — FCAU ලියාපදිංචියට මෙය අත්‍යවශ්‍යයි.</div>'
             '</div>')
    s.append('<div class="card"><h3 style="margin-top:0">🏗️ මුල සිට කළ යුතු දේ / To be built from scratch</h3>'
             '<div class="tbl"><table><tr><th>කොටස</th><th class="num">පිරිවැය (Rs)</th></tr>')
    cats = {}
    for name, qty, unit, rate, amt, cat, inkind, stg, doc in M["capex"]:
        cats[cat] = cats.get(cat, 0) + amt
    for cat, label in [("building", "🏢 ගොඩනැඟිල්ල"), ("plant", "⚙️ යන්ත්‍රෝපකරණ + QC lab"),
                       ("utility", "⚡ Utilities"), ("env", "🌿 පරිසර + ආරක්ෂාව"),
                       ("logistics", "🚚 වාහන + ගබඩා"), ("pre", "📄 ලියාපදිංචි + උපදේශන")]:
        s.append(f'<tr><td>{label}</td><td class="num">{cats[cat]:,}</td></tr>')
    s.append(f'<tr class="tot"><td>මුළු (ඉඩම හැර)</td>'
             f'<td class="num">{M["capex_subtotal"]-M["land_value"]:,}</td></tr>')
    s.append('</table></div></div>')
    s.append('</div>')

    s.append('<div class="note ol"><b>💡 මූලික කරුණ:</b> ඉඩම පමණක් තිබීමෙන් '
             '<b>කිසිදු අනුමැතියක් ලැබී නැත.</b> FCAU බෝතල් ජල ලියාපදිංචිය ලැබෙන තෙක් '
             'නිෂ්පාදනය ආරම්භ කළ <b>නොහැක</b>. සම්පූර්ණ මාර්ගය: '
             'සමාගම් ලියාපදිංචිය → ඉඩම්/zoning අනුමැති → WRB ළිඳ → ඉදිකිරීම් → '
             'FCAU + SLSI → CEA EPL → නිෂ්පාදනය. <b>මාස 14–20.</b></div>')
    s.append('</section>')

    # ================= PROCESS =================
    s.append('<section id="process"><h2><span class="n">3</span>💧 <span class="si">පිරිපහදු ක්‍රියාවලිය — filtration දාමය</span><span class="en">Water treatment process — filtration train</span></h2>'
             '<p class="lead">නළ ළිඳේ සිට බෝතලය දක්වා — අනුපිළිවෙළ වැදගත් · <b>Water treatment train — well to bottle</b></p>')
    s.append('<div class="flow">')
    steps = [("🕳️ නළ ළිඳ", ""), ("Raw tank", ""), ("⭐ Sand filter<br>(MGSF)", "key"),
             ("⭐ Carbon filter<br>(ACF)", "key"), ("Softener", ""), ("Micron<br>5→1→0.5µm", ""),
             ("⭐⭐ RO", "star"), ("Re-mineralise", ""), ("UV", ""),
             ("⭐⭐ Ozone<br>0.2–0.4 ppm", "star"), ("0.2µm sterile", ""),
             ("🍶 Filling<br>(cleanroom)", "")]
    for i, (lbl, cls) in enumerate(steps):
        if i:
            s.append('<span class="ar">→</span>')
        s.append(f'<div class="st {cls}">{lbl}</div>')
    s.append('</div>')

    s.append('<div class="grid g2" style="margin-top:8px">')
    s.append('<div class="card"><h3 style="margin-top:0">🔬 එක් එක් පෙරහන මොනවා ඉවත් කරයිද?</h3>'
             '<div class="scroll"><table><tr><th>පියවර</th><th>ඉවත් කරයි</th><th>නොකරයි</th></tr>'
             '<tr><td><b>Sand (MGSF)</b></td><td>Turbidity, අංශු, iron</td><td>ලවණ, ක්ෂුද්‍ර ජීවී</td></tr>'
             '<tr><td><b>Carbon (ACF)</b></td><td>Chlorine, ගඳ, රස, වර්ණ</td><td>ලවණ, hardness</td></tr>'
             '<tr><td><b>Softener</b></td><td>Hardness (Ca, Mg)</td><td>අනෙක් සියල්ල</td></tr>'
             '<tr><td><b>Micron 5/1/0.5</b></td><td>කුඩා අංශු, carbon fines</td><td>දියවූ ලවණ</td></tr>'
             '<tr class="land"><td><b>RO</b></td><td><b>95–99% TDS, arsenic, fluoride, nitrate, '
             'බැර ලෝහ</b></td><td>දියවූ වායු</td></tr>'
             '<tr><td><b>UV</b></td><td>බැක්ටීරියා, virus</td><td>අංශු, රසායනික</td></tr>'
             '<tr class="land"><td><b>Ozone</b></td><td><b>සියලු ක්ෂුද්‍ර ජීවී + බෝතලය/මූඩිය '
             'ඇතුළත</b></td><td>—</td></tr></table></div></div>')
    s.append('<div class="card"><h3 style="margin-top:0">🔴 වැදගත්ම අවදානම් 3</h3>'
             '<div class="note rd"><b>1. BROMATE</b> — Ozone + Bromide → පිළිකා කාරක. '
             'මූලාශ්‍ර ජලයේ <b>bromide පරීක්ෂා කිරීම අනිවාර්යයි.</b></div>'
             '<div class="note am"><b>2. RO reject 25–50%</b> — දිනකට ~26 m³ අපතේ යයි. '
             'Reuse සැලැස්මක් අවශ්‍යයි (cooling tower, බිම් සේදීම, වැසිකිළි).</div>'
             '<div class="note"><b>3. Ozone residual 0.2–0.4 ppm</b> — 0.15 ට වඩා අඩු නම් '
             'ක්ෂුද්‍ර ජීව වර්ධනය; 0.5 ට වඩා වැඩි නම් bromate + රස ප්‍රශ්න. '
             '<b>සෑම batch එකකම පරීක්ෂා කරන්න.</b></div></div>')
    s.append('</div></section>')

    # ================= 4. PRODUCTION =================
    s.append('<section id="production"><h2><span class="n">4</span>📦 <span class="si">නිෂ්පාදන පරිමාව — බෝතල් Qty</span><span class="en">Production volume — bottle quantities</span></h2>'
             '<p class="lead">නිෂ්පාදන 5ම වෙන වෙනම · '
             '<b>All five products, each with its own monthly quantity</b></p>')
    s.append('<div class="grid g4">')
    s.append(kpi("ධාරිතාව / Capacity", f'{M["capacity_bph"]:,} <em>BPH</em>',
                 f'බෝතල් පැයට · {M["shift_hours"]}h × {M["work_days"]}d/මාස'))
    s.append(kpi("මාසික උපරිමය / Nameplate", f'{M["nameplate_month"]:,}',
                 "බෝතල්/මාස — 100% ධාරිතාවේදී", "ol"))
    s.append(kpi("නිෂ්පාදන වර්ග / Products", "5",
                 "500 ml · 1 L · 1.5 L · 5 L · 19 L", "am"))
    s.append(kpi("PET රේඛාව + 19 L රේඛාව", "2",
                 "වෙනම යන්ත්‍ර දෙකක්", "bl"))
    s.append('</div>')

    s.append('<h3>📋 මාසික බෝතල් ප්‍රමාණය — නිෂ්පාදනය අනුව '
             '<span class="en">Monthly bottle quantity by product</span></h3>')
    s.append('<div class="tbl scroll"><table><thead><tr>'
             '<th>නිෂ්පාදනය / Product</th><th class="num">Mix %</th>'
             '<th class="num">50% ධාරිතාව</th><th class="num">75% ධාරිතාව</th>'
             '<th class="num">100% ධාරිතාව</th>'
             '<th class="num">ලීටර්/මාස (100%)</th></tr></thead><tbody>')
    tot = {u: 0 for u in (50, 75, 100)}
    for sk in M["skus"]:
        cells = []
        for u in (50, 75, 100):
            q = round(M["nameplate_month"] * u / 100 * sk["share"])
            tot[u] += q
            cells.append(q)
        s.append(f'<tr><td><b>💧 {sk["sku"]}</b></td>'
                 f'<td class="num">{sk["share"]*100:.0f}%</td>'
                 + "".join(f'<td class="num">{c:,}</td>' for c in cells)
                 + f'<td class="num">{round(cells[2]*sk["volume_l"]):,} L</td></tr>')
    s.append(f'<tr class="tot"><td>PET මුළු / PET total</td><td class="num">100%</td>'
             + "".join(f'<td class="num">{tot[u]:,}</td>' for u in (50, 75, 100))
             + f'<td class="num">{round(sum(round(M["nameplate_month"]*sk["share"]*sk["volume_l"]) for sk in M["skus"])):,} L</td></tr>')
    s.append(f'<tr class="land"><td><b>🫙 19 L (returnable)</b></td>'
             f'<td class="num">වෙනම රේඛාව</td>'
             f'<td class="num">20,000</td><td class="num">45,000</td>'
             f'<td class="num">80,000</td>'
             f'<td class="num">{80000*19:,} L</td></tr>')
    s.append('</tbody></table></div>')
    s.append('<div class="note"><b>💡 19 L රේඛාව වෙනමයි:</b> එය PET monoblock එකෙන් '
             'පිටත, වෙනම wash-fill-cap යන්ත්‍රයකි. බෝතල් නැවත ලබාගෙන සෝදා '
             'පුරවන බැවින් <b>බෝතලයක පිරිවැය ඉතා අඩුය</b> (Rs '
             f'{M["sku19"]["variable_cost"]:.2f}) නමුත් ආරම්භක බෝතල් තොගයක් '
             'මිලදී ගත යුතුය.</div>')
    s.append('</section>')
    # ======== 5. THE SIX BUDGET DOCUMENTS ========
    s.append('<section id="budgets"><h2><span class="n">5</span>💰 <span class="si">අයවැය ලේඛන 6ක් — වෙන වෙනම</span>'
             '<span class="en">The six budget documents — separately</span></h2>'
             '<p class="lead">ඔබේ ලේඛන 6ට අනුව වෙන් කර ඇත · '
             '<b>Split into the six budget documents, each one separate</b></p>')

    # quick index of the six
    s.append('<div class="tbl"><table><thead><tr><th>අයවැය ලේඛනය / Budget document</th>'
             '<th class="num">අයිතම්</th><th class="num">එක වර (CAPEX)</th>'
             '<th class="num">මාසික (OPEX)</th></tr></thead><tbody>')
    for key, si, en in M["budget_docs"]:
        rows = [r for r in M["capex"] if r[8] == key]
        capex = sum(r[4] for r in rows)
        opex = ""
        if key == "raw_material":
            opex = f'Rs {M["rawmat_month"]:,.0f}'
            capex = 0
        elif key == "hr":
            opex = f'Rs {M["hr_month_total"]:,.0f}'
        s.append(f'<tr><td><b class="si">{si}</b> <span class="en" style="color:var(--muted);font-size:11.5px">'
                 f'{en}</span></td><td class="num">{len(rows) if rows else "—"}</td>'
                 f'<td class="num">{("Rs "+format(capex,",")) if capex else "—"}</td>'
                 f'<td class="num">{opex or "—"}</td></tr>')
    s.append('</tbody></table></div>')

    def doc_table(num, key, emoji_si, en, rows, note):
        out = [f'<h3>{emoji_si} <span class="si">{en.split(" / ")[0]}</span> '
               f'<span class="en">{en.split(" / ")[-1]}</span></h3>']
        if rows:
            out.append('<div class="tbl scroll"><table><thead><tr>'
                       '<th style="width:30px">#</th><th>අයිතමය / Item</th>'
                       '<th class="num">Qty</th><th>ඒකකය</th>'
                       '<th class="num">ඒකක මිල (Rs)</th><th class="num">මුදල (Rs)</th>'
                       '<th>අදියර</th></tr></thead><tbody>')
            n = 0
            for name, qty, unit, rate, amt, cat, inkind, stg, doc in rows:
                n += 1
                cls = ' class="land"' if inkind else ''
                tag = ' <span class="pill p-gold">in-kind</span>' if inkind else ''
                out.append(f'<tr{cls}><td class="num">{n}</td><td>{name}{tag}</td>'
                           f'<td class="num">{qty:,}</td><td>{unit}</td>'
                           f'<td class="num">{rate:,.0f}</td>'
                           f'<td class="num"><b>{amt:,}</b></td>'
                           f'<td><span class="pill {"p-ok" if stg==1 else "p-med"}">'
                           f'අදියර {stg}</span></td></tr>')
            out.append(f'<tr class="grand"><td></td><td>මුළු / TOTAL</td>'
                       f'<td class="num"></td><td></td><td class="num"></td>'
                       f'<td class="num">{sum(r[4] for r in rows):,}</td>'
                       f'<td></td></tr></tbody></table></div>')
        out.append(note)
        return out

    # ---- 1. Registration ----
    s += doc_table(1, "registration", "📄", "ලියාපදිංචි අයවැය / Registration Budget",
                   [r for r in M["capex"] if r[8] == "registration"],
                   '<div class="note ol">සමාගම් ලියාපදිංචියේ සිට FCAU + SLSI + CEA '
                   'අනුමැතිය දක්වා සියලු නීතිමය සහ ලියාපදිංචි වියදම්. '
                   '<b>Company incorporation through to FCAU, SLSI and CEA approval.</b></div>')

    # ---- 2. Equipment ----
    s += doc_table(2, "equipment", "⚙️", "උපකරණ + ඉදිකිරීම් අයවැය / Equipment Budget",
                   [r for r in M["capex"] if r[8] == "equipment"],
                   '<div class="note">ගොඩනැඟිල්ල, cleanroom, සම්පූර්ණ ජල පිරිපහදු දාමය, '
                   'filling line, 19L රේඛාව, QC lab සහ utilities. '
                   '<b>Building, cleanroom, the full treatment train, filling lines, '
                   'the 19 L line, QC lab and utilities.</b></div>')

    # ---- 3. Raw material (monthly OPEX) ----
    s.append('<h3>🧴 අමුද්‍රව්‍ය අයවැය / Raw Material Budget '
             '<span class="en">monthly, at 100% capacity</span></h3>')
    s.append('<div class="tbl scroll"><table><thead><tr>'
             '<th>අමුද්‍රව්‍යය / Material</th><th class="num">මාසික Qty</th>'
             '<th>ඒකකය</th><th class="num">ඒකක මිල (Rs)</th>'
             '<th class="num">මාසික මුදල (Rs)</th></tr></thead><tbody>')
    for nm, qty, unit, rate, amt in M["rawmat_rows"]:
        s.append(f'<tr><td>{nm}</td><td class="num">{qty:,}</td><td>{unit}</td>'
                 f'<td class="num">{rate:,.2f}</td><td class="num"><b>{amt:,.0f}</b></td></tr>')
    s.append(f'<tr class="grand"><td>මාසික මුළු / MONTHLY TOTAL</td><td class="num"></td>'
             f'<td></td><td class="num"></td><td class="num">{M["rawmat_month"]:,.0f}</td></tr>')
    s.append(f'<tr class="sub"><td>වාර්ෂික / Annual (× 12)</td><td class="num"></td>'
             f'<td></td><td class="num"></td><td class="num">{M["rawmat_month"]*12:,.0f}</td></tr>')
    s.append('</tbody></table></div>')
    s.append('<div class="note ol"><b>📌 Wastage ඇතුළත්:</b> බෝතල් × 1.03 · මූඩි × 1.03 · '
             'ලේබල් × 1.04 · shrink film × 1.05. '
             '100% ධාරිතාවේදී (බෝතල් '
             f'{M["nameplate_month"]:,}/මාස) ගණනය කර ඇත.</div>')

    # ---- 4. Transportation ----
    s += doc_table(4, "transport", "🚚", "ප්‍රවාහන අයවැය / Transportation Budget",
                   [r for r in M["capex"] if r[8] == "transport"],
                   '<div class="note">බෙදාහැරීමේ වාහන සහ ගබඩා උපකරණ. '
                   'Option A (Lean Start) තෝරාගතහොත් මෙය <b>3PL බෙදාහැරීමකින් '
                   'ප්‍රතිස්ථාපනය කර Rs 20.5M ඉතිරි කරගත හැක.</b></div>')

    # ---- 5. HR ----
    s.append('<h3>👷 මානව සම්පත් අයවැය / HR Budget '
             '<span class="en">monthly payroll</span></h3>')
    s.append('<div class="tbl scroll"><table><thead><tr>'
             '<th>තනතුර / Role</th><th class="num">සේවකයන්</th>'
             '<th class="num">එකෙකුගේ වැටුප (Rs)</th>'
             '<th class="num">මාසික මුළු (Rs)</th></tr></thead><tbody>')
    for role, n, sal in M["hr_plan"]:
        s.append(f'<tr><td>{role}</td><td class="num">{n}</td>'
                 f'<td class="num">{sal:,}</td><td class="num"><b>{n*sal:,}</b></td></tr>')
    s.append(f'<tr class="sub"><td>දළ වැටුප් / Gross salaries</td>'
             f'<td class="num">{M["hr_headcount"]}</td><td class="num"></td>'
             f'<td class="num">{M["hr_gross"]:,.0f}</td></tr>')
    s.append(f'<tr><td>EPF (සේවාදායක 12%) + ETF (3%)</td><td class="num"></td>'
             f'<td class="num"></td><td class="num">{M["hr_employer"]:,.0f}</td></tr>')
    s.append(f'<tr class="grand"><td>මාසික මුළු / MONTHLY TOTAL</td>'
             f'<td class="num">{M["hr_headcount"]}</td><td class="num"></td>'
             f'<td class="num">{M["hr_month_total"]:,.0f}</td></tr>')
    s.append(f'<tr class="sub"><td>වාර්ෂික / Annual (× 12)</td><td class="num"></td>'
             f'<td class="num"></td><td class="num">{M["hr_year_total"]:,.0f}</td></tr>')
    s.append('</tbody></table></div>')
    s.append('<h3 style="font-size:13.5px">එක වර වියදම් / One-off HR costs</h3>')
    s.append('<div class="tbl"><table><tbody>')
    for nm, q, r in M["hr_one_off"]:
        s.append(f'<tr><td>{nm}</td><td class="num">{q}</td>'
                 f'<td class="num">{r:,}</td><td class="num"><b>{q*r:,}</b></td></tr>')
    s.append(f'<tr class="tot"><td>මුළු / Total</td><td class="num"></td>'
             f'<td class="num"></td><td class="num">{M["hr_one_off_total"]:,}</td></tr>')
    s.append('</tbody></table></div>')
    s.append('<div class="note rd"><b>⚠️ EPF/ETF:</b> පළමු සේවකයා බඳවා ගත් '
             'දින <b>14ක් ඇතුළත</b> EPF Form D ඉදිරිපත් කළ යුතුය. '
             'සේවාදායක 12% + ETF 3% = <b>15%</b> අමතර බර. '
             'වැටුප් නියම කිරීමේදී මෙය අමතක නොකරන්න.</div>')

    # ---- 6. Miscellaneous ----
    s += doc_table(6, "misc", "📦", "විවිධ අයවැය / Miscellaneous Budget",
                   [r for r in M["capex"] if r[8] == "misc"],
                   '<div class="note">පරිසර පද්ධති (ETP), ගිනි ආරක්ෂාව සහ '
                   'කීට පාලනය. Contingency සහ working capital පහත '
                   '"මුළු ආයෝජනය" කොටසේ දක්වා ඇත.</div>')
    s.append('</section>')
    # ---- the combined roll-up ----
    s.append('<section id="total"><h2><span class="n">7</span>🧾 <span class="si">මුළු ආයෝජනය — එක තැනක</span><span class="en">Total investment — all in one place</span></h2>'
             '<p class="lead">අදියර 1 + අදියර 2 + contingency + working capital · '
             '<b>Everything added up in one place</b></p>')
    s.append('<div class="tbl"><table><tbody>')
    s.append(f'<tr><td><b>A.</b> අදියර 1 — ෆැක්ටරි එක ඕපන් කරන තෙක් '
             f'<span style="color:var(--muted);font-size:12px">({len(M["stage1_rows"])} අයිතම්)</span></td>'
             f'<td class="num">{M["stage1_total"]:,}</td></tr>')
    s.append(f'<tr><td><b>B.</b> අදියර 2 — නිෂ්පාදනයට සූදානම් වන තෙක් '
             f'<span style="color:var(--muted);font-size:12px">({len(M["stage2_rows"])} අයිතම්)</span></td>'
             f'<td class="num">{M["stage2_total"]:,}</td></tr>')
    s.append(f'<tr class="tot"><td><b>C.</b> CAPEX උප මුළු (A + B)</td>'
             f'<td class="num">{M["capex_subtotal"]:,}</td></tr>')
    s.append(f'<tr><td><b>D.</b> Contingency @ 15% '
             '<span style="color:var(--muted);font-size:12px">මිල ඉහළ යාමට ආරක්ෂාව</span></td>'
             f'<td class="num">{M["contingency"]:,}</td></tr>')
    s.append(f'<tr class="tot"><td><b>E.</b> මුළු CAPEX (C + D)</td>'
             f'<td class="num">{M["total_capex"]:,}</td></tr>')
    s.append(f'<tr><td><b>F.</b> Working capital (මාස 3) '
             '<span style="color:var(--muted);font-size:12px">බෝතල්, ලේබල්, වැටුප්, විදුලිය</span></td>'
             f'<td class="num">{M["working_capital"]:,}</td></tr>')
    s.append(f'<tr class="grand"><td><b>G.</b> 💰 මුළු ආයෝජනය / TOTAL INVESTMENT (E + F)</td>'
             f'<td class="num">{M["total_investment"]:,}</td></tr>')
    s.append(f'<tr class="grand cash"><td>💵 <b>Mr. Thilakarathna ගේ මුදල් අවශ්‍යතාව / '
             f'CASH REQUIRED</b> <span style="font-size:12px">(G − ඉඩම් වටිනාකම '
             f'Rs {M["land_value"]:,})</span></td>'
             f'<td class="num">{M["cash_investment"]:,}</td></tr>')
    s.append('</tbody></table></div>')
    s.append('<div class="note rd"><b>⚠️ මිල සටහන:</b> සියලු අගයන් '
             '<b>උපකල්පිත (indicative)</b>. යන්ත්‍ර සඳහා <b>quotation 3ක්</b> ලබාගෙන '
             'තහවුරු කරගන්න — රේගු තීරු බදු, PAL, VAT, නැව් ගාස්තු සහ විනිමය අනුපාත '
             'අනුව සැලකිය යුතු ලෙස වෙනස් වේ.</div>')
    s.append('</section>')
    # ============ 8. COST OF ONE BOTTLE, PER PRODUCT ============
    s.append('<section id="unitcost"><h2><span class="n">8</span>🧮 <span class="si">එක බෝතලයක පිරිවැය — නිෂ්පාදන 5ම වෙන වෙනම</span>'
             '<span class="en">Cost per bottle — all five products separately</span></h2>'
             '<p class="lead">සෑම නිෂ්පාදනයක්ම වෙන වෙනම · '
             '<b>The cost of one bottle, worked out separately for each of the five products</b></p>')

    def cost_card(title, emoji, costs, price, cls=""):
        total = sum(costs.values())
        out = [f'<div class="card {cls}"><h3 style="margin-top:0">{emoji} {title}</h3>']
        out.append('<div class="tbl"><table><tbody>')
        for k, v in costs.items():
            out.append(f'<tr><td>{k}</td><td class="num">Rs {v:,.2f}</td>'
                       f'<td class="num" style="color:var(--faint)">{v/total*100:.1f}%</td></tr>')
        out.append(f'<tr class="grand"><td>💰 එකක මුළු පිරිවැය / TOTAL COST PER BOTTLE</td>'
                   f'<td class="num">Rs {total:,.2f}</td><td class="num">100%</td></tr>')
        out.append(f'<tr class="sub"><td>Ex-factory මිල / Selling price</td>'
                   f'<td class="num">Rs {price:,.2f}</td><td class="num"></td></tr>')
        out.append(f'<tr class="sub"><td>ලාභය / Margin</td>'
                   f'<td class="num">Rs {price-total:,.2f}</td>'
                   f'<td class="num">{(price-total)/price*100:.1f}%</td></tr>')
        out.append('</tbody></table></div></div>')
        return "".join(out)

    for sk in M["skus"]:
        s.append(cost_card(sk["sku"], "💧", sk["costs"], sk["ex_factory_price"]))
    s.append(cost_card(M["sku19"]["sku"] + " — returnable", "🫙",
                       M["sku19"]["costs"], M["sku19"]["ex_factory_price"], "land"))

    s.append('<h3>📊 පිරිවැය සංසන්දනය <span class="en">All five side by side</span></h3>')
    s.append('<div class="tbl scroll"><table><thead><tr>'
             '<th>නිෂ්පාදනය</th>'
             + "".join(f'<th class="num">{k}</th>' for k in M["skus"][0]["costs"])
             + '<th class="num">මුළු</th></tr></thead><tbody>')
    keys = list(M["skus"][0]["costs"])
    for sk in M["skus"]:
        cells = "".join(f'<td class="num">{sk["costs"].get(k, 0):,.2f}</td>' for k in keys)
        s.append(f'<tr><td><b>{sk["sku"]}</b></td>{cells}'
                 f'<td class="num"><b>{sk["variable_cost"]:,.2f}</b></td></tr>')
    s.append('</tbody></table></div>')
    s.append('<div class="note ol"><b>📌 5 L ගැන:</b> 5 L බෝතලයක PET පිරිවැය '
             'Rs 42.00 ක් වුවද, ලීටරයකට පිරිවැය ඉතා අඩුය '
             f'(Rs {76.80/5:,.2f}/L, 500 ml හි Rs {26.70/0.5:,.2f}/L ට සාපේක්ෂව). '
             'එබැවින් 5 L <b>පවුල් සහ කාර්යාල වෙළඳපොළට</b> ඉතා ලාභදායීයි.</div>')
    s.append('</section>')
    # ================= CHECKLIST =================
    s.append('<section id="checklist"><h2><span class="n">10</span>✅ <span class="si">ලේඛන සහ අවශ්‍යතා ලැයිස්තුව</span> <span class="en" style="font-size:13px;font-weight:600;color:var(--muted)">Documents &amp; requirements</span></h2>'
             f'<p class="lead">අයිතම {len(CL)}ක් · 🔴 Critical {crit} · 🟠 Mandatory {mand} · '
             f'🟡 High {high} — ලකුණු දැමූ පසු browser එකේ සේව් වේ</p>')
    s.append('<div class="card" style="margin-bottom:16px">'
             '<div style="display:flex;justify-content:space-between;align-items:center;'
             'margin-bottom:8px;font-size:13px;font-weight:600">'
             '<span>ප්‍රගතිය / Progress</span><span id="progtxt">0 / 0</span></div>'
             '<div class="bar" style="height:12px"><i id="progbar" style="width:0%"></i></div></div>')
    s.append('<div class="controls">'
             '<input type="search" id="q" placeholder="🔍 සොයන්න... (උදා: FCAU, ozone, TIN)" oninput="filt()">'
             '<select id="fphase" onchange="filt()"><option value="">සියලු Phase</option>' +
             "".join(f'<option value="{p[0]}">{p[0]}</option>' for p in phases) +
             '</select>'
             '<select id="fprio" onchange="filt()"><option value="">සියලු ප්‍රමුඛතා</option>'
             '<option>Critical</option><option>Mandatory</option><option>High</option>'
             '<option>Medium</option><option>Low</option></select>'
             '<select id="fstatus" onchange="filt()"><option value="">සියල්ල</option>'
             '<option value="todo">⬜ නොකළ</option><option value="done">✅ කළ</option></select>'
             '<button onclick="resetAll()" style="padding:8px 14px;border:1px solid var(--border2);'
             'border-radius:9px;background:var(--surface);cursor:pointer;font-family:inherit;'
             'font-size:13px">↺ Reset</button>'
             '<span id="count" style="font-size:12px;color:var(--muted)"></span>'
             '</div>')
    s.append('<div class="tbl"><table id="cl"><thead><tr>'
             '<th style="width:38px">✅</th><th>ID</th><th>ලේඛනය / අයිතමය</th>'
             '<th>ලබා ගන්නේ</th><th>කවදා</th><th class="num">වියදම (LKR)</th>'
             '<th>ප්‍රමුඛතාව</th></tr></thead><tbody>')
    pill = {"Critical": "p-crit", "Mandatory": "p-mand", "High": "p-high",
            "Medium": "p-med", "Low": "p-low"}
    for r in CL:
        s.append(
            f'<tr data-id="{r["id"]}" data-phase="{r["phase"]}" data-prio="{r["priority"]}">'
            f'<td><input type="checkbox" class="chk" onchange="toggle(\'{r["id"]}\',this)"></td>'
            f'<td style="color:var(--faint);font-size:11.5px">{r["id"]}</td>'
            f'<td><b class="en">{r["item_en"]}</b><div class="si" style="color:var(--muted);font-size:12px">'
            f'{r["item_si"]}</div></td>'
            f'<td style="font-size:12px">{r["authority_or_source"]}</td>'
            f'<td style="font-size:12px">{r["when"]}</td>'
            f'<td class="num" style="font-size:12px">{r["cost_lkr"]}</td>'
            f'<td><span class="pill {pill[r["priority"]]}">{r["priority"]}</span></td></tr>')
    s.append('</tbody></table></div></section>')

    # ================= TIMELINE =================
    s.append('<section id="timeline"><h2><span class="n">11</span>🗓️ <span class="si">කාලසටහන — මාස 14–20</span><span class="en">Timeline — 14 to 20 months</span></h2>'
             '<p class="lead">Critical path: ළිඳ → ජල පරීක්ෂණ → ඉදිකිරීම් → FCAU · <b>Timeline — 14 to 20 months</b></p>')
    s.append('<div class="tl">')
    for mth, work in [
        ("මාස 1–2", "<b>Phase 0–1</b> — ආයෝජක MOU + Shareholders Agreement · සමාගම් ලියාපදිංචිය (eROC) · TIN · බැංකු ගිණුම · ඉඩම් title report · zoning තහවුරු කිරීම"),
        ("මාස 3–4", "<b>Phase 2–3</b> — WRB ලියාපදිංචිය · ළිඳ කැණීම · UDA/ප්‍රා.ස. building permit · architect + structural drawings"),
        ("මාස 5", "<b>🔴 GATE</b> — ළිඳ සම්පූර්ණයි · <b>SLS 614:2013 + bromide + බැර ලෝහ පරීක්ෂණ</b> · මෙය අසමත් වුවහොත් ව්‍යාපෘතිය නවතී"),
        ("මාස 5–6", "<b>Phase 5</b> — යන්ත්‍ර quotation 3ක් · PO/LC නිකුත් (lead time මාස 4–8!)"),
        ("මාස 6–10", "<b>Phase 4</b> — ඉදිකිරීම් · cleanroom · CEB 3-phase · ETP · HACCP/GMP ලේඛන සමාන්තරව"),
        ("මාස 10–11", "Certificate of Conformity · Fire clearance · <b>Trade Licence</b> · CEA EPL application · යන්ත්‍ර පැමිණීම"),
        ("මාස 11–12", "යන්ත්‍ර සවි කිරීම · staff බඳවා ගැනීම + පුහුණුව · Commissioning · trial production"),
        ("මාස 12–13", "<b>Phase 6–7</b> — FCAU අයදුම්පත · <b>SLSI Audit 1</b> · shelf life validation · EPL නිකුත් වේ"),
        ("මාස 13–15", "PHI/MOH/FDI inspections · FCAU site inspection · ලේබල් මුද්‍රණ · distributors"),
        ("මාස 15", "⭐ <b>තාවකාලික FCAU ලියාපදිංචිය (වසර 1)</b> → 🎉 <b>වාණිජ නිෂ්පාදනය ආරම්භයි</b>"),
        ("මාස 16+", "SLS Mark permit · SLSI Audit 2 → වසර 3ක සම්පූර්ණ ලියාපදිංචිය · වෙළඳපොළ වර්ධනය"),
    ]:
        s.append(f'<div class="tl-i"><div class="tl-m">{mth}</div><div class="tl-c">{work}</div></div>')
    s.append('</div>')
    s.append('<div class="note am"><b>⚠️ යන්ත්‍ර lead time:</b> විදේශ සැපයුම්කරුවන්ගෙන් '
             'මාස <b>4–8</b> (නිෂ්පාදනය + නැව් + රේගු). ඇණවුම මාස 6කට පෙර නොකළහොත් '
             'ඉදිකිරීම් ඉවර වී යන්ත්‍ර නැතිව කර්මාන්ත ශාලාව හිස්ව පවතී.</div>')
    s.append('</section>')

    # ================= RISKS =================
    s.append('<section id="risks"><h2><span class="n">12</span>⚠️ <span class="si">ප්‍රධාන අවදානම් 8</span><span class="en">Top eight risks</span></h2>'
             '<p class="lead">ව්‍යාපෘතිය අසාර්ථක කළ හැකි දේ සහ ඒවා වළක්වන ආකාරය · <b>Top 8 risks and how to prevent them</b></p>')
    s.append('<div class="tbl"><table><tr><th style="width:30px">#</th><th>අවදානම</th>'
             '<th class="num">අගය</th><th>වළක්වන ආකාරය</th></tr>')
    for i, (r, sc, mt) in enumerate([
        ("මූලාශ්‍ර ජලය SLS 614 අසමත් වීම", "🔴 9",
         "ඉදිකිරීමට <b>පෙරම</b> ළිඳ කණින්න + පරීක්ෂා කරන්න. ළිං 2ක්. MOU එකේ condition precedent"),
        ("ආයෝජකයා මුදල් ප්‍රමාද කිරීම", "🔴 9",
         "Escrow ගිණුම · milestone tranches + hard deadlines · default clauses"),
        ("SLSI audit 1 අසමත් වීම", "🔴 9",
         "HACCP/GMP උපදේශකයෙකු <b>ඉදිකිරීම් අවධියේදීම</b> · SLSI පුහුණු වැඩසටහන · pre-audit gap analysis"),
        ("Zoning අනුමැතිය නොලැබීම", "🟠 6",
         "ඉඩම මිලදී ගැනීමට/භාවිතයට <b>පෙර</b> ලිඛිත zoning confirmation"),
        ("Ozone + bromide → bromate", "🔴 9",
         "මූලාශ්‍ර ජලයේ <b>bromide පරීක්ෂාව</b> · ozone මාත්‍රාව පාලනය · නිෂ්පාදන bromate පරීක්ෂාව"),
        ("නිෂ්පාදන recall එකක්", "🟠 6",
         "CCP වාර්තා · batch traceability · product liability රක්ෂණය · mock recall පුහුණුව"),
        ("ප්‍රදේශවාසී විරෝධය (ජල නිස්සාරණය)", "🟠 6",
         "මුලින්ම සාකච්ඡා · ප්‍රදේශවාසීන්ට රැකියා · CSR · විනිවිදභාවය"),
        ("Cash flow කඩා වැටීම (retail credit)", "🔴 9",
         "Working capital මාස 6ක් · credit limits · 19L contract sales · cash-on-delivery"),
    ], start=1):
        s.append(f'<tr><td class="num"><b>{i}</b></td><td><b>{r}</b></td>'
                 f'<td class="num">{sc}</td><td>{mt}</td></tr>')
    s.append('</table></div>')
    s.append('<div class="note rd"><b>🔴 මතක තබාගන්න:</b> මෙම ව්‍යාපෘතියේ විශාලතම '
             'තනි අවදානම = <b>ජලය.</b> ළිඳ කණින්න, පරීක්ෂා කරන්න, '
             '<b>SLS 614 සමත් වූ පසුව පමණක්</b> ගොඩනැඟිල්ල ඉදිකිරීම ආරම්භ කරන්න. '
             'නොඑසේ නම් කර්මාන්ත ශාලාවක් තිබී ලියාපදිංචියක් නොලැබේ.</div>')
    s.append('</section>')

    body = "\n".join(s)
    html = (PAGE.replace("__CSS__", CSS).replace("__JS__", JS)
            .replace("__LANG_BOOTSTRAP__", LANGUAGE_BOOTSTRAP)
            .replace("__LANGUAGE_SWITCH__", LANGUAGE_SWITCH)
            .replace("__BODY__", body)
            .replace("__HERO__", hero(M, len(CL), REC))
            .replace("__LOCATION__", M["location"])
            .replace("__INVESTOR__", M["investor"]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        rendered = mark_bilingual_pairs(plain(html))
        rendered = highlight_prompts(fill_empty_table_cells(rendered))
        fh.write(rendered)

    print(f"[ok] wrote {OUT} ({os.path.getsize(OUT)/1024:,.0f} KB)")
    print(f"     checklist items embedded: {len(CL)}")
    for sc in M["scenarios"]:
        print(f"     {sc['name']:<26} total Rs {sc['total_investment']:>12,} | "
              f"investor cash Rs {sc['cash_investment']:>12,}")
    print(f"     ⭐ recommended: {M['recommended']['name']}")
    print(f"     blended cost/bottle: Rs {M['blend_variable']:.2f} "
          f"| contribution Rs {M['blend_contribution']:.2f} ({M['blend_margin_pct']}%)")
    print(f"     break-even: {M['breakeven_pet']:,} bottles/mo ({M['breakeven_pct']*100:.0f}% util)")
    print(f"     payback: Year {M['payback_year']} (+{M['payback_months']} months)")


if __name__ == "__main__":
    build()
