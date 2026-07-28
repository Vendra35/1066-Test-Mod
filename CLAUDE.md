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

This file holds the RULES. Current state and architecture live in
`docs/HANDOFF.md`: Phase 1 is built, measured in a running game, and generated
by `tools/build_setup.py`; the first Phase 2 slice (five North Sea rulers) is
written but not yet observed in game. Read this file, then `docs/HANDOFF.md`,
then `docs/KNOWLEDGE.md`, in that order, before writing anything.

**Scope: the whole map, historically, in two phases.** The target is a real
overhaul — every region at 1066, not one region deep and the rest borrowed. That
is a large target, so it is reached in an order where the world is playable
throughout rather than at the end.

**Phase 1 — make the world work.** Override `main_menu/setup/start/10_countries.txt`
wholesale, built on Location Painter's vanilla template so no territory is lost,
carrying **no `ruler_term` entries at all** and giving every country
`government = { ruler = random }`. That single change clears all three defects a
1066 start currently has: rulers aged about -250, 6885 "future date" parse
errors, and the `ruler_term_container` collisions. The world ends up full,
correct in extent, and playable — just not yet peopled by the right individuals.

**Phase 2 — make it historical.** Replace `ruler = random` region by region with
real rulers, characters and dynasties, adjusting territory where 1066 differs
from 1337. Each region is independent and each is a shippable increment.

Two things keep this honest. Phase 1 is a prerequisite, not a shortcut: skipping
it means no playable build until every ruler is written, and vanilla only
supplies 188 characters who are adults in 1066 against 1566 countries holding
territory. And Phase 2 is where "historically" is actually earned — a region is
not done because it has borders, it is done when the people on the throne are
the people who were there.

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

### Everything else that is already available — look here before asking

Nothing in this list has to be re-derived. `docs/KNOWLEDGE.md` carries the full
table with what each is good for.

| Where | What |
|---|---|
| `docs/EU5-Vanilla-Script-Docs/` | **the authority** — every legal trigger, effect, scope link, modifier tag, on_action, and the GUI data types |
| `docs/*.pdf` | 34 wiki pages saved offline: Setup / Country / Character / Event / Situation / Action / Law / War / Localization / Mod structure modding, plus every continent and subcontinent |
| `C:\Users\Desktop\eu5-modding-project-1.3.11\…` | 11,631 files — `reference_official_defines/types/` (14 official type files), `reference_mods/` (20 workshop mods), a full 1.3.11 game copy, and an error-log filter with 663 known-vanilla signatures |
| `C:\Users\Desktop\Bronze Era Modu Total Overhaul` | published conversion — the attested way to move `START_DATE` and rebuild `setup/start` |
| `C:\Users\Desktop\Anno 1644 The General Crisis Modu Total overhaul for 1644` | published conversion — the SECOND attested `START_DATE` move (forward, to 1644.4.17), defines in `loading_screen` only, additive `zzz_`-prefixed setup files layered over overrides |
| `C:\Users\Desktop\Basileia Romaion 1337 total overhaul modu çok popüler` | popular published 1337 total overhaul — mass character/dynasty authoring, additive `05_br_characters.txt` shipped NEXT TO an overridden `05_characters.txt` |
| `C:\Users\Desktop\Rise of Timur Another Railroad Mod Example` | published railroad mod — runtime `found_dynasty` route instead of setup dynasties; see KNOWLEDGE.md |
| `C:\Users\Desktop\Location Painter` | the Location Painter tool itself, plus `EU5_Location_Painter_User_Guide.html` |
| `mod/Mongol Resurgence` | own mod — situation/state-machine/failsafe shapes, a mature harness, a nine-session test log |
| `mod/867 Total Conversion Test Mod` | own earlier attempt — its `EU5_MOD_MEMORY.md` found the setup BOM crash before this project did |

PDFs are read with `pdftotext -layout "<file>.pdf" -`, scoped with awk. The Read
tool cannot render them here. **The wiki is a source, not the authority** — it is
banner-marked "last verified for version pre-release" and its Country modding
page is visibly thinner than the game. Where it and the script docs disagree, the
script docs win; where it and vanilla source disagree, vanilla wins.

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
- Files: UTF-8 **with BOM** for `.txt` and `.yml` — with two exceptions, both
  measured against vanilla, both enforced by the harness:
  - `.gui` carries no BOM (vanilla ships 483 and only 49 have one).
  - **`main_menu/setup/start/` carries NO BOM.** All 25 vanilla files there are
    BOM-free, and so are all 25 of a published conversion's. Everywhere else is
    the opposite: advances 215/215 have one, templates 198/205, situations
    23/23, on_action 21/21, defines and age 1/1. A BOM in a setup file is not a
    silent failure — the parser reads it as a token and gives up on the file
    (`pdx_persistent_reader.cpp:289`, "Unexpected token"), and in one recorded
    case crashed the game while loading a new game. This project shipped exactly
    that bug once, because this rule used to say "BOM for .txt" with no
    exception.
