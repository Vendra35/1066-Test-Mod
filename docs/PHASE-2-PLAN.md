# Phase 2 — making 1066 historical

> Phase 1 made the world *work*: full map, sane rulers, no error flood. It makes
> no claim to accuracy. Phase 2 is where accuracy is earned, region by region,
> each region shippable on its own.
>
> **Historical dates below are from general knowledge, not from a cited source.**
> They are good enough to plan with and should be checked before they enter a
> trigger. Technical claims carry their evidence the same way as everywhere else
> in this repo; where something is unverified it says so.

---

## The three mechanisms

### 1. Rulers — `HISTORICAL_RULERS` in `tools/build_setup.py`
A table of `tag -> character key`. The generator swaps that country's
`ruler = random` for the named character and asserts the tag was found.

**Verified:** the hook exists and the assertion fires. Not yet exercised with a
real entry.

Much of what a 1066 start needs is already in vanilla, because vanilla's regnal
chains reach back to 886 and it ships 7236 dated characters — 330 born
1000–1070, 188 of them adults in 1066:

| Tag | Character | Born | Died |
|---|---|---|---|
| `ENG` | `eng_harold_godwinson` | 1022 | 1066.10.14 |
| `NRM` | `eng_william_the_conquerer` | 1028 | 1087.9.9 |
| `DAN` | `dan_sweyn_estridsson` | 1019 | 1076.4.28 |
| `SCO` | `sco_malcolm_iii` | 1031 | 1093.11.13 |

**The `Died` column above is historical context, NOT data to enter.** A
character alive at start must carry no `death_date` — the engine reads a
post-start one as invalid and the character begins the game DEAD, silently
(measured in game; KNOWLEDGE.md). `build_setup.py` strips all future death
dates. Deaths that should happen on schedule — Harold at Hastings, Hardrada
at Stamford Bridge — are situation/event script, with player choice per the
human-choice rule.

### 2. New characters — generated, not additive
Norway has **no** character alive in 1066 in vanilla (`nor_` prefix, zero hits),
so Harald Hardrada has to be written. Two routes:

- **Additive file** (`character_db = { … }` under a new filename). The wiki says
  setup managers are additive, and adding rather than removing is exactly what
  that supports. **Unverified here for `character_db`** — but Basileia Romaion
  ships exactly this at scale (`05_br_characters.txt`, 2359 lines, referencing
  vanilla parents and dynasties across the file boundary), so the route has a
  published precedent. For dynasties the picture is the reverse: Rise of Timur
  shipped its additive `dynasty_manager` file fully commented out and creates
  the dynasty at runtime with `found_dynasty` (character scope,
  `effects.log:3434`). Both entries in `docs/KNOWLEDGE.md`.
- **Generate `05_characters.txt`** as vanilla's plus ours, the way
  `10_countries.txt` and `15_international_organizations.txt` are already
  generated. **Chosen** — it removes an unknown, and the file stays regenerable
  after a patch instead of becoming ours to maintain.

Ordering rules apply and cause crashes rather than errors: dynasties must exist
in `dynasty_manager` before the characters that use them, and children must be
written after their parents.

### 3. Situations — purely additive
New files in `in_game/common/situations/`. Vanilla's 23 are left untouched.

**Vanilla's situations do not need re-dating.** Because the calendar stays
aligned to real years, `hundred_years_war` still fires in 1337,
`black_death` in 1347, `reformation` in 1517. What is missing is
**1066–1337 — 271 years for which vanilla ships nothing**, because it never had
to.

Field list is authoritative in `in_game/common/situations/readme.txt`:
`can_start` / `can_end` (root = situation), `visible` (root = country),
`on_start` / `on_monthly` / `on_ending` / `on_ended`, `monthly_spawn_chance`,
`map_color`, `international_organization_type`, `resolution`, `voters`.
Initial state goes in `main_menu/setup/start/22_situations.txt` via
`situation_manager = { }`.

**Design rule carried from CLAUDE.md:** whatever the AI is railroaded into, a
human player is asked. Conversions are offered and refusable, forced wars arrive
as a visible event with a postpone option, failsafes are `is_ai`-gated on both
sides and never take a player's land.

---

## Region order

Each region is done when its rulers are real, its borders are 1066's, and its
defining events exist as situations.

1. **North Sea** — England, Normandy, Denmark, Norway, Scotland. First because
   the opening decade carries itself and most characters already exist.
2. **France and the Empire** — the Capetian demesne is tiny in 1066 and the
   great vassals are effectively independent; the HRE needs its 1066 membership
   rather than vanilla's 200+ 1337 statelets.
3. **Iberia** — taifas, León-Castile, Aragón, and the Almoravid intervention.
4. **Byzantium and Anatolia** — pre-Manzikert borders, Seljuk arrival.
5. **The Levant** — Fatimid Egypt, Seljuk Syria; the ground the First Crusade
   lands on.
6. Everything else, in whatever order the work suggests.

---

## Situation backlog, 1066–1337

Priority: **A** = a 1066 mod is not credible without it. **B** = strong period
flavour. **C** = nice to have.

