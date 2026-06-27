# Task 286 Audit

Absorbs v2 `vbr1_l1_first_order_lowpass:bugfix` into v3. Task
`007-first-order-lowpass` covers the clean DUT construction form; this task
preserves a bugfix-form repair workflow for the same lowpass function.

## SOP Review

- Function boundary: valid variant, not independent circuit-function coverage.
  Keep only with counting policy: `007-first-order-lowpass` is the independent
  L1 lowpass function row; `286-first-order-lowpass-bugfix` is a bugfix skill
  variant for model-maintenance evaluation.
- Useful scenario: pass. Repairing a behavioral low-pass regression is a real
  model-maintenance task.
- Reasonable task: pass. The buggy symptom, interface, and expected step
  response are public, and the prompt now states that this is a repair task
  rather than a new lowpass design task.
- Complete tests: pass for the current reviewed slice. The visible smoke uses a
  shorter public transient, while the hidden bench keeps the full 160 ns
  settling scenario required by the lowpass checker.
- Fair evaluation: pass. The checker enforces only the public finite-bandwidth
  step behavior: input step exercised, non-instantaneous lag, monotonic first
  order movement, late settling near 0.8 V, and bounded output.

## Evidence

- Hidden gold: PASS under EVAS with `v3_286_first_order_lowpass_bugfix`.
- Concrete negative variants: 4/4 compile and fail with
  `FAIL_SIM_CORRECTNESS`:
  - `neg_001_leave_buggy`: original too-slow alpha.
  - `neg_002_passthrough_timer`: timer-delayed passthrough.
  - `neg_003_inverted_input`: wrong input polarity/final value.
  - `neg_004_output_clamped`: clips the repaired output below the late level.
- Cadence/Spectre evidence from `scripts/run_v3_spectre_audit.py`: hidden
  gold PASS and 4/4 hidden negative variants `NEGATIVE_REJECTED`.
- Gate 2 Cadence status: `cadence_lint_pending`.

## Remaining Risk

- AHDL lint evidence is not attached yet; do not mark
  `cadence_modeling_ready` until lint/triage is recorded.
- Counting reports must not claim this row as independent lowpass circuit
  coverage in addition to task 007.
