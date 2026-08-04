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
# Armed at 7: six generated files (06_pops joined with the pop phase's
# Batch 1) plus the additive 04_zz_1066_dynasties. Raise it again as more
# setup files land — a BOM here is the single most expensive byte in the
# project.
check("no BOM in setup/start", len(setup_txt), probs, min_count=7)

# THE POP OVERRIDE'S INDEPENDENT SET CHECK (guard D1's harness twin,
# 2026-08-03). The 5 MB generated 06_pops.txt cannot be read; the one
# structural property everything else hangs off is that its location-block
# NAME SET equals vanilla's exactly — the Bronze Era conversion shipped
# 2,633 duplicate blocks, 502 phantoms and 3,131 drops in this same file
# and nothing errored. Re-derived here from scratch (a separate parser
# from the build's, on purpose). Blocks sit at COLUMN 0 inside the
# wrapper — a `^\t`-anchored scan returns a confident zero.
_pops_path = os.path.join(MOD, "main_menu", "setup", "start", "06_pops.txt")
probs = []
_pop_names = []
if os.path.isfile(_pops_path):
    _ps = read(_pops_path)
    _ps = re.sub(r"#[^\n]*", "", _ps)
    _pop_names = re.findall(r"^([A-Za-z0-9_]+)[ \t]*=[ \t]*\{", _ps, re.M)
    _pop_names = [n for n in _pop_names if n != "locations"]
    _vs = re.sub(r"#[^\n]*", "",
                 open(os.path.join(VAN, "main_menu", "setup", "start",
                                   "06_pops.txt"), encoding="utf-8-sig").read())
    _van_names = [n for n in re.findall(r"^([A-Za-z0-9_]+)[ \t]*=[ \t]*\{", _vs, re.M)
                  if n != "locations"]
    if len(_pop_names) != len(set(_pop_names)):
        probs.append(f"duplicate location blocks: {len(_pop_names) - len(set(_pop_names))}")
    _diff = set(_pop_names) ^ set(_van_names)
    if _diff:
        probs.append(f"block set diverges from vanilla by {len(_diff)}: "
                     f"{sorted(_diff)[:5]}")
check("06_pops block-name set equals vanilla", len(_pop_names), probs,
      min_count=28570)

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
check("loc lines are well formed", count, probs, min_count=375)  # raised with Tibet (2026-08-02): 375 rows live

keys, dupes = set(), []
for p in yml_files:
    for m in re.finditer(r"^ ([A-Za-z0-9_.]+):", read(p), re.M):
        if m.group(1) in keys: dupes.append(m.group(1))
        keys.add(m.group(1))
check("no duplicate loc keys", len(keys), sorted(set(dupes)), min_count=375)  # raised with Tibet (2026-08-02)

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
# Armed at 290: 145 named rulers + 145 terms after Germany II.
# Raise together with HISTORICAL_RULERS as Phase 2 regions land.
check("named rulers carry an open, past-dated ruler_term", count, probs, min_count=358)  # 179 thrones (Tibet, 2026-08-02)

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
# No character seated on two tags — except the DELIBERATE pluralists.
# A ruler on several thrones is vanilla-attested: boh_john_luxembourg
# rules BOH and LUX, hai_guillaume_de_hainault HAI and HOL,
# brb_jan_iii_van_brabant BRB and LIM — one character, one `ruler =`
# line and one ruler_term per tag (docs/KNOWLEDGE.md:901). Germany II
# seats Godfrey III the Bearded on BLL and SPL that way. The allowlist
# is EXPLICIT so an accidental second seat — the copy-paste that
# silently hands one man two countries — still fails, and the stale
# check below kills the entry if the second seat ever goes away.
_PLURALISTS = {"bll_godfrey_iii_bearded"}
_seated = [r[0] for r in _bs.HISTORICAL_RULERS.values()]
count += len(_seated)
for _c in set(_seated):
    if _seated.count(_c) > 1 and _c not in _PLURALISTS:
        probs.append(f"{_c} is seated on more than one tag")
for _c in sorted(_PLURALISTS):
    if _seated.count(_c) < 2:
        probs.append(f"_PLURALISTS lists {_c}, seated on {_seated.count(_c)} "
                     "tag(s) — stale exemption, remove it")
# Armed at 540 after Italy North: 89 authored characters + 48 dynasties
# + 153 seats
# (512 measured after Germany II).
check("authored identifiers resolve (dynasty, name, birthplace, loc)", count, probs, min_count=646)  # +Dongzhan/tsongkha (Tibet, 2026-08-02)

