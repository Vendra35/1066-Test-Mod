# CRAFT ANATOMY OF EVERY VANILLA EU5 SITUATION

Source tree (read-only): `E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
All paths below are **relative to that root** unless stated otherwise.
Every claim carries a `file:line`. Nothing here is from memory.

Corpus read end to end:
- `in_game/common/situations/` — 22 situations + `readme.txt` (9,171 lines total)
- `in_game/common/generic_actions/` — 22 files declaring **155** `type = situation` actions
- `in_game/common/resolutions/` — 4 situation-bound resolutions + `readme.txt`
- `in_game/common/scripted_triggers/situation_triggers.txt` (1,050 lines) — every `can_end`
- `in_game/common/scripted_effects/situation_effects.txt` (1,224 lines) — shared machinery
- `main_menu/setup/start/22_situations.txt` — seeding
- `in_game/events/situations/` — 25 files, **473 events**, 34,297 lines
- `in_game/gui/panels/situation/` — 24 bespoke `.gui` panels
- supporting: `main_menu/common/script_values/default_values.txt`, `main_menu/common/static_modifiers/`,
  `in_game/common/prices/00_hardcoded.txt`, `main_menu/common/named_colors/02_map.txt`,
  `in_game/common/on_action/_hardcoded.txt`, `in_game/common/scriptable_hints/scripted_hints.txt`

---

## 0. THE DECLARED FORMAT — and how much of it the readme omits

`in_game/common/situations/readme.txt:1-18` documents exactly 14 keys:
`custom_description`, `monthly_spawn_chance`, `international_organization_type`, `resolution`,
`voters`, `can_start`, `can_end`, `visible`, `on_start`, `on_monthly`, `on_ending`, `on_ended`,
`tooltip`, `map_color`, `secondary_map_color`.

A depth-1 field scan of all 22 files finds these **five undocumented keys actually shipping**:

| Key | Users | Evidence |
|---|---|---|
| `hint_tag` | **all 22** | e.g. `situations/black_death.txt:4` → resolves to `in_game/common/scriptable_hints/scripted_hints.txt:691` `hint_black_death = { priority = { can_see_situation = situation:black_death } hide = { NOT = { is_situation_active = situation:black_death } } sort_priority = 200 }`. Engine-side: `Situation.GetHintTag` / `Situation.HasHint` (`docs/EU5-Vanilla-Script-Docs/data_types/data_types_uncategorized.txt:117975,118011`) |
| `legend_key` | 20 of 22 (all but `colonial_revolution`, and `sengoku` has 1) | `situations/fall_of_delhi.txt:382-411` (6 keys) |
| `is_data_map` | **2** — `black_death.txt:216`, `great_pestilence.txt:144` | nowhere else in the entire game |
| `content_trigger` | **1** — `rise_of_the_ottomans.txt:5-9` | the ONLY occurrence in the whole tree; matches engine `Situation.GetContentPriority` (`data_types_uncategorized.txt:117957`) |
| *(documented but near-unused)* `custom_description` | **1** — `treaty_of_tordesillas.txt:5` `custom_description = GetTreatyOfToredesillasDesc` | — |

**Root/scope contract** (readme.txt:9-18), which is what makes situations awkward to write:
- `can_start`, `can_end`, `on_start`, `on_monthly`, `on_ending`, `on_ended` → **root = the situation**
- `visible` → **root = country**, `scope:target` = situation
- `tooltip`, `map_color`, `secondary_map_color` → **root = location**, `scope:target` = situation

That root swap is the single biggest source of idiom churn: inside `map_color` you write
`scope:target.var:x` (`treaty_of_tordesillas.txt:380`), inside `on_monthly` you write plain `var:x`
(`treaty_of_tordesillas.txt:137`), and inside `tooltip` vanilla mixes both —
`situation:treaty_of_tordesillas.var:var_treaty_phase` (`:224`) next to
`scope:target.var:var_line_location` (`:228`).

**Situation-scope API** (from the authority, `docs/EU5-Vanilla-Script-Docs/`):
- triggers with `**Supported Scopes**: situation` — `days_since_situation_end`, `days_since_situation_start`,
  `years_since_situation_end`, `years_since_situation_start`, `situation_is_active`, `situation_has_ended`,
  plus the resolution family (`any_active_resolution`, `has_active_resolution`, `has_voted`, `has_voted_for`,
  `has_cached_or_cast_vote_for`, `resolution_is_active`, `vote_is_locked`, `votes_for_resolution`)
  (`triggers.log:3539-3549, 10272-10278, 223-226, 4301-4304, 4504-4506, 5623-5630, 10096-10099`)
- triggers taking a situation as **target**: `can_see_situation`, `is_situation_active` (`triggers.log:2922-2927, 7604-7608`)
- effects with situation scope: `set_vote`, `remove_vote`, `end_vote`, `finalize_resolution`,
  `every/ordered/random_active_resolution` (`effects.log`, scope-filtered)
- the only two situation-lifecycle effects: `activate_situation` (`effects.log:12`), `end_situation` (`effects.log:1535`)
- scope link `situation` → `Output Scopes: situation` (`event_targets.log:580-584`)

---

## 1. MASTER TABLE

`msc` = `monthly_spawn_chance`. Values from `main_menu/common/script_values/default_values.txt:1205-1212`:
`very_low 0.01 · low 0.02 · medium 0.03 · high 0.04 · very_high 0.05 · ultimate 0.1 · ultimate_high 0.5 · unique 1`.
Age start years: age_2 1342, age_3 1437, age_4 1537, age_5 1637, age_6 1737 (`in_game/common/age/00_default.txt:51,109,168,231,307`).

| key | `can_start` gates | msc | phases? | actions | resolution / voters | map fields | how it ENDS | approx lifespan |
|---|---|---|---|---|---|---|---|---|
| **black_death** | `disease_is_active = disease:bubonic_plague` (`:7`) | unique 1.0 | no — per-country bool `had_black_death` (`:73`); `var:original_outbreak` set from **outside** | 18 (9 do/undo pairs) | — | map_color `lerp` on outbreak presence (`:226-230`), **`is_data_map = yes`** (`:216`), 1 legend | `NOT = { disease_outbreak_is_active = var:original_outbreak }` (`:11`) | as long as the outbreak lives |
| **colonial_revolution** | `current_age = age_6_revolutions` + a disloyal enlightened colony (`:5-16`) | very_low 0.01 | no | 8 | — | map_color only, **0 legend_key** | **`can_end = { always = no }`** (`:17-19`); `on_ended = { }` empty (`:132-134`) | never ends |
| **columbian_exchange** | `current_age = age_5_absolutism` + an American pop-bearing loc owned from the Old World (`:5-16`) | unique 1.0 | no — per-country bool `is_in_columbian_exchange` | 4 | — | map_color, 2 legends | `columbian_exchange_end_trigger` = `current_age_or_later = { age = age_6_revolutions }` (`situation_triggers.txt:717-719`) | 1637→1737, ~100y |
| **council_of_trent** | reformation on + `current_year >= 1530` + catholic `reform_desire >= 0.25`, **or a hard 1545-1563 historical fallback** (`:6-24`) | ultimate 0.1 | **YES** — `council_of_trent_passed_debates` / `_failed_debates` vs `_max = 5` (`:40-43`) | 0 dedicated | `international_organization_type = catholic_church` (`:4`) + `voters = council_of_trent_voters` (`:5`), **no `resolution` key** — rides `resolution:policy_vote` | map_color, 2 legends | 5 passed OR 5 failed OR age_5 (`situation_triggers.txt:653-669`) | short — 5 debates |
| **fall_of_delhi** | `country_exists = c:DLH` + `c:DLH = { has_variable = starts_fall_of_delhi_variable }` (`:7-13`) | **low 0.02** | no — outcome booleans | 5 | `resolution = "fall_of_delhi_resolution"` (`:4`) + `voters = fall_of_delhi_voters` (`:5`) | map_color, **6 legends** | `fall_of_delhi_end_trigger`: the resolution sets `delhi_share_of_power` or `opposition_share_of_power`, or DLH cedes/dissolves/dies (`situation_triggers.txt:740-762`) | short — one vote |
| **golden_age_of_piracy** | age_5+ and `any_american_colonial_country = { count >= 5 }` (`:5-10`) | unique 1.0 | no — `strongest_pirate_variable` re-elected monthly | 5 | — | map_color literal `black/red/green/blue`, 4 legends | no independent pirate country **and** >30y, or flat >50y (`situation_triggers.txt:764-777`) | 30-50y |
| **great_pestilence** | `disease_is_active = disease:great_pestilence` (`:7-9`) | unique 1.0 | **YES (3 booleans)** — `var_carib_was_infected` / `var_mesoamerica_was_infected` / `var_andes_was_infected` (`:53-55`) | 10 | — | map_color `lerp`, **`is_data_map = yes`** (`:144`), 1 legend | all 3 regions infected **and** disease dead **and** ≤30 untouched American countries (`:11-35`) | decades |
| **guelphs_and_ghibellines** | `game_is_initialized = yes` + `current_date > 1337.4.1` (`:6-9`) — i.e. **starts immediately** | unique 1.0 | **YES** — `guelphs_progress` / `ghibellines_progress` accumulate a monthly tax-share (`:158-262`), target 1.0 | 7 | `voters = guelphs_and_ghibellines_voters` (`:2`), **no `resolution` key** | map_color 5-branch, 4 legends | either progress ≥1 while the other <1, or age_3 stalemate (`situation_triggers.txt:671-715`) | 1337 → ≤1437, ~100y |
| **hundred_years_war** | FRA+ENG exist, `current_date > 1337.5.1`, both crowned, Robert of Artois settled (`:5-29`) — **plus** `activate_situation` on any ENG↔FRA war declaration (`on_action/_hardcoded.txt:2059-2074`) | unique 1.0 | no | **12** | — | map_color + **`secondary_map_color`** (`:382-427`), 2 legends | `hundred_years_war_unified_requirements`: age_4, or one country gone, or ENG <4 French locs & FRA >230, or ENG union/>175 locs, or vassalage (`situation_triggers.txt:70-122`); also `end_situation` from `events/DHE/flavor_ENG.txt:291` | 1337 → ≤1537, ~116y historical |
| **hussite_wars** | `c:BOH = { is_subject = no religion = religion:hussite }` (`:5-10`) | unique 1.0 | **YES (counters)** — `heretics_eradicated_variable` / `heretics_converted_variable` (`:42-50`) | 9 | — | map_color, secondary_map_color, **1 legend with a `limit` block** (`:302-313`) | BOH catholic/gone/subject, or **>30y at peace still heretic**, or no/hussite emperor (`situation_triggers.txt:124-146`) | ≤30y |
| **italian_wars** | `NOT = { is_situation_active = situation:guelphs_and_ghibellines }` + `current_year > 1450` + (year>1495 or a GP fighting an Italian leader) (`:5-15`) | unique 1.0 | **YES** — `iw_tension` 0-100, clamped, with a point-of-no-return at 100 (`:404-470`) | 8 | — | map_color, secondary_map_color, **8 legends** | `>50y` **AND** (a league ≥200 locations, or every league <1 location after 1y, or `>50y` again) (`:17-70`) | effectively exactly 50y |
| **little_ice_age** | `current_year >= 1645` (`:5-7`) | unique 1.0 | no | 3 | — | map_color from define colors, 3 legends | `little_ice_age_end_trigger = { current_year > 1715 }` (`situation_triggers.txt:434-436`) | **exactly 70y** |
| **nanbokuchou** | `current_date > 1336.1.1` + shogunate has >1 emperor (`:7-12`) | unique 1.0 | no — three **global variable lists** as sides | 2 | `resolution = "nanbokuchou_resolution"` (`:3`) + `voters = nanbokuchou_voters` (`:4`) | map_color, secondary_map_color (marks the human player white, `:522-532`), 4 legends | ≤1 emperor, or both courts share a ruler (`situation_triggers.txt:206-220`); also `end_situation` from `peace_treaties/nanbokuchou_force_imperial_abdication.txt:64` and `events/situations/nanbokuchou.txt:646` | anti-stalemate event fires at `years_since_situation_start > 55` (`:239`) — historical 56y |
| **red_turban_rebellions** | age_2 + `current_year > 1350` + CHI monarchy at peace with low stability/legitimacy/estates, or the arrested-leader flag (`:4-27`) | unique 1.0 | **YES** — per-country `rtr_yuan_allegiance` clamped −100..+100 (`scripted_effects/situation_effects.txt:91-124`) + `rtr_historical_countries_to_release` | 10 | — | map_color 5-branch, 5 legends | `>20y` **AND** (no Middle Kingdom, or age_3, or rebels hold ≥65%, or CHI legitimacy ≥90 & stability ≥30 & celestial 50) (`situation_triggers.txt:354-394`) | ≥20y |
| **reformation** | `current_year >= 1510` (`:4-6`) — **one line** | **high 0.04** | no — preacher counters only | 3 | — | map_color by dominant religion, secondary_map_color for ≥5% minorities, **7 legends** | Council of Trent **and** War of Religions both ended, or `current_year >= 1700` (`situation_triggers.txt:637-651`) | ≤190y |
| **rise_of_the_ottomans** | `current_date > 1337.4.1` and `< 1350` (`:11-14`) | unique 1.0 | **YES (ranking)** — `strongest_beylik_variable` + 2nd + 3rd, each with a score variable, **recomputed every month** (`:170`) | 8 | — | map_color, secondary_map_color, **6 legends**, `content_trigger` (`:5-9`) | year>1565, or no beyliks left, or strongest has >500 locs & ≥50 non-rural & independent, or (after 1400) strongest <100 locs at peace (`situation_triggers.txt:560-608`) | 1337→1565, ≤228y |
| **rise_of_timur** | `has_enabled_situation_trigger = { type = rise_of_timur }` + `c:TIM` exists + `global_var:timur_character` alive (`:4-9`); activated by `events/DHE/flavor_tim.txt:653` | unique 1.0 | **YES (counters + cooldowns)** — `timur_battle_kill_counter`, `timur_total_kill_counter`, and two self-incrementing event cooldowns reset at 10 and 20 months (`:69-73, 131-133`) | 5 | — | map_color, secondary_map_color painting the **declared ambition region purple** (`:354-362`), 5 legends | stagnation (successor `total_abilities < 150`, or no ruler and no heir), or subjugation, or Mughals/Mongol-Empire formable reached (`situation_triggers.txt:508-558`) | one man's life |
| **sengoku** | `current_year >= 1400` + shogunate leaderless / `government_power <= 50` / `stability <= 20` / civil war / rebels >0.9 / ≥6 member wars (`:5-31`) | **ultimate_high 0.5** | **YES (ranking ×5)** — `sengoku_threatening_daimyo` .. `_fifth_`, recomputed monthly (`:261`) | 10 | — | map_color, **1 legend with `limit`**, **NO `tooltip` block at all** (only situation missing one) | shogunate <2 members, or only shogun+emperor, or every clan reined in to <3 buildings (`situation_triggers.txt:266-322`) | open-ended |
| **the_revolution** | `current_age = age_6_revolutions` + `any_great_power = { is_revolutionary = yes }` (`:5-10`) | unique 1.0 | no | 7 | — | map_color, secondary_map_color for the target's subjects, 5 legends | no revolutionary great power and no revolutionary still in the disaster (`situation_triggers.txt:721-738`) | open-ended |
| **treaty_of_tordesillas** | **`always = no`** (`:8-11`), `monthly_spawn_chance = 0` (`:2`) — activated only by `events/situations/treaty_of_tordesillas.txt:325` | 0 | **YES — the clearest phase machine in the game.** `var_treaty_phase` 1.0→2.0, `var_treaty_progress` 0→100→decay, `var_treaty_subtract` recomputed monthly (`:41-184`) | **12 (most of any situation)** | — | map_color, secondary_map_color with **`lerp` to the default colour at factor 0.40** (`:383-405`), 2 legends **with `limit` blocks** | `var_treaty_phase = 2.0` **and** `var_treaty_progress <= 0.0` (`:13-20`); also `end_situation` at `on_action/_hardcoded.txt:855` and `:3940` | phase 1 = 200 months at +0.5/mo ≈ 16.7y; phase 2 decays at ≥0.1/mo ≈ 80y+ |
| **war_of_religions** | `current_year >= 1590` + CoT ended + reformation on + a live catholic-vs-protestant war + an HRE holding both faiths (`:4-28`) | ultimate 0.1 | **YES** — `war_of_religions_total_war_participants_counter`, `_peace_demands_counter`, `_peace_demands_ratio` (`:38-40, 102-164`) | 5 | — | map_color 7-branch, **7 legends** | `war_of_religions_end_trigger` is **deliberately `always = no`** in both display branches (`situation_triggers.txt:610-635`); it ends only via `end_situation` from `peace_treaties/religious_supremacy.txt:53` or `events/situations/war_of_religions.txt:1827` | until a peace is signed |
| **western_schism** | `1360.1.1 < current_date < 1402.1.1` + PAP with `regency_type:papal_election_regency` and cardinals (`:7-16`) | **ultimate_high 0.5** | **YES** — `western_schism_pope_score`, `_anti_pope_score`, `_vote_counter`, `_cardinal_weight_bonus` (the last ticks +1 every month, `:191`) | 3 | `resolution = "western_schism_resolution"` (`:4`) + `international_organization_type = catholic_church` (`:5`), **no `voters` key** — eligibility comes from curia special status (`resolutions/western_schism.txt:12-25`) | map_color, 3 legends | no church/PAP/cardinals, or a score ≥2 **and** `western_schism_ended_by_event` set (`situation_triggers.txt:1021-1050`) | 1378-1417 historical |

### Headline numbers
- **22** situations; **9,171** lines of situation script; **473** events across **34,297** lines; **155** situation actions; **24** bespoke GUI panels; **1,029** English loc lines (`main_menu/localization/english/situations_l_english.yml`).
- `monthly_spawn_chance` distribution: **unique (1.0) ×14**, ultimate_high (0.5) ×3, ultimate (0.1) ×2, high ×1, low ×1, very_low ×1, literal `0` ×1.
- **9 of 22 use no phase variable at all.** The other 13 do it entirely by hand with `set_variable`/`change_variable`.
- **Only 4** declare a `resolution`; **4** declare `voters`; **3** declare `international_organization_type` — and the three sets do not coincide.
- **20 of 22** ship `legend_key` blocks (range 1-8, median 4). **Only 2** set `is_data_map`.
- **9 of 22** ship `secondary_map_color`.
- **Only 1** uses `on_ending` alone (`rise_of_the_ottomans`); **only 1** uses both `on_ending` and `on_ended` (`treaty_of_tordesillas`); the other **20 use `on_ended` only**.

---

## 2. LIFECYCLE PATTERNS

### 2.1 `on_start` — six recurring jobs

1. **Zero the counters.** Almost every phased situation opens by declaring its variables at 0:
   `council_of_trent.txt:40-43` sets four in a row; `hussite_wars.txt:42-50`; `rise_of_timur.txt:30-45`;
   `war_of_religions.txt:38-40`; `guelphs_and_ghibellines.txt:27-28`; `italian_wars.txt:381-383`.
   `treaty_of_tordesillas.txt:41-54` even declares its phase counter with a float literal
   (`value = { value = 1.0 }`) — the float form matters because the situation later compares `= 1.0`.

2. **Build the rosters as GLOBAL variable lists.** This is the load-bearing idiom.
   `rise_of_the_ottomans.txt:40-45` fills `eligible_beylik_list` from every country with
   `government_reform:anatolian_beylik`. `fall_of_delhi.txt:41,56` fills `fall_of_delhi_voters`.
   `guelphs_and_ghibellines.txt:29,39-40` fills `guelphs_and_ghibellines_voters`.
   `nanbokuchou.txt:42,54,69,81` fills four lists at once (northern / southern / neutral / voters).
   `italian_wars.txt:186-190,213-218` fills `iw_foreign_leagues_list` and `iw_italian_leagues_list`
   **with the international organizations themselves, not countries** — then sorts them
   (`:368-379` `sort_global_variable_list ... order = { value = total_locations_owned }`).

3. **Rank the field and save the winners into situation variables.**
   `rise_of_the_ottomans.txt:56-147` runs three near-identical `ordered_in_global_list` blocks
   (`max = 1`, `check_range_bounds = no`, `order_by = { add = military_strength add = country_tax_base }`)
   to store 1st/2nd/3rd strongest plus a score variable for each.
   `sengoku.txt:58-252` does the same thing **five times** with a much heavier order_by
   (`country_total_army_levy_size × country_rank_level + army_size×10 + navy/2 + income/10 + 100 if great power`).
   Both then re-run the *identical* logic monthly from `scripted_effects/situation_effects.txt`
   (`rise_of_the_ottomans_recalculate_top_3` at `:352-501`, `sengoku_reevaluate_strongest_daimyos` at `:869-1073`).

4. **Fan out introduction events.** Uniformly `every_country = { limit = {…} trigger_event_non_silently = X }`:
   `black_death.txt:42-54` (whole Old World), `hundred_years_war.txt:41-62` (all of Western Europe, plus
   a distinct event each to ENG and FRA), `rise_of_timur.txt:46-60`, `red_turban_rebellions.txt:63-78`.
   Delayed variants exist: `guelphs_and_ghibellines.txt:46-49` `trigger_event_non_silently = { id = … days = 20 }`,
   and the outstanding one, `western_schism.txt:57-62`, which schedules an event on a **fixed future
   calendar date 40 years out**: `trigger_event_non_silently = { id = western_schism.4 trigger_on_next_date = 1402.3.14 }`
   with the comment `#Hus appointed preacher at the Bethlem Chappel`.

