#!/usr/bin/env python3
"""The main call-to-action row shared by every hero.

Used by:
  build/pages_common.py    -> landing page (index.html) and the seven pages
  build/build_dashboard.py -> site/dashboard.html

Targets (check_links.py verifies these from CTA_BY_PAGE):
  landing     primary -> #project-sections (scrolls)   secondary -> dashboard.html
  dashboard   primary -> dashboard.html#dash           secondary -> index.html
  pages 1-7   primary -> dashboard.html                secondary -> index.html

The primary button is the oversized golden pill (styled in style.css); the
secondary one is a glass button.
"""
from nav_common import LANDING_FILE, DASHBOARD_FILE

PAGE_PRIMARY = ("dashboard.html", "ව්‍යාපෘති Dashboard විවෘත කරන්න", "Open the dashboard")
PAGE_SECONDARY = (LANDING_FILE, "මුල් පිටුවට", "Back to overview")

# (primary href, primary si, primary en, secondary href, secondary si, secondary en)
CTA_BY_PAGE = {
    LANDING_FILE: ("#project-sections", "ව්‍යාපෘති සාරාංශය", "Project overview",
                   DASHBOARD_FILE, "සම්පූර්ණ Dashboard", "Open full dashboard"),
    DASHBOARD_FILE: ("dashboard.html#dash", "ව්‍යාපෘති සාරාංශය බලන්න", "View project summary",
                     LANDING_FILE, "කොටස් 7 වෙත යන්න", "Explore the seven sections"),
}
for _fname in ("1-setup-budget.html", "2-first-production.html", "3-first-stock-cost.html",
               "4-process-documents.html", "5-organisation-chart.html",
               "6-sales-marketing.html", "7-final-summary.html"):
    CTA_BY_PAGE[_fname] = PAGE_PRIMARY + PAGE_SECONDARY


def _button(cls, href, si, en, arrow=False):
    tail = '<b class="btn-arrow" aria-hidden="true">→</b>' if arrow else ""
    return (f'<a class="btn {cls}" href="{href}"><span class="si">{si}</span>'
            f'<span class="en">{en}</span>{tail}</a>')


def hero_actions(fname):
    """Return the ``<div class="hero-actions">`` row for the page ``fname``."""
    p_href, p_si, p_en, s_href, s_si, s_en = CTA_BY_PAGE[fname]
    return ('<div class="hero-actions">'
            + _button("btn-primary", p_href, p_si, p_en, arrow=True)
            + _button("btn-secondary", s_href, s_si, s_en)
            + '</div>')
