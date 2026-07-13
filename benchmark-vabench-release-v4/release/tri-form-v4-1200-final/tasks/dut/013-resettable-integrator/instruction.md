# Resettable Integrator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `resettable_integrator.va`: `resettable_integrator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_ZERO`: vout begins at 0 V.
- `P_TIMER_INTEGRATION`: While reset is low, each dt timer event adds gain*vin*dt to the accumulator.
- `P_ACTIVE_HIGH_RESET`: When rst is above vth at a timer event, the accumulator and vout return toward 0 V and later restart from zero.
- `P_ACCUMULATOR_CLAMP`: vout remains in the closed 0 V to vmax range.
- `P_EVENT_HOLD`: The accumulated state changes only on dt timer events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `resettable_integrator.va`.
Do not add or omit artifacts.
