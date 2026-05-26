# vaBench Content Audit Test Plan

Date: 2026-05-25

This plan defines the review tests needed before treating
`benchmark-vabench-release-v1` as a paper-facing benchmark. It is a
content-quality audit, not an EVAS/Spectre certification report. Dual
simulation can show that packaged gold and checkers agree; it cannot prove that
the public prompt is the right analog/mixed-signal circuit problem.

Current release target:

- 64 content entries.
- 51 core circuit entries plus 13 measurement/stimulus support entries.
- 51 L1 entries and 13 L2 entries.
- 8 release categories.
- Score denominator remains disabled until fresh full EVAS/Spectre dual
  certification is complete.

Core review questions:

1. Is the top-level circuit-function table internally consistent and useful for
   an analog Verilog-A benchmark, not just an EVAS demo?
2. For each materialized task, do `prompt.md`, `checks.yaml`, and `gold/`
   describe the same circuit function?
3. For each L2 row, does the checker validate a composed flow or a meaningful
   measurement/stimulus support flow, rather than a single shallow observable?
4. Are support categories reported separately from the 51-entry core circuit
   denominator?

## Inputs

| Input | Role |
| --- | --- |
| `docs/VABENCH_RELEASE_TAXONOMY.md` | Normative top-level L0/L1/L2 taxonomy and release coverage contract. |
| `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` | Human-readable category/level coverage view. |
| `docs/VABENCH_BASE_FUNCTION_REGISTRY.md` | Current merge/remove decisions and high-risk wording decisions. |
| `docs/VABENCH_RELEASE_COMPLETED_CONTENTS.md` | Completed content inventory by category, level, and form. |
| `docs/VABENCH_TOPLEVEL_POSITIONING.md` | Paper-facing core/support split and claim boundary. |
| `docs/VABENCH_L2_CLAIM_MAPPING_AUDIT.md` | Human claim map for the 13 L2 entries. |
| `benchmark-vabench-release-v1/MANIFEST.json` | Machine-readable release package manifest. |
| `benchmark-vabench-release-v1/tasks/*/vbr1_*/release_entry.json` | Per-entry category, level, base function, forms, assets, and evidence links. |
| `benchmark-vabench-release-v1/tasks/CT*/vbr1_*/forms/*/{prompt.md,meta.json,checks.yaml,gold/}` | Public task contracts, checkers, and reference assets. |
| `benchmark-vabench-release-v1/evidence/{static,dual}/...` | Certification evidence for packaged forms. |
| `benchmark-vabench-release-v1/reports/{manifest,dual_certification,score_denominator_manifest,claim_gate}.json` | Reported package, certification, scoring, and claim-gate state. |

## Audit Gate A: Top-Level Function Table and L1/L2 Design

### A1. Denominator Consistency

Purpose: prevent paper-facing counts from drifting across docs, manifest, and
reports.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Package manifest entry count equals package asset target. | `64` release entries. | Block package-integrity claims; reconcile taxonomy or package. |
| Content denominator matches the audited target. | `64` entries: `51` core circuit entries and `13` support entries. | Block distinct-function benchmark claims. |
| Level split matches current release. | `51` L1 and `13` L2. | Fix manifest/docs or reclassify entries. |
| Category set has exactly the release taxonomy categories. | 8 categories, no legacy-only categories. | Rename, merge, or remap entries. |
| Completed-content table agrees with manifest counts. | Same entry/form totals and category counts. | Regenerate or correct docs. |
| L0 conformance cases are outside the L1/L2 denominator. | `counted_in_score=false`, separate conformance report. | Move row to conformance or reclassify. |
| Score denominator is disabled until fresh dual certification. | No counted score rows while EVAS/Spectre is pending. | Block score reporting. |

Human review:

- Check whether each category is a recognizable analog/mixed-signal behavioral
  circuit or support role, not a historical artifact.
- Check whether any category is inflated by easy variants.
- Check whether support categories are useful for Verilog-A benchmark practice
  without being counted as core circuit-function coverage.

### A2. Core / Support Split

Purpose: keep the paper's main claim about analog circuit functions separate
from reusable measurement and stimulus infrastructure.

