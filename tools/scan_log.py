#!/usr/bin/env python3
"""error.log triage — classify every line against the decoder's known
signatures and surface ONLY what is new.

Reads the game's error.log (and optionally the rotated error.N.log
files), buckets each entry into:
  ACCEPTED  — decoded classes counted out of the error budget
              (docs/EU5-ERROR-DECODER.md is the authority; each entry
              names its decoder signature)
  WATCH     — decoded but worth an eye if the count moves
  UNKNOWN   — everything else, printed in full: this is the gold

Usage:
    python tools/scan_log.py                # current error.log
    python tools/scan_log.py --all         # + every rotated error.N.log
    python tools/scan_log.py <path>        # a specific file

The known list is deliberately conservative: a pattern only enters it
once the class is decoded in the decoder. When the game finds
something new, it shows up here loudly instead of drowning in the
known noise. (The idea is the reference project's 663-signature
filter, ours grown from our own decoder.)"""
import glob
import os
import re
import sys

LOG_DIR = os.path.expanduser(
    "~/OneDrive/Belgeler/Paradox Interactive/Europa Universalis V/logs")

# (bucket, label, regex) — first match wins. Labels name the decoder
# entry. Continuation lines (Reason:, indented tooltips, culture
# lists) attach to the previous entry's bucket.
KNOWN = [
    # ------------------------------------------------ REGRESSION ---
    # Classes CONFIRMED DEAD on the 2026-08-01 accumulated-test launch.
    # Any line here means a fix regressed — treat as a finding, not
    # noise. (3702/9635: the Middle Kingdom restore; 1719: audit D2;
    # 592: the claims guard; 410: _BIRTH_FIXES; 1558/1576/169: the
    # template-less restatements; 287: the Ayyub conception fix.)
    ("REGRESSION", "tributary/tusi gate is BACK (Middle Kingdom restore broke?)",
     r"government\.cpp:3702"),
    ("REGRESSION", "CHI culture flood is BACK (Middle Kingdom restore broke?)",
     r"country\.cpp:9635"),
    ("REGRESSION", "parliament_type barrage is BACK (audit D2 regressed)",
     r"initialize_from_bookmark\.cpp:1719"),
    ("REGRESSION", "landless-no-claims is BACK (the claims guard regressed)",
     r"initialize_from_bookmark\.cpp:592"),
    ("REGRESSION", "characters without birth are BACK (_BIRTH_FIXES regressed)",
     r"initialize_from_bookmark\.cpp:410.*no birth scripted"),
    ("REGRESSION", "template-less law barrage is BACK",
     r"initialize_from_bookmark\.cpp:(1558|1576)"),
    ("REGRESSION", "conception-age validator is BACK",
     r"character_manager\.cpp:287"),
    # -------------------------------------------------- ACCEPTED ---
    ("ACCEPTED", "landless-shell law trims (3535 sub-class 3)",
     r"government\.cpp:3535.*Removing invalid law"),
    ("ACCEPTED", "landless/inland privilege trims (3662)",
     r"government\.cpp:3662.*Removing invalid estate privilege"),
    ("ACCEPTED", "ex-vassal French ducal reform trims (3612)",
     r"government\.cpp:3612.*Removing invalid reform"),
    ("ACCEPTED", "stale save/settings load refs (gamestate 133)",
     r"gamestate\.cpp:133"),
    ("ACCEPTED", "estate/pop culture mismatch (pop phase, 237/301)",
     r"initialize_from_bookmark\.cpp:(237|301)"),
    ("ACCEPTED", "releasable-country culture (205)",
     r"initialize_from_bookmark\.cpp:205.*releasable country"),
    ("ACCEPTED", "stranded owner-conditioned building (398)",
     r"initialize_from_bookmark\.cpp:398.*invalid building"),
    ("ACCEPTED", "CHI accepted-culture flood (China review, 9635)",
     r"country\.cpp:9635"),
    ("ACCEPTED", "1337 cabinet names at 1066 (cabinet_effects:44)",
     r"cabinet_effects\.cpp:44"),
    ("ACCEPTED", "vanilla diplomatic relations over limit (1176)",
     r"initialize_from_bookmark\.cpp:1176"),
    ("ACCEPTED", "vanilla double ruler traits on our seats (792)",
     r"initialize_from_bookmark\.cpp:792.*ruler traits"),
    ("ACCEPTED", "MINOR_RULERS child-ruler info (1659)",
     r"initialize_from_bookmark\.cpp:1659.*child as a ruler"),
    ("ACCEPTED", "vanilla formatter tag 'l' (807)",
     r"pdx_text_formatter\.cpp:807"),
    ("ACCEPTED", "scripted war end has no winner (toast loc)",
     r"GetWinnerCountry|WAR_WON_OTHER_COUNTRY"),
    # our IO strips: interactions referencing a stripped IO instance
    # log an invalid-object link + scope errors per evaluation. The
    # Celestial pair DIED with the Middle Kingdom restore; the big
    # remaining source is lordship_of_ireland (5 interactions x ~107).
    # Zero impact — the interactions cannot be taken. An exists-guard
    # override is BANKED if the noise ever matters (decoder).
    ("ACCEPTED", "stripped-IO interaction links (lordship_of_ireland etc.)",
     r"Event target link 'international_organization' returned"),
    ("ACCEPTED", "stripped-IO interaction scope refs (jomini 252 family)",
     r"Scoped object of type 'international_organization' is not valid"
     r"|jomini_script_system\.cpp:252"),
    # law fails the including government's own gates and self-heals
    # (the KAZ-polygyny family; YEM/ABS heir_same_religion 2026-08-01).
    ("ACCEPTED", "law-vs-government mismatch self-heal (3544)",
     r"government\.cpp:3544"),
    # town/market setup on locations LOCATION_VACATED emptied
    # (sarayjuk, chimgi_tura — the Kipchak/Siberia vacate).
    ("ACCEPTED", "buildings on vacated locations (2065)",
     r"initialize_from_bookmark\.cpp:2065"),
    ("ACCEPTED", "stranded owner-buildings (844)",
     r"building\.cpp:844"),
    ("ACCEPTED", "unused-modifier waste (static_modifier 516)",
     r"static_modifier\.cpp:516"),
    ("ACCEPTED", "input/UI environment noise (pdxinput 2896)",
     r"pdxinput_context\.cpp:2896"),
    ("ACCEPTED", "UI tooltip build hiccup (tooltips_utils)",
     r"tooltips_utils\.h:85"),
    ("ACCEPTED", "stale MR game-rule keys in settings",
     r"mr_railroad_on|MR_mongol_resurgence"),
    ("ACCEPTED", "stale-settings empty key refs (persistent_reader 289)",
     r"Failed to read key reference: (:|\"\")"),
    ("ACCEPTED", "system/hardware noise (VRAM, mipmaps, gui perf)",
     r"interface_application\.cpp|icondatabase\.h|Not enough dedicated"
     r"|minimum requirements|poor performance"),
    ("WATCH", "Mongol Resurgence load-time validation (its own repo's list)",
     r"MR_|mr_dominance|mr_[a-z_]+\."),
    # ----------------------------------------------------- WATCH ---
    ("WATCH", "HRE election tooltip on null candidate (hre.txt:328)",
     r"international_organizations/hre\.txt:328"),
    ("WATCH", "vanilla dominion null target (dominion.txt:152)",
     r"subject_types/dominion\.txt:152"),
    # QUN alone as of 2026-08-01 — HLG/SLD's lines died with their
    # landless retirement, proving landless is the class's cure.
    ("WATCH", "army-based country shatters (2477 — QUN only now)",
     r"initialize_from_bookmark\.cpp:2477"),
    ("WATCH", "DUB inherits the Pale's forts (9778)",
     r"country\.cpp:9778"),
    # one line at init while the restored IO's floods stay dead — the
    # leader_modifier demonstrably applies; decode further only if a
    # second symptom appears.
    ("WATCH", "restored Middle Kingdom leader-validity line (io 1557)",
     r"international_organization\.cpp:1557"),
    ("WATCH", "markets on vacated locations (2388 — trade impact unmeasured)",
     r"initialize_from_bookmark\.cpp:2388"),
    ("WATCH", "engine-derived loc key missing (103) — often OURS",
     r"localization_util\.cpp:103"),
]

