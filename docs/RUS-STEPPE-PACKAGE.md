> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF items 28 and 31 (Tier 1 +
> the Cumans, landed 2026-08-01).** Research record, not the state — the
> landing and deviations live in HANDOFF items 28/31; code and HANDOFF win.

# THE RUS LANDS AND THE PONTIC STEPPE — research package (DRAFT)

**STATUS: DRAFT pending main-session review.** Nothing here has been written
into the repo. Produced by an Opus research pass, 2026-07-30. Format follows
`docs/ITALY-NORTH-PACKAGE.md`. Every structural claim carries a `file:line`;
every historical claim without a hard anchor carries `[U]` (unverified detail)
or `[D]` (genuinely disputed in the sources).

Paths: `VAN` = `E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live — `in_game/map_data/definitions.txt` present, 10,559 lines).
`MOD` = this repo. Line numbers in `10_countries.txt` are the MOD's generated
file unless prefixed `vanilla`.

---

## 0. THE THEATER AT A GLANCE

This is the **inverse of the France slice and the twin of Byzantium, at larger
scale**: the rulers are nearly free, the territory is the entire job.

**Measured current state** (my own resolver over `definitions.txt` +
`10_countries.txt`, ownership read from the ten `OWN_KEYS`
`tools/build_setup.py:3403-3406`):

| fact | number |
|---|---|
| ownable locations in the theater's 40 areas | **1278** |
| tags holding land inside `ruthenia_region` / `russian_region` / `steppes_region` / `moldavia_area` / `wallachia_area` | **~60** |
| of those, tags that did not exist in 1066 | **essentially all but five** |
| GLH (Golden Horde, est. 1240s) total holdings | **731** — 289 in `steppes_region`, 115 in `russian_region`, 15 in `ruthenia_region`, 7 in `moldavia_area` |
| vanilla Rurikid characters alive AND aged 16+ on 1066.9.15 | **exactly 6** |
| of those, already seated by the mod | **5** |

**The five thrones are already correct and CLOSED** — verify, touch nothing:

| tag | line | ruler | holdings now |
|---|---|---|---|
| KIE | `10_countries.txt:38242` | `kie_iziaslav_rurikovich`, term :38271 | 74 |
| NOV | `:1734` | `nov_mstislav_izyaslavich_rurikovich`, term :1774 | 171 |
| CHR | `:2234` | `kie_sviatoslav_ii_rurikovich`, term :2250 | 15 (incl. `taman`) |
| POK | `:37896` | `pok_vseslav_bryachislavich_rurikovich`, term :37906 | 11 |
| PYS | `:58820` | `kie_vsevolod_rurikovich`, term :58823 | 5 |

**Headline of the whole package:** the Rus principalities of 1066 need **no new
tags at all**. Vanilla ships HAL (Halych), VOL (Volhynia), SMO, TUV, PNK, RYA,
MRM, RSO, SZL, VLR, TVE, PSK, MOS and ~40 more — but every one of them is a
12th–14th-century construct. The correct 1066 move is the *opposite* of
inventing: **41 vanilla tags go LANDLESS with claims** (the ZTA / giudicati /
Byzantium shape) and the five seated realms absorb their patrimonies.

Proposed Tier 1 moves **492 locations** and leaves:
KIE 74→**200**, NOV 171→**208**, PYS 5→**135**, CHR 15→**128**, POK 11→**56**.

---

## A. REGISTRY ADDITIONS (`in_game/setup/countries/zz_1066_new_countries.txt`)

**Tier 1 needs NONE.** Every Tier-1 recipient already has an identity block:
KIE `VAN/in_game/setup/countries/poland.txt:75`, POK `:85`,
NOV `VAN/in_game/setup/countries/russia.txt:1`, CHR `:190`,
PYS `MOD/in_game/setup/countries/zz_1066_new_countries.txt:11`.

**Tier 2 needs exactly one, and only if the Cuman decision goes that way:**

```
CUM = {	#The Cumans (Polovtsy) — the Pontic steppe
	color = map_CUM
	color2 = rgb { 61 8 81 }

	culture_definition = cuman_culture
	religion_definition = tengri
}
```

- `CUM` freeness verified three ways: zero rows in
  `VAN/main_menu/localization/english/country_names_l_english.yml`; zero
  `^CUM =` in every file of `VAN/in_game/setup/countries/`; zero whole-word
  hits across `VAN/main_menu/setup/start/10_countries.txt`. **Re-run all three
  before writing** (the project rule).
- `cuman_culture` is real — `VAN/in_game/common/cultures/tartar.txt:16`,
  `language = kipchak_language` `:17`. It is placed on **zero** locations in
  the 1337 map, which is exactly what a `culture_definition` is for.
- `tengri` is real — `VAN/in_game/common/religions/folk_asian.txt:992`.
- `color2 = rgb { 61 8 81 }` is the shared steppe secondary used by every
  entry in `VAN/in_game/setup/countries/steppes.txt` (CRI `:12`, NOG `:22`,
  ATR `:31`, GAZ `:67`).
- `map_CUM` is NEW → add to `MOD/main_menu/common/named_colors/zz_1066_map_colors.txt`
  (the PYS precedent, `:7`). Neighbours to check against: KIE/PYS blue,
  `map_PYS` hsv360 {190 55 65}, BYZ purple, GLH's `map_golden_horde`.
  Suggested: a dry ochre-brown, e.g. `rgb { 168 138 78 }` — verify absent
  from vanilla `02_map.txt` first.
- Loc rows in `MOD/main_menu/localization/english/1066_norman_conquest_l_english.yml`
  (the file that carries `PYS: "Pereiaslav"` at `:76`):
  `CUM: "Cumania"` / `CUM_ADJ: "Cuman"`.
- Harness: add `CUM` to `tools/verify_mod.py:922 _GENERATOR_OK` (tier-4
  no-heraldry ground — the Cumans had none) **or** author arms; the check at
  `:942-945` fails a new registry tag that has neither. Raise the
  `coat of arms references resolve` `min_count` (currently 94, `:964`) by the
  number of registry rows added.

---

## B. NEW_COUNTRIES BLOCKS (`tools/build_setup.py:383`)

**Tier 1: none.** Tier 2, conditional:

```
"CUM": """\tCUM = {
\t\town_control_core = {
\t\t\t<resolved at build time — see §E Tier 2>
\t\t}

\t\tstarting_technology_level = 3
\t\tinclude = "expl_eastern_europe"
\t\tinclude = "eurasian_tribe"
\t\tcapital = izium
\t\tcountry_rank = rank_duchy
\t}
"""
```

### THE STEPPE-HORDE TRAP, WORKED OUT

The brief asks this be confronted with the naming consequence cited. It is,
and the answer is that **the Cumans must NOT be a `steppe_horde`, and there is
a fully attested alternative.**

1. **The trap is real.** `VAN/in_game/common/customizable_localization/country_name_construction.txt`
   is ONE first-match-wins list (`country_flavor`, lines 1–2556; the next
   top-level block is `country_flavor_prefix` at `:2557`). Its horde branch:
   ```
   100			localization_key = country_name_construction_prefix_name_horde
   101			trigger = {
   102				government_type = government_type:steppe_horde
   103			}
   ```
   Vanilla's own GLH shows the consequence: `GLH: "Jochi"` is the NAME key, and
   what the map actually reads is `GLH_horde: "Golden Horde"`
   (`country_names_l_english.yml:208-210`).
2. **`tribe` is NOT trapped.** The same 187-line-relevant list contains
   **exactly one** `government_type` branch besides republic/monarchy/horde —
   there is **no tribe branch at all** (`grep government_type` returns
   `:7, :26, :82, :102, :136, :142` only). This is the same measurement the
   British slice already banked: `tools/build_setup.py:3528-3532`, "the
   original assert also banned tribes as a cautious generalization; the
   British slice MEASURED it… and the landed Gaelic tribes render their names
   in game (LEI 'Leinster', batch-tested)."
3. **The build assert allows it.** `tools/build_setup.py:3571-3573` forbids
   only `steppe_horde` recipients. Tribes are legal recipients and the whole
   Irish pass is grants to them.
4. **The template exists and fits.** `VAN/main_menu/setup/templates/eurasian_tribe.txt:2`
   `type = tribe`, `:3` `heir_selection = tribal_oldest_male`, `:19`
   `parliament_type = assembly`, `:23` `marriage_law = polygyny` — a Tengri
   nomad confederation described exactly. 27 vanilla tags use it
   (SMI KVE TAV SVO KRL BJA OBD PLY BAK KND BGJ KOD SVA KZY LYA TBY SLK BRT
   HGO KMG SAK ALT CNR DZK LEK RUT TBA); the orthodox variant
   `eurasian_orthodox_tribe.txt` is what vanilla gives ALN (Alania,
   `10_countries.txt:55219`) and KIP (`:55088`).
5. **The five horde templates, for the record** (all `:2`):
   `eurasian_horde.txt`, `eurasian_horde_not_present.txt`,
   `eurasian_horde_no_coast_no_pleading.txt`, `eurasian_horde_no_muslim.txt`,
   `eurasian_horde_no_muslim_no_protected_faith.txt`. Nothing else in
   `VAN/main_menu/setup/templates/` carries `type = steppe_horde`.
6. **Discovery is mandatory.** `eurasian_tribe.txt` supplies no `expl_*`.
   Without one the country cannot see its own capital —
   `initialize_from_bookmark.cpp:528`, the SEL lesson
   (`docs/KNOWLEDGE.md:1507-1513`). `expl_eastern_europe` is what KIE/PYS use
   (`10_countries.txt:38267`, `:58830`); `expl_mongols` is what CRI/NOG/ATR
   use (`:3777`, `:3809`, `:3835`). **Recommend `expl_eastern_europe`** — the
   Cumans of 1066 came from the Volga, not from Mongolia, and eastern Europe
   is where their capital sits.
7. **Capital.** Sharukan does not exist on the map (`sharukan` returns zero in
   `definitions.txt`; `torchesk`, `tmutarakan`, `cherson`, `vyshhorod` are
   likewise NOT FOUND). `izium` (`definitions.txt:1564`, `izium_province` of
   `sloboda_ukraine_area`) is the Donets crossing at the traditional site of
   Sharukan's winter camp [U]; `zmiiv` (`:1566`) is the alternative
   identification. Either is defensible; neither is attested as a *town* in
   1066 — this is the honest weakness of the whole Cuman option.

---

## C. RULERS

### C.1 The complete vanilla supply — this is the whole list

Test applied to all 273 Rurikid-or-Rus-prefix characters in
`VAN/main_menu/setup/start/05_characters.txt`: `birth_date <= 1050.9.15` and
(`death_date` absent or `> 1066.9.15`). **Six pass. Five are seated.**

| # | key | name key | birth | death | culture | age | file:line |
|---|---|---|---|---|---|---|---|
| 1 | `kie_iziaslav_rurikovich` | `name_iziaslav` | 1024.2.5 | 1078.10.3 | polesian_culture | 42 | `05_characters.txt:94223` |
| 2 | `kie_sviatoslav_ii_rurikovich` | `name_svyatoslav` | 1027.1.1 | 1076.12.27 | ruthenian | 39 | `:94607` |
| 3 | `pok_vseslav_bryachislavich_rurikovich` | `name_vseslav` | 1029.1.1 | 1104.4.24 | polatskian_culture | 37 | `:93485` |
| 4 | `kie_vsevolod_rurikovich` | `name_vsevolod` | 1030.2.1 | 1093.4.13 | ruthenian | 36 | `:94619` |
| 5 | `nov_mstislav_izyaslavich_rurikovich` | `name_mstislav` | 1045.1.1 | 1069.1.1 | polesian_culture | 21 | `:94240` |
| 6 | **`tuv_yaropolk_izyaslavich_rurikovich`** | `name_yaropolk` | 1047.1.1 | 1086.11.22 | polesian_culture | **19** | **`:94254`** |

Near-misses, for the record (alive, under 16, so unseatable):
`kie_sviatopolk_ii` b.1050.11.8 — **misses by 54 days** (`:94284`);
`kie_oleg_of_chernigov` 14 (`:94680`); `kie_vladimir_ii` Monomakh 13
(`:94631`); `smo_davyd_igorevich` 11 (`:95123`); `hal_borys_vyacheslavich` 10
(`:95095`); `dru_roman_vseslavich` 6 (`:93502`); `hal_rurik_rostislavich` 5
(`:94035`); `mis_gleb_vseslavich` 4 (`:93516`); `hal_volodar_rostislavich` 3
(`:94049`); `pok_rogvolod_vseslavich` 2 (`:93643`);
`vbk_sviatoslav_vseslavich` and `hal_vasilko_rostislavich` both b.1066.1.1.

**This is why the whole Rus of 1066 is five states.** There is nobody else to
seat. Every junior prince of the real 1066 — Gleb Sviatoslavich, Yaropolk,
Rostislav's sons — is either a child, a placeman with no principality, or dead.

### C.2 The sixth man — Yaropolk Iziaslavich, TUV

The only unused adult. **Recommendation: DO NOT SEAT.** In 1066 Turov was
Iziaslav's own patrimony held directly; Yaropolk receives Volhynia in 1069 and
Turov c.1073 [U]. Seating him three-to-seven years early buys a sixth flag at
the cost of the package's cleanest historical claim. Recorded as an OPEN
DECISION because a sixth Rurikid state is a visible, cheap gain if the user
wants it.

### C.3 THE TMUTARAKAN QUESTION — resolved by vanilla's own data

The brief flags Rostislav Vladimirovich seizing Tmutarakan 1064-66 and dying
"Feb 1067, poisoned by the Chersonites". The dating is **[D] genuinely
disputed** — the PVL's 6574 with a 3 February day resolves to 1066 under one
reckoning and 1067 under the other, and modern references split.

**Vanilla takes the 1066 reading and writes it down:**
`05_characters.txt:94020 vol_rostislav_vladimirovich_rurikovich`,
`birth_date = 1038.1.1`, **`death_date = 1066.2.3`**, culture
`halychian_culture`, tag VOL. That death date is BEFORE `START_DATE`
(1066.9.15), so the mod's death-date strip (`tools/build_setup.py:1743-1745`,
which removes only POST-start death dates) leaves it intact and Rostislav
starts **dead**.

**Consequence: the existing `CHR: ["taman"]` grant is CORRECT and needs no
change.** `tools/build_setup.py:760` already says so — "Tmutarakan was
Chernihiv's appanage (Gleb Sviatoslavich restored 1066)". Under vanilla's
chronology Gleb is back in Tmutarakan by September 1066 and it is Sviatoslav
II's. A TMU tag (id verified free by the southern-Italy pass,
`docs/HANDOFF.md:948`) would need Rostislav alive, which contradicts the
character database. **Recommendation: leave `taman` with CHR, record the [D],
close the item.** Listed as an OPEN DECISION only so the user can overrule
vanilla if they prefer the 1067 reading.

### C.4 Name keys — the trap list (relevant only if characters are ever authored)

Name keys are declared by a **loc row**, in
`VAN/main_menu/localization/english/character_names_dynamic_l_english.yml`
(4,343 base `name_*` keys). `in_game/common/languages/` holds only reference
*pools*. Rendering is per `name_KEY.<language|dialect>`.

**Eight Rus first names do NOT exist under their obvious key:**

| you would write | vanilla's actual key | the row that renders it | loc line |
|---|---|---|---|
| `name_vladimir` / `name_volodymyr` | **`name_waldemar`** | `.ruthenian_language: "Volodymyr"` | `:17877` |
| `name_rurik` / `name_riurik` | **`name_roderick`** | `.east_slavic_language: "Rurik"` | `:15095` |
| `name_yuri` | **`name_george`** | `.east_slavic_language: "Yuriy"` | `:7775` |
| `name_vasilko` | **`name_basil`** | `.ruthenian_language.diminutive: "Vasylko"` | `:3069` |
| `name_rogvolod` | **`name_reginald`** | `.east_slavic_language: "Rogvolod"` | `:14873` |
| `name_sviatoslav` | **`name_svyatoslav`** (y, not i) | base `:16612` | `:16612` |
| `name_vyacheslav` | **`name_wenceslas`** | `.east_slavic_language: "Vyacheslav"` | `:18102` |
| `name_andrei` | **`name_andrew`** | `.east_slavic_language: "Andrei"` | `:1730` |

Note also `name_sviatopolk` IS spelt with `i` (`:16600`) while
`name_svyatoslav` is spelt with `y` — vanilla is inconsistent and both must be
copied exactly. Present under their obvious keys: `name_iziaslav` `:9549`,
`name_mstislav` `:12921`, `name_vseslav` `:17819`, `name_vsevolod` `:17823`,
`name_yaroslav` `:18798`, `name_yaropolk` `:18795`, `name_rostislav` `:15255`,
`name_oleg` `:13471`, `name_gleb` `:8028`, `name_boris` `:3688`,
`name_igor` `:9373`, `name_volodar` `:17809`, `name_briachislav` `:3814`
(spelt `-chislav`), `name_roman` `:15173`, `name_david` `:5410`.

**Cosmetic gap already live:** `name_vseslav` (`:17819-17821`) and
`name_vsevolod` (`:17823-17825`) have **no `.ruthenian_language` row**, so
Vseslav (polatskian → belarusian_dialect) and Vsevolod (ruthenian →
ruthenian_language) fall back to the plain English base string. Harmless;
worth one line in the launch tour.

**All ten steppe names are MISSING**: `Sharukan Bonyak Tugorkan Sokal Iskal
Kegen Tyrach Osen Bagubars Altunopa` — zero rows, zero substring hits in the
dynamic loc file. `kipchak_language`'s pool
(`VAN/in_game/common/languages/00_steppes.txt:8-19`) is almost all raw
literals with empty `dynasty_names` (`:37`) and `lowborn` (`:39`). So a Cuman
khan needs either a raw literal (`first_name = { name = Sharukan }` — vanilla's
own escape hatch, `05_characters.txt:91540 first_name = { name = Vasilko }`)
or an invented key (the proven route: `name_guislabert`, the taifa three).
**Recommendation: do NOT author a Cuman khan at all** — no 1066 Cuman leader
is attested well enough to name. `ruler = random` is the honest value, and it
is what the Sardinian ARB/GAL and Corsican COR already do.

---

## D. DYNASTIES

**No new dynasty is needed.** `rurikovich_dynasty` ships in vanilla:

```
4180		rurikovich_dynasty = {
4181			name = { name = name_roderick }
4182			dynasty_name_type = patronym
4183			home = novgorod
4184		}
```
(`VAN/main_menu/setup/start/04_dynasties.txt:4180-4184`.)

**There are NO branch houses.** Grep of `04_dynasties.txt` for
`rurik|monomakh|olgovich|iziaslav|vseslav` returns exactly that one line. All
263 Rurikid characters share the single key. `polotsk_dynasty` exists
(`:8173-8176`, `home = polotsk`) but is filed under the file's `#Lithuania`
comment and worn by no Rurikid — **do not repurpose it**;
`pok_vseslav_bryachislavich_rurikovich` is a `rurikovich_dynasty` member
(`05_characters.txt:93485`).

