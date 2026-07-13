# Sample And Hold With Droop Leakage

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `leaky_hold.va`: `leaky_hold`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SAMPLE_CAPTURE`: Each rising sample crossing while reset is inactive captures the instantaneous vin voltage into the held state.
- `P_HOLD_BETWEEN_EVENTS`: Between sample and leakage events, vout reflects the retained held state rather than continuously tracking vin.
- `P_PERIODIC_DROOP`: At every leak_period update while reset is inactive, the held value is multiplied by decay.
- `P_RESET_CLEAR`: Active reset clears the held state to 0 V at sampling or leakage update events.
- `P_SMOOTH_OUTPUT`: Vout approaches each held-state target with the finite transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `leaky_hold.va`.
Do not add or omit artifacts.
