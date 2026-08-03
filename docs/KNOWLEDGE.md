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
**Fourth source (2026-07-28):** Anno 1644 — the second published conversion
that moves `START_DATE` (forward, to `1644.4.17`) — ships its defines in
`loading_screen/common/defines/zzz_1644_defines.txt` ONLY; no `in_game/` or
`main_menu/` copy exists anywhere in the mod. Four sources for one tree,
one for the mirror.

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
character with no name and no error.
**REFINED (2026-07-28, France research pass, verified):** the language pools
are only the RANDOM-GENERATION namespace. For a scripted
`first_name = { name = X }` the authority is the loc file
`main_menu/localization/english/character_names_dynamic_l_english.yml` —
vanilla's own `vnt_ebles_i_de_ventadour` (05_characters.txt:29169) uses
`name_eblo`, which exists in NO language pool but sits in that loc file at
line 6044. The scripted-name check is therefore: does the key exist in the
character-names loc — a much larger namespace than the pools. `name_harald`
exists in neither, so the original lesson stands.
**REFINED AGAIN (Persia pass, verified):** the registry is TWO files —
LITERAL names resolve from `character_names_l_english.yml` (vanilla's own
`Tashfin:4383`, `Ibrahim:1364`, and `Alp_Arslan:12559 → "Alp Arslan"`,
which also settles underscore→space as OBSERVED). A literal without a row
in either registry or our own loc renders nothing — measured on our own
`Tamim`, caught by the authored-identifiers harness check on its first
run and fixed by adding the loc key. Check BOTH files plus ours.

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
**SUPERSEDED on the deaths:** measured in game, a post-start `death_date`
starts the character DEAD (see the death_date law below). Both dates are now
stripped like every other future death; the opening month does NOT play
itself, and Stamford Bridge and Hastings belong to the Norman Conquest
situation. The sons and the succession reasoning stand.

### A named ruler does not seat without an open `ruler_term` — measured in game
**Established:** in-game test of the first Phase 2 slice (2026-07-28). All five
`HISTORICAL_RULERS` countries — ENG, NRM, DAN, SCO, NOR — started under
engine-generated regents, while every `ruler = random` country seated normally
(Sweden: a generated 31-year-old king). The character side was ruled out
byte by byte: our `05_characters.txt` blocks are identical to vanilla's, all
three generated files are BOM-free, all seven character keys present. The one
thing those five countries lacked was a `ruler_term` — `build_setup.py` strips
them all. Corroborated three ways:
1. **Anno 1644, the working conversion at a moved date, writes BOTH lines for
   every named ruler** — `ruler = X` plus an OPEN (no `end_date`) past-dated
   term: `ruler_term = { character = hol_frederik_hendrik_van_oranje
   start_date = 1644.1.1 regnal_number = 1 }` (`10_zzz_w_countries.txt:41`),
   `ruler_term = { character = jap_tokugawa_iemitsu start_date = 1623.1.1 }`
   (`10_countries.txt`, Japan block). ~209 named rulers, 231 `ruler_term`s.
2. **Vanilla:** 650 of 863 named rulers carry a matching
   `ruler_term = { character = <same key> … }` in the same block. Of the 213
   without, the visible cases are cross-tag rulers (WLS with
   `ruler = eng_edward_iii` and NO term), tribes and theocracies. Whether
   the remainder actually seat at 1337 is unmeasured — do not cite them as
   counter-examples without testing one.
   **CORRECTED by the Celtic pass:** the original version of this entry
   attributed WLS to `inherit_ruler_terms` — wrong; that key occurs
   exactly twice in the whole file and both read `= YMT` (Japan),
   re-verified by hand. WLS is simply an unmatched named ruler.
