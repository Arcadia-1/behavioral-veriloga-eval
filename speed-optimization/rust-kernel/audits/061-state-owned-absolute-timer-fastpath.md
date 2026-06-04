# 061 - State-Owned Absolute Timer Fast Path

## 结论

这一轮针对 CPPLL/ADPLL 真实热路径里的：

```verilog
@(timer(t_next_toggle)) begin
  ...
  t_next_toggle = t_next_toggle + dco_half_period;
end
```

增加了一个保守的 **state-owned absolute timer fast path**。

它不是新的 Rust production path，而是 Python generated-code hot-path 优化：当编译器能证明 timer target state 只在 `initial_step` 和自己的 timer event body 里赋值时，未到 armed target 之前不再每步重新读取 `self.state[target]` 或重新求 timer target 表达式。

## 原理

普通动态 absolute timer 每步都会执行：

```text
target = self.state["t_next_toggle"]
_check_timer_at(key, time, target)
```

但对于 state-owned timer，`timer_states[key]` 已经保存了下一次触发时间。只要：

- 当前 timer 已 armed；
- `last_fired` 还没有消费这个 armed target；
- `time < armed_target - eps`；
- target state 不可能被其它 event/普通 evaluate 语句改写；

那么重新读取 `t_next_toggle` 不会改变调度结果，直接返回 `False` 即可。

真正到首次装载、触发点、target 变化、Rust timer production、event due shadow 时，仍回到原 `_check_timer_at()`，所以 single-shot、last-fired、过期 target、event trace、breakpoint cache 语义都不复制成第二份。

## 安全判定

编译器只对以下模式启用：

- 单参数 absolute timer：`@(timer(<identifier>))`。
- `<identifier>` 是 real scalar state，不是 parameter、integer、array、表达式。
- target state 在该 timer event body 内至少赋值一次。
- target state 除 `initial_step` 和该 timer event body 外，没有被其它 top-level statement、cross/above event、其它 timer event、loop init/update 或 case/if 分支赋值。

以下模式继续走旧路径：

```verilog
@(timer(next_t + jitter))
@(timer(arr[i]))
@(timer(next_t)) ... // next_t 也被 cross/above 或普通 evaluate 语句改写
```

## 代码影响

- `EVAS/evas/simulator/backend.py`
  - 增加 `_check_state_owned_timer_at()`。
  - 编译器识别 safe `timer(state)` ownership。
  - generated code 内联“明显未到 armed target”的 skip 分支，避免每步函数调用。
  - 增加 `_state_owned_timer_targets` class metadata。
  - 增加 counters：
    - `timer_state_owned_checks`
    - `timer_state_owned_fast_skips`
    - `timer_state_owned_target_reads`
    - `timer_state_owned_fires`
    - `timer_state_owned_fallbacks`
- `EVAS/evas/simulator/engine.py`
  - 聚合上述 counters 到 simulator-level totals。
- `EVAS/tests/test_engine.py`
  - 增加 safe owner timer fast-path 测试。
  - 增加 external target write rejection 测试。

## 验证结果

### 单元/回归

| 验证 | 结果 |
|---|---:|
| `py_compile` | PASS |
| targeted timer tests | `4 passed, 226 deselected` |
| `EVAS/tests/test_engine.py` 全量 | `230 passed` |
| `EVAS/tests/test_netlist.py -k timer/cppll/transient` | `3 passed, 75 deselected` |

### in-memory microbench

构造语义等价的两个模型：

- fast path：`@(timer(next_t))`
- generic fallback：`@(timer(next_t + 0.0))`

两者最终输出一致。

| case | fast path | median wall | steps | checks | fast skips | target reads | fires |
|---|---:|---:|---:|---:|---:|---:|---:|
| `timer(next_t)` | yes | 0.020152s | 2095 | 2096 | 2075 | 21 | 20 |
| `timer(next_t + 0.0)` | no | 0.032617s | 2095 | 0 | 0 | 0 | 0 |

这个 microbench 只证明局部机制有效，不能作为 vaBench/Spectre/AX speed claim。

### top-wall 10 EVAS-only rerun

报告：`speed-optimization/reports/state_owned_timer_inline_topwall10_20260604.json`

| 指标 | 结果 |
|---|---:|
| PASS | 10/10 |
| total EVAS wall | 19.7010s |
| state-owned checks | 180956 |
| fast skips | 160486 |
| target reads | 20470 |
| fires | 20466 |
| fallbacks | 0 |

命中行主要是 CPPLL e2e/tb：

| row | wall | tran | checks | fast skips | target reads | fires |
|---|---:|---:|---:|---:|---:|---:|
| `cppll_freq_step_reacquire_smoke` | 2.5949s | 2.1448s | 90478 | 80243 | 10235 | 10233 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb` | 2.4753s | 2.0493s | 90478 | 80243 | 10235 | 10233 |

top-wall 总 wall 仍不能作为论文口径：未命中的 measurement/SAR 行有明显 run-to-run 波动，且该报告是 EVAS-only candidate evidence，不是 same-slice Spectre/AX 对照。

## 学习解释

这个优化的本质不是“让 timer 数学变快”，而是少做无用工作。

`timer(next_t)` 里，`next_t` 表示下一次事件的绝对时间。触发前，调度器已经知道这个时间，并把它存在 `timer_states[key]`。如果没有其它代码能改 `next_t`，每个小步再去读一次 `self.state["next_t"]` 只是重复确认同一个答案。

所以这一步减少的是：

- Python dict lookup；
- generated expression evaluation；
- helper function call；

但没有减少仿真步数，也没有把 event body 搬到 Rust。因此 CPPLL 这类任务仍有大量每步 event guard 检查，后续要继续做 event queue / due-dispatch 层优化。

## 风险

- 如果 target state ownership 判定漏掉外部写入，会错误跳过 target 重新求值。当前实现保守拒绝所有非 initial_step / owner timer body 写入。
- 该路径默认不在 Rust timer production 或 Rust event-due shadow 开启时跳过 `_check_timer_at()`，避免绕过 Rust parity/production 验证。
- 只覆盖 scalar real state target，不覆盖表达式、array、dynamic bus、combined event。

## 下一步

剩余瓶颈已经从“每步读取 target state”变成“每步仍要检查 event guard”。下一步更有价值的是：

1. 对 state-owned timer 生成更紧的 due-dispatch IR，让未到 armed target 的 event statement 在 scheduler 层跳过。
2. 把 state-owned timer 的 armed target 接到 typed timer arrays，减少 generated code 中的 dict lookup。
3. 最后再把 due-dispatch/event queue 搬到 Rust batch，而不是回到 per-check FFI。
