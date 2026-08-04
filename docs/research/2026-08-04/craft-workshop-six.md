# CRAFT SURVEY — situations in six numeric-ID workshop mods

Scope: `C:\Users\Desktop\eu5-modding-project-1.3.11\eu5-modding-project-1.3.11\reference_mods\{3603092142, 3613232232, 3633816300, 3668193813, 3698931463, 3735059838}`
Corpus: 10 situation definitions in 10 files, 5 GUI panels shipped (+1 fully commented out).
All paths below are mod-relative unless prefixed `VANILLA:`.
`VANILLA:` = `/e/SteamLibrary/steamapps/common/Europa Universalis V/game/…`
(sanity-checked against `reference_game_files/game/…` — `rise_of_the_ottomans.txt` is 594 lines in both, so the two copies are the same build).

---

## 0. Baseline established first (so mod deltas mean something)

The vanilla situations folder ships its own spec. `VANILLA:in_game/common/situations/readme.txt:4-18`:

```
# custom_description: <string> key for a custom description loc in customizable_localization
# monthly_spawn_chance: script value for how likely the disease is to spawn per month (0..1) (scope:situation is the situation)
# international_organization_type = <international_organization_type_tag> IO type associated with the situation
# resolution = <resolution_tag> a specific resolution that the situation references
# voters = <global_list_tag> list of people eligible to vote in the resolution above
# can_start = <trigger> can the situation start now (root = situation)
# can_end = <trigger> can the situation end (root = situation)
# visible = <trigger> can the player country see the situation and participate in it (root = country, scope:target = situation)
# on_start = <effect> effect when the situation starts, used for general set up (root = situation)
# on_monthly = <effect> effect every month (root = situation)
# on_ending = <effect> effect when the situation ends, just before its status changes (root = situation)
# on_ended = <effect> effect when the situation ends, just after its status changes (root = situation)
# tooltip = <effect> used to generate a tooltip for the map, not actually executed (root = location, scope:target = situation)
# map_color = <script color> map color for location (root = location, scope:target = situation)
# secondary_map_color = <script color> striped map color for location (root = location, scope:target = situation)
```

Facts derived from vanilla and used as the yardstick throughout:

| Fact | Citation |
|---|---|
| 22 situation definitions ship in vanilla (23 files minus `readme.txt`) | `VANILLA:in_game/common/situations/` |
| `on_ended` used 21× ; `on_ending` used 2× (`rise_of_the_ottomans.txt:297`, `treaty_of_tordesillas.txt:186`). Both legal, different timing (see readme lines 14-15) | as cited |
| `monthly_spawn_chance_unique = 1` — the value is a 0..1 probability | `VANILLA:main_menu/common/script_values/default_values.txt:1212` |
| `is_data_map = yes` is a real field, used by exactly 2 vanilla situations | `VANILLA:in_game/common/situations/black_death.txt:216`, `great_pestilence.txt:144` |
| `lerp = { min_color max_color factor }` is a real `map_color` form | `VANILLA:in_game/common/situations/black_death.txt:226-230` |
| `resolution` / `voters` are situation-level fields | `VANILLA:…/fall_of_delhi.txt:4-5`, `nanbokuchou.txt:3-4`, `western_schism.txt:4-5`, `council_of_trent.txt:4-5`, `guelphs_and_ghibellines.txt:2` |
| GUI panel file must be named after the situation and use `type situation_panel` | `VANILLA:in_game/gui/panels/situation/readme.txt:1-6`; type declared at `VANILLA:in_game/gui/panels/situation/common.gui:3` (`type situation_panel = lateralview`) |
| The default panel body is EMPTY — `block "situation_panel_main_content" {}` | `VANILLA:in_game/gui/panels/situation/common.gui:258` |
| The default header image is auto-derived from the key | `VANILLA:in_game/gui/panels/situation/common.gui:113-116`, `texture = "[GetSituationIllustration(SituationView.GetActiveSituation.GetSituation)]"`; promote exists at `docs/EU5-Vanilla-Script-Docs/data_types/data_types_uncategorized.txt:5359` |
| Art lives in `main_menu/gfx/interface/icons/situations/<key>.dds` and `main_menu/gfx/interface/illustrations/situation/<key>.dds` | `VANILLA:main_menu/gfx/interface/icons/situations/black_death.dds` etc.; there is a `_default.dds` fallback icon, e.g. `VANILLA:in_game/gui/government_lateralview.gui:656` |
| A `hint_tag` must name a registered scriptable-hint OBJECT, not just a loc key | `VANILLA:in_game/common/situations/rise_of_the_ottomans.txt:3` → `VANILLA:in_game/common/scriptable_hints/scripted_hints.txt:701` (`hint_rise_of_the_ottomans = { priority = { can_see_situation = … } hide = { … } sort_priority = 200 }`) |
| **`_info` and `_monthly` loc are OPTIONAL, not a required family.** Only 6 `_info` and 3 `_monthly` keys exist across 22 vanilla situations | `VANILLA:main_menu/localization/english/situations_l_english.yml:14,15,142,195,196,358,372,490,523` |
| `can_start = { always = no }` + external `activate_situation` is a real vanilla seeding shape | `VANILLA:in_game/common/situations/treaty_of_tordesillas.txt:9-10` (`#Activated by treaty_of_tordesillas.2`), fired at `VANILLA:in_game/events/situations/treaty_of_tordesillas.txt:325` |

**Calibration note for the parent session:** the task premise "all four situation key families (base/_desc/_info/_monthly)" is stricter than vanilla itself. Vanilla requires base + `_desc`; `_info` and `_monthly` are used by roughly a quarter and an eighth of situations respectively. Every one of the six mods ships base + `_desc`; **none** ships `_info`; exactly one ships `_monthly`. That is conformant, not deficient.

---

## 1. `3603092142` — **Historical Tweaks**

`.metadata/metadata.json`: `"name": "Historical Tweaks"`, `"id": "historical_tweaks"`, `"version": "1"`, `"supported_game_version": "1.0.10"`, `"short_description": "Makes some tweaks for more historical gameplay, such as nerfing france."`, tags `Balance / Fixes / Historical`.
Self-described scope in `README.md:1-45`: HYW nerfs to France, a Serbian-collapse situation, Ottoman/Mamluk railroading, unions, colonial railroading, Golden Horde collapse. It is a **mid-size historical-railroad mod that happens to contain the most ambitious situation work in this corpus.**

### 1.1 `rise_of_persia` — 447 lines, `in_game/common/situations/rise_of_persia.txt`

**Subject.** A post-Ilkhanate Persian unification race: the strongest Iranian-culture amir is tracked, ranked 1/2/3, and railroaded toward unifying Iran. It is a direct architectural port of vanilla `rise_of_the_ottomans`.

**Gates.** `rise_of_persia.txt:5-9`:
```
can_start = {
	current_date > 1420.1.1
	NOT = { country_exists = c:ILK }
	has_game_rule = historical_safavids
}
```
Date + tag-absence + a player-facing game rule. `monthly_spawn_chance = monthly_spawn_chance_unique` (line 2) = probability 1.

**Visibility** (`:15-31`) is a five-way OR: neighbour/rival/enemy/subject **of the currently-strongest amir read out of a situation variable** (`is_neighbor_of = situation:rise_of_persia.var:strongest_amir_variable`, line 20), plus presence in Persia / Khorasan / Caucasus / Crescent regions.

**Lifecycle in one paragraph.** `on_start` (`:34-165`) enumerates every non-TIM country with an Iranian-culture-group primary/accepted culture into a global list `eligible_amirs_list` and stamps each with `add_country_modifier = { modifier = ai_force_annexation years = -1 mode = add_and_extend }`; then runs three successive `ordered_in_global_list` passes with `order_by = { add = military_strength ; add = monthly_income_trade_and_tax }` and `max = 1` to write `strongest_amir_variable`, `second_strongest_strongest_amir_variable`, `third_strongest_strongest_amir_variable` plus their score variables onto the situation; notifies the winner (`rise_of_persia.2`) and every Persian-presence country (`rise_of_persia.1`); and if the Ilkhanate IO exists it is destroyed and its members get `rise_of_persia.900`. `on_monthly` (`:167-221`) calls one scripted effect `rise_of_persia_recalculate_top_3 = yes` (defined `in_game/common/scripted_effects/rise_of_persia_effects.txt:1`) and then a `random_list` with a 70% no-op, a 23% Safavid flavour branch gated on `c:ABL` existing and `current_year < 1545`, a 4% integration-accelerator and a 3% neighbour-subjugation branch. `on_ending` (`:224-285`) forks: if the amir list is empty (or it is past 1565 and the leader is still under 500 locations) it fires failure events `rise_of_persia.500` / `.3`; else it strips `ai_force_annexation` from everyone, fires `.4` to the losers and `.5` to the winner, clears the global list and removes the three score variables.

