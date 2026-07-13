# Event Reacquire Lock Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `event_reacquire_lock_detector.va`: `event_reacquire_lock_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RECORD_REFERENCE_CLOCK_RISING_EDGE_TIME`: Record reference clock rising-edge time and evaluate feedback clock rising edges against it.
- `P_REQUIRE_CONSECUTIVE_IN_WINDOW_FEEDBACK_EDGE`: Require consecutive in-window feedback edge errors before lock asserts.
- `P_CLEAR_LOCK_STATE_AND_PROGRESS_WHEN`: Clear lock state and progress when reset rises or is sampled high.
- `P_EXPOSE_PHASE_METRIC_AND_STATE_MON`: Expose phase_metric and state_mon as bounded voltage-coded observables.
- `P_USE_EVENT_BODY_STATE_UPDATES_PLUS`: Use event-body state updates plus local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `event_reacquire_lock_detector.va`.
Do not add or omit artifacts.
