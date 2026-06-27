# v3 Task Review SOP

This SOP is the manual two-step review for deciding whether a v3 task can be
counted as independent benchmark coverage and whether its Verilog-A artifacts
are good enough to trust as Cadence/Spectre-style behavioral models.

It is intentionally stricter than "the gold solution passes": a task can be
useful but still need rework before it enters a scored release denominator, and
a counted task can still need modeling-quality repair before it supports strong
paper-facing claims.

Use the local Cadence-derived companion SOP as the detailed modeling reference:
`../../_local_learning/cadence-veriloga/sop/cadence-to-vaevas-sop.md`.

## Review Order

Use two gates, in this order. Apply EVAS compatibility triage whenever either
gate exposes a simulator issue.

Gate 1 is benchmark admission and counting: decide what function the row claims
and whether the current assets evaluate that function.

Gate 2 is Cadence/Spectre modeling quality: decide whether the prompt, gold,
checker, metadata, linter evidence, and actual Cadence/Spectre runs make the
Verilog-A semantics explicit enough to be a credible behavioral-model
benchmark.

Do not collapse these gates. A row may pass Gate 1 but fail Gate 2 because the
Verilog-A contract is underspecified; a row may pass Gate 2 as a well-modeled
artifact but fail Gate 1 because it is duplicate, support-only, or not
independent benchmark coverage.

### Gate 1A. Function Boundary Review

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

### Gate 1B. Evaluation Alignment Review

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

### Gate 2A. Cadence Prompt Contract Review

After the row has a plausible coverage role, check whether the public prompt
and visible assets define the Verilog-A modeling contract precisely enough.

The prompt or visible assets should define, as applicable:

- module name, target artifact, ports, directions, disciplines, and ordering;
- parameters, defaults, units, legal ranges, and override behavior;
- conservative vs signal-flow behavior, branch orientation, loading, and
  current sign convention;
- thresholds, logic levels, edge directions, transition/slew timing, event
  initialization, and final-step/report behavior;
- operator semantics such as `ddt`, `idt`, `idtmod`, `absdelay`,
  `last_crossing`, `limexp`, `transition`, `slew`, and `ddx`;
- math domains, units, real vs integer arithmetic, logical vs bitwise behavior,
  relational intervals, and ternary/conditional region maps;
- bus width, bit order, generated topology, endpoint mapping, and section
  counts for `genvar`/`generate` rows;
- table files, random seeds/distributions, noise/AC/DC analysis context,
  report files, and timestep-control expectations;
- Spectre-only features, EVAS boundary features, hierarchy/view assumptions,
  and source inclusion order.

If a checker requires one of these semantics and the public prompt/visible
assets do not expose it, repair the public contract before admission. Do not
hide the actual modeling contract inside the gold solution or private checker.

### Gate 2B. Cadence Gold Verilog-A Review

Review the gold `.va` as a behavioral model, not just as a passing answer.

Gold code should normally:

- declare includes, ports, directions, disciplines, parameters, and local state
  deliberately;
- use branch access and contribution orientation intentionally, especially for
  probe/source/switch-branch rows;
- initialize state through `analog initial`, `initial_step`, or `above` only
  where that choice matches the analysis contract;
- use `cross`, `timer`, `transition`, `slew`, analog operators, and
  final-step/file IO in legal, reviewable placements;
- parenthesize complex arithmetic, relational, logical, bitwise, and ternary
  expressions;
- guard math function domains and use real literals where analog real
  arithmetic is intended;
- keep user-defined analog functions as pure helpers, not as hiding places for
  contributions, events, access functions, analog operators, filters, or
  simulator-visible state;
- use `genvar`/`generate` for static repeated analog structure and analog bus
  indexing;
- bundle and declare `$table_model` assets, random behavior, noise behavior,
  file IO/report behavior, hierarchy aliases, and compiler-directive effects;
- prefer `$abstime` for Spectre-facing time and treat `$finish`, `$stop`, and
  severity tasks as explicit diagnostics/control behavior.

Gold smells that trigger Gate 2 rework include:

- undefined port disciplines, guessed harness names, accidental branch
  orientation, or accidental multiple contributions;
- `transition` used as a smoother for continuous signals, `cross` used where
  t=0/DC state is required, or `final_step` reports with uninitialized counters;
- runtime loops containing analog operators, contributions, event controls, or
  analog-array indexing that should be `genvar`;
- chained relational expressions, integer division in analog scaling, or
  logical/bitwise confusion in voltage-domain logic;
