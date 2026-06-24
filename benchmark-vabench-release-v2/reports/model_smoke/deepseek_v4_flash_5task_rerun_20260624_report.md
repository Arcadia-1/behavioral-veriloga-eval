# DeepSeek v4 Flash 5-Task v2 Rerun — EVAS/Checker Report

Date: 2026-06-24

Scope: rerun `deepseek-v4-flash` on the current five vaBench release-v2 pilot prompts without changing the prompt files, then materialize generated artifacts and score them with the current EVAS/checker path.

## Inputs

- Generation summary: `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624/summary.json`
- Scoring summary: `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624_scored/summary.json`
- Generation output root: `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624/`
- Materialized candidate root: `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624_scored/`
- Model: `deepseek-v4-flash`; thinking: `disabled`; max tokens: `8192`; selected tasks: `5`

## Summary

- Generation status: `PASS` (`5/5` responses received).
- EVAS/checker pass rate: `1/5`.
- Status counts: `{'FAIL_DUT_COMPILE': 1, 'FAIL_SIM_CORRECTNESS': 2, 'PASS': 1, 'FAIL_TB_COMPILE': 1}`.

| Task | Status | Weighted | Candidate Dir | Primary Observation |
| --- | --- | ---: | --- | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `FAIL_DUT_COMPILE` | `0.0` | `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624_scored/vbr1_l2_weighted_sar_adc_dac_loop__e2e/candidate` | Generated TB introduces Spectre subckt/VCVS glue and duplicate instances; EVAS rejects the netlist as transistor-level/non-behavioral before simulation. |
| `vbr1_l1_window_comparator_detector:tb` | `FAIL_SIM_CORRECTNESS` | `0.6667` | `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624_scored/vbr1_l1_window_comparator_detector__tb/candidate` | TB compiles and runs, but saves vin/out while using net_vin/net_out internally; recorded vin/out are flat 0, so checker reports out_span_too_small=0.000. |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `PASS` | `1.0` | `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624_scored/vbr1_l1_aperture_delay_track_and_hold__dut/candidate` | Candidate DUT passes EVAS/checker; delayed aperture samples exactly match expected public sequence. |
| `vbr1_l1_first_order_lowpass:bugfix` | `FAIL_SIM_CORRECTNESS` | `0.6667` | `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624_scored/vbr1_l1_first_order_lowpass__bugfix/candidate` | Candidate compiles/runs but implements a 10 ns discrete timer low-pass; checker sees monotonic bounded behavior but response_fast_enough=False. |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | `FAIL_TB_COMPILE` | `0.3333` | `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624_scored/vbr1_l2_gain_extraction_convergence_measurement_flow__e2e/candidate` | Candidate extraction succeeds, but vin_src.va and lfsr.va contain procedural local declarations inside analog/event blocks; EVAS rejects with Spectre-compatible syntax errors. |

## Immediate Interpretation

- The CT03 DUT prompt remains usable: one-shot DeepSeek generated a checker-passing track-and-hold DUT.
- The CT04 low-pass candidate now simulates, but it did not use `laplace_nd()`; it failed behavior because the discrete timer implementation is too slow for the configured checker window.
- CT02 no longer exposes the earlier multiline-PWL syntax issue in this rerun; instead it exposes a public-spec/agent failure mode around saved signal names versus internal net names.
- CT01 and SUP01 failures are candidate-side structural/syntax failures under EVAS. CT01 should still be Spectre-probed if we want to separate EVAS subset rejection from Spectre legality for `subckt`/controlled-source glue, but the candidate is not a clean behavioral benchmark solution.

## Next Actions

1. Run Spectre on CT03 and CT04 candidates first: CT03 is the only EVAS PASS; CT04 compiles/runs and is useful for behavior mismatch confirmation.
2. Spectre-probe CT02 if we want to confirm that the TB is syntactically valid but semantically wrong due to saved/connected node mismatch.
3. Treat CT01/SUP01 as prompt/spec stress evidence; do not count them as model success. Use the materialized candidate files for failure taxonomy and prompt audit.
