> **STATUS (2026-08-03): REVIEWED AND DECIDED.** Main-session review against
> HEAD `189c165` reproduced **180 mechanical checks with `build_setup.py`'s
> own imported parsers — 177 exact**; the three diffs all resolved (two were
> this package's bookkeeping, one was the reviewer's own scanner reading
> `00_readme.info` — KNOWLEDGE has the trap). Errata are corrected in place
> below, each marked **✎REVIEW**; the one substantive find is the
> "Expected constant moves" table's `:205`/`:237` rows (wrong-direction
> forecasts, corrected there). **THE TEN DECISIONS ARE TAKEN (user onay
> 2026-08-03):** (1) route (a), gated on the probe; (2) first slice Baltic;
> (3) al-Andalus RE-LABELS first — conversion is re-decided as its own
> named-constant call after the mechanism is proven in game; (4) invent
> `mozarabic`, WITHOUT Basileia's −0.25 conversion modifier; (5)
> `slavic_paganism` takes all 87 locations incl. Brandenburg (knowing
> extension past the banked 894.7u — recorded here); (6) Mongol strip
> MINIMAL: Persia+Khorasan's 330 only (Anatolia's 24 die with its own
> slice; the ~670-location steppe/Siberia/China remainder parks with
> decision 8); (7) Egypt miaphysite → 0.40 as a named constant
> [U 0.30-0.60]; (8) CUM parked — one combined "Steppe demography" design
> owns it plus decision 6's remainder; (9) identity-only tests while
> re-label holds; any size-changing slice's tour must say `-leavepops`;
> (10) COMMITS per theater, LAUNCHES in three batches: Baltic+Wales+
> Ireland+micros+Ghana/Kanem → al-Andalus+Sicily+Egypt → Mongol-minimal+
> Anatolia LAST. Sequencing: the grand accumulated test runs FIRST on a
> probe-free build; the probe gets its own two-minute relaunch in the same
> sitting; the probe file is deleted in the commit that records its
> outcome. Nothing here is a test result; historical judgments keep their
> `[U]`/`[D]` flags. (Original draft: 2026-08-02, against `5000dbd`.)**
>
> **BATCH 1 LANDED (2026-08-03, same day — HANDOFF item 42 is the
> authority where this file and the implementation differ).** The probe
> measured APPEND + map-reads-pops in game; `build_pops` is live as the
> sixth target (208 touched blocks, byte-identical remainder, 13
> exact-count rules, D1-D10 all proven by breaking, the harness's
> independent set check at 28,570). Batch 1's reasoned deviations from
> this package's flat area rules are culture-scoped movers — recorded in
> item 42 and in build_setup.py's section comment. `define_pop` is now
> 50,177 (−75 folds, −3 TKA clergy). Remaining: Batch 2 (mozarabic +
> al-Andalus + Sicily + Egypt + HPJ), Batch 3 (Mongol-minimal +
> Anatolia LAST).
>
> **BATCH 1 CONFIRMED IN GAME and BATCH 2 LANDED (2026-08-03, same
> day — items 42/43).** Two [U]s closed as measurements: emptying a
> culture is ERROR-FREE and `suppress_no_pops_error` is
> parser-REJECTED (the flag insurance is retired; §0.7's caution
> resolved). `mozarabic` exists; decision 3's re-label stage +
> decision 7's 0.40 + the Sicily valli [D] are in the file;
> `define_pop` is now **50,340** (+193 created, −105 folds, −3).
> Left: Batch 3 (Mongol-minimal Persia+Khorasan, then Anatolia LAST)
> and decision 3's own conversion call.
>
> **BATCH 3 LANDED 2026-08-03 — THE §B INVENTORY IS COMPLETE (HANDOFF
> item 44).** `slavic_paganism` invented (the first mod religion);
> the Wendish shore pagan with the Altmark drawing itself (8
> German-kept locations); Persia/Khorasan pre-Chinggisid (mongolia
> asserted untouched); Anatolia pre-Manzikert (37 all-turkic
> locations re-seeded by area). `define_pop` **49,984** (1,142
> locations touched phase-wide, 461 folds, 193 created). Open BY
> DESIGN: decision 3's full conversion; banked residue: 15
> outside-scope turkic straggler locations, PLM/AGR registry culture.
> One accumulated test covers the phase; then the SITUATIONS backlog
> (Manzikert first — its Turkification-over-time is now route (d)'s
> canonical job, §C.3).

# THE POP PHASE — the mechanism first, then a correction inventory that survived an audit (DRAFT)

The map phase closed at `5000dbd`: every region of the world is 1066 by
borders, rulers, registries and diplomacy. What is left is the layer the
strategic order deliberately deferred — **the people standing on that
ground**.

This package answers the mechanism question before it costs anything, and
then hands over a correction inventory that has been **re-measured against
`06_pops.txt` rather than `location_templates.txt`**. That re-measurement is
the package's headline: five inherited corrections turn out to be artefacts
of reading the wrong layer, and one of them — Perm/Vyatka's "eleven registry
entries name religions that sit on ZERO locations" — retires completely.

Method note, stated up front because the last five reviews turned on it:
every count below was produced by importing `tools/build_setup.py`'s own
parsers (`_parse_defs` `:748`, `_ownable_set` `:772`, `find_block_end`
`:5659`, `COUNTRY_RE` `:5712`, the full ten-key `OWN_KEYS` `:5854`,
`_TAIFAS` `:540`) rather than reimplementing them, and proved against the
known positives before being trusted:

| known positive | source | this package's reader |
|---|---|---|
| `06_pops.txt` 28,570 location blocks | `POP-PHASE.md:18` | **28,570** ✔ |
| `06_pops.txt` 50,255 `define_pop` | `POP-PHASE.md:18` | **50,255** ✔ |
| ownable locations 20,922 | `build_setup._ownable_set()` | **20,922, set-identical** ✔ |
| VTN holds 32 (vanilla) | `KNOWLEDGE.md:2074` | **32** ✔ |
| TIB holds 59 (vanilla) | Tibet package | **59** ✔ |
| MOD country blocks 2,411 | `HANDOFF.md:2045` | **2,411** (strict *and* loose regex) ✔ |
| vanilla registry blocks 2,340 | `KNOWLEDGE.md:2158` | **2,340** (loose form) ✔ |
| 11 UPPERCASE location keys | `POP-PHASE.md:154-159` | **11, the same 11** ✔ |
| 2,142 locations with zero pops of their template religion | `POP-PHASE.md:53` | **2,142** ✔ |
| 222 of 244 al-Andalus locations catholic in the template | `HANDOFF.md:1044` | **222** ✔ |
| vanilla's own max same-type pops per location = 6, never 7 | `POP-PHASE.md:34` | **max 6; 12 locations at 6, none ≥ 7** ✔ |
| Bronze Era's broken generator: 2,633 dup / 502 phantom / 3,131 dropped | `POP-PHASE.md:139-140` | **2,633 / 502 / 3,131** ✔ |
| vanilla has exactly 3 zero-pop cultures | `POP-PHASE.md:110` | **3** ✔ |
| `griko` 79 pops | `POP-PHASE.md:93` | **79 pops** — but the key is `griko_culture` ✔/✎ |

One reader bug was found and fixed inside this package's own work, and it is
recorded because it is the fifth incident of the same class: the first
`location_templates.txt` parser used a **line-anchored** field regex and
reported **0 ownable locations of 28,573 blocks**, because that file is
*one line per block*. The anchor class (BOM-behind-`^`, one-line blocks,
trailing comments, tab-anchored pops, single-space registry regex) now has a
sixth member: **`in_game/map_data/location_templates.txt` is a one-line-block
file and any `^[ \t]*key` scan of it returns a confident zero.**

---

## 0. Ground truth — and the audit that reshapes the phase

### 0.1 THE HEADLINE: five inherited corrections were measured on the SEED layer

`POP-PHASE.md:47-48` already states the layer model — **`06_pops.txt` is the
STATE; `location_templates.txt` is the load-time SEED** — and it is correct.
What no package applied is its consequence: *a correction measured in
`location_templates.txt` is a hypothesis about pops, not a measurement of
them.* Vanilla's two layers disagree in **2,142 ownable locations for
religion and 1,384 for culture** (measured this session; the religion figure
reproduces `POP-PHASE.md:53` exactly), so the disagreement is systemic, not
occasional.

Re-measuring every inherited §H item against `06_pops.txt` produces this:

| inherited claim | source | measured on the SEED | measured on the STATE (`06_pops.txt`) | verdict |
|---|---|---|---|---|
| "eleven registry entries name religions that sit on **ZERO locations game-wide**" — `komi_paganism`, `samoyedic_paganism`, `obian_paganism` | `PERM-VYATKA-PACKAGE.md` §0.5 / §H | 0 / 0 / 0 template locations — **correct** | **`komi_paganism` 71 locations, `samoyedic_paganism` 63, `obian_paganism` 84** | **RETIRED — nothing to fix** |
| "CLM's `culture_definition = teco_culture` on **ZERO of 20,922 locations**" | `AMERICAS-PACKAGE.md` §H | 0 template locations — **correct** | **`teco_culture` on 6 locations — and all 6 are CLM's own** | **RETIRED — the TEMPLATE is the wrong layer, the registry is right** |
| "`toltec_culture` on **ZERO locations**" | `AMERICAS-PACKAGE.md` §H | 0 template locations — **correct** | **1 location** | shrinks to a curiosity |
| "Kedah's three locations are `sunni` and should be `mahayana` or `hindu`" | `SEA-PACKAGE.md` §H | `bujang kedah perlis` all `sunni` — **correct** | **`bujang` and `kedah` are already `mahayana` in pops; only `perlis` carries one sunni peasant pop (1.811u)** | shrinks from 3 locations to **1 define_pop line** |
| "`prussia_area` is 41 catholic / 3 romuva and should be ~28 romuva" | `BALTIC-PACKAGE.md` §H | 41/3 — **correct** | **28 of 44 locations already carry romuva pops; 99 catholic `define_pop` remain across 39** | shrinks by roughly a third |

