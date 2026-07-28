#!/usr/bin/env python3
"""Phase 1 — generate the setup files that carry 1337-dated people and dates.

The 1066 start inherits vanilla's 1337 setup, which is wrong in one specific,
mechanical way: its dates are all in the future. The engine rejects those
entries, collapses them to `1.1.1`, seats rulers born around 1312 who display at
about -250 years old, and — measured — floods error.log with tens of thousands
of script errors once the game runs. See docs/KNOWLEDGE.md.

This script removes the dated parts and leaves everything else byte for byte as
vanilla has it. Rulers become `ruler = random`, which is how a published
conversion solves the same problem. Phase 2 then puts real rulers back as TWO
lines — `ruler = <key>` plus an OPEN ruler_term (no end_date, accession before
START_DATE) — because a named ruler does not seat without one: measured in
game 2026-07-28, five named-ruler countries all under engine-generated regents
until the terms were added. See docs/KNOWLEDGE.md.

The outputs are GENERATED. Do not hand-edit them: re-run after a game patch and
the mod picks up the new vanilla data. Phase 2 layers real historical rulers on
top via HISTORICAL_RULERS, so history is added to a regenerable base rather than
replacing it.

Usage:
    python tools/build_setup.py            # write the files
    python tools/build_setup.py --dry-run  # report only, write nothing
"""
import os, re, sys

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP = os.path.join("main_menu", "setup", "start")

# ---------------------------------------------------------------- vanilla ---
_PROBE = os.path.join("in_game", "map_data", "definitions.txt")

def _usable(p):
    return p is not None and os.path.isfile(os.path.join(p, _PROBE))

VAN = os.environ.get("MR_VANILLA")
if VAN and not _usable(VAN):
    sys.exit(f"MR_VANILLA is set but has no {_PROBE} under it: {VAN}")
if not VAN:
    _candidates = [
        r"E:\SteamLibrary\steamapps\common\Europa Universalis V\game",
        os.path.join(os.path.dirname(MOD), "EU5-Vanilla", "game"),
    ]
    VAN = next((p for p in _candidates if _usable(p)), None)
if not VAN:
    sys.exit("vanilla reference tree not found — see CLAUDE.md, REQUIRED SETUP")

