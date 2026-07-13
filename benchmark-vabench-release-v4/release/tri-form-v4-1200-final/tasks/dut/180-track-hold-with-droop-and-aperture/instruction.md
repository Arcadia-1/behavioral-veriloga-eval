# Track/Hold with Droop and Aperture Metric

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `track_hold_aperture.va`: `track_hold_aperture`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or a low `enable` clears `vhold`, `aperture_metric`, `droop_metric`, and `valid`.
- `P_TRACK_MODE_FOLLOWS_INPUT`: While `track` is high and the DUT is enabled, the held state follows `vin` at the internal update cadence and `valid` remains low.
- `P_FALLING_TRACK_SAMPLE_APERTURE`: A falling `track` edge samples `vin`, asserts `valid`, and reports an aperture metric proportional to the step from the previous tracked value.
- `P_HOLD_MODE_DROOP`: During hold mode, `vhold` droops downward by `droop_per_tick` on each update tick without going below `vss`.
- `P_DROOP_METRIC_ACCUMULATION`: `droop_metric` accumulates total hold-mode droop and clears on a new sample, reset, or disable.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `track_hold_aperture.va`.
Do not add or omit artifacts.
