# 💧 බෝතල් කළ පානීය ජල කර්මාන්ත ශාලාව — සම්පූර්ණ ව්‍යාපෘති ලේඛන පැකේජය
# Bottled Drinking Water Manufacturing Plant — Complete Project Documentation Pack

> **ස්ථානය / Location:** බණ්ඩාරවෙල, බදුල්ල දිස්ත්‍රික්කය, ඌව පළාත — Bandarawela, Badulla District, Uva Province
> **ව්‍යාපෘති වර්ගය / Structure:** ආයෝජක හවුල්කාරිත්වයක් සහිත පෞද්ගලික සමාගමක් (Private Limited Company with an investor partnership)
> **සකස් කළ දිනය / Prepared:** 2026-10-10
> **අනුවාදය / Version:** 1.2

---

## ✅ තහවුරු කළ තීරණ | LOCKED DECISIONS (2026-10-10)

| තීරණය | විස්තරය |
|---|---|
| 🎯 **නිෂ්පාදනය** | **"බෝතල් කළ පානීය ජලය / Bottled Drinking Water" — SLS 894** |
| ❌ **නොකරයි** | Natural Mineral Water (SLS 1038) — සැබෑ උල්පතක් අවශ්‍ය බැවින් |
| 💧 **මූලාශ්‍රය** | නළ ළිඳ / භූගත ජලය (deep tube well) |
| 🔬 **පිරිපහදුව** | සම්පූර්ණ filtration — **MGSF → ACF → Softener → Micron → RO → UV → Ozone → 0.2µm** |
| 🏷️ **ලේබල්** | "Bottled Drinking Water" — "Natural Mineral Water" / "Spring Water" **භාවිත කළ නොහැක** |
| 💵 **ආයෝජකයා** | **Mr. Thilakarathna** — මුදල් සපයයි; **ඉඩම පමණක්** දැනට ඇති වත්කමයි |
| 🏭 **ධාරිතාව** | 6,000 BPH (බෝතල් පැයට) — PET 500ml/1L/1.5L + 19L returnable |
| 💰 **අයවැය** | ආරම්භක CAPEX **Rs 193.11M** + පළමු නිෂ්පාදන **Rs 3.43M** = **මුළු ආයෝජනය Rs 196.53M** · මුදලින් **Rs 184.53M** (ඉඩම in-kind) · working capital buffer Rs 28M වෙනම |
| 🍶 **නිෂ්පාදන** | **500 ml · 1 L · 1.5 L · 5 L · 19 L** — එකක පිරිවැය Rs 26.70 / 35.75 / 42.80 / 76.80 / 83.00 |

👉 **[තීරණ වාර්තාව / Decision log](docs/21-decisions-and-assumptions.md)** · **[ජල පිරිපහදු පද්ධතිය / Treatment train](docs/20-water-treatment-train.md)**

---

## 🌐 භාෂාව තෝරන්න | LANGUAGE SELECTOR

සෑම website page එකකම ඉහළ ඇති **භාෂාව / Language** selector එකෙන් සිංහල හෝ English තෝරන්න. තේරීම අනෙක් pages වෙතත් මතක තබා ගනී. පරිවර්තනයක් නොමැති වචනයක්/field එකක් අතුරුදහන් නොකර, පවතින මුල් භාෂාවේ fallback එක පෙන්වයි.

Use the **භාෂාව / Language** selector at the top of any generated page. Your choice is remembered across pages. Where a translation is not available, the source wording remains visible as a fallback instead of being hidden.

**Tables / වගු:** අදාළ නොවන cells සඳහා `—`; තහවුරු කළ යුතු හෝ පුරවන්නට ඇති තැන් highlight කර ඇත. නීතිමය templates වල අත්සන් සහ පෞද්ගලික තොරතුරු සඳහා හිස් fields හිතාමතා තබා ඇත.

---

## 📄 පිටු 7 — ආයෝජකයා ඉල්ලූ පිටු | THE SEVEN PAGES

> **බලන්න / View:** `site/index.html` — පිටු සියල්ලට සබැඳි ඇත · **Build:** `.venv/bin/python build/build_all.py` (Windows: `.venv\Scripts\python.exe build\build_all.py`)