# Where vanilla ships its OWN ruler_term for the same character in the same
# country block, our accession date must MATCH it — vanilla is ground truth
# for ~30 of the 53 rows, and this turns "trust the research agent" into a
# machine comparison. Rows where vanilla has no such term (authored
# characters, cross-tag seats) are simply not compared.
_van10 = read(_np(VAN + "/main_menu/setup/start/10_countries.txt"))
_vblocks = list(re.finditer(r"^\t([A-Z0-9]{2,6}) = " + BS + "{", _van10, re.M))
probs, count = [], 0
_compared = 0
# The check's FIRST exemption (SEA slice, 2026-08-02): vanilla's own
# LAV block seats adh_narai with a term from 1082.1.1 — the late Lavo
# king-list read as 1082-1087. The list's dates are reconstructions
# and the other reading is c. 1052-1082 [D]; a 1082 accession cannot
# rule at a 1066 start at all, so the seat and the [D] date stand and
# the mismatch is EXPECTED, not an error. Any new mismatch still fails.
_ACC_EXEMPT = {("LAV", "adh_narai")}
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
            if _acc not in _terms and (_tag, _char) not in _ACC_EXEMPT:
                probs.append(f"{_tag}/{_char}: our accession {_acc} vs vanilla's own term(s) {_terms}")
        break
count = len(_bs.HISTORICAL_RULERS)
print(f"       accessions cross-checked against vanilla's own terms: {_compared} of {count}")
# Armed at 145 rows after Germany II; compared coverage is 35 — vanilla
# ships zero Muslim characters born before 1054 and zero Germans alive
# in 1066 outside Heinrich IV's line, so none of those rulers is
# comparable.
check("accessions match vanilla's own terms where vanilla has them", count, probs, min_count=179)  # Tibet, 2026-08-02

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
# Armed at 116 authored characters after Italy North (+7: Beatrice,
# Matilda, Ulric, the three prelates, Adelaide).
check("authored character keys collide with nothing", count, probs, min_count=139)  # Tibet, 2026-08-02

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

# The situation ALERT rides a THREE-part hint contract (craft sweep
# 2026-08-04, SITUATION-CRAFT law #9, all three legs vanilla-verified):
# hint_tag in the def + a scriptable_hints object + the <tag>/<tag>_hint_text
# loc pair. Any missing leg is SILENT — vanilla ships it 22/22, and four
# reference/workshop mods shipped dangling hint_tags. Objects and loc may
# resolve from vanilla too (a REPLACE'd vanilla situation keeps its hint).
# File-scoped by our one-situation-per-file convention.
_hint_objs = set()
for _p in glob.glob(MOD + "/in_game/common/scriptable_hints/*.txt") + \
          glob.glob(VAN + "/in_game/common/scriptable_hints/*.txt"):
    _hint_objs |= set(re.findall(r"^([a-z_0-9]+)[ \t]*=[ \t]*" + BS + "{",
                                 strip_comments(read(_np(_p))), re.M))
_van_hint_loc = set(re.findall(r"^[ \t]+([A-Za-z0-9_.]+):",
                               read(_np(VAN + "/main_menu/localization/english/hints_l_english.yml")), re.M))
probs, count = [], 0
for _p in glob.glob(MOD + "/in_game/common/situations/*.txt"):
    _s = strip_comments(read(_np(_p)))
    _sitkeys = re.findall(r"^([a-z_0-9]+)[ \t]*=[ \t]*" + BS + "{", _s, re.M)
    _tags = re.findall(r"^\thint_tag[ \t]*=[ \t]*([a-z_0-9]+)", _s, re.M)
    for _k in _sitkeys:
        count += 1
        if not _tags:
            probs.append(f"{os.path.basename(_p)}: situation '{_k}' has no hint_tag — no alert, silently")
    for _t in _tags:
        count += 1
        if _t not in _hint_objs:
            probs.append(f"{os.path.basename(_p)}: hint_tag {_t} resolves to no scriptable_hints object")
        for _want in (_t, _t + "_hint_text"):
            count += 1
            if _want not in keys and _want not in _van_hint_loc:
                probs.append(f"hint loc key {_want} is not defined")
# Armed at 4: one situation + its tag + the two loc keys.
check("situation hint contract complete (tag, object, loc)", count, probs, min_count=4)

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

# ---- new-tag tributary overlords pass the subject-type gate ----------------
# Measured 2026-07-29: tributary.txt's visible gate (:20-24 — overlord
# steppe_horde, subject tribe/horde, or overlord carries
# modifier:allow_tributary_subject) IS enforced at game start
# (government.cpp:3702 cites those exact lines) and a failing dependency is
# silently DOWNGRADED TO VASSAL — all nine Seljuk clients were, in game.
# Vanilla's own passing overlords are hordes, tribe-subjecting, or modifier
# carriers (African advances, the Middle Kingdom IO, reforms); ours must
# carry the modifier through a reform assigned in setup. Scoped to overlords
# WE invented (the zz_1066_new_countries.txt registry): vanilla's own
# gate-failing lines are Paradox-side data, reported by the engine, not
# validated here.
probs = []
_newreg = next((s for p, s in code.items()
                if p.endswith("in_game/setup/countries/zz_1066_new_countries.txt")), "")
_newtags = set(re.findall(r"^([A-Z][A-Z0-9]{2,4}) = \{",
                          strip_comments(_newreg), re.M))
_diplo = next((s for p, s in code.items()
               if p.endswith("main_menu/setup/start/12_diplomacy.txt")), "")
