# Therm8 To Bin4 Count

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `therm8_to_bin4_count.va`: `therm8_to_bin4_count`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_COUNT_HOW_MANY_OF_TH0_TH7`: Count how many of `th0..th7` are above `vth`.
- `P_ENCODE_THE_COUNT_AS_A_4`: Encode the count as a 4-bit binary word.
- `P_DRIVE_B0_B3_AS_VOLTAGE_CODED`: Drive `b0..b3` as voltage-coded outputs with `b0` as the least significant bit.
- `P_SUPPORT_ANY_INPUT_PATTERN_BY_COUNTING`: Support any input pattern by counting high inputs rather than assuming a perfectly monotonic thermometer prefix.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `therm8_to_bin4_count.va`.
Do not add or omit artifacts.