Current split:

| Role | Categories | Count |
| --- | --- | --- |
| Core circuit entries | Data Converter Models; Comparator and Decision Circuits; Sampling and Analog Memory; Baseband Signal Conditioning; PLL Clock and Timing Systems; Calibration, DEM, and Control | 51 |
| Support entries | Measurement Instrumentation Flows; Stimulus and Source Generators | 13 |

Audit rules:

- Core entries can support the main benchmark-function count.
- Support entries can support "Verilog-A benchmark infrastructure coverage",
  "testbench/measurement modeling", or "stimulus/source modeling" claims.
- Support entries must not inflate the core circuit denominator.
- Any paper table that lists all 64 entries should visibly separate `51 core`
  from `13 support`.

### A3. Function Uniqueness and Naming

Purpose: avoid counting the same circuit function twice under different names.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Normalized `base_function` names are unique inside the package unless explicitly marked as a variant. | No accidental duplicates. | Merge, rename, or mark as distinct variant with rationale. |
| Excluded historical bases are absent from the release denominator. | Removed/merged rows are not counted. | Remove from denominator or redesign. |
| Known renamed functions use release wording, not misleading historical wording. | Binary DAC is not publicly called thermometer DAC; support categories are named as support. | Fix prompt/meta/checks/reports. |
| `source_base_id` duplication is explained by merge or companion-form policy. | No unexplained many-entry reuse. | Add merge note or split function. |

Human review:

- For near-duplicates, decide whether the distinction is electrical/behavioral
  enough to count.
- Count binary DAC and unit-element thermometer DAC separately only if the
  latter uses actual unary segment behavior.
- Count trim-voltage generator and gain trim controller separately only if
  their observable role and update law differ.
- Count support measurement/stimulus rows only when they add reusable
  Verilog-A benchmark practice, not just another testbench wrapper.

### A4. L1 Definition Test

Purpose: ensure an L1 entry is a reusable circuit function, not a disguised
multi-block flow or pure simulator primitive.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| L1 entries have `score_surface=model-capability`. | True. | Fix manifest or reclassify. |
| L1 entries are not under conformance paths. | True. | Move to L0 conformance. |
| L1 `dut` forms, when present, expose a clear module contract. | Prompt has module, ports, directions, disciplines, ranges, and public observables. | Fix prompt template. |
| L1 entries do not depend only on isolated `cross/timer/source` semantics. | Checker has circuit behavior, not only primitive behavior. | Move primitive case to L0 or rewrite as circuit block. |

Human review:

- Confirm the base function is a recognizable block such as DAC, comparator,
  sample-and-hold, filter, limiter, clock/PLL component, source, detector, or
  controller.
- If an L1 `e2e` form includes a testbench, verify it still tests the same L1
  function rather than an unclaimed L2 chain.

### A5. L2 Complete-Flow Test

Purpose: ensure L2 entries actually compose multiple interacting functions, or
are explicitly scoped as measurement/stimulus support flows.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| L2 entries use `score_surface=benchmark-e2e`. | True. | Fix manifest or reclassify. |
| L2 entries expose only `e2e` and/or `tb` unless richer forms are justified. | No accidental L1 form expansion. | Remove unsupported forms. |
| L2 gold assets include either multiple modules or one module whose prompt/checker explicitly names a composed flow. | Composition or support-flow evidence exists. | Reclassify to L1, strengthen task, or mark support-only. |
| L2 checks include chain-level observables. | Not just compile/run/non-NaN guards. | Add behavior-specific checker items. |
| Each L2 row has a claim-mapping decision. | `keep`, `revise`, `downgrade`, or `support-only`. | Block L2 coverage claims. |

Human review:

- Confirm the L2 behavior cannot be reduced to one L1 function with a long
  testbench unless the row is explicitly support-only.
- Confirm checker measures an interaction, for example:
  - SAR ADC: sample/hold plus SAR decision plus weighted DAC feedback.
  - Static-linearity flow: quantizer plus nonideal reconstruction plus metric
    consistency, not a precomputed DNL/INL lookup.
  - PLL slice: divider/timer/control lock and reacquire behavior.
  - Signal-conditioning chain: gain plus dynamic filtering/limiting response.
  - Measurement support: metric output must be tied to waveform behavior.
  - Stimulus support: scheduled waveform segments and mode continuity must be
    observable.

