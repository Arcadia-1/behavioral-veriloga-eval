# vaBench v2 Gold EVAS-Only Cert After Issue #20 Fix

- Date: 2026-06-24
- Issue: https://github.com/Arcadia-1/behavioral-veriloga-eval/issues/20
- Status: `PASS`
- Rows: `5/5` PASS
- EVAS engine: `evas`
- Spectre backend: `none`
- Raw output root: `/private/tmp/issue20_five_evas_only_cert`

Command:

```bash
VAEVAS_EVAS_PERSISTENT_WORKER=0 VAEVAS_DEFAULT_EVAS_ENGINE=evas EVAS_ENGINE=evas \
python3 benchmark-vabench-release-v2/scripts/run_gold_spectre_mini_cert.py \
  --spectre-backend none \
  --evas-engine evas \
  --timeout-s 900 \
  --task-id vbr1_l1_window_comparator_detector:tb \
  --task-id vbr1_l1_aperture_delay_track_and_hold:dut \
  --task-id vbr1_l1_first_order_lowpass:bugfix \
  --task-id vbr1_l2_weighted_sar_adc_dac_loop:e2e \
  --task-id vbr1_l2_gain_extraction_convergence_measurement_flow:e2e \
  --output-root /private/tmp/issue20_five_evas_only_cert
```

| task | status | EVAS | sim_correct | notes |
| --- | --- | --- | --- | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `PASS` | `PASS` | `1.0` | `completed_conversions=124 unique_codes=60 code_range=0..254 sample_span=0.900 vout_span=0.896 avg_quant_err=0.0018 max_quant_err=0.0035 avg_dac_err=0.0032 max_dac_err=0.0565 avg_roundtrip_err=0.0049 monotonic_reversals=0` |
| `vbr1_l1_window_comparator_detector:tb` | `PASS` | `PASS` | `1.0` | `below_hi=0.000 above_hi=0.000 inside_rise_hi=1.000 inside_fall_hi=1.000 span=0.900` |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `PASS` | `PASS` | `1.0` | `aperture_samples=0.350,0.600,0.250,0.700,0.400,0.800,0.800 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=0 span=0.550` |
| `vbr1_l1_first_order_lowpass:bugfix` | `PASS` | `PASS` | `1.0` | `configured_lowpass_samples=0.299,0.618,0.776,0.799 input_step=True monotonic=True response_fast_enough=True not_instant=True bounded=True checker_config_parameters=first_order_lowpass` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | `PASS` | `PASS` | `1.0` | `diff_gain=11.08` |

Root cause of issue #20: the weighted-SAR streaming checker sampled every
post-reset `clks` rising edge as if it were a final ADC conversion. The gold SAR
is a multi-cycle converter: it samples on an idle falling edge and resolves one
bit per following rising edge. Intermediate trial states are intentionally not
final quantized outputs, so the old checker compared partial trial codes against
the final sampled-input/DAC contract and produced large quantization errors and
many monotonic reversals.

Fix: the release SAR checker now uses `conv_done` completed-conversion windows
and `vin_sample` as the sampled-input reference. The numerical thresholds were
not loosened.

Infrastructure fix: `run_gold_spectre_mini_cert.py --spectre-backend none` is
now a clean EVAS-only mode, and `--evas-engine evas` makes Docker Python-EVAS
runs explicit. This cert also sets `VAEVAS_EVAS_PERSISTENT_WORKER=0` to match
issue #20 reproduction and uses `--timeout-s 900` to avoid classifying a slow
Python-EVAS run as a behavior failure.
