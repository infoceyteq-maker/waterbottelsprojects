#!/usr/bin/env python3
"""
Build the static documentation site into site/

Run:  python3 build/build_site.py
View: cd site && python3 -m http.server 8000 --bind 0.0.0.0
"""
import os
import re
import html
import markdown

from build_dashboard import plain  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")

# Ordered navigation: (source path relative to repo root, output name, nav title)
NAV = [
    ("README.md", "docs.html", "🏠 ලේඛන මුල් පිටුව / Docs Home"),
    (None, "dashboard.html", "📊 ⭐ ව්‍යාපෘති DASHBOARD (මුදල් + Qty)"),
    ("docs/01-phase-0-investor-mou.md", "p01.html", "0 · ආයෝජක එකඟතා / Investor & MOU"),
    ("docs/02-phase-1-company-registration.md", "p02.html", "1 · සමාගම් ලියාපදිංචිය / Company (1st Reg.)"),
    ("docs/03-phase-2-land-premises.md", "p03.html", "2 · ඉඩම සහ ගොඩනැඟිල්ල / Land"),
    ("docs/04-phase-3-water-source-wrb.md", "p04.html", "3 · ජල මූලාශ්‍රය / Water Source (WRB)"),
    ("docs/05-phase-4-factory-construction.md", "p05.html", "4 · කර්මාන්ත ශාලාව / Factory"),
    ("docs/06-phase-5-machinery-equipment.md", "p06.html", "5 · යන්ත්‍රෝපකරණ / Machinery"),
    ("docs/07-phase-6-moh-fcau-bottled-water-registration.md", "p07.html", "6 · ⭐ FCAU ලියාපදිංචිය / MoH Registration"),
    ("docs/08-phase-7-slsi-certification.md", "p08.html", "7 · SLSI සහතික / SLSI Certification"),
    ("docs/09-phase-8-environment-cea.md", "p09.html", "8 · පරිසර / Environment (CEA)"),
    ("docs/10-phase-9-tax-labour-statutory.md", "p10.html", "9 · බදු සහ ශ්‍රම / Tax & Labour"),
    ("docs/11-phase-10-launch-market.md", "p11.html", "10 · වෙළඳපොළ / Launch & Market"),
    ("docs/12-master-document-checklist.md", "p12.html", "⭐ MASTER CHECKLIST"),
    ("docs/13-capital-investment-budget.md", "p13.html", "13 · අයවැය / Budget"),
    ("docs/14-project-timeline.md", "p14.html", "14 · කාලසටහන / Timeline"),
    ("docs/15-investor-due-diligence-pack.md", "p15.html", "15 · Due Diligence"),
    ("docs/16-risk-register.md", "p16.html", "16 · අවදානම් / Risk Register"),
    ("docs/17-agency-service-directory.md", "p17.html", "17 · ආයතන / Agency Directory"),
    ("docs/18-renewal-compliance-calendar.md", "p18.html", "18 · නැවුම් කිරීම් / Renewals"),
    ("docs/19-label-requirements.md", "p19.html", "19 · ලේබල් / Labels"),
    ("docs/20-water-treatment-train.md", "p20.html", "20 · 💧 පිරිපහදුව / Water Treatment Train"),
    ("docs/21-decisions-and-assumptions.md", "p21.html", "21 · 📋 තීරණ / Decisions & Assumptions"),
    ("templates/01-MOU-term-sheet.md", "t01.html", "📄 MOU / Term Sheet"),
    ("templates/02-shareholders-agreement-heads-of-terms.md", "t02.html", "📄 Shareholders Agreement"),
    ("templates/03-board-resolution-incorporation.md", "t03.html", "📄 Board Resolution"),
    ("templates/04-water-source-test-request.md", "t04.html", "📄 ජල පරීක්ෂණ ලිපිය"),
    ("templates/05-fcau-application-cover-letter.md", "t05.html", "📄 FCAU ආවරණ ලිපිය"),
]

_HERE = os.path.dirname(os.path.abspath(__file__))


def _css(name):
    with open(os.path.join(_HERE, name), encoding="utf-8") as fh:
        return fh.read()


# style.css first (tokens + the shared vocabulary), then the doc-pack chrome
CSS = _css("style.css") + "\n" + _css("style_docs.css")