### A6. Coverage Balance and Scope Boundary

Purpose: avoid a release that is numerically complete but conceptually skewed.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Every release category has at least one L1 entry. | True. | Add content or remove category. |
| Every core category has L2 coverage if the taxonomy claims complete-flow coverage there. | True for the current 64-entry target. | Add L2 or narrow claim. |
| Support categories are clearly marked as support. | True. | Fix taxonomy/report/paper wording. |
| All entries stay in pure voltage-domain behavioral Verilog-A scope. | No unsupported current-domain/KCL/KVL/device-level/AC/noise claim. | Rewrite or remove row. |
| Score remains disabled while fresh dual certification is pending. | `counted_in_score=false`. | Block score reporting. |

Human review:

- Check whether 64 entries cover enough distinct analog/mixed-signal behavior
  to support the benchmark claim.
- Check whether CT01 data converters are overrepresented relative to other
  core categories.
- Check whether small categories need stronger representative entries rather
  than more variants.

## Audit Gate B: Prompt / Checker / Gold Alignment

### B1. Public Prompt Contract Test

Purpose: make sure a model can solve the task from public information without
seeing private gold implementation.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Prompt names required output artifact(s). | Exact filenames listed. | Fix prompt. |
| Prompt declares module name and port order where a `.va` is expected. | Explicit module declaration or equivalent port list. | Fix prompt. |
| Prompt declares port direction and electrical discipline. | Inputs/outputs and `electrical` listed. | Fix prompt. |
| Prompt lists saved waveform columns or public observables. | Present for `tb` and `e2e`; present where DUT behavior depends on probes. | Fix prompt/checker. |
| Prompt does not rely on "preserve ports" before defining ports. | No ambiguous preservation language. | Fix prompt. |
| Prompt does not leak the full reference implementation. | No copied gold netlist/module body. | Rewrite prompt. |

Human review:

- Decide whether the prompt describes the intended circuit function, not just
  the checker's easiest route to pass.
- Flag misleading historical names or claims that turn support rows into core
  circuit rows.

### B2. Artifact Contract by Form

Purpose: keep public/private boundaries fair across `dut`, `tb`, `bugfix`, and
`e2e`.

| Form | Public input should contain | Model output should contain | Private/evidence only |
| --- | --- | --- | --- |
| `dut` | `prompt.md` | DUT `.va` | reference DUT, reference TB, EVAS/Spectre evidence |
| `tb` | `prompt.md` and reference DUT interface | TB `.scs` or declared TB artifact | gold TB and evidence |
| `bugfix` | `prompt.md`, `gold/dut_buggy.va` | `dut_fixed.va` | reference fixed solution and evidence |
| `e2e` | `prompt.md` | declared system artifacts | reference system and evidence |

Failure action:

- Fix `meta.json`, `release_task.json`, and generated reports.
- Do not release bugfix tasks where the fixed solution is public input.

### B3. Gold Behavior Matches Base Function

Purpose: make sure the reference implementation is the circuit promised by the
taxonomy and prompt.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Gold module name matches prompt and meta artifacts. | Match. | Fix prompt or gold naming. |
| Gold ports match prompt order and direction. | Match. | Fix prompt/gold wrapper. |
| Gold uses only supported Verilog-A subset for release rows. | No unsupported current-domain or transistor-level constructs. | Move out of scope or rewrite. |
| Gold assets referenced by evidence are the same files in the package. | Source equivalence pass. | Regenerate evidence. |

Human review:

- Read the gold `.va` and classify the actual behavior in one sentence.
- Compare that sentence to `base_function` and the first paragraph of
  `prompt.md`.
- If they differ, the task is quarantined even if EVAS/Spectre both pass.

Review examples:

| Risk | What to check |
| --- | --- |
| Binary DAC vs thermometer DAC | Does gold implement `code/15`, or actual unit-element thermometer segments? |
| Calibration controller duplication | Is the update law materially different from adjacent calibration entries? |
| Measurement task drift | Does gold write or expose a metric artifact that the prompt asks for and checker validates? |
| VCO/PLL startup artifacts | Is benchmark behavior about final phase/frequency, while startup sample quirks stay in L0 conformance? |
| Stimulus source overclaim | Is the waveform schedule itself the target, not a hidden downstream circuit? |

### B4. Checker Semantics Match Prompt and Gold

Purpose: ensure the checker validates the declared circuit function, not only
that simulation completed.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| `checks.yaml` has `sim_correct` and `parity`. | Present. | Fix checks. |
| `sim_correct` items name function-level behavior. | Not just `runs` or `done`. | Strengthen checker. |
| Checker observables are mentioned in the prompt. | No hidden public requirement. | Fix prompt or checker. |
| Metric/file side effects are explicitly specified. | File name, schema, and tolerance declared. | Fix prompt/checker. |
| Evidence results reference the same checker intent. | Dual evidence pass under same behavior checker. | Regenerate or quarantine. |

Human review:

- For each task, ask: "Could a wrong implementation pass this checker by
  exploiting a shallow observable?"
- If yes, add a concrete missed behavior window, such as monotonicity, reset,
  clamp, signed movement, edge ordering, mode schedule, metric/waveform
  consistency, or lock/reacquire behavior.

### B5. Bugfix Badcase Validity

Purpose: ensure `bugfix` is a real repair benchmark, not a disguised normal
task or infrastructure failure.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| `dut_buggy.va` and `dut_fixed.va` both exist. | True. | Remove bugfix form or add companion. |
| Buggy case compiles/runs in EVAS and Spectre. | True. | Does not count as expected buggy-fail. |
| Buggy case fails behavioral correctness in EVAS and Spectre. | True. | Redesign badcase or reclassify. |
| Fixed case passes behavioral correctness in EVAS and Spectre. | True. | Fix reference or checker. |
| Failure label is behavior-level, not bridge, missing waveform, compile, or TB infrastructure. | True. | Quarantine as infrastructure issue. |

Human review:

- Confirm the bug type is pedagogically meaningful for Verilog-A behavioral
  modeling, such as reset priority, sign/direction error, saturation boundary,
  event ordering, pointer wrap, or missing transition.

### B6. Evidence Freshness and Source Equivalence

Purpose: avoid stale imported evidence certifying a different source triple.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Static evidence exists for every materialized form. | Pass. | Run static certification. |
| EVAS and Spectre evidence exists for every materialized form. | Pass. | Run dual certification. |
| EVAS PASS / Spectre FAIL count is zero. | Zero. | Fix EVAS, checker, or row. |
| Evidence source hashes or source-equivalence report match current package files. | Pass. | Regenerate evidence. |
| Imported historical rows are labeled and not over-claimed as fresh reruns unless rerun evidence exists. | True. | Fix report status. |

Human review:

- For rows marked as imported or historical, inspect whether the source is still
  exactly the same as the package source.
- Do not convert partial imports into final release certification.

## Proposed Review Order

| Phase | Scope | Why first |
| --- | --- | --- |
| P0 | All 13 L2 entries in `docs/VABENCH_L2_CLAIM_MAPPING_AUDIT.md`. | L2 is easiest to over-claim; checker must prove interaction or explicit support-flow behavior. |
| P1 | High-risk L1 and support entries. | Known wording or semantic risks can corrupt benchmark interpretation. |
| P2 | One representative row per category and form. | Verifies prompt/check/gold template consistency across categories. |
| P3 | Remaining L1 entries by category. | Completes coverage after risky cases are resolved. |

High-risk L1/support queue:

