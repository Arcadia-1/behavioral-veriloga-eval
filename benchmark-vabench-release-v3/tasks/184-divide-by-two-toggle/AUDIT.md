# Two-Gate SOP Audit: Task 184 Divide By Two Toggle

## Scope

Task 184 implements a rising-edge divide-by-two toggle with ports `clkin,
clkout`. It is a duplicate-function row relative to task 275, which now carries
the canonical parameterized divide-by-two toggle contract.

## Gate 1: Admission And Counting

- Admission label: `hard_duplicate_rewrite_or_remove`.
- Counting decision: keep task 184 only as a non-counted duplicate/migration
  artifact; keep task 275 as the canonical independent L1 divide-by-two toggle
  row.
- Function boundary: the state starts low and toggles on each rising input
  clock crossing, producing a divide-by-two output.
- Duplicate rationale: task 184 and task 275 share the same module name, target
  artifact role, single-output clock-divider behavior, and negative classes.
  Differences in port names, source lineage, category labels, and default
  parameterization are not independent circuit functions.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_rework` for counted coverage. The gold
  model is Spectre-valid, but the row remains non-counted because it duplicates
  task 275 and its paired simulator decks are still byte-identical.
- Checker role: the checker now derives expected output state from detected
  rising input edges rather than relying on one fixed waveform table.
- Functional-math invariant: before the first rising edge the output is low;
  after each rising edge the expected state alternates high/low.
- Cadence reference correspondence: Cadence Verilog-AMS examples show the same
  modeling pattern of `@(initial_step)` state initialization,
  `@(cross(...,+1))` threshold-crossing events, and `transition(state*Vdd, ...)`
  style discrete-state output driving. Task 184 uses the same event/state
  pattern with its legacy `clkin, clkout` interface.

## Evidence

- Human confirmation: user confirmed only one divide-by-two toggle row should
  remain counted; task 275 is retained as canonical.
- Visible/hidden relationship: task 184 paired simulator decks are
  byte-identical, which is one reason it should not remain counted.
- EVAS gold after dynamic-checker repair: PASS.
- EVAS negatives after dynamic-checker repair: 4/4 `FAIL_SIM_CORRECTNESS`.
- Spectre gold after dynamic-checker repair: visible PASS and hidden PASS.
- Spectre negatives after dynamic-checker repair: 4/4 `NEGATIVE_REJECTED`.
- AHDL lint/read-in triage: no `AHDLLINT-*` messages were found in the visible,
  hidden, or negative Spectre logs reviewed for this repair.

## Rewrite Path

To make task 184 independent later, rewrite it away from a plain divide-by-two
toggle. Plausible directions include an asynchronous resettable divider,
clock-enable divider, duty-cycle constrained divider, programmable ratio
divider, or a Measurement L2 row that characterizes divider duty cycle/jitter.
The rewrite must change the public contract, checker behavior, hidden stimulus,
and negative variants enough that it no longer shares task 275's behavior.
