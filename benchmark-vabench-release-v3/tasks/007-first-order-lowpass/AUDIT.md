# Task 007 Audit

Task: `007-first-order-lowpass`

Status: independent L1 Gate 1 formal candidate. Count this row as the
first-order lowpass circuit-function coverage; do not also count
`286-first-order-lowpass-bugfix` as a second independent lowpass function.
Gate 2 Cadence status: `cadence_modeling_ready` for the reviewed gold after
current-branch EVAS, targeted Spectre, and AHDL warning triage.

## Four-Standard Review

- Useful scenario: pass. A timer-discretized first-order lowpass is a common behavioral primitive for analog baseband filtering, settling envelopes, and stable state update examples.
- Reasonable task: pass. The public prompt fixes the module name, scalar
  voltage ports, finite-bandwidth timer-discretized lowpass behavior, forbidden
  continuous operators, and transition-driven voltage output without leaking the
  gold recurrence coefficient.
- Complete tests: pass for EVAS/Spectre gold validation and EVAS negative
  recertification. The visible `.scs` is a single public step smoke with `vin`
  and `vout` saved. The private validation deck exercises a long rising step so
  the checker can verify lag, monotonic movement, boundedness, and late-level
  settling.
- Fair evaluation: pass. Every scoring requirement follows from the public
  prompt plus supplied testbench assets; private stimulus points and tolerances
  do not define extra behavior.
- Prompt hygiene: pass after review. The public prompt no longer references
  private evaluator internals or source/provenance labels.

## Checker Contract

- Trace signals: `time`, `vin`, `vout`.
- Static checks: require a Verilog-A timer update, `transition()`, no current contribution, no `ddt()`, and no `idt()`.
- Behavioral checks: detect the input step, reject passthrough behavior, verify monotone first-order movement after safe-time windows, check bounded/no-overshoot response, and check that late `vout` levels match the expected discrete recurrence within tolerance.

## Evidence

- Reference solution: PASS under EVAS and targeted Spectre with
  `v3_007_first_order_lowpass`.
- Static structure: JSON manifests parse, no `meta.json` exists in this task, and solution/negative Verilog-A files preserve the `first_order_lowpass(vin,vout)` interface.
- Concrete negative variants:
  - `neg_001_too_slow_alpha`: wrong recurrence coefficient.
  - `neg_002_passthrough_timer`: timer-sampled passthrough.
  - `neg_003_inverted_input`: wrong input polarity/final value.
  - `neg_004_output_clamped`: clips the filtered state.
  - `neg_005_stuck_zero`: never follows the input.
- Spectre evidence from `scripts/run_v3_spectre_audit.py`: targeted gold PASS
  on the current branch.
- AHDL lint/read-in triage: EVAS AHDL-like lint preflight reports PASS with
  zero diagnostics for the hidden solution and starter cases. Spectre AHDL
  read-in reports no task-level `AHDLLINT-*`, AHDL compile, or VACOMP errors;
  the remaining `VACOMP-2435` and `SPECTRE-592` warnings are shared
  environment/mode notices.

## Remaining Risk

- Counting reports must not also count `286-first-order-lowpass-bugfix` as a
  second independent lowpass function.

Certification status: certified as an EVAS formal candidate on 2026-06-24.
