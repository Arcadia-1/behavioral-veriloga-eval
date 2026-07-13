# Soft Hysteretic Limiter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `soft_hysteretic_limiter.va`: `soft_hysteretic_limiter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_NEUTRAL`: Initialization or active reset sets out and metric to 0.45 V and clears the remembered hysteresis offset.
- `P_HYSTERESIS_STATE_UPDATE`: On rising clk crossings, vin above 0.62 V stores +hys_step, vin below 0.38 V stores -hys_step, and vin within the middle band preserves the prior offset.
- `P_GAINED_LIMITER_TRANSFER`: The held output target is 0.45 V plus gain times vin minus 0.45 V plus the remembered hysteresis offset.
- `P_OUTPUT_LIMITS`: Out is clamped to 0.10 V through 0.82 V with finite transition smoothing.
- `P_STATE_METRIC`: Metric equals 0.45 V plus twice the remembered offset, producing 0.61 V and 0.29 V for the default high- and low-memory states.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `soft_hysteretic_limiter.va`.
Do not add or omit artifacts.
