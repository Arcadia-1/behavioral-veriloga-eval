# Event Reacquire Lock Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Event Reacquire Lock Detector` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_RECORD_REFERENCE_CLOCK_RISING_EDGE_TIME`: Record reference clock rising-edge time and evaluate feedback clock rising edges against it.
- `P_REQUIRE_CONSECUTIVE_IN_WINDOW_FEEDBACK_EDGE`: Require consecutive in-window feedback edge errors before lock asserts.
- `P_CLEAR_LOCK_STATE_AND_PROGRESS_WHEN`: Clear lock state and progress when reset rises or is sampled high.
- `P_EXPOSE_PHASE_METRIC_AND_STATE_MON`: Expose phase_metric and state_mon as bounded voltage-coded observables.
- `P_USE_EVENT_BODY_STATE_UPDATES_PLUS`: Use event-body state updates plus local analog helper functions rather than user task/endtask syntax.

The required trace names are: `time`, `fb_clk`, `lock`, `phase_metric`, `ref_clk`, `rst`, `state_mon`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
