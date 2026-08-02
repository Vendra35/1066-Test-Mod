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

    # Italy and the probe, from the Italy research pass. A row may carry an
    # optional FOURTH element: a regnal_name loc key, emitted into the term
    # — vanilla's own papal convention (`regnal_number = 2 regnal_name =
    # name_callisto`, 10_countries.txt PAP block; 96 uses file-wide). The
    # pope's character keeps his BIRTH name (Anselmo of Baggio); the term
    # crowns him Alexander II.
    "VEN": ("ven_domenico_contarini", "1043.1.1", 1),     # Doge Domenico Contarini — vanilla character, vanilla's own term date
    "PAP": ("pap_anselmo_da_baggio", "1061.9.30", 2, "name_alexander"), # Pope Alexander II — NEW_CHARACTERS; capital fixed avignon->rome below
    "PYS": ("kie_vsevolod_rurikovich", "1054.2.20", 1),   # Vsevolod I, the third triumvir — seated on the NEW_COUNTRIES probe tag

    # Sardinia, restored to its giudicati by LOCATION_GRANTS. ARB's 1066
    # judge is genuinely obscure and GAL's unattested — both stay random;
    # Corsica gets territory only (no single 1066 ruler existed).
    "TOR": ("tor_barisone_i_lacon_gunale", "1038.1.1", 1), # Barisone I of Torres/Logudoro, [U] dates — NEW_CHARACTERS
    "CAG": ("cag_orzocco_torchitorio_i", "1058.1.1", 1),  # Orzocco Torchitorio I of Cagliari, [U] dates — NEW_CHARACTERS

    # The taifa factory (Opus Iberia package, key claims re-verified by the
    # main session). All thirteen rulers are NEW_CHARACTERS; every accession
    # is [U] — no taifa emir exists anywhere in vanilla to compare against.
    # regnal_number = 0 is vanilla's own convention for unnumbered rulers
    # (lon_alfonso_froilaz, 10_countries.txt:14723).
    "SEV": ("sev_abbad_al_mutadid", "1042.1.1", 2),       # Abbad II al-Mu'tadid, the taifa devourer
    "BDJ": ("bdj_muhammad_al_muzaffar", "1045.1.1", 0),   # Muhammad al-Muzaffar of Badajoz
    "TOL": ("tol_yahya_al_mamun", "1043.1.1", 1),         # Yahya I al-Ma'mun of Toledo — holds Valencia since 1065
    "CRD": ("crd_abd_al_malik_ibn_jahwar", "1064.1.1", 0),# Abd al-Malik ibn Jahwar of Cordoba, dates thin even for [U]
    "GRZ": ("grz_badis_ibn_habbus", "1038.1.1", 0),       # Badis ibn Habbus the Zirid — GRZ, never GRA (rank-branch law)
    "ALM": ("alm_muhammad_al_mutasim", "1051.1.1", 1),    # Muhammad al-Mu'tasim of Almeria
    "MRU": ("mru_muhammad_ibn_tahir", "1038.1.1", 0),     # Muhammad ibn Ahmad ibn Tahir of Murcia
    "DYA": ("dya_ali_iqbal_al_dawla", "1045.1.1", 0),     # Ali ibn Mujahid Iqbal al-Dawla of Denia and the Balearics
    "ZGZ": ("zgz_ahmad_al_muqtadir", "1046.1.1", 1),      # Ahmad I al-Muqtadir the Hudid of Zaragoza
    "LRD": ("lrd_yusuf_al_muzaffar", "1046.1.1", 0),      # Yusuf al-Muzaffar, al-Muqtadir's rival brother in Lerida
    "ABR": ("abr_abd_al_malik_ibn_razin", "1045.1.1", 0), # Abd al-Malik ibn Razin of Albarracin
    "ALP": ("alp_muhammad_yumn_al_dawla", "1043.1.1", 0), # Muhammad Yumn al-Dawla of Alpuente (capital = chelva, the map gap)
    "QRM": ("qrm_muhammad_al_birzali", "1052.1.1", 0),    # Muhammad al-Birzali of Carmona — Seville eats him in 1067

    # Christian Iberia (Opus package, terms re-verified). The three
    # brothers' vanilla terms all open on Ferdinand I's death date —
    # the partition is written into vanilla's own data.
    "LON": ("lon_alfonso_vi_jimena", "1065.12.27", 6),    # Alfonso VI of León — vanilla term :14736
    "GLC": ("glc_garcia_ii_jimena", "1065.12.27", 2),     # García II of Galicia (holds the county of Portugal) — vanilla term :14791
    "CAT": ("cat_ramon_berenguer_i_barcelona", "1035.5.26", 1), # Ramon Berenguer I of Barcelona — vanilla term :14267
    # The Pyrenean counties — NEW_CHARACTERS, accession days [U].
    "URG": ("urg_ermengol_iv_bellonid", "1065.1.1", 4),   # Ermengol IV of Urgell
    "BSL": ("bsl_bernat_ii_bellonid", "1066.1.1", 2),     # Bernat II of Besalú, brother Guillem II died 1066 [U]
    "CDY": ("cdy_ramon_guifre_bellonid", "1035.1.1", 0),  # Ramon Guifré of Cerdanya — composite name, no numbering tradition
    "EPU": ("epu_ponc_i_empuries", "1040.1.1", 1),        # Ponç I of Empúries
    "PLJ": ("plj_ramon_iv_pallars", "1047.1.1", 0),       # Ramon IV of Pallars Jussà — numbering disputed, 0 is honest
    "RSL": ("rsl_guislabert_ii_empuries", "1062.1.1", 2), # Guislabert II of Roussillon — name_guislabert is OUR key (proven mechanism)

    # The Byzantium slice adds one throne: Duklja. Constantine X, Bagrat IV
    # and the whole 1067-1081 Byzantine cast already ship in vanilla.
    "ZTA": ("zta_mihailo_vojislavljevic", "1046.1.1", 1), # Mihailo of Duklja, King from ~1077 — accession [U], NEW_CHARACTERS

    # The Seljuk world (Opus package §5). Vanilla ships ZERO Muslim
    # characters born before 1054, so all eleven are authored and every
    # date is [U]. regnal_number = 0 throughout — vanilla's own
    # no-ordinal value (184 uses, incl. Alfred the Great).
    "SEL": ("sel_alp_arslan", "1063.9.4", 0),             # Sultan Alp Arslan — Tughril died 1063.9.4; Qutalmish's revolt [D]
    "ABS": ("abs_abdallah_al_qaim", "1031.11.1", 0, "name_qaim"), # Caliph al-Qa'im — birth name Abdullah, the papal regnal_name route
    "KRM": ("krm_qawurd", "1041.1.1", 0),                 # Qavurt, Alp Arslan's brother — vanilla ships name_qawurd
    "GHZ": ("ghz_ibrahim", "1059.1.1", 0),                # Ibrahim of Ghazna — at peace with the Seljuks since 1059
    "UQY": ("uqy_muslim_ibn_quraysh", "1061.1.1", 0),     # Muslim ibn Quraysh of Mosul — accession 1061 vs 1072 [D]
    "MRD": ("mrd_nasr_nizam_al_din", "1061.1.1", 0),      # Nasr Nizam al-Din the Marwanid
    "HLB": ("hlb_mahmud_ibn_nasr", "1065.1.1", 0),        # Mahmud ibn Nasr the Mirdasid — his second reign
    "SHD": ("shd_abu_l_aswar_shavur", "1049.1.1", 0),     # Abu'l-Aswar Shavur of Ganja — dies 1067, a succession hook
    "SRV": ("srv_fariburz_i", "1063.1.1", 0),             # Fariburz I the Shirvanshah — kasranid_dynasty ships in vanilla
    "HLL": ("hll_dubays_i", "1018.1.1", 0),               # Dubays I the Mazyadid — a 63-year reign, attested [U]
    "KKY": ("kky_ali_ibn_faramurz", "1063.1.1", 0),       # Ali ibn Faramurz the Kakuyid of Yazd

    # Central Asia (package 2026-07-30, landed 2026-08-01). Both authored.
    # QRK regnal 1: "Ibrahim I" is attested Karakhanid historiography.
    # QRA regnal 0 DEVIATES from the package table's 1 — no attested
    # ordinal for Mahmud Toghrul Qara Khan (the Cadalus precedent:
    # ordinal only when the numbering is real); flagged for user review.
    "QRK": ("qrk_ibrahim_tamghach_khan", "1040.1.1", 1),  # Ibrahim ibn Nasr, Tamghach Bughra Khan, Samarkand c.1040-1068 [U]
    "QRA": ("qra_mahmud_toghrul_khan", "1059.1.1", 0),    # Mahmud Toghrul Qara Khan [D — the eastern list is unstable]

    # Arabia (package 2026-07-30, landed 2026-08-01). Both authored,
    # both dates [U]; Yahya is [D] on whether a single ruler is even the
    # right model for the Qarmatian council — he is the man attested
    # holding and losing Awal and Qatif at the state's fall.
    "QMT": ("qmt_yahya_ibn_al_abbas", "1058.1.1", 0),     # Yahya ibn al-Abbas, the council's face [U/D]
    "MDA": ("mda_al_husayn_ibn_muhanna", "1060.1.1", 0),  # al-Husayn ibn Muhanna, Husaynid emir of Medina [U]

    # India/China review, the JAP half (2026-08-01): vanilla's own
    # Go-Reizei, 41 at start, yamato_dynasty, no death_date — the
    # japanese_imperial_family reform's locked block DEMANDS a Yamato
    # ruler, so this seat is mandatory with the reform swap, not
    # optional. Accession day [U] (enthroned 1045).
    "JAP": ("jap_go_reizei_tenno", "1045.2.5", 0),        # Go-Reizei Tenno — vanilla character, resurrected by the death-strip

    # China-East (review D7, user-approved 2026-08-01). All accessions
    # [U]; temple names ride the regnal_name literal route (the papal/
    # Mustansir mechanism); regnal 0 = no ordinal (Cadalus rule) except
    # where historiography numbers the man. HSL is a VANILLA character
    # (the review's "Vinayaditya I" ordinal is not standard usage — 0
    # shipped, flagged). KHM: Udayadityavarman II dies IN 1066 [D] —
    # Harshavarman III is the safer seat, accession read as early 1066.
    "CHI": ("chi_zhao_shu_yingzong", "1063.5.1", 0, "Yingzong"),   # Yingzong of Song (Zhao Shu), r. 1063-1067
    "KOR": ("kor_wang_hwi_munjong", "1046.1.1", 0, "Munjong"),     # Munjong of Goryeo (Wang Hwi), r. 1046-1083
    "DAI": ("dai_ly_nhat_ton", "1054.11.1", 0, "Ly_Thanh_Tong"),   # Ly Thanh Tong (Ly Nhat Ton), r. 1054-1072
    "CHA": ("cha_rudravarman_iii", "1061.1.1", 3),                 # Rudravarman III of Champa, r. 1061-1074
    "CDL": ("cdl_duan_silian", "1041.1.1", 0),                     # Duan Silian of Dali, r. 1041-1075 [D]
    "KHM": ("khm_harshavarman_iii", "1066.1.1", 3),                # Harshavarman III of Angkor [D on the month]
    "HSL": ("hsl_vinayaditya_i_hoysala", "1047.1.1", 0),           # Vinayaditya the Hoysala — vanilla character, zero authoring

    # Northern Dynasties (package 2026-08-01, user-approved same day).
    # Temple names on the regnal_name literal route; both accessions
    # [U on the day]. Yizong: NO regency — 19 at start, personal rule
    # since he destroyed the Mozang in 1061; he dies 1067, as does
    # CHI's Yingzong — two northern successions inside sixteen months,
    # banked situation material.
    "LIA": ("lia_yelu_hongji_daozong", "1055.8.28", 0, "Daozong"),  # Daozong (Yelu Hongji), 8th Liao emperor, r. 1055-1101
    "XIA": ("xia_li_liangzuo_yizong", "1048.1.19", 0, "Yizong"),    # Yizong (Li Liangzuo), 2nd Xia emperor, r. 1048-1067

    # India Tier 1 (package 2026-08-01, user-approved). Eight seats;
    # TNK/DRW/GWA stay random deliberately (no agreed king — the
    # Pandya five, the bardic Tomara list, the decade-swinging
    # Chahamana dates). TWO KARNAS rule 1066 India — Chedi (RTP) and
    # Gujarat (CHU) — historically true, not a copy-paste.
    "COZ": ("coz_virarajendra_chola", "1063.1.1", 0),      # Virarajendra Chola, r. 1063-1070 [U]
    "CLK": ("clk_someshvara_i_ahavamalla", "1042.1.1", 1), # Someshvara I Ahavamalla, r. 1042-1068 (drowns himself in the Tungabhadra — a hook)
    "PAA": ("paa_vigrahapala_iii", "1054.1.1", 3),         # Vigrahapala III [D — the Pala tables disagree on the year, never on 1066]
    "PMR": ("pmr_jayasimha_i_paramara", "1055.1.1", 1),    # Jayasimha I [D — the hardest identification; both majority readings seat him 1055]
    "CHU": ("chu_karna_solanki", "1064.1.1", 0),           # Karna Chaulukya, r. 1064-1092 [U]; founds Karnavati
    "JJK": ("jjk_kirtivarman_chandela", "1060.1.1", 1),    # Kirtivarman — VANILLA'S OWN block comment attests him (10_countries JJK block)
    "RTP": ("rtp_lakshmi_karna", "1041.1.1", 0),           # Lakshmi-Karna of Chedi, r. 1041-1073 [U]
    # Africa (2026-08-02, decision 8 — the main session's own call,
    # user-approved over the package's "seat nobody"): al-Bakri,
    # WRITING 1067-68, describes the reigning king of Ghana as Tunka
    # Manin, acceded 1063 after his maternal uncle Basi [D — "Tunka"
    # may be the Soninke word for king; vanilla itself ships bare
    # `Tunka` in the mande male-name pool, 00_sahel.txt:110]. The one
    # near-contemporary attested name in the theater; nobody else in
    # sub-Saharan Africa is seated, deliberately.
    "GHA": ("gha_tunka_manin", "1063.1.1", 0),             # Tunka Manin of Wagadu, al-Bakri's king [D]
    "DBD": ("dbd_vijayabahu_i", "1055.1.1", 1),            # Vijayabahu I in Ruhuna from 1055; all Lanka 1073 [U]

    # Fatimid Egypt + the southern Levant (Opus package 2026-07-29; tag
    # freeness, the ismaili_policy pairing, cairo, the discovery
    # templates and both name registries re-verified by the main
    # session). The regnal_name slot takes a bare LITERAL as well as a
    # name key — vanilla's own `regnal_name = Chungsuk`
    # (10_countries.txt:24295, loc character_names_l_english.yml:11818);
    # Mustansir is OUR literal with a loc row (the proven mechanism).
    # Both al-Mustansir dates are firm (b. 1029.7.2, caliph 1036.6.13 —
    # aged 7; thirty years on the throne at start). NO vizier is
    # authored: the vizierate changed hands monthly in 1066 [D] and the
    # Mustansirite Hardship (1062-1073) is future situation material.
    "FAT": ("fat_maad_al_mustansir", "1036.6.13", 0, "Mustansir"), # al-Mustansir Billah, 8th Fatimid Imam-Caliph — NEW_CHARACTERS
    "MEC": ("mec_muhammad_abu_hashim", "1063.1.1", 0),    # Abu Hashim, first Hawashim emir of Mecca, appointed 1063 by al-Sulayhi [U] — NEW_CHARACTERS

    # France demesne + Languedoc (Opus package 2026-07-29; the 27-vassal
    # finding, the subject-type table, the tag ledger and every name key
    # re-verified by the main session). BER stays `ruler = random` ON
    # PURPOSE: who holds Berry in 1066 is genuinely disputed [D] — the
    # viscounty of Bourges and the Deols lordship are distinct and
    # neither is a county; random is the honest value.
    "TOU": ("tou_guilhem_iv_toulouse", "1061.1.1", 4),    # William IV of Toulouse — vanilla's own TOU regnal table expects name_william = 4 (10_countries.txt:17843) — NEW_CHARACTERS
    "VLS": ("vls_raoul_iv_crepy", "1038.1.1", 4),         # Raoul IV de Crepy — Valois, Amiens and the Vexin; accession [U] — NEW_CHARACTERS
    "VMD": ("vmd_herbert_iv_vermandois", "1045.1.1", 4),  # Herbert IV, last Carolingian count of Vermandois [U] — NEW_CHARACTERS

    # The British Isles (Opus package 2026-07-29; the SBL find, the
    # free tribe-tributary gate, the IO leader syntax, all name routes
    # and the six Welsh shells' 25/25 claim partition re-verified by
    # the main session). Deliberately random, reasons recorded:
    # TYR/ULD (the 1064-1083 Cenel nEogain succession is genuinely
    # unresolved [D]), LOI/GLY/ROS (no safely nameable 1066 ruler),
    # BER-precedent honesty throughout.
    "GDD": ("gdd_bleddyn_ap_cynfyn", "1063.8.5", 0),      # Bleddyn ap Cynfyn — Gwynedd (with Powys), installed after Gruffydd's fall — NEW_CHARACTERS
    "PWS": ("pws_rhiwallon_ap_cynfyn", "1063.8.5", 0),    # Rhiwallon, Bleddyn's brother and co-ruler, seated on Powys (d. 1069 Mechain) — NEW_CHARACTERS
    "DHB": ("dhb_maredudd_ab_owain", "1063.1.1", 0),      # Maredudd ab Owain of Deheubarth [U] — NEW_CHARACTERS
    "MWG": ("mwg_cadwgan_ap_meurig", "1055.1.1", 0),      # Cadwgan ap Meurig of Morgannwg [U] — NEW_CHARACTERS
    "GWT": ("gwt_caradog_ap_gruffydd", "1063.1.1", 0),    # Caradog ap Gruffydd — the 1065 Portskewett raid places him — NEW_CHARACTERS
    "DUB": ("lei_murchad_mac_diarmata", "1061.1.1", 0),   # Murchad mac Diarmata, king of Dublin for his father — AUTHORED SINCE THE CELTIC PASS, seated at last
    "MTH": ("mth_conchobar_ua_mael_sechlainn", "1030.1.1", 0), # Conchobar Ua Mael Sechlainn of Mide [U] — NEW_CHARACTERS
    "MOY": ("moy_mael_snechtai", "1058.1.1", 0),          # Mael Snechtai mac Lulaig of Moray [U] — vanilla's loairn_dynasty — NEW_CHARACTERS

    # Southern Italy 1066 (Opus package 2026-07-29; the SIC-advance
    # gates, SAO's one-location Malta, the name-key pool and every
    # birthplace re-verified by the main session). AGR stays
    # `ruler = random` on purpose: Ibn al-Hawwas died 1064 OR 1068 [D]
    # — a seated ruler would be a coin flip on whether he is alive.
    "APU": ("apu_robert_guiscard", "1059.8.1", 1),        # Robert Guiscard, Duke of Apulia and Calabria by the Melfi investiture [U] — NEW_CHARACTERS
    "SIC": ("sic_roger_de_hauteville", "1062.1.1", 1),    # Roger I, Count of Sicily from his Val Demone beachhead [U] — NEW_CHARACTERS
    "CUP": ("cup_richard_i_drengot", "1058.5.12", 1),     # Richard I Drengot, Prince of Capua (the city itself 1062) — NEW_CHARACTERS
    "SLR": ("slr_gisulf_ii_salerno", "1052.6.3", 2),      # Gisulf II of Salerno — succeeded on Guaimar IV's murder; falls to Guiscard 1077 — NEW_CHARACTERS
    "NEA": ("nea_sergius_v_naples", "1050.1.1", 5),       # Sergius V, Duke of Naples [D on dates] — NEW_CHARACTERS
    "GAE": ("gae_atenulf_i_aquino", "1064.1.1", 1),       # Atenulf I of Aquino, Duke of Gaeta [U] — NEW_CHARACTERS
    "PLM": ("plm_ayyub_ibn_tamim", "1063.1.1", 1),        # Ayyub ibn Tamim, emir of Palermo — son of OUR seated Tamim of TUN [U/D] — NEW_CHARACTERS

    # The Empire (HRE package 2026-07-29; the leaderless-election law,
    # the German-kingship no-hole term, the margraviate free win and
    # every name route re-verified by the main session). THE CROWN is
    # user decision D: Heinrich IV on a landed OGK with the Standard
    # 9-location Salian demesne, styled "King of the Romans" (loc
    # override) — the 1084 imperial coronation is a future event hook.
    # TRI stays random ([D] — three archbishops in one year); SPL
    # ships random (Godfrey the Bearded parks with Germany II); ZAH
    # random (Berthold seats CRH).
    "OGK": ("ogk_heinrich_iv_salier", "1056.10.5", 4),    # Heinrich IV — vanilla's OWN character and term values (10_countries.txt:34907); 15 at start — MINOR_RULERS
    "HAB": ("hab_ernst_babenberg", "1055.1.1", 1),        # Ernst the Brave, Margrave of Austria 1055-1075 [U] — NEW_CHARACTERS
    "CRH": ("crh_berthold_zahringen", "1061.1.1", 1),     # Berthold I of Zähringen, titular Duke of Carinthia [U/D — the Eppensteiner held it de facto] — NEW_CHARACTERS
    "STY": ("sty_otakar_steyr", "1056.1.1", 0),           # Otakar of Steyr, Margrave of the Carinthian March [U; ordinal disputed — 0] — NEW_CHARACTERS

    # GERMANY II (Opus package 2026-07-29; the formable-reuse ground for
    # SAX/SWA, all fourteen invented name keys, every donor tag and every
    # birthplace re-verified by the main session). The two stem duchies
    # come back on the tags Paradox ships as formables only, the fifteen
    # imperial sees get their 1066 bishops, and Godfrey the Bearded takes
    # TWO seats: ONE character on BLL and SPL, which is vanilla's own
    # pluralist route (boh_john_luxembourg rules BOH and LUX — one
    # character, one `ruler =` line and one term per tag; KNOWLEDGE.md).
    # Deliberately left `ruler = random`, reasons recorded: FKN (there is
    # no 1066 duke of Franconia — the ducal authority is the king's own),
    # HES/THU/GEL/JUL/BRG/KLE/GMK and the Tier-E minors (no safely
    # nameable 1066 ruler), NAM (Albert III from 1063 [U] — one source,
    # the BER-precedent honesty). Einhard of Speyer, Benno of Osnabrück,
    # Otto of Regensburg and Egbert of Brunswick all die within eighteen
    # months of start: ACCEPTED drift, flavor-event material later, not
    # an engine problem (a death_date on a living character starts him
    # dead — the rule that forbids the "fix").
    # All 29 rows below are authored characters (NEW_CHARACTERS): vanilla
    # ships no German alive in 1066 outside Heinrich IV's own line.
    "SWA": ("swa_rudolf_rheinfelden", "1057.1.1", 1),     # Rudolf of Rheinfelden, Duke of Swabia 1057-1079 — the future anti-king
    "SAX": ("sax_ordulf_billung", "1059.6.29", 1),        # Ordulf Billung, Duke of Saxony on his father Bernard II's death
    "KOL": ("kol_anno_ii", "1056.1.1", 2),                # Anno II, Archbishop of Cologne — regent of the Empire after Kaiserswerth
    "TRI": ("tri_udo_nellenburg", "1066.6.1", 1),         # Udo of Nellenburg, Archbishop of Trier — enthroned months before start [U]
    "BLL": ("bll_godfrey_iii_bearded", "1065.1.1", 3),    # Godfrey III the Bearded, Duke of Lower Lorraine from 1065
    "SPL": ("bll_godfrey_iii_bearded", "1057.1.1", 3),    # THE SAME character, Margrave of Tuscany/Spoleto by his 1054 marriage to Beatrice — the pluralist route
    "MEI": ("mei_otto_weimar", "1062.1.1", 1),            # Otto of Weimar-Orlamünde, Margrave of Meissen [U]
    "LUX": ("lux_conrad_i", "1059.1.1", 1),               # Conrad I, Count of Luxembourg [U]
    "HAI": ("hai_baldwin_i_hainaut", "1051.1.1", 1),      # Baldwin I of Hainaut — son of OUR seated Baldwin V of Flanders (the Ayyub/Tamim cross-tag shape)
    "UTR": ("utr_william_i", "1054.1.1", 1),              # William I, Prince-Bishop of Utrecht
    "LIE": ("lie_theodwin", "1048.1.1", 1),               # Theoduin, Prince-Bishop of Liège
    # The fifteen sees. Bishops carry NO dynasty (the mai_siegfried_i
    # precedent — dynasty-less characters are vanilla-attested), and no
    # regnal_name: the German episcopate had no papal-style regnal
    # convention, so the term's regnal_number carries the numeral alone.
    "BRE": ("bre_adalbert_goseck", "1043.1.1", 1),        # Adalbert of Goseck, Archbishop of Hamburg-Bremen — Heinrich IV's other regent
    "MAG": ("mag_werner_steusslingen", "1064.1.1", 1),    # Werner of Steusslingen, Archbishop of Magdeburg — Anno's own house
    "WBG": ("wbg_adalbero", "1045.1.1", 1),               # Adalbero, Bishop of Würzburg — later a Gregorian, deposed 1085
    "BAM": ("bam_herman_i", "1065.1.1", 1),               # Herman I, Bishop of Bamberg
    "HDH": ("hdh_hezilo", "1054.1.1", 1),                 # Hezilo, Bishop of Hildesheim
    "HBS": ("hbs_burchard_ii", "1059.1.1", 2),            # Burchard II, Bishop of Halberstadt
    "MUN": ("mun_friedrich", "1063.1.1", 1),              # Frederick, Bishop of Münster [U]
    "PDB": ("pdb_imad", "1051.1.1", 1),                   # Imad, Bishop of Paderborn
    "SLZ": ("slz_gebhard", "1060.1.1", 1),                # Gebhard, Archbishop of Salzburg — the one firm Gregorian in the German south
    "PSS": ("pss_altmann", "1065.1.1", 1),                # Altmann, Bishop of Passau
    "EIC": ("eic_gundekar_ii", "1057.1.1", 2),            # Gundekar II, Bishop of Eichstätt
    "KNZ": ("knz_rumold", "1051.1.1", 1),                 # Rumold, Bishop of Constance [U]
    "SPY": ("spy_einhard", "1060.1.1", 1),                # Einhard, Bishop of Speyer — dies February 1067, accepted drift
    "OSN": ("osn_benno_i", "1052.1.1", 1),                # Benno I, Bishop of Osnabrück — dies December 1067, accepted drift
    "REG": ("reg_otto_riedenburg", "1060.1.1", 1),        # Otto of Riedenburg, Bishop of Regensburg — dies 1067, accepted drift
    # The eastern marches and the Rhine.
    "SOR": ("sor_dedi_i", "1046.1.1", 1),                 # Dedi I of Wettin, Margrave of the Saxon Ostmark (Lusatia) [U]
    "PAL": ("pal_hermann_ii", "1064.1.1", 2),             # Hermann II of the Ezzonen, Count Palatine of the Rhine — SEVENTEEN at start, no MINOR_RULERS needed
    "BRU": ("bru_egbert_i", "1057.1.1", 1),               # Egbert I the Brunonen, Margrave of Meissen and Count of Brunswick — dies January 1068, accepted drift

    # ITALY NORTH (approved package 2026-07-29, landed by the main session
    # 2026-07-30). TUS revives on the SAX/SWA formable-reuse ground and
    # Beatrice rules the march; ISR is the slice's one new tag. Two vanilla
    # characters seat without authoring: MFA matches vanilla's own term
    # exactly (10_countries.txt:10387) and PAD is a CROSS-TAG seat of
    # vanilla's mlo_alberto_azzo_ii_este (the PYS/kie_ precedent) — Azzo's
    # real county was Este/Padua; vanilla's term for him (:10604) sits on
    # MLO, Visconti-era Milan. Deliberately `ruler = random`, reasons
    # recorded: MLO/GEN/PIS/VER/BLG (the communal shapes are BANKED
    # anachronisms, package section H — no 1066 signore existed to seat).
    # PAR regnal note: the package table said 2, but Cadalus is Parma's
    # FIRST of the name — the "II" belongs to his 1061 antipapal style
    # Honorius II, which the package itself forbids modeling; 0 is the
    # project's no-ordinal honesty value (vanilla's own, 184 uses).
    "TUS": ("tus_beatrice_di_bar", "1052.5.6", 0),        # Beatrice of Bar, margravine of Tuscany from Boniface III's murder — NEW_CHARACTERS
    "ISR": ("isr_ulrich_i_weimar", "1060.1.1", 1),        # Ulric I of Weimar, margrave of Carniola and Istria [U] — NEW_CHARACTERS
    "AQU": ("aqu_ravengerius", "1063.1.1", 0),            # Ravenger, Patriarch of Aquileia [U] — NEW_CHARACTERS
    "RAV": ("rav_henry_ravenna", "1051.1.1", 0),          # Henry, Archbishop of Ravenna [U] — NEW_CHARACTERS
    "PAR": ("par_cadalus", "1045.1.1", 0),                # Cadalus, Bishop of Parma (the future antipope — situation material, not data) — NEW_CHARACTERS
    "PIE": ("pie_adelaide_susa", "1034.1.1", 0),          # Adelaide of Susa, margravine of Turin — NEW_CHARACTERS
    "MFA": ("mfa_ottone_ii_monferrato", "1045.1.1", 2),   # Otto II of Montferrat — vanilla character, vanilla's own term values
    "PAD": ("mlo_alberto_azzo_ii_este", "1029.1.1", 2),   # Albert Azzo II d'Este on his real county — vanilla character, cross-tag seat

    # Southeast Asia, 1066 (docs/SEA-PACKAGE.md §C, user-approved
    # 2026-08-02). TWO seats — the attested set; the rest of the theater
    # stays random, the Pecheneg discipline. Held back with reasons
    # recorded: PLB (the 1067 San-fo-qi mission's ruler-name
    # Ti-hua-kia-lo is a disputed Chinese transcription [D]), KDR/JGL
    # (the post-1049 Javanese king-lists have decade-wide gaps [D]),
    # BLI (Anak Wungsu is a title-form, not a name — package decision 6,
    # the Cadalus honesty rule), ARK/HPJ (chronicle king-lists [D]).
    "PGN": ("pgn_anawrahta", "1044.8.11", 0),             # Anawrahta of Pagan, r. 1044-1077 [D on the day]; d. 1077 left to the engine — NEW_CHARACTERS
    "LAV": ("adh_narai", "1052.1.1", 0),                  # Narai of Lavo [D] — VANILLA character (b. 1020 at lopburi, lavo_dynasty, death already stripped), cross-tag seat like PAD/PYS

    # Tibet, 1066 (docs/TIBET-PACKAGE.md §C + open decision 4, main-
    # session call under the user's direct-implement authorization,
    # 2026-08-02). ONE seat: Dongzhan of Tsongkha, r. 1065-1086 [D] —
    # the only ruler in or near the theater whose accession is dated
    # to the year and covers 1066.9.15. The package recommended nobody
    # because "Dongzhan" is the Song shi's Chinese transcription of an
    # unsettled Tibetan name [D]; overruled on the Tunka Manin
    # precedent — an attested ruler known only through an external
    # source's transcription, seated by user decision in the Africa
    # slice (AFRICA-PACKAGE STATUS band, decision 8). Everyone else on
    # the plateau stays random: Guge's Tsede-vs-Jangchub-Ö reading is
    # disputed [D], Maryul's king-list is a late chronicle [D], and Ü/
    # Tsang had no ruler at all to name (package §C — the honest
    # silence is the point).
    "TKA": ("tka_dongzhan", "1065.1.1", 0),               # Dongzhan of Tsongkha [D on the day] — NEW_CHARACTERS; d. 1086 left to the engine
}

# Tags whose 1066 ruler was HISTORICALLY a minor. The adult-age check skips
# them — the engine gives them a regency, which is the history (France was
# governed by Baldwin V of Flanders as regent). The check still fails if a
# listed tag's ruler turns out to be an adult, so stale entries cannot rot.
MINOR_RULERS = {"FRA", "HOL", "HUN",
                # Heinrich IV is 15y 10m at start (b. 1050.11.11);
                # historically of age March 1065 [U] but ADULT_AGE=16
                # rules — the engine regency stands in for the
                # lingering Anno/Adalbert tutelage (HRE slice).
                "OGK"}

# ---------------------------------------------------------- new countries ---
# The NEW-COUNTRIES-DESIGN.md mechanism, first probe: PEREYASLAVL. One tag,
# five locations out of Kyiv's left bank, and a ruler vanilla already ships
# (Vsevolod I, the third triumvir). NOTE the probe's own first launch
# DISPROVED this comment's original "no identity block needed" claim —
# identity blocks are MANDATORY (country_manager.cpp:206; the registry
# is zz_1066_new_countries.txt, whose header records the correction).
# Tag id absent from every vanilla database (PYS — checked), KIE's own
# include templates. Borders are PROVISIONAL pending the Rus territory
# pass. `PER` is Perigord — never reuse it for Pereyaslavl.
NEW_COUNTRIES = {
    "PYS": """\tPYS = {
\t\town_control_core = {
\t\t\tpereiaslav desnyanskyi_horodok boryspil oster kozelets
\t\t}

\t\tstarting_technology_level = 3
\t\tinclude = "expl_eastern_europe"
\t\tinclude = "ruthenian_principality_no_coast"
\t\tgovernment = {
\t\t\their_selection = partition_inheritance
\t\t}
\t\tcapital = pereiaslav
\t\tcountry_rank = rank_duchy
\t}
""",
}

# tag -> the locations it takes at start. The generator removes each from
# whatever ownership list currently carries it and asserts exclusivity.
LOCATION_TRANSFERS = {
    "PYS": ["pereiaslav", "desnyanskyi_horodok", "boryspil", "oster", "kozelets"],
}

# ------------------------------------------------------------- the taifas ---
# THE TAIFA FACTORY (Opus Iberia data package 2026-07-28; rank trigger, LON
# precedent, reform gate, tag freeness and the three missing name keys all
# re-verified by the main session). Thirteen Muslim states at 1066.9.15;
# 244 locations leave CAS 131 / ARA 47 / POR 38 / GRA 18 / MLL 5 / MOR 4 /
# NAV 1. Block template: vanilla GRA (10_countries.txt:14801) minus all
# Nasrid-specific content (its 1238+ ruler_terms, its regnal_numbers, the
# GRA-gated jewel_of_alandalus reform, its claims). "Taifa of X" display is
# free — rank_duchy_andalusi (customizable_localization/country_ranks.txt
# :1688) fires on duchy rank + Iberian capital + muslim religion, and
# EXCLUDES `tag = GRA`: that exclusion is why Zirid Granada is the fresh
# tag GRZ and vanilla GRA goes landless (LON shape) rather than reused.
# No Valencia tag: al-Ma'mun of Toledo annexed it in 1065 [U]. Alpuente's
# town has no map location — chelva stands in (the known definitions gap).
_TAIFAS = {
    # tag: (capital, [locations — whole vanilla provinces unless the
    #                 package's judgment notes say otherwise])
    "SEV": ("sevilla", [
        "sevilla", "constantina", "coria_del_rio", "ecija", "moron",
        "olvera", "osuna", "sanlucar_la_mayor",
        "huelva", "almonaster_la_real", "aracena", "aroche", "ayamonte",
        "niebla", "puebla_de_guzman",
        "cadiz", "arcos_de_la_frontera", "jerez_de_la_frontera",
        "medina_sidonia", "sanlucar", "tarifa",
        "algeciras", "gibraltar",
        "lagos", "faro", "silves", "tavira",
        "mertola"]),
    "BDJ": ("badajoz", [
        "badajoz", "albuquerque", "barcarrota", "jerez_de_los_caballeros",
        "villanueva_del_fresno",
        "caceres", "alcantara", "arroyo", "brozas", "valencia_de_alcantara",
        "merida", "azuaga", "llerena", "monesterio", "montanchez", "zafra",
        "plasencia", "galisteo", "granadilla", "jaraicejo", "valverde",
        "trujillo", "escurial", "herrera", "puebla_de_alcocer",
        "villanueva_de_la_serena", "belalcazar", "medellin", "zalamea",
        "evora", "avis", "crato", "elvas", "estremoz", "montemor",
        "portalegre", "portel", "vila_vicosa",
        "beja", "alvalade", "alvito", "moura", "odemira", "ourique",
        "serpa", "sines",
        "lisbon", "alcacer_do_sal", "alcobaca", "setubal", "torres_vedras",
        "santarem", "mora_portugal", "ponte_sor", "salvaterra", "tomar",
        "torres_novas",
        "castelo_branco", "covilha", "idanha", "proenca_nova", "sabugal",
        "coria"]),
    "TOL": ("toledo", [
        "toledo", "guadalupe", "illescas", "los_yebenes", "navalucillos",
        "puebla_de_montalban", "puente_arzobispo", "talavera_de_la_reina",
        "alarcon", "belmonte", "iniesta", "jorquera", "moya",
        "san_clemente", "requena",
        "alcaraz", "lezuza", "alhambra_location", "montiel",
        "villapalacios", "villarobledo",
        "ciudad_real", "almaden", "almodovar_del_campo", "calatrava",
        "malagon", "manzanares", "puertollano",
        "guadalajara", "brihuega", "buitrago_de_lozoya", "cobeta",
        "siguenza", "zorita",
        "cuenca", "beteta", "canete", "huete", "molina_de_aragon",
        "pareja", "torralba",
        "madrid", "alcala_de_henares", "colmenar", "el_escorial", "maqueda",
        "ocana", "alcazar_de_san_juan", "chinchon", "consuegra",
        "tomelloso", "ucles",
        "valencia", "bunol", "lliria",
        "castellon_de_la_plana", "ares_del_maestre", "llucena", "morella",
        "peniscola",
        "jativa", "ayora"]),
    "CRD": ("cordoba", [
        "cordoba", "baena", "carpio", "espiel", "fuenteovejuna", "lucena",
        "palma_del_rio", "pedroche", "santa_eufemia"]),
    "GRZ": ("granada", [
        "granada", "adra", "almunecar", "guadix", "illora", "loja",
        "pinar", "orgiva",
        "malaga", "antequera", "velez_malaga",
        "marbella", "ronda",
        "jaen", "andujar", "baeza", "cazorla", "jodar", "martos", "ubeda"]),
    "ALM": ("almeria", [
        "almeria", "almanzora", "baza", "gergal", "huescar", "mojacar",
        "velez_rubio"]),
    "MRU": ("murcia", [
        "murcia", "cartagena", "lorca", "mula",
        "hellin", "caravaca", "cieza", "segura_de_la_sierra",
        "albacete", "chinchilla", "villena", "jumilla",
        "orihuela", "alicante", "elche"]),
    "DYA": ("denia", [
        "palma", "ciudadela_de_menorca", "ibiza", "manacor", "pollensa",
        "denia", "gandia", "alcoy"]),
    "ZGZ": ("zaragoza", [
        "zaragoza", "belchite", "pina_de_ebro", "tarazona", "zuera",
        "calatayud", "ariza", "carinena", "daroca",
        "alcaniz", "cantavieja", "caspe", "montalban", "valderrobres",
        "huesca", "almudevar", "ejea_de_los_caballeros",
        "barbastro", "monzon", "sarinena",
        "tortosa", "tudela"]),
    "LRD": ("lleida", ["lleida", "flix", "fraga", "balaguer"]),
    "ABR": ("albarracin", [
        "teruel", "albarracin", "alfambra", "mora_de_rubielos"]),
    "ALP": ("chelva", ["chelva"]),
    "QRM": ("carmona", ["carmona"]),
}

# The engine self-heals coastal template content on inland countries,
# one error line per removal (government.cpp:3662,
# sponsor_maritime_contracts — measured 2026-07-29 on exactly these
# five). Vanilla's answer is the template's _no_coast variant; it
# carries NO heir_selection of its own (measured by diff against the
# coastal one), so the heir line is restated explicitly to keep the
# shipped behavior byte-identical.
_TAIFAS_INLAND = {"CRD", "LRD", "ABR", "ALP", "QRM"}

def _taifa_block(tag, capital, locs):
    inland = tag in _TAIFAS_INLAND
    gov_tpl = ("muslim_monarchy_no_abrahamic_dhimmi_no_coast" if inland
               else "muslim_monarchy_no_abrahamic_dhimmi")
    inc = "".join(f'\t\tinclude = "{i}"\n' for i in (
        "expl_muslim_mediterranean", "expl_silk_road_west",
        "expl_silk_road_center", "expl_silk_road_east",
        "expl_indian_trade_route", gov_tpl))
    heir = ("\t\t\their_selection = cognatic_primogeniture\n" if inland
            else "")
    return (f"\t{tag} = {{\n"
            f"\t\town_control_core = {{\n\t\t\t{' '.join(locs)}\n\t\t}}\n\n"
            f"\t\tstarting_technology_level = 3\n{inc}\n"
            f"\t\tgovernment = {{\n{heir}\t\t\tlaws = {{\n"
            f"\t\t\t\tsharia_law = maliki_policy\n\t\t\t}}\n\t\t}}\n"
            f"\t\tcourt_language = maghrebi_dialect\n"
            f"\t\treligious_school = maliki_school\n"
            f"\t\tgovernment = {{ mysticism_vs_jurisprudence = -5 }}\n\n"
            f"\t\tcountry_rank = rank_duchy\n\n"
            f"\t\ttolerated_cultures = {{\n\t\t\tsephardi\n\t\t}}\n\n"
            f"\t\tcapital = {capital}\n\t}}\n")

for _t, (_cap, _locs) in _TAIFAS.items():
    if _cap not in _locs:
        sys.exit(f"_TAIFAS: {_t} capital {_cap} not in its own location list")
    if len(set(_locs)) != len(_locs):
        sys.exit(f"_TAIFAS: {_t} lists a location twice")
    NEW_COUNTRIES[_t] = _taifa_block(_t, _cap, _locs)
    LOCATION_TRANSFERS[_t] = list(_locs)
if sum(len(l) for _, l in _TAIFAS.values()) != 244:
    sys.exit("_TAIFAS: the package moves exactly 244 locations — a list changed")

# --------------------------------------------------- the Pyrenean counties ---
# CHRISTIAN IBERIA (Opus package, terms/tags/comments re-verified). The six
# counties Ramon Berenguer I did NOT rule. Block shape per vanilla FOI
# (10_countries.txt:13755, a two-location Pyrenean county); country_rank
# written explicitly (rank_county = the "County of X" fallback branch).
# Vanilla's own comments assign MLL's residual: `puigcerda prades #County
# of Cerdanya`, `perpignan #County of Roselló` (10_countries.txt:14436-7).
_COUNTIES = {
    # tag: (capital, coastal, [locations])
    "URG": ("seu_durgell", False, ["seu_durgell", "agramunt"]),
    "BSL": ("besalu", False, ["besalu", "ripoll"]),
    "CDY": ("puigcerda", False, ["berga", "puigcerda", "prades"]),
    "EPU": ("castellon_ampurias", True, ["castellon_ampurias"]),
    "RSL": ("perpignan", True, ["perpignan"]),
    "PLJ": ("talarn", False, ["talarn"]),
}

def _county_block(tag, capital, coastal, locs):
    mon = "catholic_monarchy" if coastal else "catholic_monarchy_no_coast"
    return (f"\t{tag} = {{\n"
            f"\t\town_control_core = {{\n\t\t\t{' '.join(locs)}\n\t\t}}\n\n"
            f"\t\tstarting_technology_level = 3\n"
            f'\t\tinclude = "expl_western_europe"\n'
            f'\t\tinclude = "{mon}"\n\n'
            f"\t\tcountry_rank = rank_county\n\n"
            f"\t\tcapital = {capital}\n\t}}\n")

for _t, (_cap, _coastal, _locs) in _COUNTIES.items():
    if _cap not in _locs:
        sys.exit(f"_COUNTIES: {_t} capital {_cap} not in its own location list")
    NEW_COUNTRIES[_t] = _county_block(_t, _cap, _coastal, _locs)
    LOCATION_TRANSFERS[_t] = list(_locs)
if sum(len(l) for _, _, l in _COUNTIES.values()) != 10:
    sys.exit("_COUNTIES: the package moves exactly 10 locations — a list changed")

# Christian Iberia grants to EXISTING tags: the three brothers' realms,
# Navarre's Basque+Rioja restoration (vanilla itself marks the nine Basque
# locations as NAV cores), and montpellier handed to FRA (Languedoc is the
# France slice's problem; vanilla's comment calls it a Lordship).
# Merged into LOCATION_GRANTS right after its definition below.
_IBERIA_GRANTS = ({
    "LON": ["astorga", "castrocalbon", "ponferrada", "villablino",
            "villafranca_bierzo", "benavente", "alcanices",
            "puebla_de_sanabria", "villalpando", "ciudad_rodrigo", "ledesma",
            "san_felices", "yecla_de_yeltes", "villaviciosa", "cangas",
            "llanes", "mieres", "leon", "mansilla", "riano", "sahagun",
            "salamanca", "alba_de_tormes", "bejar", "matilla_de_canos",
            "piedrahita", "oviedo", "aviles", "castropol", "tineo",
            "zamora", "alba_de_aliste", "fermoselle", "toro"],
    "GLC": ["coruna", "betanzos", "ferrol", "mondonedo", "vivero", "lugo",
            "monforte_de_lemos", "navia_de_suarna", "sarria", "villalba",
            "ourense", "barco_de_valdeorras", "ginzo_de_limia", "monterrey",
            "ribadavia", "viana_bolo", "santiago_compostela", "finisterre",
            "lalin", "mellid", "noya", "pontevedra", "tuy",
            "viseu", "besteiros", "guarda", "lamego", "meda", "pinhel",
            "seia", "trancoso", "coimbra", "chao_de_couce", "esgueira",
            "feira", "figueira", "leiria", "porto", "barcelos", "braga",
            "guimaraes", "valenca", "viana_do_castelo", "braganca",
            "aguiar", "chaves", "macedo", "miranda_de_i_douro", "mirandela",
            "moncorvo", "montalegre", "vila_real"],
    "NAV": ["vitoria", "anana", "salvatierra", "bilbao", "durango",
            "valmaseda", "san_sebastian", "onate", "tolosa",
            "logrono", "najera", "calahorra", "arnedo"],
    "CAT": ["barcelona", "sitges", "terrassa", "villafranca_del_penedes",
            "girona", "sant_feliu", "vic", "cardona", "cervera", "manresa",
            "tarragona", "montblanc", "tarrega"],
    # montpellier was parked here ("FRA": ["montpellier"] — the
    # Languedoc slice's problem) from the day MLL went landless. The
    # Languedoc slice ARRIVED (France demesne, 2026-07-29): TOU's
    # nimois sweep now takes montpellier straight out of MLL, and a
    # second FRA grant would violate the disjointness assert — which
    # is exactly how the parking's retirement was caught.
})

# -------------------------------------------------- pre-Manzikert Byzantium ---
# THE BYZANTIUM SLICE (Opus package, key claims re-verified). Constantine X
# already reigns (the ruler layer shipped earlier); this is territory. The
# 495-location grant list is RESOLVED FROM definitions.txt at build time
# rather than transcribed — the package's rule set (whole region/areas/
# provinces + explicit singles) is data, the parser walks vanilla's own
# tree, and the exact-count assertion pins the result. A location is
# ownable land iff its location_templates.txt block carries a culture
# field; wastelands, lakes and seas never enter the list.
def _parse_defs():
    s = open(os.path.join(VAN, "in_game", "map_data", "definitions.txt"),
             encoding="utf-8-sig").read()
    s = re.sub(r"#[^\n]*", "", s)
    toks = re.findall(r"[A-Za-z0-9_]+|=|\{|\}", s)
    members, stack = {}, []
    i, n = 0, len(toks)
    while i < n:
        t = toks[i]
        if i + 2 < n and toks[i + 1] == "=" and toks[i + 2] == "{":
            stack.append(t)
            members.setdefault(t, [])
            i += 3
            continue
        if t == "}":
            if stack:
                stack.pop()
            i += 1
            continue
        for name in stack:
            members[name].append(t)
        i += 1
    return members

def _ownable_set():
    s = open(os.path.join(VAN, "in_game", "map_data", "location_templates.txt"),
             encoding="utf-8-sig").read()
    own = set()
    for m in re.finditer(r"^([A-Za-z0-9_]+)[ \t]*=[ \t]*\{", s, re.M):
        end = find_block_end(s, s.index("{", m.start()))
        if re.search(r"\bculture[ \t]*=", s[m.start():end]):
            own.add(m.group(1))
    return own

# The package's rule set, verbatim: sweep names resolve recursively, the
# singles are explicit. lezha (theme of Dyrrhachion, currently SER) is the
# package's recommended addition, listed here explicitly.
_BYZ_SWEEP = [
    "anatolia_region",
    "macedonia_area", "thrace_area", "bulgaria_area",
    "northern_greece_area", "morea_area", "aegean_archipelago_area",
    "albania_province", "north_epirus_province",
    "branicevo_province", "kosovo_province", "nis_province",
    "toplica_province", "sumadija_province", "macva_province",
    "vardar_province", "prilep_province",
    "ani_province", "kars_province", "erzurum_province",
    "malazgirt_province", "antakya_province", "latakia_province",
]
_BYZ_SINGLES = [
    "zadar", "split", "brac", "sremska_mitrovica", "petrovaradin", "ilok",
    "yerevan", "bjni", "khor_virap", "igdir",
    "van", "bargiri", "ercis", "hosap",
    "mus",
    "oltu", "tortum", "ispir", "panaskerti",
    "ayntab", "dluk", "trapessac",
    "urfa", "birecik", "siverek", "suruc", "harran",
    "theodoro", "lusta", "soldaia", "vosporo",
    "lezha",
]

_DEFS_CACHE = {}
def _defs():
    if "m" not in _DEFS_CACHE:
        _DEFS_CACHE["m"] = _parse_defs()
        _DEFS_CACHE["o"] = _ownable_set()
    return _DEFS_CACHE["m"], _DEFS_CACHE["o"]

def _resolve_ruleset(ctx, sweep, singles, minus_sweeps, minus_singles):
    members, ownable = _defs()
    minus = set(minus_singles)
    for name in minus_sweeps:
        if name not in members:
            sys.exit(f"{ctx}: minus-sweep {name} not in definitions.txt")
        minus.update(members[name])
    target, seen = [], set()
    for name in sweep:
        if name not in members:
            sys.exit(f"{ctx}: {name} not found in definitions.txt")
        # seen is updated DURING the walk, not after: vanilla's own
        # definitions.txt ships a self-nested duplicate province
        # (limousin_province wraps itself, :944-945) whose members
        # arrive twice from _defs — the old after-the-fact update let
        # both copies through and a grant list with duplicated tokens
        # fails the exclusivity validate (found by the France slice,
        # 2026-07-29).
        got = []
        for l in members[name]:
            if l in ownable and l not in seen and l not in minus:
                got.append(l)
                seen.add(l)
        target.extend(got)
    for l in singles:
        if l not in ownable:
            sys.exit(f"{ctx}: single {l} is not an ownable location")
        if l not in seen and l not in minus:
            target.append(l)
            seen.add(l)
    return target

def _byz_target():
    members, ownable = _defs()
    target = []
    seen = set()
    for name in _BYZ_SWEEP:
        if name not in members:
            sys.exit(f"_BYZ_SWEEP: {name} not found in definitions.txt")
        all_own = [l for l in members[name] if l in ownable]
        if not all_own:
            sys.exit(f"_BYZ_SWEEP: {name} holds zero ownable locations")
        # zero NEW is legal: vardar/prilep sit inside macedonia_area and
        # resolve fully covered — the 495 count assert is the real guard
        got = [l for l in all_own if l not in seen]
        target.extend(got)
        seen.update(got)
    for l in _BYZ_SINGLES:
        if l not in ownable:
            sys.exit(f"_BYZ_SINGLES: {l} is not an ownable location")
        if l not in seen:
            target.append(l)
            seen.add(l)
    return target

# The Serbian world at 1066, on tags Paradox already ships landless with
# claims (the Sardinia trick generalized — package section 6): Duklja
# under Mihailo is the leading Serbian power; Rascia keeps its highlands;
# Travunia and Zahumlje are carved small; Bosnia stays independent.
# taman: Tmutarakan was Chernihiv's appanage (Gleb Sviatoslavich restored
# 1066) — TRE's only non-transfer holding goes to the Rus, closing the
# TRE 1204 exemption. koman/has/dukagjini are [U] Skadar hinterland.
_BYZ_GRANTS = {
    "ZTA": ["podgorica", "bar_cg", "gradina", "kotor", "onogost",
            "shkoder", "koman", "has", "dukagjini"],
    "TRO": ["trebinje", "gacko"],
    "HUM": ["mostar", "nevesinje", "drijeva", "metkovic", "makarska"],
    "CHR": ["taman"],
}

# ----------------------------------------------- the Seljuk-Abbasid world ---
# THE SELJUK + ABBASID SLICE (Opus package, 2026-07-29; the tributary
# war-capability law, the dead-code Caliphate branch, tag freeness, name
# keys and dynasties all re-verified by the main session). Alp Arslan's
# empire as a KINGDOM-rank monarchy — the engine's own chain then renders
# "Sultanate of the Great Seljuks" / "Sultan"; empire rank would kill the
# NAME key entirely (the prefix_adjective_rank branch, verified). Nine new
# tags; nine clients as TRIBUTARIES (tributary.txt:88 allow_declaring_wars
# always). MEASURED IN GAME 2026-07-29: the visible gate
# (tributary.txt:20-24 — overlord horde/tribe OR
# modifier:allow_tributary_subject) IS enforced at game start
# (government.cpp:3702 names exactly those lines) and a failing tributary
# is silently DOWNGRADED TO VASSAL — all nine were. The earlier reading
# "vanilla ships monarchy-over-monarchy tributaries so the gate is
# diplomacy-only" was wrong: vanilla's passing overlords are hordes,
# tribe-subjected, or modifier carriers (African advances, Middle
# Kingdom IO, reforms); vanilla's own CHI tributaries (CHA/DAI) broke
# the same way after our Middle Kingdom IO strip. Fix: SEL carries
# seljuk_khutba_reform (in_game/common/government_reforms/
# zz_1066_reforms.txt) granting the modifier — vanilla's own pattern
# for a non-horde overlord (country_specific.txt:3925,
# malian_tribute_system). Whether the reform's modifier lands BEFORE
# the start validator runs is the remaining probe; fallback if it
# fails: accept subject_type = vassal.
# ABS was the theocracy probe and it PASSED (in game 2026-07-29,
# screenshots): explicit type = theocracy beat the include template and
# "Caliphate"/"Caliph" rendered. The branch's third string,
# rank_empire_theocracy_prefix ("Holy"), is loc-overridden to empty —
# the historical name carries no "Holy".
_SELJUK_RULES = {
    # tag: (sweep names, singles, minus-sweeps, minus-singles, expected)
    "SEL": (["azerbaijan_area", "fars_area", "khuzestan_area",
             "kordestan_area", "quhestan_area", "damghan_province",
             "daylam_province", "gorgan_province", "adraskan_province",
             "western_khorasan_area", "eastern_khorasan_area",
             "kath_province", "khiva_province", "uzboy_province",
             "mughan_province", "iraq_ajam_area", "iraq_arabi_area"],
            ["julfa", "nakhchivan"],
            ["yazd_province", "kufa_province"], ["baghdad", "an_nil"], 463),
    "KRM": (["kerman_area"], [], [], [], 48),
    "GHZ": (["ghazni_province", "kabul_province", "kandahar_province",
             "bost_province", "garmsir_province"],
            ["gulistan", "quetta", "shorabak"], [], [], 34),
    "MRD": (["diyarbekir_province", "hasankeyf_province", "mardin_province",
             "nusaybin_province"],
            ["cermik", "ahlat", "bitlis", "tatvan"], [], [], 29),
    "HLB": (["halab_province", "hims_province", "tadmur_province",
             "deir_province"], ["kilis"], [], [], 26),
    "SIS": (["zaranj_province", "zabol_province", "farah_province"],
            [], [], [], 18),
    "UQY": (["mosul_province", "furat_province", "raqqa_province"],
            [], [], [], 17),
    "MZN": (["rustamdar_province", "tabaristan_province"], [], [], [], 10),
    "HLL": (["kufa_province"], ["an_nil"], [], [], 7),
    "KKY": (["yazd_province"], [], [], [], 6),
    "SHD": (["arran_province"], [], [], [], 6),
    "KCN": ([], ["goroz", "shusha"], [], [], 2),
    "ABS": ([], ["baghdad"], [], [], 1),
}
# Kharpert to BYZ — the HANDOFF-deferred Tier 2's resolvable half
# (Byzantine until the 1085 Artuqid emirate [U]); appended to the
# resolved BYZ grant list at build time.
_SELJUK_BYZ_EXTRA = ["adakli", "harput", "keban", "palu"]

# New-tag block classes. Capitals verified in definitions.txt; every
# enum verified against vanilla setup (hanafi_policy x40, jafari_policy
# x3, hanafi_school x45, jafari_school x3 — 10_countries.txt:57737 —
# persian_language court x19, all cultures in in_game/common/cultures).
# A school of None shipped once and the engine flagged every such
# country at init ("has no religious_school specified",
# initialize_from_bookmark.cpp:520, 2026-07-29): the field is required,
# so None is no longer a legal value here.
_SELJUK_TAGS = {
    # tag: (capital, rank, sharia policy, school,
    #       court language or None)
    "SEL": ("rey", "rank_kingdom", "hanafi_policy", "hanafi_school",
            "persian_language"),
    "GHZ": ("ghazni", "rank_kingdom", "hanafi_policy", "hanafi_school", None),
    "UQY": ("mosul", "rank_duchy", "jafari_policy", "jafari_school", None),
    "MRD": ("mayyafariqin", "rank_duchy", "hanafi_policy", "hanafi_school", None),
    "HLB": ("aleppo", "rank_duchy", "jafari_policy", "jafari_school", None),
    "SIS": ("zaranj", "rank_duchy", "hanafi_policy", "hanafi_school", None),
    "KKY": ("yazd", "rank_duchy", "jafari_policy", "jafari_school", None),
    "SHD": ("ganja", "rank_duchy", "hanafi_policy", "hanafi_school", None),
}

def _seljuk_block(tag, capital, rank, policy, school, court):
    # expl_middle_east is the discovery layer: vanilla's own bundle for
    # this theatre (132 uses in 10_countries.txt — CHB and the rest of
    # Mongol-era Persia), granting persia/crescent/caucasus/anatolia/
    # khorasan/arabia/egypt regions. It is REQUIRED, not decorative:
    # expl_silk_road_center is an EMPTY template (every line commented
    # out in vanilla) and a country whose capital is undiscovered fails
    # init ("does not know its capital",
    # initialize_from_bookmark.cpp:528) — playing SEL showed its own
    # empire as terra incognita (2026-07-29 screenshots).
    # Every client (and GHZ) is inland — the engine measured it for us
    # (government.cpp:3662 maritime self-heal lines, 2026-07-29); SEL
    # alone holds coast (the Gulf and the Caspian). The _no_coast
    # variant carries no heir_selection (diff-measured), so it is
    # restated explicitly.
    inland = tag != "SEL"
    gov_tpl = ("muslim_monarchy_no_abrahamic_dhimmi_no_coast" if inland
               else "muslim_monarchy_no_abrahamic_dhimmi")
    inc = "".join(f'\t\tinclude = "{i}"\n' for i in (
        "expl_silk_road_west", "expl_silk_road_center",
        "expl_silk_road_east", "expl_indian_trade_route",
        "expl_middle_east",
        gov_tpl))
    if not school:
        sys.exit(f"_seljuk_block: {tag} has no religious_school — the "
                 "engine requires one (initialize_from_bookmark.cpp:520)")
    # SEL alone carries the two reforms and the Persian bureaucracy as
    # an accepted culture (farsi_culture, cultures/persian.txt:16;
    # both shapes attested at vanilla's ARA block; user-approved
    # 2026-07-29 — the Turkic dynasty rules through Persian
    # administrators, Nizam al-Mulk's world):
    # - seljuk_khutba_reform: allow_tributary_subject, the tributary
    #   gate fix — CONFIRMED working in game 2026-07-29, second launch.
    # - seljuk_nizamiyya_reform: cultures_capacity = 6 (mechanism is
    #   the mandala reform's, country_specific.txt:3909; the MAGNITUDE
    #   is ours — +3 left no room past farsi's 3.89 cost and the other
    #   cultures' levies stayed low, measured in play 2026-07-29).
    gov_extra = ""
    if inland:
        gov_extra += "\t\t\their_selection = cognatic_primogeniture\n"
    if tag == "SEL":
        gov_extra += ("\t\t\treforms = {\n"
                      "\t\t\t\tseljuk_khutba_reform\n"
                      "\t\t\t\tseljuk_nizamiyya_reform\n"
                      "\t\t\t}\n")
    body = (f"\t{tag} = {{\n"
            f"\t\tstarting_technology_level = 3\n{inc}\n"
            f"\t\tgovernment = {{\n{gov_extra}\t\t\tlaws = {{\n"
            f"\t\t\t\tsharia_law = {policy}\n\t\t\t}}\n\t\t}}\n")
    if court:
        body += f"\t\tcourt_language = {court}\n"
    body += f"\t\treligious_school = {school}\n"
    if tag == "SEL":
        body += "\t\taccepted_cultures = { farsi_culture }\n"
    body += (f"\n\t\tcountry_rank = {rank}\n\n"
             f"\t\tcapital = {capital}\n\t}}\n")
    return body

for _t, (_cap, _rank, _pol, _sch, _crt) in _SELJUK_TAGS.items():
    NEW_COUNTRIES[_t] = _seljuk_block(_t, _cap, _rank, _pol, _sch, _crt)

# ABS — the Caliphate probe PASSED in game (2026-07-29, screenshots):
# explicit type = theocracy BEAT the include template's monarchy and
# rank_empire_theocracy rendered our "Caliphate"/"Caliph" strings. The
# same launch showed the cost of bolting theocracy onto a MONARCHY
# include: the template's heir_selection mismatched the government
# (initialize_from_bookmark.cpp:517), its feudal_de_jure_law and
# royal_court_customs_law had no advances under theocracy
# (government.cpp:687 x2), and no school/no discovery were engine
# errors of their own. So the include is GONE and the block is an
# explicit Muslim theocracy, every field cited:
# - heir_selection = theocratic_elective: the theocracy government
#   type's own list, government_types/00_default.txt:73 (same list the
#   catholic_bishopric template picks bishopric_elective from).
# - sharia_law = hanbali_policy (laws/01_legal_system.txt:1024) +
#   religious_school = hanbali_school: al-Qa'im is the caliph of the
#   Qadiri creed — Baghdad's 11th-century Hanbali moment.
# - legal_code_law = sharia_law_policy MUST ride along: the sharia_law
#   law group's potential is has_policy = sharia_law_policy
#   (01_legal_system.txt), and shipping the school policy without its
#   prerequisite got the whole law removed at init with an error line
#   (government.cpp:3535, measured 2026-07-29). The value is the muslim
#   template's own line.
# - expl_middle_east: see _seljuk_block.
NEW_COUNTRIES["ABS"] = (
    "\tABS = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_middle_east"\n'
    "\t\tgovernment = {\n"
    "\t\t\ttype = theocracy\n"
    "\t\t\their_selection = theocratic_elective\n"
    "\t\t\tlaws = {\n"
    "\t\t\t\tlegal_code_law = sharia_law_policy\n"
    "\t\t\t\tsharia_law = hanbali_policy\n"
    # The include-less explicit-theocracy shape carries NO template, so
    # the two laws every template supplies and the thirteen society
    # values must be restated — the engine logged all three absences at
    # start (initialize_from_bookmark.cpp:1558/:1576/:169, first
    # user-observed 2026-07-30). Values are the muslim family's own
    # (setup/templates/muslim_monarchy_no_abrahamic_dhimmi.txt).
    "\t\t\t\tmarriage_law = muslim_marriage\n"
    "\t\t\t\their_religion_law = heir_same_religion\n"
    "\t\t\t}\n"
    "\t\t\tcentralization_vs_decentralization = 40\n"
    "\t\t\ttraditionalist_vs_innovative = -25\n"
    "\t\t\tspiritualist_vs_humanist = -50\n"
    "\t\t\taristocracy_vs_plutocracy = -50\n"
    "\t\t\tserfdom_vs_free_subjects = -30\n"
    "\t\t\tmercantilism_vs_free_trade = -20\n"
    "\t\t\tbelligerent_vs_conciliatory = 30\n"
    "\t\t\tquality_vs_quantity = 10\n"
    "\t\t\toffensive_vs_defensive = -20\n"
    "\t\t\tland_vs_naval = -10\n"
    "\t\t\tcapital_economy_vs_traditional_economy = 70\n"
    "\t\t\tindividualism_vs_communalism = 50\n"
    "\t\t\toutward_vs_inward = -20\n"
    # The FOURTH template item — missed by the 2026-07-30 restatement;
    # the engine kept answering initialize_from_bookmark.cpp:1719 for
    # ABS/FAT until it was added (AUDIT-2026-07-31 D2). Value and
    # position are the muslim template's own
    # (muslim_monarchy_no_abrahamic_dhimmi.txt:19-21).
    "\t\t\tparliament = {\n"
    "\t\t\t\tparliament_type = council\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t\treligious_school = hanbali_school\n\n"
    "\t\tcountry_rank = rank_empire\n\n"
    "\t\tcapital = baghdad\n\t}\n")

# FAT — the Fatimid Caliphate: the ABS explicit-theocracy block's
# Shia/Ismaili variant (the Fatimid slice, Opus package 2026-07-29).
# Field citations beyond ABS's own:
# - sharia_law = ismaili_policy: laws/01_legal_system.txt:1102, whose
#   potential passes ismaili_school (jafari_policy explicitly NORs it);
#   the exact pairing ismaili_policy + ismaili_school is vanilla's own
#   setup at QHT (10_countries.txt:60609), also GLI/SND/DUL/ASR/YAM —
#   7 uses. nizari/mustali schools are post-1094 and wrong for 1066.
# - legal_code_law = sharia_law_policy rides along — the has_policy
#   prerequisite lesson (government.cpp:3535, measured on ABS).
# - discovery: expl_muslim_mediterranean is MAM's own vanilla include
#   and grants crescent_region/arabia_region/egypt_region (:15,:16,:18)
#   — the whole FAT footprint; expl_middle_east adds the Seljuk east
#   (the rival caliphate's world, the Ismaili da'wa's reach).
# - fatimid_khutba_reform: allow_tributary_subject for the MEC/BKZ
#   tributaries (the proven setup-reform-beats-validator route).
# - rank_empire + theocracy → "Fatimid Caliphate"/"Caliph" via the
#   already-shipped tag-independent rank loc overrides.
NEW_COUNTRIES["FAT"] = (
    "\tFAT = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_muslim_mediterranean"\n'
    '\t\tinclude = "expl_middle_east"\n'
    "\t\tgovernment = {\n"
    "\t\t\ttype = theocracy\n"
    "\t\t\their_selection = theocratic_elective\n"
    "\t\t\treforms = {\n"
    "\t\t\t\tfatimid_khutba_reform\n"
    "\t\t\t}\n"
    "\t\t\tlaws = {\n"
    "\t\t\t\tlegal_code_law = sharia_law_policy\n"
    "\t\t\t\tsharia_law = ismaili_policy\n"
    # Same restatement as ABS: the template-less shape must supply the
    # two laws and the society values itself (the .cpp:1558/:1576/:169
    # trio, observed 2026-07-30) — muslim-family values.
    "\t\t\t\tmarriage_law = muslim_marriage\n"
    "\t\t\t\their_religion_law = heir_same_religion\n"
    "\t\t\t}\n"
    "\t\t\tcentralization_vs_decentralization = 40\n"
    "\t\t\ttraditionalist_vs_innovative = -25\n"
    "\t\t\tspiritualist_vs_humanist = -50\n"
    "\t\t\taristocracy_vs_plutocracy = -50\n"
    "\t\t\tserfdom_vs_free_subjects = -30\n"
    "\t\t\tmercantilism_vs_free_trade = -20\n"
    "\t\t\tbelligerent_vs_conciliatory = 30\n"
    "\t\t\tquality_vs_quantity = 10\n"
    "\t\t\toffensive_vs_defensive = -20\n"
    "\t\t\tland_vs_naval = -10\n"
    "\t\t\tcapital_economy_vs_traditional_economy = 70\n"
    "\t\t\tindividualism_vs_communalism = 50\n"
    "\t\t\toutward_vs_inward = -20\n"
    # The fourth template item, exactly as in ABS (the decoder's :1719
    # rule — a template supplies FOUR things).
    "\t\t\tparliament = {\n"
    "\t\t\t\tparliament_type = council\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t\treligious_school = ismaili_school\n\n"
    "\t\tcountry_rank = rank_empire\n\n"
    "\t\tcapital = cairo\n\t}\n")

# ============================ CENTRAL ASIA ==================================
# The Kara-Khanid slice (docs/CENTRAL-ASIA-PACKAGE.md, re-verified and
# user-approved 2026-08-01). Three new tags: the two Kara-Khanid
# kaghanates and Volga Bulgaria. QRK/QRA ride _seljuk_block — the same
# inland Muslim monarchy the Seljuk slice proved in game (the no_coast
# include supplies legal_code_law and parliament_type; heir_selection
# is restated by the block builder). Muslim MONARCHIES, not hordes: by
# 1066 the Karakhanids mint coin, endow Hanafi madrasas and hold the
# khutba — and the horde name branch would kill their NAME keys (the
# JAL law). They will render "Sultanate"/"Sultan" — historically wrong
# (khans and khaqans), accepted by user decision 2026-08-01 and banked
# with SEL for the one country_ranks.txt Muslim-styling override.
# The package's KTT ruleset was DROPPED at review: KTT is a
# steppe_horde (the recipient assert forbids it) and its kulab_province
# sweep stripped QUN's capital kulob — one drop cleared both blockers;
# Khuttal keeps its 4, QUN keeps its 6.
_CENTRALASIA_TAGS = {
    # tag: (capital, rank, sharia policy, school, court language) — the
    # _SELJUK_TAGS shape. Transoxiana was the Hanafi heartland; the
    # karluk court is vanilla's own on CHG, and the Kutadgu Bilig
    # (1069, written for a Karakhanid khan) is three years out.
    "QRK": ("samarkand", "rank_kingdom", "hanafi_policy", "hanafi_school",
            "karluk_language"),
    "QRA": ("balasagun", "rank_kingdom", "hanafi_policy", "hanafi_school",
            "karluk_language"),
}
for _t, (_cap, _rank, _pol, _sch, _crt) in _CENTRALASIA_TAGS.items():
    NEW_COUNTRIES[_t] = _seljuk_block(_t, _cap, _rank, _pol, _sch, _crt)

# BLH — Volga Bulgaria, hand-written: bolghar sits in ural_region,
# which expl_middle_east does NOT grant, so the block carries inline
# discovered_regions (attested 176 times in vanilla's own
# 10_countries.txt; OBD nearby is the shape — its block grants four
# regions, ours three). ruler stays random DELIBERATELY: the Bulgar
# king-list is blank for the whole 11th century — the ARB/GAL/COR
# precedent. rank_duchy + muslim renders "Emirate"/"'Amir", which is
# the amir/malik of the Arabic sources — no styling debt here.
NEW_COUNTRIES["BLH"] = (
    "\tBLH = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_middle_east"\n'
    '\t\tinclude = "muslim_monarchy_no_abrahamic_dhimmi_no_coast"\n'
    "\t\tdiscovered_regions = {\n"
    "\t\t\tural_region\n"
    "\t\t\trussian_region\n"
    "\t\t\truthenia_region\n"
    "\t\t}\n"
    "\t\tgovernment = {\n"
    # The _no_coast variant carries no heir_selection (diff-measured,
    # Seljuk slice) — restated, as everywhere.
    "\t\t\their_selection = cognatic_primogeniture\n"
    "\t\t\tlaws = {\n"
    "\t\t\t\tsharia_law = hanafi_policy\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t\treligious_school = hanafi_school\n\n"
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = bolghar\n\t}\n")

# The definitions-resolved grants (the _SELJUK_RULES 5-tuple shape).
# Counts are the package's, independently reproduced at review.
_CENTRALASIA_RULES = {
    # Western Kara-Khanid Khanate — Transoxiana proper: the Zarafshan
    # (Samarkand, Bukhara), Kish/Nasaf, Amul on the Oxus, Ustrushana,
    # Khujand, Chaghaniyan/Termez. The four Chagatai amir-houses that
    # hold western Transoxiana at 1337 (YSU 15, BRL 13, JLY 9, SLD 9)
    # are EXACTLY the Western Kaghanate, to the location.
    "QRK": (["samarkand_province", "bukhara_province", "nurota_province",
             "amol_province", "kelif_province", "jizzakh_province",
             "khujand_province", "hissar_province"],
            [], [], [], 46),
    # Eastern Kara-Khanid Khanate — Chach, Isfijab, Ferghana, the
    # middle and lower Syr Darya, Semirechye, the Tian Shan, Kashgaria
    # (the Syr Darya reading of the 1040s division, user decision 5).
    # emin_province is subtracted from zhetysu_area: Tarbagatai is
    # Kimek country, not Karakhanid — its six join the vacate list.
    "QRA": (["chach_province", "isbijab_province", "akhsikath_province",
             "andijan_province", "farghana_province", "naryn_province",
             "otrar_province", "turkestan_province",
             "sighnaq_province", "yangikent_province",
             "zhetysu_area",
             "kashgar_province", "yarkand_province", "khotan_province"],
            ["charchan", "niya", "mazar_tagh"],
            ["emin_province"], [], 142),
    # Volga Bulgaria — the Volga-Kama triangle: Bolghar, Bilyar, Suvar,
    # the Kazan bank. The Mari forest and Bashkiria stay unowned.
    "BLH": (["bolghar_area", "kazan_province"], [], [], [], 28),
}

# LOCATION_VACATED — the new mechanism (user-approved 2026-08-01):
# remove a location from its owner and give it to NOBODY. Unowned land
# is vanilla-attested 7334 times (of 20922 ownable locations —
# identical figure in vanilla and our build). Resolution is
# SNAPSHOT-based inside build_countries — (members of these names) ∩
# (the tag's holdings at that point) — so already-unowned members
# cannot trip the exactly-once assert. Tier A, the Kipchak steppe and
# the Volga-Ural forest edge (168): the Desht-i Kipchak in 1066 had no
# khan, no capital and no attested ruler — the Pecheneg precedent, a
# state is EARNED by events (user decision 2). Tier B, West Siberia
# (116): the Golden Horde holding Tomsk in 1066 is absurd; empty is
# strictly closer to the truth, and a later Siberia slice can fill
# empty land far more easily than it can take it off a horde (user
# decision 9). CHG's 21 (Dzungaria 15 + Emin 6) make CHG landless
# (vacated, not granted to QCH — user decision 11).
LOCATION_VACATED = {
    "GLH": ["desht_kipchak_area", "lower_yik_area", "bashkiria_area",
            "yaransk_province", "mangistau_province", "mangyshlak_province",
            "ust_yurt_province",
            "chimgi_tura_area", "qashliq_area", "omsk_area", "kulykol_area",
            "bursol_area", "suzun_area", "tomsk_area", "surgut_area"],
    "CHG": ["dzungaria_area", "emin_province"],
}
LOCATION_VACATED_EXPECT = {"GLH": 284, "CHG": 21}

# Six Mongol-era tags reduced to zero by the grants + the vacate —
# landless with claims, the established terminal state. Also the SAFE
# state for type = army tags: the mod already ships 14 landless army
# tags and the 2477 class names only tiny-but-LANDED ones (HLG/QUN/
# SLD); if the next error.log shows 2477 lines naming any of these
# six, the fallback is a FIELD_FIXES strip of their type = army line.
# GLH is NOT here: it keeps 404 Pontic/Don/Kuban/Astrakhan locations —
# the Rus/steppe package's seam, a stated compromise.
CENTRALASIA_LANDLESS = ("CHG", "YSU", "BRL", "JLY", "SLD", "DGH")

# ================================ THE RUS ===================================
# Tier 1 of the Rus/steppe package (docs/RUS-STEPPE-PACKAGE.md,
# re-verified 2026-08-01, user-approved same day; the two LIVE defects
# landed separately as the Rus patch). The inverse of inventing: the
# 1066 Rus is FIVE states, all already seated with vanilla Rurikids —
# vanilla ships exactly six adult Rurikids and the sixth (Yaropolk) is
# deliberately unseated (user decision 6). 41 12th-14th-century
# principalities go landless with claims (their claim lists ARE the
# future: Moscow 1147, Tver 1135, Pskov 1348, Halych 1141), plus ORE
# folded whole into NOV at review — its capital oreshek sits inside
# NOV's sweep and the fold beats a repoint — for 42. Tier 2 (the
# Cuman steppe) waits on the Central Asia Volga line per user decision
# 15. expected = the resolved sweep size (the tag's FINAL holdings
# inside these areas); grants overlapping a recipient's own land are
# no-ops by construction (the KRM/MZN/HLL precedent).
_RUS_RULES = {
    # Kyiv: the right bank, Volhynia (Igor's, reverted 1060), the
    # Cherven towns (Rus since 1031; Halych town is first MENTIONED
    # 1141), Turov-Pinsk (Iziaslav's own patrimony), princeless
    # Smolensk (held in common 1060-73), southern Black Ruthenia.
    # desnyanskyi_horodok sits in kyiv_province (measured) but is PYS's
    # Desna fort from the item-11 probe — minus'd so KIE's sweep does
    # not take it back.
    "KIE": (["right_bank_ukraine_area", "volhynia_area",
             "red_ruthenia_area", "polesia_area", "smolensk_area",
             "mazyr_province", "rechytsa_province",
             "kletsk_province", "slutsk_province"],
            [], [], ["desnyanskyi_horodok"], 191),
    # Chernihiv: Severia, Murom-Ryazan (the testament's grant), the
    # Vyatichi [D], Kursk on the steppe edge.
    "CHR": (["severia_area", "ryazan_area", "oka_area",
             "kursk_province"],
            [], [], [], 127),
    # Pereiaslavl: Vsevolod's split realm — the Dnieper AND Zalesye
    # (Rostov, Suzdal, Beloozero; Moscow is founded 1147). His five
    # original left-bank locations arrived via LOCATION_TRANSFERS at
    # the tag's creation (item 11) and are minus'd here so the
    # transfer and grant lists stay disjoint (the assert demands it).
    "PYS": (["left_bank_ukraine_area", "suzdal_area", "vladimir_area",
             "yaroslavl_area", "beloozero_area", "moscow_area"],
            [],
            [], ["pereiaslav", "desnyanskyi_horodok", "boryspil",
                 "oster", "kozelets"], 131),
    # Novgorod: its own two areas, Torzhok's Tver corner (Tver founded
    # 1135), the Zavolochye tribute land. totma_area ships TWO unowned
    # locations (vyya, malaya_ilesha — found at review; the package's
    # "no location unowned" claim was wrong there) — minus'd or the
    # exactly-once assert dies. korela/konevets are the ORE fold
    # (outside the sweeps).
    "NOV": (["east_novgorod_area", "west_novgorod_area", "tver_area",
             "totma_area"],
            ["korela", "konevets"],
            [], ["vyya", "malaya_ilesha"], 152),
    # Polotsk: Vseslav the Sorcerer's own land, whole.
    "POK": (["white_ruthenia_area"], [], [], [], 56),
}
RUS_LANDLESS = ("BLO", "BRY", "DMI", "DRU", "FMB", "KAS", "KCH", "KLN",
                "KOS", "KZK", "MOG", "MOS", "MRM", "MSV", "NSL", "NVS",
                "ORE", "PNK", "PRK", "PSK", "RSO", "RYA", "RYL", "RZH",
                "SKY", "SMO", "SSK", "STS", "SZL", "TPS", "TRB", "TRS",
                "TUV", "TVE", "UGL", "VBK", "VLR", "VOL", "VYA", "YAR",
                "YRV", "ZUB")
# KIE -> NOV only: Mstislav is his father's placeman. The other two
# triumvirs are partners, not subjects (user decision 12).
RUS_TRIBUTARIES = (("KIE", "NOV"),)

# ============================ RUS TIER 2 (CUM) ==============================
# The Cumans (Rus/steppe package §E.4/§B, user decisions 7+8 approved
# 2026-08-01; implemented after the accumulated test closed items
# 27-30). ONE new tag: CUM, a TRIBE, not a horde — the naming trap is
# escaped exactly as the British slice measured (country_name_
# construction has ZERO tribe branches; the recipient assert bans only
# steppe_horde; landed Gaelic tribes render their names in game).
# ruler = random DELIBERATELY: no 1066 Cuman khan is attested well
# enough to name, and all ten steppe name keys are missing — the
# ARB/GAL/COR honesty. Capital izium [U] — the Donets crossing at the
# traditional site of Sharukan's winter camp; not attested as a TOWN
# in 1066, the package's stated weakness.
# Decision 8: the Danube zone (moldavia+wallachia, 94) goes EMPTY —
# Cuman domination there is an 1080s-90s fact and PEC is banked for
# that ground — but WAL and the seven Moldavian boyar tags are wrong
# under EVERY reading (Wallachia is 1330) and retire landless anyway.
# HAL's Podolian remainder rides to CUM (the package's stated Tier-2
# fate — HAL empties, its morning CAPITAL_FIXES entry goes vestigial);
# GAZ (Genoese Gazaria, founded 1266) empties into CUM's Crimea.
_RUS2_RULES = {
    # CUM-core (169) + CUM-don (42) = 211. minus kursk_province (CHR's
    # Tier-1 outpost) and the four BYZ Cherson-theme coastal singles.
    "CUM": (["yedisan_area", "zaporizhzhia_area", "pryazovia_area",
             "azov_area", "sloboda_ukraine_area", "kursk_area",
             "podolia_area", "crimea_area", "lower_don_area"],
            [],
            ["kursk_province"],
            ["theodoro", "lusta", "soldaia", "vosporo"], 211),
}
RUS2_LANDLESS = ("GAZ", "HAL", "WAL", "IAS", "BIA", "BLD", "SRC",
                 "HTN", "HSC", "SSI")

# eurasian_tribe: type = tribe, tribal_oldest_male, assembly
# parliament, polygyny — a Tengri nomad confederation exactly
# (27 vanilla users). It supplies NO discovery — expl_eastern_europe
# is KIE/PYS's own bundle and covers the capital.
NEW_COUNTRIES["CUM"] = (
    "\tCUM = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_eastern_europe"\n'
    '\t\tinclude = "eurasian_tribe"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = izium\n\t}\n")

# The Danube vacate rides the general mechanism: each owner's holdings
# inside the two areas go to NOBODY (WAL 44, IAS 11, BIA 10, BLD 9,
# SRC 4, HTN 3, HSC 3, SSI 3 — package counts; GLH's 7 extend its
# existing Tier A+B entry, 284 -> 291).
LOCATION_VACATED["GLH"] += ["moldavia_area", "wallachia_area"]
LOCATION_VACATED_EXPECT["GLH"] = 298  # 291 -> 298 with Perm/Vyatka (observed failing first, 2026-08-02): +ufa_province 4 + minusinsk 3
for _t, _n in (("WAL", 44), ("IAS", 11), ("BIA", 10), ("BLD", 9),
               ("SRC", 4), ("HTN", 3), ("HSC", 3), ("SSI", 3)):
    LOCATION_VACATED[_t] = ["moldavia_area", "wallachia_area"]
    LOCATION_VACATED_EXPECT[_t] = _n

# ============================ CHINA-EAST ====================================
# The India/China review's approved package (D2/D3/D5a/D7 + the LNG
# inversion; user-approved 2026-08-01 with two divergences from the
# review's D5b/D6: the DLH behead and the nine Indian retirements WAIT
# for Tier 1 India — vacating the settled Gangetic plain and Deccan
# with no recipients would be an AI-colonization magnet and a
# pop-log flood; the Punjab grant alone evicts Delhi from the
# Ghaznavid half). CHI becomes the SONG by the proven JAP/ASK route
# (flag/country_name are dynasty branding, the state tag stays);
# Mongolia and Manchuria are VACATED (in 1066 that ground is Liao and
# unconsolidated tribes — the Liao slice, deferred, fills empty land
# far more easily than it strips a horde); the eight Chinggisid
# brother/son hordes retire landless with auto-derived claims.
CHINA_LANDLESS = ("LNG", "CRS", "QAS", "BAT", "BGT", "KHD", "HCN",
                  "OTC", "OGE")
# 198 -> 113 with Northern Dynasties: LIA's grants take CHI's 5
# liaodong + 80 Tier-B steppe locations OUT of the vacate pool before
# the vacate resolves (grants run first; the pool intersects
# post-grant holdings). Package-measured, self-asserting.
LOCATION_VACATED["CHI"] = ["mongolia_region", "manchuria_region"]
LOCATION_VACATED_EXPECT["CHI"] = 113
# Tibet slice (2026-08-02): the Changthang — the uninhabited northern
# plateau. 9 of changtang_area's 16 are ALREADY unowned in vanilla;
# vacating TIB's 7 makes it 16/16, the honest picture at 1066 and
# arguably at 1337. The snapshot intersection excludes the
# already-unowned zagya (8 members, 7 held) — the EXPECT pins that.
# Cost: 15 pop-class lines, the cheapest vacate the project has run.
# Runs AFTER _landless_claims, so the seven stay in TIB's claim list —
# Tibet claims the Changthang.
LOCATION_VACATED["TIB"] = ["naktsang_province", "namru_province"]
LOCATION_VACATED_EXPECT["TIB"] = 7
# Perm/Vyatka slice (2026-08-02, decisions 1a and 3): the Vyatka basin
# joins the stateless north around it — the 1174 Novgorodian colony
# does not exist yet, and 14 of VYT's 19 are komi/udmurt shamanism in
# vanilla's own map data. Raw pool is 23; PRM's four (afanasyevo kirs
# koygorodok vizinga) are protected by the snapshot intersection, and
# the EXPECT pins that. Plus GLH's two leftover provinces — ufa (4,
# the bashkiria_area decision one province short: definitions.txt
# files ufa_province under perm_area) and minusinsk (GLH 3 of raw 5,
# the tomsk_area decision's missed corner and the last owned land
# east of the Urals). GLH SURVIVES at 168 — the delta guard cannot
# see a mistake in its two rules; the donor tables in the package
# (reproduced at review) are the guard.
LOCATION_VACATED["VYT"] = ["vyatka_area", "lalsk_province"]
LOCATION_VACATED_EXPECT["VYT"] = 19
LOCATION_VACATED["GLH"] += ["ufa_province", "minusinsk_province"]
# The hordes' REMAINING holdings vacate after LIA's grants (Northern
# Dynasties): CRS 37->24, BAT 18->14 (3 Tier-B + niuquanzi to XIA),
# OTC 23->8, OGE/KHD untouched by LIA. HCN/QAS/BGT lose their WHOLE
# holdings to the grant and reach landless that way — no vacate entry
# (an empty-list vacate would be a no-op; the landless verifier still
# guards them via CHINA_LANDLESS).
for _t, _n in (("CRS", 24), ("BAT", 14),
               ("KHD", 16), ("OTC", 8), ("OGE", 18)):
    # gansu_area: BAT's one Gobi-edge outlier (niuquanzi) — 1066 Gansu
    # is Western Xia ground (deferred slice); empty beats a Chinggisid.
    LOCATION_VACATED[_t] = ["mongolia_region", "manchuria_region",
                            "west_siberia_region", "xinjiang_region",
                            "steppes_region", "ural_region", "gansu_area",
                            "yanbei_area"]
    LOCATION_VACATED_EXPECT[_t] = _n
# LNG's Yunnan appanage inverts: in 1066 Dali is the sovereign and
# Yunnan is not Chinese — CDL takes LNG's 17 (measured list, the
# Sardinia shape) and LNG's 62 tusi ties die with it landless.
_CHINA_GRANTS = {
    "CDL": ["kunming", "lufeng", "yiliang", "kunyang", "anning",
            "chenggong", "yimen", "songming", "fumin", "zhennan",
            "dingyuan_chuxiong", "weichu", "nanan", "heyang",
            "jiangchuan", "lunan", "xinxing"],
}

# ========================= NORTHERN DYNASTIES ===============================
# The Liao and Western Xia (docs/NORTHERN-DYNASTIES-PACKAGE.md,
# user-approved 2026-08-01 with all recommendations: XIA at rank_empire
# per decision 1 — "Great Xia"; LIA Tier A+B; kharchin/jin_language;
# weiming_dynasty; no Liao-Xia or Chanyuan ties — the Chanyuan silver
# is SITUATION material: a subject arrow would invert the treaty's own
# brotherly fiction and collide with CHI's Middle Kingdom leadership).
# yanbei_area is NOT the Sixteen Prefectures (the package corrected
# the brief): those are beiping+datong; yanbei is the Khitan heartland.
# All five Liao capitals exist as locations; linhuang (Shangjing) was
# UNOWNED in the item-32 build and becomes the seat.
_NORTH_RULES = {
    # THE LIAO — the Five Capitals and their circuits (Tier A, 161) +
    # the eastern steppe the Liao garrisoned through them (Tier B,
    # 149; the Zubu "administration" is a claim rendered as ownership,
    # the same fiction every nomad suzerainty on this map wears).
    # Western Mongolia (64: Naimans/Merkits/Kyrgyz) stays EMPTY — the
    # Pecheneg discipline. KOR keeps linjiang_jurchen (its Yalu
    # bridgehead); Ordos/Hetao are Tangut (XIA's).
    "LIA": (["beiping_area", "yanbei_area", "liaodong_area",
             "datong_area", "xiliao_province", "taoer_province",
             "chol_province",
             "argun_area", "eastern_gobi_area", "southern_gobi_area",
             "lower_selenga_area", "upper_selenga_area",
             "shilkari_area"],
            [], ["ordos_province", "hetao_province"],
            ["linjiang_jurchen"], 310),
    # WESTERN XIA — Ordos (tongwancheng, the Tuoba-Tangut ancestral
    # seat), Ningxia (the capital; no xingqing/yinchuan location
    # exists) and the real Hexi Corridor (gansu_area, NOT hexi_area).
    # xining_province is EXCLUDED: Qingtang/Tsongkha, the Song-allied
    # Tibetan kingdom, unconquered until 1099+ [U] — a different
    # slice's wrong.
    "XIA": (["lingzhou_province", "ningxia_province", "yulin_province",
             "suide_province", "ordos_province", "hetao_province",
             "ganzhou_gansu_province", "suzhou_gansu_province",
             "shazhou_province", "yongchang_gansu_province"],
            [], [], [], 48),
}
NORTH_LANDLESS = ("SYG",)  # the Yuan Shenyang Wang is a FUTURE object

NEW_COUNTRIES["LIA"] = (
    "\tLIA = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "far_east_asia_monarchy"\n'
    '\t\tinclude = "expl_mongols"\n'
    "\t\tgovernment = {\n"
    "\t\t\their_selection = cognatic_primogeniture\n"
    "\t\t\treforms = {\n"
    "\t\t\t\tliao_ordo_reform\n"
    "\t\t\t}\n"
    "\t\t}\n"
    # jin_language (chinese_language_family) is the single token that
    # makes the map read "Great Liao" instead of "Khitan Empire" —
    # country_name_construction's empire-dynasty branch needs a
    # Chinese-family court (package §F, verified to the string).
    "\t\tcourt_language = jin_language\n\n"
    "\t\tcountry_rank = rank_empire\n\n"
    "\t\tcapital = linhuang\n\t}\n")

# ============================ INDIA TIER 1 ==================================
# The five great powers of 1066 India (docs/INDIA-TIER1-PACKAGE.md,
# user-approved 2026-08-01, all recommendations incl. the GWA-Tomara
# reuse, the five collateral retirements, PAA's Buddhist identity over
# hindu pops — the al-Andalus law — and the four renames). The Delhi
# behead lands here WITH recipients: zero LOCATION_VACATED anywhere,
# every one of DLH's 272 accounted (the settled-plain pop-flood is why
# item 32 deferred it). Nineteen tags retire landless; DBD SURVIVES as
# Vijayabahu's Ruhuna — the review wanted it retired, but it is
# vanilla's only sinhalese+theravada block AND the Mahavihara sect's
# seat. The package's proposed name-key-language harness check is NOT
# taken: its premise (a key must exist in the culture's language pool)
# is refuted by measurement — scripted names resolve from the loc
# registry (Go-Reizei's name_chikahito rendered in game with zero
# language-pool presence); the literal routes chosen are safe anyway.
_INDIA_RULES = {
    # COZ — Virarajendra's Chola: the mandalams, the Vengi clientage,
    # Chola Lanka (Polonnaruva since 1017). TNK's four Pandya
    # locations are minus'd: the Pandyas survive as feudatories.
    "COZ": (["cola_nadu", "pandya_nadu", "tondai_nadu", "kongu_nadu",
             "baramahal", "jaffna_province", "vanni", "pihiti",
             "kosta", "kamma_nadu", "vengi_nadu"],
            [], [], ["kayal", "tenkasi", "thoothukudi", "tirunelveli"],
            83),
    # CLK — Someshvara I's Western Chalukya: the Deccan whole, Tapti
    # to Tungabhadra; the Kakatiyas/Seunas/Shilaharas ride inside as
    # territory, not ties.
    "CLK": (["kalyana_karnakassala", "raichur_doab", "kampili",
             "chitradurga_province", "banavasi", "bangalore_province",
             "northern_rayalaseema", "southern_rayalaseema",
             "golconda_province", "warangal_province",
             "khammamet_province", "sirpur_province",
             "northern_desh", "southern_desh", "upper_marathwada",
             "lower_marathwada", "malnad", "baglana",
             "north_konkan", "malvana", "lower_vidarbha"],
            ["karwar", "bhadrachalam"], [], [], 180),
    # PAA — Vigrahapala III's Pala: Gauda, Varendra, Vanga, Radha,
    # Magadha, Anga. Kamarupa keeps its three (a real 1066 kingdom).
    "PAA": (["gaur_province", "devkot_province", "bogra_province",
             "jalpaiguri_province", "pandua_province", "nadia_province",
             "khulna_province", "sonargaon_province",
             "mymensingh_province", "khalifatabad_province",
             "bhagalpur_province", "patna_province", "dumka_province",
             "hazaribagh_province"],
            [], [], ["birpara", "kamatapur", "koch_bihar"], 80),
    # PMR — the Paramaras of Malwa; bhojpur is Bhoja's own foundation.
    "PMR": (["western_malwa", "eastern_malwa", "nimar", "khandesh"],
            ["hoshangabad", "bhojpur"], [], [], 38),
    # CHU — the Chaulukyas of Anahilavada (patan IS Anahilavada).
    # Saurashtra stays Chudasama, Kutch stays KUT — defensible 1066.
    "CHU": (["lata", "khekassala", "sarasvata"], [], [], [], 16),
    # ---- the survivors that absorb Delhi ----
    # RTP — Lakshmi-Karna's Kalachuris of Chedi: Dahala, Kashi, the
    # lower doab, Awadh, Rohilkhand. The six arrah locations are
    # protected (UJJ/CER are real hill lineages).
    "RTP": (["akara", "central_doab_province", "lower_doab_province",
             "awadh_area", "rokhilkhand_area", "bhojpur_area"],
            [], [], ["arrah", "ballia", "buxar", "jaund", "rohtas",
                     "sasaram"], 76),
    # GWA reused as the TOMARAS of Dhillika (decision 2): Delhi, the
    # upper doab, Braj, Mewat, and Gwalior itself.
    "GWA": (["delhi_province", "upper_doab_province", "puadh_province",
             "braj_province", "mewat_province", "gird"],
            ["bayana"], [], [], 35),
    # JJK — Kirtivarman's Chandelas restored to Bundelkhand (vanilla's
    # own block comment attests the man AND the ground).
    "JJK": (["upper_bundelkhand_province",
             "lower_bundelkhand_province"], [], [], [], 17),
    # SND — the Soomras take all Sindh (SMA, 1351, empties into them).
    "SND": (["upper_sindh_province", "northern_sindh_province",
             "sibi_province"], [], [], [], 25),
    # The Rajput and Baghelkhand edges of Delhi's demesne.
    "MEW": (["mewar"], [], [], [], 8),
    "HAD": (["hadoti"], [], [], [], 6),
    "MRW": ([], ["mandore", "osian", "kurki"], [], [], 3),
    "DRW": ([], ["sambhar", "ajmer", "ranthambore",
                 "merta", "nagaur", "makrana"], [], [], 6),
    "BGK": ([], ["sidhi", "agori", "vijaygarh"], [], [], 3),
}
INDIA_LANDLESS = ("DLH",
                  "VIJ", "MAB", "SMA", "RDY", "RCH", "JFN", "SMV", "MSN",
                  "YDR",
                  "GAU", "SGN", "STN",
                  "BND", "IDR", "RJI", "BGL", "DRP", "JWR")

# The five imperial blocks ride vanilla's own India templates —
# diff-measured: the Hindu _no_coast variant KEEPS heir_selection
# (unlike the Muslim family), so nothing is restated. CHU rides the
# _jain variant, which includes expl_india_hindu itself. tolerated
# lists are the measured minority profile of each resolved territory.
NEW_COUNTRIES["COZ"] = (
    "\tCOZ = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_india_hindu"\n'
    '\t\tinclude = "indian_hindu_monarchy"\n'
    "\t\ttolerated_cultures = {\n"
    "\t\t\tsinhalese\n\t\t\ttelugu\n\t\t\tkannadiga\n"
    "\t\t}\n\n"
    "\t\tcountry_rank = rank_kingdom\n\n"
    "\t\tcapital = thanjavur\n\t}\n")
NEW_COUNTRIES["CLK"] = (
    "\tCLK = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_india_hindu"\n'
    '\t\tinclude = "indian_hindu_monarchy"\n'
    "\t\ttolerated_cultures = {\n"
    "\t\t\tmarathi_culture\n\t\t\ttelugu\n\t\t\tkonkani\n\t\t\tgond\n"
    "\t\t}\n\n"
    "\t\tcountry_rank = rank_kingdom\n\n"
    "\t\tcapital = kalyani\n\t}\n")
NEW_COUNTRIES["PAA"] = (
    "\tPAA = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_india_hindu"\n'
    '\t\tinclude = "indian_hindu_monarchy"\n'
    "\t\ttolerated_cultures = {\n"
    "\t\t\tbhojpuri_culture\n\t\t\tmagahi\n\t\t\tmaithili_culture\n"
    "\t\t}\n\n"
    "\t\tcountry_rank = rank_kingdom\n\n"
    "\t\tcapital = monghyr\n\t}\n")
NEW_COUNTRIES["PMR"] = (
    "\tPMR = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_india_hindu"\n'
    '\t\tinclude = "indian_hindu_monarchy_no_coast"\n'
    "\t\ttolerated_cultures = {\n"
    "\t\t\tkhandeshi\n\t\t\tbhil\n\t\t\tbundeli\n"
    "\t\t}\n\n"
    "\t\tcountry_rank = rank_kingdom\n\n"
    "\t\tcapital = dhar\n\t}\n")
NEW_COUNTRIES["CHU"] = (
    "\tCHU = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "indian_hindu_monarchy_jain"\n'
    "\t\ttolerated_cultures = {\n"
    "\t\t\tbhil\n\t\t\tmewari\n"
    "\t\t}\n\n"
    "\t\tcountry_rank = rank_kingdom\n\n"
    "\t\tcapital = patan\n\t}\n")

NEW_COUNTRIES["XIA"] = (
    "\tXIA = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "east_asia_monarchy_no_coast"\n'
    '\t\tinclude = "expl_china"\n'
    "\t\tgovernment = {\n"
    # the no_coast diff was run: only maritime/piracy laws drop, the
    # heir line survives — restated anyway, the house rule.
    "\t\t\their_selection = cognatic_primogeniture\n"
    "\t\t}\n"
    "\t\tcourt_language = northern_mandarin_dialect\n\n"
    "\t\tcountry_rank = rank_empire\n\n"
    "\t\tcapital = ningxia\n\t}\n")

# ================================ BALTIC ====================================
# The Baltic package (docs/BALTIC-PACKAGE.md, user-approved 2026-08-01,
# all 12 recommendations incl. option 2 for Lithuania). The crusader
# state — TEU, LIV and their nine bishopric/city satellites, none
# founded before 1190 — retires landless with auto-derived claims (the
# thirteenth century as a claim list), and the pagan peoples the
# crusade was preached against take the ground: PRS, SUD, KUO, ZEM,
# LTG, ESO new; SXM revived onto its own vanilla claim list; AUK new
# in Lithuania's place (option 2: rank_kingdom_grand_duchy_LIT at
# country_ranks.txt:1355 is tag-gated ABOVE the tribe branches, so a
# tribal LIT at rank_duchy still renders "Grand Duchy of Lithuania" —
# retiring the tag bypasses the branch structurally). NO rulers, NO
# dynasties, NO characters: the first named Lithuanian dukes are the
# 1219 treaty's, the Prussians produce no name before Herkus Monte
# (1260s), Estonia had no king at all — the Pecheneg discipline
# applied to people.

# tag -> locations listed in that tag's `control = { ... }` block ONLY
# (owned by somebody else). Vanilla ships exactly TEN such locations
# game-wide: TEU controls six Samogitian locations LIT owns (own_core),
# and MOR controls four Tlemcen locations TLE owns — the Maghreb slice
# will need a second key here the day it retires or regrants either.
# `control` is the last member of OWN_KEYS, so all three of
# _remove_owned_many, the LANDLESS_AFTER guard and the orphan-capital
# guard read these as holdings. Any slice that grants, vacates or
# retires one of the two occupiers must clear the occupation first.
# The consuming loop runs BEFORE the _landless_claims snapshot so the
# retiring tag's claims are its REAL holdings, not its conquests — a
# 1066 Teutonic claim on Samogitia is exactly the wrong line to write.
CONTROL_STRIPS = {
    "TEU": ["palanga", "rietavas", "silale", "skuodas", "taurage",
            "mazeikiai"],
}

# The definitions-resolved grants, the _SELJUK_RULES 5-tuple shape:
# tag -> (sweeps, singles, minus-sweeps, minus-singles, expected).
# All 176 resolved locations are owned in vanilla — nothing is
# vacated, so the pop-line class (ERROR-DECODER, ~504 lines) neither
# grows nor shrinks: prefer real recipients on settled ground.
_BALTIC_RULES = {
    # THE PRUSSIANS. The five eastern provinces are the Prussian lands
    # proper — Sambia, Natangia, Warmia, Pogesania, Pomesania, Barta,
    # Galindia, Nadruvia, Skalvia. elk and barten are sudovian-culture
    # and go to SUD. Donors TEU 21 / ERM 3 / SMD 1 / PMS 1. The seat
    # is fischhausen (Sambia, the most populous land; Wiskiauten was
    # the Viking-age emporium on this ground) — konigsberg is a 1255
    # Order foundation and malbork a 1274 one, both refused.
    "PRS": (["lower_prussia_province", "upper_prussia_province",
             "warmia_province", "masuria_province",
             "lithuania_minor_province"], [], [], ["elk", "barten"], 26),
    # SUDOVIA / YOTVINGIA. Every sudovian-culture location forming a
    # contiguous block: the Suwalki lakes, the two Masurian outliers,
    # the upper Nemunas crossings, and (option 2) the Grodno pocket
    # from LIT — grodno is a Rurikid town by 1116 but sudovian-culture
    # ground in 1066 (package decision 4, RAW/SUD/NRK split).
    "SUD": (["suwalki_province"],
            ["elk", "barten", "lazdijai", "alytus", "vilkaviskis",
             "grodno", "sokolka", "grodek", "bershty"], [], [], 12),
    # THE CURONIANS — the whole Courland peninsula, Seeburg to
    # Domesnes. Donors LIV 6 / KUR 2.
    "KUO": (["courland_province"], [], [], [], 8),
    # SEMIGALLIA AND SELONIA — the Lielupe and the middle Daugava.
    # dobele is a Semigallian hillfort; jelgava (Mitau, 1265) refused.
    "ZEM": (["semigalia_province", "selonia_province"], [], [], [], 7),
    # THE LATGALIANS AND THE DAUGAVA LIVS — Latgale, Tolowa, and the
    # Livonian river mouth. koknese is Kukenois, one of the two
    # Latgalian principalities Henry of Livonia names; riga (1201)
    # refused. Donors ARR 8 / LIV 8 / RIG 1.
    "LTG": (["latgalia_province", "inner_livonia_province",
             "south_livonia_province"], [], [], [], 17),
    # ESTONIA — Sakala, Ugaunia, Revala/Harjumaa/Virumaa, Laanemaa,
    # Saaremaa. Includes DAN's seven estonia_province locations:
    # Danish Estonia begins at Lyndanisse in 1219, not 1066 (package
    # decision 11). tartu = Tarbatu, Yaroslav's Yuryev since 1030 —
    # the one Estonian place with a documented 11th-century identity.
    "ESO": (["north_livonia_province", "tartu_province",
             "estonia_province", "rotalia_province"], [], [], [], 24),
    # SAMOGITIA — vanilla's own SXM revived onto its own claim list
    # (its our_cores_conquered_by_others IS the sixteen). Requires the
    # CONTROL_STRIPS step above or the six own_core/control doubles
    # die in _remove_owned_many.
    "SXM": (["samogitia_area"], [], [], [], 16),
    # AUKSTAITIJA — the Lithuanian highlands in LIT's place (option
    # 2). kernave: continuously occupied through the 1st millennium,
    # five hillforts, the Grand Duchy's first seat — vilnius is first
    # documented 1323. The minus lists are SUD's share of the area.
    "AUK": (["lithuania_area"], [], ["suwalki_province"],
            ["lazdijai", "alytus", "vilkaviskis"], 37),
    # POLAND — Pomerelia (Gdansk, Tuchola), Culmerland and the Dobrzyn
    # land: Piast ground in 1066, Order ground only from 1228/1308.
    # Donors TEU 19 / CHL 2.
    "POL": (["danzig_province", "tuchola_province", "chelmno_province",
             "dobrzyn_province"], ["bytow", "lebork"], [], [], 21),
    # MAZOVIA — the Podlasie strip, Mazovian marchland raided by the
    # Yotvingians; RAW holds 14 in the same area (package decision 4).
    "RAW": ([], ["drohiczyn", "bielsk_podlaski", "mielnik", "sokolow",
                 "suraz"], [], [], 5),
    # NOVOGRUDOK — the two Polesian-culture, orthodox locations of
    # LIT's Black Ruthenia pocket: Kievan/Turov ground, and NRK is
    # the Rus package's chosen holder of the area (decision 4).
    "NRK": ([], ["masty", "nyasvizh"], [], [], 2),
    # HOHENLOHE — mergentheim, the Order's post-1525 seat, back to the
    # local Franconian lord: UFF (dynasty = hohenlohe_dynasty) holds
    # crailsheim and ohringen in the same tauberfranken_province, and
    # Mergentheim was a Hohenlohe possession before the 1219 donation
    # (package decision 5; the family itself is c. 1153 — the Germany
    # slice's anachronism, flagged not fixed).
    "UFF": ([], ["mergentheim"], [], [], 1),
}

# The crusader state retires whole: the Order tags (1190/1202), the
# five Prussian bishoprics (1243), Riga city (1201) and the Livonian
# sees (1186-1234) — none exists in 1066. Landless with auto-derived
# claims, never deleted: seven DHE flavor files, two country-advance
# files, the hussite situation and an on_action all hang off TEU/LIV
# by existence- or tag-gates and degrade to no-ops. LIT rides with
# them (option 2): the Grand Duchy IS the future object here — the
# claims are Mindaugas's state, exactly as TEU's are the Ordensstaat.
BALTIC_LANDLESS = ("TEU", "LIV", "ARR", "KUR", "RIG", "BID", "BIO",
                   "ERM", "SMD", "PMS", "CHL", "LIT")

# The Baltic tribes ride CUM's shape exactly (the attested 1066
# tribal block): eurasian_tribe supplies type = tribe,
# tribal_oldest_male, assembly parliament; expl_eastern_europe
# carries baltic_region, which holds all seven capitals. tech 2 is
# the Irish tribal precedent (gaelic_tribe ships 2; CUM's 3 is the
# steppe's) — package decision 8, a slider not a correctness claim.
# rank_duchy is declared, not derived, so the F-section render is
# deterministic: map label = NAME key verbatim (the tribal fallback's
# map string is bare $NAME$), long form "Tribe of ...", ruler Chief.
for _t, _cap in (("PRS", "fischhausen"), ("SUD", "suwalki"),
                 ("KUO", "grobina"), ("ZEM", "dobele"),
                 ("LTG", "koknese"), ("ESO", "tartu"),
                 ("AUK", "kernave")):
    NEW_COUNTRIES[_t] = (
        "\t" + _t + " = {\n"
        "\t\tstarting_technology_level = 2\n"
        '\t\tinclude = "expl_eastern_europe"\n'
        '\t\tinclude = "eurasian_tribe"\n'
        "\t\tcountry_rank = rank_duchy\n\n"
        "\t\tcapital = " + _cap + "\n\t}\n")

# ================================ AFRICA ====================================
# The sub-Saharan Africa package (docs/AFRICA-PACKAGE.md, user-approved
# 2026-08-02, all decisions; review corrections applied at
# implementation: KBR cannot be both repointed to GHA and landless —
# its MAL line dies in the landless sweep instead, so the repoint batch
# is FOUR tags; ETH's ankober IS orphaned by SOA's argobba sweep, so
# ETH joins CAPITAL_FIXES; rank_county_muslim does NOT exist — measured,
# zero hits in country_ranks.txt and government_names — so ZAN drops to
# rank_duchy "Emirate of Kilwa", never county).
# THE HEADLINE (package §0.1): vanilla's thirteen MAL vassals are ten
# of al-Bakri's own 1068 polities hung off a Mali that is 170 years
# away — the Sahel correction is mostly DIPLOMACY (a repoint and four
# strip batches), not territory. Two whole-file registry overrides ride
# with it (MAK miaphysite, the Hausa seven bori_religion), landed in
# their own commit and break-tested against the bijection check.

# Same 5-tuple shape as _BALTIC_RULES. All counts resolved from
# definitions.txt by the package and re-asserted here; nothing is
# vacated — the nine unowned Adrar/Arguin locations SNH absorbs
# SHRINK the pop-line class rather than growing it.
_AFRICA_RULES = {
    # THE SENEGAL. Takrur under Labi takes the lower river and (decision
    # 2) the Gambia: JOL is Ndiadiane Ndiaye's c. 1350, KAB a Mali
    # province of c. 1235 — the one power the eleventh-century sources
    # name on these rivers is Takrur. kodiam/kerbatch are BBK's two
    # gambia_area holdings (resolved 2026-08-02) and stay BBK's.
    "TKR": (["jolof_area", "gambia_area"], [],
            [], ["kodiam", "kerbatch"], 38),
    # THE INLAND DELTA. BMR (Segou, c. 1712) dissolves. Djenne-Jeno
    # takes the Djenne bend; Zagha (Dia) takes Masina and the
    # escarpment.
    "DJN": (["djenne_province", "safare_province"], [], [], [], 11),
    "ZGH": (["macina_province", "hayre_province"], [], [], [], 12),
    # THE NIGER BEND. Timbuktu is founded c. 1100; TMB stays landless
    # on its vanilla claim list (a free correctness win).
    "SON": (["timbuktu_province"], [], [], [], 5),
    # THE SANHAJA OF THE VEIL (decision 3, with the salt): the western
    # Sahara at the moment the Almoravids own it — Awdaghust sacked
    # 1054/55 [U]. Nine of the seventeen are already unowned.
    "SNH": (["tagant_province", "arguin_province", "adrar_province",
             "taghaza_province"], [], [], [], 17),
    # WAGADU. Ghana proper plus Kaarta, Khaaso and Sosso. diara is
    # carved out (package §E.4): Zafun IS Diara — DFN keeps its seat
    # and needs no CAPITAL_FIXES. banamba too (caught by the
    # _list_owner disjointness assert at implementation — the package's
    # "zero overlaps" missed it): it sits in the swept ground AND in
    # MAL's singles, and the package's own donor table gives it to MAL.
    "GHA": (["ghana_province", "kaarta_province", "khaaso_province",
             "sosso_province"], [], [], ["diara", "banamba"], 21),
    # BAMBARA's remaining Niger reach folds into Manden (Kangaba).
    "MAL": (["bambara_province"], ["koutiala", "banamba"], [], [], 8),
    # ETHIOPIA sheds Shewa and Simien (decision 9: land both shells).
    "SOA": (["argobba_province", "shewa_province", "wej_province"],
            [], [], [], 12),
    "BTI": (["semien_province"], ["gonder", "shire"], [], [], 5),
    # THE HORN. IFA (1285) dissolves; AJU survives SHRUNK inland
    # (decision 5b — MDI takes the Benadir coast, no WAR stretch).
    "ADA": (["adal_province"],
            ["siyara", "zeila", "amud", "el_sheikh", "hargeisa",
             "ali_sabieh"], [], [], 12),
    # WAR takes the Haud too — IFA's residue, resolved at
    # implementation (the package left it inside OPEN DECISION 5 and
    # the landless guard caught the gap): the Haud is the northern
    # pastoral clans' grazing commons [U], the same clan-polity model
    # vanilla itself uses for WAR's own ground.
    # kelafo/el_dhere are AJU's two haud_province holdings — Shebelle
    # towns, they stay with the surviving inland Ajuran (5b).
    "WAR": (["maakhir_province", "ciid_province", "majerteen_province",
             "guban_province", "haud_province"], [], [],
            ["siyara", "zeila", "kelafo", "el_dhere"], 29),
    "MDI": (["banaadir_province", "ajan_province"], [], [], [], 10),
    # The rest of IFA's residue, same catch: the Mora/Aussa three are
    # Afar anayurt and go to the kept AFA; the Mudug three go to the
    # surviving inland AJU (decision 5b), whose sphere Mudug is.
    "AFA": ([], ["asaita", "killelu", "mora_eth"], [], [], 3),
    "AJU": ([], ["awrtable", "el_hamurre", "galkayo"], [], [], 3),
    # NUBIA. Al-Abwab (a 1270s breakaway) folds back into the two
    # Christian kingdoms.
    "MAK": ([], ["el_metemma"], [], [], 1),
    "ALO": ([], ["ed_damer", "shendi"], [], [], 2),
}

# Static grants, the _ARABIA_GRANTS shape. Decision 7: OYO (c. 1300,
# the one clearly-late Guinea-forest tag) retires; Ife — the Yoruba
# ritual capital, whose priority over Oyo is the tradition's own claim
# [U] — takes its eleven. List copied from OYO's own_control_core.
_AFRICA_GRANTS = {
    "IFE": ["oyo_ile", "kisi", "igboho", "ikoyi", "ogbomosho", "ede",
            "tede", "saki", "irawo", "agbonle", "ilorin"],
}

# Locations that are UNOWNED in vanilla and receive an owner from a
# grant (the SNH Adrar/Arguin fill — the machinery's first such case:
# _remove_owned_many demands exactly ONE ownership entry and these
# have ZERO, measured when the first Africa dry-run died on all nine).
# Each is asserted to (a) still be ownerless in the source — a vanilla
# patch that lands an owner fails loudly, the CONTROL_STRIPS
# discipline — and (b) sit in its tag's resolved grant list; removal
# is skipped for them and the ownership write includes them. This is
# the one place the build SHRINKS the vacated-pop error class instead
# of growing it.
UNOWNED_GRANTS = {
    "SNH": ["arguin", "nouamghar", "nouakchott", "akjoujt", "atar",
            "azougui", "chingetti", "wadan", "idjil"],
}

# BMR Segou c. 1712, JOL c. 1350, KAB c. 1235, IFA (Walashma) c. 1285,
# ABW a 1270s Makurian breakaway, OYO c. 1300 — and four SIDE-EFFECT
# retirements the grants empty (SGH to SNH's Arguin sweep, KBR to
# ZGH's macina, HRL to ADA's harar, TDE to WAR's majerteen), listed
# because the emptied-but-unlisted delta guard demands it — this slice
# is that guard's first real workout. AJU is NOT here (decision 5b:
# it survives inland at 20). Claims are the snapshot's, i.e. each
# tag's FULL vanilla holdings — the Walashma's Ifat and Segou's Niger
# as future objects.
AFRICA_LANDLESS = ("BMR", "JOL", "KAB", "IFA", "ABW", "SGH", "KBR",
                   "HRL", "TDE", "OYO")

# DJN — Djenne-Jeno, the Middle Niger's oldest city, occupied from
# c. 250 BC [U]; a Muslim monarchy in the local template idiom (the
# no_coast parent declares type and heir_selection — read in full).
# SNH — the Sanhaja of the veil, Lamtuna and Gudala, the Almoravid
# heartland; a Muslim TRIBE (subsaharan_muslim_tribe -> subsaharan_
# tribe, type = tribe), renders "Tribe of the Sanhaja" via the
# tribe-beats-muslim first-match order (country_ranks.txt:1606 before
# :1743, measured). Tech 3 = the measured Sahel convention (every
# landed Sahel tag ships 3).
NEW_COUNTRIES["DJN"] = (
    "\tDJN = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_west_africa_muslim"\n'
    '\t\tinclude = "subsaharan_muslim_monarchy_no_coast"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = djenne\n\t}\n")
NEW_COUNTRIES["SNH"] = (
    "\tSNH = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_west_africa_muslim"\n'
    '\t\tinclude = "subsaharan_muslim_tribe"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = aoudaghost\n\t}\n")

# ============================ SOUTHEAST ASIA ================================
# THE SEA SLICE (docs/SEA-PACKAGE.md, key claims re-verified 2026-08-02,
# user-approved same day, decisions 1-13). Anawrahta's Pagan unifies the
# Irrawaddy, Java splits into Airlangga's 1049 halves, the Srivijayan
# mandala repoints off a Majapahit founded 227 years late. REVIEW
# CORRECTION baked in throughout: the package's country reader missed
# `own_control_integrated` blocks, so its "10 vanilla-unowned Khorat/
# Mekong locations" (and VTN 25 / PLB 34 / BTU 1...) were phantoms —
# every location granted below carries exactly ONE ownership entry,
# measured with THIS file's own reader, and UNOWNED_GRANTS gains
# nothing. Same 5-tuple shape as _BALTIC_RULES/_AFRICA_RULES.
_SEA_RULES = {
    # PAGAN. Anawrahta's kingdom: the whole Irrawaddy valley and the
    # Mon delta he took with Thaton in 1057 [D], Tenasserim included
    # (decision 12 — the chronicle tradition's reach to Mergui). The
    # four singles are the Shan-hill outliers PIN and SAG hold outside
    # the two areas, granted so both empty cleanly. `kale` is carved
    # out: KAL is a one-location tai_nua hill muang and retiring it
    # buys nothing — without the carve-out PGN resolves 75 and KAL
    # dies emptied-but-unlisted (the delta guard's third workout).
    "PGN": (["irrawady_area", "irrawady_delta_area"],
            ["wetwin", "myedu", "ngasingu", "takawng"],
            [], ["kale"], 74),
    # LAVO. The Chao Phraya basin minus the two western Mon survivors
    # (decision 8: SPN and PTC stay alive — LAV conquering Suphanburi
    # is exactly what vanilla's own flavor_ayu.1 third trigger branch
    # expects for the 1337 Ayutthaya formation). Sukhothai is 1238,
    # Ayodhya 1351; Lavo is the basin's continuous polity. Self-grant
    # of LAV's own nine rides the GHA/koumbi_saleh precedent.
    "LAV": (["ayutthaya_province", "phraek_province", "sri_thep_province",
             "sukhothai_province", "tak_province", "rayong_province"],
            [], [], [], 28),
    # HARIPUNJAYA. The Ping valley — Lamphun, Chiang Mai, the Karen
    # west. Mangrai takes it only in 1292; at 1066 it is the Mon
    # kingdom's (decision 4: Mon identity over 1337-painted Khon Muang
    # pops, the PAA law — POP-PHASE inherits the correction).
    "HPJ": (["chiang_mai_province", "muang_yuam_province"], [], [], [], 12),
    # NGOENYANG'S GROUND (decision 5): chiang_rai_province is Chiang
    # Saen and Phayao — vanilla's own singhanavati_dynasty sits at
    # chiang_saen. Grown PHY stands in; its 1094 foundation [U] is 28
    # years early and this comment is where that honesty lives.
    "PHY": (["chiang_rai_province"], [], [], [], 5),
    # NAN. muang_ngao is PHY's and stays PHY's.
    "PUA": (["phrae_province"], [], [], ["muang_ngao"], 4),
    # LNA's eastern residue.
    "KTG": (["kengtung_province"], [], [], [], 6),
    "CHH": (["muang_sing_province"], [], [], [], 6),
    # THE KHORAT PLATEAU. Lan Xang is 1353; the plateau at 1066 is
    # Khmer (Phimai, Phanom Rung) and Kuy/Bru tribal — the ONE touch on
    # the item-32 seam, territory only, no rank/ruler/capital change.
    # thakhek_proivnce is vanilla's own definitions.txt typo — verbatim.
    "KHM": (["roi_et_province", "chaiyaphum_province",
             "muang_nakhon_province", "thakhek_proivnce"], [], [], [], 24),
    # THE UPPER MEKONG. Vientiane, Loei, Muang Phuan to Muang Sua —
    # pre-Lan-Xang and plausibly 11th-c. [D].
    "MUA": (["loei_province", "vientiane_province",
             "muang_phuan_province"], [], [], [], 14),
    # JAVA, SPLIT IN 1049. Panjalu/Kediri west of the Brantas (its
    # seat daha sits in pajang_province), Janggala east. There is no
    # kediri, kahuripan, panjalu or janggala location (probed) —
    # daha IS Kediri's capital name [D], surabaya stands in for
    # Kahuripan [U].
    "KDR": (["pajang_province", "mataram_province", "demak_province"],
            [], [], [], 18),
    "JGL": (["surabaya_province", "trowulan_province"], [], [], [], 14),
    # NORTH SUMATRA. Aru is 13th-century [D]; Pannai is the polity the
    # 1030 Tanjore inscription names on this coast [D].
    "PNI": (["deli_province", "riau_rokan_province",
             "riau_siak_province"], [], [], [], 19),
    "INR": (["riau_kampar_province"], [], [], [], 6),
    # MUSLIM SUMATRA (decision 7): Pasai is c. 1267, Aceh Darussalam
    # 1496 [both U]; LGE — the Gayo highland tag, already adjacent,
    # already holding linge/gayo_lues — takes the coast. Self-grant of
    # its own two rides the same precedent; singkil is BUS's and
    # carved out.
    "LGE": (["northern_aceh_province", "southern_aceh_province"],
            [], [], ["singkil"], 13),
    # THE PHILIPPINES (decision 9): Maynila as a state is 16th-c. [U] —
    # maynila crosses the river to Tondo (the Laguna Copperplate's
    # polity, 900 [D]); Wenduling/Maguindanao is c. 1520 [U] — its five
    # go to neighbouring KIM. SUL stays: Lupah Sug is older than its
    # 1405 sultanate [D]. REVIEW CORRECTION: MGD holds FIVE locations,
    # not the package's one — the integrated-block blindness again.
    "TDO": ([], ["maynila"], [], [], 1),
    "KIM": ([], ["kabacan", "kalalaw", "kalamansig", "kuta_watu",
                 "minduso"], [], [], 5),
}

# Sixteen retirements, every one a deliberate post-1066 state whose
# whole holding is granted away by name — zero side effects, the delta
# guard stays silent throughout (if it fires, the design is wrong).
# Claims are the snapshot's, i.e. each tag's FULL holdings — Pinya's
# Upper Burma, Hanthawaddy's delta, Sukhothai's Yom, Lan Na's Ping,
# Lan Xang's Mekong, Majapahit's Java and Aru's Deli coast as future
# objects. VTN's claims are its measured 32 (not the package's 25).
SEA_LANDLESS = ("PIN", "SAG", "PEG", "TSM", "BPR", "TNG",
                "SUK", "ADH", "LNA", "VTN",
                "MAJ", "ARU", "ATJ", "PSA", "MNA", "MGD")

# The Srivijayan mandala (decisions 1, 2, 13): Palembang over the
# Malay ports as war-capable TRIBUTARIES — the loose bond the Chinese
# sources describe (San-fo-qi as a confederation of ports [D]), and
# vanilla's own Mūlasarvāstivāda sect lists exactly this world as one
# Buddhist web (15_IO:1014). NO reform: every party's template reforms
# block carries vanilla's mandala_system (allow_tributary_subject =
# yes, country_specific.txt:3894-3915) — the first tributary ring in
# the project gated by a VANILLA reform. PLB rather than JMB (decision
# 2): the larger tag, Srivijaya's own capital, and rank_kingdom +
# malay_culture renders "Mahārājya of Palembang"/"Mahārājā"
# (country_ranks.txt:1072 — LAUNCH PROBE: the dialect->language
# resolution is a scope-link inference, OWED CHECK 1).
SRIVIJAYA_TRIBUTARIES = (("PLB", "JMB"), ("PLB", "INR"), ("PLB", "SGT"),
                         ("PLB", "BUS"), ("PLB", "PNI"))

# PGN rides the COASTAL parent (decision 12 — it takes the whole
# Irrawaddy delta: dagon, pathein, martaban). Both SEA parents declare
# type + heir_selection and carry reforms = { mandala_system } (read
# in full); KDR/JGL ride indonesia_monarchy like every landed Javanese
# tag — expl_china (line 2 of every SEA template) already discovers
# both theater regions, the expl_indonesia* pair is the local
# convention. Tech 3 = the measured convention across all four
# templates. Ranks (decision 3): PGN kingdom — Anawrahta's own title;
# empire would print "Pagan Empire" via the adjective branch. HPJ/JGL
# duchy renders plain "Duchy"/"Duke" — no Mon or Javanese rank branch
# exists anywhere in country_ranks.txt (measured).
NEW_COUNTRIES["PGN"] = (
    "\tPGN = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "south_east_asia_monarchy"\n'
    "\t\tcountry_rank = rank_kingdom\n\n"
    "\t\tcapital = pagan\n\t}\n")
NEW_COUNTRIES["HPJ"] = (
    "\tHPJ = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "south_east_asia_monarchy_no_coast"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = lamphun\n\t}\n")
NEW_COUNTRIES["KDR"] = (
    "\tKDR = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_indonesian_trade_route"\n'
    '\t\tinclude = "expl_indonesia"\n'
    '\t\tinclude = "indonesia_monarchy"\n'
    "\t\tcountry_rank = rank_kingdom\n\n"
    "\t\tcapital = daha\n\t}\n")
NEW_COUNTRIES["JGL"] = (
    "\tJGL = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_indonesian_trade_route"\n'
    '\t\tinclude = "expl_indonesia"\n'
    '\t\tinclude = "indonesia_monarchy"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = surabaya\n\t}\n")

# ================================= TIBET ====================================
# THE TIBET SLICE (docs/TIBET-PACKAGE.md, every mechanical claim
# re-verified 2026-08-02 — the FIRST package to survive review with
# zero implementation-level errors; decisions taken by the main
# session under the user's direct-implement authorization, recorded
# in the STATUS band and HANDOFF item 38). Vanilla already ships the
# Era of Fragmentation — Guge, Purang, Maryul, Zanskar, Mangyül
# Gungthang and the Kham patchwork by name — and then hangs all of it
# off TIB, a Sakya theocracy whose own school vanilla DATES to 1073
# (15_IO creation_date; our future-date strip already deleted the
# Sakya and Jonang sects months ago). Retiring TIB dissolves the
# whole 15-line web through the generic landless sweep: zero named
# strips, zero repoints. Ü and Tsang land as region-tags in vanilla's
# own AMD/GOL/HOR grammar (decision 1); Tsongkha rises on the six
# xining_province locations NORTHERN-DYNASTIES-PACKAGE.md:1035 banked
# for exactly this pass (decision 3 — the one CHI touch, signed off).
_TIBET_RULES = {
    # Ü (dBus). u_area minus POO's pemako_province — the four TIB
    # provinces are named instead of sweeping the area, so POO's three
    # stay POO's without a carve-out (sweeping u_area would be the KAL
    # class). Lhasa, Yarlung, Marpa's Lhodrak, Kongpo.
    "DBU": (["kongpo_province", "lhokha_province", "u_province",
             "yarlung_province"], [], [], [], 25),
    # TSANG (gTsang). The whole area plus phari, the Chumbi valley
    # head vanilla parks in bengal_region/monyul_area — an explicit
    # single BECAUSE no tibet_region sweep reaches it; dropping it
    # leaves TIB landed and the landless guard fires. NOTE sakya the
    # LOCATION is Tsang's at any date; the monastery on it is 1073.
    "GTS": (["tsang_area"], ["phari"], [], [], 19),
    # GUGE. TIB's Ngari residue: lungkha_province whole plus the two
    # rutok outliers adjacent to GUG's own gartok/rala.
    "GUG": (["lungkha_province"], ["tsherlung", "ormogang"], [], [], 5),
    # NUBHOR. nakchukha_province is khampa_culture beside NBH's Biru.
    "NBH": (["nakchukha_province"], [], [], [], 3),
    # TSONGKHA. xining_province IS Qingtang, Gusiluo's seat, under its
    # Chinese name (no qingtang/tsongkha location exists — probed).
    # Song-painted liang/monguor pops under a Tibetan identity: the
    # al-Andalus/PAA/HPJ law, banked for POP-PHASE.
    "TKA": (["xining_province"], [], [], [], 6),
}

# ONE retirement, deliberate: TIB is the MAJ class (a post-1066
# object — Sakya capital, theocracy, Yuan-era web, and a live
# "Grand Theocracy of Tibet"/"Grand Priest" render), not the NOV
# class (a real 1066 polity with a dated constitution). Claims go
# 131 -> 190 (its own 59 join; overlap measured ZERO), i.e. the whole
# plateau — and vanilla's own TIB_f formable (0.6 of tibet_region,
# tibetan_group culture) becomes the reunification path, the Pecheneg
# philosophy with the machinery already shipped.
TIBET_LANDLESS = ("TIB",)

NEW_COUNTRIES["DBU"] = (
    "\tDBU = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "east_asia_monarchy_no_coast"\n\n'
    "\t\tcapital = lhasa\n\t}\n")
NEW_COUNTRIES["GTS"] = (
    "\tGTS = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "east_asia_monarchy_no_coast"\n\n'
    "\t\tcapital = shigatse\n\t}\n")
NEW_COUNTRIES["TKA"] = (
    "\tTKA = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "east_asia_monarchy_no_coast"\n\n'
    "\t\tcapital = xining\n\t}\n")
# NO country_rank on any of the three — deliberate: 21 of the
# theater's 22 landed tags declare none (TIB, retired, was the one),
# and the template (read in full: monarchy, cognatic_primogeniture,
# council parliament, tech 3, NO reforms block) declares none either.
# The engine derives ranks by rules no file settles — OWED CHECK,
# inherited from SEA; the click tour reads the result either way.

# =============================== THE AMERICAS ===============================
# THE WESTERN HEMISPHERE (docs/AMERICAS-PACKAGE.md, every claim
# re-verified 2026-08-02 — the THIRD consecutive zero-error package;
# decisions 1-6 user-approved, decision 4 the review's own divergence).
# The largest "already right" theater by an order of magnitude: the
# mod had never touched a single American tag, 88.9% of 4,441
# locations are unowned by design, 321 of the game's 448 type=pop
# identities are American, and the creation-date law already deleted
# the Haudenosaunee League (vanilla dates it 1142.1.1) months ago.
# Cahokia stays whole — 1066 is its PEAK and vanilla's own "Sunset of
# Cahokia" DHE lands the 1337+ terminus on the archaeology. Two
# retirements: TNC (Tenochtitlan is founded 1325 [D]; the island goes
# to TEP, its own overlord in the same province, so the rank=city
# keeps an owner and AZT_f — gated on owns=tenochtitlan, not the
# tag — stays open to be EARNED) and CSU (decision 4, the review
# overruling the package's low-confidence leave: vanilla's own
# csu_manco_qhapaq is born 1170 — the TIB/Sakya-1073 evidence class —
# and vanilla itself ships KKE "Killke", the archaeological name for
# pre-Inca Cusco; INC_f stays reachable through KKE's own Quechua).
# No Toltec tag (decision 1: toltec_culture sits on ZERO locations —
# the tag would be a Nahua state wearing an ungrounded name; extent
# unknowable [D]; tollan stays TEP's).
_AMERICAS_RULES = {
    "TEP": ([], ["tenochtitlan"], [], [], 1),
    "KKE": ([], ["qusqu", "quillarumiyoc"], [], [], 2),
}

AMERICAS_LANDLESS = ("TNC", "CSU")

# ============================= PERM / VYATKA ================================
# THE FINNO-UGRIC NORTH (docs/PERM-VYATKA-PACKAGE.md, every claim
# re-verified 2026-08-02 — the SECOND consecutive zero-error package;
# decisions 1a/2a/3/4/5a/6 by the main session under the user's
# direct-implement authorization). The smallest slice yet, because
# vanilla already ships the stateless north COMPLETE: nineteen
# type=pop Siberian identities, Bjarmia and the Bashkirs all holding
# zero land, 116 Ob-Ugric/Samoyed locations 100% unowned. Exactly two
# things were wrong, both Russian shells over Finno-Ugric ground:
# VYT — the 1174 Novgorodian Vyatka colony as a live veche republic
# rendering "Republic of Vyatka" under a "Consul" (retired landless,
# its 19 vacated: the basin joins the stateless forest around it) —
# and PRM, a Rurikid principality whose own registry says komi +
# komi_paganism (reshaped by FIELD_FIXES above). GLM/GRS/NZH (1152/
# 1221/1237) are LEFT for the Volga seam per RUS-STEPPE §H's explicit
# reservation — the internal inconsistency with VYT's retirement is
# RECORDED, not hidden (package decision 5's counter).
PERM_LANDLESS = ("VYT",)

# ================================ ARABIA ====================================
# The Arabia package (docs/ARABIA-PACKAGE.md, re-verified 2026-08-01,
# user-approved same day, all recommendations incl. UKH Tier B). One
# new tag QMT (the Qarmatian state of al-Hasa — a MONARCHY with
# elective_succession carrying the council of six: the theocracy shape
# would hit country_ranks' rank_duchy_theocracy branch FIRST and render
# "High Priest", measured static fact), one optional tag UKH (the Zaydi
# Ukhaydirids of al-Yamama, Nasir Khusraw's 1051 eyewitness anchor —
# ruler random, no 11th-c. name survives). Five 13th-century-plus tags
# retire landless: ORM (Hormuzi Oman is 14th c.), JRW (Jarwanids
# 1305+), HLG (Ilkhanate remnant), FDL/AAL (Mamluk-era amirates).
# Their four audit-D1 CAPITAL_FIXES entries from this morning become
# VESTIGIAL (capital on a landless tag — the POR/guimaraes precedent,
# user decision; kept so a vanilla patch still fails loudly).
_ARABIA_RULES = {
    # THE QARMATIAN STATE — Bahrayn proper: al-Ahsa, Qatif, Awal
    # (manama/sayhat return from ORM — vanilla itself marks them JRW's
    # cores), Qatar, the Nita/Yabrin edge, kazimah from HLG. The four
    # minus-singles are desert-tribe ground deliberately left (AAD ×2,
    # YAS, MRH).
    "QMT": (["al_ahsa_province", "batin_province", "nita_province",
             "qatar_province", "yabrin_province"],
            [], [],
            ["hafar_al_batin", "mashdhubah", "sir_bani_yas", "yabrin"],
            28),
}
_ARABIA_GRANTS = {
    # Oman decision O-1: Kerman takes the Batinah + Muscat (Qavurt's
    # conquest, 1053 or 1063 [D] — before 1066 either way; Seljuk
    # dominance to 1154); the Ibadi imamate takes the Trucial six.
    # NOTE: OMA's existing claims list is exactly the KRM 14 — kept
    # DELIBERATELY as the imamate's permanent irredenta on the coast
    # (user-approved; historically the Nabhani future).
    "KRM": ["suhar", "al_khaburah", "khor_fakkan", "nakhal", "rustaq",
            "saham", "shinas",
            "masqat", "al_kamil_wal_wafi", "as_sib", "jalan_buani_buali",
            "masirah", "qalhat", "sur"],
    "OMA": ["julfar", "abu_dhabi", "al_ayn", "al_dhaid", "dubai",
            "sharjah"],
    # The Darb Zubayda to the Mazyadids of Hilla (decision 3: HLL —
    # the Bedouin power of the Kufa desert, seated Dubays I).
    "HLL": ["zubala", "al_labbah", "al_thulayma", "al_waqbi",
            "linah", "lowqah"],
    # The Jawf to ANZ: retires AAL AND fixes ANZ's VANILLA-side orphan
    # capital (dumat_al_jandal was never ANZ's in vanilla either —
    # this grant closes a Paradox defect for free).
    "ANZ": ["dumat_al_jandal", "aba_al_qur", "al_hamad", "arar",
            "sakaka"],
    # UKH (Tier B): the six Wadi Hanifa locations, KLB 5 + SBY 1.
    "UKH": ["al_yamamah", "al_hajr", "diriyah", "malham", "thadiq",
            "ad_dilam"],
}
# KLB was CAUGHT AT IMPLEMENTATION (2026-08-01): its total holding IS
# the five Wadi Hanifa locations UKH takes — the package's own donor
# table said "KLB 5" without noticing that empties the tag. Landless
# with claims is the coherent answer: the sources say "the Banu Kilab
# eventually took control sometime after 1051" — the claims ARE that
# future, the GRA shape exactly.
ARABIA_LANDLESS = ("ORM", "JRW", "HLG", "FDL", "AAL", "KLB")

# QMT — Emirate of al-Ahsa. COASTAL include (al_qatif/manama/al_bidda);
# the coastal variant keeps heir_selection, restated anyway for the
# elective override. ismaili_policy + ismaili_school is vanilla's own
# pairing (QHT and seven others); nizari/mustali are post-1094.
# tolerated: JRW's own pair + iraqi_culture (kazimah arrives from HLG
# with iraqi template culture — coverage gap found at review).
NEW_COUNTRIES["QMT"] = (
    "\tQMT = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_middle_east"\n'
    '\t\tinclude = "muslim_monarchy_no_abrahamic_dhimmi"\n'
    "\t\tgovernment = {\n"
    "\t\t\ttype = monarchy\n"
    # elective_succession (government_types/00_default.txt:9, the
    # monarchy list) carries Nasir Khusraw's council of six — the
    # least-bad shape for a state with no dynastic succession at all.
    "\t\t\their_selection = elective_succession\n"
    "\t\t\tlaws = {\n"
    "\t\t\t\tlegal_code_law = sharia_law_policy\n"
    "\t\t\t\tsharia_law = ismaili_policy\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t\treligious_school = ismaili_school\n"
    "\t\ttolerated_cultures = {\n"
    "\t\t\tkaliji_culture\n"
    "\t\t\tnajdi_culture\n"
    "\t\t\tiraqi_culture\n"
    "\t\t}\n\n"
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = al_ahsa\n\t}\n")

# UKH — Emirate of al-Yamama (Tier B, taken by user decision 4).
# Inland: the _no_coast variant drops heir_selection — restated.
# Zaydi (the Banu Ukhaydhir were Zaydi Alids); ruler random — no
# 11th-century Ukhaydirid is named in any source found.
NEW_COUNTRIES["UKH"] = (
    "\tUKH = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_middle_east"\n'
    '\t\tinclude = "muslim_monarchy_no_abrahamic_dhimmi_no_coast"\n'
    "\t\tgovernment = {\n"
    "\t\t\their_selection = cognatic_primogeniture\n"
    "\t\t\tlaws = {\n"
    "\t\t\t\tlegal_code_law = sharia_law_policy\n"
    "\t\t\t\tsharia_law = zaidi_policy\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t\treligious_school = zaidi_school\n\n"
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = al_yamamah\n\t}\n")

# VMD — the county of Vermandois, the France slice's one new tag (see
# the registry file's comment for the PIC-reuse rejection). Inland →
# catholic_monarchy_no_coast; the catholic no_coast variant KEEPS
# heir_selection (diff-measured 2026-07-29 — unlike the muslim
# family), so nothing is restated. expl_western_europe grants
# france_region, which contains saint_quentin (capital assert).
NEW_COUNTRIES["VMD"] = (
    "\tVMD = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_western_europe"\n'
    '\t\tinclude = "catholic_monarchy_no_coast"\n'
    "\t\tcountry_rank = rank_county\n\n"
    "\t\tcapital = saint_quentin\n\t}\n")

# DUB and ULD — the British slice's two new tags. Both ride
# gaelic_tribe (type = tribe — which is ALSO what makes their
# tributary ties gate-free, tributary.txt:21) + an explicit
# expl_western_europe (grants great_britain_region AND ireland_region;
# there is no expl_british_isles). rank_duchy: the Kingdom of Dublin
# and Ulaid are kingdoms of the Irish grade — LEI's own rank.
NEW_COUNTRIES["DUB"] = (
    "\tDUB = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_western_europe"\n'
    '\t\tinclude = "gaelic_tribe"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = dublin\n\t}\n")
NEW_COUNTRIES["ULD"] = (
    "\tULD = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_western_europe"\n'
    '\t\tinclude = "gaelic_tribe"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = downpatrick\n\t}\n")

# Southern Italy: the catholic five ride the plain coastal
# catholic_monarchy (no nesting, no discovery of its own — read in
# full; expl_mediterranean carries italy_region). The muslim two
# mirror the taifa block (Maliki — Sicily's Islam was Ifriqiyan)
# with the Iberian discovery stack replaced by expl_muslim_
# mediterranean and the tolerated minority set to the island's REAL
# one: greek_culture (the griko substrate Paradox itself pops —
# 21 units on the island in 06_pops).
for _t, _cap in (("APU", "melfi"), ("CUP", "caserta"),
                 ("SLR", "salerno"), ("NEA", "naples"),
                 ("GAE", "gaeta")):
    NEW_COUNTRIES[_t] = (
        f"\t{_t} = {{\n"
        "\t\tstarting_technology_level = 3\n"
        '\t\tinclude = "expl_mediterranean"\n'
        '\t\tinclude = "catholic_monarchy"\n'
        "\t\tcountry_rank = rank_duchy\n\n"
        f"\t\tcapital = {_cap}\n\t}}\n")
# ZAH — the Zähringen Breisgau/Baar march (HRE slice's one new tag).
# Inland; german_principality adds only magdeburg_rights
# (diff-measured); expl_western_europe grants both German regions.
NEW_COUNTRIES["ZAH"] = (
    "\tZAH = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_western_europe"\n'
    '\t\tinclude = "catholic_monarchy_no_coast"\n'
    '\t\tinclude = "german_principality"\n'
    "\t\tcountry_rank = rank_county\n\n"
    "\t\tcapital = villingen\n\t}\n")

# GERMANY II: the two stem duchies. SAX and SWA exist in vanilla as
# FORMABLES only (00_formable_countries.txt:1348 `SAX_f`/:4080 `SWA_f`,
# each with `name = SAX`/`name = SWA`) — loc, CoA and flag_definition all
# ship, no 10_countries block and no identity block. The formable-reuse
# ground: 49 vanilla tags are simultaneously a formable and a live
# country, and Paradox's own 05_characters.txt:86620 carries
# `tag = LUN # Should be SAX` — an admission that the Billung duchy
# wanted this tag. Identity blocks are added to
# zz_1066_new_countries.txt (the country_manager.cpp:206 law); the
# territory arrives through _GERMANY_GRANTS, ZAH's shape exactly.
NEW_COUNTRIES["SAX"] = (
    "\tSAX = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_western_europe"\n'
    '\t\tinclude = "catholic_monarchy_no_coast"\n'
    '\t\tinclude = "german_principality"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = luneburg\n\t}\n")
NEW_COUNTRIES["SWA"] = (
    "\tSWA = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_western_europe"\n'
    '\t\tinclude = "catholic_monarchy_no_coast"\n'
    '\t\tinclude = "german_principality"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = ulm\n\t}\n")

for _t, _cap in (("PLM", "palermo"), ("AGR", "girgenti")):
    NEW_COUNTRIES[_t] = (
        f"\t{_t} = {{\n"
        "\t\tstarting_technology_level = 3\n"
        '\t\tinclude = "expl_muslim_mediterranean"\n'
        '\t\tinclude = "muslim_monarchy_no_abrahamic_dhimmi"\n'
        "\t\tgovernment = {\n\t\t\tlaws = {\n"
        "\t\t\t\tsharia_law = maliki_policy\n\t\t\t}\n\t\t}\n"
        "\t\tcourt_language = maghrebi_dialect\n"
        "\t\treligious_school = maliki_school\n"
        "\t\tgovernment = { mysticism_vs_jurisprudence = -5 }\n\n"
        "\t\tcountry_rank = rank_duchy\n\n"
        "\t\ttolerated_cultures = {\n\t\t\tgreek_culture\n\t\t}\n\n"
        f"\t\tcapital = {_cap}\n\t}}\n")

# The Fatimid territory, resolved from definitions.txt like the Seljuk
# rules. Variant A-prime (user-approved 2026-07-29): MAM's remaining 120
# minus tobruk (granted to BQA — 1066 Barqa is Zirid-aligned Banu Qurra
# [U/D], and the grant makes al_bayda_province whole under BQA), plus
# AAL's three shaam locations (Damascus hinterland — the 14th-century
# Bedouin confederation is anachronistic there; Damascus is DIRECTLY
# Fatimid-governed on 1066.9.15: Badr al-Jamali, governor of Damascus
# and all Syria from 3 July 1066). BKZ keeps Aswan (the Banu Kanz are a
# Fatimid CLIENT — Kanz al-Dawla is a Fatimid title [U] — hence the
# tributary, not annexation) and MDA keeps al_ais. 119 (MAM) + 3 (AAL)
# = 122. No Damascus tag: Atsiz taking Jerusalem 1073 and Damascus 1076
# is a decade of event material. KOJ (landless, is_historic) untouched.
_EGYPT_RULES = {
    "FAT": (["lower_egypt_area", "upper_egypt_area", "sinai_area",
             "filastin_province", "sharat_province", "lebanon_province",
             "shaam_province", "duba_province", "madian_province",
             "qura_province", "tabuk_province", "umluj_province"],
            [],
            [], ["aswan", "kom_ombo", "al_ais"], 122),
}

# The Fatimid khutba's clients, as TRIBUTARIES (the Seljuk mechanism):
# MEC — the khutba was read in Mecca for al-Mustansir until 15 April
# 1071 (the switch to the Abbasids is an event hook); BKZ — the Banu
# Kanz client emirate at Aswan. MDA is left independent (lower
# confidence); YEM stays independent (al-Sulayhi is a Fatimid da'i but
# chaining MEC under YEM would need a second reform — parked).
# MDA joined 2026-08-01 (Arabia slice): the Sharifate of Medina read
# the Fatimid khutba continuously 974-1151 — the same tie, from the
# same caliph, that MEC and BKZ already model in game.
FATIMID_TRIBUTARIES = ("MEC", "BKZ", "MDA")

# The one donor this slice empties. MAM must be emptied, NEVER deleted:
# 103 DHE references and the EGY formable's potential lean on the tag.
# Its snapshot claims (120 locations) are the Mamluk future as
# irredenta — the GRA/POR shape.
EGYPT_LANDLESS = ("MAM",)

# ------------------------------------------------- the France demesne ---
# FRANCE DEMESNE + LANGUEDOC (Opus package 2026-07-29; user-approved).
# Vanilla FRA holds 163 locations (our build 164 with montpellier);
# the 1066 Capetian demesne was famously tiny. 142 locations leave
# through the rule sets below (138 from FRA + rodez/lautrec from AMG,
# castres from VDM, thiers from FRZ — the four approved HISTORICAL
# moves; aurillac was rejected, it would empty CLT on a [D] reading).
# FRA keeps 19 (Ile-de-France, Orleanais, Sens — Henry I's 1055
# acquisition [U] — and the crown-aligned bishoprics Reims/Laon/
# Noyon/Beauvais/Chalons) and GAINS three through LOCATION_GRANTS:
# etampes (ETA keeps gien — a 12th-c. royal appanage, demesne at
# 1066), dreux (DRE empties — the county is created 1137), montreuil
# (ENG's 1279 Ponthieu-marriage relic; the crown's one seaport since
# Hugh Capet [U]). Lyonnais/Vivarais (7 locations, Kingdom-of-Arles
# side, French only from 1312) stay with FRA as a KNOWING anachronism
# banked for the Empire slice. TOU/BER/VLS rise from landless (their
# own claim lists are the 1066 borders — the ZTA/Duklja shape);
# montpellier reaches TOU through the nimois sweep and MLL's claim on
# it is untouched. NRB keeps Narbonne (autonomous viscounty).
_FRANCE_RULES = {
    "TOU": (["gevaudan_province", "narbonnais_province", "nimois_province",
             "quercy_province", "razes_province", "rouergue_province",
             "toulousain_province"],
            ["agen", "albi", "le_puy", "mirepoix", "montflanquin",
             "lautrec", "castres"],
            [], ["narbonne"], 39),
    "AQN": (["bazadais_province", "limousin_province", "lower_poitou_province",
             "saintonge_province", "turenne_province", "upper_poitou_province"],
            ["brosse", "marmande", "tarbes"],
            [], ["belin", "jonzac", "montendre", "oleron", "rochefort",
                 "royan", "saintes", "ussel", "ventadour",
                 # La Marche's own Limousin holdings + Rochechouart
                 # (RCC's) — measured by the resolver's first run; the
                 # package's minus list had missed them.
                 "aubusson", "bellac", "bourganeuf", "charroux",
                 "gueret", "rochechouart"], 31),
    "BLS": (["brie_champenois_province", "champagne_province",
             "chartrain_province", "perthois_province"],
            ["bar_sur_seine", "chaumont", "choiseul", "epernay",
             "menehould", "vertus"],
            [], ["dreux", "etampes"], 20),
    "VLS": (["amienois_province"],
            ["braine", "chaumont_vexin", "crepy", "soissons"], [], [], 7),
    "VMD": (["thierache_province", "vermandois_province"], [], [], [], 7),
    "AUV": (["lower_auvergne_province", "upper_auvergne_province"],
            [], [], ["aurillac", "vic_le_comte"], 8),
    "ANJ": (["touraine_province"], ["loudun"], [], [], 6),
    "MRC": (["combraille_province"], ["bourganeuf", "boussac"], [], [], 6),
    "BER": (["upper_berry_province"],
            ["chateauroux", "issoudun", "lignieres"],
            [], ["gien", "sancerre"], 6),
    "PER": (["perigord_province"], [], [], ["perigueux", "riberac"], 3),
    "FLA": (["roman_flanders_province"], [], [], [], 3),
    "BUR": ([], ["grancey", "langres", "macon"], [], [], 3),
    "COM": ([], ["saint_gaudens"], [], [], 1),
    "RET": ([], ["grandpre"], [], [], 1),
    "BAR": ([], ["vaucouleurs"], [], [], 1),
}

# The Capetian homage ring: the six northern fiefs that historically
# did homage to Philip I, as TRIBUTARIES (war-capable, own color,
# cancellable — tributary.txt:86-93; the vassal type the 1337 web used
# blocks war declarations, vassal.txt:80-86, the round-2 freeze).
# NOT tied, deliberately: NRM (the Norman Conquest machine — hard
# constraint), TOU/BRI and the whole Occitan south (outside royal
# reach in 1066), AQN (the [D] call — homage was nominal and loose).
FRANCE_TRIBUTARIES = ("FLA", "BUR", "BLS", "VLS", "VMD", "ANJ")

# DRE empties (the county of Dreux is created 1137 for Robert of
# France [U]; at 1066 dreux is royal demesne) — landless with its one
# location as the claim.
FRANCE_LANDLESS = ("DRE",)

# ------------------------------------------------- the British Isles ---
# THE BRITISH ISLES (Opus package 2026-07-29, user-approved before
# leaving; the LAN/CET-into-ENG fold is DEFERRED to a post-launch pass
# — it was the one item flagged with a conquest-balance cost, and the
# Norman machine is untested against this slice). Explicit grant
# lists, the Sardinia shape — the six Welsh shells' claim lists
# partition wales_area EXACTLY 25/25 (Paradox wrote the 1066 border),
# and every Irish/Scottish move is location-cited in the package.
# Headline finds: SBL, the 1332 Balliol Pretender, holds Edinburgh/
# Perth/Stirling/Roxburgh at start (revolt = yes, "Support from the
# English" — 10_countries.txt:4563); and Irish tributaries need NO
# reform (tributary.txt:21 — the SUBJECT-is-a-tribe branch of the
# visible gate; every Gaelic tag is type = tribe via its template).
_BRITISH_GRANTS = {
    # Wales: the marcher dissolution. ewyas -> GWT is the [D] call
    # (culture = welsh, location_templates:1596); ludlow/wigmore/
    # oswestry are English-culture English shires -> ENG.
    "GDD": ["carnarvon", "anglesey", "conwy", "harlech", "flint", "denbigh"],
    "PWS": ["penllyn", "montgomery", "machynlleth", "llangollen"],
    "DHB": ["carmarthen", "cardigan", "aberystwyth", "pembroke",
            "fishguard", "kidwelly", "brecknock", "builth", "radnor"],
    "MWG": ["cardiff", "caerphilly", "neath", "swansea"],
    "GWT": ["monmouth", "newport", "ewyas"],
    "ENG": ["ludlow", "wigmore", "oswestry"],
    # Ireland: the Pale and the 14th-century earldoms undone.
    "MCM": ["limerick", "cork", "waterford", "kinsale", "youghal",
            "dungarvan", "dingle", "tralee", "adare", "killmallock",
            "fermoy", "clonmel", "cashel", "roscrea", "nenagh",
            "castleconnell", "tipperary", "ennis", "bunratty", "moyarta"],
    "LEI": ["wicklow", "wexford", "new_ross", "carlow", "athy",
            "kildare", "naas"],
    "DUB": ["dublin", "fingal"],
    "MTH": ["trim", "navan", "kells", "mullingar", "ballymore",
            "drogheda", "dundalk"],
    "OSS": ["kilkenny"],
    "CNN": ["galway", "athenry", "tuam", "castlebar", "erris",
            "ballaghaderreen"],
    "ULD": ["carrickfergus", "downpatrick", "dunluce", "belfast",
            "newtownards", "ballymena", "ballycastle"],
    "BFN": ["cavan", "killycolly"],
    # Scotland, the Isles, and England's relics. berwick: Lothian is
    # Scottish from 1018 and SCO claims it (one conquerable location
    # fewer for William — noted). thurso+Sutherland: Caithness was
    # the Orkney earls' and ORK claims thurso; the sutherland sweep
    # is the [U] extension, taken. mann/skye/arran are norse_gael
    # (location_templates) and mann/skye are LOI's OWN claims.
    "SCO": ["perth", "edinburgh", "stirling", "roxburgh", "linlithgow",
            "duns", "lanark", "strathearn", "cupar", "dumfries",
            "berwick"],
    "GLY": ["kirkcudbright", "kenmure", "stranraer", "ayr", "irvine"],
    "ORK": ["thurso", "dornoch", "durness", "tongue"],
    "LOI": ["mann", "skye", "arran"],
    "NRM": ["jersey"],
    "BGN": ["abbeville"],
}

# (overlord, subject) pairs — Irish overlords differ, unlike the
# single-overlord SEL/FAT/FRA rings. Five are CONVERSIONS of vanilla
# vassal ties (war-blocking) to tributary (war-capable, own color);
# LEI->DUB is new — Murchad rules Dublin for his father. NO reform
# needed: every subject is a gaelic tribe (the free gate branch).
BRITISH_TRIBUTARIES = (("LEI", "DUB"), ("LEI", "OSS"), ("TRY", "AMH"),
                       ("TYR", "INI"), ("TYR", "KEE"), ("MCM", "BEA"))

# 25 tags end landless-with-claims: Wales 11 (the ten marchers + the
# 1267 Principality), Ireland 12 (the Pale + the Norman earldoms +
# the 1256 East Breifne), Britain 2 (SBL the 1332 pretender, MNN the
# 1333 English Mann). BCN is NOT here — it already holds zero and the
# stale-entry check would rightly kill the build. LAN/CET stay LANDED
# (the deferred fold); DCI keeps its one location (the Deisi are
# genuine 1066); DHM stays (a defensible 1066 bishopric).
BRITISH_LANDLESS = (
    "WLS", "GWR", "GMG", "MAC", "AUD", "BRO", "POS", "EWY", "CMS",
    "PMB", "DEN",
    "PLE", "DMS", "ORD", "CWM", "KID", "ULS", "CLA", "CLR", "MYO",
    "GLS", "THO", "CVN",
    "SBL", "MNN",
)

# ------------------------------------------------- southern Italy 1066 ---
# THE MEZZOGIORNO (Opus package 2026-07-29, user-approved). Explicit
# grant lists; donors NAP 65 (emptied), SIC 22->4 (KEPT as Roger's
# Norman county — vanilla locks 6 advances behind has_or_had_tag =
# SIC and every one is Norman-Sicilian content: the Constitutions of
# Melfi, the Studium Generale; an emir must never hold them), SAO 1
# (the Frankokratia duchy of Salona, holding ONLY malta since our
# Byzantium slice took its Greek locations). The 10 Abruzzo locations
# ride with APU as a KNOWING ANACHRONISM (imperial in 1066; aquila is
# a 1254 foundation — the Lyonnais precedent, banked for the HRE
# slice). Amalfi has NO map location (like Capua-city and Aversa,
# both inside caserta) — the gap is recorded, no tag is possible.
# NAP's landless snapshot auto-yields 65 mainland + its existing 22
# Sicilian claims = the 87-location Two Sicilies irredenta (the 1282
# Angevin future); SAO's yields vanilla's four Salona claims back.
_ITALY_GRANTS = {
    # The 10 Abruzzo locations LEFT this list the same day it landed:
    # the HRE slice resolved the banked anachronism by reviving SPL
    # (Spoleto takes them + its own five Umbrian claims). APU 47->37;
    # the Molise four stay (Norman since c.1054 [U]).
    "APU": ["bojano", "isernia", "larino", "trivento",
            "foggia", "bovino", "lucera", "manfredonia", "rotondo",
            "sansevero", "altamura", "andria", "francavilla",
            "martinafr",
            "potenza", "acerenza", "lagonegro", "matera", "melfi",
            "montepeloso", "santarcangelo",
            "catanzaro", "cotrone", "gerace", "monteleone", "nicastro",
            "palmi", "reggiocal",
            "cosenza", "cassano", "castrovillari", "scalea", "paola",
            "rossano",
            "avellino", "ariano", "santangelo"],
    "CUP": ["caserta", "venafro", "piedimonte", "sora"],
    "SLR": ["salerno", "campagna", "salacon", "vallo"],
    "NEA": ["naples", "nola"],
    "GAE": ["gaeta"],
    "PLM": ["palermo", "corleone", "mazara", "salemi", "trapani",
            "termini", "cefalu", "sciacca", "malta"],
    "AGR": ["girgenti", "bivona", "caltanisetta", "piazza", "catania",
            "syracuse", "caltagirone", "modica", "noto",
            "terranovasic"],
}

# The Byzantine catepanate restored: Bari (the catepan's seat, falls
# 16 April 1071 — the situation hook), the Terra d'Otranto, and the
# [D] Taranto/Brindisi pair on the recovered-1060s reading. BYZ's
# expl_mediterranean already grants italy_region — no blind capital.
_ITALY_BYZ_EXTRA = ["bari", "barletta", "monopoli", "brindisi",
                    "lecce", "gallipoliita", "taranto"]

# The Melfi investiture: Guiscard and Richard as PAPAL tributaries
# under papal_investiture_reform (the khutba pattern's fourth use;
# first theocracy overlord). SIC/SLR/NEA/GAE independent; the
# emirates independent.
ITALY_TRIBUTARIES = (("PAP", "APU"), ("PAP", "CUP"))

# NAP (the 1282 Angevin kingdom) and SAO (Salona) end landless.
ITALY_LANDLESS = ("NAP", "SAO")

# ------------------------------------------------------- the Empire ---
# THE HRE/HAB SLICE (Opus package 2026-07-29; crown = user decision D).
# HAB is REUSED as the Babenberg margraviate of Austria (its loc IS
# "Austria"; the SIC precedent — and country_HAB advances stay armed):
# keeps its 16 austria_area locations, dynasty habsburg->babenberg,
# rank county + the margraviate reform (vanilla's own rank branch
# renders "Margraviate"/"Margrave" — country_ranks.txt:2298, a free
# win; the reform is setup-assigned by NINE vanilla tags). STY/CRH
# revive from their Paradox-written claim lists (the SKE case);
# GOR/ORT/GRK dissolve (1127/12th-c./1072 creations). The Salian
# demesne (Standard 9) empties nine one-location free cities — the
# member/free-city lists self-clean through the generic landless-IO
# strip. SPL revives with its five Umbrian claims + the ten Abruzzo
# (closing the Italy slice's banked anachronism); the Lyonnais 7
# resolve to FRZ/SAV/VLN (closing the France slice's). ZAH is the one
# new tag (the Zähringen Breisgau march).
_EMPIRE_GRANTS = {
    "OGK": ["goslar", "nordhausen", "muhlhausen", "speyer", "worms",
            "frankfurt", "nuremberg", "aachen", "dortmund"],
    "STY": ["graz", "voitsberg", "judenburg", "kapfenberg", "leoben",
            "liezen", "murau", "murzzuschlag", "rottenmann",
            "schladming", "feldbach", "furstenfeld", "weiz", "pitten",
            "wiener_neustadt", "maribor", "slovenj_gradec",
            "steyr", "wels", "bad_ischl", "gmunden", "kirchdorf"],
    # novo_mesto/postojna left this list with Italy North: the Carniolan
    # interior is Ulric's march (ISR), not Berthold's duchy — they now
    # travel straight from their pre-slice owner (grant lists must be
    # disjoint). CRH revives with 11.
    "CRH": ["klagenfurt", "st_veit", "volkermarkt", "steinfeld",
            "ljubljana", "kranj",
            "hermagor", "lienz", "winklern", "spittal", "feldkirchen"],
    "PSS": ["freistadt", "perg", "rohrbach", "linz", "st_georgen"],
    "AUG": ["krumbach", "gunzburg", "wertingen"],
    "RVA": ["waldsee", "saulgau"],
    "ALS": ["ensisheim"],
    "KYB": ["kyburg", "frauenfeld", "aarau", "baden_im_aargau",
            "wolhusen"],
    "NEL": ["schaffhausen"],
    "VUD": ["fribourg"],
    "ZAH": ["bonndorf", "villingen", "waldshut", "glarus"],
    "BXN": ["bruneck"],
    # GOR dissolves four ways now: gorizia stays with the patriarch;
    # metlika/kocevje/pazin (pazin was GOR's SEVENTH location, missed
    # by the HRE package inventory and caught by the landless
    # guarantee's first dry-run) went to AQU until Italy North rerouted
    # them into ISR — Ulric's march of Carniola-Istria, the user's ISR
    # decision. Grant lists must be disjoint, so they leave this list
    # rather than bouncing through the patriarchate.
    "AQU": ["gorizia"],
    "SPL": ["assisi", "narni", "rieti", "spoleto", "todi",
            "chieti", "lanciano", "vasto", "aquila", "atri", "celano",
            "cittaducale", "csantangelo", "sulmona", "teramo"],
    "FRZ": ["lyon", "riverie", "beaujeu", "perreux"],
    "SAV": ["trevoux"],
    "VLN": ["viviers", "chalancon"],
}

# The nine emptied free cities + the three dissolved southeastern
# tags. GOR (county created c.1127), ORT (12th c.), GRK (bishopric
# founded 1072 — six years after start).
EMPIRE_LANDLESS = ("GOS", "NHS", "MLH", "SYE", "WRM", "FRN", "NUR",
                  "AAC", "DTM", "GOR", "ORT", "GRK")

# ------------------------------------------------------- Germany II ---
# GERMANY II (Opus package 2026-07-29, user-approved). The two stem
# duchies are rebuilt out of the statelets that inherited their ground,
# the Artois is handed back to Flanders, and Hamburg-Bremen becomes the
# archbishopric it was in 1066 rather than the two free cities it
# becomes in 1186/1189. Explicit lists throughout — every donor was
# checked against the CURRENT build's own holdings before a location
# entered a list (the AQN 43-vs-31 lesson).
# UTR takes the three Groningen locations only: FRI KEEPS its peasant
# republic and its other eight, because the Frisian Freedom is genuine
# 1066 and the bishop's Groningen claim is the part that is not.
_GERMANY_GRANTS = {
    # SAX: the whole Billung duchy, all 11 from LUN.
    "SAX": ["luneburg", "celle", "dannenberg", "ebstorf", "fallingbostel",
            "harburg", "isenhagen", "luchow", "uelzen", "winsen",
            "winsen_aller"],
    # SWA: 21 locations out of the eleven Swabian statelets that carve
    # the stem duchy up at 1337 — WUR 10, then ULM, TUB, HLF, HEH,
    # OET 2, HHB 2, KIR 2, WDB 1.
    "SWA": ["stuttgart", "backnang", "calw", "goppingen", "nagold",
            "oberndorf", "riedlingen", "sigmaringen", "urach", "welzheim",
            "ulm",
            "tubingen",
            "helfenstein",
            "heidenheim",
            "oettingen", "vaihingen",
            "hohenberg", "horb",
            "erbach_swabia", "illereichen",
            "waldburg"],
    # The archbishopric of Hamburg-Bremen, whole: BRM and HAM are the
    # free cities of 1186 and 1189, a century and more after start.
    "BRE": ["bremen", "hamburg"],
    # The Artois back to Flanders: ARS is the 1237 apanage, and in 1066
    # Arras is Baldwin V's. Seven locations.
    "FLA": ["arras", "bapaume", "bethune", "calais", "hesdin", "lens",
            "saint_omer"],
    # Groningen to the prince-bishop (partial on purpose — see above).
    "UTR": ["groningen", "appingedam", "wedde"],
}

# The thirteen donors this slice empties. Each keeps its registry
# identity and its former holdings become claims — the GRA/POR/MLL
# landless-with-irredenta shape the build automates through
# LANDLESS_AFTER and _landless_claims. LUN keeps welfen_dynasty on its
# shell (the Welf future is real, it just is not 1066's) and WUR keeps
# wurttemberg_dynasty for the same reason.
GERMANY_LANDLESS = ("LUN", "WUR", "ULM", "TUB", "HLF", "HEH", "OET",
                    "HHB", "KIR", "WDB", "ARS", "HAM", "BRM")

# ------------------------------------------------------- Italy North ---
# ITALY NORTH (approved package 2026-07-29; user decisions: TUS revived
# via formable reuse, FLO empties into it, ISR new for Ulric of Weimar,
# RAV takes faenza+imola). TUS rides the SAX/SWA formable-reuse ground:
# TUS_f (00_formable_countries.txt:4229) ships name = TUS, tag = TUS,
# color = map_TUS (vanilla named_colors/02_map.txt:749), loc and CoA —
# only the identity block and territory are missing. ISR is genuinely
# free (whole-tree word-grep over game and mod: zero standalone hits)
# and wears vanilla's own unused map_ISR named color (02_map.txt:138,
# an Adriatic blue) — the SKE named-color route, no zz_1066_map_colors
# entry needed; the package's "new color" step died against vanilla.
# Both take their donors' Italian five-include discovery stack; ISR
# adds expl_western_europe because its Carniolan interior (postojna/
# novo_mesto) came from CRH, which sees through that template — the
# blind-capital lesson applied at authoring time.
NEW_COUNTRIES["TUS"] = (
    "\tTUS = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_mediterranean"\n'
    '\t\tinclude = "expl_silk_road_west"\n'
    '\t\tinclude = "expl_silk_road_center"\n'
    '\t\tinclude = "expl_silk_road_east"\n'
    '\t\tinclude = "expl_indian_trade_route"\n'
    '\t\tinclude = "catholic_monarchy"\n'
    "\t\tcountry_rank = rank_duchy\n\n"
    "\t\tcapital = lucca\n\t}\n")
# ISR copies HAB's WHOLE march shape — rank_county plus the vanilla
# margraviate reform (the pair is what renders "Margraviate"/"Margrave",
# country_ranks.txt:2298; nine vanilla tags assign the reform in setup).
# court_language: the Weimar margrave's German court over croatian pops
# (central_german_dialect, cultures/german.txt:764) — the PLM
# elite-vs-pop split, maghrebi over sicilian, exactly.
NEW_COUNTRIES["ISR"] = (
    "\tISR = {\n"
    "\t\tstarting_technology_level = 3\n"
    '\t\tinclude = "expl_mediterranean"\n'
    '\t\tinclude = "expl_silk_road_west"\n'
    '\t\tinclude = "expl_silk_road_center"\n'
    '\t\tinclude = "expl_silk_road_east"\n'
    '\t\tinclude = "expl_indian_trade_route"\n'
    '\t\tinclude = "expl_western_europe"\n'
    '\t\tinclude = "catholic_monarchy"\n'
    "\t\tgovernment = {\n\t\t\treforms = {\n\t\t\t\tmargraviate\n\t\t\t}\n\t\t}\n"
    "\t\tcourt_language = central_german_dialect\n"
    "\t\tcountry_rank = rank_county\n\n"
    "\t\tcapital = pazin\n\t}\n")

# Every location's CURRENT owner was verified against the built
# 10_countries before it entered a list (the AQN lesson): all donors
# clean, no exceptions. Two package expectations corrected on
# measurement: sansepolcro's owner is PEA (Perugia — which keeps its
# other two locations and is NOT landless), and postojna/novo_mesto
# came from CRH (the HRE slice's Carniola), not AQU — a clean donor,
# and historically right: Ulric's Carniolan march was never the
# patriarch's. MLO's own_control_conquered is EXACTLY the 22 granted
# (measured token-for-token); it keeps its seven own_control_core
# (milano legnano rho varese monza lecco treviglio). VER keeps verona,
# the Brescia block (banked Tier B) and its core; the government swap
# attempt was ABORTED per the package's own condition: VER's block
# restates type = republic + signoria_selection + a
# dynastic_signoria_reform block — far beyond an include+rank swap.
_NITALY_GRANTS = {
    # The march of Tuscany: Tuscany 18 + Emilia 15 = 33. Canossa itself
    # (the house's seat) rides in MAN's donation.
    "TUS": ["lucca", "massa", "pescia",
            "florence", "mangona", "poggibonsi", "sanlorenzo", "arezzo",
            "prato", "pistoia", "volterra", "cortona",
            "sansepolcro",
            "siena", "massamar", "chiusi", "montalcino", "grosseto",
            "canossa", "reggioem", "guastalla", "mantova", "goito",
            "ostiglia", "mirandola", "asola",
            "modena", "frassinoro", "nonantola", "ferrara", "ficarolo",
            "comacchio", "argenta"],
    # The eight MLO carve-outs = exactly MLO's own_control_conquered.
    "BGM": ["bergamo", "cortenuova", "clusone", "zogno"],
    "CRM": ["cremona", "casalmaggiore", "soncino"],
    "LDI": ["lodi"],
    "NVA": ["novara", "arona", "domodossola", "varallo"],
    "VRC": ["vercelli", "biella"],
    "PCZ": ["piacenza", "bardi", "fiorenzuola"],
    "LCA": ["como", "lugano"],
    "CHV": ["chiavenna", "bormio", "tresivio"],
    # The VER carve-outs: the Veneto's bishops and the two returns.
    "VIN": ["vicenza", "bassano", "schio"],
    "CEN": ["ceneda", "conegliano"],
    "FEL": ["feltre", "belluno"],
    "TRV": ["treviso", "castelfranco", "mestre"],
    "TNT": ["rovereto"],
    "AQU": ["cividale"],
    # The march of Istria-Carniola: VEN's two Istrian ports; buzet
    # from AQU's own vanilla holdings; pazin/metlika/kocevje straight
    # from dissolving GOR (rerouted out of the HRE slice's AQU grant —
    # lists must be disjoint); postojna/novo_mesto from CRH's
    # Carniolan interior.
    "ISR": ["pola", "rovinj",
            "pazin", "buzet", "metlika", "kocevje",
            "postojna", "novo_mesto"],
    "PAD": ["rovigo"],
    "CRO": ["pag"],
    # Adelaide's march of Turin: seven single-location statelets and
    # MFA's lanzo fold into the arduinici domain.
    "PIE": ["lanzo", "cuneo", "saluzzo", "carmagnola", "chieri", "alba",
            "mondovi", "ceva"],
    "MFA": ["alessandria"],
    "SAV": ["aosta", "chatillonaos", "morgex"],
    # The archbishop takes his Romagna: faenza and imola (FAE and IMO
    # empty — 1066 Romagna is the IMPERIAL archbishop of Ravenna's
    # world, the HRE slice's PAP->FAE finding carried to its end).
    "RAV": ["faenza", "imola"],
}

# The eighteen donors this slice empties. Each keeps its registry
# identity; former holdings become claims (the GRA/POR shape the build
# automates). PEA is NOT here — it donates sansepolcro and keeps
# Perugia; MLO/VER/VEN/CRH/MFA/PRO keep cores and are not landless.
NITALY_LANDLESS = ("LUC", "FLO", "PRA", "PST", "VLT", "COT", "SIE",
                   "MAN", "FER", "SAL", "CHX", "ABA", "MND", "CEV",
                   "ASD", "AOS", "FAE", "IMO")

# Nine clients under the Seljuk khutba as TRIBUTARIES — war-capable,
# own color, own name (tributary.txt:5,7,92,93). ABS, GHZ and SRV stay
# independent: the caliph outranks the sultan, the Ghaznavid peace of
# 1059 was a treaty not a submission, and Alp Arslan's Shirvan campaign
# is 1067 — a year after start, an event's job.
SELJUK_TRIBUTARIES = ("KRM", "KKY", "SIS", "MZN", "SHD", "UQY", "MRD",
                     "HLB", "HLL")

# The 60 donors this slice empties — Mongol-era and Ottoman-era Persia/
# Iraq/Jazira wholesale (JAL keeps its horde government, which never
# renders on a landless tag: the naming trap stays unarmed).
SELJUK_LANDLESS = (
    "APD", "ARD", "ART", "ASR", "ATQ", "ATZ", "BDS", "BHT", "BIT", "BSD",
    "DGE", "DIL", "DMB", "DML", "DSN", "FAL", "GRG", "HBN", "HDN", "HDR",
    "HNY", "HSN", "HZP", "HZR", "INJ", "JAL", "JKR", "JUR", "KEL", "KHF",
    "KHT", "KHU", "KIL", "KKL", "KLR", "KRI", "KRT", "KSA", "KTW", "LCK",
    "LST", "MIH", "MKW", "MRV", "MZF", "MZJ", "NGD", "QOM", "RKL", "SBZ",
    "SFR", "SHB", "SLI", "SOH", "SRB", "SUT", "SYY", "UGH", "ZBR", "ZRQ",
)

# The 45 donors the sweep leaves with nothing. Each ends landless with
# claims equal to EVERYTHING it held before the pass (snapshotted at
# build time) — for the beyliks and Frankokratia those claims are their
# historical re-emergence. Nothing is deleted; every registry entry stays.
BYZ_LANDLESS = (
    "ACH", "AHI", "ALB", "ALY", "ANT", "ARG", "ARM", "ATH", "AYD", "BFR",
    "BOD", "BUL", "CEP", "CIL", "CND", "CRT", "CYP", "DUL", "EPI", "ERE",
    "FEO", "GRM", "HCI", "HMD", "INA", "KAR", "KBD", "KNI", "KRD", "MEN",
    "MTR", "MUS", "MZK", "NAX", "NEG", "NEO", "PAT", "SHP", "SRU", "TDJ",
    "TEK", "THP", "TUR", "TVS", "TRE",
)

# Displaced tags end LANDLESS (vanilla's own LON shape — a landless kingdom
# keeps its capital and its claims, 10_countries.txt:14682) with their
# former locations WRITTEN INTO their claims lists:
# - GRA: the Nasrid emirate IS Granada's future, expressed as irredenta.
# - POR: in 1066 Portugal is a county inside García's Galicia; the claims
#   are the 1128/1139 emergence. Vanilla's full 67-location list.
# - MLL: the 1276 kingdom; its islands are DYA's, its Roussillon residual
#   is CDY/RSL's, montpellier FRA's. Vanilla's full 9-location list.
DISPLACED_CLAIMS = {
    # ORM (Arabia slice, user decision 12): the automatic snapshot would
    # be its 22 Arabian holdings only — a Kingdom of Hormuz whose
    # irredenta excludes Hormuz itself. Vanilla's own 36, byte-for-byte.
    # HLG/FDL keep the automatic snapshot: their vanilla holdings are
    # mostly Iraq/Syria and belong to nobody's 1066 irredenta.
    "ORM": ["hormuz", "gamrun", "bandar_charak", "bandar_khamir",
            "bandar_lengeh", "kish", "minab", "manujan", "nowdezh",
            "rudkhaneh", "shaqrud", "senderk", "sirik", "julfar",
            "al_dhaid", "khor_fakkan", "shinas", "machul", "abu_dhabi",
            "al_ayn", "dubai", "sharjah", "masqat", "al_kamil_wal_wafi",
            "as_sib", "jalan_buani_buali", "masirah", "qalhat", "sur",
            "suhar", "al_khaburah", "nakhal", "rustaq", "saham",
            "manama", "sayhat"],
    "GRA": ["granada", "adra", "almunecar", "guadix", "huescar", "illora",
            "loja", "pinar", "orgiva", "malaga", "antequera", "velez_malaga",
            "almeria", "almanzora", "baza", "gergal", "mojacar",
            "velez_rubio"],
    "POR": ["lagos", "faro", "silves", "tavira", "evora", "alvalade",
            "alvito", "avis", "beja", "crato", "elvas", "estremoz",
            "mertola", "montemor", "mora_portugal", "moura", "odemira",
            "ourique", "ponte_sor", "portalegre", "portel", "salvaterra",
            "serpa", "sines", "vila_vicosa", "coimbra", "besteiros",
            "castelo_branco", "covilha", "esgueira", "feira", "guarda",
            "idanha", "lamego", "meda", "pinhel", "proenca_nova", "sabugal",
            "seia", "trancoso", "viseu", "lisbon", "alcacer_do_sal",
            "alcobaca", "chao_de_couce", "figueira", "leiria", "santarem",
            "setubal", "tomar", "torres_novas", "torres_vedras", "porto",
            "aguiar", "barcelos", "braga", "guimaraes", "montalegre",
            "valenca", "viana_do_castelo", "braganca", "chaves", "macedo",
            "miranda_de_i_douro", "mirandela", "moncorvo", "vila_real"],
    "MLL": ["puigcerda", "prades", "montpellier", "perpignan", "palma",
            "ciudadela_de_menorca", "ibiza", "manacor", "pollensa"],
}
if len(DISPLACED_CLAIMS["POR"]) != 67:
    sys.exit("DISPLACED_CLAIMS: POR must carry vanilla's exact 67 claims")
# Tags that must hold ZERO locations once the transfers have run.
LANDLESS_AFTER = ("GRA", "POR", "MLL") + BYZ_LANDLESS + SELJUK_LANDLESS \
    + EGYPT_LANDLESS + FRANCE_LANDLESS + BRITISH_LANDLESS \
    + ITALY_LANDLESS + EMPIRE_LANDLESS + GERMANY_LANDLESS \
    + NITALY_LANDLESS + CENTRALASIA_LANDLESS + RUS_LANDLESS \
    + ARABIA_LANDLESS + RUS2_LANDLESS + CHINA_LANDLESS + NORTH_LANDLESS \
    + INDIA_LANDLESS + BALTIC_LANDLESS + AFRICA_LANDLESS + SEA_LANDLESS \
    + TIBET_LANDLESS + PERM_LANDLESS + AMERICAS_LANDLESS

# tag -> locations granted to an EXISTING tag: removed from their current
# owner, written into the tag's own_control_core (created if absent — the
# landless giudicati have none), and dropped from the tag's own claims
# list, since owned land is no longer "conquered by others".
# THE SARDINIA SLICE: the four giudicati's claim lists ARE their 1066
# borders, written by Paradox (Italy pass, re-verified byte-for-byte).
# Rulers: TOR and CAG get their judges; ARB's 1066 judge is genuinely
# obscure and GAL's is unattested — both stay `ruler = random`; Corsica
# has no single 1066 ruler at all (territory only).
LOCATION_GRANTS = {
    "TOR": ["sassari", "alghero", "bosa", "macomer", "bitti", "thiesi", "castelsardo", "ozieri"],
    "CAG": ["cagliari", "tratalias", "villa_di_chiesa", "isili", "muravera", "seddori", "tortoli"],
    "GAL": ["orosei", "terranova_pausania", "posada", "tempiopausania"],
    "COR": ["aleria", "bastia", "calvi", "corte", "ajaccio", "bonifacio", "sartene", "vico"],
    # MAM's Cyrenaican toehold to Barqa: 1066 Barqa is the Banu Qurra
    # emirate under ZIRID suzerainty [U/D], not Fatimid — and the grant
    # makes al_bayda_province whole under BQA (Fatimid slice).
    "BQA": ["tobruk"],
    # The three demesne additions (France slice): etampes from ETA
    # (12th-c. royal appanage; ETA keeps gien), dreux from DRE (county
    # created 1137 — DRE empties, FRANCE_LANDLESS), montreuil from ENG
    # (the 1279 Ponthieu-marriage relic; the crown's seaport since
    # Hugh Capet [U]).
    "FRA": ["etampes", "dreux", "montreuil"],
}
LOCATION_GRANTS.update(_IBERIA_GRANTS)
LOCATION_GRANTS.update(_BYZ_GRANTS)
LOCATION_GRANTS.update(_BRITISH_GRANTS)
LOCATION_GRANTS.update(_ITALY_GRANTS)
LOCATION_GRANTS.update(_EMPIRE_GRANTS)
# Germany II EXTENDS rather than assigns: FLA is a recipient in two
# slices at once (roman_flanders from FRA through _FRANCE_RULES, the
# seven Artois locations from ARS here), and a plain `update` would drop
# whichever list landed first with no error anywhere. The France
# resolver below extends for the same reason.
for _t, _locs in sorted(_GERMANY_GRANTS.items()):
    LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + _locs
# Italy North extends for the same reason: AQU and SAV are recipients
# in the Empire slice too (gorizia-group and trevoux), and a plain
# update would silently drop whichever list landed first.
for _t, _locs in sorted(_NITALY_GRANTS.items()):
    LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + _locs
# LOCATION_GRANTS["BYZ"] itself is resolved at build time inside
# build_countries — see _byz_target().

# tag -> (expected old capital, new capital). Asserted against the old
# value so a vanilla patch moving it fails loudly.
CAPITAL_FIXES = {
    "PAP": ("avignon", "rome"),   # the 1337 block is the Avignon papacy; cardinals follow the capital
    "CAS": ("valladolid", "burgos"),  # Valladolid founded/repopulated c. 1072 — barely exists at 1066
    "ARA": ("barcelona", "jaca"),     # the kingdom of Jaca; Barcelona is CAT's
    "POR": ("lisbon", "guimaraes"),   # the comital seat; lisbon is BDJ's and POR is landless
    "SER": ("prizren", "trgoviste_SER"),  # Prizren goes to BYZ; Trgoviste IS Ras, the zupan's seat
    "MTH": ("athlone", "mullingar"),  # athlone is HYM's; the Clann Cholmain seat is Lough Ennell (British slice)
    "MCM": ("killarney", "bunratty"), # vanilla's own o_brien_dynasty comment: home = bunratty #Killaloe (04_dynasties.txt:485)
    "SIC": ("palermo", "messina"),    # Roger holds Palermo only from 1072; Messina is the 1061 beachhead (Italy slice)
    "OGK": ("aachen", "goslar"),      # Henry III's Kaiserpfalz, Heinrich IV's birthplace [U]; culture matches OGK's registry (HRE slice)
    "PAL": ("heidelberg", "kaiserslautern"), # Heidelberg is first attested 1196; Kaiserslautern is a Salian palace PAL already holds (Germany II)
    # Africa (2026-08-02): BBK's kayes goes to GHA in the khaaso sweep —
    # diawara is Bambuk's own name-place, BBK-held. ETH's ankober goes
    # to SOA in the argobba sweep (the package's E.4 MISSED this one —
    # caught at implementation); kubar is al-Yaqubi's name for the
    # Ethiopian capital [U], amhara_province, ETH keeps it — and it is
    # the package's own B.2 prescription anyway.
    "BBK": ("kayes", "diawara"),
    "ETH": ("ankober", "kubar"),
    # AJU survives INLAND (decision 5b) but its vanilla seat merca is a
    # Benadir coast town and goes to MDI — caught by this guard at
    # implementation. kelafo: the Shebelle valley, the river the Ajuran
    # tradition is about [U]; a mechanical seat on the tag's own
    # holdings, not an attested capital.
    "AJU": ("merca", "kelafo"),
    # The audit-D1 nine (AUDIT-2026-07-31): capitals stripped by earlier
    # sweeps/grants with no repoint — six arrived through area/province
    # sweeps that never name locations, which is why nobody reviewed them.
    # Mechanical seats on the tag's own remaining holdings; the Arabia and
    # Central Asia packages refine the Mongol-era relics properly later.
    "ETA": ("etampes", "gien"),           # etampes went to FRA (France slice); gien is ETA's only holding
    "AAL": ("qutayfah", "dumat_al_jandal"),  # qutayfah went to FAT; Dumat al-Jandal is the Jawf's historical oasis seat
    "FDL": ("tadmur", "zubala"),          # tadmur went to HLB; Zubala is the Darb Zubaydah station among FDL's wells
    "FRI": ("groningen", "leeuwarden"),   # groningen went to UTR (Germany II); Leeuwarden is Frisia's chief town
    "JLM": ("van", "baskale"),            # van went to BYZ; Baskale is the Hakkari highland seat JLM keeps (JLM = Julamerk)
    "ORM": ("hormuz", "qalhat"),          # hormuz went to SEL (fars sweep); Qalhat is the Hormuzi realm's attested twin city on the Oman shore
    "HLG": ("basra", "kazimah"),          # basra went to SEL (iraq sweep); kazimah is HLG's only holding
    "QUN": ("kabul", "kulob"),            # kabul went to GHZ; Kulob is the Khuttal region's town among QUN's holdings (QUN = Qara'unas)
    "SLD": ("balkh", "termez"),           # balkh went to SEL (khorasan sweep); Termez is Tokharistan's city among SLD's holdings (SLD = Suldus)
    # Rus Tier 1: HAL keeps its 10 Podolian locations but lviv goes to
    # KIE with red_ruthenia_area — the review caught this (the package
    # had not); Kamianets is the Ponizzia's fortress seat [U].
    "HAL": ("lviv", "kamianets_podilskyi"),
    # Rus Tier 2: CUM's lower_don sweep takes sarai_al_jadid (New
    # Sarai sits in beljamen_province, the Volga-Don portage — the
    # guard caught it). GLH keeps the Volga corridor; the delta town
    # is the honest stand-in seat (1066's Saqsin [U]).
    "GLH": ("sarai_al_jadid", "astrakhan"),
    # China-East: Khanbaliq is Kublai's 1267 foundation; the Northern
    # Song capital is Kaifeng (Bianjing), which CHI already holds.
    "CHI": ("dadu", "kaifeng"),
    # India Tier 1: three forced (sweeps take the old seats) — all
    # three historical upgrades — plus two riding the approved renames.
    "HSL": ("tiruvannamalai", "dvarasamudra"),  # the hoysala_dynasty's own home
    "DBD": ("kurunegala", "tissamaharama"),     # Mahagama, Ruhuna's historic seat
    "GHL": ("danduka", "sihor"),                # the Gohil seat before Bhavnagar
    "DRW": ("taranagar", "sambhar"),            # Shakambhari — the dynasty's namesake
    "GWA": ("gwalior", "delhi"),                # the Tomaras of Dhillika (decision 2)
    # SEA (2026-08-02): Launggyet is a 1237 foundation [U]; weithali
    # (Wethali/Vesali) is the Arakanese seat to c. 1018 and the only
    # pre-Lemro capital that exists as a location — the 1066 Pyinsa has
    # none. SUN's kawali stays put (decision 11: the 1066 Sunda seat is
    # genuinely unrecorded, unlike this one).
    "ARK": ("launggyet", "weithali"),
    # The Americas (2026-08-02): Mayapan is founded c. 1180-1220 [D]
    # and its league is 1220-1441; at 1066 the Yucatan hegemon is
    # Chichen Itza, which COC already holds. One token; the tag's
    # "Cocom" NAME stays (a rename would shadow a vanilla key from our
    # loc file — unattested, refused in decision 3).
    "COC": ("mayapan", "chichen_itza"),
}

# tag -> [(expected old line, new line)] — single-line field surgery inside
# an EXISTING country block, asserted against the exact old text so a
# vanilla patch changing the field fails loudly (the CAPITAL_FIXES shape,
# generalized). Every value verified against the built file and vanilla:
# rank_county is the "County of X" fallback (country_ranks.txt:2553),
# aragonese_dialect exists (languages/00_iberia.txt:131),
# catholic_monarchy_not_present is the landless include LON/GLC/CAT/GRA use.
FIELD_FIXES = {
    # NOV: the 1136 veche republic un-anachronized (the Rus package's
    # second LIVE defect, user-approved 2026-08-01). In 1066 Novgorod is
    # a Rurikid principality under Mstislav — the veche deposes its
    # first prince only in 1136. type -> monarchy; veche_selection is
    # republic-only (government_types/00_default.txt:46) ->
    # partition_inheritance, the Rurikid rota itself, legal for monarchy
    # (:7) — user decision 13; both republic-only reforms removed
    # (country_specific.txt:383 / republic.txt:30 gate them to
    # government = republic); and the republic-GATED law line removed
    # (00_republic.txt:4-8 — the package missed this fourth item: a
    # monarchy carrying it would ship a dead law). The tag-gated
    # pyatina/Ivan's-Hundred/tysiatskii/ryad privileges stay — all four
    # verified tag- or culture-gated, not government-gated. NOV's inline
    # block already carries marriage/heir laws, the thirteen sliders and
    # parliament_type, so nothing needs restating.
    "NOV": [("\t\t\ttype = republic", "\t\t\ttype = monarchy"),
            ("heir_selection = veche_selection",
             "heir_selection = partition_inheritance"),
            ("\n\t\t\t\tveche_republic", ""),
            ("\n\t\t\t\tmerchant_republic", ""),
            ("\n\t\t\treforms = {\n\t\t\t}", ""),
            ("\n\t\t\t\trepublican_foundation_law = political_dynasties_policy",
             "")],
    # --- Rus Tier 1 surgeries (package §F, re-verified; user-approved
    # 2026-08-01). KIE and POK wear the GEDIMINIDS — the Lithuanian
    # house of the 1300s (the ZTA wrong-house shape); KIE carries a
    # Cossack privilege four centuries early; KIE rank_duchy ->
    # rank_kingdom reaches country_ranks.txt:1136
    # rank_duchy_grand_principality_slavic -> "Grand Principality of
    # Kyiv"/"Grand Prince" ($PREFIX$ composition is a LAUNCH PROBE).
    # heir_selection = partition_inheritance is the Rurikid rota (user
    # decision 13), injected INSIDE the government block so it lands
    # AFTER the include and wins the merge (later-key-wins, the ABS
    # probe); KIE's injection also carries kyivan_seniority_reform —
    # the KIE->NOV tributary's visible gate, khutba pattern #5. The
    # ruler = random anchor is safe: FIELD_FIXES runs before the
    # HISTORICAL_RULERS seating and every block has exactly one.
    "KIE": [("dynasty = gediminid_dynasty", "dynasty = rurikovich_dynasty"),
            ("country_rank = rank_duchy", "country_rank = rank_kingdom"),
            ("\n\t\t\t\tcossack_identity", ""),
            ("\t\t\truler = random",
             "\t\t\their_selection = partition_inheritance\n"
             "\t\t\treforms = {\n"
             "\t\t\t\tkyivan_seniority_reform\n"
             "\t\t\t}\n"
             "\t\t\truler = random")],
    "CHR": [("heir_selection = cognatic_primogeniture",
             "heir_selection = partition_inheritance")],
    # POK: the Lithuanian government of the 1300s swapped for KIE's own
    # Ruthenian principality. Diff-measured: the ONE cross-cutting
    # field lithuanian_monarchy supplies that the Ruthenian template
    # does not is court_language = belarusian_dialect — restated, and
    # historically right for Polotsk anyway; its two Lithuanian
    # privileges (land_of_commerce, peasants_free_peasantry) and the
    # all_cultures levy line are deliberately not carried.
    "POK": [("dynasty = gediminid_dynasty", "dynasty = rurikovich_dynasty"),
            ('include = "lithuanian_monarchy"',
             'include = "ruthenian_principality_no_coast"\n'
             "\t\tcourt_language = belarusian_dialect"),
            ("\t\t\truler = random",
             "\t\t\their_selection = partition_inheritance\n"
             "\t\t\truler = random")],
    # SXM revived (Baltic slice): vanilla ships it as a catholic-
    # monarchy revolter shell — a package gap caught at implementation
    # (the KLB precedent). Landing it unchanged would seat a catholic
    # Duke over the LAST pagan corner of Europe (Samogitia converts
    # 1413); its registry identity is already samogitian + romuva.
    # Reskinned to its six new siblings' tribal shape; tech 3 -> 2
    # aligns it with them (package decision 8). The explicit
    # type/heir lines override the include's — later-key-wins — so
    # both must move with the template.
    "SXM": [('include = "eastern_european_catholic_monarchy_not_present"',
             'include = "eurasian_tribe"'),
            ("starting_technology_level = 3",
             "starting_technology_level = 2"),
            ("type = monarchy", "type = tribe"),
            ("heir_selection = cognatic_primogeniture",
             "heir_selection = tribal_oldest_male")],
    # ---- Africa (2026-08-02, docs/AFRICA-PACKAGE.md §B.2) ----
    # MAL down to the Manden chiefdom of Kangaba: the tag-gated name
    # branch (country_name_construction.txt:79-89, map string = FULL
    # string, "Mali Empire") requires kingdom-or-empire — rank_duchy
    # escapes it structurally and the map reads bare "Mali". Sundiata's
    # 1235 constitution goes with it: the reform, the Gbara assembly
    # law and the hunter-levy law; Mansa Musa's 2500 gold likewise.
    # MINIMAL surgery, deliberately narrower than the package's full
    # apparatus-drop: the remaining inline laws/sliders/privileges are
    # accepted 1337 tuning, recorded here, not silently.
    "MAL": [("country_rank = rank_empire", "country_rank = rank_duchy"),
            ("\t\t\treforms = {\n\t\t\t\tmanden_kurufa_reform\n\t\t\t}\n",
             ""),
            ("\t\t\t\tdistribution_of_power_law = dop_law_gbara\n", ""),
            ("\t\t\t\tmedieval_levy_law = ton_ta_jon_ta_ni_woro\n", ""),
            ("\t\tcurrency_data = {\n"
             "\t\t\tgold = 2500\t#Mansa Mūsā's wealth\n"
             "\t\t\tprestige = 50\n\t\t}\n", "")],
    # GHA promoted to the hegemon: rank_kingdom ("Sultanate of Ghana",
    # the muslim kingdom branch), and al-Bakri's own succession law —
    # the king is succeeded by his sister's son [U];
    # matrilineal_non_exclusive is attested in-file (MAK and ALO).
    "GHA": [("heir_selection = cognatic_primogeniture",
             "heir_selection = matrilineal_non_exclusive"),
            ("\t\tcapital = koumbi_saleh",
             "\t\tcountry_rank = rank_kingdom\n\t\tcapital = koumbi_saleh")],
    # PLB promoted to the mandala's centre (SEA decisions 1-2): vanilla
    # declares no rank on it, and rank_kingdom + malay_culture reaches
    # rank_kingdom_indian (country_ranks.txt:1072, muslim branch passes
    # first-match at :1060 — PLB is mahayana) -> "Mahārājya of
    # Palembang" under a "Mahārājā", Srivijaya's own style shipped by
    # Paradox. The GHA/koumbi_saleh insertion shape.
    "PLB": [("\t\tcapital = palembang",
             "\t\tcountry_rank = rank_kingdom\n\t\tcapital = palembang")],
    # ---- Perm/Vyatka (2026-08-02, docs/PERM-VYATKA-PACKAGE.md §B.1,
    # decisions 2a/6 — main session under the user's direct-implement
    # authorization). Great Perm de-Russified: vanilla's own registry
    # already calls it komi + komi_paganism (russia.txt:309); only the
    # start block dresses it as a Rurikid feudal principality. The SXM
    # shape, one rung colder — the Komi/Udmurt world is 1066-real, the
    # 15th-century constitution is not; 64/64 locations shamanism.
    # limited_russian_principality declares no type= at all, so the
    # explicit type/heir lines move with the include (later-key-wins).
    # Tech stays 3 (decision 6 — a settled forest polity, no
    # measurement justifies moving a live balance value).
    "PRM": [('include = "limited_russian_principality"',
             'include = "eurasian_tribe"'),
            ("\t\t\ttype = monarchy", "\t\t\ttype = tribe"),
            ("heir_selection = cognatic_primogeniture",
             "heir_selection = tribal_oldest_male"),
            ("\t\tdynasty = rurikovich_dynasty\n", "")],
    # KBO back to the Duguwa's Kanem: Hummay is c. 1075 [D] — the
    # Sayfawa house and his amendments are nine years in the future.
    # rank_kingdom renders "Kingdom of Kanem" under a "Mai"
    # (rank_kingdom_kanem beats muslim at kingdom rank, measured).
    "KBO": [("country_rank = rank_empire", "country_rank = rank_kingdom"),
            ("\t\t\treforms = {\n\t\t\t\tbanu_hummay_amendments\n\t\t\t}\n",
             ""),
            ("\t\tdynasty = sayfawa_dynasty\n", "")],
    # MAK Christianised — the single most important correction in the
    # theater (registry flip rides in the horn_of_africa.txt override):
    # the Islamic kit goes, the Coptic liturgy arrives. Dongola falls
    # in 1317, not 1066.
    "MAK": [('include = "subsaharan_muslim_monarchy_no_coast"',
             'include = "subsaharan_monarchy_no_coast"'),
            ("\t\t\tlaws = {\n\t\t\t\tsharia_law = shafii_policy\n\t\t\t}\n",
             ""),
            ("\t\treligious_school = shafii_school\n", ""),
            ("\t\tgovernment = { mysticism_vs_jurisprudence = 20 }\n", ""),
            ("\t\tcapital = dongola",
             "\t\tliturgical_language = coptic_language\n\t\tcapital = dongola")],
    # ETH de-Solomonised (the restoration is 1270) and sized to the
    # northern highlands; court_language = ethiopic_language is what
    # can make rank_kingdom_ethiopia's "Negus" fire — an OWED in-game
    # check, harmless if the branch needs more (capital -> kubar rides
    # CAPITAL_FIXES).
    "ETH": [("country_rank = rank_empire", "country_rank = rank_kingdom"),
            ("\t\tdynasty = solomonid_dynasty\n", ""),
            ("\t\tliturgical_language = geez_language\n",
             "\t\tliturgical_language = geez_language\n"
             "\t\tcourt_language = ethiopic_language\n")],
    # ZAN down to the Shirazi town: the Mahdali sultanate (1277+) goes —
    # both its reforms and its coinage-stability windfall. rank_duchy,
    # NOT county: rank_county_muslim does not exist (measured, zero
    # hits), so county would render "County of Kilwa" under a "Count".
    # court_language = persian_language stays — the Shirazi claim is
    # the town's own founding tradition [D].
    "ZAN": [("country_rank = rank_kingdom", "country_rank = rank_duchy"),
            ("\t\t\treforms = {\n\t\t\t\tkilwan_trade_communities\n"
             "\t\t\t\tcontrol_of_the_mahdali_coinage_reform\n\t\t\t}\n",
             ""),
            ("\t\tcurrency_data = {\n"
             "\t\t\tstability = 40 #Smooth and voluntary transition of power from previous Sultan\n"
             "\t\t\tprestige = 25\n"
             "\t\t\tgovernment_power = 90 #Smooth and voluntary transition of power from previous Sultan\n"
             "\t\t}\n", "")],
    # The Hausa seven de-Islamised (registry flip to bori_religion in
    # the west_africa.txt override; Islam reaches the Hausa courts in
    # the 14th century [U] and vanilla's own map data already says so —
    # all 41 hausa locations are bori_religion in location_templates).
    # Same four cuts per tag, copied from each built block.
    "ZAM": [('include = "subsaharan_muslim_monarchy_no_coast"',
             'include = "subsaharan_monarchy_no_coast"'),
            ("\t\t\tlaws = {\n\t\t\t\tsharia_law = maliki_policy\n\t\t\t}\n", ""),
            ("\t\treligious_school = maliki_school\n", ""),
            ("\t\tgovernment = { mysticism_vs_jurisprudence = -5 }\n", "")],
    "KAN": [('include = "subsaharan_muslim_monarchy_no_coast"',
             'include = "subsaharan_monarchy_no_coast"'),
            ("\t\t\tlaws = {\n\t\t\t\tsharia_law = maliki_policy\n\t\t\t}\n", ""),
            ("\t\treligious_school = maliki_school\n", ""),
            ("\t\tgovernment = { mysticism_vs_jurisprudence = -5 }\n", "")],
    "KTS": [('include = "subsaharan_muslim_monarchy_no_coast"',
             'include = "subsaharan_monarchy_no_coast"'),
            ("\t\t\tlaws = {\n\t\t\t\tsharia_law = maliki_policy\n\t\t\t}\n", ""),
            ("\t\treligious_school = maliki_school\n", ""),
            ("\t\tgovernment = { mysticism_vs_jurisprudence = -5 }\n", "")],
    "GOB": [('include = "subsaharan_muslim_monarchy_no_coast"',
             'include = "subsaharan_monarchy_no_coast"'),
            ("\t\t\tlaws = {\n\t\t\t\tsharia_law = maliki_policy\n\t\t\t}\n", ""),
            ("\t\treligious_school = maliki_school\n", ""),
            ("\t\tgovernment = { mysticism_vs_jurisprudence = -5 }\n", "")],
    "RAN": [('include = "subsaharan_muslim_monarchy_no_coast"',
             'include = "subsaharan_monarchy_no_coast"'),
            ("\t\t\tlaws = {\n\t\t\t\tsharia_law = maliki_policy\n\t\t\t}\n", ""),
            ("\t\treligious_school = maliki_school\n", ""),
            ("\t\tgovernment = { mysticism_vs_jurisprudence = -5 }\n", "")],
    "DAA": [('include = "subsaharan_muslim_monarchy_no_coast"',
             'include = "subsaharan_monarchy_no_coast"'),
            ("\t\t\tlaws = {\n\t\t\t\tsharia_law = maliki_policy\n\t\t\t}\n", ""),
            ("\t\treligious_school = maliki_school\n", ""),
            ("\t\tgovernment = { mysticism_vs_jurisprudence = -5 }\n", "")],
    "ZZZ": [('include = "subsaharan_muslim_monarchy_no_coast"',
             'include = "subsaharan_monarchy_no_coast"'),
            ("\t\t\tlaws = {\n\t\t\t\tsharia_law = maliki_policy\n\t\t\t}\n", ""),
            ("\t\treligious_school = maliki_school\n", ""),
            ("\t\tgovernment = { mysticism_vs_jurisprudence = -5 }\n", "")],
    "CAT": [("country_rank = rank_duchy", "country_rank = rank_county")],
    "ARA": [("court_language = catalan_dialect", "court_language = aragonese_dialect"),
            ("accepted_cultures = { aragonese }", "accepted_cultures = { catalan }")],
    "POR": [('include = "iberian_monarchy"', 'include = "catholic_monarchy_not_present"')],
    # Rascia was a zupa, not a kingdom until 1217; ZTA's block-level house
    # is the 14th-century Balsici — Mihailo is a Vojislavljevic.
    "SER": [("country_rank = rank_kingdom", "country_rank = rank_duchy")],
    "ZTA": [("dynasty = balsic_dynasty", "dynasty = vojislavljevic_dynasty")],
    # Kerman's block carries the 14th-century Nikruzi house; Qavurt is a
    # Seljukid. The include swap (Arabia slice): Oman's Batinah makes
    # Kerman a maritime power — and KRM already held minab/sirik/senderk
    # on the Strait under the _no_coast include, so this is arguably a
    # pre-Arabia bug fix too (the government.cpp:3662 class in reverse).
    # KRM's block states heir_selection explicitly, so the coastal
    # variant's own line is a harmless duplicate (vanilla ORM does the
    # same).
    "KRM": [("dynasty = nikruzi_dynasty", "dynasty = seljukids_dynasty"),
            ('include = "muslim_monarchy_no_abrahamic_dhimmi_no_coast"',
             'include = "muslim_monarchy_no_abrahamic_dhimmi"')],
    # Al-Sulayhi moved his capital to Sana'a in 1063; Zabid (taken 1060)
    # is the Najahid seat, not his. sana_yemen is already YEM's own and
    # sulayhid_dynasty's home.
    "YEM": [("capital = zabid", "capital = sana_yemen")],
    # The Husaynid sharifs of Medina were Twelvers [D — the Zaydi/Imami
    # line among 11th-c. Hejazi Alids is not sharp; user decision 6].
    # MEC's zaidi_school is CORRECT and stays — the Meccan sharifs were
    # Zaydi until the Ayyubids.
    "MDA": [("sharia_law = zaidi_policy", "sharia_law = jafari_policy"),
            ("religious_school = zaidi_school",
             "religious_school = imamiya_school")],
    # JAP (India/China review): the shogunate reform is gated on BEING
    # LEADER of the japanese_shogunate IO (country_specific.txt:2067 +
    # locked :2069-2071) — an IO created 1192 that our strip removes,
    # so the reform is invalid at every start (the JAP half of the old
    # "~25 invalid reform" class; decoder entry 2026-08-01).
    # japanese_imperial_family (:1952) is the 1066 truth; its own
    # locked block (:1968-1976) demands a yamato_dynasty ruler — hence
    # the mandatory Go-Reizei seat in HISTORICAL_RULERS.
    # The first launch (2026-08-01) showed Go-Reizei ruling an
    # "Ashikaga Empire": vanilla's block carries country_name/flag
    # overrides to "ASK" — the 1337 shogunal dynasty branding, the same
    # class as CHI's "YUA" pair. Both removed; the tag falls back to
    # its own JAP key ("Japan") and its own arms. The inner
    # `flag = "supports_northern_court"` VARIABLE is a different thing
    # and stays.
    "JAP": [("\t\t\t\tshogunate", "\t\t\t\tjapanese_imperial_family"),
            ('\n\t\tcountry_name = "ASK"', ""),
            ('\n\t\tflag = "ASK"', "")],
    # CHI: the Yuan becomes the Northern Song (India/China review D2,
    # user-approved 2026-08-01). flag/country_name are DYNASTY branding
    # on the CHI state tag (the proven JAP/ASK class, in reverse:
    # vanilla itself ships CSO "Song" identity + loc + map_CSO for the
    # Crisis events). Kublai's legacy reform and Bayan's anti-Han law
    # go; the sinicization slider flips to the Song court's side
    # (positive = sinicized — asia templates ship +10; the magnitude
    # 50 is ours, flagged).
    "CHI": [('flag = "YUA"', 'flag = "CSO"'),
            ('country_name = "YUA"', 'country_name = "CSO"'),
            ("\n\t\t\t\tlegacy_of_kublai_khan",
             # Kublai carried cultures_capacity = 3 and a
             # Mongol-culture allow (dead on the Song anyway);
             # replacements: three_departments_system (the
             # Song-defining institution, gate passes on the
             # Chinese court + MK leadership) and the civil-
             # service capacity reform (grand-test fix).
             "\n\t\t\t\tsong_civil_service_reform"
             "\n\t\t\t\tthree_departments_system"),
            ("\n\t\t\t\tstatus_of_the_han_law = limit_the_han_powers", ""),
            # Yuan cosmopolitan tolerance the Song court never
            # kept: the eleven steppe/Inner-Asian entries go
            # (historical regardless of the capacity math).
            ("\n\t\t\tsibe_culture", ""),
            ("\n\t\t\tjurchen_culture", ""),
            ("\n\t\t\tdaur_culture", ""),
            ("\n\t\t\ttumed_culture", ""),
            ("\n\t\t\tkharchin_culture", ""),
            ("\n\t\t\toirat_culture", ""),
            ("\n\t\t\ttuvan_culture", ""),
            ("\n\t\t\tuyghur_culture", ""),
            ("\n\t\t\tyugur_culture", ""),
            ("\n\t\t\tmonguor_culture", ""),
            ("\n\t\t\tamdowa_culture", ""),
            ("sinicized_vs_unsinicized = -50 # Bayan's policies",
             "sinicized_vs_unsinicized = 50 # the Song court [magnitude ours; positive = sinicized, asia templates +10]")],
    # France demesne slice: the three landless-to-landed tags swap the
    # _not_present include for the landed variant (the POR entry in
    # reverse). The catholic no_coast variant KEEPS heir_selection
    # (diff-measured — unlike the muslim family), nothing restated.
    # TOU is coastal (montpellier/agde); BER and VLS are inland
    # (amienois resolves to amiens/breteuil/corbie — no coast).
    "TOU": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_monarchy"')],
    "BER": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_monarchy_no_coast"')],
    "VLS": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_monarchy_no_coast"')],
    # FRA: capetian_homage_reform joins the two vanilla reforms in
    # place (10_countries.txt:15156-15157) — injection, not
    # replacement; the tributary ring's visible gate needs it.
    "FRA": [("\t\t\t\tancient_french_taxation\n",
             "\t\t\t\tancient_french_taxation\n"
             "\t\t\t\tcapetian_homage_reform\n")],
    # --- The British slice's swaps. The Welsh trap, measured:
    # catholic_monarchy_welsh_releasable's line 1 is a NESTED
    # `include = catholic_monarchy_not_present` and line 2 is the
    # tags' ONLY discovery source (`expl_western_europe`), with
    # `country_rank = rank_duchy` at line 30 — so the landed swap must
    # RESTATE both or the kingdom starts blind and rankless.
    "GDD": [('include = "catholic_monarchy_welsh_releasable"',
             'include = "catholic_monarchy"\n'
             '\t\tinclude = "expl_western_europe"\n'
             '\t\tcountry_rank = rank_duchy')],
    "PWS": [('include = "catholic_monarchy_welsh_releasable"',
             'include = "catholic_monarchy_no_coast"\n'
             '\t\tinclude = "expl_western_europe"\n'
             '\t\tcountry_rank = rank_duchy')],
    "DHB": [('include = "catholic_monarchy_welsh_releasable"',
             'include = "catholic_monarchy"\n'
             '\t\tinclude = "expl_western_europe"\n'
             '\t\tcountry_rank = rank_duchy')],
    "MWG": [('include = "catholic_monarchy_welsh_releasable"',
             'include = "catholic_monarchy"\n'
             '\t\tinclude = "expl_western_europe"\n'
             '\t\tcountry_rank = rank_duchy')],
    "GWT": [('include = "catholic_monarchy_welsh_releasable"',
             'include = "catholic_monarchy"\n'
             '\t\tinclude = "expl_western_europe"\n'
             '\t\tcountry_rank = rank_duchy')],
    # MTH and GLY land: the _not_present -> landed swap (their
    # separate expl lines survive untouched).
    "MTH": [('include = "gaelic_tribe_not_present"',
             'include = "gaelic_tribe"')],
    "GLY": [('include = "gaelic_tribe_not_present"',
             'include = "gaelic_tribe"')],
    # The four big landless-goers swap to _not_present (the POR
    # precedent; the small marchers/earldoms keep their includes and
    # join the accepted landless-trim class like the beyliks).
    "WLS": [('include = "catholic_monarchy_english_lordship"',
             'include = "catholic_monarchy_english_lordship_not_present"')],
    "PLE": [('include = "catholic_monarchy_english_lordship"',
             'include = "catholic_monarchy_english_lordship_not_present"')],
    "MNN": [('include = "catholic_monarchy_english_lordship"',
             'include = "catholic_monarchy_english_lordship_not_present"')],
    "SBL": [('include = "catholic_monarchy"',
             'include = "catholic_monarchy_not_present"')],
    # Moray: the block's norman_dialect is the 1312 Randolph earldom;
    # the Scottish-earldom template's own value for a Gaelic house.
    "MOY": [("court_language = norman_dialect",
             "court_language = scottish_gaelic_dialect")],
    # The Isles become the Kingdom of the Isles (Sudreyjar over Mann +
    # the Hebrides; vanilla already ranks Mann itself a kingdom). LOI
    # has no rank line of its own — anchored on its capital line.
    "LOI": [("capital = islay",
             "country_rank = rank_kingdom\n\t\tcapital = islay")],
    # --- Southern Italy (2026-07-29). SIC becomes Roger's COUNTY:
    # rank_kingdom is 1130 (renders "Count Roger" via the generic
    # county fallback — the CAT precedent), catalan is the 1282
    # Aragonese court. NAP and SAO go landless (the POR swap). PAP's
    # government block carries NO reforms block — the container is
    # created against the `ruler = random` anchor (field surgery runs
    # BEFORE the historical seating, measured in the report order:
    # "fields corrected" precedes "historical rulers restored"; the
    # exactly-once assert flips this loudly if the order changes).
    "SIC": [("country_rank = rank_kingdom", "country_rank = rank_county"),
            ("court_language = catalan_dialect",
             "court_language = sicilian_dialect")],
    "NAP": [('include = "catholic_monarchy"',
             'include = "catholic_monarchy_not_present"')],
    "SAO": [('include = "catholic_monarchy"',
             'include = "catholic_monarchy_not_present"')],
    "PAP": [("\t\t\truler = random\n",
             "\t\t\treforms = {\n\t\t\t\tpapal_investiture_reform\n"
             "\t\t\t}\n\t\t\truler = random\n")],
    # --- The HRE slice (2026-07-29, crown decision D). OGK lands with
    # the Salian demesne: the landed includes (the catholic no_coast
    # family KEEPS heir_selection; german_principality adds only
    # magdeburg_rights). HAB becomes the Babenberg MARGRAVIATE of
    # Austria (rank branch renders "Margraviate"/"Margrave" — the
    # margraviate reform is setup-assigned by nine vanilla tags);
    # STY joins it as the Carinthian March under the Otakars; CRH
    # stays ducal. SPL lands coastal (the Abruzzo Adriatic strip).
    "OGK": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_monarchy_no_coast"'),
            ('include = "german_principality_not_present"',
             'include = "german_principality"')],
    "HAB": [("dynasty = habsburg_dynasty", "dynasty = babenberg_dynasty"),
            ("country_rank = rank_duchy", "country_rank = rank_county"),
            ("\t\t\truler = random\n",
             "\t\t\treforms = {\n\t\t\t\tmargraviate\n"
             "\t\t\t}\n\t\t\truler = random\n")],
    "STY": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_monarchy_no_coast"'),
            ('include = "german_principality_not_present"',
             'include = "german_principality"'),
            ("country_rank = rank_duchy", "country_rank = rank_county"),
            ("\t\t\truler = random\n",
             "\t\t\treforms = {\n\t\t\t\tmargraviate\n"
             "\t\t\t}\n\t\t\truler = random\n")],
    "CRH": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_monarchy_no_coast"'),
            ('include = "german_principality_not_present"',
             'include = "german_principality"')],
    "SPL": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_monarchy"')],
    # --- Germany II (2026-07-29). Four block-level values that are
    # 1066-wrong on tags this slice seats. Each old string was checked
    # against the CURRENT built block and appears exactly once, which is
    # what the exactly-once assert below enforces.
    # BRU: welfen_dynasty is the 1138+ Welf duchy — in 1066 Brunswick is
    # the Brunonen's, Egbert I's own house.
    "BRU": [("dynasty = welfen_dynasty", "dynasty = brunonen_dynasty")],
    # MEI: the Wettins take Meissen in 1089 — at 1066 the march is
    # Otto of Weimar-Orlamünde's. (wettin_dynasty is not orphaned: Dedi
    # of the Ostmark wears it on SOR, which is where the house IS in
    # 1066.)
    "MEI": [("dynasty = wettin_dynasty", "dynasty = weimar_dynasty")],
    # PAL: the Wittelsbachs get the Palatinate in 1214 — the 1066 Count
    # Palatine of the Rhine is an Ezzone.
    "PAL": [("dynasty = wittelsbach_dynasty", "dynasty = ezzonen_dynasty")],
    # BLL: Godfrey the Bearded is Duke of Lower Lorraine, not a count;
    # rank_duchy renders the ducal branch (the CAT/SIC rank precedent in
    # reverse).
    "BLL": [("country_rank = rank_county", "country_rank = rank_duchy")],
    # --- Italy North (2026-07-29 package, landed 2026-07-30). The
    # twelve communal shells revive as the BISHOPRICS they were in 1066.
    # The include swap alone is NOT enough: each block RESTATES republic/
    # monarchy machinery at block level, and under merge semantics the
    # block value overrides the new template's theocracy — the ABS
    # include-clash class, measured in item 16. So the government lines
    # swap WITH the include: the bishopric family's own values are
    # type = theocracy + heir_selection = bishopric_elective
    # (setup/templates/catholic_bishopric_no_coast.txt:5-6), and the
    # 1337 signoria/podesta reform blocks go entirely. Template diff,
    # measured: the republic templates' laws/privileges are all
    # republic-specific (wanted gone); the bishopric family carries its
    # own full law set plus court_language = church_dialect; both sides
    # ship starting_technology_level = 3 — nothing to restate. CEN's
    # block carries NO government machinery (`ruler = random` alone), so
    # its include swap rides alone. Ranks untouched throughout (the five
    # bishop-counts already carry CNV's rank_county; the rankless six
    # were rankless as vanilla republics too). VIN's scala_dynasty and
    # RAV's polenta_dynasty block lines stay: inert under an elective
    # theocracy, noted for a future tidy pass.
    "BGM": [('include = "catholic_republic_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = podesta_elective",
             "type = theocracy\n\t\t\their_selection = bishopric_elective"),
            ("\t\t\treforms = {\n\t\t\t\tsignoria_reform\n\t\t\t}\n", "")],
    "CRM": [('include = "catholic_republic_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = podesta_elective",
             "type = theocracy\n\t\t\their_selection = bishopric_elective"),
            ("\t\t\treforms = {\n\t\t\t\tsignoria_reform\n\t\t\t}\n", "")],
    "NVA": [('include = "catholic_republic_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = podesta_elective",
             "type = theocracy\n\t\t\their_selection = bishopric_elective"),
            ("\t\t\treforms = {\n\t\t\t\tsignoria_reform\n\t\t\t}\n", "")],
    "VRC": [('include = "catholic_republic_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = podesta_elective",
             "type = theocracy\n\t\t\their_selection = bishopric_elective"),
            ("\t\t\treforms = {\n\t\t\t\tsignoria_reform\n\t\t\t}\n", "")],
    "PCZ": [('include = "catholic_republic_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = podesta_elective",
             "type = theocracy\n\t\t\their_selection = bishopric_elective"),
            ("\t\t\treforms = {\n\t\t\t\tsignoria_reform\n\t\t\t}\n", "")],
    "LDI": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = monarchy\n\t\t\their_selection = cognatic_primogeniture",
             "type = theocracy\n\t\t\their_selection = bishopric_elective")],
    "CHV": [('include = "catholic_monarchy_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = monarchy\n\t\t\their_selection = cognatic_primogeniture",
             "type = theocracy\n\t\t\their_selection = bishopric_elective")],
    "VIN": [('include = "catholic_republic_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = oligarchic_elective",
             "type = theocracy\n\t\t\their_selection = bishopric_elective")],
    "CEN": [('include = "catholic_bishopric_not_present"',
             'include = "catholic_bishopric_no_coast"')],
    "FEL": [('include = "catholic_republic_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = republic_4_year_terms",
             "type = theocracy\n\t\t\their_selection = bishopric_elective")],
    "TRV": [('include = "catholic_republic_not_present"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = podesta_elective",
             "type = theocracy\n\t\t\their_selection = bishopric_elective"),
            ("\t\t\treforms = {\n\t\t\t\tsignoria_reform\n\t\t\t}\n", "")],
    # RAV is COASTAL: catholic_bishopric is AQU's exact include, the
    # family's coastal member (TNT/CNV inland use _no_coast). PAR is
    # inland. Both drop their republic machinery like the rest.
    "RAV": [('include = "catholic_republic"',
             'include = "catholic_bishopric"'),
            ("type = republic\n\t\t\their_selection = signoria_selection",
             "type = theocracy\n\t\t\their_selection = bishopric_elective"),
            ("\t\t\treforms = {\n\t\t\t\tdynastic_signoria_reform\n\t\t\t}\n", "")],
    "PAR": [('include = "catholic_republic_no_coast"',
             'include = "catholic_bishopric_no_coast"'),
            ("type = republic\n\t\t\their_selection = podesta_elective",
             "type = theocracy\n\t\t\their_selection = bishopric_elective"),
            ("\t\t\treforms = {\n\t\t\t\tsignoria_reform\n\t\t\t}\n", "")],
    # VEN cedes control of este: este is PAD's own_core, and with the
    # 1330s Scaliger/Venetian ties gone the town reverts to its owner —
    # Azzo's own seat (package section E).
    "VEN": [("\t\tcontrol = {\n\t\t\teste\n\t\t}\n\n", "")],
    # MFA's block carries the 14th-century Palaiologos house; Otto II is
    # an Aleramici (his own vanilla character says so) — the KRM/ZTA
    # wrong-house precedent, applied on measurement.
    "MFA": [("dynasty = palaiologos_dynasty", "dynasty = aleramici_dynasty")],
}

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

	# --- 1066 Italy -------------------------------------------------------
	# Pope Alexander II — Anselmo da Baggio of Milan, elected 1061.9.30
	# against the antipope Cadalus (the schism is situation material). The
	# character carries his BIRTH name; the papal name arrives through the
	# term's regnal_name, vanilla's own convention (pap_benedetto_xii is
	# name_james/Fournier with regnal_name = name_benedict). Dynasty-less
	# and clergy_estate, per the vanilla papal characters. name_anselm is
	# the North Italian pool's own key (registry:1949). Historically dies
	# 1073.4.21 — Gregory VII and the Investiture Controversy follow.
	pap_anselmo_da_baggio = {
		first_name = { name = name_anselm }
		culture = lombard
		religion = catholic
		estate = clergy_estate
		birth_date = 1010.1.1
		birth = milano
		tag = PAP
	}

	# --- 1066 Sardinia ----------------------------------------------------
	# The judges of Torres and Cagliari, [U] dates throughout. Vanilla's
	# Sardinian name pool is unusually rich (name_barisone:2962,
	# name_torchitorio:17278, with .sardinian_dialect rows); the
	# Lacon-Gunale house that both lines descend from is ours to add.
	tor_barisone_i_lacon_gunale = {
		first_name = { name = name_barisone }
		culture = sardinian
		religion = catholic
		birth_date = 1030.1.1
		birth = sassari
		dynasty = lacon_gunale_dynasty
		tag = TOR
	}

	cag_orzocco_torchitorio_i = {
		first_name = { name = name_torchitorio }
		culture = sardinian
		religion = catholic
		birth_date = 1030.1.1
		birth = cagliari
		dynasty = lacon_gunale_dynasty
		tag = CAG
	}

	# --- 1066 al-Andalus: the thirteen taifa emirs ------------------------
	# All birth dates [U], all safely pre-start, no death dates (the alive
	# law). Name keys: name_muhammad/name_yahya/name_ahmad/name_ali are
	# vanilla (character_names_dynamic, cited in the package); name_joseph
	# IS Yusuf (.arabic_language "Yūsuf", :10200). name_abbad, name_badis
	# and name_abd_al_malik are OUR OWN keys — the invented-name-key probe,
	# patterned on vanilla's name_abd_al_qadir (:41). Culture andalusi for
	# all thirteen: the Berber houses (Zirid, Birzalid) ruled an andalusi
	# country, matching vanilla GRA's own choice.
	sev_abbad_al_mutadid = {
		first_name = { name = name_abbad }
		culture = andalusi
		religion = sunni
		birth_date = 1016.1.1
		birth = sevilla
		dynasty = abbadid_dynasty
		tag = SEV
	}

	bdj_muhammad_al_muzaffar = {
		first_name = { name = name_muhammad }
		culture = andalusi
		religion = sunni
		birth_date = 1010.1.1
		birth = badajoz
		dynasty = aftasid_dynasty
		tag = BDJ
	}

	tol_yahya_al_mamun = {
		first_name = { name = name_yahya }
		culture = andalusi
		religion = sunni
		birth_date = 1000.1.1
		birth = toledo
		dynasty = dhunnunid_dynasty
		tag = TOL
	}

	crd_abd_al_malik_ibn_jahwar = {
		first_name = { name = name_abd_al_malik }
		culture = andalusi
		religion = sunni
		birth_date = 1030.1.1
		birth = cordoba
		dynasty = jahwarid_dynasty
		tag = CRD
	}

	grz_badis_ibn_habbus = {
		first_name = { name = name_badis }
		culture = andalusi
		religion = sunni
		birth_date = 1002.1.1
		birth = granada
		dynasty = zirid_dynasty
		tag = GRZ
	}

	alm_muhammad_al_mutasim = {
		first_name = { name = name_muhammad }
		culture = andalusi
		religion = sunni
		birth_date = 1037.1.1
		birth = almeria
		dynasty = sumadihid_dynasty
		tag = ALM
	}

	mru_muhammad_ibn_tahir = {
		first_name = { name = name_muhammad }
		culture = andalusi
		religion = sunni
		birth_date = 1000.1.1
		birth = murcia
		dynasty = tahirid_murcia_dynasty
		tag = MRU
	}

	dya_ali_iqbal_al_dawla = {
		first_name = { name = name_ali }
		culture = andalusi
		religion = sunni
		birth_date = 1010.1.1
		birth = denia
		dynasty = mujahidid_dynasty
		tag = DYA
	}

	zgz_ahmad_al_muqtadir = {
		first_name = { name = name_ahmad }
		culture = andalusi
		religion = sunni
		birth_date = 1020.1.1
		birth = zaragoza
		dynasty = hudid_dynasty
		tag = ZGZ
	}

	lrd_yusuf_al_muzaffar = {
		first_name = { name = name_joseph }
		culture = andalusi
		religion = sunni
		birth_date = 1022.1.1
		birth = zaragoza
		dynasty = hudid_dynasty
		tag = LRD
	}

	abr_abd_al_malik_ibn_razin = {
		first_name = { name = name_abd_al_malik }
		culture = andalusi
		religion = sunni
		birth_date = 1025.1.1
		birth = albarracin
		dynasty = razinid_dynasty
		tag = ABR
	}

	alp_muhammad_yumn_al_dawla = {
		first_name = { name = name_muhammad }
		culture = andalusi
		religion = sunni
		birth_date = 1020.1.1
		birth = chelva
		dynasty = qasimid_dynasty
		tag = ALP
	}

	qrm_muhammad_al_birzali = {
		first_name = { name = name_muhammad }
		culture = andalusi
		religion = sunni
		birth_date = 1030.1.1
		birth = carmona
		dynasty = birzalid_dynasty
		tag = QRM
	}

	# --- 1066 Pyrenean counts -------------------------------------------
	# Birth dates [U]. Name keys: name_ermengaud renders "Ermengol" via
	# .catalan_dialect (:6552); name_raymond.name_wilfred is the attested
	# composite form; name_pontius renders "Ponç" (:14296); name_bernard's
	# "Bernat" sits on the occitan row marked "# Catalan & Occitan" —
	# eyeball in game. name_guislabert is OUR key (the proven
	# invented-name-key mechanism, fourth use).
	urg_ermengol_iv_bellonid = {
		first_name = { name = name_ermengaud }
		culture = catalan
		religion = catholic
		birth_date = 1035.1.1
		birth = seu_durgell
		dynasty = bellonid_dynasty
		tag = URG
	}

	bsl_bernat_ii_bellonid = {
		first_name = { name = name_bernard }
		culture = catalan
		religion = catholic
		birth_date = 1035.1.1
		birth = besalu
		dynasty = bellonid_dynasty
		tag = BSL
	}

	cdy_ramon_guifre_bellonid = {
		first_name = { name = name_raymond.name_wilfred }
		culture = catalan
		religion = catholic
		birth_date = 1010.1.1
		birth = puigcerda
		dynasty = bellonid_dynasty
		tag = CDY
	}

	epu_ponc_i_empuries = {
		first_name = { name = name_pontius }
		culture = catalan
		religion = catholic
		birth_date = 1010.1.1
		birth = castellon_ampurias
		dynasty = empuries_dynasty
		tag = EPU
	}

	plj_ramon_iv_pallars = {
		first_name = { name = name_raymond }
		culture = catalan
		religion = catholic
		birth_date = 1025.1.1
		birth = talarn
		dynasty = pallars_dynasty
		tag = PLJ
	}

	rsl_guislabert_ii_empuries = {
		first_name = { name = name_guislabert }
		culture = catalan
		religion = catholic
		birth_date = 1035.1.1
		birth = perpignan
		dynasty = empuries_dynasty
		tag = RSL
	}

	# --- 1066 Duklja ------------------------------------------------------
	# name_michael is IN the serbo_croatian pool (00_balkans.txt) and
	# renders in the culture's own form — do not invent name_mihailo.
	# Birth year [U].
	zta_mihailo_vojislavljevic = {
		first_name = { name = name_michael }
		culture = serbian
		religion = orthodox
		birth_date = 1015.1.1
		birth = bar_cg
		dynasty = vojislavljevic_dynasty
		tag = ZTA
	}

	# --- 1066 India Tier 1 ------------------------------------------------
	# Naming routes chosen by MEASURING the pools: tamil_language has ONE
	# name_* key in the whole game, so the Chola is the package's single
	# invented literal (Virarajendra, loc row ours); Someshvara /
	# Vigrahapala / Karna / Kirtivarman / Jayasimha / Vijayabahu are all
	# vanilla rows. Cultures/religions from each tag's registry; PAA's
	# mahayana over hindu pops is the al-Andalus law, deliberate.
	coz_virarajendra_chola = {
		first_name = { name = Virarajendra }
		culture = tamil
		religion = hindu
		birth_date = 1010.1.1
		birth = thanjavur
		dynasty = chola_dynasty
		tag = COZ
	}

	clk_someshvara_i_ahavamalla = {
		first_name = { name = Someshvara }
		culture = kannadiga
		religion = hindu
		birth_date = 1015.1.1
		birth = kalyani
		dynasty = chalukya_dynasty
		tag = CLK
	}

	paa_vigrahapala_iii = {
		first_name = { name = Vigrahapala }
		culture = bengali
		religion = mahayana
		birth_date = 1020.1.1
		birth = monghyr
		dynasty = pala_dynasty
		tag = PAA
	}

	# name_jayasimha is a VANILLA KEY present in malvi_language itself —
	# the one seat in the five that rides a key, not a literal.
	pmr_jayasimha_i_paramara = {
		first_name = { name = name_jayasimha }
		culture = malvi
		religion = hindu
		birth_date = 1025.1.1
		birth = dhar
		dynasty = paramara_dynasty
		tag = PMR
	}

	chu_karna_solanki = {
		first_name = { name = Karna }
		culture = gujarati
		religion = hindu
		birth_date = 1035.1.1
		birth = patan
		dynasty = solanki_dynasty
		tag = CHU
	}

	jjk_kirtivarman_chandela = {
		first_name = { name = Kirtivarman }
		culture = bundeli
		religion = hindu
		birth_date = 1025.1.1
		birth = kalinjar
		dynasty = chandela_dynasty
		tag = JJK
	}

	rtp_lakshmi_karna = {
		first_name = { name = Karna }
		culture = chhattisgarhi
		religion = hindu
		birth_date = 1010.1.1
		birth = ratnapura
		dynasty = kalachuri_dynasty
		tag = RTP
	}

	# name_vijayabahu: one of sinhala_language's three keys, vanilla.
	dbd_vijayabahu_i = {
		first_name = { name = name_vijayabahu }
		culture = sinhalese
		religion = theravada
		birth_date = 1030.1.1
		birth = tissamaharama
		dynasty = sinhala_dynasty
		tag = DBD
	}

	# --- 1066 Africa ------------------------------------------------------
	# The theater's one seat (decision 8): al-Bakri, writing 1067-68,
	# names the reigning king of Ghana — the single near-contemporary
	# attested ruler in sub-Saharan Africa. Invented literal + loc row
	# (the Virarajendra route): vanilla's mande pool ships bare `Tunka`
	# (00_sahel.txt:110), which supports the title-reading [D]; the
	# seat uses the full historiographical form. Religion sunni follows
	# the tag's registry (decision 4 — al-Bakri's king was NOT Muslim,
	# banked for the pop phase with the ground correction). Birth year
	# estimated [U]. cisse_dynasty: the Soninke house tradition names
	# the Cisse [D]; authored in 04_zz_1066_dynasties.txt.
	gha_tunka_manin = {
		first_name = { name = Tunka_Manin }
		culture = soninke
		religion = sunni
		birth_date = 1030.1.1
		birth = koumbi_saleh
		dynasty = cisse_dynasty
		tag = GHA
	}

	# --- 1066 Northern Dynasties ------------------------------------------
	# Cultures/religions from the tags' own registry blocks. kharchin is
	# the best-available Khitan proxy (vanilla paints it on the Khitan
	# heartland; khitan_culture is banked for the pop phase); mi_niah IS
	# vanilla's Tangut culture, on zero locations. The Weiming were the
	# Tangut imperial clan's own name; "Li" was the Tang-granted surname
	# the sources still use for the men — hence Li_Liangzuo the person,
	# weiming_dynasty the house [D].
	lia_yelu_hongji_daozong = {
		first_name = { name = Yelu_Hongji }
		culture = kharchin_culture
		religion = mahayana
		birth_date = 1032.1.1
		birth = linhuang
		dynasty = yelu_dynasty
		tag = LIA
	}

	xia_li_liangzuo_yizong = {
		first_name = { name = Li_Liangzuo }
		culture = mi_niah_culture
		religion = mahayana
		birth_date = 1047.1.1
		birth = ningxia
		dynasty = weiming_dynasty
		tag = XIA
	}

	# --- 1066 China-East --------------------------------------------------
	# All literals with loc rows (invented-literal route, proven nine
	# times); cultures/religions copied from each tag's own registry
	# block (guaranteed-valid). Births [U] except where the year is
	# firm (Munjong 1019, Ly Nhat Ton 1023, Zhao Shu 1032).
	chi_zhao_shu_yingzong = {
		first_name = { name = Zhao_Shu }
		culture = zhongyuan_culture
		religion = sanjiao
		birth_date = 1032.1.1
		birth = kaifeng
		dynasty = zhao_dynasty
		tag = CHI
	}

	kor_wang_hwi_munjong = {
		first_name = { name = Wang_Hwi }
		culture = korean_culture
		religion = mahayana
		birth_date = 1019.1.1
		birth = kaesong
		dynasty = wang_dynasty
		tag = KOR
	}

	dai_ly_nhat_ton = {
		first_name = { name = Ly_Nhat_Ton }
		culture = vietnamese_culture
		religion = mahayana
		birth_date = 1023.1.1
		birth = thang_long
		dynasty = ly_dynasty
		tag = DAI
	}

	# No dynasty on the two southern kings (the QMT/AQU precedent).
	cha_rudravarman_iii = {
		first_name = { name = Rudravarman }
		culture = cham_culture
		religion = hindu
		birth_date = 1030.1.1
		birth = vijaya
		tag = CHA
	}

	cdl_duan_silian = {
		first_name = { name = Duan_Silian }
		culture = bai_culture
		religion = mahayana
		birth_date = 1015.1.1
		birth = taihe_dali
		dynasty = duan_dynasty
		tag = CDL
	}

	# Shaiva Angkor: the ruler is hindu over KHM's theravada registry —
	# a ruler-vs-country religion split, legal and historical (the
	# Buddhist turn is Jayavarman VII, 1181).
	khm_harshavarman_iii = {
		first_name = { name = Harshavarman }
		culture = khmer_culture
		religion = hindu
		birth_date = 1035.1.1
		birth = angkor
		tag = KHM
	}

	# --- 1066 Arabia ------------------------------------------------------
	# Both dates [U]. name_yahya ships with a vanilla .arabic_language
	# row ("Yahya"/"Yaḥyā", dynamic loc :18702-18703) — bahrani_culture's
	# peninsular_dialect nests in arabic_language, so he renders "Yaḥyā";
	# name_husayn likewise ("Ḥusayn", :9276-9277). Nothing invented.
	# Yahya carries NO dynasty (the council of six had none — the
	# AQU/RAV/PAR precedent); the Husaynid sharif carries the new
	# muhanna_dynasty.
	qmt_yahya_ibn_al_abbas = {
		first_name = { name = name_yahya }
		culture = bahrani_culture
		religion = shia
		birth_date = 1020.1.1
		birth = al_ahsa
		tag = QMT
	}

	mda_al_husayn_ibn_muhanna = {
		first_name = { name = name_husayn }
		culture = hijazi_culture
		religion = shia
		birth_date = 1025.1.1
		birth = medina
		dynasty = muhanna_dynasty
		tag = MDA
	}

	# --- 1066 Central Asia (the Kara-Khanid slice) ------------------------
	# Both dates [U]. Ibrahim is a vanilla LITERAL row
	# (character_names_l_english.yml:1364 — the Alp_Arslan class);
	# name_mahmud is a vanilla key with arabic/persian/turkish rows.
	# NO invented name key in this slice — a first at this size.
	#
	# Ibrahim ibn Nasr (Buri Tigin, TAMGHACH Bughra Khan), khan of the
	# western kaghanate at Samarkand c.1040-1068: madrasa and hospital
	# founder, coin issuer, the best-attested man in the theater.
	qrk_ibrahim_tamghach_khan = {
		first_name = { name = Ibrahim }
		culture = khorezmian_culture
		religion = sunni
		birth_date = 1000.1.1
		birth = samarkand
		dynasty = qarakhanid_dynasty
		tag = QRK
	}

	# Mahmud ibn Yusuf, TOGHRUL Qara Khan, eastern khan c.1059-1075.
	# The eastern regnal list is genuinely unstable [D]: Sulayman/
	# Muhammad/Ibrahim b. Muhammad appear with different dates by
	# authority; Mahmud is the majority reading for 1066. The throne-name
	# literal Toghrul also ships in vanilla (:15547) if ever preferred —
	# the Alp Arslan precedent.
	qra_mahmud_toghrul_khan = {
		first_name = { name = name_mahmud }
		culture = khorezmian_culture
		religion = sunni
		birth_date = 1010.1.1
		birth = kashgar
		dynasty = qarakhanid_dynasty
		tag = QRA
	}

	# --- 1066 Seljuk world ------------------------------------------------
	# All dates [U]. Alp_Arslan/Ibrahim/Muslim are vanilla LITERALS
	# (character_names_l_english.yml:12559/:1364/:26123 — the
	# underscore-to-space law); Shavur, Fariburz and Dubays are OUR
	# literals (invented keys five to seven). name_qawurd and name_qaim
	# ship in vanilla.
	sel_alp_arslan = {
		first_name = { name = Alp_Arslan }
		culture = turkmen_culture
		religion = sunni
		birth_date = 1029.1.1
		birth = merv
		dynasty = seljukids_dynasty
		tag = SEL
	}

	abs_abdallah_al_qaim = {
		first_name = { name = name_abdullah }
		culture = iraqi_culture
		religion = sunni
		estate = clergy_estate
		birth_date = 1001.1.1
		birth = baghdad
		dynasty = abbasid_dynasty
		tag = ABS
	}

	krm_qawurd = {
		first_name = { name = name_qawurd }
		culture = turkmen_culture
		religion = sunni
		birth_date = 1025.1.1
		birth = merv
		dynasty = seljukids_dynasty
		tag = KRM
	}

	ghz_ibrahim = {
		first_name = { name = Ibrahim }
		culture = turkish_culture
		religion = sunni
		birth_date = 1033.1.1
		birth = ghazni
		dynasty = ghaznavid_dynasty
		tag = GHZ
	}

	uqy_muslim_ibn_quraysh = {
		first_name = { name = Muslim }
		culture = iraqi_culture
		religion = shia
		birth_date = 1035.1.1
		birth = mosul
		dynasty = uqaylid_dynasty
		tag = UQY
	}

	mrd_nasr_nizam_al_din = {
		first_name = { name = name_nasr }
		culture = kurdish_culture
		religion = sunni
		birth_date = 1030.1.1
		birth = mayyafariqin
		dynasty = marwanid_dynasty
		tag = MRD
	}

	hlb_mahmud_ibn_nasr = {
		first_name = { name = name_mahmud }
		culture = levantine_culture
		religion = shia
		birth_date = 1025.1.1
		birth = aleppo
		dynasty = mirdasid_dynasty
		tag = HLB
	}

	shd_abu_l_aswar_shavur = {
		first_name = { name = Shavur }
		culture = kurdish_culture
		religion = sunni
		birth_date = 995.1.1
		birth = ganja
		dynasty = shaddadid_dynasty
		tag = SHD
	}

	srv_fariburz_i = {
		first_name = { name = Fariburz }
		culture = adhari_culture
		religion = sunni
		birth_date = 1030.1.1
		birth = shamakhi
		dynasty = kasranid_dynasty
		tag = SRV
	}

	hll_dubays_i = {
		first_name = { name = Dubays }
		culture = iraqi_culture
		religion = shia
		birth_date = 1000.1.1
		birth = hillah
		dynasty = mazyadid_dynasty
		tag = HLL
	}

	kky_ali_ibn_faramurz = {
		first_name = { name = name_ali }
		culture = farsi_culture
		religion = shia
		birth_date = 1035.1.1
		birth = yazd
		dynasty = kakuyid_dynasty
		tag = KKY
	}

	# --- 1066 Fatimid Egypt + the southern Levant --------------------------
	# The Fatimid package (Opus 2026-07-29). Identifier routes:
	# Maad/Mustansir/Nizar are OUR literals with loc rows (the proven
	# invented-key mechanism); Badr is vanilla's own literal
	# (character_names_l_english.yml:10920); name_muhammad is the dynamic
	# registry's (:12931). Cultures: lower_egyptian_culture egypt.txt:1,
	# armenian_culture caucasian.txt:1, hijazi_culture arabia.txt:46.
	#
	# al-Mustansir Billah, 8th Fatimid Imam-Caliph — b. 2 July 1029,
	# caliph 13 June 1036 aged 7, both dates firm; d. 1094 (simulated,
	# never data). estate = clergy_estate per the ABS caliph precedent.
	fat_maad_al_mustansir = {
		first_name = { name = Maad }
		culture = lower_egyptian_culture
		religion = shia
		estate = clergy_estate
		birth_date = 1029.7.2
		birth = cairo
		dynasty = fatimid_dynasty
		tag = FAT
	}

	# Nizar, the caliph's eldest son — b. 26 Sep 1045, firm. Never
	# formally designated wali al-ahd [D]; under theocratic_elective the
	# heir is the oldest clergy-estate male, so Nizar is AN eligible
	# heir, not THE heir — accepted (the ABS trade-off; user-approved).
	fat_nizar = {
		first_name = { name = Nizar }
		culture = lower_egyptian_culture
		religion = shia
		estate = clergy_estate
		birth_date = 1045.9.26
		birth = cairo
		father = fat_maad_al_mustansir
		dynasty = fatimid_dynasty
		tag = FAT
	}

	# Badr al-Jamali — Armenian, governor of Damascus and all Syria from
	# 3 July 1066 (his second tenure); vizier and the state's rescuer
	# from Jan 1074. Authored UNSEATED, the Tashfin precedent. Birth
	# c. 1005-1008 [U]; birthplace unattested — Ani stands in [U].
	fat_badr_al_jamali = {
		first_name = { name = Badr }
		culture = armenian_culture
		religion = shia
		birth_date = 1006.1.1
		birth = ani
		tag = FAT
	}

	# Abu Hashim Muhammad ibn Ja'far al-Hasani, first Hawashim emir of
	# Mecca — appointed 1063 by Ali al-Sulayhi of Yemen (our seated YEM
	# ruler); reads the khutba for al-Mustansir until 15 April 1071 (the
	# switch to the Abbasids is an event hook). b. c. 1020-24 [U].
	mec_muhammad_abu_hashim = {
		first_name = { name = name_muhammad }
		culture = hijazi_culture
		religion = shia
		birth_date = 1022.1.1
		birth = mecca
		dynasty = hawashim_dynasty
		tag = MEC
	}

	# --- 1066 France: the demesne partition's three new thrones ------------
	# The France-demesne package (Opus 2026-07-29). Name keys are all
	# vanilla (character_names_dynamic_l_english.yml): name_william
	# renders "Guillaume"/"Guilhem" by the ruler's language (:18222/
	# :18235), name_ralph renders "Raoul" (:14702), name_herbert :8798.
	# Cultures: languedocien cultures/french.txt:389, picard :104.
	# All three accessions/births are [U] estimates.
	#
	# William IV of Toulouse (r. 1061-1094) — vanilla's own TOU regnal
	# table already counts name_william = 4 (10_countries.txt:17843);
	# Raymond IV of Saint-Gilles is 1094, a succession hook.
	tou_guilhem_iv_toulouse = {
		first_name = { name = name_william }
		culture = languedocien
		religion = catholic
		birth_date = 1040.1.1
		birth = toulouse
		dynasty = toulouse_dynasty
		tag = TOU
	}

	# Raoul IV de Crepy — count of Valois, Amiens and the Vexin, the
	# scandal of the age: marries Philip I's widowed mother Anne of
	# Kyiv c. 1062 and is excommunicated for it. Dies 1074.
	vls_raoul_iv_crepy = {
		first_name = { name = name_ralph }
		culture = picard
		religion = catholic
		birth_date = 1025.1.1
		birth = crepy
		dynasty = crepy_dynasty
		tag = VLS
	}

	# Herbert IV of Vermandois (r. 1045-1080) — the last Carolingian
	# count in the male line, hence vanilla's own carolingian_dynasty
	# (04_dynasties.txt:6746, marked "# Extinct" — not in 1066).
	vmd_herbert_iv_vermandois = {
		first_name = { name = name_herbert }
		culture = picard
		religion = catholic
		birth_date = 1032.1.1
		birth = saint_quentin
		dynasty = carolingian_dynasty
		tag = VMD
	}

	# --- 1066 British Isles ------------------------------------------------
	# The British package (Opus 2026-07-29). Name routes: Bleddyn/
	# Rhiwallon/Cadwgan/Caradog/MaelSnechtai are OUR literals with loc
	# rows (vanilla's own Welsh literals Meurig/Gwyn at
	# character_names_l_english.yml:1057-1058 are the precedent, next to
	# the ap_/ab_ patronymic particles); name_meredith renders "Maredudd"
	# (dynamic:12565 .brythonic_language) and name_connor "Conchobar"
	# (:4862 .gaelic_language). welsh culture -> welsh_dialect nested in
	# brythonic_language (british.txt:104, languages/00_great_britain.txt)
	# — the dialect->parent name fallback is the render probe.
	#
	# Bleddyn ap Cynfyn — installed over Gwynedd AND Powys with his
	# brother in August 1063 by Harold and Tostig after Gruffydd ap
	# Llywelyn's fall; rules to 1075. House of Mathrafal (ships,
	# 04_dynasties.txt:213). Births [U] throughout the Welsh five.
	gdd_bleddyn_ap_cynfyn = {
		first_name = { name = Bleddyn }
		culture = welsh
		religion = catholic
		birth_date = 1025.1.1
		birth = montgomery
		dynasty = mathrafal_dynasty
		tag = GDD
	}

	# Rhiwallon ap Cynfyn — Bleddyn's brother and co-ruler, seated on
	# Powys (the joint rule split across the two tags); dies at Mechain
	# 1069 fighting Gruffydd's sons — a succession hook.
	pws_rhiwallon_ap_cynfyn = {
		first_name = { name = Rhiwallon }
		culture = welsh
		religion = catholic
		birth_date = 1027.1.1
		birth = montgomery
		dynasty = mathrafal_dynasty
		tag = PWS
	}

	dhb_maredudd_ab_owain = {
		first_name = { name = name_meredith }
		culture = welsh
		religion = catholic
		birth_date = 1030.1.1
		birth = carmarthen
		dynasty = dinefwr_dynasty
		tag = DHB
	}

	mwg_cadwgan_ap_meurig = {
		first_name = { name = Cadwgan }
		culture = welsh
		religion = catholic
		birth_date = 1030.1.1
		birth = cardiff
		dynasty = morgannwg_dynasty
		tag = MWG
	}

	# Caradog ap Gruffydd of Gwent/Gwynllwg — the 1065 destruction of
	# Harold's hunting lodge at Portskewett is the best 1066 attestation
	# in Wales.
	gwt_caradog_ap_gruffydd = {
		first_name = { name = Caradog }
		culture = welsh
		religion = catholic
		birth_date = 1035.1.1
		birth = newport
		dynasty = gwent_dynasty
		tag = GWT
	}

	# Conchobar Ua Mael Sechlainn, king of Mide c.1030-1073 [U] — the
	# o_melaghlin_dynasty ships (04_dynasties.txt:361, home = athlone).
	mth_conchobar_ua_mael_sechlainn = {
		first_name = { name = name_connor }
		culture = irish
		religion = catholic
		birth_date = 1010.1.1
		birth = mullingar
		dynasty = o_melaghlin_dynasty
		tag = MTH
	}

	# Mael Snechtai mac Lulaig, king/mormaer of Moray — son of King
	# Lulach (SCO's own regnal table carries name_lulach = 1); defeated
	# by Malcolm III in 1078, dies 1085. Cenel Loairn: vanilla's
	# loairn_dynasty (04_dynasties.txt:626, home = inverness).
	moy_mael_snechtai = {
		first_name = { name = MaelSnechtai }
		culture = highland
		religion = catholic
		birth_date = 1035.1.1
		birth = elgin
		dynasty = loairn_dynasty
		tag = MOY
	}

	# --- 1066 southern Italy ------------------------------------------------
	# The Mezzogiorno package (Opus 2026-07-29). Vanilla ships ZERO
	# usable characters here (the only guiscard/hauteville hits are
	# comments and two Limousin lords). Name routes: the Normans'
	# name_robert/roger/richard have no norman-dialect rows and fall
	# through to the base forms — exactly right; the Lombards take the
	# neapolitan_dialect rows (name_sergius -> "Sergie"); name_gisulf
	# and name_ayyub are invented keys #8 and #9 (zero hits in both
	# registries, loc rows shipped). Births [U] throughout.
	#
	# Robert Guiscard — sixth son of Tancred of Hauteville, Duke of
	# Apulia and Calabria by the Melfi investiture of August 1059.
	# Historically dies 1085 besieging Cephalonia; excommunicated and
	# absolved twice — situation material for decades.
	apu_robert_guiscard = {
		first_name = { name = name_robert }
		culture = norman
		religion = catholic
		birth_date = 1015.1.1
		birth = coutances
		dynasty = hauteville_dynasty
		tag = APU
	}

	# Roger, Guiscard's youngest brother — Count of Sicily from the
	# Messina beachhead; takes Palermo 1072, Malta 1091; his son is
	# the first King of Sicily.
	sic_roger_de_hauteville = {
		first_name = { name = name_roger }
		culture = norman
		religion = catholic
		birth_date = 1031.1.1
		birth = coutances
		dynasty = hauteville_dynasty
		tag = SIC
	}

	cup_richard_i_drengot = {
		first_name = { name = name_richard }
		culture = norman
		religion = catholic
		birth_date = 1025.1.1
		birth = alencon
		dynasty = drengot_dynasty
		tag = CUP
	}

	# Gisulf II, last Lombard prince of Salerno — succeeded on his
	# father Guaimar IV's murder (3 June 1052); Guiscard, his own
	# brother-in-law, takes Salerno in 1077.
	slr_gisulf_ii_salerno = {
		first_name = { name = name_gisulf }
		culture = neapolitan
		religion = catholic
		birth_date = 1040.1.1
		birth = salerno
		dynasty = salerno_dynasty
		tag = SLR
	}

	nea_sergius_v_naples = {
		first_name = { name = name_sergius }
		culture = neapolitan
		religion = catholic
		birth_date = 1030.1.1
		birth = naples
		dynasty = sergi_dynasty
		tag = NEA
	}

	gae_atenulf_i_aquino = {
		first_name = { name = name_atenulf }
		culture = neapolitan
		religion = catholic
		birth_date = 1025.1.1
		birth = gaeta
		dynasty = aquino_dynasty
		tag = GAE
	}

	# Ayyub ibn Tamim — son of OUR seated Tamim of TUN, sent by the
	# Zirids to hold Palermo 1063-1068/69 [D]; rides our own
	# zirid_dynasty. The father link crosses into the NEW_CHARACTERS
	# Zirid block (zir_tamim_ibn_al_muizz precedes him — parents
	# before children).
	plm_ayyub_ibn_tamim = {
		first_name = { name = name_ayyub }
		culture = tunisian
		religion = sunni
		# 1048, not the package's 1040: Tamim is born 1031 and the engine
		# rejects a father under ten at conception
		# (character_manager.cpp:287, observed 2026-07-30). Ayyub's real
		# birth year is unrecorded [U]; 1048 makes Tamim sixteen at the
		# conception and Ayyub eighteen at start — both thresholds pass.
		birth_date = 1048.1.1
		birth = kairouan
		father = zir_tamim_ibn_al_muizz
		dynasty = zirid_dynasty
		tag = PLM
	}

	# --- 1066 Empire (HRE slice) -------------------------------------------
	# Heinrich IV needs NO authoring — vanilla ships him
	# (ogk_heinrich_iv_salier, 05_characters.txt:104039, salian_dynasty)
	# and name_henry renders "Heinrich" through german_language. The
	# three below are the southeastern cast; births [U] throughout.
	# name_ernest carries a .german_language "Ernst" row (free win);
	# name_berthold's base form is right; Otakar is invented literal
	# key #19 — name_odoacer would render "Odoacer" on a German ruler
	# (the .west_slavic_language row is the only "Otakar" in vanilla).
	hab_ernst_babenberg = {
		first_name = { name = name_ernest }
		culture = danube_bavarian
		religion = catholic
		birth_date = 1027.1.1
		birth = vienna
		dynasty = babenberg_dynasty
		tag = HAB
	}

	# Berthold I of Zähringen — TITULAR Duke of Carinthia 1061-1077;
	# never took possession [D], the Eppensteiner ruled de facto. The
	# seat models the title; the tension is Germany II material.
	crh_berthold_zahringen = {
		first_name = { name = name_berthold }
		culture = rhine_alemannic
		religion = catholic
		birth_date = 1000.1.1
		birth = villingen
		dynasty = zahringen_dynasty
		tag = CRH
	}

	sty_otakar_steyr = {
		first_name = { name = Otakar }
		culture = danube_bavarian
		religion = catholic
		birth_date = 1020.1.1
		birth = steyr
		dynasty = otakar_dynasty
		tag = STY
	}

	# --- 1066 Germany II ---------------------------------------------------
	# Twenty-eight characters for twenty-nine seats: Godfrey the Bearded
	# holds BLL and SPL at once, which is one character block and two
	# HISTORICAL_RULERS rows (vanilla's boh_john_luxembourg shape).
	#
	# NAME KEYS. Twelve ride vanilla's dynamic registry, every one checked
	# by line in main_menu/localization/english/character_names_dynamic_l_english.yml:
	#   name_rudolf :15318   name_otto :13603     name_conrad :4901
	#   name_baldwin :2813   name_william :18209  name_werner :18122
	#   name_herman :8830    name_burchard :3939  name_frederick :7376
	#   name_gebhard :7704   name_godfrey :8050   name_egbert :6137
	# name_godfrey/.german_language is "Gottfried" (:8064) and
	# name_herman/.german_language "Hermann" (:8834) — free wins on any
	# German-dialect culture, since 00_germany.txt:679 falls the dialects
	# back to german_language. name_ekbert does NOT exist anywhere;
	# name_egbert is the key for Egbert of Brunswick.
	# The other fourteen are INVENTED KEYS — the proven mechanism
	# (name_guislabert, the taifa three): a `name = name_x` reference plus
	# ONE loc row in our own yml. All fourteen were checked to have ZERO
	# rows across vanilla's ENTIRE localization tree, every language:
	# ordulf anno udo theoduin adalbert adalbero hezilo imad benno altmann
	# gundekar rumold einhard dedi.
	#
	# BIRTHPLACES are the tag's capital or the bishop's see (the package
	# rule); all 28 exist in in_game/map_data/definitions.txt.
	# CULTURES follow the birth location's own culture in
	# in_game/map_data/location_templates.txt, with four Rhineland/Moselle
	# corrections that ride vanilla's OWN character for the same tag —
	# the mod's mai_siegfried_i precedent, where Mainz is `westphalian` in
	# the templates and the archbishop is rhine_franconian:
	#   KOL ripuarian_franconian (vanilla kol_walram_von_julich)
	#   TRI walloon              (vanilla tri_balduin_von_luxembourg)
	#   SPY rhine_franconian     (vanilla spy_gerhard_von_ehrenberg)
	#   PAL rhine_franconian     (vanilla's PAL cast, 5 of 11)
	# NO death dates on anyone: all 28 are alive on 1066.9.15, and four of
	# them (Einhard, Benno, Otto of Regensburg, Egbert) die within
	# eighteen months — a death_date would start them DEAD instead.

	# Rudolf of Rheinfelden, Duke of Swabia from 1057 — elected anti-king
	# in 1077 and killed at the Elster in 1080. The single most
	# consequential man in Germany after Heinrich IV himself.
	swa_rudolf_rheinfelden = {
		first_name = { name = name_rudolf }
		culture = swabian
		religion = catholic
		birth_date = 1025.1.1
		birth = ulm
		dynasty = rheinfelden_dynasty
		tag = SWA
	}

	# Ordulf Billung, Duke of Saxony on his father Bernard II's death
	# (29 June 1059); historically dies 1072. The Billung duchy is the
	# tag Paradox wanted for LUN and said so (05_characters.txt:86620).
	sax_ordulf_billung = {
		first_name = { name = name_ordulf }
		culture = lower_saxon
		religion = catholic
		birth_date = 1020.1.1
		birth = luneburg
		dynasty = billung_dynasty
		tag = SAX
	}

	# Anno II, Archbishop of Cologne from 1056 — seized the boy king at
	# Kaiserswerth in April 1062 and governed the Empire. Historically
	# dies 1075; canonised 1183.
	kol_anno_ii = {
		first_name = { name = name_anno }
		culture = ripuarian_franconian
		religion = catholic
		birth_date = 1010.1.1
		birth = cologne
		dynasty = steusslingen_dynasty
		tag = KOL
	}

	# Udo of Nellenburg, Archbishop of Trier — enthroned in the summer of
	# 1066 after the murder of Kuno of Pfullingen [U on the day]; the
	# third archbishop Trier had that year, which is why the HRE slice
	# left the tag random and this one seats it.
	tri_udo_nellenburg = {
		first_name = { name = name_udo }
		culture = walloon
		religion = catholic
		birth_date = 1030.1.1
		birth = trier
		dynasty = nellenburg_dynasty
		tag = TRI
	}

	# Godfrey III "the Bearded" — Duke of Lower Lorraine from 1065 and,
	# through his 1054 marriage to Beatrice of Bardi, Margrave of Tuscany
	# and Spoleto. TWO SEATS, one character: the pluralist route vanilla
	# itself ships (boh_john_luxembourg on BOH and LUX). Historically
	# dies 1069; his son is Godfrey the Hunchback and his granddaughter
	# by marriage is Matilda of Canossa.
	bll_godfrey_iii_bearded = {
		first_name = { name = name_godfrey }
		culture = walloon
		religion = catholic
		birth_date = 997.1.1
		birth = bouillon
		dynasty = ardennes_dynasty
		tag = BLL
	}

	# Otto of Weimar-Orlamünde, Margrave of Meissen from 1062 [U];
	# historically dies 1067. The Wettins only take Meissen in 1089.
	mei_otto_weimar = {
		first_name = { name = name_otto }
		culture = saxon
		religion = catholic
		birth_date = 1020.1.1
		birth = meissen
		dynasty = weimar_dynasty
		tag = MEI
	}

	# Conrad I, Count of Luxembourg [U on the accession year]. The
	# Ardennes-Luxembourg branch gets its own house rather than sharing
	# Godfrey's: the two lines split four generations before 1066 and a
	# shared dynasty would render them one family in game.
	lux_conrad_i = {
		first_name = { name = name_conrad }
		culture = walloon
		religion = catholic
		birth_date = 1040.1.1
		birth = luxembourg
		dynasty = ardennes_luxembourg_dynasty
		tag = LUX
	}

	# Baldwin I of Hainaut — son of OUR seated Baldwin V of Flanders,
	# count by his 1051 marriage to Richilde. The cross-tag father link
	# and the inherited house/culture/birthplace are the Ayyub/Tamim
	# shape exactly (plm_ayyub_ibn_tamim rides his father's zirid_dynasty,
	# culture and Ifriqiyan birthplace, not Palermo's).
	hai_baldwin_i_hainaut = {
		first_name = { name = name_baldwin }
		culture = low_franconian
		religion = catholic
		birth_date = 1030.1.1
		birth = bruges
		father = fla_baldwin_v_flanders
		dynasty = flanders_dynasty
		tag = HAI
	}

	# William I, Prince-Bishop of Utrecht from 1054 — Heinrich IV's man
	# against the Gregorians; historically dies 1076.
	utr_william_i = {
		first_name = { name = name_william }
		culture = low_franconian
		religion = catholic
		birth_date = 1015.1.1
		birth = utrecht
		tag = UTR
	}

	# Theoduin (Dietwin), Prince-Bishop of Liège from 1048; historically
	# dies 1075. name_theoduin is invented key #20.
	lie_theodwin = {
		first_name = { name = name_theoduin }
		culture = walloon
		religion = catholic
		birth_date = 1000.1.1
		birth = liege
		tag = LIE
	}

	# The fifteen sees. Bishops carry NO dynasty line — the
	# mai_siegfried_i precedent; dynasty-less characters are
	# vanilla-attested — except the two whose houses this slice already
	# needs for a lay seat (Goseck for Bremen, Steusslingen for
	# Magdeburg, the same house as Anno of Cologne).

	# Adalbert of Goseck, Archbishop of Hamburg-Bremen from 1043 — Anno's
	# rival for the regency, the missionary of the North. Historically
	# dies 1072.
	bre_adalbert_goseck = {
		first_name = { name = name_adalbert }
		culture = lower_saxon
		religion = catholic
		birth_date = 1000.1.1
		birth = bremen
		dynasty = goseck_dynasty
		tag = BRE
	}

	# Werner of Steusslingen, Archbishop of Magdeburg from 1064 — Anno's
	# own kin; historically dies 1078 of wounds taken in the Saxon war.
	mag_werner_steusslingen = {
		first_name = { name = name_werner }
		culture = markish
		religion = catholic
		birth_date = 1020.1.1
		birth = magdeburg
		dynasty = steusslingen_dynasty
		tag = MAG
	}

	wbg_adalbero = {
		first_name = { name = name_adalbero }
		culture = east_franconian
		religion = catholic
		birth_date = 1010.1.1
		birth = wurzburg
		tag = WBG
	}

	bam_herman_i = {
		first_name = { name = name_herman }
		culture = east_franconian
		religion = catholic
		birth_date = 1025.1.1
		birth = bamberg
		tag = BAM
	}

	hdh_hezilo = {
		first_name = { name = name_hezilo }
		culture = lower_saxon
		religion = catholic
		birth_date = 1020.1.1
		birth = hildesheim
		tag = HDH
	}

	hbs_burchard_ii = {
		first_name = { name = name_burchard }
		culture = lower_saxon
		religion = catholic
		birth_date = 1028.1.1
		birth = halberstadt
		tag = HBS
	}

	mun_friedrich = {
		first_name = { name = name_frederick }
		culture = lower_saxon
		religion = catholic
		birth_date = 1025.1.1
		birth = munster
		tag = MUN
	}

	pdb_imad = {
		first_name = { name = name_imad }
		culture = lower_saxon
		religion = catholic
		birth_date = 1010.1.1
		birth = paderborn
		tag = PDB
	}

	# Gebhard of Salzburg — the one unwavering Gregorian in the German
	# south; historically driven from his see 1077 and dies 1088.
	slz_gebhard = {
		first_name = { name = name_gebhard }
		culture = danube_bavarian
		religion = catholic
		birth_date = 1010.1.1
		birth = salzburg
		tag = SLZ
	}

	pss_altmann = {
		first_name = { name = name_altmann }
		culture = danube_bavarian
		religion = catholic
		birth_date = 1015.1.1
		birth = passau
		tag = PSS
	}

	eic_gundekar_ii = {
		first_name = { name = name_gundekar }
		culture = danube_bavarian
		religion = catholic
		birth_date = 1019.1.1
		birth = eichstatt
		tag = EIC
	}

	knz_rumold = {
		first_name = { name = name_rumold }
		culture = high_alemannic
		religion = catholic
		birth_date = 1010.1.1
		birth = konstanz
		tag = KNZ
	}

	# Einhard, Bishop of Speyer — historically dies February 1067, four
	# months after start. Accepted drift: a death_date would start him
	# dead today rather than kill him then.
	spy_einhard = {
		first_name = { name = name_einhard }
		culture = rhine_franconian
		religion = catholic
		birth_date = 1015.1.1
		birth = speyer
		tag = SPY
	}

	# Benno I of Osnabrück — historically dies December 1067. Same
	# accepted drift.
	osn_benno_i = {
		first_name = { name = name_benno }
		culture = lower_saxon
		religion = catholic
		birth_date = 1010.1.1
		birth = osnabruck
		tag = OSN
	}

	# Otto of Riedenburg, Bishop of Regensburg — historically dies 1067.
	# Same accepted drift.
	reg_otto_riedenburg = {
		first_name = { name = name_otto }
		culture = danube_bavarian
		religion = catholic
		birth_date = 1020.1.1
		birth = regensburg
		tag = REG
	}

	# Dedi I of Wettin, Margrave of the Saxon Ostmark [U on the year] —
	# the Wettins ARE in 1066, just not yet in Meissen. Culture saxon
	# rather than his march's sorbian: vanilla's own wettin_dynasty sits
	# at halle_an_der_saale (04_dynasties.txt:4070), a saxon location,
	# and every vanilla margrave of Meissen is saxon. A German house over
	# Sorbian subjects is the ruler-culture case PLM/AGR already model.
	sor_dedi_i = {
		first_name = { name = name_dedi }
		culture = saxon
		religion = catholic
		birth_date = 1004.1.1
		birth = cottbus
		dynasty = wettin_dynasty
		tag = SOR
	}

	# Hermann II of the Ezzonen, Count Palatine of the Rhine from 1064 —
	# SEVENTEEN at start (b. 1049 [U]), so no MINOR_RULERS entry: the
	# build's adult check passes on its own and listing him would fail as
	# a stale exemption. Historically dies 1085, the last Ezzone.
	pal_hermann_ii = {
		first_name = { name = name_herman }
		culture = rhine_franconian
		religion = catholic
		birth_date = 1049.1.1
		birth = kaiserslautern
		dynasty = ezzonen_dynasty
		tag = PAL
	}

	# Egbert I the Brunonen, Margrave of Meissen and Count of Brunswick —
	# historically dies January 1068. Accepted drift; his son Egbert II
	# is the Saxon rebellion's man.
	bru_egbert_i = {
		first_name = { name = name_egbert }
		culture = lower_saxon
		religion = catholic
		birth_date = 1025.1.1
		birth = brunswick
		dynasty = brunonen_dynasty
		tag = BRU
	}

	# --- Italy North (approved package 2026-07-29) ------------------------
	# Beatrice of Bar, margravine of Tuscany — ruling since Boniface III's
	# 1052 murder, married to Godfrey the Bearded since 1054 (HE is already
	# authored on BLL/SPL: the couple rules the middle of the peninsula
	# between them, each on their own thrones). female = yes is vanilla's
	# own field shape (05_characters.txt:105). name_beatrix is vanilla
	# (character_names_dynamic_l_english.yml:3132, "Beatrix");
	# de_bar_dynasty is vanilla too (04_dynasties.txt:5959, home nancy —
	# her birth house, correct until Matilda), so neither needs authoring.
	tus_beatrice_di_bar = {
		first_name = { name = name_beatrix }
		female = yes
		culture = lorrain
		religion = catholic
		estate = nobles_estate
		birth_date = 1020.1.1
		birth = nancy
		dynasty = de_bar_dynasty
		tag = TUS
	}

	# Matilda of Canossa, the future Great Countess — authored UNSEATED at
	# twenty (the Badr al-Jamali precedent), daughter of the seated
	# Beatrice. canossa_dynasty is created for her: the march passes to
	# the house of Canossa's heiress, and the dynasty existing NOW is what
	# makes that succession expressible later. Mother link only — her
	# father Boniface is not authored, and we do not write dangling
	# references (validate ours strictly, report vanilla's). Birth city
	# [U] — Lucca by the majority reading; name_matilda is vanilla
	# (de_bar's own female_names row, 04_dynasties.txt:5956).
	tus_matilda_di_canossa = {
		first_name = { name = name_matilda }
		female = yes
		culture = tuscan
		religion = catholic
		estate = nobles_estate
		birth_date = 1046.3.1
		birth = lucca
		mother = tus_beatrice_di_bar
		dynasty = canossa_dynasty
		tag = TUS
	}

	# Ulric I of Weimar, margrave of Carniola and Istria — the brother
	# house of MEI's Otto, riding Germany II's weimar_dynasty
	# (04_zz_1066_dynasties.txt:283). name_ulrick is VANILLA
	# (languages/00_germany.txt:215; renders "Ulrich" through the
	# .german_language row, character_names_dynamic_l_english.yml:17373)
	# — the package's literal fallback proved unnecessary. saxon is
	# Weimar's own template culture (location_templates.txt:1090).
	isr_ulrich_i_weimar = {
		first_name = { name = name_ulrick }
		culture = saxon
		religion = catholic
		estate = nobles_estate
		birth_date = 1030.1.1
		birth = weimar
		dynasty = weimar_dynasty
		tag = ISR
	}

	# The three prelates, in the kol_anno shape (no estate, no skills)
	# and dynasty-less per the mai_siegfried precedent: Ravenger's origin
	# is unrecorded, Henry's uncertain, and Cadalus's Sabbioneta line is
	# in no vanilla registry. Cultures are their sees' own template
	# values; Cadalus is Veronese-born (the one biographical anchor).
	# Cadalus IS the man who becomes antipope Honorius II in 1061 — the
	# Cadalan schism is situation material and the papal claim is
	# deliberately NOT modeled in data (package decision C).
	aqu_ravengerius = {
		first_name = { name = Ravenger }
		culture = friulian
		religion = catholic
		birth_date = 1010.1.1
		birth = aquileia
		tag = AQU
	}

	rav_henry_ravenna = {
		first_name = { name = name_henry }
		culture = romagnol
		religion = catholic
		birth_date = 1010.1.1
		birth = ravenna
		tag = RAV
	}

	par_cadalus = {
		first_name = { name = Cadalus }
		culture = venetian
		religion = catholic
		birth_date = 1010.1.1
		birth = verona
		tag = PAR
	}

	# Adelaide of Susa, margravine of Turin — the LITERAL first name is
	# the Otakar precedent: name_adelaide exists but its piedmontese row
	# renders "Lalsia" (package decision, main session). arduinici_dynasty
	# is NEW (her father Ulric Manfred II's house, home turin).
	pie_adelaide_susa = {
		first_name = { name = Adelaide }
		female = yes
		culture = piedmontese
		religion = catholic
		estate = nobles_estate
		birth_date = 1015.1.1
		birth = turin
		dynasty = arduinici_dynasty
		tag = PIE
	}

	# --- 1066 Southeast Asia ----------------------------------------------
	# Anawrahta Minsaw, king of Pagan 1044-1077 [D]. Took Thaton in 1057
	# and brought Shin Arahan's Theravada north — the reason the Irrawaddy
	# delta is Pagan's at start. NO death date (alive on 1066.9.15;
	# d. 1077 [D] is left to the engine). The name is a vanilla LITERAL
	# (character_names_l_english.yml:18682, the Ravenger route);
	# pagan_dynasty ships (04_dynasties.txt:8354, home = pagan);
	# birth year 1014 or 1015 [D] — either is well past ADULT_AGE.
	pgn_anawrahta = {
		first_name = { name = Anawrahta }
		culture = burmese_culture
		religion = theravada
		birth_date = 1014.1.1
		birth = pagan
		dynasty = pagan_dynasty
		tag = PGN
	}

	# --- 1066 Tibet -------------------------------------------------------
	# Dongzhan, son of Gusiluo, ruler of Tsongkha/Qingtang 1065-1086 [D] —
	# the Song's Tibetan ally against Xia; succeeded his father the year
	# before start. NO death date (alive on 1066.9.15; d. 1086 [D] left to
	# the engine). "Dongzhan" is the Song shi's transcription and the name
	# scholarship uses; it is an authored LITERAL with its own loc row (the
	# Tamim precedent). tsongkha_dynasty is authored in
	# 04_zz_1066_dynasties.txt (realm-named, vanilla's own pagan/purang/
	# lavo grammar); birth year 1032 [D].
	tka_dongzhan = {
		first_name = { name = Dongzhan }
		culture = amdowa_culture
		religion = tibetan_buddhism
		birth_date = 1032.1.1
		birth = xining
		dynasty = tsongkha_dynasty
		tag = TKA
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


_TPL_CACHE = {}
def _tpl_grants(inc, _walking=None):
    """Container names a setup template grants discovery of. Comment-
    stripped, so an all-comment template grants the EMPTY set — which is
    the point: expl_silk_road_center is exactly that in vanilla.
    RECURSIVE since the British slice: templates nest includes —
    catholic_monarchy_welsh_releasable's line 1 is a bare
    `include = catholic_monarchy_not_present` and line 2 the quoted
    `include = "expl_western_europe"` that carries ALL its discovery.
    A one-level reader called the Welsh shells blind when they were
    not (and would have missed the reverse mistake too)."""
    if inc in _TPL_CACHE:
        return _TPL_CACHE[inc]
    _walking = _walking or set()
    if inc in _walking:
        return set()    # cycle guard; vanilla has none, but never hang
    _walking.add(inc)
    tpl = os.path.join(VAN, "main_menu", "setup", "templates",
                       inc + ".txt")
    if not os.path.isfile(tpl):
        sys.exit(f'include "{inc}" names no vanilla template')
    body = re.sub(r"#[^\n]*", "", open(tpl, encoding="utf-8-sig").read())
    names = set()
    for m in re.finditer(r"discover(?:ed)?_(?:regions|areas|provinces)"
                         r"[ \t]*=[ \t]*\{([^}]*)\}", body):
        names |= set(m.group(1).split())
    for m in re.finditer(r'^[ \t]*include[ \t]*=[ \t]*"?([A-Za-z0-9_]+)"?',
                         body, re.M):
        names |= _tpl_grants(m.group(1), _walking)
    _TPL_CACHE[inc] = names
    return names


def _assert_new_block_discovery():
    """Every generated country block must SEE ITS OWN CAPITAL, the
    engine's init requirement ("does not know its capital, need a
    discover_areas or discovered_regions",
    initialize_from_bookmark.cpp:528) — measured 2026-07-29 playing
    SEL: the whole Persian empire started as terra incognita. The first
    draft of this assert only required "some include with live
    discovery content" and its own break test proved that inadequate:
    SEL carried three LIVE silk-road includes and still failed in game,
    because none of them contains Rey. So the check is the engine's
    own: the capital must be a member of some granted region, area or
    province, resolved through definitions.txt."""
    members, _ = _defs()
    for tag in sorted(NEW_COUNTRIES):
        block = NEW_COUNTRIES[tag]
        mcap = re.search(r"capital = (\w+)", block)
        if not mcap:
            sys.exit(f"{tag}: generated block has no capital")
        cap = mcap.group(1)
        grants = set()
        for m in re.finditer(r"discovered_regions[ \t]*=[ \t]*\{([^}]*)\}",
                             block):
            grants |= set(m.group(1).split())
        for inc in re.findall(r'include = "([^"]+)"', block):
            grants |= _tpl_grants(inc)
        if not any(cap in members.get(g, ()) for g in grants):
            sys.exit(f"{tag}: capital {cap} is not discovered by any include "
                     "or inline discovered_regions — the country fails init "
                     "(initialize_from_bookmark.cpp:528) and its player "
                     "starts blind (the expl_silk_road_center trap)")


def build_countries(src):
    report = []
    _assert_new_block_discovery()
    before = len(re.findall(COUNTRY_RE, src, re.M))
    # Pristine vanilla text, kept for the orphan-capital delta in validate():
    # only violations WE introduce fail the build (vanilla ships 10 of its
    # own — report-only, per the validate-ours/report-theirs rule).
    _pristine = src

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

    # The ONE-LINE form: vanilla ships exactly 23 `government = { ruler = X }`
    # single-liners (22 random + AOS's sav_aymon_savoy, 10_countries.txt:36343).
    # The line-anchored pass above cannot see them (no newline after the name),
    # and the add-missing pass below could not either — it prepended a SECOND
    # `ruler = random` into each, and on AOS the surviving 1291-born ruler sat
    # after it in the same line. Found by the Italy North research review,
    # 2026-07-29 night.
    def _ruler_inline(m):
        nonlocal n_ruler, n_already
        if m.group(2) == "random":
            n_already += 1
            return m.group(0)
        n_ruler += 1
        return m.group(1) + "ruler = random" + m.group(3)

    src = re.sub(r"(government[ \t]*=[ \t]*\{[ \t]*)ruler[ \t]*=[ \t]*"
                 r"([A-Za-z0-9_]+)([ \t]*\})", _ruler_inline, src)
    report.append(("ruler = <name> -> random", n_ruler))
    report.append(("ruler = random already", n_already))

    # NEW COUNTRIES: transfer the locations out of their 1337 owners first
    # (exclusive ownership is the invariant), then insert the new blocks
    # before the wrapper braces. Runs BEFORE the ruler passes so a new tag
    # gets its `ruler = random` from the add-missing pass and can be seated
    # through HISTORICAL_RULERS like any other.
    # OWNERSHIP is exactly these list keys — not `capital =` lines (a
    # landless tag's capital can sit on someone else's land) and not
    # `our_cores_conquered_by_others` (claims). The first Sardinia dry-run
    # would have double-counted sassari (GEN's ownership + TOR's claim)
    # under a cruder scan; this one parses the actual list blocks.
    OWN_KEYS = ("own_control_core", "own_control_integrated",
                "own_control_conquered", "own_control_colony", "own_core",
                "own_conquered", "own_integrated", "own_colony",
                "control_core", "control")

    def _ownership_index(s, wanted):
        """ONE sweep over every ownership block: loc -> [(start, end)] for
        each wanted location. Comments are MASKED length-preservingly first
        — `#Lost 1204` style notes contain lowercase words (van, split,
        kars ARE location names) that a raw scan would count as holdings.
        The old per-location scanner had both that bug latent and O(file)
        cost per location, which the 495-location Byzantium sweep turned
        into minutes."""
        idx = {}
        for key in OWN_KEYS:
            for m in re.finditer(r"^[ \t]*" + key + r"[ \t]*=[ \t]*\{", s, re.M):
                bo = s.index("{", m.start())
                end = find_block_end(s, bo)
                masked = re.sub(r"#[^\n]*",
                                lambda mm: " " * len(mm.group(0)),
                                s[bo:end])
                for t in re.finditer(r"[a-z][A-Za-z0-9_]*", masked):
                    if t.group(0) in wanted:
                        idx.setdefault(t.group(0), []).append(
                            (bo + t.start(), bo + t.end()))
        return idx

    def _remove_owned_many(s, locs, ctx):
        idx = _ownership_index(s, set(locs))
        bad = [f"{l}({len(idx.get(l, []))})" for l in locs
               if len(idx.get(l, [])) != 1]
        if bad:
            sys.exit(f"{ctx}: ownership occurrences != 1 for {bad[:8]}")
        for a, b in sorted((sp for v in idx.values() for sp in v),
                           reverse=True):
            s = s[:a] + s[b:]
        return s

    def _owned_by(s, tag):
        blocks_ob = list(re.finditer(COUNTRY_RE, s, re.M))
        for i, b in enumerate(blocks_ob):
            if b.group(1) != tag:
                continue
            end = blocks_ob[i + 1].start() if i + 1 < len(blocks_ob) else len(s)
            body = s[b.start():end]
            held = []
            for key in OWN_KEYS:
                for m in re.finditer(r"^[ \t]*" + key + r"[ \t]*=[ \t]*\{", body, re.M):
                    bo = body.index("{", m.start())
                    inner = re.sub(r"#[^\n]*", "",
                                   body[bo + 1:find_block_end(body, bo)])
                    held.extend(re.findall(r"[a-z][A-Za-z0-9_]*", inner))
            return held
        sys.exit(f"_owned_by: tag {tag} not found")

    # Byzantium: the grant list is RESOLVED from definitions.txt (the
    # package's rule set), minus what BYZ already holds; the 45 doomed
    # donors' holdings are snapshotted BEFORE any mutation so their
    # claims can be written after the sweep.
    _byz_have = set(_owned_by(src, "BYZ"))
    _target = _byz_target()
    LOCATION_GRANTS["BYZ"] = ([l for l in _target if l not in _byz_have]
                              + _SELJUK_BYZ_EXTRA + _ITALY_BYZ_EXTRA)
    if len(LOCATION_GRANTS["BYZ"]) != 506:
        sys.exit(f"BYZ grant list resolved to {len(LOCATION_GRANTS['BYZ'])} "
                 f"locations — 495 (Byzantium package) + 4 (Kharpert) "
                 f"+ 7 (the Italian catepanate) = 506")

    # The Seljuk world resolves the same way. Grants to a tag that
    # already holds some of its list (KRM 29, MZN 6, HLL 4) are no-ops by
    # construction: removal takes them from the tag itself, the grant
    # line puts them back.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_SELJUK_RULES.items()):
        got = _resolve_ruleset(f"_SELJUK_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_SELJUK_RULES[{_t}]: resolved {len(got)} locations, "
                     f"package count is {_exp}")
        LOCATION_GRANTS[_t] = got
    for _t, (_cap, _rank, _pol, _sch, _crt) in _SELJUK_TAGS.items():
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_SELJUK_TAGS: {_t} capital {_cap} not in its resolved list")
    if "baghdad" not in LOCATION_GRANTS["ABS"]:
        sys.exit("_SELJUK_RULES: ABS must hold baghdad")

    # The Fatimid slice resolves identically (Opus package counts:
    # MAM 119 + AAL 3 = 122; tobruk is BQA's grant, aswan/kom_ombo stay
    # BKZ's, al_ais stays MDA's). The 122 assert was proven by breaking
    # (121 -> died with "resolved 122", 2026-07-29).
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_EGYPT_RULES.items()):
        got = _resolve_ruleset(f"_EGYPT_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_EGYPT_RULES[{_t}]: resolved {len(got)} locations, "
                     f"package count is {_exp}")
        LOCATION_GRANTS[_t] = got
    if "cairo" not in LOCATION_GRANTS["FAT"]:
        sys.exit("_EGYPT_RULES: FAT must hold cairo")
    for _must in ("damascus", "jerusalem"):
        if _must not in LOCATION_GRANTS["FAT"]:
            sys.exit(f"_EGYPT_RULES: FAT must hold {_must} — the slice's "
                     "whole Levant claim rests on it")

    # The Central Asia slice resolves the same way (package counts
    # independently reproduced at review 2026-08-01: QRK 46 / QRA 142 /
    # BLH 28; QRK's donors are exactly YSU+BRL+JLY+SLD whole).
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_CENTRALASIA_RULES.items()):
        got = _resolve_ruleset(f"_CENTRALASIA_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_CENTRALASIA_RULES[{_t}]: resolved {len(got)} "
                     f"locations, package count is {_exp}")
        LOCATION_GRANTS[_t] = got
    for _t, (_cap, _rank, _pol, _sch, _crt) in _CENTRALASIA_TAGS.items():
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_CENTRALASIA_TAGS: {_t} capital {_cap} not in its "
                     "resolved list")
    if "bolghar" not in LOCATION_GRANTS["BLH"]:
        sys.exit("_CENTRALASIA_RULES: BLH must hold bolghar")

    # Rus Tier 1 resolves the same way (package counts re-verified at
    # review: sweep finals 192/127/130/152/56; the recipients' own
    # holdings inside the sweeps are no-op re-grants). EXTEND, never
    # assign — the France lesson.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_RUS_RULES.items()):
        got = _resolve_ruleset(f"_RUS_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_RUS_RULES[{_t}]: resolved {len(got)} locations, "
                     f"package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    # PYS is absent below: its capital pereiaslav rides its own
    # NEW_COUNTRIES block + LOCATION_TRANSFERS, minus'd from the sweep.
    for _t, _cap in (("KIE", "kyiv"), ("CHR", "chernihiv"),
                     ("NOV", "novgorod"), ("POK", "polotsk")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_RUS_RULES: {_t} capital {_cap} not in its "
                     "resolved list")

    # Arabia resolves the same way (package count re-verified: QMT 28 =
    # JRW's 25 whole + ORM's manama/sayhat + HLG's kazimah); the plain
    # grant lists land as-is. EXTEND is REQUIRED, not caution: HLL is
    # already a Seljuk-resolution recipient (its kufa_province 7) and a
    # bare assign here would silently drop that list — the France
    # lesson, this time load-bearing.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_ARABIA_RULES.items()):
        got = _resolve_ruleset(f"_ARABIA_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_ARABIA_RULES[{_t}]: resolved {len(got)} "
                     f"locations, package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    for _t, locs in sorted(_ARABIA_GRANTS.items()):
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + list(locs)
    for _t, _cap in (("QMT", "al_ahsa"), ("UKH", "al_yamamah")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_ARABIA: {_t} capital {_cap} not in its list")

    # Rus Tier 2: the Cumans resolve the same way (package counts:
    # core 169 + don 42 = 211; donors GLH/HAL/KIE/GAZ).
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_RUS2_RULES.items()):
        got = _resolve_ruleset(f"_RUS2_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_RUS2_RULES[{_t}]: resolved {len(got)} locations, "
                     f"package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    if "izium" not in LOCATION_GRANTS["CUM"]:
        sys.exit("_RUS2_RULES: CUM capital izium not in its resolved list")

    # China-East: the Punjab to the Ghaznavids — DLH's 97 punjab_area
    # holdings, Ibrahim's Indian half (Lahore was the second capital
    # and the raid engine). SNAPSHOT-intersected: a bare area sweep
    # would also strip SND and the other Punjab holders. EXTEND — GHZ
    # already carries its Seljuk-slice 34.
    _m_all, _ = _defs()
    _punjab = sorted(set(_m_all["punjab_area"]) & set(_owned_by(src, "DLH")))
    if len(_punjab) != 97:
        sys.exit(f"CHINA-EAST: DLH's punjab holdings resolved to "
                 f"{len(_punjab)}, expected 97")
    LOCATION_GRANTS["GHZ"] = LOCATION_GRANTS.get("GHZ", []) + _punjab
    for _t, locs in sorted(_CHINA_GRANTS.items()):
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + list(locs)

    # Northern Dynasties resolve the same way (package counts: LIA
    # Tier A 161 + Tier B 149 = 310; XIA 48 — donors CHI 242, SYG 27,
    # the hordes 88, BAT's niuquanzi to XIA).
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_NORTH_RULES.items()):
        got = _resolve_ruleset(f"_NORTH_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_NORTH_RULES[{_t}]: resolved {len(got)} locations, "
                     f"package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    for _t, _cap in (("LIA", "linhuang"), ("XIA", "ningxia")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_NORTH_RULES: {_t} capital {_cap} not in its "
                     "resolved list")
    for _must in ("dadu", "liaoyang", "daning_pingquan", "datong_datong"):
        if _must not in LOCATION_GRANTS["LIA"]:
            sys.exit(f"_NORTH_RULES: LIA must hold {_must} — the Five "
                     "Capitals are the slice's spine")

    # India Tier 1 resolves the same way (fourteen rule sets, package
    # counts independently reproduced; 13 of the 576 are same-tag
    # no-op re-grants, 563 change owner; zero pairwise overlaps).
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_INDIA_RULES.items()):
        got = _resolve_ruleset(f"_INDIA_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_INDIA_RULES[{_t}]: resolved {len(got)} locations, "
                     f"package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    for _t, _cap in (("COZ", "thanjavur"), ("CLK", "kalyani"),
                     ("PAA", "monghyr"), ("PMR", "dhar"),
                     ("CHU", "patan")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_INDIA_RULES: {_t} capital {_cap} not in its "
                     "resolved list")

    # The Baltic resolves the same way (twelve rule sets, 176 total;
    # zero =UNOWNED= donors, so nothing joins the pop-line class).
    # EXTEND, never assign — POL, RAW, NRK and UFF are landed
    # recipients, the France lesson. Requires CONTROL_STRIPS below:
    # without it the six own_core/control doubles die in
    # _remove_owned_many with `occurrences != 1`.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_BALTIC_RULES.items()):
        got = _resolve_ruleset(f"_BALTIC_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_BALTIC_RULES[{_t}]: resolved {len(got)} "
                     f"locations, package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    for _t, _cap in (("PRS", "fischhausen"), ("SUD", "suwalki"),
                     ("KUO", "grobina"), ("ZEM", "dobele"),
                     ("LTG", "koknese"), ("ESO", "tartu"),
                     ("AUK", "kernave"), ("SXM", "raseiniai")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_BALTIC_RULES: {_t} capital {_cap} not in its "
                     "resolved list")

    # Africa resolves the same way (fourteen rule sets, 176 total with
    # the Gambia; zero vacates — the nine unowned Adrar locations SNH
    # absorbs SHRINK the pop-line class). EXTEND, never assign — GHA,
    # MAL, TKR, SON, ZGH, MDI, WAR, MAK, ALO are landed recipients.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_AFRICA_RULES.items()):
        got = _resolve_ruleset(f"_AFRICA_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_AFRICA_RULES[{_t}]: resolved {len(got)} "
                     f"locations, package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    for _t, locs in sorted(_AFRICA_GRANTS.items()):
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + list(locs)
    for _t, _cap in (("DJN", "djenne"), ("SNH", "aoudaghost"),
                     ("GHA", "koumbi_saleh"), ("MDI", "mogadishu")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_AFRICA_RULES: {_t} capital {_cap} not in its "
                     "resolved list")

    # Southeast Asia resolves the same way (sixteen rule sets, 249
    # total; zero vacates, zero UNOWNED_GRANTS — the review measured
    # every granted location at exactly ONE ownership entry with this
    # file's own reader, refuting the package's ten "unowned" Khorat/
    # Mekong phantoms). EXTEND, never assign — KHM, LAV, MUA, PNI,
    # INR, PHY, PUA, KTG, CHH, LGE, TDO and KIM are landed recipients,
    # and LAV/PHY/PUA/KTG/CHH/MUA/INR/LGE self-grants ride the
    # GHA/koumbi_saleh precedent.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_SEA_RULES.items()):
        got = _resolve_ruleset(f"_SEA_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_SEA_RULES[{_t}]: resolved {len(got)} "
                     f"locations, package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    for _t, _cap in (("PGN", "pagan"), ("HPJ", "lamphun"),
                     ("KDR", "daha"), ("JGL", "surabaya")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_SEA_RULES: {_t} capital {_cap} not in its "
                     "resolved list")

    # Tibet resolves the same way (five rule sets, 58 total; zero
    # UNOWNED_GRANTS — every granted location measured at exactly one
    # ownership entry with the full ten-key reader, by the package AND
    # by the review independently). EXTEND, never assign — GUG and NBH
    # are landed recipients. 52 from TIB + 6 from CHI; TIB's other 7
    # go through LOCATION_VACATED, and 52 + 7 = 59 = its whole holding.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_TIBET_RULES.items()):
        got = _resolve_ruleset(f"_TIBET_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_TIBET_RULES[{_t}]: resolved {len(got)} "
                     f"locations, package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    for _t, _cap in (("DBU", "lhasa"), ("GTS", "shigatse"),
                     ("TKA", "xining")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_TIBET_RULES: {_t} capital {_cap} not in its "
                     "resolved list")

    # The Americas resolve the same way (two singles rules, 3 total;
    # zero vacates, zero UNOWNED_GRANTS — every granted location
    # measured at exactly one ownership entry with the ten-key reader,
    # by the package AND the review independently). EXTEND, never
    # assign — TEP and KKE are landed recipients; both keep their
    # capitals (azcapotzalco, yanahuara) untouched.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_AMERICAS_RULES.items()):
        got = _resolve_ruleset(f"_AMERICAS_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_AMERICAS_RULES[{_t}]: resolved {len(got)} "
                     f"locations, package count is {_exp}")
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got

    # The France demesne resolves the same way. STRICT construction:
    # the minus lists exclude every swept-province member the DONORS do
    # not own (including the recipients' own holdings — saintes and
    # oleron are AQN's already, ventadour VNT's, narbonne NRB's), so
    # every resolved list contains ONLY donor land (FRA + the four
    # approved moves from AMG/VDM/FRZ). If a vanilla patch shifts any
    # ownership, the exact-once assert in _remove_owned_many dies.
    for _t, (_sw, _si, _ms, _ml, _exp) in sorted(_FRANCE_RULES.items()):
        got = _resolve_ruleset(f"_FRANCE_RULES[{_t}]", _sw, _si, _ms, _ml)
        if len(got) != _exp:
            sys.exit(f"_FRANCE_RULES[{_t}]: resolved {len(got)} locations, "
                     f"package count is {_exp}\n  resolved: {' '.join(got)}")
        # EXTEND, never assign: Germany II grants FLA the seven Artois
        # locations statically, and a bare assignment here would silently
        # drop them (the resolved list is only the FRA-donor part). The
        # disjointness and exactly-once asserts below cover the reverse
        # risk of a location entering twice.
        LOCATION_GRANTS[_t] = LOCATION_GRANTS.get(_t, []) + got
    for _t, _cap in (("TOU", "toulouse"), ("VLS", "soissons"),
                     ("BER", "bourges"), ("VMD", "saint_quentin")):
        if _cap not in LOCATION_GRANTS[_t]:
            sys.exit(f"_FRANCE_RULES: {_t} capital {_cap} not in its "
                     "resolved list")

    # No recipient may be a STEPPE HORDE: the horde name branch ignores
    # the NAME key entirely (the JAL law). The original assert also
    # banned tribes as a cautious generalization; the British slice
    # MEASURED it: country_name_construction.txt contains ZERO tribe
    # branches (grep "tribe" = no matches), and the landed Gaelic
    # tribes render their names in game (LEI "Leinster", batch-tested).
    # Tribes are now legal recipients — the whole Irish pass is grants
    # to them. Detection also follows TEMPLATE-carried types now: the
    # old in-block-only scan could never see a type an include brought
    # in (gaelic_tribe carries `type = tribe` for every Irish tag).
    _TPLTYPE_CACHE = {}
    def _tpl_type(inc):
        if inc not in _TPLTYPE_CACHE:
            p = os.path.join(VAN, "main_menu", "setup", "templates",
                             inc + ".txt")
            t = None
            if os.path.isfile(p):
                b = re.sub(r"#[^\n]*", "",
                           open(p, encoding="utf-8-sig").read())
                m2 = re.search(r"^[ \t]*type[ \t]*=[ \t]*(\w+)", b, re.M)
                if m2:
                    t = m2.group(1)
                else:
                    for mi in re.finditer(
                            r'^[ \t]*include[ \t]*=[ \t]*"?([A-Za-z0-9_]+)"?',
                            b, re.M):
                        t = t or _tpl_type(mi.group(1))
            _TPLTYPE_CACHE[inc] = t
        return _TPLTYPE_CACHE[inc]

    _blocks_h = list(re.finditer(COUNTRY_RE, src, re.M))
    _horde_tags = set()
    for i, m in enumerate(_blocks_h):
        _e = _blocks_h[i + 1].start() if i + 1 < len(_blocks_h) else len(src)
        _b = src[m.start():_e]
        if re.search(r"^[ \t]*type = steppe_horde[ \t]*$", _b, re.M):
            _horde_tags.add(m.group(1))
            continue
        if not re.search(r"^[ \t]*type = \w+", _b, re.M):
            for mi in re.finditer(r'include = "([^"]+)"', _b):
                if _tpl_type(mi.group(1)) == "steppe_horde":
                    _horde_tags.add(m.group(1))
                    break
    _bad_recip = (set(LOCATION_TRANSFERS) | set(LOCATION_GRANTS)) & _horde_tags
    if _bad_recip:
        sys.exit(f"steppe-horde recipients forbidden: {sorted(_bad_recip)}")

    # No location may appear in TWO different tags' transfer/grant lists:
    # the second grant would silently re-take it from the first (sorted
    # order decides the winner) and every per-location assert would still
    # pass. Found as a blind spot in the end-of-day audit — nothing had
    # fired, but the class is silent by construction.
    _list_owner = {}
    for _t, locs in list(LOCATION_TRANSFERS.items()) + list(LOCATION_GRANTS.items()):
        for l in locs:
            if l in _list_owner and _list_owner[l] != _t:
                sys.exit(f"{l} is listed for both {_list_owner[l]} and {_t} "
                         f"— transfer/grant lists must be disjoint")
            _list_owner[l] = _t

    # Occupations cleared (the Baltic slice's CONTROL_STRIPS): delete
    # each tag's `control = { ... }` block after asserting its token
    # list equals the declared list EXACTLY — a vanilla patch that
    # changes the occupation fails loudly instead of silently under-
    # or over-stripping. Must run BEFORE the _landless_claims snapshot
    # below AND before any grant touches the occupied locations (the
    # exactly-once assert in _remove_owned_many reads `control` too).
    n_strips = 0
    for _t, _locs in sorted(CONTROL_STRIPS.items()):
        blocks_cs = list(re.finditer(COUNTRY_RE, src, re.M))
        for i, b in enumerate(blocks_cs):
            if b.group(1) != _t:
                continue
            end = blocks_cs[i + 1].start() if i + 1 < len(blocks_cs) else len(src)
            body = src[b.start():end]
            m = re.search(r"^[ \t]*control[ \t]*=[ \t]*\{", body, re.M)
            if not m:
                sys.exit(f"CONTROL_STRIPS: {_t} has no control block — "
                         "vanilla changed, re-verify the occupation")
            bo = body.index("{", m.start())
            be = find_block_end(body, bo)
            toks = re.findall(r"[a-z][A-Za-z0-9_]*",
                              re.sub(r"#[^\n]*", "", body[bo + 1:be]))
            if sorted(toks) != sorted(_locs):
                sys.exit(f"CONTROL_STRIPS[{_t}]: control block holds "
                         f"{sorted(toks)}, declared {sorted(_locs)} — "
                         "vanilla changed, re-verify the occupation")
            src = src[:b.start()] + body[:m.start()] + body[be:] + src[end:]
            n_strips += len(toks)
            break
        else:
            sys.exit(f"CONTROL_STRIPS: tag {_t} not found")
    report.append(("occupations cleared (control blocks stripped)", n_strips))

    # DERIVED from LANDLESS_AFTER, not enumerated per slice. The old
    # per-slice enumeration was a second parallel list, and Italy North
    # updated one but not the other: its eighteen donors went landless
    # with NO claims written, and the engine said so at start
    # (initialize_from_bookmark.cpp:592, seventeen lines, first
    # user-observed 2026-07-30 — LUN passed because Germany II WAS in
    # both lists; SAL's single claim was vanilla's own). GRA/POR/MLL
    # are excluded because their claims are the explicit
    # DISPLACED_CLAIMS lists, byte-for-byte vanilla's.
    _landless_claims = {t: _owned_by(src, t)
                        for t in LANDLESS_AFTER
                        if t not in DISPLACED_CLAIMS}
    for _t, _held in _landless_claims.items():
        if not _held:
            sys.exit(f"LANDLESS list: {_t} already holds nothing — stale entry")

    n_transferred = 0
    for _t, locs in sorted(LOCATION_TRANSFERS.items()):
        src = _remove_owned_many(src, locs, f"LOCATION_TRANSFERS[{_t}]")
        n_transferred += len(locs)
    report.append(("locations transferred to new countries", n_transferred))
    wrap = src.rindex("\n}\n}")
    src = src[:wrap] + "\n" + "\n".join(NEW_COUNTRIES[t] for t in sorted(NEW_COUNTRIES)) + src[wrap:]
    report.append(("new countries inserted", len(NEW_COUNTRIES)))

    # Grants to EXISTING tags: remove from the current owner, write into
    # the target's own_control_core (created when the tag is landless),
    # and drop the granted locations from the target's own claims list.
    # UNOWNED_GRANTS members skip the removal (they have no owner to
    # remove from) after both asserts below.
    _uidx = _ownership_index(src, {l for v in UNOWNED_GRANTS.values()
                                   for l in v})
    for _t, _locs in sorted(UNOWNED_GRANTS.items()):
        _bad = [l for l in _locs if len(_uidx.get(l, [])) != 0]
        if _bad:
            sys.exit(f"UNOWNED_GRANTS[{_t}]: {_bad[:8]} already have an "
                     "owner — vanilla changed, re-verify (the strip "
                     "belongs in the normal grant path now)")
        _miss = [l for l in _locs if l not in LOCATION_GRANTS.get(_t, [])]
        if _miss:
            sys.exit(f"UNOWNED_GRANTS[{_t}]: {_miss[:8]} not in the "
                     "tag's resolved grant list — stale entry")
    _unowned_all = {l for v in UNOWNED_GRANTS.values() for l in v}
    report.append(("unowned locations granted an owner",
                   len(_unowned_all)))
    n_granted, n_unclaimed = 0, 0
    for _t, locs in sorted(LOCATION_GRANTS.items()):
        src = _remove_owned_many(src, [l for l in locs
                                       if l not in _unowned_all],
                                 f"LOCATION_GRANTS[{_t}]")
        blocks_g = list(re.finditer(COUNTRY_RE, src, re.M))
        for i, b in enumerate(blocks_g):
            if b.group(1) != _t:
                continue
            end = blocks_g[i + 1].start() if i + 1 < len(blocks_g) else len(src)
            body = src[b.start():end]
            m = re.search(r"^([ \t]*)own_control_core[ \t]*=[ \t]*\{", body, re.M)
            if m:
                at = b.start() + body.index("{", m.start()) + 1
                src = src[:at] + "\n" + m.group(1) + "\t" + " ".join(locs) + src[at:]
            else:
                at = b.start() + body.index("{") + 1
                src = (src[:at] + "\n\t\town_control_core = {\n\t\t\t"
                       + " ".join(locs) + "\n\t\t}\n" + src[at:])
            n_granted += len(locs)
            break
        else:
            sys.exit(f"LOCATION_GRANTS: tag {_t} not found")
        # claims cleanup, lenient: a granted location not in the claims
        # list is fine, it is just counted
        blocks_g = list(re.finditer(COUNTRY_RE, src, re.M))
        for i, b in enumerate(blocks_g):
            if b.group(1) != _t:
                continue
            end = blocks_g[i + 1].start() if i + 1 < len(blocks_g) else len(src)
            body = src[b.start():end]
            cm = re.search(r"^[ \t]*our_cores_conquered_by_others[ \t]*=[ \t]*\{", body, re.M)
            if cm:
                cend = find_block_end(body, body.index("{", cm.start()))
                seg = body[cm.start():cend]
                seg2 = seg
                for loc in locs:
                    seg2, k = re.subn(r"(?<=[\s])" + re.escape(loc) + r"(?=[\s])", "", seg2)
                    if not k:
                        n_unclaimed += 1
                src = src[:b.start() + cm.start()] + seg2 + src[b.start() + cend:]
            break
    report.append(("locations granted to existing tags", n_granted))
    if n_unclaimed:
        report.append(("  of those, not in the target's claims", n_unclaimed))

    # LOCATION_VACATED (user-approved 2026-08-01): remove from the owner,
    # write NOTHING back — the location ends owned by nobody, a state
    # vanilla ships 7334 times. Runs AFTER the _landless_claims snapshot
    # (CHG's claims must include its vacated Dzungarian holdings) and
    # after the grants. Resolution is (name members) ∩ (the tag's CURRENT
    # holdings): a definitions-resolved list would include already-unowned
    # members and trip _remove_owned_many's exactly-once assert.
    _members_v, _ = _defs()
    _vac_resolved = {}
    for _t, _names in sorted(LOCATION_VACATED.items()):
        _pool = set()
        for _n in _names:
            if _n not in _members_v:
                sys.exit(f"LOCATION_VACATED[{_t}]: {_n} is not a region/"
                         "area/province in definitions.txt")
            _pool |= set(_members_v[_n])
        got = sorted(_pool & set(_owned_by(src, _t)))
        if len(got) != LOCATION_VACATED_EXPECT[_t]:
            sys.exit(f"LOCATION_VACATED[{_t}]: resolved {len(got)} owned "
                     f"locations, expected "
                     f"{LOCATION_VACATED_EXPECT[_t]}")
        for l in got:
            if l in _list_owner:
                sys.exit(f"LOCATION_VACATED[{_t}]: {l} is also in "
                         f"{_list_owner[l]}'s transfer/grant list — vacate "
                         "and grant lists must be disjoint")
        _vac_resolved[_t] = got
    n_vacated = 0
    for _t, locs in sorted(_vac_resolved.items()):
        src = _remove_owned_many(src, locs, f"LOCATION_VACATED[{_t}]")
        n_vacated += len(locs)
    report.append(("locations vacated to no owner", n_vacated))

    # Displaced-tag bookkeeping. Claims are written into the tag's EXISTING
    # our_cores_conquered_by_others (GRA has one, holding olvera), and the
    # landless guarantee then proves the transfers emptied every ownership
    # list — a missed 19th location would leave a stray holding and quietly
    # break the "GRA is the future, not the present" story.
    n_claims = 0
    _all_claims = dict(DISPLACED_CLAIMS)
    _all_claims.update(_landless_claims)
    for _t, locs in sorted(_all_claims.items()):
        blocks_d = list(re.finditer(COUNTRY_RE, src, re.M))
        for i, b in enumerate(blocks_d):
            if b.group(1) != _t:
                continue
            end = blocks_d[i + 1].start() if i + 1 < len(blocks_d) else len(src)
            body = src[b.start():end]
            cm = re.search(r"^([ \t]*)our_cores_conquered_by_others[ \t]*=[ \t]*\{", body, re.M)
            if cm:
                at = b.start() + body.index("{", cm.start()) + 1
                src = src[:at] + "\n" + cm.group(1) + "\t" + " ".join(locs) + src[at:]
            else:
                # POR and MLL own everything they want at 1337 and ship no
                # claims block — create one, like grants create ownership.
                at = b.start() + body.index("{") + 1
                src = (src[:at] + "\n\t\tour_cores_conquered_by_others = {\n\t\t\t"
                       + " ".join(locs) + "\n\t\t}\n" + src[at:])
            n_claims += len(locs)
            break
        else:
            sys.exit(f"DISPLACED_CLAIMS: tag {_t} not found")
    report.append(("claims written onto displaced tags", n_claims))
    for _t in LANDLESS_AFTER:
        blocks_d = list(re.finditer(COUNTRY_RE, src, re.M))
        for i, b in enumerate(blocks_d):
            if b.group(1) != _t:
                continue
            end = blocks_d[i + 1].start() if i + 1 < len(blocks_d) else len(src)
            body = src[b.start():end]
            for key in OWN_KEYS:
                for m in re.finditer(r"^[ \t]*" + key + r"[ \t]*=[ \t]*\{", body, re.M):
                    bo = body.index("{", m.start())
                    # comments stripped first: MLL's emptied block keeps
                    # vanilla's `#County of Cerdanya` notes, which are not
                    # holdings. Token regex admits interior capitals —
                    # targoviste_BUL and trgoviste_SER are real locations.
                    inner = re.sub(r"#[^\n]*", "",
                                   body[bo + 1:find_block_end(body, bo)])
                    toks = re.findall(r"[a-z][A-Za-z0-9_]*", inner)
                    if toks:
                        sys.exit(f"LANDLESS_AFTER: {_t} still owns {toks[:5]}")
            # THE CHECK the 2026-07-30 game test showed was missing: a
            # landless tag must also carry a NON-EMPTY claims list, or
            # the engine rejects it at start ("does not exist, nor has
            # cores as a revolter", initialize_from_bookmark.cpp:592).
            # Verifying zero holdings alone let eighteen claim-less
            # shells ship. Proven by breaking (one tag excluded from
            # _landless_claims -> this line fired).
            _cm = re.search(
                r"^[ \t]*our_cores_conquered_by_others[ \t]*=[ \t]*\{",
                body, re.M)
            _ctoks = []
            if _cm:
                _co = body.index("{", _cm.start())
                _ctoks = re.findall(
                    r"[a-z][A-Za-z0-9_]*",
                    re.sub(r"#[^\n]*", "",
                           body[_co + 1:find_block_end(body, _co)]))
            if not _ctoks:
                sys.exit(f"LANDLESS_AFTER: {_t} is landless with NO "
                         "claims — the engine will reject it at start "
                         "(initialize_from_bookmark.cpp:592)")
            break
        else:
            sys.exit(f"LANDLESS_AFTER: tag {_t} not found")
    report.append(("displaced tags verified landless, claims-backed",
                   len(LANDLESS_AFTER)))

    # THE BALTIC BREAK-TEST'S FINDING (e), 2026-08-01: the guard above
    # inspects only LANDLESS_AFTER members — a tag EMPTIED by grants
    # but never listed shipped a green build as a claimless shell the
    # engine rejects at start (RIG, observed deliberately; KLB nearly
    # shipped the same way from the Arabia package). Delta sweep,
    # validate-ours/report-theirs: every tag that holds land in
    # PRISTINE vanilla must either still hold land or sit in
    # LANDLESS_AFTER. Pop countries and vanilla's own landless shells
    # hold nothing in pristine and are excluded by construction.
    # Proven by breaking: RIG removed from BALTIC_LANDLESS -> this
    # exit, restored (same day).
    def _held_index(s):
        out = {}
        blocks_hi = list(re.finditer(COUNTRY_RE, s, re.M))
        for i, b in enumerate(blocks_hi):
            end = blocks_hi[i + 1].start() if i + 1 < len(blocks_hi) else len(s)
            body = s[b.start():end]
            n = 0
            for key in OWN_KEYS:
                for m in re.finditer(r"^[ \t]*" + key + r"[ \t]*=[ \t]*\{",
                                     body, re.M):
                    bo = body.index("{", m.start())
                    inner = re.sub(r"#[^\n]*", "",
                                   body[bo + 1:find_block_end(body, bo)])
                    n += len(re.findall(r"[a-z][A-Za-z0-9_]*", inner))
            out[b.group(1)] = out.get(b.group(1), 0) + n
        return out
    _held_pre = _held_index(_pristine)
    _emptied = sorted(t for t, n in _held_index(src).items()
                      if not n and _held_pre.get(t, 0)
                      and t not in LANDLESS_AFTER)
    if _emptied:
        sys.exit(f"emptied but not in LANDLESS_AFTER: {_emptied} — these "
                 "tags held land in vanilla, hold none now, and carry no "
                 "derived claims; the engine rejects them at start "
                 "(initialize_from_bookmark.cpp:592, the RIG/KLB class)")
    report.append(("tags emptied by us verified listed (delta)",
                   len(_held_pre)))

    # TRE surgery: the 1204.4.1 themata bureaucracy records the founding
    # of an empire that does not exist in 1066, and the Grand-Komnenoi
    # regnal counts are the same 1204+ inflation the BYZ REGNAL_FIXES
    # corrected. Both blocks go — and with them the build's LAST
    # KNOWN_FUTURE exemption: the date audit now runs with zero.
    blocks_t = list(re.finditer(COUNTRY_RE, src, re.M))
    for i, b in enumerate(blocks_t):
        if b.group(1) != "TRE":
            continue
        end = blocks_t[i + 1].start() if i + 1 < len(blocks_t) else len(src)
        body = src[b.start():end]
        for key, must in (("bureaucracies", "1204.4.1"),
                          ("regnal_numbers", "name_alexis")):
            m = re.search(r"^[ \t]*" + key + r"[ \t]*=[ \t]*\{", body, re.M)
            if not m:
                sys.exit(f"TRE surgery: no {key} block found")
            bo = body.index("{", m.start())
            be = find_block_end(body, bo)
            if must not in body[m.start():be]:
                sys.exit(f"TRE surgery: {key} lacks `{must}` — vanilla changed, re-verify")
            body = body[:m.start()] + body[be:]
        src = src[:b.start()] + body + src[end:]
        break
    else:
        sys.exit("TRE surgery: tag TRE not found")
    report.append(("TRE future-dated blocks removed", 2))

    # Capital corrections, asserted against the expected old value.
    # Blocks are RE-SCANNED per tag: a fix that changes the block's length
    # would silently stale every later offset otherwise.
    n_cap = 0
    for _t, (old_cap, new_cap) in sorted(CAPITAL_FIXES.items()):
        starts_cf = list(re.finditer(COUNTRY_RE, src, re.M))
        for i, b in enumerate(starts_cf):
            if b.group(1) != _t:
                continue
            end = starts_cf[i + 1].start() if i + 1 < len(starts_cf) else len(src)
            body, k = re.subn(r"(^[ \t]*capital[ \t]*=[ \t]*)" + old_cap + r"\b",
                              lambda mm, nc=new_cap: mm.group(1) + nc,
                              src[b.start():end], count=1, flags=re.M)
            if not k:
                sys.exit(f"CAPITAL_FIXES: capital {old_cap} not found in {_t}")
            src = src[:b.start()] + body + src[end:]
            n_cap += 1
            break
        else:
            sys.exit(f"CAPITAL_FIXES: tag {_t} not found")
    report.append(("capitals corrected", n_cap))

    # Field surgery on existing blocks (the CAPITAL_FIXES shape,
    # generalized): each old line must appear EXACTLY ONCE in its tag's
    # block, or the build dies — a vanilla patch that rewords the field
    # fails loudly instead of silently skipping the fix.
    n_fields = 0
    for _t, fixes in sorted(FIELD_FIXES.items()):
        starts_ff = list(re.finditer(COUNTRY_RE, src, re.M))
        for i, b in enumerate(starts_ff):
            if b.group(1) != _t:
                continue
            end = starts_ff[i + 1].start() if i + 1 < len(starts_ff) else len(src)
            body = src[b.start():end]
            for old_line, new_line in fixes:
                k = body.count(old_line)
                if k != 1:
                    sys.exit(f"FIELD_FIXES: `{old_line}` appears {k}x in {_t} — expected exactly once")
                body = body.replace(old_line, new_line, 1)
                n_fields += 1
            src = src[:b.start()] + body + src[end:]
            break
        else:
            sys.exit(f"FIELD_FIXES: tag {_t} not found")
    report.append(("fields corrected in existing blocks", n_fields))

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
        # (?<![A-Za-z0-9_]) instead of a line anchor: the 23 one-line
        # `government = { ruler = ... }` blocks keep their ruler mid-line,
        # and the anchored form double-inserted into every one of them.
        # Comment-stripped first: NTC ships `#ruler = jap_koumyou_tenno`
        # and the widened search skipped it on the first run — leaving NTC
        # with no ruler at all.
        if re.search(r"(?<![A-Za-z0-9_])ruler[ \t]*=",
                     re.sub(r"#[^\n]*", "", body)):
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
        ("SIC", "name_roger"): 0,         # Roger I is our seated term's regnal 1; the table's 3 is Hohenstaufen-era (Italy slice)
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
        # PAP's 37-name table, the undisputed seventeen (Italy pass, F10).
        # Deliberately NOT touched: name_benedict, name_boniface, name_john
        # — antipope-numbering disputes, second source owed.
        ("PAP", "name_alexander"): 2,     # Alexander II reigns NOW
        ("PAP", "name_adrian"): 3,
        ("PAP", "name_anastasius"): 3,
        ("PAP", "name_callisto"): 1,
        ("PAP", "name_celestine"): 1,
        ("PAP", "name_clement"): 2,
        ("PAP", "name_eugene"): 2,
        ("PAP", "name_gelasius"): 1,
        ("PAP", "name_gregory"): 6,       # Gregory VII arrives 1073
        ("PAP", "name_honorius"): 1,      # the antipope claims II — situation material
        ("PAP", "name_innocent"): 1,
        ("PAP", "name_lucius"): 1,
        ("PAP", "name_martin"): 1,
        ("PAP", "name_nicholas"): 2,
        ("PAP", "name_paschal"): 1,
        ("PAP", "name_urban"): 1,
        ("PAP", "name_victor"): 2,
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

    for tag, row in sorted(HISTORICAL_RULERS.items()):
        char, accession, regnal = row[:3]
        rname = row[3] if len(row) > 3 else None
        term = (f"ruler_term = {{ character = {char} start_date = {accession} "
                f"regnal_number = {regnal}"
                + (f" regnal_name = {rname}" if rname else "") + " }")
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
        if after != before + len(NEW_COUNTRIES):
            return (f"country count {after} != {before} + {len(NEW_COUNTRIES)} "
                    f"new — territory would be lost or a block failed to land")
        # Transfer/grant exclusivity: every moved location must end owned
        # exactly once, measured by the same ownership-block parser that
        # moved it.
        moved = [l for _, ls in list(LOCATION_TRANSFERS.items())
                 + list(LOCATION_GRANTS.items()) for l in ls]
        _midx = _ownership_index(src, set(moved))
        for loc in moved:
            n_now = len(_midx.get(loc, []))
            if n_now != 1:
                return f"{loc}: {n_now} owners after the move — must be exactly 1"
        # Vacated locations are the ONE class the exactly-once rule must
        # NOT cover: they must end owned by NOBODY. Kept separate from
        # `moved` above by construction (disjointness asserted at
        # resolution). Proven by breaking BOTH ways (2026-08-01): a bogus
        # name aborts at resolution, and skipping GLH's removal made THIS
        # line fire — GLH stays landed, so this is its only catcher (a
        # landless donor like CHG is caught earlier by the LANDLESS_AFTER
        # still-owns guard, which the same break test also exercised).
        _vac_all = [l for ls in _vac_resolved.values() for l in ls]
        _vidx = _ownership_index(src, set(_vac_all))
        for loc in _vac_all:
            if _vidx.get(loc):
                return (f"vacated location {loc} still has an owner — the "
                        "vacate pass did not run or something re-granted it")
        for key in COUNTRY_BLOCKS + COUNTRY_LINES:
            if key == "ruler_term":
                continue    # vanilla's are stripped; OURS are re-added and audited below
            if re.search(r"^[ \t]*" + key + r"[ \t]*=", src, re.M):
                return f"{key} survived the strip"
        # Every remaining ruler must be random or a Phase 2 entry. This is the
        # check that catches a ruler line whose shape differs just enough to miss
        # the rewrite and leave that country a -250-year-old. UNANCHORED on
        # comment-stripped text: the line-anchored form was blind to the 23
        # one-line `government = { ruler = X }` blocks, which is exactly how
        # AOS's 1291-born sav_aymon_savoy shipped behind an injected
        # `ruler = random` in the same line (Italy North review, 2026-07-29).
        chars = {r[0] for r in HISTORICAL_RULERS.values()}
        src_nc = re.sub(r"#[^\n]*", "", src)
        stray = [m.group(1) for m in
                 re.finditer(r"(?<![A-Za-z0-9_])ruler[ \t]*=[ \t]*([A-Za-z0-9_]+)",
                             src_nc)
                 if m.group(1) != "random" and m.group(1) not in chars]
        if stray:
            return f"{len(stray)} ruler(s) still name a character: {stray[:8]}"
        # Exactly one per country: more can outrank a Phase 2 ruler, fewer means
        # an empty throne and an engine-generated regent.
        s2 = list(re.finditer(COUNTRY_RE, src_nc, re.M))
        bad = []
        for i, m in enumerate(s2):
            e = s2[i + 1].start() if i + 1 < len(s2) else len(src_nc)
            if len(re.findall(r"(?<![A-Za-z0-9_])ruler[ \t]*=",
                              src_nc[m.start():e])) != 1:
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
            e = s2[i + 1].start() if i + 1 < len(s2) else len(src_nc)
            r = re.findall(r"(?<![A-Za-z0-9_])ruler = ([a-z_0-9]+)",
                           src_nc[m.start():e])
            if r and r[0] != "random":
                placed[m.group(1)] = r[0]
        expected = {t: r[0] for t, r in HISTORICAL_RULERS.items()}
        if placed != expected:
            return (f"historical rulers landed in the wrong countries: "
                    f"expected {expected}, found {placed}")

        # Vanilla's ruler_terms are stripped and OURS are re-added; the two
        # motions must reconcile exactly. Every surviving term must be one we
        # generated: OPEN (no end_date), for a Phase 2 character.
        # Audit COMMENT-STRIPPED text: vanilla ships 60 commented-out
        # ruler_terms (dates and all) that the parser never sees.
        nc = re.sub(r"#[^\n]*", "", src)
        accessions = {r[0]: r[1] for r in HISTORICAL_RULERS.values()}
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
        # EMPTY since the Byzantium slice retired the TRE 1204.4.1
        # exemption by deleting the block itself — the audit now tolerates
        # ZERO future dates from any source. Kept as a set so a future
        # genuinely-unfixable case has somewhere documented to go.
        KNOWN_FUTURE = set()
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

        # No capital may be stripped without a CAPITAL_FIXES repoint. The
        # audit-D1 nine all arrived exactly this way — six through
        # area/province sweeps that never name a location, so no reviewer
        # ever saw the capital go. Delta against PRISTINE vanilla: a tag
        # vanilla already ships orphaned (10 of them) is theirs to fix,
        # not a build failure here.
        def _orphan_capitals(text):
            t_nc = re.sub(r"#[^\n]*", "", text)
            t_bs = list(re.finditer(COUNTRY_RE, t_nc, re.M))
            orphans = {}
            for i, m in enumerate(t_bs):
                e = t_bs[i + 1].start() if i + 1 < len(t_bs) else len(t_nc)
                body = t_nc[m.start():e]
                # [A-Za-z0-9_]: location ids can embed uppercase tag
                # suffixes (trgoviste_SER) — a lowercase-only class split
                # the token and produced a false orphan on first run.
                capm = re.search(r"^[ \t]*capital[ \t]*=[ \t]*([A-Za-z0-9_]+)",
                                 body, re.M)
                if not capm:
                    continue
                held = []
                for key in OWN_KEYS:
                    for om in re.finditer(
                            r"^[ \t]*" + key + r"[ \t]*=[ \t]*\{", body, re.M):
                        bo = body.index("{", om.start())
                        held.extend(re.findall(r"[a-z][A-Za-z0-9_]*",
                                               body[bo + 1:find_block_end(body, bo)]))
                if held and capm.group(1) not in held:
                    orphans[m.group(1)] = capm.group(1)
            return orphans
        _van_orph = _orphan_capitals(_pristine)
        _mod_orph = {t: c for t, c in _orphan_capitals(src).items()
                     if _van_orph.get(t) != c}
        if _mod_orph:
            return ("capitals stripped without a CAPITAL_FIXES repoint: "
                    + ", ".join(f"{t}->{c}"
                                for t, c in sorted(_mod_orph.items())[:8]))
        return None

    return src, report, validate, (f"{before} vanilla country blocks kept"
                                   f" + {len(NEW_COUNTRIES)} new = {after}")


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
    # THE MIDDLE KINGDOM RESTORE (India/China review Route B, verified
    # and user-approved 2026-08-01). The tusi gate is on the IO's
    # EXISTENCE — country_triggers.txt:1287 `exists =
    # international_organization:middle_kingdom` is the trigger body's
    # first statement, OUTSIDE the OR — so no reform can substitute:
    # Route A is provably dead. One re-date keeps the instance out of
    # the future-date strip below. 960.2.4 is the Song proclamation [U];
    # any pre-START_DATE value works mechanically, and this keeps the
    # IOs-dated-at-their-founding convention (catholic_church ships
    # 33.1.1). Its 12 ruler_terms died in the strip above; leader = CHI
    # and all 209 members stay (0 in LANDLESS_AFTER, verified). This
    # single restore closes THREE decoded classes at the root: the
    # CHA/DAI tributary downgrades (government.cpp:3702), the ~128 tusi
    # lines, and CHI's accepted-culture flood (country.cpp:9635 — the
    # leader_modifier's cultures_capacity = 50 returns).
    src, n_mk = re.subn(
        r"creation_date = 1271\.12\.18",
        "creation_date = 960.2.4 # 1271.12.18 re-dated: the Song founding [U]",
        src)
    if n_mk != 1:
        sys.exit(f"middle_kingdom re-date: expected exactly one "
                 f"creation_date = 1271.12.18, found {n_mk}")
    report.append(("middle_kingdom re-dated to the Song founding", n_mk))

    # The Coptic patriarchate of Alexandria (Africa slice, 2026-08-02):
    # at 1066 the bishops of Makuria and Alodia were consecrated in
    # Alexandria [U] — the Nubian church was a province of the Coptic
    # see for six centuries. members = { ETH } is the file's only
    # African IO membership (measured, all 80 theater tags scanned by
    # the package); depends on MAK's miaphysite registry flip, which
    # rides the horn_of_africa.txt override.
    src, n_alex = re.subn(
        r"^(\t+members = \{ )ETH( \})",
        lambda m: m.group(1) + "ETH MAK ALO" + m.group(2),
        src, flags=re.M)
    if n_alex != 1:
        sys.exit(f"Alexandria patriarchate: expected exactly one "
                 f"`members = {{ ETH }}` line, found {n_alex}")
    report.append(("Nubia joined the see of Alexandria", n_alex))

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

    # THE HIGH KINGSHIP LEADER (British slice, 2026-07-29). The IO is
    # character-led (high_kingship.txt:23 has_leader_country,
    # :26 leader_type = character) and derives the character from a
    # leader COUNTRY — the seeding syntax is `leader = <TAG>`, attested
    # by the structural twin catholic_church (its type definition :10/
    # :12 matches, its setup instance carries `leader = PAP`,
    # 15_international_organizations.txt:182). Vanilla's own chain
    # named Diarmait High King from 1064.8.22 (:303 — stripped with
    # every ruler_term above, lawfully); this restores the crown by
    # the country key. Member surgery rides along: Paradox's own rule
    # is that landless tags are not members (MTH and PLE are pointedly
    # absent from vanilla's list), so the three tags this slice
    # empties leave and the three it lands join — 27 before and after.
    _hk = re.search(r"^\tadd_international_organization = \{[^{}]*?"
                    r"type = high_kingship", src, re.M)
    if not _hk:
        sys.exit("high_kingship instance not found in 15_IO")
    _hk_end = find_block_end(src, src.index("{", _hk.start()))
    _hk_body = src[_hk.start():_hk_end]
    _mm = re.search(r"members[ \t]*=[ \t]*\{", _hk_body)
    if not _mm:
        sys.exit("high_kingship members block not found")
    _m_open = _hk_body.index("{", _mm.start())
    _m_end = find_block_end(_hk_body, _m_open)
    # comment-stripped: vanilla's list carries `#PLE` — its own note
    # that the landless Pale is excluded — and a raw split() counted
    # the comment tokens as members (measured: 29 vs the true 27).
    _members = re.sub(r"#[^\n]*", "",
                      _hk_body[_m_open + 1:_m_end - 1]).split()
    if len(_members) != 27:
        sys.exit(f"high_kingship: expected 27 vanilla members, found {len(_members)}")
    for _out in ("CLA", "THO", "CVN"):
        if _out not in _members:
            sys.exit(f"high_kingship: expected member {_out} to remove")
        _members.remove(_out)
    for _in in ("MTH", "DUB", "ULD"):
        if _in in _members:
            sys.exit(f"high_kingship: {_in} already a member")
        _members.append(_in)
    if len(_members) != 27:
        sys.exit("high_kingship: member surgery must conserve 27")
    _new_body = (_hk_body[:_m_open + 1] + "\n\t\t\t"
                 + " ".join(_members) + "\n\t\t"
                 + _hk_body[_m_end - 1:_m_end]
                 + "\n\t\tleader = LEI"
                 + _hk_body[_m_end:])
    src = src[:_hk.start()] + _new_body + src[_hk_end:]
    report.append(("High Kingship crowned (leader = LEI, members 27)", 1))

    # THE HRE CROWN (user decision D, 2026-07-29): Heinrich IV on a
    # landed OGK, styled by the HRE_LEADER loc overrides ("King of the
    # Romans" — the imperial coronation is 1084, an event hook). The
    # leaderless alternative was measured DEAD: hre_election.txt:17-21
    # goes live the moment the IO has no leader, and hre.txt:459-488
    # crowns the richest eligible member after two years — a headless
    # HRE elects a Habsburg. `leader = <TAG>` is the proven seed (the
    # High Kingship precedent); `emperor` is an auto-following special
    # status and must move with the leader. The electors lose the two
    # post-1066 constructs (SWB is Saxe-Wittenberg 1180+, PAL the 1214
    # Rhine Palatinate) for the Billung and Bavarian stem duchies [U];
    # the three archbishops and no_golden_bull_policy are already
    # 1066-exact (measured — vanilla's own pre-Bull law). OGK/CRH/STY
    # join the members (newly landed; imperial_prince auto-bestows).
    for _old, _new, _what in (
            ("leader = UBV", "leader = OGK", "HRE leader"),
            ("emperor = { UBV }", "emperor = { OGK }", "emperor status")):
        if src.count(_old) != 1:
            sys.exit(f"HRE surgery: {_what} pattern not exactly-once "
                     f"({src.count(_old)}x)")
        src = src.replace(_old, _new, 1)
    # The elector list is multi-line with per-line comments — parsed,
    # verified against the expected 1356-Bull four, rewritten as the
    # 1066 four.
    _em = re.search(r"elector[ \t]*=[ \t]*\{", src)
    _eo = src.index("{", _em.start())
    _ee = find_block_end(src, _eo)
    _etoks = re.sub(r"#[^\n]*", "", src[_eo + 1:_ee - 1]).split()
    if _etoks != ["BOH", "SWB", "BRA", "PAL"]:
        sys.exit(f"HRE surgery: elector list is {_etoks}, expected the "
                 "1356-Bull four")
    # Germany II moved the Billung seat off LUN and onto SAX, which is
    # the tag that actually holds the duchy now. HARD DEPENDENCY on the
    # landless sweep below: LUN joins LANDLESS_AFTER in the same change,
    # and a stale `LUN` here would simply be eaten by the ghost strip —
    # an elector silently deleted, exactly the class of failure the
    # sweep's exact-count assert exists to make loud.
    src = (src[:_eo + 1]
           + "\n\t\t\t\t# The 1066 four: Bohemia, the Nordmark, and the"
           + "\n\t\t\t\t# Billung and Bavarian stem duchies [U] — SWB is"
           + "\n\t\t\t\t# Saxe-Wittenberg (1180+), PAL the 1214 Palatinate."
           + "\n\t\t\t\tBOH BRA SAX UBV\n\t\t"
           + src[_ee - 1:])
    _hre = re.search(r"^\tadd_international_organization = \{[^{}]*?"
                     r"type = hre", src, re.M)
    if not _hre:
        sys.exit("hre instance not found in 15_IO")
    _hre_end = find_block_end(src, src.index("{", _hre.start()))
    _hb = src[_hre.start():_hre_end]
    _hm = re.search(r"members[ \t]*=[ \t]*\{", _hb)
    _ho = _hb.index("{", _hm.start())
    # SAX and SWA join with the HRE slice's three: the two stem duchies
    # are landed as of Germany II, and the thirteen tags that slice
    # empties leave through the generic landless sweep below. Italy
    # North adds TUS and ISR — the march of Tuscany and the march of
    # Istria were both imperial (AQU and VER were verified already in
    # the member list before the package was approved); the twelve
    # revived bishoprics are NOT added — vanilla's list never carried
    # them and the package does not ask for it (banked as a note).
    for _add in ("OGK", "CRH", "STY", "SAX", "SWA", "TUS", "ISR"):
        if re.search(r"\b" + _add + r"\b",
                     re.sub(r"#[^\n]*", "", _hb[_ho:find_block_end(_hb, _ho)])):
            sys.exit(f"HRE surgery: {_add} already a member")
    src = (src[:_hre.start() + _ho + 1] + " OGK CRH STY SAX SWA TUS ISR"
           + src[_hre.start() + _ho + 1:])
    report.append(("HRE crowned (leader = OGK) and members joined", 1))

    # Landless tags leave every IO membership/status list (the rule
    # vanilla's own high_kingship documents with its `#PLE` comment).
    # Found by the new harness check's first run: CIL — landless since
    # the Byzantium slice — was still a member of the autocephalous
    # patriarchate. Generic: any LANDLESS_AFTER tag in any members OR
    # special-status list goes (the HRE slice widened the sweep from
    # `members` alone: the nine emptied free cities also sit in
    # free_city = { }); exact-count asserted so a future slice that
    # empties an IO member fails loudly instead of shipping a ghost.
    # (Building/army/pop-based members hold no land legitimately and
    # are never in LANDLESS_AFTER, so they are untouched.)
    n_ghosts = 0
    _ghost_names = []
    # REVERSED: the loop mutates src, and forward iteration over
    # pre-mutation offsets sliced with stale indices — the exact-count
    # assert caught it on the first run (it reported a ghost set that
    # skipped CIL's own list).
    for _mb in reversed(list(re.finditer(
            r"(?:members|free_city|elector|archbishop_elector|emperor"
            r"|imperial_prince|imperial_prelate"
            r"|imperial_peasant_republic)[ \t]*=[ \t]*\{", src))):
        _o = src.index("{", _mb.start())
        _e = find_block_end(src, _o)
        _inner = src[_o + 1:_e - 1]
        _toks = re.sub(r"#[^\n]*", "", _inner).split()
        _keep = [t for t in _toks if t not in LANDLESS_AFTER]
        if len(_keep) != len(_toks):
            _ghost_names += [t for t in _toks if t in LANDLESS_AFTER]
            n_ghosts += len(_toks) - len(_keep)
            src = (src[:_o + 1] + "\n\t\t\t" + " ".join(_keep)
                   + "\n\t\t" + src[_e - 1:])
    # The measured set (2026-07-29): the original six ghosts (CIL +
    # army-based ARM/ATZ in the autocephalous patriarchate, EPI/TRE/
    # FEO in the Orthodox lists — Byzantium/Seljuk-slice leftovers)
    # plus the HRE slice's 22 occurrences: the nine emptied free
    # cities in BOTH members and free_city (7 of them; NHS/MLH sit
    # only in members — their free_city rows are vanilla's own
    # commented "should be but can't" lines) and GOR/ORT/GRK in two
    # lists each. The count moved 1 -> 4 -> 6 -> 28 as the runs
    # measured (a stale-offset loop bug was caught by this very
    # assert on run one).
    # Germany II adds 23: eleven tags in TWO lists each (BRM/HAM/ULM in
    # members + free_city; LUN/WUR/OET/HHB/HEH/HLF/KIR/TUB in members +
    # imperial_prince) and WDB in members alone. ARS is in NO imperial
    # list at all — the Artois sat outside the Empire, which is exactly
    # why Flanders gets it back. LUN leaves as a member and a prince
    # only: its elector seat moved to SAX above, BEFORE this sweep ran,
    # which is the whole point of doing the two in one change. The count
    # moved 1 -> 4 -> 6 -> 28 -> 51 as the runs measured.
    # Italy North adds 20: the fifteen emptied imperial-Italian donors
    # sit in the HRE member list (FER/FAE/IMO do NOT — Ferrara and the
    # Romagna are the papal-orbit side, which is its own confirmation),
    # and five of them (FLO/PRA/SAL/CEV/AOS) also hold imperial_prince
    # seats. The count moved 1 -> 4 -> 6 -> 28 -> 51 -> 71, every
    # transition observed failing before its constant moved.
    # Rus Tier 1 adds 42 (observed failing first, 2026-08-01): every
    # one of the 42 landless principalities sits in exactly ONE IO
    # list — the Orthodox-world membership — and each appears once.
    # The count moved 1 -> 4 -> 6 -> 28 -> 51 -> 71 -> 113.
    _expected_ghosts = sorted(
        ["ARM", "ATZ", "CIL", "EPI", "FEO", "TRE",
         "NHS", "MLH"]
        + ["AAC", "FRN", "GOS", "NUR", "SYE", "DTM", "WRM"] * 2
        + ["GOR", "ORT", "GRK"] * 2
        + ["BRM", "HAM", "ULM"] * 2
        + ["LUN", "WUR", "OET", "HHB", "HEH", "HLF", "KIR", "TUB"] * 2
        + ["WDB"]
        + ["LUC", "SIE", "MAN", "PST", "VLT", "COT", "CHX", "ABA",
           "MND", "ASD"]
        + ["FLO", "PRA", "SAL", "CEV", "AOS"] * 2
        + list(RUS_LANDLESS)
        # Rus Tier 2 adds 9 (observed failing first): HAL + the eight
        # Danube tags, one Orthodox-world membership each; GAZ (the
        # Genoese republic) sits in no IO. 113 -> 122.
        + ["HAL", "WAL", "IAS", "BIA", "BLD", "SRC", "HTN", "HSC",
           "SSI"]
        # China-East adds 9 (observed failing first): LNG + the eight
        # Chinggisid hordes leave the RESTORED Middle Kingdom's member
        # list (209 -> 200 members). 122 -> 131.
        + ["LNG", "CRS", "QAS", "BAT", "BGT", "KHD", "HCN", "OTC",
           "OGE"]
        # Northern Dynasties adds 1: SYG leaves the restored Middle
        # Kingdom's member list (200 -> 199). 131 -> 132.
        + ["SYG"]
        # India Tier 1 adds 13 (observed failing first): the
        # hindu_branch ghosts — vaishnavism loses VIJ YDR BGL DRP JWR
        # BND, shaivism loses JFN SMV RDY MSN RCH RJI, shaktism loses
        # IDR. The six Muslim retirees (DLH MAB SMA GAU SGN STN) sit
        # in no IO list; DBD contributes none BECAUSE it survives —
        # its Mahavihara seat is a reason it was kept. 132 -> 145.
        + ["VIJ", "YDR", "BGL", "DRP", "JWR", "BND",
           "JFN", "SMV", "RDY", "MSN", "RCH", "RJI", "IDR"]
        # Southeast Asia adds 10 (observed failing first): the sect
        # ghosts — Mahavihara loses PEG and TSM, the Burmese Buddhism
        # sect loses ALL FOUR members (PIN SAG TNG BPR — PGN joins
        # below or the slice ships an empty IO), Thai Buddhism loses
        # SUK and LNA, shaivism loses MAJ and (decision 9) MNA. VTN,
        # ARU, ADH, ATJ, PSA and MGD sit in no IO list. 145 -> 155.
        + ["PEG", "TSM", "PIN", "SAG", "TNG", "BPR", "SUK", "LNA",
           "MAJ", "MNA"]
        # Tibet adds 1 (observed failing first, same day): TIB leaves
        # the restored Middle Kingdom's member list (199 -> 198). It
        # sits in NO sect — the Sakya instance it belonged to was
        # already deleted by the future-date strip (creation_date
        # 1073.1.1, vanilla's own dating of the anachronism). 155 -> 156.
        + ["TIB"])
    if n_ghosts != 156 or sorted(_ghost_names) != _expected_ghosts:
        sys.exit(f"expected exactly 156 landless IO list entries, "
                 f"stripped {n_ghosts}: {sorted(_ghost_names)}")
    report.append(("landless IO list entries stripped", n_ghosts))

    # India Tier 1, decision 11: the four Shaiva powers join the
    # shaivism hindu_branch (the Cholas ARE the Shaiva dynasty par
    # excellence; Kalyani, Bhojeshwar, Somnath). PAA joins NO sect —
    # the mulasarvastivada instance is doctrinally right but its
    # members and provinces are all Indonesian. Exactly one instance
    # carries the shaivism law; asserted.
    _sh_blocks = [m for m in re.finditer(
        r"^\tadd_international_organization = \{", src, re.M)
        if "shaivism" in src[m.start():find_block_end(src, src.index("{", m.start()))]]
    if len(_sh_blocks) != 1:
        sys.exit(f"expected exactly 1 shaivism hindu_branch instance, "
                 f"found {len(_sh_blocks)}")
    _sb = _sh_blocks[0]
    _send = find_block_end(src, src.index("{", _sb.start()))
    _mem = re.search(r"^([ \t]*)members[ \t]*=[ \t]*\{",
                     src[_sb.start():_send], re.M)
    if not _mem:
        sys.exit("shaivism instance has no members block")
    _at = _sb.start() + src[_sb.start():_send].index("{", _mem.start()) + 1
    src = (src[:_at] + "\n" + _mem.group(1) + "\tCOZ CLK PMR CHU"
           + src[_at:])
    report.append(("Shaiva powers joined the shaivism branch", 4))

    # SEA §G.6: the Burmese Buddhism sect's four members ALL retire —
    # without a new member the slice ships a zero-member IO. PGN joins:
    # Anawrahta's Theravada reform through Shin Arahan of conquered
    # Thaton [D] is this tradition's own root, and the sect's provinces
    # block (pagan/pinya/pyay/sagaing/taungoo) is precisely PGN's new
    # ground. Exactly one instance carries burmese_buddhism_policy;
    # asserted, the Shaiva-powers shape.
    _bb_blocks = [m for m in re.finditer(
        r"^\tadd_international_organization = \{", src, re.M)
        if "burmese_buddhism_policy" in
        src[m.start():find_block_end(src, src.index("{", m.start()))]]
    if len(_bb_blocks) != 1:
        sys.exit(f"expected exactly 1 Burmese Buddhism sect instance, "
                 f"found {len(_bb_blocks)}")
    _sb = _bb_blocks[0]
    _send = find_block_end(src, src.index("{", _sb.start()))
    _mem = re.search(r"^([ \t]*)members[ \t]*=[ \t]*\{",
                     src[_sb.start():_send], re.M)
    if not _mem:
        sys.exit("Burmese Buddhism instance has no members block")
    _at = _sb.start() + src[_sb.start():_send].index("{", _mem.start()) + 1
    src = src[:_at] + "\n" + _mem.group(1) + "\tPGN" + src[_at:]
    report.append(("Pagan joined the Burmese Buddhism sect", 1))

    # KDR and JGL join the shaivism hindu_branch beside their
    # neighbours (SUN, KRP, BLI's web all sit in the Hindu branches;
    # MAJ leaves the same list landless) — Javanese kingship is
    # Shiva-Buddha syncretic [U]. Same block the India add found; the
    # exactly-one assert re-runs on the updated source.
    _sh2_blocks = [m for m in re.finditer(
        r"^\tadd_international_organization = \{", src, re.M)
        if "shaivism" in
        src[m.start():find_block_end(src, src.index("{", m.start()))]]
    if len(_sh2_blocks) != 1:
        sys.exit(f"expected exactly 1 shaivism hindu_branch instance, "
                 f"found {len(_sh2_blocks)} (SEA add)")
    _sb = _sh2_blocks[0]
    _send = find_block_end(src, src.index("{", _sb.start()))
    _mem = re.search(r"^([ \t]*)members[ \t]*=[ \t]*\{",
                     src[_sb.start():_send], re.M)
    if not _mem:
        sys.exit("shaivism instance has no members block (SEA add)")
    _at = _sb.start() + src[_sb.start():_send].index("{", _mem.start()) + 1
    src = src[:_at] + "\n" + _mem.group(1) + "\tKDR JGL" + src[_at:]
    report.append(("Javanese kingdoms joined the shaivism branch", 2))

    leaders = len(re.findall(r"^[ \t]*leader[ \t]*=", src, re.M))
    src = tidy(src)

    def validate():
        if re.search(r"^[ \t]*ruler_term[ \t]*=", src, re.M):
            return "ruler_term survived the strip"
        # Exactly 18 in vanilla 1.3.11; 17 since the middle_kingdom
        # re-date (2026-08-01, Route B — the instance now predates
        # START_DATE and survives on purpose). A patch changing the
        # number fails loudly and a human re-reads the file.
        if removed != 17:
            return f"expected exactly 17 future-dated IO removals, removed {removed}"
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

    # Vanilla ships exactly FOUR characters who are alive at 1066 but
    # carry no `birth = <location>` — at 1337 all four are long dead and
    # vanilla never needed to place them; our death-strip resurrection
    # exposed the gap and the engine names each at start
    # (initialize_from_bookmark.cpp:410, first user-observed 2026-07-30).
    # An independent sweep of the built file confirms these four are the
    # COMPLETE set of living-without-birth. Places: Heinrich's Goslar is
    # already the mod's recorded [U] birthplace (CAPITAL_FIXES comment);
    # the three Dunkeld Scots get scone [U] — dunkeld itself is no map
    # location, and Scone is the house's crowning seat.
    _BIRTH_FIXES = {
        "sco_malcolm_iii": "scone",
        "sco_donald_iii": "scone",
        "sco_duncan_ii": "scone",
        "ogk_heinrich_iv_salier": "goslar",
    }
    n_births = 0
    for _ch, _loc in sorted(_BIRTH_FIXES.items()):
        _bm = re.search(r"^\t" + _ch + r" = \{", src, re.M)
        if not _bm:
            sys.exit(f"BIRTH_FIXES: {_ch} not found")
        _be = find_block_end(src, src.index("{", _bm.start()))
        _body = src[_bm.start():_be]
        if re.search(r"^\t\tbirth[ \t]*=[ \t]*[a-z]", _body, re.M):
            sys.exit(f"BIRTH_FIXES: {_ch} already carries a birth — "
                     "a vanilla patch filled the gap; drop the entry")
        _bdm = re.search(r"^\t\tbirth_date[ \t]*=[^\n]*\n", _body, re.M)
        if not _bdm:
            sys.exit(f"BIRTH_FIXES: {_ch} has no birth_date to anchor on")
        _at = _bm.start() + _bdm.end()
        src = src[:_at] + f"\t\tbirth = {_loc}\n" + src[_at:]
        n_births += 1
    report.append(("birthplaces added to the resurrected", n_births))

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
        for tag, _row in sorted(HISTORICAL_RULERS.items()):
            key, accession = _row[0], _row[1]
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
    src, n = re.subn(r"^[ \t]*dependency = \{[^}\n]*subject_type = appanage[^}\n]*\}[ \t]*(?:#[^\n]*)?\n",
                     "", src, flags=re.M)
    report.append(("appanage dependencies removed", n))
    src = tidy(src)
    after = len(re.findall(r"^[ \t]*dependency = \{", src, re.M))

    # England's six 1337 subjections are all post-1066 creations: Wales as
    # a dominion (1283), the Irish Pale (1177+), Aquitaine as a Plantagenet
    # fiefdom, Durham and the rest. Harold's England of 1066 has NO
    # subjects — the batch test found our seated William VIII of Aquitaine
    # sitting under Harold's overlordship because of these lines. Same
    # poison class as the French appanages.
    src, n_eng = re.subn(r"^[ \t]*dependency = \{ first = ENG [^}\n]*\}[ \t]*(?:#[^\n]*)?\n",
                         "", src, flags=re.M)
    report.append(("English 1337 subjections removed", n_eng))

    # Future-dated dependencies STRIPPED (user-approved with the Christian
    # Iberia batch; was parked since the Italy pass). All 27 carry start
    # dates 1202.10.9-1336.8.29 — none has a defense at 1066, and the
    # Iberia slice made one of them acute: ARA's 1279 vassalage over an
    # MLL that is now landless. Exactly 27 in the current data; if a
    # vanilla patch changes the number this fails loudly.
    n_future_deps = 0
    def _drop_future_dep(m):
        nonlocal n_future_deps
        d = re.search(r"start_date[ \t]*=[ \t]*([0-9.]+)", m.group(0))
        if d and date_tuple(d.group(1)) >= _start_date():
            n_future_deps += 1
            return ""
        return m.group(0)
    # `(?:#[^\n]*)?` — six of the 27 carry a trailing comment after the
    # brace (`} #Treaty of Perpignan…`) and an end-anchored pattern
    # without it silently skips exactly those six. The one-line-block
    # lesson's cousin, found the day this strip first ran.
    src = re.sub(r"^[ \t]*dependency = \{[^}\n]*\}[ \t]*(?:#[^\n]*)?\n", _drop_future_dep,
                 src, flags=re.M)
    if n_future_deps != 27:
        sys.exit(f"expected exactly 27 future-dated dependencies, stripped {n_future_deps}")
    report.append(("future-dated dependencies stripped", n_future_deps))

    # The 1337 French vassal web dies with the demesne partition
    # (France package 2026-07-29). All 27 surviving `first = FRA ...
    # vassal` lines go: the vassal type blocks war declarations
    # (vassal.txt:80-86 — the exact class that froze the Norman
    # Conquest in round 2) and it sat on twelve of our seated thrones
    # (BRI FOI AMG BLS AST COM IJO PER MON VNT AUV BGN). The six-fief
    # homage ring returns below as TRIBUTARIES. Runs AFTER the
    # future-dated strip, which already removed FRA->FLA (1305.6.23).
    src, n_frav = re.subn(
        r"^[ \t]*dependency = \{ first = FRA second = \w+ subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
        "", src, flags=re.M)
    if n_frav != 27:
        sys.exit(f"expected exactly 27 FRA vassal dependencies, stripped {n_frav}")
    report.append(("French 1337 vassal web removed", n_frav))

    # Four fiefdom sub-ties die with it. fiefdom carries
    # has_overlords_ruler = yes (fiefdom.txt:16): BOU->MRC was
    # overriding our seated Adalbert of La Marche with BOU's random
    # ruler, FOI->BRR and FOI->MDM copied Roger II onto Bearn and
    # Mont-de-Marsan, ANJ->MIE put Geoffrey III on Maine — which in
    # 1066 is under NORMAN occupation, not Angevin. ALE->PRC stays
    # (two random-ruler tags, a defensible Belleme-family tie);
    # FLA->NAM and ARS->STP belong to the Empire slice.
    n_fief = 0
    for _pair in ("ANJ second = MIE", "FOI second = BRR",
                  "FOI second = MDM", "BOU second = MRC"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = " + _pair
            + r" subject_type = fiefdom \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_fief += _k
    if n_fief != 4:
        sys.exit(f"expected exactly 4 French fiefdom sub-ties, stripped {n_fief}")
    report.append(("French fiefdom sub-ties removed", n_fief))

    # The British slice's tie surgery (package 2026-07-29): five
    # Gaelic vassal ties become tributaries below (vassal is
    # war-blocking, and Gaelic tribes pass the tributary gate free),
    # and the two Scottish crown vassalages die — there is no earldom
    # of Ross before the 12th century, and Malcolm III's reign was a
    # war AGAINST Moray, not lordship over it. NOR->ORK is KEPT
    # (historically right, and ORK is a monarchy — a tributary
    # conversion would fail the gate without a reform on NOR).
    n_brit = 0
    for _pair in ("TRY second = AMH", "TYR second = INI",
                  "TYR second = KEE", "LEI second = OSS",
                  "MCM second = BEA", "SCO second = ROS",
                  "SCO second = MOY"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = " + _pair
            + r" subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_brit += _k
    if n_brit != 7:
        sys.exit(f"expected exactly 7 British vassal strips, stripped {n_brit}")
    report.append(("British vassal ties removed", n_brit))

    # The Rus live-defect patch (package re-verified, user-approved
    # 2026-08-01; both defects USER-CONFIRMED in game 2026-07-30):
    # GLH->KIE is the Tatar Yoke 271 years early — it made Iziaslav a
    # Golden-Horde tributary at 1066 — and LIT->POK is the 14th-century
    # Lithuanian overlordship over Polotsk. The generic landless sweep
    # provably cannot catch either (both partners stay LANDED), so they
    # are stripped by name, the British batch's shape.
    n_rus = 0
    for _pair, _st in (("GLH second = KIE", "tributary"),
                       ("LIT second = POK", "vassal")):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = " + _pair
            + r" subject_type = " + _st + r" \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_rus += _k
    if n_rus != 2:
        sys.exit(f"expected exactly 2 Rus dependency strips, stripped {n_rus}")
    report.append(("Rus 1337 overlordships removed", n_rus))

    # China-East: Goryeo is nobody's hard vassal in 1066 — the
    # celestial tributary tie lives in the restored Middle Kingdom IO
    # (KOR keeps its celestial_governor seat there, which IS the
    # historical relationship); the dependency line is 1337's.
    src, _k = re.subn(
        r"^[ \t]*dependency = \{ first = CHI second = KOR subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
        "", src, flags=re.M)
    if _k != 1:
        sys.exit(f"expected exactly 1 CHI->KOR strip, stripped {_k}")
    report.append(("Goryeo freed from the 1337 vassalage", _k))

    # Northern Dynasties: the 46-tag Manchurian bloc repoints CHI->LIA
    # as TRIBUTARIES — in 1066 the "wild Jurchen" of the Songhua and
    # Ussuri paid the Liao Eastern Capital, not Kaifeng; the Song's
    # writ never crossed the Wall. All 46 are type = tribe (measured
    # through their include chains 2026-08-01), so the tributary gate
    # passes on the subject branch — the Irish law; liao_ordo_reform
    # rides as insurance regardless. SYG's own line dies with SYG
    # landless in the sweep above. Runs BEFORE the landless sweep so
    # the repointed lines are LIA's when it looks.
    _JURCHEN = ("AAR AID ASU BAY DLA EJI FLN FUT FUY GIL HIJ HNC HOT "
                "HRO HUI HUR ILU IMN ITU JHT JUS LAL LLU MAH MIC MRE "
                "MUH NAL NEM NEY NRO SHI SIR SMN SNC SUI TAS TOD TOX "
                "USS WEJ WEK WUY YRN YIM YOO").split()
    n_liao = 0
    for _j in _JURCHEN:
        src, _k = re.subn(
            r"^([ \t]*)dependency = \{ first = CHI second = " + _j
            + r" subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
            lambda m, j=_j: (m.group(1) + "dependency = { first = LIA "
                             f"second = {j} subject_type = tributary }}\n"),
            src, flags=re.M)
        n_liao += _k
    if n_liao != 46:
        sys.exit(f"expected exactly 46 Jurchen repoints to LIA, got {n_liao}")
    report.append(("Jurchen tribes repointed to the Liao", n_liao))

    # THE JIMI FIX (grand-test launch, 2026-08-01): the sixteen
    # mid-tier tusi lords (SZH, BZU, QJG...) were LNG's OWN tusi, and
    # LNG's retirement freed them - breaking can_country_have_tusi's
    # subject-branch for their 45 sub-ties (country_triggers.txt:
    # 1291-1293; 45 government.cpp:3702 lines, measured). They repoint
    # to CHI: the Song's jimi (loose-rein) frontier prefectures are
    # this system's ancestor, and CHI as Middle-Kingdom leader passes
    # every branch of the gate. LNG's other 46 leaf-tusi (the Yunnan
    # orbit, Dali's world) still die with it.
    _JIMI = ("BZH BZU GGX GNN LIN MHU PAN PDN QJG QYN SDG SMG SZH "
             "TNZ YGS YNJ").split()
    n_jimi = 0
    for _j in _JIMI:
        src, _k = re.subn(
            r"^([ \t]*)dependency = \{ first = LNG second = " + _j
            + r" subject_type = tusi \}[ \t]*(?:#[^\n]*)?\n",
            lambda m, j=_j: (m.group(1) + "dependency = { first = CHI "
                             f"second = {j} subject_type = tusi }}\n"),
            src, flags=re.M)
        n_jimi += _k
    if n_jimi != 16:
        sys.exit(f"expected exactly 16 jimi repoints to CHI, got {n_jimi}")
    report.append(("jimi lords repointed to the Song", n_jimi))

    # THE SAHEL REPOINT (Africa slice, 2026-08-02): vanilla's thirteen
    # MAL vassals are ten of al-Bakri's own 1068 polities hung off a
    # Mali 170 years away. FOUR repoint MAL->GHA — Wagadu is the 1066
    # hegemon and al-Bakri describes exactly this overlordship [U].
    # NOT five: the package's G.2 listed KBR, but KBR goes LANDLESS in
    # this same slice (its macina to ZGH) — a landless vassal is the
    # incoherence the review caught; its MAL line dies in the landless
    # sweep below instead, like SGH's. Runs BEFORE that sweep so the
    # repointed lines are GHA's when it looks.
    _GHANA_VASSALS = ("BBK", "DFN", "TFK", "ZGH")
    n_ghana = 0
    for _g in _GHANA_VASSALS:
        src, _k = re.subn(
            r"^([ \t]*)dependency = \{ first = MAL second = " + _g
            + r" subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
            lambda m, g=_g: (m.group(1) + "dependency = { first = GHA "
                             f"second = {g} subject_type = vassal }}\n"),
            src, flags=re.M)
        n_ghana += _k
    if n_ghana != 4:
        sys.exit(f"expected exactly 4 Sahel repoints to GHA, got {n_ghana}")
    report.append(("al-Bakri's polities repointed to Ghana", n_ghana))

    # Four MAL ties DELETED by name, not repointed: GHA becomes the
    # overlord, and al-Bakri treats Kawkaw (SON), Takrur and Tadmakka
    # as kingdoms apart from Ghana [U] — Takrur in particular is
    # Ghana's rival and the Almoravids' ally. (MAL->BMR/JOL/KAB/SGH/KBR
    # die in the landless sweep, not here.)
    n_mali_free = 0
    for _g in ("GHA", "SON", "TKR", "TMK"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = MAL second = " + _g
            + r" subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_mali_free += _k
    if n_mali_free != 4:
        sys.exit(f"expected exactly 4 MAL deletions, got {n_mali_free}")
    report.append(("kingdoms freed from the 1337 Mali web", n_mali_free))

    # Kanem's Hausa tributaries: a BORNU-era relation [U] — the Sayfawa
    # do not cross to the west shore of Lake Chad until the 1380s; at
    # 1066 Kanem's reach is north (Kawar, the Fezzan road — KBO->FZA
    # is KEPT for exactly that reason).
    n_hausa = 0
    for _g in ("DAA", "GOB", "KAN", "KTS", "RAN", "ZAM", "ZZZ"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = KBO second = " + _g
            + r" subject_type = tributary \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_hausa += _k
    if n_hausa != 7:
        sys.exit(f"expected exactly 7 KBO->Hausa strips, got {n_hausa}")
    report.append(("Hausa states freed from Bornu-era Kanem", n_hausa))

    # Kilwa's thalassocracy — including six Madagascar tributaries —
    # is the Mahdali sultanate's, 1277+ [U]. The largest single strip
    # in the Africa slice: it turns "Kilwa's empire" into a coast of
    # independent city-states, which IS the 1066 Zanj coast.
    n_kilwa = 0
    for _g in ("MLI", "MBA", "GED", "PEM", "NTL", "MTO", "AHY", "MHL",
               "VOH", "NYM", "MOZ", "ZZB"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = ZAN second = " + _g
            + r" subject_type = tributary \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_kilwa += _k
    if n_kilwa != 12:
        sys.exit(f"expected exactly 12 ZAN tributary strips, got {n_kilwa}")
    report.append(("Kilwa's Mahdali thalassocracy dissolved", n_kilwa))

    # Ethiopia's southern ring — Ennarea, Hadiya, Bale, Dawaro — is
    # Amda Seyon's, 1320s-30s [U]. ETH->IFA dies in the landless sweep.
    n_eth = 0
    for _g, _st in (("ENN", "tributary"), ("HDY", "vassal"),
                    ("BLE", "vassal"), ("DAW", "vassal")):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = ETH second = " + _g
            + r" subject_type = " + _st + r" \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_eth += _k
    if n_eth != 4:
        sys.exit(f"expected exactly 4 ETH southern strips, got {n_eth}")
    report.append(("Amda Seyon's southern ring dissolved", n_eth))

    # Brunei's archipelagic overlordship of Sulu, Ma-i, Maynila, Butuan
    # and Maguindanao is the SULTANATE's, 15th-16th c. [U] — at 1066
    # Po-ni is one Song tributary among several and Butuan is another
    # (its own missions of 1001-1011 and the 1003 precedence protest
    # [D] are why it cannot be Brunei's vassal 400 years early). MNA
    # and MGD go landless in this slice; their lines die HERE by name,
    # before the landless sweep, like the rest of the web.
    n_brunei = 0
    for _g in ("SUL", "MYI", "MNA", "BTU", "MGD"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = BEI second = " + _g
            + r" subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_brunei += _k
    if n_brunei != 5:
        sys.exit(f"expected exactly 5 BEI vassal strips, got {n_brunei}")
    report.append(("the Bruneian sultanate's web dissolved", n_brunei))

    # Melayu over Pannai (vanilla 12_diplomacy.txt:425) — the one
    # Srivijayan tie whose overlord survives. Deleted by NAME, not
    # repointed (decision 13): the package prescribed BOTH a G.2
    # repoint of this line AND a PLB->PNI pair in its G.4 tributary
    # list — together they would give PNI two overlords, the HLL
    # repeating-assert class; the review caught the contradiction. The
    # mandala ships uniformly as the five PLB tributaries below.
    src, n_jmb_pni = re.subn(
        r"^[ \t]*dependency = \{ first = JMB second = PNI "
        r"subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
        "", src, flags=re.M)
    if n_jmb_pni != 1:
        sys.exit(f"expected exactly 1 JMB->PNI strip, got {n_jmb_pni}")
    report.append(("Melayu's Pannai tie dissolved into the mandala",
                   n_jmb_pni))

    # The four DEEP-PLATEAU tusi ties (Tibet slice, decision 6): the
    # Song in authority over the Golog, Amdo, the Horpa of Kandze and
    # the Nyag valley is the same error class as Yuan Tibet, one
    # province east — the Song's writ in 1066 stopped at the
    # Gansu-Sichuan rim, whose fourteen jimi/vassal ties are KEPT (the
    # item-30 frontier reading). None of the four has sub-tusi of its
    # own (measured), so the can_country_have_tusi knock-on that bit
    # the LNG retirement cannot recur. TIB's own fifteen lines die in
    # the landless sweep below, not here.
    n_tibet_tusi = 0
    for _g in ("HOR", "NYA", "GOL", "AMD"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = CHI second = " + _g
            + r" subject_type = tusi \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_tibet_tusi += _k
    if n_tibet_tusi != 4:
        sys.exit(f"expected exactly 4 deep-plateau tusi strips, got {n_tibet_tusi}")
    report.append(("the Song freed of the deep plateau", n_tibet_tusi))

    # Novgorod's Yugra tribute (vanilla 12_diplomacy.txt:50-59): ten
    # tributary ties over the trans-Ural Ob-Ugric and Samoyed
    # pop-countries. Vanilla's own geography is exact — all ten
    # subjects are beyond the Urals, and BJARMIA, the Dvina tribute
    # land NOV holds directly, has no tie at all. The first recorded
    # Yugra expedition is the PVL's 1096 entry [D] — thirty years out.
    # A named strip is REQUIRED: the subjects are type=pop countries
    # that hold no land by design, so the landless sweep below can
    # never see these lines. (This also removes the build's only
    # two-level tributary chain, KIE->NOV->these — OWED CHECK 2 of the
    # package stays open for a future case.)
    n_yugra_tribute = 0
    for _g in ("OBD", "PLY", "BAK", "KND", "BGJ", "KOD", "SVA", "KZY",
               "LYA", "TBY"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = NOV second = " + _g
            + r" subject_type = tributary \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_yugra_tribute += _k
    if n_yugra_tribute != 10:
        sys.exit(f"expected exactly 10 NOV->Yugra tributary strips, "
                 f"got {n_yugra_tribute}")
    report.append(("Novgorod's Yugra tribute unwound", n_yugra_tribute))

    # The Americas (2026-08-02): vanilla ships exactly FOUR dependency
    # lines in the whole western hemisphere and all four are post-1066.
    # TEP->TNC dies in the landless sweep below (TNC retired), so only
    # three are stripped by name here: TEP->TCP (the Tepanec hegemony
    # over Tlacopan, c. 1370-1428 [D]), COC->XIU (the Mayapan league,
    # c. 1220-1441 [D]; Mani is a post-1441 seat) and COC->HEL (Ah Chel
    # is a post-1441 cuchcabal [D]). The subjects stay LANDED (1, 3 and
    # 6 locations), so the landless sweep cannot see these three.
    n_americas_deps = 0
    for _f, _s in (("TEP", "TCP"), ("COC", "XIU"), ("COC", "HEL")):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = " + _f + r" second = " + _s
            + r" subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_americas_deps += _k
    if n_americas_deps != 3:
        sys.exit(f"expected exactly 3 American vassal strips, "
                 f"got {n_americas_deps}")
    report.append(("the Americas freed of their late hegemonies",
                   n_americas_deps))

    # A landless tag cannot sit in the vassal web: the engine logs
    # "invalid subject / non-existent overlord" for every dependency
    # naming one (first in-game observation: ~318-line start flood after
    # the Byzantium batch). All 28 are 1337 relations — the Frankokratia
    # chains, the beylik webs, Armenia's — and every partner they free
    # (Syunik, Khachen, Salona…) was historically independent in 1066.
    n_landless_deps = 0
    def _drop_landless_dep(m):
        nonlocal n_landless_deps
        f = re.search(r"first = (\w+)", m.group(0))
        s2 = re.search(r"second = (\w+)", m.group(0))
        if (f and f.group(1) in LANDLESS_AFTER) or (s2 and s2.group(1) in LANDLESS_AFTER):
            n_landless_deps += 1
            return ""
        return m.group(0)
    src = re.sub(r"^[ \t]*dependency = \{[^}\n]*\}[ \t]*(?:#[^\n]*)?\n",
                 _drop_landless_dep, src, flags=re.M)
    # 28 from the Byzantium batch + 54 from the Seljuk batch (JAL's 18,
    # SUT's 15, GRG's 10, the Jazira web...). GRG->MZN is IN: GRG dies,
    # MZN survives and is re-parented to SEL below. +8 from the Fatimid
    # batch: MAM's eight surviving 1337 dependencies (AAL AMR BKZ BQA
    # FDL SKN MDA MEC — vanilla 12_diplomacy.txt:798-808; DUL/KIL/DGE
    # died with earlier slices). The 82->90 transition was OBSERVED
    # failing before this constant moved (2026-07-29) — the assert
    # works. +18 from the British batch (10 WLS->marcher, 7 PLE->X,
    # 1 SBL->LOI), the 90->108 transition observed failing the same
    # way. +4 from Germany II (HSA->HAM and HSA->BRM, the two Hanseatic
    # memberships of cities that do not exist yet; ARS->STP and
    # WUR->HBR, the two vassalages the emptied Artois and Wurttemberg
    # were holding) — the 108->112 transition observed failing too, and
    # ARS->STP is the tie an earlier slice explicitly banked for the
    # Empire (build_diplomacy's French fiefdom comment). +3 from Italy
    # North: SAV->CEV and VER->LUC (both donors empty into PIE and TUS)
    # plus PAP->FAE — the HRE slice stripped that one by name, but FAE
    # itself is landless now, so this sweep eats it first and the
    # dedicated strip below is RETIRED. 112->115 observed failing.
    # 115 -> 127 with Central Asia (observed failing first, 2026-08-01):
    # CHG's ten 1337 ulus vassals (BKH BRL DGH JLY KRG KTT QCH QUN SLD
    # YSU) + DGH's two (MNL SRL) die with their overlords landless. The
    # message used to say 112 while the constant said 115 — a stale
    # string two agents flagged independently; now both move together.
    # 127 -> 152 with Rus Tier 1 (observed failing first, same day):
    # the 42 landless principalities' web — the BRY/CHR/KCH/LIT/NOV/
    # RYA/SMO/TVE/YAR subject lines (incl. vanilla's Chernihiv-under-
    # Bryansk absurdity), GLH's BRY/HAL/VOL tributaries, LIT's seven
    # Black-Ruthenia vassals and NOV->ORE with the ORE fold.
    # 152 -> 155 with Arabia (observed failing first, 2026-08-01):
    # ORM->JSK, ORM->JRW, and HLG->HLL — the last MIGRATED here from
    # the retired dedicated strip below (HLG is landless now, the sweep
    # sees it first). KLB has no diplomacy lines (grep-verified).
    # 155 -> 164 with Rus Tier 2 (observed failing first, 2026-08-01):
    # GEN->GAZ, GLH's seven Moldavian boyar tributaries
    # (BIA BLD HTN HSC IAS SRC SSI) and GLH->HAL.
    # 164 -> 238 with China-East (observed failing first, same day):
    # LNG's 62 tusi ties + LNG->CDL, and the Chinggisid web's 11
    # (CHI->five hordes, OGE->BAT/CRS/KHD/TRH, CRS->TVA — freeing
    # TRH and TVA, both correctly independent in 1066). 74 lines,
    # grep-verified against vanilla.
    # 238 -> 239 with Northern Dynasties (observed failing first):
    # CHI->SYG dies with SYG landless — the 46 Jurchen lines were
    # repointed to LIA BEFORE this sweep and survive as its ring.
    # 239 -> 249 with India Tier 1 (observed failing first): DLH's
    # nine samanta ties + GAU->TRF. The twelve surviving samantas are
    # all defensible 1066 hill/coastal clientages (package G.1).
    # 249 -> 233 with the jimi fix (observed failing first): the
    # sixteen mid-tier tusi lords now repoint to CHI BEFORE this sweep
    # and survive as the Song's jimi frontier.
    # 233 -> 244 with the Baltic (observed failing first, 2026-08-01):
    # the crusader web's ten lines — TEU's four bishopric vassals
    # (ERM SMD PMS CHL), LIV's five (RIG ARR KUR BIO BID) and
    # TEU->LIV itself — plus LIT->NRK, which the package's G.2 slated
    # for a named strip on the assumption both partners stay landed;
    # under option 2 LIT is landless and this sweep owns its lines
    # (the PAP->FAE law). LIT->POK still dies by name in the Rus strip
    # ABOVE this sweep, so it lands in n_rus, not here.
    # 244 -> 253 with Africa (observed failing first, 2026-08-02, the
    # predicted arithmetic): MAL->BMR/JOL/KAB (the 1337 Mali web's
    # landless side), ETH->IFA, IFA->HRL/WAR/TDE (the Walashma ring),
    # plus MAL->SGH and MAL->KBR — the two side-effect retirees whose
    # lines die here rather than by name (KBR is the review's
    # repoint-vs-landless catch; OYO has zero diplomacy lines,
    # grep-verified).
    # 253 -> 265 with Southeast Asia (observed failing first,
    # 2026-08-02): PIN->TNG/BPR, SUK->PUA/PTC/TSM, LAV->ADH, and MAJ's
    # six (JMB INR PLB TJP + the BAI/KAM tributaries) — package §G.1's
    # exact twelve. ATJ/PSA/MNA/MGD contribute nothing here: no vanilla
    # line names the first two, and the BEI web died by name above.
    # (The old message string said 233 while the constant said 253 —
    # the stale-string class again; both move together now.)
    # 265 -> 280 with Tibet (observed failing first, same day): the
    # entire Sakya web — CHI->TIB plus TIB's fourteen vassals (GUG PUR
    # MGG POO LGT DRG NCN GNJ BTG NBH LTN LMN MAR ZNK) — dies on TIB's
    # retirement alone. The cheapest diplomacy correction in the
    # project's history: fifteen lines for three characters in a tuple.
    # 280 -> 281 with the Americas (observed failing first, same day):
    # TEP->TNC — the Tepanec vassalage over a city founded in 1325.
    # CSU names no dependency (grep-verified both trees).
    if n_landless_deps != 281:
        sys.exit(f"expected exactly 281 landless-tag dependencies, stripped {n_landless_deps}")
    report.append(("dependencies naming a landless tag stripped", n_landless_deps))

    # Alliances and guarantees naming a landless tag go the same way
    # (HBN-KTW, MKW-ZZR, HLG-GRG, KRT-GRG in the Seljuk theatre, plus
    # vanilla's BYZ-TRE alliance — Trebizond is landless since the
    # Byzantium batch).
    n_pacts = 0
    def _drop_landless_pact(m):
        nonlocal n_pacts
        f = re.search(r"first = (\w+)", m.group(0))
        s2 = re.search(r"second = (\w+)", m.group(0))
        if ((f and f.group(1) in LANDLESS_AFTER)
                or (s2 and s2.group(1) in LANDLESS_AFTER)):
            n_pacts += 1
            return ""
        return m.group(0)
    src = re.sub(r"^[ \t]*scripted_(?:mutual|oneway) = \{[^}\n]*\}[ \t]*(?:#[^\n]*)?\n",
                 _drop_landless_pact, src, flags=re.M)
    # +2 British (THO<->CWM, MYO<->UMH alliances); 5->7 observed
    # failing before the constant moved, like every transition here.
    # 7 -> 9 with the Baltic (observed failing first, 2026-08-01):
    # TEU<->BOH — John of Luxembourg's crusading alliance, pure
    # 1337 — and LIT<->POL, which is Krewo 1385 inverted (Boleslaw II
    # raided Yotvingia); the latter dies FREE via LIT's option-2
    # retirement, one of the package's own arguments for it.
    # No SEA pact exists (measured: zero scripted_mutual/oneway lines
    # name a theater tag) — 9 stands. The message string below said 7
    # while the constant said 9; fixed with the SEA slice.
    if n_pacts != 9:
        sys.exit(f"expected exactly 9 landless-tag pacts, stripped {n_pacts}")
    report.append(("pacts naming a landless tag stripped", n_pacts))

    # The dedicated HLG->HLL strip is RETIRED (2026-08-01): HLG joined
    # LANDLESS_AFTER with the Arabia slice, so the generic landless
    # sweep above now owns that line — the PAP->FAE precedent. Its
    # history (the multiple-overlords assert of 2026-07-29,
    # diplomacy.cpp:4796) lives in the decoder.

    # The Seljuk khutba: nine clients as TRIBUTARY subjects —
    # war-capable (tributary.txt:88), own color and name. MEASURED
    # 2026-07-29: the tributary visible gate binds at game start and all
    # nine downgraded to vassal; SEL now carries seljuk_khutba_reform
    # (allow_tributary_subject) to pass it — see the slice comment.
    _wrap = src.rindex("\n}")
    _tribs = "".join(
        f"\tdependency = {{ first = SEL second = {t} subject_type = tributary }}\n"
        for t in SELJUK_TRIBUTARIES)
    src = (src[:_wrap]
           + "\n\n\t# 1066: the Seljuk clients under the khutba (generated)\n"
           + _tribs + src[_wrap:])
    report.append(("Seljuk tributaries added", len(SELJUK_TRIBUTARIES)))

    # The Fatimid khutba: MEC (until 15 April 1071 — the switch is an
    # event hook) and BKZ (the Banu Kanz of Aswan, Kanz al-Dawla being
    # a Fatimid title [U]). Their MAM overlord lines died with the
    # landless strip above, so no multiple-overlord collision is
    # possible; FAT carries fatimid_khutba_reform for the visible gate.
    _wrap = src.rindex("\n}")
    _ftribs = "".join(
        f"\tdependency = {{ first = FAT second = {t} subject_type = tributary }}\n"
        for t in FATIMID_TRIBUTARIES)
    src = (src[:_wrap]
           + "\n\t# 1066: the Fatimid clients under the khutba (generated)\n"
           + _ftribs + src[_wrap:])
    report.append(("Fatimid tributaries added", len(FATIMID_TRIBUTARIES)))

    # The Capetian homage ring: the six northern fiefs that
    # historically did homage to Philip I, as TRIBUTARIES —
    # war-capable, own color, cancellable (tributary.txt:86-93), the
    # loose bond 11th-century homage actually was. FRA carries
    # capetian_homage_reform for the visible gate. Their old FRA
    # vassal lines died in the strip above, so no multiple-overlord
    # collision is possible.
    _wrap = src.rindex("\n}")
    _htribs = "".join(
        f"\tdependency = {{ first = FRA second = {t} subject_type = tributary }}\n"
        for t in FRANCE_TRIBUTARIES)
    src = (src[:_wrap]
           + "\n\t# 1066: the Capetian homage ring (generated)\n"
           + _htribs + src[_wrap:])
    report.append(("Capetian homage tributaries added", len(FRANCE_TRIBUTARIES)))

    # The Kyivan seniority: Mstislav rules Novgorod for his father —
    # KIE -> NOV as a war-capable TRIBUTARY (Rus package §G.4, user
    # decision 12; the CHR/PYS triumvirs are partners, no ties). KIE
    # carries kyivan_seniority_reform for the visible gate (khutba
    # pattern #5). NOV's old NOV->ORE vassal died with ORE landless in
    # the strip above, so no collision is possible.
    _wrap = src.rindex("\n}")
    _rtribs = "".join(
        f"\tdependency = {{ first = {o} second = {s} subject_type = tributary }}\n"
        for o, s in RUS_TRIBUTARIES)
    src = (src[:_wrap]
           + "\n\t# 1066: the Kyivan seniority over Novgorod (generated)\n"
           + _rtribs + src[_wrap:])
    report.append(("Rus tributaries added", len(RUS_TRIBUTARIES)))

    # The Irish khutba needs no khutba: every subject is a gaelic
    # TRIBE, and tributary.txt:21's visible gate passes on the
    # subject's government type alone — the first reform-free
    # tributary ring (the package's second headline find). Five
    # conversions + the new LEI->DUB (Murchad rules Dublin for his
    # father, the one unambiguous 1066 subjection).
    _wrap = src.rindex("\n}")
    _btribs = "".join(
        f"\tdependency = {{ first = {o} second = {s} subject_type = tributary }}\n"
        for o, s in BRITISH_TRIBUTARIES)
    src = (src[:_wrap]
           + "\n\t# 1066: the Irish client ties (generated)\n"
           + _btribs + src[_wrap:])
    report.append(("Irish tributaries added", len(BRITISH_TRIBUTARIES)))

    # The Srivijayan mandala: Palembang over the Malay ports —
    # war-capable TRIBUTARIES, the loose bond the Chinese sources
    # describe. NO reform anywhere: every party's own vanilla template
    # carries reforms = { mandala_system } (allow_tributary_subject =
    # yes, country_specific.txt:3894-3915) — the first ring in the
    # project gated by a VANILLA reform (SEL/FAT/FRA/KIE each needed an
    # authored one; the Irish six rode the tribe branch). MAJ's three
    # Sumatran vassal lines died in the landless sweep above and
    # JMB->PNI died by name before it — no multiple-overlord collision
    # is possible.
    _wrap = src.rindex("\n}")
    _stribs = "".join(
        f"\tdependency = {{ first = {o} second = {s} subject_type = tributary }}\n"
        for o, s in SRIVIJAYA_TRIBUTARIES)
    src = (src[:_wrap]
           + "\n\t# 1066: the Srivijayan mandala (generated)\n"
           + _stribs + src[_wrap:])
    report.append(("Srivijayan mandala tributaries added",
                   len(SRIVIJAYA_TRIBUTARIES)))

    # Aragon guaranteeing Sicily is the 1282 Vespers — gone. The
    # PAP->SIC guarantee STAYS: a papal guarantee over Roger's county
    # is the Melfi relationship in miniature.
    src, n_ara = re.subn(
        r"^[ \t]*scripted_oneway = \{ first = ARA second = SIC [^}\n]*\}[ \t]*(?:#[^\n]*)?\n",
        "", src, flags=re.M)
    if n_ara != 1:
        sys.exit(f"expected exactly 1 ARA->SIC guarantee, stripped {n_ara}")
    report.append(("Vespers-era ARA->SIC guarantee removed", n_ara))

    # HRE slice: HAB's three 1337 embargoes are Habsburg-era politics
    # with no 1066 defense. (The HRE slice's second strip here —
    # PAP->FAE, the war-blocking vassal over a Faenza that belonged to
    # the IMPERIAL archbishop's world — is RETIRED: Italy North makes
    # FAE itself landless and the generic landless sweep above now owns
    # that line; its count carries the ledger entry.)
    src, n_emb = re.subn(
        r"^[ \t]*scripted_oneway = \{ first = \w+ second = HAB type = embargo_nation \}[ \t]*(?:#[^\n]*)?\n",
        "", src, flags=re.M)
    if n_emb != 3:
        sys.exit(f"expected exactly 3 HAB embargoes, stripped {n_emb}")
    report.append(("Habsburg-era embargoes removed", n_emb))

    # Italy North (2026-07-29 package): the 1330s Scaliger/Savoyard/
    # Venetian web dies where it crosses this slice's thrones —
    # SAV->PIE (Adelaide is the SENIOR: the house of Savoy are her
    # in-laws on the rise — deleted, not flipped, package decision G),
    # VER->PAD and VER->PAR (Scaliger conquests of the 1320s), and
    # VEN->RAG (1066 Ragusa sits in the Byzantine orbit; vanilla
    # 12_diplomacy.txt:219). SAV->CEV and VER->LUC died in the
    # landless sweep above — CEV and LUC empty into PIE and TUS.
    n_nit = 0
    for _pair in ("SAV second = PIE", "VER second = PAD",
                  "VER second = PAR", "VEN second = RAG"):
        src, _k = re.subn(
            r"^[ \t]*dependency = \{ first = " + _pair
            + r" subject_type = vassal \}[ \t]*(?:#[^\n]*)?\n",
            "", src, flags=re.M)
        n_nit += _k
    if n_nit != 4:
        sys.exit(f"expected exactly 4 Italy North vassal strips, stripped {n_nit}")
    report.append(("Italy North 1337 vassal ties removed", n_nit))

    # The march of Tuscany's one tie: Pisa under Beatrice — the
    # margravial suzerainty over the young commune [U]. Plain vassal on
    # purpose (package decision G; no reform gate exists for vassals).
    _wrap = src.rindex("\n}")
    src = (src[:_wrap]
           + "\n\t# 1066: the march of Tuscany (generated)\n"
           + "\tdependency = { first = TUS second = PIS subject_type = vassal }\n"
           + src[_wrap:])
    report.append(("Tuscan vassalage added", 1))

    # The Melfi investiture: Guiscard and Richard as papal
    # TRIBUTARIES (papal_investiture_reform carries the modifier —
    # the khutba pattern's fourth use, first theocracy overlord).
    _wrap = src.rindex("\n}")
    _itribs = "".join(
        f"\tdependency = {{ first = {o} second = {s} subject_type = tributary }}\n"
        for o, s in ITALY_TRIBUTARIES)
    src = (src[:_wrap]
           + "\n\t# 1066: the Melfi investiture (generated)\n"
           + _itribs + src[_wrap:])
    report.append(("Melfi tributaries added", len(ITALY_TRIBUTARIES)))

    def validate():
        if re.search(r"appanage", re.sub(r"#[^\n]*", "", src)):
            return "an appanage reference survived the strip"
        # Exactly 10 in vanilla 1.3.11. If a patch changes the number, this
        # fails loudly and a human re-reads the file — better than drifting.
        if n != 10 or before - after != n:
            return f"expected exactly 10 appanage cuts, removed {n} ({before} -> {after})"
        if n_eng != 6:
            return f"expected exactly 6 English subjection cuts, removed {n_eng}"
        if re.search(r"^[ \t]*dependency = \{ first = ENG ", src, re.M):
            return "an English subjection survived the strip"
        if n_future_deps != 27:
            return (f"future-dated dependency count changed: {n_future_deps} "
                    f"(expected 27) — re-read the file before deciding anything")
        return None

    # `after` feeds the appanage-count assertion above and is measured
    # BEFORE the English strip; the kept-count message recounts the final
    # text so it cannot go stale again.
    kept = len(re.findall(r"^[ \t]*dependency = \{", src, re.M))
    return src, report, validate, f"{kept} dependencies kept"


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
