# vaBench Checker and EVAS/Spectre Evidence Workplan

Date: 2026-05-22

## Summary

| Metric | Value |
| --- | ---: |
| prompt version | `public-contract-v2` |
| prompt manifest status | `pass` |
| L2 e2e rows | 15 |
| EVAS PASS / Spectre FAIL | 0 |
| targeted L2 tightening status | `pass` |
| targeted L2 tightening pass/fail | 2 / 0 |
| speed claim allowed | `False` |

## Work Items

| ID | Priority | Status | Work | Stop Condition |
| --- | --- | --- | --- | --- |
| `W1_prompt_version_traceability` | `P0` | `done` | Treat public-contract-v2 as the prompt source of truth and mark old baselines historical. | prompt_contract_manifest status=pass and every row baseline_compatibility=requires_rerun |
| `W2_l2_checker_strength_audit` | `P0` | `ready_for_claim_mapping` | Audit L2 e2e checkers for composition/measurement-flow strength instead of structural-only pass conditions. | Every L2 e2e row has a checker claim mapped to a public composition behavior or is explicitly downgraded. |
| `W3_evas_spectre_parity_evidence` | `P0` | `done` | Keep historical full-release dual certification separate from targeted reruns for checker-tightened rows; preserve zero EVAS PASS / Spectre FAIL. | dual_certification status=pass, targeted_l2_checker_tightening status=pass, and EVAS PASS / Spectre FAIL=0 in both evidence sources. |
| `W4_speed_evidence_positioning` | `P1` | `blocked_for_speed_claim` | Do not claim aggregate EVAS speedup until the speed artifact allows it; stratify or fix slow EVAS outliers, or narrow the claim. | speed_debug_artifact claim_allowed=true, or paper wording uses a narrower measured-subset/no-speedup-safe statement. |
| `W5_public_contract_v2_baseline_rerun` | `P2` | `pending` | Rerun minimal prompt-only baselines on public-contract-v2 after checker-strength decisions are frozen. | Baseline artifact is regenerated against prompt_version_id=public-contract-v2. |

## L2 E2E Checker Strength

| Entry | Category | Checks | Strength | Action |
| --- | --- | ---: | --- | --- |
| `vbr1_l2_adc_dac_reconstruction_chain` | Data Converters | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_adc_dac_source_sweep_flow` | Stimulus and Sources | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | PLL / Clock / Event Timing | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_amplifier_filter_chain` | Analog Behavioral Signal Conditioning | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_comparator_measurement_flow` | Comparators and Decision Circuits | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_complete_calibration_loop` | Calibration, DEM, and Control | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_converter_front_end` | Sample, Hold, and Analog Memory | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | PLL / Clock / Event Timing | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_event_controller` | Digital and Event-Driven Logic | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_flash_adc_mini_array` | Data Converters | 2 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | Measurement and Testbench Instrumentation | 2 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_measurement_flow` | Measurement and Testbench Instrumentation | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_pll_timing_slice` | PLL / Clock / Event Timing | 2 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_serializer_frame_alignment_flow` | Digital and Event-Driven Logic | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
| `vbr1_l2_weighted_sar_adc_dac_loop` | Data Converters | 3 | `multi_behavior_check` | `confirm_checker_maps_to_composition_claim` |
