> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 38 (commit e63c255) —
> NOT yet game-tested.** Research record, not the state. **The first package
> to survive main-session review with ZERO implementation-level errors**
> (all 58 verification probes green — the SEA lessons held). Decisions,
> taken by the main session under the user's direct-implement
> authorization: 1 TWO tags (DBU+GTS), 2 retire TIB, 3 TKA created,
> **4 Dongzhan SEATED — the package's "nobody" overruled on the Tunka
> Manin precedent** (an attested ruler known only through an external
> source's transcription, seated by user decision in the Africa slice;
> thrones 179, `tsongkha_dynasty` authored realm-named per vanilla's own
> pagan/purang grammar), 5 `"Ü"` (click-tour probe), 6 the four
> deep-plateau tusi STRIPPED, 7 PUR FIXED (the east_asia.txt override's
> second intended deviation), 8 Kham/Amdo left, 9 no sect adds. KNOWN
> DEVIATIONS, code wins: identifiers check rose to **646** not 645;
> **break-test (i)'s prediction was REFUTED** — a `u_area` sweep does NOT
> trip the delta guard (POO survives on its Kham 7; the only guard against
> that mistake is the exact-count assert), and (f) fired through the
> vacate-count assert rather than `:6086`'s disjointness (order effect,
> loud either way). Constants landed exactly as forecast otherwise:
> deps 280, ghosts 156, vacated +7, registry 74, blocks 2411, loc 375,
> CoA 125, parliament 1366.

# TIBET 1066 — the Era of Fragmentation is already on the map; one tag denies it (DRAFT)

**Research agent model ID: `claude-opus-5`.**

**DRAFT — pending main-session review. Nothing here has been written into any
mod file.** Produced by an Opus research agent, 2026-08-02, against the working
tree at HEAD `35ecdf6` (37 items landed; constants: registry 71 blocks, country
blocks 2408, thrones 178, landless-dep strips 265, pacts 9, IO ghosts 155).
Every mechanical claim carries a `file:line`. Historical claims that no file can
settle are flagged `[U]` (unverified — the agent's own history, no source in the
repo) or `[D]` (sources genuinely differ), never asserted silently.
§VERIFICATION collects them.

Reference roots:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, 491,179 bytes, present)
`MOD = .../1066 Test Mod`

**Method — the SEA lesson applied.** No reader was reimplemented. This package
`import`s `tools/build_setup.py` (it has a `__main__` guard at `:7973`) and
calls its own parsers: `_parse_defs` (`:732`), `_ownable_set` (`:756`),
`_resolve_ruleset` (`:799`), `find_block_end` (`:5390`) and `COUNTRY_RE`
(`:5443`). Ownership is read with the **full ten-member `OWN_KEYS` tuple copied
verbatim from `build_setup.py:5585`** — `own_control_core,
own_control_integrated, own_control_conquered, own_control_colony, own_core,
own_conquered, own_integrated, own_colony, control_core, control`. Everything
reads `encoding='utf-8-sig'`; comments are masked before tokenising. Scripts
live in the session scratchpad (`tib.py`, `hier.py`, `tagscan.py`); nothing was
written into the repo.

**Proven on known positives BEFORE any new ground, including an
`own_control_integrated` case.**

| probe | expected (source) | measured |
|---|---|---|
| ownable locations | 20,922 (`AFRICA-PACKAGE.md` §VERIFICATION) | **20,922** |
| vanilla country blocks | 2,337 | **2,337** |
| mod country blocks | 2,408 (`HANDOFF.md:1845`) | **2,408** |
| `samogitia_area` ownable | 16 (`BALTIC-PACKAGE.md:55`) | **16** |
| `courland_province` ownable | 8 (`BALTIC-PACKAGE.md:853`) | **8** |
| **VTN in vanilla** | **32** (`SEA-PACKAGE.md` STATUS band) | **32** — and its block carries `own_control_core` ×1 **plus `own_control_integrated` ×1**; a nine-key reader returns 25, which is exactly the SEA phantom |
| **PLB** | **40** (STATUS band) | **40** |
| **BTU** | **6, not 1** (STATUS band) | **6** |
| **MGD in vanilla** | **5, not 1** (STATUS band) | **5** |
| MUA in vanilla | 15 (STATUS band) | **15** |
| `06_pops.txt` blocks / `define_pop` | 28,559 / 50,227 (`AFRICA-PACKAGE.md` §E.3) | **28,559 / 50,227 for lowercase-only keys**; my scanner sees **28,570 / 50,255** because it also catches the **11 uppercase-containing location keys** (`trgoviste_SER`, `targoviste_BUL`, `ratnapura_LKA`, `tata_MOR`, `massa_MOR`, `asir_ALG`, `al_khadra_ALG`, `constantine_ALG`, `beja_TUN`, `jama_TUN`, `matanda_aChiwawa`) carrying **exactly 28 pops** — independently reproducing `KNOWLEDGE.md`'s "11 keys / 28 pops" figure and explaining the earlier packages' number |
| tag scanner, `GHA` | VAN-sub 62, en-loc 1, `west_africa.txt:251` (`AFRICA-PACKAGE.md` §A.2) | **62 / 1 / same** |
| tag scanner, `MAK` | 50 / 1 / `horn_of_africa.txt:240` | **50 / 1 / same** |
| tag scanner, `ZAN` | 134 / 13 / `east_africa.txt:2` | **134 / 13 / same** |
| tag scanner, `TMB` | 48 / 1 / `west_africa.txt:302` | **48 / 1 / same** |
| tag scanner, `PRU` | **VAN word 99**, en-loc 26, sub 429, **empty registry** | **99 / 26 / 429 / empty** |

The `PRU` word column reproduces `AFRICA-PACKAGE.md`'s 99 exactly (my "word"
column excludes localisation files, which is what Africa counted; the SEA
package's 332 counted them and said so).

**Scope.** `tibet_region` (`definitions.txt:3215`), whose six children are
`amdo_area changtang_area kham_area ngari_area tsang_area u_area`. Its parent is
the `east_asia` sub-continent, alongside `east_china_region japan_region
korea_region manchuria_region mongolia_region north_china_region
south_china_region west_china_region xinjiang_region`. **223 ownable locations,
199 owned by 22 tags + one CHI location, 24 unowned, ZERO double-ownership, 781
`define_pop` in total.** Plus one measured, flagged, deliberately-touched
6-location seam outside the region (`xining_province`, `gansu_area`,
`west_china_region`).

---

## 0. Ground truth — six findings, and they change the shape of the slice

### 0.1 THE HEADLINE: vanilla already ships the Era of Fragmentation. It then hangs it off a Sakya hegemony that begins in 1264.

`MOD/main_menu/setup/start/12_diplomacy.txt:396-409` gives **TIB fourteen
vassals**, and `:253` makes TIB itself CHI's vassal. Read the NAME keys
(`VAN/main_menu/localization/english/country_names_l_english.yml`):

| tag | loc line | NAME | what it actually is |
|---|---|---|---|
| **GUG** | `:3340` | **Guge** | Yeshe-Ö's kingdom; capital `toling` = Tholing monastery [D] |
| **PUR** | `:3342` | **Purang** | the third of the Ngari Korsum [D] |
| **MAR** | `:3344` | **Maryul** | Ladakh; capital `shey`, the pre-Leh seat [D] |
| **ZNK** | `:3346` | **Zanskar** | the Zangla valley |
| **MGG** | `:3354` | **Mangyül Gungthang** | the Kyirong/Dzongka principality |
| **POO** | `:3356` | Powo | Poyul, the Kongpo-Kham march |
| **LGT** | `:3360` | Lingtsang | Ling, of the Gesar epic [D] |
| **DRG** | `:3362` | Derge | |
| **NCN** | `:3364` | Nangchen | |
| **GNJ** | `:3366` | Gonjo | |
| **BTG** | `:3368` | Batang | |
| **NBH** | `:3370` | Nubhor | |
| **LTN** | `:3372` | Litang | |
| **LMN** | `:3418` | **Lho Mon** | Bhutan |

**Vanilla built its 1337 Tibet out of the plateau's own regional polities —
including the Ngari Korsum by name — and then subordinated the whole set to a
"Tibet" whose capital is `sakya` and whose government is a theocracy.** That is
the Sakya hegemony (1264+ [U]) and, above it, Yuan overlordship (1240s+ [U]).

**So the 1066 Tibetan correction is FIRST a diplomacy correction** — the same
shape `AFRICA-PACKAGE.md §0.1` found in the Sahel and `SEA-PACKAGE.md §0.1`
found in the Malay world. And here it is cheaper than in either, because
**every one of the fifteen lines names TIB, so retiring TIB dissolves the whole
web through the EXISTING generic sweep** (`build_setup.py:7494-7504`,
`_drop_landless_dep` drops on *either* side). **Zero named strips. Zero
repoints.**

### 0.2 THE SECOND HEADLINE: vanilla DATES the Sakya school itself — to 1073, seven years after start — and our own IO strip has already deleted it

`VAN/main_menu/setup/start/15_international_organizations.txt`, the five
Tibetan-Buddhism `type = sect` instances, with vanilla's own `creation_date`:

| line | sect | `creation_date` | members | survives our strip? |
|---|---|---|---|---|
| `:1417` | Nyingma School | `1.1.1` | `DRG` | **yes** |
| `:1435` | **Kadam School** | **`1030.1.1`** | `KHS PUR MAR` | **yes** |
| `:1454` | **Kagyu School** | **`1050.1.1`** | `ZNK NCN LMN SKK LHL` | **yes** |
| `:1472` | **Sakya School** | **`1073.1.1`** | `TIB CHI GUG MGG LGT LNG KTU POO HOR GNJ NYA GYT GYE CKL` | **NO — already stripped** |
| `:1494` | Jonang School | `1120.1.1` | `GOL AMD SNP MNZ TAZ KHG HEZ JIZ BIR` | **NO — already stripped** |

`build_setup.py:6663-6675` removes any instance whose `creation_date >=
START_DATE`, so **the mod already ships exactly the two schools that existed on
1066.9.15** — Kadam (Atiśa arrived 1042, died 1054; Dromtön founded Reting 1057
[all D]) and Kagyu (Marpa, whose seat Drowolung is in Lhodrak — and `lhodrak`
is one of the 25 locations this package moves, `lhokha_province`). The three
surviving instances are at `MOD/…/15_international_organizations.txt:1034`
(Nyingma), `:1052` (Kadam) and `:1071` (Kagyu).

**This is vanilla's own testimony that Sakya is a post-start object**, and it is
the strongest single argument in the package. It also means the religious half
of this slice is already done, by a mechanism landed months ago, and nobody has
written it down.

### 0.3 The third finding: the plateau has ZERO seatable rulers

**Every one of the 7,736 blocks in `VAN/main_menu/setup/start/05_characters.txt`
was parsed for `tag =`. Exactly six name a theater tag, and the EARLIEST birth
date is 1261.1.1** (`tib_zangpo_pal`, `VAN:96170`, `khon_dynasty`). The others
are `ktu_jayari_malla` 1276, `pur_punyamalla` 1280, `pur_prthivimalla` 1300,
`mar_rinchen` 1300, `tib_namkha_lekpa` 1305. The SEA gift (`adh_narai`, a free
vanilla adult) **does not exist here**.

Three dynasties are homed in the theater and all three are usable if ever
wanted: `khon_dynasty` (`04_dynasties.txt:8215`, `home = sakya`, loc
`dynasty_names_l_english.yml:674` → "Khon"), `lhachen_dynasty` (`:8220`,
`home = shey`, loc `:751` → "Lhachen" — the Maryul royal title),
`purang_dynasty` (`:8225`, `home = purang`, loc `:1069`).

**Consequence: this package seats NOBODY.** See §C for the one candidate that
was costed and the reasons it is refused.

### 0.4 The fourth finding: no rank branch in the game touches a Tibetan tag, but TIB's own render is measurably wrong

`VAN/in_game/common/customizable_localization/country_ranks.txt` is 2,742
lines, first-match. **Every `tag =` line in it was enumerated (68 of them);
not one names a Tibetan tag** — the nearest are `:395 tag = MOM` (Kongo) and
`:1359 tag = LIT`. Every branch was also searched for `tibet|utsang|ladakh|
khampa|amdowa|changpa|sherpa|gyalrong|sikkim|tibeto_burman|bodic|himalay` —
**zero hits.** The MAL/LIT trap and the Africa culture-gate lattice both
**do not exist in this theater**.

What DOES exist is a theocracy ladder, and TIB rides the wrong rung of it:

| branch | line | trigger | fires for TIB? |
|---|---|---|---|
| `rank_kingdom_bishopric` | `:897` | kingdom + theocracy + `religion.group = religion_group:christian` | no |
| `rank_kingdom_theocracy_dharmic` | `:907` | kingdom + theocracy + **`religion_group:dharmic`** | **NO** — `tibetan_buddhism` is `group = buddhist` (`VAN/in_game/common/religions/buddhist.txt:110-112`), not dharmic |
| **`rank_kingdom_theocracy`** | **`:917`** | kingdom + theocracy | **YES** |

`VAN/main_menu/localization/english/government_names_l_english.yml:503-507`:
`rank_kingdom_theocracy: "Theocracy"`, `_prefix: "Grand"`,
`_ADJ: "theocratic"`, `_ruler_male: "Grand Priest"`.

**So TIB renders today as "Grand Theocracy of Tibet", map label "Tibet", ruler
"Grand Priest"** — the `rank_duchy` Muslim theocracy trap that
`HANDOFF.md:1911` recorded from the Arabia package, one rung up. It is the
correct render for a Sakya hierarch and the wrong one for anything in 1066.
Retiring TIB removes it; the alternative branches in §OPEN 2 must live with it
or pay to change it.

### 0.5 The fifth finding: TIB is a FORMABLE, and its claim block is already the whole plateau

`VAN/in_game/common/formable_countries/00_formable_countries.txt:3101`:

```
TIB_f = {
	level = 2
	required_locations_fraction = 0.6
	rule = historical
	potential = { culture = { has_culture_group = culture_group:tibetan_group } }
	name = TIB   flag = TIB   adjective = TIB_ADJ   tag = TIB   color = map_TIB
	regions = { tibet_region }
	form_effect = { }
}
```

