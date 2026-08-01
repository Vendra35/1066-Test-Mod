# THE NORTHERN DYNASTIES 1066 — the Liao and Western Xia (DRAFT)

**DRAFT — pending main-session review. Nothing here has been written into any
mod file.** Produced by an Opus research agent, 2026-08-01, against commit
`c3b34d8` (China-East landed). Every mechanical claim carries a `file:line`.
Historical claims that no file can settle are flagged `[U]` (unverified /
estimated) or `[D]` (sources genuinely differ), never asserted silently.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, 491,179 bytes, present)
`MOD = .../1066 Test Mod`

**Method, and the proof that the resolver is honest.** Counts come from an
independent reimplementation of four `build_setup.py` parsers — `_parse_defs`
(`tools/build_setup.py:689`), `_ownable_set` (`:713`), `_resolve_ruleset`
(`:756`) and the `OWN_KEYS`/`COUNTRY_RE` country reader (`:4543`, `:4401`) —
all reading `encoding='utf-8-sig'`, all token/brace based, comments masked
before tokenising. **Proven on a known positive:** the resolver was pointed at
the build's own nine shipped `LOCATION_VACATED_EXPECT` constants
(`tools/build_setup.py:1363`, `:1368-1376`) and reproduced every one of them
exactly — CHI 198, CRS 37, QAS 19, BAT 18, BGT 17, KHD 16, HCN 21, OTC 23,
OGE 18, nine of nine. A resolver that could not reproduce those would have
been discarded. Location cultures/religions come from
`VAN/in_game/map_data/location_templates.txt`, whose blocks are **single-line**
— a line-anchored `^[ \t]*culture` regex returns a confident zero on every one
of the 20,922 entries. That mistake was made here first, caught by asserting
`cult['dadu'] == 'yan_culture'`, and is recorded because it is exactly the
silent-zero class the harness discipline exists for.

---

## 0. The theater, and the finding that reframes it

### 0.1 The brief's one wrong premise, corrected

The task brief (and `docs/INDIA-CHINA-REVIEW.md:443`) calls `yanbei_area` "the
Sixteen Prefectures". **It is not.** Resolved from `definitions.txt` and named
from `VAN/main_menu/localization/english/location_names/location_names_l_english.yml`,
`yanbei_area`'s six provinces are `daning` (Dàníng), `chaoyang` (Cháoyáng),
`quanning` (Quánníng), `shangdu` (Shàngdū), `xingzhou` (Xìngzhōu) and `xinghe`
(Xìnghé) — Jehol, Chifeng and the Shangdu grasslands, **north of the Great
Wall**, template culture `kharchin_culture` 15 / `mongolian_culture` 10 /
`jurchen_culture` 6, religion `tengri` 16 / `mahayana` 12 / `shamanism` 4.
That is not ceded Chinese territory. It is the **Khitan heartland** and the
seat of the Liao Central Capital.

The Sixteen Prefectures of Yan and Yun are, on this map:

| historical circuit | area | ownable | template culture | template religion |
|---|---|---|---|---|
| Yōu / Yan (幽州) — the **Southern Capital** | `beiping_area` | **48** | `yan_culture` 35, `jin_culture` 10, `jilu_culture` 3 | `mahayana` 48 |
| Yún (雲州) — the **Western Capital** | `datong_area` | **36** | `tumed_culture` 15, `jin_culture` 13, `mongolian_culture` 5, `jilu_culture` 3 | `tengri` 20, `sanjiao` 11, `mahayana` 5 |

Both are 100% CHI-held today and in vanilla. This matters for the package's
shape: taking the Sixteen Prefectures means taking `beiping_area` (which
contains `dadu`, CHI's *vanilla* capital, now repointed to `kaifeng` by
`CAPITAL_FIXES` — `tools/build_setup.py:2258`) and most of `datong_area`.

### 0.2 The finding that makes this slice cheap: all five Liao capitals exist

The Liao ran a Five Capitals system. Every one of the five is a real location
in `definitions.txt`, and four of the five already carry the right name:

| Liao capital | founded | location id | loc string | area | vanilla owner |
|---|---|---|---|---|---|
| **Shangjing Linhuang Fu** 上京臨潢府 — Supreme | 918 [U] | **`linhuang`** | `Línhuáng` (`location_names_l_english.yml`) | `songnen_area / xiliao_province` (!) | OTC |
| **Zhongjing Dading Fu** 中京大定府 — Central | 1007 [U] | `daning_pingquan` | `Dàníng` #大宁/大寧 | `yanbei_area / daning_province` | CHI |
| **Dongjing Liaoyang Fu** 東京遼陽府 — Eastern | 938 [U] | `liaoyang` | `Liáoyáng` | `liaodong_area / liaoyang_province` | SYG |
| **Nanjing Xijin Fu** 南京析津府 (Yanjing) — Southern | 938 [U] | `dadu` | `Dàdū` #大都 | `beiping_area / shuntian_province` | CHI |
| **Xijing Datong Fu** 西京大同府 — Western | 1044 [U] | `datong_datong` | `Dàtóng` #大同 | `datong_area / datong_province` | CHI |

`linhuang` is the discovery of this pass. Vanilla put the Liao Supreme Capital
in `xiliao_province` — literally "**West Liao** province" — inside
`manchuria_region / songnen_area`, template `mongolian_culture` + `tengri`, and
it is **currently unowned in the mod** because item 32's `LOCATION_VACATED["CHI"]`
sweep emptied `manchuria_region`. Its province-mates are `qingzhou_mongol`
(Qìngzhōu — the Liao imperial tomb town [U]), `kailu`, `zhengjiatun`, `haihaer`
and `xinkai`.

Do not confuse it with `shangjing` (Shàngjīng) in `songhua_area / lalin_province`,
LAL-held: that is the **Jurchen Jin** dynasty's Shangjing Huining Fu near
Harbin, a 1115+ foundation. Two different Shangjings; vanilla ships both.

### 0.3 Vanilla ships no Khitan anything

Scanned across `VAN/in_game/`, `VAN/main_menu/common/`,
`VAN/main_menu/localization/english/` and `VAN/loading_screen/` for
`Khitan|khitan|Qidan|qidan|Kitan`:

- **no country tag**, no `setup/countries` entry, no formable;
- **no culture** — `in_game/common/cultures/east_asia.txt` has no khitan entry
  and `main_menu/common/named_colors/02_map.txt` has no `map_khitan`;
- **no dynasty** in `main_menu/setup/start/04_dynasties.txt`;
- exactly **three** English strings, all descriptive prose:
  `artists_l_english.yml:1107` (the Fogong pagoda, "Constructed in 1056 during
  the Liáo dynasty… under the patronage of the Khitan rulers" — vanilla's own
  1066-adjacent flavour), `culture_groups_l_english.yml:75`
  (`jurchen_group_desc`, "destroyed the Khitan Liáo Dynasty"), and
  `events/DHE/flavor_mch_l_english.yml:118` (the Khitan script).

The Tangut fare better. **`mi_niah_culture` IS the Tangut culture** —
`VAN/in_game/common/cultures/east_asia.txt:1525`, whose own comment is
`#https://en.wikipedia.org/wiki/Tangut_people`, `language = qiangic_language`,
`color = map_tangut`, culture group `tibeto_burman_group`. The colour key
exists at `VAN/main_menu/common/named_colors/02_map.txt:2434`,
`map_tangut = rgb { 170 95 126 }`. **But `mi_niah_culture` is placed on ZERO
locations** in `location_templates.txt` — it is a definition with no pops, which
is precisely what a `culture_definition` is for (the `cuman_culture` precedent,
`in_game/setup/countries/zz_1066_new_countries.txt`, CUM).

### 0.4 What the map looks like today