And the corrections that **survive** the audit survive it cleanly:

| inherited claim | STATE measurement | verdict |
|---|---|---|
| al-Andalus is 1337-Christian | 244 locations, 928 pops, 3,902.4 units — **catholic 77.8 %** on 224 locations, sunni 20.5 % on 175, judaism 1.6 % on 142 | **CONFIRMED**, and identical to `POP-PHASE.md:79` |
| `baltic_area` should be pagan | 56 locations, **153 catholic `define_pop` (283.2u)**; romuva appears on **exactly 4** | **CONFIRMED and larger than the template said** |
| HPJ sits on Khon Muang ground | 12 locations; 9 are `khon_muang_culture`/`theravada` over a `lawa_culture` substrate, 3 are `karen_culture` | **CONFIRMED**, 14 `define_pop` |
| TKA's `xining_province` is Song-painted | 6 locations; `liang_culture`/`sanjiao` + `monguor_culture`/`mahayana` + `mongolian_culture` clergy, `amdowa` a minority on 5 of 6 | **CONFIRMED**, 12 `define_pop` |
| the Mari have no pop-country identity | **32 `mari_culture` pop locations; 0 covered by any of the 448 `type = pop` countries** (17 are owned, 15 unowned-and-uncovered) | **CONFIRMED** |
| the `wari_culture` → "Inca" render | `wari_culture` (`peruvian.txt:693`) declares `language = quechuan_language` (`:694`); `country_ranks.txt:1917` gates `rank_duchy_inca` on `culture.language = language:quechuan_language` (siblings at `:345` empire, `:1173` kingdom) | **CONFIRMED — and it is a RENDER question, not a pop question** (§C.2) |

**Means for the reviewer:** the phase is meaningfully *smaller* than the
banked lists imply, and the reason is a method error the packages could not
have caught without parsing `06_pops.txt`. Nothing was sloppy — the §H
entries all say which file they measured. They were just the wrong file.

### 0.2 The file, measured exactly

`VAN/main_menu/setup/start/06_pops.txt` — 107,398 lines, 5,084,334 bytes,
**no BOM** (first three bytes `6c 6f 63` = `loc`).

| property | measurement |
|---|---|
| location blocks | **28,570**, zero duplicate names |
| `define_pop` entries | **50,255** |
| ownable locations covered | **20,922 of 20,922** — every ownable location has a block |
| ownable locations with an EMPTY block | **119** — and **all 119 are unowned**; no owned location has zero pops |
| non-ownable blocks (seas, lakes, wastelands) | **7,648**, all empty |
| template blocks with no pop block | **3** — `lake_hovz_soltan`, `lake_namak`, `zagros_mountains8` (28,573 template blocks vs 28,570 pop blocks) |
| pop shape | exactly four fields, `type size culture religion`, one line — never optional, never extra |
| UPPERCASE-bearing location keys | **11** (`POP-PHASE.md:154-159`'s list, reproduced) |

Bronze Era proves the shape is not mandatory: its `06_pops.txt` writes the
same four fields **multi-line** and the game ships. The one-line form is
vanilla's formatting, not the parser's requirement.

### 0.3 The merge safe zone, re-measured against the whole world

`POP_MINORITY_SIMILAR_THRESHOLD = 4` and `POP_MINORITY_JUST_MERGE_THRESHOLD
= 8` (`VAN/loading_screen/common/defines/00_defines.txt:1633-1634`).
Distribution of *max pops of one type per location*, all 28,570 blocks:

| max same-type pops | locations |
|---|---|
| 1 | 14,325 |
| 2 | 4,920 |
| 3 | 1,244 |
| **4** | **249** |
| **5** | **53** |
| **6** | **12** |
| ≥ 7 | **0** |

So vanilla itself sits at or above the *similar-merge* threshold in **314
locations** and never reaches the *just-merge* threshold. `≤ 3 per type per
location` remains the safe design zone; **4-6 is attested vanilla practice,
not a bug**; ≥ 8 is untrodden ground. Eleven of the 244 al-Andalus locations
are already at 4 of one type, so an al-Andalus rule that *adds* a pop type
must count before it writes.

### 0.4 Elite pops are seeds, and the verification consequence

`POP-PHASE.md:24-30` established it and it stands: nobles/clergy/burghers
carry `has_cap` and the engine inflates them at load. The wiki states the
mechanism directly — *"Extra pops will be added to fill up the pop type caps
(if the location starts with 8 noble pops but the pop cap is 100, 92 will be
added)"*, and *"To test pure population numbers from pop definition, the
`-leavepops` commandline option … will disable any and all calculations that
might change the starting population numbers and fractions"*
(`docs/Setup modding - Europa Universalis 5 Wiki.pdf`, "Starting pop logic").

**Consequence for the grand test:** a pop slice cannot be verified by
counting people in the location panel on a normal launch. Either the test
reads *identity* (which cultures and religions are present, and which is
dominant) — which survives inflation — or the user launches with
`-leavepops`. **OPEN DECISION 9.**

### 0.5 What the three published conversions actually do

All three ship a whole-file `06_pops.txt` override. All three are BOM-free.

| mod | blocks | `define_pop` | duplicates | phantom (not a vanilla location) | dropped (vanilla location absent) |
|---|---|---|---|---|---|
| vanilla | 28,570 | 50,255 | 0 | — | — |
| **Anno 1644** | 28,581 | **150,705** | **0** | 14 | 3 |
| **Bronze Era** | 25,941 distinct / 28,574 occurrences | **50,052** ✎REVIEW | **417 names, 2,633 extra copies** | **502** | **3,131** |
| **Basileia** `06_pops.txt` | 22,399 | 46,072 | 0 | 0 | **6,174** |
| Basileia `06_pops_north_america.txt` | 4,263 | 4,818 | 0 | 0 | — |
| Basileia `06_pops_south_america.txt` | 1,911 | 1,719 | 0 | 0 | — |

✎REVIEW corrections to this table (2026-08-03, all re-measured): Bronze's
`define_pop` total is **50,052** (the draft's 46,119 matches no reading —
raw and comment-masked are both 50,052, and first-wins/last-wins distinct
counts are 50,048). Basileia's 46,072 is the RAW token count; 19 sit in
comments, **46,053 live**. Basileia's override also carries blocks for the
three template-locations vanilla's `06_pops.txt` lacks (`lake_hovz_soltan`,
`lake_namak`, `zagros_mountains8`) — "phantom 0" holds under this table's
not-a-vanilla-location definition. The 3,804/18,592 differ/identical split
reproduces as 3,803/18,593 under whitespace normalization.

Three things follow, and the third is the important one.

1. **Anno 1644 is the proof of scale**: a clean 28,581-block override with
   three times vanilla's population, shipped and playable.
2. **Bronze Era is the cautionary tale, and its numbers reproduce exactly**
   (2,633 / 502 / 3,131 — `POP-PHASE.md:139-140`). It shipped anyway. The
   block-name **set-equality** assert is the guard that catches all three
   failure modes at once.
3. **Basileia partitioned rather than layered.** Its override *drops* 6,174
   American blocks, and its two additive files restore **exactly** those
   6,174 — `4,263 + 1,911 = 6,174`, with **zero overlap** against the
   override and zero blocks that are not vanilla locations. The most
   experienced pop-editing conversion available deliberately arranged for no
   location to appear in two of its own pop files. That is behavioural
   evidence about the additive question in §A.2, and it is the reason this
   package does not treat "additive replaces" as a live hypothesis.

Also measured, as a cost anchor: of Basileia's 22,399 retained blocks,
**3,804 differ from vanilla and 18,592 are byte-identical**. A total
conversion of a whole continent's demography edited 17 % of the file.

### 0.6 The runtime toolset exists, in full

| tool | scope | `docs/EU5-Vanilla-Script-Docs/effects.log` | attested vanilla use |
|---|---|---|---|
| `add_pop` | **location** | `:331` | `scripted_effects/location_effects.txt:77` |
| `change_pop_culture` | **pop** (target culture) | `:953` | — |
| `change_pop_religion` | **pop** (target religion) | `:963` | `generic_actions/reformation.txt:75` |
| `change_pop_type` | pop | `:968` | — |
| `add_pop_size` | pop | `:339` | `location_effects.txt:93` |
| `split_pop` | pop | `:10459` | `country_interactions/demand_conversion_to_islam.txt:45` |
| `destroy_pop` | none (target pop) | `:1460` | `effect_localization/pop_effects.txt:74` |
| `every_pop` | **location, country** | `:2908` | `demand_conversion_to_islam.txt:39`, 20+ others |
| `every_location_in_region` / `_in_area` | region / area | `:2548` / `:2518` | many |
| `on_game_start` | **Expected Scope: none** | `on_actions.log:575` | `in_game/common/on_action/_hardcoded.txt:1` (vanilla builds the whole catholic IO membership here) |

So route (d) in §A.4 is *possible*. §A.4 explains why it is nevertheless the
wrong tool for this job, on a reason that is specific to this project.

### 0.7 The identifier layer — what may be emptied, and what may be invented

| measurement | value |
|---|---|
| culture keys declared top-level in `VAN/in_game/common/cultures/` | **2,083** (+4 used by pops and declared nested: `cunco_culture`, `manekenk_culture`, `yaros_culture` in `argentinian.txt:210/:2/:342`, `she_culture` in `east_asia.txt:1358`) = **2,087 distinct**, matching `POP-PHASE.md:98` |
| culture keys **without** the `_culture` suffix | **332** — the spelling trap, confirmed |
| religion keys | **293** |
| cultures on **zero** pop locations | **3** — `peruzzi_bank_culture` (`italian.txt:247`), `acciaioli_bank_culture` (`:262`), `roman_culture` (`:307`) |
| religions on **zero** pop locations | **8** — `anglican calvinist hussite lollardy lutheran strigolniki sikhism hellenism_religion` |
| vanilla cultures carrying `suppress_no_pops_error = yes` | **0** — the token exists only in its own documentation, `VAN/in_game/common/cultures/00_cultures.info:28` |

