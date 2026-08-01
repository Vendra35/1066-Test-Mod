> **STATUS (2026-08-02): IMPLEMENTED as HANDOFF item 27 (landed 2026-08-01).**
> This document is the research record, not the state: the landing and its
> deviations live in docs/HANDOFF.md item 27 and the build_setup.py comments.
> Where this document and the landed code disagree, the code and HANDOFF win.

# CENTRAL ASIA 1066 — research package (DRAFT)

**DRAFT — pending main-session review. Nothing here has been written into
the repo.** Produced by an Opus research agent, 2026-07-30. Every mechanical
claim carries a `file:line`. Historical claims that no file can settle are
flagged `[U]` (unverified / estimated) or `[D]` (sources genuinely differ),
never asserted silently.

Reference roots used:
`VAN = E:\SteamLibrary\steamapps\common\Europa Universalis V\game`
(probed live: `VAN/in_game/map_data/definitions.txt`, 491179 bytes, present)
`MOD = .../1066 Test Mod` — current owners read from the GENERATED
`main_menu/setup/start/10_countries.txt` (built 2026-07-29 22:43), parsed with
build_setup.py's own `OWN_KEYS` tuple (`tools/build_setup.py:3403-3407`) and
its own `COUNTRY_RE` (`tools/build_setup.py:3265`). Two earlier parses of mine
were WRONG until they matched those two constants exactly — recorded here
because it is the same class of silent-zero the harness discipline exists for:
a tag line may carry a trailing comment (`\tCHG = { #Chagatai`) and ownership
also lives in `own_control_integrated`, which a naive key list misses.

---

## 0. The theater, and where its seams are

**Fixed and untouchable:** the Oxus is SEL's eastern border. SEL currently
holds 463 locations including `kath_province`, `khiva_province`,
`uzboy_province` (`tools/build_setup.py:794-801`) — i.e. **Khwarazm is already
inside SEL**. Nothing in this package moves a SEL-owned location. See §4 below
for why that is also historically right.

**Mine:** everything east of the Volga. **Not mine:** the Pontic steppe, the
Rus, and `astrakhan_area` (37 locations, all GLH — the area straddles the
Volga; `dardeling_province`/`priyutnoye_province` are Kalmykia, west bank).
Named as a seam in OPEN DECISION 8.

**The one shared object across that seam is GLH (the Golden Horde).** It is a
single tag holding **731 locations** from the Dniester to the Ob. This package
takes 327 of them (28 to a new Volga Bulgar tag, 15 to the eastern Karakhanids,
284 vacated) and leaves GLH standing on **404** — the Pontic/Don/Kuban/Astrakhan
block that belongs to the Rus/steppe package. GLH therefore does NOT go landless
in this slice, and the Golden Horde remains visible on the 1066 map until that
package lands. That is a deliberate, stated compromise, not an oversight.

### What the region actually looks like in the current build

Resolved from `definitions.txt` (ownable = the location's
`location_templates.txt` block carries a `culture` field, the build's own test,
`tools/build_setup.py:650-658`):

| area (all in `khorasan_region` unless noted) | ownable | current owners |
|---|---|---|
| `transoxiana_area` | 96 | CHG 49, YSU 15, BRL 13, JLY 9, GLH 9, SLD 1 |
| `zhetysu_area` | 70 | CHG 63, GLH 6, OGE 1 |
| `desht_kipchak_area` | 85 | GLH 85 |
| `khwarazm_area` | 32 | SEL 16, GLH 16 |
| `badakhshan_area` | 38 | BKH 18, SLD 8, KRG 5, KTT 4, QUN 3 |
| `tarim_area` (`xinjiang_region`) | 54 | DGH 20, QCH 16, MNL 7, SRL 4, 7 unowned |
| `dzungaria_area` (`xinjiang_region`) | 36 | CHG 15, QCH 13, TRH 6, OGE 2 |
| `bolghar_area` (`ural_region`) | 21 | GLH 21 |
| `kazan_area` (`ural_region`) | 30 | GLH 15, PRM 15 |
| `bashkiria_area` (`ural_region`) | 26 | GLH 26 |
| `lower_yik_area` (`steppes_region`) | 33 | GLH 33 |
| `astrakhan_area` (`steppes_region`) | 37 | GLH 37 (SEAM — not mine) |

The transoxiana/zhetysu estimate in `docs/HANDOFF.md:967` ("~175 land") is
close: the true resolved figure is **96 + 70 = 166 ownable**.

Tag identities, all verified in `VAN/in_game/setup/countries/`:

