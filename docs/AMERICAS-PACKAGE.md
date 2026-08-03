> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 40 (commit 32293c3) —
> NOT yet game-tested.** Research record, not the state. **The third
> consecutive zero-error package review** (all mechanical probes green —
> two review-probe regex artifacts, both the reviewer's own, resolved by
> direct read). Decisions, user-approved on the review's table:
> 1 NO Toltec tag, 2a TNC retired + island to TEP, 3a COC capital →
> chichen_itza + two strips, **4b CSU RETIRED into KKE — the review's own
> divergence from the package's low-confidence (a)**, on the TIB/Sakya
> evidence class (Manco Cápac b. 1170 is vanilla's own dating) and on
> KKE being vanilla's own archaeological pre-Inca Cusco tag, 5a TCP's
> vassalage stripped + tag kept, 6 the 3,948 unowned left. KNOWN
> DEVIATIONS, code wins: `AMERICAS_LANDLESS = ("TNC", "CSU")`, deps 281,
> parliament **1363** (both retirements), `_AMERICAS_RULES` carries the
> KKE rule from §E.2 Alt 2; **break-test (h) as specified was
> unfireable** — a vacate on a FOREIGN owner's ground resolves to zero
> through the snapshot intersection (itself a measured guard) — and was
> reproven in the proper shape (a vacate on the RECIPIENT's own ground
> fires the disjointness assert on the granted location). The §0.2
> loose-registry-regex finding went to KNOWLEDGE as a law.

# THE AMERICAS 1066 — a sealed hemisphere vanilla already got right; twenty locations and four lines are wrong (DRAFT)

**Research agent model ID: `claude-opus-5`.**

**DRAFT — pending main-session review. Nothing here has been written into any
mod file.** Produced by an Opus research agent, 2026-08-02, against the working
tree at HEAD `ee9dbf3` (39 items landed; constants read from the code, not from
prose: registry 74 blocks, country blocks 2411, thrones 179, landless-dep strips
280, pacts 9, IO ghosts 156, vacated 625, parliament min 1365, loc rows 375, CoA
125). Every mechanical claim carries a `file:line`. Historical claims that no
file can settle are flagged `[U]` (unverified — the agent's own history, no
source in the repo) or `[D]` (sources genuinely differ), never asserted
silently. §VERIFICATION collects them.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, 491,179 bytes, present)
`MOD = .../1066 Test Mod`

**Method — the Tibet and Perm/Vyatka method, applied unchanged.** No reader was
reimplemented. This package `import`s `tools/build_setup.py` (its `__main__`
guard is at `:8216`) and calls its own parsers: `_parse_defs` (`:748`),
`_ownable_set` (`:772`), `_defs` (`:809`), `_resolve_ruleset` (`:815`),
`find_block_end` (`:5560`) and `COUNTRY_RE` (`:5613`). Ownership is read with
the **full ten-member `OWN_KEYS` tuple copied verbatim from
`build_setup.py:5755-5759`** — `own_control_core, own_control_integrated,
own_control_conquered, own_control_colony, own_core, own_conquered,
own_integrated, own_colony, control_core, control`. Everything reads
`encoding='utf-8-sig'`; comments are masked length-preservingly before
tokenising. Scripts live in the session scratchpad (`amer.py`, `lib.py`,
`tagscan2.py`); nothing was written into the repo but this file.

**Proven on known positives BEFORE any new ground, including
`own_control_integrated` cases.**

