# CT04 Non-Core Archive

Date: 2026-05-23

This archive preserves three CT04 entries removed from the paper-facing
`tasks/CT04_analog_behavioral_signal_conditioning` surface after content
audit. The retained CT04 core is:

- `vbr1_l1_voltage_gain_amplifier`
- `vbr1_l1_first_order_lowpass`
- `vbr1_l1_higher_order_filter`
- `vbr1_l1_soft_hysteretic_limiter`
- `vbr1_l1_slew_rate_limiter`
- `vbr1_l1_resettable_integrator`
- `vbr1_l2_amplifier_filter_chain`

Archived entries:

| Entry | Reason |
| --- | --- |
| `vbr1_l1_voltage_clamp_or_limiter` | Hard clamp overlaps with gain rail clamp and soft/hysteretic limiter. |
| `vbr1_l1_precision_rectifier` | Narrow piecewise sign transform; weak fit for the CT04 core claim. |
| `vbr1_l1_differential_output_driver` | More like output/interface formatting than core signal conditioning. |

The archived task assets, EVAS/Spectre evidence, and dated reports that still
referenced these entries are intentionally kept outside active `tasks/`,
`evidence/`, and `reports/` so release manifests and score denominators only
see the seven retained CT04 core entries.

Additional archive folders:

| Folder | Purpose |
| --- | --- |
| `restored_dual_after_import_repair/` | Duplicate CT04 dual evidence restored while repairing a stale import, moved back out of the active evidence surface. |
| `historical_reports_with_removed_entries/` | Dated reports from 2026-05-22 that still mention removed CT04 entries and are no longer current release evidence. |
