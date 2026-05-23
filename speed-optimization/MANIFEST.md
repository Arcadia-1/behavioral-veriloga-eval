# Speed Optimization Manifest

This manifest classifies speed-related artifacts after consolidation.

## Canonical Source

Speed-specific reports and plans now live under `speed-optimization/`.

Compatibility links remain at the old paths:

- `benchmark-vabench-release-v1/reports/same_server_speed_*`
- `benchmark-vabench-release-v1/reports/evas_speed_*`
- `benchmark-vabench-release-v1/reports/speed_*`
- `docs/VAEVAS_SPEED_ABLATION_EXPERIMENT_PLAN_2026-05-22.md`

## Claimable Current Evidence

Use these for the current paper-facing speed statement:

- `reports/same_server_speed_goal_findings_20260522.md`
- `reports/same_server_speed_goal_summary_final_20260522.json`
- `reports/same_server_speed_goal_summary_final_20260522.md`
- `reports/same_server_speed_goal_summary_all_r1_r5_with_r3_watchdog_20260522.json`
- `reports/same_server_speed_goal_summary_all_r1_r5_with_r3_watchdog_20260522.md`

Clean repeat inputs:

- `reports/same_server_speed_cold_r1_goal_20260522.json`
- `reports/same_server_speed_cold_r1_goal_20260522.md`
- `reports/same_server_speed_repeat_r2_goal_20260522.json`
- `reports/same_server_speed_repeat_r2_goal_20260522.md`
- `reports/same_server_speed_repeat_r4_goal_20260522.json`
- `reports/same_server_speed_repeat_r4_goal_20260522.md`
- `reports/same_server_speed_repeat_r5_goal_20260522.json`
- `reports/same_server_speed_repeat_r5_goal_20260522.md`

## Ablation Evidence

Use these to explain which acceleration mechanism matters:

- `reports/same_server_speed_ablation_full_goal_20260522.json`
- `reports/same_server_speed_ablation_full_goal_20260522.md`
- `reports/same_server_speed_ablation_goal_summary_20260522.json`
- `reports/same_server_speed_ablation_goal_summary_20260522.md`

## Diagnostic Evidence

Use these to explain rejected or special-case runs:

- `reports/same_server_speed_repeat_r3_goal_20260522.json`
- `reports/same_server_speed_repeat_r3_goal_20260522.md`
- `reports/same_server_speed_targeted_deadband_watchdog_fix_20260522.json`
- `reports/same_server_speed_targeted_deadband_watchdog_fix_20260522.md`
- `reports/speed_preflight_fixtures_20260522.md`

## Historical Evidence

These files are useful for audit history but should not drive the current speed claim:

- `reports/same_server_speed_sui_smoke.*`
- `reports/same_server_speed_sui_smoke_classic.*`
- `reports/same_server_speed_sui_limit2_v2.*`
- `reports/same_server_speed_sui_repro_*`
- `reports/evas_speed_experiment_p0_p3*`
- `reports/evas_speed_server_feasibility_20260521.md`
- `reports/speed_debug_artifact.*`
- `reports/speed_remaining_queue.*`
- `reports/speed_remaining_staging_manifest.*`

## Runner Source

The runnable Python source remains in `../runners/` because those files share imports with the broader benchmark harness.

Speed-specific runner defaults now point to `speed-optimization/reports/`:

- `../runners/run_vabench_release_same_server_speed.py`
- `../runners/run_vabench_release_evas_speed_experiment.py`
- `../runners/report_vabench_release_same_server_speed_goal.py`

## Raw Result Policy

Raw simulator output trees remain outside this curated directory. See `raw-results/README.md`.
