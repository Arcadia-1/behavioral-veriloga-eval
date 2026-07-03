# Two-Gate SOP Audit: Task 208 Offset Bisection Driver

## Scope

Task 208 is a comparator-offset bisection stimulus driver. It drives
`vinp/vinn` symmetrically around the analog `vcm` input, updates on falling
clock edges, and halves its step when the observed comparator decision changes
polarity.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready` as a support-style L1 component.
- Counting decision: among the 203/208 driver pair, task 208 is the stronger
  representative because its public contract includes common-mode following and
  polarity-change bisection behavior.
- Function boundary: reusable offset-search stimulus/bisection driver for
  comparator characterization.
- Checker alignment: the checker verifies falling-edge updates, common-mode
  tracking, polarity-sensitive step halving, and differential output scaling.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after bridge-backed Spectre gold
  and negative validation. The result JSON reports no task-level errors; the
  remaining Spectre warnings are global AHDL-CMI/environment or simulator-mode
  notices rather than task-specific Verilog-A modeling findings.
- Prompt hygiene: the prompt now states the public interface, parameters,
  update rule, common-mode behavior, and constraints without source-import or
  hidden-evaluator wording.
- Metadata repair: release-level `CHECKS.yaml` now includes a current
  `sim_correct:` block.
- Counting risk: task 122 is the duplicate/rewrite candidate for this
  polarity-change bisection algorithm; task 208 is the clearer retained
  representative.

## Evidence

- EVAS hidden gold: PASS; the behavior-derived checker reports six checked
  update edges with zero differential and common-mode error.
- EVAS negatives: 4/4 behavioral rejections covering zero output, missing step
  halving, inverted sign sense, and full-differential scaling.
- Spectre hidden gold: PASS via the restored Virtuoso bridge
  (`BRIDGE_PROFILE=jin`, `--spectre-backend bridge`).
- Spectre negatives: 4/4 `NEGATIVE_REJECTED` on the hidden deck. The completed
  bridge rerun rejects zero output, missing step halving, inverted sign sense,
  and full-differential scaling.

## Human Confirmation

The reviewer confirmed that support components can be meaningful benchmarks
when they model reusable AMS behavior rather than hidden testbench machinery.
