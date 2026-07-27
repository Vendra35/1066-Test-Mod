---
name: write-eu5-setup
description: Rules for writing anything under main_menu/setup/ — countries, characters, dynasties, pops, ownership. Use before creating or editing any setup file, when a setup change appears to do nothing in game, or when deciding between an additive file and a whole-file override. Encodes measurements taken against a running 1066 game, not guesses.
---

# Writing EU5 setup files

## Why this exists

`main_menu/setup/start/` is the world. It is also the part of EU5 that fails
most expensively: one wrong byte makes a file inert or crashes a new game, and
the mechanism questions have counter-intuitive answers that cost this project
several test cycles to establish.

Everything below was measured against a running game or counted in vanilla. Where
something is still inference it says so.

## Reference paths

Detect, never assume. Probe a known FILE — an empty directory passes a directory
test and makes every later grep return a confident zero.

```bash
STEAM_VAN="/e/SteamLibrary/steamapps/common/Europa Universalis V/game"
if [ -f "$STEAM_VAN/in_game/map_data/definitions.txt" ]; then
	VANILLA="$STEAM_VAN"
fi
BRONZE="/c/Users/Desktop/Bronze Era Modu Total Overhaul"   # published conversion
```

## RULE 1 — `setup/start` takes NO BOM

The single most expensive byte in this project.

| Tree | BOM |
|---|---|
| `main_menu/setup/start/` | **none** — 25/25 vanilla, 25/25 Bronze Era |
| `setup/templates/` | yes — 198/205 |
| `common/advances/` | yes — 215/215 |
| `common/situations/`, `common/on_action/` | yes — 23/23, 21/21 |
| `common/defines/`, `common/age/` | yes |

A BOM in a setup file is read as a token:

```
pdx_persistent_reader.cpp:289: Error: "Unexpected token: <invisible>"
in file: "setup/start/<file>.txt"
```

The file is then **completely inert**, and a sibling project had it crash the
game during new-game load. This once produced a false conclusion here — a probe
file "proved" that additive files cannot redefine a country, when in fact it had
never been parsed.

Write setup files without a BOM, and **check the first three bytes before
concluding anything about a setup file that appears to do nothing**:

```bash
head -c 3 "<file>" | od -An -tx1     # efbbbf means the BOM is there
```

`tools/verify_mod.py` enforces both directions. Its `no BOM in setup/start`
check is at `PENDING` while the repo ships no setup file — **raise it in the
same commit as the first one**.

## RULE 2 — the filename decides replace vs add

- **Same name as vanilla's** (`10_countries.txt`) → vanilla's file is replaced
  **entirely**. The wiki: *"A file in vanilla or in previously read mod can be
  entirely overridden by a file in the same directory and of the same name"* —
  **"even if the mod's `00_default.txt` is empty."** Observed here: overriding
  `10_countries.txt` by name emptied the map.
- **A new name** (`50_my_countries.txt`) → loads alongside, additively. Sort
  order matters, so number above vanilla's `27_`.

The wiki again: *"Most managers in the `setup/start` folder work in an additive
fashion… but makes it so that replacing entire files is required in order to
remove certain entries."*

## RULE 3 — additive files MERGE, but can never REMOVE

Measured in game, two rounds, on `ENG`:

| | |
|---|---|
| Redefines a vanilla country? | yes |
| Merge or replace the block? | **merge** — England kept all 145 locations |
| Beats vanilla's own `ruler = `? | yes |
| Can it delete vanilla's `ruler_term` entries? | **no** |

Corroborating: 175 of vanilla's 2337 country blocks declare `government = { … }`
twice within one block, the second adding only `mysticism_vs_jurisprudence`. If
the second replaced the first those countries would lose their government type.

**Decision rule.** Adding or overriding a value → additive file, cheap. Removing
an entry → whole-file override, and then you must restate everything you want to
keep, including `own_control_core`.

## RULE 4 — `ruler` seats the ruler; `ruler_term` is only history

```
government = {
	type = monarchy
	heir_selection = cognatic_primogeniture
	ruler = eng_edward_iii                    # <- who actually rules
	ruler_term = { character = eng_alfred_the_great start_date = 886.1.1 … }
}
```

The wiki: *"Government is also used to define who ruled the country before the
start of the game. It is used for regnal history and to decide regnal numbers."*

