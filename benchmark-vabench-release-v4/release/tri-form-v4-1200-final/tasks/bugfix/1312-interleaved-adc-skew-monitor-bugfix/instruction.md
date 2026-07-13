# Interleaved ADC Timing-skew Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `interleaved_adc_skew_monitor_top.va`: `interleaved_adc_skew_monitor_top`
- `sample_pair_latch.va`: `sample_pair_latch`
- `skew_metric_core.va`: `skew_metric_core`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear both sample states and all metrics.
- `P_CAPTURE_VIN_A_ON_RISING_CLK`: Capture `vin_a` on rising `clk_a` and `vin_b` on rising `clk_b`.
- `P_ESTIMATE_A_SKEW_PROXY_FROM_THE`: Estimate a skew proxy from the signed difference between the two most recent samples.
- `P_DRIVE_SKEW_METRIC_WITH_THE_ABSOLUTE`: Drive `skew_metric` with the absolute skew proxy and `magnitude_metric` with the average sample magnitude.
- `P_ASSERT_ALARM_WHEN_SKEW_METRIC_EXCEEDS`: Assert `alarm` when `skew_metric` exceeds `skew_limit` for two consecutive comparisons.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `interleaved_adc_skew_monitor_top.va`, `sample_pair_latch.va`, `skew_metric_core.va`.
Every supplied `.va` file is editable; do not add or omit files.
