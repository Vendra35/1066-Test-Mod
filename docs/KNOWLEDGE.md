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

### Regional depth first, not the whole map
**Established:** by looking at how two published total conversions ship.
One covers a era where most of the world is genuinely stateless, so an empty map
is historically honest. At 1066 the world is full, so that trick is unavailable.
**Means:** first playable target is one region at full fidelity with the rest
left vanilla-ish. Expand region by region. Do not gate a playable build on
global coverage.

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
**Not verified in a running game.** Which trees the engine actually reads for
`START_DATE` is unknown.
**Means:** we mirror all three, identical, because a start date that silently
stays 1337 is the worse failure mode. `verify_mod.py` enforces agreement. If a
duplicate-define warning ever appears, drop the two and keep `loading_screen`.
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
- **Database operation prefixes.** `TRY_REPLACE:existing_key = { … }` appears to
  modify a vanilla entry instead of replacing its file. Zero uses in vanilla,
  22 in a published mod. Reported order:
  `INJECT_OR_CREATE → REPLACE_OR_CREATE → TRY_INJECT → TRY_REPLACE → INJECT →
  REPLACE`. If this works it is the way out of whole-file overrides. **Test it.**
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
