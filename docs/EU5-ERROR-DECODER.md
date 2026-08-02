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

### `jomini_script_system.cpp:252 — Event target link 'international_organization' returned an invalid object, Script location: common/country_interactions/demand_silver_tribute.txt:8` (also `demote_celestial_governor_to_vassal.txt:9`)
**DECODED — our IO strip, vanilla's script, zero impact. ACCEPT.**
**Was seen:** 56 lines at load (2026-07-28, the Sardinia test session).
**Cause:** both are vanilla Celestial-Empire interactions probing
`international_organization:middle_kingdom`. Our 1066 build strips the
Middle Kingdom IO instance (`creation_date = 1271` — the future-IO strip,
18 instances). Vanilla even guards with
`exists = international_organization:middle_kingdom` on the line above
(`demand_silver_tribute.txt:6`), but the engine still logs the link
evaluation at line 8. The interaction is correctly HIDDEN — there is no
Middle Kingdom in 1066 — so the error is cosmetic.
**Fix:** none possible on our side short of overriding vanilla interaction
files, which is not worth it. Count these lines OUT of the error budget.

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

### `pdx_data_callstack.cpp:17 — No context supplied (Use SetDataContext), wanted context of type 'UIAction' / 'RequirementsList'` — flood while a situation panel is open
**Was seen:** hundreds of lines, all naming vanilla's shared guis
(`location_tooltips.gui`, `main_menu_cooltip_types.gui`), while the first
Norman Conquest build's situation panel was on screen — EMPTY.
**Means:** a situation is missing its per-situation GUI file. The panel
renders blank and every hover spams context errors from the shared tooltip
code. The requirement is documented in vanilla's own
`in_game/gui/panels/situation/readme.txt`.
**Fix:** ship `in_game/gui/panels/situation/<situation_key>.gui` — Mongol
Resurgence's 45-line template is the proven minimal shape. No BOM on .gui.

### `pdx_data_callstack.cpp:53 — Promote 'GetWinnerCountry' returned nullptr … loc string 'WAR_WON_OTHER_COUNTRY'` — burst when a scripted war ends
**DECODED — harmless.** A war ended by script effect (`leave_all_wars_with`,
`force_union`) has no peace treaty and therefore no winner; the "war won"
notification toast still tries to name one and its loc fetch fails. Seen
when the two 1066 setup wars wound down (Stamford withdrawal, the
Christmas union). The game continues normally. Count it OUT of the error
budget; no fix is warranted unless the toast itself starts bothering
players.

### `initialize_from_bookmark.cpp:792 — Character has too many ruler traits! … Traits: '2', Expected: '1'`
**DECODED — vanilla data, exposed by seating.** Vanilla gives some
characters two `ruler_trait` lines (`fcb_guillaume_i_burgundy`: righteous
AND expansionist, 05_characters.txt). At 1337 they are dead and nobody
notices; seat one as a 1066 ruler and the engine complains once at init.
Harmless — validate what we wrote, report what vanilla shipped.

### `initialize_from_bookmark.cpp:1659 — Country X has a child as a ruler`
**DECODED — expected companion of MINOR_RULERS.** One line per country
whose seated ruler is under 16 at start (FRA with the 14-year-old
Philip I, plus the odd random-roll child like AOS). Measured in game: the
child SEATS and RULES directly — no regency fires, matching the earlier
negative-age measurement. Informational, not a defect.

