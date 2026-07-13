# Duty Cycle Meter 8b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `duty_cycle_meter_8b.va`: `duty_cycle_meter_8b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_COMPLETE_CYCLE_MEASUREMENT`: A new duty result is produced only after observing a rising edge, one intervening falling edge, and the next rising edge.
- `P_HIGH_FRACTION_CODE`: For each complete cycle, the unsigned code is the rounded value of 255 times high time divided by period.
- `P_CODE_SATURATION`: The reported duty code is saturated to the inclusive range 0 through 255.
- `P_VALID_HOLD`: valid remains low before the first complete measurement and asserts and holds high after a duty result is available.
- `P_BIT_ORDER_AND_LEVELS`: duty0 is the least significant bit and duty7 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `duty_cycle_meter_8b.va`.
Every supplied `.va` file is editable; do not add or omit files.
