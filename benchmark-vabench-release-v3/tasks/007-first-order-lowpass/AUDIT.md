# Task 007 Audit

Task: `007-first-order-lowpass`

Status: independent L1 EVAS formal candidate. Count this row as the
first-order lowpass circuit-function coverage; do not also count
`286-first-order-lowpass-bugfix` as a second independent lowpass function.

## Four-Standard Review

- Useful scenario: pass. A timer-discretized first-order lowpass is a common behavioral primitive for analog baseband filtering, settling envelopes, and stable state update examples.
- Reasonable task: pass. The public prompt fixes the module name, scalar
  voltage ports, finite-bandwidth timer-discretized lowpass behavior, forbidden
  continuous operators, and transition-driven voltage output without leaking the
  gold recurrence coefficient.
- Complete tests: pass for EVAS formal-candidate scope. The visible `.scs` is a single public step smoke with `vin` and `vout` saved. The hidden `.scs` exercises a long rising step so the checker can verify lag, monotonic movement, boundedness, and late-level settling.
- Fair evaluation: pass. Every hidden scoring requirement follows from the
  public prompt plus supplied testbench assets; hidden stimulus points and
  tolerances are private, but no hidden-only behavior is required.
- Prompt hygiene: pass after review. The public prompt no longer references
  hidden evaluator internals or source/provenance labels.

## Checker Contract

- Trace signals: `time`, `vin`, `vout`.
- Static checks: require a Verilog-A timer update, `transition()`, no current contribution, no `ddt()`, and no `idt()`.
- Behavioral checks: detect the input step, reject passthrough behavior, verify monotone first-order movement after safe-time windows, check bounded/no-overshoot response, and check that late `vout` levels match the expected discrete recurrence within tolerance.

## Evidence

- Hidden gold: PASS under EVAS with `v3_007_first_order_lowpass`.
- Static structure: JSON manifests parse, no `meta.json` exists in this task, and solution/negative Verilog-A files preserve the `first_order_lowpass(vin,vout)` interface.
- Concrete negative variants: 5 prepared for recertification:
  - `neg_001_too_slow_alpha`: wrong recurrence coefficient.
  - `neg_002_passthrough_timer`: timer-sampled passthrough.
  - `neg_003_inverted_input`: wrong input polarity/final value.
  - `neg_004_output_clamped`: clips the filtered state.
  - `neg_005_stuck_zero`: never follows the input.

## Remaining Risk

- Concrete negative variants: 5/5 compile and fail with `FAIL_SIM_CORRECTNESS`.
- Per SOP, paper-facing final certification still needs Spectre/Spectre-AX correlation or an explicit EVAS-only label.

Certification status: certified as an EVAS formal candidate on 2026-06-24.
