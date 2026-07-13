# Dynamic Comparator Kickback Metric Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dynamic_comparator_kickback_metric.va`: `dynamic_comparator_kickback_metric`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `decision`, `kickback_metric`, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, latch the sign of `vinp - vinn` into `decision`.
- `P_DRIVE_KICKBACK_METRIC_AS_A_VOLTAGE`: Drive `kickback_metric` as a voltage-coded function of the absolute input overdrive.
- `P_SMALL_OVERDRIVE_MUST_PRODUCE_A_LARGER`: Small overdrive must produce a larger kickback metric than large overdrive, up to the public rail limits.
- `P_ASSERT_VALID_AFTER_EACH_COMPLETED_DECISION`: Assert `valid` after each completed decision update.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dynamic_comparator_kickback_metric.va`.
Every supplied `.va` file is editable; do not add or omit files.
