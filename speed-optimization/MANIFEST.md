# Speed Optimization Manifest

This manifest defines the compact speed-report surface after cleanup.

## Canonical Source

Speed-specific reports and plans now live under `speed-optimization/`.

Only two human-readable speed reports are retained:

- `reports/evas_speed_experiment_results_and_standard_20260522.md`
- `reports/evas_speed_result_analysis_20260522.md`

Compatibility links at the old release-report paths are limited to retained
machine-readable JSON data. Old split Markdown links were removed to keep a
single reader-facing report surface.

## Claimable Current Evidence

Use these two Markdown files for the current paper-facing speed statement:

- `reports/evas_speed_experiment_results_and_standard_20260522.md`
- `reports/evas_speed_result_analysis_20260522.md`

Use these JSON files for recomputation and audit:

- `reports/same_server_speed_goal_summary_final_20260522.json`
- `reports/spectre_ax_classic_self_consistency_clean_repeats_20260522.json`

## Next Precision-Ranking Plan

Use these before claiming that EVAS fast is more accurate or more
reference-consistent than the Spectre high-performance preset baseline:

- `plans/VAEVAS_SPECTRE_REFERENCE_STANDARD_2026-05-26.md`
- `plans/VAEVAS_PRECISION_RANKING_EXPERIMENT_PLAN_2026-05-26.md`
- `plans/VAEVAS_PRECISION_RANKING_EXPERIMENT_TRACKER_2026-05-26.md`

## Ablation Evidence

Use this JSON to explain which acceleration mechanism matters:

- `reports/same_server_speed_ablation_goal_summary_20260522.json`

## Rust Kernel Optimization Program

Use this directory for the ongoing EVAS indexed/Rust backend engineering record:

- `rust-kernel/README.md`
- `rust-kernel/audits/000-rust-kernel-design.md`
- `rust-kernel/audits/001-indexed-sidecar-and-rust-smoke.md`
- `rust-kernel/templates/change-audit-template.md`

These documents explain implementation principles, before/after evidence,
learning notes, risks, and rollback points for each kernel-speed change. They
do not replace same-server, Spectre-equivalence-gated speed reports.

## Deleted During Cleanup

The following classes were removed from `speed-optimization/reports/` to keep the
paper-facing surface small: per-repeat inputs, R3/watchdog diagnostic summaries,
historical SUI smoke/repro reports, old EVAS-only speed reports, raw ablation
full reports, speed debug artifacts, remaining-queue manifests, and compatibility
symlinks that would otherwise point to deleted files. The previous split
Markdown reports for main speed summary, ablation summary, Spectre ax-mode/classic
self-consistency, and findings analysis were consolidated into the two retained
Markdown reports above.

Regenerate these from the benchmark runner or remote raw result roots if audit
history is needed later; do not cite them as current paper evidence.

## Runner Source

The runnable Python source remains in `../runners/` because those files share imports with the broader benchmark harness.

Speed-specific runner defaults now point to `speed-optimization/reports/`:

- `../runners/run_vabench_release_same_server_speed.py`
- `../runners/run_vabench_release_evas_speed_experiment.py`
- `../runners/report_vabench_release_same_server_speed_goal.py`
- `../runners/report_spectre_mode_self_consistency.py`

## Raw Result Policy

Raw simulator output trees remain outside this curated directory. See `raw-results/README.md`.
