# Settling Time Measurement

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `settling_time_measurement_tb.va`: `settling_time_measurement_tb`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_ZERO_STATE`: The settling-response state initializes to 0 V and vout begins from that state.
- `P_FIRST_ORDER_UPDATE`: At each 1 ns update, the response advances by 0.04 times the difference between step and its previous value.
- `P_RESPONSE_CONVERGENCE`: For a constant input step, vout approaches the step value monotonically without overshoot under the public recurrence.
- `P_DONE_TIME_GATE`: Done remains low through 120 ns regardless of the response level.
- `P_DONE_SETTLED_GATE`: After 120 ns, done is high only while the internal settled response is above 0.75 V and otherwise remains low.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `settling_time_measurement_tb.va`.
Do not add or omit artifacts.
