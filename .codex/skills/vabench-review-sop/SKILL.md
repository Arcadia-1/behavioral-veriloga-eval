---
name: vabench-review-sop
description: Self-contained two-gate SOP for auditing, repairing, and reporting vaBench benchmark tasks. Use when reviewing benchmarkv3/v3 tasks, duplicate or filler candidates, prompt hygiene, public prompt/testbench/checker boundaries, gold Verilog-A modeling quality, EVAS/Spectre agreement, Cadence/Spectre evidence, negative variants, or benchmark admission/counting labels.
---

# vaBench Review SOP

Use this skill as the source of truth for vaBench task review. Do not require a
repo-local `REVIEW_SOP.md` or bundled reference file to execute the workflow.
Repo docs may be useful historical context, but the procedure below is complete
enough to audit and repair tasks on its own.

## Operating Rules

- Check upstream before repair work when a remote exists. Fetch, compare touched
  files, and avoid duplicating upstream work.
- Keep skill changes and benchmark asset changes in separate commits/PRs.
- Preserve user changes. Do not reset or revert unrelated dirty files.
- Review from the public solver view first: prompt, visible assets, metadata,
  then checker/gold/private assets.
- Treat `checks.yaml` and hidden checker logic as evaluation evidence, not as
  the primary definition of the circuit function.
- When a public prompt is under review, paste the exact prompt for human review
  if requested; for Chinese collaboration, include a concise Chinese
  translation and mark the core clauses that need judgment.

## Workflow

### 1. Gather Artifacts

For each task under review, inspect:

- `task.toml` or manifest metadata: form, level, category, target artifacts;
- `instruction.md`: public agent prompt;
- `starter/`, `solution/`, support files, and target artifact boundaries;
- visible and hidden testbenches;
- `test_harness/checks.yaml` and checker id;
- concrete `negative_variants/`;
- existing `AUDIT.md` or report entries.

Record whether evidence is EVAS-only, Spectre-only, or dual/parity evidence.

### 2. Gate 1: Admission And Counting

Gate 1 asks whether the task deserves independent benchmark credit and whether
the current assets evaluate that claimed function.

First identify the function boundary:

- Standalone L1 component: reusable analog/mixed-signal circuit function.
- L2 support component: useful helper inside a larger flow, not independent L1
  credit in its current form.
- Measurement L2: composed testbench/measurement/characterization flow.
- Core Circuit L2: integrated mixed-signal subsystem or flow.
- Duplicate/rewrite candidate: same behavior as another row unless rewritten.

Rules:

- `task.toml` form does not change just because review labels the task
  support-only or duplicate.
- A component may appear inside an L2 flow and still count independently only
  when its prompt has a standalone behavior boundary and the L2 row evaluates
  integration.
- A source, clock, stimulus, or reference module can be a circuit-source
  function only when the prompt models reusable circuit behavior, not merely an
  external testbench waveform.
- Local helper modules split from a larger flow are not automatically
  independent functions.

Then check evaluation alignment:

- Public prompt describes the task's own function, not import history, old
  source names, hidden evaluator behavior, or unrelated companion forms.
- DUT tasks ask for the primary DUT only; support artifacts are supplied by the
  harness unless the task is explicitly a composed flow.
- Visible tests are public smoke coverage. Hidden tests should add non-identical
  private challenge: changed parameters, edge cases, reset/reacquisition,
  longer windows, or robustness variations.
- Checker measures the claimed function. Flow-level metrics can certify L2
  rows but should not be the only evidence for an L1 component.
- Negatives must compile and fail behavioral correctness. Syntax/setup failures
  do not prove checker strength.

Use these Gate 1 labels:

| Label | Meaning |
| --- | --- |
| `independent_l1_ready` | Standalone L1 function with aligned tests, checker, and targeted negatives. |
| `independent_l1_rework` | Valuable L1 boundary, but prompt/assets/checker/negatives need repair. |
| `l2_measurement_ready` | Measurement or characterization L2 flow with aligned flow evaluation. |
| `l2_core_ready` | Core circuit/subsystem L2 flow with aligned integration evaluation. |
| `l2_support_component` | Useful helper in an L2 flow, not independent L1 credit as written. |
| `valid_variant_needs_counting_policy` | Same function appears in another form or parameter family; count only with explicit policy. |
| `hard_duplicate_rewrite_or_remove` | Same function and artifact behavior; keep at most one scored row unless rewritten. |
| `candidate_evas_only` | EVAS evidence exists, but final paper-facing certification lacks Spectre parity. |

### 3. Gate 2: Cadence/Spectre Modeling Quality

Gate 2 asks whether the public contract, gold, checker, metadata, and real
simulator evidence make the Verilog-A semantics credible.

Prompt contract must expose, when relevant:

- module name, target artifact, port directions, disciplines, and ordering;
- parameters, defaults, units, legal ranges, and override behavior;
- branch orientation, current sign convention, and loading behavior;
- thresholds, logic levels, edge directions, transition/slew timing, reset and
  initialization semantics;
- analog operators and event operators: `cross`, `timer`, `transition`, `slew`,
  `ddt`, `idt`, `idtmod`, `absdelay`, `last_crossing`, `limexp`;
- math domains, units, real vs integer arithmetic, relational intervals,
  conditionals, and bitwise/logical distinctions;
- bus width, bit order, generated topology, endpoint mapping, and section
  counts;
- random seeds/distributions, table files, noise/AC/DC context, file IO,
  report artifacts, and timestep-control expectations.

Public boundary principle:

- Prompt states task role, target artifact, interface, observable contract,
  behavior goal, and modeling constraints.
- Visible/public testbench is a verification scenario. The solver may inspect
  it to understand wiring, stimuli, rails, saves, and observables.
