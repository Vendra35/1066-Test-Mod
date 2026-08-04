# WELSH WARS (spec 9) — GROUND VERIFIED, BUILD NOT STARTED

> Session 2026-08-04 (second sitting) ran the ENTIRE ground-verification
> pass for spec 9 and stopped on the user's usage limit BEFORE writing
> any file. Everything below is verified with file:line — the next
> session starts at "BUILD PLAN" and writes, it does not re-derive.

## Ground (all verified this session)

- **Tags + rulers seated** (10_countries.txt:4387-4475): GDD Bleddyn
  (gdd_bleddyn_ap_cynfyn), PWS Rhiwallon (pws_rhiwallon_ap_cynfyn),
  DHB Maredudd (dhb_maredudd_ab_owain), MWG Cadwgan
  (mwg_cadwgan_ap_meurig), GWT Caradog (gwt_caradog_ap_gruffydd).
  DHB core list has carmarthen cardigan aberystwyth pembroke fishguard
  kidwelly brecknock builth radnor; PWS has penllyn montgomery
  machynlleth llangollen; MWG has caerphilly.
- **ALL FIVE map_ colour keys are VANILLA'S** —
  `main_menu/common/named_colors/02_map.txt:61-66` (map_GDD :61,
  map_PWS :62, map_MWG :63, map_GWT :65, map_DHB :66). The Iberian
  trap again: REUSE, never redefine. Scaffolder sides = all None.
- **`set_new_ruler`**: country scope, character target
  (effects.log:10245-10248). **Cross-court precedent =
  `c:ARS = { set_new_ruler = character:eng_robert_iii_artois }`**
  (vanilla hundred_years_war.txt:805, :980) — a setup character
  seated on ANOTHER country's throne years later. This kills any
  need for the runtime-cast probe in spec 9.
- **`is_alive`**: character scope (triggers.log:6115-6119).
- **Characters are GENERATED**: `tools/build_setup.py` embeds the
  05_characters blob; Welsh five at :4908-4962, Mael Snechtai ends
  the British section at :4980-4988, southern Italy starts :4990.
  **INSERT the four new Welsh actors between :4988 and :4990**, then
  `python tools/build_setup.py` (main :9105 — regenerates all
  targets from vanilla source, writes BOM-free; --dry-run exists).
  Only 05_characters.txt should diff.
