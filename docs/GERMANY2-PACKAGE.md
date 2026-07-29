# GERMANY II — approved implementation package (2026-07-29 night)

USER DECISIONS (final, do not reopen): SWA = the 21-location version.
Bishops = ALL 15 sees. Godfrey = TWO seats (BLL + SPL, one character,
the attested pluralist route). FLA takes the 7 Artois locations.
Main-session decisions: SAX+SWA registered via formable reuse; FKN NOT
registered; LUX gets a NEW ardennes_luxembourg_dynasty; UTR takes the
3-location Groningen move only (FRI keeps the peasant republic);
mortality drift (Einhard 1067.2, Benno 1067.12, Otto 1067, Egbert
1068.1) is ACCEPTED — flavor-event material later, no engine fix.

## A. Registry additions (in_game/setup/countries/zz_1066_new_countries.txt)

Append, with a comment noting the formable-reuse ground (vanilla ships
49 tags that are simultaneously formables and live countries; Paradox's
own `tag = LUN # Should be SAX` at vanilla 05_characters.txt:86620):

SAX = {
	color = map_SAX
	color2 = rgb { 16 41 202 }

	culture_definition = lower_saxon
	religion_definition = catholic
}

SWA = {
	color = map_SWA
	color2 = rgb { 16 41 202 }

	culture_definition = swabian
	religion_definition = catholic
}

map_SAX = vanilla named_colors/02_map.txt:243; map_SWA = :249 — both
vanilla names, so NO new entries in zz_1066_map_colors.txt for them.
lower_saxon = LUN's registry culture (north_germany.txt:747); swabian =
AUG/AGC's (south_germany.txt:49/56).

## B. New 10_countries blocks (NEW_COUNTRIES in build_setup.py, ZAH's shape)

