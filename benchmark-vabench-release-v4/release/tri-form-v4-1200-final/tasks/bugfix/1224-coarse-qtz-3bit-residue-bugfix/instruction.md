# Coarse QTZ 3bit Residue Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `coarse_qtz_3bit_residue.va`: `coarse_qtz_3bit_residue`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLIP_VIN_TO_THE_RANGE_FROM`: Clip `vin` to the range from `-vref` to `+vref`.
- `P_QUANTIZE_THE_CLIPPED_VALUE_INTO_EIGHT`: Quantize the clipped value into eight 3-bit codes using round-to-nearest behavior.
- `P_SATURATE_THE_CODE_AT_THE_ENDPOINTS`: Saturate the code at the endpoints.
- `P_USE_UNIFORMLY_SPACED_QUANTIZATION_LEVELS_START`: Use uniformly spaced quantization levels starting at `-vref`, with one LSB equal to one eighth of the full input span.
- `P_DRIVE_D0_D1_AND_D2_AS`: Drive `d0`, `d1`, and `d2` as LSB-to-MSB voltage-coded bits.
- `P_DRIVE_VRES_AS_THE_CLIPPED_INPUT`: Drive `vres` as the clipped input minus the selected quantized analog level.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `coarse_qtz_3bit_residue.va`.
Every supplied `.va` file is editable; do not add or omit files.
