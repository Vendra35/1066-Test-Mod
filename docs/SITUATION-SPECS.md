> **STATUS (2026-08-03): UNIMPLEMENTED — the situations phase is NOW
> OPEN (both world phases closed and confirmed, items 1-44); this file
> is its primary input, to be read AFTER the vanilla+reference-mod
> craft sweep the next session opens with.** Two cautions before
> building from this:
> (1) **its Pecheneg route cites the DEAD SKE law** (AUDIT-2026-07-31
> §4.1 killed it — a tag needs BOTH a registry identity block AND a
> claims-backed landless start block; re-derive that spec before use);
> (2) the world under it has changed — 41 items landed since it was
> written; re-verify every tag/holding claim against the build. New
> banked situation material since: the Second Diffusion (TIBET §H —
> re-create the Sakya 1073/Jonang 1120 sect instances on schedule), the
> 1025 Chola-Srivijaya raid (SEA §H), Novgorod's Yugra tribute c. 1096
> (PERM-VYATKA §H), a Vinland/Markland thread (AMERICAS §0.8/§H), and
> the MEC khutba switch of 1071 + the Mustansirite Hardship (item 19).

# SITUATION SPECS — the 1066 backlog, ready to build

> Produced by the situation-spec research pass (Opus agent, 2026-07-29),
> reviewed by the main session the same evening: the three headline
> mechanism claims were re-verified by hand (byzantine_succession_crisis
> carries `tag = BYZ` and NO date/age gate — live at 1066;
> `coup_attempt.txt:8` is `NOT = { current_age = age_1_traditions }` —
> dead for our 276 years; `eng_henry_i` carries
> `father = eng_william_ii_rufus` at 05_characters.txt:733 — vanilla
> bug, Henry was Rufus's BROTHER). Historical dates below follow the
> flag convention; [V] rows cite vanilla's own setup data and are free.
>
> The quality bar (user, 2026-07-29): every situation needs a real
> PURPOSE, historical grounding, and flavor density; MR-scale
> multi-phase machines are the ceiling, not the floor.
>
> Build workflow per spec: add a SPECS entry to tools/new_situation.py,
> generate the inert skeleton, design the machine under the citation
> rule, delegate flavor prose, arm the gates + bump harness min_counts
> in the same commit, test in game.

**Date flags.** `[V]` = corroborated by vanilla's own setup data, cite
given. No flag = firm and universally attested but still general
knowledge. `[U]` = single estimate, unverified. `[D]` = sources
disagree.

**Identifier flags.** `EXISTS` = a character key in our generated
05_characters.txt. `OURS` = authored in build_setup.py's
NEW_CHARACTERS. `AUTHOR` = must be written.

---

## 0. THE TOOLBOX — what a spec may call for

Everything below is attested. Nothing in the twelve specs uses a
construct not on this list.

### 0.1 Four parallel "big event" systems, not one

| System | Directory | Owns | Native modifier block | Native map paint | Actions | Voting |
|---|---|---|---|---|---|---|
| **Situation** | `in_game/common/situations/` (22 vanilla) | global; countries opt in via `visible` | **no** | **yes** | yes | yes |
| **Disaster** | `in_game/common/disasters/` (**35 vanilla — never used by this mod**) | per-country | **yes** (`modifier = {}`) | map-mode link only | yes | no |
| **IO + special status** | `international_organizations/` (34), `international_organization_special_statuses/` (10) | membership | via policies | no | yes | yes (`resolutions/`) |
| **Movement** | `movements/` (4) | location/culture/religion | `add_movement_modifier` | no | no | no |

**The discovery of this pass: the disaster system exists and we have
never touched it.** `in_game/common/disasters/readme.txt:3-12`
documents `custom_description / monthly_spawn_chance / modifier /
can_start / can_end / on_start / on_monthly / on_end / map_mode /
fire_only_once`, plus undocumented `image` (35/35 files) and
`content_priority`. A disaster is the *country-scoped* sibling of a
situation and the **only one of the two with a native modifier block**
— `disasters/byzantine_succession_crisis.txt:37-44`:
`monthly_pretender_rebel_growth = 0.01`,
`global_crown_estate_power = -0.2`,
`blocked_from_creating_subjects = yes`.

Two consequences, both large:

- **`byzantine_succession_crisis` is LIVE at 1066** (re-verified). It
  carries zero date or age gates, `tag = BYZ`, `fire_only_once = yes`,
  `monthly_spawn_chance_very_high`, and fires on
  `stability < 50 / legitimacy < 80` with a weak heir
  (`byzantine_succession_crisis.txt:9-32`). It ships pretender rebels,
  a ten-branch event pool, `plotting_rebellion_modifier` character
  sweeps and its own actions
  (`generic_actions/succession_crisis_actions.txt`). Spec 1 should
  *drive* it, not duplicate it. **NEXT-LAUNCH GREP: has it already
  been firing on our BYZ?**
- **`coup_attempt` is DEAD for our entire era** — `coup_attempt.txt:8`,
  `NOT = { current_age = age_1_traditions }`. The first cheap, measured
  content cost of the age-1 decision.

Date/age-gate census of all 35 disasters: only 12 carry any
`current_age`/`current_date` reference. The rest are tag- or
character-gated — `castilian_civil_war` is bolted to Trastámara
characters (`castilian_civil_war.txt:9-38`) and cannot fire in 1066.

### 0.2 Situation fields — readme + the four undocumented ones

`in_game/common/situations/readme.txt:4-18`: `custom_description`,
`monthly_spawn_chance`, `international_organization_type`,
`resolution`, `voters`, `can_start`/`can_end` (root = situation),
`visible` (root = country, `scope:target` = situation),
`on_start`/`on_monthly`/`on_ending`/`on_ended`, `tooltip`
(root = location), `map_color`, `secondary_map_color`.

Used in vanilla but **absent from the readme**: `hint_tag` (22/22
files, `hundred_years_war.txt:3`), `legend_key` (79 uses, sub-fields
`desc`/`color`/`require_color_on_map`,
`guelphs_and_ghibellines.txt:479-483`), `is_data_map` (2 uses,
`black_death.txt:216`), `content_trigger` (1 use,
`rise_of_the_ottomans.txt:5-9`).

**A situation has no phase field and no modifier field.** Phase is a
situation-scoped variable — `on_action/_hardcoded.txt:825-833`
(`#move the situation from stage 1 to stage 2`,
`situation:treaty_of_tordesillas = { set_variable = {
name = var_treaty_phase value = { value = 2.0 } } }`). Read back as
`situation:<key>.var:<name>` (`rise_of_the_ottomans.txt:23`) and in
GUI as
`SituationView.GetActiveSituation.GetSituation.MakeScope.GetVariable('<name>')`
(`gui/panels/situation/black_death.gui:25`).

### 0.3 Situation ACTIONS — supported, and we have never shipped one

`generic_actions/readme.txt:5` lists `situation` among the legal
`type` values; 22 vanilla files declare situation actions. The
universal binding shape (`generic_actions/black_death.txt:1-39`) is a
`select_trigger` with `looking_for_a = situation`,
`target_flag = recipient`, gated on `situation:<key> = this` +
`situation_is_active = yes`. Fields: `potential / allow / price /
ai_tick / effect / ai_will_do / cooldown / show_in_gui_list`
(`generic_actions/readme.txt:8-76`), and a per-select_trigger
`map_mode`/`map_color` that recolours the map during target selection
(`:56-59`). Our own Mongol Resurgence ships one (`MR_actions.txt:33`,
modelled on `rise_of_timur.txt:288-385`) — proven in our hands, just
not in this repo.

### 0.4 Factions = International Organizations

There is **no situation member list and no `add_to_situation`
effect.** Participation is three layers:

1. **Gate** — the `visible` trigger; queried with `can_see_situation`
   (`triggers.log:2922`).
2. **Roster** — a global variable list built in `on_start`:
   `add_to_global_variable_list = { name = eligible_beylik_list
   target = this }` (`rise_of_the_ottomans.txt:44`).
3. **Sides** — real IOs joined from a situation action:
   `join_situation_faction = { target = scope:actor
   international_organization = scope:target join_variable = …
   join_years = 5 leave_variable = … }`
   (`generic_actions/guelphs_and_ghibellines.txt:95-105`) →
   `add_country_to_international_organization`
   (`scripted_effects/situation_effects.txt:29-32`); leaving at
   `:50-86`.

Guelphs/Ghibellines is the whole pattern in one file, and its two
faction IOs were among the 18 future-dated IO instances our build_ios
strips (1125) — the IO *types* are free for us at 1066.

### 0.5 Voting

Situations may bind a resolution:
`resolution = "western_schism_resolution"` +
`international_organization_type = catholic_church`
(`western_schism.txt:4-5`); `voters = council_of_trent_voters`
(`council_of_trent.txt:5`). Effects: `propose_resolution`
(`effects.log:7631`), `set_vote` (`:10402`), `remove_vote` (`:9876`),
`end_vote` (`:1540`), `end_resolution` (`:3389`).

**23 vanilla resolutions ship**, including `libertas_ecclesiae.txt` —
the Gregorian reform's own slogan, no date gate
(`resolutions/libertas_ecclesiae.txt:5-8`) — plus
`00_excommunicate.txt`, `dei_gratia_rex.txt`, `call_crusade.txt`,
`in_coena_domini.txt`, `hre_election.txt`, `high_kingship_election.txt`.

### 0.6 Effect vocabulary these specs draw on (all `effects.log`)

| Effect | Line | Scopes → Targets | Used by |
|---|---|---|---|
| `activate_situation` / `end_situation` | 12 / 1535 | none → situation | chaining situations |
| `set_new_ruler` / `set_new_foreign_ruler` | 10245 / 10235 | country → character | every coup and succession |
| `remove_ruler` | 9822 | character → country | depositions |
| `set_as_designated_heir` | 10040 | country → character | succession steering |
| `kill_character` / `_silently` | 3554 / 3559 | any → character; `location`/`killer`/`reason` | scripted deaths |
| `create_rebel` | 1296 | country → rebels; `data = { category government culture religion estate }` | pretenders |
| `start_civil_war` | 10471 | **rebels** → country | Byzantine 1077-81, Sancho/Alfonso |
| `start_revolt` | 10493 | rebels | lesser risings |
| `set_rebel_demands` / `support_rebel` / `destroy_rebel` | 10304 / 10523 / 1465 | | |
| `change_location_owner` | 911 | location → country | ownership handover — HALF of vanilla's triple (+ `add_core` + `change_integration_level = core`, fall_of_delhi.txt:299-301); the "SKE law" is dead (AUDIT-2026-07-31 §4.1) |
| `create_country_from_location` | 1230 | location → country | generated-tag splinters only |
| `change_location_controller` / `change_control` / `change_siege_progress` | 901 / 750 / 1036 | location | sieges as events |
| `make_subject_of` / `change_subject_type` / `cancel_subject` | 3610 / 1044 / 678 | country | tributary/vassal surgery |
| `add_casus_belli` / `declare_war_with_cb` / `white_peace` | 75 / 1391 / 10607 | | |
| `add_bonus_warscore` | 62 | war | battles as events |
| `add_country_modifier` / `add_character_modifier` / `add_dynasty_modifier` | 106 / 79 / 151 | `mode = add / add_and_extend / replace` | the flavour layer |
| `add_stability` / `add_legitimacy` / `add_prestige` / `add_manpower` / `add_war_exhaustion` / `set_war_exhaustion` | 453 / 248 / 343 / 272 / 586 / 10405 | | |
| `add_estate_satisfaction` / `grant_estate_privilege` / `bribe_estate` | 162 / 3452 / 650 | country | **no `add_estate_loyalty` exists** |
| `research_advance` / `add_reform` | 9892 / 379 | country | |
| `found_dynasty` / `create_named_dynasty` / `create_character` | 3434 / 1274 / 1216 | | runtime cast |
| `annex_country` / `force_union` / `transfer_subject` | 616 / 3420 / 10556 | | |
| `international_organization_add_special_status` | 3510 | international_organization | curia seats |

`add_opinion_mutual_effect` / `remove_opinion_mutual_effect` are
scripted effects, vanilla-attested inside a situation
(`hundred_years_war.txt:54-57`, `:149-152`); our Norman Conquest uses
them and the −1000 wall was observed in game.

### 0.7 Two things the engine does NOT have

- **No character imprisonment.** Only unit-level POWs
  (`ransom_prisoners` effects.log:9506, `execute_prisoners` :3376,
  `has_prisoners` triggers.log:5275). Romanos IV's captivity is a
  modifier + variable + events.
- **No scripted battles.** Battles are events plus
  `add_bonus_warscore` / `add_war_exhaustion` / `kill_character` /
  `change_location_controller` — exactly what the Norman Conquest
  already does.

### 0.8 Our own standing laws that constrain every spec

All measured in game; sources KNOWLEDGE.md/HANDOFF.md:

1. Situations own their lifecycle (timeline in `on_start`).
2. A situation spawns on the FIRST MONTHLY TICK after `can_start`
   passes — anchor day offsets to that tick.
3. No event-level `trigger` blocks; guards inside options.
4. CB first, declaration second.
5. Opening-week wars are SHIPPED in 16_wars, never declared; the
   game-start declaration lock is ~45 days. **Open assumption: it is
   a game-start lock only — the first situation declaring a war after
   year 1 (spec 5) measures this. That answer gates specs 2, 6, 8,
   11, 12.**
6. `prev` is one scope hop.
7. Every situation lands WITH its `.gui` panel (no BOM).
8. The flavour stack is four small additive files (named color,
   static modifier, bias, loc) — in-repo templates exist.
9. `tools/new_situation.py` scaffolds the skeleton, inert.
10. Loc keys: `<key>`, `<key>_desc`, `<key>_info`, `<key>_monthly`
    (situations_l_english.yml:357-372) + `<hint_tag>` and
    `<hint_tag>_hint_text` (hints_l_english.yml:593-594) — we have
    never shipped a hint entry.
11. Tributary rings: reform for monarchy-over-monarchy (4 proven
    instances); tribe subjects pass free.
12. Raise harness `min_count`s in the same commit as new content
    kinds.

---

## THE TWELVE SPECS

### 1. THE ROAD TO MANZIKERT — the Byzantine crisis, 1067-1081 · L

**Purpose:** the player watches (or plays) the unbeatable-looking
empire destroy itself in fourteen years, and faces Byzantium's real
choice — hold the themes or hold the capital — as a real, losing one.

Beats: Constantine X dies 1067.5.23 [V, term :13194]; Romanos IV
crowned 1068.1.1 [V :13196]; Bari falls 1071.4.16; **Manzikert
1071.8.26** (`malazgirt` exists); the release on terms [U]; the
Doukas coup [V≈ :13198 opens 1071.10.1]; blinding + death of Romanos
1072 [D]; Roussel's Norman state 1073-74 [U]; Philaretos in Antioch
[U]; Bryennios + Botaneiates 1077-78 [V :13204]; **Nicaea handed to
Suleiman ibn Qutalmish 1077** [U] — Rum born from a civil war;
Alexios I 1081.4.1 [V :13207]; Dyrrhachium 1081.10.18 → spec 2.

**Cast: twelve alive in OUR data** (the death-strip resurrection):
Constantine X (seated), Romanos IV (**vanilla bug: carries
Constantine's birth AND death dates — b.1006/d.1067.5.23 vs his own
term to 1071.10.1; real b.c.1030 — fix in build_setup with this
spec**), Eudokia, Michael VII, the Caesar John Doukas, Andronikos
Doukas (the traitor), Botaneiates, **Alexios (aged 9 at start, 24 in
1081 — exact)**, John Komnenos, Maria of Alania (daughter of OUR
seated Bagrat IV), George Palaiologos, Eirene Doukaina (born 1066!).
AUTHOR 5: Bryennios, Isaac Komnenos, Anna Dalassene, Roussel,
Philaretos. Seljuk side: Alp Arslan OURS; Malik-Shah + Suleiman ibn
Qutalmish AUTHOR.

**Mechanics:** phase variable (Tordesillas idiom); Romanos via
`set_new_ruler`; Manzikert as an event with pre-rolls,
`romanos_in_captivity` modifiers standing in for imprisonment;
**phase 3 DRIVES vanilla's own `byzantine_succession_crisis` disaster**
(push stability/legitimacy under its thresholds — its pretender
machine comes free) + `create_rebel`/`start_civil_war` for the named
revolts; **phase 4: the beylik release** — `change_location_owner`
over the 45 landless BYZ_LANDLESS tags, staged 1073-1081; **Rum needs
a NEW tag** (RUM is a formable name whose tag = TUR; free ids
verified: NIC, ICO). First situation ACTION: "Pay the Anatolian
tagmata" (price + cooldown, slows the release). Four-side map mode.

**Flavour:** the Reserve Did Not Come (the Doukas case, argued); the
captive's dinner (Alp Arslan's foot and hand); Two Emperors One
Purple; the blinding at Kotyaion (refusable); Roussel proclaims the
Caesar; "Sell the Bronze Doors" (Parapinakes); the bride from Alania
(cross-tag with our Georgia).

