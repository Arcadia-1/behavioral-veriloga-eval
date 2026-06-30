# Honest SOP Audit: Task 011 PFD Up DN Logic

## Scope

Task boundary is one Verilog-A DUT, `pfd_updn.va`, plus EVAS/Spectre-compatible `.scs` testbenches.

Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. The evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present or required for this v3 task directory.

## Four Standards

- Useful scenario: PFD UP/DN reset-race logic is a common PLL clock-and-timing primitive. Correct direction and mutual reset behavior directly affect charge-pump control polarity and dead-zone behavior.
- Reasonable task: the public prompt states the exact module name, port order, 0/0.9 V logic convention, 0.45 V edge threshold, rising-edge-only behavior, REF-leading and DIV-leading reset-race behavior, VDD/VSS-referenced smoothed outputs, and prohibited current/dynamic operators.
- Complete tests: the visible smoke bench compiles the starter-facing DUT with public `ref`, `div`, `up`, and `dn` observables. The hidden bench saves `ref`, `div`, `up`, and `dn` over a 300 ns transient with both REF-leading and DIV-leading regions. The intended checker requires UP pulses when REF leads, DN pulses when DIV leads, bounded UP/DN overlap, and both outputs low after each reset race.
- Fair evaluation: hidden behavior follows directly from the public prompt and does not require unstated timing constants beyond robust 0.45 V logic interpretation and analog transition tolerance. Exact hidden PWL edge times remain private; the required behavior is public.

## Checker Contract

- `checker_id`: `v3_011_pfd_up_dn_logic`
- `check_name`: `check_pfd_reset_race`
- Runner mapping: `CHECKS["v3_011_pfd_up_dn_logic"] = check_pfd_reset_race` in `runners/simulate_evas.py`.
- Required CSV signals: `time`, `ref`, `div`, `up`, `dn`.

## Gold And Negative Expectations

- `solution/pfd_updn.va`: expected PASS under `v3_011_pfd_up_dn_logic` / `check_pfd_reset_race`.
- `neg_001.va`: expected FAIL; UP and DN output drives are swapped.
- `neg_002.va`: expected FAIL; REF-leading cycles do not clear both outputs when DIV arrives.
- `neg_003.va`: expected FAIL; DIV uses falling edges instead of rising edges.
- `neg_004.va`: expected FAIL; DIV incorrectly asserts UP, so DN pulses are missing.
- `neg_005.va`: expected FAIL; DIV-leading reset leaves UP asserted instead of clearing both outputs.

## Certification Status

EVAS formal candidate.

## Certification Evidence

- EVAS/Python-engine hidden gold smoke: `PASS`.
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`.
- The runner stages negative DUT files under the canonical artifact name from the top-level `TASKS.json` index, so the negative variants are scored by behavior rather than failing on include-file names.

## Remaining Risk

- Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
