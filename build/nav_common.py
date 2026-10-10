#!/usr/bin/env python3
"""The one shared navigation button row for the investor-facing pages.

Used by:
  build/pages_common.py   -> landing page (index.html) and the seven pages
  build/build_dashboard.py -> site/dashboard.html

Every page gets the same row, in the same order, with the current page
highlighted. The row is:

  අයවැය (Budget ▾) · ක්‍රියාවලිය · Dashboard · කළමනාකරණය සහ මූල්‍ය ·
  අලෙවිය සහ අලෙවිකරණය · අවසන් සාරාංශය · ලේඛන පැකේජය

The caret on the Budget button is drawn in CSS (.dropdown-caret), never a
text glyph.
"""
import html
import re

_NAV_BLOCK = re.compile(r"<nav\b.*?</nav>", re.S)
_BETWEEN_TAGS = re.compile(r">\s+<")


def compact_nav(document):
    """Remove formatting whitespace between tags inside every <nav> block.

    Navs must contain only their buttons: no stray whitespace text nodes and
    no pictographs. Applied by every page builder after rendering.
    """
    return _NAV_BLOCK.sub(lambda m: _BETWEEN_TAGS.sub("><", m.group(0)), document)

# (file, page number, Sinhala label, English label) - seven investor pages.
PAGES = [
    ("1-setup-budget.html", "1", "ආරම්භක අයවැය", "Setup Budget"),
    ("2-first-production.html", "2", "පළමු නිෂ්පාදන අයවැය", "First Production Budget"),
    ("3-first-stock-cost.html", "3", "පළමු stock එකේ පිරිවැය", "First Stock Cost"),
    ("4-process-documents.html", "4", "ක්‍රියාවලිය", "Process"),
    ("5-organisation-chart.html", "5", "කළමනාකරණය සහ මූල්‍ය", "Management & Finance"),
    ("6-sales-marketing.html", "6", "අලෙවිය සහ අලෙවිකරණය", "Sales & Marketing"),
    ("7-final-summary.html", "7", "අවසන් සාරාංශය", "Final Summary"),
]

LANDING_FILE = "index.html"
DASHBOARD_FILE = "dashboard.html"
DOCS_FILE = "docs.html"

BUDGET_SI, BUDGET_EN = "අයවැය", "Budget"
DASHBOARD_LABEL = ("Dashboard", "Dashboard")
DOCS_LABEL = ("ලේඛන පැකේජය", "Document Pack")

# Pages that live inside the Budget dropdown (the first three).
BUDGET_FILES = [p[0] for p in PAGES[:3]]

# The flat, ordered list of hrefs the row must expose (dropdown children
# included, in the order they appear on screen). check_links.py verifies this.
ROW_HREFS = (BUDGET_FILES + [PAGES[3][0], DASHBOARD_FILE]
             + [p[0] for p in PAGES[4:]] + [DOCS_FILE])


def _esc(text):
    return html.escape(str(text), quote=False)


def _link(fname, si, en, active):
    on = ' class="on"' if fname == active else ""
    return (f'<a href="{fname}"{on}><span class="si">{_esc(si)}</span>'
            f'<span class="en">{_esc(en)}</span></a>')


def nav_links(active=""):
    """Return the shared ``<div class="nav-links">`` row.

    ``active`` is the file name of the current page (e.g. ``"dashboard.html"``
    or ``"index.html"`` for the landing page). That page's button is marked
    ``class="on"``; the Budget dropdown is marked active and opened when one of
    its three pages is current.
    """
    budget_open = " open" if active in BUDGET_FILES else ""
    budget_on = " on" if budget_open else ""
    out = ['<div class="nav-links">',
           f'<details class="nav-dropdown budget-dropdown"{budget_open}>',
           f'<summary class="budget-trigger{budget_on}">'
           f'<span class="si">{BUDGET_SI}</span><span class="en">{BUDGET_EN}</span>'
           '<span class="dropdown-caret" aria-hidden="true"></span>'
           f'<span class="budget-count" aria-label="{len(PAGES[:3])} pages">{len(PAGES[:3])}</span></summary>',
           '<div class="dropdown-menu">']
    for fname, _num, si, en in PAGES[:3]:
        out.append(_link(fname, si, en, active))
    out.append('</div></details>')

    fname, _num, si, en = PAGES[3]
    out.append(_link(fname, si, en, active))
    out.append(_link(DASHBOARD_FILE, *DASHBOARD_LABEL, active))
    for fname, _num, si, en in PAGES[4:]:
        out.append(_link(fname, si, en, active))
    out.append(_link(DOCS_FILE, *DOCS_LABEL, active))
    out.append('</div>')
    return "".join(out)