**Deps:** none — Byzantium/Seljuk/S.Italy all closed. **Choice:**
refuse the marriage, refuse battle, refuse the blinding, buy Suleiman
or fight two usurpers; SEL may ransom or keep Romanos.

### 2. THE NORMANS IN THE SOUTH — 1066-1091 · L

**Purpose:** twelve knights eat an island and a mainland; the player
rides with them or is eaten. County → kingdom in one lifetime.

Beats: Misilmeri 1068 [D] (Ayyub withdraws — OUR PLM ruler); **Bari
1071.4.16** (BYZ→APU); **Palermo 1072.1.10** (PLM→SIC); the brothers'
partition [U]; **Salerno 1076.12.13** [D] (SLR→APU, Gisulf deposed);
Richard of Capua dies 1078; Ceprano 1080 (→ spec 6); Dyrrhachium
1081 (→ spec 1); the sack of Rome 1084.5; Guiscard dies 1085.7.17;
Syracuse 1086 → Noto 1091 (AGR); **Malta 1091**.

**Cast:** every principal OURS and seated (item 22 confirmed).
AUTHOR: Bohemond, Roger Borsa, Sichelgaita.

**Mechanics:** four-siege phase machine (`change_location_owner`
batches + battle events); **the Melfi ring MOVES** — excommunication
`cancel_subject`, Ceprano `make_subject_of` (shares the mechanism
with spec 6); the brothers' rivalry as an opinion bias + a "Demand
your brother's half" action; Malta capstone. Amalfi has no location —
write around (recorded gap).