`MOD/main_menu/setup/start/04_zz_1066_dynasties.txt` contains no Rurikid entry
and needs none.

---

## E. TERRITORY

Delivered as **rule sets**, not raw lists — the `_resolve_ruleset` /
`_byz_target` machinery (`tools/build_setup.py:693`, `:725`) resolves
area/province names against `definitions.txt` at build time and asserts an
exact count. Every count below was produced by an independent resolver that
reimplements `_parse_defs` + `_ownable_set` (`:626`, `:650`); the
implementation must reproduce them or STOP.

### E.1 The historical frame — Yaroslav's testament and the triumvirate

Yaroslav the Wise died 1054.2.20 (`05_characters.txt:93986`, matching every
seated ruler's accession date in `HISTORICAL_RULERS`). His partition, and the
two deaths that reshaped it:

| son | got | 1066 status |
|---|---|---|
| Iziaslav I (b. 1024) | **Kyiv + Turov + Novgorod's overlordship** | senior triumvir; also holds Volhynia and the Cherven towns after Rostislav's flight |
| Sviatoslav II (b. 1027) | **Chernihiv + Murom-Ryazan + Tmutarakan + the Vyatichi** | second triumvir |
| Vsevolod I (b. 1030) | **Pereiaslavl + Rostov + Suzdal + Beloozero + the upper Volga** | third triumvir — the famous split realm, Dnieper *and* Zalesye |
| Viacheslav (b. 1036) | Smolensk | **died 1057** (`05_characters.txt:95081`, `death_date = 1057.1.1`) |
| Igor (b. 1037) | Volhynia, then Smolensk 1057 | **died 1060** (`:95109`, `death_date = 1060.1.1`) |

After 1060 **Smolensk had no prince**: the three brothers divided Igor's
inheritance and ruled it in common until Vladimir Monomakh received it
c.1073-78 [U]. **Volhynia** likewise reverted to Iziaslav once Rostislav
Vladimirovich fled to Tmutarakan in 1064; Yaropolk receives it only in 1069
[U]. **Halych does not exist**: the town is first mentioned 1141 [U], and
Rostislav's sons get Peremyshl and Terebovlia in 1084/1092, confirmed at
Liubech 1097. **Polotsk is at war with the triumvirate** — Vseslav sacked
Novgorod in 1066/67 and is defeated on the Nemiga 1067.3.3 and imprisoned
1067.7 [D on the exact 1066 vs 1067 split].

That frame yields **five states, no more**, and it is what the rule sets below
encode.

### E.2 TIER 1 — the Rus core (RECOMMENDED, self-contained, 492 locations)

Format matches `_FRANCE_RULES` (`tools/build_setup.py:1148`):
`tag: (sweeps, singles, minus_sweeps, minus_singles, expected_total)`.
`expected_total` is the **resolved sweep size**, i.e. the tag's final holding
inside these areas; the *grant list* is that minus what the tag already owns.

```
"KIE": (["right_bank_ukraine_area",     # Kyiv itself, the Ros, Cherkasy, Ovruch
         "volhynia_area",               # Igor's, reverted to Iziaslav after 1060
         "red_ruthenia_area",           # the Cherven towns, Rus since 1031
         "polesia_area",                # Turov-Pinsk, Iziaslav's own patrimony
         "smolensk_area",               # princeless 1060-73, held by the triumvirs
         "mazyr_province", "rechytsa_province",
         "kletsk_province", "slutsk_province"],   # southern Black Ruthenia
        [], [], [], 192)                # gains 149, final 200
"CHR": (["severia_area",                # Chernihiv, Novhorod-Siverskyi, Starodub, Bryansk
         "ryazan_area",                 # Murom-Ryazan, the testament's grant
         "oka_area",                    # the Vyatichi, Chernihiv's tributaries [D]
         "kursk_province"],             # the one Rus outpost on the steppe edge
        [], [], [], 127)                # gains 115, final 128
"PYS": (["left_bank_ukraine_area",      # Pereiaslavl proper
         "suzdal_area", "vladimir_area",
         "yaroslavl_area", "beloozero_area",
         "moscow_area"],                # Merya/Vyatichi forest; Moscow founded 1147
        [], [], [], 135)                # gains 131, final 135
"NOV": (["east_novgorod_area", "west_novgorod_area",
         "tver_area",                   # Torzhok is Novgorod's; Tver founded 1135
         "totma_area"],                 # the Zavolochye tribute land
        [], [], [], 123+)               # gains 52, final 208
"POK": (["white_ruthenia_area"],        # Polotsk, Vitebsk, Minsk, Drutsk, Orsha
        [], [], [], 56)                 # gains 45, final 56
```

**Measured donors** (mine, reproducible):

| recipient | gains | drawn from |
|---|---|---|
| KIE | 149 | VOL 37, HAL 31, SMO 29, LIT 13, VYA 9, SSK 7, PNK 6, TUV 6, TPS 4, VBK 2, CHR 2, PYS 1, FMB 1, KCH 1 |
| CHR | 115 | GLH 31, KCH 14, NSL 12, RYA 11, BRY 9, PRK 8, MRM 7, NVS 5, KIE 4, STS 4, TRS 4, MSV 3, TRB 1, RYL 1, KZK 1 |
| PYS | 131 | MOS 26, BLO 23, KIE 19, NOV 15, KOS 9, VLR 8, SZL 7, YAR 7, RSO 4, SKY 3, UGL 3, MOG 3, DMI 2, YRV 1, VYA 1 |
| NOV | 52 | RSO 15, PSK 12, ZUB 5, KAS 4, RZH 4, ORE 3, TVE 3, KLN 2, GLM 1, VYT 1, +2 |
| POK | 45 | LIT 20, VBK 13, MSV 9, DRU 3 |

**No location in any list is currently unowned** — verified; the grant
machinery never has to invent an owner. (`arkhangelsk_area` holds 31 unowned
locations and `pomorye_area` 8; both are deliberately left out of NOV's sweep
so nothing changes there.)

### E.3 RUS_LANDLESS — 41 tags

```
RUS_LANDLESS = ("BLO","BRY","DMI","DRU","FMB","KAS","KCH","KLN","KOS","KZK",
                "MOG","MOS","MRM","MSV","NSL","NVS","PNK","PRK","PSK","RSO",
                "RYA","RYL","RZH","SKY","SMO","SSK","STS","SZL","TPS","TRB",
                "TRS","TUV","TVE","UGL","VBK","VLR","VOL","VYA","YAR","YRV",
                "ZUB")
```
All keep their registry identity; the build's own machinery converts their
former holdings into `our_cores_conquered_by_others` (the Byzantium slice's
snapshot-at-build-time route, `docs/HANDOFF.md:451`). Every one of them is a
12th–14th-century principality whose claim list becomes exactly the future the
1066 start is supposed to be reaching toward — Smolensk's 1125 principality,
Moscow's 1147 foundation, Tver's 1135, Pskov's 1348 independence, Halych's
1141 and Volhynia's Romanovich revival. **This is the ZTA/giudicati law
running in the other direction and it is the elegant part of the slice.**

Tags that SHRINK but keep land (all correct — the remainder sits outside the
theater or belongs to another package):
HAL 41→10 (podolian remainder, Tier 2), GLH 731→700, LIT 103→70 (Baltic
package), ORE 5→2, GLM 12→11, VYT 20→19.

### E.4 TIER 2 — the Pontic steppe (the OPEN DECISION; 169 / 211 / 305 locations)

Three nested scopes, each a separate yes/no:

```
CUM-core   (169)  yedisan_area zaporizhzhia_area pryazovia_area azov_area
                  sloboda_ukraine_area kursk_area podolia_area crimea_area
                  minus_singles: theodoro lusta soldaia vosporo   (BYZ's, closed)
                                 + all 8 of kursk_province        (CHR's, Tier 1)
                  donors: GLH 149, HAL 10, KIE 8, GAZ 2  →  GAZ empties
CUM-don     (42)  lower_don_area
                  donors: GLH 42
CUM-danube  (94)  moldavia_area wallachia_area
                  donors: WAL 44, IAS 11, BIA 10, BLD 9, GLH 7, SRC 4,
                          HTN 3, HSC 3, SSI 3
                  → WAL IAS BIA BLD SRC HTN HSC SSI all empty (8 tags)
```

Notes that bear on the choice:

- **The steppe locations are real, settled, culture-bearing land**, not
  wasteland. `location_templates.txt` gives `oleshia` `:4548` orthodox/
  ruthenian/wool, `kichkas` `:4559` orthodox/ruthenian/clay, `azok` `:4651`
  sunni/crimean/clay, `qalancaq` `:4553` sunni/crimean. Only the named
  `*_wasteland` / lake / sand-bar tokens are unownable (`crimean_mountains`
  `:4496`, `syvash_sand_bar` `:4509`).
- **Unowned IS mechanically legal** — the built file already contains 31
  unowned locations in `arkhangelsk_area` and 8 in `pomorye_area`. So
  "deliberately empty" is available and costs nothing structurally.
- **But unowned means colonisable.** A 169–305 location hole between Hungary,
  Byzantium and the Rus is an open invitation to AI colonisation from turn
  one. That is the real argument against emptiness here and it did not apply
  to the Pechenegs, who sat *inside* Byzantium's Paristrion.
- **The Cumans are attested on this ground at exactly this date**: first
  contact at Pereiaslavl 1055 (Bolush, peace with Vsevolod), first raid
  1061.2.2 (Sokal defeats Vsevolod), and the disaster on the Alta in September
  1068 that destroys the triumvirate's army and triggers the Kyiv uprising —
  **two years after the start date, with no actor on the map to deliver it.**
  [U] on the individual names; the sequence itself is PVL-solid.
- **What they were NOT**: a state. No capital, no single khan, no succession.
  The project's rule — "a state needs a solid anchor, otherwise deliberately
  empty" — cuts against a tag. The counter-argument is that the anchor here is
  territorial and ethnographic rather than dynastic, and that GLH holding
  Kursk, Voronezh, Bessarabia and the Crimea in 1066 is a **worse** lie than
  an anonymous Cuman tribe holding the same ground.

### E.5 GAZ, and the Crimea seam

`GAZ` = Genoese Gazaria (`10_countries.txt:3882`), `type = republic` `:3893`,
`include = "catholic_republic"` `:3908`, holding `kaffa` (`:3884`) and `tana`
(`:3888`), capital `kaffa` `:3897`, registry
`VAN/in_game/setup/countries/steppes.txt:67` `culture_definition = ligurian`,
`religion_definition = catholic`. Genoese Caffa is founded **1266**.
**GAZ must go landless in any variant** — it is the only unambiguous defect in
the Crimea. Its `dependency = { first = GEN second = GAZ subject_type = vassal }`
(`12_diplomacy.txt:84`) then dies to the existing landless-dep auto-strip.

`FEO` (Theodoro) is already landless with an **empty** `own_control_core`
(`10_countries.txt:3859`) but `capital = theodoro` (`:3870`) — a location BYZ
now owns. Cosmetic, pre-existing, not this slice's to fix; noted so nobody
re-discovers it.

---

## F. FIELD SWAPS AND THE DEFECTS ALREADY ON THE MAP

Seven defects sit in the *already-landed* Rus. Every one is a single-line
`FIELD_FIXES` surgery (`tools/build_setup.py:1573`), the ZTA/CAT shape,
asserted against the exact old text.

### F.1 KIE and POK wear the wrong house

```
10_countries.txt:38290		dynasty = gediminid_dynasty      # KIE
10_countries.txt:37945		dynasty = gediminid_dynasty      # POK
```
Iziaslav I and Vseslav the Sorcerer are on blocks whose ruling house is the
**Gediminids** — the Lithuanian dynasty of the 1300s. Exact ZTA precedent
(`tools/build_setup.py:1581`, `balsic_dynasty` → `vojislavljevic_dynasty`).

```
"KIE": [("dynasty = gediminid_dynasty", "dynasty = rurikovich_dynasty")],
"POK": [("dynasty = gediminid_dynasty", "dynasty = rurikovich_dynasty")],
```

### F.2 NOVGOROD IS A REPUBLIC — the biggest single error

```
10_countries.txt:1766		government = {
              :1767			type = republic
              :1768			heir_selection = veche_selection
              :1769			reforms = {
              :1770				veche_republic
              :1771				merchant_republic
              :1772			}
              :1773			ruler = nov_mstislav_izyaslavich_rurikovich
```
Mstislav Iziaslavich, a Rurikid prince appointed by his father, is currently
the elected head of a merchant republic. The Novgorod veche republic begins
with the expulsion of Vsevolod Mstislavich in **1136**; in 1066 Novgorod is
Kyiv's northern viceroyalty. NOV also carries **no government template
include at all** — only `include = "expl_novgorod"` `:1764` — so everything
comes from that inline block.

This one is bigger than a one-line swap. Recommended shape: replace the
`type`/`heir_selection`/`reforms` triple and let the rest of the inline slider
block stand, or swap the whole inline government for
`include = "russian_principality_no_coast"` (what every other Rus tag uses,
e.g. TVE `:1982`, RYA `:2491`) **plus** a restated `type = monarchy` — because
`russian_principality*.txt` templates contain **no `type =` key at all** (only
`parliament_type = estate_parliament`, `russian_principality.txt:17`), which is
exactly why every mod Russian-principality block writes `type = monarchy`
inline. **Restate-what-you-drop applies; diff the templates before writing.**

Side effect, and a good one: with `type = republic` gone, the
`rank_kingdom_republic_novgorod` / `rank_duchy_republic_novgorod` name branches
stop firing and NOV renders through the Slavic principality branch instead.

### F.3 KIE is only a Duchy — "Grand Principality of Kyiv" is one line away

`10_countries.txt:38291 country_rank = rank_duchy`. The rank word is chosen
first-match in `VAN/in_game/common/customizable_localization/country_ranks.txt`:

- `:1816 rank_duchy_principality_slavic` — trigger `country_rank_is_duchy` +
  `government_type = monarchy` + `culture = { has_culture_group =
  culture_group:russian_group }`. Loc `government_names_l_english.yml:683
  "Principality"`, ruler `:685 "Prince"`.
- `:1136 rank_duchy_grand_principality_slavic` — same trigger but
  `country_rank_is_kingdom = yes`. Loc `:736 "Principality"` **plus
  `:737 rank_duchy_grand_principality_slavic_prefix: "Grand"`** and
  `:739 ..._ruler_male: "Grand Prince"`.

KIE's `culture_definition = ruthenian` (`poland.txt:75`) and `ruthenian` is in
`russian_group` (`VAN/in_game/common/cultures/east_slavic.txt:63`, groups at
`:84-87`). So:

```
"KIE": [("country_rank = rank_duchy", "country_rank = rank_kingdom")],
```
should give **"Grand Principality of Kyiv"** under a **"Grand Prince"** —
which is exactly what Iziaslav was. The CAT precedent
(`tools/build_setup.py:1574`, `rank_duchy` → `rank_county`) is the same
surgery in the other direction.

**Honesty note:** the branch, the trigger, the culture group and all three loc
rows are verified. The *composition* of `$PREFIX$` into the final map name is
**not observed in game**. Treat it as a launch probe: if Kyiv reads
"Principality of Kyiv" the prefix did not compose and the fix is loc-side.
Note that `:1136` also **shadows** `:1227 rank_kingdom_russian_prince`
("Grand Principality", ruler "Grand Prince", `government_names:619-623`) for
any russian_group culture — that branch is effectively dead code and should
not be reached for.

### F.4 Three Rus tags run on a Lithuanian government

```
10_countries.txt:37903	include = "lithuanian_monarchy"   # POK — Vseslav the Sorcerer
              :38222	include = "lithuanian_monarchy"   # SMO
              :38152	include = "lithuanian_monarchy"   # VBK
```
POK is landed and seated; SMO and VBK go landless under Tier 1 so only POK
matters operationally. Swap to `ruthenian_principality_no_coast` (KIE's own,
`:38268`, and the template DOES set `type = monarchy` at
`ruthenian_principality_no_coast.txt:3`). **Diff the two templates and restate
anything `lithuanian_monarchy` provided that the Ruthenian one does not** —
the Welsh trap (`tools/build_setup.py:1603-1612`) is the standing warning.

### F.5 KIE has a Cossack privilege

`10_countries.txt:38278 cossack_identity`, inside KIE's `privilege = { }`
block. The Cossacks are a 15th–16th-century formation; `cossack_culture`
(`east_slavic.txt:133`) is placed on zero locations in vanilla. Strip it.
Low priority, one line, purely cosmetic-plus-modifier.

### F.6 The block header comments

`:38242 KIE = {	#Kyiv - Vassal of LIT`, `:38211 SMO = {	#Smolensk - Vassal of
LIT`, `:37896 POK = {	#Polotsk - Vassal of LIT`. Vanilla's own 1337 framing,
carried through. Cosmetic; fix if the surgery touches the line anyway.

### F.7 Succession — an optional flavour swap, worth one paragraph

`ruthenian_principality_no_coast.txt:4` sets
`heir_selection = cognatic_primogeniture`. The Rus of 1066 ran the **rota** —
lateral seniority among the dynasty, which is precisely what Yaroslav's
testament created and what the triumvirate embodied. Legal alternatives in the
enum (`VAN/in_game/common/government_types/00_default.txt:3-12`):
`partition_inheritance` (4 vanilla uses: `10_countries.txt:9347`,
`german_principality.txt:3`, `german_principality_not_present.txt:3`,
`swiss_monarchy.txt:3`) and `tribal_oldest_male` (277 uses). Neither is exactly
the rota. **Recommendation: `partition_inheritance` on the five Rus tags** —
it is the closest attested value and the mechanical consequence (realm splits
among sons) is the actual history of 1054, 1093 and 1097. Marked OPEN DECISION
because it changes play, not just display. `russkaya_pravda_policy` is already
in the template's `legal_code_law` — vanilla got that part right.

---

## G. DIPLOMACY (`build_diplomacy`, `tools/build_setup.py:4430`)

The theater's ties sit in `MOD/main_menu/setup/start/12_diplomacy.txt:54-100`
and `:223-231`. 482 dependencies total in the file.

### G.1 REMOVE explicitly — the subject stays landed, so the auto-strip misses it

```
:99	dependency = { first = GLH second = KIE subject_type = tributary }
```
**Iziaslav I of Kyiv is currently a tributary of the Golden Horde.** The Tatar
Yoke, 174 years early, live in the built file. This is the single most visible
anachronism in the theater and it must go first.

```
:226	dependency = { first = LIT second = POK subject_type = vassal }
```
Vseslav the Sorcerer as a Lithuanian vassal. Lithuania as a state is
Mindaugas, 1250s.

```
:63	dependency = { first = NOV second = ORE subject_type = vassal }
```
Only if ORE keeps its 2 remaining locations; folding those into NOV empties ORE
and the auto-strip handles it. Prefer the fold.

### G.2 Dies automatically once the subject is landless

`:55-72` (BRY→CHR, BRY→TRB, CHR→NVS, CHR→RYL, CHR→STS, KCH→KZK, LIT→RZH,
NOV→PSK, NZH→GRS, RYA→PRK, SMO→FMB, SMO→MSV, SMO→VYA, TVE→KAS, TVE→KLN,
TVE→ZUB, YAR→MOG), `:84` (GEN→GAZ, under Tier 2), `:97/98/100`
(GLH→BRY/HAL/VOL), `:223-230` (LIT→DRU/NRK/PNK/SSK/TPS/TUV/VBK), and under
CUM-danube the seven `:88-94` GLH→Moldavia tributaries.

**`BRY → CHR` at `:55` deserves a sentence of its own**: vanilla makes
**Chernihiv a vassal of Bryansk**, which for a 1066 file means Sviatoslav II
subject to a town that is first mentioned in 1146. It dies with BRY, but check
it is gone.

**The auto-strip constant will move a long way.** `build_diplomacy`'s
"dependencies naming a landless tag stripped" assert is currently at 112 and
the file's comment records every prior transition being *observed failing*
before the number moved (`tools/build_setup.py` ~:4560). Expect roughly +30
from Tier 1 alone. Follow the ritual: run, watch it fail, move the constant,
record the arithmetic in the comment.

### G.3 Dependencies to KEEP

`:73-82`, NOV's ten Ob-Ugrian tributaries (OBD PLY BAK KND BGJ KOD SVA KZY LYA
TBY). Novgorod's Yugra tribute is recorded from 1032 — these are **right for
1066**, and they are also the reason `docs/KNOWLEDGE.md:1484` names NOV as one
of vanilla's tributary-gate-passing overlords: every subject is a
`eurasian_tribe`, and `tributary.txt:21` passes on the subject's government
type alone. **The Irish law in vanilla's own data.** Leave untouched.

