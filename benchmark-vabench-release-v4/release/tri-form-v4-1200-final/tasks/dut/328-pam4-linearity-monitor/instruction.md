# PAM4 Linearity Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pam4_linearity_monitor.va`: `pam4_linearity_monitor`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear output, metric, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode `symbol_1..symbol_0` as one of four PAM4 levels.
- `P_DRIVE_LEVEL_OUT_TO_EVENLY_SPACED`: Drive `level_out` to evenly spaced voltage levels between `vss` and `vdd`.
- `P_EXPOSE_A_LINEARITY_METRIC_THAT_IS`: Expose a `linearity_metric` that is high only when adjacent level spacing is uniform.
- `P_ASSERT_VALID_AFTER_EACH_SAMPLED_SYMBOL`: Assert `valid` after each sampled symbol update.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pam4_linearity_monitor.va`.
Do not add or omit artifacts.
