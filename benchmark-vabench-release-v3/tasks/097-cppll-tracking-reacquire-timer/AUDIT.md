# Task 097 Audit

## Scope

Task boundary is one primary Verilog-A DUT artifact, `cppll_timer_ref.va`,
with `ref_step_clk.va` supplied as a harness support artifact used to stage the
reference-frequency step source. Only `cppll_timer_ref.va` is the graded
candidate target.

## Four Standards

- Useful scenario: accepted. The module is a reusable behavioral Verilog-A block or flow component with a concrete transient use case.
- Reasonable task: accepted for this reviewed v3 slice. The public prompt names the target artifact, interface, and behavior context.
- Complete tests: accepted for current EVAS smoke. The reference implementation passes, visible
  smoke passes with nearby-but-different public parameters, and five concrete
  behavior negatives fail by simulation correctness.
- Fair evaluation: improved. The prompt no longer asks for a testbench or leaks
  private numeric scenario details. The checker now also requires nontrivial
  `vctrl_mon` movement so a fixed-control implementation cannot pass by staying
  near the original frequency.

## Checker And Evidence

- Checker context: CPPLL reference-step reacquire behavior
- EVAS reference smoke: PASS
- EVAS visible smoke: PASS
- Concrete negatives: 5/5 `FAIL_SIM_CORRECTNESS`
- Additional checker hardening: `vctrl_span >= 0.02` in both streaming and
  in-memory CPPLL reacquire checkers.
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py`: private
  reference PASS and 5/5 private negative variants `NEGATIVE_REJECTED`.
- Gate 2 Cadence status: `cadence_lint_pending`.

## Remaining Risk

AHDL lint evidence is not attached yet; do not mark `cadence_modeling_ready`
until lint/triage is recorded.
