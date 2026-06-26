# Task 050 Audit

Task: `050-bin-to-thermometer-decoder-8b`

Status: support formal candidate for EVAS-based evaluation.

## Four-Standard Review

- Useful scenario: pass. An 8-bit binary-to-thermometer utility is a common analog/mixed-signal testbench building block for DAC arrays, element selection, and encoded stimulus expansion.
- Reasonable task: pass. The public prompt fixes the exact vector Verilog-A port order, voltage logic threshold, enable behavior, binary bit order, cumulative thermometer direction, and boundary behavior for codes 0 and 255.
- Complete tests: pass for EVAS formal-candidate scope. The hidden `.scs` testbench exercises enabled codes `0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255` plus an enable-low segment. The checker samples away from transitions and verifies high count, cumulative order from `th0`, enable gating, and required boundary cases.
- Fair evaluation: pass for the stated prompt. Every hidden scoring requirement is stated in `instruction.md`; the public smoke only checks compile/basic simulation and does not expose the hidden code sequence.

## Evidence

- Public visible smoke: `VISIBLE_SMOKE_PASS` in the EVAS container.
- Hidden gold: `PASS`, `dut_compile=1.0`, `tb_compile=1.0`, `sim_correct=1.0`.
- Hidden gold checker note: `checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, -1] boundary_seen=[0, 1, 255] enable_low_ok=True count_errors=0 cumulative_errors=0`.
- Concrete negative variants: 5/5 rejected as `FAIL_SIM_CORRECTNESS` with `dut_compile=1.0` and `tb_compile=1.0`.

Negative coverage:

- `neg_001_off_by_one_count`: rejects `code+1` high outputs.
- `neg_002_reversed_thermometer_bus`: rejects thermometer direction from `th255` downward.
- `neg_003_enable_ignored`: rejects ignoring `en`.
- `neg_004_missing_top_cell`: rejects one fewer high output.
- `neg_005_reversed_bit_order`: rejects swapped binary bit significance.

## Interface Cleanup

- The task now uses Verilog-A vector ports to keep the benchmark focused on behavior rather than mechanical scalar-port expansion. Existing EVAS testbenches still save the same scalar node columns for checker compatibility.

## Remaining Risk

- This audit is EVAS-only. Per SOP, paper-facing final certification still needs Spectre/Spectre-AX correlation or an explicit EVAS-only label.
- No model positive run has been attached yet, so this is not an A-tier core-score claim. It is ready to move out of staging as a support formal candidate.

Certification status: certified with EVAS gold PASS and concrete negative FAIL_SIM_CORRECTNESS evidence.
