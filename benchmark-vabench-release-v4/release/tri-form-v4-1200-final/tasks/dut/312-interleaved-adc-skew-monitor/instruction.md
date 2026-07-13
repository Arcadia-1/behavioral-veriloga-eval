# Interleaved ADC Timing-skew Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `interleaved_adc_skew_monitor_top.va`: `interleaved_adc_skew_monitor_top`
- `sample_pair_latch.va`: `sample_pair_latch`
- `skew_metric_core.va`: `skew_metric_core`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear both sample states and all metrics.
- `P_CAPTURE_VIN_A_ON_RISING_CLK`: Capture `vin_a` on rising `clk_a` and `vin_b` on rising `clk_b`.
- `P_ESTIMATE_A_SKEW_PROXY_FROM_THE`: Estimate a skew proxy from the signed difference between the two most recent samples.
- `P_DRIVE_SKEW_METRIC_WITH_THE_ABSOLUTE`: Drive `skew_metric` with the absolute skew proxy and `magnitude_metric` with the average sample magnitude.
- `P_ASSERT_ALARM_WHEN_SKEW_METRIC_EXCEEDS`: Assert `alarm` when `skew_metric` exceeds `skew_limit` for two consecutive comparisons.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `interleaved_adc_skew_monitor_top.va`, `sample_pair_latch.va`, `skew_metric_core.va`.
Do not add or omit artifacts.
