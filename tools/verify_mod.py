#!/usr/bin/env python3
"""Static verification harness — 1066 Test Mod.

Run after every change. Every check prints its item count, and a check that
finds nothing to scan FAILS rather than passing quietly: a silent zero is the
failure mode this whole discipline exists to prevent.

This is the GENERIC skeleton, deliberately rebuilt rather than copied from the
previous project — carrying that harness over would have imported ~15 checks
looking for files that do not exist here, which is exactly the vacuous-scan
problem in a new costume. Grow it: when the game finds a bug the harness did
not, that is two commits, the fix and the check, and the check gets proven
against a known positive before it is trusted.
"""
import re, sys, glob, os

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BS = chr(92)

# ---------------------------------------------------------------- vanilla ---
# Probe a known FILE, never the directory: an empty folder passes an isdir test
# and every later grep then returns a confident zero.
_PROBE = os.path.join("in_game", "map_data", "definitions.txt")

def _usable(p):
    return p is not None and os.path.isfile(os.path.join(p, _PROBE))

if os.environ.get("MR_VANILLA"):
    VAN = os.environ["MR_VANILLA"]
    if not _usable(VAN):
        sys.exit(f"MR_VANILLA is set but has no {_PROBE} under it: {VAN}")
else:
    _candidates = [
        r"E:\SteamLibrary\steamapps\common\Europa Universalis V\game",
        os.path.join(os.path.dirname(MOD), "EU5-Vanilla", "game"),
    ]
    VAN = next((p for p in _candidates if _usable(p)), None)
    if not VAN:
        sys.exit("vanilla reference tree not found — tried:\n  " + "\n  ".join(_candidates)
                 + "\nfix it before running (CLAUDE.md, REQUIRED SETUP), or set MR_VANILLA")

fails, skipped = [], []

# Checks for a kind of content the repo does not have yet are min_count=PENDING.
# It is not a licence to stay at zero: the moment the first file of that kind
# lands, the SAME commit raises the number to roughly what the repo holds, so a
# later deletion or a broken glob shows up as a vacuous scan instead of a quiet
# pass. Grep this name to find every check still owing that.
#
# The whole-repo CONTENT gate below cannot do this job. It is all-or-nothing:
# once ANY content exists it opens for EVERY check, so the first three .txt
# files in the repo turned five unrelated checks into failures at once.
PENDING = 0


def check(name, count, problems, min_count=1):
    if not CONTENT and min_count > 0:
        print(f"[SKIP] {name}: no mod content to scan yet")
        skipped.append(name)
        return
    status = "OK " if not problems and count >= min_count else "FAIL"
    if count < min_count:
        problems = problems + [f"(scan vacuous: only {count} items — expected >= {min_count})"]
    print(f"[{status}] {name}: {count} items")
    for p in problems[:25]:
        print(f"       - {p}")
    if problems:
        fails.append(name)

def _np(p):
    """Forward slashes always: several checks select files by substring, and on
    Windows glob returns backslashes. Three checks in the previous project
    scanned zero files for weeks because of exactly this."""
    return p.replace(os.sep, "/")

def read(p):
    return open(p, encoding="utf-8-sig").read()

def strip_comments(s):
    return re.sub(r"#.*", "", s)

# loading_screen belongs here: it is where vanilla keeps common/defines, so the
# start date lives in that tree. It was missing from this glob until the defines
# landed, which would have exempted START_DATE from the BOM and brace checks —
# the one file whose silent failure costs the most.
txt_files = sorted(_np(p) for p in
                   glob.glob(MOD + "/in_game/**/*.txt", recursive=True)
                   + glob.glob(MOD + "/main_menu/**/*.txt", recursive=True)
                   + glob.glob(MOD + "/loading_screen/**/*.txt", recursive=True))
yml_files = sorted(_np(p) for p in glob.glob(MOD + "/**/*.yml", recursive=True))
gui_files = sorted(_np(p) for p in glob.glob(MOD + "/**/*.gui", recursive=True))
all_files = txt_files + yml_files
CONTENT = bool(all_files)
code = {p: read(p) for p in txt_files}

print(f"mod content: {len(txt_files)} .txt, {len(yml_files)} .yml, {len(gui_files)} .gui")
if not CONTENT:
    print("NOTE: the harness is not guarding anything yet. Raise each check's\n"
          "      min_count as content lands, or the greens below mean nothing.\n")