### G.4 ADD — the triumvirate ring (OPEN DECISION)

The historical structure is a collegium: Iziaslav senior, Sviatoslav and
Vsevolod co-equal, Novgorod a viceroyalty held by Iziaslav's own son.

- **KIE → NOV** is genuinely defensible. Mstislav is Iziaslav's placeman, not
  a peer.
- **KIE → CHR and KIE → PYS are NOT defensible as subjection.** The triumvirs
  were partners; representing them as Kyiv's subjects would misstate the one
  thing this theater is actually about.

Mechanics if KIE → NOV is wanted: `vassal` blocks war declarations
(`vassal.txt:80-86` — the class that froze the Norman Conquest) but passes the
gate free. `tributary` is war-capable but the **visible gate binds at game
start** (`government.cpp:3702`, measured, `docs/KNOWLEDGE.md:1474-1488`) and
requires the overlord to be a horde, the subject to be a tribe, or the overlord
to carry `modifier:allow_tributary_subject`. NOV is a monarchy, so a tributary
tie needs a **fifth use of the khutba pattern**:

```
kyivan_seniority_reform = {
	potential = { tag = KIE }
	allow = { }
	country_modifier = {
		allow_tributary_subject = yes
		government_reform_slots = 1
	}
	years = 4
}
```
— exactly `seljuk_khutba_reform`'s shape
(`MOD/in_game/common/government_reforms/zz_1066_reforms.txt:28-41`), assigned
to KIE in setup. Recommendation: **add the reform and the single KIE → NOV
tributary; nothing else.**

