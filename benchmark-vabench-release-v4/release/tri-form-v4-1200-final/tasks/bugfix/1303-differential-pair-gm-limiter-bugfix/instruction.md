# Differential-pair gm Limiter Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `differential_pair_gm_limiter.va`: `differential_pair_gm_limiter`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_WHEN_DISABLED_DRIVE_BOTH_OUTPUTS_TO`: When disabled, drive both outputs to `vcm`, clear `gm_metric`, and clear `limit_flag`.
- `P_WHEN_ENABLED_CONVERT_THE_SAMPLED_DIFFERENTIAL`: When enabled, convert the sampled differential input into equal-and-opposite output deviations around `vcm`.
- `P_SCALE_SMALL_SIGNAL_OUTPUT_SEPARATION_BY`: Scale small-signal output separation by `gm_gain` and compress large differential inputs smoothly at `diff_limit`.
- `P_DRIVE_GM_METRIC_AS_A_VOLTAGE`: Drive `gm_metric` as a voltage-coded estimate of the active transconductance region.
- `P_ASSERT_LIMIT_FLAG_ONLY_WHEN_COMPRESSION`: Assert `limit_flag` only when compression is active.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `differential_pair_gm_limiter.va`.
Every supplied `.va` file is editable; do not add or omit files.
