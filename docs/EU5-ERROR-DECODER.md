# EU5 error.log — decoder

> **Purpose.** Every working session starts with log lines pasted from
> `Documents/Paradox Interactive/Europa Universalis V/logs/error.log`. Each
> signature below cost a real investigation once. Look it up here first; only
> grep vanilla when the signature is not in this table.
>
> **Every entry was decoded against a running game**, not inferred. Where a
> cause is still a hypothesis it says so.
>
> **Carried in from the Mongol Resurgence project**, where every signature below
> was decoded against a running game. The worked examples name that mod's files
> (`MR_*`, `MGO`, `MGE`) — they are kept deliberately, because a concrete case
> that actually happened is worth more than an abstract rule. Add this project's
> own signatures as they are decoded.

---

## How to read the log at all

- Two logs: `error.log` (script + GUI errors) and `debug.log`.
- Console `Log.ClearErrorLog` between checkpoints, console `error` to show.
- Prefix tells you the subsystem: `[game]` engine/database, `[cw]` Clausewitz
  core, `[cw_gui]` interface.
- **A silent load is not a working load.** The whole class this file exists for
  is content that loads without an error line *and without effect* — a wrong
  folder name, an unresolved loc key, a wargoal that does not cover the goal.
  The harness (`tools/verify_mod.py`) exists for those; the log only catches
  what the engine notices.

---

## Script errors

### `jomini_script_system.cpp:252 — Script system error! Invalid right side during comparison 'c'`
**Means:** a `c:TAG` on the RIGHT side of a comparison while that tag is not on
the map. Fires *every evaluation*, so a map mode can produce ~100k lines in a
few game-years.
**Fix:** identity → `tag = MGO` (plain string, never errors). Map modes →
`owner ?= { tag = MGO }` (block form resolves no link). Relations
(`is_subject_of`, `is_neighbor_of`, `top_owner`, `top_overlord_or_this`) →
put `country_exists = c:X` **in the same AND**, before the link; trigger ANDs
short-circuit.
**Related:** `owner = { … }` on an OWNERLESS location errors the same way —
always `owner ?= {`.

### `jomini_trigger.cpp:803 — is_in_scripted_geography: Inconsistent trigger scopes (country vs. location, province_definition, area, region, sub_continent, continent)`
**Means:** a location-scope trigger used in country scope, or the reverse. The
message names the trigger and both scope families.
**Fix:** know which family the trigger belongs to.

| Question | Country scope | Location scope |
|---|---|---|
| in this geography? | `has_presence_in = scripted_geography:X` | `is_in_scripted_geography = scripted_geography:X` |
| in this region? | `has_presence_in = region:X` | `region = region:X` |
| inside this realm? | `top_overlord_or_this ?= c:X` | `top_owner ?= c:X` (+ `has_owner = yes`) |