### G.5 A war, optionally

Vseslav of Polotsk sacked Novgorod in 1066/67 and was crushed on the Nemiga on
1067.3.3 [D on whether the sack falls before or after 1066.9.15]. `build_wars`
(`tools/build_setup.py:4802`) exists. A triumvirate-vs-Polotsk war at start
would be the single most flavourful thing in the theater — and it is also
exactly the material the situation quality bar (`docs/HANDOFF.md:1118-1127`)
would rather see as a *situation* than as a setup war. **Recommendation: do
not add a setup war; bank "The Sorcerer of Polotsk" as a situation spec.**

---

## H. LEFT ALONE DELIBERATELY — the seams

| ground | why it is not mine | who owns it |
|---|---|---|
| `lower_yik_area` (33), `ural_region`, Volga Bulgaria (`bolghar`, `bilyar`, `cukataw` — no tag exists; `BLG` is **Bologna**, `BUL` is Danube Bulgaria) | east of the Volga, explicitly excluded by the brief | **Central Asia package** |
| `astrakhan_area` (37), `tambov_area` (41), `samara_area` (43) — GLH holds all 121 | the Volga corridor: Saqsin, the Burtas, the Mordvins. West-of-Volga in geography, Volga-basin in politics | **Central Asia package** — recommend it takes them with the rest of GLH |
| `majar_area` (25), `matrega_area` minus `taman` (24) | the North Caucasus. **ALN = "Alania" exists** (`country_names_l_english.yml:4529`, registry `caucasus.txt:165`, `culture_definition = alan_culture`, `religion_definition = orthodox`) and is LANDED with 7 (`10_countries.txt:55207`, `include = "eurasian_orthodox_tribe"` `:55219`). Alania under Durgulel the Great, Bagrat IV's brother-in-law, is a **real 1066 anchor** [U on his exact dates] | **Caucasus package** — flagged as a genuinely seatable throne someone should take |
| `crimea_area` coastal strip — `theodoro lusta soldaia vosporo` | the Cherson theme, granted to BYZ by item 15 (`tools/build_setup.py:682`) | **CLOSED, Byzantium** |
| `taman` | Tmutarakan, CHR's (`tools/build_setup.py:760`) | **CLOSED, see §C.3** |
| north of the Danube, if CUM-danube is declined | `PEC` is banked for a ~1087 situation (`docs/HANDOFF.md:950-955`) | **the Pecheneg situation** |
| `black_ruthenia_area` north — grodno, novogrudok, slonim, vawkavysk (NRK 11, LIT 10) | Yatvingian and Lithuanian ground; LIT keeps 70 after Tier 1 | **Baltic package** |
| `nizhny_novgorod_area` (31) — GLM 12, GLH 8, NZH 6, GRS 6 | Merya/Mari forest; Gorodets 1152, Nizhny Novgorod 1221, Galich-Mersky 1237. Every tag there is an anachronism but nothing in 1066 clearly owns it. Deliberately NOT swept into PYS | revisit with the Volga seam |
| Torks / Oghuz / Berendei on the Ros | **no tag exists** (`TOR` is Torres, Sardinia; `TUR` is the Ottomans). Crushed by the triumvirate in 1060 and settled as federates INSIDE Kyiv — the Pecheneg reasoning exactly. `porossia_province` (`definitions.txt:1466`: `bila_tserkva bohuslav kaharlyk kaniv sherbiv skvyra`) rides with KIE | **flavour/situation material, no tag** |
| `MOL` (Moldavia) | formable only — loc `:755`, formable `00_formable_countries.txt:1622`, **no identity block anywhere**. Would need the PYS registry route | not needed under any variant |
| Pop / culture / religion conversion | separate later phase (`docs/HANDOFF.md:1043-1050`). Note `ryazan` itself is `severian` culture and `ryazanian` sits on ZERO locations; `chernihiv` is `severian`, not `ruthenian` | **pop phase** |