Resolved against the mod's built `10_countries.txt` and against pristine
vanilla (the build's actual input — see §I):

| area | ownable | VANILLA owners | MOD owners today |
|---|---|---|---|
| `beiping_area` | 48 | CHI 48 | CHI 48 |
| `datong_area` | 36 | CHI 36 | CHI 36 |
| `yanbei_area` | 36 | CHI 33, HCN 3 | CHI 33, **3 unowned** |
| `liaodong_area` | 33 | SYG 27, CHI 5, KOR 1 | SYG 27, **5 unowned**, KOR 1 |
| `songnen_area` | 33 | OTC 16, HCN 6, CHI 6, FUY 3, NEM 1, MIC 1 | **28 unowned**, FUY 3, NEM 1, MIC 1 |
| `songhua_area` | 32 | 8 tribal tags + OTC 2 + CHI 2 | **4 unowned**, 22 tribal |
| `ussuri_area` | 32 | CHI 4 + 21 tribal | **4 unowned**, 28 tribal |
| `middle_amur_area` | 50 | CHI 50 | **50 unowned** |
| `lower_amur_area` | 43 | CHI 42, HIJ 1 | **42 unowned**, HIJ 1 |
| `argun_area` | 30 | QAS 8, BGT 7, CHI 7, OTC 5, HCN 3 | **30 unowned** |
| `eastern_gobi_area` | 35 | CHI 26, HCN 9 | **35 unowned** |
| `southern_gobi_area` | 16 | CHI 13, BAT 3 | **16 unowned** |
| `lower_selenga_area` | 21 | CHI 19, BGT 2 | **21 unowned** |
| `upper_selenga_area` | 23 | CRS 13, CHI 10 | **23 unowned** |
| `shilkari_area` | 24 | QAS 11, BGT 8, CHI 5 | **24 unowned** |
| `western_gobi_area` | 32 | BAT 14, KHD 9, CHI 9 | **32 unowned** |
| `mongolian_great_lakes_area` | 21 | CRS 13, KHD 7, OGE 1 | **21 unowned** |
| `tuva_area` | 11 | CRS 11 | **11 unowned** |
| `hexi_area` | 54 | CHI 54 | CHI 54 |
| `gansu_area` | 30 | CHI 29, BAT 1 | CHI 29, **1 unowned** |
| `shaanxi_area` | 65 | CHI 65 | CHI 65 |
| `longyou_area` | 39 | CHI 22 + 7 small tags | unchanged |

`mongolia_region` is **213 ownable, 213 unowned**. `manchuria_region` is 223
ownable: 133 unowned, SYG 27, KOR 1, and **62 across 46 Jurchen/Tungus tribal
tags** holding 1-3 locations each. That tribal layer is vanilla's and survived
item 32 untouched — it is the single most 1066-correct thing on the eastern map
and this package does not disturb it (§H).

**Beware the naming trap in the west.** `hexi_area` is NOT the Hexi Corridor —
it is Yan'an, Qingyang, Pingliang, Lingzhou, Ningxia and the Ordos rim
("west of the [Yellow] River"). The actual Hexi Corridor — Liangzhou, Ganzhou,
Suzhou, Shazhou/Dunhuang — is **`gansu_area`**. A package written from the
area name alone would give Western Xia the Song's Shaanxi frontier and miss
Dunhuang entirely.

---

## A. Registry additions (`in_game/setup/countries/zz_1066_new_countries.txt`)

**Two new tags. Freeness proven THREE ways each**, both scan modes, per the
`map_TAG` blind-spot lesson (`docs/HANDOFF.md`, AUDIT-2026-07-31 D3):

1. word-boundary `grep -rw TAG` over the entire vanilla tree
   (`--include=*.txt --include=*.yml --include=*.gui`), non-localisation and
   English-localisation counted separately;
2. **substring** `grep -rn "_TAG\b\|\bTAG_"` over the same tree — this is the
   scan that catches `map_TAG` colour keys, `TAG_ADJ` loc rows, formable
   `flag = TAG` references and gfx keys;
3. the same two scans over the entire mod repo (including `tools/*.py` and
   `docs/*.md`).

| candidate | VAN word (non-loc) | VAN word (en-loc) | VAN substring | VAN registry | MOD word | MOD substring | verdict |
|---|---|---|---|---|---|---|---|
| **LIA** | 0 | 0 | 0 | 0 | 0 | 0 | **FREE** |
| **XIA** | 0 | 0 | 0 | 0 | 0 | 0 | **FREE** |
| KHI | 0 | 0 | 0 | 0 | 0 | 0 | free (banked) |
| QID | 0 | 0 | 0 | 0 | 0 | 0 | free (banked) |
| XSA | 0 | 0 | 0 | 0 | 0 | 0 | free (banked) |
| LAO | 0 | 0 | 0 | 0 | 0 | 0 | free (banked) |
| MNH | 0 | 0 | 0 | 0 | 0 | 0 | free (banked) |
| **TNG** | 25 | 1 | 18 | **1** | — | — | **TAKEN** — `TNG = { #Toungoo }`, `VAN/in_game/setup/countries/south_east_asia.txt:143`, `TNG: "Toungoo"` `country_names_l_english.yml:3680` |
| KTN | 22 | 1 | 18 | 1 | — | — | TAKEN |
| TGT | 22 | 1 | 20 | 1 | — | — | TAKEN |
| ORD | 33 | 1 | 20 | 1 | — | — | TAKEN |

The brief's warning about TNG was correct and is now proven: it is Toungoo in
Burma, and reusing it would consume a real SEA tag the deferred Pagan slice
(`docs/INDIA-CHINA-REVIEW.md:445`) will want.

```
LIA = { #The Liao — the Khitan empire (Shangjing Linhuang)
	color = map_LIA
	color2 = rgb { 16 41 202 }

	culture_definition = kharchin_culture
	religion_definition = mahayana
}

XIA = { #Western Xia — the Tangut state (Xingqing)
	color = map_XIA
	color2 = rgb { 16 41 202 }

	culture_definition = mi_niah_culture
	religion_definition = mahayana
}
```

**`culture_definition` citations and the honest caveat.**
`kharchin_culture` — `VAN/in_game/common/cultures/east_asia.txt:2802`, comment
`#https://en.wikipedia.org/wiki/Kharchin_Mongols`, `language = mongolian_language`,
groups `mongolian_group` + `steppe_group`, `color = map_kharchin`
(`02_map.txt:2640`). It is the culture vanilla itself paints across the Khitan
heartland: 15 of `yanbei_area`'s 36 locations and 2 of `liaodong_area`'s carry
it. There is no Khitan culture to use, and `kharchin_culture` is the closest
real descendant — the Kharchin Mongols of exactly this ground. **This is the
al-Andalus/BLH situation the user has accepted twice**
(`docs/HANDOFF.md:406-408`, CENTRAL-ASIA-PACKAGE §A): the identity is a
best-available proxy, the pops stay what they are until the pop phase.
See OPEN DECISION 3 for the alternative (invent `khitan_culture`).

`mi_niah_culture` — `east_asia.txt:1525`, the Tangut culture, **zero locations**.
Perfect fit: an identity-only culture for an identity-only registry field, the
exact `cuman_culture` shape CUM already ships.

`mahayana` on both — verified as a real religion by its use as a template
religion on `dadu`, `liaoyang`, `lingzhou` and 20 of `liaodong_area`'s 33
locations (`location_templates.txt`). The Liao court was aggressively Buddhist
(the 1056 Fogong pagoda is vanilla's own artist entry, `artists_l_english.yml:1107`);
the Tangut state translated the whole Buddhist canon into Tangut [U]. Note the
pop-level reality differs: `yanbei_area` is `tengri` 16 / `mahayana` 12, and
`datong_area` is `tengri` 20 / `sanjiao` 11 / `mahayana` 5. A
country-vs-pop religion split is normal and already shipped (KHM's hindu ruler
over a theravada registry, `tools/build_setup.py:3307` comment).

**Two new colours** in `main_menu/common/named_colors/zz_1066_map_colors.txt`.
Both keys verified absent from vanilla **by key name** (zero substring hits —
the D3 lesson). Neighbours checked: CHI wears crimson, KOR `map_KOR = rgb { 26 53 177 }`
(`02_map.txt:2085`), SYG `map_SYG = rgb { 50 170 50 }` (`:2087`), and the
Manchurian tribal patchwork.

```
	map_LIA = rgb { 40 60 110 }     # the Liao        Khitan indigo
	map_XIA = rgb { 170 95 126 }    # Western Xia     -- see note
```
`map_XIA`'s suggested value is deliberately vanilla's own `map_tangut`
(`02_map.txt:2434`) so the country reads as its culture; if that collides
badly against CHI's crimson, shift it toward dusty rose. Values are
suggestions; the constraint is that LIA must not read as CHI or KOR and XIA
must not read as CHI.

**Localisation** — `main_menu/localization/english/1066_norman_conquest_l_english.yml`,
one physical line each, appended in the file's existing style:
```
 LIA: "Liáo"
 LIA_ADJ: "Khitan"
 XIA: "Xià"
 XIA_ADJ: "Tangut"
```
`LIA` and `XIA` are the **NAME** keys and they are live — see §F, where the
render is worked out. No `_THE` rows: the mod's own `SEL_THE` caveat
(`docs/HANDOFF.md:1003-1005`, whether the engine consults `_THE` is unproven)
plus the fact that neither name construction branch used here reads an article.

**Coats of arms.** Both tags must land in `verify_mod.py`'s `_GENERATOR_OK`
(`tools/verify_mod.py:924`) or carry a CoA block — the check at `:957-960`
fails a new registry tag that has neither. Recommendation: `_GENERATOR_OK`,
tier 4, with the comment that neither dynasty used European-style heraldry.

---

## B. NEW_COUNTRIES blocks

Both follow the shape of vanilla's own five `far_east_asia_monarchy` users
(CHI, KOR, SYG, SSG, TMN — `VAN/main_menu/setup/start/10_countries.txt`) and
the mod's existing `_seljuk_block` / `_CENTRALASIA_TAGS` factory
(`tools/build_setup.py:912`, `:1118`). Neither block carries `own_control_core`
— territory arrives by `LOCATION_GRANTS` after the block is inserted, the
QRK/QRA/BLH/QMT route (`tools/build_setup.py:4652`, `:4827`, `:4834`).

```
	LIA = {
		starting_technology_level = 3
		include = "far_east_asia_monarchy"
		include = "expl_mongols"

		government = {
			heir_selection = cognatic_primogeniture
		}
		court_language = jin_language

		country_rank = rank_empire

		capital = linhuang
	}

	XIA = {
		starting_technology_level = 3
		include = "east_asia_monarchy_no_coast"
		include = "expl_china"

		government = {
			heir_selection = cognatic_primogeniture
		}
		court_language = northern_mandarin_dialect

		country_rank = rank_kingdom

		capital = ningxia
	}
```

Field by field, all verified:

- **`far_east_asia_monarchy`** (`VAN/main_menu/setup/templates/far_east_asia_monarchy.txt`)
  — read in full. `starting_technology_level = 3`, `include = "expl_china"`,
  `government = { type = monarchy  heir_selection = cognatic_primogeniture
  reforms = { three_departments_system } … sinicized_vs_unsinicized = -70 … }`
  plus the full law set. Five vanilla users. **The reform is valid**: 
  `three_departments_system`'s `potential`
  (`VAN/in_game/common/government_reforms/country_specific.txt:2142-2159`) is an
  OR whose first branch is `has_societal_value = societal_value_type:sinicized_vs_unsinicized`
  AND `societal_value:sinicized_vs_unsinicized < -60` — and the template itself
  sets `-70`. So the reform self-satisfies regardless of language or IO
  membership. **This is the JAP-reform bug's opposite** (`docs/INDIA-CHINA-REVIEW.md:609-630`,
  where `shogunate`'s `allow` required a stripped IO): here the template
  supplies its own gate and no error class opens.
- **`sinicized_vs_unsinicized = -70` on the Liao is a design statement**, and a
  contestable one: the Liao ran a deliberate dual administration (a Northern
  Chancellery for the tribes, a Southern for the Chinese prefectures) and were
  the *least* sinicized of the conquest dynasties by their own choice [U]. The
  alternative is `east_asia_monarchy` (`east_asia_monarchy.txt`), which sets the
  other twelve sliders but **no `sinicized_vs_unsinicized` line at all** and no
  `reforms` block — 3 vanilla users. See OPEN DECISION 5.
- **`east_asia_monarchy_no_coast` for XIA** — Western Xia is landlocked; every
  one of its 48 locations is inland. The `_no_coast` variant is vanilla's answer
  to the engine's maritime self-heal (`government.cpp:3662`, one error line per
  removed coastal content — measured on exactly five taifas,
  `tools/build_setup.py:565-571`). **Read the file before shipping**: the
  Muslim `_no_coast` variant carries no `heir_selection` and the taifa factory
  had to restate it (`:582-583`); whether `east_asia_monarchy_no_coast` does the
  same is a one-line diff the implementer must run. `heir_selection` is restated
  above either way, which is safe in both cases.
- **`expl_mongols` on LIA** (`VAN/main_menu/setup/templates/expl_mongols.txt`)
  — carries `mongolia_region`, `manchuria_region`, `north_china_region`,
  `korea_region`, `japan_region`, `west_siberia_region` and 24 more regions.
  `expl_china` (used by `far_east_asia_monarchy` internally) already carries
  `mongolia_region` + `manchuria_region` + `north_china_region`, so
  `expl_mongols` is strictly a *reach* addition, not a capital-assert
  requirement. CHI itself carries both (`10_countries.txt:26238` block).
- **The capital-discovery assert** (`tools/build_setup.py:4463-4472`,
  `"{tag}: capital {cap} is not discovered by any include"`) — `linhuang` is in
  `manchuria_region`, covered by `expl_china` inside `far_east_asia_monarchy`;
  `ningxia` is in `west_china_region`, also in `expl_china`. Both pass. **No
  inline `discovered_regions` is needed** — unlike BLH, which needed one because
  `ural_region` was in no template (CENTRAL-ASIA-PACKAGE §B).
- **`court_language = jin_language`** (`VAN/in_game/common/languages/00_china.txt:814`,
  `family = chinese_language_family`) — this single token is what makes the map
  read "Great Liáo" rather than "Khitan Empire". Worked out in full in §F.
  `jin_language` rather than `northern_mandarin_dialect` because `jin_culture`
  is the template culture of the Datong/Xuanhua prefectures the Liao actually
  ruled (13 of `datong_area`'s 36, 10 of `beiping_area`'s 48) and because
  Yan/Jin is the Liao's own Chinese-speaking subject population. CHI carries
  `northern_mandarin_dialect` (`MOD/main_menu/setup/start/10_countries.txt`,
  CHI block) — a different Chinese language keeps the two courts distinct while
  both stay in the family.
- **`court_language = northern_mandarin_dialect` on XIA** — `liang_culture`
  (`east_asia.txt:273`), the template culture of 25 of `gansu_area`'s 30 and of
  the Ningxia core, declares exactly this language. The Tangut alternative,
  `qiangic_language` (`00_china.txt:1043`), **declares no `family` line at all**
  (the last `family` in that file before it is `burmic_language_family` at
  `:1024`, and there is none after) — so a Tangut court language would drop XIA
  out of every `chinese_language_family` branch. Since XIA is `rank_kingdom`
  those branches do not fire anyway (§F), so this is a low-stakes choice; see
  OPEN DECISION 6.
- **`heir_selection = cognatic_primogeniture`** — the project's attested
  restate value, used by every new tag since the taifas. Both dynasties in fact
  practised something closer to designated succession with dowager regencies
  [U]; primogeniture is the safe, measured choice.
- **Ranks** — LIA `rank_empire`, XIA `rank_kingdom`. Argued in §F.

---

## C. Rulers

Character-block shape copies the China-East entries verbatim
(`tools/build_setup.py:3259-3315`): `first_name`, `culture`, `religion`,
`birth_date`, `birth`, `dynasty`, `tag`. **No `death_date`** — the alive law
(`docs/HANDOFF.md:9-22`). `HISTORICAL_RULERS` entries take the 4-tuple form
`(key, accession, regnal, regnal_name)` (`tools/build_setup.py:269-275`).

| tag | character key | first_name | accession | birth | regnal | regnal_name | dynasty |
|---|---|---|---|---|---|---|---|
| **LIA** | `lia_yelu_hongji_daozong` | LITERAL `Yelu_Hongji` | `1055.8.28` **[U on the day]** | `1032.1.1` [U] | 0 | `Daozong` | `yelu_dynasty` NEW |
| **XIA** | `xia_li_liangzuo_yizong` | LITERAL `Li_Liangzuo` | `1048.1.19` **[U on the day]** | `1047.1.1` [U] | 0 | `Yizong` | `weiming_dynasty` NEW |

**Daozong (Yelü Hongji, 耶律洪基), 8th Liao emperor, r. 1055-1101.** Son of
Xingzong (Yelü Zongzhen), who died in 1055 [U]. Daozong is 34 at
`START_DATE` and reigns another 35 years — the longest and least eventful Liao
reign, the one under which the dynasty peaks and then rots (the Yelü Yixin
affair, the judicial murder of Empress Xuanyi in 1075, are all future
material [U]). He is the correct man for 1066 and there is no
competing reading. The regnal name route is the `regnal_name` literal
mechanism already proven for `Yingzong`, `Munjong`, `Ly_Thanh_Tong` and
`Mustansir` (`tools/build_setup.py:269-272`, `:157`).

**One free win:** `Yelu: "Yelu"` **already exists in vanilla**,
`VAN/main_menu/localization/english/character_names_l_english.yml`. That is a
name-pool entry, not a dynasty — the same situation as `Qarakhanid`
(CENTRAL-ASIA-PACKAGE §D) — so if the implementer prefers the bare surname as
the displayed first name, no loc row is needed. `Hongji`, `Longxu` (Daozong's
Khitan name [D]), `Daozong` and `Xingzong` are all absent and need rows.

**Yizong (Li Liangzuo, 李諒祚), 2nd Western Xia emperor, r. 1048-1067.**
**The brief's "child ruler — regency question" resolves cleanly and the answer
is no regency.** Liangzuo was born in 1047 and put on the throne in 1048 as an
infant after his father Yuanhao was murdered [U]; the Mozang (没藏) clan
regency — his mother the Empress Dowager and her brother Mozang Epang — ran the
state until **1061**, when Liangzuo destroyed the Mozang and took personal
rule [U]. At `START_DATE = 1066.9.15` he is **19 years old and has ruled
personally for five years**. He clears `ADULT_AGE = 16`
(`tools/build_setup.py:5672`, citing `loading_screen/common/defines/00_defines.txt:1519`)
with three years to spare, so no `active_regent` / `regency` field is needed —
which is fortunate, since `COUNTRY_LINES` (`tools/build_setup.py:4408`) strips
every one of those fields unconditionally. **He dies in 1067**, one year in:
a ready-made early-game succession event, and the same shape as CHI's Yingzong
(who dies in January 1067 — `tools/build_setup.py:269` comment). Two of the
three great northern thrones turn over inside the first sixteen months. That is
a feature; see OPEN DECISION 10.

Culture/religion on both characters: copy the tag's own registry block, the
guaranteed-valid route the China-East batch used
(`tools/build_setup.py:3255-3258` comment). So `culture = kharchin_culture`,
`religion = mahayana` for Daozong; `culture = mi_niah_culture`,
`religion = mahayana` for Liangzuo.

`birth = linhuang` for Daozong, `birth = ningxia` for Liangzuo — both are
locations the tag will hold, satisfying `initialize_from_bookmark.cpp:410`
(`docs/EU5-ERROR-DECODER.md`, "character has no birth scripted").

**Loc rows required** (one physical line each):
```
 Yelu_Hongji: "Yelü Hongji"
 Daozong: "Daozong"
 Li_Liangzuo: "Li Liangzuo"
 Yizong: "Yizong"
 yelu_dynasty: "Yelü"
 weiming_dynasty: "Weiming"
```

---

## D. Dynasties (`main_menu/setup/start/04_zz_1066_dynasties.txt`)

Vanilla ships 1,269 dynasties and **neither of these**. Greps for
`yelu|yelü|tuoba|weiming|xixia|xi_xia` over
`VAN/main_menu/setup/start/04_dynasties.txt` and
`VAN/main_menu/localization/english/dynasty_names_l_english.yml` return nothing.
(For contrast, `wang_dynasty` `:1588`, `duan_dynasty` and `borjigin_dynasty` DO
ship, and the mod itself added `zhao_dynasty` and `ly_dynasty` in item 32.)

Appended to the existing `dynasty_manager = { … }` block, minimal entry shape
per vanilla's `munso_dynasty` and the file's own header:

```
	yelu_dynasty = {
		name = { name = yelu_dynasty }
		home = linhuang
	}
	weiming_dynasty = {
		name = { name = weiming_dynasty }
		home = ningxia
	}
```

**Why `weiming_dynasty` and not `li_xia`.** The Tangut imperial clan's own name
was Weiming (嵬名); `Li` and `Zhao` were surnames granted by the Tang and Song
courts respectively, and Yuanhao formally repudiated both when he proclaimed
the empire in 1038 [D — western sources overwhelmingly use "Li", the dynasty's
own usage was Weiming]. The rulers are still universally *called* Li Yuanhao,
Li Liangzuo etc. in English, which is why the character's `first_name` literal
above is `Li_Liangzuo` while the house is `weiming_dynasty`. That split is
deliberate and matches how the sources actually read. If it grates, `li_dynasty`
is the alternative — OPEN DECISION 7.

Both `home` locations are verified in `definitions.txt` and are held by their
tag under §E.

---

## E. Territory

### E.1 `_NORTH_RULES` — the definitions-resolved grants

Same 5-tuple shape as `_SELJUK_RULES` / `_CENTRALASIA_RULES`
(`tools/build_setup.py:855`, `:1163`):
`tag: (sweep names, singles, minus-sweeps, minus-singles, expected)`.

```python
_NORTH_RULES = {
    # THE LIAO — the Five Capitals and their circuits.
    #   beiping_area      the Southern Capital (Yanjing/dadu) — the eastern
    #                     half of the Sixteen Prefectures, ceded 938
    #   datong_area       the Western Capital (Xijing/datong_datong) — the
    #                     western half; minus the Ordos and the western
    #                     Hetao, which are Tangut (see XIA below)
    #   yanbei_area       the Central Capital (Zhongjing/daning_pingquan) —
    #                     the Khitan heartland north of the Wall
    #   liaodong_area     the Eastern Capital (Dongjing/liaoyang); KOR keeps
    #                     linjiang_jurchen, its own Yalu bridgehead
    #   xiliao/taoer/chol the Supreme Capital circuit (Shangjing/linhuang)
    #                     on the Shira Muren and the upper Nen
    "LIA": (["beiping_area", "yanbei_area", "liaodong_area", "datong_area",
             "xiliao_province", "taoer_province", "chol_province"],
            [], ["ordos_province", "hetao_province"], ["linjiang_jurchen"],
            161),

    # WESTERN XIA — Ordos, Ningxia and the Hexi Corridor.
    #   lingzhou/ningxia  the core: Xingqing Fu (ningxia = Yinchuan) and
    #                     Lingzhou/Xiping Fu, the pre-1038 seat
    #   ordos/hetao       Xiazhou (tongwancheng), the Dingnan Jiedushi's
    #                     ancestral seat, + the western Hetao
    #   yulin/suide       Yinzhou/Youzhou/Suizhou — the Song frontier the
    #                     1067 Suizhou affair is about (AFTER our date)
    #   ganzhou/suzhou/shazhou/yongchang  the Hexi Corridor proper,
    #                     conquered from the Uyghurs and Guiyi 1028-1036:
    #                     Ganzhou, Suzhou, Shazhou (Dunhuang), Liangzhou
    "XIA": (["lingzhou_province", "ningxia_province", "yulin_province",
             "suide_province", "ordos_province", "hetao_province",
             "ganzhou_gansu_province", "suzhou_gansu_province",
             "shazhou_province", "yongchang_gansu_province"],
            [], [], [], 48),
}
```

**LIA Tier A — 161 locations, by circuit, with donors:**

| circuit | resolves to | n | donors |
|---|---|---|---|
| Southern Capital | `beiping_area` | 48 | CHI 48 |
| Western Capital | `datong_area` − Ordos − Hetao | 29 | CHI 29 |
| Central Capital | `yanbei_area` | 36 | CHI 33, **HCN 3** |
| Eastern Capital | `liaodong_area` − `linjiang_jurchen` | 32 | **SYG 27**, CHI 5 |
| Supreme Capital | `xiliao` + `taoer` + `chol` | 16 | **OTC 10, HCN 6** |
| **total** | | **161** | **CHI 115, SYG 27, OTC 10, HCN 9** |

`linhuang`, `daning_pingquan`, `liaoyang`, `dadu`, `datong_datong` and
`shangdu` are all inside the resolved list — verified by membership test, the
`_CENTRALASIA_TAGS` capital assert's requirement (`tools/build_setup.py:4653-4656`).

**XIA — 48 locations, by province:**

| province | n | donors | template culture |
|---|---|---|---|
| `lingzhou_province` | 4 | CHI 4 | `liang_culture` 3, `jin_culture` 1 |
| `ningxia_province` | 4 | CHI 4 | `liang_culture` 4 |
| `yulin_province` | 5 | CHI 5 | `jin_culture` 5 |
| `suide_province` | 4 | CHI 4 | `jin_culture` 4 |
| `ordos_province` | 4 | CHI 4 | `tumed_culture` 4 |
| `hetao_province` | 3 | CHI 3 | `tumed_culture` 1, `mongolian_culture` 2 |
| `ganzhou_gansu_province` | 6 | CHI 6 | `liang_culture` 5, `amdowa_culture` 1 |
| `suzhou_gansu_province` | 4 | CHI 4 | `liang_culture` 3, `yugur_culture` 1 |
| `shazhou_province` | 7 | CHI 6, **BAT 1** | `liang_culture` 6, `mongolian_culture` 1 |
| `yongchang_gansu_province` | 7 | CHI 7 | `liang_culture` 7 |
| **total** | **48** | **CHI 47, BAT 1** | |

The capital `ningxia` (Níngxià — the Ming Ningxia Wei at modern Yinchuan, i.e.
Xingqing Fu [U]) is in `lingzhou_province`, and `tongwancheng` (Xiazhou, the
Tuoba-Tangut ancestral seat) is in `ordos_province`. Both are in the resolved
list. There is **no `xingqing` or `yinchuan` location** in `definitions.txt` —
`ningxia` is the seat this map offers, exactly the naming-era mismatch the mod
has absorbed before.

The BAT donation is `niuquanzi`, the Gobi-edge outlier item 32 already noted
(`tools/build_setup.py:1370-1371`, "1066 Gansu is Western Xia ground (deferred
slice); empty beats a Chinggisid"). **This package is that deferred slice**,
and `niuquanzi` now gets its intended owner.

**`xining_province` (6) is deliberately EXCLUDED from XIA.** That is Qingtang /
Tsongkha — the Tibetan kingdom of Gusiluo's successors, a Song ally and Xia's
enemy, not conquered until 1099+ [U]. Its template cultures are `monguor_culture` 2
and `liang_culture` 4. It stays CHI's for now, which is wrong but is a
*different* slice's wrong; see §H and OPEN DECISION 8.

### E.2 LIA Tier B — eastern Mongolia (149, OPTIONAL)

```python
    # LIA Tier B — the eastern steppe the Liao administered through its
    # Supreme and Central Capital circuits: the Kerulen, the Onon, the
    # Selenga and the eastern Gobi. The WEST (western_gobi,
    # mongolian_great_lakes, tuva — 64) is Zubu tribal ground and stays
    # EMPTY.
    "LIA_B": (["argun_area", "eastern_gobi_area", "southern_gobi_area",
               "lower_selenga_area", "upper_selenga_area", "shilkari_area"],
              [], [], [], 149),
```

| area | n | donors |
|---|---|---|
| `argun_area` | 30 | QAS 8, BGT 7, CHI 7, OTC 5, HCN 3 |
| `eastern_gobi_area` | 35 | CHI 26, HCN 9 |
| `southern_gobi_area` | 16 | CHI 13, BAT 3 |
| `lower_selenga_area` | 21 | CHI 19, BGT 2 |
| `upper_selenga_area` | 23 | CRS 13, CHI 10 |
| `shilkari_area` | 24 | QAS 11, BGT 8, CHI 5 |
| **total** | **149** | CHI 80, QAS 19, BGT 17, CRS 13, HCN 12, OTC 5, BAT 3 |

**A+B = 310 locations.** Donors: CHI 195, SYG 27, HCN 21, QAS 19, BGT 17,
OTC 15, CRS 13, BAT 3.

**The history, stated with its uncertainty.** The Liao claimed the whole
eastern steppe and garrisoned it — the Zhenzhou Weiwu Jun at Kedun on the Tuul
was its westernmost post [U] — but "administered" is far too strong a word for
the Mongolic tribes the Liao called the Zubu (阻卜), who rebelled repeatedly
through the 11th century [U]. Tier B is therefore a **claim rendered as
ownership**, which is what a grand-strategy map does with nomad suzerainty
everywhere else (the Golden Horde's 731 locations are the same fiction). Tier A
alone is defensible; Tier B is defensible; giving the Liao all 213 of
`mongolia_region` is not. See OPEN DECISION 2.

**Tier C — 64 locations left EMPTY** (`western_gobi_area` 32,
`mongolian_great_lakes_area` 21, `tuva_area` 11). Naimans, Merkits, Oirats and
Kyrgyz — no state, no capital, no attested 1066 ruler. **The Pecheneg
discipline** (`docs/HANDOFF.md:950-955`, and CENTRAL-ASIA-PACKAGE OPEN DECISION
2, which the user accepted for the Kipchaks): a state is EARNED by later
events. Recommend leaving them unowned, which is what they already are.

### E.3 Landless after

SYG loses **all 27** of its locations to LIA and must be added to the landless
machinery. This is not optional: `_landless_claims` derives from
`LANDLESS_AFTER` (`tools/build_setup.py:4814-4816`), and a tag that goes
landless *without* being in that list gets **no claims written** and the engine
says so at start — `initialize_from_bookmark.cpp:592`, the seventeen-line Italy
North class (`docs/EU5-ERROR-DECODER.md`). One line:

```python
NORTH_LANDLESS = ("SYG",)
```
appended into `LANDLESS_AFTER` (`tools/build_setup.py:2161-2165`).

SYG's claims then auto-derive to its 27 Liaodong locations — which is exactly
right: the Shenyang Wang appanage IS a future object (a Yuan-era grant to the
Korean royal house [U]), the GRA/MAM shape the project has shipped a dozen
times.

**SYG needs no `CAPITAL_FIXES` entry.** The capital-strip guard
(`tools/build_setup.py:5340-5366`) only fires when a tag **still holds
something** — `if held and capm.group(1) not in held` (`:5361`). A fully
landless tag's capital is exempt by construction; that is the POR/`guimaraes`
precedent the user already approved (`tools/build_setup.py:2217`). SYG's
`capital = shenyang` becomes vestigial and stays put.

**Every other donor is already landless-bound.** CHI keeps `kaifeng` (never
touched). HCN, OTC, QAS, BGT, CRS and BAT are all in `CHINA_LANDLESS`
(`tools/build_setup.py:1360-1361`) and go to zero either way. **No new
`CAPITAL_FIXES` entry is required by this package** — checked against every
donor.

### E.4 THE CONSTANT MOVES — exact, and self-asserting

Because grants run **before** vacates (`tools/build_setup.py:4834` then `:4886`)
and vacates resolve against the tag's *post-grant* holdings (`:4893`,
`got = sorted(_pool & set(_owned_by(src, _t)))`), every location this package
grants out of a vacate pool **must** be subtracted from that tag's
`LOCATION_VACATED_EXPECT`. The build dies loudly if you forget — 
`"LOCATION_VACATED[{t}]: resolved N owned locations, expected M"` (`:4895`).
Move these in the same commit, and per CLAUDE.md observe each one failing
first.

**If LIA takes Tier A only:**

| constant | from | to | why |
|---|---|---|---|
| `LOCATION_VACATED_EXPECT["CHI"]` | 198 | **193** | CHI's 5 `liaodong_area` locations move to LIA. (CHI's other 110 donations are in `north_china_region`, outside the CHI vacate pool `["mongolia_region","manchuria_region"]`.) |
| `LOCATION_VACATED_EXPECT["HCN"]` | 21 | **12** | 3 in `yanbei_area` + 6 in `xiliao/taoer/chol` |
| `LOCATION_VACATED_EXPECT["OTC"]` | 23 | **13** | 10 in `xiliao/taoer/chol` |