A country's seat is a location: `scope:C.capital ?= { is_in_scripted_geography
= … }`.

### `jomini_trigger.cpp:1673 — Illegal use of operator untyped at <file>:<line>, must be valid equality operator`
**Means:** that line is not a `key = value` pair at all. Almost always a
mangled line — a half-written statement, or a scripted edit that dropped the
left-hand side.
**Fix:** open the exact line. Ours were `scripted_geography:MR_geo_tibet` with
the `is_in_scripted_geography = ` prefix eaten by a bad regex. Brace counts
still balanced, so no other check caught it.

---

### `jomini_script_system.cpp:252 — Script system error! untyped trigger [ Scoped object of type 'country' is not valid (Country 'Country' (---)) ], Script location: <unknown>:0`
**DECODED — it is downstream of broken ruler data.**
**Was seen:** ~30,000 lines in ten seconds of play on a 1066 start against
vanilla's 1337 `setup/start`, filling `error.log` and five rotations. Never
during load; it began about five minutes into play. `---` is the null tag.
**Cause:** the setup data described people who did not exist yet. Once
`tools/build_setup.py` stripped the future-dated `ruler_term` chains and gave
every country a `ruler = random`, the flood **stopped completely** — confirmed
in game. Nothing else changed, so the ruler data was the whole of it.
**Fix:** do not leave a country holding a ruler the engine could not seat.

### `jomini_script_system.cpp:252 — Event target link 'dynasty' returned an invalid object, Script location: events/DHE/flavor_ENG.txt:4760`
**DECODED — the throne is empty; the "ruler" is an engine-generated regent
with no dynasty.**
**Was seen:** 5,812 lines in one session of the first Phase 2 slice, paired
with `Invalid right side during comparison 'dynasty'` at the same line, and —
whenever the player browsed England's event list — triplets of
`pdx_data_callstack.cpp:53` "Promote 'TARGET_DYNASTY' returned nullptr",
`pdx_data_localize_helper.cpp:290` FetchData failed, and
`pdx_data_localize.cpp:173` "Data error in loc string 'dynasty_equal'"
(91 of each).
**Cause:** vanilla's line 4760 is `dynasty = root.ruler.dynasty` inside an
`any_character` loop. Our five named rulers had not seated (no open
`ruler_term` — see KNOWLEDGE.md), England's throne held an engine-generated
regent with no dynasty, and every evaluation of that England flavor trigger
errored. The loc triplet is the same hole hit by tooltip rendering.
**Fix:** seat the ruler properly. The flood is a symptom, not the disease —
count it OUT of the error budget once the cause is understood, and expect it
to vanish when the throne is filled.

### `pdx_persistent_reader.cpp:289 — "Failed to read key reference: mr_railroad_on ..." / "MR_mongol_resurgence_auto_conquest_yes"` (4 lines at load)
**LEAD FOUND** — this is the signature HANDOFF once listed as
"`gamestate.cpp:133`, unexplained, no lead". The keys it fails to read are
**Mongol Resurgence's game rules**: the launcher/settings remember game-rule
choices from a playset that included that mod, and this playset does not.
Harmless to this mod; nothing in our files is involved. Expect it to clear if
game rules are re-saved without MR. The first three lines (empty key names,
`near line: 3/7/11`) are the same stale-settings block.

### `initialize_from_bookmark.cpp:410 — character <key> has no birth scripted`
**Means:** the character is being INSTANTIATED at game start and has no
`birth = <location>` field. Benign in itself — vanilla ships such characters
and the warning costs nothing. Its diagnostic value is WHO appears in it: a
character who should be unborn at the start date (e.g. `sco_william_the_lion`,
b. 1143, at a 1066 start) showing up here means the engine is instantiating
the future-born — which is what happened when ALL future death_dates were
stripped, and the game then hard-froze on the first unpause.

### Hard freeze on unpause, debug.log cut mid-word, no flood
**Was seen:** first unpause of a new game; last debug.log line
`CPauseGame::InternalExecute changing to fa` — cut inside the word. error.log
calm (~500 lines), no script spinning, no crash dump. A hang inside the first
tick, not a script error.
**Cause that time:** ~3,500 future-born characters resurrected by an
over-broad death_date strip (see KNOWLEDGE.md). If it recurs, ask what the
last data change made the ENGINE simulate more of.

### A dead-at-start ruler produces NO error at all
Not a signature — the absence of one, recorded because it cost a session.
A character alive at `START_DATE` carrying a post-start `death_date` starts
the game DEAD — reign closed on the start date, throne to a generated
regent — and error.log says **nothing**. The log even shrank (17,954 → 1,054)
while five thrones were broken. If a named ruler is mysteriously a regent,
check the character's `death_date` BEFORE reading the log; the log cannot
catch this class. `verify_mod.py` now does ("no future death_date in setup
characters").
`build_setup.py` asserts exactly one ruler per country for this reason.
**A hypothesis that was wrong, kept as a warning:** `ADULT_AGE = 16` made it look
certain that negative-age rulers would force every country into regency and spam
`in_regency_yearly_pulse`. The arithmetic was right and the conclusion was wrong
— the game showed no regency anywhere. Roughly 13 lines per country
(30143 / 2337) also looked like a per-country yearly pulse. Both were plausible;
neither was the mechanism. The signature was only ever closed by changing the
data and watching the log.

## Setup / database

### `pdx_persistent_reader.cpp:289 — Error: "Unexpected token: <invisible>, near line: N" in file: "setup/start/<file>.txt"`
**Means:** the file starts with a UTF-8 BOM and `setup/start/` does not tolerate
one. The parser reads `EF BB BF` as a token and abandons the file. In the log
the token prints as nothing at all, or as `ï»¿` if something decoded it as
Latin-1 — either way an "unexpected token" you cannot see in your editor is a
BOM until proven otherwise.
**Consequence is worse than an error line.** The file is silently inert; a
sibling project had it crash the game outright while loading a new game.
**Fix:** strip the first three bytes.
```python
raw = open(p, "rb").read()
open(p, "wb").write(raw[3:] if raw[:3] == b"\xef\xbb\xbf" else raw)
```
**Rule:** `main_menu/setup/start/` is the one BOM-free `.txt` tree — 25 of 25
vanilla files and 25 of 25 in a published conversion. Everywhere else wants the
BOM. `tools/verify_mod.py` now enforces both directions.
**Cost us a false conclusion once:** a probe file written with a BOM did nothing
in game, and the result was briefly read as "additive setup files cannot
redefine a country". The file had never been parsed. If a setup file appears to
do nothing, check its first three bytes before concluding anything about the
mechanism.

### `pdx_persistent_reader.cpp:289 — Error: "Future start date specified: <date>, near line: N" in file: "setup/start/10_countries.txt"`
**Means:** the start date was moved earlier than the setup data was written for,
so entries dated after `START_DATE` are rejected as being in the future. On a
1066 start against vanilla's 1337 setup this fires 6885 times in one load —
3738 "Future start date" and 3147 "Future end date" — almost all of them
`ruler_term` entries in the regnal history chains.
**Not a defines bug.** The calendar moved correctly; the data did not move with
it.
**Fix:** ship the affected countries' setup with dates at or before the start
date. Cannot be fixed by deleting vanilla's entries without a whole-file
override of `10_countries.txt`, and that empties the map — see the additive
approach in `docs/KNOWLEDGE.md`.

### `ruler_term_container.cpp:109 — Ruler term is active but there are subsequent ruler terms, please fix; TAG: <character> (start date: 1.1.1)`
**Means:** the downstream half of the signature above. When a `ruler_term`'s
dates are rejected as future, the term does not vanish — it collapses to
`start date: 1.1.1` and so reads as active from the beginning of time. Several
terms per country then claim to be active at once and the container complains.
`SPL` showed three at once (`sax_heinrich_the_proud`, `spl_welf_i_altdorf`,
`spl_welf_ii_altdorf`), all at `1.1.1`.
**The `1.1.1` in the message is the tell** — no vanilla file contains that date.
Seeing it means a date was discarded, not authored.
**Does NOT change who rules.** The current ruler comes from `ruler = ` in the
same government block, which is why a 1066 start still shows the 1337 monarch
rather than whichever term won the collision.

## Localisation

### `localization_reader.cpp:451 — Missing colon (:) separator at line N and column M`
**Means:** a loc entry is not `key: "value"` on ONE physical line. The entry is
**dropped entirely**, not just mis-rendered.
**Fix:** rejoin. Cause is nearly always a literal `\n` in a description that
became a real newline when the file was written by a script — escaping survives
exactly one layer, so build it explicitly (`chr(92) + "n"`) rather than counting
backslashes through a heredoc, a shell and a string literal.
**Guarded by:** harness check `loc lines are well formed`.

### `localization_util.cpp:103 — <key>: "Key With Spaces Instead Of Text"`
**Means:** the key has no localisation, so the engine invented a title-cased
string from the key itself. It is telling you the key it wanted.
**Fix:** add the key. Watch the engine-derived ones you did not write yourself:
`war_goal_<wargoal_key>` (+`_desc`) — with a wargoal named `MR_war_goal_x` that
is the double-prefixed `war_goal_MR_war_goal_x`; `rule_<key>`,
`setting_<option>` (+`_desc`); `hint_<key>` + `hint_<key>_hint_text`;
`STATIC_MODIFIER_NAME_/DESC_<key>`; `<situation_key>` + `_desc`;
`MODIFIER_TYPE_NAME_/DESC_<key>`.
**The trap that produced this here:** the keys existed — in
`in_game/localization/`. A mod loc file there with the same filename SHADOWS
the `main_menu` one, and every main_menu-only key renders raw. **All mod
localisation belongs under `main_menu/localization/<language>/`**; subfolders
are fine (vanilla has 414 files in them).

### `pdx_text_formatter.cpp:807 — Unknown formatting tag 'X'`
**Means:** `#X` markup the formatter does not recognise.
**Fix:** check your own text for stray `#` sequences and `|X]` specifiers.
**Confirmed vanilla-side here:** `'l'` appears when opening vanilla situation
panels too, with no mod loaded content involved. Before spending time on it,
open a vanilla panel and see whether it fires there as well.

