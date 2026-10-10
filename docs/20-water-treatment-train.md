# 💧 ජල පිරිපහදු පද්ධතිය — සම්පූර්ණ filtration ක්‍රියාවලිය
# Water Treatment Train — the complete filtration process

> ## ✅ තීරණය ලබාගෙන ඇත | DECISION LOCKED
> **නිෂ්පාදනය = "බෝතල් කළ පානීය ජලය / Bottled Drinking Water" — ප්‍රමිතිය SLS 894**
> මූලාශ්‍රය = නළ ළිඳ / භූගත ජලය (groundwater), **සම්පූර්ණයෙන්ම පිරිපහදු කර** බෝතල් කෙරේ.
> **Natural Mineral Water (SLS 1038) දැන් නොකරයි** — ඒ සඳහා සැබෑ ස්වාභාවික උල්පතක් සහ වෙනස් නීතිමය අනුමැති අවශ්‍යයි.
> 👉 [තීරණ වාර්තාව / Decision log](21-decisions-and-assumptions.md)

---

## 20.1 — ⭐ පිරිපහදු දාමය | The treatment train (අනුපිළිවෙළ වැදගත්!)

```
        [නළ ළිඳ / BOREWELL]
                │  ⚠️ මූලාශ්‍ර ජලය SLS 614:2013 සමත් විය යුතුය (FCAU නීතිය)
                ▼
  1.  Raw water tank (SS304 / FRP)  ── level control, vent with 0.2µm filter
                ▼
  2.  Raw water pump + Y-strainer (100µm)
                ▼
  3.  [Optional] Chlorine / hypochlorite dosing  ── shock oxidation
                ▼
  4.  ⭐ MULTI-GRADE SAND FILTER (MGSF)
      └─ ඉවත් කරයි: turbidity, suspended solids, iron, manganese (oxidised)
      └─ ඉලක්කය: turbidity < 1 NTU  (ඉලක්කය < 0.5 NTU)
                ▼
  5.  ⭐ ACTIVATED CARBON FILTER (ACF)
      └─ ඉවත් කරයි: chlorine, organics, ගඳ (odour), රස, වර්ණ, pesticide residues
      └─ ඉලක්කය: free chlorine < 0.1 ppm  (RO membrane ආරක්ෂාවට)
                ▼
  6.  WATER SOFTENER (ion exchange, NaCl regeneration)
      └─ ඉවත් කරයි: hardness (Ca²⁺, Mg²⁺)
      └─ ⚠️ අවශ්‍ය වන්නේ hardness ඉහළ නම් පමණි — RO membrane scaling වළක්වයි
                ▼
  7.  ANTISCALANT dosing  ── RO membrane scaling වළක්වයි
                ▼
  8.  ⭐ MICRON CARTRIDGE FILTRATION (SS316 housings)
      └─ 5 µm  →  1 µm  →  0.5 µm   (පෙළින් පෙළ)
                ▼
  9.  ⭐⭐ REVERSE OSMOSIS (RO)  ── ප්‍රධාන ඒකකය
      └─ ඉවත් කරයි: 95–99% dissolved solids, බැර ලෝහ, nitrate, fluoride,
                     ක්ෂුද්‍ර ජීවීන් (physical barrier)
      └─ ඵලදාව (permeate) 50–75%  |  reject 25–50%  ← ⚠️ විශාලතම අපතේ යාම
                ▼
 10.  RO permeate / treated water tank (SS316)  ── recirculation loop සහිතව
                ▼
 11.  [Optional] RE-MINERALISATION
      └─ RO ජලය "පැතලි" රසක් ගනී. Food-grade Ca/Mg/bicarbonate එකතු කර
         රස වැඩි දියුණු කරන්න. ⚠️ SLS 894 සීමාවන් තුළම තිබිය යුතුය
                ▼
 12.  ⭐ UV STERILIZER (254 nm)
      └─ validated dose ≥ 40 mJ/cm²
                ▼
 13.  ⭐⭐ OZONE GENERATOR + injection / contact tank
      └─ ⭐ ෂෙල්ෆ් ලයිෆ් එක තීරණය කරන්නේ මෙයයි
      └─ ඉලක්කය: **0.2 – 0.4 ppm residual** at the filler
      └─ බෝතලය තුළ O₃ → O₂ ලෙස විඝටනය වේ (විෂ සහිත අවශේෂ නැත)
                ▼
 14.  ⭐ STERILE FILTER 0.2 µm / 0.45 µm (පිරවීමට ඉදිරියෙන්)
                ▼
 15.  FILLING (positive-pressure cleanroom, ISO 8) → capping → labelling → packing
```

---

## 20.2 — එක් එක් පියවර මොනවා ඉවත් කරයිද? | What each step removes