### The identifier traps this theater sets — record these

| looks like | actually is | proof |
|---|---|---|
| `GLC` = Halych | **Spanish Galicia**, García II's, already seated | `iberia.txt:47`, loc `:927`, `10_countries.txt:13097` holds Santiago/Porto/Braga |
| `GLM` = Halych | **Galich-Mersky**, north-east Rus | `russia.txt:155`, loc `:98` |
| Halych's tag | **`HAL`** | `poland.txt:65`, loc `:2927` |
| `VLH` = Volhynia | **does not exist**; Volhynia is **`VOL`** | `poland.txt:58`, loc `:2929` |
| `TUR` = Turov | **the Ottomans**; Turov is **`TUV`** | loc `:1886` vs `:2955` |
| `KIP` = Kipchak | **Kipike**, a Circassian principality | `caucasus.txt:125`, loc `:4445` |
| `ALA` = Alania | **Albaamaha**, Alabama; Alania is **`ALN`** | `eastcoast.txt:96` vs `caucasus.txt:165` |
| `PRZ` = Przemysl | **Peruzzi**, the Florentine bank | loc `:713` |
| `TOR` = Torks | **Torres**, Sardinia, already seated | loc `:694` |
| `BLG` = Volga Bulgars | **Bologna** | loc `:560` |
| `PZL` = Pereiaslav | **Pereyaslavl-Zalessky**, the wrong city | loc `:88`; already recorded `docs/KNOWLEDGE.md:1015` |
| `GLH` = "Golden Horde" | NAME key is **`GLH: "Jochi"`**; the map reads `GLH_horde` | loc `:208-210` — the horde naming law in vanilla's own data |