_countries10 = next((s for p, s in code.items()
                     if p.endswith("main_menu/setup/start/10_countries.txt")), "")
_reform_src = strip_comments("\n".join(
    s for p, s in code.items() if "/in_game/common/government_reforms/" in p))
_loc_all = "\n".join(open(p, encoding="utf-8-sig").read() for p in yml_files)
# Overlords to gate-check: every new-registry tag PLUS the vanilla
# tags we hand mod-added tributaries to (FRA — the Capetian homage
# ring; LEI/TYR/TRY/MCM — the Irish ties; PAP — the Melfi
# investiture; PLB — the Srivijayan mandala, SEA slice; a vanilla
# overlord is invisible to the registry scan but its tributaries fail
# the same visible gate without a passing branch).
_MOD_TRIB_OVERLORDS = {"FRA", "LEI", "TYR", "TRY", "MCM", "PAP", "KIE",
                       "LIA", "PLB"}
_gate_deps = [(m.group(1), m.group(2)) for m in re.finditer(
    r"dependency = \{ first = (\w+) second = (\w+) subject_type = tributary \}",
    strip_comments(_diplo))
    if m.group(1) in _newtags or m.group(1) in _MOD_TRIB_OVERLORDS]
# Reform definitions live in BOTH trees: ours, and vanilla's (the SEA
# mandala rides vanilla's own mandala_system, country_specific.txt:3894
# — the first ring gated by a reform this project did not write; until
# then this lookup read mod files only and the gap was invisible).
_van_reform_src = strip_comments("\n".join(
    read(_p) for _p in glob.glob(_np(
        VAN + "/in_game/common/government_reforms/*.txt"))))
# A block's reforms may arrive through its TEMPLATE include chain, not
# inline (PLB's mandala_system sits in indonesia_monarchy's own
# reforms block) — and templates NEST includes, so a one-level reader
# lies (the welsh_releasable lesson, KNOWLEDGE.md). Walked with a
# cache, cycles guarded by the visited set.
_TPL_REFORM_CACHE = {}
def _tpl_reforms(_inc, _seen=None):
    if _inc in _TPL_REFORM_CACHE:
        return _TPL_REFORM_CACHE[_inc]
    _seen = _seen or set()
    if _inc in _seen:
        return set()
    _seen.add(_inc)
    _out = set()
    _tp = _np(VAN + "/main_menu/setup/templates/" + _inc + ".txt")
    if os.path.isfile(_tp):
        _tb = strip_comments(read(_tp))
        for _rm in re.finditer(r"reforms = \{([^}]*)\}", _tb):
            _out |= set(_rm.group(1).split())
        for _im in re.finditer(
                r'^[ \t]*include[ \t]*=[ \t]*"?([A-Za-z0-9_]+)"?', _tb, re.M):
            _out |= _tpl_reforms(_im.group(1), _seen)
    _TPL_REFORM_CACHE[_inc] = _out
    return _out
for _ov, _sub in _gate_deps:
    # The visible gate (tributary.txt:19-24) passes on EITHER branch:
    # the SUBJECT is a tribe/steppe_horde (the Gaelic ties — their
    # gaelic_tribe* includes carry type = tribe) or the overlord holds
    # modifier:allow_tributary_subject from a setup reform (inline or
    # template-carried).
    _sblk = re.search(rf"^\t{_sub} = \{{.*?^\t\}}", _countries10,
                      re.M | re.S)
    if _sblk and re.search(r'include = "gaelic_tribe', _sblk.group(0)):
        continue
    _blk = re.search(rf"^\t{_ov} = \{{.*?^\t\}}", _countries10, re.M | re.S)
    _keys = set(" ".join(re.findall(r"reforms = \{([^}]*)\}",
                                    _blk.group(0) if _blk else "")).split())
    for _im in re.finditer(r'include = "([A-Za-z0-9_]+)"',
                           _blk.group(0) if _blk else ""):
        _keys |= _tpl_reforms(_im.group(1))
    _passes = False
    for _k in sorted(_keys):
        for _rsrc in (_reform_src, _van_reform_src):
            _def = re.search(rf"^{_k} = \{{.*?^\}}", _rsrc, re.M | re.S)
            if _def and re.search(r"allow_tributary_subject\s*=\s*yes",
                                  _def.group(0)):
                _passes = True
    if not _passes:
        probs.append(f"{_ov} -> {_sub}: neither branch of the tributary "
                     "visible gate passes — no overlord reform granting "
                     "allow_tributary_subject and the subject is not a "
                     "tribe; the engine will downgrade it to a vassal")
# Every reform WE define must resolve to loc, name AND desc — a missing
# key renders raw in the government screen, silently.
for _k in re.findall(r"^([a-z0-9_]+) = \{", _reform_src, re.M):
    if not re.search(rf"^\s*{_k}:", _loc_all, re.M):
        probs.append(f"reform {_k} has no loc name entry")
    if not re.search(rf"^\s*{_k}_desc:", _loc_all, re.M):
        probs.append(f"reform {_k} has no loc desc entry")
