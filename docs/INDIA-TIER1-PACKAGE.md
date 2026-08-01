> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 34 (landed 2026-08-01).**
> Research record, not the state; code and HANDOFF item 34 win.

# INDIA TIER 1, 1066 — research package (DRAFT)

**DRAFT — pending main-session review. Nothing here has been written into the
repo.** Produced by an Opus research agent, 2026-08-01, on top of commit
`c3b34d8` (China-East). Every mechanical claim carries a `file:line` or a
count from a resolver run reproduced below. Historical claims that no file can
settle are flagged `[U]` (unverified — the agent's history) or `[D]` (sources
genuinely differ), never asserted silently.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game` — probed
live, `VAN/in_game/map_data/definitions.txt` present, 491,179 bytes.
`MOD = .../1066 Test Mod` — owners read from the GENERATED
`main_menu/setup/start/10_countries.txt` (built 2026-08-01 16:40).

## 0. Method, and the positive every scan was proven on

Four parsers, each a reimplementation of the build's own, not a regex over
lines:

| what | mirrors | proof |
|---|---|---|
| `definitions.txt` → `name -> [members]` + `child -> parent` | `tools/build_setup.py:690-713` (`_parse_defs`) | 5,226 container names resolved; `south_asia` yields exactly the five India regions |
| `location_templates.txt` → ownable set (a block with a `culture` field) | `tools/build_setup.py:715-723` (`_ownable_set`) | 20,922 ownable, the same figure the Central Asia package measured |
| `10_countries.txt` → `tag -> [locations]` via `OWN_KEYS` + `COUNTRY_RE` | `tools/build_setup.py:4543-4547`, `:4401` | **DLH resolves to 272 and GHZ to 131 — the two numbers the task brief states as current. That is the known positive.** |
| ruleset resolution (sweeps, singles, minus-sweeps, minus-singles) | `tools/build_setup.py:756-786` (`_resolve_ruleset`) | reproduces `_CENTRALASIA_RULES`' shipped QRK=46 / QRA=142 / BLH=28 |

All files opened `encoding='utf-8-sig'`. Comments masked before token scans —
`#Lost 1204`-style notes contain real location names (`van`, `split`, `kars`),
the lesson `tools/build_setup.py:4550-4556` already encodes.

One artefact worth recording: the ownership index reports ten locations owned
twice (MOR/TLE ×4, TEU/LIT ×6). Those are vanilla's own occupation pairs —
`control` on one tag, `own_*` on another — and none is in South Asia. They do
not affect a single count below.

### The theater as it stands today

South Asia is **1,230 ownable locations** in five regions. Resolved, with
current owners:

| region | ownable | the shape of the problem |
|---|---|---|
| `hindustan_region` | 333 | DLH 95 (awadh 24, bhojpur 24, rokhilkhand 12, doab 35); GHZ 97 in the Punjab (ours, correct) |
| `bengal_region` | 289 | DLH 25 (mithila 19, jharkhand 6); GAU 17 + SGN 19 + STN 19 — the Bengal **Sultanate** |
| `central_india_region` | 133 | DLH 57 (malwa 35, gondwana 13, vidarbha 9) |
| `western_india_region` | 151 | DLH 33 (rajputana 21, gujarat 12); SMA 25 in Sindh |
| `deccan_region` | 324 | DLH 62 (maharashtra 37, karnakassala 15, konkan 9, telingana 1); VIJ 36, MAB 26, RDY 18, RCH 15, MSN 20, SMV 7, DBD 21, JFN 4 |

**The 1066 map has no Chola, no Chalukya, no Pala, no Paramara and no Solanki
— and a Delhi Sultanate, a Vijayanagara, a Madurai Sultanate and a Bengal
Sultanate that are between 140 and 290 years early.** This package closes both
halves of that in one slice.

### One correction to `docs/INDIA-CHINA-REVIEW.md` §3

The review's retirement list of nine (VIJ MAB SMA RDY RCH JFN **DBD** SMV MSN,
172 locations) treats DBD as impossible. It is not. `DBD` is
`culture_definition = sinhalese` + `religion_definition = theravada`
(`VAN/in_game/setup/countries/india.txt:679-685`) — the *only* Sinhalese
identity block vanilla ships, and exactly the identity a 1066 Sinhalese
kingdom needs. **DBD survives, renamed, holding Ruhuna** (§E.1). Only the tag
NAME ("Dambadeniya", a 1220s foundation) and the capital are wrong.

The review also missed three tags of the same class: **GAU, SGN and STN** —
Gaur/Lakhnauti, Sonargaon and Saptagram, the three divisions of the *Bengal
Sultanate*, all `religion_definition = sunni`
(`VAN/in_game/setup/countries/bengal.txt:9-23`), independent Bengal being a
1338 event [U]. They hold 55 locations that must be Pala at 1066. Retiring
them is not scope creep; leaving them while retiring VIJ would be the same
inconsistency the review's own D6 argues against.

---

## A. Registry additions (`in_game/setup/countries/zz_1066_new_countries.txt`)

Five new tags. **Freeness proven in BOTH modes for each**, the audit-D3
discipline:

1. **word-boundary** `\bTAG\b` over **16,290 vanilla text files** and the
   whole mod repo — zero matches;
2. **substring** `_TAG\b | \bTAG_ | _TAG_` over the same two trees — zero
   matches. This is the mode that sees `map_TAG` in `named_colors`,
   `TAG_ADJ`/`TAG_RU_GEN_CL` in loc, `country_history_TAG`, `coa_def_TAG`;
3. cross-checked against a 2,481-entry registry built from every identity
   block in `VAN/in_game/setup/countries/` + the mod's overrides, every tag
   block in both `10_countries.txt`, and every `tag =`/`country =` in
   `VAN/in_game/common/formable_countries/00_formable_countries.txt`.