**Phases / variables.** No phase counter. State is five situation-scope variables (three country pointers + three score numbers, one of which — `strongest_strongest_amir_total_score_variable` — is set and later removed) and one global variable list, plus a per-country cooldown variable `rise_of_persia_vassal_cooldown_variable`.

**Actions.** Four `type = situation` generic actions in `in_game/common/generic_actions/rise_of_persia.txt` (476 lines): `press_persian_claims` (:1), `claim_persian_mantle` (:237), `annex_persian_amir` (:300), `restore_persian_cities` (:361). All use the two-stage `select_trigger` idiom — first `looking_for_a = situation` with `interaction_source_list = { situation:rise_of_persia = { add_to_list = source } }` and `target_flag = recipient` (`:27-43`), then `looking_for_a = province` with `target_flag = target` and per-column `data = owner_flag / name / population` (`:45-52`). AI participation is gated by `in_game/common/generic_action_ai_lists/rise_of_persia.txt:3` (`can_see_situation = situation:rise_of_persia`).

**Map colours.** `map_color` (`:342-366`) paints locations owned by amir 1/2/3 in that country's own `country_color`, else `define:NMapColors|DEFAULT_COLOR`. `secondary_map_color` is used for subject stripes. Three `legend_key` blocks (`:389-403`).

**Resolution use.** None.

**Out-of-situation plumbing.** `in_game/common/on_action/rise_of_persia.txt:1-5` hooks `on_annexed` → `on_rise_of_persia_annexed`, which re-runs the recalculation and prunes the annexed country out of `eligible_amirs_list` (`:20-32`). End conditions are a named scripted trigger, `in_game/common/scripted_triggers/situation_end_triggers.txt:1-25` (`rise_of_persia_end_trigger`), wrapping the real check in `custom_tooltip = { text = … <trigger> }` so the panel prints readable requirements.

### 1.2 `wot_turkish_expansion` — 141 lines, `in_game/common/situations/wot_turkish_expansion.txt`

A late-Ottoman expansion phase that fires **after** vanilla's own Rise of the Ottomans concludes. Gates (`:5-11`): `current_date > 1444.1.1`, `current_date < 1500.1.1`, `country_exists = c:TUR`, `situation:rise_of_the_ottomans = { situation_is_active = no }`, `c:TUR = { num_locations > 500 }`. Lifecycle is thin: `on_start` (`:29-49`) fires `wot_ottoman_extras.10` to everyone in a wide neighbour/Middle-East/North-Africa/Eastern-Europe net and `.9` to TUR; **`on_ended`** (`:51-70`) fires `.11` / `.12` to the same sets. No `on_monthly`, no variables, no phases. `tooltip` (`:72-93`) and `map_color` (`:95-120`) are a five-branch relationship read (us / allies / subjects / currently invaded / future target) with four `legend_key` entries (`:122-141`), two of which point at game-concept keys with an in-source note: `desc = "game_concept_ally" #Until loc fix` (`:128`). One `type = situation` action in `in_game/common/generic_actions/wot_turkish_expansion.txt` (103 lines) that fires `wot_ottoman_extras.100` (`:71`).

### 1.3 `htc_conquest_of_india` — **122 lines, 100% commented out**

`in_game/common/situations/htc_conquest_of_india.txt` — every line is `#`-prefixed. So is its event file (`in_game/events/situations/htc_conquest_of_india.txt`, 39 lines, all `#`), its panel (`in_game/gui/panels/situation/conquest_of_india.gui`, 94 lines, **zero** non-comment non-blank lines — measured), its generic actions (`in_game/common/generic_actions/htc_conquest_of_india.txt`, 362 lines, 1 live line: the BOM-carrying `# htc_coi_purchase_province = {`), its AI list (`in_game/common/generic_action_ai_lists/htc_conquest_of_india_list.txt`) and its scripted effects (`in_game/common/scripted_effects/htc_coi_effects.txt`). A grep for live `situation:conquest_of_india` references across the whole mod returns **nothing**. A whole six-file feature parked cleanly with no orphans.

### 1.4 GUI

Three panels, `in_game/gui/panels/situation/`: `rise_of_persia.gui` (256), `wot_turkish_expansion.gui` (134), `conquest_of_india.gui` (94, dead). Base copied = **`rise_of_the_ottomans`-family**: both live panels `blockoverride "situation_panel_image"` with `using = one_country_header_template` and a `datacontext` reading the situation variable — `rise_of_persia.gui:14`:
```
datacontext = "[SituationView.GetActiveSituation.GetSituation.MakeScope.GetVariable('strongest_amir_variable').GetCountry]"
```
`rise_of_persia.gui` additionally builds a full three-country score ladder (`left_flag` / `right_flag` / `left_top_text` / `right_bottom_text` blockoverrides, `:147-254`). `wot_turkish_expansion.gui` overrides `situation_header_left` and `situation_header_right` with an army-strength readout for `[GetCountry('TUR')…]` (`:5-42`). Both open the hints lateral view: `rise_of_persia.gui:71` / `wot_turkish_expansion.gui:127`, `on_action = "[OpenLateralViewWithParams('hints', 'selected_hint = hint_…')]"`.

### 1.5 Events

3 files under `in_game/events/situations/`: `rise_of_persia.txt` (450 lines, 12 events: `.1 .2 .3 .4 .5 .100 .101 .102 .103 .104 .105 .500 .900`), `wot_ottoman_extras.txt` (98 lines, 6 events), `htc_conquest_of_india.txt` (dead). Every event carries `type = country_event` + `category = situation_event`. Firing idioms: `trigger_event_non_silently` from situation hooks and from within events, `trigger_event_silently` from generic actions. Option architecture is two-tier: notification events carry a single acknowledging option (`rise_of_persia.txt:124`, `:136`), while decision events carry a real branch — `rise_of_persia.101` picks up to five candidate vassals via `ordered_neighbor_country` with a weighted `order_by`, saves one to `scope:target_country`, then offers option **a** (`custom_tooltip` + `trigger_event_silently = rise_of_persia.102`, `:243-247`) versus option **b** (stamp a 5-year `rise_of_persia_vassal_cooldown_variable` on the target, `:249-259`). Options attach real mechanics: `add_casus_belli = { target = … type = casus_belli:cb_unify_persia province = … }` (`:171`) followed by `refresh_map_colors = yes`.

### 1.6 Loc

`main_menu/localization/english/wot_situations_l_english.yml` (75 lines) + two event loc files. Key families: `rise_of_persia` / `_desc` / `_cooldown` (`:3-5`); `wot_turkish_expansion` / `_desc` (`:52-53`). **No `_info`, no `_monthly`.** Rich supporting keys — a `_victory_conditions` key that inlines `[SituationView.GetTooltipInformation('rise_of_persia_end_trigger_amir_victory')]` (`:2`), score tooltips, action names and descs, and two `MODIFIER_TYPE_NAME_/DESC_` pairs (`:43-48`).
**Hint entries: MISSING.** `rise_of_persia.txt:3` and `wot_turkish_expansion.txt:3` declare `hint_tag = hint_rise_of_persia` / `hint_wot_turkish_expansion`, but the mod ships no `scriptable_hints` file anywhere and no `hint_*` loc key at all (grep across the whole mod returns only the two declarations and the two GUI `OpenLateralViewWithParams` calls).

### 1.7 Art

`main_menu/gfx/interface/icons/situations/rise_of_persia.dds`, `…/wot_turkish_expansion.dds`, and `main_menu/gfx/interface/illustrations/situation/wot_turkish_expansion.dds`. Correct tree. `rise_of_persia` has no illustration, but its panel overrides `situation_panel_image` (`rise_of_persia.gui:10`) so the auto-derived texture is never requested.

### 1.8 ★ Technique worth stealing

**Wrap the end condition in a named scripted trigger built out of `custom_tooltip` blocks, then print it into the panel with `GetTooltipInformation`.** `in_game/common/scripted_triggers/situation_end_triggers.txt:1-25` defines `rise_of_persia_end_trigger` where each real clause is inside `custom_tooltip = { text = <key> <trigger> }`; a second trigger `rise_of_persia_end_trigger_amir_victory` (`:27-38`) exists **only** to be rendered, and is pulled into the panel text at `main_menu/localization/english/wot_situations_l_english.yml:2` via `[SituationView.GetTooltipInformation('rise_of_persia_end_trigger_amir_victory')]`. One source of truth for "when does this end", displayed and evaluated from the same script. Directly applicable to Manzikert.