# Nine Seljuk + two Fatimid + six Capetian + six Irish + two Melfi
# (=25), + 46 Jurchen + KIE->NOV + ETH-ring residue (73 measured
# 2026-08-02), + five Srivijayan (SEA) = 78, + LIA->KOR (China
# residue) = 79; raise if a future slice adds more.
check("new-tag tributary overlords pass the subject-type gate",
      len(_gate_deps), probs, min_count=79)

# Landless tags are not IO members — Paradox's own rule: vanilla's
# high_kingship list pointedly omits landless MTH and PLE. A member a
# slice emptied would sit in its IO as a ghost (British slice 2026-
# 07-29, whose member surgery — CLA/THO/CVN out, MTH/DUB/ULD in —
# this check guards).
probs = []
_io15 = next((s for p, s in code.items()
              if p.endswith("main_menu/setup/start/15_international_organizations.txt")), "")
_own_re = re.compile(
    r"(?:own_control_core|own_control_integrated|own_control_conquered"
    r"|own_control_colony|own_core|own_conquered|own_integrated"
    r"|own_colony|control_core|control)[ \t]*=[ \t]*\{([^}]*)\}")
_c10_clean = strip_comments(_countries10)
_blk_starts = list(re.finditer(r"^\t([A-Z0-9]{2,6}) = \{", _c10_clean, re.M))
_blk_bodies = {}
for _i, _b in enumerate(_blk_starts):
    _e = (_blk_starts[_i + 1].start() if _i + 1 < len(_blk_starts)
          else len(_c10_clean))
    _blk_bodies[_b.group(1)] = _c10_clean[_b.start():_e]
_members_checked = 0
for _mm in re.finditer(r"members[ \t]*=[ \t]*\{([^}]*)\}",
                       strip_comments(_io15)):
    for _t in _mm.group(1).split():
        _members_checked += 1
        _body = _blk_bodies.get(_t)
        if _body is None:
            probs.append(f"IO member {_t} has no country block")
        elif (not any(g.split() for g in _own_re.findall(_body))
              and not re.search(r"^\t\ttype = (building|army|pop)", _body,
                                re.M)):
            # building/army/pop-based countries legitimately hold no
            # land: this check's first runs flagged TGS/YSM (vanilla
            # `type = building` Japanese clans) and DDI (`type = pop`,
            # the Thai sect) — validate ours strictly, report what
            # vanilla shipped. It ALSO found a real ghost on the same
            # first run: landless CIL sitting in the autocephalous
            # patriarchate — now stripped by build_ios.
            probs.append(f"IO member {_t} holds no land — landless tags "
                         "are not IO members (vanilla's own rule)")
check("IO members hold land", _members_checked, probs, min_count=850)  # was 27 vs 854 scanned — the harness's weakest floor, raised with the China residue (2026-08-02), proven by breaking

# ---- no IO instance EMPTIED by the build -----------------------------------
# Vanilla legitimately ships empty members lists (11 of its 53
# instances — runtime-populated), so "empty" alone is not an error.
# The failure class is an instance OUR landless sweep drains: the SEA
# slice retired all four Burmese Buddhism members at once and only the
# PGN member-add kept the sect alive — and the break-probe of
# 2026-08-02 showed NO existing check would have noticed (harness
# green with the list hand-emptied; only a silent 855->854). So the
# empty-list COUNT is pinned: 9 in the current build. A slice that
# empties another instance moves it to 10 and fails here — the
# implementer either adds a member (the Shaiva/PGN shape) or
# consciously moves this constant. Proven by breaking (the same
# hand-emptied list -> 10).
_io_blocks = list(re.finditer(r"^\tadd_international_organization = \{",
                              strip_comments(_io15), re.M))
_io_clean = strip_comments(_io15)
_n_empty_io = 0
probs = []
for _b in _io_blocks:
    _nb = _io_clean.find("\n\tadd_international_organization", _b.end())
    _body = _io_clean[_b.start():_nb if _nb != -1 else len(_io_clean)]
    _mm = re.search(r"members[ \t]*=[ \t]*\{([^}]*)\}", _body)
    if _mm and not _mm.group(1).split():
        _n_empty_io += 1
if _n_empty_io != 9:
    probs.append(f"{_n_empty_io} instances carry an empty members list "
                 "(expected exactly 9, vanilla's own runtime-populated "
                 "set) — a sweep has drained an IO, add a member or "
                 "move the constant deliberately")
check("no IO instance emptied by the build (9 vanilla empties pinned)",
      len(_io_blocks), probs, min_count=36)

