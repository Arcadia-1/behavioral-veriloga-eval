# EVAS/Spectre Parity Audit - 2026-05-08

Scope: Main120 MiMo-V2.5-Pro D rules-only candidates.

## Result

Original D audit had 7 EVAS/Spectre PASS mismatches. Two were strict-preflight misses and have been fixed:

| Task | Old EVAS | Spectre | Fix |
| --- | --- | --- | --- |
| `vbm1_sar_logic_4b_e2e` | PASS | FAIL_DUT_COMPILE | detect malformed empty control branches like `end else if (...) end` |
| `vbm1_voltage_clamp_tb` | PASS | FAIL_TB_COMPILE | detect uncontinued multiline source/PWL statements like `vsource ... wave=[` without `\\` |

After rerunning strict-EVAS with the new preflight, D was:

| Validator | PASS |
| --- | ---: |
| strict-EVAS-v2preflight | 18/120 |
| Spectre audit | 21/120 |

Remaining PASS mismatches before kernel repair: 5.

## Kernel Parity Repair

Implemented targeted EVAS kernel fixes for the five behavior-level mismatches:

- `cross()` exact-touch: a monotonic approach that lands exactly on the threshold now fires immediately, matching Spectre-style pulse tops at `vth`.
- Event body sampling: inside `@cross` bodies, only nodes participating in the triggering cross expression are evaluated at the interpolated crossing time; unrelated control nodes use the current accepted step value.
- Pulse source scheduling: pulse waveforms expose an internal edge midpoint breakpoint so simultaneous source edges are split into chronological event steps.

Validation after repair:

| Validator | PASS | PASS/FAIL mismatch vs Spectre |
| --- | ---: | ---: |
| strict-EVAS parityfix | 21/120 | 0/120 |
| Spectre audit | 21/120 | - |

Gold regression:

| Validator | PASS |
| --- | ---: |
| strict-EVAS parityfix on Main120 gold | 120/120 |

Remaining differences are failure-label taxonomy only, not binary pass/fail disagreements. There are 12 such cases, mostly `FAIL_DUT_COMPILE` vs `FAIL_TB_COMPILE` / `FAIL_SIM_CORRECTNESS` classification differences for already failing candidates.

Normalized label-only mismatch audit:

| Pair-level reason | Count |
| --- | ---: |
| `unsupported_or_nonstandard_symbol` | 6 |
| `tb_source_or_netlist_parse` | 4 |
| `conditional_transition_semantics` | 1 |
| `interface_source_drive` | 1 |

Artifacts:

```text
analysis/main120_d_evas_spectre_failure_label_mismatch_normalized_20260509.json
analysis/main120_d_evas_spectre_failure_label_mismatch_normalized_20260509.csv
analysis/main120_d_evas_normalized_failure_taxonomy_20260509.json
analysis/main120_d_spectre_normalized_failure_taxonomy_20260509.json
```

Important interpretation: per-backend normalized reasons may still differ when
one backend exposes only a generic compile/elaboration failure while the other
exposes the concrete source construct.  For EVAS/Spectre parity tables, the
canonical comparison is binary PASS/FAIL plus pair-level failure reason.  The
normalizer now includes backend diagnostics such as `spectre_errors`; after that
diagnostic pass, the D audit still has 12 raw label mismatches, 0 binary
PASS/FAIL mismatches, and 6 per-backend normalized reason mismatches.

EVAS diagnostic refinement:

- Added EVAS-side structured diagnostics for Spectre-aligned failure reasons:
  `source_unsupported_symbol`, `source_semantics_preflight`,
  `tb_source_parse`, `interface_preflight`, and generic compile/elaboration
  buckets.
- Runtime source errors such as `KeyError: '$abstime_step'` are now reported as
  `unsupported_or_nonstandard_symbol` with `axis=dut_compile`, rather than
  being counted as behavior failures.
- Targeted 10-task splice:
  `results/main120-D-spliced-evas-diagnostics-20260509`.
- Result: PASS remains 21/120, EVAS/Spectre binary PASS/FAIL mismatch remains
  0/120, and raw status-label mismatch drops from 12 to 6.

Targeted splice check:

- Base: old D strict-EVAS-v2preflight full root, 18/120 PASS.
- Patch: targeted parityfix rerun on the five historical PASS/FAIL mismatch tasks.
- Spliced output: `results/main120-D-spliced-parityfix-vs-spectre-20260508`.
- Checkpoint comparison: 0 status mismatches versus full EVAS parityfix checkpoint.
- Spectre comparison: 0 binary PASS/FAIL mismatches and 12 failure-label-only mismatches.

## Historical Remaining Mismatches Before Kernel Repair

| Task | EVAS | Spectre | Likely family |
| --- | --- | --- | --- |
| `vbm1_barrel_pointer_window_tb` | FAIL_SIM_CORRECTNESS | PASS | event/counter update under pulse reset/clock schedule |
| `vbm1_leaky_hold_bugfix` | PASS | FAIL_SIM_CORRECTNESS | `$abstime` continuous-state decay and solver timestep semantics |
| `vbm1_sar_logic_4b_bugfix` | FAIL_SIM_CORRECTNESS | PASS | `cross()` edge scheduling and integer/bitwise state update |
| `vbm1_sar_logic_4b_dut` | FAIL_SIM_CORRECTNESS | PASS | `cross()` edge scheduling and array-backed state update |
| `vbm1_track_hold_aperture_dut` | FAIL_SIM_CORRECTNESS | PASS | aperture sampling from `$abstime >= t_arm + delay` |

These are behavior-level parity gaps, not obvious Spectre-incompatible syntax. They should be handled through small focused parity cases before changing the EVAS kernel.

## Infrastructure Changes

`runners/validate_benchmark_v2_gold.py` now supports:

- `--resume`: reuse existing per-task `evas_result.json` / `spectre_result.json`.
- `--max-workers N`: local validator parallelism. Verified with real Spectre smoke at `N=2`.
- `--spectre-preflight-short-circuit`: development mode that skips real Spectre when strict preflight already proves incompatibility. Do not use this for final paper tables.

## Prompt Token Optimization

Added compact public Spectre rule mode:

- full: `--public-spec-mode spectre-strict-v3`
- compact: `--public-spec-mode spectre-strict-v3-compact`

Static prompt comparison on three Main120 tasks showed about 3029 characters saved per task. This is intended as a D-compact ablation, not a replacement for D until measured.

## Recommended Next Step

1. Use Spectre as the final metric for all headline tables.
2. Use strict-EVAS parityfix for fast development filtering; it now matches Spectre PASS/FAIL on this Main120 D audit.
3. Keep failure-label taxonomy separate from pass/fail parity, and normalize labels only if downstream analysis needs compile-vs-behavior ownership.
4. Run a small `D-compact` smoke before full Main120 to verify token reduction does not reduce compile/pass rates.