# ------------------------------------------------------------- Phase 2 ---
# tag -> (character key, accession date, regnal number).
# Anything not listed keeps `ruler = random`.
#
# TWO lines are written per entry: `ruler = <key>` plus an OPEN ruler_term —
# no end_date, start_date = accession. Both are required: a named ruler does
# NOT seat without an open term whose start_date is before START_DATE.
# Measured in game 2026-07-28: with `ruler =` alone, all five countries below
# started under engine-generated regents while every `ruler = random` country
# seated fine. Anno 1644 ships the same two-line shape for every named ruler,
# and vanilla's own terms are the same one-line form (10_countries.txt:75).
# See docs/KNOWLEDGE.md.
#
# Every entry is checked: the character must exist in the generated
# 05_characters.txt, be at least ADULT_AGE at START_DATE, and accede between
# birth and START_DATE. A typo here does not error in game — it leaves an
# empty throne and an engine-generated regent — so the checks below are the
# only thing that catches one.
# Accession dates are well-known history, entered from general knowledge.
HISTORICAL_RULERS = {
    # North Sea, 1066. All four already exist in vanilla, which ships regnal
    # chains back to 886 and 188 characters who are adults in 1066.
    "ENG": ("eng_harold_godwinson", "1066.1.6", 2),       # Harold II, crowned the day after Edward the Confessor died; d. 1066.10.14 at Hastings
    "NRM": ("eng_william_the_conquerer", "1035.7.2", 2),  # William II as Duke of Normandy; rank_duchy, capital rouen
    "DAN": ("dan_sweyn_estridsson", "1047.10.25", 2),     # Sweyn II, sole King of Denmark at Magnus the Good's death
    "SCO": ("sco_malcolm_iii", "1058.3.18", 3),           # Malcolm III, crowned at Scone
    "NOR": ("nor_harald_hardrada", "1046.1.1", 3),        # Harald III, co-king from 1046; written below — vanilla has no Norwegian alive in 1066

    # France, 1066 — from the France research pass (docs/KNOWLEDGE.md).
    # 18 rulers below already exist in vanilla; five are authored in
    # NEW_CHARACTERS. Deliberately NOT seated, with the reasons recorded:
    # CHP/SAN (Theobald already seats BLS), POI (William VIII seats AQN),
    # BAR (the titleholder was Countess Sophie, no character; Louis of
    # Montbeliard seats his own MTB), MTZ (Gerard already seats LOR),
    # MIE (Norman-occupied, disputed), TOU (landless at 1337 — waits for
    # the border work), and the four low-confidence drafts (MRT, EVR,
    # NEV, ANG — second source needed).
    "FRA": ("fra_philippe_i_capet", "1060.8.4", 1),       # Philip I, aged 14 — MINOR_RULERS; France under Baldwin of Flanders' regency, which the engine's regency represents
    "BUR": ("bur_robert_i_burgundian", "1032.1.1", 1),    # Robert I the Old, Duke of Burgundy
    "BLS": ("chp_thibault_i_blois", "1037.11.15", 3),     # Theobald III of Blois (also I of Champagne — seated here only)
    "MTB": ("mtb_louis_scarpone", "1042.1.1", 1),         # Louis of Montbeliard
    "LOR": ("lor_gerard_alsace", "1048.11.11", 1),        # Gerard of Alsace (also Count of Metz — seated here only)
    "AUV": ("auv_robert_ii_auvergne", "1064.1.1", 2),     # Robert II of Auvergne
    "FOI": ("foi_roger_ii_foix", "1064.1.1", 2),          # Roger II of Foix — EXACTLY 16 at start, no margin
    "FCB": ("fcb_guillaume_i_burgundy", "1057.9.4", 1),   # William I, Count Palatine of Burgundy
    "DAU": ("dau_guigues_i_albon", "1034.1.1", 1),        # Guigues I of Albon
    "SAV": ("sav_pierre_i_savoy", "1060.1.1", 1),         # Peter I of Savoy
    "PER": ("per_audebert_ii_perigord", "1044.1.1", 2),   # Audebert II of Perigord
    "MRC": ("mrc_adalbert_ii_lamarche", "1047.1.1", 2),   # Adalbert II of La Marche
    "VNT": ("vnt_ebles_i_de_ventadour", "1060.1.1", 1),   # Ebles I of Ventadour
    "AMG": ("amg_geraud_ii_armagnac", "1063.1.1", 2),     # Geraud II of Armagnac
    "AST": ("ast_guillaume_astarac", "1023.1.1", 1),      # William of Astarac
    "COM": ("com_arnaud_iii_comminges", "1035.1.1", 3),   # Arnaud III of Comminges
    "IJO": ("ijo_raymond_lisle_jourdain", "1038.1.1", 1), # Raymond of L'Isle-Jourdain
    "MON": ("mon_simon_i_montfort", "1053.1.1", 1),       # Simon I of Montfort
    "BRI": ("bri_conan_ii_rennes", "1040.10.1", 2),       # Conan II of Brittany — NEW_CHARACTERS
    "ANJ": ("anj_geoffroy_iii_gatinais", "1060.11.14", 3),# Geoffrey III of Anjou — NEW_CHARACTERS
    "FLA": ("fla_baldwin_v_flanders", "1035.5.30", 5),    # Baldwin V of Flanders — NEW_CHARACTERS
    "AQN": ("aqn_guilhem_viii_poitiers", "1058.1.1", 8),  # William VIII of Aquitaine (VI of Poitou) — NEW_CHARACTERS
    "BGN": ("bgn_eustache_ii_boulogne", "1049.1.1", 2),   # Eustace II of Boulogne — NEW_CHARACTERS

    # Empire, 1066 — the clean batch from the Empire research pass. The
    # CROWN is deliberately NOT seated: Heinrich IV's OGK tag is landless
    # and the emperor needs a royal demesne first (HANDOFF, open decision).
    # Also held back: Swabia/Saxony (no usable tags), KOL/TRI (name keys
    # missing), CRH/MEI/LUX/HAI/UTR/LIE (unverified dates or disputes).
    "BOH": ("boh_vratislav_ii_premyslid", "1061.1.1", 2), # Vratislav II, Duke of Bohemia — NEW_CHARACTERS
    "UBV": ("ubv_otto_von_nordheim", "1061.1.1", 2),      # Otto of Nordheim, Duke of Bavaria; regnal II is the common attribution, unverified
    "HOL": ("hol_dirk_v", "1061.1.1", 5),                 # Dirk V of Holland, aged 14 — MINOR_RULERS
    "MAI": ("mai_siegfried_i", "1060.1.1", 1),            # Siegfried I, Archbishop of Mainz
    "BRB": ("brb_henry_ii_louvain", "1054.1.1", 2),       # Henry II of Louvain; accession sources differ (1054 vs c.1062) — earlier date entered

    # The East and Iberia, 1066 — every accession below is vanilla's OWN
    # ruler_term data (file:line in KNOWLEDGE.md); all five characters ship
    # in vanilla. Held back with reasons recorded: LON/GLC/CAT (landless at
    # 1337, the brothers' realms wait for the Iberian territory pass), GRA
    # and the 13 other taifas plus the Great Seljuks (invent-a-country
    # work), TRE/CIL/CYP/CRT/BUL (Byzantine themes — territory pass).
    "BYZ": ("byz_konstantinos_x_doukas", "1059.11.23", 10), # Constantine X Doukas; d. 1067.5.23 is SCRIPT work, not data
    "GEO": ("geo_bagrat_iv", "1027.8.16", 4),             # Bagrat IV of Georgia
    "CAS": ("cas_sancho_ii_jimena", "1065.12.27", 2),     # Sancho II of Castile — king for nine months at start
    "NAV": ("nav_sancho_iv_jimena", "1054.9.1", 4),       # Sancho IV of Navarre
    "ARA": ("ara_sancho_i_aragon", "1063.5.8", 1),        # Sancho Ramirez of Aragon

    # The North and East, 1066 — from the North/East research pass. Five
    # ride free on vanilla characters (the Rus triumvirate, the Sorcerer,
    # and Sweden, where vanilla's own term seats Halsten from 1066.1.1 and
    # Stenkil is unseatable, dead 1066.1.1); four are authored below.
    # NOT seated, reasons recorded: Pereyaslavl (NO tag — PER is Perigord!,
    # PZL the wrong city; invent-a-country #3), ICE (kingless Commonwealth),
    # the Baltic/Wendish/Yoke-era layers (territory pass; and no Slavic
    # pagan religion exists to give the Obodrites).
    "SWE": ("swe_halsten", "1066.1.1", 1),                # Halsten Stenkilsson — vanilla's own succession
    "KIE": ("kie_iziaslav_rurikovich", "1054.2.20", 1),   # Iziaslav I of Kyiv, the senior triumvir
    "NOV": ("nov_mstislav_izyaslavich_rurikovich", "1054.2.20", 1), # Mstislav, Iziaslav's son, in Novgorod
    "CHR": ("kie_sviatoslav_ii_rurikovich", "1054.2.20", 1), # Sviatoslav II in Chernihiv (I of Chernihiv, II of Kyiv later)
    "POK": ("pok_vseslav_bryachislavich_rurikovich", "1044.1.1", 1), # Vseslav the Sorcerer of Polotsk; accession year [U]
    "POL": ("pol_boleslaw_ii_szczodry_piast", "1058.11.28", 2), # Boleslaw II the Bold, DUKE until 1076 — NEW_CHARACTERS
    "HUN": ("hun_salamon_arpad", "1063.9.11", 1),         # Solomon, aged 13 — MINOR_RULERS — NEW_CHARACTERS
    "CRO": ("cro_petar_kresimir_iv", "1058.1.1", 4),      # Petar Kresimir IV — NEW_CHARACTERS
    "ORK": ("ork_paul_thorfinnsson", "1065.1.1", 1),      # Paul Thorfinnsson, joint earl with Erlend (seat-once) — NEW_CHARACTERS

    # The Islamic South, 1066 — the small [U]-flagged batch from the
    # Levant/Africa research pass; birth years are estimates throughout.
    # Parked as invent-a-country slice #4, reasons in KNOWLEDGE: Fatimid
    # Egypt (MAM's ungated rank branch), Abbasids+Great Seljuks (one job),
    # Aleppo/Damascus (no tags), Mecca (low confidence).
    "YEM": ("yem_ali_al_sulayhi", "1047.1.1", 1),         # Ali al-Sulayhi, the Ismaili rising; capital fix (zabid->sana) waits for territory — NEW_CHARACTERS
    "TUN": ("zir_tamim_ibn_al_muizz", "1062.1.1", 1),     # Tamim the Zirid, mid-Hilalian catastrophe; Hafsid rank styling auto-drops (dynasty-gated) — NEW_CHARACTERS
    "TFL": ("alm_abu_bakr_ibn_umar", "1056.1.1", 1),      # Abu Bakr ibn Umar, Almoravid amir (Yusuf ibn Tashfin authored for the ~1072 handover) — NEW_CHARACTERS

    # The Celtic world, 1066 — from the Celtic research pass. Vanilla's own
    # high_kingship IO chain (15_IO :303, stripped by our IO pass) names
    # Diarmait High King from 1064.8.22; seeding a CHARACTER-type IO leader
    # is an open probe recorded in KNOWLEDGE. Parked: all six Welsh
    # kingdom tags (landless claimant shells), Mann and Tyrone (disputed),
    # the Irish territory pass (38 tags on 96 locations).
    "LEI": ("lei_diarmait_mac_mail_na_mbo", "1042.1.1", 1), # Diarmait mac Mael na mBo, King of Leinster (and High King since 1064)
    "MCM": ("mcm_toirdelbach_ua_briain", "1063.1.1", 1),  # Toirdelbach Ua Briain, King of Munster; Donnchad deposed 1063, d. 1064.8.22
    "CNN": ("cnn_aed_in_gai_bernaig", "1046.1.1", 1),     # Aed in Gai Bernaig of Connacht, [U] dates — NEW_CHARACTERS
}

# Tags whose 1066 ruler was HISTORICALLY a minor. The adult-age check skips
# them — the engine gives them a regency, which is the history (France was
# governed by Baldwin V of Flanders as regent). The check still fails if a
# listed tag's ruler turns out to be an adult, so stale entries cannot rot.
MINOR_RULERS = {"FRA", "HOL", "HUN"}

