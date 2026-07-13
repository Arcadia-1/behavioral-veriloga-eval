# Event Counter Windowed 16b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `event_counter_windowed_16b.va`: `event_counter_windowed_16b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_WINDOW_OPEN`: A rising gate crossing clears the count, opens a new measurement window, and drives done low.
- `P_IN_WINDOW_COUNT`: Each rising event crossing increments the count exactly once only while the window is active and gate is high.
- `P_OUT_OF_WINDOW_IGNORE`: Event crossings before a window opens or after it closes do not change the held result.
- `P_WINDOW_CLOSE_HOLD`: A falling gate crossing closes the window, preserves the final count, and asserts done.
- `P_BIT_ORDER_AND_LEVELS`: count0 is the least significant bit and count15 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `event_counter_windowed_16b.va`.
Do not add or omit artifacts.
