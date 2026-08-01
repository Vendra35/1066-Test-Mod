> **STATUS (2026-08-02): ACTED ON as HANDOFF items 30 and 32 (Route B, the
> JAP fix, the Song reskin — landed 2026-08-01).** Two of its claims were
> REFUTED at review (the 18-claim-list cost, the name-key-language check
> premise) — see HANDOFF; code and HANDOFF win where they disagree.

# INDIA, CHINA AND THE REST OF ASIA AT 1066 — review and triage

> **DRAFT — pending main-session review.** Nothing here is approved and nothing
> here has been written to a mod file. This is an audit plus a triage package:
> §1 is implementation-ready, §2–§5 are inventory and pricing, §6 is the list
> of choices only the user can make.
>
> Produced by an Opus research agent, 2026-07-30. Every mechanical claim carries
> a `file:line`. Historical claims that rest only on the agent's knowledge are
> flagged `[U]` (unverified) or `[D]` (disputed) per CLAUDE.md.

## 0. Method, and what "measured" means here

Vanilla probed at `E:\SteamLibrary\steamapps\common\Europa Universalis V\game`;
the required file `in_game/map_data/definitions.txt` is present (491,179 bytes),
so every count below is real.

All location counts were produced by parsing `definitions.txt` into a
`location -> {continent, subcontinent, region, area, province}` map (28,573
locations, 82 regions, 5 nesting levels — note `definitions.txt` is
continent → subcontinent → **region** → area → province → location, so a
region sits at depth 3, not depth 1) and then parsing the mod's generated
`main_menu/setup/start/10_countries.txt` (59,225 lines, 2,380 tag blocks) for
the ten ownership keys the build script itself uses (`own_control_core`,
`own_control_integrated`, `own_control_conquered`, `own_control_colony`,
`own_core`, `own_conquered`, `own_integrated`, `own_colony`, `control_core`,
`control`). Comments were stripped before tokenising — the Byzantium pass's
own lesson (`docs/HANDOFF.md:462`).

**The headline measurement: east of Persia, the mod IS vanilla 1337.** A
tag-by-tag diff of mod vs vanilla holdings across the seventeen eastern regions
returns exactly **two** changed tags, both collateral from the Seljuk pass:

| tag | vanilla | mod | note |
|---|---|---|---|
| DAI | 114 | 73 | Đại Việt lost 41 locations outside Indochina (its Yunnan-side vanilla holdings); its 53 Indochinese locations are untouched |
| QUN | 26 | 6 | Qara'unas cut back by the Seljuk sweep; already on the shatter-watch list (`docs/EU5-ERROR-DECODER.md`, `initialize_from_bookmark.cpp:2477`) |

Everything else — China, India, Japan, Korea, Tibet, Indochina, Indonesia —
is byte-identical to Paradox's 1337 map. That is the premise of this review.

---

## 1. THE ANCHOR — restoring the Middle Kingdom

### 1.1 What was removed, exactly

`tools/build_setup.py:4067-4078` strips every `add_international_organization`
block whose `creation_date` is at or after `START_DATE`. Eighteen instances go;
one of them is the Middle Kingdom, vanilla
`main_menu/setup/start/15_international_organizations.txt:210-271`:

```
:210   add_international_organization = {
:211       type = middle_kingdom
:212       creation_date = 1271.12.18          <-- the strip trigger
:213-229   members = { CHI | CHA DAI | 74 vassals | 126 tusi }
:232       regions = { north_china_region south_china_region west_china_region }
:233-236   areas   = { fujian hubei hunan wuling jiangxi huaixi jiangnan huaidong zhejiang }
:238       leader = CHI
:240-242   celestial_governor = { KOR }
:244-255   ruler_term x12   (Kublai .. Toghon Temür — stripped anyway by build_ios)
:257-265   laws = { delegated_civil_registration_policy rice_based_tax
                    established_provincial_governors free_cefeng_tizhi_policy
                    direct_appointment allow_trade restrict_the_tianxia_policy }
:267-270   variables = { celestial_authority = 75  num_of_celestial_governors = 1 }
```

### 1.2 The IO type's FULL payload — what the engine now misses

Read whole, not just the flagged lines.
`in_game/common/international_organizations/middle_kingdom.txt`:

| lines | construct | what it gives | lost by us? |
|---|---|---|---|
| :6 | `land_ownership_rule = middle_kingdom_land_ownership` | the whole China land-claim ruleset | yes |
| :8-35 | `has_leader_country`, `leader_type = character`, leader block | the Emperor is CHI's ruler (or heir under a regency) | yes |
| :14-16 | `leader_title_key = "EMPEROR_CHINA"`, `title_is_suffix = yes`, `override_ruler_title = yes` | CHI's ruler is *styled* Emperor of China (`international_organizations_l_english.yml:604` → `$chinese_emperor$`) | yes |
| :38-40 | `modifier = { monthly_towards_sinicized = societal_value_monthly_move }` | applies to **every member** | yes |
| :41-43 | `non_leader_modifier = { block_from_change_to_empire_rank = yes }` | members cannot become empires | yes |
| **:69-75** | **`leader_modifier`** — `monthly_prestige = 0.1`, **`cultures_capacity = 50`**, `diplomatic_capacity_modifier = 0.5`, **`allow_tributary_subject = yes`**, `government_size = 1` | the four broken symptoms live here | **yes** |
| :46-53 | `only_leader_country_joins_defensive_wars`, `join_defensive_wars_auto_call` | the Emperor's defensive obligation | yes |
| :127-152 | `on_joined` / `on_left` → `relation_type:exclusive_trade_rights_with_isolated` | trade ring | yes |
| :154-164 | `monthly_effect` — auto-enrols any new CHI subject | the system self-maintains | yes |
| :166-264 | `variables` — `celestial_authority` (0-100, start 70) and `num_of_celestial_governors` (0-4) | the entire Mandate mechanic | yes |
| :266-268 | `payments_implemented = { middle_kingdom_tribute }` | tribute payments | yes |
| :270-272 | `special_statuses_implemented = { celestial_governor }` | governor status | yes |

Verified — every modifier tag above exists and is **Country**-scope:
`cultures_capacity` `docs/EU5-Vanilla-Script-Docs/modifiers.log:494`;
`allow_tributary_subject` `modifiers.log:1946`;
`diplomatic_capacity_modifier` `modifiers.log:855`;
`government_size` `modifiers.log:797`;
`monthly_prestige` `modifiers.log:730`;
`block_from_change_to_empire_rank` `modifiers.log:1382`;
`government_reform_slots` `modifiers.log:793`.

### 1.3 THE FINDING THAT CHANGES THE PLAN

**A government reform CANNOT fix the tusi flood.** The task brief assumed one
restore point; the measurement says the tusi half of the class is gated on the
IO's *existence*, not on a modifier.

`in_game/common/subject_types/tusi.txt:6-11` — the `visible` trigger is
`can_country_have_tusi = yes` on the overlord. And
`in_game/common/scripted_triggers/country_triggers.txt:1286-1303`:

```
:1286   can_country_have_tusi = {
:1287       exists = international_organization:middle_kingdom      <-- HARD GATE
:1288           OR = {
:1289               is_leader_of_international_organization = international_organization:middle_kingdom
:1291-1293          AND = { is_subject = yes  subject_type ?= subject_type:tusi }
:1295-1301          AND = { ... is_subject_of = middle_kingdom.leader_country
                             overlord ?= { culture ?= prev.culture } }
```

Line 1287 is unconditional. No `country_modifier` on any tag can satisfy it.
(The engine's own Reason lines cite 1288-1298 — the OR body — which is why the
decoder entry reads that way; the fatal line is 1287, one above.)