# Characters vanilla does not ship. Appended inside `character_db`, so vanilla's
# 7236 stay. Two ordering rules, both of which crash rather than error:
# dynasties must already exist in dynasty_manager, and children must come after
# their parents.
#
# Every identifier here was checked against vanilla before it was written:
#   name_harold      in_game/common/languages/00_scandinavia.txt:14
#                    (there is NO name_harald anywhere in the game — vanilla uses
#                    one key for Harald/Harold, as eng_harold_godwinson does)
#   name_magnus      same file, line 18
#   name_olaf        same file, line 20
#   norwegian        in_game/common/cultures/scandinavian.txt:58
#   fairhair_dynasty main_menu/setup/start/04_dynasties.txt — already in vanilla,
#                    home = haugalandet, so no dynasty_manager change is needed
#   ringerike        in_game/map_data/definitions.txt
NEW_CHARACTERS = """
	# --- 1066 Norway ------------------------------------------------------
	# NO death dates on anyone here: they are all alive at start, and a living
	# character must not carry one — the engine reads a post-start death date
	# as invalid and the character starts DEAD, silently (see KNOWLEDGE.md).
	# Historical deaths are noted in comments; the ones that matter to the
	# opening (Stamford Bridge) are the Norman Conquest situation's job.
	#
	# Harald Sigurdsson "Hardrada", king 1046-1066, of the Fairhair line through
	# Sigurd Syr. Historically dies at Stamford Bridge on 25 Sep 1066 — ten
	# days into the campaign. That death is SCRIPTED by the situation, not data.
	nor_harald_hardrada = {
		first_name = { name = name_harold }
		culture = norwegian
		religion = catholic
		birth_date = 1015.1.1
		birth = ringerike
		dynasty = fairhair_dynasty
		tag = NOR
	}

	# Sons, written after their father. They give the succession something real
	# to land on when Hardrada dies; without them Norway would fall to a
	# generated heir. Magnus II historically dies 1069, Olaf III Kyrre 1093 —
	# both left to the engine's own mortality.
	nor_magnus_ii = {
		first_name = { name = name_magnus }
		culture = norwegian
		religion = catholic
		birth_date = 1048.1.1
		birth = nidaros
		dynasty = fairhair_dynasty
		father = nor_harald_hardrada
		tag = NOR
	}

	nor_olaf_iii_kyrre = {
		first_name = { name = name_olaf }
		culture = norwegian
		religion = catholic
		birth_date = 1050.1.1
		birth = nidaros
		dynasty = fairhair_dynasty
		father = nor_harald_hardrada
		tag = NOR
	}

	# --- 1066 France ------------------------------------------------------
	# From the France research pass. Identifiers verified: name keys in
	# character_names_dynamic_l_english.yml (the scripted-name authority —
	# KNOWLEDGE.md), cultures in in_game/common/cultures/french.txt
	# (breton:30, angevin:312, poitevin:339, picard:104) and german.txt
	# (low_franconian:597), birth locations in definitions.txt, dynasties
	# in our additive setup/start/04_zz_1066_dynasties.txt.
	# NO death dates: everyone here is alive on 1066.9.15.

	# Conan II, Duke of Brittany from Alan III's death (1040), effective
	# rule from 1057. Historically dies 1066.12.11 without an heir.
	# name_conan does not exist anywhere; name_conon ("Conon", the
	# French/Occitan pool) is the closest key — vanilla's own BRI regnal
	# block leaves "#Conan = 4" commented out for the same reason.
	bri_conan_ii_rennes = {
		first_name = { name = name_conon }
		culture = breton
		religion = catholic
		birth_date = 1030.1.1
		birth = rennes
		dynasty = rennes_dynasty
		tag = BRI
	}

	# Geoffrey III "le Barbu", Count of Anjou from his uncle Geoffrey
	# Martel's death. Historically deposed by his brother Fulk IV in 1068.
	anj_geoffroy_iii_gatinais = {
		first_name = { name = name_godfrey }
		culture = angevin
		religion = catholic
		birth_date = 1040.1.1
		birth = angers
		dynasty = gatinais_dynasty
		tag = ANJ
	}

	# Baldwin V "of Lille", Count of Flanders, and regent of France for the
	# minor Philip I. Historically dies 1067.9.1. Culture follows the
	# capital (bruges is low_franconian); the court language stays french.
	fla_baldwin_v_flanders = {
		first_name = { name = name_baldwin }
		culture = low_franconian
		religion = catholic
		birth_date = 1012.1.1
		birth = bruges
		dynasty = flanders_dynasty
		tag = FLA
	}

	# William VIII "Guy-Geoffrey", Duke of Aquitaine and Count of Poitou
	# (as William VI). One man, two vanilla tags — seated in AQN only.
	aqn_guilhem_viii_poitiers = {
		first_name = { name = name_william }
		culture = poitevin
		religion = catholic
		birth_date = 1025.1.1
		birth = poitiers
		dynasty = ramnulfid_dynasty
		tag = AQN
	}

	# Eustace II, Count of Boulogne; fought at Hastings on William's side.
	# Accession c. 1049 on Eustace I's death, date approximate.
	bgn_eustache_ii_boulogne = {
		first_name = { name = name_eustathius }
		culture = picard
		religion = catholic
		birth_date = 1015.1.1
		birth = boulogne_sur_mer
		dynasty = boulogne_dynasty
		tag = BGN
	}

	# --- 1066 Empire ------------------------------------------------------
	# From the Empire research pass. Identifiers verified: name keys in the
	# character-names loc registry (vratislav:17812, otto:13603,
	# theodoric:16939, henry:8755, sigfrid:16025), cultures czech
	# (west_slavic.txt, first entry behind the BOM), eastphalian:126,
	# low_franconian:597, rhine_franconian:680 (german.txt), locations and
	# dynasties per file cites below. NO death dates: all alive at 1066.9.15.

	# Vratislav II, Duke of Bohemia from January 1061; King of Bohemia only
	# from 1085. Historically dies 1092.1.14.
	boh_vratislav_ii_premyslid = {
		first_name = { name = name_vratislav }
		culture = czech
		religion = catholic
		birth_date = 1032.1.1
		birth = prague
		dynasty = premyslid_dynasty
		tag = BOH
	}

	# Otto of Nordheim, Duke of Bavaria 1061-1070 (deposed for alleged
	# treason; historically dies 1083.1.11). "Otto II" is the common
	# attribution but no source verified the numeral this pass — flagged,
	# not invented. Birth location: northeim is not on the map; gottingen
	# is the nearest existing location.
	ubv_otto_von_nordheim = {
		first_name = { name = name_otto }
		culture = eastphalian
		religion = catholic
		birth_date = 1020.1.1
		birth = gottingen
		dynasty = northeim_dynasty
		tag = UBV
	}

	# Dirk V, Count of Holland from 1061, FOURTEEN at start — MINOR_RULERS.
	# Historical guardianship of Robert the Frisian; the engine seats minors
	# directly (measured, see the decoder). name_theodoric is vanilla's key
	# for Dirk/Thierry (lor_thierry_ii_lorraine precedent). Historically
	# dies 1091.6.17.
	hol_dirk_v = {
		first_name = { name = name_theodoric }
		culture = low_franconian
		religion = catholic
		birth_date = 1052.1.1
		birth = the_hague
		dynasty = gerulfing_dynasty
		tag = HOL
	}

	# Henry II, Count of Louvain and Brussels (Brabant is not a duchy until
	# 1183). Accession sources genuinely differ — 1054 in one account,
	# c. 1062/63 in others; the earlier date is entered. Historically
	# dies 1078.
	brb_henry_ii_louvain = {
		first_name = { name = name_henry }
		culture = low_franconian
		religion = catholic
		birth_date = 1020.1.1
		birth = leuven
		dynasty = reginar_dynasty
		tag = BRB
	}

	# Siegfried I, Archbishop of Mainz from January 1060 (historically to
	# 1084). No dynasty — the Reginbodonen have none in vanilla, and
	# dynasty-less characters are vanilla-attested. Birth year unknown,
	# c. 1015 entered.
	mai_siegfried_i = {
		first_name = { name = name_sigfrid }
		culture = rhine_franconian
		religion = catholic
		birth_date = 1015.1.1
		birth = mainz
		tag = MAI
	}

	# --- 1066 North and East ----------------------------------------------
	# From the North/East research pass. Identifiers verified: name keys
	# boleslav:3597, salomon:15508, peter:14009, krasimir:10655, paul:13820
	# in the character-names registry; cultures lesser_polish
	# (west_slavic.txt:55), hungarian (carpathian.txt:94), croatian
	# (south_slavic.txt:38), norn_culture (scandinavian.txt:101); dynasties
	# piast (04_dynasties.txt:4175), arpad (:1826); locations krakow,
	# esztergom, knin, orkney in definitions.txt. NO death dates.

	# Boleslaw II "the Bold", Duke of Poland from Casimir I's death
	# (1058.11.28); crowned KING only on Christmas Day 1076. Historically
	# exiled 1079 after executing Bishop Stanislaus — who ships in vanilla
	# (pol_saint_stanislav, alive, 36) for that future situation.
	pol_boleslaw_ii_szczodry_piast = {
		first_name = { name = name_boleslav }
		culture = lesser_polish
		religion = catholic
		birth_date = 1042.1.1
		birth = krakow
		dynasty = piast_dynasty
		tag = POL
	}

	# Solomon, King of Hungary, THIRTEEN at start — MINOR_RULERS. Crowned
	# as a child 1057, sole king from Bela I's death 1063.9.11. His cousin
	# Duke Geza holds the ducatus — the dual-power drama of 1074 is future
	# situation material. name_salomon is the real key; vanilla's own HUN
	# regnal table uses the dead name_solomon (renamed by REGNAL_RENAMES).
	hun_salamon_arpad = {
		first_name = { name = name_salomon }
		culture = hungarian
		religion = catholic
		birth_date = 1053.1.1
		birth = esztergom
		dynasty = arpad_dynasty
		tag = HUN
	}

	# Petar Kresimir IV, King of Croatia and Dalmatia at its greatest
	# extent. Composite first name — the name_x.name_y form has 205 vanilla
	# uses and CRO's own regnal table is written in it (name_kresimir does
	# not exist; name_krasimir is the key). Trpimirovic dynasty is ours —
	# vanilla ships no Croatian royal house.
	cro_petar_kresimir_iv = {
		first_name = { name = name_peter.name_krasimir }
		culture = croatian
		religion = catholic
		birth_date = 1030.1.1
		birth = knin
		dynasty = trpimirovic_dynasty
		tag = CRO
	}

	# Paul Thorfinnsson, Earl of Orkney JOINTLY with his brother Erlend
	# from Thorfinn the Mighty's death c.1065 — seat-once, Paul carries it.
	# Both earls fought at Stamford Bridge on Hardrada's side. Dynasty-less
	# (the Norse earls' house is not in vanilla); norn_culture is the
	# Northern Isles' own culture, vanilla's Orkney pops use it.
	ork_paul_thorfinnsson = {
		first_name = { name = name_paul }
		culture = norn_culture
		religion = catholic
		birth_date = 1035.1.1
		birth = orkney
		tag = ORK
	}

	# --- 1066 Islamic South -----------------------------------------------
	# From the Levant/Africa research pass. Birth years are [U] estimates
	# throughout — no source dates them; every other identifier verified
	# (name_ali:1241, name_abu_bakr:188, name_joseph:10198 in the registry;
	# literal `Tamim` per vanilla's own literal `Tashfin`,
	# 05_characters.txt:48105; cultures yemeni_culture, tunisian, sanhaja;
	# religion shia = muslim.txt:64; locations sana_yemen, kairouan,
	# aoudaghost in definitions.txt). NO death dates.

	# Ali ibn Muhammad al-Sulayhi, founder of the Sulayhid state: rose in
	# the Haraz 1047, took Sana'a 1063, Fatimid-allegiant Ismaili
	# (religion shia; the country-level ismaili_school is territory-pass
	# work). Historically assassinated c. 1067-1080 (sources differ).
	yem_ali_al_sulayhi = {
		first_name = { name = name_ali }
		culture = yemeni_culture
		religion = shia
		birth_date = 1015.1.1
		birth = sana_yemen
		dynasty = sulayhid_dynasty
		tag = YEM
	}

	# Tamim ibn al-Mu'izz, Zirid emir of Ifriqiya from his father's death
	# in 1062 — mid-Hilalian catastrophe, Kairouan sacked 1057, the court
	# on the Mahdia coast. The Zirids broke with Cairo in 1048: sunni.
	zir_tamim_ibn_al_muizz = {
		first_name = { name = Tamim }
		culture = tunisian
		religion = sunni
		birth_date = 1031.1.1
		birth = kairouan
		dynasty = zirid_dynasty
		tag = TUN
	}

	# Abu Bakr ibn Umar, Almoravid amir from his brother Yahya's death
	# c. 1056. On 1066.9.15 he, not Yusuf, leads the movement — the
	# leadership ambiguity is recorded in KNOWLEDGE; the ~1072 handover to
	# Yusuf is script work, and both actors are authored for it.
	alm_abu_bakr_ibn_umar = {
		first_name = { name = name_abu_bakr }
		culture = sanhaja
		religion = sunni
		birth_date = 1010.1.1
		birth = aoudaghost
		dynasty = almoravid_dynasty
		tag = TFL
	}

	# Yusuf ibn Tashfin, Abu Bakr's cousin and deputy, sole ruler from
	# ~1072, victor of Sagrajas 1086 — authored now, unseated, so the
	# handover and the Iberian intervention have their actor.
	alm_yusuf_ibn_tashfin = {
		first_name = { name = name_joseph }
		culture = sanhaja
		religion = sunni
		birth_date = 1009.1.1
		birth = aoudaghost
		dynasty = almoravid_dynasty
		tag = TFL
	}

	# --- 1066 Celtic world ------------------------------------------------
	# From the Celtic research pass. The naming grammar (KNOWLEDGE.md):
	# display comes from the language row of the key, and .genitive rows
	# drive patronymics — name_hugh renders Aodh in Gaelic, and Murchad's
	# father link auto-renders "mac Diarmata" from name_dermot's genitive.

	# Aed "in Gai Bernaig" Ua Conchobair, King of Connacht 1046-1067 —
	# [U] dates throughout. o_conchobair_dynasty ships in vanilla.
	cnn_aed_in_gai_bernaig = {
		first_name = { name = name_hugh }
		culture = irish
		religion = catholic
		birth_date = 1020.1.1
		birth = roscommon
		dynasty = o_conchobair_dynasty
		tag = CNN
	}

	# Murchad mac Diarmata — Diarmait's son, king of Dublin (and Mann) for
	# his father until his death in 1070. Authored unseated: Dublin has no
	# tag (it sits inside PLE), and the succession needs him.
	lei_murchad_mac_diarmata = {
		first_name = { name = name_murphy }
		culture = irish
		religion = catholic
		birth_date = 1035.1.1
		birth = dublin
		dynasty = kinsella_dynasty
		father = lei_diarmait_mac_mail_na_mbo
		tag = LEI
	}
"""