| tag | what | identity block | 1337 role |
|---|---|---|---|
| CHG | Chagatai | `east_asia.txt:2219` | the ulus itself; `type = army`, `government.type = steppe_horde`, capital `almaliq`, 127 locations (`VAN/main_menu/setup/start/10_countries.txt:48769`) |
| YSU | Yasa'uri | `persia.txt:373` | Chagatai amir house, holds **Samarkand + Bukhara**, 15 |
| BRL | Barlas | `persia.txt:365` | Timur's own house, Kish/Shahrisabz, 13 |
| JLY | Jalayirs | `persia.txt:389` | Khujand/Jizzakh, 9 |
| SLD | Suldus | `persia.txt:357` | Chaghaniyan/Termez/Hissar + kelif, 9 |
| QUN | Qara'unas | `persia.txt:325` | 6 left: `araska kulob munk` (mine) + `asadabad_kunar hajiabad parun` (`upper_indus_area`, NOT mine) |
| HLG | Huleguids | `persia.txt:309` | 1 left: `kazimah` — **the Arabia slice's**, not mine |
| GLH | Golden Horde | `steppes.txt:1` (behind the BOM) | `type = army`, `government.type = steppe_horde`, capital `sarai_al_jadid`, 731 |
| DGH | Dughlats | `east_asia.txt:3367` | Kashgar/Yarkand/Khotan, 20 |
| QCH | Qocho | `east_asia.txt:2238` | Uyghur Turfan, 29 |
| MNL | Mangalai | `east_asia.txt:2246` | Aksu/Kucha, 7 |
| SRL | Sarikol | `east_asia.txt:3383` | Pamir, 4 |
| BKH / KRG / KTT | Badakhshan / Karategin / Khuttal | `east_asia.txt:3359`, `:3375`, `persia.txt:381` | 18 / 5 / 4 |
| TRH / OGE | Oirat / (Altai) | `east_asia.txt:3311`, `:3279` | upper Irtysh 6, Altai 19 |
| PRM / VYT | Perm / Vyatka | `russia.txt:309` / — | Kama 64, Vyatka 20 — the Rus package's |

**No Karakhanid, Kipchak, Oghuz or Volga-Bulgar tag exists in vanilla.**
`country_names_l_english.yml` has zero hits for karakhanid/qarakhanid/kipchak/
cuman/oghuz/yabghu; `bulghar`/`bolghar` occurs only as `bolghar_area`,
`bolghar_culture`, `bolghar_province`, `bolghar` (the location). The one
`Qarakhanid` string in vanilla is a **first-name pool entry**
(`character_names_l_english.yml:14305`, inside a run of Mongolian clan names),
not a country and not a dynasty.

---

## A. Registry additions (`in_game/setup/countries/zz_1066_new_countries.txt`)

Three new tags. **Freeness proven three ways** for each: (1) absent from all
2217 identity entries in `VAN/in_game/setup/countries/`; (2) `\bTAG\b`
ripgrep over the ENTIRE vanilla game tree → *No matches found*; (3) the same
ripgrep over the entire mod repo → *No matches found*. (Eight further
candidates cleared the same three gates and are banked: KRH SMQ TRX KHQ BLR
OGZ YBG QPQ. `KAZ` is **not** free — it is the Kazakh Khanate formable's tag,
`in_game/common/formable_countries/00_formable_countries.txt:4572-4602`, and
reusing it would consume that formable.)

```
QRK = { #Western Kara-Khanid Khanate (Samarkand)
	color = map_QRK
	color2 = rgb { 16 41 202 }

	culture_definition = khorezmian_culture
	religion_definition = sunni
}

QRA = { #Eastern Kara-Khanid Khanate (Balasagun)
	color = map_QRA
	color2 = rgb { 16 41 202 }

	culture_definition = khorezmian_culture
	religion_definition = sunni
}

BLH = { #Volga Bulgaria (Bolghar)
	color = map_BLH
	color2 = rgb { 16 41 202 }

	culture_definition = bolghar_culture
	religion_definition = sunni
}
```

Citations: `khorezmian_culture` `VAN/in_game/common/cultures/turkic.txt:102`
(`language = karluk_language`); `bolghar_culture`
`VAN/in_game/common/cultures/tartar.txt:159` (`language = oghuric_language`);
shape and `color2` per the taifa entries already in the mod's registry
(`in_game/setup/countries/zz_1066_new_countries.txt:24-31`).

`culture_definition` choice, stated honestly: Samarkand/Bukhara/Kashgar all
carry `khorezmian_culture` in vanilla's own 1337 templates, so QRK/QRA match
the pops as well as the history. **BLH does not** — `bolghar`, `bilyar` and
`kazan` are template culture `kazani` (`location_templates.txt`), the Kipchak
successor. `bolghar_culture` is the historically correct 1066 identity and it
exists in vanilla; the pops stay `kazani` until the pop phase. This is exactly
the al-Andalus situation the taifa slice shipped and the user accepted
(`docs/HANDOFF.md:406-408`). Alternative — set `kazani` and match the pops — is
OPEN DECISION 6.

**Three new colors** in `main_menu/common/named_colors/zz_1066_map_colors.txt`,
each commented like the existing rows:
```
	map_QRK = rgb { 40 90 160 }     # W. Karakhanids  steppe blue
	map_QRA = rgb { 96 150 205 }    # E. Karakhanids  pale blue (branch of QRK)
	map_BLH = rgb { 150 100 60 }    # Volga Bulgaria  Volga bronze
```
(Values are a suggestion only; the visual constraint is that QRK/QRA must read
as related-but-distinct — the Cagliari/Gallura lesson, `docs/HANDOFF.md:378-382`
— and that BLH must not collide with GLH's `map_golden_horde`.)

Add QRK/QRA/BLH to `verify_mod.py`'s `_GENERATOR_OK` (the tier-3 comment
shape), unless the CoA batch gives them bespoke arms.