# ---- exactly one ruler key per country block -------------------------------
# Vanilla ships 23 one-line `government = { ruler = X }` blocks; every
# line-anchored scan in the build was blind to them, and AOS shipped a
# 1291-born ruler sitting AFTER an injected `ruler = random` in the same
# line — three independent scans blessed it (Italy North review,
# 2026-07-29). More than one ruler key can silently outrank a seated
# Phase 2 ruler; zero means an engine-generated regent. Unanchored, on
# comment-stripped text (NTC ships `#ruler = jap_koumyou_tenno`).
probs = []
_rblocks = 0
for _i, _b in enumerate(_blk_starts):
    _e = (_blk_starts[_i + 1].start() if _i + 1 < len(_blk_starts)
          else len(_c10_clean))
    _body = _c10_clean[_b.start():_e]
    _n = len(re.findall(r"(?<![A-Za-z0-9_])ruler[ \t]*=[ \t]*[A-Za-z0-9_]",
                        _body))
    _rblocks += 1
    if _n != 1:
        probs.append(f"{_b.group(1)}: {_n} ruler keys (exactly one required)")
check("exactly one ruler key per country block", _rblocks, probs,
      min_count=2411)  # + 3 Tibet (2026-08-02)

# ---- coat of arms references resolve ---------------------------------------
# The CoA database is additive and key-merged: a country with no
# flag_definition list uses its TAG as the COA_KEY directly
# (flag_definitions/00_flag_definitions.txt:1, confirmed by the debug
# panel's Flag row in game), and when two files define one key the
# last-loaded file wins. A missing or broken entry errors NOTHING — the
# template_lists generator silently synthesizes a religion-gated flag —
# so a typo'd texture, an undefined colour or a mis-keyed tag all render
# as a plausible generated flag with no log line. Textbook silent
# failure; this check is the only defence (CoA research pass 2026-07-29,
# measured: ABS rendered generator-white and FAT generator-black — each
# caliphate wearing the OTHER's historical colour).
probs = []
_coa_count = 0
_coa_srcs = {p: s for p, s in code.items()
             if "/main_menu/common/coat_of_arms/coat_of_arms/" in p}
_gfx_dirs = [os.path.join(r, "main_menu", "gfx", "coat_of_arms", d)
             for r in (MOD, VAN)
             for d in ("colored_emblems", "textured_emblems")]
_pat_dirs = [os.path.join(r, "main_menu", "gfx", "coat_of_arms", "patterns")
             for r in (MOD, VAN)]
_named_src = "\n".join(
    [s for p, s in code.items() if "/main_menu/common/named_colors/" in p]
    + [read(p) for p in glob.glob(os.path.join(
        VAN, "main_menu", "common", "named_colors", "*.txt"))])
_color_defs = set(re.findall(r"^\s*([A-Za-z0-9_]+)\s*=\s*(?:rgb|hsv)",
                             strip_comments(_named_src), re.M))
_our_coa_keys = set()
for _p, _s in sorted(_coa_srcs.items()):
    _rel = os.path.relpath(_p, MOD)
    _clean = strip_comments(_s)
    _our_coa_keys |= set(re.findall(r"^([A-Za-z0-9_]+)\s*=\s*\{", _clean, re.M))
    for _t in re.findall(r'texture\s*=\s*"([^"]+)"', _clean):
        _coa_count += 1
        if not any(os.path.isfile(os.path.join(d, os.path.basename(_t)))
                   for d in _gfx_dirs):
            probs.append(f"{_rel}: emblem texture {_t} is on no disk "
                         "(mod or vanilla) — renders as a generated flag, silently")
    for _t in re.findall(r'pattern\s*=\s*"([^"]+)"', _clean):
        _coa_count += 1
        if not any(os.path.isfile(os.path.join(d, os.path.basename(_t)))
                   for d in _pat_dirs):
            probs.append(f"{_rel}: pattern {_t} is on no disk (mod or vanilla)")
    for _t in re.findall(r'color\d\s*=\s*"([A-Za-z0-9_]+)"', _clean):
        _coa_count += 1
        if _t not in _color_defs:
            probs.append(f"{_rel}: named colour {_t} is defined in no "
                         "named_colors file (mod or vanilla)")
# A key vanilla also defines is an OVERRIDE (last-loaded wins) — legal,
# but only ever deliberate; computed here because the registry loop
# below also consults the vanilla key set.
_van_coa_keys = set()
for _p in glob.glob(os.path.join(VAN, "main_menu", "common",
                                 "coat_of_arms", "coat_of_arms", "*.txt")):
    _van_coa_keys |= set(re.findall(r"^([A-Za-z0-9_]+)\s*=\s*\{",
                                    strip_comments(read(_p)), re.M))
