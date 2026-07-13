# Source-follower Buffer Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `source_follower_buffer_macro.va`: `source_follower_buffer_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_OR_LOW_ENABLE_DRIVES_THE`: Reset or low `enable` drives the output and metrics low.
- `P_WHEN_ENABLED_THE_OUTPUT_FOLLOWS_VIN`: When enabled, the output follows `vin - vgs_drop`.
- `P_CLAMP_THE_OUTPUT_BETWEEN_VSS_AND`: Clamp the output between `vss` and `vbias - min_headroom`.
- `P_HEADROOM_METRIC_REPORTS_THE_REMAINING_VBIAS`: `headroom_metric` reports the remaining `vbias - vout` margin clipped to the nominal flag range.
- `P_VALID_IS_HIGH_ONLY_WHEN_ENABLED`: `valid` is high only when enabled, not reset, and the bias rail can support at least the minimum headroom.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `source_follower_buffer_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
