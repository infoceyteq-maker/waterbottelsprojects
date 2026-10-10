# ⭐ MASTER CHECKLIST — සම්පූර්ණ ලේඛන සහ අවශ්‍යතා ලැයිස්තුව
# Complete Document & Requirements Register

> මෙම ලේඛනය `data/master-checklist.csv` ගොනුවෙන් **ස්වයංක්‍රීයව** උත්පාදනය කෙරේ.
> Auto-generated from [`data/master-checklist.csv`](../data/master-checklist.csv) — edit the CSV and re-run
> `python3 build/build_checklist.py`.

**අයිතම ගණන / Total items: 160**

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
| **0 - Investor** | 10 | 2 | 4 | 3 |
| **1 - Company** | 18 | 0 | 16 | 1 |
| **2 - Land** | 18 | 1 | 10 | 4 |
| **3 - Water** | 15 | 5 | 8 | 2 |
| **4 - Factory** | 15 | 0 | 12 | 3 |
| **5 - Machinery** | 22 | 2 | 13 | 7 |
| **6 - MoH FCAU** | 17 | 2 | 15 | 0 |
| **7 - SLSI** | 9 | 0 | 8 | 1 |
| **8 - Environment** | 10 | 0 | 6 | 2 |
| **9 - Tax/Statutory** | 14 | 1 | 12 | 1 |
| **10 - Launch** | 12 | 2 | 4 | 5 |
| **මුළු / TOTAL** | **160** | **15** | **108** | **29** |

---



# 📁 0 - Investor


## Legal

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-001` | <span class="en"><strong>NDA (Non-Disclosure Agreement)</strong></span><br><sub class="si">රහස්‍යතා ගිවිසුම</sub> | Notary / Lawyer | Before sharing business plan | 15000-40000 | 3-5 years | 🟡 High | Sign before any data sharing |
| ☐ | `D-002` | <span class="en"><strong>Investor NIC / Passport copy</strong></span><br><sub class="si">ආයෝජක හැඳුනුම්පත් / විදේශ ගමන් බලපත්‍ර පිටපත</sub> | Investor | Before MOU | 0 | Permanent | 🟠 Mandatory | Needed for eROC Form 18 |
| ☐ | `D-003` | <span class="en"><strong>Investor proof of funds / bank reference</strong></span><br><sub class="si">මූල්‍ය හැකියාවේ සාක්ෂි / බැංකු නිර්දේශ ලිපිය</sub> | Bank | Before MOU | 0 | 3-6 months | 🟡 High | 3-6 month statements |
| ☐ | `D-004` | <span class="en"><strong>MOU / Term Sheet</strong></span><br><sub class="si">අන්‍යෝන්‍ය අවබෝධතා පත්‍රය</sub> | Lawyer | Before incorporation | 40000-150000 | Project | 🟠 Mandatory | Non-binding; sets Conditions Precedent |
| ☐ | `D-005` | <span class="en"><strong>Shareholders Agreement (SHA)</strong></span><br><sub class="si">කොටස්හිමි ගිවිසුම</sub> | Lawyer | At incorporation | 75000-300000 | Permanent | 🟠 Mandatory | Binding; governs control and exit |
| ☐ | `D-010` | <span class="en"><strong>Encumbrance certificate (land)</strong></span><br><sub class="si">ඉඩම් උකස් සහතිකය</sub> | Divisional Registrar Badulla | Before buying land | 500-2000 | Recent copy | 🟠 Mandatory | — |

## Technical

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-006` | <span class="en"><strong>Hydrogeological / geophysical survey report</strong></span><br><sub class="si">භූ විද්‍යාත්මක ජල සමීක්ෂණ වාර්තාව</sub> | Hydrogeologist / WRB-registered consultant | Before buying land | 150000-600000 | Permanent | 🔴 Critical | Do NOT commit money before this |
| ☐ | `D-007` | <span class="en"><strong>Land title report (root of title 30+ yrs)</strong></span><br><sub class="si">ඉඩම් හිමිකම් වාර්තාව</sub> | Lawyer | Before buying land | 25000-75000 | Permanent | 🔴 Critical | — |

## Business

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-008` | <span class="en"><strong>Feasibility study / Business plan</strong></span><br><sub class="si">සාධ්‍යතා අධ්‍යයනය / ව්‍යාපාර සැලැස්ම</sub> | Consultant | Before MOU | 75000-400000 | 2-3 years | 🟡 High | Needed for bank loan / BOI |
| ☐ | `D-009` | <span class="en"><strong>Market research report</strong></span><br><sub class="si">වෙළඳපොළ පර්යේෂණ වාර්තාව</sub> | Consultant | Before MOU | 50000-200000 | 2 years | 🔵 Medium | — |


# 📁 1 - Company


## Legal

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-011` | <span class="en"><strong>Company name reservation approval</strong></span><br><sub class="si">සමාගම් නම රක්ෂිත කිරීම</sub> | DRC / eROC | First step | 1000+VAT | 3 months | 🟠 Mandatory | eroc.gov.lk |
| ☐ | `D-012` | <span class="en"><strong>Form 1 - Application for Incorporation</strong></span><br><sub class="si">පෝරම 1 - සමාගම් ලියාපදිංචි අයදුම්පත</sub> | DRC / eROC (system-generated) | First step | 4000+VAT | Permanent | 🟠 Mandatory | PDF only; system-generated form only |
| ☐ | `D-013` | <span class="en"><strong>Form 18 - Consent of Director</strong></span><br><sub class="si">පෝරම 18 - අධ්‍යක්ෂ එකඟතාව</sub> | DRC / eROC (system-generated) | First step | 2000+VAT each director | Permanent | 🟠 Mandatory | One per director |
| ☐ | `D-014` | <span class="en"><strong>Form 19 - Consent of Secretary</strong></span><br><sub class="si">පෝරම 19 - ලේකම් එකඟතාව</sub> | DRC / eROC (system-generated) | First step | 2000+VAT | Permanent | 🟠 Mandatory | Licensed company secretary |
| ☐ | `D-015` | <span class="en"><strong>Articles of Association</strong></span><br><sub class="si">සමාගම් ප්‍රඥප්තිය</sub> | Company Secretary / Lawyer | First step | 2000+VAT | Permanent | 🟠 Mandatory | Objects MUST include bottled drinking water manufacture |
| ☐ | `D-016` | <span class="en"><strong>NIC / certified passport copies (all stakeholders)</strong></span><br><sub class="si">හැඳුනුම්පත් / සහතික කළ විදේශ ගමන් බලපත්‍ර</sub> | Directors / shareholders / secretary | First step | 0 | Permanent | 🟠 Mandatory | — |
| ☐ | `D-017` | <span class="en"><strong>Registered office proof (deed/lease + utility bill)</strong></span><br><sub class="si">ලියාපදිංචි කාර්යාලයේ සාක්ෂිය</sub> | Land owner | First step | 0 | Per lease | 🟠 Mandatory | Physical SL address; no PO Box |
| ☐ | `D-018` | <span class="en"><strong>Beneficial ownership disclosure</strong></span><br><sub class="si">ප්‍රයෝජන හිමිකාරීත්ව හෙළිකිරීම</sub> | eROC | First step | 0 | Update on change | 🟠 Mandatory | — |
| ☐ | `D-019` | <span class="en"><strong>Certificate of Incorporation</strong></span><br><sub class="si">ලියාපදිංචි සහතිකය</sub> | DRC | After approval | 0 | Permanent | 🟠 Mandatory | THIS IS THE 1ST REGISTRATION DOCUMENT |
| ☐ | `D-020` | <span class="en"><strong>Certified copy of Form 1</strong></span><br><sub class="si">සහතික කළ Form 1 පිටපත</sub> | DRC | After incorporation | 1000+VAT | Permanent | 🟠 Mandatory | Required by bank |
| ☐ | `D-021` | <span class="en"><strong>Certified copy of Articles of Association</strong></span><br><sub class="si">සහතික කළ ප්‍රඥප්ති පිටපත</sub> | DRC | After incorporation | 1000+VAT | Permanent | 🟠 Mandatory | Required by bank / FCAU / BOI |
| ☐ | `D-028` | <span class="en"><strong>Annual Return (Form 15)</strong></span><br><sub class="si">වාර්ෂික ආපසු හැරවුම් පෝරමය</sub> | DRC / eROC | After AGM (first within 18 months) | Fee | Ongoing | 🟠 Mandatory | — |

