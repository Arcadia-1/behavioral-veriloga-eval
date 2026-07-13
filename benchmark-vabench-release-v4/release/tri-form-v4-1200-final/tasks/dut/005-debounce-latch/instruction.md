# Debounce Latch

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `debounce_latch.va`: `debounce_latch`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ACTIVE_LOW_RESET`: out is low and pending qualification is cancelled whenever rst_n is below vth.
- `P_RISE_QUALIFICATION`: A sig rising edge sets out high only after sig and rst_n remain high for stable seconds.
- `P_FALL_CLEAR`: A sig falling edge clears out and cancels pending qualification.
- `P_EVENT_HOLD`: out holds between reset, sig-edge, and qualification-timer events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `debounce_latch.va`.
Do not add or omit artifacts.
