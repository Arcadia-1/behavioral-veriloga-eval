# vaBench Taxonomy Preflight

Date: 2026-05-15

## Purpose

This preflight checks whether the current vaBench taxonomy is ready to become
the instruction surface for a goal-mode build/validation loop.

Verdict: usable for the next goal-mode build loop. The two required policy
refinements have been applied:

1. Keep the release taxonomy independent from historical rows by adding a clean
   release-facing view without implementation source-trace wording.
2. Add an explicit base-function counting registry so duplicate kernels,
   evidence-only rows, L0 conformance cases, and weak e2e forms cannot inflate
   benchmark claims.

## Inputs Checked

- `docs/VAEVAS_MAINLINE_PLAN.md`
- `docs/VABENCH_TOPDOWN_FUNCTION_TAXONOMY.md`
- `docs/VABENCH_MAIN120_MATERIALIZATION.md`
- `docs/VABENCH_MAIN120_MATERIALIZATION.csv`
- `docs/VABENCH_D004_BUGFIX_TRIAGE.md`
- `docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md`
- `docs/EVAS_SPECTRE_PASS_DRIFT_AUDIT.md`
- top-level `CAPABILITY_SCOPE_MATRIX.md`
- top-level `NEGATIVE_SCOPE_GUARDS.md`

## Current Release Facts

These are the facts that can be used as goal-mode state.

| Fact | Value | Interpretation |
| --- | --- | --- |
| main120 evidence rows | 120 | Historical validated evidence rows. |
| EVAS PASS rows | 120 | Gold EVAS evidence is complete for main120. |
| Spectre PASS rows | 120 | Gold Spectre evidence is complete for main120. |
| Source-materialized rows | 116 | Rows with exact source-controlled task IDs. |
| Countable model-capability rows | 115 | Rows allowed in current model-capability denominator. |
| Countable bugfix rows | 25 | Bugfix rows with buggy/fixed provenance and dual confirmation. |
| Evidence-only rows | 5 | Excluded from model-capability, benchmark-coverage, and bugfix denominators. |
| Fixed-only historical evidence-only rows | 4 | Fixed-only historical bugfix rows without release bugfix source. |
| Additional evidence-only duplicate | 1 | `background_calibration_accumulator_bugfix`; reconstructed but duplicate kernel. |
| Base circuits in main120 | 30 | Construction material, not automatically 30 distinct release functions. |
| Current promoted L1 seed bases | 28 | Countable functions inherited from current main120 after merging `background_calibration_accumulator` and removing `offset_calibration_fsm`. |
| Promoted top-level L1 additions | 32 | Additional L1 functions selected from examples, smoke tasks, and historical validated drafts as release coverage targets; not scored until materialized and certified. |
| Selected L2 complete-circuit target entries | 20 | Multi-function circuit/flow targets selected for release coverage; not scored until materialized and certified. |
| Top-level L1/L2 coverage target | 80 | 28 current L1 seeds + 32 selected L1 additions + 20 selected L2 targets, before task-form multiplication. |
| Forms per base | 4 | `dut`, `tb`, `bugfix`, `e2e`; form does not imply L2. |

Counting correction for future goal prompts:

- Say "5 evidence-only rows total".
- Say "4 fixed-only historical rows are evidence-only".
- Do not say all 5 evidence-only rows are fixed-only; one is evidence-only
  because of duplicate-kernel policy.

## Historical Foundation Facts

These facts are useful as supporting evidence, not as headline benchmark
counts.