## Tax

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-022` | <span class="en"><strong>TIN certificate</strong></span><br><sub class="si">බදු ගෙවන්නාගේ හඳුනාගැනීමේ අංකය</sub> | IRD (RAMIS / ird.gov.lk) | Within 30 days | 0 | Permanent | 🟠 Mandatory | Free |
| ☐ | `D-027` | <span class="en"><strong>VAT registration</strong></span><br><sub class="si">VAT ලියාපදිංචිය</sub> | IRD | When turnover exceeds threshold | 0 | Ongoing | 🟡 High | Threshold LKR 60M/yr or 15M/qtr; verify current |

## Banking

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-023` | <span class="en"><strong>Company bank account</strong></span><br><sub class="si">සමාගම් බැංකු ගිණුම</sub> | Commercial bank | Immediately | 0 | Ongoing | 🟠 Mandatory | BRC + Form 1 + AoA + TIN + board resolution |

## Admin

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-024` | <span class="en"><strong>Company seal + letterhead</strong></span><br><sub class="si">සමාගම් මුද්‍රාව + නිල ලිපි ශීර්ෂය</sub> | Printer | Immediately | 3000-8000 | Ongoing | ⚪ Low | — |

## Labour

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-025` | <span class="en"><strong>EPF registration - Form D</strong></span><br><sub class="si">EPF ලියාපදිංචිය - පෝරම D</sub> | Labour Dept / CBSL | Within 14 days of first hire | 0 | Ongoing | 🟠 Mandatory | Employer 12% + employee 8% |
| ☐ | `D-026` | <span class="en"><strong>ETF registration</strong></span><br><sub class="si">ETF ලියාපදිංචිය</sub> | CBSL ETF Board | With first contribution | 0 | Ongoing | 🟠 Mandatory | Automatic with EPF number; employer 3% |


# 📁 2 - Land


## Land

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-029` | <span class="en"><strong>Deed of ownership</strong></span><br><sub class="si">ඉඩම් ඔප්පුව</sub> | Notary + Divisional Registrar | On purchase | Stamp 1-3% + legal | Permanent | 🟠 Mandatory | — |
| ☐ | `D-030` | <span class="en"><strong>Approved survey plan (min 160 perches)</strong></span><br><sub class="si">අනුමත සමීක්ෂණ සැලැස්ම (අවම පර්චස් 160)</sub> | Licensed Land Surveyor | On purchase | 30000-90000 | Permanent | 🟠 Mandatory | FCAU minimum land requirement |
| ☐ | `D-031` | <span class="en"><strong>Registered lease agreement (5+ years)</strong></span><br><sub class="si">ලියාපදිංචි බදු ගිවිසුම (වසර 5+)</sub> | Notary + Land Registry | If leased | Stamp + registration | Per term | 🟠 Mandatory | FCAU requires 5+ yrs if not owned |
| ☐ | `D-032` | <span class="en"><strong>Owner consent letter</strong></span><br><sub class="si">හිමිකරුගේ අවසර ලිපිය</sub> | Land owner | If leased | 0 | Per term | 🟡 High | — |
| ☐ | `D-033` | <span class="en"><strong>Street line certificate</strong></span><br><sub class="si">රේඛා සහතිකය</sub> | UDA / Pradeshiya Sabha | Before building | 1000-5000 | 3-6 months | 🔵 Medium | — |
| ☐ | `D-034` | <span class="en"><strong>Zoning confirmation (industrial use allowed)</strong></span><br><sub class="si">කලාප තහවුරු කිරීම (කර්මාන්ත භාවිතය)</sub> | UDA Badulla / Pradeshiya Sabha | Before buying land | 0 | Permanent | 🔴 Critical | — |
| ☐ | `D-035` | <span class="en"><strong>Rates payment receipt</strong></span><br><sub class="si">බදු ගෙවීම් රිසිට්පත</sub> | Pradeshiya Sabha / Urban Council | Annually | Fee | 1 year | 🟠 Mandatory | Required for UDA + Trade Licence |

## Technical

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-036` | <span class="en"><strong>Soil test report</strong></span><br><sub class="si">පස් පරීක්ෂණ වාර්තාව</sub> | Geotechnical engineer | Before design | 60000-150000 | Permanent | 🟡 High | — |
| ☐ | `D-037` | <span class="en"><strong>Flood / drainage assessment</strong></span><br><sub class="si">ගංවතුර / ජල බැස්ම තක්සේරුව</sub> | Engineer | Before design | 25000-75000 | Permanent | 🔵 Medium | — |

