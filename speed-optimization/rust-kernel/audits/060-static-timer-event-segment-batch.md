# 060 - Static Timer/Event Segment Batch

## 结论

这一轮把 timer/event 的下一步从“逐个 timer FFI”改成了更合理的 **compiler-level segment batch**。当前实现先落在 Python batch helper 上，不直接进入 Rust，原因是我们要先证明：

- 编译器能安全识别可 batch 的 timer 段。
- due mask 计算可以提前，但 event body 仍按原源码顺序执行。
- 动态 timer target 不会被错误提前计算。

默认路径现在会把连续的、timer 参数只依赖常量/parameter 的 timer event 合成一次：

```text
_timer_batch_hits = self._check_timer_event_batch((spec0, spec1, ...), time)
if _timer_batch_hits[0]:
    原 event body 0
if _timer_batch_hits[1]:
    原 event body 1
...
```

这不是最终 Rust 化，但它建立了后续 Rust typed-array timer batch 的正确 codegen 边界。

## 为什么不能更激进

不能把所有 timer 都提前 batch。例子：

```verilog
@(timer(next_t)) begin
  q = 1 - q;
  next_t = next_t + 1n;
end
```

这里 `next_t` 是 state，event body 会更新它。如果把后续 timer target 过早计算，可能改变事件调度语义。因此 060 只 batch：

- 连续出现的 `@(timer(...))` event statements。
- timer 参数表达式只包含 number literal、parameter、简单算术、常见数学函数。
- event body 仍然逐个按源码顺序执行。

`timer(next_t)` 这类 state-dependent timer 明确保留旧路径。

## 代码影响

- `EVAS/evas/simulator/backend.py`
  - 增加 `_check_timer_event_batch()`，一次计算同一 segment 的 due mask。
  - `Block` 编译器识别连续 batchable timer event segment。
  - `evaluate()` 顶层改为把整个 analog block 当作 `Block` 编译，让 top-level 相邻 timer 可被 grouping。
  - 新增 counters：
    - `timer_batch_due_calls`
    - `timer_batch_due_events`
    - `timer_batch_due_fires`
    - `timer_batch_due_fallbacks`
- `EVAS/evas/simulator/engine.py`
  - 聚合上述 counters 到 simulator-level totals。
- `EVAS/tests/test_engine.py`
  - 增强 timer scanner 测试，确认 static timer segment 真的生成 `_check_timer_event_batch()`。
  - 增加动态 timer guard：`timer(next_t)` 不进入 batch。

## 验证结果

### 单元/回归

| 验证 | 结果 |
|---|---:|
| `py_compile` | PASS |
| timer targeted tests | `24 passed, 204 deselected` |
| `EVAS/tests/test_engine.py` 全量 | `228 passed` |
| `EVAS/tests/test_netlist.py -k timer/cppll/transient` | `3 passed, 75 deselected` |

### top-wall 10

报告：`speed-optimization/reports/timer_batch_topwall10_20260604.json`

| mode | PASS | total wall | total tran | batch calls | batch events |
|---|---:|---:|---:|---:|---:|
| fast baseline after 060 | 10/10 | 19.1162s | 11.1339s | 0 | 0 |

当前 top-wall 10 没有触发 static timer segment batch。这说明 060 对当前 top-wall 速度没有直接贡献，但也没有造成功能回归。

### in-memory microbench

构造 16 个连续 static absolute timers，与 16 个 dynamic-state absolute timers 对比。两者最终输出都为 `16.0`。

| case | batch? | median wall | steps | batch calls | batch events | fires |
|---|---:|---:|---:|---:|---:|---:|
| static batchable 16 timers | yes | 0.040328s | 2080 | 2081 | 33296 | 16 |
| dynamic no-batch 16 timers | no | 0.046606s | 2080 | 0 | 0 | 0 |

这个 microbench 只能说明局部 batch 方向有效，不能作为 vaBench/Spectre/AX paper-facing speed claim。

## 学习解释

Rust 化或 batch 化真正减少的是“重复调度/解释开销”，不是改变 timer 数学。原来每个 timer event 每步都单独做：

```text
函数调用 -> kind lookup -> state lookup -> due 判断 -> event body
```

batch 后，同一段 timer event 变成：

```text
一次 batch 调用 -> loop 内局部变量查表 -> due mask -> 原顺序 event body
```

这一步还是 Python loop，但已经把 codegen 结构改成“先 due mask，后 body 顺序执行”。后续把 `_check_timer_event_batch()` 内部换成 Rust array loop 时，不需要再重做 event ordering 设计。

## 风险

- 060 不 batch dynamic target，因此 CPPLL 这种 `timer(next_t)` 热路径仍然不会直接加速。
- 如果某个 parameter 在非标准路径里被当作 runtime mutable state 改写，batch 识别可能过于乐观；当前 EVAS 参数语义是 instance parameter，不是 event body state。
- 当前 batch 只覆盖连续 timer event。夹在普通 assignment / contribution / cross 之间的 timer 不会跨 statement 合并。

## 下一步

下一步要真正碰 CPPLL 这类 hot path，应做 **state-owned absolute timer fast path**：

1. 编译期识别 `timer(next_t)`，其中 `next_t` 只在 initial_step 和该 timer event body 内更新。
2. 在 `time < armed_target` 且 target owner 未被其它事件改写时，跳过每步 target expression 重新求值。
3. 到 due time 后仍按原 event body 执行，并重新 arm `next_t`。

这比 per-check Rust FFI 更接近 CPPLL 的真实瓶颈。