# ------------------------------------------------------------ file hygiene ---
# setup/start is a BOM-FREE ZONE and the only one among .txt trees. All 25
# vanilla files there carry no BOM, nor do all 25 of a published conversion's,
# while everywhere else is overwhelmingly BOM'd (advances 215/215, templates
# 198/205, situations 23/23, on_action 21/21). A BOM there is read as a token:
#   pdx_persistent_reader.cpp:289: Error: "Unexpected token: <BOM>" in file:
#   "setup/start/50_1066_rulers.txt"
# and the whole file is dropped — one recorded case crashed a new game outright.
# This check used to demand a BOM on every .txt and so enforced that bug.
BOM = b"\xef\xbb\xbf"
SETUP = "/setup/start/"

setup_txt = [p for p in txt_files if SETUP in p]
bom_files = [p for p in all_files if p not in setup_txt]

probs = [os.path.relpath(p, MOD) for p in bom_files
         if open(p, "rb").read(3) != BOM]
check("BOM on .txt and .yml (outside setup/start)", len(bom_files), probs, min_count=1)

probs = [os.path.relpath(p, MOD) for p in setup_txt
         if open(p, "rb").read(3) == BOM]
# Armed at 3: build_setup.py generates 05_characters, 10_countries and
# 15_international_organizations. Raise it again as more setup files land — a BOM
# here is the single most expensive byte in the project.
check("no BOM in setup/start", len(setup_txt), probs, min_count=3)

# .gui is the other exception: vanilla ships 483 and only 49 carry a BOM.
probs = [os.path.relpath(p, MOD) for p in gui_files
         if open(p, "rb").read(3) == BOM]
check("no BOM on .gui", len(gui_files), probs, min_count=0)

probs = []
for p in txt_files:
    s = strip_comments(read(p))
    if s.count("{") != s.count("}"):
        probs.append(f"{os.path.relpath(p, MOD)}: {{={s.count('{')} }}={s.count('}')}")
check("braces balanced per file", len(txt_files), probs, min_count=1)

stray = glob.glob(MOD + "/in_game/localization/**/*.yml", recursive=True)
check("no in_game localization tree", 1,
      [os.path.relpath(p, MOD) for p in stray], min_count=0)

# Two loc files with the same NAME in different trees: the duplicate shadows
# the other and its keys vanish silently.
seen = {}
probs = []
for p in yml_files:
    seen.setdefault(os.path.basename(p), []).append(os.path.relpath(p, MOD))
for n, where in seen.items():
    if len(where) > 1:
        probs.append(f"{n} appears in {len(where)} trees: {where}")
check("no duplicate loc filenames", len(yml_files), probs, min_count=0)

# ------------------------------------------------------------ localisation ---
probs, count = [], 0
for p in yml_files:
    src = read(p)
    for i, line in enumerate(src.split(chr(10)), 1):
        t = line.strip()
        if not t or t.startswith("#") or re.match(r"^l_[a-z_]+:$", t):
            continue
        count += 1
        if not re.match(r"^ [A-Za-z0-9_.]+:\s", line):
            probs.append(f"{os.path.relpath(p, MOD)}:{i}: not a `key: value` line -> {t[:50]}")
        elif re.match(r'^ [A-Za-z0-9_.]+:\s*"', line) and not line.rstrip().endswith('"'):
            probs.append(f"{os.path.relpath(p, MOD)}:{i}: value opens a quote it never closes")
check("loc lines are well formed", count, probs, min_count=PENDING)  # first .yml

keys, dupes = set(), []
for p in yml_files:
    for m in re.finditer(r"^ ([A-Za-z0-9_.]+):", read(p), re.M):
        if m.group(1) in keys: dupes.append(m.group(1))
        keys.add(m.group(1))
check("no duplicate loc keys", len(keys), sorted(set(dupes)), min_count=PENDING)  # first .yml

# -------------------------------------------------------- dates and ages ---
# The start date is mirrored into three defines trees because the evidence for
# which one the engine reads is split (docs/KNOWLEDGE.md). Mirroring is only
# safe while the copies agree: three files quietly disagreeing about what year
# the game starts is precisely the silent failure this harness exists to catch.

def _date_year(s):
    return int(s.split(".")[0])

define_files = sorted(_np(p) for p in
                      glob.glob(MOD + "/*/common/defines/**/*.txt", recursive=True))
