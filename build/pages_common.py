#!/usr/bin/env python3
"""Build the seven separate pages the investor asked for.

  1-setup-budget.html          start -> factory registered, built, machines in,
                               up to the day work begins.  FULL budget, office
                               equipment included.
  2-first-production.html      day production starts -> first order stock is
                               finished.  Bottles, labels, bottling, wages.
  3-first-stock-cost.html      the bottle cost of that first stock, using the
                               exact quantities given.
  4-process-documents.html     the process step by step, which document each
                               step needs, and how long each step takes.

Plus a landing page (index.html) that links all of them.

Everything is derived from build/dashboard_model.py, so the seven pages and the
main dashboard can never disagree.
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_dashboard import CSS, ASSET, plain   # noqa: E402
from dashboard_model import build_model         # noqa: E402
from language_support import (LANGUAGE_BOOTSTRAP, LANGUAGE_JS, LANGUAGE_SWITCH,
                              fill_empty_table_cells, highlight_prompts,
                              mark_bilingual_pairs)  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")

PAGES = [
    ("1-setup-budget.html", "1", "ආරම්භක අයවැය", "Setup Budget"),
    ("2-first-production.html", "2", "පළමු නිෂ්පාදන අයවැය", "First Production Budget"),
    ("3-first-stock-cost.html", "3", "පළමු stock එකේ පිරිවැය", "First Stock Cost"),
    ("4-process-documents.html", "4", "ක්‍රියාවලිය", "Process"),
    ("5-organisation-chart.html", "5", "කළමනාකරණය සහ මූල්‍ය", "Management & Finance"),
    ("6-sales-marketing.html", "6", "අලෙවිය සහ අලෙවිකරණය", "Sales & Marketing"),
    ("7-final-summary.html", "7", "අවසන් සාරාංශය", "Final Summary"),
]

PAGE_CATEGORY = {
    "0": ("බණ්ඩාරවෙල · ඌව කඳුකරය", "Bandarawela · Uva Highlands"),
    "1": ("අයවැය", "Budget"),
    "2": ("අයවැය", "Budget"),
    "3": ("අයවැය", "Budget"),
    "4": ("ක්‍රියාවලිය", "Process"),
    "5": ("කළමනාකරණය සහ මූල්‍ය", "Management & Finance"),
    "6": ("අලෙවිය සහ අලෙවිකරණය", "Sales & Marketing"),
    "7": ("අවසන් සාරාංශය", "Final Summary"),
}


def esc(t):
    """& is not valid raw in HTML text."""
    return html.escape(str(t), quote=False)


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
    """One column: a slim top bar, a masthead, then every block stacked."""
    budget_open = " open" if num in {"1", "2", "3"} else ""
    budget_active = " on" if budget_open else ""
    nav = ['<div class="brand"><div class="logo">W</div><h1><span class="si">බෝතල් ජල කර්මාන්ත ශාලාව</span>'
           '<span class="en">Bottled Drinking Water Plant</span></h1>'
           f'<p>{M["location"]}<br><b><span class="si">ආයෝජක</span><span class="en">Investor</span>: '
           f'{M["investor"]}</b></p>{LANGUAGE_SWITCH}</div>',
           '<div class="nav-links">',
           f'<details class="nav-dropdown budget-dropdown"{budget_open}>',
           f'<summary class="budget-trigger{budget_active}"><span class="si">අයවැය</span>'
           '<span class="en">Budget</span><span class="dropdown-caret" aria-hidden="true">⌄</span></summary>',
           '<div class="dropdown-menu">']
    for fname, pn, si, en in PAGES[:3]:
        on = ' class="on"' if pn == num else ""
        nav.append(f'<a href="{fname}"{on}><span class="si">{esc(si)}</span><span class="en">{esc(en)}</span></a>')
    nav.append('</div></details>')
    fname, pn, si, en = PAGES[3]
    on = ' class="on"' if pn == num else ""
    nav.append(f'<a href="{fname}"{on}><span class="si">{esc(si)}</span><span class="en">{esc(en)}</span></a>')
    nav.append('<a href="dashboard.html"><span class="si">Dashboard</span>'
               '<span class="en">Dashboard</span></a>')
    for fname, pn, si, en in PAGES[4:]:
        on = ' class="on"' if pn == num else ""
        nav.append(f'<a href="{fname}"{on}><span class="si">{esc(si)}</span><span class="en">{esc(en)}</span></a>')
    nav.append('<a href="docs.html"><span class="si">ලේඛන පැකේජය</span>'
               '<span class="en">Document Pack</span></a>')
    nav.append('</div>')

    category_si, category_en = PAGE_CATEGORY.get(num, PAGE_CATEGORY["0"])
    hero_actions = ""
    if num == "0":
        hero_actions = """\n    <div class=\"hero-actions\">\n      <a class=\"btn btn-primary\" href=\"#project-sections\"><span class=\"si\">ව්‍යාපෘති සාරාංශය</span><span class=\"en\">Project overview</span></a>\n      <a class=\"btn btn-secondary\" href=\"dashboard.html\"><span class=\"si\">සම්පූර්ණ Dashboard</span><span class=\"en\">Open full dashboard</span></a>\n    </div>"""

    doc = f"""<!doctype html>
<html lang="si"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{LANGUAGE_BOOTSTRAP}
<title>{esc(title_si)} — {esc(title_en)} | Bottled Drinking Water Plant</title>
<style>{CSS}</style>
</head><body>
<div id="wrap">
<nav id="nav">{''.join(nav)}</nav>
<main id="main">
<div class="hero hero--upcountry" style="{cover_bg()}">
  <div class="hc">
    <div class="kicker"><span class="si">{category_si}</span><span class="en">{category_en}</span></div>
    <h1><span class="si">{title_si}</span><span class="en">{esc(title_en)}</span></h1>
    <p class="hsub">{subtitle}</p>{hero_actions}
  </div>
</div>
<div class="inner">
{body}
<footer>
  {M["location"]} · ආයෝජක / Investor: <b>{M["investor"]}</b><br>
  නිෂ්පාදනය / Product: <b>Bottled Drinking Water (SLS 894)</b> ·
  නිෂ්පාදන / Products: 500 ml · 1 L · 1.5 L · 5 L · 19 L<br>
  සියලු මුදල් අගයන් <b>උපකල්පිත (indicative)</b> —
  quotation 3ක් ලබාගෙන තහවුරු කරගන්න.<br>
  සකස් කළ දිනය / Prepared: 2026-10-10
</footer>
</div>
</main>
</div>
<script>{LANGUAGE_JS}</script>
</body></html>"""
    rendered = mark_bilingual_pairs(plain(doc))
    return highlight_prompts(fill_empty_table_cells(rendered))