PAGE = """<!doctype html>
<html lang="si"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · බෝතල් ජල කර්මාන්ත ශාලාව — Bandarawela</title>
<style>{css}</style></head>
<body><div id="wrap">
<nav id="nav">
  <h1>💧 බෝතල් ජල කර්මාන්ත ශාලාව</h1>
  <div class="sub">Bottled Water Manufacturing Plant · Bandarawela, Badulla<br>
  සම්පූර්ණ ලේඛන පැකේජය · v1.1 · SLS 894 · 2026-10-10</div>
  <input type="text" id="q" placeholder="🔍 පිටු සොයන්න / Filter pages…" oninput="flt()">
  <ol id="nl">{nav}</ol>
</nav>
<main id="main">{body}</main>
</div>
<script>
function flt(){{var v=document.getElementById('q').value.toLowerCase();
document.querySelectorAll('#nl a').forEach(function(a){{
a.parentElement.style.display=a.textContent.toLowerCase().indexOf(v)>-1?'':'none';}});}}
</script>
</body></html>"""


def build_link_map():
    """basename(source.md) -> output page name"""
    mapping = {}
    for src, out, _ in NAV:
        if src is None:
            continue
        mapping[os.path.basename(src)] = out
    return mapping


def fix_links(body, mapping):
    """Rewrite repo-relative .md links to generated site page names."""

    def repl(m):
        target, attrs, inner = m.group(1), m.group(2), m.group(3)
        if target.startswith(("http://", "https://", "mailto:", "#", "/")):
            return m.group(0)
        base = os.path.basename(target.split("#")[0])
        if base in mapping:
            return '<a href="%s"%s>%s</a>' % (mapping[base], attrs, inner)
        return m.group(0)

    # inner may contain <strong>/<em>/<code> etc., so match non-greedily across tags
    return re.sub(r'<a href="([^"]+)"([^>]*)>(.*?)</a>', repl, body, flags=re.S)


def main():
    os.makedirs(OUT, exist_ok=True)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "nl2br"])
    mapping = build_link_map()
    # also expose the data files next to the pages so CSV links resolve
    for extra in ["data/master-checklist.csv", "data/capex-estimate.csv", "data/renewals.csv"]:
        mapping[os.path.basename(extra)] = os.path.join("data", os.path.basename(extra))

    nav_html = []
    for src, out, title in NAV:
        nav_html.append(f'<li><a href="{out}" id="n-{out}">{html.escape(title)}</a></li>')
    nav_html = "\n".join(nav_html)

    written = 0
    for src, out, title in NAV:
        if src is None:
            continue  # nav-only entry (the dashboard is built by build_dashboard.py)
        path = os.path.join(ROOT, src)
        if not os.path.exists(path):
            print(f"[skip] missing {src}")
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        md.reset()
        body = fix_links(md.convert(text), mapping)
        page = PAGE.format(title=html.escape(title), css=CSS, nav=nav_html, body=body)
        # mark active
        page = page.replace(f'id="n-{out}"', f'id="n-{out}" class="on"')
        with open(os.path.join(OUT, out), "w", encoding="utf-8") as fh:
            fh.write(plain(page))
        written += 1

    # copy the data files
    import shutil
    data_out = os.path.join(OUT, "data")
    os.makedirs(data_out, exist_ok=True)
    copied = 0
    for name in ["master-checklist.csv", "capex-estimate.csv", "renewals.csv"]:
        src = os.path.join(ROOT, "data", name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(data_out, name))
            copied += 1

    # The dashboard is what a visitor should land on, so it becomes the site root.
    # "/" -> dashboard,  "/docs.html" -> the markdown documentation index.
    dash = os.path.join(OUT, "dashboard.html")
    if os.path.exists(dash):
        shutil.copyfile(dash, os.path.join(OUT, "index.html"))
        print("[ok] published dashboard as the site root: / -> dashboard")
    else:
        print("[!] site/dashboard.html missing - run build_dashboard.py first")

    print(f"[ok] built {written} pages + {copied} data files into {OUT}")
    print("[ok] preview: cd site && python3 -m http.server 8000 --bind 0.0.0.0")


if __name__ == "__main__":
    main()
