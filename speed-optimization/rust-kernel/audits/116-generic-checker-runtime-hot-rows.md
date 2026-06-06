# 116 - Generic Checker Runtime Hot Rows

Status: `done`

Date: `2026-06-06`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/checker_runtime_116_rowbased_20260606.json`
- `speed-optimization/reports/checker_runtime_116_streaming_20260606.json`
- `speed-optimization/reports/checker_runtime_116_rowbased_20260606.md`
- `speed-optimization/reports/checker_runtime_116_streaming_20260606.md`

## One-Line Summary

把 checker-heavy 的 rectifier、stimulus sequencer、window comparator 迁到通用 `CsvCheckerRuntime`，并给 sparse trace 预留可配置的额外调试列。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| CSV checker runtime | 每个 streaming checker 自己打开 CSV、建 header index、插值或重采样 | 新增 `CsvCheckerRuntime`，统一 header alias、required/missing、row streaming、series、window mean、插值采样和 resample rows | checker 判断口径不变；新增 checker 应复用 runtime |
| hot checker coverage | rectifier、stimulus sequencer、window comparator 仍大量走 row-list checker | 三类 checker 的 release forms 进入 `STREAMING_BEHAVIOR_CHECKS` 和 `_STREAMING_TRACE_REQUIREMENTS_BY_FUNC` | 这些 row 默认走 parity-validated streaming checker |
| release checker id | release entry base id 有 streaming registration 但未必在 `CHECKS` 可直接执行 | `RELEASE_CHECK_ALIASES` 同时注册 entry id 和 `_dut/_tb/_bugfix/_e2e` forms | base/form checker 口径一致；不覆盖已有显式 checker |
| debug columns | sparse trace 只保留 checker required columns，人工想多看列时要关掉 sparse trace | 新增 `VAEVAS_EXTRA_TRACE_SIGNALS*` 机制，把额外列追加到已有 sparse contract | 可以保留少量 debug/diagnostic columns，不必退回 full trace |
| stale helper | `_stream_samples_at_times()` 是单 checker 风格的旧实现 | 删除旧 helper，采样统一走 `CsvCheckerRuntime.samples_at()` | 减少后续 checker 分叉实现 |

## Principle

这次解决的是 **checker / harness 长尾**，不是 EVAS Rust 内核语义迁移。

row-based checker 的老流程是：先把整张 `tran.csv` 读成 Python row dict，再在 checker 内部反复扫描、采样、重采样。对这些 row 来说，EVAS2 subprocess 往往只有几十毫秒到几百毫秒，而 checker 会花 0.8s 到 1.6s。也就是说，仿真已经结束了，等待时间主要卡在 Python CSV/checker。

`CsvCheckerRuntime` 的做法是把公共动作集中起来：

- header 只解析一次，并复用已有 signal alias/canonical name 规则；
- checker 以流式 rows 读取 CSV，不需要先构造完整 row dict list；
- 常见窗口均值、时间插值、固定采样点读取、重采样 rows 都变成 runtime primitive；
- 每个 checker 只写自己的行为判定，不再复制 CSV 读表代码。

这不是为了改变精度。它只是把“读取多少列、怎样取样、怎样避免 Python object 构造”统一起来，让 checker 不再成为 E2E 的最大等待项。

## Extra Columns Contract

默认 sparse trace 只输出 checker 必需列。为了人工调试，有时需要多看几个内部节点或诊断列，这次预留了三个入口：

| Env var | Scope | Example |
|---|---|---|
| `VAEVAS_EXTRA_TRACE_SIGNALS` | 所有已有 sparse trace | `debug_a,debug_b` |
| `VAEVAS_EXTRA_TRACE_SIGNALS_BY_TASK` | exact task id、release entry prefix、或 `prefix*` | `vbr1_l1_precision_rectifier_envelope_detector=debug_env` |
| `VAEVAS_EXTRA_TRACE_SIGNALS_<TASK_ID>` | 单 task exact escape hatch，task id 会转成大写下划线 | `VAEVAS_EXTRA_TRACE_SIGNALS_VBR1_L1_PRECISION_RECTIFIER_ENVELOPE_DETECTOR_TB=debug_exact` |

安全边界：额外列只会追加到 **已经有 base sparse contract** 的 checker。未知 checker 不会因为设置了 extra env 就生成一个过窄 sparse trace。

## Before / After Evidence

对照口径：

- Before：同一 10-row smoke，设置 `VAEVAS_DISABLE_VALIDATED_FAST_CHECKERS=1`，强制走 row-based checker。
- After：同一 10-row smoke，默认启用 validated streaming checker。
- EVAS mode：`profile_fast_evas2`
- Spectre：未运行；本次只验证 EVAS checker/runtime 层。
- Rows：rectifier 4 forms、window comparator 4 forms、stimulus sequencer 2 forms。

| Metric | Row-based | Generic runtime | Speedup / delta | Interpretation |
|---|---:|---:|---:|---|
| rows PASS | 10/10 | 10/10 | unchanged | checker 语义保持一致 |
| E2E wall total | 16.388s | 4.349s | 3.77x / -12.039s | checker 长尾被消掉后，总等待明显下降 |
| behavior checker | 11.618s | 0.221s | 52.57x / -11.397s | 主要收益来源 |
| EVAS subprocess wall | 4.579s | 3.987s | 1.15x / -0.592s | 内核/子进程不是这轮主收益 |
| CSV write | 0.137s | 0.129s | 1.06x / -0.008s | 写 CSV 只小幅变化 |

Per-row checker wall:

| Row | Row-based checker | Generic runtime checker | Notes |
|---|---:|---:|---|
| `vbr1_l1_precision_rectifier_envelope_detector_bugfix` | 1.195s | 0.029s | streaming_validated |
| `vbr1_l1_precision_rectifier_envelope_detector_dut` | 1.271s | 0.030s | streaming_validated |
| `vbr1_l1_precision_rectifier_envelope_detector_e2e` | 1.201s | 0.029s | streaming_validated |
| `vbr1_l1_precision_rectifier_envelope_detector_tb` | 1.416s | 0.029s | streaming_validated |
| `vbr1_l1_window_comparator_detector_bugfix` | 1.597s | 0.015s | streaming_validated |
| `vbr1_l1_window_comparator_detector_dut` | 1.124s | 0.011s | streaming_validated |
| `vbr1_l1_window_comparator_detector_e2e` | 0.925s | 0.016s | streaming_validated |
| `vbr1_l1_window_comparator_detector_tb` | 0.943s | 0.011s | streaming_validated |
| `vbr1_l2_programmable_stimulus_sequencer_e2e` | 0.791s | 0.026s | streaming_validated |
| `vbr1_l2_programmable_stimulus_sequencer_tb` | 1.155s | 0.026s | streaming_validated |

## Functional Safety

- Default backend changed: `no`
- EVAS core semantics changed: `no`
- Rust language coverage changed: `no`
- Checker decision logic changed: `no`; row/streaming parity tests compare the same fixture both ways
- CSV schema changed: `conditional yes`; sparse trace still emits only checker contract plus optional extra columns
- Full trace fallback changed: `no`
- Claim boundary: this supports E2E runtime cleanup only, not a Spectre AX speed claim

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile runners/simulate_evas.py tests/test_vabench_function_checker_regressions.py tests/test_evas_output_cleanup.py
PYTHONPATH=runners:../EVAS python3 -m pytest tests/test_evas_output_cleanup.py -q
PYTHONPATH=runners:../EVAS python3 -m pytest tests/test_vabench_function_checker_regressions.py -q
```

