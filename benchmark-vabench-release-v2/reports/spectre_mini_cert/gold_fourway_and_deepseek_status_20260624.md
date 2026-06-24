# vaBench v2 Five-Task Four-Way + DeepSeek Status (2026-06-24)

- Gold four-way status: `PASS` for EVAS2, EVAS Python, Spectre ax, and Spectre reference on all five forms.
- DeepSeek generation status: API call/render succeeded for all five; EVAS scoring passed only one of five.
- Prompt freshness: two DeepSeek prompts match current prompts exactly; three current prompts add a saved-top-level-net rule after the DeepSeek run.

| task | current prompt used by DeepSeek | DeepSeek EVAS score | gold EVAS2 | gold EVAS Python | gold Spectre ax | gold Spectre reference | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `False` | `FAIL_DUT_COMPILE` / `0.0` | `PASS` | `PASS` | `PASS` | `PASS` | - |
| `vbr1_l1_window_comparator_detector:tb` | `False` | `FAIL_SIM_CORRECTNESS` / `0.6667` | `PASS` | `PASS` | `PASS` | `PASS` | - |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `True` | `PASS` / `1.0` | `PASS` | `PASS` | `PASS` | `PASS` | - |
| `vbr1_l1_first_order_lowpass:bugfix` | `True` | `FAIL_SIM_CORRECTNESS` / `0.6667` | `PASS` | `PASS` | `PASS` | `PASS` | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | `False` | `FAIL_TB_COMPILE` / `0.3333` | `PASS` | `PASS` | `PASS` | `PASS` | ax_diag=convergence failure; ref_diag=convergence failure |

Interpretation: the gold/reference assets are currently certified on the four requested evaluator modes. The DeepSeek smoke is not a current-prompt baseline for CT01, CT02, and SUP01 because those prompts were revised after that run.
