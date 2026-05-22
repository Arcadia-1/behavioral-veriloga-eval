# Cleanup Manifest 2026-05-15

## Purpose

Clean the repository around the current paper-facing mainline:

- vaBench is a clean behavioral Verilog-A benchmark release package.
- EVAS is the fast Spectre-aligned evaluator.
- Historical workflow/controller/SFT/repair-loop artifacts are internal
  construction material, not the contribution.

## Keep

- Current plan/spec/policy documents:
  - `docs/VAEVAS_MAINLINE_PLAN.md`
  - `docs/VABENCH_TOPDOWN_FUNCTION_TAXONOMY.md`
  - `docs/VABENCH_D004_BUGFIX_TRIAGE.md`
  - `docs/VABENCH_P2_TOLERANCE_POLICY.md`
  - `docs/VABENCH_MAIN120_MATERIALIZATION.md`
  - `docs/VABENCH_MAIN120_MATERIALIZATION.csv`
  - `docs/VAEVAS_VALIDATION_PIPELINE.md`
  - `docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md`
  - `docs/EXPERIMENT_ASSET_POLICY.md`
  - `docs/TASK_AUTHORING_CHECKLIST.md`
- Source benchmark tasks, gold files, runners, tests, and EVAS source.
- Retained result evidence referenced by active policy documents:
  - `results/vabench-main-v1-main120-gold-evas-2026-05-08`
  - `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08`
  - `results/d004-*`
  - `results/main120-D-spliced-parityfix-vs-spectre-20260508`
  - root-level `main120-D-rulesonly-*-evas-spectre.json` parity summaries.

## Remove

The cleanup removes documents that were temporary review sheets, old workflow
plans, stale 92-task/main120 source-recovery narratives, or controller/repair
experiment material superseded by the current mainline.

The cleanup also removes local raw `results/` directories and root result files
for bpack drafts, old prompt/controller/model sweeps, draft vaBench iterations,
and temporary smoke outputs that are not cited by the active mainline docs.

## Recovery

Tracked deletions remain recoverable from git history. Ignored local `results/`
artifacts are intentionally disposable under `docs/EXPERIMENT_ASSET_POLICY.md`;
only the retained evidence listed above should be used for current claims.
