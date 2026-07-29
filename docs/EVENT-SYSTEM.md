# THE EVENT SYSTEM — the flavor layer's foundation document

> Produced by the event-system research pass (Opus agent, 2026-07-29
> night), reviewed by the main session. Two vanilla reference files
> are the authority for this domain and outrank the wiki:
> `in_game/events/readme.txt` [README] and
> `in_game/common/on_action/on_actions.info` [INFO]. Corpus measured:
> 7,440 events in 349 files. THE TWO HEADLINE RESOLUTIONS: the
> round-2 "event-level triggers went silent" hypothesis is CLOSED
> (triggers ARE evaluated on every route — ours were simply false),
> and cross-file on_action merging WORKS (vanilla itself merges
> on_game_start across two files) — see the corrections section.

## 1. THE FIRING PIPELINE

### 1.1 Exactly three routes (+ one derived)

Measured route distribution over all 7,440 events: DHE self-schedule
3,212 (43%) · on_action `random_events` 1,961 (26%) ·
`trigger_event_*` from script 1,849 (25%) · on_action `events` 124
(2%) · multi-route 30 · unreferenced 264 (4%). [README] :73's
`orphan = yes` names the recognized source set: on_action,
trigger_event, dynamic_historical_event.

### 1.2 The on_action grammar [INFO — 13 sub-keys]

- `trigger` (54 uses): a false trigger = nothing happens.
- `events = { }` (53): "always fire as long as their trigger
  evaluates to true".
- `random_events = { }` (38): one weighted pick;
  `chance_to_happen = N` (31) gates evaluation; `100 = 0` = a chance
  of no event; weights factor the event's `weight_multiplier`.
- `delay = { days = N }` positional inside `events` — applies to all
  events AFTER it; a new delay overrides.
- `on_actions = { }` (17) chain; `first_valid_on_action` (4);
  `random_on_action` (1); `first_valid`/`fallback`/on_action-level
  `weight_multiplier` documented but UNUSED (0 each).
- **`effect = { }` TRAP [INFO, quoted]:** it runs "concurrently to
  events triggered by the on_action, NOT before... Scopes or local
  variables set in the effect here will not carry over to any event
  fired by the on_action." A silent-failure class we have not yet
  hit and would have.

### 1.3 Engine hooks

