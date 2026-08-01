# THE BALTIC 1066 — the pagan shore before the crusade (DRAFT)

**DRAFT — pending main-session review. Nothing here has been written into any
mod file.** Produced by an Opus research agent, 2026-08-01, against commit
`3c18c1c` (34 items landed). Every mechanical claim carries a `file:line`.
Historical claims that no file can settle are flagged `[U]` (unverified /
estimated) or `[D]` (sources genuinely differ), never asserted silently.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, 491,179 bytes, present)
`MOD = .../1066 Test Mod`

**Method, and the proof that the resolver is honest.** Counts come from an
independent reimplementation of `build_setup.py`'s parsers — `_parse_defs`
(`tools/build_setup.py:711`), `_ownable_set` (`:736`), `_resolve_ruleset`
(`:779`), `find_block_end` (`:4738`) and the `OWN_KEYS`/`COUNTRY_RE` country
reader (`:4933`, `:4791`) — all reading `encoding='utf-8-sig'`, all
token/brace based, comments masked before tokenising, never line-anchored
regex alone.

**Proven on a known positive:** the resolver was pointed at eleven of the
build's shipped `LOCATION_VACATED_EXPECT` constants and reproduced every one
exactly — `KHD 16`, `OGE 18` (`tools/build_setup.py:1405` loop), `CHG 21`
(`:1237`), and the eight Danube tags `WAL 44 / IAS 11 / BIA 10 / BLD 9 /
SRC 4 / HTN 3 / HSC 3 / SSI 3` (`:1365-1369`). Eleven of eleven. A resolver
that could not reproduce those would have been discarded.

The template parser was proven separately by asserting `cult['dadu'] ==
'yan_culture'` — the Northern Dynasties package's own recorded known positive,
and the guard against `location_templates.txt`'s **single-line blocks**, where
a line-anchored `^[ \t]*culture` regex returns a confident zero on all 20,922
entries.

The tag-freeness scanner was proven by feeding it five tags whose status is
known independently: `TEU`, `LIV`, `SXM`, `KRL` (all four in
`VAN/in_game/setup/countries/baltics.txt`) came back TAKEN with their registry
`file:line`; `PRU` came back TAKEN on 87 word hits with an **empty registry**,
which is itself the correct answer (§A.4).

---

## 0. The theater, and the three findings that shape it

### 0.1 What the Baltic looks like in the current build

`baltic_region` (`definitions.txt`) is 340 ownable locations and includes
Poland. The four areas this package is about:

| area | ownable | owners in the MOD build today (identical to vanilla — the mod has never touched this theater) |
|---|---|---|
| `baltic_area` | **56** | LIV 30, ARR 8, **DAN 7**, BIO 4, BID 4, KUR 2, RIG 1 |
| `prussia_area` | **44** | TEU 37, ERM 3, CHL 2, SMD 1, PMS 1 |
| `lithuania_area` | **43** | LIT 43 |
| `samogitia_area` | **16** | LIT 16 owned — and **TEU controls 6 of them** (§0.3) |

Adjacent, in scope only as edges: `mazovia_area` 33 (RAW 14, CZK 8, PLK 6,
**LIT 5**), `central_poland_area` 23 (SDZ 8, POL 6, LCZ 4, **TEU 3**, INO 2),
`pomerania_area` 31 (WOL 15, STE 6, KMM 3, BRA 3, **TEU 2**, MKL 1),
`mecklenburg_area` 15 (MKL 8, GSW 3, SWR 2, WRN 2), `black_ruthenia_area` 39
(KIE 22, NRK 11, **LIT 6**), `karelia_area` 44 (NOV 22, 22 unowned).

**Measured: `build_setup.py` contains ZERO references to `baltic_region`,
`baltic_area`, `prussia_area`, `lithuania_area`, `samogitia_area` or
`mazovia_area`, and ZERO string literals naming any of the 159 locations in
those areas.** The Baltic is untouched ground. This is the last large European
theater still shipping its 1337 map wholesale.

### 0.2 Vanilla ships the entire pagan Baltic already — as cultures, and as two landless tags

This is the finding that makes the package cheap. `VAN/in_game/setup/countries/baltics.txt`
is a fifteen-tag file, and its identity fields are already 1066-correct where
it matters:

| tag | line | `culture_definition` | `religion_definition` | landed today |
|---|---|---|---|---|
| LIV | `:1` | `german_baltic` | `catholic` | 30 |
| **TEU** | `:16` | `prussian` | `catholic` | 43 owned + 6 controlled |
| ERM | `:30` | `prussian` | `catholic` | 3 |
| CHL | `:37` | `prussian` | `catholic` | 2 |
| PMS | `:44` | `prussian` | `catholic` | 1 |
| SMD | `:51` | `prussian` | `catholic` | 1 |
| BIO | `:58` | `german_baltic` | `catholic` | 4 |
| KUR | `:67` | `german_baltic` | `catholic` | 2 |
| BID | `:74` | `german_baltic` | `catholic` | 4 |
| RIG | `:81` | `german_baltic` | `catholic` | 1 |
| ARR | `:89` | `liv` | `catholic` | 8 |
| **KRL** | `:98` | `karelian` | **`muinaisusko`** | 0 — a `type = pop` country (§0.4) |
| LIT | `:106` | `aukstaitian` | **`romuva`** | 70 |
| **SXM** | `:117` | `samogitian` | **`romuva`** | 0 — a landless revolter shell |

`romuva` (`VAN/in_game/common/religions/folk_european.txt:128`, `group =
folk_european_group`, `tags = { folk_european_gfx pagan_gfx }`) and
`muinaisusko` (`:160`, `color = map_tavastian`) are **real, shipped religions**.
Every Baltic culture the period needs is shipped too, with `file:line`:

| culture | file:line | language | note |
|---|---|---|---|
| `aukstaitian` | `cultures/baltic.txt:1` | `lithuanian_dialect` | `color = map_LIT`; groups `lithuanian_group` + `baltic_group` |
| `curonian` | `:22` | `western_baltic_dialect` | `color = map_curonian` |
| `estonian` | `:44` | `estonian_dialect` | `color = map_estonian` |
| `latvian` | `:63` | — | `color = map_latvian` |
| `liv` | `:85` | — | `#Finnic`; `color = map_liv` |
| `samogitian` | `:105` | — | `color = map_samogitian` |
| `sudovian` | `:126` | — | `color = map_sudovian` |
| **`pruthenian`** | `:146` | — | **the Old Prussians** |
| `german_baltic` | `:166` | `low_german_dialect` | the Baltic Germans |
| `prussian` | `cultures/german.txt:305` | `low_german_dialect` | **a GERMAN culture** — not the Old Prussians |
| `karelian` | `cultures/finno_ugric.txt:64` | — | |
| `polabian` | `cultures/west_slavic.txt:108` | `polabian_dialect` | `color = map_polabian`; **zero locations** |

**The `prussian` / `pruthenian` trap.** They are two different cultures in two
different files, and vanilla paints both on `prussia_area`: `prussian` on 19
locations, `pruthenian` on 10. TEU's registry `culture_definition` is
`prussian`, i.e. the **German** settler culture. Any 1066 Prussian tag must
carry `pruthenian`. A package written from the tag's own registry line would
give the pagan Prussians a Low German identity, with no error.

**Template religion and culture, measured across the four areas:**

| area | template cultures | template religions |
|---|---|---|
| `baltic_area` 56 | `estonian` 23, `latvian` 20, `liv` 7, `curonian` 6 | **`catholic` 56** |
| `prussia_area` 44 | `prussian` 19, `pruthenian` 10, `kashubian` 6, `samogitian` 4, `greater_polish` 3, `sudovian` 2 | `catholic` 41, `romuva` 3 |
| `lithuania_area` 43 | `aukstaitian` 32, `sudovian` 6, `polatskian_culture` 3, `samogitian` 2 | `romuva` 40, `orthodox` 3 |
| `samogitia_area` 16 | `samogitian` 14, `aukstaitian` 1, `sudovian` 1 | `romuva` 16 |

So the **cultures are already right and the religions are half right**. Vanilla
ships `romuva` on exactly 64 locations globally — 40 in `lithuania_area`, 16 in
`samogitia_area`, 5 in `black_ruthenia_area`, 3 in `prussia_area` — and
`catholic` on all 56 of Livonia/Estonia/Courland, which is flatly wrong for
1066 (Livonia is converted by the sword 1198-1227 [U], Estonia 1208-1227 [U],
Prussia 1230s-1283 [U], Samogitia not until 1413 [U]). **That is a pop-phase
correction, not a setup one** — recorded in §H so the pop phase inherits the
list rather than re-deriving it.

`muinaisusko` and `polabian` are placed on **ZERO** locations. That is the
`cuman_culture` / `mi_niah_culture` shape exactly: a definition with no pops,
which is precisely what a `culture_definition` / `religion_definition` field is
for.

### 0.3 THE LANDMINE: six locations owned by one tag and controlled by another

**Ten ownable locations in the entire game appear in TWO tags' ownership
blocks. Six of them are in this package's theater.**

| location | who | area |
|---|---|---|
| `palanga`, `rietavas`, `silale`, `skuodas`, `taurage`, `mazeikiai` | **LIT `own_core`** + **TEU `control`** | `samogitia_area` |
| `arshgul`, `madinat_alawiyyin`, `ras_al_ain`, `saida` | TLE `own_core` + MOR `control` | `algiers_area` |

Vanilla's 1337 model of the Teutonic occupation of Samogitia (and Morocco's of
Tlemcen): LIT *owns* the six, TEU *occupies* them. `TEU`'s block carries
`control = { … }` with exactly those six tokens.

Three separate parts of the build read `control` as ownership, because it is
the last member of `OWN_KEYS` (`tools/build_setup.py:4933-4936`):

1. **`_remove_owned_many` (`:4960-4968`)** asserts `len(idx.get(l, [])) != 1`
   and exits. Granting any of the six — which any Samogitian recipient must —
   dies with
   `LOCATION_GRANTS[SXM]: ownership occurrences != 1 for ['mazeikiai(2)', 'palanga(2)', …]`.
2. **The `LANDLESS_AFTER` guard (`:5364-5382`)** loops `for key in OWN_KEYS`
   and exits on any surviving token: a TEU stripped of its 43 real holdings
   still carries six `control` tokens and dies with
   `LANDLESS_AFTER: TEU still owns ['palanga', …]`.
3. **The orphan-capital guard (`:5764-5793`)** builds `held` from the same
   `OWN_KEYS` and fires `if held and capm.group(1) not in held` (`:5785`) — a
   TEU holding only the six controlled locations is **not** landless by that
   test, so `capital = malbork` becomes an orphan and the build reports
   `capitals stripped without a CAPITAL_FIXES repoint: TEU->malbork`.

**No existing mechanism handles this.** `FIELD_FIXES` cannot: it runs at
`:5464`, *after* the grants (`:5258`), the vacates (`:5330`) and the landless
guard (`:5364`). §I prescribes the minimal new step and where it must sit.

### 0.4 `type = pop` countries — a mechanism the project has not used

`KRL` is not a landless shell. It is a **pop country**:

```
	KRL = {
		type = pop
		add_pops_from_locations = {
			maloshuyka sumsky_posad unezhma vygozero
			…
			vyborg villmanstrand veckelax vederlax valkeasaari kyyrola beryozovskoye heinjoki jaskis
		}
		discovered_regions = { scandinavian_region }
		discovered_areas = { pomorye_area kola_area arkhangelsk_area west_novgorod_area }
		starting_technology_level = 0
		include = "eurasian_tribe"
		government = { type = tribe  heir_selection = tribal_oldest_male  ruler = random }
	}
```
(`MOD/main_menu/setup/start/10_countries.txt`, KRL block; identical in vanilla.)

**Measured: 448 `type = pop` countries in vanilla, 448 in the mod build** — the
mod has never touched one. They hold **no territory and no claims** and the
engine does not reject them at start, which means `country_type = pop` is a
legal landless state *without* `our_cores_conquered_by_others` — an exemption
from the `initialize_from_bookmark.cpp:592` class that costs the seventeen-line
Italy North failure everywhere else.