| පියවර | ඉවත් කරන දේ | ඉවත් **නොකරන** දේ | අධීක්ෂණය / Monitor |
|---|---|---|---|
| **Y-strainer** | මැලියම්, කොළ, කුඩා අපද්‍රව්‍ය | — | ΔP (pressure drop) |
| **MGSF (sand)** | Turbidity, TSS, oxidised iron/manganese | දියවූ ඝන, ලවණ, ක්ෂුද්‍ර ජීවී | **Turbidity < 1 NTU**; ΔP; දෛනික backwash |
| **ACF (carbon)** | Chlorine, chloramine, organics, odour, taste, colour, some pesticides | දියවූ ලවණ, hardness, ක්ෂුද්‍ර ජීවී (ඇතුළත වැඩිය හැක!) | **Free chlorine < 0.1 ppm**; සතිපතා sanitise |
| **Softener** | Hardness (Ca, Mg) | අනෙක් සියල්ල | Hardness (dH); NaCl tank; regen cycles |
| **Antiscalant** | (scaling වළක්වයි) | — | Dosing pump calibration |
| **Micron 5/1/0.5 µm** | ක්ෂුද්‍ර අංශු, carbon fines, colloids | දියවූ ලවණ | **ΔP** — cartridge මාරු කිරීමේ සංඥාව |
| **RO** | 95–99% TDS, බැර ලෝහ, nitrate, fluoride, arsenic, ක්ෂුද්‍ර ජීවී, virus | දියවූ වායු (CO₂, O₂, H₂S) | **Conductivity/TDS**; recovery %; normalised flux; salt passage |
| **Re-mineralisation** | (එකතු කරයි) | — | Hardness/alkalinity — SLS 894 සීමාවන් |
| **UV (254 nm)** | බැක්ටීරියා, virus, *Cryptosporidium* | අංශු, රසායනික | Lamp hours; UV intensity sensor; sleeve cleaning |
| **Ozone** | සියලු ක්ෂුද්‍ර ජීවී + bottle/cap ඇතුළතද | — | **O₃ residual 0.2–0.4 ppm**; ⚠️ **bromate** |
| **0.2 µm sterile filter** | අවසාන ආරක්ෂණ බාධකය | — | ΔP; integrity test; change per batch/weekly |

---

## 20.3 — 🔴 වඩාත්ම වැදගත් කරුණ 5ක් (අසාර්ථක වන තැන්) | The 5 things that kill plants

### ⚠️ 1. BROMATE — මෙය අමතක කරන්න එපා!

**Ozone + Bromide (Br⁻) → Bromate (BrO₃⁻)** — මෙය **පිළිකා කාරක (carcinogenic)** සංයෝගයකි.
බොහෝ භූගත ජලවල bromide ස්වාභාවිකව තිබේ.

- 🔴 **මූලාශ්‍ර ජලයේ Bromide පරීක්ෂා කරන්න** — මෙය [Phase 3](04-phase-3-water-source-wrb.md) ජල පරීක්ෂණ ලැයිස්තුවට **එකතු කර ඇත**.
- Bromide > ~0.01 mg/L නම් → ozone මාත්‍රාව අඩු කරන්න, contact time කෙටි කරන්න, pH පාලනය කරන්න, **හෝ UV+H₂O₂ වැනි විකල්ප disinfection සලකා බලන්න.**
- **අවසාන නිෂ්පාදනයේ bromate** නිතර පරීක්ෂා කරන්න (SLSI හෝ accredited lab).

### ⚠️ 2. RO reject ජලය — 25% සිට 50% දක්වා!

RO එකෙන් ජලයෙන් අඩක් පමණ **අපතේ යයි.** දිනකට 50 m³ නිෂ්පාදනය කරනවා නම්, reject **17–50 m³/දින**.

**නැවත භාවිත කිරීමේ සැලැස්මක් අවශ්‍යයි** (CEA EPL එකටද වැදගත්):
- Cooling tower make-up
- කර්මාන්ත ශාලා බිම් සෝදනය
- වැසිකිළි
- වාහන සෝදනය
- වගා/උයන
- Reject recovery system (දෙවන RO pass)

### ⚠️ 3. Ozone residual නිවැරදිව නොමැති වීම

| O₃ residual | ප්‍රතිඵලය |
|---|---|
| **< 0.15 ppm** | 🔴 ක්ෂුද්‍ර ජීව වර්ධනය → shelf life අසාර්ථකයි → recall |
| **0.2 – 0.4 ppm** | ✅ නිවැරදි කලාපය |
| **> 0.5 ppm** | ⚠️ රස/ගඳ; **bromate අවදානම ඉහළයි**; PET හානිය |

**දෛනිකව** residual පරීක්ෂා කර වාර්තා තබාගන්න — SLSI audit එකට අවශ්‍යයි.

