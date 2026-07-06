# Task 008 Audit

Task: `008-gain-trim-controller`

Status: EVAS formal candidate.

## Four-Standard Review

- Useful scenario: pass. A clocked gain trim controller is a common calibration/control primitive for mixed-signal behavioral models.
- Reasonable task: pass. The public prompt fixes the DUT artifact, module name, port order, voltage-domain logic threshold, reset value, update edge, deadband, 50 mV step size, clamp range, and `transition()` output drive.
- Complete tests: pass for EVAS. The public visible deck is a compile/basic-behavior smoke. Private validation exercises reset, repeated upward correction to the high clamp, an in-deadband hold segment, repeated downward correction to the low clamp, and range bounding.
- Fair evaluation: pass for EVAS. Correctness requirements are stated in `instruction.md`; private validation varies stimulus without adding unstated behavior. The runner maps the v3 checker id to a task-specific trace checker.

## Agent/Evaluator Boundary

- Agent-visible files: `instruction.md`, `starter/gain_trim_controller.va`, and `test_visible/visible.scs`.
- Private validation files: `solution/gain_trim_controller.va`, validation decks, `CHECKS.yaml`, and `negative_variants/`.
- No `meta.json` is present or required.

## Checker Contract

- Checker id: `v3_008_gain_trim_controller`.
- Checker name: `check_v3_gain_trim_controller`.
- Runner mapping: `CHECKS["v3_008_gain_trim_controller"] = check_v3_gain_trim_controller`.
- Required trace columns: `time`, `gain_ctrl`.
- Validation sample times: 20 ns, 70 ns, 150 ns, 250 ns, 290 ns, 330 ns, 470 ns, 590 ns, and 650 ns.

Expected gold result:

- `solution/gain_trim_controller.va`: `PASS`, with reset near 0.30 V, monotonic increase under low measurement, high-clamp reach near 0.85 V, no update inside the +/-20 mV deadband, monotonic decrease under high measurement, and low-clamp reach near 0.05 V.

Expected negative results:

- `neg_001_stuck_midscale`: `FAIL_SIM_CORRECTNESS`; never updates after reset.
- `neg_002_inverted_direction`: `FAIL_SIM_CORRECTNESS`; feedback direction is reversed.
- `neg_003_wrong_step_size`: `FAIL_SIM_CORRECTNESS`; uses 40 mV steps instead of 50 mV.
- `neg_004_wrong_reset_level`: `FAIL_SIM_CORRECTNESS`; resets to 0.35 V instead of 0.30 V.
- `neg_005_missing_deadband_hold`: `FAIL_SIM_CORRECTNESS`; updates inside the required +/-20 mV deadband.

## Certification Evidence

- EVAS/Python-engine gold semantic validation: `PASS`.
- Concrete negative recertification: 5/5 manifest-declared expected failures, all `FAIL_SIM_CORRECTNESS`.
- The previous deadband-missing negative now fails because the hidden waveform includes an in-deadband segment and the checker samples the held control value.

## Remaining Risk

- Per SOP, paper-facing final certification still needs Spectre/Spectre-AX correlation or an explicit EVAS-only label.

## Window B Calibration Closeout

- Gate 2 status: `cadence_modeling_ready`.
- Evidence: Window B targeted review on 2026-07-03 recorded EVAS hidden gold PASS, manifest-declared concrete negatives rejected, AHDL-like lint PASS with 0 diagnostics, and targeted Spectre hidden gold PASS.
- Counting recommendation: retain as an independent gain-trim controller L1 row.
- This supersedes the earlier EVAS-only remaining-risk note for this category-level review; final release still requires the global denominator sweep.