| Entry | Review focus |
| --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac` | Public wording must say binary-weighted DAC, not thermometer DAC. |
| `vbr1_l1_unit_element_thermometer_dac` | Must use fifteen unit-element thermometer-coded segments including full-scale `seg14` behavior. |
| `vbr1_l1_crossing_metric_writer` | Metric output must match waveform crossing time within tolerance. |
| `vbr1_l1_settling_time_detector` | Tolerance band, settle window, and metric semantics must be public and checker-aligned. |
| `vbr1_l1_vco_phase_integrator` | Check phase/frequency behavior; startup quirks stay L0. |
| `vbr1_l1_charge_pump_abstraction` | Must remain a voltage-domain control abstraction, not a current-domain charge-pump claim. |
| `vbr1_l1_loop_filter_abstraction` | Check update law and reset behavior, not just bounded output. |
| `vbr1_l1_trim_calibration_controller` | Must be distinct as a trim-voltage generator. |
| `vbr1_l1_gain_trim_controller` | Check signed movement, saturation, and in-range hold behavior. |
| `vbr1_l1_dwa_dem_encoder` | Check true DEM/DWA selection behavior, not only pointer smoke. |
| `vbr1_l1_precision_rectifier_envelope_detector` | Check nonlinear rectification/envelope behavior, not only positive output. |
| `vbr1_l1_programmable_gain_amplifier` | Check programmable gain behavior distinct from a fixed amplifier. |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | Keep as deterministic source support behavior; avoid stochastic/noise-analysis overclaim. |
| CT07 measurement entries | Support-only wording; metric must be tied to waveform behavior. |
| CT08 stimulus entries | Support-only wording; waveform schedule and continuity must be checked. |

## Manual Review Sheet Template

Use this per entry:

| Field | Reviewer answer |
| --- | --- |
| Entry ID |  |
| Category / level / core-support role |  |
| One-sentence intended function |  |
| One-sentence gold behavior after reading `.va` |  |
| Does prompt match intended function? | pass / revise / fail |
| Does checker validate the intended function? | pass / revise / fail |
| Does gold match prompt and checker? | pass / revise / fail |
| L1/L2/support classification correct? | pass / revise / fail |
| If bugfix, is badcase behavior-level and fair? | pass / revise / fail / n/a |
| Required action | keep / revise / downgrade / support-only / quarantine |

## Test Implementation Plan

Existing automated content audit surface:

| Artifact | Responsibility |
| --- | --- |
| `runners/audit_vabench_content_contract.py` | Read taxonomy docs, manifest, release entries, prompts, meta, checks, gold, and evidence; emit `content_contract_audit.json/md`. |
| `tests/test_vabench_content_contract.py` | Assert no blocking automated findings; keep human-review notes explicit. |

Recommended automated finding classes:

| Class | Meaning |
| --- | --- |
| `BLOCKER` | Count drift, missing artifact, L0 counted in denominator, prompt/gold port mismatch, public/private leak, stale evidence. |
| `REVIEW_REQUIRED` | Near-duplicate function, L2 composition ambiguity, checker may be shallow, misleading historical name. |
| `INFO` | Human-readable trace notes and sampling choices. |

The runner must not claim semantic correctness by itself. Human review remains
required for L2 claim mapping and high-risk L1/support interpretation.

## Commands

Run from `behavioral-veriloga-eval`:

```bash
python3 runners/report_vabench_release_schema_validation.py
python3 runners/audit_vabench_release_assets.py
python3 runners/report_vabench_release_completion_audit.py
python3 runners/audit_vabench_content_contract.py
python3 -m pytest -q \
  tests/test_vabench_release_schema_validation.py \
  tests/test_vabench_release_asset_integrity.py \
  tests/test_vabench_release_completion_audit.py \
  tests/test_vabench_content_contract.py
```

Fresh certification is a separate gate:

```bash
python3 runners/run_gold_dual_suite.py --release benchmark-vabench-release-v1
```

Use the actual release runner/options when launching the full EVAS/Spectre job;
the command above is the conceptual gate, not a substitute for the project
queue scripts.

## Stop Condition

The benchmark content audit is ready for baseline pilots only when:

- all Audit Gate A automated checks pass;
- all Audit Gate B automated checks pass;
- every L2 entry has a human `keep`, `revise-complete`, `downgrade`, or
  `support-only` decision;
- support-only rows are visibly separated from the 51-entry core circuit
  denominator;
- high-risk L1 entries have no unresolved wording/checker/gold mismatch;
- score remains disabled until fresh full EVAS/Spectre certification;
- any remaining caveat is documented as a non-blocking review note, not hidden
  inside a pass result.
