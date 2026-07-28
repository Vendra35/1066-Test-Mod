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
# Armed at 6: five generated files plus the additive 04_zz_1066_dynasties.
# Raise it again as more setup files land — a BOM here is the single most
# expensive byte in the project.
check("no BOM in setup/start", len(setup_txt), probs, min_count=6)

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
check("loc lines are well formed", count, probs, min_count=40)  # Norman Conquest loc

keys, dupes = set(), []
for p in yml_files:
    for m in re.finditer(r"^ ([A-Za-z0-9_.]+):", read(p), re.M):
        if m.group(1) in keys: dupes.append(m.group(1))
        keys.add(m.group(1))
check("no duplicate loc keys", len(keys), sorted(set(dupes)), min_count=40)  # Norman Conquest loc

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

# ------------------------------------------------------ named rulers seat ---
# A named ruler does NOT seat without an OPEN ruler_term (no end_date) whose
# start_date is before START_DATE — measured in game 2026-07-28: all five
# named-ruler countries started under engine-generated regents while every
# `ruler = random` country seated fine (docs/KNOWLEDGE.md). The invariant in
# the generated 10_countries.txt: named rulers and ruler_terms pair 1:1, every
# term is open and past-dated, and every named ruler has a term of their own.
_setup10 = _np(os.path.join(MOD, "main_menu", "setup", "start", "10_countries.txt"))
probs, count = [], 0
if os.path.isfile(_setup10):
    _s10 = strip_comments(read(_setup10))
    _named = [m.group(1) for m in
              re.finditer(r"^[ \t]*ruler[ \t]*=[ \t]*([a-z][a-z0-9_]*)", _s10, re.M)
              if m.group(1) != "random"]
    _terms = re.findall(r"ruler_term[ \t]*=[ \t]*" + BS + "{([^}]*)" + BS + "}", _s10)
    count = len(_named) + len(_terms)
    if len(_named) != len(_terms):
        probs.append(f"{len(_named)} named rulers but {len(_terms)} ruler_terms — they must pair 1:1")
    _start = None
    if dated:
        _start = tuple(int(x) for x in next(iter(dated.values()))["START_DATE"].split("."))
    _term_chars = set()
    for _t in _terms:
        _cm = re.search(r"character = ([a-z0-9_]+)", _t)
        _sm = re.search(r"start_date = ([0-9.]+)", _t)
        if _cm:
            _term_chars.add(_cm.group(1))
        if not _cm or not _sm:
            probs.append(f"ruler_term missing character or start_date: {{{_t.strip()[:60]}}}")
            continue
        if "end_date" in _t:
            probs.append(f"ruler_term for {_cm.group(1)} has an end_date — the current reign must be OPEN")
        if _start and tuple(int(x) for x in _sm.group(1).split(".")) >= _start:
            probs.append(f"ruler_term for {_cm.group(1)}: start_date {_sm.group(1)} is not before START_DATE")
    for _r in _named:
        if _r not in _term_chars:
            probs.append(f"named ruler {_r} has no ruler_term — the throne sits empty under a regent")
else:
    probs.append("main_menu/setup/start/10_countries.txt is missing")
# Armed at 140: 71 named rulers + 71 terms after the taifa factory.
# Raise together with HISTORICAL_RULERS as Phase 2 regions land.
check("named rulers carry an open, past-dated ruler_term", count, probs, min_count=140)

# ------------------------------------------ authored-content cross-refs ---
# Requested as the pre-test review pass and kept as permanent checks: every
# identifier OUR authored characters reference must resolve, because none
# of them errors in game — a bad dynasty, name key or birth location just
# renders wrong or not at all. The scripted-name registry is TWO loc files
# (character_names_dynamic + character_names — the second holds the
# literals; vanilla's own Tashfin/Ibrahim/Alp_Arslan live there), plus our
# own yml for keys we add. This check found its first real bug on its dry
# run: the literal `Tamim` had no loc entry anywhere.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("build_setup", os.path.join(MOD, "tools", "build_setup.py"))
_bs = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_bs)

_defs_txt = read(_np(VAN + "/in_game/map_data/definitions.txt"))
_dyn_reg = read(_np(VAN + "/main_menu/localization/english/character_names_dynamic_l_english.yml"))
_lit_reg = read(_np(VAN + "/main_menu/localization/english/character_names_l_english.yml"))
_our_loc = "".join(read(p) for p in yml_files)
_van_dyn = read(_np(VAN + "/main_menu/setup/start/04_dynasties.txt"))
_our_dynfile = ""
_our_dynpath = _np(os.path.join(MOD, "main_menu", "setup", "start", "04_zz_1066_dynasties.txt"))
if os.path.isfile(_our_dynpath):
    _our_dynfile = read(_our_dynpath)