| Foundation | Evidence | Use in paper story |
| --- | --- | --- |
| EVAS supported subset is explicit. | `CAPABILITY_SCOPE_MATRIX.md`: 27 GREEN, 18 GREEN-U, 6 YELLOW, 15 RED constructs. | Defines the pure voltage-domain event-driven behavioral scope. |
| Negative scope is explicit. | `NEGATIVE_SCOPE_GUARDS.md`. | Prevents over-claiming current-domain, KCL/KVL, AC/noise, device, and solver-level behavior. |
| Validation pipeline exists. | `docs/VAEVAS_VALIDATION_PIPELINE.md`. | Gives static, EVAS, Spectre, and compact-report gates. |
| Historical false positives were diagnosed. | `docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md`. | Motivates atomic L0 conformance suite under broad benchmark parity. |
| PASS drift was audited. | `docs/EVAS_SPECTRE_PASS_DRIFT_AUDIT.md`: 52 drifted forms, 14 deduplicated circuit groups. | Shows why stable checkers and tolerance policy matter beyond binary PASS. |
| D004 bugfix provenance policy is explicit. | `docs/VABENCH_D004_BUGFIX_TRIAGE.md`. | Prevents fixed-only historical rows from being counted as bugfix tasks. |

Additional local git-history evidence checked on 2026-05-15:

| Historical iteration | Source | Useful signal | Release boundary |
| --- | --- | --- | --- |
| `benchmark-v2` draft expansion | commit `e0c2f83`, `benchmark-v2/README.md` | 400 draft tasks were materialized across seed perturbation, hard-negative, and external-architecture splits; the 30 seed tasks and 370 expanded tasks were recorded as EVAS/Spectre gold validated. | Treat as expansion/gap source material and reusable validation history, not as the clean release definition. |
| `benchmark-balanced` task-form expansion | commit `028120d`, `benchmark-balanced/README.md` | 143 tasks explored four-form balancing across original and supplemental functions; the external supplement had 16/16 EVAS and real Spectre validation. | Useful warning that form balancing can inflate row count; release coverage must still be function-first. |
| closed-set 92 completion ledger | commit `348698a`, `docs/CLOSEDSET92_COMPLETION_LEDGER.json` and `docs/COMPLETION_PACKAGE_MANIFEST.json` | 92/92 closed-set accepted entries with explicit provenance; mechanism counts reveal reusable families such as converter decode, phase-detector pulse relation, PLL cadence, sample/hold, pointer windows, and calibration search. | Supports provenance discipline only. It cannot be used as a cold-start benchmark claim because 27/92 rows used teacher replay or teacher-derived Spectre fixes. |
| streaming checker parity proof | commit `2b39be4`, `docs/project/STREAMING_CHECKER_PARITY_2026-04-26.md` | Fixture parity showed 20/20 comparable matches and 0 mismatches; comparable real CSV smoke showed 2/2 matches. | Supports evaluator/checker infrastructure; it is not a benchmark function count. |

Safe wording:

> Earlier EVAS/Spectre work establishes the supported language subset,
> negative scope, validation pipeline, checker parity evidence, and known
> conformance risks. Earlier benchmark-v2, benchmark-balanced, and closed-set
> 92 iterations provide reusable historical evidence and source mechanisms.
> The clean vaBench release is not defined by those historical experiments; it
> reuses them only as supporting evidence, provenance, and regression material.

## Taxonomy Preflight Results

| Check | Result | Notes |
| --- | --- | --- |
| Categories are circuit-function oriented. | PASS with caveat | The nine categories are defensible, but release text should avoid saying they are a prior standard. |
| L0 is separated from L1/L2. | PASS | Current taxonomy states L0 is conformance-only and not in headline score. |
| Task form is separated from function level. | PASS with caveat | Taxonomy says only multi-component e2e rows count as L2; goal instructions must enforce this. |
| Historical rows are not the ontology source. | PASS | Clean release taxonomy now carries the main table; construction docs keep source traces only as internal implementation notes. |
| Duplicate kernel risk is visible. | PASS | Calibration/control is correctly marked as highest risk. Needs a counting registry. |
| Evidence-only policy is explicit. | PASS | D004 policy excludes five evidence-only rows from denominators. |
| Conformance cases are not counted as benchmark tasks. | PASS | Backlog defines separate `conformance/evas-spectre/` root. |
| Category hints match release taxonomy. | NEEDS ALIGNMENT | main120 hints include `analog-events`, `phase-detector`, and `signal-source`, which should map into release categories. |
| Each category has L2 direction. | PASS | All nine categories now have selected L2 targets in the level coverage table and release taxonomy. |
| Selection order optimizes function gaps. | PASS | Selected additions target real taxonomy gaps instead of row-count padding. |