Five of them have pops in this theater: **KRL** 35 (`karelia_area` 25,
`finland_area` 9, `west_novgorod_area` 1), **TAV** 15, **SVO** 10, **SMI** 7,
**KVE** 4. That is vanilla's model of the stateless Finnic north, and it is
already the 1066-correct answer (§H).

`country_type = pop` also has a naming consequence: `country_ranks.txt:5`,
`country_rank_people`, is the **first branch in the file** and its trigger is
`country_type = pop` AND `government_type = government_type:tribe`. A pop
country renders with `country_rank_people: "People"` / `_ADJ: "popular"`
(`government_names_l_english.yml:39-40`) regardless of its declared rank. A
normal tribe never reaches it.

---

## A. Registry

### A.1 What already exists and needs nothing

**`SXM` and `KRL` are free wins.** Both are vanilla registry entries
(`baltics.txt:117`, `:98`) with 1066-correct identity fields — `samogitian` +
`romuva`, `karelian` + `muinaisusko` — vanilla arms, vanilla loc rows
(`SXM: "Samogitia"`, `KRL: "Karelia"`, `country_names_l_english.yml:2953`,
`:64`), and vanilla colours. Reusing them costs **zero** registry blocks, zero
CoA decisions and zero loc rows. SXM is currently a landless revolter shell
whose `our_cores_conquered_by_others` is exactly the sixteen Samogitian
locations; KRL is a pop country and is left alone entirely.

### A.2 Freeness of the new candidates — three scans each

Per the `map_TAG` blind-spot lesson (`docs/HANDOFF.md`, AUDIT-2026-07-31 D3):
(1) word-boundary `\bTAG\b` over the whole vanilla tree, non-localisation and
English-localisation counted separately; (2) **substring** `_TAG\b|\bTAG_`
over the same tree — the scan that catches `map_TAG`, `TAG_ADJ`, formable
`flag = TAG` and gfx keys; (3) both scans over the whole mod repo. Plus a
registry index over all 2,398 tags in `VAN/in_game/setup/countries/*.txt` and
`MOD/in_game/setup/countries/*.txt`.

| candidate | VAN word | VAN en-loc | VAN sub | MOD word | MOD sub | registry | verdict |
|---|---|---|---|---|---|---|---|
| **PRS** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **SUD** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **KUO** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **ZEM** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **LTG** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **ESO** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **AUK** | 0 | 0 | 0 | 0 | 0 | — | **FREE** (needed only under §C option 2) |
| NAT, POG, NDR, SKV, OSE, UGA, SBI, JAT, YOT, OSL, VIR, HAR, REV, JRV, LAA, SEG, SEO, LVS, RGN | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| **OBO**, **LTC**, **WGR**, **RUG**, **WEN** | 0 | 0 | 0 | 0 | 0 | — | free (banked for the Wendish slice, §D.4) |
| **CUR** | 0 | 0 | **11** | 0 | 0 | — | **avoid** — every hit is `CUR_POP_DEMANDS`, one interface key in 11 languages (`interfaces_l_english.yml:362`). Mechanically harmless, but a `CUR_ADJ` living beside it is a trap for the next reader. Use `KUO`. |
| **EST** | 0 | 0 | **23** | 0 | 0 | — | **avoid** — `EST_SATISFACTION_TITLE` (`interfaces_l_english.yml:3778`) and `$EST_VAL$` (`:4287`). Use `ESO`. |
| SAM | 21 | 1 | 48 | 2 | 0 | `polynesia.txt:181` | TAKEN (Samoa) |
| SKA | 22 | 1 | 48 | 2 | 0 | `east_africa.txt:431` | TAKEN (Sakalava) |
| BRT | 21 | 1 | 48 | 1 | 0 | `siberia.txt:82` | TAKEN |
| RAN | 23 | 1 | 48 | 2 | 0 | `west_africa.txt:431` | TAKEN |
| SMG | 23 | 1 | 50 | 5 | 1 | `east_asia.txt:2043` | TAKEN |
| SLN | 28 | 1 | 48 | 3 | 0 | `british_isles.txt:401` | TAKEN |
| CRN | 30 | 1 | 114 | 1 | 0 | `british_isles.txt:416` | TAKEN |
| SAA | 30 | 1 | 48 | 10 | 0 | `north_germany.txt:147` | TAKEN |
| WRM | 23 | 1 | 48 | 1 | 0 | `north_germany.txt:548` | TAKEN |
| VLT | 42 | 1 | 48 | 19 | 0 | `italy.txt:550` | TAKEN |
| PRZ | 33 | 2 | 51 | 4 | 1 | `italy.txt:581` | TAKEN |
| SGL | 21 | 1 | 48 | 1 | 0 | `south_germany.txt:542` | TAKEN |
| MAA | 10 | 1 | 25 | 2 | 0 | `east_africa.txt:647` | TAKEN |

The `CUR` and `EST` rows are the substring scan earning its keep: both have
**zero** word hits and **no registry entry**, so a word-boundary-only check
would have called them free.

### A.3 The blocks

Six new tags, appended to `in_game/setup/countries/zz_1066_new_countries.txt`
(registry **58 → 64**; count measured by
`grep -c "^[A-Z0-9]\{2,6\} = {"`).

```
PRS = { #The Prussians — the eleven pagan lands between the Vistula and the Nemunas
	color = map_PRU
	color2 = rgb { 16 41 202 }

	culture_definition = pruthenian
	religion_definition = romuva
}

SUD = { #Sudovia / Yotvingia — the Sudovian forest between Prussia and Lithuania
	color = map_sudovian
	color2 = rgb { 16 41 202 }

	culture_definition = sudovian
	religion_definition = romuva
}

KUO = { #The Curonians — the sea-kings of the Courland coast
	color = map_curonian
	color2 = rgb { 16 41 202 }

	culture_definition = curonian
	religion_definition = romuva
}

ZEM = { #Semigallia and Selonia — the middle Daugava and the Lielupe
	color = map_latvian
	color2 = rgb { 16 41 202 }

	culture_definition = latvian
	religion_definition = romuva
}

LTG = { #The Latgalians and the Daugava Livs — Jersika, Koknese, Turaida
	color = map_liv
	color2 = rgb { 16 41 202 }

	culture_definition = latvian
	religion_definition = romuva
}

ESO = { #Estonia — the maakonnad, no king
	color = map_estonian
	color2 = rgb { 16 41 202 }

	culture_definition = estonian
	religion_definition = muinaisusko
}
```

**`religion_definition = romuva` on five of six** — verified real,
`folk_european.txt:128`. **`muinaisusko` on ESO** — `:160`, and it is placed on
**zero** locations, the identity-only shape CUM already ships. `[D]` on the
theology: whether the Estonians' Taara/Uku cult is properly "Muinaisusko" (a
modern Finnish coinage for the Finnic folk religion) is a naming question, not
a mechanical one; vanilla itself assigns `muinaisusko` to KRL, whose culture is
`karelian`, so the precedent is vanilla's own.

**`culture_definition = latvian` on both ZEM and LTG** is the honest compromise:
vanilla ships no `semigallian`, `selonian` or `latgalian` culture, and paints
`latvian` on 20 of `baltic_area`'s 56 — including every Semigallian, Selonian
and Latgalian location. Same class as `kharchin_culture` for the Khitans and
`bolghar_culture` for BLH, accepted twice already (`docs/HANDOFF.md:406-408`).
LTG's *pops* include 7 `liv` locations; the split is deliberate and noted for
the pop phase.

### A.4 Colours: ZERO new definitions needed

Every colour key above already exists in `VAN/main_menu/common/named_colors/02_map.txt`:

| key | line | value | used by any country today |
|---|---|---|---|
| `map_PRU` | `:239` | `hsv360 { 229 80 30 }` | **no** |
| `map_sudovian` | `:271` | `rgb { 132 144 54 }` | **no** |
| `map_curonian` | `:270` | `rgb { 14 52 212 }` | **no** |
| `map_latvian` | `:78` | `rgb { 0.9 0.86 0.71 }` | **no** |
| `map_liv` | `:79` | `rgb { 155 126 71 }` | **no** |
| `map_estonian` | `:77` | `rgb { 0.0 0.60 0.45 }` | **no** |
| `map_samogitian` | `:268` | `rgb { 0 124 45 }` | SXM (correct, unchanged) |
| `map_karelian` | `:24` | `rgb { 209 252 22 }` | KRL (correct, unchanged) |
| `map_osel` | `:74` | `rgb { 62 122 189 }` | BIO (goes landless) |
| `map_polabian` | `:278` | `rgb { 235 175 20 }` | **no** — banked for the Wendish slice |

**Measured against the colour-twin class** (`19a3fe6`, engine line
`"<TAG> has same color as <TAG>"`): all six keys are currently used only by
*cultures*, never by a country, and **no other country colour in vanilla or the
mod resolves to the same RGB triple**. Six new tags, zero new colour rows,
zero new twin lines. `main_menu/common/named_colors/zz_1066_map_colors.txt`
(74 `map_` keys today) is untouched by this package.

`map_PRU` doubles as the `PRU_f` formable's colour (`00_formable_countries.txt:1471`)
and as `prussian`'s culture colour (`german.txt:308`). Reuse is legal and gives
the pagan Prussians the same blue the Kingdom of Prussia later wears — a
deliberate continuity. If that reads badly next to POL, `map_pruthenian` does
**not** exist and would have to be authored.

### A.5 `PRU` is a formable-only tag — a class worth recording

`PRU` returns 87 word hits and 429 substring hits across vanilla, **and has no
`setup/countries` block at all**. Its entire identity lives inside the
formable: `00_formable_countries.txt:1458-1476` carries `name = PRU`,
`flag = PRU`, `adjective = PRU_ADJ`, `tag = PRU`, `color = map_PRU`,
`areas = { prussia_area }`, `required_locations_fraction = 0.75`,
`potential = { culture = { has_culture_group = culture_group:german_group } }`.
`LIV_f` (`:1508`) and `LVA_f` (`:1532`) are the same shape; `GLD`, `KRS`, `SLO`
and `LIB` behaved identically under the scanner.

**Consequence for this package: do NOT reuse PRU as the Prussian tribal tag.**
It would need a registry block the game does not currently have, and it would
collide with a live level-2 historical formable whose whole point is the *later*
German Prussia. `PRS` is free and costs nothing.

**Consequence for the formables, checked:** `PRU_f`'s `potential` is
`german_group` — `pruthenian` is `baltic_group` (`baltic.txt:146-165`), so PRS
can never form PRU. `LIV_f`'s is `german_group` likewise. **`LVA_f`**
(`:1532-1561`, `rule = fantasy`, `level = 2`) is the one that touches us:
`potential` = any baltic_group culture, `required_locations_fraction = 0.75`
over `baltic_area + lithuania_area + prussia_area + samogitia_area +
west_novgorod_area` = 210 ownable. The largest tag this package creates holds
37 (AUK) or 48 (LIT) — **18-23%**, far under the 75% gate. No formable is
consumed and none becomes reachable at start.

### A.6 Coats of arms

The six new tags must each land in `_GENERATOR_OK` (`tools/verify_mod.py:925`)
or carry a CoA block; the check at `:962-968` fails a new registry tag that has
neither. **Recommendation: `_GENERATOR_OK`, tier 4, permanent** — the pagan
Baltic peoples had no heraldry of any kind, and the Order/bishopric arms that
vanilla does ship belong to tags that this package retires rather than creates.
Comment to write: *"the pagan Baltic — no heraldry existed; the crusader arms
belong to the tags this slice retires."*

`SXM`'s arms are vanilla's and pass through the `_van_coa_keys` branch — one
more reason to prefer reuse.

### A.7 Localisation

`MOD/main_menu/localization/english/1066_norman_conquest_l_english.yml` (340
lines today, UTF-8 **with** BOM — loc files keep theirs). One physical line
each, in the file's existing style:

```
 PRS: "Prussia"
 PRS_ADJ: "Prussian"
 SUD: "Sudovia"
 SUD_ADJ: "Sudovian"
 KUO: "Curonia"
 KUO_ADJ: "Curonian"
 ZEM: "Semigallia"
 ZEM_ADJ: "Semigallian"
 LTG: "Latgalia"
 LTG_ADJ: "Latgalian"
 ESO: "Estonia"
 ESO_ADJ: "Estonian"
```

