#!/usr/bin/env python3
"""
Render site/dashboard.html from the model in build/dashboard_model.py.
Run:  python3 build/build_dashboard.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_model import build_model, load_checklist  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "dashboard.html")

CSS = """
:root{
  /* ── LIGHT ASH + WHITE (neutral, not green-tinted) ── */
  --bg:#f4f4f5; --bg2:#ebebed; --bg3:#e4e4e7;
  --surface:#ffffff; --surface2:#fafafa;
  --border:#e4e4e7; --border2:#d4d4d8;
  --ink:#18181b; --ink2:#3f3f46; --muted:#71717a; --faint:#a1a1aa;
  /* ── accents: used sparingly, never as page fill ── */
  --emerald:#059669; --emerald-d:#047857; --emerald-l:#ecfdf5;
  --olive:#6b8e23;  --olive-d:#556b1c;  --olive-l:#f4f8ea;
  --amber:#b45309; --amber-l:#fffbeb;
  --red:#dc2626;   --red-l:#fef2f2;
  --blue:#2563eb;  --blue-l:#eff6ff;
  --sh:0 1px 2px rgba(0,0,0,.04), 0 1px 3px rgba(0,0,0,.03);
  --sh2:0 4px 12px rgba(0,0,0,.06);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Noto Sans Sinhala","Nirmala UI","Iskoola Pota",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  line-height:1.65;font-size:15.5px;-webkit-font-smoothing:antialiased}
a{color:var(--emerald-d);text-decoration:none}
a:hover{text-decoration:underline}

/* ── bilingual label: Sinhala primary, English secondary ── */
.bi{display:block}
.bi .en{display:block;font-size:.78em;font-weight:500;color:var(--muted);letter-spacing:.01em;
  margin-top:1px;line-height:1.4}

#wrap{display:flex;min-height:100vh}
#nav{width:270px;flex:0 0 270px;background:var(--surface);border-right:1px solid var(--border);
  position:sticky;top:0;height:100vh;overflow-y:auto;padding:22px 0}
.brand{padding:0 20px 16px;border-bottom:1px solid var(--border);margin-bottom:10px}
.brand .logo{width:40px;height:40px;border-radius:12px;
  background:linear-gradient(135deg,var(--emerald),var(--olive));
  display:flex;align-items:center;justify-content:center;font-size:19px;color:#fff;margin-bottom:11px}
.brand h1{font-size:14.5px;margin:0;line-height:1.4;color:var(--ink)}
.brand p{margin:5px 0 0;font-size:11.5px;color:var(--muted);line-height:1.5}
.nsec{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--faint);
  padding:16px 20px 6px;font-weight:700}
#nav a{display:block;padding:7px 20px;font-size:13px;color:var(--ink2);border-left:3px solid transparent}
#nav a .en{display:block;font-size:10.5px;color:var(--faint);font-weight:500;margin-top:1px}
#nav a:hover{background:var(--surface2);text-decoration:none;color:var(--ink)}
#nav a.on{background:var(--emerald-l);border-left-color:var(--emerald);color:var(--emerald-d);font-weight:600}

#main{flex:1;min-width:0;padding:0 0 100px;max-width:1360px}
.inner{padding:34px 40px 0}

/* ── HERO / COVER ── */
.hero{position:relative;border-radius:0 0 26px 26px;overflow:hidden;
  background:var(--bg3);min-height:340px;display:flex;align-items:flex-end;
  background-size:cover;background-position:center;margin-bottom:30px}
.hero::after{content:"";position:absolute;inset:0;
  background:linear-gradient(to top,rgba(10,14,12,.86) 0%,rgba(10,14,12,.45) 45%,rgba(10,14,12,.12) 100%)}