| probe | expected (source) | measured |
|---|---|---|
| ownable locations | 20,922 (`TIBET-PACKAGE.md` §VERIFICATION) | **20,922** |
| vanilla country blocks | 2,337 | **2,337** |
| mod country blocks | 2,411 (`HANDOFF.md:1950`) | **2,411** |
| `samogitia_area` ownable | 16 (`BALTIC-PACKAGE.md`) | **16** |
| `courland_province` ownable | 8 (`BALTIC-PACKAGE.md`) | **8** |
| **VTN in vanilla** | **32** — the `own_control_integrated` proof | **32** |
| **PLB** | **40** | **40** |
| **BTU** | **6, not 1** | **6** |
| **MGD in vanilla** | **5, not 1** | **5** |
| MUA in vanilla | 15 | **15** |
| **TIB in vanilla** | **59** (`TIBET-PACKAGE.md` §0.7) | **59** |
| `06_pops.txt` blocks / `define_pop` | 28,559 / 50,227 lowercase-only; 28,570 / 50,255 with the 11 uppercase keys | **28,559 / 50,227** and **28,570 / 50,255** — both reproduced exactly |
| locations vacated by the build | **625** (`HANDOFF.md:1953`) | **625**, and the ledger closes: vanilla-unowned 7,334 + 625 vacated − 9 that gained an owner (all SNH's, `UNOWNED_GRANTS`) = **7,950 = the mod's measured unowned total** |
| vanilla identity tags | **2,340** (`CLAUDE.md`, "Vanilla's 2340 identity tags") | **2,340** — but only after the registry regex was fixed; see §0.2 |

**Scope.** The `america` continent (`definitions.txt:5880`), both
sub-continents, **fourteen regions**: `canada_region caribbean_region
east_coast_region great_plains_region mesoamerica_region
central_america_region aridoamerica_region alaska_region west_coast_region`
(north_america) and `colombia_region brazil_region andes_region chaco_region
la_plata_region` (south_america). **4,441 ownable locations, 6,159
`define_pop`, 493 locations owned by 223 tags, 3,948 unowned, ZERO
double-ownership, ZERO tags straddling the hemisphere.** `greenland_area` is
deliberately OUT of scope — `definitions.txt` files it under
`north_atlantic_islands_region` / `western_europe`, not under `america` (§0.8).

---

## 0. Ground truth — nine findings, and eight of them say "leave it alone"

### 0.1 THE HEADLINE: the Americas is the largest "already right" finding in the project, by an order of magnitude

**The mod has never touched a single American tag.** Measured directly: zero
American-registry tags appear on any non-comment line of `tools/build_setup.py`,
and zero appear anywhere in `tools/verify_mod.py`. Vanilla ownership and mod
ownership of all 4,441 American locations are **byte-for-byte identical** — the
same 223 tags hold the same 493 locations in both trees, and no American tag is
in `LANDLESS_AFTER`, `LOCATION_GRANTS`, `LOCATION_VACATED`, `FIELD_FIXES`,
`CAPITAL_FIXES` or `UNOWNED_GRANTS`.

And the reason nothing needed touching is structural:

| what | measured |
|---|---|
| ownable locations | **4,441** (21.2% of the game's 20,922) |
| **unowned** | **3,948 — 88.9%** |
| owned | 493, by 223 tags |
| `define_pop` on American ground | **6,159** (1,751 on owned land, 4,408 on unowned) |
| identity blocks in the eleven American registry files | **544** |
| of those, **landless `type = pop` countries** | **321 — every single landless one** |
| `type = pop` countries game-wide | **448** — so **72% of vanilla's entire stateless model is American** |
| dependency lines naming an American tag, whole hemisphere | **4** |
| pact (`scripted_mutual`/`scripted_oneway`) lines | **0** |
| American tags in the mod's `15_international_organizations.txt` | **0** |
| double-ownership | **0** |

**Seven of the fourteen regions have ZERO owned locations at all** —
`canada_region` (573), `caribbean_region` (111), `brazil_region` (499),
`la_plata_region` (155), `chaco_region` (121), `alaska_region` (316),
`west_coast_region` (357). That is 2,132 ownable locations, 2,166 pops, entirely
stateless by Paradox's design, and correct at 1066 exactly as it is at 1337.

This is the Perm/Vyatka shape — "vanilla already ships the stateless north,
complete" (`PERM-VYATKA-PACKAGE.md` §0.1) — at **twenty times** the scale: 321
pop-country identities against Siberia's nineteen.

### 0.2 A METHOD FINDING FIRST, because it changed four American answers: the strict registry regex misses 94 of vanilla's 2,340 identity blocks

`PERM-VYATKA-PACKAGE.md` §A.2 reports "2,320 registry tags indexed" over both
trees. That is **2,246 vanilla + 74 mod**, and 2,246 is what an
`^([A-Z0-9]{2,6}) = \{` regex returns. `CLAUDE.md` says vanilla ships **2,340**.
The gap is **94 blocks** whose declaration is not `TAG = {`:

- **92 use two or more spaces** — `HIR  = {` (`VAN/in_game/setup/countries/central_north_america.txt:125`), `ZIP  = {` (`colombia.txt:11`), `SFA  = { ` (`east_africa.txt:41`) …
- **2 use a tab** — `HNV`, `YDR` (`india.txt`).

A loose `^([A-Z0-9]{2,6})[ \t]*=[ \t]*\{` returns **2,340 vanilla / 2,414
mod-visible**, reproducing `CLAUDE.md`'s constant and `verify_mod.py:1119`'s
`min_count = 2414` exactly.

**Four of the 94 are American: `HIR` (Hiraaca), `ZAC` (Zacatecah), `ZAI`
(Zaín), `ZIP` (Muyquyta).** ZIP is a **landed** tag holding five
`colombia_region` locations, and under the strict regex it reported as "holds
American land but has no registry entry" — a phantom of exactly the class
`KNOWLEDGE.md` records for `^`-anchored-with-BOM and one-line blocks. The
earlier packages' word-boundary scans would still have shown a collision by
count, so no published freeness verdict is wrong; but their **registry `file:line`
column is blind to 94 tags**, and this is the fourth incident in the anchor
class. Every registry number in this document uses the loose form.

### 0.3 THE SECOND HEADLINE: the creation-date law already answered North America's biggest question, months ago and silently

`VAN/main_menu/setup/start/15_international_organizations.txt:757-761`:

```
	add_international_organization = {
		type = tribal_confederation
		creation_date = 1142.1.1
		members = { ONO KKA ONY GYO ONN }
	}
```

**That is the Haudenosaunee League — the Five Nations — and vanilla dates it to
1142.1.1, seventy-six years after our start.** The build's future-dated-IO
strip (`build_setup.py:6849-6863`, `creation_date >= START_DATE`, assert
`removed != 17` at `:7172`) deleted it along with the other sixteen. Measured in
the current build: **zero American tags appear anywhere in
`MOD/main_menu/setup/start/15_international_organizations.txt`**, in any
`members` / `free_city` / `elector` list.

So on 1066.9.15 the Mohawk (KKA, 11), Oneida (ONY, 6), Seneca (ONN, 4), Cayuga
(GYO, 3) and Onondaga (ONO, 3) stand as **five independent tribes with no
league** — which is what every reading of the confederacy's date supports,
whether one takes 1142 [D, the astronomical argument] or the mainstream c.
1450-1600 [D]. Nobody had to decide anything, and nobody wrote it down.

The other `tribal_confederation` instance (`:762-766`, `creation_date =
1337.1.1`, `members = { AFR SDQ }`) went the same way.

**This is the TIBET §0.2 finding repeated in another hemisphere, and it is the
package's cheapest win: the North American diplomacy correction is already
shipped.**

### 0.4 THE THIRD HEADLINE: Cahokia is a full country, and 1066 is the RIGHT date for it — vanilla's own DHE even lands the sunset correctly

`MOD/main_menu/setup/start/10_countries.txt:56253` (`VAN:60930`), registry
`VAN/in_game/setup/countries/eastcoast.txt:367`:

**CHK "Cahokia" holds 23 locations** — `illinois_area` and `missouri_area`
mostly, plus `iowa_area` — carrying **77 `define_pop`**, with its **own culture
(`cahokia_culture`, 14 locations game-wide), its own religion
(`mississippian_ceremonial`, 461 locations), its own court language
(`dhegiha_language`), `capital = cahokia`, `starting_technology_level = 1`,
`type = tribe`, a `reforms = { agricultural_cultivation }` block, thirteen
sliders, thirteen privileges, a ten-area `discovered_areas` block and four
`tolerated_cultures`.** It is the most fully-realised non-Mesoamerican country
in the hemisphere, and it declares no template include at all — the block is
entirely inline.

At 1337 Cahokia is a ruin: the site depopulates c. 1350-1400 with major decline
from c. 1200 [D]. **At 1066 it is at or within a generation of its peak** — the
"Big Bang" c. 1050, Monks Mound built c. 1050-1100 [both D].

And vanilla's own flavour agrees. `VAN/in_game/events/DHE/flavor_CHK.txt` is
**23 events, 22 of them `dynamic_historical_event` blocks tagged CHK**, and the
first is `flavor_chk.1`, **"The Sunset of Cahokia"**, window `from = 1337.1.1 to
= 1356.1.1`. The remaining 21 run to 1437.

**So a 1066 start gives Cahokia a 271-year arc that begins at its peak and ends,
on vanilla's own schedule, roughly where the archaeology puts the abandonment —
which is a better fit than the date Paradox wrote it for.** Nothing to do. This
is the strongest "our date improves vanilla" finding the project has recorded.

### 0.5 The fourth finding: exactly FOUR dependency lines exist in the whole hemisphere, and all four are post-1066

`MOD/main_menu/setup/start/12_diplomacy.txt` (265 dependency lines, 28 pact
lines total). Every line naming an American tag:

```
:226  dependency = { first = TEP second = TNC subject_type = vassal }   # VAN:515
:227  dependency = { first = TEP second = TCP subject_type = vassal }   # VAN:516
:402  dependency = { first = COC second = XIU subject_type = vassal }   # VAN:815
:403  dependency = { first = COC second = HEL subject_type = vassal }   # VAN:816
```

| line | what it models | 1066 verdict |
|---|---|---|
| TEP → TNC | Azcapotzalco's overlordship of the Mexica | **TENOCHTITLAN DOES NOT EXIST.** Founded 1325 [D]; the Tepanec hegemony over the lake cities is c. 1370-1428 [D] |
| TEP → TCP | Azcapotzalco over Tlacopan/Tacuba | The town may be older [U]; its Tepanec vassalage is the same 14th-century object [D] |
| COC → XIU | Cocom of Mayapán over the Tutul-Xiu | **THE MAYAPÁN LEAGUE**, c. 1220-1441 [D]. XIU's capital is `mani`, a seat that exists only after the league's fall in 1441 [D] |
| COC → HEL | Cocom over Chel | Chel (Ah Chel) is one of the sixteen *cuchcabalob* that appear AFTER 1441 [D] |

**Mechanically all four are free of every gate.** The tributary visible-gate
check reads only `subject_type = tributary` lines whose overlord is a new tag or
in `_MOD_TRIB_OVERLORDS = {FRA, LEI, TYR, TRY, MCM, PAP, KIE, LIA, PLB}`
(`verify_mod.py:766-771`) — these are `vassal`, and neither TEP nor COC is in
the set. `min_count = 78` (`:843`) cannot move whatever is done to them.

### 0.6 The fifth finding: the theater has ZERO seatable rulers, and vanilla's own character data dates the Inca founder to 104 years after our start

Every one of the 7,875 blocks in `MOD/main_menu/setup/start/05_characters.txt`
(7,736 in vanilla's) was parsed for `tag =`. **Forty-seven name an American tag.
The EARLIEST birth date is 1170.1.1** — `csu_manco_qhapaq` (Manco Cápac,
`hurin_qusqu_dynasty`, death 1230.1.1), then `csu_sinchi_ruqa` 1200,
`tar_pauacume_uanacaze` 1220, `csu_lluqi_yupanki` 1240, and everything else
1250-1336. **The Mexica set (`azt_tenoch` 1299, `azt_acamapichtli_tenochcatl`
1336) and the Purépecha set (`tar_tariacuri_uanacaze` 1336.8.1) are the latest.**

That is 104 years emptier than Perm/Vyatka's 1230 and 195 years emptier than
Tibet's 1261. Nineteen dynasties are homed on American locations
(`04_dynasties.txt`: `azcapotzalco calkini cempoala culhuacan dzilam huexotzinco
mani mayapan noh_peten patzcuaro pisaq pismachi qusqu tenochtitlan tetzcoco
xaltocan yucucui`), all of them late houses.

**This package seats NOBODY. Thrones stay at 179.** The Cadalus honest-silence
rule applies without a single borderline case: there is no attested individual
anywhere in the western hemisphere on 1066.9.15 whose name a source in this repo
could supply, and none this agent can name [U]. That is not a gap in the
research — it is what the sources are.

**`csu_manco_qhapaq`'s `birth_date = 1170.1.1` is vanilla's own testimony that
the Inca ruling line begins after our start**, and it is the single most useful
dated object in the theater (§D.4).

### 0.7 The sixth finding: the render lattice is the RICHEST in the game, and it needs nothing

Unlike Tibet — where `country_ranks.txt`'s 2,741 lines contained no Tibetan word
at all — the Americas carry a **complete native title system**, and it is
culture- and language-gated, the African-lattice shape rather than the tag-gated
one.

`VAN/in_game/common/customizable_localization/country_ranks.txt` is one
first-match list, `country_flavor`, running `:1`-`:2556` (its first line is
BOM-hidden from a `^`-anchored grep — `KNOWLEDGE.md`'s law again), with
`rank_county` as the fallback at `:2553-2555`.

| branch | line | trigger | loc (`government_names_l_english.yml`) |
|---|---|---|---|
| `rank_county_republic_maya` | `:118` | county + republic + `court_language ?= language:maya_language` | `:1039-1041` "$rank_county_kuchkabal$" / **"Batab"** |
| `rank_empire_inca` | `:345` | empire + `culture.language = language:quechuan_language` | `:221-223` "$rank_empire$" / **"Sapa Inca"** / "Coya" |
| `rank_empire_nahua` | `:590` | empire + `culture_group:nahua_group` | `:264-266` **"Huēyi Tlahtohcāyōtl"** / **"Huēyi Tlahtoāni"** |
| `rank_kingdom_maya` | `:719` | kingdom + maya court language | `:339-341` **"K'uhul Ajawil"** / **"K'uhul Ajaw"** |
| `rank_kingdom_inca` | `:1173` | kingdom + quechuan | `:575-577` "$rank_kingdom$" / **"Inca"** |
| **`rank_duchy_ajawil`** | **`:1320`** | duchy + maya court language | `:719-721` **"Ajawil"** / **"Ajaw"** |
| **`rank_duchy_irechikwa`** | **`:1332`** | duchy + `purepecha_language` | `:723-725` **"Iréchikwa"** / **"Irecha"** |
| `rank_duchy_tribe_haudenosaunee` | `:1596` | duchy + tribe + `culture_group:haudenosaunee_group` | `:786-788` "$rank_duchy_tribe$" / **"Royaner"** / "Iakoianes" |
| `rank_duchy_tribe` | `:1606` | duchy + tribe | `:790-792` "Tribe" / "Chief" |
| `rank_duchy_inca` | `:1917` | duchy + quechuan | `:847-849` "$rank_duchy$" / **"Inca"** |
| `rank_duchy_aymara` | `:1926` | duchy + aymara | `:852-853` "$rank_duchy$" / **"Cinchi"** |
| `rank_duchy_nahua` | `:1990` | duchy + nahua group | `:875-877` **"Tlahtohcāyōtl"** / "Tlahtoāni" |
| `rank_county_tribe_haudenosaunee` | `:2269` | county + tribe + haudenosaunee | `:1014-1016` **"Clan"** / "Royaner" |
| `rank_county_theocracy_maya` | `:2160` | county + theocracy + maya | `:1034-1036` "$rank_county_kuchkabal$" / **"Ah K'in"** |
| **`rank_county_kuchkabal`** | **`:2385`** | **maya court language, NO rank test** | `:915-917` **"Kuchkabal"** / **"Halach Winik"** |
| `rank_county_iya` | `:2392` | eastern_otomanguean or otopamean court language | — |
| `rank_county_inca` | `:2459` | county + quechuan | `:1193-1195` "$rank_county$" / **"Auqui"** |
| `rank_county_nahua` | `:2497` | county + nahua group | `:1043-1045` **"$altepetl$"** = "Āltepētl" / **"Tlahtoāni"** / "Cihuātlahtoāni" |
| `rank_inca_heir` / `rank_maya_heir` | `:2610` / `:2628` | heir block | "Auqui" / "B'aah Ch'ok" |

**And the name side is the simplest possible.**
`country_name_construction.txt` is 188 lines, first-match, read in full. Its
gated branches name `ROM BYZ PAP GBR MAM DAU PAL MAL HBURG BGIRO TIM GLH CHG LAT
PLC HSA KNI ARA CAS POL BOH`, `culture:frisian`, `religion_group:muslim`,
`government_type` republic/monarchy/`steppe_horde`, a Chinese court-language
branch, and `country_type = pop` (`:154`). **Not one reaches an American tag
except the `type = pop` branch.** Everything else lands on the fallback
`country_name_construction_prefix_rank_of_name` (`:183-186`, `fallback = yes` at
`:185`), whose `_map` string is **`"$NAME$"`**
(`government_names_l_english.yml:11-12`).

**THE LAW for this theater: every landed American country's map label is its
NAME key verbatim.** No adjective trap, no horde trap, no tag-gated trap. The
321 `type = pop` countries take the `:116-157` adjective branch, as vanilla
intends.

Court languages are declared **inline in 202 of the 223 landed blocks** —
`nahuatl_language` 84, `maya_language` 31, `otopamean_language` 30,
`quechuan_language` 15, `aymara_language` 9, `purepecha_language` 6,
`totozoquean_language` 6, `tanoan_language` 5, `keres/chicham/muchik` 3 each,
`dhegiha/quingnam/cariban/cuitlatec/tayrona` 1 each, `chibchan_language` 2, and
21 declare none. **Only TWO of the 223 declare a `country_rank`** — ITZ and TAR,
both `rank_duchy` — so 221 leave it to the engine, the same convention Tibet
measured (21 of 22).

**Consequence: TAR renders "Iréchikwa of Purépecha" under an "Irecha", COC and
ITZ render "Ajawil" under an "Ajaw", the Nahua altepetl render "Āltepētl" under
a "Tlahtoāni", the Aymara señoríos under a "Cinchi", the Five Nations under a
"Royaner".** This is the best-served theater in the game for native titles, and
there is nothing to fix, bank or override.

One live oddity, recorded not fixed: **`wari_culture` maps to
`quechuan_language`** (`VAN/in_game/common/cultures/peruvian.txt:693`), so the
eleven `wari_culture` monarchies (AYA CUI PCR MYM ANI HCH PCO PIG SRA CNC and
kin) reach `rank_duchy_inca` (`:1917`) and render their rulers **"Inca"** —
275 years before the Inca. The tribe branch at `:1606` fires first for
tribe-government tags, so `andean_tribe` riders (KKE, MYM) escape it. It is
vanilla's condition at 1337 too and it is a POP/culture-pass matter, not a 1066
one (§H).

### 0.8 The seventh finding: the hemisphere is SEALED — one sea zone is the only link, and it grants nothing

The brief's "effectively no seams" is confirmed, with one qualification worth
recording precisely.

| probe | result |
|---|---|
| tags holding land on BOTH sides of the Atlantic | **0** (every one of the 223 holds only American land) |
| dependency lines crossing the hemisphere | **0** (all four are American-to-American) |
| pact lines naming an American tag | **0** |
| IO instances with an American member, in the MOD build | **0** |
| setup templates naming an American region or area | **9** — `american_east_coast_tribe`, `amerindian_tribe_settled`, `caribbean_tribe`, `expl_amerindian_east_coast`, `expl_andean`, `expl_aridoamerica`, `expl_mesoamerica`, `expl_northwestern_america`, `expl_southamerica`. **All nine are themselves American templates.** No Old World template grants American discovery |
| NON-American country blocks with inline American discovery | **exactly ONE — `GRL`** |

**GRL "Greenland"** (`VAN/in_game/setup/countries/_scandinavia.txt:134`) holds
twelve `greenland_area` locations (`gardr brattahlid dyrnes hvalsey einarsfjord
vatnahverfi herjolfsnes petursvik lundey altafjord ketilsfjord siglufjord`, all
`icelandic`/`catholic`) and declares `discovered_areas = { labrador_sea_area }`.
`labrador_sea_area` sits in `canada_region` and contains **zero ownable
locations** — it is water. `greenland_area` itself is filed under
`north_atlantic_islands_region` / `western_europe`, i.e. **outside the `america`
continent**, so it is not this package's ground.

**So the only Old World → New World link in the entire build is one Norse
country's knowledge of one stretch of sea.** It grants no land, no claim, no
diplomacy, and it is a rather good 1066 detail on its own terms (the Greenland
colony is founded 985 and the Vinland voyages are c. 1000 [both D]). Labrador
(37 ownable, `dorset_culture`/`innu_culture`) and Newfoundland (27,
`beothuk_culture`) are **100% unowned in both trees** — and Dorset occupation of
Labrador at 1066 is more correct than at 1337, the Thule displacement being c.
1200-1400 [D].

### 0.9 Ownership, culture, religion and pops — measured per region, in the CURRENT build

Ownable counts from `definitions.txt` via `_defs`; culture/religion from
`location_templates.txt`; owners from `MOD/main_menu/setup/start/10_countries.txt`
with the full ten-key reader; `define_pop` from `VAN/.../06_pops.txt`.

| region | ownable | pops | owned | tags | principal holders |
|---|---|---|---|---|---|
| `mesoamerica_region` | **325** | 1,065 | **301** | ~150 | TAR 19, COC 12, MIX 8, CLM 7, XOL 6, HEL 6, TEO 5, CKP 5, ZAP 5, … (the altepetl swarm: most hold 1-4) |
| `andes_region` | **375** | 675 | **95** | 34 | CYA 10, PCJ 7, CRA 5, XLL 5, HNK 5, CUI 4, AYA 4, CHM 4, SUR 4, … |
| `east_coast_region` | **628** | 925 | **36** | 6 | KKA 11, **CHK 9**, ONY 6, ONN 4, GYO 3, ONO 3 |
| `central_america_region` | **124** | 219 | **22** | 9 | KUS 4, ITZ 4, CHT 4, KIC 3, QUA 2, KAQ 2, TZU/MMM/QAN 1 |
| `great_plains_region` | **358** | 431 | **14** | 1 | **CHK 14** |
| `aridoamerica_region` | **292** | 395 | **13** | 11 | XCT 2, XOC 2, and eight one-location Rio Grande pueblos |
| `colombia_region` | **207** | 233 | **12** | 3 | ZIP 5, ZAQ 4, TAI 3 |
| `canada_region` | 573 | 564 | **0** | 0 | — |
| `brazil_region` | 499 | 502 | **0** | 0 | — |
| `west_coast_region` | 357 | 357 | **0** | 0 | — |
| `alaska_region` | 316 | 308 | **0** | 0 | — |
| `la_plata_region` | 155 | 193 | **0** | 0 | — |
| `chaco_region` | 121 | 131 | **0** | 0 | — |
| `caribbean_region` | 111 | 111 | **0** | 0 | — |
| **total** | **4,441** | **6,159** | **493** | **223** | |

**Pop density is the lowest of any theater the project has measured: 1.39 pops
per location** (Tibet 3.5, Perm/Vyatka 2.6). Owned American land runs 3.55, the
3,948 unowned locations 1.12. **A vacate here would be the cheapest anywhere —
which is exactly why the package proposes none: there is nothing to empty.**

**1,853 of the 3,948 unowned locations are covered by some pop-country's
`add_pops_from_locations`** (game-wide only 3,735 locations are so covered, so
**half of vanilla's entire pop-country coverage is American**). The uncovered
2,095 carry 2,150 pops and are vanilla's own untouched wilderness — the same
class as the 4,515 uncovered locations Perm/Vyatka measured game-wide.

Registry health: of the 544 American identity blocks, **three name a
`culture_definition` that sits on zero of the 20,922 locations** — CLM
`teco_culture` (`mesoamerica.txt:383`, **landed**, 7 locations), HLK
`heiltsuk_culture` (`westcoast.txt:167`, landless), TWK `tawakoni_culture`
(`central_north_america.txt:277`, landless). **Zero name a `religion_definition`
on zero locations.** That is a far healthier registry than Perm/Vyatka's eleven
Uralic religions on zero ground.

---

## A. Registry

### A.1 What already exists and needs nothing

| what | where | measured | verdict |
|---|---|---|---|
| **544 American identity blocks** | eleven files: `mesoamerica.txt` 180, `eastcoast.txt` 102, `andes.txt` 74, `central_north_america.txt` 45, `aridoamerica.txt` 39, `colombia.txt` 31, `canadian.txt` 22, `westcoast.txt` 20, `brasil.txt` 15, `centralamerica.txt` 11, `chaco.txt` 3 | 223 landed, 321 landless | **NOTHING NEEDED.** No override, no addition |
| **321 landless `type = pop` identities** | all eleven files | every one carries `type = pop` in its `10_countries` block; **zero exceptions** | Vanilla's legitimate stateless class, at 17× the Siberian scale |
| **HTS "Hisatsinom"** — the Ancestral Pueblo | `aridoamerica.txt:326`, `ancestral_pueblo_culture` | 0 locations, 4 pop-locations; `ancestral_pueblo_culture` on **7 locations, all unowned** | **The Chaco answer is already shipped.** §D.6 |
| **HHK Hohokam / HOP Hopi / ZNI Zuni** | `aridoamerica.txt:92 :146 :164` | 0 / 8, 0 / 4, 0 / 4 | same |
| **CHK Cahokia** | `eastcoast.txt:367` | 23 locations | §0.4 — **the theater's best object, and 1066 is its date** |
| **the five Haudenosaunee nations** | `eastcoast.txt` | KKA 11, ONY 6, ONN 4, GYO 3, ONO 3 | §0.3 — league already deleted by the creation-date strip |
| **the eight Rio Grande pueblos** ACO ISL KER OHK TAO TEY TNN TST | `aridoamerica.txt` | 1 location each, `keres`/`tanoan` + `kachina_religion` | Continuously occupied at 1066 and at 1337 [D]. **Untouchable and correct** |
| **CHM "Chimu"** | `andes.txt:11`, `chimu_culture`, `capital = chan_chan` | 4 locations | Chan Chan is founded c. 850-900 [D]; a four-location early Chimor is a defensible 1066 |
| **the Aymara señoríos** PCJ QUL LUP KRK KNA SUR UMA CRA | `andes.txt`, `aimara_culture`, `capital`s at Axawiri/Hatunqulla/Chucuito | 25 locations in `qullaw_area`, and **`tiwanaku` itself is PCJ's** | Tiwanaku collapses c. 1000-1100 [D]; Aymara señoríos over the same ground is the only model vanilla ships and the right one at 1066 |
| **TAR "Purépecha"** | `mesoamerica.txt`, `country_rank = rank_duchy`, `purepecha_language` | 19 locations, capital `tzintzuntzan` | The Uacúsecha dynasty is 13th-century [D] and its own vanilla characters start 1220 — but the tag is a PEOPLE, the render is "Iréchikwa"/"Irecha", and Michoacán was inhabited. §H |

**No new registry block and no registry override is proposed under the
recommended design.** Registry stays at **74**, overrides stay at **five files**
(`east_asia.txt`, `horn_of_africa.txt`, `iberia.txt`, `italy.txt`,
`west_africa.txt`). `mesoamerica.txt`, `andes.txt`, `eastcoast.txt` and the
other eight American files are **NOT overridden and must not be** — the Gallura
cost stays unpaid, as in Tibet and Perm/Vyatka.

### A.2 Freeness of the candidates — three scans each, run for the tags this package REFUSES as much as for any it proposes

Method per `TIBET-PACKAGE.md` §A.2 / `PERM-VYATKA-PACKAGE.md` §A.2: (1)
word-boundary `\bTAG\b` over the whole vanilla tree, non-localisation and
English-localisation counted separately; (2) **substring** `_TAG\b|\bTAG_` over
the same tree; (3) both over the whole mod repo. Text files only
(`.txt .yml .gui .info .asset .gfx .py .md .json .mod .csv .log .settings`) —
`KNOWLEDGE.md`, "Tag-freeness sweeps MUST exclude binaries". Registry index read
`utf-8-sig` over BOTH `in_game/setup/countries/` trees, **unanchored and with
the loose whitespace form of §0.2**. **16,226 vanilla files and 71 mod files
scanned; 2,414 registry tags indexed.**

| candidate | VAN word | VAN en-loc | VAN sub | MOD word | MOD sub | registry | verdict |
|---|---|---|---|---|---|---|---|
| **TOC** (TOlteCa) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **TLC** (ToLteCa) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **TCA** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **XTL** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **CZA** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **MYP** (Mayapán) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **TLT** | 23 | 1 | 48 | 2 | 18 | `VAN:mesoamerica.txt:1260` | **TAKEN** — Tlacotlalpan, one location away in the same region |
| **TUA** | 22 | 1 | 48 | 2 | 18 | `VAN:central_north_america.txt:246` | **TAKEN — and it is the brief's trap: `TUA` IS named "Tula", but it is the CADDOAN Tula of Arkansas, a landless `type = pop` country, not Toltec Tollan** |
| **TUL** | 35 | 1 | 60 | 3 | 30 | `VAN:france.txt:452` | **TAKEN** — Toulouse |
| **TOL** | 0 | 0 | 1 | 12 | 4 | `MOD:zz_1066_new_countries.txt:40` | **TAKEN — by this mod's own new-tag file.** Free in vanilla, gone here |
| **TLN** | 22 | 1 | 48 | 2 | 18 | `VAN:andes.txt:38` | **TAKEN** — Tallan, a Peruvian coastal tag |
| **CHZ** | 24 | 1 | 50 | 5 | 19 | `MOD:east_asia.txt:1132` | **TAKEN** — Chinese |
| **CHN** | 25 | 1 | 48 | 6 | 18 | `VAN:lowlands.txt:55` | **TAKEN** |
| **KUK** | 21 | 1 | 48 | 1 | 18 | `VAN:maghreb.txt:60` | **TAKEN** |
| **MAY** | 17 | 1 | 67 | 1 | 12 | **none** | **TAKEN, EMPTY REGISTRY — the PRU class.** `MAY: "Maya"` (`country_names_l_english.yml:914`), `MAY_f` (`00_formable_countries.txt:3866`, `formable_countries_l_english.yml:115`) |
| **AZT** | 25 | 3 | 105 | 0 | 13 | **none** | **TAKEN, EMPTY REGISTRY.** `AZT: "Aztecs"` (`:2491`), `AZT_f` (`:4763`), `country_AZT.txt` advances, `flavor_AZT.txt` (17 events) |
| **INC** | 28 | 2 | 94 | 0 | 12 | **none** | **TAKEN, EMPTY REGISTRY.** `INC: "Inca"` (`:4678`), `INC_f` (`:3332`), `country_INC.txt` advances |
| TNC / TCP / COC / CSU / KKE / CHK / HTS | 52 / 23 / 30 / 64 / 24 / 45 / 8 | — | — | — | — | `mesoamerica.txt:56 :95 :1442`, `andes.txt:92 :572`, `eastcoast.txt:367`, `aridoamerica.txt:326` | **TAKEN, all landed or `type = pop` — the tags this package discusses** |

**Three empty-registry PRU-class tags live in this hemisphere (MAY, AZT, INC),
which is more than anywhere else in the game.** They are the formable
identities, and any future American slice that reaches for an obvious mnemonic
must scan first.

### A.3 New blocks — NONE under the recommended design

No `NEW_COUNTRIES` entry (`build_setup.py:502`), no colour, no CoA, no loc row.
The one candidate that survived measurement — a Toltec Tollan — is costed in
full in §E.3 and refused in OPEN DECISION 1.

**Colour note for whoever overturns that.** `map_toltec`
(`VAN/main_menu/common/named_colors/02_map.txt:1420`, `rgb { 38 145 6 }`) exists
and is used by **no country** — it is `toltec_culture`'s own key
(`in_game/common/cultures/mesoamerican.txt:367`). **It is the `map_tibetan`
class and must NOT be written onto a country** (`TIBET-PACKAGE.md`
implementation checklist step 2, "never write `map_tibetan`"). A new Toltec tag
needs a NEW key; `map_TOC` and `map_TLC` are both absent from vanilla's 3,742
`map_*` definitions, proven by the substring column above returning 0.

---

## B. The country blocks

### B.1 `CAPITAL_FIXES` — one entry, the cheapest correction in the package

`CAPITAL_FIXES` (`build_setup.py:3050`, 31 entries) is applied per tag with an
exact-old-value assert (`:6431-6444`, `sys.exit("CAPITAL_FIXES: capital
{old_cap} not found in {_t}")`).

```python
    "COC": ("mayapan", "chichen_itza"),  # Mayapan is founded c. 1180-1220 [D]
                                         # and its league is 1220-1441; at 1066
                                         # the Yucatan hegemon is Chichen Itza,
                                         # which COC already holds. One token.
```

Verified against the built block (`MOD/main_menu/setup/start/10_countries.txt:41121`):

```
	COC = {
		own_control_core = {
			mayapan sotuta hocabail hunucma maxcanu motul
			 chichen_itza zaci tases kalotmul
			jootsuuk tho
		}
		include = "amerindian_advanced_monarchy_not_nahuatl"
		include = "expl_mesoamerica"
		government = { type = monarchy  heir_selection = cognatic_primogeniture  ruler = random }
		court_language = maya_language
		capital = mayapan
		dynasty = cocom_dynasty
	}
```

`capital = mayapan` occurs exactly once; **`chichen_itza` is already COC's**, so
the orphan-capital guard (`:6754-6783`, `if held and capm.group(1) not in held`)
stays silent by construction. **Zero territory moves. Zero constants move.**

The tag's NAME key stays "Cocom" and the map label stays "Cocom" (the §0.7 law).
That is defensible — the Cocom claimed descent from the Itzá of Chichén [D] —
and a rename is banked, not proposed (OPEN DECISION 3's counter).

### B.2 TNC — no field surgery, because the tag itself is the anachronism

`MOD/main_menu/setup/start/10_countries.txt:38503` (`VAN:43094`), registry
`mesoamerica.txt:56`, NAME "Tenōchtitlan" (`country_names_l_english.yml`, macron
included — **which is why a naive `tenoch` substring scan finds nothing; the
second anchor-class trap in this theater**):

```
	TNC = {
		own_control_core = {
			tenochtitlan
		}
		include = "amerindian_advanced_monarchy_no_coast"
		include = "expl_mesoamerica"
		government = { type = monarchy  heir_selection = cognatic_primogeniture  ruler = random  … }
		court_language = nahuatl_language
		capital = tenochtitlan
	}
```

**One location, no claims, no IO, one incoming vassalage.** The NOV precedent
(reshape a polity that existed but whose constitution was dated) does not apply:
Novgorod was there in 1066, and the island of Tenochtitlan was empty until 1325
[D]. TNC is the MAJ / SUK / TIB / VYT class — a post-1066 object — and the
project retires those. §E.1.

### B.3 `FIELD_FIXES` — none proposed

Two candidates were costed and refused:

- **COC's `dynasty = cocom_dynasty`.** The KBO precedent (`build_setup.py:3211`,
  a whole `dynasty =` line dropped) would fit, and the Cocom lineage's
  attestation is 13th-century-and-later [D]. But the tag IS the lineage; dropping
  its house while keeping its name is incoherent. **Left.**
- **CSU's `andean_monarchy` include.** Reshaping Qusqu to `andean_tribe` (the
  SXM/PRM shape) would make it a Killke-era chiefdom without retiring it. But
  `andean_tribe` is what KKE already rides, the registry culture stays
  `inka_culture` either way, and the render change ("Inca" → "Chief") is the
  whole effect. **Left; see OPEN DECISION 4.**

### B.4 Registry overrides — NONE proposed

None of the eleven American registry files is currently overridden and this
package proposes overriding none. **This is load-bearing for CSU**: the
otherwise attractive one-token fix `CSU: culture_definition = inka_culture →
killke_culture` would require a **whole-file override of `andes.txt` (74
blocks)**, inheriting the `verify-vanilla-override` re-diff-after-every-patch
duty for all 74. That is the Gallura cost, and it is not worth one token
(contrast PUR's `hindu` fix, which was free only because `east_asia.txt` was
already ours).

---

## C. Rulers — nobody, and the reasoning is one sentence long

**Zero characters exist for any American tag with a birth date before 1170.1.1**
(§0.6). No 1066 ruler of Tula, Chichén Itzá, Cahokia, Chan Chan, the Cusco
basin, the Valley of Mexico or anywhere else in the hemisphere is attested well
enough to name [U] — the Mesoamerican king-lists that reach the 11th century are
the Toltec ones, and those are the *Anales de Cuauhtitlan* / Sahagún
Quetzalcóatl-Topiltzin tradition, which is myth-history that no two readings
date the same way [D].

The Tunka Manin / Dongzhan precedent (an attested ruler known only through an
external source's transcription) has **no instance here**: there is no
transcription to seat. The Cadalus honest-silence rule applies cleanly.

**Thrones stay at 179. Zero characters, zero dynasties, zero name-key loc rows.**

---

## D. What must die, what must be left, and where the seams are

### D.1 TNC "Tenōchtitlan" — the hemisphere's one unambiguous retirement

The Mexica were still migrating in 1066 [U]; the traditional foundation of
Tenochtitlan is 1325, with 1345 a serious minority reading [D]; vanilla's own
earliest Mexica character is `azt_tenoch`, born 1299. **The location is on the
map with a `rank = city` entry** (`07_cities_and_buildings.txt`,
`tenochtitlan = { rank = city  town_setup = mexican_city }`), it carries five
pops, and it is a vassal of Azcapotzalco.

**Verdict: RETIRE landless with claims, and GRANT `tenochtitlan` to TEP.** §E.1.

What this buys and what it costs:

- the TEP → TNC line dies **free** in `_drop_landless_dep`
  (`build_setup.py:7732-7742`, drops on either side) — `n_landless_deps` 280 → **281**
- the city stays owned by its own overlord and nearest neighbour (`azcapotzalco`
  is in the same `anahuac_province`) — **zero pop-class error lines, zero vacate**
- TNC's claims 0 → **1**, satisfying the claims-backed landless guard (`:6352`)
- **`AZT_f` survives and becomes something to EARN.** Its `allow` is
  `owns = location:tenochtitlan` and its `potential` is
  `OR = { religion = religion:nahuatl  culture = culture:nahua_culture }`
  (`00_formable_countries.txt:4763-4795`) — TEP satisfies both. The Aztec Empire
  remains formable by whoever holds the island, which is the project's own
  Pecheneg philosophy ("a state EARNED by events") applied to the most famous
  polity in the hemisphere
- **cost: `flavor_AZT.txt`'s sixteen TNC-gated `dynamic_historical_event` blocks
  and `country_TNC.txt`'s advance tree become orphaned-but-not-broken** — the
  TIB / `country_TIB.txt` precedent exactly. All sixteen windows open at
  1337.1.1 or later, and most carry an `owns = location:tenochtitlan`-shaped
  trigger a landless shell cannot satisfy

### D.2 TCP "Tlacōpan" — leave the tag, kill the vassalage

Tlacopan/Tacuba as a settlement may predate the Tepanec expansion [U]; its
`tlacopan` location is `nahua_culture`/`nahuatl` and a `rank = city`. What is
certainly 14th-century is its **vassalage to Azcapotzalco**, which is the same
object as the Tepanec hegemony [D].

**Verdict: KEEP TCP landed, STRIP `TEP → TCP` by name.** §G.1. This is the
Kham/Shan/Philippines decision at one-tag scale: the settlement is plausible,
the relation is dated.

### D.3 The Yucatán — capital fix and two strips, no territory

| tag | holds | what it is at 1066 | verdict |
|---|---|---|---|
| **COC "Cocom"** | 12 — `mayapan_province` 5, `chichen_itza_province` 4, `dzilam_province` 2, `ekab_province` 1 | Mayapán's ruling lineage. **Mayapán is c. 1180-1220 [D]; Chichén Itzá is the 11th-century hegemon [D] and COC already owns it and its whole province** | **KEEP, capital → `chichen_itza`** (§B.1) |
| **XIU "Tutul-Xiu"** | 3 — `mani`, `dzibilnocac`, `telantunich` | Mani is the Xiu seat AFTER Mayapán falls in 1441 [D] | **KEEP LANDED, free of COC.** Retiring it would vacate a `rank = city` and gain nothing |
| **HEL "Chel"** | 6 — `dzilam_province` 2, `ekab_province` 4 (incl. `coba`) | Ah Chel is a post-1441 *cuchcabal* [D] — but `coba` is a genuine Terminal Classic centre [D] | **KEEP LANDED, free of COC** |
| **CKP "Chakan Putum"** (5), **ITZ "Itza"** (7), **UAY** (3), **CTM** (2), **KOW** (4), **CNL** (1) | 22 | Champotón, the Petén Itzá, Uaymil, Chetumal, the Kowoj, Ah Canul — the sixteenth-century provinces [all D]. **ITZ's capital `noh_peten` is Tayasal, which the Spanish take in 1697** | **KEEP ALL.** The MODEL — a Yucatán of competing lineage-provinces with no overlord — is right at 1066 once COC's league is gone, even though several names are five centuries late |

**This is the Shan-states / Kham decision taken a third time on the same
reasoning, and it is flagged as OPEN DECISION 3 so the main session can refuse
it.**

### D.4 Cusco — measured, argued both ways, and left

| tag | holds | measured | 1066 reading |
|---|---|---|---|
| **CSU "Qusqu"** | 2 — `qusqu` (`inka_culture`), `quillarumiyoc` (**`killke_culture`**) | `andean_monarchy`, `capital = qusqu`, `inka_culture` registry, **vanilla's own `csu_manco_qhapaq` born 1170.1.1** | The Inca dynasty's founder is born 104 years after our start, on vanilla's own testimony. But the SETTLEMENT is occupied — by the Killke, c. 1000-1200 [D] — and "Qusqu" is a place name, not a dynasty name |
| **KKE "Killke"** | 3 — `willka_pampa` (`acamama_area`) + 2 in `puna_area` | `andean_tribe`, `killke_culture`, `capital = yanahuara` | **Vanilla ships the archaeological name for pre-Inca Cusco as its own tag.** This is the 1066-correct polity and it is already on the map |
| **AYA "Ayarmaca"** (4), **PIG "Pinagua"** (1, `pikillaqta`), **CNC "Canchi"** (1) | 6 | `wari_culture` | The Inca oral tradition's own list of Cusco-basin rivals [D]. Right at 1066 for the same reason Kham's patchwork is |

**Verdict: LEAVE, and record the argument.** Retiring CSU and granting its two
to KKE is one clean rule with one donor (§E.2, Alt 2) and it is the
archaeologically exact answer; it also orphans `flavor_CSU.txt` (8 events, DHE
windows from 1340.1.1) and is the only place in the hemisphere where this
package would contradict its own "the model is right, the name is late" rule.
**OPEN DECISION 4 carries both, fully costed.**

`INC_f` is unaffected either way: its `potential` is
`culture.language = language:quechuan_language`
(`00_formable_countries.txt:3332-3340`) — and `killke_culture` maps to
`quechuan_language` (`peruvian.txt:32`), so KKE can form Tawantinsuyu without
CSU existing. Its `areas = { acamama_area puna_area }` at
`required_locations_fraction = 0.8` means 62 of 77 ownable — unreachable at
start by anybody, which is the design.

### D.5 The Valley of Mexico beyond Tenochtitlan — 45 locations, ~26 tags, all left

`mexihko_area` is 45 ownable locations and 177 pops, split among ~26 altepetl of
one to four locations each: TEP (Azcapotzalco + `cuauhtitlan` + **`tollan`**),
TTZ "Acolhuacan" (Tetzcoco, `tehotihuacan`, `apan`, `zempoala`), CUL
"Culhuacan", OTO "Xaltocan", CLC "Chalco", XCH "Xochimilco", TCP "Tlacōpan",
and a long tail.

**Vanilla's Valley of Mexico is the PRE-imperial one** — Acolhuacan,
Tepanecapan, Culhuacan and Xaltocan as separate powers, with the Mexica a
one-location vassal. That is a 1337 design, and with TNC gone it becomes a
perfectly serviceable 1066 one: the altepetl system, the Otomi and Nahua mixture
(`otomanguean_culture` 30 court languages against `nahuatl_language` 84), and no
hegemon. **Every one of the ~26 is left.**

### D.6 The North American interior, Aridoamerica, and the far north — the largest "leave it" in the project

| ground | measured | verdict |
|---|---|---|
| **`canada_region`** 573 ownable, 564 pops | **0 owned**; 266 covered by a pop-country | **LEAVE.** Vanilla's stateless model, correct at 1066 and 1337 |
| **`alaska_region`** 316, **`west_coast_region`** 357, **`brazil_region`** 499, **`la_plata_region`** 155, **`chaco_region`** 121, **`caribbean_region`** 111 | **0 owned each**, 1,559 locations, 1,602 pops | **LEAVE ALL.** The brief's "measure and leave" — confirmed at 2,132 locations |
| **Labrador (37) and Newfoundland (27)** | 0 owned; `dorset_culture` 23 locations, `beothuk_culture` 26 | **LEAVE.** The Dorset are the right people at 1066 and the Thule displacement is c. 1200-1400 [D] — *more* correct at our date than at vanilla's |
| **The Ancestral Pueblo world** | `ancestral_pueblo_culture` **7 locations, 100% unowned**; **HTS "Hisatsinom"** (`aridoamerica.txt:326`) is its named `type = pop` identity with 4 pop-locations | **LEAVE.** Chaco Canyon's great houses are not modelled as locations at all (probed: no `chaco`, `pueblo_bonito`, `mesa_verde`, `aztec_ruins` location exists) — a light pass cannot invent map data, and vanilla's stateless-with-identity answer is the Perm/Vyatka shape |
| **The Hohokam** | `hohokam_culture` 7 locations, all unowned; **HHK** (`aridoamerica.txt:92`) covers 8 | **LEAVE.** The Hohokam Classic is c. 1150-1450 [D]; a stateless Sedentary-period Hohokam is right at 1066 |
| **The eight Rio Grande pueblos** ACO ISL KER OHK TAO TEY TNN TST | 8 locations, 32 pops, `keres`/`tanoan`, `kachina_religion` | **LEAVE.** Acoma and Taos are continuously occupied from before 1066 [D] |
| **`great_plains_region`'s 344 unowned** (CHK's 14 aside) | 431 pops, 222 pop-covered | **LEAVE** |
| **`east_coast_region`'s 592 unowned** | 925 pops, **578 pop-covered — the densest pop-country coverage on the map** | **LEAVE** |

### D.7 The measured seams — named, not touched

| ground | measurement | whose |
|---|---|---|
| **GRL "Greenland"** — 12 `greenland_area` locations, `discovered_areas = { labrador_sea_area }` | `_scandinavia.txt:134`; `greenland_area` is `north_atlantic_islands_region`/`western_europe`; `labrador_sea_area` has **0 ownable** | **The Scandinavian slice's, not this one's.** Recorded because it is the only trans-Atlantic link in the build (§0.8). A Vinland/Markland situation is banked, not proposed (§H) |
| **`colombia_region`'s 12 owned** — ZIP "Muyquyta" 5, ZAQ "Chunsua" 4, TAI "Tairona" 3 | `muisca_culture`/`muisca_religion`, `tayrona_culture`; the Muisca confederations consolidate late [D], the Tairona towns are c. 900+ [D] | **LEAVE.** Three tags over 207 locations is already a minimal reading, and ZIP is one of the 94 tags §0.2's strict regex hides |
| **`central_america_region`'s 22 owned** — KUS "Kuskatan" 4 (Pipil), QUA, KIC, KAQ, CHT, MMM, QAN, TZU, ITZ | Pipil migrations into Cuzcatlán are c. 900-1200 [D]; the K'iche'/Kaqchikel highland states are 13th-15th century [D] | **LEAVE** — the Kham decision again, and 102 of the region's 124 are unowned anyway |
| **The `wari_culture` → "Inca" render** (11 monarchies) | `peruvian.txt:693`, `country_ranks.txt:1917` | A culture/language question, not a 1066 one. **✎RE-FILED (2026-08-03) to a NAMING/STYLING pass, not POP-PHASE** — pops change nothing; the render rides the culture's `language` field (POP-PHASE-PACKAGE §C.2) |
| **CLM's `teco_culture` on zero locations** | `mesoamerica.txt:383`, CLM landed with 7 | **✎RETIRED (2026-08-03) — a `location_templates.txt` (SEED) artefact; on POPS `teco_culture` sits on 6 locations and all 6 are CLM's own (POP-PHASE-PACKAGE §0.1). The registry is right** |

**DOUBLE-OWNERSHIP CHECK — clean.** All 4,441 American locations were tested for
membership in more than one country block's `OWN_KEYS` set. **Zero.**
`CONTROL_STRIPS` (`build_setup.py:1720`) needs no American key.

---

## E. Territory

### E.1 The recommended rule set — one grant, one retirement, no vacates

**This package proposes ZERO `LOCATION_VACATED` entries and ZERO
`UNOWNED_GRANTS`.** The hemisphere is already 88.9% unowned; emptying more of it
would be a statement, not a correction, and every location this package touches
has exactly one owner (measured with the ten-key reader), so
`UNOWNED_GRANTS` (`build_setup.py:1934`) is not needed and **must not be used** —
the SEA phantom's lesson applied prospectively.

Same 5-tuple shape as `_AFRICA_RULES` / `_SEA_RULES` / `_TIBET_RULES`
(`build_setup.py:1853`, `:1986`, `:2145`; consuming loops at `:5991`, `:6013`,
`:6031`). **The count below was resolved by `build_setup._resolve_ruleset`
itself, not transcribed.**

```python
# --- THE AMERICAS. Tenochtitlan is founded in 1325 [D]; on 1066.9.15 the
#     island is empty. The city goes to TEP, its own overlord and the
#     holder of azcapotzalco in the same anahuac_province — so the
#     rank = city entry (07_cities_and_buildings.txt) keeps an owner and
#     the vacated-pop error class does not grow. AZT_f is gated on
#     `owns = location:tenochtitlan`, not on the tag, so the Aztec path
#     stays open and has to be earned.
_AMERICAS_RULES = {
    "TEP": ([], ["tenochtitlan"], [], [], 1),
}

AMERICAS_LANDLESS = ("TNC",)
```

### E.2 DONOR TABLES — every proposed rule and every costed alternative

**This is the section `KNOWLEDGE.md`'s delta-guard law demands, and the main
session is asked to reproduce it before implementing.** The law's reason applies
directly here: TEP survives every alternative below, so for any rule that takes
from TEP the emptied-but-unlisted delta guard (`build_setup.py:6389-6396`) stays
silent and **the exact-count assert is the only line of defence.**

**RULE 1 (recommended) — `_AMERICAS_RULES["TEP"] = ([], ["tenochtitlan"], [], [], 1)`.**

| donor | loses | of | locations | `define_pop` | survives? |
|---|---|---|---|---|---|
| **TNC** | **1** | 1 | `tenochtitlan` | **5** | **NO — emptied, and it is in `AMERICAS_LANDLESS`. The delta guard is the check that would catch an omission here** |
| **total** | **1** | | | **5** | |

Raw resolve of the single is **1**; TNC holds it. `tenochtitlan` carries
**exactly one** ownership entry (re-measured with the ten-key reader), so
`_remove_owned_many`'s `!= 1` exit (`:5787`) will not fire. TEP goes 3 → **4**.

---

**Alt 1 — the Toltec Tollan rule sets (OPEN DECISION 1).** Three shapes were
resolved. **All three empty at least one surviving-elsewhere donor's entire
holding, which makes every one of them a multi-tag retirement — the fact that
decides the decision.**

**Alt 1a — `TOC: (["xilotepec_province"], [], [], [], 6)`** — the Tula-Jilotepec
corridor:

| donor | loses | of | locations | pops | survives? |
|---|---|---|---|---|---|
| **XIL "Xilotepec"** | **3** | **3** | `ixtachichimecapan kerhiretarhu xilotepec` | 10 | **NO — emptied. Needs `LANDLESS_AFTER`** |
| **TEP "Tepanecapan"** | **2** | 3 | `cuauhtitlan tollan` | 6 | yes, at 1 (`azcapotzalco`) — **the delta guard cannot see this loss** |
| **AXO "Axocopan"** | **1** | 3 | `mixquiahuala` | 3 | yes, at 2 — **likewise invisible to the guard** |
| **total** | **6** | | | **19** | |

**Alt 1b — `TOC: (["xilotepec_province"], ["tollantzinco"], [], [], 7)`** — adds
Tulancingo, the second Toltec city [D]:

| donor | loses | of | locations | pops | survives? |
|---|---|---|---|---|---|
| **XIL** | **3** | **3** | as above | 10 | **NO — emptied** |
| **TEP** | **2** | 3 | as above | 6 | yes, at 1 |
| **AXO** | **1** | 3 | `mixquiahuala` | 3 | yes, at 2 |
| **TZC "Tollantzinco"** | **1** | **1** | `tollantzinco` | 4 | **NO — emptied** |
| **total** | **7** | | | **23** | |

**Alt 1c — `TOC: ([], ["tollan", "cuauhtitlan"], [], [], 2)`** — the minimal
version, one donor:

| donor | loses | of | locations | pops | survives? |
|---|---|---|---|---|---|
| **TEP** | **2** | 3 | `cuauhtitlan tollan` | 6 | yes, at 1 (`azcapotzalco`, its capital) |
| **total** | **2** | | | **6** | |

Under 1a `LANDLESS_AFTER` gains XIL; under 1b it gains XIL and TZC; both then
need derived claims and both change `n_landless_deps` by 0 (neither names a
dependency — grep-verified). Under all three, TEP keeps `azcapotzalco` and its
capital, so no `CAPITAL_FIXES` entry is needed.

---

**Alt 2 — retire CSU and grant its two to KKE (OPEN DECISION 4).**

```python
_AMERICAS_RULES["KKE"] = ([], ["qusqu", "quillarumiyoc"], [], [], 2)
AMERICAS_LANDLESS = ("TNC", "CSU")
```

| donor | loses | of | locations | pops | survives? |
|---|---|---|---|---|---|
| **CSU "Qusqu"** | **2** | **2** | `qusqu quillarumiyoc` | **11** | **NO — emptied, listed in `AMERICAS_LANDLESS`** |
| **total** | **2** | | | **11** | |

Both carry exactly one ownership entry. KKE goes 3 → **5**, its capital
`yanahuara` untouched. CSU's claims 0 → 2. `n_landless_deps` unchanged (CSU
names no dependency — grep-verified over both trees). `flavor_CSU.txt`'s 8
events are orphaned; `INC_f` is not (§D.4).

---

**Alt 3 — vacate `tenochtitlan` instead of granting it (OPEN DECISION 2b).**

```python
LOCATION_VACATED["TNC"] = ["anahuac_province"]
LOCATION_VACATED_EXPECT["TNC"] = 1
```

| donor | loses | of | locations | pops |
|---|---|---|---|---|
| **TNC** | **1** | 1 | `tenochtitlan` | **5** |
| TEP | **0** | — | `azcapotzalco` is inside the swept name and is **TEP's** — excluded by the snapshot intersection at `:6268`, not by a minus-list | — |
| CLC / TCP / XCH | **0** | — | `chalco`, `tlacopan`, `xochimilco` likewise | — |
| **total** | **1** | | | **5** |

**Raw resolve of `anahuac_province` is 5; TNC holds 1.** Writing `5` fires the
assert at `:6269-6272` with 1 — this is break-test (d). Cost: `vacated` 625 →
**626**, ~3 lines of the vacated-pop class (the ≈0.55 ratio,
`EU5-ERROR-DECODER.md` as corrected by `PERM-VYATKA-PACKAGE.md` §E.4), **and an
unowned `rank = city` on the map** (`07_cities_and_buildings.txt` ships
`tenochtitlan = { rank = city }`). Costed and refused.

---

**Alt 4 — the maximal Yucatán (OPEN DECISION 3c): fold XIU and HEL into COC.**

```python
_AMERICAS_RULES["COC"] = ([], ["mani", "dzibilnocac", "telantunich",
                               "dzilam", "titsimin", "coba", "ekab",
                               "labcah", "zama"], [], [], 9)
AMERICAS_LANDLESS += ("XIU", "HEL")
```

| donor | loses | of | locations | pops | survives? |
|---|---|---|---|---|---|
| **HEL "Chel"** | **6** | **6** | `coba dzilam ekab labcah titsimin zama` | 20 | **NO — emptied** |
| **XIU "Tutul-Xiu"** | **3** | **3** | `dzibilnocac mani telantunich` | 11 | **NO — emptied** |
| **total** | **9** | | | **31** | |

COC 12 → **21**, `n_landless_deps` 281 → **283** (both COC lines then die free
and the named strips of §G.1 shrink to one), parliament 1364 → **1362**, ghosts
unchanged (neither is in an IO). Costed; **refused** — it replaces a defensible
patchwork with an invented eleventh-century Chichén empire whose extent no source
supplies [U], and `mani` is a `rank = city`.

### E.3 What each tag keeps, under the recommended design

| tag | before | after | verdict |
|---|---|---|---|
| **TNC** | 1 | **0** | **LANDLESS** — claims 0 → 1, derived by `_landless_claims` (`build_setup.py:6170`), which snapshots holdings BEFORE the grants |
| **TEP** | 3 | **4** | recipient (`azcapotzalco cuauhtitlan tollan` + `tenochtitlan`) |
| **COC** | 12 | **12 — unchanged** | capital repointed only (§B.1) |
| **TCP / XIU / HEL / CSU / KKE / CHK** and the other 216 | — | **unchanged** | §D |

**ONE retirement, and it is not a side effect** — TNC's single location is
granted away by name, so the emptied-but-unlisted delta guard (`:6389-6396`)
should stay **silent throughout. If it fires, the design is wrong.**

### E.4 `CAPITAL_FIXES` — one entry (§B.1)

TNC's `capital = tenochtitlan` becomes vestigial and is **exempt** by the orphan
guard's `if held and …` condition (`:6776`) — the POR/`guimaraes` precedent. It
is also *right*: a landless Tenochtitlan whose capital is the island is a
Tenochtitlan whose future starts where the sources say it started. COC's is the
package's only capital correction.

### E.5 What this slice moves, in one line

**1 location changes owner, 0 are vacated, 1 tag is retired landless, 0 new tags
are created, 1 capital is corrected, 3 dependency lines are stripped by name and
1 dies free, 0 rulers are seated, 0 characters, 0 dynasties, 0 registry blocks,
0 registry overrides, 0 colours, 0 CoA, 0 loc rows.**

That is the smallest slice in the project's history — smaller than Perm/Vyatka's
26 vacated — for the largest theater on the map.

---

## F. Rank, government and naming — worked out to the rendered string

### F.1 The law, restated for this theater

Every landed American country reaches
`country_name_construction_prefix_rank_of_name` (`country_name_construction.txt:183-186`),
whose `_map` is bare `"$NAME$"` (`government_names_l_english.yml:12`).
**Map label = NAME key, verbatim, for all 223.** The 321 `type = pop` countries
take the `:154` `country_type = pop` branch and render from their ADJ keys.
Full branch enumeration in §0.7.

### F.2 What the tags this package touches render as, before and after

| tag | today | after the recommended design |
|---|---|---|
| **TNC** | map **"Tenōchtitlan"**; `nahuatl_language`, nahua_culture, monarchy, no declared rank → `rank_county_nahua` (`:2497`) or `rank_duchy_nahua` (`:1990`) → **"Āltepētl of Tenōchtitlan" / "Tlahtoāni"** | **gone from the map** — a landless shell with 1 claim |
| **TEP** | map "Tepanecapan"; same chain → "Āltepētl"/"Tlahtoāni" | unchanged, four locations |
| **COC** | map "Cocom"; `maya_language`, monarchy, no rank → `rank_duchy_ajawil` (`:1320`) → **"Ajawil of Cocom" / "Ajaw"**, or at county `rank_county_kuchkabal` (`:2385`) → **"Kuchkabal" / "Halach Winik"** | **unchanged in render; the capital panel now reads Chich'en Itza** |
| **XIU / HEL / CKP / ITZ / CTM / UAY / KOW / CNL** | maya chain, same | unchanged; **independent** |
| **TCP** | "Tlacōpan", nahua chain | unchanged; **independent** |
| **CHK** | map "Cahokia"; `dhegiha_language`, **tribe**, no rank → `rank_duchy_tribe` (`:1606`) or `rank_county_tribe` (`:2278`) → **"Tribe of Cahokia"/"Chief"** or "Minor Tribe"/"Chieftain" | unchanged |
| **the five Haudenosaunee** | tribe + `culture_group:haudenosaunee_group` → `:1596` / `:2269` → **"Tribe"/"Clan" under a "Royaner"** | unchanged; **no league** (§0.3) |
| **TAR** | declares `country_rank = rank_duchy`, `purepecha_language` → `:1332` → **"Iréchikwa of Purépecha" / "Irecha"** | unchanged |
| **CSU** | `andean_monarchy`, `quechuan_language` → `rank_duchy_inca` (`:1917`) → **"Duchy of Qusqu" / "Inca"** | unchanged under the recommendation; **gone** under OPEN 4b |

### F.3 The derived-rank question, restated honestly

**221 of the 223 landed American tags declare no `country_rank`, and no file
settles the thresholds by which the engine derives one** — the same gap Tibet,
SEA and Perm/Vyatka all left open (`build_setup.py:2181-2185`). At 1-23
locations the plausible derivations are county and duchy. **Every render cell in
F.2 that names a county-or-duchy alternative is conditional on that, and the
click tour is what settles it.** Inherited, still owed.

### F.4 Formables — five in the hemisphere, none opened, none consumed

`VAN/in_game/common/formable_countries/00_formable_countries.txt`:

| formable | line | tag | frac | scope | potential / allow | reachable at start? |
|---|---|---|---|---|---|---|
| **AZT_f** | `:4763` | AZT | 0.75 | `regions = { mesoamerica_region }` = 325 ownable → **244** | `OR = { religion = religion:nahuatl  culture = culture:nahua_culture }`; `allow = { owns = location:tenochtitlan }` | **NO.** Largest Nahua holding after this slice is TEP at 4 |
| **INC_f** | `:3332` | INC | 0.8 | `areas = { acamama_area puna_area }` = 77 ownable → **62** | `culture.language = language:quechuan_language`; `allow = { religion.group = religion_group:folk_peruvian_group }` | **NO** |
| **MAY_f** | `:3866` | MAY | — | — | — | **NO** |
| **MEX_f** | `:2650` | MEX | 0.5 | `mesoamerica_region` | — | **NO** |
| **USA_f** / **CAN_f** | `:2587` / `:2617` | USA / CAN | 0.35 | `east_coast_region` / `canada_region` | — | **NO** |

**No formable names TNC, COC, CSU or any tag this package touches**, and
AZT_f's only tag-shaped reference is the *location* `tenochtitlan` — so
retiring TNC leaves the Aztec path intact and unclaimed, which is the design
(§D.1). `country_AZT.txt`, `country_INC.txt`, `country_TNC.txt` and
`country_USA.txt` are the hemisphere's four advance trees; only `country_TNC.txt`
is affected, and orphaned-but-not-broken (the TIB precedent).

---

## G. Diplomacy

### G.1 Three named strips, and one line that dies free

```python
    # The Americas (2026-08-02). Vanilla ships exactly FOUR dependency
    # lines in the whole western hemisphere and all four are post-1066.
    # TEP->TNC dies in the landless sweep below (TNC retired, D.1), so
    # only three are stripped by name here:
    #   TEP->TCP  the Tepanec hegemony over Tlacopan, c. 1370-1428 [D]
    #   COC->XIU  the Mayapan league, c. 1220-1441 [D]; Mani is a
    #             post-1441 seat [D]
    #   COC->HEL  Ah Chel is a post-1441 cuchcabal [D]
    # The subjects stay LANDED (they hold 1, 3 and 6 locations), so the
    # landless sweep cannot see these three: they must die here.
    n_americas_deps = 0
    for _f, _s in (("TEP", "TCP"), ("COC", "XIU"), ("COC", "HEL")):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = " + _f + r" second = " + _s
            + r" subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_americas_deps += _k
    if n_americas_deps != 3:
        sys.exit(f"expected exactly 3 American vassal strips, "
                 f"got {n_americas_deps}")
    report.append(("the Americas freed of their late hegemonies",
                   n_americas_deps))
```

Shape copied verbatim from the KBO→Hausa batch (`build_setup.py:7607-7616`,
`assert n_hausa == 7`) and the Tibet tusi batch (`:7691-7700`,
`assert n_tibet_tusi == 4`). Counted against the **VANILLA** source the build
reads every run: `VAN/main_menu/setup/start/12_diplomacy.txt:515 :516 :815 :816`
— exactly four lines, exactly one match each.

**Placement: beside the other named strips and BEFORE the landless sweep at
`:7732`.**

**`n_landless_deps` 280 → 281** (`build_setup.py:7820-7822`) — TEP → TNC only.
**Observe it failing first**, per CLAUDE.md.

**No double-overlord risk:** the three lines are removed, not repointed, and no
new tie is proposed anywhere in this package. Every one of TCP, XIU and HEL has
exactly one overlord today and zero after.

### G.2 Repoints — NONE. New ties — NONE.

**This package proposes no tributary, vassal or pact line of any kind.** The
1066 Americas had no inter-polity overlordship that any source in this repo can
date, and giving one to COC or TEP would invent the very thing the slice
removes.

One variant was costed and refused: `COC → CKP` (Chakan Putum) as a
`subject_type = tributary` would pass the visible gate — but the Yucatán's
league structure is the object being retired, and re-creating it under a
different pair is incoherent. Under it, `"COC"` would have to join
`_MOD_TRIB_OVERLORDS` (`verify_mod.py:766-767`) and `:843`'s `min_count` would
rise 78 → 79.

### G.3 What the landless sweep does and does not do here

| constant | `file:line` | effect of retiring TNC |
|---|---|---|
| `n_landless_deps` | `build_setup.py:7820` | **280 → 281** (TEP → TNC) |
| `n_pacts` | `:7850` | **9 — unchanged.** Measured: **zero** `scripted_mutual`/`scripted_oneway` lines name any American tag, in either tree |
| `n_ghosts` / `_expected_ghosts` | `:7087` / `:7040` | **156 — unchanged.** TNC is in no IO member list; **no American tag is** |
| empty-IO-members pin | `verify_mod.py:909-916` | **9 — unchanged.** Nothing can be drained: the mod's `15_international_organizations.txt` has **zero** American members after the creation-date strip (§0.3) |
| tributary-gate `min_count` | `verify_mod.py:843` | **78 — unchanged.** All four American lines are `vassal`, and neither TEP nor COC is in `_MOD_TRIB_OVERLORDS` |

**That ties Perm/Vyatka for the cheapest diplomacy profile any retirement in
this project has had, and beats it on IO risk: there is no IO to drain.**

---

## H. Left alone deliberately

| what | measurement | why |
|---|---|---|
| **The 321 American `type = pop` identities** | 0 locations each; **72% of the game's 448** | §0.1. Vanilla's stateless model, complete, 1066-correct, and seventeen times the Siberian precedent. **The single largest "already right" finding in any package so far, by a wide margin** |
| **The 3,948 unowned American locations** | 4,408 `define_pop`; 1,853 covered by a pop-country | §0.9. This package *adds* none and touches none |
| **Seven regions with zero owned land** (canada, caribbean, brazil, la_plata, chaco, alaska, west_coast) | 2,132 locations, 2,166 pops | §D.6. The brief's "measure and leave" — confirmed |
| **CHK Cahokia's 23** | 77 `define_pop`; `flavor_CHK.txt` 23 events, "The Sunset of Cahokia" at 1337-1356 | §0.4. **1066 is Cahokia's right date and vanilla's own DHE lands the terminus correctly.** Do not touch it |
| **The five Haudenosaunee nations** | 27 locations; the league's `creation_date = 1142.1.1` instance **already deleted** | §0.3. The creation-date law did the work months ago |
| **The Ancestral Pueblo / Hohokam / Hopi / Zuni** | 4 identities, 0 land, 18 pop-locations; `ancestral_pueblo_culture` 7 locations 100% unowned; **Chaco Canyon is not a location at all** | §D.6. A light pass cannot invent map data, and the identity layer already exists |
| **The Yucatán's ten late-named lineage provinces** COC XIU HEL CKP ITZ UAY CTM KOW CNL MOP | 43 locations; ITZ's capital `noh_peten` is a 1697 object [D] | §D.3, OPEN DECISION 3. The Shan/Kham/Philippines decision a third time |
| **TAR Purépecha (19), the Mixtec/Zapotec set (MIX 8, ZAP 5, THT 4, TCQ 3, TZL 3, COI 2 …), the ~26 Valley altepetl** | ~120 locations | Michoacán and Oaxaca were inhabited and politically fragmented at 1066 [D]; the tags are peoples and places, not late dynasties. The Kham reasoning |
| **CSU "Qusqu"** | 2 locations, 11 pops; vanilla's own founder born **1170.1.1** | §D.4, OPEN DECISION 4. The theater's one place where this package's own rule cuts both ways, stated rather than buried |
| **The `wari_culture` → `quechuan_language` → "Inca" render** on 11 monarchies | `peruvian.txt:693`; `country_ranks.txt:1917` | **✎RE-FILED (2026-08-03) to a NAMING/STYLING pass** (POP-PHASE-PACKAGE §C.2 — pops change nothing, the culture's `language` field does). A culture-mapping question that is equally wrong at 1337 |
| **CLM's `culture_definition = teco_culture` on ZERO of 20,922 locations** | `mesoamerica.txt:383`; CLM landed with 7 | **✎RETIRED (2026-08-03) — measured on the SEED layer; on POPS `teco_culture` sits on 6 locations, all CLM's own (POP-PHASE-PACKAGE §0.1)** |
| **`toltec_culture` on ZERO locations** | `mesoamerican.txt:364`, `map_toltec` `02_map.txt:1420`, loc `cultural_and_languages_l_english.yml:1069`; **TEP carries `tolerated_cultures = { toltec_culture }`** | §E.2 Alt 1 and OPEN DECISION 1. Vanilla built the culture, gave it a colour, gave the Tepanec a tolerance for it, and put it on no ground — it exists to be *referenced* by `flavor_azt.160`, the "claim Toltec descent" event |
| **GRL's `labrador_sea_area` discovery** | `_scandinavia.txt:134`; 0 ownable in the area | §0.8. The Scandinavian slice's. **Banked: a Vinland/Markland situation** — the Greenland colony (985) and the Vinland voyages (c. 1000) are both live at 1066 [D], and vanilla already grants GRL the sea it needs |
| **`06_pops.txt` / `07_cities_and_buildings.txt`** | vanilla's, un-overridden; 1,019 ranked city entries game-wide (748 town, 261 city, 7 rural_settlement, 3 megalopolis), **25 of them American** — `tenochtitlan azcapotzalco tlacopan tetzcoco mayapan mani chakan_putum noh_peten pismachi` are `city`, the rest `town` | Note `KNOWLEDGE.md`'s "`tag = X … location = L` where X does not own L is FIRST-CLASS vanilla" — do **not** "fix" `07_cities` after the grant. This is also the argument against Alt 3 (vacating `tenochtitlan` would leave an unowned `rank = city`) |
| **`flavor_AZT` / `flavor_CSU` / `flavor_usa`** | 17 / 8 / 24 events; every American DHE window opens at **1337.1.1 or later** | Nothing fires before 1337 at a 1066 start, so the whole American flavour layer is inert for 271 years and then arrives on schedule. **No date surgery is needed anywhere in the hemisphere** |
| **The altepetl reform's `potential`** | `country_specific.txt:2685-2708`, `potential = { culture = culture:nahua_culture … }`; **51 landed American tags carry it via their templates and ALL 51 are `nahua_culture`** — zero violations | A clean data point for the **reforms-vs-potential OWED CHECK** inherited from Africa/SEA: vanilla itself ships no violation here |

---

## I. Mechanism — every tool exists, and the package uses three of them

**This package needs no new build step and no new harness capability.**

| need | existing mechanism | `file:line` |
|---|---|---|
| region/area/province → locations | `_parse_defs` + `_ownable_set` + `_defs` | `:748`, `:772`, `:809` |
| rule-set resolution | `_resolve_ruleset` | `:815`; consuming-loop models at `:5991` (Africa), `:6013` (SEA), `:6031` (Tibet) |
| **grant one location by name** | `_AMERICAS_RULES` 5-tuple → `LOCATION_GRANTS` **extend** (TEP is a landed recipient) | declare `:3012`; loop model `:6031-6045` |
| exactly-one-owner on every grant | `_remove_owned_many` | `:5782`, exit `:5787` |
| grant-list disjointness | `_list_owner` | `:6119-6125` |
| steppe-horde recipient guard | `_bad_recip` — **TEP is a monarchy; not reached** | `:6110-6112` |
| retire with auto-derived claims | `LANDLESS_AFTER` + `_landless_claims` | `:2995`, `:6170` |
| prove the retiree really emptied | the `LANDLESS_AFTER … still owns` guard | `:6333` |
| prove the retiree carries claims | the claims-backed landless guard | `:6352` |
| catch a side-effect retirement | the emptied-but-unlisted delta guard | `:6389-6396` |
| **capital correction, old value asserted** | `CAPITAL_FIXES` | declare `:3050`; apply `:6431-6444` |
| orphan-capital delta (landless tags exempt) | `_orphan_capitals` in `validate()` | `:6754-6783` |
| **named dependency strip** | the KBO→Hausa / Tibet-tusi shape | `:7607-7616`, `:7691-7700` |
| dependency dissolution by landlessness | `_drop_landless_dep` | `:7732-7742`, assert `:7820` |
| IO member strip | `build_ios`'s generic `LANDLESS_AFTER` sweep | assert `:7087` — **not reached: no American tag is in any IO** |
| the future-dated IO strip (already ran) | `creation_date >= START_DATE` | `:6849-6863`, assert `:7172` (`removed != 17`) |
| **`LOCATION_VACATED` + `_EXPECT`** | **NOT USED** (Alt 3 only) | `:1265`, `:1273`; resolve+assert `:6254-6277` |
| **`UNOWNED_GRANTS`** | **NOT USED, and must not be** — `tenochtitlan` has exactly one owner, re-proven with the ten-key reader | `:1934` |
| `CONTROL_STRIPS` | **no key needed** — zero double-ownership in 4,441 locations | `:1720` |
| `FIELD_FIXES` | **+0** | `:3123`, apply `:6454-6464` |
| new country blocks / capital discovery | `NEW_COUNTRIES`, `_assert_new_block_discovery` | `:502`, `:5658` — **not used** |
| `HISTORICAL_RULERS` / `NEW_CHARACTERS` | **not used — zero rulers** | `:69`, `:3667` |

**Nothing here needs a NEW mechanism.** Every alternative in §E.2 also runs on
existing tools; Alt 1a/1b would additionally need `LANDLESS_AFTER` entries for
XIL (and TZC), `NEW_COUNTRIES` + a colour key + a CoA decision + two loc rows
for TOC, and Alt 3 would need a `LOCATION_VACATED` key.

**Four asserts that will fire if the design is wrong, and should be watched:**

1. **`_AMERICAS_RULES["TEP"]` resolved-count** (`:6031`-loop) — must be **1**.
2. **`_remove_owned_many != 1`** (`:5787`) — fires if `tenochtitlan` has two
   ownership entries or zero. Measured at exactly one.
3. **the emptied-but-unlisted delta guard** (`:6389-6396`) — must stay
   **silent**. TNC is the only retirement and it is listed. **If it fires, the
   grant took more than the design intends.** Note honestly: TEP survives at 4,
   so if a future edit took TEP's land instead, the guard could *not* fire —
   **the donor table of §E.2 is the guard.**
4. **`CAPITAL_FIXES` old-value assert** (`:6440`) — `capital = mayapan` must be
   found in COC exactly once. A vanilla patch that reformats the block fails
   loudly here, as intended.

**The harness needs no new check.** Every class this package touches is already
guarded: landless holdings, landless claims, IO ghosts, empty IO members,
one-ruler-per-block, the identity↔start-block bijection, parliament reach, the
tributary gate, CoA coverage, orphan capitals.

---

## OPEN DECISIONS

**1. A Toltec Tollan — create a tag, or leave `tollan` as TEP's location?**
Tula/Tollan is the one major named 1066 polity in the hemisphere with no vanilla
tag. Its apogee is c. 950-1150 with collapse c. 1150-1200 [D], so 1066 is the
middle of its hegemony. Vanilla's evidence that it *knows* this: `toltec_culture`
exists with its own colour and English loc (`mesoamerican.txt:364`,
`02_map.txt:1420`, `cultural_and_languages_l_english.yml:1069`), **TEP carries
`tolerated_cultures = { toltec_culture }`**, and `flavor_azt.160` is an event
about claiming Toltec descent.
**(a) NO NEW TAG** (recommended): `tollan` stays one of TEP's four locations, as
it is today. Zero cost, zero invention.
**(b) TOC over `xilotepec_province`** (Alt 1a, donor table §E.2): 6 locations,
19 pops, **retires XIL as a side effect** (3 of 3), takes 2 from a surviving TEP
and 1 from a surviving AXO. Registry +1, colour +1, CoA +1, loc +2,
`LANDLESS_AFTER` +2 (TOC's donors), country blocks 2411 → 2412.
**(c) TOC over `xilotepec_province` + `tollantzinco`** (Alt 1b): 7 locations,
**retires XIL and TZC**. The most historically shaped extent — Tollan and
Tollan-Tzinco are the two Toltec cities [D].
**(d) TOC over `tollan` + `cuauhtitlan` only** (Alt 1c): 2 locations, one donor,
no side-effect retirement — and a two-location "Toltec Empire", which asserts a
hegemon and then draws it as a village.
**Recommendation: (a).** Three measured reasons, in order of weight. First,
**`toltec_culture` sits on ZERO of 20,922 locations** — a Toltec tag would have
`nahua_culture` as its primary culture (what `tollan` actually carries), so the
"Toltec" would be a Nahua state wearing a name vanilla put on no ground.
Second, the extent is unknowable: every reading of the Toltec state's reach is
inference from Aztec myth-history [D], and (b)/(c) both empty a surviving tag,
which is precisely the case the delta guard cannot see. Third, this is a LIGHT
pass and (a) is the only option that asserts nothing.
**Counter, and it is the strongest in the package:** Tula at 1066 is to central
Mexico what Cahokia is to the Mississippi and Chichén Itzá is to Yucatán — and
this package keeps both of those and drops this one, purely because vanilla
happened to build tags for two of the three. A 1066 map of Mesoamerica with no
Toltec state is a visible historical hole, and (c) is fully costed with its
donor table printed. If the main session wants one invention in the hemisphere,
this is the one to make.

**2. TNC "Tenōchtitlan" — retire it, and what happens to the location?**
**(a) RETIRE + GRANT `tenochtitlan` to TEP** (recommended, §E.1): 1 location, 0
pop-error lines, the city keeps an owner, TEP → TNC dies free
(`n_landless_deps` 281), claims 0 → 1, `AZT_f` stays open and has to be earned.
**(b) RETIRE + VACATE it** (Alt 3): `vacated` 626, ~3 error lines, and an
**unowned `rank = city`** on the map.
**(c) LEAVE**: a 1066 map with a city founded in 1325 on it, vassal to a
hegemony that begins in the 1370s.
**Recommendation: (a).** Tenochtitlan's foundation date is the least contested
fact in Mesoamerican political chronology that bears on this project, and the
tag is one location — the cheapest correction of the clearest anachronism
anywhere on the map. **Counter:** it orphans `flavor_AZT.txt`'s sixteen events
and `country_TNC.txt`, which is more vanilla content than any single retirement
this project has made outside TIB; and a *landless* TNC with one claim is
arguably a worse story than a *tiny* TNC, since the island really was empty
rather than "conquered". (b) tells the true story at the price of three log
lines and an ownerless city.

**3. The Yucatán — capital fix + two strips, or something larger?**
**(a) CAPITAL_FIXES COC `mayapan` → `chichen_itza`, and strip COC→XIU and
COC→HEL** (recommended, §B.1 + §G.1): one token, two lines, zero territory. The
Yucatán becomes ten independent lineage-provinces with the hegemon seated where
the 11th century puts it.
**(b) STRIPS ONLY, leave the capital**: keeps "Mayapán" as a capital 115 years
before its foundation [D].
**(c) FOLD XIU and HEL into COC** (Alt 4, donor table §E.2): 9 locations, 31
pops, two more retirements, one continuous Chichén hegemony.
**(d) ALSO RENAME COC** to "Chich'en Itza" — two loc rows in the mod's own
`1066_norman_conquest_l_english.yml` (`COC:` and `COC_ADJ:`), which would
shadow vanilla's keys and change the map label under the §0.7 law.
**Recommendation: (a).** **Counter:** (d) is where the visual payoff actually
is — a player clicking Yucatán reads "Cocom", the name of a lineage first
attested centuries later, when the thing on the ground in 1066 is Chichén Itzá;
but **overriding a VANILLA tag's NAME key from the mod's own loc file is
unattested in this repo** (all 375 rows serve mod-created tags or name keys),
so it must be proven before it is written, and this package will not assert it.
(c) is refused because no source supplies Chichén's extent [U].

**4. CSU "Qusqu" — leave, or retire it into KKE "Killke"?**
**(a) LEAVE** (recommended, §D.4): "Qusqu" is a place name over an occupied
place; the Killke tag already exists beside it; the cost is that the registry
`culture_definition = inka_culture` asserts Inca ethnicity at 1066, and fixing
*that* would need a whole-file override of `andes.txt` (74 blocks — the Gallura
cost), which is not worth one token.
**(b) RETIRE CSU + GRANT its 2 to KKE** (Alt 2, donor table §E.2): 2 locations,
11 pops, zero vacate, one donor, `INC_f` still reachable through KKE's own
quechuan language. The archaeologically exact answer.
**Recommendation: (a), and I am least confident of this one.** Vanilla's own
`csu_manco_qhapaq` at `birth_date = 1170.1.1` is the same *kind* of evidence as
the Sakya `creation_date = 1073.1.1` that decided Tibet — and Tibet retired TIB
on it. The difference I am leaning on is that TIB was a *hegemony over other
tags* while CSU is two locations that assert nothing beyond themselves.
**Counter:** by the project's own standard (a post-1066 object is retired) (b)
is correct, it costs one rule and one tuple entry, and it puts the right
archaeological name on the Cusco basin at the price of orphaning eight DHE
events that cannot fire before 1340 anyway.

**5. TCP "Tlacōpan" — strip its vassalage only, or retire the tag too?**
**(a) STRIP `TEP → TCP`, keep TCP landed** (recommended, §D.2): the town's
antiquity is arguable [U], its Tepanec vassalage is not [D].
**(b) LEAVE BOTH**: consistent with a maximally light pass, and one fewer line
of code.
**(c) RETIRE TCP TOO**: then `tlacopan` (a `rank = city`) must be granted to TEP
or vacated, and the package's retirements double for a claim no source settles.
**Recommendation: (a).** **Counter:** (a) is the only place where this package
splits a tag from its relation rather than treating them as one object, and a
reviewer could reasonably ask why TNC gets retired and TCP does not when both
are lake-basin Tepanec dependencies. The honest answer is that one has a date
and the other does not.

**6. Should anything at all be done about the 3,948 unowned locations?**
**Recommendation: NO — and this is the decision the package most wants
confirmed.** Every earlier theater found land to vacate; this one finds 88.9%
already vacated, 321 named stateless identities already painting the pops, and
half of vanilla's entire `add_pops_from_locations` coverage. **Counter:** the
converse question is whether a hemisphere that is 89% blank at 1066 is
*playable* — 493 owned locations for 223 tags across two continents is a very
thin map for a player who picks a New World start, and the project has
elsewhere preferred a full map to an empty one (`RUS-STEPPE-PACKAGE.md:461-465`,
CUM over emptiness). That is a game-design question, not a 1066 question, and it
belongs to whoever owns colonisation balance.

---

## Implementation checklist

Ordered so each step can be verified before the next. **Reproduce §E.2's donor
tables first — the delta-guard law makes that the review's job, not the
package's.**

1. **`CAPITAL_FIXES["COC"] = ("mayapan", "chichen_itza")`** appended at
   `build_setup.py:3050`ff. **Re-read the built block first**
   (`MOD/main_menu/setup/start/10_countries.txt:41121`) and confirm
   `capital = mayapan` appears exactly once; `:6440` says so loudly if not.
   `n_cap` in the build report rises by 1 (31 → 32 entries).
2. **`_AMERICAS_RULES = {"TEP": ([], ["tenochtitlan"], [], [], 1)}`** plus the
   resolution loop, modelled on the Tibet loop (`:6031-6045`): resolve, assert
   the exact count, **EXTEND** `LOCATION_GRANTS` (never assign — TEP is a landed
   recipient), then assert TEP's capital `azcapotzalco` is still held. **Observe
   the resolved count = 1.**
3. **`AMERICAS_LANDLESS = ("TNC",)` into `LANDLESS_AFTER`** (`:2995`). The delta
   guard (`:6389`) should stay silent. TNC's claims go 0 → **1**; verify the
   claims-backed guard (`:6352`) passes and that the build **creates** the
   `our_cores_conquered_by_others` block (TNC has none today — the POR/MLL path
   at `:6306-6310`).
4. **The three named strips of §G.1**, with `assert n_americas_deps == 3`.
   Place beside the other named strips (`:7607`, `:7691`), **before** the
   landless sweep at `:7732`.
5. **`n_landless_deps` 280 → 281** (`:7820`) — **observe it failing first**, per
   CLAUDE.md. `n_pacts` stays **9** (`:7850`) and `n_ghosts` stays **156**
   (`:7087`): both measured, both asserted, so a wrong assumption fails the
   build rather than shipping.
6. **Harness constants — under the recommended design exactly ONE moves:**
   `verify_mod.py:1244` parliament `min_count` **1365 → 1364** (TNC was landed
   and reached `parliament_type = assembly` through
   `amerindian_advanced_monarchy_no_coast`; TEP stays landed).
   **Verify, do not assume.** Everything else — `:167`/`:174` 375, `:288` 358,
   `:376` 646, `:413` 179, `:429` 139, `:843` 78, `:884` 27, `:909` 9, `:938`
   2411, `:1086` 125, `:1119` 2414 — stays put, and each was checked against
   the reason it would move.
7. **Optional, per decisions** — OPEN 1b/1c's Toltec tag (registry +1, colour
   +1 in `zz_1066_map_colors.txt`, `_GENERATOR_OK` +1, loc +2,
   `NEW_COUNTRIES` +1, `LANDLESS_AFTER` +1 or +2, blocks 2411 → 2412 and 2414 →
   2415, CoA 125 → 126, loc rows 375 → 377); OPEN 2b's vacate
   (`LOCATION_VACATED["TNC"] = ["anahuac_province"]`, `_EXPECT = 1`, vacated
   625 → 626); OPEN 3c's Yucatán fold (deps 281 → 283, parliament 1364 → 1362,
   strips 3 → 1); OPEN 4b's CSU retirement (`LANDLESS_AFTER` +1, one more rule
   set, parliament 1364 → 1363); OPEN 5c's TCP retirement.

**Break-tests owed** (a check never seen failing is untested):

(a) a bogus single in `_AMERICAS_RULES["TEP"]` must abort;
(b) set the `expected` to 2 and watch the loop abort with the resolved 1;
(c) **omit `"TNC"` from `LANDLESS_AFTER` and watch the delta guard (`:6393`)
    fire** — TNC is emptied by the grant and nothing else would catch it;
(d) **under OPEN 2b only: set `LOCATION_VACATED_EXPECT["TNC"] = 5` and watch
    `:6269-6272` abort with 1** — proving the snapshot intersection excludes
    TEP's `azcapotzalco`, CLC's `chalco`, TCP's `tlacopan` and XCH's
    `xochimilco` from an `anahuac_province` sweep. **This is the delta-guard
    law's own demonstration in this theater: those four donors all survive, so
    only the count assert stands between the design and stolen land**;
(e) misspell `mayapan` in `CAPITAL_FIXES["COC"]` and watch `:6440` abort
    ("capital mayapan not found in COC");
(f) drop one pair from the §G.1 tuple and watch the strip assert fire with 2;
(g) leave `n_landless_deps` at 280 and watch `:7820` abort with 281 printed;
(h) put `tenochtitlan` into a `LOCATION_VACATED` list as well and watch the
    vacate/grant disjointness assert (`:6274-6277`) fire.

## Expected constant moves, collected

| constant | `file:line` | from | to (recommended) | to (all decisions maximal) |
|---|---|---|---|---|
| registry blocks | `zz_1066_new_countries.txt` | **74** | **74 — unchanged** | 75 (OPEN 1) |
| registry overrides | `MOD/in_game/setup/countries/` | 5 files | **5 — unchanged** | 5 |
| `NEW_COUNTRIES` | `build_setup.py:502` | 74 | **+0** | +1 (TOC) |
| `LANDLESS_AFTER` | `:2995` | **313** | **314** (+TNC) | 319 (+XIL +TZC +CSU +XIU +HEL +TCP, −overlaps) |
| `FIELD_FIXES` | `:3123` | 75 tags | **+0** | +0 |
| `CAPITAL_FIXES` | `:3050` | **31** | **32** (+COC) | 32 |
| `LOCATION_GRANTS` | `:3012` | 83 tags | **84** (+TEP's single) | 86 (+TOC, +KKE, +COC) |
| `LOCATION_VACATED` | `:1265` | 18 tags | **18 — unchanged** | 19 (+TNC, OPEN 2b) |
| `LOCATION_VACATED_EXPECT` | `:1273` | 18 keys | **unchanged** | +`{"TNC": 1}` |
| locations granted | build report | current | **+1** | +18 |
| locations vacated | build report | **625** | **625 — unchanged** | 626 |
| unowned locations | measured | **7,950** | **7,950 — unchanged** | 7,951 |
| `UNOWNED_GRANTS` | `:1934` | SNH / 9 | **unchanged — none needed** | unchanged |
| `CONTROL_STRIPS` | `:1720` | TEU / 6 | **unchanged** | unchanged |
| named dependency strips | new, `:7607` shape | — | **3** | 1 (under OPEN 3c) or 4 (under OPEN 5c) |
| `n_landless_deps` | `:7820` | **280** | **281** | 283 |
| `n_pacts` | `:7850` | **9** | **9 — unchanged, measured** | 9 |
| `n_ghosts` | `:7087` | **156** | **156 — unchanged, measured** | 156 |
| empty-IO pin | `verify_mod.py:909` | **9** | **9 — unchanged** (no American IO member exists) | 9 |
| `_MOD_TRIB_OVERLORDS` | `verify_mod.py:766` | 9 tags | **9 — unchanged** | 9 |
| tributary-gate `min_count` | `verify_mod.py:843` | **78** | **78 — unchanged** (all four lines are `vassal`) | 78 |
| country blocks | `verify_mod.py:938`, `:1119` | **2411 / 2414** | **2411 / 2414 — unchanged** | 2412 / 2415 |
| thrones | `verify_mod.py:288`, `:413` | **179** | **179 — unchanged** | 179 |
| new characters / dynasties | — | — | **0 / 0** | 0 / 0 |
| loc rows | `verify_mod.py:167`, `:174` | **375** | **375 — unchanged** | 377 (TOC) or 379 (+OPEN 3d) |
| CoA references | `verify_mod.py:1086` | **125** | **125 — unchanged** | 126 |
| parliament `min_count` | `verify_mod.py:1244` | **1365** | **verify — expect 1364** | verify — expect 1360 |

**Two of the twenty-six constants move under the recommended reading; twelve
under the maximal one.** That is the honest shape of the largest theater on the
map: it is the smallest slice in the project's history.

---

## VERIFICATION

Per CLAUDE.md's say-what-you-verified rule.

- **Verified — the reader, with the FULL ten-key tuple.** `tools/build_setup.py`
  was imported (its `__main__` guard is at `:8216`) and its own `_parse_defs`
  (`:748`), `_ownable_set` (`:772`), `_defs` (`:809`), `_resolve_ruleset`
  (`:815`), `find_block_end` (`:5560`) and `COUNTRY_RE` (`:5613`) were used
  directly. `OWN_KEYS` was copied verbatim from `:5755-5759` — all ten members.
  The reader reproduces **20,922 ownable locations**, **2,337 vanilla and 2,411
  mod country blocks**, `samogitia_area` 16, `courland_province` 8, and — the
  `own_control_integrated` proof — **VTN 32, PLB 40, BTU 6, MGD 5, MUA 15, TIB
  59**, every one a published STATUS-band figure from an earlier package.
  Comments are masked length-preservingly before tokenising.
- **Verified — the pop parser.** `VAN/main_menu/setup/start/06_pops.txt` yields
  **28,559 location blocks / 50,227 `define_pop`** counting lowercase-only keys
  and **28,570 / 50,255** counting the eleven uppercase-containing keys — both
  of `TIBET-PACKAGE.md`'s figures reproduced exactly. (First attempt used a
  one-tab-anchored regex and returned 1 block / 0 pops, because `06_pops.txt`
  indents its location blocks at column 0 inside a `locations={` wrapper. The
  mismatch against the published figure caught it. Recorded because it is the
  anchor class again.)
- **Verified — the vacate ledger.** 7,334 vanilla-unowned + **625** vacated by
  the build − **9** that gained an owner (all SNH's, `UNOWNED_GRANTS`) =
  **7,950 = the mod's measured unowned total**. `HANDOFF.md`'s constant
  reproduced.
- **Verified — the registry regex, and a correction to two earlier packages.**
  A strict `^([A-Z0-9]{2,6}) = \{` over `VAN/in_game/setup/countries/` returns
  **2,246** tags; a loose `^([A-Z0-9]{2,6})[ \t]*=[ \t]*\{` returns **2,340**,
  matching `CLAUDE.md`. The 94-block gap is 92 multi-space declarations plus 2
  tab declarations (`HNV`, `YDR`, `india.txt`). **Four are American: `HIR`
  (`central_north_america.txt:125`), `ZAC` (`mesoamerica.txt:639`), `ZAI`
  (`mesoamerica.txt:648`), `ZIP` (`colombia.txt:11`)** — and ZIP is LANDED with
  five locations. With the loose form the mod-visible index is **2,414**,
  matching `verify_mod.py:1119`.
- **Verified — the theater's shape.** 4,441 ownable locations across the
  fourteen `america` regions (`definitions.txt:5880`); **493 owned by 223 tags,
  3,948 unowned, ZERO double-ownership** (every location tested against all ten
  `OWN_KEYS` across all 2,411 mod country blocks); **6,159 `define_pop`**.
  Vanilla ownership and mod ownership are identical across all 4,441 — measured
  set-for-set, both trees.
- **Verified — the mod has never touched the Americas.** Zero
  American-registry tags appear on any non-comment line of
  `tools/build_setup.py`; zero appear anywhere in `tools/verify_mod.py`.
- **Verified — the `type = pop` model.** All **321** landless American-registry
  tags carry `type = pop` in their `10_countries` blocks; **zero exceptions**.
  **448** `type = pop` countries exist in the build game-wide, **321 of them
  American**. `add_pops_from_locations` coverage: 3,735 locations game-wide,
  **1,853 of them American**.
- **Verified — the Haudenosaunee League's date, from vanilla's own file.**
  `VAN/main_menu/setup/start/15_international_organizations.txt:757-761`,
  `type = tribal_confederation`, **`creation_date = 1142.1.1`**,
  `members = { ONO KKA ONY GYO ONN }`. The build's strip
  (`build_setup.py:6849-6863`, assert `:7172`) removes it; the mod's file
  contains **zero** American tags in any member list, in any instance
  (36 instances remain of vanilla's 53).
- **Verified — Cahokia.** `MOD/main_menu/setup/start/10_countries.txt:56253`
  (`VAN:60930`), registry `eastcoast.txt:367`: **23 locations** (`illinois_area`
  9, `missouri_area` 11, `iowa_area` 1, and kin), **77 `define_pop`**,
  `type = tribe`, `starting_technology_level = 1`,
  `court_language = dhegiha_language`, `capital = cahokia`,
  `reforms = { agricultural_cultivation }`, **no template include**.
  `cahokia_culture` covers 14 locations, `mississippian_ceremonial` 461.
  `VAN/in_game/events/DHE/flavor_CHK.txt` is 23 events / 22
  `dynamic_historical_event` blocks, the first `flavor_chk.1` "The Sunset of
  Cahokia", `from = 1337.1.1 to = 1356.1.1`.
- **Verified — the four dependency lines.**
  `MOD/main_menu/setup/start/12_diplomacy.txt:226 :227 :402 :403`
  (`VAN:515 :516 :815 :816`), quoted in §0.5. The mod file carries **265**
  dependency lines and **28** scripted pact lines (vanilla 647 and 41);
  **zero pact lines name any American tag**, in either tree.
- **Verified — the characters.** All 7,875 blocks in
  `MOD/main_menu/setup/start/05_characters.txt` (7,736 in vanilla's) parsed for
  `tag =`. **Forty-seven name an American tag; the earliest birth is
  `1170.1.1`** (`csu_manco_qhapaq`, `hurin_qusqu_dynasty`, death 1230.1.1).
  Nineteen dynasties are homed on American locations. **No American character is
  alive in 1066.**
- **Verified — the render laws.** `country_name_construction.txt` is 188 lines,
  first-match, read in full; its gated branches name no American tag, culture,
  religion or government type except `country_type = pop` (`:154`); the fallback
  is `:183-186` (`fallback = yes` at `:185`) and its `_map` is bare `"$NAME$"`
  (`government_names_l_english.yml:11-12`). `country_ranks.txt` is 2,741 lines,
  one first-match block `country_flavor` (**line 1, BOM-hidden from a
  `^`-anchored grep**) running to the `rank_county` fallback at `:2553-2555`,
  plus four derived `country_flavor_*` blocks. The American branches and their
  loc strings are enumerated in §0.7 with line numbers, all read directly.
  Culture→language: `wari_culture`, `inka_culture`, `killke_culture`,
  `chanka_culture`, `chincha_culture`, `ychsma_culture`, `huarco_culture` →
  `quechuan_language`; `aimara_culture`, `churajon_culture` →
  `aymara_language`; `yucatec/itza/putun/kiche/mam/kaqchikel/chorti/kowoj/chol/
  huastec` → `maya_language`; `nahua_culture`, `tlaxcaltec_culture`,
  `teco_culture`, `pipil_culture` → `nahuatl_language`; `purepecha_culture` →
  `purepecha_language`; `cahokia_culture` → `dhegiha_language`;
  `kanienkehaka_culture` → `haudenosaunee_language`; `chimu_culture` →
  `quingnam_language` (all `VAN/in_game/common/cultures/`).
  **221 of 223 landed American tags declare no `country_rank`** (ITZ and TAR
  declare `rank_duchy`).
- **Verified — the templates.** Twelve American government templates are in use;
  **every one supplies `parliament_type = assembly`**. Four carry a
  `reforms = { }` block: `amerindian_advanced_monarchy` and
  `..._no_coast` → `altepetl`, `andean_monarchy` → `andean_monarchy`,
  `haudenosaunee_tribe` → `haudenosaunee_clan_mothers`. **51 landed American
  tags carry `altepetl` through their template chain and all 51 are
  `nahua_culture`** — the reform's own `potential`
  (`VAN/in_game/common/government_reforms/country_specific.txt:2685-2693`) is
  satisfied in every case. Walked with a nested, cached include reader (the
  welsh_releasable lesson).
- **Verified — the blocks this package touches.** TNC
  `MOD/…/10_countries.txt:38503` (1 location, 0 claims,
  `capital = tenochtitlan`, `court_language = nahuatl_language`,
  `include = "amerindian_advanced_monarchy_no_coast"`); TEP `:38572` (3:
  `azcapotzalco cuauhtitlan tollan`, **`tolerated_cultures = { toltec_culture }`**);
  TCP `:38593` (1); COC `:41121` (12, `capital = mayapan`,
  `dynasty = cocom_dynasty`, `court_language = maya_language`); XIU `:41140`
  (3); HEL `:41191` (6); CSU `:42931` (2); KKE `:43806` (3); XIL `:40214` (3);
  TZC `:40150` (1); AXO `:38628` (3). **None of the eleven carries a claims
  block.**
- **Verified — the formables and advances.**
  `00_formable_countries.txt`: `USA_f` `:2587`, `CAN_f` `:2617`, `MEX_f`
  `:2650`, `INC_f` `:3332` (frac 0.8, `areas = { acamama_area puna_area }`,
  `potential = { culture.language = language:quechuan_language }`,
  `allow = { religion.group = religion_group:folk_peruvian_group }`), `MAY_f`
  `:3866`, `AZT_f` `:4763` (frac 0.75, `regions = { mesoamerica_region }`,
  `potential = { OR = { religion = religion:nahuatl  culture =
  culture:nahua_culture } }`, **`allow = { owns = location:tenochtitlan }`**).
  **No formable names TNC, TEP, COC, CSU, KKE, CHK or any other landed American
  tag.** Advance trees: `country_AZT.txt`, `country_INC.txt`,
  `country_TNC.txt`, `country_USA.txt`. DHE: `flavor_AZT.txt` (17 events, 16
  DHE blocks, all `tag = TNC`, earliest window 1337.1.1), `flavor_CHK.txt` (23
  / 22, all CHK, 1337.1.1+), `flavor_CSU.txt` (8 / 2, CSU 1340.1.1 and AYA
  1350.1.1), `flavor_usa.txt` (24, no DHE blocks). **Every American DHE window
  opens at 1337.1.1 or later.**
- **Verified — the seam.** Exactly one non-American country block declares
  inline discovery of an American region or area: **GRL**
  (`discovered_areas = { labrador_sea_area }`; `labrador_sea_area` is
  `canada_region` and has **0 ownable locations**). `greenland_area` is filed
  under `north_atlantic_islands_region` / `western_europe`. All nine setup
  templates naming an American region are themselves American templates.
  **Zero tags hold land on both sides of the Atlantic.**
- **Verified — colours and cities.**
  `VAN/main_menu/common/named_colors/02_map.txt` carries **3,742** `map_*`
  definitions (reproducing `TIBET-PACKAGE.md`'s figure). `map_toltec` `:1420`
  `rgb { 38 145 6 }` and `map_aztec` `:1220` `rgb { 136 8 8 }` are used by **no
  country**; `map_toltec` is `toltec_culture`'s own key
  (`cultures/mesoamerican.txt:367`) — the `map_tibetan` class.
  `map_TOC`, `map_TLC`, `map_MAY`, `map_AZT`, `map_CHK`, `map_COC`, `map_TNC`,
  `map_CSU` do not exist. `07_cities_and_buildings.txt` carries **1,019** ranked
  entries (748 town, 261 city, 7 rural_settlement, 3 megalopolis — my regex; the
  Perm/Vyatka figure of 1,108/746/262/3/7 differs slightly and one of the two
  counts is off by a handful, flagged rather than silently reconciled), **25 of
  them American**, including `tenochtitlan`, `mayapan`, `mani`, `noh_peten`,
  `pismachi`, `chakan_putum`, `azcapotzalco`, `tlacopan` and `tetzcoco` as
  `city` and `cahokia`, `chan_chan`, `tzintzuntzan` as `town`.
- **Verified — tag freeness.** 16,226 vanilla and 71 mod text files scanned in
  the three-scan form; 2,414 registry tags indexed BOM-safe, unanchored and with
  the loose whitespace form. **TOC, TLC, TCA, XTL, CZA, MYP free; TLT, TUA, TUL,
  TOL, TLN, CHZ, CHN, KUK taken with a registry `file:line`; MAY, AZT and INC
  taken with EMPTY registries — three PRU-class tags, more than any other
  theater.** The `TUA` row is the scanner earning its keep: `TUA` is NAMED
  "Tula" and is the Caddoan Tula of Arkansas
  (`central_north_america.txt:246`), not Toltec Tollan.
- **Verified — the zero-location definitions.** Across all 20,922 ownable
  locations: **`toltec_culture` 0**, `killke_culture` 4, `inka_culture` 2,
  `wari_culture` 47, `cahokia_culture` 14, `ancestral_pueblo_culture` 7,
  `hohokam_culture` 7, `mogollon_culture` 0, `dorset_culture` 23,
  `beothuk_culture` 26. Of the 544 American registry blocks, **three name a
  `culture_definition` on zero locations** (CLM `teco_culture` — landed; HLK,
  TWK — landless) and **zero name a `religion_definition` on zero locations**.

**Historical claims — every one flagged.**

| claim | flag | note |
|---|---|---|
| Tenochtitlan is founded in 1325 (1345 a minority reading); the island was uninhabited before | **[D]** | the least contested chronological fact in the theater; corroborated inside the repo by vanilla's earliest Mexica character `azt_tenoch`, `birth_date = 1299.1.1` |
| The Tepanec hegemony of Azcapotzalco over the lake basin is c. 1370-1428, ending at the Triple Alliance | **[D]** | |
| Tlacopan/Tacuba predates the Tepanec expansion | **[U]** | the weakest claim behind OPEN DECISION 5 |
| Tula/Tollan is the dominant central-Mexican polity c. 950-1150, collapsing c. 1150-1200 | **[D]** | the Toltec chronology rests on Aztec myth-history (*Anales de Cuauhtitlan*, Sahagún) and no two readings date it alike |
| The Toltec state's territorial extent is not recoverable | **[U]** | the decisive argument in OPEN DECISION 1 |
| Chichén Itzá is the Yucatán hegemon in the Terminal Classic / Early Postclassic, florescence c. 900-1050/1100, decline c. 1100-1200 | **[D]** | |
| Mayapán is founded c. 1180-1220 and its league runs c. 1220-1441 | **[D]** | |
| The Yucatán *cuchcabalob* (Xiu at Mani, Chel, Ah Canul, Cocom at Sotuta…) are the post-1441 political map recorded at Spanish contact | **[D]** | |
| Tayasal / Noh Petén (ITZ's capital) falls in 1697 | **[D]** | the latest-dated capital in the hemisphere |
| Cahokia's "Big Bang" is c. 1050 and Monks Mound is built c. 1050-1100; decline from c. 1200, abandonment c. 1350-1400 | **[D]** | corroborated inside the repo by vanilla's own `flavor_chk.1` window, 1337-1356 |
| The Haudenosaunee League's date is contested: 1142 (astronomical argument) against a mainstream c. 1450-1600 | **[D]** | **vanilla itself picks 1142.1.1** (`15_IO.txt:759`), and either reading is post-1066 |
| Chan Chan is founded c. 850-900; the Chimor state's imperial expansion is c. 1300+ | **[D]** | |
| Tiwanaku collapses c. 1000-1100; the Aymara señoríos consolidate c. 1100-1200 | **[D]** | the señoríos may be slightly early at 1066; the alternative (a surviving Tiwanaku state) is worse and is not shipped |
| Wari collapses c. 1000 | **[D]** | bears on `wari_culture` being a *culture* key, not a state |
| The Inca ruling line begins c. 1200 (Manco Cápac traditional) | **[D]** | **vanilla dates its own `csu_manco_qhapaq` to `birth_date = 1170.1.1`** — an in-repo date, cited before any external source per the creation-date law |
| The Killke archaeological phase occupies the Cusco basin c. 1000-1200 | **[D]** | |
| The Ancestral Pueblo florescence at Chaco is c. 1020-1120; the great houses are abandoned c. 1130-1150 | **[D]** | Chaco is not a location in `definitions.txt`, so nothing rides on this |
| The Hohokam Classic period is c. 1150-1450 | **[D]** | |
| Acoma and Taos are continuously occupied from before 1066 | **[D]** | |
| The Dorset persist in Labrador to c. 1300-1500; the Thule migration is c. 1200-1400 | **[D]** | makes vanilla's Labrador *more* correct at 1066 than at 1337 |
| Norse Greenland is settled 985; the Vinland voyages are c. 1000; the Eastern Settlement survives past 1400 | **[D]** | GRL is the Scandinavian slice's, not this one's |
| Pipil migration into Cuzcatlán is c. 900-1200 | **[D]** | |
| The K'iche' and Kaqchikel highland states are 13th-15th century | **[D]** | |
| The Purépecha (Uacúsecha) state is 13th-century | **[D]** | corroborated by vanilla's own `tar_pauacume_uanacaze`, birth 1220.1.1 |
| The Muisca confederations (Zipa/Zaque) consolidate in the 15th century | **[D]** | ZIP and ZAQ hold 9 locations between them; left |
| The Tairona towns date from c. 900 | **[D]** | |
| No individual ruler anywhere in the western hemisphere is attested by name for 1066.9.15 | **[U]** | the strongest claim in §C, and the one a better-sourced session should re-test first |
| The Mexica were still migrating in 1066 | **[U]** | the brief's own anchor, confirmed only in the negative (no source places them in the basin) |

**OWED CHECKS — four, all in-game, none answerable from any file.**

1. **What rank does the engine derive** for the 221 American tags that declare
   none? At 1-23 locations the plausible derivations are county and duchy, and
   the difference decides whether COC reads **"Ajawil"/"Ajaw"** or
   **"Kuchkabal"/"Halach Winik"**, whether the Nahua altepetl read
   **"Āltepētl"/"Tlahtoāni"** or **"Tlahtohcāyōtl"**, and whether Cahokia reads
   "Tribe"/"Chief" or "Minor Tribe"/"Chieftain". Inherited unresolved from SEA,
   Tibet and Perm/Vyatka. **This theater is the best place to answer it**: 223
   tags at every size from 1 to 23 with a rank word that visibly changes.
2. **Does the mod's own loc file shadow a VANILLA tag's NAME key?** OPEN
   DECISION 3d rides entirely on it, and all 375 existing rows serve mod-created
   tags or invented name keys, so the repo has no instance. Unattested; must be
   proven before it is written.
3. **Do the American DHE chains fire correctly from a 1066 start?** All 63
   American `dynamic_historical_event` windows open at 1337.1.1 or later, i.e.
   271 years in. Nothing in either tree says whether a `dynamic_historical_event`
   whose window opens long after `START_DATE` behaves any differently from one
   that opens at it. Bears on the whole "the flavour layer arrives on schedule"
   claim of §0.4 and §H.
4. **Does a landless shell still satisfy `dynamic_historical_event = { tag = X }`?**
   Under OPEN DECISION 2a a retired TNC keeps its block and its sixteen
   `flavor_AZT` windows. If a landless country is skipped entirely, the events
   are inert (fine). If it is not, sixteen events fire on a country with no
   land — measured nowhere, and the same question a landless TIB raised for
   `country_TIB.txt` and nobody looked.
