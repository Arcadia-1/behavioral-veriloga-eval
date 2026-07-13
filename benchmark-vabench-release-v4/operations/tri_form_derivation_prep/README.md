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
hash-bound exact-five DUT denominator and creates 400 DUT, 400 Testbench, and
400 Bugfix task views plus the G0-G5 experiment records.

Prompt composition is fixed as canonical task inputs, optional form skill,
optional feedback skill, and the neutral submission wrapper last. This gives
G0-G5 an identical final submission contract. The three form skills are short,
task-independent checklists derived from installed Cadence Spectre 21.1 help
(`spectre -h veriloga`, `spectre -h vsource`, and `spectre -h ahdllint`); their
source commands and version are recorded in the generated skill manifest.

To refresh only prompt assets and 7,200 prompt records after a global skill or
composition update, without rebuilding any task directory, run:

```bash
python3 operations/tri_form_derivation_prep/refresh_prompt_assets.py
```

The generated plan activates exactly five mutations per family: 2,000 active
mutations in the formal tri-form release. The 51 source-catalog extras remain
in a provenance-only archive index and are not exported as scored cases.

The release treats `evaluator/score_tb.scs` as the canonical reference fixture.
Existing score-profile gold and mutation evidence is reused by hash.
Mutations certified only under a legacy feedback deck enter a cross-profile
audit queue; they are rerun only when semantic witness portability cannot be
proved. Legacy include paths use a content-identical private path adapter and
do not trigger analog reruns by themselves. Public candidate testbenches still
use the canonical `./dut/{artifact_path}` binding.

Materialize and audit the 1,200 task views:

```bash
python3 operations/tri_form_derivation_prep/materialize_tri_form_release.py
python3 operations/tri_form_derivation_prep/audit_tri_form_release.py
```

Export one runtime record without mounting evaluator-private files:

```bash
python3 operations/tri_form_derivation_prep/export_tri_form_runtime.py \
  --task v4-501 --mode G2 --working-token-budget 65536 \
  --output /tmp/vabench-runtime-v4-501-g2
python3 operations/tri_form_derivation_prep/audit_runtime_export.py \
  --run /tmp/vabench-runtime-v4-501-g2 \
  --output /tmp/vabench-runtime-v4-501-g2/evidence/runtime_export_audit.json
```

Rebuild the historical preparation snapshot only when its input inventory is
needed:

```bash
python3 operations/tri_form_derivation_prep/build_sync_prep.py
```

The builder emits `package_materialized_behavior_evidence_pending`; a successful
static audit writes a `package_structure_sealed` seal. A fingerprint mismatch
means evidence must be rebound or replayed against current bytes, but the
materializer does not by itself decide that an analog simulation rerun is
necessary. Runtime export evidence proves record ingestion and public/private
bundle isolation only. It is not a model-run result, a fixed-toolchain
EVAS/Spectre certification, or a final score.

The old `formal_derivatives/` front-20 packages are prototypes and are not the
canonical derivative task set. The canonical generated views now live under
`release/tri-form-v4-1200-final/tasks/`. This static release name is fixed for
runner/prompt use; EVAS/Spectre behavior-seal claims remain a separate evidence
gate.
