# Buck Soft-start Ramp Controller

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `buck_soft_start_ramp_controller.va`: `buck_soft_start_ramp_controller`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `soft_ref`, ramp metric, and `done`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, increase `soft_ref` toward `target_ref` by at most `ramp_step`.
- `P_NEVER_ALLOW_SOFT_REF_TO_EXCEED`: Never allow `soft_ref` to exceed `target_ref` or the public rails.
- `P_EXPOSE_THE_REMAINING_RAMP_DISTANCE_ON`: Expose the remaining ramp distance on `ramp_metric`.
- `P_ASSERT_DONE_ONLY_AFTER_SOFT_REF`: Assert `done` only after `soft_ref` reaches the target within `ramp_tol`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `buck_soft_start_ramp_controller.va`.
Do not add or omit artifacts.