### `country_manager.cpp:206 — Unknown country 'X' referenced. Please add it to setup/countries/_countries.txt`
**DECODED — the tag is not registered.** The suggested file does not
exist in vanilla; the REAL registry is the `in_game/setup/countries/`
folder's identity blocks (color/color2 + culture/religion_definition per
00_readme.info). Without one, the tag's whole 10_countries block is
rejected: the parser then reports "Unknown country 'government'",
"'ruler'", "'ruler_term'"… (the block's own keys read as tags) plus
"Unexpected token" per line, and the tag's locations sit OWNERLESS on
the map. Measured on the Pereyaslavl probe's first launch; fixed by the
additive registration file.

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

### "invalid subject" / "non-existent overlord" flood at game start (~318 lines, 2026-07-28)
**DECODED — dependencies naming a landless tag; FIXED at the generator.**
**Was seen:** after the Byzantium batch, before the landless-dependency
strip landed. Exact engine wording unconfirmed (the log was overwritten
by the next launch) but the scale matched the measurement: exactly 28
kept dependencies named at least one of the 48 landless tags (the
Frankokratia vassal chains, the beylik webs, Armenia's relations).
**Fix:** `build_diplomacy` strips any dependency whose `first` or
`second` is in `LANDLESS_AFTER`, exact-count asserted at 28. Every
partner freed by the strip (Syunik, Khachen, Salona…) was historically
independent at 1066. If this flood reappears, a NEW landless tag
probably joined LANDLESS_AFTER without the count being re-checked —
the assert will already have said so at build time.

### `government.cpp:3535/3662 — Removing invalid law / estate privilege '<X>' for '<TAG>' at game start`
**DECODED (2026-07-29) — engine self-healing with three distinct
sub-classes; the line names a missing PREREQUISITE, not noise.** (An
earlier version of this entry declared the class "gone" after the
dependency strips — half right: the dependency-correlated flood went,
this residue stayed and decodes differently.)
1. **Missing has_policy prerequisite (ours, FIXED):** ABS shipped
   `sharia_law = hanbali_policy` without `legal_code_law =
   sharia_law_policy`; the sharia_law group's potential failed and the
   whole law was removed. Ship the prerequisite policy in the same
   block.
2. **Coastal template on an inland country (ours, FIXED):**
   `sponsor_maritime_contracts` removed for every inland new block —
   the flagged list IS the inland set. Use the template's `_no_coast`
   variant (vanilla ships one for every family; diff it first — the
   muslim no_coast variant drops heir_selection too).
3. **Landless shells (accepted):** education_masses_law / dhimmi and
   road privileges removed for landless tags (FAL, BDS, CIL, CND, the
   beyliks…). Their vanilla blocks carry laws whose prerequisites need
   land/pops; the engine trims them on our landless shape. Harmless,
   the tags are dormant; no data fix.

### `government.cpp:3612 — Removing invalid reform 'french_ducal_vassal_reform' for '<TAG>' at game start`
**DECODED (2026-07-29, via tools/scan_log.py's first triage) — the
France slice's 27-vassal strip made the reform invalid on the
ex-subjects; the engine self-heals.** AUM/ROU/RET/BRR/MDM and the
other former French vassals carry `french_ducal_vassal_reform` in
their 1337 blocks; its potential wants a French subjection our strip
removed. Same self-heal family as 3535/3662 — the line names the
missing prerequisite (the vassalage), the tags run fine without the
reform. ACCEPT; if the reform's bonuses are ever missed, the France
polish pass can swap blocks instead. which does not work for a tag, which would look silly as 'The Great TAG Empire Empire'`
**Means:** a country name containing "Empire". Rank titles compose as
`<prefix> <adjective> <rank noun>`, so the word doubles.
**Fix:** rename, or accept — it is a load-time cosmetic line. **Zero vanilla
country names contain "Empire".** Note the map label is built from
`<rank>_prefix` + `<TAG>_ADJ` + `<rank noun>` and never uses the country name
at all, so renaming may not change what you see on the map: an empire-rank
steppe horde reads "Great <Adj> Horde" whatever you call it.

### `government.cpp:3702 — Subject type 'tributary' is invalid for '<TAG>' at game start … Reason: file: common/subject_types/tributary.txt line: 20 … 24`
**DECODED (2026-07-29) — the subject type's `visible` trigger binds at
game start, and a failing dependency is silently DOWNGRADED TO VASSAL.**
The Reason lines are literally the failing trigger's lines: tributary's
20-24 are the OR of overlord-steppe_horde / subject-tribe /
subject-steppe_horde / `modifier:allow_tributary_subject`. All nine
Seljuk clients logged this and arrived as vassals. Same cpp line as the
old French-appanage class (~25 of the 53-line baseline) — one decoder
entry, many subject types.
**Fix, CONFIRMED in game (2026-07-29 second launch):** give the
overlord the modifier the gate wants — `seljuk_khutba_reform`
(vanilla's own reform pattern, country_specific.txt:3917). A
setup-assigned reform's country_modifier applies BEFORE this validator
runs: all nine clients arrived as tributaries and their lines left the
log. **Known ours, parked for the China review:** CHA Champa and DAI
Đại Việt (tributary), and ~30 Guizhou-area tags whose `tusi` subject
type fails the same way (Reason: country_triggers.txt:1288-1298, a
scripted trigger leaning on the Middle Kingdom IO our strip removed).
**FIXED 2026-08-01 (Route B):** the tusi gate is on the IO's EXISTENCE
(`country_triggers.txt:1287`, OUTSIDE the OR the engine cites — the
engine's Reason line names 1288-1298 while the fatal line is 1287, one
above) — so no reform could substitute; the vanilla instance is
restored re-dated `1271.12.18 → 960.2.4`. NEXT LAUNCH: the CHA/DAI
lines and all ~126 tusi lines must be GONE.

### `country.cpp:9635 — Country CHI Yuán starts with <N> out of <M> accepted or tolerated cultures…` + `ACCEPTED_CULTURE_SETUP_ERROR_IF_ABOVE_MAX` culture-list tooltip
**DECODED (2026-07-29, third Seljuk launch) — our Middle Kingdom strip
again; CHI lost the IO leader's +50 culture capacity.** The Middle
Kingdom IO's `leader_modifier` is where BOTH lost pieces live
(`middle_kingdom.txt:69-75`): `cultures_capacity = 50` — without it
CHI's capacity collapses to 6 against its 56.45-cost accepted/tolerated
list, hence this line — and `allow_tributary_subject = yes`, which is
why CHA/DAI downgrade to vassal (the 3702 class) as well. One removed
IO instance, three symptoms: this flood, the CHA/DAI tributary lines,
the ~30 `tusi` lines (country_triggers.txt:1288-1298). All parked for
the China review; the fix there is restoring an equivalent modifier
source for 1066 China (an ABS-style setup reform is the attested
shape), not patching tags one by one. Count these lines OUT of the
error budget until that review.
**FIXED 2026-08-01 — but NOT by a reform:** the review measured that
the tusi third of the triple is gated on the IO's *existence*, which
no modifier can satisfy, so the fix is the Middle Kingdom instance
RESTORED re-dated to 960.2.4 (the Song founding [U]) — the
leader_modifier and its `cultures_capacity = 50` +
`allow_tributary_subject` return with it. NEXT LAUNCH: this flood must
be gone entirely.

### `country_specific.txt:2063-2071 — JAP's shogunate reform invalid at start` (the JAP half of the old "~25 invalid reform" class)
**DECODED 2026-08-01 (India/China review, re-verified).** HANDOFF's
old 48-error table blamed `ruler = random` for the whole
appanage/imperial-reform class; the JAP half is actually the
`shogunate` reform's allow AND locked blocks both requiring
`is_leader_of_international_organization = international_organization:
japanese_shogunate` (`country_specific.txt:2067`, `:2069-2071`) — an
IO created 1192.1.1 that our future-date strip removes. No 1066 state
can ever satisfy it.
**Fix, FIXED same day:** `FIELD_FIXES["JAP"]` swaps the reform to
`japanese_imperial_family` (`:1952`) — whose own locked block
(`:1968-1976`) demands a `yamato_dynasty` ruler with NO tag
alternative, so vanilla's Go-Reizei (41 at start, resurrected by the
death-strip) is seated as a mandatory pair. NEXT LAUNCH: the JAP
reform line must be gone; Go-Reizei on the throne.

### `initialize_from_bookmark.cpp:528 — Country '<TAG>' does not know its capital, need a discover_areas = or discovered_regions = .`
**DECODED+FIXED — the block has no discovery source CONTAINING its
capital.** Playing such a country shows terra incognita over its own
land. Trap: `expl_silk_road_center` is an ALL-COMMENT vanilla template,
so including it grants nothing. Fix: `expl_middle_east` (vanilla's
132-use bundle for the theatre) on every generated Mideast block, and
`build_setup.py` now asserts every new block's capital is a member of
some granted region/area/province (resolved via definitions.txt).

### `initialize_from_bookmark.cpp:517/520 — heir-selection does not match government / no religious_school specified`
**DECODED+FIXED — both were the monarchy include under ABS's theocracy,
plus schools omitted from three client blocks.** ABS is an explicit
theocracy block now (heir_selection = theocratic_elective); a school of
None fails the build. The pair is a smell for "government type bolted
onto a mismatched include".

### `government.cpp:687 — Setting a law - <law> - … at game start that the country doesn't have the advance for`
**DECODED+FIXED — same root as above:** the muslim-monarchy template's
`feudal_de_jure_law`/`royal_court_customs_law` have no advances under a
theocracy. Gone with ABS's explicit block. If seen again: the block's
laws come from a template written for another government type.

### `diplomacy.cpp:4796 — Country with multiple overlords` + `pdx_assert.cpp:214 — Important assertion failed`
**DECODED+FIXED — two dependencies name the same subject.** HLL held
vanilla's Mongol-era HLG vassalage (which survived the landless strip —
HLG still holds kazimah) plus our SEL tributary. Repeats every few
ticks. `build_diplomacy` strips the HLG line, exact-count 1. If seen
again: grep 12_diplomacy for `second = <TAG>` and count.

### `country.cpp:6166 — primary culture is duplicated in accepted cultures for <TAG>`
**DECODED+FIXED — the registry's `culture_definition` IS the landed
tag's primary culture, and a setup `accepted_cultures` list repeated
it.** ARA: registry catalan + our accepted { catalan }. Fixed by the
attested registry override route (our iberia.txt, one line, catalan →
aragonese). This line is also the measurement that closed the deferred
"does culture_definition matter for a landed tag" question: it does.

### `initialize_from_bookmark.cpp:398 — Location <X> has an invalid building <B>`
**DECODED (2026-07-29, the France+British launch) — ownership/capital
changes strand owner-conditioned buildings; cosmetic.** Six lines:
rodos order_headquarters (KNI went landless, Rhodes is BYZ's),
valladolid chancery+sergeantry (CAS's capital moved to burgos),
lisbon sergeantry (BDJ's now), bursa sergeantry (BYZ's), dunbar peel
towers. The building sits in the location; the new owner fails its
condition; the engine reports and moves on. Same family as the
first-class `tag = X location = L` law in KNOWLEDGE — do not "fix"
07_cities. ACCEPT; a future buildings pass may tidy.

### `initialize_from_bookmark.cpp:205 — The releasable country '<TAG>' has no pops of its defined culture ... in its core locations`
**DECODED (2026-07-29) — landless shells whose culture_definition has
no matching pops under their claims; vanilla ships the same class
itself.** Eight lines: our ATQ/SUT/JKR/KHF/ART (Mongol-era shells over
re-cultured ground), our CMS/EWY (English marcher shells over Welsh
pops) — and vanilla's OWN 'ATH Athens' (catalan over Greek pops, the
1311 Catalan duchy). Informational; the tags are dormant irredenta.
ACCEPT.

### `initialize_from_bookmark.cpp:237/:301 + country.cpp:9778 — primary-vs-pop culture mismatches, discriminated estate cultures, DUB fort limit`
**DECODED (2026-07-29) — the POP PHASE's debt made visible; the
strategic order's "territory first, pops later" printing its bill.**
The estate-culture mechanics derive estate cultures from POPS, and
our territory moved without them: GDD/MWG nobles read `english` (the
marcher-era gentry pops), DUB's upper class reads `anglo_irish` (the
1337 Pale pops) against a norse_gael primary, GLC reads portuguese,
HLL iraqi-vs-hijazi is vanilla's own registry choice. DUB also
inherits the Pale's forts (2.5/1.2 fort limit, country.cpp:9778).
ALL of it is the pop-conversion phase's work — user-diagnosed
correctly at first sight, recorded so nobody re-investigates. ACCEPT
until that phase.

### `cabinet_effects.cpp:44 — Tried to add blocked character <name> to a cabinet in <TAG>`
**DECODED (2026-07-29) — 1337 scripted cabinet appointments hitting
1066; three lines (CHI, MAJ Gajah Mada, BYZ).** Vanilla setup/script
seats named 1337 cabinet members; at our date they are dead, unborn
or otherwise blocked and the engine refuses them. Same poison class
as the stripped ruler_terms, but cabinet lines live outside our
generated files. Cosmetic — the cabinets fill with generated people.
ACCEPT.

### The `tusi`/tributary 3702 flood is ~128 lines, not ~30
**Correction (2026-07-29):** the China class decoded earlier
undercounted — the full load logs **128** `government.cpp:3702` lines
(126 `tusi` + CHA/DAI tributary), every one a Chinese/SEA tag broken
by the Middle Kingdom strip. Still ONE root cause, still the China
review's single item. Grep tip: the tag sits inside quotes —
`invalid for '<TAG> ` — a space-delimited filter misses every line.

### `initialize_from_bookmark.cpp:2477 — Army Based Country '<TAG>' can not create regiments at start, and will this shatter.`
**WATCH — side effect of our sweeps, not yet observed causing harm.**
HLG/QUN/SLD: Mongol-era army-based tags whose holdings the
Byzantium/Seljuk passes reduced to nearly nothing. The engine shatters
them at start; the Mongol tags are gone from the map anyway (intended).
The real fix is the Arabia and Central Asia slices retiring these tags
properly. Decode further only if a shattered remnant shows in game.

### `initialize_from_bookmark.cpp:792 — Character has too many ruler traits! Character: '<key>', Traits: 'N', Expected: 'M'`
**WATCH — cosmetic, vanilla data on rulers WE seated.** The characters
named (Sancho II, Alfonso VI, Sancho Ramírez, Guillaume of Burgundy…)
are vanilla people who do not rule at 1337; seating them at 1066
exposes trait counts above the engine's expected-for-age formula. No
observed in-game effect. Revisit only if trait-driven content misfires.

### `jomini_script_system.cpp:252 — untyped trigger [ Scoped object of type 'country' is not valid (---) ] … common/international_organizations/hre.txt:328`
**DECODED (2026-07-29, the HRE launch) — a UI TOOLTIP trigger
evaluated on a null candidate; cosmetic.** hre.txt:328 sits inside
`can_lead_tooltip_trigger` (the election-candidate tooltip; the :327
`trigger_if` block's `exists = union`). 180 lines in the session that
confirmed the crowned HRE — consistent with the panel being OPEN
during the check; the root country is `---`, i.e. the UI evaluated
the tooltip with an empty candidate slot (no election is live — our
seeded `leader = OGK` holds). Same family as the "No context
supplied" GUI class: the cited line is where the trigger lives, not
where the mistake is, and there is no mistake on our side —
crown/electors/title all render correctly. WATCH: if the class grows
during play WITHOUT the HRE panel open, revisit (the candidate-sweep
theory would then need a second look). Count it OUT of the error
budget meanwhile.
**DECODED (2026-07-30): the two lines are NOR→ICE and NOR→GRL** —
vanilla's own dominion pairs, both kept by us
(12_diplomacy.txt:40-41). `dominion.txt:152` runs
`set_court_language = scope:future_overlord.court_dialect` in a block
written for runtime subject creation; replayed at bookmark init the
saved scope does not exist and the effect's target is null. Vanilla's
own start would produce the same two lines. Harmless, cosmetic, count
is exactly the number of start-date dominions. WATCH only if the count
grows past the dominion count or a dominion misbehaves.

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

### `jomini_script_system.cpp:252 — Undefined event target 'target_ruler'/'target_province' + Event target link 'scope' returned an unset scope` at `events/disaster/horde_civil_war.txt:608/628/739/750/761`
**Means:** VANILLA-side (decoded in Mongol Resurgence 2026-07-30, which
ships no override of that file — and neither do we). Vanilla saves the
scopes through a swallowed link (`ruler_or_regent ?= { save_scope_as }`)
and uses them UNGUARDED in the option bodies; a momentarily rulerless
civil-war party makes every option error. The error.log
`CHARACTER.GetName`/`FetchData`/`THIRD_ADD_CHARACTER_MODIFIER_DURATION`
trio with identical timestamps is the same event's tooltips, not a
second bug. 1066 is full of hordes, so this disaster CAN fire here —
when the signature appears, it is this.
**Fix:** none — accepted, harmless no-op.

### `initialize_from_bookmark.cpp:495-1719 — Country '<TAG>' has no government type / heir-selection / capital / society values / parliament_type…` (10-line barrage per tag: :495 :498 :517 :520 :525 :528 :1558 :1576 :169 :1719)
**Means:** a registry identity block with NO `10_countries` presence at
bookmark init. The ONLY silencer is a start block — landed or
claims-backed landless. Corrected 2026-08-01 (AUDIT-2026-07-31 §4.3):
an earlier version of this entry conflated this signature with `:592`
below — `is_historic = yes` belongs to THAT one and does NOT silence
this barrage (MR, live, 2026-07-31: three is_historic tags produced
the full barrage anyway). Vanilla corroborates: all 55 of its
`is_historic = yes` tags ALSO carry a start block, and SKE — once
cited here as "revolter cores instead of a block" — is a landed
kingdom whose block IS `10_countries.txt:308`. Our landless shells all
carry claims-backed 10_countries blocks, which is why this never
fired here.
**Fix:** give the tag a start block — a claims-backed landless shell
is enough. There is no alternative route; vanilla ships none.

### `initialize_from_bookmark.cpp:592 — Country '<TAG>' does not exist, nor has cores as a revolter at start… add 'is_historic = yes'`
**Means:** a landless tag shipped with NO claims list — the engine
accepts land, revolter cores (= `our_cores_conquered_by_others`) or
`is_historic`, and the tag has none of the three. First fired
2026-07-30, seventeen lines, all Italy North donors: the build's
`_landless_claims` was a per-slice enumeration PARALLEL to
`LANDLESS_AFTER`, and the slice updated one list but not the other —
so the eighteen donors went landless with their claims never written
(SAL's single claim was vanilla's own; Germany II's thirteen passed
because that slice was in both lists).
**Fix:** FIXED same day — `_landless_claims` now DERIVES from
`LANDLESS_AFTER` (minus the three DISPLACED_CLAIMS tags), and the
landless verifier asserts a non-empty claims list per tag, proven by
breaking. If this signature ever reappears, a landless tag shipped
claim-less past that assert — re-read the build before anything else.
The companion `:595` reverse line — `'OGK Holy Roman' is set as
'is_historic = yes' but it currently exists` — is vanilla's registry
marking OGK historic while we landed it: one cosmetic line, accepted.

### `jomini_script_system.cpp:252 — Event target link 'religion' returned an invalid object` at `scripted_triggers/pop_triggers.txt:3` via `pop_types/00_default.txt:153` (~504 lines)
**DECODED 2026-08-01 (first LOCATION_VACATED launch) — pops on vacated
SETTLED land.** A pop-type trigger reads the owning country's religion;
the location has no owner, so the link returns nothing — one line per
pop at init. Vanilla's own 7334 unowned locations are UNSETTLED, which
is why the class never existed before us: our Kipchak/Siberia/Danube
vacates emptied real towns with real pops. Harmless fail-safe (the
promotion/assimilation check just fails); the two one-shot
pdx_assert:214 Lookup lines in the same launch are WATCH-paired with
it. The class shrinks as future slices land owners on the steppe.
**Fix:** none — accepted; scan_log.py classifies it.
**MODEL CORRECTED 2026-08-02 (Perm/Vyatka package §E.4, arithmetic on
recorded numbers — NOT an in-game observation).** "One line per pop"
over-predicts: the 2026-08-01 launch's 305 vacated locations carry 911
`define_pop` and produced ~504 lines — ratio ≈0.55. The candidate
filters were tested and REFUTED: not pop presence (vanilla's 7,334
unowned carry 8,245 pops with no such class), not town presence (only
8 of the vacated appear in 07_cities), not `type = pop` coverage
(4,515 vanilla-unowned locations lack it). **The true filter is
UNKNOWN — an OWED in-game question.** Forecast for the next launch:
the build now vacates 625 locations carrying ~1,895 pops, so expect
this class near **~1,000 lines**, not 504 — scan_log.py's baseline
must move with it, and a count near 1,000 is EXPECTED, not a
regression.

### `country_database.cpp:107 — The following two countries have the same name 'GRZ' & 'GRA' = 'Granada'` (and `'NEA' & 'NAP' = 'Naples'`)
**Means:** by design. The landless irredenta tag IS the future of the
same polity the landed 1066 tag represents — Zirid Granada beside the
Nasrid shell, the duchy of Naples beside the Angevin-kingdom shell.
The engine only warns about the display-name collision; the landless
twin never renders on the map.
**Fix:** none — accepted, exactly two lines. If a future slice mints a
third pair, expect a third line.

### `pdx_persistent_reader.cpp:289 — Failed to read key reference: mr_railroad_on / MR_* …" in file: ""`
**Means:** ENVIRONMENT-side, not the mod. The user's Paradox settings
persist Mongol Resurgence game-rule selections; a 1066 session without
MR loaded cannot resolve those keys and logs one line per remembered
rule (the empty-name `::` lines at nearby line numbers are the same
settings file's other entries). Zero effect on the 1066 mod.
**Fix:** none needed; deleting the remembered game-rule block from the
launcher settings would silence it. This LIKELY also closes the old
`gamestate.cpp:133` "Failed to read key reference" ×4 that HANDOFF
carried as *Unexplained* since Phase 1 — same failed-key-reference
family, no file named, count matches a small settings block. Marked
likely rather than certain: the :133 lines were never re-observed
side by side with the MR keys.

### `initialize_from_bookmark.cpp:410 — character <key> has no birth scripted`
**Means:** a character ALIVE at start with no `birth = <location>`
field. Vanilla ships exactly four such characters (sco_malcolm_iii,
sco_donald_iii, sco_duncan_ii, ogk_heinrich_iv_salier) — dead by 1337,
so vanilla never needed to place them; OUR death-strip resurrection
exposed the gap (first observed 2026-07-30; an independent sweep
confirmed the four are the complete living-without-birth set).
**Fix:** FIXED — build_characters' `_BIRTH_FIXES` injects birthplaces
(scone [U] for the three Dunkeld Scots, goslar for Heinrich), with
already-has-birth and exact-count asserts so a vanilla patch filling
the gap fails loudly.

### `initialize_from_bookmark.cpp:1558/:1576/:169 — '<TAG>' has no marriage_law / heir_religion_law / society values scripted`
**Means:** a 10_countries block built WITHOUT any template include —
the template family is what supplies those laws and the thirteen
society sliders. Our two template-less explicit theocracies (ABS, FAT)
were the only tags in this state.
**Fix:** FIXED 2026-07-30 — both blocks restate
`marriage_law = muslim_marriage`, `heir_religion_law =
heir_same_religion` and the muslim family's thirteen sliders
(setup/templates/muslim_monarchy_no_abrahamic_dhimmi.txt values). That
fix was one item SHORT: a template supplies FOUR things, and the
nested `parliament = { parliament_type = council }` block
(muslim_monarchy_no_abrahamic_dhimmi.txt:19-21) was missed — the
engine kept answering with `:1719` for ABS and FAT until it was added
2026-08-01 (AUDIT-2026-07-31 D2). Rule for future template-less
blocks: restate both laws, the thirteen sliders, AND the nested
`parliament = { parliament_type = X }` block, or the engine logs the
classes and defaults silently.

### `character_manager.cpp:287 — <parent> has less than 10 years in <date> when Child (<key>) was conceived`
**Means:** the engine back-computes conception (birth minus nine
months) and requires the named parent to be at least ten. Fired once:
authored Ayyub (b. 1040) against authored Tamim (b. 1031).
**Fix:** FIXED — Ayyub moved to 1048.1.1 [U] (Tamim sixteen at
conception, Ayyub eighteen at start — the seat threshold still
passes). Rule for future cross-links: parent's birth + ~10y 9m must
precede the child's birth.

## Adding to this file

When the game reports a signature that is not here, add a row **once you have
decoded it** — signature, what it actually means, the fix, and whether it is
fixable at all. If it turns out to be vanilla-side, say so explicitly and say
how it was confirmed; that saves the next session from re-investigating a
non-problem. Two entries above are exactly that.
