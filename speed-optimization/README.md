# vaEVAS Speed Optimization

This directory is the canonical workspace for EVAS/Spectre speed optimization experiments.

The goal is to keep the speed story versionable and auditable:
- one place for speed plans and reports;
- two reader-facing Markdown reports for the current speed claim;
- compact JSON data retained for recomputation and audit;
- raw simulator outputs kept out of the curated evidence path.

## Layout

```text
speed-optimization/
  AGENTS.md
  MANIFEST.md
  rust-kernel/
    README.md
    audits/
    templates/
  plans/
    VAEVAS_SPEED_ABLATION_EXPERIMENT_PLAN_2026-05-22.md
    VAEVAS_SPECTRE_REFERENCE_STANDARD_2026-05-26.md
    VAEVAS_PRECISION_RANKING_EXPERIMENT_PLAN_2026-05-26.md
    VAEVAS_PRECISION_RANKING_EXPERIMENT_TRACKER_2026-05-26.md
  reports/
    evas_speed_experiment_results_and_standard_20260522.md
    evas_speed_result_analysis_20260522.md
    same_server_speed_goal_summary_final_20260522.json
    same_server_speed_ablation_goal_summary_20260522.json
    spectre_ax_classic_self_consistency_clean_repeats_20260522.json
  raw-results/
    README.md
```

## Current Claim Entry Points

Use these files first when analyzing the current speed conclusion:

- `reports/evas_speed_experiment_results_and_standard_20260522.md`
- `reports/evas_speed_result_analysis_20260522.md`

Use these JSON files only when recomputing or auditing the tables:

- `reports/same_server_speed_goal_summary_final_20260522.json`
- `reports/same_server_speed_ablation_goal_summary_20260522.json`
- `reports/spectre_ax_classic_self_consistency_clean_repeats_20260522.json`

The current official summary uses clean repeats R1, R2, R4, and R5. R3 is diagnostic only because it had one watchdog false failure.

Use these files before launching the next precision-ranking experiments:

- `plans/VAEVAS_SPECTRE_REFERENCE_STANDARD_2026-05-26.md`
- `plans/VAEVAS_PRECISION_RANKING_EXPERIMENT_PLAN_2026-05-26.md`
- `plans/VAEVAS_PRECISION_RANKING_EXPERIMENT_TRACKER_2026-05-26.md`

Use this directory before starting or reviewing EVAS indexed/Rust kernel work:

- `rust-kernel/README.md`
- `rust-kernel/audits/000-rust-kernel-design.md`
- `rust-kernel/templates/change-audit-template.md`

## Current Result Snapshot

The current Spectre-equivalence-gated result is:

- `profile_fast_skip_source_error_control`: 1036/1036 PASS across clean repeats.
- Spectre ax-mode / EVAS fast+skip geomean speedup: 6.958x.
- Spectre classic / EVAS fast+skip geomean speedup: 21.63x.
- Spectre ax-mode / EVAS strict geomean speedup: 4.276x.
- Spectre classic / EVAS strict geomean speedup: 13.29x.
- Spectre ax-mode/classic self-consistency: 1036/1036 row pairs pass the current waveform equivalence lens; 0 needs-review and 0 blocked.

These are same-server timing claims. They should not be mixed with older EVAS-only speed reports.

## Compatibility

Files previously under `benchmark-vabench-release-v1/reports/` were moved here when they were speed-specific. Old Markdown compatibility links were removed during consolidation so the current reader-facing surface has exactly two reports. Retained JSON compatibility links may remain only for scripts or audit tooling that need machine-readable data.

Future speed reports should use `speed-optimization/reports/` directly. The speed runner defaults have been updated to write there.

Future EVAS kernel-speed implementation notes should use `speed-optimization/rust-kernel/audits/` with numbered audit documents. These are engineering audit records, not release-wide speed claims by themselves.

## What Not To Commit As Evidence

Do not promote raw simulator output trees directly into this directory. Keep bulky run output under `results/` or on the server, and promote only compact summaries, report JSON, report Markdown, and the command/provenance needed to reproduce them.
