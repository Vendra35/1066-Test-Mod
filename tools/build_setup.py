#!/usr/bin/env python3
"""Phase 1 — generate the setup files that carry 1337-dated people and dates.

The 1066 start inherits vanilla's 1337 setup, which is wrong in one specific,
mechanical way: its dates are all in the future. The engine rejects those
entries, collapses them to `1.1.1`, seats rulers born around 1312 who display at
about -250 years old, and — measured — floods error.log with tens of thousands
of script errors once the game runs. See docs/KNOWLEDGE.md.

This script removes the dated parts and leaves everything else byte for byte as
vanilla has it. Rulers become `ruler = random`, which is how a published
conversion solves the same problem.

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
# tag -> character key. Anything not listed keeps `ruler = random`.
# Every entry is checked: the character must exist in the generated
# 05_characters.txt and be at least ADULT_AGE at START_DATE. A typo here does not
# error in game — it leaves an empty throne and an engine-generated regent — so
# the check below is the only thing that catches one.
HISTORICAL_RULERS = {
    # North Sea, 1066. All four already exist in vanilla, which ships regnal
    # chains back to 886 and 188 characters who are adults in 1066.
    "ENG": "eng_harold_godwinson",       # d. 1066.10.14 at Hastings — one month in
    "NRM": "eng_william_the_conquerer",  # Duke of Normandy; rank_duchy, capital rouen
    "DAN": "dan_sweyn_estridsson",       # King of Denmark 1047-1076
    "SCO": "sco_malcolm_iii",            # King of Scots 1058-1093
    "NOR": "nor_harald_hardrada",        # written below — vanilla has no Norwegian alive in 1066
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
	# Harald Sigurdsson "Hardrada", king 1046-1066, of the Fairhair line through
	# Sigurd Syr. He dies at Stamford Bridge on 1066.9.25 — ten days into the
	# campaign — which is the history and is meant to happen.
	nor_harald_hardrada = {
		first_name = { name = name_harold }
		culture = norwegian
		religion = catholic
		birth_date = 1015.1.1
		birth = ringerike
		death_date = 1066.9.25
		dynasty = fairhair_dynasty
		tag = NOR
	}

	# Sons, written after their father. They give the succession something real
	# to land on when Hardrada dies; without them Norway would fall to a
	# generated heir ten days into the game.
	nor_magnus_ii = {
		first_name = { name = name_magnus }
		culture = norwegian
		religion = catholic
		birth_date = 1048.1.1
		birth = nidaros
		death_date = 1069.4.28
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
		death_date = 1093.9.22
		dynasty = fairhair_dynasty
		father = nor_harald_hardrada
		tag = NOR
	}
"""


# ------------------------------------------------------------------ tools ---
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

    for tag, char in sorted(HISTORICAL_RULERS.items()):
        pat = re.compile(r"(^\t" + tag + r" = \{.*?^[ \t]*)ruler = random", re.M | re.S)
        src, k = pat.subn(r"\1ruler = " + char, src, count=1)
        if not k:
            sys.exit(f"HISTORICAL_RULERS: no `ruler = random` found for {tag}")
    report.append(("historical rulers restored", len(HISTORICAL_RULERS)))

    src = tidy(src)
    after = len(re.findall(COUNTRY_RE, src, re.M))

    def validate():
        if after != before:
            return f"country count changed {before} -> {after}: territory would be lost"
        for key in COUNTRY_BLOCKS + COUNTRY_LINES:
            if re.search(r"^[ \t]*" + key + r"[ \t]*=", src, re.M):
                return f"{key} survived the strip"
        # Every remaining ruler must be random or a Phase 2 entry. This is the
        # check that catches a ruler line whose shape differs just enough to miss
        # the rewrite and leave that country a -250-year-old.
        stray = [m.group(1) for m in
                 re.finditer(r"^[ \t]*ruler[ \t]*=[ \t]*([A-Za-z0-9_]+)", src, re.M)
                 if m.group(1) != "random"
                 and m.group(1) not in HISTORICAL_RULERS.values()]
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
        if placed != HISTORICAL_RULERS:
            return (f"historical rulers landed in the wrong countries: "
                    f"expected {HISTORICAL_RULERS}, found {placed}")
        # No date may survive: at 1066 every one of them reads as the future.
        # Checked here rather than globally, because in 05_characters.txt
        # birth_date and death_date are exactly what the file is for.
        if re.search(r"^[ \t]*(start_date|end_date|date)[ \t]*=", src, re.M):
            return "a date survived — it would parse as future at 1066"
        return None

    return src, report, validate, f"{before} country blocks, all kept"


def build_ios(src):
    """International organizations carry regnal history for the HRE and the
    Papacy in exactly the same shape as countries. Safe to strip: an IO's head is
    `leader = <TAG>`, a country, not a character — so removing the terms cannot
    leave it headless the way it would a country."""
    report = []
    leaders = len(re.findall(r"^[ \t]*leader[ \t]*=", src, re.M))
    src, n = strip_blocks(src, "ruler_term")
    report.append(("ruler_term blocks removed", n))
    src = tidy(src)

    def validate():
        if re.search(r"^[ \t]*ruler_term[ \t]*=", src, re.M):
            return "ruler_term survived the strip"
        now = len(re.findall(r"^[ \t]*leader[ \t]*=", src, re.M))
        if now != leaders:
            return f"leader count changed {leaders} -> {now}"
        if re.search(r"^[ \t]*(start_date|end_date)[ \t]*=", src, re.M):
            return "a date survived — it would parse as future at 1066"
        return None

    return src, report, validate, f"{leaders} IO leaders, all kept"


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

        # Every historical ruler must exist and be an adult on the start date.
        for tag, key in sorted(HISTORICAL_RULERS.items()):
            if key not in pos:
                return f"HISTORICAL_RULERS[{tag}] = {key} is not a character"
            body = src[pos[key]:pos[key] + 700]
            bd = re.search(r"birth_date = (\d+)\.(\d+)\.(\d+)", body)
            if not bd:
                return f"{key} has no birth_date"
            born = tuple(int(x) for x in bd.groups())
            age = start[0] - born[0] - ((start[1], start[2]) < (born[1], born[2]))
            if age < ADULT_AGE:
                return (f"{key} is {age} at {start[0]}.{start[1]}.{start[2]} — "
                        f"under ADULT_AGE {ADULT_AGE}, the throne would sit empty")
            dd = re.search(r"death_date = (\d+)\.(\d+)\.(\d+)", body)
            if dd and tuple(int(x) for x in dd.groups()) < start:
                return f"{key} is already dead at the start date"
        return None

    return src, report, validate, f"{after} characters, {len(HISTORICAL_RULERS)} rulers checked"


TARGETS = [
    ("05_characters.txt", build_characters),
    ("10_countries.txt", build_countries),
    ("15_international_organizations.txt", build_ios),
]

HEADER = """# GENERATED by tools/build_setup.py — do not hand-edit.
# Source: vanilla {rel}
#
# Removed: entries carrying 1337-dated people or dates, which a 1066 start reads
# as the future. The engine rejects them, collapses them to `1.1.1`, and the
# result is rulers aged about -250 and a flood of script errors.
# Everything else — territory, capitals, ranks, templates, laws — is vanilla's.
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