So the two candidate routes are **not** equivalent:

| route | kills 3702 CHA/DAI (2 lines) | kills 3702 tusi (126 lines) | kills 9635 CHI cultures | kills the 56-line IO-link class | vanilla content restored |
|---|---|---|---|---|---|
| **A. `song_mandate_reform`** (ABS/khutba pattern) | yes | **no** | yes | no | none |
| **B. Restore the IO instance, re-dated** | yes | yes (see risk) | yes | yes | 54 files' worth |

Restoring the instance is also what unblocks vanilla's Chinese content at
large: **54 files** under `in_game/` reference
`international_organization:middle_kingdom` (325 individual references) —
`common/casus_belli/unify_china.txt`, `common/laws/20_middle_kingdom.txt`,
`common/disasters/crisis_of_the_chinese_dynasty.txt`,
`common/formable_countries/00_formable_countries.txt`,
`common/situations/red_turban_rebellions.txt`, three country_interactions,
three building_types, the imperial-examination and Confucian event files, and
eight `events/DHE/flavor_*` files. With the instance gone, all of it is inert
or erroring, silently.

**Recommendation: Route B, with Route A's reform as the named fallback.**

### 1.4 Route B — implementation spec

**Where.** `tools/build_setup.py`, inside `build_ios()` (`:4046`), BEFORE the
future-instance strip loop at `:4067`. Same shape as the High Kingship surgery
at `:4093-4127` and the HRE surgery at `:4143-4171`: locate the block by
`type = middle_kingdom`, assert it exists exactly once, rewrite in place.

**Edits to the instance, in order:**

1. **`creation_date = 1271.12.18` → `creation_date = 960.2.4`** — the Song
   proclamation [U]. Any pre-`START_DATE` date works mechanically; this one is
   defensible and keeps the "IOs are dated when they were founded" convention.
   Assert the pattern matches exactly once before substituting, and assert
   afterwards that no `creation_date >= START_DATE` survives — `build_ios`
   already runs that check at `:4264-4266`.

2. **Members.** Vanilla's list (`:213-229`) is CHI + CHA/DAI + 74 vassals +
   126 tusi. Two constraints already enforced by the harness:
   - the "IO members hold land" check (753 items, added in the British slice,
     `docs/HANDOFF.md:750-753`) will fail on any landless member, so the
     member list must be filtered through the same generic landless sweep the
     other IOs get (`build_ios:4195-4218`);
   - `middle_kingdom.txt:87` — `can_join_trigger` contains
     `NOT = { country_rank = country_rank:rank_empire }`. That is a *join*
     trigger, not a setup validator, so setup members are not checked against
     it; but if any 1066 redraw makes a member an empire, expect noise.

   For a **minimal** anchor pass, keep vanilla's member list verbatim minus
   landless tags. It is wrong for 1066 in detail (§2) but it is *consistent*,
   and every later China slice edits it with the same surgery.

3. **`leader = CHI`** — keep (`:238`). CHI is the tag the engine styles as
   Emperor; `leader_type = character` derives the person from the leader
   country's ruler (`middle_kingdom.txt:17-35`), and CHI currently carries
   `ruler = random` (`10_countries.txt:26322`), which the engine fills. This
   is the same `leader = <TAG>` seeding proven twice already — the High
   Kingship (`leader = LEI`) and the catholic_church precedent
   (`15_international_organizations.txt:182`).

4. **`celestial_governor = { KOR }` (`:240-242`) — REMOVE.** Goryeo was a
   tributary of Liao in 1066, not a provincial governorship of China [U]. It
   is also the single member most likely to look absurd to a player. Removing
   it leaves `num_of_celestial_governors` start value to the IO type's own
   default (`middle_kingdom.txt:167-172`, `start = 1`); set the instance
   variable `num_of_celestial_governors = 0` to match.

5. **`variables` (`:267-270`)** — keep `celestial_authority = 75` or lower it.
   75 is Kublai's consolidated Yuan; a Song two years into Yingzong's short
   reign under an activist bureaucracy is arguably lower [U]. Cosmetic;
   recommend leaving 75 in the anchor pass and revisiting with §2.

6. **Laws (`:257-265`)** — all seven options exist and none is date- or
   advance-gated: `delegated_civil_registration_policy`
   `in_game/common/laws/20_middle_kingdom.txt:33`, `rice_based_tax` `:236`,
   `established_provincial_governors` `:515`, `free_cefeng_tizhi_policy`
   `:875`, `direct_appointment` `:1231`, `allow_trade` `:1435`,
   `restrict_the_tianxia_policy` `:1717`. Keep as-is for the anchor pass.

7. **`ruler_term` x12 (`:244-255`)** — no action needed; `build_ios:4052`
   already strips every `ruler_term` from the IO file before anything else runs.

**Assertions to add (each proven by breaking, per CLAUDE.md):**
- the `type = middle_kingdom` block is found exactly once, and its
  `creation_date` reads `1271.12.18` before substitution (a patch that changes
  it upstream must fail loudly, not silently skip);
- after substitution, the instance survives the future-strip loop (count of
  removed instances drops 18 → 17 — move that constant in the same commit and
  observe it failing first);
- `leader = CHI` is present and CHI holds land;
- `celestial_governor` is absent;
- no member of the instance is in `LANDLESS_AFTER`.

**Harness:** raise the IO-instance count check and add "the Middle Kingdom
exists and its leader holds land" (1 item). The existing "IO members hold
land" check (753 items) will grow by the retained members — record the new
number in the same commit.

### 1.5 Route A — the fallback reform, spec'd in full

If Route B is rejected, or if the restored IO produces a class of failure worse
than the one it cures, this is the honest partial fix. It follows the four
landed khutba-pattern reforms in
`in_game/common/government_reforms/zz_1066_reforms.txt` exactly
(`seljuk_khutba_reform:28-41`, `seljuk_nizamiyya_reform:55-68`,
`fatimid_khutba_reform:78-91`, `capetian_homage_reform:102-115`,
`papal_investiture_reform:124-137`), whose model is vanilla's
`malian_tribute_system` (`in_game/common/government_reforms/country_specific.txt:3917`)
and whose `cultures_capacity` precedent is the SE-Asian mandala reform
(`country_specific.txt:3909`, `cultures_capacity = 3`).

