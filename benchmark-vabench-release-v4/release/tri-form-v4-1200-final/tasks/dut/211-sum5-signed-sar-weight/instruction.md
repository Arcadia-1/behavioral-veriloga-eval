# SUM5 Signed SAR Weight

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sum5_signed_sar_weight.va`: `sum5_signed_sar_weight`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_TREAT_EACH_DECISION_INPUT_AS_1`: Treat each decision input as `+1` when its voltage is above `vth` and `-1` otherwise. Combine the signed decisions with SAR weights `d5 = 1/2`, `d4 = 1/4`, `d3 = 1/8`, `d2 = 1/16`, and `d1 = 1/32`. Drive `out` to the scaled signed reconstruction:
- `P_TEXT_OUT_1_1_2_SIGNED`: ```text out = 1.1 * (2 * signed_weighted_sum - 1) ```
- `P_THE_BEHAVIOR_IS_CONTINUOUS_WITH_RESPECT`: The behavior is continuous with respect to the voltage-coded decision inputs after thresholding.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sum5_signed_sar_weight.va`.
Do not add or omit artifacts.
