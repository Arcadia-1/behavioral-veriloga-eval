# EVAS/Spectre Conformance Backlog

Date: 2026-05-13

## Purpose

This backlog turns EVAS/Spectre disagreements into single-cause regression
targets. It is not a replacement for `vaBench-main`; it is the diagnostic layer
under the broad benchmark gate.

## Current Evidence Layers

| Layer | Evidence | Current conclusion |
| --- | --- | --- |
| Gold main120 EVAS | `results/vabench-main-v1-main120-gold-evas-2026-05-08/summary.json` | 120/120 PASS. |
| Gold main120 Spectre | `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08/summary.json` | 120/120 PASS. |
| Historical D old strict candidate parity | `results/main120-D-rulesonly-mimo-v2.5-pro-20260508-main120-D-evas-spectre.json` | 3 EVAS PASS / Spectre FAIL false positives. |
| D v2preflight candidate parity | `results/main120-D-rulesonly-mimo-v2.5-pro-20260508-main120-D-v2preflight-evas-spectre.json` | 1 EVAS PASS / Spectre FAIL false positive remains. |
| D parityfix splice | `results/main120-D-spliced-parityfix-vs-spectre-20260508/splice_comparisons.json` | 0 binary pass/fail mismatches. |

## Confirmed Conformance Regression Targets

These are the first cases to convert into atomic tests.

| Priority | Case | Evidence | Failure mode | Regression type | Current state |
| --- | --- | --- | --- | --- | --- |
| P0 | Empty control branch | `vbm1_sar_logic_4b_e2e` in old D strict parity | EVAS accepted a candidate that Spectre rejected due to an empty control branch. | Spectre syntax legality | Fixed by stricter preflight; needs atomic regression. |
| P0 | Uncontinued multiline source/PWL | `vbm1_voltage_clamp_tb` in old D strict parity | EVAS accepted a testbench source line that Spectre rejected because the multiline source was not continued legally. | Spectre source syntax | Fixed by stricter preflight; needs atomic regression. |
| P0 | `$abstime` continuous decay sampling | `vbm1_leaky_hold_bugfix` in D v2preflight parity | EVAS passed while Spectre failed on continuous decay behavior tied to solver-time sampling. | Solver-time sampling / behavioral semantics | Fixed in parityfix evidence; needs a small diagnostic regression. |
| P1 | Status-label mismatch after parityfix | `main120-D-spliced-parityfix-vs-spectre-20260508/splice_comparisons.json` | Binary agreement is clean, but several failure labels differ. | Failure taxonomy | Keep separate from binary parity; add label-level tests only if needed for reports. |

## Candidate Stress Semantics

These should be added only when they isolate a distinct simulator semantic. Many
historical LLM failures are model or prompt failures, not EVAS/Spectre bugs.

| Semantic | Candidate source | Why it matters | Test shape |
| --- | --- | --- | --- |
| `cross()` exact touch and tolerance | `cross_sine_precision_smoke`, EVAS engine tests | Cross timing can differ between event-driven and continuous-time simulators. | Tiny source ramp or sine with one threshold crossing and fixed tolerance. |
| Coincident timer and source breakpoint | timer-driven transition tests, PLL tasks | EVAS must order timer events and source knees predictably. | Minimal module with `@(timer())`, PWL edge, and a saved state. |
| `transition()` placement legality | strict preflight logs and EVAS tests | Spectre accepts some transition forms and rejects others. | Separate accepted and rejected VA snippets. |
| PWL bracket and continuation handling | `tests/test_pwl_statements.py`, source parser tests | Testbench syntax mistakes caused false positives historically. | Valid multiline PWL, invalid uncontinued PWL, empty PWL. |
| Checker timeout and missing CSV paths | `pfd_deadzone_smoke`, runtime failure reports | Some failures are checker/harness failures, not simulator disagreements. | Unit tests around checker failure classification. |

## Non-Conformance Stress Candidates

The following are useful benchmark stress cases, but should not be labeled as
EVAS/Spectre conformance failures unless a direct EVAS/Spectre disagreement is
reproduced on the same gold or candidate artifact:

- PLL lock and ratio-hop failures from model repair runs.
- DWA/window/element-shuffling behavior failures from generated candidates.
- ADC/DAC stuck-code failures from generated candidates.
- Sequence-generation failures such as LFSR or PRBS stuck transitions.
- Broad timeout failures where no Spectre-vs-EVAS binary mismatch has been
  isolated.

## Implementation Order

1. Add P0 syntax legality regressions first:
   - empty control branch,
   - uncontinued multiline source/PWL.
2. Add the P0 `$abstime`/continuous-decay behavioral regression.
3. Re-run EVAS unit tests and the affected `behavioral-veriloga-eval` pytest
   smoke tests.
4. Run the full `vaBench-main` broad gate when Spectre bridge access is
   available.
5. Promote P1 stress cases only when they cover a new simulator semantic rather
   than another model-generation failure.

## Acceptance Criteria

- Each conformance test has one intended failure cause.
- Each test explains whether EVAS should match Spectre by accepting, rejecting,
  or producing the same binary PASS/FAIL outcome.
- Broad `vaBench-main` parity remains the paper-facing gate.
- The invariant for audited slices is zero EVAS PASS / Spectre FAIL binary
  mismatches.
