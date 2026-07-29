# THE COAT-OF-ARMS SYSTEM — decoded, with the 1066 batch and its deferred tiers

> Produced by the CoA research pass (Opus agent, 2026-07-29 night),
> reviewed by the main session; the load-bearing claims (texture files
> on disk, colour names defined, SIC_ancient's vanilla line, the eight
> target tags' vanilla absence) re-verified inline before landing.
> User screenshots settled the headline: flags are NOT white — the
> engine GENERATES them.

## 1. The system

**Compositional, CK3-style** — `pattern` + `colored_emblem` /
`textured_emblem` + named colors; no per-tag art. The database:
`main_menu/common/coat_of_arms/coat_of_arms/` (9 vanilla files, 4583
keys), assets under `main_menu/gfx/coat_of_arms/` (66 patterns, 3594
colored emblems, 478 textured).

**The binding chain** (`flag_definitions/00_flag_definitions.txt:1`,
confirmed by the debug panel's `Flag` row in game): tag →
flag_definition list of the same name → highest-priority valid
`coa = KEY` → CoA database. **With no list, the tag ITSELF is the
COA_KEY.** `DEFAULT` is not a universal fallback (its 7 entries are
all trigger-gated colonial/pirate cases).

**Additive and key-merged; last-loaded file wins per key.** Zero of 24
examined published mods override the vanilla files — every one drops a
`zz_`-prefixed file into the same directory (Basileia states the rule
in `zz_br_flags.txt:1`). Dynasty arms live in the SAME directory.
Dated/conditional arms exist via flag_definition `priority` +
`trigger`; `coa_def_renaissance_age_2_trigger = no` is a perfect
276-year age-1 gate if ever needed.

**BOM:** vanilla ships all 14 files here BOM-free, but Basileia's
`zz_br_flags.txt` carries a BOM (measured: `efbbbf`) and works in a
popular published mod — ours ships WITH BOM, matching the harness rule.
If arms ever fail to render wholesale, strip the BOM first and add the
documented exception.

## 2. The generator (why nothing is ever white)

A missing entry errors NOTHING. `template_lists/coa_templates.txt:5`
is a weighted template pool gated by 289 `coa_def_*` scripted triggers
reading religion group, culture, government, rank, age and dynasty off
`scope:actor`; colors come from `color_lists.txt` (islamic:
red/black/green + white; christian: red-heavy + white). Vanilla itself
ships 280 landed 1337 tags with no arms at all — generation is the
designed path, not a failure.

**Measured on our own map (user screenshots, 2026-07-29):** PLM drew a
green field + white crescent (islamic pool, exactly the odds), VMD a
red field (christian pool's heaviest colour) — and the two Caliphates
drew EACH OTHER'S colours: ABS rendered white-with-red-border, FAT
rendered black-with-inscription. History inverted, silently. The
registry `color` field does NOT feed the flag (VMD's old-gold registry
colour vs its red generated flag is the disproof).

## 3. The batch (landed 2026-07-29 night — item 24)

`main_menu/common/coat_of_arms/coat_of_arms/zz_1066_flags.txt`,
9 keys:

| Key | Arms | Ground |
|---|---|---|
| SEL | blue, white double-headed eagle | vanilla's own `seljukids_dynasty` (pre_scripted_dynasties.txt:16080) |
| ABS | BLACK banner, white kufic square | al-raya al-sawda'; the generator cannot make it |
| FAT | WHITE, green naskh | the anti-Abbasid dynastic white; [U] green accent |
| APU | blue, checky bend | vanilla's NAP_hauteville charge (:27420) |
| PYS | blue, gold Rurikid tamga | ce_rurikid.dds, three vanilla dynasties wear it |
| ZAH | gold, red eagle | vanilla FBG's charge (:12504) |
| VMD | checky or-and-azure | [U] attested 12th c., conventional stand-in |
| DUB | red, raven banner | Norse-Gael Dublin |
| SIC_ancient | checky bend (OVERRIDE) | vanilla's default is the Hohenstaufen eagle — 128 years early; key-level override leaves every later variant's trigger intact |

HAB needs nothing: the generator-shown Bindenschild is historically
the Babenberg arms — correct for Ernst. `mathrafal_dynasty` and
`seljukids_dynasty` already ship as dynasty arms; `default_dynasty`
covers the rest.

## 4. The deferred tiers (the harness's `_GENERATOR_OK` mirrors this)

**Tier 3 — deferred until eyeballed in game (11 tags):** the six
Catalan counties (URG BSL CDY EPU RSL PLJ — `culture:catalan` already
feeds their pool partial senyera templates via `coa_def_senyera_trigger`;
the full senyera list is colonial/age-4-gated and does NOT fire at
1066), ULD (the Red Hand — vanilla ULS's cross is the 1177+ Norman
earldom, do not reuse), and CUP SLR NEA GAE. Sketches with texture
names live in the research transcript; every texture was
disk-verified.

**Tier 4 — permanent generator territory (22 tags):** 13 taifas
(SEV BDJ TOL CRD GRZ ALM MRU DYA ZGZ LRD ABR ALP QRM — GRZ must NEVER
reuse vanilla GRA's `ce_nasrid_motto.dds`, Nasrid is 1238+), PLM AGR,
and the 7 Seljuk clients (GHZ UQY MRD HLB SIS KKY SHD). These polities
had no heraldry; the generator's religion-gated designs are no less
historical than anything we would invent. If one is ever promoted, GHZ
first (a black field ties it to ABS, whose name was in its khutba).

## 5. The harness check

`verify_mod.py` "coat of arms references resolve" (92 items at
landing, min_count=90; proven by breaking three ways): textures and
patterns on disk (mod or vanilla), quoted colours defined in
named_colors, every registry tag either armed or in `_GENERATOR_OK`
(exact-set both directions), and no vanilla key overwritten outside
`_INTENTIONAL_COA_OVERRIDES` (sole member: SIC_ancient). A new-slice
tag now FAILS the harness until someone chooses its side — that is the
point.