**Localisation** (`main_menu/localization/english/1066_norman_conquest_l_english.yml`,
one physical line each):
```
 QRK: "Kara-Khanids"
 QRK_ADJ: "Kara-Khanid"
 QRK_THE: "$common_string_prefix_article$"
 QRA: "Eastern Kara-Khanids"
 QRA_ADJ: "Eastern Kara-Khanid"
 QRA_THE: "$common_string_prefix_article$"
 BLH: "Volga Bulgaria"
 BLH_ADJ: "Bulgar"
 BLH_THE: "$common_string_prefix_article$"
```
`_THE` shape copied from the mod's own `SEL_THE`
(`1066_norman_conquest_l_english.yml:144`). Note the standing caveat there:
whether the engine consults `_THE` is still unproven (`docs/HANDOFF.md:1003-1005`).

---

## B. NEW_COUNTRIES blocks

All three follow `_seljuk_block`'s shape (`tools/build_setup.py:849-905`) —
the inland Muslim monarchy that the Seljuk slice already proved in game.

```
	QRK = {
		starting_technology_level = 3
		include = "expl_middle_east"
		include = "muslim_monarchy_no_abrahamic_dhimmi_no_coast"

		government = {
			heir_selection = cognatic_primogeniture
			laws = {
				sharia_law = hanafi_policy
			}
		}
		court_language = karluk_language
		religious_school = hanafi_school

		country_rank = rank_kingdom

		capital = samarkand
	}
```
`QRA` identical with `capital = balasagun`.

```
	BLH = {
		starting_technology_level = 3
		include = "expl_middle_east"
		include = "muslim_monarchy_no_abrahamic_dhimmi_no_coast"
		discovered_regions = {
			ural_region
			russian_region
			ruthenia_region
		}

		government = {
			heir_selection = cognatic_primogeniture
			ruler = random
			laws = {
				sharia_law = hanafi_policy
			}
		}
		religious_school = hanafi_school

		country_rank = rank_duchy

		capital = bolghar
	}
```

Field-by-field:

- `expl_middle_east` — grants `khorasan_region` AND `xinjiang_region` AND
  `steppes_region` (`VAN/main_menu/setup/templates/expl_middle_east.txt:15-17`),
  which covers `samarkand` and `balasagun` (both `khorasan_region`) and QRA's
  Kashgaria (`xinjiang_region`). 132 vanilla uses; the build's capital-discovery
  assert (`tools/build_setup.py:3310-3339`) passes for both.
- BLH's **inline `discovered_regions`** — `expl_middle_east` does NOT contain
  `ural_region`, and `bolghar` lives there, so the capital assert would kill the
  build. Inline `discovered_regions` in a setup country block is attested 176
  times in vanilla's own `10_countries.txt`; the exact three-region shape is
  vanilla's OBD block (`VAN/main_menu/setup/start/10_countries.txt:3512-3515`).
  `expl_novgorod` (42 uses) is the ready-made alternative — it carries
  `ural_region` + `russian_region` + `steppes_region`
  (`VAN/main_menu/setup/templates/expl_novgorod.txt:1-19`) but drags in the
  whole Latin West.
- `_no_coast` — none of the three touches sea. The `_no_coast` Muslim variant
  carries **no `heir_selection`** (read in full,
  `VAN/main_menu/setup/templates/muslim_monarchy_no_abrahamic_dhimmi_no_coast.txt`
  — the `government` block goes straight from `type = monarchy` to the ethos
  sliders), so it must be restated. This is the diff-measured rule the Seljuk
  slice already encodes (`tools/build_setup.py:861-863, 887-888`). If the
  engine's maritime self-heal (`government.cpp:3662`) flags any of the three at
  next launch, swap that one to the coastal variant — same route as
  `docs/HANDOFF.md:581-584`.
- `hanafi_policy` / `hanafi_school` — Transoxiana was the Hanafi heartland and
  Tamghach Ibrahim's Samarkand madrasas were Hanafi; the Volga Bulgars took
  Hanafi Islam with Ibn Fadlan's mission (922). Identifiers verified:
  `hanafi_policy` `VAN/in_game/common/laws/01_legal_system.txt:1005`,
  `hanafi_school` referenced at `:982`. The build FORBIDS a school of `None`
  (`tools/build_setup.py:872-874`, engine
  `initialize_from_bookmark.cpp:520`).
- `court_language = karluk_language` on QRK/QRA — attested at vanilla's own CHG
  block (`VAN/main_menu/setup/start/10_countries.txt:48769ff`,
  `court_language = karluk_language`) and historically pointed: the Kutadgu
  Bilig, the first Turkic mirror-for-princes, was written for a Karakhanid khan
  in 1069, three years after our start date. BLH gets none (default = culture's
  `oghuric_language`).
- `heir_selection = cognatic_primogeniture` — the project's attested restate
  value. See OPEN DECISION 7 for `partition_inheritance`, which is the
  Karakhanid appanage system itself and is legal for monarchy
  (`VAN/in_game/common/government_types/00_default.txt:7`).
- Ranks — see §F.

---

## C. Rulers

