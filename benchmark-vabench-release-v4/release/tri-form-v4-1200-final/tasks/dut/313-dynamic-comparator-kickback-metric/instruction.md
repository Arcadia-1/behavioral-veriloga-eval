# Dynamic Comparator Kickback Metric

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dynamic_comparator_kickback_metric.va`: `dynamic_comparator_kickback_metric`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `decision`, `kickback_metric`, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, latch the sign of `vinp - vinn` into `decision`.
- `P_DRIVE_KICKBACK_METRIC_AS_A_VOLTAGE`: Drive `kickback_metric` as a voltage-coded function of the absolute input overdrive.
- `P_SMALL_OVERDRIVE_MUST_PRODUCE_A_LARGER`: Small overdrive must produce a larger kickback metric than large overdrive, up to the public rail limits.
- `P_ASSERT_VALID_AFTER_EACH_COMPLETED_DECISION`: Assert `valid` after each completed decision update.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dynamic_comparator_kickback_metric.va`.
Do not add or omit artifacts.
