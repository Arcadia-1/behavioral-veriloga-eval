# Task 284 Audit

Task 284 is a testbench-generation task for the window-comparator detector.

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
  copy of the full private reference testbench.
- Fair evaluation: pass. The checker evaluates only public `vin/out` behavior:
  below-window low, above-window low, rising-side inside-window high, and
  falling-side inside-window high.

## Evidence

- Reference implementation: PASS under EVAS with
  `v3_284_window_comparator_testbench`.
- Concrete negative variants: 4/4 compile and fail with
  `FAIL_SIM_CORRECTNESS`:
  - `neg_001_no_window_sweep`: input never visits the comparator window.
  - `neg_002_no_above_window`: no above-window region.
  - `neg_003_no_falling_window`: no falling-side in-window region.
  - `neg_004_no_below_window`: no below-window region.
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py` using the
  restored Virtuoso bridge (`BRIDGE_PROFILE=jin`, `--spectre-backend bridge`):
  hidden reference PASS and 4/4 private negative variants `NEGATIVE_REJECTED`.
- Runner repair: `scripts/run_v3_spectre_audit.py` now falls back to
  `TASKS.json` for `form=tb` when a task has no `task.toml`, so Spectre
  negative runs use the candidate testbench artifact rather than the hidden
  reference deck.
- AHDL lint/read-in triage: Spectre reports no task-level errors. The remaining
  warnings are global AHDL-CMI/environment or simulator-mode notices, not
  task-specific Verilog-A modeling findings.
- Gate 2 Cadence status: `cadence_modeling_ready`.

## Remaining Risk

- Counting reports must not claim this row as independent window-comparator
  circuit-function coverage in addition to task 049.