## Approval

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-038` | <span class="en"><strong>Preliminary Planning Clearance (PPC)</strong></span><br><sub class="si">පූර්ව සැලසුම් අනුමැතිය</sub> | UDA (applications.uda.lk) | Before building permit | Fee | Project | 🟡 High | — |
| ☐ | `D-039` | <span class="en"><strong>Development Permit + Approved Building Plan (Form B)</strong></span><br><sub class="si">සංවර්ධන බලපත්‍රය + අනුමත ගොඩනැඟිලි සැලැස්ම</sub> | UDA / Pradeshiya Sabha | Before construction | Fee | Project | 🟠 Mandatory | FCAU requires the approved building plan |
| ☐ | `D-040` | <span class="en"><strong>Structural engineer certificate</strong></span><br><sub class="si">ව්‍යුහ ඉංජිනේරු සහතිකය</sub> | Chartered Structural Engineer | With building plan | 100000-350000 | Project | 🟠 Mandatory | — |
| ☐ | `D-041` | <span class="en"><strong>Certificate of Conformity (CoC - Form D)</strong></span><br><sub class="si">අනුකූලතා සහතිකය</sub> | UDA / Pradeshiya Sabha | After construction before occupation | Fee | Ongoing | 🟠 Mandatory | Required for EPL + FCAU |
| ☐ | `D-042` | <span class="en"><strong>Fire Department clearance / certificate</strong></span><br><sub class="si">ගිනි අනතුරු දෙපාර්තමේන්තු අනුමැතිය</sub> | Fire Service Dept Badulla | Before operation | 15000-60000 | 1-3 years | 🟠 Mandatory | — |

## Utility

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-043` | <span class="en"><strong>CEB 3-phase electricity connection</strong></span><br><sub class="si">විදුලිබල මණ්ඩල 3-කලාප සම්බන්ධතාව</sub> | CEB | Before operation | 100000-1000000+ | Ongoing | 🟠 Mandatory | Deposits scale with load |
| ☐ | `D-044` | <span class="en"><strong>NWS&DB water connection</strong></span><br><sub class="si">ජල සම්බන්ධතාව</sub> | NWS&DB | Before operation | 25000-150000 | Ongoing | 🔵 Medium | Backup supply |

## Licence

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-045` | <span class="en"><strong>Trade Licence (Annual Licence)</strong></span><br><sub class="si">වාර්ෂික ව්‍යාපාර බලපත්‍රය</sub> | Bandarawela Pradeshiya Sabha / Urban Council | After CoC | Gazette fee | 1 year | 🟠 Mandatory | MANDATORY for FCAU application (R6) |

## Labour

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-046` | <span class="en"><strong>Factory registration - Factories Ordinance No 45 of 1942</strong></span><br><sub class="si">කර්මාන්ත ශාලා ලියාපදිංචිය</sub> | Dept of Labour - District Factory Inspecting Engineer | Before occupying factory | Fee | Ongoing | 🟡 High | Verify requirement with Labour Dept |


# 📁 3 - Water


## WRB

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-047` | <span class="en"><strong>Hydrogeological survey report</strong></span><br><sub class="si">භූ විද්‍යාත්මක ජල සමීක්ෂණ වාර්තාව</sub> | Hydrogeologist | Before drilling | 150000-600000 | Permanent | 🔴 Critical | — |
| ☐ | `D-048` | <span class="en"><strong>WRB registration - industrial groundwater user</strong></span><br><sub class="si">WRB ලියාපදිංචිය - වාණිජ භූගත ජල පරිශීලක</sub> | Water Resources Board Rajagiriya | Before drilling | Fee | Ongoing | 🟠 Mandatory | Bottled water is a listed industry |
| ☐ | `D-049` | <span class="en"><strong>WRB written permission to drill the well</strong></span><br><sub class="si">ළිඳ කැණීමට WRB ලිඛිත අනුමැතිය</sub> | WRB (Act 29/1964; Gazette 2010/23) | Before drilling | 0 | Project | 🟠 Mandatory | — |
| ☐ | `D-050` | <span class="en"><strong>Registered drilling contractor certificate</strong></span><br><sub class="si">ලියාපදිංචි කැණීම් කොන්ත්‍රාත්තරු සහතිකය</sub> | WRB-registered contractor | Before drilling | 0 | Ongoing | 🟠 Mandatory | Illegal drilling is an offence |
| ☐ | `D-051` | <span class="en"><strong>Borewell completion certificate</strong></span><br><sub class="si">නළ ළිඳ සම්පූර්ණ කිරීමේ සහතිකය</sub> | Contractor + WRB | After drilling | 0 | Permanent | 🟠 Mandatory | — |
| ☐ | `D-058` | <span class="en"><strong>6-monthly water quality reports to WRB</strong></span><br><sub class="si">මාස 6කට වරක් ජල තත්ත්ව වාර්තා</sub> | Accredited lab -> WRB | Every 6 months | 25000-90000 | Per test | 🟠 Mandatory | — |

## Technical

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-052` | <span class="en"><strong>Pumping / yield test report</strong></span><br><sub class="si">පොම්ප කිරීමේ / ඵලදායිතා පරීක්ෂණ වාර්තාව</sub> | Hydrogeologist | After drilling | 40000-120000 | Permanent | 🟠 Mandatory | — |
| ☐ | `D-055` | <span class="en"><strong>Sanitary / pollution source survey</strong></span><br><sub class="si">සනීපාරක්ෂක / දූෂණ මූලාශ්‍ර සමීක්ෂණය</sub> | Hydrogeologist / PHI | With source test | 25000-75000 | Permanent | 🟡 High | — |

