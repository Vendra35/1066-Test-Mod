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

## BATCH TEST — one game session covers everything below

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

## Repo state

Uncommitted at handoff. The 34 wiki PDFs in `docs/` are untracked and about
26 MB — decide whether they belong in git or in `.gitignore`.

`python tools/verify_mod.py` → all checks passed.
`python tools/build_setup.py --dry-run` → clean.
