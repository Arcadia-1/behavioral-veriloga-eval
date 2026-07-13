# Offset Bisection Driver

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `offset_bisection_driver.va`: `offset_bisection_driver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_BISECTION_INITIAL_STATE`: The differential residue initializes to zero, the step initializes to `step_initial`, and the previous decision polarity initializes to the low-decision direction.
- `P_FALLING_CLOCK_DECISION_UPDATE`: On each falling `clk` crossing, sample `vout` and update the residue using the specified comparator polarity.
- `P_SIGN_CHANGE_STEP_HALVING`: The bisection step halves when the sampled decision polarity changes.
- `P_VCM_CENTERED_DIFFERENTIAL_DRIVE`: `vinp` and `vinn` remain centered around `vcm` with half of the differential residue on each side.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `offset_bisection_driver.va`.
Do not add or omit artifacts.