### ⚠️ 4. පිරිපහදුවෙන් **පසු** දූෂණය (post-contamination)

ජලය පිරිසිදුයි — නමුත් **බෝතලය, මූඩිය, වාතය** නිසා නැවත දූෂණය වේ.
- 🔴 **Oil-free / food-grade compressed air** (ISO 8573-1 Class 0) — සාමාන්‍ය compressor එකක් blow moulding/filling සඳහා **භාවිත කළ නොහැක**
- Bottle rinser — පිරිපහදු කළ ජලයෙන්ම (raw water වලින් නොවේ!)
- Cleanroom **positive pressure** + air filtration
- CIP — දෛනිකව; වාර්තා තබාගන්න
- Cap/bottle storage — ආවරණය, වියළි, දූලි රහිත

### ⚠️ 5. Filter media කල් ඉකුත් වීම — වාර්තා තබාගන්න

| Media / කොටස | ආයු කාලය | මාරු කිරීමේ සංඥාව |
|---|---|---|
| Sand (MGSF) | වසර 3–5 | Turbidity ඉහළ යාම, ΔP |
| **Activated carbon** | වසර 1–2 | **Chlorine breakthrough > 0.1 ppm** ⭐ |
| Softener resin | වසර 5–8 | Hardness breakthrough |
| **Micron cartridges (5µm)** | මාස 1–3 | ΔP > නිර්මාපක සීමාව |
| Micron cartridges (1µm, 0.5µm) | සති 2–8 | ΔP |
| **RO membranes** | වසර 2–5 | Normalised flux ↓ 15%, salt passage ↑ |
| **UV lamp** | පැය 9,000–12,000 (≈ වසර 1) | පැය ගණක; UV sensor |
| Ozone generator (tube/cell) | වසර 2–5 | O₃ output ↓ |
| **0.2 µm sterile filter** | Batch එකක් / සතියක් | ΔP; integrity test |

---

## 20.4 — ⭐ CCP — HACCP අවධි ලක්ෂ්‍ය | Critical Control Points

| CCP | උපද්‍රවය | සීමාව / Critical limit | අධීක්ෂණය | නිවැරදි කිරීම |
|---|---|---|---|---|
| **CCP 1** — MGSF | අංශු, iron | Turbidity < 1 NTU | සෑම පැය 4කට | Backwash; ඉදිරියට යාම නවත්වන්න |
| **CCP 2** — ACF | Chlorine (membrane හානිය) | Free Cl < 0.1 ppm | දෛනික + online | Carbon මාරු කරන්න; batch hold |
| **CCP 3** — RO | දියවූ ලවණ, බැර ලෝහ | Conductivity ≤ [___] µS/cm; TDS ≤ [___] | **Online, අඛණ්ඩව** | ඉදිරියට යාම නවත්වන්න; batch reject |
| **CCP 4** — UV | ක්ෂුද්‍ර ජීවී | Dose ≥ 40 mJ/cm²; lamp OK | Lamp hours + intensity alarm | Lamp මාරු කරන්න; batch hold |
| **CCP 5** — ⭐ **Ozone** | ක්ෂුද්‍ර ජීවී + shelf life | **0.2–0.4 ppm** at filler | **සෑම batch එකකම** | O₃ generator adjust; **batch නිකුත් නොකරන්න** |
| **CCP 6** — 0.2 µm filter | අවසාන බාධකය | ΔP within spec; integrity OK | Batch එකකට | Filter මාරු කරන්න; batch hold |
| **CCP 7** — Filling/capping | පිරිපහදුවෙන් පසු දූෂණය | Cleanroom ΔP (+); O₃ present | දෛනික | Line නවත්වන්න; CIP; batch hold |

> සියලු CCP වාර්තා **වසර 2ක්** තබාගන්න — FCAU/SLSI audit එකට අවශ්‍යයි, සහ **product recall** එකකදී ඔබේ එකම ආරක්ෂාව එයයි.

---

## 20.5 — SLS 894 අවසාන නිෂ්පාදන පරාමිතීන් | Finished product testing

සෑම batch එකක් සඳහාම (internal lab) + මාසික/අර්ධ-වාර්ෂික external verification:

| කාණ්ඩය | පරාමිතීන් |
|---|---|
| **භෞතික** | pH, Conductivity, TDS, Turbidity, Colour, Odour, Taste |
| **ක්ෂුද්‍ර ජීව** ⭐ | Plate count (22 °C, 37 °C), Total coliforms, *E. coli*, *Pseudomonas aeruginosa*, Fecal streptococci |
| **රසායනික** | Nitrate, Nitrite, Ammonia, Chloride, Sulphate, Hardness, Aluminium, Fluoride |
| **බැර ලෝහ** ⭐ | **Arsenic**, Lead, Cadmium, Chromium, Mercury, Manganese, Iron |
| **උප-නිෂ්පාදන** 🔴 | **Bromate** (ozonation නිසා), Trihalomethanes (chlorination කරන්නේ නම්) |
| **Ozone** | Residual at filling; 24h පසු |
| **Shelf life** | 6/12 මාස study — 30 °C + 40 °C storage |