**All six NAME keys are LIVE, and on the map they are the whole string** — §F
works the render out to the character. No `_THE` rows are proposed: the mod's
own `SEL_THE` caveat stands (`docs/HANDOFF.md:1003-1005`), and `$ARTICLE$`
resolves through `common_string_prefix_article: "the"`
(`common_used_strings_l_english.yml:95`) in the branch that uses it, which is
the non-map string only.

`SXM: "Samogitia"` and `SXM_ADJ: "Samogitian"` already exist in vanilla
(`country_names_l_english.yml:2953-2954`). Nothing to add.

---

## B. NEW_COUNTRIES blocks

All six follow the mod's own `CUM` block (`tools/build_setup.py:1351-1357`) —
the attested 1066 tribal shape, and the one the brief names. Neither carries
`own_control_core`: territory arrives by `LOCATION_GRANTS` after insertion, the
QRK/QRA/BLH/QMT route (`:5258`).

```
	PRS = {
		starting_technology_level = 2
		include = "expl_eastern_europe"
		include = "eurasian_tribe"

		country_rank = rank_duchy

		capital = fischhausen
	}
```
…and the same shape for SUD (`capital = suwalki`), KUO (`grobina`),
ZEM (`dobele`), LTG (`koknese`), ESO (`tartu`).

Field by field, verified:

- **`include = "eurasian_tribe"`** — `VAN/main_menu/setup/templates/eurasian_tribe.txt`,
  read in full: `government = { type = tribe  heir_selection = tribal_oldest_male
  … parliament = { parliament_type = assembly } laws = { marriage_law = polygyny
  heir_religion_law = heir_same_religion } privilege = { tribes_tribal_levies
  tribes_allow_gatherings } }`. **27 vanilla users**, plus CUM. It declares no
  `starting_technology_level` and no coast handling, so the block must supply
  the former. `marriage_law = polygyny` is not a misfit here: Baltic pagan
  polygyny is attested by the crusade chroniclers [U].
- **`include = "expl_eastern_europe"`** — its `discovered_regions` include
  `baltic_region` (verified by reading the file), which is where all six
  capitals live. **The capital-discovery assert (`tools/build_setup.py:4862`,
  `"{tag}: capital {cap} is not discovered by any include"`) passes for all
  six.** `expl_northern_europe` also carries `baltic_region` and adds
  `scandinavian_region`; use it instead if a future tag's capital moves into
  Karelia or Finland.
- **`starting_technology_level = 2`** — CUM uses 3, KRL uses 0, `gaelic_tribe`
  ships 2 internally. 2 is the middle and matches the Irish tribal precedent;
  see OPEN DECISION 8. This is a slider, not a correctness question.
- **`country_rank = rank_duchy`** — **measured: all 55 landed `type = tribe`
  countries in the built file carry NO `country_rank` line at all** and let the
  engine derive rank from size. CUM's explicit `rank_duchy` is the mod's own
  departure. Declaring it is what makes the render predictable (§F); omitting it
  is what vanilla does. OPEN DECISION 7.
