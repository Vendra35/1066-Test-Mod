> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 29 (landed 2026-08-01,
> incl. the KLB catch the package missed).** Research record, not the state;
> code and HANDOFF item 29 win where they disagree.

# ARABIA — research package (DRAFT, pending main-session review)

Research pass 2026-07-30 (Opus subagent). **DRAFT — nothing here is
approved.** Every territory rule is resolved against
`in_game/map_data/definitions.txt` and the counts printed below are the
resolver's, not transcriptions. Every identifier carries a `file:line`.
Historical claims carry `[U]` (unattested/reconstructed) or `[D]`
(genuinely disputed between sources).

Runs any time after the Seljuk (items 16-18) and Fatimid (item 19)
slices, both CLOSED and confirmed in game. It has **no dependency on
Italy North or Germany II** and can be scheduled independently.

---

## 0. What the theater actually looks like right now

`arabia_region` (definitions.txt:2190-2313) holds **351 ownable land
locations** across seven land areas:

| area | land locs | current state |
|---|---|---|
| `hedjaz_area` | 79 | FAT holds the north coast (29, item 19); MEC 22; MDA 12; the rest tribal |
| `najd_area` | 67 | wholly tribal (BNL SBY MUT DWS KLB ANZ AAD ZIB) — untouched by any slice |
| `south_yemen_area` | 63 | YEM 56, DHF 7 |
| `north_yemen_area` | 51 | YEM 22, MEC 9, QHT 12, SBY 6, YAM 8, UTB 3 |
| `bahrein_area` | 32 | JRW 25, ORM 2, HLG 1, AAD 2, MRH 1, YAS 1 |
| `hail_area` | 30 | SHM 8, AAL 5, FDL 6, AMR 4, HUT 5, BNL 3 |
| `oman_area` | 29 | ORM 20, OMA 7, YAS 2 |

**Only the Hejaz has been touched.** Everything else in Arabia is
exactly vanilla's 1337 arrangement — verified by a location-by-location
mod-vs-vanilla diff (the only `<<CHANGED` rows in the whole region are
FAT's 29 in `duba/madian/qura/tabuk/umluj` provinces, ex-MAM).

### The four anachronisms and the one defect we caused

A global sweep found **18 tags that hold land but not their capital**.
Five of them are this theater's, and four of those five are also
1337-only polities:

| tag | vanilla name (`country_names_l_english.yml`) | holds | capital | owned by | verdict |
|---|---|---|---|---|---|
| ORM | "Ormus" :4405 | 22, ALL in Arabia | `hormuz` | SEL | Hormuzi conquest of Oman is 14th c. **RETIRE** |
| JRW | "Jarwanids" :4589 | 25 | `al_qatif` | itself | Jarwanid dynasty is 1305-1487. **REPLACE** |
| HLG | "Hüleguids" :4503 | **1** (`kazimah`) | `basra` | SEL | Ilkhanate, 1256+. **RETIRE** |
| FDL | "Āl Faḍl" :1970 | 6 | `tadmur` | HLB | Āl Faḍl amirate is 13th c. **RETIRE** |
| AAL | "Al 'Alī" :1964 | 5 | `qutayfah` | **FAT** | capital lost to OUR item-19 grant — **our defect** |

ORM/HLG/FDL/AAL's capital loss is entirely our doing (SEL took `hormuz`,
`basra` and `tadmur`; FAT took `qutayfah`). ANZ's capital
(`dumat_al_jandal`) is owned by AAL in **vanilla too** — that one is
Paradox's own, and this package fixes it for free.

`initialize_from_bookmark.cpp:2477` is already logged for HLG/QUN/SLD
(`docs/EU5-ERROR-DECODER.md:540-548`, "the real fix is the Arabia and
Central Asia slices retiring these tags properly").

### THE SEAM — HLG is ours, QUN/SLD are Central Asia's

Measured, not assumed. Total map-wide holdings:

* **HLG = 1 location, `kazimah`, in `bahrein_area/batin_province`.**
  Nothing else anywhere. Its retirement is 100% inside Arabia.
* **QUN = 6**: `araska kulob munk parun asadabad_kunar hajiabad`,
  capital `kabul` — all Central Asia.
* **SLD = 9**: `kelif hissar aiwanj basand darzanji denov qubodijon
  shuman termez`, capital `balkh` — all Central Asia.

**Written seam:** the Arabia slice retires HLG by granting `kazimah`
away and adding HLG to `LANDLESS_AFTER`. The Central Asia slice retires
QUN and SLD the same way. Neither package touches the other's tags.
Whichever lands second should re-read `initialize_from_bookmark.cpp:2477`
in the log and confirm only its own tags are gone.

---

## A. Registry additions (`in_game/setup/countries/zz_1066_new_countries.txt`)

**ONE new tag** (plus one optional). Tag freeness verified three ways —
whole-tree `rg -w` over the vanilla game (0 files), over the mod
excluding PDFs (0 files), and no `QMT:`/`QMT_ADJ:` loc key anywhere in
`main_menu/localization/english/`. Same three for `UKH`.

Note for the main session: **`QRM` is NOT available** — this mod already
uses it for the Taifa of Carmona (`zz_1066_new_countries.txt`, "Taifa of
Carmona"). `QAR` (14 vanilla files), `KRT` (20), `HSA` (127 — Hanseatic),
`LHS` (11), `AWA` (15), `KHD` (18) are all contaminated. `QMT`, `QRT`,
`AHS`, `AWL`, `BHR`, `UKH`, `YMM`, `YMA`, `UYN`, `OMN`, `NZW`, `SUH`,
`JLF` are all clean.

```
QMT = { #Qarmatians of al-Hasa
	color = map_QMT
	color2 = rgb { 16 41 202 }

	culture_definition = bahrani_culture
	religion_definition = shia
}
```

* `bahrani_culture` — `in_game/common/cultures/arabia.txt:31`. It is
  vanilla's own registry choice for this exact ground (JRW,
  `in_game/setup/countries/arabia.txt:9-14`). `culture_definition` IS
  the landed tag's primary culture (measured, KNOWLEDGE.md /
  `country.cpp:6166`), so **do not** repeat it in `accepted_cultures`.