- **Dynasties**: mathrafal + aberffraw SHIP (vanilla
  04_dynasties.txt:213/:614). dinefwr_dynasty/morgannwg_dynasty/
  gwent_dynasty are OURS (04_zz_1066_dynasties.txt:194-203, homes
  carmarthen/cardiff). **ADD `arwystli_dynasty` there** (home =
  machynlleth [U]; Trahaearn's house — vanilla has none). Dynasty
  loc rows precedent: 1066_norman_conquest_l_english.yml:196-197
  ("Dinefwr"/"Morgannwg") — put `arwystli_dynasty: "Arwystli"` in
  the welsh_wars loc file.
- **Name routes**: vanilla literal `Gruffydd: "Gruffydd"`
  (character_names_l_english.yml:860; also ap_Gruffydd :1064) —
  Gruffudd ap Cynan is free. NO vanilla Rhys/Trahaearn — two OUR
  literals with loc rows (`Trahaearn:`, `Rhys:`), the
  Bleddyn/Rhiwallon precedent (those rows live in
  1066_norman_conquest_l_english.yml:199-200).
- **`dublin` location exists** (DUB capital = dublin,
  10_countries:58763) — Gruffudd's birth + court (tag = DUB), the
  HYW eng_-prefix-on-ARS-throne convention.

## The four new characters (build_setup blob, [U] births)

```
gdd_trahaearn_ap_caradog  — Trahaearn, welsh, catholic, b.1025 montgomery, arwystli_dynasty, tag GDD
dhb_rhys_ab_owain         — Rhys, welsh, catholic, b.1035 carmarthen, dinefwr_dynasty, tag DHB
dhb_rhys_ap_tewdwr        — Rhys, welsh, catholic, b.1040 carmarthen, dinefwr_dynasty, tag DHB
dub_gruffudd_ap_cynan     — Gruffydd (vanilla literal), welsh, catholic, b.1055 dublin, aberffraw_dynasty, tag DUB
```

Spec said AUTHOR 3; Rhys ab Owain is the FOURTH — he must exist
because .30's declinable murder plot is HIS, and .40 kills him by
name. (Bleddyn was killed 1075 at Rhys ab Owain's instigation; the
spec's [D] beat.)

## BUILD PLAN (decided; spec-faithful: pure kill/set_new_ruler, NO
unions/annexes/wars — Mechain's joint rule is narrated, not modelled)

Key `welsh_wars`, title "The Sons of Cynfyn". Files mirror
three_brothers (situation/events/gui/hints/loc; NO colors file, NO
modifiers file, NO 16_wars, on_monthly EMPTY — no declared wars, so
the lock probe is irrelevant here).

- **SPECS entry** in new_situation.py: sides
  `{"GDD": None, "PWS": None, "DHB": None, "MWG": None, "GWT": None}`,
  events (1,10,20,30,40,50,60,90); run scaffolder, then arm.
- **can_start**: `current_date >= 1069.1.1` + five country_exists.
- **on_start**: intro .1 non-silently to the five courts (?=-guarded).
- **Events** (DHE windows, monthly_chance = 100, fire_only_once,
  three_brothers.txt is the exact shape template):
  - **.10 Mechain** (GDD, 1069.1.1-1069.9.1): trigger rhiwallon
    is_alive; a (rail): kill_character rhiwallon location:montgomery
    [U-nearest], prestige mild; b: stability mild. PWS succession =
    engine heir [U], accepted.
  - **.20 the Rhymney** (GWT, 1072.1.1-1072.9.1): trigger maredudd
    is_alive + DHB exists; a (rail): kill maredudd
    location:caerphilly, `c:DHB ?= { set_new_ruler =
    character:dhb_rhys_ab_owain }`, GWT prestige; b: flavour only —
    NO spare flag (one divergence per situation, the tb precedent).
  - **.30 the murder of Bleddyn [D]** (DHB, 1075.1.1-1075.9.1):
    trigger bleddyn alive + trahaearn alive; a (ai 100): kill
    bleddyn location:carmarthen [U — Ystrad Tywi], `c:GDD ?= {
    set_new_ruler = character:gdd_trahaearn_ap_caradog }`; b (ai 0,
    the player's refusal STICKS): set_variable ww_bleddyn_spared
    years = 15 + stability mild. [WATCH: kill→seat in one option —
    engine auto-succession runs on the kill, set_new_ruler then
    overrides; each half attested, sequence needs the game test.]
  - **.40 Pwllgwdig** (GDD, 1078.1.1-1078.9.1): trigger
    `NOT = { c:DHB ?= { has_variable = ww_bleddyn_spared } }` +
    rhys_ab_owain alive; a (rail): kill rhys_ab_owain
    location:fishguard, `c:DHB ?= { set_new_ruler =
    character:dhb_rhys_ap_tewdwr }`, GDD prestige; b flavour.
  - **.50 Mynydd Carn** (DHB, 1081.4.1-1081.12.1): trigger not-spared
    + trahaearn alive + gruffudd alive; a (rail): kill trahaearn
    location:fishguard [U — nearest to the field], kill caradog
    location:fishguard, `c:GDD ?= { set_new_ruler =
    character:dub_gruffudd_ap_cynan }` (THE HYW SHAPE), set_variable
    ww_carn_won (no years — permanent); b flavour. GWT succession =
    engine heir [U].
  - **.60 St David's** (ENG, 1081.6.1-1082.6.1): pure flavour march,
    prestige either way, no mechanics.
  - **.90 closing** (on_ended, every can_see country).
- **can_end** custom_tooltip OR-ladder: settled =
  `current_date >= 1081.6.1` + `c:DHB ?= { has_variable =
  ww_carn_won }` (welsh_wars_end_settled_tt); expired =
  `current_date >= 1085.1.1` (welsh_wars_end_expired_tt).
- **visible**: five tags + ENG + capital sub_continent
  western_europe (tb shape).
- **map_color**: five plain owner branches (no subject branches —
  none have subjects), five legend_keys, secondary five branches;
  ALL colours vanilla's.
- **Loc** (~45 rows, tb file is the template): base+desc+info, hint
  family (hint_welsh_wars + _hint_text + _1..3), two end tooltips,
  8 events × (title+desc+a+b), literals `Trahaearn:`/`Rhys:`,
  `arwystli_dynasty: "Arwystli"`.
- **Harness floors same commit**: situation fields 39→+welsh block,
  hint contract 12→16, DHE 14→+5 (the five DHE windows here).
- Then HANDOFF item 52 + Turkish click tour + slice/docs commits.