probs, dated = [], {}
for p in define_files:
    src = strip_comments(read(p))
    found = dict(re.findall(r'(START_DATE|END_DATE)' + BS + 's*=' + BS + 's*"([0-9.]+)"', src))
    if found:
        dated[os.path.relpath(p, MOD)] = found

for rel, d in sorted(dated.items()):
    for key in ("START_DATE", "END_DATE"):
        if key not in d:
            probs.append(f"{rel}: declares the other date but not {key}")
    if len(d) == 2 and _date_year(d["START_DATE"]) >= _date_year(d["END_DATE"]):
        probs.append(f"{rel}: START_DATE {d['START_DATE']} is not before END_DATE {d['END_DATE']}")

for key in ("START_DATE", "END_DATE"):
    values = {d[key] for d in dated.values() if key in d}
    if len(values) > 1:
        probs.append(f"{key} disagrees across trees: "
                     + ", ".join(f"{r}={d[key]}" for r, d in sorted(dated.items()) if key in d))

# min_count is 3 because three mirrored copies is what the repo ships. Drop it
# only together with the mirroring decision it guards.
check("start/end date mirrored and consistent", len(dated), probs, min_count=3)

# Ages carry ABSOLUTE years and do not move with START_DATE. We ship no age
# override, so this reads vanilla's file — the scan is never vacuous, and the
# day an override does land it is checked without touching this code.
_mod_age = sorted(glob.glob(MOD + "/in_game/common/age/*.txt"))
_age_src = read(_np(_mod_age[0])) if _mod_age else read(VAN + "/in_game/common/age/00_default.txt")
_age_from = os.path.relpath(_mod_age[0], MOD) if _mod_age else "vanilla 00_default.txt"

ages, probs = [], []
_starts = [(m.start(), m.group(1)) for m in
           re.finditer(r"^([a-z_0-9]+) = " + BS + "{", strip_comments(_age_src), re.M)]
for i, (pos, name) in enumerate(_starts):
    end = _starts[i + 1][0] if i + 1 < len(_starts) else len(_age_src)
    m = re.search(r"^" + BS + "s+year = ([0-9]+)", strip_comments(_age_src)[pos:end], re.M)
    if not m:
        probs.append(f"{name}: no year field")
    else:
        ages.append((name, int(m.group(1))))

for (an, ay), (bn, by) in zip(ages, ages[1:]):
    if by <= ay:
        probs.append(f"{bn} year {by} does not come after {an} year {ay}")

if ages and dated:
    start_year = _date_year(next(iter(dated.values()))["START_DATE"])
    if start_year < ages[0][1]:
        probs.append(f"START_DATE year {start_year} is before the first age "
                     f"({ages[0][0]} year {ages[0][1]}) — the game would start outside every age")
    else:
        _in = [a for a in ages if a[1] <= start_year][-1]
        _nxt = next((a for a in ages if a[1] > start_year), None)
        _span = (_nxt[1] - start_year) if _nxt else "to END_DATE"
        print(f"       start year {start_year} falls in {_in[0]}; "
              f"{_span} years until {_nxt[0] if _nxt else 'the end'}")

check(f"ages ascending and start date inside one ({_age_from})", len(ages), probs, min_count=6)

# ---------------------------------------------- the engine's own documentation ---
# docs/EU5-Vanilla-Script-Docs/ is the output of `script_docs` and
# `dump_data_types`. It says what is LEGAL, where grepping vanilla only ever
# said what someone happened to write.
_SD = MOD + "/docs/EU5-Vanilla-Script-Docs"
if not os.path.isdir(_SD):
    print("[FAIL] engine script docs missing — regenerate per CLAUDE.md")
    fails.append("engine script docs present")
