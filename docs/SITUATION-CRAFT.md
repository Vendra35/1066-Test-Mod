# SITUATION CRAFT — the vanilla + reference-mod sweep (2026-08-04)

> The situations phase's opening research pass: six Opus agent reports,
> raw copies banked in `docs/research/2026-08-04/` (craft-vanilla-anatomy,
> craft-vanilla-flavour, craft-anno1644, craft-timur-bronze-basileia,
> craft-national-destinies, craft-workshop-six). This file is the
> main-session distillation — the laws and traps every 1066 situation is
> built under, alongside `SITUATION-SPECS.md` (the WHAT) and this file
> (the HOW). Corpus: vanilla 22 situations / 9,171 lines + 473 situation
> events / 34,297 lines + 155 situation actions + 23 GUI panels; five
> reference mods and six workshop mods end to end.
>
> **Verification status.** Seven load-bearing claims were re-verified by
> the main session against vanilla the same day (marked ✓MS below):
> spawn-chance value table; 22_situations' single live empty-body entry;
> the scriptable_hints situation objects; `end_reason` = 0 vanilla uses;
> `type situation_panel = lateralview` + the auto-built action list;
> 13 DHE uses in the situation event corpus; `hint_tag` in 22/22
> situation defs. Everything else carries the agent report's file:line
> and is one grep away; a claim cited only to a report is a hypothesis
> until someone reproduces it.

## The twelve craft laws

**1. The definition is the metronome.** Firing verbs: 303 in
`in_game/common/situations/` vs 72 in `in_game/events/situations/`.
`on_start` schedules, `on_monthly` drives, `on_ended` cleans. Our
Norman Conquest architecture matches; its deficit is density, not shape.

**2. The seeding law (four sources).** NO vanilla situation starts
active at 1337; `22_situations.txt` is dead even in vanilla — one live
entry, `rise_of_the_ottomans`, with an EMPTY body (✓MS). Day-one starts
are an already-true `can_start` + `monthly_spawn_chance_unique` (= 1,
i.e. 100%/month; value table `default_values.txt:1205-1212` ✓MS —
very_low .01 / low .02 / medium .03 / high .04 / very_high .05 /
ultimate .1 / ultimate_high .5 / unique 1). Anno 1644 does the same at
its moved date (5 of 7 fire in the first month;
`war_of_three_kingdoms.txt:17` reads `current_date >= 1644.4.1`);
Bronze Era ships a deliberately empty `situation_manager`; Basileia's
22_situations is a byte-identical no-op. Our measured
"spawns on the first monthly tick" law is this mechanism seen from the
other side. `activate_situation` chaining exists but is rare (6 uses
game-wide).

**3. There is no engine phase concept — five hand-rolled idioms.**
(a) float phase + progress bar (`treaty_of_tordesillas`, the best
*shape* to copy — the only true two-stage machine); (b) race-to-1.0
accumulators stored ON THE IOs, not the situation
(`guelphs_and_ghibellines`); (c) clamped 0-100 tension with a one-shot
point of no return (`italian_wars`); (d) debate counters compared
variable-vs-`_max` (`council_of_trent`, `western_schism`); (e) monthly
recomputed top-N ranking variables (`rise_of_the_ottomans` ×3,
`sengoku` ×5). Modded sixth: Bronze Era's month-counter ladder
(36/72/120/180) with global pressure floors player actions cannot erase
plus per-country state they can move. Read-back root changes by site:
`var:x` in on_monthly, `situation:key.var:x` in can_end,
`scope:target.var:x` in map_color.

**4. Flavour's backbone is `dynamic_historical_event`.** A
self-scheduling date-window block — 13 uses in the situation corpus
(✓MS: fall_of_delhi 2, hundred_years_war 8, hussite_wars 2,
rise_of_the_ottomans 1), 3,182 across vanilla's event tree, no
`effects.log` entry. Anno 1644 fills its moved-date world with 333 DHE
blocks opening `from = 1644.1.1`. No `mean_time_to_happen` exists
anywhere; the idiom is a weighted `on_monthly` `random_list` with an
empty-weight idler. National Destinies is the degenerate case — 1,601
byte-identical DHE polling blocks gated only on `has_advance`: 40 good
beats beat 400 acknowledgements.

