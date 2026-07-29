# Handoff — where the 1066 mod stands

> Written at the end of the first working session. Read `CLAUDE.md` first, then
> this, then `docs/KNOWLEDGE.md`. Everything below is either measured or marked
> as unverified.

## The Phase 2 slice: two engine laws found in one day, third test pending

**Test 1 (2026-07-28).** All five named-ruler countries under engine
regents; every `ruler = random` country fine. Law 1: **a named ruler does
not seat without an OPEN `ruler_term`** (no `end_date`, `start_date` before
`START_DATE`). Fixed: `HISTORICAL_RULERS` is now `tag -> (character,
accession, regnal number)` and the generator writes `ruler = X` plus the
open one-line term, vanilla's own form (`10_countries.txt:75`).

**Test 2 (same day, after that fix).** The term WORKED — Ruling History
shows "King Harold II Godwinson", crowned 6 January 1066 — but all five
rulers were DEAD at start, reigns closed on `START_DATE`, regents again.
Law 2: **a character alive at start must carry NO death_date** — a
post-start one is read as invalid and the character starts dead, with ZERO
error.log lines. Vanilla agrees: 4,304/4,305 of its death_dates are past at
1337 and living Edward III carries none. Both laws in `docs/KNOWLEDGE.md`,
with screenshots.

**Fixed and statically proven, NOT yet observed in game:** the generator now
strips every `death_date >= START_DATE` — 3,762 lines, resurrecting the
**260 vanilla characters alive in 1066** who were all starting dead.
Historical deaths on schedule (Hardrada 25 Sep, Harold 14 Oct) are now the
Norman Conquest situation's job — script with player choice, never data.

**Test 3 (same day): the kings LIVED — and the game froze.** All five alive
and ruling, randoms intact, both engine laws confirmed working. But the
full death-strip had also resurrected ~3,500 FUTURE-BORN characters
(collapsed births + no deaths = ancient and alive; init logged future-born
`sco_william_the_lion` as instantiated), and the game **hard-froze on the
first unpause** — debug.log cut mid-word, no flood, no crash. Test 1-2
ticked fine with those characters dead.

**Fix: the strip is now SCOPED to characters born before `START_DATE`** —
exactly 260 lines, matching the independent count of alive-in-1066
characters; the future-born keep their vanilla death_dates. Proven by
canary and harness ("no death_date on a character alive at start",
4,045 items).

**Test 4 (same day): ALL GREEN — the slice is CONFIRMED IN GAME.**
The freeze is gone, the game runs for months. Five kings alive and ruling —
Harold II, William II (NRM), Sweyn II, Malcolm III, Harald III — random
rulers intact, nobody dies on their own, and `error.log` is at **53 lines**,
back in the known-classified band. The North Sea RULER layer is done; what
remains of the first deliverable is `situations/norman_conquest.txt`, which
now also owns the two scheduled deaths and both successions.

## What works, measured in game

- Start date **1066.9.15**, age 1 (`age_1_traditions`), mod loads clean.
- The world is full — all 2337 country blocks, no territory lost.
- Rulers are sane. Before Phase 1 every ruler was the 1337 one, displayed at
  about **-250 years old**.
- A **~30,000-line script error flood** that filled `error.log` five times over
  is gone. It was downstream of the broken ruler data; nothing else changed.
- Error count went **30,000+ → ~300 → 48**.

## The 48 remaining errors, classified

None are parse errors. All are "1337 content wearing a 1066 date".

| Class | Count | Note |
|---|---|---|
| French appanages and Japanese imperial reform invalid | ~25 | **Caused by `ruler = random`** — the appanage trigger needs a Capetian dynastic link. Arguably correct: Normandy was not a French appanage in 1066 |
| Post-1066 institutions exist | 3 | Middle Kingdom (created 1271), Lordship of Ireland (1177), Tatar Yoke (~1240). 18 of 53 IOs are post-1066; only 3 complain |
| Unused modifiers | 2 | Left over from the 5 `timed_modifier` blocks we strip. Engine calls it "a waste" |
| Diplomatic relations over limit | 3 | Vanilla balance at our date |
| `gamestate.cpp:133` "Failed to read key reference" | 4 | **Unexplained.** No file named. No lead |

## Architecture

**`tools/build_setup.py` generates three files. They are never hand-edited.**
Re-run it after a game patch; it reads vanilla and rewrites ours.

```
main_menu/setup/start/05_characters.txt              vanilla's 7732 + our 3
main_menu/setup/start/10_countries.txt               62966 -> 57600 lines
main_menu/setup/start/15_international_organizations.txt
```

It strips everything carrying a 1337-dated person or date: 3852 `ruler_term`
blocks and 5 `timed_modifier` blocks from countries, 93 `ruler_term` blocks from
IOs, 174 `heir`/`consort`/`regency` lines, and **3,762 future-dated
`death_date` lines from characters** (546 pre-1066 deaths stay — they are
history on dead people). Then 861 named rulers become
`random`, 1360 already were, and 116 countries that had none get one — totalling
**2337, exactly the country count**. Phase 2 then seats its historical rulers
back on top: `ruler = X` plus an open past-dated `ruler_term` per entry.

`HISTORICAL_RULERS` at the top of the script is the Phase 2 hook: `tag ->
(character key, accession date, regnal number)`. The generator writes TWO
lines per entry — `ruler = <key>` plus an OPEN `ruler_term` — because a named
ruler does not seat without one. Five entries so far.

