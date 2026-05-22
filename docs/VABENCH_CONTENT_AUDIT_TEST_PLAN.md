# vaBench Content Audit Test Plan

Date: 2026-05-17

This plan defines the review tests needed before treating the current
`vabench-release-v1` contents as a paper-facing benchmark. It focuses on two
questions:

1. Is the top-level circuit-function table and L1/L2 design internally
   consistent?
2. For each materialized task, do `prompt.md`, `checks.yaml`, and `gold/`
   describe the same circuit function?

This is a content-quality audit. It is separate from EVAS/Spectre certification:
dual simulation can prove that the packaged gold and checker agree, but it
cannot prove that the public task wording is the right circuit problem.

## Inputs

| Input | Role |
| --- | --- |
| `docs/VABENCH_RELEASE_TAXONOMY.md` | Normative top-level L0/L1/L2 taxonomy and release coverage contract. |
| `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` | Human-readable category/level coverage view. |
| `docs/VABENCH_BASE_FUNCTION_REGISTRY.md` | Current-seed merge/remove decisions and high-risk wording decisions. |
| `docs/VABENCH_RELEASE_COMPLETED_CONTENTS.md` | Completed content inventory by category, level, and form. |
| `benchmark-vabench-release-v1/MANIFEST.json` | Machine-readable release package manifest. |
| `benchmark-vabench-release-v1/tasks/*/release_entry.json` | Per-entry category, level, base function, forms, assets, and evidence links. |
| `benchmark-vabench-release-v1/tasks/*/forms/*/{prompt.md,meta.json,checks.yaml,gold/}` | Public task contracts, checkers, and reference assets. |
| `benchmark-vabench-release-v1/evidence/{static,dual}/...` | Certification evidence for packaged forms. |

## Audit Gate A: Top-Level Function Table and L1/L2 Design

### A1. Denominator Consistency

Purpose: prevent paper-facing counts from drifting across docs, manifest, and
reports.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Package manifest entry count equals package asset target. | `80` release entries. | Block package-integrity claims; reconcile taxonomy or package. |
| Strong content denominator matches the audited target. | `75` entries: `60` L1 and `15` non-duplicate L2. | Block distinct-function benchmark claims. |
| Category set has exactly the release taxonomy categories. | 9 categories, no legacy-only categories. | Rename or remap entries. |
| Completed-content table agrees with manifest counts. | Same entry/form totals and category counts. | Regenerate or correct docs. |
| L0 conformance cases are outside the L1/L2 denominator. | `counted_in_score=false`, separate conformance report. | Move row to conformance or reclassify. |
| Exact duplicate L2 kernels are content-excluded. | Duplicates remain as package assets only. | Rewrite or exclude before counting. |

Human review:

- Check whether each category name is an analog/mixed-signal behavioral circuit
  role, not a historical artifact.
- Check whether any category is too broad or hides duplicate circuit kernels.

### A2. Function Uniqueness and Naming

Purpose: avoid counting the same circuit function twice under different names.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Normalized `base_function` names are unique inside the package unless explicitly marked as a variant. | No accidental duplicates. | Merge, rename, or mark as distinct variant with rationale. |
| Excluded historical bases are absent from the release denominator. | `background_calibration_accumulator` and `offset_calibration_fsm` are not counted. | Remove from denominator or redesign. |
| Known renamed functions use release wording, not misleading historical wording. | Binary DAC is not publicly called thermometer DAC. | Fix prompt/meta/checks/reports. |
| `source_base_id` duplication is explained by merge or companion-form policy. | No unexplained many-entry reuse. | Add merge note or split function. |

Human review:

- For near-duplicates, decide whether the distinction is electrical/behavioral
  enough to count. Examples:
  - hard clamp vs soft/hysteretic limiter: count only if checker exercises
    different behavior.
  - binary DAC vs unit-element thermometer DAC: count separately only if the
    latter uses unit-element thermometer-coded behavior.
  - trim-voltage generator vs gain trim controller: count separately only
    if the measured update law and observable role differ.

### A3. L1 Definition Test