CONT = re.compile(r"^\s|^Accepted|^Tolerated|^-\s|^\t|Reason:|^$"
                  r"|^file: |^You may experience")


def scan(path):
    known_counts = {}
    watch_lines = []
    unknown = []
    last_bucket = None
    try:
        text = open(path, encoding="utf-8-sig", errors="replace").read()
    except OSError as e:
        sys.exit(f"cannot read {path}: {e}")
    for line in text.splitlines():
        if CONT.match(line) and last_bucket is not None:
            # continuation of the previous entry — inherit its bucket
            if last_bucket == "UNKNOWN":
                unknown.append("    " + line.strip())
            continue
        hit = None
        for bucket, label, pat in KNOWN:
            if re.search(pat, line):
                hit = (bucket, label)
                break
        if hit:
            bucket, label = hit
            known_counts[label] = known_counts.get(label, 0) + 1
            if bucket == "WATCH":
                watch_lines.append(label)
            last_bucket = bucket
        else:
            unknown.append(line.strip())
            last_bucket = "UNKNOWN"
    return known_counts, unknown


def main():
    args = [a for a in sys.argv[1:] if a != "--all"]
    if args:
        paths = args
    elif "--all" in sys.argv:
        paths = sorted(glob.glob(os.path.join(LOG_DIR, "error*.log")))
    else:
        paths = [os.path.join(LOG_DIR, "error.log")]

    for path in paths:
        print(f"=== {os.path.basename(path)} ===")
        counts, unknown = scan(path)
        total = sum(counts.values())
        for label, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            bucket = next(b for b, l, _ in KNOWN if l == label)
            print(f"  [{bucket:8}] {n:5}  {label}")
        real_unknown = [u for u in unknown if u]
        print(f"  known entries: {total}; UNKNOWN lines: {len(real_unknown)}")
        if real_unknown:
            print("  ---- UNKNOWN (the gold) ----")
            for u in real_unknown[:60]:
                print("  " + u)
            if len(real_unknown) > 60:
                print(f"  ... and {len(real_unknown) - 60} more")
        print()


if __name__ == "__main__":
    main()