---

## GUI

### `pdx_data_callstack.cpp:17 — No context supplied (Use SetDataContext), wanted context of type 'T' for 'T.Method'`
plus the downstream trio `pdx_gui_data_manager.cpp:233 FetchData failed`,
`pdx_gui_localize.cpp:140`, `pdx_data_localize_helper.cpp:290`.

**Means:** a widget needs a datacontext of type `T` and no ancestor pushes one.
The cited `<file>:<line>` is where the widget lives, **not** where the mistake
is.
**Fix:** find who was supposed to push that context.
**The case here:** `one_country_header_template` declares `block
"CountryContext"` **twice** — once empty for the portrait, once carrying the
default `datacontext = "[Country.GetGovernment]"` for the ruler-title strip. A
single `blockoverride` replaces BOTH, so the strip received a Country where it
needed a Government and logged on every frame. Fix used:
`blockoverride "one_country_ruler_title_visible" { visible = no }` — hiding the
strip, which vanilla's `reformation.gui:88` does for its own reasons. It cost
nothing visible because every widget in that strip is gated on
`[Government.HasRuler]` and was already rendering blank.
**General lesson:** a `blockoverride` applies to EVERY block of that name in
the template. Read the template before overriding.

### `pdx_gui_factory.cpp:624 — '<name>' is not a valid widget/type/property`
**Means:** invented widget or property.
**Fix:** grep vanilla `.gui` for the name; zero hits means it does not exist.
Ours: `textbox_single` (the real one is `text_single`, 3926 vanilla uses) and
`progress` (a progressbar's fill property is `value`, with `min`/`max`).

---

## Database / registry

### `generic_action_ai_list.cpp:82 — Action X is not explicitly listed in an ai list! This has performance considerations!`
**Means:** no `in_game/common/generic_action_ai_lists/` entry, so the AI
re-evaluates the action far more often than it needs to.
**Fix:** one file with `potential = { … }` + `actions = { X }`. Shape:
vanilla `rise_of_timur_list.txt`.

### `price_database.cpp:117 — Missing modifier type for price. <price>_cost_modifier`
**Means:** declaring a `common/prices/` entry also implies a modifier TYPE
named `<price_key>_cost_modifier`.
**Fix:** add it under `main_menu/common/modifier_type_definitions/`:
`{ color=bad  percent=yes  game_data={ category=country } }`. Shape: vanilla
`hussite_wars_actions_price_cost_modifier`.

### `modifier_type.cpp:1294 — Missing Icon for Modifier: <key>`
**Means:** the modifier type has no icon **declaration**.
**Fix — no art required.** There is no `icon` field on the modifier type, and
it is not purely a filename convention either: icons are declared in
`main_menu/common/modifier_icons/` (vanilla ships 4912 entries):

```
<modifier_type> = {
	positive = "gfx/interface/icons/modifier_types/whatever.dds"   # >= 0, or the only one
	negative = "gfx/interface/icons/modifier_types/whatever.dds"   # optional, < 0
}
```

The path may point at **any existing `.dds`, including another modifier's** —
vanilla does exactly that (`build_hippodrome_price_cost_modifier` borrows
`expand_rgo`'s, `rot_reform_into_monarchy` borrows `rot_select_core_region`'s).
So borrow one and the error clears. There is also a `default = yes` entry in
the file, which is what you fall back to when nothing matches.

### `message_handler.cpp:421 — Failed to find message type: PERFORM_<action>_ACTION`
**Means:** a `type = situation` generic action sends a message when performed
and the message type is not registered. 149 of vanilla's 155 situation actions
register one.
**NOT FIXABLE IN A MOD.** The engine reads exactly one file for these,
`main_menu/gui/messagetypes.txt`, with 1348 vanilla entries. A differently
named file in that folder is silently ignored — verified: vanilla ships no
second `.txt` there, and a large published mod ships one that is dead. A file
with THAT name replaces all 1348.
**Accept:** one log line when the action fires, and no popup. The action works.

### `country_database.cpp:98 — <TAG> has the name 'empire' in it, which does not work for a tag, which would look silly as 'The Great TAG Empire Empire'`
**Means:** a country name containing "Empire". Rank titles compose as
`<prefix> <adjective> <rank noun>`, so the word doubles.
**Fix:** rename, or accept — it is a load-time cosmetic line. **Zero vanilla
country names contain "Empire".** Note the map label is built from
`<rank>_prefix` + `<TAG>_ADJ` + `<rank noun>` and never uses the country name
at all, so renaming may not change what you see on the map: an empire-rank
steppe horde reads "Great <Adj> Horde" whatever you call it.

---

## Separating your errors from vanilla's

Vanilla emits plenty of its own errors, and telling them apart costs real time
— `Unknown formatting tag 'l'` was investigated three times here before being
confirmed vanilla-side. A published project solves this with a maintained
filter list plus a watcher script that strips known-vanilla entries from
`error.log` and writes a clean copy. Their filter format is worth copying:

```
contains:<text>
exact:<full entry body>
regex:<python regular expression>
```

Their list is 663 lines for EU5 1.3. Building one for this project is cheap and
pays back the first time an unfamiliar signature turns out not to be ours.

## Adding to this file

When the game reports a signature that is not here, add a row **once you have
decoded it** — signature, what it actually means, the fix, and whether it is
fixable at all. If it turns out to be vanilla-side, say so explicitly and say
how it was confirmed; that saves the next session from re-investigating a
non-problem. Two entries above are exactly that.