| tag | character key | name key / literal | accession | birth | regnal | dynasty | notes |
|---|---|---|---|---|---|---|---|
| QRK | `qrk_ibrahim_tamghach_khan` | LITERAL `Ibrahim` — vanilla row `character_names_l_english.yml:1364` (`Ibrahim: "Ibrahim"`), the same class as the mod's own `Alp_Arslan` / `Muslim` literals (`tools/build_setup.py:2365-2366`) | 1040.1.1 [U] | 1000.1.1 [U] | 1 | `qarakhanid_dynasty` NEW | Ibrāhīm ibn Naṣr, Böri Tigin, **Tamghach Bughra Khan**, ruled Samarkand c.1040–1068. The single best-attested person in this theater: madrasa and hospital founder, coin issuer, the khan the Western Kaghanate is named for. `culture = khorezmian_culture`, `religion = sunni`, `birth = samarkand` |
| QRA | `qra_mahmud_toghrul_khan` | `name_mahmud` — VANILLA key, bare row + arabic/persian/turkish rows (`character_names_dynamic_l_english.yml:11761-11764`); renders "Mahmud" for a karluk-language culture via the bare row | 1059.1.1 **[D]** | 1010.1.1 [U] | 1 | `qarakhanid_dynasty` (or the eastern branch house — see §D) | Maḥmūd ibn Yūsuf, **Toghrul Qara Khan**, eastern khan c.1059–1075. **[D]: the eastern regnal list is genuinely unstable between authorities** — Sulaymān b. Yūsuf (1032–56), Muḥammad b. Yūsuf (1056–57), Ibrāhīm b. Muḥammad (1057–59), then Maḥmūd. Any of the middle three appears with different dates in different lists; Maḥmūd is the majority reading for 1066. `culture = khorezmian_culture`, `religion = sunni`, `birth = kashgar` |
| BLH | — | — | — | — | — | — | **`ruler = random` DELIBERATELY.** The Volga Bulgar king-list is blank for the whole 11th century: the named rulers stop with Muʾmin ibn al-Ḥasan in the 970s and do not resume until the 12th. Inventing one would be worse than random. Precedent: ARB/GAL/COR, SIS and MZN all ship random for exactly this reason (`docs/HANDOFF.md:370-372`, `:492`) |

If the Toghrul reading is preferred as the *displayed* name (the Alp Arslan
precedent — vanilla itself seats a man under his throne-name, not his given
name Muḥammad), the literal `Toghrul` also exists in vanilla
(`character_names_l_english.yml:15547`) and needs no loc row of ours. So does
`Bughra` (`:15441`) if a Bughra Khan is ever wanted. **No invented name key is
required by this package** — a first for a slice this size.

Character-block shape follows the taifa/Seljuk entries verbatim
(`tools/build_setup.py:2153-2161`): `first_name`, `culture`, `religion`,
`birth_date`, `birth`, `dynasty`, `tag`. No `death_date` (the alive law).

---

## D. Dynasties (`main_menu/setup/start/04_zz_1066_dynasties.txt`)

Vanilla ships 1269 dynasties and **not one Karakhanid** — grep for
afrasiyab / qarakhan / karakhan / ilek / bughra over
`VAN/main_menu/setup/start/04_dynasties.txt` returns only `seljukids_dynasty`
(`:8010`). One house is therefore new.

```
	qarakhanid_dynasty = {
		name = { name = qarakhanid_dynasty }
		home = samarkand
	}
```
loc row: ` qarakhanid_dynasty: "Qarakhanid"`

No key collision: the existing vanilla `Qarakhanid` string is a first-name pool
entry, a different key in a different file
(`character_names_l_english.yml:14305`).

**One house or two?** The Karakhanids are one lineage (the Āl-i Afrāsiyāb)
split into two branches — the **Alids** (descendants of ʿAlī b. Mūsā; Ibrāhīm
b. Naṣr b. ʿAlī, our QRK) and the **Hasanids/Yūsufids** (descendants of Ḥasan
b. Sulaymān; Maḥmūd b. Yūsuf b. Hārūn, our QRA) [D]. Two-branch option:

```
	qarakhanid_ali_dynasty  = { name = { name = qarakhanid_ali_dynasty  } home = samarkand }
	qarakhanid_hasan_dynasty= { name = { name = qarakhanid_hasan_dynasty} home = balasagun }
```
loc ` qarakhanid_ali_dynasty: "Āl-i ʿAlī"` / ` qarakhanid_hasan_dynasty: "Āl-i Ḥasan"`

**Recommendation: ONE house, `qarakhanid_dynasty`, loc "Qarakhanid".** The two
tags already carry the split; two near-identical Arabic house names on the map
buys precision the player cannot read. OPEN DECISION 3.

No dynasty for BLH (no ruler).

---

## E. Territory

### E.1 `_CENTRALASIA_RULES` — the definitions.txt-resolved grants

Same 5-tuple shape as `_SELJUK_RULES` (`tools/build_setup.py:792-821`):
`tag: (sweep names, singles, minus-sweeps, minus-singles, expected)`.
Every count below was resolved by an independent reimplementation of
`_resolve_ruleset` (`tools/build_setup.py:693-723`) against
`definitions.txt` + `location_templates.txt`, and the donor breakdown was
cross-checked against the built `10_countries.txt`.