Ten further candidates cleared all three gates and are **banked**: `CKY`
`CHY` `KLY` `PLI` `PMA` `VNG` `CLY` `CYL` `TJR` `CDM` `GUD` `CLU` `GRJ`
`VGR`. The obvious ids are all consumed and this is worth writing down so the
next slice does not re-derive it: **`CHO` is Kongo's** (`kongo.txt:62`),
**`COL` is Coligua** (`central_north_america.txt:169`), **`CLA` is Clare**
(`british_isles.txt:47`), **`PAL` is the Palatinate** (`south_germany.txt:280`
— and it is already in this repo's `CAPITAL_FIXES`), **`PLA` is Pal Lahara**
(`india.txt:652`, one location in Orissa), **`PRM` is Perm**
(`russia.txt:309`), **`GUJ` is the Gujarat formable**
(`00_formable_countries.txt:2959` — reusing it would consume the formable, the
`KAZ` lesson), **`MLW` and `SLK` are Malawi and Selkup**, and **`SOL` is
vanilla's *commented-out* Solon** (`east_asia.txt:2617`, `#SOL = { #Solon`) —
technically free but still carrying 26 live Russian custom-loc rows keyed to
it (`ru_EU5_custom_loc.txt`), so avoid.

```
COZ = { #Chola Empire (Thanjavur)
	color = map_COZ
	color2 = rgb { 16 41 202 }

	culture_definition = tamil
	religion_definition = hindu
}

CLK = { #Western Chalukyas of Kalyani
	color = map_CLK
	color2 = rgb { 16 41 202 }

	culture_definition = kannadiga
	religion_definition = hindu
}

PAA = { #Pala Empire (Bengal and Magadha)
	color = map_PAA
	color2 = rgb { 16 41 202 }

	culture_definition = bengali
	religion_definition = mahayana
}

PMR = { #Paramaras of Malwa (Dhar)
	color = map_PMR
	color2 = rgb { 16 41 202 }

	culture_definition = malvi
	religion_definition = hindu
}

CHU = { #Chaulukyas (Solankis) of Gujarat (Anahilavada)
	color = map_CHU
	color2 = rgb { 16 41 202 }

	culture_definition = gujarati
	religion_definition = hindu
}
```

**`culture_definition` is the landed tag's primary culture** — measured, and
recorded as this project's own law (`docs/HANDOFF.md:1377`). So each of the
five is chosen to MATCH the template pops, not to fight them. Measured over
each tag's resolved territory (§E.1):

| tag | template-pop culture profile of its resolved land | `culture_definition` | match |
|---|---|---|---|
| COZ | `tamil` 53/53 across cola/pandya/tondai/kongu/baramahal | `tamil` (`VAN/in_game/common/cultures/dravidian.txt:136`) | exact |
| CLK | `kannadiga` 64/64 across the Karnataka core | `kannadiga` (`dravidian.txt:76`) | exact |
| PAA | `bengali` 67, `bhojpuri_culture` 38, `magahi` 15, `maithili_culture` 12 | `bengali` (`indo_aryan.txt:180`) | plurality |
| PMR | `malvi` 17, `khandeshi` 7, `bhil` 5 | `malvi` (`indo_aryan.txt:733`) | plurality |
| CHU | `gujarati` 35/39 | `gujarati` (`indo_aryan.txt:677`) | near-exact |

**`religion_definition = mahayana` on PAA is the one deliberate mismatch.**
`mahayana` is a real religion (`VAN/in_game/common/religions/buddhist.txt:24`)
and the Palas are the last great Buddhist dynasty of India — Vikramashila and
Nalanda are theirs. But **every one of the 145 non-tribal locations in PAA's
resolved territory templates as `hindu`** (measured; the only non-hindu
templates in the whole Bengal block are 6 `sarna_religion`, 2 `koch_religion`,
1 `kirat_mundhum_religion`, 1 `gosain_religion`). This is precisely the
al-Andalus / Volga-Bulgar situation the user has now accepted twice
(`docs/HANDOFF.md:406-408`, Central Asia decision 6): the *identity* is
historical, the *pops* stay what they are until the pop phase. It is OPEN
DECISION 4, with `hindu` as the alternative.

**Five new colours** in `main_menu/common/named_colors/zz_1066_map_colors.txt`
(the file holds 63 `map_` rows today). Every key verified absent from vanilla
BY NAME (zero substring hits — the D3 lesson). Neighbour values read for
contrast: `map_delhi = rgb { 157 200 42 }`, `map_vijayanagar = { 246 196 24 }`,
`map_hoysala = { 237 13 29 }`, `map_orissa = { 210 106 47 }`,
`map_dambadeniya = { 21 97 40 }`, `map_pandya = { 168 131 200 }`,
`map_sindh = { 124 55 220 }`, `map_gwalior = { 153 237 145 }`,
`map_jejakabhukti = { 234 127 22 }`, `map_GAU = { 220 140 40 }`
(`VAN/main_menu/common/named_colors/02_map.txt:416-424, 486, 512, 569-571, 3230`).

```
	# India Tier 1. COZ must not read as map_pandya (violet) — TNK is
	# its immediate neighbour and both are Tamil; CLK must not read as
	# map_vijayanagar's gold, which it replaces on the same ground.
	map_COZ = rgb { 176 30 46 }     # Chola      tiger crimson
	map_CLK = rgb { 216 152 40 }    # Chalukya   Deccan ochre
	map_PAA = rgb { 190 108 30 }    # Pala       kasaya saffron-brown
	map_PMR = rgb { 92 132 60 }     # Paramara   Malwa green
	map_CHU = rgb { 60 128 176 }    # Solanki    Gujarat sea-blue
```
(Values are a suggestion; the constraints are (a) COZ vs `map_pandya`,
(b) CLK vs `map_hoysala` crimson AND `map_orissa` orange, (c) PAA vs
`map_GAU`'s orange which it replaces, (d) CHU vs `map_kutch` and
`map_junagarh` in Saurashtra.)

Add COZ/CLK/PAA/PMR/CHU to `verify_mod.py`'s `_GENERATOR_OK`
(`tools/verify_mod.py:924`) unless the CoA batch gives them bespoke arms.
**Tier 3, not tier 4:** unlike the taifas, Indian dynastic emblems ARE
attested — the Chola tiger, the Chalukya boar (Varaha), the Pala/Gauda
symbols, the Paramara eagle — so these deserve an eyeball in game before
investing, not a permanent generator waiver.

**Localisation** (`main_menu/localization/english/1066_norman_conquest_l_english.yml`,
one physical line each — the file holds 300 well-formed rows today):
```
 COZ: "Chola"
 COZ_ADJ: "Chola"
 CLK: "Chalukya"
 CLK_ADJ: "Chalukyan"
 PAA: "Pala"
 PAA_ADJ: "Pala"
 PMR: "Paramara"
 PMR_ADJ: "Paramara"
 CHU: "Solanki"
 CHU_ADJ: "Solanki"
```
Dynasty-name styling throughout, so the map reads Chola / Chalukya / Pala /
Paramara / Solanki as a set. Place-name alternatives, all attested as
locations or areas: "Cholamandalam", "Kalyani", "Gauda", "Malwa", "Gujarat".
See OPEN DECISION 6.

---

## B. NEW_COUNTRIES blocks

All five ride vanilla's own India templates, not the Muslim-monarchy family
the last three slices used. Read in full, and **diffed**:

- `indian_hindu_monarchy` (`VAN/main_menu/setup/templates/indian_hindu_monarchy.txt`)
  carries `starting_technology_level = 3`, `type = monarchy`,
  **`heir_selection = cognatic_primogeniture`**, thirteen societal sliders,
  `parliament = { parliament_type = council }`, eighteen estate privileges and
  seventeen laws. Unlike the `muslim_monarchy_*_no_coast` family, **the
  `_no_coast` Hindu variant KEEPS `heir_selection`** — diffed line by line:
  `_no_coast` differs only by dropping `sponsor_maritime_contracts`,
  `maritime_law` and `piracy_law` and adding `building_roads_rights`. So
  nothing has to be restated, and the Seljuk-family restate rule
  (`tools/build_setup.py:861-863`) does **not** apply here. This is the same
  measured asymmetry the France slice found for the catholic family
  (`tools/build_setup.py:1503-1510` comment).
- `indian_hindu_monarchy_jain` differs from the plain variant by exactly three
  lines: it `include = "expl_india_hindu"` **itself**, and adds
  `jain_banking_rights` + `jain_scholars`. So a tag on the jain variant needs
  no separate `expl_india_hindu`.
- `expl_india_hindu` (`VAN/main_menu/setup/templates/expl_india_hindu.txt`)
  grants `hindustan_region`, `bengal_region`, `central_india_region`,
  `western_india_region`, `deccan_region` (plus Persia, Arabia, Indochina,
  China, Tibet, the four Indian Ocean areas and more). **All five capitals
  resolve inside it** — the build's capital-discovery assert
  (`tools/build_setup.py:3310-3339`, `:4461-4472`) passes for every one:
  `thanjavur` → `cola_nadu` → `tamil_land_area` → `deccan_region`;
  `kalyani` → `kalyana_karnakassala` → `karnakassala_area` → `deccan_region`;
  `monghyr` → `bhagalpur_province` → `mithila_area` → `bengal_region`;
  `dhar` → `western_malwa` → `malwa_area` → `central_india_region`;
  `patan` → `sarasvata` → `gujarat_area` → `western_india_region`.

**Coastal or not — measured, not guessed** (a location is coastal iff its
`location_templates.txt` block carries `natural_harbor_suitability`):

| tag | harbour locations in its resolved land | variant |
|---|---|---|
| COZ | 15 (`nagapattinam karaikal pattukkottai trincomalee mahatittha jaffna` …) | coastal |
| CLK | 6 (`janjira chaul bombay bassein rajapur dabhol`) | coastal |
| PAA | 10 (`east_sundarban jaynagar kulpi chandpur barguna` …) | coastal |
| PMR | **0** | `_no_coast` |
| CHU | 8 (`daman surat rander broach khambat` …) | coastal |

```
	COZ = {
		starting_technology_level = 3
		include = "expl_india_hindu"
		include = "indian_hindu_monarchy"

		country_rank = rank_kingdom

		capital = thanjavur
	}

	CLK = {
		starting_technology_level = 3
		include = "expl_india_hindu"
		include = "indian_hindu_monarchy"

		country_rank = rank_kingdom

		capital = kalyani
	}

	PAA = {
		starting_technology_level = 3
		include = "expl_india_hindu"
		include = "indian_hindu_monarchy"

		country_rank = rank_kingdom

		capital = monghyr
	}

	PMR = {
		starting_technology_level = 3
		include = "expl_india_hindu"
		include = "indian_hindu_monarchy_no_coast"

		country_rank = rank_kingdom

		capital = dhar
	}

	CHU = {
		starting_technology_level = 3
		include = "indian_hindu_monarchy_jain"

		country_rank = rank_kingdom

		capital = patan
	}
```

Notes on the field set:
- `starting_technology_level = 3` is restated even though the template sets
  it, matching every vanilla India block and every block this repo has
  written.
- **CHU carries no `expl_india_hindu`** — `indian_hindu_monarchy_jain`
  includes it. Adding it again would be harmless but the build's block writer
  emits what it is given; keep it single.
- **`tolerated_cultures`.** Vanilla gives these to every big Indian tag
  (`HSL` → tamil/telugu/kodaga, `ORI` → telugu/bengali/sora_culture,
  `VIJ` → telugu/konkani). Ours, derived from the measured minority profile of
  each resolved territory:
  - COZ: `sinhalese` (18 of its 13 Ceylon locations' neighbours; its own take
    is `tamil` 7 + `sinhalese` 6 in Pihiti/Vanni), `telugu` (the Vengi block),
    `kannadiga`
  - CLK: `marathi_culture` (39 in Maharashtra), `telugu` (Telangana),
    `konkani`, `gond`
  - PAA: `bhojpuri_culture`, `magahi`, `maithili_culture`
  - PMR: `khandeshi`, `bhil`, `bundeli`
  - CHU: `bhil`, `mewari`
  Every one of these culture keys is verified in
  `VAN/in_game/common/cultures/{dravidian,indo_aryan}.txt` at the line numbers
  in §A's table plus `bhojpuri_culture:199`, `magahi:235`,
  `maithili_culture:253`, `khandeshi:714`, `bhil:639`, `bundeli:522`,
  `mewari:774`, `marathi_culture:446`, `konkani:426`, `sinhalese:465`,
  `telugu:212`, `gond:177`.
- **No `court_language`.** Each tag's own culture language is right
  (`tamil_language`, `kannada_language`, `bengali_language`,
  `malvi_language`, `gujarati_language`) and setting a court language would
  only risk the rank branch (§F). Sanskrit as a court language is tempting and
  is OPEN DECISION 7.

---

## C. Rulers

The naming route per ruler was chosen by **measuring the name pools**, not by
preference. Two facts drove almost every choice:

**`tamil_language` contains exactly ONE `name_*` key in the whole game —
`name_samuel`.** (`marathi_language` has one, `name_ranoji`;
`malayalam_language` two.) So no Tamil ruler can be named through a name key;
the literal route is mandatory for the Chola. Counts, from a parse of all 57
files in `VAN/in_game/common/languages/`: kannada 27, malvi 24, gujarati 27,
bengali 17, bihari 17, telugu 20, sinhala 3, hindustani 23, rajasthani 37,
oriya 13, kashmiri 35, sindhi 27, punjabi 32, **tamil 1**, **marathi 1**.

**Vanilla's `character_names_l_english.yml` already carries most of the
literals we need** — a first-name literal renders through that file with no
loc row of ours (the `Alp_Arslan` / `Ibrahim` class,
`tools/build_setup.py:3384-3390`):

| literal | vanilla row | needed by |
|---|---|---|
| `Someshvara` | `:2072` (also `Someshwara` `:2073`, `Somesvara` `:8194`) | CLK |
| `Vigrahapala` | `:2255` | PAA |
| `Karna` | `:29035` | CHU **and** RTP |
| `Kirtivarman` | `:1510` | JJK |
| `Vijayabahu` | `:8486` | DBD |
| `Udayaditya` | `:2213` | PMR alternative |
| `Chamundaraja` | `:1221` | DRW alternative |
| `Jayasimha` | `:1419` | PMR |
| `Bhoja` `:1186`, `Mahipala` `:1638`, `Nayapala` `:1753`, `Vikramaditya` `:2264`, `Rajaraja` `:7894`, `Solanki` `:2067` | — | banked for successions |
| **`Virarajendra`** | **ABSENT** | COZ — the only invented literal this package needs |

`Rajendra` and `Kulottunga` are also absent (only `Rajendralakshmi` `:1909`,
`Rajendranarayan` `:7901`, `Rajendravarman` `:18366`, `Rajadhiraja_Simha`
`:7889`), which matters for the Chola succession chain later.

| tag | character key | name route | accession | birth | regnal | dynasty | notes |
|---|---|---|---|---|---|---|---|
| **COZ** | `coz_virarajendra_chola` | **LITERAL `Virarajendra`** + one loc row ` Virarajendra: "Vīrarājendra"` (the proven invented-literal mechanism — `Shavur`/`Fariburz`/`Dubays` at `1066_norman_conquest_l_english.yml:170-172`) | 1063.1.1 [U] | 1010.1.1 [U] | **0** | `chola_dynasty` NEW | Vīrarājendra Chōḷa, third son of Rajendra I, r. 1063–1070 [U]. Preceded by Rajadhiraja I (d. 1054 at Koppam) and Rajendra II (1054–1063). Regnal 0 per the Cadalus rule — "Virarajendra" carries no ordinal in normal usage. `culture = tamil`, `religion = hindu`, `birth = thanjavur` |
| **CLK** | `clk_someshvara_i_ahavamalla` | **LITERAL `Someshvara`** — vanilla row `:2072`, no loc row of ours. The KEY route is a trap here: `name_someshwara` exists in malvi/gujarati/rajasthani but **not in `kannada_language`**, and CLK's culture is `kannadiga` → the `name_harald` failure (`docs/HANDOFF.md:120`) — a nameless king, no error | 1042.1.1 [U] | 1015.1.1 [U] | **1** | `chalukya_dynasty` NEW | Someśvara I Āhavamalla, r. 1042–1068; drowned himself in the Tungabhadra in 1068 — a two-year succession hook. `culture = kannadiga`, `religion = hindu`, `birth = kalyani` |
| **PAA** | `paa_vigrahapala_iii` | **LITERAL `Vigrahapala`** — vanilla row `:2255` | 1054.1.1 **[D]** | 1020.1.1 [U] | **3** | `pala_dynasty` NEW | Vigrahapāla III. **[D]: the Pala regnal dates are genuinely unstable** — 1043–1070, 1054–1072 and 1055–1070 all appear in standard tables. Every reading has him reigning in 1066; only the accession year moves. Successor Mahipala II (`Mahipala` literal is banked above). `culture = bengali`, `religion = mahayana` (or `hindu` — DECISION 4), `birth = monghyr` |
| **PMR** | `pmr_jayasimha_i_paramara` | **`name_jayasimha` — a VANILLA KEY in the RIGHT language.** Present in `malvi_language` (PMR's culture is `malvi`), and also kannada/gujarati/hindustani/telugu/rajasthani/oriya/kashmiri/punjabi. Loc rows `name_jayasimha: "Jayasinha"` and `name_jayasimha.sanskrit_language: "Jayasiṃha"` — `character_names_dynamic_l_english.yml:19853-19854` | 1055.1.1 **[D]** | 1025.1.1 [U] | **1** | `paramara_dynasty` **SHIPS** (`VAN/main_menu/setup/start/04_dynasties.txt:9169`) | **The hardest identification in the package. [D].** Bhoja died c. 1055. One standard reading: Jayasimha I 1055–1070, then Udayaditya 1070–1086/93. Another: Jayasimha I 1055–1060, then Udayaditya c. 1060–1087. A third denies Jayasimha existed. **Jayasimha is recommended because BOTH majority readings put him on the throne in 1055 and only one takes him off before 1066** — and, independently, because he is the only one of the five whose name is a vanilla key in his own language. `culture = malvi`, `religion = hindu`, `birth = dhar`. Alternative: `pmr_udayaditya_paramara`, LITERAL `Udayaditya` (`:2213`), accession 1060.1.1 [D], regnal 0 |
| **CHU** | `chu_karna_solanki` | **LITERAL `Karna`** — vanilla row `:29035`. (`name_karan` exists in rajasthani/kashmiri/sindhi/punjabi but **not `gujarati_language`** — the same trap as CLK) | 1064.1.1 [U] | 1035.1.1 [U] | **0** | `solanki_dynasty` NEW | Karṇadeva Chaulukya, son of Bhima I, r. 1064–1092 [U]. Founded Karnavati (modern Ahmedabad). Regnal 0 — "Karna I" is not standard usage. `culture = gujarati`, `religion = hindu`, `birth = patan` |

### C.2 The reseats that ride the same slice

| tag | ruler | route | source strength |
|---|---|---|---|
| **JJK** (Chandelas) | **Kirtivarman**, r. 1060–1100, regnal **1**, accession 1060.1.1 | LITERAL `Kirtivarman` (`:1510`); `chandela_dynasty` **SHIPS**, `home = kalinjar` (`04_dynasties.txt:9099-9102`) | **VANILLA ITSELF ATTESTS THIS RULER.** `VAN/main_menu/setup/start/10_countries.txt:7276` — inside JJK's own `government` block — reads `#Kirtti-Varman (Kīrtivarman)	1060–1100`. This is the strongest-sourced 1066 Indian ruler in the game, and it is Paradox's own text, not the agent's history. Note JJK's existing `regnal_numbers = { name_vira.name_varman = 2 }` block, which our literal does not touch |
| **RTP** (Kalachuris) | **Karna of Tripuri** (Lakshmi-Karna), r. 1041–1073 [U], regnal **0**, accession 1041.1.1 [U] | LITERAL `Karna` (`:29035`); `kalachuri_dynasty` **NEW** — grep for `kalachuri` over `dynasty_names_l_english.yml` and `04_dynasties.txt` returns **nothing** | [U]. Note: **two Karnas rule in 1066 India** — Chedi and Gujarat. That is historically true and worth a code comment so a later reviewer does not read it as a copy-paste |
| **DBD** (Ruhuna) | **Vijayabahu I**, king in Ruhuna from 1055, king of all Lanka 1073 [U], regnal **1**, accession 1055.1.1 [U] | **`name_vijayabahu` — a VANILLA KEY in `sinhala_language`** (one of only three sinhala keys), loc `character_names_dynamic_l_english.yml:20024`. The literal `Vijayabahu` also exists (`:8486`) | [U], but the identification is secure: Vijayabahu I is the only named Sinhalese ruler of the 1060s. Dynasty: **NEW** — grep over `dynasty_names_l_english.yml` for sinhal/lanka/polonnaru/ruhun/vijayabahu/parakrama returns nothing. Suggested `sinhala_dynasty`, loc "Sinhala" |
| **TNK** (Pandyas) | **`ruler = random`, deliberately** | — | [D]. The 1066 Pandyas are the "Five Pandyas", Chola feudatories with no agreed single king. The honest answer, per the TIB/BER/BLH precedent (`docs/HANDOFF.md:370-372`, `:492`) |
| **DRW** (Chahamanas of Shakambhari) | **`ruler = random`**, or **Chamundaraja** [D] | LITERAL `Chamundaraja` (`:1221`); `chauhan_dynasty` SHIPS (`04_dynasties.txt:8944`) | [D]. The Shakambhari list around 1066 runs Viryarama → Chamundaraja (c. 1060–1080) → Durlabharaja III, with dates that differ by a decade between authorities. Recommend random |
| **GWA** (Tomaras) | **`ruler = random`**, deliberately | `tomara_dynasty` SHIPS (`04_dynasties.txt:9134`) but a dynasty needs a character | [D]. The Tomara king-list of Delhi is bardic; Anangapala II's c. 1051–1081 is not a source, it is a tradition |

**Character-block shape** follows the taifa/Seljuk/China-East entries verbatim
(`tools/build_setup.py:2153-2161`, `:3260-3320`): `first_name`, `culture`,
`religion`, `birth_date`, `birth`, `dynasty`, `tag`. **No `death_date`** — the
alive law (`docs/HANDOFF.md:9-22`).

**Two banked cheap seats found while reading vanilla, not part of this
package but worth recording so nobody re-derives them:** vanilla's own
`10_countries.txt:6715` gives **CAB (Chamba) `#Raja SOMA VERMAN vers 1066`** —
a Paradox-attested 1066 ruler for a two-location tag this package does not
touch — and `:6876` gives **GLI (Gilgit) `#Nur Khan 1057-1127`**. Both are
zero-territory seats of the Yemen/Tunis class.

---

## D. Dynasties (`main_menu/setup/start/04_zz_1066_dynasties.txt`)

Vanilla ships **1,274** dynasty blocks and thirteen Indian houses:
`chandela_dynasty` `:278`, `chauhan_dynasty` `:282`, `guhila_dynasty` `:529`,
`hoysala_dynasty` `:589`, `kadamba_dynasty` `:646`, `kakatiya_dynasty` `:649`,
`pandya_dynasty` `:1007`, `paramara_dynasty` `:1010`, `purba_ganga_dynasty`
`:1071`, `sisodia_dynasty` `:1191`, `soomra_dynasty` `:1201`, `tomara_dynasty`
`:1288`, `yadava_dynasty` `:1618` (line numbers in
`VAN/main_menu/localization/english/dynasty_names_l_english.yml`; every one
also has a block in `04_dynasties.txt`).

**Four are missing and needed.** Word-boundary grep over BOTH
`dynasty_names_l_english.yml` and `04_dynasties.txt` for `chola_dynasty`,
`chalukya_dynasty`, `pala_dynasty`, `kalachuri_dynasty`, `solanki_dynasty`,
`chaulukya_dynasty`, `sinhala_dynasty` returns **zero hits for all seven**.
(`Chola` `:6536`, `Chalukya` `:6481`, `Pala` `:30719` and `Solanki` `:2067`
exist only as first-name pool rows in `character_names_l_english.yml` — a
different key in a different file, no collision.)

```
	# India Tier 1. Vanilla ships thirteen Indian houses and not one of
	# the five imperial dynasties of 1066: grep over 04_dynasties.txt AND
	# dynasty_names_l_english.yml returns zero for chola/chalukya/pala/
	# kalachuri/solanki. paramara_dynasty and chandela_dynasty DO ship and
	# are reused. All homes verified in definitions.txt.
	chola_dynasty = {
		name = { name = chola_dynasty }
		home = thanjavur
	}
	chalukya_dynasty = {
		name = { name = chalukya_dynasty }
		home = kalyani
	}
	pala_dynasty = {
		name = { name = pala_dynasty }
		home = monghyr
	}
	solanki_dynasty = {
		name = { name = solanki_dynasty }
		home = patan
	}
	kalachuri_dynasty = {
		name = { name = kalachuri_dynasty }
		home = ratnapura
	}
	sinhala_dynasty = {
		name = { name = sinhala_dynasty }
		home = tissamaharama
	}
```
loc rows:
```
 chola_dynasty: "Chola"
 chalukya_dynasty: "Chalukya"
 pala_dynasty: "Pala"
 solanki_dynasty: "Solanki"
 kalachuri_dynasty: "Kalachuri"
 sinhala_dynasty: "Sinhala"
```

**`paramara_dynasty` is REUSED, not redeclared.** It ships at
`04_dynasties.txt:9169` with `home = pal_lahara` — which is the *Orissa*
Paramara branch, not Malwa. The `home` field is cosmetic for our purposes and
this repo has already made exactly this call once, in writing: "The Granadan
Zirids REUSE `zirid_dynasty` above (same Banū Zīrī house via Zawi ibn Ziri;
the kairouan home is cosmetic)" (`04_zz_1066_dynasties.txt:63-66`). Declaring
`paramara_malwa_dynasty` instead is OPEN DECISION 8.

`chandela_dynasty` (home `kalinjar` — JJK's own capital) and `chauhan_dynasty`
and `tomara_dynasty` are likewise reused as-is.

Every `home` verified present and ownable in `definitions.txt`: `thanjavur`
(cola_nadu), `kalyani` (kalyana_karnakassala), `monghyr` (bhagalpur_province),
`patan` (sarasvata), `ratnapura` (dakshina_kosala), `tissamaharama` (ruhunu).

**Four capital-name identifiers the brief proposed do NOT exist and must not
be written:** `gangaikonda` (Gangaikonda Cholapuram has no location; the map's
stand-in is **`jayankondam`**, cola_nadu — the modern town on the site),
`gauda` (the map has **`gaur`**, gaur_province), `pataliputra` (the map has
**`patna`**, patna_province), `anahilavada` (the map has **`patan`**,
sarasvata — Patan *is* Anahilavada Patan). `tripuri` also does not exist,
which is why RTP keeps a Ratanpur seat (§E.4). All four absences confirmed
against the 5,226-name/20,922-location parse.

---

## E. Territory

### E.1 `_INDIA_RULES` — the definitions-resolved grants

Same 5-tuple shape as `_SELJUK_RULES`/`_CENTRALASIA_RULES`
(`tools/build_setup.py:855`, `:1163`):
`tag: (sweep names, singles, minus-sweeps, minus-singles, expected)`.
**Every count below came from an independent reimplementation of
`_resolve_ruleset` run against `definitions.txt` + `location_templates.txt`,
with the donor breakdown cross-checked against the built `10_countries.txt`.**

```python
_INDIA_RULES = {
    # ---- COZ, the Chola empire of Virarajendra. Cholamandalam,
    # Pandimandalam, Tondaimandalam, Kongu and the Baramahal; the
    # Vengi viceroyalty on the Godavari (Rajaraja Narendra's line held
    # it as a Chola client [D]); and the northern half of Lanka, which
    # the Cholas had ruled from Polonnaruva since 1017 [U].
    # TNK's four Pandya locations are protected by minus-singles:
    # tenkasi is TNK's capital and the Pandyas survive as feudatories.
    "COZ": (["cola_nadu", "pandya_nadu", "tondai_nadu", "kongu_nadu",
             "baramahal", "jaffna_province", "vanni", "pihiti",
             "kosta", "kamma_nadu", "vengi_nadu"],
            [], [], ["kayal", "tenkasi", "thoothukudi", "tirunelveli"],
            83),

    # ---- CLK, the Western Chalukya empire of Someshvara I: the whole
    # Deccan from the Tapti to the Tungabhadra. Kalyani, the Raichur
    # Doab, Banavasi, Telangana (the Kakatiyas are Chalukya
    # feudatories in 1066 [U]), Maharashtra (the Seunas), the northern
    # Konkan (the Shilaharas) and Vidarbha.
    "CLK": (["kalyana_karnakassala", "raichur_doab", "kampili",
             "chitradurga_province", "banavasi", "bangalore_province",
             "northern_rayalaseema", "southern_rayalaseema",
             "golconda_province", "warangal_province",
             "khammamet_province", "sirpur_province",
             "northern_desh", "southern_desh", "upper_marathwada",
             "lower_marathwada", "malnad", "baglana",
             "north_konkan", "malvana", "lower_vidarbha"],
            ["karwar", "bhadrachalam"], [], [], 180),

    # ---- PAA, the Pala empire of Vigrahapala III: Gauda, Varendra,
    # Vanga, Radha, Magadha and Anga. kanara/tulu are NOT swept, so
    # the Kadambas of Goa and the Alupas keep their coast; KMA
    # (Kamarupa) keeps its three jalpaiguri_province locations by
    # minus-single — Kamarupa is a real and separate 1066 kingdom.
    "PAA": (["gaur_province", "devkot_province", "bogra_province",
             "jalpaiguri_province", "pandua_province", "nadia_province",
             "khulna_province", "sonargaon_province",
             "mymensingh_province", "khalifatabad_province",
             "bhagalpur_province", "patna_province", "dumka_province",
             "hazaribagh_province"],
            [], [], ["birpara", "kamatapur", "koch_bihar"], 80),

    # ---- PMR, the Paramaras of Malwa: Avanti, Nimar, Khandesh.
    # bhojpur is Raja Bhoja's own foundation and hoshangabad its
    # Narmada neighbour — the two mahadeo locations DLH holds.
    "PMR": (["western_malwa", "eastern_malwa", "nimar", "khandesh"],
            ["hoshangabad", "bhojpur"], [], [], 38),

    # ---- CHU, the Chaulukyas of Anahilavada: Lata, the Khekassala
    # plain and the Sarasvata. Saurashtra stays with the Chudasamas
    # (JNG) and Kutch with KUT — both defensible at 1066.
    "CHU": (["lata", "khekassala", "sarasvata"], [], [], [], 16),

    # ================= the survivors that absorb Delhi ================
    # RTP, the Kalachuris of Chedi under Karna — the third great power
    # of the north in the 1050s-60s [D]. Dahala (akara), Kashi and the
    # Ganges-Yamuna doab below Delhi, Awadh and Rohilkhand. The six
    # arrah_province locations (UJJ/CER, the Ujjainiya and Chero) are
    # protected: both are real hill lineages, not 14th-century tags.
    "RTP": (["akara", "central_doab_province", "lower_doab_province",
             "awadh_area", "rokhilkhand_area", "bhojpur_area"],
            [], [], ["arrah", "ballia", "buxar", "jaund", "rohtas",
                     "sasaram"], 76),

    # GWA, reused as the TOMARAS of Dhillika (Delhi) — see DECISION 2.
    # Delhi, the upper doab, Puadh, Braj, Mewat, and Gwalior itself.
    "GWA": (["delhi_province", "upper_doab_province", "puadh_province",
             "braj_province", "mewat_province", "gird"],
            ["bayana"], [], [], 35),

    # JJK, the Chandelas of Jejakabhukti under Kirtivarman, restored to
    # Bundelkhand — the ground vanilla's own comment says they held.
    "JJK": (["upper_bundelkhand_province",
             "lower_bundelkhand_province"], [], [], [], 17),

    # SND, the Soomras of Sindh: the whole province, which is what
    # they held [U]. SMA (Samma, 1351) empties into them.
    "SND": (["upper_sindh_province", "northern_sindh_province",
             "sibi_province"], [], [], [], 25),

    # The Rajput and Baghelkhand edges of Delhi's demesne.
    "MEW": (["mewar"], [], [], [], 8),               # Guhilas
    "HAD": (["hadoti"], [], [], [], 6),              # Hadas of Bundi
    "MRW": ([], ["mandore", "osian", "kurki"], [], [], 3),
    "DRW": ([], ["sambhar", "ajmer", "ranthambore",
                 "merta", "nagaur", "makrana"], [], [], 6),  # Shakambhari
    "BGK": ([], ["sidhi", "agori", "vijaygarh"], [], [], 3), # Baghelkhand
}
```

**Donor breakdown — every recipient, verified against the built file:**

| recipient | takes | from | ends at |
|---|---|---|---|
| **COZ** | **83** | MAB 26, RDY 18, HSL 16, DBD 9, SMV 7, JFN 4, KPL 3 | 83 |
| **CLK** | **180** | DLH 71, VIJ 36, MSN 20, HSL 17, RCH 15, YDR 9, CHD 7, BGL 3, DRP 1, JWR 1 | 180 |
| **PAA** | **80** | DLH 25, STN 19, SGN 19, GAU 17 | 80 |
| **PMR** | **38** | DLH 37, CMN 1 | 38 |
| **CHU** | **16** | DLH 12, RJI 1, GHL 1, JLR 1, IDR 1 | 16 |
| **RTP** | **76** | DLH 75, GHR 1 | 18 → **94** |
| **GWA** | **35** | DLH 32, GWA 3 (no-op) | 3 → **35** |
| **JJK** | **17** | BND 10, BGK 3, JJK 2 (no-op), DLH 2 | 2 → **17** |
| **SND** | **25** | SMA 25 | 18 → **43** |
| **MEW** | **8** | MEW 5 (no-op), DLH 3 | 6 → **9** |
| **HAD** | **6** | HAD 3 (no-op), DLH 3 | 3 → **6** |
| **DRW** | **6** | DLH 6 | 2 → **8** |
| **MRW** | **3** | DLH 3 | 3 → **6** |
| **BGK** | **3** | DLH 3 | 10 → **13** |

Grants that overlap a recipient's own holdings are no-ops by construction —
the KRM/MZN/HLL precedent (`tools/build_setup.py:3472-3474`); 13 of the 576
are of that kind (MEW 5, GWA 3, HAD 3, JJK 2), so **563 locations actually
change owner**.

`expected` = the resolved sweep size, i.e. the tag's FINAL holdings inside
those names — the `_RUS_RULES` convention (`tools/build_setup.py:1233-1240`).

**Zero overlaps between the fourteen rule sets** (checked pairwise across all
576 tokens), so the build's disjointness assert passes.

### E.2 The Delhi behead — every one of the 272 accounted

| DLH holdings by area | count | goes to |
|---|---|---|
| `maharashtra_area` | 37 | CLK |
| `doab_area` | 35 | GWA 26 (delhi/upper_doab/puadh/braj/mewat), RTP 9 (central_doab/lower_doab) |
| `malwa_area` | 35 | PMR |
| `awadh_area` | 24 | RTP |
| `bhojpur_area` | 24 | RTP |
| `rajputana_area` | 21 | DRW 6, GWA 6 (gird 5 + bayana), MEW 3, HAD 3, MRW 3 |
| `mithila_area` | 19 | PAA |
| `karnakassala_area` | 15 | CLK |
| `gondwana_area` | 13 | RTP 6 (akara), BGK 3, PMR 2 (mahadeo), JJK 2 |
| `rokhilkhand_area` | 12 | RTP |
| `gujarat_area` | 12 | CHU |
| `konkan_area` | 9 | CLK |
| `vidarbha_area` | 9 | CLK |
| `jharkhand_area` | 6 | PAA |
| `telingana_area` | 1 | CLK |
| **TOTAL** | **272** | **CLK 71, RTP 75, PMR 37, GWA 32, PAA 25, CHU 12, DRW 6, BGK 3, MEW 3, HAD 3, MRW 3, JJK 2 = 272** |

**Resolver residue after the grants: DLH 272 → 0. Orphans: zero.** The same
check run over every retiring tag returns 0 residue for all eighteen. This is
the "every location accounted, no orphan" requirement, measured.

**No `LOCATION_VACATED` is used anywhere in this package.** That is deliberate
and is the reason the behead was deferred out of item 32 in the first place
(`tools/build_setup.py:1350-1353`): vacating settled land logs one
pop-religion line per pop, and the Gangetic plain and the Deccan are the
densest settled ground on the map. Every released location has a real
recipient.

### E.3 Landless after — nineteen tags

```python
INDIA_LANDLESS = ("DLH",
                  "VIJ", "MAB", "SMA", "RDY", "RCH", "JFN", "SMV", "MSN",
                  "YDR",
                  "GAU", "SGN", "STN",
                  "BND", "IDR", "RJI", "BGL", "DRP", "JWR")
```

Each keeps its registry identity and its pre-pass holdings become
`our_cores_conquered_by_others`, auto-derived — no authoring
(`tools/build_setup.py:4814-4817`, `:4960-4983`). Every one of the nineteen
had land, so every one passes the LANDLESS_AFTER non-empty-claims guard.

| tag | vanilla identity | what it is | why it cannot exist at 1066 |
|---|---|---|---|
| DLH | `india.txt:1` | Delhi Sultanate | founded 1206 [U]; the block is dated to the month (vanilla's own capital comment: "in 1337 the capital has been temporarily transferred to Sargadwari due to famine") |
| VIJ | `india.txt:25` | Vijayanagara | 1336 [U] |
| MAB | `india.txt:35` | Madurai Sultanate; `culture_definition = haryanvi_culture` — the Delhi-Turkish elite | 1335 [U] |
| SMA | `india.txt:362` | Samma of Sindh | 1351 [U] |
| RDY | `india.txt:49` | Reddi | 1325 [U] |
| RCH | `india.txt:197` | Recherla Nayakas | 1325 [U] |
| JFN | `india.txt:686` | Jaffna | 1215 [U] |
| SMV | `india.txt:18` | Sambuvarayar | 13th c. [U] |
| MSN | `india.txt:189` | Musunuri Nayakas | 1326 [U] |
| **YDR** | `india.txt:58`, `map_yadavaraya` | Yadavarayas of Chandragiri | 13th–14th c. [U]. **Not in the review's list; emptied by CLK's `southern_rayalaseema` sweep, so it must join or the build leaves a nine-location ghost** |
| **GAU** | `bengal.txt:9`, sunni | Gaur / Lakhnauti | Bengal Sultanate, 1338 [U] |
| **SGN** | `bengal.txt:1`, sunni | Sonargaon | Fakhruddin Mubarak Shah, 1338 [U] |
| **STN** | `bengal.txt:17`, sunni | Saptagram / Satgaon | same [U] |
| **BND** | `india.txt:545` | Bundelas of Orchha | 1501 [U]; they sit on the Chandela heartland |
| IDR | `india.txt:321` | Idar (Rathore) | 1257 [U] |
| RJI | `india.txt:344` | Rajpipla | 1340 [U] |
| BGL | `india.txt:239` | Baglana | 14th c. [U] |
| DRP | `india.txt:286` | Ramnagar / Dharampur | 1262 [U] |
| JWR | `india.txt:296` | Jawhar | 1343 [U] |

The last five (IDR RJI BGL DRP JWR, **7 locations between them**) are
collateral of the Gujarat and Maharashtra sweeps rather than targets. They are
the same class of error as the nine and retiring them is consistent, but they
could be protected with minus-singles at the cost of five one-location
anachronisms staying on the map. **OPEN DECISION 3.**

**None of the nineteen is `type = army` or `type = tribe`** (checked against
the `initialize_from_bookmark.cpp:2477` class — `docs/EU5-ERROR-DECODER.md`),
so no FIELD_FIXES fallback is expected.

### E.4 CAPITAL_FIXES — the repoints this package REQUIRES

The build refuses to strip any tag's capital without a repoint
(`tools/build_setup.py:5334-5369`), and the guard exempts landless tags
(`if held and capm.group(1) not in held` — `:5361`), which is why the
nineteen above need nothing. **Every one of the fourteen recipients and every
surviving donor was checked against every grant.** Three repoints are
required, and all three are historical improvements rather than mechanical
stand-ins:

```python
    # India Tier 1: three capitals stripped by the Tier-1 sweeps.
    "HSL": ("tiruvannamalai", "dvarasamudra"),
    "DBD": ("kurunegala", "tissamaharama"),
    "GHL": ("danduka", "sihor"),
```

- **HSL.** `tiruvannamalai` sits in `tondai_nadu`, which the Chola sweep
  takes; HSL keeps 14 locations, all `mysore_plateau`. `dvarasamudra` is
  vanilla's own `hoysala_dynasty` `home` (`04_dynasties.txt:8909-8912`) and
  the Hoysala capital in fact. Verified: `dvarasamudra` ∈ `mysore_plateau`,
  and it is one of HSL's surviving 14.
- **DBD.** `kurunegala` sits in `pihiti`, which the Chola sweep takes; DBD
  keeps 12 (`ruhunu` 6, `malaya` 3, `dakhina_desa` 3). `tissamaharama` is
  Mahagama/Magama, the historic seat of Ruhuna [U], and is one of the six DBD
  keeps.
- **GHL.** `danduka` sits in `khekassala`, which the Solanki sweep takes; GHL
  keeps exactly one location, `sihor` — which is the Gohil capital before
  Bhavnagar [U]. A forced repoint that happens to be right.

**No repoint is needed for** MEW (`chittor` is inside its own `mewar` grant),
HAD (`bundi` inside `hadoti`), JJK (`kalinjar` inside
`lower_bundelkhand_province`), GWA (`gwalior` inside `gird`), CHD
(`ballarpur` in `chanda_province`, untouched), KPL (`pithapuram` in
`kalingandhra`, untouched), JLR (`chandravati` in `godwar`, untouched), GHR
(`garha` in `garha_mandla`, untouched), CMN (`champaner` in `rewa_kantha`,
untouched), BGK (`bandogarh`, untouched), MRW (`khed`, untouched), DRW
(`taranagar`, untouched — but see the rename below), SND (`umarkot` in
`tharparkar_province`, untouched).

**Two OPTIONAL repoints that go with the renames** (§F.3): `DRW` →
`sambhar` (Shakambhari is literally the place the dynasty is named for, and
DRW takes it in this package) and `GWA` → `delhi`. Both are historical, not
forced; if the renames are rejected the capitals stay.

### E.5 What this slice moves, in one line

**576 locations touched** (563 change owner, 13 no-op), **5 new tags**,
**19 tags retired**, **9 existing tags enlarged**, **8 rulers seated**
(5 new + Kirtivarman + Karna of Tripuri + Vijayabahu I). DLH 272 → 0.
CLK 0 → 180 becomes the largest state in India. Comparable in size to the
Byzantium slice (495 granted, 45 landless) and larger than the Taifa Factory
(244 moved, 13 states).

---

## F. Government, rank, and the naming consequence — worked out

### F.1 The Indic rank branch, and why every tag here is `rank_kingdom`

Chased link by link:

- `VAN/in_game/common/customizable_localization/country_ranks.txt:1072-1092` —
  branch `rank_kingdom_indian`, trigger `country_rank_is_kingdom = yes` AND
  (`culture.language` OR `court_language`) has
  `language_family:indic_language_family` OR
  `language_family:dravidian_language_family` OR `language:malay_language`.
- Verified family membership for all five:
  `tamil_language` `family = dravidian_language_family`
  (`VAN/in_game/common/languages/00_deccan.txt:50-53`);
  `kannada_language` dravidian (`00_deccan.txt:167-170`);
  `bengali_language` indic (`:359-362`); `malvi_language` indic (`:671-674`);
  `gujarati_language` indic (`00_western_india.txt:178-181`).
- `VAN/main_menu/localization/english/government_names_l_english.yml:467-469`
  — `rank_kingdom_indian: "Mahārājya"`,
  `rank_kingdom_indian_ruler_male: "Mahārājā"`,
  `..._ruler_female: "Mahārānī"`.
- First-match: `rank_kingdom_muslim` sits at `country_ranks.txt:1060`, one
  branch ABOVE — irrelevant, none of ours is Muslim. Nothing between the top
  of the kingdom section and `:1072` matches a Hindu Indian monarchy.
- Name construction: a Hindu Indian monarchy matches **no** branch in
  `country_name_construction.txt` and falls to the `fallback = yes` branch
  `country_name_construction_prefix_rank_of_name` (`:184-187`), whose value is
  `"$PREFIX$ $RANK$ of $ARTICLE$ $NAME$"` and whose `_map` variant is bare
  `"$NAME$"` (`government_names_l_english.yml:11-12`).

**So the map will read `Chola`, `Chalukya`, `Pala`, `Paramara`, `Solanki`,
the tooltip `the Mahārājya of Chola`, and the ruler `Mahārājā
Virarajendra`.** The NAME key is live, the styling is Indic, and no
`country_ranks.txt` override is needed. **This is the first slice in the
project with no rank-styling debt** — unlike SEL and QRK/QRA, which are still
banked for the one Muslim-styling override (`docs/HANDOFF.md:1028-1039`).

### F.2 The empire-rank trap, stated so it is not walked into

`rank_empire` would be the natural instinct for the Chola. It costs two
things:

1. **The NAME key dies.** `country_name_construction.txt:117-121` — branch
   `country_name_construction_prefix_adjective_rank`, first condition
   `AND = { country_rank = country_rank:rank_empire  NOT = { tag = LAT } }`.
   Value `"$PREFIX$ $ADJ$ $RANK$"` — ADJECTIVE and RANK only. This is the JAL
   law (CLAUDE.md) in its non-horde form, and it is the exact reason SEL is
   `rank_kingdom` (`tools/build_setup.py:855` comment: "empire rank would kill
   the NAME key entirely (the prefix_adjective_rank branch, verified)").
2. **The Indic styling dies too.** There is **no `rank_empire_indian`
   branch** — grep `localization_key = rank_empire` over `country_ranks.txt`
   returns 44 branches (Mali, Inca, Aymara, Jurchen, Korean, Persian, four
   Muslim tag-gated ones, Tsar, dynasty, Ethiopia, Kanem, Vietnamese,
   Byzantine, Turkish, Nahua, Slovene, Serbo-Croatian, Bulgarian …) and not
   one of them is Indic. A Hindu empire falls to the plain `rank_empire` at
   `:625`, i.e. `rank_empire: "Empire"` / `rank_empire_ruler_male: "Emperor"`
   (`government_names_l_english.yml:54-56`).

So `rank_empire` renders **"the Chola Empire" ruled by "Emperor
Virarajendra"** — generic European styling, NAME key dead. `rank_kingdom`
renders **"the Mahārājya of Chola" ruled by "Mahārājā Virarajendra"**. The
second is both more correct and mechanically safer. **Recommendation:
`rank_kingdom` for all five.** OPEN DECISION 5 records the alternative for
the Chola alone, and the fix if it is wanted: a tag-gated `rank_empire_indian`
branch inserted ahead of `:625` in a whole-file `country_ranks.txt` override —
the same override SEL/QRK/QRA already need, so one file would serve all four
(first-match-wins rules out an additive file).

### F.3 The renames — what is needed and what is already right

The review's §3.4 lists three "cheap renames". **Measured against
`VAN/main_menu/localization/english/country_names_l_english.yml`, one of them
is a no-op and one is misdirected:**

| tag | current loc | verdict |
|---|---|---|
| **TNK** | `TNK: "Pandya"` `:457`, `TNK_ADJ: "Pandyan"` `:458`, and its registry colour is `map_pandya` | **ALREADY CORRECT. No rename needed** — only the (declined) seat and the shipped `pandya_dynasty` |
| **JJK** | `JJK: "Jejakabhukti"` `:815` | Jejakabhukti IS the Chandela realm's own name, and vanilla's block comment calls it "the Chandella dynasty". A rename to "Chandela" is a *choice*, not a fix. **Recommend leaving it** — the realm name is better map furniture than the house name, and it is what the tag id means |
| **RTP** | `RTP: "Ratnapura"` `:827` | **Genuinely wrong.** Ratnapura is Ratanpur, seat of the *southern* Kalachuri cadet branch; the tag now carries Karna of Tripuri and 94 locations from Chedi to Rohilkhand. **Override to `RTP: "Chedi"` / `RTP_ADJ: "Chedi"`** — the realm, not the house, matching JJK's convention |
| **DBD** | `DBD: "Dambadeniya"` `:449` | Wrong by 154 years. **Override to `DBD: "Ruhuna"` / `DBD_ADJ: "Ruhunu"`** (or "Lanka"/"Sinhala" — DECISION 9) |
| **DRW** | `DRW: "Dadrewa"` `:2980` | Dadrewa is a village; the tag now holds Sambhar and Ajmer. **Override to `DRW: "Shakambhari"` / `DRW_ADJ: "Chahamana"`** |
| **GWA** | `GWA: "Gwalior"` `:813` | Only if the Tomara reuse is taken (DECISION 2). Then **`GWA: "Tomara"`** — "Delhi" is DLH's key and two "Delhi"s on one map is worse than a house name |

A loc override of a vanilla `country_names` key is the proven route: this repo
already overrides `CAT: "Barcelona"` (`1066_norman_conquest_l_english.yml:138`)
and `rank_empire_theocracy_prefix: ""`. The harness's duplicate-key check
(`tools/verify_mod.py:174`) is per-file, so a mod row shadowing a vanilla row
in a different file passes — that is how CAT already works.

### F.4 Government shape

Every recipient of a grant must pass the build's **steppe-horde recipient
assert** (`tools/build_setup.py:3558-3573`, "steppe-horde recipients
forbidden"). Checked: all fourteen recipients are `type = monarchy` — the five
new ones through `indian_hindu_monarchy*`, and RTP (`india_limited_monarchy`),
GWA/JJK/BGK/MEW/HAD/MRW/DRW (`indian_hindu_monarchy*` variants), SND
(`indian_muslim_monarchy`). No horde, no tribe. **The assert passes
untouched.**

`heir_selection` — the Hindu templates all supply
`cognatic_primogeniture` and none of ours needs to restate it (§B).
`partition_inheritance` would arguably model the Chalukya and Paramara
appanage habit better; it is unmeasured in this project and the Central Asia
package's decision 7 parked it. Not proposed.

---

## G. Diplomacy, and the web

### G.1 The 22 `samanta` dependencies — audited one by one

`main_menu/setup/start/12_diplomacy.txt` carries **354 dependencies** in the
current build: vassal 182, tributary 79, tusi 64, **samanta 22**, fiefdom 4,
dominion 2, hanseatic_member 1.

The full samanta list, and its fate:

| line | tie | fate |
|---|---|---|
| DLH → GWA, HAD, MEW, JLR, IDR, CMN, SGN, GAU, STN | **9 ties** | **auto-stripped** — DLH enters LANDLESS_AFTER, and the generic landless sweep (`tools/build_setup.py:5996-6050`) eats every dependency naming a landless tag |
| GAU → TRF | 1 tie | **auto-stripped** — GAU is landless |
| ALU → STR, JSL → PRT, PDU → VDK, KSH → RJR, KSH → PNC, RTP → SRG, ORI → NRS, ORI → BAD, ORI → KJA, ORI → PTN, ORI → MJU, SRM → JBL | **12 ties** | **kept, and defensible at 1066.** Every one is a hill/coastal principality under a neighbour that this package leaves standing; none names a retiring tag. ORI's five (the Orissa garjats under the Eastern Gangas at Kataka) and RTP → SRG (Sarangarh under the Kalachuris) are actively *more* right at 1066 than at 1337 |

**So: 10 of the 22 die automatically, 12 survive, none needs a named strip.**
The exact-count constant must still move deliberately, because the strip
asserts its own number.

**No new `samanta` tie is proposed**, and the reason is a measured risk:
`VAN/in_game/common/subject_types/samanta.txt:7` gates `visible` on
`has_advance = samanta_advance`, and `samanta_advance`
(`VAN/in_game/common/advances/culture_indian.txt:25-31`) is
`age = age_1_traditions` with `requires = feudalism_advance` and
`potential = { culture = { has_culture_group = culture_group:indian_group } }`.
Whether a `starting_technology_level = 3` tag has that advance at init is
**not statically determinable** — and the Seljuk slice measured exactly this
class failing: a tributary whose visible gate fails is silently **downgraded
to vassal** at game start (`government.cpp:3702`,
`tools/build_setup.py:825-840`). Vanilla's own 22 samantas suggest it passes,
but "vanilla ships it" was precisely the reasoning that was wrong about
tributaries. The historically obvious tie — **CLK → HSL** (the Hoysalas were
Chalukya feudatories in 1066 [U]) — is therefore **flagged, not written**:
OPEN DECISION 10.

### G.2 The four `hindu_branch` IO member lists — exact moves

All four survive the future-instance strip (`creation_date = 1.1.1`). Landless
members are auto-stripped by the generic sweep
(`tools/build_setup.py:5595-5635`), so no member surgery is needed — but the
`_expected_ghosts` list and the `n_ghosts != 131` constant must both move, and
the expected member counts are:

| instance | line | law | members now | after | loses |
|---|---|---|---|---|---|
| `hindu_branch` | `:1173` | `vaishnavism` | 61 | **55** | VIJ YDR BGL DRP JWR BND |
| `hindu_branch` | `:1191` | `shaivism` | 55 | **49** | JFN SMV RDY MSN RCH RJI |
| `hindu_branch` | `:1209` | `shaktism` | 16 | **15** | IDR |
| `hindu_branch` | `:1224` | `smartism` | 6 | **6** | — |
| **total ghosts** | | | | | **13** |

DLH, MAB, SMA, GAU, SGN and STN are Muslim tags and sit in **no** IO list
(verified: a scan of the whole 15_international_organizations.txt for all
nineteen retiring tags returns exactly 13 tokens, and those six contribute
none).

**DBD contributes no ghost either — and that is a second reason to keep it.**
DBD's single IO membership is the **Mahāvihāra** sect
(`15_international_organizations.txt:1090-1095`, `icon = mahavihara`,
`law = mahavihara_policy`, members `DBD PEG ARK TSM`). The Mahavihara of
Anuradhapura is the 1066 Sinhalese Buddhist establishment; retiring DBD would
have stripped exactly the tag that belongs there.

**Should the five new tags JOIN a hindu_branch?** Nothing forces it — the
harness only checks that members hold land, not that landholders are members
(`tools/verify_mod.py:837`). But four of the five are Shaiva by conviction and
the branch lists are how the game expresses that:

| tag | branch | historical basis |
|---|---|---|
| COZ | `shaivism` (`:1191`) | the Cholas are the Shaiva dynasty par excellence — Rajaraja's Brihadisvara, the Tevaram canon |
| CLK | `shaivism` | Kalyani's Shaiva establishment; also heavy Jain patronage |
| PMR | `shaivism` | Bhoja's Bhojeshwar; the Paramaras are Shaiva |
| CHU | `shaivism` | Somnath is theirs; Jain patronage alongside (hence the `_jain` template) |
| PAA | **none, or `mulasarvastivada`** | the Palas are Buddhist. The `mulasarvastivada` sect instance (`:1014`, `variables.religion = religion:mahayana`) is the Mahayana Vinaya school and is doctrinally right — but its 10 members are all Indonesian (JMB BUS INR SGT PLB…) and it carries `provinces = { johor_province lower_jambi_province }`. Adding PAA is mechanically fine and geographically odd. **Recommend: leave PAA out of any sect this pass** |

Adding COZ/CLK/PMR/CHU to the `shaivism` list moves it 49 → 53 and the "IO
members hold land" count 870 → 861 (−13 ghosts +4). OPEN DECISION 11.

### G.3 Everything else in the web

- **No pacts.** A scan of `12_diplomacy.txt` for alliances/guarantees naming
  any of the nineteen returns **zero**. The `n_pacts != 7` constant does not
  move.
- **No tributary or tusi tie** names an Indian tag in this package's scope.
- **No new dependency is proposed at all.** The Chola's overlordship of the
  Pandyas, the Chalukya's of the Hoysalas and the Kakatiyas, and the Chola
  occupation of Lanka are all expressed as *territory* here, not as subject
  ties — which is the safer modelling given G.1's gate risk and the project's
  standing rule that a player's ties are not created without consent.

---

## H. Left alone deliberately

| what | why |
|---|---|
| **GHZ's 131, including the Punjab's 97** | Item 32's own grant, correct and landed. The Ghaznavid–Indian frontier is the one part of 1066 India already right. Nothing here touches a GHZ location |
| **Kerala — 13 tags over `malabar_area`'s 25** (ZMR KLT PDU VND KTN KDU KYA VLD ELA TKU VDK STR ALU) | At 1066 this is ONE state: the Chera Perumals of Mahodayapuram under Rama Kulasekhara, dissolving c. 1102 [U]. Unifying it is a real slice of its own (a new tag, a new dynasty, 13 retirements) and it is the **single largest remaining India error after this package**. Explicitly banked, not forgotten |
| **ORI (21) and the eleven Orissa garjats** | ORI is the Eastern Gangas at Kataka. In 1066 the Gangas held Kalinga and the Somavamshis held Utkala [D] — a real error, but a *small* one, and ORI's five samanta ties are defensible. A later Orissa pass |
| **KMA (14), AHO (8), CUT, DIM, JNT, LUR, TWI, TRF** | Kamarupa and the Brahmaputra polities. Kamarupa under the Pala kings of Kamarupa is genuinely separate from Bengal in 1066 [U]; KMA is protected by minus-singles in PAA's ruleset for exactly that reason. AHO (Ahom, 1228 [U]) is an anachronism the Assam review should take |
| **The Himalayan belt — KHS LWA KMN GWL KTU DTI SRM JBL, 61 locations in `nepal_area`** | Khasa, Limbuwan, Kumaon, Garhwal, Kathmandu. Fragmented in 1066 and fragmented at 1337; the tags are roughly right. Nepal is its own review |
| **`upper_indus_area`'s 46 — SWT GLI KSH CTR HNZ CRL RJR PNC NAG QUN** | Kashmir under the first Lohara dynasty and the Dard/Kohistani principalities. Vanilla's fragmentation is not far wrong. **QUN's three (`asadabad_kunar hajiabad parun`) are still the Afghan/upper-Indus review's**, as the Central Asia package flagged (`docs/CENTRAL-ASIA-PACKAGE.md` §H) — this package does not close QUN either |
| **`maldives_area` (DGL 4 + 1 unowned)** | Islam arrives in the Maldives in 1153 [U]; `religion_definition = sunni` on DGL is early. One tag, four atolls — a footnote |
| **GOA (2), HNV (1), ALU (5), STR (1)** | The Kadambas of Goa (Jayakeshi I, r. c. 1050–1080 [U]) and the Alupas of Tulu Nadu are *real* 1066 lineages and `kadamba_dynasty` ships. `kanara` and `tulu_nadu` are deliberately absent from CLK's sweep so all four keep their coast. Cheap seats for a later pass |
| **CHD (4), GHR (8), BST, KNK, BGR, WRG, KHR, JPO, SRG, PTN, BAD, KJA and the Gond/Orissa hill tags** | The Gondwana and Orissa uplands. Their vanilla identities are late, but they hold ground no 1066 empire administered, and turning them into empty land would cost the settled-pop log flood for no gain. **The Pecheneg discipline in its positive form: no location-level evidence of a different owner, so no change** |
| **UJJ (5) and CER (4)** | The Ujjainiya and Chero of the Son valley — protected by minus-singles in RTP's ruleset. Both are hill lineages with long histories and neither is a 14th-century invention |
| **Pops, cultures and religions everywhere in this theater** | Separate phase by user decision (`docs/HANDOFF.md:1047-1050`). Two notes for it: `bidar`/`kalyani`/`gulbarga` template as `kannadiga`+`hindu`, which is right; and **PAA's whole 80 templates as `hindu`** against a `mahayana` state religion (§A) — the single largest pop/identity gap this package creates |

---

## OPEN DECISIONS

**1. Take the whole package, or the five tags without the Delhi behead?**
The five new tags can technically land on the nine retirements' 172 locations
alone, leaving DLH at 272. **Recommendation: take it whole.** The five great
powers would then have to be drawn AROUND a Delhi Sultanate that holds Malwa,
Gujarat, Maharashtra and the Deccan — i.e. the Paramaras would have no Malwa
and the Chalukyas no Maharashtra, which is worse than not shipping them. The
behead is what makes the five possible, and the behead needs the five as
recipients. They are one object.

---

**2. GWA reused as the Tomaras of Delhi, or the Doab given to RTP?**
DLH's 26 doab locations (Delhi, the upper Doab, Puadh, Braj, Mewat) need a
home. Three options:
- **(a) Reuse GWA (RECOMMENDED).** GWA is vanilla's Tomaras of Gwalior; the
  Tomaras of Delhi are the same house and `tomara_dynasty` ships. Loc override
  to "Tomara", capital → `delhi`, 3 → 35 locations. Cost: one loc override,
  one optional capital repoint, zero new tags. Puts a recognisable Delhi on
  the 1066 map that is not a Sultanate.
- **(b) Give them to RTP** with the rest of the Ganges. RTP 94 → 120. Cost:
  zero. Makes the Kalachuris implausibly large and leaves Delhi as a Kalachuri
  provincial town.
- **(c) A new TMR tag.** Cost: a sixth registry block, colour, loc. Cleanest
  identity, most scope.
The Tomara king-list is bardic either way, so all three ship `ruler = random`.

---

**3. The five collateral retirements — IDR, RJI, BGL, DRP, JWR (7 locations).**
They are emptied by the Gujarat and Maharashtra sweeps rather than targeted.
All five are 13th–14th-century foundations [U], the same class as the nine.
- **Recommendation: retire them.** Consistency, and 7 locations is not worth
  five sets of minus-singles.
- **Against:** it takes the nineteen-tag retirement list past what the review
  proposed, and BGL/DRP/JWR are Bhil/Koli hill chiefdoms whose *people* were
  certainly there in 1066 even if the dynasties were not. Protecting them
  costs five minus-singles and leaves five one-location anachronisms.

---

**4. PAA's `religion_definition`: `mahayana` or `hindu`?**
`mahayana` is historically right — the Palas are the last Buddhist imperial
dynasty of India and Vikramashila is founded by them. But **all 145 non-tribal
locations in PAA's territory template as `hindu`** (measured), so a Buddhist
Pala starts as a religious minority in its own realm.
- **Recommendation: `mahayana`.** It is the al-Andalus decision the user has
  already made twice (`docs/HANDOFF.md:406-408`; Central Asia decision 6), it
  puts the only Buddhist great power in India on the map, and it is the single
  most distinctive thing about 1066 in this theater. The pop phase closes the
  gap.
- **Against:** unlike `bolghar_culture` on 28 locations, this is 80 locations
  and a *religion*, which drives unity, tolerance and stability — a harder
  start than the Bulgars'. If a playable Pala matters more than a historical
  one, ship `hindu`.

---

**5. The Chola at `rank_kingdom` or `rank_empire`?**
`rank_kingdom` → "the Mahārājya of Chola" / "Mahārājā", NAME key live, Indic
styling, no override needed. `rank_empire` → "the Chola Empire" / "Emperor",
**NAME key dead** (only `COZ_ADJ` is ever read), generic styling, because
there is no `rank_empire_indian` branch (§F.2).
- **Recommendation: `rank_kingdom` for all five.** "Mahārājya"/"Mahārājā" is
  better flavour than "Empire"/"Emperor" and costs nothing.
- **If empire rank is wanted for the Chola:** it needs a tag-gated
  `rank_empire_indian` branch inserted ahead of `country_ranks.txt:625` in a
  whole-file override — which is the same override SEL/QRK/QRA are already
  banked for, so **one file would serve all four**. Fold it into that pass.

---

**6. Tag names: dynasty or place?**
Recommended: Chola / Chalukya / Pala / Paramara / Solanki — a legible set,
matching vanilla's own `HSL: "Hoysala"` and `RDY: "Reddi"`.
Place-name alternatives, all attested: Cholamandalam, Kalyani, Gauda, Malwa,
Gujarat. Mixed sets read badly; pick one convention.
- **Recommendation: dynasty names.**

---

**7. A `court_language` for any of the five?**
Not proposed. Sanskrit as the court language of the Chola or Chalukya court is
defensible [U] — but `court_language` is one of the two inputs to the
`rank_kingdom_indian` trigger, and `culture.language` already satisfies it, so
setting it buys nothing and risks the branch if a Sanskrit language key turns
out to sit in a different family. **Recommendation: none.** (`sanskrit_language`
does exist — `character_names_dynamic_l_english.yml` carries
`name_jayasimha.sanskrit_language` — but its family was not verified and this
package does not need it.)

---

**8. `paramara_dynasty` reused, or `paramara_malwa_dynasty` declared?**
Vanilla's `paramara_dynasty` (`04_dynasties.txt:9169`) has `home = pal_lahara`
— the Orissa branch, one location.
- **Recommendation: reuse it.** `home` is cosmetic and this repo has already
  made and documented the identical call for `zirid_dynasty`
  (`04_zz_1066_dynasties.txt:63-66`). Reusing also means the Malwa Paramaras
  and the Pal Lahara Paramaras read as one family, which they were.
- **Against:** a later Orissa slice may want them distinguished. Declaring
  `paramara_malwa_dynasty` with `home = dhar` costs three lines and one loc
  row.

---

**9. DBD's new name: "Ruhuna", "Lanka" or "Sinhala"?**
The tag holds Ruhuna, Malaya and Dakhina Desa — the southern two-thirds of the
island — while the Chola holds Rajarata. In 1066 Vijayabahu I styles himself
king of Lanka in exile.
- **Recommendation: "Ruhuna" / "Ruhunu".** It is what the state *is* in
  1066 and it makes the Chola occupation legible on the map. "Lanka" invites
  the question of who holds Anuradhapura; "Sinhala" duplicates the dynasty
  name.
- Related: **is the Chola/Ruhuna line right?** [D] — the Chola held Rajarata
  from Polonnaruva 1017–1070 and Vijayabahu drove them out in 1070, so 1066
  is four years before the reconquest. The 13/12 split proposed (Chola takes
  `jaffna_province` + `vanni` + `pihiti`; DBD keeps `ruhunu` + `malaya` +
  `dakhina_desa`) is the standard reading. An alternative gives the Chola
  `dakhina_desa` too (the western coast), 16/9.

---

**10. `CLK → HSL` as a `samanta` tie?**
The Hoysalas were Chalukya feudatories in 1066 [U] and the tie would be the
single most historically pointed relationship in the Deccan. But
`samanta.txt:7` gates it on `has_advance = samanta_advance` on the overlord,
and whether a `starting_technology_level = 3` tag holds that advance at init
is not statically determinable — the exact class the Seljuk slice measured
failing and silently downgrading to vassal (`government.cpp:3702`).
- **Recommendation: do not write it this pass.** Ship HSL independent at 14
  locations; measure whether vanilla's own 12 surviving samantas survive in
  the next error.log; add the tie in a follow-up if they do. If it is wanted
  now, the safe form is `subject_type = vassal`, which has no advance gate.

---

**11. Do the five new tags join a `hindu_branch` IO?**
Nothing forces it. Adding COZ/CLK/PMR/CHU to the `shaivism` list
(`15_international_organizations.txt:1191`) is four tokens and moves that list
49 → 53.
- **Recommendation: yes, add the four Hindu tags to `shaivism`; leave PAA out
  of every sect.** A 180-location Chalukya standing outside every religious
  IO on a map where 55 one-location Rajput states are inside one reads as an
  oversight. PAA's only doctrinally-correct home
  (`mulasarvastivada`) is an Indonesian instance with Malay provinces
  attached, which is worse than nothing.

---

**12. RTP at 94 locations — is the Kalachuri empire too generous?**
The package gives Karna of Tripuri Dahala, Kashi, the lower Doab, Awadh and
Rohilkhand: 18 → 94, the second-largest state in India. Karna's empire at its
height (1050s–60s) did reach Kanauj, Anga and the Ganges [D], but it collapsed
after 1073 and some authorities keep it much smaller.
- **Recommendation: ship it at 94.** The alternative is a fourth invented tag
  (a Gahadavala at Kanauj, which is a 1089 foundation and therefore itself
  anachronistic) or leaving Awadh/Rohilkhand with a landless Delhi, which is
  not an option.
- **Against:** if it plays badly, the cheap correction is to move
  `awadh_area` (24) and `rokhilkhand_area` (12) out of RTP's ruleset — but
  they then need a recipient, which is decision 2 again.

---

## Implementation checklist

1. **Registry** — five blocks in `in_game/setup/countries/zz_1066_new_countries.txt`
   (the file holds 51 blocks today). Five rows in
   `main_menu/common/named_colors/zz_1066_map_colors.txt` (63 `map_` rows
   today). Ten loc rows + four/six dynasty loc rows + one invented literal row
   (`Virarajendra`) in `1066_norman_conquest_l_english.yml` (300 rows today).
   Five entries in `verify_mod.py`'s `_GENERATOR_OK` (tier 3).
2. **Dynasties** — six new blocks in `04_zz_1066_dynasties.txt`
   (`chola_`, `chalukya_`, `pala_`, `solanki_`, `kalachuri_`, `sinhala_`);
   `paramara_dynasty`, `chandela_dynasty`, `chauhan_dynasty`,
   `tomara_dynasty` reused.
3. **NEW_COUNTRIES** — five blocks in `tools/build_setup.py`, and the
   `_INDIA_TAGS` loop if a `_seljuk_block`-style helper is wanted (the five
   differ only in capital, template variant and tolerated cultures, so a table
   is worth it).
4. **`_INDIA_RULES`** — fourteen rule sets, `expected` asserted per tag.
   Feed into `LOCATION_GRANTS` the same way `_CENTRALASIA_RULES` does.
5. **Capital asserts** — add the `_SELJUK_TAGS`/`_CENTRALASIA_TAGS` pattern
   (`tools/build_setup.py:4623`, `:4655`) for the five: `thanjavur ∈ COZ`,
   `kalyani ∈ CLK`, `monghyr ∈ PAA`, `dhar ∈ PMR`, `patan ∈ CHU`. All five
   hold in the resolved lists.
6. **`CAPITAL_FIXES`** — three required: HSL, DBD, GHL (§E.4). Two optional
   with the renames: DRW, GWA.
7. **`LANDLESS_AFTER`** — nineteen additions.
8. **`HISTORICAL_RULERS` + `NEW_CHARACTERS`** — eight seats: COZ CLK PAA PMR
   CHU JJK RTP DBD. TNK, DRW, GWA stay `ruler = random` deliberately.
9. **Loc overrides** — RTP, DBD, DRW (+ GWA if decision 2a). TNK and JJK need
   none.
10. **Harness** — raise every constant below, each **observed failing first**
    (CLAUDE.md: "prove every new check against a known positive").

### Expected constant moves — every one measured

| constant | where | now | after | why |
|---|---|---|---|---|
| landless IO list entries stripped | `build_setup.py:5633` | **131** | **144** | +13 hindu_branch ghosts: VIJ YDR BGL DRP JWR BND (vaishnavism) + JFN SMV RDY MSN RCH RJI (shaivism) + IDR (shaktism). All thirteen must also be added to `_expected_ghosts` (`build_setup.py:5610-5632`), which asserts the exact multiset, not just the count |
| landless-tag dependencies stripped | `build_setup.py:6048` | **238** | **248** | DLH's 9 samanta + GAU → TRF (§G.1) |
| landless-tag pacts stripped | `build_setup.py:6071` | **7** | **7** | unchanged — zero pacts name any of the nineteen |
| future-dated IO removals | `build_setup.py:5386` | 17 | 17 | untouched |
| `IO members hold land` | `verify_mod.py:837` | **870** | **857** (or **861** with decision 11) | −13 ghosts (+4 if COZ/CLK/PMR/CHU join `shaivism`) |
| `exactly one ruler key per country block` | `verify_mod.py:859` | **2388** | **2393** | +5 new blocks |
| `identity <-> start-block bijection` | `verify_mod.py:1012` | **2391** | **2396** | +5 |
| `mod named colours shadow no vanilla key` | `verify_mod.py:1039` | **48** | **53** | +5 |
| `coat of arms references resolve` | `verify_mod.py:979` | **102** | **107** | +5 `_GENERATOR_OK` |
| `landed countries reach a parliament_type` | `verify_mod.py:1131` | **1398** | **1384** | −19 retired +5 new. **This one is currently EXACT (min_count == actual), so it will fail loudly the first run — which is the point** |
| `named rulers carry an open, past-dated ruler_term` | `verify_mod.py:288` | **330** | **338** | +8 seats |
| `authored character keys collide with nothing` | `verify_mod.py:422` | **126** | **134** | +8 |
| `authored identifiers resolve` | `verify_mod.py:376` | **583** | ~**630** | ~6 identifiers per authored character |
| `no death_date on a character alive at start` | `verify_mod.py:458` | **4045** | **4053** | +8 |
| `regions/areas/locations exist` | `verify_mod.py:636` | 11 | ≥ 11 | the fourteen rule sets add many names; raise to the new actual |

### A new harness check this slice earns

**"every India Tier-1 recipient's capital is one of its own holdings"** is
already covered by the generic orphan-capital validator
(`build_setup.py:5340-5369`). What is NOT covered, and what this package's
research surfaced, is:

> **A country's `first_name = { name = name_X }` must resolve in the language
> its OWN culture speaks.** The harness checks that authored identifiers
> resolve (`verify_mod.py:376`) but — per the `name_harald` trap
> (`docs/HANDOFF.md:120`) — a key that exists in *some* language and not in
> the character's own gives a nameless character with no error. Two of the
> five rulers in this package would have hit it (`name_someshwara` is absent
> from `kannada_language`; `name_karan` from `gujarati_language`), and it was
> caught only by parsing all 57 language files per-block. **That check is
> worth writing, and `name_someshwara` on a `kannadiga` character is its
> known positive.**

---

## Verification statements

Per CLAUDE.md's say-what-you-verified rule:

- Verified — the ownership parser reproduces the project's own stated state:
  **DLH 272, GHZ 131**, from `main_menu/setup/start/10_countries.txt` using
  `OWN_KEYS` (`tools/build_setup.py:4543-4547`) and `COUNTRY_RE` (`:4401`).
- Verified — `_resolve_ruleset` reimplementation reproduces the shipped
  Central Asia counts QRK 46 / QRA 142 / BLH 28
  (`tools/build_setup.py:1163-1200`).
- Verified — **tag freeness for COZ CLK PAA PMR CHU in both scan modes**:
  `\bTAG\b` and `_TAG\b|\bTAG_|_TAG_` over 16,290 vanilla text files and the
  mod repo, zero hits each; and absent from a 2,481-entry registry built from
  every identity block, every start block and every formable `tag =`.
- Verified — `rank_kingdom_indian`,
  `VAN/in_game/common/customizable_localization/country_ranks.txt:1072-1092`,
  trigger on `indic_language_family` OR `dravidian_language_family`; value
  `government_names_l_english.yml:467`, `rank_kingdom_indian: "Mahārājya"`.
- Verified — the empire-rank NAME-key kill,
  `country_name_construction.txt:117-121`
  (`country_name_construction_prefix_adjective_rank`, first condition
  `country_rank = rank_empire NOT tag = LAT`), value
  `government_names_l_english.yml:9`, `"$PREFIX$ $ADJ$ $RANK$"`; and the
  absence of any `rank_empire_indian` branch among the 44
  `localization_key = rank_empire*` branches in `country_ranks.txt`.
- Verified — the fallback name branch
  `country_name_construction_prefix_rank_of_name`,
  `country_name_construction.txt:184-187`, `fallback = yes`; value
  `government_names_l_english.yml:11-12`,
  `"$PREFIX$ $RANK$ of $ARTICLE$ $NAME$"` / map `"$NAME$"`.
- Verified — `indian_hindu_monarchy` carries `heir_selection =
  cognatic_primogeniture` and `parliament_type = council`, and its `_no_coast`
  variant KEEPS `heir_selection` (line-by-line diff of all four variants in
  `VAN/main_menu/setup/templates/`).
- Verified — `expl_india_hindu` grants all five South Asian regions
  (`VAN/main_menu/setup/templates/expl_india_hindu.txt:1-21`), so all five
  proposed capitals pass the capital-discovery assert.
- Verified — `paramara_dynasty` `VAN/main_menu/setup/start/04_dynasties.txt:9169`
  (`home = pal_lahara`), `chandela_dynasty` `:9099` (`home = kalinjar`),
  `hoysala_dynasty` `:8909` (`home = dvarasamudra`), `pandya_dynasty` `:8924`,
  `chauhan_dynasty` `:8944`, `tomara_dynasty` `:9134` — all present.
- Verified — **zero hits** for `chola_dynasty`, `chalukya_dynasty`,
  `pala_dynasty`, `kalachuri_dynasty`, `solanki_dynasty`,
  `chaulukya_dynasty`, `sinhala_dynasty` in either
  `dynasty_names_l_english.yml` or `04_dynasties.txt`.
- Verified — the literal rows `Someshvara` `:2072`, `Vigrahapala` `:2255`,
  `Karna` `:29035`, `Kirtivarman` `:1510`, `Vijayabahu` `:8486`,
  `Udayaditya` `:2213`, `Jayasimha` `:1419`, `Chamundaraja` `:1221` in
  `VAN/main_menu/localization/english/character_names_l_english.yml`; and
  the **absence** of `Virarajendra`, `Rajendra` and `Kulottunga` from the
  same file.
- Verified — `name_jayasimha` present in `malvi_language`;
  `name_someshwara` **absent** from `kannada_language`; `name_karan`
  **absent** from `gujarati_language`; `name_vijayabahu` present in
  `sinhala_language`; `tamil_language` contains exactly one `name_*` key
  (`name_samuel`) — all from a per-block parse of all 57 files in
  `VAN/in_game/common/languages/`.
- Verified — vanilla's own attestation of the Chandela ruler,
  `VAN/main_menu/setup/start/10_countries.txt:7276`, inside JJK's
  `government` block: `#Kirtti-Varman (Kīrtivarman)	1060–1100`.
- Verified — `samanta`'s visible gate,
  `VAN/in_game/common/subject_types/samanta.txt:7`,
  `has_advance = samanta_advance`, and the advance itself,
  `VAN/in_game/common/advances/culture_indian.txt:25-31`,
  `age = age_1_traditions requires = feudalism_advance`.
- Verified — the four `hindu_branch` instances at
  `main_menu/setup/start/15_international_organizations.txt:1173/1191/1209/1224`
  with 61/55/16/6 members, and the `mahavihara` sect at `:1090` with members
  `DBD PEG ARK TSM`.
- Verified — DBD's identity block, `VAN/in_game/setup/countries/india.txt:679-685`,
  `culture_definition = sinhalese religion_definition = theravada`; and
  GAU/SGN/STN at `VAN/in_game/setup/countries/bengal.txt:1-23`, all
  `religion_definition = sunni`.
- Verified — the absence of `gangaikonda`, `gauda`, `pataliputra`,
  `anahilavada` and `tripuri` from `definitions.txt`, and the presence of
  `thanjavur`, `kalyani`, `monghyr`, `dhar`, `patan`, `jayankondam`, `gaur`,
  `patna`, `dvarasamudra`, `tissamaharama`, `sihor`, `sambhar`, `delhi`.
- **Not verified, and stated as such:** every 1066 ruler identity, accession
  date, regnal number and polity extent flagged `[U]` or `[D]` above. The
  Paramara succession (Jayasimha vs Udayaditya), the Pala regnal dates, the
  Chola/Ruhuna line on Ceylon and the extent of Karna of Tripuri's empire are
  the four where the sources genuinely differ, and each carries its
  alternative in the OPEN DECISIONS.
