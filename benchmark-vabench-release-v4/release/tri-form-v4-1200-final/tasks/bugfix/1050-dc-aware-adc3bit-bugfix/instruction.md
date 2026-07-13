# DC Aware ADC3bit Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dc_aware_adc3bit.va`: `dc_aware_adc3bit`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_STATIC_CONVERSION`: The output code represents the current vin level without requiring a clock or prior transient event.
- `P_UNIFORM_QUANTIZATION`: The 0-to-vref input span is divided into eight ordered uniform code regions producing unsigned codes 0 through 7.
- `P_INPUT_CLIPPING`: Inputs at or below 0 V produce code 0, and inputs at or above vref produce code 7.
- `P_BINARY_BIT_ORDER`: d2 is the most significant output bit and d0 is the least significant output bit.
- `P_OUTPUT_LEVELS`: Each output bit approaches 0 V for logic low and vh for logic high with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dc_aware_adc3bit.va`.
Every supplied `.va` file is editable; do not add or omit files.
