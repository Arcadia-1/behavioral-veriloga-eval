# Adaptive Threshold Tracker

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `adaptive_threshold_tracker.va`: `adaptive_threshold_tracker`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIALIZE_THE_STORED_THRESHOLD_TO_THRESHOLD`: Initialize the stored threshold to `threshold_init`, `threshold_mon` to `threshold_init`, and the other observables to zero. On each rising clock crossing, reset the stored threshold and outputs to those initial values while `rst` is high. Otherwise compare `vin` against the previously stored threshold: drive `trip = vhi` when `V(vin) > old_threshold`, otherwise drive `trip = 0 V`. Drive `margin_metric = vhi * clip01(abs(V(vin) - old_threshold) / margin_fullscale)`.
- `P_WHEN_ADAPT_VTH_UPDATE_THE_STORED`: When `adapt > vth`, update the stored threshold after the comparison using `threshold = clamp(adapt_alpha * old_threshold + (1.0 - adapt_alpha) * V(vin), threshold_min, threshold_max)`. Drive `threshold_mon` with the resulting next-sample threshold. Hold the last observable values between rising clock crossings.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `adaptive_threshold_tracker.va`.
Do not add or omit artifacts.