- **No `court_language`.** `baltic_language` (`VAN/in_game/common/languages/00_baltic.txt:1`)
  **declares no `family` line — measured, `grep -c family` returns 0 for the
  whole file** — and its dialects are `latvian_dialect` (`:47`),
  `lithuanian_dialect` (`:66`) and `western_baltic_dialect` (`:74`). Since no
  name-construction branch that these tags can reach keys on a language family
  (§F), a court language buys nothing and risks nothing. If one is wanted for
  flavour: `western_baltic_dialect` for PRS/KUO (it is `curonian`'s own),
  `lithuanian_dialect` for SUD, `estonian_dialect` for ESO (a dialect of
  `finnish_language`, `00_scandinavia.txt:243`, `family = uralic_language_family`
  at `:247`).
- **No `heir_selection` restatement needed** — `eurasian_tribe` supplies
  `tribal_oldest_male` and nothing strips it. (Contrast the Muslim `_no_coast`
  variant that forced the taifa factory to restate, `tools/build_setup.py:565-571`.)
- **No steppe-horde risk.** `_bad_recip` (`tools/build_setup.py:5212`) exits on
  any grant/transfer recipient whose block resolves to `type = steppe_horde`.
  `eurasian_tribe` is `type = tribe`. **Tribes are explicitly fine** — CUM,
  the Irish tribal tags and the 46 Jurchen tags are all grant-adjacent already.

### B.1 The capitals, and why each one

Every capital was checked to be *inside its own tag's resolved grant list*
(the `_CENTRALASIA_TAGS` assert's requirement) — all six pass. Names are the
map's, which is the Order-era German/Latvian layer; the 1066 names are given
so the comment can be honest. This is the `ningxia`-for-Xingqing situation the
mod has absorbed before.

| tag | capital | loc string | 1066 reality |
|---|---|---|---|
| PRS | `fischhausen` | Fischhausen | Sambia — the most populous Prussian land; Wiskiauten/Kaup, the Viking-age emporium, is on this ground [U]. `konigsberg` is a 1255 Order foundation and `malbork` a 1274 one — both refused deliberately. |
| SUD | `suwalki` | Suwałki | the Sudovian forest; no attested 1066 centre at all [U] — this is a mechanical seat and the comment must say so. |
| KUO | `grobina` | Grobiņa | Seeburg — the Scandinavian-Curonian trading settlement excavated there, 7th-9th c., and named in Rimbert's *Vita Anskarii* [U]. The one genuinely pre-crusade seat in the package. |
| ZEM | `dobele` | Dobele | a Semigallian hillfort [U]. `jelgava` (Mitau) is 1265 and was refused. |
| LTG | `koknese` | Koknese | Kukenois — one of the two Latgalian principalities Henry of Livonia names (with Jersika), tributary to Polotsk [U]. `riga` is 1201 and was refused. |
| ESO | `tartu` | Tartu | Tarbatu; taken by Yaroslav in 1030 and held as **Yuryev** [U] — the one Estonian place with a documented 11th-century identity, and Ugaunia's fort. `tallinn` (Lindanise/Kolyvan) is the alternative. |

---

## C. Lithuania — and the tag-specific rank branch that decides it

### C.1 What LIT is today

```
	LIT = {	#Lithuania
		own_control_core = { … 58 … }
		own_control_integrated = { … 6 … }
		own_core = { … 6 … }              <- the six TEU controls (§0.3)

		include = "expl_eastern_europe"
		include = "lithuanian_monarchy"
		government = { … ruler = random }
		tolerated_cultures = { … }
		capital = vilnius
		dynasty = gediminid_dynasty
		court_language = belarusian_dialect
		country_rank = rank_duchy
		currency_data = { … }
	}
```
70 locations: `lithuania_area` 43, `samogitia_area` 16, `black_ruthenia_area` 6
(`grodno bershty masty sokolka nyasvizh grodek`), `mazovia_area` 5 — the
Podlasie strip (`drohiczyn bielsk_podlaski mielnik sokolow suraz`).

Four fields are 1300s-1400s objects on a 1066 map: `lithuanian_monarchy`
(`VAN/main_menu/setup/templates/lithuanian_monarchy.txt`, read in full —
`type = monarchy`, `heir_selection = favorite_son_elective_succession`, a
sixteen-law estate-parliament state, and its own trailing
`court_language = belarusian_dialect`), `dynasty = gediminid_dynasty` (Gediminas
r. 1316-1341 [U]), `court_language = belarusian_dialect` (the Ruthenian chancery
language of the Grand Duchy), and `capital = vilnius` (first documented 1323
[U]).

### C.2 THE FINDING: `rank_kingdom_grand_duchy_LIT`

`VAN/in_game/common/customizable_localization/country_ranks.txt:1355-1362`:

```
	text = {
		localization_key = rank_kingdom_grand_duchy_LIT
		trigger = {
			tag = LIT

			country_rank_is_duchy = yes
		}
	}
```

with `rank_kingdom_grand_duchy_LIT: "Grand Duchy"` and
`_ruler_male: "Grand Duke"` (`government_names_l_english.yml:634-636`).

`country_ranks.txt` is **first-match**, and this branch sits at `:1357` —
**249 lines before `rank_duchy_tribe` at `:1606`**. `country_rank_is_duchy`
resolves through `country_triggers.txt:44-46` to the country's current rank.

**Therefore: a LIT reskinned as a tribe but keeping `country_rank = rank_duchy`
still renders "Grand Duchy of Lithuania" ruled by a "Grand Duke".** The
government swap is invisible to the name. This is the CLAUDE.md
horde-name class exactly — a name composed somewhere other than where you are
looking — and it is hard-coded on the tag, so no field on LIT can escape it
except the rank itself.

### C.3 The two options, both costed

**Option 1 — keep LIT, reskin it (the brief's first proposal).**
`FIELD_FIXES` surgery in the POK shape (`tools/build_setup.py:2567-2573`, the
exact precedent: `include = "lithuanian_monarchy"` → another template plus a
restated `court_language`):

```python
    "LIT": [('include = "lithuanian_monarchy"', 'include = "eurasian_tribe"'),
            ("\t\tdynasty = gediminid_dynasty\n", ""),
            ("court_language = belarusian_dialect",
             "court_language = lithuanian_dialect"),
            ("country_rank = rank_duchy", "country_rank = rank_county"),
            ("\t\t\truler = random",
             "\t\t\ttype = tribe\n"
             "\t\t\their_selection = tribal_oldest_male\n"
             "\t\t\truler = random")],
```
`country_rank = rank_county` is **mandatory** here, not cosmetic: it is the only
way past `:1357`. The render then becomes `rank_county_tribe` (`:2279`),
`"Tribe"` with `rank_county_tribe_prefix: "Minor"`
(`government_names_l_english.yml:1018-1019`) → **"Minor Tribe of the
Lithuanians"**, ruler "Chieftain", map label "Lithuania". "Minor Tribe" for a
48-location realm is an odd string, and the reader who later restores
`rank_duchy` silently restores the Grand Duchy.

Keeps: the LIT tag, its loc, its arms, its colour, its 14 pool characters.
Costs: 5 FIELD_FIXES pairs, and the standing trap above.

**Option 2 — retire LIT landless, land `AUK` (RECOMMENDED).**
LIT joins `LANDLESS_AFTER` with auto-derived claims over all 70 of its
locations — which is exactly right: the Grand Duchy IS the future object here,
the same treatment TEU and LIV get, and the same shape as SKE, GRA and MAM. A
new `AUK` tag takes the 37 non-Sudovian locations of `lithuania_area` with
`culture_definition = aukstaitian`, `religion_definition = romuva`,
`color = map_aukstaitian` (`02_map.txt:80`, unused by any country),
`capital = kernave`.

`kernave` (Kernavė) is the choice: continuously occupied through the 1st
millennium, five hillforts, the archaeological centre of early Lithuania and
the Grand Duchy's first seat [U]. It is inside `vilnius_province` and inside
AUK's resolved list.

Renders **"Tribe of the Aukštaitians"**, map label **"Aukštaitija"**, ruler
"Chief" — with `rank_duchy` and no trap.

Costs: one more registry block (64 → 65), one more loc pair, one more
`_GENERATOR_OK` entry, and recipients for LIT's 11 edge locations (§E.4).
Gains: the tag-specific branch is bypassed structurally rather than dodged; the
Mindaugas/Gediminas future becomes a claim list; and "Lithuania" stops naming a
polity that will not exist for 190 years.

### C.4 Rulers — there are none, and that is the finding

**No ruler is proposed for any tag in this package.** Every one of them takes
`ruler = random` via its template, and that is not laziness:

- The first named Lithuanian dukes appear in the 1219 treaty with Volhynia
  (twenty-one of them, Mindaugas among the youngest) [U]. Before that the
  sources are silent.
- The Prussians produce no named ruler before Herkus Monte (1260s) [U]; the
  eleven *lands* are named by Peter of Dusburg in the 1320s, projecting
  backwards.
- The Curonian and Oeselian "sea-kings" are a real 1066 phenomenon — Adam of
  Bremen's Curonians and the Saaremaa raiders who sacked Sigtuna in 1187 [U] —
  but no individual is attested for 1066.
- Estonia had no king at all; the *maakonnad* were governed by elders assembled
  at the Raikküla thing [U].

This is the **Pecheneg discipline** (`docs/HANDOFF.md:950-955`, and the
Kipchak decision the user accepted in CENTRAL-ASIA-PACKAGE OPEN DECISION 2)
applied to people rather than to territory. Inventing a Prussian chieftain
would be inventing history to fill a field the engine is happy to fill itself.

**Consequence: `HISTORICAL_RULERS` gains nothing, `NEW_CHARACTERS` gains
nothing, `04_zz_1066_dynasties.txt` gains nothing.** This package is territory,
identity and diplomacy only — the first one in the project with no §C content,
and the honest reason is written above rather than left as an omission.

---

## D. What must die, and what must not

### D.1 THE TEUTONIC ORDER — both instances, identified

The map shows two military-order labels. They are:

| tag | registry | founded | holds today | capital | map label |
|---|---|---|---|---|---|
| **TEU** — the Teutonic Order | `baltics.txt:16` | **1190** Acre; Prussia from **1230** [U] | 43 owned + 6 controlled | `malbork` (Marienburg, 1274 [U]) | **"Teutonic Order"** |
| **LIV** — the Livonian Order | `baltics.txt:1` | Sword Brothers **1202**; absorbed as the Livonian branch **1237** [U] | 30 | `parnu` (Pärnu, 1251 [U]) | **"Livonian Order"** |

Both derive their label from `catholic_military_order`
(`VAN/main_menu/setup/templates/catholic_military_order.txt`, read in full:
`type = theocracy`, `heir_selection = grandmaster_elective`,
`court_language = church_dialect`, `reforms = { military_order_reform }`,
`spiritualist_vs_humanist = -90`). The chain, verified link by link:

- `country_name_construction.txt:117-155`,
  `country_name_construction_prefix_adjective_rank`, whose trigger OR-list
  includes `AND = { has_reform = government_reform:military_order_reform
  OR = { country_rank = rank_kingdom  country_rank = rank_duchy }
  NOT = { tag = KNI } }` (`:139-147`). Both tags are `rank_duchy`. It fires.
- `country_name_construction_prefix_adjective_rank: "$PREFIX$ $ADJ$ $RANK$"`
  and `…_map: "$PREFIX$ $ADJ$ $RANK$"` (`government_names_l_english.yml:9-10`) —
  the map string is the same as the full string.
- `$RANK$` from `country_ranks.txt`: `rank_duchy_order_german_subject` (`:1454`,
  requires `is_subject = yes` + a german-language court/culture),
  `rank_duchy_order_subject` (`:1469`), `rank_duchy_order_german` (`:1480`),
  `rank_duchy_order` (`:1494`) — **all four resolve `"Order"`**
  (`government_names_l_english.yml:811`, `:815`, `:819`, `:823`, each
  `"$rank_duchy_order$"`). They differ only in the ruler title: Grandmaster /
  Landmaster / Hochmeister / Landmeister (`:812`, `:816`, `:820`, `:824`).
  No `rank_duchy_order_prefix` key exists, so `$PREFIX$` is empty.
- `$ADJ$` is the tag's `_ADJ` key: `TEU_ADJ: "Teutonic"`
  (`country_names_l_english.yml:1980`), `LIV_ADJ: "Livonian"` (`:72`).

**So the NAME keys `TEU: "Teutons"` (`:1979`) and `LIV: "Livonia"` (`:71`) are
DEAD on both tags** — another instance of the CLAUDE.md law, found in the wild.
Editing either would do nothing, with no error. Anyone attempting a *rename*
rather than a retirement must know this first.

### D.2 The nine crusader-state satellites

| tag | what | holds | capital |
|---|---|---|---|
| ERM | Ermland / Warmia — prince-bishopric, 1243 [U] | 3 | `lidzbark` (Heilsberg) |
| CHL | Chełmno / Culm — bishopric, 1243 [U] | 2 | `lubawa` |
| PMS | Pomesania — bishopric, 1243 [U] | 1 | `kwidzyn` (Marienwerder) |
| SMD | Samland — bishopric, 1243 [U] | 1 | `fischhausen` |
| ARR | Archbishopric of Riga, 1255 [U] (bishopric 1186) | 8 | `limbazi` |
| RIG | the city of Riga, founded **1201** [U] | 1 | `riga` |
| BID | Bishopric of Dorpat, 1224 [U] | 4 | `tartu` |
| BIO | Bishopric of Ösel-Wiek, 1228 [U] | 4 | `kuressaare` |
| KUR | Bishopric of Courland, 1234 [U] | 2 | `piltene` |

Not one of these institutions, or the town of Riga itself, exists in 1066.
All nine are `catholic_bishopric` / `catholic_republic` includes.

### D.3 Verdict: LANDLESS with claims, for all eleven — never deleted

**Recommendation: TEU, LIV, ARR, KUR, RIG, BID, BIO, ERM, SMD, PMS, CHL all
join `LANDLESS_AFTER` (`tools/build_setup.py:2404-2409`) and take
auto-derived claims** (`_landless_claims`, `:5238-5240`). Four reasons, the
first two mechanical:

1. **`_landless_claims` gives them the crusader future for free.** TEU's claims
   become its 43 Prussian and Pomerelian locations; LIV's its 30 Livonian ones;
   each bishopric's its own see. That IS the thirteenth century, expressed in
   the mod's own established idiom (GRA, MAM, SKE, SYG).
2. **Vanilla ships a lot of content hanging off these tags, and landless keeps
   every bit of it intact.** Measured: seven DHE flavour files naming TEU
   (`flavor_teu.txt`, `flavor_pol_teu.txt`, `flavor_dan_teu.txt`,
   `flavor_swe_teu.txt`, `flavor_brapru_teu.txt`, `flavor_brapru.txt`,
   `flavor_plc.txt`) and three naming LIV; **country-specific advance files**
   `in_game/common/advances/country_TEU.txt` and `country_LIV.txt` (gated
   `potential = { has_or_had_tag = TEU }`, e.g. `teu_crusader_discipline`
   `:1-10`); the `hussite_wars.txt` situation; `laws/01_common.txt:1571-1572`;
   `scripted_triggers/religion_triggers.txt:301-309`
   (`can_give_land_to_pope_trigger`, `trigger_if` on `country_exists = c:TEU`);
   and an `on_action/_hardcoded.txt:135-143` game-start block
   (`c:TEU = { every_current_war = { limit = { c:LIT = { is_war_leader_of = prev } } … } }`).
   Every one is existence- or tag-gated and degrades to a no-op. Deleting the
   registry entries would strand all of it.
3. **The engine requires it.** A landless tag without claims is rejected at
   start — `initialize_from_bookmark.cpp:592`, the seventeen-line Italy North
   class (`docs/EU5-ERROR-DECODER.md`), and the build's own guard at `:5401`.
4. It is what the project already does eleven dozen times.

**The capital guard needs NO `CAPITAL_FIXES` entry for any of the eleven.**
`if held and capm.group(1) not in held` (`tools/build_setup.py:5785`) exempts a
fully landless tag by construction — the POR/`guimaraes` precedent (`:2462`).
Verified individually: every one of the eleven reaches exactly zero holdings
under §E, **provided the TEU control-block strip runs** (§0.3, §I).

### D.4 The Wendish shore — FLAGGED, NOT RESOLVED

Gottschalk of the Obodrites was murdered at Lenzen on **7 June 1066** [U] —
**three months and eight days before `START_DATE = 1066.9.15`**. The pagan
reaction under Blus and then Kruto is the live event of the season: Hamburg
sacked, the Christian mission destroyed, Gottschalk's son Henry in exile in
Denmark, and the Rani of Rügen at the height of their power at Arkona [U].

**What the map ships there** (`north_german_region`), and why this package does
not touch it:

| area | ownable | owners today | template cultures |
|---|---|---|---|
| `mecklenburg_area` | 15 | MKL 8, GSW 3, SWR 2, WRN 2 | `western_pomeranian` 12, `lower_saxon` 2, `markish` 1 |
| `pomerania_area` | 31 | WOL 15, STE 6, KMM 3, BRA 3, **TEU 2**, MKL 1 | `eastern_pomeranian` 13, `western_pomeranian` 10, `markish` 6, `kashubian` 2 |
| `brandenburg_area` | 41 | BRA 21, SOR 6, SWB 4, MAG 3, HVB 2, RUP 1 | `markish` 29, **`sorbian` 7**, `saxon` 4 |

**Three hard reasons to flag rather than fix.** (a) **HRE collision:**
`mecklenburg_area` is in the HRE instance's `areas` list and the Pomeranian
provinces (`schwerin_province vorpommern_province stettin_province
koslin_province pyritz_province stolp_province`) are in its `provinces` list —
`MOD/main_menu/setup/start/15_international_organizations.txt:45`, `:57-58`.
MKL, GSW, SWR, WRN, WOL, STE, KMM, NWG, SOR and BRA are all in its
`members` list (`:38-44`). Carving an Obodrite state out of that is HRE surgery,
which items 23/25 own. (b) **Germany-slice collision:** those tags are the
Germany passes' ground and this package must not touch their work. (c) **No
Slavic pagan religion exists.** Scanned every file in
`VAN/in_game/common/religions/`: there is **no** `slavic_pagan`, no
`rodnovery`, no Wendish religion of any name. An Obodrite tag would need
either an invented religion or a proxy.

**What is banked for whoever does take it:** `polabian` culture is shipped
(`west_slavic.txt:108`, `language = polabian_dialect`, `color = map_polabian`
at `02_map.txt:278`) and placed on **zero** locations — the identity-only shape,
ready to be a `culture_definition`. `sorbian` (`:175`) is placed on 11.
`OBO`, `LTC`, `WGR`, `RUG` and `WEN` are all **FREE** by all three scans and are
banked here so the Wendish slice does not re-derive them.

### D.5 Denmark, Sweden, Norway — one edge, and it is flat wrong

Scanned every Scandinavian tag's Baltic-shore holdings. Exactly one is
indefensible for 1066:

**DAN holds 7 locations in `estonia_province`** — `tallinn`, `narva`, `padise`,
`rakvere`, `rapla`, `toolse`, `vasknarva`, all `estonian` culture. That is
**Danish Estonia**, which begins with Valdemar II's landing at Lyndanisse in
**1219** and ends with the 1346 sale to the Order [U]. In 1066 Denmark under
Svend Estridsen holds nothing across the Baltic. **Recommendation: the seven go
to ESO.** DAN 40 → 33; `capital = roskilde` is untouched, so no guard fires.

Everything else on the Scandinavian shore is left alone: SWE holds 32 of
`finland_area` (a live 1066 anachronism — the Swedish crusades to Finland are
1150+ [U] — but that is a Scandinavian slice's item, not this one, and is
flagged in §H); NOR and SKE touch nothing Baltic.

---

## E. Territory

### E.1 `_BALTIC_RULES` — the definitions-resolved grants

Same 5-tuple shape as `_SELJUK_RULES` / `_CENTRALASIA_RULES` /
`_NORTH_RULES`: `tag: (sweep names, singles, minus-sweeps, minus-singles,
expected)`. Every count below is resolved, not transcribed, and every list was
tested for pairwise disjointness by the resolver (zero overlaps).

```python
_BALTIC_RULES = {
    # THE PRUSSIANS. The five eastern provinces are the Prussian lands
    # proper — Sambia, Natangia, Warmia, Pogesania, Pomesania, Barta,
    # Galindia, Nadruvia, Skalvia. elk and barten are sudovian-culture
    # and go to SUD.
    "PRS": (["lower_prussia_province", "upper_prussia_province",
             "warmia_province", "masuria_province",
             "lithuania_minor_province"], [], [], ["elk", "barten"], 26),

    # SUDOVIA / YOTVINGIA. Every sudovian-culture location that forms a
    # contiguous block: the Suwalki lakes, the two Masurian outliers, the
    # upper Nemunas crossings, and (option 2 only) the Grodno pocket.
    "SUD": (["suwalki_province"],
            ["elk", "barten", "lazdijai", "alytus", "vilkaviskis"],
            [], [], 8),

    # THE CURONIANS — the whole Courland peninsula, Seeburg to Domesnes.
    "KUO": (["courland_province"], [], [], [], 8),

    # SEMIGALLIA AND SELONIA — the Lielupe and the middle Daugava.
    "ZEM": (["semigalia_province", "selonia_province"], [], [], [], 7),

    # THE LATGALIANS AND THE DAUGAVA LIVS — Latgale, Tolowa, and the
    # Livonian river mouth (Riga is not founded; salaspils is Holme).
    "LTG": (["latgalia_province", "inner_livonia_province",
             "south_livonia_province"], [], [], [], 17),

    # ESTONIA — Sakala, Ugaunia, Revala/Harjumaa/Virumaa, Laanemaa and
    # Saaremaa. Includes the seven Danish Estonian locations (1219!).
    "ESO": (["north_livonia_province", "tartu_province",
             "estonia_province", "rotalia_province"], [], [], [], 24),

    # SAMOGITIA — vanilla's own SXM revived onto its own claim list.
    "SXM": (["samogitia_area"], [], [], [], 16),

    # POLAND — Pomerelia (Gdansk, Tuchola), Culmerland and the Dobrzyn
    # land: Piast ground in 1066, Order ground from 1228/1308.
    "POL": (["danzig_province", "tuchola_province", "chelmno_province",
             "dobrzyn_province"], ["bytow", "lebork"], [], [], 21),

    # HOHENLOHE — mergentheim, the Order's post-1525 seat, back to the
    # local Franconian lord.
    "UFF": ([], ["mergentheim"], [], [], 1),
}
```

**Resolved, with donors:**

| tag | n | donors | template cultures |
|---|---|---|---|
| **PRS** | 26 | TEU 21, ERM 3, SMD 1, PMS 1 | `prussian` 12, `pruthenian` 10, `samogitian` 4 |
| **SUD** | 8 | LIT 6, TEU 2 | `sudovian` 8 |
| **KUO** | 8 | LIV 6, KUR 2 | `curonian` 6, `liv` 2 |
| **ZEM** | 7 | LIV 7 | `latvian` 6, `liv` 1 |
| **LTG** | 17 | ARR 8, LIV 8, RIG 1 | `latvian` 14, `liv` 2, `estonian` 1 |
| **ESO** | 24 | LIV 9, **DAN 7**, BID 4, BIO 4 | `estonian` 22, `liv` 2 |
| **SXM** | 16 | LIT 16 | `samogitian` 14, `aukstaitian` 1, `sudovian` 1 |
| **POL** | 21 | TEU 19, CHL 2 | `kashubian` 10, `prussian` 7, `greater_polish` 4 |
| **UFF** | 1 | TEU 1 | `east_franconian` 1 |
| **total** | **128** | TEU 43, LIV 30, LIT 22, ARR 8, DAN 7, BID 4, BIO 4, ERM 3, KUR 2, CHL 2, RIG 1, SMD 1, PMS 1 | |

`mergentheim` → **UFF (Hohenlohe)** because UFF already holds `crailsheim` and
`ohringen`, the two other Hohenlohe locations in the same
`tauberfranken_province`, and Mergentheim was a Hohenlohe possession before the
1219 donation [U]. Note the anachronism this *inherits*: the Hohenlohe family
itself is first attested c. 1153 [U]. That is the Germany slice's item; flagged,
not fixed. Alternative: `MAI` (Mainz), which holds `tauberbischofsheim` next
door.

### E.2 What each donor keeps

| tag | before | after | verdict |
|---|---|---|---|
| **TEU** | 43 owned (+6 controlled) | **0** | LANDLESS — requires the control strip (§I) |
| **LIV** | 30 | **0** | LANDLESS |
| **ARR** | 8 | **0** | LANDLESS |
| **BID** | 4 | **0** | LANDLESS |
| **BIO** | 4 | **0** | LANDLESS |
| **ERM** | 3 | **0** | LANDLESS |
| **CHL** | 2 | **0** | LANDLESS |
| **KUR** | 2 | **0** | LANDLESS |
| **RIG** | 1 | **0** | LANDLESS |
| **SMD** | 1 | **0** | LANDLESS |
| **PMS** | 1 | **0** | LANDLESS |
| **DAN** | 40 | 33 | keeps `roskilde`; no guard |
| **LIT** | 70 | 48 (option 1) / **0** (option 2) | §C.3 |
| **POL** | 75 | 96 | recipient |
| **UFF** | 4 | 5 | recipient |

```python
BALTIC_LANDLESS = ("TEU", "LIV", "ARR", "KUR", "RIG", "BID", "BIO",
                   "ERM", "SMD", "PMS", "CHL")            # +("LIT",) under option 2
```
appended into `LANDLESS_AFTER` (`tools/build_setup.py:2404-2409`).

**`_landless_claims` (`:5238`) snapshots `_owned_by(src, t)` BEFORE the grants,
and `_owned_by` reads `control` too.** So the control strip must run **before
`:5238`**, not merely before the grants — otherwise TEU's claims would include
six Samogitian locations it never owned, and a 1066 Teutonic claim on Samogitia
is exactly the wrong thing to write into the file.

### E.3 THE CONSTANT MOVES — and the good news is that there are almost none

**Measured: no `LOCATION_VACATED` pool in the build touches the Baltic.** The
four pools in existence are `["moldavia_area", "wallachia_area"]` (GLH + eight
Danube tags), `["dzungaria_area", "emin_province"]` (CHG), the GLH steppe list
(`:1230-1236`), and `["mongolia_region", "manchuria_region", …]` (CHI and the
five hordes, `:1390-1405`). None resolves into `baltic_region`.

**Therefore: ZERO `LOCATION_VACATED_EXPECT` constants move.** This is the first
territory package in the project with none.

What does move:

| constant | file:line | from | to | why |
|---|---|---|---|---|
| registry blocks | `zz_1066_new_countries.txt` | 58 | **64** (65 with AUK) | §A.3 |
| `LANDLESS_AFTER` | `build_setup.py:2404` | current | **+11** (+12 with LIT) | §E.2 |
| `n_landless_deps` assert | `:6565` | **233** | **243** | the 10 Order/bishopric dependencies (§G.1) |
| `n_pacts` assert | `:6587` | **7** | **8** | TEU↔BOH alliance (§G.1) |
| named dependency strips | new, the Rus shape `:6425-6435` | — | **+2** | LIT→NRK, LIT↔POL (§G.2) |
| `LOCATION_VACATED_EXPECT[*]` | `:1237`, `:1364`, `:1390`, `:1405` | — | **unchanged** | measured |
| locations granted | build report | current | **+128** (+176 under option 2) | §E.1 |
| locations vacated | build report | current | **unchanged** | nothing is vacated |

`n_landless_deps` 233 → 243 is derived, not guessed: **exactly 11 lines in
`MOD/main_menu/setup/start/12_diplomacy.txt` name any of the eleven tags**
(measured), of which 10 are `dependency` and 1 is `scripted_mutual` (§G.1).

### E.4 The Lithuanian edge — 11 locations, and who should have them

Under option 1 LIT keeps them and nothing moves. Under option 2 they need
recipients, and the honest answer crosses two other packages' seams:

| locations | area | culture / religion | 1066 | recommended |
|---|---|---|---|---|
| `drohiczyn bielsk_podlaski mielnik sokolow suraz` | `mazovia_area` | `mazovian` / catholic | Podlasie — Mazovian marchland raided by the Yotvingians [U] | **RAW** (Rawa/Mazovia, holds 14 in the same area) |
| `grodno sokolka` | `black_ruthenia_area` | `sudovian` / romuva | the Yotvingian pocket on the Neman [D — Grodno is a Rurikid town by 1116 [U]] | **SUD** |
| `grodek bershty` | `black_ruthenia_area` | `mazovian` / `aukstaitian`, romuva | the forest between | **SUD** |
| `masty nyasvizh` | `black_ruthenia_area` | `polesian_culture` / orthodox | Kievan/Turov ground | **NRK** (holds 11 in the same area) |

That is the Rus package's seam and the Poland slice's seam. **Flagged with a
recommendation, not resolved** — OPEN DECISION 4.

### E.5 What this slice moves, in one line

**Option 1 (LIT reskinned):** 128 locations change owner, 0 vacated, **11 tags
retired**, 6 new tags, 1 tag revived (SXM), 0 rulers, 0 dynasties.

**Option 2 (LIT retired, AUK lands):** **176** locations change owner, 0
vacated, **12 tags retired**, 7 new tags, 1 revived, 0 rulers, 0 dynasties.

### E.6 The pop-line class does not grow

`docs/EU5-ERROR-DECODER.md:676` records the ~504-line
`jomini_script_system.cpp:252` class, one line per pop on vacated **settled**
land. **This package vacates nothing** — every one of the 128 (or 176)
locations goes from one owner to another, and all of them are owned in vanilla
(measured: zero `=UNOWNED=` across all nine rule sets). The class neither grows
nor shrinks. That is the direct consequence of the brief's own law: prefer real
recipients on settled ground.

---

## F. Rank, government and naming — worked out to the rendered string

### F.1 The two branches that matter, and the law they establish

`country_name_construction.txt` is **first-match**. For a `type = tribe`,
pagan, non-horde, non-Muslim, non-tagged country, every branch fails until the
declared fallback:

| line | branch | why it fails for a Baltic tribe |
|---|---|---|
| `:4-32` | ROM / BYZ specials | tag-gated |
| `:35`, `:46`, `:80` | PAP / GBR / MAM / DAU / PAL / MAL | tag-gated |
| `:92` | `prefix_name` | needs `rank_empire` + a `chinese_language_family` court |
| `:100` | `prefix_name_horde` | needs `government_type = steppe_horde` |
| `:107` | bank special | tag-gated |
| `:117` | `prefix_adjective_rank` | needs rank_empire, or one of eight named tags, or a frisian republic, or **`military_order_reform`**, or `japanese_clan`, or `country_type = pop` |
| `:160` | `sultanate` | needs `religion.group = muslim` |
| `:169` | `crown` | tag-gated ARA/CAS/POL/BOH |
| **`:184-186`** | **`prefix_rank_of_name`, `fallback = yes`** | **fires** |

Loc (`government_names_l_english.yml`):
- `country_name_construction_prefix_rank_of_name: "$PREFIX$ $RANK$ of $ARTICLE$ $NAME$"` (`:11`)
- **`country_name_construction_prefix_rank_of_name_map: "$NAME$"` (`:12`)**

**THE LAW, sharpened.** There is no tribe branch in `country_name_construction.txt`
at all, so every tribal tag lands on the fallback — and the fallback's **map**
variant is bare `$NAME$`. **A Baltic tribal tag's map label is its NAME key
verbatim, nothing else.** The rank word appears only in the long form
(diplomacy panels, tooltips).

The one caveat that must be checked per tag, and which §C.2 shows is not
theoretical: `country_ranks.txt` **is** full of tag-gated branches, and one of
them (`:1357`, LIT) sits above the tribe branches.

### F.2 The rank word, verified per rank

`country_ranks.txt`, first-match, walking down for `government_type = tribe`,
`country_type != pop`:

| branch | line | fires when | loc |
|---|---|---|---|
| `country_rank_people` | **`:5`** | `country_type = pop` **and** tribe | `"People"` / `_ADJ: "popular"` (`:39-40`) |
| `rank_empire_tribe` | `:325` | empire + tribe | `"Tribes"`, prefix `"Imperial"` (`:182-183`) |
| `rank_kingdom_tribe` | `:945` | kingdom + tribe | — |
| **`rank_duchy_tribe`** | **`:1606`** | duchy + tribe | **`"Tribe"`, ruler `"Chief"`** (`:790-791`), **no `_prefix` key** |
| **`rank_county_tribe`** | **`:2279`** | county + tribe | **`"Tribe"`, prefix `"Minor"`, ruler `"Chieftain"`** (`:1018-1021`) |

The maori and haudenosaunee variants at `:1590`/`:1600` and `:2263`/`:2273`
are culture-gated and unreachable.

### F.3 What each proposed tag renders as

| tag | rank | branch chain | full name | **map label** | ruler title |
|---|---|---|---|---|---|
| **PRS** | `rank_duchy` | `:184` fallback + `:1606` | "Tribe of the Prussians" | **Prussia** | Chief |
| **SUD** | `rank_duchy` | same | "Tribe of the Sudovians" | **Sudovia** | Chief |
| **KUO** | `rank_duchy` | same | "Tribe of the Curonians" | **Curonia** | Chief |
| **ZEM** | `rank_duchy` | same | "Tribe of the Semigallians" | **Semigallia** | Chief |
| **LTG** | `rank_duchy` | same | "Tribe of the Latgalians" | **Latgalia** | Chief |
| **ESO** | `rank_duchy` | same | "Tribe of the Estonians" | **Estonia** | Chief |
| **SXM** | `rank_duchy` (already in its block) | same | "Tribe of the Samogitians" | **Samogitia** | Chief |
| **AUK** (option 2) | `rank_duchy` | same | "Tribe of the Aukštaitians" | **Aukštaitija** | Chief |
| **LIT** (option 1, rank_duchy) | `rank_duchy` | **`:1357` LIT-gated** | **"Grand Duchy of Lithuania"** | **Lithuania** | **Grand Duke** |
| **LIT** (option 1, rank_county) | `rank_county` | `:184` + `:2279` | "Minor Tribe of the Lithuanians" | **Lithuania** | Chieftain |

Because the map label is `$NAME$` alone, the `_ADJ` keys are used only in the
long form and in flavour text — but they must still exist, or the long form
renders a raw key.

### F.4 Formables — checked, none consumed, none opened

- **`PRU_f`** (`:1458`) — `potential = { culture = { has_culture_group =
  culture_group:german_group } }`. `pruthenian` is `baltic_group`. Unreachable
  by PRS.
- **`LIV_f`** (`:1508`) — german_group likewise. Unreachable.
- **`LVA_f`** (`:1532`) — baltic_group, `required_locations_fraction = 0.75`
  over five areas totalling **210** ownable. Largest tag here: 48 (LIT option
  1) = **23%**. Unreachable.
- `MCH_f`, `MGO_f`, `MGE_f` — irrelevant to this theater.

---

## G. Diplomacy (`build_diplomacy`)

`MOD/main_menu/setup/start/12_diplomacy.txt` today: **326 `dependency` lines,
20 `scripted_mutual`/`scripted_oneway` lines.**

### G.1 The eleven lines that auto-strip

**Measured: exactly 11 lines in the whole file name any of the eleven retiring
tags.** Ten are dependencies:

```
:44  dependency = { first = TEU second = LIV subject_type = vassal }
:45  dependency = { first = LIV second = RIG subject_type = vassal }
:46  dependency = { first = LIV second = ARR subject_type = vassal }
:47  dependency = { first = LIV second = KUR subject_type = vassal }
:48  dependency = { first = LIV second = BIO subject_type = vassal }
:49  dependency = { first = LIV second = BID subject_type = vassal }
:171 dependency = { first = TEU second = ERM subject_type = vassal }
:172 dependency = { first = TEU second = SMD subject_type = vassal }
:173 dependency = { first = TEU second = PMS subject_type = vassal }
:174 dependency = { first = TEU second = CHL subject_type = vassal }
```
and one is a pact:
```
:175 scripted_mutual = { first = TEU second = BOH type = alliance }
```

All eleven are removed **automatically** by the generic landless sweeps —
`_drop_landless_dep` (`tools/build_setup.py:6505-6514`) and
`_drop_landless_pact` (`:6574-6584`) — the moment the eleven tags enter
`LANDLESS_AFTER`. Both sweeps carry exact-count asserts that must move in the
same commit: **`n_landless_deps` 233 → 243** (`:6565`) and **`n_pacts` 7 → 8**
(`:6587`). Both are self-asserting: leaving either at its old value aborts the
build with the observed count printed. Per CLAUDE.md, observe each failing
first.

### G.2 The two lines the generic sweep provably cannot catch

Both partners stay landed, so both need a **named strip in the Rus batch's
shape** (`tools/build_setup.py:6418-6435`, the `GLH→KIE` / `LIT→POK` precedent
with its `if n_rus != 2` assert):

```
:178 dependency = { first = LIT second = NRK subject_type = vassal }
:179 scripted_mutual  = { first = LIT second = POL type = alliance }
```

**LIT→NRK.** The Rus package stripped seven of LIT's eight vanilla vassals
(vanilla `12_diplomacy.txt:300-307`: DRU, NRK, PNK, POK, SSK, TPS, TUV, VBK,
plus RZH at `:74`) and left NRK. That is the seam the brief names. Novogrudok
is a Kievan/Turov town in 1066; Lithuanian overlordship over Black Ruthenia is
Mindaugas's, 1240s [U]. **Recommendation: strip.** Whether NRK then becomes
independent or KIE's is the Rus package's call (OPEN DECISION 4).

**LIT↔POL.** A Polish-Lithuanian alliance in 1066 inverts the period: Bolesław
II raided Yotvingia and Pomerania, and the first Polish-Lithuanian pact is
Krewo, **1385** [U]. **Recommendation: strip.** (Under option 2 this line dies
free, via the landless-pact sweep — one more small argument for retiring LIT.)

### G.3 The Hanseatic residue — measured, and it is one live item

`hanseatic_member` is a **subject type**, not an IO:
`VAN/in_game/common/subject_types/hanseatic_member.txt:1`, `subject_pays =
hanseatic_member_cost` (`prices/03_diplomacy.txt:48`), `color =
subject_hanseatic_member`. There is **no `hanseatic` IO type** — the whole
`in_game/common/international_organizations/` directory was listed and it is
not there. HSA is an ordinary country tag and an HRE member
(`15_international_organizations.txt:40`).

**In the diplomacy file: vanilla ships 3 `hanseatic_member` dependencies, the
mod ships 1** — `:74 dependency = { first = HSA second = LUB subject_type =
hanseatic_member }`. Two died with Germany II (`tools/build_setup.py:6524`:
"HSA→HAM and HSA→BRM"). **No Baltic tag is a Hanseatic member.** Nothing here
to strip.

**But there is a live Hanseatic anachronism this package cannot fix and must
name.** The mod overrides only six files under `main_menu/setup/start/`
(`04_zz_1066_dynasties.txt`, `05_characters.txt`, `10_countries.txt`,
`12_diplomacy.txt`, `15_international_organizations.txt`, `16_wars.txt`).
`07_cities_and_buildings.txt` is **vanilla's, live**, and it carries
`hanseatic_kontor = { tag = HSA level = 2 location = riga }` (`:1319`) and
`… location = visby }` (`:1318`), alongside Lübeck, Hamburg, Bremen, Goslar and
Rostock. **A Hanseatic kontor stands in a Riga that will not be founded for 135
years, on a location this package hands to LTG.** `06_pops.txt` likewise ships
`culture = hanseatic` pops (`:1377-1378`, `:3182`).

That is a whole-file-override question (`docs/` skill `verify-vanilla-override`),
not a setup-block one, and it is **out of scope**. Flagged loudly so it is not
re-discovered: **OPEN DECISION 6.**

### G.4 Novgorod's Chud sphere — keep, and here is the measurement

NOV holds **22 of `karelia_area`'s 44**, the other 22 unowned; 51 of
`west_novgorod_area`, 49 of `east_novgorod_area`, 29 of `pomorye_area`, 27 of
`totma_area`, 23 of `tver_area`, 7 of `arkhangelsk_area`. Template cultures in
`karelia_area`: `karelian` 26, `sapmi` 12, `novgorodian` 6.

Overlaying that is **KRL, a `type = pop` country holding Karelian pops from 35
locations** (25 of them in `karelia_area`), plus SMI 7, KVE 4, SVO 10, TAV 15.
Novgorod owns the ground; the peoples hold the pops. **That is a 1066-correct
model of the Chud tribute sphere and vanilla built it by accident** — the
Yugra expedition of 1032 and the *pogosty* tribute system are exactly this
shape [U].

**Recommendation: touch nothing.** No `SETUMAA`/`UGAUNIA` tag exists in vanilla
and none is needed: Ugaunia and Sakala are inside ESO (`tartu_province` and
`north_livonia_province`), and Setumaa has no location of its own. The brief's
"1032 Yugra precedent" is upheld by leaving the whole northern sphere alone.

---

## H. Left alone deliberately

| what | why |
|---|---|
| **KRL, SMI, KVE, SVO, TAV — the five Finnic pop-countries** and their 71 theater pops | Vanilla's stateless-peoples model, and it is right for 1066. This package neither adds a member nor removes one, and takes no location from `karelia_area`. |
| **NOV's whole northern sphere** (`karelia_area` 22, `pomorye_area` 29, `arkhangelsk_area` 7, `totma_area` 27) | §G.4 — Novgorod's Chud tribute sphere is already correct. |
| **The 22 unowned locations of `karelia_area` and all 24 of `kola_area`** | Sámi ground, no state, no capital, no attested 1066 ruler. The Pecheneg discipline (`docs/HANDOFF.md:950-955`). They already contribute to the pop-line class and that is the honest price. |
| **The Wendish shore** — `mecklenburg_area` 15, `pomerania_area` 29 (after TEU's 2 move), `brandenburg_area` 41 | §D.4 — HRE surgery, Germany-slice ground, and no Slavic pagan religion exists. `polabian` + `OBO`/`LTC`/`WGR`/`RUG`/`WEN` are banked. |
| **SWE's 32 locations in `finland_area`** | A live anachronism — the Swedish crusades to Finland are 1150+ [U], and 26 of `finland_area`'s 58 are already unowned. A Scandinavian slice's item, named here so it is not re-derived. |
| **`silesia_area` (50, 21 tags), `greater_poland_area` (35), `lesser_poland_area` (40), `central_poland_area` minus Dobrzyń (20), `mazovia_area` minus Podlasie (28)** | The Poland slice's ground. This package touches Polish territory in exactly one direction — *giving* POL 21 locations that the Order took in 1228/1308 — and adjusts nothing else. |
| **The ~30 vanilla characters in the pool tagged to the retiring tags** (TEU 5, LIT 14, LIV/ARR/BID/BIO/KUR/ERM/CHL/PMS/SMD 1 each) | All are 1280-1400 people (e.g. `teu_dietrich_von_altenburg`, `birth_date = 1290.1.1`, `05_characters.txt`). They are a **pool**, not instantiated: the mod carries no `ruler_term`, so nothing references them. Inert. Worth knowing they are there before an event pulls one. |
| **Every religion on every location in the theater** | `baltic_area` is **100% catholic** in `location_templates.txt` and should be pagan on all 56; `prussia_area` is 41 catholic / 3 romuva and should be ~28 romuva. Vanilla already ships `romuva` on 64 and `muinaisusko` on 0. **This is the single largest correction the pop phase inherits from this theater, and the list is exactly: `baltic_area` all 56, `prussia_area`'s 25 non-romuva Prussian-culture locations.** Recorded so the pop phase does not re-derive it. |
| **`prussia_area`'s German location names** (Königsberg, Marienburg/Malbork, Memel, Tilsit, Insterburg, Elbing/Elbląg) | The map's names are the Order's. Renaming 44 locations is a `location_names` override, a different kind of change, and the mod has absorbed this class before (`ningxia` for Xingqing). |
| **`hanseatic_kontor` at `riga` and `visby`, and the `hanseatic` pops** | §G.3 — a live vanilla-file anachronism outside this package's file set. OPEN DECISION 6. |

---

## I. THE MECHANISM QUESTION — one new step is required, and it is small

Unlike the Northern Dynasties package, this one **cannot** run on the existing
machinery. §0.3 is the reason: six locations carry two ownership entries, and
three separate guards read `control` as ownership.

### I.1 Why every alternative fails

| route | outcome |
|---|---|
| put the six in `LOCATION_GRANTS["SXM"]` | `_remove_owned_many` (`:4960-4968`) exits: `ownership occurrences != 1 for ['mazeikiai(2)', …]` |
| put the six in `LOCATION_VACATED["TEU"]` | same assert, via `:5330` |
| `FIELD_FIXES["TEU"]` deleting the `control` block | **runs at `:5464`, after grants `:5258`, vacates `:5330` and the landless guard `:5364`.** Too late for all three. |
| relax `_remove_owned_many` to `>= 1` | changes global semantics; the `!= 1` assert is the thing that caught the Sardinia double-count and must not be loosened for a ten-location edge case |

### I.2 The prescription

A single new step, placed **immediately before the `_landless_claims` snapshot
at `:5238`** — so that the snapshot, the grants, the vacates and the landless
guard all see a clean file:

```python
# tag -> locations listed in that tag's `control = { … }` block ONLY
# (owned by somebody else). Vanilla ships exactly TEN such locations
# game-wide: TEU controls six Samogitian locations LIT owns
# (own_core), and MOR controls four Tlemcen locations TLE owns.
# `control` is the last member of OWN_KEYS (:4936), so all three of
# _remove_owned_many (:4960), the LANDLESS_AFTER guard (:5364) and the
# orphan-capital guard (:5785) read these as holdings. Any slice that
# grants, vacates or retires one of the two occupiers must clear the
# occupation first. Runs BEFORE the _landless_claims snapshot so the
# retiring tag's claims are its REAL holdings, not its conquests.
CONTROL_STRIPS = {
    "TEU": ["palanga", "rietavas", "silale", "skuodas", "taurage",
            "mazeikiai"],
}
```
consumed by a loop that, for each tag, finds its block, finds its
`^[ \t]*control[ \t]*=[ \t]*\{` block, asserts the token list equals the
declared list **exactly** (so a vanilla patch that changes the occupation fails
loudly rather than silently under- or over-stripping), and deletes the whole
`control = { … }` block. Report line: `("occupations cleared", n)`.

**Break-test owed:** remove one location from the list and watch the assert
fire; then leave the step out entirely and watch `LOCATION_GRANTS[SXM]` die
with `occurrences != 1`. A check never seen failing is untested.

### I.3 Two consequences worth stating

1. **The strip is the historically correct edit on its own terms.** A Teutonic
   occupation of Samogitia in 1066 is 250 years early regardless of what else
   this package does. Even a Baltic slice that changed nothing else should ship
   this line.
2. **The Maghreb twin is now on the record.** MOR's four Tlemcen locations sit
   in the same trap, and the Maghreb slice will hit it the day it retires or
   regrants MOR or TLE. `CONTROL_STRIPS` is written as a dict for that reason,
   with one key today.

### I.4 Everything else runs on the existing machinery

- **All 128 (or 176) granted locations are owned in vanilla** — measured, zero
  `=UNOWNED=` across all nine rule sets. `_remove_owned_many` passes on every
  one once the control block is gone.
- **The grants-before-vacates order is irrelevant here** — nothing is vacated.
- **`_list_owner` disjointness (`:5322-5327`) cannot fire** — no vacate list
  covers the Baltic, and the nine rule sets were tested pairwise disjoint by the
  resolver.
- **No Baltic location is named as a string literal anywhere in
  `build_setup.py`** — measured. Zero collision with any existing grant,
  transfer or fix list.
- **The capital-discovery assert (`:4862`) passes for all six new tags** —
  `expl_eastern_europe` carries `baltic_region`.
- **No `CAPITAL_FIXES` entry is required** — every stripped-capital tag reaches
  exactly zero holdings and is exempt at `:5785`. (The `kernave` and
  `fischhausen` choices are historical, not mechanical.)

---

## OPEN DECISIONS

**1. Lithuania: reskin LIT, or retire LIT and land AUK?**
`country_ranks.txt:1355-1362` hard-codes `rank_kingdom_grand_duchy_LIT` on
`tag = LIT` + `country_rank_is_duchy`, 249 lines above `rank_duchy_tribe` —
so a tribal LIT at duchy rank still reads **"Grand Duchy of Lithuania"** under
a **"Grand Duke"**, and only `rank_county` escapes it, at the price of the
string "Minor Tribe of the Lithuanians".
**Recommendation: retire LIT landless with claims over all 70, land `AUK`
(37, capital `kernave`).** It bypasses the tag-gated branch structurally
instead of dodging it, it makes Mindaugas's state a future object exactly as
TEU's and LIV's are, and it frees the LIT↔POL alliance via the generic pact
sweep. Cost: +1 registry block, +2 loc rows, and recipients for LIT's 11 edge
locations (decision 4). The counter-argument is real: option 1 keeps a
recognisable "Lithuania" on the map from turn one, which some players will
expect, and costs 5 `FIELD_FIXES` pairs instead of a new tag.

**2. How many Prussian tags — one, or several?**
The eleven Prussian lands are named by Peter of Dusburg in the 1320s [U] and
none has an attested 1066 ruler. Vanilla gives the whole area two cultures
(`pruthenian` 10, `prussian` 19 — the latter German) and one usable colour.
**Recommendation: TWO — `PRS` (26) and `SUD` (8)** — and the split is justified
by vanilla's own data, not by taste: `sudovian` is a separate shipped culture
(`baltic.txt:126`) on 14 locations across four areas, and Sudovia/Yotvingia was
the one Prussian land that acted politically apart. Eleven tags for 34
locations would be Pecheneg-discipline failure in the other direction: naming
polities the sources cannot name.

**3. How many tags in Livonia and Estonia — four, or fewer?**
The draft proposes `KUO` 8, `ZEM` 7, `LTG` 17, `ESO` 24. Every one of the four
corresponds to a distinct people Henry of Livonia distinguishes [U], and three
of them map onto distinct vanilla cultures (`curonian`, `latvian`, `estonian`,
`liv`). **Recommendation: keep four.** The alternative worth naming: split ESO
into Sakala (6) / Ugaunia (4) / the northern maakonnad (8) / Saaremaa-Läänemaa
(6), all four tags free (`SAK` is taken — a pop country — but `UGA`, `OSE`,
`VIR`, `HAR`, `REV`, `LAA` are free). That is more truthful about Estonian
statelessness and produces four 4-8 location tags that will be eaten by the
first neighbour. Against merging: ZEM+LTG into one 24-location "Latvia" would
paper over the Semigallian/Latgalian distinction the whole 13th century turns
on.

**4. LIT's 11 edge locations under option 2 (Podlasie 5, Black Ruthenia 6).**
`drohiczyn bielsk_podlaski mielnik sokolow suraz` are `mazovian`/catholic;
`grodno sokolka grodek bershty` are sudovian/aukstaitian/romuva; `masty
nyasvizh` are `polesian_culture`/orthodox.
**Recommendation: RAW takes the five Podlasie, SUD takes the four forest
locations, NRK takes the two Polesian ones.** But this is the Rus package's and
the Poland slice's seam, and the Rus package deliberately left NRK holding 11
in `black_ruthenia_area`. If the main session prefers, all 11 can go to KIE and
NRK by a Rus-side follow-up instead, leaving option 2's grant list at 165.

**5. `mergentheim` — UFF or MAI?**
The Order's post-1525 seat, 1 location in `tauberfranken_province`, 1,000 km
from Prussia. **Recommendation: UFF (Hohenlohe)**, which holds the two other
Hohenlohe locations in the same province and was Mergentheim's lord before the
1219 donation [U]. The inherited anachronism (the Hohenlohe family is c. 1153
[U]) is the Germany slice's, flagged not fixed. `MAI` (Mainz, holds
`tauberbischofsheim`) is the alternative if the main session prefers a
1066-attested lord.

**6. The Hanseatic kontors at `riga` and `visby` — accept, or override
`07_cities_and_buildings.txt`?**
Vanilla's un-overridden file plants a level-2 HSA kontor on a location this
package hands to LTG, 135 years before Riga is founded
(`VAN/main_menu/setup/start/07_cities_and_buildings.txt:1317-1323`), and
`06_pops.txt:1377-1378` ships `culture = hanseatic` pops.
**Recommendation: accept for now and BANK it.** Overriding
`07_cities_and_buildings.txt` is a whole-file freeze of a 1,300+-line vanilla
database — exactly the class the `verify-vanilla-override` skill exists to slow
down — and the right time to do it is the buildings/pops phase, once, for the
whole map. Named here so the next session finds it rather than re-discovers it.

**7. Explicit `country_rank = rank_duchy` on the new tribes, or omit it?**
**Measured: all 55 landed `type = tribe` countries in the built file carry no
`country_rank` line**; the mod's own CUM carries `rank_duchy`.
**Recommendation: declare `rank_duchy` explicitly**, as CUM does. It makes the
§F render deterministic and stops a 6-location tag drifting into
`rank_county_tribe`'s "Minor Tribe of…". The counter: vanilla's silence is
itself a measurement, and letting the engine size them is one fewer thing to be
wrong about.

**8. `starting_technology_level` — 0, 2 or 3?**
KRL uses 0, `gaelic_tribe` ships 2, CUM uses 3. **Recommendation: 2** — the
Irish tribal precedent, and it keeps the Baltic pagans behind Poland and
Denmark without making them Siberian. A slider, revisable by one
`FIELD_FIXES` line; flagged so the choice is deliberate rather than copied.

**9. `CONTROL_STRIPS` — build it, or find another way?**
§I proves the three existing guards all read `control` and that `FIELD_FIXES`
runs too late. **Recommendation: build it, minimal, one key, exact-count
asserted, placed before `:5238`.** The alternative — hand-editing the six
tokens out of the vanilla input — is not available: the build reads pristine
vanilla every run (`:6896`).

**10. `ESO`'s religion: `muinaisusko`, or invent an Estonian one?**
`muinaisusko` is shipped (`folk_european.txt:160`), placed on zero locations,
and is what vanilla itself gives KRL. The Estonians' Taara/Uku cult is not
Finnish Muinaisusko in any strict sense [D].
**Recommendation: `muinaisusko`.** It is the al-Andalus/BLH/`kharchin_culture`
law again: use the shipped best-available proxy, bank the invented one for the
pop phase where it would actually be visible.

**11. Does DAN really lose all seven Estonian locations?**
Danish Estonia is 1219 [U] and there is no reading in which Svend Estridsen
holds Reval in 1066. **Recommendation: yes, all seven to ESO.** Recorded as a
decision only because it touches a major power's borders and the brief asked
for Scandinavian edges to be justified individually.

**12. `map_PRU` for PRS — reuse, or author `map_pruthenian`?**
`map_PRU` is `hsv360 { 229 80 30 }` (`02_map.txt:239`), used by no country and
by `prussian`'s culture, and it gives the pagan Prussians the blue the Kingdom
of Prussia later wears. **Recommendation: reuse** — zero new colour rows and a
deliberate continuity. If it reads as Poland's neighbour rather than its enemy
in game, `map_pruthenian` does not exist and must be authored.

---

## Implementation checklist

Ordered so each step can be verified before the next.

1. **`CONTROL_STRIPS`** (§I.2) — the new step and its exact-count assert,
   placed before `tools/build_setup.py:5238`. **Ship this first and alone**,
   observe the build still passing, then observe it failing with a wrong list.
   Everything below depends on it.
2. **Registry** — six blocks appended to
   `in_game/setup/countries/zz_1066_new_countries.txt` (§A.3). Count 58 → 64
   (65 with AUK).
3. **Colours** — **none.** Verify by re-running the key/RGB check in §A.4
   before assuming it.
4. **Localisation** — 12 rows (14 with AUK) in
   `main_menu/localization/english/1066_norman_conquest_l_english.yml`, one
   physical line each, UTF-8 **with** BOM.
5. **`_GENERATOR_OK`** — add the six (seven) tags at `tools/verify_mod.py:925`
   with a tier-4 comment; the check at `:962-968` fails otherwise.
6. **`NEW_COUNTRIES`** — six (seven) blocks (§B). Read `eurasian_tribe.txt`
   again before shipping and restate anything it omits.
7. **`_BALTIC_RULES` + resolution loop** — modelled on the Central Asia loop
   (`tools/build_setup.py:5037`): resolve, assert the exact count, assign
   into `LOCATION_GRANTS`, then assert each capital is in its own resolved list.
8. **`BALTIC_LANDLESS`** into `LANDLESS_AFTER` (`:2404`) — 11 tags, or 12 under
   option 2.
9. **`LOCATION_VACATED_EXPECT`** — **verify nothing moves** (§E.3). This is a
   negative claim and the build will not tell you if it is wrong in the safe
   direction; re-run the pool check.
10. **`n_landless_deps` 233 → 243** (`:6565`) and **`n_pacts` 7 → 8** (`:6587`)
    — **in the same commit**, and per CLAUDE.md **observe each failing first**.
11. **Named strips** — LIT→NRK and LIT↔POL in the Rus batch's shape
    (`:6418-6435`), with an `if n != 2` assert (§G.2). Under option 2 the
    LIT↔POL line dies free and the assert is `!= 1`.
12. **LIT** — either the 5-pair `FIELD_FIXES` (option 1, §C.3) **including the
    mandatory `rank_county`**, or `LANDLESS_AFTER` + the `AUK` block + the
    11-location edge grants (option 2).
13. **Harness** — raise `min_count` on the registry, dynasty and character
    checks by what this slice adds, per CLAUDE.md's raise-as-content-lands rule.
    Note this slice adds **zero** characters and **zero** dynasties: those two
    checks stay put, which is itself worth a comment so the next reader does not
    think it was forgotten.

**Break-tests owed** (a check never seen failing is untested):
(a) a bogus location in `_BALTIC_RULES` must abort;
(b) an off-by-one `expected` must abort with the resolved count printed;
(c) `CONTROL_STRIPS` removed entirely must abort at `LOCATION_GRANTS[SXM]` with
`occurrences != 1` — **observe this one specifically**, it is the finding this
package rests on;
(d) `CONTROL_STRIPS` with five of the six locations must abort on its own
exact-count assert;
(e) removing one tag from `BALTIC_LANDLESS` must produce a landless tag with no
claims, caught by the verifier at `:5401` before the game sees it;
(f) `n_landless_deps` and `n_pacts` left at their old values must both abort.

## Expected constant moves, collected

| constant | file:line | from | to (option 1) | to (option 2) |
|---|---|---|---|---|
| registry blocks | `zz_1066_new_countries.txt` | 58 | **64** | **65** |
| `NEW_COUNTRIES` count | `build_setup.py:466` | current | **+6** | **+7** |
| `LANDLESS_AFTER` | `:2404` | current | **+11** | **+12** |
| `n_landless_deps` | `:6565` | 233 | **243** | **243** |
| `n_pacts` | `:6587` | 7 | **8** | **9** |
| named dependency strips | new | — | **2** | **1** |
| `LOCATION_VACATED_EXPECT[*]` | `:1237` `:1364` `:1390` `:1405` | — | **unchanged** | **unchanged** |
| `CONTROL_STRIPS` | new | — | **1 tag / 6 locations** | same |
| locations granted | build report | current | **+128** | **+176** |
| locations vacated | build report | current | **+0** | **+0** |
| new characters / dynasties | — | — | **0 / 0** | **0 / 0** |

---

## Verification statements

Per CLAUDE.md's say-what-you-verified rule.

- **Verified — the resolver.** An independent reimplementation of
  `_parse_defs` (`tools/build_setup.py:711`), `_ownable_set` (`:736`),
  `find_block_end` (`:4738`) and the `OWN_KEYS`/`COUNTRY_RE` reader
  (`:4933`/`:4791`) reproduced **eleven of eleven** shipped
  `LOCATION_VACATED_EXPECT` constants exactly: KHD 16, OGE 18, CHG 21,
  WAL 44, IAS 11, BIA 10, BLD 9, SRC 4, HTN 3, HSC 3, SSI 3. That is the
  known positive every count in this document rests on.
- **Verified — the template parser**, by asserting `cult['dadu'] ==
  'yan_culture'`; `location_templates.txt` blocks are single-line and a
  line-anchored culture regex returns zero on all 20,922 entries.
- **Verified — the tag scanner**, by feeding it TEU, LIV, SXM, KRL (all four
  returned TAKEN with their `baltics.txt` line) and PRU (TAKEN on 87 word
  hits with an empty registry — the formable-only class, §A.5).
- **Verified — six locations carry two ownership entries.** `palanga`,
  `rietavas`, `silale`, `skuodas`, `taurage`, `mazeikiai` appear in LIT's
  `own_core` **and** TEU's `control`. Game-wide there are exactly ten such
  locations; the other four are MOR/TLE in `algiers_area`. `_remove_owned_many`
  (`:4960-4968`) exits on `!= 1`; the `LANDLESS_AFTER` guard (`:5364-5382`)
  and the orphan-capital guard (`:5764-5793`) both loop `OWN_KEYS`, which ends
  with `"control"` (`:4936`); `FIELD_FIXES` runs at `:5464`, after all three.
- **Verified — the Baltic is untouched ground.** Zero references to
  `baltic_region`/`baltic_area`/`prussia_area`/`lithuania_area`/
  `samogitia_area`/`mazovia_area` in `build_setup.py`, and zero string
  literals naming any of the theater's 159 locations. MOD ownership across all
  four areas is byte-identical to vanilla.
- **Verified — no vacate pool touches the Baltic**, hence zero
  `LOCATION_VACATED_EXPECT` moves. The four pools are enumerated in §E.3.
- **Verified — `romuva`** (`VAN/in_game/common/religions/folk_european.txt:128`,
  `group = folk_european_group`, `tags = { folk_european_gfx pagan_gfx }`, loc
  `romuva: "Romuva"`) and **`muinaisusko`** (`:160`, `color = map_tavastian`,
  loc `muinaisusko: "Muinaisusko"`). `muinaisusko` is placed on **zero**
  locations; `romuva` on **64**.
- **Verified — `pruthenian` ≠ `prussian`.** `pruthenian`
  `cultures/baltic.txt:146` (`baltic_group`); `prussian`
  `cultures/german.txt:305` (`language = low_german_dialect`,
  `color = map_PRU`, `north_german_gfx`). TEU's registry
  `culture_definition = prussian` is the German one.
- **Verified — `polabian` exists and is placed nowhere**,
  `cultures/west_slavic.txt:108`, `language = polabian_dialect`,
  `color = map_polabian` (`02_map.txt:278`).
- **Verified — `baltic_language` declares no `family`.** `grep -c family` over
  `VAN/in_game/common/languages/00_baltic.txt` returns **0**; its dialects are
  `latvian_dialect`, `lithuanian_dialect`, `western_baltic_dialect`.
- **Verified — the tribal name chain.** `country_name_construction.txt` has no
  tribe branch; `:184-186` is the declared `fallback = yes`;
  `country_name_construction_prefix_rank_of_name: "$PREFIX$ $RANK$ of
  $ARTICLE$ $NAME$"` (`government_names_l_english.yml:11`) and
  **`…_map: "$NAME$"` (`:12`)**. `rank_duchy_tribe` at `country_ranks.txt:1606`
  → `"Tribe"` / ruler `"Chief"` (`:790-791`), no prefix key;
  `rank_county_tribe` at `:2279` → `"Tribe"` / prefix `"Minor"` / ruler
  `"Chieftain"` (`:1018-1021`); `country_rank_people` at **`:5`** requires
  `country_type = pop`.
- **Verified — `rank_kingdom_grand_duchy_LIT`**, `country_ranks.txt:1355-1362`,
  trigger `tag = LIT` + `country_rank_is_duchy = yes`, loc `"Grand Duchy"` /
  `"Grand Duke"` (`government_names_l_english.yml:634-636`) — **249 lines above
  `rank_duchy_tribe`**, and `country_rank_is_duchy` resolves through
  `scripted_triggers/country_triggers.txt:44-46`.
- **Verified — TEU's and LIV's NAME keys are dead.** Both hit
  `country_name_construction.txt:117-155` via `has_reform =
  government_reform:military_order_reform` (`:139-147`, `military_order_reform`
  defined at `government_reforms/theocracy.txt:1`, supplied by
  `catholic_military_order.txt`) at `rank_duchy`; all four
  `rank_duchy_order*` branches (`country_ranks.txt:1454`, `:1469`, `:1480`,
  `:1494`) resolve `"Order"`; `$ADJ$` is `TEU_ADJ: "Teutonic"` /
  `LIV_ADJ: "Livonian"` (`country_names_l_english.yml:1980`, `:72`).
- **Verified — 448 `type = pop` countries in vanilla and 448 in the build**,
  none touched by the mod; KRL is one, with `add_pops_from_locations` covering
  35 theater locations.
- **Verified — the eleven diplomacy lines.** Exactly 11 lines in
  `MOD/main_menu/setup/start/12_diplomacy.txt` name any of the eleven retiring
  tags: 10 dependencies (`:44-49`, `:171-174`) and one `scripted_mutual`
  (`:175`). File totals: 326 dependencies, 20 pacts. LIT→NRK (`:178`) and
  LIT↔POL (`:179`) name only landed tags. Vanilla ships nine LIT vassals
  (`:74`, `:300-307`); the Rus package left NRK.
- **Verified — `hanseatic_member` is a subject type**,
  `VAN/in_game/common/subject_types/hanseatic_member.txt:1`; there is **no
  `hanseatic` IO type** in `in_game/common/international_organizations/`. The
  mod ships one `hanseatic_member` dependency (`:74`, HSA→LUB) against
  vanilla's three. **`hanseatic_kontor` at `riga` and `visby` is LIVE** —
  `VAN/main_menu/setup/start/07_cities_and_buildings.txt:1317-1323`, a file the
  mod does not override (its `setup/start` set is six files).
- **Verified — TEU and LIV are NOT HRE members**; `mecklenburg_area` and the
  six Pomeranian provinces ARE in the HRE instance
  (`MOD/main_menu/setup/start/15_international_organizations.txt:38-58`), as
  are MKL, GSW, SWR, WRN, WOL, STE, KMM, NWG, SOR, BRA. The `catholic_church`
  instance carries `members = { PAP }` only (`:144-147`) — no bishopric is in
  it.
- **Verified — no Slavic pagan religion exists.** Every file in
  `VAN/in_game/common/religions/` scanned for `slav|rodnov|wend|polab`: the
  only hits are `church_slavonic_language` in `christian.txt` and
  `map_wendat` in `folk_north_america.txt`.
- **Verified — the formables.** `PRU_f` (`00_formable_countries.txt:1458`) and
  `LIV_f` (`:1508`) gate on `german_group`; `LVA_f` (`:1532`) gates on
  `baltic_group` at `required_locations_fraction = 0.75` over five areas
  totalling 210 ownable — the largest tag this package creates holds 23%.
- **Verified — the colour keys.** All ten candidate `map_*` keys exist in
  `02_map.txt` at the lines given in §A.4; **none is used by any country**
  except `map_osel`→BIO, `map_samogitian`→SXM and `map_karelian`→KRL, and **no
  other country colour resolves to the same RGB triple** (checked across every
  `color = <key>` in vanilla's and the mod's `setup/countries`).
- **Verified — every capital.** All six new capitals resolve inside their own
  tag's grant list; `expl_eastern_europe` carries `baltic_region` (read in
  full), so the `:4862` capital-discovery assert passes; every retiring
  tag reaches zero holdings and is exempt from the orphan-capital guard by
  `:5785`'s `if held and …`.
- **Verified — the character pool.** ~30 vanilla characters carry `tag =` one
  of the eleven (TEU 5, LIT 14, one each for the rest), all born 1280-1400
  (e.g. `teu_dietrich_von_altenburg`, `birth_date = 1290.1.1`). No
  `ruler_term` references any of them.
- **NOT verified, and stated as such:** every foundation date, polity extent
  and ethnographic claim carrying `[U]` or `[D]` — the Order's and the
  bishoprics' foundation years, Gottschalk's murder date and the Obodrite
  reaction, the Curonian and Oeselian sea-kings, the eleven Prussian lands and
  Peter of Dusburg's retrojection, Grobiņa/Seeburg, Koknese/Kukenois and
  Jersika's tributary status to Polotsk, Yaroslav's 1030 Yuryev, Kernavė's
  occupation sequence, the Raikküla thing, Baltic pagan polygyny, Danish
  Estonia's 1219 start, Mergentheim's Hohenlohe lordship, the 1385 Krewo
  union, and the conversion dates in §0.2. Those rest on the agent's own
  history and need a source before they enter a comment, let alone setup data.
- **NOT checked, and owed before implementation:** whether
  `low_german_dialect` satisfies `culture.language = language:german_language`
  in `country_ranks.txt:1480`/`:1454` (it decides only whether TEU's *current*
  ruler title reads "Hochmeister" or "Grandmaster", and both tags are being
  retired); the `government_type` reached by `eurasian_tribe` when a
  `country_rank` line is present (assumed `tribe`, as the template states, but
  the 55 landed vanilla tribes all omit the rank line); and whether
  `country_exists = c:TEU` is true for a landless-with-claims TEU — which
  decides whether `religion_triggers.txt:301-309` and `laws/01_common.txt:1571`
  take their `trigger_if` branch. None of the three can break the build; all
  three are worth a look at the first launch.