Both: starting_technology_level = 3, include = "expl_western_europe",
include = "catholic_monarchy_no_coast", include = "german_principality",
country_rank = rank_duchy.
- SAX: capital = luneburg
- SWA: capital = ulm
(Check ZAH's actual generated block first and mirror it exactly —
whatever ZAH's block carries beyond the above, SAX/SWA carry too.)

## C. Ruler table — HISTORICAL_RULERS rows + NEW_CHARACTERS

Age >= 16 at 1066.9.15 holds for every row. Birthplace: use the
capital/see location unless noted; verify every birthplace exists in
definitions.txt. [U] on birth years is normal — enter the year given.

### Tier A
| tag | character key | name key | accession | birth | regnal | dynasty |
|---|---|---|---|---|---|---|
| SWA | swa_rudolf_rheinfelden | name_rudolf (vanilla :15318) | 1057.1.1 | 1025.1.1 | 1 | rheinfelden_dynasty NEW |
| SAX | sax_ordulf_billung | name_ordulf INVENT "Ordulf" | 1059.6.29 | 1020.1.1 | 1 | billung_dynasty NEW |
| KOL | kol_anno_ii | name_anno INVENT "Anno" | 1056.1.1 | 1010.1.1 | 2 | steusslingen_dynasty NEW |
| TRI | tri_udo_nellenburg | name_udo INVENT "Udo" | 1066.6.1 | 1030.1.1 | 1 | nellenburg_dynasty NEW |
| BLL | bll_godfrey_iii_bearded | name_godfrey (:8050; .german_language "Gottfried" :8064) | 1065.1.1 | 997.1.1 | 3 | ardennes_dynasty NEW |
| SPL | SAME character bll_godfrey_iii_bearded | — | 1057.1.1 | — | 3 | — |

SPL is the SAME character seated on a second tag (the pluralist route:
vanilla's boh_john_luxembourg sits on BOH+LUX — KNOWLEDGE.md records
it). One character entry, two HISTORICAL_RULERS rows, one ruler_term
per tag. Check how the build's per-entry validation counts characters
vs terms — the exact-count asserts will need the distinction (terms =
rows, characters = unique keys).

### Tier B
| tag | character key | name key | accession | birth | regnal | dynasty |
|---|---|---|---|---|---|---|
| MEI | mei_otto_weimar | name_otto (:13603) | 1062.1.1 | 1020.1.1 | 1 | weimar_dynasty NEW |
| LUX | lux_conrad_i | name_conrad (:4901) | 1059.1.1 | 1040.1.1 | 1 | ardennes_luxembourg_dynasty NEW |
| HAI | hai_baldwin_i_hainaut | name_baldwin (:2813) | 1051.1.1 | 1030.1.1 | 1 | flanders_dynasty (MOD's own, reuse) + father = fla_baldwin_v_flanders (the Ayyub/Tamim cross-tag precedent) |
| UTR | utr_william_i | name_william (:18209) | 1054.1.1 | 1015.1.1 | 1 | none (bishop) |
| LIE | lie_theodwin | name_theoduin INVENT "Theoduin" | 1048.1.1 | 1000.1.1 | 1 | none (bishop) |

### Tier C — all 15 sees (bishops carry NO dynasty line unless noted; the mai_siegfried_i precedent)
| tag | see | character key | name key | accession | birth |
|---|---|---|---|---|---|
| BRE | Hamburg-Bremen | bre_adalbert_goseck | name_adalbert INVENT "Adalbert" | 1043.1.1 | 1000.1.1 | dynasty goseck_dynasty NEW |
| MAG | Magdeburg | mag_werner_steusslingen | name_werner (:18122) | 1064.1.1 | 1020.1.1 | dynasty steusslingen_dynasty (same house as Anno) |
| WBG | Würzburg | wbg_adalbero | name_adalbero INVENT "Adalbero" | 1045.1.1 | 1010.1.1 |
| BAM | Bamberg | bam_herman_i | name_herman (:8830, german "Hermann") | 1065.1.1 | 1025.1.1 |
| HDH | Hildesheim | hdh_hezilo | name_hezilo INVENT "Hezilo" | 1054.1.1 | 1020.1.1 |
| HBS | Halberstadt | hbs_burchard_ii | name_burchard (:3939) | 1059.1.1 | 1028.1.1 |
| MUN | Münster | mun_friedrich | name_frederick (:7376) | 1063.1.1 | 1025.1.1 |
| PDB | Paderborn | pdb_imad | name_imad INVENT "Imad" | 1051.1.1 | 1010.1.1 |
| SLZ | Salzburg | slz_gebhard | name_gebhard (:7704) | 1060.1.1 | 1010.1.1 |
| PSS | Passau | pss_altmann | name_altmann INVENT "Altmann" | 1065.1.1 | 1015.1.1 |
| EIC | Eichstätt | eic_gundekar_ii | name_gundekar INVENT "Gundekar" | 1057.1.1 | 1019.1.1 | regnal 2 |
| KNZ | Constance | knz_rumold | name_rumold INVENT "Rumold" | 1051.1.1 | 1010.1.1 |
| SPY | Speyer | spy_einhard | name_einhard INVENT "Einhard" | 1060.1.1 | 1015.1.1 |
| OSN | Osnabrück | osn_benno_i | name_benno INVENT "Benno" | 1052.1.1 | 1010.1.1 |
| REG | Regensburg | reg_otto_riedenburg | name_otto (:13603) | 1060.1.1 | 1020.1.1 |

Regnal numbers: KOL 2, EIC 2, MEI 1... enter what the table says; where
blank use 1 for I, 2 for II per the ruler's numeral; BAM Herman I = 1,
HBS Burchard II = 2, OSN Benno I = 1, HDH/WBG/LIE etc. no numeral
tradition for bishops in vanilla — check how the mod seated MAI
Siegfried I and PAP and follow that shape exactly (regnal + optional
regnal_name).

### Tier D
| tag | character key | name key | accession | birth | regnal | dynasty |
|---|---|---|---|---|---|---|
| SOR | sor_dedi_i | name_dedi INVENT "Dedi" | 1046.1.1 | 1004.1.1 | 1 | wettin_dynasty (VANILLA 04_dynasties.txt:4068 — reuse, historically exact) |
| PAL | pal_hermann_ii | name_herman (:8830) | 1064.1.1 | 1049.1.1 | 2 | ezzonen_dynasty NEW |
| BRU | bru_egbert_i | name_egbert (:6137 — free win; name_ekbert does NOT exist) | 1057.1.1 | 1025.1.1 | 1 | brunonen_dynasty NEW |

PAL is 17 at start — check the mod's MINOR_RULERS/under-18 handling
(HOL Dirk V at 14 was entered; follow that precedent).

## D. Dynasties (main_menu/setup/start/04_zz_1066_dynasties.txt)

NEW (verify each name/home; homes must be locations in definitions.txt):
rheinfelden_dynasty home mullheim (vanilla's own stand-in: 05_characters.txt:84031 "birth = mullheim #Rheinfelden")
billung_dynasty home luneburg
steusslingen_dynasty home riedlingen
nellenburg_dynasty home stockach
ardennes_dynasty home bouillon
weimar_dynasty home weimar
brunonen_dynasty home brunswick
ezzonen_dynasty home cochem
ardennes_luxembourg_dynasty home luxembourg
goseck_dynasty home weissenfels
Each needs a dynasty loc row (follow babenberg/zahringen rows in
1066_norman_conquest_l_english.yml). ardennes_luxembourg_dynasty's
display name: "Luxemburg".

## E. Invented name keys (loc — the taifa key mechanism, NOT bare literals)

name_ordulf "Ordulf", name_anno "Anno", name_udo "Udo",
name_theoduin "Theoduin", name_adalbert "Adalbert",
name_adalbero "Adalbero", name_hezilo "Hezilo", name_imad "Imad",
name_benno "Benno", name_altmann "Altmann", name_gundekar "Gundekar",
name_rumold "Rumold", name_einhard "Einhard", name_dedi "Dedi".
All 14 verified missing across the entire vanilla localization tree.
One loc row each, single physical line, in the mod's existing loc file
next to the earlier invented keys.

## F. Territory (grants + landless), exactly these lists

_GERMANY_GRANTS = {
    "SAX": ["luneburg","celle","dannenberg","ebstorf","fallingbostel",
            "harburg","isenhagen","luchow","uelzen","winsen","winsen_aller"],  # all 11 from LUN
    "SWA": ["stuttgart","backnang","calw","goppingen","nagold",
            "oberndorf","riedlingen","sigmaringen","urach","welzheim",  # WUR 10
            "ulm",            # ULM
            "tubingen",       # TUB
            "helfenstein",    # HLF
            "heidenheim",     # HEH
            "oettingen","vaihingen",  # OET
            "hohenberg","horb",       # HHB
            "erbach_swabia","illereichen",  # KIR
            "waldburg"],      # WDB
    "BRE": ["bremen","hamburg"],          # BRM, HAM (free cities are 1186/1189)
    "FLA": ["arras","bapaume","bethune","calais","hesdin","lens","saint_omer"],  # ARS
    "UTR": ["groningen","appingedam","wedde"],  # from FRI (partial on purpose)
}
GERMANY_LANDLESS = ("LUN","WUR","ULM","TUB","HLF","HEH","OET","HHB",
                    "KIR","WDB","ARS","HAM","BRM")
Each landless tag keeps its registry identity and its former holdings
become claims (the GRA/POR/MLL landless-with-irredenta shape the build
already automates via LANDLESS_AFTER/_landless_claims).
NOTE: donor lists must be verified against the CURRENT build's actual
holdings (the AQN 43-vs-31 lesson: foreign-held locations in a sweep).
These lists are explicit singles, so verify each location's current
owner before granting; if an owner differs from the comment, STOP and
report rather than granting.

## G. IO surgery (build_ios) — HARD DEPENDENCY

1. Elector swap: the secular elector list currently `BOH BRA LUN UBV`
   (our 15_IO line 94) becomes `BOH BRA SAX UBV`. Same commit as LUN
   emptying or the landless sweep silently eats an elector.
2. HRE members: add SAX and SWA; the landless sweep will drop
   LUN/WUR/ULM/TUB/HLF/HEH/OET/HHB/KIR/WDB/ARS/HAM/BRM from members
   and every status list automatically — but the exact-multiset assert
   on stripped entries WILL move; observe the new count and update the
   constant (observed-then-moved, never predicted).

## H. FIELD_FIXES / CAPITAL_FIXES

FIELD_FIXES (block-level, 1066-wrong dynasties on tags this slice seats):
  BRU: dynasty = welfen_dynasty -> dynasty = brunonen_dynasty
  MEI: dynasty = wettin_dynasty -> dynasty = weimar_dynasty
  PAL: dynasty = wittelsbach_dynasty -> dynasty = ezzonen_dynasty
  BLL: country_rank = rank_county -> country_rank = rank_duchy
LUN keeps welfen_dynasty on its landless shell (the Welf future);
WUR keeps wurttemberg_dynasty likewise. Verify each old string exists
in the tag's current block before adding the fix (exact-match rule).
CAPITAL_FIXES: PAL heidelberg -> kaiserslautern (Heidelberg first
attested 1196; Kaiserslautern is a Salian palace PAL already holds).

## I. Left alone DELIBERATELY (write nothing, but keep in the report)

FKN stays a formable (no 1066 duke; ducal authority is the king's own).
HES/THU/GEL/JUL/BRG/KLE/GMK and every Tier-E tag stay ruler = random.
NAM (Albert III from 1063 [U]) is the one Tier-E promotion candidate if
a second source ever appears. LBB/LUB/BRC are banked for the Baltic and
Bavaria passes. Einhard/Benno/Otto/Egbert die within 18 months of
start — accepted drift, flavor material.
