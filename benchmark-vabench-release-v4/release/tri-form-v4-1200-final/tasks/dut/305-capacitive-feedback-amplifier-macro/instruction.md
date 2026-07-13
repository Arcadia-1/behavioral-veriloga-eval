# Capacitive-feedback Amplifier Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `capacitive_feedback_amplifier_macro.va`: `capacitive_feedback_amplifier_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear `sampled_metric`, and clear `settled`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, sample `vin` and decode `gain_1..gain_0` as a programmable capacitor ratio.
- `P_DRIVE_SAMPLED_METRIC_WITH_THE_HELD`: Drive `sampled_metric` with the held input sample.
- `P_MOVE_VOUT_TOWARD_VCM_GAIN_SAMPLE`: Move `vout` toward `vcm + gain * (sample - vcm)` with bounded per-update movement.
- `P_ASSERT_SETTLED_AFTER_THE_OUTPUT_HAS`: Assert `settled` after the output has stayed within `settle_tol` of the target for two enabled updates.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `capacitive_feedback_amplifier_macro.va`.
Do not add or omit artifacts.
