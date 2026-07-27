# Project knowledge

> Discoveries specific to THIS project, written down the moment they are made.
>
> Where things go: a rule that would help anyone modding EU5 → `EU5-MODDING-GUIDE.md`.
> An engine error signature → `EU5-ERROR-DECODER.md`. Everything else — a
> decision and its reasoning, a measurement, a constraint we hit — → here.
>
> Each entry: what is true, how it was established, and what it means for the
> work. An entry with no evidence line is a guess and should say so.

---

## Decisions taken before any code

### 1066, chosen over 1178 and 867 with the cost known
**Established:** by measuring all three against the engine, then choosing on the
setting. Superseded an earlier "1178 over 867" entry, which is kept below in
substance because its reasoning was sound and is why the cost here is accepted
rather than discovered later.

EU5 supports exactly ONE start date — a single `START_DATE`, a single
`setup/start/` tree, and `main_menu/common/scenarios/00_scenarios.txt` holds
country picks with no dates in it. No bookmark system was found. So this was a
one-way door, not a menu.

The engine cost is driven by one fact: `age_1_traditions` is `year = 1` and
`age_2_renaissance` is `year = 1342`, so everything before 1342 falls inside a
single age.

| Date | Years stuck in `age_1` | New ages needed |
|---|---|---|
| 1178 | 164 | 0 |
| **1066** | **276** | **>= 1** |
| 867 | 475 | >= 3 |

A new age is not cheap: `age_1` holds 613 advances, `age_2` 653, `age_3` 530, so
an added age means authoring roughly 400-600 of them or shipping a century with
nothing to research.

1178 was the cheapest date and remains the one the engine cooperates with; it
is 159 years from the shipped world, so most tags exist and it is roughly half
the data entry of 867. It was passed over anyway. 1066 buys an opening decade
1178 cannot match — Norman Conquest in the first months, Manzikert +5, First
Crusade +30 — and the Mongol arc still lands inside the campaign at 1206
(year 140 of 770), so the situation/state-machine work in the Mongol Resurgence
mod remains reusable with a shifted trigger year.
**Means:** the 276-year `age_1` is a known, accepted debt, not an oversight. It
is not being paid off before the game has been played, because nothing static
can say how much it actually hurts. See the open question below.

### 867 was tried once already
**Established:** `mod/867 Total Conversion Test Mod` — 4 commits, 35 `.txt`,
last substantive commit "ENG added with LocationPainter only".
**Means:** the cost estimate above is not theoretical for this author.

### Superseded: "regional depth first, not the whole map"
This entry used to say the first playable target was one region at full fidelity
with the rest left vanilla-ish. **That is no longer the project's scope** — the
target is the whole map, historically, and CLAUDE.md now carries the two-phase
plan that gets there.

The observation underneath it still holds and is why Phase 1 exists: one of the
two published conversions covers an era where most of the world is genuinely
stateless, so its empty map is historically honest. At 1066 the world is full,
so emptying it is not an option here. Phase 1 therefore keeps every country and
buys correctness at the level of *extent* first, leaving *identity* to Phase 2.
**Means:** do not gate a playable build on historical rulers. Do gate the claim
"this region is done" on them.

---

## How a total conversion is actually built

### The world comes from `main_menu/setup/start/`, not from the map
**Established:** two total conversions were read; neither ships any map data at
all — no `locations.png`, no `definitions.txt`, in one case no `map_data`
folder whatsoever. Vanilla's pipeline is 25 numbered files
(`02_core` … `27_armies`) and a mod overrides them.
A country is placed by listing **vanilla location names**:

```
countries = { countries = {
	NOR = { own_control_core = { bergen oslo nidaros stavanger … } }
} }
```

Anything no country claims stays empty.
**Means:** the map is not the hard part and does not need painting. Budget the
work as data entry against `setup/start`.

