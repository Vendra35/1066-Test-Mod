# NEW_COUNTRIES — design for inventing a country that vanilla does not ship

> Written 2026-07-28 while the ruler layer stood at 50. Four parked slices
> all block on this one mechanism: the Great Seljuks + Abbasids (one job),
> the 14 Iberian taifas, Pereyaslavl, and Fatimid Egypt. Everything below
> is synthesized from the region research passes and carries their
> citations; nothing here is implemented yet.

## What a new tag needs — the verified checklist

Sources: the Iberia pass (its F8 prerequisite audit), the Levant pass, the
Empire pass (F6, formables-without-identity), all in KNOWLEDGE.md.

1. **A country block in `10_countries.txt`** — the minimal working template
   is ANR at vanilla `:14294`: ~17 lines — `own_control_core`,
   `starting_technology_level`, `include` lines, `government`, `capital`,
   `country_rank`. For Muslim tags, GRA (`:14801`) is the richer template:
   `court_language`, `religious_school`, `sharia_law`, the muslim
   `include`s, `tolerated_cultures` (drop its Nasrid-specific reform and
   regnal_numbers).
2. **Territory taken FROM existing owners.** A new tag's locations must be
   REMOVED from whoever holds them at 1337 — ownership must stay
   exclusive. This is the mechanism's real work and its real risk.
3. **An identity block in `in_game/setup/countries/` — PROBABLY OPTIONAL
   for landed tags.** Load-bearing observation from the Levant pass:
   **SIC has NO identity block anywhere and lives as a landed 1337
   kingdom.** Identity blocks (`culture_definition`, `religion_definition`)
   exist so LANDLESS tags can be instantiated later (the SKE law). A new
   tag born WITH land plausibly needs none — cheap to try first, add if
   the game disagrees. If needed: additive file, KOJ (`crescent.txt:45`)
   as the shape.
4. **A named color** — additive `main_menu/common/named_colors/` file
   (ours exists). `map_egypt` already ships for EGY (`02_map.txt:885`).
5. **Loc: `TAG` and `TAG_ADJ` keys** — our loc file. For Muslim
   duchy-rank tags with Iberian capitals, "Taifa of X" renders free
   (`rank_duchy_andalusi`, country_ranks.txt:1689).
6. **Coat of arms — optional**, engine falls back to default; polish item.
7. **A dynasty + characters** — mechanisms already proven (additive
   dynasty file, NEW_CHARACTERS). Fatimid and Abbasid houses are already
   banked in `04_zz_1066_dynasties.txt`.

## Mechanism shape in build_setup.py

Two new tables, executed in build_countries BEFORE the ruler pass so new
tags are seatable through the same HISTORICAL_RULERS row:

```python
# tag -> the full country block text (template-derived, hand-written per
# slice, verified identifiers only)
NEW_COUNTRIES = { "SEV": "...", ... }

# tag -> locations it takes; the generator REMOVES each from whatever
# own_control_* list currently carries it, and asserts every location was
# found exactly once and ends owned exactly once.
LOCATION_TRANSFERS = { "SEV": ["sevilla", ...], ... }
```

Order of operations: transfers → new blocks appended → rulers → validate.

New assertions (each to be proven by breaking, as always):
- country count == 2337 + len(NEW_COUNTRIES);
- every transferred location exists in `definitions.txt`;
- no location appears in two owners' lists after the pass;
- every NEW tag got exactly one government/ruler and, if listed in
  HISTORICAL_RULERS, its historical ruler landed in it;
- every NEW tag has a named color and TAG/TAG_ADJ loc keys (harness side).

Displaced 1337 tags are EMPTIED, never deleted — the SKE landless road —
because events and formables reference them by name
(rise_of_the_ottomans.txt names TUR; deleting blocks breaks references
silently). Their `our_cores_conquered_by_others` claims stay, which is
historically elegant: the beylik claims ARE the future.

## Rollout — smallest probe first

1. **Probe slice: PEREYASLAVL.** One tag, ~5-8 locations out of KIE, and
   the ruler needs NO authoring — `kie_vsevolod_rurikovich` ships in
   vanilla (b. 1030, the third triumvir). Smallest possible end-to-end
   test of the whole mechanism. Must NOT reuse the tag id `PER`
   (Périgord!) — a fresh id like `PYS` after checking it is unused in
   vanilla AND unreserved by loc/formables.
2. **The taifas** (template-driven mass production, GRA shape ×13).
3. **Seljuks + Abbasids** (+ JAL dissolved to landless, government type
   correction so no horde naming).
4. **Fatimid Egypt** (+ the MAM rank-branch decision, KNOWLEDGE).

## Open questions the probe must answer

- Does a landed tag truly need no identity block (the SIC precedent)?
- Does the engine accept a tag id absent from every vanilla database, or
  is there a tag registry beyond `10_countries.txt`? (The Iberia pass
  found none; `setup/countries` identity blocks and loc are the only
  sightings. The probe measures it.)
- Do `include = "..."` template references resolve for new tags the same
  way (expected yes — they are setup-side templates).