```
# The Mandate of Heaven. Restates, on the tag itself, what the Middle
# Kingdom IO's leader_modifier gave the Emperor of China
# (in_game/common/international_organizations/middle_kingdom.txt:69-75)
# and which our future-IO strip (tools/build_setup.py:4067-4078,
# creation_date = 1271.12.18) removed. Country-scope modifier tags all
# verified in docs/EU5-Vanilla-Script-Docs/modifiers.log:
#   cultures_capacity :494   allow_tributary_subject :1946
#   diplomatic_capacity_modifier :855   government_size :797
#   monthly_prestige :730    government_reform_slots :793
# government_reform_slots = 1 so the reform does not consume a slot —
# user request 2026-07-29, vanilla's own revolutionary_empire pattern
# (government_reforms/monarchy.txt:169).
# KNOWN LIMIT: this does NOT restore the ~126 tusi dependencies.
# in_game/common/scripted_triggers/country_triggers.txt:1287 gates
# can_country_have_tusi on `exists = international_organization:
# middle_kingdom`, which no country_modifier can satisfy.
song_mandate_reform = {
	potential = {
		tag = CHI
	}
	allow = {
	}

	country_modifier = {
		allow_tributary_subject = yes
		cultures_capacity = 50
		diplomatic_capacity_modifier = 0.5
		government_size = 1
		monthly_prestige = 0.1
		government_reform_slots = 1
	}

	years = 4
}
```

**Magnitude decision — `cultures_capacity = 50`.** Restate vanilla's number,
do not re-derive it. CHI's setup carries **9 accepted + 74 tolerated = 83
cultures** (`10_countries.txt:26325-26410`); the engine measured its cost at
56.45 against a capacity of 6 (`country.cpp:9635`, decoder entry). The Seljuk
precedent shows the danger of guessing low: `seljuk_nizamiyya_reform` shipped
at +3, was measured insufficient in play, and had to be recalibrated to +6
(`zz_1066_reforms.txt:43-54`). 50 is Paradox's own figure for exactly this
country and exactly this culture list. Do not shave it.

**Assignment:** `reforms = { song_mandate_reform }` inside CHI's
`government` block — the block already exists at `10_countries.txt:26319-26321`
and currently holds `legacy_of_kublai_khan`. Written by `build_setup.py`
through the same mechanism that assigns SEL's and FAT's reforms.

**Which tags get it: CHI only.** Nothing else in the east is an overlord that
fails the tributary gate. All 126 tusi overlords fail on the IO gate instead
(LNG 62, CHI 19, SZH 12, BZU 7, QYN 4, QJG 4, SDG 3, and eleven more with 1-2
each) and are beyond this reform's reach.

**Loc keys required** (the harness sweeps every mod reform for these —
`docs/HANDOFF.md:588`): `song_mandate_reform` and `song_mandate_reform_desc`
in `main_menu/localization/english/`. Suggested name: "The Mandate of Heaven".

### 1.6 Expected error.log delta — all four classes, named

| class | lines | Route A | Route B |
|---|---|---|---|
| `government.cpp:3702 — Subject type 'tributary' is invalid for 'CHA'/'DAI' … Reason: common/subject_types/tributary.txt line: 20 … 24` (`12_diplomacy.txt:586-587`) | 2 | **gone** | **gone** |
| `government.cpp:3702 — Subject type 'tusi' is invalid for '<TAG>' … Reason: country_triggers.txt:1288-1298` (`12_diplomacy.txt`, 126 dependencies) | 126 | remains | **gone** (risk below) |
| `country.cpp:9635 — Country CHI Yuán starts with <N> out of <M> accepted or tolerated cultures` + the `ACCEPTED_CULTURE_SETUP_ERROR_IF_ABOVE_MAX` tooltip | 1+ | **gone** | **gone** |
| `jomini_script_system.cpp:252 — Event target link 'international_organization' returned an invalid object` at `common/country_interactions/demand_silver_tribute.txt:8` and `demote_celestial_governor_to_vassal.txt:9` | 56 | remains | **gone** |

Total at stake: **185 log lines**, against a ~53-line "healthy" baseline
(`docs/HANDOFF.md:48`). This is the single largest remaining mod-side error
class in the build.

**The one risk in Route B, stated plainly.** Of the 126 tusi, only CHI's 19
pass `can_country_have_tusi` through branch 1 (`:1289`, is-leader). The other
107 belong to overlords who are themselves CHI vassals and must pass through
branch 3 (`:1295-1301`), which additionally requires
`overlord ?= { culture ?= prev.culture }` — CHI's country culture must equal
the vassal's. Whether that holds is **not statically determinable** (country
culture is derived at init, not written in setup) and must be measured. If
those 107 lines survive the restore, the deterministic fallback is a
`build_diplomacy` conversion of the residual tusi dependencies to `vassal` —
which is what the engine silently does to them today anyway, only loudly.

Note also the `prev` law here (CLAUDE.md): `AND` is transparent, `overlord ?= {}`
is one hop, so `prev` inside it lands on the country under test, not on the
overlord. Vanilla's construct is correct; do not "fix" it.

---

## 2. CHINA 1066 — audit and triage

### 2.1 What the map actually shows today

**CHI = the Yuán, entire.** `10_countries.txt:26092` — the block is literally
commented `#Yuán`, and:

| field | value | line |
|---|---|---|
| holdings | **1,661 locations** | :26093-26301 |
| capital | `dadu` (Khanbaliq/Beijing) | :26411 |
| rank | `rank_empire` | :26412 |
| flag / name | `"YUA"` / `"YUA"` | :26413-26414 |
| reform | `legacy_of_kublai_khan` | :26320 |
| law | `status_of_the_han_law = limit_the_han_powers` | :26316 |
| societal | `sinicized_vs_unsinicized = -50` `# Bayan's policies` | :26313 |
| court language | `northern_mandarin_dialect` | :26325 |
| cultures | 9 accepted + 74 tolerated | :26326-26410 |

Its 1,661 locations break down: north China 519, east China 488, west China
286, south China 169, **Manchuria 109, Mongolia 89**, Tibet 1. The Mongolia
and Manchuria holdings alone (198) are the Yuan's steppe homeland — the single
most visible anachronism on the eastern map, since in 1066 that ground belonged
to the Liao and to unconsolidated Jurchen and Mongol tribes [U].

**Everything around it is Yuan-collapse-era too.** Nine steppe hordes named for
Genghis's brothers and sons hold Mongolia and Manchuria — CRS Choros 37,
QAS Qasar 19, BAT Baatud 18, BGT Belgutei 17, KHD Khoid 16, HCN Hachiun 21,
OTC Otchigin 23, OGE Ögedei 19 — none of which can exist before 1206 [U].
LNG "Liang" (`10_countries.txt`, Kunming, 17 locations) is the Yuan Prince of
Liang's Yunnan appanage and holds **62 tusi subjects plus CDL Dali as a
vassal** (`12_diplomacy.txt:382`), which inverts the 1066 relationship
entirely: Dali was a sovereign kingdom and Yunnan was not Chinese [U].

### 2.2 Is vanilla's tag structure usable for a Song?

**Yes, and cheaply.** Vanilla separates the *state* from the *dynasty*:

- `CHI = { #China }` — `in_game/setup/countries/east_asia.txt:1139` — is the
  Chinese state, and wears whichever dynasty's flag and name the setup gives
  it. That is why the 1337 block sets `flag = "YUA"` / `country_name = "YUA"`.
- `CSO = { #Song }` — `east_asia.txt:1169` — exists as an identity-only block
  with `color = map_CSO`, `color2 = rgb { 153 51 51 }`,
  `culture_definition = zhongyuan_culture`, `religion_definition = sanjiao`,
  `is_historic = yes  #Released during the Crisis events`.
- Localisation ships: `CSO: "Sòng"` and `CSO_ADJ: "Sòng"` —
  `main_menu/localization/english/country_names_l_english.yml:3004-3005`.
  (Siblings: `CHI: "China"` :2998, `YUA: "Yuán"` :3000, `MNG: "Míng"` :3002.)

So **`flag = "CSO"` + `country_name = "CSO"` on CHI turns the Yuán into the
Sòng — two token changes.** No new tag, no new loc, no new colour. This is the
same mechanism the Sardinia and Iberia slices used and it is already proven in
this repo's builder.

`zhongyuan_culture` is in CHI's *accepted* list today (`:26328`) — so the
dynasty definition and the state's culture profile already agree.

### 2.3 Which 1337 tags are flatly impossible at 1066