| # | පිටුව | අන්තර්ගතය |
|---|---|---|
| 1 | [`1-setup-budget.html`](site/1-setup-budget.html) | ආරම්භයේ සිට කර්මාන්ත ශාලාව ලියාපදිංචි වී, ගොඩනැගිලි ඉදිවී, යන්ත්‍ර සවිකර, වැඩ ආරම්භ වන දිනය දක්වා — **සම්පූර්ණ අයවැය**, කාර්යාල උපකරණ සහිතව |
| 2 | [`2-first-production.html`](site/2-first-production.html) | නිෂ්පාදනය ආරම්භ වන දිනයේ සිට පළමු order stock එක අවසන් වන තෙක් — බෝතල්, ලේබල්, පිරවීම, සේවක පඩි |
| 3 | [`3-first-stock-cost.html`](site/3-first-stock-cost.html) | ඒ stock එකේ **බෝතලයක පිරිවැය**, නිශ්චිත ප්‍රමාණ සහිතව (500 ml 5,000 · 1 L 3,000 · 1.5 L 3,000 · 5 L 1,000 · 19 L 150) |
| 4 | [`4-process-documents.html`](site/4-process-documents.html) | ක්‍රියාවලිය පියවරෙන් පියවර · එක් එක් පියවරට අවශ්‍ය ලේඛන · ගතවන කාලය (පියවර 24 · මාස 14–20) |
| 5 | [`5-organisation-chart.html`](site/5-organisation-chart.html) | **කර්මාන්ඩල සටහන** — දෙපාර්තමේන්තු 4ක් අනුව රැකියා ධූරාවලිය, වැටුප් + EPF/ETF සහිතව (43 දෙනා · Rs 2,421,900/මාස) |
| 6 | [`6-sales-marketing.html`](site/6-sales-marketing.html) | **Factory → Distributor → Retail** මිල පඩිපෙළ · නිෂ්පාදනය අනුව ලාභය · පළමු stock එකේ ලාභය |
| 7 | [`7-final-summary.html`](site/7-final-summary.html) | **අවසන් සාරාංශය** — මුළු ආයෝජනය · දවසට විකුණිය යුතු ප්‍රමාණය · ආයෝජනය ආපසු ලැබෙන මාස · අවුරුද්දක ඉලක්කය |

### 🎯 ප්‍රධාන ඉලක්කම් / Headline numbers — [පිටුව 7](site/7-final-summary.html)

| | |
|---|---|
| 💼 **මුළු ආයෝජනය / Total investment** | **Rs 196,532,230** = ආරම්භක Rs 193,105,125 + පළමු නිෂ්පාදන Rs 3,427,105 |
| 💵 මුදලින් අවශ්‍ය / Cash to raise | **Rs 184,532,230** — ඉඩම Rs 12M Mr. Thilakarathna ගේ in-kind දායකත්වයකි |
| 🏦 නිර්දේශිත working capital buffer | Rs 28,000,000 → බැංකුවේ තිබිය යුත්තේ **Rs 212,532,230** |
| 📦 පළමු stock එකේ ලාභය | **Rs 321,600** (බෝතල් 12,150 · **එකක Rs 26.47** · 41.2%) |
| 🔴 **දවසට විකුණිය යුතු අවම** | **බෝතල් 13,984** (මාසික 349,612 = ධාරිතාවෙන් 29%) |
| 🎯 **අවුරුද්දක් තුළ ආපසු ලබා ගැනීමට** | දවසට **නිෂ්පාදනය 38,734 · විකිණීම 38,734** (ධාරිතාවෙන් 81% — එක shift එකකින් හැකියි) |
| ⏳ 100% ධාරිතාවේදී ආපසු | **මාස 8.7** (බදු පෙර) · මාස 12.5 (බදු 30% පසු) |

> ⚠️ බදු 30% සලකා **අවුරුද්දක්** තුළ ආපසු ලබා ගැනීමට දවසට බෝතල් 49,341ක් (ධාරිතාවෙන් 103%) අවශ්‍යයි — එක shift එකකින් නොහැක. බදු පසු ආපසු ලැබෙන්නේ මාස 15.8කින්.

---


## 📊 ⭐ ව්‍යාපෘති DASHBOARD — මුදල්, බෝතල් Qty, ලාභය | One-page panel

> **බලන්න / View:** `site/dashboard.html` — සම්පූර්ණ dashboard එක. Site landing page එක `site/index.html` හි ඇත.
> **Build:** `.venv/bin/python build/build_all.py` (සියල්ල එකවර; Windows: `.venv\Scripts\python.exe build\build_all.py`) · **ලේඛන / Docs:** `site/docs.html`

> **GitHub Pages:** Build and deployment source එක **GitHub Actions** ලෙස සකසන්න. `.github/workflows/deploy-pages.yml` මඟින් `site/` build කර publish කරයි; website home එක landing page වන අතර dashboard එක `/dashboard.html` හි ඇත.

