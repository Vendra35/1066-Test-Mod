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

### 1178 over 867
**Established:** by comparing the delta from vanilla's 1337 setup.
1178 is 159 years from the shipped world — most tags exist, borders are
recognisable, Iberia is partly reconquered, Anatolia partly Turkish, the Baltic
crusades under way. 867 needs nearly every tag created and nearly every
location's culture and religion changed.
**Means:** the same project is roughly half the data entry at 1178. It is also
the Mongol-relevant date — Temüjin is born c. 1162, unifies in 1206.

### Regional depth first, not the whole map
**Established:** by looking at how two published total conversions ship.
One covers a era where most of the world is genuinely stateless, so an empty map
is historically honest. At 1178 the world is full, so that trick is unavailable.
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

### Timeframe moves via `common/defines`
**Established:** `START_DATE` / `END_DATE` overridden there in a published
conversion, with a documented reason for keeping the engine calendar positive:
vanilla timers, cooldowns, AI scheduling, situations, institutions and saves
assume positive years in several places.
**Means:** 1178 is positive so no display trickery is needed. Ages and advances
still need remapping — vanilla's ages begin at 1337.

### Country tags need not be three letters
**Established:** vanilla has 2217 tags and every one is exactly 3. A published
conversion ships 531 tags of which 471 are five letters and 47 are four, used
live in script (`c:ALASI`, `tag = ASYRI`).
**Not verified in a running game here.** Confirm before relying on it.
**Means:** if 3-letter uniqueness becomes painful across hundreds of new tags,
there is probably room. Test it early and cheaply rather than late.

---

## Open questions to settle early

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