### 1.9 ⚠ Mistake to avoid

**A ported `legend_key` whose `desc` and `color` were not re-paired.** `rise_of_persia.txt:389-393`:
```
legend_key = { 
	desc = "STRONGEST_AMIR_TOOLTIP"
	color = situation:rise_of_persia.var:second_strongest_strongest_amir_variable.country_color
	require_color_on_map = yes
}
```
The vanilla original it was copied from is correct — `VANILLA:in_game/common/situations/rise_of_the_ottomans.txt:523-527` pairs `desc = "STRONGEST_BEYLIK_TOOLTIP"` with `strongest_beylik_variable.country_color`. The mod's #1 legend swatch therefore shows #2's colour. **Silent — no error, and only visible by looking at the map legend next to the map.**

Three further defects in the same file, all silent:
- **Duplicate `secondary_map_color`.** Declared twice: `:368-387` and again `:405-447`. The second is a superset; which one wins is UNVERIFIED, but one of the two is dead script.
- **Stale in-source pointer.** `:169` reads `###########See in_game\common\scripted_effects\situation_effects############` — no such file exists in the mod; the effect actually lives in `in_game/common/scripted_effects/rise_of_persia_effects.txt:1`.
- **Loc/logic drift.** `wot_situations_l_english.yml:21` `no_amir_has_100_locations_tt: "…at least 100 locations"` and key name `strongest_amir_has_over_75_locations` (`:25`) both describe thresholds the code no longer uses — `situation_end_triggers.txt:16-17` checks `num_locations > 600` and `num_of_non_rural >= 50`, and the loc *body* at `:25` says 600. Key name, sibling key, and code disagree three ways.
- **Out-of-range spawn chance.** `wot_turkish_expansion.txt:2` `monthly_spawn_chance = 100` against a documented 0..1 field (`VANILLA:…/readme.txt:5`) whose "always" constant is `1` (`VANILLA:main_menu/common/script_values/default_values.txt:1212`). Probably clamped and harmless; non-idiomatic and worth not copying.

---

## 2. `3613232232` — **Prosper or Perish**

`.metadata/metadata.json`: `"name": "Prosper or Perish"`, `"id": ""` (**empty**), `"version": "0.9.1"`, `"supported_game_version": "1.3.11"`, tags `Advancements / Balance / Gameplay / Overhaul / Trade and Economics`. Self-described as an economic and demographic overhaul: "This mod disentangles Population Growth from Prosperity, making Food the primary driver of pop growths and migration."

### 2.1 `harvest_situation` — 271 lines, `in_game/common/situations/pp_variable_harvest_situation.txt`

**⚠ The situation KEY is `harvest_situation` (`:1`), not the filename `pp_variable_harvest_situation`.** Every cross-reference must use the key, and the mod's own loc lives in a third file again (`pp_europedia_l_english.yml`, not `pp_situations_l_english.yml`).

**Subject.** A permanent world-wide September harvest lottery. `can_start = { always = yes }` (`:4-6`), `can_end = { always = no }` (`:8-10`) — it is a **permanent host**, not an episode. `visible = { NOT = { has_game_rule = pp_variable_harvest_disabled } }` (`:12-14`) — player-facing opt-out via game rule.

**Lifecycle.** `on_start` is empty (`:15-16`). `on_monthly` is four lines (`:17-25`): `if current_month = 9` and the rule is on → `apply_regional_harvest_effect = yes`, one scripted effect defined at `in_game/common/scripted_effects/pp_variable_harvest_effects.txt:3` in a **1380-line** file of per-broad-area shock effects (`pp_apply_australasia_harvest_shock_bad` at `:244`, `…_neutral` at `:253`, `…_good` at `:262`, and so on for 17 broad areas × 3 outcomes). The situation is a scheduler; the mass lives in scripted effects.

**Map colours.** The bulk of the file (`:72-233`) is a seven-tier `map_color` cascade keyed on `has_location_modifier = pp_harvest_<broad_area>_<tier>` — 17 modifiers ORed per tier, 6 tiers, plus a starvation override and a default. Nine `legend_key` blocks (`:235-270`). Colours come from `define:NMapColors|MAP_COLOR_MIN/LOW/MID/HIGH/MAX/TOP` and `POPULATION_STARVING_COLOR_STRIPE`. `tooltip` (`:26-49`) stacks three independent `if` blocks (not `else_if`) so a starving + negative-balance + extended-winter location prints all three lines.

**⚠ Dead code.** `on_ended` (`:50-69`) fires `little_ice_age.100` to every extended-winter capital and strips `harsh_winters_modifier` from every location on earth — but `can_end = { always = no }` means it can never run. It reads as copy-paste from `little_ice_age`.

### 2.2 `pp_mod_welcome_situation` — 35 lines, `in_game/common/situations/pp_mod_welcome_situation.txt`

A **year-one onboarding notice**, self-documented at `:1`: `# Year-one onboarding: from game start, ends after one in-game year (once per campaign).` Gated on a global flag pair (`:5-8`): `has_global_variable = pp_mod_welcome_situation_pending` AND `NOT = { has_global_variable = pp_mod_welcome_situation_completed }`. `can_end = { years_since_situation_start >= 1 }` (`:10-12`). `visible = { is_human = yes }` (`:14-16`). `on_start` removes the pending flag (`:19`); `on_ended` sets the completed flag (`:22-27`). `map_color` is a stub returning `DEFAULT_COLOR` (`:29-34`). No events, no actions, no variables beyond the two flags.

**Seeding (quote).** `in_game/common/on_action/pp_game_start.txt:4-16` runs `on_game_start = { on_actions = { pp_mod_welcome_situation_game_start … } }`; the entry itself, `:126-149`, is commented in source:
```
# Flags the welcome situation to spawn on the next monthly situation check (once per campaign).
# Do not re-set pending while the situation is already active (e.g. loading a save mid year-one).
pp_mod_welcome_situation_game_start = {
	effect = {
		if = {
			limit = {
				NOT = { has_global_variable = pp_mod_welcome_situation_completed }
				situation:pp_mod_welcome_situation = { situation_is_active = no }
			}
			set_global_variable = { name = pp_mod_welcome_situation_pending value = yes }
		}
	}
}
```

### 2.3 GUI — **none**

Neither situation has a file in `in_game/gui/panels/situation/`; the directory does not exist in this mod (`find` for `*.gui` returns only encyclopedia and tooltip files). So both panels render with the default empty body (`VANILLA:…/common.gui:258`). The `harvest_situation` panel would also request `gfx/interface/illustrations/situation/harvest_situation.dds`, which is not shipped. **They do not appear to know**, or they accepted it: the mod's own documentation strategy is the Europedia instead — the loc `harvest_situation_desc` is a 6-paragraph Europedia article (`pp_europedia_l_english.yml:18`) and the welcome situation's desc points the player at Europedia ("I've documented Prosper or Perish extensively in the Europedia", `pp_situations_l_english.yml:3`).

### 2.4 Loc

Split across two files. `main_menu/localization/english/pp_situations_l_english.yml` (15 lines) carries `pp_mod_welcome_situation` / `_desc` (`:2-3`), the three harvest tooltip keys (`:4-6`) and nine `PP_HARVEST_LEGEND_KEY_*` (`:7-15`). `main_menu/localization/english/pp_europedia_l_english.yml` carries `harvest_situation` (`:17`), `harvest_situation_desc` (`:18`) and — uniquely in this corpus — **`harvest_situation_monthly`** (`:19`), plus `game_concept_harvest_situation` / `_desc` (`:13-14`). No `_info`. No hint entries and no `hint_tag` declared.

**⚠ Loc indentation.** Verified by byte-read: in `pp_europedia_l_english.yml` the keys sit at **column 0** — `harvest_situation: "P&P: Variable Harvests"` with no leading space — whereas every vanilla entry and PP's own `pp_situations_l_english.yml` uses a single leading space (` pp_mod_welcome_situation: …`). Whether the EU5 yml reader tolerates column-0 keys is **UNVERIFIED**; the deviation itself is measured.

### 2.5 Art — **wrong tree**

`in_game/gfx/interface/icons/situations/pp_mod_welcome_situation.dds`. Vanilla ships all situation icons under `main_menu/gfx/interface/icons/situations/`. No icon at all for `harvest_situation`.

### 2.6 ★ Technique worth stealing