**If LIA takes Tier A + Tier B:**

| constant | from | to |
|---|---|---|
| `LOCATION_VACATED_EXPECT["CHI"]` | 198 | **113** |
| `LOCATION_VACATED_EXPECT["OTC"]` | 23 | **8** |
| `LOCATION_VACATED_EXPECT["CRS"]` | 37 | **24** |
| `LOCATION_VACATED_EXPECT["BAT"]` | 18 | **15** |
| `LOCATION_VACATED_EXPECT["HCN"]` | 21 | **0** — DELETE the entry |
| `LOCATION_VACATED_EXPECT["QAS"]` | 19 | **0** — DELETE the entry |
| `LOCATION_VACATED_EXPECT["BGT"]` | 17 | **0** — DELETE the entry |

(HCN, QAS and BGT lose their *entire* holdings to LIA's grant, so they reach
landless through the grant rather than the vacate. They stay in
`CHINA_LANDLESS`; only their `LOCATION_VACATED` / `_EXPECT` entries go. Leaving
a zero-count entry would also work — `_remove_owned_many` on an empty list is a
no-op — but deleting is cleaner and the landless verifier still guards them.)

**If XIA is taken (independent of the LIA tier):**

| constant | from | to | why |
|---|---|---|---|
| `LOCATION_VACATED_EXPECT["BAT"]` | 18 | **17** | `niuquanzi` (`gansu_area` is in the horde vacate pool, `tools/build_setup.py:1374`) |