# ------------------------------------------------------------------ tools ---
def date_tuple(s):
    """Tolerant y.m.d parser. Vanilla ships partial dates — 2 characters carry
    `birth_date = 1010.1.` with a trailing dot ("# unknown") — and a strict
    int() on the empty tail crashed the build once. Missing parts pad to 1."""
    parts = [p for p in s.split(".") if p != ""]
    while len(parts) < 3:
        parts.append("1")
    return tuple(int(p) for p in parts[:3])


def find_block_end(s, open_brace):
    """Index just past the `}` matching the `{` at open_brace, ignoring braces
    inside comments and quoted strings."""
    depth, i, n = 0, open_brace, len(s)
    while i < n:
        c = s[i]
        if c == "#":
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        if c == '"':
            i += 1
            while i < n and s[i] != '"':
                i += 2 if s[i] == "\\" else 1
            i += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError(f"unbalanced brace from offset {open_brace}")


def strip_blocks(src, key):
    """Delete every `key = { … }`, including the ones that span lines."""
    cuts, n = [], 0
    for m in re.finditer(r"^[ \t]*" + key + r"[ \t]*=[ \t]*\{", src, re.M):
        end = find_block_end(src, src.index("{", m.start()))
        a = src.rfind("\n", 0, m.start()) + 1
        b = src.find("\n", end - 1)
        cuts.append((a, len(src) if b < 0 else b + 1))
        n += 1
    for a, b in reversed(cuts):
        src = src[:a] + src[b:]
    return src, n


def strip_lines(src, key):
    return re.subn(r"^[ \t]*" + key + r"[ \t]*=[^\n]*\n", "", src, flags=re.M)


def tidy(src):
    """Stripping thousands of lines leaves long runs of blanks. These files are
    generated but still get diffed against vanilla by people."""
    return re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", src)


# --------------------------------------------------------------- builders ---
# Capturing: several checks need the tag itself, not just the position.
# `len(re.findall(...))` is unaffected by the group, so counts stay correct.
COUNTRY_RE = r"^\t([A-Z0-9]{2,6}) = \{"

# Blocks removed whole — both carry dates that are future at a 1066 start.
COUNTRY_BLOCKS = ("ruler_term", "timed_modifier")
# Lines removed. Each names a 1337 character or a 1330s date, and per the wiki
# neither `heir` nor `consort` accepts `random`, so unlike `ruler` they cannot be
# neutralised — they have to go.
COUNTRY_LINES = ("heir", "consort", "active_regent", "designated_heir_reason",
                 "regency", "start_regency_date", "end_regency_date",
                 "inherit_ruler_terms")


