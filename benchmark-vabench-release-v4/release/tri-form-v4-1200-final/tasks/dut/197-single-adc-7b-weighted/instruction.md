# Single ADC 7b Weighted

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `single_adc_7b_weighted.va`: `single_adc_7b_weighted`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INPUT_THRESHOLDING`: Treat each `din` input as high only when it is above `vth`.
- `P_WEIGHTED_CODE_SUM`: Sum the selected 7-bit weights, including the MSB contribution, using the declared weight basis.
- `P_NORMALIZED_SINGLE_ENDED_OUTPUT`: Drive the normalized single-ended ADC output from the weighted code without extra fixed offsets or scale errors.
- `P_MONOTONIC_CODE_RESPONSE`: The output changes monotonically with increasing selected code weight.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `single_adc_7b_weighted.va`.
Do not add or omit artifacts.
