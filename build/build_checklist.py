#!/usr/bin/env python3
"""
Generate docs/12-master-document-checklist.md from data/master-checklist.csv

Run:  python3 build/build_checklist.py
"""
import csv
import os
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_IN = os.path.join(ROOT, "data", "master-checklist.csv")
MD_OUT = os.path.join(ROOT, "docs", "12-master-document-checklist.md")

PRIORITY_ICON = {"Critical": "🔴", "Mandatory": "🟠", "High": "🟡", "Medium": "🔵", "Low": "⚪"}

HEADER = """# ⭐ MASTER CHECKLIST — සම්පූර්ණ ලේඛන සහ අවශ්‍යතා ලැයිස්තුව
# Complete Document & Requirements Register

> මෙම ලේඛනය `data/master-checklist.csv` ගොනුවෙන් **ස්වයංක්‍රීයව** උත්පාදනය කෙරේ.
> Auto-generated from [`data/master-checklist.csv`](../data/master-checklist.csv) — edit the CSV and re-run
> `python3 build/build_checklist.py`.

**අයිතම ගණන / Total items: __COUNT__**

## දර්ශක / Legend

| ලකුණ | අර්ථය |
|---|---|
| 🔴 **Critical** | මෙය අසමත් වුවහොත් ව්‍යාපෘතියම අවදානමේ — පළමුව කරන්න |
| 🟠 **Mandatory** | නීතියෙන් අනිවාර්යයි — නොමැතිව ක්‍රියාත්මක විය නොහැක |
| 🟡 **High** | ඉතා වැදගත් — කාලය/මුදල් විශාල ලෙස ඉතුරු කරයි |
| 🔵 **Medium** | නිර්දේශිත |
| ⚪ **Low** | අවශ්‍ය නම් |

---

## ක්ෂණික සාරාංශය — Phase අනුව | Phase summary

| Phase | අයිතම | 🔴 | 🟠 | 🟡 |
|---|---:|---:|---:|---:|
__PHASE_TABLE__

---

"""

FOOTER = """
---

## 📥 මෙය Excel / Google Sheets වෙත ගෙනයාම

`data/master-checklist.csv` ගොනුව විවෘත කර Google Sheets වෙත ආයාත කරන්න. එවිට:
1. `Status` තීරුවක් එක් කරන්න (Not started / In progress / Received / N/A)
2. `Owner` තීරුවක් එක් කරන්න (ඔබ / ආයෝජක / නීතිඥ / QA Manager)
3. `Target date` සහ `Actual date` තීරු එක් කරන්න
4. `File path / link` තීරුවක් එක් කර Google Drive වෙත සම්බන්ධ කරන්න

**👉 ආයෝජකයාට සතිපතා මෙම ලැයිස්තුව යවන්න — එය ව්‍යාපෘතියේ ප්‍රගති වාර්තාව වේ.**

---

**⬅️ ආපසු:** [Phase 10 — වෙළඳපොළට පිවිසීම](11-phase-10-launch-market.md) | [මුල් පිටුව](../README.md)
**➡️ ඊළඟට:** [මූලධන ආයෝජනය සහ අයවැය](13-capital-investment-budget.md)
"""


def main():
    with open(CSV_IN, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    # ---- phase summary ----
    phase_counts = OrderedDict()
    for r in rows:
        p = r["phase"]
        if p not in phase_counts:
            phase_counts[p] = {"total": 0, "Critical": 0, "Mandatory": 0, "High": 0}
        phase_counts[p]["total"] += 1
        if r["priority"] in phase_counts[p]:
            phase_counts[p][r["priority"]] += 1

    phase_table = "\n".join(
        f"| **{p}** | {c['total']} | {c['Critical']} | {c['Mandatory']} | {c['High']} |"
        for p, c in phase_counts.items()
    )
    total = len(rows)
    phase_table += f"\n| **මුළු / TOTAL** | **{total}** | " + \
        f"**{sum(c['Critical'] for c in phase_counts.values())}** | " + \
        f"**{sum(c['Mandatory'] for c in phase_counts.values())}** | " + \
        f"**{sum(c['High'] for c in phase_counts.values())}** |"

    out = [HEADER.replace("__COUNT__", str(total)).replace("__PHASE_TABLE__", phase_table)]

    # ---- grouped by phase, then category ----
    by_phase = OrderedDict()
    for r in rows:
        by_phase.setdefault(r["phase"], OrderedDict()).setdefault(r["category"], []).append(r)

    for phase, cats in by_phase.items():
        out.append(f"\n# 📁 {phase}\n")
        for cat, items in cats.items():
            out.append(f"\n## {cat}\n")
            out.append(
                "| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |"
            )
            out.append("|:--:|---|---|---|---|---|---|:--:|---|")
            for r in items:
                icon = PRIORITY_ICON.get(r["priority"], "")
                name = (f'<span class="en"><strong>{r["item_en"]}</strong></span>'
                        f'<br><sub class="si">{r["item_si"]}</sub>')
                note = r["notes"].replace("|", "/") if r["notes"] else "—"
                out.append(
                    f"| ☐ | `{r['id']}` | {name} | {r['authority_or_source']} | {r['when']} | "
                    f"{r['cost_lkr']} | {r['validity']} | {icon} {r['priority']} | {note} |"
                )
        out.append("")

    out.append(FOOTER)
    with open(MD_OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))

    print(f"[ok] wrote {MD_OUT}")
    print(f"[ok] {total} items across {len(phase_counts)} phases, "
          f"{len({c for cats in by_phase.values() for c in cats})} categories")


if __name__ == "__main__":
    main()
