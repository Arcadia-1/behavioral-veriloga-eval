# Settling Time Measurement Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `settling_time_measurement_tb.va`: `settling_time_measurement_tb`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_ZERO_STATE`: The settling-response state initializes to 0 V and vout begins from that state.
- `P_FIRST_ORDER_UPDATE`: At each 1 ns update, the response advances by 0.04 times the difference between step and its previous value.
- `P_RESPONSE_CONVERGENCE`: For a constant input step, vout approaches the step value monotonically without overshoot under the public recurrence.
- `P_DONE_TIME_GATE`: Done remains low through 120 ns regardless of the response level.
- `P_DONE_SETTLED_GATE`: After 120 ns, done is high only while the internal settled response is above 0.75 V and otherwise remains low.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `settling_time_measurement_tb.va`.
Every supplied `.va` file is editable; do not add or omit files.