def build_countries(src):
    report = []
    before = len(re.findall(COUNTRY_RE, src, re.M))

    for key in COUNTRY_BLOCKS:
        src, n = strip_blocks(src, key)
        report.append((f"{key} blocks removed", n))
    for key in COUNTRY_LINES:
        src, n = strip_lines(src, key)
        report.append((f"{key} lines removed", n))

    # `ruler = <name>` -> random. Counted apart from the no-ops, because a
    # substitution count including them would report work that never happened.
    n_ruler, n_already = 0, 0

    def _ruler(m):
        nonlocal n_ruler, n_already
        indent, name, comment = m.group(1), m.group(2), m.group(3) or ""
        if name == "random":
            n_already += 1
            return m.group(0)
        n_ruler += 1
        return f"{indent}ruler = random{' ' + comment if comment else ''}\n"

    # The trailing-comment group is not cosmetic: 17 of vanilla's `ruler` lines
    # carry one and 4 of those name a real character. Without it they slip
    # through and those countries keep a 1337 ruler.
    src = re.sub(r"^([ \t]*)ruler[ \t]*=[ \t]*([A-Za-z0-9_]+)[ \t]*(#[^\n]*)?\n",
                 _ruler, src, flags=re.M)
    report.append(("ruler = <name> -> random", n_ruler))
    report.append(("ruler = random already", n_already))

    # A country with no ruler at all hits the empty-throne regency the ENG probe
    # produced, so make it explicit. The test is per COUNTRY, not per government
    # block: 175 country blocks declare `government = { … }` twice, and testing
    # per block put a stray second `ruler = random` in each — invisible now, but
    # it would silently outrank the first historical ruler Phase 2 sets.
    added, no_gov = 0, 0
    starts = list(re.finditer(COUNTRY_RE, src, re.M))
    edits = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(src)
        body = src[m.start():end]
        if re.search(r"^[ \t]*ruler[ \t]*=", body, re.M):
            continue
        gov = re.search(r"^([ \t]*)government[ \t]*=[ \t]*\{", body, re.M)
        if gov:
            edits.append((m.start() + body.index("{", gov.start()) + 1,
                          f"\n{gov.group(1)}\truler = random"))
        else:
            edits.append((m.start() + body.index("{") + 1,
                          "\n\t\tgovernment = {\n\t\t\truler = random\n\t\t}"))
            no_gov += 1
        added += 1
    for at, text in sorted(edits, reverse=True):
        src = src[:at] + text + src[at:]
    report.append(("ruler = random added (had none)", added))
    if no_gov:
        report.append(("  of those, needed a government block", no_gov))

    # Regnal-number tables are 1337's: ENG carries name_william = 2 (counting
    # the Conqueror and Rufus), so William crowned via the union displayed as
    # "William III" in game. 0 makes the next William the first. BYZ's table
    # is inflated by every emperor between 1066 and 1337 (research pass,
    # KNOWLEDGE.md). Grow this table as wrong numerals are OBSERVED or
    # research-attested, not preemptively.
    REGNAL_FIXES = {
        ("ENG", "name_william"): 0,
        ("BYZ", "name_michael"): 6,       # Michael VII accedes 1071
        ("BYZ", "name_roman"): 3,         # Romanos IV accedes 1068
        ("BYZ", "name_nikephoros"): 2,    # Nikephoros III accedes 1078
        ("BYZ", "name_alexis"): 0,        # Alexios I accedes 1081
        ("BYZ", "name_isaac"): 1,
        ("BYZ", "name_emmanuel"): 0,      # Manuel I accedes 1143
        ("BYZ", "name_andronikos"): 0,    # first Andronikos is 1183; key renamed below
        ("SWE", "name_eric"): 7,          # vanilla's own chain: Erik VII to 995, Erik VIII accedes 1083
        ("HUN", "name_stephen"): 1,       # Stephen I the Saint only, pre-1066
        ("HUN", "name_andrew"): 1,        # Andrew I d. 1060
        ("HUN", "name_bela"): 1,          # Bela I d. 1063
        ("HUN", "name_geza"): 0,          # Geza I accedes 1074 (the 1066 DUKE Geza is not king)
        ("HUN", "name_vladislav"): 0,     # Ladislaus I accedes 1077
        ("HUN", "name_kalman"): 0,        # Coloman accedes 1095
        ("HUN", "name_emmerich"): 0,      # Emeric accedes 1196
        ("HUN", "name_salomon"): 1,       # Solomon reigns NOW — counted like BYZ's Constantine 10; key renamed below
        ("POK", "name_vseslav"): 1,       # Vseslav reigns now, the first
        ("POK", "name_iziaslav"): 1,
        ("POK", "name_briachislav"): 1,
    }
    # Vanilla typo: BYZ's table says `name_andonikos` — a key with no loc
    # entry anywhere (the registry has only name_andronikos,
    # character_names_dynamic_l_english.yml:1783). Renamed FIRST so the
    # value fix above can find it. Report-vanilla, fix-ours discipline:
    # this is a rename in OUR generated copy, vanilla stays untouched.
    REGNAL_RENAMES = {
        ("BYZ", "name_andonikos"): "name_andronikos",
        # Vanilla bug #5: HUN's table uses name_solomon — zero loc entries
        # anywhere; the registry's key is name_salomon (loc:15508).
        ("HUN", "name_solomon"): "name_salomon",
    }
    n_fix = 0
    starts_rf = list(re.finditer(COUNTRY_RE, src, re.M))
    for (tag, oldkey), newkey in sorted(REGNAL_RENAMES.items()):
        for i, b in enumerate(starts_rf):
            if b.group(1) != tag:
                continue
            end = starts_rf[i + 1].start() if i + 1 < len(starts_rf) else len(src)
            body, k = re.subn(r"(^[ \t]*)" + oldkey + r"\b",
                              lambda mm, nk=newkey: mm.group(1) + nk,
                              src[b.start():end], count=1, flags=re.M)
            if not k:
                sys.exit(f"REGNAL_RENAMES: {oldkey} not found inside {tag}")
            src = src[:b.start()] + body + src[end:]
            break
        else:
            sys.exit(f"REGNAL_RENAMES: tag {tag} not found")
    starts_rf = list(re.finditer(COUNTRY_RE, src, re.M))
    for (tag, namekey), val in sorted(REGNAL_FIXES.items()):
        for i, b in enumerate(starts_rf):
            if b.group(1) != tag:
                continue
            end = starts_rf[i + 1].start() if i + 1 < len(starts_rf) else len(src)
            body, k = re.subn(r"(^[ \t]*" + namekey + r" = )\d+",
                              lambda mm, v=val: mm.group(1) + str(v),
                              src[b.start():end], count=1, flags=re.M)
            if not k:
                sys.exit(f"REGNAL_FIXES: {namekey} not found inside {tag}")
            src = src[:b.start()] + body + src[end:]
            n_fix += k
            break
        else:
            sys.exit(f"REGNAL_FIXES: tag {tag} not found")
    report.append(("regnal numbers recalibrated", n_fix))

    for tag, (char, accession, regnal) in sorted(HISTORICAL_RULERS.items()):
        term = (f"ruler_term = {{ character = {char} start_date = {accession} "
                f"regnal_number = {regnal} }}")
        pat = re.compile(r"(^\t" + tag + r" = \{.*?^)([ \t]*)ruler = random", re.M | re.S)
        src, k = pat.subn(lambda m, c=char, t=term:
                          f"{m.group(1)}{m.group(2)}ruler = {c}\n{m.group(2)}{t}",
                          src, count=1)
        if not k:
            sys.exit(f"HISTORICAL_RULERS: no `ruler = random` found for {tag}")
    report.append(("historical rulers restored (+ open term)", len(HISTORICAL_RULERS)))

    src = tidy(src)
    after = len(re.findall(COUNTRY_RE, src, re.M))

    def validate():
        if after != before:
            return f"country count changed {before} -> {after}: territory would be lost"
        for key in COUNTRY_BLOCKS + COUNTRY_LINES:
            if key == "ruler_term":
                continue    # vanilla's are stripped; OURS are re-added and audited below
            if re.search(r"^[ \t]*" + key + r"[ \t]*=", src, re.M):
                return f"{key} survived the strip"
        # Every remaining ruler must be random or a Phase 2 entry. This is the
        # check that catches a ruler line whose shape differs just enough to miss
        # the rewrite and leave that country a -250-year-old.
        chars = {c for c, _, _ in HISTORICAL_RULERS.values()}
        stray = [m.group(1) for m in
                 re.finditer(r"^[ \t]*ruler[ \t]*=[ \t]*([A-Za-z0-9_]+)", src, re.M)
                 if m.group(1) != "random" and m.group(1) not in chars]
        if stray:
            return f"{len(stray)} ruler(s) still name a character: {stray[:8]}"
        # Exactly one per country: more can outrank a Phase 2 ruler, fewer means
        # an empty throne and an engine-generated regent.
        s2 = list(re.finditer(COUNTRY_RE, src, re.M))
        bad = []
        for i, m in enumerate(s2):
            e = s2[i + 1].start() if i + 1 < len(s2) else len(src)
            if len(re.findall(r"^[ \t]*ruler[ \t]*=", src[m.start():e], re.M)) != 1:
                bad.append(m.group(0).strip()[:6])
        if bad:
            return f"{len(bad)} countries lack exactly one ruler: {bad[:8]}"

        # The HISTORICAL_RULERS substitution is a non-greedy `.*?` under re.S
        # anchored on the tag, so it is only bounded by finding a
        # `ruler = random` — if a tag's own block ever lacked one it would run
        # on and rewrite the NEXT country's ruler instead, silently and
        # plausibly. The invariant above makes that impossible today; this
        # confirms placement rather than trusting it.
        placed = {}
        for i, m in enumerate(s2):
            e = s2[i + 1].start() if i + 1 < len(s2) else len(src)
            r = re.findall(r"^[ \t]*ruler = ([a-z_0-9]+)", src[m.start():e], re.M)
            if r and r[0] != "random":
                placed[m.group(1)] = r[0]
        expected = {t: c for t, (c, _, _) in HISTORICAL_RULERS.items()}
        if placed != expected:
            return (f"historical rulers landed in the wrong countries: "
                    f"expected {expected}, found {placed}")

        # Vanilla's ruler_terms are stripped and OURS are re-added; the two
        # motions must reconcile exactly. Every surviving term must be one we
        # generated: OPEN (no end_date), for a Phase 2 character.
        # Audit COMMENT-STRIPPED text: vanilla ships 60 commented-out
        # ruler_terms (dates and all) that the parser never sees.
        nc = re.sub(r"#[^\n]*", "", src)
        accessions = {c: acc for c, acc, _ in HISTORICAL_RULERS.values()}
        terms = re.findall(r"ruler_term[ \t]*=[ \t]*\{([^}]*)\}", nc)
        if len(terms) != len(HISTORICAL_RULERS):
            return f"expected {len(HISTORICAL_RULERS)} ruler_terms, found {len(terms)}"
        for t in terms:
            cm = re.search(r"character = ([a-z0-9_]+)", t)
            if not cm or cm.group(1) not in accessions:
                return f"a ruler_term names no Phase 2 character: {{{t.strip()}}}"
            if "end_date" in t:
                return (f"ruler_term for {cm.group(1)} has an end_date — the "
                        f"current reign must be OPEN or nobody seats")

        # No FUTURE date may survive: at 1066 vanilla's 1337 dates read as the
        # future. NOT line-anchored — one-line blocks put dates mid-line, and
        # the old line-anchored scan sailed right past them for all of Phase 1.
        # What it was missing: five live `date =` fields in bureaucracy entries
        # (BYZ 680/330/500/892 — past, parse fine; TRE 1204.4.1 — genuinely
        # future). TRE's shipped through Phase 1 measured-clean, so it is a
        # DOCUMENTED exemption deferred to the Byzantium/Anatolia slice, not a
        # silent fix. Anything new and future still fails the build.
        # (In 05_characters.txt dates are exempt: birth_date and death_date are
        # exactly what that file is for.)
        KNOWN_FUTURE = {"1204.4.1"}   # TRE themata_bureaucracy — Trebizond founded 1204
        start = _start_date()
        starts_seen = 0
        for key, val in re.findall(r"\b(start_date|end_date|date)[ \t]*=[ \t]*([0-9.]+)", nc):
            d = tuple(int(x) for x in val.split("."))
            if key == "start_date":
                starts_seen += 1
                if val not in accessions.values():
                    return f"start_date = {val} is not an accession date we wrote"
                if d >= start:
                    return f"start_date = {val} is not before START_DATE — the term would not be active"
            elif key == "end_date":
                return f"end_date = {val} survived — it would parse as future at 1066"
            elif d >= start and val not in KNOWN_FUTURE:
                return f"date = {val} is future at 1066 and not a documented exemption"
        if starts_seen != len(HISTORICAL_RULERS):
            return (f"{starts_seen} start_dates survived, expected exactly "
                    f"{len(HISTORICAL_RULERS)} (one per generated ruler_term)")
        return None

    return src, report, validate, f"{before} country blocks, all kept"


