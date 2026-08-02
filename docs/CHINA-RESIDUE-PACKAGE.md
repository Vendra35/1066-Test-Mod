> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 41 (commit 401952b) —
> NOT yet game-tested. THE MAP PHASE CLOSES WITH THIS SLICE.** Research
> record, not the state. Decisions as implemented: 1 BOTH identity lines
> + the ARA cure, 2 the slider DELETED, 3 all 28 tusi, 4b (HQG+YAN into
> CDL; 4c's ring refused), **5 the review's call — governorship stripped,
> num→0, LIA→KOR tributary added** (item 32's divergence overturned
> because item 33 created the Liao under it), **6 Alt Q extended** —
> see deviations — 7 CDL stays in the MK, 8 floor 27→850 proven by
> breaking. KNOWN DEVIATIONS, code wins: **the package's "BKH, KTT and
> GHZ are all monarchies" was REFUTED by `_bad_recip` at first run — KTT
> is a `steppe_horde`** (the first package error after three clean ones,
> caught by the build's guard, not the review; kulob/munk joined the
> Alt-Q vacate, EXPECT 5, vacated 630; KTT's horde state banked);
> **ghosts moved 156→160, not 158** — the package forgot its own §4.2
> (HQG and YAN are MK members too; MK 198→196); parliament observed
> 1360 (QUN counted); break-test (c) fired via the YAN-still-owns guard
> rather than naming GYT (loud either way — the lijiang trap comment
> stands in `_CHINA2_RULES`).

# CHINA RESIDUE 1066 — the closing package of the map phase: what D2-D7 really landed, and the Northern Song that is still Mongolian (DRAFT)

**Research agent model ID: `claude-opus-5`.**

**DRAFT — pending main-session review. Nothing here has been written into any
mod file.** Produced by an Opus research agent, 2026-08-02, against the working
tree at HEAD `0a39b5f` (40 items landed; constants read from the code, not from
prose: registry 74 blocks, country blocks 2411, thrones 179, landless-dep strips
281, pacts 9, IO ghosts 156, vacated 625, parliament min 1363, loc rows 375, CoA
125). Every mechanical claim carries a `file:line`. Historical claims that no
file can settle are flagged `[U]` (unverified — the agent's own history, no
source in the repo) or `[D]` (sources genuinely differ), never asserted
silently. §VERIFICATION collects them.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, present)
`MOD = .../1066 Test Mod`

**Method — the Tibet / Perm-Vyatka / Americas method, applied unchanged.** No
reader was reimplemented. This package `import`s `tools/build_setup.py` (its
`__main__` guard is at `:8288`) and calls its own parsers: `_parse_defs`
(`:748`), `_ownable_set` (`:772`), `_defs` (`:809`), `find_block_end` (`:5595`)
and `COUNTRY_RE` (`:5648`). Ownership is read with the **full ten-member
`OWN_KEYS` tuple copied verbatim from `build_setup.py:5790-5793`** —
`own_control_core, own_control_integrated, own_control_conquered,
own_control_colony, own_core, own_conquered, own_integrated, own_colony,
control_core, control` — i.e. `_owned_by`'s logic (`:5828-5843`), comments
stripped. Registry scans use the **loose whitespace form**
`^([A-Z0-9]{2,6})[ \t]*=[ \t]*\{` (`KNOWLEDGE.md`, "A single-space registry
regex misses 94 of vanilla's 2,340 identity blocks"). Everything reads
`encoding='utf-8-sig'`. Scripts live in the session scratchpad; nothing was
written into the repo but this file.

**Proven on known positives BEFORE any new ground, including
`own_control_integrated` cases.**

| probe | expected (source) | measured |
|---|---|---|
| vanilla country blocks | 2,337 | **2,337** |
| mod country blocks | 2,411 (`HANDOFF.md`, item-40 constants) | **2,411** |
| **VTN in vanilla** | **32** — the `own_control_integrated` proof (`KNOWLEDGE.md`, phantom-unowned law) | **32** |
| **PLB** | **40** | **40** |
| **TIB in vanilla** | **59** (`TIBET-PACKAGE.md` §0.7) | **59** |
| MUA / BTU / MGD in vanilla | 15 / 6 / 5 | **15 / 6 / 5** |
| vanilla identity tags, loose regex | **2,340** (`CLAUDE.md`) | **2,340** (strict `^TAG = {` returns 2,246 — the 94-block gap reproduced) |
| mod new-country registry blocks | **74** | **74** |
| locations vacated by the build | **625** | **625** |
| IO members scanned by the harness | 854 (`verify_mod.py` run) | **854** |
| empty IO member lists (mod / vanilla) | 9 pinned / 11 | **9 / 11** |
| `define_pop` in `06_pops.txt` | 50,255 over 28,570 locations | **50,255 / 28,570** |
| harness | all green | **all 33 checks green, working tree clean** |

**Scope.** The audit covers `INDIA-CHINA-REVIEW.md`'s D2-D7 and its §5.2
residue list. The prescription covers the Yunnan/Dali world
(`south_china_region / dali_area + yunnan_area`, 139 ownable locations) plus the
three genuine leftovers no item landed. Everything closed by items 30/32/33/34/38
is measured and named in §5, not redesigned.

---

## 0. THE AUDIT — D2 through D7 against the build that actually shipped

Measured, not read off the prose. Two of the review's own prescriptions were
knowingly diverged from at implementation, and one whole half of a prescription
was never implemented at all and nobody has noticed for a day.

### 0.1 Scoreboard

| # | review's prescription | landed as | verdict |
|---|---|---|---|
| **D1** | Route B — restore the Middle Kingdom re-dated | item 30 | **DONE**, measured in game 2026-08-01 (four error classes died together). Instance at `MOD/…/15_international_organizations.txt:164`, `creation_date = 960.2.4`, `leader = CHI`, 198 members |
| **D2** | CHI Yuán → Sòng: `flag`/`country_name` → `"CSO"`, drop `legacy_of_kublai_khan`, drop `status_of_the_han_law`, capital → `kaifeng` | item 32 | **DONE for every token the review named — and the review named the wrong four.** The state's *identity* (culture + religion) is still the Yuan's. **§1** |
| **D3** | CHI drops Mongolia + Manchuria (198); the eight Chinggisid hordes go landless (170) | items 32 + 33 | **DONE and superseded.** `LOCATION_VACATED["CHI"] = ["mongolia_region","manchuria_region"]`, `_EXPECT = 113` (`build_setup.py:1425-1426`) — 198 minus the 85 LIA took first. Measured: mongolia LIA 149 / unowned 64; manchuria LIA 48 / unowned 112 / tribal 63. **No residue** |
| **D4** | The Liao — defer, or reskin SYG | item 33 | **DONE, and beyond the review**: LIA created (310, Daozong, `yelu_dynasty`), XIA created (48, Yizong), SYG retired landless. **No residue** |
| **D5b** | Punjab → GHZ, then behead DLH | items 32 (D5a) + 34 (the behead) | **DONE.** GHZ 34 → 131; DLH **0** and in `LANDLESS_AFTER` (`build_setup.py:3024`, 315 members). **No residue** |
| **D6** | Retire the nine impossible Indian tags | item 34 | **DONE** and enlarged to nineteen. Measured: VIJ 0, MAB 0, SMA 0, RDY 0, RCH 0, JFN 0, SMV 0, MSN 0; DBD **survives at Vijayabahu's Ruhuna** — the review's own list overturned on evidence. **No residue** |
| **D7** | Seven cheap seats + the JAP reform swap | items 30 + 32 | **DONE — 8 of 7.** All seven seated, plus KHM. `HISTORICAL_RULERS` (`build_setup.py:69`) carries CHI, JAP, KOR, DAI, CHA, CDL, KHM, HSL. TIB left random, then TIB retired entirely (item 38). **No residue** |
| §5.2/1 | strip `CHI → KOR` vassalage | item 32 | **DONE** — KOR carries **zero** dependencies |
| §5.2/2 | strip `CHI → TIB` vassalage | item 38 | **DONE** — died free in the landless sweep |
| §5.2/3 | strip `LNG → CDL` | item 32 | **DONE** — died with LNG's retirement. **But its 46 sibling ties died with it too, and that is the Dali residue. §3** |
| §5.2/4 | remove `celestial_governor = { KOR }`, set `num_of_celestial_governors = 0` | — | **NOT DONE — a deliberate, recorded divergence** (item 32: "its celestial_governor seat in the restored IO IS the historical tie"). Both lines still present at `MOD/…:164` block. **Open decision 5** |
| §5.2/5 | the 4 `hindu_branch` member lists | item 34 | **DONE** — harness green at 854 members, zero landless non-`type` members |
| §5.2/6 | the `shinto` IO — "flagged as worth a look" | — | **NOT DONE, correctly.** `creation_date = 539.12.5`, JAP + ~150 `type = building` clan tags (`MOD/…:230`). Legitimate under the harness's own exemption (`verify_mod.py:874-880`). Japan-slice work, not residue |
| §5.2/7 | **retire QUN with the India pass** | — | **NOT DONE.** QUN still holds 6 and is the **last** tag producing `initialize_from_bookmark.cpp:2477` (decoder, "down to QUN alone"). **§4.1, open decision 6** |

**Bottom line: D3, D4, D5, D6, D7 and five of the seven §5.2 items are closed
with zero residue.** What is genuinely open is (a) D2's unnamed half — the
registry identity, §1-§2; (b) the Dali/Yunnan world that D3's LNG retirement
created and no decision ever covered, §3; (c) three named leftovers, §4.

### 0.2 What the review got wrong that this audit can now settle

- **§2.2's "two token changes" was the whole miss.** The review located `CSO`'s
  identity block (`VAN/in_game/setup/countries/east_asia.txt:1169`) and quoted
  its `culture_definition = zhongyuan_culture` / `religion_definition = sanjiao`
  **in the same paragraph** — then prescribed only `flag` and `country_name`.
  It never noticed that CHI's own block, thirty lines above, carries
  `mongolian_culture` / `tibetan_buddhism`, and that those are what the engine
  reads. Implementation followed the prescription faithfully. §1.
- **§1.5's `song_mandate_reform` magnitude argument survives, in a smaller
  form.** Route B restored `cultures_capacity = 50` via the IO leader_modifier,
  as predicted; the implementation still had to add
  `song_civil_service_reform` at **+16** (`in_game/common/government_reforms/
  zz_1066_reforms.txt:173-186`) after the grand test logged 66.18/53 — because
  dropping `legacy_of_kublai_khan` cost 3 and the share-based costs rose when
  the steppe left. The review's "do not shave it" lesson held.
- **§1.6's "risk in Route B" (the 107 non-CHI tusi and the culture branch)
  never materialised in the shape predicted.** The real breakage was
  `can_country_have_tusi`'s **subject** branch, not its culture branch: LNG's
  retirement freed sixteen mid-tier lords, whose 45 sub-ties then failed
  `country_triggers.txt:1291-1293`. The jimi repoint (`build_setup.py:
  7588-7610`, exact count 16) fixed it. Branch 3 (`:1295-1301`) is not in play
  anywhere in the current build.

---

## 1. THE HEADLINE: the Northern Song is a Mongolian-culture, Tibetan-Buddhist state, and nothing in the game says so out loud

### 1.1 The two lines

`MOD/in_game/setup/countries/east_asia.txt` is already a whole-file override
(item 32, header-documented, "EXACTLY TWO intended changes"). CHI's block:

```
:1148   CHI = { #China
:1149       color = map_CSO # 1066: the Song crimson (vanilla's own key)   <- item 32 changed THIS
:1150       color2 = rgb { 16 41 202 }
…
:1156       culture_definition = mongolian_culture                          <- untouched
:1157       religion_definition = tibetan_buddhism                          <- untouched
```

Seven lines below the line item 32 edited sit the Yuan's culture and the Yuan's
religion, wearing the Song's crimson.

Vanilla's own Song identity block, which the review quoted and nobody used:

```
VAN/in_game/setup/countries/east_asia.txt:1169   CSO = {	#Song
:1170       color = map_CSO
:1171       color2 = rgb { 153 51 51 }
:1172       culture_definition = zhongyuan_culture
:1173       religion_definition = sanjiao
:1174       is_historic = yes	#Released during the Crisis events
```

### 1.2 Why those two lines are not decoration

`KNOWLEDGE.md`, "The registry's `culture_definition` IS a landed tag's primary
culture — measured": established in game 2026-07-29 by the ARA duplicate
(`country.cpp:6166`), which is only possible if the registry field IS the
primary. `CLAUDE.md` states the same for both fields: "the registry's
`culture_definition`/`religion_definition` are read at bookmark init".

This project's own new tags all treat the pair as a design decision, never a
default: LIA `kharchin_culture`/`mahayana`, XIA `mi_niah_culture`/`mahayana`,
PAA `bengali`/`mahayana` (the deliberate "Buddhist identity over hindu pops"),
TKA `amdowa_culture`/`tibetan_buddhism`
(`MOD/in_game/setup/countries/zz_1066_new_countries.txt:521, :577, :553, :705`).

### 1.3 What the ground says — measured over all 50,255 `define_pop`

CHI's **1,300 held locations**, pop-size weighted:

| | value | share |
|---|---|---|
| religion `sanjiao` | 74,645.7 | **96.1 %** |
| religion `tibetan_buddhism` — **the state religion** | **3.853** | **0.005 %** |
| culture `zhongyuan_culture` | 5,826.5 | 7.5 % (largest single culture in north China at 24.2 %) |
| culture `mongolian_culture` — **the primary culture** | **0.171** | **0.0002 %** |

**The capital settles it on its own.** `kaifeng`'s pops
(`VAN/main_menu/setup/start/06_pops.txt`) are `zhongyuan_culture` /`sanjiao`
throughout — nobles, clergy, burghers, peasants — beside vanilla's two lovely
minorities, a `qayfengi`/`judaism` burgher-and-peasant pair (the Kaifeng Jews)
and a `hui_muslim_culture`/`sunni` peasant pop. **Not one Mongol, not one
Tibetan Buddhist, in the Song capital.**

`zhongyuan_culture` is `chinese_group` + `confucian_group`
(`VAN/in_game/common/cultures/east_asia.txt:257-270`); `mongolian_culture` is
`mongolian_group` + `steppe_group` (`:1112-1126`).

### 1.4 What it silently changes, today

No error line names any of this. The consequences are all in the "silent
failure is the default failure" class:

- **Every `culture_group` gate in the game reads CHI as a steppe power.**
  `cb_claim_mandate_of_heaven` (`VAN/in_game/common/casus_belli/
  unify_china.txt:33, :51`) lists `chinese_group / confucian_group /
  jurchen_group / mongolian_group` — CHI qualifies through the Mongol door.
  `CHI_f` (`00_formable_countries.txt:3940-3956`) gates on
  `has_culture_group = culture_group:chinese_group` at `:3947`.
- **The Song's own heartland cultures are merely *accepted*.** CHI carries 9
  accepted + 61 tolerated (vanilla: 9 + 72; item 32 removed eleven steppe
  entries). The primary culture — the one that costs nothing and assimilates —
  has 0.0002 % of the population.
- **CHI is a `tibetan_buddhism` country belonging to no sect.**
  `tibetan_buddhism` is `max_sects = 1`
  (`VAN/in_game/common/religions/buddhist.txt:110`); vanilla's Sakya sect,
  which is where vanilla put CHI (`VAN/…/15_international_organizations.txt:
  1472`, members include `TIB CHI GUG MGG LGT LNG`), is dated **1073.1.1** and
  our future-date strip deleted it months ago — the creation-date law, working
  exactly as `KNOWLEDGE.md` describes. So CHI joins Tibet's 28 sect-less tags
  as a 29th instance of the same OWED in-game check.
- **`sanjiao` is `max_sects = 3` (`buddhist.txt:133`) and no `sanjiao` sect
  instance exists in the game at all** — the 21 surviving sects are mahayana,
  shinto, tibetan_buddhism and theravada only. So the fix does not create a
  sect obligation; it removes a `max_sects = 1` one.

### 1.5 What it does NOT change — checked, because this is the reassuring half

**The "Great Sòng" render is safe.** Both branches that build CHI's name and
rank read the **court language and the IO leadership, never the culture**:

- `VAN/in_game/common/customizable_localization/country_name_construction.txt:
  91-96` — `country_name_construction_prefix_name`, trigger
  `country_rank ?= rank_empire` + `court_language ?= { language_family ?=
  language_family:chinese_language_family }`. CHI's `court_language =
  northern_mandarin_dialect` is untouched by anything proposed here.
- `VAN/in_game/common/customizable_localization/country_ranks.txt:481-493` —
  `rank_empire_dynasty`, trigger `country_rank_is_empire` + (chinese court
  language **OR** `is_leader_of_international_organization =
  international_organization:middle_kingdom`). Both hold.
  (`government_names_l_english.yml:95`, `rank_empire_dynasty: "Dynasty"`;
  `:13`, `country_name_construction_prefix_name: "$PREFIX$ $NAME$"`.)

**`three_departments_system` stays valid.** Its `potential`
(`VAN/in_game/common/government_reforms/country_specific.txt:2140-2170`) is an
OR whose surviving branches for CHI are `court_language.language_family ?=
chinese_language_family` and MK leadership. Neither moves.

### 1.6 The one thing the fix breaks, and its one-line cure

`zhongyuan_culture` is **already in CHI's `accepted_cultures`** (position 2 of
9). Making it the primary without removing it from the accepted list reproduces
the ARA defect exactly — `country.cpp:6166`, "primary culture is duplicated in
accepted cultures". `KNOWLEDGE.md`: "never repeat the primary in the accepted
list." The cure is one `FIELD_FIXES` pair on CHI (`build_setup.py:3158`, applied
`:6497+` with an exact-once assert), dropping `\n\t\t\tzhongyuan_culture` — the
identical shape to the eleven steppe-culture removals item 32 already ships at
`:3444-3454`. Accepted goes 9 → 8, which *returns* cultural capacity rather than
spending it.

---

## 2. The sinicization slider is inverted — and correcting §1 makes the line inapplicable rather than merely wrong

### 2.1 The axis, measured

`VAN/in_game/common/societal_values/00_default.txt:389-421`:

```
sinicized_vs_unsinicized = {
	allow = {
		NOT = { culture ?= { has_culture_group = culture_group:chinese_group } }
		OR = { is_subject_of = c:CHI   … capital sub_continent east_asia/south_east_asia
		       … is_member_of_international_organization = middle_kingdom }
	}
	left_modifier  = { #Sinicized    legislative_efficiency 0.25  research_speed_modifier 0.1
	                                 cultural_tradition_modifier -0.5  global_merchant_capacity_modifier 0.2
	                                 tribute_payment_received_modifier 0.25 }
	right_modifier = { #Unsinicized  prestige_decay -0.002  stability_cost_efficiency 0.66
	                                 cultural_tradition_modifier 0.5  global_merchant_capacity_modifier -0.2 }
}
```

Left is Sinicized, right is Unsinicized — i.e. **negative = sinicized**.
Vanilla's own setup values are unanimous:

| template | value | who they are |
|---|---|---|
| `far_east_asia_monarchy.txt:26` | **−70** | China itself |
| `japanese_clan.txt:26` | −50 | the Japanese court |
| `jianzhou_tribe.txt:19` | −5 | the Jianzhou Jurchen — the **most** sinicized of the three groups [U] |
| `asia_tribe.txt:20`, `asia_advanced_tribe.txt:21`, `asia_advanced_no_pagan_tribe.txt:21` | +10 | generic Asian tribes |
| `haixi_tribe.txt:19` | +25 | the Haixi Jurchen |
| **`yeren_tribe.txt:19`** | **+95** | the Yeren — "wild men", the **least** sinicized [U] |

### 2.2 What we shipped

`build_setup.py:3456-3457` writes onto CHI:

```
sinicized_vs_unsinicized = 50 # the Song court [magnitude ours; positive = sinicized, asia templates +10]
```

The bracketed note has the sign backwards, and cites `asia templates +10` — the
tribes — as its evidence for "positive = sinicized". Vanilla's Yuán shipped
**−50** with the comment `# Bayan's policies`. **We moved the Song 100 points
in the unsinicized direction from where the Yuan sat**, and it currently earns
`prestige_decay −0.002 / stability_cost_efficiency 0.66 /
cultural_tradition_modifier +0.5 / global_merchant_capacity_modifier −0.2`
instead of the bureaucratic package a Song court should have.

### 2.3 The coupling that makes this cheap

The `allow` block's **first** statement is
`NOT = { culture ?= { has_culture_group = culture_group:chinese_group } }`. The
moment §1 lands, CHI's primary is `zhongyuan_culture`, which **is**
`chinese_group` — so the societal value becomes inapplicable to CHI and the
setup line should be **deleted**, not re-signed. That is one more `FIELD_FIXES`
pair (delete `\n\t\t\tsinicized_vs_unsinicized = 50 # …`), and it removes the
line item 32 added rather than adding a second wrong one.

If §1 is refused, the line is *valid* and merely inverted, and the fix is a
magnitude flip to a negative value. Both shapes are in open decision 2.

---

## 3. THE DALI / YUNNAN CORE — the world D3's LNG retirement made and no decision covered

### 3.1 What the build ships today, measured

`dali_area` and `yunnan_area` are the two areas of `south_china_region`
(`definitions.txt`: `south_china_region` → `haibei_hainan_area guangdong_area
liangjiang_area guangxi_area guizhou_area dali_area yunnan_area
south_china_coastline`). Together **139 ownable locations, 41 tags.**

| | mod | vanilla | changed by |
|---|---|---|---|
| `dali_area` 60 ownable | CDL 12, MMA 12, LJG 8, GYT 3, YAN 3, BZH 3, MHA 3, MGN 3, MHN 3, MLM 4, HQG 2, MHK 2, YNG 2 | **identical** | **nothing — item 32 never touched `dali_area`** |
| `yunnan_area` 79 ownable | **CDL 17**, CHH 8, GGX 5, YNJ 5, MGK 4, NGZ 4, LZI 3, GNN 3, NWU 3, WDG 3, + 19 more | LNG 17 in CDL's place | item 32's `_CHINA_GRANTS["CDL"]` (`build_setup.py:1470-1476`, 17 named locations) |

So CDL is **29** (12 + 17), independent, `rank_kingdom`, capital `taihe_dali`,
Duan Silian seated (`HISTORICAL_RULERS["CDL"] = ('cdl_duan_silian','1041.1.1',0)`),
`include = "far_east_asia_monarchy_no_coast"`, `court_language =
southern_mandarin_dialect`, `tolerated_cultures = { yi_culture }`, registry
`bai_culture` / `mahayana #Azhaliism`
(`VAN/in_game/setup/countries/east_asia.txt:2163`). Its ground is 58.6 % yi /
bimoism and 26.4 % bai / mahayana; `taihe_dali` itself is pure bai/mahayana with
a hui/sunni minority. **CDL is correct as it stands — a Bai dynasty over a Yi
majority, vanilla's own reading, and the PAA precedent.**

### 3.2 The residue: 46 orphaned leaf-tusi

Vanilla gave LNG 63 subjects — 62 `tusi` + CDL as a `vassal`
(`VAN/main_menu/setup/start/12_diplomacy.txt`). LNG went landless (item 32,
`CHINA_LANDLESS`, `build_setup.py:1419`), which killed all 63 ties in the
generic sweep. Sixteen were rescued by the jimi repoint to CHI
(`build_setup.py:7588-7610`, `_JIMI = BZH BZU GGX GNN LIN MHU PAN PDN QJG QYN
SDG SMG SZH TNZ YGS YNJ`, exact count 16) because their own 45 sub-ties were
erroring. **The remaining 46 were simply dropped and are now fully sovereign
micro-states.** Measured: all 46 still hold exactly their vanilla holdings; not
one has any overlord in the current build.

**They split cleanly along the 1066 political line:**

| side | tags | locations | areas |
|---|---|---|---|
| **Dali's world** (`dali_area` + `yunnan_area`) | **18** | **45** | dali 16 (GYT 3, HQG 2, LJG 8, YAN 3), yunnan 29 (AGN 1, JSI 1, LZI 3, MGK 4, MWO 2, NGZ 4, NLU 2, NNN 1, NYZ 2, RND 1, SPG 1, SZI 2, WDG 3, ZYI 2) |
| **the Song's jimi frontier** | **28** | **65** | chuannan 32 (CGZ 1, CLE 2, DCN 4, GNG 1, LLS 7, RNG 1, WNG 4, WSA 3, XLG 1, YJI 4, YNL 1, ZNX 3), guizhou 13 (DYN 2, LTU 1, PDG 1, SXI 9), wuling 9 (DWG 1, GLU 1, RGM 2, SGZ 1, TGY 1, TNP 1, ZGL 2), liangjiang 8 (TPG 5, ZNN 3), chuandong 3 (PCD 1, SZU 1, YYG 1) |

**This costs zero error lines today.** A sovereign micro-state logs nothing;
`government.cpp:3702` fires only on an *invalid subject type*. The residue is
historical and visual: **an internal inconsistency inside our own build.**
Sixteen hill lords on the Song's Sichuan-Guizhou margin are the Song's jimi
prefectures; twenty-eight of their neighbours on the same ground, of the same
cultures, are sovereign — for no reason except which row of vanilla's 1337
subject tree they happened to sit on.

All 46 pass `is_country_valid_for_tusi_subject`
(`VAN/in_game/common/scripted_triggers/country_triggers.txt:1266-1284`) on every
statically checkable clause: **none** is `chinese_group` (measured, all 46),
every capital is in `west_china_region` / `south_china_region` /
`east_china_region`, and the largest holding is 9 (`num_locations <= 15`). Two
(GYT, LJG) are `government_type = tribe`; 44 are monarchies. The rank clause
(`country_rank_level = 1` OR tribe) cannot be settled statically — no file
settles the derived-rank thresholds, the standing OWED check — but **vanilla
itself shipped all 46 as tusi at these exact sizes**, which is the strongest
evidence available.

### 3.3 Vanilla's own testimony about Dali: the Azhaliism sect, dated 821

`MOD/main_menu/setup/start/15_international_organizations.txt:979-995`
(= `VAN/…:1362-1378`, byte-identical):

```
add_international_organization = { #Azhaliism
	type = sect
	creation_date = 821.1.1
	icon = azhaliism
	members = { CDL YAN HQG }
	laws = { azhaliism_policy vajrayana_policy }
	variables = { sect_favor = 40  religion = religion:mahayana }
	provinces = { dali_province }
}
```

**Vanilla names Dali's religious community and it is exactly three tags: CDL,
YAN and HQG** — and exactly the three `bai_culture` / `mahayana` tags in the
whole theater. `creation_date = 821.1.1` is pre-`START_DATE`, so the instance
survives our strip: the creation-date law again, this time confirming rather
than deleting. This is the only vanilla statement anywhere about which
neighbours belong to Dali, and it should carry more weight than any external
source.

Geography agrees: `heqing_province` is **2/2 HQG** (`heqing`, `jianchuan`) and
`yaoan_province` is **3/3 YAN** (`yaozhou`, `dayao`, `juque`) — two clean
single-owner provinces immediately north and east of `dali_province`, which is
**8/8 CDL**. Yaozhou and Heqing were *fu* of the Dali kingdom, not separate
states [U].

### 3.4 The Song–Dali seam, and the trap in it

`lijiang_province` is **LJG 3 / GYT 3**. GYT "Gyelthang" is `khampa_culture` /
`tibetan_buddhism` and is a **named, protected seam** — `TIBET-PACKAGE.md`
§D.6, "the measured seams — named, not touched". GYT holds **only** those 3, so
any rule that sweeps `lijiang_province` empties GYT entirely. The
emptied-but-unlisted delta guard (`build_setup.py:6420-6441`) *would* fire —
but a designer who "fixes" that by adding GYT to `LANDLESS_AFTER` would
silently delete the Tibet slice's decision. **Name GYT explicitly in any rule's
minus list; never sweep `lijiang_province`.**

`lanzhou_province` is LJG 5 / CDL 1 — a mixed province, same warning.

### 3.5 Mechanism constraints on any Dali ring — settled before the options

- **CDL can never have `tusi` subjects.** `can_country_have_tusi`
  (`country_triggers.txt:1286-1303`) is evaluated on the *overlord*. Branch 1
  needs MK leadership (CHI has it, CDL cannot). Branch 2 needs the overlord to
  itself be someone's `tusi` (CDL is nobody's subject and must not become one —
  §3.6 refuses it). Branch 3 needs `is_subject_of = middle_kingdom.leader_country`
  plus `overlord ?= { culture ?= prev.culture }`. **All three fail. `tusi` is
  off the table for Dali.**
- **CDL as a `tusi` of CHI is additionally illegal on size.**
  `is_country_valid_for_tusi_subject` caps a tusi at `num_locations <= 15`
  (`:1283`); CDL holds 29.
- **`tributary` is the only mechanism, and it needs a gate.**
  `VAN/in_game/common/subject_types/tributary.txt:9-25` — the four-branch OR is
  overlord-is-a-horde / **subject-is-a-tribe** / subject-is-a-horde /
  `modifier:allow_tributary_subject = yes`. Of the 18 Yunnan-world orphans,
  **2 are tribes** (GYT, LJG — free, the Irish law) and **16 are monarchies**
  (`south_east_asia_monarchy_no_mandala_no_coast` and siblings — the
  `_no_mandala` variants carry no `reforms` block at all).
- **`mandala_system` cannot pay Dali's gate.** Its `potential`
  (`country_specific.txt:3894-3899`) is `capital.sub_continent =
  sub_continent:south_east_asia`; `taihe_dali` is `east_asia`. So a ring over
  the sixteen monarchies needs an **authored** `dali_*_reform` — gate pattern
  #6 after the five khutba-family reforms, the tribe branch, and vanilla's
  `mandala_system`. The rank clause is satisfied: CDL is `rank_kingdom` and
  every candidate subject has no explicit rank.
- **No double overlords anywhere below.** Every tag named in every option holds
  **zero** dependencies today (verified against the mod's 261 live `dependency`
  lines, comment-masked). Nothing proposed here gives any tag a second overlord,
  and nothing repoints a tie that already exists.

### 3.6 DONOR TABLES — every proposed rule and every costed alternative

**This is the section `KNOWLEDGE.md`'s delta-guard law demands, and the main
session is asked to reproduce it before implementing.** Its reason binds hard
here: `lijiang_province` and `lanzhou_province` both have surviving donors, so
for any sweep touching them **the exact-count assert is the only line of
defence.**

---

**RULE 1 (recommended) — `_CHINA2_RULES["CDL"] = (["heqing_province", "yaoan_province"], [], [], [], 5)`**

| donor | loses | of | locations | `define_pop` | survives? |
|---|---|---|---|---|---|
| **HQG "Heqing"** | **2** | **2** | `heqing jianchuan` | 6 | **NO — emptied. Needs `LANDLESS_AFTER`; the delta guard is what catches an omission** |
| **YAN "Yaozhou"** | **3** | **3** | `yaozhou dayao juque` | 12 | **NO — emptied. Needs `LANDLESS_AFTER`** |
| **total** | **5** | | | **18** | |

Raw resolve of the two provinces is **5**; the intersection with current
ownership is also **5** (both provinces are single-owner — no protected donor
inside either). Every one of the five carries **exactly one** ownership entry
(re-measured with the ten-key reader), so `_remove_owned_many`'s `!= 1` exit
(`build_setup.py:5822`) will not fire. **CDL 29 → 34.**

*IO consequence, stated because the pinned-9 rule demands it:* the Azhaliism
sect goes **3 members → 1** (CDL) through the generic ghost sweep
(`build_setup.py:7029-7057`). It does **not** empty, so the pinned empty-list
count stays at **9** and `verify_mod.py:916` does not move. IO ghosts **156 →
158**.

*Culture consequence:* both donors are `bai_culture`, CDL's own primary — the
absorption adds no accepted/tolerated pressure. `tolerated_cultures = { yi_culture }`
already covers the Yi pops arriving with `yaoan_province`.

---

**Alt 1 — RULE 1 plus a CDL tributary ring over the sixteen remaining
Yunnan-world orphans (open decision 4c).** No territory moves; this is
diplomacy only, so there is no donor table in the territorial sense — but the
gate cost is real:

| subject | gov | passes the gate how |
|---|---|---|
| LJG (8, Naxi/Lijiang) | **tribe** | free — `tributary.txt:21`, the Irish law |
| AGN JSI LZI MGK MWO NGZ NLU NNN NYZ RND SPG SZI WDG ZYI (14, 29 loc) | monarchy | **only** via an authored `dali_*_reform` on CDL carrying `allow_tributary_subject = yes` |
| **GYT (3)** | tribe | **EXCLUDED — the Tibet package's protected Kham seam (§3.4)** |

Cost: one reform block in `in_game/common/government_reforms/zz_1066_reforms.txt`
(the `liao_ordo_reform` shape, `:188-200`), two loc rows (name + `_desc`, swept
by the harness), one `reforms = { }` line on CDL, and fifteen new `dependency`
lines. Harness: the tributary-gate check moves **78 → 93** (`verify_mod.py:843`).
The historical anchor is the "Thirty-seven Tribes" (三十七部) of eastern Yunnan,
Dali's confederated Yi vassals [U] — which is exactly the set: 10 of the 14
monarchies are `yi_culture`.

---

**Alt 2 — CDL absorbs the whole Yunnan world (139) — REFUSED, costed for
completeness.** Donor table would run to 40 tags, 18 of them emptied, and it
would delete the tusi/tribal texture that is the theater's most distinctive
feature — the SEA and Tibet slices' repeated finding that vanilla's micro-tag
patchwork *is* the 1066 picture. It would also strip CHI of 31 tusi (its own
subjects sit inside `yunnan_area`) and reopen the class item 32 spent a whole
grand-test fix closing.

---

**Alt 3 — the Song jimi completion (open decision 3), diplomacy only.** Repoint
the **28** non-Yunnan orphans to CHI as `tusi`, in the exact shape of the
existing jimi block (`build_setup.py:7588-7610`) but as *additions* rather than
repoints, since the LNG lines no longer exist to rewrite. Zero territory. CHI's
tusi count **31 → 59**; total tusi **76 → 104**. Gate: branch 1
(`is_leader_of_international_organization`), already proven live for CHI's 31 in
the 2026-08-01 grand test. Every one of the 28 passes the statically checkable
clauses of `is_country_valid_for_tusi_subject` (§3.2).

---

## 4. The other genuine leftovers

### 4.1 QUN — the last tag on the shatter-watch

`INDIA-CHINA-REVIEW.md` §5.2/7 said "retire it with the India pass". Item 34
did not. QUN is not in `LANDLESS_AFTER` and holds **6**:

```
MOD/main_menu/setup/start/10_countries.txt   QUN = { #Qara'unas
	type = army
	…	include = "eurasian_horde_no_coast_no_pleading"
	government = { type = steppe_horde  …  reforms = { legacy_of_genghis } }
	capital = kulob
```

A `type = army` **steppe horde** running `legacy_of_genghis` in 1066 — the same
class as the eight Chinggisid hordes item 32 retired, missed because it sits in
Badakhshan rather than Mongolia. The decoder's
`initialize_from_bookmark.cpp:2477` entry named HLG/QUN/SLD; HLG and SLD were
retired by the Arabia and Central Asia slices and the item-30 test recorded
":2477 down to **QUN alone**". **Retiring QUN closes an error class outright.**

Its six sit in three clean province neighbourhoods:

**RULE Q — three grants, six locations, zero vacates (recommended shape):**

| rule | donor | loses | of | locations | pops | survives? |
|---|---|---|---|---|---|---|
| `BKH += ["araska"]` | **QUN** | 1 | 6 | `araska` | 2 | — |
| `KTT += ["kulob","munk"]` | **QUN** | 2 | 6 | `kulob munk` | 4 | — |
| `GHZ += kafiristan (3)` | **QUN** | 3 | 6 | `parun asadabad_kunar hajiabad` | 6 | — |
| **total** | **QUN** | **6** | **6** | | **12** | **NO — emptied; `LANDLESS_AFTER`** |

Measured intersections: `badakhshan_province` is BKH 4 / QUN 1 — BKH is the
obvious and adjacent taker, and it **survives**, so only the count assert guards
that rule. `kulab_province` is KTT 4 / QUN 2 — same. `kafiristan` is **QUN 3/3**,
a whole single-owner province.

**Alt Q — vacate `kafiristan` instead of granting it** (the Pecheneg
discipline). Kafiristan/Nuristan was unconquered pagan hill country until 1896
[U], and vanilla's own pops there are `nuristani_culture` / `pashayi_culture`
`slaves` under `hindu` (vanilla's stand-in for Nuristani paganism) plus a token
`mongolian_culture` clergy pop — the Qara'unas garrison stamp. Cost: 3 locations
vacated, **625 → 628**, and ~6 lines of the known vacated-pop class. `BKH`/`KTT`
still take the other three.

*Note on the horde guard:* `_bad_recip` (`build_setup.py:6158-6160`) forbids a
steppe horde as a **recipient**. QUN is a donor here, so the guard is not
reached; BKH, KTT and GHZ are all monarchies.

### 4.2 The Middle Kingdom's member list is still vanilla's 1337 tianxia

198 members (vanilla 209 minus the 11 our landless sweep took: BAT BGT CRS HCN
KHD LNG OGE OTC QAS SYG TIB). **All 41 Yunnan-world tags are members, CDL
included.** Nine members hold zero land — DUR EVK NVK ORC ORQ SIB TVA UDE ULC —
and all nine are `type = pop`, i.e. legitimately landless under the harness's
own exemption (`verify_mod.py:874-880`). **No ghost. No error. Nothing to fix
mechanically.**

The open question is design: whether a **sovereign Dali** should be inside the
Song's tianxia at all. Vanilla's rationale is a Yuan one. Dali did receive Song
investiture — but as "King of Yunnan" in **1117**, fifty-one years after start,
after decades in which the Song rebuffed its embassies [D]. Membership is not
cosmetic: `middle_kingdom.txt`'s member modifiers apply
`monthly_towards_sinicized` to every member and `block_from_change_to_empire_rank`
to every non-leader. **Open decision 7.**

### 4.3 The harness's weakest floor sits on the file this slice edits

`verify_mod.py:884` — `check("IO members hold land", _members_checked, probs,
min_count=27)`. It scans **854** items. A 31× gap, and the lowest ratio in the
harness (every other content floor was raised with its slice: loc 375, thrones
358, bijection 2414, parliament 1363, CoA 125, gate 78, IO instances 36). If a
regex change or a rewritten `15_international_organizations.txt` ever reduced
the member sweep to a handful, this check would pass green. **`CLAUDE.md`:
"Raise `min_count` as content lands."** Any change in §3-§4 touches that file;
the floor should move in the same commit.

### 4.4 Two cosmetics, recorded and not recommended

- CHI's generated block still opens `CHI = { #Yuán` — vanilla's comment,
  carried through by the whole-file copy. Invisible in game (it is a comment in
  a generated file). Fixing it means a `FIELD_FIXES` pair for a comment; not
  worth a build assert.
- `YUA` is a live registered identity (`MOD/…/east_asia.txt:1163`,
  `mongolian_culture`/`tibetan_buddhism`) with a formable `YUA_f`
  (`00_formable_countries.txt:4953-4964`). **Correct and desirable at 1066** —
  the Yuan as a future the Mongols may earn. Leave it; and note it is the
  reason §1's fix must touch `:1156-1157` and **not** `:1166-1167`.

---

## 5. EXCLUDED seams — measured, named, not redesigned

Everything below was closed by items 30/32/33/34/38 and is reported only so the
main session can confirm the audit reproduced it.

| seam | measured state | closed by |
|---|---|---|
| **XIA** | 48 locations, `rank_empire`, Yizong seated, `mi_niah_culture`/`mahayana`; holds `north_china_region` 7 + `west_china_region` 41 | item 33 |
| **LIA** | **310** — `mongolia_region` 149, `north_china_region` 113, `manchuria_region` 48; `dadu` is **LIA's** (the Sixteen Prefectures, correct for 1066); capital `linhuang`; `liao_ordo_reform`; `rank_empire` | item 33 |
| **the Jurchen ring** | 46 `LIA → tribe` tributaries (`build_setup.py:7575-7586`, exact count 46), all `government_type = tribe` → the free branch | item 33 |
| **TKA's xining** | `xining` is TKA's; CHI no longer owns the Huangshui valley | item 38 |
| **the deep-plateau tusi** | CHI → HOR/NYA/GOL/AMD stripped, exact count 4 (`build_setup.py:7730-7748`); the fourteen rim ties kept | item 38 |
| **KHM / DAI / CHA** | KHM 104 (82 + SEA's 24 Khorat), DAI 53, CHA 21; `CHI → CHA` and `CHI → DAI` **tributary** live (`12_diplomacy.txt`), CHI's gate paid by the MK leader_modifier | items 30/32/37 |
| **the India nine** | VIJ MAB SMA RDY RCH JFN SMV MSN all at **0**; DLH at **0**; DBD survives as Ruhuna | item 34 |
| **the jimi sixteen** | BZH BZU GGX GNN LIN MHU PAN PDN QJG QYN SDG SMG SZH TNZ YGS YNJ → CHI `tusi`, 71 locations, their 45 sub-ties alive | item 32's grand-test fix |
| **western Mongolia** | 64 unowned (`mongolian_great_lakes_area` 21, `western_gobi_area` 32, `tuva_area` 11) | item 33, Pecheneg discipline |
| **the Amur** | 112 unowned in `manchuria_region` (`middle_amur_area` 50, `lower_amur_area` 42, `songnen_area` 12, `songhua_area` 4, `ussuri_area` 4) | items 32-33. *Note for the test tour: item 33's line "Manchuria mostly Liao" is imprecise — Liao holds 48 there, the Amur basin is empty and the Jurchen fringe holds ~63* |

---

## I. Mechanism — every tool exists; this package needs no new build step

| need | existing mechanism | `file:line` |
|---|---|---|
| region/area/province → locations | `_parse_defs` + `_ownable_set` + `_defs` | `:748`, `:772`, `:809` |
| rule-set resolution | `_resolve_ruleset` | `:815`; consuming-loop models `:5991` (Africa), `:6013` (SEA), `:6031` (Tibet) |
| grant by province sweep | a `_CHINA2_RULES` 5-tuple → `LOCATION_GRANTS` extend (CDL is a landed recipient) | declare `:3041`; loop model `:6031-6045` |
| exactly-one-owner on every grant | `_remove_owned_many` | `:5817`, exit `:5822` |
| grant-list disjointness | `_list_owner` | `:6167-6173` |
| steppe-horde recipient guard | `_bad_recip` — CDL/BKH/KTT/GHZ are monarchies; not reached | `:6146-6160` |
| retire with auto-derived claims | `LANDLESS_AFTER` + `_landless_claims` | `:3024`, `:6218` |
| prove the retiree really emptied | the `LANDLESS_AFTER … still owns` guard | `:6381` |
| prove the retiree carries claims | the claimless-shell guard | `:6399-6402` |
| catch a side-effect retirement | the emptied-but-unlisted delta guard | `:6420-6441` |
| **registry surgery (culture/religion)** | direct edit of the EXISTING whole-file override — the Gallura / ARA / PUR / Makuria route | `MOD/in_game/setup/countries/east_asia.txt:1156-1157` |
| **field surgery on a country block** | `FIELD_FIXES`, exact-once asserted | declare `:3158`; apply `:6497+`; CHI's existing entry `:3428-3457` |
| capital correction | `CAPITAL_FIXES` | `:3079`; apply `:6478-6494` — **not used** |
| **named dependency add / repoint** | the jimi block's `re.subn` + exact-count shape | `:7588-7610`; Jurchen twin `:7575-7586` |
| dependency dissolution by landlessness | `_drop_landless_dep` | `:7802-7811` |
| IO member strip (ghosts) | `build_ios`'s generic `LANDLESS_AFTER` sweep | `:7029-7057` |
| the future-dated IO strip (already ran) | `creation_date >= START_DATE` | assert `:7219` (`removed != 17`) |
| `LOCATION_VACATED` + `_EXPECT` | resolve + assert | `:1265`, `:1273`; `:6309-6329` — **only under Alt Q** |
| `UNOWNED_GRANTS` | — | `:1934` — **not used, and must not be**: every location named here has exactly one owner, re-proven with the ten-key reader |
| `CONTROL_STRIPS` | — | `:1720` — **no key needed**: zero double-ownership across all 139 Yunnan-world locations and all 6 of QUN's |
| new tags / colours / CoA / loc rows | `NEW_COUNTRIES`, `_assert_new_block_discovery` | `:502`, `:5693` — **not used: this package proposes ZERO new tags** |
| `HISTORICAL_RULERS` / `NEW_CHARACTERS` | — | `:69`, `:3702` — **not used: zero new rulers, zero new dynasties** |
| an authored gate reform | `zz_1066_reforms.txt`, the `liao_ordo_reform` shape | `:188-200` — **only under Alt 1 (decision 4c)** |

**Asserts that will fire if the design is wrong, and must be watched:**

1. **`_CHINA2_RULES["CDL"]` resolved count** — must be **5**. A vanilla patch
   that moves a location into `heqing_province` or `yaoan_province` fails here,
   loudly, as intended.
2. **`_remove_owned_many != 1`** (`:5822`) — fires if any of the five has two
   ownership entries or zero. Measured at exactly one each.
3. **the emptied-but-unlisted delta guard** (`:6420-6441`) — must stay silent
   once HQG and YAN are in `LANDLESS_AFTER`. **Honest caveat: it cannot protect
   GYT under a `lijiang_province` sweep in the way a designer would expect** —
   it *would* fire (GYT holds nothing else), and the wrong "fix" is to list GYT.
   §3.4. The donor table above is the real guard.
4. **`FIELD_FIXES` exact-once** — `zhongyuan_culture` must appear exactly once
   inside CHI's `accepted_cultures`, and the `sinicized_vs_unsinicized = 50`
   line exactly once. Both measured at one.
5. **the landless-dep strip count** — moves with every retirement below;
   observe it failing before moving the constant (the house rule).

---

## OPEN DECISIONS

---

**1 — CHI's registry identity: does the Northern Song stop being Mongolian and Tibetan Buddhist?**

- **Recommend: YES, both lines, plus the accepted-list cure.** Edit the two
  lines already inside our own override — `MOD/in_game/setup/countries/
  east_asia.txt:1156-1157`, `mongolian_culture → zhongyuan_culture` and
  `tibetan_buddhism → sanjiao` — and add one `FIELD_FIXES` pair on CHI dropping
  `zhongyuan_culture` from `accepted_cultures`. Vanilla's own `CSO` block
  (`VAN/…east_asia.txt:1172-1173`) prescribes exactly this pair; the capital's
  own pops are 100 % `zhongyuan_culture`/`sanjiao`; CHI's whole territory is
  96.1 % sanjiao and 0.0002 % mongolian. The render is proven safe (§1.5) and
  the change costs **three lines and no new mechanism** — the cheapest
  high-impact correction left on the map.
- **Cost:** 0 locations, 0 tags, 0 characters, 0 new mechanisms. Registry 74
  unchanged. Accepted cultures 9 → 8.
- **Honest counter:** the **religion** half has the widest blast radius of
  anything in this package and no static check can predict it. CHI leaves a
  `max_sects = 1` religion for a `max_sects = 3` one; conversion pressure,
  stability, tolerance and every religion-gated CB and advance shift at once;
  and there is **no `sanjiao` sect instance in the game**, so CHI stays
  sect-less either way. The 96.1 % figure argues the *current* state is the
  risky one — a court whose religion 0.005 % of its subjects share — but "the
  religion the map already has" is not the same claim as "the religion the
  engine will behave well with".
- **Split fallback if that counter bites:** take `culture_definition` alone
  (one line, the ARA law fully attested, blast radius understood) and bank the
  religion line for the same launch's observation.

---

**2 — The sinicization slider.**

- **Recommend: DELETE the line.** If decision 1 lands, CHI's primary is
  `chinese_group` and `sinicized_vs_unsinicized`'s `allow` (`00_default.txt:391`)
  refuses the value outright — keeping a number there is keeping a line the
  engine will not read. One `FIELD_FIXES` pair removing what item 32 added.
- **Cost:** one line.
- **Honest counter, and the branch if decision 1 is refused:** the line is then
  *live* and *inverted* — `+50` is 100 points unsinicized of vanilla's own Yuán
  and 120 of its Chinese-monarchy template. In that world the fix is a
  magnitude flip to **−70** (`far_east_asia_monarchy.txt:26`, vanilla's own
  figure for China, and the "restate vanilla's number, do not re-derive it"
  lesson from the `cultures_capacity = 50` argument). Either way the current
  value is wrong; only the shape of the fix depends on decision 1.

---

**3 — The 28 Song-side orphans: jimi repoint, or leave sovereign?**

- **Recommend: repoint to CHI as `tusi`** (Alt 3, §3.6). It removes an
  inconsistency **we created**: sixteen hill lords of the same cultures on the
  same ground are already CHI's jimi and twenty-eight are not, for no reason
  except which row of vanilla's Yuan subject tree they occupied. The mechanism
  is proven live (branch 1, measured in the 2026-08-01 grand test), needs no
  reform and no territory, and every candidate passes the statically checkable
  clauses of `is_country_valid_for_tusi_subject`.
- **Cost:** 0 locations, 0 characters. 28 `dependency` lines; CHI's tusi 31 →
  59, total tusi 76 → 104.
- **Honest counter:** the exact roster of Song jimi prefectures at 1066 is
  `[U]` — the 46 are the *Yuan's* Liang appanage tree, and we would be reusing
  a 14th-century administrative map as an 11th-century one. It also makes the
  Song look administratively deeper than it was, and 28 more subject arrows on
  the Guizhou-Sichuan map is visual clutter. **The coherent opposite — leave all
  46 sovereign and undo the sixteen — is NOT available**: that repoint exists
  because its absence produced 45 measured `government.cpp:3702` lines.
  A middle option exists and is defensible: repoint only the **12
  chuannan_area** tags (Sichuan's Yi/Bo margin, the best-attested jimi
  frontier [U]) and leave Guizhou/Wuling/Liangjiang's 16 sovereign.

---

**4 — Dali's Yunnan orbit.**

- **Recommend: 4b — RULE 1 alone.** CDL absorbs `heqing_province` (HQG 2) and
  `yaoan_province` (YAN 3) → **CDL 34**; HQG and YAN retire landless with
  auto-derived claims. The evidence is vanilla's own Azhaliism sect
  (`creation_date = 821.1.1`, members exactly `CDL YAN HQG`), reinforced by
  both provinces being clean single-owner blocks of Dali's own `bai_culture`
  immediately adjacent to `dali_province`. Zero new mechanisms, zero new tags,
  zero new characters, no reform, no gate.
- **Cost:** 5 locations, 2 tags retired, 0 characters. Landless-dep strips
  unchanged (neither tag has ties). IO ghosts 156 → 158, Azhaliism 3 → 1
  members, empty-list count stays at 9.
- **Honest counter:** it is a *shrinking* move for the map's tag diversity, and
  the SEA/Tibet/Americas slices' repeated lesson is that vanilla's micro-tag
  patchwork usually IS the 1066 picture. Two more grey names vanish from
  Yunnan for five locations.
- **4a — do nothing.** Fully defensible: CDL at 29 with a seated Duan Silian is
  already a correct sovereign Dali, and the 18 sovereign neighbours cost zero
  error lines. If the user wants the map phase closed at minimum risk, 4a plus
  decisions 1-2 is a complete answer.
- **4c — 4b plus the tributary ring** over LJG (free, tribe) and the fourteen
  Yi/Tai monarchies, GYT excluded. This is the only option in the package
  needing a new authored reform and two new loc rows; gate check 78 → 93. It
  buys the Thirty-seven Tribes [U], the single most characteristic feature of
  the Dali polity — and it is the option to take if the user wants Yunnan to
  *look* like a kingdom rather than a scatter.
- **4d — full absorption. Refused** (§3.6 Alt 2).

---

**5 — `celestial_governor = { KOR }`: keep item 32's divergence, or take the review's prescription?**

- **Recommend: KEEP.** It is a recorded, reasoned divergence and it is the only
  thing left tying Goryeo to the Chinese world after item 32 stripped the
  vassalage. Removing it would leave KOR with no relationship to anyone.
- **Cost of keeping:** zero.
- **Honest counter, which is strong:** at 1066 Goryeo was a **Liao** tributary,
  and Song–Goryeo relations were suspended from 1022 until **1071** [D] — five
  years after start. `num_of_celestial_governors = 1` is therefore asserting a
  tie that history says was in abeyance on the exact day the game begins. The
  alternative is the review's §1.4/4 in full — delete
  `celestial_governor = { KOR }` and set `num_of_celestial_governors = 0` — and
  optionally add **`LIA → KOR tributary`**, which is legal and gate-clean: KOR
  holds **zero** dependencies today (no double overlord), LIA is `rank_empire`
  against KOR's `rank_kingdom` (the rank clause passes), and LIA already carries
  `liao_ordo_reform`'s `allow_tributary_subject`
  (`zz_1066_reforms.txt:188-200`), so the gate is paid — gate check 78 → 79.
  This is the historically strongest single line in the package and the one the
  agent would take if only one of decisions 3-5 could be taken.

---

**6 — QUN, the last tag on the shatter-watch.**

- **Recommend: retire it** — RULE Q's three grants (BKH 1, KTT 2, GHZ 3) plus
  `LANDLESS_AFTER`. It is a `type = army` steppe horde running
  `legacy_of_genghis` in Badakhshan in 1066, it is the review's own §5.2/7 that
  no item landed, and it is the **sole remaining producer** of
  `initialize_from_bookmark.cpp:2477` — retiring it closes a decoder class
  outright rather than shrinking it.
- **Cost:** 6 locations, 1 tag, 0 characters. Landless-dep strips: QUN holds no
  dependencies, so no strip. Claims auto-derived from its pre-sweep holdings.
- **Honest counter:** `GHZ += kafiristan` puts the Ghaznavids into Nuristan,
  which they raided but never held [U] — the Kafirs were still pagan in 1896.
  **Alt Q vacates those three instead** (vacated 625 → 628, ~6 lines of the
  known pop class), which is the more honest map and matches the Pecheneg
  discipline this project has applied five times. The agent's preference is
  **Alt Q**; the recommendation above is written the other way because vacating
  settled land is the more expensive habit and the user has consistently been
  asked before each one.

---

**7 — Should a sovereign Dali sit inside the Middle Kingdom?**

- **Recommend: LEAVE CDL in.** It is vanilla's own member list, membership is
  not a dependency (Dali stays fully sovereign on the map and in the subject
  panel), and the alternative costs an exact-count member surgery for a
  cosmetic gain.
- **Cost of leaving:** zero.
- **Honest counter:** the tianxia membership applies real modifiers —
  `monthly_towards_sinicized` to every member, `block_from_change_to_empire_rank`
  to every non-leader — and Dali's Song investiture is **1117**, fifty-one years
  after start, after decades of rebuffed embassies [D]. If decision 4c lands
  (Dali as a real overlord), a Dali that cannot rise past kingdom rank because
  of a Yuan-era member list is a design contradiction worth removing. This
  would be a one-token strip in the same `build_ios` surgery that already
  re-dates the instance.

---

**8 — Raise the harness's weakest floor.**

- **Recommend: `verify_mod.py:884`, `min_count=27 → 850`.** It scans 854. Every
  other content floor was raised with its slice. Any decision above touches
  `15_international_organizations.txt`; this belongs in the same commit.
- **Cost:** one integer. **Counter:** none. Prove it by breaking (drop the
  member sweep's regex to `members` in one file, watch the vacuous-scan floor
  fail, restore).

---

## Implementation checklist

Ordered so each step is observable before the next. Every constant is
**observed failing first**, then moved — the house rule.

1. **Decision 1, culture.** Edit `MOD/in_game/setup/countries/east_asia.txt:1156`
   `mongolian_culture → zhongyuan_culture`. **Touch `:1156` only — `:1166` is
   YUA's identical line and must not move.** File keeps its BOM (it is
   `in_game/`, not `setup/start/`); diff the whole file against vanilla
   afterwards and confirm exactly **three** intended deltas (the header block,
   CHI's colour, PUR's religion) plus the new one.
2. **Decision 1, religion.** Same block, `:1157`
   `tibetan_buddhism → sanjiao`. Extend the override's header comment: it
   currently says "EXACTLY TWO intended changes" and will be stale.
3. **Decision 1, the ARA cure.** `FIELD_FIXES["CHI"]` += `("\n\t\t\tzhongyuan_culture", "")`.
   Break-test: point it at a culture not in the list, confirm the exact-once
   assert exits.
4. **Decision 2.** `FIELD_FIXES["CHI"]` += a pair deleting
   `sinicized_vs_unsinicized = 50 # …` (match the full generated string,
   `build_setup.py:3456-3457`).
5. **Decision 4b.** Add `_CHINA2_RULES = {"CDL": (["heqing_province",
   "yaoan_province"], [], [], [], 5)}` next to `_CHINA_GRANTS`
   (`build_setup.py:1470`), consumed by the Tibet-shaped loop (`:6031-6045`).
   Add `CHINA2_LANDLESS = ("HQG", "YAN")` into `LANDLESS_AFTER` (`:3024`).
   **Break-test (a):** drop HQG from the landless tuple → the
   emptied-but-unlisted delta guard (`:6420-6441`) must exit.
   **Break-test (b):** change the expected count 5 → 6 → the rule's count assert
   must exit.
   **Break-test (c):** swap `yaoan_province` for `lijiang_province` → the guard
   must name **GYT**, proving §3.4's trap is live; restore.
6. **Decision 6 (or Alt Q).** `_QUN_RULES` for BKH/KTT/GHZ (or
   `LOCATION_VACATED["kafiristan"]` equivalent + two grants), `QUN` into
   `LANDLESS_AFTER`. **Break-test (d):** omit QUN from `LANDLESS_AFTER` → the
   delta guard exits.
7. **Decision 3 and/or 5, diplomacy.** New named-add blocks in
   `build_diplomacy` modelled on `:7588-7610`, each with an exact count
   (28, or 12; and 1 for `LIA → KOR`). **Break-test (e):** misspell one tag →
   the count assert exits.
8. **Decision 5 alternative, IO surgery.** If taken: strip
   `celestial_governor = { KOR }` and set `num_of_celestial_governors = 0`
   inside the existing `build_ios` Middle Kingdom block (`:6873-6881`), each
   with an exact-count `re.subn`.
9. **Decision 4c, only if taken.** `dali_*_reform` in
   `zz_1066_reforms.txt` (the `:188-200` shape, `government_reform_slots = 1`
   per the house rule), two loc rows, `reforms = { }` on CDL, fifteen
   `dependency` lines. **Break-test (f):** remove the reform → the
   tributary-gate check must flag all fourteen monarchy ties (the tribe LJG
   must NOT be flagged — that is the branch-2 proof).
10. **Decision 8.** `verify_mod.py:884` `min_count=27 → 850`, proven by
    breaking.
11. `python tools/build_setup.py --dry-run`, then
    `python tools/verify_mod.py`. Move every constant only after observing its
    old value fail.
12. Commit as a pair: the slice, then the HANDOFF item + Turkish click tour.

---

## Expected constant moves, collected

From HEAD `0a39b5f`'s constants (registry 74, country blocks 2411, thrones 179,
landless-dep strips 281, pacts 9, IO ghosts 156, vacated 625, parliament min
1363, loc rows 375, CoA 125).

| constant | now | after decisions 1+2+4b+6 (recommended core) | if 3 taken | if 4c taken | if 5-alt taken |
|---|---|---|---|---|---|
| registry blocks (`zz_1066_new_countries.txt`) | 74 | **74** — zero new tags | 74 | 74 | 74 |
| country blocks | 2411 | **2411** — nothing created or deleted | 2411 | 2411 | 2411 |
| thrones (`HISTORICAL_RULERS`) | 179 | **179** — zero new rulers | 179 | 179 | 179 |
| `LANDLESS_AFTER` members | 315 | **318** (HQG, YAN, QUN) | 318 | 318 | 318 |
| landless-dep strips | 281 | **281** — none of the three retirees holds a dependency | 281 | 281 | 281 |
| live dependencies | 261 | 261 | **289** (+28) or **273** (+12) | **304** (+15 on top) | **+1** (`LIA → KOR`) |
| tributary-gate check items | 78 | 78 | 78 (`tusi` is not gated by that check) | **93** | **79** |
| IO ghosts | 156 | **158** (HQG, YAN leave Azhaliism) | 158 | 158 | 158 |
| empty IO member lists (pinned) | **9** | **9 — unchanged**; Azhaliism drops 3 → 1, it does not empty | 9 | 9 | 9 |
| MK members | 198 | 198 | 198 | 198 | 198 (the governor list is a separate key) |
| vacated | 625 | **625** under RULE Q; **628** under Alt Q | 625 | 625 | 625 |
| parliament min | 1363 | **1361** (HQG, YAN leave the landed set; QUN is a horde — confirm against the check's own definition before moving) | 1361 | 1361 | 1361 |
| loc rows | 375 | 375 | 375 | **377** (reform name + `_desc`) | 375 |
| CoA | 125 | 125 | 125 | 125 | 125 |
| `IO members hold land` floor | 27 | **850** (decision 8) | 850 | 850 | 850 |
| CHI accepted cultures | 9 | **8** | 8 | 8 | 8 |
| CDL holdings | 29 | **34** | 34 | 34 | 34 |
| QUN holdings | 6 | **0** | 0 | 0 | 0 |

**Error-log expectations.** `initialize_from_bookmark.cpp:2477` should go to
**zero** (QUN was the last). The landless-shell trim class grows by three tag
blocks (HQG, YAN, QUN — decoder sub-class 3, accepted). Under Alt Q the
vacated-pop class grows by ~6 lines. **No new class is predicted** — and that
prediction is itself the thing to check, because decision 1's religion half is
the one change in this package whose consequences no static analysis reaches.

---

## VERIFICATION

**Verified — mechanical, with source:**

- The ten-member `OWN_KEYS`, `build_setup.py:5790-5793`; reader logic
  `_owned_by` `:5828-5843`. Reproduced VTN 32, PLB 40, TIB 59, MUA 15, BTU 6,
  MGD 5, 2337/2411 country blocks, 625 vacated.
- The loose registry regex reproduces **2,340** vanilla identity blocks against
  the strict form's 2,246 — `KNOWLEDGE.md`, the Americas law, confirmed live.
- `CHI` registry, `MOD/in_game/setup/countries/east_asia.txt:1148-1157`,
  `color = map_CSO` at `:1149`, `culture_definition = mongolian_culture` at
  `:1156`, `religion_definition = tibetan_buddhism` at `:1157`. Vanilla's twin
  at `VAN/…:1139-1150`, `color = map_YUA`.
- `CSO` registry, `VAN/in_game/setup/countries/east_asia.txt:1169-1175`,
  "culture_definition = zhongyuan_culture", "religion_definition = sanjiao".
- `zhongyuan_culture` → `chinese_group confucian_group`,
  `VAN/in_game/common/cultures/east_asia.txt:257-270`; `mongolian_culture` →
  `mongolian_group steppe_group`, `:1112-1126`; `bai_culture` →
  `confucian_group tibeto_burman_group`, `:1281-1295`.
- `sinicized_vs_unsinicized`, `VAN/in_game/common/societal_values/
  00_default.txt:389-421`, `allow` line 391
  "NOT = { culture ?= { has_culture_group = culture_group:chinese_group } }",
  `left_modifier = { #Sinicized`, `right_modifier = { #Unsinicized`. Template
  values `far_east_asia_monarchy.txt:26` −70, `japanese_clan.txt:26` −50,
  `jianzhou_tribe.txt:19` −5, `asia_tribe.txt:20` +10, `haixi_tribe.txt:19`
  +25, `yeren_tribe.txt:19` +95.
- CHI's generated block, `MOD/main_menu/setup/start/10_countries.txt:26239-26509`:
  `sinicized_vs_unsinicized = 50` `:26413`, `reforms = { song_civil_service_reform
  three_departments_system }` `:26418-26421`, `ruler = chi_zhao_shu_yingzong`
  `:26422`, `capital = kaifeng` `:26501`, `flag = "CSO"` `:26503`,
  `country_name = "CSO"` `:26504`. Accepted 9 (`zhongyuan_culture` present),
  tolerated 61.
- `country_name_construction.txt:91-96` and
  `customizable_localization/country_ranks.txt:481-493` — both read court
  language / MK leadership, never culture. Loc:
  `government_names_l_english.yml:13, :95, :292`.
- `three_departments_system` `country_specific.txt:2140-2170`; `mandala_system`
  `:3894-3915` with `potential = { capital.sub_continent =
  sub_continent:south_east_asia }`; `malian_tribute_system` `:3917`.
- `tributary.txt:9-25` — the four-branch OR and the rank clause. `tusi.txt:6-11`.
  `country_triggers.txt:1266-1284` (`is_country_valid_for_tusi_subject`, incl.
  `num_locations <= 15` at `:1283`) and `:1286-1303` (`can_country_have_tusi`).
- `buddhist.txt` — `mahayana:24` `max_sects = 3`, `tibetan_buddhism:110`
  `max_sects = 1`, `sanjiao:133` `max_sects = 3`.
- Middle Kingdom instance, `MOD/main_menu/setup/start/
  15_international_organizations.txt:164`, `creation_date = 960.2.4`,
  `leader = CHI`, 198 members, `celestial_governor = { KOR }`,
  `num_of_celestial_governors = 1`. Re-date surgery `build_setup.py:6873-6881`.
  Vanilla twin `VAN/…:210-271`, 209 members.
- Azhaliism sect, `MOD/…:979-995` = `VAN/…:1362-1378`,
  `creation_date = 821.1.1`, `members = { CDL YAN HQG }`,
  `provinces = { dali_province }`. Sakya sect `VAN/…:1472`,
  `creation_date = 1073.1.1`, members include `CHI` — deleted by our strip.
- 17 vanilla IO instances stripped (assert `build_setup.py:7219`); 9 empty
  member lists pinned (`verify_mod.py:916`), vanilla ships 11.
- Ownership, current build: `dali_area` 60 / `yunnan_area` 79 ownable; CDL 29;
  the 46 orphan leaf-tusi hold 110 (45 in the two areas, 65 outside), each at
  its exact vanilla count, each with **zero** dependencies (261 live
  `dependency` lines, comment-masked, cross-checked).
- `heqing_province` 2/2 HQG; `yaoan_province` 3/3 YAN; `dali_province` 8/8 CDL;
  `lijiang_province` LJG 3 / **GYT 3**; `lanzhou_province` LJG 5 / CDL 1.
- QUN: `type = army`, `government type = steppe_horde`,
  `reforms = { legacy_of_genghis }`, capital `kulob`, holds
  `araska` (`badakhshan_province`, BKH 4 alongside), `kulob munk`
  (`kulab_province`, KTT 4 alongside), `parun asadabad_kunar hajiabad`
  (`kafiristan`, 3/3 QUN). No tag claims any of the six.
- Pops: 50,255 `define_pop` over 28,570 locations. CHI's 1,300 held locations
  96.1 % sanjiao / 0.005 % tibetan_buddhism, 7.5 % zhongyuan / 0.0002 %
  mongolian. `kaifeng` pops all `zhongyuan_culture`/`sanjiao` plus `qayfengi`/
  `judaism` and `hui_muslim_culture`/`sunni`. `taihe_dali` bai/mahayana plus
  hui/sunni. Kafiristan's three: `nuristani_culture`/`pashayi_culture` `slaves`
  under `hindu`, each with a `mongolian_culture` clergy pop.
- Harness at HEAD: all 33 checks green; `IO members hold land` scans **854**
  against `min_count=27` (`verify_mod.py:884`).

**Tag freeness — three scans each, run for the tags this package REFUSES as
much as for any it proposes.** Method per `AMERICAS-PACKAGE.md` §A.2:
(1) word-boundary `\bTAG\b` over the whole vanilla tree, non-localisation and
English-localisation counted separately; (2) substring `_TAG\b|\bTAG_` over the
same tree; (3) both over the whole mod repo. Text files only. **16,226 vanilla
files and 72 mod files scanned; registry read `utf-8-sig` over both
`in_game/setup/countries/` trees with the loose whitespace form.**

| candidate | VAN word | VAN en-loc | VAN sub | MOD word | MOD sub | registry | verdict |
|---|---|---|---|---|---|---|---|
| **DAL** (DALi) | 34 | 3 | 79 | 0 | 24 | **none** | **TAKEN, EMPTY REGISTRY — the PRU/MAY class.** `DAL: "Dalmatia"` (`country_names_l_english.yml:5056-5057`), a formable (`00_formable_countries.txt:4297-4300`, `name = DAL flag = DAL tag = DAL`) |
| **NZH** (NanZHao) | 32 | 1 | 50 | 38 | 18 | `VAN:russia.txt:267` | **TAKEN** — Nizhny Novgorod |
| **TAL** | 22 | 1 | 48 | 2 | 18 | `VAN:east_africa.txt:539` | **TAKEN** |
| **NAN** (NANzhao) | 15 | 1 | 41 | 4 | 12 | **none** | **TAKEN, EMPTY REGISTRY.** `NAN: "Nanai"` (`:3428-3429`) — a Tungusic pop identity |
| **DLI** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **AZH** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **GAO** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **ERH** | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| CDL / LNG / CSO / YUA | 27 / 80 / 45 / 45 | 1 / 1 / 2 / 17 | 50 / 20 / 57 / 182 | 26 / 42 / 22 / 17 | 19 / 7 / 31 / 34 | `MOD/east_asia.txt:2172 :2164 :1178 :1163` | **TAKEN, all registered — the tags this package discusses** |

**Vanilla ships exactly one Dali tag and it is CDL** (`CDL: "Dali"`,
`country_names_l_english.yml:3260-3261`; `map_CDL = rgb { 245 245 220 }`,
`named_colors/02_map.txt:2582`). There is no `NZH`/`DAL`-class second Dali or
Nanzhao identity anywhere. **This package proposes ZERO new tags**, so DLI/AZH/
GAO/ERH are recorded free and unused — scanned because the next slice that
reaches for an obvious Yunnan mnemonic must not have to re-derive it.

**`[U]` — the agent's own history, no source in the repo:**

- The Dali kingdom exists 937-1253 under the Duan; Duan Silian reigns from
  1041 (already seated by item 32, so this is inherited, not new).
- Yaozhou and Heqing were administrative *fu* of the Dali kingdom rather than
  independent states.
- The "Thirty-seven Tribes" (三十七部) of eastern Yunnan were Dali's
  confederated Yi vassals.
- The Song's *jimi* (羈縻, loose-rein) prefecture system covered the Sichuan,
  Guizhou, western Hunan and Guangxi hill peoples at 1066; its exact 1066
  roster is not recoverable from any file.
- The Jianzhou Jurchen were the most and the Yeren the least sinicized of the
  three Jurchen groups (used only to read vanilla's own slider signs, which are
  themselves the evidence).
- Kafiristan/Nuristan remained unconquered and pagan far past 1066; the
  Ghaznavids raided but did not hold it.
- Lijiang's Naxi and Gyelthang's Khampa sat on opposite sides of the
  Dali/Tibetan cultural line.

**`[D]` — sources genuinely differ:**

- Goryeo's 1066 alignment. It was a Liao tributary and its Song relations were
  suspended c. 1022-1071; whether the tianxia seat is defensible on the start
  date is exactly the disagreement decision 5 records.
- Dali's Song investiture. The "King of Yunnan" title is 1117; whether the
  relationship before it counts as tributary membership is disputed, and
  decision 7 turns on it.

**Not verified, and stated as such:** the derived `country_rank_level` of every
tag in §3 without an explicit `country_rank` line. No file settles the
thresholds — the standing OWED in-game check from the SEA, Tibet and
Perm/Vyatka slices. It affects `is_country_valid_for_tusi_subject`'s first
clause (decision 3) and `tributary.txt`'s rank clause (decision 4c). The only
available evidence is that **vanilla itself shipped all 46 as `tusi` and all 41
Yunnan tags at these exact sizes**, which is strong but is not a file that says
so.
