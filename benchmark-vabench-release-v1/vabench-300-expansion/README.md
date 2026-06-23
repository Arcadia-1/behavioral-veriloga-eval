# vaBench 300 Expansion Manifest

- tasks: 300
- existing certified v1 tasks: 271
- task-specific v1.1 tasks: 29
- paper-score-ready tasks: 300
- simulator-certified benchmark tasks: 300
- fresh Spectre-certified v1.1 tasks: 29
- score-denominator-admitted v1.1 tasks: 29
- score-denominator-pending v1.1 tasks: 0
- negatives per task: 5
- total partial-pass negatives: 1500
- static shallow-shape verified negatives after audit: 1500
- simulator shallow-lane verified negatives: recorded by `v11_task_specific_quality_evidence.json`
- full-checker fail verified negatives: recorded by `v11_task_specific_quality_evidence.json`

Certification boundary: the 29 v1.1 rows now have task-specific prompts, gold implementations, checker IDs, near-miss negatives, local EVAS quality evidence, fresh EVAS/Spectre PASS evidence, and explicit score-denominator admission evidence.

## Purpose

This directory is the primary vaBench 300 management surface. It indexes 271 inherited certified v1 form-level rows plus 29 task-specific v1.1 rows. Use 300 as the asset-management and simulator-certification surface. The current scored model-evaluation denominator contains 265 core rows after support-suite exclusions.

`benchmark-vabench-release-v1/reports/vabench_300_v11_fresh_spectre_rerun.json` records the compact fresh Spectre rerun import for the 29 v1.1 rows. Raw simulator outputs are intentionally not versioned.

Every task has a partial-pass negative manifest with five near-miss candidates. For v1.1 rows, the negatives are generated from task-specific variants intended to compile and run while failing the registered full checker.

## Files

- `VABENCH_300_MANIFEST.json`: the 300-task index.
- `v11_task_specific_quality_evidence.json`: EVAS gold/negative quality evidence for v1.1 rows.
- `benchmark-vabench-release-v1/reports/vabench_300_v11_fresh_spectre_rerun.json`: compact fresh Spectre rerun evidence for v1.1 rows.
- `benchmark-vabench-release-v1/reports/vabench_300_v11_score_admission.json`: score-denominator admission audit for the 29 v1.1 rows.
- `negative_audit.json`: asset/hash/count audit for all negative manifests.
- `existing-negatives/`: five negative candidates for each existing certified v1 task.
- `proposed-tasks/`: the 29 v1.1 task assets, including prompt, checks, gold, release task manifests, and negatives.

## Schemas

- `../../schemas/vabench-300-expansion-manifest.schema.json`
- `../../schemas/vabench-partial-pass-negatives.schema.json`

## Commands

Regenerate the pre-import expansion package:

```bash
python3 runners/build_vabench_300_expansion.py
```

Reattach fresh v1.1 Spectre evidence after a rerun:

```bash
python3 runners/import_vabench_300_v11_spectre_rerun.py --summary /path/to/summary.json
```

Audit and admit v1.1 rows to the score denominator:

```bash
python3 runners/audit_vabench_300_v11_score_admission.py --apply
```

Audit negative manifests:

```bash
python3 runners/audit_vabench_300_expansion.py
```

Run the focused tests:

```bash
PYTHONPATH=runners python3 -m pytest tests/test_vabench_300_expansion.py -q
```
