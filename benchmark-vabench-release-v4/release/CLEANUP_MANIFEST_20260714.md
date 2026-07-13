# vaBench v4 release cleanup manifest — 2026-07-14

Current kept release roots:

- `tri-form-v4-1200-final` — active 1,200-task tri-form benchmark release.
- `dut-base-v3-exact-five-hash-bound-v2` — canonical DUT source package referenced by the final tri-form task records.

Removed stale release roots:

- `tri-form-v4-1200-draft`
- `dut`
- `dut-base-v3`
- `dut-base-v3-catalog-certified`
- `dut-base-v3-exact-five`
- `dut-base-v3-exact-five-hash-bound`

Removed stale prep manifests:

- `operations/tri_form_derivation_prep/DERIVATIVE_TASK_INDEX.json`
- `operations/tri_form_derivation_prep/PREP_MANIFEST.json`

Reason:

- Runner, prompt export, campaign, feedback, and selected API pilot configs now point at `tri-form-v4-1200-final`.
- The final package has `solver_contract.json` for all 1,200 tasks, v2 testbench security policy alignment, and 7,200 prompt records.
- Older materialized roots were removed to prevent accidental stale benchmark runs.