| tag | what it is | founded | 1066 reality | holdings |
|---|---|---|---|---|
| CHI-as-YUA | Yuán | 1271 | Northern Song under Yingzong (r. 1063-1067) [U] | 1,661 |
| LNG | Liang (Yunnan appanage) | 14th c. [U] | Dali kingdom, sovereign | 17 (+62 tusi, +CDL vassal) |
| CRS QAS BAT BGT KHD HCN OTC OGE | Chinggisid brother/son hordes | 1206+ [U] | scattered Mongol/Tatar tribes | 170 combined |
| SYG | Shenyang (Yuan Liaoyang province) | [U] | Liao Eastern Capital | 27 |
| JAP-as-ASK | Ashikaga shogunate | 1336 | Heian court under Go-Reizei [U] | 339 |
| MAJ | Majapahit | 1293 [U] | post-Srivijaya Java | 32 |
| PIN | Pinya | 1313 [U] | **Pagan under Anawrahta** [U] | 26 |
| SUK | Sukhothai | 1238 [U] | Khmer/Mon ground | 20 |
| LNA | Lan Na | 1292 [U] | — | 21 |
| VTN | Vientiane / Lan Xang | 1353 [U] | — | 32 |
| PEG | Pegu / Hanthawaddy | 1287 [U] | Mon Thaton, Pagan's target | 28 |
| ARK | Arakan (Launggyet) | 1237 [U] | — | 17 |

**There is no PAG/Pagan tag.** `PAG` returns nothing in
`in_game/setup/countries/`; the whole SEA set is `south_east_asia.txt`'s 56
tags, all 1337-era. Anawrahta's Pagan — the largest 1066 polity in mainland
SEA — would have to be **invented**, or PIN reused with its name and colour
overridden. Vanilla does ship `pagan_dynasty: "Pagan"`
(`dynasty_names_l_english.yml:1003`) and `pagan` is a real location
(`location_names_l_english.yml:5461`, `pagan_province`
`province_names_l_english.yml:3294`), so the identity material exists.

### 2.4 Where vanilla is nearly right for 1066

Four genuine near-misses. These are the cheap end of China.

- **KOR = Goryeo.** `country_names_l_english.yml:1515-1516` literally reads
  `KOR: "Goryeo"`. 133 locations, capital `kaesong` — Goryeo's actual capital.
  The dynasty key `wang_dynasty: "Wang"` exists
  (`dynasty_names_l_english.yml:1588`) and Goryeo's house *was* Wang [U].
  KOR needs a ruler and the removal of its CHI vassalage; the territory is
  right. **CHEAP-WIN.**
- **JAP = Heian Japan.** 339 locations under one tag, capital `kyoto`,
  `rank_empire`. A single imperial Japan is *more* correct for 1066 than for
  1337. Two edits: `flag`/`country_name` off `"ASK"`, and the reform (§4).
  **CHEAP-WIN.**
- **CDL = Dali.** `CDL: "Dali"` `country_names_l_english.yml:3260-3261`,
  capital `taihe_dali`, `rank_kingdom`, 12 locations. Correct polity, correct
  seat, wrong size and wrong overlord (LNG vassal, `12_diplomacy.txt:382`).
- **DAI = Đại Việt, CHA = Champa.** Both correct polities at 1066 with correct
  capitals (`thang_long`, `vijaya`) and roughly correct extents (53 and 21).
  Their tributary status under CHI is *historically right* [U] — it is only
  the engine gate that breaks it, which §1 fixes.
- **TIB.** 59 locations, capital `sakya` — the Sakya hegemony is 1264+ [U]; at
  1066 Tibet was fragmented (the era of fragmentation). But 22 Tibetan tags
  already hold 199 of the region's 349 locations, so the fragmentation is
  *already on the map*; only TIB's 59-location primacy and its `sakya` capital
  are wrong.

### 2.5 CHINA TRIAGE TABLE

| tier | item | what it costs | locations | tags | new characters |
|---|---|---|---|---|---|
| **MUST-FIX** | The Middle Kingdom anchor (§1) | one builder function, one date, one member filter | 0 | 1 (CHI) | 0 |
| **MUST-FIX** | CHI reskin Yuán → Sòng: `flag`/`country_name` → `"CSO"`, drop `legacy_of_kublai_khan`, drop `status_of_the_han_law`, capital `dadu` → `kaifeng` | four token edits in the builder | 0 | 1 | 0 |
| **MUST-FIX** | JAP reform `shogunate` → `japanese_imperial_family` (§4 — the reform is currently *invalid at start*) | one token + one ruler | 0 | 1 | 0 |
| **CHEAP-WIN** | Ruler seats: Japan, Goryeo, Đại Việt, Champa, Dali, Khmer (§4) | HISTORICAL_RULERS entries | 0 | 6 | 4-6 |
| **CHEAP-WIN** | CHI drops Mongolia + Manchuria (the Yuan homeland): 198 locations to landless-or-tribal | one grant rule; recipients already exist | 198 | ~10 | 0 |
| **CHEAP-WIN** | Retire the eight Chinggisid hordes to landless-with-claims (the BYZ_LANDLESS shape) | 170 locations released, LANDLESS_AFTER entries | 170 | 8 | 0 |
| **CHEAP-WIN** | LNG landless; CDL freed from LNG and given LNG's 17 | inverts one wrong vassalage | 17 | 2 | 0-1 |
| **EXPENSIVE-DEFER** | **The Liao.** A new tag (or SYG reskinned) taking the Sixteen Prefectures + Manchuria + eastern Mongolia | new tag, culture/religion decisions, a Khitan dynasty | ~450-500 est. | 1 new + ~15 donors | 3-5 |
| **EXPENSIVE-DEFER** | **Western Xia.** A new tag over Hexi/Gansu/Ordos | new tag, Tangut culture check | ~110 est. (`hexi_area` 54 + `gansu_area` 29 CHI-held, plus Ordos) | 1 new | 2-3 |
| **EXPENSIVE-DEFER** | **Pagan under Anawrahta** — invent PAG or reskin PIN, absorb PEG/SAG/BPR/TNG | new tag or heavy reskin | ~80-90 est. | 1 new + 6 donors | 2-3 |
| **EXPENSIVE-DEFER** | Retire SUK/LNA/VTN/ARK/MAJ (all post-1066 foundings) and give the ground to Khmer/Pagan/Srivijaya | six landless retirements + redistribution | ~140 | ~10 | 0-2 |
| **EXPENSIVE-DEFER** | Tibet's 1066 fragmentation (TIB's 59 + capital) | research-heavy, low visibility | 59 | ~5 | 0 |
| **EXPENSIVE-DEFER** | The 126 tusi web as *1066* frontier prefectures | depends on §1's measurement | 0 | 18 overlords | 0 |

**Totals.** MUST-FIX: 3 items, 0 locations moved, 3 tags. CHEAP-WIN: 4 items,
**385 locations**, ~26 tags, 4-7 new characters. EXPENSIVE-DEFER: 6 items,
**~840-900 locations**, ~40 tags, 7-13 new characters, 3 invented tags.

---

## 3. INDIA 1066 — audit and triage

### 3.1 The Delhi problem

`DLH` is `in_game/setup/countries/india.txt:1` and in the mod holds **369
locations** (`10_countries.txt`, capital `sargadwari`, `rank_kingdom`,
`include = "indian_muslim_monarchy"`, `religious_school = chishti_school`,
reforms `taluqdar_nobility` + `indian_sultanate_reform`,
`iqta_law = lenient_taxation`). Vanilla's own comment on the capital reads
*"Originally Delhi but moved recently to Daulautabad in Deccan / In 1337 the
capital has been temporarily transferred to Sargadwari due to famine and
disease in Delhi"* — this block is dated to the month.

The Delhi Sultanate was founded in 1206 [U]. **It is the single largest
impossible object on the 1066 map after the Yuán.** Its 369 locations spread
across five regions:

| area | DLH holdings |
|---|---|
| punjab_area | 97 |
| maharashtra_area | 37 |
| doab_area | 35 |
| malwa_area | 35 |
| awadh_area | 24 |
| bhojpur_area | 24 |
| rajputana_area | 21 |
| mithila_area | 19 |
| karnakassala_area | 15 |
| gondwana_area | 13 |
| rokhilkhand_area | 12 |
| gujarat_area | 12 |
| konkan_area | 9 |
| vidarbha_area | 9 |
| jharkhand_area | 6 |
| telingana_area | 1 |

### 3.2 The Ghaznavid question — answered

**GHZ does NOT cover Lahore, and it is not a vanilla tag.** GHZ is one of this
project's own inventions, registered at
`in_game/setup/countries/zz_1066_new_countries.txt:200` (`GHZ = { #Ghaznavids`,
`color = map_GHZ`) by the Seljuk slice. It holds **34 locations, every one of
them in `persia_region`** — `sistan_area` 31 and `baluchistan_area` 3:
Ghazni, Kabul, Kandahar, Quetta, Jalalabad, Gardez, Bost, Gereshk and 26 more.
Capital `ghazni`.

Meanwhile `lahore`, `multan` and `peshawar` are all in
`hindustan_region / punjab_area` (`definitions.txt:3714`, 141 locations in the
area) and all three are held by **DLH**, in both vanilla and the mod.

At 1066 the Ghaznavid empire under Ibrahim (r. 1059-1099) was precisely
Afghanistan **plus** the Punjab, with Lahore as its second capital and the
engine of its Indian raids [U]. So GHZ is missing its whole Indian half.

**This is the cheapest correct move in India:** DLH's 97 punjab_area
locations → GHZ. That single grant simultaneously (a) makes the Ghaznavids
historically shaped, (b) removes the Delhi Sultanate from the Punjab, and
(c) costs one rule in `_GRANTS`, no new tag, no new character — GHZ already
has Ibrahim's slot open. GHZ would go 34 → 131.

### 3.3 What vanilla ships for India — and what it does not

`india.txt` holds **101 tags**, and they are the *Tughlaq-era* set. Checked
against the 1066 dynasties:

| 1066 polity [U] | vanilla tag? | verdict |
|---|---|---|
| Ghaznavid Punjab (Ibrahim) | GHZ (ours) + DLH's punjab | **reusable** — grant, §3.2 |
| Chauhans of Shakambhari | — | no tag; `DRW` is "Chauhans of Dadrewa" (2 locations) |
| Chandelas of Kalinjar (Kirtivarman) | **JJK** `india.txt:537`, capital `kalinjar`, comment *"What remains of the Chandella dynasty"* | **reusable** — 2 locations, needs growth |
| Paramaras of Malwa (Jayasimha) | — | no tag; `paramara_dynasty` exists (`dynasty_names_l_english.yml:1010`) |
| Solankis/Chaulukyas of Gujarat (Karna) | — | no tag; `Solanki` is a character-name pool entry only (`character_names_l_english.yml:2067`) |
| Kalachuris of Tripuri (Karna) | **RTP** `india.txt:587`, capital `ratnapura`, comment *"The remains of the ancient Haihaya/Chedi"* | **reusable** — 18 locations |
| Palas of Bengal (Vigrahapala III) | — | no tag; `Pala` is a name-pool entry (`character_names_l_english.yml:30719`) |
| Senas | — | correctly absent (Sena rule begins c. 1097 [U]) |
| Cholas (Virarajendra) | — | **no tag**; `Chola` name-pool entry only (`character_names_l_english.yml:6536`) |
| Western Chalukyas (Someshvara I) | — | **no tag**; `Chalukya` name-pool entry only (`character_names_l_english.yml:6481`) |
| Eastern Gangas | — | no tag; `ORI` (Kataka, 21) is the seat |
| Hoysalas (Vinayaditya I) | **HSL** `india.txt:11` | **reusable and already peopled** — see §4 |
| Pandyas | **TNK** — `TNK: "Pandya"` `country_names_l_english.yml:457`, `pandya_dynasty` `:1007` | **reusable** — 4 locations |
| Kakatiyas | **MSN** `india.txt:189` (Musunuri, capital `warangal`) + `kakatiya_dynasty` `:649` | reusable seat, wrong tag identity |
| Soomras of Sindh | **SND** `india.txt:369` + `soomra_dynasty` `:1201` | **reusable** |
| Guhilas of Mewar | **MEW** `india.txt:312`, capital `chittor` | **reusable** |
| Yadavas/Seunas | `yadava_dynasty` `:1618`, no tag | — |

**Flatly impossible at 1066** (all [U] on foundation dates): DLH (1206, 369),
VIJ Vijayanagara (1336, 36), MAB Madurai Sultanate (1335, 26), SMA Samma of
Sindh (1351, 25), RDY Reddi (1325, 18), RCH Recherla (1325, 15), JFN Jaffna
(1215, 4), DBD Dambadeniya-line Kurunegala (1220s, 20), SMV Sambuvaraya (13th
c., 7), MSN Musunuri (1326, 20). That is **560 locations across ten tags**
that cannot be what they say they are.

**The structural verdict: India cannot be made historical cheaply.** Four of
its five great 1066 powers — Chola, Western Chalukya, Pala, Paramara — have no
tag at all. A faithful India is an invent-a-country project of the Taifa
Factory's size (that slice created 13 states and moved 244 locations,
`docs/HANDOFF.md:388`), and probably larger.

### 3.4 INDIA TRIAGE TABLE

| tier | item | locations | tags | new characters |
|---|---|---|---|---|
| **MUST-FIX** | DLH's 97 punjab_area locations → GHZ (§3.2). Fixes the Ghaznavids and evicts Delhi from the Punjab in one rule. | 97 | 2 | 0 (GHZ's seat is a separate item) |
| **MUST-FIX** | DLH **beheaded**: the remaining 272 locations released and DLH goes landless-with-claims (the GRA/MAM/POR shape, `docs/HANDOFF.md:388`/`:612`). The Sultanate's 1206 foundation becomes the future, exactly as MAM's 1250 does in Egypt. | 272 | 1 + recipients | 0 |
| **CHEAP-WIN** | Seat HSL on **Vinayaditya I** — vanilla already ships him (§4) | 0 | 1 | 0 |
| **CHEAP-WIN** | Retire the nine other impossible tags (VIJ MAB SMA RDY RCH JFN DBD SMV MSN) to landless-with-claims | 191 | 9 | 0 |
| **CHEAP-WIN** | Rename/reseat the three surviving 1066 lineages already on the map: JJK → Chandela, RTP → Kalachuri, TNK → Pandya (loc override + dynasty, all three dynasty keys ship) | 0 | 3 | 3 |
| **EXPENSIVE-DEFER** | **Tier 1 India — the four missing great powers.** New tags for Chola, Western Chalukya, Pala, Paramara + Solanki. New dynasties for all five (only `hoysala`/`kakatiya`/`pandya`/`chandela`/`paramara`/`soomra`/`yadava` ship as dynasty keys; Chola, Chalukya, Pala, Solanki, Kalachuri exist only as name-pool strings and need `04_zz_1066_dynasties.txt` entries) | ~500-600 est. (the 272 released by DLH + the 191 from the retirements + Deccan redistribution) | 5 new + ~25 donors | 8-12 |
| **EXPENSIVE-DEFER** | **Tier 2 India — the Rajput and central belt.** Chauhan, Gahadavala, Tomara, Chandela growth, Kalachuri growth | ~150 est. | 3-5 new | 5-8 |
| **EXPENSIVE-DEFER** | **Tier 3 India — the far south and Sri Lanka.** Chola supremacy over Pandya/Kerala, the Chola occupation of Anuradhapura and Vijayabahu I's Ruhuna [U] | ~120 est. (`tamil_land_area` 58, `sailan_area` 25, `malabar_area` 31) | ~8 | 3-5 |
| **EXPENSIVE-DEFER** | The 4 `hindu_branch` IO member lists (`15_international_organizations.txt:1139/1157/1175/1190`) rewritten for whatever India becomes — the "IO members hold land" harness check will force this | 0 | ~60 named members | 0 |
| **EXPENSIVE-DEFER** | The 22 `samanta` dependencies (`12_diplomacy.txt`) re-pointed | 0 | ~25 | 0 |

