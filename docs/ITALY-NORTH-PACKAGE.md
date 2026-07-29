# ITALY NORTH — approved implementation package (2026-07-29 night)

RUNS AFTER the Germany II batch is committed (needs its
weimar_dynasty and its build state).

USER DECISIONS (final): TUS revived via formable reuse. FLO empties
(TUS = 33 locations). ISR = new tag for Ulric I of Weimar (Istria).
RAV takes faenza + imola (FAE and IMO empty).
Main-session decisions: Brescia Tier B NOT taken (bank as optional;
asola still rides with the MAN grants — Boniface held it). Adelaide
of Susa enters as a LITERAL first name "Adelaide" (name_adelaide's
piedmontese row renders "Lalsia" — the Otakar literal precedent).
Albert Azzo II seats on PAD, not MLO (his real county; vanilla's term
sits on MLO — if the accessions-match-vanilla harness check trips,
teach it minimally with a comment). GEN/VEN anachronistic reforms
(compagna_communis, council_of_forty/ten, signoria/podesta) are
BANKED as known-wrong, not stripped in this pass. VER: attempt the
government swap to catholic_monarchy_no_coast + margraviate reform
following the HAB margraviate precedent; if the nested-include diff
shows anything beyond the include+rank swap, leave the Scaliger shape
and report.

## A. Registry additions (zz_1066_new_countries.txt)

TUS = {
	color = map_TUS
	color2 = rgb { 16 41 202 }

	culture_definition = tuscan
	religion_definition = catholic
}
(map_TUS is vanilla — cited by the formable at
00_formable_countries.txt:4228-4253; verify the named color exists,
then no new color entry needed.)

ISR = {
	color = map_ISR
	color2 = rgb { 16 41 202 }

	culture_definition = <the POP-majority culture of the Istrian
	locations — read pola/rovinj/pazin/buzet in
	location_templates.txt and use the majority value; the PLM
	precedent: primary = pop reality, the German margrave is the
	RULER's culture only>
	religion_definition = catholic
}
map_ISR is NEW — add to zz_1066_map_colors.txt (pick an unused
Adriatic-ish color; comment it). Add ISR to verify_mod's
_GENERATOR_OK with a tier-3-style comment (no bespoke arms yet).
ISR freeness was verified three ways by the research pass; re-run the
three greps quickly and cite them in your report.

## B. NEW_COUNTRIES blocks

