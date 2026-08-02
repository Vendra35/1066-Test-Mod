> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 39 (commit 2c9a76d) —
> NOT yet game-tested.** Research record, not the state. **The second
> consecutive zero-error package review** (22/22 probes; both donor tables
> reproduced per the delta-guard law). Decisions, taken by the main session
> under the user's direct-implement authorization: 1a (VYT retired + 19
> vacated), 2a (PRM reshaped to eurasian_tribe, the SXM shape), 3 (GLH's
> 7 vacated — EXPECT 291→298 observed failing first), 4 (the ten Yugra
> ties stripped by name; OWED CHECK 2's two-level chain thereby leaves the
> build unmeasured — stays open for a future case), 5a (GLM/GRS/NZH left
> for the Volga seam, the internal inconsistency with VYT recorded in the
> build comment, not hidden), 6 (tech 3 kept). Constants landed exactly as
> forecast: vacated 625, deps/pacts/ghosts 280/9/156 unchanged, parliament
> 1365 observed. Break-tests: all eight fired exactly — including (h),
> the delta-guard law's own demonstration reproduced on GLH. §E.4's
> refutation of the decoder's one-line-per-pop vacate model is now
> recorded in EU5-ERROR-DECODER.md with OWED CHECK 3; expect the class
> near ~1,000 lines (1,895 pops on 625 vacated locations × the measured
> ≈0.55 ratio) at the next launch, NOT 504.

# PERM AND VYATKA 1066 — the stateless north is already shipped; two Russian shells deny it (DRAFT)

**Research agent model ID: `claude-opus-5`.**

**DRAFT — pending main-session review. Nothing here has been written into any
mod file.** Produced by an Opus research agent, 2026-08-02, against the working
tree at HEAD `e027550` (38 items landed; constants read from the code, not from
prose: registry 74 blocks, country blocks 2411, thrones 179, landless-dep strips
280, pacts 9, IO ghosts 156, vacated 599, parliament min 1366, loc rows 375, CoA
125). Every mechanical claim carries a `file:line`. Historical claims that no
file can settle are flagged `[U]` (unverified — the agent's own history, no
source in the repo) or `[D]` (sources genuinely differ), never asserted
silently. §VERIFICATION collects them.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, 491,179 bytes, present)
`MOD = .../1066 Test Mod`

**Method — the SEA lesson and the Tibet method, applied unchanged.** No reader
was reimplemented. This package `import`s `tools/build_setup.py` (its `__main__`
guard is at `:8141`) and calls its own parsers: `_parse_defs` (`:748`),
`_ownable_set` (`:772`), `_defs` (`:809`), `_resolve_ruleset` (`:815`),
`find_block_end` (`:5509`) and `COUNTRY_RE` (`:5562`). Ownership is read with
the **full ten-member `OWN_KEYS` tuple copied verbatim from
`build_setup.py:5704-5707`** — `own_control_core, own_control_integrated,
own_control_conquered, own_control_colony, own_core, own_conquered,
own_integrated, own_colony, control_core, control`. Everything reads
`encoding='utf-8-sig'`; comments are masked length-preservingly before
tokenising. Scripts live in the session scratchpad (`perm.py`, `tree*.py`,
`cov.py`, `detail.py`, `rules.py`, `tagscan2.py`); nothing was written into the
repo but this file.

**Proven on known positives BEFORE any new ground, including an
`own_control_integrated` case.**

| probe | expected (source) | measured |
|---|---|---|
| ownable locations | 20,922 (`TIBET-PACKAGE.md` §VERIFICATION) | **20,922** |
| vanilla country blocks | 2,337 | **2,337** |
| mod country blocks | 2,411 (`HANDOFF.md:1905`) | **2,411** |
| `samogitia_area` ownable | 16 (`BALTIC-PACKAGE.md:66`) | **16** |
| `courland_province` ownable | 8 (`BALTIC-PACKAGE.md:863`) | **8** |
| **VTN in vanilla** | **32** (`SEA-PACKAGE.md` STATUS band — the `own_control_integrated` proof) | **32** |
| **PLB** | **40** | **40** |
| **BTU** | **6, not 1** | **6** |
| **MGD in vanilla** | **5, not 1** | **5** |
| MUA in vanilla | 15 | **15** |
| **TIB in vanilla** | **59** (`TIBET-PACKAGE.md` §0.7) | **59** |
| `06_pops.txt` blocks / `define_pop` | 28,559 / 50,227 lowercase-only, 28,570 / 50,255 with the 11 uppercase keys (`TIBET-PACKAGE.md` §VERIFICATION) | **28,559 / 50,227** and **28,570 / 50,255** — both reproduced exactly |
| locations vacated by the build | **599** (`HANDOFF.md:1907`) | **599**, and the ledger closes: vanilla-unowned 7,334 + 599 vacated − 9 that gained an owner (all SNH's, `UNOWNED_GRANTS`) = **7,924 = the mod's measured unowned total** |

**Scope.** `ural_region` (`definitions.txt`, `eastern_europe` sub-continent) —
nine areas, **194 ownable locations** — plus the northern lobe of
`russian_region` (`arkhangelsk_area` 25, `pomorye_area` 30, `totma_area` 29,
`nizhny_novgorod_area` 31 = 115), and `west_siberia_region` (330) measured and
almost entirely left. **Zero double-ownership anywhere in `ural_region`**
(measured; `CONTROL_STRIPS`, `build_setup.py:1705`, needs no key here).

---

## 0. Ground truth — eight findings, and seven of them say "leave it alone"

### 0.1 THE HEADLINE: vanilla already ships the stateless north, in full, with identities — and the mod inherits it unchanged

`VAN/in_game/setup/countries/siberia.txt` is a registry file of **nineteen
identity blocks**, and **every one of them holds ZERO locations in vanilla and
ZERO in the current mod build** (measured with the ten-key reader, both trees):

| tag | `siberia.txt` | NAME | `culture_definition` | `religion_definition` |
|---|---|---|---|---|
| **OBD** | `:1` | Obdor | `nenets_culture` | `samoyedic_paganism` |
| **PLY** | `:9` | Pelym | `mansi_culture` | `obian_paganism` |
| **BAK** | `:17` | Bardak | `khanty_culture` | `obian_paganism` |
| **KND** | `:25` | Konda | `khanty_culture` | `obian_paganism` |
| **BGJ** | `:32` | Belogorye | `khanty_culture` | `obian_paganism` |
| **KOD** | `:39` | Koda | `khanty_culture` | `obian_paganism` |
| **SVA** | `:46` | Sosva | `khanty_culture` | `obian_paganism` |
| **KZY** | `:53` | Kazym | `khanty_culture` | `obian_paganism` |
| **LYA** | `:60` | Lyapin | `nenets_culture` | `samoyedic_paganism` |
| **TBY** | `:67` | Tabary | `mansi_culture` | `obian_paganism` |
| **SLK** | `:74` | Selkup | `selkup_culture` | `samoyedic_paganism` |
| BRT HGO ALT KMG SAK EVE YKG KYK | `:82`-`:138` | Buryatia … Koryak | Turkic/Mongol/Tungusic | tengri / shamanisms |

Each has a `10_countries` block, and each block's first line is **`type = pop`**
(`MOD/main_menu/setup/start/10_countries.txt:3225` OBD, `:3257` PLY, `:3286`
BAK, `:3314` KND, `:3342` BGJ, `:3370` KOD, `:3398` SVA, `:3426` KZY, `:3454`
LYA, `:3482` TBY, `:3510` SLK, `:3538` BRT, `:3564` HGO, `:3592` KMG, `:3616`
SAK, `:3677` ALT, `:44934` EVE, `:44951` YKG, `:44971` KYK). The shape (OBD,
`:3225-3254`) is: `type = pop`, an `add_pops_from_locations` list, a
`discovered_regions` block, `starting_technology_level = 0`,
`include = "eurasian_tribe"`, `government = { type = tribe heir_selection =
tribal_oldest_male ruler = random }`, `capital = obdorsk` — a capital on a
location it does not own, the first-class vanilla shape `KNOWLEDGE.md` records
("`tag = X … location = L` where X does not own L is FIRST-CLASS vanilla").

The consequence, measured across the whole map:

| culture | locations | `define_pop` | owners in the CURRENT mod build |
|---|---|---|---|
| `khanty_culture` | 41 | 111 | **41 unowned** |
| `mansi_culture` | 29 | 56 | **29 unowned** |
| `nenets_culture` | 26 | 37 | **26 unowned** |
| `selkup_culture` | 20 | 30 | **20 unowned** |
| `vepsian` | 3 | 3 | **3 unowned** |

**116 Ob-Ugric and Samoyed locations, 234 pops, one hundred per cent unowned,
each with a named tribal identity that paints its pops and nothing else.** This
is the Changthang precedent at eight times the scale, and it is not something
this project has to build — vanilla built it and the build inherits it
untouched. **The Yugra half of the brief is already done.**

The same model reaches back across the Urals. Three more `type = pop` countries
cover the European north:

| tag | NAME | pop-locations | where | any of them owned? |
|---|---|---|---|---|
| **BJA** | **Bjarmia** | 16 | `arkhangelsk_area` 13, `ust_sysola_area` 3 | **none — all 16 unowned** |
| **BSH** | Bashkir | 24 | `desht_kipchak_area` 12, `bashkiria_area` 8, `kulykol_area` 3, `chimgi_tura_area` 1 | **none — all 24 unowned** |
| KRL | Karelia | 40 | `karelia_area` 25, `finland_area` 9, `pomorye_area` 5, `west_novgorod_area` 1 | 28 (NOV 21, SWE 7) — the Baltic/Sweden seam, not mine |

**Bjarmia exists, it is stateless, and its sixteen locations are exactly the
Mezen–Pinega–Vashka ground the brief asks about.** Nothing to create.

### 0.2 The second finding: exactly TWO things in this theater are wrong, and both are Russian shells over Finno-Ugric ground

Everything else in the theater is either already stateless or belongs to another
slice's declared seam. The two:

**(a) VYT "Vyatka" — 19 locations — is a VECHE REPUBLIC.**
`MOD/main_menu/setup/start/10_countries.txt:3108-3190` (83 lines): `type =
republic`, `heir_selection = veche_selection`, `reforms = { veche_republic }`,
`parliament_type = estate_parliament`, `dynasty = rurikovich_dynasty`, thirteen
sliders, thirteen privileges (`the_ryad_privilege`, `kormlenije`,
`trade_monopolies` …) and eleven laws including `administrative_system =
pyatina_policy`, `republican_foundation_law = political_dynasties_policy` and
`legal_code_law = russkaya_pravda_policy`. Registry: `VAN/in_game/setup/
countries/russia.txt:316`, `culture_definition = novgorodian`,
`religion_definition = orthodox`.

**This is the defect the Rus slice already fixed once, on the tag next door, and
never came back for.** `build_setup.py:3106-3113` is `FIELD_FIXES["NOV"]` —
"the 1136 veche republic un-anachronized (the Rus package's second LIVE defect,
user-approved 2026-08-01)" — six surgeries that turned Novgorod into a
monarchy. **VYT carries the identical apparatus, byte for byte in places
(`pyatina_policy`, `the_ryad_privilege`, the same slider block), and was not
touched.** Diffed live: NOV's built block is now `type = monarchy` /
`partition_inheritance` under `nov_mstislav_izyaslavich_rurikovich`
(`:1754`ff); VYT's is untouched vanilla.

