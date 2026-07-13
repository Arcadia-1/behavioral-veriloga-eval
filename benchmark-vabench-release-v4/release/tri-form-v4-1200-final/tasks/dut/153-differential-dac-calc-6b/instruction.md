# Differential DAC Calc 6b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `differential_dac_calc_6b.va`: `differential_dac_calc_6b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_SIX_BIT_WEIGHTED_CODE`: Each rising `clks` crossing samples `din0` through `din5` into the declared six-bit weighted DAC code.
- `P_COMPLEMENTARY_DIFFERENTIAL_OUTPUTS`: `voutp` and `voutn` use complementary weighted sums about the common-mode value.
- `P_OUTPUT_SWING_SCALE`: The differential outputs use the declared reference span and bit weights without extra swing scaling.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `differential_dac_calc_6b.va`.
Do not add or omit artifacts.
