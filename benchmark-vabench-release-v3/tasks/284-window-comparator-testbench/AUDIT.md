# Task 284 Audit

Absorbs v2 `vbr1_l1_window_comparator_detector:tb` into v3.

## SOP Review

- Function boundary: valid testbench-generation variant, not independent
  circuit-function coverage. Task `049-window-comparator-detector` remains the
  independent L1 window-comparator DUT row; this row evaluates whether an agent
  can write a verification bench for the supplied DUT.
- Useful scenario: pass. Testbench generation for a threshold/window detector is
  a practical verification task.
- Reasonable task: pass. The DUT is supplied and the required waveform coverage,
  supply rails, transient settings, and saved observables are public because
  they are the target `.scs` artifact contract.
- Complete tests: pass for the current reviewed slice after adding targeted
  negatives and repairing Spectre-legal negative fixtures.
  The visible smoke bench is now a shorter public example rather than a byte
  copy of the full hidden/gold testbench.
- Fair evaluation: pass. The checker evaluates only public `vin/out` behavior:
  below-window low, above-window low, rising-side inside-window high, and
  falling-side inside-window high.

## Evidence

- Hidden gold: PASS under EVAS with `v3_284_window_comparator_testbench`.
- Concrete negative variants: 4/4 compile and fail with
  `FAIL_SIM_CORRECTNESS`:
  - `neg_001_no_window_sweep`: input never visits the comparator window.
  - `neg_002_no_above_window`: no above-window region.
  - `neg_003_no_falling_window`: no falling-side in-window region.
  - `neg_004_no_below_window`: no below-window region.
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py`: hidden
  gold PASS and 4/4 hidden negative variants `NEGATIVE_REJECTED`.
- Gate 2 Cadence status: `cadence_lint_pending`.

## Remaining Risk

- AHDL lint evidence is not attached yet; do not mark
  `cadence_modeling_ready` until lint/triage is recorded.
- Counting reports must not claim this row as independent window-comparator
  circuit-function coverage in addition to task 049.