def build_ios(src):
    """International organizations carry regnal history for the HRE and the
    Papacy in exactly the same shape as countries. Safe to strip: an IO's head is
    `leader = <TAG>`, a country, not a character — so removing the terms cannot
    leave it headless the way it would a country."""
    report = []
    src, n = strip_blocks(src, "ruler_term")
    report.append(("ruler_term blocks removed", n))

    # Future-dated IO INSTANCES are the same poison class everything else
    # from 1337 wears: the Middle Kingdom (1271), the Lordship of Ireland
    # (1177), the Guelph and Ghibelline leagues (1125)... 18 instances whose
    # creation_date is after 1066.9.15, seeded active with leaders and
    # members — three of them complained at every load (the accepted error
    # class). Found by the Italy research pass: `creation_date` was
    # INVISIBLE to the old date audit, because \bdate\b cannot match after
    # an underscore. The blocks go whole; the IO TYPES stay defined in
    # in_game/common, and later centuries can script them back when their
    # years arrive.
    start = _start_date()
    cuts, removed = [], 0
    for m in re.finditer(r"^\tadd_international_organization = \{", src, re.M):
        end = find_block_end(src, src.index("{", m.start()))
        body = src[m.start():end]
        cd = re.search(r"creation_date[ \t]*=[ \t]*([0-9.]+)", body)
        if cd and date_tuple(cd.group(1)) >= start:
            a = src.rfind("\n", 0, m.start()) + 1
            b = src.find("\n", end - 1)
            cuts.append((a, len(src) if b < 0 else b + 1))
            removed += 1
    for a, b in reversed(cuts):
        src = src[:a] + src[b:]
    report.append(("future-dated IO instances removed", removed))

    leaders = len(re.findall(r"^[ \t]*leader[ \t]*=", src, re.M))
    src = tidy(src)

    def validate():
        if re.search(r"^[ \t]*ruler_term[ \t]*=", src, re.M):
            return "ruler_term survived the strip"
        # Exactly 18 in vanilla 1.3.11 — a patch changing the number fails
        # loudly and a human re-reads the file.
        if removed != 18:
            return f"expected exactly 18 future-dated IO removals, removed {removed}"
        nc = re.sub(r"#[^\n]*", "", src)
        for mm in re.finditer(r"creation_date[ \t]*=[ \t]*([0-9.]+)", nc):
            if date_tuple(mm.group(1)) >= start:
                return f"a future creation_date survived: {mm.group(1)}"
        m2 = re.search(r"\b(start_date|end_date|date)[ \t]*=[ \t]*([0-9.]+)", nc)
        if m2:
            return f"{m2.group(1)} = {m2.group(2)} survived — it would parse as future at 1066"
        return None

    return src, report, validate, f"{leaders} IO leaders kept in the surviving instances"


def _start_date():
    """Read START_DATE from our own defines rather than hardcoding it, so the
    adult-age check below can never drift away from the date the game uses."""
    p = os.path.join(MOD, "loading_screen", "common", "defines", "zz_1066_dates.txt")
    m = re.search(r'START_DATE\s*=\s*"(\d+)\.(\d+)\.(\d+)"',
                  open(p, encoding="utf-8-sig").read())
    if not m:
        sys.exit(f"could not read START_DATE from {p}")
    return tuple(int(x) for x in m.groups())


ADULT_AGE = 16   # loading_screen/common/defines/00_defines.txt:1519


