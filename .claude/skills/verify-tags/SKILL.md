---
name: verify-tags
description: Resolve EU5 country tags, location, area, region, culture and religion identifiers against vanilla before they are used in mod code. Use whenever a tag, a place name or a culture/religion key appears in a task, a design note or a draft file — and always before writing setup data. A wrong identifier does not error; it silently does nothing.
---

# Verify tags and named references

## Why this exists

A wrong identifier is the quietest failure in EU5. The trigger simply never
matches, the location is simply never assigned, and nothing appears in any log.
This project is a whole-map 1066 conversion, so it will resolve identifiers by
the hundred — which makes a habit, not a one-off check, the only defence.

The trap is that wrong names look right. Historical plausibility is not
evidence: the English name of a place is frequently not its key.

## Reference paths

Detect, never assume. Probe a known FILE — an empty directory passes a directory
test and every grep against it then returns a confident zero.

```bash
STEAM_VAN="/e/SteamLibrary/steamapps/common/Europa Universalis V/game"
if [ -f "$STEAM_VAN/in_game/map_data/definitions.txt" ]; then
	VANILLA="$STEAM_VAN"
fi
```

## Country tags

**Vanilla ships 2246 tags. 2245 are exactly 3 characters; the one exception is
`DUMMY`, a placeholder in `_default.txt` that is not a country.** Counted across
the 46 files in `in_game/setup/countries/`, which are organised by region —
`anatolia.txt`, `balkans.txt`, `british_isles.txt`, …

**Count with the BOM stripped, or you will undercount.** These files carry a BOM
and the first tag in each sits on line 1 immediately after it, so a plain
`^[A-Z]{3} = {` regex silently misses one tag per file. That is how `ENG` first
appeared not to exist here — it is `british_isles.txt:1`, behind the BOM.

```bash
ls "$VANILLA/in_game/setup/countries/"
grep -rn 'ENG = {' "$VANILLA/in_game/setup/countries/"     # no ^ anchor
```

```python
# counting: always utf-8-sig
src = io.open(path, encoding="utf-8-sig").read()
re.findall(r"^([A-Za-z0-9]{2,8}) = \{", src, re.M)
```

Note also that a tag being absent here does not mean it is absent from the game:
`IRE` is in no country definition file, yet Ireland exists as a concept. Check
`main_menu/setup/start/10_countries.txt` too before declaring a tag missing.

Report whether it exists, what it is, and the `file:line`.

**On longer tags.** A published conversion ships 531 tags of which 471 are five
characters and 47 are four, used live in script (`c:ALASI`, `tag = ASYRI`), and
vanilla's own `DUMMY` is five. So the 3-character shape is a convention rather
than a proven engine limit — but no longer tag has been **verified in a running
game here**. Prefer 3 characters; if a longer one is ever needed, test that one
tag alone before building a scheme on it.

## Locations, areas, regions

`in_game/map_data/definitions.txt` is the authority — 10,557 lines, nested:

```
europe = {
	western_europe = {
		scandinavian_region = {
			svealand_area = {
				<locations>
```

So continent → subcontinent → region → area → location. Resolve the exact
string, and note which level it sits at, because triggers differ by level:

```bash
grep -n '\bstockholm\b'        "$VANILLA/in_game/map_data/definitions.txt"
grep -n 'svealand_area'        "$VANILLA/in_game/map_data/definitions.txt"
grep -n 'scandinavian_region'  "$VANILLA/in_game/map_data/definitions.txt"
```

`in_game/map_data/location_templates.txt` (28,573 lines, one entry per location)
says what each location IS — `topography`, `vegetation`, `climate`, `religion`,
`culture`, `raw_material`. Use it to check a location exists AND to read its
1337 culture and religion, which is the baseline any 1066 change is a delta from.

**Region reference PDFs.** `docs/` holds the wiki's per-region pages — Western
European, Eastern European, Middle Eastern, Central and North Asian, East Asian,
South Asian, Southeast Asian, African, North and South American, Oceania, plus
German and Japanese regions. Read with:

```bash
pdftotext -layout "docs/Western European subcontinent - Europa Universalis 5 Wiki.pdf" - | less
```

They are convenient for orientation and for finding what a region contains.
They are **secondary**: the wiki carries a *"last verified for version
pre-release"* banner, and two well-regarded external references checked during
this project's setup both contained false claims. Confirm against
`definitions.txt` before anything is written.

## Cultures, religions, governments, ranks

```bash
grep -rn 'english_culture'   "$VANILLA/in_game/common/cultures/"     | head
grep -rn 'catholic'          "$VANILLA/in_game/common/religions/"    | head
grep -rn 'monarchy'          "$VANILLA/in_game/common/government_types/" | head
grep -rn 'rank_kingdom'      "$VANILLA/in_game/common/country_ranks/"    | head
```

Enum values are one of the categories where writing from memory is forbidden
(CLAUDE.md). `country_rank`, `heir_selection`, `location_rank` and integration
levels all have exact vanilla spellings — read them, do not infer them.

## Characters

For a 1066 conversion, check whether a person already exists before authoring
them. Vanilla ships 7236 dated characters, 330 born 1000–1070, of whom 188 would
be aged 16–56 in 1066 — because vanilla's regnal chains reach back to 886.

```bash
grep -n -A8 '^\s*eng_harold_godwinson = {' "$VANILLA/main_menu/setup/start/05_characters.txt"
```

Note `birth_date` **and** `death_date`: a character who dies before or shortly
after the start date is not a usable long-term ruler.

## Order of evidence

1. Vanilla game files — the authority.
2. `docs/EU5-Vanilla-Script-Docs/` — what is legal, for triggers/effects/scopes.
3. Wiki PDFs in `docs/` — orientation only.
4. Other mods (Bronze Era, the reference mods) — how someone else did it, never
   proof that it is correct.

If a search returns nothing, the identifier is wrong. Say so and stop, rather
than substituting something that looks close.
