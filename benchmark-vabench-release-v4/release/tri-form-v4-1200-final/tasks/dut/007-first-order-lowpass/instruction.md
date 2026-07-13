# First Order Lowpass

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `first_order_lowpass.va`: `first_order_lowpass`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_STATE`: vout begins at 0 V before the first periodic update.
- `P_PERIODIC_UPDATE`: The internal output updates only on the public 500 ps periodic schedule using y := y + alpha*(vin-y).
- `P_STEP_MONOTONICITY`: For a positive input step, vout is monotone and bounded by the input level.
- `P_LOW_PASS_RESPONSE`: The step response is slower than an instantaneous copy of vin.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `first_order_lowpass.va`.
Do not add or omit artifacts.