# Every invented tag either carries arms, or has VANILLA arms already
# (the formable-reuse class: SAX/SWA ship scripted CoAs with no registry
# block — reviving the tag inherits the flag for free), or sits
# DELIBERATELY on the generator list — so a future slice's new tag fails
# loudly instead of quietly shipping a flag nobody chose. The membership
# mirrors the CoA package's tiers (docs/COA.md): tier 3 deferred, tier 4
# permanent.
_GENERATOR_OK = {
    # 13 taifas — taifa polities had no heraldry; the generator's
    # religion-gated Islamic designs are no less historical than
    # anything we would invent (tier 4, permanent)
    "SEV", "BDJ", "TOL", "CRD", "GRZ", "ALM", "MRU", "DYA", "ZGZ",
    "LRD", "ABR", "ALP", "QRM",
    # 6 Catalan counties — deferred (tier 3): culture:catalan already
    # feeds their generator pool partial senyera templates; eyeball in
    # game before investing
    "URG", "BSL", "CDY", "EPU", "RSL", "PLJ",
    # 7 Seljuk clients + 2 Sicilian emirates — no-heraldry ground (tier 4)
    "GHZ", "UQY", "MRD", "HLB", "SIS", "KKY", "SHD", "PLM", "AGR",
    # ULD + 4 south-Italian states — deferred (tier 3)
    "ULD", "CUP", "SLR", "NEA", "GAE",
    # ISR — deferred (tier 3): no Istrian march heraldry is attested for
    # 1066; eyeball the generated flag in game before investing. TUS is
    # NOT here: it has VANILLA arms (the SAX/SWA formable-reuse class —
    # TUS_f ships flag = TUS) and passes through the _van_coa_keys branch.
    "ISR",
    # Central Asia — deferred (tier 3): no Karakhanid or Volga-Bulgar
    # heraldry is attested; eyeball the generated flags before investing.
    "QRK", "QRA", "BLH",
    # Arabia — tier 4, permanent: the Qarmatian council and the
    # Ukhaydirid emirate had no heraldry.
    "QMT", "UKH",
    # Rus Tier 2 — tier 4, permanent: the Cumans had none.
    "CUM",
    # Northern Dynasties — tier 4, permanent: neither dynasty used
    # European-style heraldry.
    "LIA", "XIA",
    # India Tier 1 — tier 3, DEFERRED not permanent: Indian dynastic
    # emblems ARE attested (the Chola tiger, the Chalukya boar, the
    # Paramara eagle) — eyeball the generated flags before investing.
    "COZ", "CLK", "PAA", "PMR", "CHU",
    # Baltic — tier 4, permanent: the pagan Baltic peoples had no
    # heraldry of any kind; the Order/bishopric arms vanilla ships
    # belong to the tags that slice retires, not to these. SXM is NOT
    # here: it has vanilla arms (the _van_coa_keys branch).
    "PRS", "SUD", "KUO", "ZEM", "LTG", "ESO", "AUK",
    # Africa — tier 4, permanent: neither Djenne-Jeno nor the Sanhaja
    # confederations had heraldry; the generator's religion-gated
    # Islamic designs are the taifa rationale exactly. Every OTHER
    # Africa-slice tag is vanilla with vanilla arms.
    "DJN", "SNH",
    # Southeast Asia — tier 4, permanent: Pagan, Haripunjaya, Kediri
    # and Janggala sealed with inscriptions and royal seals, not
    # shields — no heraldry existed to reproduce. Every other
    # SEA-slice tag is vanilla with vanilla arms.
    "PGN", "HPJ", "KDR", "JGL",
    # Tibet — tier 4, permanent: Tibetan polities used seals, banners
    # and monastic emblems, not shields. TIB itself keeps vanilla's
    # arms as a landless shell (_van_coa_keys branch).
    "DBU", "GTS", "TKA",
}
for _t in sorted(_newtags):
    _coa_count += 1
    if _t in _our_coa_keys and _t in _GENERATOR_OK:
        probs.append(f"{_t} both carries arms and sits in _GENERATOR_OK — "
                     "drop it from the list")
    elif (_t not in _our_coa_keys and _t not in _GENERATOR_OK
          and _t not in _van_coa_keys):
        probs.append(f"new tag {_t} has neither a CoA block, nor vanilla "
                     "arms, nor a _GENERATOR_OK entry — choose deliberately")
for _t in sorted(_GENERATOR_OK - _newtags):
    probs.append(f"_GENERATOR_OK lists {_t}, which is not in the "
                 "new-country registry — stale entry")
# SIC_ancient is the one intended override member — at 1066 Sicily's
# default flag is the Hauteville bend, not the Hohenstaufen eagle
# (1194+); the key-level override leaves vanilla's SIC flag_definition
# list and all its later variants untouched.
_INTENTIONAL_COA_OVERRIDES = {"SIC_ancient"}
for _k in sorted(_our_coa_keys):
    _coa_count += 1
    if _k in _van_coa_keys and _k not in _INTENTIONAL_COA_OVERRIDES:
        probs.append(f"CoA key {_k} silently overwrites a vanilla flag — "
                     "add to _INTENTIONAL_COA_OVERRIDES only if intended")
for _k in sorted(_INTENTIONAL_COA_OVERRIDES - _our_coa_keys):
    probs.append(f"_INTENTIONAL_COA_OVERRIDES lists {_k} but our CoA "
                 "files define no such key")
# 9 blocks (10 textures + 9 patterns + 23 colours + 9 keys) + 45
# registry tags = 96 after Italy North (TUS + ISR); raise as arms land.
# 116 after the Baltic's 7 registry tags (2026-08-01); 118 after
# Africa's DJN + SNH (2026-08-02).
check("coat of arms references resolve", _coa_count, probs, min_count=125)  # + 3 Tibet (2026-08-02)