මුළු ව්‍යාපෘතියම **එක පිටුවක** — කියවන්නට පහසු, ඕනෑම කෙනෙකුට තේරෙන ආකාරයට:

| අංශය | අන්තර්ගතය |
|---|---|
| 1️⃣ සාරාංශය | Mr. Thilakarathna · ඉඩම · **නිෂ්පාදන 5** · ප්‍රධාන පිරිවැය 2 |
| 2️⃣ ව්‍යාපෘතිය | දැනට ඇත්තේ ඉඩම පමණයි — ඉතිරි සියල්ල මුල සිට |
| 3️⃣ පිරිපහදු ක්‍රියාවලිය | 8 පියවර · 7 CCPs · SLS 894 |
| 4️⃣ නිෂ්පාදන 5 | 500 ml · 1 L · 1.5 L · **5 L** · 19 L — වෙන වෙනම Qty |
| 5️⃣ **අදියර 1** | 💰 **පටන් ගත් දවසේ සිට ෆැක්ටරි එක ඕපන් කරන තෙක්** — Rs 75.15M |
| 6️⃣ **අදියර 2** | 🏭 **ෆැක්ටරි එක ඕපන් සිට නිෂ්පාදනයට සූදානම් වන තෙක්** — Rs 86.80M |
| 7️⃣ මුළු ආයෝජනය | Dashboard A → G: **Rs 214.24M** (CAPEX incl. contingency + Rs 28M working capital; cash Rs 202.24M). පිටු 1–7: **Rs 196.53M** (setup + first production; working capital හැර) |
| 8️⃣ **බෝතලයක පිරිවැය** | 🧮 **නිෂ්පාදන 5ම වෙන වෙනම** — අයිතම් 10 බැගින් |
| 9️⃣ අමුද්‍රව්‍ය + ලේබල් | මාසික Qty — wastage සහිතව |
| 🔟 ලේඛන ලැයිස්තුව | අයිතම් 160 — tick කරන්න, progress bar එකක් සමඟ |
| 1️⃣1️⃣–1️⃣2️⃣ | කාලසටහන · ප්‍රධාන අවදානම් |

> ⚠️ **Budget reconciliation අවශ්‍යයි:** පිටු 1–7 හි cash Rs 184.53223M + Rs 28M buffer = **Rs 212.53223M**; Dashboard Option B cash requirement **Rs 202.2425M**. වෙනස **Rs 10.28973M** — budget දෙකේ ඇතුළත් අයිතම/පරාස එකිනෙකට වෙනස් බැවින් funding තීරණයකට පෙර line items එකඟ කරගන්න.

> ⛔ **මෙහි නැත්තේ:** අවුරුදු ගණන් ලාභ/පාඩු ප්‍රක්ෂේපණ, payback, break-even, sensitivity.
> ඔබ ඉල්ලූ පරිදි dashboard එක **නිෂ්පාදනය ආරම්භ කරන තැනින් නවතී.** ඒවා පසුව වෙනම සාදමු.

---

## 🎯 මෙම පැකේජයෙන් ලැබෙන්නේ මොනවාද? / What is in this pack?

ඔබ ඉල්ලූ පරිදි — **"1st Registration Document එක ඉඳන්"**, එනම් සමාගම ලියාපදිංචි කිරීමේ පළමු ලේඛනයේ සිට කර්මාන්ත ශාලාව විවෘත කර නිෂ්පාදනය ආරම්භ කරන තෙක් **අවශ්‍ය සියලුම මූලික ලේඛන, අවශ්‍ය දේවල් (උපකරණ/සේවා), සහ සේවා සපයන්නන්** — වෙන වෙනම, පිළිවෙළින්, ලැයිස්තුගත කර ඇත.

As you asked — from the **very first registration document** (company incorporation) right up to opening the plant and starting production, every required document, every required item and every required service is listed **separately and in order**.

---

## 📚 ලේඛන සිතියම / Document Map

### කොටස 1 — පියවර 10 ව්‍යාපෘති මාර්ග සිතියම (Phase-by-phase requirements)

