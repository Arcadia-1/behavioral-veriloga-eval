# DC Aware ADC3bit

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dc_aware_adc3bit.va`: `dc_aware_adc3bit`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_STATIC_CONVERSION`: The output code represents the current vin level without requiring a clock or prior transient event.
- `P_UNIFORM_QUANTIZATION`: The 0-to-vref input span is divided into eight ordered uniform code regions producing unsigned codes 0 through 7.
- `P_INPUT_CLIPPING`: Inputs at or below 0 V produce code 0, and inputs at or above vref produce code 7.
- `P_BINARY_BIT_ORDER`: d2 is the most significant output bit and d0 is the least significant output bit.
- `P_OUTPUT_LEVELS`: Each output bit approaches 0 V for logic low and vh for logic high with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dc_aware_adc3bit.va`.
Do not add or omit artifacts.