# ---- audit 2026-07-31: the four class-closing checks -----------------------
# From the verified external audit (docs/AUDIT-2026-07-31.md, Part 5 items
# 1-4). Each closes the CLASS one of the confirmed D-findings landed in.

# (1) Identity <-> start-block bijection. A registered tag without a start
# block NEVER EXISTS in game — it cannot catch up later (MR, live
# 2026-07-31); vanilla's only blockless registry entries are the three
# engine placeholders. The reverse is the PYS lesson: a start block whose
# tag is unregistered is rejected whole and its land goes ownerless. The
# effective registry is vanilla's setup/countries overlaid by same-name mod
# files (iberia/italy), plus mod-only files (zz_1066_new_countries).
probs = []
_ID_TAG = re.compile(r"^([A-Z][A-Z0-9_]{1,7})\s*=\s*\{", re.M)
_id_files = {os.path.basename(_p): read(_p) for _p in
             glob.glob(os.path.join(VAN, "in_game", "setup", "countries", "*.txt"))}
for _p, _s in code.items():
    if "/in_game/setup/countries/" in _p:
        _id_files[os.path.basename(_p)] = _s
_id_tags = set()
for _s in _id_files.values():
    _id_tags |= set(_ID_TAG.findall(strip_comments(_s)))
_start_tags = set(re.findall(r"^\t([A-Z][A-Z0-9_]{1,7}) = \{",
                             strip_comments(_countries10), re.M))
_PLACEHOLDERS = {"DUMMY", "MER", "PIR"}  # _default.txt engine placeholders
for _t in sorted(_id_tags - _start_tags - _PLACEHOLDERS):
    probs.append(f"registry tag {_t} has NO 10_countries block — it will "
                 "never exist in game, not even as a landless shell")
for _t in sorted(_start_tags - _id_tags):
    probs.append(f"10_countries block {_t} has NO registry identity block — "
                 "the engine rejects the whole block (PYS lesson)")
check("identity <-> start-block bijection (DUMMY/MER/PIR excepted)",
      len(_id_tags), probs, min_count=2414)  # +3 Tibet (2026-08-02)

