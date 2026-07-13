# CDR Eye Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cdr_eye_monitor_top.va`: `cdr_eye_monitor_top`
- `edge_margin_sampler.va`: `edge_margin_sampler`
- `eye_metric_filter.va`: `eye_metric_filter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear early/late flags, eye metric, lock hint, and `valid`.
- `P_ON_EACH_SAMPLING_CLOCK_EDGE_COMPARE`: On each sampling-clock edge, compare the sampled data level with the previous sample.
- `P_RAISE_EARLY_OR_LATE_ACCORDING_TO`: Raise `early` or `late` according to the sign of the edge-position proxy around the sample instant.
- `P_DRIVE_EYE_METRIC_FROM_RECENT_TRANSITION`: Drive `eye_metric` from recent transition stability and sample margin.
- `P_ASSERT_LOCK_HINT_AFTER_FOUR_CONSECUTIVE`: Assert `lock_hint` after four consecutive samples with eye metric above `eye_min`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cdr_eye_monitor_top.va`, `edge_margin_sampler.va`, `eye_metric_filter.va`.
Do not add or omit artifacts.