XIA's other 47 come from CHI in `west_china_region` and `datong_area`
(`north_china_region`) — **outside** CHI's vacate pool, so `EXPECT["CHI"]` is
untouched by XIA.

**If both, with LIA at A+B:** BAT goes 18 → **14** (3 from Tier B + 1 from XIA);
all other rows as listed above.

### E.5 What this slice moves, in one line

**Tier A + XIA:** 209 locations change owner, 0 vacated, 1 tag retired,
2 new tags, 2 named rulers, 2 new dynasties. CHI 1,463 → 1,301 landed.

**Tier A + B + XIA:** 358 locations change owner, 2 new tags, 1 tag retired,
7 vacate constants moved. CHI 1,463 → 1,221 landed. SYG 27 → 0.

### E.6 The pop-line class shrinks — counted

`docs/EU5-ERROR-DECODER.md:676` records the class decoded on 2026-08-01:
`jomini_script_system.cpp:252 — Event target link 'religion' returned an
invalid object` at `scripted_triggers/pop_triggers.txt:3` via
`pop_types/00_default.txt:153`, **~504 lines**, one per pop on vacated
*settled* land, "accepted; the class shrinks as future slices land owners on
the steppe."

**This package is one of those slices, and the count is:**

| option | locations granted | of which UNOWNED in today's build |
|---|---|---|
| LIA Tier A | 161 | **24** |
| LIA Tier A+B | 310 | **173** |
| XIA | 48 | **1** |