**Totals.** MUST-FIX: 2 items, **369 locations**, ~15 tags touched, 0 new
characters. CHEAP-WIN: 3 items, 191 locations, 13 tags, 3 new characters.
EXPENSIVE-DEFER: 5 items, **~770-870 locations**, ~100 tags, 16-25 new
characters, **8-10 invented tags**.

**Price comparison for the user:** the MUST-FIX floor for India is one grant
rule and one landless retirement — comparable in effort to the Sardinia slice
(27 locations, `docs/HANDOFF.md:358`) despite moving 369, because both moves
are wholesale and need no new identity. The full-fidelity India is bigger than
the Taifa Factory and the Byzantium slice combined.

---

## 4. Cheap ruler seats — the batch candidate

The Yemen/Tunis precedent: a tag whose borders are roughly right and which
needs only a person. Sorted by confidence.

### 4.1 Already in vanilla's character data — zero authoring

A sweep of the mod's `main_menu/setup/start/05_characters.txt` (7,841 dated
characters) for anyone **born 1000-1050 with no `death_date`** — i.e. an adult
alive at `START_DATE` under the two engine laws (`docs/HANDOFF.md:9-22`) —
returns **278 candidates**, of whom **97 are eastern**:

| tag | ruler | character key | b. | dynasty | name key | flags |
|---|---|---|---|---|---|---|
| **JAP** | Emperor **Go-Reizei** | `jap_go_reizei_tenno` | 1025 | `yamato_dynasty` | `name_chikahito` | [U] on the regnal display; the accession is 1045 [U] |
| — | Go-Sanjō (successor, acc. 1068) | `jap_go_sanjou_tenno` | 1034 | `yamato_dynasty` | `name_takahito` | banked for a succession event |
| **HSL** | **Vinayaditya I Hoysala** | `hsl_vinayaditya_i_hoysala` | 1020 | `hoysala_dynasty` | `name_vinayaditya` | kannadiga; the *actual* 1066 Hoysala [U] |
| ADH | Narai of Lavo | `adh_narai` | 1020 | `lavo_dynasty` | `name_narai` | [D] — Lavo's king-list is legendary |

Plus **93 Japanese clan heads** born 1000-1050 with no death date —
Fujiwara (18, incl. `jap_fujiwara_morozane` b1042), Taira (11), Minamoto (10,
incl. `jap_minamoto_yoshiie` b1039), Munakata (5), Kudou (5), and 44 others
across `saigoku_culture` (70), `tougoku_culture` (15) and `kyushu_culture` (9).
**Vanilla ships the entire 1066 Japanese aristocracy, alive and ready.** None
of it is used today because JAP is one tag; it is the raw material for any
future Japan slice at zero authoring cost.

### 4.2 The JAP reform bug — a cheap win hiding in the error log

`JAP`'s government block (`10_countries.txt:21762-21774`) carries
`reforms = { shogunate }`. Vanilla's `shogunate`
(`in_game/common/government_reforms/country_specific.txt:2052`) has:

```
:2063   allow = {
:2064       NOT = { has_reform = government_reform:daimyo }
:2065       NOT = { has_reform = government_reform:japanese_imperial_family }
:2066       NOT = { has_reform = government_reform:japanese_clan }
:2067       is_leader_of_international_organization = international_organization:japanese_shogunate
:2068   }
```

Our build strips the `japanese_shogunate` IO instance —
`main_menu/setup/start/15_international_organizations.txt:365-366`,
`creation_date = 1192.1.1`. So `:2067` cannot be satisfied and the reform is
invalid at start. **That is the "Japanese imperial reform invalid" half of the
~25-line class in `docs/HANDOFF.md:69`**, whose French half was cured by the
France slice (item 20).

The 1066-correct replacement is named in the same `allow` block:
`japanese_imperial_family` (`country_specific.txt:1952`), whose `allow`
(`:1959-1967`) requires `ruler_or_heir_if_regent ?= { dynasty ?= dynasty:yamato_dynasty }`
— and `jap_go_reizei_tenno` **is** `yamato_dynasty`. Seating Go-Reizei and
swapping the reform fixes the history and the log in one change.

(`japanese_clan` is both a setup template — `main_menu/setup/templates/japanese_clan.txt`,
which JAP includes at `10_countries.txt:21761` — and a government reform,
`country_specific.txt:1998`. The template sets no `reforms` block, so there is
no clash. Verified: `grep -c reforms japanese_clan.txt` = 0.)

### 4.3 Seats needing an authored character — cheap, one each

Borders already acceptable; the person must be written. All ruler identities
below are **[U]** — the agent's history, no vanilla anchor.

| tag | 1066 ruler | seat | dynasty key | name key status |
|---|---|---|---|---|
| **KOR** | Munjong of Goryeo (Wang Hwi, r. 1046-1083) | `kaesong` — correct | **`wang_dynasty` ships** (`dynasty_names_l_english.yml:1588`) | needs a check in `in_game/common/languages/00_korea_japan.txt`; the `regnal_name` literal route (Chungsuk/Mustansir precedent, `docs/HANDOFF.md:612`) covers a temple name |
| **DAI** | Lý Thánh Tông (r. 1054-1072) | `thang_long` — correct | Lý — **not in `dynasty_names`**; `tran_dynasty` (`:1299`) is the wrong house. New dynasty needed | literal-name route |
| **CHA** | Rudravarman III (r. 1061-1074) | `vijaya` — correct | none | literal-name route |
| **KHM** | Udayadityavarman II (r. 1050-1066) — note he dies **in** 1066 [D]; Harshavarman III is the safer seat | `angkor` — correct | none | literal-name route |
| **CDL** | Duan Silian (r. 1041-1075) [D] | `taihe_dali` — correct | Duan — none | literal |
| **CHI** | Yingzong of Song (Zhao Shu, r. 1063-1067); Shenzong from Jan 1067 | `dadu` → **`kaifeng`** | Zhao — none | `regnal_name` literal, papal route |
| **TIB** | genuinely fragmented [D] | — | — | leave `ruler = random`, the honest answer (the Moray/Galloway precedent, `docs/HANDOFF.md:786`) |

**Verification owed before any of these is written** (CLAUDE.md, and the
`name_harald` trap at `docs/HANDOFF.md:120`): every `name_*` key must be
confirmed present in `in_game/common/languages/` — `00_china.txt`,
`00_korea_japan.txt`, `00_indochina.txt`, `00_deccan.txt`, `00_bengal.txt`.
A missing key gives a nameless character and no error. The invented-name-key
mechanism is proven here (seven so far, `docs/HANDOFF.md:409`), so a missing
key is a cost, not a blocker.

**Batch shape:** 6 seats + the JAP reform swap. 2 use vanilla characters
verbatim (JAP, HSL), 5 need authoring, ~3 need new dynasties. That is smaller
than the Celtic batch (3 seats + 1 authored, `docs/HANDOFF.md:319`) and about
half the Iberia batch.

---

## 5. Diplomacy and IO residue in the east

### 5.1 What our IO strip removed east of Persia

