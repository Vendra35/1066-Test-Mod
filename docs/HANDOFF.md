# Handoff — where the 1066 mod stands

> Written at the end of the first working session. Read `CLAUDE.md` first, then
> this, then `docs/KNOWLEDGE.md`. Everything below is either measured or marked
> as unverified.

## The one thing that is untested

**Nothing in this session's last commit has been observed in a running game.**
Phase 1 was tested and works. The Phase 2 slice — five historical rulers and
three new Norwegian characters — is generated, validated by the build script, and
passes the harness, but has never been launched.

**Do this first, before writing anything new:**

1. Launch and check the five rulers are the right people with visible names:
   `ENG` Harold Godwinson, `NRM` William, `DAN` Sweyn Estridsson,
   `SCO` Malcolm III, `NOR` Harald Hardrada.
   Hardrada's name is the specific thing to look at — he uses `name_harold`
   because **`name_harald` does not exist in the game**. If he is nameless, that
   is why.
2. Advance past **1066.9.25**. Hardrada dies at Stamford Bridge — that death
   comes from our own `death_date`. Does Norway pass to Magnus II, or to a
   generated heir? This answers whether `father =` links are enough for
   succession, which decides how much the Norman Conquest situation has to do.
3. Advance past **1066.10.14**. Harold dies at Hastings — that one is vanilla's
   `death_date`, not ours. What happens to England?
4. Check `error.log`. It was at **48 lines** at last test. If it grew, the new
   characters are the suspect.

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
IOs, plus 174 `heir`/`consort`/`regency` lines. Then 861 named rulers become
`random`, 1360 already were, and 116 countries that had none get one — totalling
**2337, exactly the country count**.

`HISTORICAL_RULERS` at the top of the script is the Phase 2 hook: `tag ->
character key`. Five entries so far.

The script refuses to write unless: country count unchanged, exactly one ruler
per country, each historical ruler landed **in its own country**, no non-random
ruler is unaccounted for, no date survives in the country or IO files, braces
balance, and every historical ruler exists and is at least 16 at `START_DATE`.

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

## Next, in order

1. **Test the five rulers** (above). Nothing else should be written first.
2. **`situations/norman_conquest.txt`** — shape it around what step 2 and 3 of
   the test actually produce. Field list is authoritative in
   `in_game/common/situations/readme.txt`. Remember CLAUDE.md's rule: the AI can
   be railroaded, the player is asked.
3. **Harness check for situations** when the first one lands, and raise the four
   remaining `PENDING` counts as their content types appear — grep `PENDING` in
   `tools/verify_mod.py`.
4. Then the next region. `docs/PHASE-2-PLAN.md` has the order and the
   1066–1337 event backlog with priorities.

## Repo state

Uncommitted at handoff. The 34 wiki PDFs in `docs/` are untracked and about
26 MB — decide whether they belong in git or in `.gitignore`.

`python tools/verify_mod.py` → all checks passed.
`python tools/build_setup.py --dry-run` → clean.
