# Slew Rate Limiter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `slew_rate_limiter.va`: `slew_rate_limiter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_ZERO`: vout begins at 0 V.
- `P_PERIODIC_UPDATE`: The state changes only on the public 1 ns periodic update schedule.
- `P_BIDIRECTIONAL_STEP_LIMIT`: Each rising or falling update changes the state toward vin by no more than step.
- `P_NEAR_TARGET_SETTLE`: When vin is within one step, vout may settle directly to vin.
- `P_EVENTUAL_TRACKING`: The limited response eventually reaches sustained high and low input levels while remaining non-instantaneous.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `slew_rate_limiter.va`.
Do not add or omit artifacts.
