# v3 Task Review SOP

This SOP is the manual admission checklist for deciding whether a v3 task can
be counted as independent benchmark coverage. It is intentionally stricter than
"the gold solution passes": a task can be useful but still need rework before it
enters a scored release denominator.

## Review Order

Use two admission passes, in this order. Apply EVAS compatibility triage
whenever either pass exposes a simulator issue.

### 1. Function Boundary Review

Decide what function the task claims before looking at checker details.

- Keep `task.toml` `form` separate from scoring/admission status. A `dut` task
  remains a DUT task unless the prompt and artifacts are rewritten.
- Decide whether the DUT is a standalone L1 component, an L2 support component,
  a Measurement L2 flow, a Core Circuit L2 flow, or a duplicate/rewrite
  candidate.
- A component may appear inside an L2 flow and still count independently when
  the component prompt has a standalone behavior boundary and the L2 prompt
  evaluates integration.
- A local module split from a larger flow is not automatically an independent
  function. It must have a reusable analog/mixed-signal role outside that one
  flow.
- Source, clock, stimulus, and reference modules are not automatically support
  tasks. They can count as circuit-source functions only when the prompt models
  a reusable circuit behavior rather than an external testbench waveform.

### 2. Evaluation Alignment Review

After the function boundary is accepted, check whether the current assets
actually evaluate that boundary.

- Public prompt must describe the task's own function, not a historical import
  path, hidden evaluator, or unrelated companion form.
- A DUT task should name the primary target artifact clearly. Support artifacts
  may be supplied by the harness, but the solver should not be asked to repair a
  whole flow when the credit is for one L1 component.
- Visible tests should be public smoke coverage. Hidden tests should add a
  non-identical private challenge: different parameters, extra windows,
  reset/reacquisition behavior, edge cases, or longer scenarios.
- The checker must measure the claimed function. A flow-level metric is valid
  for an L2 flow, but not enough evidence for an L1 component unless it also
  isolates the component's local behavior.
- Concrete negatives must compile and fail behavioral correctness. `neg_001_zero`
  alone is not enough for final admission; use targeted mutations that exercise
  the claimed function.
- EVAS-only evidence must be labeled as such. Paper-facing final certification
  still needs Spectre/Spectre-AX parity or an explicit EVAS-only scope label.

### 3. EVAS Compatibility Triage

When review or repair exposes an EVAS frontend/backend issue, handle it before
continuing benchmark admission.

- First decide whether the failing construct is valid within vaBench's
  voltage-domain/event-driven Verilog-A scope. If it is unsupported by design,
  rewrite or reject the benchmark asset and record the scope reason.
- If the construct is valid but EVAS fails to parse, compile, or simulate it,
  treat that as an EVAS compatibility bug. Do not treat a benchmark-side
  workaround as the primary fix; reduce a minimal EVAS regression, fix EVAS
  upstream or open a PR, and link the issue/PR in the benchmark audit note.
- A temporary benchmark rewrite may be used only to keep local review moving. It
  must be labeled as a workaround and must not be counted as evidence that the
  original EVAS issue is resolved.
- Do not accept a negative variant that fails only because of an EVAS bug. The
  negative must fail by behavioral correctness after the EVAS issue is fixed, or
  it remains pending/non-counting.
- After the EVAS fix, rerun the minimal regression and the affected benchmark
  gold/negative checks before returning the task to admission review.

## Prompt Hygiene Checks

Reject or rewrite a public prompt before admission if it contains any of these
red flags:

- `hidden evaluator`, `hidden checker`, or private checker implementation
  details;
- historical migration ids such as old `vbr1_*` task names used as the task's
  public rationale;
- stale form residue such as "write a Spectre testbench" inside a `dut` prompt;
- "original public behavior context" blocks copied from another form;
- exact hidden-only timing windows, sample indices, seeds, or checker thresholds;
- implementation-style notes that leak gold-history repairs rather than the
  public behavior contract.

Public numerical parameters are allowed when they are part of the public task
contract, especially for a concrete testbench/e2e flow. They are risky when the
visible and hidden benches use exactly the same parameter set and no hidden
behavior is left to generalize.

## Artifact Boundary Checks

For each task, inspect `task.toml`, `starter/`, `solution/`, and the testbenches.

- For a standalone L1 DUT, `artifacts.target` should normally contain the
  primary DUT file. Companion files should be support files supplied by the
  harness, not co-equal solver targets.
