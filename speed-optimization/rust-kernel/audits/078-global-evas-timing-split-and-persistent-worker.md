# 078 - Global EVAS Timing Split And Persistent Worker

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_stage78_global_timing_split_smoke_20260604.json`
- `speed-optimization/reports/rust_stage78_global_timing_split_smoke_20260604.md`
- `speed-optimization/reports/rust_stage78_persistent_worker_smoke_20260604.json`
- `speed-optimization/reports/rust_stage78_persistent_worker_smoke_20260604.md`
- `speed-optimization/reports/rust_stage78_persistent_worker_topwall10_20260604.json`
- `speed-optimization/reports/rust_stage78_persistent_worker_topwall10_20260604.md`

## One-Line Summary

停止继续加 benchmark 特例 fastpath，先把所有 EVAS benchmark 共用的 runner/subprocess 固定开销拆清楚，并提供 opt-in persistent EVAS worker 来复用已 import 的 EVAS 进程。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| speed harness timing | `Timing Split Totals` 只汇总外层 `run_case_*`，CSV/runner 内部计时只能从 `stdout_tail` 手工读 | `simulate_evas.run_case` 把 EVAS 自报的 tran/total、runner CSV/derive 计时桥接到 `timing_split` | 默认行为不变，只增加结构化 timing evidence |
| EVAS launch | 每个 row 都执行一次 `python -m evas simulate ...` | `VAEVAS_EVAS_PERSISTENT_WORKER=1` 时，每个 runner 线程复用一个 EVAS worker，通过 JSON line 发送 run request | 默认关闭；打开后 CSV/schema/checker 不变 |
| timeout/fallback | subprocess 自带 timeout | worker request 由 parent `Queue.get(timeout=...)` 监管，超时会 kill worker 并返回普通 failure | 默认 subprocess fallback 仍存在 |

## Principle

这次优化属于 **减少外层固定开销**，不是更改仿真数学内核。

原始路径每跑一个 benchmark 都要重新启动 Python 解释器、重新 import EVAS、重新进入 CLI。Rust whole-segment 已经把部分真实 row 的 tran 核心压到几十毫秒后，这个固定成本会盖过核心收益。persistent worker 的作用是让这些固定成本按一批任务摊销，而不是每行重复支付。

这不是针对 SAR、CPPLL、gain 之类任务的特例；任何通过 `simulate_evas.run_case()` 调用 EVAS 的 benchmark 都可以使用同一个 opt-in worker。

## Before / After Evidence

2-row same-runner smoke, same row source, same EVAS mode `profile_fast_rust_55`:

| Metric | Before: subprocess per row | After: persistent worker | Interpretation |
|---|---:|---:|---|
| rows PASS | 2/2 | 2/2 | function preserved |
| evaluator E2E wall | 2.763813 s | 1.440291 s | 1.92x faster on this smoke |
| EVAS subprocess/worker wall | 2.557692 s | 1.145133 s | 2.23x lower launch/runtime boundary |
| EVAS reported tran | 0.058100 s | 0.101500 s | core timing is not the optimized target here and is noisy |
| CSV write | 0.130675 s | 0.134761 s | unchanged bottleneck |
| behavior checker | 0.104321 s | 0.178422 s | unchanged/noisy bottleneck |
| subprocess unattributed | 2.257692 s | 0.762579 s | fixed process/import/CLI overhead greatly reduced |

10-row top-wall worker smoke:

| Metric | Value | Interpretation |
|---|---:|---|
| rows PASS | 10/10 | worker path preserves current benchmark behavior on top-wall slice |
| evaluator E2E wall | 3.072457 s | EVAS-only smoke, not a Spectre AX claim |
| EVAS worker wall | 1.740664 s | worker now below checker+CSV combined on this slice |
| EVAS reported tran | 0.412500 s | Rust whole-segment kernels are no longer dominant for many rows |
| CSV write | 0.659301 s | next global output-path target |
| behavior checker | 1.155738 s | next global checker/runtime target |
| worker unattributed | 0.583573 s | remaining startup/log/runner overhead after worker reuse |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`; unset `VAEVAS_EVAS_PERSISTENT_WORKER` to return to old subprocess-per-row behavior

## Validation

Commands run:

```bash
env PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_078 python3 -m py_compile behavioral-veriloga-eval/runners/simulate_evas.py
env PYTHONPATH=behavioral-veriloga-eval/runners PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_078 python3 -m pytest behavioral-veriloga-eval/tests/test_evas_output_cleanup.py -q
env VAEVAS_EVAS_PERSISTENT_WORKER=1 PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_078 python3 behavioral-veriloga-eval/runners/run_vabench_release_same_server_speed.py --speed-artifact behavioral-veriloga-eval/speed-optimization/reports/current_fourway_topwall10_clean_20260604.json --suite top-wall --limit 10 --skip-spectre --evas-mode profile_fast_rust_55 --output-root /private/tmp/vaevas_stage078_persistent_worker_topwall10_runs --report-json speed-optimization/reports/rust_stage78_persistent_worker_topwall10_20260604.json --report-md speed-optimization/reports/rust_stage78_persistent_worker_topwall10_20260604.md --timeout-s 180 --jobs 1
pgrep -af "simulate_evas.py --evas-worker"
```

Results:

```text
5 passed in 0.07s
10/10 profile_fast_rust_55 top-wall worker smoke PASS
pgrep found no leftover worker process
```

## Learning Notes

仿真速度里有两类时间：

- **核心仿真时间**：真正推进时间步、计算事件、更新节点电压的时间。
- **外层固定时间**：启动 Python、import 模块、解析 CLI、读写 CSV、跑 checker、整理 report 的时间。

当核心仿真很慢时，外层固定时间不显眼；当 Rust 把核心仿真压到几十毫秒后，外层固定时间就会变成主要瓶颈。persistent worker 就像把“每次都重新打开工具箱”改成“一次打开工具箱，连续处理多个电路”。它不改变电路数学，只减少重复启动和重复 import。

这也解释了为什么后续不能只盯着 Rust 内核：top-wall 10 worker smoke 里 tran 只有 0.4125 s，但 checker+CSV 已经是 1.8150 s。下一步全局收益应该来自 required-signal/sparse trace、CSV/record array path 和 checker runtime，而不是继续堆小型 case fastpath。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| worker protocol 被 EVAS stdout/strobe 污染 | JSON decode error or `evas_worker_protocol_error` in stderr | unset `VAEVAS_EVAS_PERSISTENT_WORKER` |
| worker timeout kills current worker | result note contains `evas_worker_timeout` | unset env or increase timeout; next call starts a new worker |
| thread worker leak in `--jobs > 1` | `pgrep -af "simulate_evas.py --evas-worker"` after run | registry/atexit cleanup closes all registered workers; default path unaffected |
| timing comparison overclaimed | report lacks Spectre strict/AX reference in worker smoke | keep this as EVAS-only engineering evidence, not paper-facing speed claim |

## Next Step

- `079 - required-signal/sparse trace and checker runtime`: reduce CSV write and checker input cost globally by emitting/reading only signals required by checker/user save contract.
