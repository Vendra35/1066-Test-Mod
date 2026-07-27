# 1066 Test Mod — a Europa Universalis V total conversion

Moves the game to **1066.9.15**, the best known of the Crusader Kings III start
dates. Stamford Bridge is ten days out and Hastings a month; Manzikert is five
years away, the First Crusade thirty. Byzantium is still pre-Manzikert, Anatolia
still Greek, Iberia still taifa, the Baltic still pagan, Song China still whole.
The Mongols arrive at 1206, year 140 of a 770-year campaign.

867 and 1178 were weighed and rejected. 1178 is the date the engine cooperates
with and 867 the one it fights; 1066 was chosen on the setting with its cost
accepted in advance — `docs/KNOWLEDGE.md` records the measurements and the
debt, which is that everything before 1342 falls inside a single age.

Nothing is built yet. What exists is the scaffolding that made the previous
project tractable, carried in on day one instead of being rediscovered.

## Documentation map

| Doc | What it is |
|---|---|
| `CLAUDE.md` | The standing rules: setup, verification, hard rules, workflow. **Read first.** |
| `docs/EU5-Vanilla-Script-Docs/` | **The authority.** Console output of `script_docs` and `dump_data_types`: 1798 triggers and 1534 effects with their supported scopes, 289 event targets, 2436 modifier tags, every on_action, 2.9 MB of GUI data types |
| `docs/EU5-ERROR-DECODER.md` | error.log signature → what it means → the fix. Check here before investigating any log line |
| `docs/EU5-MODDING-GUIDE.md` | General EU5 field guide — situations, events, wars, geography, localisation, GUI, and the verification discipline |
| `docs/KNOWLEDGE.md` | This project's own discoveries and decisions, with how each was established |
| `docs/PHASE-2-PLAN.md` | How 1066 becomes historical: the three mechanisms, the region order, and the situation backlog for 1066–1337 |
| `docs/HANDOFF.md` | **Start here when resuming.** What works, what is untested, the traps that already cost time, and the next step |
| `tools/verify_mod.py` | Static verification harness — run after every change |

The guide and the decoder were carried in from the Mongol Resurgence project and
name that mod's files in their examples. That is deliberate: a case that
actually happened is worth more than an abstract rule.

## The two things that matter most

**Look it up, do not remember it.** `docs/EU5-Vanilla-Script-Docs/` says what is
*legal* — including every trigger's supported scopes. Grepping vanilla only ever
showed what someone happened to write. Regenerate after a game patch: launch
with `-debug_mode`, console `script_docs` then `dump_data_types`, copy the logs
out of the user folder.

**A green harness must mean something.** Every check prints its item count and a
check with nothing to scan fails rather than passing quietly. On a fresh repo
most checks report `SKIP` — that is honest, and each one's `min_count` should be
raised as content lands. When the game finds a bug the harness did not, that is
two commits: the fix, and the check, proven against a known positive.