- table/random/file/report behavior that depends on untracked assets,
  implicit seeds, unstable parse formats, or missing close behavior;
- linter-relevant exact time/equality tests, missing `case` defaults, nested
  derivatives, conditional contributions, or timestep-collapse hazards.

### Gate 2C. Cadence Checker, Metadata, and Linter Review

Checker strength must prove the Cadence-level contract, not only parse or
produce any waveform.

Add or strengthen checks for:

- initialization, event direction/tolerance, threshold boundaries, output
  levels, transition/slew windows, and final-step reports;
- DC/transient/operator behavior for `ddt`, `idt`, `idtmod`, `absdelay`,
  `last_crossing`, `limexp`, `transition`, `slew`, and `ddx`;
- every conditional region, default path, clamp/saturation path, and both
  switch-branch states;
- bit order, bus width, generated section count, endpoint mapping, and
  parameterized topology boundaries;
- table lookup domains and extrapolation behavior, random fixed-seed or
  statistical acceptance, noise/AC analysis context, file/report parseability,
  and oscillator/source frequency at multiple times.

Recommended metadata fields from the Cadence SOP should be attached where
relevant: `branch_contract`, `event_operator_contract`,
`analog_operator_state`, `math_domain_contract`,
`conditional_region_contract`, `generate_semantics`,
`analysis_function_contract`, `table_model_dependencies`,
`random_semantics`, `noise_semantics`, `file_io_artifacts`,
`report_contract`, `source_timestep_control`, `ahdllint_status`, and
`ahdllint_options`.

When Cadence is available, run or record AHDL linter status before promoting a
gold model. Keep linter status separate from Spectre pass/fail and checker
pass/fail: warnings are triage evidence, not automatic failures, unless they
invalidate the row contract or gold quality.

### Gate 2D. Actual Cadence/Spectre Simulation Review

Do not promote a row to `cadence_modeling_ready` from EVAS evidence alone when
Cadence access is available. Run the real Cadence/Spectre path through the
configured bridge or direct Spectre backend and record the evidence before
making strong benchmark claims.

For each reviewed row, run the smallest Spectre slice that proves the claim:

- gold DUT/testbench on the hidden or official grading scenario;
- visible smoke when the public scenario or prompt/testbench contract changed;
- targeted negative variants when checker strength or negative coverage is
  being claimed;
- both the standalone component and composed flow when an L1 component also
  appears inside an L2 measurement/core flow.

Record enough provenance for each Cadence run:

- command or runner entry point, bridge/direct backend, bridge profile, Spectre
  mode, Cadence/Spectre version when available, timestamp, and host class;
- task id, candidate/gold artifact paths, testbench path, checker id, and output
  result/log paths;
- Spectre compile status, AHDL/linter warnings, transient completion status,
  checker result, and any extracted waveform/report metrics;
- whether the evidence is gold-only, visible smoke, hidden grading, negative
  variant, or EVAS/Spectre dual parity evidence.

Classify failures before editing the benchmark:

- Spectre compile/AHDL errors usually mean the public/gold Verilog-A or Spectre
  deck is not a valid Cadence artifact; repair the benchmark asset, not the
  checker.
- Spectre pass with EVAS fail is EVAS false-negative debt unless the construct
  is outside vaBench scope.
- EVAS pass with Spectre fail is a hard compatibility or checker-strength
  problem; reduce the Spectre failure and fix EVAS/checker before admission.
- Spectre pass with checker fail means the checker, expected contract, or
  tolerance/windowing needs review against the waveform.
- Bridge, SSH, license, daemon, or timeout failures are infrastructure blockers.
  Record them as blocked evidence, not as benchmark failures.

Actual Cadence simulation is part of Gate 2 evidence, not a replacement for
Gate 1. A duplicate/support-only row can have clean Spectre results and still
remain non-counted; a valid independent row can pass Gate 1 but remain pending
until Spectre/linter evidence is attached.

## Public Contract Alignment Page

Use this page whenever a review turns on whether a prompt leaks too much, or
whether the prompt still contains enough information after cleanup.

Ideal solver-facing split:

- Prompt: task role/form, target artifact, public interface, observable output
  contract, behavior goal, and modeling constraints.
- Public/visible testbench: exact stimulus values, transient length, analysis
  settings, saved signals, instance wiring, and support artifact syntax.
- Checker: verifies behavior implied by the prompt plus public/visible assets.
  It should not require hidden-only semantics, hidden sample points, gold
  implementation constants, or private checker thresholds.
