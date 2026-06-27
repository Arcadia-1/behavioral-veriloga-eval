# Honest SOP Audit: Task 049 Window Comparator Detector

## Scope

Task boundary is one Verilog-A DUT, `window_comparator_ref.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A window comparator is a common threshold-monitoring and range-detection macro.
- Reasonable task: pass. The public prompt fixes in-window assertion,
  outside-window deassertion, public thresholds, port-derived output rails, and
  transition behavior. It no longer exposes hidden-evaluator wording or asks the
  DUT to copy transient/testbench timing constants into the Verilog-A model.
- Complete tests: pass for EVAS. Hidden samples check below-window,
  above-window, rising into-window, falling into-window, and output span. The
  visible smoke now saves `vin` and `out`, while structured concrete negatives
  cover inverted output, one-sided thresholding, wrong window limits, and stuck
  low output. Legacy flat near-miss negatives are retained as imported fixtures
  but are not the diversity claim.
- Fair evaluation: pass for EVAS. The checker uses public voltage observables
  and stated window behavior. Testbench-only values such as transient length and
  waveform breakpoints are public verification settings, not DUT implementation
  constants.

## Checker And Evidence

- Checker id: `v3_049_window_comparator_detector`
- Runner mapping: `CHECKS["v3_049_window_comparator_detector"] = check_true_window_comparator`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 4/4 structured negatives fail as
  simulation-correctness negatives.
- Visible compile/sim smoke: `COMPILE_SIM_OK` with public `vin/out`
  observables saved.
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py`: hidden
  gold PASS and 4/4 hidden negative variants `NEGATIVE_REJECTED`.
- Gate 2 Cadence status: `cadence_lint_pending`.

## Remaining Risk

AHDL lint evidence is not attached yet; do not mark `cadence_modeling_ready`
until lint/triage is recorded.