TUS: rank_duchy, capital = lucca, includes per ZAH/SAX/SWA shape.
ISR: rank_county [or rank_duchy if the march precedent HAB uses
rank_duchy — copy HAB's rank], capital = pazin, same include stack.
Add TUS to the HRE members list (build_ios surgery — ISR too: the
march of Istria was imperial; verify AQU/VER are members, they are).

## C. Rulers

| tag | character key | name | accession | birth | regnal | dynasty | notes |
|---|---|---|---|---|---|---|---|
| TUS | tus_beatrice_di_bar | name_beatrix (vanilla :3132; renders "Beatrice" via culture tuscan) | 1052.5.6 | 1020.1.1 | 0 | de_bar_dynasty (VANILLA 04_dynasties.txt:5959 — reuse; her birth house, correct until Matilda) | female = yes (verify the vanilla female-character field shape first and cite one) |
| ISR | isr_ulrich_i_weimar | name key: check vanilla for name_ulric/name_ulrich/name_udalrich — if all missing, literal "Ulric" | 1060.1.1 | 1030.1.1 | 1 | weimar_dynasty (arrives with Germany II — verify present) | brother-house of MEI's Otto |
| AQU | aqu_ravengerius | literal "Ravenger" (name_ravenger missing — Otakar precedent) | 1063.1.1 | 1010.1.1 | 0 | none (patriarch) | |
| RAV | rav_henry_ravenna | name_henry (vanilla :8755) | 1051.1.1 | 1010.1.1 | 0 | none (archbishop) | |
| PAR | par_cadalus | literal "Cadalus" | 1045.1.1 | 1010.1.1 | 2 | none (bishop; the antipope Honorius II — situation material, do NOT model the papal claim in data) | |
| PIE | pie_adelaide_susa | LITERAL "Adelaide" | 1034.1.1 | 1015.1.1 | 0 | arduinici_dynasty NEW | female = yes |
| MFA | mfa_ottone_ii_monferrato | VANILLA character — vanilla's own term 1045.1.1 regnal 2; check whether the mod's death-strip left him alive and simply seat via HISTORICAL_RULERS like other vanilla-character seats (the sav/ven precedent below) | 1045.1.1 | — | 2 | vanilla | |
| PAD | mlo_alberto_azzo_ii_este | vanilla character, cross-tag seat (CHR precedent: kie_ character on CHR) | 1029.1.1 | — | 2 | vanilla deste | |

SAV (sav_pierre_i_savoy) and VEN (ven_domenico_contarini) are ALREADY
seated — verify, touch nothing.
MLO/GEN/PIS/VER/BLG stay ruler = random DELIBERATELY.

## D. Dynasties (04_zz_1066_dynasties.txt)

canossa_dynasty home canossa  (Matilda's future — created now, used
by the heir entry if one is authored; author Matilda as a non-ruler
character ONLY if the mod already has a non-ruler-character precedent;
otherwise skip her entirely and note it)
arduinici_dynasty home turin
Both need loc rows. de_bar_dynasty is vanilla — no entry.

## E. Territory — _NITALY_GRANTS

"TUS": lucca massa pescia florence mangona poggibonsi sanlorenzo
       arezzo prato pistoia volterra cortona sansepolcro siena
       massamar chiusi montalcino grosseto            (Tuscany 18)
       canossa reggioem guastalla mantova goito ostiglia mirandola
       asola modena frassinoro nonantola ferrara ficarolo comacchio
       argenta                                        (Emilia 15)
  donors: LUC FLO PRA PST VLT COT PEA SIE MAN FER — verify each
  location's CURRENT owner in the built 10_countries and STOP on any
  mismatch.
"BGM": bergamo cortenuova clusone zogno                (from MLO)
"CRM": cremona casalmaggiore soncino                   (from MLO)
"LDI": lodi                                            (from MLO)
"NVA": novara arona domodossola varallo                (from MLO)
"VRC": vercelli biella                                 (from MLO)
"PCZ": piacenza bardi fiorenzuola                      (from MLO)
"LCA": como lugano                                     (from MLO)
"CHV": chiavenna bormio tresivio                       (from MLO)
  (8 grants = 22 locations = exactly MLO's own_control_conquered;
   MLO keeps milano legnano rho varese monza lecco treviglio)
"VIN": vicenza bassano schio                           (from VER)
"CEN": ceneda conegliano                               (from VER)
"FEL": feltre belluno                                  (from VER)
"TRV": treviso castelfranco mestre                     (from VER)
"TNT": rovereto                                        (from VER)
"AQU": cividale                                        (from VER)
"ISR": pola rovinj                                     (from VEN)
       pazin buzet metlika kocevje                     (from AQU — partially reverses the HRE slice's grant, per the user's ISR decision)
       postojna novo_mesto                             (verify current owner first; if not AQU or a clean donor, STOP and report)
"PAD": rovigo                                          (from FER)
"CRO": pag                                             (from VEN)
"PIE": lanzo cuneo saluzzo carmagnola chieri alba mondovi ceva
  donors: MFA PRO SAL CHX ABA MND CEV — verify each.
"MFA": alessandria                                     (from ASD)
"SAV": aosta chatillonaos morgex                       (from AOS)
"RAV": faenza imola                                    (from FAE, IMO)

NITALY_LANDLESS = LUC FLO PRA PST VLT COT SIE MAN FER SAL CHX ABA
                  MND CEV ASD AOS FAE IMO           (18 tags)
All keep registry identity; former holdings become claims (the
GRA/POR shape the build automates).
VEN also drops its `control = { este }` line (este is PAD's own_core)
— FIELD_FIXES or a targeted strip; verify first.

## F. Include swaps (FIELD_FIXES — the restate-what-you-drop rule)

Revivals now landed need the landed include variant:
BGM CRM NVA VRC PCZ = catholic_republic_not_present -> these are
BISHOP-COUNTS in 1066: use catholic_bishopric_no_coast (CNV's include,
attested in the build) and country_rank per CNV.
LDI CHV = catholic_monarchy_not_present -> catholic_bishopric_no_coast.
VIN TRV FEL = catholic_republic_not_present -> catholic_bishopric_no_coast
(their 1066 holders are their bishops).
CEN = catholic_bishopric_not_present -> catholic_bishopric_no_coast.
RAV PAR: catholic_republic* -> catholic_bishopric (AQU's exact
include; check coast — Ravenna is coastal, use the coastal variant if
one exists; otherwise AQU's).
For EVERY swap: diff the nested includes of old vs new template
(location_templates / setup templates tree) and restate what the
dropped template provided if the new one lacks it. Report the diff
per tag in one line each.

## G. Diplomacy (build_diplomacy)

REMOVE: SAV->CEV, SAV->PIE (Adelaide is the senior — delete, do not
flip), VER->PAD, VER->PAR, VER->LUC, VEN->RAG (all 1330s facts).
ADD: dependency = { first = TUS second = PIS subject_type = vassal }.
The landless-dep auto-strip will take the deps whose subject empties;
observe the constant and move it.

## H. Left alone deliberately

GEN PIS BLG CES RIM TTE MSP CRR TTN PTG URB GUB PES all keep their
current state. Brescia block stays with VER (banked). Vanilla female
character warning: if `female = yes` is NOT the attested field shape,
find the real one from a vanilla female character and use that.
