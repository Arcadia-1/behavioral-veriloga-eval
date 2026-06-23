# vaBench 300 v1.1 Score Admission Audit

Date: 2026-06-23

This report gates whether the 29 fresh-certified v1.1 rows may enter the
paper score denominator.

## Verdict

- status: `pass`
- verdict: `admit_all`
- audited rows: 29 / 29
- admission-ready rows: 29
- blocked rows: 0
- EVAS PASS / Spectre FAIL rows: 0

## Evidence

- fresh Spectre pass rows: 29
- fresh Spectre parity pass rows: 29
- task-specific negative full-checker fails: 145
- negative audit issues: 0

## Blockers

- none

## Warnings

- `prompt_uses_candidate_wording`: 29

## Row Results

| Entry | Form | Ready | Warnings | Blockers |
| --- | --- | ---: | ---: | ---: |
| vbr11_l1_bootstrapped_sample_switch | bugfix | yes | 1 | 0 |
| vbr11_l1_bootstrapped_sample_switch | dut | yes | 1 | 0 |
| vbr11_l1_bootstrapped_sample_switch | e2e | yes | 1 | 0 |
| vbr11_l1_bootstrapped_sample_switch | tb | yes | 1 | 0 |
| vbr11_l1_sigma_delta_modulator_loop | bugfix | yes | 1 | 0 |
| vbr11_l1_sigma_delta_modulator_loop | dut | yes | 1 | 0 |
| vbr11_l1_sigma_delta_modulator_loop | e2e | yes | 1 | 0 |
| vbr11_l1_sigma_delta_modulator_loop | tb | yes | 1 | 0 |
| vbr11_l2_bandgap_startup_trim_flow | bugfix | yes | 1 | 0 |
| vbr11_l2_bandgap_startup_trim_flow | dut | yes | 1 | 0 |
| vbr11_l2_bandgap_startup_trim_flow | e2e | yes | 1 | 0 |
| vbr11_l2_bandgap_startup_trim_flow | tb | yes | 1 | 0 |
| vbr11_l2_fractional_n_pll_divider_flow | bugfix | yes | 1 | 0 |
| vbr11_l2_fractional_n_pll_divider_flow | dut | yes | 1 | 0 |
| vbr11_l2_fractional_n_pll_divider_flow | e2e | yes | 1 | 0 |
| vbr11_l2_fractional_n_pll_divider_flow | tb | yes | 1 | 0 |
| vbr11_l2_metastability_window_comparator_flow | bugfix | yes | 1 | 0 |
| vbr11_l2_metastability_window_comparator_flow | dut | yes | 1 | 0 |
| vbr11_l2_metastability_window_comparator_flow | e2e | yes | 1 | 0 |
| vbr11_l2_metastability_window_comparator_flow | tb | yes | 1 | 0 |
| vbr11_l2_quadrature_iq_imbalance_corrector | bugfix | yes | 1 | 0 |
| vbr11_l2_quadrature_iq_imbalance_corrector | dut | yes | 1 | 0 |
| vbr11_l2_quadrature_iq_imbalance_corrector | e2e | yes | 1 | 0 |
| vbr11_l2_quadrature_iq_imbalance_corrector | tb | yes | 1 | 0 |
| vbr11_l2_time_interleaved_adc_mismatch_flow | bugfix | yes | 1 | 0 |
| vbr11_l2_time_interleaved_adc_mismatch_flow | dut | yes | 1 | 0 |
| vbr11_l2_time_interleaved_adc_mismatch_flow | e2e | yes | 1 | 0 |
| vbr11_l2_time_interleaved_adc_mismatch_flow | tb | yes | 1 | 0 |
| vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow | bugfix | yes | 1 | 0 |

## Claim Boundary

- This report only admits fresh-certified v1.1 rows to the score denominator; support-suite exclusions still apply globally.
- Spectre remains the final paper-facing judge; EVAS evidence is a fast evaluator and checker-strength signal.
- Warnings flag wording hygiene or non-blocking prompt text; blockers prevent admission.