- DUT code should not hard-code testbench-only stop times, waveform breakpoints,
  maxstep, or supply constants unless the prompt makes them part of the public
  circuit contract. Prefer port-derived behavior such as `V(VDD,VSS)`.
- Testbench-generation tasks may require exact stimulus/supply/save/analysis
  values; that makes them verification coverage, not a second independent
  circuit-function row.
- Checker must not require hidden-only semantics that are absent from both the
  prompt and visible assets.

Gold Verilog-A review:

- Verify includes, ports, directions, disciplines, parameters, local state, and
  branch contributions are deliberate.
- Check `cross`, `timer`, `transition`, analog operators, and `final_step` are
  used in legal and reviewable placements.
- Ensure state initialization matches the analysis contract.
- Parenthesize complex arithmetic and avoid integer division surprises.
- Guard math domains and use real literals where analog real arithmetic is
  intended.
- Remove gold-history comments such as "EVAS acceptance", "original
  transition", or "benchmark gold style" from public/starter/solution assets.

Checker, metadata, and linter review:

- Check initialization, event direction/tolerance, threshold boundaries, output
  levels, transition windows, final reports, and all conditional regions.
- Check bus order, generated section counts, endpoint mapping, random/table/file
  dependencies, and oscillator/source frequency when relevant.
- Record AHDL linter status separately from Spectre pass/fail. If no linter
  evidence was run, use `cadence_lint_pending`, not `cadence_modeling_ready`.

Actual Spectre review:

- Run the smallest Cadence/Spectre slice that proves the claim when access is
  available: hidden/official gold, visible smoke if public assets changed,
  targeted negatives, and both component/flow where overlap matters.
- Record command, backend/bridge, work/output paths, task ids, checker ids,
  split, variants, pass/fail counts, and simulator warnings.
- Gate 2 evidence does not replace Gate 1. A duplicate row can pass Spectre and
  remain non-counted; an independent row can pass Gate 1 and remain
  `cadence_lint_pending` or `cadence_sim_pending`.

Use these Gate 2 statuses:

| Status | Meaning |
| --- | --- |
| `cadence_modeling_ready` | Prompt, gold, checker, metadata, lint, and simulation evidence are sufficient. |
| `cadence_modeling_rework` | Coverage may be valid, but modeling semantics need repair. |
| `cadence_boundary_only` | Spectre-valid boundary/L0 construct outside scored scope. |
| `cadence_lint_pending` | Modeling/sim evidence is plausible, but AHDL lint evidence is missing or untriaged. |
| `cadence_sim_pending` | Modeling review is plausible, but actual Spectre evidence is missing. |
| `cadence_sim_blocked` | Spectre evidence is blocked by bridge, license, SSH, daemon, or timeout. |
| `cadence_sim_rework` | Spectre exposed compile/runtime/waveform/checker/parity issue. |
| `cadence_not_applicable` | Only bookkeeping or non-Verilog-A metadata was touched. |

### 4. EVAS Compatibility Triage

If review exposes an EVAS frontend/backend problem, pause benchmark admission
and triage EVAS first.

- Decide whether the construct is valid in vaBench's voltage-domain,
  event-driven Verilog-A scope.
- If valid Verilog-A fails in EVAS, reduce a minimal EVAS regression and fix
  EVAS upstream or open/link an EVAS PR. Do not treat a benchmark workaround as
  the real fix.
- Treat EVAS PASS / Spectre FAIL as a hard compatibility or checker-strength
  issue until proven otherwise.
- Treat Spectre PASS / EVAS FAIL on a valid candidate as EVAS false-negative
  debt unless the construct is out of scope.
- Never add task-name, benchmark-id, model-name, or checker-note special cases
  to EVAS core.
- After the EVAS fix, rerun the minimal regression and affected benchmark
  gold/negative checks.

### 5. Prompt Hygiene

Rewrite a public prompt before admission if it contains:

- `hidden evaluator`, `hidden checker`, or private checker implementation
  details;
- old source names or migration ids used as public rationale;
- stale form residue, such as asking for a Spectre testbench in a DUT task;
- copied "original public behavior context" blocks;
- hidden-only timing windows, sample indices, random seeds, or checker
  thresholds;
- implementation-history notes rather than public behavior contract.

Use neutral public wording such as "checker logic", "private test hooks", or
"simulator-private side channels" only as constraints against bad solutions,
not as descriptions of hidden evaluator internals.

### 6. Repair Policy

- Repair the public prompt/visible contract before changing gold or checkers
  unless the issue is solely a private fixture bug.
- Do not leak gold implementation details merely because the hidden checker
  uses them.
- If a task is duplicate but otherwise well-modeled, mark it non-counted or
  propose a rewrite path rather than deleting evidence.
- Strengthen negatives with distinct behavior classes: polarity, scaling,
  threshold, timing/reset, bus order, state, common-mode, clipping, or flow
  completion.
- Keep diffs narrow and reversible. Avoid broad refactors during audit repair.

### 7. Report Template

For each reviewed task or group, record:

- Gate 1 label and reasoning;
- Gate 2 status and reasoning;
- public prompt changes and hygiene issues removed;
- target artifact boundary and whether support files are solver targets;
- visible/hidden test relationship;
- checker id and what behavior it proves;
- negative variant count and whether failures are behavioral;
- EVAS evidence and Spectre evidence with commands/output paths;
- AHDL lint status or why it is pending;
- EVAS bugs found, linked EVAS issue/PR, and rerun evidence;
- uncertainties for human review and suggested rewrite paths.

When presenting prompts to the user for manual review, show each task
separately with:

1. the exact English prompt;
2. a concise Chinese translation;
3. the core review points: public contract, possible leakage, independence
   claim, and any uncertain semantics.
