---
name: verify-vanilla-override
description: Decide correctly between editing one vanilla database entry and freezing a whole vanilla file, and prove nothing was silently dropped. Use before creating any file whose path and name match a vanilla file, before writing TRY_INJECT/REPLACE, and whenever a vanilla feature stops working after a mod file is added. A whole-file override deletes everything it does not repeat, with no error.
---

# Overriding vanilla without silently deleting it

A mod file whose **path and filename both match a vanilla file replaces that
file entirely**. Everything the vanilla version contained and yours does not is
gone. The engine reports nothing. The feature simply stops existing.

This is the most expensive silent failure available in a total conversion,
because a conversion touches vanilla databases constantly.

## The decision, in order

**1. Does a vanilla file share this exact relative path and name?**

```bash
V="/e/SteamLibrary/steamapps/common/Europa Universalis V/game"
# from the mod root, for the file you are about to create:
test -f "$V/<relative/path/to/file.txt>" && echo "OVERRIDES VANILLA" || echo "new file, safe"
```

Sweep the whole mod the same way when auditing:

```bash
find in_game main_menu -type f \( -name '*.txt' -o -name '*.yml' \) | while read f; do
  [ -f "$V/$f" ] && echo "OVERRIDES: $f  (vanilla $(wc -l < "$V/$f") lines vs mod $(wc -l < "$f"))"
done
```

If it does not overlap, stop — you are adding, not overriding. Prefer this:
**a new filename is almost always available**, and under `setup/` it is the
only option (see below).

**2. If it overlaps, can one database ENTRY be edited instead of the file?**

Under `in_game/common/…` the engine accepts operation prefixes on a key:

```
TRY_INJECT:castle = { important_for_AI = yes }      # add fields to a vanilla entry
TRY_REPLACE:call_parliament = { ... }               # replace one vanilla entry
```

Measured across 20 workshop mods: 599 `REPLACE:`, 295 `TRY_INJECT:`,
190 `INJECT:`, 116 `TRY_REPLACE:` — all of them under `in_game/common/`.
Conflict-resolution order reported by third-party docs:
`INJECT_OR_CREATE → REPLACE_OR_CREATE → TRY_INJECT → TRY_REPLACE → INJECT →
REPLACE`, by operation type first and filename second.

Two known limits:

- **Zero uses anywhere under `setup/`.** Country/character/pop data is not
  reachable this way; use a new filename in `setup/start/` instead.
- **First-match-wins files cannot always be fixed by injection.** In
  `customizable_localization/country_name_construction.txt` and
  `country_ranks.txt` the engine takes the first matching `text` block, so an
  appended branch lands *after* the one that already matched and never runs.
  There a whole-file override may genuinely be required.

**3. If a whole-file override is unavoidable, diff it and say what you lose.**

Never write the file from memory or from another mod's copy. Start from the
CURRENT vanilla file, then diff before committing:

```bash
diff <(tr -d '\r' < "$V/<path>") <(tr -d '\r' < "<path>")
```

Read every `<` line. Each one is vanilla content your file deletes. State them
explicitly in the report, then decide whether each is acceptable — not after.

## Why this exists

The Prussian Destiny whole-file-overrides
`in_game/common/customizable_localization/country_name_construction.txt` to add
one tag to one branch. Diffed against vanilla, its copy **silently deletes**
vanilla's `ROM_republic` and `BYZ_greek` naming branches. Anyone running that
mod loses the Roman republic and Byzantine Greek country names, with no error
anywhere and no way to notice except by reading both files side by side.

The same mod also ships `main_menu/setup/start/26_ai_personalities.txt` as a
full replacement. That one is currently correct — a `comm` of the entry keys
shows no vanilla personality dropped — but it freezes vanilla's version of that
file: any future patch that touches AI personalities is reverted for that mod's
users, and any personality Paradox adds disappears.

By contrast the same author's REAI mod does it right, with
`TRY_INJECT:castle = { … }` in `in_game/common/building_types/` and
`TRY_REPLACE:call_parliament` in `generic_actions/` — one entry each, vanilla
file untouched, patch-survivable.

## Report format

Categorised, and never write before approval:

- **overrides** — path, vanilla line count vs ours, and the diff's `<` lines
- **injectable** — could be `TRY_INJECT:`/`TRY_REPLACE:` instead, with the key
- **safe** — new filename, no vanilla collision

## Checks worth having in the harness

- every mod file path tested against the vanilla tree; each hit reported with
  its line-count delta
- for each override, a stored list of vanilla top-level keys, so a later edit
  that drops one fails the run rather than passing quietly
