# Craft study — situations in three published EU5 mods
### A) Rise of Timur · B) Bronze Era · C) Basileia Romaion
Research date 2026-08-04. All trees read-only; nothing was written outside this file.

Citation convention: paths are **mod-relative** unless prefixed `VANILLA:`, which means
`E:\SteamLibrary\steamapps\common\Europa Universalis V\game\`. Every claim below carries a
`file:line`. Claims I could not verify are marked **UNVERIFIED** and are few.

---

## 0. Correction to the task brief, and the single most important finding

The brief asked me to read "`rise_of_timur.txt:288-385`" as the Rise of Timur mod's action block.
**There is no `rise_of_timur.txt` in the mod.** The mod's `in_game/common/situations/` contains
exactly four files:

```
in_game/common/situations/fate_of_mesopotamia.txt      (230 lines)
in_game/common/situations/rise_of_mughals.txt          (158 lines)
in_game/common/situations/rise_of_persia.txt           (521 lines)
in_game/common/situations/wot_turkish_expansion.txt    (215 lines)
```

`rise_of_timur` is a **vanilla** situation — `VANILLA:in_game/common/situations/rise_of_timur.txt`
(389 lines). Lines 288-385 of that vanilla file are its `on_ended` tail, `tooltip`, `map_color` and
`legend_key` blocks; there are no actions there at all (actions never live in situation files —
see §1.3).

This is not a trivia correction. It is **the** structural lesson of the mod:

> Rise of Timur does not write the Timur railroad. It **rides vanilla's** `rise_of_timur`
> situation and bolts a private layer of on_actions, events, game rules and static modifiers
> around it.

The proof is that the mod references the vanilla situation by name from its own on_action file
without ever defining it:

- `in_game/common/on_action/forcewar.txt:81` — `is_situation_active = situation:rise_of_timur`
- `in_game/common/on_action/forcewar.txt:111` — `situation:rise_of_timur = { situation_is_active = yes }`

Both resolve because vanilla supplies the situation. Note in passing that the mod uses **two
different syntaxes for the same question** in one file, 30 lines apart (`is_situation_active = X`
vs `X = { situation_is_active = yes }`); both are attested in vanilla
(`VANILLA:in_game/common/situations/rise_of_timur.txt:197` uses the first form,
`:259-260` the second).

**Consequence for the 1066 project.** For Manzikert there is no vanilla situation to ride. Rise of
Timur is therefore a model for the *surrounding layer*, not for the situation core; for the core,
the models are vanilla itself and Bronze Era's `sea_peoples_crisis`.

---

## 0.1 The vanilla situation schema — the authority, found during this study

Vanilla ships a schema readme that settles every "is this a legal block" question below:
`VANILLA:in_game/common/situations/readme.txt`. Quoting lines 4-18 verbatim:

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

`on_ending` and `on_ended` are **two distinct hooks**, before and after the status flip. Both legal.

Measured key census across all 22 vanilla situation files (depth-1 keys, comments stripped):

| key | vanilla uses |
|---|---|
| `legend_key` | 79 |
| `visible` / `on_start` / `on_monthly` / `monthly_spawn_chance` / `map_color` / `hint_tag` / `can_start` / `can_end` | 22 each |
| `tooltip` | 21 |
| `on_ended` | 21 |
| `secondary_map_color` | 9 |
| `voters` | 4 |
| `resolution` | 3 |
| `on_ending` | 2 (`rise_of_the_ottomans.txt:297`, `treaty_of_tordesillas.txt:186`) |
| `is_data_map` | 2 (`black_death.txt:216`, `great_pestilence.txt:144`) |
| `international_organization_type` | 2 |
| `custom_description` | 1 |
| `content_trigger` | 1 (`rise_of_the_ottomans.txt:5`) |

`on_end` and `end_conditions`: **zero vanilla uses, absent from the readme.** This matters in §2.

---

# A. RISE OF TIMUR — the railroad craft

## A.1 Inventory

| thing | count | where |
|---|---|---|
| own situations | 4 | `in_game/common/situations/` |
| vanilla situations ridden | 2 | `rise_of_timur`, `rise_of_the_ottomans` (refs at `on_action/forcewar.txt:81`, `:26`) |
| disasters | 2 | `in_game/common/disasters/crisis_of_the_timurids.txt`, `decline_of_mamluks.txt` |
| event files | 13 | 4 in `events/situations/`, 7 in `events/DHE/`, 2 in `events/disaster/` |
| **total events** | **143** | counted via `^<ns>.<n> = {` across `in_game/events/` |
| situation actions | 19 `type = situation` | `in_game/common/generic_actions/` (see A.4) |
| own GUI panels | 4 | `in_game/gui/panels/situation/*.gui` (134-321 lines) |
| own situation icons + illustrations | 4 + 4 | `main_menu/gfx/interface/icons/situations/`, `.../illustrations/situation/` |
| game rules | 5 groups | `main_menu/common/game_rules/timur_game_rules.txt` |
| on_action files | 8 | `in_game/common/on_action/` |

Per-file event counts: `rise_of_persia.txt` 35, `crisis_of_the_timurids.txt` 24,
`wot_ottoman_extras.txt` 11, `decline_of_mamluks.txt` 11, `flavor_pap_holy_league.txt` 10,
`fate_of_mesopotamia.txt` 8, `rise_of_mughals.txt` 8, `flavor_muzaffarids_injuids.txt` 8,
`flavor_sheep_turkomen.txt` 8, `flavor_wrath_of_timur.txt` 7, `flavor_rise_of_safavids.txt` 6,
`flavor_mughals.txt` 5, `wot_war_events.txt` 2.

## A.2 How the multi-decade conquest arc is actually driven

There are **five independent drivers**, deliberately layered. This is the reusable architecture.

### Driver 1 — immortality, so the protagonist survives his own arc
`in_game/common/on_action/wot_game_start.txt:22-31`:

```
timur_immortality_setter = {
    effect = {
        character:chg_timur_lame_borjigin ?= {
            add_character_modifier = {
                modifier = historically_needed
                years = 65
            }
        }
    }
}
```

and `main_menu/common/static_modifiers/wrath_of_timur_modifiers.txt:1-6`:

```
historically_needed = {	
	game_data = {
		category = character
	}
	is_immortal = yes
}
```

A **timed** immortality (65 years) — not permanent. Note the whole hook is delayed:
`wot_game_start.txt:1-8` declares `on_game_start` with `delay = { days = 1 }` before its
sub-actions, i.e. setup is allowed to finish before characters are touched. That delay is a
technique in itself.

The counterpart, for players who don't want the railroad, is `timur_remove`
(`wot_game_start.txt:33-36`): `trigger = { has_game_rule = timur_disabled }`,
`effect = { kill_character_silently = character:chg_timur_lame_borjigin }`.

### Driver 2 — the game rule spine
`main_menu/common/game_rules/timur_game_rules.txt:1-19` defines `historical_timur` with four
options, default `historical_timur_conquests`:
`timur_disabled`, `historical_timur_conquests`, `ahistorical_timur_conquests`,
`nightmare_timur_conquests` — each carrying `flag = flavour_rule`. Four more rule groups follow
(`turk_expansion_historical`, `rise_of_the_turkomen`, `rise_of_the_safavids`,
`enable_mamluk_decline`, `:21-71`).

Nearly every railroad effect is gated on one of these. The rule is the off-switch, and it is
per-arc rather than global.

### Driver 3 — dated invasion waves as hidden fire-once events
The conquest arc is a **sequence of dated event windows**, each an invisible event that declares
war on everyone in a named geography. All four share one shape
(`in_game/events/DHE/flavor_wrath_of_timur.txt`):

| event | window | target geography | line |
|---|---|---|---|
| `wrath_of_timur.1` | 1360.1.1 → 1365.1.1, `monthly_chance = 100` | Transoxiana/Khwarazm/Badakhshan/W+E Khorasan areas | `:3-77` |
| `wrath_of_timur.10` | 1363.1.1 → 1390.1.1, `monthly_chance = 70` | `capital.region = region:persia_region` | `:236-279` |
| `wrath_of_timur.11` | 1375.1.1 → 1390.1.1, `monthly_chance = 70` | `region:caucasus_region`, `region:crescent_region` | `:281-329` |
| `wrath_of_timur.12` | 1385.1.1 → 1390.1.1, `monthly_chance = 70` | `area:punjab_area`, `area:sindh_area` | `:331-379` |

The declaration idiom, `flavor_wrath_of_timur.txt:311-326`:

```
every_known_country = {
    limit = {
        any_owned_location = {
            OR = {
                region = region:caucasus_region
                region = region:crescent_region
            }
        }
        NOT = { 
            is_at_war_with = root 
            is_subject_of = root
        }
    }
    prev = { declare_war_with_cb = { target = prev type = casus_belli:cb_timurs_conquests } }
}
```

Note `prev = { declare_war_with_cb = { target = prev ... } }` — it hops **out** of
`every_known_country` to reach TIM, then `target = prev` reaches back in to the iterated country.
Exactly one hop each way. This is the CLAUDE.md `prev` rule being obeyed correctly, and it is worth
copying verbatim as the shape for "conqueror declares on a whole region".

Each wave is also an **army injection**, `flavor_wrath_of_timur.txt:300-309`:

```
capital = {
    while = {
        count = 5
        create_sub_unit_with_owner = {
            type = a_steppe_horse_archers
            owner = root
        }
    }
}
```

5 units for the Persian and western waves, **10** for India (`:350-359`) — pacing the strength of
each wave to its difficulty.

All four are `hidden = yes`, `fire_only_once = yes`, and gated `is_ai = yes`
(`:250-253`, `:295-298`, `:345-348`). **The player never receives them.**

### Driver 4 — the continuous top-up on_action
Dated waves alone leave gaps. `in_game/common/on_action/forcewar.txt:76-105` runs on
`monthly_country_pulse` (`:14-19`) and keeps a war always live:

```
timurid_invasion_helper = {
    trigger = {
        tag = TIM
        current_year >= 1360
        is_ai = yes
        is_situation_active = situation:rise_of_timur
        character:chg_timur_lame_borjigin = { is_alive = yes }
    }
    effect = {
        random_known_country = {
            limit = { 
                is_ai = yes
                NOR = { 
                    country_type = building
                    country_type = pop
                    has_truce_with = c:TIM
                    is_subject_of = c:TIM 
                    has_mutual_scripted_relation = {
                        type = relation_type:alliance
                        target = c:TIM
                    }
                }
                any_owned_location = { is_in_scripted_geography = scripted_geography:historical_timurid_empire }
                is_neighbor_of = c:TIM
            }
            c:TIM = { declare_war_with_cb = { type = casus_belli:cb_timurs_conquests target = prev } }
        }
    }
}
```

Two things to steal. First, the exclusion list `country_type = building` / `country_type = pop` —
EU5 has non-country "countries" and a naive `random_known_country` will pick one. Second, the whole
thing is **doubly gated on `is_ai = yes`**: TIM must be AI (line 79) *and* the victim must be AI
(line 87). A human neighbour is never auto-attacked.

`timruid_nightmare_helper` (`:107-126`, sic — misspelt identifier, harmless but shipped) is the
same shape with the geography restriction removed, active only under
`has_game_rule = nightmare_timur_conquests`.

### Driver 5 — the rubber band: reverting ahistorical conquests
The most transferable idea in the mod.
`in_game/common/on_action/timur_historical_border_preservation.txt:10-24`:

```
on_timurid_occupy_ahistorical_borders = {
	trigger = {
        has_game_rule = historical_timur_conquests
		scope:winner ?= {
			tag = TIM
            is_ai = yes
            in_civil_war = no
            ruler ?= { has_character_modifier = timmy_wants_to_play } 
		}
        root = { NOT = { is_in_scripted_geography = scripted_geography:historical_timurid_empire } }
	}
	effect = { root = { change_location_owner = scope:loser } }
}
```

Hooked on `on_location_changed_owner` (`:1-8`). The AI conqueror is allowed to fight anywhere, but
any location it takes **outside** the scripted historical geography is silently handed straight
back. Result: an unbounded aggression setting produces historically bounded borders, with no cap on
the AI's war behaviour and no scripted peace deals. This is how you get "Timur conquers Persia and
then stops" without ever telling the AI to stop.

### The chaining mechanism between situations
`in_game/common/situations/wot_turkish_expansion.txt:5-11`:

```
    can_start = {
		current_date > 1490.1.1
		any_country = {
			has_variable = rise_of_the_ottomans_winner_variable
			num_locations > 500
		}
		NOT = { is_situation_active = situation:rise_of_the_ottomans }
	}
```

Situation N+1 starts when (a) situation N is no longer active, and (b) some country carries the
**winner variable N left behind**. The successor then binds that country as its protagonist,
`wot_turkish_expansion.txt:34-40`:

```
    on_start = {
		random_country = {
			limit = { has_variable = rise_of_the_ottomans_winner_variable }
			situation:wot_turkish_expansion = { set_variable = { name = wot_actor value = prev } }
		}
		var:wot_actor ?= { add_area_preference = ottoman_expansion_beyond }
```

Thereafter everything — actions, end trigger, war hooks — addresses
`situation:wot_turkish_expansion.var:wot_actor` rather than a hardcoded tag
(`generic_actions/wot_turkish_expansion.txt:6-7, :110-111, :157-158, :227-228, :246-247`;
`scripted_triggers/situation_end_triggers.txt:28-32`;
`on_action/war_end_annexations.txt:79, :92`).

**This is the pattern the 1066 project needs.** A chained arc where the protagonist is a variable,
not a tag, survives the player conquering the protagonist — and survives history going differently.

## A.3 The "keep AI on rails, leave the player free" mechanism, itemised

| mechanism | player exempt? | citation |
|---|---|---|
| invasion waves | yes — `is_ai = yes` on all four | `flavor_wrath_of_timur.txt:250, :295-298, :345-348` (and `:52` for wave 1) |
| monthly top-up war | yes, both sides | `on_action/forcewar.txt:79, :87` |
| nightmare buffs | yes | `flavor_wrath_of_timur.txt:26-38` (`is_ai = yes` + game rule) |
| border rubber band (Timur) | yes | `on_action/timur_historical_border_preservation.txt:15` |
| forced government change | yes | `flavor_wrath_of_timur.txt:399` |
| **submission to Timur** | **NO — and correctly so** | `flavor_wrath_of_timur.txt:135-233` |

The last row is the mod's best "human choice" work, and it deserves calling out. When Timur
declares war, the victim — player or AI — gets `wrath_of_timur.8` (fired from
`on_action/war_subjugation_threat.txt:9-21` on `on_war_declared`). It is a **visible, three-option
event**:

- `option = { name = wrath_of_timur.8.a }` — submit as vassal; only shown if your capital is inside
  `scripted_geography:historical_timurid_empire` (`:146-148`); `ai_will_select = { value = 40 }`
- `option = { name = wrath_of_timur.8.b }` — cede the territory inside that geography; shown only
  if your capital is *outside* it (`:207-209`); `ai_will_select = { value = 40 }`
- `option = { name = wrath_of_timur.8.c }` — fight to the death; `ai_will_select = { value = 80 }`

The AI's own weighting favours fighting (80 vs 40+40). The railroad is offered, not imposed, and it
is offered to AI and player on identical terms. This is precisely the CLAUDE.md "Human choice"
rule, implemented.

Option (a) also contains the mod's most elaborate effect — a **partition** of the submitting
country into one new country per area (`:160-198`), using `create_country_from_location`:

```
root = {
    random_owned_location = {
        limit = { area = scope:current_area }
        save_scope_as = chosen_capital
        create_country_from_location = {
            save_scope_as = new_country
            set_capital = prev
        }
    }
    every_owned_location = {
        limit = { area = scope:current_area }
        add_core = scope:new_country
        change_location_owner = scope:new_country
    }
}
```

Two notes against CLAUDE.md's vanilla-triple rule (`change_location_owner` + `add_core` +
`change_integration_level = core`): this call **omits `change_integration_level`**
(`:189-193`), so the new countries' land should sit at `integration_conquered`.
**UNVERIFIED** whether `create_country_from_location` sets integration itself for the
locations it is subsequently given; only in-game observation settles it. Treat as a risk, not a
confirmed bug.

## A.4 The situation ACTIONS

19 blocks carrying `type = situation`, distributed:
`rise_of_persia.txt` 8, `wot_turkish_expansion.txt` 4, `fate_of_mesopotamia.txt` 2,
`rise_of_mughals.txt` 1, `rto_action_reworks.txt` 1, plus disaster-side
`crisis_of_the_timurids.txt` and `decline_of_mamluks.txt`.

The `rise_of_persia` set (`in_game/common/generic_actions/rise_of_persia.txt`):

| action | line | purpose (from the file's own comment) |
|---|---|---|
| `proclaim_empire` | 1 | "strongest nation proclaims himself empire, and rival will do so as well, pitting both nations as enemies" |
| `press_persian_claims` | 73 | "Gives special cb to expand" |
| `patronize_culture` | 289 | — |
| `resettle_devastated_lands` | 399 | "add development, and population growth in a province, make buildings cheaper, increasing prosperity, and more" |
| `restore_persian_cities` | 502 | "add a modifier to the large persian cities, bringing migration, prosperity, and slight development, and increasing max control" |
| `mint_royal_coinage` | 617 | "Gain gold and prestige as you mint your own coin to be used in Persia" |
| `seek_clerical_endorsement` | 692 | "increase self tolerance, add some levy/manpower buff, add legitimacy, and stability" |
| `recruit_turko_mongol_talent` | 759 | "Hire some horse archers, and a slight buff to horses, and a decent general" |

Common skeleton, from `proclaim_empire` (`:1-71`) and repeated in all eight:

```
type = situation
show_message = no
potential = { scope:actor = { ... } }
allow = { scope:actor = { at_war = no } }
automation_tick = never
automation_tick_frequency = 12
ai_tick = monthly
ai_tick_frequency = 24
cooldown = { type = <key>_cooldown_key years = N }
select_trigger = {
    looking_for_a = situation
    interaction_source_list = { situation:rise_of_persia = { add_to_list = source } }
    target_flag = recipient
    name = "choose_situation"
    column = { data = name }
    visible = { situation:rise_of_persia = this  situation_is_active = yes }
}
effect = { ... }
ai_will_do = { ... }
```

`press_persian_claims` adds a **second** `select_trigger` for the target province
(`:120-160`), with `looking_for_a = province`, `none_available_msg_key = "no_provinces_available"`,
and three display columns (`owner_flag`, `name`, `population`). That is the two-step
"pick a situation, then pick a target" UI pattern.

**How the AI is told the actions exist** — `in_game/common/generic_action_ai_lists/rise_of_persia.txt`
(complete file):

```
rise_of_persia_list = {
    potential = {
        can_see_situation = situation:rise_of_persia
    }
    actions = {
        proclaim_empire
        press_persian_claims
        patronize_culture
        resettle_devastated_lands
        restore_persian_cities
        mint_royal_coinage
        seek_clerical_endorsement
        recruit_turko_mongol_talent
    }
}
```

A situation action without a matching `generic_action_ai_lists` entry is a **player-only** action.
This is a silent-failure class: the action will look fine and the AI will simply never use it.

`ai_will_do` in `press_persian_claims` (`:176-286`) is the most careful scoring in the mod — six
`subtract = 1000` vetoes (own subject, bankruptcy, loans, stability < 0, truce, existing CB), then
`add = { value = "scope:actor.relative_defensive_alliance_strength(scope:target.owner)" multiply = 100 subtract = 60 }`
and `add = { value = "scope:actor.conquer_desire(scope:target.owner)" divide = 5 }`. Note the
**function-call syntax in a quoted string** — `"scope:actor.conquer_desire(scope:target.owner)"`.

## A.5 Runtime cast: `create_character` and `found_dynasty`

15 `create_character` calls, 2 `found_dynasty` calls across the mod.

**The setup file for the dynasty is entirely commented out** —
`main_menu/setup/start/timurid_dynasty.txt`, complete contents (4 lines):

```
# dynasty_manager = {
#     gurkani_dynasty = {
#         name = { name = gurkani_dynasty }
#     }
# }
```

So the Gurkani dynasty is created **at runtime**, in an event option, confirming the CLAUDE.md
note about this mod. `in_game/events/DHE/flavor_wrath_of_timur.txt:107-126`:

```
        create_character = {
            first_name = name_saray_mulk
            dynasty = dynasty:borjigin_dynasty
            culture = culture:mongolian_culture
            religion = religion:sunni
            father = character:chg_qazan_borjigin
            birth_date = 1341.1.1
            female = yes
            save_scope_as = timur_wife
        }

        ruler = {
            if = { 
                limit = { exists = first_spouse }
                divorce_character = first_spouse
            } 
            found_dynasty = gurkani_dynasty
            every_descendant = { change_dynasty = dynasty:gurkani_dynasty }
            marry_character = scope:timur_wife
        }
```

Argument shapes worth recording exactly:
- `found_dynasty = gurkani_dynasty` — **bare identifier, no `dynasty:` prefix.**
- `change_dynasty = dynasty:gurkani_dynasty` — **`dynasty:` prefix required here.**
- `dynasty = dynasty:borjigin_dynasty` inside `create_character` — prefix required.
- `father = character:chg_qazan_borjigin` — an existing setup character, by `character:` prefix.
- `first_name = name_saray_mulk` — a **loc key**, not a literal string.

The other `found_dynasty` is `in_game/events/DHE/flavor_mughals.txt:6`, same bare form.

The other flavour of `create_character` is the **statless generated general**,
`generic_actions/rise_of_persia.txt:811-877` (and a `turkmen_culture` twin at `:880-946`,
selected 50/50 by `random_list` at `:809`):

```
create_character = {
    culture = culture:mongolian_culture
    trait_category = general
    adm = {
        integer_range = {
            min = { value = 30  add = { value = army_tradition  multiply = 0.5 } }
            max = { value = 80  add = { value = army_tradition  multiply = 0.5 } }
        }
    }
    ... dip, mil identical ...
    add_character_modifier = { modifier = recruited_in_the_military  mode = add_and_extend }
    add_trait = trait:born_to_the_saddle
    add_trait = trait:hardy_warrior
    add_trait = trait:goal_oriented
}
```

`integer_range` with `min`/`max` **script-value blocks** scaling off `army_tradition` — no
`birth_date`, no `first_name`, no `dynasty`: the engine fills them. That is the right way to mint
anonymous personnel, versus the fully-specified form used for a named historical wife.

## A.6 Failure and failsafe handling

- **End conditions are a scripted trigger, not inline** —
  `in_game/common/scripted_triggers/situation_end_triggers.txt` holds all four
  (`rise_of_persia_end_trigger:11`, `wot_turkish_expansion_end_trigger:24`,
  `rise_of_mughals_end_trigger:41`, `fate_of_mesopotamia_end_trigger:58`). Each is
  `OR = { <hard date cutoff>  <victory condition> }` — e.g. `:12-21`:

  ```
  OR = {
      current_year >= 1600
      custom_tooltip = {
          text = rop_end_trigger
          OR = {
              rise_of_persia_end_land_ownership = { target = rop_strongest_native_variable }
              rise_of_persia_end_land_ownership = { target = rop_strongest_invader_variable }
          }
      }
  }
  ```

  **Every situation has a date backstop.** None can hang forever. `rise_of_mughals_end_trigger`
  (`:41-47`) additionally has `NOT = { country_exists = c:MUG }` — the protagonist dying ends the
  situation rather than leaving it stuck.

- **`?=` everywhere on protagonist access.** `var:rop_strongest_native_variable ?= { ... }` appears
  throughout `situations/rise_of_persia.txt` (`:134, :140, :146, :152, :162, :178, :184, :200, :293, :303`).
  The safe-access operator is used on *every* dereference of a country that may have been annexed.

- **`on_ended` cleans up**, `situations/rise_of_persia.txt:341-359`: removes
  `ai_force_annexation` and `rop_expansionism_improvement` from every list member,
  `clear_global_variable_list` on both lists, and destroys the Ilkhanate IO if it still exists.
  A situation that ends without removing its own modifiers leaves permanent buffs on the map.

- **Vanilla's own failsafe, for comparison**: `VANILLA:in_game/common/situations/rise_of_timur.txt:298`
  — `remove_global_variable = timur_character` in `on_ended`, and `:299-304` strips
  `rot_timurs_core_region` from every owned location.

## A.7 Pacing — measured

`situations/rise_of_persia.txt` `on_monthly` (`:109-290`) contains three independent rolls:

1. `:128-206` — `random_list = { 85 = {}  10 = {...}  3 = {...} }`, weights summing 98.
   ≈10.2 %/month an integration event (`rise_of_persia.105`), ≈3.1 %/month a vassalisation event
   (`rise_of_persia.101`). Both are further gated by inner `trigger` blocks.
2. `:208-219` — the Yazd holder, `90 = {} / 10 = {...}`: ≈10 %/month for `rise_of_persia.500`,
   one-shot via `NOT = { has_variable = persia_zoro_event }`.
3. `:221-289` — one random native/invader country, weights `86` plus **thirteen** `2`s = 112.
   ≈23.2 %/month that *some* flavour event fires (`rise_of_persia.600`-`.611`, `.616`).

Rough totals: **≈1.6 structural events/year plus ≈2.8 flavour events/year** in the Persian theatre,
on top of the per-country `dynamic_historical_event` windows. That is the calibration: a situation
should speak a few times a year, not monthly.

The vanilla comparison is a **cooldown counter** rather than probability —
`VANILLA:in_game/common/situations/rise_of_timur.txt:68-73` increments
`rise_of_the_timur_event_cooldown` monthly and only rolls when `> 10`, then resets it to 1; a
second counter `rise_of_the_timur_unique_event_cooldown` gates unique events at `> 20`
(`:131-133`). **Deterministic spacing, ~11 and ~21 months.** For a 271-year gap this is the safer
of the two idioms — it cannot cluster.

Vanilla also gates unique events on `can_fire_situation_event = { situation = root  event = <key> }`
and `has_fired_situation_event = { ... }` (`:137-144`, `:154-161`, `:171-174`, `:190-193`,
`:205-208`, `:227-229`, `:252-255`) — a per-situation fired-event registry, cleaner than the
mod's `has_variable` flags.

## A.8 Techniques worth stealing — Rise of Timur

1. **Timed immortality via a `is_immortal = yes` character static modifier.**
   `main_menu/common/static_modifiers/wrath_of_timur_modifiers.txt:1-6` +
   `on_action/wot_game_start.txt:22-31`. Directly applicable: Alp Arslan must survive to 1071,
   Robert Guiscard to 1085. Prefer the timed form (`years = 65`) over `days = -1`.
2. **The border rubber band.** `on_action/timur_historical_border_preservation.txt:10-24`.
   Let the AI conqueror be maximally aggressive, then revert every gain outside a
   `scripted_geography` on `on_location_changed_owner`. This is how you railroad an outcome
   without scripting the war.
3. **Protagonist-as-variable, and situation chaining through a winner variable.**
   `situations/wot_turkish_expansion.txt:5-11` and `:34-40`. Essential for a 271-year arc where the
   protagonist may be conquered, or may be the player.
4. **Per-arc game rules with a `_disabled` option and a `kill_character_silently` implementation.**
   `main_menu/common/game_rules/timur_game_rules.txt:4-6` + `on_action/wot_game_start.txt:33-36`.
5. **The subjugation offer as a real 3-option event with `ai_will_select`, given to player and AI
   alike.** `events/DHE/flavor_wrath_of_timur.txt:135-233`. This is the CLAUDE.md human-choice rule
   done properly, and it is worth copying structurally.
6. **`generic_action_ai_lists` is mandatory, not optional.**
   `in_game/common/generic_action_ai_lists/rise_of_persia.txt` — without it the AI never uses a
   situation action, silently.

## A.9 Mistakes to avoid — Rise of Timur

1. **Dangling `hint_tag`s.** The mod declares three new hint tags and defines none:
   `situations/rise_of_persia.txt:3` (`hint_rise_of_persia`),
   `situations/rise_of_mughals.txt:3` (`hint_rise_of_mughals`),
   `situations/wot_turkish_expansion.txt:3` (`hint_wot_turkish_expansion`).
   Hint tags live in `VANILLA:in_game/common/scriptable_hints/scripted_hints.txt`, and the mod
   **ships no `scriptable_hints` folder at all**. I checked each of the three against that file:
   all three UNDEFINED. Worse, `gui/panels/situation/rise_of_persia.gui:58` wires a button to
   `OpenLateralViewWithParams('hints', 'selected_hint = hint_rise_of_persia')` — a button to a
   hint that does not exist.
2. **A copy-pasted hint tag.** `situations/fate_of_mesopotamia.txt:3` reads
   `hint_tag = hint_wot_turkish_expansion` — the Mesopotamia situation points at the Turkish
   expansion hint. Pure copy-paste, invisible in game beyond a wrong/absent hint.
3. **The border rubber band is `is_ai`-gated only for Timur.** Compare
   `timur_historical_border_preservation.txt:15` (`is_ai = yes`, present) with the three siblings
   in the same file — `on_safavid_occupy_ahistorical_borders` (`:26-42`),
   `on_mughal_occupy_ahistorical_borders` (`:44-59`), `on_ottoman_hungarian_invasion_borders`
   (`:61-76`) — **none of which contains `is_ai`**. A human playing IRA/ABL whose ruler carries
   `rise_of_ismail`, or MUG with `rise_of_babur`, or TUR with `special_war_modifier`, has
   conquests outside the scripted geography silently confiscated on
   `on_location_changed_owner`, with no message. That is exactly the failure mode CLAUDE.md's
   "Human choice" section exists to prevent, and it is invisible in testing unless you play those
   tags.
4. **`.gui` files carry a BOM.** `gui/panels/situation/rise_of_persia.gui` begins `ef bb bf`
   (measured). CLAUDE.md's measured rule is that vanilla `.gui` is BOM-free (483 files, only 49
   with one). Not necessarily fatal here, but it is a deviation from the vanilla majority and
   should not be copied as precedent.

---

# B. BRONZE ERA — situations at a moved START_DATE

## B.1 The moved date, and what it does to date gates

`loading_screen/common/defines/zz_bronze_era_dates.txt:5-6`:

```
	START_DATE = "1.1.1"
	END_DATE = "1329.12.31"
```

Year 1 is the epoch. Every situation date gate is therefore an **offset from the start**, and the
mod documents the conversion inline. `in_game/common/situations/00_bronze_sea_peoples_crisis.txt:9-14`:

```
	can_start = {
		# Visual chronology: 1195 BC.
		# Internal year 1 = 1209 BC, so 1195 BC = internal year 15.
		current_date >= 15.1.1
		NOT = { has_global_variable = sea_peoples_crisis_ended }
	}
```

**This comment convention is the single most valuable thing in Bronze Era for our project.** A bare
`current_date >= 15.1.1` is unreadable and unreviewable; the two-line comment giving the displayed
date and the arithmetic makes it checkable. Other instances:
`00_bronze_trojan_war_phase_1.txt:7` (`>= 5.1.1`), `:17` (`>= 14.1.1`),
`00_bronze_trojan_war_phase_2.txt:8` (`>= 14.1.1`), `:55` (`>= 14.6.1`).

For 1066 the dates are not remapped (1066 is a real EU5 date), so the arithmetic does not apply —
but the discipline of writing the *historical event* next to the *engine date* does.

## B.2 Seeding: nothing is active at start

`main_menu/setup/start/22_situations.txt` — the **entire file** (5 lines):

```
situation_manager = {
	# Bronze Age crisis situations are not forced active at game start.
	# Sea Peoples begins through its 1195 BCE trigger, and the Hattie Collapse
	# follows only after Sea Peoples pressure reaches Hatti or phase 2.
}
```

An empty `situation_manager` block with the reasoning written down. Every situation arrives through
`can_start` + `monthly_spawn_chance` instead. Two of the five use
`monthly_spawn_chance = monthly_spawn_chance_unique`
(`00_bronze_sea_peoples_crisis.txt:2`, `00_bronze_hatti_collapse.txt:2`); the Trojan pair use a raw
`monthly_spawn_chance = { value = 100 }` (`00_bronze_trojan_war_phase_1.txt:2-4`,
`phase_2.txt:3-5`).

BOM check (measured): `main_menu/setup/start/22_situations.txt` = `73 69 74` — **no BOM**, correct
per the CLAUDE.md setup/start rule. `in_game/gui/panels/situation/sea_peoples_crisis.gui` = `73 69 74`
— no BOM, also correct. But `in_game/common/situations/00_bronze_sea_peoples_crisis.txt` = `73 65 61`
— **no BOM**, where vanilla situation files do carry one
(`VANILLA:.../rise_of_the_ottomans.txt` begins `ef bb bf`). A deviation; the mod evidently loads,
so BOM is not required there, but it is not the vanilla convention.

## B.3 Scale and tone of the five situations

| situation | lines | actions | GUI panel | icon | illustration |
|---|---|---|---|---|---|
| `sea_peoples_crisis` | 525 | 10 (+1 raiding) | 351 lines | yes | yes |
| `bronze_hatti_collapse` | 361 | 11 | 305 lines | yes | yes |
| `mycenaean_fragmentation` | 192 | 15 | 231 lines | yes | yes |
| `trojan_war_phase_1` | 45 | 0 | 151 lines | yes | **no** |
| `trojan_war_phase_2` | 129 | 0 | 96 lines | **no** | **no** |

Events: 111 total across 10 files — `bronze_ruins_expedition_events.txt` 24,
`bronze_mycenaean_league_events.txt` 22, `bronze_hatti_collapse_events.txt` 20,
`bronze_sea_peoples_crisis_events.txt` 20, `bronze_city_razing_events.txt` 10,
`bronze_city_prestige_events.txt` 7, `bronze_trojan_war_phase_1_events.txt` 3,
`bronze_rome_foundation_events.txt` 2, `bronze_ruins_debug_events.txt` 2,
`bronze_trojan_war_phase_2_events.txt` 1.

The gradient is stark: three deep situations and two shallow ones. The Trojan pair are essentially
date-gated modifier applications with no monthly life at all (no `on_monthly`, no `tooltip`, no
`map_color`, no `legend_key` in either — see the key census in §B.5).

**Action naming is exemplary.** The 36 situation actions read as historical decisions rather than
mechanics — `00_bronze_hatti_collapse_actions.txt`: `bronze_hatti_send_grain_to_cities:1`,
`bronze_hatti_fortify_the_coast:52`, `bronze_hatti_appease_vassals:101`,
`bronze_hatti_crush_rebellious_lords:151`, `bronze_hatti_evacuate_settlements:210`,
`bronze_hatti_centralize_around_hattusa:258`, `bronze_hatti_recognize_successors:307`,
`bronze_hatti_host_vassal_kings:360`, `bronze_hatti_seize_temple_grain:408`,
`bronze_hatti_call_chariot_host:453`, `bronze_hatti_abandon_syrian_road:501`.
Similarly `00_bronze_mycenaean_league_actions.txt` has 15, from
`mycenaean_call_megaron_council:1` to `mycenaean_restore_palace_network:956`.

Note also `00_bronze_sea_peoples_raiding_actions.txt:1-8` — `sea_peoples_raid_coastal_settlements`
is **`type = owncountry`**, not `type = situation`, with
`player_automated_category = privateers`. The crisis's *victims* get situation actions; its
*perpetrators* get a country action. Different actor classes get different action types.

## B.4 The phase machinery — the best thing in Bronze Era

`00_bronze_sea_peoples_crisis.txt` runs a **two-tier** model.

Tier 1, global, on the situation itself. `on_start:36-47` initialises eleven counters
(`sea_peoples_global_phase = 1`, `sea_peoples_global_pressure = 10`,
`sea_peoples_global_famine_pressure = 10`, `sea_peoples_situation_months = 0`, plus seven
statistics counters). `on_monthly:155` does `change_variable = { name = sea_peoples_situation_months add = 1 }`,
then escalates phase on a pure month count (`:157-184`):

```
36 months  -> phase 2
72 months  -> phase 3
120 months -> phase 4
180 months -> phase 5
```

Then a **floor-and-drift** pressure model (`:186-245`), with the design intent written in as a
comment at `:186-187`:

```
		# The displayed situation pressure is global collapse momentum. Local country actions
		# reduce local damage, but they should not let the whole Mediterranean crisis vanish.
```

Each phase sets a minimum pressure (phase 5 → 35, phase 4 → 60, phase 3 → 40, phase 2 → 25, else
10) and the higher phases add drift (`change_variable = { name = sea_peoples_global_pressure add = 1 }`
at `:209, :221, :234`), with hard clamps at 100 (`:246-253`).

Tier 2, per-country. `on_monthly:264-275` propagates the global phase down:

```
			every_country = {
				limit = {
					sea_peoples_crisis_active_country = yes
					sea_peoples_crisis_direct_country = yes
				}
				if = {
					limit = {
						situation:sea_peoples_crisis = { var:sea_peoples_global_phase >= 2 }
						NOT = { sea_peoples_crisis_phase_at_least = { value = 2 } }
					}
					sea_peoples_set_phase = { value = 2 }
```

**The reusable insight:** a long crisis needs a global clock the player cannot stop and a local
state the player *can* affect. Player actions move the local number; the global number has a floor.
That is how you make a 271-year situation that stays threatening without being unwinnable.

`on_monthly` is also **self-healing** — `:110-153` re-initialises every one of the eleven counters
if missing (`if = { limit = { NOT = { has_variable = X } } set_variable = { name = X value = N } }`).
Defensive against save-game upgrades and against `on_start` having been missed. Verbose, but for a
situation that must survive 271 years and mid-campaign mod updates, correct.

`can_end` is duration-based (`:16-21`): `has_variable = sea_peoples_situation_months` and
`var:sea_peoples_situation_months >= 360` — a flat 30 years.

`on_ending` (`:58-89`) removes all eleven per-country variables from every affected country and
sets the global `sea_peoples_crisis_ended` guard that `can_start:13` reads, so it cannot restart.

## B.5 Dead code: `on_end` and `end_conditions`

Measured key census for Bronze Era's five situations, cross-checked against the vanilla
readme (§0.1) and the 22-file vanilla census:

| key | Bronze Era uses | legal? |
|---|---|---|
| `can_start`, `can_end`, `on_start`, `on_monthly`, `monthly_spawn_chance`, `visible`, `tooltip`, `map_color`, `secondary_map_color`, `legend_key`, `hint_tag`, `is_data_map`, `content_trigger`, `on_ending` | — | **yes**, all attested |
| **`on_end`** | 2 | **NO — 0 vanilla uses, absent from readme** |
| **`end_conditions`** | 2 | **NO — 0 vanilla uses, absent from readme** |

Locations:
- `00_bronze_trojan_war_phase_1.txt:22` — `end_conditions` (empty block, harmless)
- `00_bronze_trojan_war_phase_1.txt:26` — `on_end`, containing
  `set_global_variable = { name = "trojan_war_phase_1_ended" value = yes }`
- `00_bronze_trojan_war_phase_2.txt:66` — `end_conditions`, containing **the entire victory
  resolution** (`:66-83`): the `greece_actually_won` check and every
  `trojan_war_greece_victory` / `trojan_war_anatolian_victory` modifier award
- `00_bronze_trojan_war_phase_2.txt:85` — `on_end`, containing all the modifier cleanup and the
  `change_subject_type` reversions (`:85-114`)

If `on_end` and `end_conditions` are not real hooks — and neither the readme nor 22 vanilla files
know them — then **the Trojan War has no victor and never cleans up**: the phase-2 country
modifiers stay on all seven tags permanently, WILUS and SEHA stay
`subject_type:trojan_situation_vassal` forever, and `trojan_war_phase_1_ended` /
`trojan_war_phase_2_ended` are never set, so the `visible` blocks
(`phase_1.txt:40`, `phase_2.txt:126`) never turn off.

Note the mod's own author suspected something: `00_bronze_trojan_war_phase_2.txt:41-43` carries the
comment `# this one dosent trigger in game but when triggered in debugg gives wrong event`, and
`:65` reads `# rework have this logic done some where else then added in on end add contry modifer`.

**Strictly speaking** the engine may accept unknown keys silently (that is the whole silent-failure
thesis) — I cannot execute anything. But by the citation rule these two keys have **no attestation
in any source**, and a block with no attestation is a block that does nothing until proven
otherwise.

Note the phases are chained by **date only** — `phase_2.can_start:8` is `current_date >= 14.1.1`,
and `phase_1.can_end:17` is `current_date >= 14.1.1`. Phase 2 does not check that phase 1 ended. So
the arc survives the dead `on_end` by accident.

## B.6 Localisation — the shadowing bug, measured

Bronze Era ships localisation in **two trees**:
- `localization/english/` and `localization/french/` (root level, 26 files)
- `main_menu/localization/english/`, `.../french/` (the correct tree, 60+ files)

**22 filenames exist in both trees.** Measured by comparing basenames:

```
Bronze_chronology_l_english.yml          Bronze_chronology_l_french.yml
Bronze_country_names_l_english.yml       Bronze_country_names_l_french.yml
Bronze_cultures_l_english.yml            Bronze_cultures_l_french.yml
Bronze_hatti_collapse_l_english.yml      Bronze_hatti_collapse_l_french.yml
Bronze_industry_l_english.yml            Bronze_languages_l_french.yml
Bronze_languages_l_english.yml           Bronze_mycenaean_league_l_french.yml
Bronze_mycenaean_league_l_english.yml    Bronze_palatial_complex_l_french.yml
Bronze_palatial_complex_l_english.yml    Bronze_religions_l_french.yml
Bronze_religions_l_english.yml           Bronze_sea_peoples_crisis_l_french.yml
Bronze_sea_peoples_crisis_l_english.yml  Bronze_static_modifiers_l_french.yml
Bronze_static_modifiers_l_english.yml    zz_bronze_celtic_cultures_l_english.yml
```

This is the exact state CLAUDE.md warns about ("A published total conversion has 20 files in
exactly that state") — **this is that conversion, and the count is now 22.** Among the shadowed
pairs are `Bronze_hatti_collapse`, `Bronze_mycenaean_league` and `Bronze_sea_peoples_crisis`: the
loc for three of the five situations.

Three further loc-tree hygiene problems, all measured:
- `main_menu/localization/english/location_painter_countries_l_english_backup.yml` — a backup with
  a **`.yml` extension**, so it is parsed as live localisation and its keys compete with the real
  file.
- `main_menu/localization/english/location_painter_countries_l_english.yml.bak`,
  `...cultures_l_english.yml.bak`, `...religions_l_english.yml.bak` — these are safe (`.bak` is
  not `.yml`), but they show the working pattern that produced the unsafe one.
- Only **two** event loc files exist under the events subfolder
  (`main_menu/localization/english/events/Bronze_sea_peoples_crisis_l_english.yml` 293 lines,
  `Bronze_trojan_war_phase_1_events_l_english.yml` 20 lines) against 111 events. The rest is
  carried in the top-level files — including the shadowed ones.

Total loc volume is nonetheless large: 12,921 keys under `main_menu/localization/`.

## B.7 Techniques worth stealing — Bronze Era

1. **Write the historical date next to the engine date.**
   `00_bronze_sea_peoples_crisis.txt:10-12`. Cheap, and it makes every date gate reviewable.
2. **Empty `situation_manager` with the reasoning in comments.**
   `main_menu/setup/start/22_situations.txt` (whole file). Nothing forced active; every situation
   earns its start through `can_start`. This is the right default for 1066, where the situations
   are spread over 271 years.
3. **Two-tier pressure: a global clock with a per-phase floor, plus per-country state that player
   actions move.** `00_bronze_sea_peoples_crisis.txt:157-184` (phase ladder on a month counter),
   `:186-245` (floors and drift), `:264-275` (propagation down to countries). The design comment at
   `:186-187` states the principle better than I can paraphrase it.
4. **Self-healing `on_monthly`.** `:110-153` re-initialises every counter if absent. For a situation
   that must survive mid-campaign mod updates across 271 years, this is not paranoia.
5. **Different action `type` for different actor classes.** Victims get `type = situation`
   (`00_bronze_sea_peoples_crisis_actions.txt`, 10 actions); the raiders get `type = owncountry`
   with `player_automated_category = privateers`
   (`00_bronze_sea_peoples_raiding_actions.txt:1-8`).
6. **Name actions as historical decisions.** `bronze_hatti_seize_temple_grain`,
   `bronze_hatti_abandon_syrian_road`, `mycenaean_call_megaron_council`.

## B.8 Mistakes to avoid — Bronze Era

1. **Inventing block names.** `on_end` (`trojan_war_phase_1.txt:26`, `phase_2.txt:85`) and
   `end_conditions` (`phase_1.txt:22`, `phase_2.txt:66`) have zero attestation. Phase 2's entire
   victory resolution and cleanup sit inside them. The correct names are `on_ending` (before the
   status flip) and `on_ended` (after) — and Bronze Era's own other three situations use
   `on_ending` correctly (`sea_peoples_crisis.txt:58`, `hatti_collapse.txt:58`,
   `mycenaean_fragmentation.txt:182`), which makes the Trojan pair a consistency failure inside one
   mod.
2. **Two localisation trees with 22 shadowed filenames**, plus a `_backup.yml` that the parser will
   read. See §B.6.
3. **`add_country_modifier = { name = ... }`** at `trojan_war_phase_2.txt:33-39, :72, :75-80`,
   e.g. `0001G = { add_country_modifier = { name = trojan_war_greece_modifier_phase_2 } }`.
   **Discrepancy, flagged rather than resolved:** the script docs write the parameter as `name`
   (`docs/EU5-Vanilla-Script-Docs/effects.log:108` — `add_country_modifier = { name = name
   days/months/years=x mode = add/extend/replace/add_and_extend <size = x> <desc = string>}`),
   but vanilla writes `modifier =` **1919 times and `name =` 0 times** across
   `in_game/common/situations/` and `in_game/events/` (measured). Rise of Timur also uses
   `modifier =` (`events/DHE/flavor_wrath_of_timur.txt:41`, `:33`). Given CLAUDE.md's
   "existence is not enough — check scope, magnitude and semantics", I would write `modifier =`
   and treat `name =` as **UNVERIFIED**.
4. **Bare tags as scopes.** `trojan_war_phase_2.txt:33-39` writes `0001G = { ... }`,
   `WILUS = { ... }` while `:18` and `:108` in the same file write `c:WILUS = { ... }`. Vanilla
   situations use the `c:` prefix (49 occurrences of `^\s*c:TAG = {` across the 22 files). The bare
   form is unattested. **UNVERIFIED** whether the engine resolves it.
5. **Two situations shipped without map presence.** `trojan_war_phase_1` and `phase_2` have no
   `tooltip`, no `map_color`, no `legend_key`, and phase 2 has no `hint_tag` and no icon file
   (there is `main_menu/gfx/interface/icons/situations/00_bronze_trojan_war_phase_1.dds` but no
   phase-2 equivalent, and no illustration for either). A situation with a GUI panel but no map
   colour is half-built.
6. **Undefined hint tags**, same class as Rise of Timur: `hint_bronze_hatti_collapse`
   (`00_bronze_hatti_collapse.txt:3`), `hint_mycenaean_fragmentation`
   (`00_bronze_mycenaean_fragmentation.txt:3`), `hint_sea_peoples_crisis`
   (`00_bronze_sea_peoples_crisis.txt:3`) — all three checked against
   `VANILLA:in_game/common/scriptable_hints/scripted_hints.txt`, all three UNDEFINED, and the mod
   ships no `scriptable_hints` folder.

---

# C. BASILEIA ROMAION — the single-flagship pattern

## C.1 What is actually there

| thing | count |
|---|---|
| situation files | **1** — `in_game/common/situations/rise_of_the_ottomans.txt` (606 lines) |
| own GUI panels | **0** — the mod ships **no `.gui` files at all** (`find . -name "*.gui"` returns nothing) |
| event files | 14 in `in_game/events/br_events/` (one is `readme.txt`, so 13 with content) |
| **total events** | **126** |
| on_action files | 1 — `in_game/common/on_action/br_startup.txt` |
| situation-side loc | none specific; `hint_tag` reuses vanilla's |
| **total English loc keys** | **6,054** |

The one situation is **not new**. It is a modification of vanilla's `rise_of_the_ottomans`, and the
verdict on the "single flagship" framing is: **Basileia barely does situations at all.** Its craft
budget went into events and localisation.

Per-file event counts: `br_ere_resistance_events.txt` 57, `br_ERE_events.txt` 29,
`br_latin_wars.txt` 16, `br_country_startup.txt` 7, `northern_trade.txt` 4, `br_hangzhou.txt` 3,
`br_elysium.txt` 2, `br_indikes_events.txt` 2, `southern_trade.txt` 2, `br_startup.txt` 1,
`br_hre.txt` 1, `br_ere_subjugation.txt` 1, `br_ere_succession_crisis.txt` 1.

## C.2 The override technique — `REPLACE_OR_CREATE:`

`in_game/common/situations/rise_of_the_ottomans.txt:1`:

```
REPLACE_OR_CREATE:rise_of_the_ottomans = {
```

This is a **database-entry directive**, and it is the most transferable thing in this mod. Usage
across Basileia (measured): **246 `REPLACE_OR_CREATE:` and 57 `TRY_INJECT:`**, spanning 30+ files
including `in_game/common/cultures/00_br_overrides.txt`,
`in_game/common/building_types/br_buildings_injects.txt` vs `br_buildings_replaced.txt` (the
naming convention itself encodes which directive is used), `in_game/setup/countries/br_anatolia.txt`,
and `in_game/common/scripted_effects/br_scripted_effects.txt`.

Vanilla itself uses these zero times (measured: 0 files under the game tree contain
`REPLACE_OR_CREATE`). They are mod-only. The documented ordering, from
`C:\Users\Desktop\eu5-modding-project-1.3.11\eu5-modding-project-1.3.11\docs\technical\EU5_Modding_Knowledge_Base.md:118`:

```
INJECT_OR_CREATE -> REPLACE_OR_CREATE -> TRY_INJECT -> TRY_REPLACE -> INJECT -> REPLACE
```

and `:121`: *"Filename order resolves conflicts only between entries using the same operation type.
A later-named `REPLACE_OR_CREATE:` cannot beat an earlier-named `REPLACE:`, because all `REPLACE:`
operations are processed later."* And `:123`: *"These keywords work only on top-level objects…
Support for these keywords is database-type dependent and must be verified for the target folder."*

Rise of Timur uses the family too — `in_game/common/generic_actions/rto_action_reworks.txt:1`
is `TRY_REPLACE:press_claims = {`, and
`main_menu/common/static_modifiers/wrath_of_timur_modifiers.txt:8` is
`INJECT:timmy_wants_to_play = {`. So two of the three mods independently reached for this, which is
a decent signal it works.

**Caveat worth recording:** Basileia's file sits at the *same path and filename* as vanilla's
(`in_game/common/situations/rise_of_the_ottomans.txt`), which by normal Paradox file resolution
already shadows the vanilla file wholesale. Whether `REPLACE_OR_CREATE:` is doing anything at all
in that position, or is redundant belt-and-braces, is **UNVERIFIED** — the knowledge base's own
warning that support "must be verified for the target folder" applies. The safe reading: use the
directive **from a differently-named file** so the vanilla file still loads.

## C.3 What Basileia actually changed in the situation

Normalised diff (BOM and CRLF stripped) against
`VANILLA:in_game/common/situations/rise_of_the_ottomans.txt` — 152 diff lines, four substantive
changes:

1. **`content_trigger` deleted.** Vanilla `:5-9` has
   `content_trigger = { OR = { tag = TUR } }`; Basileia's file has no `content_trigger` at all
   (confirmed against the Bronze/vanilla key census — Basileia's file jumps from `hint_tag` at `:3`
   to `can_start` at `:5`).
2. **Scoring metric swapped**, six sites: `country_tax_base` → `monthly_income_trade_and_tax`
   in the three `ordered_in_global_list` `order_by` blocks and their three matching
   `_total_score_variable` computations. Both identifiers verified real:
   `docs/EU5-Vanilla-Script-Docs/triggers.log:3275` (`country_tax_base`) and
   `:8506` (`monthly_income_trade_and_tax`), the latter also used across vanilla
   (`in_game/common/auto_modifiers/country.txt`, `country_interactions/demand_silver_tribute.txt`,
   and others).
3. **`ai_force_annexation` moved from `c:TUR` to every beylik.** Vanilla `:47-54` applies it in a
   `c:TUR = { ... }` block; Basileia folds it into the `every_country = { limit = { has_reform =
   government_reform:anatolian_beylik } ... }` loop so **all** eligible beyliks get it
   (`in_game/common/situations/rise_of_the_ottomans.txt:33-42`). Sensible for a mod where the
   Ottomans are not guaranteed to be the winner.
4. **`visible` geography changed**, `:25-26`:
   ```
			has_presence_in = region:crescent_region
			has_presence_in = region:persia_region
   ```
   where vanilla has `region:balkan_region` and `region:anatolia_region`. The same swap is repeated
   in the `on_start` capital filter (vanilla `:154-155` → Basileia `:145-146`).

   Both `crescent_region` and `persia_region` are real
   (`VANILLA:in_game/map_data/definitions.txt:2134` and `:2309`), and Basileia ships **no
   `in_game/map_data/`**, so it is not renaming regions. **This looks like a bug**, and a
   consequential one: a Byzantine overhaul has just made the Ottoman situation invisible to
   everyone in the Balkans and Anatolia — including Byzantium — while showing it to Persia. It is
   flagged as **suspect, not confirmed**, because the `visible` block is an `OR` whose first branch
   (`is_neighbor_of` / `is_rival_of` / `is_enemy_of` / `is_subject_or_below_of` the strongest
   beylik, `:16-24`) will still catch most Anatolian and Balkan neighbours once
   `strongest_beylik_variable` is set. The damage is therefore partial: the situation is invisible
   to non-neighbours who should see it, and visible to Persians who should not.

5. `on_ending` restructured (vanilla `:297-330` → Basileia `:287-...`): vanilla's
   `if / else_if` chain becomes a single `if` with a three-branch `OR`, adding a clause requiring
   `any_in_global_list = { variable = eligible_beylik_list  is_subject = no  num_locations >= 100 }`.
   A tidy-up rather than a redesign.

## C.4 The seeding file — identical to vanilla

`main_menu/setup/start/22_situations.txt` is a **byte-for-byte match** for
`VANILLA:main_menu/setup/start/22_situations.txt` (I diffed them; no differences). Both contain:

```
situation_manager={
	rise_of_the_ottomans={
	#	status=active
	...
	}
	# guelphs_and_ghibellines = { ... }
}
```

— an entry with `status=active` **commented out**, and the whole `guelphs_and_ghibellines` block
commented out. So the situation is registered but not forced active; it starts through
`can_start:5-8` (`current_date > 1337.4.1`, `current_date < 1350`).

**This is a shipped no-op file.** Basileia gains nothing by overriding it, and pays the cost that
any future vanilla patch to this file is silently discarded. For 1066 the lesson is: if the
override is identical, do not ship it.

## C.5 How 126 events are driven without situations

Measured firing mechanisms across `in_game/events/`:

| mechanism | count |
|---|---|
| `type = country_event` | 125 |
| `fire_only_once` | 75 |
| `dynamic_historical_event` | 50 |
| `trigger_event_silently` | 29 |
| `trigger_event_non_silently` | 23 |
| `hidden = yes` | **1** |
| `category = disaster_event` | 1 |
| `category = situation_event` | **0** |

The profile is the opposite of Rise of Timur's. **Almost nothing is hidden** (1 of 126), so nearly
every event is something the player reads. Not one event is tagged `category = situation_event`.
The engine driver is `dynamic_historical_event` — 50 dated windows — plus a single
`on_game_start` hook.

That hook, `in_game/common/on_action/br_startup.txt:1-5`, is the whole on_action budget:

```
on_game_start = {
    on_actions = {
        br_on_game_start
    }
}
```

and `br_on_game_start` (`:7-...`) is a flat list of per-tag kickoffs —
`c:E1Y ?= { trigger_event_silently = br_startup.1 }`, `c:LOT ?=`, `c:SAR ?=`, `c:S1C ?=`,
`c:B0L ?=`, `c:BNK ?=`, `c:K1K ?=` and more, each with `?=` so a missing tag is not an error.
Preceded by an `every_country` block (`:9-26`) that gives every holder of
`special_status:defiant_strategoi` in `international_organization:roman_world` an
`ai_personality:ai_defensive` and two opinion modifiers against `c:BYZ`.

**The pattern:** instead of a situation with `on_monthly`, Basileia sets initial conditions once at
game start and then lets 50 dated event windows carry the century. Cheaper to build, and it
produces a lot of readable content — but there is no map layer, no phase state, and no player
agency loop beyond event options.

## C.6 Flavour density and loc craft

`in_game/events/br_events/br_ere_resistance_events.txt:5-22` is representative:

```
br_ere_resistance_events.1 = {
	hide_portraits = yes
	type = country_event
	title = br_ere_resistance_events.1.title
	desc = br_ere_resistance_events.1.desc
	outcome = neutral
	image = "gfx/interface/illustrations/situation/rise_of_the_ottomans.dds"
	fire_only_once = yes
	major = yes
	dynamic_historical_event = {
		tag = PAP
		from = 1356.1.1
		to = 1800.1.1
		monthly_chance = 10
	}
```

Note `major = yes` (broadcasts a notification to other countries), an explicit `image` reusing a
**situation illustration** for an event, and a 444-year window at `monthly_chance = 10`.

Loc volume is where this mod is genuinely strong: **6,054 English keys**, in 18 top-level files plus
an `events/` subfolder (7 files) and a `replace/` subfolder. Event-loc key counts:
`br_ere_resistance_events_l_english.yml` 224, `br_ere_events_l_english.yml` 142,
`br_latin_wars_events_l_english.yml` 65, `br_other_events_l_english.yml` 28,
`br_northern_trade_events_l_english.yml` 22, `br_hangzhou_events_l_english.yml` 13,
`br_elysium_events_l_english.yml` 4.

Ratio check: 224 keys for 57 events ≈ 3.9 keys/event — consistent with title + desc + ~2 options
each, i.e. **the loc is essentially complete for its largest event file.** Contrast Bronze Era,
where 111 events are served by 2 dedicated event-loc files.

Basileia's loc tree is also **single** — everything under `main_menu/localization/english/`, no
root-level `localization/` directory. No shadowing.

## C.7 A shipped modding reference — `br_events/readme.txt`

Worth flagging as an artefact rather than a technique: `in_game/events/br_events/readme.txt` is a
116-line commented **event schema reference** the mod ships in its own source tree. It documents
fields that are otherwise easy to get wrong, e.g. `:70`:

```
#	orphan = yes		# The game will not log an error about this event being unreferenced. Useful for debug events
```

which is directly relevant to the CLAUDE.md note about the engine's orphan-detection blind spot,
and `:73`:

```
#	category = disaster_event/situation_event/international_organization_event			# Determines what icon the event should have. Does NOT show any icon when it is a generic_event which is the default
```

which is the enum for event `category` — one of the FORBIDDEN-from-memory categories, now attested.
It also documents `interface_lock = no` (`:63`), `exclusive = yes` (`:93`),
`original_recipient_only = yes` (`:94`), and marks `moral_option` / `evil_option` /
`high_risk_option` / `high_reward_option` as `# ???` (`:95-98`) — i.e. the mod author did not know
what they do either.

Vanilla ships the same readme (`VANILLA:in_game/common/situations/readme.txt` is its situation-side
sibling), so this is a copied vanilla file, not original documentation. **Recommendation: read the
vanilla `readme.txt` in every `common/` and `events/` folder before writing in it.** Both Bronze
Era and Basileia carry copies; neither project's mistakes suggest they read them closely.

## C.8 Techniques worth stealing — Basileia

1. **`REPLACE_OR_CREATE:` / `TRY_INJECT:` for surgical vanilla edits instead of whole-file
   overrides.** `in_game/common/situations/rise_of_the_ottomans.txt:1`, and 246 + 57 uses
   mod-wide. With the ordering caveat from
   `eu5-modding-project-1.3.11/docs/technical/EU5_Modding_Knowledge_Base.md:118-123`, and the
   recommendation to place them in a **differently-named** file.
2. **Filename-encoded intent.** `br_buildings_injects.txt` vs `br_buildings_replaced.txt` — the
   directive used is visible from the file list. Cheap, and it makes an override audit trivial.
3. **One `on_game_start` hook with `?=` on every tag.** `on_action/br_startup.txt:28-50`. Every
   per-country kickoff is `c:TAG ?= { trigger_event_silently = X }`, so a tag that does not exist
   in this campaign is skipped rather than erroring. For a 1066 map with 180 landless shells this
   is the right idiom.
4. **Loc completeness as a countable invariant.** 224 keys / 57 events ≈ 3.9. That ratio is a
   harness check waiting to be written: count event definitions, count loc keys, flag any file
   whose ratio collapses.
5. **`major = yes` + an explicit `image` reusing situation illustration art.**
   `br_ere_resistance_events.txt:11, :14`. Free production value — situation illustrations already
   exist and are the right size.

## C.9 Mistakes to avoid — Basileia

1. **Shipping an override identical to vanilla.** `main_menu/setup/start/22_situations.txt` is
   byte-identical to `VANILLA:main_menu/setup/start/22_situations.txt`. Pure liability: it
   discards future vanilla changes to that file and buys nothing.
2. **Silently dropping a block during a whole-entry replace.** Vanilla's
   `content_trigger = { OR = { tag = TUR } }`
   (`VANILLA:in_game/common/situations/rise_of_the_ottomans.txt:5-9`) is absent from Basileia's
   version. Whether deliberate or lost in a copy, this is exactly the
   "a whole-file override deletes everything it does not repeat, with no error" failure. When
   using `REPLACE_OR_CREATE:` on a vanilla entry, diff the result against vanilla and account for
   every removed line.
3. **The `crescent_region` / `persia_region` swap** in `visible` (`:25-26`) and the `on_start`
   capital filter (`:145-146`). Suspect — see §C.3.4. Real identifiers, wrong-looking semantics;
   the sort of change that produces no error and a situation nobody can see.

---

# 4. COMPARISON TABLE

| | **Rise of Timur** | **Bronze Era** | **Basileia Romaion** |
|---|---|---|---|
| **# situations (own)** | 4 | 5 | **1** (a modified vanilla entry) |
| **vanilla situations ridden** | 2 (`rise_of_timur`, `rise_of_the_ottomans`) | 0 | 1 (the same file it edits) |
| **# events** | **143** (13 files) | 111 (10 files) | 126 (13 files + readme) |
| **phases?** | no explicit phase var; **arc = 4 dated invasion waves** + chained situations via winner variable (`wot_turkish_expansion.txt:5-11`) | **yes — best in class.** 5-phase ladder on a month counter, global + per-country tiers (`00_bronze_sea_peoples_crisis.txt:157-275`) | **no** |
| **actions?** | **19** `type = situation` (8 in `rise_of_persia.txt`) + `generic_action_ai_lists` wiring | **36** `type = situation` + 1 `type = owncountry`; **no `generic_action_ai_lists` for the bronze actions** (its lists are `D008_*`/religion lists) | 0 situation actions (2 files: `br_colonial_charters.txt`, `br_io_actions.txt`, neither situation-typed) |
| **own GUI panels?** | **yes — 4** (134-321 lines) | **yes — 5** (96-351 lines) | **no — zero `.gui` files in the mod** |
| **own icons / illustrations?** | 4 icons + 4 illustrations | 4 icons + 4 illustrations (phase 2 has neither) | none |
| **seeding at start?** | **no** — no `22_situations.txt` at all; all via `can_start` | **no** — empty `situation_manager` with documented reasoning | **no** — file present but byte-identical to vanilla (a no-op) |
| **date handling** | real dates, 1360-1600 | **offset from `START_DATE = "1.1.1"`**, with historical dates in comments | real dates, 1337-1800 |
| **AI/player split** | **strongest** — `is_ai = yes` on every railroad effect for TIM; subjugation offered as a 3-option event to both | weak — actions are open to all, no `is_ai` gating found in the situations | n/a (no railroad) |
| **failsafes** | **strongest** — every end trigger has a date backstop; `?=` on all protagonist access; `on_ended` cleanup | good in 3 of 5; **Trojan pair's cleanup is in unattested `on_end`/`end_conditions`** | minimal |
| **loc completeness** | good — `wot_situations_l_english.yml` covers every action name+desc, all 8 map/legend tooltips, the end-trigger string; 4 event-loc files under `events/` | **large but broken — 12,921 keys, 22 filenames shadowed across two loc trees**, plus a live `_backup.yml`; only 2 event-loc files for 111 events | **best — 6,054 keys, one tree, no shadowing, ≈3.9 keys/event** |
| **hint tags** | 3 declared, **3 undefined**, 1 copy-pasted wrong | 3 declared, **3 undefined** | reuses vanilla's `hint_rise_of_the_ottomans` — **the only one that resolves** |
| **override technique** | `TRY_REPLACE:`, `INJECT:` (2 uses) | plain file overrides | **`REPLACE_OR_CREATE:` ×246, `TRY_INJECT:` ×57** |
| **one-line verdict** | **The railroad reference.** Copy its AI/player split, its rubber band, its immortality modifier and its chaining — but not its dangling hints or its ungated non-Timur rubber bands. | **The phase-machine reference**, and the cautionary tale on loc trees and invented block names. Steal the pressure model; audit every block name against the vanilla readme. | **The loc and override reference.** Proof that 126 well-localised events buy a lot of mod — but it does not teach situations, because it barely writes one. |

---

# 5. What this means for 1066 — synthesis for the main session

**The situation core** should follow vanilla + Bronze Era's `sea_peoples_crisis`:
`can_start`/`can_end`/`on_start`/`on_monthly`/`on_ending`/`on_ended`, a phase variable escalated on
a month counter, a global pressure with per-phase floors, and per-country state that actions move.
Manzikert's 271-year successor arc needs exactly that shape.

**The railroad layer** should follow Rise of Timur: `is_ai`-gated dated waves, a monthly top-up
on_action, the border rubber band against a `scripted_geography`, a per-arc game rule with a
disable option, and the conqueror kept alive by a timed `is_immortal = yes` character modifier.
The Timurid subjugation event (`flavor_wrath_of_timur.txt:135-233`) is the model for offering the
railroad to a player.

**Chaining across 271 years** should follow `wot_turkish_expansion.txt:5-11` — successor situations
gated on `NOT = { is_situation_active = <predecessor> }` plus a winner variable the predecessor
left on a country, with the protagonist addressed as `situation:X.var:actor` rather than a tag.

**Four checks the harness does not yet have**, each provable against a known positive in these
trees:
1. every `hint_tag` resolves to an entry in a `scriptable_hints` file (3 mods, 6 failures)
2. every situation top-level key is in the vanilla `readme.txt` whitelist (Bronze Era, 4 failures)
3. no two loc files share a basename across trees (Bronze Era, 22 failures)
4. every `type = situation` action appears in some `generic_action_ai_lists` `actions = { }` block

**Two things to verify in game before relying on them**, both marked UNVERIFIED above:
`add_country_modifier` parameter name (`modifier` vs `name`), and whether
`create_country_from_location` needs the third leg of the vanilla triple
(`change_integration_level = core`).