## Lab

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-053` | <span class="en"><strong>Source water test report - SLS 614:2013 (before treatment)</strong></span><br><sub class="si">මූලාශ්‍ර ජල පරීක්ෂණ වාර්තාව - SLS 614:2013</sub> | SLSI / ISO 17025 lab | Before building the factory | 25000-90000 | Per test | 🔴 Critical | FCAU will NOT register if this fails |
| ☐ | `D-054` | <span class="en"><strong>Heavy metals + pesticide + fluoride/arsenic panel</strong></span><br><sub class="si">බැර ලෝහ + කීටනාශක පරීක්ෂණ</sub> | Accredited lab | Before building the factory | 40000-150000 | Per test | 🔴 Critical | — |
| ☐ | `D-149` | <span class="en"><strong>Bromide (Br-) test of source water</strong></span><br><sub class="si">මූලාශ්‍ර ජලයේ බ්‍රෝමයිඩ් පරීක්ෂණය</sub> | Accredited lab | Before ozone system design | 25000-80000 | Per test | 🔴 Critical | Ozone + bromide = BROMATE (carcinogen). Controls ozone dose |
| ☐ | `D-150` | <span class="en"><strong>SDI + LSI + full cation/anion profile + silica/barium</strong></span><br><sub class="si">RO සැලසුම සඳහා SDI LSI සහ සම්පූර්ණ අයන පැතිකඩ</sub> | Accredited lab / RO supplier | Before RO plant order | 40000-120000 | Per test | 🔴 Critical | RO supplier needs this to size membranes and antiscalant |
| ☐ | `D-151` | <span class="en"><strong>Dry-season + wet-season source samples</strong></span><br><sub class="si">වියළි සහ වැසි කාල දෙකෙහිම නියැදි</sub> | Accredited lab | Across the year | 50000-180000 | Per test | 🟡 High | Groundwater quality varies seasonally |

## Equipment

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-056` | <span class="en"><strong>Flow meter + daily abstraction log</strong></span><br><sub class="si">ජල මාපකය + දෛනික වාර්තා පොත</sub> | Supplier | After drilling | 30000-150000 | Ongoing | 🟠 Mandatory | Required above 30000 L/month |

## Construction

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-057` | <span class="en"><strong>Well head protection structure</strong></span><br><sub class="si">ළිඳ මුඛ ආරක්ෂණ ව්‍යුහය</sub> | Contractor | During construction | 100000-400000 | Permanent | 🟠 Mandatory | — |


# 📁 4 - Factory


## Technical

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-059` | <span class="en"><strong>Architectural drawings (approved)</strong></span><br><sub class="si">ගෘහ නිර්මාණ ශිල්ප සැලසුම්</sub> | Chartered Architect | Design phase | 200000-800000 | Project | 🟠 Mandatory | — |
| ☐ | `D-060` | <span class="en"><strong>Structural drawings + calculation report</strong></span><br><sub class="si">ව්‍යුහ සැලසුම් + ගණනය වාර්තාව</sub> | Chartered Structural Engineer | Design phase | 150000-500000 | Project | 🟠 Mandatory | — |
| ☐ | `D-061` | <span class="en"><strong>M&E drawings (electrical/plumbing/drainage)</strong></span><br><sub class="si">යාන්ත්‍රික හා විදුලි සැලසුම්</sub> | Chartered Engineer | Design phase | 100000-400000 | Project | 🟡 High | — |
| ☐ | `D-062` | <span class="en"><strong>Process flow diagram + P&ID</strong></span><br><sub class="si">ක්‍රියාවලි ප්‍රවාහ සටහන</sub> | Process engineer / plant supplier | Design phase | 50000-200000 | Project | 🟠 Mandatory | Needed for FCAU (R5) |
| ☐ | `D-063` | <span class="en"><strong>Cleanroom specification and layout</strong></span><br><sub class="si">පිරිසිදු කාමර පිරිවිතර හා සැලැස්ම</sub> | Cleanroom contractor | Design phase | 100000-500000 | Project | 🟠 Mandatory | Filling room ISO 8 / Class 100000 |
| ☐ | `D-064` | <span class="en"><strong>Bill of Quantities (BOQ)</strong></span><br><sub class="si">ප්‍රමාණ පත්‍රය</sub> | Quantity Surveyor | Design phase | 75000-250000 | Project | 🟡 High | — |
| ☐ | `D-066` | <span class="en"><strong>Material test certificates (tiles/epoxy/SS grade)</strong></span><br><sub class="si">ද්‍රව්‍ය පරීක්ෂණ සහතික</sub> | Suppliers | During construction | 0 | Permanent | 🟡 High | — |
| ☐ | `D-067` | <span class="en"><strong>Commissioning report</strong></span><br><sub class="si">ක්‍රියාරම්භක වාර්තාව</sub> | Plant supplier | At handover | 0 | Permanent | 🟠 Mandatory | SLSI audit evidence |
| ☐ | `D-068` | <span class="en"><strong>As-built drawings</strong></span><br><sub class="si">සැබෑ ඉදිකිරීම් සැලසුම්</sub> | Architect | At handover | 75000-250000 | Permanent | 🟠 Mandatory | FCAU submission |

## Legal

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-065` | <span class="en"><strong>Contractor agreement + insurance</strong></span><br><sub class="si">කොන්ත්‍රාත්තරු ගිවිසුම + රක්ෂණය</sub> | Lawyer | Before construction | 25000-100000 | Project | 🟠 Mandatory | — |

## FCAU

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-069` | <span class="en"><strong>Location Map (Google map)</strong></span><br><sub class="si">පිහිටුම් සිතියම (ගූගල්)</sub> | You | FCAU application | 0 | Ongoing | 🟠 Mandatory | FCAU required doc R1 |
| ☐ | `D-070` | <span class="en"><strong>Site plan on survey plan (source + factory marked)</strong></span><br><sub class="si">සමීක්ෂණ සැලැස්ම මත ස්ථාන සැලැස්ම</sub> | Surveyor | FCAU application | 25000-75000 | Ongoing | 🟠 Mandatory | FCAU required doc R2 |
| ☐ | `D-071` | <span class="en"><strong>Factory layout (approved building plan)</strong></span><br><sub class="si">කර්මාන්ත ශාලා සැලැස්ම</sub> | Local authority | FCAU application | Fee | Ongoing | 🟠 Mandatory | FCAU required doc R3 |
| ☐ | `D-072` | <span class="en"><strong>Sketch map of source water and processing facility</strong></span><br><sub class="si">ජල මූලාශ්‍ර හා සැකසුම් පහසුකම් සිතියම</sub> | Process engineer | FCAU application | 25000-100000 | Ongoing | 🟠 Mandatory | FCAU required doc R4 |
| ☐ | `D-073` | <span class="en"><strong>Process flow chart</strong></span><br><sub class="si">ක්‍රියාවලි ප්‍රවාහ ප්‍රස්තාරය</sub> | Process engineer | FCAU application | 15000-50000 | Ongoing | 🟠 Mandatory | FCAU required doc R5 |


# 📁 5 - Machinery


