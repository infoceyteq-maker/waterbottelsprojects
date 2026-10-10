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
            ok(f"data/{name}: {len(rows)} rows, {len(rows[0])} columns")


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

    # the model numbers must be present and non-trivial
    for token, label in [("Mr. Thilakarathna", "investor name"),
                         ("Bandarawela", "location"),
                         ("SLS 894", "product standard"),
                         ("Break-even", "break-even block"),
                         ("LKR", None)]:
        if label and token not in html_src:
            fail(f"dashboard missing expected content: {label} ('{token}')")
    ok("dashboard contains investor, location, SLS 894 and break-even content")

    # the dashboard must also be the site root, so "/" shows it
    idx = os.path.join(ROOT, "site", "index.html")
    if not os.path.exists(idx):
        fail("site/index.html missing - \"/\" would not show the dashboard")
    elif os.path.getsize(idx) != os.path.getsize(fp):
        fail("site/index.html is not a copy of dashboard.html - "
             "\"/\" shows the docs index, not the dashboard. Re-run build_site.py")
    else:
        ok(f"site/index.html == dashboard.html, so \"/\" lands on the dashboard "
           f"({os.path.getsize(idx)/1024:,.0f} KB)")


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

    print("\n" + "=" * 68)
    if failures:
        print(f"FAILED - {len(failures)} problem(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASSED - all checks green ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