`CUM`, `KHA` (Khazars), `PEC`, `TMU` and a Volga-Bulgar id are all **free**.

---

## OPEN DECISIONS — every user choice, with a recommendation

**1. Tier 1 as a whole — 492 locations, 41 tags landless.**
> **RECOMMEND: yes, as one slice.** It is self-contained, needs no new tag, no
> new character, no new dynasty and no new colour. It is the largest single
> territory change in the project (Byzantium moved 495 and emptied 45), and
> the machinery it uses is all proven.

**2. Smolensk — SMO landless, `smolensk_area` → KIE?**
> **RECOMMEND: yes.** 1060-1073 Smolensk genuinely had no prince; the
> triumvirs held Igor's inheritance in common. A three-way checkerboard split
> would be literal but unreadable. SMO's 29 locations become its claims — the
> 1125 principality as a stated future. *Alternative: land SMO with
> `ruler = random` as a condominium placeholder (ugly, and invents a state).*

**3. Volhynia — VOL landless, `volhynia_area` → KIE?**
> **RECOMMEND: yes.** Igor left in 1057 and died 1060; Rostislav fled in 1064;
> Yaropolk arrives 1069. In September 1066 Volhynia is administered from Kyiv.

**4. Halych — HAL landless, `red_ruthenia_area` → KIE?**
> **RECOMMEND: yes, emphatically.** Halych town is first mentioned 1141; the
> Rostislavichi get Peremyshl/Terebovlia in 1084/1092 and are confirmed at
> Liubech in 1097. HAL's claim list becomes their inheritance, which is the
> single most satisfying landless conversion in the package.