```python
_CENTRALASIA_RULES = {
    # Western Kara-Khanid Khanate — Transoxiana proper: the Zarafshan
    # (Samarkand, Bukhara), the Kashka Darya (Kish/Nasaf), Amul on the Oxus,
    # Ustrushana, Khujand, and Chaghaniyan/Termez north of the river.
    "QRK": (["samarkand_province", "bukhara_province", "nurota_province",
             "amol_province", "kelif_province", "jizzakh_province",
             "khujand_province", "hissar_province"],
            [], [], [], 46),

    # Eastern Kara-Khanid Khanate — Chach, Isfijab, Ferghana, the middle and
    # lower Syr Darya, Semirechye, the Tian Shan, and Kashgaria.
    "QRA": (["chach_province", "isbijab_province", "akhsikath_province",
             "andijan_province", "farghana_province", "naryn_province",
             "otrar_province", "turkestan_province",
             "sighnaq_province", "yangikent_province",
             "zhetysu_area",
             "kashgar_province", "yarkand_province", "khotan_province"],
            ["charchan", "niya", "mazar_tagh"],
            ["emin_province"], [], 142),

    # Khuttal — the one Oxus-bank principality kept as its own state.
    # KTT already holds 4 of these 6; the two others are QUN's residue.
    # Grants that overlap the recipient's own holdings are no-ops by
    # construction (the KRM/MZN/HLL precedent, tools/build_setup.py:3472-3474).
    "KTT": (["kulab_province"], [], [], [], 6),

    # Volga Bulgaria — the Volga-Kama triangle: Bolghar, Bilyar, Suvar, and
    # the Kazan bank. The Mari forest and Bashkiria are NOT owned (see E.2).
    "BLH": (["bolghar_area", "kazan_province"], [], [], [], 28),
}
```

**Donor breakdown (verified against the built file):**

| recipient | total | from |
|---|---|---|
| QRK | **46** | YSU 15, BRL 13, SLD 9, JLY 9 — **exactly all four tags' entire holdings** |
| QRA | **142** | CHG 106, DGH 20, GLH 15, OGE 1 (`ayagoz`) |
| KTT | **6** | KTT 4 (no-op), QUN 2 (`kulob`, `munk`) |
| BLH | **28** | GLH 28 |

QRK's 46 is the pleasing result of the pass: the four Chagatai amir-houses
that hold western Transoxiana in 1337 (Yasa'uri at Samarkand and Bukhara,
Barlas at Kish, Jalayir at Khujand, Suldus at Termez) are **exactly** the
territory of the Western Kaghanate, to the location. Nothing had to be
hand-picked.

`emin_province` is subtracted from `zhetysu_area` because Tarbagatai/Emin is
Kimek country, not Karakhanid: `emin targabatay dahra_sasykkol ilanbalyk
koktuma toli` (6, all CHG) fall into E.2 instead.

**Capital asserts to add** (the `_SELJUK_TAGS` pattern,
`tools/build_setup.py:3481-3483`): `samarkand ∈ QRK`, `balasagun ∈ QRA`,
`bolghar ∈ BLH`. All three hold in the resolved lists.

### E.2 `LOCATION_VACATED` — a NEW build mechanism

**This slice needs something the build cannot do yet: remove a location from
its owner and give it to nobody.** There is no such list today —
`LOCATION_TRANSFERS` and `LOCATION_GRANTS` both end in a write
(`tools/build_setup.py:3597-3629`), and `LANDLESS_AFTER` only *asserts*
emptiness (`:3683-3705`).

Unowned land is not exotic: **7334 of vanilla's 20922 ownable locations have no
owner at all** in `VAN/main_menu/setup/start/10_countries.txt` — measured, both
in vanilla and in the mod's current build (identical figure, so no slice so far
has created or destroyed one). `tarim_area` alone ships 7 unowned and
`qashliq_area` 16, immediately adjacent to what this package vacates.

Proposed shape — snapshot-based, because a definitions-resolved list would
contain already-unowned locations and trip `_remove_owned_many`'s exactly-once
assert:

```python
# tag -> area/province names; resolves to (members ∩ that tag's CURRENT holdings)
LOCATION_VACATED = {
    "GLH": [ ...Tier A..., ...Tier B... ],
    "CHG": ["dzungaria_area", "emin_province"],
}
```
with an exact-count assert per tag and a post-validate that every listed
location ends owned by nobody.

**Tier A — the Kipchak steppe and the Volga-Ural forest edge (168, all GLH):**
`desht_kipchak_area` (85), `lower_yik_area` (33), `bashkiria_area` (26),
`yaransk_province` (8), and Mangyshlak/Ust-Yurt —
`mangistau_province` + `mangyshlak_province` + `ust_yurt_province` (16).

**Tier B — West Siberia (116, all GLH):** `chimgi_tura_area` (15),
`qashliq_area` (9), `omsk_area` (28), `kulykol_area` (14), `bursol_area` GLH
part (14), `suzun_area` GLH part (17), `tomsk_area` GLH part (5),
`surgut_area` (14). **Tier B is optional** — see OPEN DECISION 9. OGE's 15
locations inside `bursol_area`/`suzun_area` are untouched.

**CHG residue (21):** `dzungaria_area` CHG part (15: `urumqi manas bortala
jing kuytun urghtbulaq usu_xinjiang utbulaq zhekdeliq yangjibaliq kutubi
ulan_us qanbalik hoboksar gonganbao`) + `emin_province` (6). Vacating these is
what makes CHG landless. Alternative: hand the Dzungarian 15 to QCH (Qocho) —
OPEN DECISION 5.

### E.3 Landless after

```
CENTRALASIA_LANDLESS = ("CHG", "YSU", "BRL", "JLY", "SLD", "DGH")
```
Six tags, all Mongol-era, all reduced to zero by E.1 + E.2. Each keeps its
registry identity and its pre-pass holdings become
`our_cores_conquered_by_others` — the established shape the build automates
(`tools/build_setup.py:3588-3705`).