## Procurement

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-074` | <span class="en"><strong>3 competing quotations per major machine</strong></span><br><sub class="si">ප්‍රධාන යන්ත්‍ර සඳහා තරඟකාරී quotation 3ක්</sub> | Suppliers | Before PO | 0 | Ongoing | 🟠 Mandatory | Investor governance requirement |
| ☐ | `D-075` | <span class="en"><strong>Landed cost calculation (customs/PAL/VAT/CESS/shipping)</strong></span><br><sub class="si">සම්පූර්ණ ආනයන පිරිවැය ගණනය</sub> | Clearing agent | Before PO | 0 | Ongoing | 🟡 High | For imported machines |

## Customs

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-076` | <span class="en"><strong>Customs registration (importer)</strong></span><br><sub class="si">රේගු ලියාපදිංචිය (ආනයනකරු)</sub> | Sri Lanka Customs | Before importing | Fee | Ongoing | 🟠 Mandatory | — |

## Equipment

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-077` | <span class="en"><strong>Water treatment plant (RO + filters + ozone + UV)</strong></span><br><sub class="si">ජල පිරිපහදු පද්ධතිය</sub> | Plant supplier | Construction phase | 4000000-25000000 | 10+ years | 🔴 Critical | Core asset |
| ☐ | `D-078` | <span class="en"><strong>PET stretch blow moulding machine</strong></span><br><sub class="si">PET බෝතල් නිෂ්පාදන යන්ත්‍රය</sub> | Machine supplier | Construction phase | 3000000-25000000 | 10+ years | 🟡 High | Or buy bottles externally |
| ☐ | `D-079` | <span class="en"><strong>Rinsing-filling-capping monoblock</strong></span><br><sub class="si">පිරවීම-මුද්‍රා තැබීමේ යන්ත්‍රය</sub> | Machine supplier | Construction phase | 4000000-40000000 | 10+ years | 🔴 Critical | Core asset |
| ☐ | `D-080` | <span class="en"><strong>Labelling + shrink wrap + palletizing</strong></span><br><sub class="si">ලේබල් + ඇසුරුම් යන්ත්‍ර</sub> | Machine supplier | Construction phase | 2000000-12000000 | 10+ years | 🟡 High | — |
| ☐ | `D-081` | <span class="en"><strong>Date/batch coder (inkjet or laser)</strong></span><br><sub class="si">දින/කාණ්ඩ මුද්‍රණ යන්ත්‍රය</sub> | Supplier | Construction phase | 350000-2000000 | 8 years | 🟠 Mandatory | Label law requirement |
| ☐ | `D-082` | <span class="en"><strong>Oil-free food-grade air compressor</strong></span><br><sub class="si">ආහාර ශ්‍රේණියේ වායු සම්පීඩකය</sub> | Supplier | Construction phase | 600000-3500000 | 10 years | 🟠 Mandatory | Ordinary compressed air not acceptable |
| ☐ | `D-083` | <span class="en"><strong>Standby generator</strong></span><br><sub class="si">විකල්ප ජනක යන්ත්‍රය</sub> | Supplier | Construction phase | 3000000-15000000 | 10 years | 🟡 High | — |
| ☐ | `D-084` | <span class="en"><strong>Quality control laboratory equipment</strong></span><br><sub class="si">තත්ත්ව පාලන පරීක්ෂණාගාර උපකරණ</sub> | Lab supplier | Construction phase | 2000000-6000000 | 8 years | 🟠 Mandatory | SLSI requires in-house QC |
| ☐ | `D-085` | <span class="en"><strong>CIP (Clean-in-Place) system</strong></span><br><sub class="si">CIP පිරිසිදු කිරීමේ පද්ධතිය</sub> | Plant supplier | Construction phase | 400000-1800000 | 10 years | 🟠 Mandatory | — |
| ☐ | `D-152` | <span class="en"><strong>Re-mineralisation dosing system (Ca/Mg/bicarbonate)</strong></span><br><sub class="si">ඛනිජ යළි එකතු කිරීමේ පද්ධතිය</sub> | Plant supplier | Construction phase | 200000-700000 | 10 years | 🟡 High | RO water tastes flat; must stay within SLS 894 limits |
| ☐ | `D-153` | <span class="en"><strong>0.2 micron sterile filter before filler</strong></span><br><sub class="si">පිරවීමට පෙර 0.2 මයික්‍රෝන් වන්ධ්‍යා පෙරහන</sub> | Plant supplier | Construction phase | 150000-600000 | 10 years | 🟠 Mandatory | Final microbial barrier - CCP 6 |
| ☐ | `D-154` | <span class="en"><strong>UV sterilizer with validated dose and intensity sensor</strong></span><br><sub class="si">සත්‍යාපිත මාත්‍රාවක් සහිත UV විෂබීජහරණ යන්ත්‍රය</sub> | Plant supplier | Construction phase | 150000-700000 | 10 years | 🟠 Mandatory | Dose >= 40 mJ/cm2 - CCP 4; lamp change yearly |
| ☐ | `D-155` | <span class="en"><strong>RO reject water recovery / reuse system</strong></span><br><sub class="si">RO අප ජල නැවත භාවිත පද්ධතිය</sub> | Contractor | Construction phase | 500000-2500000 | 10 years | 🟡 High | RO rejects 25-50% of feed; CEA discharge limits apply |
| ☐ | `D-086` | <span class="en"><strong>Spare parts initial stock</strong></span><br><sub class="si">ආරම්භක අමතර කොටස් තොගය</sub> | Suppliers | At commissioning | 500000-3000000 | Ongoing | 🟡 High | — |

## Service

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-087` | <span class="en"><strong>Preventive maintenance contracts</strong></span><br><sub class="si">වැළැක්වීමේ නඩත්තු ගිවිසුම්</sub> | Plant suppliers | At commissioning | Annual fee | 1 year | 🟠 Mandatory | — |
| ☐ | `D-088` | <span class="en"><strong>Calibration services (pH/balance/thermometer/flow)</strong></span><br><sub class="si">මාපාංකන සේවා</sub> | Accredited calibration lab | Annually | 50000-250000 | 6-12 months | 🟠 Mandatory | SLSI audit evidence |
| ☐ | `D-089` | <span class="en"><strong>Pest control contract</strong></span><br><sub class="si">කීට පාලන ගිවිසුම</sub> | Licensed pest control | Monthly | 120000-480000 | 1 year | 🟠 Mandatory | FCAU/SLSI requirement |
| ☐ | `D-090` | <span class="en"><strong>Staff training (food handling / GMP / machines)</strong></span><br><sub class="si">සේවක පුහුණුව</sub> | SLSI / ITI / supplier | Annually | 100000-500000 | 1 year | 🟠 Mandatory | FCAU required doc R10 |
| ☐ | `D-156` | <span class="en"><strong>Filter media replacement schedule and log</strong></span><br><sub class="si">පෙරහන් මාධ්‍ය මාරු කිරීමේ කාලසටහන සහ වාර්තාව</sub> | QA Manager | Ongoing | 500000-2000000 | Ongoing | 🟠 Mandatory | Carbon 1-2 yrs; cartridges 1-3 months; membranes 2-5 yrs |