Fourteen of VYT's nineteen locations are `komi`/`udmurt` culture on
`shamanism`; only five are `muscovite`/`orthodox` (measured per location, §0.7).
So the tag is a Russian republic whose own ground is three-quarters
Finno-Ugric pagan — vanilla's own map data arguing against vanilla's own tag.

**(b) PRM "Perm" — 64 locations — is a RURIKID PRINCIPALITY.**
`MOD/…/10_countries.txt:3192-3223`: `type = monarchy`, `heir_selection =
cognatic_primogeniture`, **`dynasty = rurikovich_dynasty`**, `capital =
cherdyn`, `include = "limited_russian_principality"`, `tolerated_cultures = {
udmurt }`. The template (`VAN/main_menu/setup/templates/
limited_russian_principality.txt`, read in full) supplies `parliament_type =
estate_parliament`, thirteen estate privileges (`noble_serfdom_rights`,
`clergy_land_rights`, `market_fairs`, `formal_guilds`, `building_roads_rights`
…) and eleven laws (`medieval_levy_law = noble_levies`, `administrative_system
= feudal_administration`, `mining_law = nobles_mining_law`, `coin_laws =
gold_and_silver_coins`). It declares **no `type =` line at all** — PRM's own
block is the only source of `monarchy`.

And the registry disagrees with the block: `VAN/in_game/setup/countries/
russia.txt:309` gives PRM `culture_definition = komi` and `religion_definition
= komi_paganism`. **Paradox's identity for Perm is a Komi pagan people; its
start block is a Russian feudal principality with a Rurikid house.** All 64 of
its locations are `shamanism` and 49 of 64 are `udmurt` culture (§0.7).

### 0.3 The third finding: the theater has ZERO seatable rulers, and it is the emptiest yet

Every `tag =` line in `MOD/main_menu/setup/start/05_characters.txt` and in
vanilla's was scanned for the theater's tags. **Five characters exist, all five
are GLM's, and the EARLIEST birth date is 1230.1.1** —
`glm_konstantin_yaroslavich_rurikovich` (`MOD:92055`, `VAN:92273`), then
`glm_davyd_konstantinovich` 1248, `glm_vasily_konstantinovich` 1250,
`glm_fyodor_davydovich`, `glm_ivan_fyodorovich`. **PRM, VYT, NZH and GRS name
no character at all, in either tree.**

That is emptier than Tibet, whose earliest was 1261 (`TIBET-PACKAGE.md` §0.3).
No dynasty is homed anywhere in the theater either (`04_dynasties.txt` probed
for `home = cherdyn|vyatka|perm|galich|gorodets|nizhny_novgorod|ust_sysola` —
zero hits).

One thing DOES exist and should be recorded for a future pass: **`permic_language`
carries a full name pool** (`VAN/in_game/common/languages/00_ural.txt:83-102`
— `male_names = { Istopka Mikvor Mitrok name_michael Mitruk Oloksan Orti Yogush
Yovgin Korak Matvuy }`, eleven female names, `patronym_suffix_komi`), and
`ugrian_language` (`:104`) another. So a Komi ruler is *renderable*; there is
simply no attested 1066 Komi chief to render [U — no source in this repo, and
none known to the agent]. **This package seats nobody.**

### 0.4 The fourth finding: the rank/name lattice has no trap here — and exactly one live wrong render, which belongs to VYT

`VAN/in_game/common/customizable_localization/country_name_construction.txt` is
188 lines, first-match, read in full. Only two branches are government-gated:
`:99-104` (`government_type = steppe_horde`) and the empire/`type = pop`
adjective branch at `:116-157`. **Every countable branch was checked against
this theater and none reaches it**; everything lands on the fallback at
`:183-186`, `country_name_construction_prefix_rank_of_name`, whose loc is
`"$PREFIX$ $RANK$ of $ARTICLE$ $NAME$"` and — the line that matters —
**`…_map: "$NAME$"`** (`VAN/main_menu/localization/english/
government_names_l_english.yml:11-12`).

**THE LAW for this theater: every map label is the NAME key verbatim** — "Perm",
"Vyatka", "Galich-Mersky", "Nizhny Novgorod", "Gorodets". No adjective trap, no
horde trap, no tag-gated trap. And `country_name_construction.txt` contains
**zero tribe branches** (grep: `tribe` matches nowhere in the file), so a
tribal Perm still renders "Perm" — the same clearance the British and Cuman
slices measured.

`country_ranks.txt` (2,742 lines, first-match) was walked at duchy rank for the
branches these tags can reach:

| branch | line | trigger | fires? |
|---|---|---|---|
| `rank_duchy_republic_novgorod` | `:1413` | duchy + **`tag = NOV`** + republic | no (tag-gated to NOV) |
| **`rank_duchy_republic`** | **`:1423`** | duchy + `government_type = republic` | **YES — this is VYT today** |
| `rank_duchy_tribe` | `:1606` | duchy + tribe | fires if PRM becomes a tribe |
| `rank_duchy_russian_prince` | `:1973` | duchy + `culture.language = language:east_slavic_language` | GLM/GRS/NZH (`muscovite`); **not PRM** (`komi` → `permic_language`, `VAN/in_game/common/cultures/permic.txt:1-2`) |
| `rank_duchy` (default) | `:2006` | duchy | PRM today |

Loc (`government_names_l_english.yml`):

| key | line | renders |
|---|---|---|
| **`rank_duchy_republic`** | **`:693-696`** | RANK **"Republic"**, ruler **"Consul"**, ADJ "republican" |
| `rank_duchy_russian_prince` | `:871-873` | "Principality" / "Prince" |
| `rank_duchy_tribe` | `:790-792` | "Tribe" / "Chief" |
| `rank_county_tribe` | `:1018-1022` | "Tribe", prefix "Minor" / "Chieftain" |
| `rank_kingdom_tribe` | `:482-485` | "Tribal Kingdom" / "King" |
| `rank_duchy` | `:641-644` | "Duchy" / "Duke" |

**So VYT renders today as "Republic of Vyatka" under a "Consul".** That is the
"Grand Priest" class of live wrongness (`TIBET-PACKAGE.md` §0.4) and the
`rank_duchy_theocracy` class the Arabia package found: a Roman republican
magistracy on an eleventh-century Kama trading settlement. It is a *static*
finding — no file settles which rank the engine derives at 19 locations, so
whether the branch is the duchy one or the county one is **OWED CHECK 1**;
either way there is no NOV-style tag branch to catch it and the ruler title is
"Consul" or the county-republic equivalent.

### 0.5 The fifth finding: the registry needs NOTHING, and one of its values sits on zero locations game-wide

`MOD/in_game/setup/countries/` holds five whole-file overrides
(`east_asia.txt`, `horn_of_africa.txt`, `iberia.txt`, `italy.txt`,
`west_africa.txt`) plus `zz_1066_new_countries.txt` (74 blocks, measured).
**`russia.txt` and `siberia.txt` are NOT overridden**, and this package proposes
no override of either — the Gallura cost stays unpaid, as in Tibet.

PRM's registry (`russia.txt:309`) is already `komi` + `komi_paganism`, i.e.
already the 1066 identity. But:

**`komi_paganism` sits on ZERO locations in the entire game.** So do
`samoyedic_paganism` and `obian_paganism`. Measured across all 20,922 ownable
locations from `location_templates.txt`: `shamanism` covers **508**,
`erzya_religion` **9**, and the three Uralic-specific keys **0 each**. They
exist only as `religion_definition` values in `russia.txt`/`siberia.txt`
(`komi_paganism` on PRM; `samoyedic_paganism` on OBD/LYA/SLK; `obian_paganism`
on PLY/BAK/KND/BGJ/KOD/SVA/KZY/TBY). `komi_paganism` is a real religion
(`VAN/in_game/common/religions/folk_european.txt:224`, `group =
folk_european_group`, `permic_coa_gfx`); `shamanism` is
`folk_asian.txt:979`, `group = folk_asian_group` — **a different religion
GROUP**.

So PRM starts as a `komi_paganism` state over 64 `shamanism` locations: its
religious unity is structurally zero and its pops are in another religion group
from its own court. This is vanilla's condition at 1337 too, it is not a 1066
error, and it is **not this slice's to fix** — but it is the single most useful
thing this theater hands the pop phase, and nobody has written it down (§H).

### 0.6 The sixth finding: Novgorod holds TEN Ob-Ugric tributaries — and vanilla pointedly did NOT give it Bjarmia

`MOD/main_menu/setup/start/12_diplomacy.txt:50-59`, under the comment
`# Russia`, ten consecutive lines:

```
dependency = { first = NOV second = OBD subject_type = tributary }   # :50
dependency = { first = NOV second = PLY subject_type = tributary }   # :51
dependency = { first = NOV second = BAK subject_type = tributary }   # :52
dependency = { first = NOV second = KND subject_type = tributary }   # :53
dependency = { first = NOV second = BGJ subject_type = tributary }   # :54
dependency = { first = NOV second = KOD subject_type = tributary }   # :55
dependency = { first = NOV second = SVA subject_type = tributary }   # :56
dependency = { first = NOV second = KZY subject_type = tributary }   # :57
dependency = { first = NOV second = LYA subject_type = tributary }   # :58
dependency = { first = NOV second = TBY subject_type = tributary }   # :59
```

**This is vanilla's model of the Yugra tribute, and its geography is exact:**
eight of the ten (OBD LYA BAK KND BGJ KOD SVA KZY) sit in `west_siberia_region`
and two (PLY TBY) on the eastern Ural slope in `ural_area` — i.e. **all ten are
trans-Ural**. Bjarmia (BJA), the *Dvina* tribute land, has **no dependency line
at all** (grep-verified over the whole file). Paradox drew the line between the
Zavolochye, which Novgorod held directly, and Yugra, which it taxed.

The 1066 question is therefore narrow and answerable: **does the trans-Ural
tribute exist yet on 1066.9.15?** The first recorded Novgorod expedition to
Yugra is the Primary Chronicle's entry under 1096, Gyuryata Rogovich's man at
the Pechora and beyond [D — the entry describes a route as if established, so
whether it *begins* in 1096 or merely is *reported* then is exactly the point
sources differ on]. See OPEN DECISION 4.

Mechanically these ten cost nothing today: NOV is not in
`_MOD_TRIB_OVERLORDS` (`verify_mod.py:766-767` — `{FRA, LEI, TYR, TRY, MCM,
PAP, KIE, LIA, PLB}`), so the tributary visible-gate check does not read them;
and they would pass anyway on the **subject** branch, since every one of the ten
resolves to `type = tribe` (`eurasian_tribe` plus an explicit line in each
block). Stripping them cannot break the gate check and cannot move its
`min_count=78` (`verify_mod.py:843`).

One thing nobody has measured: NOV is itself KIE's tributary
(`RUS_TRIBUTARIES = (("KIE", "NOV"),)`, `build_setup.py:1349`), so the build
currently ships a **tributary that holds ten tributaries**. Vanilla shipped the
ten; the mod added the eleventh above them. Whether the engine flattens,
forbids or accepts a two-level tributary chain is **OWED CHECK 2** — no file in
either tree settles it and no click tour has looked.

### 0.7 Ownership, culture, religion and pops — measured per area, in the CURRENT build

Ownable counts from `definitions.txt` via `_defs`; culture/religion from
`location_templates.txt`; owners from `MOD/main_menu/setup/start/10_countries.txt`
with the full ten-key reader; `define_pop` from `VAN/main_menu/setup/start/
06_pops.txt`.