### `location_templates.txt` is an optional second layer
**Established:** it is a vanilla file — 28,573 lines, one per location, setting
`topography`, `vegetation`, `climate`, `religion`, `culture`, `raw_material`,
`natural_harbor_suitability`. One conversion overrides it wholesale, the other
does not touch it.
**Means:** skip it for v1 — locations keeping their 1337 culture and religion is
an acceptable first-release compromise. When it is done, remember it is a
whole-file override and must be re-merged on any patch that touches it.

### Defines live in `loading_screen/`, and CLAUDE.md said otherwise
**Established:** `loading_screen/common/defines/00_defines.txt:2-3`,
`START_DATE = "1337.4.1"` / `END_DATE = "1836.12.31"`, inside `NGame = { }`.
It is the ONLY defines tree vanilla ships — there is no `main_menu/common/defines`
at all, which is where CLAUDE.md and the modding guide both pointed until this
was checked. Corroborated independently by an external reference project's mod
layout (`docs/knowledge/BRIEF.md:79`).
**Means:** the original instruction would have produced a folder the engine
never reads, with no error anywhere. Both files are now corrected. This is the
canonical example of why paths get probed rather than assumed.

### Defines are mirrored to three trees, on split evidence
**Established:** vanilla keeps defines in `loading_screen` only, and so does a
published balance mod (SOL, both its deploy targets). The one published total
conversion that actually moves `START_DATE` writes the same `NGame` block to
`in_game/`, `loading_screen/` and `main_menu/`, with an in-file comment
instructing that they be kept mirrored.
**Since tested in a running game:** the date moved to 1066.9.15 correctly and
`debug.log` logged **no duplicate-define warning** — the only `defines.cpp:230`
lines name vanilla's own defines. So mirroring is at worst harmless.
**The wiki then contradicted the mirror**, and is explicit: *"To modify a
define, create a new file in `<mod>/loading_screen/common/defines/` that loads
after the base game files such as `01_mod_defines.txt`."* One tree. That now
makes three sources for `loading_screen` only — vanilla's own layout, a shipped
balance mod, and the wiki — against one conversion that mirrors.
**Means:** the two extra copies are very probably dead weight. Dropping them is
a change to something that currently works, so it wants its own commit and its
own launch: delete `in_game/` and `main_menu/` copies, drop the harness check's
`min_count` from 3 to 1, confirm the date still reads 1066 in the lobby.
The `zz_` prefix on the loading_screen copy is load order: vanilla's own
`00_defines.txt` sits in that folder and the override has to sort after it.

### A partial `NGame` block is enough
**Established:** a published conversion overrides `START_DATE`/`END_DATE` in a
four-line `NGame` block rather than copying vanilla's 2608-line file.
**Means:** never copy the whole defines file — that would turn every patch
touching any define into a merge.

### Ages do not move with the start date
**Established:** `in_game/common/age/00_default.txt`. Each age carries an
absolute `year`: `age_1_traditions` 1, `age_2_renaissance` 1342,
`age_3_discovery` 1437, `age_4_reformation` 1537, `age_5_absolutism` 1637,
`age_6_revolutions` 1737. A published conversion spanning 1329 internal years
retimed these six rather than adding any.
**Means:** moving `START_DATE` alone lengthens age 1 by exactly the distance
moved. Ages 2-6 stay put, which is why 1437+ keeps working untouched.

### Advances and institutions have no year gates
**Established:** across the 215 files in `in_game/common/advances/`, the number
containing a `year` field is **zero**; the only gate is `age = age_N_x`
(`0_age_of_traditions.txt:5`). Same for `in_game/common/institution/` — no year
or date match anywhere, two institutions per age.
**Means:** retiming an age silently retimes its entire advance tree, at no cost.
It also means a long age cannot be softened by staggering advances within it.

### Age keys cannot be renamed
**Established:** `age_1_traditions` is referenced in 352 files, `age_2_renaissance`
in 423 (a full sweep timed out; the magnitude is the point).
**Means:** only the `year` values are editable. A new age must be a NEW key
placed alongside them, never a rename.