.hero .hc{position:relative;z-index:2;padding:30px 40px 34px;width:100%;color:#fff}
.hero .kicker{font-size:11px;letter-spacing:2.2px;text-transform:uppercase;font-weight:700;
  color:#a7f3d0;margin-bottom:10px}
.hero h1{font-size:34px;line-height:1.22;margin:0 0 8px;font-weight:750;letter-spacing:-.6px;color:#fff}
.hero .hsub{font-size:15px;color:#e7e9e6;margin:0 0 18px;max-width:760px;line-height:1.6}
.hero .chips{display:flex;flex-wrap:wrap;gap:8px}
.hero .chip{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);
  backdrop-filter:blur(6px);padding:6px 13px;border-radius:99px;font-size:12.5px;font-weight:600;color:#fff}
.hero .chip b{color:#6ee7b7}
.hero .nofallback{position:absolute;inset:0;z-index:1;display:flex;align-items:center;
  justify-content:center;font-size:64px;background:linear-gradient(135deg,#e7e9e6,#d8dbd4)}

header.top{margin-bottom:26px}
header.top h1{font-size:26px;margin:0 0 6px;letter-spacing:-.2px}
header.top .sub{color:var(--muted);font-size:14px}
.badge{display:inline-block;padding:3px 10px;border-radius:99px;font-size:11.5px;font-weight:600;
  background:var(--emerald-l);color:var(--emerald-d);border:1px solid #a7f3d0;margin:2px 4px 2px 0}
.badge.ol{background:var(--olive-l);color:var(--olive-d);border-color:#dde8c4}
.badge.am{background:var(--amber-l);color:var(--amber);border-color:#fde68a}
.badge.rd{background:var(--red-l);color:var(--red);border-color:#fecaca}

section{margin-bottom:46px;scroll-margin-top:20px}
section>h2{font-size:21px;margin:0 0 5px;display:flex;align-items:flex-start;gap:11px;letter-spacing:-.2px}
section>h2 .n{width:27px;height:27px;border-radius:9px;
  background:linear-gradient(135deg,var(--emerald),var(--olive));color:#fff;
  font-size:12.5px;display:inline-flex;align-items:center;justify-content:center;flex:0 0 27px;
  font-weight:700;margin-top:2px}
section>.lead{color:var(--muted);font-size:13.5px;margin:0 0 18px;padding-left:38px}
h3{font-size:15.5px;margin:28px 0 11px;color:var(--emerald-d);
  padding-left:11px;border-left:3px solid var(--emerald)}
h3 .en{font-weight:500;color:var(--muted);font-size:12.5px}

.card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:22px;
  box-shadow:var(--sh)}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
.g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.g4{grid-template-columns:repeat(4,minmax(0,1fr))}
.g5{grid-template-columns:repeat(5,minmax(0,1fr))}

.kpi{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:18px 20px;
  position:relative;overflow:hidden;box-shadow:var(--sh)}
.kpi::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--emerald)}
.kpi.ol::before{background:var(--olive)}
.kpi.am::before{background:var(--amber)}
.kpi.bl::before{background:var(--blue)}
.kpi .l{font-size:11px;color:var(--olive-d);letter-spacing:.3px;font-weight:600;line-height:1.4}
.kpi .v{font-size:25px;font-weight:750;margin:7px 0 3px;letter-spacing:-.7px;color:var(--ink)}
.kpi .v.sm{font-size:19px}
.kpi .h{font-size:11.5px;color:var(--faint);line-height:1.45}
.kpi .v em{font-style:normal;font-size:13px;font-weight:600;color:var(--muted)}

table{border-collapse:collapse;width:100%;font-size:13px;background:var(--surface)}
.tbl{border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--sh)}
.scroll{overflow-x:auto}
th,td{padding:10px 13px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top}
th{background:var(--olive-l);color:var(--olive-d);font-weight:700;font-size:11px;
  text-transform:uppercase;letter-spacing:.5px;white-space:nowrap;
  border-bottom:2px solid #cfe0a8}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:var(--emerald-l)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.tot td{background:var(--olive-l)!important;font-weight:750;color:var(--olive-d);
  border-top:2px solid var(--olive)}
tr.sub td{background:var(--surface2)!important;font-weight:700;color:var(--olive-d)}
tr.land td{background:var(--emerald-l)!important}
tr.grp td{background:linear-gradient(90deg,var(--emerald-l),var(--surface2))!important;
  font-weight:750;color:var(--emerald-d);font-size:12px;text-transform:uppercase;
  letter-spacing:.6px;border-bottom:1px solid #a7f3d0;padding:8px 13px}
tr.grand td{background:linear-gradient(90deg,var(--emerald),var(--olive))!important;
  color:#fff!important;font-weight:800;font-size:14px;border-top:2px solid var(--emerald-d)}
tr.grand td .num,tr.grand td.num{color:#fff!important}
tr.grand.cash td{background:linear-gradient(90deg,var(--olive-d),var(--emerald-d))!important;
  font-size:15px}

.bar{height:8px;border-radius:4px;background:var(--bg3);overflow:hidden;min-width:60px}
.bar>i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--emerald),var(--olive))}
.bar.ol>i{background:var(--olive)}
.bar.am>i{background:var(--amber)}

.bar-chart{display:flex;flex-direction:column;gap:10px}
.bc-row{display:grid;grid-template-columns:200px 1fr 115px;gap:12px;align-items:center;font-size:12.5px}
.bc-row .lbl{color:var(--ink2)}
.bc-row .val{text-align:right;font-variant-numeric:tabular-nums;font-weight:700;color:var(--olive-d)}

.pill{display:inline-block;padding:2px 9px;border-radius:99px;font-size:11px;font-weight:700;white-space:nowrap}
.p-crit{background:var(--red-l);color:var(--red)}
.p-mand{background:var(--amber-l);color:var(--amber)}
.p-high{background:var(--emerald-l);color:var(--emerald-d)}
.p-med{background:var(--blue-l);color:var(--blue)}
.p-low{background:var(--bg2);color:var(--muted)}

.note{background:var(--emerald-l);border:1px solid #a7f3d0;
  border-left:4px solid var(--emerald);padding:13px 17px;
  border-radius:0 12px 12px 0;font-size:13.5px;margin:16px 0;box-shadow:var(--sh)}
.note.ol{background:var(--olive-l);border-color:#dde8c4;border-left-color:var(--olive)}
.note.am{background:var(--amber-l);border-color:#fde68a;border-left-color:var(--amber)}
.note.rd{background:var(--red-l);border-color:#fecaca;border-left-color:var(--red)}
.note b{color:var(--ink)}

.controls{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
input[type=search],select{padding:9px 13px;border:1px solid var(--border2);border-radius:10px;
  background:var(--surface);color:var(--ink);font-size:13px;font-family:inherit}
input[type=search]{flex:1;min-width:200px}
input[type=search]:focus,select:focus{outline:2px solid var(--emerald);outline-offset:-1px}
.chk{width:17px;height:17px;accent-color:var(--emerald);cursor:pointer}
.done td{opacity:.5}
.done td:nth-child(3){text-decoration:line-through}
.hidden{display:none!important}

.flow{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:14px 0}
.flow .st{background:var(--surface);border:1px solid var(--border2);border-radius:11px;
  padding:9px 13px;font-size:12px;font-weight:600;color:var(--ink2);text-align:center;min-width:96px}
.flow .st.key{border-color:var(--emerald);background:var(--emerald-l);color:var(--emerald-d)}
.flow .st.star{border-color:var(--olive);background:var(--olive);color:#fff}
.flow .ar{color:var(--faint);font-weight:700}

.tl{display:flex;flex-direction:column;gap:0;margin-top:14px}
.tl-i{display:grid;grid-template-columns:80px 1fr;gap:16px;padding:12px 0;border-bottom:1px dashed var(--border)}
.tl-i:last-child{border-bottom:none}
.tl-m{font-weight:700;color:var(--emerald-d);font-size:13px;font-variant-numeric:tabular-nums}
.tl-c{font-size:13.5px}
.tl-c b{color:var(--ink)}
.tl-c .t{color:var(--muted);font-size:12.5px}

footer{margin-top:50px;padding-top:20px;border-top:1px solid var(--border);
  color:var(--faint);font-size:12px}

@media(max-width:1080px){#wrap{flex-direction:column}#nav{width:100%;flex:none;height:auto;
  position:static;border-right:none;border-bottom:1px solid var(--border)}
  .inner{padding:24px 20px 0}#main{padding-bottom:70px}
  .g4,.g5{grid-template-columns:repeat(2,minmax(0,1fr))}
  .hero h1{font-size:26px}.hero .hc{padding:24px 20px 26px}}
@media(max-width:620px){.g2,.g3,.g4,.g5{grid-template-columns:1fr}
  .bc-row{grid-template-columns:120px 1fr 84px}.hero{min-height:290px}}
@media print{#nav{display:none}#main{max-width:100%}
  body{background:#fff}.kpi,.card,.tbl{box-shadow:none}.hero{display:none}}
"""

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
  const c=document.getElementById('count'); if(c) c.textContent=shown+' අයිතම දැක්වේ';
}
function resetAll(){
  if(!confirm('සියලු ලකුණු ඉවත් කරන්නද? / Clear all ticks?'))return;
  state={};save();
  document.querySelectorAll('tr[data-id]').forEach(tr=>{tr.classList.remove('done');
    const cb=tr.querySelector('.chk'); if(cb)cb.checked=false;});
  updateProgress();
}
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

PAGE = """<!doctype html>
<html lang="si"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>💧 බෝතල් ජල කර්මාන්ත ශාලාව — ව්‍යාපෘති Dashboard | Bandarawela Bottled Water Plant</title>
<style>__CSS__</style>
</head><body>
<div id="wrap">
<nav id="nav">
  <div class="brand">
    <div class="logo">💧</div>
    <h1>බෝතල් ජල කර්මාන්ත ශාලාව
      <span style="display:block;font-size:11.5px;font-weight:500;color:var(--muted);margin-top:3px">Bottled Drinking Water Plant</span></h1>
    <p>__LOCATION__<br><b>ආයෝජක / Investor:<br>__INVESTOR__</b></p>
  </div>
  <div class="nsec">දළ විශ්ලේෂණය / Overview</div>
  <a href="#dash">📊 සාරාංශය<span class="en">Summary &amp; the 5 products</span></a>
  <a href="#project">🏭 ව්‍යාපෘතිය<span class="en">What exists today</span></a>
  <a href="#process">💧 පිරිපහදු ක්‍රියාවලිය<span class="en">Treatment train</span></a>
  <a href="#production">📦 නිෂ්පාදන 5<span class="en">Bottle quantities</span></a>
  <div class="nsec">පිරිවැය / The cost</div>
  <a href="#stage1">💰 අදියර 1 — ෆැක්ටරි ඕපන්<span class="en">Day one to open factory</span></a>
  <a href="#stage2">🏭 අදියර 2 — නිෂ්පාදනයට<span class="en">Open factory to manufacturing</span></a>
  <a href="#total">🧾 මුළු ආයෝජනය<span class="en">Everything added up</span></a>
  <a href="#unitcost">🧮 බෝතලයක පිරිවැය<span class="en">Cost per bottle, all 5</span></a>
  <a href="#materials">🏷️ අමුද්‍රව්‍ය + ලේබල්<span class="en">What to buy monthly</span></a>
  <div class="nsec">ක්‍රියාත්මක කිරීම / Execution</div>
  <a href="#checklist">✅ ලේඛන ලැයිස්තුව<span class="en">160-item checklist</span></a>
  <a href="#timeline">🗓️ කාලසටහන<span class="en">Timeline</span></a>
  <a href="#risks">⚠️ අවදානම්<span class="en">Top risks</span></a>
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


def kpi(label, value, hint="", cls=""):
    return (f'<div class="kpi {cls}"><div class="l">{label}</div>'
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


ASSET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "assets", "cover.jpg")


def hero(M, n_items, rec):
    """Full-width upcountry cover. Embeds assets/cover.jpg as base64 so the
    dashboard stays a single self-contained file; degrades gracefully."""
    style, art = "", '<div class="nofallback">💧🏔️</div>'
    if os.path.exists(ASSET):
        with open(ASSET, "rb") as fh:
            import base64
            b64 = base64.b64encode(fh.read()).decode("ascii")
        style = f'background-image:url("data:image/jpeg;base64,{b64}")'
        art = ""  # the fallback tile must NOT render over the real photo
    return f"""<div class="hero" style="{style}">
  {art}
  <div class="hc">
    <div class="kicker">බණ්ඩාරවෙල · ඌව කඳුකරය &nbsp;·&nbsp; Bandarawela, Uva Highlands</div>
    <h1>කඳුකර නියම ජලයෙන් බෝතල් කරන ලද පානීය ජලය<br>
      <span style="font-size:19px;font-weight:600;color:#cbd5ce">
      Bottled Drinking Water from the Uva Highlands</span></h1>
    <p class="hsub">
      Mr. {M["investor"]} ආයෝජනය කරන, {M["location"]} හි පිහිටි,
      {M["capacity_bph"]:,} BPH ධාරිතාවේ සම්පූර්ණ RO + UV + Ozone පිරිපහදු කර්මාන්ත ශාලාවක්.<br>
      A {M["capacity_bph"]:,} BPH plant at {M["location"]}, funded by Mr. {M["investor"]}.
      Currently only the land exists — building, plant and every approval start from scratch.
    </p>
    <div class="chips">
      <span class="chip">🏞️ ඉඩම ඇත / <b>Land owned</b></span>
      <span class="chip">🏗️ ගොඩනැඟිල්ල + යන්ත්‍ර = මුල සිට / <b>From scratch</b></span>
      <span class="chip">💰 ආයෝජනය / <b>Rs {rec["total_investment"]/1e6:,.1f}M</b></span>
      <span class="chip">🧾 බෝතලයක ලාභය / <b>Rs {M["blend_contribution"]:.2f}</b></span>
      <span class="chip">📄 ලේඛන / <b>{n_items} items</b></span>
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
    s.append('<section id="dash"><h2><span class="n">1</span>📊 සාරාංශය — එක බැල්මකින්</h2>'
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

    s.append('<h3>🍶 නිෂ්පාදන 5ක් — වෙන වෙනම <span class="en">The five products, separately</span></h3>')
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
    s.append('<section id="project"><h2><span class="n">2</span>🏭 ව්‍යාපෘතිය — දැන් තිබෙන්නේ මොනවාද?</h2>'
             '<p class="lead">දැනට ඇති දේ සහ මුල සිට ගොඩනැගිය යුතු දේ · <b>What exists today vs. what must be built from scratch</b></p>')
    s.append('<div class="grid g2">')
    s.append('<div class="card"><h3 style="margin-top:0">✅ දැනට තිබෙන දේ / What exists today</h3>'
             '<div class="tbl"><table>'
             '<tr><th>අයිතමය</th><th>තත්ත්වය</th></tr>'
             f'<tr class="land"><td><b>ඉඩම</b> — {M["location"]}</td>'
             f'<td><span class="pill p-high">✓ ඇත</span> — {M["investor"]} සතු</td></tr>'
             '<tr><td>ආයෝජකයා</td><td><span class="pill p-high">✓ සිටී</span> — '
             f'{M["investor"]}</td></tr>'
             '<tr><td>ව්‍යාපාර සංකල්පය</td><td><span class="pill p-high">✓ පැහැදිලියි</span></td></tr>'
             '</table></div>'
             '<div class="note rd" style="margin-bottom:0"><b>⚠️ තහවුරු කළ යුතුයි:</b> '
             'ඉඩම <b>පර්චස් 160+</b> ද? කර්මාන්ත භාවිතයට <b>zoning අවසර</b> තිබේද? '
             'ඉඩම සමාගමට <b>හරවා දෙන්නේද / බදු දෙන්නේද?</b> — FCAU ලියාපදිංචියට මෙය අත්‍යවශ්‍යයි.</div>'
             '</div>')
    s.append('<div class="card"><h3 style="margin-top:0">🏗️ මුල සිට කළ යුතු දේ / To be built from scratch</h3>'
             '<div class="tbl"><table><tr><th>කොටස</th><th class="num">පිරිවැය (Rs)</th></tr>')
    cats = {}
    for name, qty, unit, rate, amt, cat, inkind, stg in M["capex"]:
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
    s.append('<section id="process"><h2><span class="n">3</span>💧 පිරිපහදු ක්‍රියාවලිය — filtration දාමය</h2>'
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
    s.append('<section id="production"><h2><span class="n">4</span>📦 නිෂ්පාදන පරිමාව — බෝතල් Qty</h2>'
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
    # ============ 5 + 6. STAGE 1 and STAGE 2 BUDGETS ============
    CAT_LBL = {"land": "🏞️ ඉඩම / Land",
               "building": "🏢 ගොඩනැඟිලි / Building & civil",
               "plant": "⚙️ යන්ත්‍රෝපකරණ / Plant & machinery",
               "utility": "⚡ උපයෝගිතා / Utilities",
               "env": "🌿 පරිසර + ආරක්ෂාව / Environment & safety",
               "logistics": "🚚 ප්‍රවාහන / Logistics",
               "pre": "📄 ලියාපදිංචි + උපදේශන / Registration & consultancy"}
    CAT_ORDER = ["land", "building", "plant", "utility", "env", "logistics", "pre"]

    def stage_block(num, stage, anchor, rows, stage_total, extra_note):
        si, en = M["stage_titles"][stage]
        out = [f'<section id="{anchor}"><h2><span class="n">{num}</span>'
               f'💰 {si}</h2><p class="lead">{en}</p>']
        out.append('<div class="tbl scroll"><table><thead><tr>'
                   '<th style="width:34px">#</th><th>අයිතමය / Item</th>'
                   '<th class="num">Qty</th><th>ඒකකය / Unit</th>'
                   '<th class="num">ඒකක මිල / Rate (Rs)</th>'
                   '<th class="num">මුදල / Amount (Rs)</th></tr></thead><tbody>')
        n = 0
        for ckey in CAT_ORDER:
            sel = [r for r in rows if r[5] == ckey]
            if not sel:
                continue
            out.append(f'<tr class="grp"><td colspan="6">{CAT_LBL[ckey]}</td></tr>')
            for name, qty, unit, rate, amt, cat, inkind, stg in sel:
                n += 1
                cls = ' class="land"' if inkind else ''
                tag = ' <span class="pill p-high">ආයෝජකයාගේ / in-kind</span>' if inkind else ''
                out.append(f'<tr{cls}><td class="num">{n}</td><td>{name}{tag}</td>'
                           f'<td class="num">{qty:,}</td><td>{unit}</td>'
                           f'<td class="num">{rate:,.0f}</td>'
                           f'<td class="num"><b>{amt:,}</b></td></tr>')
            out.append(f'<tr class="sub"><td></td><td>උප මුළු / Subtotal</td>'
                       f'<td class="num"></td><td></td><td class="num"></td>'
                       f'<td class="num">{sum(r[4] for r in sel):,}</td></tr>')
        out.append(f'<tr class="grand"><td></td><td>🔵 අදියර {stage} මුළු පිරිවැය / '
                   f'STAGE {stage} TOTAL ({n} අයිතම්)</td><td class="num"></td><td></td>'
                   f'<td class="num"></td><td class="num">{stage_total:,}</td></tr>')
        cash = sum(r[4] for r in rows if not r[6])
        out.append(f'<tr class="grand cash"><td></td><td>💵 මුදලින් ගෙවිය යුතු / '
                   f'CASH OUT (ඉඩම හැර / excl. land)</td><td class="num"></td><td></td>'
                   f'<td class="num"></td><td class="num">{cash:,}</td></tr>')
        out.append('</tbody></table></div>')
        out.append(extra_note)
        out.append('</section>')
        return out

    s += stage_block(
        5, 1, "stage1", M["stage1_rows"], M["stage1_total"],
        '<div class="note ol"><b>🏁 අදියර 1 අවසන් වන්නේ:</b> ගොඩනැඟිල්ල සම්පූර්ණයි, '
        'විදුලිය සම්බන්ධයි, ළිඳ කැණී ජල පරීක්ෂණ සමත් වී ඇත, ETP සහ ගිනි ආරක්ෂාව '
        'සූදානම්, CEA EPL ලැබී ඇත. <b>නමුත් තවම නිෂ්පාදනය කළ නොහැක</b> — '
        'යන්ත්‍ර නැත.<br><b>Stage 1 ends when</b> the building is complete, power is on, '
        'the well is drilled and has passed SLS 614, and the ETP and fire systems are in. '
        'You still cannot manufacture — there is no machinery yet.</div>')

    s += stage_block(
        6, 2, "stage2", M["stage2_rows"], M["stage2_total"],
        '<div class="note"><b>🏭 අදියර 2 අවසන් වන්නේ:</b> සම්පූර්ණ පිරිපහදු දාමය සවි කර '
        'ඇත, filling monoblock සහ 19L රේඛාව ක්‍රියාත්මකයි, QC lab සූදානම්, '
        'FCAU + SLSI ලියාපදිංචිය ලැබී ඇත → <b>නිෂ්පාදනය ආරම්භ කළ හැක.</b> '
        '<b>මෙතනින් ඔබ්බට මෙම dashboard එක යන්නේ නැත.</b>'
        '<br><b>Stage 2 ends when</b> the treatment train and filling lines run, the QC lab '
        'is equipped and FCAU + SLSI registration is granted — manufacturing can start. '
        'This dashboard stops here.</div>')

    # ---- the combined roll-up ----
    s.append('<section id="total"><h2><span class="n">7</span>🧾 මුළු ආයෝජනය — එක තැනක</h2>'
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
    s.append('<section id="unitcost"><h2><span class="n">8</span>🧮 එක බෝතලයක පිරිවැය — '
             'නිෂ්පාදන 5ම වෙන වෙනම</h2>'
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
    # ============ 9. MATERIALS AND LABELS ============
    s.append('<section id="materials"><h2><span class="n">9</span>🏷️ අමුද්‍රව්‍ය සහ ලේබල් Qty</h2>'
             '<p class="lead">නිෂ්පාදන 5ම — මිලදී ගත යුතු ප්‍රමාණය wastage සහිතව · '
             '<b>What to buy each month for all five products, wastage included</b></p>')
    s.append('<div class="tbl scroll"><table><thead><tr>'
             '<th>නිෂ්පාදනය / Product</th><th class="num">බෝතල්/මාස</th>'
             '<th class="num">× 1.03</th><th class="num">මූඩි / Caps</th>'
             '<th class="num">ලේබල් / Labels × 1.04</th>'
             '<th class="num">Shrink film × 1.05</th></tr></thead><tbody>')
    t = [0, 0, 0, 0, 0]
    for sk in M["skus"]:
        base = round(M["nameplate_month"] * sk["share"])
        b = round(base * sk["bottle_qty_factor"])
        cp = round(base * sk["cap_qty_factor"])
        lb = round(base * sk["label_qty_factor"])
        fm = round(base * sk["film_qty_factor"])
        for i, v in enumerate((base, b, cp, lb, fm)):
            t[i] += v
        s.append(f'<tr><td><b>💧 {sk["sku"]}</b></td><td class="num">{base:,}</td>'
                 f'<td class="num">{b:,}</td><td class="num">{cp:,}</td>'
                 f'<td class="num">{lb:,}</td><td class="num">{fm:,}</td></tr>')
    s.append(f'<tr class="land"><td><b>🫙 19 L (returnable)</b></td>'
             f'<td class="num">80,000</td><td class="num">—</td>'
             f'<td class="num">82,400</td><td class="num">83,200</td>'
             f'<td class="num">—</td></tr>')
    s.append(f'<tr class="grand"><td>මුළු / TOTAL (100% ධාරිතාව)</td>'
             f'<td class="num">{t[0]:,}</td><td class="num">{t[1]:,}</td>'
             f'<td class="num">{t[2]:,}</td><td class="num">{t[3]:,}</td>'
             f'<td class="num">{t[4]:,}</td></tr>')
    s.append('</tbody></table></div>')
    s.append('<div class="note ol"><b>📌 Wastage නීති:</b> බෝතල් <b>× 1.03</b> (3%) · '
             'මූඩි <b>× 1.03</b> (3%) · ලේබල් <b>× 1.04</b> (4% — මුද්‍රණ වැරදි, '
             'යන්ත්‍ර waste, changeovers) · shrink film <b>× 1.05</b> (5%). '
             '<br><b>🎨 ලේබල් නිර්මාණ 5ක් අවශ්‍යයි</b> — එක් නිෂ්පාදනයකට එක බැගින්. '
             'සෑම ලේබලයක්ම <b>FCAU අනුමත</b> විය යුතුය.</div>')
    s.append('</section>')
    # ================= CHECKLIST =================
    s.append('<section id="checklist"><h2><span class="n">10</span>✅ ලේඛන සහ අවශ්‍යතා ලැයිස්තුව <span class="en" style="font-size:13px;font-weight:600;color:var(--muted)">Documents &amp; requirements</span></h2>'
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
            f'<td><b>{r["item_en"]}</b><div style="color:var(--muted);font-size:12px">'
            f'{r["item_si"]}</div></td>'
            f'<td style="font-size:12px">{r["authority_or_source"]}</td>'
            f'<td style="font-size:12px">{r["when"]}</td>'
            f'<td class="num" style="font-size:12px">{r["cost_lkr"]}</td>'
            f'<td><span class="pill {pill[r["priority"]]}">{r["priority"]}</span></td></tr>')
    s.append('</tbody></table></div></section>')

    # ================= TIMELINE =================
    s.append('<section id="timeline"><h2><span class="n">11</span>🗓️ කාලසටහන — මාස 14–20</h2>'
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
    s.append('<section id="risks"><h2><span class="n">12</span>⚠️ ප්‍රධාන අවදානම් 8</h2>'
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
            .replace("__BODY__", body)
            .replace("__HERO__", hero(M, len(CL), REC))
            .replace("__LOCATION__", M["location"])
            .replace("__INVESTOR__", M["investor"]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)

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