5. **Push the world-state changes the situation is "about".**
   `little_ice_age.txt:22-75` adds `extended_winter` to **37 named regions** one line each, then walks every
   area with winter and stamps `harsh_winters_modifier` with `years = -1` on every ownable location.
   `reformation.txt:29-129` is the richest single `on_start` in the game: enables `religion:lutheran`,
   picks a weighted random European university location (`weight` block at `:41-68` — +12 north German,
   +6 Scandinavian, +4 south German, +4 HRE-owned, **−0.5 Iberia and Italy**), splits **50% of its catholic
   pops** to lutheran (`split_pop = { fraction = 0.50 religion = religion:lutheran }`), `spawn_movement` with
   `supporters = { value = population multiply = 0.4 }`, `create_character` for Martin Luther with real birth
   data and `mil = { 80 100 }`, then registers him as the movement's first `add_spreader`.
   `war_of_religions.txt:49-85` **creates two international organizations from nothing** and installs their
   leaders in one pass. `italian_wars.txt:155-357` creates up to **seven** IOs (4 foreign leagues + 3 Italian).
   `sengoku.txt:42` forms a country outright: `c:JAP ?= { form_country = formable_country:ASK_f }`.

6. **Grant an AI personality/aggression nudge instead of a player-facing bonus.**
   `rise_of_the_ottomans.txt:47-54` gives `c:TUR` the modifier `ai_force_annexation` permanently
   (`years = -1`) — which is `ai_force_annexation_modifier = 1, aggressiveness_modifier = 2.5`
   (`main_menu/common/static_modifiers/country.txt:2838-2844`).
   `rise_of_timur.txt:61-66` gives TIM `rise_of_timur_impact`, `add_area_preference = timurids_timur_conquests`
   and `set_personality = ai_personality:ai_expansionist`.

