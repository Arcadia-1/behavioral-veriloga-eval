# Speed Optimization Manifest

This manifest defines the compact speed-report surface after cleanup.

## Canonical Source

Speed-specific reports and plans now live under `speed-optimization/`.

Only two human-readable reports are retained as current paper-facing speed
entry points:

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

## Rust EVAS2 Engineering Freeze

Use these reports as the current Rust EVAS2 four-way engineering reference.
They supersede ad-hoc smoke results for discussion, but they are not by
themselves final paper-facing same-host speed claims:

- `reports/full_release_fourway_reference_after_cmp_delay_cross_time_fix_20260608.md`
- `reports/full_release_fourway_reference_after_cmp_delay_cross_time_fix_20260608.json`
- `reports/full_release_fourway_freeze_risk_audit_20260608.md`
- `reports/cmp_delay_cross_time_fix_evas2_allforms_20260608_r2.md`
- `reports/cmp_delay_cross_time_fix_evas2_allforms_20260608_r2.json`

## Diagnostic Engineering Reports

These reports explain implementation bottlenecks or local EVAS-only probes.
They are useful for engineering review, but they are not paper-facing speed
claims:

- `rust-kernel/EVAS2_P0P1_CLOSEOUT_20260606.md`
- `rust-kernel/EVAS2_CURRENT_ARTIFACT_INDEX_20260606.md`
- `rust-kernel/audits/114-full-release-rust-py-spectre-fourway.md`
- `rust-kernel/audits/115-auto-row-checker-sparse-trace-contract.md`
- `rust-kernel/audits/116-generic-checker-runtime-hot-rows.md`
- `rust-kernel/audits/117-rustsim-while-body-gate.md`
- `reports/current_release_rust_coverage_manifest_rustsim_gate_20260606.json`
- `reports/current_release_rust_coverage_manifest_rustsim_gate_20260606.md`
- `reports/current_release_rust_coverage_manifest_rustsim_gate_after_while_20260606.md`
- `reports/current_release_rust_coverage_manifest_rustsim_gate_after_while_20260606.json`
- `reports/evas2_while_cppll_smoke_20260606.md`
- `reports/evas2_while_cppll_smoke_20260606.json`
- `reports/full_release_fourway_reference_20260606.md`
- `reports/full_release_fourway_reference_20260606.json`
- `reports/full_release_fourway_rust_py_spectre_summary_20260606.json`
- `reports/full_release_rows_for_fourway_20260606.json`
- `reports/full_release_evas_py_rust_after_fixes_20260606.md`
- `reports/full_release_spectre_ax_strict_20260606.md`
- `reports/full_release_evas2_auto_row_trace_20260606_r4.md`
- `reports/full_release_evas2_auto_row_trace_20260606_r4_summary.json`
- `reports/checker_runtime_116_rowbased_20260606.md`
- `reports/checker_runtime_116_rowbased_20260606.json`
- `reports/checker_runtime_116_streaming_20260606.md`
- `reports/checker_runtime_116_streaming_20260606.json`
- `reports/evas2_p0p1_clean_smoke_20260606.md`
- `reports/evas2_p0p1_clean_smoke_summary_20260606.json`
- `reports/checker_runtime_072_20260604.md`
- `reports/checker_runtime_072_20260604.json`
- `reports/checker_runtime_priority_073_20260604.md`
- `reports/checker_runtime_priority_073_20260604.json`
- `reports/checker_runtime_074_prop_delay_20260604.md`
- `reports/checker_runtime_074_prop_delay_20260604.json`
- `reports/rust_stage55_topwall10_072_20260604.md`
- `reports/rust_stage55_topwall10_072_20260604.json`
- `reports/rust_speed_claim_gate_073_20260604.md`
- `reports/rust_speed_claim_gate_073_20260604.json`
- `reports/rust_stage74_topwall_evas_smoke_20260604.md`
- `reports/rust_stage74_topwall_evas_smoke_20260604.json`
- `reports/rust_gain_measurement_flow_075_20260604.md`
- `reports/rust_gain_measurement_flow_075_20260604.json`
- `reports/rust_stage75_topwall_evas_smoke_20260604.md`
- `reports/rust_stage75_topwall_evas_smoke_20260604.json`
- `reports/rust_stage76_topwall10_current_20260604.md`
- `reports/rust_stage76_topwall10_current_20260604.json`
- `reports/rust_stage77_record_trace_copy_smoke_20260604.md`
- `reports/rust_stage77_record_trace_copy_smoke_20260604.json`
- `reports/rust_stage78_global_timing_split_smoke_20260604.md`
- `reports/rust_stage78_global_timing_split_smoke_20260604.json`
- `reports/rust_stage78_persistent_worker_smoke_20260604.md`
- `reports/rust_stage78_persistent_worker_smoke_20260604.json`
- `reports/rust_stage78_persistent_worker_topwall10_20260604.md`
- `reports/rust_stage78_persistent_worker_topwall10_20260604.json`
- `reports/rust_stage79_required_trace_topwall10_20260604.md`
- `reports/rust_stage79_required_trace_topwall10_20260604.json`
- `reports/rust_stage79_required_trace_disabled_topwall10_20260604.md`
- `reports/rust_stage79_required_trace_disabled_topwall10_20260604.json`

## Rust Kernel Optimization Program

Use this directory for the ongoing EVAS indexed/Rust backend engineering record:

- `rust-kernel/README.md`
- `rust-kernel/audits/000-rust-kernel-design.md`
- `rust-kernel/audits/001-indexed-sidecar-and-rust-smoke.md`
- `rust-kernel/audits/002-python-indexed-ir-parity.md`
- `rust-kernel/audits/003-python-indexed-voltage-snapshot.md`
- `rust-kernel/audits/078-global-evas-timing-split-and-persistent-worker.md`
- `rust-kernel/audits/079-required-signal-global-trace.md`
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
