> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 36 (commits 5a2977d /
> ef51eb4 / 170c944) — NOT yet game-tested.** Research record, not the
> state. KNOWN DEVIATIONS, code wins: the repoint batch is FOUR (KBR is
> landless in this same slice — §G.2's five was a contradiction); GHA
> resolves 21 (diara AND banamba carved — banamba sat in two grant lists);
> IFA's 14-location residue went Haud->WAR, Mora->AFA, Mudug->AJU;
> CAPITAL_FIXES gained ETH ankober->kubar (§E.4 missed it) and AJU
> merca->kelafo; n_landless_deps is 253, not 252; ZAN is rank_duchy
> (rank_county_muslim does not exist — OWED check 2 settled); Tunka Manin
> IS seated (decision 8, the user's call); and the UNOWNED_GRANTS
> mechanism was born for SNH's nine ownerless locations, which §I did not
> anticipate.

# SUB-SAHARAN AFRICA 1066 — Ghana's world, Christian Nubia, the Zanj coast (DRAFT)

**Research agent model ID: `claude-opus-5`.**

**DRAFT — pending main-session review. Nothing here has been written into any
mod file.** Produced by an Opus research agent, 2026-08-02, against the working
tree at commit `182b09d` (35 items landed, plus the uncommitted
`docs/AUDIT-2026-07-31.md`). Every mechanical claim carries a `file:line`.
Historical claims that no file can settle are flagged `[U]` (unverified /
my own history, no source in the repo) or `[D]` (sources genuinely differ),
never asserted silently. §VERIFICATION collects them.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, 491,179 bytes, present)
`MOD = .../1066 Test Mod`

**Method.** Counts come from an independent reimplementation of
`build_setup.py`'s parsers — `_parse_defs` (`tools/build_setup.py:711`),
`_ownable_set` (`:736`), `_resolve_ruleset` (`:779`), `find_block_end`
(`:4896`) and the `OWN_KEYS`/`COUNTRY_RE` country reader (`:5091`, `:4791`) —
all reading `encoding='utf-8-sig'`, all token/brace based, comments masked
before tokenising.

**Proven on known positives.** The resolver reproduces the Baltic package's
own published figures exactly (`samogitia_area` 16, `courland_province` 8,
`BALTIC-PACKAGE.md:55`, `:853`); the template parser returns
`cult['dadu'] == 'yan_culture'` (the Northern Dynasties known positive, and
the guard against `location_templates.txt`'s single-line blocks); the country
reader finds **2337 blocks in vanilla and 2402 in the mod build**, matching
CLAUDE.md's own "all 2337 country blocks". The tag scanner
(`scratchpad/tagfast.py`) was fed five known tags — `GHA`, `MAK`, `ETH`, `ZAN`
came back TAKEN with their registry `file:line`, and `PRU` came back TAKEN on
99 word hits with an **empty registry**, the formable-only class that
`BALTIC-PACKAGE.md §A.5` records.

**Scope.** Sub-Saharan Africa: `sahel_region`, `guinea_region`,
`nubia_region`, `ethiopia_region`, `somalia_region`, `swahili_coast_region`,
and the Lake Chad edge of `central_africa_region`. Named as flagged seams and
NOT touched: Egypt and its Aswan edge (BKZ/SKN — the Fatimid slice's),
the Maghreb (its own future slice; the MOR/TLE `control` twin is already in
`CONTROL_STRIPS`'s comment, `tools/build_setup.py:1659`), Mamluk MAM
(landless since the Fatimid slice, `:2026`). Measured-but-left-alone:
`kongo_region`, `great_lakes_region`, `madagascar_region`,
`southern_africa_region`, `zimbabwe_region` (§H).

---

## 0. Ground truth — and the four findings that shape the package

### 0.1 THE HEADLINE: vanilla already ships Ghana's world. It just hangs it off the wrong overlord.

`VAN/main_menu/setup/start/12_diplomacy.txt` gives MAL thirteen vassals
(mod file `:249-261`). Read their **NAME keys**
(`VAN/main_menu/localization/english/country_names_l_english.yml`):

| tag | loc line | name | first attested |
|---|---|---|---|
| GHA | `:1321` | **Ghana** | al-Bakri 1068 [U] |
| DFN | `:1319` | **Diafunu** | al-Bakri's Zafun/Zafqu [U] |
| BBK | `:1315` | **Bambuk** | the gold field [U] |
| SGH | `:1325` | **Sanghana** | al-Bakri, at the Senegal mouth [U] |
| TKR | `:1327` | **Takrur** | al-Bakri; War Jabi's conversion c. 1040 [D] |
| TMK | `:1329` | **Tadmekka** | al-Bakri's Tadmakka [U] |
| SON | `:1333` | **Songhai** (Gao/Kawkaw) | al-Bakri's Kawkaw [U] |
| TFK | `:1317` | Tirafka | [D] |
| KBR | `:1311` | Kabura | al-Idrisi [D] |
| ZGH | `:1313` | Zagha | Middle Niger town, Dia [D] |
| BMR | `:1309` | Bambara | **c. 1712 [U]** |
| JOL | `:1155` | Jolof | **c. 1350 [D]** |
| KAB | `:1209` | Kaabu | **c. 1235 [U]** |

**Ten of the thirteen are al-Bakri's polities, writing in 1068.** Vanilla built
the 1337 Sahel out of the eleventh-century sources and then subordinated the
whole set to a Mali that will not exist for 170 years. **The 1066 correction is
therefore mostly a DIPLOMACY correction, not a territory one** — and
`build_setup.py` already owns the exact mechanism: the **repoint**, attested
twice (`:6713-6724`, 46 Jurchen `CHI`→`LIA`; `:6735-6748`, 16 jimi
`LNG`→`CHI`, both with exact-count asserts).

Two more of the same shape, both already in the file:

- `koumbi_saleh`, `aoudaghost`, `diara`, `njimi`, `manan`, `tadmekka`,
  `silla`, `kubar`, `dongola`, `soba`, `axum` and `takedda` are all real
  locations (resolved from `definitions.txt`). The eleventh century's own
  place-names are on this map.
- KBO carries `dynasty = sayfawa_dynasty`, `capital = njimi`, and
  `reforms = { banu_hummay_amendments }` (mod `10_countries.txt`, KBO block) —
  the Sayfawa house and Hummay's own reform. Hummay is c. **1075** [D]. Vanilla
  has modelled a state that begins **nine years after our start date**.

### 0.2 Sub-Saharan Africa is UNTOUCHED ground for this mod

**Measured: `tools/build_setup.py` contains ZERO references to any of
`sahel_region`, `guinea_region`, `nubia_region`, `ethiopia_region`,
`somalia_region`, `swahili_coast_region`, `kongo_region`,
`great_lakes_region`, `madagascar_region`, `zimbabwe_region`,
`southern_africa_region`, `central_africa_region`, or to any of the 197 tags
registered in vanilla's five African registry files.** The only African tags
the build names are `BKZ` (`:2020`, `FATIMID_TRIBUTARIES`) and `FZA`
(Fezzan, whose 13 locations are 12 in `desert_area` and one — `qatrun` — in
`kanem_area`). MOD ownership across every African area is byte-identical to
vanilla.

Registry file sizes (`VAN/in_game/setup/countries/`): `west_africa.txt` 64
tags, `east_africa.txt` 72, `horn_of_africa.txt` 41, `kongo.txt` 14,
`south_africa.txt` 6 — **197 African identity blocks**. Of the 197:

| kind | n | note |
|---|---|---|
| landed at 1337 | 111 | |
| **`type = pop`** | **45** | the stateless-peoples model — KRL's shape, `BALTIC-PACKAGE.md §0.4` |
| landless **with** claims | 39 | vanilla's own `our_cores_conquered_by_others` shells |
| landless with **no** claims | 2 | `DAH` (`west_africa.txt:514`), `KEB` (`:422`, an empty `own_control_core = { }`) |

Two mechanism notes that follow, both new to this project:

1. **Vanilla ships 39 landless-with-claims African tags.** The claim lists
   accept **container names as well as locations** — `SOA`'s is
   `ankober gendebelo nora_eth argobba_province`, `END`'s ends
   `enderta_province`. Nine of them are exactly the tags this package wants to
   land (§C).
2. **A `dependency` may name a `type = pop` country.** ZMW's eight
   "tributaries" (`12_diplomacy.txt:239-246` — KLG TNA SEN TSG MNY ZEZ NBY
   VED) are **all pop countries**, holding no territory. They survive
   `_drop_landless_dep` (`tools/build_setup.py:6756-6765`) because that sweep
   keys on `LANDLESS_AFTER`, not on actual holdings.

### 0.3 Template culture and religion, measured per area (the §0-style table)

Ownable counts resolved from `definitions.txt`; culture/religion from
`location_templates.txt`; owners from `MOD/main_menu/setup/start/10_countries.txt`.

| area | ownable | owners today | template cultures | template religions |
|---|---|---|---|---|
| `ghana_area` | **31** | DFN 11, **unowned 9**, GHA 5, BBK 2, TKR 2, SGH 2 | `soninke` 16, **`lamtuna_culture` 8**, **`godala_culture` 6**, `tuareg` 1 | `sunni` 31 |
| `mali_area` | **31** | MAL 13, BMR 7, GHA 5, DFN 4, BBK 2 | `mandinka` 24, `soninke` 5, `bobo` 2 | `sunni` 31 |
| `timbuktu_area` | **31** | BMR 22, GHA 6, TFK 1, KBR 1, ZGH 1 | `mandinka` 18, `bambara` 6, `dogon` 4, `messufa_culture` 3 | `sunni` 27, `dogon_religion` 4 |
| `gao_area` | **23** | SON 12, unowned 6, TFK 4, TMK 1 | `songhai` 18, `tuareg` 2, `gurma` 2, `mossi` 1 | `sunni` 20, `rogo_miki_religion` 3 |
| `kanem_area` | **24** | KBO 14, unowned 9, FZA 1 | `kanembu_culture` 12, `toubou_culture` 6, `sao_culture` 4, `zaghawa_culture` 2 | `sunni` 18, `sao_religion` 4, `karama_religion` 2 |
| `bornu_area` | **31** | KBO 18, unowned 13 | `kanembu_culture` 18, `adamawa_culture` 8, `tuareg` 4, `sao_culture` 1 | `sunni` 22, `adamawa_religion` 8, `sao_religion` 1 |
| `north_hausa_area` | **20** | ZAM 12, GOB 4, KTS 3, DAA 1 | `hausa` 20 | **`bori_religion` 20** |
| `south_hausa_area` | **21** | ZZZ 6, RAN 5, ZAM 5, KAN 4, KTS 1 | `hausa` 21 | **`bori_religion` 21** |
| `air_area` | 14 | unowned 12, GOB 2 | `tuareg` 12, `hausa` 2 | `sunni` 12, `bori_religion` 2 |
| `zarma_area` | 19 | **unowned 19** | `tuareg` 9, `bariba` 7, `gurma` 3 | `sunni` 9, `isese_religion` 7, `rogo_miki` 3 |
| `east_mossi_area` | 20 | BSM 6, unowned 5, TEN 5, GUR 4 | `mossi` 15, `gurma` 5 | `rogo_miki_religion` 20 |
| `west_mossi_area` | 27 | OUA 16, GWI 6, YAT 5 | `mossi` 16, `gurunsi` 8, `bobo` 2, `senufo` 1 | `rogo_miki_religion` 26, `nyama_religion` 1 |
| `futa_tooro_area` | **19** | TKR 14, BBK 5 | `fulbe` 16, `soninke` 3 | `sunni` 19 |
| `jolof_area` | **22** | JOL 22 | `wolof` 10, `serer` 9, `mandinka` 3 | `geno_religion` 10, `a_fat_roog_religion` 9, `sunni` 3 |
| `gambia_area` | **18** | KAB 16, BBK 2 | `fulbe` 7, `balanta` 4, `jola` 3, `manjak` 3, `mandinka` 1 | `sunni` 8, `nhaala_religion` 7, `emit_religion` 3 |
| `south_manding_area` | 8 | MAL 8 | `mandinka` 5, `dyula` 2, `kissi` 1 | `sunni` 7, `kuru_masaba_religion` 1 |
| `nubia_proper_area` | **21** | MAK 15, BKZ 2, ABW 1, ALO 1, SKN 1, JRN 1 | `nubian` 13, `sudanese_arab` 4, `beja_culture` 4 | **`sunni` 11, `miaphysite` 10** |
| `butana_area` | **24** | ALO 16, unowned 3, BQL 2, ABW 2, NQS 1 | `nubian` 16, `sudanese_arab` 2, `beja_culture` 2, `dinka` 2, `tigre` 1, `gumuz` 1 | **`miaphysite` 18**, `sunni` 3, `muonyjang` 2, `rebba` 1 |
| `darfur_area` | 24 | DAJ 20, ALO 2, unowned 1, MAK 1 | `daju_culture` 11, `nuba` 5, `nubian` 3, `nuer` 2, … | `kalge_religion` 12, `musala_religion` 6, `miaphysite` 2, `sunni` 2, `muonyjang` 2 |
| `equatoria_area` | 23 | **unowned 23** | `dinka` 6, `anuak` 4, `seru` 3, `shilluk` 3, `madi` 3, … | `muonyjang_religion` 17, `ori` 3, `mbori` 3 |
| `northern_ethiopia_area` | **33** | ETH 10, AFA 8, MED 6, BZN 3, QTA 2, JRN 2, DHK 1, BQL 1 | `tigrinya` 16, `afar_culture` 9, `tigre` 5, `kunama` 3 | `miaphysite` 19, `sunni` 11, `anna_religion` 3 |
| `central_ethiopia_area` | **30** | ETH 22, DBE 4, IFA 3, AFA 1 | `amhara` 17, `afar_culture` 6, `agaw_culture` 4, `tigrinya` 2, `harla` 1 | `miaphysite` 21, `sunni` 7, **`judaism` 2** |
| `southern_ethiopia_area` | **32** | ETH 11, unowned 9, ENN 6, HDY 3, DAM 2, DAW 1 | `gonga_culture` 17, `amhara` 5, `gumuz` 5, `harla` 3, `surma` 2 | `omo_religion` 12, `miaphysite` 8, `sunni` 5, `rebba` 5, `muonyjang` 2 |
| `northern_somalia_area` | **27** | IFA 17, WAR 6, TDE 4 | `somali_culture` 27 | `sunni` 27 |
| `inner_somalia_area` | **26** | IFA 13, unowned 4, BLE 3, ETH 2, AJU 2, HRL 1, DAW 1 | `harla_culture` 10, `somali_culture` 9, `oromo_culture` 7 | `sunni` 19, `waaqeffanna_religion` 7 |
| `southern_somalia_area` | **30** | AJU 25, IFA 4, MDI 1 | `somali_culture` 30 | `sunni` 30 |
| `tana_area` | 18 | unowned 11, then LAM/UGW/PTE/AJU/MBA/MLI/GED 1 each | `swahili_culture` 7, `ongamo` 4, `kalenjin` 3, `mbugu` 2, … | `sunni` 7, `maasai` 4, `bantu` 3, `asis` 3, `waaqeffanna` 1 |
| `wami_area` | 22 | unowned 13, ZAN 7, ZZB 1, PEM 1 | `swahili_culture` 9, `seuta` 3, `ruvu` 3, `south_cushitic` 3, … | `bantu_religion` 12, `sunni` 4, … |
| `rufiji_area` | 17 | unowned 12, ZAN 5 | `matuumbi` 9, `ruvu` 4, `bena` 3, `swahili_culture` 1 | `bantu_religion` 14, `sunni` 3 |
| `ruvuma_lurio_area` | 26 | unowned 17, ZAN 9 | `makhuwa` 12, `yao` 10, `chewa` 3, `matuumbi` 1 | **`bantu_religion` 26** |
| `mozambique_area` | 14 | unowned 11, MOZ 1, AGH 1, QLM 1 | `makhuwa_culture` 14 | `bantu_religion` 14 |
| `logone_area` | 18 | **unowned 18** | `sao_culture` 10, `baguirmi` 7, `adamawa` 1 | `sao_religion` 17, `adamawa` 1 |
| `wadai_area` | 10 | DAJ 5, unowned 5 | `bilala` 5, `maba_africa` 2, `tunjur` 2, `masalit` 1 | `kalge_religion` 5, `sunni` 5 |

Four things this table settles:

- **The Hausa location data is already pagan.** All 41 `hausa` locations carry
  `bori_religion` while all seven Hausa **countries** carry
  `religion_definition = sunni` (`west_africa.txt:398-453`). Vanilla's own map
  data disagrees with vanilla's own registry, and the map data is the 1066
  answer.
- **`lamtuna_culture` (8) and `godala_culture` (6) sit inside `ghana_area`.**
  Those are the Sanhaja confederations of the **Almoravid movement** — Yahya
  ibn Ibrahim's Gudala and Abu Bakr ibn Umar's Lamtuna [U]. The western Sahara
  is painted as a distinct people and **nine of its fourteen locations are
  already unowned** (§E.2).
- **`nubia_proper_area` is half Muslim in the template data (11 sunni / 10
  miaphysite)** while `butana_area` is 18/24 miaphysite. That is the 1337
  picture: Dongola fell in 1317 [U] and Alodia had not yet. At 1066 Nubia is
  Christian to the Aswan frontier.
- **The Swahili coast is mostly `bantu_religion`, not `sunni`, in the template
  data** — vanilla already models incomplete Islamisation there, which is a
  1066-correct posture inherited free.

### 0.4 The religions and cultures that already exist — nothing needs authoring

`VAN/in_game/common/religions/folk_african.txt` ships **51 African folk
religions** with line numbers:
`bantu_religion:3`, `bori_religion:57` (Hausa animism), `muonyjang_religion:75`
(Dinka), `waaqeffanna_religion:148` (Oromo/Somali), `kaggen_religion:184` (San),
`akan_religion:220`, `vodun_religion:238`, `isese_religion:274` (Yoruba),
`odinala_religion:310` (Igbo), `a_fat_roog_religion:328` (Serer),
`dogon_religion:346`, **`nyama_religion:364` (Mande)**, `nyesoa_religion:382`,
**`karama_religion:400` (Zaghawa)**, `buyli_religion:419`, `adamawa_religion:458`,
`geno_religion:477` (Fulani), `emit_religion:496`, `nhaala_religion:515`,
`kuru_masaba_religion:572`, **`sao_religion:591`**, `rogo_miki_religion:610`
(Mossi), **`songhai_religion:629`**, **`godala_religion:648`**,
`anna_religion:686` (Kunama), `rebba_religion:705`, `omo_religion:724`,
`musala_religion:743`, `kalge_religion:762` (Daju), `mbori_religion:781`,
`ori_religion:800`.

Christian and Abrahamic: `miaphysite` (`christian.txt:365`), `judaism`
(`israelite.txt`, and vanilla places it on `waldeba`/`debarq` —
`beyte_yisrael` culture, `cultures/israelite.txt:55`), `sunni`
(`muslim.txt:123`), `shia` (`:64`). **There is no `coptic` religion** — the
whole `in_game/common/religions/` directory was listed; `miaphysite` is the
shipped answer for Nubia and Ethiopia both, and vanilla already assigns it to
ALO, ABW, ETH, MED, DBE, DAM, ENN and GJJ.

Languages: `coptic_language` (`00_egypt.txt:2`), `nubian_language`
(`00_horn_africa.txt:56`), `agaw_language` (`:153`), `beja_language` (`:177`),
`ethiopic_language` (`:225`), `north_ethiopic_language` (`:257`),
`geez_language` (`:283`), `swahili_language` (`00_east_africa.txt:171`),
`mande_language` (`00_sahel.txt:104`), `songhai_language` (`:56`),
`hausa_language` (`:149`), `saharan_language`, `persian_language`
(`00_persia.txt:66`).

**`ethiopic_language`'s own `dynasty_names` list contains `zagwe_dynasty` and
`solomonid_dynasty`, and its `male_names` are the Zagwe king-list**
(`Mara_Takla`, `Yemrehana_Krestos`, `Naakueto_Laab`, `Kedus_Harbe`,
`Jan_Seyum`, `Germa_Seyum`, `Harbai`, `Tatadim`, `Mairari`,
`00_horn_africa.txt:229-233`). Vanilla ships the pre-Solomonic name pool and
never uses it.

Cultures used below, all shipped: `soninke` (`west_african.txt:24`,
`language = mande_language` — this matters for MAL_f, §F.4), `mandinka`,
`bambara` (`:762`), `songhai` (`:823`), `kanembu_culture` (`:868`),
`zaghawa_culture` (`:898`), `sao_culture` (`:973`), `messufa_culture`
(`:1007`), `lamtuna_culture` (`:1025`), `godala_culture` (`:1044`),
`hausa` (`:747`), `wolof` (`:162`), `fulbe` (`:242`), `nubian`
(`horn_of_africa.txt:476`), `beja_culture` (`:169`), `amhara`
(`horn_of_africa.txt:1`, `language = ethiopic_language`), `tigrinya` (`:50`),
`agaw_culture` (`:154`), `harla_culture` (`:233`, `language = ethiopic_language`),
`somali_culture` (`:297`), `daju_culture` (`:313`), `swahili_culture`
(`east_african.txt:254`), `beyte_yisrael` (`israelite.txt:55`).

**Consequence: this package authors ZERO cultures and ZERO religions.**

---

## A. Registry

### A.1 What already exists and needs nothing — the bulk of the package

Nine vanilla **landless-with-claims** tags are exactly the polities 1066 needs,
with vanilla arms, vanilla loc and vanilla colours. Their claim lists are
where they land:

| tag | registry | loc | claims (verbatim) | 1066 |
|---|---|---|---|---|
| **SOA** | `horn_of_africa.txt:167` | Shewa (`:1251`) | `ankober gendebelo nora_eth argobba_province` | the **Makhzumi Sultanate of Shewa, founded 896** [U] — destroyed by Ifat 1285 [U] |
| **BTI** | `:62` | Simien (`:1229`) | `gonder kosoge debarq waldeba shire` | the Beta Israel highland polity; the "Gudit" tradition [D] |
| **ADA** | `:71` | Adal (`:1233`) | `siyara harar arabi awbare dakkar dire_dawa jeldesa` | Zeila's hinterland; "Adal" as a name is 13th c. [D] |
| **END** | `:27` | Enderta (`:1215`) | `abala adigrat agula mekele enderta_province` | banked |
| **GJJ** | `:46` | Gojjam (`:1225`) | `dima bahir_dar dangila debra_warq enjebara gojjam_province` | banked |
| **TMB** | `west_africa.txt:302` | Timbuktu (`:1379`) | 31 tokens over `timbuktu_area` | **stays landless — Timbuktu is founded c. 1100** [U] |
| **FUL** | `:9` | Great Fulo (`:1157`) | 13 tokens over `takrur_province`/`galam_province` | banked |
| **GLE** | `horn_of_africa.txt:183` | Geledi (`:1255`) | `mogadishu barawa haranka merca qoryooley` | **18th c.** [U] — do NOT land; MDI is the Benadir tag |
| **WAD** | `west_africa.txt:506` | Wadai (`:1381`) | `ouara abesehir guereda hadjer_haddid am_dam` | **17th c.** [U] — stays landless |

`TMB` staying landless is a free correctness win nobody has to pay for: its
claim list already IS the answer to "who gets Timbuktu later".

### A.2 Freeness of the new candidates — three scans each

Per `BALTIC-PACKAGE.md §A.2`: (1) word-boundary `\bTAG\b` over the whole
vanilla tree, non-localisation and English-localisation counted separately;
(2) **substring** `_TAG\b|\bTAG_` over the same tree; (3) both scans over the
whole mod repo. Plus a registry index over `VAN/in_game/setup/countries/*.txt`
and `MOD/in_game/setup/countries/*.txt`.

| candidate | VAN word | VAN en-loc | VAN sub | MOD word | MOD sub | registry | verdict |
|---|---|---|---|---|---|---|---|
| **DJN** (Djenné) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **SNH** (Sanhaja) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **LMT** (Lamtuna) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **KGB** (Kangaba) | 0 | 0 | 0 | 0 | 0 | — | free (banked, §B.2) |
| **WGD** (Wagadu) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| **NOB** (Nobatia) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| **DGW** (Duguwa) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| **KWK** (Kawkaw) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| **ZFN** (Zafunu) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| SLL | 22 | 1 | 48 | 2 | 0 | `andes.txt:203` | TAKEN |
| SAO | 38 | 1 | 48 | 8 | 0 | `balkans.txt:228` | TAKEN — the Sao must use **KOT** |
| BRB | 67 | 4 | 81 | 30 | 0 | `lowlands.txt:22` | TAKEN (Brabant) |
| GHA | 35 | 1 | 62 | 2 | 0 | `west_africa.txt:251` | TAKEN — **and that is the point** |
| MAK | 31 | 1 | 50 | 6 | 0 | `horn_of_africa.txt:240` | TAKEN |
| ETH | 142 | 18 | 104 | 24 | 0 | `horn_of_africa.txt:35` | TAKEN |
| ZAN | 72 | 13 | 134 | 21 | 0 | `east_africa.txt:2` | TAKEN |
| PRU | 99 | 26 | 429 | 0 | 1 | — | TAKEN, **empty registry** (formable-only) |

The `SAO` row is the substring scan earning its keep in the other direction:
the obvious mnemonic for the Sao civilisation is taken by a Balkan tag, and
vanilla already provides `KOT` (`west_africa.txt:474`,
`culture_definition = sao_culture`, `religion_definition = sao_religion`,
loc `Sao`, `:1371`) as a `type = pop` country.

**The formable-only class has more African members.** `MSI`, `BEJ`, `NUB`,
`SOI`, `HAU`, `SKO`, `KON` all have **no `setup/countries` block and no
`10_countries` block** — their whole identity lives inside
`00_formable_countries.txt` (§F.4). Do not reuse any of them as a start tag.

### A.3 The new blocks — ONE tag, or two

Appended to `in_game/setup/countries/zz_1066_new_countries.txt`
(registry **65 → 66**, or 67 with SNH; current count measured by
`grep -c "^[A-Z0-9]\{2,6\} = {"` = **65**).

```
DJN = { #Djenne-Jeno — the Middle Niger's oldest city, occupied 250 BC-1400 AD
	color = map_djenne_LOOKUP_REQUIRED
	color2 = black

	culture_definition = bambara
	religion_definition = sunni
}
```

**`map_djenne` does NOT exist** (`VAN/main_menu/common/named_colors/02_map.txt`
scanned; `map_dia` does not either). DJN must reuse a free key or author one.
Free `map_*` keys measured **unused by any country in vanilla or the mod**:
`map_soninke` (`:904`, `rgb { 55 43 14 }`), `map_messufa` (`:950`,
`rgb { 0 78 100 }`), `map_lamtuna` (`:951`, `rgb { 30 50 80 }`),
`map_godala` (`:952`, `rgb { 20 40 100 }`). `map_sao` (`:932`) and
`map_zaghawa` (`:930`) ARE used — by `KOT` (`west_africa.txt:475`) and `ZGW`
(`:499`). **Recommendation: DJN takes `map_messufa`** (unused, and visually
distinct from `map_bambara`, which BMR wears).

```
SNH = { #The Sanhaja of the veil — Lamtuna and Gudala, the Almoravid heartland
	color = map_lamtuna
	color2 = black

	culture_definition = lamtuna_culture
	religion_definition = sunni
}
```

`lamtuna_culture` verified `cultures/west_african.txt:1025`,
`language = tamazight_language`, `color = map_lamtuna`. SNH is the OPEN
DECISION 3 tag: it is the western Sahara at the exact moment the Almoravids
own it, and it is the cheapest tag in the package (§E.2 — nine of its fourteen
locations are **already unowned**).

### A.4 Colours: ZERO new colour rows required

| key | line | value | used by a country today |
|---|---|---|---|
| `map_GHA` | `:957` | `rgb { 260 140 25 }` | GHA — unchanged |
| `map_mali` | `:942` | `rgb { 255 255 185 }` | MAL — unchanged |
| `map_kanembu` | `:912` | `rgb { 30 131 162 }` | KBO — unchanged |
| `map_makuria` | `:1082` | `rgb { 184 80 52 }` | MAK — unchanged |
| `map_alodia` | `:1080` | `rgb { 135 144 180 }` | ALO — unchanged |
| `map_ethiopia` | `:1041` | `rgb { 56 120 191 }` | ETH — unchanged |
| `map_semien` | `:1049` | `rgb { 232 121 145 }` | BTI — unchanged |
| `map_shewa` | `:1068` | `rgb { 1 200 200 }` | SOA — unchanged |
| `map_adal` | `:1052` | `rgb { 145 70 130 }` | ADA — unchanged |
| `map_mogadishu` | `:1076` | `rgb { 212 175 55 }` | MDI — unchanged |
| **`map_lamtuna`** | `:951` | `rgb { 30 50 80 }` | **no** — for SNH |
| **`map_messufa`** | `:950` | `rgb { 0 78 100 }` | **no** — for DJN |
| `map_godala` | `:952` | `rgb { 20 40 100 }` | **no** — banked |
| `map_soninke` | `:904` | `rgb { 55 43 14 }` | **no** — banked |

`MOD/main_menu/common/named_colors/zz_1066_map_colors.txt` is untouched by
this package.

### A.5 Coats of arms

DJN and SNH must each land in `_GENERATOR_OK` (`tools/verify_mod.py:925`) or
carry a CoA block; the check at `:970-973` fails a new registry tag that has
neither. **Recommendation: `_GENERATOR_OK`, tier 4, permanent** — neither
Djenné-Jeno nor the Sanhaja confederations had heraldry of any kind, and the
generator's Islamic religion-gated designs are no less historical than anything
invented, which is the standing rationale for the thirteen taifas (`:926-930`).

Every OTHER tag in this package (GHA, MAL, KBO, MAK, ALO, ETH, BTI, SOA, ADA,
TKR, SON, ZAN, MDI, the Hausa seven, …) is a **vanilla** tag with vanilla arms
and passes through `_van_coa_keys`. Zero CoA work.

### A.6 Localisation

Two rows (four with SNH) in
`MOD/main_menu/localization/english/1066_norman_conquest_l_english.yml`, one
physical line each, UTF-8 **with** BOM:

```
 DJN: "Djenne"
 DJN_ADJ: "Djenne"
 SNH: "Sanhaja"
 SNH_ADJ: "Sanhaja"
```

Every other name is vanilla's (§0.1 table plus `MAK: "Makuria"` `:1275`,
`ALO: "Alodia"` `:1263`, `ETH: "Ethiopia"` `:1217`, `BTI: "Simien"` `:1229`,
`SOA: "Shewa"` `:1251`, `ADA: "Adal"` `:1233`, `MDI: "Mogadishu"` `:1257`,
`ZAN: "Kilwa"` `:1385`).

**`ZAN`'s NAME key is "Kilwa" and `ZZB`'s is "Zanzibar".** A reader who assumes
ZAN = Zanzibar will strip the wrong tag. This is the single most likely
misreading in the theater.

---

## B. The country blocks

### B.1 The two new NEW_COUNTRIES blocks

```
	DJN = {
		starting_technology_level = 3
		include = "expl_west_africa_muslim"
		include = "subsaharan_muslim_monarchy_no_coast"

		country_rank = rank_duchy

		capital = djenne
	}

	SNH = {
		starting_technology_level = 3
		include = "expl_west_africa_muslim"
		include = "subsaharan_muslim_tribe"

		country_rank = rank_duchy

		capital = aoudaghost
	}
```

Field by field, verified:

- **`include = "subsaharan_muslim_monarchy_no_coast"`** —
  `VAN/main_menu/setup/templates/subsaharan_muslim_monarchy_no_coast.txt`, read
  in full: it is a one-line `include = "subsaharan_monarchy_no_coast"` plus
  `legal_code_law = sharia_law_policy` and `immigration_law = open_borders_law`.
  The parent (`subsaharan_monarchy_no_coast.txt`) declares
  `starting_technology_level = 3`, `type = monarchy`,
  `heir_selection = cognatic_primogeniture`,
  `parliament = { parliament_type = assembly }`, thirteen sliders, twelve
  privileges and nine laws. **It DOES declare `type` and `heir_selection`** —
  unlike the coastal `subsaharan_monarchy.txt`, which declares neither (which
  is why ETH/MAK/ALO restate them inline). Used by GHA, KBO, SON, TKR, BMR,
  DFN, BBK, TFK, KBR, ZGH and MAK today.
- **`include = "expl_west_africa_muslim"`** — read in full: its
  `discovered_regions` are `arabia_region sahel_region egypt_region
  ethiopia_region crescent_region`, plus `discovered_areas` covering the whole
  Maghreb, `darfur_area butana_area nubia_proper_area`, all of `guinea_region`'s
  areas, and `logone_area wadai_area adamawa_area`. `djenne` is in
  `timbuktu_area` ⊂ `sahel_region`; `aoudaghost` is in `ghana_area` ⊂
  `sahel_region`. **The capital-discovery assert (`tools/build_setup.py:4862`,
  `"{tag}: capital {cap} is not discovered by any include"`) passes for both.**
- **`starting_technology_level = 3`** — every landed Sahel tag uses 3 (measured
  across GHA/MAL/KBO/SON/TKR/BMR/DFN/BBK/SGH/TFK/TMK/KBR/ZGH). Matching them is
  the local convention, not a judgement.
- **`country_rank = rank_duchy`** — see §F for the render; it is what makes
  the string predictable. Note the standing counter-argument from
  `BALTIC-PACKAGE.md` OPEN DECISION 7 (vanilla's landed tribes omit the line).
- **`subsaharan_muslim_tribe` for SNH** — `type = tribe`. **Tribes are legal
  grant recipients**; `_bad_recip` (`tools/build_setup.py:5391`) exits only on
  `type = steppe_horde`, resolved through the include chain at `:5380-5389`.
  **No African template resolves to `steppe_horde`** (measured: the string
  `steppe_horde` appears in no `subsaharan_*` or `expl_*_africa*` template).

### B.2 The tags this package RESHAPES rather than creates

Every one is a `FIELD_FIXES` job (`tools/build_setup.py:2653`) — exact-substring
surgery on the vanilla block, the NOV/POK/KIE precedent.

| tag | today (measured, mod `10_countries.txt`) | 1066 change |
|---|---|---|
| **MAL** | `country_rank = rank_empire`, `capital = niani`, `dynasty = keita_dynasty`, `reforms = { manden_kurufa_reform }`, a **17-law inline block** incl. `dop_law_gbara` and `ton_ta_jon_ta_ni_woro`, 14 sliders, 27 privileges, `accepted_cultures = { soninke }` | → `rank_duchy`; drop `manden_kurufa_reform`; drop the inline law/privilege/slider block and take `include = "subsaharan_muslim_monarchy_no_coast"`; **keep `keita_dynasty` and `niani`** — the Keita of Kangaba pre-date Sundiata by tradition [D] |
| **GHA** | `subsaharan_muslim_monarchy_no_coast`, `capital = koumbi_saleh`, `heir_selection = cognatic_primogeniture`, no `country_rank` | → add `country_rank = rank_kingdom`; `heir_selection` → **`matrilineal_non_exclusive`** (al-Bakri: the king is succeeded by his sister's son [U]; the value is attested in the same file — MAK and ALO both carry it) |
| **KBO** | `country_rank = rank_empire`, `dynasty = sayfawa_dynasty`, `reforms = { banu_hummay_amendments }`, `regnal_numbers` for six Sayfawa names, three `kbo_*` privileges | → `rank_kingdom`; **drop `sayfawa_dynasty`** (Hummay c. 1075 [D]) and **drop `banu_hummay_amendments`**; keep `njimi`, keep the `kbo_*` privileges (tag-gated flavour, `country_specific.txt:1391` `potential = { has_or_had_tag = KBO }`) |
| **MAK** | `subsaharan_muslim_monarchy_no_coast`, `sharia_law = shafii_policy`, `religious_school = shafii_school`, `mysticism_vs_jurisprudence = 20`, `heir_selection = matrilineal_non_exclusive`, `rank_kingdom`, `capital = dongola` | → include → `subsaharan_monarchy_no_coast`; delete the three Islamic lines; add `liturgical_language = coptic_language`; **registry `religion_definition = sunni` → `miaphysite`** (§B.3) |
| **ETH** | `rank_empire`, `dynasty = solomonid_dynasty`, `capital = ankober` (with vanilla's own comment `#Marade/Tegulet, made capital by Amda Seyon I`), `liturgical_language = geez_language`, `subsaharan_monarchy_no_coast` | → **drop `solomonid_dynasty`** (1270 [U]); `capital = ankober` → **`kubar`** (`amhara_province`, ETH-owned, al-Yaqubi's name for the Ethiopian capital [U]); `rank_empire` → `rank_kingdom`; **add `court_language = ethiopic_language`** (§F.3 — this is what makes the Negus title fire, and it is an OWED check) |
| **ZAN** | `rank_kingdom`, `capital = kilwa_kisiwani`, `court_language = persian_language`, `reforms = { kilwan_trade_communities control_of_the_mahdali_coinage_reform }`, 16 laws, 13 sliders, 20 privileges, a 24-token `currency_data` | → `rank_county`; **drop both reforms** (`country_specific.txt:3847`, `:3861`, both `potential = { has_or_had_tag = ZAN }` — the Mahdali take Kilwa in 1277 [U]); drop the `currency_data`; **keep `court_language = persian_language`** — the Shirazi claim is the town's own founding tradition [D] |
| **the Hausa seven** ZAM KAN KTS GOB RAN DAA ZZZ | all `subsaharan_muslim_monarchy_no_coast` + `sharia_law = maliki_policy` + `religious_school = maliki_school`; registry `religion_definition = sunni` | → include → `subsaharan_monarchy_no_coast`; delete the Islamic lines; **registry `religion_definition` → `bori_religion`** (§B.3) |

### B.3 The registry overrides — an attested route, used twice already

Changing a **registered** tag's `culture_definition` / `religion_definition`
requires a whole-file override of the vanilla registry file. The mod already
does this three times: `in_game/setup/countries/iberia.txt` (ARA's culture,
with a 13-line header comment explaining the single change),
`italy.txt` (the Gallura precedent, named in that header) and `east_asia.txt`.

This package needs **two** more:

| file | vanilla tags | changes |
|---|---|---|
| `in_game/setup/countries/horn_of_africa.txt` | 41 | **MAK `religion_definition = sunni` → `miaphysite`** (`:244`) — one line |
| `in_game/setup/countries/west_africa.txt` | 64 | **ZAM `:419`, KAN `:403`, KTS `:411`, GOB `:444`, RAN `:436`, DAA `:452`, ZZZ `:70` — `sunni` → `bori_religion`** — seven lines |

Both are pure whole-file copies with the named lines changed and a header
comment in `iberia.txt`'s style. The `verify-vanilla-override` skill applies:
a whole-file override deletes everything it does not repeat, and both files
must be re-diffed after every game patch.

**Not proposed, deliberately:** GHA's and KBO's `religion_definition`. See
OPEN DECISION 4 — the pagan-king question.

---

## C. Rulers — five names, and the honest silence around them

**No ruler enters this package without attestation.** For 1066 sub-Saharan
Africa the attested set is genuinely small, and most of the theater takes
`ruler = random`. What can be defended:

| tag | proposed ruler | accession | confidence | note |
|---|---|---|---|---|
| **GHA** | **Tunka Manin** | **1063** | **[D]** | al-Bakri, writing 1067-68, describes the reigning king of Ghana as Tunka Manin, who succeeded his maternal uncle Basi. "Tunka" is arguably the TITLE (Soninke *tunka* = king), so the personal name may be Manin alone. Both the date and the name-vs-title reading are disputed. |
| **TKR** | **Labi** (son of War Jabi) | c. 1041 | **[D]** | War Jabi of Takrur converted c. 1040 and died c. 1040/41; his son led Takruri troops with the Almoravids at Tabfarilla (1056), where Yahya ibn Umar died. The son's name is given variously (Labi / Lebi / Leb). |
| **MAK** | **Solomon** | unknown | **[D]** | A Makurian king Solomon abdicated in 1079 to become a monk and died in Egypt, per the Coptic *History of the Patriarchs*. Reigning in 1066 is plausible but the accession year is not recorded. |
| **KBO** | **Abd al-Jalil** (last Duguwa) | unknown | **[D]** | The Diwan/Girgam king-list places the Duguwa→Sayfawa break at Hummay, dated anywhere from 1067 to 1097. If Hummay's date is 1067, the 1066 ruler is his predecessor for one year. |
| **ETH** | **none — `ruler = random`** | — | — | The century between the "Gudit" disruption (c. 960 [D]) and Mara Takla Haymanot's Zagwe (c. 1137 [D]) has no reliable king-list. This is the Pecheneg discipline (`docs/HANDOFF.md:950-955`) applied to people. |

**Recommendation: seat NOBODY, or seat Tunka Manin alone.** Four of the five
entries above are `[D]` on either the name or the date, and the project's own
standard (`HISTORICAL_RULERS` is `tag -> (character, accession, regnal)` with
an OPEN pre-1066 `ruler_term`, `tools/build_setup.py:69`) requires an
accession date that is *before* `START_DATE` and defensible. Tunka Manin's
1063 is the only one with a near-contemporary source. See OPEN DECISION 8.

**Dynasties.** Vanilla ships exactly **eight** sub-Saharan dynasties
(`VAN/main_menu/setup/start/04_dynasties.txt:6786-6853`): `ndiaye_dynasty`
(`home = linguere`), `keita_dynasty` (`niani`), `sayfawa_dynasty` (`njimi`),
`solomonid_dynasty` (`axum`), `walashma_dynasty` (`zeila`), `maki_dynasty`
(`alula`), `garen_dynasty` (`mareeg`), `mahdali_dynasty` (`kilwa_kisiwani`),
plus `bachwezi`/`baranzi`/`buganda` in the Great Lakes. **There is no
`duguwa_dynasty`, no `cisse_dynasty` (Ghana), no `zagwe_dynasty`, no
`makhzumi_dynasty` and no Makurian house.** Any of them would have to be
authored in `MOD/main_menu/setup/start/04_zz_1066_dynasties.txt` (10,858 bytes
today). If OPEN DECISION 8 lands on "seat Tunka Manin", a `cisse_dynasty`
(the Soninke house tradition names the Cissé [D]) is the one dynasty this
package would add.

**Character pool.** Vanilla ships 7,876 `tag =` lines in `05_characters.txt`.
For this theater: MAL 16, ETH 15, KBO 11, IFA 6, ZAN 6, MAK 3, AJU 1, JOL 1,
MDI 1 — and **GHA 0, SON 0, TKR 0, ALO 0, DFN 0, BMR 0, KAB 0, ZMW 0, DAJ 0**.
All are a *pool*: the mod carries no `ruler_term`, so nothing instantiates
them, and the death-strip already handles the ones born before `START_DATE`.
Inert — but worth knowing that MAL's and KBO's pools are 1300s Keita and
Sayfawa people who would surface if an event ever pulled one.

---

## D. What must die, what must be reskinned, and what must not be touched

Every tag holding land in the six in-scope regions, with a verdict. Holdings
are resolved counts from the mod build.

### D.1 The Sahel and West Africa

| tag | holds | founded | verdict | reason |
|---|---|---|---|---|
| **GHA** Ghana | 16 | pre-800 [U] | **PROMOTE** — the hegemon, `rank_kingdom`, **5 of MAL's 13 vassals repointed to it** (§G.2) | Wagadu at its height under Tunka Manin |
| **MAL** Mali | 21 | **1235** [U] | **RESHAPE, not retire** — `rank_empire`→`rank_duchy`, the Manden chiefdom of Kangaba, territory unchanged | its 21 ARE `old_manding_province` + `tengrela` + `south_manding_area` + `niagassola` — Sundiata's exact heartland |
| **KBO** Kanem | 32 | Duguwa pre-800 [U] | **KEEP**, reshape (§B.2) | Kanem is the one Sahel state older than the start date |
| **SON** Songhai/Gao | 12 | Za/Zuwa, pre-1000 [U] | **KEEP**, independent — **strip nothing but the MAL tie** | al-Bakri treats Kawkaw as a kingdom apart from Ghana |
| **TKR** Takrur | 16 | c. 1030 [D] | **KEEP + GROW** (+22, §E.1) — independent of GHA | Takrur was Ghana's rival and the Almoravids' ally, not its vassal |
| **DFN** Diafunu | 15 | al-Bakri's Zafun [U] | **KEEP** as GHA vassal | |
| **BBK** Bambuk | 11 | the gold field [U] | **KEEP** as GHA vassal | |
| **SGH** Sanghana | 2 | al-Bakri [U] | **KEEP** as GHA vassal | `culture_definition = godala_culture` — the Gudala, the Almoravid movement's first patrons |
| **TMK** Tadmekka | 1 | al-Bakri's Tadmakka [U] | **KEEP**, independent | a Berber town, never Ghana's |
| **TFK** Tirafka | 5 | [D] | KEEP as GHA vassal | |
| **KBR** Kabura | 1 | al-Idrisi [D] | KEEP | |
| **ZGH** Zagha | 1 | Middle Niger, Dia [D] | **KEEP + GROW** (+11, §E.1) | Dia is one of the oldest Muslim towns of the inland delta [D] |
| **BMR** Bambara | **29** | **c. 1712** [U] | **RETIRE landless with claims** | Segou's Bambara state is Mamari Kulubali's, 650 years late |
| **JOL** Jolof | **22** | **c. 1350** [D] | **RETIRE landless with claims** | Ndiadiane Ndiaye's confederation is 14th c. |
| **KAB** Kaabu | **16** | **c. 1235** [U] | **RETIRE landless with claims** | a Mali province founded by Tiramakhan Traore |
| the Hausa seven | 41 | king-lists from c. 999 [D] | **KEEP, flip to `bori_religion`** | the states may be old; their Islam is 14th c. |
| **OUA GWI YAT TEN BSM GUR** (Mossi/Gurma) | 47 | **c. 1400-1500** [D] | **LEAVE ALONE — flagged** | OPEN DECISION 6: retiring six tags to vacate 47 settled locations (152 `define_pop` entries) is the most expensive move available, and the Mossi founding dates are the most disputed in the theater |
| the Guinea forest — BEN OYO NRI IFE OWO IJB IJE IJS ISO OKE IYA AWO AKR ADO OND BON DGB MPR NUP BOR KNG KET ZZZ | 84 in `guinea_region` | Ife c. 1000+, Nri c. 948 (traditional), Benin's Ogiso pre-1200, **Oyo c. 1300** [all D] | **LEAVE ALONE — flagged** | OPEN DECISION 7. Only Oyo is clearly late, and it holds 11 |

### D.2 Nubia

| tag | holds | verdict |
|---|---|---|
| **MAK** Makuria | 16 | **KEEP + CHRISTIANISE** — the registry flip is the single most important correction in the theater |
| **ALO** Alodia | 19 | **KEEP unchanged** — vanilla already ships it miaphysite, `capital = soba`, `heir_selection = matrilineal_non_exclusive`, `rank_kingdom`. At its height in 1066, and vanilla got it right by accident |
| **ABW** Al-Abwab | 3 | **RETIRE landless with claims** — a Makurian province that breaks away in the 1270s [U] |
| **BQL** Baqlin, **NQS** Naqis, **QTA** Qata, **JRN** Jarin, **BZN** Bazin | 3+1+2+3+3 = 12 | **KEEP ALL FIVE** — these are al-Yaqubi's **ninth-century** Beja kingdoms. They are MORE apt at 1066 than at 1337 [U]. A free win |
| **DAJ** Daju | 25 | **KEEP, flagged** — the Daju are the earliest attested Darfur dynasty, dated anywhere from the 12th to the 14th c. [D]. Retiring it vacates 25 settled locations for a disputed date |
| **BKZ** Banu Kanz, **SKN** Suakin | 2+1 in `nubia_proper_area` | **DO NOT TOUCH** — `egypt.txt:9`/`:35`; BKZ is already `FAT`'s tributary (`12_diplomacy.txt:513`) from the Fatimid slice. Flagged seam |

### D.3 Ethiopia and the Horn

| tag | holds | founded | verdict |
|---|---|---|---|
| **ETH** | 45 | continuous [U] | **KEEP, shrink to the northern highlands** (−16, §E.1) and de-Solomonise |
| **BTI** Simien | 0 | Beta Israel highland polity [D] | **LAND with its own 5 claims** — `gonder kosoge debarq waldeba shire`, all from ETH. `culture_definition = beyte_yisrael`, `religion_definition = judaism`, both vanilla (`horn_of_africa.txt:62-67`) |
| **SOA** Shewa | 0 | **896** [U] | **LAND with its 4 claims + the Shewa plateau** (12, §E.1) — the Makhzumi sultanate, the one Horn polity older than 1066 |
| **ADA** Adal | 0 | 13th c. as a name [D] | **LAND with its 7 claims + Zeila** (12, §E.1) — see OPEN DECISION 9 |
| **IFA** Ifat | **37** | **c. 1285** [U] | **RETIRE landless with claims** — the Walashma sultanate is 220 years late, and it is the single largest anachronism in the Horn |
| **AJU** Ajuran | **28** | **13th-17th c.** [D] | **RETIRE landless with claims** — see OPEN DECISION 5 |
| **MDI** Mogadishu | 1 | c. 900-1000 [D] | **GROW to 10** (the Benadir coast, §E.1) — the coast's real 1066 power |
| **WAR** Warsangali, **TDE** Tanade | 6+4 | Somali clan polities [D] | **KEEP + GROW** (§E.1) |
| **AFA** Dankali/Afar, **MED** Medri Bahri, **DHK** Dahlak, **DBE** Dobe'a, **HRL** Harla, **BLE** Bale, **DAW** Dawaro, **HDY** Hadiya, **ENN** Ennarea, **DAM** Damot | 9+6+1+4+1+3+2+3+6+2 | mostly [D] | **KEEP ALL** — none is clearly post-1066, and every one of them absorbs land ETH must shed. Medri Bahri as a *name* is late [D] but the Bahr Negash office is old |
| **GLE** Geledi | 0 | **18th c.** [U] | **stays landless** |

### D.4 The Swahili coast

| tag | holds | verdict |
|---|---|---|
| **ZAN** Kilwa | **21** | **SHRINK to 5** (`rufiji_area`'s current ZAN holdings) + strip both Mahdali-era reforms + strip all 12 tributaries. The Kilwa Chronicle's Shirazi founding is dated c. 957, c. 1000 **or c. 1070** [D] — every reading puts a *town* there in 1066 and none puts an *empire* |
| **ZZB** Zanzibar, **PEM** Pemba, **MBA** Mombasa, **MLI** Malindi, **PTE** Pate, **LAM** Lamu, **GED** Gedi, **UGW** Ungwana, **MOZ**, **AGH** Angoche, **QLM** Quelimane, **BMB** Bambao | 1 each | **KEEP ALL TWELVE UNCHANGED** — a coast of one-location Muslim city-states IS the 1066 Zanj coast. Vanilla built it and this package does not have to |
| **SFA** Sofala, **INH** Inhambane | 1+3 | KEEP — Sofala is named by al-Masudi c. 916 [U] |

### D.5 The measured seams — named, not touched

| what | measurement | why not here |
|---|---|---|
| **Egypt / Aswan** | BKZ 4 (`aswan kom_ombo` in `upper_egypt_area`, `aydhab deraheib` in `nubia_proper_area`), SKN 1 (`suakin`), `FAT→BKZ` tributary at `12_diplomacy.txt:513` | done — the Fatimid slice |
| **the Maghreb** | `MOR` `control` holds four `algiers_area` locations `TLE` owns — the CONTROL_STRIPS twin, already recorded in `tools/build_setup.py:1652-1659` | its own slice |
| **MAM** | `EGYPT_LANDLESS = ("MAM",)`, `tools/build_setup.py:2026` | landless already |
| **FZA** Fezzan | 13 locations, 12 in `desert_area` + `qatrun` in `kanem_area`; `KBO→FZA` vassal at `12_diplomacy.txt:133` | the one Kanem tie that crosses into the Maghreb slice. **Recommendation: keep the tie** — the Kawar–Fezzan road IS Kanem's reason to exist [U] |

**DOUBLE-OWNERSHIP CHECK — clean.** Every donor and recipient named in this
package was tested against the game-wide ten-location double-ownership set
recorded in `BALTIC-PACKAGE.md §0.3` and `tools/build_setup.py:1652-1659`:
the six Samogitian locations (LIT/TEU) and the four `algiers_area` locations
(TLE/MOR). **No African tag carries a `control` block naming another tag's
land.** `CONTROL_STRIPS` needs no African key.

---

## E. Territory

### E.1 `_AFRICA_RULES` — the definitions-resolved grants

Same 5-tuple shape as `_BALTIC_RULES` / `_SELJUK_RULES` / `_NORTH_RULES`:
`tag: (sweep names, singles, minus-sweeps, minus-singles, expected)`. Every
count below is **resolved from `definitions.txt`, not transcribed**, and every
list was tested pairwise disjoint by the resolver (zero overlaps).

```python
_AFRICA_RULES = {
    # --- THE SENEGAL. Takrur under Labi takes the lower river. JOL is
    # Ndiadiane Ndiaye's, c. 1350; the Wolof and Serer states are all
    # 14th century or later, and the one power the eleventh-century
    # sources name on this river is Takrur.
    "TKR": (["jolof_area"], [], [], [], 22),

    # --- THE INLAND DELTA. BMR (Segou, c. 1712) dissolves. Djenne-Jeno
    # takes the Djenne bend and the Safare lakes; Zagha takes Masina and
    # the Bandiagara escarpment (its own capital dia is in macina).
    "DJN": (["djenne_province", "safare_province"], [], [], [], 11),
    "ZGH": (["macina_province", "hayre_province"], [], [], [], 12),

    # --- THE NIGER BEND. Timbuktu is founded c. 1100 and TMB stays
    # landless; the lakes and the salt road go to Gao and the Sahara.
    "SON": (["timbuktu_province"], [], [], [], 5),

    # --- THE SANHAJA OF THE VEIL. The western Sahara at the moment the
    # Almoravids own it: Awdaghust was sacked 1054/55. NINE of these
    # fourteen are already unowned in vanilla.
    "SNH": (["tagant_province", "arguin_province", "adrar_province",
             "taghaza_province"], [], [], [], 17),

    # --- WAGADU. Ghana proper plus Kaarta, Khaaso and Sosso. GHA's own
    # timbuktu_area holdings leave in the SON/SNH/ZGH sweeps above.
    "GHA": (["ghana_province", "kaarta_province", "khaaso_province",
             "sosso_province"], [], [], [], 23),

    # --- BAMBARA's remaining Niger reach folds into Manden.
    "MAL": (["bambara_province"], ["koutiala", "banamba"], [], [], 8),

    # --- ETHIOPIA sheds Shewa and the south.
    "SOA": (["argobba_province", "shewa_province", "wej_province"],
            [], [], [], 12),
    "BTI": (["semien_province"], ["gonder", "shire"], [], [], 5),

    # --- THE HORN. IFA (1285) and AJU (13th c.) dissolve.
    "ADA": (["adal_province"],
            ["siyara", "zeila", "amud", "el_sheikh", "hargeisa",
             "ali_sabieh"], [], [], 12),
    "WAR": (["maakhir_province", "ciid_province", "majerteen_province",
             "guban_province"], [], [],
            ["siyara", "zeila"], 21),
    "MDI": (["banaadir_province", "ajan_province"], [], [], [], 10),

    # --- NUBIA. Al-Abwab (1270s) folds back into Makuria and Alodia.
    "MAK": ([], ["el_metemma"], [], [], 1),
    "ALO": ([], ["ed_damer", "shendi"], [], [], 2),
}
```

**Resolved, with donors and template cultures:**

| tag | n | donors | template cultures |
|---|---|---|---|
| **TKR** | 22 | JOL 22 | `wolof` 10, `serer` 9, `mandinka` 3 |
| **DJN** | 11 | BMR 11 | `mandinka` 6, `bambara` 4, `dogon` 1 |
| **ZGH** | 12 | BMR 8, GHA 2, KBR 1, ZGH 1 | `mandinka` 7, `dogon` 3, `bambara` 2 |
| **SON** | 5 | GHA 1, BMR 3, TFK 1 | `mandinka` 5 |
| **SNH** | 17 | **unowned 9**, GHA 3, DFN 3, SGH 2 | `lamtuna_culture` 8, `godala_culture` 6, `messufa_culture` 3 |
| **GHA** | 23 | GHA 10, DFN 9, BBK 2, TKR 2 | `soninke` 18, `mandinka` 4, `tuareg` 1 |
| **MAL** | 8 | BMR 7, DFN 1 | `mandinka` 8 |
| **SOA** | 12 | ETH 11, DAW 1 | `amhara` 6, `harla_culture` 4, `afar_culture` 2 |
| **BTI** | 5 | ETH 5 | `agaw_culture` 4, `tigrinya` 1 |
| **ADA** | 12 | IFA 11, HRL 1 | `harla_culture` 6, `somali_culture` 6 |
| **WAR** | 21 | IFA 11, WAR 6, TDE 4 | `somali_culture` 21 |
| **MDI** | 10 | AJU 8, MDI 1, IFA 1 | `somali_culture` 10 |
| **MAK** | 1 | ABW 1 | `nubian` 1 |
| **ALO** | 2 | ABW 2 | `nubian` 2 |
| **total** | **161** | | |

Notes the resolver forced:

- **`SNH` is the cheapest tag in the package.** Nine of its seventeen
  locations are `=UNOWNED=` in vanilla — the Adrar and Arguin coast. Landing
  SNH therefore *reduces* the number of unowned settled locations by nine
  rather than increasing it.
- **`taghaza_province`'s three `messufa_culture` locations** (`taghaza`,
  `taoudenni`, `araouane`) are the Sahara salt mines. They are GHA's in
  vanilla. Giving them to the Sanhaja is the historically contested reading
  [D] — Ghana taxed the salt, the Sanhaja mined and moved it. Flagged in
  OPEN DECISION 3.
- **`el_metemma`, `ed_damer`, `shendi`** are ABW's three, and they are its
  entire holding — ABW reaches zero and joins `LANDLESS_AFTER`.

### E.2 What each donor keeps

| tag | before | after | verdict |
|---|---|---|---|
| **BMR** | 29 | **0** | LANDLESS (claims = its 29) |
| **JOL** | 22 | **0** | LANDLESS (claims = its 22) |
| **KAB** | 16 | **0 or 16** | LANDLESS — **but no recipient is proposed**; OPEN DECISION 2 |
| **IFA** | 37 | **0 or 14** | LANDLESS — 23 recipients found (ADA 11, WAR 11, MDI 1); the remaining **14** (`haud_province`'s 8, `mora_province`'s 3, `southern_somalia`'s 3) need a decision. OPEN DECISION 5 |
| **AJU** | 28 | **8** | 20 to MDI/left; the `jubaland`/`mudugh`/`shebelle` interior (20 locations, 44 `define_pop`) is the cost. OPEN DECISION 5 |
| **ABW** | 3 | **0** | LANDLESS (claims = its 3) |
| **ETH** | 45 | **29** | keeps `tigray`, `enderta`, `lasta`, `amhara`, `begemder`, `gojjam`, `dobea`, `serae`, `akele_guzai`, `hamasien` |
| **GHA** | 16 | **23** (net +7; loses 6 in `timbuktu_area`, gains 13) | recipient |
| **TKR** | 16 | **36** (+22 −2 to GHA) | recipient |
| **MAL** | 21 | **29** | recipient — Kangaba plus Segou's reach |
| **ZGH** | 1 | **12** | recipient |
| **SON** | 12 | **17** | recipient |
| **MDI** | 1 | **10** | recipient |
| **WAR** | 6 | **21** | recipient |
| **DFN** | 15 | **2** | keeps `banamba`? — **NO. DFN reaches 2** (`sandare` is swept by GHA; `diara` too). **This is a CAPITAL_FIXES case: DFN's `capital = diara` is granted to GHA.** §E.4 |
| **BBK** | 11 | **9** | keeps `bambouk_province` + `bundu_province`; `capital = kayes` is swept by GHA → **CAPITAL_FIXES** |
| **SGH** | 2 | **0** | both `awlil` and `rosso` are in `arguin_province` → SGH is **emptied by the SNH grant and MUST enter `LANDLESS_AFTER`** (the delta guard, `tools/build_setup.py:5652-5658`) |
| **TFK** | 5 | **4** | fine |
| **KBR** | 1 | **0** | `macina` swept by ZGH → **LANDLESS_AFTER** |
| **HRL** | 1 | **0** | `harar` to ADA → **LANDLESS_AFTER** |
| **TDE** | 4 | **0** | all four in `majerteen_province` → **LANDLESS_AFTER** |
| **DAW** | 2 | **1** | `sharka` to SOA |

```python
AFRICA_LANDLESS = ("BMR", "JOL", "KAB", "IFA", "ABW", "SGH", "KBR",
                   "HRL", "TDE")            # +("AJU",) under decision 5
```

**Four of those nine — SGH, KBR, HRL, TDE — are emptied as a SIDE EFFECT of
grants aimed at somebody else.** That is precisely what the emptied-but-unlisted
delta guard (`tools/build_setup.py:5652-5658`,
`"emptied but not in LANDLESS_AFTER"`) exists to catch, and this package would
be its first real workout. **If the main session prefers fewer retirements**,
SGH/KBR/HRL/TDE can each be kept alive by carving one location out of the
sweep — §E.4 lists which.

`_landless_claims` (`tools/build_setup.py:5238`) snapshots `_owned_by` **before
all grants**, so every retiree's claims are its FULL vanilla holdings: BMR 29,
JOL 22, KAB 16, IFA 37, ABW 3, SGH 2, KBR 1, HRL 1, TDE 4, AJU 28. Those are
the right claim lists — the Walashma's Ifat, the Ajuran's Benadir, Kaabu's
Gambia and Segou's Niger are all *future* objects at 1066.

### E.3 Vacates — and the honest count

`docs/EU5-ERROR-DECODER.md:675-685` records the ~504-line
`jomini_script_system.cpp:252` class: **one line per pop on vacated SETTLED
land**. Measured `define_pop` counts from `VAN/main_menu/setup/start/06_pops.txt`
(28,559 locations with pop blocks, 50,227 `define_pop` entries total):

| candidate vacate | locations | `define_pop` | in this package? |
|---|---|---|---|
| `gambia_area` (KAB's 16 + BBK's 2) | 18 | **48** | **only if OPEN DECISION 2 chooses "vacate"** |
| AJU's `jubaland`+`mudugh`+`shebelle` | 20 | **44** | **only if OPEN DECISION 5 chooses "vacate"** |
| IFA's `haud_province` residue | 8 | ~18 | OPEN DECISION 5 |
| `bornu_area`'s KBO 18 | 18 | **76** | **NO — rejected**, OPEN DECISION 10 |
| the Mossi 47 | 47 | **152** | **NO — rejected**, OPEN DECISION 6 |
| ZAN's `ruvuma_lurio` 9 + `wami` 7 | 16 | **43** | **NO** — they go to ZZB/PEM/MOZ/AGH or stay ZAN's |

**The recommended package vacates ZERO locations** and therefore does not grow
the pop-line class at all: every one of the 161 granted locations goes from one
owner to another except the nine already-unowned ones in `SNH`'s sweep, which
go from unowned to owned — a **nine-location shrink** of the class. That is the
brief's own law (prefer real recipients on settled ground) taken to its end.

### E.4 CAPITAL_FIXES — three, measured

The orphan-capital guard (`tools/build_setup.py:5764-5793`) fires
`if held and capm.group(1) not in held`, i.e. only for a tag that still holds
land but not its capital. Three tags qualify:

| tag | capital | swept by | fix |
|---|---|---|---|
| **DFN** | `diara` | GHA (`ghana_province`) | → `nioro`? **NO — `kaarta_province` is also GHA's.** DFN's survivors are `banamba`(→MAL) and `narena`/`tabou_m`/`kita`. **Recommendation: repoint `capital = kita`**, or carve `diara` out of GHA's sweep (`minus_singles`) and leave DFN at Diara, which is the historically better answer — Zafun IS Diara [D] |
| **BBK** | `kayes` | GHA (`khaaso_province`) | → **`diawara`** (`bambouk_province`, BBK-held, and Bambuk's own name) |
| **SGH** | `awlil` | SNH (`arguin_province`) | SGH goes landless → **exempt** by `:5785`'s `if held and …`, the POR/`guimaraes` precedent (`:2462`). No fix needed |

**Recommendation: carve `diara` out of GHA's `ghana_province` sweep** rather
than repoint DFN. It costs one `minus_singles` token, keeps Diafunu at
Diafunu, and drops GHA's resolved count 23 → 22.

### E.5 What this slice moves, in one line

**161 locations change owner (160 if `diara` is carved out, §E.4), 0 vacated,
9 unowned locations filled, 9 tags retired (10 with AJU), 1 new tag (2 with
SNH), 3 vanilla landless tags revived (BTI, SOA, ADA), 5 rulers considered and
at most 1 seated, 0-1 dynasties authored, 8 registry lines changed across 2
whole-file overrides.**

---

## F. Rank, government and naming — worked out to the rendered string

### F.1 The branches that matter

`VAN/in_game/common/customizable_localization/country_name_construction.txt` is
**first-match**, 188 lines, read in full. Two branches reach this theater:

| line | branch | who it catches |
|---|---|---|
| **`:79-89`** | `country_name_construction_prefix_name_rank` | **`tag = MAL`** + `government_type = monarchy` + rank_kingdom **or** rank_empire |
| **`:159-164`** | `country_name_construction_sultanate` | **any** `religion.group = religion_group:muslim` |
| `:183-186` | `prefix_rank_of_name`, `fallback = yes` | everybody else |

Loc (`government_names_l_english.yml`):
- `country_name_construction_prefix_name_rank: "$PREFIX$ $NAME$ $RANK$"` (`:7`)
  and **`…_map: "$PREFIX$ $NAME$ $RANK$"` (`:8`)** — the map string is the full
  string.
- `country_name_construction_sultanate: "$country_name_construction_prefix_rank_of_name$"` (`:19`)
  and `…_map: "$country_name_construction_prefix_rank_of_name_map$"` (`:20`).
- `country_name_construction_prefix_rank_of_name: "$PREFIX$ $RANK$ of $ARTICLE$ $NAME$"` (`:11`)
  and **`…_map: "$NAME$"` (`:12`)**.

**THE LAW, for this theater: a Muslim country's map label is its NAME key
verbatim.** The sultanate branch redirects straight to the fallback's strings.
So `GHA` reads "Ghana", `KBO` reads "Kanem", `MAK` reads "Makuria" on the map —
NAME keys are LIVE for almost everything here, unlike TEU/LIV in the Baltic.

### F.2 THE MAL TRAP — a tag-gated branch, and it is worse than LIT's

`country_name_construction.txt:79-89` is gated on `tag = MAL` AND
`government_type = monarchy` AND (`rank_kingdom` OR `rank_empire`), and its map
string is `"$PREFIX$ $NAME$ $RANK$"`.

`country_ranks.txt` then supplies `$RANK$`. It is **first-match, 2741 lines**,
and it carries **culture-gated African branches** — not tag-gated:

| branch | line | trigger | loc |
|---|---|---|---|
| `rank_empire_mali` | **`:335`** | `country_rank_is_empire` + **`culture = culture:mandinka`** | `"$rank_empire$"` = "Empire", ruler **"Mansa"** (`:218-219`) |
| `rank_kingdom_mali` | **`:967`** | kingdom + `culture:mandinka` | `"$rank_kingdom$"` = "Kingdom", ruler **"Mansa"** (`:566-567`) |
| `rank_duchy_mali` | **`:1907`** | duchy + `culture:mandinka` | `"$rank_duchy$"` = "Duchy", ruler **"Mansa"** (`:844-845`) |
| `rank_empire_kanem` | `:506` | empire + **`culture:kanembu_culture`** | "Empire", ruler **"Mai"** (`:208-209`) |
| `rank_kingdom_kanem` | `:957` | kingdom + `kanembu_culture` | "Kingdom", ruler **"Mai"** (`:563-564`, `"$rank_empire_kanem_ruler_male$"`) |
| `rank_duchy_kanem` | `:1897` | duchy + `kanembu_culture` | "Duchy", ruler **"Shehu"** (`:841-842`) |
| `rank_empire_ethiopia` | `:496` | empire + **`court_language ?= language:ethiopic_language`** + christian | "Empire", ruler **"Negusa Nagast"** (`:193-195`) |
| `rank_kingdom_ethiopia` | `:1162` | kingdom + same | "Kingdom", ruler **"Negus"** (`:587-589`) |
| `rank_duchy_ethiopia` | `:1887` | duchy + same | **"Duchy"**, ruler **"Ras"** (`:837-839`) |
| `rank_kingdom_zimbabwe` | `:987` | kingdom + `culture:shona_culture` | "Kingdom", ruler "Mambo" (`:569-570`) |

**Therefore: MAL at `rank_empire` renders "Mali Empire" on the map, ruled by a
Mansa** — the tag branch fires (`:87`), `$RANK$` resolves through `:335` to
"Empire", and the map string is the full string. **The rank line is the only
escape.** At `rank_duchy` the tag branch at `:79` fails (it requires
kingdom-or-empire), MAL falls through the sultanate branch to the fallback, and
the map reads bare **"Mali"**.

This is the `rank_kingdom_grand_duchy_LIT` class (`BALTIC-PACKAGE.md §C.2`)
with a difference that makes it worse: **LIT's trap is tag-gated and therefore
escapable by retiring the tag. MAL's `$RANK$` is CULTURE-gated**, so any
`mandinka`-culture tag this project ever creates inherits the Mansa title
whether it wants it or not — including a hypothetical `KGB` Kangaba.

**First-match order at duchy rank, walked** (the order decides everything):
`:1494` order → `:1505` abbey → `:1515` bishopric → `:1525/1535` theocracy →
`:1546` horde → `:1555/1572` celtic → `:1586/1596` maori/haudenosaunee →
**`:1606` `rank_duchy_tribe`** → `:1617` turkish → … → **`:1743`
`rank_duchy_muslim`** → `:1755` indian → … → **`:1887` ethiopia** → **`:1897`
kanem** → **`:1907` mali** → … → `:2006` `rank_duchy` (default).

**Two consequences the design must obey:**
1. `rank_duchy_tribe` (`:1606`) **outranks** `rank_duchy_muslim` (`:1743`). A
   Muslim tribe at duchy rank renders **"Tribe" / "Chief"** (`:790-791`), not
   "Emirate". SNH is `subsaharan_muslim_tribe` → it renders "Tribe of the
   Sanhaja" / map "Sanhaja" / ruler "Chief".
2. `rank_duchy_muslim` (`:1743`) **outranks** ethiopia/kanem/mali
   (`:1887/1897/1907`). So the Mansa/Mai/Ras titles are unreachable for a
   MUSLIM duchy. A Muslim mandinka duchy reads **"Emirate of Mali" / "'Amīr"**
   (`rank_duchy_muslim: "Emirate"`, ruler `"'Amīr"`, `:781-782`).

At **kingdom** rank the order is the reverse where it matters: `:945` tribe →
**`:957` kanem** → **`:967` mali** → `:976/987` zimbabwe → `:996` persian →
`:1012-1050` the five tag-gated muslim dynastic branches (MAM `:1014`, MOR
`:1024`, TLE `:1033`, TUN `:1042`, GRA `:1052`) → **`:1060`
`rank_kingdom_muslim`** ("Sultanate" / "Sultan", `:463-464`) → … → **`:1162`
ethiopia**.

**So kanem and mali BEAT muslim at kingdom rank and LOSE to it at duchy rank.**
That single asymmetry decides three of this package's rank choices.

### F.3 What each tag renders as, under the recommended design

| tag | religion | gov | rank | branch chain | full name | **map label** | ruler title |
|---|---|---|---|---|---|---|---|
| **GHA** | sunni | monarchy | **`rank_kingdom`** | `:160` sultanate → `:1060` | "Sultanate of Ghana" | **Ghana** | **Sultan** |
| **MAL** | sunni | monarchy | **`rank_duchy`** | `:160` sultanate → `:1743` | "Emirate of Mali" | **Mali** | **'Amīr** |
| **KBO** | sunni | monarchy | **`rank_kingdom`** | `:160` sultanate → **`:957` kanem** | "Kingdom of Kanem" | **Kanem** | **Mai** |
| **SON** | sunni | monarchy | none declared | sultanate → size-derived | "…of Songhai" | **Songhai** | Sultan/'Amīr |
| **TKR** | sunni | monarchy | none | sultanate | "…of Takrur" | **Takrur** | ditto |
| **SNH** | sunni | **tribe** | `rank_duchy` | `:160` sultanate → **`:1606` tribe** | "Tribe of the Sanhaja" | **Sanhaja** | **Chief** |
| **DJN** | sunni | monarchy | `rank_duchy` | sultanate → `:1743` | "Emirate of Djenne" | **Djenne** | 'Amīr |
| **MAK** | **miaphysite** | monarchy | `rank_kingdom` | `:183` fallback → `:1252` `rank_kingdom` | "Kingdom of Makuria" | **Makuria** | **King** |
| **ALO** | miaphysite | monarchy | `rank_kingdom` | same | "Kingdom of Alodia" | **Alodia** | King |
| **ETH** | miaphysite | monarchy | **`rank_kingdom`** | fallback → **`:1162` ethiopia** *if* court_language fires, else `:1252` | "Kingdom of Ethiopia" | **Ethiopia** | **Negus** *or* King |
| **BTI** | **judaism** | monarchy | derived | fallback | "…of Simien" | **Simien** | King/Duke |
| **SOA** | sunni | monarchy | derived | sultanate | "…of Shewa" | **Shewa** | Sultan/'Amīr |
| **ADA** | sunni | monarchy | derived | sultanate | "…of Adal" | **Adal** | ditto |
| **MDI** | sunni | monarchy | `rank_kingdom` | sultanate → `:1060` | "Sultanate of Mogadishu" | **Mogadishu** | Sultan |
| **ZAN** | sunni | monarchy | **`rank_county`** | sultanate → `rank_county_muslim`* | "…of Kilwa" | **Kilwa** | * |
| the Hausa seven | **`bori_religion`** | monarchy | derived | fallback → `rank_*` default | "Kingdom/Duchy of Kano…" | **Kano**, **Katsina**, … | King/Duke |

\* `rank_county_muslim` was not located in `government_names_l_english.yml` by
direct grep; the county section of `country_ranks.txt` begins at `:2018` and
`rank_county_tribe` is at `:2279`. **OWED CHECK** before ZAN's rank drops to
county — if no `rank_county_muslim` branch exists, ZAN falls to `rank_county`
("County" / "Count", `:884-887`), which reads badly for a Swahili town.
`rank_duchy` is the safe alternative ("Emirate of Kilwa" / "'Amīr").

**The ETH question is the one open render.** `rank_kingdom_ethiopia` requires
`court_language ?= language:ethiopic_language`. **Measured: not one of vanilla's
347 `court_language` lines in `10_countries.txt` sets `ethiopic_language`, and
ETH declares no `court_language` at all** — it declares
`liturgical_language = geez_language`. ETH's *culture* `amhara` does have
`language = ethiopic_language` (`horn_of_africa.txt:1-2`). Whether
`court_language` defaults from the primary culture is **not established by any
file in this repo**. If it does not, the Negus/Negusa Nagast titles are dead
code that vanilla ships and never reaches. **Recommendation: add
`court_language = ethiopic_language` to ETH's block** — one line, harmless if
redundant, and it is what makes the title fire either way.

### F.4 Formables — one becomes reachable, one becomes unreachable

`VAN/in_game/common/formable_countries/00_formable_countries.txt`, 143
formables. Six touch this theater:

| formable | line | tag | level | fraction | scope | potential | reachable at start? |
|---|---|---|---|---|---|---|---|
| **MAL_f** | **`:4467`** | MAL | 2 | **0.75** | `mali_area` + `ghana_area` = **62 ownable** → **47 needed** | `culture.language = language:mande_language` | **GHA reaches 23 under §E.1 = 37%. NO.** But `soninke`'s language IS `mande_language` (`west_african.txt:24-25`), so **Ghana→Mali is a live, historically exact formation path** for a player who conquers the Niger |
| **NUB_f** | `:4495` | NUB | 2 | 0.75 | `nubia_proper_area` + `butana_area` = 45 → 34 | `culture = culture:nubian` | MAK reaches 17, ALO 21. Neither alone. **NO** |
| **SOI_f** | `:4383` | SOI | 2 | 0.5 | `somalia_region` = 83 → 42 | `culture:somali_culture` | WAR reaches 21, MDI 10. **NO** |
| **HAU_f** | `:3151` | HAU | 2 | 0.5 | the two Hausa areas = 41 → 21 | `culture:hausa` | ZAM holds 17. **NO — but close.** Watch it |
| **SKO_f** | `:3120` | SKO | 3 | 0.75 | same 41 → 31 | `(hausa or fulbe)` **AND `religion = religion:sunni`** | **the Hausa religion flip makes SKO_f UNREACHABLE at start** — which is correct: Sokoto is 1804 |
| **ETH_f** | `:1208` | ETH | 3 | 0.6 | `ethiopia_region` = 95 → 57 | `(agaw/amhara/tigre/tigrinya)` AND **`religion = religion:miaphysite`** | ETH reaches 29 under §E.1 = 31%. **NO.** ETH keeping `miaphysite` keeps the path open, which is right |
| **MSI_f** | `:1151` | MSI | 1 | 0.75 | the two Mossi areas = 47 → 36 | `culture:mossi` | OUA holds 16. **NO** |
| **BEJ_f** | `:1178` | BEJ | 1 | 0.75 | five named locations (`deraheib agordat tesenei massawa zula`) → **4** | `culture:beja_culture` | today they are BKZ/BQL/BZN/JRN/QTA, one each — **nobody holds 2**. NO. Worth knowing it is a 4-location gate |

**No formable is consumed and none becomes reachable at start.** MAL_f is the
one worth naming to the user: it turns "Ghana grows into Mali" into a real
mechanic that vanilla already built.

---

## G. Diplomacy

`MOD/main_menu/setup/start/12_diplomacy.txt` today: **348 `dependency` lines,
28 `scripted_mutual`/`scripted_oneway` lines** (measured).

**Exactly 50 lines name a sub-Saharan African tag** (measured by an
80-tag alternation grep). Their fate:

### G.1 Lines the generic landless sweep kills for free — 7

`_drop_landless_dep` (`tools/build_setup.py:6756-6765`) removes a line if
**either** side is in `LANDLESS_AFTER`.

```
:250 dependency = { first = MAL second = BMR subject_type = vassal }      -> BMR landless
:253 dependency = { first = MAL second = JOL subject_type = vassal }      -> JOL landless
:254 dependency = { first = MAL second = KAB subject_type = vassal }      -> KAB landless
:214 dependency = { first = ETH second = IFA subject_type = tributary }   -> IFA landless
:220 dependency = { first = IFA second = HRL subject_type = vassal }      -> IFA + HRL landless
:221 dependency = { first = IFA second = WAR subject_type = tributary }   -> IFA landless
:222 dependency = { first = IFA second = TDE subject_type = tributary }   -> IFA + TDE landless
```

**`n_landless_deps` 244 → 251** (`tools/build_setup.py:6824`). Under OPEN
DECISION 5's "retire AJU" branch, AJU adds **zero** more — measured: no
dependency line names AJU.

### G.2 The MAL → GHA REPOINT — 10 lines, the Jurchen shape

Ten of MAL's thirteen vassals survive as landed tags. They do not become
independent: they become **Ghana's**. This is the repoint, attested twice
(`:6713-6724` 46 Jurchen `CHI`→`LIA` with `if n_liao != 46`; `:6735-6748` 16
jimi `LNG`→`CHI` with `if n_jimi != 16`).

```
:249 MAL->BBK   :251 MAL->DFN   :252 MAL->GHA*  :255 MAL->KBR
:256 MAL->SGH*  :257 MAL->SON*  :258 MAL->TFK   :259 MAL->TKR*
:260 MAL->TMK*  :261 MAL->ZGH
```

- **`:252 MAL->GHA` is DELETED, not repointed** — GHA becomes the overlord.
- **`:257 MAL->SON`, `:259 MAL->TKR`, `:260 MAL->TMK` are DELETED** — al-Bakri
  treats Kawkaw, Takrur and Tadmakka as kingdoms apart from Ghana [U]; Takrur
  in particular is Ghana's rival and the Almoravids' ally.
- **`:256 MAL->SGH` is DELETED** — SGH is emptied by the SNH grant (§E.2) and
  goes landless, so this line dies free in the sweep instead. That makes
  `n_landless_deps` **252**, not 251.
- **The five that repoint `MAL` → `GHA`: BBK, DFN, KBR, TFK, ZGH.**

```python
_GHANA_VASSALS = ("BBK", "DFN", "KBR", "TFK", "ZGH")
# assert n_ghana == 5
```
plus four named deletions (GHA, SON, TKR, TMK), `assert n == 4`.

### G.3 The KBO → Hausa strips — 7 lines

```
:263 KBO->DAA  :264 KBO->GOB  :265 KBO->KAN  :266 KBO->KTS
:267 KBO->RAN  :268 KBO->ZAM  :269 KBO->ZZZ   (all subject_type = tributary)
```
Kanem-Bornu's overlordship of the Hausa states is a **Bornu-era** relation
[U] — the Sayfawa do not cross to the west shore of Lake Chad until the 1380s.
At 1066 Kanem's reach is north (Kawar, Fezzan), not west. **Strip all seven by
name**, the Rus batch's shape (`:6676-6686`), `assert n_hausa == 7`.

### G.4 The ZAN → 12 tributaries — 12 lines

```
:225 ZAN->MLI  :226 ZAN->MBA  :227 ZAN->GED  :228 ZAN->PEM
:229 ZAN->NTL  :230 ZAN->MTO  :231 ZAN->AHY  :232 ZAN->MHL
:233 ZAN->VOH  :234 ZAN->NYM  :235 ZAN->MOZ  :236 ZAN->ZZB
```
Kilwa's thalassocracy — including **six Madagascar tributaries** (NTL, MTO,
AHY, MHL, VOH, NYM) — is the Mahdali sultanate's, 1277+ [U]. **Strip all
twelve by name**, `assert n_kilwa == 12`. This is the largest single strip in
the package and it is what turns the map from "Kilwa's empire" into "a coast
of city-states".

### G.5 The ETH → 4 tributaries — 4 lines

```
:215 ETH->ENN (tributary)  :216 ETH->HDY (vassal)
:217 ETH->BLE (vassal)     :218 ETH->DAW (vassal)
```
Ennarea, Hadiya, Bale and Dawaro are the southern Muslim and Sidama polities
that Amda Seyon I subdued in the 1320s-30s [U]. **Strip all four**,
`assert n_eth == 4`.

### G.6 Left alone

```
:133 KBO->FZA (vassal)     -- KEEP: the Kawar-Fezzan road IS Kanem's artery [U]
:239-246 ZMW-> 8 pop tribs -- out of scope (§H); note they are pop countries
:513 FAT->BKZ (tributary)  -- the Fatimid slice's, untouched
```

### G.7 Pacts and IOs

**Measured: not one `scripted_mutual` or `scripted_oneway` line in the file
names a sub-Saharan African tag.** `n_pacts` stays at **9**
(`tools/build_setup.py:6851`).

**International organizations — one addition, and it is exact.**
`MOD/main_menu/setup/start/15_international_organizations.txt:376-392` carries
`add_international_organization = { type = autocephalous_patriarchate
creation_date = 451.1.1 members = { ETH } variables = { religion =
religion:miaphysite seat = location:alexandria } … }`. That is the **Coptic
patriarchate of Alexandria**, and it currently has one member.

At 1066 the bishops of **Makuria and Alodia were consecrated in Alexandria**
[U] — the Nubian church was a province of the Coptic patriarchate for six
centuries. **Recommendation: `members = { ETH }` → `members = { ETH MAK ALO }`.**
Two tokens, one of the cheapest and most exact statements the package can make,
and it depends on the MAK religion flip (§B.3) landing first.

**Measured: no other African tag appears in any IO member list in the file** —
the whole file was scanned for 80 African tags and ETH is the sole hit. No HRE
collision, no Hanseatic residue, nothing.

---

## H. Left alone deliberately

| what | measurement | why |
|---|---|---|
| **`kongo_region`** — 403 ownable, of which `west_kongo_area` 74 (72 unowned, VUN 2) and `kongo_area`'s MOM 7, MPE 6, NSU 2, VNA 1, MBT 1 | 14 registry tags in `kongo.txt` | Outside the brief. Note for whoever takes it: `country_ranks.txt:395` carries a `tag = MOM # Momboares` branch — a tag-gated rank for a Kongo tag, the LIT trap's shape |
| **`great_lakes_region`** — 144 ownable, **130 unowned**, KIT 4, BUG 3, WNA 1 | `BNY` Bunyoro, `RWA`, `KRW` Karagwe, `NKO` Nkore, `UBH` Buha, `BUU` Burundi all landless with 1-5 claims each; `bachwezi_dynasty` and `baranzi_dynasty` ship at `home = bigo_bya_mugenyi` | The Chwezi/Kitara traditions are exactly the 11th-13th c. [D] and this is the theater where a 1066 mod could add most, but it is outside the brief and the sources are oral |
| **`madagascar_region`** — 90 ownable, **79 unowned**; 10 one-location tags | 14 landless Malagasy tags with 1 claim each | Outside the brief. Six of them are ZAN tributaries and those ties die in §G.4 |
| **`zimbabwe_region`** — 109 ownable, ZMW 22, INH 3, SFA 1, **83 unowned** | 8 pop-country tributaries | **A real anachronism, flagged:** Great Zimbabwe's floruit is c. 1100-1450 and Mapungubwe's c. 1075-1220 [both D] — at 1066 neither exists. Outside the brief; OPEN DECISION 11 |
| **`southern_africa_region`** — 184 ownable, **184 unowned** | `kaggen_religion` on 116 | Vanilla already models it as stateless. Correct for 1066 and for 1337 |
| **`central_africa_region`** — 160 ownable, DAJ 5 and ZZZ 1, **154 unowned**; `logone_area` 18 all unowned with `sao_culture` 10 / `sao_religion` 17 | `KOT` (Sao) and `BGI` (Baguirmi) are pop countries | The Sao city-states of the Chari-Logone are a live 1066 subject [U] and `KOT` is the tag for them — banked, not built. Converting a pop country to a landed one is machinery this project has never used |
| **the Guinea forest** — 84 locations across `benin_area`, `yoruba_area`, `akan_area`, `gur_area`, `lower_niger_area`, `gold_coast_area`, `kru_area`, `upper_guinea_area`, `gulf_of_guinea_area`, `kong_area` (117 of them **already unowned**) | 23 landed tags | OPEN DECISION 7 |
| **the Mossi and Gurma** — 47 locations, 152 `define_pop` | OUA 16, GWI 6, YAT 5, TEN 5, BSM 6, GUR 4 | OPEN DECISION 6 |
| **`zarma_area` 19, `air_area`'s 12, `equatoria_area` 23** — all unowned in vanilla | | Tuareg, Zarma and Nilotic ground with no state at 1066 and none at 1337. The Pecheneg discipline. They already contribute to the pop-line class and that is the honest price |
| **the pop-phase inheritance** | `ghana_area` is **`sunni` 31/31** and `kanem_area` **`sunni` 18/24** in `location_templates.txt` | If OPEN DECISION 4 lands on "pagan kings", the pop phase inherits the matching correction — `nyama_religion` on the Soninke locations, `karama_religion` on the Kanembu. Recorded here so it is not re-derived |
| **`06_pops.txt` and `07_cities_and_buildings.txt`** | vanilla's, un-overridden — the mod's `setup/start` set is six files | Any Africa pop or building anachronism is a whole-file-override question, the class `BALTIC-PACKAGE.md` OPEN DECISION 6 already banked |

---

## I. Mechanism — everything runs on machinery that already exists

Unlike the Baltic, this package needs **no new build step**.

| need | existing mechanism | `file:line` |
|---|---|---|
| grants resolved from `definitions.txt` | `_resolve_ruleset` + the Central Asia loop | `:779`, `:5037` |
| retire with auto-derived claims | `LANDLESS_AFTER` + `_landless_claims` | `:2546`, `:5238` |
| catch side-effect retirements | the emptied-but-unlisted delta guard | `:5652-5658` |
| block surgery on vanilla blocks | `FIELD_FIXES` | `:2653` |
| capital repoint | `CAPITAL_FIXES` | `:2600` |
| **overlord change** | the **repoint**, twice attested | `:6713-6724`, `:6735-6748` |
| named dependency strips | the Rus batch's shape | `:6676-6686` |
| registry identity change | whole-file override | `MOD/in_game/setup/countries/iberia.txt:1-13` |
| double-ownership | `CONTROL_STRIPS` — **no African key needed** | `:1659` |
| steppe-horde recipient guard | `_bad_recip` — no African template is a horde | `:5391` |

Three asserts that will fire if the design is wrong, and should be watched:

1. **`_remove_owned_many` `!= 1`** (`:5220` region) — fires if any granted
   location has two ownership entries. Measured clean for all 161.
2. **`_list_owner` disjointness** (`:5322`) — the fourteen rule-sets were
   tested pairwise disjoint by the resolver (zero overlaps).
3. **the capital-discovery assert** (`:4862`) — `expl_west_africa_muslim`
   carries `sahel_region`, so `djenne` and `aoudaghost` both pass.

---

## OPEN DECISIONS

**1. MAL: reskin down to Kangaba, or retire landless?**
`country_name_construction.txt:79-89` gates a name branch on `tag = MAL` +
monarchy + kingdom-or-empire, whose **map string is the full string**
(`government_names_l_english.yml:8`); `country_ranks.txt:335` then supplies
`"Empire"` and the ruler title `"Mansa"` — **so MAL at `rank_empire` literally
reads "Mali Empire" on the 1066 map.** MAL's 21 locations are already exactly
Sundiata's heartland.
**Recommendation: RESHAPE, do not retire.** Drop the rank to `rank_duchy`
(which structurally escapes `:79`), drop `manden_kurufa_reform` and the 17-law
inline block, keep `keita_dynasty` and `niani`, and let the map read "Mali" over
a 29-location Manden chiefdom. It costs one `FIELD_FIXES` entry and zero
territory. **Counter-argument:** "Mali" naming anything in 1066 will read as an
error to a player who knows Sundiata's date, and retiring MAL landless would
make the empire a claim-set exactly as GRA, MAM and SKE are — at the price of a
new `KGB` tag (**FREE**, scanned), a colour, a loc pair and a `_GENERATOR_OK`
entry, plus inheriting the culture-gated Mansa title anyway.

**2. Kaabu's 16 — vacate, or keep KAB?**
KAB (c. 1235, a Mali province [U]) holds all 16 settled locations of
`gambia_area`'s Jola/Balanta/Manjak country, and **no vanilla tag exists for
that ground**. Vacating costs **48 `define_pop`** lines in the known
`jomini_script_system.cpp:252` class.
**Recommendation: RETIRE KAB and hand `gambia_area` to TKR**, which under
decision-free §E.1 already reaches 36 and whose Senegal-basin sphere is the
nearest attested overlordship. Zero vacates, zero new tags. **Counter:** Takrur
holding the Gambia is not attested and is a bigger invention than leaving Kaabu
250 years early; the honest alternatives are "keep KAB with a comment" (zero
cost, one anachronism) or "vacate 16" (48 error lines, no invention).

**3. The Sanhaja tag `SNH` — build it, or leave the Sahara to Ghana?**
`ghana_area` carries `lamtuna_culture` on 8 locations and `godala_culture` on 6
— the Almoravid confederations — and **nine of the fourteen are already
unowned**. Awdaghust was sacked by the Almoravids in 1054/55 [U], twelve years
before start.
**Recommendation: BUILD IT.** 17 locations, of which 9 cost nothing (they are
unowned), a free tag, a free colour (`map_lamtuna`, `02_map.txt:951`, unused by
any country), and it puts the decade's most important West African fact on the
map. **Counter:** the Almoravids are the Maghreb slice's subject and a
sub-Saharan `SNH` will collide with whatever that slice does with `MOR`/Abu
Bakr ibn Umar's southern command; and `taghaza_province`'s three salt-mine
locations are genuinely contested between Ghana and the Sanhaja [D]. If the
main session prefers, drop `taghaza_province` from SNH's sweep (17 → 14) and
leave the salt with Ghana.

**4. THE PAGAN-KING QUESTION — do GHA and KBO start Muslim?**
al-Bakri is explicit that the king of Ghana in 1068 was **not** a Muslim while
his ministers and the twin town were [U]; the Duguwa of Kanem convert with
Hummay c. 1075 [D]. Vanilla gives both `religion_definition = sunni`
(`west_africa.txt:256`, `:460`). The shipped proxies exist and are exact:
`nyama_religion` (`folk_african.txt:364`, the Mande religion) for Soninke Ghana,
`karama_religion` (`:400`, the Zaghawa religion) for the Duguwa.
**Recommendation: LEAVE BOTH SUNNI, and record the correction for the pop
phase.** `ghana_area` is `sunni` on **31 of 31** locations and `kanem_area` on
18 of 24 in `location_templates.txt`; a pagan country over 100% Muslim pops
produces immediate heresy/unrest mechanics that misrepresent the eleventh
century worse than the label does, and the setup fix is only half the fix.
**Counter — and it is strong:** this is the single most famous fact about
Ghana, the registry override is one line each in a file this package already
overrides for MAK, and "wrong now, right in the pop phase" is how anachronisms
survive. If the main session wants it, the change is: registry line +
include swap (`subsaharan_muslim_monarchy_no_coast` → `subsaharan_monarchy_no_coast`)
+ delete `religious_school`/`sharia_law`/`mysticism_vs_jurisprudence`, per tag.

**5. Ajuran — retire (and what takes the interior), or keep?**
AJU (13th-17th c. [D]) holds 28, of which 20 are the Jubaland/Mudugh/Shebelle
interior (**44 `define_pop`**). MDI (Mogadishu, c. 900-1000 [D]) holds one
location and is the coast's real 1066 power.
**Recommendation: RETIRE AJU, grow MDI to 10 (the Benadir and Ajan coasts), and
give the 20-location interior to WAR** — Somali clan-polity ground, already the
model vanilla uses in the north. Zero vacates. **Counter:** WAR (Warsangali) is
a *northern* clan confederation and stretching it to the Jubba is an invention
of the same size as leaving Ajuran early; the alternatives are "vacate 20" (44
error lines) or "keep AJU with a comment". Note that **no diplomacy line names
AJU**, so retiring it is free on that side.

**6. The Mossi — six tags, 47 locations, and the most disputed dates in the
theater.**
Mossi state formation is dated anywhere from the Naba Wedraogo tradition (11th
c.) to the archaeological and documentary consensus of the 15th-16th c. [D];
the first firm event is the Mossi raid on Timbuktu in 1330 [U].
**Recommendation: LEAVE ALL SIX ALONE.** Retiring them vacates 47 settled
locations and **152 `define_pop`** entries — the most expensive move available
in Africa — to act on the theater's least settled dating. **Counter:** if the
project's standard is "a region is done when the people on the throne are the
people who were there", six kingdoms that probably did not exist is exactly the
kind of thing this project retires elsewhere. A cheap middle path exists:
retire the five smaller ones (GWI, YAT, TEN, BSM, GUR, 26 locations) into OUA,
leaving one Mossi tribal polity — zero vacates, one anachronism instead of six.

**7. The Guinea forest — 84 locations, 23 tags, and only one clear error.**
Ife's floruit is c. 1000+ , Nri's tradition begins 948, Benin's Ogiso predate
1200, but **Oyo is c. 1300** [all D]. 117 locations in `guinea_region` are
already unowned.
**Recommendation: TOUCH ONLY OYO** — retire OYO landless with claims (11), and
let IFE (which holds 1) take `yoruba_area`'s core. Ife is the Yoruba ritual
capital and its priority over Oyo is the tradition's own claim [U].
**Counter:** the whole forest belt's dating is oral tradition and the honest
move may be to leave all 23 exactly as vanilla has them; that is what this
document recommends for the Mossi, and consistency argues for it here too.

**8. Rulers — seat Tunka Manin, or seat nobody?**
Four of the five candidates in §C are `[D]` on the name, the date or both.
Tunka Manin alone has a near-contemporary source (al-Bakri, writing 1067-68),
and even there "Tunka" may be the Soninke title for king rather than a name.
**Recommendation: seat NOBODY.** The Pecheneg discipline; `ruler = random` is
what the sources support, and the package is already the largest territory and
diplomacy slice in Africa without adding five contestable people. **Counter:**
Tunka Manin is the single most famous named sub-Saharan ruler of the 1060s, the
mechanism is a one-line `HISTORICAL_RULERS` entry plus a `NEW_CHARACTERS` block
plus a `cisse_dynasty` (which vanilla does not ship), and a 1066 mod that leaves
Ghana's throne to the engine has left the theater's one nameable person out.

**9. Adal, or Shewa, or both — who holds Zeila?**
`ADA` is landless with 7 claims (`siyara harar arabi awbare dakkar dire_dawa
jeldesa`) and `SOA` with 4 (`ankober gendebelo nora_eth argobba_province`).
Shewa's Makhzumi sultanate is **896** [U] and unambiguous; "Adal" as a name is
13th c. [D], though Zeila as a Muslim port is much older [U].
**Recommendation: land BOTH** — SOA takes the Shewan plateau (12, from ETH) and
ADA takes Zeila and the Harar hinterland (12, from IFA). Both tags, both
colours, both loc rows are vanilla's; the cost is zero. **Counter:** ADA under
that name is as anachronistic as Ifat; the alternative is to land SOA only and
give Zeila's coast to `WAR`, at the price of a 21→33 Warsangali that is its own
invention.

**10. Kanem: keep Bornu, or make it an east-of-Chad power?**
KBO holds 32 — `kanem_area` 14 and `bornu_area` 18. The Sayfawa do not move to
Bornu until the 1380s, driven out of Kanem by the Bulala [U]; at 1066 Bornu is
Sao and pre-Kanuri country.
**Recommendation: KEEP ALL 32.** Vacating the 18 costs **76 `define_pop`**
entries — the second most expensive move in the theater — and the only real
recipient (`KOT`, the Sao) is a `type = pop` country whose conversion to a
landed tag is machinery this project has never used and cannot verify.
**Counter:** it leaves the theater's second-largest anachronism standing, and
the fix is otherwise trivial to describe.

**11. Great Zimbabwe (ZMW, 22 locations, 8 pop tributaries) — in scope or not?**
Great Zimbabwe's floruit is c. 1100-1450 and Mapungubwe's c. 1075-1220 [both D]
— at 1066 the Shona plateau has neither.
**Recommendation: OUT OF SCOPE, flagged for a southern Africa slice.** The
brief names five theaters and this is not one of them, `zimbabwe_region` is
83/109 unowned already, and the eight tributaries are pop countries whose
handling is unprecedented here. **Counter:** it is the clearest single
anachronism left standing in sub-Saharan Africa after this package lands, and
whoever reads the map next will see "Zimbabwe" on it.

**12. ZAN's rank — `rank_county` or `rank_duchy`?**
`rank_county_muslim` could not be located in `government_names_l_english.yml`
by direct grep (§F.3). If it does not exist, a county-rank Kilwa falls to
`rank_county` — **"County of Kilwa" ruled by a "Count"**, which is absurd on
the Swahili coast.
**Recommendation: `rank_duchy`** → `rank_duchy_muslim` (`country_ranks.txt:1743`,
`"Emirate"` / `"'Amīr"`, `government_names_l_english.yml:781-782`), verified to
exist. **Counter:** a five-location town at duchy rank is generous; if the
county-muslim branch does exist, county is the better size. **This is an OWED
CHECK, not a preference** — grep `country_ranks.txt` between `:2018` and the end
for a muslim county branch before choosing.

---

## Implementation checklist

Ordered so each step can be verified before the next.

1. **Registry overrides FIRST and alone** — copy
   `VAN/in_game/setup/countries/horn_of_africa.txt` (41 tags) and
   `west_africa.txt` (64 tags) into `MOD/in_game/setup/countries/`, change
   **one line** in the first (MAK `:244` `sunni` → `miaphysite`) and **seven**
   in the second (ZAM `:419`, KAN `:403`, KTS `:411`, GOB `:444`, RAN `:436`,
   DAA `:452`, ZZZ `:70`), each with an `iberia.txt`-style header comment.
   Diff both against vanilla and confirm the tag counts are unchanged
   (`grep -c "^[A-Z0-9]\{2,6\} = {"` → 41 and 64). Run the
   `verify-vanilla-override` skill. Ship and observe before anything else.
2. **Registry additions** — `DJN` (and `SNH`) appended to
   `zz_1066_new_countries.txt`. Count **65 → 66** (67 with SNH).
3. **Colours — none.** Re-run the key/RGB check in §A.4 before assuming it.
4. **Localisation** — 2 rows (4 with SNH), one physical line each, UTF-8
   **with** BOM.
5. **`_GENERATOR_OK`** — add DJN (and SNH) at `tools/verify_mod.py:925` with a
   tier-4 comment; the check at `:970-973` fails otherwise.
6. **`NEW_COUNTRIES`** — the one (two) blocks of §B.1. Re-read
   `subsaharan_muslim_monarchy_no_coast.txt` and its parent before shipping and
   restate anything they omit.
7. **`_AFRICA_RULES` + resolution loop** — modelled on the Central Asia loop
   (`tools/build_setup.py:5037`): resolve, assert the exact count per tag,
   assign into `LOCATION_GRANTS`, then assert each capital is in its own
   resolved list.
8. **`AFRICA_LANDLESS`** into `LANDLESS_AFTER` (`:2546`) — 9 tags (10 with AJU).
   **Four of the nine are side-effect retirements** (SGH, KBR, HRL, TDE) and
   exist only to satisfy the delta guard.
9. **`CAPITAL_FIXES`** — BBK → `diawara`. DFN is avoided by the `diara`
   `minus_singles` carve-out (§E.4); if the main session prefers the repoint,
   DFN → `kita`.
10. **`FIELD_FIXES`** — MAL, GHA, KBO, MAK, ETH, ZAN and the Hausa seven
    (§B.2). Thirteen entries. Every substring must be copied from the built
    file, not retyped.
11. **`n_landless_deps` 244 → 252** (`:6824`) — **observe it failing first**,
    per CLAUDE.md. `n_pacts` stays **9** (`:6851`): measured, no African pact
    exists.
12. **The repoint** — `MAL` → `GHA` for BBK, DFN, KBR, TFK, ZGH, in the
    Jurchen shape (`:6713-6724`), with `if n_ghana != 5`.
13. **Named strips** — 4 (MAL→GHA/SON/TKR/TMK deletions), 7 (KBO→Hausa),
    12 (ZAN→tributaries), 4 (ETH→southern) = **27 strips in four batches, each
    with its own exact-count assert**.
14. **IO** — `members = { ETH }` → `members = { ETH MAK ALO }` at the Alexandria
    patriarchate (`15_international_organizations.txt:376-392`). Depends on
    step 1.
15. **Harness** — the parliament check's `min_count = 1381`
    (`tools/verify_mod.py:1148`) should not move (no parliament is added or
    removed; `subsaharan_monarchy_no_coast` supplies
    `parliament_type = assembly` to both the old and the new includes) —
    **but verify, because seven Hausa include swaps and one ETH change all
    touch parliament-bearing templates.** Raise the registry check by 1-2.
    This package adds **zero** characters and **zero** dynasties under the
    recommended decisions, so those two checks stay put — worth a comment so
    the next reader does not think it was forgotten.

**Break-tests owed** (a check never seen failing is untested):

(a) a bogus location in `_AFRICA_RULES` must abort;
(b) an off-by-one `expected` must abort with the resolved count printed;
(c) **remove SGH from `AFRICA_LANDLESS` and watch the emptied-but-unlisted
delta guard (`:5652-5658`) fire** — this package is that guard's first real
workout and it has never been seen failing on a side-effect retirement;
(d) `n_landless_deps` left at 244 must abort with 252 printed;
(e) a repoint count of 4 or 6 instead of 5 must abort;
(f) each of the four named-strip batches must abort at the wrong count;
(g) point `LOCATION_GRANTS["SNH"]` at a location `ADA` also claims and watch
`_list_owner` (`:5322`) fire;
(h) break the `horn_of_africa.txt` override by dropping one tag block and watch
whatever registry-count check exists fail — **if none does, that is the check
this package owes** (a whole-file registry override that silently loses a tag
is exactly the class CLAUDE.md's silent-failure rule is about).

## Expected constant moves, collected

| constant | `file:line` | from | to (recommended) | to (all decisions maximal) |
|---|---|---|---|---|
| registry blocks | `zz_1066_new_countries.txt` | **65** | **66** (DJN) | **67** (+SNH) |
| registry overrides | `MOD/in_game/setup/countries/` | 3 files | **5 files** | 5 |
| `NEW_COUNTRIES` count | `build_setup.py:466` | current | **+1** | **+2** |
| `LANDLESS_AFTER` | `:2546` | current | **+9** | **+10** (AJU) |
| `n_landless_deps` | `:6824` | **244** | **252** | 252 |
| `n_pacts` | `:6851` | **9** | **9 — unchanged, measured** | 9 |
| repoints (new batch) | new, `:6713` shape | — | **5** | 5 |
| named dependency strips | new, `:6676` shape | — | **27** in 4 batches | 27 |
| `CAPITAL_FIXES` | `:2600` | current | **+1** (BBK) | +2 (DFN) |
| `FIELD_FIXES` | `:2653` | current | **+13** | +15 |
| `CONTROL_STRIPS` | `:1659` | 1 tag | **unchanged — no African double-ownership** | unchanged |
| `LOCATION_VACATED_EXPECT[*]` | `:1237`, `:1364`, `:1390` | — | **unchanged** | unchanged |
| locations granted | build report | current | **+161** | +177 (KAB→TKR) |
| locations vacated | build report | current | **+0** | +0 |
| unowned locations | — | current | **−9** (SNH fills the Adrar) | −9 |
| IO members | `15_international_organizations.txt:380` | ETH | **ETH MAK ALO** | same |
| parliament check `min_count` | `verify_mod.py:1148` | **1381** | **verify — expected unchanged** | unchanged |
| new characters / dynasties | — | — | **0 / 0** | 1 / 1 (Tunka Manin + `cisse_dynasty`) |

---

## Verification statements

Per CLAUDE.md's say-what-you-verified rule.

- **Verified — the resolver.** An independent reimplementation of
  `_parse_defs` (`tools/build_setup.py:711`), `_ownable_set` (`:736`),
  `_resolve_ruleset` (`:779`), `find_block_end` (`:4896`) and the
  `OWN_KEYS`/`COUNTRY_RE` reader (`:5091`/`:4791`) reproduces the Baltic
  package's published counts (`samogitia_area` 16, `courland_province` 8),
  finds 20,922 ownable locations, and reads **2337 country blocks in vanilla,
  2402 in the mod** — matching CLAUDE.md's own figure.
- **Verified — the template parser**, by asserting `cult['dadu'] ==
  'yan_culture'`; `location_templates.txt` blocks are single-line and a
  line-anchored culture regex returns zero on all 20,922 entries.
- **Verified — the tag scanner**, by feeding it GHA, MAK, ETH, ZAN (all four
  TAKEN with their registry `file:line`) and PRU (TAKEN on 99 word hits with
  an **empty registry** — the formable-only class).
- **Verified — sub-Saharan Africa is untouched by this mod.** Zero references
  to any of the twelve African region names in `tools/build_setup.py`, and zero
  string literals naming any of the 197 tags in vanilla's five African registry
  files. The only African tags the build knows are `BKZ` (`:2020`) and `FZA`.
- **Verified — MAL's thirteen vassals**, `MOD/main_menu/setup/start/12_diplomacy.txt:249-261`,
  and their NAME keys in `VAN/main_menu/localization/english/country_names_l_english.yml`
  at the lines given in §0.1. **Verified — `ZAN: "Kilwa"` (`:1385`) and
  `ZZB: "Zanzibar"` (`:1421`).**
- **Verified — KBO ships the Sayfawa.** `dynasty = sayfawa_dynasty`,
  `capital = njimi`, `country_rank = rank_empire`,
  `reforms = { banu_hummay_amendments }` and six Sayfawa `regnal_numbers`
  in the mod's KBO block; `banu_hummay_amendments` at
  `VAN/in_game/common/government_reforms/country_specific.txt:1391`,
  `potential = { has_or_had_tag = KBO }`.
- **Verified — MAK is Muslim in vanilla's registry.**
  `VAN/in_game/setup/countries/horn_of_africa.txt:240-245`,
  `culture_definition = nubian`, **`religion_definition = sunni`**; its
  `10_countries` block carries `include = "subsaharan_muslim_monarchy_no_coast"`,
  `sharia_law = shafii_policy`, `religious_school = shafii_school` and
  `heir_selection = matrilineal_non_exclusive`. ALO (`:224-229`) is
  `miaphysite` with `liturgical_language = geez_language` and the same
  matrilineal succession.
- **Verified — the Hausa contradiction.** All seven Hausa registry blocks carry
  `religion_definition = sunni` (`west_africa.txt:398-453`) while **all 41
  `hausa`-culture locations carry `religion = bori_religion`** in
  `location_templates.txt`. `bori_religion` is real:
  `in_game/common/religions/folk_african.txt:57`.
- **Verified — the render laws.** `country_name_construction.txt` is 188 lines,
  first-match; `:79-89` is tag-gated on **MAL** + monarchy + kingdom/empire with
  map string `"$PREFIX$ $NAME$ $RANK$"` (`government_names_l_english.yml:7-8`);
  `:159-164` catches every muslim-group country and redirects to
  `prefix_rank_of_name`, whose **map string is bare `"$NAME$"`** (`:12`).
  `country_ranks.txt` is 2741 lines, first-match, with the African branches at
  `:335`, `:496`, `:506`, `:957`, `:967`, `:976`, `:987`, `:1162`, `:1887`,
  `:1897`, `:1907` — **all CULTURE- or COURT-LANGUAGE-gated, none tag-gated**.
  `rank_duchy_tribe` (`:1606`) precedes `rank_duchy_muslim` (`:1743`), which
  precedes `rank_duchy_ethiopia/kanem/mali` (`:1887/1897/1907`); at kingdom rank
  `rank_kingdom_kanem` (`:957`) and `rank_kingdom_mali` (`:967`) **precede**
  `rank_kingdom_muslim` (`:1060`). Loc values quoted in §F.2 are from
  `government_names_l_english.yml` at `:193-195`, `:208-209`, `:218-219`,
  `:463-464`, `:563-567`, `:587-589`, `:781-782`, `:790-791`, `:837-845`.
- **Verified — no African tag is tag-gated in `country_ranks.txt`.** Every
  `tag = ` line in that file was listed; the only Africa-adjacent one is
  `:395 tag = MOM # Momboares`, a Kongo tag out of this package's scope.
- **Verified — the formables.** `MAL_f` (`00_formable_countries.txt:4467`,
  `potential = { culture.language = language:mande_language }`,
  `areas = { mali_area ghana_area }`, `required_locations_fraction = 0.75`),
  `NUB_f` (`:4495`), `SOI_f` (`:4383`), `HAU_f` (`:3151`), `SKO_f` (`:3120`,
  `potential` requires `religion = religion:sunni`), `ETH_f` (`:1208`,
  requires `religion = religion:miaphysite`), `MSI_f` (`:1151`), `BEJ_f`
  (`:1178`, five named locations). `soninke`'s language is `mande_language`
  (`cultures/west_african.txt:24-25`), which is what makes Ghana→Mali live.
  **`MSI`, `BEJ`, `NUB`, `SOI`, `HAU`, `SKO`, `KON` have no registry block and
  no `10_countries` block** — the PRU class.
- **Verified — the IO.** `MOD/main_menu/setup/start/15_international_organizations.txt:376-392`
  is an `autocephalous_patriarchate`, `creation_date = 451.1.1`,
  `members = { ETH }`, `variables = { religion = religion:miaphysite
  seat = location:alexandria }`. **ETH is the only African tag in any IO member
  list in the file** — all 80 theater tags were scanned.
- **Verified — the diplomacy.** 348 `dependency` lines and 28
  `scripted_mutual`/`scripted_oneway` lines in the mod file; **exactly 50 name
  a sub-Saharan African tag**, enumerated in §G. `_drop_landless_dep`
  (`:6756-6765`) drops on **either** side being in `LANDLESS_AFTER`; the
  repoint precedent is `:6713-6724` (46 Jurchen) and `:6735-6748` (16 jimi),
  both with exact-count asserts. `n_landless_deps` is asserted at **244**
  (`:6824`) and `n_pacts` at **9** (`:6851`).
- **Verified — no African double-ownership.** The game-wide set is ten
  locations (six LIT/TEU, four TLE/MOR), already recorded in
  `tools/build_setup.py:1652-1659`. No tag in this package carries a `control`
  block naming another tag's land.
- **Verified — 45 African `type = pop` countries**, including all eight of
  ZMW's "tributaries" (KLG TNA SEN TSG MNY ZEZ NBY VED, `12_diplomacy.txt:239-246`),
  plus KOT (Sao), ZGW (Zaghawa), BGI, MDR, YAO, TRG, MNK, LIP, ORO, AFR, SDQ,
  FNJ, GUM, KUN, VAZ, BTS, VEZ, VIL, TKE, ABD, CBD, YAK, CEW. **A dependency
  may name a pop country** and the landless sweep does not remove it.
- **Verified — 39 African landless-with-claims tags**, with the nine relevant
  claim lists quoted verbatim in §A.1. Claim lists accept **container names**
  as well as location names (`argobba_province`, `enderta_province`,
  `gojjam_province`, `bale_province`, `hadiya_province`, `sidamo_province`,
  `shewa_province`, `afar_province`).
- **Verified — `DAH` (`west_africa.txt:514`) and `KEB` (`:422`) are landless
  with NO claims**, KEB via an empty `own_control_core = { }`. Two vanilla
  countries in the state `initialize_from_bookmark.cpp:592` is supposed to
  reject. Worth a look at first launch; not this package's problem.
- **Verified — the colours.** All fourteen `map_*` keys in §A.4 exist at the
  lines given in `VAN/main_menu/common/named_colors/02_map.txt`;
  `map_lamtuna`, `map_godala`, `map_messufa` and `map_soninke` are used by **no
  country** in vanilla or the mod (checked across every `color = <key>` in both
  `setup/countries` trees), while `map_sao` and `map_zaghawa` ARE used
  (`west_africa.txt:475`, `:499`). **`map_djenne` and `map_dia` do not exist.**
- **Verified — pop costs.** `VAN/main_menu/setup/start/06_pops.txt` has 28,559
  location blocks and 50,227 `define_pop` entries. The vacate candidates cost:
  `gambia_area` 18 locations / 48 pops; AJU's interior 20 / 44;
  `bornu_area`'s KBO 18 / 76; the Mossi 47 / 152; ZAN's outer 16 / 43. The
  recommended package vacates **nothing**.
- **Verified — the templates.** `subsaharan_monarchy_no_coast.txt` declares
  `type = monarchy` and `heir_selection = cognatic_primogeniture`;
  `subsaharan_monarchy.txt` (coastal) declares **neither**;
  `subsaharan_muslim_monarchy_no_coast.txt` is the former plus
  `legal_code_law = sharia_law_policy` and `immigration_law = open_borders_law`.
  `expl_west_africa_muslim.txt` carries `sahel_region` in `discovered_regions`.
- **Verified — the mod's registry-override precedent.**
  `MOD/in_game/setup/countries/iberia.txt:1-13` is a whole-file override of
  vanilla's 10-tag file with a **single** changed line and a header comment
  naming the Gallura/`italy.txt` precedent. The mod ships three such overrides
  today (`iberia.txt`, `italy.txt`, `east_asia.txt`).
- **Verified — `CONTROL_STRIPS` has landed** (`tools/build_setup.py:1659`),
  the emptied-but-unlisted delta guard exists (`:5652-5658`), `FIELD_FIXES`
  (`:2653`), `CAPITAL_FIXES` (`:2600`), `LANDLESS_AFTER` (`:2546`),
  `_bad_recip` (`:5391`), `n_landless_deps` (`:6824`), `n_pacts` (`:6851`),
  registry count 65, parliament `min_count = 1381` (`verify_mod.py:1148`).
- **NOT verified, and stated as such — every historical claim carrying `[U]` or
  `[D]`:** al-Bakri's date (1067-68) and his account of Tunka Manin, Basi and
  the matrilineal succession; the sack of Awdaghust (1054/55); Tabfarilla
  (1056) and Yahya ibn Umar's death; War Jabi's conversion (c. 1040) and his
  son's name; Hummay's accession (1067-1097 [D]); the Duguwa/Sayfawa break and
  Abd al-Jalil; Kanem's move to Bornu (1380s); Sundiata (c. 1235) and the
  Kouroukan Fouga; Segou's Bambara state (c. 1712); Jolof (c. 1350); Kaabu
  (c. 1235); Timbuktu's foundation (c. 1100); Djenné-Jeno's occupation span;
  the Hausa king-lists and the 14th-century arrival of Islam; the Mossi
  founding dates; Ife/Nri/Benin/Oyo; the Makurian king Solomon and his 1079
  abdication; Dongola's fall (1317); Al-Abwab's 1270s breakaway; al-Yaqubi's
  Beja kingdoms; the Daju dynasty's dating; Ethiopia's Gudit disruption
  (c. 960), the Zagwe (c. 1137), Mara Takla Haymanot, Kubar as the capital, and
  the Solomonic restoration (1270); the Makhzumi sultanate of Shewa (896) and
  its destruction (1285); the Walashma of Ifat (c. 1285); Ajuran's dating;
  Mogadishu's, Kilwa's, Sofala's and the Benadir towns' foundation traditions;
  the Kilwa Chronicle's Shirazi dates and the Mahdali takeover (1277); Great
  Zimbabwe (c. 1100-1450) and Mapungubwe (c. 1075-1220); the Chwezi/Kitara
  traditions; and the claim that Nubian bishops were consecrated at Alexandria.
  Every one rests on the agent's own history and needs a source before it
  enters a comment, let alone setup data.
- **NOT checked, and OWED before implementation:**
  (1) **whether `court_language` defaults from the primary culture** — it
  decides whether `rank_kingdom_ethiopia` (`country_ranks.txt:1162`) is
  reachable at all, and therefore whether ETH's ruler reads "Negus" or "King";
  measured: zero of vanilla's 347 `court_language` lines set
  `ethiopic_language`;
  (2) **whether a `rank_county_muslim` branch exists** in `country_ranks.txt`'s
  county section (`:2018`+) — it decides ZAN's rank (OPEN DECISION 12);
  (3) **whether `country_exists = c:MAL` is true for a landless-with-claims
  MAL** — it decides whether `MAL_f` can be formed while the landless shell
  lives, and the same question is open for GHA→MAL under decision 1;
  (4) **whether the engine validates a setup `reforms = { }` entry against the
  reform's own `potential`** — MAL ships `manden_kurufa_reform` whose potential
  is `has_advance = kouroukan_fouga_advance`, which a 1066 MAL will not have;
  (5) **whether the harness has a check that a whole-file registry override
  preserves its tag count** — if not, break-test (h) is the check this package
  owes.
