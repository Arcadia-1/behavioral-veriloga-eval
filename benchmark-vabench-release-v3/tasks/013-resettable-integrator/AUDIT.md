# Task 013 Audit

Task: `013-resettable-integrator`

Status: EVAS formal candidate.

## Four-Standard Review

- Useful scenario: pass. A resettable voltage-domain integrator is a common behavioral block for timers, accumulators, baseband conditioning, and mixed-signal control loops.
- Reasonable task: pass. The public prompt fixes the module name, port order, electrical ports, logic threshold, timer cadence, gain, reset polarity, clamp limits, and voltage-only implementation constraints.
- Complete tests: pass for EVAS. The hidden SCS testbench exercises positive input drive, a long pre-reset integration window, an active-high reset pulse, reset clearing, and post-reset restart. The public smoke test is intentionally lighter and checks solver-visible compile/simulation viability without exposing hidden stimulus.
- Fair evaluation: pass for EVAS. Every behavior checked by the hidden evaluator is stated in `instruction.md`; hidden-only material is limited to concrete stimulus, checker execution, gold reference, and negative variants.

## Boundary Check

- Agent-visible files: `instruction.md`, `starter/resettable_integrator.va`, and `test_visible/`.
- Evaluator-only files: `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`.
- No `meta.json` was added.

## Checker

- checker_id: `v3_013_resettable_integrator`
- check_name: `check_resettable_integrator`
- Runner mapping: `CHECKS["v3_013_resettable_integrator"] = check_vbm1_resettable_integrator`.

## Expected Results

- Hidden gold result: `PASS`, `dut_compile=1.0`, `tb_compile=1.0`, `sim_correct=1.0`.
- `neg_001`: expected `FAIL_SIM_CORRECTNESS`; integrates with gain `0.8e9`, too slow before reset and after reset.
- `neg_002`: expected `FAIL_SIM_CORRECTNESS`; updates every `2*dt` while accumulating one `dt`, so timer cadence is too slow.
- `neg_003`: expected `FAIL_SIM_CORRECTNESS`; subtracts the input and clamps at zero, so positive input does not integrate upward.
- `neg_004`: expected `FAIL_SIM_CORRECTNESS`; ignores active-high reset and does not clear the accumulated state.
- `neg_005`: expected `FAIL_SIM_CORRECTNESS`; drives `vout` at half the internal accumulator amplitude.

## Verification Performed

- Static self-consistency pass: visible and hidden SCS benches save `vin rst vout`; solution preserves the public module signature and uses `@(timer(...))` plus `transition(...)`; negative manifest hashes match current negative files; no `meta.json` exists.
- `python3 -m py_compile test_visible/tests/run_visible_smoke.py`: pass.
- EVAS/Python-engine hidden gold smoke: `PASS`.
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`.

## Remaining Risk

- Spectre/Spectre-AX correlation has not been run from this working tree; per SOP, use EVAS-only wording until that evidence exists.
