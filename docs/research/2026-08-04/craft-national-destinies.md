# CRAFT STUDY — "National Destinies" (trin.national_destinies v1.3.1)

Source tree (read-only): `C:\Users\Desktop\National Destinies Mod`
Vanilla comparison tree: `E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probe file present: `in_game/map_data/definitions.txt` — vanilla detection passed)

All paths below are **mod-relative** unless prefixed `VANILLA:`.
Every factual claim carries `file:line`. Claims I could not verify are marked
**UNVERIFIED** or **INFERENCE** and are separated out in §8.

---

## 0. WHAT THIS MOD ACTUALLY IS (correcting the brief)

The brief called it "the flavour giant... ~2 situations + ~154 event files". That
is right on the counts and wrong on the shape. Its own metadata states the
design in one line:

> `"short_description": "Adds unique, historically-themed bonuses to every formable country in EU5."`
> — `.metadata/metadata.json:8`

It is **not** a situation mod with an event corpus attached. It is a
**per-formable-country content-stack mod**: 152 country tags, each with a
near-identical 9-file stack. The two situations are outliers — the only two
places in 342k lines where real state machines exist. The event corpus is a
*delivery layer for advances*, not a free-standing narrative system.

That distinction is the single most useful thing in this report, because it
changes what is copyable. See §7.

---

## 1. INVENTORY — MEASURED

### 1.1 Total footprint

3,333 files: 1,657 `.dds`, 1,457 `.txt`, 201 `.yml`, 15 `.png`, 2 `.gui`,
1 `.eu5deploy`.

Lines of script + localisation, by directory (counting `.txt`/`.yml`/`.gui`):

```
  71454  in_game/common/advances
  60123  in_game/events
  57889  in_game/common/building_types
  51457  in_game/common/bureaucracies
  40643  main_menu/localization/english
  25010  main_menu/common/static_modifiers
  18574  in_game/common/unit_types
   4354  in_game/common/levies
   4139  in_game/common/formable_countries
   1988  main_menu/common/auto_modifiers
    863  main_menu/common/modifier_type_definitions
    854  main_menu/common/modifier_icons
    776  in_game/events/situations
    717  in_game/common/situations
    595  in_game/common/generic_actions
    509  main_menu/common/coat_of_arms/coat_of_arms
    490  in_game/gui/panels/situation
    450  in_game/common/on_action
    346  in_game/common/disasters
    233  in_game/common/scripted_effects
    135  main_menu/common/named_colors
     98  in_game/common/international_organizations
     83  in_game/common/government_reforms
     80  in_game/common/scripted_triggers
     70  in_game/common/laws
     63  in_game/common/peace_treaties
     38  main_menu/common/game_rules
     22  in_game/common/cultures
     15  in_game/common/generic_action_ai_lists
      8  main_menu/setup/start
      3  in_game/common/biases
 342079  TOTAL