👉 ඉලක්ක ප්‍රමිතිය: **SLS 894** (බෝතල් කළ පානීය ජලය)

---

## 20.6 — RO අවශ්‍යද? | Is RO strictly necessary?

**ඔව් — ශ්‍රී ලංකාවේ භූගත ජලය සඳහා ප්‍රායෝගිකව අනිවාර්යයි.**

| හේතුව | විස්තරය |
|---|---|
| TDS / hardness ඉහළයි | SLS 894 සීමාවන් තුළට ගෙන ඒමට RO පමණයි හැක්කේ |
| **Arsenic / fluoride** | උඩරට ඇතුළු ශ්‍රී ලංකාවේ ප්‍රදේශ රැසක භූගත ජලයේ තිබේ — **සාමාන්‍ය filtration වලින් ඉවත් නොවේ** |
| Nitrate (කෘෂි දූෂණය) | තේ/එළවළු වගා ප්‍රදේශවල |
| ක්ෂුද්‍ර ජීවී | RO membrane = 0.0001 µm බාධකය |
| නිෂ්පාදන නිරන්තරතාව | ළිඳේ ජල තත්ත්වය වෙනස් වුවද RO නිෂ්පාදනය ස්ථාවරව තබයි |

**නමුත්:** RO ජලය "හිස්" — රසක් නැත. එබැවින් **re-mineralisation** (පියවර 11) නිර්දේශ කරයි. මෙය වෙළඳපොළේ බොහෝ ප්‍රමුඛ බ්‍රෑන්ඩ් කරන දෙයයි.

---

## 20.7 — ජල මූලාශ්‍ර පරීක්ෂණයට **එකතු කළ යුතු** අමතර පරාමිතීන්

[Phase 3](04-phase-3-water-source-wrb.md) ලැයිස්තුවට **මේවා එකතු කරන්න** (RO සැලසුම් කිරීමට අත්‍යවශ්‍යයි):

- [ ] 🔴 **Bromide (Br⁻)** — bromate අවදානම තීරණය කරයි
- [ ] **Langelier Saturation Index (LSI) / Silt Density Index (SDI)** — RO membrane design
- [ ] සම්පූර්ණ cation/anion profile (Ca, Mg, Na, K, Cl, SO₄, HCO₃, CO₃)
- [ ] CO₂ / alkalinity
- [ ] Silica (SiO₂) — membrane scaling
- [ ] Barium, Strontium — scaling
- [ ] H₂S (අවශ්‍ය නම්)
- [ ] වසරේ **වියළි + වැසි** කාල දෙකෙහිම නියැදි

---

## 20.8 — ධාරිතාව ගණනය කිරීම | Sizing the treatment plant

```
නිෂ්පාදන අවශ්‍යතාව (m³/hr)
   ÷ RO recovery (උදා: 0.65)      = RO feed (m³/hr)
   ÷ පෙර-පිරිපහදු ඵලදාව (~0.95)  = ළිඳෙන් අවශ්‍ය ජලය (m³/hr)

උදාහරණය — 6,000 BPH × 1 L = 6 m³/hr නිෂ්පාදනය:
   RO feed    = 6 ÷ 0.65 = 9.23 m³/hr
   ළිඳෙන්     = 9.23 ÷ 0.95 = 9.7 m³/hr
   RO reject  = 9.23 − 6 = 3.2 m³/hr  (පැයට!) → දිනකට ~26 m³
                                        ⚠️ reuse plan අවශ්‍යයි
```

| BPH (1 L) | නිෂ්පාදනය m³/hr | RO feed m³/hr | ළිඳෙන් m³/hr | Reject m³/දින (8h) |
|---:|---:|---:|---:|---:|
| 2,000 | 2.0 | 3.1 | 3.2 | ~9.5 |
| 4,000 | 4.0 | 6.2 | 6.5 | ~19 |
| 6,000 | 6.0 | 9.2 | 9.7 | ~26 |
| 12,000 | 12.0 | 18.5 | 19.5 | ~52 |

> ⚠️ **ළිඳේ ඵලදායිතාව (yield) මෙයට වඩා වැඩි විය යුතුය** — සහ WRB අනුමත උපරිම නිස්සාරණය තුළ.

---

**⬅️ ආපසු:** [ලේබල් අවශ්‍යතා](19-label-requirements.md) | **➡️ ඊළඟට:** [තීරණ වාර්තාව](21-decisions-and-assumptions.md)