**This is also the answer to the `initialize_from_bookmark.cpp:2477` question**
(`docs/EU5-ERROR-DECODER.md:540-546`). Measured: the mod already ships **14
landless `type = army` tags** — JAL ZAZ TIM MGE OIR CHB UGH GRG JUR JKR NGD BSD
ART APD — and the observed 2477 lines name only HLG (1 location), QUN (6) and
SLD (9), i.e. the tiny-but-LANDED ones. **Landless is therefore the safe
terminal state for an army-based tag, and "retire them properly" means make
them landless, not shrink them.** Caveat stated plainly: the decoder's list of
named tags may be abridged, so the next error.log must be checked for 2477
lines naming CHG/YSU/BRL/JLY/SLD/DGH. If any appear, the fallback is a
FIELD_FIXES strip of the `type = army` line on those six.

After this slice the 2477 class still owns two tags: **HLG** (`kazimah`, the
Arabia slice's — `docs/HANDOFF.md:971-972`) and **QUN**, which keeps
`asadabad_kunar hajiabad parun` in `upper_indus_area`. Those three are not in
my theater; whoever does the Afghan/upper-Indus review should take them and
close QUN. Flagged, not fixed.

### E.4 What this slice moves, in one line

218 net location changes of owner (46 + 142 + 2 + 28) plus 305 vacated
(168 + 116 + 21) = **523 locations touched**, 3 new tags, 6 tags retired,
2 named rulers. GLH 731 → 404. CHG 127 → 0.

---

## F. Government and rank — and the naming consequence, worked out

### F.1 The horde trap, measured

The rule in `CLAUDE.md` is exact and I re-verified every link:

- `country_name_construction.txt:98-103` — branch
  `country_name_construction_prefix_name_horde`, trigger
  `government_type = government_type:steppe_horde`.
- `government_names_l_english.yml:15` —
  `country_name_construction_prefix_name_horde: "$country_name_construction_prefix_adjective_rank$"`
- `government_names_l_english.yml:9` —
  `country_name_construction_prefix_adjective_rank: "$PREFIX$ $ADJ$ $RANK$"`

So a steppe_horde's map name is PREFIX + **ADJECTIVE** + RANK and its NAME key
is never read. The rank words are:
`rank_kingdom_horde: "Horde"` / ruler `"Khān"` (`:124-125`);
`rank_empire_horde_prefix: "Great"`, `rank_empire_horde: "Horde"`, ruler
`"Khāghān"` (`:119-121`); `rank_duchy_horde: "Horde"` / ruler `"Noyan"`
(`:764-765`).

The build's assert lives at `tools/build_setup.py:3558-3573`; it detects
`type = steppe_horde` both in-block and through includes, and dies with
`steppe-horde recipients forbidden`. **CHG trips it today** — CHG carries
`government = { type = steppe_horde }` and would be a donor, not a recipient,
so no conflict; but any Kipchak/Oghuz horde *recipient* would.

There are currently **19 landed steppe_horde tags** in the build (GLH 731,
CHG 127, CRS 37, OTC 23, HCN 21, DGH 20, OGE 19, QAS 19, BAT 18, BGT 17,
KHD 16, YSU 15, BRL 13, SLD 9, JLY 9, TRH 6, QUN 6, KTT 4, HLG 1) and 17
landless. **This matters for the loc-override escape hatch: overriding
`rank_kingdom_horde` to "Khanate" would hit every one of them**, so the
"Holy"-drop trick (`docs/HANDOFF.md:552`) does not transfer here.

### F.2 The choice this package makes

**QRK and QRA are Muslim MONARCHIES, not hordes.** By 1066 the Karakhanids
were a settled Islamic dynasty minting coin in Samarkand and Kashgar, endowing
madrasas, and having the khuṭba read in their name — the exact profile the
`muslim_monarchy` template models. This choice:

- keeps the NAME key alive (map name is composed by
  `country_name_construction_sultanate`, `country_name_construction.txt:158-163`,
  trigger `religion.group = religion_group:muslim`, value
  `"$PREFIX$ $RANK$ of $ARTICLE$ $NAME$"`);
- passes the build's horde assert without touching it;
- **renders `rank_kingdom` + muslim as "Sultanate"** —
  `rank_kingdom_muslim: "Sultanate"`, ruler `"Sultan"`
  (`government_names_l_english.yml:463-464`), reached because
  `country_ranks.txt:1059-1069`'s generic muslim-kingdom branch is first-match
  for anything not MAM/MOR/TLE/TUN/GRA.

**So the map will read "the Sultanate of the Kara-Khanids" and "Sultan
Ibrahim".** That is historically wrong — they were khans and khaqans, never
sultans — and it is the SAME defect already banked for SEL
(`docs/HANDOFF.md:1028-1039`). It is one problem, not two, and it has one fix:
a whole-file override of `country_ranks.txt` inserting tag-gated
"Khanate"/"Khan" branches ahead of the generic muslim branch, exactly as
`rank_kingdom_muslim_mamluk` (`country_ranks.txt:1011-1018`) proves the slot
exists. First-match-wins rules out an additive file. **Recommendation: ship
"Sultanate" now, bundle the Khanate branch with the already-parked
Muslim-empire-styling pass, and treat that pass as covering SEL + QRK + QRA
together.** OPEN DECISION 1.

**BLH is `rank_duchy`**, which gives `rank_duchy_muslim: "Emirate"` and ruler
`"'Amīr"` (`government_names_l_english.yml:781-782`) → **"the Emirate of Volga
Bulgaria"**, and that is right: the Bulgar ruler's title in the Arabic sources
is amīr/malik, and vanilla itself styles the mod's small Muslim states this way.
No override needed.

### F.3 If a steppe entity is wanted anyway

Should the user overrule §2 below and want a Kipchak state, the honest shape is
`government = { type = steppe_horde }` at `rank_kingdom`, giving **"the Kipchak
Horde"** with ruler **"Khān"** — which is, ironically, the correct rendering.
The costs are exact and both must be paid:

1. The tag's NAME key becomes dead weight; only `TAG_ADJ` is read. Anyone later
   editing `KIP:` will see no effect and no error.
2. `tools/build_setup.py:3571-3573` must be relaxed. The safe relaxation is an
   explicit allow-list — `_HORDE_RECIPIENTS_OK = {"KIP"}` subtracted from
   `_bad_recip` — with a comment naming the reason, mirroring how the British
   slice narrowed the same assert from tribes to hordes only
   (`tools/build_setup.py:3528-3537`). A blanket removal throws away a guard
   that has already earned its keep.

---

## G. Diplomacy (`build_diplomacy`)

**REMOVE — twelve 1337 Chagatai-ulus lines** (`main_menu/setup/start/12_diplomacy.txt`
in the current build, lines 493-505):
```
CHG -> BKH, BRL, DGH, JLY, KRG, KTT, QCH, QUN, SLD, YSU   (vassal x10)
DGH -> MNL, DGH -> SRL                                     (vassal x2)
```
Ten of these die automatically anyway once CHG goes landless (the landless-dep
auto-strip, `docs/HANDOFF.md:474-479`), but the exact-count constant must be
moved deliberately — the strip asserts its own number.

**LEAVE ALONE for now:** GLH's fifteen dependencies (BIA BLD HTN HSC IAS SRC SSI
BRY HAL KIE VOL as tributaries; AVR LEK SMS TRK as vassals, `12_diplomacy.txt:88-100,
261-264`). Every one of them is a Rus or Caucasus subject — the Rus/steppe
package's, and GLH stays landed in this slice so they do not auto-strip.