**5. Turov — TUV landless, `polesia_area` → KIE?**
> **RECOMMEND: yes.** Turov was Iziaslav's own patrimony, held directly.

**6. Seat Yaropolk Iziaslavich on TUV as a sixth Rurikid state?**
> **RECOMMEND: no.** He is the only unused adult Rurikid in the game, aged 19,
> and it is tempting — but he gets Volhynia in 1069 and Turov c.1073, so it
> buys a flag by breaking the package's cleanest claim. *Say the word and it
> is one row in `HISTORICAL_RULERS` plus dropping TUV from `RUS_LANDLESS`.*

**7. THE CUMANS — tag or empty?**
> **RECOMMEND: a `CUM` tribe tag with CUM-core + CUM-don (211 locations),
> `ruler = random`.**
> The naming trap is fully escaped: `eurasian_tribe` gives `type = tribe`,
> `country_name_construction.txt` has zero tribe branches, the build's assert
> bans only `steppe_horde`, and the British slice already measured landed
> tribes rendering their names. The alternative — leaving 211 locations
> unowned — is mechanically legal but hands the Pontic steppe to AI
> colonisation from 1066, and it leaves the Alta disaster of 1068 with no
> actor. *Against: no capital, no khan, no state; `izium` as a capital is [U].*
> *Middle option: CUM-core only (169), lower Don left empty.*

