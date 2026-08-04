# CRAFT STUDY — "Anno 1644: The General Crisis" situations

**Source tree (read-only):** `C:\Users\Desktop\Anno 1644 The General Crisis Modu Total overhaul for 1644`
All mod paths below are relative to that root. Vanilla paths are relative to
`E:\SteamLibrary\steamapps\common\Europa Universalis V\game` and are prefixed `VANILLA:`.
Nothing in the mod tree was written to. Every claim carries `file:line`.

Start date of the studied mod: **1644.4.17** (asserted by the parent task; the date is
independently corroborated in-tree by `in_game/common/situations/war_of_three_kingdoms.txt:17`
`current_date >= 1644.4.1` under the comment `# 開始条件（1644年4月即時発火）`
("start condition: immediate fire, April 1644") at `war_of_three_kingdoms.txt:14`).

---

## 0. THE AUTHORITY DOCUMENT (read this first)

Vanilla ships a field-by-field spec for situations that answers most lifecycle questions
outright. It is 18 lines and was not previously in our notes:

`VANILLA: in_game/common/situations/readme.txt:4-18`

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

Note the **root scopes differ per block**: `can_start`/`can_end`/`on_*` are SITUATION scope;
`visible` is COUNTRY scope with `scope:target = situation`; `tooltip`/`map_color`/
`secondary_map_color` are LOCATION scope with `scope:target = situation`. Anno 1644 obeys this
consistently — e.g. `visible = { has_presence_in = continent:europe }`
(`in_game/common/situations/thirty_years_war.txt:46-48`, country scope) vs
`map_color = { if = { limit = { has_owner = yes owner ?= c:ROE } ... } }`
(`in_game/common/situations/war_of_three_kingdoms.txt:173-181`, location scope using `owner`).

There is a matching GUI readme: `VANILLA: in_game/gui/panels/situation/readme.txt:1-6` —
"2. You should create a new file in the situations folder with the name of the situation.
3. Your new created file should have the same structure as the other situation files.
Specially using the type situation_panel."