Purpose: ensure an L1 entry is a reusable circuit function, not a disguised
multi-block flow or pure simulator primitive.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| L1 entries have `score_surface=model-capability`. | True. | Fix manifest or reclassify. |
| L1 entries are not under conformance paths. | True. | Move to L0 conformance. |
| L1 `dut` forms, when present, expose a clear module contract. | Prompt has module, ports, directions, disciplines, and ranges. | Fix prompt template. |
| L1 entries do not depend only on isolated `cross/timer/source` semantics. | Checker has circuit behavior, not only primitive behavior. | Move primitive case to L0. |

Human review:

- Confirm the base function is a recognizable circuit block, such as DAC,
  comparator, clock divider, sample-and-hold, filter, source, detector, or
  controller.
- If an L1 `e2e` form includes a testbench, verify it is still testing the same
  L1 function rather than an L2 chain.

### A4. L2 Complete-Circuit Test

Purpose: ensure L2 entries actually compose multiple interacting functions.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| L2 entries use `score_surface=benchmark-e2e`. | True. | Fix manifest or reclassify. |
| L2 entries expose only `e2e` and/or `tb` unless a richer form is deliberately justified. | No accidental L1 form expansion. | Remove unsupported forms. |
| L2 gold assets include either multiple modules or one module whose prompt/checker explicitly names a composed flow. | Composition evidence exists. | Reclassify to L1 or strengthen task. |
| L2 checks include chain-level observables. | Not just generic compile/sim/run guards. | Add chain-specific checker items. |

Human review:

- Confirm the L2 behavior cannot be reduced to one L1 function with a long
  testbench.
- Confirm checker measures an interaction, for example:
  - SAR ADC: comparator + DAC feedback + SAR code convergence.
  - PLL slice: PFD/divider/VCO or loop-control interaction.
  - signal-conditioning chain: gain plus filtering/limiting response, not just
    final non-NaN output.

### A5. Coverage Balance and Scope Boundary

Purpose: avoid a release that is numerically complete but conceptually skewed.

Automated checks:

| Check | Expected result | Failure action |
| --- | --- | --- |
| Every release category has at least one L1 entry. | True. | Add or remove category. |
| Every release category has L2 coverage if the taxonomy claims complete-circuit coverage there. | True for the current 80-entry target. | Add L2 or narrow claim. |
| All entries stay in pure voltage-domain behavioral Verilog-A scope. | No unsupported current-domain/KCL/KVL claim. | Rewrite or remove row. |
| Score remains disabled while audit is open. | `counted_in_score=false`. | Block score reporting. |

Human review:

- Check whether 80 entries cover enough distinct analog/mixed-signal behavior
  to support the benchmark claim.
- Check whether any category is underrepresented or inflated by easy variants.

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
- Flag misleading historical names, such as a binary DAC task retaining
  thermometer-DAC wording.

### B2. Artifact Contract by Form

Purpose: keep public/private boundaries fair across `dut`, `tb`, `bugfix`, and
`e2e`.

Automated checks:

| Form | Public input should contain | Model output should contain | Private/evidence only |
| --- | --- | --- | --- |
| `dut` | `prompt.md` | DUT `.va` | reference DUT, reference TB, EVAS/Spectre evidence |
| `tb` | `prompt.md` and reference DUT interface | TB `.scs` or declared TB artifact | gold TB and evidence |
| `bugfix` | `prompt.md`, `gold/dut_buggy.va` | `dut_fixed.va` | reference fixed solution and evidence |
| `e2e` | `prompt.md` | declared system artifacts | reference system and evidence |

Failure action:

- Fix `meta.json`, `release_task.json`, and generated reports.
- Do not release bugfix tasks where the fixed solution is public input.

Human review:

- For bugfix tasks, confirm the buggy source is a realistic repair problem and
  not a synthetic one-line trick unless the task explicitly targets that bug
  class.

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
| Calibration controller duplication | Is the update law materially different from `cdac_calibration`, or just the same signed accumulator? |
| Measurement task drift | Does gold write a metric artifact that the prompt asks for and checker validates? |
| VCO/PLL startup artifacts | Is benchmark behavior about final phase/frequency, while startup sample quirks stay in L0 conformance? |

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
  clamp, signed movement, edge ordering, or metric/waveform consistency.

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
- A good fixed solution may correspond to multiple possible badcases; that is
  acceptable only if the released badcase is specific, realistic, and
  behavior-checked.

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

## Proposed Review Order

