# PAM4 Slicer and Gray Decoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pam4_slicer_gray_decoder.va`: `pam4_slicer_gray_decoder`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears both bits, level metric, and valid.
- `P_RISING_EDGE_SAMPLE_HOLD`: vin is sliced only on enabled rising clk edges and outputs hold between samples.
- `P_PAM4_THRESHOLDS`: The three ordered thresholds divide vin into levels zero through three.
- `P_GRAY_MAPPING`: Levels zero through three map to Gray codes 00, 01, 11, and 10.
- `P_LEVEL_METRIC`: level_metric reports the sliced level as vss plus k/3 of the output span.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pam4_slicer_gray_decoder.va`.
Every supplied `.va` file is editable; do not add or omit files.
