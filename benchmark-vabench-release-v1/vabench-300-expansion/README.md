# vaBench 300 Expansion Manifest

- tasks: 300
- existing certified v1 tasks: 271
- promoted v1.1 tasks: 29
- certified benchmark tasks: 300
- pending certification tasks: 0
- negatives per task: 5
- total partial-pass negatives: 1500
- static shallow-shape verified negatives after audit: 1500
- simulator shallow-lane verified negatives: 0
- full-checker fail verified negatives: 0

Certification boundary: the 29 v1.1 tasks are promoted by `speed-optimization/reports/vabench300_p0_p2_closure_20260620.md`. Negative candidates remain static-shape audited, not full-checker-certified.

## Purpose

This directory is the primary vaBench 300 management surface. It treats each form-level task as a benchmark task: 271 inherited certified v1 rows plus 29 promoted v1.1 rows.

Every task has a partial-pass negative manifest with five near-miss candidates. These candidates are intended to preserve enough surface structure to pass shallow checks while failing the full checker. The current audit verifies file presence, hashes, counts, metadata, required negative categories, and static shallow shape (non-empty, different from reference, interface/testbench structure preserved); it is not simulator proof that every candidate has the intended full-check failure.

## Files

- `VABENCH_300_MANIFEST.json`: the 300-task index.
- `negative_audit.json`: asset/hash/count audit for all negative manifests.
- `existing-negatives/`: five negative candidates for each existing certified v1 task.
- `proposed-tasks/`: the 29 promoted v1.1 task assets, including prompt, checks, gold, release task manifests, and negatives.

## Schemas

- `../../schemas/vabench-300-expansion-manifest.schema.json`
- `../../schemas/vabench-partial-pass-negatives.schema.json`

## Commands

Regenerate this expansion package:

```bash
python3 runners/build_vabench_300_expansion.py
```

Audit negative manifests:

```bash
python3 runners/audit_vabench_300_expansion.py
```

Run the focused tests:

```bash
PYTHONPATH=runners python3 -m pytest tests/test_vabench_300_expansion.py -q
```