### 2.2 `on_monthly` — five recurring jobs

1. **The weighted no-op roll.** The universal shape is a `random_list` whose largest weight is an empty
   block, so most months nothing happens. Vanilla's tuning spread is wide and deliberate:
   - `black_death.txt:74-103` — 27 events at weight 10 against `500 = { }` → ~35% chance of *something* per infected country per month
   - `little_ice_age.txt:119-139` — 18 events at weight 2 against `1000 = { }` → ~3.5%
   - `italian_wars.txt:484-495` — 9 events at weight 1 against `261 = {}`, with the comment
     `#Approximately 3.5% chance u get a relevant event per month`
   - `colonial_revolution.txt:44-65` — 3 events against `300 = { }` → ~1%
   - `sengoku.txt:293-332` — 3 events at 20 against `200 = { }` → ~23%
   - `the_revolution.txt:59-72` — **three independent rolls in sequence**, 2%, 1%, 1%
   - `fall_of_delhi.txt:135-203` — **two independent `random_list`s in the same month**, the second
     with a `95 = {}` filler and unequal weights (25 for the dhimmi/slavery event, 5 for its follow-up)

2. **Per-target `trigger` gates inside the roll.** The `random_list` entry can carry its own `trigger = { … }`
   so a branch is only eligible when it would make sense — `hundred_years_war.txt:76-138` gates the four
   war-driving branches on `NOT = { has_casus_belli_on }` / `NOT = { has_truce_with }` / `at_war = no` /
   `manpower_percentage > 0.75` / `war_exhaustion_percentage < 0.1` / `relative_strength … value > 0.45`.
   `rise_of_timur.txt:74-129` does the same for its three "help Timur" branches.

3. **Hand-rolled event cooldowns**, because the format has none.
   Three distinct dialects ship:
   - **Situation-side integer counters**: `rise_of_timur.txt:69-73,131-133` — increment two counters every
     month, and only roll when `var:rise_of_the_timur_event_cooldown > 10` (then reset to 1) or
     `> 20` for the "unique" tier.
   - **Fired-once flags**: `scripted_triggers/situation_triggers.txt:10-22` defines
     `can_fire_situation_event = { $situation$ = { situation_is_active = yes NOT = { has_variable = situation_event_$event$_fired } } }`
     and `has_fired_situation_event`, paired with the setter
     `flag_situation_event = { $situation$ = { set_variable = situation_event_$event$_fired } }`
     (`scripted_effects/situation_effects.txt:23-27`). `rise_of_timur.txt:137-268` is built almost
     entirely on this pair, chaining `if / else_if` over eight named "unique" events.
   - **Per-country `_cd` variables**: black_death's 27 events each own one — cleaned up individually
     in `on_ended` as 27 consecutive `if = { limit = { has_variable = bd1001_cd } remove_variable = bd1001_cd }`
     lines (`black_death.txt:158-184`).

4. **The severity/progress ratchet.** Only some situations escalate; when they do:
   - `guelphs_and_ghibellines.txt:158-262` — every month, sum the tax base of all Italian capitals into
     `gag_total_tax`, `multiply = 800`, sum each faction's members' tax base into local variables, divide,
     and `change_variable` the faction's `guelphs_progress` / `ghibellines_progress` by the resulting share.
     A faction wins at 1.0, so the multiplier 800 *is* the pacing dial.
   - `italian_wars.txt:404-424` — `iw_increase_tension_effect = { value = iw_tension_gain_low }` unconditionally,
     **plus one flat bonus if any foreign league leader is at war, plus one if any Italian league leader is**
     (with the comment `#not per-leader, to avoid stacking`), and decay while the PoNR cooldown holds.
     At `>= 50` tension it stamps `demand:italian_wars_militarization` on every league leader's capital market
     (`:472-478`); at `>= 100` it fires `italian_wars.11` at every league leader and sets a 10-year lockout
     variable (`:449-470`).
   - `treaty_of_tordesillas.txt:135-183` — phase 1 adds `+0.5` progress a month, clamped 0-100; on hitting
     100 it flips `var_treaty_phase` to 2.0, fires a silent event to every catholic, and calls
     `distribute_world = yes`. Phase 2 then recomputes `var_treaty_subtract` from scratch every month
     (`0.1` base plus `0.1` per country currently violating the treaty) and subtracts it from progress.
   - `western_schism.txt:191` — one line, `change_variable = { name = western_schism_cardinal_weight_bonus add = 1 }`,
     which silently makes each successive papal vote more decisive.
   - `war_of_religions.txt:100-164` — rebuild the "wants war" / "wants peace" global lists from the current
     war's participants using a **war-length × war-exhaustion staircase** (`>25y: everyone; >20y & WE>0.2;
     >15y & WE>0.4; >10y & WE>0.6; WE>0.8`), then compute a ratio and fire the Peace of Westphalia at `> 0.8`.

5. **Self-healing / desync repair.** Vanilla assumes its own bookkeeping will drift:
   `western_schism.txt:70-72` re-runs `set_papal_states_schism_cardinal` and `set_schism_opponent_country`
   monthly with the comment `#if the cardinals get lost for whatever reason, then we need to make new ones`.
   `italian_wars.txt:401` calls `reconcile_italian_wars_league_land = yes`, defined at
   `scripted_effects/situation_effects.txt:1169-1224` with the comment
   `#Safety net for locations conquered during a war/peace that on_location_changed_owner missed`.
   `war_of_religions.txt:166-199` re-joins a league leader to the war it should be in after an IO
   leadership transfer (`#Bug fix: keep league leaders as war participants after IO leadership transfers`).
   `fall_of_delhi.txt:123-134` re-applies `dlh_situation_modifier` if it has gone missing.
   `nanbokuchou.txt:88-155` clears and rebuilds all three side lists from scratch every single month.

6. **Performance caching, done in script.** `sengoku.txt:263-291` precomputes a per-clan boolean
   `sengoku_has_hostage_candidate` with the comment
   `# Cache whether each clan has a valid hostage candidate so sengoku_ask_for_hostage visible checks can use
   a cheap variable lookup instead of any_close_relative per target.`
   `nanbokuchou.txt:140-153` does the same for `nanbokuchou_has_valid_cb_target` / `_war_target`.
   This is a real technique: the expensive predicate runs once per member per month instead of once per
   action-target evaluation.

### 2.3 `on_ending` vs `on_ended`

Per the readme (`situations/readme.txt:14-15`): `on_ending` runs "just before its status changes",
`on_ended` "just after". Vanilla barely uses the distinction:

- `rise_of_the_ottomans.txt:297` uses **`on_ending` only** — because it must still read
  `var:strongest_beylik_variable` and `eligible_beylik_list` to decide the outcome, then
  `form_country = formable_country:RUM_f` and finally clear the list (`:383-386`).
