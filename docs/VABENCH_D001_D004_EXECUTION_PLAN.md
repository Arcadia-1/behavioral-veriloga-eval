# vaBench D001-D008 Execution Plan

Date: 2026-05-14

This plan turns the accepted D001-D008 benchmark-semantic decisions into an
execution path for materializing `vabench-main-v1-main120` as source-controlled
benchmark tasks plus a separate EVAS/Spectre conformance suite.

## Objective

Produce release-facing benchmark assets with honest task semantics:

- release checkers measure circuit behavior, not simulator output-grid artifacts;
- public `bugfix` tasks include a bad/fixed repair pair;
- fixed-only historical bugfix evidence is either reconstructed into true
  bugfix form, retained as evidence-only, or demoted only as a documented
  fallback;
- EVAS/Spectre semantic cases move into a separate conformance suite.
- P2 numeric drift is handled by documented metric tolerances and watchlists
  unless binary behavior or exact event/state semantics diverge.

## Non-Goals

- Do not present workflow/controller/RAG/SFT machinery as the contribution.
- Do not use raw CSV row counts, row fractions, or final-row boundary samples as
  release pass/fail criteria.
- Do not keep a task labeled `bugfix` merely because a historical row name
  contains `_bugfix`.
- Do not mix conformance tests into normal vaBench model-capability statistics.

## Required Inputs

- Main120 materialization map: `docs/VABENCH_MAIN120_MATERIALIZATION.csv`.
- Semantic policy: `docs/VABENCH_SEMANTIC_DECISIONS.md`.
- Bugfix triage table: `docs/VABENCH_D004_BUGFIX_TRIAGE.md`.
- PASS drift audit: `docs/EVAS_SPECTRE_PASS_DRIFT_AUDIT.md`.
- P2 metric/tolerance policy: `docs/VABENCH_P2_TOLERANCE_POLICY.md`.
- Conformance backlog: `docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md`.
- Stable checker helpers: `runners/main120_stable_checks.py`,
  `runners/p2_metric_helpers.py`.

## Implementation Touchpoints

The current strategy is not complete until these code paths enforce it:

| Area | Files | Required work |
| --- | --- | --- |
| Metadata schema | `schemas/task.schema.json`, `schemas/conformance.schema.json`, `tests/test_meta_schema.py` | Add and validate vaBench task fields: `asset_type`, `benchmark_split`, `release_form`, `provenance_status`, `source_main120_id`, `badcase_origin`, and count flags; keep conformance on a separate schema. |
| Policy helper | `runners/vabench_policy.py`, `tests/test_vabench_policy.py`, `tests/test_task_count_filters.py` | Centralize count filtering and provenance validation so generation, scoring, and gold validation share the same hard gates. |
| Main120 materialization | `runners/materialize_main120_inventory.py` | Emit D001-D008 metadata fields and block incomplete promotion states. |
| Legacy migration path | `runners/migrate_veriloga_evals.py` | Keep older metadata writers compatible with the new promotion contract if they remain in use. |
| Stable checker contracts | `runners/main120_stable_checks.py`, `tests/test_p1_checker_hardening.py` | Extend current P1 checker hardening beyond the four already covered tasks when new P1/P2 cases are promoted. |
| Runtime checker wiring | `runners/simulate_evas.py` | Route materialized tasks to D001-safe checkers instead of row-count/final-row logic. |
| P2 metric helpers | `runners/p2_metric_helpers.py`, `tests/test_p2_metric_helpers.py` | Reuse time-weighted, edge-count, window-mean, and tolerance helpers for P2 release checks. |
| Drift/action mapping | `runners/audit_evas_spectre_pass_drift.py` | Keep drift classes aligned with reconstructed bugfix rows and conformance split. |

Current implementation gap: the D001-D008 policy is documented, but schema and
materialization do not yet enforce all required provenance fields. Phase 0 must
close this gap before scaling task generation.

## Work Order

### Phase 0: Freeze Promotion Contract

Goal: make the source-task schema reflect D001-D008 before generating more
tasks.

Tasks:

1. Define required metadata fields for promoted main120 tasks:
   - `asset_type: vabench_task`
   - `benchmark_split: vabench-main-v1`
   - `family`
   - `category`
   - `domain`
   - `release_form`
   - `provenance_status`
   - `source_main120_id`
   - `badcase_origin` for reconstructed bugfix tasks
   - `counts.model_capability`
   - `counts.benchmark_coverage`
   - `counts.bugfix_claim`
2. Define allowed values:
   - `release_form`: `normal`, `true-bugfix`, `behavior-regression`,
     `evidence-only`
   - `provenance_status`: `clean`, `badcase_available`,
     `historical_bugfix_fixed_only`, `reconstructed_badcase`,
     `provenance_incomplete`
3. Define a separate conformance metadata contract outside normal vaBench task
   metadata:
   - `asset_type: evas_spectre_conformance`
   - `suite: evas-spectre`
   - `conformance_axis`
   - `expected_relation`
   - `origin.source_main120_id`
   - `minimality_note`
   - count flags that all evaluate to `false` for vaBench model capability.