## Taxonomy Issues To Fix Before Goal Mode

### T001: Release taxonomy should not expose implementation source traces

Problem: construction documents can contain implementation source traces. They
are useful during package assembly, but they invite readers or agents to treat
main120/examples as the ontology source if they appear in the paper-facing
table.

Fix: keep the current table as internal construction material, but add a clean
release-facing table with these columns:

```text
category
base_function
level
complete_circuit_form
required_task_forms
score_surface
release_status
certification_status
```

### T002: Add a base-function counting registry

Problem: 120 rows and 30 bases are construction counts. They do not equal 30
distinct release functions after duplicate-kernel and evidence-only policy.

Fix: add a registry with one row per base function:

```text
base_id
release_name
category
level
canonical_kernel
counts_as_distinct_function
allowed_task_forms
release_status
evidence_status
notes
```

### T003: Align historical category hints to release categories

Current mismatch:

| Historical hint | Release mapping |
| --- | --- |
| `phase-detector` | `PLL Clock and Timing Systems` |
| `analog-events` | map to the concrete analog-facing circuit family; keep pure timer/event primitives as conformance-only extraction |
| `signal-source` | split: real source generators go to `Stimulus and Source Generators`; clamps/slew limiters go to `Baseband Signal Conditioning` |
| `dac` | split: converter functions stay in `Data Converter Models`; CDAC calibration controller should map to calibration/control unless the public task is truly DAC modeling |

### T004: Do not count every e2e row as L2

Problem: some current e2e forms are single-block scenarios with a reference
testbench. They are useful benchmark forms but not necessarily complete
mini-systems.

Fix: add `level: L1-form` or `level: L2` per e2e row. Only multi-component
systems such as SAR ADC loop, PLL slice, calibration loop, measurement flow, or
signal chain should count in L2 score.

### T005: Measurement and stimulus need tighter counting rules

Measurement and stimulus can be valid benchmark tasks, but they can also become
testbench helper code or L0 simulator semantics.

Fix:

- Count measurement rows only when they implement a reusable measurement block
  or measurement flow.
- Count stimulus rows only when the model output is a reusable source block.
- Move pure file I/O, final-step timing, PWL syntax, and source breakpoint
  behavior into L0 conformance.

## Suggested Pre-Goal Work Order

| Run ID | Task | Output | Status |
| --- | --- | --- | --- |
| R000 | Approve this preflight policy. | Human decision. | Accepted in discussion. |
| R001 | Add clean release taxonomy view. | `docs/VABENCH_RELEASE_TAXONOMY.md`. | Done. |
| R002 | Add base-function counting registry. | `docs/VABENCH_BASE_FUNCTION_REGISTRY.csv` and `.md`. | Done. |
| R003 | Map historical category hints to release categories. | Registry mapping and category correction table. | Done. |
| R004 | Mark e2e level status. | `e2e_counting_rule` in registry. | Done for base-level release decisions; per-task metadata still needs propagation. |
| R005 | Update goal-mode facts. | Updated preflight and mainline references. | Done for documentation; final English goal input can now be regenerated. |

## Feasibility Verdict

The strategy is feasible.

The taxonomy is strong enough to guide the next stage if the goal-mode prompt
includes the safeguards above. The main unresolved risk is not technical; it is
counting semantics. Without a base-function registry, the agent loop may
silently convert row count into function count, or convert e2e form into L2
system coverage.

Recommended decision:

- The taxonomy-freeze pass has enough structure to support the larger
  release/validation/expansion goal.
- Before using automated goal mode to edit many tasks, use
  `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` as the human-readable L0/L1/L2 map
  and keep the two excluded bases out of release denominators.