def build_characters(src):
    """Append our characters inside vanilla's `character_db`, keeping all 7236
    of vanilla's. Vanilla's chains reach back to 886, so most of what a 1066
    start needs is already there; this is only for the gaps."""
    report = []
    before = len(re.findall(r"^\t([a-z][a-z0-9_]*) = \{", src, re.M))

    close = src.rindex("}")            # the `}` closing character_db
    src = src[:close].rstrip() + "\n" + NEW_CHARACTERS + "}\n"

    after = len(re.findall(r"^\t([a-z][a-z0-9_]*) = \{", src, re.M))
    added = after - before
    report.append(("vanilla characters kept", before))
    report.append(("characters added", added))

    # A character ALIVE at start must carry NO death_date. The engine treats a
    # future death_date as invalid and the character starts DEAD — reign closed
    # on START_DATE, throne to an engine-generated regent, and not one line in
    # error.log. Measured in game 2026-07-28: all five historical rulers dead
    # at start this way, Sweyn's death a full ten YEARS out. Vanilla's own
    # convention agrees: 4304 of its 4305 death_dates are past at 1337, and
    # eng_edward_iii (historically dies 1377) carries none.
    #
    # SCOPED to characters BORN BEFORE START_DATE, the hard way: stripping all
    # 3,762 future death_dates also resurrected ~3,500 FUTURE-BORN characters
    # (their collapsed birth dates plus no death made them ancient and alive —
    # init logged future-born sco_william_the_lion as instantiated), and the
    # game HARD-FROZE on the first unpause, log cut mid-word. Future-born
    # characters keep their vanilla death_dates: dead-or-unborn is exactly the
    # state the game demonstrably ran with. Past deaths are history and stay.
    start = _start_date()
    blocks = list(re.finditer(r"^\t([a-z][a-z0-9_]*) = \{", src, re.M))
    cuts = []
    for i, b in enumerate(blocks):
        end = blocks[i + 1].start() if i + 1 < len(blocks) else len(src)
        body = src[b.start():end]
        bd = re.search(r"birth_date[ \t]*=[ \t]*([0-9.]+)", body)
        if not bd or date_tuple(bd.group(1)) >= start:
            continue    # unborn or undated: leave exactly as vanilla wrote it
        for dm in re.finditer(r"^[ \t]*death_date[ \t]*=[ \t]*([0-9.]+)"
                              r"[ \t]*(?:#[^\n]*)?\n", body, re.M):
            if date_tuple(dm.group(1)) >= start:
                cuts.append((b.start() + dm.start(), b.start() + dm.end()))
    for a, z in reversed(cuts):
        src = src[:a] + src[z:]
    report.append(("death_date removed from the living", len(cuts)))

    # Vanilla's own loose ends, reported so they are not mistaken for ours.
    _pos = {m.group(1) for m in re.finditer(r"^\t([a-z][a-z0-9_]*) = \{", src, re.M)}
    _dangling = {m.group(2) for m in
                 re.finditer(r"^\t\t(father|mother|spouse) = ([a-z][a-z0-9_]*)", src, re.M)
                 if m.group(2) != "random" and m.group(2) not in _pos}
    if _dangling:
        report.append(("  vanilla dangling parent refs (not ours)", len(_dangling)))

    def validate():
        if before == 0:
            return "no vanilla characters parsed — the shape of the file changed"
        if added != len(re.findall(r"^\t[a-z][a-z0-9_]* = \{", NEW_CHARACTERS, re.M)):
            return "added count does not match NEW_CHARACTERS"

        start = _start_date()
        pos = {m.group(1): m.start()
               for m in re.finditer(r"^\t([a-z][a-z0-9_]*) = \{", src, re.M)}

        # Exhaustive backstop for the line-anchored death_date strip: scan the
        # comment-stripped text the parser actually sees, any format, any
        # position, block by block. NOBODY may be born before start yet carry a
        # post-start death — that character starts the game dead, silently.
        # (Future-born characters legitimately keep theirs.)
        nc5 = re.sub(r"#[^\n]*", "", src)
        blks = list(re.finditer(r"^\t([a-z][a-z0-9_]*) = \{", nc5, re.M))
        for i, b in enumerate(blks):
            e5 = blks[i + 1].start() if i + 1 < len(blks) else len(nc5)
            body = nc5[b.start():e5]
            bd = re.search(r"birth_date[ \t]*=[ \t]*([0-9.]+)", body)
            dd = re.search(r"death_date[ \t]*=[ \t]*([0-9.]+)", body)
            if bd and dd and date_tuple(bd.group(1)) < start <= date_tuple(dd.group(1)):
                return (f"{b.group(1)}: alive at start but carries "
                        f"death_date {dd.group(1)} — starts the game dead")

        # A named parent must exist — but only OURS is a build failure. Vanilla
        # ships 8 dangling references of its own (yem_al_muzaffar_yusuf_i,
        # wls_goronwy_ap_tudur_hen, sav_humbert_i_savoy, dhf_al_faiz) and runs
        # anyway, so failing on those would block work over someone else's data.
        # `random` is a legal value here, not a dangling name — vanilla uses it.
        for m in re.finditer(r"^\t\t(father|mother|spouse) = ([a-z][a-z0-9_]*)",
                             NEW_CHARACTERS, re.M):
            if m.group(2) != "random" and m.group(2) not in pos:
                return f"NEW_CHARACTERS: {m.group(1)} = {m.group(2)} does not exist"

        # Ordering is NOT checked across the whole file. Vanilla's own header
        # says "write sons and daughters ALWAYS after their parents to avoid
        # crashes", and a published conversion repeats it — but vanilla itself
        # ships 614 characters that name a parent declared later, and the game
        # runs. So the rule as stated is not enforced by the engine. We still
        # keep OUR OWN additions ordered, because it costs nothing and the
        # warning may hold in some narrower case nobody has pinned down.
        ours = {m.group(1): m.start()
                for m in re.finditer(r"^\t([a-z][a-z0-9_]*) = \{", NEW_CHARACTERS, re.M)}
        for m in re.finditer(r"^\t\t(father|mother) = ([a-z][a-z0-9_]*)",
                             NEW_CHARACTERS, re.M):
            p = m.group(2)
            if p in ours and ours[p] > m.start():
                return f"NEW_CHARACTERS: {p} is declared after a child that names it"

        # Every historical ruler must exist, be an adult on the start date, and
        # accede between birth and START_DATE — the accession feeds the open
        # ruler_term, and a future or pre-birth date there means no seat.
        for tag, (key, accession, _regnal) in sorted(HISTORICAL_RULERS.items()):
            if key not in pos:
                return f"HISTORICAL_RULERS[{tag}] = {key} is not a character"
            body = src[pos[key]:pos[key] + 700]
            bd = re.search(r"birth_date = (\d+)\.(\d+)\.(\d+)", body)
            if not bd:
                return f"{key} has no birth_date"
            born = tuple(int(x) for x in bd.groups())
            age = start[0] - born[0] - ((start[1], start[2]) < (born[1], born[2]))
            if age < ADULT_AGE and tag not in MINOR_RULERS:
                return (f"{key} is {age} at {start[0]}.{start[1]}.{start[2]} — "
                        f"under ADULT_AGE {ADULT_AGE}, the throne would sit empty; "
                        f"if the minority is HISTORICAL, list the tag in MINOR_RULERS")
            if age >= ADULT_AGE and tag in MINOR_RULERS:
                return (f"MINOR_RULERS lists {tag} but {key} is {age} — "
                        f"stale exemption, remove it")
            dd = re.search(r"death_date = (\d+)\.(\d+)\.(\d+)", body)
            if dd and tuple(int(x) for x in dd.groups()) < start:
                return f"{key} is already dead at the start date"
            acc = tuple(int(x) for x in accession.split("."))
            if len(acc) != 3:
                return f"{key} accession {accession} is not a y.m.d date"
            if acc >= start:
                return f"{key} accession {accession} is not before the start date"
            if acc < born:
                return f"{key} accession {accession} is before their birth"
        return None

    return src, report, validate, f"{after} characters, {len(HISTORICAL_RULERS)} rulers checked"


