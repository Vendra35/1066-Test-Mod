> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 37 (commit b3f3665) —
> NOT yet game-tested.** Research record, not the state. KNOWN DEVIATIONS,
> code wins: **the package's country reader missed `own_control_integrated`
> blocks** (build_setup.py:5388's OWN_KEYS has TEN members), so —
> **UNOWNED_GRANTS is DEAD**: the "ten vanilla-unowned Khorat/Mekong
> locations" are VTN's 7 + MUA's 3 integrated holdings, every granted
> location carries exactly one ownership entry, §E.3/checklist-7/break-test
> (e) are void; holdings corrections: VTN **32** (its §0.5 "correction" of
> INDIA-CHINA-REVIEW's 32 is WITHDRAWN — the 57-not-56 finding stands),
> PLB 40, JMB 12, MUA 15, BEI 7, LGK 9, **MGD 5 not 1** (five locations to
> KIM), **BTU 6 not 1** (it already holds the Agusan coast — decision 9's
> growth counter was moot); theater stats: 893 owned / **151** unowned
> (not 831/213), khorat 0, Borneo 34, Philippines 54, Celebes 2 unowned.
> **§G.2 and §G.4 contradicted each other** (the repoint + the PLB→PNI
> pair = two overlords on PNI, the HLL class): resolved as decision 13 —
> `:425` stripped by name, uniform five-pair tributary list. Decisions as
> implemented: 1 five, 2 PLB, 3 kingdom, 4 mon, 5 as-costed, 6 nobody,
> 7 retire→LGE, 8 alive, 9 MNA/MGD retire + SUL stays, 10 keep,
> **11 DECLINED (kawali stays)**, 12 coastal + TSM folds. Landless is
> SIXTEEN, ghosts 155 (MNA sits in shaivism — §G.1's "154 maximal" was
> wrong), deps 265, grants 249. `adh_narai`: vanilla's own LAV block
> terms him from 1082.1.1 — the cross-tag seat is vanilla-endorsed, the
> [D] 1052 accession ours; `_ACC_EXEMPT` born in verify_mod. OWED CHECK 1
> (dialect→language, the Mahārājā render) is in the item-37 click tour.
> The §I harness gap was real TWICE OVER: the gate check also read only
> inline reforms and only mod reform files — extended to nested template
> chains + vanilla reforms; break-test (i) confirmed nothing caught a
> drained IO — the pinned-9 empty-members check now does (proven).

# SOUTHEAST ASIA 1066 — Anawrahta's Pagan, the Srivijayan mandala, Java split in two (DRAFT)

**Research agent model ID: `claude-opus-5`.**

**DRAFT — pending main-session review. Nothing here has been written into any
mod file.** Produced by an Opus research agent, 2026-08-02, against the working
tree at commit `0a91142` (36 items landed, working tree clean). Every mechanical
claim carries a `file:line`. Historical claims that no file can settle are
flagged `[U]` (unverified / the agent's own history, no source in the repo) or
`[D]` (sources genuinely differ), never asserted silently. §VERIFICATION
collects them.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, 491,179 bytes, present)
`MOD = .../1066 Test Mod`

**Method.** Counts come from an independent reimplementation of
`build_setup.py`'s parsers — `_parse_defs` (`tools/build_setup.py:721`),
`_ownable_set` (`:745`), `_resolve_ruleset` (`:788`), `find_block_end`
(`:5193`) and the `OWN_KEYS`/`COUNTRY_RE` country reader (`:5246`, and the
`OWN_KEYS` tuple `build_countries` walks) — all reading
`encoding='utf-8-sig'`, all token/brace based, comments masked before
tokenising. Scripts live in the session scratchpad (`sea.py`, `resolve.py`,
`tagfast.py`, `reg.py`); nothing was written into the repo.

**Proven on known positives.** Before any new ground was measured the tooling
was fed figures other packages had already published:

| probe | expected (source) | measured |
|---|---|---|
| ownable locations | 20,922 (`AFRICA-PACKAGE.md` §VERIFICATION) | **20,922** |
| vanilla country blocks | 2,337 (CLAUDE.md, `AFRICA-PACKAGE.md`) | **2,337** |
| mod country blocks | 2,404 (`HANDOFF.md:1780`) | **2,404** |
| `samogitia_area` ownable | 16 (`BALTIC-PACKAGE.md:55`) | **16** |
| `courland_province` ownable | 8 (`BALTIC-PACKAGE.md:853`) | **8** |
| `cult['dadu']` | `yan_culture` (Northern Dynasties) | **`yan_culture`** |
| `06_pops.txt` location blocks / `define_pop` | 28,559 / 50,227 (`AFRICA-PACKAGE.md` §E.3) | **28,559 / 50,227** |
| tag scanner, `GHA` | VAN-sub 62, VAN-en-loc 1, registry `west_africa.txt:251` | **62 / 1 / `west_africa.txt:251`** |
| tag scanner, `MAK` | VAN-sub 50, en-loc 1, `horn_of_africa.txt:240` | **50 / 1 / same** |
| tag scanner, `ZAN` | VAN-sub 134, en-loc 13, `east_africa.txt:2` | **134 / 13 / same** |
| tag scanner, `TMB` | VAN-sub 48, en-loc 1, `west_africa.txt:302` | **48 / 1 / same** |
| tag scanner, `PRU` | VAN-sub 429, en-loc 26, **empty registry** (formable-only) | **429 / 26 / empty** |

One column deliberately differs and is named so nobody reconciles it by
mistake: my **VAN word** column counts *occurrences* over all text files,
where `AFRICA-PACKAGE.md`'s counted a narrower set (its `PRU` row reads 99
where mine reads 332). The substring and English-localisation columns — the
two the free/taken verdict actually rests on — reproduce exactly.

**Scope.** `indochina_region` and `indonesia_region` — together vanilla's
`south_east_asia` sub-continent (`definitions.txt:4334`, whose only two
children are those two regions). **1,044 ownable locations, 831 owned by 125
tags, 213 unowned, ZERO double-ownership.** Named as flagged seams and NOT
touched: Đại Việt (DAI), Champa (CHA), the Khmer (KHM) beyond a 24-location
Khorat edge, Korea and Japan — all done in items 30/32/33 — and the Chola
world (item 34).

---

## 0. Ground truth — and the five findings that shape the package

### 0.1 THE HEADLINE: vanilla already ships the Srivijayan mandala. It just hangs it off Majapahit.

`MOD/main_menu/setup/start/12_diplomacy.txt:424-427` gives MAJ four Sumatran
and Riau vassals, and `:425` gives one of them a vassal of its own. Read their
NAME keys (`VAN/main_menu/localization/english/country_names_l_english.yml`):

| tag | loc line | NAME | what it actually is |
|---|---|---|---|
| **PLB** | `:3947` | **Palembang** | Srivijaya's own capital; 34 locations, `mahayana`, `malay_culture` |
| **JMB** | `:3925` | **Melayu** — *not* "Jambi" | the Malayu kingdom, San-fo-qi's other seat [D] |
| **PNI** | `:3933` | **Pannai** | the Srivijayan Batak-coast mandala named in the 1030 Tanjore inscription [D] |
| **INR** | `:3937` | Indragiri | a Riau river polity |
| **SGT** | `:3939` | Siguntur | capital `dharmasraya`, `mauli_dynasty` — the Melayu successor house |
| **BUS** | `:3935` | Barus | the camphor port; the Lobu Tua inscription is 1088 [D] |

Vanilla built the 1337 Malay world out of the eleventh century's own polities
and then subordinated the whole set to a **Majapahit founded in 1293** [U].
And it went further: `15_international_organizations.txt:1013-1030` ships a
**Mūlasarvāstivāda sect** whose members are `JMB BUS INR SGT PLB MYI PGS PAH
MUA PNI` and whose provinces are `johor_province lower_jambi_province` — the
Srivijayan Buddhist world, listed by name, at 1337.

**So the 1066 maritime correction is mostly a DIPLOMACY correction, not a
territory one** — exactly the shape `AFRICA-PACKAGE.md §0.1` found in the
Sahel, and `build_setup.py` already owns the mechanism: the **repoint**,
attested twice (`:7058-7072` 46 Jurchen `CHI`→`LIA`; `:7085-7097` 16 jimi
`LNG`→`CHI`, both with exact-count asserts) and the named strip
(the KBO→Hausa batch, `:7140-7151`).

Two more of the same shape:

- **`malacca`, `pagan`, `thaton`, `daha`, `dharmasraya`, `kota_kapur`,
  `pannai`, `butuan`, `lamphun`, `lopburi`, `weithali`, `temasek`, `barus`,
  `borobudur` and `trowulan` are all real locations** (resolved from
  `definitions.txt`). The eleventh century's own place-names are on this map.
- **`pagan_dynasty` ships in vanilla** (`04_dynasties.txt:8354`,
  `home = pagan`, loc `dynasty_names_l_english.yml:1003` → `"Pagan"`), and so
  do `lavo_dynasty` (`:8309`, `home = ayodhya`), `mauli_dynasty` (`:8407`,
  `home = dharmasraya`), `singhanavati_dynasty` (`:8314`, `home =
  chiang_saen`) and `bali_dynasty` (`:8412`). Vanilla ships the pre-1337
  houses and never seats them.

### 0.2 THE SECOND HEADLINE: vanilla ships two SEA characters who are ADULTS in 1066, and nobody has noticed

Scanning all 192 `tag =` blocks in `VAN/main_menu/setup/start/05_characters.txt`
that name a Southeast Asian tag, **exactly two are born on or before 1050**:

```
	adh_narai = {
		first_name = { name = name_narai }
		culture = thai_culture
		religion = theravada
		birth_date = 1020.1.1 #Unknown
		birth = lopburi
		death_date = 1087.1.1 #Exact date unknown
		dynasty = lavo_dynasty
		tag = ADH
	}
	adh_luang = {                     # father = adh_narai
		birth_date = 1050.1.1 #Unknown
		birth = lopburi
		death_date = 1111.1.1
		dynasty = lavo_dynasty
	}
```

The third-earliest SEA birth is 1070 (`lav_kraisornrat`); the fourth is 1100.
Both `name_narai` and `name_luang` exist as keys
(`VAN/main_menu/localization/english/character_names_dynamic_l_english.yml:21872-21873`),
`lavo_dynasty` exists, `lopburi` exists — and **the mod's own death-strip has
already removed both death dates** (`MOD/main_menu/setup/start/05_characters.txt`,
both blocks, verified by diff against vanilla). Narai is 46 at start, Luang is
16 — exactly `ADULT_AGE` (`tools/build_setup.py:6731`).

**This is the theater's Tunka Manin, and it costs ZERO authoring.** One
`HISTORICAL_RULERS` row. See §C.

### 0.3 The third finding: the tributary gate is FREE for this entire theater

`VAN/in_game/common/government_reforms/country_specific.txt:3894-3915`:

```
mandala_system = {
	major = yes
	potential = {
		capital.sub_continent = sub_continent:south_east_asia
		OR = { religion.group = religion_group:dharmic
		       religion = religion:theravada
		       religion = religion:mahayana
		       religion = religion:satsana_phi }
	}
	country_modifier = {
		cultures_capacity = 3
		monthly_towards_decentralization = societal_value_minor_monthly_move
		allow_tributary_subject = yes
	}
	years = 4
}
```

**And all four of the theater's monarchy templates already carry it in a
`reforms = { }` block** — `VAN/main_menu/setup/templates/`
`south_east_asia_monarchy.txt:43`, `south_east_asia_monarchy_no_coast.txt:40`,
`indonesia_monarchy.txt` (last block) and `indonesia_monarchy_no_coast.txt:65`,
each resolving to exactly `mandala_system`. The `_no_mandala` variants
(`south_east_asia_monarchy_no_mandala_no_coast.txt`,
`indonesia_monarchy_no_mandala.txt`, `indonesia_muslim_monarchy_no_mandala.txt`)
are the ones that drop it, and `indonesia_muslim_monarchy_no_mandala.txt:1` is
a bare `include = "indonesia_monarchy_no_mandala"` — Paradox's own
acknowledgement that a Muslim SEA state cannot hold the reform (its `potential`
demands a dharmic/Buddhist religion).

**Consequence:** the Srivijayan mandala can ship as REAL `subject_type =
tributary` lines, not downgraded vassals, with **no new reform** — the fourth
independent confirmation of KNOWLEDGE's modifier branch of the visible gate
(`common/subject_types/tributary.txt:19-24`), and the first time it arrives
from a vanilla template rather than one this project wrote.

### 0.4 The fourth finding: ZERO tag-gated rank branches, and a culture-gated one that is a gift

Every `tag = ` line in
`VAN/in_game/common/customizable_localization/country_ranks.txt` (2,741 lines,
first-match) was listed. **Not one names a Southeast Asian tag.** The MAL/LIT
trap (`KNOWLEDGE.md`, "A tag-gated RANK branch can sit above the generic ones")
does not exist here.

What DOES exist is culture/language-gated, and one branch is worth the whole
package:

| branch | line | trigger | loc |
|---|---|---|---|
| `rank_kingdom_indian` | **`:1072`** | kingdom + (`indic`/`dravidian` family **or `this = language:malay_language`**) | **"Mahārājya"**, ruler **"Mahārājā"** (`government_names_l_english.yml:467-469`) |
| `rank_duchy_indian` | `:1755` | duchy + same | "Rāj" / "Rājā" (`:752-754`) |
| `rank_county_indian` | `:2336` | same OR-set, **no rank gate of its own** | "Thikana" / "Thakur" (`:997-999`) |
| `rank_duchy_thai` | `:1998` | duchy + `culture_group:thai_group` | "Principality" / **"Chao"** (`:879-881`) |
| `rank_county_thai` | `:2513` | county + `thai_group` | "Lordship" / "Chao" (`:1049-1051`) |
| `rank_county_barangay` | `:2505` | county + `philippine_language_family` | **"Barangay"** (`:1047`) — see the trap in §F.2 |

**A Malay-culture, non-Muslim kingdom renders "Mahārājya of Palembang" ruled by
a "Mahārājā".** That is Srivijaya's own title, shipped by Paradox, reachable
with one `country_rank = rank_kingdom` line. §F.3 walks it to the string.

### 0.5 Southeast Asia is UNTOUCHED ground for this mod

**Measured: `tools/build_setup.py` contains ZERO references to
`indochina_region` or `indonesia_region`, or to any of their twenty-one areas,
and no string literal naming any of the 141 tags registered in
`south_east_asia.txt` (57) and `indonesia.txt` (84).** The only theater-adjacent
tags the build names are `DAI`, `CHA`, `KHM`, `CDL`, `MLM` and `MMA`, all from
the China-East slice (`:1380-1423`, `HISTORICAL_RULERS`). MOD ownership across
every SEA area is byte-identical to vanilla except where DAI's out-of-theater
Yunnan holdings were taken (item 32 — DAI's 53 *Indochinese* locations are
untouched, `INDIA-CHINA-REVIEW.md:41`).

**A correction to `docs/INDIA-CHINA-REVIEW.md` §2.3, recorded here so the next
reader does not inherit it:** that document says "the whole SEA set is
`south_east_asia.txt`'s **56** tags". It is **57** (`KHM` is the file's first
block and sits behind the BOM — the `^`-anchored-grep class,
`KNOWLEDGE.md`, "Registry first lines hide behind the BOM"). The same section
gives VTN 32 locations; the measured figure in the current build is **25**.

### 0.6 Template culture and religion, measured per area

Ownable counts resolved from `definitions.txt`; culture/religion from
`location_templates.txt`; owners from `MOD/main_menu/setup/start/10_countries.txt`.
`define_pop` from `VAN/main_menu/setup/start/06_pops.txt`.