So Tier A + XIA re-owns **25** currently-vacated locations; Tier A+B + XIA
re-owns **174**. The exact line reduction is not statically derivable (it is one
line *per pop*, not per location, and pop counts come from
`main_menu/setup/start/` pop files this package has not parsed), but the
direction and the location counts are measured. Tier B is where the real relief
is: 173 of the 174 are Mongolian steppe towns that item 32 emptied.

---

## F. Government, rank and naming — worked out to the rendered string

### F.1 The chain, verified link by link

The map name is composed by `country_name_construction.txt`, **first matching
branch wins**. In file order the relevant branches are:

| line | branch | trigger |
|---|---|---|
| `:92-98` | `country_name_construction_prefix_name` | `country_rank ?= country_rank:rank_empire` AND `court_language ?= { language_family ?= language_family:chinese_language_family }` |
| `:100-105` | `country_name_construction_prefix_name_horde` | `government_type = government_type:steppe_horde` |
| `:117-155` | `country_name_construction_prefix_adjective_rank` | `country_rank = rank_empire` (and eight other alternatives) |

Loc values (`VAN/main_menu/localization/english/government_names_l_english.yml`):
- `country_name_construction_prefix_name: "$PREFIX$ $NAME$"`
- `country_name_construction_prefix_adjective_rank: "$PREFIX$ $ADJ$ $RANK$"`

`$PREFIX$` and `$RANK$` come from the matching `country_ranks.txt` branch, also
first-match. In file order the empire branches that matter here:

| line | key | trigger | loc |
|---|---|---|---|
| `:306` | `rank_empire_horde` | `government_type = steppe_horde` | `rank_empire_horde: "Horde"`, `rank_empire_horde_prefix: "Great"` (`:119-121`) |
| `:365` | `rank_empire_jurchen` | `culture ?= { has_culture_group = culture_group:jurchen_group }` | `rank_empire_jurchen: "$rank_empire$"` (`:248`) |
| `:482` | `rank_empire_dynasty` | `court_language ?= { language_family ?= chinese_language_family }` OR is Middle Kingdom leader | **`rank_empire_dynasty: "Dynasty"`, `rank_empire_dynasty_prefix: "Great"`, `rank_empire_dynasty_ADJ: "imperial"`** (`government_names_l_english.yml:95-97`) |

### F.2 What LIA will actually render as

With `country_rank = rank_empire` + `court_language = jin_language`
(chinese family, `00_china.txt:818`):

- name construction: branch `:92` fires first → **`"$PREFIX$ $NAME$"`**;
- rank branch: `rank_empire_horde` fails (monarchy), `rank_empire_jurchen`
  fails (`kharchin_culture` is `mongolian_group` + `steppe_group`,
  `east_asia.txt:2812-2815`), `rank_empire_dynasty` fires at `:482` →
  `$PREFIX$` = **"Great"**;
- **the map reads `Great Liáo`** — 大遼, the dynasty's own self-designation,
  and the **`LIA:` NAME key IS live**;
- ruler title: `rank_empire_dynasty` declares no `_ruler_male`, so it falls
  through to `rank_empire_ruler_male: "Emperor"` (`:56`). **"Emperor Daozong."**

This is the same machinery that already renders CHI as **"Great Sòng"**: CHI is
`rank_empire`, `court_language = northern_mandarin_dialect`, `country_name = "CSO"`
(measured in the mod's built `10_countries.txt`, CHI block at line 26238).
Two Chinese-style empires side by side, styled identically, which is exactly
what 1066 looked like from the inside — the Chanyuan settlement made them
formal equals.

**What happens if you get the court language wrong.** Drop
`court_language = jin_language` and branch `:92` fails (`kharchin_culture`'s own
`mongolian_language` declares **no `family` line at all** —
`VAN/in_game/common/languages/00_mongolia.txt:1-8`). Then branch `:117` fires on
`country_rank = rank_empire` → `"$PREFIX$ $ADJ$ $RANK$"`, and the NAME key goes
**silently dead**, exactly the horde trap CLAUDE.md warns about. The map would
read `Khitan Empire` (PREFIX empty, `$ADJ$` = `LIA_ADJ`, `$RANK$` =
`rank_empire` = "Empire") and any later edit to `LIA:` would do nothing with no
error. That is a perfectly acceptable *second-best* render — but it must be
chosen, not stumbled into. OPEN DECISION 4.

**LIA must NOT be a steppe horde.** Two independent reasons, both hard:
1. `tools/build_setup.py:4780-4790` — `_bad_recip` dies with
   `"steppe-horde recipients forbidden"` for any grant/transfer recipient whose
   block resolves to `type = steppe_horde`, in-block or through an include.
   LIA is a grant recipient of 161-310 locations.
2. The horde branch (`country_name_construction.txt:100`) precedes
   `prefix_adjective_rank` and kills the NAME key, giving **"the Great Khitan
   Horde"** — which is both ugly and wrong. The Liao minted coin, ran an
   examination system, built the Fogong pagoda in 1056 and called itself a
   dynasty. `far_east_asia_monarchy` is the right template.

### F.3 What XIA will render as

`rank_kingdom` + monarchy + `mahayana`. The kingdom branch list
(`country_ranks.txt:938-1252`) has no East-Asian non-Jurchen, non-Japanese,
non-Vietnamese, non-Korean branch, so it falls through to
`rank_kingdom: "Kingdom"` (`government_names_l_english.yml`). Name construction:
`:92` needs `rank_empire` (fails), `:100` needs horde (fails), `:117`'s first
alternative needs `rank_empire` (fails) and none of its tag/reform alternatives
apply → falls to `country_name_construction_prefix_rank_of_name` (`:184`).

**The map will read something of the form "the Kingdom of Xià", ruler "King".**

That is historically **wrong** — Yuanhao proclaimed himself emperor (皇帝) in
1038 and the Song refused the title, which was the whole content of the 1044
Qingli settlement [U]. The honest options are (a) accept "Kingdom", (b) make
XIA `rank_empire` too, which drags in the `rank_empire_dynasty` branch and
renders **"Great Xià"** — 大夏, again the state's own name — or (c) the
`country_ranks.txt` whole-file override that is already parked for SEL and the
Karakhanids (CENTRAL-ASIA-PACKAGE OPEN DECISION 1). **Recommendation: (b)** —
see OPEN DECISION 1. Note that `rank_empire` also has a diplomatic consequence:
`tributary.txt:8-11` gates `visible` on
`country_rank_level >= scope:target.country_rank_level`.

### F.4 Formable-country interaction — checked

Two vanilla formables cover this ground and neither is consumed:

- **`MCH_f`** (`VAN/in_game/common/formable_countries/00_formable_countries.txt:3421-3446`)
  — Manchuria, `level = 3`, `required_locations_fraction = 0.5`, areas
  `liaodong lower_amur middle_amur songhua songnen ussuri`,
  `potential = { culture ?= { has_culture_group = culture_group:jurchen_group } }`.
  LIA's `kharchin_culture` is `mongolian_group` + `steppe_group`, **not**
  `jurchen_group`, so LIA can never form MCH. Correct: the Jin conquest is the
  Jurchen tribes' story, not the Liao's.
- **`MGO_f`** (`:3644-3665`) — Mongolia, `level = 3`,
  `required_locations_fraction = 0.85`, `regions = { mongolia_region }`,
  `potential = { culture = { has_culture_group = culture_group:mongolian_group } }`.
  `kharchin_culture` **IS** `mongolian_group`. So a Liao that holds 85% of
  `mongolia_region` could form MGO and become "Mongolia". Tier A holds **0%**
  of `mongolia_region` (all five circuits are north_china/manchuria); Tier B
  holds 149/213 = **70%**, still under the gate. **Tier C is what would push it
  over** — a third reason to leave the western steppe empty.
- `MGE_f` (the Mongol Empire, `:3520-3618`) requires `owns = location:karakorum`
  plus eight other capitals worldwide and a Borjigin ruler or a steppe-horde
  government. Unreachable.

---

## G. Diplomacy (`build_diplomacy`)

### G.1 The 47-line Manchurian bloc — the cheapest correct move in the package

`MOD/main_menu/setup/start/12_diplomacy.txt` carries **354 dependencies**, of
which **88 have `first = CHI`**. Classified by where the subject's land is:

| class | count | locations | tags |
|---|---|---|---|
| **purely `manchuria_region`** | **47** | **87** | SYG + 46 Jurchen/Tungus tribal tags: `AAR AID ASU BAY DLA EJI FLN FUT FUY GIL HIJ HNC HOT HRO HUI HUR ILU IMN ITU JHT JUS LAL LLU MAH MIC MRE MUH NAL NEM NEY NRO SHI SIR SMN SNC SUI TAS TOD TOX USS WEJ WEK WUY YRN YIM YOO` |
| Korea-region-touching | 4 | 20 | SSG 6, HIY 7, HLN 5, TMN 2 |
| holding nothing (auto-strip) | 8 | 0 | `DUR EVK NVK ORC ORQ SIB UDE ULC` |
| elsewhere (Tibet, Sichuan, the south, the tusi web) | 29 | — | — |

**In 1066 not one of those 47 was a Chinese subject.** Liaodong was the Liao
Eastern Capital circuit and the "wild Jurchen" of the Songhua and the Ussuri
paid tribute to the Liao, not to Kaifeng [U]. The Song's writ did not cross the
Wall at all.

**Recommendation: repoint `first = CHI` → `first = LIA` for the 46 tribal
tags** (SYG's line dies automatically once SYG is landless — the landless-dep
auto-strip, `docs/HANDOFF.md:474-479`), and change `subject_type = vassal` →
`tributary`. That single sweep:

- makes the Liao look like the Liao — a Chinese-style court with a tribal
  periphery paying in furs and horses — for the price of one loop;
- removes 47 lines of "the Song rules Manchuria" from the diplomacy file;
- costs nothing in new content.

**But it needs the tributary gate.** `VAN/in_game/common/subject_types/tributary.txt:8-24`:
`visible` requires (a) `country_rank_level >= scope:target.country_rank_level`
— satisfied, LIA at `rank_empire` outranks every tribal tag — AND (b) one of
`government_type = steppe_horde` (LIA is a monarchy, fails) /
`scope:target = { government_type = government_type:tribe }` (**likely true for
the Jurchen tags — must be measured, their includes were not read here**) /
`scope:target = { government_type = steppe_horde }` / `modifier:allow_tributary_subject = yes`.

If the tribal tags are `type = tribe`, branch (b)#2 passes and **no reform is
needed**. If any are not, LIA needs the khutba-pattern reform:

```
# The Liao periphery. tributary.txt:19-24 requires the overlord to be a
# steppe horde, the subject a tribe/horde, or the overlord to carry
# modifier:allow_tributary_subject. Same construct and same reason as
# seljuk_khutba_reform (in_game/common/government_reforms/zz_1066_reforms.txt:28),
# whose model is vanilla's malian_tribute_system
# (in_game/common/government_reforms/country_specific.txt:3917).
liao_ordo_reform = {
	potential = {
		tag = LIA
	}
	allow = {
	}

	country_modifier = {
		allow_tributary_subject = yes
		government_reform_slots = 1
	}

	years = 4
}
```
plus `liao_ordo_reform` / `liao_ordo_reform_desc` loc rows (the harness sweeps
every mod reform for both — `docs/HANDOFF.md:588`). Cheap insurance;
recommend shipping it regardless, since it costs one reform slot back and
guarantees the 46 lines survive.

### G.2 The Chanyuan question — modelled or not?

**The history, stated precisely.** The Treaty of Chanyuan (1005) ended the
Liao's invasion of the Song. Its terms: the Song court paid the Liao **100,000
taels of silver and 200,000 bolts of silk annually**, raised in 1042 to 200,000
taels and 300,000 bolts; the two emperors addressed each other as **brothers**
(兄弟之國), with seniority by generation rather than by state; the border was
fixed and both sides forswore fortification of it [U on the exact figures,
firm on the structure]. In 1066 the payment has been flowing for 61 years and
neither court regards it as tribute — the 1042 renegotiation was fought
entirely over whether the Chinese character used would be 納 ("submit") or 贈
("present") [D on the detail, the dispute is well attested].

**So: is CHI a tributary of LIA?** Mechanically it is expressible.
`dependency = { first = LIA second = CHI subject_type = tributary }` would pass
`tributary.txt:8-11` if LIA is `rank_empire` (equal rank suffices —
`country_rank_level >= target`), and pass `:19-24` via `liao_ordo_reform`.

**Recommendation: DO NOT model it.** Four reasons, in order of weight:

1. **It inverts the fiction the treaty was written to preserve.** Both courts
   spent 120 years insisting they were equals. A subject arrow on the map from
   Linhuang to Kaifeng says the opposite of what either party said, and the
   player sees the arrow, not the footnote.
2. **CHI is the leader of the restored Middle Kingdom IO.** The instance is
   live in the current build (`MOD/main_menu/setup/start/15_international_organizations.txt:165`,
   `type = middle_kingdom`). Making the Son of Heaven a foreign power's
   tributary while he is `leader = CHI` of the tianxia system is a collision
   between two models of the same world, and the interaction —
   `only_leader_country_joins_defensive_wars`
   (`VAN/in_game/common/international_organizations/middle_kingdom.txt:46-53`),
   the celestial-authority variables, `demand_silver_tribute` — is unmeasured
   and would need a launch to characterise.
3. **The AI would act on it.** A tributary tie is not decoration: it constrains
   war, diplomacy and annexation. The Song under an AI Liao overlord in 1066 is
   a materially different game from the historical stalemate.
4. **The right tool exists and is not this one.** The Chanyuan payments are a
   *situation* — a recurring transfer with a renegotiation crisis in 1042's
   shape, a war trigger if either side refuses, and the Song's chronic
   fiscal-drain debate. That is `docs/SITUATION-SPECS.md` material, and the
   project already holds itself to an "HYW/G&G/MR-class richness" bar for
   situations (user memory, 2026-07-30).

**Ship instead:** nothing at all in `12_diplomacy.txt` between LIA and CHI, and
a note in `docs/SITUATION-SPECS.md` that the Chanyuan system is banked. If the
user wants something visible immediately, the minimal honest gesture is a
mutual non-aggression/alliance-adjacent relation rather than a subject tie —
but even that needs the relation types checked, which this pass did not do.

### G.3 Xia's own subjection [D]

Western Xia was formally a **Liao** vassal — Liangzuo's father married a Liao
princess and Liangzuo himself took one; the Xia rulers received Liao investiture
[U] — while *also* being formally a Song tributary under the 1044 Qingli
settlement, and while the Liao invaded Xia in 1044 and 1049 [U]. Three
incompatible formal relationships at once is normal for the period and
unmodellable as a single arrow.

**Recommendation: XIA independent, no dependency in either direction.** Same
reasoning as the QRK/QRA decision (CENTRAL-ASIA-PACKAGE OPEN DECISION 4):
"modelling them as independent equals is the safe reading". If a tie is wanted,
`dependency = { first = LIA second = XIA subject_type = tributary }` is the
better-attested of the two and rides `liao_ordo_reform` for free — OPEN
DECISION 9.

### G.4 The Korean frontier — measured, and the answer is "no touch"

The brief asks whether KOR's extent needs adjusting at the Yalu. **It does
not.** Measured against `definitions.txt` and both country files:

- `gwanseo_area` (21, the Yalu side): KOR holds 20 of 21 including **`uiju`**
  (Uiju, at the Yalu mouth), **`gwiju`** (Kwiju — where Gang Gam-chan destroyed
  the Liao army in 1019 [U]), `jeongju_jeongju`, `sakju`, `seonju`. SSG holds
  `yangam`. This is precisely the frontier the Six Garrison Settlements
  established after the Goryeo-Liao wars.
- `gwanbuk_area` (18, the northeast): KOR holds only **4** — `gapsan`, `samsu`,
  `jangjin` and (in `gwanseo`) the Ch'ŏngch'ŏn line. The rest is HIY 7
  (`musan gyeongseong buryeong gilju myeongcheon onseong heoryeong`), HLN 3
  (`hamheung dancheon bukcheong`) and SSG 5 — **Jurchen tribal tags**, all
  `jurchen_culture` templates. That is exactly right: Goryeo did **not** hold
  northeastern Korea in 1066. Yun Kwan's Nine Fortresses campaign is 1107 [U].
- KOR's one location across the Yalu is **`linjiang_jurchen`** (Línjiāng,
  `liaodong_area / dingliao_province`, `jurchen_culture`, `shamanism`). The
  `_NORTH_RULES` list above **subtracts it** (`minus_singles`) so Goryeo keeps
  its bridgehead. Defensible either way — the Liao held Poju on the east bank
  and Goryeo wanted it back for a century [U] — but taking one location off an
  already-correct Korea to make a border 1% tidier is not worth a decision.