**5. Concentrate tempo on 1-2 protagonists.** Measured: HYW ~3.7
beats/year — but only for ENG and FRA; every other country gets exactly
one event ever. Black death ~4.2 for everyone (it IS everyone's story);
rise_of_the_ottomans ~1.5-2 for the leader, <0.5 for the rest; G&G 0.24
flat. Bystanders get map colour, panel state and actions, not events.

**6. Chains are short; depth lives in the panel.** Longest event→event
chain in the corpus is 3 hops (`reformation.17→18→19→21`); 378 of 456
events are terminals. ZERO situation events carry `hidden = yes` —
hidden machinery is `hidden_effect` blocks (131) inside player-facing
events plus the on_monthly tick. (`trigger_event_silently` differs from
non-silently ONLY in whether the firing effect's tooltip names the
event — `effects.log:10574-10584`.)

**7. An action's price currency IS the theme.** HYW charges
`government_power = 10`; Hussite/Schism charge `religious_influence`
10/20; Red Turban charges `legitimacy = 5`; Sengoku hostages cost
prestige+legitimacy; Nanbokuchō side-switch costs `stability = 30` +
`honor = 30` (`prices/00_hardcoded.txt:885-888`) — the harshest price
in the game. ~1/5 of the 155 actions are free; cooldowns run 2 months
to 30 years. The panel lists actions AUTOMATICALLY
(`common.gui` builds from the action-group datamodel, ✓MS on the
actions vbox) — a new `type = situation` generic_action costs zero GUI
work.

**8. The reward/penalty band.** Vanilla will go to −50 stability in a
single event (`stability_ultimate_penalty`, 5 situation uses); Red
Turban cuts levy size 45% and mercs 75% for the duration
(`static_modifiers/country.txt:8421-8432`); Little Ice Age stamps a
permanent food modifier on every location in 37 regions. But flagship
"impact" modifiers are often flags, not stats —
`hundred_years_war_impact` is `blocks_country_formation = yes` and
nothing else (confirmed twice now).

**9. The hint is a three-part contract and the alert rides it.**
`hint_tag` in 22/22 vanilla situations (✓MS); it resolves into a
`scriptable_hints` object gated on `can_see_situation` /
`is_situation_active` (✓MS, `scripted_hints.txt` ~691); loc family is
strict: `hint_<key>`, `_hint_text`, `_hint_text_1..N` (_1 what it is,
_2 `#T Recommended Actions:#!`, _3 `#T Extra Hints:#!`), plus
`_diplomatic`/`_administrative`/`_military`. Without the object the
situation raises no alert. Two of six workshop mods shipped dangling
hint_tags; so did Timur and Bronze Era (six between them). OUR NORMAN
CONQUEST HAS NO HINT — v2 debt. Harness check: every situation's
hint_tag resolves to object + loc (lands with the NC v2 commit).

**10. GUI: one type, minimal = three blockoverrides.**
`type situation_panel = lateralview` (`common.gui:3` ✓MS); the
END_REQUIREMENTS card is 10-line boilerplate identical everywhere but
the hint key; Paradox's own readme names `rise_of_the_ottomans.gui` as
the copy base (MR's proven 45-line minimal template is our in-house
equivalent). Freebies: illustration binds by `.dds` filename via
`GetSituationIllustration`, icon by
`main_menu/gfx/interface/icons/situations/<situation_key>.dds` — no
`.gfx` registration at all (Anno 1644 ships zero `.gfx` files). The
rich end: `guelphs_and_ghibellines.gui`, 143 blockoverrides, its own
`types` block, a barchart sliced by member country in map colour.

**11. The loc voice.** 470 event descs, median 55 words; 340 titles,
median 4 words. Devices: a period quotation as the entire desc;
second-person plural; roughly one joke per 90 earnest lines. Key
families: `<key>`, `<key>_desc` always; `_info` exists only 6 times,
`_monthly` only 3 — base+`_desc` is conformance, the other two are
opt-in flourishes (they read live variables when present).

**12. Re-gating a vanilla situation = `REPLACE:<key>`, with the
overwrite trap.** REPLACE inherits panel, art, hint and events for
free — the right tool if a vanilla situation must move or die (Anno
1644 neuters 16 in one additive file by giving each an impossible
can_start). But it is a FULL entry overwrite: MEIOU's Columbian
Exchange REPLACE silently drops vanilla's two `legend_key` blocks —
218 copied lines to lose a map legend. We currently need NO re-gating:
our calendar is real-year aligned, vanilla's situations fire in their
correct historical years by design (the "Ages untouched" decision
paying out).

## Where we stand

Norman Conquest: 690 lines, 0 actions, 0 hint, 1 phase — vs vanilla's
richest (rise_of_the_ottomans 42 events + a 4-rung escalation ladder;
red_turban_rebellions 46 events + a signed −100..+100 allegiance
scalar + a 14-branch release engine) and our own MR corpus (~8,100
lines, five situations). NC's architecture was re-confirmed by this
sweep at every point (lifecycle ownership, CB-first, monthly retry,
16_wars shipping); its v2 scope is now concrete: hint contract, 1-2
actions, a DHE flavour layer, a phase variable, panel richness.

## Forbidden / trap list (new entries from this sweep)

- **`end_reason` is NOT REAL** — zero uses in vanilla situations (✓MS),
  absent from the readme and the official defines. National Destinies
  built both its situations' endings on it, commented as "a 1.3
  feature"; if the engine ignores it those situations have no end
  clause. Never copy it.
- **`on_action` `effect` is single-value** — ND shipped a bug where
  vanilla's own handler, parsed last, silently ate both of ND's; and
  `on_country_yearly_pulse` does not exist (ND invented it). Recurring
  non-situation work belongs in self-gating handlers aggregated in one
  attested pulse (Anno 1644's `monthly_country_pulse` hoisting).
- **`add_country_modifier`'s parameter is `modifier`, not `name`** —
  script docs say `name`, vanilla writes `modifier` 1919/0. Vanilla
  wins per our source hierarchy; UNVERIFIED in game, flagged for the
  next launch's error.log read.
- **`on_start` runs before the activator's follow-up code** —
  bubonic_plague sets `original_outbreak` AFTER `activate_situation`,
  so the activated situation's on_start cannot read it. Order any
  activate-then-configure sequence the other way.
- **Dead-clause drift is vanilla-normal; audit what you copy** —
  italian_wars carries four never-called scripted triggers, one
  contradicting the live `can_end` (65y vs 50y), and its live can_end
  is self-redundant (ends at exactly 50y regardless); G&G ships a
  24-line ordered block with an empty body; sengoku has no `tooltip`
  block at all; colonial_revolution has `can_end = { always = no }`
  with an empty on_ended.
- **The reachability blind spot has a third member:** events fired
  only by their own `dynamic_historical_event` block look dead to
  call-site scanners (fall_of_delhi.1/.18). Our checker must learn the
  DHE syntax before the first DHE lands.
- **SPECS citation corrected:** situation actions live in
  `in_game/common/generic_actions/` — vanilla's Timur actions are
  `generic_actions/rise_of_timur.txt` (situation-type action block at
  :289, ✓MS), NOT `situations/rise_of_timur.txt:288-385` (that range
  is the tooltip/map_color tail). And `rise_of_timur` the situation is
  VANILLA's; the Timur mod rides it with a private layer — dated
  invasion waves, a monthly top-up, timed `is_immortal`, and the
  rubber band (`on_location_changed_owner` reverting AI conquests
  outside a `scripted_geography`). For Manzikert there is no vanilla
  situation to ride; Timur is the model for the surrounding layer,
  not the core.

## Techniques adopted into the build vocabulary

1. **DHE → global variable → `can_start`** (Anno 1644's
   `flavor_zaz.2000` arming `the_deluge`): arm a situation off story
   state instead of a hardcoded date.
2. **`can_end` as a `custom_tooltip`-wrapped OR-ladder**, optionally
   externalised to a scripted trigger printed by the panel via
   `GetEndConditions` / `GetTooltipInformation` — one source of truth
   for logic AND display (Anno 1644 + HTC + ND, three independent
   attestations).
3. **Visible counter seeded by earlier chain choices** replacing RNG
   exits; **timed variables + `_fired` guards on a country pulse** so
   a chain survives its situation's early end (ND).
4. **The rubber band** for railroading an AI conqueror without capping
   a player (Timur).
5. **Map-mode mirror**: duplicate a situation's `lerp` colouring into
   a real map mode and force-select it on panel open (SOL); `lerp` is
   the only way to paint a NUMBER (3 vanilla users); vanilla's best
   secondary_map_color is Timur's declared-intent stripes
   (`situations/rise_of_timur.txt:354-362`) — a player's choice
   rendered on the map.
6. **Offsets documented against the real date** inline (Bronze Era's
   convention) — ours already does this in norman_conquest.txt; keep.
7. **Parked features shelved by comment across all files with zero
   orphan refs** (HTC's India) — the clean way to shelve.