# 📁 6 - MoH FCAU


## Registration

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-091` | <span class="en"><strong>FCAU bottled water registration application</strong></span><br><sub class="si">FCAU බෝතල් ජල ලියාපදිංචි අයදුම්පත</sub> | Food Control Administration Unit | After plant is ready | Fee | Ongoing | 🟠 Mandatory | Food Act 26/1980 + Regs 2011 |
| ☐ | `D-092` | <span class="en"><strong>Two specimen labels</strong></span><br><sub class="si">ලේබල් නියැදි දෙකක්</sub> | Printer | FCAU application | 10000-50000 | Per design | 🟠 Mandatory | Food (Labelling) Regs 2005 |
| ☐ | `D-093` | <span class="en"><strong>Organization chart</strong></span><br><sub class="si">සංවිධාන ප්‍රස්තාරය</sub> | HR | FCAU application | 0 | Ongoing | 🟠 Mandatory | FCAU required doc R8 |
| ☐ | `D-094` | <span class="en"><strong>Supervision schedules</strong></span><br><sub class="si">අධීක්ෂණ කාලසටහන්</sub> | QA Manager | FCAU application | 0 | Ongoing | 🟠 Mandatory | FCAU required doc R9 |
| ☐ | `D-095` | <span class="en"><strong>Training documents (food handling / hygiene)</strong></span><br><sub class="si">පුහුණු ලේඛන</sub> | HR / trainer | FCAU application | 0 | Ongoing | 🟠 Mandatory | FCAU required doc R10 |
| ☐ | `D-096` | <span class="en"><strong>Job descriptions for all staff</strong></span><br><sub class="si">සියලු සේවක රාජකාරි විස්තර</sub> | HR | FCAU application | 0 | Ongoing | 🟠 Mandatory | FCAU required doc R11 |
| ☐ | `D-100` | <span class="en"><strong>SLSI recommendation letter (valid 1 year)</strong></span><br><sub class="si">SLSI නිර්දේශ ලිපිය (වසර 1)</sub> | SLSI | After audit 1 | 0 | 1 year | 🟠 Mandatory | — |
| ☐ | `D-101` | <span class="en"><strong>PHI / MOH / FDI inspection recommendations</strong></span><br><sub class="si">PHI / MOH / FDI පරීක්ෂණ නිර්දේශ</sub> | Local health authorities | After SLSI audit | 0 | Project | 🟠 Mandatory | — |
| ☐ | `D-102` | <span class="en"><strong>Conditional temporary registration (1 year)</strong></span><br><sub class="si">කොන්දේසි සහිත තාවකාලික ලියාපදිංචිය</sub> | Chief Food Authority | After all recommendations | 0 | 1 year | 🟠 Mandatory | — |
| ☐ | `D-103` | <span class="en"><strong>Full registration after SLSI audit 2 (2 more years)</strong></span><br><sub class="si">SLSI දෙවන විගණනයෙන් පසු සම්පූර්ණ ලියාපදිංචිය</sub> | Chief Food Authority | Within year 1 | 0 | 2 years | 🟠 Mandatory | Total validity 3 years |

## Quality

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-097` | <span class="en"><strong>HACCP plan and food safety management system</strong></span><br><sub class="si">HACCP සැලැස්ම සහ ආහාර සුරක්ෂිතතා පද්ධතිය</sub> | Food safety consultant | Before SLSI audit | 250000-900000 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-098` | <span class="en"><strong>GMP manual + SOPs</strong></span><br><sub class="si">GMP අත්පොත + සම්මත ක්‍රියාපටිපාටි</sub> | QA Manager | Before SLSI audit | 150000-500000 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-099` | <span class="en"><strong>Food handler medical certificates</strong></span><br><sub class="si">ආහාර හසුරුවන්නන්ගේ වෛද්‍ය සහතික</sub> | Hospital / PHI | Annually | 5000-15000 per person | 1 year | 🟠 Mandatory | — |
| ☐ | `D-104` | <span class="en"><strong>Finished product test reports - SLS 894 (Bottled Drinking Water)</strong></span><br><sub class="si">අවසාන නිෂ්පාදන පරීක්ෂණ වාර්තා - SLS 894</sub> | SLSI / accredited lab | Monthly + per audit | 25000-90000 | Per test | 🟠 Mandatory | SLS 1038 not applicable - product decision 2026-10-10 |
| ☐ | `D-157` | <span class="en"><strong>Ozone residual monitoring records (CCP 5) - 0.2-0.4 ppm</strong></span><br><sub class="si">ඕසෝන් අවශේෂ අධීක්ෂණ වාර්තා - 0.2-0.4 ppm</sub> | QA lab | Every batch | 0 | 2 years retention | 🔴 Critical | Determines shelf life; below 0.15 ppm = microbial growth |
| ☐ | `D-158` | <span class="en"><strong>Bromate testing of finished product</strong></span><br><sub class="si">අවසාන නිෂ්පාදනයේ බ්‍රෝමේට් පරීක්ෂණය</sub> | SLSI / accredited lab | Monthly + per audit | 25000-90000 | Per test | 🔴 Critical | Ozonation by-product; carcinogenic if bromide present in source |
| ☐ | `D-159` | <span class="en"><strong>Shelf life validation study (6 / 12 months at 30C and 40C)</strong></span><br><sub class="si">ගබඩා කාල වලංගු අධ්‍යයනය</sub> | Accredited lab | Before launch | 100000-400000 | Per product | 🟠 Mandatory | Sets the Best Before date on the label |


# 📁 7 - SLSI


