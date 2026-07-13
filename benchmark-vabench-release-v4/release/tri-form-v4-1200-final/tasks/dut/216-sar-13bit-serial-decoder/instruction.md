# SAR 13bit Serial Decoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sar_13bit_serial_decoder.va`: `sar_13bit_serial_decoder`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CONSUME_ONE_MSB_FIRST_BIT_ON`: Consume one MSB-first bit on each rising `ready` crossing, starting with bit 12 and ending with bit 0.
- `P_ADD_THE_CORRESPONDING_BINARY_WEIGHT_WHEN`: Add the corresponding binary weight when `din` is high.
- `P_INCREMENT_DNUM_FOR_EACH_HIGH_DECISION`: Increment `dnum` for each high decision in the current frame.
- `P_ON_EACH_RISING_CLKS_CROSSING_PUBLISH`: On each rising `clks` crossing, publish the previous frame as a normalized bipolar output.
- `P_MAP_AN_ALL_LOW_FRAME_TO`: Map an all-low frame to `-0.5` and an all-high frame near `+0.5`.
- `P_AFTER_PUBLISHING_RESET_THE_ACCUMULATOR_HIGH`: After publishing, reset the accumulator, high-bit count, and bit pointer for the next frame.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sar_13bit_serial_decoder.va`.
Do not add or omit artifacts.