**The situation as a pure monthly scheduler with the mass in scripted effects, plus a game-rule opt-out wired into `visible`.** `pp_variable_harvest_situation.txt:17-25` is nine lines of `on_monthly` calling one effect; the 1380-line implementation is `in_game/common/scripted_effects/pp_variable_harvest_effects.txt`. The same game rule appears in both `visible` (`:13`) and inside `on_monthly` (`:21`), so turning the rule off hides the panel AND stops the tick — the situation is not merely invisible, it is inert.

### 2.7 ⚠ Mistake to avoid

**A never-reachable `on_ended` on a `can_end = { always = no }` situation.** `pp_variable_harvest_situation.txt:8-10` vs `:50-69`. The block strips `harsh_winters_modifier` from every location in the world and fires `little_ice_age.100` — real, expensive, and dead. Nothing errors. If a later edit ever makes `can_end` reachable, that block executes a global winter cleanup nobody remembered writing.

---

## 3. `3633816300` — **OGAS Optimized**

`.metadata/metadata.json`: `"name": "OGAS Optimized"`, `"id": "ogasoptimized"`, `"version": "20260209"`, `"supported_game_version": "1.1.*"`, `"short_description": "Optimized Auto Road Builder"`, tags `Fixes / Gameplay / Utilities`. A 21-file utility mod, localized into **11 languages** (`main_menu/localization/{braz_por,english,french,german,japanese,korean,polish,russian,simp_chinese,spanish,turkish}/OGAS_l_*.yml`).

### 3.1 `OGAS` — 95 lines, `in_game/common/situations/OGAS_situations.txt`

**Subject.** This is not a historical situation at all. It is **a situation used as a UI host**: the panel is the mod's control surface for an automatic road-builder, and the map colouring is its progress readout.

**Gates.** `:2` `monthly_spawn_chance = 1` (= always). `can_start` is an **empty block** with the discovery recorded inline (`:5-8`):
```
can_start = {
	#this scope is situation not country
	#is_ai = no
}
```
`can_end = { always = no }` (`:10-12`). `visible = { is_ai = no }` (`:14-16`) — player-only, and the comment above explains why `is_ai = no` had to move out of `can_start`: `can_start`'s root is the situation, not a country. That matches `VANILLA:in_game/common/situations/readme.txt:9,11`.

**Lifecycle.** `on_start = {}` and `on_monthly = {}` are both empty (`:18-22`). All work happens in `in_game/common/on_action/OGAS_country_monthly.txt` and the scripted effects. **The situation contributes zero simulation** — only `visible`, `tooltip`, `map_color` and a panel.

**Map colours.** `is_data_map = yes` (`:75`) — the same flag vanilla uses for the two plague maps (`VANILLA:black_death.txt:216`, `great_pestilence.txt:144`). Three-way colour on `has_variable = OGAS_Cache_Auto_Road_Complete` / `_Ongoing` / else (`:77-94`). `tooltip` (`:24-73`) branches on a country variable `OGAS_Auto_Road_Mode` (1 = proximity, 2 = market access) crossed with the two cache variables — six distinct tooltip keys. No `legend_key`.

**Actions / events / resolution.** None of any kind. Zero events in the whole mod.

### 3.2 GUI — **yes, and it is the point**

`in_game/gui/panels/situation/OGAS.gui`, 164 lines, filename matches the key. Base copied: minimal — only `situation_subheader_content` (`:10`), `situation_panel_main_content` (`:13`) and `situation_panel_main_content_bottom` (`:100`) are overridden; header, image and subheader are left at vanilla defaults. Inside, the panel is a **control board**: a `situation_card_expandable` intro card (`:14-29`), a gold-reserve stepper with four `button_regular` (`-10k / -1k / +1k / +10k`, `:56-85`), an `AutomationCheckbox` (`:89-97`), two mutually-exclusive `checkbutton_02_alt` mode buttons (`:110-148`) and an initialise button (`:151-160`). Every control is a scripted-GUI call, e.g. `:159`:
```
onclick = "[GetScriptedGui('OGAS_Auto_Road_Initialize_sgui').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
```
Targets defined in `in_game/common/scripted_guis/OGAS_sgui.txt` — `OGAS_Auto_Road_Initialize_sgui` (`:1`), `OGAS_Auto_Road_Construct_sgui` (`:10`), `OGAS_Auto_Road_Set_Mode_Proximity_sgui` (`:50`), `…_Market_Access_sgui` (`:60`) — each `scope = country` with `is_shown` / `is_valid` / `effect`.

**⚠ Missing illustration.** `OGAS.gui` does NOT override `situation_panel_image`, so the default at `VANILLA:…/common.gui:113-116` requests `gfx/interface/illustrations/situation/OGAS.dds`, and the mod ships **no** `.dds` at all. The panel header image will not resolve.

### 3.3 Loc

`main_menu/localization/english/OGAS_l_english.yml`: `OGAS` (`:2`), `OGAS_desc` (`:3`), the six tooltip keys (`:4-9`) and nine UI strings (`:10-19`). No `_info`, no `_monthly`. **No hint entries — and correctly so**, because `:3` of the situation file is `#hint_tag = hint_OGAS`, commented out. This is the only mod in the corpus that got the hint question right.

### 3.4 ★ Technique worth stealing

**Use a permanent, `is_ai = no`-gated, effect-free situation purely as a hosted GUI panel and a data map.** `OGAS_situations.txt:10-22` — `can_end = { always = no }`, `visible = { is_ai = no }`, both hooks empty, `is_data_map = yes` at `:75` — combined with `OGAS.gui`'s scripted-GUI buttons. This is the cheapest legal way to give a mod a persistent, map-linked settings/status panel in EU5, with no ongoing simulation cost and no chance of an accidental end. For 1066 this is the shape for any "mod control panel" or "campaign dashboard" you might want alongside the historical situations.

### 3.5 ⚠ Mistake to avoid

**Not overriding `situation_panel_image` while also shipping no illustration.** `OGAS.gui` has no `blockoverride "situation_panel_image"` (measured: its only blockoverrides are at `:10, :13, :15, :17, :20, :100`), so the vanilla default at `VANILLA:in_game/gui/panels/situation/common.gui:113-116` resolves `[GetSituationIllustration(...)]` against a file that does not exist in the mod. Either ship `main_menu/gfx/interface/illustrations/situation/<key>.dds` or blockoverride the image — the other four GUI-shipping mods in this corpus all do the latter.

---

## 4. `3668193813` — **National Destinies**

`.metadata/metadata.json`: `"name": "National Destinies"`, `"id": "trin.national_destinies"`, `"version": "1.3.0"`, `"supported_game_version": "1.*.*"`, `"game_id": "eu5"`, `"short_description": "Adds unique, historically-themed bonuses to every formable country in EU5."`, tag `Gameplay`. It ships ~190 English loc files, one per formable. **The richest and best-documented situation work in the corpus.**

### 4.1 `nd_dnm_reaction_of_the_reich` — 226 lines, `in_game/common/situations/99_nd_dnm.txt`

**Subject.** The diplomatic backlash when a player forms the Danubian Monarchy (`DNM`) by walking out of the HRE. The file opens with a 21-line design header (`:1-21`) that states the design contract, the three exits, and the seeding decision.

**Gates.** `can_start = { always = no }` (`:26-28`) — seeded exclusively from outside.

**Seeding (quote).** `99_nd_dnm.txt:19-20`:
```
# can_start = { always = no }: started solely by activate_situation in
# nd_dnm.1 (vanilla hussite_wars pattern).
```
Actual firing sites: `in_game/events/nd_dnm.txt:61` and `:87`, both `activate_situation = situation:nd_dnm_reaction_of_the_reich`.
**⚠ The comment misattributes the pattern.** `VANILLA:in_game/common/situations/hussite_wars.txt:5-11` has a real `can_start` trigger on `c:BOH`. The vanilla situation that actually uses `can_start = { always = no }` + external `activate_situation` is **`treaty_of_tordesillas`** — `VANILLA:…/treaty_of_tordesillas.txt:9-10` (`#Activated by treaty_of_tordesillas.2`), fired at `VANILLA:in_game/events/situations/treaty_of_tordesillas.txt:325`.

**`can_end` uses an undocumented construct — see §4.5.**

**Visibility.** `:90-96`, three-way OR (`tag = DNM` / HRE member / `has_presence_in = continent:europe`), with the reason recorded at `:83-89` including the observed failure: *"Without this the situation showed on every country's map worldwide."*

