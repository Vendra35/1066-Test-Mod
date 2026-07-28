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
checked — low risk, verify in passing next launch.) New observation for
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
still-unverified -1000 opinion wall between the 1066 claimants.

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
  reads badly).
- **Pop/religion/culture conversion phase**: after the world's borders
  are done (user decision below). The taifa measurement stands: 222 of
  244 al-Andalus locations have catholic template religion.

## STRATEGIC ORDER (user decision, 2026-07-28 evening)
**Territory first, across the WHOLE map — pops/religions/cultures as a
separate later phase.** The world's borders get finished before any pop
conversion work starts.
**DONE so far:** Sardinia, the 13 taifas, Christian Iberia, Byzantium,
Seljuks+Abbasids (last one UNTESTED — tomorrow's first job).
**Remaining, in rough order:** Fatimid Egypt + the Levant south of the
named line (Damascus/Palestine; MAM keeps 120 there), France demesne
163→~25 + Languedoc (montpellier already parked there), British Isles
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

## Repo state (2026-07-29, end of the marathon session)

Everything is COMMITTED through the Seljuk+Abbasid slice. The working
tree should be clean; if it is not, `git log --oneline -8` first — the
last commits tell the story (Sardinia → taifas → Christian Iberia →
Byzantium → landless-dependency fix → Seljuks). The 34 wiki PDFs in
`docs/` remain untracked (~26 MB) — still undecided, still harmless.

`python tools/verify_mod.py` → 23 checks green (last run this session).
`python tools/build_setup.py --dry-run` → clean, ~12s (the ownership
index refactor; if it takes minutes, something regressed).

**MONGOL RESURGENCE: CLOSED OUT THE SAME NIGHT.** The deep audit
(committed in MR as `docs/AUDIT-2026-07-29.md`) found six DEFINITE
bugs; ALL SIX were then fixed with the user, harness 16/16 green —
including D6, which the user's design review REVISED: a human Khaghan
collapses like anyone else (years of visible counterplay exist);
only bystander human vassals are protected. MR's remaining to-do is
its own: the first in-game session of the Great Partition block
(audit S3), plus S1/S2/S4 checks. Nothing in MR blocks this project.

**TOMORROW STARTS WITH:** the Seljuk batch in-game test — the full list
is item 16 above, headline question the ABS Caliphate probe. Then the
next slice per the strategic order (Fatimid Egypt is the natural one:
the Levant line is already drawn and named in item 16's package).
Standing rhythm with the user: propose batch → "onay" → land → they
test in game → findings become fixes and decoder entries. Conversation
in Turkish, everything in the repo in English.