## Certification

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-105` | <span class="en"><strong>SLSI application form + fee</strong></span><br><sub class="si">SLSI අයදුම්පත + ගාස්තුව</sub> | SLSI | After MoH process starts | Fee | Project | 🟠 Mandatory | — |
| ☐ | `D-106` | <span class="en"><strong>Quality manual + documented QMS</strong></span><br><sub class="si">තත්ත්ව අත්පොත + ලේඛනගත QMS</sub> | QA Manager | Before SLSI audit | 150000-600000 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-107` | <span class="en"><strong>Internal audit + management review records</strong></span><br><sub class="si">අභ්‍යන්තර විගණන + කළමනාකරණ සමාලෝචන වාර්තා</sub> | QA | Before SLSI audit | 0 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-108` | <span class="en"><strong>Raw material specs + supplier CoAs</strong></span><br><sub class="si">අමුද්‍රව්‍ය පිරිවිතර + සැපයුම්කරු සහතික</sub> | Suppliers | Ongoing | 0 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-109` | <span class="en"><strong>Batch production records + traceability</strong></span><br><sub class="si">කාණ්ඩ නිෂ්පාදන වාර්තා + සොයාගැනීමේ හැකියාව</sub> | Production | Ongoing | 0 | 2 years | 🟠 Mandatory | — |
| ☐ | `D-110` | <span class="en"><strong>Complaint handling + product recall procedure</strong></span><br><sub class="si">පැමිණිලි කළමනාකරණය + නිෂ්පාදන ආපසු කැඳවීම</sub> | QA Manager | Before SLSI audit | 0 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-111` | <span class="en"><strong>SLS 1336:2008 certification for PET bottles</strong></span><br><sub class="si">PET බෝතල් සඳහා SLS 1336:2008 සහතිකය</sub> | SLSI (own) or bottle supplier | Ongoing | Fee | 3 years | 🟠 Mandatory | CAA enforced since 01.09.2016 (Gazette 1918/18) |
| ☐ | `D-112` | <span class="en"><strong>SLS Product Certification Mark permit (SLS 894 - Bottled Drinking Water)</strong></span><br><sub class="si">SLS නිෂ්පාදන සහතික ලකුණ - SLS 894</sub> | SLSI | After 2 conforming samples | Annual fee on turnover | 3 years | 🟡 High | Voluntary but commercially essential; SLS 1038 not applicable |
| ☐ | `D-113` | <span class="en"><strong>Agreement with SLSI (permit conditions)</strong></span><br><sub class="si">SLSI සමඟ ගිවිසුම</sub> | SLSI | With permit | 0 | 3 years | 🟠 Mandatory | Indemnity / misuse / cancellation clauses |


# 📁 8 - Environment


## Licence

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-114` | <span class="en"><strong>EPL category determination (A/B/C/D)</strong></span><br><sub class="si">EPL ප්‍රවර්ග තීරණය</sub> | CEA Badulla District Office | Early in project | 0 | Ongoing | 🟠 Mandatory | Gazette 2264/18 (27.01.2022) |
| ☐ | `D-115` | <span class="en"><strong>EIA / IEE screening determination</strong></span><br><sub class="si">EIA / IEE තීරණය</sub> | CEA | Early in project | 0 | Ongoing | 🟡 High | Only if prescribed project / sensitive area |
| ☐ | `D-116` | <span class="en"><strong>Effluent treatment plant (ETP) + discharge permit</strong></span><br><sub class="si">අප ජල පිරිපහදු පද්ධතිය</sub> | Contractor + CEA | Before operation | 1000000-5000000 | Ongoing | 🟠 Mandatory | Gazette 2264/17 discharge standards |
| ☐ | `D-117` | <span class="en"><strong>Effluent characteristics lab report</strong></span><br><sub class="si">අප ජල රසායනික වාර්තාව</sub> | Accredited lab | Before EPL | 30000-100000 | Per test | 🟠 Mandatory | — |
| ☐ | `D-118` | <span class="en"><strong>Pollutant abatement proposal</strong></span><br><sub class="si">දූෂක අවම කිරීමේ යෝජනාව</sub> | Environmental consultant | Before EPL | 75000-300000 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-119` | <span class="en"><strong>Environmental Protection Licence (EPL)</strong></span><br><sub class="si">පරිසර ආරක්ෂණ බලපත්‍රය</sub> | CEA / Local Authority (cat D) | Before commercial operation | 4000-15000 + VAT | 1-3 years | 🟠 Mandatory | National Environment Act s.23A |
| ☐ | `D-120` | <span class="en"><strong>Scheduled Waste Management Licence (generator)</strong></span><br><sub class="si">අනතුරුදායක අපද්‍රව්‍ය බලපත්‍රය</sub> | CEA | If hazardous waste | 4000-15000 + VAT | 1-3 years | 🟡 High | Gazette 1534/18; RO membranes waste oil etc |

## Service

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-121` | <span class="en"><strong>Licensed scheduled waste collector / transporter agreement</strong></span><br><sub class="si">බලපත්‍රලාභී අපද්‍රව්‍ය එකතුකරු ගිවිසුම</sub> | CEA-licensed collector | Ongoing | Fee | 1 year | 🟠 Mandatory | Declaration form per consignment |

## Technical

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-122` | <span class="en"><strong>Noise assessment (blow moulding / generator)</strong></span><br><sub class="si">ශබ්ද තක්සේරුව</sub> | Acoustic consultant | Before operation | 50000-150000 | Ongoing | 🔵 Medium | — |
| ☐ | `D-123` | <span class="en"><strong>Air emission source list + stack test (boiler/generator)</strong></span><br><sub class="si">වායු විමෝචන වාර්තාව</sub> | Accredited lab | Before operation | 50000-200000 | Ongoing | 🔵 Medium | Gazette 2126/36 |


# 📁 9 - Tax/Statutory


## Tax

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-124` | <span class="en"><strong>VAT returns</strong></span><br><sub class="si">VAT ආපසු ඉල්ලීම්</sub> | IRD | Monthly | 0 | Ongoing | 🟠 Mandatory | Due end of following month |
| ☐ | `D-125` | <span class="en"><strong>APIT / PAYE withholding returns</strong></span><br><sub class="si">APIT වාර්තා</sub> | IRD | Monthly | 0 | Ongoing | 🟠 Mandatory | Due 15th of following month |
| ☐ | `D-126` | <span class="en"><strong>Corporate income tax return</strong></span><br><sub class="si">ආයතනික ආදායම් බදු ආපසු ඉල්ලීම</sub> | IRD | Annually | 0 | Ongoing | 🟠 Mandatory | — |

