#!/usr/bin/env python3
"""Situation scaffold generator — the boilerplate half of a situation,
from the PROVEN Norman Conquest shapes, with every trap rule baked in.

What it does NOT do: triggers, effects, scopes, design. Those are
main-session work under the citation rule (CLAUDE.md). What it does:
the six-file skeleton whose mechanical mistakes cost the Norman build
its first two in-game rounds — the missing GUI panel, the BOM rules,
the loc conventions, the guards-inside-options event shape, the
event-reachability wiring.

Usage:
    python tools/new_situation.py <spec-key> [--out DIR]

The skeleton is INERT: can_start carries `always = no`. A generated
situation never fires in game until an author flips the gate — so a
scaffold can land in the repo without a test debt.

Shapes cloned from (all confirmed in game):
    in_game/common/situations/norman_conquest.txt
    in_game/events/situations/norman_conquest.txt
    in_game/gui/panels/situation/norman_conquest.gui  (MR's template)
"""
import os
import re
import sys

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- specs ---
# key: {
#   "title":  loc string for the situation name,
#   "desc":   one-line loc string (ONE physical line — the parser drops
#             multi-line loc values),
#   "info":   short loc string for the _info key,
#   "sides":  {TAG: "rgb { r g b }"} — named colors map_<TAG> are emitted
#             into a per-situation additive colors file; reuse an existing
#             map_* name by giving the value None,
#   "events": [(number, "short comment"), ...] — stub events, each wired
#             into on_start so the reachability check holds,
# }
SPECS = {
    # "manzikert": {
    #     "title": "The Road to Manzikert",
    #     "desc": "...",
    #     "info": "...",
    #     "sides": {"BYZ": None, "SEL": None},
    #     "events": [(1, "the intro, to both courts")],
    # },
    "demo": {   # --out testing only; never generate into the repo
        "title": "Scaffold Demo",
        "desc": "Scaffold demo description on one line.",
        "info": "Scaffold demo info.",
        "sides": {"AAA": "rgb { 10 20 30 }", "BBB": None},
        "events": [(1, "the intro"), (10, "the first beat")],
    },
}

SITUATION_TPL = """# {title} — SCAFFOLD. The situation owns its own lifecycle
# (can_start opens, on_start schedules, can_end closes — the on_action
# route did nothing in game; KNOWLEDGE.md). Observed: situations spawn
# on the FIRST MONTHLY TICK after can_start passes, not on the day
# itself — anchor day offsets to that tick and recalibrate in game.
#
# AUTHOR CHECKLIST (every item cost a Norman round):
# - RAILROAD beats carry NO event-level trigger (guards go INSIDE
#   options as if/limit); FLAVOR events MAY carry one — the resolved
#   trigger law, docs/EVENT-SYSTEM.md 4.3
# - wars that must exist in the opening weeks are SHIPPED in 16_wars,
#   never declared from script (the round-5 lesson)
# - CBs are granted in on_start, BEFORE any legality check
# - prev is ONE scope hop; two hops down use save_scope_as
# - every c:TAG link is ?=-guarded

{key} = {{
	monthly_spawn_chance = 1

	can_start = {{
		always = no
		# AUTHOR GATE — replace with the real gate, e.g.:
		# current_date >= 1066.9.15
		# country_exists = c:XXX
	}}

	on_start = {{
{on_start_body}	}}

	can_end = {{
		always = no
		# AUTHOR GATE — the real end conditions render in the panel's
		# END_REQUIREMENTS card.
	}}

	on_monthly = {{
	}}

	on_ended = {{
	}}

	# map_color / legend_key / secondary_map_color: clone the exact
	# shapes from in_game/common/situations/norman_conquest.txt (proven
	# in game) once the sides are final. Named colors for the sides are
	# in main_menu/common/named_colors/zz_1066_{key}_colors.txt.
}}
"""

EVENT_TPL = """######################################
# {num} — {comment}
######################################

{key}.{num} = {{
	type = country_event
	category = situation_event

	title = {key}.{num}.title
	desc = {key}.{num}.desc
	outcome = neutral

	image = "gfx/interface/illustrations/situation/_default.dds"

	option = {{
		name = {key}.{num}.a
	}}
}}
"""