4. Update materialization scripts/schema checks to require these fields for
   main120-derived tasks and to reject conformance assets from normal task
   aggregators.

Acceptance criteria:

- A missing `release_form` or `provenance_status` blocks promotion.
- A `family=bugfix` task without buggy/fixed evidence is rejected unless it is
  explicitly marked `evidence-only`.
- A conformance case cannot be stored under `tasks/` or counted in normal
  vaBench capability, coverage, or bugfix denominators.
- `evidence-only` rows are allowed in manifests but hard-excluded from public
  benchmark pass-rate denominators.

### Phase 1: D001 Checker Normalization

Goal: convert known shallow observables into robust release checker contracts.

Priority cases:

| Group | Current issue | Required replacement |
| --- | --- | --- |
| `barrel_pointer_window` | raw state/high sample counts | fixed safe-time state sequence |
| `element_shuffler` | raw high rows per output | fixed safe-time active-output sequence |
| `rotating_element_selector` | raw high rows per output | fixed safe-time active-output sequence |
| `strongarm_comparator_behavior` | row fraction and boundary stop sensitivity | fixed decision samples away from boundaries |
| `edge_detector`, `one_shot_timer`, `lock_detector` | row fractions | edge count and time-weighted pulse/lock duration |

Tasks:

1. Materialize checks for P1/P2-exposed tasks using
   `main120_stable_checks.py` and `p2_metric_helpers.py` patterns.
2. Remove release pass/fail dependence on:
   - raw row count,
   - high rows / total rows,
   - exact notes string equality,
   - final saved row at source or clock transition boundary.
3. Add regression tests proving checker decisions are stable across current
   EVAS/Spectre CSVs.
4. Reject out-of-range sample times rather than silently extrapolating from the
   first or last saved row.
5. For pulse/window tasks, add at least one interval-level assertion such as
   no extra pulses, minimum dwell time, transition count, or stop-time
   perturbation stability.

Acceptance criteria:

- P1 cases produce identical semantic notes across EVAS/Spectre historical CSVs.
- P2 cases use documented tolerances and time-weighted/windowed metrics.
- Tests fail if a checker reintroduces row-count or final-row-only logic for
  release decisions.
- Tests fail if a release checker samples outside the saved waveform range and
  accepts an extrapolated value.

### Phase 2: D004 Bugfix Reconstruction

Goal: preserve `bugfix` as a real repair task family by adding or recovering
`dut_buggy.va` for fixed-only historical bugfix rows.

Per-row workflow:

1. Read fixed DUT, TB, checker notes, and category.
2. Propose one realistic single-root-cause bug.
3. Create `dut_buggy.va` and keep the fixed source as `dut_fixed.va`.
4. Verify:
   - `dut_buggy.va` compiles if the task is a behavioral bugfix rather than a
     syntax bugfix;
   - for behavioral bugfixes, EVAS and Spectre both fail the buggy source on
     the public checker;
   - for syntax bugfixes, backend-specific compile expectations are recorded;
   - EVAS and Spectre both pass the fixed source before release.
5. Record metadata:
   - `release_form: true-bugfix`
   - `provenance_status: reconstructed_badcase`
   - `badcase_origin: reconstructed`
   - `source_main120_id: <original vbm1_*_bugfix>`
6. Record a reconstruction dossier:
   - one-root-cause diff summary;
   - historical clue or rationale;
   - why the case is not a conformance-only semantic;
   - buggy/fixed EVAS and Spectre evidence;
   - reviewer signoff.

Pilot batch:

| Priority | Task | Proposed bug class |
| --- | --- | --- |
| 1 | `vbm1_cdac_calibration_bugfix` | wrong trim update direction, missing clamp, or wrong reset level |
| 2 | `vbm1_barrel_pointer_window_bugfix` | off-by-one pointer update or wrong two-window mapping |
| 3 | `vbm1_edge_detector_bugfix` | wrong edge polarity or missing timer clear |
| 4 | `vbm1_pfd_reset_race_bugfix` | missing both-high reset or wrong reset order |
| 5 | `vbm1_segmented_dac_bugfix` | unary/binary weighting or monotonicity bug |

Acceptance criteria:

- Each reconstructed bug has a written one-root-cause explanation.
- The checker distinguishes buggy fail from fixed pass.
- The bug is plausible and not contrived solely to preserve the label.
- Bugfix claim counts include only rows with buggy-fail and fixed-pass evidence.
- User manually approves the first 3-5 reconstructed badcases before scaling to
  the remaining fixed-only rows.

### Phase 3: Conformance Suite Split

Goal: move EVAS/Spectre semantic tests out of normal vaBench capability
statistics.

Initial conformance targets:

| Priority | Case | Axis |
| --- | --- | --- |
| P0 | empty control branch | Spectre syntax legality |
| P0 | uncontinued multiline source/PWL | Spectre source syntax |
| P0 | `$abstime` continuous decay | solver-time sampling |
| P0 | `timer(0)+transition` startup | initial event ordering |
| P1 | source-edge/final-boundary behavior | endpoint/breakpoint policy |
| P1 | row-fraction checker hazard | checker semantic, not simulator physics |

Tasks:

1. Create or formalize a separate conformance directory/suite:
   `conformance/evas-spectre/`.
2. For each case, write a minimal source/TB pair with one intended failure
   cause.
3. Define expected relation:
   - EVAS and Spectre both accept,
   - EVAS and Spectre both reject,
   - or EVAS waveform matches Spectre within a defined tolerance.
4. For both-reject cases, store a diagnostic class or log-signature expectation
   so equal rejection does not hide unrelated root causes.
5. Add report generation for conformance pass matrix under a separate report
   root such as `reports/evas-spectre-conformance/<run-id>/`.

Acceptance criteria:

- Each conformance case has exactly one named semantic axis.
- A conformance failure gives a precise diagnosis without requiring broad
  benchmark debugging.
- Conformance results are reported separately from vaBench model pass rates.
- Normal vaBench runners and aggregators reject `asset_type:
  evas_spectre_conformance`.

### Phase 4: Materialize Source Tasks

Goal: convert main120 evidence into editable source-controlled tasks in batches.

Batch order:

1. P1/D001-exposed tasks:
   - `barrel_pointer_window`
   - `element_shuffler`
   - `rotating_element_selector`
   - `strongarm_comparator_behavior`
2. D004 pilot bugfix reconstructions:
   - `cdac_calibration`
   - `barrel_pointer_window`
   - `edge_detector`
   - `pfd_reset_race`
   - `segmented_dac`
3. P2/tolerance-exposed tasks:
   - `edge_detector`
   - `one_shot_timer`
   - `lock_detector`
   - `first_order_lowpass`
   - `leaky_hold`
   - `resettable_integrator`
4. Remaining main120 rows, 20-40 tasks per batch.

Each task must include:

- `prompt.md`
- `meta.json`
- `checks.yaml`
- `gold/` sources
- EVAS evidence path or fresh result pointer
- Spectre evidence path or fresh result pointer when paper-facing

Acceptance criteria:

- No promoted task is missing prompt/meta/checks/gold.
- `prompt.md` describes behavior without leaking gold implementation.
- `checks.yaml` expresses D001-safe observables.
- `meta.json` records D002-D004 provenance/release semantics.
- `prompt.md` exposes intended circuit behavior and public observables without
  leaking checker-only sample points, private state variable names, or the exact
  reconstructed patch.

### Phase 5: Validation Gates

Goal: verify each promoted batch before it becomes paper-facing.

Gate order:

1. Static/schema integrity.
2. Checker unit tests.
3. Strict EVAS gold validation.
4. EVAS/Spectre dual smoke for the changed batch.
5. Family slice dual run.
6. Full source-backed parity gate when enough tasks have been materialized.

Hard stop conditions:

- Any EVAS PASS / Spectre FAIL on an audited source task.
- Any public `bugfix` whose buggy source also passes.
- Any public behavioral `bugfix` whose buggy source was not run through both
  EVAS and Spectre.
- Any checker relying on row count, row fraction, exact notes, or final-row
  boundary value for release decisions.
- Any conformance task mixed into normal vaBench capability statistics.
- Any report denominator that includes `evidence-only` rows as released tasks.

### Phase 6: Paper-Facing Reports

Goal: produce clean evidence for the benchmark/evaluator story.

Reports:

1. vaBench coverage table:
   - by family,
   - category,
   - release form,
   - provenance status.
2. Bugfix provenance table:
   - original badcase,
   - reconstructed badcase,
   - evidence-only,
   - excluded/conformance.
3. EVAS/Spectre parity table:
   - binary agreement,
   - P1 resolved,
   - P2 tolerance/watchlist.
4. Conformance table:
   - syntax,
   - source parsing,
   - event scheduling,
   - solver-time sampling,
   - checker semantics.
5. Denominator audit:
   - row-level statistics;
   - base-clustered statistics, because main120 has multiple task forms per
     underlying circuit family.

Acceptance criteria:

- Every paper claim links to a source task, validation artifact, or conformance
  regression.
- Bugfix claim counts only tasks with bad/fixed evidence.
- EVAS claim separates broad benchmark parity from atomic conformance coverage.
- `evidence-only` appears only in provenance/manifests, not in public pass-rate
  denominators.

## Immediate Next Actions

1. Add schema/materialization support for vaBench `asset_type`, `release_form`,
   `provenance_status`, `badcase_origin`, and count flags.
2. Materialize the four D001 P1 bases first.
3. Reconstruct and manually review the five D004 pilot badcases.
4. Create the first conformance pack from the four P0 semantic cases under a
   separate conformance root.
5. Promote the D005 P2 tolerance rows with documented metric helpers.
6. Run EVAS-only validation for the materialized slice, then Spectre dual smoke
   once bridge readiness is confirmed.

## Open Review Points

- Whether reconstructed badcases should be generated under `gold/` as
  `dut_buggy.va` / `dut_fixed.va` for every bugfix task.
- Whether behavior-regression fallback rows should be included in the public
  benchmark immediately or kept evidence-only until the true bugfix pass is
  complete.
- Exact numeric tolerances for each P2 continuous-valued metric after the first
  representative EVAS/Spectre validation run.
