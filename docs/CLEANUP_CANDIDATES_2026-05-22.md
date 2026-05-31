# Cleanup Candidates 2026-05-22

This is a deletion manifest for generated experiment artifacts under
`behavioral-veriloga-eval`.

The repository mainline is vaBench plus EVAS/Spectre parity. Do not delete
benchmark source, gold references, checkers, schemas, runner source, or compact
paper-facing reports.

## Keep

Keep these directories/files unless their references are first decoupled from
tests, reports, or imported evidence:

- `benchmark-vabench-release-v1/`
- `speed-optimization/`
- `conformance/`
- `datasets/`
- `docs/`
- `examples/`
- `runners/`
- `schemas/`
- `scripts/`
- `tasks/`
- `tests/`
- `tables/`
- `docs/RESULT_ARCHIVE_MANIFEST_2026-05-22.md`
- `docs/RESULT_ARCHIVE_MANIFEST_2026-05-22.json`

The four large result directories previously listed here were generated output.
They have been compressed outside the repository and are now tracked by the
archive manifest above. Restore them only for waveform-level historical
reproduction.

## Safe Cleanup Candidates

These are cache or generated-result directories and are already covered by
`.gitignore` patterns:

- `.pycache/`
- `.pytest_cache/`
- `.DS_Store`
- `results/tmp-*`
- `results/*dry-check*`
- `results/*smoke*`
- `generated-main120-*`
- `results-bpack48__*`
- `results-probe-*`
- `results-mimo-*`
- `experiment-logs/`
- `runlogs/`
- `refine-logs/`

Estimated reclaim from the sampled groups:

- cache files: about 1.1 MB
- temp/dry/smoke result groups: about 26 MB
- old generated main120 / bpack / probe / mimo groups: about 82 MB

Status: first-pass cleanup executed for caches, old generated main120/bpack/probe/mimo
groups, `runlogs/`, `experiment-logs/`, `refine-logs/`, `results/tmp-*`, and
`results/vabench-release-v1-dual-rerun-dry-check-*`.

## Speed Raw Output Candidates

Compact speed evidence now lives under `speed-optimization/reports/`, so these
raw run output directories can be deleted when waveform-level debugging is not
needed:

- `results/evas-speed-*`
- `results/vabench-release-v1-dual-rerun-speed-remaining-*`

Estimated reclaim: about 119 MB.

Status: first-pass cleanup executed.

## Larger Candidate After Review

These shard directories are not referenced by current docs/tests/reports in the
local grep pass and appear to be intermediate raw rerun shards:

- `results/vabench-release-v1-dual-rerun-shard-*`

Estimated reclaim: about 284 MB.

Status: first-pass cleanup executed.

## Do Not Delete Blindly

Do not delete all of `results/` at once. Several result roots are still named by
paper artifact reports, tests, and imported dual evidence. Clean individual
generated groups only, then rerun the relevant tests.

## Archived Raw Evidence

Status: archived after validation.

- `results/vabench-main-v1-main120-gold-evas-2026-05-08`
- `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08`
- `results/vabench-release-v1-dual-rerun-20260516-full-after-fixes`
- `results/vabench-release-v1-nonreview-dual-20260518-023558`

See `docs/RESULT_ARCHIVE_MANIFEST_2026-05-22.md` for archive paths, SHA-256
checksums, summaries, and restore commands.

Recommended smoke check after cleanup:

```text
python3 scripts/check_repo_layout.py
python3 -m pytest tests/test_vabench_release_speed_baseline_artifacts.py
```