**8. North of the Danube — CUM-danube (94), or empty?**
> **RECOMMEND: empty, and strip WAL + the seven Moldavian boyar tags anyway.**
> Wallachia is 1330 and the Moldavian seats are 14th-century; they are wrong
> under every reading. But Cuman domination of Wallachia/Moldavia is an
> 1080s-1090s fact, not a 1066 one, and `PEC` is already banked for exactly
> this ground (`docs/HANDOFF.md:950-955`). *Cost: a 94-location hole. If that
> reads badly in game, folding it into CUM later is one line.*

**9. `GLH → KIE` tributary — remove?**
> **RECOMMEND: yes, immediately, whatever else is decided.** The Golden Horde
> holding Kyiv in tribute in 1066 is the theater's worst single line and it is
> live right now (`12_diplomacy.txt:99`).

**10. KIE `rank_duchy` → `rank_kingdom` for "Grand Principality of Kyiv"?**
> **RECOMMEND: yes, as a launch probe.** All the pieces are verified
> (`country_ranks.txt:1136`, `government_names_l_english.yml:736-742`,
> `ruthenian` ∈ `russian_group`); the composition is unobserved. If it reads
> "Principality of Kyiv" nothing is lost and we have learned how `$PREFIX$`
> composes.

**11. Novgorod's republic — fix now or bank?**
> **RECOMMEND: fix now.** A Rurikid prince ruling a merchant republic with a
> veche is the second-worst line in the theater and it is on a *seated* ruler.
> Requires a template diff (`russian_principality_no_coast` carries no
> `type =`), so it is the one item that needs care rather than a one-liner.

**12. KIE → NOV as the one dependency, via a `kyivan_seniority_reform`?**
> **RECOMMEND: yes for KIE → NOV; no for CHR and PYS.** Mstislav is his
> father's placeman; Sviatoslav and Vsevolod are not anyone's subjects.
> *Alternative: no ties at all — three independent brothers plus a Novgorod
> that is nominally Kyiv's. Defensible, and cheaper.*

**13. `heir_selection = partition_inheritance` on the five Rus tags?**
> **RECOMMEND: yes.** The rota is what the whole 1054 settlement was, and
> `partition_inheritance` is the closest attested enum value. Flagged because
> it changes play, not display.

**14. Tmutarakan — keep `taman` with CHR (vanilla's 1066 death date) or move
it to a revived Rostislav?**
> **RECOMMEND: keep with CHR, no change.** Vanilla writes
> `death_date = 1066.2.3` on Rostislav (`05_characters.txt:94020`), so under
> the game's own chronology he is dead seven months before the start and Gleb
> Sviatoslavich holds Tmutarakan. Overruling that means editing a vanilla
> character to follow the 1067 reading — possible, but it buys one location.

**15. Delivery — one slice or two?**
> **RECOMMEND: two.** Tier 1 (the Rus core) lands and gets tested on its own;
> Tier 2 (the steppe) follows once the Cuman decision is made and the Central
> Asia package has drawn its Volga line. Tier 1 depends on nothing outside
> itself; Tier 2 shares a donor (GLH) with Central Asia and a border with the
> closed Byzantine Danube.

---

## Implementation checklist (for whoever builds this)

- [ ] Re-run the three CUM freeness greps and cite them in the report.
- [ ] Reproduce all five Tier-1 resolved counts (192 / 127 / 135 / 123+ / 56)
      and the 492 total; STOP on any mismatch.
- [ ] `RUS_LANDLESS` must be exactly 41 tags; assert it.
- [ ] Every `FIELD_FIXES` entry asserted against its exact current line.
- [ ] Diff `lithuanian_monarchy` vs `ruthenian_principality_no_coast` and
      restate anything dropped (POK).
- [ ] Diff NOV's inline government against `russian_principality_no_coast`
      before swapping; `type =` is NOT in that template.
- [ ] Move the landless-dep strip constant only after watching it fail.
- [ ] Raise `min_count` on the CoA / registry checks in `tools/verify_mod.py`
      in the same commit that adds content.
- [ ] `main_menu/setup/start/` files carry **NO BOM**.
- [ ] `python tools/verify_mod.py` and `python tools/build_setup.py --dry-run`
      green before the report.
