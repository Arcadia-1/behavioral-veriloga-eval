# DAC Restore 10bit Offset Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dac_restore_10bit_offset.va`: `dac_restore_10bit_offset`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_CODE_SAMPLING`: Only rising crossings of `clk` through `vth` update the held DAC output; input-bit changes between clock crossings do not alter `vout`.
- `P_WEIGHTED_REDUNDANT_CODE`: `D10` is the largest weight, `D0` is the LSB, and `D6` and `D7` both contribute the redundant 64-LSB weight before scaling.
- `P_OFFSET_MIDRISE_OUTPUT`: The asserted weighted code is shifted by the source -32 LSB offset and placed at the mid-rise half-LSB output level using the public `lsb` scale.
- `P_OUTPUT_SMOOTH_HOLD`: `vout` transitions smoothly to each sampled code value and holds that value until the next qualifying clock edge.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dac_restore_10bit_offset.va`.
Every supplied `.va` file is editable; do not add or omit files.