217 on_actions in on_actions.log, 153 engine-fired. The country
pulses: `monthly_country_pulse`, `yearly_country_pulse`,
`biyearly_country_pulse`, `four_yearly_country_pulse`,
`government_flavor_pulse`, `religion_flavor_pulse`,
`on_country_specific_pulse`, `in_regency_yearly_pulse`; location:
`earthquake_location_pulse`, `volcano_location_pulse`.
**`yearly_country_pulse` is STAGGERED per country, not 1 January**
(Bronze Era's own chronology comment attests the trap). Vanilla's
performance idiom (country_yearly.txt:5-7): narrow-condition events
live in cheap-outer-trigger sub-on_actions, not in the universal
`events` list.

### 1.4 How a DHE fires — no on_action involved

The event declares its own schedule (flavor_ENG.txt:14-32 traced):
engine monthly tick → tag match → `from <= today <= to` →
`monthly_chance`% roll → **the event's own `trigger` evaluates** →
show. The DHE block has exactly four legal sub-fields (measured over
3,232 events): `tag` (repeatable), `from`, `to`, `monthly_chance`.
Dynasty gates live in the ordinary `trigger` with `?=` safe-compares
(flavor_ENG.txt:4417, :4426).

### 1.5 THE TRIGGER LAW — the round-2 hypothesis RESOLVED

**`trigger_event_silently` and `trigger_event_non_silently` DO
evaluate the target event's `trigger` — immediate and delayed. A
false trigger silently discards the event on every route.** Five
confirmations, no dissent: [README] :58 (`on_trigger_fail` runs for
"a queued event (or one triggered immediately from script)" that
fails its trigger — a named hook for exactly this); [INFO] :15 and
:17 (delayed fires evaluate the trigger TWICE — at fire and at
delivery); vanilla's own comment country_yearly.txt:579 ("fired
unconditionally, gated by their own triggers"); 467 events fired
ONLY by trigger_event that carry triggers; flavor_pap.txt:3943 uses
on_trigger_fail to fire a substitute.

**What round 2 actually was:** the triggers were FALSE (the appanage
war-legality chain) — findings 1 and 2 of that entry were ONE
finding. The corrected house rule is in §4.

Secondary measurements: plain `trigger_event` DOES NOT EXIST (0
vanilla uses; the effects.log body text is a Paradox typo);
`is_triggered_only` does not exist (chain-only = no DHE block +
`orphan = yes`); "silently" means the event's name is not announced,
NOT hidden — player flavor uses `_non_silently`, machinery
`_silently`.

### 1.6 The derived fourth route: a self-driving mod pulse

`trigger_event_silently = { on_action = X days = N }`
(effects.log:10582, 9 vanilla uses) fires an ON_ACTION on a delay —
vanilla's treasure-voyage pulse re-schedules itself from its own
payload events (flavor_chi_treasure_expedition.txt:498-501; saved
scopes survive the hop). A mod-owned cadence with zero vanilla-file
contact.

### 1.7 The complete legal field set — 21 fields, nothing else

title 7418 · desc 7417 · outcome 7417 (neutral/negative/positive —
AUDIO only) · option 7414 (14,427 blocks) · type 7405 · immediate
6823 · trigger 5812 · illustration_tags 5174 · fire_only_once 3681 ·
dynamic_historical_event 3232 · historical_info 1725 · image 1512 ·
hide_portraits 975 · category 920 · after 373 · major 174 ·
major_trigger 153 · orphan 59 · hidden 7 · weight_multiplier 5 ·
on_trigger_fail 2.

Confirmed NOT to exist (0 uses each): `id`, `picture`,
`is_triggered_only`, `mean_time_to_happen`, `cooldown`, `sound`,
`goto_location`, `theme`, `duration`. `interface_lock` is documented
([README] :64) with ZERO uses — [U] if we ever use it.

**`fire_only_once` is GLOBAL** — once for the whole campaign, not
per-country (README :63 + wiki: a global variable
`<event>_fire_only_once`). A trap for multi-tag flavor.
**DHE + fire_only_once are near-mandatory together** — the engine
warns otherwise; vanilla itself trips the warning 22 times (all in
one hidden-events file).

### 1.8 Types and categories

`type`: country_event 7216, exploration_event 36, location_event 20,
age_event 1, omens_event 1. **No character_event exists** —
character-focused events are country_events saving character scopes
in `immediate` (the first two saved character scopes drive the
portraits; `hide_portraits = yes` suppresses).
`category`: disaster_event 455, situation_event 452,
international_organization_event 3 — engine enums, icon only
([README] :75); DHEs use NO category (they get the country-flag
badge, eventwindow.gui:890).

## 2. THE DHE ARCHITECTURE

### 2.1 The corpus

`DHE/` is 159 files / 311,764 lines. Naming `flavor_<TAG>.txt`
(case-inconsistent in vanilla; namespace always lowercase);
bilateral `flavor_<a>_<b>.txt` (25); DLC prefix `D008_`. Top tags:
ENG 234, TUR 228, FRA 208, CAS 205, HAB 168... 219 tags carry DHE
blocks; 361 namespaces exist tree-wide, 156 of them `flavor_*`.

### 2.2 THE 1066-1200 BLACKOUT, QUANTIFIED

Dated DHE events able to fire, by window: **1066-1200: ZERO.**
1201-1299: 2 (both flavor_eng, monthly_chance 1). 1300-1336: 65.
1337+: 3,124. **67 of 3,191 (2.1%) can fire before 1337** — the
"vanilla covers the late end" note refines to: coverage starts at
1300. The first 234 years of our campaign are empty; prioritizing
1066-1200 is the only option.

### 2.3 Pacing

`monthly_chance` is a straight %; distribution peaks at 10/1/5.
`100` = fires the month the window opens (74 vanilla uses; Mongol
Resurgence uses it for dated beats on the user's own instruction —
its test log records the fix). No MTTH exists; `weight_multiplier`
applies ONLY to random_events pools.

### 2.4 Chains, delays, broadcasts

Both effect forms attested (block 664+274, bare 275+323); intervals
`days = { A B }`, `months = { A B }`, `years = N`; cross-country
delayed via `c:X = { trigger_event_silently = { id years = 1 } }`.
**Broadcast idiom** (flavor_ENG.txt:313-320): `every_country = {
limit = { ... } trigger_event_non_silently = shared.id }` + a named
event for the co-protagonist. **`every_neighbour_country` (British
spelling) does not exist.** Hidden machinery: `title/desc =
empty_text` + `hidden = yes` (7 in vanilla; 4 combine hidden+DHE — a
dated invisible self-scheduling effect, useful).

### 2.5 Illustrations

`image` = raw quoted path; 175 distinct vanilla values, ALL resolve
(so a static existence check is meaningful). **The real flavor
system is `illustration_tags`** (5,174 vs 1,512): a weighted pool
over SIX real tags — interior/regular/exterior/angry/happy/armed —
composing scene names (gfx/scenes/00_scenes_events.txt). Whether a
bad image path errors or silently defaults: [UNVERIFIED].

### 2.6 Localization — SIX keys per DHE event

`<id>.title`, `.desc`, **`.entry`**, `.historical_info`, `.a`, `.b`.
**`.entry` is engine-derived and DHE-specific** (3,206 of 3,232 DHEs
carry it) — it labels the per-country DHE timeline panel
(country_dhe_lateralview.gui:194), and the missing-key error is the
known localization_util.cpp:103 signature (Mongol Resurgence's own
test log caught exactly it — which also proves MR's mod-authored
DHEs run in game). **Option loc keys are EXPLICIT** — 14,427/14,427
options carry `name =`; the .a/.b convention is habit, not
derivation. Dynamic title/desc via first_valid/random_valid/switch
([README] :7-42, 749 uses). Event loc lives under
`main_menu/localization/<lang>/events/` (DHE subfolder).

### 2.7 Option internals

name 14,427 (100%) · custom_tooltip 2,701 (keys like `<id>.tt2`) ·
historical_option 2,302 (Historical AI always picks it) · trigger
1,448 (**HIDES the option**, README) · ai_chance 1,211 ·
show_as_tooltip 392 · ai_will_select 180 (overrules ai_chance) ·
high_risk_option 75 · fallback 43 (available when all others are
not) · hidden_trigger 38 · exclusive 3. `ai_weight`, `highlight`,
`tooltip` DO NOT EXIST; `show_as_unavailable` is marked NOT
IMPLEMENTED by Paradox. Only 5 options visible at a time (wiki).

## 3. HOW MODS ADD FLAVOR

### 3.1 Cross-file on_action merge: WORKS

**Vanilla itself merges `on_game_start` across `_hardcoded.txt:1`
and `ai_personalities_setup.txt:9`** — the only duplicated name of
216 declarations, and both demonstrably run. 75 of 79 surveyed mod
on_action files use NEW filenames declaring vanilla hook names; six
mods coexist on shared framework hooks; one published author states
the merge rule outright. The one dissenting mod (claiming singleton)
is contradicted by vanilla and its own 773-vs-966-line "verbatim"
copy — the conservative whole-file route is the one that silently
deleted content. Caveat, stated honestly: vanilla's attestation
merges an `effect` file with an `on_actions` file; merging two
`events` lists is attested by mods only — treat
`on_actions = { my_dispatcher }` as the proven shape.

**Consequences for our record:** the round-1 on_game_start mystery
loses the merge candidate; the NEW candidate (attested by the
framework mods) is that **on_game_start fires BEFORE country
selection**, so player-scoped effects cannot work there; workaround
`delay = { days = 1 }` or the [UNVERIFIED] hooks
`on_game_start_after_lobby`/`on_game_load` (no vanilla presence,
three mods use them).

### 3.2 Directives and event modification

`REPLACE:/INJECT:/TRY_*` never appear in any events directory (wiki
confirms they do not work there). To modify a vanilla event: a new
file sorting BEFORE vanilla's re-declares the namespace and copies
the event; the resulting "Duplicated event ID" line is expected and
harmless (wiki) — for US that same line means an accidental
override, hence the namespace-collision harness check.

### 3.3 The published architectures

Anno 1644: 916 DHEs, proven in brand-new files AND namespaces.
Basileia (the closest analogue): own events subfolder, own loc, one
new-named on_action, 50 DHEs, **`?=` on every c:TAG link in its
startup fan-out**. Bronze Era: zero DHEs, pure on_action+chains —
and one DEAD 160-event pulse (defined, never referenced). Mongol
Resurgence (ours): 20 DHE events, ALL with DHE blocks and 19 with
top-level triggers — the exact combination round 2 feared, live in
game.

### 3.4 Anti-routes — shipped silent failures found in the corpus

Misspelled hook name (`on_country_yearly_pulse`) = a dead succession
chain, zero errors; an on_action defined but never referenced =
dead; referencing an undefined sub-on_action = dead entry;
`is_ai = no` in on_game_start = never true; assuming
yearly_country_pulse lands on 1 Jan.

## 4. THE 1066 FLAVOR ARCHITECTURE (adopted)

### 4.1 Route: `dynamic_historical_event` for essentially everything

No on_action file → the merge/load-order/misspelling classes become
unreachable; largest vanilla route; proven in-house (MR) and in new
namespaces (Anno 1644); populates the per-country DHE timeline
panel free. Secondary: chains from options; situation lifecycles
(unchanged); the self-driving pulse (§1.6) if a cadence needs it; a
new-filename dispatcher on_action ONLY for AI sustainment. Never
ship a file named after a vanilla on_action file.

### 4.2 Files and naming

`in_game/events/DHE/1066_flavor_<TAG>.txt`, namespace
`f1066_<tag>` (zero collisions verified; NEVER reuse a `flavor_*`
namespace — reuse is the override mechanism); loc at
`main_menu/localization/english/events/DHE/
1066_flavor_<tag>_l_english.yml`; BOM on both; ids 1-9999 (engine
range, README :4), banded 1-99 beats / 100-199 chains / 900-999
hidden machinery.

### 4.3 THE CORRECTED TRIGGER RULE (supersedes "no event-level triggers")

- **FLAVOR events SHOULD carry an event-level `trigger`** — 95% of
  vanilla DHEs do; being swallowed when conditions fail is the
  point. `?=` on every nullable link (ruler, dynasty, owner) — the
  DHE panel evaluates listed events' triggers CONTINUOUSLY
  (country_dhe_lateralview.gui:224), so an unguarded link floods.
- **RAILROAD beats (scripted deaths, successions, coronations) still
  carry NO event-level trigger** — guards inside options as
  if/limit. The Norman lesson survives intact, narrowed to its true
  scope.
- A flavor event that must react to its own failure uses
  `on_trigger_fail` (does not run for on_action-fired events).

### 4.4 The house template (six loc keys)

See DESIGN INPUTS in the research report; canonical stub: type +
fire_only_once + title/desc/historical_info + outcome +
illustration_tags (weighted, six real tags) + dynamic_historical_
event { tag from to monthly_chance } + guarded trigger + immediate
(scope saves drive portraits) + explicit-named options with
historical_option/ai_chance. Loc: `.title .desc .entry
.historical_info .a .b` — **`.entry` is the one nobody would
guess.**

### 4.5 `tools/new_flavor.py` (to build)

Mirror new_situation.py: SPECS dict, emits event+loc files, inert
via `trigger = { always = no }` + `# ARM:` marker (attested idiom),
the eight measured traps in the header comments (.entry;
fire_only_once global; explicit option names; no plain
trigger_event; no every_neighbour_country; ?= links; id range;
flavor-vs-railroad rule).

### 4.6 Harness additions (each proven by breaking when built)

1. Loc coverage extended to `.entry` + `.historical_info`.
2. `image` path existence (incl. the DLC root).
3. Namespace collision vs vanilla's 361.
4. Event id 1-9999 + uniqueness.
5. DHE well-formedness (fire_only_once present; only
   tag/from/to/monthly_chance inside; from < to; to > START_DATE).
6. Reachability extended with the DHE route.
7. Every option carries `name =`.
8. Field whitelist (the 21 + option set).
9. Re-arm the on_action-hook-exists check IF an on_action file ever
   lands.

## 5. ERROR BUDGET

Missing `.entry`/loc keys → localization_util:103 (named, loud).
Orphaned event → engine logs it (exact string [UNVERIFIED] — decoder
on first sighting). DHE without fire_only_once → warning
([UNVERIFIED] string). Bad image path → [UNVERIFIED] behavior;
static check instead. Duplicate event id → harmless per wiki, but
for us = accidental override (namespace check). Unguarded trigger
links → jomini 252 floods via the DHE panel. Misspelled on_action /
false-trigger-swallows → SILENT (route avoidance + the corrected
rule are the guards).

## CORRECTIONS TO THE PROJECT RECORD (applied to KNOWLEDGE.md)

1. Round-2's event-trigger hypothesis: CLOSED — triggers evaluate on
   every route; ours were false via the appanage chain; one finding,
   not two.
2. Round-1's on_game_start mystery: the cross-file-merge candidate
   is ELIMINATED (vanilla merges it itself); the live candidate is
   fires-before-country-selection.
3. Meta: a `^`-anchored grep over vanilla .txt is defeated by BOMs —
   this pass nearly shipped an inverted central finding that way
   (the same class as the ENG-doesn't-exist and HAB-registry
   incidents; now three strikes).
