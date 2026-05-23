# Speed Optimization Agent Contract

This directory is the canonical home for vaEVAS speed optimization work.

Keep here:
- Speed experiment plans.
- Compact JSON/Markdown speed reports.
- Speed ablation summaries.
- Diagnostic notes needed to explain speed outliers or invalid runs.

Keep outside this directory:
- Runner source that depends on the shared `runners/` import layout.
- Raw simulator output trees under `../results/`.
- Release-wide schemas, paper tables, and benchmark evidence that are not speed-specific.

Compatibility policy:
- Existing release report paths may remain as symlinks into this directory.
- New speed reports should be written under `speed-optimization/reports/`.
- Do not remove compatibility links unless all scripts/tests that read the old paths have been updated.

Claim policy:
- Paper-facing speed claims must use same-server EVAS/Spectre timing.
- Report only accuracy-gated rows.
- Treat EVAS-only timing reports and failed/rejected repeats as diagnostic evidence, not as claim evidence.