- `treaty_of_tordesillas.txt:186-218` uses **both**: `on_ending` fires the closing event to every catholic
  who can see the situation, `on_ended` strips the colonial claims and the violation modifiers.
- All 20 others use `on_ended` only.

### 2.4 What `on_ended` actually does — four jobs

1. **Strip everything the situation added.** `black_death.txt:143-214` is the archetype: remove 11 country
   modifiers from *every* country unconditionally, remove 27 cooldown variables, remove temporary market
   demands, and `every_location_in_the_world = { remove_location_modifier = isolating_cities }`.
   `little_ice_age.txt:184-189` walks every area on the map removing `harsh_winters_modifier` and
   `remove_extended_winter`. `hundred_years_war.txt:147-164` removes the modifier, the mutual opinion,
   **and the situation's two casus belli** (`cb_hundred_years_war`, `cb_hundred_years_war_fra`).
2. **Branch the outcome and fire an ending event per faction.** `guelphs_and_ghibellines.txt:268-372` has
   three outcomes and four fallbacks for who narrates the ending (PAP → winning faction leader → any
   Western European country). `hundred_years_war.txt:167-238` has three (English victory / French victory /
   inconclusive). `red_turban_rebellions.txt:157-300` has a **five-deep `else_if` chain to decide who "China"
   now is**: surviving Yuán → red-turban leader → owner of Dàdū → owner of Shàngyuán → the most populous
   east-Asian country of a Chinese/Mongol/Jurchen culture group.
3. **Write the permanent record.** `guelphs_and_ghibellines.txt:277,293,301` sets a global variable
   `guelphs_and_ghibellines_ended` to `1 / -1 / 0` and stamps `won_guelphs_and_ghibellines` on every member
   of the winning IO. `hussite_wars.txt:125-135` sets `victorious_hussites_variable` with `years = 1` **and**
   a permanent `hussites_won_hussite_wars`, explicitly commented `#Tracking for the achievement house_of_hus`.
   `black_death.txt:144` calls `set_situation_end_flag_effect = { situation = black_death }`, which is
   `set_global_variable = situation_ended_$situation$` (`scripted_effects/global_effects.txt:242-248`) —
   the readable counterpart to the engine's own `situation_has_ended`, queryable later via
   `had_situation_trigger` (`scripted_triggers/situation_triggers.txt:33-39`). **Only black_death calls it.**
4. **Copy situation state down to the countries before the situation is destroyed.**
   `western_schism.txt:199-208` copies five situation variables onto **every catholic country** so the
   ending event can read them, then removes them from the situation. This is the only clean answer to
   "the situation object is gone but the epilogue still needs its numbers".

### 2.5 Chaining

`activate_situation` appears **6 times** in the whole game:
- `in_game/common/diseases/bubonic_plague.txt:165` → black_death
- `in_game/common/diseases/great_pestilence.txt:105` → great_pestilence
- `in_game/common/on_action/_hardcoded.txt:2074` → hundred_years_war (on an ENG/FRA war declaration)
- `in_game/events/DHE/flavor_tim.txt:653` → rise_of_timur
- `in_game/events/situations/treaty_of_tordesillas.txt:325` → treaty_of_tordesillas

`end_situation` appears **8 times**: treaty_of_tordesillas ×2 (`_hardcoded.txt:855,3940`),
nanbokuchou (`peace_treaties/nanbokuchou_force_imperial_abdication.txt:64`, `events/situations/nanbokuchou.txt:646`),
war_of_religions (`peace_treaties/religious_supremacy.txt:53`, `events/situations/war_of_religions.txt:1827`),
council_of_trent (`scripted_effects/situation_effects.txt:515`), hundred_years_war (`events/DHE/flavor_ENG.txt:291`).

**No situation ever calls `activate_situation` on another situation.** Chaining is done by *gating*:
`war_of_religions.txt:6-9` requires `situation:council_of_trent = { situation_is_active = no situation_has_ended = yes }`;
`reformation_end_trigger` requires both CoT and WoR to have ended (`situation_triggers.txt:637-651`);
`italian_wars.txt:6` requires `NOT = { is_situation_active = situation:guelphs_and_ghibellines }`.
That is the whole vanilla technique for sequencing an era.

### 2.6 The on_action surface

Situations are referenced **80 times** in `in_game/common/on_action/_hardcoded.txt`, concentrated in:
`on_annexed` (23), `on_war_declared` (14), `on_religion_changed` (14), `on_location_changed_owner` (8),
`on_winning_war` (6), `on_ending_war` (6), `on_new_ruler` (2), `on_dependency_gained` (2), `on_annex` (2),
`on_losing_war` (1), `on_great_battle_won` (1), `on_battle_won` (1).
Examples: `_hardcoded.txt:1517-1529` re-points `fall_of_delhi`'s `strongest_claimant_capital` when its owner
loses a war; `_hardcoded.txt:1979-1997` clears `rise_of_timur`'s `rot_conquest_ambition` region;
`_hardcoded.txt:801-889` runs the whole Tordesillas country-replacement dance on annexation.
**A rich situation is not self-contained** — roughly a third of its state maintenance lives in on_actions.

---

## 3. PHASE MACHINERY — every situation that models stages, with the read-back idiom

There is **no engine phase concept**. Every phase is a hand-rolled variable on the situation.
Five distinct idioms ship:

**(a) Explicit float phase + progress bar** — `treaty_of_tordesillas` only.
Set: `situations/treaty_of_tordesillas.txt:47-50` `set_variable = { name = var_treaty_phase value = { value = 1.0 } }`.
Advance: `:149` `set_variable = { name = var_treaty_phase value = { value = 2.0 } }`.
Read back three different ways depending on root:
- inside `on_monthly` (root = situation): `:137` `var:var_treaty_phase = 1.0`
- inside `can_end`: `:17` `situation:treaty_of_tordesillas.var:var_treaty_phase = 2.0`
- inside `tooltip`/`map_color` (root = location): `:224` `situation:treaty_of_tordesillas.var:var_treaty_phase = 1.0`
  and `:339-343` `scope:target = { has_variable = var_line_location } scope:target.var:var_line_location ?= this`
The progress bar itself: `:140-141` `change_variable = { name = var_treaty_progress add = 0.5 }` then
`clamp_variable = { name = var_treaty_progress max = 100 min = 0.0 }`.

**(b) Race-to-1.0 progress accumulators** — `guelphs_and_ghibellines`.
The variables live **on the IOs, not on the situation**: `:232-262`
`international_organization:guelphs_io ?= { … change_variable = { name = guelphs_progress add = local_var:guelphs_total_tax } }`.
Read back in `can_end` via the scripted trigger `guelphs_and_ghibellines_guelphs_end_trigger`
(`scripted_triggers/situation_triggers.txt:671-683`): `international_organization:guelphs_io = { has_variable = guelphs_progress var:guelphs_progress >= 1 }`.
Note the situation *also* declares `guelphs_progress`/`ghibellines_progress` on itself at `:27-28` —
and those two copies are never read again (see §9).

**(c) Bounded tension meter with a point of no return** — `italian_wars`.
`scripted_effects/situation_effects.txt:1087-1103`:
```
iw_increase_tension_effect = {
	custom_description = { text = iw_increase_tension_effect_tt value = $value$
		situation:italian_wars ?= {
			change_variable = { name = iw_tension add = $value$ }
			clamp_variable = { name = iw_tension min = 0 max = 100 }
		} } }
```
plus `iw_reset_tension_effect` (`:1075-1085`). Read back in `on_monthly` as `var:iw_tension >= 100` (`:451`)
and `var:iw_tension >= 50` (`:473`). The PoNR is one-shot per cycle because it writes
`allow_call_members_offensive_wars_variable = current_year` and refuses to re-fire while that exists.

**(d) Debate / score counters with a declared maximum** — `council_of_trent`, `western_schism`, `hussite_wars`, `war_of_religions`.
`council_of_trent.txt:40-43`: `council_of_trent_passed_debates`, `_failed_debates`, and both `_max = 5`.
Mutated from *outside* the situation file, in the vote callbacks
(`scripted_effects/situation_effects.txt:545-600` `council_of_trent_pass_effect`, `:602-639` `council_of_trent_reject_effect`),
read back in `council_of_trent_end_trigger` (`situation_triggers.txt:653-669`) by comparing
`var:council_of_trent_passed_debates >= var:council_of_trent_passed_debates_max` — **variable vs variable,
not variable vs literal**, which is what makes the max tunable.
`western_schism.txt:44-47` mirrors this with `western_schism_pope_score` / `_anti_pope_score`, incremented
in `resolutions/western_schism.txt:112-126`.

**(e) Ranking variables refreshed every month** — `rise_of_the_ottomans` (3 ranks), `sengoku` (5 ranks).
Written as `situation:rise_of_the_ottomans = { set_variable = { name = strongest_beylik_variable value = prev } }`
inside an `ordered_in_global_list` (`rise_of_the_ottomans.txt:70-82`). Read back **everywhere**:
- `visible`: `country_exists = situation:rise_of_the_ottomans.var:strongest_beylik_variable` (`:23`)
- `on_monthly` (root = situation): `var:strongest_beylik_variable ?= { … }` (`:190`)
- `tooltip`/`map_color` (root = location): `situation:rise_of_the_ottomans.var:strongest_beylik_variable = owner` (`:418`)
- `legend_key`: `color = situation:rise_of_the_ottomans.var:strongest_beylik_variable.country_color` (`:525`)
- from another situation entirely: `rise_of_timur.txt:341` `scope:previous_owner = situation:rise_of_the_ottomans.var:strongest_beylik_variable`

**(f) Clamped per-country allegiance scalar** — `red_turban_rebellions`.
`scripted_effects/situation_effects.txt:91-124` `rtr_change_allegiance_points` — initialise to 0 if absent,
`change_variable`, then clamp by hand with two `if` blocks at ±100 (it does **not** use `clamp_variable`).
Read back in the situation's `map_color` (`red_turban_rebellions.txt:378-379`) as
`has_variable = rtr_yuan_allegiance` **and** `var:rtr_yuan_allegiance > 50` — the existence check is
mandatory, and the tooltip immediately above (`:322`) omits it (see §9).