### 1066–1100
| Pri | Event | Dates | Notes |
|---|---|---|---|
| A | **Norman Conquest** | 1066 | Stamford Bridge 25 Sep, Hastings 14 Oct, coronation 25 Dec. Three claimants at once. The opening. |
| B | Harrying of the North | 1069–70 | Consolidation, unrest, depopulation of Yorkshire |
| A | **Investiture Controversy** | 1076–1122 | Gregory VII vs Henry IV, Canossa 1077, ends at the Concordat of Worms. The defining Papacy–Empire struggle; an IO-flavoured situation |
| A | **First Crusade** | 1095–1099 | Clermont Nov 1095, Jerusalem 15 Jul 1099. Creates the Crusader states |
| B | Norman conquest of Sicily | to 1091 | Palermo 1072; ends Muslim rule in Sicily |
| B | Almoravid intervention in Iberia | 1086– | Sagrajas 1086 halts the Reconquista for a generation |

### 1100–1200
| Pri | Event | Dates | Notes |
|---|---|---|---|
| B | Crusader states consolidate | 1100s | Jerusalem, Antioch, Tripoli, Edessa |
| B | The Anarchy | 1135–53 | Stephen vs Matilda; English civil war |
| B | Fall of Edessa → Second Crusade | 1144, 1147–49 | The crusade that failed |
| B | Angevin Empire | 1154– | Henry II holds England and half of France |
| A | **Saladin and the fall of Jerusalem** | 1171–1187 | Egypt 1171, Hattin and Jerusalem 1187 |
| A | **Third Crusade** | 1189–92 | Richard I; Barbarossa drowns 1190 |
| C | Almohads replace Almoravids | ~1147 | |

### 1200–1300
| Pri | Event | Dates | Notes |
|---|---|---|---|
| A | **Fourth Crusade and the Latin Empire** | 1202–04, to 1261 | Constantinople sacked; Byzantium shattered. Arguably the single most consequential event of the period |
| A | **Las Navas de Tolosa** | 1212 | Breaks Almohad power; the Reconquista becomes unstoppable |
| A | **Mongol invasions** | 1206–1260 | Unification 1206, Khwarezm 1219–21, Rus 1237–40, Legnica and Mohi 1241, Baghdad 1258, Ain Jalut 1260. **Reuse the Mongol Resurgence state machine with shifted trigger years** |
| B | Magna Carta | 1215 | Vanilla already ships `magna_carta_reform`; gate it on the date instead of granting it at start |
| B | Teutonic Order in Prussia | 1226– | Baltic crusades |
| B | Later crusades | 1217–54 | Fifth, Sixth, Seventh |
| A | **Byzantine restoration** | 1261 | Michael VIII retakes Constantinople |
| B | Sicilian Vespers | 1282 | |
| A | **Fall of Acre** | 1291 | End of the Crusader states in the Levant |

### 1300–1337 — bridging into vanilla
| Pri | Event | Dates | Notes |
|---|---|---|---|
| B | Suppression of the Templars | 1307–12 | |
| B | Avignon Papacy | 1309– | Vanilla's `western_schism` picks the thread up later |
| B | Scottish Wars of Independence | to 1314 | Bannockburn |
| B | Great Famine | 1315–17 | Precedes vanilla's `black_death` (1347) |

By 1337 the world should hand over cleanly to vanilla's own situation set.

---

## First deliverable — North Sea 1066

**Status: written and validated, NOT yet observed in game.** Steps 1 and 2 are
done; step 3 is not started.

**Scope**
1. ~~`HISTORICAL_RULERS` gains `ENG`, `NRM`, `DAN`, `SCO`~~ — **done**, plus
   `NOR`. Five entries, four of which needed no new character.
2. ~~`05_characters.txt` becomes generated~~ — **done**. Gained
   `nor_harald_hardrada`, `nor_magnus_ii`, `nor_olaf_iii_kyrre`.
   `fairhair_dynasty` already existed in vanilla, so `dynasty_manager` was not
   touched.
3. `situations/norman_conquest.txt` plus events, CBs, wargoals, on_action and
   localisation — **written and statically proven, NOT yet observed in game**.
   The timeline is on_action-driven and day-exact; the AI is railroaded to
   history and the player is asked at every fork. See HANDOFF for the
   in-game test checklist.

**What makes it interesting, and what makes it hard.** Nothing happens on its
own: future death dates cannot be data (they start the character dead —
KNOWLEDGE.md), so Stamford Bridge and Hastings only happen if the situation
makes them happen. Its job grew accordingly: stage the two invasions, script
the two deaths at their historical moments, route the successions — William's
claim, Hardrada's claim — and ask the player rather than railroad them.

**Verify before writing** (`verify-tags`): that `NRM`, `DAN`, `SCO`, `NOR` hold
the territory 1066 needs, and that the character keys resolve. `ENG` is real but
sits at `british_isles.txt:1` behind a BOM — a `^`-anchored grep will say it
does not exist.

**Then:** the harness gets a check that every `HISTORICAL_RULERS` character
exists in the generated `05_characters.txt` and is an adult at `START_DATE`,
proven by breaking it. Nothing else will catch a typo in a character key —
a bad reference does not error, it just leaves an empty throne.
