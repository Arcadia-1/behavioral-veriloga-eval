# SAR 13bit Serial Decoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sar_13bit_serial_decoder.va`: `sar_13bit_serial_decoder`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CONSUME_ONE_MSB_FIRST_BIT_ON`: Consume one MSB-first bit on each rising `ready` crossing, starting with bit 12 and ending with bit 0.
- `P_ADD_THE_CORRESPONDING_BINARY_WEIGHT_WHEN`: Add the corresponding binary weight when `din` is high.
- `P_INCREMENT_DNUM_FOR_EACH_HIGH_DECISION`: Increment `dnum` for each high decision in the current frame.
- `P_ON_EACH_RISING_CLKS_CROSSING_PUBLISH`: On each rising `clks` crossing, publish the previous frame as a normalized bipolar output.
- `P_MAP_AN_ALL_LOW_FRAME_TO`: Map an all-low frame to `-0.5` and an all-high frame near `+0.5`.
- `P_AFTER_PUBLISHING_RESET_THE_ACCUMULATOR_HIGH`: After publishing, reset the accumulator, high-bit count, and bit pointer for the next frame.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sar_13bit_serial_decoder.va`.
Every supplied `.va` file is editable; do not add or omit files.