| # | ලේඛනය / Document | අන්තර්ගතය / Contents |
|---|---|---|
| 01 | [Phase 0 — ආයෝජක එකඟතා / Investor & MOU](docs/01-phase-0-investor-mou.md) | ආයෝජක පරීක්ෂණ ලේඛන, MOU, Term Sheet, හවුල්කාරිත්ව ගිවිසුම් |
| 02 | [Phase 1 — **සමාගම ලියාපදිංචි කිරීම (1st Registration)**](docs/02-phase-1-company-registration.md) | eROC, Form 1/18/19, Articles of Association, TIN, බැංකු ගිණුම |
| 03 | [Phase 2 — ඉඩම සහ ගොඩනැඟිල්ල / Land & Premises](docs/03-phase-2-land-premises.md) | ඔප්පු, සමීක්ෂණ සැලසුම, UDA/ප්‍රා.ස. අනුමැති, Certificate of Conformity |
| 04 | [Phase 3 — ජල මූලාශ්‍රය / Water Source (WRB)](docs/04-phase-3-water-source-wrb.md) | Gazette 2010/23, ළිඳ/නළ ළිඳ, SLS 614:2013 පරීක්ෂණ |
| 05 | [Phase 4 — කර්මාන්ත ශාලා ඉදිකිරීම / Factory Construction](docs/05-phase-4-factory-construction.md) | ආහාර ශ්‍රේණියේ සැලසුම, filling room, utilities, ETP |
| 06 | [Phase 5 — යන්ත්‍රෝපකරණ සහ උපකරණ / Machinery & Equipment](docs/06-phase-5-machinery-equipment.md) | සම්පූර්ණ machine list, lab equipment, spare parts, consumables |
| 07 | [Phase 6 — **සෞඛ්‍ය අමාත්‍යාංශ ලියාපදිංචිය (FCAU)**](docs/07-phase-6-moh-fcau-bottled-water-registration.md) | Food (Bottled Water Registration) Regulations 2011 — සම්පූර්ණ ලේඛන ලැයිස්තුව |
| 08 | [Phase 7 — SLSI සහතික කිරීම / SLSI Certification](docs/08-phase-7-slsi-certification.md) | SLS 894, SLS 1038, SLS 1336:2008 (PET බෝතල්), SLS Mark |
| 09 | [Phase 8 — පරිසර අනුමැති / Environmental (CEA)](docs/09-phase-8-environment-cea.md) | EPL, Scheduled Waste Licence, discharge standards |
| 10 | [Phase 9 — බදු, ශ්‍රම, වෙනත් නීතිමය / Tax, Labour, Statutory](docs/10-phase-9-tax-labour-statutory.md) | TIN, VAT, SSCL, EPF/ETF, Factory Ordinance, Annual Return |
| 11 | [Phase 10 — වෙළඳපොළට පිවිසීම / Launch & Market](docs/11-phase-10-launch-market.md) | Trademark, Barcode, Label, Distribution, Export, BOI |

### කොටස 2 — එක්තැන් කරන ලද මූලික ලේඛන (Consolidated references)

| # | ලේඛනය / Document | අන්තර්ගතය / Contents |
|---|---|---|
| 12 | [**MASTER CHECKLIST — සම්පූර්ණ ලේඛන ලැයිස්තුව**](docs/12-master-document-checklist.md) | ලේඛන **90+** එකම තැනක — Phase, නිකුතු කරන ආයතනය, කාලය, වියදම, වලංගු කාලය |
| 13 | [මූලධන ආයෝජනය සහ අයවැය / Capital Investment Budget](docs/13-capital-investment-budget.md) | CAPEX / OPEX, කුඩා–මධ්‍යම–විශාල යන විකල්ප 3 |
| 14 | [ව්‍යාපෘති කාල සටහන / Project Timeline](docs/14-project-timeline.md) | මාස 12–18 Gantt සැලැස්ම |
| 15 | [ආයෝජක Due Diligence පැකේජය / Investor Due Diligence](docs/15-investor-due-diligence-pack.md) | ආයෝජකයාට පෙන්විය යුතු ලේඛන |
| 16 | [අවදානම් ලේඛනය / Risk Register](docs/16-risk-register.md) | අවදානම් 20ක් + අඩු කිරීමේ ක්‍රියාමාර්ග |
| 17 | [ආයතන සහ සේවා සපයන්නන් / Agency & Service Directory](docs/17-agency-service-directory.md) | කවුරුන් වෙත කුමක් ලබාගන්නේද — සම්පූර්ණ ලැයිස්තුව |
| 18 | [නැවුම් කිරීමේ කාලසටහන / Renewal & Compliance Calendar](docs/18-renewal-compliance-calendar.md) | මාසික / වාර්ෂික / වසර 3ක යුතුකම් |
| 19 | [ලේබල් අවශ්‍යතා / Label Requirements](docs/19-label-requirements.md) | Food (Labelling & Advertising) Regulations 2005 |
| 20 | [💧 **ජල පිරිපහදු පද්ධතිය / Water Treatment Train**](docs/20-water-treatment-train.md) | ⭐ සම්පූර්ණ **filtration දාමය** — එක් එක් පෙරහන මොනවා ඉවත් කරයිද, CCP 7ක්, media මාරු කිරීමේ කාලසටහන, RO reject, **bromate අවදානම** |
| 21 | [📋 **තීරණ සහ උපකල්පන / Decision & Assumption Log**](docs/21-decisions-and-assumptions.md) | ⭐ තහවුරු කළ තීරණ, විවෘත ප්‍රශ්න 6ක්, ධාරිතාව පිළිබඳ නිර්දේශය, Phase 1→4 වර්ධන සැලැස්ම |