```

### 1.2 The per-tag content stack

One file per tag, per system, all named `<prefix>nd_<tag>.txt`. Load-order
prefixes are used deliberately and differ per system:

| Directory | Prefix | Files |
|---|---|---|
| `in_game/events/` | `nd_` | 153 |
| `in_game/common/advances/` | `99_nd_` | 153 |
| `in_game/common/building_types/` | `99_nd_` | 153 |
| `main_menu/common/static_modifiers/` | `99_nd_` | 153 |
| `in_game/common/unit_types/` | `99_nd_` | 151 |
| `in_game/common/bureaucracies/` | `99_nd_` | 151 |
| `main_menu/common/auto_modifiers/` | `99_nd_` | 150 |
| `in_game/common/levies/` | **`00_nd_`** | 150 |
| `in_game/common/formable_countries/` | `99_nd_` | 144 |
| `main_menu/localization/english/` | `nd_<tag>_l_english.yml` | 201 |

Levies alone use `00_` — everything else `99_`. **INFERENCE**: levies must load
*before* the advances/unit files that reference them (`unlock_levy = levy_nd_byz_dromon`,
`in_game/common/advances/99_nd_byz.txt:21`) and after nothing.

Tag coverage cross-check (measured): 153 event files = 152 country tags +
`nd_orphan_anchor.txt`. 144 formable files. Eight tags carry events but no
formable file — `ayu bah dah hre mlc mtm pgr yua` — i.e. tags that exist at
game start or use a vanilla formable definition unchanged. **Zero formable
files lack a matching event file.** That is a real cross-reference discipline
worth noting: the "does every formable have its content" invariant holds at
144/144.

### 1.3 Counts of the primary content objects

- **Advances defined by the mod: 5,447** across 152 files
  (mean 35.8/tag, median 35, min 2 `governance`, max 49 `nse`).
- **Events defined: 1,790** (1,773 in `in_game/events/*.txt`, 17 in
  `in_game/events/situations/nd_mandate_crisis.txt`).
- **Bureaucracy entries: 845.**
- **Localisation keys: 36,957** across 201 files, **zero malformed / multi-line**.
- **Situations: 2.** **Disasters: 2.** **Generic actions: 8.**
  **International organizations: 1.** **Peace treaties: 1.** **Laws: 1.**
  **Government reforms: 1** file. **Cultures: 1.** **On_action files: 1.**

### 1.4 BOM discipline — a third independent attestation of our setup/start law

Measured across every `.txt`/`.yml`/`.gui` in the mod:

```
('gui', BOM=True)   2
('txt', BOM=True)   1456
('txt', BOM=False)  1        <-- main_menu/setup/start/99_nd_pops.txt
('yml', BOM=True)   201
```

**The single BOM-free `.txt` in the entire 1,457-file corpus is the one file
under `main_menu/setup/start/`.** This is an independent third confirmation of
the rule in our `CLAUDE.md` (previously attested from vanilla's 25/25 and a
published conversion's 25/25).

Divergence to note: ND ships **both** its `.gui` files WITH a BOM
(`in_game/gui/panels/situation/*.gui`), against our rule-of-thumb that `.gui`
carries none. Vanilla remains the authority; this is one shipped mod's practice,
not a counter-law.

### 1.5 Loc trap sweep — clean

- Zero duplicate `.yml` basenames anywhere in the tree.
- **All 201 loc files live in `main_menu/localization/english/`.** No
  `in_game/localization/` exists.
- Zero multi-line values: every one of 36,957 entries parsed as
  `^\s*KEY:\s*\d*\s*"…"$` on one physical line. Paragraph breaks are the
  literal two-character escape `\n\n` (present in 1,087 of 1,773 event
  descriptions).

---

## 2. THE TWO SITUATIONS — FULL ANATOMY

### 2.A `nd_mandate_crisis` — the Chinese dynastic cycle
`in_game/common/situations/nd_mandate_crisis.txt` (498 lines)
Events: `in_game/events/situations/nd_mandate_crisis.txt` (776 lines, 17 events)
Triggers: `in_game/common/scripted_triggers/nd_mandate_crisis_triggers.txt` (80)
Effects: `in_game/common/scripted_effects/nd_mandate_crisis_effects.txt` (233)
Actions: `in_game/common/generic_actions/nd_mandate_crisis.txt` (595, 8 actions)
AI list: `in_game/common/generic_action_ai_lists/nd_mandate_crisis_list.txt` (15)
IO: `in_game/common/international_organizations/nd_mandate_challengers.txt` (98)
GUI: `in_game/gui/panels/situation/nd_mandate_crisis.gui` (189)
Colours: `main_menu/common/named_colors/99_nd_mandate_crisis.txt`
Loc: `main_menu/localization/english/nd_mandate_crisis_l_english.yml` (306)

**Spawn.** `monthly_spawn_chance = monthly_spawn_chance_low`
(`nd_mandate_crisis.txt:2`). Verified — `monthly_spawn_chance_low = 0.02`,
`VANILLA:main_menu/common/script_values/default_values.txt:1206`.

**Gate (`can_start`, lines 4-32).** A five-layer funnel, all on the
`middle_kingdom` IO leader:
1. `has_game_rule = nd_mandate_crisis_enabled` — off by default (§4.4).
2. IO and its leader must exist.
3. `NOT = { is_situation_active = situation:red_turban_rebellions }` —
   explicit non-collision with the vanilla situation covering the same ground.
4. Leader-country health: no cooldown var, `has_any_active_disaster = no`,
   `in_civil_war = no`, `var:celestial_authority <= 30`.
5. A **weighted stress test** — `weighted_calc_true_if = { amount >= 2 … }`
   over stability<0, government_power<40, legitimacy<40, and a nested
   `weighted_calc_true_if` over four estate satisfactions where the peasants
   count double (`1 =` for nobles/clergy/burghers, `2 =` for peasants,
   lines 24-27).

This is the single best-designed gate in the mod: the situation cannot fire on a
healthy empire, cannot double up with vanilla's Red Turbans, cannot re-fire for
30 years (`set_variable = { name = nd_mc_cooldown years = 30 }`,
`scripted_effects/nd_mandate_crisis_effects.txt:229-232`), and needs *two*
independent stress signals rather than one.

**Visibility (lines 41-61).** Four OR clauses: you lead the Middle Kingdom, you
neighbour/subject/enemy its leader, your capital is in `sub_continent:east_asia`,
or you are in the challengers IO. Note the `?=` safe-access on
`capital ?= { sub_continent ?= sub_continent:east_asia }` (line 55).

**Lifecycle — two phases, three exits.**

`on_start` (63-103): destroys any stale challenger IO; sets
`nd_mc_phase = 1` and `nd_mc_tags_released = 0` on the emperor; applies
`nd_mandate_crisis_unrest` with `months = -1 mode = replace` (permanent, single
instance); fires `nd_mandate_crisis.1` to the emperor and `.2` at
`days = 1` to every neighbour/East-Asian country.

`on_monthly` (105-283), three blocks:

- **Phase 1 flavour** — `random_list = { 600 = {} 100 = {.10} 100 = {.11} …
  100 = {.15} }` (118-126). Six flavour events, 1,200 total weight, so
  **50% chance of no event per month**, ~8.3% each. Cheap, readable, honest.
- **Phase 1→2 transition** (129-145) — polled inside the phase-1 branch:
  `years_since_situation_start > 0` AND `celestial_authority < 20`. Swaps
  `nd_mandate_crisis_unrest` for `nd_mandate_crisis_fragmentation`, fires `.23`.
- **Phase 2 releases** (149-236) — an **accelerating** release pace:
  `random = { chance = { value = 20 if(released>=3) add 15 if(released>=6) add 15 } }`,
  i.e. 20% → 35% → 50% per month as the empire crumbles. Inside, a
  `random_list` of 11 historical tags each guarded by
  `nd_mc_can_release_tag = { tag = MNG location = shangyuan }` (weight 10 each),
  a `50 =` dynamic-culture fallback, and a `100 = { }` no-op. Each historical
  branch fires `.20` at `days = { 5 15 }` and stores the choice in a
  per-tag variable `nd_mc_release_current_tag_MNG` etc.
- **Foreign opportunity** (239-255) — `chance = 3` monthly, picks a
  non-Chinese-culture-group neighbour at peace and fires `.32`.
- **Warlord "Claim the Mandate"** (261-282) — reaches into
  `international_organization:nd_mandate_challengers`, picks a member with
  `var:nd_mc_emperor_allegiance < -20` that has not yet claimed, 10% monthly.

`on_ended` (285-367): an `if / else_if / else_if` resolution ladder —
**Path C New Dynasty** (challenger controls ≥65% of Middle-Kingdom locations,
tested via `any_international_organization_owned_location = { … percent >= 0.65 }`),
**Path A Reform** (still phase 1), **Path B Reconquest** (fallback). Each fires
its resolution event (`.5` / `.3` / `.4`) and stamps a 10-year modifier. Then
three cleanup passes: emperor variables, every country's
`nd_mc_emperor_allegiance`, and `destroy_international_organization_no_instigator`.

**End trigger.** Externalised into a scripted trigger so the situation file and
the panel share one definition:
```
can_end = { custom_tooltip = { text = nd_mc_resolved_end_tt
                               nd_mandate_crisis_end_trigger = yes } }
```
(`nd_mandate_crisis.txt:34-39`). The trigger itself
(`scripted_triggers/nd_mandate_crisis_triggers.txt:22-79`) is an OR of five
clauses: Path A (phase 1 + stab≥30 + gov power≥50 + celestial authority ≥60),
Path B (phase 2 + emperor holds ≥65% + challengers dissolved), Path C
(challenger holds ≥65%), a **50-year safety valve**
(`years_since_situation_start > 50`, line 75), and "Middle Kingdom dissolved".

**Map.** `tooltip` (369-419), `map_color` (421-471) and five `legend_key`
blocks (473-497) all use the **same five-branch if/else_if ladder** — emperor /
challenger-leader / loyalist (`allegiance >= 50`) / rebel (`< 0`) / neutral. The
colours are named colours, not literals
(`main_menu/common/named_colors/99_nd_mandate_crisis.txt:2-6`), so the legend and
the map read from one source. Every legend entry carries
`require_color_on_map = yes`.

**Actions.** 8 `type = situation` generic actions
(`generic_actions/nd_mandate_crisis.txt`: `nd_mc_reform_bureaucracy:3`,
`nd_mc_purge_eunuchs:63`, `nd_mc_appease_generals:123`,
`nd_mc_grant_autonomy:189`, `nd_mc_negotiate_surrender:246`,
`nd_mc_imperial_edict:365`, `nd_mc_declare_loyalty:435`, `nd_mc_seek_mandate:512`).
Each is once-per-crisis, enforced by a `custom_tooltip`-wrapped
`NOT = { has_variable = nd_mc_used_X }` in `allow` (lines 21-24) so the panel
shows *why* it is greyed out. Each has a `select_trigger` block
(`looking_for_a = situation`, `target_flag = recipient`,
`visible = { situation:nd_mandate_crisis = this situation_is_active = yes }`,
lines 28-39) and an `ai_will_do` that doubles weight when the AI can afford it.
Some are priced: `price = price:rtr_negotiate_with_rebels_price` (line 132) —
reusing a vanilla Red-Turban price value rather than inventing one.
Registered for the AI via
`generic_action_ai_lists/nd_mandate_crisis_list.txt`, gated
`potential = { can_see_situation = situation:nd_mandate_crisis }`.

**The custom IO.** `nd_mandate_challengers` (98 lines). `unique = yes`,
`show_on_diplomatic_map = yes`, `create_visible_trigger = { always = no }` and
`can_join_trigger = { always = no }` — it is script-only, no player can create
or join it. Leadership is `leader_change_method = score` on `great_power_score`,
re-evaluated monthly. `auto_leave_trigger` (36-56) is the elegant part: a
warlord leaves automatically when its allegiance recovers to ≥50, when it loses
`government_reform:warring_state`, or when it becomes the emperor's
subject/ally. **The IO's own `monthly_effect` (60-89) drives the allegiance
variable** from live diplomacy:
```
change_variable = { name = nd_mc_emperor_allegiance
                    add = { value = "opinion(international_organization:middle_kingdom.leader_country)"
                            divide = 100  subtract = 1 } }
```
then clamps to [-100, 100] with two guarded `set_variable`s. So a warlord the
emperor courts diplomatically drifts back to loyalty on its own.

**GUI panel.** `nd_mandate_crisis.gui` (189 lines). Header left = phase counter
read straight off a country variable:
```
raw_text = "[GetUniqueInternationalOrganization('middle_kingdom').GetLeaderCountry.MakeScope.GetVariable('nd_mc_phase').GetValue|1] / 2"
```
(line 32) — note the `|1` default fallback. Header right = breakaway count with
`|0` fallback (line 52). Main image uses `one_country_header_template`
anchored on the IO leader (64-88). Three `situation_card_expandable` cards:
description, "The Dynastic Cycle", and END_REQUIREMENTS driven by
`TooltipRequirementsList = { textcontext = "[SituationView.GetActiveSituation.GetSituation.GetEndConditions]" }`
(172-175). Each card's expand/collapse is a `LateralView.Vars.Toggle('mc_desc_toggled')`
with three paired `visible` blockoverrides. The file's own header comment names
its sources: `the_revolution.gui`, `nd_dnm_reaction_of_the_reich.gui` (lines 7-10).

### 2.B `nd_dnm_reaction_of_the_reich` — the Danubian Monarchy's pariah decade
`in_game/common/situations/99_nd_dnm.txt` (219 lines)
GUI: `in_game/gui/panels/situation/nd_dnm_reaction_of_the_reich.gui` (301)
Disasters: `in_game/common/disasters/99_nd_dnm.txt` (346, 2 disasters)
Peace treaty: `in_game/common/peace_treaties/99_nd_dnm.txt` (63)
Events: `in_game/events/nd_dnm.txt` (1,219, 39 events — the largest event file)
Chain driver: `in_game/common/on_action/99_nd_on_actions.txt:373-402`

This is the mod's showpiece and the only place it builds a genuine multi-system
machine. Its file header states the design contract explicitly
(`99_nd_dnm.txt:1-21`):

> `# Resolution #1: the Situation OWNS every external consequence of forming`
> `# the Danubian Monarchy. There is no parallel scripted backlash`
> `# … it must coexist additively with vanilla HRE situations -- Reformation,`
> `# war_of_religions, guelphs_and_ghibellines`

**Start.** `can_start = { always = no }` (26-28) — the situation is started
*only* by `activate_situation = situation:nd_dnm_reaction_of_the_reich` inside
the formation event's `hidden_effect` (`in_game/events/nd_dnm.txt:61`, and again
at :87 for path B). `monthly_spawn_chance = monthly_spawn_chance_unique`
(line 23; `= 1`, VANILLA:`default_values.txt:1212`).
`hint_tag = hint_nd_dnm_reaction_of_the_reich` (line 24).

**`can_end` — three earnable exits plus a hidden fail-escape (38-74).** The
whole block is an `OR` of four `custom_tooltip`-wrapped clauses:
- Legitimacy: `has_variable = nd_dnm_ps_resolved`
- Strength: `has_variable = nd_dnm_reich_humbled`
- Endurance: `NOT = { has_variable = nd_dnm_pariah_timer }` (a 50-year timed
  variable) AND `legitimacy >= 60` AND `prestige >= 50`
- `hidden_trigger = { NOT = { any_country = { tag = DNM } } }` — keeps
  "DNM no longer exists" out of the player-facing requirements list.

**And the file records the scope bug it hit and how it fixed it** (30-37):

> `# the situation's can_end evaluates in SITUATION scope (no implicit`
> `# country owner). Bare has_variable = X / legitimacy >= N etc would either`
> `# evaluate against the wrong scope or fall through to a default-true result`
> `# (we observed the endurance clause silently going green at game start …)`

Every clause therefore wraps its country checks in `any_country = { tag = DNM … }`.
**This is a first-class engine finding and directly relevant to us.**

**`on_start` (91-126).** Three effects, each with a reason in comment:
1. `add_country_modifier = nd_dnm_reich_pariah` with `years = -1` (permanent).
2. **Gives the Emperor real teeth**: `random_country = { limit = { is_emperor = yes }
   add_casus_belli = { target = c:DNM type = casus_belli:cb_imperial_ban } }`.
   The comment (101-113) records that `international_organization:hre = { leader = { … } }`
   is **not a valid scope link** — engine logs
   `"Invalid scope types for event target link, link: leader"` — and the working
   idiom is `random_country = { limit = { is_emperor = yes } }`.
3. Notifies the Papacy via `c:PAP`.

**`on_monthly` (148-166).** Deliberately thin: one 3%/97% `random_list` firing
`nd_dnm.27`, gated by `NOT = { has_country_modifier = nd_dnm_reich_pressure_recent }`
so its 1-year debuff can never stack. The comment (128-147) records that the old
war-score poll was removed as fragile and replaced by an explicit **peace
treaty** the player must demand, and that chain advancement was moved OUT of the
situation so it survives an early end.

**`on_ended` (168-201).** Removes the pariah modifier, fires `nd_dnm.29`,
idempotently strips six chain modifiers ("`remove_country_modifier` is
idempotent so calling both is safe", 177-181), and — the nice touch —
**revokes the Emperor's imperial-ban CB** so a diplomatic settlement actually
settles something (189-200).

**The strength exit is a peace treaty, not a poll.**
`peace_treaties/99_nd_dnm.txt:16-62`: `peace_nd_dnm_humble_reich` with
`cost = { add = { desc = "DIPLOREASON_BASE" value = 80 } }`,
`potential` requiring `scope:winner = { tag = DNM has_country_modifier = nd_dnm_reich_pariah }`
and `scope:loser = { is_emperor = yes }`, `effect` setting
`nd_dnm_reich_humbled` and firing `nd_dnm.33`, and
`ai_desire = { add = { … value = -100 } }` so the AI Emperor only folds under
crushing war score. The file comment (1-15) explains why: *"peace treaty cost is
measured directly in war-score points"* — so `cost = 80` **is** the 80%-war-score
requirement, expressed in a system the player can see and act on.

**Two disasters feed the situation** (`disasters/99_nd_dnm.txt`):

- `nd_dnm_nationalities_question` (27-111). `can_start` needs `tag = DNM`,
  `has_variable = nd_dnm_formed`, `NOT = { has_variable = nd_dnm_grace }`
  (a 10-year timed var set at formation), `has_any_active_disaster = no`,
  `stability < 0`, and either >⅓ untolerated-culture population or
  `average_control_in_home_region < 0.5`. `on_start` snapshots a **target**:
  `set_variable = { name = nd_dnm_nq_control_target value = { add = average_control_in_home_region
  multiply = 1.15 min = 0.5 max = 0.8 } }` — i.e. the goal is relative to where
  you actually are, floored and capped. Three exits via `on_end`'s
  if/else_if/else on `nd_dnm_ausgleich_reached` / `nd_dnm_nq_reasserted` / else.
- `nd_dnm_pragmatic_sanction_crisis` (140-346). **A visible counter replaces
  RNG.** `on_start` sets `nd_dnm_crown_confidence = 0` and
  `nd_dnm_crown_confidence_target = 80`, then adds +15 if the player took the
  "rally the diets" chain choice and +25 for "ratify the decree" — so the
  narrative chain's choices are *materially load-bearing* on disaster difficulty
  (249-262). Exits: counter ≥ target (Upheld), counter ≤ -30 (Broken),
  or the player explicitly ceded. Its `monthly_spawn_chance` is itself
  conditional (148-157): `monthly_spawn_chance_low` normally,
  `monthly_spawn_chance_ultimate_high` once `nd_dnm_succession_step >= 3`, so
  the chain reliably hands off into the disaster.

  Its `on_monthly` (315-345) is the best single content-pump in the mod:
  ```
  random_list = { 25 = { custom_tooltip = an_event_occurs_tt }
                  75 = { custom_tooltip = no_event_occurs_tt } }
  hidden_effect = { random_list = {
      75 = {}
      3 = { trigger_event_silently = nd_dnm.40 }   # counter UP via gold
      3 = { nd_dnm.41 }  # UP via diplomacy
      3 = { nd_dnm.42 }  # UP via military
      3 = { nd_dnm.43 }  # UP via gold + stability
      3 = { nd_dnm.44 }  # DOWN (mitigable)
      3 = { nd_dnm.45 }  # DOWN
      2 = { nd_dnm.23 }  # cede escape
      2 = { trigger = { var:nd_dnm_crown_confidence >= 50 }  nd_dnm.46 }  # positive feedback
      2 = { trigger = { var:nd_dnm_crown_confidence <= 20 }  nd_dnm.47 }  # negative feedback
  } }
  ```
  The **visible/hidden pairing** is the technique: a visible `random_list` that
  only prints `an_event_occurs_tt` / `no_event_occurs_tt` so the player sees an
  honest "25% something happens this month" in the tooltip, and a
  `hidden_effect`-wrapped second `random_list` that does the real selection.
  Also note the two **state-conditional** entries — content that only exists
  when you are winning, and content that only exists when you are losing.

  And a real engine note in the comments (206-209):
  > `# EU5 polls can_end conditions even for INACTIVE disasters (for tooltip`
  > `# previews etc), so every var:X comparison must be guarded by has_variable`
  > `# to avoid runtime "Failed to fetch variable" errors`

**The succession chain.** Three events (`nd_dnm.30/.31/.32`) fired at years
2/5/8 post-formation. The mechanism (worth copying verbatim): formation event
sets three **timed** variables
```
set_variable = { name = nd_dnm_chain_30_pending value = yes years = 2 }
set_variable = { name = nd_dnm_chain_31_pending value = yes years = 5 }
set_variable = { name = nd_dnm_chain_32_pending value = yes years = 8 }
```
(`in_game/events/nd_dnm.txt:58-60`), and `monthly_country_pulse` polls for
"`_pending` gone AND `_fired` unset AND previous step's `_fired` set", firing the
event and stamping the guard (`on_action/99_nd_on_actions.txt:373-402`).
Timed-variable decay is the clock; `_fired` guards enforce narrative order even
if game time jumps. Each event's `immediate` removes the previous step's
modifier so the chain is *one thread, not a stack*
(`in_game/events/nd_dnm.txt:1124-1126`, `:1166-1169`).

**GUI panel — per-perspective cards.** `nd_dnm_reaction_of_the_reich.gui`
(301 lines) is the more advanced of the two. `two_countries_header_template`
with DNM left and `GetUniqueInternationalOrganization('hre').GetLeaderCountry`
right (70-102). Two header counters reading country variables with `|0`
fallbacks (37, 57). Then **five cards, two of them perspective-gated**:
```
visible = "[SituationView.GetPlayer.MakeScope.GetVariable('nd_dnm_formed').IsSet]"   # line 232, DNM card
visible = "[GetUniqueInternationalOrganization('hre').IsIOLeaderCountry(SituationView.GetPlayer)]"  # line 269, Emperor card
```
The DNM card's gate comment is instructive (225-230): DNM is identified by a
*country variable* rather than a tag check, because "the variable dies with the
country". Cards also carry an `onaction_hint` blockoverride opening the hint
panel: `on_action = "[OpenLateralViewWithParams('hints', 'selected_hint = hint_nd_dnm_reaction_of_the_reich')]"`
(136, 171).

Both GUI files carry a header comment naming the vanilla panels they borrowed
from (`hussite_wars.gui`, `the_revolution.gui`, `middle_kingdom.gui`,
`left_panel.gui`; `nd_dnm_reaction_of_the_reich.gui:10-15`). **All widget names
used are real vanilla widgets** — verified in §8.

---

## 3. THE EVENT MASS, MEASURED

### 3.1 Organisation: strictly per country tag

153 files in `in_game/events/`, one per tag (`nd_byz.txt`, `nd_arc.txt`, …),
plus `nd_orphan_anchor.txt`. One additional file for the situation,
`in_game/events/situations/nd_mandate_crisis.txt`. No thematic files, no
shared/generic event file, no per-region grouping.

Namespace = filename = tag: `namespace = nd_byz` (`in_game/events/nd_byz.txt:1`).

Event counts per file: max 39 (`nd_dnm`), then 20 (`nd_khl`), 17 (`nd_tkt`),
16, 16, 15, 15, 15 …; modal band 12-14. Minimum 2 (`nd_ayu`, `nd_dah`).

### 3.2 Total events and type census

**1,790 event definitions.** Type census across `in_game/events/`:

```
type = country_event      1790
type = character_event       0
type = location_event        0
type = situation_event       0     (situation_event appears only as `category =`)
category = situation_event  17
hidden = yes                 1     (nd_orphan_anchor.1)
major = yes                  0
is_triggered_only            0
fire_only_once             1761
```

**Every event in the mod is a `country_event`.** There is not one character or
location event in 342k lines.

### 3.3 Firing idiom census — one idiom dominates

```
dynamic_historical_event    1601   (89.4% of all events)
trigger_event                233   (mostly trigger_event_non_silently)
trigger_event_silently        15
```

The 1,601 `dynamic_historical_event` blocks were parsed. **Field census across
all 1,601 blocks — they are byte-identical apart from the tag:**

```
tag             1621 occurrences
from            1601   -> value 1337.1.1  x1600,  1521.1.1  x1
to              1601   -> value 1836.1.1  x1601
monthly_chance  1601   -> value 100       x1601
```

So the date window is **the entire campaign** and the chance is **100% monthly**.
`dynamic_historical_event` is not being used as a date-window scheduler at all —
it is being used as a **cheap monthly polling harness**. The real gate is the
`trigger` block, and the trigger census is startling:

```
DHE events with a trigger block: 1601   without: 0
trigger contents:   has_advance   1601
                    has_variable     9
```

**Every single one of the 1,601 free-firing events is gated on
`has_advance = <X>` and nothing else.** Cross-referenced: the 1,601 distinct
advances named in triggers are all mod-defined (zero vanilla advances
referenced), and **no advance is referenced twice** — a strict 1:1 pairing.
Of the mod's 5,447 advances, 1,601 (29%) carry a paired narrative event; 3,846
are silent stat grants.

### 3.4 What rides the situations vs what fires free

| Delivery route | Events | Share |
|---|---|---|
| `dynamic_historical_event` + `has_advance` (free-firing, advance-gated) | 1,601 | 89.4% |
| Situation / disaster / IO / on_action driven (`trigger_event*`) | 188 | 10.5% |
| Never fires by design (`nd_orphan_anchor.1`) | 1 | 0.1% |

Breaking down the 188: 17 belong to `nd_mandate_crisis`, and the bulk of the
rest are DNM's 39 (situation + two disasters + chain) plus ~130 formation
events fired from `form_effect` in `formable_countries/`.

**There are no `on_action`-hooked flavour pulses beyond one file.** The mod's
entire on_action surface is `in_game/common/on_action/99_nd_on_actions.txt`
(450 lines) with exactly two hooks: `monthly_country_pulse.effect` (bootstrap +
DNM chain) and `on_four_yearly_check_for_script.on_actions` → a custom
`nd_on_four_yearly_check` on_action (BYZ achievement gate).

### 3.5 The on_action file is the mod's best-documented artefact

`in_game/common/on_action/99_nd_on_actions.txt:1-34` is a 34-line header
recording four hard-won engine facts. Verbatim:

> `# An on_action's `effect` is a SINGLE-VALUE field. When two files declare`
> `# `effect` for the same on_action the engine keeps one and silently discards`
> `# the other, logging only "There is more than one 'effect' defined using most`
> `# recent: <file>". Vanilla never does this: across all 164 vanilla on_actions`
> `# there are zero cases of two files declaring the same field.`

> `# Engine periodic country hooks are `monthly_country_pulse`,`
> `# `biyearly_country_pulse`, `yearly_country_pulse`,`
> `# `four_yearly_country_pulse` -- no `on_` prefix. An `on_`-prefixed pulse`
> `# name is almost certainly invented and will never fire.`

> `# Free slots as of EU5 buildid 24187685: monthly_country_pulse.effect,`
> `# biyearly_country_pulse.effect, on_country_specific_pulse.{effect,`
> `# on_actions}, on_four_yearly_check_for_script.on_actions.`

The chaining workaround — declare `on_actions = { my_custom_on_action }` on the
vanilla hook when its `effect` is taken — is used at lines 417-419 and credited
to vanilla's `ai_personalities_setup.txt`.

And the file records the exact failure this caused in the shipped mod
(lines 15-21): its effects were silently dropped, producing three Workshop bug
reports ("Austria 2026-06-13, Bohemia 2026-07-16, Bohemia + Poland 2026-07-27",
lines 42-43) before the cause was found.

### 3.6 `nd_orphan_anchor.txt` — a validator-appeasement pattern

`in_game/events/nd_orphan_anchor.txt` (77 lines, 1 event) exists solely to make
the engine's reachability validator stop warning about variables that are only
read in localisation tooltips. It is
`hidden = yes`, `fire_only_once = yes`, **`orphan = yes`**, and
`trigger = { always = no  OR = { has_variable = … x35 } }`.

The comment records the measurement that proves how it works (lines 340-350 of
the on_action file):

> `# The anchor works purely by EXISTING -- the reachability check is static.`
> `# Calling it also made the engine log "Event nd_orphan_anchor.1 is scripted`
> `# as an orphan, but has callers", since `orphan = yes` promises no callers.`

Verified vanilla-legal: `orphan = yes` appears **62 times** in
`VANILLA:in_game/events/`.

---

## 4. FLAVOUR CRAFT — CONCRETELY

### 4.1 Option architecture — measured across 1,773 events

```
options per event:   1 option  ->  707 events
                     2 options -> 1047 events
                     3 options ->   19 events
```

Feature presence (number of events containing each construct), across all 1,773:

```
trigger = {          1605     (the DHE has_advance gate)
hidden_effect         164
add_gold                4
immediate = {           2
save_scope_as           1
triggered_desc          1
first_valid             1
custom_tooltip          1
is_ai                   0
ai_chance               0
highlight               0
```

Effect presence:
```
add_country_modifier  1169     (66% of events)
set_variable           159
change_societal_value   53
add_stability           11
change_variable          9
add_legitimacy           6
add_prestige             3
add_estate_satisfaction  2
add_manpower             2
```

**Read that table carefully.** The 1,773-event corpus is
*mechanically almost inert*: two options at most, one timed country modifier as
the payload, no AI weighting, no priced options, no scoped characters, no
conditional descriptions. All the mechanical sophistication in the mod is
concentrated in the ~50 DNM + mandate-crisis events.

`outcome` enum usage: `neutral` 1687, `positive` 93, `negative` 10.

### 4.2 Where the real option craft lives — 4 condensed skeletons

**(a) The three-tier priced choice** — `in_game/events/nd_dnm.txt:797-831`.
The pattern that makes a counter-driven disaster feel like a decision:
```
nd_dnm.40 = {                              # An Estate Petitions for Loyalty
	type = country_event
	title/desc/outcome = neutral
	option = {  name = nd_dnm.40.a         # spare no expense
		add_gold = { value = monthly_income_trade_and_tax  multiply = -12  max = -100 }
		change_variable = { name = nd_dnm_crown_confidence add = 15 } }
	option = {  name = nd_dnm.40.b         # moderate sum
		add_gold = { value = monthly_income_trade_and_tax  multiply = -6   max = -50 }
		change_variable = { name = nd_dnm_crown_confidence add = 7 } }
	option = {  name = nd_dnm.40.c         # refuse
		change_variable = { name = nd_dnm_crown_confidence add = -3 }
		add_estate_satisfaction = { type = estate_type:nobles_estate
		                            value = estate_satisfaction_weak_penalty } }
}
```
The cost is **relative** (`monthly_income_trade_and_tax × N`) with an absolute
floor (`max = -100` — note that `max` on a negative value is the floor). A poor
country pays a real minimum; a rich one pays proportionally. The same three-tier
shape recurs with different currencies: diplomacy/prestige (`.41:835-860`),
manpower (`.42:864-894`), gold+stability (`.43:898-933`). **Four different
resources, one repeatable dramatic shape.**

**(b) The religion-branched formation event** — `in_game/events/nd_byz.txt:4-70`.
The only `first_valid`/`triggered_desc` in the corpus:
```
nd_byz.1 = {
	type = country_event   fire_only_once = yes   outcome = neutral
	desc = { first_valid = {
		triggered_desc = { trigger = { religion = religion:hellenism_religion }
		                   desc = nd_byz.1.d.hellenic }
		triggered_desc = { desc = nd_byz.1.d } } }
	option = { name = nd_byz.1.a                                   # always
		add_country_modifier = { modifier = nd_byz_renovatio_imperii years = 40 mode = add_and_extend }
		change_societal_value = { type = centralization_vs_decentralization
		                          value = societal_value_large_move_to_left }
		hidden_effect = { set_variable = nd_formed
		                  set_variable = nd_byz_formed
		                  set_variable = nd_byz_path_a } }
	option = { name = nd_byz.1.b  trigger = { religion = religion:orthodox }   … path_b }
	option = { name = nd_byz.1.c  trigger = { religion = religion:hellenism_religion } … path_c }
}
```
Three paths where the third only exists if a DLC feature was used. The
`hidden_effect { set_variable }` triple — `nd_formed` (global "any destiny
formed"), `nd_<tag>_formed` (this tag's tree unlock), `nd_<tag>_path_a`
(which branch) — is the **universal contract** across all 152 tags.

**(c) "Play as the breakaway"** — `in_game/events/situations/nd_mandate_crisis.txt:424-510`.
```
option = {
	name = nd_mandate_crisis.20.play_as_tag
	trigger = { hidden_trigger = { is_ai = no } }
	if = { limit = { has_variable = nd_mc_release_current_tag_MNG }
	       nd_mc_release_warlord_tag = { tag = MNG culture = culture:jianghuai_culture
	                                     accepted_culture = culture:wu_culture }
	       nd_mc_add_country_to_challengers_and_dow = { country = c:MNG }
	       change_player = c:MNG }
	else_if = { … x10 more tags … }
}
```
`trigger = { hidden_trigger = { is_ai = no } }` — the option is invisible to the
AI *and* the "is_ai = no" condition never renders in a tooltip. This is the only
`is_ai` use in the whole mod (2 occurrences, both here and at :605). Note the
cost: the else_if ladder is duplicated verbatim between option A and the
play-as option — 11 branches × 2 = 22 near-identical blocks, ~170 lines.

**(d) Dynamic country creation from a culture** —
`in_game/events/situations/nd_mandate_crisis.txt:530-600`. The fallback when no
historical tag can be released. `immediate` finds the biggest non-primary-culture
location by weighted population:
```
immediate = {
	ruler_or_regent = { save_scope_as = target_character }
	ordered_owned_location = {
		limit = { NOT = { dominant_culture = root.culture }
		          province != root.capital.province }
		order_by = { value = population
		             if = { limit = { location_rank = location_rank:city } multiply = 10 }
		             if = { limit = { location_rank = location_rank:town } multiply = 5 } }
		max = 1   check_range_bounds = no
		dominant_culture = { save_scope_as = target_culture }
		save_scope_as = target_location } }
option = { …
	scope:target_location = {
		create_dynasty_from_location = random
		last_dynasty_in_location = { save_scope_as = target_dynasty }
		create_country_from_location = {
			save_scope_as = target_country
			nd_mc_released_country_setup = yes
			set_capital = prev
			create_character = { culture = scope:target_culture  age = 30
			                     dynasty = scope:target_dynasty
			                     save_scope_as = new_ruler
			                     prev = { set_new_ruler = prev } } } }
	every_owned_location = { limit = { dominant_culture = scope:target_culture
	                                   province != root.capital.province }
	                         change_location_owner = scope:target_country } }
```
`create_dynasty_from_location = random` → `last_dynasty_in_location` →
`create_country_from_location` → `create_character` is the full generated-successor
recipe. The historical-tag path uses the *other* tool:
`create_country_from_cores_in_our_locations = c:$tag$`
(`scripted_effects/nd_mandate_crisis_effects.txt:125`).

### 4.3 Named characters, quotes, chained narratives

Measured across all 1,773 event descriptions:

```
paragraph break \n\n              1087
1st/2nd person (you/your/we/our)   732
contains a 4-digit year (1xxx)     177
#bold formatting                   164
contains a [promote] token          10
#italic formatting                   3
contains an escaped quotation        0
```

- **Named historical characters appear inside the prose, not as scoped
  characters.** e.g. `nd_arc.4.d` (`main_menu/localization/english/nd_arc_l_english.yml:43`):
  *"In 1254 Hethum I rode east through the Mongol lands to the court of the Great
  Khan Möngke. He covered four thousand miles and was received in audience for
  fifty days."* There is exactly one `save_scope_as` in 1,773 events; the
  situation events do use `ruler_or_regent = { save_scope_as = target_character }`
  (e.g. `events/situations/nd_mandate_crisis.txt:18`) but the tag corpus does not.
- **Period quotes are essentially absent**: across 8,721 `nd_*_desc` keys
  (advance descriptions) exactly **one** contains an embedded quotation —
  `nd_dnm_bella_gerant_alii_desc` (`nd_dnm_l_english.yml:60`),
  *"\"Let others wage war; you, happy Austria, marry.\""*.
- **Only 10 of 1,773 descriptions use any `[…]` promote token.** The prose is
  static, hand-written, and non-interpolated. That is a deliberate trade: it
  reads as a chronicle rather than a mail-merge, but it also means a formed
  country's own name never appears in its own event text.
- **Chained narrative exists in exactly one place**: the DNM succession chain
  (`.30/.31/.32`), plus the disaster's counter arc. The 152-tag corpus has no
  chains at all — every event is `fire_only_once`, independent, advance-gated.

### 4.4 How a long campaign is kept supplied — the honest answer

Not by date windows (all 1,601 windows are identical and span the whole game),
not by repeatable pulses with cooldowns (there are none in the tag corpus), and
not by on_action hooks (two, both administrative).

**Content is unlocked by player progress through the advance tree.** The
destiny tree structure, per tag (read from `in_game/common/advances/99_nd_arc.txt:308-430`
and the matching events at `in_game/events/nd_arc.txt:263-490`):

```
nd_<tag>_destiny                depth = 0   allow = { stability >= 75 }
├── nd_<tag>_dest_<A1>          requires = nd_<tag>_destiny
│     allow = { custom_tooltip = { text = nd_<tag>_path_a_tt has_variable = nd_<tag>_path_a }
│               owns_or_non_sovereign_subject_owns = location:jerusalem
│               owns_or_non_sovereign_subject_owns = location:urfa
│               prestige >= 50   stability >= 75 }
├── nd_<tag>_dest_<A2>          requires = <A1>   (2 more locations, total_development >= 2000)
├── nd_<tag>_dest_<A3>          requires = <A2>   (2 more locations, army_size >= 75, gold >= 3000)
├── nd_<tag>_dest_<B1>          requires = nd_<tag>_destiny   (path_b tooltip gate)
├── nd_<tag>_dest_<B2>          requires = <B1>
└── nd_<tag>_dest_<B3>          requires = <B2>
```

Every advance carries
`potential = { has_or_had_tag = ARC has_variable = nd_arc_formed has_game_rule = nd_destinies_enabled }`.
The path-exclusivity is enforced **only on the stage-1 openers**, via a
`custom_tooltip`-wrapped `has_variable = nd_arc_path_a` — stages 2 and 3
inherit exclusivity through `requires`. Elegant: one gate, not six.

Each of those 7 advances has a paired event: root + A1 + B1 are single-option
acknowledgements; A2/A3/B2/B3 offer a **two-option sub-choice of timed
modifiers** — two readings of the same achievement
(`in_game/events/nd_arc.txt:316-389`). Documented in-source at
`in_game/events/nd_dnm.txt:283-285`:
> `# One DHE per destiny advance. Root + the two stage-1 openers are single`
> `# acknowledgements; the stage-2 and stage-3 milestones offer a sub-choice`
> `# of two timed modifiers (a different reading of the same achievement).`

The remaining events per tag are "heritage" DHEs paired with the tag's ordinary
(non-destiny) advances, e.g. `nd_byz.2` gated on `has_advance = nd_byz_greek_fire`
(`in_game/events/nd_byz.txt:74-102`), `nd_arc.2` through `.7` on the Cilician
heritage advances.

**Master switches.** Three game rules make the whole mass optional
(`main_menu/common/game_rules/99_nd_game_rules.txt`):
`nd_mandate_crisis_rule` (default **disabled**),
`nd_bureaucracies_rule` (default enabled), `nd_destinies_rule` (default enabled).
All three carry `flag = flavour_rule`. And the loc for the off state tells you
exactly what survives (`nd_destinies_l_english.yml:7`):
> `setting_nd_destinies_disabled_desc: "Destiny advances do not appear after forming. Formation events and timed modifiers still play; heritage advance trees, bureaucracies, and custom units/buildings/levies remain enabled."`

---

## 5. LOCALISATION STYLE

### 5.1 Scale

- 201 files, all in `main_menu/localization/english/`, all BOM'd, **36,957 keys**.
- Value length: mean 112 chars, median 37, max 1,317
  (`nd_dnm_l_english.yml:436  nd_dnm_panel_dnm_body`).
- **Event descriptions (`.d`): 1,773 keys, mean 587 chars, median 582, max 1,291.**
  Every event has exactly one. Total event-facing prose (`.t`/`.d`/`.a`/`.b`/`.c`):
  6,430 keys, **1,199,277 characters**.
- Advance/modifier descriptions (`nd_*_desc`): 8,721 keys, mean 170 chars.

### 5.2 File-splitting convention

Two files per tag:
- `nd_<tag>_l_english.yml` — everything (events, modifiers, advances, tooltips).
- `nd_<tag>_country_l_english.yml` — **only** the country-identity keys (39 tags
  have one). Complete example, `nd_dnm_country_l_english.yml`:
  ```
  DNM:        "Danubian Monarchy"
  DNM_ADJ:    "Danubian"
  DNM_f:      "Danubian Monarchy"
  DNM_f_desc: "The Danubian Monarchy is the empire the House of Habsburg forges by abandoning the Reich. …"
  ```
  (4 keys, one of them a 900-character pitch for the formable.)

Eleven cross-cutting files: `nd_destinies_`, `nd_event_entries_`,
`nd_mandate_crisis_`, `nd_orphan_anchor_`, `nd_bureaucracies_`,
`nd_bureaucracy_governance_`, `nd_bureaucracy_impact_modifier_types_`,
`nd_governance_`, `nd_minor_governors_`, `nd_pm_names_`, `nd_rom_byz_`.

### 5.3 Key naming conventions (all read from source, not memory)

| Pattern | Example | Source |
|---|---|---|
| `<namespace>.<n>.t` / `.d` / `.a` `.b` `.c` | `nd_dnm.1.t` | `nd_dnm_l_english.yml:15-17` |
| `<namespace>.<n>.entry` | `nd_adu.1.entry: "$nd_adu.1.t$"` | `nd_event_entries_l_english.yml:4` |
| `<namespace>.<n>.d.<variant>` | `nd_byz.1.d.hellenic` | `in_game/events/nd_byz.txt:12` |
| `<option>_tt` | `nd_mandate_crisis.10.a_tt` | `events/situations/nd_mandate_crisis.txt:130` |
| `STATIC_MODIFIER_NAME_<key>` / `_DESC_` | `STATIC_MODIFIER_NAME_nd_dnm_gesamtmonarchie` | `nd_dnm_l_english.yml:38-41` |
| `<advance_key>` / `<advance_key>_desc` | `nd_dnm_bella_gerant_alii` / `_desc` | `nd_dnm_l_english.yml:59-60` |
| `<TAG>` / `<TAG>_ADJ` / `<TAG>_f` / `<TAG>_f_desc` | `DNM_f_desc` | `nd_dnm_country_l_english.yml` |
| `<TAG>_f_trigger_<x>` (formable allow tooltip) | `DNM_f_trigger_hab` | `nd_dnm_l_english.yml:4` |
| `nd_<tag>_<var>_tt` (variable tooltip) | `nd_dnm_path_a_tt` | `nd_dnm_l_english.yml:10` |
| `rule_<rule>` / `setting_<opt>` / `setting_<opt>_desc` | `rule_nd_destinies_rule` | `nd_destinies_l_english.yml:4-7` |
| `<hint_tag>` / `<hint_tag>_hint_text` / `_hint_text_<n>` | `hint_nd_dnm_reaction_of_the_reich_hint_text_1` | `nd_dnm_l_english.yml:410-413` |
| situation key itself + `_desc` | `nd_mandate_crisis` / `nd_mandate_crisis_desc` | `nd_mandate_crisis_l_english.yml:11-12` |

**`.entry` is a required engine-derived key**, verified vanilla: 5,211
`.entry` keys in `VANILLA:main_menu/localization/english/`. ND covers
1,751 of its 1,790 events in the bulk file, plus 39 more inside
`nd_dnm_l_english.yml` — total 1,790 minus the 17 `category = situation_event`
events, which have **no** `.entry` key. **INFERENCE**: `category = situation_event`
events are not listed in the event-log ledger and so need no entry key.

### 5.4 Voice and formatting

Voice is **first-person-plural royal-council** sliding into a decision, not
second-person instruction and not detached chronicle. 732 of 1,773 descriptions
use we/our/you/your.

Sample, `nd_arc.1.d` (`nd_arc_l_english.yml:28`):
> *"The crown of Sis is set; the kingdom holds. Yet the prelates have come to the
> citadel with a question that cannot be deferred. For two centuries the
> Apostolic Church has stood apart from Chalcedon and from Rome alike… The
> highland clergy refuse: better the Mamluk than the Pope, better isolation than
> the loss of the kingdom's soul. The barons in Frankish surcoats answer them:
> better Cyprus than ruin, better the Pope than the desert. Two paths open
> before the Catholicate; both are the kingdom's life.\n\n#bold This choice
> unlocks a destiny path in the Traditions tab.#!"*

Two structural habits worth naming:
1. **The closing question.** Almost every heritage description ends on an
   explicit pivot to the choice: *"The question is what to do with a standing
   army that never disbands."* (`nd_dnm.2.d`, `nd_dnm_l_english.yml:20`);
   *"The question is how far to commit."* (`nd_arc.4.d:43`).
2. **The mechanical signpost, formatted and separated.** Formation events close
   with a literal `\n\n#bold This choice unlocks a destiny path in the Traditions
   tab.#!` — the game-mechanics sentence is quarantined in bold at the end so it
   never contaminates the prose.

Option names are **verb-first, then a colon or dash, then the reading**:
```
nd_arc.1.a: "Apostolic Sanctuary: keep the kingdom undivided in faith"
nd_dnm.1.a: "Antemurale Christianitatis -- be the bulwark of Christendom"
nd_arc.4.a: "Press the alliance: stake everything on the steppe brotherhood"
```

Formatting tokens in use (all read from source): `#bold …#!`, `#italic …#!`,
`#T …#!` (heading), `#Y …#!` (emphasis/yellow), `@arrow_bonus_tier_1!` /
`_tier_2!` / `_tier_3!` icons, `$OTHER_KEY$` interpolation,
`[ShowCasusBelliName('cb_imperial_ban')]`, `[casus_belli|e]`,
`[GetUniqueInternationalOrganization('hre').GetLeaderTitle]`,
`[ShowDisasterName('nd_dnm_pragmatic_sanction_crisis')]`,
`[GetSituationByKey('nd_dnm_reaction_of_the_reich').GetNameWithNoTooltip]`
(`nd_dnm_l_english.yml:410-413`). Hint bodies are composed from numbered
sub-keys: `hint_X_hint_text: "$hint_X_hint_text_1$\n\n$hint_X_hint_text_2$"` —
which is exactly vanilla's shape (`VANILLA:hints_l_english.yml:537`).

**No loc traps found.** Zero duplicate filenames across trees, zero multi-line
values, zero files outside `main_menu/localization/`.

---

## 6. SCALE ECONOMICS — HAND-WRITTEN OR TEMPLATED?

### 6.1 Script per delivered beat

Across the 1,773 tag events:
```
event script lines (excl. blank/comment):  mean 27.6   median 32   min 7   max 70
total:                                     49,075 lines
```
Classified by line role:
```
structural / boilerplate  36,346  =  74%
substantive (effects)     12,729  =  26%
```
("Structural" = `type =`, `fire_only_once =`, the six `dynamic_historical_event`
lines, `trigger = {`, `has_advance =`, `title/desc/outcome =`, `option = {`,
`name =`, and closing braces.)

### 6.2 Templating measured directly

I normalised every event (stripping identifiers, `nd_*` names, and whitespace)
and hashed the skeleton:
```
distinct skeletons:                              1,638
events sharing a skeleton with another event:      199
largest skeleton cohort:                             9
```
So the *script* is not literally generated — 1,638 distinct shapes for 1,773
events — but the variety is trivial: the shapes differ only in whether there is
one option or two and whether a `add_country_modifier` block is present. A
generator with four templates would reproduce ~90% of it.

### 6.3 The actual ratio

| Per delivered player-facing beat (one event) | |
|---|---|
| Script lines | ~28 (of which ~21 boilerplate) |
| Localisation characters | ~677 (`.t` + `.d` + options), of which `.d` alone ~587 |
| Mechanical payload | 0.66 timed country modifiers |
| Accompanying advance | 1 (with its own name + `_desc` loc) |

**The mod's cost is prose, not script.** 1.2 million characters of hand-written
historical description — roughly 200,000 words, the length of a long novel —
carried on 49,000 lines of near-mechanical wrapper. The supporting systems
(advances 71k, buildings 58k, bureaucracies 51k lines) are likewise stat blocks
with a comment header each, e.g.
`in_game/common/advances/99_nd_byz.txt:13-15`:
```
# Greek Fire — unlocks the dromon war galley and its levy.
# The most feared weapon in the medieval Mediterranean, Greek fire
# gave Byzantine galleys devastating close-range superiority.
```
Every single content object in the mod carries a 2-5 line historical
justification comment. That is where the "immersive" reputation is actually
manufactured: not in the mechanics, but in a corpus where nothing is unlabelled.

### 6.4 Visible generator/template traces

- `main_menu/localization/english/nd_event_entries_l_english.yml` (2,058 lines):
  pure mechanical output, alphabetically sorted **as strings** so `.10` and `.11`
  precede `.2` (lines 4-14). Nobody hand-wrote that ordering.
- The 11-branch else_if ladders in
  `events/situations/nd_mandate_crisis.txt:345-410` and `:429-505` are the same
  block emitted twice with `change_player` appended.
- The `nd_mc_cleanup_variables` effect
  (`scripted_effects/nd_mandate_crisis_effects.txt:199-233`) lists all 11
  release variables and 5 action variables as individual guarded removals.
- Every advance in a tag file repeats
  `potential = { has_or_had_tag = XXX has_variable = nd_xxx_formed has_game_rule = nd_destinies_enabled }`
  verbatim 40-46 times (measured: 46 identical copies in the RUM file, 41 in AIR).

---

## 7. VERDICT

### 7.1 Techniques worth copying for 1066's situation flavour

**T1 — Externalise `can_end` into a scripted trigger, and wrap every clause in
`custom_tooltip`.**
`situations/nd_mandate_crisis.txt:34-39` delegating to
`scripted_triggers/nd_mandate_crisis_triggers.txt:22-79`; the DNM situation
does the same inline at `situations/99_nd_dnm.txt:38-74`. The payoff is that
`TooltipRequirementsList = { textcontext = "[SituationView.GetActiveSituation.GetSituation.GetEndConditions]" }`
(`gui/panels/situation/nd_mandate_crisis.gui:172-175`) renders the end
conditions in the panel *as written prose*, and a `hidden_trigger` clause
(`99_nd_dnm.txt:70-72`) hides the ugly fail-escape from that same list. This
is directly vanilla-attested — `VANILLA:in_game/common/scripted_triggers/disaster_triggers.txt:58-77`
uses exactly this custom_tooltip/hidden_trigger mix.

**T2 — Replace RNG exits with a visible counter seeded by earlier choices.**
`disasters/99_nd_dnm.txt:113-138` documents the redesign, `:249-262` implements
the seeding (+15 from `nd_dnm_succession_groundwork`, +25 from
`nd_dnm_decree_ratified`, target 80). The narrative chain three years earlier
becomes a difficulty setting the player chose. Pair with a header counter in the
GUI (`nd_dnm_reaction_of_the_reich.gui:57`) so the number is visible.

**T3 — Timed variables as a narrative clock, `_fired` guards as an order
enforcer.** `events/nd_dnm.txt:58-60` sets `_pending` vars at years 2/5/8;
`on_action/99_nd_on_actions.txt:373-402` polls monthly for
"`_pending` gone AND `_fired` unset AND previous `_fired` set". Cheap, save-safe,
survives time jumps, and — critically — **lives on a pulse, not on the
situation**, so the chain does not die when the situation ends early
(the rationale is recorded at `99_nd_dnm.txt:145-147`). For 1066 this is exactly
how a 271-year situation supplies its beats.

**T4 — The visible/hidden `random_list` pair.**
`disasters/99_nd_dnm.txt:315-345` and `:82-95`. One `random_list` whose branches
are nothing but `custom_tooltip = an_event_occurs_tt` / `no_event_occurs_tt`
(so the tooltip honestly says "25% something happens"), and a second inside
`hidden_effect` that does the selection. Add **state-conditional entries**
(`2 = { trigger = { var:X >= 50 } … }`, lines 334-342) so the pool changes shape
as the player wins or loses.

**T5 — Accelerating pressure via a computed `chance`.**
`situations/nd_mandate_crisis.txt:155-166`:
`chance = { value = 20  if(released>=3) add 15  if(released>=6) add 15 }`.
Collapse should feel like collapse. Three lines.

**T6 — Perspective-gated GUI cards.**
`nd_dnm_reaction_of_the_reich.gui:232` and `:269`. One panel, different content
for the situation's protagonist, its antagonist, and bystanders, keyed off a
country variable and an IO-leader check respectively. The comment at :225-230
explains why the variable is the right key: "the variable dies with the country",
so a re-formed successor does not inherit the protagonist's panel.

**T7 — A five-branch `map_color` / `tooltip` / `legend_key` ladder driven by named
colours.** `situations/nd_mandate_crisis.txt:369-497` +
`main_menu/common/named_colors/99_nd_mandate_crisis.txt:2-6`. The same
if/else_if ladder is written three times against one colour table, so the map,
the hover text and the legend can never disagree. `require_color_on_map = yes`
on every legend entry.

**T8 — Give the antagonist real teeth, and take them back on resolution.**
`situations/99_nd_dnm.txt:114-121` grants the Emperor
`cb_imperial_ban` against the apostate on start; `:194-200` revokes it on end.
A pariah situation where the pariah only suffers a modifier is scenery; one
where a specific AI can legally invade is a situation.

**T9 — Express a war-score gate as a peace treaty, not a poll.**
`peace_treaties/99_nd_dnm.txt:16-62`. `cost = 80` *is* "80% war score", it is
visible in the peace UI, the player acts on it deliberately, and
`ai_desire = -100` makes the AI resist. The file's comment (1-15) is an
explicit post-mortem of the polling version it replaced.

**T10 — Master game rules with honest "disabled" descriptions.**
`main_menu/common/game_rules/99_nd_game_rules.txt` (3 rules, 38 lines) +
`nd_destinies_l_english.yml:5-7`. The disabled-state description enumerates what
still runs. For a total conversion this is how a large flavour layer stays
uninstallable-in-place.

### 7.2 Mistakes to avoid

**M1 — Do not let a comment assert a vanilla pattern you have not checked.**
`situations/99_nd_dnm.txt:19-20` states:
> `# can_start = { always = no }: started solely by activate_situation in`
> `# nd_dnm.1 (vanilla hussite_wars pattern).`

Measured: `VANILLA:in_game/common/situations/hussite_wars.txt:5-9` has a real
`can_start` (`c:BOH = { is_subject = no  religion = religion:hussite }`), and
**zero of vanilla's 23 situations use `can_start = { always = no }`.** The
technique itself is fine and `activate_situation` is genuine vanilla (6 uses,
e.g. `VANILLA:in_game/common/diseases/bubonic_plague.txt:165`) — but the
citation is false. A false citation in a comment is worse than none, because the
next reader stops checking. This is our citation rule, violated in a mod that is
otherwise the best-commented reference we have.

**M2 — Do not declare `effect` on a vanilla on_action without checking whether
vanilla already declares it.** `on_action/99_nd_on_actions.txt:1-21` documents
the shipped bug: `effect` is single-value, a second declaration is *silently*
discarded with only a `"There is more than one 'effect' defined"` log line, and
because the mod's filename sorted before vanilla's, **both** its handlers were
dropped. Result: three Workshop bug reports over six weeks (lines 42-43). The
same file also records inventing `on_country_yearly_pulse`, a hook name that
"appears nowhere in vanilla, so it was never called and the DNM succession chain
never fired" (lines 19-21). Two silent failures, one file. Our harness should
carry a check for both: (a) mod declares a field a vanilla file already
declares on the same on_action; (b) on_action name not present in vanilla.

**M3 — Do not build a 1,600-event corpus where every event is the same event.**
1 or 2 options, one timed modifier, zero `is_ai`, zero `ai_chance`, zero
`triggered_desc` outside a single file, 10 promote tokens in 1,773
descriptions. It reads well the first time and identically the twentieth. The
two situations show the author knows how to do better; the mass does not get
that treatment because the mass is too large to. **For 1066, prefer 40 events
with the DNM `.40-.47` shape over 400 with the `nd_arc.9` shape.**

**M4 — Do not duplicate a long branch ladder for a player-only variant.**
`events/situations/nd_mandate_crisis.txt:341-510`: the 11-tag else_if ladder
appears twice, ~170 lines, differing only by a trailing `change_player`. Any
edit must be made in both places and nothing will tell you if you miss one.
The scripted-effect machinery to avoid this already exists in the same mod
(`nd_mc_release_warlord_tag = { tag = $tag$ … }`,
`scripted_effects/nd_mandate_crisis_effects.txt:120-155`) — it just was not
taken one level further.

**M5 — Do not rely on `hint_tag` alone to surface a hint.**
`situations/99_nd_dnm.txt:24` sets `hint_tag = hint_nd_dnm_reaction_of_the_reich`
and the loc exists (`nd_dnm_l_english.yml:410-413`), but the mod ships **no**
`in_game/common/scriptable_hints/` file. Vanilla registers its situation hints
there — `VANILLA:in_game/common/scriptable_hints/scripted_hints.txt:691-693`
declares `hint_black_death = { priority = { can_see_situation = situation:black_death } }`.
**INFERENCE (not observed in game):** ND's hint is reachable only through the
panel's explicit `OpenLateralViewWithParams('hints', …)` button
(`nd_dnm_reaction_of_the_reich.gui:136`), not through the automatic hint alert.
If we want a 1066 situation's hint to surface on its own, we need the
`scriptable_hints` entry as well as the `hint_tag`.

**M6 (minor) — Watch the whole-file-override boundary.** ND uses `REPLACE:` 8
times, all in `in_game/common/formable_countries/`, and `INJECT:` 4 times.
`REPLACE:BYZ_trebizond_f` (`formable_countries/99_nd_byz.txt:71-126`) copies the
entire vanilla definition — including `unlock_policy_effect` calls for six
vanilla policies — in order to append two lines. The comment (61-70) admits the
copy is verbatim-plus-two. Every future vanilla patch to that formable is now
silently lost. Our `verify-vanilla-override` skill exists for exactly this.

---

## 8. VERIFICATION LEDGER

Claims checked against `VANILLA:` (`E:\SteamLibrary\steamapps\common\Europa Universalis V\game`):

| Construct | Status | Evidence |
|---|---|---|
| `dynamic_historical_event = { tag from to monthly_chance }` | vanilla-legal | 3,235 occurrences in `VANILLA:in_game/events/`; sample `VANILLA:in_game/events/ai_area_conqest_events/hidden_events_for_ai_conquest.txt:12-17` |
| `orphan = yes` on an event | vanilla-legal | 62 occurrences in `VANILLA:in_game/events/` |
| `<event_id>.entry` loc key | vanilla convention | 5,211 in `VANILLA:main_menu/localization/english/`; e.g. `flavor_ach.1.entry` |
| `hint_tag` on a situation | vanilla field | `VANILLA:in_game/common/situations/black_death.txt:4`, `colonial_revolution.txt:3`, `fall_of_delhi.txt:3` |
| `<hint_tag>` + `<hint_tag>_hint_text` + `_hint_text_<n>` loc | vanilla convention | `VANILLA:main_menu/localization/english/hints_l_english.yml:536-540` |
| Hint needs a `scriptable_hints` entry to auto-surface | vanilla does register it | `VANILLA:in_game/common/scriptable_hints/scripted_hints.txt:691-693` |
| `activate_situation = situation:X` | vanilla-legal | `VANILLA:in_game/common/diseases/bubonic_plague.txt:165`; `_hardcoded.txt:2074`; `events/DHE/flavor_tim.txt:653` |
| `custom_tooltip` + `hidden_trigger` inside an end-trigger `OR` | vanilla pattern | `VANILLA:in_game/common/scripted_triggers/disaster_triggers.txt:58-77` (hidden_trigger at 71-76) |
| `monthly_spawn_chance_low` = 0.02 | verified | `VANILLA:main_menu/common/script_values/default_values.txt:1206` |
| `monthly_spawn_chance_ultimate_high` = 0.5 | verified | same file:1211 |
| `monthly_spawn_chance_unique` = 1 | verified | same file:1212 |
| GUI widgets `situation_panel`, `situation_card_expandable`, `situation_fancy_two_line_card` | vanilla | `VANILLA:in_game/gui/panels/situation/black_death.gui` |
| GUI templates `one_country_header_template`, `two_countries_header_template` | vanilla | `VANILLA:in_game/gui/country_header.gui` |
| `TooltipRequirementsList` | vanilla | `VANILLA:in_game/gui/alertmanager.gui` |
| Situation GUI panel filename == situation key | vanilla convention | `VANILLA:in_game/gui/panels/situation/` — 23 files, all matching situation keys |
| `can_start = { always = no }` "is the hussite_wars pattern" | **FALSE** | `VANILLA:hussite_wars.txt:5-9` has a real `can_start`; 0 of 23 vanilla situations use `always = no` |

**Not verified (stated as INFERENCE above):**
- Why levies use the `00_` prefix while every other system uses `99_`.
- That `category = situation_event` events do not require an `.entry` key.
- That ND's `hint_nd_dnm_reaction_of_the_reich` does not auto-surface. This
  follows from the absent `scriptable_hints` file but was not observed in game.
- Every claim in ND's own source comments about engine behaviour (the
  single-value `effect` field, the "no `on_` prefix on pulses" rule, the
  inactive-disaster `can_end` polling, the "Invalid scope types … link: leader"
  error, the situation-scope `can_end` default-true fall-through). These are
  reported here **as the mod's testimony**, with `file:line`, not as verified
  engine facts. They are all worth independent confirmation before we build on
  them — but note that each is written as a post-mortem of a shipped bug, with
  dates and Workshop report references, which is the strongest form of
  third-party evidence available short of our own measurement.

Nothing in the source tree was created, edited or written. The only file written
by this task is this report.
