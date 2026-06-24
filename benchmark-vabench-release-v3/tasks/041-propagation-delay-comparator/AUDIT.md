# Honest SOP Audit: Task 041 Propagation Delay Comparator

## Scope

Task boundary is Verilog-A DUT artifact `cmp_delay.va` plus evaluator-supplied companion artifact `edge_interval_timer.va` and EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. Input-dependent comparator propagation delay is a practical behavioral model for decision circuits.
- Reasonable task: pass. The public prompt fixes clocked comparison, output transition, and larger delay for smaller differential input.
- Complete tests: pass for EVAS. Hidden samples check output assertion and delay ordering across differential-input phases. Five concrete negatives cover fixed delay, inverted comparison, missing transition, missing edge timing behavior, and stuck output.
- Fair evaluation: pass for EVAS. The checker uses public voltage and timing observables; companion timing support is supplied by the evaluator so the agent only owns the comparator DUT.

## Checker And Evidence

- Checker id: `v3_041_propagation_delay_comparator`
- Runner mapping: `CHECKS["v3_041_propagation_delay_comparator"] = check_cmp_delay`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been rerun from this working tree; use EVAS-only wording unless fresh dual-simulator evidence is attached.