**ADD — the Karakhanid family tie.** The two kaghanates were one house and the
eastern branch held formal seniority in the 1040s-60s [D], but they also fought
each other (1057-59). Modelling them as independent equals is the safe reading
and is what I recommend: **no new dependency**. If a tie is wanted, the shape is
`dependency = { first = QRA second = QRK subject_type = tributary }` and it
would need a `karakhanid_khutba_reform` on QRA granting
`allow_tributary_subject` — the proven route (`docs/HANDOFF.md:534-538, 568-571`,
`in_game/common/government_reforms/zz_1066_reforms.txt`). OPEN DECISION 4.

**KTT** currently sits under CHG. Once that line is stripped it is independent.
A Karakhanid tributary ring over KTT/BKH/KRG/SRL is available on the same
khuṭba-reform pattern; I do not recommend it without better evidence than I have
(these mountain principalities' 1066 allegiances are genuinely unrecorded).

---

## H. Left alone deliberately

| what | why |
|---|---|
| **SEL's 463 locations, including all of Khwarazm** (`kath`/`khiva`/`uzboy` provinces, 16 locations) | Fixed constraint AND correct: the Khwarazmshahs were **Seljuk appointees** at 1066 — the Anushtegenid line that later becomes the Khwarazmian Empire begins with Anushtegin Gharchai, a Seljuk cupbearer, appointed governor c.1077 [D]; in 1066 Khwarazm is administered directly for Alp Arslan. **Nothing to propose. The Oxus border stands.** |
| **`astrakhan_area` (37, GLH)** | Straddles the Volga; the Saqsin question (the Oghuz-Khazar successor town at the Volga mouth, c.1050-1229) belongs with the Pontic/Khazar seam, not with Transoxiana. Rus/steppe package. |
| **PRM (64) and VYT (20)** | Kama and Vyatka, west/north of my line and inside the Rus orbit. VYT is in fact an ANACHRONISM at 1066 — the Vyatka Land is a late-12th-century Novgorodian colony — but retiring it is the Rus package's call, not mine. Flagged, not touched. |
| **QCH (29), MNL (7), SRL (4), TRH (6), OGE (19)** | Qocho is genuinely right for 1066 — the Uyghur Kingdom of Qocho ran 843-1132, Buddhist, at Turfan/Beshbalik, and vanilla already gives it `uyghur_culture` + `mahayana` templates. MNL (Aksu/Kucha) is a Mongol-era name on land that was Uyghur or Karakhanid in 1066 and is the cleanest candidate for a later Xinjiang tidy. TRH/OGE are Altai/Irtysh and belong to a Siberia/Mongolia review. |
| **BKH (18), KRG (5)** | Badakhshan and Karategin were real mountain principalities with their own lines through the 11th century; leaving them independent is defensible and cheap. Their 1337 religion (`mahayana` on the Pamir) is a pop-phase problem, not a territory one. |
| **HLG's `kazimah`** | The Arabia slice's, explicitly (`docs/HANDOFF.md:971-972`). |
| **QUN's `asadabad_kunar`, `hajiabad`, `parun`** | `upper_indus_area`, Kunar/Nuristan — an Afghan/India-review matter. Named here so it is not re-discovered. |
| **The Pecheneg/Cuman world west of the Volga** | Rus/steppe package, per the brief. |
| **Pops, cultures, religions everywhere in this theater** | Separate phase by user decision (`docs/HANDOFF.md:1047-1050`). Note for that phase: `balasagun` templates as `kyrgyz_culture` + **`tengri`**, which is wrong for a Muslim Karakhanid capital; `bolghar`/`bilyar`/`kazan` template as `kazani`, the Kipchak successor culture. |

---

## OPEN DECISIONS

**1. "Sultanate of the Kara-Khanids" or a Khanate branch?**
A Muslim monarchy at kingdom rank renders "Sultanate"/"Sultan"
(`government_names_l_english.yml:463-464`). The Karakhanids were khaqans.
The only tag-safe fix is a whole-file override of `country_ranks.txt` with
tag-gated branches, which is also the already-parked fix for SEL.
**Recommendation: accept "Sultanate" in this slice; fold QRK/QRA into the
banked Muslim-styling pass so one override serves all three.**

**2. Does the Kipchak steppe get a state?**
Historically the Desht-i Kipchak in 1066 had no khan, no capital and no
attested ruler — the Kimek khaganate on the Irtysh had just dissolved and the
Cumans were only beginning to press the Rus frontier (first contact 1055,
first major raid 1061). The project's own precedent is decisive: **the
Pechenegs got NO tag, and a state is EARNED by later events**
(`docs/HANDOFF.md:950-955`). **Recommendation: NO Kipchak tag. Vacate Tier A
(168 locations) to unowned steppe.** If overruled, §F.3 has the exact horde
shape and the exact assert relaxation; `QPQ` is a verified-free tag.

**3. One Karakhanid house or two branch houses?**
**Recommendation: one — `qarakhanid_dynasty`, loc "Qarakhanid".** The two tags
already carry the split. Two-branch version is drafted in §D if wanted.

**4. Any tie between QRK and QRA?**
**Recommendation: none — two independent kaghanates.** They fought in 1057-59.
A QRA→QRK tributary is available on the proven khuṭba-reform route if the user
prefers a formal senior/junior pair.

**5. Where does the Ferghana / Chach / Isfijab block go?** [D]
This package puts Chach (Tashkent), Isfijab, Ferghana, Otrar and Turkestan with
the EAST (QRA), on the Syr Darya reading of the 1040s division, and because
Uzgend in `andijan_province` was the eastern branch's own old seat. The
authorities genuinely differ and Ferghana changed hands more than once.
Moving those five provinces west instead makes it **QRK 75 / QRA 113** rather
than **QRK 46 / QRA 142**. **Recommendation: keep as drafted (Syr Darya line).**

**6. BLH's `culture_definition`: `bolghar_culture` or `kazani`?**
`bolghar_culture` is historically right and exists in vanilla; `kazani` is what
the pops actually are until the pop phase. **Recommendation:
`bolghar_culture`** — it matches the al-Andalus decision the user already made.
Note the standing question of whether `culture_definition` even matters for a
LANDED tag (`docs/HANDOFF.md:986-988`) is still unanswered in game.

**7. `heir_selection`: `cognatic_primogeniture` or `partition_inheritance`?**
`partition_inheritance` is legal for monarchy
(`VAN/in_game/common/government_types/00_default.txt:7`) and is literally the
Karakhanid appanage system that split the realm in the 1040s. It is also
unmeasured in this project and could shatter the AI's Karakhanids early.
**Recommendation: ship `cognatic_primogeniture`; bank `partition_inheritance`
as a flavor probe for a later launch, on QRA alone first.**

**8. `astrakhan_area` — mine or the Rus/steppe package's?**
37 GLH locations on both banks of the lower Volga. **Recommendation: theirs.**
It is one object with the Pontic steppe and with the Saqsin/Khazar question.

**9. West Siberia (Tier B, 116 GLH locations) — this slice or a later one?**
The Golden Horde holding Tomsk and Surgut at 1066 is absurd, and vacating them
costs nothing extra once the mechanism exists. But it is a long way from
Transoxiana and a Siberia review may want those locations for Ugrian tribal
tags rather than empty. **Recommendation: INCLUDE Tier B** — empty is strictly
closer to the truth than Golden Horde, vanilla already ships 34 unowned
locations inside the same areas, and a later slice can fill empty land far more
easily than it can take it off a horde.

**10. `LOCATION_VACATED` — approve the new build mechanism?**
This slice cannot be built without a way to make land unowned (§E.2). It is a
small, self-asserting addition modelled on `LOCATION_GRANTS`, and the state it
produces is vanilla-attested 7334 times. **Recommendation: approve, and prove
it by breaking — a bogus location must abort, and disabling the removal must be
caught by the ownership validate, the same two break tests the Sardinia grants
passed (`docs/HANDOFF.md:366-369`).**

**11. CHG's Dzungarian 15 — vacate or hand to QCH?**
`urumqi manas bortala jing kuytun urghtbulaq usu_xinjiang utbulaq zhekdeliq
yangjibaliq kutubi ulan_us qanbalik hoboksar gonganbao`. QCH (Uyghur Qocho)
already holds Beshbalik and Turfan next door. **Recommendation: vacate** —
Qocho's real reach north of the Tian Shan in 1066 is not something I can
source, and QCH belongs to the Xinjiang/China review anyway.

**12. QRA's displayed name: `name_mahmud` or the literal `Toghrul`?**
Both exist in vanilla and neither needs a loc row of ours.
**Recommendation: `name_mahmud`** (the personal name), with a comment noting
the throne-name alternative and the Alp Arslan precedent for preferring it.
