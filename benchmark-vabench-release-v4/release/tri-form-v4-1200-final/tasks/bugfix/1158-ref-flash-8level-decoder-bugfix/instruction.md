# Ref Flash 8level Decoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ref_flash_8level_decoder.va`: `ref_flash_8level_decoder`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_EIGHT_TAP_COUNT`: Each rising `clks` crossing counts all eight asserted flash taps into the held decoder count.
- `P_RESIDUE_CENTERING`: `vres` subtracts the centered four-count flash estimate from the sampled input residue.
- `P_OUTPUT_NORMALIZATION`: `dout` reports the tap count normalized by eight without extra output scaling.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ref_flash_8level_decoder.va`.
Every supplied `.va` file is editable; do not add or omit files.
