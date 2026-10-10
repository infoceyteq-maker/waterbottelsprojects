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
section>h2 .n{width:27px;height:27px;border-radius:9px;background:var(--ink);color:#fff;
  font-size:12.5px;display:inline-flex;align-items:center;justify-content:center;flex:0 0 27px;
  font-weight:700;margin-top:2px}
section>.lead{color:var(--muted);font-size:13.5px;margin:0 0 18px;padding-left:38px}
h3{font-size:15.5px;margin:28px 0 11px;color:var(--ink)}
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
.kpi::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--emerald)}
.kpi.ol::before{background:var(--olive)}
.kpi.am::before{background:var(--amber)}
.kpi.bl::before{background:var(--blue)}
.kpi .l{font-size:11px;color:var(--muted);letter-spacing:.3px;font-weight:600;line-height:1.4}
.kpi .v{font-size:25px;font-weight:750;margin:7px 0 3px;letter-spacing:-.7px;color:var(--ink)}
.kpi .v.sm{font-size:19px}
.kpi .h{font-size:11.5px;color:var(--faint);line-height:1.45}
.kpi .v em{font-style:normal;font-size:13px;font-weight:600;color:var(--muted)}

table{border-collapse:collapse;width:100%;font-size:13px;background:var(--surface)}
.tbl{border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--sh)}
.scroll{overflow-x:auto}
th,td{padding:10px 13px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top}
th{background:var(--surface2);color:var(--muted);font-weight:700;font-size:11px;
  text-transform:uppercase;letter-spacing:.5px;white-space:nowrap;
  border-bottom:1px solid var(--border2)}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:var(--surface2)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.tot td{background:var(--bg2)!important;font-weight:750;color:var(--ink);
  border-top:2px solid var(--ink2)}
tr.sub td{background:var(--surface2)!important;font-weight:700}
tr.land td{background:var(--emerald-l)!important}

.bar{height:8px;border-radius:4px;background:var(--bg3);overflow:hidden;min-width:60px}
.bar>i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--emerald),var(--olive))}
.bar.ol>i{background:var(--olive)}
.bar.am>i{background:var(--amber)}

.bar-chart{display:flex;flex-direction:column;gap:10px}
.bc-row{display:grid;grid-template-columns:200px 1fr 115px;gap:12px;align-items:center;font-size:12.5px}
.bc-row .lbl{color:var(--ink2)}
.bc-row .val{text-align:right;font-variant-numeric:tabular-nums;font-weight:650;color:var(--ink)}

.pill{display:inline-block;padding:2px 9px;border-radius:99px;font-size:11px;font-weight:700;white-space:nowrap}
.p-crit{background:var(--red-l);color:var(--red)}
.p-mand{background:var(--amber-l);color:var(--amber)}
.p-high{background:var(--emerald-l);color:var(--emerald-d)}
.p-med{background:var(--blue-l);color:var(--blue)}
.p-low{background:var(--bg2);color:var(--muted)}

.note{border-left:3px solid var(--emerald);background:var(--surface);border:1px solid var(--border);
  border-left:3px solid var(--emerald);padding:13px 17px;
  border-radius:0 12px 12px 0;font-size:13.5px;margin:16px 0;box-shadow:var(--sh)}
