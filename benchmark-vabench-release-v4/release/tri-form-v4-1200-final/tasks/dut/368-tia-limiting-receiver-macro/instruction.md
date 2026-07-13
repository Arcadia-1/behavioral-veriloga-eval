# TIA Limiting Receiver Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `tia_limiting_receiver.va`: `tia_limiting_receiver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, drive `vout` to `vcm` and clear `decision`, `limit_flag`, `valid`, and `amp_metric`.
- `P_TREAT_VIN_PROXY_AS_A_VOLTAGE`: Treat `vin_proxy` as a voltage-domain proxy for receiver input magnitude; no current ports are required.
- `P_APPLY_GAIN_TO_THE_DEVIATION_FROM`: Apply gain to the deviation from `vcm` and clamp the output to `vcm +/- limit`.
- `P_ASSERT_LIMIT_FLAG_WHEN_THE_UNCLAMPED`: Assert `limit_flag` when the unclamped amplified signal would exceed the limiter range.
- `P_ON_EACH_RISING_CLK_EDGE_DRIVE`: On each rising `clk` edge, drive `decision` high when the limited output is at or above `vcm`, otherwise low.
- `P_ASSERT_VALID_WHEN_AMP_METRIC_IS`: Assert `valid` when `amp_metric` is at least `valid_min` for two consecutive clock updates.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `tia_limiting_receiver.va`.
Do not add or omit artifacts.
