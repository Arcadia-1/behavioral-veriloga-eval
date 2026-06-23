# 079 - Required-Signal Global Trace

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_stage79_required_trace_topwall10_20260604.json`
- `speed-optimization/reports/rust_stage79_required_trace_topwall10_20260604.md`
- Controlled trace-off comparison:
  - `speed-optimization/reports/rust_stage79_required_trace_disabled_topwall10_20260604.json`
  - `speed-optimization/reports/rust_stage79_required_trace_disabled_topwall10_20260604.md`
- Baseline for comparison: `speed-optimization/reports/rust_stage78_persistent_worker_topwall10_20260604.json`

## One-Line Summary

把 EVAS trace 从“默认记录/写出 save 列或全部节点”扩展为“checker 声明必要观测信号，harness 下发给 EVAS，EVAS 只 record/write 这些信号”的全局机制。

## What Changed

| Layer | Before | After | Default impact |
|---|---|---|---|
| checker contract | streaming checker 的 required columns 只藏在函数内部 | `required_trace_signals_for_checker()` 统一暴露 checker 需要的信号集合 | 未注册 checker 返回空集合 |
| harness -> EVAS | `run_case()` 不告诉 EVAS checker 只需要哪些信号 | `run_case()` 通过 `EVAS_REQUIRED_TRACE_SIGNALS` 下发 required-signal contract | 只对有显式 contract 的 streaming checker 生效 |
| persistent worker | worker 环境变量可能跨请求残留 | 每个 request 设置/恢复 `EVAS_REQUIRED_TRACE_SIGNALS` | 防止上一条任务污染下一条 |
| EVAS record/write | 有 `save` 时按 save，没 `save` 时记录全部节点 | 有 required trace contract 时按 contract 选择 record nodes 和 CSV columns | CLI 默认行为不变；harness opt-in |
| evidence | CSV/checker 只能看 wall time | EVAS log 增加 `Trace counters:`，报告可读到 record/csv signal count | 便于审计实际少写了多少列 |

## Principle

这一步不是改变仿真数学，也不是 Rust fastpath。它减少的是 **trace 数据面**：

1. EVAS 每个时间点会把被 record 的节点电压追加到数组。
2. 仿真结束后 `_write_csv()` 把这些数组写成 `tran.csv`。
3. checker 再从 `tran.csv` 读取它需要的列。

如果 checker 只需要 4 个信号，而 EVAS 写了 20 个或全部节点，那么多出来的列不会增加正确性，只会增加数组 append、CSV 格式化、磁盘写入、CSV 读取和字符串解析成本。required-signal trace 的作用就是让“checker 需要什么”成为全局合约，而不是让每个 benchmark 写一个特殊 fastpath。

## Controlled A/B Evidence

Same current code, same local top-wall 10 EVAS-only slice, same mode `profile_fast_rust_55`, both with persistent worker. The only intentional switch is `VAEVAS_DISABLE_REQUIRED_TRACE=1` for the trace-off control.

| Metric | Trace off | Trace on | Change |
|---|---:|---:|---:|
| rows PASS | 10/10 | 10/10 | preserved |
| evaluator E2E wall | 2.526897 s | 2.023591 s | 1.25x faster |
| EVAS worker wall | 1.631964 s | 1.186777 s | 1.38x faster |
| EVAS reported total | 1.300000 s | 0.900000 s | 1.44x faster |
| EVAS reported tran | 0.670500 s | 0.296700 s | 2.26x faster |
| CSV write | 0.518620 s | 0.403575 s | 1.29x faster |
| behavior checker | 0.750431 s | 0.699490 s | 1.07x faster |
| subprocess/worker unattributed | 0.389376 s | 0.375595 s | 1.04x faster |

The main direct and repeatable effect is lower EVAS trace/CSV work. Checker time also decreases mildly because less CSV data reaches the checker path. Some per-row wall numbers are still noisy because this is a local EVAS-only smoke, so the controlled A/B is engineering evidence, not a paper-facing AX speed claim.

## Historical Stage78 / Stage79 Comparison

Same local top-wall 10 EVAS-only slice, same mode `profile_fast_rust_55`, both with persistent worker. Stage79 uses the new required-signal trace; Stage78 is the previous worker baseline.

| Metric | Stage78 worker baseline | Stage79 required trace | Change |
|---|---:|---:|---:|
| rows PASS | 10/10 | 10/10 | preserved |
| evaluator E2E wall | 3.072457 s | 2.023591 s | 1.52x faster |
| EVAS worker wall | 1.740664 s | 1.186777 s | 1.47x faster |
| EVAS reported total | 1.200000 s | 0.900000 s | 1.33x faster |
| EVAS reported tran | 0.412500 s | 0.296700 s | 1.39x faster |
| CSV write | 0.659301 s | 0.403575 s | 1.63x faster |
| behavior checker | 1.155738 s | 0.699490 s | 1.65x faster |
| subprocess/worker unattributed | 0.583573 s | 0.375595 s | 1.55x faster |

Per-row column/count evidence:

| Row | Old CSV columns | New CSV columns | Trace contract columns | Main effect |
|---|---:|---:|---:|---|
| weighted SAR ADC loop/tb | 20 | 19 | 19 | removes unused `dout_code`; main checker gain likely from lower worker/cache noise plus narrower trace path |
| gain extraction flow/tb | 4 | 4 | 4 | same columns, but trace contract bypasses unrelated save/default path |
| gain extraction flow/e2e | 4 | 4 | 4 | same |
| propagation delay comparator/dut | 6 | 6 | 6 | same |
| pfd reset race/bugfix | 4 | 4 | 4 | same |
| CPPLL/tb | 5 | 4 | 4 | drops unused `dco_clk` |
| LFSR PRBS/dut | 12 | 11 | 11 | drops derived `state_code` |
| CPPLL/e2e | 5 | 4 | 4 | drops unused `dco_clk` |
| gain estimator/tb | 6 | 6 | 6 | same |
| gain estimator/e2e | 6 | 6 | 6 | same |

Interpretation: this top-wall slice was already mostly save-narrowed, so column-count reduction is modest. The controlled A/B above is the better estimate of this patch alone. The Stage78 comparison remains useful as a before/after engineering checkpoint, but it also includes normal local runtime noise and previous-artifact differences.

## Functional Safety

- Default EVAS CLI behavior changed: `no`
- Harness behavior changed for validated streaming checkers: `yes`, output is checker-required trace instead of all saved extras
- Checker result changed: `no`, top-wall 10 remains PASS
- Precision/math changed: `no`
- Fallback exists: `yes`; set `VAEVAS_DISABLE_REQUIRED_TRACE=1` to disable harness trace contracts

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile EVAS/evas/netlist/runner.py
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile behavioral-veriloga-eval/runners/simulate_evas.py
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=behavioral-veriloga-eval/runners python3 -m pytest behavioral-veriloga-eval/tests/test_evas_output_cleanup.py -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=behavioral-veriloga-eval/runners VAEVAS_EVAS_PERSISTENT_WORKER=1 python3 behavioral-veriloga-eval/runners/run_vabench_release_same_server_speed.py --speed-artifact behavioral-veriloga-eval/speed-optimization/reports/current_fourway_topwall10_clean_20260604.json --suite top-wall --limit 10 --skip-spectre --evas-mode profile_fast_rust_55 --output-root /private/tmp/vaevas_stage079_required_trace_topwall10_runs --report-json speed-optimization/reports/rust_stage79_required_trace_topwall10_20260604.json --report-md speed-optimization/reports/rust_stage79_required_trace_topwall10_20260604.md --timeout-s 300 --jobs 1
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=behavioral-veriloga-eval/runners VAEVAS_EVAS_PERSISTENT_WORKER=1 VAEVAS_DISABLE_REQUIRED_TRACE=1 python3 behavioral-veriloga-eval/runners/run_vabench_release_same_server_speed.py --speed-artifact behavioral-veriloga-eval/speed-optimization/reports/current_fourway_topwall10_clean_20260604.json --suite top-wall --limit 10 --skip-spectre --evas-mode profile_fast_rust_55 --output-root /private/tmp/vaevas_stage079_required_trace_disabled_topwall10_runs --report-json speed-optimization/reports/rust_stage79_required_trace_disabled_topwall10_20260604.json --report-md speed-optimization/reports/rust_stage79_required_trace_disabled_topwall10_20260604.md --timeout-s 300 --jobs 1
```

