# vaBench Release Package v1

This directory is the clean paper-facing benchmark package for the 72-entry L1/L2
vaBench release target. It is intentionally claim-gated: source assets,
static checks, imported EVAS/Spectre evidence, fresh rerun staging, score
denominators, speed/debug measurements, and model baselines are reported as
separate surfaces.

This package is the current vaBench release target. It can be cited only through
the current reports in `reports/`. A row
is not part of the scored benchmark until its score-denominator report marks it
as counted, and no pending or blocked simulator run is certification evidence.

## Layout

- `tasks/`: scored L1/L2 task directories after materialization.
- `conformance/`: non-scored L0 EVAS/Spectre diagnostic cases.
- `evidence/`: certification bundles and simulator logs referenced by tasks.
- `reports/`: coverage, parity, speed/debug, baseline, completion, artifact
  index, claim gate, and paper table summaries.
- `rerun_staging/`: staged runnable bundles for the fresh EVAS/Spectre rerun.

Rows are planned in `../docs/VABENCH_RELEASE_TRACKER.csv`. A row is not part of
the scored benchmark until its task assets and EVAS/Spectre evidence are
complete.

Current seed rows may contain `forms/<form>/` directories copied from reviewed
source tasks. These copied assets are release-materialized, but still unscored
until static, EVAS, and Spectre certification are attached.

L0 conformance assets are synchronized from `../conformance/evas-spectre/`.
They are simulator diagnostics and do not count toward L1/L2 benchmark coverage,
model capability, bugfix claims, or broad parity denominators.

## Current Claim Boundary

The current local package is source-complete, statically certified, and
EVAS/Spectre certified for the release denominator. Speed/debug measurements and
model baselines remain separate gated claims.

Use these reports as the source of truth:

- `reports/claim_gate.json`: allowed and blocked paper claims with safe wording.
- `reports/paper_tables.json`: CSV/Markdown table exports for paper drafting.
- `reports/completion_audit.json`: requirement-by-requirement completion gate.
- `reports/artifact_index.json`: traceability index for artifacts and commands.
- `reports/score_denominator_manifest.json`: only source of truth for scored
  entries/forms.
- `reports/external_blockers.json`: external bridge/rerun/import blocker chain.
- `reports/finish_readiness.json`: preflight gate for safely starting,
  importing, and finishing the fresh EVAS/Spectre release rerun.
- `MANIFEST.json`: package-level machine-readable index for entries, forms,
  assets, evidence links, certification status, and score inclusion.
- `EVALUATOR.json`: machine-readable evaluator contract for task selection,
  backend roles, result/evidence schemas, score gates, and baseline lanes.

Current safe wording is intentionally narrow:

- The package defines a 72-entry L1/L2 coverage target.
- All materialized release forms pass static/integrity checks.
- The certified EVAS/Spectre release evidence is clean with respect to EVAS
  PASS / Spectre FAIL mismatches.
- L0 conformance is separate from the benchmark denominator.

Do not claim EVAS speedup, debug advantage, or model baselines until the
corresponding claim gate is allowed.

## Reproducible Commands

Regenerate the local release package, reports, schema validation, checksums, and
tests:

```bash
python3 runners/run_vabench_release_longrun.py
```

After the external Virtuoso bridge is reachable, finish the fresh dual rerun,
import only complete results, and refresh downstream reports:

```bash
python3 runners/finish_vabench_release_after_bridge.py
```

The direct rerun command is:

```bash
./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py \
  --output-root results/vabench-release-v1-dual-rerun \
  --timeout-s 180
```

Blocked or dry-run summaries must not be imported as certification evidence.
Use `reports/bridge_profile_diagnostics.json` and
`reports/external_blockers.json` to decide whether the bridge is ready. Use
`reports/finish_readiness.json` before importing any fresh rerun summary.