# (2) Named-colour keys must not shadow vanilla's. map_NRM was redefined
# and silently repainted vanilla's Normandy AND the norman CULTURE (D3):
# the authoring check had compared rgb VALUES, and a word-boundary tag scan
# cannot see a map_TAG key at all (underscore is a word character). Compare
# KEY NAMES, mod against vanilla.
probs = []
_CKEY = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*(?:rgb|hsv|hex|\{)", re.M)
_van_ckeys = set()
for _p in glob.glob(os.path.join(VAN, "main_menu", "common",
                                 "named_colors", "*.txt")):
    _van_ckeys |= set(_CKEY.findall(strip_comments(read(_p))))
_mod_ckeys = set()
for _p, _s in code.items():
    if "/main_menu/common/named_colors/" in _p:
        _mod_ckeys |= set(_CKEY.findall(strip_comments(_s)))
_van_ckeys.discard("colors"); _mod_ckeys.discard("colors")
_INTENTIONAL_COLOR_OVERRIDES = set()  # none today — only ever deliberate
for _k in sorted((_mod_ckeys & _van_ckeys) - _INTENTIONAL_COLOR_OVERRIDES):
    probs.append(f"named colour {_k} redefines a vanilla key (zz_ loads "
                 "last, vanilla consumers move with it) — rename it "
                 f"{_k}_1066 or add to _INTENTIONAL_COLOR_OVERRIDES")
for _k in sorted(_INTENTIONAL_COLOR_OVERRIDES - _mod_ckeys):
    probs.append(f"_INTENTIONAL_COLOR_OVERRIDES lists {_k}, which our "
                 "named_colors files no longer define — stale entry")
check("mod named colours shadow no vanilla key", len(_mod_ckeys), probs,
      min_count=45)

# (3) .gui references resolve, and the hint-pair rule. using =
# fontsize_medium resolved to NOTHING anywhere and failed silently (D4).
# Blanking visible_hint flips the template default visible = no, so the
# hint button APPEARS; blanking onaction_hint kills its action — together
# a visible dead button (D5; vanilla: 19/19 panels that blank visible_hint
# supply a real onaction_hint, 8 more cards override neither).
probs = []
_gui_defs, _gui_blocks = set(), set()
for _root in (VAN,):
    for _p in glob.glob(os.path.join(_root, "*", "gui", "**", "*.gui"),
                        recursive=True):
        _s = open(_p, encoding="utf-8-sig", errors="replace").read()
        _gui_defs |= set(re.findall(r"^\s*template\s+([A-Za-z0-9_]+)", _s, re.M))
        _gui_defs |= set(re.findall(r"^\s*type\s+([A-Za-z0-9_]+)\s*=", _s, re.M))
        _gui_blocks |= set(re.findall(r'\bblock\s+"([^"]+)"', _s))
for _p in gui_files:
    _s = open(_p, encoding="utf-8-sig").read()
    _gui_defs |= set(re.findall(r"^\s*template\s+([A-Za-z0-9_]+)", _s, re.M))
    _gui_defs |= set(re.findall(r"^\s*type\s+([A-Za-z0-9_]+)\s*=", _s, re.M))
    _gui_blocks |= set(re.findall(r'\bblock\s+"([^"]+)"', _s))
_gui_refs = 0
for _p in gui_files:
    _rel = os.path.relpath(_p, MOD)
    _clean = re.sub(r"#.*", "", open(_p, encoding="utf-8-sig").read())
    for _u in re.findall(r"using\s*=\s*([A-Za-z0-9_]+)", _clean):
        _gui_refs += 1
        if _u not in _gui_defs:
            probs.append(f"{_rel}: using = {_u} is defined nowhere (mod or "
                         "vanilla gui trees) — widget silently keeps defaults")
    for _b in re.findall(r'blockoverride\s+"([^"]+)"', _clean):
        _gui_refs += 1
        if _b not in _gui_blocks:
            probs.append(f'{_rel}: blockoverride "{_b}" matches no declared '
                         "block name anywhere — silently ignored")
    _gui_refs += len(re.findall(r'blockoverride\s+"visible_hint"', _clean))
    if (re.search(r'blockoverride\s+"visible_hint"\s*\{\s*\}', _clean)
            and not re.search(
                r'blockoverride\s+"onaction_hint"\s*\{[^{}]*\S[^{}]*\}',
                _clean)):
        probs.append(f"{_rel}: blanks visible_hint (default visible = no — "
                     "the button APPEARS) without a non-empty onaction_hint: "
                     "a visible dead button; drop the override instead (D5)")
check(".gui using/blockoverride references resolve", _gui_refs, probs,
      min_count=13)

# (4) Every LANDED country reaches a parliament_type — inline or through
# its include chain (templates may nest includes; 8 vanilla templates
# inherit it that way). ABS/FAT were the only two blocks in mod OR vanilla
# without one (D2): initialize_from_bookmark.cpp:1719, silent defaults.
probs = []
_tpl_paths = {}
for _root in (MOD, VAN):  # mod first: a mod template would override
    for _f in glob.glob(os.path.join(_root, "main_menu", "setup",
                                     "templates", "**", "*.txt"),
                        recursive=True):
        _tpl_paths.setdefault(os.path.splitext(os.path.basename(_f))[0], _f)
_tpl_cache = {}
def _tpl_has_parl(name, _seen=None):
    _seen = _seen if _seen is not None else set()
    if name in _seen or name not in _tpl_paths:
        return False
    _seen.add(name)
    if name not in _tpl_cache:
        _s = strip_comments(read(_tpl_paths[name]))
        _tpl_cache[name] = ("parliament_type" in _s or any(
            _tpl_has_parl(_n, _seen)
            for _n in re.findall(r'include\s*=\s*"([^"]+)"', _s)))
    return _tpl_cache[name]
_landed = 0
for _m in re.finditer(r"^\t([A-Z][A-Z0-9_]{1,7}) = \{(.*?)^\t\}",
                      strip_comments(_countries10), re.M | re.S):
    _tag, _body = _m.group(1), _m.group(2)
    # landed = any own* ownership list with content (our_cores_* is claims)
    if not re.search(r"^\t\town\w*\s*=\s*\{[^}]*\w", _body, re.M):
        continue
    _landed += 1
    if "parliament_type" in _body:
        continue
    if any(_tpl_has_parl(_n)
           for _n in re.findall(r'include\s*=\s*"([^"]+)"', _body)):
        continue
    probs.append(f"{_tag}: landed with no parliament_type inline or via "
                 "its include chain — the :1719 class (D2), silent default")
# 1464 at birth; 1461 after Central Asia (6 landless, 3 new landed);
# 1420 after Rus Tier 1 (42 landless, ORE fold included); 1416 after
# Arabia (6 landless incl. the KLB catch, 2 new landed); 1407 after
# Rus Tier 2 (10 landless, CUM landed); 1398 after China-East (9
# landless); 1399 after Northern Dynasties (+2 new, -1 SYG); 1385
# after India Tier 1 (19 landless, 5 new landed) — each drop tripped
# the vacuous-scan guard first and was moved deliberately; 1381 after
# the Baltic (12 landless — the crusader state and LIT — against 7 new
# tribes + SXM revived, all eight reaching assembly via eurasian_tribe).
# 1376 after Africa (10 landless — the Mali/Walashma/Mahdali webs and
# the four side-effect retirees — against DJN + SNH new and BTI, SOA,
# ADA revived, all five reaching a parliament through their templates).
check("landed countries reach a parliament_type", _landed, probs,
      min_count=1360)  # -HQG -YAN -QUN (China residue), observed (2026-08-02)

print()
if fails:
    print(f"RESULT: {len(fails)} check(s) with findings: {', '.join(fails)}")
    sys.exit(1)
if skipped:
    print(f"RESULT: no findings, but {len(skipped)} check(s) had nothing to scan")
    sys.exit(0)
print("RESULT: all checks passed")
