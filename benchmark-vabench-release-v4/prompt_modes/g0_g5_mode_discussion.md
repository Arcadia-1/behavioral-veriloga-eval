# G0-G5 Mode Discussion

The v4 pilot uses six main experiment conditions. Every condition starts from
the same clean canonical task contract. The differences are the execution mode
and the generic skill wrappers.

## Mode Summary

| Mode | Short name | Process family | Verilog-A skill | Feedback/debug skill | Feedback access | Intended role |
|---|---|---|---|---|---|---|
| `G0` | direct baseline | `llms` | no | no | none | clean one-shot baseline |
| `G1` | direct + Verilog-A skill | `llms` | yes | no | none | direct writing-skill ablation |
| `G2` | agent + visible feedback oracle | `agents` | no | no | runnable public oracle | common oracle-loop baseline |
| `G3` | agent + oracle + Verilog-A skill | `agents` | yes | no | runnable public oracle | Verilog-A skill effect in agents |
| `G4` | agent + oracle + feedback/debug skill | `agents` | no | yes | runnable public oracle | feedback-use skill effect |
| `G5` | agent + oracle + both skills | `agents` | yes | yes | runnable public oracle | combined agent skill condition |

## G0: Direct Baseline

`G0` is the pure direct-answer baseline. The model sees only:

- the canonical task contract;
- the required output file protocol.

It does not get shell access, file browsing, feedback-oracle access, EVAS
permission, private score details, or any skill/checklist text.

Use `G0` to measure how well a model can implement the requested Verilog-A
artifact from the public task contract alone.

## G1: Direct One-Shot With Verilog-A Skill

`G1` keeps the direct one-shot setting but adds a clean Verilog-A writing
checklist. The checklist is generic: it reminds the model about exact interface
preservation, includes, electrical ports, module-scope declarations, analog
event usage, unconditional output contributions, and exact file output.

It still does not expose shell access, file browsing, feedback-oracle access,
EVAS, private score testbenches, checker profiles, Vela paths, or local
simulator instructions.

Use `G1` to isolate whether a general Verilog-A writing skill improves direct
generation, without giving the model executable feedback.

## G2: Agent With Visible Feedback Oracle

`G2` changes the process family from direct `llms` to `agents`. The agent sees
the canonical task contract plus a minimal wrapper that permits the public
black-box feedback oracle.

The agent may:

- inspect the public task files `instruction.md`, `public_contract.json`,
  `test_feedback/public_tb.scs`, and `test_feedback/run_feedback.py`;
- run the feedback command against a candidate source directory;
- use shell/file operations needed for that feedback loop.

The feedback oracle may emit AHDL-like preflight diagnostics, EVAS simulation
errors, trace-availability errors, and behavior-property diagnostics. The
public feedback TB is visible as a debugging example and is the only TB the
agent can use during the feedback loop. Private score testbenches, checker
profiles, and final scoring assets remain inaccessible.

Use `G2` to measure the value of an agentic edit-run-debug loop when the common
capability is the visible feedback oracle and no additional Verilog-A or
feedback/debug skill wrapper is supplied.

## G3: Agent Plus Verilog-A Skill

`G3` is `G2` plus the same clean Verilog-A writing checklist used in `G1`.

It keeps the feedback oracle from `G2`, but adds generic Verilog-A
implementation guidance. It does not add feedback/debug strategy beyond the
minimal feedback interface wrapper.

Use `G3` to measure whether Verilog-A writing guidance improves an agentic
feedback loop.

## G4: Agent Plus Feedback/Debug Skill

`G4` is `G2` plus generic feedback/debug guidance. It does not include the
Verilog-A writing checklist.

The feedback/debug skill tells the agent how to use public feedback output:
triage AHDL-like preflight and lint diagnostics, EVAS compile or simulation
errors, trace-availability failures, and behavior-property diagnostics. It must
not reveal private score testbenches, checker profiles, private checker
internals, task-specific sample windows, or gold implementation details.

Use `G4` to measure whether a generic strategy for using feedback improves the
agent loop independently of Verilog-A writing guidance.

## G5: Agent Plus Both Skills

`G5` is the full combined agent condition:

- canonical task contract;
- runnable black-box feedback oracle;
- Verilog-A writing checklist;
- feedback/debug skill.

Use `G5` to measure whether the two generic skills combine constructively in an
agentic feedback loop.

## Recommended Comparisons

- `G0 -> G1`: effect of Verilog-A writing guidance in direct one-shot.
- `G0 -> G2`: effect of moving from direct one-shot to agentic feedback with no
  extra skill wrapper.
- `G1 -> G3`: effect of moving from direct to agentic execution when both runs
  have the Verilog-A writing skill.
- `G2 -> G3`: effect of Verilog-A writing guidance inside the agent loop.
- `G2 -> G4`: effect of feedback/debug guidance inside the agent loop.
- `G3/G4 -> G5`: whether the two skills stack beyond either skill alone.

## Boundary Rules

- The canonical task prompt is identical across modes for the same task.
- Every mode is finally scored by the evaluator-only score TB and hidden checker.
- Direct modes (`G0`, `G1`) must not mention or expose feedback-oracle access,
  EVAS, private score testbenches, checker profiles, Vela paths, shell access,
  local simulator workflow, or public feedback-interface files.
- Agentic modes (`G2`, `G3`, `G4`, `G5`) expose only the public feedback
  surface, public feedback TB, and black-box feedback command.
- The public feedback TB and private score TB must implement the same public
  task contract; the score TB should only vary held-out stimulus values, timing,
  corners, or coverage strength.
- AHDL-like diagnostics are treated as an EVAS-backed feedback feature exposed
  through the feedback command, not as an additional gate or mode.
- No mode embeds private score testbenches, checker profiles, private score
  assets, or private checker internals in the prompt.