`culture_group:tibetan_group` is `VAN/in_game/common/culture_groups/00_culture_groups.txt:210`
and carries `utsang_culture`, `khampa_culture`, `amdowa_culture`,
`ladakh_culture`, `changpa_culture`, `sherpa_culture`, `sikkim_culture` and
more (`cultures/east_asia.txt:1225 :1241 :1261 :1790 :1807 :1842 :1854 :1920
:1936 :1950 :1967`). 0.6 × 223 ownable = **134 locations** to reunify Tibet [the
fraction's denominator — ownable vs raw membership — is not settled by any file
and is flagged as OWED CHECK 2].

And TIB's block already carries **131 claims** in
`our_cores_conquered_by_others` (`MOD/…/10_countries.txt:44006`ff), covering
`ngari_area` 33, `kham_area` 67, `amdo_area` 28, `u_area` 3 — **with zero
overlap with its own 59 holdings**. So a landless TIB ends with **190 claims**,
i.e. essentially the entire plateau, written mostly by Paradox.

**A landless TIB is therefore not a deletion but a reunification target** — the
project's own Pecheneg philosophy ("a state EARNED by events",
`HANDOFF.md:950-955`) with the machinery already in place. **And a formable
target that exists as a landless shell is normal in this very repo: 27 vanilla
formables already point at a tag the current build leaves landless** (`WLS_f`,
`DLH_f`, `LAT_f`, `LIV_f`, `ULS_f`, `TIM_f`, `ARM_f`, `BUL_f`, `FIN_f`,
`YUA_f`…), and 29 more point at tags that are landed.

### 0.6 The sixth finding: the registry file is ALREADY a mod override, so registry surgery here is a one-liner

