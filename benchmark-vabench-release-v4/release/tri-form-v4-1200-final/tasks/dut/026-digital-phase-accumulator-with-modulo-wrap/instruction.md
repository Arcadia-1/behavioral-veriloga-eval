# Digital Phase Accumulator With Modulo Wrap

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `phase_accumulator_timer_wrap_ref.va`: `phase_accumulator_timer_wrap_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_TIMER_INCREMENT`: On every dt timer event, normalized phase advances by phase_step.
- `P_MODULO_WRAP`: The phase state wraps modulo one and never grows unbounded.
- `P_PHASE_RAIL_SCALING`: Phase_out equals wrapped normalized phase scaled by the local VDD-minus-VSS rail span.
- `P_PHASE_DERIVED_CLOCK`: Clk_out is rail-high while normalized phase is below 0.5 and low while phase is at or above 0.5.
- `P_PARAMETERIZED_PERIOD`: Changing dt or phase_step changes the observable phase and clock cadence according to the same update and wrap rules.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `phase_accumulator_timer_wrap_ref.va`.
Do not add or omit artifacts.
