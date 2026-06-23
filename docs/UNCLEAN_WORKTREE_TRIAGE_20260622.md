# Unclean Worktree Triage, 2026-06-22

This note groups the current `behavioral-veriloga-eval` dirty worktree into commit-safe buckets.
It is a triage artifact only: it does not certify that any generated report is current, paper-facing, or safe to commit.

## Snapshot

- Repository branch: `codex/main120-normal-source-materialization`
- Local state: branch is ahead of origin by 1 commit before this triage note
- `git status --porcelain=v1`: 560 visible entries because untracked directories are collapsed
- `git status --porcelain=v1 -uall`: 7,772 expanded file entries
- Main risk: most dirty entries are generated rerun/speed artifacts, not source changes

## Triage Rules

- Do not commit generated rerun staging directories wholesale.
- Do not commit raw simulator outputs or historical speed sweeps unless promoted to a named fixture/report.
- Keep paper-facing benchmark release reports consistent with their generator scripts and tests.
- Treat modified `evidence/dual` files as high-risk until EVAS/Spectre version, row slice, and rerun provenance are pinned.
- Keep training/SFT/GRPO artifacts out of this repository line unless that scope is explicitly reopened.

## Groups

| Group | Expanded Count | Status | Action |
| --- | ---: | --- | --- |
| Release rerun staging dirs | 5,229 | untracked | Do not commit wholesale; archive or delete after preserving a manifest if needed. |
| vaBench-300 expansion package | 1,988 | untracked | Separate branch/data package candidate; do not mix into release-v1 cleanup. |
| Speed optimization reports | 357 | untracked | Mostly historical/generated; promote only selected summary reports after claim gating. |
| Release dual evidence | 62 | modified | High-risk paper-facing evidence; commit only with pinned provenance and parity validation. |
| Release generated reports | 37 | modified | Commit only if regenerated from accepted source/tool changes and schemas/tests pass. |
| Runner source changes | 23 | 18 modified, 5 untracked | Candidate source commit after focused diff review and tests. |
| Release mismatch triage reports | 18 | untracked | Diagnostic support; keep only final/current summaries, otherwise archive. |
| Test changes | 14 | 12 modified, 2 untracked | Candidate source commit together with the runner/schema behavior they validate. |
| Release task metadata | 12 | modified | Candidate paper-facing metadata commit after content and report consistency checks. |
| Release model baseline audit reports | 7 | 2 modified, 5 untracked | Support-only; defer until score denominator and baseline protocol are stable. |
| Release speed remaining queue reports | 6 | untracked | Defer until same-slice speed experiment claim gate is stable. |
| Release package root manifests | 5 | modified | Commit only with generated report set and manifest checksum consistency. |
| Speed optimization analysis | 4 | untracked | Local analysis/scratch unless promoted into a compact report. |
| Release paper table CSVs | 3 | modified | Commit only with corresponding JSON/Markdown report regeneration. |
| Schema changes | 3 | 1 modified, 2 untracked | Candidate source commit, but only with tests and migration notes. |
| Speed optimization plans | 3 | untracked | Historical/support docs; commit only if they remain part of current speed claim protocol. |
| Docs web asset | 1 | untracked | Unknown provenance; inspect before committing. |

## Commit Batches

### Batch 1: Source and Validation Plumbing

Candidate paths:

- `runners/`
- `schemas/`
- `tests/`

Purpose:

- Preserve actual code/schema/test changes before touching generated reports.
- Make later report updates reproducible.

Required checks:

- Inspect diffs for scope creep into model-baseline or speed-only code.
- Run the smallest relevant `pytest` subset for changed reports/runners.
- Do not include generated report outputs in this commit.

### Batch 2: Release Metadata and Report Regeneration

Candidate paths:

- `benchmark-vabench-release-v1/EVALUATOR.*`
- `benchmark-vabench-release-v1/MANIFEST.*`
- `benchmark-vabench-release-v1/README.md`
- `benchmark-vabench-release-v1/tasks/**/release_entry.json`
- `benchmark-vabench-release-v1/tasks/**/release_task.json`
- `benchmark-vabench-release-v1/reports/*.json`
- `benchmark-vabench-release-v1/reports/*.md`
- `benchmark-vabench-release-v1/reports/paper_tables/*.csv`

Purpose:

- Capture the paper-facing release package state after source/tooling is verified.

Required checks:

- Validate manifest/report schema consistency.
- Confirm `score_denominator_manifest` remains the scoring source of truth.
- Confirm no EVAS PASS / Spectre FAIL is introduced in audited release slices.
- Label any stale or imported-only report before committing it.

### Batch 3: Dual Evidence Refresh

Candidate paths:

- `benchmark-vabench-release-v1/evidence/dual/**`

Purpose:

- Preserve current EVAS/Spectre certification evidence only if it is current and reproducible.

Required checks:

- Pin EVAS Rust commit, Spectre/Cadence environment, row slice, and runner command.
- Confirm evidence corresponds to the same release rows referenced by reports.
- Do not mix historical rerun imports with final certification evidence unless explicitly labeled.

### Batch 4: Diagnostic Support Reports

Candidate paths:

- `benchmark-vabench-release-v1/reports/evas_spectre_mismatch_triage_*`
- `benchmark-vabench-release-v1/reports/vabench_model_baseline_quality_audit_*`
- `benchmark-vabench-release-v1/reports/speed_remaining_*`

Purpose:

- Keep compact diagnostics that support decisions, not every historical attempt.

Required checks:

- Choose one current report per diagnostic purpose.
- Mark older reports as historical or archive them outside the repo.
- Do not use these as final benchmark score, parity, speed, or baseline claims without the corresponding claim gate.

### Batch 5: vaBench-300 Expansion

Candidate paths:

- `benchmark-vabench-release-v1/vabench-300-expansion/`
- `runners/*vabench_300*`
- `schemas/vabench-300-expansion-manifest.schema.json`
- `tests/test_vabench_300_expansion.py`

Purpose:

- Keep expansion work separate from the current release-v1 paper package.

Required checks:

- Use a separate branch or data-package decision before committing.
- Decide whether the expansion is source material, heldout/OOD material, or a future benchmark version.
- Avoid making vaBench-300 part of current release-v1 claims prematurely.

### Batch 6: Speed Optimization Archive/Promotion

Candidate paths:

- `speed-optimization/analysis/`
- `speed-optimization/plans/`
- `speed-optimization/reports/`

Purpose:

- Preserve only compact, paper-relevant speed evidence and archive the rest.

Required checks:

- Follow `speed-optimization/AGENTS.md` before editing inside this tree.
- Promote only reports tied to same-slice EVAS/Spectre timings.
- Archive historical raw sweeps outside the repo with a manifest before deletion.

### Batch 7: Rerun Staging Cleanup

Candidate paths:

- `benchmark-vabench-release-v1/rerun_staging*/`

Purpose:

- Remove or archive generated staging data so the repository remains reviewable.

Required checks:

- Preserve a short manifest if deletion is broad.
- Do not delete source/gold/checker assets that were intentionally promoted into the release package.
- Do not commit staging directories wholesale.

## Recommended Next Step

Start with Batch 1. If runner/schema/test diffs are coherent, commit them alone with targeted tests.
Then regenerate or validate release reports and evidence in separate commits.