---

## 4. THE ACTION ECONOMY — 155 situation actions

Declared with `type = situation` (`in_game/common/generic_actions/readme.txt:5`). The mandatory plumbing that
makes an action *belong* to a situation is a `select_trigger` of `looking_for_a = situation` with
`target_flag = recipient`:
```
select_trigger = {
	looking_for_a = situation
	target_flag = recipient
	name = "choose_situation"
	column = { data = name }
	visible = { situation:hussite_wars = this  situation_is_active = yes }
}
```
(`generic_actions/hussite_wars_actions.txt:169-180` — this exact block, with the situation key swapped,
appears in essentially every situation action.)

### 4.1 Counts

| situation | actions | situation | actions |
|---|---|---|---|
| black_death | **18** (9 do/undo pairs) | rise_of_the_ottomans | 8 |
| treaty_of_tordesillas | **12** | colonial_revolution | 8 |
| hundred_years_war | **12** | italian_wars | 8 |
| great_pestilence | 10 | guelphs_and_ghibellines | 7 |
| red_turban_rebellions | 10 | the_revolution | 7 |
| sengoku | 10 | fall_of_delhi | 5 |
| hussite_wars | 9 | golden_age_of_piracy | 5 |
| — | — | rise_of_timur / war_of_religions | 5 / 5 |
| — | — | columbian_exchange 4, reformation 3, western_schism 3, little_ice_age 3, nanbokuchou 2 |
| **council_of_trent: 0** — it has no action file at all; the player acts through `resolution:policy_vote` on the Catholic Church IO |

### 4.2 Price — six currencies, and gold is not the default

Prices are named entries in `in_game/common/prices/00_hardcoded.txt`. Real values:

| price | contents | file:line |
|---|---|---|
| `hyw_main_actions_price` | `government_power = 10` | `:1164-1166` |
| `hussite_wars_actions_price` | `religious_influence = 10` | `:437-439` |
| `western_schism_ri_actions_price` | `religious_influence = 20` | `:1174-1176` |
| `western_schism_gold_actions_price` | `scaled_gold = 1` | `:1178-1180` |
| `lia_actions_price` | `government_power = 5` | `:1182-1184` |
| `revolution_actions_price` | `scaled_gold = 1` **+** `government_power = 5` | `:1168-1171` |
| `rtr_grant_titles_price` | `legitimacy = 5` | `:820-822` |
| `rtr_negotiate_with_rebels_price` | `scaled_gold = 1.0` | `:823-825` |
| `join_italian_wars_price` | `scaled_gold = 1`, `max_scale = 500` | `:851-854` |
| `create_italian_league_price` | `scaled_gold = 5` | `:856` |
| `rto_press_claims_price` | `scaled_gold = 2` | `:964-966` |
| `rto_create_uc_bey` | flat `gold = 100` | `:968-970` |
| `nanbokuchou_change_sides` | `stability = 30` **+** `honor = 30` | `:885-888` |
| `nanbokuchou_declare_neutrality` | `stability = 10` | `:890-891` |
| `sengoku_offer_hostage` | `prestige = 20` + `legitimacy = 15` | `:932-935` |
| `sengoku_ask_for_hostage` | `prestige = 30` | `:937-938` |
| `tordesillas_move_the_line` | `prestige = 5` + `religious_influence = 1` | `:1124-1127` |
| `tordesillas_swap_sides` | `prestige = 15` | `:1129-1130` |

**The design point:** the currency *is* the theme. Hundred Years' War actions cost government power
(court capacity), Hussite and Schism actions cost religious influence, Red Turban actions cost legitimacy,
Sengoku hostage diplomacy costs prestige and legitimacy, and switching sides in the Nanbokuchō costs
**30 stability and 30 honor** — the harshest single action price in the set, and the only one that uses `honor`.
Of the 155 actions, roughly a fifth have **no `price` at all** (e.g. all 7 `guelphs_and_ghibellines` actions,
all 5 `war_of_religions` actions, `fall_of_delhi`'s 5) — those are gated by cooldown and trigger only.

`price_modifier` is used **4 times** in all 155: `hundred_years_war.txt` (`crown_new_ruler`),
`italian_wars.txt` (`fortify_key_location`), `red_turban_rebellions.txt` (`rtr_rein_in_area`),
`treaty_of_tordesillas.txt` (`tordesillas_move_the_line`, which multiplies by the per-country counter
`var_tordesillas_moved_the_line` initialised at `situations/treaty_of_tordesillas.txt:57-68` —
each use of the action makes the next one dearer).

### 4.3 Cooldown — the pacing dial

`cooldown = { type = <tag> days/weeks/months/years = <int> }` (`generic_actions/readme.txt:73`).
Observed spread across the 155:
- **2 months** — `influence_french_subject` (`hundred_years_war.txt:70` per the extraction: `type = influence_french_subject months = 2`)
- **6 months** — every `sengoku` hostage/autonomy/revoke action; `little_ice_age` `send_food_aid`
- **1 year** — `columbian_exchange` `learn_from_foreigners` / `absorb_institutions`, all six
  `tordesillas_*` claim actions, `rise_of_the_ottomans` `offer_diplomatic_protection`, `hussite_wars` `convert_heretics`
- **2-5 years** — the bulk
- **10 years** — `guelphs_sanction_emperor` / `ghibellines_sanction_pope`, `hyw` `demand_autonomy`,
  `join_the_imperial_side_hw_action`, `create_allied_pirate_nation`, `migrate_to_new_waters`, `demand_member_removal`
- **15 years** — `request_papal_delegates`
- **30 years** — `crown_new_ruler` (the longest in the set; a once-a-reign action)
- **Computed cooldowns** exist: `italian_wars.txt` `plan_campaign_in_italy` has a `years = { if = { limit = { scope:actor ?= { NOT = { has_variable = lower_cooldown_campaign_in_italy_variable … }` block, and
  `fortify_key_location` uses `years = { add = { value = 10 desc = BASE_VALUE … } }`.

A **second, softer cooldown layer** is built from situation variables rather than the engine's:
`generic_actions/guelphs_and_ghibellines.txt:46-63` blocks joining if
`country_has_recently_joined_situation_faction = { situation = guelphs_and_ghibellines years = 5 variable = gag_recently_joined_a_faction }`
or `…left… years = 2 …`, with those variables set by `join_situation_faction` /
`leave_situation_faction` (`scripted_effects/situation_effects.txt:29-86`). Faction churn is therefore
5 years in / 2 years out — a real strategic commitment, not a toggle.

### 4.4 `ai_tick` — how often the AI even looks

From the extraction: `ai_tick = daily` on all 18 black_death actions and all 10 great_pestilence actions
(plague responses must be immediate), `ai_tick = monthly` on the large majority, `ai_tick = never` on
exactly two — `black_death.txt` `procure_remedies` (`ai_will_do` absent too) and
`rise_of_the_ottomans.txt` `create_uc_bey`. Most also carry `ai_tick_frequency` (commonly 6) and
`automation_tick = never / automation_tick_frequency = 12` (`generic_actions/readme.txt:61-64`).

### 4.5 `ai_will_do` — the difference between decorative and meaningful

The floor is one line: `ai_will_do = { add = 100 }` — all three Hussite donation actions
(`hussite_wars_actions.txt:201-203, 266-268, 330-332`). The AI will always do it, always.

One tier up, a conditional preference:
```
ai_will_do = {	#Appanage should always want this as long as they are disloyal
	add = 5
	if = { limit = { scope:actor = { subject_loyalty > 50 } } add = -10 }
}
```
(`hundred_years_war.txt:64-71`)

And a hard situational gate — the AI does this *only* when losing a stalemate:
```
ai_will_do = {
	if = { limit = { scope:actor = { any_current_war = { … war_score_in_war = { war = prev value < 10 } } } }
		add = 100 }
	else = { subtract = -100 }
}
```
(`hundred_years_war.txt:151-175`)

The ceiling is `gag_join_faction` (`generic_actions/guelphs_and_ghibellines.txt:108-171`), which scores by
**comparing the utility of the modifiers on offer** and adds explicit inertia:
```
add = { value = "scope:target.modifier_utility(scope:actor)" }
… if not in any faction: add = 100
every_international_organizations_member_of = { … subtract = { value = "modifier_utility(scope:actor)" add = 1 } }   #inertia
… ruler has gag_favors_guelphs and target is guelphs_io: add = 100
… has_variable = gag_force_switched_faction_penalty: add = -100
```
**This is the craft distinction.** An action is decorative when its `ai_will_do` is a constant and its
effect is a one-off resource transfer. It is meaningful when (a) the price is a currency the situation
itself is about, (b) the cooldown is long enough to make it a decision rather than a rotation, (c) the
`ai_will_do` reads the current world state, and (d) the effect writes into the situation's own phase
variables so the choice moves the meter. `italian_wars`'s `plan_campaign_in_italy` (216 lines,
computed cooldown, feeds `iw_tension`) and `guelphs_and_ghibellines`'s faction actions (which move
`guelphs_progress`) are the two clearest examples of all four.

### 4.6 Action size

The 155 actions are not small. Median block length ~110 lines; the largest are
`columbian_exchange` `move_ow_good_to_new_location` (492 lines), `move_nw_good_to_new_location` (373),
`war_of_religions` `join_the_league_war` (270), `italian_wars` `iw_intervene_in_war` (269),
`rise_of_the_ottomans` `press_claims` (289), `hundred_years_war` `betray_our_allegiance` (231).
`select_trigger` count runs 1-4 per action; the 4-target ones are
`columbian_exchange`'s two goods-movers, `rise_of_the_ottomans` `offer_diplomatic_protection`,
`rise_of_timur` `rot_promote_regional_culture`, and `tordesillas_demand_transfer_colony`.

---

## 5. THE REWARD / PENALTY ECONOMY — how harsh vanilla is willing to be

### 5.1 The magnitude ladder

