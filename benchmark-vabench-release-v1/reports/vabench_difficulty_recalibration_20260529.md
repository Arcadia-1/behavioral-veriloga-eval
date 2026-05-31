# vaBench Difficulty Recalibration

Date: 2026-05-29

## Policy

- Basis: Difficulty is calibrated from benchmark-facing circuit/form complexity, not from one model's pass rate.
- D1: single-block threshold, first-order, or simple bounded voltage behavior
- D2: standard L1 analog/mixed-signal macromodel with state, hysteresis, settling, or moderate nonlinearity
- D3: L2 composition/flow rows or advanced nonlinear approximation rows that require multiple public behavior constraints

## Counts

| Metric | Before | After |
| --- | --- | --- |
| entry difficulty counts | `{'D1': 10, 'D2': 49, 'D3': 20}` | `{'D1': 10, 'D2': 49, 'D3': 20}` |
| form difficulty counts | `{'D1': 39, 'D2': 186, 'D3': 46}` | `{'D1': 39, 'D2': 186, 'D3': 46}` |

## Changed Entries

| Entry | Old | New | Rationale |
| --- | --- | --- | --- |

## Calibrated Override Entries

| Entry | Difficulty | Rationale |
| --- | --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac` | `D1` | Preserved as D1 from prior release calibration: a single reusable primitive with a direct public input/output relation. |
| `vbr1_l1_pipeline_adc_stage` | `D3` | Preserved as D3 from prior release calibration because the L1 row still requires residue/decision/stage behavior rather than one direct scalar transform. |
| `vbr1_l1_thermometer_code_decoder` | `D1` | Preserved as D1 from prior release calibration: a single reusable primitive with a direct public input/output relation. |
| `vbr1_l1_unit_element_thermometer_dac` | `D1` | Preserved as D1 from prior release calibration: a single reusable primitive with a direct public input/output relation. |
| `vbr1_l1_offset_comparator` | `D1` | Default calibrated difficulty from release level and entry override policy. |
| `vbr1_l1_threshold_comparator` | `D1` | Default calibrated difficulty from release level and entry override policy. |
| `vbr1_l1_first_order_lowpass` | `D1` | Default calibrated difficulty from release level and entry override policy. |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `D1` | Reclassified as D1 because the public task is a single-block bounded voltage behavior with one dominant decision or limiting relation. |
| `vbr1_l1_uvlo_brownout_detector` | `D1` | Reclassified as D1 because the public task is a single-block bounded voltage behavior with one dominant decision or limiting relation. |
| `vbr1_l1_limiting_amplifier_frontend` | `D1` | Reclassified as D1 because the public task is a single-block bounded voltage behavior with one dominant decision or limiting relation. |
| `vbr1_l1_log_rssi_power_detector` | `D3` | Reclassified as D3 because the task requires a nonlinear compressed approximation and multiple public behavior constraints under the supported Verilog-A subset. |
| `vbr1_l1_pa_compression_macro` | `D3` | Reclassified as D3 because the task requires a nonlinear compressed approximation and multiple public behavior constraints under the supported Verilog-A subset. |
| `vbr1_l1_sine_periodic_voltage_source` | `D1` | Preserved as D1 from prior release calibration: a single reusable primitive with a direct public input/output relation. |
