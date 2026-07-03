# Task 013 Audit

Task: `013-resettable-integrator`

Status: independent L1 candidate. Gate 2 Cadence status is
`cadence_modeling_ready` for the reviewed gold after current-branch EVAS,
targeted Spectre, and AHDL warning triage.

## Four-Standard Review

- Useful scenario: pass. A resettable voltage-domain integrator is a common behavioral block for timers, accumulators, baseband conditioning, and mixed-signal control loops.
- Reasonable task: pass. The public prompt fixes the module name, port order, electrical ports, logic threshold, timer cadence, gain, reset polarity, clamp limits, and voltage-only implementation constraints.
- Complete tests: pass for EVAS/Spectre gold validation and EVAS negative
  recertification. The private validation deck exercises positive input drive,
  a long pre-reset integration window, an active-high reset pulse, reset
  clearing, and post-reset restart. The public smoke test is intentionally
  lighter and checks solver-visible compile/simulation viability.
- Fair evaluation: pass. Every behavior checked by the evaluator is stated in
  `instruction.md`; private material is limited to concrete stimulus, checker
  execution, reference solution, and negative variants.

## Boundary Check

- Agent-visible files: `instruction.md`, `starter/resettable_integrator.va`, and `test_visible/`.
- Private validation files: `solution/`, `test_hidden/`, `test_harness/`, and
  `negative_variants/`.
- No `meta.json` was added.

## Checker

- checker_id: `v3_013_resettable_integrator`
- check_name: `check_resettable_integrator`
- Runner mapping: `CHECKS["v3_013_resettable_integrator"] = check_vbm1_resettable_integrator`.

## Expected Results

- Reference solution result: PASS under EVAS and targeted Spectre.
- `neg_001`: expected `FAIL_SIM_CORRECTNESS`; integrates with gain `0.8e9`, too slow before reset and after reset.
- `neg_002`: expected `FAIL_SIM_CORRECTNESS`; updates every `2*dt` while accumulating one `dt`, so timer cadence is too slow.
- `neg_003`: expected `FAIL_SIM_CORRECTNESS`; subtracts the input and clamps at zero, so positive input does not integrate upward.
- `neg_004`: expected `FAIL_SIM_CORRECTNESS`; ignores active-high reset and does not clear the accumulated state.
- `neg_005`: expected `FAIL_SIM_CORRECTNESS`; drives `vout` at half the internal accumulator amplitude.

## Verification Performed

- Static self-consistency pass: visible and private SCS benches save `vin rst
  vout`; solution preserves the public module signature and uses
  `@(timer(...))` plus `transition(...)`; negative manifest hashes match current
  negative files; no `meta.json` exists.
- `python3 -m py_compile test_visible/tests/run_visible_smoke.py`: pass.
- EVAS/Python-engine reference solution smoke: PASS.
- Targeted Spectre gold validation: PASS with `v3_013_resettable_integrator`.
- AHDL lint/read-in triage: EVAS AHDL-like lint preflight reports PASS with
  zero diagnostics for the hidden solution and starter cases. Spectre AHDL
  read-in reports no task-level `AHDLLINT-*`, AHDL compile, or VACOMP errors;
  the remaining `VACOMP-2435` and `SPECTRE-592` warnings are shared
  environment/mode notices.
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`.