| area | ownable | pops | owners today | template cultures | template religions |
|---|---|---|---|---|---|
| `arakhan_area` | **19** | 63 | ARK 17, TWI 1, unowned 1 | `rakhine_culture` 19 | `theravada` 19 |
| `irrawady_area` | **36** | 122 | PIN 25, SAG 5, BPR 3, TNG 2, KAL 1 | `burmese` 32, `zo` 2, `tai_nua` 1, `karen` 1 | `theravada` 32, `mizo` 2, `satsana_phi` 1, `karen` 1 |
| `irrawady_delta_area` | **35** | 101 | PEG 28, TSM 7 | `mon_culture` 33, `karen` 2 | `theravada` 33, `karen` 2 |
| `chao_phraya_area` | **36** | 99 | SUK 18, LAV 9, SPN 5, PTC 3, ADH 1 | `thai` 29, `karen` 4, `khmer` 2, `dambro` 1 | `theravada` 32, `karen` 4 |
| `northern_tai_highland_area` | **38** | 97 | LNA 19, MUA 11, PHY 2, SUK 2, PUA 2, CHH 1, CBK 1 | `khon_muang` 19, `lao` 7, `dai` 4, `karen` 3, … | `theravada` 21, `satsana_phi` 9, `mahayana` 4, … |
| `shan_highland_area` | 39 | 134 | HSE 10, MNI 5, HSI 4, unowned 4, MGT 3, SAG 2, … | `tai_long` 16, `tai_nua` 9, `karen` 4, … | `satsana_phi` 28, `karen` 4, … |
| `kachin_area` | 25 | 79 | unowned 5, MKA 5, MKN 3, MYA 3, HKM 3, … | `tai_nua` 14, `naga` 6, `jingpo` 4 | `satsana_phi` 14, `naga` 6, `jingpo` 4 |
| `khorat_plateau_area` | **65** | 278 | KHM 29, VTN 25, unowned 10, MUA 1 | `khmu` 17, `bru` 16, `kuy` 15, `khmer` 9, `lao` 6 | `satsana_phi` 32, `bru` 16, `theravada` 9, `mahayana` 6 |
| `lower_mekong_area` | 49 | — | **KHM 49** | `khmer` 46, `bahnar` 3 | `theravada` 46 |
| `red_river_delta_area` | 57 | — | DAI 49, CBK 8 | `vietnamese` 35, `zhuang` 8, `muong` 7, `dai` 7 | `mahayana` 35, … |
| `champa_area` | 29 | — | CHA 21, DAI 4, KHM 4 | `cham` 17, `degar` 7, … | `hindu` 17, … |
| `malay_peninsula_area` | **43** | 154 | LIG 15, PAH 11, LGK 8, KED 3, MNJ 3, SNG 1, BES 1, unowned 1 | `malay` 19, `dambro` 12, `orang_asli` 12 | `theravada` 12, `orang_asli` 12, `hindu` 9, `mahayana` 7, **`sunni` 3** |
| `south_sumatra_area` | **83** | 254 | PLB 34, unowned 16, JMB 9, SGT 8, INR 6, SNG 5, ARU 5 | `malay` 27, `minangkabau` 17, `lampung` 10, `orang_rimba` 10, … | `mahayana` 28, `minangkabau` 16, `piil_pesenggiri` 10, … |
| `north_sumatra_area` | **50** | 162 | ARU 19, BUS 7, PNI 7, ATJ 6, PSA 5, unowned 4, LGE 2 | `batak` 14, `malay` 14, `acehnese` 11, `minangkabau` 5, … | `mahayana` 15, `pelebegu` 14, `hindu` 9, `minangkabau` 5, **`sunni` 3** |
| `java_area` | **49** | 122 | MAJ 32, SUN 17 | `javanese` 28, `sundanese` 17, `madurese` 4 | **`hindu` 49** |
| `lesser_sunda_area` | 34 | 82 | unowned 19, WHL 4, BLI 3, SLP 2, … | 20 cultures | `hindu` 7, `wetarese` 6, … |
| `south_borneo_area` | 67 | 147 | unowned 24, TJP 14, NSR 12, KRP 8, SMB 5, … | `ngaju` 18, `banjar` 15, `malay` 14, `bidayuh` 13 | `kaharingan` 33, `hindu` 32, … |
| `north_borneo_area` | 76 | 243 | unowned 33, TDG 11, MRP 10, MNU 5, SBG 5, **BEI 4**, … | `kayan` 20, `dusun` 13, `iban` 9, … | `kan_khwan` 20, `pengarap_asal` 14, … |
| `celebes_area` | 59 | 242 | unowned 10 + 21 one-to-nine-location tags | 20 cultures | 11 folk religions |
| `moluccas_area` | 32 | 72 | unowned 21, JLO 5, MOO 2, TER 1, LOL 1, TID 1, BAC 1 | 12 cultures | 6 folk religions |
| `luzon_area` | 57 | 179 | unowned 30, IBL 6, MYI 6, TDO 5, PGS 4, … | `tagalog` 13, `aeta` 6, `bicolano` 5, … | **`anitism` 53**, `hindu` 3, `mahayana` 1 |
| `visayas_area` | 26 | 65 | unowned 13, MDY 8, CEB 3, BOL 2 | `hiligaynon` 8, `waray` 8, … | `anitism` 24, `hindu` 2 |
| `mindanao_area` | 40 | 130 | unowned 22, SML 6, KIM 4, LNO 3, SUL 2, **BTU 1**, MGD 1, KML 1 | 14 cultures | `anitism` 37, `hindu` 3 |

Five things this table settles:

- **Java is 49/49 `hindu` in the template data** — vanilla already models
  pre-Islamic Java, which is the 1066 posture inherited free. The Islamisation
  of Java is 15th-16th century and vanilla did not paint it.
- **There is almost no `sunni` in the theater's location data: three locations
  in `malay_peninsula_area` (all `kedah_province`) and three in
  `north_sumatra_area` (`bandar_aceh`, `pasai`, `kota_rentang`).** Six
  locations out of 1,044. But **five COUNTRIES carry
  `religion_definition = sunni`** — ARU, ATJ, PSA, KED, LGE — and four of them
  are anachronistic at 1066. Unlike the Hausa case, here the map data mostly
  AGREES with the registry; the anachronism is the tags' *names and dates*, not
  a data contradiction (§D.3, OPEN DECISION 7).
- **The Philippines are `anitism_religion` on 114 of their 123 ownable
  locations** — vanilla's animist model is 1066-correct and free.
- **213 of the theater's 1,044 locations are already unowned**, concentrated in
  Borneo (57), the Philippines (65), the Moluccas (21) and the Lesser Sundas
  (19). Vanilla's own stateless model, and the Pecheneg discipline says leave it.
- **The theater's pop density is LOW.** The whole `chao_phraya_area` is 99
  `define_pop` for 36 locations; `java_area` is 122 for 49. Compare Africa's
  `bornu_area` at 76 for 18. A vacate here is cheaper per location than
  anywhere the project has worked — but this package still vacates zero.

### 0.7 The religions, cultures and dynasties that already exist — nothing needs authoring

Cultures used below, all shipped (`VAN/in_game/common/cultures/`):
`burmese_culture` (`south_east_asia.txt:124`, `language = burmese_language`,
group `tibeto_burman_group`), `mon_culture` (`:94`, `mon_language`,
`austroasiatic_group`), `rakhine_culture` (`:109`, `burmese_language`),
`khmer_culture` (`:1`), `thai_culture` (`:47`, `thai_dialect`, `thai_group`),
`khon_muang_culture` (`:79`, `thai_dialect`, `thai_group`), `lao_culture`
(`:183`), `dambro_culture` (`:64`), `tai_long_culture` (`:198`, groups
`shan_group thai_group`), `malay_culture` (`:424`, **`language =
malay_dialect`**, `austronesian_group`), `javanese_culture`
(`indonesia.txt:1`), `sundanese_culture` (`:31`), `madurese_culture` (`:212`),
`balinese_culture` (`:16`), `batak_culture` (`:61`), `minangkabau_culture`
(`:76`), `acehnese_culture` (`:46`), `tagalog_culture` (`:1697`,
`tagalog_language`, `philippine_language_family`), `butuanon_culture`
(`:1817`).

Religions, all shipped: `theravada`, `mahayana`, `hindu`, `satsana_phi`,
`anitism_religion`, `kaharingan_religion`, `orang_asli_religion`,
`pelebegu_religion`, `minangkabau_religion`, `sunni`, plus ~40 more folk
religions across Borneo, Celebes, the Moluccas and the Lesser Sundas.

Dynasties homed in the theater — **43 in vanilla**
(`VAN/main_menu/setup/start/04_dynasties.txt:8269-8482` plus
`of_toungoo_dynasty:8848`), of which four matter here:
`pagan_dynasty` (`:8354`, `home = pagan`), `lavo_dynasty` (`:8309`,
`home = ayodhya`), `mauli_dynasty` (`:8407`, `home = dharmasraya`),
`singhanavati_dynasty` (`:8314`, `home = chiang_saen`). All four carry loc
rows (`dynasty_names_l_english.yml:1003`, `:737`, `:819`, `:1189`).

Name material: `Anawrahta` is a LITERAL with a loc row
(`VAN/main_menu/localization/english/character_names_l_english.yml:18682`,
`Anawrahta: "Anawrahta"`); `Airlangga` is both a pool name
(`in_game/common/languages/00_indonesia.txt`) **and** a literal (`:18937`);
`name_narai` and `name_luang` are keys
(`character_names_dynamic_l_english.yml:21872-21873`). The literal route is
already used in this repo (`tools/build_setup.py:5138`,
`first_name = { name = Ravenger }`).

**Consequence: this package authors ZERO cultures, ZERO religions and ZERO
dynasties.** It authors exactly ONE character.

---

## A. Registry

### A.1 What already exists and needs nothing

The theater's 141 registry blocks (`south_east_asia.txt` 57,
`indonesia.txt` 84) supply almost every polity 1066 needs, with vanilla arms,
vanilla loc and vanilla colours. **Vanilla ships ZERO landless-with-claims tags
in either file** — measured: every block's `own_control_core` is empty or
absent, and every one of the 141 either holds land in `10_countries.txt` or is
a `type = pop` country. That is the opposite of Africa (39 landless shells) and
it means **this package cannot revive anything; every polity it wants that is
not already landed has to be created.**

The tags that are already right for 1066 and need nothing at all:

| tag | registry | holds | why it is right |
|---|---|---|---|
| **PLB** Palembang | `indonesia.txt:92` | 34 | Srivijaya's capital; `mahayana`, `malay_culture` |
| **JMB** Melayu | `:28` | 9 | the Malayu kingdom [D on the seat, §OPEN 2] |
| **PNI** Pannai | `:60` | 7 | named in the 1030 Tanjore inscription [D] |
| **SGT** Siguntur | `:84` | 8 | capital `dharmasraya`, `mauli_dynasty` |
| **BUS** Barus | `:68` | 7 | the camphor port [D] |
| **INR** Indragiri | `:76` | 6 | a Riau river polity |
| **SUN** Sunda | `:20` | 17 | the Sundanese kingdom, continuous from the 7th c. [D] |
| **BLI** Bali | `:12` | 3 | the Warmadewa kingdom, Airlangga's birthplace [D] |
| **LIG** Ligor | `south_east_asia.txt:79` | 15 | Tambralinga/Nakhon Si Thammarat — the Chola raid's Ma-damalingam [D] |
| **LGK** Langkasuka | `:87` | 8 | attested from the 2nd c. [D] |
| **PAH** Pahang | `:103` | 11 | a Srivijayan peninsula polity |
| **LAV** Lavo | `:47` | 9 | Lopburi; the theater's one seatable throne (§C) |
| **ARK** Arakan | `:119` | 17 | correct polity, **wrong capital** (§E.4) |
| **KHM** Khmer | `:1` | 82 | seated in item 32; a 24-location Khorat edge is the only touch |
| **MYI** Ma-i | `indonesia.txt:502` | 6 | Chinese sources name Ma-i from 971/982 [D] |
| **TDO** Tondo | `:518` | 5 | the Laguna Copperplate Inscription is 900 [D] |
| **BTU** Butuan | `:550` | 1 | Song tribute missions 1001/1003/1007/1011 [D] |
| **BEI** Brunei / Po-ni | `:164` | 4 | Song missions 977, 1082 [D]; already `hindu`, not `sunni` |
| the Borneo / Celebes / Moluccas / Visayas micro-tags (~70) | both files | 1-14 each | vanilla's stateless-coast model, 1066-correct (§H) |

**`JMB`'s NAME key is "Melayu", not "Jambi".** A reader who greps for "Jambi"
finds only the *location*. This is the theater's `ZAN: "Kilwa"` trap and the
single most likely misreading here.

### A.2 Freeness of the new candidates — three scans each

Per `BALTIC-PACKAGE.md §A.2` and `AFRICA-PACKAGE.md §A.2`: (1) word-boundary
`\bTAG\b` over the whole vanilla tree, non-localisation and English-localisation
counted separately; (2) **substring** `_TAG\b|\bTAG_` over the same tree;
(3) both scans over the whole mod repo. Text files only
(`.txt .yml .gui .info .asset .gfx .py .md .json .mod …`) — `KNOWLEDGE.md`,
"Tag-freeness sweeps MUST exclude binaries". Registry index read with
`encoding='utf-8-sig'` over both `in_game/setup/countries/` trees, unanchored —
the BOM trap.

| candidate | VAN word | VAN en-loc | VAN sub | MOD word | MOD sub | registry | verdict |
|---|---|---|---|---|---|---|---|
| **PGN** (Pagan) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **HPJ** (Haripunjaya) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **KDR** (Kediri) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **JGL** (Janggala) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| HRP (Haripunjaya alt) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| PJL (Panjalu) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| JGA (Janggala alt) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| SVJ (Srivijaya) | 0 | 0 | 0 | 0 | 0 | — | free (banked, not needed) |
| NGY (Ngoenyang) | 0 | 0 | 0 | 0 | 0 | — | free (banked, §OPEN 5) |
| DVR (Dvaravati) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| PAG | 0 | 0 | 0 | **4** | 0 | — | vanilla-free but **contaminated in the mod** — `docs/INDIA-CHINA-REVIEW.md` discusses "PAG" as a hypothetical. Avoid; use PGN |
| **SRV** | 45 | 1 | 51 | 11 | 18 | `caucasus.txt:36` | **TAKEN — Shirvan**, and the mod SEATS it (`srv_fariburz_i`, `build_setup.py` HISTORICAL_RULERS). The obvious Srivijaya mnemonic is gone |
| **AVA** | 18 | 1 | 18 | 1 | 6 | `brasil.txt:74` | **TAKEN — a Brazilian tag.** `AVA: "Ava"` (`country_names_l_english.yml:4149`) is the Avá, not Burmese Ava |
| BGN | 51 | 1 | 60 | 14 | 30 | `lowlands.txt:146` | TAKEN (Boulogne) |
| **MLC** (Malacca) | 57 | 2 | 115 | 0 | 24 | — | TAKEN, **empty registry** — the PRU class, see §F.4 |
| **AYU** (Ayutthaya) | 89 | 4 | 79 | 0 | 12 | — | TAKEN, **empty registry** — the PRU class |

The `SRV` and `AVA` rows are the substring/word scan earning its keep in the
other direction: both obvious mnemonics for this theater belong to countries on
other continents, and `AVA`'s loc key reads plausibly enough that a hurried
reader would ship a Brazilian tag into Burma.

**`MLC` and `AYU` are formable-only tags with NO registry block and NO
`10_countries` block** (`00_formable_countries.txt:2085` and `:3722`, both
`potential = { always = no }` with empty location lists — event-formed). So
**Malacca and Ayutthaya do not exist on the 1337 map at all**: two of the
brief's eight "likely 1337-only states to kill" require **zero work**. §D
records the other six.

### A.3 The new blocks — four tags

Appended to `MOD/in_game/setup/countries/zz_1066_new_countries.txt`
(registry **67 → 71**; current count measured **67** with a BOM-safe reader).
Shape copied verbatim from the file's own DJN/SNH tail.

```
PGN = { #Pagan (Bagan) — Anawrahta's kingdom, Thaton conquered 1057
	color = map_burmese
	color2 = rgb { 16 41 202 }

	culture_definition = burmese_culture
	religion_definition = theravada
}

HPJ = { #Haripunjaya — the Mon kingdom of the Ping valley, seat Lamphun
	color = map_mon
	color2 = rgb { 16 41 202 }

	culture_definition = mon_culture
	religion_definition = theravada
}

KDR = { #Panjalu/Kediri — the western half of Airlangga's 1049 partition
	color = map_MAJ
	color2 = rgb { 16 41 202 }

	culture_definition = javanese_culture
	religion_definition = hindu
}

JGL = { #Janggala — the eastern half of Airlangga's 1049 partition
	color = map_javanese_LOOKUP_REQUIRED
	color2 = rgb { 16 41 202 }

	culture_definition = javanese_culture
	religion_definition = hindu
}
```

