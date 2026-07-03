# Two-Gate SOP Audit: Task 146 Smooth Comparator Tanh

## Scope

Task 146 is an independent L1 comparator row. It models a memoryless smooth
comparator transfer from the differential input `V(sigin,sigref)` to `sigout`
using a public tanh expression with overrideable output levels, input offset,
and slope.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: keep task 146 as the scored smooth-transfer comparator.
- Function boundary: continuous, memoryless soft-decision comparator behavior.
- Duplicate check: task 292 is no longer a duplicate of 146 after its rewrite
  into a hysteretic comparator receiver with state, separate rising/falling
  thresholds, propagation delay, and rail-coded output.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the audited task definition.
- Prompt hygiene: the public prompt declares the module interface, public
  parameters, observable tanh transfer, and DUT/testbench boundary without
  hidden-checker or gold-history wording.
- Gold quality: the gold model is a pure voltage-domain Verilog-A contribution
  using the public tanh transfer.
- Checker alignment: the task checker evaluates the smooth tanh transfer over
  the saved waveform instead of relying only on a small fixed sample table.
- Negative strength: five concrete negatives compile and target behavior
  classes including zero output, polarity inversion, slope error, output-span
  error, and scaled-output error.

## Evidence Summary

- Visible and hidden decks exercise different input/reference trajectories
  under the same public parameter contract.
- The task has been reviewed as comparator-category content, not as a generic
  mixed-signal utility row.
- EVAS evidence for the current checker: visible gold PASS, hidden gold PASS,
  and 5/5 hidden negatives rejected with `FAIL_SIM_CORRECTNESS`.
- Spectre evidence for the current checker: hidden gold PASS and 5/5 hidden
  negatives `NEGATIVE_REJECTED`.
- AHDL warning triage: the targeted Spectre runs reported no task-specific
  AHDL lint failure; the remaining warnings were the shared
  `VACOMP-2435`/`SPECTRE-592` environment/setup notices.
