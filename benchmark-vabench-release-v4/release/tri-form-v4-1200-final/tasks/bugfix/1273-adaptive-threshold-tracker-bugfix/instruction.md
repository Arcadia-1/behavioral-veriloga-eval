# Adaptive Threshold Tracker Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `adaptive_threshold_tracker.va`: `adaptive_threshold_tracker`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIALIZE_THE_STORED_THRESHOLD_TO_THRESHOLD`: Initialize the stored threshold to `threshold_init`, `threshold_mon` to `threshold_init`, and the other observables to zero. On each rising clock crossing, reset the stored threshold and outputs to those initial values while `rst` is high. Otherwise compare `vin` against the previously stored threshold: drive `trip = vhi` when `V(vin) > old_threshold`, otherwise drive `trip = 0 V`. Drive `margin_metric = vhi * clip01(abs(V(vin) - old_threshold) / margin_fullscale)`.
- `P_WHEN_ADAPT_VTH_UPDATE_THE_STORED`: When `adapt > vth`, update the stored threshold after the comparison using `threshold = clamp(adapt_alpha * old_threshold + (1.0 - adapt_alpha) * V(vin), threshold_min, threshold_max)`. Drive `threshold_mon` with the resulting next-sample threshold. Hold the last observable values between rising clock crossings.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `adaptive_threshold_tracker.va`.
Every supplied `.va` file is editable; do not add or omit files.
