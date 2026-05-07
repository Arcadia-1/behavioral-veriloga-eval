# Repository Cleanup Policy

**Date**: 2026-05-07

This policy keeps the vaEVAS repository usable while preserving experiment
traceability.  The goal is to reduce local noise without deleting evidence that
may still explain historical results.

## Cleanup Principle

Do not delete experiment artifacts just because they are messy.  First classify
them:

| Class | Examples | Action |
| --- | --- | --- |
| Maintained source | `runners/`, `benchmark-balanced/`, `benchmark-v2/`, tests, canonical docs | Keep tracked and review normally. |
| Maintained compact evidence | summary markdown/json, manifests, audit summaries referenced by clean mainline docs | Keep tracked if already part of PR evidence. |
| Local generated artifacts | `generated-*`, `results-*`, `runlogs/`, `scratch/`, `refine-logs/` | Ignore by default; do not add unless explicitly promoted. |
| Historical generated artifacts already tracked | older `generated-*` directories that are already in git history | Do not bulk delete; archive/remove only through a reviewed manifest. |
| Retired experiments | standalone old 92 runs, fixed-stage EVAS, identity-routed G, unstable MiMo partials | Keep only compact summaries if needed; raw artifacts can be archived outside the main PR after review. |

## Current Noise Source

The workspace currently contains many local experiment directories.  A quick
scan found hundreds of top-level artifact directories matching patterns such as:

```text
generated-*
results-*
runlogs/
scratch/
refine-logs/
```

`.gitignore` now ignores these broad local artifact patterns for future runs.
This does not untrack files that were already committed; it only keeps new local
runs from polluting `git status`.

## What Should Stay In The Main PR

Keep the clean paper-facing spine:

1. benchmark/task source files needed to run `b143`
2. strict EVAS/Spectre parity fixes
3. compile-skill code, registry, tests, and compact manifests
4. docs that define the clean mainline and maintained evidence
5. compact result summaries referenced by the PR body

## What Should Not Be Added By Default

Do not add by default:

- raw model responses
- waveform CSVs
- per-task transient logs
- full generated candidate trees from exploratory runs
- local bridge uploads/downloads
- partial failed provider runs
- prompt-compression scratch experiments

If one of these is needed as evidence, add a compact derived summary instead.
Only force-add raw artifacts after a reviewer explicitly asks for them.

## Safe Cleanup Workflow

Use this order:

1. **Ignore local noise**: update `.gitignore` for broad local artifact patterns.
2. **Document retained evidence**: keep a clean list in `docs/VAEVAS_CLEAN_MAINLINE.md`.
3. **Summarize before deleting**: for any artifact family to remove/archive,
   first write a manifest with path, size, result it supports, and replacement
   summary file.
4. **Archive outside the PR**: move bulky raw artifacts to external storage or a
   release asset only after the manifest is reviewed.
5. **Delete in a separate cleanup PR**: never mix destructive cleanup with method
   or evaluator changes.

## Commands For Auditing

List local artifact directories:

```bash
find . -maxdepth 1 -type d \
  \( -name 'generated-*' -o -name 'results-*' -o -name 'runlogs' -o -name 'scratch' -o -name 'refine-logs' \) \
  | sort
```

Check whether a noisy path is ignored:

```bash
git check-ignore -v generated-b143__kimi-k25__strict-evas__rules-only__20260507
```

Find tracked historical generated artifacts before considering any deletion:

```bash
git ls-files 'generated-*' 'results-*' | sed -n '1,200p'
```

## Deletion Rule

No raw artifact deletion should happen in the same PR as algorithm, validator,
benchmark, or paper-claim changes.  Deletion is allowed only after:

1. the artifact is not referenced by the clean mainline, PR body, or result docs;
2. a compact summary or manifest exists if the artifact supports a historical
   claim;
3. the cleanup is reviewed as a standalone cleanup commit/PR.