else:
    def _headed(fname, lvl):
        out, cur = {}, None
        for _l in read(_np(os.path.join(_SD, fname))).split(chr(10)):
            if _l.startswith(lvl) and not _l.startswith(lvl + "#"):
                cur = _l[len(lvl):].strip(); out[cur] = []
            elif cur is not None:
                out[cur].append(_l)
        return out

    TRIGGERS = _headed("triggers.log", "## ")
    EFFECTS = _headed("effects.log", "## ")
    EVENT_TARGETS = _headed("event_targets.log", "### ")
    MODIFIERS = {}
    for _l in read(_np(os.path.join(_SD, "modifiers.log"))).split(chr(10)):
        _m = re.match(r"Tag: ([a-z_0-9]+), Categories: (.*)", _l.strip())
        if _m:
            MODIFIERS[_m.group(1)] = {c.strip().lower() for c in _m.group(2).split(",") if c.strip()}
    ON_ACTIONS = set(re.findall(r"^([a-z_0-9]+):$",
                                read(_np(os.path.join(_SD, "on_actions.log"))), re.M))
    print(f"[OK ] engine script docs loaded: {len(TRIGGERS)} triggers, "
          f"{len(EFFECTS)} effects, {len(EVENT_TARGETS)} event targets, "
          f"{len(MODIFIERS)} modifier tags, {len(ON_ACTIONS)} on_actions")

    def supported_scopes(name):
        """The scopes a trigger or effect is legal in, straight from the docs."""
        for line in TRIGGERS.get(name, []) + EFFECTS.get(name, []):
            m = re.search(r"\*\*Supported Scopes\*\*:\s*(.+)", line)
            if m:
                return [x.strip() for x in m.group(1).split(",") if x.strip()]
        return []

    # Modifier tags must exist. NOT their category: every tag also carries
    # "All", so a category comparison can never fail — and it would be wrong,
    # since the category says what a modifier AFFECTS, not where it may be
    # declared (siege_ability is documented Unit yet works in a country block).
    probs, count = [], 0
    for p in glob.glob(MOD + "/main_menu/common/static_modifiers/*.txt"):
        for _m in re.finditer(r"^([A-Za-z_0-9]+) = " + BS + "{(.*?)^" + BS + "}",
                              strip_comments(read(_np(p))), re.M | re.S):
            for _line in _m.group(2).split(chr(10)):
                _k = re.match(r"[ " + BS + "t]*([a-z_0-9]+) = ", _line)
                if not _k or _k.group(1) in ("game_data", "category"): continue
                count += 1
                if _k.group(1) not in MODIFIERS:
                    probs.append(f"{_m.group(1)}: '{_k.group(1)}' is not a modifier tag")
    check("modifier tags exist in engine docs", count, probs, min_count=PENDING)  # first static_modifier

    probs, count = [], 0
    for p in glob.glob(MOD + "/in_game/common/on_action/*.txt"):
        oa = strip_comments(read(_np(p)))
        hooks = set(re.findall(r"^([a-z_0-9]+) = " + BS + "{", oa, re.M))
        own = hooks & set(re.findall(r"^[ " + BS + "t]+([a-z_0-9]+)$", oa, re.M))
        for h in sorted(hooks - own):
            count += 1
            if h not in ON_ACTIONS:
                probs.append(f"{h} is not an on_action the engine declares")
    check("on_action hooks exist in engine docs", count, probs, min_count=PENDING)  # first on_action

# ------------------------------------------------------------- geography ---
defs = read(VAN + "/in_game/map_data/definitions.txt")
probs, count = [], 0
refs = set()
for p, s in code.items():
    b = strip_comments(s)
    refs |= {("region", x) for x in re.findall(r"region:([a-z_0-9]+)", b)}
    refs |= {("area", x) for x in re.findall(r"area:([a-z_0-9]+)", b)}
    refs |= {("location", x) for x in re.findall(r"location:([a-z_0-9]+)", b)}
for p in glob.glob(MOD + "/in_game/common/scripted_geography/*.txt"):
    for kind, members in re.findall(r"(region|area|province_definition|location) = "
                                    + BS + "{([^}]*)" + BS + "}",
                                    strip_comments(read(_np(p)))):
        for n in members.split():
            refs.add(("province" if kind == "province_definition" else kind, n))
for kind, name in sorted(refs):
    count += 1
    if not re.search(r"\b" + re.escape(name) + r"\b", defs):
        probs.append(f"{kind}:{name} not in definitions.txt")
# Armed: the generated 15_international_organizations.txt carries 10 geography
# references (9 locations, 1 region). Raise this as region work adds more.
check("regions/areas/locations exist", count, probs, min_count=10)

