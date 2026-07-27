# CLAUDE.md — 1066 Test Mod (EU5 total conversion)

## What this is
A total conversion moving Europa Universalis V to **1066**, the best known of
the Crusader Kings III start dates. The opening decade carries itself: the
Norman Conquest lands in the first months, Manzikert is five years out, the
First Crusade thirty. Byzantium is still pre-Manzikert, Anatolia still Greek,
Iberia still taifa, the Baltic still pagan, Song China still whole.

867 and 1178 were both weighed and rejected — see `docs/KNOWLEDGE.md`. The short
version: 1178 is the cheapest date to build and 867 the most expensive, and 1066
was chosen on the strength of the setting with its cost accepted knowingly. That
cost is real and is written down, not glossed: EU5 puts everything before 1342
inside a single age, so 1066 spends 276 years in `age_1_traditions` and will
most likely need an age of its own eventually.

Nothing is built yet. This file holds the RULES. It does not describe an
architecture, because there is no architecture — that section gets written when
the first real systems exist, and is updated as a by-product of each change.

**Scope discipline:** the first playable target is regional depth, not global
fidelity. A world where one region is fully realised and the rest is
vanilla-ish ships in months; "the whole map at 1066 fidelity" does not.

## REQUIRED SETUP
Two read-only reference trees, both outside this repo. Detect, never assume,
and probe a known FILE rather than the directory — an empty folder passes a
directory test and makes every later grep return a confident zero.

```bash
STEAM_VAN="/e/SteamLibrary/steamapps/common/Europa Universalis V/game"
if [ -f "$STEAM_VAN/in_game/map_data/definitions.txt" ]; then
	VANILLA="$STEAM_VAN"
fi
```

Key vanilla paths used constantly: `in_game/map_data/definitions.txt`
(region → area → province → location), `in_game/map_data/location_templates.txt`
(what every location IS), `main_menu/setup/start/` (the world at game start),
`in_game/setup/countries/`, `main_menu/common/` (script values, modifier types,
game rules, modifier icons), `in_game/common/age/00_default.txt` (the six ages).

**Defines are NOT under `main_menu/common/`.** The only defines tree vanilla
ships is `loading_screen/common/defines/`, and `00_defines.txt` there is where
`START_DATE` and `END_DATE` live. This file said `main_menu/common/` until the
first session checked, which is exactly the kind of confident wrong path that
produces a folder the engine never reads and no error anywhere.

## Verification — read this before writing anything

**`docs/EU5-Vanilla-Script-Docs/` is the authority.** It is the console output of
`script_docs` and `dump_data_types` run against the shipped game:

| File | Contains | Look here for |
|---|---|---|
| `triggers.log` | 1798 triggers | Does it exist, and **`**Supported Scopes**`** |
| `effects.log` | 1534 effects | same |
| `event_targets.log` | 289 scope links | `Input Scopes:` → `Output Scopes:` |
| `modifiers.log` | 2436 modifier tags | Is this a real modifier |
| `on_actions.log` | every hook | `Expected Scope:` |
| `data_types/` | GUI/promote types | What `Country.`, `Character.` expose |

Look there FIRST. Grepping vanilla only ever shows what someone happened to
write; this shows what is **legal**. Regenerate after a game patch: launch with
`-debug_mode`, console `script_docs` then `dump_data_types`, copy the logs from
`Documents/Paradox Interactive/Europa Universalis V/`.

**Citation rule.** No field, effect or trigger enters a file without either an
entry in the script docs or a vanilla `file:line` using it *in the same
position and scope*. Existence is not enough — check scope, magnitude and
semantics. `add_mil` exists but is a **character**-scope skill effect.

**Categories where writing from memory is FORBIDDEN.** Go to the script docs or
vanilla source first, every time, no exceptions:
- any trigger's or effect's **scope**
- `blockoverride` block names and what the surrounding template declares
- GUI widget and property names, and `custom_tooltip` key formats
- any enum value (`location_rank`, `country_rank`, integration levels…)
- any modifier tag or modifier category
- any scripted trigger/effect not defined in this repo
- localisation encoding and the engine-derived key conventions

**Say what you verified.** Before writing in those categories, state it:
`Verified — <name>, <source file:line>, "<quote>"`. If nothing is found, say so
and stop rather than guessing.

**The citation rule applies to every source, including good ones.** Two
well-regarded external references were checked during setup and both contained
false claims — one used a construct with zero vanilla uses anywhere, the other
documented an enum as having three values when vanilla uses four. Published and
popular is not attested.

## Hard rules

### Silent failure is the default failure
Most mistakes here produce no error and no effect. The log only catches what
the engine notices; everything else needs a check.
- Verify directory names against vanilla before creating any folder.
- Every cross-reference must resolve: loc keys, rule options, hook names, gfx
  keys, hint tags.
- **ALL localisation lives in `main_menu/localization/<language>/`.** Never
  create `in_game/localization/`, and never ship two loc files with the same
  filename in different trees — the duplicate shadows the other and its keys
  vanish. A published total conversion has 20 files in exactly that state.
- Loc values must sit on ONE physical line. A literal `\n` that becomes a real
  newline splits the entry and the game drops it.
- Files: UTF-8 **with BOM** for `.txt` and `.yml`. `.gui` files carry no BOM
  (vanilla ships 483 and only 49 have one).
- English only, including comments. Tabs for indentation.

### When the game reports something
Decode it with `docs/EU5-ERROR-DECODER.md` before investigating from scratch;
16 signatures are already explained there, two of them as *unfixable, accept
it*. Add new signatures to that file as they are decoded, and say explicitly
when something turns out to be vanilla-side — that saves the next session from
re-investigating a non-problem.

### The harness
`tools/verify_mod.py` after every change. **Every check prints its item count**,
and a check that finds nothing to scan FAILS — a silent zero is the failure
mode this whole discipline exists to prevent. Three checks in the previous
project scanned zero files for weeks while reporting clean.

**When the game finds something the harness did not, that is two commits: the
fix, and the check.** Prove every new check against a known positive — break
the fix, watch it fail, restore. A check never seen failing is untested.

**Raise `min_count` as content lands.** The harness ships with most checks at
`min_count = 1` and reports `SKIP` while the repo is empty, which is honest but
guards nothing. Every time a new KIND of content appears — the first situation,
the first event file, the first localisation file, the first scripted trigger —
set that check's `min_count` to roughly what the repo actually contains, so a
future deletion or a broken glob shows up as a vacuous scan instead of a quiet
pass. Do this as part of the same change that adds the content, not later.

### Human choice
Whatever the AI is railroaded into, a human player is asked. Conversions are
offered and refusable, forced wars come as a visible event with a postpone
option, failsafes are `is_ai`-gated on both sides and never take a player's
land, and a player's alliances are not dissolved without consent.

## Workflow
- **Never write to a file without approval.** Audit first, report categorised
  (definite / suspect / needs-decision), fix after approval, file by file.
- Nothing can be run here. Static verification is the only line of defence and
  must never be presented as a test result. Only in-game observation is
  evidence of behaviour.
- Search before building — vanilla very often already has the feature.
- Record durable knowledge in `docs/KNOWLEDGE.md` in the same response as the
  discovery, not when asked. Rules that generalise go to
  `docs/EU5-MODDING-GUIDE.md`; engine error signatures go to the decoder.

## Language
All code, localisation and comments in English. Conversation in Turkish.
