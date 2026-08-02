> **STATUS (2026-08-02, end of the map phase): SUPERSEDED as the design —
> `docs/POP-PHASE-PACKAGE.md` is now the pop phase's decision-ready
> package** (DRAFT, unreviewed — the next session's first job). This file
> remains the banked-traps record it consumed. CRITICAL refinement the
> package established: several §H corrections in the theater packages
> were measured on the SEED layer (`location_templates.txt`) rather than
> the STATE (`06_pops.txt` pops) — five of them RETIRE outright
> (PERM-VYATKA §0.5's eleven Uralic religions sit on 71/63/84 POP
> locations; AMERICAS' CLM teco is on CLM's own six; Kedah shrinks to
> one line). Re-measure against POPS, not templates. Also note its
> anchor-class find: `location_templates.txt` is a ONE-LINE-BLOCK file —
> a line-anchored parser returns a confident zero. This file's :79
> Basileia citation says `mozarab`; the actual key is `mozarabic`.

# THE POP PHASE — decoded data layer + generator design brief

> Produced by the pop-conversion research pass (Opus agent, 2026-07-29
> night), reviewed by the main session. Every number is a measurement;
> historical demography carries the three-tier confidence framework
> (STRONG direction / DIRECTIONAL / DEBATED percentages — percentages
> are named constants with [U] comments, never baked into machinery).

## 1. THE DATA LAYER

- `06_pops.txt`: 28,570 location blocks, 50,255 `define_pop` entries,
  393,896 units (×1000 people — DISPLAY_SIZE, defines:1601). NO BOM.
  Exactly 4 fields per pop: `type size culture religion` — never
  optional, never extra; binding to location is positional; no estate
  field, no dates, no literacy (Location Painter emits `literacy` —
  UNATTESTED, do not use).
- **Elite pops are SEEDS, not populations**: all 1,805 noble pops
  world-wide sum to 33 units. nobles/clergy/burghers have
  `has_cap = yes` and the engine INFLATES them to their caps at load
  (wiki: Starting pop logic). Author IDENTITY, not quantity — this
  makes the estate-culture fix disproportionately cheap.
  **In-game verification of pop work requires the `-leavepops`
  launch option** or you measure the inflation, not the file.
- **THE MERGE TRAP** (defines:1633-1634):
  `POP_MINORITY_SIMILAR_THRESHOLD = 4`, `JUST_MERGE = 8` — ≥4 pops of
  one TYPE per location merge similar, ≥8 collapse to the largest.
  Vanilla's own max is 6, never 7. **≤3 per type per location is the
  safe zone**; ≥8 silently destroys a minority split.
- **Estate culture is 100% derived** (weights defines:1679-1685:
  primary 1.20 / accepted 1.00 / tolerated 0.50 / discriminated 0.25,
  ×1.10 incumbency, 60-month cooldown; no set_estate_culture effect
  exists). Seed the elite pops' culture and the estate follows.
  `is_dhimmi` (pop_triggers.txt:1-15) is religion-group + Muslim
  owner — Mozarab/Coptic/Jewish pops under Muslim rule land in
  dhimmi_estate automatically; no reciprocal estate exists for
  Muslims under Christians.

## 2. THE LAYER MODEL (the central question, answered)

**`06_pops.txt` is the STATE; `location_templates.txt` is the
load-time SEED.** Location has NO GetCulture/GetReligion — only
GetDominantCulture/GetDominantReligion (pop-derived, cached —
`force_refresh_culture_and_religion` proves it). Every trigger,
estate, levy, mapmode reads pops. The layers disagree in 3,419/20,803
locations (2,142 with ZERO pops of the template religion — e.g. the
whole Jiangnan mahayana/sanjiao cluster). Corroborated: Basileia
rewrote Anatolian demography with ZERO map_data files; Location
Painter writes its culture/religion tabs into 06_pops; our own :237
errors compare against pops. The template pass (Bronze Era's shape:
copy vanilla, rewrite ONLY religion+culture, keep everything else) is
DEFERRED until slice 0 answers whether it is needed at all.

Pop inputs at start: tax_per_pop (nobles 100 / clergy 25 / burghers
40 / peasants 1 / dhimmi 1), power_per_pop, levies per-pop, control
via literacy, market attraction via dominant language,
ECONOMICAL_BASE_FROM_POP. Development has NO pop term (capacity flows
the other way). No over/under-capacity setup errors exist.

**THE ACCEPTANCE INTERACTION:** cost = 3 × (1 + Σfactors)
(defines:1447-1458); TWO factors are pop shares (country + world,
×0.35 each, clamped ±0.35). Our measured farsi 3.89 = 3 × 1.2967
against farsi's measured 20.8% share of SEL. **The Mongol-strip slice
raises that share → SEL's capacity-8.00 calibration must be
re-measured after.** And `ACCEPTED_CULTURE_SETUP_ERROR_IF_ABOVE_MAX
= 2` / `_IF_BELOW_MAX = 1` fire in BOTH directions — a mod-wide new
error class every slice can trigger outside its own theatre.

## 3. THE TARGETS (measured debt → rules)

| theatre | locs/pops/units | 1337 measured | 1066 rule |
|---|---|---|---|
| al-Andalus | 244/928/3,902 | catholic 77.8% | amplify andalusi/sunni (seeded in 175/244); RE-LABEL Christians as `mozarab` (invented — Basileia's br_iberia.txt:24 is the template, reuses maghrebi_dialect); keep sephardi; elite seed andalusi/sunni |
| Anatolia | 258/1,003/5,371 | turkic 40.6% | DELETE all turkic/mongol pops, redistribute proportionally; seed the 41 Christian-less locations (greek/armenian by band); use cappadocian/pontic greek keys |
| Sicily | 23/88/716 | sunni 0.0%! | **`maltese` IS the shipped Siculo-Arabic** (italian.txt:93, groups italian+maghrebi+arabic); Mazara 0.80 / Noto 0.55 / Demone 0.25; amplify griko |
| Calabria+Apulia | 30/226/823 | griko 10.1% everywhere | amplify only |
| Egypt/Levant | 122/424/5,755 | coptic 14.5% | raise coptic/miaphysite toward 0.40 [U 0.30-0.60]; Melkite = orthodox proxy; FAT elite stays lower_egyptian/shia |
| Seljuk Persia | 463/1,963/4,099 | **mongolian+nogai 11.0%** | KNOWLEDGE's "no pop debt" was RELIGION-ONLY — strip the Mongol layer (451 units/150 locs), religion untouched |
| Ireland | 95/345/708 | anglo_irish+english 17.0% | delete, redistribute to irish; KEEP norse_gael (Dublin/Waterford/Limerick genuinely Hiberno-Norse) |
| Wales | 25/58/309 | english 20.4% | delete |
| England | — | english/northumbrian | **NO CHANGE — vanilla is accidentally right** (norman is 0.3% of Britain; anglo_saxon does not exist and is not needed) |
| Baltic+Finland | 194/588/1,287 | catholic 41.3% | → romuva / muinaisusko; Scandinavia proper NO CHANGE |

Total: ~5,623 entries = 11.2% of the world, for territory already done.

**Identifiers: amplify, don't invent.** Existing and populated:
griko (79 pops), coptic_culture (102), sephardi+11 Jewish (1,108),
cappadocian/pontic greek, maltese, norse_gael, andalusi. The ONLY
required invention: `mozarab`. **Invent the culture, never the
language.** Spelling traps: romanyoti, zenati, nestorianism, judaism,
andalusi (no suffix) — 332 of 2,087 culture keys lack `_culture`;
verify every key.

**THE SLAVIC PAGANISM DECISION — TAKEN (user, 2026-07-29 night):
INVENT the religion.** `slavic_paganism` will be authored on romuva's
template shape (one religion entry + loc + color) as part of the
Baltic pop slice; Mecklenburg/Pomerania's 895.8 catholic units
convert to it. It also grounds the Obodrite-revolt and Wendish
Crusade (1147) situation material. The Baltic slice is unblocked.

**Emptying a culture world-wide** (anglo_irish → 0) errors unless the
culture carries `suppress_no_pops_error = yes`
(cultures/00_cultures.info:28; vanilla has exactly 3 zero-pop
cultures). Add it via **`REPLACE_OR_CREATE:`** — a real prefix
KNOWLEDGE's list lacks (Basileia ×167) — never a whole-file cultures
override.

## 4. GENERATOR

- **A sixth TARGETS entry in build_setup.py**: ("06_pops.txt",
  build_pops). Whole-file override (additive cannot delete),
  NO `replace_paths` (it would force shipping all 25 setup files —
  Basileia's cost; Bronze/Anno prove the single-override route).
- **Reuse the territory rule sets** (_TAIFAS, _byz_target,
  _resolve_ruleset over _SELJUK/_EGYPT/_FRANCE rules, the grant
  dicts — verified importable this session): pop scope keys off the
  SAME source of truth as borders.
- **Per-theatre slices, cheapest-signal first:**
  0. **SICILY PROBE (23 locs, pops-only, NO template file)** — the
     smallest, 100%-invention theatre; one launch answers whether
     pops alone flip the map (template override then stays OUT of
     the mod entirely) — the whole design's fork.
  1. Wales+Ireland (pure deletion — retires 3 named error lines).
  2. al-Andalus. 3. Anatolia. 4. Seljuk Mongol strip (+capacity
  re-measure). 5. Egypt. 6. Baltic (blocked on the Wendish call).
  7. Rest-of-world with the border review.
- Safety rails (each proven by breaking): exact touched-count per
  theatre; every rule-set location present in 06_pops; unit
  conservation ±0.1% on re-labels; **≤3 per type per location**
  (ceiling 6); identifiers resolve (incl. our additive files); no
  culture emptied without suppress_no_pops_error; share-band asserts;
  4-field shape; block-name SET equals vanilla's 28,570 (the Bronze
  Era guard — their generator shipped 2,633 duplicate blocks, 502
  phantom locations and 3,131 dropped ones, and shipped anyway).

## 5. ERROR BUDGET

RETIRES: the estate/pop culture class (237/301 — GDD/MWG/DUB/GLC),
the releasable-culture lines (ours; vanilla's ATH stays — do not
chase), item 22's emirate debt, item 13's Castilian-Seville limit.
CREATES: the accepted-culture both-directions class (mod-wide);
SEL calibration drift; silent minority merges (guarded);
zero-pop cultures (guarded); every slice is a balance change in a
data commit's clothes — say so in its test list.

## NEW TRAPS (banked to KNOWLEDGE)

1. **11 vanilla location keys carry UPPERCASE letters**
   (trgoviste_SER, targoviste_BUL, ratnapura_LKA, tata_MOR,
   massa_MOR, asir_ALG, al_khadra_ALG, constantine_ALG, beja_TUN,
   jama_TUN, matanda_aChiwawa — 28 pops between them). A lowercase
   location regex silently drops all 11; the agent's own first
   parser did (50,228 vs 50,255). `[A-Za-z0-9_]+` always.
2. **in_game/map_data/ is BOM-MIXED** — definitions.txt HAS one,
   location_templates.txt does NOT. If the template override ever
   lands, verify_mod's BOM check needs the documented exception in
   the same commit.
3. **`REPLACE_OR_CREATE:`** exists (Basileia ×167) — the right tool
   for one-entry additions to vanilla databases.
4. Never ship `*_backup.txt` in a loaded directory (Bronze does — a
   live duplicate-definition hazard).
