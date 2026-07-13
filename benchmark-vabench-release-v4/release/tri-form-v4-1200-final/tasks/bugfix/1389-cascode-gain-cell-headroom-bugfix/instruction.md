# Cascode Gain-cell Headroom Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cascode_gain_cell_headroom.va`: `cascode_gain_cell_headroom`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_OR_LOW_ENABLE_DRIVES_VOUT`: Reset or low `enable` drives `vout` to common mode and clears metrics.
- `P_WHEN_ENABLED_COMPUTE_AN_INVERTING_GAIN`: When enabled, compute an inverting gain-cell output around common mode.
- `P_CLAMP_THE_OUTPUT_BETWEEN_VSS_AND`: Clamp the output between `vss` and the available headroom limit.
- `P_GAIN_METRIC_REPORTS_THE_ABSOLUTE_OUTPUT`: `gain_metric` reports the absolute output excursion from common mode.
- `P_HEADROOM_OK_IS_HIGH_ONLY_WHEN`: `headroom_ok` is high only when the available headroom limit remains above common mode.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cascode_gain_cell_headroom.va`.
Every supplied `.va` file is editable; do not add or omit files.