Results:

```text
py_compile passed
tests/test_evas_output_cleanup.py: 11 passed
tests/test_vabench_function_checker_regressions.py: 62 passed
```

Speed smoke commands:

```bash
VAEVAS_DISABLE_VALIDATED_FAST_CHECKERS=1 PYTHONPATH=runners:../EVAS python3 runners/run_vabench_release_same_server_speed.py --speed-artifact /private/tmp/vaevas_checker_runtime_116_rows.json --suite all --limit 10 --evas-mode profile_fast_evas2 --skip-spectre --timeout-s 240 --jobs 1 --output-root results/checker-runtime-116-rowbased --report-json speed-optimization/reports/checker_runtime_116_rowbased_20260606.json --report-md speed-optimization/reports/checker_runtime_116_rowbased_20260606.md

PYTHONPATH=runners:../EVAS python3 runners/run_vabench_release_same_server_speed.py --speed-artifact /private/tmp/vaevas_checker_runtime_116_rows.json --suite all --limit 10 --evas-mode profile_fast_evas2 --skip-spectre --timeout-s 240 --jobs 1 --output-root results/checker-runtime-116-streaming --report-json speed-optimization/reports/checker_runtime_116_streaming_20260606.json --report-md speed-optimization/reports/checker_runtime_116_streaming_20260606.md
```

Results:

```text
row-based: 10/10 PASS, total wall 16.388s, checker 11.618s
generic runtime: 10/10 PASS, total wall 4.349s, checker 0.221s
```

## Learning Notes

`checker runtime` 可以理解成 checker 的公共读表和采样库。它不懂电路功能，只负责把 CSV 变成 checker 需要的少量数值序列。真正的电路判断仍在每个 checker 函数里，例如 rectifier 要看全波整流和 envelope hold，window comparator 要看窗口内外输出，stimulus sequencer 要看 ramp/chirp/burst。

为什么这会快很多：Python 创建大量 dict/list/object 的成本很高，尤其是“读完整 CSV 后再扫描很多遍”。现在 runtime 直接按列 index 读字符串并转 float，checker 可以一边读一边累计窗口统计。少建对象、少读列、少重复扫描，速度自然会下降一个数量级。

为什么仍然不是内核加速：EVAS subprocess wall 没有同等比例下降，说明模型求值、event queue、transition、record 等仿真语义没有因为这次改动变快。这次只是把仿真结束后的 checker 长尾收掉。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| streaming checker 和 row checker 判断不一致 | parity regression fail 或 full release checker mismatch | 从 `STREAMING_BEHAVIOR_CHECKS` 移除对应 task，回到 row checker |
| extra debug column 拼写错误 | sparse CSV 不包含目标列 | 检查 `VAEVAS_EXTRA_TRACE_SIGNALS*`，或临时设置 `VAEVAS_DISABLE_REQUIRED_TRACE=1` |
| 新 checker 绕开 runtime 重写 CSV parsing | code review 中出现新的 ad hoc header/index/interpolation helper | 改用 `CsvCheckerRuntime` |
| E2E speed 被误写成 core speed | EVAS subprocess wall 未同步下降 | 报告中分开写 checker wall、subprocess wall 和 E2E wall |

## Next Step

后续 checker/harness 层只做通用 runtime 复用，不再为单个 benchmark 写特殊读表逻辑。主线仍应回到 EVAS 内核：generated model evaluate、event/timer/breakpoint、transition/breakpoint ownership、record/CSV array path。