A sitting ruler's term carries **no `end_date`**. `inherit_ruler_terms = TAG`
copies regnal history from another tag.

**But `ruler = ` alone is not enough when the chain is wrong** — see rule 5.

## RULE 5 — entries dated after `START_DATE` collapse to `1.1.1`

Moving the start date earlier without rewriting setup produces, in one load:

```
pdx_persistent_reader.cpp:289: "Future start date specified: …"   (3738)
pdx_persistent_reader.cpp:289: "Future end date specified: …"     (3147)
ruler_term_container.cpp:109: Ruler term is active but there are subsequent
  ruler terms, please fix; TAG: <character> (start date: 1.1.1)
```

The rejected term is not dropped — it collapses to `start date: 1.1.1`, reads as
active since the beginning of time, and several per country then collide.
**`1.1.1` in a log line is the tell**: no vanilla file contains that date, so
seeing it means a date was discarded rather than authored.

Consequence measured here: a country whose chain is in this state **cannot be
given a working ruler additively**. Setting `ruler = ` displaces vanilla's
choice, but the container refuses to seat anyone and the engine generates a
regent instead. Appending our own `ruler_term` does not help.

The clean escape, and what a published conversion does: ship the country file
with **no `ruler_term` entries at all** and `government = { ruler = random }`.
That removes every future-dated entry, so all three signatures disappear and
rulers are generated at sane ages.

## RULE 6 — ordering: what is real and what is folklore

- Dynasties must exist in `dynasty_manager` **before** characters referencing
  them (wiki).
- "Children after parents" is **not enforced by the engine.** Vanilla's own
  `05_characters.txt` opens with *"Remember to write sons and daughters ALWAYS
  after their parents to avoid crashes"* and a published conversion repeats it —
  yet vanilla itself ships **614** characters naming a parent declared later, and
  the game runs. Keep your own additions ordered because it is free, but never
  fail a build over vanilla's ordering.
- Vanilla also ships **8 dangling parent references** and one `father = random`,
  which is a legal value, not a broken name.
- **The general rule this produced: validate what we wrote strictly, report what
  vanilla shipped.** A check that fails on Paradox's data blocks our work over
  someone else's bug.
- `birth_date` may be negative even when `START_DATE` is positive — Bronze Era
  runs `START_DATE = "1.1.1"` with `birth_date = -54.1.1`.

## RULE 7 — names come from `common/languages/`, not imagination

`first_name = { name = name_X }` only works if `name_X` is defined in
`in_game/common/languages/`. There is **no `name_harald`** in the game; vanilla
uses `name_harold` for both, which is why `eng_harold_godwinson` carries it.
A missing name key produces a nameless character and no error.

```bash
grep -rn "name_harold" "$VANILLA/in_game/common/languages/"
```

## Field reference

Ownership keys, all taking a location list:
`own_control_core`, `own_control_integrated`, `own_control_conquered`,
`own_control_colony`, `own_core`, `own_integrated`, `own_conquered`,
`own_colony`, `control_core`, `control`, `our_cores_conquered_by_others`.

The last one is claims WITHOUT territory — a landless claimant tag has only
that. Do not read its presence as ownership.

Country file skeleton:

```
current_age = age_1_traditions        # starting age, stated in setup

countries = {
	countries = {
		TAG = {
			own_control_core = { location_a location_b … }
			capital = <location>
			country_rank = rank_duchy   # verify the enum against vanilla
			include = "<template>"      # setup/templates/<template>.txt, key IS the filename
			government = { … }
		}
	}
}
```

## Before writing, and after

1. Confirm every location, tag, culture and religion name resolves — see the
   `verify-tags` skill. A wrong name does not error, it silently does nothing.
2. Confirm every field against vanilla or `docs/EU5-Vanilla-Script-Docs/`, in
   the same position and scope. `docs/Setup modding - …pdf` is a source, not the
   authority; it carries a *"last verified for version pre-release"* banner. Read
   it with `pdftotext -layout "<file>.pdf" -` and scope the section with awk.
3. No BOM. Tabs. English comments.
4. Run `tools/verify_mod.py`.
5. Only in-game observation is evidence that it worked. Check `error.log` and
   `debug.log`; decode signatures with `docs/EU5-ERROR-DECODER.md` first.
