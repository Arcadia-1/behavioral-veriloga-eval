# Event Counter Windowed 16b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `event_counter_windowed_16b.va`: `event_counter_windowed_16b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_WINDOW_OPEN`: A rising gate crossing clears the count, opens a new measurement window, and drives done low.
- `P_IN_WINDOW_COUNT`: Each rising event crossing increments the count exactly once only while the window is active and gate is high.
- `P_OUT_OF_WINDOW_IGNORE`: Event crossings before a window opens or after it closes do not change the held result.
- `P_WINDOW_CLOSE_HOLD`: A falling gate crossing closes the window, preserves the final count, and asserts done.
- `P_BIT_ORDER_AND_LEVELS`: count0 is the least significant bit and count15 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `event_counter_windowed_16b.va`.
Every supplied `.va` file is editable; do not add or omit files.
