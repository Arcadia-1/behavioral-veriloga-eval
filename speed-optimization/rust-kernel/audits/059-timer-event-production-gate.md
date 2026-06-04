# 059 - Timer/Event Production Gate

## 结论

这一轮验证了 B11 timer/event 路径的一个关键边界：**不能把单个 `timer()` check 逐次搬到 Rust 调用**。在 CPPLL 这类真实 hot case 里，timer 很热，但每个 model 基本是单 timer state。逐次 Rust FFI 会把原来的 Python O(1) dict bookkeeping 变成：

```text
每次 timer check = Python 数组打包 + ctypes FFI + Rust length-1 loop + 结果拷回 Python
```

所以算法复杂度没有下降，常数项反而变大。

本轮最终保留的是：

- `evas_rust_timer_event=true` 独立开关，能加载 Rust timer backend，但不强制开启全局 indexed arrays。
- Rust timer scanner / due production 增加小集合 gate：同一 model 少于 2 个 timer state 时不走 Rust，避免 length-1 FFI 负收益。
- 默认 Python timer hot path 去掉未启用 shadow 时的多余 before-state 采样，并避免重复写 `timer_kinds`、重复查 `timer_states`。

## 改造原理

`timer(t)` 是绝对时间事件，`timer(start, period)` 是周期事件。EVAS 当前仍由 Python 维护：

- `timer_states[key]`: 下一次触发时间。
- `timer_last_fired[key]`: absolute timer 防止同一 target 重复触发。
- `timer_kinds[key]`: absolute / periodic 类型，用于过期处理和 breakpoint 扫描。

Rust primitive 已能正确计算 periodic/absolute due/reschedule，但只有在“多个 timer 一起批处理”时才可能赢。对单 timer 高频调用，Rust 的 `O(1)` loop 没有比 Python 少做事情，反而多了一次跨语言边界。

因此本轮选择：

```text
单 timer 高频路径: 优先瘦 Python bookkeeping
多 timer array 路径: 允许 Rust scanner / due primitive
真正加速目标: 后续 compiler-level timer batch，而不是逐个 timer FFI
```

## 实验结果

### 失败尝试：逐次 Rust timer check

报告：`speed-optimization/reports/rust_timer_event_cppll_20260604.json`

| case | baseline wall | per-check Rust wall | 结果 | 关键 counters |
|---|---:|---:|---|---|
| CPPLL e2e | 2.8293s | 3.6122s | 变慢 | `rust_timer_event_production_absolute_calls_total=90478` |
| CPPLL tb | 2.6403s | 3.8000s | 变慢 | `rust_timer_breakpoint_scans_total=10235` |

两个 case 都 PASS，fallback 为 0，说明语义正确；但速度变慢，说明问题在调用粒度。

### 最终 gate 后：top-wall 10

报告：`speed-optimization/reports/rust_timer_event_topwall10_20260604_r2.json`

| mode | PASS | total wall | total tran | Rust timer scans | Rust absolute calls | 结论 |
|---|---:|---:|---:|---:|---:|---|
| fast baseline | 10/10 | 20.2422s | 10.5685s | 0 | 0 | 当前参考 |
| fast + rust_timer_event | 10/10 | 20.2278s | 10.6866s | 0 | 0 | gate 生效，基本持平 |

真实 top-wall 10 没有触发 Rust timer path，因为这些 case 的 timer 结构不是“同一 model 多 timer array scan”，而是 CPPLL 这种“单 timer 高频 absolute check”。这说明下一步不应该继续做 length-1 Rust 化。

## 正确性验证

- `python3 -m py_compile` 覆盖：
  - `EVAS/evas/simulator/backend.py`
  - `EVAS/evas/simulator/engine.py`
  - `EVAS/evas/netlist/runner.py`
  - `behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py`
  - `EVAS/tests/test_engine.py`
- targeted timer tests：`24 passed, 204 deselected`
- CPPLL smoke：2 forms × 2 modes 全部 PASS
- top-wall 10：2 modes × 10 rows 全部 PASS

Rust core 本轮没有改动，所以未重跑完整 `cargo test`。

## 代码影响

- `EVAS/evas/simulator/backend.py`
  - 增加 Rust timer production backend hook。
  - 增加 `rust_timer_event` counters。
  - 增加小 timer 集合 gate，避免 single-timer length-1 FFI。
  - 优化 Python timer fallback 的 dict bookkeeping。
- `EVAS/evas/simulator/engine.py`
  - 增加 `rust_timer_event` run flag、backend install、perf 汇总和 cleanup。
- `EVAS/evas/netlist/runner.py`
  - 增加 `evas_rust_timer_event` / `EVAS_RUST_TIMER_EVENT`。
- `behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py`
  - 增加 `profile_fast_rust_timer_event` mode。
  - 扩展 timer/rust timer counter 解析。
- `EVAS/tests/test_engine.py`
  - 增加 default vs Rust timer-event parity 测试。

## 风险和解释口径

`rust_timer_event_enabled=1` 只表示该开关和 backend 可用；是否真正执行 Rust timer path 要看：

- `rust_timer_breakpoint_scans_total`
- `rust_timer_event_production_absolute_calls_total`
- `rust_timer_event_production_periodic_calls_total`

如果这些 counter 为 0，说明 gate 判断该 case 不适合逐次 Rust timer path。这不是失败，而是防止负收益的保护。

## 下一步

timer/event 的真正 Rust 化应该改成 compiler/engine batch：

1. 编译期收集同一 model 的 timer event keys、target/period 表达式和 event body 顺序。
2. 每个 `post_update_events()` phase 用一次 Rust batch 计算所有 timer due flags。
3. Python 只按 due mask 执行必须保留顺序的 event body，或者继续把简单 event body lowering 到 Rust batch。
4. scheduler breakpoint scan 也应该消费同一份 typed timer arrays，而不是在每次 `_next_timer_breakpoint()` 里临时打包。

这条路线才有机会把成本从：

```text
N_timer_checks 次 Python/Rust 边界
```

降成：

```text
N_steps 次 model-level timer batch
```

当前 top-wall 证据显示：在真实样本上，优先级应该是 **single-timer Python hot path + compiler-level event/timer batch**，不是继续扩 per-check Rust primitive。
