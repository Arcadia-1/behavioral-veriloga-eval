# Thermometer To Binary Encoder 8b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `therm_to_bin_8b.va`: `therm_to_bin_8b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_VALID_CUMULATIVE_WORD`: valid is high exactly for prefix thermometer words representing counts 0 through 255: asserted inputs start at th[0], contain no low-to-high hole, and th[255] remains low; the all-low word is valid and the all-high 256-line word is invalid.
- `P_UNSIGNED_COUNT`: For a valid word, b[7:0] equals the number of asserted thermometer inputs, with b[7] the most significant bit and b[0] the least significant bit.
- `P_INVALID_ZERO_CODE`: For any non-cumulative thermometer word, valid is low and every binary output bit is low.
- `P_ENDPOINT_CODES`: The all-low word produces code 0, while th[0] through th[254] high and th[255] low produces code 255.
- `P_OUTPUT_LEVELS`: Binary and valid outputs use 0 V for logic low and vdd for logic high with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `therm_to_bin_8b.va`.
Do not add or omit artifacts.