**Verdict: KOR is left entirely alone.** Vanilla's 1337 Goryeo is, by accident,
a good 1066 Goryeo, and item 32 already seated Munjong
(`tools/build_setup.py:270`). The only KOR-adjacent change in this package is
that `CHI → SSG/HIY/HLN/TMN` (4 vassal lines, 20 locations) become
questionable — those are Jurchen and Tamna, not Chinese subjects. **Flagged,
not fixed**: HIY/HLN belong with a Korea pass, and Tamna (Jeju) was a *Goryeo*
tributary in 1066 [U], which is a KOR-side item.

---

## H. Left alone deliberately

| what | why |
|---|---|
| **The 46 Jurchen/Tungus tribal tags and their 62 locations** (`songhua_area` 22, `ussuri_area` 28, `songnen_area` 5, plus HIJ) | The single most 1066-correct thing on the eastern map. The "wild Jurchen" were a tribal patchwork under nominal Liao tribute, not a state — vanilla modelled them exactly that way and item 32 did not touch them. This package repoints their *overlord* (§G.1) and takes not one location. |
| **`middle_amur_area` (50) and `lower_amur_area` (42), currently unowned** | The Wuguo and Nivkh country of the lower Amur, outside any state's administration in 1066 [U]. Empty is correct; they contribute to the pop-line class and that is the honest price. A future Amur/Siberia pass can fill them. |
| **Tier C — `western_gobi_area` 32, `mongolian_great_lakes_area` 21, `tuva_area` 11** | Naiman, Merkit, Oirat, Kyrgyz — no state, no capital, no attested 1066 ruler. The Pecheneg/Kipchak discipline (`docs/HANDOFF.md:950-955`). Also the `MGO_f` guard (§F.4). |
| **`xining_province` (6) — Qingtang / Tsongkha** | A real 1066 polity (the Gusiluo line's Tibetan kingdom, Song ally, Xia's western enemy) that vanilla gives to CHI and that deserves its own tag, not annexation by Xia. Flagged for a Tibet/Amdo pass, not fixed here. |
| **`shaanxi_area` (65) and the rest of `hexi_area` (26: Yan'an, Qingyang, Pingliang, Jingzhou, Jingning, Guyuan, Jiazhou)** | The Song's Shaanxi circuits — CHI's, correctly. The 1060s Song-Xia war was fought *over* this line, not across it; Xia raided it and did not hold it [U]. Jiazhou (Fuzhou, the Zhe family's) and Guyuan are the two arguable ones — OPEN DECISION 8. |
| **`longyou_area`'s seven small tags** (MNZ 5, KHG 4, TAZ 3, HEZ 2, BIR 1, JIZ 1, SNP 1) | Amdo Tibetan and Salar ground on the Gansu-Tibet seam; a Tibet-pass matter. |
| **KOR entirely** (§G.4) | Measured correct. |
| **The Middle Kingdom IO's member list** | Restored by item 32 and holding. This package adds no member and removes none; LIA and XIA are outside the tianxia by construction, which is the point. If the user later wants them inside as `cefeng` participants, that is an IO surgery, not a setup one. |
| **The Chanyuan payments** (§G.2) | Situation material, banked. |
| **Pops, cultures and religions everywhere in this theater** | Separate phase by user decision (`docs/HANDOFF.md:1047-1050`). Note for that phase: `linhuang` and the whole Supreme Capital circuit template as `mongolian_culture` + `tengri`; `beiping_area` is 100% `mahayana` and reads as fully Chinese; `datong_area` is `tengri` 20 / `sanjiao` 11 — the Liao's own dual society is already in the pop data, which is a gift. |

---

## I. THE MECHANISM QUESTION — answered by measurement, and the answer is "no new code path"

The brief asks how unowned→owned grants should work, notes that
`_remove_owned_many` asserts exactly one owner per granted location, and asks
for a prescription. **The prescription is: change nothing in the mechanism.**
Here is the measurement that settles it.

### I.1 What `_remove_owned_many` actually enforces

`tools/build_setup.py:4570-4579`:
```python
    def _remove_owned_many(s, locs, ctx):
        idx = _ownership_index(s, set(locs))
        bad = [f"{l}({len(idx.get(l, []))})" for l in locs
               if len(idx.get(l, [])) != 1]
        if bad:
            sys.exit(f"{ctx}: ownership occurrences != 1 for {bad[:8]}")
```
`!= 1` — so **zero occurrences fails just as hard as two**. Granting a location
with no owner would die with `"LOCATION_GRANTS[LIA]: ownership occurrences != 1
for ['linhuang(0)']"`. That much of the brief's premise is exactly right.

### I.2 Why it never arises: the build reads VANILLA, every run

`tools/build_setup.py:6376` in `main()`:
```python
        src = open(os.path.join(VAN, rel), encoding="utf-8-sig").read()
```
Every target file is rebuilt from **pristine vanilla**, not from the previous
build's output. The mod's `10_countries.txt` is a pure function of vanilla plus
the rule tables. **"Unowned" is a property of the OUTPUT, never of the INPUT.**

The order inside `build_countries` is fixed and matters:

| step | line | what |
|---|---|---|
| 1 | `:4814` | `_landless_claims` snapshot — every `LANDLESS_AFTER` tag's **vanilla** holdings |
| 2 | `:4822` | `LOCATION_TRANSFERS` → `_remove_owned_many` |
| 3 | `:4827` | `NEW_COUNTRIES` blocks inserted |
| 4 | `:4834` | `LOCATION_GRANTS` → `_remove_owned_many`, then write into the target's `own_control_core` |
| 5 | `:4886` | `LOCATION_VACATED` → resolve `(name members) ∩ _owned_by(src, tag)` **after** the grants, then `_remove_owned_many` |
| 6 | `:4918` | claims written from the step-1 snapshot |

**Measured, for every location this package touches: all 358 are owned in
vanilla.** Zero `=UNOWNED=` across `beiping_area`, `datong_area`, `yanbei_area`,
`liaodong_area`, `xiliao/taoer/chol`, all six Tier B areas and all ten XIA
provinces. (`songhua_area` and `ussuri_area` have vanilla-unowned members, but
this package takes nothing from either.) Every grant therefore hits a location
with exactly one owner and `_remove_owned_many` passes.

### I.3 The three consequences the implementer must handle

1. **`LOCATION_VACATED_EXPECT` must shrink** — §E.4, exact numbers. This is
   **self-asserting**: forget one and the build dies at `:4894-4897` with the
   resolved and expected counts printed. That is the mechanism working, not
   failing.
2. **The vacate/grant disjointness assert (`:4898-4902`) will NOT fire.** It
   tests the *resolved* vacate list against `_list_owner`; since the granted
   locations were already removed from the tag at step 4, they are absent from
   `got` at step 5. No conflict by construction.
3. **The eight hordes keep their claims over the ground LIA takes.** The
   snapshot at step 1 runs before the grants, so `HCN`, `QAS`, `BGT`, `OTC`,
   `CRS` and `BAT` still write `our_cores_conquered_by_others` lists covering
   locations that now belong to the Liao. **This is correct and it is the
   package's best free feature**: the eight Chinggisid brother/son hordes end up
   with standing claims on a Liao-held eastern steppe, which is precisely the
   1206 rise the deferred Mongol situation will dramatise. The grant machinery
   strips granted locations only from the **target's** claims
   (`:4854-4872`), never from anyone else's.

### I.4 When a new code path WOULD be needed, and what it should look like

Only if a future slice wants to grant one of vanilla's **7,334 genuinely
ownerless locations** (measured: 7,334 in vanilla, 8,100 in today's build; the
766-location difference is what the vacates so far have emptied). If that day
comes, the minimal correct change is a per-list opt-in, not a relaxation of the
assert:

```python
# tag -> locations that may be granted WITHOUT a prior owner. Vanilla
# ships 7334 ownerless ownable locations; a grant into one of them has
# nothing to remove, and _remove_owned_many's exactly-once assert is
# right to refuse by default.
LOCATION_GRANTS_UNOWNED_OK = {}
```
consumed by splitting the step-4 loop into `[l for l in locs if l not in
LOCATION_GRANTS_UNOWNED_OK.get(t, ())]` for the removal and the full `locs` for
the write, with an added assert that every opted-in location **is** ownerless
(so a vanilla patch that gives it an owner fails loudly rather than
double-writing). **Do not build this now.** It is dead code for this package
and every check in this repo that scanned zero items for weeks started as
something reasonable that nothing exercised.

---

## OPEN DECISIONS

**1. XIA's rank: `rank_kingdom` or `rank_empire`?**
`rank_kingdom` renders "the Kingdom of Xià" / "King", which contradicts the
1038 proclamation the whole Qingli war was fought over. `rank_empire` +
`court_language = northern_mandarin_dialect` puts XIA on the same
`rank_empire_dynasty` branch as CHI and LIA and renders **"Great Xià"** (大夏)
with "Emperor" — the state's own name and title, for free, no override.
**Recommendation: `rank_empire`.** The counter-argument is scale: 48 locations
is a small empire and three empires in a row across north China may read as
title inflation. Against that, the Song, Liao and Xia genuinely all claimed the
imperial title simultaneously — that *is* the eleventh century — and EU5
already tolerates it (vanilla ships `rank_empire_horde` on tiny hordes).

**2. LIA's Mongolian reach: Tier A only, or A+B?**
Tier A (161) is the Five Capitals and their circuits — indisputably Liao,
indisputably administered. Tier B adds 149 locations of eastern steppe the Liao
claimed and garrisoned but did not administer [U]. **Recommendation: take
A+B.** Three reasons: the alternative leaves 149 locations of *empty* steppe
between the Liao and nothing, which is a worse lie than nomad suzerainty
rendered as ownership; it is where 173 of the 174 pop-line reductions live
(§E.6); and it stays under `MGO_f`'s 0.85 gate at 70%. Tier A alone is the
conservative answer and costs only 3 constant moves instead of 7.

**3. `kharchin_culture` as LIA's `culture_definition`, or invent `khitan_culture`?**
Vanilla has no Khitan culture and `kharchin_culture` is the closest real
descendant, already painted on 15 of `yanbei_area`'s locations. Inventing one
means a new file under `in_game/common/cultures/`, a `map_khitan` colour, a
culture-group assignment, and the standing question of whether
`culture_definition` even matters for a *landed* tag
(`docs/HANDOFF.md:986-988`, still unanswered in game).
**Recommendation: `kharchin_culture` now**, and bank `khitan_culture` for the
pop phase, where it would actually be visible. This matches the BLH/`bolghar_culture`
and taifa/al-Andalus decisions the user has already made.

**4. LIA's `court_language`: `jin_language`, `northern_mandarin_dialect`, or none?**
Only a `chinese_language_family` court language keeps the `LIA:` NAME key alive
and yields "Great Liáo" (§F.2). `mongolian_language` declares no family at all
and would silently kill the NAME key.
**Recommendation: `jin_language`** — it is the language of the Sixteen
Prefectures the Liao actually ruled, and it keeps LIA visually distinct from
CHI's `northern_mandarin_dialect` while both stay in the family. If the user
prefers the Liao to read as a steppe power rather than a dynasty, omitting
`court_language` gives **"Khitan Empire"**, which is a defensible second-best —
but it must be chosen deliberately, with the dead-NAME-key consequence written
into the comment.

**5. `far_east_asia_monarchy` (sinicized −70) or `east_asia_monarchy` (no sinicized line)?**
`far_east_asia_monarchy` is what CHI/KOR/SYG use, ships
`three_departments_system` and self-satisfies its own gate — zero risk of the
JAP reform-invalid class. But −70 says the Liao was fully sinicized, and the
Liao's whole institutional identity was the dual administration.
**Recommendation: `far_east_asia_monarchy` for the first launch** — the
societal value is a slider a later flavour pass can move with a `FIELD_FIXES`
line, and starting with a template that ships a *valid* reform is worth more
than starting with a philosophically purer one. Revisit after the launch.

**6. XIA's `court_language`: `northern_mandarin_dialect` or `qiangic_language`?**
`liang_culture`, the actual template culture of the Xia core, declares
`northern_mandarin_dialect`. `qiangic_language` is the Tangut language but
declares **no `family`**, so it drops XIA out of the `rank_empire_dynasty` and
`prefix_name` branches — which only matters if OPEN DECISION 1 goes to
`rank_empire`. **Recommendation: `northern_mandarin_dialect` if XIA becomes an
empire** (it is what makes "Great Xià" work), `qiangic_language` if XIA stays a
kingdom (nothing is lost and the flavour is better).

**7. `weiming_dynasty` or `li_dynasty`?**
The clan's own name was Weiming; "Li" was a Tang grant Yuanhao repudiated in
1038 [D], but every English source calls the rulers Li Yuanhao and Li Liangzuo.
**Recommendation: `weiming_dynasty`, loc "Weiming", with the character's
first-name literal left as `Li_Liangzuo`.** The split is how the sources
actually read, and the dynasty name is the one the state used of itself.

**8. Does XIA get `jiazhou_province` (4) and `guyuan_province` (3)?**
Both sit on the contested Song-Xia line. Jiazhou (Fugu, Shenmu) was the Zhe
family's hereditary Song command through the whole period [U]; Guyuan/Zhenrong
was a Song fortified district. **Recommendation: no — leave both with CHI.**
The 48-location Xia is the defensible core; padding it to 55 buys nothing and
loses the "the Song held the ridge, the Xia held the plain" shape that makes
the 1067 Suizhou affair legible. Recorded so it is not re-derived.

**9. Any Liao→Xia tributary tie?**
Xia was formally a Liao vassal *and* a Song tributary *and* fought both [U/D].
**Recommendation: none — XIA fully independent.** The QRK/QRA precedent
(CENTRAL-ASIA-PACKAGE OPEN DECISION 4) is that independent equals is the safe
reading when the formal relationships contradict each other. If a tie is
wanted, `first = LIA second = XIA subject_type = tributary` is the
better-attested direction and rides `liao_ordo_reform` at zero extra cost.

**10. Yizong dies in 1067 — leave it, or move him?**
Li Liangzuo dies at 20, roughly fourteen months after `START_DATE` [U]. CHI's
Yingzong dies in January 1067 (`tools/build_setup.py:269` comment). So two of
north China's three thrones turn over inside sixteen months, into a Xia
regency for the infant Bingchang and the Song's Shenzong — who brings Wang
Anshi. **Recommendation: leave both, and say so in the comment.** It is the
truth, it is dramatic, and the engine handles succession. The alternative
(seating Bingchang early) would be inventing history to avoid an event the
game is built to run.

**11. Does `linjiang_jurchen` stay with KOR?**
One location across the Yalu. The draft leaves it with Goryeo via
`minus_singles`. **Recommendation: leave it** — Goryeo's extent is otherwise
measured-correct (§G.4) and a one-location border tidy is not worth the
attention.

**12. The 4 Korea-region CHI vassals (SSG, HIY, HLN, TMN — 20 locations).**
Jurchen tribes of the Korean northeast plus Tamna/Jeju. Not Chinese subjects in
1066 [U]; HIY/HLN arguably Liao-adjacent, TMN a Goryeo tributary.
**Recommendation: out of scope — flag for a Korea pass.** Named here so the
next session does not re-discover them.

---

## Implementation checklist

Ordered so each step can be verified before the next.

1. **Registry** — two blocks appended to
   `in_game/setup/countries/zz_1066_new_countries.txt` (§A). Registry count
   51 → 53.
2. **Colours** — `map_LIA`, `map_XIA` in
   `main_menu/common/named_colors/zz_1066_map_colors.txt`, commented in the
   file's existing style, key-name-checked against vanilla (§A).
3. **Localisation** — 4 tag rows + 6 character/dynasty rows in
   `main_menu/localization/english/1066_norman_conquest_l_english.yml`, one
   physical line each, UTF-8 **with** BOM (loc files keep theirs).
