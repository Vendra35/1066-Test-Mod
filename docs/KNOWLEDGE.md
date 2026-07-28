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
   without, the visible cases are PU juniors whose terms live in the senior
   partner (WLS with `ruler = eng_edward_iii`, via `inherit_ruler_terms`),
   tribes and theocracies. Whether the remainder actually seat at 1337 is
   unmeasured — do not cite them as counter-examples without testing one.
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
effect). The architectural answer was already paid for in our own Mongol
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

### A wrapping expanding vbox spreads situation cards apart
**Established:** screenshot, round 3 — the two cards sat at opposite ends
of the panel. MR's fuller gui wraps its MANY cards in an expanding vbox;
with only two cards the free space lands between them. Vanilla's
`rise_of_the_ottomans.gui` (the readme's recommended base) puts its two
cards DIRECTLY in the `situation_panel_main_content` blockoverride.
**Means:** no wrapping vbox for few-card panels; cards as direct siblings.

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
