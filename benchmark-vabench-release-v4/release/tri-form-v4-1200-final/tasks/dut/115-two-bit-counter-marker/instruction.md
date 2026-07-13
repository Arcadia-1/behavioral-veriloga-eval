# Two Bit Counter Marker

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `two_bit_counter_marker.va`: `two_bit_counter_marker`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_LOW`: The timing/readout marker output initializes at 0.0 V before any counted edge.
- `P_RISING_EDGE_COUNT`: Only rising crossings of CLKIN through 0.5 V advance the internal modulo-four sequence.
- `P_WRAP_MARKER`: MC is driven to the 1.0 V marker level on the counted edge that wraps the sequence from count 3 to count 0.
- `P_NONWRAP_LOW`: MC is driven to 0.0 V on each of the other three counted edges in every four-edge cycle.
- `P_PERIOD_FOUR`: For a continuing valid clock, marker assertions repeat once per four rising threshold crossings.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `two_bit_counter_marker.va`.
Do not add or omit artifacts.
