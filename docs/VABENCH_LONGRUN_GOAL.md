# vaBench Long-Run Goal

Date: 2026-05-17

## Objective

Build the clean vaBench release package from the 75-entry top-level L1/L2
coverage target. The release must contain public prompts, metadata, checks,
gold assets, EVAS/Spectre certification evidence, and paper-facing reports.

## Non-Negotiable Invariants

- Do not score uncertified rows.
- Keep L0 EVAS/Spectre conformance outside the L1/L2 benchmark denominator.
- Keep current-domain, KCL/KVL, transistor-level, AC/noise, and device physics
  outside this release unless the project scope is explicitly changed.
- Do not revive controller/RAG/SFT/workflow engineering as the core
  contribution.
- Spectre remains the final certification reference; EVAS remains the fast
  debug evaluator.

## Execution Surface

- Tracker: `docs/VABENCH_RELEASE_TRACKER.csv`
- Human tracker: `docs/VABENCH_RELEASE_TRACKER.md`
- Release package root: `benchmark-vabench-release-v1/`
- Release entry schema: `schemas/vabench-release-entry.schema.json`
- Release task schema: `schemas/vabench-release-task.schema.json`
- Evidence schema: `schemas/vabench-evidence.schema.json`
- Result schema: `schemas/vabench-release-result.schema.json`

## Required End State

1. Every tracker row has a release task or an explicit documented exclusion.
2. Every scored row has reviewed `prompt.md`, `meta.json`, `checks.yaml`,
   `gold/`, `evidence.json`, and `result.json`.
3. EVAS/Spectre dual certification has zero EVAS PASS / Spectre FAIL rows.
4. L0 conformance cases explain known syntax, source, event, sampling, and
   checker semantic risks.
5. Paper-facing reports include coverage, certification, parity, speed/debug,
   and baseline summaries.
6. A completion audit maps each goal requirement to current evidence and keeps
   blocked or pending items out of the completed state.
7. An artifact index maps schemas, trackers, reports, and rerun commands to
   their paper-facing claim roles.
8. Schema validation covers release entries, release task manifests, evidence,
   and result JSON surfaces.
9. A checksum manifest hashes release package, release docs, and schema files
   for reproducible paper-facing artifacts.
10. A score denominator manifest is the source of truth for scored entries and
   forms, and it keeps all uncertified rows out of reported model scores.

## Single Long-Run Policy

Do not expand this release by hand-sized batches. The runner should traverse
the full 75-entry tracker every time. Entries with release-ready source assets
are materialized immediately; entries without release-ready source assets are
kept as explicit pending package skeletons. Missing EVAS/Spectre evidence is a
pending certification blocker, not a simulator failure and not a scored result.

## Current Checkpoint

The current automated release run materializes 75 planned L1/L2 entries and
259 release forms. Static/integrity certification is regenerated from the clean
package assets. Historical dual evidence certifies the current imported subset,
while remaining primary forms are staged and ready
for a fresh EVAS/Spectre rerun. The remaining simulator blocker is external
bridge access: stale or partial rerun summaries are explicitly rejected by the
import gate until a fresh complete rerun exists.

The current verification command is:

```bash
python3 runners/run_vabench_release_longrun.py
```

It regenerates release package artifacts and runs the release test suite. Treat
the pytest summary printed by this command as the current local verification
evidence.

## Long-Run Command Pattern

Use this objective for the long process:

```text
Materialize and certify the clean vaBench release from docs/VABENCH_RELEASE_TRACKER.csv.
For each row, create or update the release task under benchmark-vabench-release-v1/tasks,
write prompt/meta/checks/gold assets, run static checks, stage EVAS and Spectre
certification bundles, import only complete rerun evidence, update evidence/result
files, and update the tracker. Do not score or claim any row until certification
passes. Keep L0 conformance separate.
```

## Automation Commands

Bootstrap, materialize, statically certify, prepare rerun staging, and refresh
claim-gated reports:

```bash
python3 runners/run_vabench_release_longrun.py
```

Run the primary EVAS/Spectre release rerun when the Virtuoso bridge is ready:

```bash
./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py \
  --output-root results/vabench-release-v1-dual-rerun \
  --timeout-s 180
```

Or use the one-command finish path, which tries bridge profiles, imports only
complete rerun evidence, and refreshes speed/baseline/paper/completion reports:

```bash
python3 runners/finish_vabench_release_after_bridge.py
```

The rerun consumes
`benchmark-vabench-release-v1/reports/dual_rerun_staging_manifest.json`.
By default it runs only primary pass bundles (`gold` and bugfix `fixed`). Use
`--include-buggy` only for the separate badcase confirmation lane.

The bridge wrapper is fail-fast and claim-gated:

- `VB_SSH_CONNECT_TIMEOUT`, `VB_SSH_SERVER_ALIVE_INTERVAL`, and
  `VB_SSH_SERVER_ALIVE_COUNT_MAX` bound SSH tunnel startup.
- Set `BRIDGE_PROFILE=jin` or another profile name to route through
  `VB_*_<profile>` values from the bridge `.env` without editing the file.
- Set `VB_USE_SSH_CONFIG_JUMP=1` when the bridge `.env` `VB_JUMP_HOST`
  conflicts with the local SSH `ProxyJump`; this lets `ssh` use the local
  `~/.ssh/config` route instead of passing an explicit `-J`.
- If tunnel startup fails before the release rerun runner starts, the wrapper
  asks `run_vabench_release_dual_rerun.py` to write only a blocked summary;
  it does not enable simulator direct-run fallback.
- A blocked summary is never imported as certification evidence.
- `benchmark-vabench-release-v1/reports/completion_audit.json` is the final
  per-run completion gate. It must remain `in_progress` until every required
  item is proved by current artifacts.
- `benchmark-vabench-release-v1/reports/artifact_index.json` is the
  traceability index for paper-facing artifacts and reproducible commands.
- `benchmark-vabench-release-v1/reports/schema_validation.json` validates
  release entries, per-form release task manifests, evaluator contract,
  score denominator, speed/debug, baseline, paper artifacts, claim gates,
  dual rerun gates, bridge/readiness gates, evidence, and results.
- `benchmark-vabench-release-v1/reports/score_denominator_manifest.json` is
  the only source of truth for scored entry/form denominators.
- `benchmark-vabench-release-v1/reports/checksum_manifest.json` records
  SHA-256 hashes for release artifacts, excluding itself.