Two corrections to the banked note:

- **`POP-PHASE.md:107-112` says emptying a culture world-wide "errors unless
  the culture carries `suppress_no_pops_error = yes`". Vanilla ships three
  zero-pop cultures and NOT ONE of them carries the flag.** So either the
  error is emitted for vanilla's own three (a known-vanilla signature to be
  confirmed at the next launch, not a mod defect), or the claim needs
  narrowing. Either way, adding the flag via `REPLACE_OR_CREATE:` is cheap
  insurance rather than a proven necessity. **Watch for it at the test.**
- **Religions are not in the same boat**: vanilla ships **eight** zero-pop
  religions with no flag and no equivalent token, because a Reformation
  religion is *supposed* to have no pops at 1337. Emptying a religion is not
  an error class.

The invention precedent is `REPLACE_OR_CREATE:` (a real database prefix,
259 occurrences across Basileia; `KNOWLEDGE.md`'s prefix list gains a fourth
member). **Correction to `POP-PHASE.md:79`: Basileia's invented Iberian
culture is `mozarabic`, not `mozarab`** —
`Basileia/in_game/common/cultures/br_iberia.txt:24`, and its file opens with
`REPLACE_OR_CREATE:andalusi = {` at `:1`, which re-points vanilla's
`andalusi` at `maghrebi_dialect`. Basileia's `mozarabic` also carries a
`location_modifier = { local_pop_conversion_speed_modifier = -0.25 }` block
that `POP-PHASE.md` does not mention. The suffix trap caught the banked note
itself; it will catch us.

---

## A. THE MECHANISM — four routes, costed, one recommendation

### A.1 Route (a): a whole-file `06_pops.txt` override, generated

**What it is.** A sixth entry in `TARGETS` (`build_setup.py:8338`, currently
five), `("06_pops.txt", build_pops)`, reading vanilla's file and emitting a
mod copy with the corrections applied — exactly the shape the other five
already use.