- Hidden testbench: may vary parameters, extend observation windows, add edge
  cases, or stress robustness, but must not redefine the task's public
  function.

For DUT tasks, the public/visible testbench is a verification scenario, not an
implementation template. The solver may use it to understand which ports are
driven, which rails and waveforms are supplied, which observables are saved, and
which behavior will be exercised. The DUT should not hard-code testbench-only
values such as transient stop time, waveform breakpoints, maxstep, or a
particular supply value unless that value is explicitly part of the circuit
function contract. Prefer port-derived behavior, such as using `V(VDD,VSS)` for
an output rail, over copying a visible bench's `0.9 V` supply into the DUT.

For testbench-generation tasks, exact stimulus, supply, save, and analysis
settings may be part of the requested output contract. That makes the row a
verification/testbench variant for the associated function, not a second
independent circuit-function coverage row.

Review questions:

- Can a solver using only the prompt and public/visible assets write a plausible
  implementation without seeing the hidden checker?
- Are exact numeric values in the prompt truly part of the public behavior
  contract, or do they belong in the visible testbench?
- Does the checker require an exact value, timing point, or threshold that is
  absent from both the prompt and public/visible testbench?
- Are hidden-only values just robustness variations, or do they define the
  behavior needed to pass?
- If a prompt says "by the end of the transient window" or similar, is that
  window discoverable from the public/visible testbench rather than a hidden
  leak?
- For a DUT task, does the prompt encourage a general model that responds to
  supplied ports/stimuli, or does it invite hard-coding the visible testbench's
  timing, waveform, or rail constants into the DUT?
- For a testbench-generation task, are exact bench parameters clearly part of
  the target artifact contract, and is the row counted as verification coverage
  rather than independent circuit-function coverage?

Decision rule: if prompt plus public/visible assets are insufficient, promote
the missing requirement into the public prompt or visible asset. If the checker
requires information that should remain hidden, repair the checker or mark the
task non-admitted. Do not keep exact implementation constants in the prompt only
because the hidden checker happens to use them.

## Cross-Gate EVAS Compatibility Triage

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

Use these Gate 1 labels consistently in reports and PR notes.

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

## Modeling Quality Status

Use these Gate 2 statuses alongside, not instead of, the admission label.

| Status | Meaning |
| --- | --- |
| `cadence_modeling_ready` | Prompt, gold, checker, metadata, and evidence make the Verilog-A/Spectre semantics explicit and sufficiently checked. |
| `cadence_modeling_rework` | The coverage role may be valid, but prompt/gold/checker/metadata need Cadence-level semantic repair before strong claims. |
| `cadence_boundary_only` | The row intentionally exercises a Spectre-valid construct outside ordinary EVAS/scored scope; keep as boundary/L0 evidence unless separately admitted. |
| `cadence_lint_pending` | Modeling review is otherwise plausible, but AHDL linter evidence is unavailable or not yet triaged where Cadence access is expected. |
| `cadence_sim_pending` | Modeling review and linter status are plausible, but actual Cadence/Spectre simulation evidence has not been run or attached. |
| `cadence_sim_blocked` | Cadence/Spectre evidence is blocked by bridge, SSH, license, daemon, timeout, or other infrastructure rather than by benchmark semantics. |
| `cadence_sim_rework` | Actual Cadence/Spectre simulation exposed compile, runtime, waveform, checker, or EVAS/Spectre parity issues that require benchmark, checker, or EVAS repair. |
| `cadence_not_applicable` | The touched artifact is only bookkeeping, counting policy, or non-Verilog-A metadata. |

## Worked Example: 099/101/111/287

The gain-extraction group shows why the two-gate SOP is necessary.

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
- which Cadence modeling-quality status each touched task receives;
- which prompt hygiene issues were removed;
- which prompt/gold/checker/metadata semantics were repaired under Gate 2;
- whether visible and hidden tests differ, and how;
- which checker id is used and what behavior it proves;
- how many concrete negatives were run and whether they failed by behavioral
  correctness rather than compile/setup failures;
- whether AHDL linter was run, unavailable, or deferred, and which warnings
  were triaged when present;
- which actual Cadence/Spectre runs were executed, including bridge/direct
  backend, profile, Spectre mode, result/log paths, and whether the evidence was
  visible, hidden, gold, negative, or dual-parity;
- whether review exposed an EVAS bug, and if so the linked EVAS issue/PR plus
  the rerun evidence after the fix;
- whether the evidence is EVAS-only or includes Spectre/Spectre-AX parity.