Vanilla ships 53 IO instances; the mod's file carries **35**
(`main_menu/setup/start/15_international_organizations.txt`: 20 `sect`,
7 `autocephalous_patriarchate`, 4 `hindu_branch`, 1 each `shinto`, `hre`,
`high_kingship`, `catholic_church`). The eastern casualties:

| IO | vanilla creation | correct to strip at 1066? | consequence |
|---|---|---|---|
| `middle_kingdom` | 1271.12.18 | **NO** — the tianxia system long predates the Yuan [U] | §1: 185 log lines, 54 files of dead content |
| `japanese_shogunate` | 1192.1.1 | **yes** — no shogunate in 1066 | but leaves JAP's `shogunate` reform invalid (§4.2) — fix the reform, not the IO |
| `jurchen_confederation` ×3 | post-1066 | **yes** [U] | none observed |
| `tribal_confederation` ×2 | post-1066 | yes [U] | none observed |
| `tatar_yoke`, `ilkhanate` | 1240s / 1256 [U] | yes | already in the accepted class |

### 5.2 The subject web east of Persia — full inventory

`main_menu/setup/start/12_diplomacy.txt` (674 lines) carries 482 dependencies:

| subject type | count | eastern relevance |
|---|---|---|
| `vassal` | 239 | CHI alone is overlord of ~74 (`:342-361`, `:508-...`), incl. **KOR** (`:346`), **TIB** (`:358`), **MMA** (`:348`), LNG (`:347`) |
| `tusi` | **126** | 18 overlords: LNG 62, CHI 19, SZH 12, BZU 7, QYN 4, QJG 4, SDG 3, GGX/LIN/TNZ/GNN 2 each, BZH/YNJ/MHU/YGS/PDN/PAN/SMG 1 each |
| `tributary` | 88 | includes **CHI→CHA** `:586` and **CHI→DAI** `:587` — the two named in the decoder |
| `samanta` | 22 | the Indian vassal type (`in_game/common/subject_types/samanta.txt:3`, `visible = { has_advance = samanta_advance }`) — will need re-pointing with any India rebuild |
| `fiefdom` / `dominion` / `hanseatic_member` | 4 / 2 / 1 | western |

**What dies with the anchor fix:** all 128 `government.cpp:3702` lines
(126 tusi + CHA/DAI), the 56 `jomini_script_system.cpp:252` IO-link lines, and
CHI's `country.cpp:9635` culture flood — **185 lines, on Route B**. On Route A,
only 3 lines plus the culture flood.

**What needs its own work regardless of §1:**

1. **`CHI → KOR` vassalage** (`:346`). Goryeo was never a Chinese vassal; it
   was a Liao tributary in 1066 [U]. Strip or convert to `tributary` — the
   latter now passes the gate free once CHI carries
   `allow_tributary_subject` (either route).
2. **`CHI → TIB` vassalage** (`:358`). Yuan overlordship of Tibet is 1240s+
   [U]. Strip.
3. **`LNG → CDL`** (`:382`). Dali was sovereign in 1066 [U]. Strip; LNG should
   be landless.
4. **The `celestial_governor = { KOR }`** in the restored instance — remove
   (§1.4 item 4).
5. **The 4 `hindu_branch` IO member lists** (`:1139`, `:1157`, `:1175`,
   `:1190`, `creation_date = 1.1.1` so all four survive the strip). Their
   members are 1337 India tags. Any India retirement makes them landless
   members and the "IO members hold land" harness check (753 items) will fail —
   **this check is the tripwire that forces the member surgery**, and the
   generic landless-member strip at `build_setup.py:4195-4218` already handles
   it if the tags enter `LANDLESS_AFTER`.
6. **The `shinto` IO** (1 instance, survives). Not audited here; flagged as
   worth a look during any Japan slice.
7. **`QUN` on the shatter-watch** (`initialize_from_bookmark.cpp:2477`,
   decoder). 26 → 6 locations after the Seljuk sweep. Its 3 remaining
   hindustan_region locations sit under a Mongol-era tag that cannot exist at
   1066 [U]; retire it with the India pass.

---

## 6. OPEN DECISIONS

Each carries the agent's recommendation and a cost estimate. Nothing below has
been written.

---

**D1 — The anchor route. IO restore, or reform?**

- **Recommend: Route B, restore the Middle Kingdom instance re-dated to 960.**
  It kills 185 log lines against Route A's ~3, and it un-bricks 54 vanilla
  files of Chinese content that are currently inert with no error.
- **Cost:** 0 locations, 1 tag, 0 characters. One new `build_ios` surgery
  (~40 lines, modelled on the High Kingship block at `:4093-4127`), five
  assertions, one harness check.
- **Risk:** the 107 non-CHI tusi may still fail on the culture branch
  (`country_triggers.txt:1295-1301`) — not statically determinable, must be
  measured. Deterministic fallback: convert residual tusi → vassal in
  `build_diplomacy`.
- **Alternative if rejected:** `song_mandate_reform` as spec'd in §1.5, and
  the 126 tusi lines stay in the accepted budget.

---

**D2 — Does CHI become the Sòng in this pass, or stay the Yuán?**

- **Recommend: yes, reskin now.** `flag = "CSO"` and `country_name = "CSO"`
  are two tokens; `CSO: "Sòng"` already exists
  (`country_names_l_english.yml:3004`), `map_CSO` already exists, and the
  identity block is already registered (`east_asia.txt:1169`). Drop
  `legacy_of_kublai_khan` (`:26320`) and `status_of_the_han_law`
  (`:26316`) with it — a Song emperor does not limit Han power. Move the
  capital `dadu` → `kaifeng`.
- **Cost:** 0 locations, 1 tag, 0 new characters. Four token edits.
- **Against:** it makes a *Song-named* state that still holds Mongolia and
  Manchuria, which may read worse than an honestly-labelled Yuán until D3
  lands. If the user prefers coherence over correctness in the interim, defer
  to the same pass as D3.

---

**D3 — CHI's steppe: does China give up Mongolia and Manchuria now?**

- **Recommend: yes, in the cheap tier.** 198 locations (Mongolia 89,
  Manchuria 109) that no Chinese dynasty held in 1066 [U]. The recipients
  already exist as tags; the eight Chinggisid hordes that hold the rest
  (170 locations) go landless-with-claims in the same rule — the
  BYZ_LANDLESS shape, already proven twice.
- **Cost:** 368 locations moved or released, ~18 tags, 0 new characters.
- **Note:** this is *removal*, not authoring. It makes the map honest without
  requiring the Liao to exist yet.

---

**D4 — The Liao. Now, later, or never?**

- **Recommend: defer, but decide the tag now.** The Liao is the second power
  of East Asia in 1066 and its absence is the biggest single hole. But it is a
  new tag, a new dynasty (Yelü — no vanilla key), a culture/religion decision
  (Khitan), and ~450-500 locations resolved from `definitions.txt`. That is a
  Byzantium-sized slice on its own.
- **Cost if taken:** ~450-500 locations, 1 new tag + ~15 donors, 3-5 new
  characters, 1 new dynasty.
- **Cheaper half-measure:** reskin **SYG** (Shenyang, 27 locations, capital
  `shenyang` — the Liao Eastern Capital [U]) as the Liao and give it D3's
  Manchurian and Mongolian releases. That converts D3's *removal* into a
  *transfer* at almost no extra cost and puts a recognisable Liao on the map
  without inventing a tag.

---

**D5 — India's floor: how much of Delhi comes off?**

Three options, in ascending cost:

- **D5a — Punjab only.** DLH's 97 `punjab_area` locations → GHZ. Delhi shrinks
  to 272 and stays on the map as an anachronism. **Cost: 97 locations, 2 tags,
  0 characters.**
