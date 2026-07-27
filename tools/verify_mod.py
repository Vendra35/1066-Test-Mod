#!/usr/bin/env python3
"""Static verification harness — 1178 Test Mod.

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

txt_files = sorted(_np(p) for p in
                   glob.glob(MOD + "/in_game/**/*.txt", recursive=True)
                   + glob.glob(MOD + "/main_menu/**/*.txt", recursive=True))
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
probs = [os.path.relpath(p, MOD) for p in all_files
         if open(p, "rb").read(3) != b"\xef\xbb\xbf"]
check("BOM on .txt and .yml", len(all_files), probs, min_count=1)

# .gui is the exception: vanilla ships 483 and only 49 carry a BOM.
probs = [os.path.relpath(p, MOD) for p in gui_files
         if open(p, "rb").read(3) == b"\xef\xbb\xbf"]
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
check("loc lines are well formed", count, probs, min_count=1)

keys, dupes = set(), []
for p in yml_files:
    for m in re.finditer(r"^ ([A-Za-z0-9_.]+):", read(p), re.M):
        if m.group(1) in keys: dupes.append(m.group(1))
        keys.add(m.group(1))
check("no duplicate loc keys", len(keys), sorted(set(dupes)), min_count=1)

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
    check("modifier tags exist in engine docs", count, probs, min_count=1)

    probs, count = [], 0
    for p in glob.glob(MOD + "/in_game/common/on_action/*.txt"):
        oa = strip_comments(read(_np(p)))
        hooks = set(re.findall(r"^([a-z_0-9]+) = " + BS + "{", oa, re.M))
        own = hooks & set(re.findall(r"^[ " + BS + "t]+([a-z_0-9]+)$", oa, re.M))
        for h in sorted(hooks - own):
            count += 1
            if h not in ON_ACTIONS:
                probs.append(f"{h} is not an on_action the engine declares")
    check("on_action hooks exist in engine docs", count, probs, min_count=1)

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
check("regions/areas/locations exist", count, probs, min_count=1)

print()
if fails:
    print(f"RESULT: {len(fails)} check(s) with findings: {', '.join(fails)}")
    sys.exit(1)
if skipped:
    print(f"RESULT: no findings, but {len(skipped)} check(s) had nothing to scan")
    sys.exit(0)
print("RESULT: all checks passed")
