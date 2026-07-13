# Source-follower Buffer Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `source_follower_buffer_macro.va`: `source_follower_buffer_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_OR_LOW_ENABLE_DRIVES_THE`: Reset or low `enable` drives the output and metrics low.
- `P_WHEN_ENABLED_THE_OUTPUT_FOLLOWS_VIN`: When enabled, the output follows `vin - vgs_drop`.
- `P_CLAMP_THE_OUTPUT_BETWEEN_VSS_AND`: Clamp the output between `vss` and `vbias - min_headroom`.
- `P_HEADROOM_METRIC_REPORTS_THE_REMAINING_VBIAS`: `headroom_metric` reports the remaining `vbias - vout` margin clipped to the nominal flag range.
- `P_VALID_IS_HIGH_ONLY_WHEN_ENABLED`: `valid` is high only when enabled, not reset, and the bias rail can support at least the minimum headroom.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `source_follower_buffer_macro.va`.
Do not add or omit artifacts.