GUI_TPL = """situation_panel = {{

	##################################### SUBHEADER #####################################

	blockoverride "situation_subheader_content" {{}}

	##################################### MAIN CONTENT #####################################

	# Cards sit DIRECTLY in the blockoverride, no wrapping vbox — the
	# measured two-card lesson (a wrapping expanding vbox spreads them).

	blockoverride "situation_panel_main_content" {{

		situation_card_expandable = {{
			blockoverride "header_button_onclick" {{
				onclick = "[LateralView.Vars.Toggle( '{k}_desc_toggled' )]"
			}}
			blockoverride "header_text" {{
				text = "{key}"
			}}
			blockoverride "header_icon" {{
				texture = "gfx/interface/icons/traits/_default.dds"
			}}
			blockoverride "bottom_content" {{
				text_multi = {{
					margin = {{ 15 10 }}
					layoutpolicy_horizontal = expanding
					max_width = 460
					autoresize = yes
					text = "{key}_desc"
					using = fontsize_medium
				}}
			}}
			blockoverride "bottom_content_onclick" {{
				visible = "[LateralView.Vars.Exists( '{k}_desc_toggled' )]"
			}}
			blockoverride "icon_replace_visible_yes" {{
				visible = "[LateralView.Vars.Exists( '{k}_desc_toggled' )]"
			}}
			blockoverride "icon_replace_visible_not" {{
				visible = "[Not(LateralView.Vars.Exists( '{k}_desc_toggled' ))]"
			}}
		}}

		situation_card_expandable = {{
			blockoverride "header_button_onclick" {{
				onclick = "[LateralView.Vars.Toggle( '{k}_req_toggled' )]"
			}}
			blockoverride "header_text" {{
				text = "END_REQUIREMENTS"
			}}
			blockoverride "header_icon" {{
				texture = "gfx/interface/icons/disasters/end_requirements_green.dds"
			}}
			blockoverride "bottom_content" {{
				TooltipRequirementsList = {{
					textcontext = "[SituationView.GetActiveSituation.GetSituation.GetEndConditions]"
				}}
			}}
			blockoverride "visible_hint" {{}}
			blockoverride "onaction_hint" {{}}
			blockoverride "bottom_content_onclick" {{
				visible = "[LateralView.Vars.Exists( '{k}_req_toggled' )]"
			}}
			blockoverride "icon_replace_visible_yes" {{
				visible = "[LateralView.Vars.Exists( '{k}_req_toggled' )]"
			}}
			blockoverride "icon_replace_visible_not" {{
				visible = "[Not(LateralView.Vars.Exists( '{k}_req_toggled' ))]"
			}}
		}}
	}}

}}
"""

BOM = b"\xef\xbb\xbf"


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
    title, desc, info = spec["title"], spec["desc"], spec["info"]
    events = spec["events"]
    if "\n" in desc or "\n" in info:
        sys.exit("loc values must be ONE physical line (the parser drops "
                 "multi-line entries)")
    k_short = "".join(w[0] for w in key.split("_"))[:4]

    on_start = "".join(
        f"\t\t# {c}\n\t\ttrigger_event_non_silently = {{ id = {key}.{n} }}\n"
        for n, c in events)

    written = []
    written.append(_write(
        os.path.join(out, "in_game", "common", "situations", key + ".txt"),
        SITUATION_TPL.format(key=key, title=title, on_start_body=on_start),
        bom=True))

    ev_body = ("# %s — SCAFFOLD events. NO event-level triggers (the round-2\n"
               "# class); guards go inside options as if/limit.\n\n" % title
               + "\n".join(EVENT_TPL.format(key=key, num=n, comment=c)
                           for n, c in events))
    written.append(_write(
        os.path.join(out, "in_game", "events", "situations", key + ".txt"),
        ev_body, bom=True))

    written.append(_write(
        os.path.join(out, "in_game", "gui", "panels", "situation",
                     key + ".gui"),
        GUI_TPL.format(key=key, k=k_short), bom=False))

    loc = ["﻿l_english:",
           f' {key}: "{title}"',
           f' {key}_desc: "{desc}"',
           f' {key}_info: "{info}"']
    for n, c in events:
        loc += [f' {key}.{n}.title: "TODO — {c}"',
                f' {key}.{n}.desc: "TODO"',
                f' {key}.{n}.a: "TODO"']
    written.append(_write(
        os.path.join(out, "main_menu", "localization", "english",
                     f"1066_{key}_l_english.yml"),
        "\n".join(loc) + "\n", bom=False))   # BOM is in the ﻿ literal

    new_colors = {t: v for t, v in spec["sides"].items() if v}
    if new_colors:
        body = ("colors = {\n"
                + "".join(f"\tmap_{t} = {v}\n" for t, v in new_colors.items())
                + "}\n")
        written.append(_write(
            os.path.join(out, "main_menu", "common", "named_colors",
                         f"zz_1066_{key}_colors.txt"),
            body, bom=True))

    # ------------------------------------------------------ self-check ---
    for p in written:
        raw = open(p, "rb").read()
        wants_bom = not p.endswith(".gui")
        if (raw[:3] == BOM) != wants_bom:
            sys.exit(f"BOM self-check failed on {p}")
        text = raw.decode("utf-8-sig")
        if text.count("{") != text.count("}"):
            sys.exit(f"brace balance self-check failed on {p}")
        if p.endswith(".yml"):
            for line in text.splitlines()[1:]:
                if line and not re.match(r'^ [A-Za-z0-9_.]+: ".*"$', line):
                    sys.exit(f"loc line shape self-check failed on {p}: "
                             f"{line!r}")

    print(f"scaffold '{key}' written — {len(written)} files:")
    for p in written:
        print("  " + os.path.relpath(p, out))
    print("""
STILL YOURS TO DO (the generator cannot):
  1. flip the two `always = no` author gates once the design is real
  2. map_color / legend blocks (clone norman_conquest.txt's exact shape)
  3. every trigger/effect under the citation rule — script docs first
  4. CBs/wargoals if the situation fights (+ their war_goal_* loc pairs)
  5. bump the harness min_counts in the SAME commit that arms the gate
  6. the illustration and header icon (defaults are placeholders)""")


if __name__ == "__main__":
    argv = sys.argv[1:]
    out = MOD
    if "--out" in argv:
        i = argv.index("--out")
        out = argv[i + 1]
        del argv[i:i + 2]
    if len(argv) != 1:
        sys.exit("usage: python tools/new_situation.py <spec-key> [--out DIR]")
    args = argv
    if args[0] == "demo" and os.path.abspath(out) == os.path.abspath(MOD):
        sys.exit("the demo spec only generates outside the repo (--out)")
    generate(args[0], out)