* `religion_definition = shia` — `in_game/common/religions/muslim.txt:64`.
  There is no `ismaili` RELIGION; Ismailism is a religious *school*
  (`religious_schools/shia.txt:27`). Vanilla ships only `ibadi`
  (`muslim.txt:1`), `shia` (:64) and `sunni` (:123) in the Muslim file.
* `color2 = rgb { 16 41 202 }` — the shared Arabian secondary; every
  entry in `in_game/setup/countries/arabia.txt` uses it.

**OPTIONAL (Tier B, see OPEN DECISIONS #4):**

```
UKH = { #Ukhaydirids of al-Yamama
	color = map_UKH
	color2 = rgb { 16 41 202 }

	culture_definition = najdi_culture
	religion_definition = shia
}
```
`najdi_culture` is the template culture of `al_yamamah` and `diriyah`
(location_templates.txt); `shia` because the Banu Ukhaydhir were Zaydi
Alids (see #4).

### `main_menu/common/named_colors/zz_1066_map_colors.txt`

Both are NEW named colors. Neighbours to stay distinct from: JRW's
`map_kaliji` (retiring, but the name stays registered), OMA `map_omani`,
MEC `map_hijazi`, YEM `color_culture_yemeni`, SEL `map_seljukids`
(30 160 203), KRM vanilla.

```
	# The Qarmatian state of al-Hasa (Bahrayn) and, if taken, the
	# Ukhaydirid emirate of al-Yamama. Checked against map_kaliji,
	# map_omani, map_hijazi and map_seljukids.
	map_QMT = rgb { 168 62 78 }     # al-Hasa      Gulf carmine
	map_UKH = rgb { 122 104 176 }   # al-Yamama    Alid violet
```
(Both rgb triples must be re-checked absent from vanilla's 3744
`map_*` entries in `named_colors/02_map.txt` before writing — the taifa
batch's own procedure.)

### Harness

* `tools/verify_mod.py` `_GENERATOR_OK`: add `QMT` (and `UKH`) with a
  **tier-4 permanent** comment — the Qarmatian council and the
  Ukhaydirid emirate had no heraldry, exactly the taifa/Seljuk-client
  ground already recorded in that list.
* `check("coat of arms references resolve", …, min_count=94)` →
  **95** (96 with UKH).

---

## B. NEW_COUNTRIES blocks (`tools/build_setup.py`)

### QMT — Emirate of al-Ahsa (the Qarmatian state)

**The government question, measured — do NOT use the ABS/FAT
explicit-theocracy shape here.** `country_ranks.txt` is first-match-wins
and its theocracy block (lines 1430-1540) sits ABOVE the generic muslim
branch (`rank_duchy_muslim`, :1743). A `rank_duchy` + `theocracy` +
Muslim country with no reform therefore falls to
`localization_key = rank_duchy_theocracy` (:1533-1540), which vanilla
localises as:

```
government_names_l_english.yml:800  rank_duchy_theocracy: "Theocracy"
government_names_l_english.yml:801  rank_duchy_theocracy_prefix: "High"
government_names_l_english.yml:802  rank_duchy_theocracy_ruler_male: "High Priest"
```

i.e. "the High Qarmatian Theocracy", ruled by a "High Priest". The
theocracy shape works for ABS/FAT only because `rank_empire_theocracy`
(:296) is a key we already overrode to "Caliphate". Overriding
`rank_duchy_theocracy` would be tag-independent and would rename every
duchy-rank theocracy on the map.

A `monarchy` at `rank_duchy` falls through to `rank_duchy_muslim`
(country_ranks.txt:1742-1750, trigger `country_rank_is_duchy` +
`religion.group = religion_group:muslim`), which reads:

```
government_names_l_english.yml:781  rank_duchy_muslim: "Emirate"
government_names_l_english.yml:782  rank_duchy_muslim_ruler_male: "'Amīr"
```

So: **monarchy**, with `elective_succession` carrying the council of six
(`government_types/00_default.txt:9`, the monarchy type's own list).

```python
NEW_COUNTRIES["QMT"] = (
    "\tQMT = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_middle_east"\n'
    '\t\tinclude = "muslim_monarchy_no_abrahamic_dhimmi"\n'
    "\t\tgovernment = {\n"
    "\t\t\ttype = monarchy\n"
    "\t\t\their_selection = elective_succession\n"
    "\t\t\tlaws = {\n"
    "\t\t\t\tlegal_code_law = sharia_law_policy\n"
    "\t\t\t\tsharia_law = ismaili_policy\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t\treligious_school = ismaili_school\n"
    "\t\ttolerated_cultures = {\n\t\t\tkaliji_culture\n\t\t\tnajdi_culture\n\t\t}\n\n"
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = al_ahsa\n\t}\n")
```

Citations, field by field:
* `expl_middle_east` — `main_menu/setup/templates/expl_middle_east.txt`
  grants `arabia_region` (line 3 of its `discovered_regions`), which
  contains `al_ahsa`. Required, not decorative
  (`initialize_from_bookmark.cpp:528`, decoder :453).
* `muslim_monarchy_no_abrahamic_dhimmi` — the **coastal** variant. QMT
  holds `al_qatif`, `al_uqayr`, `al_jubayl`, `manama`, `al_bidda`;
  `diff muslim_monarchy_no_abrahamic_dhimmi.txt
  muslim_monarchy_no_abrahamic_dhimmi_no_coast.txt` shows the no_coast
  variant drops `heir_selection`, the `sponsor_maritime_contracts`
  advance, `maritime_law` and `piracy_law` — the coastal one is right
  and needs nothing restated. JRW uses this exact include today
  (10_countries.txt, JRW block).
* `elective_succession` — `government_types/00_default.txt:9`, inside the
  `monarchy` type's own `heir_selection` list. Restated explicitly on
  top of the template's `cognatic_primogeniture`; vanilla's own ORM
  block does exactly this (explicit `heir_selection` next to the same
  include).
* `ismaili_policy` — `laws/01_legal_system.txt:1102`. Its `potential` is
  `religion = religion:shia` + `religious_school ?= NOR { jafari_school
  zaidi_school }`, so `ismaili_school` passes. The pairing
  `ismaili_policy` + `ismaili_school` is vanilla's own at QHT
  (10_countries.txt:60609) and six others.
* `legal_code_law = sharia_law_policy` (`01_legal_system.txt:108`) MUST
  ride along — the `sharia_law` group's potential is
  `has_policy = sharia_law_policy` (:974); ABS shipped without it and
  the whole law was removed at init (`government.cpp:3535`, decoder :385).
* `ismaili_school` — `religious_schools/shia.txt:27`. `nizari_school`
  (:96) and `mustali_school` (:117) are post-1094 and wrong for 1066.
* `tolerated_cultures` — JRW's own list, unchanged. `kaliji_culture`
  (`cultures/arabia.txt:16`) is the actual template culture of every
  al-Ahsa/Qatar location; `najdi_culture` covers the Yabrin/Nita edge.
* `capital = al_ahsa` — the Qarmatian capital was al-Ahsa (Hofuf), not
  al-Qatif; the Uyunid siege of 1077 is the "Siege of Hofuf".
  `al_ahsa` is in `al_ahsa_province` ∈ `bahrein_area` ∈ `arabia_region`,
  so the build's capital-inside-granted-region assert passes.

### UKH — Emirate of al-Yamama (OPTIONAL, Tier B)

Inland (al-Yamama is the Wadi Hanifa, no coast):

```python
NEW_COUNTRIES["UKH"] = (
    "\tUKH = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_middle_east"\n'
    '\t\tinclude = "muslim_monarchy_no_abrahamic_dhimmi_no_coast"\n'
    "\t\tgovernment = {\n"
    "\t\t\their_selection = cognatic_primogeniture\n"
    "\t\t\tlaws = {\n"
    "\t\t\t\tlegal_code_law = sharia_law_policy\n"
    "\t\t\t\tsharia_law = zaidi_policy\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t\treligious_school = zaidi_school\n\n"
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = al_yamamah\n\t}\n")
```
`heir_selection` restated because the muslim `_no_coast` template drops
it (diff above — the `_seljuk_block` lesson).
`zaidi_policy` `01_legal_system.txt:1137`, `zaidi_school`
`religious_schools/shia.txt:52`; the pair is vanilla's own on MEC and
MDA today.

---

## C. Rulers

| tag | character key | name | accession | birth | regnal | dynasty | notes |
|---|---|---|---|---|---|---|---|
| QMT | `qmt_yahya_ibn_al_abbas` | `name_yahya` (`character_names_dynamic_l_english.yml:18702` → "Yahya") | 1058.1.1 **[U]** | 1020.1.1 **[U]** | 0 | **none** | See below. `[D]` on whether a single ruler is even the right model |
| MDA | `mda_al_husayn_ibn_muhanna` | `name_husayn` (`:9276` "Husayn", `:9277` `.arabic_language` "Ḥusayn") | 1060.1.1 **[U]** | 1025.1.1 **[U]** | 0 | `muhanna_dynasty` NEW | Husaynid emir of Medina, first named c. 1076/7 **[D]** |
| UKH | — | — | — | — | — | — | `ruler = random` deliberately: no 11th-c. Ukhaydirid is named in any source found |

Character shape is the mod's own (`05_characters.txt`,
`mec_muhammad_abu_hashim`):
```
	qmt_yahya_ibn_al_abbas = {
		first_name = { name = name_yahya }
		culture = bahrani_culture
		religion = shia
		birth_date = 1020.1.1
		birth = al_ahsa
		tag = QMT
	}
```
No `dynasty` line — the AQU/RAV/PAR precedent (Italy North package,
section C: patriarchs and archbishops carry none).

**Name-key rendering, verified.** All Arabian cultures use
`peninsular_dialect` (`cultures/arabia.txt:17,32,47` — `language =
peninsular_dialect`), which is a **dialect nested inside
`arabic_language`** (`in_game/common/languages/00_arabia.txt:61`). The
mod already proved the inheritance works: Abu Hashim rendered
"Šayḵ Muḥammad Hawāshim" in game (HANDOFF item 19), i.e. the
`name_muhammad.arabic_language` row (`:12935` "Muḥammad") reached a
`hijazi_culture` character. So `name_husayn` → "Ḥusayn" and
`name_yahya` → "Yahya" (no `.arabic_language` row, falls back to the
base row). **Nothing must be invented for these two.**

### Why Yahya ibn al-Abbas, and the honest caveat

Nasir Khusraw, who was physically in Lahsa in 1051, reports the
Qarmatian state governed by **a council of six descendants of Abu
Sa'id assisted by six viziers of the line of Ibn Sanbar** — there is no
single emir. The two Qarmatian leaders named at the state's fall
(executed by the Uyunids, 1077-78) are **Abu Abdullah ibn Sanbar** and
**Yahya ibn al-Abbas**. Yahya is the one attested holding and losing
Awal and Qatif, so he is the least-bad single face for 1066. `[U]` on
both dates; `[D]` on the whole idea of a named ruler here. The fallback
— `ruler = random` with a comment — is legitimate and costs nothing.

### Rulers deliberately NOT authored

* **ORM, JRW, HLG, FDL, AAL** — all going landless.
* **OMA** (Nizwa) — the Ibadi Fourth Imamate spans 1016-1164 by the
  wiki's own phase list, but it names no imam for the 1060s and no
  second source found one. Keep `ruler = random`.
* **The fifteen Najd/Hejaz tribal tags** — no named 1066 shaykhs.
* **MEC** — already seated (`mec_muhammad_abu_hashim`, item 19). Do not
  touch. His dates are confirmed: Abu Hashim Muhammad ibn Ja'far,
  sharif 1063-1094.
* **YEM** — already seated (`yem_ali_al_sulayhi`). See OPEN DECISION #7
  for a `[D]` on his death year that is worth one look.
* **KRM** — already seated with `krm_qawurd` from 1041 (10_countries
  .txt:53027). This is the historically correct conqueror of Oman —
  see section E.

---

## D. Dynasties (`main_menu/setup/start/04_zz_1066_dynasties.txt`)

Only if MDA is seated:

```
	# --- 1066 Medina: the Banu Muhanna, the Husaynid sharifs who held
	# the city from the late 10th century and read the Fatimid khutba.
	# Vanilla ships no Husaynid house at all.
	muhanna_dynasty = {
		name = { name = muhanna_dynasty }
		home = medina
	}
```
`home = medina` verified in definitions.txt (`medina_province`).
Loc row required (section H).

QMT needs **no** dynasty. UKH needs none (no ruler).

---

## E. Territory — `_ARABIA_RULES` (the `_SELJUK_RULES` sweep format)

Every count below was produced by re-running the build's own resolver
(`_parse_defs` + `_ownable_set` + `_resolve_ruleset`) against
`definitions.txt` and `location_templates.txt`. They are exact and can be
pasted straight into the expected-count slot.

```python
# tag: (sweep names, singles, minus-sweeps, minus-singles, expected)
_ARABIA_RULES = {
    "QMT": (["al_ahsa_province", "batin_province", "nita_province",
             "qatar_province", "yabrin_province"],
            [], [],
            ["hafar_al_batin", "mashdhubah", "sir_bani_yas", "yabrin"], 28),
}
```

**QMT = 28.** Resolved list, in resolver order:
```
al_ahsa al_jubayl al_qatif al_uqayr baqqa manama sayhat
ar_rukai ash_shuaybah kazimah qurain
nita_arabia al_suman al_uyayna jannah jarrarah qaryat_ulya
al_bidda al_huwaila al_mashqar al_udayd eglat_faisal zubarah
al_hunayy harad_al_ahsa khurays rumah urayrah
```
Donors, verified against the built `10_countries.txt`:
JRW 25 (all of them) + ORM 2 (`manama`, `sayhat` — vanilla marks these
JRW's `our_cores_conquered_by_others`, so this literally restores
vanilla's own pre-Hormuzi state) + HLG 1 (`kazimah`).
The four minus-singles are the desert tribes we deliberately leave:
`hafar_al_batin`/`mashdhubah` (AAD), `sir_bani_yas` (YAS), `yabrin` (MRH).

### The plain grants (`LOCATION_GRANTS` style, existing tags)

```python
_ARABIA_GRANTS = {
    # Oman — see OPEN DECISION #2 for which of these two lines ships
    "KRM": ["suhar", "al_khaburah", "khor_fakkan", "nakhal", "rustaq",
            "saham", "shinas",
            "masqat", "al_kamil_wal_wafi", "as_sib", "jalan_buani_buali",
            "masirah", "qalhat", "sur"],                          # 14
    "OMA": ["julfar", "abu_dhabi", "al_ayn", "al_dhaid", "dubai",
            "sharjah"],                                            # 6
    # The Darb Zubayda — see OPEN DECISION #3
    "HLL": ["zubala", "al_labbah", "al_thulayma", "al_waqbi",
            "linah", "lowqah"],                                    # 6
    # Jawf: retires AAL AND fixes ANZ's vanilla-side capital defect
    "ANZ": ["dumat_al_jandal", "aba_al_qur", "al_hamad", "arar",
            "sakaka"],                                             # 5
}
```
14 + 6 = exactly ORM's remaining 20 after QMT takes `manama`/`sayhat`;
HLL's 6 = exactly FDL's holding; ANZ's 5 = exactly AAL's holding. Every
donor empties to zero, which is what `LANDLESS_AFTER` asserts.

**Resolver output for each, verbatim:**
```
KRM+ (batina+masqat): 14 -> suhar al_khaburah khor_fakkan nakhal rustaq saham shinas
                            masqat al_kamil_wal_wafi as_sib jalan_buani_buali masirah qalhat sur
OMA+ (julfar six):     6 -> julfar abu_dhabi al_ayn al_dhaid dubai sharjah
HLL+:                  6 -> zubala al_labbah al_thulayma al_waqbi linah lowqah
ANZ+:                  5 -> dumat_al_jandal aba_al_qur al_hamad arar sakaka
```

### The Oman case (why KRM, not a new tag)

1066 Oman splits cleanly and the mod already owns both halves.

* **The coast was Seljuk.** Kerman was Qavurd's hereditary fief from
  1041, "and to Kerman belonged also the opposite coast of Oman, which
  enjoyed well-ordered government until 1170" (1911 EB, *Seljūks*);
  Qavurd's conquest of Oman is dated 1053 or 1063 **[D]** — either way,
  before 1066. Seljuk dominance ends in 1154 with the Nabhani revolt,
  which is why the Nabhanis are wrong for us.
* **The interior was Ibadi.** OMA already holds `nizwa_province` (7)
  with `ibadi_policy`/`ibadi_school` — leave it exactly as it is.
* **KRM is already seated with the right man.** `krm_qawurd` from
  1041.1.1 (10_countries.txt:53027-53028), `dynasty = seljukids_dynasty`
  (via the existing `FIELD_FIXES["KRM"]`), and KRM is already a SEL
  tributary (`SELJUK_TRIBUTARIES`). Granting Oman's Batinah and Muscat
  to KRM needs **no new tag, no new ruler, no new dynasty and no new
  diplomacy** — the whole Seljuk-Oman fact lands as 14 location moves.
* `julfar_province`'s six (Julfar, Sharjah, Dubai, Abu Dhabi, al-Ayn,
  al-Dhaid) are the Trucial coast, not the Batinah; they were never
  meaningfully Kerman-governed. To OMA, whose `our_cores_conquered_by_others`
  list already claims the Batinah. (Note `julfar`'s template culture is
  `shihhi_culture`, not `omani_culture` — a pop-phase detail, not a
  border argument.)

### The Darb Zubayda case (FDL's six)

`zubala_province` is the Kufa→Mecca pilgrim road (Darb Zubayda):
`zubala al_labbah al_thulayma al_waqbi linah lowqah`. The Āl Faḍl who
hold it in 1337 are a 13th-century Mamluk-era creation. In the 1060s
the desert between Kufa and Najd was the Mazyadid (Banu Asad) sphere
out of Hilla — and **HLL is already seated with `hll_dubays_i` from
1018** (10_countries.txt:30391-30392) and is already a SEL tributary.
Six locations doubles a 7-location client, which is proportionate for a
Bedouin amirate whose whole basis was desert control. Alternatives in
OPEN DECISIONS #3.

### The Jawf case (AAL's five)

Two defects, one grant. AAL's capital `qutayfah` went to FAT in item 19;
ANZ's capital `dumat_al_jandal` has **never** been ANZ's, in vanilla or
here. Granting AAL's five Jawf locations to ANZ retires the 13th-century
Āl ʿAlī, gives ANZ the capital vanilla clearly meant it to have, and
leaves the Jawf oasis under a Najdi tribal tag — which is what
Dumat al-Jandal was in 1066 **[U]**.

### `LANDLESS_AFTER` additions

```python
ARABIA_LANDLESS = ("ORM", "JRW", "HLG", "FDL", "AAL")
```
None of the five appears in any existing landless tuple (checked against
`SELJUK_LANDLESS`'s 60, `BYZ_LANDLESS`'s 45, `EGYPT_LANDLESS`,
`FRANCE_LANDLESS`, `BRITISH_LANDLESS`, `ITALY_LANDLESS`,
`EMPIRE_LANDLESS`, `GERMANY_LANDLESS`) — so the build's
"stale entry" assert stays quiet.

All five keep their registry identity and get claims equal to what they
held at build time (the GRA/POR shape the build automates). **One
optional refinement:** ORM's snapshot will be its 22 Arabian locations
only, because the Seljuk slice already took `hormuz`, `kish`, `minab`
etc. A Kingdom of Hormuz whose irredenta excludes Hormuz reads oddly. If
the main session wants it right, a `DISPLACED_CLAIMS["ORM"]` entry with
vanilla's own 36 is available:
```
hormuz gamrun bandar_charak bandar_khamir bandar_lengeh kish minab
manujan nowdezh rudkhaneh shaqrud senderk sirik julfar al_dhaid
khor_fakkan shinas machul abu_dhabi al_ayn dubai sharjah masqat
al_kamil_wal_wafi as_sib jalan_buani_buali masirah qalhat sur suhar
al_khaburah nakhal rustaq saham manama sayhat
```
(Same option exists for HLG's vanilla 31 and FDL's vanilla 27 — both of
which are mostly Iraq/Syria and arguably better left as the build's
automatic Arabia-only snapshot. Recommend ORM only.)

---

## F. Include and field swaps (`FIELD_FIXES`)

```python
    # Oman's coast makes Kerman a maritime power — the template's
    # no_coast variant drops sponsor_maritime_contracts, maritime_law
    # and piracy_law (diff-measured against
    # muslim_monarchy_no_abrahamic_dhimmi.txt). KRM's block already
    # states heir_selection explicitly, so the coastal variant's own
    # heir_selection line is a harmless duplicate (vanilla's ORM block
    # does the same).
    "KRM": [('include = "muslim_monarchy_no_abrahamic_dhimmi_no_coast"',
             'include = "muslim_monarchy_no_abrahamic_dhimmi"')],
    # Al-Sulayhi moved his capital to Sana'a in 1063; Zabid was taken in
    # 1060 and is the Najahid seat, not his.
    "YEM": [("capital = zabid", "capital = sana_yemen")],
```

**Before writing the KRM line, check the log.** KRM's grant of
`kerman_area` in the Seljuk slice already gave it `minab`, `sirik` and
`senderk` on the Strait of Hormuz while its include stayed `_no_coast`.
If `government.cpp:3662` already names KRM in the current error.log
(the "coastal template on an inland country" class, in reverse — decoder
:390), this swap is a **bug fix that predates Arabia**, and the existing
`FIELD_FIXES["KRM"]` entry is the place for it. Say so in the commit.

`YEM: capital = zabid → sana_yemen` — `sana_yemen` is already YEM's
`own_control_core` and `sulayhid_dynasty`'s `home`
(04_zz_1066_dynasties.txt:37-40), so nothing else moves.

**No include swaps for the five landless-goers.** They join the accepted
landless-trim class, exactly like the Seljuk slice's 60 donors, rather
than the four big British/Iberian `_not_present` swaps.

**Optional (see OPEN DECISION #6):**
```python
    # The Husaynid sharifs of Medina were Twelvers, not Zaydis.
    "MDA": [("sharia_law = zaidi_policy", "sharia_law = jafari_policy"),
            ("religious_school = zaidi_school",
             "religious_school = imamiya_school")],
```
`imamiya_school` `religious_schools/shia.txt:75`; `jafari_policy`
`01_legal_system.txt:1120`, whose potential NORs `ismaili_school` and
`zaidi_school` — `imamiya_school` passes. Vanilla uses
`imamiya_school` at 10_countries.txt:60253 and JRW uses it with no
`sharia_law` line at all, so the pairing is legal either way.

---

## G. Diplomacy (`build_diplomacy`)

**Automatic — nothing to write, one constant to move.** The two 1337
lines crossing Arabia both name ORM as `first`, and ORM goes landless:

```
12_diplomacy.txt:276  dependency = { first = ORM second = JSK subject_type = vassal }
12_diplomacy.txt:618  dependency = { first = ORM second = JRW subject_type = vassal }
```

Both die in the existing landless-dependency auto-strip, so
`if n_landless_deps != 112` becomes **114**. Observe the printed count
and move the constant — do not pre-guess it if anything else in the
batch changes.

JSK survives landed (`bandar_e_jask`, `jagin_zir`) and simply becomes
independent, which is right — a Baluch coastal tribe owed Hormuz nothing
in 1066.

`12_diplomacy.txt:620 scripted_mutual = { first = QHT second = DWS type = alliance }`
is a harmless tribal alliance between two tags we leave alone. **Keep.**

**One addition:**
```python
FATIMID_TRIBUTARIES = ("MEC", "BKZ", "MDA")
```
The Sharifate of Medina recognised Fatimid suzerainty in the khutba
continuously from 974 to 1151 — the same relationship, from the same
caliph, that MEC and BKZ already model. FAT already carries
`fatimid_khutba_reform` (`allow_tributary_subject`), MDA is a Muslim
monarchy exactly like MEC, and MEC/BKZ are **confirmed working in game**
(HANDOFF item 19, screenshots: own colours, open war screens). Zero new
mechanism. The harness's
`check("new-tag tributary overlords pass the subject-type gate", …)`
covers it.

**No tributary for QMT.** The Qarmatians acknowledged no one in 1066 —
that is the whole point of the state. Independent is correct.

**No tributary for OMA.** Its overlord in fact was Kerman, but KRM
carries no khutba reform and adding one to a client to model a
sub-client is not worth it. The Ibadi imamate as a small independent is
fine.

---

## H. Localisation (`main_menu/localization/english/1066_norman_conquest_l_english.yml`)

Append to the existing file (never a second file — the duplicate-filename
shadowing rule). All values on ONE physical line.

```
 QMT: "al-Hasa"
 QMT_ADJ: "Qarmatian"
```
Rationale: the map label for a duchy-rank Muslim monarchy composes as
`<prefix> <ADJ> <rank noun>` → "Qarmatian Emirate", and the country panel
reads "al-Hasa". Naming the tag "Qarmatians" would give "Qarmatians
Emirate" in the panel-adjacent strings.

If UKH ships:
```
 UKH: "al-Yamama"
 UKH_ADJ: "Ukhaydirid"
```
If MDA is seated:
```
 muhanna_dynasty: "Banū Muhannā"
```
(Form follows the file's own Arabic house rows — `uqaylid_dynasty:
"Banū ʿUqayl"` :162, `mirdasid_dynasty: "Banū Mirdās"` :164.)

**Nothing must be invented for names.** `name_yahya` and `name_husayn`
both ship with vanilla loc rows (`character_names_dynamic_l_english.yml`
:18702 and :9276). `name_yahya` is absent from every
`in_game/common/languages/*.txt` male-name list — that governs *random
generation only*, not an explicitly-named character, so it is not a
problem; note it in a comment so nobody "fixes" it later.

**ORM/JRW/HLG/FDL/AAL keep their vanilla loc.** No rows to add or
remove — landless tags render fine (the GRA/POR/MLL precedent).

---

## I. Left alone deliberately — and the argument for each

### Najd's fifteen tribal tags: LEAVE

`SHM ANZ MUT UTB HRB SBY DWS QHT BNL AAD HUT MRH AZF ZIB KLB` (and
`YAM`, `YAS`) are all early-modern or modern confederations projected
back to 1337 by Paradox. Replacing them with 11th-century names (Tayy,
Banu Numayr, Banu Khafaja, Banu Hilal, Banu Sulaym) would mean ~15
invented tags with **no location-level evidence** for any of their
borders — precisely the Pecheneg case the project already decided.
Three further reasons:

1. Vanilla's own quilt is not wrong in *kind* — 1066 Najd genuinely was
   a bedouin patchwork with no state, and that is what the map shows.
2. At least one placement is arguably right in spirit: **SHM sits on
   `hail`**, i.e. Jabal Aja/Salma, which in the 11th century was Tayy
   country — and Shammar claims Tayy descent.
3. Everything gained would be cosmetic; nothing in the tribal quilt
   produces an error line or a broken tie.

**Bank as a possible later "Najd tribal renaming" pass**, priced as
loc-only work (rename existing tags via loc override, no territory
moves) if the user ever wants it.

### AMR (Al Mira): LEAVE

Holds `hawran_province` (7, Levant) plus four Wadi Sirhan locations that
happen to fall inside `hail_area`. Same 13th-century class as FDL and
AAL, but its capital `irbid` is its own, it produces no error, and the
Hawran is Levant business that the Fatimid slice deliberately left. If a
future Levant pass retires it, the four Sirhan locations come with it.

### The Hejaz interior: ALREADY CORRECT — no carve needed

This is the package's most useful negative finding. HANDOFF's open
thread reads "the Hejaz interior (Mecca/Medina proper) belongs to the
Arabia slice", which implies something is missing. It is not:

* **MEC already holds Mecca and Jeddah** (`mecca_province` whole: `mecca
  al_jumum al_lith dhat_irq ghumayqah jeddah yalamlam`) plus
  `khulays_province`'s six and `hali_province`'s nine — 22 locations
  under a seated Abu Hashim.
* **MDA already holds Medina and Yanbu** (`medina al_furaish` +
  `yanbu_province`'s six + `al_thamad buwat shajwa` + `al_ais`) — 12.
* The remaining interior (Khaybar, Fadak, al-Hinakiyah, al-Rabadha,
  Taif) sits with ANZ/AZF/ZIB/MUT/HRB/UTB — and in 1066 that interior
  genuinely **was** bedouin (Harb, Sulaym, Muzayna). Leaving it tribal
  is the historical answer, not a gap.

The real Hejaz work is therefore not territory at all: it is MDA's
ruler, MDA's Fatimid tie, and the two optional edges below.

### YEM: extent is RIGHT for 1066.9.15, capital is wrong

Checked against the actual chronology:
* Ali al-Sulayhi took **Zabid in 1060** and drove Najah's sons to
  Dahlak; the Najahid restoration is **1081**, fifteen years after our
  start. So YEM holding `zabid_province` is correct — the Najahid
  conflict is live but the Najahids are in exile. There is no land for a
  Najahid tag: Dahlak exists only as the sea zone
  `dahlak_archipelago` (`red_sea_area/eritrean_coast_sea_province`),
  never as an ownable location.
* **Aden** fell in 1061-62; the **Zurayids** are 1080. YEM holding
  `aden_province` is correct.
* Hadramawt and Sana'a: "by 1063 he had unified the entire country of
  Yemen". Correct.
* Only the **capital** is wrong — see FIELD_FIXES.

**DHF (Dhofar/Mahra, 7 including Socotra): LEAVE.** The Mahra tribes
were effectively independent; the Manjawi/Habudi dynasty of Zafar is
later. `ruler = random` is honest.

**QHT/YAM (Najran, Tathlith): LEAVE.** Najran under the Banu al-Harith
in a Sulayhid orbit — no land-level evidence for a carve.

### Bahrain island (Awal): a tag we do NOT take

Two members of the Abd al-Qays, **Abu al-Bahlul al-Awwam** and his
brother **Abu'l-Walid Muslim**, revolted on Awal and re-established
orthodox Islam on the islands — but the date is a live conflict: several
sources say **1058**, Wikipedia's own *Overthrow of the Qarmatians* says
**1068** **[D]**, and the same article has Awal changing hands three
times (Abu al-Bahlul → Yahya ibn al-Abbas → Abdullah ibn Ali) before
1077. Committing a tag to `manama` on a date that may be two years after
our start is exactly the wrong kind of confidence. `AWL` and `BHR` are
both verified free if a future situation ever wants to *earn* it — which
is the better home for it anyway: **the fall of the Qarmatians
(1058-1078) is first-class situation material**, with the Uyunid revolt,
the seven-year war, the Seljuk intervention and the Siege of Hofuf all
inside the first twelve years of the game.

---

## OPEN DECISIONS — every one is the user's, each with a recommendation

**#1 — Does the Qarmatian state get a new tag at all, or does JRW just
get re-localised?**
Reuse would mean keeping `JRW` (registry, colour, CoA, 25 locations) and
overriding `JRW:`/`JRW_ADJ:` to "al-Hasa"/"Qarmatian" — zero new tags,
zero new colours, zero harness changes. Against it: JRW is a *named
dynasty* tag ("Jarwanids"), and the mod already learned from GRZ that
reuse bites when the tag carries other data; the Jarwanid emirate is a
genuine 1305+ polity that a later formable or event might legitimately
want.
**RECOMMEND: new tag QMT**, JRW joins the landless class with its 25
locations as claims — its own future, expressed as irredenta, exactly
like GRA.

**#2 — Oman: who gets the coast?**
* **O-1 (recommended):** KRM takes the Batinah + Muscat (14); OMA takes
  the Trucial six (`julfar` etc.); ORM landless. Historically exact,
  reuses a seated tag with the correct ruler, needs one include swap.
* **O-2:** OMA takes all 20 — one Omani state of 27, simplest map,
  but wrong: the coast was not the imamate's in 1066, and it hands the
  Ibadis a Gulf navy they did not have.
* **O-3:** KRM takes all 20 including Julfar. Cleaner border, weaker
  history on the Trucial coast.
**RECOMMEND O-1.**

**#3 — FDL's six Darb Zubayda locations go to…?**
* **HLL (recommended)** — Mazyadids of Hilla, seated `hll_dubays_i`, the
  Bedouin power of the Kufa desert in the 1060s. Cost: touches a CLOSED
  Seljuk-slice tag's border (permitted by the brief, argued here).
* **UQY** — Uqaylids of Mosul, also seated, also Bedouin, but their axis
  is the Jazira, not the pilgrim road.
* **SHM** — Shammar; keeps the whole change inside Arabia and touches no
  closed tag. Lowest blast radius, weakest history.
**RECOMMEND HLL**; take SHM if the main session would rather not reopen
a closed tag's border at all.

**#4 — Does al-Yamama get the Ukhaydirid emirate (new tag UKH, 6
locations from KLB/SBY)?**
For: Nasir Khusraw was physically in al-Yamama in **1051** and found the
Banu Ukhaydhir still ruling — a first-hand source fifteen years before
our start, and a Zaydi Alid emirate is genuinely characterful.
Against: the same source-set says the record "becomes obscure" after
that and "the Banu Kilab eventually took control sometime after 1051"
— so KLB, vanilla's own tag, is a defensible reading of 1066 **[D]**;
and no 11th-century Ukhaydirid ruler is named anywhere, so the tag would
ship `ruler = random`.
Resolved extent if taken: `al_yamamah al_hajr diriyah malham thadiq
ad_dilam` = **6** (donors KLB 5, SBY 1), capital `al_yamamah`.
**RECOMMEND: TAKE, as Tier B** — it is the one place in Najd with a
solid anchor, and "Najd deserves exactly one state" is a better answer
than "Najd is fifteen tribes". **Drop it without argument if the session
wants the slice minimal**; nothing else depends on it.

**#5 — Is QMT a monarchy ("Emirate"/"'Amīr") or a republic
("Republic"/"Consul")?**
The theocracy shape is ruled out on measured evidence (section B). That
leaves monarchy — which renders `rank_duchy_muslim` "Emirate"/"'Amīr"
(government_names_l_english.yml:781-782) — or `republic` +
`oligarchic_elective` (`government_types/00_default.txt:41`) via
vanilla's own `muslim_republic` template (used by 2 vanilla tags),
which renders `rank_duchy_republic` "Republic"/"Consul" (:693,:695).
"The Qarmatian Republic" is genuinely the standard historiographic
label, and a council of six IS an oligarchy — but "Consul" of al-Hasa
is jarring, and fixing it would need a tag-independent loc override.
**RECOMMEND: monarchy with `heir_selection = elective_succession`** —
right title, elective succession carries the council, no loc override.

**#6 — Does MDA's school change from Zaydi to Twelver?**
The Sharifate of Medina "maintained Twelver Shi'ism" per its own
article; vanilla gives MDA `zaidi_policy`/`zaidi_school`. Two lines of
`FIELD_FIXES`, no other consequence. `[D]` — the distinction between
Zaydi and Imami among 11th-century Hejazi Alids is not sharp.
**RECOMMEND: yes, but it is genuinely optional** — bundle it or drop it
without cost. (MEC's `zaidi_school` is **correct** and must not change:
the Meccan sharifs were Zaydi until the Ayyubids.)

**#7 — Ali al-Sulayhi's death year: is our seat safe? (worth one look,
not a reopening)**
YEM is CLOSED and seated. But Wikipedia's infobox gives his death as
**1066** at al-Mahjam, killed by Sa'id al-Ahwal while riding to the
hajj; the conventional date is **459 AH**, which begins 22 Nov 1066 —
i.e. *after* our 1066.9.15 start; and a minority reading is 473/1081
**[D]**. If the 1066 reading is the right one and the ambush fell before
15 September, we have seated a dead man. **RECOMMEND: one targeted
source check by the main session**; if the pre-September reading wins,
the fix is not a re-seat but an *event* — his assassination in the first
months is superb 1066 content either way.

**#8 — Does MEC take Taif (4 locations from UTB)?**
Taif was the sharifate's summer seat and grain source, but in 1066 it
was tribal ground (Banu Sa'd, Hudhayl) with Meccan influence rather than
Meccan rule **[D]**. Resolved: `taif al_kharabah al_mahani bani_saad`
= 4.
**RECOMMEND: NO** — Pecheneg discipline; no location-level anchor.

**#9 — Does the Asir/Tihama coast leave MEC for a Sulaymanid tag?**
The **Sulaymanids** — Hasanid sharifs, "ruled around 1063-1174", centre
at Jazan, sphere the Mikhlaf Sulaymani (northern Tihama + Asir) — are a
real 1066 polity, and Hamza ibn Wahhas was expelled from Mecca c.
1063-69 by the Sulayhids. A carve would take MEC's `hali_province` 9 and
YEM's `jazan_province` 6 = 15 into a new tag. Against: it cuts a CLOSED
tag (YEM) and MEC's bulk, on a dynasty whose 1066 borders are not
attested at location level **[D]**.
**RECOMMEND: NO in this pass. Bank it** as a Tier-C option and as
situation material (the Sulayhid–Sulaymanid–Najahid triangle is the
Red Sea's 1060s-80s story).

**#10 — Does MEC's overlord stay FAT, or become YEM?**
Al-Sulayhi conquered Mecca by 1064 and "installed a client king there";
Abu Hashim, our seated sharif, is that client. So the *physical* overlord
in 1066 is Yemen, not Egypt.
Against changing it: the **khutba** — the thing the mechanism actually
models — was read for al-Mustansir, and al-Sulayhi was himself a Fatimid
daʿi who "shifted Yemen's loyalty to the Cairo-based Fatimid Caliphate"
in 1062. FAT is the correct top of the chain, and chaining MEC under YEM
would need a second `allow_tributary_subject` reform on YEM (HANDOFF
item 19 already parked this).
**RECOMMEND: keep FAT→MEC unchanged.**

**#11 — HLG's `type = army` after retirement.**
Retiring HLG to landless is certain. Whether
`initialize_from_bookmark.cpp:2477` stops is not: 33 tags in the built
file carry `type = army`, and it is unverified whether the engine still
tries to raise regiments for a landless one.
**RECOMMEND: land the landless retirement alone, read the log, and only
then decide** whether a `FIELD_FIXES["HLG"]` stripping `type = army` is
needed. Update the decoder entry at :540 either way — that entry
explicitly names this slice as its owner.

**#12 — Does ORM get a `DISPLACED_CLAIMS` entry?**
Default behaviour gives it claims over the 22 Arabian locations it holds
right now, which excludes Hormuz itself.
**RECOMMEND: yes, ORM only** — vanilla's full 36 (listed in section E).
HLG and FDL keep the automatic snapshot; their vanilla holdings are
mostly Iraq and Syria and belong to nobody's irredenta at 1066.

---

## Headline numbers if everything recommended ships

| item | count |
|---|---|
| new tags | 1 (QMT), 2 with UKH |
| tags retired to landless | 5 (ORM JRW HLG FDL AAL) |
| locations moved | 59 (QMT 28, KRM 14, OMA 6, HLL 6, ANZ 5), 65 with UKH |
| new characters | 1 (MDA), 2 with QMT's Yahya |
| new dynasties | 1 (`muhanna_dynasty`) |
| new diplomacy lines | 1 (`FATIMID_TRIBUTARIES` += MDA); 2 auto-stripped |
| `FIELD_FIXES` entries | 2 required (KRM include, YEM capital), 1 optional (MDA school) |
| new loc rows | 3 (QMT, QMT_ADJ, muhanna_dynasty), 5 with UKH |
| harness constants to move | `n_landless_deps` 112→114; CoA `min_count` 94→95 |
| capital-not-owned defects fixed | 5 (ORM JRW→n/a, HLG FDL AAL retired; **ANZ fixed outright**) |

Arabia after the slice: **FAT** on the northern Hejaz coast, **MEC**
(tributary) at Mecca, **MDA** (tributary) at Medina, **QMT** the
Qarmatians on the Gulf, **KRM** on the Oman coast and **OMA** in the
Ibadi interior, **YEM** from Sana'a over all Yemen, **DHF** on the
Mahra coast — and a bedouin Najd that is bedouin because it was.
