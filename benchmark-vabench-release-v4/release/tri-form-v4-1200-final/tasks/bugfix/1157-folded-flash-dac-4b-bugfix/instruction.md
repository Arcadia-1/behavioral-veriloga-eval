# Folded Flash DAC 4b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `folded_flash_dac_4b.va`: `folded_flash_dac_4b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_VOLTAGE_CODED_SUBCODE_DECODE`: `vd1` through `vd3` form the lower subcode and `vd4` selects the folded branch using `vtrans`.
- `P_FOLD_MIRROR_TRANSFER`: The upper folded branch mirrors the subcode around the fold center instead of using a direct unsigned code.
- `P_OUTPUT_SCALE_DENOMINATOR`: The folded code is scaled by the declared 4-bit denominator and reference before driving `vout`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `folded_flash_dac_4b.va`.
Every supplied `.va` file is editable; do not add or omit files.
