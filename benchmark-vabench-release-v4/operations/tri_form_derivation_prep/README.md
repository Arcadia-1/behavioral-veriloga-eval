# Tri-Form Release Builder

This directory contains the isolated preparation and materialization tools for
deriving the Testbench and Bugfix forms from the 400 canonical DUT families.

It intentionally does not modify:

- `tasks/` or `formal_tasks/`;
- `formal_derivatives/`;
- task-local `evaluator/certification.json` files;
- release manifests or `TOOLCHAIN_LOCK.json`;
- any `operations/task_side_*` closeout directory.

`build_sync_prep.py` is the historical pre-freeze inventory builder.
`materialize_tri_form_release.py` is the release builder: it consumes the
hash-bound exact-five DUT denominator from `provenance/` and creates 400 DUT,
400 Testbench, and 400 Bugfix public task views under one benchmark package
root. It also regenerates the `private_evaluator/` subpackage used by audits
and runners.

The generated plan activates exactly five mutations per family: 2,000 active
mutations in the formal tri-form release. The 51 source-catalog extras remain
in a provenance-only archive index and are not exported as scored cases.

The private evaluator package treats `evaluator/score_tb.scs` as the
canonical reference fixture. Existing score-profile gold and mutation evidence
is reused by hash.
Mutations certified only under a legacy feedback deck enter a cross-profile
audit queue; they are rerun only when semantic witness portability cannot be
proved. Legacy include paths use a content-identical private path adapter and
do not trigger analog reruns by themselves. Public candidate testbenches still
use the canonical `./dut/{artifact_path}` binding.

Materialize and audit the 1,200 task views:

```bash
python3 operations/tri_form_derivation_prep/materialize_tri_form_release.py
python3 operations/tri_form_derivation_prep/audit_tri_form_release.py \
  --output release/benchmarkv4/private_evaluator/evidence/AUDIT_REPORT.json \
  --seal-output release/benchmarkv4/private_evaluator/evidence/RELEASE_SEAL.json
```

The tracked release package is `release/benchmarkv4/`. Its root contains the
solver-facing public surface (`MANIFEST.json`, `TASK_INDEX.json`,
`prompt_modes/`, and `tasks/`). Its `private_evaluator/` subdirectory contains
gold references, mutation bundles, score policies, and derivation records for
local scoring and audits. Only local generated audit/runtime evidence under
`private_evaluator/evidence/` and optional prompt-record snapshots under
`private_evaluator/prompt_records/` are ignored by git.

The construction source package is tracked separately under
`provenance/dut-base-v3-exact-five-hash-bound-v2/` so `release/` contains only
the final distributable package. Per-task `public_contract.json` files remain
inside `release/benchmarkv4/tasks/` as machine-readable public metadata, but
runtime export does not mount or inline them into model prompts.

Export one runtime record without mounting evaluator-private files:

```bash
python3 operations/tri_form_derivation_prep/export_tri_form_runtime.py \
  --task v4-501 --mode G2 --working-token-budget 32768 \
  --output /tmp/vabench-runtime-v4-501-g2
python3 operations/tri_form_derivation_prep/audit_runtime_export.py \
  --run /tmp/vabench-runtime-v4-501-g2
```

Rebuild the historical preparation snapshot only when its input inventory is
needed:

```bash
python3 operations/tri_form_derivation_prep/build_sync_prep.py
```

The materialized release is structurally audited, but its status remains
`materialized_gate3_audit_pending`. Runtime export evidence proves record
ingestion and public/private bundle isolation only. It is not a model-run
result, a fixed-toolchain EVAS/Spectre certification, or a final score.

The old `formal_derivatives/` front-20 packages are prototypes and are not the
canonical 800 derivative tasks. The canonical public generated views live under
`release/benchmarkv4/tasks/`. The historical "tri-form" wording remains an
internal construction term for DUT/Testbench/Bugfix derivation, not the public
package name.
