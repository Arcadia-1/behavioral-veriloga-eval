# Successive Approximation Calibration Search FSM Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `successive_approximation_calibration_search_fsm.va`: `successive_approximation_calibration_search_fsm`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_SEARCH_STATE`: Active reset restores out to target, the current step to step_init, the cycle count to zero, and metric low.
- `P_SIGNED_TRIAL_UPDATE`: On each active rising clk update before completion, vin above target increases out by the current step and vin below target decreases it.
- `P_SUCCESSIVE_STEP_HALVING`: The current step halves after every active decision update, yielding the public successive-approximation sequence from step_init.
- `P_FOUR_STEP_DONE`: Metric asserts after four active search updates and subsequent rising clocks hold the completed trial state until reset.
- `P_TRIM_CLAMP`: Out remains within vmin through vmax for every trial update.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `successive_approximation_calibration_search_fsm.va`.
Every supplied `.va` file is editable; do not add or omit files.