# --------------------------------------------------------------- scopes ---
# `prev` is ONE scope hop, and only scope-CHANGING blocks count as hops:
# if / limit / AND / OR / NOT are transparent, so the nesting on screen is not
# the nesting prev walks. Two hops down (c:X -> situation:Y -> var:target) it
# lands on the SITUATION, and the engine reports
#   "left was 'country', right was 'situation'"  jomini_script_system.cpp:252
# That shipped in all three phases of the previous project and is RARE in the
# log, because the gate above it short-circuits nearly every tick — it cannot
# be relied on to surface in testing, which is exactly why it is a check.
_LINKS = {"owner", "top_owner", "ruler", "heir", "consort", "capital", "overlord",
          "top_overlord_or_this", "culture", "religion", "market", "province",
          "location", "area", "region", "this", "root", "prev", "from", "dynasty",
          "defender_leader", "attacker_leader", "employer", "country", "controller"}
_PREF = re.compile(r"^(c|scope|var|situation|region|area|location|culture|religion|"
                   r"scripted_geography|province|continent|sub_continent|character|"
                   r"trait|building|government_type|culture_group|casus_belli):")
_ITER = re.compile(r"^(every|any|random|ordered)_")
# scope:/var: are deliberately absent — their type is not knowable from the
# text, so they are never flagged.
_NOTC = re.compile(r"^(situation|region|area|location|scripted_geography|culture|"
                   r"religion|province|continent|sub_continent|character|dynasty|"
                   r"trait|building):|^(every|any|random|ordered)_"
                   r"(location|area|region|province|character|sub_unit|unit|building)")
_NOTCL = {"capital", "ruler", "heir", "consort", "culture", "religion", "market",
          "province", "location", "area", "region", "dynasty"}
_CT = re.compile(r"^\s*(has_truce_with|top_overlord_or_this|is_subject_of|is_neighbor_of|"
                 r"is_at_war_with|is_rival_of|cancel_subject|target|first|second|this|"
                 r"overlord|owner|top_owner)\s*\??=\s*prev\s*$")
_OPEN = re.compile(r"^\s*([A-Za-z0-9_:.\-]+)\s*\??=\s*\{\s*$")


def _prev_findings(src, rel):
    found, seen, stack, depth = [], 0, [], 0
    for n, raw in enumerate(src.splitlines(), 1):
        line = re.sub(r"#.*", "", raw)
        if not line.strip():
            continue
        if _CT.match(line):
            seen += 1
            parent = stack[-2][0] if len(stack) >= 2 else "<file root>"
            if _NOTC.match(parent) or parent in _NOTCL:
                found.append(f"{rel}:{n}: prev resolves to '{parent}', not a country"
                             f" -> {line.strip()[:48]}")
        m = _OPEN.match(line)
        if m:
            depth += 1
            k = m.group(1)
            if _PREF.match(k) or _ITER.match(k) or k in _LINKS:
                stack.append((k, depth))
            continue
        depth += line.count("{")
        for _ in range(line.count("}")):
            if stack and stack[-1][1] == depth:
                stack.pop()
            depth -= 1
    return found, seen


# Known positive: the exact shape that shipped broken, so a walker that stops
# walking cannot pass this check vacuously. A check never seen failing is
# untested — this one fails on demand, every run.
_canary = """
c:XXX = {
	if = {
		limit = {
			situation:some_situation = {
				var:target_country = {
					NOT = {
						top_overlord_or_this ?= prev
					}
				}
			}
		}
	}
}
"""
assert _prev_findings(_canary, "canary")[0], "prev scope walker is broken — canary not flagged"
assert not _prev_findings(_canary.replace("?= prev", "?= c:XXX"), "canary")[0],     "prev scope walker false-positives on the fixed form"

probs, count = [], 0
for p, s in code.items():
    f, seen = _prev_findings(s, os.path.relpath(p, MOD).replace(os.sep, "/"))
    probs += f
    count += seen
# prev.prev has zero uses anywhere in vanilla, so it is not attested syntax.
for p, s in code.items():
    for _ in re.finditer(r"prev\s*\.\s*prev|prevprev", strip_comments(s)):
        probs.append(f"{os.path.relpath(p, MOD)}: prev.prev is unattested syntax")
# Raise as script content lands; today the repo is almost all setup data.
check("prev lands on a country where one is required", count, probs, min_count=0)

print()
if fails:
    print(f"RESULT: {len(fails)} check(s) with findings: {', '.join(fails)}")
    sys.exit(1)
if skipped:
    print(f"RESULT: no findings, but {len(skipped)} check(s) had nothing to scan")
    sys.exit(0)
print("RESULT: all checks passed")
