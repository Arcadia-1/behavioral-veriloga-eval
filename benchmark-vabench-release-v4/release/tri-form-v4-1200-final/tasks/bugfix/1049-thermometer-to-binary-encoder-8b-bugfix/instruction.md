# Thermometer To Binary Encoder 8b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `therm_to_bin_8b.va`: `therm_to_bin_8b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_VALID_CUMULATIVE_WORD`: valid is high exactly for prefix thermometer words representing counts 0 through 255: asserted inputs start at th[0], contain no low-to-high hole, and th[255] remains low; the all-low word is valid and the all-high 256-line word is invalid.
- `P_UNSIGNED_COUNT`: For a valid word, b[7:0] equals the number of asserted thermometer inputs, with b[7] the most significant bit and b[0] the least significant bit.
- `P_INVALID_ZERO_CODE`: For any non-cumulative thermometer word, valid is low and every binary output bit is low.
- `P_ENDPOINT_CODES`: The all-low word produces code 0, while th[0] through th[254] high and th[255] low produces code 255.
- `P_OUTPUT_LEVELS`: Binary and valid outputs use 0 V for logic low and vdd for logic high with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `therm_to_bin_8b.va`.
Every supplied `.va` file is editable; do not add or omit files.
