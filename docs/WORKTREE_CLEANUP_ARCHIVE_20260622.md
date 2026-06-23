# Worktree Cleanup Archive, 2026-06-22

This document records the cleanup performed after the dirty worktree triage.
The cleanup goal was to avoid committing old or generated files while preserving enough evidence to recover any discarded local state.

## Result

- Repository: `behavioral-veriloga-eval`
- Branch: `codex/main120-normal-source-materialization`
- Archive path: `/Users/bucketsran/Documents/TsingProject/vaEvas/_archives/behavioral-veriloga-eval/worktree-cleanup-20260622T131500`
- Archived HEAD: `f1d0e73aa9f7a6134233e9389c8e84d851c63696`
- Expanded dirty entries before cleanup: 7,772
- Untracked files moved out of the repository: 7,620
- Unexpected nested result directory moved out: `behavioral-veriloga-eval/`
- Tracked local modifications restored to `HEAD`: yes
- Tracked patch archive: `tracked_dirty.patch`
- Tracked patch SHA256: `ab487dea08723496fc3bc037640878ab620646c4fb9c8db96b4d0097482003b6`

## Preserved Archive Files

- `summary.json`: machine-readable cleanup summary.
- `HEAD.txt`: source commit before cleanup.
- `BRANCH.txt`: source branch before cleanup.
- `status_porcelain_uall.txt`: full dirty worktree status before cleanup.
- `status_porcelain_collapsed.txt`: collapsed dirty worktree status before cleanup.
- `mtime_audit.jsonl`: status, path, size, and modification time for each dirty entry.
- `tracked_dirty.patch`: patch for all tracked local modifications before restore.
- `tracked_dirty.diffstat.txt`: diffstat for tracked local modifications.
- `tracked_dirty.name_status.txt`: name-status for tracked local modifications.
- `untracked_files.txt`: list of all untracked files moved into the archive.
- `untracked/`: preserved copy of moved untracked files, with repository-relative paths.
- `unexpected-top-level/behavioral-veriloga-eval/`: preserved nested raw result directory that violated the repository layout policy.

## Modification-Time Findings

- Most old files were generated rerun staging material from `2026-05-24` through `2026-05-31`.
- Large untracked generated groups were not committed during initial cleanup:
  - `benchmark-vabench-release-v1/rerun_staging*/`
  - `speed-optimization/reports/`
  - ad hoc diagnostic reports under `benchmark-vabench-release-v1/reports/`
- `benchmark-vabench-release-v1/vabench-300-expansion/` was initially archived as untracked material, then selectively restored after verifying that it is the intended 300-task benchmark surface rather than disposable staging output.
- A nested `behavioral-veriloga-eval/results/...` directory was also removed from the repository root and archived because it was raw result output in an invalid top-level location.
- Recent source/test edits from `2026-06-21` and `2026-06-22` were also preserved in `tracked_dirty.patch` or `untracked/`, but not committed because they were not yet proven coherent with tests and reports.

## Selected Restoration

After cleanup, the following archived paths were restored because they form the intended vaBench-300 surface and its validation harness:

- `benchmark-vabench-release-v1/vabench-300-expansion/`
- `runners/audit_vabench_300_expansion.py`
- `runners/build_vabench_300_expansion.py`
- `runners/report_vabench_300_dual_summary.py`
- `runners/run_vabench_300_dual_rerun.py`
- `runners/run_vabench_300_evas_gold.py`
- `schemas/vabench-300-expansion-manifest.schema.json`
- `schemas/vabench-partial-pass-negatives.schema.json`
- `tests/test_vabench_300_expansion.py`
- `speed-optimization/reports/vabench300_p0_p2_closure_20260620.md`

The minimal tracked runner dependency for `run_vabench_300_dual_rerun.py` was also restored from `tracked_dirty.patch`: Spectre invocation mode support in `runners/run_gold_dual_suite.py` and `runners/run_vabench_release_dual_rerun.py`.

## Recovery

To inspect the archived tracked changes:

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval
git apply --stat /Users/bucketsran/Documents/TsingProject/vaEvas/_archives/behavioral-veriloga-eval/worktree-cleanup-20260622T131500/tracked_dirty.patch
```

To restore selected untracked files, copy only the required paths from:

```bash
/Users/bucketsran/Documents/TsingProject/vaEvas/_archives/behavioral-veriloga-eval/worktree-cleanup-20260622T131500/untracked/
```

Do not bulk-restore the archived rerun staging or speed report trees unless they are explicitly promoted to paper-facing fixtures or compact reports.