| area | ownable | pops | owners in the MOD build (vanilla's, where different) |
|---|---|---|---|
| `bashkiria_area` | 26 | 82 | **26 unowned** (vanilla: GLH 26 — the Central Asia vacate) |
| `bolghar_area` | 21 | 61 | **BLH 21** (Central Asia slice — closed seam) |
| `karagay_area` | 15 | 42 | **PRM 15** |
| `kazan_area` | 30 | 88 | **PRM 15, BLH 7, 8 unowned** (vanilla: GLH 15, PRM 15) |
| `perm_area` | 27 | 66 | **PRM 18, GLH 4, 5 unowned** |
| `ural_area` | 31 | 47 | **31 unowned** |
| `ust_sysola_area` | 17 | 41 | **PRM 11, VYT 3, 3 unowned** |
| `vorkuta_area` | 9 | 15 | **PRM 3, 6 unowned** |
| `vyatka_area` | 18 | 60 | **VYT 16, PRM 2** |
| **`ural_region` total** | **194** | **502** | PRM 64, BLH 28, VYT 19, GLH 4, **79 unowned** |
| `arkhangelsk_area` | 25 | 89 | NOV 7, **18 unowned** (13 of them BJA's) |
| `pomorye_area` | 30 | 72 | NOV 29, 1 unowned |
| `totma_area` | 29 | 76 | NOV 27, 2 unowned |
| `nizhny_novgorod_area` | 31 | 67 | GLM 11, GLH 8, NZH 6, GRS 6 |

**Religion and culture are already 1066-correct on the ground.** Of
`ural_region`'s 194: `shamanism` **132**, `sunni` 51 (the Bolghar/Bashkir
Muslim belt — BLH's slice), `orthodox` **7**, `erzya_religion` 4. The seven
Orthodox locations are the five VYT holds in `vyatka_area` plus two in
`kazan_area`. **There is no 222-location al-Andalus problem here and no Hausa
registry problem; the pop phase inherits almost nothing from this theater
except §0.5's religion-key mismatch.**

**The theater already contains 100 unowned locations carrying 215 pops**, of
which 67 (135 pops) are covered by no `type = pop` country at all — that is
vanilla's and the build's own stateless model already running at scale in
exactly the ground the brief describes.

Pop density: `ural_region` is 502 pops over 194 locations, **2.6 per
location** — thinner than Tibet's 3.5 and the thinnest theater the project has
measured. A vacate here is cheap.

### 0.8 The eighth finding: this ground was double-punted, and both punts point here

`RUS-STEPPE-PACKAGE.md:737` (§H) sends `ural_region` and Volga Bulgaria to the
**Central Asia package**. `CENTRAL-ASIA-PACKAGE.md:621` (§H) sends it back:

> **PRM (64) and VYT (20)** | Kama and Vyatka, west/north of my line and inside
> the Rus orbit. **VYT is in fact an ANACHRONISM at 1066** — the Vyatka Land is
> a late-12th-century Novgorodian colony — but retiring it is the Rus package's
> call, not mine. Flagged, not touched.

And `RUS-STEPPE-PACKAGE.md:744` on the third piece:

> `nizhny_novgorod_area` (31) — GLM 12, GLH 8, NZH 6, GRS 6 | Merya/Mari
> forest; Gorodets 1152, Nizhny Novgorod 1221, Galich-Mersky 1237. **Every tag
> there is an anachronism but nothing in 1066 clearly owns it.** Deliberately
> NOT swept into PYS | revisit with the Volga seam

**Two packages looked at this ground, both named the same anachronism, and
neither claimed it.** This package closes the Perm/Vyatka half and — per §D.3 —
recommends leaving the `nizhny_novgorod_area` half where RUS-STEPPE put it,
with the counter-argument stated rather than buried.

---

## A. Registry

### A.1 What already exists and needs nothing

| tag | registry | holds now | why it is right, or what is wrong |
|---|---|---|---|
| **PRM** Perm | `VAN/…/russia.txt:309` | 64 | identity **already correct** (`komi` + `komi_paganism`); only the start block is wrong (§B.1) |
| **VYT** Vyatka | `russia.txt:316` | 19 | `novgorodian` + `orthodox` — correct for the polity vanilla means, which is the problem |
| **the nineteen Siberian identities** | `siberia.txt:1`-`:138` | 0 each | vanilla's legitimate `type = pop` class — the Tibetan MSH/TAN/MNP precedent at nineteen times the scale |
| **BJA** Bjarmia | `VAN/…/_scandinavia.txt:77` | 0 | `type = pop`, 16 pop-locations, all unowned. **Exactly right at 1066** |
| **BSH** Bashkir | (registry probed, `type = pop` block at `10_countries`) | 0 | same |
| GLM / GRS / NZH | `russia.txt:155` / `:274` / `:267` | 11 / 6 / 6 | `muscovite` + `orthodox`; §D.3 and OPEN DECISION 5 |

**No new registry block is proposed and no registry override is proposed.**
Registry stays at **74**, overrides stay at **five files**.

### A.2 Freeness of candidates — three scans each, run anyway

Even though this package creates no tag, the scan was run so that a reviewer
asking "why not an Udmurt tag?" gets a measured answer rather than an opinion.
Method per `TIBET-PACKAGE.md` §A.2: (1) word-boundary `\bTAG\b` over the whole
vanilla tree, non-localisation and English-localisation counted separately; (2)
**substring** `_TAG\b|\bTAG_` over the same tree; (3) both over the whole mod
repo. Text files only (`.txt .yml .gui .info .asset .gfx .py .md .json .mod
.csv .log .settings`) — `KNOWLEDGE.md`, "Tag-freeness sweeps MUST exclude
binaries". Registry index read `utf-8-sig` over BOTH `in_game/setup/countries/`
trees, **unanchored** — the BOM trap. **16,226 vanilla files and 70 mod files
scanned; 2,320 registry tags indexed.**

| candidate | VAN word | VAN en-loc | VAN sub | MOD word | MOD sub | registry | verdict |
|---|---|---|---|---|---|---|---|
| **UDM** (Udmurt) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **VOT** (Votyak) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **ZYR** (Zyrian) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **YUG** (Yugra) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **BJR** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **VTK** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **KHL** (Khlynov) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **KOM** (Komi) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **MDV** (Mordvin) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **ERZ** (Erzya) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **MKS** (Moksha) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **MRI** | 40 | 1 | 50 | 9 | 19 | `VAN:east_asia.txt:729` | **TAKEN** — the obvious "Mari" mnemonic is gone |
| **CHM** (Cheremis) | 23 | 1 | 48 | 2 | 18 | `VAN:andes.txt:11` | **TAKEN** — an Andean tag |
| **ARS** (Arsk) | 47 | 11 | 54 | 15 | 18 | `VAN:lowlands.txt:132` | **TAKEN** — Artois |
| **PCH** (Pechora) | 22 | 1 | 48 | 2 | 18 | `VAN:central_north_america.txt:136` | **TAKEN** |
| **PER** | 48 | 2 | 67 | 32 | 18 | `VAN:france.txt:389` | **TAKEN** |
| **MER** | 19 | 1 | 47 | 7 | 17 | `VAN:_default.txt:9` | **TAKEN** — an engine placeholder (the DUMMY/MER/PIR set, `verify_mod.py:1111`) |
| **BJA** | 20 | 1 | 47 | 2 | 17 | `VAN:_scandinavia.txt:77` | **TAKEN** — Bjarmia already exists |
| **MAR** | 24 | 1 | 51 | 25 | 20 | `VAN:east_asia.txt:2203` | **TAKEN** — Maryul (Ladakh), the Tibet slice's |
| **VYA** | 29 | 1 | 50 | 7 | 18 | `VAN:russia.txt:169` | **TAKEN — and this is the brief's own trap: `VYA` is VYAZMA, a Smolensk-area principality already retired in `RUS_LANDLESS` (`build_setup.py:1345`). Vyatka is `VYT`, and `VYT` is LANDED with 19.** |

The `VYA`/`VYT` row is the scanner earning its keep for the second time in this
project: the brief hypothesised "VYA/Vyatka may ALREADY be landless". It is
not. `VYA` (Vyazma, `country_names_l_english.yml` NAME "Vyazma", vanilla
holdings 10 = `smolensk_area` 9 + `moscow_area` 1) went landless with the
other 41 Rus principalities; `VYT` (Vyatka) never entered any landless tuple
and holds 19 locations today.

### A.3 New blocks — NONE

No `NEW_COUNTRIES` entry (`build_setup.py:502`), no colour, no CoA, no loc row.
The candidate case is argued and refused in OPEN DECISION 2.

---

## B. The country blocks

### B.1 `FIELD_FIXES` — PRM de-Russified in place (the SXM shape)

`FIELD_FIXES` (`build_setup.py:3089`) is applied per tag with an
exactly-once assertion on every `old_line` (`:6403-6419`, "appears {k}x in
{_t} — expected exactly once"). Each string below was verified against the
built block at `MOD/…/10_countries.txt:3192-3223` and occurs **exactly once**
inside it.

```python
    # PRM: Great Perm de-Russified. Vanilla's own registry already calls
    # it komi + komi_paganism (russia.txt:309); only the start block
    # dresses it as a Rurikid feudal principality — the SXM shape
    # (build_setup.py:3161), one rung colder. The Komi of the Vychegda
    # and the Udmurts of the Cheptsa had no state in 1066 [D]; a tribe
    # over the same 64 locations is the model the map data already
    # paints (64/64 shamanism, 49/64 udmurt). The explicit type/heir
    # lines override the include's, so all three must move together;
    # limited_russian_principality declares no `type =` at all.
    "PRM": [('include = "limited_russian_principality"',
             'include = "eurasian_tribe"'),
            ("\t\t\ttype = monarchy", "\t\t\ttype = tribe"),
            ("heir_selection = cognatic_primogeniture",
             "heir_selection = tribal_oldest_male"),
            ("\t\tdynasty = rurikovich_dynasty\n", "")],
```

Four surgeries, each with a precedent already in the file:

| surgery | precedent | `file:line` |
|---|---|---|
| include swap monarchy-template → `eurasian_tribe` | SXM (Baltic slice) | `build_setup.py:3161-3162` |
| explicit `type = monarchy` → `type = tribe` | SXM | `:3166` |
| `heir_selection` → `tribal_oldest_male` | SXM | `:3167-3168` |
| drop a `dynasty = …` line whole | KBO (`dynasty = sayfawa_dynasty` removed, Africa slice) | `:3211` |

`eurasian_tribe` (`VAN/main_menu/setup/templates/eurasian_tribe.txt`, read in
full) supplies `type = tribe`, `heir_selection = tribal_oldest_male`, thirteen
sliders, **`parliament = { parliament_type = assembly }`**, `laws = {
marriage_law = polygyny, heir_religion_law = heir_same_religion }` and
privileges `tribes_tribal_levies` + `tribes_allow_gatherings`. It is the same
template the seven new Baltic tribes and all nineteen Siberian pop-countries
already ride, and it keeps PRM inside the parliament check
(`verify_mod.py:1244`) rather than dropping it.

What is deliberately NOT restated: nothing. Diffed both templates —
`limited_russian_principality` supplies no field `eurasian_tribe` lacks that
PRM's block needs, because every field it supplies is one of the eleven feudal
laws and thirteen estate privileges the swap is *for*. PRM keeps
`starting_technology_level = 3` (see OPEN DECISION 3), `tolerated_cultures = {
udmurt }`, `capital = cherdyn`, `include = "expl_novgorod"` and `include =
"expl_mongols"`.

**`ruler = random` is untouched** and stays exactly one per block —
`FIELD_FIXES` runs before the ruler pass (`build_setup.py:6425-6455`) and the
one-ruler check (`verify_mod.py:937`) is unaffected.

### B.2 VYT — no field surgery, because the tag itself is the anachronism

The NOV precedent applies when the polity existed and only its constitution was
dated (`build_setup.py:3091-3105`: "In 1066 Novgorod is a Rurikid principality
under Mstislav — the veche deposes its first prince only in 1136"). **Novgorod
was there in 1066; the Vyatka Land was not.** Retiring the tag (§E.1) removes
the whole 83-line republic apparatus at once, along with the "Consul" render,
and is strictly cheaper than a six-surgery NOV-shaped `FIELD_FIXES` that would
leave a Novgorodian Orthodox principality on Udmurt pagan ground.

### B.3 Registry overrides — NONE proposed

---

## C. Rulers — nobody, and the reasoning is short

Zero characters exist for PRM, VYT, NZH or GRS in either tree; GLM's five are
all born 1230 or later (§0.3). No 1066 Komi, Udmurt, Mari or Vyatka ruler is
attested well enough to name [U]. `permic_language` would render one
beautifully (§0.3) and the mechanism is fully attested in this repo (the
Dongzhan/Tunka Manin precedent, `HANDOFF.md:1852-1854`), but the Tunka Manin
argument was *an attested ruler known through a transcription*; here there is
no ruler, transcribed or otherwise.

**Thrones stay at 179. Zero characters, zero dynasties, zero name-key loc rows.**

---

## D. What must die, what must be left, and where the seams are

### D.1 VYT — the theater's one unambiguous retirement

Vyatka: the "Tale of the Vyatka Country" places the Novgorodian settlement at
1174 and Khlynov's foundation shortly after; the town first appears in Moscow
chronicles in 1374; archaeologically the Russian occupation of the Vyatka
basin is 12th–13th century [all D — the Tale is a late compilation and its
1174 date is contested]. The veche republic proper belongs to the 14th–15th
centuries and ends in 1489 [D]. **On 1066.9.15 the Vyatka basin is Udmurt and
Komi ground with no state at all**, and vanilla's own map data agrees: 14 of
VYT's 19 locations are `komi`/`udmurt` on `shamanism`.

VYT is the MAJ/SUK/TIB class — a post-1066 object — and the project retires
those. §E.1.

### D.2 PRM — reshape, do not retire

Perm the Great as a *principality* seated at Cherdyn is a 15th-century object;
its princes appear in Moscow's records from the 1450s and it is annexed in 1472
[D]. The Komi were christianised by Stephen of Perm 1379–96 [D]. **But the
Komi/Udmurt world itself is 1066-real**, PRM's registry already says so, and
vacating 64 locations carrying 177 pops to replace them with nothing would be
the largest vacate the project has made outside Central Asia — for ground where
a named tribal identity already exists in the database.

This is the Kham/Shan/Philippines decision: **the model is right even though the
state name is late.** Difference from Kham: there the fix was to leave the tags
untouched; here one constitutional surgery makes the model honest (§B.1).

### D.3 `nizhny_novgorod_area` — measured, and left where RUS-STEPPE put it

GLM 11 (`galich_province` 6 + `unzha_province` 5), GRS 6
(`gorodets_province`), NZH 6 (`nizhny_novgorod_province`), GLH 8
(`uren_province`) — 31 locations, 67 pops, **100% `muscovite` culture and
`orthodox` religion in `location_templates.txt`**. Nizhny Novgorod is founded
1221 by Yuri Vsevolodovich, Gorodets c.1152 by Yuri Dolgoruky, Galich-Mersky
first mentioned 1237/38 [all D]. Every tag there is late; RUS-STEPPE said so
(`:744`) and declined it.

**Recommendation: LEAVE, and hand it to the Volga seam with this measurement
attached.** Three reasons, and the counter is in OPEN DECISION 5: the ground is
painted Russian-Orthodox by Paradox, so neither vacating it nor tribalising it
matches the map data without a pop pass; it sits in `russian_region`, outside
the Finno-Ugric brief; and it is the one piece of this theater that another
package explicitly reserved.

### D.4 GLH's residue inside the theater — 15 locations, three provinces, two classes

| province | area | n | pops | culture / religion | class |
|---|---|---|---|---|---|
| `ufa_province` | `perm_area` (**`ural_region`**) | **4** | 8 | `mari_culture` / `shamanism` | **the `bashkiria_area` class the Central Asia vacate already answered — and missed, because `ufa_province` is filed under `perm_area`, not `bashkiria_area`** |
| `minusinsk_province` | `kansk_area` (`west_siberia_region`) | **3** | 6 | `khakas_culture` / `tengri` | the Siberia class (decision 9, `build_setup.py:1258-1262`: "the Golden Horde holding Tomsk in 1066 is absurd") — `tomsk_area` was vacated, `kansk_area` was not |
| `uren_province` | `nizhny_novgorod_area` (`russian_region`) | 8 | 16 | `muscovite` / `orthodox` | goes with §D.3 — leave |

`LOCATION_VACATED["GLH"]` (`build_setup.py:1265-1272`, re-set to 291 at
`:1400`) already names `bashkiria_area` and `yaransk_province` and
`tomsk_area`. **The four Ufa locations and the three Minusinsk ones are the
same two decisions, one province short each.** OPEN DECISION 3.

### D.5 The seams — named, measured, not touched

| ground | measured now | whose |
|---|---|---|
| **BLH** Volga Bulgaria — `bolghar_area` 21 + `kazan_province` 7 = **28** | landed, correct | Central Asia slice, **CLOSED** (`build_setup.py:1245-1247`) |
| **NOV's 63 northern locations** — `pomorye_area` 29, `totma_area` 27, `arkhangelsk_area` 7 | 146 pops, all `orthodox` | Rus Tier 1, **CLOSED** (`RUS-STEPPE-PACKAGE.md:389`, `totma_area` swept deliberately as "the Zavolochye tribute land") |
| **KRL** Karelia's 28 owned pop-locations (NOV 21, SWE 7) | — | Baltic / Sweden-Finland edge |
| **CUM** 211, **GLH** 175 elsewhere (`samara_area` 43, `tambov_area` 41, `astrakhan_area` 37, `majar_area` 25, `matrega_area` 10, `northern_caucasus_area` 4) | — | Rus Tier 2 done; the Volga/Caucasus residue is the declared Volga-seam and Caucasus-package property |
| **`west_siberia_region`** 330 and **`east_siberia_region`** 537 | 327 and 537 unowned respectively; **GLH's 3 in `kansk_area` are the only owned land east of the Urals** | measured and left (OPEN DECISION 3 covers the 3) |
| `erzya_culture` 9 + `moksha_culture` 3 — the Mordvin ground | CHR 3, GLH 5, BLH 1, 3 unowned | scattered across `oka_area`/`tambov_area`/`bashkiria_area`; belongs to the Volga seam with §D.3 |

---

## E. Territory

### E.1 The recommended rule sets — vacates only, no grants, and every donor table printed

**This package proposes ZERO `LOCATION_GRANTS` entries.** Nothing changes hands;
land is removed from owners who should not have it and given to nobody, which
is what "stateless" means and what the theater's 100 already-unowned locations
already look like. `UNOWNED_GRANTS` (`build_setup.py:1919`) is not used and
must not be — the SEA phantom's lesson applied prospectively.

The mechanism is `LOCATION_VACATED` + `LOCATION_VACATED_EXPECT`
(`build_setup.py:1265`, `:1273`), resolved at `:6210-6232`. Resolution is
**snapshot-based**: `_pool` is the union of the named region/area/province
members, and `got = sorted(_pool & set(_owned_by(src, _t)))` (`:6217`) — the
intersection is taken **against that tag's holdings only**, so a location
belonging to any other tag can never be swept. This is a structurally stronger
guard than the grant path, and it is why the recommended design uses it
exclusively.

```python
# --- Vyatka: the Novgorodian colony that does not exist yet. The two
#     names cover 23 ownable; PRM owns 4 of them (afanasyevo, kirs,
#     koygorodok, vizinga) and the snapshot intersection excludes them.
LOCATION_VACATED["VYT"] = ["vyatka_area", "lalsk_province"]
LOCATION_VACATED_EXPECT["VYT"] = 19

# --- the Ufa corner: mari_culture/shamanism forest inside perm_area,
#     the one province the Central Asia bashkiria_area vacate could not
#     reach because definitions.txt files it elsewhere. OPEN DECISION 3.
LOCATION_VACATED["GLH"] += ["ufa_province"]                    # 291 -> 295
# --- and the Minusinsk basin, kansk_area's GLH toehold: the last owned
#     land east of the Urals. OPEN DECISION 3.
LOCATION_VACATED["GLH"] += ["minusinsk_province"]              # 295 -> 298
LOCATION_VACATED_EXPECT["GLH"] = 298

PERM_LANDLESS = ("VYT",)
```

### E.2 DONOR TABLES — every proposed rule, who loses exactly what, summed per donor

**This is the section `KNOWLEDGE.md`'s delta-guard law demands, and the main
session is asked to reproduce it before implementing.** The reason is stated in
the law itself: when a donor survives elsewhere, the emptied-but-unlisted delta
guard (`build_setup.py:6338-6343`) stays silent and the exact-count assert is
the *only* line of defence. GLH survives with 171 locations after both proposed
vacates; **no guard will notice if these rules take the wrong land.**

**Rule 1 — `LOCATION_VACATED["VYT"] = ["vyatka_area", "lalsk_province"]`,
expected 19.**

| donor | loses | locations |
|---|---|---|
| **VYT** | **19** | `belozerye bolshaya_yakshanga kholunitsky kobra koksharov lalsk nagorsk nikolsky obyachevo omutninsk oparino orlov podosinovets slobodskoy suna ust_cheptsa verkhoshizhemye vokhma vyatka` |
| PRM | **0** | `afanasyevo kirs koygorodok vizinga` are inside the swept names and are **PRM's** — excluded by the snapshot intersection at `:6217`, not by a minus-list |
| **total** | **19** | **55 `define_pop`** |

Raw resolve of the two names is **23**; VYT holds **19** of them. If the
implementation writes `23`, the assert at `:6218-6221` fires with 19 — this is
break-test (b).

**Rule 2 — `LOCATION_VACATED["GLH"] += ["ufa_province"]`, +4.**

| donor | loses | locations |
|---|---|---|
| **GLH** | **4** | `askino baltas burayevo ufa` |
| **total** | **4** | **8 `define_pop`** |

Raw resolve 4, all four GLH's. **GLH survives with 171 — the delta guard will
NOT fire and cannot.**

**Rule 3 — `LOCATION_VACATED["GLH"] += ["minusinsk_province"]`, +3.**

| donor | loses | locations |
|---|---|---|
| **GLH** | **3** | `abakasnk beya shushenskoye` |
| — | 0 | `idrinskoye` and `minusinsk` are inside the province and are **already unowned** — excluded by the intersection |
| **total** | **3** | **6 `define_pop`** |

Raw resolve 5, GLH holds 3. Writing `5` fires the assert with 3 — this is the
Tibet `zagya` case reproduced, break-test (c).

**Combined: `LOCATION_VACATED_EXPECT["GLH"]` 291 → 298.** The sum must be
checked as one number, because the two additions share a dict entry.

**Donor tables for the ALTERNATIVES, so the main session can pick either
without re-measuring:**

**Alt 1a — grant VYT's 19 to PRM instead of vacating** (OPEN DECISION 1b).
Rule set in the SEA/Tibet convention (`build_setup.py:5962-5972`, `:5980-5990`
— `expected` is the **resolved list size**, extended into `LOCATION_GRANTS`):

```python
_PERM_RULES = {"PRM": (["vyatka_area", "lalsk_province"], [], [], [], 23)}
```

| donor | loses | note |
|---|---|---|
| **VYT** | **19** | the list above |
| **PRM** | **0 (self-grant of 4)** | `afanasyevo kirs koygorodok vizinga` are already PRM's; a self-grant is attested (`build_setup.py:5959-5961`, "LAV/PHY/PUA/KTG/CHH/MUA/INR/LGE self-grants ride the GHA/koumbi_saleh precedent") |
| **total resolved** | **23** | PRM 64 → 83; **every one of the 23 carries exactly ONE ownership entry** (re-measured with the ten-key reader — `_remove_owned_many`'s `!= 1` exit at `:5731` will not fire) |

**Alt 1b — vacate ALL of PRM as well** (OPEN DECISION 2c): PRM loses 64, 177
pops, and `PERM_LANDLESS` becomes `("VYT", "PRM")`. Donor table is PRM 64 and
nobody else — `karagay_area` 15, `perm_area` 18, `kazan_area` 15,
`ust_sysola_area` 11, `vorkuta_area` 3, `vyatka_area` 2, which is **not**
resolvable by whole-area names (PRM's holdings straddle six areas it does not
own outright) and would need eleven province names plus two singles. Costed and
refused.

**Alt 3 — retire GLM/GRS/NZH and vacate their 23** (OPEN DECISION 5b):

| rule | donor | loses | pops |
|---|---|---|---|
| `LOCATION_VACATED["GLM"] = ["galich_province", "unzha_province"]`, 11 | **GLM** | **11** (`chukhloma galich kologriv kuzhbal manturovo nikolo_dor parfenyevo pyshchug sol_galichskaya sudai unzha`) | 22 |
| `LOCATION_VACATED["GRS"] = ["gorodets_province"]`, 6 | **GRS** | **6** (`gorodets kadyy korenevo lukh vasilyeva_sloboda yuryev_povolzhsk`) | 15 |
| `LOCATION_VACATED["NZH"] = ["nizhny_novgorod_province"]`, 6 | **NZH** | **6** (`dalneye_konstantinovo gorokhovets meshchersk nizhny_novgorod pestyaki rastyapino`) | 14 |
| `LOCATION_VACATED["GLH"] += ["uren_province"]`, +8 | **GLH** | **8** (`kovernino krasnye_baki semyonov sharanga tonshayevo uren varnavino vetluga`) | 16 |
| **total** | | **31** | **67** |

Each of the three provinces resolves to exactly the tag's own holdings (raw
resolve equals the intersection in all four cases — verified). Under Alt 3,
`_expected_ghosts` gains `["GLM", "GRS", "NZH"]` (156 → 159, §G.3) and
`n_landless_deps` gains 1 (280 → 281, the NZH→GRS line).

### E.3 What each tag keeps

| tag | before | after (recommended) | verdict |
|---|---|---|---|
| **VYT** | 19 | **0** | **LANDLESS** — claims derived from the 19 by `_landless_claims` (`build_setup.py:6119`), which snapshots holdings BEFORE the vacate (`:6203-6204` comment: "Runs AFTER the `_landless_claims` snapshot") |
| **PRM** | 64 | **64 — unchanged** | reshaped, not moved (§B.1) |
| **GLH** | 175 | **168** | 4 + 3 vacated; **survives, so the delta guard cannot see a mistake here** |
| BLH / NOV / GLM / GRS / NZH / the 19 pop-countries | — | **unchanged** | §D.3, §D.5 |

**Order matters and is already right:** `_landless_claims` snapshots at `:6119`,
the vacate runs at `:6210-6232`. VYT's nineteen therefore enter its claim list,
which is correct — a landless Vyatka claims the Vyatka land, and that claim IS
the 1174 colony as a stated future, exactly the shape `RUS-STEPPE-PACKAGE.md:425`
calls "the ZTA/giudicati law running in the other direction".

### E.4 The vacate's real cost, and a correction to the decoder's model

`docs/EU5-ERROR-DECODER.md:675-685` costs a vacate at "one line per pop on
vacated settled land" and records ~504 lines observed at the first
`LOCATION_VACATED` launch. That launch's vacate was GLH 284 + CHG 21 = **305
locations**, and those 305 carry **911 `define_pop`** (measured by resolving
`LOCATION_VACATED["GLH"]`/`["CHG"]` against vanilla ownership). **911 pops
produced ~504 lines, a ratio of ≈0.55** — so the one-line-per-pop model
over-predicts by nearly half.

Two things follow, both flagged as arithmetic on two recorded numbers, **not as
an in-game observation**:

1. The build's current 599 vacated locations carry **1,869 `define_pop`**, so
   the class should stand near **1,000 lines** at the next launch, not 504.
   Worth one glance in the accumulated test (`HANDOFF.md:1910`).
2. This package's recommended vacates cost **55 + 8 + 6 = 69 `define_pop` ≈ 38
   lines**. Under Alt 3 add 67 pops ≈ 37 more.

A candidate explanation was tested and **REFUTED**, and is recorded so nobody
re-tests it: it is not that unowned land is unsettled. Vanilla's own 7,334
unowned locations carry **8,245 `define_pop`**, and only **8** of the 599
vacated locations appear in `07_cities_and_buildings.txt` at all (which holds
1,108 entries: 746 `town`, 262 `city`, 3 `megalopolis`, 7 `rural_settlement`).
Neither pop presence nor town presence predicts the count. A second candidate —
that `add_pops_from_locations` coverage by a `type = pop` country supplies the
missing religion link — also fails on arithmetic: 4,515 vanilla-unowned
locations lack such coverage and carry 4,766 pops, which would have made the
class enormous before this project existed. **The true filter is unknown and
is OWED CHECK 3.**

### E.5 `CAPITAL_FIXES` — none

The orphan-capital guard fires only for a tag that still holds land but not its
capital. PRM keeps `cherdyn` (in `cherdyn_province`, retained). **VYT's `capital
= vyatka` becomes vestigial and is exempt** by the guard's `if held and …`
condition — the POR/`guimaraes` precedent, and the Arabia slice's four
deliberately-kept vestigial entries (`build_setup.py:2198-2201`). It is also
*right*: a landless Vyatka whose capital is Khlynov is a Vyatka whose future
starts where the sources say it started. **`CAPITAL_FIXES` (`:3016`) gains
nothing.**

### E.6 What this slice moves, in one line

**0 locations change owner, 26 are vacated (VYT 19 + GLH 7), 1 tag is retired
landless, 0 new tags, 1 block reshaped by four field surgeries, 10 dependency
lines stripped by name, 0 capitals corrected, 0 rulers seated, 0 characters, 0
dynasties, 0 registry blocks, 0 registry overrides, 0 colours, 0 CoA, 0 loc
rows.**

---

## F. Rank, government and naming — worked out to the rendered string

### F.1 What each tag renders as, before and after

| tag | today | after the recommended design |
|---|---|---|
| **VYT** | map "Vyatka"; panel **"Republic of Vyatka"**; ruler **"Consul"** (`rank_duchy_republic`, `country_ranks.txt:1423` → `government_names_l_english.yml:693-696`) — subject to OWED CHECK 1 on the derived rank | **gone from the map** — a landless shell with 19 claims |
| **PRM** | map "Perm"; `rank_duchy` default (`:2006`) → "Duchy of Perm" / **"Duke"** | map still "Perm" (fallback `_map: "$NAME$"`); `rank_duchy_tribe` (`:1606`) → **"Tribe of Perm" / "Chief"**, or `rank_county_tribe` (`:2278`) → "Minor Tribe" / **"Chieftain"** at county rank |
| GLM / GRS / NZH | `country_rank = rank_duchy` declared explicitly; `muscovite` → `east_slavic_language` → `rank_duchy_russian_prince` (`:1973`) → **"Principality of Galich-Mersky" / "Prince"** | unchanged (D.3) |
| the 19 pop-countries | `type = pop` reaches the ADJ branch at `country_name_construction.txt:116-157` | unchanged |

**PRM does NOT reach `rank_duchy_russian_prince`** — that branch tests
`culture.language = language:east_slavic_language`, and PRM's registry culture
`komi` maps to `permic_language` (`VAN/in_game/common/cultures/permic.txt:1-2`,
`komi = { language = permic_language`). Verified explicitly because the branch
sits above the generic `rank_duchy` and a `muscovite`-cultured Perm would have
rendered "Prince" — the LIT trap's shape.

**No tag-gated branch in `country_ranks.txt` names any theater tag** except
`rank_duchy_republic_novgorod`/`rank_kingdom_republic_novgorod`
(`:1413`/`:826`, both `tag = NOV`) — and NOV is a monarchy in the current build,
so those two branches are dead for us already.

### F.2 The derived-rank question, restated honestly

Neither PRM nor VYT declares a `country_rank`. **No file settles the thresholds
by which the engine derives one** — the Tibet slice recorded the same gap and
left it as an owed check (`build_setup.py:2181-2185`, "The engine derives ranks
by rules no file settles — OWED CHECK"). At 64 and 19 locations the plausible
derivations are duchy and duchy-or-county respectively. **Every render claim in
F.1 is conditional on that, and the click tour is what settles it.**

Declaring `country_rank = rank_county` on a tribal PRM would *guarantee*
"Minor Tribe of Perm" / "Chieftain", which reads better for a Komi chiefdom than
"Tribe"/"Chief" — but it is a styling choice made from a guess about what the
engine would otherwise do, and this package does not make it. Banked.

### F.3 Formables — none touched, none opened

`VAN/in_game/common/formable_countries/00_formable_countries.txt` and
`common/hegemons/` were grepped for PRM, VYT, GLM, GRS, NZH: **zero hits in
either**. Unlike TIB, a landless Vyatka is not a reunification target vanilla
already wrote; it is a claims-backed shell whose 19 claims are its own future.
Opening a `VYT_f` is available and is **not** recommended — the Vyatka
Republic is a specific 14th-century object, not a culture-group reunification.

---

## G. Diplomacy

### G.1 The ten Yugra tributary lines — the only named strip proposed

`MOD/main_menu/setup/start/12_diplomacy.txt:50-59` (§0.6). The prescription
copies the KBO→Hausa shape (`build_setup.py:7556-7565`) and the Tibet tusi
shape (`:7640-7649`) exactly:

```python
    # Novgorod's Yugra tribute (12_diplomacy.txt:50-59): ten tributary
    # ties over the trans-Ural Ob-Ugric and Samoyed pop-countries.
    # Vanilla's own geography is exact — all ten are beyond the Urals,
    # and BJARMIA, the Dvina tribute land, has no tie at all. The first
    # recorded Novgorod expedition to Yugra is the PVL's 1096 entry
    # [D]; on 1066.9.15 the trans-Ural tribute is thirty years out
    # while the Zavolochye NOV holds directly is not. The subjects stay
    # landed (they hold nothing to begin with — type = pop), so the
    # landless sweep below cannot see these lines: they must die here.
    n_yugra_tribute = 0
    for _g in ("OBD", "PLY", "BAK", "KND", "BGJ", "KOD", "SVA", "KZY",
               "LYA", "TBY"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = NOV second = " + _g
            + r" subject_type = tributary \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_yugra_tribute += _k
    if n_yugra_tribute != 10:
        sys.exit(f"expected exactly 10 NOV->Yugra tributary strips, "
                 f"got {n_yugra_tribute}")
    report.append(("Novgorod's Yugra tribute unwound", n_yugra_tribute))
```

**A named strip is REQUIRED here and the landless sweep cannot substitute.**
`_drop_landless_dep` (`:7657-7666`) tests membership in `LANDLESS_AFTER`, and
none of the ten is or should be in it — they are `type = pop` countries that
hold no land by design and must not be listed as retirements. `n_landless_deps`
therefore stays **280** under the recommended design.

**No double-overlord risk**: the ten lines are removed, not repointed, and no
new tie is proposed anywhere in this package. Every one of the ten subjects has
exactly one overlord today and zero after.

### G.2 Repoints — NONE. New ties — NONE.

### G.3 What the landless sweep does and does not do here

**VYT names no dependency and sits in no international organization** —
grep-verified over both files with word boundaries: `12_diplomacy.txt` **0**
hits, `15_international_organizations.txt` **0** hits, in the mod tree and in
vanilla's. **PRM likewise: 0 and 0.**

Consequences, all measured:

| constant | `file:line` | effect of retiring VYT |
|---|---|---|
| `n_landless_deps` | `build_setup.py:7745` | **280 — unchanged** |
| `n_pacts` | `:7775` | **9 — unchanged** |
| `n_ghosts` / `_expected_ghosts` | `:7036` / `:6989` | **156 — unchanged**; VYT is in no member list |
| empty-IO-members pin | `verify_mod.py:910` | **9 — unchanged**; nothing is drained |

That is the cheapest diplomacy profile any retirement in this project has had.

For contrast, under Alt 3 (OPEN DECISION 5b) GLM, GRS and NZH are each members
of the `autocephalous_patriarchate` instance at
`MOD/…/15_international_organizations.txt:263-268` (`creation_date = 330.1.1`,
members `BYZ NOV SER GLM CHR NZH GRS KIE POK NRK`), so ghosts would go **156 →
159**, the list would drop to seven members (**not** empty — the pin at
`verify_mod.py:910` stays 9), and the `NZH → GRS` vassal line
(`12_diplomacy.txt:49`) would die in the landless sweep, **280 → 281**.

### G.4 Left alone

`NZH → GRS` vassal (`:49`) — dies only if D.3 is overturned. `KIE → NOV`
(`build_setup.py:1349`) — Rus Tier 1's, closed. Nothing else in the theater has
a diplomatic line.

---

## H. Left alone deliberately

| what | measurement | why |
|---|---|---|
| **The nineteen Siberian `type = pop` identities** | 0 locations each, in vanilla and in the build | §0.1. Vanilla's stateless model, complete and 1066-correct. **The single largest "already right" finding in any package so far** |
| **BJA Bjarmia (16 pop-locations) and BSH Bashkir (24)** | all 40 unowned | The Dvina and the Bashkir steppe-forest already stateless and already identified |
| **The 116 Ob-Ugric/Samoyed locations + 3 vepsian** | 234 + 3 `define_pop`, 100% unowned | ditto |
| **The theater's 100 already-unowned locations** | 215 `define_pop`; 67 of them (135 pops) covered by no pop-country | Vanilla's and the build's model. This package *adds* 26 and touches none of the 100 |
| **`west_siberia_region` (330) and `east_siberia_region` (537)** | 327 + 537 unowned; GLH's 3 in `kansk_area` the only exception | The brief's "measure and almost certainly leave" — confirmed. The 3 are OPEN DECISION 3 |
| **NOV's 63 northern locations** | 146 `define_pop`, all `orthodox`; `pomorye_area` 29, `totma_area` 27, `arkhangelsk_area` 7 | Rus Tier 1 swept `totma_area` deliberately as "the Zavolochye tribute land" (`RUS-STEPPE-PACKAGE.md:389`). Note for the record: Veliky Ustyug is founded 1147 and Totma first appears 1137 [both D], so this ground is forward-dated **as towns** — but EU5 ownership models tribute reach, and Novgorod's Dvina tribute is 11th-century [D]. Closed seam |
| **`nizhny_novgorod_area`'s 31** (GLM 11, GLH 8, NZH 6, GRS 6) | 67 `define_pop`, 100% `muscovite`/`orthodox` | §D.3, OPEN DECISION 5. Reserved by `RUS-STEPPE-PACKAGE.md:744` |
| **BLH's 28** | `bolghar_area` 21 + `kazan_province` 7 | Central Asia slice, closed |
| **`yaransk_province`'s 8 unowned Mari locations** | 16 `define_pop`, `mari_culture`/`shamanism`, covered by NO pop-country | Already vacated by the Central Asia slice and correct. **Banked for POP-PHASE: the Mari have no `type = pop` identity anywhere in the game** (measured — no pop-country's `add_pops_from_locations` touches them), unlike the Khanty, Mansi, Nenets, Selkup, Bashkir and Bjarmians. Extending a pop-country's location list is a mechanism this build does not have, so it is not proposed here |
| **PRM's `religion_definition = komi_paganism` over 64 `shamanism` locations** | `komi_paganism`, `samoyedic_paganism` and `obian_paganism` sit on **ZERO of 20,922 locations**; `shamanism` on 508 | §0.5. **The strongest thing this theater hands POP-PHASE.** Same class as the Tibet slice's PUR `hindu` finding, but larger and vanilla-wide: eleven registry entries name religions no location carries. Whether that costs religious unity at start is an in-game question, not a file question |
| **A `country_rank` declaration on PRM** | vanilla declares none; 21 of Tibet's 22 landed tags likewise | §F.2. A styling choice made from a guess. Banked |
| **A Komi ruler** | `permic_language` ships 11 male + 11 female names and `patronym_suffix_komi` (`00_ural.txt:83-102`) | §C. The machinery is ready; the person is not attested |
| **`06_pops.txt` / `07_cities_and_buildings.txt`** | vanilla's, un-overridden | Note `KNOWLEDGE.md`'s "`tag = X … location = L` where X does not own L is FIRST-CLASS vanilla" — do **not** "fix" `07_cities` after the vacates. Only 8 of the build's 599 vacated locations are in it at all |
| **A Yugra situation** | vanilla dates nothing here; but the ten stripped ties are a dated, re-creatable object | Banked, the Second-Diffusion shape (`TIBET-PACKAGE.md` §H): a situation could re-establish NOV's Yugra tribute c.1096 on schedule, which is script the mod already knows how to write. Situation backlog, not setup data |

---

## I. Mechanism — every tool exists, and one of them is used in its safest mode

**This package needs no new build step and no new harness capability.**

| need | existing mechanism | `file:line` |
|---|---|---|
| region/area/province → locations | `_parse_defs` + `_ownable_set` + `_defs` | `:748`, `:772`, `:809` |
| rule-set resolution (alternatives only) | `_resolve_ruleset` | `:815`; SEA/Tibet model loops at `:5962-5972`, `:5980-5990` |
| **remove land and give it to nobody** | **`LOCATION_VACATED` + `LOCATION_VACATED_EXPECT`** | declare `:1265`, `:1273`; resolve + assert `:6210-6232` |
| the vacate's per-tag snapshot intersection (why no donor can be hit) | `got = sorted(_pool & set(_owned_by(src, _t)))` | `:6217` |
| vacate exact-count assert | | `:6218-6221` |
| vacate ∩ grant-list disjointness | | `:6223-6226` |
| retire with auto-derived claims | `LANDLESS_AFTER` + `_landless_claims` | `:2961`, `:6119` |
| prove the retiree really emptied | the `LANDLESS_AFTER … still owns` guard | `:6282` |
| prove the retiree carries claims | the claims-backed landless guard | `:6301` |
| catch a side-effect retirement | the emptied-but-unlisted delta guard | `:6338-6343` |
| exactly-one-owner on every removal | `_remove_owned_many` | `:5731` |
| field surgery in an existing block, exactly-once asserted | `FIELD_FIXES` | declare `:3089`, apply `:6403-6419`; **SXM model at `:3161-3168`, KBO dynasty-drop model at `:3211`** |
| named dependency strip | the KBO→Hausa / Tibet-tusi shape | `:7556-7565`, `:7640-7649` |
| dependency dissolution by landlessness | `_drop_landless_dep` | `:7657-7666`, assert `:7745` |
| IO member strip | `build_ios`'s generic `LANDLESS_AFTER` sweep | assert `:7036` |
| steppe-horde recipient guard | `_bad_recip` | `:6059-6061` — **not reached: this package has no recipients at all** |
| grant-list disjointness | `_list_owner` | `:6068-6074` — **not reached** |
| double-ownership | `CONTROL_STRIPS` | `:1705` — **no key needed; `ural_region` measured at zero double-ownership** |
| new country blocks / capital discovery | `NEW_COUNTRIES`, `_assert_new_block_discovery` | `:502`, `:5607` — **not used** |
| **`UNOWNED_GRANTS`** | **NOT USED, and must not be** | `:1919` |

Four asserts that will fire if the design is wrong, and should be watched:

1. **`LOCATION_VACATED["VYT"]` resolved-count** (`:6218`) — must be **19**, not
   the raw 23. This is the design's only near-miss.
2. **`LOCATION_VACATED_EXPECT["GLH"]`** (`:6218`) — must be **298**, not 291,
   295 or 300. Two additions share one entry; a half-applied change fails
   loudly, which is the point.
3. **the emptied-but-unlisted delta guard** (`:6338-6343`) — must stay
   **silent**. VYT is the only retirement and it is listed. **If it fires, a
   vacate took more than the design intends.** Note honestly what §E.2 says:
   for the two GLH rules this guard *cannot* fire either way, because GLH keeps
   168 locations. The donor table is the guard.
4. **`FIELD_FIXES` exactly-once** (`:6413`) — all four PRM strings were counted
   in the built block and each occurs once. A vanilla patch that reformats the
   block fails loudly here, as intended.

**The harness needs no new check.** Every class this package touches is already
guarded: landless holdings, landless claims, IO ghosts, empty IO members,
one-ruler-per-block, the identity↔start-block bijection, parliament reach, the
tributary gate, CoA coverage.

---

## OPEN DECISIONS

**1. VYT — retire landless, and what happens to the 19 locations?**
**(a) RETIRE + VACATE all 19** (recommended): 55 `define_pop` ≈ 30 log lines of
the accepted vacate class; claims 0 → 19; zero ghosts, zero dep strips, zero
pacts; the "Consul" render dies; the Vyatka basin joins the 100 already-unowned
locations around it and looks like what it was — Udmurt and Komi forest with no
state.
**(b) RETIRE + GRANT the 19 to PRM** (donor table in §E.2, Alt 1a): zero pop
lines, PRM 64 → 83, and the map shows one continuous Permian country from the
Vychegda to the Vyatka. Cheaper in log lines, and arguably the better *game*
(no colonisable hole between PRM and NOV).
**(c) LEAVE VYT ALONE**: costs nothing, keeps a Roman consul on the Kama.
**Recommendation: (a).** The Vyatka Land is the clearest post-1066 object in
the theater — later than Nizhny Novgorod, later than Gorodets — and vanilla's
own map data (14 of 19 locations `komi`/`udmurt` on `shamanism`) argues against
vanilla's own tag. **Counter:** (b) asserts less than it looks like it does —
"Great Perm" in this build is about to become a Komi tribe, and a Komi tribe
reaching the Vyatka is a smaller invention than an empty basin is an
assertion; and the project chose CUM over emptiness on exactly this
"unowned means colonisable" argument (`RUS-STEPPE-PACKAGE.md:461-465`). If the
main session prefers a full map, (b) is defensible and its donor table is
already printed.

**2. PRM — reskin in place, or retire?**
**(a) RESHAPE to a tribe** (recommended, §B.1): four `FIELD_FIXES` surgeries,
zero territory movement, zero new tags, zero pop lines. The registry already
says `komi` + `komi_paganism`; only the block disagrees.
**(b) LEAVE**: a Rurikid dynasty ruling a Komi pagan people through an estate
parliament, feudal administration and gold-and-silver coinage in 1066.
**(c) RETIRE + VACATE all 64** (donor table §E.2, Alt 1b): 177 `define_pop` ≈
97 log lines, eleven province names plus two singles to write, and a
64-location hole where a named Komi identity already exists.
**Recommendation: (a).** This is the Kham/Shan decision with one surgery: the
model (a Komi-Udmurt people occupying the Kama basin) is 1066-right; the
constitution is 15th-century. **Counter:** the project's own standard is "a
region is done when the people on the throne are the people who were there",
and a tribe with `ruler = random` and no attested chief satisfies that only by
lowering the bar to "nobody was there in particular". (c) is the option that
asserts nothing at all, and 177 pop lines is affordable — the build already
carries ~1,000.

**3. GLH's two leftover provinces — vacate 7, or leave to the Volga seam?**
`ufa_province` (4, `mari_culture`/`shamanism`, inside `perm_area`) is the
`bashkiria_area` decision one province short; `minusinsk_province` (3,
`khakas_culture`/`tengri`, `kansk_area`) is the `tomsk_area` decision one
province short and the **last owned land east of the Urals**.
**Recommendation: VACATE BOTH, 7 locations, expect 291 → 298** — both are
already-taken decisions whose sweeps missed a province because
`definitions.txt` files it elsewhere, and both cost 14 pops between them.
**Counter:** GLH's residue was explicitly reserved (`HANDOFF.md:1517`, "GLH
shrunk to the lower Volga + North Caucasus"), the line between "leftover" and
"seam" is drawn by this agent and nobody else, and the exact-count assert is
the *only* guard against these two rules (§E.2) — a seam this small is exactly
where a mis-set constant hides. Deferring both keeps the slice inside
`ural_region` proper.

**4. Novgorod's ten Yugra tributaries — strip, or leave?**
**Recommendation: STRIP ALL TEN by name** (`assert n_yugra_tribute == 10`,
§G.1). Vanilla drew the line for us: all ten subjects are trans-Ural and
Bjarmia has no tie. The first recorded Yugra expedition is 1096 [D], thirty
years after start, and stripping them leaves exactly the 1066 picture —
Novgorod holding the Dvina directly (its 63 northern locations stay) and taxing
nothing beyond the mountains yet. It costs four lines of code, moves no
constant, and cannot break the tributary gate check.
**Counter:** the PVL's 1096 entry reports a route as though established, which
is why the sources differ [D]; the Novgorod-Yugra tribute may well predate its
first mention, and EU5's tributary is a soft tie, not an occupation. And there
is an unmeasured mechanical reason to be careful: the build already ships NOV
as **KIE's** tributary while NOV holds these ten, so stripping them also
removes the project's only instance of a two-level tributary chain before
anybody has looked at what the engine does with one (**OWED CHECK 2**). Keeping
them and looking is a legitimate choice.

**5. GLM / GRS / NZH — leave, or retire the three (and GLH's `uren_province`
with them)?**
**(a) LEAVE ALL THREE** (recommended, §D.3): the ground is painted
`muscovite`/`orthodox` by Paradox, it sits in `russian_region` outside the
Finno-Ugric brief, and `RUS-STEPPE-PACKAGE.md:744` reserved it for the Volga
seam.
**(b) RETIRE ALL THREE + vacate 23, plus GLH's `uren_province` 8** (donor
table §E.2, Alt 3): 31 locations, 67 pops ≈ 37 log lines, ghosts 156 → 159,
`n_landless_deps` 280 → 281, parliament 1366 → 1362.
**Recommendation: (a).** **Counter, and it is a strong one:** Nizhny Novgorod
(1221), Gorodets (1152) and Galich-Mersky (1237) are *later* than the Vyatka
Land this package retires on exactly the same argument. Declining them is a
scope decision, not a historical one, and saying so now is cheaper than
discovering the inconsistency at the click tour. If the main session wants
internal consistency over scope discipline, (b) is fully costed above and needs
no further research.

**6. PRM's `starting_technology_level` — 3, or 2 like the tribes?**
PRM keeps 3 under the recommended design. The Baltic slice moved SXM 3 → 2 to
align it with its six new tribal siblings (`build_setup.py:3163-3165`,
"tech 3 -> 2 aligns it with them (package decision 8)"), and the nineteen
Siberian pop-countries all ship at **0**. A tribal Perm at 3 is technologically
level with Kyiv.
**Recommendation: LEAVE AT 3** — it is a live gameplay balance value, PRM is a
64-location settled forest polity rather than a nomadic band, and this package
has no measurement that justifies moving it. **Counter:** the SXM precedent is
exact and one token; leaving 3 makes PRM the only `eurasian_tribe` in the game
at a Rus tech level.

---

## Implementation checklist

Ordered so each step can be verified before the next. **Reproduce §E.2's donor
tables first — the delta-guard law makes that the review's job, not the
package's.**

1. **`FIELD_FIXES["PRM"]`** — the four surgeries of §B.1, appended to
   `build_setup.py:3089`ff. **Re-read the built block first** and confirm each
   `old_line` appears exactly once (`:6413` will say so loudly if not).
   `n_fields` in the build report rises by 4.
2. **`LOCATION_VACATED["VYT"] = ["vyatka_area", "lalsk_province"]`,
   `LOCATION_VACATED_EXPECT["VYT"] = 19`.** **Observe the resolved count**: the
   two names contain 23 ownable, four of which are PRM's and are excluded by
   the snapshot intersection at `:6217`. If it resolves 23, the intersection is
   not doing its job.
3. **`PERM_LANDLESS = ("VYT",)` into `LANDLESS_AFTER`** (`:2961`). The delta
   guard should stay silent. VYT's claims go 0 → **19**; verify the claims-backed
   guard (`:6301`) passes.
4. **Per OPEN DECISION 3** — `LOCATION_VACATED["GLH"] += ["ufa_province",
   "minusinsk_province"]`, `LOCATION_VACATED_EXPECT["GLH"] = 298`.
   **Observe it failing first at 291** (CLAUDE.md's rule), then move it. The
   raw resolves are 4 and 5; GLH holds 4 and 3.
5. **Per OPEN DECISION 4** — the ten named Yugra strips of §G.1, with
   `assert n_yugra_tribute == 10`. Place it beside the other named strips
   (`:7556`, `:7604`, `:7640`), **before** the landless sweep at `:7657`.
6. **Harness constants** — under the recommended design only ONE moves:
   `verify_mod.py:1244` parliament `min_count` **1366 → 1365** (VYT was landed
   and reached `estate_parliament`; PRM stays landed and reaches `assembly`
   through `eurasian_tribe`). **Verify, do not assume.** Everything else —
   `:288` 358, `:413` 179, `:843` 78, `:910` 9, `:937` 2411, `:1086` 125,
   `:1119` 2414, `167`/`174` 375 — stays put, and each was checked against the
   reason it would move.
7. **`build_setup.py:7745`, `:7775`, `:7036`** — `n_landless_deps` **280**,
   `n_pacts` **9**, `n_ghosts` **156**: all three **unchanged**, and all three
   are asserted, so a wrong assumption here fails the build rather than
   shipping.
8. **Optional, per decisions** — OPEN 1b's `_PERM_RULES` grant (drop step 2 and
   add the rule set + `LOCATION_GRANTS` extend); OPEN 2c's PRM vacate; OPEN 5b's
   three retirements (then ghosts 156 → **159** with `["GLM", "GRS", "NZH"]`
   added to `_expected_ghosts` at `:6989`, deps 280 → **281**, parliament
   1365 → **1362**); OPEN 6's tech token.

**Break-tests owed** (a check never seen failing is untested):

(a) a bogus province name in `LOCATION_VACATED["VYT"]` must abort at `:6213`
    ("is not a region/area/province in definitions.txt");
(b) **set `LOCATION_VACATED_EXPECT["VYT"] = 23` and watch `:6218-6221` abort
    with 19** — proving the snapshot intersection protects PRM's four;
(c) **set `LOCATION_VACATED_EXPECT["GLH"] = 300` and watch it abort with 298** —
    proving `minusinsk_province`'s two already-unowned members are excluded (the
    Tibet `zagya` case reproduced);
(d) omit `"VYT"` from `LANDLESS_AFTER` and watch the **delta guard**
    (`:6341`) fire — VYT is emptied by the vacate and nothing else would catch
    it;
(e) put one of VYT's nineteen into any `LOCATION_GRANTS` list and watch
    `:6223-6226` fire ("vacate and grant lists must be disjoint");
(f) misspell one PRM `old_line` and watch `FIELD_FIXES` abort at `:6413`
    ("appears 0x in PRM");
(g) set `n_yugra_tribute != 10` (drop one tag from the tuple) and watch the
    strip assert fire with 9;
(h) **the donor-table test the delta-guard law asks for**: add
    `"uren_province"` to `LOCATION_VACATED["GLH"]` without moving 298 → 306 and
    watch the count assert fire — **and confirm that the delta guard does NOT**,
    because GLH survives. That is the law's own demonstration, reproduced in
    this theater.

## Expected constant moves, collected

| constant | `file:line` | from | to (recommended) | to (all decisions maximal) |
|---|---|---|---|---|
| registry blocks | `zz_1066_new_countries.txt` | **74** | **74 — unchanged** | 74 |
| registry overrides | `MOD/in_game/setup/countries/` | 5 files | **5 — unchanged** | 5 |
| `NEW_COUNTRIES` | `build_setup.py:502` | current | **+0** | +0 |
| `LANDLESS_AFTER` | `:2961` | current | **+1** (VYT) | +4 (VYT GLM GRS NZH) |
| `FIELD_FIXES` | `:3089` | current | **+1 tag / 4 surgeries** (PRM) | +1 tag / 5 (with OPEN 6) |
| `LOCATION_GRANTS` | `:2978` | current | **+0** | +1 rule set (OPEN 1b, 23 locations) |
| `LOCATION_VACATED` | `:1265` | 9 tags | **10 (+VYT)**, and GLH's list +2 names | 13 (+GLM +GRS +NZH), GLH +3 names |
| `LOCATION_VACATED_EXPECT` | `:1273` | GLH **291**, TIB 7, CHI 113, CHG 21, +Danube 8 | **+`{"VYT": 19}`; GLH 291 → 298** | +`{"GLM": 11, "GRS": 6, "NZH": 6}`; GLH → 306 |
| locations vacated | build report | **599** | **625** (+26) | **664** (+65) |
| unowned locations | measured | **7,924** | **7,950** | 7,989 |
| locations granted | build report | current | **+0** | +23 (OPEN 1b) |
| `n_landless_deps` | `:7745` | **280** | **280 — unchanged, measured** | 281 (OPEN 5b's NZH→GRS) |
| named dependency strips | new, `:7556` shape | — | **10** (the Yugra ties) | 10 |
| `n_pacts` | `:7775` | **9** | **9 — unchanged, measured** | 9 |
| `n_ghosts` | `:7036` | **156** | **156 — unchanged, measured** | **159** (OPEN 5b) |
| empty-IO pin | `verify_mod.py:910` | **9** | **9 — unchanged** | 9 |
| `_MOD_TRIB_OVERLORDS` | `verify_mod.py:766` | 9 tags | **9 — unchanged** | 9 |
| tributary-gate `min_count` | `verify_mod.py:843` | **78** | **78 — unchanged** (NOV was never counted) | 78 |
| `CAPITAL_FIXES` | `:3016` | current | **+0** | +0 |
| `UNOWNED_GRANTS` | `:1919` | 3 tags / 19 locations | **unchanged — none needed** | unchanged |
| `CONTROL_STRIPS` | `:1705` | 1 tag | **unchanged** | unchanged |
| country blocks | `verify_mod.py:937`, `:1119` | **2411 / 2414** | **2411 / 2414 — unchanged** | unchanged |
| thrones | `verify_mod.py:288`, `:413` | **179** | **179 — unchanged** | 179 |
| new characters / dynasties | — | — | **0 / 0** | 0 / 0 |
| loc rows | `verify_mod.py:167`, `:174` | **375** | **375 — unchanged** | 375 |
| CoA references | `verify_mod.py:1086` | **125** | **125 — unchanged** | 125 |
| parliament `min_count` | `verify_mod.py:1244` | **1366** | **verify — expect 1365** | verify — expect 1362 |

**Nine of the twenty-six constants would move under the maximal reading; two
under the recommended one.** That is the honest shape of this theater.

---

## VERIFICATION

Per CLAUDE.md's say-what-you-verified rule.

- **Verified — the reader, with the FULL ten-key tuple.** `tools/build_setup.py`
  was imported (its `__main__` guard is at `:8141`) and its own `_parse_defs`
  (`:748`), `_ownable_set` (`:772`), `_defs` (`:809`), `_resolve_ruleset`
  (`:815`), `find_block_end` (`:5509`) and `COUNTRY_RE` (`:5562`) were used
  directly. `OWN_KEYS` was copied verbatim from `:5704-5707` — all ten members.
  The reader reproduces **20,922 ownable locations**, **2,337 vanilla and 2,411
  mod country blocks**, `samogitia_area` 16, `courland_province` 8, and — the
  `own_control_integrated` proof — **VTN 32, PLB 40, BTU 6, MGD 5, MUA 15, TIB
  59**, every one a published STATUS-band or §0.7 figure from an earlier
  package. Comments are masked length-preservingly before tokenising.
- **Verified — the pop parser.** `VAN/main_menu/setup/start/06_pops.txt` yields
  **28,559 location blocks / 50,227 `define_pop`** counting lowercase-only keys
  and **28,570 / 50,255** counting the eleven uppercase-containing keys — both
  of `TIBET-PACKAGE.md`'s figures reproduced exactly, which is what validates
  every pop number in this document. (First attempt used a one-tab-anchored
  regex and returned 50,255/50,255; the mismatch against the published figure
  caught it. Recorded because it is the anchor class again.)
- **Verified — `type = pop` is nineteen Siberian identities plus BJA/BSH/KRL,
  all zero-land.** `VAN/in_game/setup/countries/siberia.txt` enumerated;
  every tag's holdings measured at 0 in both trees; every block's `type = pop`
  line and `add_pops_from_locations` list read from
  `MOD/main_menu/setup/start/10_countries.txt` at the lines cited in §0.1.
  448 `type = pop` countries exist in the build game-wide.
- **Verified — VYT's republic.** `MOD/…/10_countries.txt:3108-3190`, quoted:
  `type = republic`, `heir_selection = veche_selection`, `reforms = {
  veche_republic }`, `republican_foundation_law = political_dynasties_policy`,
  `administrative_system = pyatina_policy`. Vanilla's identical block at
  `VAN/…/10_countries.txt:3387`. NOV's fixed block read at `MOD:1754` and
  `FIELD_FIXES["NOV"]` at `build_setup.py:3106-3113`.
- **Verified — PRM's principality.** `MOD/…/10_countries.txt:3192-3223`:
  `type = monarchy`, `heir_selection = cognatic_primogeniture`, `dynasty =
  rurikovich_dynasty`, `include = "limited_russian_principality"`,
  `tolerated_cultures = { udmurt }`, `capital = cherdyn`. Template read in full
  at `VAN/main_menu/setup/templates/limited_russian_principality.txt` — it
  declares **no `type =`**. `eurasian_tribe.txt` read in full.
- **Verified — the registries.** `VAN/in_game/setup/countries/russia.txt:309`
  (`PRM`: `culture_definition = komi`, `religion_definition = komi_paganism`),
  `:316` (`VYT`: `novgorodian` / `orthodox`), `:155` GLM, `:267` NZH, `:274`
  GRS, `:1` NOV — all read with `utf-8-sig` and an UNANCHORED regex (the BOM
  trap). The mod overrides neither `russia.txt` nor `siberia.txt`.
- **Verified — the rank and name lattice.**
  `country_name_construction.txt` read in full: the only government-gated
  branches are `:99-104` (`steppe_horde`) and the `type = pop`/empire branch;
  fallback `:183-186`; **zero `tribe` matches in the file**. Loc `:11-12` in
  `government_names_l_english.yml` gives `_map: "$NAME$"`.
  `country_ranks.txt` walked at duchy rank: `:1413` (tag-gated NOV), `:1423`
  `rank_duchy_republic`, `:1606` `rank_duchy_tribe`, `:1973`
  `rank_duchy_russian_prince` (`east_slavic_language`), `:2006` default. Loc
  `:693-696` "Republic"/**"Consul"**, `:790-792` "Tribe"/"Chief", `:1018-1022`
  "Minor Tribe"/"Chieftain", `:871-873` "Principality"/"Prince", `:482-485`
  "Tribal Kingdom"/"King". `komi = { language = permic_language }` at
  `VAN/in_game/common/cultures/permic.txt:1-2`.
- **Verified — the religion mismatch.** `komi_paganism`
  (`VAN/in_game/common/religions/folk_european.txt:224`, `group =
  folk_european_group`), `shamanism` (`folk_asian.txt:979`, `group =
  folk_asian_group`). Across all 20,922 ownable locations: `shamanism` 508,
  `erzya_religion` 9, `komi_paganism` / `samoyedic_paganism` / `obian_paganism`
  **0 each**.
- **Verified — diplomacy and IOs.** `MOD/…/12_diplomacy.txt:49` (NZH→GRS
  vassal), `:50-59` (the ten NOV tributaries), quoted in §0.6. `VYT` and `PRM`
  return **zero** word-boundary hits in `12_diplomacy.txt` and
  `15_international_organizations.txt` in both trees. `GLM`, `NZH`, `GRS` each
  appear once in the `autocephalous_patriarchate` instance at
  `MOD/…/15_international_organizations.txt:263-268`. `_MOD_TRIB_OVERLORDS` at
  `verify_mod.py:766-767` does not contain NOV.
- **Verified — the characters.** Every `tag =` line in both `05_characters.txt`
  files scanned: five characters name a theater tag, all five GLM's, earliest
  birth `1230.1.1` (`MOD:92055` / `VAN:92273`). `04_dynasties.txt` probed for
  seven `home =` locations in the theater: zero hits.
- **Verified — the vacate arithmetic.** 599 vanilla-owned→mod-unowned
  (reproducing `HANDOFF.md`'s constant), 9 vanilla-unowned→mod-owned (all SNH),
  7,334 + 599 − 9 = 7,924 = measured mod-unowned. The first-launch vacate
  (`LOCATION_VACATED["GLH"]` 284 + `["CHG"]` 21 = 305) carries **911
  `define_pop`** against the decoder's recorded ~504 lines
  (`EU5-ERROR-DECODER.md:675-685`) — ratio ≈0.55, so the one-line-per-pop model
  over-predicts. Only 8 of the 599 appear in `07_cities_and_buildings.txt`
  (1,108 entries). **The true filter is unidentified — OWED CHECK 3.**
- **Verified — tag freeness.** 16,226 vanilla and 70 mod text files scanned in
  the three-scan form; 2,320 registry tags indexed BOM-safe and unanchored.
  **`VYA` is Vyazma** (`russia.txt:169`, already in `RUS_LANDLESS`,
  `build_setup.py:1345`) and **`VYT` is Vyatka** (`russia.txt:316`, landed
  with 19) — the brief's hypothesis inverted. UDM VOT ZYR YUG BJR VTK KHL KOM
  MDV ERZ MKS free; MRI CHM ARS PCH PER MER BJA MAR taken.
- **Verified — zero double-ownership in `ural_region`** (194 locations tested
  for membership in more than one country block's `OWN_KEYS` set); game-wide the
  build has 4 (`saida ras_al_ain arshgul madinat_alawiyyin`) against vanilla's
  11.

**Historical claims — every one flagged.**

| claim | flag | note |
|---|---|---|
| The Vyatka Land is a Novgorodian colony of the late 12th century; the "Tale of the Vyatka Country" dates the settlement to 1174; Khlynov appears in Moscow chronicles 1374 | **[D]** | the Tale is a late compilation and its date is contested; archaeology puts Russian occupation 12th–13th c. Corroborated inside the repo by `CENTRAL-ASIA-PACKAGE.md:621` |
| The Vyatka veche republic proper is a 14th–15th-century object, annexed 1489 | **[D]** | |
| Perm the Great as a principality seated at Cherdyn is 15th-century; annexed by Moscow 1472 | **[D]** | |
| The Komi were christianised by Stephen of Perm, 1379–96 | **[D]** | bears on `komi_paganism` being right at 1066 |
| The Komi of the Vychegda and the Udmurts of the Cheptsa had no state in 1066 | **[U]** | no source in the repo; the agent's own history |
| Novgorod's first recorded Yugra expedition is the PVL entry under 1096 (Gyuryata Rogovich) | **[D]** | the entry reports the route as if established, which is precisely why sources differ on whether the tribute *begins* then |
| Bjarmaland is attested from Ohthere's voyage c.890 and Thorir Hund's raid 1026 | **[D]** | |
| Novgorod's Zavolochye/Dvina tribute is 11th-century | **[D]** | Sviatoslav Olgovich's tithe charter of 1137 names Dvina points; earlier reach is inference |
| Veliky Ustyug is founded 1147; Totma first mentioned 1137 | **[D]** | bears on NOV's `totma_area`, a closed seam |
| Nizhny Novgorod founded 1221 (Yuri Vsevolodovich); Gorodets c.1152 (Yuri Dolgoruky); Galich-Mersky first mentioned 1237/38 | **[D]** | corroborated inside the repo by `RUS-STEPPE-PACKAGE.md:744`, which gives 1152 / 1221 / 1237 |
| The Mari and Udmurts paid tribute to Volga Bulgaria rather than to any Rus principality in the 11th century | **[U]** | |
| The Bashkirs are attested on this ground from Ibn Fadlan's 922 embassy | **[D]** | |
| No 1066 Komi, Udmurt, Mari or Vyatka ruler is attested well enough to name | **[U]** | the strongest claim in §C, and the one a better-sourced session should re-test first |

**OWED CHECKS — three, all in-game, none answerable from any file.**

1. **What rank does the engine derive** for a 19-location VYT and a 64-location
   PRM with no `country_rank` line? It decides whether VYT reads "Republic"/
   "Consul" or the county-republic equivalent today, and whether a tribal PRM
   reads "Tribe"/"Chief" or "Minor Tribe"/"Chieftain" after. Inherited from the
   SEA and Tibet slices, still open.
2. **Does the engine accept a two-level tributary chain?** The build ships
   `KIE → NOV` and `NOV → {ten pop-countries}` simultaneously. Nothing in either
   tree settles it and no click tour has looked. Bears directly on OPEN
   DECISION 4.
3. **What actually filters the vacated-pop error class?** 911 `define_pop` on
   305 vacated locations produced ~504 lines; neither pop count, town presence
   nor `type = pop` coverage predicts it. Until it is known, every vacate's cost
   estimate in every package is a guess with a measured ceiling.
