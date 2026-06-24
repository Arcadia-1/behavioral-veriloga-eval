# Task 057 Audit

Task: `057-signed-magnitude-to-twos-complement-8b`

Status: support formal candidate for EVAS-based evaluation.

## Four-Standard Review

- Useful scenario: pass. `Signed Magnitude To Twos Complement 8b` is a reusable analog/mixed-signal testbench utility.
- Reasonable task: pass. The public prompt fixes the exact scalar port order, logic threshold, output encoding, and invalid-state behavior when applicable.
- Complete tests: pass for EVAS formal-candidate scope. Hidden tests cover boundary values, representative interior values, and invalid/gating cases when applicable.
- Fair evaluation: pass for the stated prompt. Hidden scoring requirements are stated in `instruction.md`; public smoke only checks compile/basic simulation viability.

## Evidence

- Hidden gold expected result: `PASS`, `dut_compile=1.0`, `tb_compile=1.0`, `sim_correct=1.0`.
- Positive vectors: +/-0,+/-1,+/-2,+/-63,+/-127.
- Concrete negative variants: 5 expected rejections.

Negative coverage:

- `neg_001`: rejected as `FAIL_SIM_CORRECTNESS`.
- `neg_002`: rejected as `FAIL_SIM_CORRECTNESS`.
- `neg_003`: rejected as `FAIL_SIM_CORRECTNESS`.
- `neg_004`: rejected as `FAIL_SIM_CORRECTNESS`.
- `neg_005`: rejected as `FAIL_SIM_CORRECTNESS`.

## Remaining Risk

- This audit is EVAS-only. Per SOP, paper-facing final certification still needs Spectre/Spectre-AX correlation or an explicit EVAS-only label.
- No model positive run has been attached yet, so this is not an A-tier core-score claim. It is ready to move out of staging as a support formal candidate.

Certification status: certified with EVAS gold PASS and concrete negative FAIL_SIM_CORRECTNESS evidence.