Situations almost never write bare numbers; they use the shared ladder in
`main_menu/common/script_values/default_values.txt`:

| tier | stability (`:10-23`) | prestige (`:26-37`) | legitimacy (`:70-81`) |
|---|---|---|---|
| weak | ±2.5 | ±5 | ±5 |
| mild | ±7 | ±10 | ±10 |
| severe | ±12 | ±15 | ±15 |
| extreme | ±20 | ±20 | ±20 |
| very_extreme | ±25 | — | — |
| ultimate | ±50 | ±50 | ±50 |
| radical | ±100 | ±100 | ±100 |

Across the 473 situation events, actual usage is: `stability_mild_penalty` (−7) ×24,
`stability_mild_bonus` ×20, `stability_weak_penalty` ×17, `stability_severe_penalty` (−12) ×14,
`stability_extreme_penalty` (−20) ×8, **`stability_ultimate_penalty` (−50) ×5**,
`stability_very_extreme_penalty` (−25) ×1.

**Vanilla is willing to take half a country's stability in one event option.** Confirmed sites:
`events/situations/fall_of_delhi.txt:1449`, `events/situations/hundred_years_war.txt:1211`,
`events/situations/hussite_wars.txt:169` (paired with `estate_satisfaction_radical_penalty` two lines above),
`events/situations/rise_of_timur.txt:1415,1442`; and `−25` at `events/situations/little_ice_age.txt:1633`
(spoiled food stores). War exhaustion goes to `war_exhaustion_ultimate_penalty` once
(`events/situations/war_of_religions.txt:1904`).

Prestige usage is gentler and roughly symmetric: `prestige_mild_penalty` ×24 vs `prestige_mild_bonus` ×19,
`prestige_extreme_bonus` ×10 vs `prestige_extreme_penalty` ×4, and `prestige_radical_bonus` (+100) ×3.
Legitimacy is the rarest lever (26 uses total).

### 5.2 The modifiers situations push

| modifier | contents | file:line |
|---|---|---|
| `hundred_years_war_impact` | **`blocks_country_formation = yes` and nothing else** | `main_menu/common/static_modifiers/country.txt:6466-6471` |
| `rise_of_timur_impact` | `blocks_country_formation = yes`, `aggressiveness_modifier = 0.5` | `country.txt:6472-6478` |
| `ai_force_annexation` (given to TUR) | `ai_force_annexation_modifier = 1`, `aggressiveness_modifier = 2.5` | `country.txt:2838-2844` |
| `jap_nanbokuchou` (every clan, `years = -1`) | `monthly_prestige = -0.1`, `monthly_legitimacy = -0.2` | `country.txt:7012-7019` |
| `dlh_situation_modifier` (the strongest claimant) | `declaring_war_cost_modifier = -0.33`, `global_integration_speed_modifier = 0.1`, `antagonism_received_modifier = -0.2` | `country.txt:7717-7725` |
| `rtr_red_turban_rebellions` | `monthly_rebel_growth = -0.05`, `stability_investment` penalty, `monthly_legitimacy = -0.05`, `country_cabinet_efficiency = -0.2`, medium estate-satisfaction penalty, **`global_levy_size_modifier = -0.45`**, **`global_mercenaries_modifier = -0.75`** | `country.txt:8421-8432` |
| `hussite_heresy_modifier` | small estate-satisfaction penalty, `monthly_religious_influence = -0.1` | `country.txt:6185-6191` |
| `strongest_pirate_modifier` (re-elected monthly) | `global_sailors_modifier = 0.33`, `naval_damage_done = 0.1`, `monthly_prestige = 0.2` | `country.txt:11376-11382` |
| `harsh_winters_modifier` (every location in 37 regions, permanent) | `local_food_capacity_modifier = -0.25`, `local_monthly_food_modifier = -0.25` | `main_menu/common/static_modifiers/location.txt:2972-2978` |
| `western_schism_modifier` (on `religion:catholic`, `days = -1`) | `monthly_reform_desire = 0.0005`, `cardinal_price_cost_modifier = -0.5`, **`curia_actions_blocked = yes`** | `main_menu/common/static_modifiers/religion.txt:20-27` |

Two lessons: **(1)** the flagship modifiers are frequently *flags, not stats* — the Hundred Years' War's
signature country modifier does exactly one thing, block country formation. **(2)** when vanilla does go
hard, it goes very hard and permanently: `rtr_red_turban_rebellions` cuts levy size by 45% and mercenaries
by 75% for the whole duration; the Little Ice Age puts a permanent −25%/−25% food modifier on **every
location in 37 regions** (`situations/little_ice_age.txt:22-75`); the Western Schism blocks all curia
actions for the entire Catholic religion for as long as it runs.

Duration convention across situation events: `years = -1` (permanent, cleaned up in `on_ended`) is the
most common by far (57 uses), then `years = 5` (31), `years = 10` (30), `years = 2` (13), `years = 1` (11),
with rare long tails at 100 and 200 years.

### 5.3 Resolution-level penalty

`resolutions/western_schism.txt:41-44` — while the schism vote is open, **every member of the Catholic
Church IO** carries `vote_ongoing_modifier = { clergy_estate_target_satisfaction = small_permanent_target_satisfaction_penalty  monthly_prestige = -0.05 }`.
The dithering itself costs, which is the pressure that ends the vote.

---

## 6. MAP DRAMA

### 6.1 Colour sourcing — four schools

1. **Owner's own colour** (the "who is in whose camp" look): `value = owner.country_color`
   (`hussite_wars.txt:217,235,242,249`; `sengoku.txt:347`; `colonial_revolution.txt:184,197`;
   `italian_wars.txt:795,806,817`) and `value = top_owner.country_color` (`colonial_revolution.txt:200`,
   `treaty_of_tordesillas.txt:319,329`).
2. **Named colours from `main_menu/common/named_colors/02_map.txt`** (4,081 entries) — the situation-specific
   block sits at `:4252-4327`: `delhi_claimant_color = rgb { 220 20 60 }` (`:4252`),
   `cot_conciliatory_color = rgb { 45 75 203 }` / `cot_belligerent_color = rgb { 203 75 43 }` (`:4259-4260`),
   `rtr_emperor_color = rgb { 254 206 27 }` (`:4263`), `rtr_neutral_color = rgb { 100 100 100 }` (`:4267`),
   `gag_guelphs_color = rgb { 232 149 18 }` / `gag_guelphs_leader_color = hsv360 { 60 100 100 }` (`:4270-4271`),
   `war_of_religions_protestant_union_color = rgb { 0 76 153 }` (`:4275`),
   `reformation_reformer = rgb { 27 201 104 }` (`:4285`), `map_iw_italian_1 = rgb { 185 35 35 }` (`:4321`),
   `iw_center_color = rgb { 255 220 50 }` (`:4327`). Country-map colours are reused directly:
   `map_ENG` (`:15`), `map_FRA` (`:83`), `map_TIM` (`:129`), `map_delhi` (`:418`).
3. **Bare engine literals** — `black`, `red`, `green`, `blue`, `yellow`, `purple`, `orange`
   (`golden_age_of_piracy.txt:207-241`; `nanbokuchou.txt:416-494`; `rise_of_timur.txt:340-348`).
4. **Defines** — `define:NMapColors|DEFAULT_COLOR` is the universal else-branch (16 of 22 situations);
   also `POPULATION_STARVING_COLOR_STRIPE`, `MAP_COLOR_MID`, `MAP_COLOR_HIGH`, `MAP_COLOR_LOW`
   (`little_ice_age.txt:199-214`).

### 6.2 The three tricks worth stealing

**`lerp` for a continuous gradient.** Only three situations recolour *by magnitude*:
```
lerp = { min_color = rgb { 248 180 194 }  max_color = rgb { 61 0 0 }
         factor = "disease_presence(disease:great_pestilence)" }
```
(`great_pestilence.txt:150-154`); `black_death.txt:226-230` does the same against
`disease_outbreak_presence(scope:target.var:original_outbreak)`; `treaty_of_tordesillas.txt:383-405`
lerps a league colour toward the default at a fixed `factor = 0.40` to produce a washed-out "claimed but
not owned" tint. **This is the only mechanism in the format for showing a number on the map.**

**`secondary_map_color` for a second, orthogonal fact.** 9 of 22 use it, and the good uses are the ones
that say something the primary colour cannot:
- `hundred_years_war.txt:382-427` — primary = who you belong to, secondary = who you are *allied* to,
  so a country loyal to France but allied to England is visibly striped.
- `rise_of_the_ottomans.txt:544-551` — a red stripe wherever a `seljuk_mint` stands.
- `italian_wars.txt:907-913` — gold stripes over the league colour for the
  `italian_administration_center` building (`# Italian Administration Center — gold stripes over the province's league color`).
- `rise_of_timur.txt:354-362` — purple stripes over **the region Timur has publicly declared he intends
  to conquer** (`scope:target = { has_variable = rot_conquest_ambition } region = scope:target.var:rot_conquest_ambition`).
  This is the single most expressive use of the field in vanilla: a player-visible declaration of intent,
  painted on the map, driven by an action.
- `hussite_wars.txt:256-263` — a low-colour stripe on any province with `recent_tribunal_modifier`.
- `nanbokuchou.txt:522-532` — `is_multiplayer_session = no` and human-owned → `value = white`, i.e.
  **the map marks the player's own holdings** in single player.
- `reformation.txt:589-606` — stripes for a ≥5% religious minority that is not yet dominant.