3. **Our two earlier probe rounds** (England regent despite `ruler =` while
   vanilla's poisoned term chain was present) now read as the same law from
   the other side: seating goes through the term container. A poisoned chain
   fails it one way, an absent chain the other.
**Means:** `ruler =` alone is advisory; the wiki's "regnal history and regnal
numbers" description undersells `ruler_term`. `build_setup.py` must emit, for
each `HISTORICAL_RULERS` entry, an open `ruler_term = { character = X
start_date = <accession date, before START_DATE> }`, and its "no date
survives" assertions must be narrowed to "no FUTURE date survives".

### The date audit was blind to one-line blocks, and Phase 1 shipped five dates through it
**Established:** while adding the ruler_term emission (2026-07-28). The old
"no date survives" check was line-anchored; vanilla writes one-line blocks
with dates mid-line, so the check passed while five live `date =` fields
survived every Phase 1 build: BYZ bureaucracy entries dated 680.6.1, 330.5.11,
500.6.1, 892.6.1 (past at 1066 — parse fine) and TRE
`themata_bureaucracy date = 1204.4.1`, which IS future at a 1066 start.
Vanilla also ships 60 commented-out ruler_terms in `10_countries.txt`, which
the first non-anchored audit draft duly flagged — audits must run on
comment-stripped text, matching what the parser sees.
**Means:** both builders now audit non-anchored, comment-stripped text. TRE's
1204.4.1 is a DOCUMENTED exemption (`KNOWN_FUTURE` in `build_setup.py`) — the
world was measured clean with it aboard, so it is deferred to the
Byzantium/Anatolia slice rather than blindly stripped. Possibly related to the
4 unexplained `gamestate.cpp:133` "Failed to read key reference" lines —
unverified, noted for whoever investigates those.

### A character alive at start must carry NO death_date — measured, with screenshots
**Established:** in-game 2026-07-28, second test of the Phase 2 slice. The
open ruler_term DID seat Harold — Ruling History shows "King Harold II
Godwinson", crowned 6 January 1066, regnal number correct — but his reign
closed ON the start date ("King of England from 6 January, 1066 to
15 September, 1066"), skull icon, "His Late Majesty", and England fell to a
generated regent. Norway and Denmark identical. Sweyn's death_date is
1076.4.28 — ten YEARS out — and he still started dead, which rules out "the
death fired early" and leaves the known future-date rejection: a death_date
at or after START_DATE is invalid and the character begins the game dead.
**Completely silent** — zero error.log lines; the log actually shrank
(17,954 → 1,054) while all five thrones were broken.
Vanilla's convention, measured: **4,304 of its 4,305 death_dates are past at
1337**, and `eng_edward_iii` (historically dies 1377) carries NONE — living
characters' deaths are simulated, not scripted. The lone exception
(`cas_pedro_fernandez_castro`, 1342.1.1) is vanilla's own slip and
presumably starts dead in vanilla too, unnoticed. At a 1066 start, 3,762
vanilla death_dates are future, and **260 belong to characters alive in
1066** — the entire period cast was starting dead.
**Means:** `build_setup.py` strips every `death_date >= START_DATE`
(3,762 lines; 546 past deaths stay), with a line-anchored strip, a
non-anchored comment-stripped backstop proven by a one-line-block canary,
and a harness check proven by breaking. Scheduled historical deaths
(Stamford Bridge 25 Sep, Hastings 14 Oct) are SCRIPT work — the Norman
Conquest situation's job — never data. The previous entry's law stands
confirmed: `ruler` + open `ruler_term` seats the ruler; it was the death
date that emptied the throne again.
**SCOPED the hard way (test 3, same day):** stripping ALL 3,762 future
death_dates put the five kings on their thrones — both laws confirmed
working — and then the game **hard-froze on the first unpause**: debug.log
cut mid-word inside `CPauseGame::InternalExecute`, no script flood, no crash.
The tell: init logged 21 × "has no birth scripted" including FUTURE-BORN
`sco_william_the_lion` (b. 1143) — the ~3,500 future-born characters, their
births collapsing and their deaths now gone, were being instantiated as
ancient living characters. Test 1-2 ran fine with them dead. So the strip is
scoped to characters BORN BEFORE `START_DATE` — exactly 260, matching the
independent count of alive-in-1066 characters — and the future-born keep
their vanilla death_dates. **Confirmed in game (test 4):** freeze gone, game
runs for months, five kings alive and ruling, error.log at 53 lines, nobody
dies on their own. All three laws of this day are now measured, not inferred.
**Also found:** vanilla ships two malformed partial dates
(`birth_date = 1010.1.` "# unknown", lines 228 and 240) — date parsing in
tools must be tolerant, pad missing parts, never crash on vanilla's data.

### Vanilla DHE flavor already covers the late end of the 1066–1337 gap
**Established:** in-game observation (2026-07-28), browsing England's event
list: vanilla DHE events for the houses of Lancaster and York are visible with
trigger windows in the 1300s. `flavor_ENG.txt` is dense with dynasty-driven,
date-gated events (`dynasty:lancaster_dynasty` from line 4426 on).
**Means:** the 1066–1337 gap is not uniformly empty — the decades nearest 1337
already have vanilla flavor that fires correctly because the calendar stays
real-year aligned. Prioritise the situation backlog toward the EARLY end
(1066–1200), where vanilla truly has nothing.

### Norman Conquest situation — the mechanisms, verified before design
**Established:** 2026-07-28, against the script docs and vanilla source.
- `kill_character` / `kill_character_silently` — any scope, character target,
  optional `location`, `killer`, `reason`, `disease` (`effects.log:3554/3559`).
- `set_as_designated_heir` — country scope, character target
  (`effects.log:10040`). Succession need not rely on `father =` links alone.
- `add_casus_belli` — country scope, `{ target type [character] [years] }`
  (`effects.log:75`); `declare_war_with_cb` — country scope,
  `{ target = <country> type = <cb_type> }` (`effects.log:1391`).
- The attested war-start idiom, guards included:
  `events/situations/hundred_years_war.txt:243-258` — `leave_all_wars_with`,
  a `can_declare_legal_war_on` gate, `declare_war_with_cb`, and
  `add_casus_belli` as the else-branch. Situations define their own CB types
  (`casus_belli:cb_hundred_years_war`).
- Situation events live in `in_game/events/situations/<name>.txt` (23 files).
- Seeding at game start: `main_menu/setup/start/22_situations.txt`,
  `situation_manager = { <key> = { status=active } }` — vanilla's file is 47
  lines, nearly all commented-out examples. Whether an ADDITIVE file merges
  into `situation_manager` is UNTESTED.
- Wars in progress at start exist as a mechanism: `16_wars.txt`,
  `war_manager` blocks with PAST `start_date` (`1332.7.6` at a 1337 start),
  attacker/defender/request/caller shape. NOT chosen for the conquest — the
  situation declares its wars from events, one mechanism instead of two.
  Open question parked: what becomes of vanilla's ~219 future-dated 1337
  wars at a 1066 start is unmeasured.
- Exact-day timing inside a monthly-ticking situation: delayed events
  (`trigger_event = { id = X days = N }` family) scheduled from `on_start` —
  the delayed block form is attested vanilla-wide (812 events fired only
  that way).
**Means:** exact-date deaths, controlled succession, player-choice
railroading and a scripted invasion war are all buildable from attested
constructs. Genuinely new ground: a custom `cb_norman_conquest` type (check
vanilla's CB list for a reusable throne-war CB first), and the 22_situations
additive-merge question.

### The on_game_start on_action route did NOTHING — situations own their lifecycle
**Established:** in game 2026-07-28, first launch of the Norman Conquest
build. Its timeline hung off an additive
`on_game_start = { on_actions = { … } }` file; in game nothing fired — no
intro events, no wars, no scheduled deaths — while the situation itself
spawned normally on the first monthly tick (1 October). The cause was not
isolated (candidates: the cross-file merge of the `on_actions` list, three
files now touching `on_game_start`; or the scope-less `c:X` links in the
effect).
**UPDATED (2026-07-29, the event-system pass): the MERGE candidate is
ELIMINATED** — vanilla itself declares `on_game_start` in TWO files
(_hardcoded.txt:1 behind a BOM + ai_personalities_setup.txt:9) and
both run; cross-file on_action merging is real. The new lead
candidate (attested by three framework mods): **on_game_start fires
BEFORE country selection**, so anything player-scoped or
selection-dependent cannot work there. The architectural answer
(situations own their lifecycle) stands regardless. The architectural answer was already paid for in our own Mongol
Resurgence mod — its on_action file header records the same lesson
verbatim: hand-firing phase events from on_actions produced its dangling
trigger_event bugs, and it moved to *"the situations own their own
lifecycle"* (can_start opens, on_start/on_monthly drive, can_end closes).
**Means:** the timeline lives in the situation's own `on_start`, scheduling
per-country delayed events via `c:X ?= { trigger_event_non_silently =
{ id days } }` — hundred_years_war's attested on_start shape. Offsets
anchor to the OBSERVED start of 1 October: +13 = Hastings 14 Oct, +85 =
coronation 25 Dec. Check the reference mods for the lesson BEFORE building,
not after — the user had to point at MR.

### Every situation needs its own GUI panel file, or the panel is empty
**Established:** in game — the situation opened with an EMPTY panel and
hovering it flooded the log with `No context supplied (Use SetDataContext)`
errors from vanilla's shared tooltip guis. The requirement is written in
vanilla's own `in_game/gui/panels/situation/readme.txt`: a file named after
the situation, `type situation_panel`, based on an existing one. Mongol
Resurgence ships a proven 45-line minimal template
(`mr_torghut_migration.gui`) — one END_REQUIREMENTS card reading
`SituationView.GetActiveSituation.GetSituation.GetEndConditions`.
**Means:** `norman_conquest.gui` is that template with the mod-specific
hint reference emptied. Any future situation lands WITH its `.gui` in the
same commit. `.gui` files carry NO BOM.

### CWTools flags `GetCountry` in situation `_info` loc keys — false positive
**Established:** CW266 "uses command GetCountry which does not exist in data
type None" on `norman_conquest_info`, while vanilla's own
`hundred_years_war_info` (`situations_l_english.yml:358`) uses the identical
`[GetCountry('ENG').GetName]` construct.
**Means:** vanilla-attested; ignore this CWTools diagnostic for `_info` keys.

### Round 2 of the situation: subjects cannot declare war, and 1337's appanages came along
**Established:** in game 2026-07-28 (second situation round) plus source.
The situation started cleanly (1 Oct), the GUI showed, the trigger-less
intro event fired — and nothing else happened: no wars, no deaths. Two
findings underneath:
1. **NRM is France's APPANAGE in vanilla's `12_diplomacy.txt:167`**, carried
   into our start untouched. A subject cannot freely declare war —
   `can_declare_legal_war_on` fails and the event's else-branch granted an
   invisible CB and stopped. The engine had been saying so all along:
   the "Subject type 'appanage' is invalid at game start" class (~25 of the
   53-line baseline) names exactly these ten French appanage dependencies,
   all requiring a Capetian dynastic link no 1066 ruler has.
   `build_setup.py` now generates `12_diplomacy.txt` stripping exactly
   those ten; 637 other dependencies untouched. Historically right too —
   the 1066 great fiefs were de facto independent.
2. **Every event that carried an event-level `trigger` went silent while
   the trigger-less one fired.** Not yet isolated from finding 1 (the war
   gates in those triggers were genuinely false). HYPOTHESIS, not law.
   The build now avoids the whole class: no event-level triggers; guards
   sit inside options as if/limit, so a false guard skips an effect
   instead of swallowing the event; and the two declarations also RETRY
   from the situation's `on_monthly` while their historical window is
   open (HYW's own architecture), `is_ai`-gated so a player's refusal
   sticks.
   **RESOLVED (2026-07-29, the event-system pass — docs/EVENT-SYSTEM.md):
   the hypothesis is FALSE as stated; the mechanic under it is LAW.**
   `trigger_event_*` DOES evaluate the target's trigger on every route
   (vanilla's own readme documents `on_trigger_fail` for exactly this;
   delayed fires evaluate TWICE). Round 2's triggers were simply false
   — findings 1 and 2 were ONE finding. The corrected rule: flavor
   events SHOULD carry triggers (95% of vanilla DHEs do); RAILROAD
   beats still must not (guards in options) — narrowed, not deleted.
**Also learned:** the engine auto-generates wargoal loc keys and prints
them into error.log — `war_goal_<key>` and `war_goal_<key>_desc`
(`localization_util.cpp:103`). That log line IS the naming convention,
straight from the engine; both pairs are now defined.
**Means:** round 3 discriminates cleanly: deaths now happen regardless of
war state (the railroad is history, war is flavour), so if kings die but
wars still fail, the legality chain is the remaining suspect — and if
everything fires, the event-trigger hypothesis is confirmed as the round-2
culprit alongside the appanage block.

### Round 3: the machine works — and a war declaration needs the CB in hand FIRST
**Established:** in game 2026-07-28, third situation round. Everything core
fired: Hardrada died and Magnus II succeeded, the Hastings event killed
Harold on 14 October, and ON 25 December the coronation event built the
England–Normandy union with William ruling both. The two war declarations
lagged: Normandy declared only on 1 November, Norway never did — but
Norway HELD the "Invade England" casus belli (visible in the diplomacy
panel, ten-year duration). That pattern decodes the mechanism:
`can_declare_legal_war_on` is a SCRIPTED trigger
(`country_triggers.txt:1198`) wrapping the engine's `can_declare_war_on`,
and the separate existence of `can_declare_no_cb_war_on` shows a normal
declaration requires a casus belli ALREADY HELD. Our events granted the CB
only in the else-branch after the check failed — so every attempt cost one
monthly-retry cycle, and Norway's window closed with Hardrada's death.
**Means:** grant the CB BEFORE checking legality — the situation's on_start
now hands both CBs out at start, and events plus monthly retries go
CB-first. Also measured: `add_casus_belli` without a duration shows a
ten-year expiry in game; the monthly retry architecture works (Normandy's
1 November declaration WAS the retry).
**Cosmetic debts noted for the polish pass:** William displays as
"William III" (ENG's regnal_numbers are 1337-calibrated — the documented
KNOWN WRONG); England between Hastings and the coronation sits under a
generated regency (historically Edgar Ætheling, who vanilla does not ship).

### Round 4: CB-in-hand at day 0 STILL does not unlock the declaration
**Established:** in game 2026-07-28, fourth round. With both CBs granted in
the situation's on_start, Normandy again declared only on 1 November — the
first monthly retry — and again only after Hastings. So on day 0 something
OTHER than the casus belli fails inside the engine's `can_declare_war_on`,
and it passes by the next month. Two candidates, indistinguishable with
monthly retries (the next attempt after day 0 IS 1 November): a CB whose
registration only lands on a later tick, or a game-start declaration lock
(no such define was found; would be hardcoded).
**Means:** a ladder of HIDDEN retry events at +1, +2, +3, +5, +8, +13 days
converges on the earliest legal day whatever the mechanism is. The hidden
machinery-event shape is attested verbatim in vanilla:
`events/ai_area_conqest_events/hidden_events_for_ai_conquest.txt` —
`type = country_event`, `title/desc = empty_text`, `hidden = yes`, effects
in `immediate`. Stamford moved to +3 so Norway's declaration window (+1,
+2) comes BEFORE Hardrada's death — the historical order. Whichever rung
of the ladder fires in round 5 measures the actual lock length.

### Round 5: the declaration lock is real — ship opening wars in the SETUP
**Established:** in game 2026-07-28, fifth round. With the CB in hand from
on_start AND hidden retries on days +1, +2, +3, +5, +8 and +13, Normandy's
declaration STILL only succeeded on 1 November, the first monthly tick of
the next month, for the third round running. Every scripted attempt
through 14 October fails; ~45 days after START_DATE it works. No defines
constant matches (searched); the lock is engine-side.
**Means:** wars that must exist in the opening weeks are not DECLARED,
they are SHIPPED — `16_wars.txt`, the mechanism vanilla uses for 219 wars
of its own. `build_setup.py` now generates it: all 13 vanilla blocks are
future-dated at 1066 (earliest start 1283.1.1 — the same poison class as
the ruler_terms) and are stripped; the two 1066 wars go in with past
start dates (Norway 1066.9.8, the Fulford campaign; Normandy 1066.1.6,
the quarrel dated from Harold's crowning). Superiority goal binding
attested at `16_wars.txt:270`. The declaration events, hidden pulses and
monthly retries remain as guarded no-ops and alt-history failsafes — with
one edge caught by review, not by testing: after force_union the NRM
retry would have re-declared on its own union partner, so those guards
now carry `NOT = { in_union_with = c:ENG }`.
**Also from this round's screenshots-by-eye:** the player-England submit
option in .42 lacked `historical_option = yes` while the other historical
paths had it — the marker matters to players running the historical-AI
game rule. Fixed.

### The situation flavour stack, located piece by piece
**Established:** while building the Norman Conquest polish pass, all cited.
- Situation map colors are NAMED COLORS: `map_ENG = hsv360 { 2 80 95 }` in
  `main_menu/common/named_colors/02_map.txt:15`, referenced bare
  (`value = map_ENG`) from situation map_color blocks. New sides = new
  named colors in an additive file with the `colors = { }` wrapper.
- Situation "impact" modifiers are nearly markers: vanilla's
  `hundred_years_war_impact` (static_modifiers/country.txt:6466) is only
  `blocks_country_formation = yes` — which is a static-modifier FIELD, not
  a modifier tag; the harness skiplist knows.
- Opinion walls are biases: `opinion_hyw_enemies = { value = -1000 }`
  (biases/01_opinion_scripted_diplomacy.txt:544), applied/removed with
  `add/remove_opinion_mutual_effect` in the situation lifecycle.
- Static modifier loc: `STATIC_MODIFIER_NAME_<key>` / `_DESC_<key>`.
**Means:** the flavour layer of any future situation is four small additive
files and a handful of lifecycle lines — the Norman Conquest versions are
the in-repo template.

### A wrapping expanding vbox spreads situation cards apart
**Established:** screenshot, round 3 — the two cards sat at opposite ends
of the panel. MR's fuller gui wraps its MANY cards in an expanding vbox;
with only two cards the free space lands between them. Vanilla's
`rise_of_the_ottomans.gui` (the readme's recommended base) puts its two
cards DIRECTLY in the `situation_panel_main_content` blockoverride.
**Means:** no wrapping vbox for few-card panels; cards as direct siblings.

### France landed: 23 rulers in one pass, the delegation model working
**Established:** 2026-07-28, from the Opus France research report,
spot-verified here (name-key authority claim, core character cites,
cultures, birth locations — all held). 18 rulers were already vanilla
characters and cost one HISTORICAL_RULERS row each; five were authored
(Conan II, Geoffrey III, Baldwin V, William VIII, Eustace II) with five
new dynasties.
- **The additive dynasty route is attested after all:** Anno 1644 ships
  `04_zzz_ottoman_dynasties.txt` (`dynasty_manager = { koprulu_dynasty }`)
  — a working published mod adding dynasties additively. Our
  `04_zz_1066_dynasties.txt` follows it. This refines the earlier
  Timur-based doubt: Timur ABANDONED the route, Anno USES it.
- **MINOR_RULERS:** tags whose 1066 ruler was historically a minor (FRA —
  Philip I, 14, France under Baldwin's regency) skip the adult check; a
  stale exemption (adult ruler on the list) fails the build. Proven both
  ways.
- **Deliberately NOT seated, with reasons in the table comment:** CHP/SAN
  and POI (their rulers already seat BLS/AQN), BAR (titleholder Countess
  Sophie has no character), MTZ (Gerard seats LOR), MIE (Norman-occupied),
  TOU (landless at 1337 — border work first), MRT/EVR/NEV/ANG
  (low-confidence drafts, second source needed).
- Engine-generated loc keys flagged the missing `opinion_*` name the same
  way they did the wargoals — `localization_util.cpp:103` lines ARE the
  loc-key convention, straight from the engine.
**Means:** a region's ruler layer now costs a research subagent run plus a
verification pass plus table rows. France went from zero to 23 rulers in
one sitting; the same pipeline is aimed at the Empire next.

### The Empire at 1066 — structural facts from the research pass (verified cites)
**Established:** 2026-07-28, Opus Empire report, spot-verification pending
landing; the structural claims below carry vanilla file:line cites.
- **The HRE IO's leader is a COUNTRY and the emperor is that country's
  ruler** (`in_game/common/international_organizations/hre.txt:21-25`);
  vanilla 1337 uses `leader = UBV` (Wittelsbach Upper Bavaria).
- **Vanilla's own emperor chain has a HOLE containing our start date:**
  Heinrich III's imperial term ends 1056.10.5 and Heinrich IV's begins
  only 1084.4.1 (`15_international_organizations.txt:130-131`) — the
  engine supports a leaderless HRE (`disband_if_no_leader = no`,
  `hre.txt:50`). Historically exact: the King of the Romans was uncrowned
  emperor in 1066.
- **`ogk_heinrich_iv_salier` exists and is FIFTEEN at start** (b.
  1050.11.11 — 16 on 1066.11.11); OGK ("Holy Roman", rank_empire,
  `is_historic = yes`) is a LANDLESS regnal-history tag with an empty
  `own_control_core`. Seating the emperor needs both MINOR_RULERS and a
  royal demesne — territory work.
- **A pluralist ruler is vanilla-attested:** `boh_john_luxembourg` rules
  BOH and LUX, `hai_guillaume_de_hainault` rules HAI and HOL,
  `brb_jan_iii_van_brabant` rules BRB and LIM — one character, several
  `ruler =` lines plus a term per tag. (This also retro-justifies the
  France pass's caution — seat once until needed.)
- **BAV/SAX/SWA/FKN exist only as FORMABLES** — loc, CoA, colors, formable
  defs, but no `10_countries.txt` block and no identity block.
  **CORRECTED by the Germany II pass (2026-07-29): "no usable tag" was
  one step short.** A formable tag becomes a live country by adding a
  registry identity block — the PYS route — and vanilla itself ships 49
  tags that are BOTH formables and live countries (ENG, FRA, BOH…),
  plus its own comment `tag = LUN # Should be SAX`
  (05_characters.txt:86620). SAX and SWA were revived exactly this way
  (item 25), inheriting name/adjective/color/ARMS free; the cost is
  that the formable becomes unreachable (its target exists from day 1).
  EGY's rejection still stands — that was identity mismatch (Fatimids
  are not "Egypt"), not formable status. CRH/STY are plain landless
  shells (identity block + claims-backed `10_countries` block — the
  shape once misattributed to SKE, which is in fact LANDED at 1337;
  AUDIT-2026-07-31 §4.1).
- The electors (`elector = { BOH SWB BRA PAL }` + three archbishops) are
  the 1356 Golden Bull read backwards; vanilla ships
  `no_golden_bull_policy` so a pre-Bull state is modelled.
**Means:** the Empire's RULER layer has a landable core (Bohemia, Bavaria,
Holland, Mainz, Louvain…) but its CROWN and its DUCHIES are territory
work: OGK needs a demesne, HAB needs breaking up, Swabia/Saxony need a
decision (new tags vs proxy tags). The IO leadership choice is recorded in
HANDOFF as an open decision.

### Byzantium/Anatolia at 1066 — the mirror image of France (research pass, core claims re-verified)
**Established:** 2026-07-28, Opus East report; the three load-bearing cites
checked by hand and exact. France was ruler work on serviceable borders;
the East is the inverse: **the rulers are free, the territory is the job.**
- **Two rows buy the theatre's crowns:** vanilla ships the ENTIRE
  11th-century Byzantine and Georgian cast alive and linked —
  `byz_konstantinos_x_doukas` (term `10_countries.txt:13194`, accession
  1059.11.23, regnal 10) and `geo_bagrat_iv` (term :59447, 1027.8.16,
  regnal 4), plus Eudokia, Michael VII (16 to the day), Romanos IV, the
  Caesar John Doukas, the child Alexios Komnenos — the whole
  1067→1071→1081 arc has actors with family links already wired.
  There is NO Manzikert content anywhere in vanilla — greenfield.
- **The Great Seljuk Empire does not exist in vanilla in any form.** No
  tag, no identity block, no character. `RUM` is only a formable NAME
  whose `tag = TUR` — forming Rum makes you the Ottomans renamed. Only
  `seljukids_dynasty` ships (04_dynasties.txt:8010, home konya). The
  largest state of the 1066 world must be invented whole; Manzikert in
  five years needs someone to fight.
- **The Anatolian transfer is ~305 locations:** BYZ holds 5 of ~308
  Anatolian land locations; 26 beylik-era tags (none with a character
  born before 1210) hold 253. BYZ's own `our_cores_conquered_by_others`
  (:13023-13060) is a Paradox-written 63-location reconquest manifest
  with loss-year comments. Balkans add ~130 more (BUL's 63 Byzantine
  since 1018, Latin Greece…). Dissolve-vs-empty (the landless-shell
  road) is the slice's one real design call — parked.
- **Three vanilla bugs, citable:** BYZ regnal_numbers carries
  `name_andonikos = 3` (:13282) — a typo, zero loc keys match
  (`name_andronikos` is the key); `byz_romanos_iv_diogenes` wears
  Constantine X's death date (1067.5.23) though his own vanilla term runs
  to 1071.10.1; BYZ's regnal numbers are 1337-inflated
  (michael 9→6, roman 4→3, nikephoros 3→2, alexis 5→0, isaac 2→1,
  emmanuel 1→0 for 1066).
- Literal first names are vanilla-attested 496 times
  (`{ name = Karaman }`, `{ name = Selcuk }`, `Izz_al_Din` for
  multi-word) — the escape hatch for missing name keys (no name_alp, no
  name_tughril, no name_gagik…). Underscore→space rendering unobserved.
- TRE's `date = 1204.4.1` KNOWN_FUTURE exemption belongs to this slice:
  Trebizond at 1066 is a Byzantine theme; when it dissolves, the
  exemption goes with it.
**Means:** the East's ruler batch is the cheapest win yet (two rows plus
regnal fixes); everything else is the territory pass, and the Seljuk tag
is the project's first invent-a-country job.

### Iberia at 1066 — Christian rulers free, al-Andalus absent (research pass, core claims re-verified)
**Established:** 2026-07-28, Opus Iberia report; term cites and the LON
landless claim checked by hand (a first crude check here matched GRA's
block by accident — checker-first, again).
- **All six Christian rulers ship in vanilla with their exact accession
  terms**, including the pivot of the start: Ferdinand I's death
  1065.12.27 and the three-way division — CAS Sancho II (:14521, regnal
  2), LON Alfonso VI (:14736, regnal 6), GLC García II (:14791, regnal
  2), plus NAV Sancho IV (1054.9.1), ARA Sancho Ramírez (1063.5.8), CAT
  Ramon Berenguer I (1035.5.26). Vanilla even ships Sancho II's 1071-72
  seizure of his brothers' realms as terms. **But LON, GLC, CAT and VAL
  are LANDLESS at 1337** (claims-only blocks; CAS holds 244 locations) —
  only CAS/NAV/ARA are seatable before the Iberian territory pass.
- **Muslim Iberia does not exist**: no taifa tags, characters or
  dynasties; earliest andalusi character is born 1175. Fourteen taifas =
  the project's second invent-a-country job (after the Seljuks), needing
  the new-tag prerequisite list the report banked (identity block, map
  color, country block, loc, CoA) — build_setup has no NEW_COUNTRIES
  mechanism yet.
- **Free win found:** `rank_duchy_andalusi` (country_ranks.txt:1689) —
  any Muslim duchy-rank tag with an Iberian capital displays as
  "Taifa of X" automatically. The first-match-wins machinery working FOR
  us for once.
- **Name-key traps for the Arabic world:** Yusuf → name_joseph,
  Sulayman → name_salomon, Ismail → name_ishmael, Umar → name_omar (the
  loc registry's .arabic_language rows render them correctly); genuinely
  missing: name_abbad, name_badis, name_abd_al_malik. Inventing our own
  name key is legal-in-principle (a name key is just a loc key) but
  UNTESTED — cheap in-game check before 14 characters depend on it.
- `alpuente` is the one 1066 taifa capital with no location on the map
  (chelva is nearest).
**Means:** Iberia contributes CAS/NAV/ARA to the ruler layer now; the
brothers' realms (LON/GLC/CAT) join with the territory pass — and the
Sancho II vs Alfonso VI fratricidal war (1068-1072) is a ready-made
situation with every actor and date already in vanilla's own data.

### The North and East at 1066 — the Rus are the cheapest region yet (research pass, core claims re-verified)
**Established:** 2026-07-28, Opus North/East report; SWE/KIE terms, the
name_solomon bug and the composite-name attestation checked by hand.
- **Four rows buy the Rus triumvirate plus the Sorcerer:** KIE Iziaslav I,
  NOV Mstislav, CHR Sviatoslav II, POK Vseslav — vanilla characters,
  vanilla family links, vanilla accession terms (KIE :42875, 1054.2.20).
  Only Pereyaslavl is missing — and beware: **`PER` is Périgord, already
  seated**; a careless Pereyaslavl row would silently overwrite France.
  PZL is Pereyaslavl-ZALESSKY, the wrong city. Invent-a-country job #3.
- **Sweden decides itself:** `swe_stenkil` dies 1066.1.1 (pre-start —
  unseatable by our own validator) and vanilla's own term seats
  `swe_halsten` from 1066.1.1 (:81). Mechanically there is no choice.
- **Composite scripted names are vanilla-attested:**
  `name_x.name_y` appears 205 times; CRO's own regnal table carries
  `name_stephen.name_drzislav` (:13915). The key for Petar Krešimir IV is
  `name_peter.name_krasimir` (name_kresimir does not exist).
- **Vanilla bugs #5 and #6:** HUN's regnal table uses `name_solomon = 1`
  (:18524) — ZERO loc entries; the real key is `name_salomon` (:15508).
  SMO's table carries a bare literal `Iwan = 1`. Same class as
  name_andonikos; REGNAL_RENAMES handles the first.
- **A third malformed vanilla date:** `swe_halsten` has
  `death_date = 1100` — a bare year plus `#unknown really..`;
  `date_tuple()`'s padding is load-bearing for it.
- **The region's hard identifier hole: NO Slavic paganism religion**
  exists (`norse`, `romuva`, `muinaisusko`, `sapmi_shamanism` do). The
  Obodrites who revolted in June 1066 have no religion to be — authoring
  one vs proxying romuva is a design call, parked.
- Poland needs a REGNAL_ADDS mechanism eventually (its table lacks
  name_boleslav entirely and REGNAL_FIXES exits on missing keys); the
  ruler_term's own regnal_number carries the display meanwhile.
- The Baltic/Wendish/Yoke-era tag layers (LIT's 98 locations, the
  Ordensstaat, Moscow, the 1138 Piast splinters) are all 12th-14th
  century constructs — territory-pass class, same shape as Anatolia.
**Means:** nine seatable thrones (5 vanilla-free + 4 authored), one new
dynasty (Trpimirović), HUN joins MINOR_RULERS (Solomon, 13), and regnal
surgery for SWE/HUN/CRO/POK rides along.

### The Islamic South at 1066 — the hardest theatre: both rulers AND territory (research pass)
**Established:** 2026-07-28, Opus Levant/Africa report (63 tool uses,
identifier ledger throughout; spot-verification owed at landing).
- **Vanilla ships ZERO Muslim characters who are adults on 1066.9.15.**
  474 Muslim characters, earliest birth 1054 — al-Hariri of Basra, the
  poet, aged 12 (and he starts alive for free). Every ruler in the
  theatre must be authored, on [U] birth years.
- **No tag exists for Fatimid Egypt, the Abbasids, Aleppo or Damascus.**
  ABB is Arbabni in Ethiopia. MAM (143 locations, deeply
  Mamluk-specific) sits on three-or-four 1066 states; JAL is a Mongol
  steppe_horde on Baghdad — repurposing it without a government change
  would render the caliph as a horde (the composed-name law). The
  Abbasid tag and the GREAT SELJUK tag are the same piece of work.
- **Naming machinery, decoded both ways** — CORRECTED by the Persia pass:
  `rank_empire_muslim` ("Caliphate") is **theocracy-gated**
  (`country_ranks.txt:1434` requires `government_type = theocracy`,
  re-verified by hand) — an empire-rank Muslim MONARCHY stays "Empire",
  and the Abbasid tag must be a theocracy or the styling silently never
  fires; the
  Marinid/Zayyanid/Hafsid/Nasrid rank branches are DYNASTY-GATED, so
  seating a Zirid on TUN auto-drops the Hafsid styling with no override
  (first-match working FOR us) — but MAM's branch is tag-gated with no
  dynasty check: an empire-rank MAM becomes "Mamlūk Egyptian Caliphate"
  regardless of who rules. Egypt therefore wants either the branch
  overridden or a real EGY tag (invent-a-country #4).
- **KOJ — the Kingdom of Jerusalem — ships landless WITH identity and
  `is_historic = yes`:** the First Crusade's arrival tag is pre-built.
- **No caliphate IO exists** (34 IO files, none for the era's defining
  Sunni-vs-Ismaili rivalry); the HRE IO is the shape to copy if wanted.
- Religion keys: Fatimids are `religion = shia` + school
  `ismaili_school`; ibadi/shia/sunni are the only Muslim religions;
  ibadi Mzab/Wargla are the least anachronistic Saharan tags.
- Almoravid facts: MRK is landless with the WRONG culture (masmuda =
  Almohad; Almoravids are sanhaja); TFL (Sijilmasa, 21 locations,
  Almoravid since 1054/55) is the one landed seat needing no territory
  work. The September-1066 leadership is genuinely ambiguous — Abu Bakr
  ibn Umar is amir, Yusuf ibn Tashfin his deputy until ~1072; seat Abu
  Bakr, author Yusuf, script the handover.
- Literal names attested IN THIS CONTEXT: `{ name = Tashfin }` is
  vanilla's own (05_characters.txt:48105); ~520 locations in the
  theatre belong to states 150-270 years unborn — a bigger transfer
  than Anatolia's, and most receiving tags must be invented first.
**Means:** a small [U]-flagged batch is landable now (Yemen's Sulayhi,
Zirid Tunis, Almoravid TFL); Egypt/Abbasids/Seljuks/Aleppo are one
coordinated invent-a-country slice; the caliphate IO and the Hilalian
catastrophe are future situation material.

### The Celtic world at 1066 — the High Kingship ships, and the naming grammar decodes (research pass, core claims re-verified)
**Established:** 2026-07-28, Opus Celtic report; the IO term, the
inherit_ruler_terms correction and the Gaelic loc rows checked by hand.
- **The High Kingship of Ireland is a fully built vanilla IO**
  (`international_organizations/high_kingship.txt`): character-type
  leader, elections, THREE casus belli, a GUI panel, and
  `override_ruler_title = yes` — "High King" outranks the holder's own
  title. Vanilla's own term chain (15_IO :303) names the 1066 holder:
  **Diarmait mac Máel na mBó, from 1064.8.22.** Leaderless at 1337; how a
  CHARACTER-type leader is seeded at setup is an open probe. Our
  generator stripped the chain lawfully — a comment now owed pointing
  back at vanilla :302-304.
- **The scripted-name grammar, decoded from the registry's own header:**
  `name_KEY.<language>` rows drive display per the ruler's culture→
  language, `.genitive` drives PATRONYMICS (74 `.gaelic_language.genitive`
  rows — a son of a `name_dermot` father auto-renders "mac Diarmata"),
  and the base key is often unrecognisable: `name_louis` renders
  **Llywelyn** in Welsh, `name_eugene` → Owain, `name_hugh` → Aodh,
  `name_godfrey` → Goraidh. Search the language ROW, not the base key.
- **Clean batch: LEI Diarmait + MCM Toirdelbach Ua Briain** — vanilla
  characters, landed tags (tiny: 1 and 4 locations — Ireland is an
  Anatolia-shape territory job, 38 tags on 96 locations). Vanilla files
  the whole 10th-12th century Munster cast under `mcm_`.
- **Wales is entirely landless** — all six kingdom tags are claimant
  shells (the LON/GLC/CAT shape); WLS itself is the 1267 Principality
  with `culture_definition = english`. Welsh rulers wait for the
  dissolution of the ten marcher tags. `aberffraw_dynasty` and
  `mathrafal_dynasty` ship; Welsh name keys mostly do not (Bleddyn: zero
  hits game-wide; literals are the road).
- **Two more New-World tag traps:** `ISL` is in aridoamerica.txt and
  `GWY` in eastcoast.txt — same class as PER-is-Périgord.
- **Vanilla bug #7:** `tyr_domnall_ua_lochlainn` carries
  `dynasty = o_neill_dynasty` though he is a Mac Lochlainn and
  `lochlainn_dynasty` exists (04_dynasties.txt:379).
- Mann's 1066 ruler is genuinely disputed [D] (Chronicle of Mann vs the
  Irish annals); Godred Crovan is NOT king until 1079 — he fought at
  Stamford Bridge, a ready-made Isles hook for the situation layer.
**Means:** two rows land now (LEI, MCM) plus Diarmait's son Murchad
authored for the Dublin/Mann layer; the High Kingship leader probe and
the Irish/Welsh territory passes are recorded work; the naming-grammar
law upgrades every future Celtic/Gaelic authoring.

### Persia/Central Asia and Italy — the last two theatres mapped (research passes; key claims re-verified)
**Established:** 2026-07-28, the Persia pass (93 tool uses) and the Italy
pass (88); rank_empire_muslim gate, Alp_Arslan literal, map_seljukids,
and the two live output defects re-verified by hand.
- **The Great Seljuk synthesis:** 847 locations / 104 tags at its 1066
  maximum (bigger than Anatolia AND the Levant); recommended carrier is a
  NEW `SEL` tag — free id, and Paradox already ships `seljukids_dynasty`
  + its coat of arms + "Al-e Saljuq" loc + an UNUSED
  `map_seljukids = rgb { 30 160 203 }` (02_map.txt:2926). KRM (Kerman) is
  a ready-made Qavurt appanage seat; MRV sits on Merv; Khwarezm and
  Shaddadid-Ani are Seljuk PROVINCES in 1066 (their founders arrive
  1077/1072 — script, not setup). Do NOT repurpose TIM (breaks the
  Timurid formable — the Prussian-Destiny failure mode) or JAL (horde).
- **The Papacy needs one builder change:** papal names live in the term's
  `regnal_name` (96 vanilla uses — Benedict XII's character is
  name_james/Fournier), which HISTORICAL_RULERS cannot yet emit; and
  PAP's capital is AVIGNON (cardinal-generation follows the capital).
  Otherwise the papal machinery is free: `PAP: "Rome"` IS read (branch 3
  of name construction), rank renders "Papacy"/"Pope", the
  catholic_church IO derives the pope from PAP's ruler, and membership
  is built at runtime by _hardcoded on_game_start. NO 11th-century pope
  ships (earliest papal term is Callixtus II, 1119; the only pap_ alive
  in 1066 is Callixtus aged SIX — Guy of Burgundy, son of our seated
  FCB ruler!).
- **Italy quick wins vs holds:** VEN's 1066 doge SHIPS
  (`ven_domenico_contarini`, doge 1043, with successors); NAP can take an
  authored Guiscard (hauteville dynasty pending); SIC must be HELD
  (Muslim island in 1066 — Palermo falls 1072); Tuscany has NO monarchy
  tag (communes only — design decision); the Byzantine Catepanate
  (Bari falls 1071!) is the southern half of the Byzantium slice, with
  griko_culture shipped and unused. **CORRECTED by the Italy slice
  (2026-07-29): "shipped and unused" is wrong** — griko has zero uses
  in location_templates but **79 define_pop entries in 06_pops.txt**
  (orthodox; Calabria 62.7 units, Sicily 21.2 incl. messina 10.43,
  Apulia 24.8, malta 1.89). Paradox already wrote the Byzantine
  substrate of the Mezzogiorno — under-scaled for 1066, not absent.
- **Two LIVE defects found in our own output and closed/parked:**
  `creation_date` was invisible to every date audit (`\bdate\b` cannot
  match after an underscore — the third one-line/wordbreak blindness of
  the day) — 18 future-dated IO INSTANCES (Guelph/Ghibelline leagues
  1125, Middle Kingdom 1271…) were seeded active at 1066 and are now
  stripped by build_ios with assertions; and 28 future-dated
  DEPENDENCIES ride in 12_diplomacy (Venice-Trieste 1202…) — counted
  and asserted, strip PARKED (it reshapes the vassal web).
- **The authored-identifiers harness check** (dynasty/name/birthplace/
  dynasty-loc/single-seat, 132 items) exists per the pre-test review
  request and caught the `Tamim` missing-loc bug on its first dry run.

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
- **Database operation prefixes — ANSWERED, and now tested in our own code.**
  Measured across 20 workshop mods in the reference project: 599 `REPLACE:`,
  295 `TRY_INJECT:`, 190 `INJECT:`, 116 `TRY_REPLACE:`. Every single use is
  under `in_game/common/…` — advances, prices, laws, generic_actions,
  static_modifiers. **Zero uses anywhere under `setup/`**, so they are not the
  answer for country data; a new filename in `setup/start/` is (see the setup
  section above).
  **Our own REAI mod uses them and works**: `TRY_INJECT:castle = { … }` through
  `in_game/common/building_types/zz_REAI_building_adjustments_addon.txt`, and
  `TRY_REPLACE:call_parliament = { … }` in `generic_actions/`. That is the
  pattern to copy — it edits one database entry instead of freezing a vanilla
  file.
  **And the cost of NOT using them is now measured too.** The Prussian Destiny
  whole-file-overrides `customizable_localization/country_name_construction.txt`;
  diffed against vanilla, its copy silently DELETES vanilla's `ROM_republic` and
  `BYZ_greek` naming branches. No error, no log line — the Roman republic and
  Byzantine Greek names just stop existing for anyone running that mod. For a
  conversion touching hundreds of vanilla databases this is the whole difference
  between patch-survivable and quietly-broken-on-1.4.
  **Known limit:** files whose entries are evaluated FIRST-MATCH-WINS
  (`country_name_construction.txt`, `country_ranks.txt`) cannot always be fixed
  by injection, because an appended branch lands after the one that already
  matched. There a whole-file override may be unavoidable — but then it is a
  decision, taken with the diff in hand, not a default.
- **`replace_paths`** in `metadata.json` → `game_custom_data` declares vanilla
  paths to ignore entirely. Present but empty in a published conversion. For a
  conversion this is how you drop vanilla countries wholesale.
- **`@icon_name!` inline icons** from `main_menu/gui/shared/font_icons.gui`
  (364 named icons) — cheaper than an icon widget, never used by us.

---

## What the new reference mods measure (probed 2026-07-28)

### A popular published mod ships an additive `character_db` setup file
**Established:** Basileia Romaion ships
`main_menu/setup/start/05_br_characters.txt` — 2359 lines, BOM-free, a
`character_db = { … }` block of new characters — ALONGSIDE an edited override
of `05_characters.txt` (2.56 MB vs vanilla's 2.47 MB). Its additive characters
reference vanilla characters as parents (`father = byz_michael_kantakouzenos`)
and vanilla dynasties (`dynasty = kantakouzenos_dynasty`) across the file
boundary.
**Not verified in a running game here**, and published is not attested — but it
is the first sighting of the additive `character_db` route shipped at scale.
**Means:** if our generated-`05_characters.txt` route ever becomes a patch
burden, the additive route has a working precedent worth testing. Until tested
here, generation stays the chosen mechanism.

### A railroad mod abandoned setup dynasties for runtime `found_dynasty`
**Established:** Rise of Timur's `main_menu/setup/start/timurid_dynasty.txt`
is four lines, ALL commented out — a `dynasty_manager` block that never runs.
The dynasty is created at runtime instead:
`in_game/events/DHE/flavor_mughals.txt:5-6` guards with
`NOT = { exists = dynasty:gurkani_dynasty }` then `found_dynasty =
gurkani_dynasty`, and moves members in with `change_dynasty =
dynasty:gurkani_dynasty` (`flavor_wrath_of_timur.txt:124`).
Verified — `found_dynasty`, `docs/EU5-Vanilla-Script-Docs/effects.log:3434`,
"Makes the character found a new dynasty", **Supported Scopes: character**.
**Means:** weak negative evidence on additive `dynasty_manager` in setup — the
one mod seen trying it shipped it commented out. If a Phase 2 region needs a
dynasty vanilla lacks, the attested creation route is `found_dynasty` at
runtime; the setup route needs a test before trust. (So far unneeded:
`fairhair_dynasty` existed.)

### Anno 1644 corroborates the setup BOM rule from a third dataset
**Established:** three of its `main_menu/setup/start/` files sampled
(`05_characters.txt`, `04_dynasties.txt`, `02_zzz_cores.txt`) — first bytes
plain ASCII, no BOM. Its defines file DOES open with a BOM, matching the
"everywhere else wants one" side of the rule. Also of note: it layers additive
`zzz_`-prefixed setup files (`05_zzz_characters.txt`, `04_zzz_w_dynasties.txt`)
over overridden ones — the same additive-next-to-override mix as Basileia.
**Means:** the BOM rule now rests on vanilla, Bronze Era, and Anno 1644.
Nothing to change; recorded so the tally is known.

---

## Reference trees available outside this repo

All read-only. Detect by probing a known file, never a directory.

| Path | What it is | Good for |
|---|---|---|
| `E:\SteamLibrary\...\Europa Universalis V\game` | vanilla 1.3.11 | the authority for everything |
| `mod/Mongol Resurgence` | own railroad mod | situation/state-machine/failsafe shapes, a mature harness, a nine-session test log |
| `C:\Users\Desktop\Bronze Era Modu Total Overhaul` | published conversion | `setup/start`, `location_templates`, the first attested `START_DATE` move |
| `C:\Users\Desktop\Anno 1644 The General Crisis Modu Total overhaul for 1644` | published conversion, start moved to 1644.4.17 | the second attested `START_DATE` move; defines in one tree; additive `zzz_` setup layering |
| `C:\Users\Desktop\Basileia Romaion 1337 total overhaul modu çok popüler` | popular published 1337 total overhaul | mass character/dynasty authoring; additive `05_br_characters.txt` next to an overridden `05_characters.txt` |
| `C:\Users\Desktop\Rise of Timur Another Railroad Mod Example` | published railroad mod | runtime `found_dynasty` instead of setup dynasties; railroad event shapes |
| `C:\Users\Desktop\Location Painter` | the Location Painter tool itself | territorial edits for Phase 2; `EU5_Location_Painter_User_Guide.html` ships next to the exe |
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

### The taifa factory: rank_duchy_andalusi EXCLUDES GRA, and the "Taifa of X" free win is real
**Established:** 2026-07-28, Opus Iberia data package; the rank trigger, LON
precedent, jewel-reform gate, tag freeness and the three missing name keys
re-verified by the main session before a line was written.
- `rank_duchy_andalusi` (customizable_localization/country_ranks.txt:1688)
  fires on duchy rank + (Iberian capital OR iberian_group culture) + muslim
  religion — and carries **`NOT = { tag = GRA }`**. A reused GRA with a
  Zirid ruler falls through every branch to the bare `rank_duchy` at :2006
  and silently displays "Duchy of Granada". Second confirmed case of the
  dynasty/tag-gated rank-branch law (first: Zirid-on-TUN). Hence the
  fresh tag GRZ, with vanilla GRA kept landless in the LON shape
  (10_countries.txt:14682 — a landless kingdom keeps capital and claims)
  and its 18 former locations written into its claims list.
- `the_jewel_of_alandalus_reform` is `has_or_had_tag = GRA`-gated
  (government_reforms/country_specific.txt:3298) — a second, independent
  reason not to reuse GRA.
- **Three invented name keys shipped AND PROVEN IN GAME** (2026-07-28,
  screenshots): name_abbad renders as "'Abbād II Banū ʿAbbād",
  name_badis as "Bādīs Banū Zīrī" — both in their .arabic_language
  forms, because andalusi speaks arabic_language, exactly as the
  two-file-registry law predicts. A name key IS just a loc key,
  confirmed end-to-end; the harness accepts our loc file as a registry.
  Bonus observations from the same screenshots: the character sheet
  renders BIRTH LOCATIONS language-appropriately ("'Ishbīliyyah" for
  sevilla, "Ġarnāṭah" for granada) with zero work from us, and the
  ruler style "Hajib" fires from rank_duchy_andalusi's _ruler_male row.
- **The pop gap, measured:** of the 244 moved locations, 222 are
  `religion = catholic` in location_templates; only 175 carry any sunni
  minority pop in 06_pops. The factory produces borders and thrones; a
  POP CONVERSION SLICE of comparable size is now a named backlog item,
  not a discovery waiting in game.
**Means:** al-Andalus exists: 13 tags, 244 locations out of CAS 131 /
ARA 47 / POR 38 / GRA 18 / MLL 5 / MOR 4 / NAV 1, every emir seated, all
accessions [U] (no taifa ruler exists in vanilla to compare against).

### CORRECTION: "subjects cannot declare war" is a VASSAL law, not a subject law
> **PARTLY SUPERSEDED (2026-07-29, in game):** the war-capability half
> stands (tributary.txt:88), but the conclusion "representable as setup
> tributaries without disarming anyone" FAILED in game — the `visible`
> gate binds at start. See "the tributary `visible` gate DOES bind at
> setup" below.

**Established:** 2026-07-29, Seljuk pass; re-verified by the main session.
`vassal.txt:80-86` restricts declarations to three scripted exceptions —
but **`tributary.txt:88` is `allow_declaring_wars = { always = yes }`**,
and tributaries keep their own color and map name (`tributary.txt:92-93`,
`counts_as_external = yes`). Vanilla ships monarchy-over-monarchy
tributaries AT SETUP in quantity (TUN over BTL/DJE/MZB/ZAB, ERE over
KBD/TDJ/HCI/BFR, ETH, ZAN — 67 total), so the `visible` gate is a
diplomacy-action gate, not a setup validator. The earlier banked law
stays true FOR VASSALS (the appanage/English-subjection strips remain
right); it just never applied to tributaries.
**Means:** loose historical overlordships (the Seljuk khutba: nine
clients) are representable as setup tributaries without disarming
anyone. SEL itself stays independent — Manzikert 1071 is safe.

### The empire-rank name law, and vanilla's dead "Caliphate" branch
**Established:** 2026-07-29, Seljuk pass, all line-cited and re-verified.
- `country_name_construction_prefix_adjective_rank` (:117) fires on
  ANY empire rank (except LAT) and renders `$PREFIX$ $ADJ$ $RANK$` —
  **an empire-rank tag's NAME key is never read.** SEL is therefore a
  KINGDOM: the muslim branch then renders "Sultanate of the Great
  Seljuks" / "Sultan" for free (kingdom size is no objection — vanilla
  GLH is a 738-location rank_kingdom).
- `rank_empire_theocracy` (country_ranks.txt:296) carries NO religion
  gate and sits 1,138 lines before `rank_empire_muslim` (:1434) —
  **vanilla's "Caliphate" string is unreachable dead code.** Our loc
  file overrides the theocracy branch's two strings to
  "Caliphate"/"Caliph"; safe because no vanilla setup theocracy is
  empire-rank (all 16 checked). ABS (type = theocracy + rank_empire) is
  the probe; if the explicit type fails against the include template's
  monarchy, ABS degrades to "Abbasid Empire" — that render IS the
  probe's answer, either way.
- `rank_duchy_persian` = "Malikdom"/"Malik" (:1673) fires before
  `rank_duchy_muslim` "Emirate" for persian-language duchies — the
  Persian client maliks style themselves for free.
- **`$PREFIX$` COMPOSES IN GAME — confirmed live 2026-08-01.** KIE at
  `country_rank = rank_kingdom` with a russian_group culture reaches
  `rank_duchy_grand_principality_slavic` (country_ranks.txt:1136) and
  the map renders **"Grand Principality of Kyiv"** — the prefix row
  (`government_names_l_english.yml:737 "Grand"`) really is prepended to
  the composed name. The probe class is closed: prefix rows can be
  designed for, not just hoped for. (Same launch confirmed the whole
  slavic-principality family: NOV renders "Principality of Velikiy
  Novgorod" as a monarchy.)
- `regnal_number = 0` is vanilla's own no-ordinal value — 184 uses,
  including Alfred the Great and Harold Godwinson.
- **No pop debt for Persia/Iraq:** 634 of the slice's 671 locations are
  already Muslim in location_templates (94.5%) — unlike Iberia, this
  theatre needs no pop conversion slice.
  **CORRECTED by the pop pass (2026-07-29): RELIGION-only.** The
  CULTURE axis carries a real debt: mongolian_culture + nogai are
  11.0% of SEL's pop units (451 units across 150 locations) —
  13th-century Ilkhanate/Horde deposits. The Mongol-strip pop slice
  removes them, which RAISES farsi's share and moves the measured
  3.89 acceptance cost — the Nizamiyya capacity calibration must be
  re-measured after (docs/POP-PHASE.md).

### Landless-with-claims is Paradox's OWN standard shape — the Sardinia trick generalizes
**Established:** 2026-07-28, Byzantium pass. Vanilla ships THIRTEEN
landless-with-claims tags in the Balkans/Caucasus theatre alone (LAT THE
THS VID KVN MOE ZTA HUM TRO SVN CAR TRA IME AMB — ZTA at
10_countries.txt:12486 with claims that ARE Duklja's 1066 borders, LAT
landless at rank_empire :11399). Their claim lists are usable 1066
border data, and the shape scales: this project now ships 48 landless
tags (GRA POR MLL + 45 Byzantine donors), every one keeping capital,
rank, registry entry and claims = its historical re-emergence.
**Means:** before inventing any border, check the target tag's OWN
claims block first; and displacing a tag is never deletion.

### `tag = X ... location = L` where X does not own L is FIRST-CLASS vanilla, not a desync
**Established:** 2026-07-28, Byzantium pass deletion-danger scan.
1,170 of vanilla's own 2,776 tag+location building entries already name
a tag that does not own the location (order_commandery KNI in london,
:1702, is the canonical case; the whole Japanese shoen layer works this
way). The shipped taifa/Sardinia passes added 103 more with no reported
problem.
**Means:** do NOT "fix" 07_cities_and_buildings.txt after ownership
passes; a cathedral on a landless tag's former seat is cosmetic. Of the
27 vanilla setup/start files the mod does not override, only 06_pops
and 07_cities interact with mass ownership change at all, and neither
breaks.

### End-anchored one-liner regexes have a SECOND blind spot: trailing comments
**Established:** 2026-07-28, the future-dependency strip's first run. The
strip pattern `dependency = \{[^}\n]*\}[ \t]*\n` silently skipped 6 of 27
targets because vanilla puts comments AFTER the closing brace on exactly
those six lines (`} #Treaty of Perpignan…`). The one-line-block law's
cousin: line-ANCHORED patterns miss one-line blocks, line-END-anchored
patterns miss trailing comments. The strip's exact-count assertion
(`!= 27 -> die`) is what caught it — a lenient strip would have shipped
six future-dated vassalages silently.
**Means:** every end-anchored one-liner pattern gets `(?:#[^\n]*)?` before
its `\n`, and every bulk strip carries an exact-count assertion.

### Changing a REGISTERED tag's identity data (color etc.) = whole-file override; additive re-declaration is unattested
**Established:** 2026-07-28, the Gallura recolor. Vanilla ships GAL
`rgb { 100 100 100 }` and CAG `hsv { 0 0 0.43 }` — the same grey, invisible
side by side once both hold land (user screenshot; Paradox never cared
because both are landless at 1337). Three routes were checked before
touching anything: (1) Basileia Romaion's additive `br_*` registry files
re-declare ZERO vanilla tags — no attested merge semantics for a duplicate
declaration in `in_game/setup/countries/`; (2) Anno 1644 changes vanilla
countries by overriding the SAME-NAMED registry file wholesale
(`british_isles.txt` etc.) — that is the attested route; (3) the tempting
`color = map_ASK` inside a vanilla 10_countries block
(`10_countries.txt:24524`) is NOT an override precedent — ASK has NO
registry entry anywhere in `in_game/setup/`; its block carries inline
`country_name`/`flag`/`color` because it is a full inline definition, a
different mechanism entirely. Setup-block color on a registered tag would
be an unattested experiment with silent-failure risk.
**Means:** our `in_game/setup/countries/italy.txt` is a byte-for-byte
vanilla copy with ONE changed line (GAL → crimson `rgb { 158 28 35 }`,
the Visconti-of-Gallura rooster) and a header saying exactly that. Diff
it against vanilla after every game patch. Same route for any future
recolor of an existing tag.

### The Caliphate probe PASSED — and the theocracy branch carries a "Holy" prefix
**Established:** in game 2026-07-29, screenshots. ABS rendered "Holy
Abbasid Caliphate" with "Caliph Qaim Banū ʿAbbās, 65" — so an explicit
`type = theocracy` in the setup government block BEATS the include
template's `type = monarchy` (later-key-wins across the include/block
merge), `rank_empire_theocracy` is reachable exactly as designed, and
both loc overrides ("Caliphate"/"Caliph") render. The unplanned third
string: the composed form is `$PREFIX$ $ADJ$ $RANK$` and the branch's
prefix is `rank_empire_theocracy_prefix: "Holy"`
(government_names_l_english.yml:106). The caliphate never carried a
"Holy" — it is a Latin-Christian gloss — so our loc file overrides the
prefix to "" (user-approved 2026-07-29). name_qaim needed no invention:
vanilla ships it (character_names_dynamic_l_english.yml:19941, "Qaim").
**But the monarchy include underneath cost three engine errors** —
heir_selection mismatch (initialize_from_bookmark.cpp:517), two
monarchy laws without their advances under theocracy
(government.cpp:687), no religious_school (:520) — so ABS is now an
explicit theocracy block, every field cited in build_setup.py:
`heir_selection = theocratic_elective` (government_types/
00_default.txt:73), `sharia_law = hanbali_policy`
(laws/01_legal_system.txt:1024), `hanbali_school` (al-Qa'im is the
caliph of the Qadiri creed — Baghdad's Hanbali moment).
**Means:** Muslim theocracies are buildable with no vanilla template,
and the ABS block is the model the Fatimid slice copies (shia/ismaili
variant). "Caliphate" styling needs all three: empire rank + theocracy
+ the prefix override.

### SUPERSEDED in game: the tributary `visible` gate DOES bind at setup
**Established:** in game 2026-07-29. All nine Seljuk clients shipped
`subject_type = tributary` and every one arrived a VASSAL; error.log
names the mechanism to the line — `government.cpp:3702 "Subject type
'tributary' is invalid for 'X' at game start … Reason:
tributary.txt line: 20-24"`, and lines 20-24 ARE the `visible` gate's
OR (overlord steppe_horde / subject tribe / subject steppe_horde /
`modifier:allow_tributary_subject`). The earlier correction's evidence
("vanilla ships monarchy-over-monarchy tributaries at setup") does not
hold: BTL is a monarchy but the vanilla overlords that PASS are hordes
(GLH), tribe-subjecting (NOV), or modifier carriers — the African
advances, the Middle Kingdom IO, government reforms
(country_specific.txt ×3). A downgraded client is a plain vassal:
war-incapable and overlord-tinted, the two things the tributary choice
existed to avoid.
**Collateral, ours:** CHA Champa and DAI Đại Việt log the same class —
vanilla's own CHI tributaries broke when our IO strip removed the
Middle Kingdom, CHI's modifier source. Parked for the China review;
recorded so nobody re-discovers it.
**Fix CONFIRMED IN GAME (2026-07-29, second launch):** SEL carries
`seljuk_khutba_reform` (in_game/common/government_reforms/
zz_1066_reforms.txt) granting `allow_tributary_subject` — vanilla's own
pattern for a non-horde overlord (malian_tribute_system,
country_specific.txt:3917), assigned in setup like ENG's
magna_carta_reform — and it WORKS: all nine clients arrived as
tributaries, own colors, war-declaration screen open, and the nine
3702 lines left error.log. So **a setup-assigned reform's
country_modifier is applied BEFORE the game-start subject validator
runs** — a load-order fact worth its own sentence, because nothing
static could prove it. The harness guards the class ("new-tag
tributary overlords pass the subject-type gate", proven by breaking in
both directions).

### A country must DISCOVER its own capital — and expl_silk_road_center grants nothing
**Established:** in game 2026-07-29 playing SEL: the empire's own land
rendered as terra incognita while Anatolia/Egypt showed, and init said
it outright — "Country 'SEL the Great Seljuks' does not know its
capital, need a discover_areas or discovered_regions"
(initialize_from_bookmark.cpp:528; same line for ABS, UQY, MRD, KKY,
SHD). Root cause: the one include that should cover Persia,
`expl_silk_road_center`, is an ALL-COMMENT template in vanilla — every
line commented out, a no-op include, no error anywhere. Setup discovery
comes from the expl_* templates or an inline `discovered_regions` (PAP
carries one); vanilla's bundle for this theatre is `expl_middle_east`
(132 uses — Mongol-era Persia's own blocks), granting persia/crescent/
caucasus/anatolia/khorasan/arabia/egypt and more. All eight generated
client blocks + ABS now carry it. Hillah seeing the world while Mosul
saw nothing was the same law from the other side: vanilla-blocked tags
kept vanilla's discovery lines.
**Means:** every new landed block needs a discovery source that
actually CONTAINS its capital. `build_setup.py` asserts exactly that,
resolving the capital's membership through definitions.txt — the
assert's own FIRST draft ("any include with live discovery content")
was proven inadequate by its break test: SEL carried three live
silk-road includes that simply do not contain Rey. Checks must encode
the engine's requirement, not a proxy for it.

### The registry's culture_definition IS a landed tag's primary culture — measured
**Established:** in game 2026-07-29: "primary culture is duplicated in
accepted cultures for ARA Aragon" (country.cpp:6166). The Iberia pass
wrote `accepted_cultures = { catalan }` (vanilla ARA carries
`{ aragonese }`); the duplicate is only possible if ARA's primary IS
the registry's `culture_definition = catalan` (iberia.txt:17). That
closes the deferred "VERIFY IN GAME first that the field even matters
for a landed tag" item — it does. Fix by the attested registry-override
route (the Gallura precedent): our `in_game/setup/countries/iberia.txt`
changes that one line to `aragonese` (key verified cultures/
iberian.txt:22; vanilla itself writes the same value form in this
file's commented MTS block). Setup `accepted_cultures = { catalan }`
stays — Jaca's kingdom is Aragonese-primary, Catalan-accepting.
**Means:** a tag's `culture_definition` is not registry decoration. At
design time, set it to the intended PRIMARY culture, and never repeat
the primary in the accepted list.

### Accepting a culture costs cultural capacity — and a reform can pay it
**Established:** in game 2026-07-29, screenshot of SEL's society panel.
`accepted_cultures = { farsi_culture }` costs **3.89** capacity (the
cost scales with the culture's pop share — Farsi is 20.57% of the
empire) against a kingdom's capacity of **2.00** (+1 rank, +1 Age I),
and the overflow penalty is severe: **-47.41% cultural tradition,
-47.41% cultural influence, -18.96% cabinet efficiency**. Setup
acceptance is not free flavour.
**Means:** the acceptance and its budget ship TOGETHER:
`seljuk_nizamiyya_reform` grants `cultures_capacity = 3` — vanilla's
own construct at vanilla's own magnitude (the SE-Asian mandala reform,
country_specific.txt:3909) — capacity 5.00, penalty gone, and the
reform IS the history (the Turkic sword, the Persian pen). Any future
slice that accepts a large culture must budget capacity the same way.
**CONFIRMED IN GAME (2026-07-29, third launch):** capacity 5.00, the
penalty box gone, and both reforms render by name in the government
screen ("Recognition of the Khutba", "The Nizamiyya").
**RECALIBRATED (2026-07-29, played):** +3 was penalty-free but left
1.11 headroom after farsi — no second culture could be accepted or
tolerated (tolerate costs 1/3 of accept, the engine's own tooltip)
and their pops' levies stayed low. The reform now grants +6 (capacity
8.00). Vanilla reforms cap at 3, so this magnitude is OUR play-sized
calibration, not an attested one — recorded as such in the reform
file; retune as SEL's borders change. UNTESTED until the next launch
(expect capacity 8.00 in the society panel).

### Second-launch residue: a has_policy prerequisite, and the _no_coast template family
**Established:** in game 2026-07-29, second launch — two self-heal
classes remained in error.log, both decoded to the line.
1. **A law group whose `potential` is `has_policy = X` needs X shipped
   in the same block.** ABS carried `sharia_law = hanbali_policy` but
   not `legal_code_law = sharia_law_policy`; the group's potential
   (01_legal_system.txt) failed and the engine REMOVED the law at init
   (government.cpp:3535). One missing line — the muslim template's own
   `legal_code_law = sharia_law_policy` — makes it legal. The clients
   never hit this because their template carries the prerequisite.
2. **Vanilla's setup templates come in _no_coast variants, and the
   engine tells you which countries need one.** The coastal muslim
   template's `sponsor_maritime_contracts` privilege (and two maritime
   laws) get self-heal-removed on every INLAND country, one error line
   each (government.cpp:3662) — the flagged list (5 inland taifas, the
   7 inland clients, GHZ) was exactly the inland set, measured for us.
   Vanilla has 27 no_coast uses in this file; ours makes 39. Diff the
   variant before switching: no_coast carries NO heir_selection of its
   own, so the heir line is restated explicitly in our generated
   blocks.
**Means:** when the engine "removes" something at init, it is naming a
missing prerequisite or a wrong template variant — read it as a diff
against what the block should have declared, not as noise.
**Both fixes CONFIRMED IN GAME (2026-07-29, third launch):** ABS's
sharia_law line gone, and no 3535/3662 line names ANY of the 12
no_coast-switched blocks. The surviving 3662 residue was classified
tag by tag against the build lists: all 28 flagged tags are landless
shells (decoder sub-class 3) — reading a "still there" log correctly
meant checking WHICH tags, not counting lines.

### CWTools CW225 flags cross-file $refs$ in loc — false positive, with a live caveat
**Established:** CW225 on `SEL_THE: "$common_string_prefix_article$"` —
"references common_string_prefix_article which doesn't exist in
English". The string exists (common_used_strings_l_english.yml:95,
"the") and the construct is vanilla's own (`THE_FUGGERS_THE`,
country_names_l_english.yml:8); CWTools just does not resolve
cross-file $refs$.
**Caveat:** the 2026-07-29 screenshots show the map name WITHOUT the
article — "Sultanate of Great Seljuks" — so whether the engine consults
`<TAG>_THE` here at all is UNPROVEN. Eyeball item on the backlog, not a
bug hunt.

### A setup reform need not consume a reform slot — grant the slot back inside the reform
**Established:** 2026-07-29, user request on the Seljuk reforms. The
slot capacity is the country modifier `government_reform_slots`
(modifiers.log:793; the DLH event counts against it —
`num_reforms >= modifier:government_reform_slots`,
flavor_DLH.txt:4659). `government_size` is a DIFFERENT modifier
(:797) — do not confuse them. A reform granting
`government_reform_slots = 1` in its own `country_modifier` is
vanilla's own pattern: revolutionary_empire
(government_reforms/monarchy.txt:169), theocracy.txt:75/96,
republic.txt ×5 — the reform occupies a slot and hands one back, net
zero.
**Means:** all three mod reforms (seljuk_khutba, seljuk_nizamiyya,
fatimid_khutba) carry it, so a setup-assigned historical reform never
eats the player's or AI's enactment budget. Any future setup reform
ships with the same line.
**CONFIRMED IN GAME (2026-07-29, Fatimid launch):** SEL's government
screen shows the extra free slot; both reforms still render.

### regnal_name accepts an invented LITERAL — measured
**Established:** in game 2026-07-29, the Fatimid launch. FAT's term
carries `regnal_name = Mustansir` where `Mustansir` is OUR literal
(loc row `Mustansir: "al-Mustansir"`), not a name key — and Cairo
renders "Caliph al-Mustansir". Vanilla's own `regnal_name = Chungsuk`
(10_countries.txt:24295 against character_names_l_english.yml:11818)
predicted it; now proven in our data. The papal route (name keys —
name_alexander, name_qaim) and the literal route are BOTH live.
**Means:** a regnal name never blocks on the name-key bank again —
any missing key is one loc row away, same as first names.

### The French subject-type laws — appanage's real killer, fiefdom's ruler theft, and the vassal web that outlived the strip
**Established:** 2026-07-29, France demesne package; every cite
re-verified by the main session against the subject_types files.
1. **Appanage dies at 1066 because of the REGENCY, not the dynasty
   link.** The `visible` block (appanage.txt:120-133) has NO dynasty
   condition — it wants monarchy + `french_feudal_nobility`, which
   vanilla FRA carries (10_countries.txt:15156). The killer is the
   separate `enabled` block (:135-155): its first line is
   `exists = root.ruler_or_heir_if_regent.dynasty`, and FRA at 1066 is
   under an ENGINE regency (Philip I is 14) — the generated regent has
   no dynasty, so every appanage fails [INFERRED from the block +
   the observed all-ten failure; consistent, not screenshot-proven].
   The earlier "needs a Capetian dynastic link" reading was the right
   outcome for the wrong clause.
2. **fiefdom and dominion carry `has_overlords_ruler = yes`**
   (fiefdom.txt:16, dominion.txt:17) — the subject's throne shows the
   OVERLORD's ruler. Vanilla's BOU→MRC fiefdom was silently overriding
   our seated Adalbert of La Marche; FOI→BRR/MDM copied Roger II onto
   Béarn. Never leave a fiefdom tie over a seated ruler.
3. **Only `subject_type = appanage` was ever stripped — 27
   `first = FRA ... vassal` lines survived every launch** until this
   slice, war-blocking (vassal.txt:80-86) twelve of our seated
   thrones. A premise like "the fiefs are independent now" must be
   grepped, not remembered — the check took one command.
4. march is the only gate-free type (rank + lock only, march.txt:6-33)
   but drags subjects into EVERY offensive war (:36-38) and its
   war-declaration/map-tint behavior is unattested — probe before use.
**Means:** loose feudal geometry = tributary + a khutba-pattern reform
(third use: capetian_homage_reform); the subject-type table in the
France package is the reference for every future tie decision.

### Vanilla definitions.txt ships a SELF-NESTED duplicate province
**Established:** 2026-07-29, the France slice's first dry-run.
`limousin_province = { limousin_province = { limoges aixe ... } }`
(definitions.txt:944-945) — the flattening parser lists every member
TWICE, and `_resolve_ruleset`'s sweep comprehension (seen updated
after the walk) let both copies into the grant list, where the
duplicated tokens would have failed the exclusivity validate.
**Means:** the resolver now dedups DURING the walk (build_setup.py,
comment in place). Any future parser over definitions.txt must assume
duplicate members are possible — Paradox's own data does it at least
once.

### The tributary gate's THIRD branch is free: a tribe subject needs no reform
**Established:** 2026-07-29, British package; tributary.txt:19-24
re-read. The visible gate is an OR of overlord-steppe_horde /
subject-TRIBE / subject-steppe_horde / modifier:allow_tributary_subject.
Every Gaelic tag rides `gaelic_tribe*` includes (type = tribe), so the
six Irish ties ship with NO reform — SEL/FAT/FRA each needed one only
because their subjects are monarchies.
**CONFIRMED IN GAME (2026-07-29 evening):** all six Irish tributaries
arrived AS tributaries, war screens open, and the load log carries
ZERO 3702 lines naming any mod tag — **the tribe branch of the
visible gate IS evaluated at game start**, exactly like the modifier
branch (now proven three ways: modifier via reform ×2 slices, tribe
via this one).
**Means:** when designing a tributary ring, check the SUBJECTS'
government type first — the reform is only for monarchy-over-monarchy.
The harness gate check knows both branches (proven by breaking).

### Seeding a CHARACTER-led IO leader at setup: `leader = <TAG>`
**Established:** 2026-07-29, British package.
**CONFIRMED IN GAME the same evening:** Ireland tints under Leinster
on the map and Diarmait renders "High King" in the IO panel — the
one-line seed works exactly as the catholic_church precedent
predicted.
A character-led IO (high_kingship.txt:23 has_leader_country,
:26 leader_type = character) derives its character from a leader
COUNTRY through its own `leader = { leader_country ?= { ruler ... } }`
block — so setup seeds the TAG, exactly like a country-led IO. The
attested precedent is the structural twin catholic_church
(type definition :10/:12 identical shape; setup instance
`leader = PAP`, 15_international_organizations.txt:182). Our
high_kingship instance now carries `leader = LEI` — Diarmait, High
King since 1064.8.22 by vanilla's own stripped term (:303). The
observable: Ireland tints under the leader (show_as_overlord_on_map
fires only with a leader) and `override_ruler_title` renders
"High King".
**Means:** any future character-led IO (a caliphate IO one day) seeds
its leader the same one-line way.

### Landless tags ghost in IO member lists — and vanilla has three legitimate landless-member types
**Established:** 2026-07-29, the new "IO members hold land" harness
check's FIRST runs. Vanilla's own high_kingship list documents the
rule (its `#PLE` comment excludes the landless Pale) — and our earlier
slices had left SIX ghosts behind: ARM/ATZ/CIL in the autocephalous
patriarchate and EPI/TRE/FEO in Orthodox lists, all emptied by the
Byzantium/Seljuk passes and sitting in their IOs ever since.
build_ios now strips LANDLESS_AFTER members generically (exact-count
6, the count measured 1→4→6 as a stale-offset loop bug — caught by
the assert itself — was fixed). The check's false positives mapped
vanilla's legitimate landless-member types: `type = building`
(Japanese clans TGS/YSM), `type = army`, `type = pop` (Thai sect
DDI) — validate ours strictly, report what vanilla ships.
**Means:** every future slice that empties a tag gets the IO sweep
free; the check (753 members) and the strip guard each other.

### A leaderless HRE does not stay leaderless — the election is live at day 0
**Established:** 2026-07-29, HRE package; re-verified by the main
session. `resolutions/hre_election.txt:17-21` — the election
resolution's `is_live` is `international_organization_has_leader = no`,
so a headless HRE votes IMMEDIATELY; and `hre.txt:459-488` is a
monthly failsafe that, after a two-year deadlock, crowns the richest
eligible member by `country_tax_base` — at 1066 that means a Habsburg
(68 locations) or Přemyslid emperor within two years. The
"historically exact leaderless interregnum" design was therefore
DEAD ON MEASUREMENT; the crown went to Heinrich IV on a landed OGK
(user decision D) with the title fixed by loc override
(HRE_LEADER_MALE → "King of the Romans"). Also measured: vanilla's
GERMAN-KINGSHIP chain has no hole (Heinrich IV rules OGK
1056.10.5-1106.8.7, 10_countries.txt:34907) — only the IMPERIAL term
chain gaps 1056-1084; and `can_lead_trigger` wants `country_exists`
+ no-regent-or-heir, so a landless OGK could never have led anyway
(every one of vanilla's seven led IOs has a LANDED leader).
**Means:** never design around "the IO just stays headless"; the
election machinery is always on. Title wrongness is a loc problem,
not a leadership problem.

### The margraviate rank branch is a free win for marches
**Established:** 2026-07-29, HRE package; country_ranks.txt:2298 —
`rank_county_margraviate` fires on county rank + the `margraviate`
reform (government_reforms/monarchy.txt:30, setup-assigned by NINE
vanilla tags) → "Margraviate"/"Margrave". Austria and Styria style
themselves correctly for one FIELD_FIXES line each.
**Means:** any future march (Brandenburg-era work, Spanish marches)
gets the styling free — county rank + the reform.

### Registry first lines hide behind the BOM — grep ^TAG misses them
**Established:** 2026-07-29, HRE package correction. `HAB = {` IS in
`south_germany.txt:1` and `HOL = {` in `lowlands.txt:1` — but the
UTF-8 BOM sits on the same line, so a `^`-anchored grep reports them
absent (this file's own history: the same trap produced "ENG does not
exist" in week one, and STILL caught a research pass this week).
**Means:** registry greps use utf-8-sig reading or drop the anchor;
"no registry entry" claims about a file's FIRST tag are suspect until
byte-checked.

### Tag-freeness sweeps MUST exclude binaries
**Established:** 2026-07-29, Italy package. An unfiltered `grep -rlw`
for a three-letter id over the game tree returns 91-356 "hits" per
candidate — all `.dds`/`.bin`/`.mesh` binary noise; with
`--include=*.txt --include=*.yml ...` (or `-I`) the same ids return
their true counts (APU/CUP/SLR/NEA/GAE/PLM/AGR: zero each). The CAP
verdict also refined: its 11 hits are a `$CAP|=+$` loc PARAMETER in
interfaces loc, not a tag — conservative to avoid, but not proven
taken.
**Means:** every freeness sweep names its file-type filter, or it
lies in the safe-looking direction and wastes free ids.

### The pop pass's banked traps (full detail in docs/POP-PHASE.md)
**Established:** 2026-07-29, the pop research pass; headline items:
(1) **11 vanilla location keys carry UPPERCASE letters**
(trgoviste_SER, tata_MOR, matanda_aChiwawa...) with 28 pops between
them — a lowercase-only key regex drops them silently (the agent's
own first parser did; our _ownable_set was already correct);
(2) **pops are the STATE, location_templates the load-time SEED** —
every trigger/estate/levy reads pops; the layers disagree in 3,419
vanilla locations; (3) elite pops are SEEDS the engine inflates
(nobles world-wide = 33 units) — author identity, not quantity, and
verify in game only with `-leavepops`; (4) ≥4 same-type pops per
location MERGE (defines:1633) — ≤3 is the safe zone; (5)
**`REPLACE_OR_CREATE:` is a real database prefix** (Basileia ×167) —
the prefix list in this file gains a fourth member; (6) emptying a
culture world-wide errors unless it carries
suppress_no_pops_error = yes; (7) in_game/map_data is BOM-MIXED
(definitions yes, location_templates no).
**Means:** the pop generator design (a sixth build target reusing
the territory rule sets, per-theatre slices, the Sicily probe first)
is fully briefed in POP-PHASE.md; the ONE escalated design call is
Slavic paganism (invent/proxy/accept — user decision pending).

### Setup templates NEST includes — a one-level reader lies
**Established:** 2026-07-29, British package.
catholic_monarchy_welsh_releasable.txt line 1 is a bare
`include = catholic_monarchy_not_present` (unquoted!) and line 2 the
quoted `include = "expl_western_europe"` — the Welsh shells' ONLY
discovery source and their `country_rank = rank_duchy` both live in
the template, not the blocks. The one-level `_tpl_grants` would have
called the shells blind AND the landed swap would have silently
dropped their discovery and rank. `_tpl_grants` is now recursive
(cycle-guarded, both include spellings), and the Welsh FIELD_FIXES
restate expl + rank explicitly.
**Means:** any check or swap that reasons about a template must walk
the full include chain; vanilla mixes quoted and unquoted include
forms.

### The situation-spec pass's mechanism findings (2026-07-29; the specs live in docs/SITUATION-SPECS.md)
**Established:** the spec-bank research pass; the three headline
claims re-verified by the main session by hand.
1. **The DISASTER system exists and we have never used it** — 35
   vanilla disasters, a native `modifier = {}` block situations lack,
   `fire_only_once`, its own actions and map-mode link
   (disasters/readme.txt). The country-scoped sibling of a situation.
2. **`byzantine_succession_crisis` is LIVE at 1066** (re-verified:
   `tag = BYZ`, no date/age gate) — a complete pretender machine that
   can fire on our Byzantium TODAY. Next-launch grep: has it been
   firing already? Spec 1 drives it rather than duplicating it.
3. **`coup_attempt` is dead for our whole era** (re-verified:
   `NOT = { current_age = age_1_traditions }`, coup_attempt.txt:8) —
   the first cheap MEASURED content cost of the age-1 decision;
   feeds the open age-1 question.
4. A situation has NO phase field and NO modifier block — phase is a
   situation-scoped variable (the Tordesillas idiom), modifiers are
   pushed from lifecycle hooks; situation FACTIONS are real IOs
   joined via `join_situation_faction` (no add_to_situation exists).
5. NO character imprisonment and NO scripted battles exist — both
   are modifier+event constructions.
6. **Vanilla bug #8:** `eng_henry_i` carries
   `father = eng_william_ii_rufus` (his BROTHER; both are the
   Conqueror's sons — re-verified 05_characters.txt:733). Fix rides
   with the Norman v2 spec. Bug #2's consequence sharpened:
   `byz_romanos_iv_diogenes` wears Constantine X's BIRTH date too —
   our death-strip leaves him alive but aged 60 at Manzikert; fix
   rides with the Manzikert spec.
7. The 11th-century vanilla roster is 43% Japanese (193 of 446 born
   1000-1090); Latin Christendom + Byzantium is under 150 — every
   Islamic/Norman-Italian/Welsh/Pecheneg actor must be authored.
8. Map gaps of the alpuente/Amalfi class, recorded: alamut,
   silistra, sofia, pliska, adrianople, zallaqa, tyre.
**Means:** the situation phase opens with twelve reviewed build
briefs, a priority order whose first five items teach the tools the
flagships need, and two vanilla-bug fixes pre-assigned to their
specs.

### Coats of arms are compositional, key-bound and GENERATED when absent
**Established:** the CoA research pass (2026-07-29 night), main-session
re-verified; full bank in `docs/COA.md`. The chain:
`flag_definitions/00_flag_definitions.txt:1` — a country with no
flag_definition list uses its TAG as the COA_KEY (the debug panel's
`Flag` row shows it). The database is additive and key-merged,
last-loaded file wins per key (Basileia `zz_br_flags.txt:1` states it;
24/24 published mods do it). A tag with NO entry gets a flag from the
`template_lists` generator — religion/culture/rank-gated, so it is
plausible, silent, and sometimes exactly backwards: our ABS rendered
generator-white and FAT generator-black (user screenshots), each
Caliphate wearing the other's colour. The registry `color` field does
NOT feed the flag (VMD: old-gold registry, red generated flag).
Vanilla itself leaves 280 landed 1337 tags to the generator.
**Means:** invented tags need no arms to look fine, so arms are a
COSMETIC-UPGRADE pass, not debt — but a broken texture name, colour or
key also falls back to generation with NO log line, so verify_mod's
"coat of arms references resolve" check (proven by breaking) is the
only detector. Every new-slice tag must either get arms in
`zz_1066_flags.txt` or join `_GENERATOR_OK` deliberately.

### Line-anchored scans are blind to one-line blocks — the anchor class's fourth incident
**Established:** vanilla ships exactly 23 one-line
`government = { ruler = X }` blocks (22 random + AOS's 1291-born
sav_aymon_savoy, vanilla 10_countries.txt:36343). Every line-anchored
ruler scan in build_setup.py missed them: the rewrite pass could not
convert them, the add-missing pass double-inserted into all 23, and
the build's own validator shared the anchor and blessed the result —
three independent scans wrong about the same construct (the
two-validators-wrong-about-DHE-reachability shape, again). Found by
the Italy North research review 2026-07-29; NTC's commented
`#ruler = jap_koumyou_tenno` then ambushed the widened scan on its
first run, so the fix is BOTH unanchored AND comment-stripped.
**Means:** with BOM-defeats-^ (three incidents) this is the anchor
class's fourth: any `^`-anchored scan over Paradox script must first
prove the construct never occurs mid-line. Harness now guards
"exactly one ruler key per country block" (2378 items, proven by
breaking); the build validator scans unanchored comment-stripped text.

### Four laws imported from the MR session of 2026-07-30
**Established:** the MR observer-run decode + six-lens audit, each point
measured there and re-checked for relevance here.
1. **Advance `requires` never crosses an age.** 2748 of 2748 vanilla
   `requires` entries name a SAME-age advance, zero exceptions; vanilla's
   Chagatai line roots its age-3 advance on a fresh age-3 root rather
   than its own age-2 predecessor. A cross-age chain likely dead-ends
   silently at the age boundary. Matters here the day 1066 authors
   advances — and age_1 spans 276 years, so our chains will be LONG;
   MR's harness now encodes the law, copy that check when the first
   1066 advance lands.
2. **Resource modifiers no-op silently on governments lacking the
   resource.** `monthly_horde_unity` on a settled monarchy errors
   NOTHING — vanilla grants it to non-hordes deliberately (generic
   age-5 reform `licensing_of_the_press_act` gives horde unity AND
   tribal cohesion to everyone). Cross-government content costs dead
   tooltip lines, never log spam — relevant to every 1066 reform or
   advance that touches tribes and hordes.
3. **A pure identity block trips a 12-line init barrage** unless it has
   a 10_countries presence, revolter cores, or `is_historic = yes` —
   full decode in the error decoder. Our landless shells are immune
   (they carry claim blocks); a future presence-less tag is not.
4. **definitions.txt: 1337 of 4150 province blocks are MULTI-LINE.**
   Any line-based parser silently drops 38% of the map — MR's harness
   did exactly that (16,948 memberships seen vs 27,279 real) until its
   2026-07-30 fix. Checked the same day: our `_parse_defs` is
   token-stack, brace-aware, comment-stripped — CLEAN. The law binds
   any FUTURE parser: token/brace-based only, never line-shape.
**Means:** the anchor class (BOM-^, one-line blocks, now multi-line
provinces) keeps producing members; parse structure, never line shape.

## Carried over, still to do

- **Raise the harness `min_count`s** as each kind of content first appears. The
  rule is in `CLAUDE.md`; this is the reminder that it applies from the very
  first `.txt` file, because until then every check reports `SKIP`.
- **Install CWTools** (`tboby.cwtools-vscode`) — a Paradox script language
  server that catches syntax and reference errors in the editor, before the
  harness and long before the game.

### An unbound country slot in a static tooltip renders as SWEDEN — the database's first-registered tag
**Established:** in game 2026-07-30, on Mongol Resurgence's late-steppe
situation panels: `government_type = government_type:steppe_horde`
inside an `any_country` end trigger rendered as "Sweden is Steppe
Horde". The fallback is mechanical: SWE is the first tag the country
database registers (`_scandinavia.txt:1` — underscore-prefixed file
sorts first, SWE sits on line 1 behind the BOM). Evaluation is
per-iterated-country and CORRECT; only the display subject is unbound.
The scope-compare form itself is vanilla's own (culture_jurchen.txt:
121-122), and the bare-key form has zero vanilla uses in trigger
position — so the fix is never to rewrite the trigger, it is to wrap
the requirement in `custom_tooltip` (MR's header rule: ONE
custom_tooltip PER requirement, text on one line — a single wrap
around everything fights the checklist widget, measured in MR Phase 3).
**Means:** any player-visible trigger context (situation can_end
foremost) that iterates countries or compares scope objects needs its
custom_tooltip wrap from day one; "Sweden" appearing in a tooltip is
THIS, not a tag error. Fixed in MR 3f082c5.

### Ten locations game-wide live in TWO ownership blocks — vanilla's occupation model
**Established:** Baltic package measurement, confirmed at implementation
2026-08-01: `palanga rietavas silale skuodas taurage mazeikiai` sit in
LIT's `own_core` AND TEU's `control` (vanilla 10_countries.txt:726-734);
`arshgul madinat_alawiyyin ras_al_ain saida` sit in TLE's `own_core`
AND MOR's `control`. `control` is the last member of the build's
OWN_KEYS, so `_remove_owned_many`'s exactly-once assert, the
LANDLESS_AFTER guard and the orphan-capital guard all read the
occupation as a holding. `FIELD_FIXES` runs after all three and cannot
help.
**Means:** any slice that grants, vacates or retires TEU/LIT (done) or
MOR/TLE (the Maghreb slice's day one) must clear the occupation first —
`CONTROL_STRIPS` in build_setup.py, exact-count asserted, placed BEFORE
the `_landless_claims` snapshot so the retiree's claims are its real
holdings, not its conquests.

### A tag-gated RANK branch can sit above the generic ones — the LIT instance of the horde-name law
**Established:** `country_ranks.txt:1355-1362` triggers on `tag = LIT` +
`country_rank_is_duchy` and resolves "Grand Duchy" / "Grand Duke" — 249
lines above `rank_duchy_tribe` (`:1606`). First-match: a LIT reskinned
to `type = tribe` but keeping `rank_duchy` still renders "Grand Duchy of
Lithuania"; only `rank_county` escapes, at the price of
`rank_county_tribe`'s "Minor Tribe of ..." (`:2279`).
**Means:** before reskinning ANY tag, grep `country_ranks.txt` for the
tag name — the name-composition trap (CLAUDE.md horde law) extends to
the RANK word, and it is hard-coded on the tag. The Baltic slice retired
LIT rather than fight the branch (user decision, option 2).

### A tag emptied by grants but absent from LANDLESS_AFTER ships a GREEN build the engine rejects
**Established:** Baltic break-test (e), 2026-08-01: RIG removed from
BALTIC_LANDLESS produced a full green build with RIG as an emptied,
claimless shell — the `initialize_from_bookmark.cpp:592` state. The
:5401 guard loops only LANDLESS_AFTER members; KLB nearly shipped the
same way from the Arabia package. Closed by the delta sweep (commit
6ce8ed7): every tag holding land in PRISTINE vanilla must still hold
land or be listed; proven against the RIG known positive.
**Means:** the guard class to trust is delta-vs-pristine, not
list-membership; and a package's "the verifier catches this" claim is
itself a break-test target, not a fact.

### A `^`-anchored grep misses a file's FIRST identifier when the file carries a BOM
**Established:** 2026-08-01, nearly a false refutation: `grep
"^aukstaitian" cultures/baltic.txt` returns nothing because
`aukstaitian` is the file's first block and sits BEHIND the BOM
(baltic.txt:1). The Sweden-tooltip entry above records the same
byte-order fact from the engine's side (SWE on line 1 behind the BOM).
**Means:** never conclude "identifier does not exist" from an anchored
grep alone — re-run unanchored before declaring a package claim false.

### Granting vanilla-UNOWNED land needs its own path — the grant machinery demands exactly-one ownership
**Established:** Africa slice, 2026-08-02: SNH's nine Adrar/Arguin
locations are ownerless in vanilla, and `_remove_owned_many`'s
exactly-once assert (the Sardinia guard) died with `occurrences != 1
for ['arguin(0)', …]` on the first dry-run — the machinery was built
for owner-to-owner moves and had never filled empty land. Closed by
`UNOWNED_GRANTS` (build_setup.py): each location zero-asserted against
the source (a vanilla patch that lands an owner fails loudly), asserted
present in its tag's resolved grant list, removal skipped, ownership
write included. Break-tested with an owned location (awlil → abort).
**Means:** any future slice that settles vanilla-empty ground (steppe,
Sahara, taiga) lists it in UNOWNED_GRANTS; never loosen the
exactly-once assert itself. Filling unowned settled land SHRINKS the
~504-line vacated-pop error class — the only mechanism that does.

### The African rank/name lattice: culture-gated RANK branches, and a tag branch whose MAP string is the FULL string
**Established:** Africa package, re-verified at implementation.
`country_name_construction.txt:79-89` is gated `tag = MAL` + monarchy +
kingdom-or-empire and its `_map` loc string is `"$PREFIX$ $NAME$
$RANK$"` — the full string, so a 1066 MAL at rank_empire reads "Mali
Empire" ON THE MAP; only the rank line escapes (rank_duchy → the
muslim fallback, map reads bare "Mali"). Deeper than the LIT trap:
`country_ranks.txt`'s African branches are CULTURE- or court-language-
gated, not tag-gated — `rank_*_mali` follows `culture:mandinka`
(ruler "Mansa"), `rank_*_kanem` follows `kanembu_culture` ("Mai"/
"Shehu"), `rank_*_ethiopia` follows `court_language ?=
ethiopic_language` ("Negus") — so ANY tag of that culture inherits the
title. And first-match order flips by rank: at duchy, tribe (`:1606`)
beats muslim (`:1743`) which beats mali/kanem/ethiopia
(`:1887-1907`); at kingdom, kanem (`:957`) and mali (`:967`) BEAT
muslim (`:1060`). That asymmetry set KBO at rank_kingdom (renders
"Mai") and MAL at rank_duchy. Also measured: `rank_county_muslim`
does not exist — a county-rank Muslim state renders "County"/"Count".
**Means:** rank choices for non-European tags are RENDER choices;
walk both files at the exact rank before declaring one, and grep for
culture-gated branches, not just tag-gated ones.

### A country reader missing an OWN_KEYS member reports phantom unowned land

**Established:** SEA package review, 2026-08-02. The build's ownership
model is exactly TEN list keys (`tools/build_setup.py:5388`,
`own_control_core` … `control`); the SEA research agent's independent
reader counted a subset that missed **`own_control_integrated`**, and
every conclusion downstream of it was confidently wrong: ten
"vanilla-unowned" Khorat/Mekong locations (VTN's 7 + MUA's 3 integrated
holdings) grew a whole UNOWNED_GRANTS design for land that had owners;
VTN "25" (real 32) "corrected" INDIA-CHINA-REVIEW's correct figure;
BTU "1 location" actually holds the Agusan coast (6) — mooting a
grow-Butuan decision argument; MGD "1" was 5. In-theater, 62 locations
sat invisible. The review caught it by re-running the counts with the
build's own reader — same class as the `^`-anchored-BOM and
one-line-block blind spots: a partial reader does not error, it lies.
**Means:** a package's "unowned" / "holds N" claims are hypotheses
until reproduced with the full OWN_KEYS set; any UNOWNED_GRANTS
proposal must first re-prove the zero with `_ownership_index`, and any
reader written outside `build_setup.py` should import its parsers
rather than reimplement them.

### The tributary visible gate can ride a VANILLA reform — and the gate check had to learn templates

**Established:** SEA slice, 2026-08-02. `mandala_system`
(`VAN/in_game/common/government_reforms/country_specific.txt:3894-3915`)
carries `allow_tributary_subject = yes` and sits in the `reforms = { }`
block of all four SEA monarchy templates — so the five-pair Srivijayan
ring (PLB → JMB/INR/SGT/BUS/PNI) ships with NO authored reform: gate
pattern #4 after the authored-khutba reforms, the tribe branch, and
the setup-assigned-reform-beats-validator law. Exposing it exposed the
HARNESS: the tributary-gate check read only the overlord block's
INLINE `reforms = { }` and looked the key up only in MOD reform files
— both blind because every earlier ring was mod-authored and inline.
The check now walks the overlord's include chain (NESTED, cached — the
welsh_releasable lesson again) and searches vanilla's
government_reforms too; proven both directions (the five PLB ties
flagged before the fix, green after; PLB removed from
`_MOD_TRIB_OVERLORDS` fails the vacuous-scan floor 73<78). Rider from
the same day: vanilla ships **11 legitimately EMPTY IO member lists**,
so "zero members" is not an error class — a sect DRAINED by our
landless sweep is, and no check noticed a hand-drained Burmese
Buddhism sect until the pinned-count check (9 empties, proven by
breaking) was added.
**Means:** before authoring a gate reform for a new tributary ring,
read the parties' template chains — vanilla may already pay the gate;
and any check that reads a country block's fields must follow
includes, or it sees only what vanilla chose to inline.

### Vanilla DATES its own anachronisms in IO creation_dates — and the future-date strip has been quietly correcting history since item 10

**Established:** Tibet slice review, 2026-08-02. The five Tibetan
`type = sect` instances carry vanilla's own founding dates — Kadam
`1030.1.1`, Kagyu `1050.1.1`, **Sakya `1073.1.1`**, Jonang `1120.1.1`
(`VAN/main_menu/setup/start/15_international_organizations.txt:1435
:1454 :1472 :1494`) — so the mod's future-dated-IO strip
(`build_setup.py`, `creation_date >= START_DATE`) had already deleted
the two post-1066 schools months before anyone researched Tibet,
leaving exactly the two that existed on 1066.9.15. The same date was
the strongest argument for retiring TIB itself (a theocracy capitaled
at a monastery vanilla says is founded seven years after start).
**Means:** an IO instance's `creation_date` is vanilla's own testimony
about when an institution begins — cite it before any external source
when arguing a tag or web is post-start; and when a theater "already
looks right", check whether the future-date strip silently did the
work, then write it down (this one went unrecorded for three weeks).
Corollary for situations: the deleted instances are DATED and intact
in vanilla's file — a script can re-create them on schedule (the
banked Second Diffusion situation re-adds Sakya in 1073).

### The emptied-but-unlisted delta guard does NOT catch an over-sweep whose donor survives elsewhere

**Established:** Tibet slice break-test (i), 2026-08-02 — the test
REFUTED its own package's prediction. Sweeping `u_area` whole (28)
instead of naming TIB's four provinces (25) takes POO's three
`pemako_province` locations — and NO guard fires: POO keeps its seven
Kham locations, so the delta guard (which only knows
held-land-then-emptied) stays silent, disjointness holds (the three
enter one list once), and exactly-once holds (each had one owner). The
build ran GREEN with stolen land. The only guard that catches the
mistake is the per-rule **exact-count assert** — which a designer who
mis-measured once will set wrong too (28 was "correct" for the wrong
design).
**Means:** the count assert is the ONLY line of defence against
taking land from a surviving donor, so a rule set's DONOR TABLE must
be verified against ownership (who loses what, summing to the
expected count per donor) at review time, every slice — the resolver
cannot know intent. When a package prints a donor table, reproduce
it; when it doesn't, demand it.

### A single-space registry regex misses 94 of vanilla's 2,340 identity blocks

**Established:** Americas package, 2026-08-02 — the anchor class's
FIFTH incident. `^TAG = {` (one space) returns 2,246 over
`VAN/in_game/setup/countries/`; vanilla's real count is **2,340**
(CLAUDE.md's own constant). The 94-block gap: 92 declarations use two
or more spaces (`HIR  = {`, `ZIP  = {` …) and 2 use a tab (HNV, YDR,
india.txt). Four of the 94 are American, and `ZIP` is LANDED — under
the strict regex it reported as holding land with no registry entry,
a phantom. The Perm/Vyatka package's "2,320 tags indexed" was this
regex (2,246 + 74 mod); its published freeness VERDICTS survive
(word-boundary scans catch collisions by count) but its registry
file:line column was blind to the 94. The loose form
`^([A-Z0-9]{2,6})[ \t]*=[ \t]*\{` reproduces 2,340/2,414 exactly.
**Means:** every registry scan uses the loose whitespace form, always
— joining BOM-behind-`^`, one-line blocks, trailing comments and
tab-anchored pops as the anchor class's members. A "no registry
entry" verdict from a strict scan is a hypothesis about the scanner
first.

### A vanilla `.info` file opens with a BOM-shadowed example block — and directory sweeps must enumerate `*.txt`

**Established:** 2026-08-03, pop-package review. `VAN/in_game/setup/
countries/00_readme.info` line 1 is a literal example block `TAG = {`
sitting BEHIND a BOM (`ef bb bf 54 41 47`). Two independent readers
mis-handled it the same morning, in opposite directions: a directory-wide
registry count that read *every file in the folder* returned 2,415
against the canonical 2,414 (the engine reads only `.txt`; `.info` is
documentation — 2,340 vanilla + 74 mod is the real registry), and a
`^`-anchored grep of the same file returned ZERO uppercase blocks
because the BOM sits before the anchor. One file, both blind spots of
the anchor class at once. The review's other instrument errata, for the
record: `_TAIFAS` values are `(capital, [locations])` tuples, not bare
lists — a reader that unions `values()` directly crashes.
**Means:** registry/database sweeps enumerate `*.txt` explicitly, never
"everything in the directory"; any surprising ±1 against a canonical
count is FIRST a question about the scanner's file list; and the
package-review law held again — of 180 reproduced checks the three
diffs were two draft bookkeeping slips (Bronze `define_pop` 50,052 not
46,119; `07_cities` has 1,023 location blocks not 1,129) and one
reviewer-scanner bug, with every load-bearing number exact.

## Template for new entries

```
### <short claim>
**Established:** how — a file:line, a measurement, an in-game observation.
**Means:** what changes because of it.
```