**Flavour:** the emirs' invitation (refusable); Bari's three years;
Palermo's surrender terms (a real tolerance choice); the trilingual
chancery; Sichelgaita at Dyrrhachium; the Cefalù mosaic.

**Deps:** item 22 ✅; wants spec 6 for excommunication beats (can ship
with no-ops). **Choice:** PLM/AGR may fight, submit, or evacuate;
the Lombard cities may buy, call Rome, or call Byzantium; the sack of
Rome is offered.

### 3. THE MUSTANSIRITE HARDSHIP — 1062-1073 · M

**Purpose:** the richest state on the map is four years into a
collapse nobody can see; the player chooses the humiliation that
saves it.

Beats: the Turkish–Sudanese army war (from 1062); seven low Niles
1064-72 [U]; Nasir al-Dawla takes Cairo and reads the ABBASID khutba
in Fustat 1067-68 [U]; the Cannibal Years; Mecca defects 1071.4.15
(spec 4); **Badr sails from Acre winter 1073** — OUR
fat_badr_al_jamali, authored and waiting since item 19; the one-night
purge 1074; amir al-juyush.

**Mechanics: OUR FIRST DISASTER** (native modifier block,
fire_only_once, map_mode — precedents: crisis_of_the_sayfawa,
decline_of_mali, tag-gated, no date gate). Severity variable driving
modifier tiers from on_monthly; the Nile as an annual random_list;
**Badr's rescue as the exit choice** — accept (disaster ends, the
caliph loses his powers to a permanent amir_al_juyush state) or
refuse (sovereign and starving). AUTHOR: Nasir al-Dawla; later
al-Afdal. The 1066 vizier stays unauthored (monthly turnover [D] —
item 19's recorded call).

**Flavour:** three servants and a mule; the library sold for shoe
leather; the 500-dinar dog; the Abbasid khutba inside Cairo; the
Armenian winter fleet; one night in Cairo.

**Deps:** item 19 ✅. Pairs with spec 4. **Choice:** every tier has a
priced mitigation; refusing Badr is survivable; a player FAT is never
annexed.

### 4. THE KHUTBA WARS — 1071-1075 · S

**Purpose:** sovereignty as a sentence spoken in a mosque. The
smallest situation in the bank and the best teacher of the Islamic
world's rules.

Beats: pressure 1069 [U]; **Abu Hashim reads the khutba for the
Abbasids 1071.4.15** (banked in build_setup as an event hook); Medina
follows; the 1075 reversal [U/D]; the permanent switch 1077 [U].

**Cast: NOBODY TO AUTHOR** — Abu Hashim, al-Qa'im, al-Mustansir, Alp
Arslan, al-Sulayhi: all five OURS and seated. Highest
flavour-per-hour in the bank.

**Mechanics:** tributary surgery on live rings (MEC leaves FAT's,
joins ABS's — **the one probe: runtime `add_reform` on ABS for the
gate**, effects.log:379; the setup-reform route is proven, the
runtime route is not); three timed modifiers; a −1000-style opinion
wall between the caliphates.

**Flavour:** the Friday the name changed (the sentence itself); the
patron's letter (fires to OUR YEM); the Abbasid caliph's one good
day; gold for a sentence; the pilgrim wells.

**Deps:** none. **Choice:** MEC runs a three-way auction; FAT pays,
threatens, or lets go.

### 5. THE THREE BROTHERS — Sancho II vs Alfonso VI, 1068-1073 · M

**Purpose:** what partible inheritance actually does; honour the will
or the kingdom's logic.

**Beats — ALL [V], vanilla's own terms:** the triple accession
1065.12.27 (:14521/:14736/:14791); Llantada 1068.7.19 [U]; García
deposed 1071.1.1 [V]; Golpejera 1072.1.12 [V — Sancho's LON term
opens]; Alfonso's exile to OUR al-Ma'mun of Toledo [U]; **Zamora
1072.10.7** [V — Sancho's death date and all three terms close];
Alfonso takes CAS+LON same day [V]; García imprisoned 17 years
1073.2.13 [V].

**Cast:** the three brothers seated (item 14); al-Ma'mun seated.
AUTHOR 3: **El Cid (ABSENT from vanilla entirely)**, Urraca of
Zamora, Elvira of Toro. **Trap: lon_urraca_i_jimena (b.1086) is the
DAUGHTER queen — never reuse for the sister.**

**Mechanics:** a situation, NOT the castilian_civil_war disaster
(Trastámara-gated, cannot fire). Three-side map. **THE
DECLARATION-LOCK PROBE: first war declared after year 1** — build
early for that measurement alone. Zamora as `kill_character` with
location/killer/reason. **El Cid as a travelling character modifier**
(el_campeador) moved by `change_character_allegiance` — hireable by
whoever, including the taifas (historically exact).

**Flavour:** the will; the wager Alfonso doesn't pay; "Zamora is not
taken in an hour"; Vellido Dolfos; **the oath of Santa Gadea** (El
Cid exiled for administering it); García buried in his fetters.

**Deps:** items 13-14 ✅. **Feeds spec 12.** **Choice:** all three
brothers playable and refusable; García can be warned.

### 6. LIBERTAS ECCLESIAE — the Investiture Controversy, 1073-1122 · L

**Purpose:** who appoints a bishop becomes who is above whom in
Christendom; pick a side in a four-year war with no army in it.

Beats: Alexander II dies 1073.4.21 (OUR seated Pope's exit);
Gregory VII acclaimed; Dictatus Papae 1075.3 [U]; Worms 1076.1.24
("descend, descend!"); the excommunication 1076.2.22; **CANOSSA
1077.1.25-28** (`canossa` exists, definitions:1162); Rudolf anti-king
1077.3.15; the Elster 1080.10.15 [U] (the hand); Clement III;
Henry crowned by his own pope 1084.3.31; the sack 1084.5 (spec 2);
Gregory dies at Salerno 1085.5.25; Worms Concordat 1122 = can_end.

**Cast:** Alexander II OURS-seated; **Henry IV EXISTS with vanilla's
own OGK term** — NOW SEATED with a demesne (item 23, crown decision
D). AUTHOR 5: Gregory VII, Urban II, Matilda (+ canossa dynasty),
Rudolf, Clement III. Vanilla's papal throne is EMPTY 1066-1119.

**Mechanics — the most vanilla reuse in the bank:** two faction IOs
via `join_situation_faction` (the G&G types are free at 1066 — our
build strips their 1125 instances); situation `resolution`+`voters`;
**`libertas_ecclesiae` ships as a dateless resolution**;
excommunication is a LIVE mechanic (cb_excommunication,
is_excommunicated, catholic_interactions) — fire it, don't build it;
the curia special status as franchise; move the cc_papal_authority/
cc_simony/cc_marriage_of_priest laws rather than invent parallels;
lay investiture itself is greenfield (zero vanilla content). The 1084
coronation is literally where vanilla's imperial term chain resumes
(:131).

**Flavour:** "descend, descend!"; three days in the snow AS A CHOICE
(both branches survivable); Matilda's castle; the hand at the Elster
(call it a judgment or a coincidence); two popes two Christendoms
(recognition visible on the map); "I have loved justice…"; the
Concordat nobody wanted.

**Deps:** ~~HARD BLOCK: the crown~~ — **UNBLOCKED by item 23** (OGK
landed, Heinrich seated, "King of the Romans"). Wants spec 2 for the
sack. **Choice:** every catholic country picks a side and may switch
(join_years cooldown); Canossa and the antipope are choices; neither
head is machine-annexed.

### 7. THE SULTAN'S BROTHERS — the Seljuk succession, 1072-1073 · M

**Purpose:** the empire is the family's property; the strongest
takes it — unless a Persian bureaucrat decides otherwise.

Beats: Alp Arslan dies on the Oxus 1072.11.24/12.15 [D] (the captive
castellan's knife — his recorded last words are the event);
Malik-Shah (17) succeeds because Nizam al-Mulk moves the treasury
first [U]; **Qavurt revolts 1073** — OUR seated, LIVE TRIBUTARY on
KRM; Hamadan; the bowstring [D]; the Siyasatnama era; Alamut 1090
(NO LOCATION — recorded gap; character-thread only).

**Cast:** Alp Arslan + Qavurt OURS-seated; the caliph OURS (the
diploma beat costs nothing). AUTHOR 3: Malik-Shah, Nizam al-Mulk,
Tutush.

**Mechanics:** kill + `set_new_ruler`; **Qavurt = a tributary
breaking its ring** (cancel_subject + cb_claim_throne + a normal 1073
declaration); design call: grant seljuk_nizamiyya_reform here instead
of setup (currently setup — defensible, Nizam is vizier from 1064);
the caliph's confirmation exchange.

**Flavour:** the last words; the bowstring; the Siyasatnama finished
the year its author is assassinated; the Nizamiyya of Baghdad; a boy
of seventeen; the Old Man of the Mountain sting.

**Deps:** none. Pairs with spec 1. **Choice:** designate an heir, buy
Qavurt, or fight; KRM may revolt, submit, or secede east.

### 8. THE NORMAN CONQUEST v2 — the flavour pass the machine owes · M

**Purpose:** make the 1066 winner pay until 1071 — the ætheling, the
Danish fleet, the Harrying, Abernethy.

Beats: Edgar proclaimed 1066.10.15 [U], submits December; Exeter and
the earls 1068; Durham burns 1069.1.28; **Sweyn's fleet in the
Humber 1069.9** (OUR seated DAN); **the Harrying, winter 1069-70**
(~100k dead); Sweyn bought off 1070; **Hereward and Ely 1070-71**;
Malcolm raids; **Abernethy 1072** (OUR seated SCO submits, hostage
son); the Revolt of the Earls 1075.

**Cast:** all central actors seated; `eng_william_ii_rufus` EXISTS
(b.1056). AUTHOR 4: Edgar Ætheling, Robert Curthose, Hereward,
Margaret of Wessex. **Fix in the same commit: vanilla bug #8 —
eng_henry_i's father says Rufus (his brother); must be the
Conqueror** — and author Curthose+Henry beside Rufus to cure the
engine's filler family (the HANDOFF backlog item lands here).

**Mechanics:** extend can_end to ~1072; phase 2 on the coronation;
**the Harrying as `add_location_modifier` on Yorkshire** (the
map-visible flavour; black_death's is_data_map as the model); Sweyn's
1069 CB+declaration (past the lock); Edgar as a travelling claimant
(change_character_allegiance); Abernethy as a temporary tie or
modifier.

**Flavour:** the six-week king; the Domesday sentence; the Danes
three years late; the sinking causeway of Ely; Malcolm's hostage and
marriage; the deathbed at Rouen 1087.

**Deps:** none — every file exists and is round-6 proven. **Choice:**
harry or garrison (mercy costs manpower and keeps revolts alive);
pay or fight Sweyn; press Scotland or take the submission.

### 9. THE SONS OF CYNFYN — the Welsh wars, 1069-1081 · S

**Purpose:** all of Wales as one comprehensible war a player can
actually win.

Beats: **Mechain 1069** (Rhiwallon dies — his character comment
already names it); the Rhymney 1072 (Maredudd dies); **Bleddyn
murdered 1075 [D]**; Trahaearn seizes Gwynedd; Rhys ab Owain killed
1078; **Mynydd Carn 1081** (Trahaearn AND Caradog die; Gruffudd ap
Cynan comes from DUBLIN with a Hiberno-Norse fleet); William marches
to St David's.

**Cast:** all five OURS-seated, rendering confirmed (item 21).
AUTHOR 3: Trahaearn, Rhys ap Tewdwr, Gruffudd ap Cynan (links spec
10).

**Mechanics:** pure event chain + kill/set_new_ruler; the five claim
lists partition wales_area 25/25 (Paradox's own border) so ownership
moves are trivially correct; tribe-to-tribe ties gate-free; no new
CBs.

**Flavour:** the brothers installed by a dead Englishman; Mechain
(everyone dies); the Hiberno-Norse fleet; the Laws of Hywel Dda; the
stone castle at Chepstow.

**Deps:** item 21 ✅. **Choice:** five playable kingdoms; every murder
is a declinable plot.

### 10. THE KING OF THE ISLES — Godred Crovan, 1066-1095 · S

**Purpose:** the underdog — from Stamford Bridge survivor to king of
an Irish Sea empire.

Beats: escapes Stamford 1066.9.25 (fires DURING the Norman
situation); **Sky Hill 1079** [U]; Man + Hebrides + Dublin's
overlordship; takes Dublin 1091 [U]; expelled by Muirchertach 1094
(EXISTS, b.1050); dies on Islay 1095.

**Cast:** Murchad OURS-seated on DUB; Diarmait crowned High King
(live IO); MCM seated. AUTHOR: **Godred + crovan_dynasty — THE
RUNTIME-CAST PROBE**: `create_character` + `found_dynasty`
(the Rise-of-Timur route, never yet used by us). LOI/MNN rulers are
deliberately random — the empty thrones this fills.

**Mechanics:** runtime creation, then set_new_ruler +
change_location_owner; three attempts as rising random_list rolls;
the 1091 Dublin phase touches the High Kingship members (proven
surgery).

**Flavour:** the survivor of someone else's disaster; Sky Hill's
hidden 300; "Crovan" [D] (say so in the tooltip); a sea-kingdom map
mode; Dublin ×4 in four years.

**Deps:** item 21 ✅; build after spec 8 (the Stamford hook).
**Choice:** playable from either side; the attempts can be abandoned.

### 11. LEVOUNION — the Pecheneg war, 1087-1091 · M

**Purpose:** there is no army left, so buy one — the post-Manzikert
Byzantine method, shown whole.

Beats: the foederati backstory (HANDOFF's own PEC design note); the
Danubian lords 1072+; Tzelgu 1087 [U]; Dristra (NO `silistra`
location — gap); the 1090-91 winter at the walls + Tzachas's
two-front plan; **Levounion 1091.4.29** — "an entire people perished
in a single day".

**Cast:** Alexios EXISTS (34 in 1091). AUTHOR: Tzelgu, Tzachas, a
Cuman khan, a Pecheneg house. Vanilla has ZERO Pecheneg content.

**Mechanics:** **PEC instantiated BY EVENTS** (the banked philosophy:
a state earned, not set up) — BOTH registrations shipped at setup:
identity block (PYS law) AND a claims-backed landless `10_countries`
shell, because a start-blockless tag never exists at all and cannot
catch up (MR, live 2026-07-31; AUDIT-2026-07-31 §4.1/§4.15). Arrival
is the vanilla triple — change_location_owner + add_core +
change_integration_level = core (fall_of_delhi.txt:299-301) — with
religion/culture set by hand (registry fields are bookmark-init only);
annihilated back out in 1091. NOTE: the full runtime-arrival
combination is UNOBSERVED in game — probe it on a throwaway before
building the situation on it. The "Hire the Cumans" situation action
WITH A PRICE is the centerpiece; a permanent the_scythians_are_no_more
modifier. Map gaps recorded: silistra, sofia, pliska, adrianople,
levounion.

**Flavour:** the frontier already inside; Tzachas the emperor-emir;
the April ditty; buying the steppe with the steppe; the massacre,
unsoftened.

**Deps:** wants the steppe/Rus slice (a Cuman source); after spec 1.
**Choice:** hire, pay off, or fight alone; the annihilation never
applies to a player PEC.

### 12. THE CROSSING — the Almoravids and Sagrajas, 1085-1091 · L

**Purpose:** calling for help is how the taifas died. The Iberian
flagship.

Beats: Carmona eaten 1067 (QRM seated for exactly this); the
Abu Bakr → Yusuf handover 1072 (BOTH OURS, authored for it);
**Toledo falls 1085.5.25** (OUR seated TOL); the appeal 1086 —
"better a camel-driver than a swineherd"; the crossing at Algeciras
(SEV's own land) 1086.6.30 [U]; **SAGRAJAS 1086.10.23** (fought on
BDJ's ground); Aledo 1088; **the deposition cascade 1090-94**
(Granada, Seville — al-Mu'tamid to Aghmat — Badajoz); El Cid takes
Valencia 1094 (spec 5's thread lands).

**Cast:** thirteen emirs + Abu Bakr + Yusuf + Alfonso all OURS/
seated. AUTHOR 2: al-Mu'tamid (the poet-king), El Cid (shared).

**Mechanics:** three phases. **The parias as the design call**: a
tributary ring (khutba pattern #5 — monarchy under monarchy, reform
needed) vs a cheaper modifier pair — main session decides. TFL's
beachhead via change_location_owner (algeciras/gibraltar — the
honest route; no unit-spawn precedent exists). Sagrajas as an event
(warscore + exhaustion + named deaths + a permanent
disaster_at_sagrajas on LON). The deposition as a per-taifa
annex_country cascade with three attested outcomes offered each
time. The peninsula recolours twice in eight years.

**Flavour:** the camel-driver line (the subtitle); the Toledo bells
(the hanging Alfonso is talked out of — by the Muslims); the parias
receipt (a running number); the drums at Sagrajas; the fatwa from
Baghdad; Aghmat (the poet in the cell); the veil.

**Deps:** items 13-14 ✅; AFTER spec 5; the pop phase would improve
it — note, don't wait. **Choice:** pay, refuse, or call — and having
called, refuse deposition; LON presses or takes gold; TFL crosses or
stays; a player taifa is never machine-annexed.

---

## 13. SEEDS — too small for their own situation

| Seed | Date | Actors | Fold into |
|---|---|---|---|
| Shavur's death; Arran slides to SEL 1075 | 1067 [U] | OURS (key #5) | spec 7 |
| Carmona eaten | 1067 [U] | both OURS | spec 12 ph.1 |
| Ayyub's withdrawal to Ifriqiya | 1068/69 [D] | OURS + father | spec 2 |
| Conan II's poisoned gloves | 1066.12.11 | OURS | spec 8 |
| Baldwin V dies; Philip I comes of age | 1067.9.1 | both OURS | France flavour |
| William IV → Raymond IV of Toulouse (→ Crusade) | 1088-94 [D] | OURS; Raymond AUTHOR | Crusade prologue |
| Alamut (NO location — gap) | 1090.9.4 | AUTHOR | spec 7 sting |
| The Nizari schism: al-Mustansir dies, Nizar executed | 1094-95 | Nizar OURS | spec 3 coda |
| Kakheti under Aghsartan (KAK free, name_aghsartan missing) | 1058-84 | AUTHOR | Caucasus |
| The Hilalian catastrophe | ongoing | Tamim OURS | Maghreb |

---

## PRIORITY TABLE — recommended build order

Weights: (1) the era is empty 1066-1200 in vanilla — early first;
(2) flagship value; (3) unblocked today; (4) teaches a mechanism the
later ones need.

| # | Situation | Scale | Blocked? | Reason |
|---|---|---|---|---|
| 1 | **Norman Conquest v2** | M | No | every file exists; retires the below-the-bar debt; home of the Henry-I bug fix and William's real sons |
| 2 | **The khutba wars** | S | No | half a day, five seated thrones; proves runtime tributary surgery + runtime add_reform (needed by 11, 12) |
| 3 | **The three brothers** | M | No | vanilla's own terms ARE the timeline; **measures the declaration lock** — gates 2, 6, 8, 11, 12 |
| 4 | **The Welsh wars** | S | No | half a day; closes the British story |
| 5 | **Godred Crovan** | S | No | **the runtime-cast probe** (create_character + found_dynasty) — Malik-Shah/Gregory/Bohemond all depend on it |
| 6 | **THE ROAD TO MANZIKERT** | L | No | the flagship; first disaster-driving, first situation action; build after the cheap five teach the tools |
| 7 | **The sultan's brothers** | M | No | the direct sequel; shares Malik-Shah |
| 8 | **The Normans in the south** | L | soft (wants 6) | can ship with excommunication no-ops |
| 9 | **THE CROSSING** | L | after 5 | the Iberian flagship; Yusuf has waited since the Levant pass |
| 10 | **The Mustansirite Hardship** | M | No | our first disaster; Badr has waited since item 19 |
| 11 | **LIBERTAS ECCLESIAE** | L | **UNBLOCKED by item 23** | the most vanilla scaffolding; build now that OGK has a demesne |
| 12 | **Levounion** | M | soft (steppe slice) | the phase closer; carries recorded map gaps |
| — | Seeds | S | — | fold into hosts |

Phase shape: 1-5 ≈ three days → six situations live. 6-7 the flagship
week. 8-12 the second phase.