probs, count = [], 0
_nc_src = _bs.NEW_CHARACTERS
for _m in re.finditer(r"^\t([a-z][a-z0-9_]*) = " + BS + "{", _nc_src, re.M):
    _key = _m.group(1)
    _end = _nc_src.find("\n\t}", _m.start())
    _body = _nc_src[_m.start():_end]
    _bodync = re.sub(r"#[^\n]*", "", _body)
    # dynasty resolves (vanilla or ours); dynasty-less is legal
    _dy = re.search(r"dynasty[ \t]*=[ \t]*([a-z_0-9]+)", _bodync)
    if _dy:
        count += 1
        if (_dy.group(1) + " = {") not in _van_dyn and (_dy.group(1) + " = {") not in _our_dynfile:
            probs.append(f"{_key}: dynasty {_dy.group(1)} exists nowhere")
    # name key resolves: name_ parts in the dynamic registry; literals in
    # the literal registry or our own loc
    _nm = re.search(r"name[ \t]*=[ \t]*([A-Za-z_0-9.]+)[ \t]*" + BS + "}", _bodync)
    if _nm:
        count += 1
        for _part in _nm.group(1).split("."):
            if _part.startswith("name_"):
                # A name key is a loc key (KNOWLEDGE): vanilla's dynamic
                # registry OR our own loc file both count — the taifa slice
                # ships three invented keys (name_abbad, name_badis,
                # name_abd_al_malik) patterned on name_abd_al_qadir.
                if f" {_part}:" not in _dyn_reg and f" {_part}:" not in _our_loc:
                    probs.append(f"{_key}: name part {_part} not in the dynamic registry or our loc")
            else:
                if f" {_part}:" not in _lit_reg and f" {_part}:" not in _our_loc:
                    probs.append(f"{_key}: literal name {_part} has no loc entry anywhere")
    # birth location exists
    _bl = re.search(r"birth[ \t]*=[ \t]*([a-z_0-9]+)", _bodync)
    if _bl:
        count += 1
        if not re.search(r"\b" + re.escape(_bl.group(1)) + r"\b", _defs_txt):
            probs.append(f"{_key}: birth location {_bl.group(1)} not in definitions.txt")
# our dynasties each carry a loc key
for _dk in re.findall(r"^\t([a-z_0-9]+) = " + BS + "{", strip_comments(_our_dynfile), re.M):
    count += 1
    if f" {_dk}:" not in _our_loc:
        probs.append(f"our dynasty {_dk} has no loc key")
# no character seated on two tags
_seated = [r[0] for r in _bs.HISTORICAL_RULERS.values()]
count += len(_seated)
for _c in set(_seated):
    if _seated.count(_c) > 1:
        probs.append(f"{_c} is seated on more than one tag")
# Armed at 200: 36 authored characters + 25 dynasties + 71 seats
# (209 measured after the taifa factory).
check("authored identifiers resolve (dynasty, name, birthplace, loc)", count, probs, min_count=200)

# Where vanilla ships its OWN ruler_term for the same character in the same
# country block, our accession date must MATCH it — vanilla is ground truth
# for ~30 of the 53 rows, and this turns "trust the research agent" into a
# machine comparison. Rows where vanilla has no such term (authored
# characters, cross-tag seats) are simply not compared.
_van10 = read(_np(VAN + "/main_menu/setup/start/10_countries.txt"))
_vblocks = list(re.finditer(r"^\t([A-Z0-9]{2,6}) = " + BS + "{", _van10, re.M))
probs, count = [], 0
_compared = 0
for _tag, _row in sorted(_bs.HISTORICAL_RULERS.items()):
    _char, _acc = _row[0], _row[1]
    for _i, _b in enumerate(_vblocks):
        if _b.group(1) != _tag:
            continue
        _e = _vblocks[_i + 1].start() if _i + 1 < len(_vblocks) else len(_van10)
        _terms = re.findall(r"ruler_term = " + BS + "{ character = " + _char
                            + r" start_date = ([0-9.]+)", _van10[_b.start():_e])
        if _terms:
            _compared += 1
            if _acc not in _terms:
                probs.append(f"{_tag}/{_char}: our accession {_acc} vs vanilla's own term(s) {_terms}")
        break
count = len(_bs.HISTORICAL_RULERS)
print(f"       accessions cross-checked against vanilla's own terms: {_compared} of {count}")
# Armed at 71 rows after the taifa factory; the printed compared-count is
# the real coverage figure (the thirteen emirs exist nowhere in vanilla,
# so the compared set stays at 31).
check("accessions match vanilla's own terms where vanilla has them", count, probs, min_count=71)

