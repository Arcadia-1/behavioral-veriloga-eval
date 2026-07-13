# Track/Hold with Droop and Aperture Metric Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `track_hold_aperture.va`: `track_hold_aperture`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or a low `enable` clears `vhold`, `aperture_metric`, `droop_metric`, and `valid`.
- `P_TRACK_MODE_FOLLOWS_INPUT`: While `track` is high and the DUT is enabled, the held state follows `vin` at the internal update cadence and `valid` remains low.
- `P_FALLING_TRACK_SAMPLE_APERTURE`: A falling `track` edge samples `vin`, asserts `valid`, and reports an aperture metric proportional to the step from the previous tracked value.
- `P_HOLD_MODE_DROOP`: During hold mode, `vhold` droops downward by `droop_per_tick` on each update tick without going below `vss`.
- `P_DROOP_METRIC_ACCUMULATION`: `droop_metric` accumulates total hold-mode droop and clears on a new sample, reset, or disable.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `track_hold_aperture.va`.
Every supplied `.va` file is editable; do not add or omit files.
