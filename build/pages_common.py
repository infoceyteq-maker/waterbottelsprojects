#!/usr/bin/env python3
"""Build the four separate pages the investor asked for.

  1-setup-budget.html          start -> factory registered, built, machines in,
                               up to the day work begins.  FULL budget, office
                               equipment included.
  2-first-production.html      day production starts -> first order stock is
                               finished.  Bottles, labels, bottling, wages.
  3-first-stock-cost.html      the bottle cost of that first stock, using the
                               exact quantities given.
  4-process-documents.html     the process step by step, which document each
                               step needs, and how long each step takes.

Plus a landing page (index.html) that links all four.

Everything is derived from build/dashboard_model.py, so the five pages and the
main dashboard can never disagree.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_dashboard import CSS, ASSET          # noqa: E402
from dashboard_model import build_model         # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")

PAGES = [
    ("1-setup-budget.html", "1", "ආරම්භක අයවැය", "Setup budget"),
    ("2-first-production.html", "2", "පළමු නිෂ්පාදන අයවැය", "First production"),
    ("3-first-stock-cost.html", "3", "පළමු stock එකේ පිරිවැය", "First stock cost"),
    ("4-process-documents.html", "4", "ක්‍රියාවලිය + ලේඛන", "Process & documents"),
    ("5-organisation-chart.html", "5", "කර්මාන්ඩල සටහන", "Organisation chart"),
]


def m(n):
    return f"{n/1_000_000:,.1f}M"


def kpi(label, value, hint="", cls=""):
    return (f'<div class="kpi {cls}"><div class="l">{label}</div>'
            f'<div class="v">{value}</div><div class="h">{hint}</div></div>')


def cover_bg():
    if not os.path.exists(ASSET):
        return ""
    import base64
    with open(ASSET, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return f'background-image:url("data:image/jpeg;base64,{b64}")'


def shell(M, num, title_si, title_en, subtitle, body):
    nav = ['<div class="brand"><div class="logo">💧</div>'
           '<h1>බෝතල් ජල කර්මාන්ත ශාලාව'
           '<span style="display:block;font-size:11.5px;font-weight:500;'
           'color:var(--muted);margin-top:3px">Bottled Drinking Water Plant</span></h1>'
           f'<p>{M["location"]}<br><b>ආයෝජක / Investor:<br>{M["investor"]}</b></p></div>',
           '<div class="nsec">පිටු 4 / The five pages</div>']
    for fname, n, si, en in PAGES:
        on = ' class="on"' if n == num else ""
        nav.append(f'<a href="{fname}"{on}>📄 පිටුව {n} — {si}'
                   f'<span class="en">{en}</span></a>')
    nav.append('<div class="nsec">අමතර / Also</div>')
    nav.append('<a href="dashboard.html">📊 සම්පූර්ණ Dashboard'
               '<span class="en">The full panel</span></a>')
    nav.append('<a href="docs.html">📚 ලේඛන පැකේජය'
               '<span class="en">21 documents</span></a>')

    return f"""<!doctype html>
<html lang="si"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_si} — {title_en} | Bandarawela Water Plant</title>
<style>{CSS}</style>
</head><body>
<div id="wrap">
<nav id="nav">{''.join(nav)}</nav>
<main id="main">
<div class="hero" style="{cover_bg()}">
  <div class="hc">
    <div class="kicker">පිටුව {num} &nbsp;·&nbsp; Page {num} of 5</div>
    <h1>{title_si}<br><span style="font-size:19px;font-weight:600;color:#cbd5ce">{title_en}</span></h1>
    <p class="hsub">{subtitle}</p>
  </div>
</div>
<div class="inner">
{body}
<footer>
  💧 {M["location"]} · ආයෝජක / Investor: <b>{M["investor"]}</b><br>
  නිෂ්පාදනය / Product: <b>Bottled Drinking Water (SLS 894)</b> ·
  නිෂ්පාදන / Products: 500 ml · 1 L · 1.5 L · 5 L · 19 L<br>
  සියලු මුදල් අගයන් <b>උපකල්පිත (indicative)</b> — quotation 3ක් ලබාගෙන තහවුරු කරගන්න.<br>
  සකස් කළ දිනය / Prepared: 2026-10-10
</footer>
</div>
</main>
</div>
</body></html>"""


def table(head, rows, total=None, total_label="මුළු / TOTAL"):
    """head: list of column titles. rows: list of lists. total: list or None."""
    out = ['<div class="tbl scroll"><table><thead><tr>']
    out += [f'<th class="num">{h}</th>' if i else f'<th>{h}</th>'
            for i, h in enumerate(head)]
    out.append('</tr></thead><tbody>')
    for r in rows:
        out.append('<tr>' + "".join(
            f'<td class="num">{c}</td>' if i else f'<td>{c}</td>'
            for i, c in enumerate(r)) + '</tr>')
    if total:
        out.append('<tr class="grand">' + "".join(
            f'<td class="num">{c}</td>' if i else f'<td>{c}</td>'
            for i, c in enumerate([total_label] + list(total))) + '</tr>')
    out.append('</tbody></table></div>')
    return "".join(out)
