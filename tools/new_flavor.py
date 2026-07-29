#!/usr/bin/env python3
"""DHE flavor-file scaffold generator — the boilerplate half of a flavor
pack, from the shapes proven in vanilla and in Mongol Resurgence's own
in-game-tested DHE layer (docs/EVENT-SYSTEM.md is the design record).

What it does NOT do: triggers, effects, option bodies, design. Those are
main-session work under the citation rule (CLAUDE.md). What it does: the
two-file skeleton (events + loc) with every measured trap pre-answered.

THE EIGHT MEASURED TRAPS (EVENT-SYSTEM.md; each cost someone a round):
1. `.entry` — the sixth loc key nobody would guess: the per-country DHE
   timeline panel reads <id>.entry (country_dhe_lateralview.gui:194);
   missing = the known localization_util.cpp:103 error.
2. `fire_only_once` is GLOBAL, and 3,206/3,232 vanilla DHEs carry it —
   a tag-bound one-shot is the wanted shape; omit it only for a
   deliberately repeating event.
3. Option names are EXPLICIT — 14,427/14,427 vanilla options carry
   `name =`; the .a/.b convention is habit, not derivation.
4. Chained events fire via trigger_event_silently /
   trigger_event_non_silently (both forms attested); there is no plain
   `trigger_event` in EU5.
5. `every_neighbour_country` DOES NOT EXIST (the British-spelling trap);
   the broadcast idiom is every_country + limit (flavor_ENG.txt:313).
6. `?=` on EVERY nullable link (ruler, dynasty, owner, c:TAG) in the
   event-level trigger — the DHE panel re-evaluates listed events'
   triggers CONTINUOUSLY (country_dhe_lateralview.gui:224), so one
   unguarded link floods jomini_script_system.cpp:252.
7. Event ids 1-9999 (engine range); this project bands them:
   1-99 story beats, 100-199 chain continuations, 900-999 hidden
   machinery.
8. THE TRIGGER LAW: FLAVOR events SHOULD carry an event-level trigger
   (95% of vanilla DHEs do — being swallowed when conditions fail is
   the point). RAILROAD beats (scripted deaths, successions,
   coronations) carry NONE — their guards live inside options as
   if/limit. This generator emits FLAVOR shapes.

Usage:
    python tools/new_flavor.py <spec-key> [--out DIR]

The skeleton is INERT: every event's trigger is `always = no` behind an
`# ARM:` marker — a generated pack can land in the repo without a test
debt. The nine harness checks of EVENT-SYSTEM.md 4.6 land in the SAME
commit that arms the first event, not before (nothing to prove them
against until then).

Shapes cloned from:
    vanilla in_game/events/DHE/D008_flavor_BYZ.txt (the canonical stub)
    Mongol Resurgence in_game/events/DHE/MR_dominance_dhe_events.txt
        (illustration_tags weighting; proven in game by MR's test log)
"""
import os
import re
import sys

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = (1066, 9, 15)

# ---------------------------------------------------------------- specs ---
# key: {
#   "tag":    the country TAG the pack belongs to (uppercase),
#   "events": [(id, "short comment", "from", "to", monthly_chance), ...]
#             — dates as "Y.M.D" strings; from/to bound the DHE window
#             and must satisfy from < to and to > start date; ids obey
#             the band rule (trap 7),
# }
SPECS = {
    # "eng": {
    #     "tag": "ENG",
    #     "events": [
    #         (1, "the Ætheling's shadow", "1066.12.25", "1072.1.1", 10),
    #     ],
    # },
    "demo": {   # --out testing only; never generate into the repo
        "tag": "AAA",
        "events": [
            (1, "the first beat", "1066.10.1", "1070.1.1", 10),
            (100, "its continuation", "1066.10.1", "1075.1.1", 5),
        ],
    },
}

EVENT_TPL = """######################################
# {num} — {comment}
######################################

{ns}.{num} = {{
	type = country_event
	title = {ns}.{num}.title
	desc = {ns}.{num}.desc
	historical_info = {ns}.{num}.historical_info
	outcome = neutral
	fire_only_once = yes

	illustration_tags = {{
		10 = regular
		10 = interior
	}}

	dynamic_historical_event = {{
		tag = {tag}
		from = {frm}
		to = {to}
		monthly_chance = {chance}
	}}

	# ARM: replace `always = no` with the real gate (this is a FLAVOR
	# event — it SHOULD have one; trap 8). Every nullable link behind
	# ?= (trap 6). Harness checks of EVENT-SYSTEM.md 4.6 ride in the
	# arming commit.
	trigger = {{
		always = no
	}}

	option = {{
		name = {ns}.{num}.a
		historical_option = yes
	}}

	option = {{
		name = {ns}.{num}.b
	}}
}}
"""

BOM = b"\xef\xbb\xbf"


