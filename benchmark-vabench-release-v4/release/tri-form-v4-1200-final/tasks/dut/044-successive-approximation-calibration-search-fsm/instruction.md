# Successive Approximation Calibration Search FSM

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `successive_approximation_calibration_search_fsm.va`: `successive_approximation_calibration_search_fsm`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_SEARCH_STATE`: Active reset restores out to target, the current step to step_init, the cycle count to zero, and metric low.
- `P_SIGNED_TRIAL_UPDATE`: On each active rising clk update before completion, vin above target increases out by the current step and vin below target decreases it.
- `P_SUCCESSIVE_STEP_HALVING`: The current step halves after every active decision update, yielding the public successive-approximation sequence from step_init.
- `P_FOUR_STEP_DONE`: Metric asserts after four active search updates and subsequent rising clocks hold the completed trial state until reset.
- `P_TRIM_CLAMP`: Out remains within vmin through vmax for every trial update.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `successive_approximation_calibration_search_fsm.va`.
Do not add or omit artifacts.