# Our authored character keys must not collide with vanilla's — repeated
# keys MERGE inside character_db (the QAR law), so a collision would
# silently overwrite a vanilla character with ours, no error anywhere.
_van05 = read(_np(VAN + "/main_menu/setup/start/05_characters.txt"))
probs, count = [], 0
_ours_keys = re.findall(r"^\t([a-z][a-z0-9_]*) = " + BS + "{", _bs.NEW_CHARACTERS, re.M)
for _k in _ours_keys:
    count += 1
    if re.search(r"^\t" + _k + r" = " + BS + "{", _van05, re.M):
        probs.append(f"{_k} already exists in vanilla — our block would silently merge over it")
if len(_ours_keys) != len(set(_ours_keys)):
    probs.append("duplicate key inside NEW_CHARACTERS itself")
# Armed at 21 authored characters.
check("authored character keys collide with nothing", count, probs, min_count=21)

# A character ALIVE at start (born before START_DATE) must carry NO
# death_date — a post-start one starts them DEAD, silently: reign closed on
# START_DATE, throne to a generated regent, zero error.log lines. But
# FUTURE-BORN characters must KEEP theirs: stripping those resurrected
# ~3,500 ancients and hard-froze the game on the first unpause
# (docs/KNOWLEDGE.md, both measured 2026-07-28).
_setup05 = _np(os.path.join(MOD, "main_menu", "setup", "start", "05_characters.txt"))
probs, count = [], 0
if os.path.isfile(_setup05):
    _s05 = strip_comments(read(_setup05))
    _start5 = (tuple(int(x) for x in next(iter(dated.values()))["START_DATE"].split("."))
               if dated else None)
    _blks5 = list(re.finditer(r"^\t([a-z][a-z0-9_]*) = " + BS + "{", _s05, re.M))
    for _i, _b in enumerate(_blks5):
        _e5 = _blks5[_i + 1].start() if _i + 1 < len(_blks5) else len(_s05)
        _body = _s05[_b.start():_e5]
        _dd = re.search(r"death_date[ \t]*=[ \t]*([0-9.]+)", _body)
        if not _dd:
            continue
        count += 1
        _bd = re.search(r"birth_date[ \t]*=[ \t]*([0-9.]+)", _body)
        if _start5 and _bd:
            # tolerant y.m.d: vanilla ships `birth_date = 1010.1.` (trailing
            # dot, "# unknown") — pad missing parts with 1 instead of crashing
            def _dt5(s):
                _p = [x for x in s.split(".") if x != ""]
                return tuple(int(x) for x in (_p + ["1", "1"])[:3])
            if _dt5(_bd.group(1)) < _start5 <= _dt5(_dd.group(1)):
                probs.append(f"{_b.group(1)}: alive at start but carries death_date "
                             f"{_dd.group(1)} — starts the game DEAD, silently")
else:
    probs.append("main_menu/setup/start/05_characters.txt is missing")
# Armed at 3000: ~4,045 death_dates remain after the scoped strip (543 past +
# ~3,502 on the future-born). A vacuous scan means the strip ate history.
check("no death_date on a character alive at start", count, probs, min_count=3000)

# --------------------------------------------------- situations and events ---
# Situation top-level fields, self-calibrated against vanilla: whatever field
# names vanilla's 23 situation files use at one-tab depth is the legal set;
# a typo'd field in ours does nothing, silently.
_van_sit = set()
for _p in glob.glob(VAN + "/in_game/common/situations/*.txt"):
    _van_sit |= set(re.findall(r"^\t([a-z_0-9]+)[ \t]*=", strip_comments(read(_np(_p))), re.M))
probs, count = [], 0
for _p in glob.glob(MOD + "/in_game/common/situations/*.txt"):
    for _f in re.findall(r"^\t([a-z_0-9]+)[ \t]*=", strip_comments(read(_np(_p))), re.M):
        count += 1
        if _f not in _van_sit:
            probs.append(f"{os.path.basename(_p)}: field '{_f}' appears in no vanilla situation")
# Armed at 5: norman_conquest.txt carries 5 top-level fields.
check("situation fields exist in vanilla's field set", count, probs, min_count=5)

# Every event id we REFERENCE in a namespace we DECLARE must be DEFINED by us.
# Both reference shapes are scanned — the plain `trigger_event_x = ns.1` and
# the delayed block `{ id = ns.1 days = N }`. The block form is the exact
# blind spot that once made two independent validators call 812 healthy
# vanilla events orphaned; it does not get to happen here.
_our_ns, _our_defined, _our_refs = set(), set(), []
_ev_files = [p for p in txt_files if "/in_game/events/" in p]
for _p in _ev_files:
    _s = strip_comments(read(_p))
    _our_ns |= set(re.findall(r"^namespace[ \t]*=[ \t]*([a-z_0-9]+)", _s, re.M))
    _our_defined |= set(re.findall(r"^([a-z_0-9]+" + BS + ".[0-9]+)[ \t]*=[ \t]*" + BS + "{", _s, re.M))