Script-doc corroboration of the situation verb set (from our repo's dumps):
- `docs/EU5-Vanilla-Script-Docs/effects.log:12-15` — `activate_situation`, "activates a situation", **Supported Targets**: situation
- `docs/EU5-Vanilla-Script-Docs/effects.log:1535-1538` — `end_situation`, "End a situation", **Supported Targets**: situation
- `docs/EU5-Vanilla-Script-Docs/triggers.log:2922 / :10272 / :10278` — `can_see_situation`, `situation_has_ended`, `situation_is_active`

---

## 1. INVENTORY

Eight situation definitions in `in_game/common/situations/` (2 015 lines total),
six situation-event files in `in_game/events/situations/` (2 615 lines),
seven GUI panels in `in_game/gui/panels/situation/` (1 822 lines).

| Situation key | Def file : lines | Event file : lines | GUI panel : lines | Subject |
|---|---|---|---|---|
| `netherland_independent` | `in_game/common/situations/netherland_independent.txt` : 450 | `in_game/events/situations/netherland_independent_events.txt` : 236 (9 events) | `netherland_independent.gui` : 356 | Dutch Revolt endgame, NED vs SPA |
| `thirty_years_war` | `thirty_years_war.txt` : 308 | `thirty_years_war_events.txt` : 1016 (18 events) | `thirty_years_war.gui` : 529 | HRE religious war; replaces vanilla `war_of_religions` |
| `late_ming_crisis` | `zzz_late_ming_crisis.txt` : 498 | `late_ming_crisis.txt` : 404 (6 events) | `late_ming_crisis.gui` : 423 | Ming / Shun / Qing three-way for China |
| `war_of_three_kingdoms` | `war_of_three_kingdoms.txt` : 218 | `war_of_three_kingdoms.txt` : 689 (12 events, namespace `english_civil_war`) | `war_of_three_kingdoms.gui` : 153 | English Civil War, ENG vs ROE |
| `the_deluge` | `the_deluge.txt` : 123 | `the_deluge.txt` : 201 (8 events) | `the_deluge.gui` : 81 | PLC collapse, Khmelnytsky onward |
| `the_steppe` | `the_steppe.txt` : 130 | `the_steppe_events.txt` : 69 (3 events) | `the_steppe.gui` : 111 | Permanent nomad/herd framework, Ukraine→Mongolia |
| `peace_talk_in_westphalia` | `peace_talk_in_westphalia.txt` : 153 | (no own file; uses `thirty_years_war_events.*`) | `peace_talk_in_westphalia.gui` : 169 | 5-phase congress minigame |
| *(vanilla neutering)* | `zzz_1644_overrides.txt` : 135 | — | — | 16 `REPLACE:` blocks shutting off vanilla situations |

Support systems attached to situations:
- `in_game/common/generic_actions/` — **12 actions with `type = situation`** (counted from
  `grep -h "^\s*type = " in_game/common/generic_actions/*.txt`), spread over
  `peace_talk_in_westphalia.txt` (1), `the_deluge.txt` (5), `the_steppe.txt` (2),
  `thirty_years_war.txt` (1), `zzz_late_ming_crisis_actions.txt` (3).
- `in_game/common/on_action/` — 11 files, of which `netherland_independent.txt` (53),
  `the_deluge.txt` (38), `the_steppe.txt` (30), `the_steppe_country_yearly.txt` (7) are
  situation-owned.
- `in_game/common/scripted_effects/` — `netherland_independent_effects.txt`,
  `the_steppe_effects.txt`, `thirty_years_war_effects.txt`, `zzz_1644_ming_crisis_effects.txt`.
- `main_menu/common/static_modifiers/zzz_1644_situation_modifiers.txt` — 1 modifier,
  `late_ming_crisis_participant` (lines 1-20).
- `main_menu/common/game_rules/03_game_rules.txt:1-9` — a player-facing rule
  `treaty_of_westphalia` with options `treaty_of_westphalia_default` / `_historical`.

**Not used at all:** resolutions, `voters`, `international_organization_type` in the situation
block, `custom_description` — `grep -rn "resolution\|international_organization_type =\|custom_description\|voters" in_game/common/situations/*.txt` returns nothing. There is no
`resolutions/` directory anywhere in the mod (`find . -type d -name "*resolution*"` → empty).

---

## 2. SEEDING AT A MOVED START DATE — the core question

### 2.1 The setup-file route is present but essentially VESTIGIAL

The mod ships `main_menu/setup/start/22_zzz_w_situations.txt`, a **`zzz_`-prefixed additive
file** (vanilla's file is `22_situations.txt`; the mod does **not** override it). Full content,
14 lines:

```
situation_manager={
	netherland_independent = {
	}

	#thirty_years_war = {
	#	status = active
		#start_date = 1618.5.23
	#}

	#war_of_three_kingdoms = {
	#	status = active
	#	start_date = 1639.3.21
	#}
}
```
(`main_menu/setup/start/22_zzz_w_situations.txt:1-14`)

Three observations:

1. **Only one situation is listed, and with an empty body.** `netherland_independent = { }`
   carries no `status`, so it is not being force-activated here.
2. The `status = active` form is real — vanilla uses it, commented, at
   `VANILLA: main_menu/setup/start/22_situations.txt:2-15`:
   ```
   situation_manager={
   	rise_of_the_ottomans={
   	#	status=active
   	#	variables={
   	#		data={ {
   	#				flag="rise_of_the_ottomans_cooldown"
   	#				tick=0
   	#				data={ type=value identity=100000 }
   	#			} }
   	#	}
   	}
   ```
   So the attested setup-time payload is `status=active` plus a savegame-shaped
   `variables={ data={ { flag=... tick=... data={ type=value identity=... } } } }`.
3. **`start_date` is UNVERIFIED.** It appears only inside a comment
   (`22_zzz_w_situations.txt:7` and `:12`) and nowhere in vanilla's setup or script docs.
   Treat it as an author's guess, not an attested field.
4. The file is **BOM-free** (`head -c3` = `73 69 74` = "sit"), consistent with our project's
   measured rule that `main_menu/setup/start/` carries no BOM.

### 2.2 The route that actually fires: `can_start` date gates written against 1644

Five of the seven live situations satisfy `can_start` **on the first monthly tick after
1644.4.17**, and `monthly_spawn_chance` is set so high they fire immediately.

`monthly_spawn_chance` semantics, verified: it is a probability in 0..1
(`VANILLA: in_game/common/situations/readme.txt:5`) and
`monthly_spawn_chance_unique = 1` — i.e. 100 % per month —
(`VANILLA: main_menu/common/script_values/default_values.txt:1212`; the ladder is
`_very_low = 0.01` :1205 … `_ultimate_high = 0.5` :1211).

| Situation | `can_start` gate | Fires at 1644.4? |
|---|---|---|
| `war_of_three_kingdoms` | `current_date >= 1644.4.1` + `country_exists = c:ROE` + `c:ENG` (`war_of_three_kingdoms.txt:17-21`), `monthly_spawn_chance = monthly_spawn_chance_unique` (`:3`) | **YES — gate written exactly at the new start date** |
| `the_steppe` | `current_year > 1643 / current_year < 1990` (`the_steppe.txt:8-9`), spawn `_unique` (`:5`) | **YES — lower bound is start-year minus one** |
| `late_ming_crisis` | `current_year >= 1627`, `<= 1665`, `exists = c:MNG`, `NOT = { c:MNG = { owns = location:dadu } }` (`zzz_late_ming_crisis.txt:6-11`), `monthly_spawn_chance = 100` (`:2`) | **YES — a *state* gate (Ming has lost Beijing) rather than a date gate** |
| `thirty_years_war` | `current_year >= 1615` + HRE exists with ≥1 independent catholic and ≥1 independent protestant member (`thirty_years_war.txt:5-21`), spawn `_unique` (`:2`) | **YES — an era floor well below 1644, plus a world-state gate** |
| `netherland_independent` | `(c:NED or c:HOL) and c:SPA` + `current_year > 1568` + `< 1700` (`netherland_independent.txt:6-14`), spawn `_unique` (`:4`) | **YES** |
| `the_deluge` | `current_year > 1640` + `< 1700` + **`has_global_variable = rise_of_chemielnicki`** (`the_deluge.txt:11-13`) | **NO — waits for a flag** |
| `peace_talk_in_westphalia` | `situation:thirty_years_war = { situation_is_active = no }` + `has_global_variable = start_peace_talk_in_westphalia` + `NOT = { has_game_rule = treaty_of_westphalia_historical }` (`peace_talk_in_westphalia.txt:6-15`) | **NO — chained downstream** |

Note the commented-out original in `thirty_years_war.txt:6-7`:
```
        #current_year > 1590
        #current_year < 1655
```
replaced by the single `current_year >= 1615` at `:8` — i.e. the author *widened* the window
downwards and dropped the upper bound so a 1644 start would never miss it. That is the
concrete edit a moved start date forces on an inherited situation.

### 2.3 The best technique in the mod: DHE → global variable → `can_start`

`the_deluge` is not date-gated at all. Its gate is a global variable set by a *dated flavour
event*:

- `in_game/events/DHE/flavor_ZAZ.txt:383-394` — `flavor_zaz.2000` ("A men called Bohdan
  Khmelnytsky asking for help"), `major = yes`, with
  ```
  dynamic_historical_event = {
  	tag = ZAZ
  	from = 1648.1.1
  	to   = 1673.1.1
  	monthly_chance = 15
  }
  ```
  and `fire_only_once = yes` at `:396`.
- Its option body reaches `in_game/events/DHE/flavor_ZAZ.txt:502` —
  `set_global_variable = rise_of_chemielnicki`.
- Which is exactly the gate at `in_game/common/situations/the_deluge.txt:13`.

So a situation four years in the future is armed by a historical event in a 25-year window,
not by a hardcoded date. The same shape recurs for the congress:
`thirty_years_war_events.txt:338-340` sets `start_peace_talk_in_westphalia`, consumed at
`peace_talk_in_westphalia.txt:11` and also as an *end* condition of the parent war at
`thirty_years_war.txt:26-28`.

### 2.4 Neutering vanilla situations: `REPLACE:` on the database entry, NOT a file override

`in_game/common/situations/zzz_1644_overrides.txt` is 135 lines of nothing but per-entry
replacements. It does **not** share a filename with any vanilla situation file — verified:
the mod's eight filenames (`netherland_independent`, `peace_talk_in_westphalia`, `the_deluge`,
`the_steppe`, `thirty_years_war`, `war_of_three_kingdoms`, `zzz_1644_overrides`,
`zzz_late_ming_crisis`) intersect vanilla's 22 filenames in **zero** places. The mod is purely
additive at file level and surgical at entry level:

```
REPLACE:black_death = {
	can_start = { current_year < 1600 }

	can_end = {
		current_year >= 1600
	}
}
```
(`zzz_1644_overrides.txt:1-7`; the identical five-line shape repeats for `sengoku` :9,
`hundred_years_war` :17, `western_schism` :25, `hussite_wars` :33, `italian_wars` :41,
`council_of_trent` :49, `nanbokuchou` :66, `rise_of_timur` :74, `rise_of_the_ottomans` :82,
`guelphs_and_ghibellines` :90, `fall_of_delhi` :98, `treaty_of_tordesillas` :106,
`great_pestilence` :118, `war_of_religions` :126 — 16 entries in all.)

One entry gets stronger treatment because vanilla can start it from world state rather than
date:
```
REPLACE:reformation = {
	can_start = { always = no }
	visible = { always = no }

	can_end = {
		current_year >= 1600
	}
}
```
(`zzz_1644_overrides.txt:57-64`)

`columbian_exchange` is deliberately left alive — its block is commented out at
`zzz_1644_overrides.txt:114-116`.

The `REPLACE:` prefix is used the same way elsewhere in the mod, confirming it is a general
database-entry mechanism and not situation-specific:
`main_menu/common/game_rules/03_game_rules.txt:11` `REPLACE:mission_packs_enabled_rule`,
`:21` `REPLACE:ai_colonisation_rule`;
`in_game/common/generic_actions/replaced_actions.txt:1`
`REPLACE:add_location_to_international_organization`;
`in_game/common/on_action/zzz_1644_monthly.txt:18` `REPLACE:on_nation_changing`.

### 2.5 The other seeding lever: `on_game_start` with day-offset scheduling

`in_game/common/on_action/zzz_1644_start.txt` (619 lines) is one giant `on_game_start` effect.
It stages the first weeks of the game:

```
        c:CSH = {
            trigger_event_silently = csh_1644_start_army.1
            trigger_event_silently = { id = csh_1644_unification.1 days = 4 }
            unlock_government_reform_effect = { type = chi_peasant_empire_reform }
        }
        c:QNG = {
            trigger_event_silently = qng_1644_banner_army.1
            trigger_event_silently = { id = qng_1644_unification.1 days = 23 }
        }
```
(`in_game/common/on_action/zzz_1644_start.txt:23-32`)

Also inside it: a bulk tech/institution pass
(`set_starting_tech_level_by_region = yes` / `give_institutions_by_tech_level = yes`, `:5-7`),
a demographic patch (`while = { count = 5 create_character = { female = yes age = { 16 29 } … } }`
for every country, `:54-66`), and an AI throttle for the opening years
(`if = { limit = { current_year < 1645 } … add_cooldown = { type = ai_spam_protection years = 4 } }`,
`:95-107`).

And a measured lesson written into a comment — this one is directly transferable:

```
        hidden_effect = {
            international_organization:hre = {
                #HRE Reform - It wont change when I define it in setup so I have to put it here
                add_policy_to_international_organization = policy:landfriede_rank_4_policy
```
(`in_game/events/start_events.txt:17-20`) — IO policies set in `setup/start` do not stick; they
must be applied from a start-time event.

---

## 3. LIFECYCLE CRAFT

### 3.1 `can_end` written as a player-readable OR-ladder with `custom_tooltip`

`thirty_years_war.txt:22-44` is the model. Every branch that is not self-explanatory is wrapped
in a `custom_tooltip` so the END REQUIREMENTS card in the panel reads as prose:

```
    can_end = {
        OR = {
            current_year >= 1700
            custom_tooltip = {
                text = in_peace_talk_in_westphalia
                has_global_variable = start_peace_talk_in_westphalia
            }
            custom_tooltip = {
                text = war_of_religions_peace_treaty_enforced_tt
                always = no
            }
            AND = {
                has_game_rule = treaty_of_westphalia_historical
                custom_tooltip = {
                    text = current_war_length_larger_to_equal_360
                    global_var:current_religion_war_length >= 360
                }
            }
            NOT = { exists = international_organization:protestant_union }
            NOT = { exists = international_organization:catholic_league }
            NOT = { exists = international_organization:hre }
        }
    }
```

Note `custom_tooltip = { text = … always = no }` at `:29-32` — a *documented but currently
impossible* end condition, shown to the player as a line of text with no mechanical effect.
Same idiom in `netherland_independent.txt:33-42`.

Every panel then renders that ladder verbatim via
`TooltipRequirementsList = { textcontext = "[SituationView.GetActiveSituation.GetSituation.GetEndConditions]" }`
(`in_game/gui/panels/situation/the_deluge.gui:60-62`, and identically in
`war_of_three_kingdoms.gui:64-66`, `thirty_years_war.gui:204-206`). So the `can_end` block *is*
the UI text. Writing it legibly is not optional polish.

### 3.2 Phase machine driven from `on_monthly` + situation-scope `var:`

`peace_talk_in_westphalia` is the cleanest phase idiom in the mod. `on_start` seeds two
situation variables and one global:

```
    on_start = {
        set_variable = { name = peace_talk_in_westphalia_phase_remaining_month value = 5 }
        set_variable = { name = peace_talk_in_westphalia_phase value = 1 }
        set_global_variable = { name = now_talking_about_north_europe_problem }
        set_global_variable = { name = losing_side_benifit value = 0 }
        count_allowed_treaty_effect = yes
    }
```
(`peace_talk_in_westphalia.txt:28-45`)

`on_monthly` decrements the countdown, rolls the phase, clears all five topic globals and sets
the one for the new phase (`:47-103`), and `can_end = { var:peace_talk_in_westphalia_phase = 5 }`
(`:18`) terminates it. Five phases × five months = a bounded 25-month minigame.

`thirty_years_war` uses the same tools at lower resolution — `on_start` seeds
`current_religion_war_length = 312` and `current_war_balance = 51.8` (with `max = 100 min = 0`)
(`thirty_years_war.txt:50-63`) — **note the 312: the war is seeded as if it had already been
running 26 years when the game opens.** `on_monthly` then just ticks the counter and calls one
scripted effect (`:65-71`).

### 3.3 `on_ended` as the branching epilogue, and what it leaves behind

Every situation cleans up its own modifiers and then narrates the outcome by branch.

`the_deluge.txt:96-106` — total cleanup, no permanent mark:
```
    on_ended = {
        every_location_in_the_world = {
            limit = { has_location_modifier = chaos_and_destruction }
            remove_location_modifier = chaos_and_destruction
        }
        c:PLC = { remove_country_modifier = the_deluge }
    }
```

`netherland_independent.txt:93-167` — a five-branch `if / else_if` chain, each branch firing a
different closing event to a different audience: `.3` "Independent Failed!" to every third
party, `.4` "Peaceful End!", `.5` "Peace of Münster" to the belligerents and their subjects,
`.9` "Peace of Trier" to NED alone, `.8` on timeout.

`thirty_years_war.txt:73-94` — the only situation that leaves a *structural* mark: on the
historical game-rule branch it fires the Westphalia settlement event, and past 1700 it destroys
both religious IOs:
```
            destroy_international_organization = { target = international_organization:catholic_league }
            destroy_international_organization = { target = international_organization:protestant_union }
```
The actual territorial settlement is not in `on_ended` at all — it is in the option body of
`thirty_years_war_events.1` (`in_game/events/situations/thirty_years_war_events.txt:125-243`),
which redraws seven areas by list, transfers Bremen and Stettin inside the Swedish Empire IO,
adds two HRE policies, appoints a new elector, and *ends the situation from inside its own
option*:
```
    option = {
        name = thirty_years_war_events.1.a
        situation:thirty_years_war = {
            end_situation = this
        }
```
(`thirty_years_war_events.txt:125-129`)

Two other places end or start situations from outside the situation file:
- `in_game/common/peace_treaties/religious_supremacy.txt:53` — `end_situation = situation:thirty_years_war`
  (a peace treaty terminates the situation)
- `in_game/common/diseases/bubonic_plague.txt:165` — `activate_situation = situation:black_death`
  (the only `activate_situation` call in the mod; it is inherited vanilla content)

The mod never calls `activate_situation` on any of its own eight situations. Everything is
`can_start` + `monthly_spawn_chance`.

### 3.4 Map colours and legend keys

Two styles coexist. **Named colours** (`thirty_years_war.txt:183-308`) — seven branches feeding
seven `legend_key` blocks, all using vanilla-registered names:
`war_of_religions_protestant_union_leader_color`
(`VANILLA: main_menu/common/named_colors/02_map.txt:4276`),
`war_of_religions_catholic_league_color` (`:4278`), `rtr_neutral_color` (`:4267`).
Legend shape:
```
    legend_key = {
        desc = "WAR_OF_RELIGIONS_PROTESTANT_UNION_LEADER"
        color = war_of_religions_protestant_union_leader_color
        require_color_on_map = yes
    }
```
(`thirty_years_war.txt:274-278`)

**Literal rgb** (`netherland_independent.txt:312-413`, `the_steppe.txt:56-130`,
`war_of_three_kingdoms.txt:173-203`) — `value = rgb { 85 175 169 }` etc., with
`else = { value = define:NMapColors|DEFAULT_COLOR }` as the fall-through
(`thirty_years_war.txt:270`, `war_of_three_kingdoms.txt:201`,
`zzz_late_ming_crisis.txt:473`).

`secondary_map_color` (the striped overlay) is used by exactly two situations:
`netherland_independent.txt:415-450` (subjects and allies get their patron's stripe) and
`the_steppe.txt:109-130` (the whole steppe geography gets one stripe regardless of owner).
The mod adds **no** named colours of its own — `main_menu/common/named_colors/` holds a single
file, `age_7_colors.txt` (10 lines), containing only goods and railroad colours.

### 3.5 `tooltip` = the map-hover text, written as a first-match `if/else_if` cascade

`netherland_independent.txt:169-310` runs eleven branches to classify a hovered location:
is-NED, is-SPA, loyal-NED-subject, disloyal-NED-subject, loyal-SPA-subject,
disloyal-SPA-subject, Utrecht member, Arras member, SPA-ally, NED-ally, both-ally,
unaligned-lowlander. `thirty_years_war.txt:96-181` does the same in seven. The readme warns this
block "is not actually executed" (`VANILLA: readme.txt:16`) — it exists purely to generate text,
so every branch must terminate in a `custom_tooltip`.

### 3.6 `type = situation` generic actions — the player's buttons on the panel

Twelve of them. Canonical shape (`in_game/common/generic_actions/thirty_years_war.txt:1-42`):

```
request_peaceful_talk = {
    type = situation

    potential = { scope:actor = { OR = { is_leader_of_international_organization = … } }
        situation:thirty_years_war = { situation_is_active = yes } }
    allow = { … NOT = { has_game_rule = treaty_of_westphalia_historical } }

    ai_tick = monthly
    ai_tick_frequency = 3
    automation_tick = never
    automation_tick_frequency = 12

    select_trigger = {
        looking_for_a = situation
        target_flag = recipient
        name = "choose_situation"
        column = { data = name }
        visible = { situation:thirty_years_war = this  situation_is_active = yes }
    }
```

The `select_trigger { looking_for_a = situation … target_flag = recipient }` preamble is
boilerplate on all twelve — it is how the action binds itself to the situation panel. Variants
worth noting:
- `price = price:the_steppe_horde_claims_price` + `cooldown = { type = the_steppe_horde_claims_price_key years = 3 }`
  (`in_game/common/generic_actions/the_steppe.txt:25-30`) — actions cost money and have cooldowns.
- `price = 1` (`the_deluge.txt:24`) — a literal price is legal.
- `show_message = no` (`the_deluge.txt:4`, `the_steppe.txt:3`) — silent actions.
- `source_global_list = china_countries_list` inside a `select_trigger`
  (`zzz_late_ming_crisis_actions.txt:45-47`) — the target list is a runtime global list, not a
  static scope. Paired with `none_available_msg_key = "no_countries_available"` (`:48`).
- `interaction_source_list = { situation:the_steppe = { add_to_list = source } }`
  (`the_steppe.txt:34-38`) — an explicit source-list builder.

### 3.7 `on_action` wrappers gated on situation liveness

The situations do not do all their monthly work inside `on_monthly`. Recurring work is hoisted
into `on_action` handlers that self-gate:

```
on_the_deluge_foreign_occupy_land = {
    trigger = {
        location ?= { owner = c:PLC  controller != owner
            NOT = { has_location_modifier = chaos_and_destruction}
            save_temporary_scope_as = target_location }
        situation:the_deluge = { situation_is_active = yes }
    }
    effect = { scope:target_location = { add_location_modifier = { modifier = chaos_and_destruction } } }
}
```
(`in_game/common/on_action/the_deluge.txt:1-19`)

and hooked in via a single aggregator:
```
monthly_country_pulse = {
	on_actions = {
		on_netherland_netural_list
		on_netherland_netherland_side_list
		on_netherland_spain_side_list
		on_netherland_control_brussels
		on_horde_nations_list
		on_monthly_herd_check
		on_corruption_monthly_check
	}
}
```
(`in_game/common/on_action/zzz_1644_monthly.txt:2-16`)

with a re-entrancy guard on each — `NOT = { has_global_variable = temp_monthly_netherland_netural_check }`
(`in_game/common/on_action/netherland_independent.txt:6`), the flag being set with a `days = 10`
lifetime elsewhere (same idiom visible at `corruption_on_actions.txt:7-10`:
`set_global_variable = { name = temp_monthly_corruption_check days = 10 }`).

Ambient flavour rides a yearly pulse with weighted random events:
```
yearly_country_pulse = {
    random_events = {
        10 = the_steppe_random_event.1
        10 = the_steppe_random_event.2
        10 = the_steppe_random_event.3
        10 = the_steppe_random_event.4
    }
}
```
(`in_game/common/on_action/the_steppe_country_yearly.txt:1-7`)

---

## 4. EVENT MASS

**170 event files, 91 741 lines** (`find in_game/events -name "*.txt" | wc -l` = 170;
concatenated line count = 91 741). Organisation:

| Directory | Files | Organising principle |
|---|---|---|
| `in_game/events/DHE/` | 143 | **per country tag** — `flavor_ENG.txt`, `flavor_FRA.txt`, `flavor_HAB.txt`, `flavor_ZAZ.txt`, plus pair-files (`flavor_cas_por.txt`, `flavor_brapru_teu.txt`) and theme-files (`flavor_chi_treasure_expedition.txt`) |
| `in_game/events/situations/` | 6 | **per situation** |
| `in_game/events/` (root) | 17 | start-up / faction bootstrap (`zzz_1644_qing_start_army.txt`, `zzz_1644_wsg_choice.txt`, `qing_1644_unification.txt` …) |
| `in_game/events/stories/`, `/DHE`, `/colonization`, `/disaster` | 4 | inherited vanilla categories |

**The fraction riding situations is small: 6 of 170 files, 2 615 of 91 741 lines ≈ 2.9 %.**
The overwhelming bulk is free DHE flavour. That is the real answer to "how do you fill 200
years": not situations, DHE.

### 4.1 `dynamic_historical_event` — the mass mechanism

**916 `dynamic_historical_event` blocks** across `in_game/events/`. Canonical form:

```
	dynamic_historical_event = {
		tag = ENG
		from = 1644.1.1
		to = 1700.1.1
		monthly_chance = 5
	}
```
(`in_game/events/DHE/flavor_ENG.txt:12-17`)

Field frequency inside those blocks (counted over `in_game/events/DHE/`):
`tag =` 946, `from =` 895, `to =` 895, `monthly_chance =` 895. So the block is essentially
always all four fields, and a handful carry a second `tag`.

**`from =` year histogram — the single most important number in this study:**

| `from =` | count |
|---|---|
| **1644** | **333** |
| 1700 | 60 |
| 1650 | 43 |
| 1750 | 36 |
| 1680 | 21 |
| 1780 | 19 |
| 1770 | 17 |
| 1660 | 17 |
| 1760 | 16 |
| 1670 | 16 |
| … | … |

**333 of 895 DHE blocks (37 %) open exactly at the moved start date.** This is how a total
conversion at a new date populates its first decades: a dense wave of tag-scoped, date-windowed,
`fire_only_once` events all armed on day one and dribbling out over decades at
`monthly_chance` 1-15.

Density per tag: `flavor_ENG.txt` 86 blocks, `flavor_FRA.txt` 73, `flavor_HAB.txt` 67,
`flavor_CAS.txt` 50, `flavor_dan.txt` 36, `flavor_brapru.txt` 33, `flavor_IRO.txt` 24,
`flavor_ira.txt` 22.

### 4.2 Firing idioms inside situations

Three distinct patterns:

1. **Immediate broadcast on `on_start`** —
   ```
   		every_country = {
   			limit = { capital.sub_continent = sub_continent:british_isles }
   			trigger_event_non_silently = war_of_three_kingdoms.1
   		}
   ```
   (`war_of_three_kingdoms.txt:68-73`); likewise `netherland_independent.txt:72-86` fires `.1`
   at NED and `.2` at SPA.

2. **Weighted monthly rolls with day-jitter** — the `late_ming_crisis` engine. Each of five
   rebellion hooks is an `if` gated on a "not yet happened" variable, wrapping a `random` whose
   `chance` is modified by up to eight world-state `modifier` blocks, ending in a delayed event:
   ```
   				random = {
   					chance = 10
   					modifier = { c:CSH.var:chi_domination < 70   multiply = 4 }
   					modifier = { c:CSH.var:chi_domination < 60   multiply = 2 }
   					…
   					modifier = { location:dadu.owner = c:QNG      multiply = 4 }
   					modifier = { c:CSH.var:chi_domination > 75   divide = 2 }
   					c:CJX = {
   						trigger_event_silently = { id = late_ming_crisis.1 days = { 3 10 } }
   					}
   				}
   ```
   (`zzz_late_ming_crisis.txt:186-234`; four more at `:250-287`, `:299-328`, `:347-388`,
   `:402-426`). Note `days = { 3 10 }` — a random offset range, so simultaneous triggers do not
   land on the same tick.

3. **Chained event → event** — `netherland_independent.6` → `.7` → `.8`
   (`netherland_independent_events.txt:90`, `:116`), each `fire_only_once = yes`.

All situation events carry `category = situation_event`
(`thirty_years_war_events.txt:103`, `late_ming_crisis.txt:5`, etc.) — vanilla attests this
category 403 + 49 times across `VANILLA: in_game/events/`.

Situation-event files also declare **top-level `scripted_effect` blocks inside the event file**:
`thirty_years_war_events.txt:4-97` defines nine list-builders (`east_pomerania_area`,
`wismar_area`, `gelre_area`, `upper_alsace_area`, `jamtland_area`, `amberg_area`,
`halberstadt_area`, `rosello_area`) immediately above the events that call them at `:115-121`.
This is legal — vanilla does the same in `VANILLA: in_game/events/culture/culture_greek.txt`,
`.../colonization/settle_the_frontier.txt` and others.

### 4.3 Option architecture

- **`historical_option = yes`** — 659 uses across `in_game/events/`. Marks the branch the AI
  and the history books took (`flavor_eng.8.a` at `flavor_ENG.txt:53`;
  `late_ming_crisis.1.a` at `late_ming_crisis.txt:34`).
- **Two `ai_chance` syntaxes, both in use:** bare number `ai_chance = 12`
  (`thirty_years_war_events.txt:271`) and block `ai_chance = { base = 95 }`
  (`netherland_independent_events.txt:86-88`), the block form also taking
  `modifier = { factor = 2 … }` (`flavor_ZAZ.txt:158-162`).
- **`ai_chance = 0` as the human-only escape hatch** —
  `late_ming_crisis.txt:88-99`, option `.1.c` ("remain loyal"): the AI will never pick it, the
  player can.
- **Per-option `trigger`** — options appear only when the world supports them:
  ```
   	option = {#归明
   	     name = late_ming_crisis.1.b
   	     trigger = {
   	         c:MNG.var:chi_domination > c:CSH.var:chi_domination
   	         c:MNG.var:chi_domination > c:QNG.var:chi_domination
   	     }
  ```
  (`late_ming_crisis.txt:72-77`). Same file `:66-69` puts a `trigger` at the *end* of option `.a`.
- **`is_ai` gating is nearly absent** — exactly one use in all six situation event files:
  `in_game/events/situations/the_deluge.txt:120` `trigger = { is_ai = no }`.
- Refusability is real but thin: 29 options across 18 events in `thirty_years_war_events.txt`,
  16 across 12 in `war_of_three_kingdoms.txt`, 11/9 in `netherland_independent_events.txt`,
  12/8 in `the_deluge.txt`, 10/6 in `late_ming_crisis.txt`, 4/3 in `the_steppe_events.txt`.
  Many are single-option acknowledgements (`netherland_independent.2` through `.5` each have one
  option and no effect body, `netherland_independent_events.txt:16-62`).
- **`custom_tooltip` wrapping an effect** so the player sees what an option does:
  ```
        option = {
            name = the_steppe_random_event.1.a
            custom_tooltip = {
                text = the_steppe_random_event.1.tt
                change_variable = { name = current_herd  add = 50 }
            }
        }
  ```
  (`in_game/events/the_steppe_random_event.txt:14-23`); `custom_description` is the sibling form
  (`flavor_ZAZ.txt:494-500`).
- **`illustration_tags = { 10 = regular  10 = interior }`** on almost every situation event
  (`thirty_years_war_events.txt:109-112`, `flavor_ENG.txt:38-41`) — 212 uses in DHE.
  `event_illustration_estate_effect = { foreground = estate_type:nobles_estate background = … }`
  in `immediate` (`flavor_ENG.txt:44`) is the estate-art variant.

---

## 5. GUI

### 5.1 One panel per situation, named after the KEY

Seven panels for seven live situations. The critical naming fact:
the situation whose **file** is `zzz_late_ming_crisis.txt` but whose **key** is
`late_ming_crisis` (`zzz_late_ming_crisis.txt:1`) has its panel at
`in_game/gui/panels/situation/late_ming_crisis.gui` — **the panel filename must match the
situation key, not the definition filename.**

`zzz_1644_overrides.txt` needs no panel (it only edits existing keys).

### 5.2 What a minimal panel is

`in_game/gui/panels/situation/the_deluge.gui` is the whole 81-line skeleton and is the file to
copy:

```
situation_panel = {

    blockoverride "situation_panel_image" {
        using = two_countries_header_template

        blockoverride "FirstCountryContext"  { datacontext = "[GetCountry('PLC')]" }
        blockoverride "SecondCountryContext" { datacontext = "[GetCountry('ZAZ')]" }
        blockoverride "first_character_portrait_anchor"  { parentanchor = bottom|left }
        blockoverride "second_character_portrait_anchor" { parentanchor = bottom|right }
        blockoverride "character_religion_visibility"    { visible = no }
        blockoverride "character_name_maximumsize"       { maximumsize = { 270 -1 } }
        blockoverride "country_header_extra" { hbox = { … expand = { } } }
    }

    blockoverride "situation_panel_main_content" {
        situation_card_expandable = {
            blockoverride "header_text"  { text = "END_REQUIREMENTS" }
            blockoverride "header_icon"  { texture = "gfx/interface/icons/disasters/end_requirements_green.dds" }
            blockoverride "bottom_content" {
                TooltipRequirementsList = {
                    textcontext = "[SituationView.GetActiveSituation.GetSituation.GetEndConditions]"
                }
            }
            …
        }
    }
}
```
(`the_deluge.gui:1-82`, condensed; every line quoted appears verbatim)

Verified bases (all vanilla, all real):
- `type situation_panel = lateralview` — `VANILLA: in_game/gui/panels/situation/common.gui:3`
- `template two_countries_header_template` — `VANILLA: in_game/gui/country_header.gui:202`
- `type situation_card_expandable = card_expandable` — `VANILLA: in_game/gui/shared/cards.gui:2631`
- `type situation_side_cards = side_cards` — `VANILLA: in_game/gui/shared/cards.gui:2841`
- `type situation_fancy_two_line_card = fancy_two_line_card` — `VANILLA: in_game/gui/shared/cards.gui:3103`

The `blockoverride` names available on `situation_panel` (from
`VANILLA: in_game/gui/panels/situation/common.gui`): `situation_header_extra` :43,
`situation_top_subheader_content` :47, `situation_header_left` :55, `situation_header_center` :66,
`situation_header_right` :94, **`situation_panel_image` :113**, `situation_extra_tabs_content` :182,
**`situation_subheader_content` :190**, `situation_subheader_extra` :192, `situation_subheader_left` :204,
`situation_subheader_center` :212, `situation_subheader_right` :220,
`situation_panel_main_maximumsize` :234, `situation_panel_autoresize_scroll_area` :237,
**`situation_panel_main_content` :258**, `situation_variable_progress_bar_visible` :261,
`situation_bar_first_threshold_text` :276 … Anno 1644 additionally uses
`situation_panel_main_content_bottom` (`war_of_three_kingdoms.gui:109`).

Richer panels: `war_of_three_kingdoms.gui:79-104` adds a `situation_fancy_two_line_card` for the
two-side strength readout and `:109-152` a `situation_side_cards` with two scrollable
`dynamicgridbox` of flags driven by
`datacontext = "[GetWillJoinCountryList(GetCountry('ENG').Self, GetCountry('ROE').Self)]"` /
`datamodel = "[WillJoinCountryList.GetJoinDefensive]"` (`:124-125`).
`late_ming_crisis.gui:1-70` hand-builds a *three*-country header out of the two-country
template's blocks, gating each column on
`visible = "[And(GetCountry('CSH').Exists, GetCountry('CSH').GetGovernment.HasRulerOrRegent)]"`
(`:35`).

Panels link into the hints system:
```
			blockoverride "onaction_hint" {
				action_tooltip = {
					title = "OPEN_HINT"
					on_action = "[OpenLateralViewWithParams('hints', 'selected_hint = hint_war_of_three_kingdoms')]"
				}
			}
```
(`war_of_three_kingdoms.gui:68-73`)

### 5.3 Icon pipeline — **binding is by CONVENTION, there is no `.gfx` file**

`find . -name "*.gfx"` over the whole mod returns **zero files**. The mod ships
`main_menu/gfx/interface/icons/situations/late_ming_crisis.dds` (and a stray `.png` of the same
name, plus `middle_kingdom.dds`) and nothing declares it.

The binding is the engine promote, used in the shared header:
```
						icon = {
						texture = "[SituationView.GetActiveSituation.GetIcon]"
						size = { 30 30 }
					}
```
(`VANILLA: in_game/gui/panels/situation/common.gui:13-16`, repeated at `:168` and `:383`)

`Situation.GetIcon` and `ActiveSituation.GetIcon` are real promotes —
`docs/EU5-Vanilla-Script-Docs/data_types/data_types_uncategorized.txt:117981` and `:35244`.

**Conclusion: drop `<situation_key>.dds` into `main_menu/gfx/interface/icons/situations/` and it
binds. Nothing else is needed.** Corroborated negatively: the mod's other six situations ship no
icon at all and rely on either the vanilla file of the same name or `_default.dds`
(`VANILLA: main_menu/gfx/interface/icons/situations/_default.dds` exists). `thirty_years_war` is
the explicit case — its panel points at the vanilla art by hand:
`texture = "gfx/interface/icons/situations/war_of_religions.dds"` (`thirty_years_war.gui:444`).
Likewise `late_ming_crisis.gui:13` reuses the vanilla illustration
`gfx/interface/illustrations/situation/red_turban_rebellions.dds` — the mod ships no
`illustrations/situation/` directory of its own.

---

## 6. LOCALISATION

### 6.1 Key families and volume

Total English loc: **3 974 lines** across all trees.
The situation-specific file is `main_menu/localization/english/w_situations_l_english.yml`
(96 lines, BOM present).

Key convention, matching vanilla exactly (`VANILLA: main_menu/localization/english/situations_l_english.yml:12-13`
` black_death: "Black Death"` / ` black_death_desc: "…"`):

| Family | Example | Cite |
|---|---|---|
| `<situation_key>` | ` late_ming_crisis:"Late Ming Crisis"` | `w_situations_l_english.yml:2` |
| `<situation_key>_desc` | ` late_ming_crisis_desc:"In the year 1644. …"` | `:3` |
| `<situation_key>_info` | ` netherland_independent_info:"People who lived in lowland now declaim independent!…"` | `:14` |
| `<something>_tt` | ` this_is_netherland_tt:"This is [GetCountry('NED').GetName]"` | `:16` |
| SHOUTY legend/GUI keys | ` NED_NEUTRAL_TT: "Neutral Dutches Nations"` | `:29` |
| `hint_<x>` | ` hint_thirty_years_war: "[GetSituationByKey('war_of_religions').GetNameWithNoTooltip]` | `:82` |
| `<action_key>` / `_desc` | ` the_steppe_horde_claims: "Claim another part of The Steppe"` / `_desc` | `:56-57` |

Tone: descriptive-historical, 1-3 sentences, heavy on datafunctions rather than literal names —
`ShowContinentName('europe')`, `ShowLocationName('osnabruck')`,
`ShowScriptedGeographyName('steppe_geography')`, `GetPopTypeByName('herdsman').GetName`,
`GetUniqueInternationalOrganization('middle_kingdom').GetName`
(`w_situations_l_english.yml:52`, `:61`, `:64`;
`in_game/localization/english/late_ming_crisis_l_english.yml:13`). Length: `_desc` values run
250-500 characters; `_tt` values 20-80. All values on one physical line, with `\n` written as
the two-character escape (`w_situations_l_english.yml:40`) — never a real newline.

Localisation coverage of the other languages: `main_menu/localization/simp_chinese/` has 61
files (vs 28+3 dirs in english), `main_menu/localization/japanese/` has 5 files plus a
`replace/` subdirectory containing `zzz_1644_names_l_japanese.yml`.

### 6.2 The duplicate-filename trap — CONFIRMED, and it is live

Our rule says never ship two loc files with the same filename in different directories.
Anno 1644 does exactly that, and the consequence is visible:

- `main_menu/localization/english/00_province_l_english.yml` — 33 lines, values are
  **the keys themselves**:
  ```
  ﻿l_english:
   xiangyan_province: "xiangyan_province"
   dean_province: "dean_province"
   anlu_province: "anlu_province"
  ```
  (`:1-4`)
- `main_menu/localization/english/location_names/00_province_l_english.yml` — 33 lines,
  **the real names**:
  ```
  ﻿l_english:
  xiangyan_province: "Xiangjing"
  dean_province: "Anle"
  anlu_province: "Yangwu"
  ```
  (`:1-4`)

Same basename, same tree, different subdirectory, same 33 keys. One shadows the other and the
Chinese province names either all read correctly or all read as raw keys — a coin flip the
author does not control. (`find . -name "*_l_english.yml" -printf "%f\n" | sort | uniq -d`
returns exactly this one filename.)

### 6.3 They also ship an `in_game/localization/` tree

`in_game/localization/english/` holds three files —
`late_ming_crisis_l_english.yml` (31 lines), `new_age_l_english.yml`,
`zzz_1644_heir_selection_l_english.yml` — plus a `simp_chinese` twin set.
Vanilla's `in_game/localization/` contains only a `jomini` subdirectory. Whether the engine
reads a mod's `in_game/localization/english/` is **not established by this study**; what is
established is that the situation `late_ming_crisis` has its display name in
`main_menu/…/w_situations_l_english.yml:2-3` (the tree that certainly works) and only its
*action and GUI* keys in the `in_game` tree — so a failure there would degrade the panel, not
the situation's name. That split is itself a hazard.

Two more defects in that file: the first block of keys (`:4-17`) sits at **column 0** while the
second block (`:20-29`) has the conventional one-space indent, and vanilla is uniformly
one-space.

### 6.4 The big miss: an entire situation ships unlocalised

`war_of_three_kingdoms` has **zero** loc keys, in any language, in the mod or in vanilla:

| Key referenced | Where referenced | Files containing it (mod, all langs) | (vanilla english) |
|---|---|---|---|
| `english_civil_war.*` (12 events × title/desc/options) | `in_game/events/situations/war_of_three_kingdoms.txt:8-9` etc. | **0** | 3 (unrelated) |
| `war_of_three_kingdoms_royalist_tt` | `war_of_three_kingdoms.txt:159` | **0** | 0 |
| `WAR_OF_THREE_KINGDOMS_ROE` | `war_of_three_kingdoms.txt:209` | **0** | 0 |
| `ENG_STRENGTH_TT` | `war_of_three_kingdoms.gui:90` | **0** | 0 |
| `PARLIAMENTARIAN_SIDE_TT` | `war_of_three_kingdoms.gui:116` | **0** | 0 |

Both `legend_key` entries, all three map tooltips, both strength labels, both side headers, and
every one of the 12 events' 16 options will render as raw keys.

---

## 7. CROSS-REFERENCE DEFECTS FOUND (all silent failures)

Recorded here because they are the concrete failure modes our harness should catch.

1. **Four situation-fired events do not exist.**
   `war_of_three_kingdoms.txt:72` fires `war_of_three_kingdoms.1`, `:107` fires `.100`,
   `:136` fires `.101`, `:144` fires `.102`. The event file next to it
   (`in_game/events/situations/war_of_three_kingdoms.txt:1`) declares
   `namespace = english_civil_war` and defines only `english_civil_war.250` … `.261`.
   `grep -rn "^war_of_three_kingdoms\.\|namespace = war_of_three_kingdoms" in_game/events/`
   → **empty**. The situation's entire on_start broadcast and all three on_ended endings are dead.

2. **A country modifier referenced four times exists nowhere.**
   `war_of_three_kingdoms.txt:77`, `:85` `add_country_modifier = { modifier = war_of_three_kingdoms_impact … }`
   and `:149`, `:150` `remove_country_modifier = war_of_three_kingdoms_impact`.
   `grep -rn "war_of_three_kingdoms_impact"` over the mod returns only those four lines; over
   vanilla, nothing.

3. **Dangling `hint_tag`s.** The mod ships **no** `in_game/common/scriptable_hints/` directory
   (`ls in_game/common/ | grep -i hint` → empty), yet declares
   `hint_tag = hint_thirty_years_war` (`thirty_years_war.txt:3`) and
   `hint_tag = hint_war_of_three_kingdoms` (`war_of_three_kingdoms.txt:4`), and its panels open
   `hint_the_deluge` (`the_deluge.gui:68`), `hint_thirty_years_war` (`thirty_years_war.gui:212`),
   `hint_war_of_three_kingdoms` (`war_of_three_kingdoms.gui:71`). Vanilla's
   `scripted_hints.txt` defines 92 hints and contains **zero** of those three.
   Only `hint_tag = hint_red_turban_rebellions` (`zzz_late_ming_crisis.txt:3`) resolves —
   `VANILLA: in_game/common/scriptable_hints/scripted_hints.txt:862`.

4. **A `legend_key` colour that is not a registered colour.**
   `war_of_three_kingdoms.txt:210` `color = map_ROE`. `map_ROE` appears nowhere in
   `VANILLA: main_menu/common/named_colors/` (its sibling `map_ENG` does, at `02_map.txt:15`).

5. **Legend contradicts the map it legends.**
   `zzz_late_ming_crisis.txt:441-475` paints MNG `orange`, CSH `blue`, QNG `yellow`, participants
   `green`. Its `legend_key` block at `:477-496` says MNG `yellow`, CSH `red`, QNG `blue`,
   participants `green`. Three of four rows are wrong, and `require_color_on_map = yes` will
   quietly suppress the rows whose colour never appears. Same class of error in
   `war_of_three_kingdoms.txt`: map uses `rgb { 245 210 80 }` / `rgb { 200 150 255 }` (`:185`,
   `:198`) while the legend claims `map_ROE` / `map_ENG` (`:210`, `:215`).

6. **`monthly_spawn_chance = 100`** (`zzz_late_ming_crisis.txt:2`) against a documented 0..1
   range (`VANILLA: readme.txt:5`). Harmless in practice (it clamps to certainty) but it is a
   100× magnitude error and signals the author never read the readme.

7. **Hardcoded English in `.gui`** in a mod that ships Chinese and Japanese:
   `raw_text = "Netherlands"` (`netherland_independent.gui:174`),
   `raw_text = "Spain"` (`:216`), `raw_text = "Hesse"` (`thirty_years_war.gui:315`),
   `raw_text = "Current War Balance"` (`:334`), `raw_text = "Austria"` (`:358`),
   `raw_text = "Current War Length: [GetGlobalVariable('current_religion_war_length').GetValue]"` (`:251`).
   (Note: `raw_text` with a *loc key* is legitimate — vanilla does it at
   `VANILLA: guelphs_and_ghibellines.gui:703`. The defect is the literal prose.)

8. **A 6.3 MB backup shipped inside `main_menu/setup/start/`** —
   `main_menu/setup/start/06_pops.txt.backup`, sitting beside the live 13.9 MB `06_pops.txt`.
   The extension probably keeps the parser away, but it is 6 MB of dead payload in the most
   parse-sensitive directory in the game.

9. **BOM discipline is absent, and nothing broke.** Measured across the situation corpus:
   `in_game/common/situations/` — 5 with BOM, 3 without;
   `in_game/events/situations/` — 4 with, 2 without;
   `in_game/gui/panels/situation/` — 1 with (`thirty_years_war.gui`), 6 without.
   `main_menu/setup/start/22_zzz_w_situations.txt` — **no BOM**, matching our measured rule.
   Takeaway: outside `setup/start`, BOM presence in `.txt` is not load-bearing; inside it, our
   existing rule stands unchallenged (all 40 files in their `setup/start` are BOM-free).

---

## 8. VERDICT

### 8.1 Techniques worth copying into the 1066 conversion (7)

**T1 — Neuter every out-of-era vanilla situation with a `REPLACE:` sweep in one additive file.**
`in_game/common/situations/zzz_1644_overrides.txt:1-132` disables 16 vanilla situations with a
uniform five-line block, without overriding a single vanilla *file*. Our 1066 equivalent is the
mirror image: `can_start = { current_year > 1342 }` for the ones that must wait (`black_death`,
`hundred_years_war`, `italian_wars`, `western_schism`, `reformation`, `sengoku`,
`rise_of_the_ottomans`, `rise_of_timur`, `guelphs_and_ghibellines`, `fall_of_delhi`,
`hussite_wars`, `council_of_trent`, `nanbokuchou`, `treaty_of_tordesillas`, `great_pestilence`,
`war_of_religions`), and `can_start = { always = no }  visible = { always = no }` for anything
that can start from world state alone (their treatment of `reformation`,
`zzz_1644_overrides.txt:57-64`). This costs one file and preserves every vanilla situation for
the late game.

**T2 — Arm a future situation from a dated DHE that sets a global variable, not from a date.**
`flavor_zaz.2000` (`in_game/events/DHE/flavor_ZAZ.txt:389-393`, window 1648-1673,
`monthly_chance = 15`, `fire_only_once = yes`) sets `rise_of_chemielnicki` at `:502`, which is
`the_deluge`'s only non-date gate (`the_deluge.txt:13`). For 1066 this is the pattern for
Manzikert: a Seljuk DHE in a 1068-1075 window sets a flag, and the situation's `can_start`
reads the flag. The situation then starts *because the history happened*, not because the
calendar turned — which survives a player who conquered Anatolia first.

**T3 — Write `can_end` as an OR-ladder of `custom_tooltip`-wrapped branches, because the ladder
IS the UI.** `thirty_years_war.txt:22-44` is rendered verbatim into the panel by
`TooltipRequirementsList = { textcontext = "[SituationView.GetActiveSituation.GetSituation.GetEndConditions]" }`
(`the_deluge.gui:60-62`). A bare `NOT = { exists = … }` shows the player raw script; a wrapped
one shows a sentence. And `custom_tooltip = { text = X  always = no }` (`:29-32`) lets you
advertise an end condition you have not built yet.

**T4 — Bounded phase machines: `on_start` seeds a counter and a phase, `on_monthly` rolls,
`can_end` reads the phase.** `peace_talk_in_westphalia.txt:28-45` (seed), `:47-103` (roll,
including clearing all five topic globals before setting the new one), `:18`
(`can_end = { var:peace_talk_in_westphalia_phase = 5 }`). 25 months, five topics, deterministic
exit. This is the right skeleton for a First Crusade council or a Great Schism negotiation —
far better than an open-ended `current_year >` end.

**T5 — Hoist recurring work out of `on_monthly` into self-gating `on_action` handlers with a
re-entrancy flag.** `in_game/common/on_action/the_deluge.txt:1-19` gates on
`situation:the_deluge = { situation_is_active = yes }` *inside the handler's own trigger*, and
`netherland_independent.txt:6` adds `NOT = { has_global_variable = temp_monthly_… }` with the
flag set `days = 10` (`corruption_on_actions.txt:7-10`). All of them are wired in from one
aggregator, `zzz_1644_monthly.txt:2-16`. Benefit: the work also runs on `on_location_occupied` /
`on_siege_won` (`the_deluge.txt:1`, `on_location_occupied.txt:1-13`) rather than only on the
monthly tick, so map state reacts immediately.

**T6 — `type = situation` generic actions are the player's agency inside a situation.**
Twelve of them, and the boilerplate is small: `type = situation` + `potential` gated on
`situation:X = { situation_is_active = yes }` + a `select_trigger { looking_for_a = situation
target_flag = recipient … visible = { situation:X = this  situation_is_active = yes } }`
(`in_game/common/generic_actions/thirty_years_war.txt:1-42`). They accept `price =`
(`the_steppe.txt:25`), `cooldown = { … years = 3 }` (`:27-30`), `show_message = no` (`:3`), and
runtime target lists via `source_global_list` (`zzz_late_ming_crisis_actions.txt:46`). This is
how a 1066 situation gives the player buttons instead of only events. It also satisfies our
"human choice" rule structurally — the AI reaches them through `ai_tick`/`ai_will_do`, the
player through the panel.

**T7 — Copy `the_deluge.gui` as the panel template and let the icon bind by convention.**
81 lines, `situation_panel` + `two_countries_header_template` + one
`situation_card_expandable` showing the end conditions — that is a complete, non-empty panel.
Add art by dropping `<situation_key>.dds` into
`main_menu/gfx/interface/icons/situations/`: **no `.gfx` file is needed** (the mod ships none)
because `common.gui:14` uses `[SituationView.GetActiveSituation.GetIcon]`. And if you have no
art, point at vanilla's — `thirty_years_war.gui:444` reuses `war_of_religions.dds`,
`late_ming_crisis.gui:13` reuses `red_turban_rebellions.dds`.

**Bonus T8 — the DHE wave is how you fill the years.** 916 `dynamic_historical_event` blocks,
**333 of them opening at the exact moved start date**, organised one file per tag
(`in_game/events/DHE/flavor_ENG.txt` 86 blocks, `flavor_FRA.txt` 73, `flavor_HAB.txt` 67).
Situations are 2.9 % of their event mass. If our 271-year gap needs filling, the honest budget
is DHE-heavy, situation-light.

### 8.2 Anti-patterns to avoid (5)

**A1 — Never let a situation's `on_start`/`on_ended` fire an event that does not exist.**
`war_of_three_kingdoms.txt` fires `war_of_three_kingdoms.1/.100/.101/.102`; its own event file
declares `namespace = english_civil_war` and defines none of them. The whole situation is a
silent no-op at both ends. **Harness check:** for every `trigger_event*` inside
`common/situations/`, resolve `<namespace>.<id>` against the declared namespaces in
`events/` — and remember our own decoder note that the delayed form
`trigger_event_silently = { id = X days = { 3 10 } }` must be matched too
(`zzz_late_ming_crisis.txt:229-232`).

**A2 — Never ship a situation without its localisation.** `war_of_three_kingdoms` has zero loc
keys anywhere: 12 events × title/desc, 16 option names, 3 map tooltips
(`war_of_three_kingdoms.txt:159/163/166`), 2 legend descs (`:209/:214`), 4 GUI labels
(`war_of_three_kingdoms.gui:90/102/116/136`). The situation is fully coded, fully wired, and
completely unreadable. **Harness check:** collect `custom_tooltip`, `legend_key.desc`, event
`title`/`desc`/`option.name` and GUI `text =` keys from every situation asset and assert each
resolves in `main_menu/localization/english/`.

**A3 — Never ship two loc files with the same basename.**
`main_menu/localization/english/00_province_l_english.yml` (values = the keys) and
`main_menu/localization/english/location_names/00_province_l_english.yml` (values = real names)
are a live coin-flip over 33 Chinese province names. Our existing rule is vindicated; the fix
is trivial (rename) and the failure is invisible until a player reads a map. Note also their
`in_game/localization/english/` tree, which vanilla uses only for `jomini` — do not follow them
there.

**A4 — A `legend_key` is a promise about `map_color`; keep them in one edit.**
`zzz_late_ming_crisis.txt` maps MNG orange / CSH blue / QNG yellow (`:441-462`) and legends them
yellow / red / blue (`:477-491`). With `require_color_on_map = yes` the mismatched rows vanish
from the legend entirely, so the player gets a partial legend for a fully coloured map and no
error anywhere. Same in `war_of_three_kingdoms.txt` (literal rgb vs `map_ROE`/`map_ENG`), where
`map_ROE` is not even a registered colour. **Harness check:** every `legend_key.color` must
appear as a `map_color`/`secondary_map_color` value in the same situation AND resolve in
`named_colors/`.

**A5 — Declare `hint_tag` only if you ship the hint.** Three `hint_tag`/`selected_hint`
references (`thirty_years_war.txt:3`, `war_of_three_kingdoms.txt:4`, `the_deluge.gui:68`) point
at hints that exist in neither the mod (no `scriptable_hints/` directory at all) nor vanilla's
92. A loc key named `hint_thirty_years_war` (`w_situations_l_english.yml:82`) does **not**
register a hint — and its value is itself broken, an unterminated string
(`"[GetSituationByKey('war_of_religions').GetNameWithNoTooltip]` with no closing quote), which
by our one-physical-line rule will swallow or drop the entry. Reuse a vanilla hint tag the way
`zzz_late_ming_crisis.txt:3` reuses `hint_red_turban_rebellions`, or ship
`in_game/common/scriptable_hints/`.

**Bonus A6 — read `VANILLA: in_game/common/situations/readme.txt` before setting any numeric
field.** `monthly_spawn_chance = 100` (`zzz_late_ming_crisis.txt:2`) against a documented 0..1
range is what happens when you don't. The same readme documents `on_ending` (fires *before* the
status flips) — a hook Anno 1644 never uses once in eight situations, and the only place to run
an effect while the situation is still queryable.

---

## 9. LOOSE ENDS / UNVERIFIED

- **`start_date` inside `situation_manager`** — appears only as a comment
  (`main_menu/setup/start/22_zzz_w_situations.txt:7`, `:12`), no vanilla attestation, not in the
  script docs. **UNVERIFIED — do not use.**
- **What `netherland_independent = { }` with an empty body actually does** in
  `22_zzz_w_situations.txt:2-3`. Vanilla's `rise_of_the_ottomans={}`
  (`VANILLA: main_menu/setup/start/22_situations.txt:2-15`) has the same shape. Since the
  situation's `can_start` is satisfied at 1644 anyway and `monthly_spawn_chance` is 1.0, the
  entry is not doing observable work and its purpose cannot be determined statically.
  **UNVERIFIED.**
- **Whether a mod's `in_game/localization/english/` is loaded at all.** Vanilla's
  `in_game/localization/` holds only `jomini`. The mod ships three files there. Not resolvable
  without running the game. **UNVERIFIED.**
- **Whether `raw_text` resolves loc keys.** Vanilla uses `raw_text = "GAG_GUELPHS_TITLE_NO_TOOLTIP"`
  (`VANILLA: in_game/gui/panels/situation/guelphs_and_ghibellines.gui:703`) and
  `raw_text = "black_death_end_trigger_tt"` (`black_death.gui:136`), so it evidently does at
  least sometimes. I make no claim either way; the anti-pattern I record (A-list item 7) is only
  about literal English prose, which is wrong under any reading.
- The mod's tag-registration discipline was spot-checked and is **correct**: `ROE` has an
  identity block in an additive file (`in_game/setup/countries/zzz_new_western_europe.txt:1`)
  AND a start block (`main_menu/setup/start/10_countries.txt:1646`) — the two registrations our
  CLAUDE.md requires.