_HTML_TAGS = re.compile(r"<[^>]+>")
_NUMBER_CELL = re.compile(r"^\(?-?\d+(?:\.\d+)?\)?$")


def _looks_numeric(value):
    """Return whether a rendered table value behaves like a number.

    The reports contain a mix of quantities, currency, units and phases.  The
    former all need to align on the decimal/ones place; the latter should stay
    left-aligned for fast scanning.  This deliberately accepts common display
    prefixes/suffixes while leaving descriptive text alone.
    """
    text = _HTML_TAGS.sub("", str(value)).replace("&nbsp;", " ").strip()
    if not text or text in {"—", "-", "–"}:
        return None
    text = re.sub(r"(?i)\b(?:rs\.?|lkr)\s*", "", text)
    text = text.replace(",", "").replace("%", "").strip()
    text = re.sub(r"\s*(?:L|M|K)$", "", text, flags=re.I)
    return bool(_NUMBER_CELL.fullmatch(text))


def _numeric_columns(head, rows):
    """Infer semantic number columns from actual data, not their position."""
    numeric = set()
    for index, title in enumerate(head):
        values = [row[index] for row in rows if len(row) > index]
        checks = [_looks_numeric(value) for value in values]
        observed = [value for value in checks if value is not None]
        if observed and sum(observed) / len(observed) >= 0.65:
            numeric.add(index)
            continue
        label = _HTML_TAGS.sub("", str(title)).lower()
        if any(token in label for token in (
            "qty", "quantity", "cost", "price", "margin", "profit", "amount",
            "rate", "salary", "capex", "opex", "investment", "%", "මුදල", "මිල",
            "වියදම", "වැටුප", "ප්‍රමාණ", "ධාරිතාව",
        )):
            numeric.add(index)
    return numeric


def _amount_columns(head):
    money_words = ("cost", "price", "amount", "rate", "salary", "capex", "opex",
                   "investment", "මුදල", "මිල", "වියදම", "වැටුප")
    return {index for index, title in enumerate(head)
            if any(word in _HTML_TAGS.sub("", str(title)).lower() for word in money_words)}


def table(head, rows, total=None, total_label="මුළු / TOTAL"):
    """Render an accessible report table with semantic numeric columns.

    Number alignment is inferred per column, so a ``Unit`` or ``Phase`` column
    remains readable while quantities and LKR figures receive tabular numeric
    treatment.  Generated totals inherit the same column semantics.
    """
    numeric = _numeric_columns(head, rows)
    amounts = _amount_columns(head)

    def classes(index):
        names = []
        if index in numeric:
            names.append("num")
        if index in amounts:
            names.append("amount")
        return f' class="{" ".join(names)}"' if names else ""

    out = ['<div class="tbl scroll"><table><colgroup>']
    out += [f'<col{classes(index)}>' for index in range(len(head))]
    out.append('</colgroup><thead><tr>')
    out += [f'<th scope="col"{classes(index)}>{title}</th>'
            for index, title in enumerate(head)]
    out.append('</tr></thead><tbody>')
    for row in rows:
        out.append('<tr>' + "".join(
            f'<td{classes(index)}>{cell}</td>'
            for index, cell in enumerate(row)) + '</tr>')
    if total:
        total_row = [total_label] + list(total)
        out.append('<tr class="grand">' + "".join(
            f'<td{classes(index)}>{cell}</td>'
            for index, cell in enumerate(total_row)) + '</tr>')
    out.append('</tbody></table></div>')
    return "".join(out)