- English only, including comments. Tabs for indentation.

### Scope, tags and names — three things that fail quietly

**`prev` is exactly ONE scope hop, and only scope-CHANGING blocks count as
hops.** `if` / `limit` / `AND` / `OR` / `NOT` are transparent, so the nesting on
screen is not the nesting `prev` walks. Two hops down —
`c:X = { … situation:Y = { var:target = { … prev } } }` — it lands on the
*situation*, and the engine says so precisely: `Left side and right side during
comparison were of different types (left was 'country', right was 'situation')`
(`jomini_script_system.cpp:252`). This shipped in all three phases of Mongol
Resurgence, inherited from a reference mod that had it too, and it is RARE in
the log because the gate above it short-circuits nearly every tick — testing
will not surface it. Going up more than one hop: `save_scope_as` + `scope:x`,
never `prev.prev` (zero vanilla uses). Mongol Resurgence's harness has a scope
walker with a canary for this; port it.

**A tag that is DEFINED but holds no land is brought onto the map by
`change_location_owner` alone.** No formable, no `create_country_from_location`.
Vanilla revives SKE — landless at 1337, identity-only block in
`setup/countries/_scandinavia.txt` — with a plain
`location:asbo = { change_location_owner = c:SKE }`
(`events/DHE/flavor_swe_dan.txt:4`). The `culture_definition` and
`religion_definition` fields in a `setup/countries` block exist precisely so the
engine can instantiate a tag that comes into existence later.
`create_country_from_location` (`effects.log:1230`) is the OTHER tool: it makes
a country with a GENERATED tag, which is what vanilla wants for Red Turban
splinters and wokou republics and what you do NOT want when the successor must
be recognisable. Choose by whether the new country needs an identity.

**A country's displayed name may never read its NAME key.** Name is composed by
`common/customizable_localization/country_name_construction.txt`, first matching
branch wins, and one of those branches is `government_type = steppe_horde` →
`"$PREFIX$ $ADJ$ $RANK$"`. So a horde's map name is built from its ADJECTIVE and
its RANK word and the NAME key is never consulted. RANK is itself chosen by
`country_ranks.txt`, also first-match: `rank_empire_horde` sits at line 306 and
the plain `rank_empire` fallback at 625. Editing the NAME key of such a country
does nothing at all, with no error. This matters here more than in a normal
mod — 1066 is full of tribes, hordes and theocracies, and every one of them may
compose its name from somewhere other than where you are looking.

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

**When a check reports "not referenced", verify the CHECK's coverage before
trusting it.** A reachability check is only as good as the syntaxes it knows.
Ours matched `trigger_event_silently = X` and missed the delayed block form
`trigger_event_silently = { id = X years = N }` — it then reported 11 healthy
events in another mod as never fired, and the same blind spot exists in the
ENGINE's own load-time validator, which calls such an event `orphaned` while
vanilla itself ships 812 events fired only that way. Two independent validators
were wrong about the same construct. So: an unreferenced-looking thing is a
hypothesis about the checker first and about the code second.

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

## Division of labor — the main session designs, subagents produce

The main session runs Claude Fable 5. `.claude/settings.local.json` sets
`CLAUDE_CODE_SUBAGENT_MODEL=claude-opus-5`, so every subagent it launches runs
Claude Opus 5 — verified live by having an agent report its own model ID. The
split is deliberate:

- **Main session (Fable):** the plan, engine constraints, trigger/scope logic,
  the shape of every situation, everything in the FORBIDDEN-from-memory
  categories, and final review of anything that enters the repo.
- **Subagents (Opus):** volume — per-region historical research (who ruled
  every tag in 1066), bulk setup data entry, localisation, mass audits and
  cross-reference sweeps. Routine hundreds-of-lines writing is delegated, not
  done inline in the main session.
- **Delegation relaxes nothing.** A subagent prompt names the exact reference
  paths to verify against and restates the rules that apply to its task
  (citation rule, BOM rules, verify-tags). Subagent output is a draft until
  the main session has reviewed it and `tools/verify_mod.py` has passed. A
  subagent claim without a `file:line` is an unverified claim.

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