| dimension | honest cost |
|---|---|
| capability | **complete** — add, edit, delete, reorder |
| file size | ~5.0 MB, the largest file the mod would ship (today's largest is `05_characters.txt` at 2.5 MB) |
| generator cost | small: the parse is a two-level brace walk over an utterly regular file. The rule application is where the work is |
| patch fragility | **LOW, and this is counter-intuitive.** The file is *generated from vanilla's file at build time*, so a patch that edits pops is absorbed by re-running the build — the same property that makes the existing 1.18 MB `10_countries.txt` override sustainable. What a patch CAN break is an exact-count assert, which is the intended behaviour: it fails loudly |
| `replace_paths` | **not needed and must not be used** — Bronze and Anno both prove the single-file-override route; `replace_paths` would force shipping all 25 setup files (Basileia's cost) |
| the known failure mode | Bronze Era's 2,633/502/3,131. Guarded by set-equality on block names (§D) |
| review cost | a 5 MB generated file cannot be read. The guards ARE the review |

**The `07_cities` / `08_institutions` question, answered:** overriding
`06_pops.txt` does **not** touch them. They are separate *files* in the same
`locations = { }` manager, and override is by filename
(`.claude/skills/write-eu5-setup/SKILL.md`, RULE 2). Measured: `07_cities_
and_buildings.txt` has **1,023** location blocks (✎REVIEW — the draft said
1,129; the file's SECOND manager, `building_manager`, holds 2,646 blocks of
its own, and every one of the 1,023 location blocks is also a `06_pops.txt`
block) carrying only `rank` / `town_setup` and **zero `define_pop`**; `08_institutions.txt` has 13,090
carrying only institution keys; `06_pops.txt` has zero `rank` or
`town_setup`. The three files are disjoint in *fields* and overlapping in
*keys* — which is exactly the proof §A.2 needs.

### A.2 Route (b): an additive setup file — and why the merge question is already answered

**The question:** does a later-loading setup file's location block *replace*
a location's pop block, or only *add* pops to it?

It is answered **inside vanilla, without a probe**:

> **1,023 locations appear in both `06_pops.txt` and
> `07_cities_and_buildings.txt`, and 13,090 appear in both `06_pops.txt` and
> `08_institutions.txt`.** `aachen` is `{ define_pop … ×N }` in the first and
> `{ rank = town town_setup = german_town }` in the second. Aachen is a town
> *and* has pops in game. If a later file's location block replaced an
> earlier one, vanilla's own `07_cities_and_buildings.txt` would have
> deleted the pops of 1,023 of its most important locations at load.

So **location blocks merge at the key level across setup files.** That
corroborates, from a second dataset, the in-game measurement already banked
for country blocks (`write-eu5-setup` RULE 3: England redefined additively
kept all 145 locations), and vanilla's own 175 country blocks that declare
`government = { … }` twice inside one block.

What that proof does **not** settle is the narrower case where the *same
repeated key* (`define_pop`) appears for the same location in two files —
append or replace-the-list. Three independent things point at **append**:

1. the wiki's own wording: *"`define_pop` can be used to **add** a pop to a
   location"* (`Setup modding` PDF, "Locations");
2. the merge defines exist precisely to arbitrate many pops of one type in
   one location (`00_defines.txt:1633-1634`), which is a list-append world;
3. Basileia — the only conversion that mass-edits pops — **arranged its
   files so the case never arises** (§0.5), which is what an author does
   when append is the behaviour and deletion is what they need.

**Conclusion: an additive pop file can ADD pops and has no attested way to
remove or edit one.** That is fatal for al-Andalus, Anatolia, Ireland and
Wales, which are removals. It is perfectly adequate for pure seeding.

**Cost if used for what it can do:** near zero — a new filename sorted above
`27_` (e.g. `50_1066_pops.txt`), no BOM, no generator, no patch fragility,
no set-equality guard needed.

### A.3 Route (c): `location_templates.txt` — what it actually drives

**Recommendation: stay out.** Three measurements:

1. **The GUI cannot read it.** `docs/EU5-Vanilla-Script-Docs/data_types/`
   contains **zero** `Location.GetCulture` and **zero**
   `Location.GetReligion`. What exists is `Location.GetDominantCulture`
   (`data_types_uncategorized.txt:82405`, `:83209`),
   `Location.GetDominantReligion` (`:82423`, `:83227`),
   `GetDominantLanguage` and `GetDominantDialect` — all pop-derived. There
   is no promote path from a location to its template religion at all.
2. **Vanilla tolerates the disagreement at scale**: 2,142 ownable locations
   have no pop of their template religion and 1,384 none of their template
   culture, shipped, in the base game.
3. **Basileia rewrote Anatolian demography with zero `map_data` files**
   (`POP-PHASE.md:54-56`).

The tree is also **BOM-mixed** (`definitions.txt` has one,
`location_templates.txt` does not — `POP-PHASE.md:160-163`), so an override
there would need a documented harness exception in the same commit. Nothing
in the inventory in §B requires it. **DEFER, and let the probe in §A.6
confirm it can stay deferred forever.**

### A.4 Route (d): runtime conversion at `on_game_start`

Every tool exists (§0.6) and the shape is attested vanilla script:

```
# NOT PROPOSED — shown to cost the route honestly
on_game_start = { effect = {
	every_location_in_area = { … every_pop = {
		limit = { religion = religion:catholic }
		change_pop_religion = religion:romuva
	} }
} }
```

It has one real advantage — no 5 MB file, no patch fragility at all — and
three disqualifying costs, of which the third is specific to this project:

1. **It converts POST-inflation pops.** The engine fills elite pops to their
   caps at load (§0.4); a runtime pass therefore acts on a population the
   file never described, and the estate-culture derivation (weights at
   `00_defines.txt:1679-1685`, 60-month cooldown) has already run once on the
   *wrong* cultures.
2. **It is visible as a change**, not as a start state — the player watches
   Andalusia convert on day 1, and `-leavepops` cannot verify it.
3. **It cannot retire the errors the phase exists to retire.** The whole
   named debt — `initialize_from_bookmark.cpp:237/:301` + `country.cpp:9778`
   (`EU5-ERROR-DECODER.md:539-548`, *"ALL of it is the pop-conversion phase's
   work"*) and `initialize_from_bookmark.cpp:205`
   (`EU5-ERROR-DECODER.md:530-537`) — is emitted **at bookmark
   initialisation**, which is before `on_game_start` by the function's own
   name and by `KNOWLEDGE.md`'s measured law that the registry's
   culture/religion fields "are read at bookmark init only". A route that
   runs after init cannot silence an init-time diagnostic.

**Reserve route (d) for what it is genuinely good at: conversion over
TIME**, inside a situation (§C.3).

### A.5 THE RECOMMENDATION

> **Route (a) — a whole-file `06_pops.txt` override, generated by
> `build_setup.py` as a sixth `TARGETS` entry — with route (b) held in
> reserve for any future purely-additive slice, route (c) permanently
> deferred, and route (d) reserved for situations.**

Reasoning, in order of weight:

1. **Only (a) can delete**, and the inventory's two largest items
   (al-Andalus 554 catholic `define_pop`, Anatolia 527 turkic/mongol
   `define_pop`) are deletions or re-labels. Nothing else can do them.
2. **Only (a) is init-time**, and the errors being retired are init-time.
3. **It is the attested route** — three of three published conversions,
   including one at three times vanilla's population.
4. **The generator is the cheap part.** The file is regular enough that the
   parse is ~40 lines; the design work is in the rules, and the rules are
   the same rules whichever route carries them.
5. **Patch fragility is lower than it looks**, because the file is generated
   from vanilla each build, exactly like `10_countries.txt`.

**The honest counter, stated so the review can weigh it:** this ships the
largest file in the mod, ~5 MB of generated data no human will read, whose
correctness rests entirely on guards. Bronze Era shipped exactly this file,
exactly this way, broken in three independent ways, and nobody noticed. If
the review is not willing to fund the guard set in §D, route (a) should not
be taken.

### A.6 THE PROBE — the PYS shape, twelve lines, before the generator is written

The recommendation above rests on one unproven inference (append vs replace)
and one inherited inference (the map reads pops). Both are settled by **one
additive file and one launch**, and the probe costs nothing if it fails.

**File:** `main_menu/setup/start/50_1066_pop_probe.txt` — **NO BOM**, tabs,
sorted above vanilla's `27_`.

```
locations = {
	mistretta = {
		define_pop = {	type = peasants	size = 60.000	culture = maltese	religion = sunni }
	}
}
```

**Why `mistretta`.** It is in `sicily_area`, owned by SIC in the current
build, and carries **exactly two** vanilla pops — `clergy 0.009
sicilian/catholic` and `peasants 26.315 sicilian/catholic` — with a template
of `sicilian`/`catholic`. `maltese` is a real shipped culture (one pop
location, `malta`) and `sunni` is unmistakable on the religion map mode. The
probe pop is **60.000 units, deliberately larger than the 26.315 it sits
beside**, so an append flips the location's *dominant* religion and the map
colour changes in one glance.

**The four outcomes, and what each one decides:**

| what the location panel and religion map mode show | conclusion | consequence |
|---|---|---|
| **3 pops; dominant religion Sunni; Mistretta reads Sunni on the map** | additive files **APPEND**; the map reads pops | the recommendation stands unchanged; route (c) stays deferred forever |
| **1 pop (only the maltese/sunni one)** | additive files **REPLACE** a location's pop block | **the 5 MB override becomes unnecessary** — the whole phase can ship as one additive file listing only corrected locations. Re-open §A before writing the generator |
| 3 pops, but the map mode still paints Mistretta catholic | the map reads `location_templates.txt` | **route (c) becomes mandatory**, and the phase doubles in size. This is the fork `POP-PHASE.md:56-58` named. Prior is strongly against it (§A.3) |
| unchanged — 2 pops, catholic | the file never parsed | check the first three bytes (`head -c 3 … \| od -An -tx1`), check the filename sorts after `06_`; the additive-file mechanism is already proven by `04_zz_1066_dynasties.txt`, so a null result is a defect in the probe, not a finding |

**Discipline:** the probe file is deleted in the same commit that records its
result. It is a measurement instrument, not content. It must never ride the
grand accumulated test alongside a real slice, because two changes in one
launch cannot be told apart.

---

## B. THE CORRECTION INVENTORY, re-measured

### B.0 The master table

All counts are `06_pops.txt` measurements against the **current build's**
ownership (the mod's `10_countries.txt`, ten-key reader). "pops" is the
number of `define_pop` lines a rule touches, not the number in the theatre.

| # | theatre | locs in scope | locs touched | `define_pop` touched | units | rule | inherited from |
|---|---|---|---|---|---|---|---|
| 1 | **al-Andalus** (the 244 `_TAIFAS`) | 244 | 224 | **554** | 3,036.5 | catholic → sunni / `mozarabic` | HANDOFF item 13; `POP-PHASE.md:79` |
| 2 | **Anatolia** (`anatolia_region`) | 258 | 217 | **527** | 2,180.7 | delete turkish/turkoman/mongolian/nogai, redistribute | `POP-PHASE.md:80` |
| 3 | **the Wendish shore** (`mecklenburg` 15 + `pomerania` 31 + `brandenburg` 41) | 87 | 87 | **285** | 1,585.1 | catholic → `slavic_paganism` (invented; user decision 2026-07-29) | `POP-PHASE.md:100-105`; `BALTIC-PACKAGE.md` §H |
| 4 | **Egypt** (`egypt_region`) | 82 | 76 | **164** | 3,776.9 | raise miaphysite share against sunni | `POP-PHASE.md:83` |
| 5 | **`baltic_area`** | 56 | 56 | **153** | 283.2 | catholic → romuva | `BALTIC-PACKAGE.md` §H |
| 6 | **`finland_area`** | 58 | 35 | **107** | 95.5 | catholic → muinaisusko | `BALTIC-PACKAGE.md` §H |
| 7 | **`prussia_area`** | 44 | 39 | **99** | 267.3 | catholic → romuva | `BALTIC-PACKAGE.md` §H |
| 8 | **Sicily** (`sicily_area`) | 23 | 23 | **85** | 694.5 | catholic → sunni on a `maltese` Siculo-Arab layer | `POP-PHASE.md:81` |
| 9 | **`ghana_area`** | 31 | 31 | **60** | 156.3 | sunni share → `nyama_religion` | `AFRICA-PACKAGE.md` §H |
| 10 | **`kanem_area`** | 24 | 20 | **54** | 232.5 | sunni share → `karama_religion` | `AFRICA-PACKAGE.md` §H |
| 11 | **Persia + Khorasan** | 896 | 330 | **532** | 593.5 | strip the Mongol layer | `POP-PHASE.md:84` |
| 12 | **Ireland** (`ireland_region`) | 95 | 26 | **50** | 120.6 | delete `anglo_irish`/`english`, keep `norse_gael` | `POP-PHASE.md:85` |
| 13 | **Wales** (`wales_area`) | 25 | 15 | **19** | 54.8 | delete `english` | `POP-PHASE.md:86` |
| 14 | **HPJ** | 12 | 9 | **14** | 37.5 | `khon_muang_culture` → `mon_culture` | `SEA-PACKAGE.md` decision 4 |
| 15 | **TKA `xining_province`** | 6 | 6 | **12** | 56.1 | strip the post-1104 Song layer | `TIBET-PACKAGE.md` §A.3 |
| 16 | **PRM's Kipchak slave layer** | 64 | 10 | **10** | 34.1 | `chiyalik_culture`/`tengri` slaves on ten Bashkir-edge locations | **NEW — found this session** |
| 17 | **KED `perlis`** | 3 | 1 | **1** | 1.8 | sunni → mahayana | `SEA-PACKAGE.md` §H |
| | **TOTAL** | | | **2,726** | | | **5.4 % of 50,255** |

Two different honest totals are in circulation and both should be quoted:
`POP-PHASE.md:90`'s **~5,623 entries = 11.2 %** counts *every pop in the
listed theatres*; this table's **2,726 = 5.4 %** counts *only the pops a rule
touches*. The second is the number that matters for guards and for review.

### B.1 al-Andalus — the largest item, and the one with a named debt

The taifa slice (HANDOFF item 13) shipped with the limit stated out loud to
the user: *"pops are still 1337-Christian — Castilian Seville is EXPECTED;
the pop conversion slice is the named follow-up"* (`HANDOFF.md:407-408`).
This is that follow-up.

**The ground, exactly** (the 244 locations of `build_setup._TAIFAS`, all 244
still held by their 13 taifas in the current build):

| | value |
|---|---|
| `define_pop` in the 244 | **928** |
| units | **3,902.4** |
| catholic | **554 pops / 3,036.5u / 77.8 % — on 224 of 244 locations** |
| sunni | 204 pops / 801.6u / 20.5 % — on 175 locations |
| judaism | 170 pops / 64.3u / 1.6 % — on 142 locations |
| locations with **zero** sunni pops | **69** |
| locations with **zero** `andalusi` pops | **69** (the same 69 — `andalusi` and `sunni` are co-extensive here) |
| the catholic pops' cultures | castilian 271, portuguese 87, catalan 76, aragonese 69, leonese 34, ligurian 10, basque 4, gascon 2, french 1 |
| the catholic pops' types | peasants 238, clergy 222, nobles 52, burghers 42 |
| already at 4 pops of one type | **11 locations** |

**Per taifa** (locations / with-any-sunni / with-any-catholic / with-any-judaism):

| tag | locs | sunni | catholic | judaism |
|---|---|---|---|---|
| BDJ | 63 | 50 | 63 | 51 |
| TOL | 62 | 38 | 62 | 30 |
| SEV | 28 | 14 | 26 | 14 |
| ZGZ | 22 | 22 | 22 | 15 |
| GRZ | 20 | 14 | 8 | 8 |
| MRU | 15 | 8 | 15 | 6 |
| CRD | 9 | 4 | 9 | 4 |
| DYA | 8 | 8 | 8 | 5 |
| ALM | 7 | 7 | 1 | 2 |
| ABR | 4 | 4 | 4 | 3 |
| LRD | 4 | 4 | 4 | 2 |
| ALP | 1 | 1 | 1 | 1 |
| QRM | 1 | 1 | 1 | 1 |

The pattern is legible and it is exactly the 1337 Reconquista frontier: ALM
and GRZ (the deep south) are the least Christianised; BDJ and TOL (the
Christian conquests of 1085-1230) are the most. **The correction is
therefore not uniform — it is a reversal of the frontier's direction.**

**The rule set to design (not decided here — OPEN DECISION 3):** the two
defensible shapes are (i) *re-label* — every catholic pop in the 244 becomes
`mozarabic`/`catholic`, preserving unit totals exactly and keeping the
Mozarab community that genuinely existed, with `andalusi`/`sunni` amplified
from its existing 175-location seed; or (ii) *convert* — the majority of
catholic peasant units become `andalusi`/`sunni` and a `mozarabic` minority
is left behind at a named percentage. (i) is unit-conserving and cheap;
(ii) is closer to the demography [D] and is a balance change.

**Free consequences of either shape:** `is_dhimmi` (`pop_triggers.txt:1-15`,
religion-group + Muslim owner) puts the `mozarabic` and `sephardi` pops into
`dhimmi_estate` automatically, with no authored line. The 170 judaism pops
should not be touched.

### B.2 The Baltic — the tightest correction in the inventory, and it verifies twice

`BALTIC-PACKAGE.md` §H banked this as *"the single largest correction the
pop phase inherits from this theater"*. Re-measured on pops it is smaller
than the template said in Prussia and **larger** than the template said in
the Baltic proper.

| area | locs | catholic `define_pop` | units | locations with **no** pagan pop at all | owners in the current build |
|---|---|---|---|---|---|
| `baltic_area` | 56 | **153** | 283.2 | **52 of 56** | ESO 24, LTG 17, KUO 8, ZEM 7 |
| `prussia_area` | 44 | **99** | 267.3 | 16 of 44 | PRS 26, POL 16, SUD 2 |
| `finland_area` | 58 | **107** | 95.5 | 36 of 58 | SWE 32, unowned 26 |

**The independent second measurement.** §0.1's registry-vs-ground scan asked
a completely different question — *which landed tags have a
`religion_definition` that appears in none of their own locations' pops?* —
and returned ten tags world-wide. **Three of them are this theatre, and
their location counts sum to exactly the ground above:**

| tag | locs | `religion_definition` | that religion's locations world-wide | registry `file:line` |
|---|---|---|---|---|
| **ESO** | 24 | `muinaisusko` | 128 | `zz_1066_new_countries.txt:625` |
| **LTG** | 17 | `romuva` | 107 | `zz_1066_new_countries.txt:617` |
| **ZEM** | 7 | `romuva` | 107 | `zz_1066_new_countries.txt:609` |

ESO 24 + LTG 17 + ZEM 7 = **48 locations whose own state religion is on none
of their ground**, plus KUO's 8 (which already carry romuva on 4). Two
independent scans, same answer. **This is the recommended FIRST real slice
(OPEN DECISION 2)**: it is the smallest theatre with the strongest signal,
its tags were minted by this project so no vanilla intent is being
overridden, and it has a one-glance in-game test that survives pop inflation
— open ESO/LTG/ZEM and read religious unity, which is structurally 0 today.

`samogitia_area` is the control: **16 locations, 53 pops, 100 % romuva** —
vanilla already got it right, and a rule that touches it is a bug.

### B.3 Anatolia — the largest deletion, and the acceptance-cost risk

258 locations, 1,003 pops, 5,370.6 units. Culture shares: greek 32.4 %,
**turkish 26.4 %**, **turkoman 13.0 %**, armenian 12.1 %, pontic greek
7.5 %, laz 3.6 %, cappadocian greek 1.6 %.

**217 locations carry a turkish/turkoman/mongolian/nogai pop, across 527
`define_pop`.** Forty-one Anatolian locations carry **no** orthodox,
miaphysite or nestorian pop at all — those are the ones a deletion rule
leaves empty and must re-seed (`POP-PHASE.md:80`'s "seed the 41
Christian-less locations" reproduces exactly).

This is the item with the **largest side-effect risk in the whole phase**,
and it is not the deletion — it is
`ACCEPTED_CULTURE_SETUP_ERROR_IF_ABOVE_MAX = 2` /
`ACCEPTED_CULTURE_SETUP_ERROR_IF_BELOW_MAX = 1`
(`00_defines.txt:1508-1509`), which fire in **both** directions and are
evaluated against country-wide and world-wide culture shares. Deleting
1,425.3 units of `turkish_culture` and 734.0 of `turkoman_culture` moves the
world share of every other culture slightly and the Anatolian countries'
shares enormously. **`POP-PHASE.md:66-73` already warns that this is a
mod-wide new error class that any one slice can trigger outside its own
theatre.** Anatolia should therefore be **late** in the slice order, and the
launch after it must re-read the accepted-culture error class everywhere,
not just in Anatolia.

### B.4 Persia + Khorasan — and how wide the Mongol strip really is

`POP-PHASE.md:84` scoped this as "451 units / 150 locs" in Seljuk Persia.
Measured on the two regions with the correct keys (`mongolian_culture` **and
`nogai` — no `_culture` suffix**, the spelling trap):

| region | ownable locs | mongol/nogai carrier locs | `define_pop` | units |
|---|---|---|---|---|
| `persia_region` | 479 | 95 | 188 | 259.4 |
| `khorasan_region` | 417 | 235 | 344 | 334.2 |
| **both** | 896 | **330** | **532** | **593.5** |

And the world-wide total, which is the number the decision needs:
**`mongolian_culture` + `nogai` sit on 1,192 locations, 1,943 `define_pop`,
2,507.1 units**, distributed:

| region | carrier locations |
|---|---|
| steppes | 188 |
| khorasan | 185 |
| **mongolia** | **166** |
| persia | 95 |
| south_china | 82 |
| west_china | 78 |
| russian | 76 |
| west_siberia | 74 |
| xinjiang | 32 |
| east_china | 25 |
| anatolia | 24 |
| north_china | 22 |
| manchuria | 21 |
| ruthenia | 16 |
| caucasus | 12 |
| tibet | 6 |
| hindustan | 3 |

**`mongolia_region`'s 166 must be KEPT** — Mongols in Mongolia in 1066 are
correct. Everything west and south of it is Chinggisid paint on a
pre-Chinggisid map. **How far the strip reaches is OPEN DECISION 6**, and
it is the single largest scope question in the phase: 330 locations
(Persia+Khorasan only) versus ~1,026 (everything but Mongolia).

### B.5 Africa — Ghana and Kanem, where the ground is *more* Islamic than the countries

`AFRICA-PACKAGE.md` §H banked the correction conditionally on its OPEN
DECISION 4 ("pagan kings"), which landed: `HANDOFF`'s commit `5a2977d`
overrode two African registries for *"Christian Makuria, pagan Hausa"*.

| area | locs | sunni `define_pop` | units | locs with any sunni | the pagan alternative already present |
|---|---|---|---|---|---|
| `ghana_area` | 31 | **60** | 156.3 | **31 of 31** | `nyama_religion` 10.6 % on 13 locations |
| `kanem_area` | 24 | **54** | 232.5 | 20 of 24 | `karama_religion` 7.6 % on 6; `sao_religion` 13.6 % on 4 |

The sunni pops by culture — Ghana: soninke 34, lamtuna 11, godala 8, tuareg
4, dyula 2, mandinka 1; Kanem: kanembu 32, toubou 17, bilala 3, tuareg 2.

**The design point.** This is not a delete-and-replace like the Baltic. The
Sahel in 1066 is genuinely mixed: the Almoravid Lamtuna and the trans-Saharan
Dyula merchants ARE Muslim in 1066 [D], while the Soninke court and
countryside are not yet [D]. The honest rule is a **share shift by culture**
— `soninke` and `kanembu` peasant/tribesmen pops move to
`nyama_religion`/`karama_religion`, while `lamtuna_culture`, `dyula` and
`tuareg` pops stay sunni. That rule is expressible in ~6 lines and is
defensible; a blanket area sweep is not. `mali_area` (31 locs, already
57.6 % sunni / 42.4 % nyama on **all 31**) is the model vanilla itself
already ships and the shape to copy.

### B.6 The four micro-corrections — one slice, 37 `define_pop`

Small enough to ride together, and each closes a package's named debt.

**HPJ (12 locations, 14 pops).** Registry `culture_definition = mon_culture`
(`zz_1066_new_countries.txt:665`), deliberately chosen against the map data
under `SEA-PACKAGE.md` decision 4. Ground: nine locations are
`khon_muang_culture`/`theravada` over a `lawa_culture` peasant substrate;
three (`mae_hong_son`, `muang_yuam`, `sariang`) are
`karen_culture`/`karen_religion`. Rule: the **14 `khon_muang_culture`
`define_pop` become `mon_culture`**; the Lawa substrate and the Karen three
stay — Haripunjaya was a Mon court over a Lawa countryside [D], which is
what that shape says. HPJ is one of the twelve tags in §0.1's culture scan
whose `culture_definition` appears on none of its own ground; this is the
fix.

**TKA (6 locations, 12 pops).** `xining_province` is painted for the
post-1104 Song Xining [U] — `liang_culture`/`sanjiao` on 4,
`monguor_culture`/`mahayana` on 2, plus **`mongolian_culture` clergy pops on
3** (`gushan`, `nianbo`, `xining` — `zhuanglang`'s clergy is `liang_culture`)
and `mi_niah_culture`/`mahayana` on 4.
`amdowa_culture`/`tibetan_buddhism` already exists on 5 of the 6 as a
minority (all but `zhuanglang`). Rule: raise `amdowa` against `liang`, and
delete the three `mongolian_culture` clergy pops — a Mongol clergy in an
1066 Huangshui valley is indefensible at any reading. Note `zhuanglang` is
31.028 units of `liang_culture` and is genuinely Chinese ground; it should
keep its character.

**KED `perlis` (1 pop).** `bujang` and `kedah` are **already `mahayana` in
pops**; only `perlis` carries `peasants 1.811 malay_culture/sunni`. One line.

**PRM's Kipchak slave layer (10 locations, 10 pops) — NEW.** Ten of PRM's 64
locations (`aspa kasevo orda osa saygatsky suksun tatyshly ust_kishert
yanaul yelovo`) have **exactly one pop each and it is
`slaves / chiyalik_culture / tengri`** — 34.1 units total. Chiyalik is a
Golden-Horde-era Kipchak identity; ten locations on the Bashkir edge of Perm
populated *exclusively* by Kipchak slaves is a 13th-century tableau standing
on an 11th-century map. Rule: re-label to `komi`/`komi_paganism` or
`bashkir`/`tengri` peasants — a decision for the slice, not for this package.

### B.7 The remaining named items, sized

| item | measurement | note |
|---|---|---|
| **Sicily** | 23 locations, 88 pops, 716.1u; **catholic 97.0 %**, `sicilian` 91.9 %; `griko_culture` on 3, `maltese` on 1 (`malta`, 17.0u), sunni **0.0 %**. Currently split AGR 10 / PLM 9 / SIC 4 | 100 % invention: `maltese` is the shipped Siculo-Arabic (`POP-PHASE.md:81`). The most *interesting* slice and the least *necessary* one |
| **Ireland** | 95 locations, 345 pops, 708.3u; irish 82.7 % on all 95; **`anglo_irish` 42 pops on 25 locations (113.6u)**, `english` 8 pops on 3 (7.0u), `norse_gael` 8 pops on 4 (0.9u) | pure deletion; **retires three named error lines** (`EU5-ERROR-DECODER.md:544` — DUB's upper class reads `anglo_irish`). `norse_gael` KEPT |
| **Wales** | 25 locations, 58 pops, 308.7u; welsh 79.6 %, **`english` 19 pops on 15 locations (54.8u)** | pure deletion; retires the CMS/EWY lines (`EU5-ERROR-DECODER.md:533`) |
| **Egypt** | 82 locations, 301 pops, 5,076.2u; sunni 74.4 % on 76, **miaphysite 14.3 % on 74**, shia 7.1 % on 7, orthodox 3.5 % on 26 | a share shift, not a re-label — miaphysite is already on 74 of 82. The target percentage is DEBATED and must be a named constant [U 0.30-0.60] |
| **the Wendish shore** | `mecklenburg_area` 15 locs / 381.6u catholic, `pomerania_area` 31 / 513.1u, `brandenburg_area` 41 / 690.3u — **285 catholic `define_pop`, 1,585.1u across 87 locations** | Mecklenburg + Pomerania alone = **894.7u**, which reproduces `POP-PHASE.md:104`'s 895.8 to within a rounding of the pre-Baltic-slice boundary. **Brandenburg's 690.3u was NOT in the banked figure** — OPEN DECISION 5 |

### B.8 The registry-vs-ground scan — the phase's own new finding

Running §0.1's scan over **every** landed tag in the current build (2,411
country blocks, 1,360 landed) against the **effective** registry (vanilla's
45 files minus the five the mod overrides by name, plus
`zz_1066_new_countries.txt` — 2,414 blocks) produces two short lists that
nobody has had before. These are *diagnostics*, not a work list: several are
deliberate design choices already recorded elsewhere.

**Landed tags whose `religion_definition` appears in NONE of their own
locations' pops — 10:**

| tag | locs | religion | that religion's world-wide pop locations | registry |
|---|---|---|---|---|
| PAA | 80 | `mahayana` | 473 | `zz_1066_new_countries.txt:553` — **deliberate** (the "Buddhist identity over hindu pops" call) |
| **ESO** | 24 | `muinaisusko` | 128 | `:625` — §B.2 |
| BKH | 19 | `mahayana` | 473 | `east_asia.txt:3373` |
| **LTG** | 17 | `romuva` | 107 | `:617` — §B.2 |
| UQY | 17 | `shia` | 496 | `:208` |
| AGR | 10 | `sunni` | 3,420 | `:365` — Kalbid Sicily; §B.7's Sicily slice IS this fix |
| PLM | 9 | `sunni` | 3,420 | `:357` — the same |
| **ZEM** | 7 | `romuva` | 107 | `:609` — §B.2 |
| KKY | 6 | `shia` | 496 | `:240` |
| SKN | 1 | `shia` | 496 | `egypt.txt:35` |

**Landed tags whose `culture_definition` appears in NONE of their own
locations' pops — 12:** CUM 211 (`cuman_culture`, on 5 world-wide),
GHZ 131 (`turkish_culture`), HLL 13 (`hijazi_culture` — vanilla's own
choice, already accepted at `EU5-ERROR-DECODER.md:546`), **HPJ 12**
(`mon_culture` — §B.6), KIM 10 (`tagakaulo_culture`), SHD 6
(`kurdish_culture`), BKZ 4 (`bedouin_culture`), ZAH 4 (`rhine_alemannic`),
CEM 3 (`kurdish_culture`), JSK 2 (`farsi_culture`), DCI 1 (`anglo_irish` —
✎REVIEW: the Ireland deletion ENTRENCHES this mismatch rather than fixing
it — a registry-side call, parked with the other registry questions),
EGL 1 (`kurdish_culture`).

**CUM is the one that should worry a reviewer:** 211 locations, and
`cuman_culture` exists on **five** locations in the entire world's pops. A
Cuman confederation of 211 locations with no Cuman pops is the largest
single registry/ground mismatch in the build. It is not in any banked list.
**OPEN DECISION 8.**

Finally, of the *effective* registry's 2,414 blocks, exactly **two** name a
culture that sits on zero pop locations world-wide: ACC's
`acciaioli_bank_culture` and PRZ's `peruzzi_bank_culture` — vanilla's two
building-based bank tags, working as designed.

---

## C. SCOPE DISCIPLINE — what must NOT be touched

### C.1 What is already right, measured

The packages kept finding that vanilla's data is 1066-correct, and the pop
layer confirms it at a scale worth stating plainly.

| ground | measurement | why it is right |
|---|---|---|
| **The Perm/Vyatka Uralic religions** | `komi_paganism` on **71** pop locations, `samoyedic_paganism` **63**, `obian_paganism` **84**. PRM's own `komi_paganism` appears on **53 of its 64** locations. The other eleven registry entries (OBD LYA SLK PLY BAK KND BGJ KOD SVA KZY TBY) are **`type = pop` countries** — they hold no land by design — and each one's `add_pops_from_locations` set carries its own religion in pops (OBD 5 locs all `samoyedic_paganism`; BAK 2 all `obian_paganism`; SLK 23 `samoyedic_paganism` + `tengri` + `obian_paganism`) | **The single largest retirement in this package.** `PERM-VYATKA-PACKAGE.md` §0.5's headline is a `location_templates.txt` artefact end to end |
| **CLM's `teco_culture`** | 6 pop locations, **all six CLM's own** (`caxitlan chucutitlan coahuayana coliman tlayolan tochpan`; the seventh, `apatzingan`, is `purepecha_culture`) | the registry is right and the TEMPLATE is wrong. `AMERICAS-PACKAGE.md` §H's item is retired |
| **England** | `english` 158 pop locations world-wide; `norman` is 0.3 % of Britain | `POP-PHASE.md:87` — vanilla is accidentally right. NO CHANGE |
| **Scandinavia proper** | `samogitia_area` 16 locs / 53 pops / **100 % romuva** as the same-region control | `POP-PHASE.md:88` |
| **The Americas** | 3,948 unowned locations carrying 4,408 pops; 321 of the 448 `type = pop` identities are American | `AMERICAS-PACKAGE.md` §0.1/§0.9. The pop layer touches none of it |
| **Tibet** | `tibetan_buddhism` on 337 pop locations against 253 template locations — the plateau's pops are 1066-correct | `TIBET-PACKAGE.md` §H |
| **The Song** | CHI's 1,300 held locations are 96.1 % `sanjiao` by units; `kaifeng` is `zhongyuan_culture`/`sanjiao` throughout | item 41 fixed the *registry* to match this ground. Nothing left to do on the pop side |

### C.2 RENDER and REGISTRY questions that are NOT pop questions

Three inherited items look like pop work and are not. Doing them in the pop
phase would be doing them in the wrong file.

1. **The `wari_culture` → "Inca" render.** `wari_culture`
   (`peruvian.txt:693`) declares `language = quechuan_language` (`:694`);
   `country_ranks.txt` gates the whole Inca title family on
   `culture.language = language:quechuan_language` — `rank_empire_inca`
   `:345`, `rank_kingdom_inca` `:1173`, `rank_duchy_inca` `:1917`. So eleven
   Andean monarchies render "Inca" **because of a language field in a
   culture file**, and `wari_culture` sits on 64 pop locations (27 owned).
   Changing pops changes nothing; changing the *culture's language* or
   inserting a rank branch does. **This belongs to a naming/styling pass, in
   `common/`, and it is equally wrong at 1337** — `AMERICAS-PACKAGE.md` §H
   said so and filed it under POP-PHASE anyway. Re-file it.
2. **CLM's `teco_culture`** — retired above; if anything is wrong it is
   `location_templates.txt`, which route (c) says stay out of.
3. **PRM's `komi_paganism`** — retired above.

### C.3 What belongs to SITUATIONS, not to setup data

The pop file is a *start state*. Change over time is a different tool, and
route (d) (§A.4) is exactly right for it. Vanilla ships the modifier family
to drive it: `local_pop_conversion_speed` / `_modifier`,
`global_pop_conversion_speed` / `_modifier`, the heretic and heathen
variants, and `local_/global_pop_assimilation_speed` / `_modifier`
(`modifiers.log:614-625`), plus the per-pop-type assimilation blocks at
`:1441-1448`.

Four things the inventory should hand to the situations backlog rather than
bake into 1066's start:

- **the Almoravid conversion of the Sahel** — Ghana and Kanem's Islamisation
  is a *process* running through the 11th and 12th centuries [D]; §B.5 sets
  the 1066 state, and a situation moves it;
- **the Turkification of Anatolia** — the thing §B.3 is deleting is the
  *result* of Manzikert (1071, five years from start). A Manzikert situation
  that converts Anatolian pops over 200 years is the correct home for what
  is currently baked into the file, and it is already the named first
  situation (`HANDOFF.md:2074`);
- **the Reconquista's Mozarab decline** — the inverse of §B.1;
- **the Wendish Crusade (1147)** — already banked with the
  `slavic_paganism` decision (`POP-PHASE.md:104-105`).

Stated as a rule: **if the correct 1066 value and the correct 1337 value
differ *and vanilla's number is the 1337 one*, the pop phase writes the 1066
number and a situation carries the road between them.** That is the whole
justification for a 1066 conversion doing pop work at all.

---

## D. HARNESS — what a `06_pops.txt` override obliges

A 5 MB generated file that no human will read is guarded or it is not
shipped. Every check below must be **proven by breaking** before it is
trusted (`CLAUDE.md`, "A check never seen failing is untested"), and every
one prints its item count.

| # | check | assertion | why (and the failure it catches) |
|---|---|---|---|
| D1 | **block-name SET equality** | the mod file's set of location block names == vanilla's, **28,570**, and every name occurs **exactly once** | the Bronze Era guard: catches all three of duplicates (2,633), phantoms (502) and drops (3,131) in one comparison. Without it, none of the three errors anything |
| D2 | **`define_pop` census** | total == 50,255 ± the slice's declared delta, asserted per slice as an exact number | the count assert is the only defence against an over-broad rule (`KNOWLEDGE.md:2147`, the Tibet donor-table law) |
| D3 | **four-field shape** | every `define_pop` matches `type … size … culture … religion` and nothing else | Location Painter emits `literacy`, which is UNATTESTED (`POP-PHASE.md:22`) |
| D4 | **identifiers resolve** | every culture and religion token in the file exists in `common/cultures/` or `common/religions/` **or in our own additive files** — using the **nested-declaration-aware** reader (4 vanilla cultures are declared nested) and remembering that **332 of 2,087 culture keys lack the `_culture` suffix** | a misspelt culture does not error, it silently does nothing |
| D5 | **the merge safe zone** | no location exceeds **3** pops of one type in any location the mod TOUCHED; ceiling **6** anywhere (vanilla's own max) | ≥4 merges similar, ≥8 collapses to the largest (`00_defines.txt:1633-1634`). Vanilla itself sits at 4-6 in 314 locations, so the check must be scoped to *touched* locations or it fails on vanilla's data — the "validate what we wrote, report what vanilla shipped" law |
| D6 | **unit conservation** | for every re-label rule, total units in the touched set are unchanged ±0.1 % | a re-label that silently changes population is a balance change wearing a data commit's clothes |
| D7 | **rule coverage** | every location named by a rule set exists in `06_pops.txt` **and** in `_ownable_set()` | a typo'd location key is a silent no-op |
| D8 | **no culture emptied without a flag** | no culture whose world-wide pop-location count reaches 0 unless it carries `suppress_no_pops_error = yes` — **and the check must know that vanilla already ships three such cultures without the flag** (§0.7) | the `anglo_irish → 0` case, which the Ireland slice creates |
| D9 | **share bands** | per-theatre assertions that the post-build religion/culture share lands inside the designed band | the only guard on the *design*, as opposed to the mechanics |
| D10 | **UPPERCASE-safe key regex** | the generator's location regex is `[A-Za-z0-9_]+`, proven by asserting all **11** uppercase keys survive the round trip | a lowercase regex drops `trgoviste_SER` and ten others, 28 pops, silently — it already happened once to a research agent's parser |

**Existing checks that move on the same commit:**

| check | `tools/verify_mod.py` | now | after |
|---|---|---|---|
| `no BOM in setup/start` | `:125` | `min_count=6` | **7** — and `06_pops.txt` must be BOM-free like the other six (all six current files verified BOM-free this session) |
| `braces balanced per file` | `:137` | — | will now scan a 5 MB file; confirm it still runs in reasonable time |

**Checks that do NOT move.** The pop phase touches no country block, no
registry entry, no diplomacy line and no IO. `exactly one ruler key per
country block` (`:938`, 2,411), `landed countries reach a parliament_type`
(`:1244`, 1,360 — reproduced exactly this session), `IO members hold land`
(`:884`, 850), the CoA floor (`:1086`, 125) and the gate floor (`:843`, 79)
all stay where they are. **If a pop commit moves any of them, something
other than pops was edited.**

---

## OPEN DECISIONS

**1. Which mechanism route?**
**Recommendation: route (a), a whole-file `06_pops.txt` override generated by
`build_setup.py` as a sixth `TARGETS` entry** — because only (a) can delete,
only (a) is init-time (and the errors being retired are init-time), and three
of three published conversions do it.
**Counter, and it is real:** this ships ~5 MB of generated data whose
correctness rests entirely on guards, in a file that has already been shipped
broken-in-three-ways by a published mod. Route (b) — additive, ~100 lines,
zero patch surface — covers every *seeding* correction in §B (Ghana, Kanem,
Egypt, Sicily, half the Baltic) and cannot break anything. A conservative
main session could ship the additive half first, get the in-game signal, and
only then fund the override for the deletions.

**2. What is the first slice?**
**Recommendation: the Baltic (ESO/LTG/ZEM, 48 locations, ~250 `define_pop`
across `baltic_area` + `prussia_area`)** — not `POP-PHASE.md:126`'s Sicily.
Reasons: it verifies from two independent directions (§B.2), the tags are
this project's own so no vanilla intent is being second-guessed, the in-game
signal (three countries' religious unity moving off structural zero) survives
pop inflation and needs no launch option, and it is a correction rather than
an invention.
**Counter:** Sicily is smaller (23 locations, 85 pops) and it is the theatre
`POP-PHASE.md` designed the probe around. But Sicily is 100 % invention — if
it looks wrong in game there is no way to tell a mechanism failure from a
design disagreement, which is exactly what a slice-0 must not have.

**3. al-Andalus: re-label or convert?**
**Recommendation: re-label** — the 554 catholic `define_pop` become
`mozarabic` (Basileia's key, `br_iberia.txt:24`) at unchanged sizes, and the
existing `andalusi`/`sunni` seed on 175 locations is amplified toward a named
target share on the 69 locations that have none. Unit-conserving, guard D6
applies, and it produces a genuinely Mozarab al-Andalus rather than a
counterfactual one.
**Counter:** 3,036.5 units of Mozarabs against 801.6 of Muslims inverts the
real demography of 1066 al-Andalus, where Arabised Muslims were already the
majority in the south [D]. A pure re-label ships a taifa realm that is 78 %
Christian, which is the *same* wrongness with a better label on it. The
honest version is a conversion with a named constant, and it is a balance
change that must be declared as one.

**4. Invent `mozarabic`, or re-point `andalusi`?**
**Recommendation: invent `mozarabic` via `REPLACE_OR_CREATE:` in an additive
`in_game/common/cultures/` file** (BOM, per the tree's rule), copying
Basileia's shape but **not** its `local_pop_conversion_speed_modifier = -0.25`
unless the review wants that balance effect deliberately.
**Counter:** every invented identifier is a new maintenance surface with its
own loc keys, colour and `culture_groups` membership, and `andalusi` already
exists on 218 pop locations. Using `andalusi` for everyone and skipping the
invention costs one decision and zero files.

**5. Does `slavic_paganism` reach Brandenburg?**
**Recommendation: yes — all 87 locations** (`mecklenburg` 15, `pomerania` 31,
`brandenburg` 41), 285 catholic `define_pop`, 1,585.1 units. The Great Slav
Rising of 983 threw the Havelberg and Brandenburg bishoprics out, and the
Hevelli and Sprevane are pagan again by 1066 [D].
**Counter:** the banked figure was **894.7 units (Mecklenburg + Pomerania
only)** and Brandenburg's 690.3 nearly doubles it. Brandenburg is also HRE
ground and Germany-slice territory (`BALTIC-PACKAGE.md` §H explicitly left
the Wendish shore to a German pass), so taking it here reaches across a seam
another slice owns.

**6. How wide is the Mongol strip?**
**Recommendation: Persia + Khorasan + Anatolia + Caucasus + Ruthenia +
Russia + the steppes — everything except `mongolia_region`'s 166 carrier
locations**, i.e. roughly 1,026 locations and ~1,600 `define_pop`, staged
across the slices that own those theatres rather than as one sweep.
**Counter:** at 1,026 locations this becomes the largest single item in the
phase, larger than al-Andalus and Anatolia combined, and it crosses eight
theatres whose packages all measured "leave it alone". The minimal reading —
Persia + Khorasan's 330 locations, `POP-PHASE.md:84`'s scope — is safe,
defensible on its own, and leaves the rest to whoever next opens the steppe.

**7. Egypt's Coptic share.**
**Recommendation: raise miaphysite toward 0.40 of Egyptian units as a NAMED
CONSTANT with a `[U 0.30-0.60]` comment**, never a number baked into the
rule. Ground today: 74.4 % sunni / 14.3 % miaphysite over 82 locations.
**Counter:** the date at which Egypt's Christian majority ended is one of the
most contested numbers in the field [D]; 0.40 at 1066 is a choice, not a
finding, and shipping it as data makes it look like a measurement. An
alternative is to leave Egypt alone and let a situation carry the decline —
Egypt is not one of the theatres where the 1337 number is obviously wrong at
1066.

**8. CUM — 211 locations, `cuman_culture` on five in the world.**
**Recommendation: out of scope for this phase; open it as a Steppe pop
question.** It is a registry/ground mismatch of a different kind and size
from everything in §B, it was created by this project's own Rus/steppe
slices, and it needs a Cuman demographic design before it needs a file edit.
**Counter:** 211 locations is the largest mismatch in the build and the pop
phase is exactly where such things are supposed to be settled. Deferring it
means the phase closes with the biggest one still open.

**9. `-leavepops` for the test, or identity-only tests?**
**Recommendation: identity-only tests.** Every click tour in §B is written to
read *which* cultures and religions are present and which is dominant — all
of which survive inflation — so no launch option is needed and the pop tours
can ride the ordinary accumulated test.
**Counter:** any slice that changes pop *sizes* (a conversion rather than a
re-label — decision 3's counter) cannot be verified without `-leavepops`, and
finding that out after the launch wastes a test session. If decision 3 lands
on "convert", decision 9 must land on `-leavepops`.

**10. One slice or many?**
**Recommendation: per-theatre slices in the order Baltic → Wales+Ireland →
the four micro-corrections → Ghana/Kanem → al-Andalus → Sicily → Egypt →
Mongol strip → Anatolia last** (Anatolia last because §B.3's
accepted-culture class can fire mod-wide and should not be entangled with a
first launch).
**Counter:** every slice re-emits the whole 5 MB file, so the per-slice cost
is not the file, it is the launch. Ten slices is ten launches of the user's
time, and the user is already accumulating tests deliberately. Two batches —
"the deletions" and "the seedings" — may be the right granularity.

---

## Implementation checklist

Nothing below is authorised; it is the shape a decided version would take.

1. **The probe first (§A.6).** `50_1066_pop_probe.txt`, no BOM, one
   location, one pop. Launch, read the four outcomes, record the answer in
   `KNOWLEDGE.md`, **delete the probe file in the same commit as the
   result.** Do not run it in the same launch as any other change.
2. **If the probe says APPEND (expected):** add
   `("06_pops.txt", build_pops)` to `TARGETS` (`build_setup.py:8338`) and
   write `build_pops` as a two-level brace walk that (a) parses vanilla's
   file into `[(name, [pops])]` preserving order, (b) applies the slice's
   rule sets, (c) re-emits. Reuse `_defs()` / `_resolve_ruleset` / `_TAIFAS`
   so pop scope keys off the **same source of truth as borders**.
3. **Guards D1-D10 in the same commit as the first pop content**, each one
   proven by breaking (D1 by duplicating a block, D2 by widening a rule, D5
   by adding a fourth pop of a type, D10 by lowercasing the key regex and
   watching `trgoviste_SER` vanish). A guard added later is a guard that was
   never tested against the bug it exists for.
4. **Raise `no BOM in setup/start` from 6 to 7** (`verify_mod.py:125`) in
   that same commit, and confirm the emitted file's first three bytes are
   not `ef bb bf`.
5. **Slice by slice per decision 10**, each with: an exact touched-count
   assert, a donor-table equivalent (which pops change, from what, to what,
   how many lines — the Tibet law, `KNOWLEDGE.md:2147`), a Turkish click
   tour banked into a HANDOFF item, and an explicit sentence in that item
   saying **this is a balance change in a data commit's clothes**.
6. **Do not touch** `07_cities_and_buildings.txt` or
   `location_templates.txt`. Do not "fix" `tag = X … location = L`
   (`KNOWLEDGE.md`, first-class vanilla).
7. **Re-file the `wari`/Inca render** out of POP-PHASE and into a naming
   pass (§C.2), and **strike the retired items** from
   `PERM-VYATKA-PACKAGE.md` §0.5/§H and `AMERICAS-PACKAGE.md` §H with a
   one-line note saying which layer they were measured on — so the next
   session does not re-derive a non-problem.

---

## Expected constant moves

| constant | now | after the first pop slice | note |
|---|---|---|---|
| `setup/start` files shipped | **6** | **7** | `verify_mod.py:125` `min_count` 6 → 7 |
| largest file in the mod | `05_characters.txt`, 2.5 MB | `06_pops.txt`, ~5.0 MB | |
| `06_pops.txt` block count | (vanilla's) 28,570 | **28,570 — must not move, ever** | D1 |
| `06_pops.txt` `define_pop` | 50,255 | 50,255 ± the slice's declared delta | D2; the full inventory is **−/±2,726 at most**, 5.4 % |
| registry 74 / country blocks 2,411 / thrones 179 / deps 281 / pacts 9 / ghosts 160 / vacated 630 / parliament 1,360 / loc 375 / CoA 125 / gate 79 / IO floor 850 | as `HANDOFF.md:2044-2048` | **UNCHANGED** | the pop phase touches no country block. Any movement means something else was edited |
| error class `initialize_from_bookmark.cpp:237/:301` + `country.cpp:9778` | live, accepted | **GDD/MWG/DUB retire; GLC's portuguese line is expected to STAY** (✎REVIEW — GLC's portuguese pops are its own county of Portugal, which no slice touches) | `EU5-ERROR-DECODER.md:539-548` |
| error class `initialize_from_bookmark.cpp:205` | 8 lines | **UNCHANGED** (✎REVIEW — the draft forecast "shrinks by CMS/EWY/DCI", which is wrong-direction: CMS/EWY are `culture_definition = english` shells over Welsh cores (`british_isles.txt:474 :481`), and deleting english pops cannot feed them; DCI is not in this class at all) | `:530-537`; vanilla's own ATH line stays |
| error class: accepted-culture both directions | none | **NEW, mod-wide, unpredictable** | `00_defines.txt:1508-1509`; Anatolia is the trigger. Budget for it before the launch, not after |
| the vacated-pop class (`jomini_script_system.cpp:252`) | ~1,000 expected | **unchanged** — the pop phase vacates nothing | `:675-701` |

---

## VERIFICATION

### Mechanical claims — every one reproduced this session

| claim | source |
|---|---|
| `06_pops.txt`: 28,570 blocks, 50,255 `define_pop`, no BOM, 20,922 ownable covered, 119 empty-and-unowned, 7,648 non-ownable | `VAN/main_menu/setup/start/06_pops.txt`, parsed with `build_setup.find_block_end` |
| merge thresholds 4 / 8; `DISPLAY_SIZE = 1000`; accepted-culture setup errors 2 / 1 | `VAN/loading_screen/common/defines/00_defines.txt:1633-1634`, `:1601`, `:1508-1509` |
| location blocks MERGE across setup files: 1,023 locations in both `06_pops` and `07_cities`, 13,090 in both `06_pops` and `08_institutions`; `07_cities` carries zero `define_pop`, `06_pops` zero `rank`/`town_setup` | measured across the three vanilla files |
| `Location.GetCulture` / `Location.GetReligion` do not exist; only `GetDominantCulture` / `GetDominantReligion` | `docs/EU5-Vanilla-Script-Docs/data_types/data_types_uncategorized.txt:82405 :82423 :83209 :83227` |
| runtime pop toolset and scopes | `effects.log:331 :339 :953 :963 :968 :1460 :2518 :2548 :2908 :10459`; `on_actions.log:575` |
| vanilla `every_pop` + `split_pop` / `change_pop_religion` / `add_pop` shapes | `VAN/in_game/common/country_interactions/demand_conversion_to_islam.txt:39-49`; `generic_actions/reformation.txt:70-79`; `scripted_effects/location_effects.txt:71-93` |
| `on_game_start` is a real vanilla world-shaping hook, scope none | `VAN/in_game/common/on_action/_hardcoded.txt:1`; `ai_personalities_setup.txt:9` |
| the three published conversions' pop files, block/pop/duplicate/phantom/drop counts | Bronze `…/main_menu/setup/start/06_pops.txt`; Anno idem; Basileia idem + `06_pops_north_america.txt` + `06_pops_south_america.txt` |
| `REPLACE_OR_CREATE:` is real; Basileia's Iberian invention is **`mozarabic`**, not `mozarab` | `Basileia/in_game/common/cultures/br_iberia.txt:1` and `:24` |
| three zero-pop cultures, none carrying the flag; the flag's only occurrence is its own doc line; eight zero-pop religions | `VAN/in_game/common/cultures/italian.txt:247 :262 :307`; `00_cultures.info:28` |
| `wari_culture` → `quechuan_language` → the Inca rank family | `VAN/in_game/common/cultures/peruvian.txt:693-694`; `customizable_localization/country_ranks.txt:345 :1173 :1917` |
| the Uralic religions on pops (71 / 63 / 84); the eleven tags are `type = pop`; PRM's own 53 of 64 | `VAN/in_game/setup/countries/russia.txt:309`, `siberia.txt:1 :9 :17 :25 :32 :39 :46 :53 :60 :67 :74`; `06_pops.txt`; the mod's `10_countries.txt` |
| `teco_culture` on 6 locations, all CLM's | `06_pops.txt`; `VAN/in_game/common/cultures/mesoamerican.txt:61`; CLM registry `mesoamerica.txt:383` |
| `add_pops_from_locations` is a `10_countries.txt` field, not a `06_pops.txt` one; the mod ships 448 `type = pop` countries whose lists carry 4,011 entries with overlap = **3,736 distinct locations** (✎REVIEW) | `docs/Setup modding …pdf` ("If you are creating a non-playable pops based country"); the mod's `10_countries.txt` |
| 32 `mari_culture` pop locations, 0 covered by any pop-country | `06_pops.txt` × the mod's 448 `add_pops_from_locations` sets |
| every theatre count in §B.0 and §B.1-B.7 | `06_pops.txt` × `build_setup._TAIFAS` / `_defs()` / the ten-key ownership reader |

### Historical judgments — flagged, and none of them is settled here

| claim | flag |
|---|---|
| al-Andalus was majority Muslim in the south and Mozarab-minority by 1066 | **[D]** — the pace of Islamisation in al-Andalus is contested; the whole of decision 3 turns on it |
| the Hevelli/Sprevane of Brandenburg were pagan again in 1066 after the 983 rising | **[D]** |
| Sahel Islam in 1066 was a merchant-and-Almoravid religion, not a Soninke/Kanembu one | **[D]** |
| Haripunjaya was a Mon court over a Lawa countryside; the Khon Muang arrive in the 13th c. | **[D]** — inherited from `SEA-PACKAGE.md` decision 4, not re-derived |
| `xining_province`'s Chinese and Monguor pops are post-1104 Song paint | **[U]** — inherited from `TIBET-PACKAGE.md` §A.3 |
| Kedah's Islam is 12th-century | **[D]** — inherited from `SEA-PACKAGE.md` §H |
| Egypt's Coptic share at 1066 | **[U 0.30-0.60]** — the single most contested number in the inventory |
| Sicily's Siculo-Arab share (Mazara 0.80 / Noto 0.55 / Demone 0.25) | **[D]** — inherited from `POP-PHASE.md:81`, not re-derived |
| the `chiyalik_culture` slave layer in Perm is Golden-Horde-era | **[U]** — the culture's date is inferred from its identity, not from a vanilla date field |
| whether emptying a culture world-wide actually errors | **[U] — and it is a MECHANICAL unknown, not a historical one.** Vanilla ships three zero-pop cultures with no flag. Confirm at the next launch before designing around it |

### What this package did NOT verify, and a reviewer should not assume it did

1. **Append vs replace for a repeated `define_pop` across files.** Inferred
   from three converging sources (§A.2) and left as the probe's job. If a
   reviewer treats it as established, the probe loses its point.
2. **That the religion/culture map modes read pops.** Strongly implied by
   the absence of `Location.GetCulture`/`GetReligion` and by 2,142 shipped
   disagreements, but **not observed in game**. Also the probe's job.
3. **Whether `location_templates.txt` drives anything at all.** This package
   establishes that the GUI cannot read it and that vanilla contradicts it
   2,142 times. It does not establish what it *does* — only that nothing in
   the inventory needs it.
4. **Timing of `on_game_start` relative to bookmark init.** §A.4's third
   argument rests on the function names and on `KNOWLEDGE.md`'s measured
   "registry fields are read at bookmark init only". It is a strong
   inference, not a measurement, and it is the load-bearing reason route (d)
   is rejected — if a reviewer wants route (d), this is the claim to attack.
5. **Any in-game behaviour whatsoever.** Nothing here has been run. Static
   verification is not a test result.