**Lifecycle.** `on_start` (`:98-133`) stamps DNM with a permanent `nd_dnm_reich_pariah` modifier (`years = -1 mode = add_and_extend`), fires `nd_dnm.25` to DNM, hands the Emperor `casus_belli:cb_imperial_ban` against `c:DNM` and fires `.26` to the Emperor and the Papacy. `on_monthly` (`:155-173`) is deliberately small: one `random_country` limited to DNM-with-pariah, gated on a cooldown modifier, running `random_list = { 97 = {} 3 = { trigger_event_non_silently = nd_dnm.27 } }`. `on_ended` (`:175-208`) strips the pariah modifier, fires `.29`, then idempotently removes six chain modifiers, and finally revokes the Emperor's `cb_imperial_ban` — with the reason stated at `:196-199` (*"Without this the CB would sit in the Emperor's pocket forever after a political settlement"*).

**Phases / variables.** Country-scope variables on DNM: `nd_dnm_ps_resolved`, `nd_dnm_reich_humbled`, `nd_dnm_pariah_timer`. No phase counter — the chain lives in a disaster and a yearly pulse (`:151-154` points at `common/on_action/99_nd_on_actions.txt`'s `on_country_yearly_pulse`).

**Map.** `tooltip` is a single `custom_tooltip = nd_dnm_reaction_of_the_reich_tt` (`:210-212`); `map_color` is two-branch (DNM's own colour, else default, `:214-225`). No `legend_key`.

### 4.2 `nd_mandate_crisis` — 498 lines, `in_game/common/situations/nd_mandate_crisis.txt`

**Subject.** A Chinese dynastic-cycle fragmentation crisis driven off the `middle_kingdom` IO's `celestial_authority`.

**Gates.** `:4-31`, the most conditional `can_start` in the corpus: a game rule (`has_game_rule = nd_mandate_crisis_enabled`), the IO and its leader existing, `NOT = { is_situation_active = situation:red_turban_rebellions }` (explicit non-overlap with vanilla), a cooldown variable check, no active disaster, not in civil war, `var:celestial_authority <= 30`, and a nested `weighted_calc_true_if = { amount >= 2 … }` over stability / government power / legitimacy / estate satisfaction. `monthly_spawn_chance = monthly_spawn_chance_low` (`:2`) — the only non-`unique` spawn chance in the corpus.

**Lifecycle.** `on_start` (`:64-104`) destroys any stale `nd_mandate_challengers` IO, initialises `nd_mc_phase = 1` and `nd_mc_tags_released = 0` on the Emperor, applies `nd_mandate_crisis_unrest` with `months = -1 mode = replace`, and notifies the Emperor (`.1`) plus East-Asian neighbours (`.2`, delayed `days = 1`). `on_monthly` (`:105-283`) is a two-phase state machine: **Phase 1** rolls a 6-way flavour `random_list` (`.10`–`.15`) and tests the transition (`years_since_situation_start > 0` AND `celestial_authority < 20` → set `nd_mc_phase = 2`, swap `nd_mandate_crisis_unrest` for `nd_mandate_crisis_fragmentation`, fire `.23`); **Phase 2** runs an accelerating release lottery (base `chance = 20`, `+15` at 3 released, `+15` more at 6) over eleven historical warlord tags each gated by `nd_mc_can_release_tag = { tag = MNG location = shangyuan }` etc. (`:169-223`), with a `50 = { … }` dynamic-culture fallback firing `.21` and a `100 = { }` no-op; plus a 3% foreign-opportunity branch (`.32`). A separate block (`:261-282`) lets hostile challengers "claim the mandate" (`.31`). `on_ended` (`:285-367`) picks one of three outcomes by trigger order — **Path C** New Dynasty (challenger holds ≥65% of IO land, `percent >= 0.65`), **Path A** Reform (still Phase 1), **Path B** Reconquest (fallback) — each stamping a 10-year modifier and firing `.5` / `.3` / `.4`; then cleans up variables, strips `nd_mc_emperor_allegiance` from every country, and destroys the challenger IO.

**Phases / variables.** Explicit: `nd_mc_phase` (1/2), `nd_mc_tags_released`, `nd_mc_emperor_allegiance` (per warlord, thresholded at ≥50 loyalist / <0 rebel), `nd_mc_claimed_mandate`, `nd_mc_cooldown`, and eleven `nd_mc_release_current_tag_<TAG>` flags.

**Actions.** Eight `type = situation` generic actions in `in_game/common/generic_actions/nd_mandate_crisis.txt`: `nd_mc_reform_bureaucracy` (:3), `nd_mc_purge_eunuchs` (:63), `nd_mc_appease_generals` (:123), `nd_mc_grant_autonomy` (:189), `nd_mc_negotiate_surrender` (:246), `nd_mc_imperial_edict` (:365), `nd_mc_declare_loyalty` (:435), `nd_mc_seek_mandate` (:512) — Emperor-side and warlord-side both playable. AI gating in `in_game/common/generic_action_ai_lists/nd_mandate_crisis_list.txt`.

**Map.** Five-branch `map_color` with explicit `rgb { … }` literals rather than named colours (`:421-471`) and **five matching `legend_key` blocks** with `require_color_on_map = yes` (`:473-497`) — the only mod in the corpus whose legend is one-to-one complete with its colour cascade.

**IO use.** A custom IO, `in_game/common/international_organizations/nd_mandate_challengers.txt`, created for the crisis and destroyed on end (`:363-366`). Note the situation does **not** declare `international_organization_type`; vanilla does that at `VANILLA:western_schism.txt:5` / `council_of_trent.txt:4`.

### 4.3 GUI — yes, two, both provenance-documented

`in_game/gui/panels/situation/nd_dnm_reaction_of_the_reich.gui` (301) and `nd_mandate_crisis.gui` (189). Both open with a header block naming the exact vanilla panels each pattern came from — `nd_mandate_crisis.gui:1-10`:
```
# Patterns borrowed from:
#   - the_revolution.gui (one_country_header_template anchored on a focal country)
#   - nd_dnm_reaction_of_the_reich.gui (header counters, expandable cards,
#     TooltipRequirementsList end-requirements card)
```
and `nd_dnm_reaction_of_the_reich.gui:10-15` names `hussite_wars.gui`, `the_revolution.gui`, `middle_kingdom.gui` and `left_panel.gui`. The DNM panel uses the **two-country** header (`blockoverride "FirstCountryContext"` / `"SecondCountryContext"`, `:73-80`) and switches whole cards on perspective (DNM / Emperor / third party, documented at `:3-8`); the crisis panel uses the one-country header with phase and release counters in `situation_header_left` / `_right` (`:17-63`). Both override `situation_panel_image` (`:70` / `:64`), which is necessary because **this mod ships no situation `.dds` at all**.

### 4.4 Events and loc

`in_game/events/situations/nd_mandate_crisis.txt` — 776 lines, **17 events** (`.1 .2 .3 .4 .5 .10–.15 .20 .21 .23 .30 .31 .32`), 28 `option` blocks, every one `type = country_event` + `category = situation_event`. `in_game/events/nd_dnm.txt` — 1219 lines, 39 `nd_dnm.*` events of which `.25 .26 .27 .29 .30 .31 .32 .33` serve the situation. Firing idioms: `trigger_event_non_silently = <id>` and the delayed block form `trigger_event_non_silently = { id = nd_mandate_crisis.2 days = 1 }` / `{ id = … days = { 5 15 } }`. Option architecture: notification events take one acknowledging option; decision events pair a cost-bearing option against a decline, and options attach modifiers, variables and CBs (`nd_mandate_crisis.txt:765` `type = casus_belli:cb_conquer_enemy`).
**⚠ `nd_dnm.28` does not exist** — deliberately, and the deletion is recorded at `99_nd_dnm.txt:148-150`.

Loc: `main_menu/localization/english/nd_dnm_l_english.yml` (592 lines) has `nd_dnm_reaction_of_the_reich` (`:251`), `_desc` (`:252`), `_tt` (`:253`); `nd_mandate_crisis_l_english.yml` (306 lines) has `nd_mandate_crisis` (`:11`) and `_desc` (`:12`) plus game-rule loc (`:4-8`). No `_info`, no `_monthly` for either.
**Hint entries: present in loc, absent as objects.** `nd_dnm_l_english.yml:410-413` ships the full vanilla-shaped set — `hint_nd_dnm_reaction_of_the_reich`, `_hint_text`, `_hint_text_1`, `_hint_text_2`, matching `VANILLA:main_menu/localization/english/hints_l_english.yml:561-562` — but the mod ships **no `scriptable_hints` file**, so `99_nd_dnm.txt:24`'s `hint_tag = hint_nd_dnm_reaction_of_the_reich` names a hint object that is never registered (contrast `VANILLA:in_game/common/scriptable_hints/scripted_hints.txt:701`).

### 4.5 ⚠ THE BIG ONE — `end_reason`, zero vanilla attestation

Both ND situations use a `can_end` form this survey could not attest anywhere. `99_nd_dnm.txt:41-51`:
```
can_end = {
	# Legitimacy path: the succession crisis has been settled.
	end_reason = {
		trigger = {
			any_country = { tag = DNM has_variable = nd_dnm_ps_resolved }
		}
		desc = nd_dnm_ps_resolved_end_tt
	}
	…
}
```
Four `end_reason` blocks there (`:43, :53, :63, :75`), one in `nd_mandate_crisis.txt:34-37`. The mod's own comment (`99_nd_dnm.txt:38-40`) claims *"1.3: can_end takes end_reason blocks (trigger + desc), any one of which ends the situation."*

**Measured:** `grep -rn "end_reason"` returns **zero** matches in `VANILLA:in_game/common/situations/` **and** zero in `reference_game_files/game/in_game/common/situations/`, and zero in `reference_official_defines/`. It is not in `VANILLA:in_game/common/situations/readme.txt`. Status: **UNVERIFIED**. Either it is a field added after both game copies on hand, or it is invented and the four blocks are unknown keys — in which case `can_end` has no real clause and the situation's end behaviour is undefined. **This construct must not be copied into 1066 without in-game evidence.**

### 4.6 ★ Technique worth stealing

**Record the engine's actual error next to the workaround, in the file, at the line you had to change.** `99_nd_dnm.txt:116-120`:
```
# `leader = { ... }` as a scope change inside `international_organization:hre`
# is NOT a valid scope link in EU5 -- the engine logs "Invalid scope types
# for event target link, link: leader". Instead, find the emperor via
# `random_country = { limit = { is_emperor = yes } }` which is the
# documented vanilla pattern (see hre.txt country_interactions).
```
(Corroborated: `docs/EU5-Vanilla-Script-Docs/event_targets.log:1917-1923` lists `leaders`, not `leader`, in that region of the link table.)
And `:30-37`, which is the single most valuable paragraph in this corpus:
```
# Each clause wraps its country-trigger checks in `any_country = { tag = DNM ... }`.
# Reason: the situation's can_end evaluates in SITUATION scope (no implicit
# country owner). Bare `has_variable = X` / `legitimacy >= N` etc would either
# evaluate against the wrong scope or fall through to a default-true result
# (we observed the endurance clause silently going green at game start because
# `legitimacy >= 60` and `prestige >= 50` were not being checked against DNM).
```
That is exactly the CLAUDE.md failure mode — **a `can_end` clause that silently evaluates true because its root was the situation, not a country** — caught in play and written down at the fix site. This is the discipline to copy wholesale.

### 4.7 ⚠ Mistake to avoid

Beyond `end_reason` (§4.5): **a design comment that cites the wrong vanilla precedent.** `99_nd_dnm.txt:19-20` credits `hussite_wars` for the `can_start = { always = no }` + `activate_situation` pattern; `VANILLA:hussite_wars.txt:5-11` has a real trigger, and the actual precedent is `treaty_of_tordesillas.txt:9-10`. Harmless at runtime, corrosive over time: a future session that follows the pointer learns the wrong pattern. Under this project's citation rule, a comment naming a vanilla file is a claim and needs the same `file:line` check as code.

---

## 5. `3698931463` — **Standard of Living**

`.metadata/metadata.json`: `"name": "Standard of Living"`, `"id": "hades.sol"`, `"version": "1.3.6"`, `"supported_game_version": "1.3.6"`, `"short_description": "Our core objective is to fix the static pop demands of the vanilla game, introduce real macroeconomic dynamics, and heavily penalize brainless snowballing."`, tags `Balance / Trade and Economics`. It declares a **hard dependency** — `"rel_type": "dependency", "id": "community_mod_framework", "version": "2.*"` — and `"game_custom_data": { "multiplayer_synchronized": true }`.
**⚠ Note:** the mod-root `README.md:1-14` describes a *different* mod ("EU5 MP Stable Balance Mod … based on reference mod 3644897537 (Amalgamation Synergy)"). Where README and metadata disagree, metadata is the shipped identity.

### 5.1 `global_living_standard` — 123 lines, `in_game/common/situations/SOL_economy_situation.txt`

**Subject.** A permanent macroeconomic dashboard: per-location per-capita spending, computed monthly, painted as a heat map, read in a statistics panel.

**Gates.** `:2-5`: `monthly_spawn_chance = 1`, `can_start = { current_date >= 1337.4.1 }`. Seeded by **date alone, three months after the vanilla 1337.1.1 start**, at probability 1 — so it is effectively active from early game one, with no flag, no event, no `activate_situation`. `can_end = { always = no }` (`:7-9`). `visible = { sol_sol_is_on = yes }` (`:11-13`), a scripted trigger at `in_game/common/scripted_triggers/SOL_cmm_triggers.txt:110` — the framework's master switch.

**Lifecycle.** **No `on_start`. No `on_ending`. No `on_ended`.** Only `on_monthly` (`:15-37`): if the master switch is on, refresh the market pop-demand maps in January or if uninitialised (`sol_refresh_market_pop_demand_maps`), then for every country with population run `gls_compute_savings_pressure`, and additionally for humans `gls_compute_panel_display` and — in January or if uncached — `gls_accumulate_panel_stats`. Note the human/AI split: the expensive panel arithmetic runs only for `is_human = yes` (`:27`).

**Phases / variables.** No phases. Location-scope variable `gls_location_actual_per_capita_spending` drives everything; country-scope `gls_country_sol_all` caches the panel; global `sol_market_pop_demand_maps_initialized` guards the yearly refresh.

**Map.** `is_data_map = yes` (`:88`). `map_color` (`:89-106`) is the only **continuous** colouring in the corpus:
```
lerp = {
	min_color = define:NMapColors|MAP_COLOR_LOW
	max_color = define:NMapColors|MAP_COLOR_HIGH
	factor = "gls_location_color_factor"
}
```
— the exact form vanilla uses for plague density (`VANILLA:black_death.txt:226-230`). Three `legend_key` (`:108-121`). `tooltip` is a five-tier threshold cascade at 0.5 / 0.1 / 0.01 / any / none (`:39-86`), and each branch emits **two** `custom_tooltip` lines (a band label plus a value line) — legal stacking inside one branch.

**Resolution use — yes, and unusually.** `in_game/common/resolutions/SOL_economy_resolution.txt:1` defines `global_living_standard_recalculate` with `requires_vote = { always = no }`, `days = 1`, `should_finalize_vote = { always = yes }`, `show_message = no`, and an `effect` that runs `gls_full_refresh_country` for every populated country. **But the situation file does not declare `resolution = …` or `voters = …`** — the binding is the other way round, from the resolution's `select_trigger` blocks (`:23-42`), with an in-source note at `:32`: `# Last select_trigger is the vote target in resolution framework.` Contrast vanilla, which declares the field on the situation (`VANILLA:fall_of_delhi.txt:4-5`, `nanbokuchou.txt:3-4`, `western_schism.txt:4-5`). Effectively: a resolution repurposed as a manual "refresh cache" button.

### 5.2 GUI — yes, 268 lines, and it drives the map mode

`in_game/gui/panels/situation/global_living_standard.gui`. Overrides only four blocks (`:14, :16, :21, :23-27`) — the body is a dense statistics table (`SOL_GUI_SECTION_INCOME`, per-estate columns for nobles/clergy/burghers, `:37-53`). Two things stand out:

1. **The panel forces a map mode when shown.** `:1-12`:
```
situation_panel = {
	# Re-run this each time the panel is shown; trigger_on_create only runs once.
	widget = {
		name = "sol_living_standard_mapmode_autoselect"
		size = { 0 0 }
		visible = "[And(CanChangeMapMode, LateralView.IsShown)]"
		state = {
			name = _show
			on_start = "[GetMapMode('sol_living_standard').SetMapMode]"
		}
	}
```
2. **It borrows vanilla art instead of shipping its own illustration.** `:17` sets the header background to `"gfx/interface/illustrations/situation/columbian_exchange.dds"` under a fade mask. (The mod does ship its own list icon at `main_menu/gfx/interface/icons/situations/global_living_standard.dds` — correct tree.)

### 5.3 Loc

`main_menu/localization/english/SOL_economy_l_english.yml`: `global_living_standard` (`:12`), `_desc` (`:13`), `_recalculate` / `_desc` (`:14-15`), `_recalculate_specific` / `_desc` (`:16-17`), `vote_in_global_living_standard_recalculate` / `_desc` (`:18-19`). No `_info`, no `_monthly`, no `hint_tag` declared and none needed. Translated to `simp_chinese` (same key set, `SOL_economy_l_simp_chinese.yml:12-19`).

### 5.4 ★ Technique worth stealing

**Duplicate the situation's `map_color` into a real map mode, then have the panel select it on open.** `in_game/gfx/map/map_modes/SOL_map_modes.txt:1` defines `sol_living_standard` with the *same* `lerp` block as the situation (`:8-16`), plus `tooltip_key` branches, `category = economy`, `index = 0`, `color_refresh_counters = { Month }` and `color_and_names_refresh_counters = { Month }`; and `global_living_standard.gui:1-12` (quoted above) auto-selects it whenever the lateral view is shown. Result: the data is visible on the map through the normal map-mode UI *and* the panel guarantees you are looking at it. The comment `# Re-run this each time the panel is shown; trigger_on_create only runs once.` is itself a recorded GUI discovery.

### 5.5 ⚠ Mistake to avoid

**Double-escaped newlines in a situation `_desc`.** Verified by byte-read of `main_menu/localization/english/SOL_economy_l_english.yml:13`:
```
 global_living_standard_desc: "Opens the Living Standard statistics panel.\\n\\nThe system updates market pop-spending maps yearly and applies local_pop_demand to each location monthly."
```
That is a literal backslash followed by `n`, twice — the panel will print `\n\n` as text rather than break the paragraph. The rest of the mod's keys are fine, so this is a per-key slip, not a policy. Exactly the class of loc defect this project's one-physical-line rule is aimed at, from the other direction: too many escapes rather than a real newline.

---

## 6. `3735059838` — **MEIOU and Taxes**

`.metadata/metadata.json`: `"name": "MEIOU and Taxes"`, `"id": "meiou_and_taxes"`, `"version": "0.1.6"`, `"supported_game_version": "1.3.*"`, `"short_description": "Overhaul in the works"`, no tags. `readme.md:1-3`: *"MEIOU and Taxes / Overhaul mod to be. Restart of M&T for EU4."* A very large in-progress conversion.

### 6.1 `columbian_exchange` — 218 lines, `in_game/common/situations/MnT_columbian_exchange.txt`

**This is not a new situation. It is an entry-level replacement of vanilla's.** Line 1:
```
REPLACE:columbian_exchange = {
```
The `REPLACE:` prefix targets one database entry rather than the whole file, so the filename can be `MnT_`-prefixed and vanilla's `columbian_exchange.txt` stays loaded for anything else. The same technique is used across the mod — `in_game/common/scripted_triggers/MnT_situation_triggers.txt:5` `REPLACE:is_candidate_for_NW_good`, `in_game/common/generic_actions/MnT_columbian_exchange.txt:7` `REPLACE:move_nw_good_to_new_location` (1083 lines).

**What it does.** Same as vanilla: gates on `current_age = age_5_absolutism` plus any American location owned from the Old World (`:5-16`); `visible` (`:22-66`) uses a `trigger_if` / `trigger_else` pair to ask New-World countries whether their markets carry Old-World goods and vice versa, each wrapped in `custom_tooltip` + `hidden_trigger` so the panel prints a readable reason; `on_start` and `on_monthly` (`:69-179`) are the same enrolment loop stamping `is_in_columbian_exchange` and firing `columbian_exchange.1`; `on_ended` (`:185-192`) clears the variable; `map_color` (`:194-217`) is two-branch New-World / Old-World with `color_nw_country` / `color_ow_country`. `tooltip = { }` is **empty** (`:181-182`) — as in vanilla. `hint_tag = hint_columbian_exchange` (`:3`) correctly points at a **registered vanilla** hint object (`VANILLA:in_game/common/scriptable_hints/scripted_hints.txt:791`).

**Scripted trigger.** `can_end = { columbian_exchange_end_trigger = yes }` (`:19`) — vanilla's trigger, unmodified.

### 6.2 GUI — none, and none needed

No `in_game/gui/` in this mod. Because the key is `columbian_exchange`, vanilla's `VANILLA:in_game/gui/panels/situation/columbian_exchange.gui` still serves the panel, and vanilla's icon and illustration still resolve. **This is the one mod in the corpus with a fully-dressed situation panel and zero GUI work** — the payoff of replacing an entry instead of inventing a key.

### 6.3 Seeding, events, loc

Seeding is vanilla's: date/age gate + `monthly_spawn_chance = monthly_spawn_chance_unique` (`:2`). **Zero situation events shipped** — `columbian_exchange.1` is vanilla's. **Zero situation loc shipped** — all key families inherited from vanilla, which does supply `columbian_exchange` and `_desc` (and no `_info`/`_monthly`).

### 6.4 ★ Technique worth stealing

**`REPLACE:<entry>` to retune a vanilla situation while keeping its panel, art, hint, events and loc.** `MnT_columbian_exchange.txt:1`. For 1066 this is directly relevant: several vanilla situations (`black_death`, `little_ice_age`, `columbian_exchange`, `western_schism`) have subjects that exist in the 1066–1337 window or need their date gates moved. Re-gating them by `REPLACE:` is far cheaper than authoring a new key, and it inherits every asset — the exact opposite of the whole-file override the project's `verify-vanilla-override` skill warns about.

### 6.5 ⚠ Mistake to avoid — **and this is the sharpest one in the survey**

**A `REPLACE:` copy taken from an older build silently deletes whatever the newer vanilla added.**

Diffing `MnT_columbian_exchange.txt` against `VANILLA:in_game/common/situations/columbian_exchange.txt` (230 lines) with the BOM and the `REPLACE:` prefix normalised away, the **entire** semantic delta is:

```
219,228d216
< 	}
< 	
< 	legend_key = { 
< 		desc = "new_world_goods"
< 		color = color_nw_country
< 	}
< 	
< 	legend_key = { 
< 		desc = "old_world_goods"
< 		color = color_ow_country
```
(the remaining four hunks — `118d117`, `128c127`, `175d173`, `193c191` — are a blank line and two trailing-whitespace changes.)

So this 218-line replacement exists to reproduce vanilla exactly **minus vanilla's two `legend_key` blocks** (`VANILLA:columbian_exchange.txt:221-228`). The map keeps its New-World / Old-World colours and loses the legend that explains them. Nothing errors; nothing in the log; the only symptom is an unexplained two-colour map. This is the entry-level analogue of the whole-file-override trap: **`REPLACE:` is a full overwrite of that entry, so anything vanilla added after your copy was taken is deleted.** The mitigation is mechanical and cheap: diff every `REPLACE:` block against current vanilla before shipping, and again after every game patch.

---

## 7. Cross-cutting findings

### 7.1 Hint tags — 2 of 3 declarations are dangling

| Mod | Declaration | `scriptable_hints` object | `hint_*` loc | Verdict |
|---|---|---|---|---|
| 3603092142 | `rise_of_persia.txt:3`, `wot_turkish_expansion.txt:3` | **none in mod** | **none in mod** | dangling ×2 |
| 3668193813 | `99_nd_dnm.txt:24` | **none in mod** | present, `nd_dnm_l_english.yml:410-413` | dangling |
| 3633816300 | `OGAS_situations.txt:3` — `#hint_tag = hint_OGAS`, commented out | n/a | n/a | **correct** |
| 3735059838 | `MnT_columbian_exchange.txt:3` → vanilla | `VANILLA:…/scripted_hints.txt:791` | vanilla | **correct** |
| 3613232232, 3698931463 | no `hint_tag` | — | — | n/a |

Both GUI panels in 3603092142 also wire a button to `[OpenLateralViewWithParams('hints', 'selected_hint = hint_rise_of_persia')]` (`rise_of_persia.gui:71`) pointing at the same unregistered hint. Consequence UNVERIFIED (likely an empty hints view rather than an error) — but it is three cross-references that do not resolve, in two separately-authored mods. **For 1066: a `hint_tag` is a three-part contract — situation field + `in_game/common/scriptable_hints/` entry + `hint_*` / `_hint_text` / `_hint_text_1..n` loc. Ship all three or ship none.**

### 7.2 Loc key families — measured, all six mods

| Situation key | base | `_desc` | `_info` | `_monthly` |
|---|---|---|---|---|
| `rise_of_persia` | ✓ | ✓ | — | — |
| `wot_turkish_expansion` | ✓ | ✓ | — | — |
| `pp_mod_welcome_situation` | ✓ | ✓ | — | — |
| `harvest_situation` | ✓ | ✓ | — | **✓** |
| `OGAS` | ✓ | ✓ | — | — |
| `nd_dnm_reaction_of_the_reich` | ✓ | ✓ | — | — |
| `nd_mandate_crisis` | ✓ | ✓ | — | — |
| `global_living_standard` | ✓ | ✓ | — | — |
| *(`columbian_exchange` inherits vanilla: base + `_desc`, no `_info`/`_monthly`)* | | | | |

`_info` is used by **nobody** in this corpus and by 6/22 vanilla situations; `_monthly` by one mod and 3/22 vanilla situations.

### 7.3 BOM discipline — measured on every situation-related file

`.txt` / `.yml`: **26 of 26 carry a BOM.** Uniform and correct per this project's rule.
`.gui`: **4 of 7 carry a BOM** — `3603092142/…/rise_of_persia.gui`, `…/wot_turkish_expansion.gui`, `3668193813/…/nd_dnm_reaction_of_the_reich.gui`, `…/nd_mandate_crisis.gui`. BOM-free: `3603092142/…/conquest_of_india.gui`, `3633816300/…/OGAS.gui`, `3698931463/…/global_living_standard.gui`. This project's rule (`.gui` carries no BOM; vanilla ships 483 with only 49 BOM'd) is therefore violated by two of the four GUI-shipping mods. No functional consequence observed or claimed — **UNVERIFIED** — but the split is real and the majority of workshop `.gui` files here are BOM-free.

### 7.4 Art tree

Vanilla: `main_menu/gfx/interface/icons/situations/` and `main_menu/gfx/interface/illustrations/situation/`.
- 3603092142 — correct tree, 2 icons + 1 illustration.
- 3698931463 — correct tree, 1 icon; borrows vanilla `columbian_exchange.dds` for the panel image (`global_living_standard.gui:17`).
- **3613232232 — wrong tree**: `in_game/gfx/interface/icons/situations/pp_mod_welcome_situation.dds`. Zero vanilla precedent for `in_game/gfx/.../icons/situations/`.
- 3668193813 — no art at all, but both panels override `situation_panel_image`, so only the list icon falls back (`_default.dds` exists, e.g. `VANILLA:in_game/gui/government_lateralview.gui:656`).
- 3633816300 — no art and no image override → unresolved header illustration.
- 3735059838 — inherits vanilla art via the key.

### 7.5 Seeding taxonomy observed

| Shape | Example |
|---|---|
| date + tag/rule gate, `monthly_spawn_chance_unique` | `rise_of_persia.txt:5-9` |
| date + predecessor-situation-inactive + size gate | `wot_turkish_expansion.txt:5-11` |
| `always = yes`, permanent | `pp_variable_harvest_situation.txt:4-10` |
| empty `can_start`, permanent, `visible = { is_ai = no }` | `OGAS_situations.txt:5-16` |
| date-only, ~3 months after start, permanent | `SOL_economy_situation.txt:3-9` |
| `always = no` + external `activate_situation` from an event | `99_nd_dnm.txt:26-28` ← `nd_dnm.txt:61,87` |
| global-flag handshake set by `on_game_start` | `pp_mod_welcome_situation.txt:5-8` ← `pp_game_start.txt:126-149` |
| heavy multi-clause IO/authority gate + game rule | `nd_mandate_crisis.txt:4-31` |
| inherited from vanilla via `REPLACE:` | `MnT_columbian_exchange.txt:1-16` |

---

## 8. Comparative table

| mod-id | situation keys | scale (situation / events / gui, lines) | GUI shipped? | seeded how | verdict in one line |
|---|---|---|---|---|---|
| **3603092142** *Historical Tweaks* | `rise_of_persia`, `wot_turkish_expansion`, *(`conquest_of_india` — 100% commented out)* | 447+141+122 / 450+98+39 / 256+134+94 | **Yes ×2** (+1 dead), base = `rise_of_the_ottomans` family, `one_country_header_template` | date + game rule + tag-absence; `monthly_spawn_chance_unique` | The most ambitious port in the corpus — a full three-rank leader race with actions, AI lists and an `on_annexed` hook — carrying a mis-paired legend colour, a duplicated `secondary_map_color`, stale loc thresholds and two dangling `hint_tag`s. |
| **3613232232** *Prosper or Perish* | `harvest_situation` (**≠ filename**), `pp_mod_welcome_situation` | 271+35 / 0 / **0** | **No** — default empty body for both | `always = yes`; and a `on_game_start` global-flag handshake | Situations used as a monthly scheduler and a mod-notice board, documented via Europedia instead of a panel — with a dead `on_ended` behind `can_end = { always = no }` and its icon in the wrong gfx tree. |
| **3633816300** *OGAS Optimized* | `OGAS` | 95 / 0 / 164 | **Yes**, minimal-override control board driving `GetScriptedGui(...)` buttons | empty `can_start` + `monthly_spawn_chance = 1`, `visible = { is_ai = no }` | The cleanest idea here: a permanent, effect-free, player-only situation used purely as a hosted settings panel and `is_data_map` readout — the only mod that correctly *disabled* its unbacked `hint_tag`, and the only one whose header illustration will not resolve. |
| **3668193813** *National Destinies* | `nd_dnm_reaction_of_the_reich`, `nd_mandate_crisis` | 226+498 / 1219(39 ev)+776(17 ev) / 301+189 | **Yes ×2**, provenance-documented (`hussite_wars`, `the_revolution`, `middle_kingdom`, `left_panel`) | `always = no` + `activate_situation` from `nd_dnm.1`; heavy IO/authority/game-rule gate | Craft-leader and cautionary tale in one: an explicit two-phase state machine, a custom IO, 8 situation actions, 5 matched legend keys and engine errors recorded inline — built on `end_reason`, a `can_end` construct with **zero attestation in either vanilla copy checked**. |
| **3698931463** *Standard of Living* | `global_living_standard` | 123 / 0 / 268 | **Yes**, statistics dashboard that force-selects its own map mode | date-only, `current_date >= 1337.4.1`, `monthly_spawn_chance = 1`, permanent | A situation with no `on_start` and no `on_ended` at all — a pure monthly compute host with a `lerp` heat map mirrored into a real map mode, a resolution repurposed as a refresh button, and one `\\n\\n` loc slip. |
| **3735059838** *MEIOU and Taxes* | `columbian_exchange` (via `REPLACE:`) | 218 / 0 / 0 (inherits vanilla) | **N/A — inherits vanilla's panel, art, hint and events** | inherited vanilla age + presence gate | The cheapest possible situation change and the sharpest warning: `REPLACE:` keeps every vanilla asset for free, and this 218-line copy's *only* delta from live vanilla is that it silently deletes vanilla's two `legend_key` blocks. |

---

## 9. Five things to carry into the SITUATIONS phase

1. **Adopt ND's inline-error discipline** (`99_nd_dnm.txt:30-37, 116-120`): when a scope or link surprises you, paste the engine's exact message next to the workaround. That file is the only artefact in the corpus that would survive this project's citation rule.
2. **Adopt HTC's tooltip-bearing end trigger** (`situation_end_triggers.txt:1-25` + `[SituationView.GetTooltipInformation('…')]` at `wot_situations_l_english.yml:2`): one scripted trigger, evaluated by `can_end` and rendered into the panel, so the displayed victory condition cannot drift from the coded one. HTC's own loc drift (§1.9) shows what happens when you write the two separately.
3. **Adopt MnT's `REPLACE:` for vanilla situations that need re-gating for 1066** — and diff every such block against live vanilla before shipping and after every patch (§6.5).
4. **Adopt OGAS's shape for any non-historical panel** (mod dashboard, campaign settings): permanent + `visible = { is_ai = no }` + empty hooks + `is_data_map = yes`, and **do** override `situation_panel_image` (§3.5).
5. **Do not use `end_reason`.** It has zero attestation in `VANILLA:in_game/common/situations/`, zero in `reference_game_files/game/`, zero in `reference_official_defines/`, and is absent from `VANILLA:in_game/common/situations/readme.txt`. Use `can_end = { <named scripted trigger> }` with `custom_tooltip` wrappers, the vanilla + HTC route, until in-game evidence says otherwise.

---

*Every claim above carries a mod-relative or `VANILLA:`-prefixed `file:line`. Claims explicitly marked UNVERIFIED: the runtime legality of `end_reason`; the runtime consequence of a dangling `hint_tag`; the runtime consequence of column-0 loc keys; the runtime consequence of a BOM on a `.gui`; which of two duplicate `secondary_map_color` blocks the parser keeps. No file in any game, mod or repo tree was created or modified.*
