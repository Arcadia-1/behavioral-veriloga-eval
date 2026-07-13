# Duty Cycle Meter 8b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `duty_cycle_meter_8b.va`: `duty_cycle_meter_8b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_COMPLETE_CYCLE_MEASUREMENT`: A new duty result is produced only after observing a rising edge, one intervening falling edge, and the next rising edge.
- `P_HIGH_FRACTION_CODE`: For each complete cycle, the unsigned code is the rounded value of 255 times high time divided by period.
- `P_CODE_SATURATION`: The reported duty code is saturated to the inclusive range 0 through 255.
- `P_VALID_HOLD`: valid remains low before the first complete measurement and asserts and holds high after a duty result is available.
- `P_BIT_ORDER_AND_LEVELS`: duty0 is the least significant bit and duty7 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `duty_cycle_meter_8b.va`.
Do not add or omit artifacts.