The script refuses to write unless: country count unchanged, exactly one ruler
per country, each historical ruler landed **in its own country**, no non-random
ruler is unaccounted for, exactly one open past-dated ruler_term per historical
ruler and no other, no FUTURE date survives in the country or IO files (one
documented exemption: TRE's `date = 1204.4.1`), braces balance, and every
historical ruler exists, is at least 16 at `START_DATE`, and acceded between
birth and `START_DATE`.

**Also shipped:** `loading_screen|in_game|main_menu/common/defines/*_1066_dates.txt`
— three identical copies of `START_DATE = "1066.9.15"` / `END_DATE = "1836.12.31"`.

## Traps that already cost time

1. **`setup/start` takes NO BOM.** It is the only BOM-free `.txt` tree — 25/25
   vanilla files, 25/25 in a published conversion. Everywhere else wants one. A
   BOM there is read as a token and the file goes **silently inert**; in a
   sibling project it crashed a new game. This produced a false conclusion here
   once: a probe "proved" additive setup files cannot redefine a country, when
   the file had simply never been parsed. **If a setup file appears to do
   nothing, check its first three bytes before concluding anything.**
2. **`name_harald` does not exist.** Name keys live in
   `in_game/common/languages/`. A missing one gives a nameless character, no
   error.
3. **`ruler =` sets the ruler; `ruler_term` is only regnal history.** But
   `ruler =` alone cannot fix a country whose `ruler_term` chain is future-dated
   — the engine seats nobody and generates a regent. That is why
   `10_countries.txt` is a whole-file override.
4. **Same filename = total replacement**, even if the mod's file is empty.
   Overriding `10_countries.txt` by name emptied the map once. A *new* filename
   is additive and merges key-by-key — verified in game — but can never *remove*
   an entry.
5. **Vanilla contradicts its own "children after parents" warning 614 times**
   and ships 8 dangling parent references. Validate what we wrote strictly,
   report what vanilla shipped.
6. **Count tags with `utf-8-sig`.** These files are BOM'd and the first tag sits
   on line 1 behind it; a `^`-anchored grep silently misses one per file. That is
   how `ENG` first appeared not to exist.

## Decisions taken, with their reasoning

- **1066 over 1178 and 867.** EU5 has one start date, so this was a one-way door.
  Everything before 1342 falls in a single age, so 1066 spends **276 years** in
  `age_1_traditions` (1178 would be 164, 867 would be 475). A new age means
  authoring 400–600 advances. 1066 was chosen on the setting with that cost
  accepted; the debt is unpaid and deliberate.
- **Whole map, two phases.** Phase 1 = the world works (`ruler = random`
  everywhere). Phase 2 = history, region by region. Phase 1 is done.
- **Ages untouched.** Vanilla's `age/00_default.txt` is not overridden. Because
  the calendar stays aligned to real years, vanilla's situations still fire
  correctly — Hundred Years War 1337, Black Death 1347, Reformation 1517. What is
  missing is **1066–1337, 271 years vanilla has nothing for**. That is the
  situation backlog in `docs/PHASE-2-PLAN.md`.
- **Defines mirrored to three trees.** Probably unnecessary — vanilla, a shipped
  balance mod and the wiki all use `loading_screen` only, against one conversion
  that mirrors. It works and logs no duplicate warning. Dropping the two extras
  deserves its own commit and its own launch.

## The Norman Conquest situation is BUILT — statically proven, NEVER launched

Six new files (2026-07-28, after the rulers were confirmed): the situation
(`in_game/common/situations/norman_conquest.txt`), 11 events
(`in_game/events/situations/norman_conquest.txt`), two CBs + two wargoals,
an `on_game_start` on_action that drives the timeline day-exact (the
situation's monthly tick is too coarse for Sep 20 – Dec 25), and 46 loc
keys. AI is railroaded to history; every alternative option carries
`trigger = { is_ai = no }`; a player England is offered submission in
event .42 instead of being force-unioned. Every construct is cited in-file.
The harness gained three checks (situation fields vs vanilla's field set,
event-id reachability in BOTH reference shapes, event/war/cb loc key
resolution), each proven by breaking.

**First launch FAILED, rebuilt (same day).** The on_game_start on_action
fired NOTHING in game, and the situation panel was empty — no per-situation
GUI file existed. Both causes and both fixes are in KNOWLEDGE.md: the
timeline now lives in the situation's own `on_start` (the MR lesson,
"situations own their lifecycle"), and `gui/panels/situation/
norman_conquest.gui` exists (MR's proven 45-line template). The on_action
file is deleted.

**Round 2 (same day): situation started, GUI fine, intro fired — nothing
else.** Two causes found and fixed (KNOWLEDGE.md): NRM was France's
appanage from vanilla's 1337 diplomacy and could not legally declare war —
`build_setup.py` now generates `12_diplomacy.txt` with the ten
engine-invalid French appanages stripped — and every event carrying an
event-level trigger went silent (hypothesis, not isolated), so guards
moved inside options and the two declarations retry monthly from the
situation while their window is open.

**Round 3 (same day): the machine WORKS.** Hardrada died and Magnus II
succeeded; Hastings killed Harold on 14 Oct; the coronation event fired ON
25 Dec, built the union, ended the war, William ruling both. Error classes
gone. Two flaws, both decoded (KNOWLEDGE.md): the declarations lagged a
monthly-retry cycle because a normal declaration needs the CB already in
hand — Norway's window closed with Hardrada's death, Normandy declared
1 Nov — fixed by granting both CBs in the situation's on_start and going
CB-first everywhere; and the panel's two cards sat far apart — the
wrapping expanding vbox was the cause, cards now sit directly in the
blockoverride like rise_of_the_ottomans.

**Round 4: panel fixed; wars still lag.** With CBs granted at on_start,
Normandy STILL declared only on 1 Nov — day 0 fails on something other
than the CB, and monthly retries cannot resolve what (the next attempt
after day 0 IS 1 Nov). Fix: hidden retry ladders at +1/+2 (Norway, before
Stamford at +3) and +1..+13 (Normandy), attested hidden-event shape.
Whichever rung fires measures the real lock.

**Round 5: the declaration lock is engine-side and unbeatable from
script** (even +1..+13-day hidden retries; Normandy declared 1 Nov for
the third round running). Solution shipped: `16_wars.txt` is now the
FIFTH generated file — vanilla's 13 future-dated wars and truces
stripped, our two 1066 wars in progress from day one (Norway since
1066.9.8, Normandy since 1066.1.6). Also fixed from this round: .42's
submit option now carries historical_option, and the NRM retry guards
gained `NOT = { in_union_with = c:ENG }` — reviewed, they would have
re-declared on their own union partner.

**Round 6: CONFIRMED WORKING END TO END.** Both wars live from day one,
Stamford on ~4 Oct with the succession and the withdrawal, Hastings on
14 Oct, the coronation and union on 25 Dec. The only new log signature —
`GetWinnerCountry returned nullptr` during the scripted war endings — is
decoded as harmless (no peace treaty means no winner for the toast to
name). **The Norman Conquest is done: the first Phase 2 deliverable is
complete and measured in game.**

**Polish pass v1 SHIPPED (untested in game):** situation map mode with
three side colors (map_NRM/map_NOR named colors added, map_ENG vanilla's),
legend keys, the norman_conquest_impact marker + opinion wall (-1000)
through the situation lifecycle, three timed flavour modifiers
(bled_at_stamford_bridge on the Stamford news, papal_banner on the
sailing, the_norman_yoke for 5 years on the AI submission AND the player
submission), and ENG's regnal table recalibrated so the Conqueror crowns
as William I, not III. Still open in polish: proper illustration, hint
entry, richer loc, Edgar Ætheling, Sweyn 1069, Malcolm.

**Polish v1 CONFIRMED IN GAME**: three-color map mode, all three timed
modifiers arriving, the Norman Yoke after the coronation, and William
crowns as **William I**. (The -1000 opinion wall was not explicitly
checked then; CLOSED — observed live in the Byzantium-batch launch,
2026-07-28.) New observation for
the backlog: the engine generates filler family for William — a
plausible 11-year-old son William, and an impossible 70-year-old
daughter. The fix is authoring his REAL family (Robert Curthose ~1051,
William Rufus ~1056, Henry 1068 — the next kings of England), same
NEW_CHARACTERS pipeline; goes with the Edgar Ætheling item.

**FRANCE LANDED (untested in game):** 28 historical rulers total now —
the North Sea five plus 23 French (18 straight from vanilla characters,
5 authored with 5 new dynasties in the additive
`04_zz_1066_dynasties.txt`, Anno 1644's attested route). MINOR_RULERS
carries FRA (Philip I, 14 — the engine regency IS the historical
regency). The opinion loc key the engine flagged is added.

## BATCH TEST — ✅ PASSED 2026-07-28 evening, all ten fronts

All 53 thrones verified (screenshots on file): the composite name renders
with diacritics (Petar Krešimir IV. Trpimirović), the language-row law
showed two more faces (Basque "Antso IV", Gaelic "Tanist Murchadh Ó
Cennsalach"), Tamīm rules the Sultanate of Tunis (dynasty-gated rank law
confirmed in game), the stripped IOs left zero invalid-leader errors, the
Norman opening ran clean, and both logs show ZERO mod-side error
classes. One finding, fixed same session: vanilla 1337 gives England six
subjects (Wales 1283, the Pale, the Aquitaine fiefdom…) — all stripped;
NEXT LAUNCH check: Aquitaine independent under William VIII, and the
still-unverified -1000 opinion wall between the 1066 claimants —
**both since CONFIRMED** (Byzantium-batch launch, 2026-07-28).

The original checklist, kept for the record:

## (was) BATCH TEST — one game session covers everything below

> Landings continue without per-batch game tests while the user is away
> (their call, 2026-07-28 evening); every batch is harness-green and
> build-asserted, and THIS list accumulates what the single catch-up
> session must check. Mechanism-class changes (borders, the crown, new
> situations) stay parked until testing resumes.

1. **Empire batch:** Bohemia = Vratislav II (Prague), Bavaria = Otto
   (Munich), Holland = Dirk 14 ruling directly (The Hague), Mainz =
   Siegfried, Louvain/Brabant = Henry (Brussels). Expect one new
   "child as a ruler" info line (HOL).
2. **Dynasty names round 2:** Flanders shows "Flanders" (not "Of
   Flanders"), Boulogne "Boulogne", plus "Nordheim" on Bavaria.
3. **Aquitaine:** the tag DOES exist — look at Bordeaux, named
   "Aquitaine", William VIII on the throne.
4. **Standing regressions:** Norman Conquest opening beats, France
   spot-checks, error.log against the ~53-line class profile.
5. **East + Iberia batch (LANDED, phone-approved):** Byzantium =
   Constantine X Doukas (Constantinople, regnal X), Georgia = Bagrat IV
   (Tbilisi), Castile = Sancho II (Valladolid — territory oversized but
   seatable), Navarre = Sancho IV (Pamplona), Aragon = Sancho Ramírez
   (Barcelona-capital anachronism noted). BYZ regnal numerals corrected
   for 1066 and the vanilla `name_andonikos` typo renamed to
   `name_andronikos` (value 0). 38 rulers total. Check the five thrones
   plus: does Constantine X display as "Constantine X"?
   Held for territory passes: LON/GLC/CAT (landless brothers' realms),
   the 14 taifas and the Great Seljuks (invent-a-country),
   TRE/CIL/CYP/CRT/BUL (Byzantine themes).

7. **North/East batch (LANDED, phone-approved):** Kyiv = Iziaslav I,
   Novgorod = Mstislav, Chernihiv = Sviatoslav II, Polotsk = Vseslav the
   Sorcerer, Sweden = Halsten, Poland = Boleslaw II, Hungary = the
   13-year-old Solomon (MINOR), Croatia = Petar Krešimir IV (composite
   name — check it renders!), Orkney = Paul. 47 rulers total. Check the
   nine thrones + Hungary's regnal display.
8. **Levant/Africa small batch (awaiting approval):** Yemen = Ali
   al-Sulayhi, Tunis = Tamim ibn al-Mu'izz (Zirid — the Hafsid styling
   auto-drops, dynasty-gated), Sijilmasa/TFL = Abu Bakr ibn Umar with
   Yusuf ibn Tashfin authored for the 1072 handover. All [U] birth
   years, literal names (vanilla's own Tashfin precedent), 4-5 new
   dynasties. Parked as invent-a-country slice #4: Fatimid Egypt (MAM
   naming trap), Abbasids+Seljuks (one job), Aleppo/Damascus; plus the
   Mirdasid religion dispute and the missing caliphate IO.

**Meanwhile prepared:** `docs/NEW-COUNTRIES-DESIGN.md` — the mechanism all
four invent-a-country slices block on, synthesized from the research
passes with a smallest-probe-first rollout (Pereyaslavl: one tag, eight
locations, a vanilla ruler). Three more research agents are digging
Italy+Papacy, Persia/Central Asia (the Seljuk body), and the Celtic world.

9. **Celtic batch (LANDED, phone-approved):** Leinster = Diarmait mac
   Máel na mBó (vanilla's own High King since 1064 — the high_kingship
   IO ships fully built and leaderless; seeding a character-type leader
   is an open probe), Munster = Toirdelbach Ua Briain, Connacht = Áed
   [U]. Murchad authored (patronymic showcase — should render
   "mac Diarmata"). 53 rulers total.
10. **Pre-test review findings (this session, per request):** the
   `Tamim` literal had NO loc entry — fixed, and the new
   authored-identifiers harness check (132 items, proven) now guards
   the whole class. 18 future-dated IO instances (Guelph/Ghibelline
   leagues 1125, Middle Kingdom 1271, Lordship of Ireland 1177…) are
   now STRIPPED by build_ios — expect the three IO-leader errors GONE
   from error.log and those IOs absent in game. 28 future-dated
   dependencies counted and parked. Italy/Persia reports in KNOWLEDGE;
   Italy quick win awaiting approval: VEN = Doge Domenico Contarini
   (vanilla character); PAP needs a regnal_name builder change first;
   the Great Seljuk slice has its full design brief.

11. **Italy quick wins + THE PROBE (LANDED, untested):** Venice = Doge
   Domenico Contarini (vanilla's own term date, machine-matched);
   Rome = Pope Alexander II via the NEW regnal_name term mechanism
   (character keeps his birth name Anselmo da Baggio; 17 undisputed
   papal regnal numbers recalibrated; capital corrected avignon→rome
   through the new CAPITAL_FIXES); and **PYS/Pereiaslav — the first
   invented country**: five left-bank locations out of Kyiv, Vsevolod I
   seated, no identity block (the SIC precedent under test). 56 rulers.
   NEXT LAUNCH: does Pereiaslav EXIST on the map with Vsevolod ruling
   (the probe's whole question); does the Pope display as
   "Alexander II" of "Rome"; Doge Contarini in Venice; Aquitaine now
   independent under William VIII; the -1000 opinion wall.
   **PROBE CONFIRMED IN GAME (2026-07-28, screenshots):** Pereiaslav on
   the map, Vsevolod ruling — but only after the tag-registry lesson
   (identity block MANDATORY, `zz_1066_new_countries.txt`).
   **The rest of the list CONFIRMED in the Byzantium-batch launch
   (2026-07-28):** the Pope renders "Alexander II" of "Rome", Doge
   Contarini in Venice, Aquitaine independent under William VIII, and
   the -1000 opinion wall observed live. Nothing from item 11 remains
   open.

12. **Sardinia giudicati slice (LANDED, untested):** first use of
   **LOCATION_GRANTS** — territory to EXISTING landless tags, the
   complement of NEW_COUNTRIES. 27 locations restored byte-for-byte from
   vanilla's own claim lists (`our_cores_conquered_by_others` IS the 1066
   border): TOR 8 (from GEN+ARB), CAG 7 (from PIS), GAL 4 (from PIS),
   COR 8 (from GEN+PIS+ARA); ARB kept its remaining 4. Ownership moved
   by a block-aware parser (`_owned_spans` over the ten own/control list
   keys) because sassari sits in GEN's ownership AND TOR's claims — a
   crude token scan double-counts. Granted tokens also stripped from the
   receiving tag's own claims list (27/27 found). Both new assertions
   proven by breaking (bogus location → abort; removal disabled →
   validate caught "sassari: 2 owners"). Rulers: TOR = Barisone I,
   CAG = Orzocco Torchitorio I (both authored, [U] dates, new
   lacon-gunale dynasty, home sassari); ARB/GAL/COR stay random
   (1066 holders obscure/unattested). 58 rulers total.
   TEST: Sardinia shows FOUR states + ARB; Corsica independent under COR;
   Barisone in Sassari, Torchitorio in Cagliari, Lacon-Gunale renders;
   GEN/PIS/ARA hold nothing on the islands; error.log for new classes.
   **CONFIRMED IN GAME (2026-07-28, screenshots):** all five states
   correct, both judges seated, Lacon-Gunale renders, Corsica
   independent, the mainland republics off the islands (ARA keeps its
   vanilla Mallorca vassal — correct). Two findings: (a) CAG and GAL
   were the SAME grey (vanilla never colored its landless tags) — fixed
   by the attested whole-file override of `in_game/setup/countries/
   italy.txt`, GAL now crimson; KNOWLEDGE has the override law.
   (b) 56 log lines `Event target link 'international_organization'
   returned an invalid object` in two Celestial-Empire interactions —
   our Middle Kingdom IO strip, zero impact, decoder entry added.
   RE-TEST (quick): Gallura renders crimson, distinct from Cagliari.

13. **THE TAIFA FACTORY (LANDED, untested):** thirteen Muslim states at
   1066.9.15 — SEV 28, BDJ 63, TOL 62 (holds Valencia, annexed 1065),
   ZGZ 22, GRZ 20, MRU 15, CRD 9, DYA 8 (with the Balearics), LRD 4,
   ABR 4, ALM 7, ALP 1 (capital chelva — alpuente has no location),
   QRM 1 (Seville eats it in 1067). 244 locations out of CAS/ARA/POR/
   GRA/MLL/MOR/NAV; GRA emptied to the LON landless shape with its 18
   ex-locations as claims (the Nasrid future). All from the Opus Iberia
   package, key claims re-verified; four new build assertions proven by
   breaking; 71 named rulers. THE HEADLINE QUESTION: the three INVENTED
   name keys (name_abbad Seville, name_badis Granada, name_abd_al_malik
   Cordoba+Albarracin) — legal in principle, never observed in game.
   TEST: (a) al-Andalus green/olive/ochre, thirteen states, all display
   "Taifa of X" (ESPECIALLY Granada — if it reads "Duchy of Granada"
   the GRZ/rank finding failed); (b) Abbad, Badis and two Abd al-Maliks
   RENDER THEIR NAMES (blank/raw-key name = invented keys failed);
   (c) al-Mu'tadid in Seville aged 50, al-Muqtadir in Zaragoza,
   al-Ma'mun in Toledo holding Valencia; (d) Balearics under Denia;
   (e) CAS/ARA/POR visibly shrunk, no orphan locations; (f) error.log
   new classes only. KNOWN LIMIT, tell the user BEFORE they zoom in:
   pops are still 1337-Christian — Castilian Seville is EXPECTED; the
   pop conversion slice is the named follow-up.
   **CONFIRMED IN GAME (2026-07-28, screenshots):** every point passed —
   all thirteen render as "Taifa of X" (Granada included: GRZ works),
   the three invented name keys render in their .arabic_language forms,
   donors shrunk, no orphans, log clean, Gallura crimson. The
   invented-name-key mechanism is now a PROVEN tool.

14. **CHRISTIAN IBERIA (LANDED, untested):** Ferdinand I's partition,
   written in vanilla's own data (all three sons' terms open 1065.12.27).
   123 locations: LON +34 (Alfonso VI), GLC +52 with the county of
   Portugal (García II), NAV +22 total (Basque provinces + La Rioja —
   vanilla itself marks the nine Basque locations as NAV cores),
   CAS 113→43 (Sancho II, capital Valladolid→Burgos — the town barely
   exists in 1066), ARA 26→6 (kingdom of Jaca; capital→jaca,
   court_language→aragonese_dialect via the NEW FIELD_FIXES mechanism),
   CAT landed with 13 as rank_county "Barcelona" (loc override; the
   "Catalonia"/"Aragon"-dynasty names are 12th-century anachronisms),
   six NEW county tags URG/BSL/CDY/EPU/RSL/PLJ (Bellonid/Empúries/
   Pallars houses; RSL's Guislabert II uses OUR name_guislabert — fourth
   invented key), POR and MLL LANDLESS with claims (67/9; POR capital→
   guimaraes), montpellier→FRA (Languedoc slice's problem), and ALL 27
   future-dated dependencies stripped (parked since Italy pass,
   user-approved; the strip's exact-count assert caught the
   trailing-comment regex blind spot — KNOWLEDGE).
   TEST: (a) the three brothers on their thrones (León/Galicia split
   visible), Sancho II in Burgos; (b) Navarre big (Bilbao–Logroño),
   Aragon tiny (Jaca); (c) County of Barcelona (NOT "Duchy of
   Catalonia"), house "Barcelona" (NOT "Aragon"); (d) six counties in
   the Pyrenees, Guislabert renders in Roussillon; (e) Portugal and
   Mallorca GONE from the map; (f) no orphan locations, error.log.
   **CONFIRMED IN GAME (2026-07-28, screenshots):** renders exactly as
   designed — the three brothers on their thrones, big Navarre, tiny
   Jaca, County of Barcelona, six Pyrenean counties, Portugal and
   Mallorca gone. (Recorded at the time only in commit 486163f's
   message; this paragraph closes the doc debt.)

15. **PRE-MANZIKERT BYZANTIUM (LANDED, untested) — the largest slice.**
   BYZ 87→582: all Anatolia (no Turkish state exists — raids only),
   the Balkans south of the Danube, the islands, Cilicia, the
   Antioch/Edessa ducates, the Cherson theme. The 495-location grant
   list is RESOLVED from definitions.txt at build time (the package's
   area/province rule set + explicit singles; my resolver independently
   reproduced the package's machine count — two implementations, same
   495). 45 donors go LANDLESS with claims = their pre-pass holdings
   (snapshotted at build time): all 21 beyliks incl. the Ottomans
   (Söğüt as a claim IS the post-Manzikert future), the Frankokratia,
   Bulgaria, Trebizond. Serbian world: Duklja (ZTA) restored with 9
   under Mihailo Vojislavljević (name_michael — IN the serbo-croatian
   pool; new vojislavljevic dynasty; block dynasty balsic→vojislavljevic
   via FIELD_FIXES), Rascia 13 (rank→duchy, capital prizren→
   trgoviste_SER = Ras), TRO 2, HUM 5, BOS 16 independent, RAG kept.
   TRE's 1204.4.1 themata bureaucracy + Grand-Komnenoi regnal blocks
   DELETED — **KNOWN_FUTURE is now the empty set**; taman → CHR
   (Tmutarakan was Chernihiv's). Perf: ownership ops went through one
   comment-masked index sweep per batch (the old per-location scan hit
   minutes at this scale AND could count comment words as holdings).
   TEST: (a) Constantinople rules from the Danube to the Euphrates —
   ONE purple empire, no beyliks, no Trebizond, no Frankish Greece;
   (b) Duklja under Mihailo (house Vojislavljević renders), Rascia/
   Bosnia/Ragusa/Croatia small and independent; (c) Bulgaria GONE
   (theme since 1018); (d) Cyprus+Crete+Rhodes+Aegean Byzantine;
   (e) Ani/Kars Byzantine, Georgia untouched under Bagrat IV;
   (f) error.log — expect a DROP (the -1000 opinion wall and IO noise
   partly came from now-landless tags).
   **CONFIRMED IN GAME (2026-07-28, screenshots):** one purple empire
   from the Danube to the Euphrates, the Serbian world small and
   independent around it. One real defect found: a ~318-line
   invalid-subject/nonexistent-overlord start flood — exactly 28 kept
   dependencies named a landless tag; fixed the same night in 486163f
   (build_diplomacy strips them, exact-count asserted, decoder entry
   added). This launch also closed the item 11 leftovers and the
   -1000 opinion wall (see above).

16. **THE SELJUK + ABBASID WORLD (LANDED, untested — TOMORROW'S TEST).**
   SEL = the Great Seljuks, 463 locations resolved from definitions.txt
   (rule set, exact-count asserted), a KINGDOM so the engine renders
   "Sultanate of the Great Seljuks" / "Sultan Alp Arslan" (empire rank
   would kill the NAME key — KNOWLEDGE). Alp Arslan seated via
   vanilla's own literal `Alp_Arslan`; vanilla seljukids_dynasty
   ("Al-e Saljuq") and map_seljukids color reused. ABS = Abbasid
   Caliphate, one location (Baghdad), al-Qa'im via the papal
   regnal_name route, THE THEOCRACY PROBE (see test list). Nine
   TRIBUTARY clients (war-capable — the corrected law): Kerman
   (Qavurt, vanilla name_qawurd), Mosul, Diyar Bakr, Aleppo (shia [D]),
   Sistan (random ruler), Yazd, Arran, Tabaristan (random), Hilla.
   GHZ (Ghaznavids, 34), SRV (Fariburz I) and ABS independent. 60 more
   tags landless (JAL keeps its horde government unrendered — the
   naming trap stays unarmed; new build assert: NO recipient may be
   horde/tribe, proven by breaking). Kharpert's 4 → BYZ (586), closing
   half the deferred Tier 2. 82 landless-tag dependencies + 5 pacts
   stripped, 9 tributaries added, 531 dependencies kept. Invented keys
   five-to-seven: Shavur, Fariburz, Dubays. 92 named rulers; 108
   landless tags; all 23 checks green.
   TEST (tomorrow): (a) "Sultanate of the Great Seljuks" across
   Iran-Iraq, Sultan Alp Arslan in Rey; (b) **THE PROBE: does ABS
   render "Abbasid Caliphate" with "Caliph al-Qa'im"?** If it shows
   "Abbasid Empire", the explicit government type lost to the include
   template — record it in KNOWLEDGE either way; (c) nine clients show
   the tributary subject line under SEL, keep their own colors, CAN
   declare war (spot-check one in the war interface); (d) Shavur/
   Fariburz/Dubays render; Qavurt in Kerman as "Al-e Saljuq";
   (e) Ghazna/Shirvan independent; (f) the Mongol-era Persia tags GONE
   (no Jalayirids, no Injuids, no Muzaffarids...); (g) error.log —
   the subject/overlord flood from the Byzantium test should be gone
   (28+54 dependency strips landed since), "removed invalid law"
   should shrink or vanish; the 'l' formatting flood is known vanilla.
   **TESTED 2026-07-29 (screenshots): 6/10 clean, 3 real bugs, all
   decoded same day.** PASSED: **the Caliphate probe — "Caliphate"/
   "Caliph" rendered, theocracy beat the include** (bonus finding: the
   branch prefix "Holy" came along); Alp Arslan in Rey; Shavur/
   Fariburz/Dubays render (invented keys 5-7 PROVEN); Qavurt/Al-e
   Saljuq; GHZ+SRV independent; Mongol tags gone; old error floods
   gone ("removed invalid law" hypothesis confirmed); Norman opening
   clean. FAILED, causes measured: (1) all nine tributaries were
   silently DOWNGRADED TO VASSAL — tributary.txt's visible gate binds
   at game start (government.cpp:3702 cites its lines 20-24);
   (2) SEL/ABS/clients could not see their own capitals — playing SEL
   showed terra incognita (expl_silk_road_center is an ALL-COMMENT
   vanilla template; no include contained Rey); (3) HLL under two
   overlords, repeating assert (vanilla's Mongol-era HLG vassalage
   survived + our SEL line); plus ABS include-clash errors
   (heir_selection/laws/school) and ARA's duplicated primary culture
   (which ANSWERED the deferred registry question). All fixed in
   item 17.

17. **SELJUK FIX BATCH (LANDED, untested) — everything the 16-test
   found, one commit pair.** (a) Tributary gate: NEW
   `seljuk_khutba_reform` (in_game/common/government_reforms/
   zz_1066_reforms.txt, malian_tribute_system's attested shape) grants
   SEL `allow_tributary_subject`; assigned in SEL's setup government.
   THE PROBE: does the reform's modifier land before the start
   validator? (b) Discovery: `expl_middle_east` (132 vanilla uses) on
   all eight generated blocks + ABS; build now asserts every new
   block's CAPITAL is inside some granted region/area/province
   (definitions.txt-resolved; first draft of the assert was proven
   inadequate by its own break test and strengthened). (c) HLG→HLL
   Mongol-era vassalage stripped (exact-count 1) — the
   multiple-overlord assert dies. (d) ABS rebuilt as an explicit
   theocracy: theocratic_elective, hanbali_policy + hanbali_school
   (Qadiri creed), no monarchy include — the heir/law/school error
   trio dies. (e) jafari_school on UQY/HLB/KKY. (f) ARA: registry
   override in_game/setup/countries/iberia.txt (catalan→aragonese,
   one line, Gallura route) — primary-duplicate error dies.
   (g) accepted_cultures = { farsi_culture } on SEL (user-approved:
   the Persian bureaucracy). (h) "Holy" dropped:
   rank_empire_theocracy_prefix loc-overridden to "".
   (i) Harness: "new-tag tributary overlords pass the subject-type
   gate" (9 items, proven both ways).
   TEST NEXT LAUNCH: (a) THE TRIBUTARY PROBE — do the nine clients
   now show as TRIBUTARIES (own colors, subject line under SEL), and
   can one open a war-declaration screen? If still vassals, the
   reform lost to init order: fallback is honest vassalage — decide
   then. (b) Play SEL: is Persia VISIBLE from Rey outward? Play a
   client (Mosul): world visible? (c) ABS panel reads "Abbasid
   Caliphate" — no "Holy". (d) error.log: the 3702 tributary lines
   for our nine GONE (CHA/DAI's two remain — known, China review),
   capital/heir/school/law/multiple-overlord classes GONE, ARA
   duplicate GONE. (e) SEL's Persian lands: integration/acceptance
   visibly better with farsi accepted. (f) Regression: taifas still
   render, Norman opening, error.log class profile.
   **CONFIRMED IN GAME (2026-07-29, second launch): ALL PASSED.**
   Nine tributaries with open war screens — **the reform beat the
   validator: a setup-assigned reform's country_modifier applies
   BEFORE the game-start subject check** — Persia visible, plain
   "Abbasid Caliphate", the fixed error classes gone. Residue decoded
   same session (decoder has all three): ABS's sharia_law removed
   (missing has_policy prerequisite), maritime privilege self-heals on
   our 12 inland blocks (coastal template), landless-shell law trims
   (accepted), and the tusi ×30 China class (our IO strip, parked).
   Also measured: farsi acceptance costs 3.89 capacity against 2.00 —
   a -47%/-47%/-19% penalty wall (screenshot). All fixed in item 18.

18. **SELJUK POLISH BATCH (LANDED, untested):** (a) ABS laws gain
   `legal_code_law = sharia_law_policy` — the sharia_law group's
   has_policy prerequisite. (b) The 12 engine-flagged inland blocks
   (CRD LRD ABR ALP QRM + GHZ UQY MRD HLB SIS KKY SHD) switch to
   `muslim_monarchy_no_abrahamic_dhimmi_no_coast` with heir_selection
   restated (the variant carries none — diff-measured). (c) NEW
   `seljuk_nizamiyya_reform`: cultures_capacity = 3 (the mandala
   reform's attested magnitude) — SEL's capacity 2.00→5.00, the farsi
   penalty wall dies. Harness reform-loc sweep now covers every mod
   reform (proven by breaking).
   TEST NEXT LAUNCH: (a) SEL society panel: capacity ~3.89/5.00, NO
   overflow penalty box, two reforms visible in the government screen
   with names rendered ("Recognition of the Khutba", "The Nizamiyya");
   (b) error.log: ABS sharia_law removal GONE, the 12
   sponsor_maritime_contracts removals GONE (landless-shell trims and
   tusi remain — known); (c) regression: tributaries still tributary,
   Persia still visible, taifa/client thrones unchanged.
   **CONFIRMED IN GAME (2026-07-29, third launch): ALL PASSED — THE
   SELJUK SLICE IS CLOSED.** Capacity 5.00 with the penalty box gone,
   both reforms render by name, ABS's sharia_law line gone, and the 12
   maritime removals gone — the user's pasted 3662 residue was checked
   tag by tag: all 28 flagged tags are landless shells
   (SELJUK_LANDLESS / BYZ_LANDLESS / GRA), NONE of the 12 no_coast
   blocks among them — decoder sub-class 3, accepted. Regression clean
   (nine tributaries, Persia visible, thrones unchanged). One NEW
   signature decoded and parked: CHI's accepted-culture flood
   (country.cpp:9635) is the Middle Kingdom strip again — the IO's
   leader_modifier carried cultures_capacity = 50 AND
   allow_tributary_subject (middle_kingdom.txt:69-75), so this flood,
   CHA/DAI and the tusi ×30 are ONE root cause, owned by the China
   review (decoder entry added).

19. **FATIMID EGYPT + SOUTHERN LEVANT (LANDED, untested).** FAT = the
   Fatimid Caliphate, 122 locations resolved from definitions.txt
   (MAM's remaining 119 + AAL's 3 Damascus-hinterland; exact-count
   assert proven by breaking). MAM landless with its 120 as claims
   (the Mamluk future); tobruk granted to BQA (1066 Barqa is
   Zirid-aligned Banu Qurra); BKZ keeps Aswan, MDA keeps al_ais.
   FAT is the ABS explicit-theocracy block's Ismaili variant:
   theocratic_elective, legal_code_law + sharia_law = ismaili_policy
   (vanilla's own pairing with ismaili_school — QHT :60609),
   rank_empire → "Fatimid Caliphate"/"Caliph" via the existing
   tag-independent rank overrides; discovery
   expl_muslim_mediterranean + expl_middle_east; capital cairo.
   Cast: al-Mustansir seated via regnal_name = Mustansir (FIRST
   LITERAL regnal_name — vanilla's Chungsuk precedent; Maad/Mustansir/
   Nizar are new invented literals), Nizar authored (clergy_estate —
   an eligible heir under theocratic_elective, not the designated
   one), Badr al-Jamali authored unseated (the Tashfin precedent),
   Abu Hashim seated on MEC (name_muhammad, new hawashim_dynasty).
   Two tributaries under fatimid_khutba_reform: MEC (khutba until
   15 Apr 1071 — event hook) and BKZ. NO vizier authored (monthly
   turnover in 1066 [D]); the Mustansirite Hardship (1062-1073) is
   future situation material. ALSO: all three mod reforms now carry
   government_reform_slots = 1 (user request — they no longer consume
   a reform slot; vanilla's own revolutionary_empire pattern,
   monarchy.txt:169). Landless-dep strip 82→90 (observed failing
   before the constant moved), country count 2367, tributary-gate
   harness check 9→11 items, 24 checks green.
   TEST NEXT LAUNCH: (a) "Fatimid Caliphate" from Cyrenaica's edge to
   Lebanon, EMERALD green, "Caliph al-Mustansir" (the literal
   regnal_name probe!) in Cairo; (b) THREE caliphate-styled states
   coexist — ABS "Abbasid Caliphate", FAT "Fatimid Caliphate", no
   "Holy" prefix on either; (c) MEC + BKZ show as tributaries under
   FAT (own colors, war screens open); Abu Hashim rules Mecca;
   (d) Mamluks GONE from the map; KOJ still absent (landless);
   Jerusalem/Damascus Fatimid; (e) SEL government screen: the two
   Seljuk reforms still render AND the reform-slot counter shows
   free slots (the government_reform_slots addition); (f) error.log:
   expect the landless-shell trim class to GROW by MAM's block (known,
   accepted); new classes only — the first coastal explicit theocracy
   is the one real unknown; (g) regression: nine Seljuk tributaries,
   Persia visible, taifa/Iberia/Norman opening unchanged.
   **CONFIRMED IN GAME (2026-07-29, same day, screenshots): ALL SEVEN
   PASSED — THE FATIMID SLICE IS CLOSED.** "Fatimid Caliphate" emerald
   across Egypt-Palestine-Lebanon-Hejaz coast, "Caliph al-Mustansir"
   in Cairo — **the literal regnal_name probe PASSED** (first
   non-name_key regnal_name, Chungsuk precedent proven in our data);
   both Caliphates styled, no "Holy"; MEC/BKZ tributaries with open
   war screens; Abu Hashim renders "Šayḵ Muḥammad Hawāshim" of the
   "Sheikhdom of Mecca" (hawashim_dynasty + name_muhammad confirmed on
   the debug panel); Mamluks gone, Barqa separate; **the reform-slot
   fix shows +1 free slot in game**; error.log grew by EXACTLY the
   forecast three MAM lines (education_masses + 2 privileges —
   decoder sub-class 3, accepted) and NOTHING else: **a coastal
   explicit theocracy produced zero new error classes — the ABS
   minimal-law shape is proven for coastal use too.** All standing
   classes unchanged (French appanage, tusi, landless trims — all
   decoded).

20. **FRANCE DEMESNE + LANGUEDOC (LANDED, untested — the user is away;
   test list ACCUMULATES, remote approvals continue).** FRA 164→29:
   the 1066 Capetian demesne (19: Île-de-France, Orléanais, Sens,
   the crown bishoprics) + 3 additions (etampes — ETA keeps gien;
   dreux — DRE empties, county created 1137; montreuil — ENG's 1279
   Ponthieu relic) + 7 Lyonnais/Vivarais kept as a KNOWING anachronism
   (Kingdom-of-Arles side, French only 1312 — banked for the Empire
   slice). 142 locations to 16 recipients via _FRANCE_RULES (exact
   counts, proven by breaking): TOU 39 (Toulousain-Quercy-Rouergue-
   Gévaudan-Narbonnais-Nîmois incl. montpellier — the Iberia-era
   parking RETIRED), AQN 31, BLS 20 (Champagne folded under Theobald),
   VLS 7, VMD 7, AUV 8, ANJ 6, MRC 6, BER 6, PER 3, FLA 3 (the 1305
   Lille relic returns), BUR 3, COM/RET/BAR 1 each. Four approved
   HISTORICAL moves ride along (rodez/lautrec from AMG, castres from
   VDM, thiers from FRZ). TOU/BER/VLS rise from landless (own claims =
   1066 borders); VMD is the one NEW tag (Vermandois — fresh over
   PIC-reuse, whose claims bundle Ponthieu). THE TIE REFORM: the 1337
   French web is GONE — 27 `first = FRA` vassal lines (war-blocking,
   the round-2 freeze class, sat on twelve seated thrones) + 4
   fiefdom sub-ties (fiefdom carries has_overlords_ruler = yes:
   BOU→MRC was overriding our Adalbert!) — and the six northern fiefs
   (FLA BUR BLS VLS VMD ANJ) return as TRIBUTARIES under
   capetian_homage_reform (khutba pattern #3). NRM/TOU/BRI/AQN and
   the Occitan south stay fully independent. Cast: William IV of
   Toulouse (vanilla's own TOU regnal table expects name_william =
   4), Raoul IV de Crépy, Herbert IV on vanilla's carolingian_dynasty
   ("Caroling" — the last Carolingian male line); BER stays random
   ([D] — Berry's 1066 holder genuinely disputed). Found and fixed on
   the way: vanilla definitions.txt ships a SELF-NESTED duplicate
   province (limousin_province wraps itself, :944-945) — the resolver
   now dedups within sweeps. 24 checks green, tributary gate at 17
   (proven by breaking: reform removed → all six FRA lines flagged).
   TEST WHEN THE USER RETURNS (accumulated list): (a) France is
   SMALL — Paris/Orléans core + Reims/Sens; Toulouse big and
   independent under "William IV" (Guilhèm? — the occitan_dialect
   name-fallback probe); Vermandois gold in Picardy under Herbert IV
   (house renders "Caroling"); Raoul IV in Soissons/Amiens; Berry
   under a random ruler in Bourges. (b) The six homage tributaries
   render with OWN colors and open war screens; SEL/FAT rings
   regression. (c) MRC: Adalbert II RULES AGAIN (the fiefdom override
   is gone — if he was a random before, this fix is visible);
   FOI rules only Foix (BRR/MDM freed); MIE independent. (d) DRE gone
   from the map, ETA = gien only, FRA holds montreuil. (e) SEL
   capacity 8.00 (the +6 Nizamiyya recalibration). (f) error.log:
   expect the French appanage class (~25 lines) GONE — the ten
   appanage lines died long ago but the 27-vassal web may have been
   feeding other classes; new classes only; the landless trims grow
   by DRE. (g) Norman opening regression — NRM untouched, but the
   whole French theatre changed around it: watch the two 1066 wars
   still fire.

21. **THE BRITISH ISLES (LANDED, untested — test list accumulates).**
   106 locations moved, 25 tags landless, 2 new tags (DUB, ULD), 2370
   country blocks, 8 new thrones. WALES: the ten marcher tags + the
   1267 WLS Principality dissolve into the six claimant shells whose
   claim lists partition wales_area EXACTLY 25/25 (Paradox's own 1066
   border): Bleddyn ap Cynfyn on Gwynedd, brother Rhiwallon on Powys
   (both Mathrafal — the house ships), Maredudd on Deheubarth
   (name_meredith → "Maredudd"), Cadwgan on Morgannwg, Caradog on
   Gwent (the 1065 Portskewett raid); ludlow/wigmore/oswestry
   (English-culture shires) → ENG. IRELAND: the Pale and the Norman
   earldoms undone — MCM 24, LEI 8, CNN 8, new DUB under **Murchad
   mac Diarmata, authored since the Celtic pass and seated at last**,
   MTH rises from landless under Conchobar Ua Mael Sechlainn, new ULD
   for Ulaid (random [D]). **THE HIGH KINGSHIP IS CROWNED:**
   `leader = LEI` seeded by the catholic_church precedent
   (leader = PAP, 15_IO:182 — the character-led-IO syntax), member
   surgery CLA/THO/CVN→MTH/DUB/ULD (27 conserved). **Six Irish
   tributaries with NO reform** — every subject is a gaelic tribe and
   tributary.txt:21's subject-is-a-tribe branch passes free (five
   vassal conversions + new LEI→DUB). SCOTLAND: **the SBL find** —
   the 1332 Balliol Pretender held Edinburgh/Perth/Stirling/Roxburgh
   at start ("Support from the English", revolt = yes); SCO
   reunified at 36 (+berwick from ENG — Lothian is Scottish from
   1018), Galloway independent (its own claim list), Moray under
   Mael Snechtai mac Lulaig (vanilla's loairn_dynasty; norman court
   language fixed to Gaelic; SCO→MOY and SCO→ROS vassalages
   stripped — Malcolm's reign was a war AGAINST Moray), ORK takes
   Caithness+Sutherland, LOI becomes the KINGDOM of the Isles
   (mann/skye/arran; MNN landless as the 1333 English irredenta).
   ENGLAND: jersey → NRM, abbeville → BGN (the last Ponthieu relic).
   **DEFERRED: the LAN/CET fold into ENG** — the one conquest-balance
   item, parked for a post-launch pass. FOUND ON THE WAY: the new
   "IO members hold land" harness check (753 items) caught SIX ghost
   members the earlier slices left in IOs (ARM ATZ CIL EPI TRE FEO —
   now generically stripped, exact-count 6); _tpl_grants went
   recursive (welsh_releasable carries its discovery in a NESTED
   include — a one-level reader called the shells blind); the
   horde/tribe recipient assert narrowed to steppe_horde on
   measurement (country_name_construction has ZERO tribe branches);
   vanilla's high_kingship member list carries comment tokens
   (#PLE) a raw split miscounts. 25 checks green, tributary gate 23
   (tribe branch proven by breaking), all count transitions observed
   failing before their constants moved.
   TEST WHEN THE USER RETURNS: (a) **Ireland tints under Leinster
   and Diarmait renders "High King"** — the IO probe's pass/fail
   signal (show_as_overlord_on_map fires only with a leader);
   (b) Wales in five native kingdoms, Bleddyn in Gwynedd ("Bleddyn"
   literal + brythonic fallback probe), no marcher lords; (c) Dublin
   under Murchad ("Murchadh mac Diarmata" — the patronymic
   showcase), six Irish tributaries LIVE WITHOUT any reform (the
   tribe-branch probe — if downgraded to vassal, the branch is not
   evaluated at setup and the fallback is a LEI reform); (d) Scotland
   whole — Edinburgh SCOTTISH, no Balliol pretender, Moray under
   Mael Snechtai, Galloway/Isles independent, ORK holds Caithness;
   (e) ENG regression: the conquest opening plays, jersey Norman,
   137→134-ish holdings; (f) error.log: landless trims grow by ~25
   tags (known class), the six IO ghosts should log nothing new,
   watch for tributary 3702 lines naming the Irish six.
   **CONFIRMED IN GAME (2026-07-29 evening, one launch covering
   items 20+21+the Nizamiyya): EVERYTHING PASSED.** The High
   Kingship IS crowned — Ireland tinted under Leinster, Diarmait
   renders "High King" in the IO panel; **the Irish tributaries
   passed the gate REFORM-FREE: zero 3702 lines name any mod tag —
   the tribe branch IS evaluated at setup** (new law, KNOWLEDGE);
   all twelve mod tributaries live and war-capable; Murchad rules
   Dublin (screenshot); Wales in its five kingdoms (screenshot);
   Scotland whole, Moray/Galloway/Isles as designed (their random
   rulers are the recorded [D] honesty); France tiny with its six
   homage tributaries; **Adalbert back on La Marche** (the fiefdom
   override confirmed and cured); Dreux gone; SEL capacity 8.00 and
   the slot refund visible on all three reforms; wars at day 0 and
   the conquest beats sequential. Blind capitals: ZERO (the Welsh
   discovery restatement worked). The NRM "William II" the user
   flagged is CORRECT BY DESIGN — duke numbering (he is the second
   Duke William of Normandy; the recalibrated ENG table crowns him
   King William I of England at Christmas). Log residue all decoded
   same session (four new decoder entries): stranded owner-buildings
   ×6, releasable-culture shells ×8 (incl. vanilla's own ATH),
   estate/pop culture mismatches + DUB's Pale forts (the POP PHASE's
   bill, user-diagnosed on sight), blocked 1337 cabinet names ×3,
   and the tusi flood corrected to its true ~128 (one root, China
   review). Open eyeball, not retested: Toulouse's ruler render
   ("Guilhèm" — the occitan fallback probe) — one click next launch.

22. **SOUTHERN ITALY 1066 (LANDED, untested).** 88 locations, 7 new
   tags, 2377 blocks, 7 new thrones. **Robert Guiscard's Apulia-
   Calabria (APU, 47)** with the 10 Abruzzo locations as a knowing
   anachronism (Lyonnais precedent, banked for the HRE slice);
   **SIC REUSED as Roger's County of Sicily** (4, Messina-Val
   Demone) — FORCED: vanilla locks 6 advances behind
   has_or_had_tag = SIC and all are Norman-Sicilian (the
   Constitutions of Melfi under an emir was the veto); surgery:
   capital→messina, rank→county ("Count Roger"), court
   catalan→sicilian, regnal roger 3→0. Capua (CUP, Richard
   Drengot), Salerno (SLR, Gisulf II — Guiscard takes it 1077),
   Naples (NEA, Sergius V), Gaeta (GAE, Atenulf I). **Emirate of
   Palermo (PLM, 9 + Malta)** under **Ayyub ibn Tamim — son of OUR
   seated Tamim of TUN, riding our own zirid_dynasty**; Emirate of
   Agrigento (AGR, 10, random — Ibn al-Hawwas's death is 1064 OR
   1068 [D]). Both emirates take sicilian as PRIMARY (no
   siculo-arabic culture exists; 100% of their pops are sicilian —
   the capacity-wall avoidance; Arab elite = the ruler's culture).
   **The Byzantine catepanate returns: BYZ +7** (Bari — falls
   16 Apr 1071, the situation hook — Otranto, Taranto). **The Melfi
   investiture: PAP → APU and PAP → CUP as TRIBUTARIES** under
   papal_investiture_reform (khutba pattern #4 — the FIRST theocracy
   overlord, the slice's one genuinely new shape; fallback if 3702
   names them: honest vassalage). NAP landless — its snapshot
   auto-yielded the 87-location Two Sicilies irredenta (65 mainland
   + its existing 22 Sicilian claims); SAO (Salona — which had been
   ruling ONLY Malta since the Byzantium slice!) landless with
   vanilla's exact four claims back, verified in the output.
   ARA→SIC guarantee stripped (1282 Vespers), PAP→SIC kept (Melfi
   in miniature). Amalfi has NO map location (like Capua-city and
   Aversa) — gap recorded, no tag possible. Invented name keys
   #8-9: name_gisulf, name_ayyub. All counts proven by breaking
   (BYZ 506, ARA-strip); 26 checks green, gate at 25.
   TEST NEXT LAUNCH: (a) the Mezzogiorno in seven colors — Guiscard
   crimson over Apulia-Calabria, "Count Roger" in Messina (the
   rank-fallback probe), the two emirate greens vs SIC's dark olive
   (Gallura-class eyeball); (b) PAP's two tributaries LIVE (the
   theocracy-overlord probe — 3702 naming APU/CUP = the fallback
   trigger); (c) "Gisulfo" and "Ayyūb" render (invented keys #8-9);
   Ayyub's dynasty shows "Banū Zīrī" and his father is Tamim of
   Tunis (cross-tag family link); (d) Bari/Taranto BYZANTINE again;
   Naples/Salerno/Gaeta independent city-states; (e) Malta under
   Palermo; SAO gone from the map; (f) error.log: expect the
   landless trims +2 (NAP/SAO — the MAM class), the pop-culture
   class grows by the 19 Christian-pop emirate locations (known,
   pop phase), white flags on 7 more tags (CoA debt); (g)
   regression: PAP still renders "Alexander II"/"Rome", VEN
   Contarini, the taifas, the Norman opening.
   **CONFIRMED IN GAME (2026-07-29, same evening): ALL PASSED — THE
   SLICE IS CLOSED.** The map, the whole click tour, "Count Roger",
   "Gisulfo"/"Ayyūb" (invented keys #8-9 proven), Ayyub's Banū Zīrī
   dynasty with the cross-tag father link to Tamim of Tunis, the
   Byzantine heel, Malta under Palermo — and **BOTH Melfi
   tributaries LIVE: a THEOCRACY overlord's setup reform passes the
   tributary gate** (the khutba pattern is now proven under
   monarchy overlords, tribe subjects and a theocracy overlord
   alike). Zero 3702 lines naming APU/CUP; only the known
   estate-culture class in the log. The user spotted PAP's third
   subject: **PAP→FAE (Faenza) vassal — vanilla's own**
   (12_diplomacy:162, untouched by every strip). 1066 Romagna's
   papal-vs-imperial status is the HRE/central-Italy pass's
   judgment call — parked there, recorded here.

23. **THE HRE/HAB SLICE (LANDED, untested) — the crown is DECISION D
   (user, 2026-07-29 night):** Heinrich IV on a LANDED OGK with the
   Standard 9-location Salian demesne (Goslar capital — his
   birthplace; Speyer, Worms, Aachen, Frankfurt, Nuremberg,
   Dortmund, Nordhausen, Mühlhausen — nine one-location free cities
   emptied), `leader = OGK` + `emperor = { OGK }`, and the
   HRE_LEADER loc overridden to **"King of the Romans"** — the 1084
   imperial coronation is a banked event hook. THE MEASURED LAW that
   killed the leaderless option: hre_election goes LIVE the moment
   the IO is headless and the hre.txt failsafe crowns the richest
   member after two years — a headless HRE elects a Habsburg.
   Electors: the 1356-Bull SWB/PAL out, LUN/UBV in (with BOH/BRA)
   [U]; archbishops + no_golden_bull already 1066-exact. HAB REUSED
   as the **Babenberg Margraviate of Austria** (16, Ernst the Brave,
   babenberg_dynasty, the margraviate-reform rank branch renders
   "Margrave" — a vanilla free win); **STY rises as the Carinthian
   March under Otakar of Steyr** (22 — invented literal #19: the
   only vanilla "Otakar" is a west-slavic row, name_odoacer would
   render "Odoacer"); **CRH ducal under Berthold of Zähringen** (13;
   titular [D] — the Eppensteiner tension is Germany II material);
   GOR/ORT/GRK dissolve (+pazin, GOR's SEVENTH location, missed by
   the package and caught by the landless guarantee — to AQU);
   PSS/AUG/RVA/ALS/KYB/NEL/VUD grow; ZAH is the one new tag (the
   Zähringen Breisgau). ALL THREE BANKED DEBTS CLOSED: **SPL revives
   with 15** (its five Umbrian claims from PAP + the ten Abruzzo
   from APU — the Italy anachronism resolved the day it was banked;
   random, Godfrey parks with Germany II), **the Lyonnais 7 resolve**
   (lyon/riverie/beaujeu/perreux→FRZ, trevoux→SAV,
   viviers/chalancon→VLN), **PAP→FAE stripped** (1066 Faenza is the
   imperial archbishop of Ravenna's world). HAB's three 1337
   embargoes stripped. The generic landless-IO sweep WIDENED to all
   membership/status lists (members alone missed free_city — 28
   entries stripped, exact-multiset asserted). 2378 blocks, 116
   rulers, all counts observed-then-moved, 26 checks green. PARKED:
   **Germany II** (Swabia/Saxony/Franconia/Rhineland — 249 tags, 148
   of them 1-2 locations; Rudolf of Rheinfelden, Ordulf Billung,
   Anno of Cologne with the name_anno/name_ordulf invented-key
   decisions, Lower Lorraine/Godfrey) and **Italy North**
   (Tuscany/Canossa/Matilda, the Verona march — Berthold's other
   title, Aquileia/Friuli, the communes). Also parked: the 11_art
   future-date audit (101 of 137 entries — one error.log grep next
   launch decides if those files need overriding).
   TEST NEXT LAUNCH (click tour): (a) map overview — Austria SHRUNK
   to the Danube strip, Styria/Carinthia separate colors beside it,
   nine imperial cities in OGK's grey-green scattered across
   Germany, Lyon no longer French-blue, the Abruzzo out of Norman
   crimson into Spoleto's; (b) click Goslar → country "Holy Roman
   Empire", ruler Heinrich (15, regency) — his TITLE via the IO
   should read **"King of the Romans"** (the loc-override probe);
   open the HRE IO panel → leader Heinrich, electors BOH BRA LUN
   UBV; (c) click Vienna → **"Margraviate of Austria" / "Margrave
   Ernst"** (house Babenberg — the rank-branch probe); Graz →
   Styria under **"Otakar"** (invented literal #19 render probe);
   Klagenfurt → Carinthia under Berthold (house Zähringen);
   (d) Spoleto → duchy with a random ruler holding the Abruzzo;
   Faenza independent; Rome's subject list still exactly APU+CUP;
   (e) villingen area → the small red Zähringen county;
   (f) error.log: no 3702 naming OGK/HAB/CRH/STY, landless trims
   grow by ~12 (known), watch the free-city auto-rescind lines;
   (g) regression: the whole prior map (İtalya güneyi, Fransa,
   Britanya) unchanged.
   **CONFIRMED IN GAME (2026-07-29 night, screenshots): ALL PASSED —
   THE SLICE IS CLOSED.** "Holy Roman Empire" under tag OGK with the
   15-year-old Heinrich, title correct ("King of the Romans"),
   electors correct; the Babenberg Margraviate, Styria (STY) and
   Carinthia (CRH) exactly as designed; Spoleto/Lyonnais/Faenza all
   verified; zero 3702 lines naming the slice. One new signature,
   decoded same session: 180× jomini-252 from hre.txt:328 —
   `can_lead_tooltip_trigger` evaluated by the UI on a null election
   candidate while the IO panel was open; cosmetic, decoder entry
   added, WATCH status. The user's map screenshot is the whole 1066
   Europe in one frame — every slice visible.

## DEFERRED BY DESIGN — the backlog a fresh session must know
Every item below was DECIDED, not forgotten. Sources: the taifa,
Christian-Iberia and Byzantium packages (2026-07-28), all re-verified.
- **Southern Italy 1066 slice** (spec banked): 87 locations (NAP 65 +
  SIC 22), ~5 new tags (Guiscard's Apulia-Calabria, Capua, Salerno,
  Naples, Kalbid Sicily rump), Byzantine catepanate carve-out (Bari
  falls only 1071.4), Roger's Messina, malta stays Muslim until 1091.
  Free ids verified: APU GAE RAS DUK KAK PEC ZET DIO TMU (word-grep
  zero); **CAP is NOT free** (interfaces loc, all languages).
- **Pechenegs: NO tag at start** — 1046-53 settlement made them
  foederati INSIDE the Paristrion theme; the autonomous lords (Tatrys,
  Sesthlav, Satzas) are 1072+. PEC is banked for a future Danube/steppe
  situation around the 1087 invasion — a state EARNED by events, per
  the project's philosophy. North of the Danube (WAL/Moldavia/steppe)
  untouched = the steppe slice.
- **Kakheti-Hereti micro-slice**: independent under Aghsartan I
  1058-1084, needs invented tag (KAK/HER free) + name_aghsartan
  (missing). Tashir-Dzoraget (AAI) arguably right as-is.
- **Kharpert/Dersim Tier 2** (8 locations, SUT/CEM/EGL): softest edge
  of the eastern frontier, NO source anchor found — deliberately left.
- **RESOLVED by the Seljuk slice (2026-07-29):** Marwanid Diyar Bakr
  and Mirdasid Aleppo are landed tags (MRD, HLB); Kharpert's four
  locations went to BYZ. Still open from that seam: the Dersim
  remainder (CEM/BIN/EGL, 6 locations, no anchor), Hakkari/Amadiya.
- **Central Asia slice** (named by the Seljuk package): Kara-Khanids
  (Western at Samarkand under Ibrahim Tamghach Khan, Eastern at
  Balasagun), transoxiana_area + zhetysu_area (~175 land, CHG/YSU/
  BRL/JLY), Kipchak steppe, Oghuz remnant, Volga Bulgars — one
  coherent slice, nothing in the Seljuk slice depends on it. The Oxus
  is SEL's fixed eastern border.
- **Arabia slice**: FDL's 6 Najd locations, ORM's Oman 22, HLG's
  kazimah (1 — taking it would make HLG landless), the Hejaz.
- **Rawwadid Tabriz Tier-2**: azerbaijan_area went to SEL whole; the
  Rawwadids of Tabriz were Seljuk vassals until 1071 — a possible
  14th client if ever wanted (34 locations affected).
- **Gilan/Talish/Shaki left as 1337 micro-states on purpose**: the
  Caspian littoral autonomies are not obviously wrong at 1066.
- **ABS probe watch item**: if "Abbasid Empire" renders, the explicit
  `type = theocracy` lost to the include template — KNOWLEDGE either
  way; the fallback loc-only fix is
  country_name_construction override (route 3 in the package).
- **CAS/LON border alternative**: the Pisuerga reading moves palencia,
  carrion_de_los_condes, saldana, monzon_campos CAS→LON. Area-line
  chosen (vanilla's own claims signal); 4-location revisit.
- **vielha**: left ARA; the Comminges reading (→COM) is the alternative.
- **ARA culture_definition = catalan** (registry, iberia.txt:17): fix
  needs whole-file override; VERIFY IN GAME first that the field even
  matters for a landed tag.
- **Armenian patriarchate seat = sis** (now BYZ-owned): left unchanged
  on purpose — every alternative is equally Byzantine-owned.
- **Name-key bank (all confirmed MISSING in vanilla):** name_mihailo,
  name_stefan, name_bodin, name_petrislav, name_gojislav,
  name_konstantin, name_gagik, name_ashot, name_smbat, name_kiurike,
  name_aghsartan, name_giorgi, name_mujahid, name_hudhayl, name_hisham,
  name_mundhir, name_zuhayr. Present: name_michael, name_voislav,
  name_radoslav, name_bagrat, name_george, name_david, name_nuno.
- **BYZ's claims comments**: emptying BYZ's 63-claim block left
  Paradox's loss-year comments orphaned in place — cosmetic; a tidy
  pass may remove them someday.
- **Eyeball items**: Bernat of Besalú renders via name_bernard's
  occitan row ("# Catalan & Occitan"); ARA/NAV are both dark red and
  NEWLY adjacent in the west Pyrenees (Gallura-class recolor if it
  reads badly); SEL's map name lacks its article ("Sultanate of Great
  Seljuks") — SEL_THE exists and CW225 on it is a false positive, but
  whether the engine consults _THE keys is unproven.
- **COAT-OF-ARMS BATCH for all new tags — RECLASSIFIED as a cosmetic
  upgrade (2026-07-29 night, measured):** the engine AUTO-GENERATES
  plausible flags for entry-less tags — the user's screenshots show
  PLM with a green crescent-and-star flag (the generator reads at
  least religion) and VMD with a red-and-white emblem. The earlier
  "ABS rendered WHITE" note does not generalize. ~733 of vanilla's
  own 2217 tags also lack entries (1484 in pre_scripted_countries).
  The batch therefore targets only tags whose generated flag is
  historically WRONG enough to matter: ABS (the black Abbasid
  banner), FAT (white/green), SEL, Hauteville APU/SIC, and
  case-by-case. The system is compositional script (pattern +
  color1/color2 + emblems) — cheap to author. Research package
  pending.
- **CHA/DAI (China) tributaries broke with our Middle Kingdom strip**
  (government.cpp:3702 class) — CHI lost its modifier source; the ~30
  Guizhou `tusi` subjects fail the same way (country_triggers.txt:
  1288-1298 leans on the IO). Owned by the future China review; do not
  re-discover. **Third symptom, same root (2026-07-29):** CHI's
  accepted-culture flood (country.cpp:9635) — the IO's leader_modifier
  also carried `cultures_capacity = 50` (middle_kingdom.txt:71). One
  restore point (an ABS-style setup reform for 1066 China) fixes all
  three.
- **Muslim empire-rank styling** (user question, 2026-07-29): SEL's
  kingdom rank is the HISTORICAL styling (Sultanate; and ABS holds
  empire rank — the de jure hierarchy of the Islamic world is in the
  setup). If SEL ever ranks UP, the name becomes "Seljuk Empire"
  (legitimate historiography) but the ruler becomes "Emperor" (wrong —
  sultans never took it). The "Holy" loc trick does NOT transfer: the
  generic empire strings belong to every empire (BYZ's "Emperor" must
  live). The real fix is a whole-file override of country_ranks.txt
  inserting a muslim-MONARCHY-empire branch ("Sultanate"/"Sultan")
  before the generic — MAM's tag-gated empire branch proves the slot
  exists; first-match-wins rules out injection. Do it deliberately,
  diff in hand, bundled with a future empire-styling pass (Fatimids).
- **HLG/QUN/SLD army-based shatter lines** (initialize_from_bookmark
  .cpp:2477) — Mongol-era army tags our sweeps starved; Arabia and
  Central Asia slices retire them properly.
- **Pop/religion/culture conversion phase**: after the world's borders
  are done (user decision below). The taifa measurement stands: 222 of
  244 al-Andalus locations have catholic template religion.

## STRATEGIC ORDER (user decision, 2026-07-28 evening)
**Territory first, across the WHOLE map — pops/religions/cultures as a
separate later phase.** The world's borders get finished before any pop
conversion work starts.
**DONE so far:** Sardinia, the 13 taifas, Christian Iberia, Byzantium,
Seljuks+Abbasids (CLOSED — confirmed in game 2026-07-29 across THREE
launches: Caliphate probe passed, tributary reform beat the validator,
and the item 18 polish batch passed its five-minute check), Fatimid
Egypt + southern Levant (CLOSED — confirmed in game 2026-07-29 the
same day it landed, all seven test points; item 19).
**Remaining, in rough order:** ~~France demesne + Languedoc~~ (item
20), ~~British Isles~~ (item 21 — both LANDED 2026-07-29, tests
accumulate)
(Wales marcher dissolution, Ireland/PLE breakup), HRE/HAB breakup,
southern Italy 1066 (spec banked), Central Asia (Kara-Khanids),
Arabia, the Rus/steppe east, India/China/rest-of-world review — then
the pop phase (al-Andalus owes 222 locations; Persia owes none).

## Next, in order

1. **Test France in game:** (a) Philip I on the French throne, aged 14,
   under a regency; (b) spot-check Brittany (Conan — displays "Conon"),
   Flanders (Baldwin V), Aquitaine (William VIII), Burgundy (Robert I),
   Foix (Roger II, exactly 16); (c) the five new dynasty names render
   (de Rennes, of Flanders…); (d) error.log for any new class; (e) the
   Norman Conquest opening still plays (regression).
2. **EMPIRE CLEAN BATCH LANDED (untested in game):** 33 rulers total.
   New: BOH Vratislav II, UBV Otto of Nordheim (regnal II flagged as
   common-but-unverified), HOL Dirk V (14 — MINOR_RULERS), MAI
   Siegfried I (dynasty-less, vanilla-attested), BRB Henry II (accession
   sources differ, earlier date entered), plus the northeim dynasty.
   Test: Bohemia/Bavaria/Holland/Mainz/Louvain thrones, Dirk aged 14
   ruling directly, error.log.
   Still held back, decisions recorded: the CROWN (Heinrich IV 15 +
   landless OGK + HRE IO leadership options), Swabia/Saxony (no usable
   tags), KOL/TRI (name keys missing — would be our first own name-key
   loc entries), CRH/MEI/LUX/HAI/UTR/LIE (unverified dates).
2. **Polish pass** once round 4 is clean: map_color/legend/tooltip layer,
   a proper illustration, richer loc (Opus subagent), a hint entry,
   regnal_numbers recalibrated for 1066 (William shows as "III"), Edgar
   Ætheling for England's interregnum, Sweyn's 1069 invasion and
   Malcolm's role as follow-ups.
3. Then the next region: **France and the Empire** — `docs/PHASE-2-PLAN.md`
   has the order and the 1066–1337 backlog.

## Repo state (2026-07-29, end of the Seljuk test-and-fix day; 3-day break follows)

Everything is COMMITTED through the item 18 polish batch. The working
tree should be clean; if it is not, `git log --oneline -8` first — the
day's last commits tell the story (doc-debt closure → Seljuk-test fix
batch → tributary-gate harness guard → polish batch → reform-loc
sweep). The 34 wiki PDFs in `docs/` remain untracked (~26 MB) — still
undecided, still harmless.

`python tools/verify_mod.py` → 24 checks green (last run this session;
the two newest — the tributary gate and the reform-loc sweep — were
proven by breaking).
`python tools/build_setup.py --dry-run` → clean, ~12s (the ownership
index refactor; if it takes minutes, something regressed). The build
now also asserts capital discovery for every generated block, resolved
through definitions.txt.

**MONGOL RESURGENCE: CLOSED OUT THE SAME NIGHT.** The deep audit
(committed in MR as `docs/AUDIT-2026-07-29.md`) found six DEFINITE
bugs; ALL SIX were then fixed with the user, harness 16/16 green —
including D6, which the user's design review REVISED: a human Khaghan
collapses like anyone else (years of visible counterplay exist);
only bystander human vassals are protected. MR's remaining to-do is
its own: the first in-game session of the Great Partition block
(audit S3), plus S1/S2/S4 checks. Nothing in MR blocks this project.

**THE SITUATION QUALITY BAR (user decision, 2026-07-29 evening,
refined same evening):** every situation needs (1) a real PURPOSE,
(2) historical grounding, (3) flavor density — events, buffs/nerfs,
texture; "uğraşılmış hissettirsin." MR-scale multi-phase machines
are the CEILING, not the floor — scale fits the subject (Manzikert
big; the Mecca khutba switch small but flavorful). The shipped
Norman Conquest is below the bar — it was the machinery probe, and
it owes a v2 flavor pass (seeds already in its polish backlog:
Edgar Ætheling, Sweyn 1069, Malcolm, the Harrying). Size situations
1-4 days each by subject; the phase in weeks.

**WATCH (2026-07-29 night screenshot):** VMD sits at 47.17% subject
loyalty — a DISLOYAL tributary in the Capetian homage ring. One
disloyal fief is period-accurate flavor; if a longer observer run
shows the whole ring cancelling early, the ring gets an opinion
cushion. Fold into the next long observer session's checklist.

**ITEM 24 — THE COAT-OF-ARMS BATCH (landed 2026-07-29 night, NEEDS
GAME TEST).** `zz_1066_flags.txt`, 9 arms; system decoded in
`docs/COA.md`; harness check proven by breaking three ways. The user's
"before" screenshots are the baseline: ABS flew generator-WHITE, FAT
generator-BLACK (history inverted), SEL a generic red-crescent flag.
Test — click tour, ~5 minutes, all in the country panel's flag:
1. **Seljuks** (the big power over Persia): flag should now be BLUE
   with a white DOUBLE-HEADED EAGLE. If it is still red with
   crescents, the file did not load — say so, we strip the BOM.
2. **Abbasid Caliphate** (Baghdad, one location): SOLID BLACK with a
   small white square inscription.
3. **Fatimid Caliphate** (Egypt): WHITE with a small green
   inscription. Black-vs-white side by side is the whole point —
   eyeball both on the map at once.
4. **Apulia** (southern Italy, Guiscard): blue with a diagonal
   red-and-white CHECKERED BAND.
5. **Sicily** (the island kingdom-to-be, Roger's SIC): the SAME
   checkered band — it used to be a black German eagle; if you still
   see an eagle, the override failed.
6. **Dublin** (Ireland's east coast): red with a black RAVEN.
7. **Vermandois** (the small fief northeast of Paris): a gold-and-blue
   CHECKERBOARD.
8. **Zähringen** (southwest Germany, Breisgau): gold with a red eagle.
9. **Pereiaslavl** (Rus, on the Dnieper south of Kyiv): blue with a
   gold trident-like TAMGA.
Everything else (taifas, Catalan counties, Seljuk clients, PLM/AGR,
ULD, south-Italian minors) KEEPS its generated flag by design — the
deferred tiers are in `docs/COA.md` §4.

**NEXT SESSION STARTS WITH:** item 23's game test (the HRE — click
tour in the item; headline probes: "King of the Romans", the
Margraviate branch, literal #19, shrunken Austria) — **DONE, item 23
is CONFIRMED AND CLOSED the same night.** Items 16-23 are
ALL CONFIRMED IN GAME (2026-07-29 — six slices tested and closed in
ONE day). Remaining territory per the strategic order: **Germany II**
(parked with its cast questions), **Italy North**, Central Asia,
Arabia, the Rus/steppe east, the India/China review (the Middle
Kingdom restoration is its anchor item). Meanwhile banked: the
SITUATION-SPECS package (a research agent's report pending review
into docs/SITUATION-SPECS.md), the situation scaffold generator
(tools/new_situation.py, tested), the CoA batch (LANDED as item 24 —
not white flags after all, see docs/COA.md), the 11_art audit grep. Items 16-19 are ALL CONFIRMED IN GAME
(2026-07-29). Threads item 19 left for later: the MEC khutba switch of
1071 and the Mustansirite Hardship are situation material; the
coat-of-arms batch PAID FAT its white banner (item 24); the
Hejaz interior (Mecca/Medina proper) belongs to the Arabia slice.
Standing rhythm with the user: propose batch → "onay" → land → they
test in game → findings become fixes and decoder entries. Conversation
in Turkish, everything in the repo in English.
