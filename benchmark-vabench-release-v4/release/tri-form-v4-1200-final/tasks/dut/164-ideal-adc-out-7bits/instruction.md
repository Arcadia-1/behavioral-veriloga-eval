# Ideal ADC Out 7bits

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ideal_adc_out_7bits_scalar.va`: `ideal_adc_out_7bits_scalar`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_THRESHOLD_CODE_DETECTION`: Each `din` input is interpreted as asserted only when it is above `vth`.
- `P_WEIGHTED_GROUP_SUM`: `din6` through `din2` contribute 16, 8, 4, 2, and 1 unit groups, while `din1` and `din0` contribute half-LSB and quarter-LSB trim groups.
- `P_SCALED_SCALAR_OUTPUT`: `dout` represents the correctly scaled fractional scalar sum without fixed offsets or denominator errors.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ideal_adc_out_7bits_scalar.va`.
Do not add or omit artifacts.