**Which situations recolour over time.** Only those whose colour predicate reads a moving variable:
`treaty_of_tordesillas` (phase 1 vs 2 changes which branches even evaluate),
`rise_of_the_ottomans` and `sengoku` (the top-N variables move monthly, so the map's "hot" countries drift),
`black_death` / `great_pestilence` (the lerp factor is the live infection level),
`reformation` (dominant religion per location), `red_turban_rebellions` (the allegiance scalar crossing
+50 / −25), `little_ice_age` (starving vs negative food balance vs merely cold).
The rest are static in shape and change only when a country changes camp.

### 6.3 `legend_key`

`legend_key = { desc = <loc or engine expression> color = <same colour expression> require_color_on_map = yes }`.
`require_color_on_map = yes` hides the row when nothing on the map carries the colour — used in 18 of the
20 situations that have legends. Three situations put a **`limit` block inside the legend key** so the row
only exists for qualifying locations: `hussite_wars.txt:302-313`, `sengoku.txt:354-368`,
`treaty_of_tordesillas.txt:350-371`. `desc` accepts engine expressions, not just loc keys:
`desc = "[disease|e]"` (`black_death.txt:238`), `desc = "[pirates|e]"` (`golden_age_of_piracy.txt:246`),
`desc = "[ShowBuildingTypeName('seljuk_mint')]"` (`rise_of_the_ottomans.txt:539`),
`desc = "[revolutionary_target|e]"` (`the_revolution.txt:218`).

### 6.4 `is_data_map`

Set by exactly two situations, both plague (`black_death.txt:216`, `great_pestilence.txt:144`), and by
nothing else in the game. Both are also the only two using `lerp` on a live engine value. The pairing is
almost certainly the rule: **`is_data_map = yes` is for a situation whose map is a heat map of a number,
not a partition into camps.**

---

## 7. SEEDING — what `22_situations.txt` actually contains

`main_menu/setup/start/22_situations.txt` is **47 lines and almost entirely commented out**:

```
situation_manager={
	rise_of_the_ottomans={
	#	status=active
	#
	#	variables={
	#		data={ {
	#				flag="rise_of_the_ottomans_cooldown"
	#				tick=0
	#				data={ type=value  identity=100000 }
	#			} }
	#	}
	}

	# guelphs_and_ghibellines = { … all commented … }
}
```
(`main_menu/setup/start/22_situations.txt:1-47`)

Findings:
- The wrapper key is `situation_manager`, and each situation is a block keyed by its situation key.
- **`rise_of_the_ottomans` is the only live entry, and its body is empty** — the `status=active` line is
  commented out. So **no situation starts active at 1337.** Everything begins via `can_start` polling,
  or via `activate_situation` from a disease/event/on_action.
- The commented-out form documents the save-game-style shape a modder *could* use:
  `status=active` and a `variables={ data={ { flag="…" tick=0 data={ type=value identity=100000 } } } }` block.
  `identity=100000` is the save-file encoding of a value-typed variable, not something you would hand-write.
- Practical consequence for a 1066 mod: **the seeding file is not the tool for starting a situation on day
  one.** The two attested day-one mechanisms are (a) a `can_start` that is already true —
  `guelphs_and_ghibellines.txt:6-9` is exactly this, `game_is_initialized = yes` plus
  `current_date > 1337.4.1`, which fires within the first month at `monthly_spawn_chance = 1.0`; and
  (b) an `activate_situation` from an on_action or a bookmark event.
- Note the format's date arithmetic: `guelphs_and_ghibellines`, `rise_of_the_ottomans` and
  `hundred_years_war` all gate on `current_date > 1337.4.1` / `1337.5.1` — i.e. **one to two months after
  the 1337.1.1 start**, never on the start date itself.

---

## 8. THE FOUR RICHEST SITUATIONS — dissected

Ranked by total moving parts (situation lines + events + actions + GUI + phase variables + IOs).

### 8.1 `rise_of_the_ottomans` — the richest by content volume
- 593 situation lines, **42 events / 3,152 event lines**, **8 actions / 22,383 bytes**, 8,958-byte GUI panel.
- **Phase machinery:** 6 variables (3 ranked countries + 3 score variables), recomputed **every month** by
  `rise_of_the_ottomans_recalculate_top_3` (`scripted_effects/situation_effects.txt:352-501`, 150 lines) —
  which first *prunes dead or vassalised countries out of `eligible_beylik_list`* (`:353-379`) before ranking.
- **Escalation ladder in `on_monthly`, four rungs keyed to the leader's size** (`:253-293`):
  `num_locations > 120` → the "we are becoming a power" event pair (`.400`, then `.215` after `days = { 10 25 }`);
  `num_locations > 300` **and** `num_of_non_rural >= 30` **and** `owns = location:constantinople` → `.600`.
- **The only user of `content_trigger`** (`:5-9`).
- **Three-way outcome in `on_ending`** (`:297-387`): no beyliks left → generic end; a stagnation branch
  gated on year and size → `.500` to every beylik; otherwise **the winner forms a country** —
  `form_country = formable_country:RUM_f` after stripping every TUR core from the map (`:352-367`), and
  a two-year global victory flag.
- Map: 6 legend keys, a full `secondary_map_color` mirror of the primary, and the legend colours are
  themselves *variable reads* (`color = situation:….var:strongest_beylik_variable.country_color`, `:525`).
- **Verdict on what makes it rich:** a live competitive ranking the player can see, an escalation ladder
  tied to concrete map facts (location count, non-rural count, one named city), and three genuinely
  different endings one of which rewrites the political map.

### 8.2 `italian_wars` — the richest by systems integration
- **1,059 situation lines (the longest)**, 20 events / 2,106 lines, 8 actions / 40,813 bytes,
  34,759-byte GUI panel, 8 legend keys.
- **Creates up to seven international organizations in `on_start`** (`:155-357`): `foreign_league_balkan`
  (only if a Christian power holds Constantinople with ≥100 locations), `foreign_league_france`,
  `foreign_league_iberia`, `foreign_league_hre`, and `italian_league_1/2/3` — each by ranking
  `military_strength` in a region and calling `create_international_organization` with
  `add_country_to_international_organization` + `set_leader_country` in one block.
- **Keeps two sorted global lists of IOs** and re-sorts them monthly by `total_locations_owned`
  (`:368-379, 387-398`).
- **The tension meter** (§3c) with a 50-point threshold that adds a market demand
  (`demand:italian_wars_militarization`, `add_italian_wars_militarization_demands` at
  `scripted_effects/situation_effects.txt:1105-1138`) and a 100-point point of no return that pushes every
  league leader toward offensive war and then locks out for 10 years.
- **A dedicated reconciliation pass** (`reconcile_italian_wars_league_land`, 56 lines,
  `situation_effects.txt:1169-1224`) that repairs IO land ownership the on_actions missed.
- **A building** (`building_type:italian_administration_center`) with its own gold map stripe and legend row.
- **Verdict:** it is rich because the situation owns *economic* state (market demands), *organisational*
  state (7 IOs), *territorial* state (IO land ownership), and a meter, and all four interact.

### 8.3 `guelphs_and_ghibellines` — the richest by pure mechanism-per-line
- 499 situation lines, 18 events / 1,027 lines, 7 actions, and the **second-largest GUI panel in the game
  at 38,902 bytes** — larger than its own script.
- **The cleanest scored race in vanilla** (§3b): two IOs, each accumulating a share of Italy's total tax
  base every month, first to 1.0 wins. Nothing else in the game is scored this legibly.
- **Faction membership as the core verb**, with asymmetric commitment costs — 5 years to rejoin after
  joining, 2 years after leaving (`generic_actions/guelphs_and_ghibellines.txt:46-63`), and a ruler-trait
  pull (`gag_favors_guelphs` / `gag_favors_ghibellines`) that both gates `potential` and weights `ai_will_do`.
- **Two symmetric "sanction" actions** with 10-year cooldowns (`guelphs_sanction_emperor`,
  `ghibellines_sanction_pope`) plus two asymmetric support actions.
- **Three-way ending with a four-deep narrator fallback** (`:327-371`).
- **Verdict:** the design is small and legible — one meter, two sides, seven verbs — and it earns its
  richness from the *quality* of the meter, not from volume.

### 8.4 `red_turban_rebellions` — the richest by event content
- **46 events / 3,938 event lines — the most of any situation**, 437 situation lines, 10 actions.
- **A per-country signed allegiance scalar** (`rtr_yuan_allegiance`, −100..+100) that is the only
  bidirectional loyalty meter in the set, mutated by a scripted effect and read directly by the map
  (`:378-379`).
- **A scripted release engine**: `on_monthly` (`:88-137`) uses a `switch = { trigger = has_variable … }`
  over **fourteen** named tag/culture release flags (`rtr_release_tag_CTW`, `…_CHE`, `…_MNG` …), each
  firing a different event, at 20% per month, with a separate 1% generic-culture branch whose chance
  scales up as historical releases run out.
- **A five-deep succession search in `on_ended`** to decide who "China" is (§2.4).
- **Runtime empire reconstruction**: `rtr_recreate_middle_kingdom` (`situation_effects.txt:125-173`)
  creates the Middle Kingdom IO if absent, cancels every tusi subject, transfers leadership, sets celestial
  authority, researches `chi_bureaucracy_advance` and installs `six_boards_bureaucracy` with
  `set_entrenchment = 60 / set_maintenance = 0.50`, then cores all of East Asia and grants
  `casus_belli:cb_chinese_unification` against every capital in four Chinese regions
  (`rtr_core_all_of_china_effect` `:175-213`).
- **Verdict:** rich by breadth of *consequence* — it can end with a different country, a different
  international organization, a different bureaucracy and a different core map.

### 8.5 Honourable mention — `treaty_of_tordesillas`
Not the biggest (441 lines, 7 events) but **the most structurally instructive**: the only true
two-phase progress machine, the most actions (12), the only `custom_description`, the only situation
using both `on_ending` and `on_ended`, `monthly_spawn_chance = 0` with `can_start = { always = no }`,
`legend_key` with `limit`, and a `secondary_map_color` that lerps toward the default colour. If a modder
wants to learn the format's *shape*, this is the file to copy; if they want to learn its *scale*, copy
`rise_of_the_ottomans`.

---

## 9. ANTI-PATTERNS, DEAD CODE AND TRAPS

Ordered by how likely a modder is to copy them wrongly.

**1. Four scripted triggers written for `italian_wars` and never referenced.**
`italian_wars_end_requirements` (`scripted_triggers/situation_triggers.txt:410-432`),
`is_member_of_any_league` (`:396-408`), `has_foreign_league_won_the_italian_wars` (`:438-471`),
`has_italian_league_won_the_italian_wars` (`:473-506`). A full-tree grep finds **zero call sites** in
`in_game/` — the only other hits are localisation for `is_member_of_any_league_tt` in eleven languages
(e.g. `main_menu/localization/english/situations_l_english.yml:771`). The situation inlines its own
`can_end` instead (`situations/italian_wars.txt:17-70`) — and the two versions **disagree**:
the dead trigger says `years_since_situation_start > 65`, the live one says `> 50`.
*Trap:* copying `italian_wars` as a template drags four dead triggers and a wrong number with it.

**2. `italian_wars`'s live `can_end` is redundant with itself.**
`situations/italian_wars.txt:18` requires `years_since_situation_start > 50` as an AND-ed precondition,
and then `:68` repeats `situation:italian_wars = { years_since_situation_start > 50 }` as one of the
OR-branches. The OR is therefore always satisfied once the AND is — every other branch is unreachable.
The situation ends at exactly 50 years regardless of who is winning.

**3. Dead `ordered_country_in_religion` block with an empty body.**
`situations/guelphs_and_ghibellines.txt:74-97` — a 24-line trigger set, `order_by = country_tax_base`,
`max = 1`, `check_range_bounds = no`, and then the block closes with no effect. Somebody's intent was
deleted and the scaffolding left behind. It costs a full religion iteration every time the situation starts.

**4. Duplicate list insertions in `guelphs_and_ghibellines`'s `on_start`.**
`:29` adds `international_organization:guelphs_io` to `guelphs_and_ghibellines_voters` once.
Then `:39-40`, **inside `every_country`**, adds `ghibellines_io` and `guelphs_io` again — once per
qualifying country. With N Italian countries the voters list holds `guelphs_io` N+1 times.

**5. `great_pestilence`'s `on_ended` uses AND where `black_death` uses OR.**
```
every_market_in_world = { limit = {
	location.continent = continent:america
	has_temporary_demand = demand:procure_remedies
	has_temporary_demand = demand:procure_remedies_no_liquor }
	remove_temporary_demand = … }
```
(`situations/great_pestilence.txt:133-141`) — a market with only one of the two demands is skipped
and keeps it forever. `situations/black_death.txt:195-210` does the same job correctly with an
`OR` limit and two guarded `if` blocks.

**6. `red_turban_rebellions`' tooltip and map_color disagree on existence checks.**
`map_color` guards correctly: `AND = { has_variable = rtr_yuan_allegiance  var:rtr_yuan_allegiance > 50 }`
(`:377-380`). The `tooltip` for the same state reads `var:rtr_yuan_allegiance >= 50` with **no
`has_variable` guard** (`:323`) and `var:rtr_yuan_allegiance < 0` (`:336`) — on a country that has never
had the variable, that is an unguarded read. The two also use different thresholds (`>= 50` vs `> 50`,
`< 0` vs `< -25`), so the tooltip and the colour can contradict each other on the same location.

**7. `on_start` runs *before* the activator's follow-up code.**
`in_game/common/diseases/bubonic_plague.txt:165-171` calls `activate_situation = situation:black_death`
and **then** sets `original_outbreak` on the situation. So black_death's `on_start` (`:41-66`) executes
while `var:original_outbreak` does not yet exist. It happens to be safe because `on_start` never touches
that variable — but `can_end` (`:11`), `visible` (`:24`), `on_monthly` (`:71`), `tooltip` (`:134`) and
`map_color` (`:222,229`) all do. *Trap:* any variable your activator sets after `activate_situation` is
unavailable in `on_start`. Set it before, or set it inside `on_start`.

**8. `colonial_revolution` can never end and cleans up nothing.**
`can_end = { always = no }` (`:17-19`) with `on_ended = { }` (`:132-134`). Once it starts, it is
permanent for the rest of the campaign, keeps polling `every_colonial_country` and
`every_colonial_overlord` every month forever, and its `on_ended` cleanup — if the situation ever were
ended by `end_situation` — would leave everything behind. It is also the only situation with **no
`legend_key` at all**, so its map mode has no legend.

**9. `war_of_religions`'s `can_end` is a lie told deliberately, and it is documented.**
`scripted_triggers/situation_triggers.txt:610-635` opens with
`#The entire trigger is always = no because we end the situation with the end_situation = … effect in the
peace treaty / the Westphalia event` and then ships two `custom_tooltip` branches wrapping `always = no`
purely so the UI can *display* end conditions that the trigger will never satisfy. This is a legitimate
technique (externally-ended situation with informative tooltips) but it looks like a bug on first read.

**10. The `readme.txt` omits five shipping keys.** §0. A modder reading only the readme will never
discover `hint_tag` (which every single vanilla situation has, and without which the situation gets no
alert entry), `legend_key`, `is_data_map`, or `content_trigger`.

**11. `sengoku` has no `tooltip` block.** `situations/sengoku.txt` defines `map_color` (`:335`) and a
`legend_key` (`:354`) but no `tooltip` — so hovering a location in the Sengoku map mode says nothing.
Every other situation has one. Likely an oversight; do not copy `sengoku` as a map-mode template.

**12. `columbian_exchange` ships `tooltip = { }` empty** (`:183-184`) — the block exists but is a no-op.

**13. Massive copy-paste in the ranking blocks.** `sengoku.txt:58-252` repeats a 40-line
`ordered_international_organization_member` block five times with only `position` and the variable name
changed — and then `scripted_effects/situation_effects.txt:869-1073` repeats the *same five blocks* again
for the monthly refresh. That is ~400 lines of duplicated `order_by`. `rise_of_the_ottomans` has the same
problem at three copies × two sites. Any tuning change to the ordering formula must be made in ten places.
A modder should factor this into one parameterised scripted effect from the start.

**14. Two different "has this situation happened" mechanisms coexist.**
The engine's `situation_has_ended` (`triggers.log:10272-10276`) and the script-side
`set_situation_end_flag_effect` / `had_situation_trigger` pair
(`scripted_effects/global_effects.txt:242-248`, `scripted_triggers/situation_triggers.txt:33-39`).
Only **one** situation — black_death (`:144`) — calls the setter, so `had_situation_trigger` returns false
for the other 21 no matter what happened. Use the engine trigger unless you specifically need a
tooltip-able custom description.

**15. `western_schism` declares `resolution` but no `voters`; `guelphs_and_ghibellines` declares `voters`
but no `resolution`; `council_of_trent` declares `voters` and an IO type but no `resolution`.**
The three keys are independent and none implies another. `western_schism`'s eligibility comes from
`country_has_special_status = { type = special_status:curia … }` inside the resolution's `can_vote`
(`resolutions/western_schism.txt:12-25`); `council_of_trent` piggybacks on `resolution:policy_vote`
belonging to the Catholic Church IO and only uses its `voters` list to drive the map colour
(`situations/council_of_trent.txt:210-235`). *Trap:* declaring `voters` does not create a vote.

**16. Resolution recipients differ by design and it is not obvious.**
`fall_of_delhi` and `nanbokuchou` propose with `recipient = situation:<key>`
(`situations/fall_of_delhi.txt:103-108`, `situations/nanbokuchou.txt:29-34`) — the situation *is* the
voting body. `council_of_trent` and `western_schism` route everything through
`international_organization:catholic_church` instead. Both patterns are supported
(`triggers.log` lists the resolution family as `**Supported Scopes**: international_organization, situation`),
but the scripted effects that read votes must match: `council_of_trent_vote_effect`
(`situation_effects.txt:641-666`) checks `scope:recipient = international_organization:catholic_church`,
while `nanbokuchou_change_sides_effect` (`:219-255`) calls `situation:nanbokuchou = { set_vote = … }`.

**17. `prev` inside `map_color` means "the location", not "the situation".**
`rise_of_the_ottomans.txt:490` writes `situation:rise_of_the_ottomans.var:strongest_beylik_variable = prev.owner`
inside `map_color` where root is already the location — `prev` there resolves through the surrounding
`if/limit`, which are transparent. Two lines away the same file writes `owner` bare
(`:418` `situation:….var:strongest_beylik_variable = owner`). Both work; the inconsistency is a trap
if copied into a differently-nested block.

**18. `italian_wars` `on_ended` calls `destroy_all_italian_leagues` but `war_of_religions` needs a
country scope to destroy its IOs.**
`situations/war_of_religions.txt:597-600` wraps the destruction in `random_country = { destroy_international_organization = … }`
— an arbitrary country picked purely to provide a scope. That is the attested workaround; it is not
obvious from the effect docs.

---

## 10. WHAT THIS MEANS FOR A NEW SITUATION (design checklist derived from the corpus)

Minimum viable (matches the thinnest vanilla shipping situation, `little_ice_age` — 233 lines):
`monthly_spawn_chance` + `hint_tag` + `can_start` + `can_end` + `visible` + `on_start` + `on_monthly` +
`on_ended` + `tooltip` + `map_color` + ≥1 `legend_key`, plus a `scripted_hints` entry, plus a
`gui/panels/situation/<key>.gui`, plus loc.

To reach HYW/G&G class, the corpus says you additionally need:
1. **A meter** — one situation variable with a visible target (progress to 1.0, tension to 100, debates to 5).
   Without it the situation is a themed event pack.
2. **Rosters as global variable lists**, built in `on_start`, pruned and re-sorted in `on_monthly`.
3. **6-12 actions** whose price is a currency thematically tied to the situation, cooldowns of 2-10 years,
   and at least two whose effect writes into the meter.
4. **A weighted no-op monthly roll** in the 1-5% band per country (35% only for plague), with per-branch
   `trigger` gates, and a hand-rolled cooldown mechanism (`can_fire_situation_event` is the cleanest).
5. **Two or three genuinely different endings**, each with its own event fan-out and a permanent global
   variable recording which happened.
6. **A `secondary_map_color`** carrying an orthogonal fact (alliance vs allegiance, a building, a declared
   ambition) — this is what makes the map mode worth opening twice.
7. **on_action hooks** for the state the monthly tick cannot catch (annexation, war declaration, ownership
   change), plus a monthly reconciliation pass that assumes those hooks missed something.
8. **`on_ended` that removes everything** — every modifier on every country, every location modifier
   worldwide, every variable, every list — because nothing is cleaned up for you.
