# Ref Flash 15level Decoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ref_flash_15level_decoder.va`: `ref_flash_15level_decoder`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_FIFTEEN_TAP_COUNT`: Each rising `clks` crossing counts voltage-coded assertions across the 15 tap inputs.
- `P_FULL_TAP_COVERAGE`: Upper and lower tap inputs all contribute to the count; no subset of taps is ignored.
- `P_FRACTION_NORMALIZATION_AND_GAIN`: `dout` reports the count divided by 15 without additional gain scaling.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ref_flash_15level_decoder.va`.
Every supplied `.va` file is editable; do not add or omit files.