### කොටස 3 — සූදානම් කරගත හැකි ආකෘති පත්‍ර (Ready-to-use templates)

| ලේඛනය / Template |
|---|
| [MOU / Term Sheet — ආයෝජක අන්‍යෝන්‍ය අවබෝධතා ගිවිසුම](templates/01-MOU-term-sheet.md) |
| [Shareholders Agreement — Heads of Terms](templates/02-shareholders-agreement-heads-of-terms.md) |
| [Board Resolution — සමාගම ලියාපදිංචි කිරීම සඳහා](templates/03-board-resolution-incorporation.md) |
| [ජල පරීක්ෂණ ඉල්ලුම් ලිපිය (SLSI/ITI)](templates/04-water-source-test-request.md) |
| [FCAU අයදුම්පත සඳහා ආවරණ ලිපිය](templates/05-fcau-application-cover-letter.md) |

### කොටස 4 — දත්ත ගොනු (Machine-readable data)

| ගොනුව / File | භාවිතය / Use |
|---|---|
| [`data/master-checklist.csv`](data/master-checklist.csv) | Excel/Google Sheets වෙත ගෙන යා හැක — progress tracking |
| [`data/capex-estimate.csv`](data/capex-estimate.csv) | යන්ත්‍රෝපකරණ + ඉදිකිරීම් අයවැය |
| [`data/renewals.csv`](data/renewals.csv) | නැවුම් කිරීමේ දින |

---

## 🚀 ඉක්මන් ආරම්භය / Quick Start — පළමු පියවර 7

1. **ඉඩම තහවුරු කරගන්න** — අවම **පර්චස් 160** (FCAU අවශ්‍යතාව). ඔප්පුව/බදු ගිවිසුම (වසර 5+) ලියාපදිංචි කරන්න.
2. **ජල මූලාශ්‍රය පරීක්ෂා කරන්න** — කර්මාන්ත ශාලාව ඉදිකිරීමට **පෙර** ළිඳ සම්පූර්ණ කර **SLS 614:2013** පරීක්ෂණ වාර්තාව ලබාගන්න. මෙය අසමත් වුවහොත් ලියාපදිංචිය නොලැබේ.
3. **MOU එක අත්සන් කරන්න** — ආයෝජකයා සමඟ කොටස්, පාලනය, පිටවීමේ කොන්දේසි.
4. **සමාගම ලියාපදිංචි කරන්න (eROC)** — මෙයයි **1st Registration Document**.
5. **TIN + බැංකු ගිණුම** ලබාගන්න.
6. **ගොඩනැඟිලි අනුමැති + යන්ත්‍ර ඇණවුම්** එකවර ආරම්භ කරන්න.
7. **FCAU අයදුම්පත** → SLSI audit → තාවකාලික ලියාපදිංචිය.

---

## ⚠️ වැදගත් සටහන / Important Note

මෙම ලේඛනය **මාර්ගෝපදේශයකි (guidance document)**, නීතිමය උපදෙසක් නොවේ. රජයේ ගාස්තු, නීති සහ අවශ්‍යතා වෙනස් විය හැක. එක් එක් අයිතමය සඳහා **"තහවුරු කරන්න / Verify"** ලෙස සලකුණු කර ඇති ස්ථානවලදී අදාළ ආයතනයෙන් (DRC, FCAU, SLSI, CEA, WRB, IRD, ප්‍රාදේශීය ලේකම්/ප්‍රා.ස.) ඍජුවම තහවුරු කරගන්න.

This is a **guidance document**, not legal advice. Verify all fees and requirements directly with the issuing authority before committing money.

---

## 🖥️ ලේඛන පිරික්සීම / Browse the pack

`site/` තුළ ස්ථිතික වෙබ් අඩවියක් උත්පාදනය කර ඇත. පළමු වරට build කිරීමට Python 3 සහ `requirements.txt` හි dependency ස්ථාපනය කරන්න:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build/build_all.py
```

Windows PowerShell සඳහා:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe build\build_all.py
```

Build එකෙන් පසු site එක නැරඹීමට:

```bash
cd site && python3 -m http.server 8000 --bind 0.0.0.0
```
