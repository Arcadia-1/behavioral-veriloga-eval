# Ideal ADC Out 7bits Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ideal_adc_out_7bits_scalar.va`: `ideal_adc_out_7bits_scalar`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_THRESHOLD_CODE_DETECTION`: Each `din` input is interpreted as asserted only when it is above `vth`.
- `P_WEIGHTED_GROUP_SUM`: `din6` through `din2` contribute 16, 8, 4, 2, and 1 unit groups, while `din1` and `din0` contribute half-LSB and quarter-LSB trim groups.
- `P_SCALED_SCALAR_OUTPUT`: `dout` represents the correctly scaled fractional scalar sum without fixed offsets or denominator errors.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ideal_adc_out_7bits_scalar.va`.
Every supplied `.va` file is editable; do not add or omit files.
