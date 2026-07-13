# Differential-pair gm Limiter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `differential_pair_gm_limiter.va`: `differential_pair_gm_limiter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_WHEN_DISABLED_DRIVE_BOTH_OUTPUTS_TO`: When disabled, drive both outputs to `vcm`, clear `gm_metric`, and clear `limit_flag`.
- `P_WHEN_ENABLED_CONVERT_THE_SAMPLED_DIFFERENTIAL`: When enabled, convert the sampled differential input into equal-and-opposite output deviations around `vcm`.
- `P_SCALE_SMALL_SIGNAL_OUTPUT_SEPARATION_BY`: Scale small-signal output separation by `gm_gain` and compress large differential inputs smoothly at `diff_limit`.
- `P_DRIVE_GM_METRIC_AS_A_VOLTAGE`: Drive `gm_metric` as a voltage-coded estimate of the active transconductance region.
- `P_ASSERT_LIMIT_FLAG_ONLY_WHEN_COMPRESSION`: Assert `limit_flag` only when compression is active.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `differential_pair_gm_limiter.va`.
Do not add or omit artifacts.
