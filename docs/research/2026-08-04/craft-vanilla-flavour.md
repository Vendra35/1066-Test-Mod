# CRAFT STUDY — Vanilla EU5 Situation Flavour

Read-only study of `E:\SteamLibrary\steamapps\common\Europa Universalis V\game`.
All paths below are relative to that root unless stated. Nothing was written to any
game or mod directory.

**Citation discipline.** Every structural claim carries `file:line` or a measured
count produced by a script over the named directory. Where a number is a *derived
estimate* (e.g. "events per historical year") the derivation is stated and the
historical span is flagged as an editorial reference, not a scripted value.
Nothing in the FORBIDDEN-from-memory categories (GUI block names, loc key shapes,
scopes, enums) is stated except as a direct quote from a file I opened.

---

## 0. The corpus, and the first correction

The prompt named `in_game\events\situations\` (25 files) and
`in_game\gui\panels\situation\` (24 files) as the corpus. Those are two of **four**
trees that jointly produce situation flavour. The other two carry more of the
machinery than the event files do, and a study that stops at the event files
would misread the architecture completely:

| Tree | Files | What it holds |
|---|---|---|
| `in_game/common/situations/` | 23 defs + `readme.txt` | the situation itself: lifecycle hooks, **the event dispatcher**, map colours, map tooltips |
| `in_game/events/situations/` | 25 | the 456 event bodies |
| `in_game/gui/panels/situation/` | 23 `.gui` + `readme.txt` | the panel |
| `in_game/common/generic_actions/` | ~22 situation-named files among 100+ | the player's clickable actions inside the panel |

Plus `in_game/common/scriptable_hints/scripted_hints.txt` (92 hints, of which the
situation ones), and four localization files/dirs.

**The single most important structural fact:** the event *files* contain almost no
scheduling. Scheduling lives in the situation definition. Measured
(`in_game/common/situations/*.txt` vs `in_game/events/situations/*.txt`):

```
firing verbs in in_game/common/situations/*.txt : 303 trigger_event_non_silently + 10 trigger_event_silently
firing verbs in in_game/events/situations/*.txt :  72 trigger_event_non_silently + 62 trigger_event_silently
```

The situation definition is the metronome; the event file is the score.

### 0.1 `readme.txt`, `in_game/common/situations/readme.txt` — verbatim

```
# Situations
#
#
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

Note the giveaway in line 5: `monthly_spawn_chance` is documented as "how likely
the **disease** is to spawn" — the situation system grew out of the disease
system, and the readme was never updated. It is in fact the per-month chance the
situation itself spawns. Values, all from
`main_menu/common/script_values/default_values.txt:1205-1212`:

```
monthly_spawn_chance_very_low       = 0.01
monthly_spawn_chance_low            = 0.02
monthly_spawn_chance_high           = 0.04
monthly_spawn_chance_ultimate       = 0.1
monthly_spawn_chance_ultimate_high  = 0.5
monthly_spawn_chance_unique         = 1
```

18 of the 23 situations use `monthly_spawn_chance_unique` (= 1, fires the first
month `can_start` passes). `treaty_of_tordesillas.txt:2` uses a literal
`monthly_spawn_chance = 0` — it is started by script from elsewhere, never by the
spawner.

### 0.2 `readme.txt`, `in_game/gui/panels/situation/readme.txt` — verbatim (all 5 lines)

```
# If you want to create a situation in the UI:

# 1. Check the common.gui file to see the different building blocks that can be used to create a situation.
# 2. You should create a new file in the situations folder with the name of the situation.
# 3. Your new created file should have the same structure as the other situation files. Specially using the type situation_panel.
# Recommendation: Use as a base layout a situation that has similar building blocks as yours. A good situation to take a look right now is the rise_of_the_ottomans
```

Paradox's own recommended template is `rise_of_the_ottomans.gui` (264 lines).
That is the file to copy.

### 0.3 Encoding, measured

| Tree | BOM |
|---|---|
| `in_game/events/situations/*.txt` | 25/25 **with** BOM |
| `in_game/common/situations/*.txt` | 23/23 **with** BOM |
| `in_game/gui/panels/situation/*.gui` | 0/23 with BOM (all BOM-free) |

Consistent with the project's existing rules; no new exception found here.

---

## 1. EVENT STACKS, MEASURED

### 1.1 Global shape

456 events total across the 25 files (455 `type = country_event`, 1
`type = location_event`). Field census, taken at depth-1 (`^\t<key> = `) across
all 25 files:

```
775 option            456 outcome          453 type / title / desc
452 category          364 immediate        260 image
156 trigger           149 illustration_tags 71 fire_only_once
 53 major              50 after             48 historical_info
 47 major_trigger      14 hide_portraits    13 dynamic_historical_event
  3 weight_multiplier
```

Category census: `category = situation_event` 452, `estate` 5, `same_religion` 2,
`religious` 1. Outcome census: `neutral` 445, `negative` 7, `positive` 4 — i.e.
Paradox effectively does not use the outcome colouring on situation events.

### 1.2 The hidden/player-facing split — the answer is not what the field names suggest

**Zero of the 456 events carry `hidden = yes`.** Every event in the corpus is a
player-facing popup. The hidden machinery is somewhere else, in two places:

1. `hidden_effect = { … }` blocks *inside* player-facing events —
   **131 uses** across `in_game/events/situations/*.txt`, only **4** in
   `in_game/common/situations/*.txt`. The idiom is: show the player a tooltipped
   consequence with `custom_tooltip`, then do the real bookkeeping invisibly.
   Canonical shape, `hundred_years_war.txt:478-482`:
   ```
   c:ENG = { trigger_event_silently = {  id = hundred_years_war.201 days = { 3 5 } } }
   hidden_effect = {
       c:ENG = {
           set_variable = {
   ```
2. The situation `on_monthly` block, which is pure machinery and never shows.
   `guelphs_and_ghibellines.txt:101` opens its entire monthly tick with
   `hidden_effect = {` and spends ~100 lines summing tax bases into
   `gag_total_tax`, `guelphs_total_tax`, `ghibellines_total_tax` before any event
   fires.

**Do not confuse `trigger_event_silently` with "hidden".** From the project's own
authority, `docs/EU5-Vanilla-Script-Docs/effects.log:10574-10584`:

```
## trigger_event_non_silently
triggers an event or on_action, but shows the name of the event
trigger_event_non_silently = { id = X days/months/years = Y } (for events)
**Supported Scopes**: none

## trigger_event_silently
triggers an event or on_action
trigger_event = { id = X days/months/years = Y } (for events)
…
```

The difference is whether the *effect's tooltip* names the event, not whether the
event appears. Both produce a popup. Vanilla situations use `non_silently`
overwhelmingly in the dispatcher (303 vs 10) and mix them roughly evenly inside
event options (72 vs 62) — the pattern being: name the event when the player
should be able to see in a tooltip what they are about to cause; hide the name
when the chain should be a surprise.

### 1.3 Firing idioms — the five that exist

**(a) `on_start` broadcast.** Everyone who can see it gets an intro event.
`hundred_years_war.txt` (`in_game/common/situations/`) lines 40-63: every country
with a capital in `sub_continent:western_europe` gets `hundred_years_war.1`,
England gets `.2`, France gets `.3`, and both get
`add_country_modifier = { modifier = hundred_years_war_impact years = -1 mode = add }`.
Per-situation `on_start` event counts are in the table at §1.6.

**(b) `on_monthly` weighted `random_list`.** The workhorse.
`hundred_years_war.txt:66-70` and `:71-142`:
```
on_monthly = {
    random_list = {
        1 = { c:ENG = { trigger_event_non_silently = hundred_years_war.211 } }
        1 = { c:FRA = { trigger_event_non_silently = hundred_years_war.211 } }
        99 = {}
    }
    custom_tooltip = {
        text = hundred_years_war_monthly
        random_list = {
            20 = { trigger = { … } c:ENG = { trigger_event_non_silently = hundred_years_war.10 } }
            20 = { … hundred_years_war.11 }
            20 = { … hundred_years_war.20 }
            20 = { … hundred_years_war.21 }
            200 = {}
        }
    }
}
```
Two things worth stealing: the empty-weight idler (`99 = {}`, `200 = {}`) that
sets the tempo, and the `custom_tooltip = { text = hundred_years_war_monthly … }`
wrapper — it makes the *whole monthly roll* legible to the player in the panel as
one loc string (`situations_l_english.yml:372`:
`hundred_years_war_monthly: "If there is [peace|e], there is a chance of either side restarting the conflict."`).

**(c) `dynamic_historical_event` — the date-window self-scheduler.** This is the
single most transferable idiom for a 1066 mod and it is *not* documented in
`effects.log` (I checked: no entry). An event carries its own schedule:
```
fire_only_once = yes
dynamic_historical_event = {
    tag = FRA
    from = 1337.1.1
    to = 1342.1.1
    monthly_chance = 100
}
```
(`hundred_years_war.txt:451-457`.) All 13 uses inside the situation corpus:

```
fall_of_delhi.txt:363          tag = DLH from = 1300.1.1 to = 1345.1.1 monthly_chance = 25
fall_of_delhi.txt:1618         tag = DLH from = 1340.1.1 to = 1375.1.1 monthly_chance = 1
hundred_years_war.txt:452      tag = FRA from = 1337.1.1 to = 1342.1.1 monthly_chance = 100
hundred_years_war.txt:524      tag = ENG from = 1337.1.1 to = 1342.1.1 monthly_chance = 100
hundred_years_war.txt:633      tag = FRA from = 1337.1.1 to = 1342.1.1 monthly_chance = 100
hundred_years_war.txt:724      tag = FRA from = 1337.1.1 to = 1342.1.1 monthly_chance = 100
hundred_years_war.txt:831      tag = ENG from = 1337.6.1 to = 1431.1.1 monthly_chance = 80
hundred_years_war.txt:943      tag = ENG from = 1339.1.1 to = 1431.1.1 monthly_chance = 100
hundred_years_war.txt:2567     tag = NRM from = 1337.1.1 to = 1375.1.1 monthly_chance = 100
hundred_years_war.txt:2635     tag = FLA from = 1337.1.1 to = 1375.1.1 monthly_chance = 100
hussite_wars.txt:26            tag = BOH from = 1400.1.1 to = 1480.1.1 monthly_chance = 3
hussite_wars.txt:465           tag = BOH from = 1380.1.1 to = 1450.1.1 monthly_chance = 5
rise_of_the_ottomans.txt:2714  tag = TUR from = 1337.1.1 to = 1375.1.1 monthly_chance = 10
```

Scope of the mechanism in vanilla as a whole: **3182 `dynamic_historical_event`
blocks parsed across `in_game/events/**/*.txt`**, of which 159 files in
`in_game/events/DHE/`. Key census inside those 3182 blocks:
`tag` 3574 (blocks may list several), `monthly_chance` 3160, `from` 3159,
`to` 3159, plus rare `add_area_preference` 26, `immediate` 18, `trigger` 4.
So the shape is essentially fixed: tag + window + monthly chance.

**(d) chained `trigger_event_*` from an option or `immediate`.** 107 event→event
edges from 78 source events. Almost always with a short delay:
```
days = { 5 15 }  ×15      days = { 3 7 }   ×4
days = { 60 90 } ×3       days = { 3 5 }   ×3
days = { 20 60 } ×2       days = { 10 30 } ×2
days = { 500 1000 } ×1    days = { 180 365 } ×1   (…and 6 more one-offs)
```
The 3-to-15-day delay is the house style: the reply arrives as a separate popup a
few days later, so the exchange reads as correspondence rather than a dialogue
box. `hundred_years_war.txt:478`:
`c:ENG = { trigger_event_silently = {  id = hundred_years_war.201 days = { 3 5 } } }`.

**(e) `fire_only_once = yes`** — 71 uses. Combined with `set_variable` cooldowns
inside `immediate`, e.g. `black_death.txt:1319` `NOT = { has_variable = bd1013_cd }`
in the trigger and `black_death.txt:1326` `set_variable = bd1013_cd` in `immediate`.

**No `mean_time_to_happen` anywhere in the corpus.** EU5 situations do not use
MTTH; the weighted `random_list` in `on_monthly` replaces it entirely.

### 1.4 Chain depth — shallower than expected

Longest event→event chain in the entire corpus: **3 hops**.
```
reformation.17 -> reformation.18 -> reformation.19 -> reformation.21
```
107 edges from 78 events; 378 of the 456 events are chain terminals. Paradox does
**not** build long branching event trees here. Depth comes from the panel and the
actions, not from event chains. This is a load-bearing observation for anyone
budgeting a situation: a 30-event situation is 30 mostly-independent beats plus a
handful of two-beat exchanges, not a tree.

### 1.5 Where each situation's events are actually fired from

Traced by scanning all `in_game/**` and `main_menu/**` `.txt`/`.gui` for
`trigger_event_(non_)?silently = <id>`:

```
file                          events  primary dispatchers (count of call sites)
D008_reformation.txt              5   situations/D008_reformation 4, generic_actions/D008_lutheran 1
black_death.txt                  30   situations/black_death 29, diseases/bubonic_plague 1
colonial_revolution.txt          18   situations/colonial_revolution 20, generic_actions/colonial_revolution 1
columbian_exchange.txt            1   situations/columbian_exchange 4
council_of_trent.txt              5   situations/council_of_trent 5
diseases.txt                      1   diseases/{influenza,measles,smallpox,typhus} 1 each
fall_of_delhi.txt                22   situations/fall_of_delhi 19, on_action/_hardcoded 2, disasters/dissolution_of_delhi 1
golden_age_of_piracy.txt         13   situations/golden_age_of_piracy 10, generic_actions/golden_age_of_piracy 2
great_pestilence.txt              6   situations/great_pestilence 5, diseases/great_pestilence 1
guelphs_and_ghibellines.txt      18   situations/guelphs_and_ghibellines 23, generic_actions/… 2, on_action/_hardcoded 1
hundred_years_war.txt            33   situations/hundred_years_war 22, generic_actions/hundred_years_war 12, DHE/flavor_ENG 1
hussite_wars.txt                 10   situations/hussite_wars 13
italian_wars.txt                 20   situations/italian_wars 30, scripted_effects/international_organization_effects 8, generic_actions 2
little_ice_age.txt               22   situations/little_ice_age 21
movements.txt                     2   movements/hellenism_religion_movement 1, movements/roman_culture_movement 1
nanbokuchou.txt                   9   situations/nanbokuchou 10, generic_actions/nanbokuchou 1
red_turban_rebellions.txt        46   situations/red_turban_rebellions 65, scripted_effects/on_action_effects 1
reformation.txt                  18   situations/reformation 16, movements/{calvinism,lutheranism}_movement 1 each
rise_of_the_ottomans.txt         42   situations/rise_of_the_ottomans 27, building_types/unique_buildings 8, generic_actions 6, on_action/_hardcoded 4
rise_of_timur.txt                34   situations/rise_of_timur 29, on_action/_hardcoded 3, scripted_effects/situation_effects 2, formable_countries 1
sengoku.txt                      23   situations/sengoku 18, generic_actions/sengoku 8
the_revolution.txt               12   situations/the_revolution 8, generic_actions/the_revolution 3
treaty_of_tordesillas.txt         7   generic_actions/treaty_of_tordesillas 4, situations/treaty_of_tordesillas 4, on_action/_hardcoded 3, colonization/colonial_charter 1
war_of_religions.txt             31   situations/war_of_religions 27, on_action/country_monthly 2
western_schism.txt               27   situations/western_schism 30, resolutions/western_schism 3, generic_actions/western_schism 2
```

The recurring pair is `common/situations/<name>.txt` + `common/generic_actions/<name>.txt`.
The second file is the player's agency and it is *large*: `generic_actions/black_death.txt`
is 1137 lines / 17 actions; `generic_actions/italian_wars.txt` 1785 lines / 9;
`generic_actions/hundred_years_war.txt` 1763 lines / 11;
`generic_actions/rise_of_the_ottomans.txt` 1162 lines / 7.

### 1.6 Per-situation table

`ev` = event bodies in `in_game/events/situations/<file>`; `hid` = events with
`hidden = yes` (always 0); `st/mo/end` = `trigger_event_*` call sites inside the
situation definition's `on_start` / `on_monthly` / `on_ending`+`on_ended`;
`opt` = total `option` blocks; `img` = events carrying `image = `;
`hinfo` = events carrying `historical_info = `.

| situation file | ev | hid | st | mo | end | opt | img | hinfo | dominant firing idiom |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| black_death | 30 | 0 | 1 | 27 | 1 | 66 | 30 | 0 | flat 27-way monthly `random_list` |
| colonial_revolution | 18 | 0 | 2 | 10 | 0 | 33 | 15 | 0 | monthly `random_list` |
| columbian_exchange | 1 | 0 | 2 | 2 | 0 | 1 | 1 | 0 | on_start/monthly, panel-carried |
| council_of_trent | 5 | 0 | 3 | 1 | 1 | 9 | 3 | 0 | resolution-driven (`voters =`) |
| D008_reformation | 5 | 0 | — | — | — | 8 | 0 | 5 | delayed block `trigger_event = {…}` ×4 |
| diseases | 1 | 0 | — | — | — | 1 | 1 | 0 | fired from 4 disease files |
| fall_of_delhi | 22 | 0 | 2 | 10 | 4 | 34 | 18 | 2 | monthly + 2× `dynamic_historical_event` |
| golden_age_of_piracy | 13 | 0 | 1 | 5 | 2 | 22 | 3 | 7 | monthly + actions |
| great_pestilence | 6 | 0 | 0 | 5 | 1 | 14 | 7 | 1 | monthly, disease-gated |
| guelphs_and_ghibellines | 18 | 0 | 3 | 3 | 10 | 29 | 8 | 0 | **on_ended-heavy** (10 endgame events) |
| hundred_years_war | 33 | 0 | 3 | 6 | 4 | 67 | 33 | 5 | monthly `random_list` + 8 DHE + 12 action calls |
| hussite_wars | 10 | 0 | 2 | 2 | 3 | 25 | 10 | 2 | 2× DHE (`monthly_chance = 3` and `5`) |
| italian_wars | 20 | 0 | 8 | 20 | 1 | 38 | 20 | 2 | tension thresholds + IO effects |
| little_ice_age | 22 | 0 | 1 | 19 | 1 | 30 | 22 | 5 | monthly `random_list` |
| movements | 2 | 0 | — | — | — | 4 | 0 | 0 | fired from `movements/` |
| nanbokuchou | 9 | 0 | 1 | 6 | 1 | 18 | 9 | 0 | monthly + resolution |
| red_turban_rebellions | 46 | 0 | 2 | 24 | 4 | 82 | 3 | 0 | monthly, 30 delayed-block calls |
| reformation | 18 | 0 | 1 | 15 | 0 | 25 | 1 | 0 | monthly + movement files |
| rise_of_the_ottomans | 42 | 0 | 2 | 9 | 5 | 57 | 7 | **12** | monthly + building + action + hardcoded on_action |
| rise_of_timur | 34 | 0 | 2 | 11 | 2 | 46 | 3 | 2 | monthly + `flag_situation_event` timeline |
| sengoku | 23 | 0 | 1 | 3 | 1 | 33 | 23 | 0 | **action-driven** (8 of 18 calls from actions) |
| the_revolution | 12 | 0 | 1 | 5 | 1 | 20 | 6 | 2 | monthly + actions |
| treaty_of_tordesillas | 7 | 0 | 0 | 1 | 1 | 20 | 7 | 2 | **action-driven**, `monthly_spawn_chance = 0` |
| war_of_religions | 31 | 0 | 3 | 20 | 0 | 51 | 3 | 0 | monthly `random_list` |
| western_schism | 27 | 0 | 3 | 21 | 1 | 42 | 27 | 1 | monthly + resolution voting |

### 1.7 Flavour density — events per game-year of historical span

The situations do not carry a scripted duration, so "span" below is the
**editorial historical span** of the referenced episode (from the situation's own
`historical_info`/desc loc where present, else the standard dates), and the
density is `ev / span`. Treat the density column as an order-of-magnitude
budgeting figure, not a measured game value. Scripted start gates are quoted
where they exist.

| situation | scripted start gate (`can_start`) | historical span used | yrs | ev | ev/yr |
|---|---|---:|---:|---:|---:|
| black_death | (disease-driven; `monthly_spawn_chance_unique`) | 1346–1353 | 7 | 30 | **4.3** |
| red_turban_rebellions | `current_year > 1350` | 1351–1368 | 17 | 46 | **2.7** |
| war_of_religions | `current_year >= 1590` | 1618–1648 | 30 | 31 | 1.0 |
| rise_of_timur | — | 1370–1405 | 35 | 34 | 1.0 |
| little_ice_age | `current_year >= 1645` | 1645–1715 | 70 | 22 | 0.31 |
| western_schism | `current_date > 1360.1.1` `< 1402.1.1` | 1378–1417 | 39 | 27 | 0.69 |
| hussite_wars | (DHE 1400–1480) | 1419–1434 | 15 | 10 | 0.67 |
| fall_of_delhi | (DHE 1300–1345) | 1335–1370 | 35 | 22 | 0.63 |
| reformation | `current_year >= 1510` | 1517–1555 | 38 | 18 | 0.47 |
| golden_age_of_piracy | — | 1690–1726 | 36 | 13 | 0.36 |
| rise_of_the_ottomans | `current_date > 1337.4.1` `< 1350` | 1337–1453 | 116 | 42 | 0.36 |
| italian_wars | `current_year > 1450` (auto from 1496) | 1494–1559 | 65 | 20 | 0.31 |
| hundred_years_war | `current_date > 1337.5.1` | 1337–1453 | 116 | 33 | 0.28 |
| council_of_trent | `current_year >= 1530`; window `1545`–`1563` | 1545–1563 | 18 | 5 | 0.28 |
| nanbokuchou | `current_date > 1336.1.1` | 1336–1392 | 56 | 9 | 0.16 |
| sengoku | `current_year >= 1400` | 1467–1615 | 148 | 23 | 0.16 |
| guelphs_and_ghibellines | `current_date > 1337.4.1` | (open-ended) | — | 18 | — |
| the_revolution | — | 1789–1799 | 10 | 12 | 1.2 |
| colonial_revolution | — | 1775–1825 | 50 | 18 | 0.36 |
| treaty_of_tordesillas | `monthly_spawn_chance = 0` | 1494 (point event) | — | 7 | — |

**The rule of thumb this yields:** a short, catastrophic, everyone-participates
situation earns 3–5 events per game-year; a century-long two-power rivalry earns
0.3. The absolute event count clusters far more tightly than the span does — 18
to 46 events is the normal band regardless of whether the situation covers 7
years or 148. Only `black_death` (30 events / 7 years) and
`red_turban_rebellions` (46 / 17) are genuinely dense, and both of those are
situations where the player is *in* the crisis every month rather than watching
it.

---

## 2. OPTION ARCHITECTURE

### 2.1 Choice-count distribution (455 events measured)

```
0 options →   3 events   (0.7 %)
1 option  → 200 events   (44 %)
2 options → 198 events   (44 %)
3 options →  42 events   (9 %)
4 options →   9 events   (2 %)
5 options →   2 events
7 options →   1 event    (hussite_wars, max in corpus)
```

**88 % of situation events have one or two options.** A one-option event is an
announcement ("This was expected."). A two-option event is a fork. Three or more
is rare and reserved for the moment of the situation. Per-file maxima:
`hussite_wars` 7, `nanbokuchou` 5, `treaty_of_tordesillas` 5, everything else ≤4.

### 2.2 Option-level field census (all `^\t\t<key> = `)

```
778 name              373 if            225 custom_tooltip
137 trigger           101 set_variable   98 hidden_effect
 94 add_stability      83 ai_chance      80 add_prestige
 75 else               65 ai_will_select 63 change_societal_value
 62 add_estate_satisfaction  60 add_government_power
 56 show_as_tooltip    55 remove_variable  50 save_scope_as
 45 first_valid        41 create_character  38 historical_option
 31 add_country_modifier  30 change_gold_effect
```

Note `custom_tooltip` (225) outnumbering nearly every actual effect. The house
style is: write the consequence in prose, then do it in a `hidden_effect`.
`show_as_tooltip` (56) is the companion — it previews an effect on another country
without executing it (`hundred_years_war.txt:1063-1064`:
`custom_tooltip = IF_THEY_ACCEPT` / `show_as_tooltip = {`).

### 2.3 `historical_option` — 38 uses, 8 files

```
red_turban_rebellions 11 | hundred_years_war 9 | rise_of_timur 8 | hussite_wars 5
fall_of_delhi 2 | nanbokuchou 1 | rise_of_the_ottomans 1 | the_revolution 1
```
Only the *railroad* situations use it. It sits on the option, directly under the
name, with no arguments (`hundred_years_war.txt:207-208`):
```
option = {
    name = hundred_years_war.20.a
    historical_option = yes
```
17 of the 25 files use it zero times. It is the marker for "this is what actually
happened", not a general-purpose field.

### 2.4 `ai_chance` vs `ai_will_select` — two different tools

83 `ai_chance`, 65 `ai_will_select`. Distribution of `ai_chance` by file:
`hundred_years_war` 34, `rise_of_the_ottomans` 12, `fall_of_delhi` 10,
`guelphs_and_ghibellines` 8, `italian_wars` 5, `colonial_revolution` 4,
`hussite_wars` 4, `nanbokuchou` 3, `the_revolution` 2, `rise_of_timur` 1.

Three observed shapes, ascending in sophistication:

*Flat:* `rise_of_the_ottomans.txt` — `ai_chance = { factor = 50 }` / `{ factor = 75 }` / `{ factor = 25 }`.

*Factor with modifiers:* `rise_of_the_ottomans.txt`
```
ai_chance = {
    factor = 50
    modifier = {
        factor = 10
        has_variable = more_likely_to_accept_vassalization_variable
    }
}
```

*Base with situational multipliers, `hundred_years_war.txt:1245-1268`* — the AI
weighs whether it can afford to pay:
```
ai_chance = {
    base = 50
    modifier = {
        factor = 10
        OR = {
            gold >= { value = monthly_income_total multiply = 12 }
            monthly_balance > { value = monthly_income_total divide = 2 }
        }
    }
    modifier = {
        factor = 0.25
        OR = { is_during_bankruptcy = yes  monthly_balance < -10  num_loans > 5 }
    }
}
```

`ai_will_select` is the *additive score* form and it carries `desc =` strings that
surface in the AI-reasoning tooltip. `hundred_years_war.txt:210-236` is the best
single example in the corpus and is worth copying wholesale (quoted in §2.7).

### 2.5 Priced options — the surprise

**Situation *events* almost never charge gold.** The whole corpus contains 30
`change_gold_effect` calls and 47 `add_gold`. `change_gold_effect` shapes:
```
scale = -3 ×5   scale = -2 ×4   scale = -6 ×3   scale = 5 ×3
scale = -4 ×3   scale = -1 ×2   scale = -6.00, -5.5, -5, 3, -1.5, 1 ×1 each
```
`change_gold_effect` is a scripted effect whose sibling is defined at
`in_game/common/scripted_effects/country_gold_effects.txt:50-64` — it scales off
`capital_wealth` and `country_economical_base`, so `scale = -3` is a *relative*
cost, not a flat 3 ducats. That is the right idiom for a mod spanning 276 years:
prices that stay meaningful.

The actual pricing lives on the **actions**, not the events.
`in_game/common/generic_actions/rise_of_the_ottomans.txt:18`:
`price = price:rto_press_claims_price`, resolved at
`in_game/common/prices/00_hardcoded.txt:964-984`:
```
rto_press_claims_price = { scaled_gold = 2 }
rto_create_uc_bey     = { gold = 100 }
succession_crisis_price = { prestige = 5 }
wotr_action_price     = { scaled_gold = 2  stability = 5 }
peasants_war_actions_price = { government_power = 10 }
```
So the currency vocabulary is `scaled_gold`, `gold`, `prestige`, `stability`,
`government_power` — and the *situation panel* is where the player spends. Events
give and take stability/prestige/government power as narrative consequence
(`add_stability` 94 uses at option level, `add_prestige` 80,
`add_government_power` 60, `change_societal_value` 63,
`add_estate_satisfaction` 62), while the panel actions are the priced ones.

### 2.6 Refusable railroads, and `is_ai` gating

The refusal is a plain second option with a low-key name and a real but bearable
cost. Measured examples (`main_menu/localization/english/events/situations/`):
```
hundred_years_war_events_l_english.yml:30   hundred_years_war.20.b: "Now is not the time"
hundred_years_war_events_l_english.yml:35   hundred_years_war.21.b: "Now is not the time"
hundred_years_war_events_l_english.yml:103  hundred_years_war.206.d: "Nevermind."
hussite_wars_events_l_english.yml:83        hussite_wars.3.b: "Let us not rush into action."
fall_of_delhi_events_l_english.yml:13       delhi_situation.2.c: "Let us not meddle for now..."
colonial_revolution_events_l_english.yml:91 colonial_revolution.1001.b: "No, we would not want their ideas of freedom spreading to us."
```
The cost of `hundred_years_war.20.b` is `add_prestige = prestige_mild_penalty` +
`add_truce_with = { target = c:FRA years = 2 }` (`hundred_years_war.txt:280-283`) —
i.e. the refusal *is honoured*, it just costs prestige and buys a two-year truce.
That is the shape a human-choice rule wants: the railroad postpones, it does not
force.

`is_ai` appears **24 times in the whole corpus**: `red_turban_rebellions` 22,
`hundred_years_war` 1, `golden_age_of_piracy` 1. The two singletons show both
directions:
- *Give the AI a shove the player does not need*, `hundred_years_war.txt:1455-1461`:
  ```
  scope:actor = {
      if = {
          limit = { is_ai = yes }
          add_country_modifier = { modifier = aggressive_planning years = 3 mode = replace }
  ```
- *Hide a player-only option from the AI*, `golden_age_of_piracy.txt:205-211`:
  ```
  option = {
      name = golden_age_of_piracy.110.b
      high_risk_option = yes
      trigger = { is_ai = no }	#Let's avoid weird potential issues...
      change_player = scope:pirate_tag_scope
  }
  ```
  `high_risk_option = yes` is a real option-level field (it has no entry in
  `effects.log`; it is an event-schema field, attested here in vanilla source).
  This is the "become the pirate republic" option — a player-only tag swap.

### 2.7 Four exemplary events, condensed skeletons

**(A) The AI-scored war decision — `hundred_years_war.20`, `hundred_years_war.txt:194-286`.**
The best `ai_will_select` in the corpus; note the `desc =` strings, which are what
the AI-reasoning tooltip shows.
```
hundred_years_war.20 = {                    # "England starts another phase"
    type = country_event
    category = situation_event
    title = hundred_years_war.20.title      # "It is Time for War"
    desc  = hundred_years_war.20.desc
    outcome = neutral
    image = "gfx/interface/illustrations/situation/hundred_years_war.dds"

    option = {                              # a: go
        name = hundred_years_war.20.a       # "And War it shall be!"
        historical_option = yes
        ai_will_select = {
            add = { value = 50                                   desc = BASE_VALUE }
            add = { value = 100 multiply = "relative_strength(c:FRA)" divide = 5
                                                                 desc = "RELATIVE_STRENGTH" }
            add = { value = modifier:aggressiveness_modifier
                    subtract = modifier:carefulness_modifier multiply = 50
                    desc = "aggressiveness modifier minus carefulness modifier" }
            add = { value = manpower_percentage multiply = 10    desc = "CURRENT_MANPOWER_TOOLTIP" }
            add = { value = army_size                            desc = "army_size" }
        }
        if = {
            limit = { NOT = { is_at_war_with = c:FRA } }
            leave_all_wars_with = c:FRA
            if   = { limit = { can_declare_legal_war_on = { target = c:FRA } }
                     declare_war_with_cb = { target = c:FRA type = casus_belli:cb_hundred_years_war } }
            else = { add_casus_belli = { target = c:FRA type = casus_belli:cb_hundred_years_war } }
        }
    }
    option = {                              # b: refuse, cheaply
        name = hundred_years_war.20.b       # "Now is not the time"
        ai_will_select = {
            add      = { value = 50 desc = BASE_VALUE }
            subtract = { value = 100 multiply = "relative_strength(c:FRA)" divide = 5 desc = "RELATIVE_STRENGTH" }
            subtract = { value = modifier:aggressiveness_modifier
                         subtract = modifier:carefulness_modifier multiply = 50
                         desc = "aggressiveness modifier minus carefulness modifier" }
        }
        add_prestige = prestige_mild_penalty
        add_truce_with = { target = c:FRA years = 2 }
    }
}
```

**(B) The broadcast with an audience filter — `hundred_years_war.207`, `hundred_years_war.txt:1156-1213`.**
`major = yes` + `major_trigger` is the "everyone who cares sees this" idiom (53 and
47 uses respectively). It defines *who* the event's importance applies to.
```
hundred_years_war.207 = {
    type = country_event
    category = situation_event
    title = hundred_years_war.207.title
    desc  = hundred_years_war.207.desc
    outcome = neutral
    image = "gfx/interface/illustrations/situation/hundred_years_war.dds"
    major = yes
    major_trigger = {
        OR = {
            tag = ENG
            tag = FRA
            is_subject_of = c:FRA
            is_subject_of = c:ENG
            has_mutual_scripted_relation = { type = relation_type:alliance target = c:ENG }
            has_mutual_scripted_relation = { type = relation_type:alliance target = c:FRA }
        }
    }
    immediate = {                                  # portrait casting
        c:FRA.ruler_or_regent ?= { save_scope_as = target_character1 }
        c:ENG.ruler_or_regent ?= { save_scope_as = target_character2 }
        scope:actor           =  { save_scope_as = target_asker }
    }
    option = {
        name = hundred_years_war.207.a             # "Let us end the senseless violence with a powerful decree!"
        ai_will_select = { value = 180 }
        add_government_power = government_power_extreme_bonus
        add_prestige = prestige_extreme_bonus
        if   = { limit = { scope:target_asker = c:FRA }
                 c:ENG = { trigger_event_non_silently = hundred_years_war.212 } }
        else = { c:FRA = { trigger_event_non_silently = hundred_years_war.212 } }
    }
    option = {
        name = hundred_years_war.207.b
        ai_will_select = { value = -60  add = root.stability }
        add_stability = stability_ultimate_penalty
    }
}
```

**(C) The culture-branched description — `great_pestilence.1`, `great_pestilence.txt:3-70`.**
The `first_valid` / `triggered_desc` pair is how one event says two different
things to two civilisations. This is the single most valuable pattern for a
world-spanning 1066 mod.
```
great_pestilence.1 = {                       # "Country gets infected"
    type = country_event
    category = situation_event
    title = great_pestilence.1.title
    desc = {
        first_valid = {
            triggered_desc = {
                trigger = { culture = { is_culture_native_american = yes } }
                desc = great_pestilence.1.desc
            }
            triggered_desc = { desc = great_pestilence.1.descB }
        }
    }
    outcome = neutral
    historical_info = columbian_exchange.1.historical_info      # <- cross-situation reuse, see §7
    image = "gfx/interface/illustrations/situation/great_pestilence.dds"

    immediate = {                             # anchor the event to a real infected location
        if = {
            limit = { country_type = pop }
            random_owned_nomad_pop = {
                limit = { location = { disease_presence = { disease = disease:great_pestilence value > 0 } } }
                location = { save_scope_as = diseased_location_scope }
            }
        }
        else = {
            random_owned_location = {
                limit = { disease_presence = { disease = disease:great_pestilence value > 0 } }
                save_scope_as = diseased_location_scope
            }
        }
    }
    option = {                                # the two sides of the same shock
        name = great_pestilence.1.a
        trigger = { culture = { is_culture_native_american = yes } }
        change_societal_value = { type = spiritualist_vs_humanist value = societal_value_minor_move_to_left }
        add_stability = stability_extreme_penalty
    }
    option = {
        name = great_pestilence.1.a2
        trigger = { NOT = { culture = { is_culture_native_american = yes } } }
        change_societal_value = { type = spiritualist_vs_humanist value = societal_value_tiny_move_to_left }
        add_stability = stability_weak_penalty
    }
}
```

**(D) The small, repeatable, location-anchored beat — `black_death.1013`, `black_death.txt:1309-1360`.**
This is what 27 of the Black Death's 30 events look like. Note the
per-country cooldown variable, the `random_owned_rural_location` anchor, the
`custom_tooltip` + `hidden_effect` pairing, and that neither option is "correct".
```
black_death.1013 = { # Village Stops Paying Taxes
    type = country_event
    category = situation_event
    title = black_death.1013.t
    desc  = black_death.1013.desc
    outcome = neutral
    image = "gfx/interface/illustrations/situation/black_death.dds"

    trigger = {
        NOT = { has_variable = bd1013_cd }
        country_has_disease = disease:bubonic_plague
        any_owned_rural_location = { disease_presence = { disease = disease:bubonic_plague value > 0.25 } }
        NOT = { has_country_modifier = peasants_estate_less_tax_burden }
    }
    immediate = {
        set_variable = bd1013_cd
        random_owned_rural_location = {
            limit = { disease_presence = { disease = disease:bubonic_plague value > 0.25 } }
            save_scope_as = target_location
        }
    }
    option = {                                   # a: collect anyway
        name = black_death.1013.a
        scope:target_location = {
            change_control = control_mild_bonus
            custom_tooltip = every_pop_25_satisfaction_loss_tt
            hidden_effect = { every_pop = { limit = { owner = root }
                                            add_pop_satisfaction = pop_satisfaction_extreme_penalty } }
        }
    }
    option = {                                   # b: forgive the taxes  ("No taxes for anyone suffering!")
        name = black_death.1013.b
        scope:target_location = {
            change_control = control_mild_penalty
            custom_tooltip = every_pop_10_satisfaction_gain_tt
            hidden_effect = { every_pop = { … add_pop_satisfaction … } }
        }
    }
}
```

---

## 3. GUI PANELS

### 3.1 The base type — `in_game/gui/panels/situation/common.gui`

One type is declared for the whole system (`common.gui:1-3`):
```
types SituationPanel
{
	type situation_panel = lateralview {
		name = "situation_panel"
```
It derives from `lateralview` and immediately overrides two of the parent's
blocks: `blockoverride "panel_header"` (`common.gui:6`) and
`blockoverride "panel_content"` (`common.gui:33`). Everything a situation panel
author touches is inside `panel_content`.

The `block` names `situation_panel` **declares** for its children, exact strings
with `common.gui` line numbers:

| block name | line | what it is |
|---|---:|---|
| `"situation_top_subheader_content"` | 47 | the whole 45px subheader strip |
| `"situation_header_left"` | 55 | left slot of the strip (`visible = no` by default) |
| `"situation_header_center"` | 66 | centre slot (empty, and the default content is commented out at 67-82) |
| `"situation_header_right"` | 94 | right slot (`visible = no` by default) |
| `"header_center_modifiers"` | 105 | overlay on the illustration band |
| `"situation_panel_image"` | 113 | the 220px illustration band |
| `"situation_extra_tabs_content"` | 182 | extra tab buttons next to "Breakdown" |
| `"situation_subheader_content"` | 190 | second subheader |
| `"situation_subheader_extra"` | 192 | inside it |
| `"situation_subheader_right"` | 220 | right slot of it |
| `"situation_panel_main_maximumsize"` | 234 | scrollarea sizing |
| `"situation_panel_main_content"` | 258 | **the card stack — the main body** |
| `"disaster_progressbar"` | 318 | the threshold bar (whole vbox is `visible = no` at 262) |
| `"situation_panel_main_content_bottom"` | 337 | cards below the action list |
| `"situation_main_content_extra"` | 344 | outside the scrollarea |
| `"situation_extra_tab_panels"` | 348 | the panels the extra tabs switch to |

Plus three templates at the bottom of the same file: `situations_actions`
(`common.gui:366`), `vote_countries` (`:392`), `vote_countries_list` (`:530`).

Two hard-wired behaviours worth knowing before designing a panel:

- **The illustration path is derived, not written.** `common.gui:113-117`:
  ```
  block "situation_panel_image" {
      background = {
          # gfx/interface/illustrations/situation/
          texture = "[GetSituationIllustration(SituationView.GetActiveSituation.GetSituation)]"
      }
  ```
  The comment gives the folder; the function does the lookup. A mod situation
  needs a `.dds` in `gfx/interface/illustrations/situation/` named for the
  situation key, and no GUI edit at all.
- **The action list is automatic.** `common.gui:332-335` unconditionally does
  `using = situations_actions`, and that template
  (`common.gui:366-390`) builds a `dynamicgridbox` over
  `datamodel = "[SituationView.GetActionGroups]"`, one `situation_card_actions`
  per group, header text `"[ActionGroup.GetName]"`. **Add a
  `generic_actions` entry with `type = situation` and it appears in the panel
  with zero GUI work.** That is where most of a panel's perceived richness comes
  from for free.
- **The end-conditions text is derived too.** Every panel that shows requirements
  reads `textcontext = "[SituationView.GetActiveSituation.GetSituation.GetEndConditions]"`
  (e.g. `hundred_years_war.gui:75`), which renders the `can_end` trigger. Writing
  `can_end` with `custom_tooltip` wrappers is therefore writing UI text.

### 3.2 Which blocks the 23 panels actually override

```
"situation_subheader_content"          21 panels   (20 of them as `{}` — i.e. deliberately blanked)
"situation_panel_main_content"         21
"situation_panel_image"                17
"situation_header_left"                12
"situation_header_right"               11
"situation_panel_main_content_bottom"  10
"situation_header_extra"                5   (4 of them commented out)
"situation_extra_tabs_content"          3
"situation_extra_tab_panels"            3
"situation_header_style"                3
"situation_top_subheader_content"       2
"situation_panel_main_maximumsize"      2
"situation_header_center"               1   (guelphs_and_ghibellines only)
"situation_main_content_extra"          1   (guelphs_and_ghibellines only)
"situation_subheader_right"             1
"situation_subheader_extra"             1
"situation_vote_resolution_actions"     1
```

**A minimal panel is three overrides.** The rest of the file is the card contents.

### 3.3 Anatomy — minimal: `the_revolution.gui` (133 lines, 24 blockoverrides)

Three overrides:
1. `blockoverride "situation_header_left"` (`:6-13`) — one `country_flag_small`
   with `datacontext = "[RevolutionaryTarget]"` and `visible = "[IsRevolutionaryTargetActive]"`.
2. `blockoverride "situation_panel_image"` (`:17-42`) — `using = one_country_header_template`
   (defined at `in_game/gui/country_header.gui:135`) with five sub-overrides:
   `"CountryContext"`, `"character_portrait_anchor"`,
   `"character_religion_visibility"`, `"character_name_maximumsize"`,
   `"country_header_extra"`.
3. `blockoverride "situation_panel_main_content"` (`:54-131`) — two cards:
   a `situation_card_expandable` for END_REQUIREMENTS, and a
   `horizontal_scroll_card` for the strongest rebel with a
   `progressbar` (`:112-116`) and a monthly-change readout.

The END_REQUIREMENTS card is boilerplate and **identical in nearly every panel**;
it is 10 blockoverrides and the only thing that changes is the hint key:
```
situation_card_expandable = {
    blockoverride "header_button_onclick" { onclick = "[LateralView.Vars.Toggle( 'requirements_toggled' )]" }
    blockoverride "header_text"  { text = "END_REQUIREMENTS" }
    blockoverride "header_icon"  { texture = "gfx/interface/icons/disasters/end_requirements_green.dds" }
    blockoverride "bottom_content" {
        TooltipRequirementsList = { textcontext = "[SituationView.GetActiveSituation.GetSituation.GetEndConditions]" }
    }
    blockoverride "visible_hint" {}
    blockoverride "onaction_hint" {
        action_tooltip = {
            title = "OPEN_HINT"
            on_action = "[OpenLateralViewWithParams('hints', 'selected_hint = hint_the_revolution')]"
        }
    }
    blockoverride "bottom_content_onclick"    { visible = "[LateralView.Vars.Exists( 'requirements_toggled' )]" }
    blockoverride "icon_replace_visible_yes"  { visible = "[LateralView.Vars.Exists( 'requirements_toggled' )]" }
    blockoverride "icon_replace_visible_not"  { visible = "[Not(LateralView.Vars.Exists( 'requirements_toggled' ))]" }
}
```
(`the_revolution.gui:56-87`; the same block with `'requirements_toggled'` and
`hint_hundred_years_war` at `hundred_years_war.gui:63-94`, with
`hint_black_death` at `black_death.gui:124-155`, with `hint_rise_of_the_ottomans`
at `rise_of_the_ottomans.gui:52-83`.) **The `onaction_hint` override is the wire
from the panel to the hint system** — this is where `hint_tag` in the situation
definition pays off.

### 3.4 Anatomy — the recommended base: `rise_of_the_ottomans.gui` (264 lines)

Three overrides, and it is the readme's suggested starting point.
- `"situation_panel_image"` (`:10-35`) — `one_country_header_template` pointed at
  a *variable*, not a tag:
  `datacontext = "[SituationView.GetActiveSituation.GetSituation.MakeScope.GetVariable('strongest_beylik_variable').GetCountry]"` (`:14`).
  This is the key move for a situation whose protagonist is not known at design time.
- `"situation_subheader_content"{}` (`:45`) — blanked.
- `"situation_panel_main_content"` (`:50-260`) — three cards:
  1. END_REQUIREMENTS boilerplate,
  2. a second `situation_card_expandable` whose `header_icon` is a
     `country_flag_small_plus` of the leader variable and whose `bottom_content`
     is a `text_multi` of `"STRONGEST_BEYLIK_BONUS_TOOLTIP"` (`:85-147`),
  3. a `situation_fancy_two_line_card` showing #2 and #3 by variable, each with a
     `ContextualTooltipType` containing a `TooltipStringPairList` **and** a
     `TooltipFlavorTextBlock` (`:123-127`, `:197-201`, `:250-254`).

`TooltipFlavorTextBlock` is the italic-voice tooltip widget. Its content in this
panel is `situations_l_english.yml:250`:
`ROTT_LEADER_COUNTRY_SCORE_FLAVOR_TT: "#italic Every month, the overall performance of the countries in the [ShowSituationNameWithNoTooltip('rise_of_the_ottomans')] [situation|e] is evaluated and the positions of the three most powerful ones are updated based on the new scores.#!"`
— i.e. the panel explains its own mechanics in the situation's voice.

### 3.5 Anatomy — two-protagonist: `hundred_years_war.gui` (255 lines)

Adds `blockoverride "situation_panel_main_content_bottom"`. The image band uses
`using = two_countries_header_template` (`:11`, defined at
`in_game/gui/country_header.gui:202`) with `"FirstCountryContext"` =
`[GetCountry('ENG')]` and `"SecondCountryContext"` = `[GetCountry('FRA')]`
(`:13-19`), and portraits anchored `bottom|left` / `bottom|right` (`:23-29`).

The bottom block (`:173-254`) is a `situation_side_cards` with two mirrored
scrollareas over
`datacontext = "[GetWillJoinCountryList(GetCountry('ENG').Self, GetCountry('FRA').Self)]"`
and `datamodel = "[WillJoinCountryList.GetJoinDefensive]"` (`:200`, `:206`),
`datamodel_wrap = 6`, `maxhorizontalslots = 6`, item = `country_flag_small`. So
the panel shows, live, who would join each side — a diplomatic map of the war
without a single event.

### 3.6 Anatomy — the richest: `guelphs_and_ghibellines.gui` (143 blockoverrides)

This is the only panel that overrides `"situation_header_center"` and
`"situation_main_content_extra"`, and one of three that adds a tab. What it has
that the minimal panels do not:

- **Its own `types` block** (`:1-122`), declaring `gag_faction_barchart_widget`
  (`:3`) and `gag_faction_member_row` (`:34`). A situation may ship custom widget
  types in its own panel file. `italian_wars.gui` does the same
  (`types ItalianWarsTypes { type tension_threshold_icon = widget {` at `:2-3`).
- **A `barchart` whose slices are countries.** `:7-31`:
  ```
  barchart = {
      block "bar_datamodel" { datamodel = "[GetUniqueInternationalOrganization('guelphs_io').GetMembers]" }
      item = {
          barslice = {
              texture = "gfx/interface/progressbars/progress_bar_whiteish.dds"
              color = "[Country.GetMapColor]"
              block "bar_slice_value" { value = "[Country.GetCountryGuelphsProgress]" }
          }
      }
      barslice_no_highlight = {
          color = { 0 0 0 1 }
          block "bar_remainder_value" {
              value = "[Subtract_float('(float)1.0', FixedPointToFloat(GetUniqueInternationalOrganization('guelphs_io').GetVariable('guelphs_progress')))]"
          }
      }
  }
  ```
  Each member country contributes a slice **in its own map colour**. This is the
  best single piece of information design in the situation system: you look at
  the bar and you see who is carrying the faction.
- **A two-sided race banner** with different textures per faction — `:351`
  `texture = "gfx/interface/component_decoration/situation/white_banner.dds"` and
  `:413` `"gfx/interface/component_decoration/situation/red_banner.dds"` with
  `mirror = horizontal`. The Guelph/Ghibelline white-and-red is literal.
- **An extra tab** — `blockoverride "situation_extra_tabs_content"` (`:506-…`)
  adds a `button_secondary_tab_alt` with `blockoverride "tab_text" { text = "SITUATION_MEMBERS" }`
  and `on_action = "[SituationView.Vars.Set( 'situation_tab', 'situation_members' )]"`;
  the corresponding panel goes in `"situation_extra_tab_panels"` (`:536`), and the
  member rows use `situation_member_country_row` with
  `blockoverride "situation_member_gp"`, `"situation_member_opinion"`,
  `"situation_member_extra_columns"` (`:764-766`).
- **Per-country monthly deltas in the row**, `:77`:
  `raw_text = "+[GagCountryItem.GetCountryProgressMonthly|G3%]"`.

### 3.7 The variable-read idiom — the one thing to memorise

Every panel reads situation state the same way. Two forms, both attested:

*From the active situation (used inside a situation panel):*
```
"[SituationView.GetActiveSituation.GetSituation.MakeScope.GetVariable('strongest_beylik_variable').GetCountry]"
```
(`rise_of_the_ottomans.gui:14`)

*From any situation by key (used in loc, and in panels for other situations):*
```
[GetSituationByKey('treaty_of_tordesillas').MakeScope.GetVariable('treaty_location').GetLocation.GetName]
```
(`situations_l_english.yml:58`)

Note `.MakeScope` sits between the situation and `.GetVariable`, and the
type-cast suffix (`.GetCountry`, `.GetLocation`, `.GetCharacter`, `.GetValue`,
`.GetCardinal`, `.GetDiseaseOutbreak`, `.GetPolicy`) comes after. Getting that
chain wrong produces an empty string, not an error.

Textures referenced by the panels, as an inventory of what already exists:
`"[SituationView.GetActiveSituation.GetIcon]"` (the situation's own icon, used
throughout), `gfx/interface/component_tiles/regular_banner.dds` (common.gui:124),
`gfx/interface/icons/disasters/end_requirements_green.dds` (every panel),
`gfx/interface/icons/map_subdivisons/location.dds` (black_death.gui:33),
`gfx/interface/icons/flat_icons/geopolitics/privateer.dds` (black_death.gui:102 —
used as the *deaths* icon), `gfx/interface/icons/outliner/categories/sieges.dds`
(black_death.gui:186), `gfx/interface/icons/rebels/fist.dds` (common.gui:283 etc.),
`gfx/interface/progressbars/progress_bar_whiteish.dds` (g&g:17),
`gfx/interface/component_decoration/situation/{white,red}_banner.dds` (g&g:351,413),
`gfx/interface/icons/international_organizations/{guelphs,ghibellines}_io.dds`,
`gfx/interface/icons/situations/guelphs_and_ghibellines.dds` (g&g:82),
`gfx/interface/component_tiles/square_highlight.dds` (common.gui:443),
`gfx/interface/icons/laws/resolutions/law_voting.dds` (common.gui:460),
`gfx/interface/pie_charts/pie_chart_alpha_80.dds` (common.gui:591, commented out).

Card templates live outside the situation folder, at `in_game/gui/shared/cards.gui`:
`situation_card_actions` (`:2318`), `situation_card_expandable` (`:2631`),
`situation_side_cards` (`:2841`), `situation_fancy_two_line_card` (`:3103`).
Header templates at `in_game/gui/country_header.gui`: `one_country_header_template`
(`:135`), `two_countries_header_template` (`:202`).

### 3.8 What a rich panel has that a minimal one lacks — the short answer

1. A **race** — two numbers moving against each other with a bar
   (`gag_faction_barchart_widget`, `IW_BALANCE_OF_POWER`, `ROTT_LEADER_COUNTRY`).
2. **Per-participant attribution** — the bar is sliced by country in map colour,
   the member row shows that country's monthly contribution.
3. **A second tab** — Members / Reformers / Countries, with sortable columns.
4. **Its own widget types** in its own file.
5. **Flavour tooltips** (`TooltipFlavorTextBlock`) explaining the mechanic in
   character, not just in numbers.
6. **A running total** the player watches climb (`KILL_COUNTER`, `TOTAL_DEATHS`,
   `CONVERTED_LOCATIONS`).

None of 1–6 requires a single extra event.

---

## 4. LOCALIZATION STYLE

### 4.1 The four key families for a situation, quoted from `main_menu/localization/english/situations_l_english.yml`

**(1) `<situation_key>` — the display name.** Line 12:
`black_death: "Black Death"`. Not always literal — line 242
`rise_of_the_ottomans: "Rise of the Turks"` (key says Ottomans, name says Turks,
because at 1337 there is no Ottoman Empire yet), line 275
`rise_of_timur: "Rise of $name_timur$"`, line 57
`treaty_of_tordesillas: "Treaty of [GetSituationByKey('treaty_of_tordesillas').MakeScope.GetVariable('treaty_location').GetLocation.GetNameWithNoTooltip]"`
(named after whichever location the game picked).

**(2) `<situation_key>_desc` — the long prose blurb** shown in the panel. This is
the single longest string a situation owns. 22 of 23 situations have one.

**(3) `<situation_key>_info` — one short line of live state.** Only 6 situations
have one, and every one of them is a *variable read*, not prose:
```
14  black_death_info: "Originated in [ROOT.GetVariable('original_outbreak').GetDiseaseOutbreak.GetOrigin.GetName]"
142 western_schism_info: "The schism is a conflict between the factions supporting [ROOT.GetVariable('schism_pope_cardinal').GetCardinal.GetName] and [ROOT.GetVariable('schism_opponent_cardinal').GetCardinal.GetName]."
195 great_pestilence_info: "[ROOT.GetVariable('great_pestilence_origin').GetLocation.GetName]"
358 hundred_years_war_info: "This is a conflict that will create [wars|e] between [GetCountry('ENG').GetName] and [GetCountry('FRA').GetName] until one side has reached their goals."
490 nanbokuchou_info: "The division between the Northern Court in [GetCountry('NTC').GetCapital.GetName] and the Southern Court in [GetCountry('STC').GetCapital.GetName]."
523 fall_of_delhi_info: "During the Fall of [GetCountry('DLH').GetNameWithNoTooltip], countries across $india$ will attempt to wrest control of their regions from the powerful [GetCountry('DLH').GetL…"
```
Note `ROOT` here is the situation. `_info` answers "what is happening right now",
`_desc` answers "what is this".

**(4) `<situation_key>_monthly` — what the monthly tick does, in one bulleted line.**
Only 3 exist, and they are the ones that pair with the
`custom_tooltip = { text = <key> ... }` wrapper around the `on_monthly`
`random_list`:
```
15  black_death_monthly: "$BULLET$This plague will spread to nearby [locations|e] and across trade routes\n$BULLET$It will kill many [pops|E], [armies|e], and [characters|E] wherever it spreads."
196 great_pestilence_monthly: "$BULLET$This plague will spread to nearby [locations|e], and across trade routes.\n$BULLET$It will kill many [pops|E], [armies|e], and [characters|E] where it has spread."
372 hundred_years_war_monthly: "If there is [peace|e], there is a chance of either side restarting the conflict."
```
`$BULLET$` is the bullet macro. (See §7 for where vanilla forgot it.)

**Two supporting families that are just as load-bearing:**

*(5) `<something>_tt` — tooltip fragments used by `custom_tooltip` in triggers.*
The `can_end` trigger's text is built from these, and they are how the
END_REQUIREMENTS card gets readable:
```
43  black_death_end_trigger_tt: "No [location|e] has the disease present"
44  great_pestilence_end_trigger_tt: "The Situation will end after most of the continent of [ShowContinentName('america')] has been infected, and the disease has disappeared from every [location|e]"
77  treaty_of_tordesillas_end_tooltip: "This Situation will end when the Treaty's Relevance drops to 0 during its second phase."
267 strongest_beylik_has_over_Y_locations: "[…] owns at least 1250 [locations|e] between themselves and all their subjects, as well as 100 [towns_or_cities|e]."
```

*(6) `<map_state>_tt` — the map-mode legend*, read by the situation's
`tooltip = { … custom_tooltip = <key> }` block:
```
377 this_is_france_tt: "This is the [GetCountry('FRA').GetLongName]"
380 loyal_member_of_the_french_side_tt: "This is a loyal [subject|e] of [GetCountry('FRA').GetName]"
379 disloyal_member_of_the_french_side_tt: "This is a [disloyal_subject|e] of [GetCountry('FRA').GetName]"
385 this_is_ally_of_both_tt: "This is an [ally|e] of both [GetCountry('ENG').GetName] and [GetCountry('FRA').GetName]"
159 SCHISM_SIDE_WITH_ROME: "[THIS.GetLocation.GetOwner.GetLongName|Y] is supporting the #Y Pope#! in [GetSituationByKey('western_schism').MakeScope.GetVariable('schism_pope_cardinal').GetCardinal.GetLocation.GetName]!"
```

*(7) Action families,* one set per `generic_action` with `type = situation`:
`<action>`, `<action>_desc`, `<action>_price`, `<action>_tt` —
`situations_l_english.yml:304-306, 344`:
```
press_claims: "Press Claims"
press_claims_desc: "[ShowRegionName('anatolia_region')] is under threat by outside forces. […] It is up to us to unite them all under #italic our#! banner!"
roto_press_claims_explanation_tt: "Grants a claim against a [province|e] in [ShowRegionNameWithNoTooltip('anatolia_region')]"
rto_press_claims_price: "Press Claims Price"
```

### 4.2 Hint loc — the file is `main_menu/localization/english/hints_l_english.yml`

The hint itself is defined in `in_game/common/scriptable_hints/scripted_hints.txt`
(92 hints), and its shape is tiny — `scripted_hints.txt:691-699`:
```
hint_black_death = {
	priority = {
		can_see_situation = situation:black_death
	}
	hide = {
		NOT = { is_situation_active = situation:black_death }
	}
	sort_priority = 200 #React now!
}
```
Every situation hint in the file is that exact shape with the key substituted, and
every one uses `sort_priority = 200 #React now!`.

The loc key family, verified against `hints_l_english.yml`:

| key | line | content |
|---|---:|---|
| `hint_black_death` | 536 | `"The Black Death"` — the hint's title |
| `hint_black_death_hint_text` | 537 | `"$hint_black_death_hint_text_1$\n\n$hint_black_death_hint_text_2$\n\n$hint_black_death_…"` — an assembly of the numbered parts |
| `hint_black_death_hint_text_1` | 538 | what the situation is |
| `hint_black_death_hint_text_2` | 539 | `"#T Recommended Actions:#!\n@arrow_bonus_tier_3! …"` |
| `hint_black_death_hint_text_3` | 540 | `"#T Extra Hints:#!\n@hint! …"` |
| `hint_black_death_diplomatic` | 542 | advisor voice line, in escaped quotes |
| `hint_black_death_administrative` | 543 | advisor voice line |
| `hint_black_death_military` | 544 | advisor voice line |

The three-part body is a strict convention: **_1 = what it is, _2 = "#T Recommended
Actions:#!" with `@arrow_bonus_tier_3/2/1!` icons in descending priority, _3 =
"#T Extra Hints:#!" with `@hint!` icons.** Longer situations extend it — HYW runs
to `_hint_text_5` (`hints_l_english.yml:599`, `"#T Vassal Defection#!"`), and
`hint_italian_wars_hint_text_2` (`:621`) is 3 paragraphs of strategy.

The three advisor lines are the flavour payload and are the funniest writing in
the game:
```
542 hint_black_death_diplomatic: "\"Death rides forth. Ruin and turmoil follow.\""
543 hint_black_death_administrative: "\"Pale Death knocks with impartial foot at the towers of the kings and the huts of the poor.\""   [Horace, Odes I.4]
544 hint_black_death_military: "\"The fourth Rider is upon us. No Hint will save us now.\""
601 hint_hundred_years_war_diplomatic: "\"Give war a chance!\""
603 hint_hundred_years_war_military: "\"While [GetCountry('FRA').GetName] and [GetCountry('ENG').GetName] bleed each other dry, there is much to be gained for those with vision. Keep armies ready and allies close.\""
```
Where a situation has nothing to say, the three keys fall back:
`hint_guelphs_and_ghibellines_diplomatic: "$hint_advisor_salute_diplomatic$"`
(`hints_l_english.yml:717`).

### 4.3 Event loc — where it lives and how big it is

`main_menu/localization/english/events/situations/` — 26 `.yml` files,
2300 lines, 1881 keys. Not one per event file: `golden_age_of_piracy.txt`'s events
are split across `golden_age_of_piracy_events_l_english.yml` (15 keys) and
`great_pirate_era_l_english.yml` (35 keys); `little_ice_age` borrows
`winter_events`; `fall_of_delhi` uses `delhi_situation_*` keys entirely (see §7).

Largest: `red_turban_rebellions_events_l_english.yml` (179 keys),
`hundred_years_war_events_l_english.yml` (178), `rise_of_the_ottomans` (160),
`rise_of_timur` (144).

### 4.4 Measured prose lengths (variable substitutions collapsed to one token)

```
470 event .desc strings   median  55 words   mean 54.7   max 169
340 event .title strings  median   4 words   max 7
```
Per-file `.desc` medians:
```
great_pirate_era 94.5 | council_of_trent 87 | little_ice_age 82.5 | movements 77
revolution 74 | black_death 72.5 | fall_of_delhi 70 | great_pestilence 66
hundred_years_war 61 | rise_of_the_ottomans 60.5 | hussite_wars 57
italian_wars 54 | nanbokuchou 53 | red_turban 50.5 | sengoku 50.5
reformation 50 | colonial_revolution 50 | tordesillas 48.5 | rise_of_timur 41
western_schism 33 | guelphs_and_ghibellines 23.5 | war_of_religions 7
```
**The target is 50–70 words for a situation event description, 3–5 words for a
title.** `war_of_religions`'s median of 7 is an artefact — that file's keys are
mostly short `_tt` fragments rather than event descs.

The situation `_desc` blurbs are longer: `rise_of_the_ottomans_desc`
(`:243`) runs three paragraphs; `reformation_desc` (`:86`) three;
`hundred_years_war_desc` (`:359`) one long paragraph of ~90 words.

### 4.5 Voice — six lines that define it

**1. Open a catastrophe with a period source, in single quotes, and let it run.**
`situations_l_english.yml:13`
```
black_death_desc: "'Father abandoned child, wife husband, one brother another; for this illness seemed to strike through the breath and sight. And so they died... great pits were dug and piled deep with the multitude of dead... And as soon as those ditches were filled, more were dug... And so many died that all believed it was the end of the world.'"
```
The entire description is the quotation. No framing, no explanation. (It is
Agnolo di Tura, paraphrased.)

**2. Open a movement with its founding document, then explain.**
`situations_l_english.yml:86`
```
reformation_desc: "'#italic When our Lord and Master Jesus Christ said 'Repent,' he willed the entire life of believers to be one of repentance.#!'\n\nThese were the first notes in a document of 95 Theses found nailed to a church door, each detailing the corruption of the [GetInternationalOrganization('catholic_church').GetName]. […]"
```
`'#italic … #!'` inside single quotes, then `\n\n`, then the prose. This is the
canonical two-beat opening.

**3. Write the *other* civilisation's point of view, not yours.**
`situations_l_english.yml:194`
```
great_pestilence_desc: "Terrible news reaches us from abroad. Misery and plague sweep the land, and death runs with them, apparently brought by mysterious bearded foreigners. This plague is not something our elders have ever heard of, and no answers in our ancestors' memories could help us face the catastrophe if it reaches our settlements. Will our people perish, or will we somehow resist when this walking death reaches us?"
```
"mysterious bearded foreigners" — the Columbian exchange written from the
Mesoamerican side, ending on a question. Compare the Black Death desc, which is
European and ends on certainty.

**4. Let an option be a single line of period speech.**
`events/situations/rise_of_the_ottomans_events_l_english.yml:198`
```
rise_of_the_ottomans.600.a: "#italic We are the [ROOT.GetCountry.GetGovernment.GetRulerTitle] of the lands and the seas, the shadow of [ROOT.GetCountry.GetReligion.GetGodName] on earth.#!"
```
The option *is* the ruler's proclamation. The event it belongs to
(`rise_of_the_ottomans.txt:3104-3148`) silently promotes the country to
`country_rank:rank_empire` — the mechanical payload is entirely hidden behind one
italic sentence.

**5. Titles are short, concrete and often idiomatic.**
```
events/situations/hundred_years_war_events_l_english.yml:23   hundred_years_war.11.title: "Perfidious Albion!"
events/situations/hundred_years_war_events_l_english.yml:19   hundred_years_war.10.title: "The Issue is not Settled"
events/situations/western_schism_events_l_english.yml:75      western_schism.1000.title: "The Price of #italic Oboedientia#!"
events/situations/rise_of_the_ottomans_events_l_english.yml:159 rise_of_the_ottomans.214.title: "Mints of the Old Sultanate"
```
`Oboedientia` untranslated, `Perfidious Albion` as a French event title — the
titles carry period idiom the descriptions cannot.

**6. And they will break voice for a joke, once.**
`situations_l_english.yml:175`
```
western_schism_become_neutral_desc: "'#italic What makes a man turn neutral? Lust for gold? Power? Or were you just born with a heart full of neutrality?#!'"
```
(A *Watchmen* line, used as the flavour for abstaining in the Schism vote.) Also
`hints_l_english.yml:544` `"The fourth Rider is upon us. No Hint will save us now."`
— a joke that only works because the surrounding 90 hints are earnest.

**7. Second person plural throughout.** Every description is "we / our" from the
country's perspective: "We can no longer disregard the fact…"
(`hundred_years_war.2.desc`), "We still do not agree with the […] position about
who should rule…" (`hundred_years_war.10.desc`). Third person is used only for
outcome announcements: "In a remarkable turn of events, the [ENG] has emerged
victorious…" (`hundred_years_war.100.desc`).

---

## 5. IMMERSION DEVICES — the complete list, one citation each

| # | device | citation |
|---|---|---|
| 1 | **Named historical characters by key in event text.** 23 uses of `GetCharacter('…')` across the situation event loc; 10 distinct people. | `hundred_years_war_events_l_english.yml:10` — `"[…] makes [GetCharacter('fra_philip_vi_valois').GetName] the […] of [FRA], when it clearly should be [GetCharacter('eng_edward_iii').GetName], as [GetCharacter('eng_edward_iii').GetHerHis] mother [GetCharacter('eng_isabella_of_france').GetName] was the sister of [GetCharacter('fra_charles_iv_capet').GetName]."` |
| 2 | **A named character as a *plot object*, gating the situation's start.** | `in_game/common/situations/hundred_years_war.txt:17-28` — `can_start` contains `custom_tooltip = { text = matter_of_robert_is_settled_tt  OR = { c:ENG = { … has_variable = robert_the_fugitive_flag … }  character:eng_robert_iii_artois = { is_alive = no } } }`. The Hundred Years' War does not begin until Robert of Artois' case is closed. |
| 3 | **Period quotation as the whole description.** | `situations_l_english.yml:13` (Black Death); `:86` (Luther's Thesis 1) |
| 4 | **`historical_info` — the out-of-character encyclopedia note.** 48 events carry one; `rise_of_the_ottomans` alone has 12. | `hundred_years_war_events_l_english.yml:7` — `hundred_years_war_historical_info: "The Hundred Years' War was a long and brutal conflict between England and France that lasted from 1337 to 1453. […]"` ; `rise_of_timur_events_l_english.yml` — `rise_of_timur.1040.desc.historical_info: "In the year 1398, Bayezid 'the Thunderbolt' I came into his first conflict with the Timurid Empire […]"` |
| 5 | **A running total the player watches climb.** | `situations_l_english.yml:288` — `KILL_COUNTER_DESC: "The marauding armies of the [GetCountry('TIM').GetLongName] have killed #Y [SituationView.GetActiveSituation.GetSituation.MakeScope.GetVariable('timur_total_kill_counter').GetValue]#! people in total."` (also `TOTAL_DEATHS`, `:28`; `COUNTRY_DEATHS`, `:37`) |
| 6 | **Live per-location numbers in the map tooltip.** | `situations_l_english.yml:18` — `BLACK_DEATH_PRESENT_IN_LOCATION: "[THIS.GetLocation.GetName|Y]\nCurrent Population: [THIS.GetLocation.GetTotalPopulation|Y]\nThe #R Black Death#! has infected [THIS.GetLocation.GetDiseaseInfectionPercentage('bubonic_plague')|R2%] of our people."` |
| 7 | **Location-anchored events** — the event picks a real owned location and the text names it. `scope:target_location` alone appears **214** times in the corpus. | `black_death.txt:1327-1330` — `random_owned_rural_location = { limit = { disease_presence = … } save_scope_as = target_location }` |
| 8 | **Map spectacle: recoloured provinces.** 22 of 23 situations define `map_color`, 9 also `secondary_map_color` (striped). | `in_game/common/situations/hundred_years_war.txt:323-353` — a 5-branch `if/else_if` chain assigning `value = map_FRA` / `value = map_ENG` by ownership *and subject loyalty* (`subject_loyalty > 50`). Disloyal vassals visibly change colour on the map. |
| 9 | **Map spectacle: per-location legend text.** 21 of 23 define `tooltip = { … }`. | `in_game/common/situations/hundred_years_war.txt:241-266` → `custom_tooltip = this_is_france_tt` / `loyal_member_of_the_french_side_tt` / `disloyal_member_of_the_french_side_tt` |
| 10 | **Named real places as objectives.** | `situations_l_english.yml:269` — `TRUNK_ROAD_TOOLTIP: "This location is part of the trunk road to [ShowLocationNameWithNoTooltip('erzurum')]. Owning it will give us access to the [ShowEstatePrivilegeName('trunk_road_to_erzurum_privilege')] [estate_privilege|e]"` ; `:268` `SELJUK_MINT_TOOLTIP`. The map itself becomes a quest board. |
| 11 | **A situation timeline the player can look back on** — `flag_situation_event`. 11 uses. | `rise_of_timur.txt:477-480` — `flag_situation_event = { situation = situation:rise_of_timur  event = rot_fall_of_delhi }`. The named flags (`rot_fall_of_delhi`, `rot_prepare_conquest_of_china`) are also referenced from `in_game/common/on_action/_hardcoded.txt:4501` and `in_game/common/scripted_effects/situation_effects.txt:308`. |
| 12 | **Culture/religion-branched descriptions.** 45 uses of `first_valid` at option level plus `desc = { first_valid = { triggered_desc = … } }` at event level. | `great_pestilence.txt:9-19` (quoted in §2.7C) |
| 13 | **Portrait casting.** 41 `create_character` calls at option level; `save_scope_as = target_character*` used to place the right faces on the event. `hide_portraits = yes` (14 uses) suppresses them for impersonal events. | `hundred_years_war.txt:1233-1236` — `scope:actor.ruler_or_regent ?= { save_scope_as = target_character1 }` / `ruler_or_regent ?= { save_scope_as = target_character2 }` ; `italian_wars.txt:8`, `little_ice_age.txt:32`, `sengoku.txt:64` — `hide_portraits = yes` |
| 14 | **Estate-composed illustrations.** `event_illustration_estate_effect` — 127 uses, an `immediate`-block effect that composes the event art from two estate types. | `rise_of_timur.txt:476` — `event_illustration_estate_effect = { foreground = estate_type:peasants_estate background = estate_type:peasants_estate }` ; 22 uses of `{ foreground = estate_type:nobles_estate background = estate_type:burghers_estate }` |
| 15 | **Randomised illustration variants.** `illustration_tags`, 149 uses, weighted. | `rise_of_timur.txt` — `illustration_tags = { 10 = regular  10 = interior }`. Distinct tag values across the corpus: `exterior` 109, `armed` 68, `regular` 50, `interior` 43, `happy` 19, `angry` 14. |
| 16 | **Fixed illustration per situation.** 260 events carry `image = `. | `hundred_years_war.txt:1163` — `image = "gfx/interface/illustrations/situation/hundred_years_war.dds"` (all 33 HYW events use the same one) |
| 17 | **No sound fields.** Searched for `sound`, `theme`, `play_sound`, `left_portrait`, `right_portrait`, `open_view`, `goto_location` across all 25 files: **zero hits.** The only presentation fields are `image`, `illustration_tags`, `event_illustration_estate_effect`, `hide_portraits`. Situation audio is not scripted per-event. |
| 18 | **A phase/tension meter that unlocks actions at thresholds.** | `in_game/common/situations/italian_wars.txt:380-473` — `set_variable = { name = iw_tension value = 0 }`, `iw_increase_tension_effect = { value = iw_tension_gain_low }`, and gates at `var:iw_tension >= 100` / `>= 50`. Documented to the player at `hints_l_english.yml:620`: `"As the conflict deepens, [situation_tension|e] rises, unlocking new [actions_with_icon|e] at four key thresholds."` |
| 19 | **Voting and resolutions.** 4 situations declare `resolution =` / `voters =`. | `in_game/common/situations/council_of_trent.txt:4-5` — `international_organization_type = catholic_church` / `voters = council_of_trent_voters` ; `fall_of_delhi.txt:4-5` — `resolution = "fall_of_delhi_resolution"` / `voters = fall_of_delhi_voters` |
| 20 | **The panel explaining itself in the situation's voice.** | `situations_l_english.yml:250` — `ROTT_LEADER_COUNTRY_SCORE_FLAVOR_TT: "#italic Every month, the overall performance of the countries in the […] [situation|e] is evaluated and the positions of the three most powerful ones are updated based on the new scores.#!"` |
| 21 | **Colour and icon markup as emphasis.** `#R` red, `#Y`/`|Y` yellow, `#G` green, `#V`, `#T` header, `#W`, `#italic`, `#bold`, `#weak`, `@trigger_yes!`, `@trigger_no!`, `@hint!`, `@arrow_bonus_tier_3!`, `$BULLET$`. | `situations_l_english.yml:299` — `STRONGEST_BEYLIK_BONUS_TOOLTIP: "…\n@trigger_yes! [events|e] that speed up the [integration|e] of [provinces|e]\n@trigger_yes! $game_concept_events$ that [subjugate|e] weaker neighbors\n@trigger_yes! Unique [situation|e] [actions|e]"` |
| 22 | **Concept links everywhere.** `[situation|e]`, `[locations|e]`, `[pops|E]` (capital E = plural-capitalised), `[war_goal_with_icon|e]`, `[situation_with_icon|e]`. | `situations_l_english.yml:8` — `SITUATION_MEMBERS_TT_TEXT: "Shows all the [members|e] in the [situation|e]."` |
| 23 | **Named characters *created* by the situation and then referenced.** | `rise_of_timur` — `[GetCountry('TIM').MakeScope.GetVariable('tim_founding_father').GetCharacter.GetName]` in `situations_l_english.yml:276`, i.e. the situation's protagonist is a runtime variable, not a hardcoded key. |

---

## 6. TEMPO — player-visible beats per year

Computed from the `on_monthly` `random_list` weights in
`in_game/common/situations/<name>.txt`. "Peak" = every trigger passing; "idle" =
gating triggers failing, so only the ungated rolls fire. These are per *eligible
country*, and eligibility is the crucial variable.

### `black_death` — the densest in the game

`black_death.txt:68-102`. Per month, for **every country with the outbreak**:
27 branches at weight 10 against an idler of `500 = { }`.
```
P(beat) = 270 / 770 = 35.1 % per month  →  ~4.2 player-visible events per year
```
There is no idle state: the roll is unconditional on the situation's own side
(only the `every_country` limit `country_has_disease_outbreak` gates it), and the
individual events carry their own `trigger` + cooldown variable, so a country that
has seen a given beat rolls it again and falls through to nothing. Peak ≈ 4.2/yr,
declining as cooldown variables accumulate. Add 1 `on_start` and 1 `on_ended`.

### `hundred_years_war` — a two-country drumbeat, and silence for everyone else

`hundred_years_war.txt:65-143`. Two rolls:
- `random_list { 1 = ENG→.211 ; 1 = FRA→.211 ; 99 = {} }` → 1.98 %/month, ungated.
- `random_list { 20 ×4 ; 200 = {} }` → 7.14 % per branch, 28.6 % total, each branch
  trigger-gated on CB/truce/war/manpower/war-exhaustion/relative-strength.
```
Peak (all four gates open):  ~30.6 %/month  →  ~3.7 beats/year, split between ENG and FRA
Idle (at war, or truced):    ~2.0 %/month   →  ~0.24 beats/year
```
**Everyone else in western Europe gets exactly one event, ever** (the `on_start`
broadcast `hundred_years_war.1`) plus whatever they trigger through the 11
`generic_actions/hundred_years_war.txt` actions and the 8
`dynamic_historical_event` blocks. The situation's presence for a bystander is
carried by the map colours, the panel, and the actions — not by events.

### `rise_of_the_ottomans`

`rise_of_the_ottomans.txt:165-293`. Four rolls plus three unconditional `if` gates:
- `random_list { 93 = {} ; 4 → .105 ; 3 → .101 }` → 7 %/month **to the leader only**
- `random_list { 95 = {} ; 5 → .300 }` → 5 %/month to one random eligible beylik
- `if current_year > 1337 → random_list { 50 = {} ; 25 → .213 to ALL ; 25 → .214 to ALL }`
  → 50 %/month broadcast, but both events carry
  `trigger = { has_variable = trunk_road_event_eligible_variable }`
  (`rise_of_the_ottomans.txt:2791`) and remove it in `immediate` — so each fires
  **at most once per country**, not monthly.
- three `if` gates on `num_locations > 120` / `> 300` for `.400`, `.215`, `.600`.
```
Leader, peak:   ~12 %/month + threshold events  →  ~1.5–2 beats/year
Non-leader:     ~5 %/month shared across all beyliks  →  well under 1/year each
```
Plus 8 `building_types/unique_buildings.txt` call sites and 6 action call sites.
This is a situation whose tempo is *deliberately unequal* — the leader gets the
story, the rest get the map.

### `guelphs_and_ghibellines` — the panel carries it, not the events

`guelphs_and_ghibellines.txt:100-267`. The entire monthly tick opens with
`hidden_effect = {` at `:101` and is ~150 lines of variable arithmetic. The only
event roll is `random_list { 2 = → .9 ; 98 = {} }`, applied three times to three
disjoint audiences (`c:PAP` at `:113-125`, the HRE leader at `:126-138`, and every
non-aligned country present in `region:italy_region` at `:139-154`).
```
Peak = idle = 2 %/month  →  ~0.24 beats/year, and only for the unaligned
```
Members of either IO get **no monthly events at all**. What they get instead:
3 `on_start` events, **10 `on_ending`/`on_ended` events**, 7 panel actions, and a
live two-sided barchart sliced by member country in map colour. The Guelphs and
Ghibellines is the proof that a situation can be highly immersive with a
0.24-events-per-year event budget, provided the panel is doing the work.

### Summary

| situation | peak beats/yr | idle beats/yr | who receives them |
|---|---:|---:|---|
| black_death | ~4.2 | ~4.2 (decaying) | every infected country |
| rise_of_the_ottomans | ~1.5–2 | <0.5 | the leading beylik |
| hundred_years_war | ~3.7 | ~0.24 | ENG and FRA only |
| guelphs_and_ghibellines | ~0.24 | ~0.24 | unaligned Italians, PAP, Emperor |

**The design lesson:** vanilla concentrates event tempo on 1–2 protagonists and
gives everyone else map colour, panel state, and clickable actions. A mod that
tries to give every participant 4 events a year will produce popup fatigue and
will not match the vanilla feel.

---

## 7. ANTI-PATTERNS

### 7.1 What is *not* wrong — two checks that came back clean

Run before assuming anything:

- **Orphaned loc keys: zero.** All 1881 keys in
  `main_menu/localization/english/events/situations/*.yml` and all 916 keys in
  `situations_l_english.yml` are referenced at least once elsewhere in
  `in_game/**` or `main_menu/**` (`.txt`/`.gui`/`.yml`). Scanned 9059 files.
- **Dead events: two, and both are false positives.** Of 455 event ids, only
  `fall_of_delhi.1` and `fall_of_delhi.18` are never named by a
  `trigger_event_*`. Both are fired by their own `dynamic_historical_event` block
  (`fall_of_delhi.txt:362-368` and `:1618-…`).

  **This is the exact blind spot the project's harness already knows about, in a
  new syntax.** A reachability checker that only looks for `trigger_event_*` will
  report these two healthy events as orphans. Any situation-event reachability
  check written for this mod must treat `dynamic_historical_event = { … }` as a
  firing site — and that construct is used **3182 times** across vanilla's event
  tree, so the blind spot is enormous, not marginal.

### 7.2 Real defects in shipped vanilla — do not copy

| # | defect | citation |
|---|---|---|
| 1 | **A whole file's loc namespace does not match its event namespace.** `fall_of_delhi.txt` declares `namespace = fall_of_delhi` and defines `fall_of_delhi.N`, but every one of its 22 events points at `delhi_situation.N.title` / `.desc`. It works, but it defeats every convention-based tool. | `in_game/events/situations/fall_of_delhi.txt:355` `title = delhi_situation.1.title` vs the event id `fall_of_delhi.1` at `:353` |
| 2 | **A placeholder key name shipped.** | `situations_l_english.yml:227` — `XYZ: "The following [laws|e] can be changed while the [situation|e] is active:"` |
| 3 | **A TODO shipped in a user-visible name.** | `situations_l_english.yml:888` — `the_revolution: "People's Uprising" #Temp until we figure out a better name` |
| 4 | **A literal bullet where the macro belongs**, breaking consistency with the sibling key 2 lines up. | `situations_l_english.yml:198` — `great_pestilence_kills: "•It will kill many …"` vs `:197` `great_pestilence_spreads: "$BULLET$This plague will spread…"` and `:17` `black_death_kills: "$BULLET$It will kill many…"` |
| 5 | **Cross-situation `historical_info` reuse.** A Great Pestilence event shows the Columbian Exchange's historical note. | `in_game/events/situations/great_pestilence.txt:23` — `historical_info = columbian_exchange.1.historical_info` |
| 6 | **Title key reused across two different events**, so the notification list shows the same headline twice. | `hundred_years_war.txt:1038` and `:1218` both `title = hundred_years_war.206.title` (on events `.206` and `.208`) |
| 7 | **Typos in shipped English.** | `golden_age_of_piracy_events_l_english.yml:5` `"No, we wil not bow down…"` ; `hundred_years_war_events_l_english.yml:28` `"We have a a claim to the throne…"` ; `little_ice_age_events_l_english.yml:4` `"Marked by by a series of cooling periods…"` |
| 8 | **Copy-paste comments left in place.** `hundred_years_war.gui:99` labels the *English* half of the card `#Left - Delhi the infirm`, and `:135` labels France `#Right - Opposers' Strongest Country` — both lifted verbatim from `fall_of_delhi.gui`. `black_death.gui:223` has the same `#Right - Opposers' Strongest Country` over the deaths counter. | `hundred_years_war.gui:99,135` ; `black_death.gui:223` |
| 9 | **Dead GUI declared and then disabled.** `common.gui:43` declares `# block "situation_header_extra" {}` **inside a comment** — so four panels write `blockoverride "situation_header_extra"` (also commented out, e.g. `hundred_years_war.gui:4`) against a block that does not exist. Likewise the entire threshold-progressbar vbox at `common.gui:260-329` is hard-set `visible = no` at `:262` with its own `block "situation_variable_progress_bar_visible"` commented out at `:261`, and the `situation_piechart_template` at `:583-610` is commented out wholesale. | `common.gui:43, 61-83, 204-214, 236-239, 261-263, 276-302, 312-325, 403-405, 413, 456, 583-610` |
| 10 | **`monthly_spawn_chance` documented as a disease field.** The readme still describes it as "how likely the **disease** is to spawn per month". | `in_game/common/situations/readme.txt:5` |
| 11 | **`is_ai = no` as a defensive workaround, with the reason in the comment.** Worth copying the *practice* (gate player-only tag swaps), not the resignation. | `golden_age_of_piracy.txt:209` — `trigger = { is_ai = no }	#Let's avoid weird potential issues...` |
| 12 | **Two files sharing one `namespace`.** `reformation.txt` and `D008_reformation.txt` both declare `namespace = reformation`. No id collision today (checked), but nothing prevents one, and a DLC file that collides with a base file would be silent. | `in_game/events/situations/reformation.txt` and `D008_reformation.txt`, both line 1 |

---

## 8. THE TRANSFERABLE RECIPE

Distilled from the above; every element is attested in §1–§6.

**A vanilla-grade situation is seven files.**

1. `in_game/common/situations/<key>.txt` — BOM. `monthly_spawn_chance`,
   `hint_tag`, `can_start`, `can_end`, `visible`, `on_start`, `on_monthly`,
   `on_ending`/`on_ended`, `tooltip`, `map_color`, optionally
   `secondary_map_color`. **This file is the event dispatcher.**
2. `in_game/events/situations/<key>.txt` — BOM. 18–46 events, 88 % of them with
   1–2 options, chains no deeper than 2 hops, 50–70-word descriptions.
3. `in_game/common/generic_actions/<key>.txt` — BOM. 5–15 actions with
   `type = situation`. These appear in the panel automatically
   (`common.gui:332-335`) and are where the player spends gold
   (`price = price:<key>`).
4. `in_game/common/prices/…` — the action prices
   (`scaled_gold` / `gold` / `prestige` / `stability` / `government_power`).
5. `in_game/gui/panels/situation/<key>.gui` — **no BOM**. Copy
   `rise_of_the_ottomans.gui`. Minimum three blockoverrides:
   `"situation_panel_image"`, `"situation_subheader_content"{}`,
   `"situation_panel_main_content"` containing the END_REQUIREMENTS card.
6. `in_game/common/scriptable_hints/scripted_hints.txt` — one 9-line entry with
   `priority = { can_see_situation = situation:<key> }`,
   `hide = { NOT = { is_situation_active = situation:<key> } }`,
   `sort_priority = 200`.
7. Localization: `<key>` / `<key>_desc` / `<key>_info` / `<key>_monthly` in a
   situations file; `hint_<key>` / `_hint_text` / `_hint_text_1..N` /
   `_diplomatic` / `_administrative` / `_military`; one events yml per situation;
   plus `_tt` fragments for every `custom_tooltip` in `can_end` and `tooltip`.

Plus one asset: `gfx/interface/illustrations/situation/<key>.dds`, found by
`GetSituationIllustration` with no GUI reference needed.

**Three things that buy the most immersion per unit of work, in order:**

1. `map_color` + `tooltip` in the situation definition (~60 lines, gives the whole
   map a legible faction state and a hover legend for every province).
2. The `generic_actions` file (appears in the panel free; carries all the player
   agency; 5 actions is a plausible minimum).
3. A single running number in the panel (`KILL_COUNTER`, `TOTAL_DEATHS`,
   `CONVERTED_LOCATIONS`) — one `set_variable` in `on_monthly` and one
   `situation_card_expandable`.

**Two things that cost the most and buy the least:** long event chains (vanilla's
deepest is 3 hops) and high event tempo for non-protagonists (vanilla gives
bystanders 0.24 events/year and lets the map and the panel do the talking).
