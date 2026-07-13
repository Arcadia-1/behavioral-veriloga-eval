# Ready/Valid Latency Counter 12b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ready_valid_latency_counter_12b.va`: `ready_valid_latency_counter_12b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_REQUEST_START`: While idle, a rising clock crossing that samples valid_i high starts a measurement at count zero and clears done.
- `P_WAIT_CYCLE_COUNT`: While active, each rising clock crossing that samples ready_i low increments the pending latency by one cycle.
- `P_READY_COMPLETION`: While active, a rising clock crossing that samples ready_i high latches the current count to lat[11:0], asserts done, and returns the meter to idle.
- `P_ZERO_LATENCY`: If valid_i and ready_i are both high on the starting clock edge, the reported latency is zero.
- `P_RESULT_HOLD_AND_ORDER`: The completed result holds until a later request starts; lat0 is LSB, lat11 is MSB, and asserted outputs use vdd.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ready_valid_latency_counter_12b.va`.
Do not add or omit artifacts.
