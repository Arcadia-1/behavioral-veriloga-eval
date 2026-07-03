# Task 017 Audit

Task: `017-slew-rate-limiter`

Status: independent L1 candidate. Gate 2 Cadence status is
`cadence_modeling_ready` for the reviewed gold after current-branch EVAS,
targeted Spectre, and AHDL warning triage.

## Four Standards

- Useful scenario: pass. A slew-rate limiter is a common baseband and control-loop behavioral block.
- Reasonable task: pass. The prompt states the 1 ns timer cadence, maximum 15 mV update step, bidirectional limiting, output smoothing, and voltage-only constraints.
- Complete tests: pass for EVAS/Spectre gold validation and EVAS negative
  recertification. The private validation stimulus exercises a rising step and
  falling step, checks lagged response, eventual high/low reach, and both
  rising/falling slew limits. Five concrete negatives cover stuck output,
  passthrough behavior, wrong update logic, too-slow movement, and missing
  falling response.
- Fair evaluation: pass. The checker uses public `vin`/`vout` behavior and
  tolerant level windows rather than private structural assumptions.

## Checker And Evidence

- Checker id: `v3_017_slew_rate_limiter`
- Runner mapping: `CHECKS["v3_017_slew_rate_limiter"] = check_vbm1_slew_rate_limiter`
- Reference solution: PASS under EVAS and targeted Spectre.
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Public visible smoke: EVAS compile/transient smoke PASS.
- AHDL lint/read-in triage: EVAS AHDL-like lint preflight reports PASS with
  zero diagnostics for the hidden solution and starter cases. Spectre AHDL
  read-in reports no task-level `AHDLLINT-*`, AHDL compile, or VACOMP errors;
  the remaining `VACOMP-2435` and `SPECTRE-592` warnings are shared
  environment/mode notices.