### More than six ages should render
**Established:** the UI builds the age list from data, not fixed slots —
`in_game/gui/advances_lateralview.gui:787`, `datamodel = "[AdvancesLateralView.GetAges]"`,
with the same call at `societal_values_lateralview.gui:661` and
`technology_lateralview.gui:1847`. `Age` is a first-class script type
(`data_types_script.txt:134`), with `GetCurrentAge`, `IsCurrentAge`,
`IsFutureAge`, `GetAgeEndingDate`, `GetAgeIcon`.
**Not verified in a running game.** Two loose ends: `victory_card` runs 0-5 in
vanilla and index 6 is unattested (there is a `victory_cards_enabled` game rule,
so it can be switched off), and `GetAgeIcon` would want an icon for a seventh.
**Means:** a seventh age is probably legal. The real cost was never the engine,
it is the 400-600 advances it would want.

### `setup/start/` is date-agnostic
**Established:** none of the 25 files under `main_menu/setup/start/` contains
`START_DATE` or `1337.4.1`.
**Means:** the world data and the calendar are independent. Moving the date does
not invalidate setup work, and setup work can begin before the age question is
settled.

### `starting_technology_level` is the knob for an early start
**Established:** `main_menu/setup/start/10_countries.txt` carries 1133 of them —
915 at level 3, 79 at 0, 15 at 1, 1 at 2. `0_age_of_traditions.txt:1`:
"starting_technology_level is only relevant in age of traditions, where advances
with higher value than the countries value starts as unresearched."
**Means:** age 1's 613 advances are mostly pre-researched at 1337 by handing out
level 3. Starting in 1066 at level 0-1 turns that same tier into a real research
tree, which is part of why a long age 1 may prove more survivable than it looks.

### Vanilla content is gated on real years, and that survives an earlier start
**Established:** `situations/reformation.txt:5` `current_year >= 1510`,
`italian_wars.txt:10` `> 1495`, `council_of_trent.txt:8` `>= 1530`,
`little_ice_age.txt:6` `>= 1645`, `hundred_years_war.txt:8`
`current_date > 1337.5.1`, `nanbokuchou.txt:8` `> 1336.1.1`, plus
`on_action/_hardcoded.txt:33` `current_year < 1338` gating an AI cooldown.
**Means:** because we moved the start back and left the calendar aligned to real
years, every one of these still fires in its correct historical year. Shifting
the ages back instead would have stranded all of them.

### Country tags need not be three letters
**Established:** vanilla has 2217 tags and every one is exactly 3. A published
conversion ships 531 tags of which 471 are five letters and 47 are four, used
live in script (`c:ALASI`, `tag = ASYRI`).
**Not verified in a running game here.** Confirm before relying on it.
**Means:** if 3-letter uniqueness becomes painful across hundreds of new tags,
there is probably room. Test it early and cheaply rather than late.

---

---

## What an early start date does to `setup/start` (first in-game session)

### `ruler = ` sets the ruler; `ruler_term` is only regnal history
**Established:** vanilla's ENG block, `main_menu/setup/start/10_countries.txt`:
`government = { type = monarchy  heir_selection = cognatic_primogeniture
ruler = eng_edward_iii  ruler_term = { character = eng_alfred_the_great
start_date = 886.1.1 … } … }`. The wiki agrees: *"Government is also used to
define who ruled the country before the start of the game. It is used for
regnal history and to decide regnal numbers (Otto IV instead of Otto I)."*
**Means:** the ruler a country starts with is ONE line. Fixing rulers for 1066
is `ruler = <somebody alive in 1066>` per country — not a rewrite of the
ruler_term chains. An earlier reading of this session, that the engine "falls
back to the last ruler_term", was wrong and is recorded here so it is not
re-derived.

### At 1066 every country is ruled by its 1337 ruler, aged about -250
**Established:** in-game. England is ruled by Edward III, displayed as an infant
at roughly -247 years old. `eng_edward_iii` has `birth_date = 1312.11.13`
(`05_characters.txt:1224`), and 1066 - 1312 = -246.
**Means:** cosmetic it is not — see the death question below — but it is also
not a defines bug. It is `ruler = ` pointing at the wrong century, which is the
setup workstream, not the calendar.

