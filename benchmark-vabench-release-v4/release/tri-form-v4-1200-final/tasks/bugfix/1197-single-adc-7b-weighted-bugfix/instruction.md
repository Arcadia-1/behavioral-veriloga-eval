# Single ADC 7b Weighted Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `single_adc_7b_weighted.va`: `single_adc_7b_weighted`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INPUT_THRESHOLDING`: Treat each `din` input as high only when it is above `vth`.
- `P_WEIGHTED_CODE_SUM`: Sum the selected 7-bit weights, including the MSB contribution, using the declared weight basis.
- `P_NORMALIZED_SINGLE_ENDED_OUTPUT`: Drive the normalized single-ended ADC output from the weighted code without extra fixed offsets or scale errors.
- `P_MONOTONIC_CODE_RESPONSE`: The output changes monotonically with increasing selected code weight.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `single_adc_7b_weighted.va`.
Every supplied `.va` file is editable; do not add or omit files.