def _date(s):
    p = s.split(".")
    if len(p) != 3 or not all(x.isdigit() for x in p):
        sys.exit(f"bad date {s!r} — expected Y.M.D")
    return tuple(int(x) for x in p)


def _write(path, text, bom):
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = text.replace("\r\n", "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write((BOM if bom else b"") + data)
    return path


def generate(key, out):
    spec = SPECS.get(key) or sys.exit(f"no spec named {key!r} in SPECS")
    tag, events = spec["tag"], spec["events"]
    if not re.fullmatch(r"[A-Z][A-Z0-9]{2}", tag):
        sys.exit(f"tag {tag!r} is not a 3-char uppercase tag")
    ns = f"f1066_{tag.lower()}"

    seen = set()
    for num, comment, frm, to, chance in events:
        if not 1 <= num <= 9999:
            sys.exit(f"event id {num} outside the engine's 1-9999 range")
        if num in seen:
            sys.exit(f"event id {num} duplicated in the spec")
        seen.add(num)
        if not (_date(frm) < _date(to) and _date(to) > START):
            sys.exit(f"event {num}: window {frm}..{to} must be ordered "
                     "and end after the 1066.9.15 start")
        if not 0 < chance <= 100:
            sys.exit(f"event {num}: monthly_chance {chance} outside 1-100")

    header = (f"namespace = {ns}\n"
              f"# {tag} flavor — SCAFFOLD (tools/new_flavor.py). Every event\n"
              f"# is INERT until its `# ARM:` gate is replaced; the trigger\n"
              f"# law and the eight traps are in the generator header and\n"
              f"# docs/EVENT-SYSTEM.md.\n\n")
    body = header + "\n".join(
        EVENT_TPL.format(ns=ns, num=n, comment=c, tag=tag, frm=f, to=t,
                         chance=ch)
        for n, c, f, t, ch in events)

    written = []
    written.append(_write(
        os.path.join(out, "in_game", "events", "DHE",
                     f"1066_flavor_{tag}.txt"),
        body, bom=True))

    loc = ["﻿l_english:"]
    for n, c, _f, _t, _ch in events:
        loc += [f' {ns}.{n}.title: "TODO — {c}"',
                f' {ns}.{n}.desc: "TODO"',
                f' {ns}.{n}.entry: "TODO — DHE timeline label (trap 1)"',
                f' {ns}.{n}.historical_info: "TODO"',
                f' {ns}.{n}.a: "TODO"',
                f' {ns}.{n}.b: "TODO"']
    written.append(_write(
        os.path.join(out, "main_menu", "localization", "english", "events",
                     "DHE", f"1066_flavor_{tag.lower()}_l_english.yml"),
        "\n".join(loc) + "\n", bom=False))   # BOM is the ﻿ literal

    # ------------------------------------------------------ self-check ---
    for p in written:
        raw = open(p, "rb").read()
        if raw[:3] != BOM:
            sys.exit(f"BOM self-check failed on {p}")
        text = raw.decode("utf-8-sig")
        if text.count("{") != text.count("}"):
            sys.exit(f"brace balance self-check failed on {p}")
        if p.endswith(".yml"):
            for line in text.splitlines()[1:]:
                if line and not re.match(r'^ [A-Za-z0-9_.]+: ".*"$', line):
                    sys.exit(f"loc line shape self-check failed on {p}: "
                             f"{line!r}")
        else:
            if len(re.findall(r"^\t*option = \{", text, re.M)) != \
                    2 * len(events):
                sys.exit(f"option count self-check failed on {p}")
            if text.count("name = ") != 2 * len(events):
                sys.exit(f"explicit option-name self-check failed on {p} "
                         "(trap 3)")

    print(f"flavor scaffold '{key}' ({tag}) written — {len(written)} files:")
    for p in written:
        print("  " + os.path.relpath(p, out))
    print("""
STILL YOURS TO DO (the generator cannot):
  1. replace every `always = no` ARM gate with the real, ?=-guarded
     trigger — script docs first, citation rule applies
  2. write the six loc values per event (ONE physical line each)
  3. option bodies: effects, ai_chance, chains
     (trigger_event_*_silently only — no plain trigger_event)
  4. illustration_tags weights per event's mood, or a real `image =`
  5. the EVENT-SYSTEM.md 4.6 harness checks land IN THE ARMING COMMIT,
     with min_counts set to what the repo then holds
  6. delete any event the design dropped — an unreferenced inert stub
     is clutter, not flavor""")


if __name__ == "__main__":
    argv = sys.argv[1:]
    out = MOD
    if "--out" in argv:
        i = argv.index("--out")
        out = argv[i + 1]
        del argv[i:i + 2]
    if len(argv) != 1:
        sys.exit("usage: python tools/new_flavor.py <spec-key> [--out DIR]")
    if argv[0] == "demo" and os.path.abspath(out) == os.path.abspath(MOD):
        sys.exit("the demo spec only generates outside the repo (--out)")
    generate(argv[0], out)
