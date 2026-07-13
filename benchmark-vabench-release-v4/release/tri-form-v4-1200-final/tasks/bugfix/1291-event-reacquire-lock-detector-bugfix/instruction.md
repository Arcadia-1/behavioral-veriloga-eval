# Event Reacquire Lock Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `event_reacquire_lock_detector.va`: `event_reacquire_lock_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RECORD_REFERENCE_CLOCK_RISING_EDGE_TIME`: Record reference clock rising-edge time and evaluate feedback clock rising edges against it.
- `P_REQUIRE_CONSECUTIVE_IN_WINDOW_FEEDBACK_EDGE`: Require consecutive in-window feedback edge errors before lock asserts.
- `P_CLEAR_LOCK_STATE_AND_PROGRESS_WHEN`: Clear lock state and progress when reset rises or is sampled high.
- `P_EXPOSE_PHASE_METRIC_AND_STATE_MON`: Expose phase_metric and state_mon as bounded voltage-coded observables.
- `P_USE_EVENT_BODY_STATE_UPDATES_PLUS`: Use event-body state updates plus local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `event_reacquire_lock_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