### Future-dated setup entries collapse to `1.1.1`
**Established:** two signatures, both in `docs/EU5-ERROR-DECODER.md`.
`pdx_persistent_reader.cpp:289` rejects each out-of-range date — 3738 "Future
start date" plus 3147 "Future end date", 6885 in one load. The rejected term
then reports as `(start date: 1.1.1)` in `ruler_term_container.cpp:109`, and
several terms per country end up simultaneously active.
**Means:** unavoidable noise while vanilla's `10_countries.txt` is in play,
because removing entries needs a whole-file replacement (see below) and that
empties the map.

### Regency was NOT triggered — hypothesis tested and dead
**Established:** in-game observation. `ADULT_AGE = 16`
(`loading_screen/common/defines/00_defines.txt:1519`) made it look certain that
a -247-year-old ruler would be underage and put every country into regency.
The game shows no regency; the infant rulers rule directly.
**Means:** recorded so the next session does not spend the same hour on it. The
~30,000 `jomini_script_system.cpp:252` runtime errors remain undiagnosed and
regency is excluded as their cause.

### Rulers with negative age do not appear to die
**Established:** in-game, two months advanced, no deaths. **Weak evidence** —
two months proves very little. Needs 15-20 years at speed before it is a fact.
**Means:** if confirmed, succession, heirs and regency never fire until the
1320s, which would be a hard blocker rather than a cosmetic one.

### `setup/start` is additive, but same-name files replace wholesale
**Established:** the wiki, *"Most managers in the `setup/start` folder work in
an additive fashion… but makes it so that replacing entire files is required in
order to remove certain entries"*, and *"A file in vanilla or in previously read
mod can be entirely overridden by a file in the same directory and of the same
name"* — **"even if the mod's `00_default.txt` is empty."** Confirmed the hard
way in this project: overriding `10_countries.txt` by name emptied the map.
Corroborated by a published mod that ships
`main_menu/setup/start/sheep_turkomen_countries.txt`, a 47-line ADDITIVE file
which both adds a tag absent from vanilla (`AKK`) and redefines one that is
present (`QAR`, vanilla `10_countries.txt:34725`).
**Means:** additive files can carry country data. **Now measured by us**, in two
rounds against a running game:

| | Result |
|---|---|
| Does an additive file redefine a vanilla country? | **Yes** |
| Merge or replace? | **Merge** — England kept all 145 locations |
| Does `ruler = X` beat vanilla's own `ruler = `? | **Yes** — vanilla's `ruler = eng_edward_iii` was displaced |
| Does the named ruler then take the throne? | **No** |
| Does adding our own `ruler_term` fix that? | **No** |

Rounds 1 and 2 both ended with England under an engine-generated regent and no
ruler. The cause is in the decoder under `ruler_term_container.cpp:109`:
Harold's vanilla term is genuinely active on 1066.9.15, but the terms after it
are future-dated, get rejected, collapse to `1.1.1`, and remain in the list. The
container sees an active term with successors and seats nobody. Appending our
own term does not help, because the offending entries are still there.
**Means:** the ruler cannot be fixed while vanilla's `ruler_term` chain is
present, and removing entries requires a whole-file override. So
`10_countries.txt` gets overridden wholesale after all — the Bronze Era road,
which a sibling 867 project also arrived at independently. The additive
mechanism is still worth knowing: it is the right tool for anything ADDED rather
than removed.

