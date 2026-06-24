# vaBench Release v2 Package Manifest

Date: 2026-06-24

This manifest indexes migrated v2 task forms. It is package metadata,
not fresh EVAS/Spectre certification evidence.

## Summary

| Metric | Value |
| --- | ---: |
| entries | `5` |
| forms | `5` |
| prompt-boundary pass forms | `5` |
| spec-checker map forms | `5` |
| public/private requirement links | `10` |
| score candidate forms | `4` |
| final score-enabled forms | `0` |
| fresh dual-certification pending forms | `5` |

## Claim Boundary

- v2 score claims remain disabled until fresh v2 EVAS/Spectre certification is available.
- Agent prompts must be rendered from `agent_visible_files.json`, not from private evaluator files.
- `task_release_card.json`, `private/*`, and gold assets must never be agent-visible.

## Forms

| Task | Form | Prompt Boundary | Score Enabled | Fresh Dual Pending |
| --- | --- | --- | --- | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `end-to-end` | `pass` | `False` | `True` |
| `vbr1_l1_window_comparator_detector:tb` | `tb-generation` | `pass` | `False` | `True` |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `spec-to-va` | `pass` | `False` | `True` |
| `vbr1_l1_first_order_lowpass:bugfix` | `bugfix` | `pass` | `False` | `True` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | `end-to-end` | `pass` | `False` | `True` |
