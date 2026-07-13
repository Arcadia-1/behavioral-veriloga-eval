# Ready/Valid Latency Counter 12b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ready_valid_latency_counter_12b.va`: `ready_valid_latency_counter_12b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_REQUEST_START`: While idle, a rising clock crossing that samples valid_i high starts a measurement at count zero and clears done.
- `P_WAIT_CYCLE_COUNT`: While active, each rising clock crossing that samples ready_i low increments the pending latency by one cycle.
- `P_READY_COMPLETION`: While active, a rising clock crossing that samples ready_i high latches the current count to lat[11:0], asserts done, and returns the meter to idle.
- `P_ZERO_LATENCY`: If valid_i and ready_i are both high on the starting clock edge, the reported latency is zero.
- `P_RESULT_HOLD_AND_ORDER`: The completed result holds until a later request starts; lat0 is LSB, lat11 is MSB, and asserted outputs use vdd.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ready_valid_latency_counter_12b.va`.
Every supplied `.va` file is editable; do not add or omit files.