`MOD/in_game/setup/countries/east_asia.txt` is a whole-file override (the fifth
of the mod's five, `SEA-PACKAGE.md §B.3`), diffed against vanilla: a five-line
header comment plus **exactly one changed line** — CHI's `color = map_YUA` →
`map_CSO` (item 32's Yuán→Sòng reskin). Every Tibetan identity block sits in it
at a +5 line offset from vanilla:

| tag | VAN `east_asia.txt` | MOD `east_asia.txt` | `culture_definition` | `religion_definition` | `color` |
|---|---|---|---|---|---|
| TIB | `:2179` | **`:2184`** | `utsang_culture` | `tibetan_buddhism` | `map_TIB` |
| GUG | `:2187` | `:2192` | `utsang_culture` | `tibetan_buddhism` | `map_GUG` |
| PUR | `:2195` | `:2200` | `utsang_culture` | **`hindu`** | `map_PUR` |
| MAR | `:2203` | `:2208` | `ladakh_culture` | `tibetan_buddhism` | `map_MAR` |
| ZNK | `:2211` | `:2216` | `ladakh_culture` | `tibetan_buddhism` | `map_ZNK` |
| MGG | `:2254` | `:2259` | — | — | `map_MGG` |
| (the other 33) | `:2262`-`:2543` | +5 each | — | — | — |

**PUR's `religion_definition = hindu` is a live oddity** — Purang is
`tibetan_buddhism` on all four of its area's locations, and vanilla's own Kadam
sect lists PUR as a member with the comment "#Purang capital, Tholing
Monastery, is Kadam". It is a one-token fix in a file the mod already owns
(OPEN DECISION 7). **The Gallura cost is already paid: this package proposes no
new registry override.**

### 0.7 Ownership, culture and religion, measured per area and per province

Ownable counts resolved from `definitions.txt`; culture/religion from
`location_templates.txt`; owners from `MOD/main_menu/setup/start/10_countries.txt`
with the full ten-key reader; `define_pop` from `VAN/main_menu/setup/start/06_pops.txt`.

| area | ownable | pops | owners today |
|---|---|---|---|
| `amdo_area` | **48** | 149 | unowned 15, AMD 12, GOL 8, NCN 8, LGT 4, CHI 1 |
| `changtang_area` | **16** | 15 | unowned 9, TIB 7 |
| `kham_area` | **75** | 326 | GNJ 10, BTG 9, NBH 8, DRG 7, POO 7, CKL 6, HOR 5, GYE 4, LGT 4, GOL 4, LTN 3, YNG 3, TIB 3, NYA 2 |
| `ngari_area` | **38** | 151 | MAR 16, GUG 7, TIB 5, MGG 5, ZNK 3, PUR 2 |
| `tsang_area` | **18** | 55 | **TIB 18** |
| `u_area` | **28** | 85 | **TIB 25**, POO 3 |
| **total** | **223** | **781** | 22 tags + CHI; **24 unowned**; **zero double-ownership** |

**Religion and culture are uniform and 1066-correct already.** Of the 223
locations, `tibetan_buddhism` covers everything except: `bon` on 8
(`gyelrong_province` 5, `dartsedo_province` 2, `muli_province` 1) and
`bimoism` on 2 (`muli_province`). Cultures: `amdowa_culture` 48,
`khampa_culture` ~55, `utsang_culture` ~40, `changpa_culture` 16,
`ladakh_culture` ~15, `gyalrong_culture` 8, `sherpa_culture` 3, plus `yi`/`pumi`
in Muli. **The pop phase inherits almost nothing from this theater** — unlike
al-Andalus (222 wrong locations) or the Hausa registries.

**The pop density is the lowest the project has met: 223 locations carry 781
`define_pop`, 3.5 per location.** Compare Africa's `bornu_area` at 76 for 18
(4.2) and SEA's `chao_phraya_area` at 99 for 36 (2.75). A vacate here is cheap.

TIB's own 59, resolved per province — this is the table the whole design rests
on:

| area | province | TIB holds | of | pops | who else |
|---|---|---|---|---|---|
| `u_area` | `u_province` | **8** | 8 | 24 | — (`lhasa damzhung drigung galo gyama taklung tsora tsurphu`) |
| `u_area` | `lhokha_province` | **7** | 7 | 22 | — (`trigu chikchar gonpatsi lhodrak lho_taklung tragor zangchen`) |
| `u_area` | `yarlung_province` | **6** | 6 | 18 | — (`nedong densatil gongkar nyemo rinpung_yarlung samye`) |
| `u_area` | `kongpo_province` | **4** | 4 | 12 | — (`gyamda buchu daklha_gampo zhokha`) |
| `tsang_area` | `lhato_province` | **5** | 5 | 16 | — (`sakya ganden_delingshar lhadrak ngamring tagmo_lingkha`) |
| `tsang_area` | `dingri_province` | **5** | 5 | 15 | — |
| `tsang_area` | `tsang_province` | **5** | 5 | 15 | — (`shigatse jonang namling tropu tsangdram`) |
| `tsang_area` | `nyang_province` | **3** | 3 | 9 | — (`gyantse nenying ralung`) |
| `changtang_area` | `namru_province` | **4** | 5 | 6 | 1 unowned |
| `changtang_area` | `naktsang_province` | **3** | 3 | 9 | — |
| `kham_area` | `nakchukha_province` | **3** | 3 | 9 | — (`nakchu barom rongpo`) |
| `ngari_area` | `lungkha_province` | **3** | 3 | 9 | — (`mendong samten selephu`) |
| `ngari_area` | `rutok_province` | **2** | 8 | 4 | MAR 4, GUG 2 |
| `monyul_area` (bengal_region) | `sikkim_province` | **1** | 5 | 3 | SKK 4 — the location is `phari`, the Chumbi valley |
| **total** | | **59** | | **171** | |

Two things this settles. **TIB owns `u_area` and `tsang_area` outright except
for POO's three in `pemako_province`** — the two areas are a clean,
definitions-resolvable pair. And **`sakya` itself sits in `lhato_province`,
i.e. in TSANG, not in Ü** — a detail any redistribution has to get right.

---

## A. Registry

### A.1 What already exists and needs nothing

The theater's 38 identity blocks in `east_asia.txt` supply almost every polity
1066 needs, with vanilla arms, vanilla loc and vanilla colours.

| tag | MOD registry | holds | why it is right at 1066 |
|---|---|---|---|
| **GUG** Guge | `:2192` | 7 → **12** | Yeshe-Ö's Ngari kingdom; capital `toling` **is** Tholing monastery, founded 997 [D]. Its king in 1066 would be Tsede, with the royal monk Jangchub Ö (Atiśa's patron, d. 1078) alive [both D] |
| **PUR** Purang | `:2200` | 2 | the Ngari Korsum's third district; absorbed by Guge c. 1100 [D], so distinct at 1066 |
| **MAR** Maryul | `:2208` | 16 | Ladakh; capital `shey` is the pre-Leh royal seat [D] and `lhachen_dynasty` is homed there |
| **ZNK** Zanskar | `:2216` | 3 | |
| **MGG** Mangyül Gungthang | `:2259` | 5 | capital `dzongkar` (Dzongka) — the Kyirong seat |
| **the eleven Kham tags** POO HOR LGT DRG NCN GNJ BTG NBH LTN NYA CKL | `:2267`-`:2499` | 2-10 each | vanilla's Khampa-chiefdom patchwork. Their individual king-lists are 13th-18th century [all D], but a patchwork of small lay and monastic lordships **is** 1066 Kham. §D.3 |
| **AMD GOL GYE** | `:2481`-`:2508` | 4-12 | Amdo and Gyelrong; same reasoning |
| **LMN** Lho Mon | `:2541` | 9 | Bhutan; capital `paro`. §D.5 |
| **MSH TAN MNP** | `:2517`-`:2533` | 0 | `type = pop` countries (`10_countries.txt:44798 :44817 :44838`) — vanilla's legitimate landless class, the SEA `type = pop` precedent |

**GUG's NAME key is "Guge", MAR's is "Maryul", MGG's is "Mangyül Gungthang".**
A reader who greps for "Ladakh" or "Gungthang" finds only the *location* or
nothing — this theater's `ZAN: "Kilwa"` trap.

### A.2 Freeness of the new candidates — three scans each

Per `BALTIC-PACKAGE.md §A.2` / `AFRICA-PACKAGE.md §A.2` / `SEA-PACKAGE.md §A.2`:
(1) word-boundary `\bTAG\b` over the whole vanilla tree, non-localisation and
English-localisation counted separately; (2) **substring** `_TAG\b|\bTAG_` over
the same tree; (3) both over the whole mod repo. Text files only
(`.txt .yml .gui .info .asset .gfx .py .md .json .mod .csv .log .settings`) —
`KNOWLEDGE.md`, "Tag-freeness sweeps MUST exclude binaries". Registry index read
`utf-8-sig` over BOTH `in_game/setup/countries/` trees, **unanchored** — the BOM
trap.

| candidate | VAN word | VAN en-loc | VAN sub | MOD word | MOD sub | registry | verdict |
|---|---|---|---|---|---|---|---|
| **DBU** (Ü / dBus) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **GTS** (Tsang / gTsang) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| **TKA** (Tsongkha) | 0 | 0 | 0 | 0 | 0 | — | **FREE** |
| QTG (Qingtang) | 0 | 0 | 0 | 0 | 0 | — | free (banked, the Chinese-name alternative for TKA) |
| GSL (Gusiluo) | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| QNT | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| UTS, YLG, MYG, NGC, CGT, NGA, PHM, ZHL, RTG | 0 | 0 | 0 | 0 | 0 | — | free (banked) |
| **TSO** | 20 | 1 | 48 | 1 | 18 | `VAN:eastcoast.txt:276` | **TAKEN** — a North American tag |
| **TSN** | 21 | 1 | 48 | 1 | 18 | `VAN:eastcoast.txt:306` | **TAKEN** — likewise |
| **TSG** | 23 | 1 | 48 | 4 | 18 | `VAN:east_africa.txt:242` | **TAKEN** — East Africa. The obvious "Tsang" mnemonic is gone |
| **YAR** | 30 | 1 | 50 | 9 | 18 | `VAN:russia.txt:106` | **TAKEN** — Yaroslavl. The obvious "Yarlung" mnemonic is gone |
| **SKY** | 35 | 1 | 61 | 10 | 18 | `VAN:russia.txt:260` | **TAKEN** — the obvious "Sakya" mnemonic is gone (and unwanted) |
| **SHL** | 19 | **3** | 67 | 0 | 12 | — | **TAKEN, empty registry** — `SHL: "Holstein"` (`country_names_l_english.yml:2003`), `SHL_f` (`formable_countries_l_english.yml:213`), named in `flavor_dan.8`. The PRU class |
| **LHG** | 0 | 0 | **13** | 0 | 0 | — | **AVOID** — the 13 hits are a `LHG_` loc PARAMETER in `interfaces_l_*.yml` (`english:2489`, and 12 other languages). The `CAP` class (`KNOWLEDGE.md`, "Tag-freeness sweeps MUST exclude binaries") — not proven taken, conservative to avoid |
| **LHS** | 0 | **2** | 0 | 1 | 0 | — | **AVOID** — `APPEND_RHS: "$LHS$…"` (`core_l_english.yml:436`), a loc parameter. Same class |

`TSO`, `TSN`, `TSG`, `YAR` and `SKY` are the scanner earning its keep: **five of
the six obvious mnemonics for this theater belong to countries on other
continents**, and `TSG`/`YAR` in particular would have read plausibly to a
hurried reader.

### A.3 The new blocks — three tags

Appended to `MOD/in_game/setup/countries/zz_1066_new_countries.txt` (registry
**71 → 74**; current count measured **71** with a BOM-safe reader, the file's
tail being `… DJN SNH PGN HPJ KDR JGL`). Shape copied verbatim from that file's
own PGN/HPJ tail.

```
DBU = { #Ü (dBus) — central Tibet east of the Tsangpo bend, seat Lhasa
	color = map_TIB
	color2 = rgb { 16 41 202 }

	culture_definition = utsang_culture
	religion_definition = tibetan_buddhism
}

GTS = { #Tsang (gTsang) — central Tibet west of Ü, seat Shigatse
	color = map_GTS
	color2 = rgb { 16 41 202 }

	culture_definition = utsang_culture
	religion_definition = tibetan_buddhism
}

TKA = { #Tsongkha — the Amdo kingdom of Gusiluo's line, seat Qingtang/Xining
	color = map_TKA
	color2 = rgb { 16 41 202 }

	culture_definition = amdowa_culture
	religion_definition = tibetan_buddhism
}
```

`culture_definition` is a landed tag's PRIMARY culture, not decoration
(`KNOWLEDGE.md`, "The registry's culture_definition IS a landed tag's primary
culture — measured"). DBU's and GTS's 44 locations are `utsang_culture`
throughout (measured, §0.7) — no mismatch.

**TKA's is this package's ONE deliberate mismatch and it is a large one.**
`xining_province`'s six locations are `liang_culture` 4 + `monguor_culture` 2 in
`location_templates.txt`, and `sanjiao` 4 + `mahayana` 2 — i.e. painted for the
**post-1104 Song Xining**, after Wang Shao's Hehuang campaigns took the valley
[U]. A Tibetan Tsongkha over Chinese-and-Monguor pops is the al-Andalus / PAA /
HPJ precedent (`build_setup.py:1487-1489`), and it is flagged in OPEN DECISION 3
and banked for `POP-PHASE.md`.

### A.4 Colours — one reuse, two new keys

`VAN/main_menu/common/named_colors/02_map.txt` carries **3,742 `map_*` keys**.
Every `color = <key>` in both `setup/countries` trees plus every inline
`color = map_*` in both `10_countries.txt` files was indexed.

| key | line | value | used by a country today |
|---|---|---|---|
| **`map_TIB`** | `:2596` | `rgb { 177 207 205 }` pale sage | **yes — TIB**, which this package retires |
| `map_tibetan` | `:2410` | `rgb { 177 207 205 }` — the SAME value | **no country** — but it is `tibetan_language`'s own colour (`in_game/common/languages/00_tibet.txt:3`) |
| `map_changpa` | `:2589` | `rgb { 80 70 120 }` | no |
| `map_sherpa` | `:2584` | `rgb { 165 180 200 }` | no |
| `map_khampa` | `:2411` | `rgb { 150 170 205 }` | no |
| `map_amdowa` | `:2412` | `rgb { 90 120 135 }` | no |
| `map_GUG` | `:2597` | `rgb { 200 175 110 }` ochre | yes — GUG, which survives |
| `map_MGG` | `:2602` | `rgb { 170 115 105 }` | yes — survives |
| `map_POO` | `:2603` | `rgb { 130 90 180 }` violet | yes — survives, and is Ü's south-eastern neighbour |
| `map_NBH` | `:2610` | `rgb { 170 90 55 }` | yes — survives |
| `map_sikkim` | `:2630` | `rgb { 93 180 76 }` | yes — SKK |
| `map_tangut` | `:2434` | `rgb { 170 95 126 }` | XIA wears this VALUE via `map_XIA` |

**Recommendation.**
- **DBU takes `map_TIB`** — a *retiring* tag's key, the PGN/`map_burmese`
  precedent exactly (`SEA-PACKAGE.md §A.4`); a landless shell paints nothing,
  and central Tibet then renders in Tibet's own colour. **This is valid only
  under the recommended TIB retirement — under OPEN DECISION 2's alternatives it
  collides and DBU needs its own key.**
- **GTS and TKA take NEW keys** in `MOD/main_menu/common/named_colors/zz_1066_map_colors.txt`.
  Both key NAMES were proven absent from vanilla by the substring scan
  (`_GTS\b|\bGTS_` and `_TKA\b|\bTKA_` both return **0** over the whole vanilla
  tree, which is what `map_GTS`/`map_TKA` would match) — the AUDIT-D3 lesson.
  Suggested values, chosen against the measured neighbours and flagged as
  eyeball items:

```
	# Tibet. DBU wears vanilla's own map_TIB (02_map.txt:2596, freed by
	# TIB's retirement). GTS against DBU's pale sage, GUG's ochre
	# (200 175 110), MGG's terracotta (170 115 105) and POO's violet
	# (130 90 180); TKA against XIA's Tangut rose (170 95 126), CHI's
	# map_CSO crimson (153 51 51), AMD's green (90 180 90) and GOL's
	# sand (193 179 127). Both key names verified absent from vanilla
	# BY NAME (zero substring hits — the D3 lesson).
	map_GTS = rgb { 62 118 130 }    # Tsang       plateau teal
	map_TKA = rgb { 196 126 44 }    # Tsongkha    Kokonor amber
```

### A.5 Coats of arms

All three new tags must land in `_GENERATOR_OK` (`tools/verify_mod.py:1003`) or
carry CoA blocks; the check at `:1055-1061` fails a new registry tag that has
neither, `:1062` fails a stale entry, and `:1082` counts them (`min_count = 122`).

**Recommendation: `_GENERATOR_OK`, tier 4, permanent, for all three.** Tibetan
polities used seals, banners and monastic emblems, not shields; there is no
heraldry to reproduce. This is the taifa / Baltic / SEA rationale verbatim
(`verify_mod.py:1005-1008`, `:1041-1046`, `:1051-1055`).

**TIB keeps vanilla's arms** — it is retired, not deleted, and a landless tag
passes through `_van_coa_keys`. Every other tag this package touches (GUG, NBH,
SKK, MAR, PUR, MGG, AMD, GOL…) is vanilla with vanilla arms. **Zero CoA
authoring.**

### A.6 Localisation

Six rows in `MOD/main_menu/localization/english/1066_norman_conquest_l_english.yml`,
one physical line each, UTF-8 **with** BOM (the loc-row checks are
`verify_mod.py:167` and `:174`, both `min_count = 367`; they rise to 373):

```
 DBU: "Ü"
 DBU_ADJ: "Ü"
 GTS: "Tsang"
 GTS_ADJ: "Tsang"
 TKA: "Tsongkha"
 TKA_ADJ: "Tsongkha"
```

`"Ü"` is a single non-ASCII character and it **is** the standard English name of
the province (vanilla itself ships "Mangyül Gungthang" and "Yǒngníng" with
diacritics, `country_names_l_english.yml:3354` and `:3378`). It may also read as
a rendering fault on the map — OPEN DECISION 5 offers `"Ü-Tsang"`, `"Lhasa"` and
`"Uru"` as alternatives. Every other name in this package is vanilla's.

---

## B. The country blocks

### B.1 The three new `NEW_COUNTRIES` blocks

```
	DBU = {
		starting_technology_level = 3
		include = "east_asia_monarchy_no_coast"

		capital = lhasa
	}

	GTS = {
		starting_technology_level = 3
		include = "east_asia_monarchy_no_coast"

		capital = shigatse
	}

	TKA = {
		starting_technology_level = 3
		include = "east_asia_monarchy_no_coast"

		capital = xining
	}
```

Field by field, verified:

- **`include = "east_asia_monarchy_no_coast"`** —
  `VAN/main_menu/setup/templates/east_asia_monarchy_no_coast.txt`, 63 lines,
  read in full: line 2 is `include = "expl_china"`, and the `government` block
  declares `type = monarchy`, `heir_selection = cognatic_primogeniture`,
  `parliament = { parliament_type = council }`, the slider set, laws and
  privileges. It carries **no `reforms = { }` block**. This is the template GUG,
  PUR, MAR, ZNK, MGG, POO, HOR, DRG, NCN and GNJ all ride today (measured from
  `MOD/…/10_countries.txt`), so the three new tags match their neighbours
  exactly. `_no_coast` is correct: all three are landlocked, and the other
  variants are `east_asia_monarchy.txt` (coastal) and
  `east_asia_monarchy_not_present.txt`.
- **Discovery.** `VAN/main_menu/setup/templates/expl_china.txt` (25 lines) has
  `discovered_regions = { indonesia_region indochina_region tibet_region
  west_china_region east_china_region mongolia_region north_china_region
  south_china_region korea_region japan_region manchuria_region bengal_region
  western_india_region central_india_region deccan_region xinjiang_region
  hindustan_region }`. `lhasa` and `shigatse` resolve into `tibet_region`,
  `xining` into `west_china_region` (`xining_province` → `gansu_area` →
  `west_china_region`, resolved from `definitions.txt`). **All three pass
  `_assert_new_block_discovery`** (`tools/build_setup.py:5488`, exit at `:5517`)
  with no extra include.
- **`starting_technology_level = 3`** — the template's own value and what every
  landed Tibetan monarchy carries (measured: TIB, GUG, MAR… all 3; the
  tribe-template tags carry 2 via `asia_advanced_no_pagan_tribe`). Matching is
  the local convention, not a judgement.
- **NO `country_rank` line.** This is deliberate and it is the theater's rule:
  **of the 22 tags holding land in `tibet_region`, exactly ONE declares a
  `country_rank` — TIB (`rank_kingdom`).** Every other one leaves it to the
  engine. Declaring nothing matches 21 of 22 and asserts nothing; see §F.3 for
  what that costs in predictability.
- **Capitals.** `lhasa` (`u_province`), `shigatse` (`tsang_province`) and
  `xining` (`xining_province`) are all real locations, all inside their own
  tag's resolved grant list (§E.1), so the orphan-capital guard
  (`build_setup.py:6566`) stays silent. **There is no `qingtang`, `tsongkha`,
  `hehuang`, `miaochuan`, `dbus`, `tsang`, `yarlung`, `shalu`, `reting` or
  `sangphu` location** (each probed: zero hits in `definitions.txt`) — `xining`
  IS Qingtang, the Tsongkha capital, under its Chinese name.

### B.2 The tags this package RESHAPES rather than creates

| tag | today (measured, `MOD/main_menu/setup/start/10_countries.txt`) | 1066 change |
|---|---|---|
| **TIB** | `:44006`, 59 locations, `capital = sakya`, **`country_rank = rank_kingdom`**, inline `government = { type = theocracy  heir_selection = theocratic_elective … }`, `tolerated_cultures = { changpa_culture khampa_culture }`, 131 claims, `include = "expl_china"` **only** (no government template — the block is fully inline) | → **LANDLESS with claims.** No field surgery at all: the whole block stays as vanilla wrote it, the ownership lists empty, the claims list grows to 190. `LANDLESS_AFTER` + `_landless_claims` do all of it |
| **GUG** | `:44121`, 7, `capital = toling`, no rank, `east_asia_monarchy_no_coast` | → **+5** (§E.1). Zero field surgery |
| **NBH** | `:44464`, 8, `capital = biru`, no rank, `asia_advanced_no_pagan_tribe` | → **+3** (§E.1). Zero field surgery |
| **PUR** | `:44136`, 2, `capital = purang`, `east_asia_monarchy_no_coast`, **registry `religion_definition = hindu`** | → registry one-token fix under OPEN DECISION 7; otherwise untouched |
| **CHI** | `:26245`, **1,306** locations after items 30/32/34 | → **−6** (`xining_province`) under OPEN DECISION 3. The seam is *measured*, not redesigned — no rank, ruler, capital, reform, law or culture change |

### B.3 Registry overrides — NONE proposed

`MOD/in_game/setup/countries/east_asia.txt` is already an override and stays at
its **one** intended deviation from vanilla. OPEN DECISION 7 (PUR's `hindu`)
would make it two, in the same already-owned file, at a cost of one token. The
`verify-vanilla-override` skill's re-diff-after-every-patch duty already applies
to this file and does not grow.

---

## C. Rulers — nobody, and the reasoning is the point

**No ruler enters this package.** The theater has no seatable person and the
project's own standard says so out loud.

| tag | 1066 candidate | why NOT seated |
|---|---|---|
| **TKA** Tsongkha | **Dongzhan** (董氈), son of Gusiluo, r. 1065-1086 [D] | **The best-attested 1066 ruler on or near the plateau** — Gusiluo (rGyal-sras, c. 997-1065 [D]) died the year before start and his son succeeded. But "Dongzhan" is a **Chinese transcription** whose Tibetan original is not settled [D], the name is absent from `character_names_l_english.yml` and from `character_names_dynamic_l_english.yml` (both probed), and no dynasty key exists. Cost if wanted: one `NEW_CHARACTERS` block, one invented `name_dongzhan` key + one loc row (the mod already ships that pattern 24 times, `1066_norman_conquest_l_english.yml:116-259`), one new dynasty. **OPEN DECISION 4** |
| **GUG** Guge | **Tsede** (rTse-lde), r. c. 1057-1088 [D]; or the royal monk **Jangchub Ö**, d. 1078 [D] | The Guge king-list is reconstructed from inscriptions and the *mNga' ris rgyal rabs*, and the two readings disagree about who held the throne versus the monastic office in 1066 [D]. Neither name exists as a key. **The Cadalus rule** |
| **MAR** Maryul | a Lhachen [D] | The *La dvags rgyal rabs* king-list for the 11th century is a late chronicle with no agreed regnal dates [D]. `lhachen_dynasty` ships and is homed at `shey` — the house is available the moment a name is |
| **DBU / GTS** | **nobody, and there is nobody** | Ü and Tsang in 1066 are a patchwork of lay lords (*sde pa*) and the first monastic estates; no chronicle names a ruler of either province. This is the theater's Pecheneg case (`HANDOFF.md:950-955`) and its Moray/Galloway case (`HANDOFF.md:786`) |
| **everyone else** | — | `INDIA-CHINA-REVIEW.md:660` already reached this verdict for TIB — "genuinely fragmented [D] … leave `ruler = random`, the honest answer" — and this package extends it to the whole plateau |

**Recommendation: seat ZERO. Thrones stay at 178.** The name material is on
disk if a later session wants it — `VAN/in_game/common/languages/00_tibet.txt:1`
defines `tibetan_language` (family `tibetic_language_family`, colour
`map_tibetan`) with ~110 male-name literals, of which `Yeshe`
(`character_names_l_english.yml:14460`), `Rinchen` (`:14435`), `Namkha`
(`:14416`), `Dorje` (`:14380`), `Osel` (`:14425`) and `Tashi` (`:14350`) all
carry English loc rows in the block at `:14350-14474`. **None of the four names
this package would actually need is among them.**

---

## D. What must die, what must be left, and where the seams are

### D.1 Ü and Tsang — the theater's one real question

| tag | holds | what it is at 1066 | verdict |
|---|---|---|---|
| **TIB** "Tibet" | **59** | A theocracy at Sakya. **Sakya monastery is founded in 1073** — vanilla's own IO instance says so to the year (`VAN/…/15_IO.txt:1472`, `creation_date = 1073.1.1`) — and the Sakya *hegemony* over Tibet is 1264+ [U]. The tag's government (`theocracy` + `theocratic_elective`), its capital (`sakya`), its 14 vassals and its own CHI overlord are all one object, and the object is the Yuan settlement | **RETIRE landless with claims.** 131 existing + 59 = **190 claims**, the whole plateau, and `TIB_f` (§0.5) is the reunification path |
| **DBU** *(new)* | 0 → **25** | `u_area` minus POO's `pemako_province`: Lhasa, Yarlung, Lhodrak, Kongpo | **CREATE.** The name is a **region**, not a dynasty — vanilla's own grammar (AMD "Amdo", GOL "Golog", GYE "Gyelrong", HOR "Hor" are all regions or peoples, not houses) |
| **GTS** *(new)* | 0 → **19** | `tsang_area` whole plus `phari`: Shigatse, Gyantse, Sakya, Dingri | **CREATE.** Same reasoning |

**Why two tags and not one, and not none.** One tag over all 43 is TIB again
under a different name — it asserts a unified central Tibet that did not exist.
Zero tags means vacating 43 locations and 131 pops, which is historically the
closest reading and leaves the most populated part of the plateau blank. Two is
the cheapest split that says "Ü and Tsang were separate and neither was
unified", which is what every account of the fragmentation says [D]. **OPEN
DECISION 1 carries all three options with their costs.**

### D.2 Amdo and the Gansu seam

| tag | holds | verdict |
|---|---|---|
| **TKA** *(new)* | 0 → **6** | **CREATE — OPEN DECISION 3.** Tsongkha/Qingtang is the one *named, dated, externally attested* polity in the theater: Gusiluo's Song-allied Tibetan kingdom of the Huangshui, unconquered by the Song until 1104 [U]. `NORTHERN-DYNASTIES-PACKAGE.md:1035` excluded `xining_province` from XIA specifically and banked it "for a Tibet/Amdo pass, not fixed here" — **this is that pass.** The ground is CHI's, which makes it a flagged seam touch |
| **AMD** Amdo (12), **GOL** Golog (12), **NCN** Nangchen (8), **LGT** Lingtsang (8) | 40 | **KEEP ALL UNCHANGED.** Amdo's tribal confederations are the right model at any date. Their CHI *tusi* ties are OPEN DECISION 6 |
| **the seven `longyou_area` tags** MNZ 6, KHG 4, TAZ 3, HEZ 2, BIR 1, JIZ 1 (+SNP 8 in `chuanxi_area`) | 25 | **LEAVE ALONE — flagged.** `NORTHERN-DYNASTIES-PACKAGE.md:1037` called them "a Tibet-pass matter"; on measurement they are a **Song-frontier** matter, not a plateau one: `hezhou_province` is `sarta_culture`/`salar_culture` sunni 2 + `amdowa` 2, `taozhou_province` is `amdowa` 7 + `sarta` 1, and all seven are CHI's vassals or *tusi* whose 1066 ancestor is the Song *jimi* prefecture system (`build_setup.py:7346-7368`, the jimi-fix comment). §D.6 |

### D.3 Kham — the biggest "leave it alone" in the package

Eleven tags hold 71 of `kham_area`'s 75 locations (`chamdo` GNJ 3, `derge` DRG 7,
`nubhor` NBH 8, `poyul` POO 4, `tehor` HOR 3, `lithang` LTN 3, `setha` GOL 4,
`gyelrong` GYE 4, `dartsedo` CKL 3, `muli` YNG 3, …). **Their individual state
histories are late** — Derge's principality is 15th-16th century, Batang and
Litang are Ming/Qing *tusi* names, Lingtsang's chiefdom is 13th-century [all D].
**But the MODEL is right**: eastern Tibet in 1066 was a patchwork of lay
lordships and valley chiefdoms with no overlord, which is precisely what the map
shows once TIB's fourteen vassalages are gone.

**Verdict: KEEP ALL ELEVEN, change nothing but their independence.** Retiring
them would cost eleven retirements, ~326 pops of vacate or a redistribution to
nobody, and would replace a defensible patchwork with an empty one. This is the
Shan-states decision (`SEA-PACKAGE.md` OPEN DECISION 5) and the Philippines
decision (`SEA-PACKAGE.md §H`) taken again on the same reasoning, and it is
flagged as OPEN DECISION 8 so the main session can refuse it.

**One hard constraint the review must not miss: `DRG` is the SOLE member of the
Nyingma sect** (`MOD/…/15_international_organizations.txt:1034`, `members = {
DRG }`). Retiring DRG in any future slice **drains that IO** and trips the
pinned-9 empty-members check (`verify_mod.py:910`). Recorded here so nobody
rediscovers it.

### D.4 Ngari — correct as shipped, and the one growth

| tag | holds | verdict |
|---|---|---|
| **GUG** Guge | 7 → **12** | **KEEP + GROW.** Takes TIB's `lungkha_province` 3 and its two `rutok_province` outliers, both adjacent to GUG's own `gartok`/`rala`. Capital `toling` is Tholing monastery — the most historically exact capital in the theater |
| **PUR** Purang | 2 | **KEEP.** Registry religion fix in OPEN DECISION 7 |
| **MAR** Maryul | 16 | **KEEP UNCHANGED.** Capital `shey` correct; `lhachen_dynasty` homed there |
| **ZNK** Zanskar (3), **MGG** Mangyül Gungthang (5) | 8 | **KEEP UNCHANGED** |

### D.5 The Himalayan rim and Bhutan

| tag | holds | verdict |
|---|---|---|
| **LMN** Lho Mon | 9 (`western_bhutan_province` 6, `eastern_bhutan_province` 3) | **KEEP UNCHANGED.** Bhutan in 1066 is pre-Drukpa; "Lho Mon" (the southern Mon country) is a Tibetan geographic label, not a state name, which is exactly right. Its TIB vassalage dies free |
| **SKK** Sikkim | 4 in `sikkim_province` | **KEEP UNCHANGED.** `sikkim_culture`/`mahayana`; the Namgyal monarchy is 1642 [U] but the tag is a region label. `phari` is NOT given to it — see §E.1 |
| **MSH, TAN, MNP** | 0, `type = pop` | **DO NOT TOUCH.** Vanilla's legitimate landless class |
| **KHS** Khasa (18), **KTU** Kathmandu (6), **LHL** Lahul (2) | 26 | **DO NOT TOUCH — the Nepal/Himalaya seam.** `INDIA-TIER1-PACKAGE.md:986` explicitly left "the Himalayan belt — KHS LWA KMN GWL KTU DTI SRM JBL, 61 locations in `nepal_area`" as "its own review", and `:987` left `upper_indus_area` (Kashmir) likewise. **Item 34 touched neither**, and neither does this package |

### D.6 The measured seams — named, not touched

| what | measurement | why not here |
|---|---|---|
| **CHI** | 1,306 locations after items 30/32/34 (vanilla 1,661); Yuán→Sòng reskin via `FIELD_FIXES["CHI"]` (`build_setup.py:3243-3270`), which also **deletes `amdowa_culture` from CHI's tolerated list** (`:3268`) — a Tibet-adjacent change already landed | done — items 30/32. **This package's ONE touch is −6 (`xining_province`)** under OPEN DECISION 3, flagged for explicit sign-off |
| **XIA** | 48 locations (`build_setup.py:1469-1473`); `xining_province` **deliberately excluded** with the comment "Qingtang/Tsongkha … a different slice's wrong" (`:1466-1468`) | done — item 33. This package is the slice that comment names |
| **The Middle Kingdom IO** | `MOD/…/15_IO.txt:164`, **199 members**, re-dated 1271→960 by item 30's Route B (`build_setup.py:6638-6644`). **Twenty-one of its members are Tibetan-plateau or Sino-Tibetan-frontier tags** — TIB HOR NYA GYT YNG TNQ MCI WMO TSK SNP LGZ MNZ TAZ KHG HEZ JIZ BIR GYE GOL CKL AMD | done — item 30. Retiring TIB removes exactly ONE (199 → 198). **Whether the Song *tianxia* should list Golog and Amdo at 1066 is a China-review question** — measured, flagged, not proposed |
| **The 18 CHI *tusi*/vassal ties over Tibetan-culture tags** | `MOD/…/12_diplomacy.txt:242 :243 :245 :250 :252` (vassal: HEZ JIZ MNZ SNP TAZ), `:258-264` (*tusi*: TNQ MCI WMO TSK LGZ KHG BIR), `:270-275` (*tusi*: HOR NYA GYE GOL AMD CKL) | OPEN DECISION 6 proposes a **four-line** subset; the rest is the China review's |
| **`bengal_region/monyul_area`** | 32 ownable: CUT 5, LMN 9, AHO 2, SKK 4, TIB 1 (`phari`), **12 unowned** | the India/Assam seam. This package moves `phari` only |
| **`dali_area`** | GYT (Gyelthang) holds 3 there; `LNG → GYT` (vanilla `12_diplomacy.txt:596`) already died with LNG's retirement in item 30 | the Yunnan seam, done |

**DOUBLE-OWNERSHIP CHECK — clean.** All 223 `tibet_region` locations were tested
for membership in more than one country block's `OWN_KEYS` set. **Zero.**
`CONTROL_STRIPS` (`build_setup.py:1679`) needs no Tibetan key.

---

## E. Territory

### E.1 `_TIBET_RULES` — the definitions-resolved grants

Same 5-tuple shape as `_AFRICA_RULES` / `_SEA_RULES` / `_BALTIC_RULES`:
`tag: (sweep names, singles, minus-sweeps, minus-singles, expected)`. **Every
count below was resolved by `build_setup._resolve_ruleset` itself, not
transcribed**, and all five lists were tested pairwise disjoint (zero overlaps).

```python
_TIBET_RULES = {
    # --- Ü (dBus). u_area minus POO's pemako_province, which the sweep
    # never reaches because the four provinces are named explicitly.
    # Lhasa, Yarlung (Nedong, Samye, Densatil), Lhodrak — Marpa's
    # country — and Kongpo. TIB owns all 25 outright.
    "DBU": (["kongpo_province", "lhokha_province", "u_province",
             "yarlung_province"], [], [], [], 25),

    # --- TSANG (gTsang). The whole area plus phari, the Chumbi valley
    # head, which vanilla parks in bengal_region/monyul_area. NOTE
    # `sakya` is in lhato_province, i.e. in TSANG: the monastery is a
    # 1073 foundation but the LOCATION is Tsang's at any date.
    "GTS": (["tsang_area"], ["phari"], [], [], 19),

    # --- GUGE. TIB's Ngari residue: lungkha_province whole, plus the
    # two rutok outliers adjacent to GUG's own gartok and rala.
    "GUG": (["lungkha_province"], ["tsherlung", "ormogang"], [], [], 5),

    # --- NUBHOR. nakchukha_province (Nagchu, Barom, Rongpo) is
    # khampa_culture in the map data and sits beside NBH's own Biru.
    "NBH": (["nakchukha_province"], [], [], [], 3),

    # --- TSONGKHA. xining_province is Qingtang, Gusiluo's seat; the
    # ONLY location list in this package taken from CHI. OPEN DECISION 3.
    "TKA": (["xining_province"], [], [], [], 6),
}
```

**Resolved, with donors and pops:**

| tag | n | donors | `define_pop` | template cultures |
|---|---|---|---|---|
| **DBU** | **25** | TIB 25 | 76 | `utsang_culture` 25 |
| **GTS** | **19** | TIB 19 | 58 | `utsang_culture` 16, `sherpa_culture` 3 |
| **GUG** | **5** | TIB 5 | 13 | `utsang_culture` 5 |
| **NBH** | **3** | TIB 3 | 9 | `khampa_culture` 3 |
| **TKA** | **6** | **CHI 6** | 23 | `liang_culture` 4, `monguor_culture` 2 |
| **total** | **58** | | **179** | |

Notes the resolver forced:

- **`phari` must be an explicit single.** It is in `bengal_region`, not
  `tibet_region`, so no `tsang_area` sweep reaches it — and if it is left
  ungranted, TIB is not landless and the `LANDLESS_AFTER` guard
  (`build_setup.py:6145`) fires.
- **`pemako_province` needs no minus-token.** `u_area` was NOT swept as an area;
  its four TIB provinces are named instead, so POO's three stay POO's without a
  carve-out. (Sweeping `u_area` would resolve 28 and take POO's three — the KAL
  class.)
- **No location in any list is unowned.** Every one of the 58 carries exactly one
  ownership entry, verified with `build_setup`'s own ten-key reader.
  **`UNOWNED_GRANTS` is not used and must not be** — this is the SEA phantom's
  lesson applied prospectively.
- **The three donors are TIB (52) and CHI (6).** Nothing else moves.

### E.2 What each donor keeps

| tag | before | after | verdict |
|---|---|---|---|
| **TIB** | 59 | **0** | **LANDLESS** — claims 131 → **190** (`_landless_claims`, `build_setup.py:5982`, snapshots holdings BEFORE the grants; the union is disjoint, measured) |
| **CHI** | 1,306 | **1,300** | recipient-side seam, OPEN DECISION 3 |
| **DBU / GTS** | 0 | 25 / 19 | new |
| **GUG** | 7 | **12** | recipient |
| **NBH** | 8 | **11** | recipient |
| **TKA** | 0 | 6 | new |

```python
TIBET_LANDLESS = ("TIB",)
```

**ONE retirement, and it is not a side effect** — every one of TIB's 59
locations is granted away or vacated by name, so the emptied-but-unlisted delta
guard (`build_setup.py:6201-6209`) should stay **silent throughout. If it fires,
the design is wrong.**

### E.3 The vacate — seven locations, the smallest in the project

`LOCATION_VACATED` (`build_setup.py:1249`) + `LOCATION_VACATED_EXPECT` (`:1257`)
already exist and are proven (GLH 291, CHG 21, CHI 113, and the six horde
entries). Resolution is snapshot-based — `(members of these names) ∩ (the tag's
holdings at that point)` (`:6071-6090`) — so an already-unowned member cannot
trip the exactly-once assert.

```python
LOCATION_VACATED["TIB"] = ["naktsang_province", "namru_province"]
LOCATION_VACATED_EXPECT["TIB"] = 7
```

**Resolved: exactly 7** — `gonkri namtso_doring ronglung serzhik shantsa
tsedzong zangdan` — carrying **15 `define_pop`**. (`zagya`, the eighth member of
those two provinces, is already unowned and is correctly excluded by the
intersection.)

The Changthang (`byang thang`) is the uninhabited northern plateau: 9 of
`changtang_area`'s 16 ownable locations are **already** unowned in vanilla, all
16 are `changpa_culture`, and the whole area carries 15 pops across 16
locations. Vacating the remaining 7 makes the area **16/16 unowned**, which is
the honest 1066 picture and, arguably, the honest 1337 one.

**Cost: 15 lines of the `jomini_script_system.cpp:252` pop class**
(`docs/EU5-ERROR-DECODER.md:675-685`, one line per pop on vacated settled land).
That is the cheapest vacate the project has costed — Central Asia's was 284
locations, SEA's cheapest alternative was 30 pops.

**Order matters:** the vacate runs AFTER `_landless_claims` (`:6066-6067`), so
the seven are in TIB's claim list, which is correct — Tibet claims the
Changthang.

### E.4 `CAPITAL_FIXES` — none

The orphan-capital guard (`build_setup.py:6566`) fires only for a tag that still
holds land but not its capital. **Every capital in this package was tested
against its own tag's post-grant holding: all pass.** DBU's `lhasa`, GTS's
`shigatse`, TKA's `xining`, GUG's `toling` (retained), NBH's `biru` (retained),
MAR's `shey`, PUR's `purang`, MGG's `dzongkar`, SKK's `yuksom`, LMN's `paro` —
each sits inside its own tag's list or retained holding.

**TIB's `capital = sakya` is exempt** by the guard's `if held and …` condition —
the POR/`guimaraes` precedent. And it is *right*: a landless Tibet whose capital
is Sakya is a Tibet whose recovery starts where vanilla says it started.
**`CAPITAL_FIXES` gains nothing.**

### E.5 What this slice moves, in one line

**58 locations change owner, 7 are vacated, 1 tag is retired landless, 3 new
tags are created, 0 capitals corrected, 0 rulers seated, 0 characters authored,
0 dynasties authored, 0 registry overrides added, 0 named dependency strips, 0
repoints.**

---

## F. Rank, government and naming — worked out to the rendered string

### F.1 The branches that matter

`VAN/in_game/common/customizable_localization/country_name_construction.txt` is
**first-match, 188 lines**, read in full. Which branches can reach a Tibetan
tag?

| line | branch | reaches this theater? |
|---|---|---|
| `:91-97` | `..._prefix_name` — `rank_empire` **AND** `court_language` in `chinese_language_family` | **no.** No Tibetan tag declares a `court_language` (measured across both `10_countries.txt` files) and none holds `rank_empire` |
| `:99-104` | `..._prefix_name_horde` — `government_type = steppe_horde` | **no.** No Tibetan template resolves to `steppe_horde` (`east_asia_monarchy_no_coast` is `monarchy`, `asia_advanced_no_pagan_tribe` is `tribe`) — `_bad_recip` (`build_setup.py:5922`) needs no Tibetan key |
| `:116-157` | `..._prefix_adjective_rank` — `rank_empire` (or `country_type = pop`, or `japanese_clan`, or `military_order_reform`…) | **only for MSH/TAN/MNP**, the three `type = pop` countries, which render from their ADJ keys |
| `:159-164` | `..._sultanate` — `religion.group = religion_group:muslim` | **no** |
| **`:183-186`** | **`..._prefix_rank_of_name`, `fallback = yes`** | **EVERYBODY ELSE IN THE THEATER** |

Loc (`VAN/main_menu/localization/english/government_names_l_english.yml`):
`country_name_construction_prefix_rank_of_name: "$PREFIX$ $RANK$ of $ARTICLE$
$NAME$"` (`:11`) and **`…_map: "$NAME$"` (`:12`)**.

**THE LAW, for this theater: every Tibetan country's map label is its NAME key
verbatim.** So the map prints "Guge", "Maryul", "Purang", "Derge", "Amdo", "Ü",
"Tsang", "Tsongkha". There is no adjective trap, no horde trap, no sultanate
trap and no tag-gated trap anywhere on the plateau. **This is the simplest
naming situation the project has met.**

### F.2 The rank word — one live wrongness, and it belongs to TIB

`country_ranks.txt` is **first-match, 2,742 lines**. First-match order at each
rank, walked for the branches a Tibetan tag can reach:

- **empire**: `:285 rank_empire_theocracy_dharmic` → `:295 rank_empire_theocracy`
  → `:324 rank_empire_tribe` → … → **`:624 rank_empire` (default)**.
- **kingdom**: `:897 rank_kingdom_bishopric` → **`:907 rank_kingdom_theocracy_dharmic`**
  → **`:917 rank_kingdom_theocracy`** → `:944 rank_kingdom_tribe` → … →
  **`:1251 rank_kingdom` (default)**.
- **duchy**: `:1524 rank_duchy_theocracy_dharmic` → `:1534 rank_duchy_theocracy`
  → `:1605 rank_duchy_tribe` → … → **`:2005 rank_duchy` (default)**.
- **county**: `:2212 rank_county_theocracy_dharmic` → `:2222 rank_county_theocracy`
  → `:2278 rank_county_tribe` → … → **`:2552 rank_county` (default)**.

The dharmic branches **never fire here**: `tibetan_buddhism` and `bon` are both
`group = buddhist` (`VAN/in_game/common/religions/buddhist.txt:110-112` and
`:1-3`), and `religion_groups/00_default.txt` lists `buddhist` (`:10`) and
`dharmic` (`:29`) as separate groups.

| what fires | loc | renders |
|---|---|---|
| `rank_kingdom_theocracy` (TIB today) | `government_names_l_english.yml:503-507` | RANK "Theocracy", PREFIX "Grand", ruler **"Grand Priest"** |
| `rank_kingdom` (a monarchy at kingdom rank) | `:292-295` | "Kingdom" / **"King"** |
| `rank_duchy` | `:641` | "Duchy" / "Duke" |
| `rank_duchy_tribe` (the Kham tribe tags, if the engine derives duchy) | `:790-792` | "Tribe" / **"Chief"** |
| `rank_county_tribe` | `:1018-1022` | "Tribe", prefix "Minor" / **"Chieftain"** |
| `rank_kingdom_tribe` | `:482-485` | "Tribal Kingdom" / "King" |

**No Tibetan rank word exists anywhere in the game.** There is no
`rank_*_tibetan`, no `rank_*_lama`, no "Gyalpo", no "Depa", no "Desi". A
Tibetan king renders "King", a Tibetan chief renders "Chief". That is a loss of
flavour and it is *cheap to fix later* (a `country_ranks.txt` whole-file
override with a `culture_group:tibetan_group` branch inserted above the
generics, the MAM-branch precedent from `HANDOFF.md:1035-1038`) — **banked, not
proposed.**

### F.3 What each tag renders as, under the recommended design

| tag | religion | gov | rank | branch chain | full name | **map label** | ruler title |
|---|---|---|---|---|---|---|---|
| **DBU** | tibetan_buddhism | monarchy | **none declared** | `:183` fallback → size-derived | "…of Ü" | **Ü** | King/Duke/Count |
| **GTS** | tibetan_buddhism | monarchy | **none declared** | `:183` fallback → size-derived | "…of Tsang" | **Tsang** | King/Duke/Count |
| **TKA** | tibetan_buddhism | monarchy | **none declared** | `:183` fallback → size-derived | "…of Tsongkha" | **Tsongkha** | King/Duke/Count |
| **GUG** | tibetan_buddhism | monarchy | none (vanilla) | same | "…of Guge" | **Guge** | ditto |
| **MAR** | tibetan_buddhism | monarchy | none (vanilla) | same | "…of Maryul" | **Maryul** | ditto |
| the eleven Kham tags | tibetan_buddhism / bon | **tribe** (`asia_advanced_no_pagan_tribe`) or monarchy | none | `:183` fallback → `:1605`/`:2278` if tribe | "Tribe of Derge" | **Derge** | **Chief / Chieftain** |
| **TIB** *(landless)* | tibetan_buddhism | theocracy | `rank_kingdom` | `:183` fallback → **`:917`** | **"Grand Theocracy of Tibet"** | **Tibet** | **"Grand Priest"** — *invisible once landless* |
| MSH / TAN / MNP | — | **pop** | — | **`:116` adjective** | "$ADJ$ $RANK$" | from the ADJ key | — |

**A tag that declares no `country_rank` gets an engine-derived rank, and no file
in this repo settles the thresholds.** `VAN/in_game/common/country_ranks/00_default.txt`
carries `level`, modifiers and an `allow` block calling
`can_upgrade_country_rank`, but no size rule. **Twenty-one of the theater's 22
landed tags already declare no rank**, so the three new blocks matching them is
the local convention — but every "size-derived" cell above is a prediction about
engine code, not about data. Inherited unresolved from `SEA-PACKAGE.md`'s owed
list; **OWED CHECK 1**.

### F.4 Formables — one consumed in the good sense, none opened

`VAN/in_game/common/formable_countries/00_formable_countries.txt`, 150
formables carrying a `tag =`. **Exactly one touches this theater.**

| formable | line | tag | frac | scope | potential | reachable at start? |
|---|---|---|---|---|---|---|
| **TIB_f** | **`:3101`** | TIB | **0.6** | `regions = { tibet_region }` = 223 ownable → **134** | `culture = { has_culture_group = culture_group:tibetan_group }` | **NO** — the largest Tibetan-culture holding after this slice is DBU at 25. **The path opens for a conqueror, which is the design** |

No other formable names a Tibetan tag, region, area or culture group (the whole
file was scanned for `tibet|utsang|ladakh|khampa|amdowa|TIB|MAR|GUG`).

`VAN/in_game/common/advances/country_TIB.txt` (80 lines, **7 nodes**, every one
gated `potential = { has_or_had_tag = TIB }`, the first literally named
**`sakya_hegemony`**) becomes orphaned-but-not-broken: a landless shell still
satisfies its own `has_or_had_tag`, and nobody else can reach the tree — the
taifa precedent. **No vanilla event anywhere gates on TIB** (grep over
`VAN/in_game/events/`: zero files). The only other engine reference to the
region is `situations/little_ice_age.txt:45`
(`region:tibet_region = { every_area_in_region = { add_extended_winter = this } }`),
which is geography and is unaffected.

---

## G. Diplomacy

`MOD/main_menu/setup/start/12_diplomacy.txt` today: **299 `dependency` lines, 28
`scripted_mutual`/`scripted_oneway` lines** (measured; vanilla has 652 and 41).

**Exactly 33 lines name a tag with a `tibetan_buddhism` or `bon` registry
religion.** Every one is enumerated below.

### G.1 The fifteen lines the generic landless sweep kills for FREE

`_drop_landless_dep` (`build_setup.py:7494-7504`) removes a line if **either**
side is in `LANDLESS_AFTER`. Retiring TIB alone kills the entire Sakya web:

```
:253 dependency = { first = CHI second = TIB subject_type = vassal }   -> TIB landless
:396 dependency = { first = TIB second = GUG subject_type = vassal }
:397 dependency = { first = TIB second = PUR subject_type = vassal }
:398 dependency = { first = TIB second = MGG subject_type = vassal }
:399 dependency = { first = TIB second = POO subject_type = vassal }
:400 dependency = { first = TIB second = LGT subject_type = vassal }
:401 dependency = { first = TIB second = DRG subject_type = vassal }
:402 dependency = { first = TIB second = NCN subject_type = vassal }
:403 dependency = { first = TIB second = GNJ subject_type = vassal }
:404 dependency = { first = TIB second = BTG subject_type = vassal }
:405 dependency = { first = TIB second = NBH subject_type = vassal }
:406 dependency = { first = TIB second = LTN subject_type = vassal }
:407 dependency = { first = TIB second = LMN subject_type = vassal }
:408 dependency = { first = TIB second = MAR subject_type = vassal }
:409 dependency = { first = TIB second = ZNK subject_type = vassal }
```

**Counted against the VANILLA source the build reads every run
(`build_setup.py:6376`, `src = open(os.path.join(VAN, rel), …)`): exactly 15
lines name TIB** (`VAN/12_diplomacy.txt:536` and `:752-765`).

**`n_landless_deps` 265 → 280** (`build_setup.py:7577`). **Observe it failing
first**, per CLAUDE.md.

This is the cheapest diplomacy correction in the project's history: fourteen
vassalages and one overlordship dissolved by adding three characters to a tuple.

### G.2 Repoints — NONE

There is no surviving two-landed-tags relation to repoint. Every TIB tie has TIB
on one side. The Jurchen/jimi/Sahel repoint shape
(`build_setup.py:7320-7391`) is not needed.

### G.3 Named strips — NONE required, four PROPOSED

Nothing must be stripped by name. **OPEN DECISION 6** proposes four, and they
are the only optional diplomacy in the package:

```
:270 dependency = { first = CHI second = HOR subject_type = tusi }
:271 dependency = { first = CHI second = NYA subject_type = tusi }
:273 dependency = { first = CHI second = GOL subject_type = tusi }
:274 dependency = { first = CHI second = AMD subject_type = tusi }
```

Golog, Amdo, Hor (the Horpa of Kandze) and Nyarong are **deep-plateau** tags,
not frontier ones — the Song's writ never reached the Yellow River sources or
the Nyag valley in 1066 [U]. The other fourteen CHI ties in the theater sit on
the Gansu-Sichuan rim (`:242 :243 :245 :250 :252 :258-264 :272 :275`), where the
Song *jimi* prefecture system is the real 1066 institution — the reading item
30's jimi fix already adopted (`build_setup.py:7346-7354`). Named-strip shape:
the KBO→Hausa batch (`:7413-7422`), `assert n_tibet_tusi == 4`.

### G.4 New ties — NONE

**This package proposes no tributary, vassal or pact line of any kind.** The
1066 plateau had no overlord; giving one to DBU, GTS or TKA would be inventing
the very thing the slice removes.

**One variant was costed and refused.** `TKA → AMD` and `TKA → GOL` as
`subject_type = tributary` would pass the visible gate **for free** — both AMD
and GOL ride `asia_advanced_no_pagan_tribe`, whose `type = tribe`
(`VAN/main_menu/setup/templates/asia_advanced_no_pagan_tribe.txt`) satisfies the
SUBJECT-tribe branch of `tributary.txt:19-24`, the Irish law
(`KNOWLEDGE.md`, "The tributary gate's THIRD branch is free"). **The mechanism
is free; the history is not.** Gusiluo's authority over the Golog and the
Kokonor tribes is asserted by no source this agent can cite [U]. Refused, and
recorded so it is not re-derived. Under it, `PLB`-style, `"TKA"` would have to
join `_MOD_TRIB_OVERLORDS` (`verify_mod.py:767`) and `:843`'s `min_count` would
rise 78 → 80.

**`n_pacts` stays at 9** (`build_setup.py:7607`) — measured: **zero
`scripted_mutual`/`scripted_oneway` lines name any theater tag.**

### G.5 Left alone

```
:242 CHI->HEZ (vassal)   :243 CHI->JIZ   :245 CHI->MNZ   :250 CHI->SNP
:252 CHI->TAZ            -- the Gansu/longyou frontier; the Song jimi reading
:258 CHI->TNQ (tusi)     :259 CHI->MCI   :260 CHI->WMO   :261 CHI->TSK
:262 CHI->LGZ            :263 CHI->KHG   :264 CHI->BIR   -- the Sichuan rim
:272 CHI->GYE (tusi)     :275 CHI->CKL   -- Gyelrong and Minyag, frontier
:294 BZH->YNG (tusi)     -- Muli under Beisheng, the Yunnan seam
```

### G.6 International organizations — one ghost, no drain

Every `members`/`free_city`/`elector`/… list in
`MOD/main_menu/setup/start/15_international_organizations.txt` was scanned for
the retiree.

| retiree | IO | line | list size before |
|---|---|---|---|
| **TIB** | **Middle Kingdom** | **`:164`** | **199 → 198** |

**TIB appears in exactly ONE list and nowhere else** — it is in **no sect**,
because the Sakya instance it belonged to was already removed by the future-date
strip (§0.2). `build_ios`'s generic sweep (`build_setup.py:6804-6825`, exit at
`:6893`) removes it. **`n_ghosts` 155 → 156**, and `_expected_ghosts`
(`:6852-6892`) gains `["TIB"]`.

**No IO is drained, and no member-add is needed.** The pinned empty-members
count stays at **9** (`verify_mod.py:910`).

**The sect landscape after this slice — measured, and worth the main session's
eye.** Of the 35 landed tags whose registry religion is `tibetan_buddhism` or
`bon`, **28 are in no sect at all**: AMD BIR BTG CHI CKL GNJ GOL GUG GYE GYT HEZ
HOR JIZ KHG KTU LGT LTN MCI MGG MNZ NBH NYA POO SNP TAZ TIB TNQ TSK. Only DRG
(Nyingma), KHS/PUR/MAR (Kadam) and ZNK/NCN/LMN/SKK/LHL (Kagyu) sit in one. **This
is a pre-existing consequence of items already landed** — vanilla had 14 of them
in the Sakya instance and 9 in Jonang, both correctly stripped as post-1066 —
and it is recorded here rather than fixed, because `tibetan_buddhism` carries
`max_sects = 1` (`buddhist.txt:115`) and whether a sect-less country of a
sect-bearing religion produces any log line at all is **unmeasured (OWED CHECK 3)**.

**If a member-add is wanted anyway**, the grounded one is **DBU → the Kadam
sect (`:1052`)**: Atiśa died at Nyethang and Dromtön founded Reting in 1057,
both in Ü [D], and the sect's own `creation_date = 1030.1.1` is inside the
Kadam period. GTS has no equally clean home (Shalu, 1040, is Tsang's but the
sect lists do not model it). **OPEN DECISION 9**; the mechanism is the
Shaiva-powers precedent (`build_setup.py:7043-7066`), exact-instance asserted.

---

## H. Left alone deliberately

| what | measurement | why |
|---|---|---|
| **Kham's eleven tags** — 71 of `kham_area`'s 75 locations | 326 `define_pop` | §D.3, OPEN DECISION 8. The patchwork model is 1066-correct even though the individual state names are late [all D]. **DRG is the Nyingma sect's only member** — retiring it drains an IO |
| **Amdo's four** AMD GOL NCN LGT — 40 locations | 149 `define_pop` | Same. Tribal Amdo is right at any date; only the CHI *tusi* ties are arguable (OPEN DECISION 6) |
| **The 24 already-unowned locations** — `changtang_province` 8, `gyahor_province` 7, `tsaidam_province` 8, `zagya` | **10 `define_pop` total** | Vanilla's own stateless model for the Changthang, the Yellow River sources and the Tsaidam salt flats. Correct for 1066 and for 1337; the Pecheneg discipline. This package *adds* seven to the set and touches none of the existing 24 |
| **`longyou_area`'s seven Sino-Tibetan frontier tags** (MNZ KHG TAZ HEZ BIR JIZ + SNP) | 25 locations; `hezhou_province` is `sarta`/`salar` **sunni** 2 | The Song-frontier seam, not the plateau. `NORTHERN-DYNASTIES-PACKAGE.md:1037` sent them here; on measurement they belong with a Gansu/Hehuang pass that also owns the *jimi* question |
| **The Himalayan rim** — KHS 18, KTU 6, LHL 2, plus `nepal_area` and `upper_indus_area` | — | `INDIA-TIER1-PACKAGE.md:986-987` left both explicitly, item 34 touched neither |
| **PUR's `religion_definition = hindu`** | `MOD/east_asia.txt:2200`; all four `purang_province` locations are `tibetan_buddhism` | One token in an already-overridden file. OPEN DECISION 7 — held out of the recommended package only because it is a registry claim about a tag this slice does not otherwise touch |
| **A Tibetan `country_ranks.txt` branch** ("Gyalpo"/"Depa") | zero such branch exists in 2,742 lines | Banked. A whole-file override inserting a `culture_group:tibetan_group` branch above the generics is the MAM precedent (`HANDOFF.md:1035-1038`); it is a styling pass, not a 1066 pass |
| **`06_pops.txt` and `07_cities_and_buildings.txt`** | vanilla's, un-overridden | The plateau's pop data is **already 1066-correct** — `tibetan_buddhism` on 213 of 223, culture matching the tag set. The one inherited correction is TKA's `xining_province` (§A.3). Note `KNOWLEDGE.md`'s "`tag = X … location = L` where X does not own L is FIRST-CLASS vanilla" — do **not** "fix" `07_cities` after these grants |
| **The Second Diffusion as a situation** | Atiśa 1042-1054, Reting 1057, **Sakya 1073**, Sangphu 1073, the Kadam/Kagyu/Sakya school formation [all D] — and vanilla ships the two 1066-live sects plus the two future ones with **dated instances ready to be re-added** | **The strongest banked situation material this theater offers.** A "Second Diffusion" situation could re-create the Sakya (1073) and Jonang (1120) IO instances on schedule, which is script the mod already knows how to write. Situation backlog, not setup data |

---

## I. Mechanism — every tool already exists, and one is used for the first time on a settled plateau

**This package needs no new build step and no new harness capability.**

| need | existing mechanism | `file:line` |
|---|---|---|
| grants resolved from `definitions.txt` | `_resolve_ruleset` + the per-slice loop | `:799`, model at `:5843-5854` (SEA) |
| retire with auto-derived claims | `LANDLESS_AFTER` + `_landless_claims` | `:2862`, `:5982` |
| catch side-effect retirements | the emptied-but-unlisted delta guard | `:6201-6209` |
| prove the retiree really emptied | the `LANDLESS_AFTER … still owns` guard | `:6145` |
| prove the retiree carries claims | the claims-backed landless guard | `:6147-6160` |
| **remove land and give it to nobody** | **`LOCATION_VACATED` + `LOCATION_VACATED_EXPECT`** — snapshot-resolved, disjointness-asserted against the grant lists | `:1249`, `:1257`, `:6064-6095` |
| exactly-one-owner on every grant | `_remove_owned_many` | `:5612-5621` |
| grant-list disjointness | `_list_owner` | `:5934-5937` |
| new country blocks | `NEW_COUNTRIES` | `:486` |
| capital discovery | `_assert_new_block_discovery` | `:5488`, exit `:5517` |
| dependency dissolution | `_drop_landless_dep` — **the whole diplomacy correction rides this** | `:7494-7504`, assert `:7577` |
| IO member strip | `build_ios`'s generic `LANDLESS_AFTER` sweep | `:6804-6825`, assert `:6893` |
| named dependency strips (OPEN 6 only) | the KBO→Hausa shape | `:7413-7422` |
| IO member ADD (OPEN 9 only) | the Shaiva-powers precedent | `:7043-7066` |
| steppe-horde recipient guard | `_bad_recip` — **no Tibetan template resolves to `steppe_horde`** (measured) | `:5922-5924` |
| double-ownership | `CONTROL_STRIPS` — **no Tibetan key needed** | `:1679` |
| **`UNOWNED_GRANTS`** | **NOT USED, and must not be** — every one of the 58 granted locations was measured at exactly ONE ownership entry with the ten-key reader | `:1893` |

Five asserts that will fire if the design is wrong, and should be watched:

1. **`_remove_owned_many != 1`** (`:5612-5617`) — fires if a granted location
   has two ownership entries or **zero**. All 58 were measured at exactly one.
2. **`_list_owner` disjointness** (`:5934-5937`) — the five rule-sets were
   tested pairwise disjoint by the resolver (zero overlaps), and the vacate list
   is disjoint from every grant list (`:6086-6089` asserts this separately).
3. **`LOCATION_VACATED[TIB]` resolved-count** (`:6081-6084`) — must be **7**. If
   a patch changes `changtang_area`, this dies loudly.
4. **the emptied-but-unlisted delta guard** (`:6201-6209`) — must stay
   **silent**. TIB is the only retirement and it is deliberate; **if the guard
   fires, a sweep took more than the design intends.**
5. **`_assert_new_block_discovery`** (`:5488`) — `expl_china` carries both
   `tibet_region` and `west_china_region`, so `lhasa`, `shigatse` and `xining`
   all pass.

**The one thing worth saying about the harness: it needs no new check.** Every
class this package touches is already guarded — landless holdings, landless
claims, IO ghosts, empty IO members, one-ruler-per-block, the
identity↔start-block bijection, CoA coverage, parliament reach. That is what
thirty-seven slices of check-building buys.

---

## OPEN DECISIONS

**1. Ü-Tsang — two new tags, one, or none?**
TIB's 43 central locations (`u_area` 25 + `tsang_area` 18, 131 `define_pop`)
must go somewhere. Three shapes were costed:
**(a) TWO new tags, DBU "Ü" 25 and GTS "Tsang" 19 (with `phari`)** — 2 registry
blocks, 2 CoA entries, 4 loc rows, 2 colours, 0 rulers, 0 vacate.
**(b) ONE new tag** over all 43 — half the cost, but it puts a unified central
Tibet on the map, which is TIB again wearing a different name.
**(c) VACATE all 43** — zero new tags, and the historically closest reading (no
state existed), at the price of **131 pop-class error lines** and a blank Lhasa
on a map where every neighbour is painted.
**Recommendation: (a), TWO.** It says exactly what the sources say — Ü and
Tsang were distinct and neither was unified — and it uses vanilla's own naming
grammar, in which Tibetan tags are *regions and peoples* (AMD "Amdo", GOL
"Golog", GYE "Gyelrong", HOR "Hor"), not dynasties. **Counter:** two tags with
no rulers, no dynasties and invented statehood are still two inventions, and (c)
is the only option that asserts nothing at all; the project's own Pecheneg and
Philippines precedents both chose emptiness over a plausible-looking tag, and
131 pop lines is a real but affordable price on the emptiest settled ground the
project has met.

**2. TIB — retire landless, or reshape in place?**
**(a) RETIRE landless with claims** (recommended): 190 claims, `TIB_f` becomes
the reunification path, the entire 15-line Sakya web dies free, the "Grand
Priest" render disappears, and the tag keeps its arms, colour, registry entry
and advance tree.
**(b) RESHAPE in place**: keep TIB landed on Ü+Tsang, `CAPITAL_FIXES` `sakya` →
`lhasa`, and `FIELD_FIXES` the government from `theocracy` /
`theocratic_elective` to `monarchy` / something legal — the NOV precedent
(`build_setup.py:2989`ff). Cost: **zero new tags**, one capital fix, one field
fix, and the fourteen vassal lines then need a **named strip** because TIB stays
landed (the LIT→POK class).
**Recommendation: (a).** The NOV precedent applies when the polity existed and
only its constitution was dated; Novgorod was there in 1066, "Tibet" was not.
TIB is the MAJ/SUK class — a post-1066 object — and the project retires those.
**Counter:** (b) is dramatically cheaper (0 registry blocks, 0 colours, 0 loc
rows, 0 CoA decisions), it keeps a playable central-Tibetan power for a human
player, and it avoids the "Ü"-on-the-map legibility question entirely. If the
main session wants the smallest possible Tibet slice, (b) plus §G.1's fourteen
lines as a named strip is a two-hour change.

**3. Tsongkha (TKA) — create it, taking six locations from CHI?**
`xining_province` (6 locations, 23 `define_pop`) is Qingtang, Gusiluo's seat and
the Song's ally against Xia; the Song did not take the Huangshui until 1104 [U].
`NORTHERN-DYNASTIES-PACKAGE.md:1035` excluded it from XIA **specifically for
this pass**. But it is CHI's ground, CHI is a done-slice seam, and the location
data is `liang_culture`/`monguor_culture` + `sanjiao`/`mahayana` — painted for
the post-conquest valley.
**Recommendation: YES, six locations, flagged for explicit sign-off** — the SEA
`KHM +24` precedent, where a seam touch was made once, measured and signed off
rather than smuggled. It is the only named 1066 polity in the theater and
leaving it as six Chinese locations is a visible error on any map of the period.
**Counter:** it is the package's only CHI touch, its only culture/religion
mismatch, and its only tag with an argument for a ruler that the package then
refuses to seat — three separate risks bought for six locations. Deferring TKA
to a Gansu/Hehuang pass that also owns the *jimi* question (OPEN 6) would keep
this slice entirely inside `tibet_region`.

**4. Tsongkha's ruler — Dongzhan, or nobody?**
Gusiluo died in 1065 and his son Dongzhan (董氈) ruled 1065-1086 [D] — the only
1066 ruler in or near the theater whose accession is dated to the year and
falls *inside* the game's window. Cost: one `NEW_CHARACTERS` block, one invented
`name_dongzhan` key + one loc row (24 such rows already ship,
`1066_norman_conquest_l_english.yml:116-259`), one new dynasty key + loc row.
Thrones 178 → 179.
**Recommendation: NOBODY.** "Dongzhan" is a Chinese transcription whose Tibetan
original is unsettled [D]; seating it writes a Chinese exonym onto a Tibetan
king, which is a different error from leaving the throne random. **Counter:** he
is the one man in this entire theater whose reign covers 1066.9.15 by agreement
of the sources, the mechanism is fully attested in this repo, and a click tour
with one named Tibetan king is worth more to the user than a plateau of
`random`.

**5. `DBU`'s displayed name — `"Ü"`, or something longer?**
`DBU: "Ü"` is the standard English name of the province and matches vanilla's
own diacritic practice ("Mangyül Gungthang", "Yǒngníng"). But a
single-character map label may read as a rendering fault, and the
`_ADJ` key ("Ü") appears in tooltips.
**Recommendation: `"Ü"`.** It is what the place is called. **Counter:**
`"Ü-Tsang"` is wrong (that is both provinces), `"Lhasa"` names the seat rather
than the region but is unambiguous and is how vanilla handles Kathmandu (KTU),
and `"Uru"` (dbU ru, the imperial "Centre Horn") is a real 11th-century
administrative name that reads as a word. If the user's click tour cannot find
"Ü" on the map, that is the answer.

**6. The four deep-plateau CHI *tusi* ties — strip, or leave to the China review?**
`:270 CHI→HOR`, `:271 CHI→NYA`, `:273 CHI→GOL`, `:274 CHI→AMD` put the Song in
authority over the Nyag valley, Kandze, the Golog and Amdo. The other fourteen
CHI ties in the theater are on the Gansu-Sichuan rim, where the *jimi* reading
item 30 adopted actually holds.
**Recommendation: STRIP THE FOUR by name** (`assert n_tibet_tusi == 4`). It is
four lines, it costs nothing, and leaving them means the 1066 map shows Song
Amdo — which is the same class of error as Yuan Tibet, one province east.
**Counter:** the *tusi* web is the China review's declared property
(`INDIA-CHINA-REVIEW.md:453`, "The 126 *tusi* web as *1066* frontier
prefectures"), the line between "frontier" and "deep plateau" is drawn by this
agent and by nobody else, and stripping a `tusi` tie has a knock-on into
`can_country_have_tusi`'s subject branch that item 30 already had to repair once
(`build_setup.py:7346-7354`).

**7. PUR's `religion_definition = hindu` — fix it?**
`MOD/in_game/setup/countries/east_asia.txt:2200` gives Purang `hindu`, while all
four `purang_province` locations are `tibetan_buddhism` and vanilla's own Kadam
sect lists PUR with the comment "#Purang capital, Tholing Monastery, is Kadam".
The file is **already a mod override**, so the fix is one token and adds no new
override.
**Recommendation: FIX IT** to `tibetan_buddhism`, in the same commit, with the
comment naming vanilla's own contradiction. **Counter:** it is outside this
slice's declared scope, the registry religion of a landed tag has measurable
effects (`KNOWLEDGE.md`, "The registry's `culture_definition` IS a landed tag's
primary culture"), and a two-location Purang under a Hindu king may be a
deliberate Paradox nod to the Khasa-Malla Hindu influence in Purang [D] rather
than an error. The safe version is to bank it for the pop phase.

**8. Kham and Amdo's fifteen late-named tags — leave them?**
Derge (15th-16th c.), Batang, Litang, Lingtsang, Nangchen, Gonjo, Nubhor, Hor,
Nyarong, Powo, Minyag, Gyelrong, Golog, Amdo — 111 locations, 475 `define_pop`,
almost every one a chiefdom whose recorded history starts after 1200 [all D].
**Recommendation: LEAVE ALL FIFTEEN.** The *model* — a dozen unaligned valley
lordships with no overlord — is exactly 1066 eastern Tibet, and the alternative
is 111 vacated locations or fifteen inventions. This is the Shan decision and
the Philippines decision. **Counter:** the project's own standard is "a region
is not done because it has borders, it is done when the people on the throne are
the people who were there", and fifteen tags whose king-lists begin in the 13th
century is precisely what it retires elsewhere. If the standard binds, this
theater is not done — and saying so now is cheaper than discovering it later.

**9. Do DBU/GTS/TKA join a sect?**
28 of the 35 landed Tibetan-Buddhist tags are already sect-less (a measured
consequence of the correct Sakya/Jonang strip), so joining none matches the
majority. The grounded add is **DBU → Kadam (`:1052`)** — Atiśa died at Nyethang
and Reting was founded in 1057, both in Ü [D].
**Recommendation: NO ADDS**, matching the theater's 28. **Counter:** the Kadam
sect currently holds three western tags (KHS PUR MAR) and none in Ü, which is
where Kadam actually began; one member-add would put the school in its own
homeland for the price of one exact-instance assert. Either way **OWED CHECK 3
must be answered first**: nobody has measured whether a sect-less country of a
`max_sects = 1` religion logs anything.

---

## Implementation checklist

Ordered so each step can be verified before the next.

1. **Registry additions FIRST and alone** — `DBU`, `GTS`, `TKA` appended to
   `MOD/in_game/setup/countries/zz_1066_new_countries.txt`. Count **71 → 74**
   (`verify_mod.py:1115`, `min_count = 2411` → 2414). **No new registry
   override** — `east_asia.txt` stays at its one intended deviation (two under
   OPEN DECISION 7).
2. **Colours** — `DBU` `map_TIB` (`02_map.txt:2596`, freed by TIB's retirement);
   `map_GTS` and `map_TKA` as NEW rows in
   `MOD/main_menu/common/named_colors/zz_1066_map_colors.txt`. **Re-run the
   key-name absence scan before writing either** — the AUDIT-D3 lesson — and
   never write `map_tibetan` (it is `tibetan_language`'s own key,
   `00_tibet.txt:3`).
3. **Localisation** — 6 rows, one physical line each, UTF-8 **with** BOM.
   `verify_mod.py:167` and `:174` rise 367 → 373.
4. **`_GENERATOR_OK`** — add `DBU`, `GTS`, `TKA` at `tools/verify_mod.py:1003`
   with a tier-4 comment; `:1055-1061` fails otherwise and `:1082` rises
   122 → 125.
5. **`NEW_COUNTRIES`** — the three blocks of §B.1. **Re-read
   `east_asia_monarchy_no_coast.txt` in full before shipping** and restate
   anything it omits (§I's house rule).
6. **`_TIBET_RULES` + resolution loop** — modelled on the SEA loop
   (`build_setup.py:5843-5854`): resolve, assert the exact count per tag, EXTEND
   `LOCATION_GRANTS` (never assign — GUG and NBH are landed recipients), then
   assert each capital is in its own resolved list. **`phari` is an explicit
   single and is in `bengal_region`, not `tibet_region`** — a `tsang_area` sweep
   alone leaves TIB holding one location and the landless guard fires.
7. **`LOCATION_VACATED["TIB"]` = `["naktsang_province", "namru_province"]`,
   `LOCATION_VACATED_EXPECT["TIB"] = 7`.** **Observe the resolved count**: the
   two provinces contain 8 ownable, one of which (`zagya`) is already unowned
   and is excluded by the snapshot intersection. If it resolves 8, the
   intersection is not doing its job.
8. **`TIBET_LANDLESS = ("TIB",)` into `LANDLESS_AFTER`** (`:2862`). The delta
   guard should stay silent. TIB's claims go 131 → **190**; verify the union is
   190 and not 131+59−(overlap) — the overlap was measured at **zero**.
9. **`n_landless_deps` 265 → 280** (`:7577`) — **observe it failing first**, per
   CLAUDE.md. `n_pacts` stays **9** (`:7607`): measured, no theater pact exists.
10. **IOs** — `n_ghosts` **155 → 156** with `["TIB"]` added to `_expected_ghosts`
    (`:6852-6892`). **No member-add and no member-drain**; the pinned
    empty-members count stays **9** (`verify_mod.py:910`).
11. **Optional, per decisions** — OPEN 3's TKA (already in step 6's rule set;
    drop the `"TKA"` key to defer), OPEN 4's Dongzhan (`HISTORICAL_RULERS` +
    `NEW_CHARACTERS` + name-key loc row; thrones 178 → 179, `verify_mod.py:288`
    356 → 358, `:413` 178 → 179, `:376` 641 → 645, `:429` 138 → 139), OPEN 6's
    four named `tusi` strips (`assert n_tibet_tusi == 4`), OPEN 7's PUR token,
    OPEN 9's Kadam member-add.
12. **Harness** — `:938` (one-ruler) and `:1115` (bijection) rise by 3:
    **2408 → 2411** and **2411 → 2414**. `:1240`'s parliament `min_count = 1364`
    moves: 1 landless against 3 new landed, all three reaching
    `parliament_type = council` through `east_asia_monarchy_no_coast` →
    **expect 1366**, but **verify, do not assume**.

**Break-tests owed** (a check never seen failing is untested):

(a) a bogus location in `_TIBET_RULES` must abort;
(b) an off-by-one `expected` must abort with the resolved count printed;
(c) **drop `phari` from GTS's singles and watch the `LANDLESS_AFTER … still
owns` guard (`:6145`) fire on TIB** — this package's only near-miss;
(d) `n_landless_deps` left at 265 must abort with 280 printed;
(e) **set `LOCATION_VACATED_EXPECT["TIB"] = 8` and watch `:6081-6084` abort with
7** — proving the snapshot intersection excludes the already-unowned `zagya`;
(f) **put one vacated location into a grant list and watch `:6086-6089` fire**
("vacate and grant lists must be disjoint");
(g) point `LOCATION_GRANTS["GUG"]` at a location `DBU` also claims and watch
`_list_owner` (`:5934-5937`) fire;
(h) **omit `["TIB"]` from `_expected_ghosts` and watch `:6893` abort at 156**;
(i) **sweep `u_area` instead of its four provinces and watch the delta guard
(`:6201`) fire on POO** — the KAL carve-out class, reproduced deliberately.

## Expected constant moves, collected

| constant | `file:line` | from | to (recommended) | to (all decisions maximal) |
|---|---|---|---|---|
| registry blocks | `zz_1066_new_countries.txt` | **71** | **74** | 74 |
| registry overrides | `MOD/in_game/setup/countries/` | 5 files | **5 — unchanged** | 5 (OPEN 7 edits an existing one) |
| `NEW_COUNTRIES` count | `build_setup.py:486` | current | **+3** | +3 (−1 if OPEN 3 defers TKA) |
| `LANDLESS_AFTER` | `:2862` | current | **+1** (TIB) | +1 |
| `n_landless_deps` | `:7577` | **265** | **280** | 280 |
| `n_pacts` | `:7607` | **9** | **9 — unchanged, measured** | 9 |
| repoints (new batch) | — | — | **0** | 0 |
| named dependency strips | new, `:7413` shape | — | **0** | **4** (OPEN 6) |
| new tributary pairs | — | — | **0** | 2 (the refused `TKA→AMD/GOL` variant) |
| `_MOD_TRIB_OVERLORDS` | `verify_mod.py:767` | 9 tags | **9 — unchanged** | 10 (+TKA) |
| tributary-gate `min_count` | `verify_mod.py:843` | **78** | **78 — unchanged** | 80 |
| `CAPITAL_FIXES` | `:2916` | current | **+0** | +1 (TIB `sakya`→`lhasa`, OPEN 2b only) |
| `FIELD_FIXES` | `:2989` | current | **+0** | +1 (TIB government, OPEN 2b only) |
| `UNOWNED_GRANTS` | `:1893` | 3 tags / 19 locations | **unchanged — none needed** | unchanged |
| `CONTROL_STRIPS` | `:1679` | 1 tag | **unchanged** | unchanged |
| `LOCATION_VACATED` | `:1249` | 8 tags | **9 (+TIB)** | 9 |
| `LOCATION_VACATED_EXPECT` | `:1257` | — | **+`{"TIB": 7}`** | +`{"TIB": 7}` |
| locations granted | build report | current | **+58** | +52 (if TKA defers) |
| locations vacated | build report | current | **+7** | +7 (+43 under OPEN 1c) |
| unowned locations | — | current | **+7** | +7 |
| IO ghosts | `:6893` | **155** | **156** | 156 |
| IO members added | — | — | **none** | DBU → Kadam `:1052` (OPEN 9) |
| country blocks | `verify_mod.py:938`, `:1115` | **2408 / 2411** | **2411 / 2414** | 2411 / 2414 |
| thrones | `verify_mod.py:288`, `:413` | **178** | **178 — unchanged** | 179 (+Dongzhan) |
| new characters / dynasties | — | — | **0 / 0** | 1 / 1 |
| loc rows | `verify_mod.py:167`, `:174` | **367** | **373** | 375 (+`name_dongzhan`, +the dynasty) |
| CoA references | `verify_mod.py:1082` | **122** | **125** | 125 |
| parliament `min_count` | `verify_mod.py:1240` | **1364** | **verify — expect 1366** | verify |

---

## VERIFICATION

Per CLAUDE.md's say-what-you-verified rule.

- **Verified — the reader, with the FULL ten-key tuple.** `tools/build_setup.py`
  was imported (its `__main__` guard is at `:7973`) and its own `_parse_defs`
  (`:732`), `_ownable_set` (`:756`), `_resolve_ruleset` (`:799`),
  `find_block_end` (`:5390`) and `COUNTRY_RE` (`:5443`) were used directly.
  `OWN_KEYS` was copied verbatim from `:5585` — all ten members. The reader
  reproduces **20,922 ownable locations**, **2,337 vanilla and 2,408 mod country
  blocks**, `samogitia_area` 16, `courland_province` 8, and — the
  `own_control_integrated` proof — **VTN 32, PLB 40, BTU 6, MGD 5, MUA 15**,
  every one a `SEA-PACKAGE.md` STATUS-band figure. VTN's vanilla block was
  further shown to carry `own_control_core` ×1 **and `own_control_integrated`
  ×1, so a nine-key reader returns 25 — the exact SEA phantom, reproduced and
  then avoided.
- **Verified — the pop parser, and a refinement to two earlier packages.**
  `VAN/main_menu/setup/start/06_pops.txt` yields **28,559 location blocks /
  50,227 `define_pop`** for lowercase-only keys, matching `AFRICA-PACKAGE.md`
  §E.3 and `SEA-PACKAGE.md` exactly, and **28,570 / 50,255** when the eleven
  uppercase-containing keys are included — a difference of **11 blocks and
  exactly 28 pops**, independently reproducing `KNOWLEDGE.md`'s "11 keys / 28
  pops" figure from `POP-PHASE.md`.
- **Verified — the tag scanner**, by feeding it GHA, MAK, ZAN, TMB (all four
  TAKEN with the registry `file:line` and the substring/en-loc counts
  `AFRICA-PACKAGE.md` §A.2 published) and PRU (TAKEN, **empty registry** — the
  formable-only class; VAN word **99**, matching Africa's narrower column
  exactly). `DBU`, `GTS`, `TKA`, `QTG`, `GSL`, `QNT`, `UTS`, `YLG`, `MYG`,
  `NGC`, `CGT`, `NGA`, `PHM`, `ZHL`, `RTG` come back **0/0/0/0/0**. **`TSO` and
  `TSN` are North American (`eastcoast.txt:276`, `:306`), `TSG` is East African
  (`east_africa.txt:242`), `YAR` is Yaroslavl (`russia.txt:106`), `SKY` is
  `russia.txt:260`, `SHL` is "Holstein" with an empty registry (the PRU class)** —
  all scanned, all refused. `LHG` (13 `LHG_` loc-parameter hits in
  `interfaces_l_*.yml`) and `LHS` (`APPEND_RHS`, `core_l_english.yml:436`) are
  the CAP class and are avoided rather than declared taken.
- **Verified — the theater's shape.** 223 ownable locations in `tibet_region`
  (`definitions.txt:3215`, children `amdo_area changtang_area kham_area
  ngari_area tsang_area u_area`, parent `east_asia`); **199 owned by 22 tags plus
  one CHI location, 24 unowned, ZERO double-ownership** (every location tested
  against all ten `OWN_KEYS` across all 2,408 mod country blocks); **781
  `define_pop`**. TIB's 59 break down as `u_area` 25, `tsang_area` 18,
  `changtang_area` 7, `ngari_area` 5, `kham_area` 3, `monyul_area` 1 (`phari`).
- **Verified — the Sakya date, from vanilla's own file.**
  `VAN/main_menu/setup/start/15_international_organizations.txt`: Nyingma
  `:1417` `creation_date = 1.1.1`; **Kadam `:1435` `1030.1.1`; Kagyu `:1454`
  `1050.1.1`; Sakya `:1472` `1073.1.1`; Jonang `:1494` `1120.1.1`.** The mod's
  future-date strip (`build_setup.py:6663-6675`) has already removed the last
  two; the surviving three sit at `MOD/…:1034`, `:1052`, `:1071` with members
  `DRG` / `KHS PUR MAR` / `ZNK NCN LMN SKK LHL`. **DRG is the Nyingma sect's
  only member.**
- **Verified — the Sakya web.** `MOD/main_menu/setup/start/12_diplomacy.txt:253`
  (`CHI→TIB vassal`) and `:396-409` (fourteen `TIB→X vassal` lines: GUG PUR MGG
  POO LGT DRG NCN GNJ BTG NBH LTN LMN MAR ZNK). Counted against the **vanilla**
  source the build reads every run (`VAN/12_diplomacy.txt:536`, `:752-765`):
  **exactly 15 lines name TIB**, all of which `_drop_landless_dep`
  (`build_setup.py:7494-7504`, drops on either side) removes once TIB is in
  `LANDLESS_AFTER`. The mod file carries **299 dependency lines and 28
  scripted pact lines**; **zero pact lines name any theater tag.**
- **Verified — TIB's block.** `MOD/main_menu/setup/start/10_countries.txt:44006`:
  59 locations, `capital = sakya`, `country_rank = rank_kingdom`,
  `starting_technology_level = 3`, `include = "expl_china"` **only** (the
  government block is fully inline: `type = theocracy`,
  `heir_selection = theocratic_elective`, thirteen sliders, eight laws, eight
  privileges, `parliament_type = council`), `tolerated_cultures = {
  changpa_culture khampa_culture }`, and **131 claims in
  `our_cores_conquered_by_others`** whose intersection with its 59 holdings is
  **zero** (so a landless TIB carries **190**).
- **Verified — the render laws.** `country_name_construction.txt` is 188 lines,
  first-match, read in full; `:91-97` needs `rank_empire` + a Chinese-family
  court language, `:99-104` needs `steppe_horde`, `:116-157` needs `rank_empire`
  or `country_type = pop`, `:159-164` catches the muslim group, and `:183-186`
  is the fallback whose `_map` is bare `"$NAME$"`
  (`government_names_l_english.yml:11-12`). **No Tibetan tag reaches anything but
  the fallback.** `country_ranks.txt` is 2,742 lines, first-match; **all 68
  `tag =` lines were listed and none names a Tibetan tag**, and a search of
  every one of its 255 `text = { }` branches for
  `tibet|utsang|ladakh|khampa|amdowa|changpa|sherpa|gyalrong|sikkim|
  tibeto_burman|bodic|himalay` returns **zero**. The theocracy ladder is
  `:897 bishopric` → `:907 theocracy_dharmic` → `:917 theocracy`, and
  `tibetan_buddhism` is `group = buddhist` (`religions/buddhist.txt:110-112`),
  **not `dharmic`** (`religion_groups/00_default.txt:10` vs `:29`) — so **TIB
  renders `rank_kingdom_theocracy`: "Theocracy" / "Grand" / "Grand Priest"**
  (`government_names_l_english.yml:503-507`). Tribe words:
  `rank_kingdom_tribe` `:944` → `:482-485` "Tribal Kingdom"/"King";
  `rank_duchy_tribe` `:1605` → `:790-792` "Tribe"/"Chief"; `rank_county_tribe`
  `:2278` → `:1018-1022` "Tribe"/"Minor"/"Chieftain".
- **Verified — the templates.**
  `VAN/main_menu/setup/templates/east_asia_monarchy_no_coast.txt` (63 lines):
  `include = "expl_china"` on line 2, `type = monarchy`,
  `heir_selection = cognatic_primogeniture`,
  `parliament = { parliament_type = council }`,
  `starting_technology_level = 3`, **no `reforms = { }` block**. Its siblings are
  `east_asia_monarchy.txt` and `east_asia_monarchy_not_present.txt`.
  `asia_advanced_no_pagan_tribe.txt`: `type = tribe`,
  `heir_selection = tribal_oldest_male`, `parliament_type = assembly`,
  `starting_technology_level = 2`. `limited_east_asia_monarchy.txt`:
  monarchy, tech 3. `expl_china.txt` (25 lines) grants `tibet_region`,
  `west_china_region` and fifteen more regions, so `lhasa`, `shigatse` and
  `xining` all pass `_assert_new_block_discovery` (`build_setup.py:5488`).
- **Verified — the registry.** `MOD/in_game/setup/countries/east_asia.txt` is a
  whole-file override whose only deviation from vanilla is a five-line header
  plus `CHI`'s `color = map_YUA` → `map_CSO` (diffed line by line). TIB sits at
  `MOD:2184` / `VAN:2179` (`culture_definition = utsang_culture`,
  `religion_definition = tibetan_buddhism`, `color = map_TIB`), and every other
  Tibetan block at a +5 offset. **PUR's `religion_definition` is `hindu`**
  (`MOD:2200`) against four `tibetan_buddhism` locations.
  `zz_1066_new_countries.txt` holds **71** blocks, read `utf-8-sig`, ending
  `… DJN SNH PGN HPJ KDR JGL`.
- **Verified — the colours.** `VAN/main_menu/common/named_colors/02_map.txt`
  carries **3,742** `map_*` keys. `map_TIB` `:2596` `rgb { 177 207 205 }` is
  used by TIB alone; `map_tibetan` `:2410` carries the **same value** and is
  `tibetan_language`'s own colour (`in_game/common/languages/00_tibet.txt:3`),
  used by no country. `map_changpa` `:2589`, `map_sherpa` `:2584`,
  `map_khampa` `:2411`, `map_amdowa` `:2412` are used by no country.
  **`map_GTS` and `map_TKA` do not exist** — the substring scan that would match
  them returns 0 for both tags over the whole vanilla tree.
- **Verified — the characters.** All 7,736 blocks in
  `VAN/main_menu/setup/start/05_characters.txt` were parsed for `tag =`.
  **Exactly six name a theater tag and the earliest birth is 1261.1.1**
  (`tib_zangpo_pal`, `VAN:96170`, `khon_dynasty`, `death_date 1323.1.1`);
  the rest are 1276, 1280, 1300, 1300, 1305. **No vanilla character in this
  theater is alive in 1066.** Three dynasties are homed here:
  `khon_dynasty` (`04_dynasties.txt:8215`, `home = sakya`, loc
  `dynasty_names_l_english.yml:674`), `lhachen_dynasty` (`:8220`, `home = shey`,
  loc `:751`), `purang_dynasty` (`:8225`, `home = purang`, loc `:1069`).
  `tibetan_language` (`00_tibet.txt:1`, family `tibetic_language_family`) lists
  ~110 male-name literals; `Yeshe` (`character_names_l_english.yml:14460`),
  `Rinchen` (`:14435`), `Namkha` (`:14416`), `Dorje` (`:14380`), `Osel`
  (`:14425`) and `Tashi` (`:14350`) carry loc rows. **`Tsede`, `Jangchub`,
  `Dongzhan`, `Gusiluo` and `Lhachen` are all ABSENT from both
  `character_names_l_english.yml` and `character_names_dynamic_l_english.yml`.**
- **Verified — the formable and the advances.**
  `00_formable_countries.txt:3101` `TIB_f`: `required_locations_fraction = 0.6`,
  `regions = { tibet_region }`, `potential = { culture = { has_culture_group =
  culture_group:tibetan_group } }` (`culture_groups/00_culture_groups.txt:210`),
  `rule = historical`, empty `form_effect`. **It is the only formable naming any
  Tibetan tag, region, area or culture group.** **27 vanilla formables already
  target a tag that the current mod build leaves landless** (WLS, DLH, LAT, THE,
  LIV, ULS, TIM, ARM, ALB, BUL, TRA, FIN, MIR, CIR, TUR, YUA, CSH, NOL, SWI,
  NSA, KOJ, YMT, MGE, DAH), and 29 target landed tags — so an existing landless
  target is the norm, not an exception. `VAN/in_game/common/advances/country_TIB.txt`
  is 80 lines with **7 nodes**, all `potential = { has_or_had_tag = TIB }`, the
  first named `sakya_hegemony`. **Zero vanilla event files reference TIB**
  (grep over `VAN/in_game/events/`); the only other engine reference is
  `situations/little_ice_age.txt:45`.
- **Verified — the resolutions.** Every count in §E.1 was produced by
  `build_setup._resolve_ruleset` itself: DBU 25, GTS 19, GUG 5, NBH 3, TKA 6,
  total **58**, **pairwise disjoint (zero overlaps)**. `LOCATION_VACATED`'s
  snapshot intersection over `naktsang_province` + `namru_province` ∩ TIB's
  holdings resolves **7** (`gonkri namtso_doring ronglung serzhik shantsa
  tsedzong zangdan`, 15 `define_pop`), correctly excluding the already-unowned
  `zagya`. 52 + 7 = **59 = TIB's entire holding**, verified by set arithmetic.
  Every granted location carries **exactly one** ownership entry — measured with
  the ten-key reader — so `UNOWNED_GRANTS` is not needed and must not be used.
- **Verified — the IO consequences.** Every `members`/`free_city`/`elector`/…
  list in `MOD/main_menu/setup/start/15_international_organizations.txt` was
  scanned for TIB: **it appears in exactly one, the Middle Kingdom's at `:164`
  (199 members)**, and in **no sect**. Twenty-one Middle Kingdom members are
  Tibetan-plateau or Sino-Tibetan-frontier tags. **28 of the 35 landed
  `tibetan_buddhism`/`bon` tags are currently in no sect**, a pre-existing
  consequence of the correct Sakya/Jonang strip. `build_ios`'s sweep is
  `:6804-6825` with `n_ghosts` asserted at **155** (`:6893`); the pinned
  empty-members check is `verify_mod.py:902-911` at **9**.
- **NOT verified, and stated as such — every historical claim carrying `[U]` or
  `[D]`:** the collapse of the Tibetan empire (842) and the Yumten/Ösung split;
  Kyide Nyimagön's westward migration (c. 930) and the founding of the Ngari
  Korsum as Maryul, Guge and Purang; Yeshe-Ö (c. 947-1024), Tholing's founding
  (997), Rinchen Zangpo, Jangchub Ö and the invitation of Atiśa (arrived 1042,
  died 1054); Tsede of Guge (c. 1057-1088); Dromtön and Reting (1057); the Kadam
  school's formation; Marpa (1012-1097) at Drowolung in Lhodrak and Milarepa;
  the founding of Shalu (1040), Sakya (1073) and Sangphu (1073); Khön Konchok
  Gyalpo; the Sakya hegemony under Yuan patronage (1264+) and the thirteen
  myriarchies of the 1268 census; Phagmodrupa (1354) and Rinpungpa; the Ladakh
  chronicle's 11th-century king-list; Purang's absorption by Guge (c. 1100);
  Gusiluo/rGyal-sras of Tsongkha (c. 997-1065), his son Dongzhan (r. 1065-1086),
  the Song alliance and the Song conquest of Qingtang (1104); Wang Shao's
  Hehuang campaigns (1070s); the Xia-Tsongkha wars; the foundation dates of
  Derge, Lingtsang, Batang, Litang, Nangchen, Gonjo, Nubhor, Powo, Minyag,
  Gyelrong, Hor and Nyarong; the Namgyal dynasty of Sikkim (1642); Bhutan's
  Drukpa unification (1616); the Khasa-Malla kingdom; and every statement that a
  named polity did or did not exist on 1066.9.15. Every one rests on this
  agent's own history and needs a source before it enters a comment, let alone
  setup data.
- **NOT checked, and OWED before implementation:**
  (1) **how the engine derives `country_rank` when a block declares none.**
  `VAN/in_game/common/country_ranks/00_default.txt` carries `level`, modifiers
  and an `allow` block calling `can_upgrade_country_rank`, but **no size rule**.
  Twenty-one of the theater's 22 landed tags declare no rank, and every
  "size-derived" cell in §F.3 is a prediction about engine code, not about data.
  Inherited unresolved from `SEA-PACKAGE.md`'s owed list (3).
  (2) **whether `required_locations_fraction` counts OWNABLE locations or raw
  `definitions.txt` membership.** `tibet_region` has 349 raw members and 223
  ownable; 0.6 of those is 210 versus 134. It decides how hard `TIB_f` is, and
  no file in this repo settles it.
  (3) **whether a country of a sect-bearing religion that belongs to no sect
  logs anything.** `tibetan_buddhism` carries `max_sects = 1`
  (`religions/buddhist.txt:115`) and **28 landed tags are currently sect-less**
  as a result of an item already shipped. If it is silent, OPEN DECISION 9 is
  cosmetic; if it is not, the theater already carries 28 lines nobody has
  attributed.
  (4) **whether the engine validates a setup `reforms = { }` entry against the
  reform's own `potential`** — inherited unresolved from `AFRICA-PACKAGE.md` and
  `SEA-PACKAGE.md`. Not triggered here (no template in this theater carries a
  `reforms` block at all, measured), but still owed for the general case.
