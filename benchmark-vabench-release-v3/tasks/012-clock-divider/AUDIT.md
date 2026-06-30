# Task 012 Audit

Task: `012-clock-divider`

Status: EVAS formal candidate.

## Four-Standard Review

- Useful scenario: pass. A programmable voltage-domain feedback divider is a realistic PLL/ADPLL behavioral primitive, and the task exercises edge timing, reset acquisition, ratio decode, and lock signaling.
- Reasonable task: pass. The public prompt fixes the exact target artifact, module name, scalar electrical port order, voltage logic convention, LSB-first ratio decode, divide-by-1 behavior, reset behavior, output-period contract, odd-ratio high/low segmentation, lock acquisition, and forbidden analog operators.
- Complete tests: pass for EVAS. Visible smoke is independent and solver-visible, while hidden materials include the formal SCS testbench, checker config, gold reference, and five concrete behavioral negatives. EVAS hidden gold and all five negatives have been run through the target v3 runner.
- Fair evaluation: pass for EVAS. Hidden scoring requirements are stated as public behavior in `instruction.md`; the exact hidden stimulus is not disclosed. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`.

## Boundary Check

- Agent-visible: `instruction.md`, `starter/clk_divider_ref.va`, `test_visible/`.
- Evaluator-only: `solution/clk_divider_ref.va`, `test_hidden/`, `test_harness/`, `negative_variants/`.
- No `meta.json` is present or required.
- Single target artifact: `clk_divider_ref.va`.

## Checker Wiring

- checker_id: `v3_012_clock_divider`
- check_name: `check_clk_divider`
- Runner mapping: `CHECKS["v3_012_clock_divider"] = check_clk_divider`

## Expected Results

- Gold solution: `PASS`, with `dut_compile=1.0`, `tb_compile=1.0`, and `sim_correct=1.0`.
- `neg_001`: expected `FAIL_SIM_CORRECTNESS`; drops `div_code_2`, so ratio code decode is wrong.
- `neg_002`: expected `FAIL_SIM_CORRECTNESS`; divides by decoded ratio plus one.
- `neg_003`: expected `FAIL_SIM_CORRECTNESS`; decodes ratio bits in reverse order.
- `neg_004`: expected `FAIL_SIM_CORRECTNESS`; plausible divided clock but `lock` never asserts.
- `neg_005`: expected `FAIL_SIM_CORRECTNESS`; asserts `lock` but `clk_out` is not periodic.

## Certification Evidence

- EVAS/Python-engine hidden gold smoke: `PASS`.
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`.
- The runner stages negative DUT files under the canonical artifact name from the top-level `TASKS.json` index, so the negative variants are scored by behavior rather than failing on include-file names.

## Remaining Risk

- For paper-facing certification, run or attach Spectre/Spectre-AX correlation evidence, or label the task EVAS-only.