.note.ol{border-left-color:var(--olive)}
.note.am{border-left-color:var(--amber)}
.note.rd{border-left-color:var(--red)}
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
.tl-m{font-weight:700;color:var(--ink);font-size:13px;font-variant-numeric:tabular-nums}
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
  <a href="#dash">📊 Dashboard<span class="en">At a glance</span></a>
  <a href="#project">🏭 ව්‍යාපෘතිය<span class="en">What exists today</span></a>
  <a href="#process">💧 පිරිපහදු ක්‍රියාවලිය<span class="en">Treatment train</span></a>
  <div class="nsec">මුදල් / Money</div>
  <a href="#production">📦 නිෂ්පාදන පරිමාව<span class="en">Bottle quantities</span></a>
  <a href="#materials">🏷️ අමුද්‍රව්‍ය + ලේබල්<span class="en">Material &amp; label qty</span></a>
  <a href="#budget">💰 සම්පූර්ණ අයවැය<span class="en">Full budget</span></a>
  <a href="#unitcost">🧮 බෝතලයක පිරිවැය<span class="en">Cost per bottle</span></a>
  <a href="#profit">📈 ලාභය + Break-even<span class="en">Profit & break-even</span></a>
  <a href="#growth">🚀 වර්ධන සැලැස්ම<span class="en">Expansion plan</span></a>
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

    # ================= DASHBOARD =================
    s = []
    # (hero cover replaces the old text header)

    s.append('<section id="dash"><h2><span class="n">1</span>📊 Dashboard — එක බැල්මකින්</h2>'
             '<p class="lead">සම්පූර්ණ ව්‍යාපෘතියේ ප්‍රධාන සංඛ්‍යා · <b>The whole project at a glance</b></p>')
    s.append('<div class="grid g4">')
    s.append(kpi("ධාරිතාව / Capacity", f'{M["capacity_bph"]:,} <em>BPH</em>',
                 f'{M["shift_hours"]}h × {M["work_days"]}d = {M["nameplate_month"]:,} බෝතල්/මාස (100%)'))
    s.append(kpi("මුළු ආයෝජනය / Total Investment", "Rs " + m(REC["total_investment"]),
                 "⭐ Option A (Lean Start) · CAPEX + working capital", "ol"))
    s.append(kpi("Mr. Thilakarathna ගේ මුදල්", "Rs " + m(REC["cash_investment"]),
                 f'Option A · ඉඩම් වටිනාකම Rs {m(M["land_value"])} අඩු කිරීමෙන් පසු', "am"))
    s.append(kpi("බෝතලයක පිරිවැය (blended)", f'Rs {M["blend_variable"]:,.2f}',
                 "PET බෝතලයක සාමාන්‍ය variable cost", "bl"))
    s.append('</div>')
    s.append('<div class="grid g4" style="margin-top:14px">')
    s.append(kpi("බෝතලයක ලාභය (blended)", f'Rs {M["blend_contribution"]:,.2f}',
                 f'Margin {M["blend_margin_pct"]}% · ex-factory Rs {M["blend_price"]:,.0f}'))
    s.append(kpi("Break-even", f'{M["breakeven_pct"]*100:,.0f}<em>%</em>',
                 f'බෝතල් {M["breakeven_pet"]:,}/මාස — ඉතා ආරක්ෂිතයි', "ol"))
    s.append(kpi("Year 1 ශුද්ධ ලාභය", "Rs " + m(y1["pat_y"]),
                 f'25% utilisation (පරික්ෂාකාරී) · Revenue Rs {m(y1["revenue_y"])}/yr'))
    s.append(kpi("Payback", f'{M["payback_year"]} <em>වසර</em>',
                 f'Year {M["payback_year"]} මාස {M["payback_months"]} දී ආයෝජනය ආපසු', "ol"))
    s.append('</div>')

    s.append('<div class="card" style="margin-top:16px"><h3 style="margin-top:0">'
             '📅 වසර 3ක ප්‍රක්ෂේපණය / 3-Year Projection</h3><div class="scroll"><table>'
             '<tr><th>වසර</th><th class="num">Utilisation</th><th class="num">බෝතල්/මාස</th>'
             '<th class="num">ආදායම/වසර</th><th class="num">Contribution/මාස</th>'
             '<th class="num">Fixed/මාස</th><th class="num">ශුද්ධ ලාභය/වසර</th></tr>')
    for p in M["projection"]:
        s.append(f'<tr><td><b>{p["year"]}</b></td><td class="num">{p["utilisation"]*100:,.0f}%</td>'
                 f'<td class="num">{p["pet_bottles_m"]:,}</td>'
                 f'<td class="num">Rs {m(p["revenue_y"])}</td>'
                 f'<td class="num">Rs {m(p["contribution_m"])}</td>'
                 f'<td class="num">Rs {m(p["fixed_m"])}</td>'
                 f'<td class="num"><b>Rs {m(p["pat_y"])}</b></td></tr>')
    s.append('</table></div></div></section>')

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
    for name, amt, cat, inkind in M["capex"]:
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

    # ================= PRODUCTION =================
    s.append('<section id="production"><h2><span class="n">4</span>📦 නිෂ්පාදන පරිමාව — බෝතල් Qty</h2>'
             '<p class="lead">SKU mix අනුව මාසික බෝතල් ප්‍රමාණය · <b>Production volumes — monthly bottle quantities by SKU</b></p>')
    s.append('<div class="grid g3">')
    s.append(kpi("Nameplate (100%, 1 shift)", f'{M["nameplate_month"]:,}',
                 f'{M["capacity_bph"]:,} BPH × {M["shift_hours"]}h × {M["work_days"]}d'))
    s.append(kpi("Year 1 (40%)", f'{y1["pet_bottles_m"]:,}',
                 f'බෝතල්/මාස · {y1["pet_bottles_y"]:,}/වසර', "ol"))
    s.append(kpi("Year 2 (50%)", f'{y2["pet_bottles_m"]:,}',
                 f'බෝතල්/මාස · {y2["pet_bottles_y"]:,}/වසර', "ol"))
    s.append(kpi("Year 4 (100%)", f'{y4["pet_bottles_m"]:,}',
                 f'බෝතල්/මාස · {y4["pet_bottles_y"]:,}/වසර', "ol"))
    s.append('</div>')

    s.append('<h3>🍶 SKU mix — PET රේඛාව</h3><div class="tbl"><table>'
             '<tr><th>බෝතලය</th><th class="num">Mix</th><th class="num">Y1 බෝතල්/මාස</th>'
             '<th class="num">Y2 බෝතල්/මාස</th><th class="num">Y3 බෝතල්/මාස</th>'
             '<th class="num">Y4 බෝතල්/මාස</th><th class="num">ලීටර්/මාස (Y1)</th></tr>')
    for sk in M["skus"]:
        s.append(f'<tr><td><b>{sk["sku"]}</b></td><td class="num">{sk["share"]*100:.0f}%</td>'
                 f'<td class="num">{round(y1["pet_bottles_m"]*sk["share"]):,}</td>'
                 f'<td class="num">{round(y2["pet_bottles_m"]*sk["share"]):,}</td>'
                 f'<td class="num">{round(y3["pet_bottles_m"]*sk["share"]):,}</td>'
                 f'<td class="num">{round(y4["pet_bottles_m"]*sk["share"]):,}</td>'
                 f'<td class="num">{round(y1["pet_bottles_m"]*sk["share"]*sk["volume_l"]):,}</td></tr>')
    tot_l = sum(y1["pet_bottles_m"] * sk["share"] * sk["volume_l"] for sk in M["skus"])
    s.append(f'<tr class="tot"><td>මුළු PET</td><td class="num">100%</td>'
             f'<td class="num">{y1["pet_bottles_m"]:,}</td><td class="num">{y2["pet_bottles_m"]:,}</td>'
             f'<td class="num">{y3["pet_bottles_m"]:,}</td><td class="num">{y4["pet_bottles_m"]:,}</td>'
             f'<td class="num">{round(tot_l):,} L</td></tr>')
    s.append(f'<tr class="land"><td><b>19 L (returnable)</b></td><td class="num">වෙනම රේඛාව</td>'
             f'<td class="num">{y1["v19_m"]:,}</td><td class="num">{y2["v19_m"]:,}</td>'
             f'<td class="num">{y3["v19_m"]:,}</td><td class="num">{y4["v19_m"]:,}</td>'
             f'<td class="num">{y1["v19_m"]*19:,} L</td></tr>')
    s.append('</table></div>')

    s.append('<div class="note"><b>⭐ 19 L රේඛාව ඇයි වැදගත්:</b> බෝතලය වරක් මිලදී ගෙන '
             'වසර 3–5ක් නැවත භාවිත කරයි → ඇසුරුම් පිරිවැය ඉතා අඩුයි. '
             f'Gross margin <b>{M["sku19"]["margin_pct"]:.0f}%</b> '
             f'(PET වල {M["blend_margin_pct"]:.0f}% ට එරෙහිව). '
             'උඩරට හෝටල්, නිවාඩු නිකේතන, කාර්යාල, රෝහල් සඳහා ඉල්ලුම වැඩියි.</div>')
    s.append('</section>')

    # ================= MATERIALS =================
    s.append('<section id="materials"><h2><span class="n">5</span>🏷️ අමුද්‍රව්‍ය සහ ලේබල් Qty</h2>'
             '<p class="lead">සෑම මාසයකම මිලදී ගත යුතු ප්‍රමාණය (wastage සහිතව) · <b>Raw material &amp; label quantities to buy each month</b></p>')
    s.append('<h3>PET රේඛාව — මාසික අවශ්‍යතා</h3>')
    for label, yr in [("Year 1 (40%)", y1), ("Year 2 (70%)", y2), ("Year 3 (100%)", y3)]:
        s.append(f'<h3 style="font-size:13.5px;color:var(--muted)">{label} — '
                 f'බෝතල් {yr["pet_bottles_m"]:,}</h3>')
        s.append('<div class="tbl"><table><tr><th>අමුද්‍රව්‍යය</th><th class="num">500 ml</th>'
                 '<th class="num">1 L</th><th class="num">1.5 L</th><th class="num">මුළු</th></tr>')
        rows = [("බෝතල් (PET, SLS 1336)", "bottle_qty_factor"),
                ("මූඩි / Caps", "cap_qty_factor"),
                ("ලේබල් / Shrink sleeves", "label_qty_factor")]
        for nm, key in rows:
            tot = 0
            cells = []
            for sk in M["skus"]:
                q = round(yr["pet_bottles_m"] * sk["share"] * sk[key])
                cells.append(q)
                tot += q
            s.append(f'<tr><td><b>{nm}</b></td>' +
                     "".join(f'<td class="num">{c:,}</td>' for c in cells) +
                     f'<td class="num"><b>{tot:,}</b></td></tr>')
        film = round(yr["pet_bottles_m"] * 1.05)
        s.append(f'<tr><td>Shrink film / multipack ඒකක</td>'
                 f'<td class="num" colspan="3">මුළු බෝතල් × 1.05</td>'
                 f'<td class="num">{film:,}</td></tr>')
        s.append(f'<tr><td>Pallets (60 බෝතල්/pallet)</td>'
                 f'<td class="num" colspan="3">—</td>'
                 f'<td class="num">{round(yr["pet_bottles_m"]/60):,}</td></tr>')
        s.append('</table></div>')

    s.append('<div class="note ol"><b>📌 ලේබල් ගණනය කිරීමේ නීතිය:</b> '
             'ලේබල් 1ක් = බෝතල් 1ක්. නමුත් මුද්‍රණ වැරදි, යන්ත්‍ර waste, '
             'label changeovers නිසා <b>4% wastage</b> එක් කරන්න. '
             'Caps සහ බෝතල් සඳහා <b>3%</b>. '
             '<b>SKU එකකට වෙනම ලේබලයක්</b> — එබැවින් SKU 3ක් = ලේබල් නිර්මාණ 3ක් '
             '(+ 19L tag = 4ක්). '
             'සෑම ලේබලයක්ම FCAU අනුමත විය යුතුය.</div>')

    s.append('<h3>19 L රේඛාව — මාසික</h3><div class="tbl"><table>'
             '<tr><th>අමුද්‍රව්‍යය</th><th class="num">Y1</th><th class="num">Y2</th>'
             '<th class="num">Y3</th></tr>')
    for nm, f in [("19 L බෝතල් (ආරම්භක තොගය — returnable)", 1.15),
                  ("Caps (returnable)", 1.10),
                  ("Handle tags / ලේබල්", 1.05)]:
        s.append(f'<tr><td>{nm}</td>' +
                 "".join(f'<td class="num">{round(y["v19_m"]*f):,}</td>' for y in M["projection"]) +
                 '</tr>')
    s.append('</table></div>')
    s.append('<div class="note am"><b>⚠️ 19 L බෝතල් = ආයෝජනයක්, පිරිවැයක් නොවේ.</b> '
             'බෝතලයක් ~Rs 1,200; එය වාර 40ක් භාවිත කරයි → භාරය Rs 30/බෝතල්. '
             'නමුත් ආරම්භක තොගය (Y1: '
             f'{round(y1["v19_m"]*1.15):,} බෝතල් × Rs 1,200 = '
             f'Rs {y1["v19_m"]*1.15*1200/1_000_000:,.1f}M) CAPEX එකේ ඇතුළත් විය යුතුය.</div>')
    s.append('</section>')

    # ================= BUDGET =================
    s.append('<section id="budget"><h2><span class="n">6</span>💰 සම්පූර්ණ අයවැය — නිෂ්පාදනය ආරම්භ කරන තෙක්</h2>'
             '<p class="lead">නිෂ්පාදනය ආරම්භ කරන තෙක් සියලු විස්තර · <b>Full budget to the point of manufacturing — every line item</b></p>')
    s.append('<div class="grid g4">')
    s.append(kpi("ඉදිකිරීම් + යන්ත්‍ර", "Rs " + m(cats["building"] + cats["plant"] + cats["utility"]
                                                  + cats["env"] + cats["logistics"]),
                 "ගොඩනැඟිල්ල, plant, utilities, වාහන"))
    s.append(kpi("ලියාපදිංචි + උපදේශන", "Rs " + m(cats["pre"]),
                 "සමාගම්, WRB, FCAU, SLSI, CEA, branding", "ol"))
    s.append(kpi("Contingency (15%)", "Rs " + m(M["contingency"]),
                 "ඉදිකිරීම් වියදම් ඉහළ යාම සඳහා", "am"))
    s.append(kpi("Working capital (මාස 3)", "Rs " + m(M["working_capital"]),
                 "බෝතල්, ලේබල්, වැටුප්, විදුලිය", "bl"))
    s.append('</div>')

    s.append('<h3>📋 සම්පූර්ණ CAPEX ලැයිස්තුව</h3><div class="tbl scroll"><table>'
             '<tr><th>අයිතමය</th><th class="num">පිරිවැය (LKR)</th><th class="num">%</th></tr>')
    for name, amt, cat, inkind in M["capex"]:
        cls = ' class="land"' if inkind else ''
        tag = ' <span class="pill p-high">ඉඩම — ආයෝජකයාගේ</span>' if inkind else ''
        pct = amt / M["total_capex"] * 100
        s.append(f'<tr{cls}><td>{name}{tag}</td><td class="num">{amt:,}</td>'
                 f'<td class="num">{pct:.1f}%</td></tr>')
    s.append(f'<tr class="sub"><td>උප මුළු / Subtotal</td>'
             f'<td class="num">{M["capex_subtotal"]:,}</td><td class="num"></td></tr>')
    s.append(f'<tr><td>Contingency (15%)</td><td class="num">{M["contingency"]:,}</td>'
             f'<td class="num"></td></tr>')
    s.append(f'<tr class="tot"><td>මුළු CAPEX</td><td class="num">{M["total_capex"]:,}</td>'
             f'<td class="num">100%</td></tr>')
    s.append(f'<tr><td>Working capital (මාස 3)</td><td class="num">{M["working_capital"]:,}</td>'
             f'<td class="num"></td></tr>')
    s.append(f'<tr class="tot"><td>💰 මුළු ආයෝජනය / TOTAL INVESTMENT</td>'
             f'<td class="num">{M["total_investment"]:,}</td><td class="num"></td></tr>')
    s.append(f'<tr class="land"><td><b>Mr. Thilakarathna ගේ මුදල් අවශ්‍යතාව</b> '
             f'(ඉඩම් වටිනාකම Rs {M["land_value"]:,} අඩු කිරීමෙන් පසු)</td>'
             f'<td class="num"><b>{M["cash_investment"]:,}</b></td><td class="num"></td></tr>')
    s.append('</table></div>')

    s.append('<h3>📊 කාණ්ඩ අනුව බෙදීම</h3><div class="card">' +
             bar_chart([(lbl, cats[c]) for c, lbl in
                        [("building", "🏢 ගොඩනැඟිල්ල"), ("plant", "⚙️ යන්ත්‍රෝපකරණ + QC lab"),
                         ("utility", "⚡ Utilities"), ("logistics", "🚚 වාහන + ගබඩා"),
                         ("env", "🌿 පරිසර + ආරක්ෂාව"), ("pre", "📄 ලියාපදිංචි + උපදේශන")]]) +
             '</div>')

    s.append('<div class="note rd"><b>⚠️ මිල සටහන:</b> ඉහත සියලු අගයන් '
             '<b>උපකල්පිත (indicative) පමණි.</b> විදේශ යන්ත්‍ර සඳහා රේගු තීරු බදු, PAL, VAT, '
             'CESS, නැව් ගාස්තු සහ විනිමය අනුපාත අනුව සැලකිය යුතු ලෙස වෙනස් වේ. '
             '<b>සෑම ප්‍රධාන යන්ත්‍රයක් සඳහාම quotation 3ක්</b> ලබාගෙන මෙම අයවැය '
             'යළි ගණනය කරන්න. මෙය ආයෝජන තීරණයක් ගැනීමට පෙර අනිවාර්යයි.</div>')
    s.append('<h3>🎯 අයවැය විකල්ප 3ක් — Mr. Thilakarathna ට තෝරාගැනීමට</h3>')
    s.append('<div class="tbl"><table><tr><th>විකල්පය</th><th class="num">CAPEX</th>'
             '<th class="num">Working capital</th><th class="num">මුළු ආයෝජනය</th>'
             '<th class="num">ආයෝජකයාගේ මුදල්</th><th>විස්තරය</th></tr>')
    for sc in M["scenarios"]:
        star = ' class="land"' if sc is M["scenarios"][0] else ''
        s.append(f'<tr{star}><td><b>{sc["name"]}</b><br>'
                 f'<span class="pill p-high">{sc["tag"]}</span></td>'
                 f'<td class="num">{sc["total_capex"]:,}</td>'
                 f'<td class="num">{sc["working_capital"]:,}</td>'
                 f'<td class="num"><b>{sc["total_investment"]:,}</b></td>'
                 f'<td class="num">{sc["cash_investment"]:,}</td>'
                 f'<td style="font-size:12px">{sc["note"]}</td></tr>')
    s.append('</table></div>')
    saving = M["scenarios"][1]["cash_investment"] - M["scenarios"][0]["cash_investment"]
    s.append(f'<div class="note"><b>⭐ Option A නිර්දේශ කරන්නේ ඇයි:</b> Option B ට වඩා '
             f'<b>Rs {saving/1_000_000:,.1f}M ක් අඩුය.</b> ඒ මුදලින් වෙළඳපොළ වර්ධනය කළ හැක. '
             'වාහන, 19L රේඛාව සහ blow moulding වෙළඳපොළ තහවුරු වූ <b>පසු</b> එකතු කරන්න — '
             'එවිට ඒවාට අවශ්‍ය ධාරිතාව ඇති බව ඔබ දන්නවා. '
             '<b>අඩු ආරම්භක මුදලක් + අඩු අවදානමක් + එකම වර්ධන මාර්ගය.</b></div>')

    s.append('</section>')

    # ================= UNIT COST =================
    s.append('<section id="unitcost"><h2><span class="n">7</span>🧮 බෝතලයක පිරිවැය — සම්පූර්ණ ගණනය</h2>'
             '<p class="lead">සෑම සතයක්ම කොහෙද යන්නේ කියා · <b>Cost of one bottle — line by line</b></p>')
    s.append('<div class="grid g4">')
    for sk in M["skus"]:
        s.append(kpi(f'{sk["sku"]} — පිරිවැය', f'Rs {sk["variable_cost"]:,.2f}',
                     f'විකුණුම් Rs {sk["ex_factory_price"]:,.0f} · ලාභය Rs {sk["contribution"]:,.2f} '
                     f'({sk["margin_pct"]:.0f}%)'))
    s.append(kpi("19 L — පිරිවැය", f'Rs {M["sku19"]["variable_cost"]:,.2f}',
                 f'විකුණුම් Rs {M["sku19"]["ex_factory_price"]:,.0f} · ලාභය '
                 f'Rs {M["sku19"]["contribution"]:,.2f} ({M["sku19"]["margin_pct"]:.0f}%)', "ol"))
    s.append('</div>')

    for sk in M["skus"] + [M["sku19"]]:
        s.append(f'<h3>🍶 {sk["sku"]} — පිරිවැය ගොඩනැගීම</h3>')
        s.append('<div class="grid g2"><div class="tbl"><table>'
                 '<tr><th>අයිතමය</th><th class="num">Rs</th><th class="num">%</th></tr>')
        tot = sum(sk["costs"].values())
        for k, v in sk["costs"].items():
            s.append(f'<tr><td>{k}</td><td class="num">{v:,.2f}</td>'
                     f'<td class="num">{v/tot*100:.0f}%</td></tr>')
        s.append(f'<tr class="tot"><td>මුළු variable පිරිවැය</td>'
                 f'<td class="num">{tot:,.2f}</td><td class="num">100%</td></tr>')
        s.append('</table></div><div>')
        mx = max(sk["costs"].values())
        s.append('<div class="card" style="height:100%"><div class="bar-chart">')
        for k, v in sorted(sk["costs"].items(), key=lambda x: -x[1]):
            w = max(3, round(v / mx * 100))
            short = k.split("(")[0].strip()[:34]
            s.append(f'<div class="bc-row"><div class="lbl">{short}</div>'
                     f'<div class="bar"><i style="width:{w}%"></i></div>'
                     f'<div class="val">{v:,.2f}</div></div>')
        s.append('</div></div></div></div>')

    s.append('<h3>🎯 Blended (මිශ්‍ර) — SKU mix අනුව</h3><div class="tbl"><table>'
             '<tr><th>SKU</th><th class="num">Mix</th><th class="num">පිරිවැය</th>'
             '<th class="num">Ex-factory මිල</th><th class="num">ලාභය</th>'
             '<th class="num">Margin</th><th class="num">Retail මිල</th></tr>')
    for sk in M["skus"]:
        s.append(f'<tr><td><b>{sk["sku"]}</b></td><td class="num">{sk["share"]*100:.0f}%</td>'
                 f'<td class="num">Rs {sk["variable_cost"]:,.2f}</td>'
                 f'<td class="num">Rs {sk["ex_factory_price"]:,.2f}</td>'
                 f'<td class="num">Rs {sk["contribution"]:,.2f}</td>'
                 f'<td class="num">{sk["margin_pct"]:.0f}%</td>'
                 f'<td class="num">Rs {sk["retail_price"]:,.0f}</td></tr>')
    s.append(f'<tr class="tot"><td>Blended</td><td class="num">100%</td>'
             f'<td class="num">Rs {M["blend_variable"]:,.2f}</td>'
             f'<td class="num">Rs {M["blend_price"]:,.2f}</td>'
             f'<td class="num">Rs {M["blend_contribution"]:,.2f}</td>'
             f'<td class="num">{M["blend_margin_pct"]:.0f}%</td><td class="num">—</td></tr>')
    s.append('</table></div>')

    s.append('<div class="note"><b>🔑 වැදගත්:</b> ඉහත පිරිවැය <b>variable</b> පමණි. '
             'Fixed පිරිවැය (වැටුප්, marketing, නඩත්තු, depreciation) තවත් '
             f'<b>Rs {M["fixed_total_y1"]/y1["pet_bottles_m"]:,.2f}</b> එක් බෝතලයකට එකතු වේ '
             f'(Year 1, බෝතල් {y1["pet_bottles_m"]:,}/මාස දී). '
             f'එවිට <b>සම්පූර්ණ පිරිවැය ≈ Rs {M["blend_variable"]+M["fixed_total_y1"]/y1["pet_bottles_m"]:,.2f}</b> '
             f'· ලාභය ≈ Rs {M["blend_price"]-(M["blend_variable"]+M["fixed_total_y1"]/y1["pet_bottles_m"]):,.2f}/බෝතලය.</div>')
    s.append('</section>')

    # ================= PROFIT =================
    s.append('<section id="profit"><h2><span class="n">8</span>📈 ලාභය සහ Break-even</h2>'
             '<p class="lead">ව්‍යාපාරය ලාභදායී වන්නේ කෙසේද · <b>How the business makes money</b></p>')
    s.append('<div class="grid g4">')
    s.append(kpi("Contribution / බෝතලය", f'Rs {M["blend_contribution"]:,.2f}',
                 f'{M["blend_margin_pct"]}% margin'))
    s.append(kpi("Break-even පරිමාව", f'{M["breakeven_pet"]:,}',
                 f'බෝතල්/මාස · ධාරිතාවෙන් {M["breakeven_pct"]*100:.0f}% පමණයි', "ol"))
    s.append(kpi("Fixed පිරිවැය / මාස (Y1)", "Rs " + m(M["fixed_total_y1"]),
                 "වැටුප්, marketing, නඩත්තු, depreciation"))
    s.append(kpi("Payback", f'{M["payback_year"]} <em>වසර</em>',
                 f'Year {M["payback_year"]} මාස {M["payback_months"]} දී', "ol"))
    s.append('</div>')

    s.append('<h3>📊 මාසික P&L — වසර 3</h3><div class="tbl"><table>'
             '<tr><th>අයිතමය</th>' +
             "".join(f'<th class="num">{p["year"]}</th>' for p in M["projection"]) +
             '</tr>')
    lines = [
        ("ධාරිතාව භාවිතය", lambda p: f'{p["utilisation"]*100:.0f}%', False),
        ("PET බෝතල් / මාස", lambda p: f'{p["pet_bottles_m"]:,}', False),
        ("19 L බෝතල් / මාස", lambda p: f'{p["v19_m"]:,}', False),
        ("ආදායම / මාස", lambda p: f'{p["revenue_m"]:,.0f}', False),
        ("Variable පිරිවැය", lambda p: f'{p["variable_m"]:,.0f}', False),
        ("**Contribution**", lambda p: f'{p["contribution_m"]:,.0f}', True),
        ("Fixed පිරිවැය", lambda p: f'{p["fixed_m"]:,.0f}', False),
        ("**ලාභය (බදු ට පෙර) / මාස**", lambda p: f'{p["pbt_m"]:,.0f}', True),
        ("බදු (30%)", lambda p: f'{p["pbt_m"]*M["tax_rate"]:,.0f}', False),
        ("**ශුද්ධ ලාභය / මාස**", lambda p: f'{p["pat_m"]:,.0f}', True),
        ("**ශුද්ධ ලාභය / වසර**", lambda p: f'{p["pat_y"]:,.0f}', True),
    ]
    for nm, fn, bold in lines:
        cls = ' class="sub"' if bold else ''
        label = nm.replace("**", "")
        s.append(f'<tr{cls}><td>{"<b>" if bold else ""}{label}{"</b>" if bold else ""}</td>' +
                 "".join(f'<td class="num">{fn(p)}</td>' for p in M["projection"]) + '</tr>')
    s.append('</table></div>')

    s.append('<h3>💰 ආයෝජනය ආපසු ලැබීම / Cumulative payback</h3><div class="card">' +
             bar_chart([("Year 1", y1["pat_y"]),
                        ("Year 1–2", y1["pat_y"] + y2["pat_y"]),
                        ("Year 1–3", y1["pat_y"] + y2["pat_y"] + y3["pat_y"]),
                        ("අවශ්‍ය මුදල් (cash)", M["cash_investment"])], "ol") +
             '</div>')

    s.append('<div class="note"><b>✅ Break-even ඇයි ආරක්ෂිත:</b> '
             f'ධාරිතාවෙන් <b>{M["breakeven_pct"]*100:.0f}%</b> පමණක් විකුණුවද '
             f'(බෝතල් {M["breakeven_pet"]:,}/මාස) ව්‍යාපාරය පාඩු නොලබයි. '
             'Year 1 ඉලක්කය 40% බැවින් ආරක්ෂිත පරතරයක් ඇත.</div>')

    s.append('<h3>🎚️ Sensitivity — ධාරිතාව අනුව ලාභය</h3>')
    s.append('<p style="color:var(--muted);font-size:12.5px;margin:0 0 8px">'
             'ඔබ සැබවින්ම කීයක් විකුණයිද කියා නොදනී. එබැවින් අවස්ථා කිහිපයක්:</p>')
    s.append('<div class="tbl"><table><tr><th>ධාරිතාව භාවිතය</th><th class="num">බෝතල්/මාස</th>'
             '<th class="num">ආදායම/මාස</th><th class="num">Contribution/මාස</th>'
             '<th class="num">ශුද්ධ ලාභය/වසර</th><th>තත්ත්වය</th></tr>')
    for r in M["sensitivity"]:
        if r["pat_y"] <= 0:
            tag, cls = "🔴 පාඩු", "p-crit"
        elif r["pat_y"] < 20_000_000:
            tag, cls = "🟡 සුළු ලාභ", "p-mand"
        else:
            tag, cls = "🟢 ලාභදායී", "p-high"
        row = ' class="land"' if abs(r["util"] - 0.25) < 0.001 else ''
        s.append(f'<tr{row}><td><b>{r["util"]*100:.0f}%</b></td>'
                 f'<td class="num">{r["bottles"]:,}</td>'
                 f'<td class="num">{r["revenue_m"]:,.0f}</td>'
                 f'<td class="num">{r["contribution_m"]:,.0f}</td>'
                 f'<td class="num"><b>{r["pat_y"]:,.0f}</b></td>'
                 f'<td><span class="pill {cls}">{tag}</span></td></tr>')
    s.append('</table></div>')
    s.append('<div class="note ol"><b>🟢 හොඳ පුවත:</b> ධාරිතාවෙන් '
             f'<b>{M["breakeven_pct"]*100:.0f}%</b> පමණක් විකුණුවද පාඩු නැත '
             f'(බෝතල් {M["breakeven_pet"]:,}/මාස). '
             'නමුත් 15% ට වඩා අඩු නම් පාඩු ලැබේ — එබැවින් '
             '<b>බෙදාහැරීමේ ජාලය මුලින්ම ශක්තිමත් කරගන්න.</b></div>')

    s.append('<h3>💸 මිල පීඩනය — තරඟකරුවන් මිල අඩු කළොත්?</h3>')
    s.append('<div class="tbl"><table><tr><th>මිල වෙනස</th><th class="num">Ex-factory (blended)</th>'
             '<th class="num">Contribution/බෝතලය</th><th class="num">Margin</th>'
             '<th class="num">Break-even බෝතල්/මාස</th></tr>')
    for r in M["price_sens"]:
        sign = "+" if r["delta"] > 0 else ""
        be = f'{r["breakeven"]:,}' if r["breakeven"] else "⛔ කළ නොහැක"
        row = ' class="land"' if r["delta"] == 0 else ''
        s.append(f'<tr{row}><td><b>{sign}{r["delta"]*100:.0f}%</b></td>'
                 f'<td class="num">Rs {r["price"]:,.2f}</td>'
                 f'<td class="num">Rs {r["contribution"]:,.2f}</td>'
                 f'<td class="num">{r["margin"]:.0f}%</td>'
                 f'<td class="num">{be}</td></tr>')
    s.append('</table></div>')
    s.append('<div class="note am"><b>⚠️ තරඟකාරී මිල යුද්ධය:</b> විශාල බ්‍රෑන්ඩ් මිල '
             '10–15% ක් අඩු කළහොත් ඔබේ margin සැලකිය යුතු ලෙස අඩු වේ. '
             '<b>ආරක්ෂාව:</b> (1) 19L contract sales — මිල යුද්ධයෙන් ඔබ්බට, '
             '(2) කඳුකර මූලාශ්‍රය = premium positioning, '
             '(3) Phase 2 blow moulding = ඒකක පිරිවැය 30–40% අඩුයි.</div>')

    s.append('<h3>📈 ලාභ වැඩි කරන ක්‍රම 6</h3><div class="grid g3">')
    for t, d in [("19 L රේඛාව වැඩි කරන්න",
                  f'Margin {M["sku19"]["margin_pct"]:.0f}% — PET වලට වඩා දෙගුණයක්. '
                  'කාර්යාල/හෝටල් contract එකක් = ස්ථාවර ආදායමක්'),
                 ("Phase 2: Blow moulding",
                  'බෝතල් තමන්ම හැදුවහොත් ඒකක පිරිවැය 30–40% අඩු වේ '
                  '(preform Rs 8–10 vs බෝතලය Rs 12.50–23)'),
                 ("2 වන shift එක",
                  'Fixed පිරිවැය වෙනස් නොවී නිෂ්පාදනය දෙගුණ වේ → ඒකක පිරිවැය අඩුයි'),
                 ("උඩරට hotel/tourism",
                  'බණ්ඩාරවෙල–එල්ල–හපුතලේ සංචාරක කලාපය. Premium මිලට විකිණිය හැක'),
                 ("Private label",
                  'හෝටල්/සුපිරි වෙළඳසැල් සඳහා ඔවුන්ගේ ලේබලයෙන් — marketing පිරිවැයක් නැත'),
                 ("අපනයනය",
                  'Maldives, Middle East — VAT zero-rated; ඉහළ මිල')]:
        s.append(f'<div class="card"><b>{t}</b><div style="color:var(--muted);font-size:12.5px;'
                 f'margin-top:4px">{d}</div></div>')
    s.append('</div></section>')

    # ================= GROWTH =================
    s.append('<section id="growth"><h2><span class="n">9</span>🚀 ව්‍යාපෘතිය ඉක්මනින් වර්ධනය කිරීම</h2>'
             '<p class="lead">අවදානම අඩුවෙන්, වේගයෙන් · <b>Fast expansion plan — phase by phase</b></p>')
    s.append('<div class="tl">')
    for ph, ttl, body in [
        ("Phase 1", "වසර 1 — පදනම + වෙළඳපොළට පිවිසීම",
         "6,000 BPH · බෝතල් මිලදී ගැනීම · PET 500ml/1L/1.5L + 19L රේඛාව · "
         "බණ්ඩාරවෙල–බදුල්ල–හපුතලේ–එල්ල බෙදාහැරීම · ඉලක්කය 40% ධාරිතාව · "
         "<b>ආයෝජනය Rs " + m(REC["total_investment"]) + "</b> (Option A — Lean Start)"),
        ("Phase 2", "වසර 2 — ඒකක පිරිවැය අඩු කිරීම",
         "PET blow moulding යන්ත්‍රය එකතු කිරීම → බෝතල් පිරිවැය 30–40% අඩු වේ · "
         "නුවරඑළිය–මහනුවර දක්වා ව්‍යාප්තිය · ඉලක්කය 70% · "
         "අමතර ආයෝජනය Rs 8M–18M"),
        ("Phase 3", "වසර 3 — පරිමාව දෙගුණ කිරීම",
         "2 වන shift · දෙවන monoblock · 100% ධාරිතාව · කොළඹ වෙළඳපොළ · "
         "Private label contracts · අමතර ආයෝජනය Rs 25M–45M"),
        ("Phase 4", "වසර 4+ — අපනයනය + premium",
         "Maldives, Middle East (UAE/Qatar) · ISO 22000 / FSSC 22000 · "
         "Halal · උල්පතක් සොයාගතහොත් premium Natural Mineral Water (SLS 1038) දෙවන බ්‍රෑන්ඩ් එකක් ලෙස"),
    ]:
        s.append(f'<div class="tl-i"><div class="tl-m">{ph}</div>'
                 f'<div class="tl-c"><b>{ttl}</b><div class="t">{body}</div></div></div>')
    s.append('</div>')

    s.append('<h3>⚡ ඉක්මන් වර්ධනයට තීරණාත්මක කරුණු 7</h3><div class="tbl"><table>'
             '<tr><th>#</th><th>ක්‍රියාමාර්ගය</th><th>ඇයි වැදගත්</th></tr>')
    for i, (a, b) in enumerate([
        ("ළිඳ 2ක් කණින්න", "එක ළිඳක් අසාර්ථක වුවහොත් කර්මාන්ත ශාලාව නවතී. දෙවන ළිඳ = ආරක්ෂාව + ධාරිතාව"),
        ("19 L contract sales මුලින්ම", "ස්ථාවර මාසික ආදායමක් → cash flow ස්ථාවරයි → ණය අවශ්‍යතාව අඩුයි"),
        ("බෙදාහරින්නන් 6–8ක් එකවර", "එක් අයෙකු මත රඳා පැවතීම අවදානමකි. ප්‍රදේශ අනුව බෙදන්න"),
        ("Trademark මුලින්ම", "බ්‍රෑන්ඩ් එක වර්ධනය වූ පසු නම අහිමි වීම = සියල්ල අහිමි වීම"),
        ("QR → lab report", "විනිවිදභාවය = වෙළඳ ලකුණ. කඳුකර මූලාශ්‍රය = විශාලතම වාසිය"),
        ("Phase 2 blow moulding කල් දමන්න", "ආරම්භක CAPEX අඩු කරයි; විකුණුම් තහවුරු වූ පසු ආයෝජනය කරන්න"),
        ("Working capital මාස 6ක්", "Retail credit 30–60 දින. Cash flow කඩා වැටීම = ව්‍යාපාරය මිය යයි"),
    ], start=1):
        s.append(f'<tr><td class="num"><b>{i}</b></td><td><b>{a}</b></td><td>{b}</td></tr>')
    s.append('</table></div></section>')

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
