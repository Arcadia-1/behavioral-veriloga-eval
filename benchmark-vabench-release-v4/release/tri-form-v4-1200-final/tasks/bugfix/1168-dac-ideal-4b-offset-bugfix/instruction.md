# DAC Ideal 4b Offset Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dac_ideal_4b_offset.va`: `dac_ideal_4b_offset`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_THRESHOLDED_4BIT_CODE`: `din3` is the MSB and `din0` is the LSB of a 4-bit unsigned code using threshold `vth`.
- `P_OFFSET_PLUS_SCALED_TRIM`: The output equals the public `offset` plus the code-scaled trim increment using the public `scaling` factor.
- `P_EVENT_UPDATED_OUTPUT`: `dout` updates on input threshold crossings or initial step and otherwise holds the smooth voltage output.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dac_ideal_4b_offset.va`.
Every supplied `.va` file is editable; do not add or omit files.