4. **`_GENERATOR_OK`** — add `"LIA"`, `"XIA"` to `tools/verify_mod.py:924` with
   a tier-4 comment, or author CoA blocks. The check at `:957-960` fails
   otherwise.
5. **Dynasties** — `yelu_dynasty`, `weiming_dynasty` into
   `main_menu/setup/start/04_zz_1066_dynasties.txt` (§D). **NO BOM.**
6. **Characters** — two `NEW_CHARACTERS` entries (§C).
7. **`HISTORICAL_RULERS`** — two 4-tuple entries (§C). The build already
   asserts each character exists, is ≥ `ADULT_AGE`, and accedes between birth
   and `START_DATE` (`tools/build_setup.py:63-67`).
8. **`NEW_COUNTRIES`** — two blocks (§B). Read
   `east_asia_monarchy_no_coast.txt` in full first and restate anything it
   omits, the taifa `_no_coast` lesson (`tools/build_setup.py:565-571`).
9. **`_NORTH_RULES` + resolution loop** — modelled on the Central Asia loop at
   `tools/build_setup.py:4647-4658`: resolve, assert the exact count, assign
   into `LOCATION_GRANTS`, then assert each capital is in its own resolved list.
10. **`NORTH_LANDLESS = ("SYG",)`** into `LANDLESS_AFTER` (§E.3).
11. **`LOCATION_VACATED_EXPECT` moves** (§E.4) — **in the same commit**, and
    per CLAUDE.md **observe each one failing first** by moving the constant
    without the grant.
12. **Diplomacy** — the 46-line `first = CHI` → `first = LIA` repoint plus
    `vassal` → `tributary` (§G.1), with an exact-count assert. SYG's line
    auto-strips.
13. **`liao_ordo_reform`** into
    `in_game/common/government_reforms/zz_1066_reforms.txt` + 2 loc rows (§G.1).
    Assigned via `reforms = { liao_ordo_reform }` in LIA's `government` block.
14. **Harness** — raise `min_count` on the registry, colour, dynasty and
    character checks by the counts this slice adds, per CLAUDE.md's
    raise-`min_count`-as-content-lands rule.

**Break-tests owed** (a check never seen failing is untested): (a) a bogus
location in `_NORTH_RULES` must abort; (b) an off-by-one `expected` must abort
with the resolved count printed; (c) removing `"SYG"` from `NORTH_LANDLESS`
must produce a landless tag with no claims — verify the landless verifier
catches it *before* the game does; (d) each moved `LOCATION_VACATED_EXPECT`
must abort when left at its old value.

## Expected constant moves, collected

| constant | file:line | from | to (Tier A + XIA) | to (Tier A+B + XIA) |
|---|---|---|---|---|
| `LOCATION_VACATED_EXPECT["CHI"]` | `build_setup.py:1363` | 198 | **193** | **113** |
| `LOCATION_VACATED_EXPECT["HCN"]` | `:1368-1376` | 21 | **12** | **delete** |
| `LOCATION_VACATED_EXPECT["OTC"]` | `:1368-1376` | 23 | **13** | **8** |
| `LOCATION_VACATED_EXPECT["QAS"]` | `:1368-1376` | 19 | 19 | **delete** |
| `LOCATION_VACATED_EXPECT["BGT"]` | `:1368-1376` | 17 | 17 | **delete** |
| `LOCATION_VACATED_EXPECT["CRS"]` | `:1368-1376` | 37 | 37 | **24** |
| `LOCATION_VACATED_EXPECT["BAT"]` | `:1368-1376` | 18 | **17** | **14** |
| registry blocks | `zz_1066_new_countries.txt` | 51 | **53** | **53** |
| `NEW_COUNTRIES` count | `build_setup.py:443` | current | **+2** | **+2** |
| `LANDLESS_AFTER` | `:2161` | current | **+1 (SYG)** | **+1 (SYG)** |
| locations granted | build report | current | **+209** | **+358** |
| locations vacated | build report | current | **−25** | **−174** |

---

## Verification statements

Per CLAUDE.md's say-what-you-verified rule.

- **Verified — the resolver.** An independent reimplementation of
  `_parse_defs` (`tools/build_setup.py:689`), `_ownable_set` (`:713`),
  `_resolve_ruleset` (`:756`) and the `OWN_KEYS`/`COUNTRY_RE` reader
  (`:4543`/`:4401`) reproduced **all nine** shipped
  `LOCATION_VACATED_EXPECT` constants exactly (CHI 198, CRS 37, QAS 19,
  BAT 18, BGT 17, KHD 16, HCN 21, OTC 23, OGE 18). That is the known
  positive every count in this document rests on.
- **Verified — `linhuang` exists**, `location_names_l_english.yml`,
  `linhuang: "Línhuáng"`, resolved to
  `asia / east_asia / manchuria_region / songnen_area / xiliao_province`,
  ownable, template `mongolian_culture` + `tengri`, vanilla owner OTC.
- **Verified — `yanbei_area` is not the Sixteen Prefectures.** Its six
  provinces are `daning chaoyang quanning shangdu xingzhou xinghe`; the
  Sixteen Prefectures resolve to `beiping_area` (48) + `datong_area` (36).
- **Verified — no Khitan content in vanilla.** Zero country tags, zero
  cultures, zero dynasties, zero `map_khitan`; exactly three English loc
  strings, all descriptive prose (`artists_l_english.yml:1107`,
  `culture_groups_l_english.yml:75`,
  `events/DHE/flavor_mch_l_english.yml:118`).
- **Verified — `mi_niah_culture` is the Tangut culture**,
  `VAN/in_game/common/cultures/east_asia.txt:1525`, comment
  `#https://en.wikipedia.org/wiki/Tangut_people`, `color = map_tangut`
  (`VAN/main_menu/common/named_colors/02_map.txt:2434`), and it is placed on
  **zero** locations in `location_templates.txt`.
- **Verified — `kharchin_culture`**, `east_asia.txt:2802`,
  `language = mongolian_language`, groups `mongolian_group` + `steppe_group`.
- **Verified — LIA and XIA are free**, by word-boundary AND substring scan,
  over both the vanilla tree and the mod repo, zero hits in all four scans.
  **Verified — TNG is TAKEN**: `TNG = { #Toungoo }`,
  `VAN/in_game/setup/countries/south_east_asia.txt:143`; `TNG: "Toungoo"`,
  `country_names_l_english.yml:3680`. KTN, TGT and ORD likewise taken.
- **Verified — the name-construction chain.**
  `country_name_construction.txt:92-98`
  (`localization_key = country_name_construction_prefix_name`, trigger
  `country_rank ?= country_rank:rank_empire` +
  `court_language ?= { language_family ?= language_family:chinese_language_family }`)
  precedes the horde branch at `:100` and the adjective branch at `:117`;
  `government_names_l_english.yml` gives
  `country_name_construction_prefix_name: "$PREFIX$ $NAME$"` and
  `rank_empire_dynasty_prefix: "Great"` (`:97`), reached via
  `country_ranks.txt:482`. Hence **"Great Liáo"** with a live NAME key.
- **Verified — `rank_empire_jurchen` exists at `country_ranks.txt:365`** and
  fires on `culture ?= { has_culture_group = culture_group:jurchen_group }`,
  which `kharchin_culture` is not.
- **Verified — `mongolian_language` declares no `family`**
  (`VAN/in_game/common/languages/00_mongolia.txt:1-8`), and
  `qiangic_language` declares none either (`00_china.txt:1043`; the last
  `family` line in that file is `burmic_language_family` at `:1024`).
- **Verified — `far_east_asia_monarchy`** sets
  `sinicized_vs_unsinicized = -70` and `reforms = { three_departments_system }`,
  and that reform's `potential`
  (`VAN/in_game/common/government_reforms/country_specific.txt:2142-2159`)
  is satisfied by `societal_value:sinicized_vs_unsinicized < -60` — so the
  template self-satisfies and opens no reform-invalid class.
- **Verified — the tributary gate**,
  `VAN/in_game/common/subject_types/tributary.txt:8-11` (rank) and `:19-24`
  (horde / tribe / `modifier:allow_tributary_subject`).
- **Verified — `MCH_f`** (`00_formable_countries.txt:3421-3446`, jurchen_group
  gate) and **`MGO_f`** (`:3644-3665`, mongolian_group, 0.85 of
  `mongolia_region`); Tier B is 149/213 = 70%.
- **Verified — the build reads vanilla every run**, `tools/build_setup.py:6376`,
  `src = open(os.path.join(VAN, rel), encoding="utf-8-sig").read()`; the
  grants-before-vacates order at `:4834` then `:4886`; the vacate resolution
  against post-grant holdings at `:4893`; the `_landless_claims` snapshot
  before both at `:4814`; and `_remove_owned_many`'s `!= 1` assert at `:4572`.
  **Measured: all 358 locations this package touches are owned in vanilla.**
- **Verified — the capital-strip guard exempts fully landless tags**,
  `tools/build_setup.py:5361`, `if held and capm.group(1) not in held`. No
  donor in this package needs a `CAPITAL_FIXES` entry.
- **Verified — `SYG`'s registry block** is
  `VAN/in_game/setup/countries/east_asia.txt:20-26` with
  `culture_definition = korean_culture`, `map_SYG = rgb { 50 170 50 }`
  (`02_map.txt:2087`) — the reason SYG is a poor reskin target for a Khitan
  empire (changing that field means a whole-file override of a 2,217-entry
  vanilla registry).
- **Verified — the Manchurian dependency bloc**: 88 `first = CHI` dependencies
  in the built `12_diplomacy.txt`, of which 47 have all their land inside
  `manchuria_region` (87 locations, SYG + 46 tribal tags), 4 touch
  `korea_region`, and 8 hold nothing at all.
- **Verified — Goryeo's frontier**: KOR holds 20 of `gwanseo_area`'s 21
  including `uiju` and `gwiju`, but only 4 in `gwanbuk_area`, the rest being
  HIY/HLN/SSG `jurchen_culture` tags — i.e. vanilla's Goryeo already stops
  where 1066 Goryeo stopped.
- **Verified — the Middle Kingdom instance is live** in the current build,
  `MOD/main_menu/setup/start/15_international_organizations.txt:165`,
  `type = middle_kingdom`.
- **NOT verified, and stated as such:** every date, reign, treaty term and
  polity extent carrying `[U]` or `[D]` — the Liao Five Capitals' foundation
  years, Daozong's and Liangzuo's birth and accession days, the Chanyuan
  figures and the 1042 renegotiation, the Zubu relationship, Xia's simultaneous
  Liao and Song subjections, the Song-Xia border of the 1060s, Goryeo's Liao
  tributary status, and the Weiming/Li surname question. Those rest on the
  agent's own history and need a source before they enter setup data.
- **NOT checked, and owed before implementation:** the `government_type` of the
  46 Jurchen tribal tags (§G.1 — decides whether `liao_ordo_reform` is required
  or merely insurance), and a full read of
  `VAN/main_menu/setup/templates/east_asia_monarchy_no_coast.txt` for omitted
  fields (§B).
