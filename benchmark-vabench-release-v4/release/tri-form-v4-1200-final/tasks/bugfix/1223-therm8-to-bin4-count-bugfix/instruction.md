# Therm8 To Bin4 Count Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `therm8_to_bin4_count.va`: `therm8_to_bin4_count`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_COUNT_HOW_MANY_OF_TH0_TH7`: Count how many of `th0..th7` are above `vth`.
- `P_ENCODE_THE_COUNT_AS_A_4`: Encode the count as a 4-bit binary word.
- `P_DRIVE_B0_B3_AS_VOLTAGE_CODED`: Drive `b0..b3` as voltage-coded outputs with `b0` as the least significant bit.
- `P_SUPPORT_ANY_INPUT_PATTERN_BY_COUNTING`: Support any input pattern by counting high inputs rather than assuming a perfectly monotonic thermometer prefix.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `therm8_to_bin4_count.va`.
Every supplied `.va` file is editable; do not add or omit files.