Results:

```text
7 passed in 0.05s
10/10 profile_fast_rust_55 top-wall required-trace smoke PASS
10/10 profile_fast_rust_55 top-wall trace-off control PASS
```

## Learning Notes

可以把 trace 理解成“仿真时顺手拍照”。以前很多任务是“每一步把所有能看到的东西都拍下来”，但 checker 最后只检查其中几张照片。现在改成 checker 先告诉 EVAS：“我只需要这些镜头”，EVAS 就只保存这些镜头。

这不影响电路怎么被仿真，因为节点电压、事件、状态更新仍然照常计算；它只影响最终保留哪些观测量给 checker。也因此它属于全局 runtime/IO 优化，不是某个电路模型的数学优化。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| checker contract 少列 | result fails with `missing_columns=...` | add missing signal to checker contract or set `VAEVAS_DISABLE_REQUIRED_TRACE=1` |
| dynamic-header checker 被错误收窄 | streaming checker falls back/fails unexpectedly | keep dynamic checkers off the contract map until required columns are explicit |
| persistent worker env leak | later row uses previous trace set | request-scoped env restore added; disable worker if suspected |
| overclaim speed | report is EVAS-only and local | keep this as engineering evidence, not Spectre AX speed claim |

## Next Step

- Move record/CSV arrays closer to an indexed array path so required trace avoids Python dict/string lookups at every record point.
- For dynamic checkers such as CDAC calibration, make their observable contract explicit before enabling sparse trace.