### EU5 Location Painter covers the largest part of that override
**Established:** the tool at
`steamapps/workshop/content/3450310/3722312428/`, and its output visible in the
867 project. Its `templates/vanilla_control_core_location_painter_assignments.txt`
is vanilla's whole territorial layout in paintable form — its own header reads
*"Source: …/main_menu/setup/start/10_countries.txt"*, "Countries with
assignments: 1566", "Assigned unique locations: 13588". A second template
carries all 20897 ownable land locations against a `TMP` placeholder tag.
It writes `own_control_core`-style ownership lists, `06_pops.txt`, and a
`location_painter_countries_l_english.yml`.
**Means:** for a mod defined as a delta from 1337, the vanilla template is the
correct starting point — load it, edit only what differs in 1066, export. That
removes the most error-prone half of a wholesale `10_countries.txt`.
**What it does not touch:** `government` blocks, `ruler`, `ruler_term`,
characters, dynasties — which is exactly the blocker above. Territory is
painted; rulers are written by hand.
**Note:** `in_game/setup/location_painter/00_location_painter.txt`, which the
tool asks for, is a **tool working file**. Vanilla has no such path and the game
never reads it.

### `setup/start/` is a BOM-free zone, and it is the only one
**Established:** by counting bytes. Vanilla `main_menu/setup/start/`: 25 files,
**0 with a BOM**. A published conversion's: 25 files, 0 with a BOM. Everywhere
else sampled is the opposite — `advances` 215/215, `setup/templates` 198/205,
`situations` 23/23, `on_action` 21/21, `defines` 1/1, `age` 1/1.
Then confirmed from our own log: our probe file, written with a BOM because
CLAUDE.md said `.txt` takes one, produced
`pdx_persistent_reader.cpp:289: Error: "Unexpected token: ﻿" in file:
"setup/start/50_1066_rulers.txt"` and was never parsed. A sibling 867 project hit
the identical thing on `07_cities_and_buildings.txt` and it **crashed the game**
during new-game load.
**Means:** CLAUDE.md's "UTF-8 with BOM for `.txt`" was wrong without an
exception, and the harness enforced the wrong version — it demanded the byte
that breaks the file. Both are fixed, and `verify_mod.py` now checks both
directions, each proven by breaking it.
**And it cost a false conclusion.** The probe appeared to show that additive
setup files cannot redefine a vanilla country. It showed nothing of the kind;
the file never reached the parser. That question is still open.

### Repeated keys merge — within a file, at least
**Established:** 175 of vanilla's 2337 country blocks declare
`government = { … }` twice. QAR is one: the first declaration carries `type`,
`heir_selection`, `ruler` and `laws`, the second carries only
`mysticism_vs_jurisprudence = -15`. A replacing second block would strip QAR of
its government type and ruler, and vanilla ships it.
**Means:** repeated keys merge inside a file. Whether the merge crosses file
boundaries — our additive file against vanilla's `10_countries.txt` — is the
open question, and is what the probe measures.
**Correction:** an earlier entry in this file argued merging from a published
mod redefining QAR without a location list. That argument was void — vanilla's
QAR has no `own_control_core` at all, only `our_cores_conquered_by_others`, so
it is a landless claimant tag and its redefinition says nothing about whether
territory survives. Recorded because the wrong version was nearly built on.

### Vanilla already ships the 11th century
**Established:** `05_characters.txt` holds 7236 dated characters — 330 born
1000-1070, of whom 188 would be aged 16-56 in 1066. England's regnal chain runs
back to `eng_alfred_the_great start_date = 886.1.1`.
**Means:** rulers for a focus region are mostly a matter of pointing `ruler = `
at character keys that already exist, not of authoring characters.

