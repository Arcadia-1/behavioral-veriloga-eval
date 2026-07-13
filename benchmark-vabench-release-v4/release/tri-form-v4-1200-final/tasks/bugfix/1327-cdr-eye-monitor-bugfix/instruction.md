# CDR Eye Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cdr_eye_monitor_top.va`: `cdr_eye_monitor_top`
- `edge_margin_sampler.va`: `edge_margin_sampler`
- `eye_metric_filter.va`: `eye_metric_filter`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear early/late flags, eye metric, lock hint, and `valid`.
- `P_ON_EACH_SAMPLING_CLOCK_EDGE_COMPARE`: On each sampling-clock edge, compare the sampled data level with the previous sample.
- `P_RAISE_EARLY_OR_LATE_ACCORDING_TO`: Raise `early` or `late` according to the sign of the edge-position proxy around the sample instant.
- `P_DRIVE_EYE_METRIC_FROM_RECENT_TRANSITION`: Drive `eye_metric` from recent transition stability and sample margin.
- `P_ASSERT_LOCK_HINT_AFTER_FOUR_CONSECUTIVE`: Assert `lock_hint` after four consecutive samples with eye metric above `eye_min`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cdr_eye_monitor_top.va`, `edge_margin_sampler.va`, `eye_metric_filter.va`.
Every supplied `.va` file is editable; do not add or omit files.