- **D5b — Punjab + behead. (RECOMMENDED)** D5a, then DLH goes
  landless-with-claims and its remaining 272 locations are released. Delhi
  becomes the *future*, exactly as MAM does in Egypt (`docs/HANDOFF.md:612`)
  and GRA in Iberia. **Cost: 369 locations, ~15 tags, 0 characters.** The
  recipients can initially be the existing small Indian tags whose claim lists
  already cover the ground — the Sardinia method
  (`our_cores_conquered_by_others` IS the border, `docs/HANDOFF.md:358`).
- **D5c — Full Tier 1.** D5b plus five invented tags (Chola, Western Chalukya,
  Pala, Paramara, Solanki) with dynasties and rulers. **Cost: ~500-600
  locations, 5 new tags + ~25 donors, 8-12 characters, 5 new dynasties.**
  Larger than the Taifa Factory.

The agent's read: **D5b is the right floor.** It removes the impossible object
at zero authoring cost, and leaves a fragmented India of small real
principalities — which is not *right*, but is not *wrong* in the way a
Tughlaq Sultanate at 1066 is wrong.

---

**D6 — The nine other impossible Indian tags (VIJ MAB SMA RDY RCH JFN DBD SMV MSN, 191 locations).**

- **Recommend: retire with D5b in the same pass.** They are the same class of
  error as DLH and the same mechanism retires them. Leaving them while
  removing Delhi would be inconsistent.
- **Cost:** 191 locations, 9 tags, 0 characters.
- **Against:** it empties large parts of the Deccan with nothing historical to
  put back until D5c, which may look worse than wrong tags. If that matters
  more than accuracy, hold them and take D5b alone.

---

**D7 — The cheap ruler-seat batch (§4). Which seats?**

- **Recommend: take all seven** — JAP (Go-Reizei, vanilla character, + the
  `shogunate` → `japanese_imperial_family` reform swap that also kills a
  standing error class), HSL (Vinayaditya I, vanilla character), KOR, DAI,
  CHA, CDL, CHI. Leave TIB random ([D] — honest).
- **Cost:** 0 locations, 7 tags, 5 authored characters, ~3 new dynasties,
  ~6 name-key verifications in `in_game/common/languages/`.
- **Sequencing note:** the JAP item is worth taking *even alone*. It is one
  token plus one vanilla character and it retires the last surviving half of
  the ~25-line reform-invalid class.

---

**D8 — Pagan under Anawrahta: invent PAG, or reskin PIN?**

- **Recommend: reskin PIN.** Pinya (26 locations, capital `pinya`, 1313 [U])
  sits on the right ground; the identity material for Pagan already ships
  (`pagan_dynasty` `dynasty_names_l_english.yml:1003`, the `pagan` location,
  `pagan_province`). A loc override on the tag name plus a capital move to
  `pagan` is far cheaper than a registry addition, and the `is_historic`
  releasable future is preserved.
- **Cost (reskin):** ~30-60 locations if PEG/SAG/BPR fold in, 1-4 tags, 2-3
  characters. **Cost (invent):** add ~1 registry block and a colour.
- **Defer either way** — this is EXPENSIVE-DEFER tier and does not block the
  anchor.

---

**D9 — Scope of this whole theatre. What actually gets built?**

The agent's recommended package, in order, is:

| # | item | locations | tags | characters | tier |
|---|---|---|---|---|---|
| 1 | Middle Kingdom restore (D1, Route B) | 0 | 1 | 0 | MUST |
| 2 | JAP reform swap + Go-Reizei (D7 partial) | 0 | 1 | 0 | MUST |
| 3 | DLH: Punjab → GHZ, then behead (D5b) | 369 | ~15 | 0 | MUST |
| 4 | CHI reskin to Sòng (D2) | 0 | 1 | 0 | CHEAP |
| 5 | CHI drops the steppe; hordes retired (D3), optionally into a SYG-Liao (D4 half-measure) | 368 | ~18 | 0-2 | CHEAP |
| 6 | The remaining six ruler seats (D7) | 0 | 6 | 5 | CHEAP |
| 7 | Nine impossible Indian tags retired (D6) | 191 | 9 | 0 | CHEAP |
| | **TOTAL** | **928** | **~51** | **5-7** | |

That is a slice comparable to the Byzantium pass (495 locations granted, 45
tags landless, `docs/HANDOFF.md:444`) but with a fraction of its character
authoring — because the eastern work is overwhelmingly *removal* of things
that cannot exist, not *creation* of things that must.

Everything in EXPENSIVE-DEFER (the Liao proper, Western Xia, Pagan, SEA's
post-1066 states, Tibet's fragmentation, and India Tiers 1-3) stays banked:
**~1,600-1,800 locations, ~10 invented tags, ~25-35 new characters** — a
second full theatre, roughly the size of everything shipped between items 13
and 21.

---

## 7. Verification statements

Per CLAUDE.md's say-what-you-verified rule:

- Verified — `cultures_capacity`, `docs/EU5-Vanilla-Script-Docs/modifiers.log:494`,
  "Tag: cultures_capacity, Categories: Country".
- Verified — `allow_tributary_subject`, `modifiers.log:1946`,
  "Tag: allow_tributary_subject, Categories: Country".
- Verified — `diplomatic_capacity_modifier` `modifiers.log:855`,
  `government_size` `:797`, `monthly_prestige` `:730`,
  `government_reform_slots` `:793`,
  `block_from_change_to_empire_rank` `:1382` — all Country scope.
- Verified — the tusi IO gate,
  `in_game/common/scripted_triggers/country_triggers.txt:1287`,
  "exists = international_organization:middle_kingdom", reached from
  `in_game/common/subject_types/tusi.txt:7` `can_country_have_tusi = yes`.
- Verified — the tributary gate,
  `in_game/common/subject_types/tributary.txt:20-25`, whose fourth branch is
  `modifier:allow_tributary_subject = yes` — matching the decoder entry.
- Verified — the IO's full leader payload,
  `in_game/common/international_organizations/middle_kingdom.txt:69-75`.
- Verified — the setup instance and its `creation_date = 1271.12.18`,
  `main_menu/setup/start/15_international_organizations.txt:210-271`.
- Verified — `CSO` exists as an identity block,
  `in_game/setup/countries/east_asia.txt:1169`, and localises as "Sòng",
  `main_menu/localization/english/country_names_l_english.yml:3004-3005`.
- Verified — the `shogunate` reform's IO requirement,
  `in_game/common/government_reforms/country_specific.txt:2067`, and its
  1066-legal alternative `japanese_imperial_family` at `:1952-1976`.
- Verified — `GHZ` is a mod-created tag,
  `in_game/setup/countries/zz_1066_new_countries.txt:200`, and holds no
  location outside `persia_region`.
- Verified — `lahore`, `multan`, `peshawar` are all in
  `hindustan_region / punjab_area` (`in_game/map_data/definitions.txt:3714`)
  and all owned by DLH in both vanilla and the mod.
- Verified — `jap_go_reizei_tenno` (b. 1025, `yamato_dynasty`,
  `name_chikahito`) and `hsl_vinayaditya_i_hoysala` (b. 1020,
  `hoysala_dynasty`, `name_vinayaditya`) exist in the mod's
  `main_menu/setup/start/05_characters.txt` with **no `death_date`** — i.e.
  they satisfy both engine laws (`docs/HANDOFF.md:9-22`) and can be seated
  as-is.
- **Not verified, and stated as such:** every 1066 ruler identity, accession
  date and polity extent in §2.3, §3.3 and §4.3 that carries `[U]` or `[D]`.
  Those rest on the agent's own history and need a source before they are
  written into setup data.