`culture_definition` is a landed tag's PRIMARY culture, not decoration
(`KNOWLEDGE.md`, "The registry's culture_definition IS a landed tag's primary
culture — measured"), so each value above is the culture the tag's own
territory actually carries (§E.1 resolves the mixes).

**HPJ's `culture_definition = mon_culture` is the package's one deliberate
mismatch with its own ground:** the 12 locations it takes are
`khon_muang_culture` 9 + `karen_culture` 3 (§E.1). Haripunjaya was a **Mon**
kingdom [D] and the Tai of the Ping valley are the 13th-century arrivals; the
location data is painted for 1337. Setting HPJ Mon-primary over Khon Muang pops
is the al-Andalus / PAA precedent (`build_setup.py:1487-1489`, "PAA's Buddhist
identity over hindu pops — the al-Andalus law"), and it is flagged in
OPEN DECISION 4.

### A.4 Colours — one lookup owed, three free

`VAN/main_menu/common/named_colors/02_map.txt` carries 3,744 `map_*` keys. Every
`color = <key>` in both `setup/countries` trees plus every inline `color = map_*`
in both `10_countries.txt` files was indexed:

| key | line | value | used by a country today |
|---|---|---|---|
| **`map_burmese`** | `:2406` | `rgb { 232 214 9 }` | **yes — `VAN:TNG`.** TNG retires in this package, freeing it; but see below |
| **`map_mon`** | `:2662` | `rgb { 105 0 115 }` | **no** — free, and it is literally the Mon colour |
| **`map_tai`** | `:2401` | `rgb { 89 194 221 }` | **no** — free (banked) |
| **`map_dambro`** | `:2402` | `rgb { 160 30 150 }` | **no** — free (banked) |
| **`map_malay`** | `:2663` | `rgb { 100 96 197 }` | **no** — free (banked) |
| `map_MAJ` | `:2723` | `rgb { 201 28 54 }` | yes — MAJ, which retires; free for KDR |
| `map_PIN` | `:2693` | `rgb { 215 190 50 }` | yes — PIN, retires |
| `map_PEG` | `:2686` | `rgb { 140 210 160 }` | yes — PEG, retires |
| `map_SUK` | `:2682` | `rgb { 159 127 255 }` | yes — SUK, retires |
| `map_LNA` | `:2664` | `rgb { 74 92 128 }` | yes — LNA, retires |

**Recommendation: PGN takes `map_burmese`, HPJ takes `map_mon`, KDR takes
`map_MAJ`, JGL takes `map_tai`.** Reusing a *retiring* tag's colour is safe
only because a landless shell paints nothing; but `map_burmese` is currently
**TNG's**, and TNG also retires, so the reuse is clean. **`map_javanese` was
NOT found and must not be written** — the JGL block above deliberately carries
a `_LOOKUP_REQUIRED` placeholder so it cannot ship by accident. `map_tai` is
the free alternative, or `map_dambro`.

`MOD/main_menu/common/named_colors/zz_1066_map_colors.txt` needs **no new rows**
under the recommendation.

### A.5 Coats of arms

All four new tags must land in `_GENERATOR_OK` (`tools/verify_mod.py:925`) or
carry CoA blocks; the check at `:975-979` fails a new registry tag that has
neither, and the check at `:999` (`min_count = 118`) counts them.

**Recommendation: `_GENERATOR_OK`, tier 4, permanent, for all four.** Pagan,
Haripunjaya, Kediri and Janggala had no heraldry of any kind — their royal
emblems were seals and inscriptions, not shields — and the generator's
religion-gated designs are the standing rationale (`verify_mod.py:926-930`, the
thirteen taifas; `:965-970`, the Baltic seven).

Every OTHER tag in this package (PLB, JMB, PNI, LAV, ARK, BTU, MYI, TDO, BEI,
KHM, INR, PHY, PUA, KTG, CHH, MUA …) is a **vanilla** tag with vanilla arms and
passes through `_van_coa_keys`. Zero CoA authoring.

### A.6 Localisation

Eight rows in
`MOD/main_menu/localization/english/1066_norman_conquest_l_english.yml`, one
physical line each, UTF-8 **with** BOM (the loc-row checks are at
`verify_mod.py:167` and `:174`, both `min_count = 359`; they rise to 367):

```
 PGN: "Pagan"
 PGN_ADJ: "Pagan"
 HPJ: "Haripunjaya"
 HPJ_ADJ: "Haripunjaya"
 KDR: "Kediri"
 KDR_ADJ: "Kediri"
 JGL: "Janggala"
 JGL_ADJ: "Janggala"
```

`PGN_ADJ` matters more than usual: at `rank_empire` the ADJECTIVE is what the
map prints, not the name (§F.2). Every other name in this package is vanilla's.

---

## B. The country blocks

### B.1 The four new `NEW_COUNTRIES` blocks

```
	PGN = {
		starting_technology_level = 3
		include = "south_east_asia_monarchy_no_coast"

		country_rank = rank_kingdom

		capital = pagan
	}

	HPJ = {
		starting_technology_level = 3
		include = "south_east_asia_monarchy_no_coast"

		country_rank = rank_duchy

		capital = lamphun
	}

	KDR = {
		starting_technology_level = 3
		include = "expl_indonesian_trade_route"
		include = "expl_indonesia"
		include = "indonesia_monarchy"

		country_rank = rank_kingdom

		capital = daha
	}

	JGL = {
		starting_technology_level = 3
		include = "expl_indonesian_trade_route"
		include = "expl_indonesia"
		include = "indonesia_monarchy"

		country_rank = rank_duchy

		capital = surabaya
	}
```

Field by field, verified:

- **`include = "south_east_asia_monarchy_no_coast"`** —
  `VAN/main_menu/setup/templates/south_east_asia_monarchy_no_coast.txt`, read in
  full: line 2 is `include = "expl_china"`, and the `government` block declares
  `type = monarchy` (`:4`), `heir_selection = cognatic_primogeniture` (`:5`),
  `parliament = { parliament_type = council }` (`:21`), thirteen sliders, laws,
  privileges and `reforms = { mandala_system }` (`:40`). It is what PIN, SAG,
  BPR, TNG, SUK, LNA, VTN, MUA and HSE all ride today. **It declares `type` and
  `heir_selection`**, so nothing needs restating — but §I's house rule is to
  restate anyway.
  **`_no_coast` is correct for PGN only if Pagan is treated as inland.** It is
  NOT: PGN takes the whole Irrawaddy delta including `dagon` (Yangon),
  `pathein` and `martaban`. **Use `south_east_asia_monarchy` (the coastal
  variant, `:43` also `reforms = { mandala_system }`) for PGN.** Recorded as a
  correction to the block above; see OPEN DECISION 12.
- **Discovery: `include = "expl_china"` covers the entire theater.**
  `VAN/main_menu/setup/templates/expl_china.txt` names **both**
  `indochina_region` and `indonesia_region` in `discovered_regions`, and every
  SEA template's line 2 is `include = "expl_china"`. So the capital-discovery
  assert (`tools/build_setup.py:5291`, `_assert_new_block_discovery`) passes for
  `pagan`, `lamphun`, `daha` and `surabaya` with no extra include. The
  `expl_indonesia*` lines on KDR/JGL are the local convention (every
  `indonesia.txt` tag carries them), not a requirement.
- **`starting_technology_level = 3`** — measured across every landed SEA tag's
  template: all four monarchy templates open with `starting_technology_level = 3`.
  Matching them is the local convention, not a judgement.
- **`country_rank`** — see §F.3 for the render. PGN at `rank_kingdom` reads
  "Kingdom of Pagan"/"King"; at `rank_empire` it reads "**Pagan Empire**"/
  "Emperor" through the adjective branch. OPEN DECISION 3.
- **`capital = daha`** — `daha` is a real location in `pajang_province`
  (resolved from `definitions.txt`), and Daha *is* Kediri's own capital name
  [D]. There is **no `kediri`, `kahuripan`, `panjalu` or `janggala` location**
  (probed: zero hits each in `definitions.txt`), which is why JGL's seat has to
  be `surabaya` — the nearest attested locality to Kahuripan [U].

### B.2 The tags this package RESHAPES rather than creates

Every one is a `FIELD_FIXES` job (`tools/build_setup.py:2818`) — exact-substring
surgery on the built block, the NOV/POK/KIE precedent — or a `CAPITAL_FIXES`
entry (`:2751`).

| tag | today (measured, `MOD/main_menu/setup/start/10_countries.txt`) | 1066 change |
|---|---|---|
| **PLB** | `:48717`, 34 locations, `capital = palembang`, **no `country_rank`**, `include = expl_china / expl_indonesian_trade_route / expl_indonesia / indonesia_monarchy` | → **add `country_rank = rank_kingdom`**. That single line turns the map label into "Palembang" and the ruler into a **Mahārājā** (§F.3). Nothing else changes |
| **ARK** | `:46551`, 17 locations, `capital = launggyet`, no rank, `south_east_asia_monarchy` | → **`CAPITAL_FIXES` `launggyet` → `weithali`.** Launggyet is a 1237 foundation [U]; `weithali` (Wethali/Vesali) is the Arakanese capital to c. 1018 and the only pre-Lemro seat that exists as a location. The Lemro-period seat at 1066 would be Pyinsa (1018-1103) [D], which has no location |
| **LAV** | `:46340`, 9 locations, `capital = lopburi`, no rank, `accepted_cultures = { mon_culture }` | → grows to 28 (§E.1); **seat Narai** (§C). No field surgery needed — `lopburi` is already the capital and `mon_culture` already accepted |
| **BEI** | `:48967`, 4 locations, `capital = berune`, `rank_duchy`, `hindu`, `accepted_cultures = { dusun_culture }` | → **no field change**; five dependency lines stripped (§G.3). `bolkiah_dynasty` (`04_dynasties.txt:8299`, `home = berune`) is 15th-century [U] but BEI's block carries **no `dynasty` line**, so nothing is inherited |
| **BTU** | `:50007`, 1 location, `capital = butuan`, `indonesia_limited_monarchy` + explicit `reforms = { mandala_system }` | → freed from BEI (§G.3). Optionally grown into `agusan_province`'s 7 unowned locations — OPEN DECISION 9 |
| **KHM** | `:46150`, 82 locations, `rank_empire`, `capital = angkor`, Harshavarman III seated (item 32) | → **+24 on the Khorat plateau only** (§E.1). No rank, ruler, capital, name or reform change — the seam is *measured*, not redesigned |
| **PUA / PHY / KTG / CHH / MUA / INR / PNI** | 2 / 2 / 2 / 11 / 12 / 6 / 7 | → **territory only**, absorbing the retirees' ground (§E.1). Zero field surgery |

### B.3 Registry overrides — NONE proposed, and that is a decision

Changing a **registered** tag's `culture_definition` / `religion_definition`
requires a whole-file override of the vanilla registry file (the Gallura
precedent; the mod ships five today: `iberia.txt`, `italy.txt`, `east_asia.txt`,
`horn_of_africa.txt`, `west_africa.txt`).

The candidates would be **KED, LGE, ARU, ATJ, PSA** — five `sunni` registry
entries in a theater whose location data is `sunni` on only six locations.
**This package proposes overriding NONE of them**, for the reason
`AFRICA-PACKAGE.md` OPEN DECISION 4 gave and the main session accepted: for
**KED and LGE** the *location* data is also `sunni` (`kedah`, `bujang`,
`perlis`; `bandar_aceh` is ATJ's), so flipping the country would put a Buddhist
king over 100% Muslim pops — worse than the label. For **ARU, ATJ and PSA** the
anachronism is the tag's *identity*, not its religion, and the honest fix is
retirement, not a registry line (§D.3, OPEN DECISION 7).

`in_game/setup/countries/indonesia.txt` (84 tags) and `south_east_asia.txt` (57
tags) therefore stay vanilla. If the main session takes OPEN DECISION 7's
"de-Islamise" branch instead, the `verify-vanilla-override` skill applies and
both files must be re-diffed after every game patch.

---

## C. Rulers — two names, both free, and the honest silence around everything else

**No ruler enters this package without attestation.** For 1066 Southeast Asia
the attested set is small, and most of the theater takes `ruler = random`.

| tag | proposed ruler | accession | regnal | confidence | note |
|---|---|---|---|---|---|
| **PGN** | **Anawrahta** | **1044.8.11** | 0 | **[D on the day, U on the year]** | Anawrahta Minsaw, king of Pagan 1044-1077; killed Sokkate at Myinkaba and took the throne. Conquered Thaton in 1057, which is what makes Pagan the delta's owner at start. The name is a LITERAL with a vanilla loc row (`character_names_l_english.yml:18682`); `pagan_dynasty` ships (`04_dynasties.txt:8354`); `pagan` is his birth location. **One `NEW_CHARACTERS` block, zero new dynasties, zero new loc rows.** |
| **LAV** | **Narai** (`adh_narai`) | **1052.1.1** | 0 | **[D]** | The Lavo chronicle's Narai, king at Lopburi c. 1052-1082 [D — the Lavo king-list is late and the dates are reconstructions]. **A VANILLA character** (`05_characters.txt`, b. 1020.1.1 at `lopburi`, `lavo_dynasty`), already death-stripped in the mod build. **Zero authoring.** Seated CROSS-TAG: his `tag = ADH` field is character-DB metadata; the `mlo_alberto_azzo_ii_este` → PAD precedent (`build_setup.py` HISTORICAL_RULERS, Italy North) and `kie_vsevolod` → PYS establish it |
| **PLB** | **none — `ruler = random`** | — | — | — | Srivijaya's maharaja in 1066 is not recoverable. The Song *shi* records a San-fo-qi mission of 1067 under a ruler transcribed **Ti-hua-kia-lo** (Divakara?) [D]; the name is a Chinese transcription of uncertain reconstruction, and whether it names the maharaja or the envoy is disputed. **The Pecheneg discipline** (`HANDOFF.md:950-955`) |
| **KDR** | **none** | — | — | — | Panjalu's king after the 1049 partition is given as **Sri Samarawijaya** [D] in the Pamwatan/Turun Hyang readings; no name key or loc row exists and the 1042-1104 Kediri list has gaps a decade wide |
| **JGL** | **none** | — | — | — | Janggala's is given as **Mapanji Garasakan** (1042-1052) then Alanjung Ahyes then Samarotsaha [D]; who reigns in 1066 is genuinely unknown |
| **BLI** | **none** | — | — | — | **Anak Wungsu**, king of Bali c. 1049-1077 [D], is the best-attested candidate in the whole maritime theater — but "Anak Wungsu" is a title-form ("youngest child") and no name key or loc row exists. See OPEN DECISION 6 |
| **ARK / HPJ / KHM / everyone else** | **none** | — | — | — | Arakan's Lemro king-list is a 19th-century chronicle reconstruction [D]; Haripunjaya's is legendary; KHM is already seated by item 32 |

**Recommendation: seat exactly TWO — Anawrahta on PGN and Narai on LAV.**
Anawrahta is the single most famous named ruler in eleventh-century Southeast
Asia and the mechanism is one `HISTORICAL_RULERS` row plus one `NEW_CHARACTERS`
block. Narai costs nothing at all — the character, the name key, the dynasty and
the birthplace all ship, and the mod has already stripped his death date.
**Thrones 176 → 178.**

```python
    "PGN": ("pgn_anawrahta", "1044.8.11", 0),   # Anawrahta Minsaw of Pagan [D on the day]
    "LAV": ("adh_narai", "1052.1.1", 0),        # Narai of Lavo — VANILLA character, cross-tag seat [D]
```

```
	# Anawrahta Minsaw, king of Pagan 1044-1077. Conquered Thaton in 1057 and
	# brought Shin Arahan's Theravada north — the reason the Irrawaddy delta is
	# Pagan's at start. NO death date: he is alive on 1066.9.15 (d. 1077 [D]).
	pgn_anawrahta = {
		first_name = { name = Anawrahta }
		culture = burmese_culture
		religion = theravada
		birth_date = 1014.1.1
		birth = pagan
		dynasty = pagan_dynasty
		tag = PGN
	}
```

Every identifier in that block was resolved: `Anawrahta`
(`character_names_l_english.yml:18682`), `burmese_culture`
(`cultures/south_east_asia.txt:124`), `theravada`, `pagan` (a location in
`pagan_province`), `pagan_dynasty` (`04_dynasties.txt:8354`). It will pass
`verify_mod.py:376` ("authored identifiers resolve", `min_count = 636` → 640)
and `:422` ("authored character keys collide with nothing", `min_count = 137`
→ 138). **`birth_date = 1014` is [D]** — Anawrahta's birth year is given as
1014 or 1015; either makes him 52 at start and well past `ADULT_AGE`.

**Character pool.** Vanilla ships 192 `tag =` blocks naming a SEA tag: PIN 24,
MAJ 19, DAI 16, PEG 14, KHM 13, BPR 11, TER 11, CHA 10, ADH 10, SAG 7, SUK 6,
LAV 5, SPN 5, JMB 5, BEI 3, SNG 3, KED 3, and 25 tags with 1-2 each. All but
the two named above are 1180-1500 people; they are a *pool* — the mod carries
no `ruler_term` for them, so nothing instantiates them, and the death-strip has
already handled the ones with post-start death dates. Inert. Worth knowing that
PIN's and MAJ's pools are the Pinya and Rajasa houses, which would surface if an
event ever pulled one after those tags go landless.

---

## D. What must die, what must be reskinned, and what must not be touched

Every tag holding land in the two in-scope regions, with a verdict. Holdings are
resolved counts from the mod build.

### D.1 Burma and Arakan

| tag | holds | founded | verdict | reason |
|---|---|---|---|---|
| **PGN** *(new)* | 0 → **74** | Pagan c. 849, Anawrahta 1044 [D] | **CREATE** — the largest 1066 polity in mainland SEA after the Khmer | the Irrawaddy valley + the Mon delta Anawrahta took in 1057 [D] |
| **PIN** Pinya | 26 | **1313** [U] | **RETIRE landless with claims** | Pinya is one of the three Ava-era successor states; its 26 are Pagan's core |
| **SAG** Sagaing | 8 | **1315** [U] | **RETIRE landless with claims** | the other Ava-era successor |
| **PEG** Hanthawaddy | 28 | **1287** [U] | **RETIRE landless with claims** | Wareru's Mon kingdom; `wareru_dynasty` (`04_dynasties.txt:8334`) is its own date-stamp. Its 28 include `thaton`, which Anawrahta took in 1057 |
| **TSM** Tenasserim | 7 | [D] | **RETIRE landless with claims** — folds into PGN | Tenasserim as a distinct Mon polity is late; Anawrahta's reach to Mergui is traditional [D]. OPEN DECISION 12 offers the "leave TSM alive" variant |
| **BPR** Prome | 3 | Sri Ksetra is Pyu, pre-9th c.; "Prome" as a state is [D] | **RETIRE landless with claims** | Pyay was Pagan's, absorbed before Anawrahta |
| **TNG** Toungoo | 2 | **1280s** [U]; `of_toungoo_dynasty` is 1510 | **RETIRE landless with claims** | |
| **KAL** Kale | 1 | a Shan muang, [D] | **KEEP** — `kale` is carved out of PGN's sweep by one `minus_singles` token | a 1-location tai_nua hill state; retiring it buys nothing |
| **ARK** Arakan | 17 | continuous [D] | **KEEP + `CAPITAL_FIXES`** `launggyet` → `weithali` | correct polity, 1237 capital |
| **TWI** | 1 (`karpus_mahal`) | — | **DO NOT TOUCH** — a Bengal-registry tag (`bengal.txt`), the India seam | |
| the Shan states **HSE HSI MNI MGT MKA MKN MYA WNT HHP HKM BHM MTG MHK MLM MMA** | 41 | king-lists from the 12th-14th c. [all D] | **LEAVE ALONE — flagged** | OPEN DECISION 5. The Shan/Tai migration into the hills is 11th-13th c. and the dating is the theater's least settled |

### D.2 The Tai and Mon country — the theater's hardest question

**At 1066 the Tai states of the Chao Phraya and the northern valleys do not
exist.** Sukhothai is 1238, Lan Na 1292, Lan Xang 1353, Phayao 1094, Ayutthaya
1351 [all U/D]. What does exist is Mon (Haripunjaya, Dvaravati's remnants),
Khmer (the Khorat plateau, Lopburi as a Khmer client) and a scatter of Tai
muang in the upper valleys.

| tag | holds | founded | verdict |
|---|---|---|---|
| **LAV** Lavo | 9 → **28** | Lavo/Lavapura, pre-7th c. [D] | **KEEP + GROW**, and seat Narai. The Chao Phraya's one continuous 1066 polity |
| **SUK** Sukhothai | 20 | **1238** [U] | **RETIRE landless with claims** — 18 to LAV, 2 to PUA |
| **ADH** Ayodhya | 1 | **1351** [U] — vanilla's own block comment reads `#Lavo` | **RETIRE landless with claims** — `ayodhya` to LAV. Note the block comment: Paradox itself treats ADH as Lavo's continuation |
| **LNA** Lan Na | 21 | **1292** [U] | **RETIRE landless with claims** — 12 to HPJ, 4 to PHY, 3 to CHH, 2 to KTG |
| **HPJ** *(new)* | 0 → **12** | Haripunjaya c. 629 [D], conquered by Mangrai 1292 | **CREATE** — the Mon kingdom of the Ping valley, seat `lamphun` |
| **VTN** Vientiane | 25 | **Lan Xang 1353** [U] | **RETIRE landless with claims** — 15 to KHM, 10 to MUA |
| **MUA** Muang Sua | 12 → **23** | Muang Sua / Xieng Dong Xieng Thong, [D] — pre-Lan Xang and plausibly 11th-c. | **KEEP + GROW** — the upper Mekong |
| **PHY** Phayao | 2 → **6** | **1094** [U] — 28 years after start | **KEEP + GROW, flagged.** Its ground (`chiang_rai_province`, incl. `chiang_saen`) is **Ngoenyang/Yonok**, the Tai polity vanilla itself dates with `singhanavati_dynasty` (`home = chiang_saen`). OPEN DECISION 5 offers the NGY-tag variant |
| **PUA** Pua | 2 → **4** | Nan/Pua, [D] | **KEEP + GROW** |
| **SPN** Suphanburi | 5 | Suphannaphum / U Thong, [D] — a Dvaravati Mon locality with a late state name | **KEEP** — carved out of LAV's sweep. OPEN DECISION 8 |
| **PTC** Phetchaburi | 3 | [D] — an old Mon port town | **KEEP** — carved out of LAV's sweep |
| **LIG** Ligor | 15 | Tambralinga, 10th c. Chinese Tan-mei-liu; the Chola's Ma-damalingam 1025 [D] | **KEEP UNCHANGED** — a genuinely 1066-correct polity that vanilla already ships |
| **CHH KTG CBK** | 11 / 2 / 9 | Tai Lu / Kengtung / "Cobra", [all D] | **KEEP + GROW** on LNA's residue |

### D.3 Sumatra and the Malay world

| tag | holds | founded | verdict |
|---|---|---|---|
| **PLB** Palembang | **34** | Srivijaya c. 671 [D] | **PROMOTE** — `rank_kingdom`, overlord of the mandala (§G.2). No territory change |
| **JMB** Melayu | 9 | Malayu, 7th c.; the post-1025 seat [D] | **KEEP** as PLB's tributary; OPEN DECISION 2 inverts this |
| **PNI** Pannai | 7 → **26** | the 1030 Tanjore inscription's Pannai [D] | **KEEP + GROW** — takes ARU's Deli/Rokan/Siak coast |
| **SGT BUS INR** | 8 / 7 / 6→11 | Dharmasraya / Barus / Indragiri [D] | **KEEP** — INR grows by Riau-Kampar |
| **ARU** Aru | **24** | **13th c.** [D] — first Chinese/Javanese attestation | **RETIRE landless with claims** — 19 to PNI, 5 to INR |
| **PSA** Pasai | 5 | **Samudera-Pasai c. 1267** [U] | **RETIRE landless with claims** — OPEN DECISION 7 |
| **ATJ** Aceh | 6 | **Aceh Darussalam 1496** [U] | **RETIRE landless with claims** — OPEN DECISION 7 |
| **LGE** Linge | 2 | Gayo, [D] | **KEEP** — no better claimant to the Gayo highlands |
| **SNG** Singapura | 6 | **Singapura 1299** [U]; capital `temasek` | **KEEP, flagged** — five of its six are `riau_islands_province` orang-laut ground, correct at any date; only `temasek` is the anachronism. Retiring it moves one location. OPEN DECISION 10 |
| **KED** Kedah | 3 | Kadaram/Kedah, ancient; but `religion_definition = sunni` | **KEEP** — the Islam is 12th-c.+ [D] and the *location* data is sunni too, so the flip is a pop-phase job (§B.3) |
| **LGK PAH MNJ BES** | 8 / 11 / 3 / 1 | Langkasuka / Pahang / Manjung / Beruas [D] | **KEEP UNCHANGED** |

### D.4 Java, Bali and the Lesser Sundas

| tag | holds | founded | verdict |
|---|---|---|---|
| **MAJ** Majapahit | **32** | **1293** [U] | **RETIRE landless with claims** — the theater's clearest single anachronism. `rajasa_dynasty` (`04_dynasties.txt:8402`, `home = trowulan`) is Ken Arok's, 1222 |
| **KDR** *(new)* | 0 → **18** | Panjalu/Kadiri, **1049** [D] | **CREATE** — the western half of Airlangga's partition, seat `daha` |
| **JGL** *(new)* | 0 → **14** | Janggala, **1049** [D] | **CREATE** — the eastern half, seat `surabaya` (Kahuripan has no location) |
| **SUN** Sunda | 17 | continuous [D] | **KEEP.** Its `capital = kawali` is the 14th-c. Sunda Galuh seat [D]; `pakuan` exists as a location and is the better 1066 answer — OPEN DECISION 11 |
| **BLI** Bali | 3 | the Warmadewa kingdom, continuous [D] | **KEEP UNCHANGED** at `rank_kingdom` — correct polity, correct scale |
| **SLP BIM DOM NGL TLW LRT WHL** | 2/1/1/1/1/2/4 | Lesser Sunda micro-polities [all D] | **KEEP ALL** — 19 of `lesser_sunda_area`'s 34 are already unowned; vanilla's model is 1066-correct |

### D.5 Borneo, Celebes, the Moluccas and the Philippines

| tag | holds | verdict |
|---|---|---|
| **BEI** Brunei / Po-ni | 4 | **KEEP UNCHANGED** — Song missions 977 and 1082 [D] put Po-ni on the map at 1066. Only its **five vassals** are wrong (§G.3) |
| **BTU** Butuan | 1 | **KEEP + FREE** — Butuan's own Song tribute missions of 1001/1003/1007/1011, and its 1003 complaint about ranking below Champa [D], make it an independent Song tributary at 1066, not Brunei's vassal 400 years early |
| **MYI** Ma-i | 6 | **KEEP + FREE** — Ma-i appears in Chinese sources from 971/982 [D] |
| **TDO** Tondo | 5 | **KEEP UNCHANGED** at `rank_kingdom` — the Laguna Copperplate Inscription is dated 900 [D] |
| **SUL** Lupah Sug | 4 | **RETIRE or KEEP-and-free — flagged.** The Sulu sultanate is **1405** [U]; the Tausug polity itself is older [D]. Its two sub-vassals (SML, KML) die with it. OPEN DECISION 9 |
| **MNA** Maynila | 1 | **RETIRE landless — flagged.** Maynila as a state is 16th c. [U]; `maynila` goes to TDO across the river. OPEN DECISION 9 |
| **MGD** Wenduling | 1 | **RETIRE landless — flagged.** The Maguindanao sultanate is c. 1520 [U] |
| **PGS IBL CEB BOL MDY KIM LNO SML KML TYY PLL CNT** | 1-8 each | **KEEP ALL** — vanilla's barangay model over 65 unowned Philippine locations is the 1066 answer |
| the Borneo tags **TJP NSR KRP SMB SGU LNK MRP TDG MNU SBG SBU SLA KKG** | 2-14 each | **KEEP ALL UNCHANGED** — 57 of Borneo's 143 locations are already unowned |
| the Celebes / Moluccas tags (~28) | 1-9 each | **KEEP ALL UNCHANGED** |

### D.6 The measured seams — named, not touched

| what | measurement | why not here |
|---|---|---|
| **Đại Việt** | DAI holds **53** locations, all in `red_river_delta_area` (49) and `champa_area` (4); `CHI→DAI` tributary at `12_diplomacy.txt:413`; `dai_ly_nhat_ton` seated with `regnal_name = Ly_Thanh_Tong`; `ly_dynasty` authored (`04_zz_1066_dynasties.txt:330`) | done — item 32 (`INDIA-CHINA-REVIEW.md:655`) |
| **Champa** | CHA holds 21 in `champa_area`; `CHI→CHA` at `:412`; `cha_rudravarman_iii` seated | done — item 32 |
| **The Khmer** | KHM holds **82** — `lower_mekong_area` 49, `khorat_plateau_area` 29, `champa_area` 4; `rank_empire`, `capital = angkor`, `khm_harshavarman_iii` seated | done — item 32. **This package's ONE touch is +24 on the Khorat plateau** (§E.1). No rank, ruler, capital or reform change. Flagged for the main session's explicit sign-off |
| **The Middle Kingdom IO** | `15_international_organizations.txt:164` — CHA, DAI, MMA, CHH, MLM and CDL are members; the instance was re-dated 1271→960 by item 30's Route B | done — items 30/32. **Retiring any theater tag that sits in it would move the member count**; measured: none of this package's twelve retirees is a Middle Kingdom member |
| **The Chola raids on Srivijaya** | COZ holds **83** after item 34 (`build_setup.py:1504-1508`), including `jaffna_province vanni pihiti kosta` — Chola Lanka. **No vanilla dependency or pact line connects COZ to any SEA tag** (measured across all 312 mod dependency lines and 28 pact lines) | the 1025 raid is thirty years before start and left no suzerainty vanilla models. **Situation material, not setup data** |
| **Butuan-China tribute** | BTU is BEI's vassal (`12_diplomacy.txt:435`) and is NOT a Middle Kingdom member | this package strips the BEI tie (§G.3). Adding BTU to the Middle Kingdom IO would be a China-slice change — **flagged, not proposed** |
| **TWI** | 1 location (`karpus_mahal`) in `chittagong_province`; a `bengal.txt` registry tag | the India seam |

**DOUBLE-OWNERSHIP CHECK — clean.** Every one of the theater's 1,044 ownable
locations was tested for membership in more than one country block's
`OWN_KEYS` set. **Zero.** The game-wide ten-location set
(`KNOWLEDGE.md`, "Ten locations game-wide live in TWO ownership blocks";
`tools/build_setup.py:1668`, `CONTROL_STRIPS`) is the six Samogitian LIT/TEU
and the four `algiers_area` TLE/MOR — **no SEA tag carries a `control` block
naming another tag's land.** `CONTROL_STRIPS` needs no SEA key.

---

## E. Territory

### E.1 `_SEA_RULES` — the definitions-resolved grants

Same 5-tuple shape as `_AFRICA_RULES` / `_BALTIC_RULES` / `_SELJUK_RULES`:
`tag: (sweep names, singles, minus-sweeps, minus-singles, expected)`. Every
count below is **resolved from `definitions.txt`, not transcribed**, and all
thirteen lists were tested pairwise disjoint by the resolver (zero overlaps).

```python
_SEA_RULES = {
    # --- PAGAN. Anawrahta's kingdom: the whole Irrawaddy valley and the
    # Mon delta he took with Thaton in 1057. The four singles are the
    # Shan-hill outliers PIN and SAG hold outside the two areas, granted
    # so both tags empty cleanly rather than surviving on one location.
    # `kale` is carved out: KAL is a one-location tai_nua hill muang and
    # retiring it buys nothing.
    "PGN": (["irrawady_area", "irrawady_delta_area"],
            ["wetwin", "myedu", "ngasingu", "takawng"],
            [], ["kale"], 74),

    # --- LAVO. The Chao Phraya basin minus the two western Mon
    # survivors (Suphanburi, Phetchaburi). Sukhothai is 1238 and
    # Ayodhya 1351; Lavo is the basin's continuous polity.
    "LAV": (["ayutthaya_province", "phraek_province", "sri_thep_province",
             "sukhothai_province", "tak_province", "rayong_province"],
            [], [], [], 28),

    # --- HARIPUNJAYA. The Ping valley: Lamphun, Chiang Mai, Lampang,
    # and the Karen west. Mangrai takes it in 1292.
    "HPJ": (["chiang_mai_province", "muang_yuam_province"], [], [], [], 12),

    # --- NGOENYANG'S GROUND. chiang_rai_province is Chiang Saen and
    # Phayao — vanilla's own singhanavati_dynasty sits at chiang_saen.
    "PHY": (["chiang_rai_province"], [], [], [], 5),
    # --- NAN. muang_ngao is PHY's and stays PHY's.
    "PUA": (["phrae_province"], [], [], ["muang_ngao"], 4),
    # --- LNA's eastern residue.
    "KTG": (["kengtung_province"], [], [], [], 6),
    "CHH": (["muang_sing_province"], [], [], [], 6),

    # --- THE KHORAT PLATEAU. Lan Xang is 1353; the plateau at 1066 is
    # Khmer (Phimai, Phanom Rung) and Kuy/Bru tribal. SEVEN of these
    # twenty-four are already UNOWNED — see UNOWNED_GRANTS below.
    "KHM": (["roi_et_province", "chaiyaphum_province",
             "muang_nakhon_province", "thakhek_proivnce"], [], [], [], 24),
    # --- THE UPPER MEKONG. Lao highland: Vientiane, Loei, Muang Phuan.
    # THREE are already UNOWNED.
    "MUA": (["loei_province", "vientiane_province",
             "muang_phuan_province"], [], [], [], 14),

    # --- JAVA, SPLIT IN 1049. Panjalu/Kediri west of the Brantas
    # (its seat daha sits in pajang_province), Janggala east.
    "KDR": (["pajang_province", "mataram_province", "demak_province"],
            [], [], [], 18),
    "JGL": (["surabaya_province", "trowulan_province"], [], [], [], 14),

    # --- NORTH SUMATRA. Aru is 13th-century; Pannai is the polity the
    # Tanjore inscription names on this coast.
    "PNI": (["deli_province", "riau_rokan_province",
             "riau_siak_province"], [], [], [], 19),
    "INR": (["riau_kampar_province"], [], [], [], 6),
}
```

**Resolved, with donors and template cultures:**

| tag | n | donors | template cultures |
|---|---|---|---|
| **PGN** | **74** | PEG 28, PIN 26, SAG 8, TSM 7, BPR 3, TNG 2 | `burmese` 36, `mon` 33, `karen` 3, `zo` 2 |
| **LAV** | 28 | SUK 18, LAV 9, ADH 1 | `thai` 24, `karen` 2, `khmer` 2 |
| **HPJ** | 12 | LNA 12 | `khon_muang` 9, `karen` 3 |
| **PHY** | 5 | LNA 4, PHY 1 | `khon_muang` 5 |
| **PUA** | 4 | SUK 2, PUA 2 | `thai` 2, `khon_muang` 2 |
| **KTG** | 6 | KTG 2, LNA 2, CHH 2 | `tai_lu` 3, `wa` 2, `tai_long` 1 |
| **CHH** | 6 | LNA 3, MUA 2, CHH 1 | `lao` 3, `khon_muang` 2, `tai_lu` 1 |
| **KHM** | 24 | VTN 15, **unowned 7**, KHM 2 | `khmu` 10, `bru` 6, `kuy` 4, `khmer` 3, `lao` 1 |
| **MUA** | 14 | VTN 10, **unowned 3**, MUA 1 | `khmu` 7, `lao` 5, `bru` 2 |
| **KDR** | 18 | MAJ 18 | `javanese` 18 |
| **JGL** | 14 | MAJ 14 | `javanese` 10, `madurese` 4 |
| **PNI** | 19 | ARU 19 | `malay` 10, `batak` 5, `minangkabau` 4 |
| **INR** | 6 | ARU 5, INR 1 | `malay` 3, `minangkabau` 3 |
| **total** | **230** | | |

Notes the resolver forced:

- **`kale` must be carved out or KAL dies as a side effect.** Without the
  `minus_singles` token PGN resolves 75 and KAL reaches zero — exactly the
  emptied-but-unlisted class the delta guard exists for
  (`tools/build_setup.py:5988`).
- **PIN and SAG do not empty from the two-area sweep alone.** PIN keeps
  `wetwin` (`hsipaw_province`) and SAG keeps `myedu` (`wuntho_province`),
  `ngasingu` (`hsipaw_province`) and `takawng` (`manmaw_province`) — four
  Shan-hill locations outside `irrawady_area`. The four `singles` above take
  them. **The alternative is to hand them to HSI/WNT/MGT instead**, which is the
  more conservative reading of Anawrahta's hill reach [D]; either way they must
  be assigned or PIN and SAG cannot go landless.
- **`thakhek_proivnce` is spelled that way in vanilla.** It is a typo in
  `definitions.txt` and the resolver will not find `thakhek_province`. Copying
  it verbatim is mandatory.
- **`ARU` empties in two steps** — PNI takes 19 (Deli/Rokan/Siak), INR takes the
  remaining 5 in `riau_kampar_province` where INR already holds `kuala_kampar`.
- **`LNA` empties in four steps** — HPJ 12, PHY 4, CHH 3, KTG 2. Every one of
  the four recipients is a vanilla tag; no Lan Na location goes unowned.

### E.2 What each donor keeps

| tag | before | after | verdict |
|---|---|---|---|
| **MAJ** | 32 | **0** | LANDLESS (claims = its 32) |
| **PEG** | 28 | **0** | LANDLESS (claims = its 28) |
| **PIN** | 26 | **0** | LANDLESS (claims = its 26) |
| **VTN** | 25 | **0** | LANDLESS (claims = its 25) |
| **ARU** | 24 | **0** | LANDLESS (claims = its 24) |
| **LNA** | 21 | **0** | LANDLESS (claims = its 21) |
| **SUK** | 20 | **0** | LANDLESS (claims = its 20) |
| **SAG** | 8 | **0** | LANDLESS (claims = its 8) |
| **TSM** | 7 | **0** | LANDLESS (claims = its 7) |
| **BPR** | 3 | **0** | LANDLESS (claims = its 3) |
| **TNG** | 2 | **0** | LANDLESS (claims = its 2) |
| **ADH** | 1 | **0** | LANDLESS (claims = `ayodhya`) — and it ALREADY carries `our_cores_conquered_by_others = { dong_lakhon dong_si_maha_phot lopburi muang_khuan_kra_buri phanat prachinburi rayong sa_kaeo saraburi }`, i.e. all nine of LAV's, verbatim from vanilla |
| **KHM** | 82 | **104** | recipient — the seam touch |
| **LAV** | 9 | **28** | recipient |
| **MUA** | 12 | **23** | recipient |
| **PNI** | 7 | **26** | recipient |
| **KDR / JGL / HPJ** | 0 | 18 / 14 / 12 | new |
| **CHH** | 11 | **14** | recipient |
| **INR** | 6 | **11** | recipient |
| **PHY** | 2 | **6** | recipient |
| **KTG** | 2 | **6** | recipient |
| **PUA** | 2 | **4** | recipient |
| **KAL** | 1 | **1** | preserved by the `kale` carve-out |

```python
SEA_LANDLESS = ("PIN", "SAG", "PEG", "TSM", "BPR", "TNG",
                "SUK", "ADH", "LNA", "VTN",
                "MAJ", "ARU")
# + ("PSA", "ATJ") under OPEN DECISION 7
# + ("SUL", "MNA", "MGD") under OPEN DECISION 9
```

**Twelve retirements, and NONE of them is a side effect** — every one is a
deliberate retirement of a post-1066 state whose whole holding is granted away
by name. That is a cleaner shape than Africa's (four of nine were side
effects), and the emptied-but-unlisted delta guard (`:5988`) should stay
silent throughout. **If it fires, the design is wrong.**

`_landless_claims` (`tools/build_setup.py:5765`) snapshots `_owned_by` **before**
all grants, so every retiree's claims are its FULL vanilla holdings: PIN 26,
SAG 8, PEG 28, TSM 7, BPR 3, TNG 2, SUK 20, ADH 1, LNA 21, VTN 25, MAJ 32,
ARU 24. Those are the right claim lists — Pinya's Upper Burma, Hanthawaddy's
delta, Sukhothai's Yom valley, Lan Na's Ping, Lan Xang's Mekong, Majapahit's
Java and Aru's Deli coast are all *future* objects at 1066, and every one of
them is a real later state whose claim set is now usable border data.

### E.3 Vacates — zero — and ten unowned locations FILLED

`docs/EU5-ERROR-DECODER.md:675-685` records the ~504-line
`jomini_script_system.cpp:252` class: **one line per pop on vacated SETTLED
land.** Measured `define_pop` counts from
`VAN/main_menu/setup/start/06_pops.txt` (28,559 location blocks, 50,227
`define_pop` entries):

| candidate vacate | locations | `define_pop` | in this package? |
|---|---|---|---|
| VTN's 25 | 25 | **107** | **NO** — KHM takes 15, MUA 10 |
| the Shan 41 | 41 | ~134 | **NO — rejected**, OPEN DECISION 5 |
| LNA's 21 | 21 | ~54 | **NO** — four recipients |
| SUK's 20 | 20 | 46 | **NO** — LAV and PUA |
| ARU's 24 | 24 | 83 | **NO** — PNI and INR |
| ATJ + PSA (Aceh) | 11 | 30 | **only under OPEN DECISION 7's "vacate" branch** |
| SUL + MNA + MGD | 6 | 23 | **only under OPEN DECISION 9's "vacate" branch** |

**The recommended package vacates ZERO locations** and therefore does not grow
the pop-line class at all. Better: it **shrinks it by ten**.

```python
UNOWNED_GRANTS["KHM"] = ["roi_et", "muang_khemarat", "yasothon", "chaiyaphum",
                         "kaset_sombun", "khon_san", "mancha_khiri"]
UNOWNED_GRANTS["MUA"] = ["ban_khon", "sayniabuli", "vang_vieng"]
```

Ten locations are ownerless in vanilla and receive an owner from the Khorat and
upper-Mekong sweeps. `_remove_owned_many`'s exactly-once assert (`tools/build_setup.py:5415-5420`,
`"ownership occurrences != 1 for …"`) demands **exactly one** ownership entry
and these have **zero** — the failure mode the
Africa slice discovered and closed (`KNOWLEDGE.md`, "Granting vanilla-UNOWNED
land needs its own path"; `tools/build_setup.py:1882-1885`). Each must be
zero-asserted against the source and asserted present in its tag's resolved
grant list. **This is the second use of `UNOWNED_GRANTS` and the first outside
Africa** — the mechanism generalises exactly as KNOWLEDGE predicted ("any
future slice that settles vanilla-empty ground (steppe, Sahara, taiga) lists it
in UNOWNED_GRANTS").

### E.4 `CAPITAL_FIXES` — one, measured

The orphan-capital guard (`tools/build_setup.py:6349-6374`) fires
`if held and capm.group(1) not in held` (`:6370`), i.e. only for a tag that
still holds land but not its capital. **Every capital in this package's grant lists was
tested against its own tag's post-grant holding: all pass.** PGN's `pagan`,
HPJ's `lamphun`, KDR's `daha`, JGL's `surabaya`, LAV's `lopburi`, PHY's
`phayao`, PUA's `pua`, KTG's `kengtung`, CHH's `muang_sing`, MUA's `muang_sua`,
KHM's `angkor`, PNI's `pannai`, INR's `rengat` — each sits inside its own tag's
resolved list or its retained holding. **The twelve retirees are exempt** by
`:6370`'s `if held and …` — the POR/`guimaraes` precedent.

The one entry is not an orphan at all but a correction:

| tag | capital | to | why |
|---|---|---|---|
| **ARK** | `launggyet` | **`weithali`** | Launggyet is a 1237 foundation [U]; `weithali` is the Arakanese seat to c. 1018 and the only pre-Lemro capital that exists as a location. `SUN` `kawali` → `pakuan` is the optional second (OPEN DECISION 11) |

### E.5 What this slice moves, in one line

**230 locations change owner, 0 vacated, 10 unowned locations filled, 12 tags
retired landless (15-17 under decisions 7 and 9), 4 new tags, 1 capital
corrected, 2 rulers seated (1 authored, 1 free), 0 dynasties authored, 0
registry overrides.**

---

## F. Rank, government and naming — worked out to the rendered string

### F.1 The branches that matter

`VAN/in_game/common/customizable_localization/country_name_construction.txt` is
**first-match, 188 lines**, read in full. Three branches reach this theater:

| line | branch | who it catches |
|---|---|---|
| `:91-97` | `country_name_construction_prefix_name` | `rank_empire` **AND** `court_language` in `chinese_language_family` — the Liao/Song branch. **No SEA tag has a Chinese-family court language** (measured: zero of vanilla's 347 `court_language` lines sets one on a SEA tag; PSA and ATJ set `malay_dialect`, nobody else sets anything) |
| **`:116-157`** | `country_name_construction_prefix_adjective_rank` | **`country_rank = rank_empire` AND `NOT = { tag = LAT }`** — and separately **`country_type = pop`**. This is the horde-name law's shape, and at empire rank it catches KHM and would catch any empire this package created |
| `:159-164` | `country_name_construction_sultanate` | `religion.group = religion_group:muslim` — ARU, ATJ, PSA, KED, LGE only |
| `:183-186` | `prefix_rank_of_name`, `fallback = yes` | **everybody else in the theater** |

Loc (`VAN/main_menu/localization/english/government_names_l_english.yml`):
- `country_name_construction_prefix_rank_of_name: "$PREFIX$ $RANK$ of $ARTICLE$ $NAME$"` (`:11`)
  and **`…_map: "$NAME$"` (`:12`)**.
- `country_name_construction_prefix_adjective_rank: "$PREFIX$ $ADJ$ $RANK$"` (`:9`)
  and **`…_map: "$PREFIX$ $ADJ$ $RANK$"` (`:10`)** — the map string is the FULL
  string.
- `country_name_construction_sultanate: "$country_name_construction_prefix_rank_of_name$"` (`:19`),
  `…_map:` → the fallback's map string (`:20`).

**THE LAW, for this theater: below empire rank a country's map label is its
NAME key verbatim; at EMPIRE rank the NAME key is never consulted and the map
prints `$ADJ$ $RANK$`.** So `PGN` at kingdom reads "Pagan", at empire reads
"Pagan Empire"; `KHM` at `rank_empire` reads "Khmer Empire" from `KHM_ADJ`
(`country_names_l_english.yml:3643`, `"Khmer"`) — which is why KHM's NAME key
has never mattered.

### F.2 The rank word — three traps, all culture- or language-gated

`country_ranks.txt` is **first-match, 2,741 lines**, and — unlike Africa and the
Baltic — **it carries ZERO tag-gated branches for any SEA tag.** Every `tag = `
line in the file was enumerated; the nearest is `:395 tag = MOM # Momboares`
(Kongo) and `:1359 tag = LIT`. The MAL/LIT trap does not exist here. What
exists instead:

**TRAP 1 — `rank_*_indian` fires on `language:malay_language`.** The branch's
OR-set is `indic_language_family` OR `dravidian_language_family` OR
**`this = language:malay_language`** (`:1081-1088`, `:1764-1771`, `:2344-2352`).
So every Malay-culture tag inherits an Indian rank word — "Mahārājya"/"Mahārājā"
at kingdom, "Rāj"/"Rājā" at duchy, "Thikana"/"Thakur" at county — **unless it is
Muslim**, because `rank_kingdom_muslim` (`:1060`) and `rank_duchy_muslim`
(`:1743`) sit ABOVE the Indian branches (`:1072`, `:1755`). For Srivijaya that
is a gift; for a *county-rank* Malay town it produces "Thikana of X" ruled by a
"Thakur", which reads as an error.

**One caveat, and it is the package's largest single mechanical risk.**
`malay_culture`'s `language` is **`malay_dialect`**
(`cultures/south_east_asia.txt:424`), a dialect of `malay_language`
(`languages/00_indochina.txt:744`, `malay_dialect = { default = yes }` inside
`malay_language`'s `dialects` block, `:708`). The trigger tests
`this = language:malay_language`. The script docs settle the direction:
`event_targets.log:1287-1290` gives the `language` scope link **Input Scopes:
country, sub_unit, character, dynasty, culture, religion, market, dialect →
Output Scopes: language**, and `:774-778` gives `court_language` **Input:
country → Output: language** while `court_dialect` outputs `dialect`;
`effects.log:10103-10106` confirms `set_court_language` takes a **dialect**
target. So `culture.language` on a dialect-carrying culture resolves UP to the
parent language and `language:malay_language` matches. **That is an inference
from the scope-link table, not an observation** — flagged as OWED CHECK 1.

**TRAP 2 — `rank_county_indian` (`:2336`) has NO rank gate of its own.** Its
trigger is the bare OR-set with no `country_rank_is_county = yes`. It is only
harmless because every branch above it that a higher-rank country could match
(`rank_empire` `:625`, `rank_kingdom` `:1252`, `rank_duchy` `:2006`) DOES carry
a rank gate and catches everything first. It is a fragile construct and a patch
that reorders the file would break it. Recorded, not acted on.

**TRAP 3 — `rank_county_barangay` (`:2505`) has a rank word and NO ruler
title.** `government_names_l_english.yml` carries exactly one row for it:
`:1047 rank_county_barangay: "Barangay"`. There is no
`rank_county_barangay_ruler_male`. What a county-rank Philippine tag's ruler is
called is therefore **not settled by any file in this repo** — OWED CHECK 2.
This package declares no `country_rank` on any Philippine tag, so it does not
trigger the question; a future Philippines slice must.

**First-match order at each rank, walked** (the order decides everything):

- **empire**: … `:325 tribe` → `:335 mali` → … `:515 vietnamese` → … → **`:625 rank_empire` (default)**. There is **no `rank_empire_indian` and no `rank_empire_thai`** — an empire-rank Malay or Tai country gets the plain "Empire"/"Emperor".
- **kingdom**: … `:908 theocracy_dharmic` → `:918 theocracy` → `:929 horde` → `:945 tribe` → `:957 kanem` → `:967 mali` → … → **`:1060 rank_kingdom_muslim`** → **`:1072 rank_kingdom_indian`** → … → **`:1252 rank_kingdom` (default)**. **Muslim BEATS Indian at kingdom rank.**
- **duchy**: … `:1606 rank_duchy_tribe` → `:1617 turkish` → … → **`:1743 rank_duchy_muslim`** → **`:1755 rank_duchy_indian`** → … → `:1964 vietnamese` → … → **`:1998 rank_duchy_thai`** → **`:2006 rank_duchy` (default)**. **Indian BEATS Thai at duchy rank** — so a Tai country whose court language were ever set to something Indic would lose "Chao".
- **county**: … `:2279 rank_county_tribe` → … → **`:2336 rank_county_indian`** → … → **`:2505 barangay`** → **`:2513 thai`** → … → **`:2553 rank_county` (default)**. **Indian BEATS barangay and thai at county rank.**

**A tag that declares no `country_rank` gets an engine-derived rank, and no
file in this repo settles the thresholds.** `VAN/in_game/common/country_ranks/00_default.txt`
(the four rank definitions, `rank_empire:1`, `rank_kingdom:52`, `rank_duchy:95`,
`rank_county:140`) carries `level`, modifiers and an `allow` block calling
`can_upgrade_country_rank`, but **no size rule**. **Forty of the theater's 57
Indochinese tags and most of the 84 Indonesian ones declare no rank.** Any
render prediction for them is a prediction about engine code, not about data.

### F.3 What each tag renders as, under the recommended design

| tag | religion | gov | rank | branch chain | full name | **map label** | ruler title |
|---|---|---|---|---|---|---|---|
| **PGN** | theravada | monarchy | **`rank_kingdom`** | `:183` fallback → `:1252` | "Kingdom of Pagan" | **Pagan** | **King** |
| *PGN alt* | theravada | monarchy | *`rank_empire`* | *`:116` adjective → `:625`* | *"Pagan Empire"* | ***Pagan Empire*** | *Emperor* |
| **HPJ** | theravada | monarchy | **`rank_duchy`** | `:183` fallback → `:2006` | "Duchy of Haripunjaya" | **Haripunjaya** | **Duke** |
| **KDR** | hindu | monarchy | **`rank_kingdom`** | `:183` fallback → `:1252` | "Kingdom of Kediri" | **Kediri** | **King** |
| **JGL** | hindu | monarchy | **`rank_duchy`** | `:183` fallback → `:2006` | "Duchy of Janggala" | **Janggala** | **Duke** |
| **PLB** | mahayana | monarchy | **`rank_kingdom`** | `:183` fallback → **`:1072` indian** | **"Mahārājya of Palembang"** | **Palembang** | **Mahārājā** |
| **JMB** | mahayana | monarchy | `rank_kingdom` (vanilla) | fallback → `:1072` | "Mahārājya of Melayu" | **Melayu** | **Mahārājā** |
| **LAV** | theravada | monarchy | none declared | fallback → size-derived | "…of Lavo" | **Lavo** | King *or* **Chao** (`rank_duchy_thai`/`rank_county_thai` if the engine derives duchy or county) |
| **ARK** | theravada | monarchy | none declared | fallback → size-derived | "…of Launggyet" | **Launggyet** | King/Duke |
| **KHM** | theravada | monarchy | `rank_empire` (vanilla) | **`:116` adjective** → `:625` | "Khmer Empire" | **Khmer Empire** | Emperor |
| **BLI** | hindu | monarchy | `rank_kingdom` (vanilla) | fallback → `:1252` | "Kingdom of Bali" | **Bali** | King |
| **TDO** | hindu | monarchy | `rank_kingdom` (vanilla) | fallback → `:1252` | "Kingdom of Tondo" | **Tondo** | King |
| **BEI** | hindu | monarchy | `rank_duchy` (vanilla) | fallback → **`:1755` indian** (malay) | **"Rāj of Brunei"** | **Brunei** | **Rājā** |
| **BTU** | hindu | monarchy | none declared | fallback → size-derived | "…of Butuan" | **Butuan** | County/Duchy title |
| **PNI** | mahayana | monarchy | none declared | fallback → `:1072`/`:1755` (malay) | "Mahārājya/Rāj of Pannai" | **Pannai** | Mahārājā/Rājā |
| **SUN** | hindu | monarchy | none declared | fallback → size-derived; `sundanese_language` is `bornean_language_family`, **not** malay → the Indian branches do NOT fire | "…of Sunda" | **Sunda** | King/Duke |
| ARU / ATJ / PSA / KED / LGE | **sunni** | monarchy | none declared | **`:159` sultanate** → `:1060`/`:1743` | "Sultanate/Emirate of X" | **Aru, Aceh, Pasai, Kedah, Linge** | Sultan / 'Amīr |
| the 18 `type = pop` countries (ASL BHN BVK DEG JGP KMU KRN KUY MUO NAA SED WAS ZHU ZOO DDI WGE MSL ILC) | various | **pop** | — | **`:116` adjective** (`country_type = pop`) | "$ADJ$ $RANK$" | **from the ADJ key** | — |

Three consequences the design obeys:

1. **PLB at `rank_kingdom` is the package's cheapest and most exact statement**:
   one line, and Srivijaya's ruler is styled Mahārājā by vanilla's own loc.
2. **PGN's rank is a real choice, not a default.** `rank_kingdom` gives
   "Kingdom of Pagan"/"Pagan"/"King"; `rank_empire` gives "Pagan Empire" on the
   map (via `PGN_ADJ`) and "Emperor". The historiography says "Pagan Empire"
   [U]; the eleventh-century title does not. OPEN DECISION 3.
3. **HPJ and JGL at `rank_duchy` render "Duchy"/"Duke", not anything local** —
   `mon_culture` is `austroasiatic_group` (no thai branch) and
   `mon_language`/`javanese_language` are neither Indic nor Malay. There is no
   Mon or Javanese rank branch anywhere in the file. Accepted; the alternative
   is `rank_kingdom` and "Kingdom", which is no more local.

### F.4 Formables — none consumed, none opened, and two 1337 states that never existed

`VAN/in_game/common/formable_countries/00_formable_countries.txt`, 143
formables. Eight touch this theater:

| formable | line | tag | frac | scope | potential | reachable at start? |
|---|---|---|---|---|---|---|
| **MLC_f** | **`:2085`** | MLC | — | **empty `locations = { }`** | **`always = no #Event`** | **NO — and MLC has no registry block and no `10_countries` block.** Malacca is not on the 1337 map at all |
| **AYU_f** | **`:3722`** | AYU | — | **empty `areas`/`provinces`** | **`always = no #Formed by event`** | **NO — same class.** Ayutthaya is not on the 1337 map |
| SIA_f | `:3021` | SIA | 0.75 | `chao_phraya_area` + `northern_tai_highland_area` = 74 → 56 | `culture = culture:thai_culture` | LAV reaches 28 = 38%. **NO** — but LAV is `thai_culture`, so **Lavo→Siam is a live formation path** |
| SHA_f | `:2970` | SHA | 0.9 | `shan_highland_area` = 39 → 36 | `has_culture_group = culture_group:shan_group` | HSE holds 10. **NO** |
| MSA_f | `:2995` | MSA | 0.9 | `malay_peninsula_area` = 43 → 39 | `malay_culture` **AND `religion.group = religion_group:muslim`** | LIG 15, PAH 11 — and the peninsula is Buddhist/Hindu at 1066. **NO**, correctly |
| NUS_f | `:4654` | NUS | 0.5 | `indonesia_region` = 573 → 287 | javanese/sundanese/madurese | KDR reaches 18. **NO** |
| BAN_f | `:3047` | BAN | 0.5 | (no scope block) | `culture:sundanese_culture` | SUN holds 17. **Scope is empty — behaviour unknown.** Flagged, not acted on |
| BNO_f | `:4711` | BNO | 0.90 | `north_borneo_area` + `south_borneo_area` = 143 → 129 | **empty `potential`** | 57 unowned. **NO** |

**No formable is consumed and none becomes reachable at start.** The two worth
naming to the user: **Malacca and Ayutthaya are event-only tags that vanilla
never places on the map**, so two of the brief's eight kill-list entries need no
work at all; and `flavor_ayu.1` (`VAN/in_game/events/DHE/flavor_ayu.txt:3-50`)
is a `dynamic_historical_event` gated `tag = LAV` / `tag = ADH`,
`from = 1337.1.1 to = 1400.1.1`, whose **third trigger branch is
`own_entire_province = ayutthaya_province` AND `own_entire_province =
suphanburi_province`** — no `country_exists = c:ADH` required. **So retiring ADH
landless does not break the Ayutthaya chain: a grown LAV can still form
Ayutthaya on schedule in 1337-1400.** That is the historically exact outcome and
it comes free.

Two advance trees become orphaned but not broken: `country_suk.txt` and
`country_MAJ.txt` (`VAN/in_game/common/advances/`) gate every node on
`has_or_had_tag = SUK` / `= MAJ`. A landless shell still satisfies its own
`has_or_had_tag`, and nobody else can reach them — the taifa precedent. The
`flavor_maj.txt` chain is likewise `dynamic_historical_event { tag = MAJ }` from
1337, so a landless MAJ shell can still receive it; harmless, recorded.

---

## G. Diplomacy

`MOD/main_menu/setup/start/12_diplomacy.txt` today: **312 `dependency` lines,
28 `scripted_mutual`/`scripted_oneway` lines** (measured; vanilla has 652 and 41).

**Exactly 26 lines name a Southeast Asian tag** — `:412-421` and `:424-439`,
under vanilla's own `#------------South East Asia-------------` and
`#------------Indonesia-------------` headers. Every one is enumerated below.
**Not one `scripted_mutual` or `scripted_oneway` line names a SEA tag**, so
`n_pacts` stays at **9** (`tools/build_setup.py:7292`).

### G.1 Lines the generic landless sweep kills for free — 12

`_drop_landless_dep` (`tools/build_setup.py:7191-7199`) removes a line if
**either** side is in `LANDLESS_AFTER`.

```
:414 dependency = { first = PIN second = TNG subject_type = vassal }     -> PIN + TNG landless
:415 dependency = { first = PIN second = BPR subject_type = vassal }     -> PIN + BPR landless
:416 dependency = { first = SUK second = PUA subject_type = vassal }     -> SUK landless
:419 dependency = { first = SUK second = PTC subject_type = vassal }     -> SUK landless
:420 dependency = { first = SUK second = TSM subject_type = vassal }     -> SUK + TSM landless
:421 dependency = { first = LAV second = ADH subject_type = vassal }     -> ADH landless
:424 dependency = { first = MAJ second = JMB subject_type = vassal }     -> MAJ landless
:426 dependency = { first = MAJ second = INR subject_type = vassal }     -> MAJ landless
:427 dependency = { first = MAJ second = PLB subject_type = vassal }     -> MAJ landless
:428 dependency = { first = MAJ second = TJP subject_type = vassal }     -> MAJ landless
:430 dependency = { first = MAJ second = BAI subject_type = tributary }  -> MAJ landless
:431 dependency = { first = MAJ second = KAM subject_type = tributary }  -> MAJ landless
```

**`n_landless_deps` 253 → 265** (`tools/build_setup.py:7265`). Under OPEN
DECISION 7's "retire ATJ/PSA" branch this does **not** move — measured: no
dependency line names ATJ or PSA. Under DECISION 9's "retire SUL/MNA/MGD"
branch it moves a further **2** (`:437 SUL→SML`, `:438 SUL→KML`), to 267; the
three `BEI→` lines die by name first (§G.3) and never reach the sweep.

### G.2 The MAJ → PLB repoint — 1 line, the Jurchen shape

Only one of MAJ's Sumatran web survives as a two-landed-tags relation, because
the other three (`:424 MAJ→JMB`, `:426 MAJ→INR`, `:427 MAJ→PLB`) all have MAJ
on the *first* side and die in the sweep.

```
:425 dependency = { first = JMB second = PNI subject_type = vassal }
```

Melayu over Pannai is defensible at 1066 [D] — Pannai is Melayu's own coast —
but under the recommended design **PLB is the mandala's centre**, and Pannai
appears in the Tanjore inscription as one of the *Srivijayan* ports the Cholas
raided [D], not as Melayu's.

**Recommendation: repoint `JMB → PLB` for PNI**, the attested repoint shape
(`tools/build_setup.py:7058-7072`, 46 Jurchen `CHI`→`LIA`, `if n_liao != 46`
at `:7071`; `:7085-7097`, 16 jimi, `if n_jimi != 16` at `:7095`):

```python
_SRIVIJAYA_VASSALS = ("PNI",)
# assert n_srivijaya == 1
```

**Counter, and it is real: a one-line repoint is a very thin use of a mechanism
built for 46 lines.** The honest alternative is to leave `:425` alone and add
PLB→PNI to the new-ties list in §G.4, which produces the same graph with one
fewer moving part. Named in OPEN DECISION 2.

### G.3 Named strips — 5, the Brunei web

```
:432 dependency = { first = BEI second = SUL subject_type = vassal }
:433 dependency = { first = BEI second = MYI subject_type = vassal }
:434 dependency = { first = BEI second = MNA subject_type = vassal }
:435 dependency = { first = BEI second = BTU subject_type = vassal }
:436 dependency = { first = BEI second = MGD subject_type = vassal }
```

Brunei's overlordship of Sulu, Ma-i, Maynila, Butuan and Maguindanao is the
**Bruneian sultanate's**, 15th-16th century [U]. At 1066 Po-ni is one of several
Song tributaries in the archipelago and **Butuan is another** — its own missions
of 1001, 1003, 1007 and 1011, and its recorded complaint about being ranked
below Champa [D], are the reason it cannot be Brunei's vassal. Ma-i appears in
Chinese sources from 971/982 [D] as an independent trading polity.

**Strip all five by name**, the named-strip shape (the KBO→Hausa batch,
`:7140-7151`, `assert n_hausa == 7`), `assert n_brunei == 5`.

### G.4 New mandala ties — the Srivijayan web, and it needs NO reform

Under the recommended design PLB becomes the overlord of the Malay world. The
mechanism is the existing tributary-list shape (`FATIMID_TRIBUTARIES`
`tools/build_setup.py:2171`, `SELJUK_TRIBUTARIES` `:2625`,
`FRANCE_TRIBUTARIES` `:2245`, `BRITISH_TRIBUTARIES` `:2313` — the last is a
pair-list, which is what a non-FAT-shaped overlord needs):

```python
SRIVIJAYA_TRIBUTARIES = (("PLB", "JMB"), ("PLB", "INR"), ("PLB", "SGT"),
                         ("PLB", "BUS"), ("PLB", "PNI"))
```

**`subject_type = tributary`, not `vassal`** — and it passes the visible gate
for free. PLB's include chain reaches `indonesia_monarchy`, whose
`reforms = { mandala_system }` grants `allow_tributary_subject = yes`
(§0.3). So does every proposed subject's. **This is the first tributary ring in
the project that needs no authored reform at all** — SEL, FAT and FRA each
needed one; the Irish six rode the tribe branch; this one rides a vanilla
template's own reform.

**Two things the harness must be told.** `verify_mod.py:761-764` gate-checks
only overlords that are new-registry tags or members of `_MOD_TRIB_OVERLORDS`
(`:759-760`). **PLB is neither** — it is a vanilla tag receiving mod-added
tributaries, exactly the case that set comment says it exists for. **`PLB` must
be added to `_MOD_TRIB_OVERLORDS`**, and the check's `min_count = 25` (`:797`)
rises to 30. Without both, five ties ship ungated.

**How many subjects?** Five is the recommendation. The maximal reading adds LGK,
PAH, KED and LIG (the peninsula), which the Chinese sources do describe as
San-fo-qi dependencies [D]; the minimal reading is JMB alone. OPEN DECISION 1.

### G.5 Left alone

```
:412 CHI->CHA (tributary)   -- the China seam, item 32
:413 CHI->DAI (tributary)   -- the China seam, item 32
:417 HSE->MGT (vassal)      -- the Shan web; both survive, [D] on the date
:418 CHI->MLM (vassal)      -- Mong Lem is in Yunnan, out of theater
:429 TJP->SMB (vassal)      -- Tanjungpura over Sambas, Borneo; both survive
:437 SUL->SML (vassal)      -- KEEP unless DECISION 9 retires SUL
:438 SUL->KML (vassal)      -- ditto
:439 MYI->TYY (tributary)   -- Ma-i over Taytay; MYI is freed, the tie survives
```

### G.6 International organizations — 9 ghosts, and two lists that need members added

Every `members`/`free_city`/`elector`/… list in
`MOD/main_menu/setup/start/15_international_organizations.txt` was scanned for
the twelve retirees. **Each appears in exactly ONE list; nine appear at all:**

| retiree | IO | line |
|---|---|---|
| PEG, TSM | Mahāvihāra sect | `:1094` |
| PIN, SAG, TNG, BPR | **Burmese Buddhism sect** | `:1116` |
| SUK, LNA | Thai Buddhism sect | `:1136` |
| MAJ | shaivism `hindu_branch` | `:1188` |
| VTN, ARU, ADH | — | none |

`build_ios`'s generic strip (`tools/build_setup.py:6588-6606`, exit at `:6668`)
removes any
`LANDLESS_AFTER` member from any such list, exact-count asserted. **`n_ghosts`
145 → 154**, and the `_expected_ghosts` list (`:6640-6668`) gains
`["PEG","TSM","PIN","SAG","TNG","BPR","SUK","LNA","MAJ"]`.

**Two lists then need members ADDED, and one of them would otherwise be
EMPTY.** The Burmese Buddhism sect's members are exactly `PIN SAG TNG BPR`
(`:1112-1117`) — all four retire, leaving a sect with zero members. Its own
`provinces` block is `pagan_province pinya_province pyay_province
sagaing_province taungoo_province` (`:1119`), i.e. precisely PGN's new ground.

**Recommendation, using the Shaiva-powers precedent
(`tools/build_setup.py:7043-7066`, "the four Shaiva powers join the shaivism
hindu_branch", exact-instance asserted at `:7054-7056`):**

- **Burmese Buddhism sect (`:1116`): `members = { }` → `members = { PGN }`.**
  Without it the slice ships an empty IO. Anawrahta's own Theravada reform came
  through Shin Arahan from conquered Thaton [D], and this sect is that
  tradition's descendant.
- **shaivism `hindu_branch` (`:1188`): add `KDR JGL`** — Javanese kingship was
  Shiva-Buddha syncretic and MAJ, SUN, KRP and BLI's neighbours are all already
  in the Hindu branches. Both new tags are `hindu`.
- **Mahāvihāra (`:1094`) keeps DBD and ARK** — no addition needed.
- **Thai Buddhism (`:1136`) keeps MMA CHH DDI LAV LIG SPN PHY PUA PTC** — a
  growing Lavo is already a member. No addition needed.
- **Mūlasarvāstivāda (`:1014`, `JMB BUS INR SGT PLB MYI PGS PAH MUA PNI`)** —
  untouched. Every member survives, and the list is the Srivijayan mandala's own
  roster, which is the second-strongest evidence for §G.4's design.

**Measured: no SEA retiree appears in the Middle Kingdom IO's member list**
(`:164`) — its SEA entries are CHA, DAI, MMA, CHH, MLM, CDL, all survivors.

---

## H. Left alone deliberately

| what | measurement | why |
|---|---|---|
| **The Shan states** — 41 locations across `shan_highland_area` (39, of which 4 unowned) and `kachin_area` (25, 5 unowned), under HSE MNI HSI MGT MKA MKN MYA WNT HHP HKM BHM MTG MHK KAL | 134 + 79 `define_pop` | OPEN DECISION 5. Shan state-formation dates are the theater's least settled [D] and vanilla's own model — a dozen small hill muang — is not obviously wrong for 1066 |
| **The Philippines** — 123 ownable, **65 unowned**, `anitism_religion` on 114 | 374 `define_pop` | Vanilla already models it as a barangay coast. Correct for 1066 and for 1337. Only the Brunei ties and three sultanate tags are anachronistic (§D.5, DECISION 9) |
| **Borneo** — 143 ownable, **57 unowned** | 390 `define_pop` | Same. The one live item is BEI's five vassals, handled in §G.3 |
| **Celebes / the Moluccas / the Lesser Sundas** — 125 ownable, **50 unowned**, ~40 one-to-nine-location tags | 396 `define_pop` | Outside the brief and 1066-plausible. Note for whoever takes it: `ternate_dynasty` and `bolaang_dynasty` ship (`04_dynasties.txt:8482`, `:8452`) |
| **KED / LGE `sunni`** | `kedah bujang perlis` are all `sunni` in `location_templates.txt`; ARU's `kota_rentang` too | §B.3 — a country flip over Muslim pops is worse than the label, the Africa DECISION-4 reasoning. **The pop phase inherits this correction**: Kedah's Islam is 12th-c. [D] and the three locations should be `mahayana` or `hindu` |
| **`06_pops.txt` and `07_cities_and_buildings.txt`** | vanilla's, un-overridden — the mod's `setup/start` set is six files | any SEA pop or building anachronism is a whole-file-override question, the class `BALTIC-PACKAGE.md` OPEN DECISION 6 banked. Note `KNOWLEDGE.md`'s "tag = X … location = L where X does not own L is FIRST-CLASS vanilla" — do **not** "fix" `07_cities` after these grants |
| **The 1025 Chola raid** | zero dependency and zero pact lines connect COZ to any SEA tag | situation material, not setup data. A Chola-Srivijaya situation is the natural v2 of this slice |
| **`bali_dynasty`, `sunda_dynasty`, `singhanavati_dynasty`, `mauli_dynasty`** | all ship, all unhomed to a seated ruler | banked. If OPEN DECISION 6 seats Anak Wungsu, `bali_dynasty` is the house |

---

## I. Mechanism — one existing tool used in a new place, and one harness gap

Like Africa, this package needs **no new build step**.

| need | existing mechanism | `file:line` |
|---|---|---|
| grants resolved from `definitions.txt` | `_resolve_ruleset` + the per-slice loop | `:788`, `:5037` |
| retire with auto-derived claims | `LANDLESS_AFTER` + `_landless_claims` | `:2697`, `:5765` |
| catch side-effect retirements | the emptied-but-unlisted delta guard | `:5988` |
| **fill vanilla-UNOWNED land** | **`UNOWNED_GRANTS`** — born in the Africa slice, **used here for the first time outside it** (10 locations) | `:1882` |
| block surgery on vanilla blocks | `FIELD_FIXES` | `:2818` |
| capital repoint | `CAPITAL_FIXES` | `:2751` |
| overlord change | the repoint, twice attested | `:7058-7072`, `:7085-7097` |
| named dependency strips | the named-strip shape (KBO→Hausa) | `:7140-7151` |
| **new tributary ring, no reform** | the tributary-pair lists + `mandala_system` from a **vanilla template** | `:2313` shape; `country_specific.txt:3894` |
| IO member strip | `build_ios`'s generic `LANDLESS_AFTER` sweep | `:6588-6606` |
| **IO member ADD** | the Shaiva-powers precedent, exact-instance asserted | `:7043-7066` |
| double-ownership | `CONTROL_STRIPS` — **no SEA key needed** | `:1668` |
| steppe-horde recipient guard | `_bad_recip` — no SEA template resolves to `steppe_horde` (measured: the string appears in no `south_east_asia_*`, `indonesia_*` or `expl_indonesia*` template) | `:5705-5707` |

**The one genuine gap is in the HARNESS, not the builder.**
`verify_mod.py:761-764` gate-checks a tributary only if its overlord is a
new-registry tag or a member of `_MOD_TRIB_OVERLORDS` (`:759-760`). PLB is
neither. **Adding `"PLB"` to that set is a required part of this change**, not
an optional tidy — without it the five new mandala ties are the first
mod-authored tributaries in the project to ship with no gate check at all.

Four asserts that will fire if the design is wrong, and should be watched:

1. **`_remove_owned_many != 1`** (`:5415-5420`) — fires if a granted location has
   two ownership entries, or **zero**. Ten of the 230 have zero and MUST be in
   `UNOWNED_GRANTS`; the other 220 were measured to have exactly one.
2. **`_list_owner` disjointness** (`:5714-5720`) — the thirteen rule-sets were
   tested pairwise disjoint by the resolver (zero overlaps).
3. **the emptied-but-unlisted delta guard** (`:5988`) — should stay
   **silent**. Every retirement here is deliberate; if the guard fires, a sweep
   is taking more than the design intends (the `kale` carve-out is the one place
   it nearly does).
4. **the capital-discovery assert** (`_assert_new_block_discovery`, `:5291`;
   the exit is `:5317`, `"{tag}: capital {cap} is not discovered by any
   include"`) — `expl_china` carries both SEA regions, so all four new capitals
   pass.

---

## OPEN DECISIONS

**1. How wide is the Srivijayan mandala — five tributaries, one, or nine?**
Vanilla's own Mūlasarvāstivāda sect (`15_international_organizations.txt:1014`)
lists `JMB BUS INR SGT PLB MYI PGS PAH MUA PNI` as one Buddhist world, and the
Chinese sources describe San-fo-qi as a confederation of ports rather than a
territorial state [D].
**Recommendation: FIVE — `PLB → JMB, INR, SGT, BUS, PNI`**, all Sumatran,
all `subject_type = tributary`, all passing the visible gate free through
`mandala_system`. That is the Sumatran core and nothing that requires a claim
about the peninsula. **Counter:** the peninsula (LGK, PAH, KED, LIG) is exactly
what the Cholas raided *as Srivijaya's* in 1025 [D], and leaving it independent
makes the 1066 map read as if Srivijaya had already collapsed — which is the
maximalist reading's whole point. The minimal alternative — PLB→JMB alone — is
the safest and says almost nothing.

**2. Palembang or Jambi — which is San-fo-qi's seat in 1066?**
This is the brief's own `[D]`. After the 1025 Chola raid the centre is usually
placed at **Jambi/Melayu**, and the Song missions of 1079 and 1082 are recorded
from *Chan-pi* (Jambi) [D]; but the 1067 mission is recorded from San-fo-qi
without qualification, and Palembang's own inscriptional record does not stop.
Vanilla gives PLB 34 locations and JMB 9, and gives JMB `rank_kingdom` while PLB
declares no rank.
**Recommendation: PLB, at `rank_kingdom`.** It is the larger tag, it carries
Srivijaya's own capital as its capital, and `rank_kingdom` + `malay_culture`
renders **"Mahārājya of Palembang" / "Mahārājā"** with one line. Under this
choice `:425 JMB→PNI` repoints to PLB. **Counter:** JMB already has
`rank_kingdom` and a vassal, so choosing it costs *zero* lines — the entire
change becomes "strip MAJ's three ties and add PLB/INR/SGT/BUS under JMB". If
the main session prefers the post-1025 Jambi reading, that is the cheaper build
as well as a defensible history.

**3. PGN's rank — `rank_kingdom` or `rank_empire`?**
At `rank_empire` the adjective branch (`country_name_construction.txt:116-157`)
fires and the **map string is the full string** — "Pagan Empire", ruler
"Emperor". At `rank_kingdom` the fallback gives map "Pagan", full "Kingdom of
Pagan", ruler "King". KHM already sits at `rank_empire` with 82 → 104
locations; PGN would have 74.
**Recommendation: `rank_kingdom`.** Anawrahta's title was *king*, the
"Pagan Empire" label is modern historiography [U], and leaving KHM as the
theater's only empire keeps the 1066 hierarchy legible. **Counter:** Pagan at 74
locations under a "King" while Angkor at 104 is an "Empire" understates the
first unification of Burma, and "Pagan Empire" is what every map in every
textbook prints.

**4. HPJ's identity — Mon over Tai pops, or match the map data?**
`chiang_mai_province` + `muang_yuam_province` are `khon_muang_culture` 9 +
`karen_culture` 3 in `location_templates.txt` — data painted for 1337, after
Mangrai. Haripunjaya was a **Mon** kingdom [D] and the Khon Muang are the
13th-century arrivals.
**Recommendation: `culture_definition = mon_culture`,** the al-Andalus / PAA law
(`build_setup.py:1487-1489`) — the tag's identity is what it was, and the pop
correction is the pop phase's job. Record it in `POP-PHASE.md`'s inherited list.
**Counter:** a Mon king over 9 Khon Muang locations produces immediate cultural
unrest that misrepresents an 11th-century Haripunjaya no one was rebelling
against; `khon_muang_culture` is the zero-friction choice at the price of the
name meaning nothing.

**5. The Tai north and the Shan hills — how far does this package reach?**
The recommendation above retires LNA and hands its 21 to HPJ (12), PHY (4),
CHH (3) and KTG (2), leaving the 41 Shan/Kachin locations alone. Two further
moves were costed and rejected:
(a) **a new `NGY` (Ngoenyang) tag** on `chiang_rai_province` instead of growing
PHY — free tag, free colour, and vanilla's own `singhanavati_dynasty`
(`home = chiang_saen`) is the house; rejected only because PHY already holds
`phayao` and a fifth new tag is a fifth CoA/loc/colour decision. **PHY's own
1094 foundation [U] is 28 years late and this is the honest place to record
it.**
(b) **retiring the Shan twelve** — 41 locations, ~213 `define_pop`, and the most
disputed dating in the theater.
**Recommendation: as costed — retire LNA, grow PHY, leave the Shan alone.**
**Counter:** if the project's standard is "a region is done when the people on
the throne are the people who were there", a dozen Shan states whose king-lists
begin in the 13th century is exactly what it retires elsewhere; and NGY is a
better answer than a 28-years-early Phayao.

**6. Bali — seat Anak Wungsu, or nobody?**
Anak Wungsu ruled Bali c. 1049-1077 [D] and is the best-attested maritime ruler
in the theater; `bali_dynasty` ships (`04_dynasties.txt:8412`,
`home = samprangan`). But "Anak Wungsu" is a title-form, no name key or loc row
exists, and the invented-literal route would have to carry it.
**Recommendation: NOBODY.** The invented-literal mechanism is proven
(`KNOWLEDGE.md`, "regnal_name accepts an invented LITERAL"; the mod's own
`Mustansir`), so the cost is one loc row — but a title-form is not a name, and
the project's own standard (the Cadalus rule, the BER precedent) is to prefer
honest silence. **Counter:** he is the one 1066 ruler in maritime Southeast Asia
whose reign dates are agreed, the dynasty ships, and Bali is a three-location
tag where a named king costs nothing and shows up immediately in a click tour.

**7. Muslim Sumatra — retire ATJ and PSA, or leave them?**
Pasai is c. 1267 and Aceh Darussalam 1496 [both U]; together they hold 11
locations across `northern_aceh_province` and `southern_aceh_province`, of which
only `bandar_aceh` and `pasai` are `sunni` in the location data — the other nine
are `hindu` or `pelebegu_religion`. **There is no vanilla tag for the 1066 Aceh
coast** (Lamuri/Ilamuridesam of the Tanjore inscription [D] has none).
**Recommendation: RETIRE BOTH landless with claims and give the 11 to `LGE`**
— the Gayo highland tag, already adjacent, already holding `linge` and
`gayo_lues`. Zero vacates, zero new tags, and it puts a non-Muslim polity on the
1066 Aceh coast. **Counter:** Linge holding the whole Aceh coast is not attested
and is a bigger invention than leaving Pasai 200 years early; the honest
alternatives are "vacate 11" (**30 `define_pop`** — the cheapest vacate in the
package by far) or "keep both with a comment", which is what this package does
for KED on the same reasoning.

**8. Suphanburi and Phetchaburi — carve them out of Lavo, or fold them in?**
The recommended `_SEA_RULES` sweeps six of `chao_phraya_area`'s eight provinces
and leaves SPN (5) and PTC (3) alive. Both are old Mon localities with late
state names [D]; U Thong/Suvarnabhumi is where Ayutthaya's founder comes from.
**Recommendation: LEAVE BOTH ALIVE.** Two western Mon survivors beside a Khmer-
client Lavo is a better picture of the 1066 basin than one 36-location Lavo, and
`flavor_ayu.1`'s third branch needs `suphanburi_province` owned entire *by the
former* for the 1337 Ayutthaya formation to fire — leaving SPN alive means LAV
must conquer it, which is the history. **Counter:** SPN and PTC are 1300s state
names on the map exactly as SUK is; folding them in costs one sweep token
(`LAV` takes `chao_phraya_area` whole = 36) and removes two anachronisms.

**9. The Philippine sultanates — SUL, MNA, MGD.**
Sulu is 1405, Maynila 16th c., Maguindanao c. 1520 [all U]; together 6 locations
and 23 `define_pop`. TDO (Tondo, LCI 900 [D]) sits directly across the river
from `maynila`.
**Recommendation: RETIRE MNA (→ TDO) and MGD (→ KIM), KEEP SUL.** Maynila and
Wenduling are unambiguously late and each is one location with an obvious
neighbour. Sulu's *sultanate* is 1405 but the Tausug polity of Lupah Sug is
older [D], and retiring it also kills `:437 SUL→SML` and `:438 SUL→KML`, which
would leave Sanmalan and Kumalarang free — an outcome nobody has researched.
**Counter:** the three are one class and splitting them is arbitrary; and
`agusan_province`'s **7 unowned locations** next to a 1-location Butuan are the
theater's best small opportunity — growing BTU to 8 would make the 1003 Song
embassy legible on the map, at the cost of seven more `UNOWNED_GRANTS` entries.

**10. Singapura (SNG).**
Six locations: five in `riau_islands_province` (all `orang_laut_culture`, correct
at any date) and `temasek` in `johor_province`. Only the tag's *name* is the
1299 anachronism.
**Recommendation: KEEP.** Retiring a tag to move one location, and inventing a
new orang-laut tag to hold the other five, is the most expensive way to fix the
smallest error in the theater. **Counter:** "Singapura" on a 1066 map is exactly
the kind of thing a knowledgeable player screenshots.

**11. Sunda's capital — `kawali` or `pakuan`?**
Vanilla gives SUN `capital = kawali`; Kawali is the Sunda Galuh seat from the
14th century [D]. `pakuan` exists as a location (`banten_province`, SUN-held).
**Recommendation: `CAPITAL_FIXES` `kawali` → `pakuan`.** One token, and Pakuan
Pajajaran is the older seat [D]. **Counter:** the Sundanese capital moved
repeatedly between Pakuan, Galuh and Kawali and the 1066 seat is genuinely
unrecorded [D]; ARK's `launggyet` → `weithali` rests on a firmer chronology and
this one may be motion for its own sake.

**12. PGN's template — coastal or `_no_coast`?**
§B.1's draft block uses `south_east_asia_monarchy_no_coast`, copying PIN's. That
is **wrong**: PGN takes the whole Irrawaddy delta including `dagon`, `pathein`,
`martaban` and `mergui`. The coastal `south_east_asia_monarchy.txt` also carries
`reforms = { mandala_system }` (`:43`) and the same `type`/`heir_selection`.
**Recommendation: `south_east_asia_monarchy` (coastal).** Recorded as a decision
rather than a silent fix because it interacts with DECISION 12's twin: **whether
TSM (Tenasserim, 7 locations) folds into Pagan at all.** If TSM stays alive
(`minus_sweeps: ["tenasserim_province"]`, PGN 74 → 67, one fewer retirement),
Pagan is still coastal through `pegu_province` and `myaungmya_province`.
**Counter on TSM:** Anawrahta's reach to Mergui is a chronicle tradition [D] and
a Mon Tenasserim beside a Burman Pagan is a defensible 1066 map.

---

## Implementation checklist

Ordered so each step can be verified before the next.

1. **Registry additions FIRST and alone** — `PGN`, `HPJ`, `KDR`, `JGL` appended
   to `MOD/in_game/setup/countries/zz_1066_new_countries.txt`. Count **67 → 71**
   (`verify_mod.py:1032`, `min_count = 2407` → 2411). **No registry overrides in
   this package** — `indonesia.txt` and `south_east_asia.txt` stay vanilla.
2. **Colours** — `PGN` `map_burmese` (`02_map.txt:2406`), `HPJ` `map_mon`
   (`:2662`), `KDR` `map_MAJ` (`:2723`), `JGL` `map_tai` (`:2401`).
   **Re-run the key/RGB usage check in §A.4 before assuming it**, and never
   write `map_javanese` — it does not exist.
3. **Localisation** — 8 rows, one physical line each, UTF-8 **with** BOM.
   `verify_mod.py:167` and `:174` rise 359 → 367.
4. **`_GENERATOR_OK`** — add PGN, HPJ, KDR, JGL at `tools/verify_mod.py:925`
   with a tier-4 comment; the check at `:975-979` fails otherwise and `:999`
   rises 118 → 122.
5. **`NEW_COUNTRIES`** — the four blocks of §B.1, **with PGN on the COASTAL
   template** (DECISION 12). Re-read `south_east_asia_monarchy.txt` and
   `indonesia_monarchy.txt` in full before shipping and restate anything they
   omit.
6. **`_SEA_RULES` + resolution loop** — modelled on the Africa loop: resolve,
   assert the exact count per tag, assign into `LOCATION_GRANTS`, then assert
   each capital is in its own resolved list. **`thakhek_proivnce` is vanilla's
   own spelling — copy it verbatim.**
7. **`UNOWNED_GRANTS`** — the ten Khorat/Mekong locations (§E.3), each
   zero-asserted against the source. **Observe the `_remove_owned_many` failure
   first** if they are omitted — that is the Africa slice's own discovery
   reproduced on new ground.
8. **`SEA_LANDLESS`** into `LANDLESS_AFTER` (`:2697`) — **12 tags**. None is a
   side-effect retirement; the delta guard should stay silent.
9. **`CAPITAL_FIXES`** — ARK `launggyet` → `weithali` (+ SUN `kawali` →
   `pakuan` under DECISION 11).
10. **`FIELD_FIXES`** — PLB gains `country_rank = rank_kingdom`. **One entry**,
    and the substring must be copied from the built file, not retyped.
11. **`HISTORICAL_RULERS` + `NEW_CHARACTERS`** — PGN/Anawrahta (authored) and
    LAV/`adh_narai` (vanilla, cross-tag). Thrones **176 → 178**
    (`verify_mod.py:288` `min_count = 352` → 356; `:406` `min_count = 176` → 178;
    `:376` 636 → 640; `:422` 137 → 138).
12. **`n_landless_deps` 253 → 265** (`:7265`) — **observe it failing first**,
    per CLAUDE.md. `n_pacts` stays **9** (`:7292`): measured, no SEA pact exists.
13. **The repoint** — `JMB → PLB` for PNI, Jurchen shape, `if n_srivijaya != 1`
    (or fold into step 14 per DECISION 2's counter).
14. **Named strips** — the five `BEI→` lines, `assert n_brunei == 5`.
15. **New tributaries** — `SRIVIJAYA_TRIBUTARIES`, five pairs,
    `subject_type = tributary`, plus **`"PLB"` added to
    `verify_mod.py:759`'s `_MOD_TRIB_OVERLORDS`** and `:797`'s `min_count`
    25 → 30. **Both, or the ties ship ungated.**
16. **IOs** — `n_ghosts` **145 → 154** with the nine names added to
    `_expected_ghosts` (`:6640-6668`); then **add `PGN` to the Burmese Buddhism
    sect** (`15_international_organizations.txt:1116` — it is otherwise EMPTY)
    and **`KDR JGL` to the shaivism `hindu_branch`** (`:1188`), each with its own
    exact-instance assert, the Shaiva-powers shape (`:7043-7066`).
    `verify_mod.py:838` ("IO members hold land") stays green only if both
    additions land.
17. **Harness** — `verify_mod.py:1157`'s parliament `min_count = 1376` moves:
    12 landless against 4 new landed, all four reaching
    `parliament_type = council` through their templates → **expect 1368**, but
    **verify, do not assume**. `:860` and `:1032` rise by 4 (country blocks
    **2404 → 2408**).

**Break-tests owed** (a check never seen failing is untested):

(a) a bogus location in `_SEA_RULES` must abort;
(b) an off-by-one `expected` must abort with the resolved count printed;
(c) **drop the `kale` `minus_singles` token and watch the emptied-but-unlisted
delta guard (`:5988`) fire on KAL** — this package's only near-miss, and
the guard's second workout;
(d) `n_landless_deps` left at 253 must abort with 265 printed;
(e) **remove one of the ten `UNOWNED_GRANTS` entries and watch
`_remove_owned_many` die with `occurrences != 1`** — the Africa failure
reproduced deliberately on new ground;
(f) the Brunei strip at 4 or 6 instead of 5 must abort;
(g) point `LOCATION_GRANTS["HPJ"]` at a location `PHY` also claims and watch
`_list_owner` (`:5714-5720`) fire;
(h) **remove `"PLB"` from `_MOD_TRIB_OVERLORDS` and confirm the tributary-gate
check goes SILENT rather than failing** — proving the gap §I names is real, then
restore. If it stays silent with PLB present too, the check itself is broken;
(i) leave the Burmese Buddhism sect empty and confirm whether any check notices
a zero-member IO — **if none does, that is the check this package owes.**

## Expected constant moves, collected

| constant | `file:line` | from | to (recommended) | to (all decisions maximal) |
|---|---|---|---|---|
| registry blocks | `zz_1066_new_countries.txt` | **67** | **71** | 72 (+NGY) |
| registry overrides | `MOD/in_game/setup/countries/` | 5 files | **5 — unchanged** | 6 (+`indonesia.txt`) |
| `NEW_COUNTRIES` count | `build_setup.py:475` | current | **+4** | +5 |
| `LANDLESS_AFTER` | `:2697` | current | **+12** | +17 (ATJ PSA SUL MNA MGD) |
| `n_landless_deps` | `:7265` | **253** | **265** | 267 |
| `n_pacts` | `:7292` | **9** | **9 — unchanged, measured** | 9 |
| repoints (new batch) | new, `:7058` shape | — | **1** (JMB→PLB) | 1 |
| named dependency strips | new, `:7140` shape | — | **5** (the Brunei web) | 5 |
| new tributary pairs | new, `:2313` shape | — | **5** | 9 (+peninsula) |
| `_MOD_TRIB_OVERLORDS` | `verify_mod.py:759` | 8 tags | **9 (+PLB)** | 9 |
| tributary-gate check `min_count` | `verify_mod.py:797` | **25** | **30** | 34 |
| `CAPITAL_FIXES` | `:2751` | current | **+1** (ARK) | +2 (SUN) |
| `FIELD_FIXES` | `:2818` | current | **+1** (PLB rank) | +1 |
| `UNOWNED_GRANTS` | `:1882` | 1 tag / 9 locations | **3 tags / 19 locations** | 4 / 26 (+BTU's Agusan) |
| `CONTROL_STRIPS` | `:1668` | 1 tag | **unchanged — no SEA double-ownership** | unchanged |
| `LOCATION_VACATED_EXPECT[*]` | `:1246`, `:1373`, `:1399` | — | **unchanged** | unchanged |
| locations granted | build report | current | **+230** | +247 |
| locations vacated | build report | current | **+0** | +0 |
| unowned locations | — | current | **−10** | −17 |
| IO ghosts | `:6668` | **145** | **154** | 154 |
| IO members added | `15_IO.txt:1116`, `:1188` | — | **PGN; KDR JGL** | same |
| country blocks | `verify_mod.py:860`, `:1032` | **2404 / 2407** | **2408 / 2411** | 2409 / 2412 |
| thrones | `verify_mod.py:288`, `:406` | **176** | **178** | 179 (+Anak Wungsu) |
| new characters / dynasties | — | — | **1 / 0** | 2 / 0 |
| loc rows | `verify_mod.py:167`, `:174` | **359** | **367** | 369 |
| CoA references | `verify_mod.py:999` | **118** | **122** | 123 |
| parliament check `min_count` | `verify_mod.py:1157` | **1376** | **verify — expect 1368** | verify |

---

## Verification statements

Per CLAUDE.md's say-what-you-verified rule.

- **Verified — the resolver.** An independent reimplementation of `_parse_defs`
  (`tools/build_setup.py:721`), `_ownable_set` (`:745`), `_resolve_ruleset`
  (`:788`), `find_block_end` (`:5193`) and the `OWN_KEYS`/`COUNTRY_RE` reader
  reproduces `BALTIC-PACKAGE.md`'s published counts (`samogitia_area` 16,
  `courland_province` 8), finds **20,922 ownable locations**, reads **2,337
  country blocks in vanilla and 2,404 in the mod** (matching `HANDOFF.md:1780`),
  and reproduces `AFRICA-PACKAGE.md`'s `06_pops.txt` figures exactly
  (**28,559 location blocks / 50,227 `define_pop`**).
- **Verified — the template parser**, by asserting `cult['dadu'] ==
  'yan_culture'`; `location_templates.txt` blocks are single-line and a
  line-anchored culture regex returns zero on all 20,922 entries.
- **Verified — the tag scanner**, by feeding it GHA, MAK, ZAN, TMB (all four
  TAKEN with the registry `file:line` and the substring/en-loc counts
  `AFRICA-PACKAGE.md §A.2` published) and PRU (TAKEN, **empty registry** — the
  formable-only class). PGN, HPJ, KDR, JGL, HRP, PJL, JGA, SVJ, NGY and DVR come
  back **0/0/0/0/0**. **SRV is Shirvan (`caucasus.txt:36`) and AVA is Brazilian
  (`brasil.txt:74`)** — both scanned, both refused.
- **Verified — Southeast Asia is untouched by this mod.** Zero references to
  `indochina_region` / `indonesia_region` or any of their 21 areas in
  `tools/build_setup.py`, and zero string literals naming any of the 141 tags in
  `south_east_asia.txt` (57) and `indonesia.txt` (84). The theater-adjacent tags
  the build knows are DAI, CHA, KHM, CDL, MLM, MMA — all item-32 seams.
- **Verified — the theater's shape.** 1,044 ownable locations across
  `indochina_region` (471) and `indonesia_region` (573); **831 owned by 125
  tags, 213 unowned, ZERO double-ownership** (every location tested against all
  six `OWN_KEYS` across all 2,404 mod country blocks).
- **Verified — the two adult characters.** All 192 SEA `tag =` blocks in
  `VAN/main_menu/setup/start/05_characters.txt` were parsed for `birth_date`;
  exactly two are ≤ 1050 (`adh_narai` 1020, `adh_luang` 1050), the next is 1070.
  Both carry `dynasty = lavo_dynasty`, `birth = lopburi`, `culture =
  thai_culture`, `religion = theravada`, and **both have had their `death_date`
  removed in the mod build** (diffed against vanilla). `name_narai` and
  `name_luang` are keys at
  `character_names_dynamic_l_english.yml:21872-21873`; `lavo_dynasty` is
  `04_dynasties.txt:8309` with loc `dynasty_names_l_english.yml:737`.
- **Verified — `Anawrahta` is a shipped literal**,
  `VAN/main_menu/localization/english/character_names_l_english.yml:18682`,
  `Anawrahta: "Anawrahta"`. `pagan_dynasty` is `04_dynasties.txt:8354`
  (`home = pagan`, loc `dynasty_names_l_english.yml:1003`). The literal route is
  attested in this repo at `tools/build_setup.py:5138`
  (`first_name = { name = Ravenger }`).
- **Verified — the mandala reform.**
  `VAN/in_game/common/government_reforms/country_specific.txt:3894-3915`,
  `potential = { capital.sub_continent = sub_continent:south_east_asia OR = {
  dharmic / theravada / mahayana / satsana_phi } }`,
  `country_modifier = { cultures_capacity = 3 …
  allow_tributary_subject = yes }`. **All four SEA monarchy templates carry it**
  — `south_east_asia_monarchy.txt:43`, `south_east_asia_monarchy_no_coast.txt:40`,
  `indonesia_monarchy.txt` (final block), `indonesia_monarchy_no_coast.txt:65` —
  and `indonesia_muslim_monarchy_no_mandala.txt:1` is a bare
  `include = "indonesia_monarchy_no_mandala"`. `definitions.txt:4334` shows
  `south_east_asia`'s only children are `indochina_region` and
  `indonesia_region`.
- **Verified — the render laws.** `country_name_construction.txt` is 188 lines,
  first-match, read in full; `:91-97` needs `rank_empire` + a Chinese-family
  court language, `:116-157` needs `rank_empire` (or `country_type = pop`) and
  its `_map` string is `"$PREFIX$ $ADJ$ $RANK$"`
  (`government_names_l_english.yml:9-10`), `:159-164` catches the muslim group,
  `:183-186` is the fallback whose `_map` is **bare `"$NAME$"`** (`:12`).
  `country_ranks.txt` is 2,741 lines, first-match; **every `tag = ` line in it
  was listed and none names a SEA tag**. The SEA branches are `rank_kingdom_indian`
  `:1072`, `rank_duchy_indian` `:1755`, `rank_county_indian` `:2336` (each with
  `this = language:malay_language` in its OR-set at `:1081/:1088`, `:1764/:1771`,
  `:2344/:2352`), `rank_duchy_thai` `:1998` and `rank_county_thai` `:2513` (both
  `has_culture_group = culture_group:thai_group`), and `rank_county_barangay`
  `:2505` (`philippine_language_family`). Loc: `:467-469` "Mahārājya"/"Mahārājā",
  `:752-754` "Rāj"/"Rājā", `:997-999` "Thikana"/"Thakur", `:879-881`
  "Principality"/"Chao", `:1049-1051` "Lordship"/"Chao", **`:1047`
  `rank_county_barangay: "Barangay"` with NO ruler key**. `rank_kingdom_muslim`
  `:1060` precedes `rank_kingdom_indian` `:1072`; `rank_duchy_muslim` `:1743`
  precedes `rank_duchy_indian` `:1755`, which precedes `rank_duchy_thai` `:1998`;
  `rank_county_indian` `:2336` precedes both `:2505` and `:2513`.
- **Verified — the dialect question is a SCOPE-LINK question, and the script
  docs answer it in the right direction.** `malay_culture`'s `language` is
  `malay_dialect` (`cultures/south_east_asia.txt:424`), a `default = yes`
  dialect of `malay_language` (`languages/00_indochina.txt:708`, `:744`).
  `event_targets.log:1287-1290`: the `language` link takes
  `country, sub_unit, character, dynasty, culture, religion, market, **dialect**`
  and outputs `language`; `:774-778`: `court_language` outputs `language` while
  `court_dialect` outputs `dialect`; `effects.log:10103-10106`:
  `set_court_language` takes a **dialect** target. Vanilla writes both forms in
  setup (347 `court_language` lines: 84 `nahuatl_language`, 7
  `southern_mandarin_dialect`, 2 `malay_dialect` …). **The conclusion that
  `culture.language` on `malay_culture` matches `language:malay_language` is an
  INFERENCE from those links, not an observation — OWED CHECK 1.**
- **Verified — the diplomacy.** 312 `dependency` lines and 28
  `scripted_mutual`/`scripted_oneway` lines in the mod file (652 and 41 in
  vanilla); **exactly 26 name a SEA tag**, at `:412-421` and `:424-439`,
  enumerated in §G. `_drop_landless_dep` (`:7191-7199`) drops on **either** side;
  the repoint precedents are `:7058-7072` and `:7085-7097`, both exact-count
  asserted; `n_landless_deps` is asserted at **253** (`:7265`) and `n_pacts` at
  **9** (`:7292`).
- **Verified — the IO lists.** Every `members`/`free_city`/`elector`/… list in
  `MOD/main_menu/setup/start/15_international_organizations.txt` (862 member
  tokens) was scanned for the twelve retirees: **nine appear, each in exactly
  one list** — PEG/TSM `:1094`, PIN/SAG/TNG/BPR `:1116`, SUK/LNA `:1136`, MAJ
  `:1188`. VTN, ARU and ADH appear in none. **The Burmese Buddhism sect's
  members are exactly `PIN SAG TNG BPR`, so all four retirements empty it**, and
  its own `provinces` block (`:1119`) is `pagan_province pinya_province
  pyay_province sagaing_province taungoo_province`. The Mūlasarvāstivāda sect
  (`:1014`) lists `JMB BUS INR SGT PLB MYI PGS PAH MUA PNI` and loses nobody.
  `build_ios`'s strip is `:6588-6606` with `n_ghosts` asserted at **145**
  (`:6668`); the member-add precedent is `:7043-7066` (`_sh_blocks`, exit at `:7054`).
- **Verified — the formables.** `MLC_f` (`00_formable_countries.txt:2085`,
  `potential = { always = no #Event }`, `locations = { }`) and `AYU_f` (`:3722`,
  `always = no #Formed by event`, empty `areas`/`provinces`) are **event-only
  with no registry block and no `10_countries` block** — the PRU class.
  `SIA_f` `:3021`, `SHA_f` `:2970`, `MSA_f` `:2995`, `NUS_f` `:4654`,
  `BAN_f` `:3047` (empty scope), `BNO_f` `:4711` (empty `potential`). None is
  consumed; none becomes reachable at start.
  `flavor_ayu.1` (`VAN/in_game/events/DHE/flavor_ayu.txt:3-50`) is
  `dynamic_historical_event { tag = LAV tag = ADH from = 1337.1.1 to = 1400.1.1 }`
  and its third trigger branch is `own_entire_province = ayutthaya_province`
  AND `own_entire_province = suphanburi_province` — **no `country_exists = c:ADH`
  required**, so a grown LAV can still form Ayutthaya.
- **Verified — the colours.** Every `map_*` key in §A.4 exists at the line given
  in `VAN/main_menu/common/named_colors/02_map.txt` (3,744 keys total).
  `map_mon` (`:2662`), `map_tai` (`:2401`), `map_dambro` (`:2402`) and
  `map_malay` (`:2663`) are used by **no country** in vanilla or the mod
  (checked across every `color = <key>` in both `setup/countries` trees and every
  inline `color = map_*` in both `10_countries.txt`). `map_burmese` (`:2406`) is
  used by **TNG**, which this package retires. **`map_javanese` does not exist.**
- **Verified — 18 `type = pop` countries touch the theater** (ASL BHN BVK DEG
  JGP KMU KRN KUY MUO NAA SED WAS ZHU ZOO DDI WGE MSL ILC), each with an
  `add_pops_from_locations` list naming theater locations; vanilla ships 451
  `type = pop` blocks game-wide. `country_name_construction.txt:154` puts
  `country_type = pop` in the ADJECTIVE branch, so every one of them renders
  from its ADJ key.
- **Verified — vanilla ships ZERO landless-with-claims tags in either SEA
  registry file.** Every one of the 141 blocks in `south_east_asia.txt` and
  `indonesia.txt` was read (`utf-8-sig`) and cross-referenced against
  `10_countries.txt`: each either holds land or is a `type = pop` country. This
  package therefore cannot revive anything, unlike Africa's nine.
- **Verified — the corrections to `docs/INDIA-CHINA-REVIEW.md`.**
  `south_east_asia.txt` has **57** blocks, not 56 (KHM is the first block and
  sits behind the BOM). VTN holds **25** locations in the current build, not 32.
  Its §2.3 claim "There is no PAG/Pagan tag" stands, and its D8 recommendation
  ("reskin PIN") is refused here in favour of a new PGN tag — PIN's NAME,
  ADJ, colour and CoA are all "Pinya", and the ASK/CHI `country_name`/`flag`
  route (`build_setup.py:3047-3065`) would need a new flag asset that does not
  exist for Pagan.
- **NOT verified, and stated as such — every historical claim carrying `[U]` or
  `[D]`:** Anawrahta's regnal dates (1044-1077), his accession day (1044.8.11),
  his birth year (1014 or 1015) and the Thaton conquest of 1057; Shin Arahan and
  the Theravada reform; Pagan's foundation (c. 849); Pinya (1313), Sagaing
  (1315), Hanthawaddy/Wareru (1287), Toungoo (1280s) and Prome's status;
  Arakan's Lemro capitals (Sambawak/Pyinsa/Parein/Hkrit, 1018-1430) and
  Launggyet (1237); Wethali's abandonment (c. 1018); Lavo's Narai and Luang and
  their reigns; Sukhothai (1238), Lan Na and Mangrai (1292), Lan Xang (1353),
  Phayao (1094), Ayutthaya and U Thong (1351), Haripunjaya (c. 629-1292),
  Ngoenyang/Yonok (c. 638); Dvaravati's survival and Suphannaphum/U Thong;
  Tambralinga and the 1025 Chola raid (Ma-damalingam, Kadaram, Pannai,
  Ilamuridesam in the Tanjore inscription); Srivijaya's post-1025 condition and
  the Palembang-vs-Jambi seat; the San-fo-qi missions of 1067, 1077, 1079 and
  1082 and the ruler-name Ti-hua-kia-lo; Airlangga's death (1049) and the
  partition into Janggala and Panjalu; Samarawijaya, Mapanji Garasakan,
  Alanjung Ahyes and Samarotsaha; Kahuripan's location; Majapahit (1293),
  Singhasari (1222) and Ken Arok; Anak Wungsu of Bali (c. 1049-1077) and the
  Warmadewa; Sunda's capitals (Pakuan, Galuh, Kawali); Aru (13th c.),
  Samudera-Pasai (c. 1267), Aceh Darussalam (1496), Perlak's traditional dates
  (840 or 1042), Barus and the Lobu Tua inscription (1088), Kedah's Islamisation
  (1136 or later); Singapura (1299) and Malacca (c. 1400); Po-ni's Song missions
  (977, 1082) and the Bruneian sultanate; Butuan's missions (1001/1003/1007/1011)
  and its 1003 protest; Ma-i (971/982); Tondo and the Laguna Copperplate
  Inscription (900); Sulu (1405), Maynila (16th c.) and Maguindanao (c. 1520);
  the Shan and Tai muang king-lists; and the Khmer hold on the Khorat plateau
  under Suryavarman I and Harshavarman III. Every one rests on the agent's own
  history and needs a source before it enters a comment, let alone setup data.
- **NOT checked, and OWED before implementation:**
  (1) **whether `culture.language` on a dialect-carrying culture matches
  `language:<parent>`** — it decides whether `rank_kingdom_indian`
  (`country_ranks.txt:1072`) fires for PLB at all, and therefore whether
  Srivijaya's ruler reads **"Mahārājā"** or plain "King". The scope-link table
  says it should (`event_targets.log:1287-1290`); nothing observes it. **This is
  the single most load-bearing unverified claim in the package.**
  (2) **whether `rank_county_barangay` has any ruler title** —
  `government_names_l_english.yml` carries one row (`:1047`) and no
  `_ruler_male`. Not triggered by this package; owed by a future Philippines
  slice.
  (3) **how the engine derives `country_rank` when a block declares none** —
  `in_game/common/country_ranks/00_default.txt` carries no size rule, and forty
  of the theater's Indochinese tags plus most Indonesian ones declare no rank.
  Every "size-derived" cell in §F.3 is a guess about engine code.
  (4) **whether the engine validates a setup `reforms = { }` entry against the
  reform's own `potential`** — inherited unresolved from
  `AFRICA-PACKAGE.md`'s owed list, and it matters here because
  `mandala_system`'s potential excludes Muslim states while KED, LGE, ARU, ATJ
  and PSA all ride `indonesia_muslim_monarchy_no_mandala`, which correctly drops
  it. If the engine does NOT validate, nothing breaks; if it does, nothing
  breaks either — but the answer is still owed for the general case.
  (5) **whether any harness check notices a zero-member IO** — the Burmese
  Buddhism sect empties completely under this package. If nothing catches it,
  break-test (i) is the check this package owes.