### How a published conversion sidesteps all of this
**Established:** Bronze Era ships `10_countries.txt` with **zero** `ruler_term`
entries and `government = { ruler = random }`, plus a 2.5 KB `05_characters.txt`
against vanilla's enormous one. Its file also opens with `current_age =
age_1_traditions`, so the starting age can be stated in setup.
**Means:** `ruler = random` is the cheap global answer for everything outside
the focus region. It costs all historical flavour, which is why it is a
baseline and not the plan.

### Two setup ordering rules that cause crashes, not errors
**Established:** the wiki — *"Dynasties used by characters in `character_db`
need to be created in `dynasty_manager` first"*. Bronze Era's characters file
opens with *"Remember to write sons and daughters ALWAYS after their parents to
avoid crashes."*
**Means:** order is load-bearing in setup files. Dynasties before characters,
parents before children.

### Birth dates may be negative even when `START_DATE` is not
**Established:** Bronze Era runs `START_DATE = "1.1.1"` and still writes
`birth_date = -54.1.1`.
**Means:** the positive-calendar rule constrains the game clock, not character
birth dates.

### Decision: `10_countries.txt` is left alone for now
**Taken** after the two probe rounds, with the costs measured:

| Route | Cost | World outside the focus region |
|---|---|---|
| Copy vanilla and edit | 62,966 lines adopted, re-merged on patches | intact |
| Region only (Bronze Era / 867) | 425 lines for 7 countries, 12,596 for 383 | **empty** |
| **Leave it (chosen)** | **0 lines** | intact, ruled by -247 year olds |

The deciding observation is that the regency was **self-inflicted**. Untouched
countries keep a working ruler — an absurdly aged one, but a ruler. England
lost its throne only because our probe displaced `ruler = eng_edward_iii` with a
name the container then refused to seat. Reverting the probe restores England to
the same broken-but-functional state as everywhere else.
**Means:** no country data is written until the focus region is chosen, because
the choice between the two override shapes IS the choice of how much world
survives, and it should be made with a region in hand rather than in the
abstract. Until then the world stays full, the rulers stay wrong, and the 6885
future-date lines stay in the log.
**Also means** CLAUDE.md's "one region deep, the rest vanilla-ish" is still
intact — but it is now known that the region-only route would break it, and
that is a decision to take deliberately rather than discover.

### Phase 1 works — measured in game
**Established:** first launch after `tools/build_setup.py` ran. All four defects
of the 1066 start are gone: rulers are random and sanely aged instead of about
-250; the world is still full with every country in place; the 6885 future-date
errors are gone from `10_countries.txt`; and the **~30,000-line script error
flood stopped completely**, which closes the `jomini_script_system.cpp:252`
signature in the decoder — it was downstream of the broken ruler data all along.
**Means:** the phased plan holds. A 1066 world that runs is one generated file
away from vanilla, and history can now be added incrementally to something that
already works.

### The same defect lives in `15_international_organizations.txt`
**Established:** the ~300 errors left after the first pass all came from that
one file — 93 `ruler_term` blocks carrying the Holy Roman Emperors from
`ogk_heinrich_iii_salier` (1046) onward and the Papal line, in exactly the same
shape as countries, producing the same `1.1.1` collapse.
**Safe to strip, unlike a country's:** an IO's head is `leader = <TAG>` — a
country, not a character (`leader = UBV` for the HRE, `leader = PAP`). Removing
the terms cannot leave it headless the way it left England.
**Means:** `build_setup.py` now generates both files, and asserts the IO leader
count is unchanged.

### Phase 1 is generated, not hand-maintained
**Established:** `tools/build_setup.py` reads vanilla's 62,966-line
`10_countries.txt` and writes ours. Per run it removes 3852 `ruler_term` blocks,
5 `timed_modifier` blocks, and 174 character/regency lines
(43 `heir`, 39 `consort`, 28 `active_regent`, 28 `regency`, 28+28 regency dates,
6 `designated_heir_reason`, 2 `inherit_ruler_terms`); rewrites 861
`ruler = <name>` to `random`, leaves 1360 that were already random, and adds 116
where a country had none — 21 of which needed a `government` block created.
861 + 1360 + 116 = **2337, exactly the country count**, and the script refuses
to write unless every country has exactly one ruler, the block count is
unchanged, braces balance, and no date survives anywhere.
**Means:** the 63k-line file is never hand-edited or hand-merged. After a game
patch, re-run it. Phase 2 adds real rulers through the `HISTORICAL_RULERS` table
in the same script, so historical work layers on top of a regenerable base
instead of replacing it.

### Two bugs the generator caught, both of the silent kind
**Established:** while building it.
1. **Trailing comments.** 17 of vanilla's `ruler =` lines end in a comment, and
   4 of those name a real character (`hnv_jamal_ud_din_honnavara`,
   `gen_galeotto_spinola`, `msp_morello_iii_malaspina`,
   `nur_rappold_von_kulsheim`). A regex expecting a newline skipped them, and
   those 4 countries would have kept a 1337 ruler with nothing to show for it.
2. **Per-block vs per-country.** Adding a missing ruler per `government` block
   put a second `ruler = random` in each of the 175 countries that declare
   `government = { … }` twice. Invisible in Phase 1 — everything is random —
   but it would have silently outranked the first historical ruler Phase 2 set.
**Means:** both are now assertions in the script, so neither can come back. This
is the same lesson as the harness: the check goes in next to the fix.

### Known wrong in the Phase 1 output, deliberately
**Established:** by reading the generated file.
- `regnal_numbers` survive and are calibrated for 1337 — England carries
  `name_edward = 3`, `name_william = 2`. Cosmetic, no errors.
- Country content generally is still 1337's: England starts with
  `magna_carta_reform`, which is 1215.
**Means:** Phase 1 buys a world that is correct in *extent* and *works*. It does
not claim historical accuracy — that is exactly what Phase 2 is for, and these
are on its list.

### Vanilla contradicts the "children after parents" rule 614 times
**Established:** vanilla's own `05_characters.txt` opens with *"Remember to write
sons and daughters ALWAYS after their parents to avoid crashes"*, and a published
conversion repeats the warning. Counting the file: **614 characters name a parent
that is declared later**, and the game runs. Vanilla also ships **8 dangling
parent references** (`yem_al_muzaffar_yusuf_i`, `wls_goronwy_ap_tudur_hen`,
`sav_humbert_i_savoy`, `dhf_al_faiz`) and one `father = random`, which is a legal
value rather than a broken name.
**Means:** the ordering rule as stated is not enforced by the engine. It is not
dismissed — it may hold in some narrower case nobody has pinned down — so
`build_setup.py` keeps OUR additions ordered while refusing to fail the build on
Paradox's data. The general lesson: **validate what we wrote strictly, report
what vanilla shipped.** A check that fails on vanilla's own quirks blocks work
over someone else's bug.

### Name keys are not free-form — `name_harald` does not exist
**Established:** name keys live in `in_game/common/languages/`. The Scandinavian
pool (`00_scandinavia.txt`) has `name_harold` (line 14), `name_magnus` (18),
`name_olaf` (20), `name_sven` (22), `name_sigurd` (235). There is **no
`name_harald` anywhere in the game** — vanilla uses one key for Harald/Harold,
which is why `eng_harold_godwinson` carries `name_harold`.
**Means:** writing `first_name = { name = name_harald }` would have produced a
character with no name and no error. Every `name_*` goes through
`in_game/common/languages/` before it is written.

### First Phase 2 slice: North Sea 1066
**Established:** generated and validated; not yet observed in game.
`HISTORICAL_RULERS` now carries five entries — `ENG` Harold Godwinson, `NRM`
William of Normandy, `DAN` Sweyn Estridsson, `SCO` Malcolm III, `NOR` Harald
Hardrada. Four came free from vanilla; only Norway needed authoring, because no
`nor_` character is alive in 1066. `fairhair_dynasty` already exists in vanilla
(`home = haugalandet`), so no `dynasty_manager` change was needed.
Territory checked before writing: ENG 145 locations/london, NOR 119/oslo,
DAN 49/roskilde, SCO 27/dunfermline, NRM 21/rouen and `rank_duchy` — all correct
for 1066.
**Two deaths are scheduled by the data itself:** Hardrada on 1066.9.25 at
Stamford Bridge, ten days in, and Harold on 1066.10.14 at Hastings, one month in.
Both are vanilla's own `death_date`s. Magnus II and Olaf III Kyrre were written
as Hardrada's sons so Norway's succession has something real to land on.
**Means:** the opening month plays itself before a single situation is written.
What that produces — who inherits, whether the claims materialise — is the next
thing to observe.

## Open questions to settle early

- **How badly does a 276-year `age_1` actually play?** THE question for this
  project, and unanswerable without playing. Watch: research pace with
  `efficiency = 1.0` (no age discount), `expected_navy_size_modifier = -0.8` for
  the whole stretch, `max_price = 3`, and no hegemons until 1437. Mitigation
  available before any age surgery: drop `starting_technology_level` so the 613
  age-1 advances become a real tree. Only if that is not enough does a seventh
  age get designed — and it is designed from what hurt, not from a guess.
- **Does the engine read `START_DATE` from all three defines trees?** We mirror
  because the evidence is split. First launch answers it.
- **Database operation prefixes — largely answered.** Measured across 20
  workshop mods in the reference project: 599 `REPLACE:`, 295 `TRY_INJECT:`,
  190 `INJECT:`, 116 `TRY_REPLACE:`. Multiple shipped mods rely on them, so they
  work. Every single use is under `in_game/common/…` — advances, prices, laws,
  generic_actions, static_modifiers. **Zero uses anywhere under `setup/`**, so
  they are not the answer for country data; a new filename in `setup/start/` is
  (see the setup section above). Still untested by us in our own files.
- **`replace_paths`** in `metadata.json` → `game_custom_data` declares vanilla
  paths to ignore entirely. Present but empty in a published conversion. For a
  conversion this is how you drop vanilla countries wholesale.
- **`@icon_name!` inline icons** from `main_menu/gui/shared/font_icons.gui`
  (364 named icons) — cheaper than an icon widget, never used by us.

---

## Reference trees available outside this repo

All read-only. Detect by probing a known file, never a directory.

| Path | What it is | Good for |
|---|---|---|
| `E:\SteamLibrary\...\Europa Universalis V\game` | vanilla 1.3.11 | the authority for everything |
| `mod/Mongol Resurgence` | own railroad mod | situation/state-machine/failsafe shapes, a mature harness, a nine-session test log |
| `C:\Users\Desktop\Bronze Era Modu Total Overhaul` | published conversion | `setup/start`, `location_templates`, the only attested `START_DATE` move |
| `C:\Users\Desktop\eu5-modding-project-1.3.11\...` | SOL balance mod project, 11631 files | `reference_official_defines/types/` (14 official type files), `reference_mods/` (20 workshop mods), a full 1.3.11 game copy |
| `docs/*.pdf` (in this repo) | 34 wiki pages saved 2026-07-20 | offline copies of Setup / Country / Character / Event / Situation / Localization / Mod structure modding and more |

The wiki PDFs are read with `pdftotext -layout "<file>.pdf" -` — the Read tool
cannot render them here (no poppler for page images), but `pdftotext` is on PATH
and gives the full text including code blocks. Section-scope it with awk rather
than dumping 19 pages.

**The wiki is a source, not the authority.** It carries a banner —
*"At least some were last verified for version pre-release"* — and its Country
modding page is visibly thinner than the game. Where it and
`docs/EU5-Vanilla-Script-Docs/` disagree, the script docs win. Where it and
vanilla source disagree, vanilla wins.

The 1.3.11 game copy in that last tree was diffed against the installed game:
`in_game/common/age/00_default.txt` is byte-identical and `00_defines.txt` opens
identically. Citations taken so far are version-current.

## Carried over, still to do

- **Raise the harness `min_count`s** as each kind of content first appears. The
  rule is in `CLAUDE.md`; this is the reminder that it applies from the very
  first `.txt` file, because until then every check reports `SKIP`.
- **Install CWTools** (`tboby.cwtools-vscode`) — a Paradox script language
  server that catches syntax and reference errors in the editor, before the
  harness and long before the game.

## Template for new entries

```
### <short claim>
**Established:** how — a file:line, a measurement, an in-game observation.
**Means:** what changes because of it.
```