def build_diplomacy(src):
    """Strip the ten French appanage dependencies (12_diplomacy.txt:158-170).
    The appanage subject type needs a Capetian dynastic link no 1066 ruler
    has — the engine declares every one invalid at game start
    (government.cpp:3702, ~25 of the 53-line error baseline) — and as French
    SUBJECTS the great fiefs cannot declare war, which is what blocked
    William's conquest in game: can_declare_legal_war_on = no, silently.
    Historically the 1066 great vassals were de facto independent
    (docs/PHASE-2-PLAN.md); the France-region pass will model their loose
    ties properly. Every other dependency is left exactly as vanilla wrote
    it."""
    report = []
    before = len(re.findall(r"^[ \t]*dependency = \{", src, re.M))
    src, n = re.subn(r"^[ \t]*dependency = \{[^}\n]*subject_type = appanage[^}\n]*\}[ \t]*\n",
                     "", src, flags=re.M)
    report.append(("appanage dependencies removed", n))
    src = tidy(src)
    after = len(re.findall(r"^[ \t]*dependency = \{", src, re.M))

    # AUDIT, decision parked (Italy pass, F2): 28 of the surviving
    # dependencies carry FUTURE start_dates (earliest 1202.10.9 — Venice's
    # vassal Trieste dated to Enrico Dandolo). Whether the engine collapses
    # them like ruler_terms is unmeasured, and stripping them reshapes the
    # whole 1337 vassal web — recorded as a proposal, counted here so any
    # drift is loud.
    n_future_deps = sum(1 for d in re.findall(
        r"start_date[ \t]*=[ \t]*([0-9.]+)", re.sub(r"#[^\n]*", "", src))
        if date_tuple(d) >= _start_date())
    report.append(("future-dated dependencies (parked)", n_future_deps))

    def validate():
        if re.search(r"appanage", re.sub(r"#[^\n]*", "", src)):
            return "an appanage reference survived the strip"
        # Exactly 10 in vanilla 1.3.11. If a patch changes the number, this
        # fails loudly and a human re-reads the file — better than drifting.
        if n != 10 or before - after != n:
            return f"expected exactly 10 appanage cuts, removed {n} ({before} -> {after})"
        if n_future_deps != 28:
            return (f"future-dated dependency count changed: {n_future_deps} "
                    f"(expected 28) — re-read the file before deciding anything")
        return None

    return src, report, validate, f"{after} dependencies kept"


# The two wars of 1066, in progress at game start. Declaring them from
# script was measured IMPOSSIBLE before ~1 November across three in-game
# rounds — with the CB in hand, with hidden retries on days +1..+13, the
# declaration only ever succeeded on the first monthly tick of November,
# which reads as an engine-side declaration lock in the opening weeks. A war
# shipped in setup simply EXISTS from day one, the mechanism vanilla uses
# for 219 wars of its own. Historically right as well: Hardrada's army is
# already in England on 1066.9.15, and contemporaries dated the Norman
# quarrel from Harold's crowning on 6 January.
# Shape attested: war_name/start_date/action/attacker/defender per
# vanilla 16_wars.txt:1-45, the superiority goal binding per 16_wars.txt:270.
NEW_WARS = """
	war = {
		war_name = {
			name = "NORWEGIAN_INVASION_WAR_NAME"
			ordinal = 1
		}

		superiority = {
			type = norwegian_invasion_wargoal
			casus_belli = cb_norwegian_invasion
		}

		start_date = 1066.9.8
		action = 1066.9.14
		attacker = {
			country = NOR
			request = {
				reason = Instigator
			}
		}
		defender = {
			country = ENG
			request = {
				reason = Target
			}
		}
	}

	war = {
		war_name = {
			name = "NORMAN_CONQUEST_WAR_NAME"
			ordinal = 1
		}

		superiority = {
			type = norman_conquest_wargoal
			casus_belli = cb_norman_conquest
		}

		start_date = 1066.1.6
		action = 1066.9.14
		attacker = {
			country = NRM
			request = {
				reason = Instigator
			}
		}
		defender = {
			country = ENG
			request = {
				reason = Target
			}
		}
	}
"""


def build_wars(src):
    """Replace the war_manager body: every one of vanilla's wars and truces
    is future-dated at 1066 (earliest start_date 1283.1.1), the same poison
    class as the ruler_terms, and our two 1066 wars go in instead."""
    report = []
    open_b = src.index("{", src.index("war_manager"))
    close_b = find_block_end(src, open_b)
    body = src[open_b + 1:close_b - 1]
    n_blocks = len(re.findall(r"^\t[a-z_]+ = \{", body, re.M))
    dates = [date_tuple(d) for d in re.findall(r"start_date = ([0-9.]+)", body)]
    report.append(("vanilla wars and truces removed", n_blocks))
    src = src[:open_b + 1] + NEW_WARS + src[close_b - 1:]
    report.append(("1066 wars added", len(re.findall(r"^\twar = \{", NEW_WARS, re.M))))

    def validate():
        start = _start_date()
        for d in dates:
            if d < start:
                return (f"a vanilla war starts {d} — BEFORE our start date; "
                        f"it would have been valid and should not be stripped blindly")
        ours = [date_tuple(x) for x in re.findall(r"start_date = ([0-9.]+)", NEW_WARS)]
        if len(ours) != 2 or any(d >= start for d in ours):
            return f"our wars must both start before {start}: {ours}"
        for need in ("NOR", "NRM", "ENG"):
            if not re.search(r"country = " + need + r"\b", NEW_WARS):
                return f"{need} missing from the 1066 wars"
        return None

    return src, report, validate, "2 wars of 1066 in progress at start"


TARGETS = [
    ("05_characters.txt", build_characters),
    ("10_countries.txt", build_countries),
    ("12_diplomacy.txt", build_diplomacy),
    ("15_international_organizations.txt", build_ios),
    ("16_wars.txt", build_wars),
]

HEADER = """# GENERATED by tools/build_setup.py — do not hand-edit.
# Source: vanilla {rel}
#
# Removed: entries carrying 1337-dated people or dates, which a 1066 start reads
# as the future. The engine rejects them, collapses them to `1.1.1`, and the
# result is rulers aged about -250 and a flood of script errors. That includes
# every death_date at or after START_DATE: a living character carrying one
# starts the game DEAD, silently.
# Everything else — territory, capitals, ranks, templates, laws — is vanilla's.
#
# Added back: for each Phase 2 historical ruler, `ruler = <key>` PLUS an OPEN
# pre-1066 ruler_term. A named ruler does not seat without one — measured in
# game; see docs/KNOWLEDGE.md.
#
# KNOWN WRONG, deliberately left: regnal_numbers are still calibrated for 1337,
# so a ruler may be numbered as though his predecessors had already reigned.
# Cosmetic, no errors. Country content is likewise still 1337's — England starts
# with magna_carta_reform, which is 1215. Both are Phase 2 work.
#
# Re-run after a game patch. See docs/KNOWLEDGE.md.

"""


def main():
    dry = "--dry-run" in sys.argv
    failed = False

    for name, build in TARGETS:
        rel = os.path.join(SETUP, name)
        src = open(os.path.join(VAN, rel), encoding="utf-8-sig").read()
        before_lines = src.count("\n")

        out, report, validate, kept = build(src)
        out = HEADER.format(rel=rel.replace(os.sep, "/")) + out

        print(f"{name}")
        print(f"  {before_lines} lines in -> {out.count(chr(10))} out")
        for label, n in report:
            print(f"    {label:38} {n:6}")

        err = validate()
        if err is None and out.count("{") != out.count("}"):
            err = f"braces unbalanced: {{={out.count('{')} }}={out.count('}')}"
        if err:
            print(f"    FAIL: {err}")
            failed = True
            continue
        print(f"    OK — {kept}")

        if not dry:
            dst = os.path.join(MOD, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            # NO BOM. setup/start is the one BOM-free .txt tree; a BOM here is
            # read as a token and the file goes silently inert. See the
            # write-eu5-setup skill.
            with open(dst, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            print(f"    written: {rel}")
        print()

    if failed:
        sys.exit(1)
    if dry:
        print("--dry-run: nothing written")


if __name__ == "__main__":
    main()