for _p in txt_files:
    _s = strip_comments(read(_p))
    _our_refs += [(m, _p) for m in re.findall(
        r"trigger_event[a-z_]*[ \t]*=[ \t]*([a-z_0-9]+" + BS + ".[0-9]+)", _s)]
    _our_refs += [(m, _p) for m in re.findall(
        r"id[ \t]*=[ \t]*([a-z_0-9]+" + BS + ".[0-9]+)", _s)]
probs, count = [], 0
for _id, _p in _our_refs:
    if _id.split(".")[0] not in _our_ns:
        continue    # a vanilla event; not ours to define
    count += 1
    if _id not in _our_defined:
        probs.append(f"{os.path.relpath(_p, MOD)}: {_id} is referenced but defined nowhere in our events")
# Armed at 10: the on_action schedules 9 refs and the situation fires .90.
check("referenced event ids in our namespaces are defined", count, probs, min_count=10)

# Every title/desc/option-name key in our events must exist in our loc — and
# so must war_name keys and the <cb>/<cb>_desc pair of every casus belli we
# define. A missing loc key shows as a raw key string in game, no error.
_loc_keys = keys    # collected by the duplicate-loc-keys check above
probs, count = [], 0
for _p in _ev_files:
    _s = strip_comments(read(_p))
    for _k in re.findall(r"^[ \t]*(?:title|desc|name)[ \t]*=[ \t]*([A-Za-z0-9_.]+)$", _s, re.M):
        if _k.split(".")[0] not in _our_ns:
            continue
        count += 1
        if _k not in _loc_keys:
            probs.append(f"loc key {_k} is referenced but not defined")
for _p in [p for p in txt_files if "/wargoals/" in p]:
    for _k in re.findall(r'war_name[ \t]*=[ \t]*"([A-Z0-9_]+)"', read(_p)):
        count += 1
        if _k not in _loc_keys:
            probs.append(f"war_name loc key {_k} is not defined")
for _p in [p for p in txt_files if "/casus_belli/" in p]:
    for _k in re.findall(r"^(cb_[a-z_0-9]+)[ \t]*=[ \t]*" + BS + "{", strip_comments(read(_p)), re.M):
        for _want in (_k, _k + "_desc"):
            count += 1
            if _want not in _loc_keys:
                probs.append(f"casus belli loc key {_want} is not defined")
# Armed at 40: 11 events x (title+desc+options) plus 2 war names and 2 CBs.
check("event, war and cb loc keys resolve", count, probs, min_count=40)

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
                # blocks_country_formation is a static-modifier FIELD, not a
                # modifier tag — vanilla's hundred_years_war_impact carries it
                # (static_modifiers/country.txt:6470).
                if not _k or _k.group(1) in ("game_data", "category",
                                             "blocks_country_formation"):
                    continue
                count += 1
                if _k.group(1) not in MODIFIERS:
                    probs.append(f"{_m.group(1)}: '{_k.group(1)}' is not a modifier tag")
    # Armed at 4: the Norman Conquest modifier file carries four real tags.
    check("modifier tags exist in engine docs", count, probs, min_count=4)

    probs, count = [], 0
    for p in glob.glob(MOD + "/in_game/common/on_action/*.txt"):
        oa = strip_comments(read(_np(p)))
        hooks = set(re.findall(r"^([a-z_0-9]+) = " + BS + "{", oa, re.M))
        # A custom on_action is legal when something else calls it. Two call
        # shapes: a bare name on its own line, and the ONE-LINE list
        # `on_actions = { x y }` — vanilla's own ai_personalities_setup.txt
        # uses the one-line form, and this check missed it until it flagged
        # our first on_action file. One-line blocks are the day's recurring
        # blind spot; scan both shapes.
        own = set(re.findall(r"^[ " + BS + "t]+([a-z_0-9]+)$", oa, re.M))
        for inner in re.findall(r"on_actions[ " + BS + "t]*=[ " + BS + "t]*" + BS + "{([^}]*)" + BS + "}", oa):
            own |= set(inner.split())
        own &= hooks
        for h in sorted(hooks - own):
            count += 1
            if h not in ON_ACTIONS:
                probs.append(f"{h} is not an on_action the engine declares")
    # Back to PENDING: the Norman Conquest on_action was deleted after it
    # did nothing in game — the situation owns its timeline now (see
    # KNOWLEDGE.md). Re-arm when the next on_action file lands.
    check("on_action hooks exist in engine docs", count, probs, min_count=PENDING)

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
