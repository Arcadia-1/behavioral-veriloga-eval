# vaEVAS Speed Optimization

This directory is the canonical workspace for EVAS/Spectre speed optimization experiments.

The goal is to keep the speed story versionable and auditable:
- one place for speed plans and reports;
- old release-report paths kept as compatibility symlinks;
- raw simulator outputs kept out of the curated evidence path.

## Layout

```text
speed-optimization/
  AGENTS.md
  MANIFEST.md
  plans/
    VAEVAS_SPEED_ABLATION_EXPERIMENT_PLAN_2026-05-22.md
  reports/
    same_server_speed_goal_findings_20260522.md
    same_server_speed_goal_summary_final_20260522.{json,md}
    same_server_speed_ablation_goal_summary_20260522.{json,md}
    ...
  raw-results/
    README.md
```

## Current Claim Entry Points

Use these files first when analyzing the current speed conclusion:

- `reports/same_server_speed_goal_findings_20260522.md`
- `reports/same_server_speed_goal_summary_final_20260522.md`
- `reports/same_server_speed_goal_summary_final_20260522.json`
- `reports/same_server_speed_ablation_goal_summary_20260522.md`
- `reports/same_server_speed_ablation_goal_summary_20260522.json`

The current official summary uses clean repeats R1, R2, R4, and R5. R3 is diagnostic only because it had one watchdog false failure.

## Current Result Snapshot

The current accuracy-gated result is:

- `profile_fast_skip_source_error_control`: 1036/1036 PASS across clean repeats.
- Spectre AX / EVAS fast+skip geomean speedup: 6.958x.
- Spectre classic / EVAS fast+skip geomean speedup: 21.63x.
- Spectre AX / EVAS strict geomean speedup: 4.276x.
- Spectre classic / EVAS strict geomean speedup: 13.29x.

These are same-server timing claims. They should not be mixed with older EVAS-only speed reports.

## Compatibility

Files previously under `benchmark-vabench-release-v1/reports/` were moved here when they were speed-specific. The old paths are symlinks so existing scripts, tests, and generated reports can still resolve them.

Future speed reports should use `speed-optimization/reports/` directly. The speed runner defaults have been updated to write there.

## What Not To Commit As Evidence

Do not promote raw simulator output trees directly into this directory. Keep bulky run output under `results/` or on the server, and promote only compact summaries, report JSON, report Markdown, and the command/provenance needed to reproduce them.