## Labour

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-127` | <span class="en"><strong>EPF monthly contributions (Form C)</strong></span><br><sub class="si">EPF මාසික දායකත්ව</sub> | CBSL | Monthly | 0 | Ongoing | 🟠 Mandatory | Last working day of following month |
| ☐ | `D-128` | <span class="en"><strong>ETF monthly contributions</strong></span><br><sub class="si">ETF මාසික දායකත්ව</sub> | CBSL | Monthly | 0 | Ongoing | 🟠 Mandatory | Last working day of following month |
| ☐ | `D-129` | <span class="en"><strong>Written employment contracts</strong></span><br><sub class="si">ලිඛිත සේවා ගිවිසුම්</sub> | HR | On hiring | 0 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-130` | <span class="en"><strong>Gratuity provision (Act 12 of 1983)</strong></span><br><sub class="si">වැටහීමේ දීමනා ප්‍රතිපාදන</sub> | Accounts | Annually | 0 | Ongoing | 🟠 Mandatory | — |

## Audit

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-131` | <span class="en"><strong>Statutory audit + financial statements</strong></span><br><sub class="si">විගණිත මූල්‍ය ප්‍රකාශන</sub> | Chartered Accountant | Annually | 300000-1200000 | Ongoing | 🟠 Mandatory | — |
| ☐ | `D-132` | <span class="en"><strong>AGM minutes + board resolutions</strong></span><br><sub class="si">වාර්ෂික මහා සභා විනාඩි සටහන්</sub> | Company Secretary | Annually | Secretarial fee | Ongoing | 🟠 Mandatory | — |

## Insurance

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-133` | <span class="en"><strong>Fire and perils insurance</strong></span><br><sub class="si">ගිනි රක්ෂණය</sub> | Insurance company | Before operation | Annual premium | 1 year | 🟠 Mandatory | — |
| ☐ | `D-134` | <span class="en"><strong>Product liability insurance</strong></span><br><sub class="si">නිෂ්පාදන වගකීම් රක්ෂණය</sub> | Insurance company | Before launch | Annual premium | 1 year | 🔴 Critical | Highest risk exposure |
| ☐ | `D-135` | <span class="en"><strong>Public liability insurance</strong></span><br><sub class="si">මහජන වගකීම් රක්ෂණය</sub> | Insurance company | Before operation | Annual premium | 1 year | 🟠 Mandatory | — |
| ☐ | `D-136` | <span class="en"><strong>Workmen's compensation / group personal accident</strong></span><br><sub class="si">සේවක වන්දි රක්ෂණය</sub> | Insurance company | On hiring | Annual premium | 1 year | 🟠 Mandatory | — |
| ☐ | `D-137` | <span class="en"><strong>Machinery breakdown + goods in transit</strong></span><br><sub class="si">යන්ත්‍ර බිඳවැටීම් + ප්‍රවාහන රක්ෂණය</sub> | Insurance company | Before operation | Annual premium | 1 year | 🟡 High | — |


# 📁 10 - Launch


## IP

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-138` | <span class="en"><strong>Trademark search + registration</strong></span><br><sub class="si">වෙළඳ ලකුණ සෙවීම + ලියාපදිංචිය</sub> | NIPO (nipo.gov.lk) | Before branding | 5000-15000 + agent | 10 years | 🔴 Critical | Do before moulds and labels are made |
| ☐ | `D-139` | <span class="en"><strong>Logo and packaging copyright</strong></span><br><sub class="si">ලෝගෝ සහ ඇසුරුම් ප්‍රකාශන හිමිකම</sub> | NIPO | With branding | 75000-400000 | Life of author | 🟡 High | — |

## Product

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-140` | <span class="en"><strong>GS1 Sri Lanka barcode membership</strong></span><br><sub class="si">GS1 ශ්‍රී ලංකා barcode සාමාජිකත්වය</sub> | GS1 Sri Lanka | Before retail | Annual fee | 1 year | 🟠 Mandatory | One GTIN per SKU |
| ☐ | `D-141` | <span class="en"><strong>Label compliance check (Food Labelling Regs 2005)</strong></span><br><sub class="si">ලේබල් අනුකූලතා පරීක්ෂාව</sub> | QA / FCAU | Before printing | 0 | Per design | 🟠 Mandatory | — |
| ☐ | `D-160` | <span class="en"><strong>Label wording locked to Bottled Drinking Water only</strong></span><br><sub class="si">ලේබල් නාමය බෝතල් කළ පානීය ජලය ලෙස සීමා කිරීම</sub> | QA / legal | Before label print | 0 | Ongoing | 🔴 Critical | No spring means Natural Mineral Water and Spring Water are illegal claims |

## Quality

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-142` | <span class="en"><strong>Shelf life validation study</strong></span><br><sub class="si">ගබඩා කාල වලංගු අධ්‍යයනය</sub> | Accredited lab | Before launch | 100000-400000 | Per product | 🟠 Mandatory | — |

## Operations

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-143` | <span class="en"><strong>Distributor / dealer agreements</strong></span><br><sub class="si">බෙදාහරින්නන්ගේ ගිවිසුම්</sub> | Lawyer | Before launch | 25000-100000 each | 1-3 years | 🟡 High | — |
| ☐ | `D-144` | <span class="en"><strong>Vehicle revenue licences + permits</strong></span><br><sub class="si">වාහන බලපත්‍ර</sub> | DMT / Pradeshiya Sabha | Annually | Fee | 1 year | 🟠 Mandatory | — |

## Export

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-145` | <span class="en"><strong>Exporter registration (Customs + Dept of Commerce)</strong></span><br><sub class="si">අපනයනකරු ලියාපදිංචිය</sub> | Sri Lanka Customs / DoC | Before export | Fee | Ongoing | 🟡 High | Export phase only |
| ☐ | `D-146` | <span class="en"><strong>Certificate of Free Sale / Health Certificate</strong></span><br><sub class="si">නිදහස් විකුණුම් සහතිකය</sub> | MoH / EDB | Per shipment | Fee | Per shipment | 🟡 High | Export phase only |
| ☐ | `D-147` | <span class="en"><strong>Certificate of Origin</strong></span><br><sub class="si">මූලාරම්භ සහතිකය</sub> | Ceylon Chamber / National Chamber | Per shipment | Fee | Per shipment | 🟡 High | Export phase only |

## Investment

| ✅ | ID | ලේඛනය / අයිතමය | නිකුතු කරන්නා | කවදා | වියදම (LKR) | වලංගු | ප්‍රමුඛතාව | සටහන් |
|:--:|---|---|---|---|---|---|:--:|---|
| ☐ | `D-148` | <span class="en"><strong>BOI registration (if foreign investment or export focus)</strong></span><br><sub class="si">BOI ලියාපදිංචිය</sub> | Board of Investment | Early if applicable | 0 | Project term | 🔵 Medium | investsrilanka.com |


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
