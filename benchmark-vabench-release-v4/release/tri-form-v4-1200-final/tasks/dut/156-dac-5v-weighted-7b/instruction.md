# DAC 5V Weighted 7b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dac_5v_weighted_7b.va`: `dac_5v_weighted_7b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM`: Each rising `clks` crossing samples `din0` through `din6` into the declared seven-bit weighted DAC sum.
- `P_MSB_AND_TERMINATION_CONTRIBUTIONS`: `din0` contributes the largest switched weight and the fixed termination contribution is included.
- `P_REFERENCE_ENDPOINTS_AND_SCALE`: The output uses the declared `refp` and `refn` endpoints and full DAC scale.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dac_5v_weighted_7b.va`.
Do not add or omit artifacts.
