# 074 - Rust55 Top-Wall EVAS Smoke

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related files:

- `speed-optimization/reports/rust_stage74_topwall_evas_smoke_20260604.json`
- `speed-optimization/reports/rust_stage74_topwall_evas_smoke_20260604.md`
- Raw local artifact: `/private/tmp/vaevas_exp074_topwall10_evas_only.json`
- Raw local artifact: `/private/tmp/vaevas_exp074_strict_missing_fastpath.json`
- Raw local artifact: `/private/tmp/vaevas_exp074_missing_fastpath.json`

## One-Line Summary

按分阶段实验节奏先跑 EVAS-only top-wall smoke：Rust55 在 whole-segment production fastpath 命中的 row 上有明显收益，但在 gain measurement flow 和 PFD 这类未启用 fastpath 的 row 上基本回到 Python fast。

## What Was Run

| Experiment | Scope | Modes | Purpose |
|---|---:|---|---|
| Missing-fastpath smoke | 3 unique rows | `profile_fast_skip_source_error_control`, `profile_fast_rust_55`, `profile_fast_event_trace_audit` | 先定位没有 production fastpath 的 top-wall row |
| Missing-fastpath strict rerun | 3 unique rows | `strict_current`, `profile_fast_skip_source_error_control`, `profile_fast_rust_55` | 补 strict baseline 和 strict parity gate |
| Top-wall EVAS smoke | 6 unique rows | `strict_current`, `profile_fast_skip_source_error_control`, `profile_fast_rust_55` | 看当前 Rust55 在真实 top-wall slice 的有效覆盖和剩余瓶颈 |

这些实验都是本地 EVAS-only 工程证据。它们可以指导下一轮内核优化，但不能替代 same-server Spectre AX speed claim。

## Top-Wall Result

Canonical report:

```text
speed-optimization/reports/rust_stage74_topwall_evas_smoke_20260604.md
speed-optimization/reports/rust_stage74_topwall_evas_smoke_20260604.json
```

| Mode | PASS | Total wall s | Speedup vs strict |
|---|---:|---:|---:|
| `strict_current` | 6/6 | `121.458` | `1.00x` |
| `profile_fast_skip_source_error_control` | 6/6 | `9.030` | `13.45x` |
| `profile_fast_rust_55` | 6/6 | `3.750` | `32.39x` |

Rust55 vs normal fast total speedup on this EVAS-only slice is `2.41x`.

## Where Rust55 Helped

| Row | Fast s | Rust55 s | Rust55 / fast | Reason |
|---|---:|---:|---:|---|
| `vbr1_l1_propagation_delay_comparator/dut` | `1.384` | `0.178` | `7.78x` | Whole-segment comparator trace production path enabled |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/tb` | `2.517` | `0.539` | `4.67x` | CPPLL reacquire trace production path enabled |
| `vbr1_l2_weighted_sar_adc_dac_loop/tb` | `2.666` | `0.590` | `4.52x` | SAR loop whole-segment production path enabled |

These rows have `rust_full_model_fastpath_enabled=1`, zero model/source breakpoint scan counters in the Rust55 path, and nonzero Rust whole-segment point counters.

## Where Rust55 Did Not Help

| Row | Fast s | Rust55 s | Rust55 / fast | Main counters |
|---|---:|---:|---:|---|
| `vbr1_l1_pfd_up_dn_logic/bugfix` | `0.172` | `0.174` | `0.99x` | Tiny row; `383` steps, `770` transition calls |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e` | `1.121` | `1.143` | `0.98x` | `16236` steps, `48714` transition calls, `32472` model/source breakpoint scans |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/tb` | `1.170` | `1.127` | `1.04x` | Same transition and breakpoint pattern as e2e |

These rows report `rust_full_model_fastpath_available=1` but `rust_full_model_fastpath_enabled=0`. In plain terms: the compiler/runtime can see some Rust-related metadata, but the production Rust whole-segment executor is not actually taking over the row.

## Historical AX Anchor

For orientation only, the same six rows have historical `spectre/ax_speed` wall total `28.599s` in `current_fourway_topwall10_clean_20260604.json`; this run's Rust55 EVAS-only total is `3.750s`. The directional ratio is `7.63x`.

This is not claimable because the AX rows and this Rust55 run are not a newly generated same-server artifact with both modes. The 073 claim gate remains correct: Spectre AX speed claim stays closed until a same-server rerun includes `profile_fast_rust_55`.

## Interpretation

The Rust mechanism is not inherently ineffective. It is very effective when an entire hot segment moves into Rust:

1. Python generated model calls disappear for the covered segment.
2. Per-step source/model breakpoint scans disappear or are replaced by typed-array loop state.
3. Transition/event/output writes are emitted as a precomputed trace rather than repeated Python object operations.
4. Record/checker/CSV overhead remains visible, but it no longer dominates the covered heavy rows.

The current defect is coverage, not the Rust ABI itself. The top remaining Rust55 wall in this slice is the gain extraction measurement-flow tb/e2e pair, which together account for about 60% of Rust55 top-wall wall time.

## Next Step

Do not spend the next step on full AX rerun yet. The next engineering target should be:

1. Lower `vbr1_l2_gain_extraction_convergence_measurement_flow` into a production Rust whole-segment path, or produce a concrete blocker explaining why it cannot be safely lowered.
2. Rerun the same EVAS-only top-wall smoke.
3. If the gain rows move from Python fast into Rust55 and still pass strict parity, then run a small same-server Spectre AX smoke.
4. Only after the small AX smoke is stable should we run a full same-server AX rerun and re-open the 073 AX claim gate.

## Validation

Commands run:

```bash
PYTHONPATH=EVAS:behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_exp074 \
python3 behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact behavioral-veriloga-eval/speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --entry vbr1_l2_gain_extraction_convergence_measurement_flow \
  --entry vbr1_l1_pfd_up_dn_logic \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_55 \
  --mode profile_fast_event_trace_audit \
  --output-root /private/tmp/vaevas_exp074_missing_fastpath \
  --report-json /private/tmp/vaevas_exp074_missing_fastpath.json \
  --report-md /private/tmp/vaevas_exp074_missing_fastpath.md \
  --timeout-s 240 --jobs 1

PYTHONPATH=EVAS:behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_exp074b \
python3 behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact behavioral-veriloga-eval/speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --entry vbr1_l2_gain_extraction_convergence_measurement_flow \
  --entry vbr1_l1_pfd_up_dn_logic \
  --mode strict_current \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_55 \
  --output-root /private/tmp/vaevas_exp074_strict_missing_fastpath \
  --report-json /private/tmp/vaevas_exp074_strict_missing_fastpath.json \
  --report-md /private/tmp/vaevas_exp074_strict_missing_fastpath.md \
  --timeout-s 240 --jobs 1

PYTHONPATH=EVAS:behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_exp074_topwall \
python3 behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact behavioral-veriloga-eval/speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --mode strict_current \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_55 \
  --output-root /private/tmp/vaevas_exp074_topwall10_evas_only \
  --report-json /private/tmp/vaevas_exp074_topwall10_evas_only.json \
  --report-md /private/tmp/vaevas_exp074_topwall10_evas_only.md \
  --timeout-s 300 --jobs 1
```

Results:

```text
missing-fastpath smoke: 3/3 PASS
missing-fastpath strict rerun: 3/3 PASS, 3/3 safe_vs_strict
top-wall EVAS smoke: 6/6 PASS, 6/6 safe_vs_strict for Rust55
summary JSON validation: PASS via python3 -m json.tool
```
