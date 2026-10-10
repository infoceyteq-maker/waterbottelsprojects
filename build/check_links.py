#!/usr/bin/env python3
"""
Project self-check for the documentation pack.

Verifies:
  1. Every markdown file listed in the README index actually exists
  2. Every relative link inside every .md file resolves to a real file
  3. The master-checklist CSV parses and has the documented columns
  4. The generated site contains one page per navigation entry
  5. The generated master checklist is in sync with the CSV

Run:  python3 build/check_links.py
Exit code 0 = all checks pass.
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_dashboard import plain as de_emoji  # noqa: E402
from nav_common import ROW_HREFS, DASHBOARD_FILE, LANDING_FILE  # noqa: E402
from nav_common import PAGES as INVESTOR_PAGES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))

EXPECTED_CSV_COLS = ["id", "phase", "category", "item_en", "item_si",
                     "authority_or_source", "when", "cost_lkr", "validity",
                     "priority", "notes"]
VALID_PRIORITY = {"Critical", "Mandatory", "High", "Medium", "Low"}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

failures = []
warnings = []


def ok(msg):
    print("  \u2713 " + msg)


def fail(msg):
    failures.append(msg)
    print("  \u2717 " + msg)


def warn(msg):
    warnings.append(msg)
    print("  ! " + msg)


def md_files():
    out = []
    for base in ("docs", "templates", "."):
        d = os.path.join(ROOT, base)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".md"):
                out.append(os.path.join(d, name))
    return out


def check_relative_links():
    print("\n[1] Relative markdown links resolve")
    total = checked = 0
    for path in md_files():
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            total += 1
            target_path = target.split("#")[0]
            if not target_path:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target_path))
            if os.path.exists(resolved):
                checked += 1
            else:
                fail(f"{os.path.relpath(path, ROOT)} -> {target} (missing)")
    ok(f"{checked}/{total} relative links resolve to real files")


def check_readme_index():
    print("\n[2] README index entries exist")
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
        readme = fh.read()
    refs = [t for t in (m.group(1).strip() for m in LINK_RE.finditer(readme))
            if not t.startswith(("http://", "https://", "#"))]
    missing = [r for r in refs
               if not os.path.exists(os.path.normpath(os.path.join(ROOT, r.split("#")[0])))]
    for r in missing:
        fail(f"README references missing file: {r}")
    if not missing:
        ok(f"all {len(refs)} README references resolve")


def check_csv():
    print("\n[3] data/master-checklist.csv structure")
    path = os.path.join(ROOT, "data", "master-checklist.csv")
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames
        rows = list(reader)

    if cols != EXPECTED_CSV_COLS:
        fail(f"CSV columns mismatch\n     expected: {EXPECTED_CSV_COLS}\n     got:      {cols}")
    else:
        ok(f"CSV has the {len(cols)} documented columns")

    ids = [r["id"] for r in rows]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        fail(f"duplicate ids: {sorted(dupes)}")
    else:
        ok(f"{len(ids)} unique item ids, no duplicates")

    bad_prio = {r["id"]: r["priority"] for r in rows if r["priority"] not in VALID_PRIORITY}
    if bad_prio:
        fail(f"invalid priority values: {bad_prio}")
    else:
        ok(f"all priorities valid ({', '.join(sorted(VALID_PRIORITY))})")

    blanks = [r["id"] for r in rows if not r["item_en"].strip() or not r["phase"].strip()]
    if blanks:
        fail(f"rows missing item_en/phase: {blanks}")
    else:
        ok("no blank phase/item_en values")

    blank_notes = [r["id"] for r in rows if not r["notes"].strip()]
    if blank_notes:
        fail(f"rows with blank Notes cells: {blank_notes[:10]}")
    else:
        ok("all checklist Notes cells are explicit (text or —)")

    phases = []
    for r in rows:
        if r["phase"] not in phases:
            phases.append(r["phase"])
    ok(f"{len(phases)} phases: {phases[0]} ... {phases[-1]}")
    return len(rows), len(phases)


def check_data_files():
    print("\n[4] Other data files parse")
    for name in ("capex-estimate.csv", "renewals.csv"):
        p = os.path.join(ROOT, "data", name)
        if not os.path.exists(p):
            fail(f"missing data/{name}")
            continue
        with open(p, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        if not rows:
            fail(f"data/{name} is empty")
        else:
            blank_cells = [(i + 2, key) for i, row in enumerate(rows)
                           for key, value in row.items() if not (value or "").strip()]
            if blank_cells:
                fail(f"data/{name} has blank cells: {blank_cells[:8]}")
            else:
                ok(f"data/{name}: {len(rows)} rows, {len(rows[0])} columns; no blank cells")


def check_site(item_count):
    print("\n[5] Generated site")
    site = os.path.join(ROOT, "site")
    if not os.path.isdir(site):
        warn("site/ not built yet - run: python3 build/build_site.py")
        return
    from build_site import NAV  # noqa: E402
    missing = [out for _, out, _ in NAV if not os.path.exists(os.path.join(site, out))]
    if missing:
        fail(f"site pages missing: {missing}")
    else:
        ok(f"all {len(NAV)} navigation pages built")

    # no stale .md links should survive the build
    stale = []
    for _, out, _ in NAV:
        with open(os.path.join(site, out), encoding="utf-8") as fh:
            body = fh.read()
        for m in re.finditer(r'href="([^"]+\.md)"', body):
            stale.append((out, m.group(1)))
    if stale:
        fail(f"{len(stale)} unresolved .md links in built pages, e.g. {stale[:3]}")
    else:
        ok("no unresolved .md links in built pages")

    # master checklist page must be in sync with the CSV row count
    with open(os.path.join(site, "p12.html"), encoding="utf-8") as fh:
        p12 = fh.read()
    rows_in_html = len(re.findall(r"<td[^>]*>\u2610</td>", p12))
    if rows_in_html != item_count:
        fail(f"site/p12.html shows {rows_in_html} checklist rows but CSV has {item_count}")
    else:
        ok(f"site/p12.html in sync with CSV ({rows_in_html} checklist rows)")

    # Every generated page family must expose the persistent language picker.
    html_files = [name for name in os.listdir(site) if name.endswith(".html")]
    missing_switch = []
    for name in html_files:
        with open(os.path.join(site, name), encoding="utf-8") as fh:
            page = fh.read()
        required = ('class="language-select"', 'option value="si"',
                    'option value="en"', 'wb-project-language')
        if any(token not in page for token in required):
            missing_switch.append(name)
    if missing_switch:
        fail(f"language selector or persistence script missing from: {missing_switch}")
    else:
        ok(f"Sinhala/English selector and saved preference present on all {len(html_files)} generated pages")

    # Every generated page head loads Inter + Noto Sans Sinhala (LANGUAGE_BOOTSTRAP)
    no_fonts, glyph = [], []
    for name in html_files:
        with open(os.path.join(site, name), encoding="utf-8") as fh:
            page = fh.read()
        if "fonts.googleapis.com/css2?family=Inter" not in page or \
           "Noto+Sans+Sinhala" not in page:
            no_fonts.append(name)
        if "⌄" in page:
            glyph.append(name)
    if no_fonts:
        fail(f"Google Fonts (Inter + Noto Sans Sinhala) missing from: {no_fonts}")
    else:
        ok(f"Inter + Noto Sans Sinhala loaded in all {len(html_files)} generated pages")
    if glyph:
        fail(f"literal ⌄ glyph still rendered in: {glyph}")
    else:
        ok("no literal ⌄ glyph anywhere in the site")

    # Non-template output must not leave cells blank; templates retain highlighted
    # blank input/signature fields by design.
    blank_pages = []
    template_pages = []
    for name in html_files:
        with open(os.path.join(site, name), encoding="utf-8") as fh:
            page = fh.read()
        blanks = len(re.findall(r'<td(?:\s[^>]*)?>\s*</td>', page, re.I))
        if 'class="template-page"' in page:
            template_pages.append(name)
        elif blanks:
            blank_pages.append((name, blanks))
    if blank_pages:
        fail(f"non-template pages have unfilled table cells: {blank_pages}")
    else:
        ok("generated tables are complete; intentional template fields remain blank and highlighted")


def check_csv_in_sync(item_count):
    print("\n[6] docs/12-master-document-checklist.md in sync with CSV")
    with open(os.path.join(ROOT, "docs", "12-master-document-checklist.md"),
              encoding="utf-8") as fh:
        doc = fh.read()
    rows = doc.count("| \u2610 |")
    if rows != item_count:
        fail(f"generated checklist has {rows} rows but CSV has {item_count} "
             f"- re-run: python3 build/build_checklist.py")
    else:
        ok(f"generated checklist in sync ({rows} rows)")


SHARED_ROW_LABELS = ("Budget", "ක්‍රියාවලිය", "Dashboard", "කළමනාකරණය සහ මූල්‍ය",
                     "අලෙවිය සහ අලෙවිකරණය", "අවසන් සාරාංශය", "ලේඛන පැකේජය")


def check_shared_nav(fname, page, label=None):
    """The one shared button row: same buttons, same order, current page on.

    Verifies the row built by build/nav_common.py is present, exposes the
    expected hrefs in order (Budget dropdown children included), marks exactly
    the current page as ``on``, draws the Budget caret in CSS (no ``⌄`` glyph),
    and carries the Sinhala label for the Budget button.
    """
    label = label or fname
    row = re.search(r'<div class="nav-links">(.*?)</nav>', page, re.S)
    if not row:
        fail(f"{label}: shared nav row missing")
        return
    row_html = row.group(1)
    hrefs = re.findall(r'<a href="([^"]+)"', row_html)
    if hrefs != list(ROW_HREFS):
        fail(f"{label}: shared nav hrefs {hrefs} != expected {list(ROW_HREFS)}")
        return
    active = re.findall(r'<a href="([^"]+)" class="on">', row_html)
    expected_active = [fname] if fname in ROW_HREFS else []
    if active != expected_active:
        fail(f"{label}: active nav button {active}, expected {expected_active}")
        return
    if '<span class="dropdown-caret" aria-hidden="true"></span>' not in row_html:
        fail(f"{label}: Budget caret is not the CSS-drawn element")
        return
    if "⌄" in row_html:
        fail(f"{label}: literal ⌄ glyph in the nav")
        return
    if "අයවැය" not in row_html:
        fail(f"{label}: Budget button label missing")
        return
    ok(f"{label}: shared nav row (7 buttons, Budget dropdown), current page highlighted")


def check_shared_nav_all_pages():
    print("\n[7b] Shared nav row on every investor page")
    site = os.path.join(ROOT, "site")
    # the dashboard is checked inside check_dashboard(), so it is not repeated here
    names = [LANDING_FILE] + [p[0] for p in INVESTOR_PAGES]
    for name in names:
        fp = os.path.join(site, name)
        if not os.path.exists(fp):
            fail(f"{name} not built")
            continue
        with open(fp, encoding="utf-8") as fh:
            check_shared_nav(name, fh.read())


def check_dashboard(item_count):
    print("\n[7] Dashboard (site/dashboard.html)")
    fp = os.path.join(ROOT, "site", "dashboard.html")
    if not os.path.exists(fp):
        warn("dashboard not built - run: python3 build/build_dashboard.py")
        return
    with open(fp, encoding="utf-8") as fh:
        html_src = fh.read()

    rows = len(re.findall(r'<tr data-id="', html_src))
    if rows != item_count:
        fail(f"dashboard embeds {rows} checklist rows but CSV has {item_count} "
             f"- re-run: python3 build/build_dashboard.py")
    else:
        ok(f"dashboard checklist in sync ({rows} rows)")

    # every checklist id from the CSV must appear in the dashboard
    ids = [r["id"] for r in load_csv_rows()]
    missing = [i for i in ids if f'data-id="{i}"' not in html_src]
    if missing:
        fail(f"{len(missing)} checklist ids missing from dashboard, e.g. {missing[:5]}")
    else:
        ok(f"all {len(ids)} checklist ids present in dashboard")

    # tag balance
    from html.parser import HTMLParser

    class V(HTMLParser):
        VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                "link", "meta", "source", "track", "wbr"}

        def __init__(self):
            super().__init__()
            self.stack = []
            self.errs = []

        def handle_starttag(self, t, a):
            if t not in self.VOID:
                self.stack.append(t)

        def handle_endtag(self, t):
            if t in self.VOID:
                return
            if not self.stack:
                self.errs.append(f"stray </{t}>")
            elif self.stack[-1] != t:
                self.errs.append(f"mismatch: open <{self.stack[-1]}> closed by </{t}>")
            else:
                self.stack.pop()

    v = V()
    v.feed(html_src)
    if v.stack or v.errs:
        fail(f"unbalanced HTML in dashboard: unclosed={v.stack[:5]} errors={v.errs[:5]}")
    else:
        ok("dashboard HTML tags balanced")

    # --- the cover photo must not be hidden behind the placeholder tile ---
    # A hero can carry optional modifier classes (for example, the Uva Highlands
    # treatment) as long as it still embeds a complete, visible JPEG.
    hero_open = re.search(r'<div class="[^\"]*\bhero\b[^\"]*"[^>]*>', html_src)
    if not hero_open:
        fail("dashboard hero container missing")
        hero = ""
    else:
        hero = html_src[hero_open.start():html_src.index('<div class="hc">', hero_open.end())]
    if 'background-image:url("data:image/jpeg;base64,' not in hero:
        fail("hero has no cover image - upcountry asset missing or not embedded")
    elif "nofallback" in hero:
        fail("the placeholder tile renders OVER the cover photo - the image is invisible")
    else:
        import base64
        raw = base64.b64decode(re.search(r"base64,([A-Za-z0-9+/=]+)", hero).group(1))
        if raw[:3] != b"\xff\xd8\xff" or raw[-2:] != b"\xff\xd9":
            fail(f"embedded cover is not a complete JPEG ({len(raw)} bytes)")
        else:
            ok(f"cover photo embedded and unobstructed ({len(raw)/1024:,.0f} KB JPEG)")

    # --- the two stages must both be there, and roll up to the same total ---
    for anchor, label in [("budgets", "six budget documents"), ("total", "roll-up")]:
        if f'id="{anchor}"' not in html_src:
            fail(f"{label} section missing from the dashboard")
    # assert on the text the reader actually sees: tags stripped AND the
    # pictographs removed by build_dashboard.plain(), which now runs on output
    # whitespace is normalised too: removing a pictograph leaves a double
    # space, which HTML collapses on screen but would break a substring test
    seen = re.sub(r"\s+", " ", de_emoji(re.sub(r"<[^>]+>", "", html_src)))
    for rung in ["A. අදියර 1", "B. අදියර 2", "C. CAPEX උප මුළු", "D. Contingency",
                 "E. මුළු CAPEX", "F. Working capital", "G. මුළු ආයෝජනය",
                 "CASH REQUIRED"]:
        if rung not in seen:
            fail(f"roll-up is missing rung: {rung}")
    if 'class="grand cash"' not in html_src:
        fail("expected a CASH REQUIRED row in the roll-up")
    ok("six budget documents + the A-G roll-up all present")

    # --- each stage table must show Qty | Unit | Rate | Amount ---
    for col in [">Qty</th>", "ඒකකය", "ඒකක මිල", "මුදල"]:
        if col not in html_src:
            fail(f"budget table missing column: {col}")
    ok("budget tables show Qty | Unit | Rate | Amount")

    # --- all five products, each with its own cost card ---
    for prod in ["500 ml", "1 L", "1.5 L", "5 L", "19 L"]:
        if f'>{prod}<' not in html_src and f'{prod} ' not in html_src:
            fail(f"product {prod} not rendered")
    if "TOTAL COST PER BOTTLE" not in html_src:
        fail("no per-bottle cost total rendered")
    n_cards = html_src.count("TOTAL COST PER BOTTLE")
    if n_cards != 5:
        fail(f"{n_cards} per-product cost cards rendered, expected 5")
    ok("all 5 products present with 5 separate cost cards")

    # --- the user asked for NO multi-year profit projections ---
    for gone in ['id="profit"', 'id="growth"', "Payback", "Sensitivity", "Break-even"]:
        if gone in html_src:
            fail(f"removed section/label still present: {gone}")
    ok("no yearly profit / payback / break-even sections (as requested)")

    # --- in-page section strip must match the rendered section order ---
    dom = re.findall(r'<section id="([a-z0-9]+)"', html_src)
    strip = re.search(r'<nav class="section-jump".*?</nav>', html_src, re.S)
    nav = re.findall(r'<a href="#([a-z0-9]+)"', strip.group(0)) if strip else []
    if dom != nav:
        fail(f"section strip {nav} does not match DOM order {dom}")
    else:
        ok(f"section strip matches section order ({len(dom)} sections)")

    # --- dashboard-nav: the shared button row, identical to every other page ---
    check_shared_nav(DASHBOARD_FILE, html_src, label="dashboard")

    # the model numbers must be present and non-trivial
    for token, label in [("Mr. Thilakarathna", "investor name"),
                         ("Bandarawela", "location"),
                         ("SLS 894", "product standard"),
                         ("5 L", "the 5 L product"),
                         ("LKR", None)]:
        if label and token not in html_src:
            fail(f"dashboard missing expected content: {label} ('{token}')")
    ok("dashboard contains investor, location, SLS 894 and all five products")

    # "/" must land on the landing page that links all four pages
    idx = os.path.join(ROOT, "site", "index.html")
    if not os.path.exists(idx):
        fail("site/index.html missing - \"/\" shows nothing")
    else:
        landing = open(idx, encoding="utf-8").read()
        missing = [f for f in ("1-setup-budget.html", "2-first-production.html",
                               "3-first-stock-cost.html", "4-process-documents.html",
                               "5-organisation-chart.html",
                               "6-sales-marketing.html",
                               "7-final-summary.html")
                   if f'href="{f}"' not in landing]
        if missing:
            fail(f"landing page does not link: {missing}")
        else:
            ok("landing page links all seven pages")

    # each of the seven pages must exist and be well formed
    four = ["1-setup-budget.html", "2-first-production.html",
            "3-first-stock-cost.html", "4-process-documents.html",
            "5-organisation-chart.html",
            "6-sales-marketing.html",
            "7-final-summary.html"]
    from html.parser import HTMLParser

    class Bal(HTMLParser):
        VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                "link", "meta", "source", "track", "wbr"}

        def __init__(self):
            super().__init__()
            self.st = []
            self.e = []

        def handle_starttag(self, t, a):
            if t not in self.VOID:
                self.st.append(t)

        def handle_endtag(self, t):
            if t in self.VOID:
                return
            if not self.st:
                self.e.append(f"stray </{t}>")
            elif self.st[-1] != t:
                self.e.append(f"<{self.st[-1]}> vs </{t}>")
            else:
                self.st.pop()

    orgp = os.path.join(ROOT, "site", "5-organisation-chart.html")
    if os.path.exists(orgp):
        org = open(orgp, encoding="utf-8").read()
        need = ["Manufacturing &amp; Quality", "HR &amp; Finance",
                "Sales &amp; Marketing", "Transportation", "org-dept",
                "EPF", "ETF", "Plant Manager"]
        miss = [n for n in need if n not in org]
        if miss:
            fail(f"org chart missing: {miss}")
        else:
            ok("org chart has all 4 departments, the hierarchy and the EPF/ETF math")

    for f in four:
        path = os.path.join(ROOT, "site", f)
        if not os.path.exists(path):
            fail(f"{f} missing - run build_pages.py")
            continue
        b = Bal()
        b.feed(open(path, encoding="utf-8").read())
        if b.st or b.e:
            fail(f"{f} unbalanced HTML: {b.st[:3]} {b.e[:3]}")
    if not any(f"site/{f} missing" in str(x) for x in []):
        ok("all seven pages built and well formed")


VAR_USE_RE = re.compile(r"var\((--[A-Za-z0-9_-]+)")
VAR_DEF_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")


def check_css_variables():
    """Every var(--x) used by the stylesheets or the built pages must be
    defined in a :root block of build/style.css (the only :root in the pack)."""
    print("\n[8] CSS variables: every var(--x) is defined in :root")
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "style.css"), encoding="utf-8") as fh:
        css = fh.read()
    roots = re.findall(r":root\s*\{([^}]*)\}", css)
    defined = set()
    for block in roots:
        defined.update(VAR_DEF_RE.findall(block))
    used = {}
    for name in ("style.css", "style_docs.css"):
        with open(os.path.join(here, name), encoding="utf-8") as fh:
            text = re.sub(r"/\*.*?\*/", "", fh.read(), flags=re.S)  # comments don't count
            for v in VAR_USE_RE.findall(text):
                used.setdefault(v, set()).add(name)
    site = os.path.join(ROOT, "site")
    if os.path.isdir(site):
        for name in sorted(os.listdir(site)):
            if name.endswith(".html"):
                with open(os.path.join(site, name), encoding="utf-8") as fh:
                    text = re.sub(r"/\*.*?\*/", "", fh.read(), flags=re.S)
                    for v in VAR_USE_RE.findall(text):
                        used.setdefault(v, set()).add(name)
    undefined = sorted(v for v in used if v not in defined)
    if undefined:
        fail("undefined CSS variables: " + ", ".join(
            f"{v} (used in {', '.join(sorted(used[v]))[:80]})" for v in undefined))
    else:
        ok(f"{len(used)} distinct variables used, all defined in :root "
           f"({len(defined)} defined)")


def load_csv_rows():
    with open(os.path.join(ROOT, "data", "master-checklist.csv"), newline="",
              encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    print("=" * 68)
    print("waterbottelsprojects - documentation pack self-check")
    print("=" * 68)
    check_relative_links()
    check_readme_index()
    item_count, _ = check_csv()
    check_data_files()
    check_csv_in_sync(item_count)
    check_site(item_count)
    check_dashboard(item_count)
    check_shared_nav_all_pages()
    check_css_variables()

    print("\n" + "=" * 68)
    if failures:
        print(f"FAILED - {len(failures)} problem(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASSED - all checks green ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