- If `starter/` and `solution/` contain an entire multi-module flow for a task
  claiming one L1 component, mark it as a migration-residue risk.
- If `test_visible` and `test_hidden` are byte-identical, mark hidden coverage
  as insufficient unless the task is explicitly only a visible smoke candidate.
- If multiple tasks share the same hidden testbench and checker, verify whether
  they are intended L2/component overlap or accidental duplicate credit.

## Checker Alignment Checks

Classify the checker by what it proves.

- Local component checker: validates the primary DUT's behavior directly, such
  as dither polarity/amplitude/common-mode, gain/polarity/common-mode, reset
  semantics, code weights, threshold windows, or sequence timing.
- Flow checker: validates a composed scenario, such as gain separation,
  converter-loop completion, PLL reacquisition, or measurement artifact output.
- A flow checker can certify a Measurement L2 or Core Circuit L2 task. It should
  not be used as the only final evidence for an independent L1 component.
- Alias reuse is acceptable only when the alias still measures the claimed
  function. Otherwise create a v3-specific checker or keep the task
  non-counted/pending.

## Negative Variant Checks

Final admitted tasks should have multiple targeted concrete negatives.

- Minimum final expectation: at least four concrete behavior negatives for
  source-import style L1 tasks, or a task-specific equivalent for migrated L1/L2
  tasks.
- Negatives should target distinct behavior classes, not merely all-zero output.
- A negative that fails by syntax, missing files, compile error, timeout, or
  unsupported simulator feature does not prove checker strength.
- If a negative passes because the hidden stimulus does not observe the mutated
  behavior, strengthen the hidden test or replace the negative.

## Admission Labels

Use these labels consistently in reports and PR notes.

| Label | Meaning |
| --- | --- |
| `independent_l1_ready` | Standalone L1 function with aligned hidden tests, checker, and targeted negatives. |
| `independent_l1_rework` | Function boundary is worth preserving, but prompt/artifacts/checker/negatives need repair. |
| `l2_measurement_ready` | Measurement/characterization L2 flow with aligned flow-level evaluation. |
| `l2_core_ready` | Core circuit/subsystem L2 flow with aligned integration evaluation. |
| `l2_support_component` | Useful helper inside an L2 flow, not counted as an independent L1 credit in its current prompt form. |
| `valid_variant_needs_counting_policy` | Same function appears in another form, such as DUT vs bugfix/testbench; keep only with explicit counting rules. |
| `hard_duplicate_rewrite_or_remove` | Same function and artifact behavior; keep at most one scored row unless one is rewritten. |
| `candidate_evas_only` | EVAS evidence exists, but final paper-facing certification is pending Spectre/Spectre-AX parity. |

## Worked Example: 099/101/111/287

The gain-extraction group shows why the two-pass SOP is necessary.

- `099-dither-adder`: function boundary is worth preserving as an L1
  differential dither-injection component. Current assets need rework because
  the prompt still references the original gain-extraction hidden scenario, the
  task ships the whole flow as targets/support, the visible and hidden benches
  are identical, the checker is flow-level, and only `neg_001_zero` exists.
  Label: `independent_l1_rework`.
- `101-fixed-gain-amplifier`: function boundary is worth preserving as an L1
  fixed-gain differential amplifier. It has the same evaluation-alignment
  problems as task 099. Label: `independent_l1_rework`.
- `111-clocked-sine-source`: current prompt is an ordinary testbench sine
  source for the gain-extraction scenario, not a standalone circuit-source
  function. Keep as an L2 support component unless rewritten. Label:
  `l2_support_component`.
- `287-gain-extraction-flow`: preserves the composed source/dither/gain/testbench
  flow. It has independent value as a Measurement L2, but needs fresh
  recertification and stronger negatives before final admission. Label:
  `l2_measurement_ready` only after that evidence is attached.

## PR Checklist

Every task-quality PR should state:

- which function-boundary label each touched task receives;
- which prompt hygiene issues were removed;
- whether visible and hidden tests differ, and how;
- which checker id is used and what behavior it proves;
- how many concrete negatives were run and whether they failed by behavioral
  correctness rather than compile/setup failures;
- whether review exposed an EVAS bug, and if so the linked EVAS issue/PR plus
  the rerun evidence after the fix;
- whether the evidence is EVAS-only or includes Spectre/Spectre-AX parity.
