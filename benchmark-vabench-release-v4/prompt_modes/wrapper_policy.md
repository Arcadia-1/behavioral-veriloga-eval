# V4 Pilot Prompt Wrapper Policy

The v4 pilot separates task content from experiment execution conditions. Every
mode starts from the same canonical task contract in `instruction.md`; the
wrapper changes only whether the run is direct or agentic and which generic
skill text is provided.

See `g0_g5_mode_discussion.md` for the detailed interpretation of each mode
and the recommended comparisons.

## Canonical Prompt

The canonical prompt is the task's `instruction.md`. It contains the public task
contract only. It must not mention feedback-oracle profiles, score `.scs` decks,
EVAS, private score evaluation, checker internals, Vela paths, transient stop
times, validation sample windows, or local run mechanics.

## Direct Modes

`G0` and `G1` are direct one-shot modes. They receive no shell, no file
browsing, no feedback-oracle access, no EVAS permission, no public feedback TB,
no checker profile, and no private scoring assets.

- `G0` receives only the canonical task prompt and the output file protocol.
- `G1` receives `G0` plus a generic Verilog-A writing checklist.

`G1` is not a clean baseline, but it is still a direct one-shot condition.

## Agentic Modes

`G2`, `G3`, `G4`, and `G5` are agentic feedback-loop modes. They receive the
canonical prompt plus a wrapper that grants access to a black-box feedback
oracle. They may inspect only the public files `instruction.md`,
`public_contract.json`, `test_feedback/public_tb.scs`, and
`test_feedback/run_feedback.py`; they may run the feedback command against
candidate artifacts.

The public feedback TB is visible as a debugging example. Private score
testbenches, checker profiles, private checker internals, solution files, and
negative variants remain inaccessible.

The final score is always computed with the private `evaluator/score_tb.scs`
and hidden checker profile. That score TB must stay within the same public task
contract as the feedback TB while changing numeric stimuli, timing, corners, or
coverage strength enough to discourage hard-coding the public feedback deck.

The agentic skill conditions are a 2x2 ablation:

- `G2`: agent with visible feedback oracle and no additional Verilog-A or feedback/debug skill wrapper.
- `G3`: agent with visible feedback oracle plus generic Verilog-A writing skill.
- `G4`: agent with visible feedback oracle plus generic feedback/debug skill.
- `G5`: agent with visible feedback oracle plus both Verilog-A writing skill and feedback/debug skill.

The reusable skill texts are stored in `prompt_modes/skills/`. Rendered prompt
metadata and experiment records preserve the skill file path and SHA-256 hash.

AHDL-like preflight or lint-style diagnostics emitted by the feedback oracle are
part of the EVAS-backed feedback channel. They are not modeled as a separate
gate or a separate experiment condition.

## Removed Embedded-Interface Condition

The earlier direct prompt that embedded `public_contract.json` and
`test_feedback/run_feedback.py` has been removed from the main G0-G5 design.
That condition mixed prompt-format exposure with direct generation and was not a
clean ablation for either one-shot generation or agentic feedback.

## Experiment Records

Prompt rendering and experiment execution are separate. The structured records
under `reports/experiment_specs/` state which process family, files, commands,
and skills each mode may use.

- `G0` and `G1` must use direct `llms` records.
- `G2`, `G3`, `G4`, and `G5` must use `agents` records.
- Direct records expose no feedback files, embedded feedback-interface files,
  or feedback commands.
- Agentic records expose only the public feedback surface, the public feedback
  TB, and the black-box feedback command.

The data-spec audit checks this boundary so the mode name cannot drift away from
the actual execution interface.
