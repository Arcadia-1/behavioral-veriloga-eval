# Task 030 Audit

Task: `030-higher-order-filter`

Status: independent L1 candidate for a clocked cascaded two-pole sampled
filter. This is separate from `007-first-order-lowpass`, which covers the
single-state timer-updated first-order low-pass primitive. Gate 2 Cadence status
is `cadence_modeling_ready` for the reviewed gold after current-branch EVAS,
targeted Spectre, and AHDL warning triage.

## Review Decision

- Useful scenario: pass. Cascaded first-order sections are a standard
  behavioral way to model a higher-order low-pass response in sampled or
  event-driven AMS models.
- Reasonable task: pass. The public prompt defines a clocked, resettable,
  two-state filter with a common-mode-centered lag metric.
- Complete tests: pass for EVAS/Spectre gold validation and EVAS negative
  recertification. The private validation stimulus exercises reset, rising
  response, falling response, settling lag, and metric span. Five concrete
  negatives cover passthrough, stuck/midscale behavior, wrong polarity/dynamics,
  missing lag, and inadequate response span.
- Fair evaluation: pass. The checker uses observable `clk`, `rst`, `vin`,
  `out`, and `metric` behavior rather than requiring a private implementation
  formula.

## Checker And Evidence

- Checker id: `v3_030_higher_order_filter`
- Runner mapping: `CHECKS["v3_030_higher_order_filter"] = check_release_two_pole_filter`
- Reference solution: PASS under EVAS and targeted Spectre.
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Public visible smoke: EVAS compile/transient smoke PASS.
- AHDL lint/read-in triage: EVAS AHDL-like lint preflight reports PASS with
  zero diagnostics for the hidden solution and starter cases. Spectre AHDL
  read-in reports no task-level `AHDLLINT-*`, AHDL compile, or VACOMP errors;
  the remaining `VACOMP-2435` and `SPECTRE-592` warnings are shared
  environment/mode notices.