| Phase | Scope | Why first |
| --- | --- | --- |
| P0 | All 20 L2 entries. | L2 is easiest to over-claim; checker must prove interaction, not just component behavior. |
| P1 | High-risk L1 entries. | Known wording or semantic risks can corrupt benchmark interpretation. |
| P2 | One representative row per category and form. | Verifies template consistency across categories. |
| P3 | Remaining L1 entries by category. | Completes coverage after the risky cases are resolved. |

High-risk L1 queue:

| Entry | Review focus |
| --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac` | Public wording must say binary-weighted DAC, not thermometer DAC. |
| `vbr1_l1_unit_element_thermometer_dac` | Must actually use unit-element thermometer-coded behavior. |
| `vbr1_l1_crossing_metric_writer` | Metric file must match waveform crossing time. |
| `vbr1_l1_settling_time_detector` | Define tolerance band, settle window, and metric semantics. |
| `vbr1_l1_vco_phase_integrator` | Benchmark should check phase/frequency behavior; startup quirks stay L0. |
| `vbr1_l1_charge_pump_abstraction` | Voltage-domain abstraction must not over-claim current-domain simulation. |
| `vbr1_l1_loop_filter_abstraction` | Check proportional/integral update semantics, not just bounded output. |
| `vbr1_l1_pfd_dead_zone_model` | Treat as PFD small-phase-error response; avoid making simulator threshold conformance replace circuit-level PFD behavior. |
| `vbr1_l1_trim_calibration_controller` | Confirm distinctness from merged calibration accumulator evidence. |
| `vbr1_l1_gain_trim_controller` | Confirm signed gain-control movement and saturation behavior. |

Current semantic audit status:

The current content audit has 0 `REVIEW_REQUIRED` findings. The former
remaining high-risk entries were cleared by tightening their public checks and
their executable behavior checkers:

| Entry | Resolution evidence |
| --- | --- |
| `vbr1_l1_loop_filter_abstraction` | Dedicated checker now verifies proportional step decay, integral residual behavior, metric timing after valid updates, reset clearing, and bounded output. |
| `vbr1_l1_gain_trim_controller` | Stimulus now drives sustained low/high measurement windows, and the checker verifies reset, signed control movement, upper clamp, lower clamp, and in-range behavior. |

Resolved wording-only items in this pass:

| Entry | Resolution |
| --- | --- |
| `vbr1_l1_charge_pump_abstraction` | Public function name is now "Voltage-domain charge-pump control abstraction"; prompt and taxonomy explicitly exclude current contributions, KCL/KVL assumptions, and transistor-level charge-pump claims. |
| `vbr1_l1_settling_time_detector` | Public function name is now "Settling response measurement helper"; exact 120 ns event ordering remains an EVAS/Spectre conformance matter rather than the benchmark function. |
| `vbr1_l1_trim_calibration_controller` | Public function name is now "Trim-voltage generator"; it is explicitly a calibration accumulator that drives `trim`, not a full capacitor-array CDAC model. |
| `vbr1_l1_unit_element_thermometer_dac` | Public function name remains unit-element thermometer DAC; prompt/checker/gold all require fifteen unary segments including `seg14`, so it is distinct from the simple binary-coded DAC. |
| `vbr1_l1_crossing_metric_writer` | Public checker requires a single `metric.out` record matching waveform crossing time within tolerance; file I/O atomicity remains L0 conformance rather than a circuit-function claim. |

Function-checked DUT companion resolution:

The former 14 auxiliary `dut` companion forms have been promoted only after
adding function-level EVAS checker aliases, replacing generic checks, and
rewriting public prompts with explicit module/port/observable contracts.

Resolved in this pass: `vbr1_l1_burst_clock_source`,
`vbr1_l1_clocked_adc_quantizer`, `vbr1_l1_resettable_sample_and_hold`
(historical ID; public function is now clocked sample-and-hold), and the 14
entries below now expose function-level DUT prompts and checks.

| Entry | Current status | Strong-checker direction |
| --- | --- | --- |
| `vbr1_l1_clocked_comparator` | Function-checked DUT. | Check reset/evaluate phases, threshold decision, and output transition timing. |
| `vbr1_l1_differential_output_driver` | Function-checked DUT. | Check complementary outputs, common-mode, swing, and sign relation. |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | Function-checked DUT. | Check phase increment, wrap, and output event relation. |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | Function-checked DUT. | Check nonconstant dither/noise deviation from input. |
| `vbr1_l1_dwa_dem_encoder` | Function-checked DUT. | Check one-hot pointer rotation, latched-code cell span, and wrap behavior. |
| `vbr1_l1_hysteresis_comparator` | Function-checked DUT. | Check separate rising/falling thresholds and state retention inside hysteresis band. |
| `vbr1_l1_pfd_dead_zone_model` | Function-checked DUT. | Check small phase-error UP/DN behavior without reducing it to exact threshold conformance. |
| `vbr1_l1_propagation_delay_comparator` | Function-checked DUT. | Check threshold decision after delay and delay dependence on input difference. |
| `vbr1_l1_ramp_or_step_source` | Function-checked DUT. | Check phase ramp, period wrap, and guard pulse width. |
| `vbr1_l1_serializer_frame_aligner` | Function-checked DUT. | Check frame boundary, serial order, and bounded frame pulse. |
| `vbr1_l1_threshold_comparator` | Function-checked DUT. | Check low/high threshold decisions and transition boundedness. |
| `vbr1_l1_unit_element_thermometer_dac` | Function-checked DUT. | Check 15 unit elements, monotonic thermometer-code activation, endpoint scaling, and full-scale `seg14` coverage. |
| `vbr1_l1_window_comparator_detector` | Function-checked DUT. | Check inside-window versus outside-window states with two thresholds. |
| `vbr1_l1_xor_phase_detector` | Function-checked DUT. | Check phase/duty relationship, XOR high-time, and bounded output. |

## Manual Review Sheet Template

Use this per entry:

| Field | Reviewer answer |
| --- | --- |
| Entry ID |  |
| Category / level |  |
| One-sentence intended circuit function |  |
| One-sentence gold behavior after reading `.va` |  |
| Does prompt match intended function? | pass / revise / fail |
| Does checker validate the intended function? | pass / revise / fail |
| Does gold match prompt and checker? | pass / revise / fail |
| L1/L2 classification correct? | pass / revise / fail |
| If bugfix, is badcase behavior-level and fair? | pass / revise / fail / n/a |
| Required action | keep / rename / strengthen checker / reclassify / quarantine |

## Test Implementation Plan

Add one content-audit runner and one pytest wrapper:

| Artifact | Responsibility |
| --- | --- |
| `runners/audit_vabench_content_contract.py` | Read taxonomy docs, manifest, release entries, prompts, meta, checks, gold, and evidence; emit `content_contract_audit.json/md`. |
| `tests/test_vabench_content_contract.py` | Assert no blocking automated findings; allow human-review warnings to remain explicit. |

Recommended automated finding classes:

| Class | Meaning |
| --- | --- |
| `BLOCKER` | Count drift, missing artifact, L0 counted in denominator, prompt/gold port mismatch, public/private leak, stale evidence. |
| `REVIEW_REQUIRED` | Near-duplicate function, L2 composition ambiguity, checker may be shallow, misleading historical name. |
| `INFO` | Human-readable trace notes and sampling choices. |

The runner should not claim semantic correctness by itself. Its final status
should be:

| Status | Meaning |
| --- | --- |
| `pass` | No automated blockers and no required human-review queue remains. |
| `review_required` | No automated blockers, but semantic review rows remain. |
| `fail` | At least one automated blocker exists. |

## Commands

Current structural checks to run before the new content audit:

```bash
cd behavioral-veriloga-eval
python3 runners/report_vabench_release_schema_validation.py
python3 runners/audit_vabench_release_assets.py
python3 runners/report_vabench_release_completion_audit.py
pytest -q \
  tests/test_vabench_release_schema_validation.py \
  tests/test_vabench_release_asset_integrity.py \
  tests/test_vabench_release_completion_audit.py
```

After implementing the new audit runner:

```bash
cd behavioral-veriloga-eval
python3 runners/audit_vabench_content_contract.py
pytest -q tests/test_vabench_content_contract.py
```

## Stop Condition

The benchmark content audit is ready for baseline pilots only when:

- all Audit Gate A automated checks pass;
- all Audit Gate B automated checks pass;
- every L2 entry has a human `keep` or `revise-complete` decision;
- high-risk L1 entries have no unresolved wording/checker/gold mismatch;
- score remains disabled, while unweighted pass-rate reporting is allowed;
- any remaining caveat is documented as a non-blocking review note, not hidden
  inside a pass result.
