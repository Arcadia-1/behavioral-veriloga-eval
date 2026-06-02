# 018 - Event Interpolation IR Boundary

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 6c67aaf`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/indexed.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

把 event trigger expression 中的 voltage read 和 event body 中的 voltage read 显式拆成 indexed IO metadata，为后续 Rust/native event lowering 建立精度边界，但不改变当前 event 执行语义。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| compiled model metadata | 只有 `_static_voltage_read_nodes` 和 `_event_voltage_read_nodes`；`cross(V(clk))` 的 trigger read 只混在 static read 里 | 新增 `_event_trigger_voltage_read_nodes` 和 `_event_body_voltage_read_nodes`；旧 `_event_voltage_read_nodes` 保持为 event body read alias | 默认仿真不变 |
| indexed model IO plan | 只暴露 static read、event read、static write | 新增 `event_trigger_voltage_node_ids`、`event_body_voltage_read_node_ids` 和对应 count | 只影响 opt-in stats/IR |
| simulator stats | `Indexed model IO plan` 只打印 `event_voltage_read_count` | 同时打印 `event_trigger_voltage_count` 和 `event_body_voltage_read_count` | 只影响日志诊断 |
| runtime event handling | `_check_cross()` 设置 event time，event body `_get_voltage()` 在 event context 插值 | 完全不改 | crossing-time 语义不变 |
| static fastpath | event body read fallback 到 `_get_voltage()` | 完全不改 | 017 direct array 不碰 event read |

## Principle

这个改动本身不是直接速度优化，而是 **降低未来优化的精度风险**。

普通 static read 是：

```text
V(node) at current simulation step
```

017 可以把它降成：

```text
values[node_id]
```

但 event 相关 read 有两类：

```text
trigger read:    cross(V(clk) - 0.5)
event body read: sample = V(inp)
```

trigger read 用来判断是否发生 crossing；event body read 可能要在 crossing time 采样，而 crossing time 可能落在上一点和当前点之间：

```text
prev step ---- crossing time ---- current step
```

所以 event body 里的 `V(inp)` 不能简单读当前 `values[node_id]`。它需要根据 `_event_time` 在 previous/current node voltages 之间插值。

018 的作用是把这个边界变成可测试的 IR：

- `event_trigger_voltage_node_ids`：哪些节点参与 cross/above 触发检测；
- `event_body_voltage_read_node_ids`：哪些节点在 event body 中被采样；
- `event_voltage_read_node_ids`：保留旧字段，等价于 event body read，避免破坏现有测试/调用者。

这一步让后续 Rust 化可以先看 metadata，再决定哪些 read 可以 current-step direct array，哪些必须走 event-time interpolation。

## Before / After Evidence

Validation commands:

```bash
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_records_static_branch_io_metadata tests/test_indexed_backend.py::test_indexed_model_io_plan_includes_static_branch_io_nodes -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in -q
python3 -m pytest tests/test_engine.py tests/test_indexed_backend.py tests/test_netlist.py -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
2 passed in 0.34s
1 passed in 0.51s
276 passed in 1.57s
445 passed in 33.71s
git diff --check: clean
```

Observed metadata on sample-hold fixture:

```text
_static_voltage_read_nodes        = ("clk",)
_event_trigger_voltage_read_nodes = ("clk",)
_event_voltage_read_nodes         = ("inp",)
_event_body_voltage_read_nodes    = ("inp",)
_static_output_write_nodes        = ("out",)
```

Interpretation:

- `clk` is still a static read because trigger expression evaluation happens in the ordinary evaluate pass.
- `clk` is also explicitly marked as event trigger read, so native event lowering can see it separately.
- `inp` is event body read, so it must remain protected from current-step direct-array lowering unless event interpolation is implemented.
- No runtime waveform, CSV, strobe, checker, or event ordering behavior changed.

## Functional Safety

- Default backend changed: `no`
- Default generated runtime code changed: `no`
- Runtime event ordering changed: `no`
- Event interpolation changed: `no`
- Static fastpath behavior changed: `no`
- Dynamic bus changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected`; full EVAS test suite passed

## Learning Notes

### 为什么 event body 不能直接快读？

假设 clock 在 `0ns` 是 `0V`，在 `10ns` 是 `1V`，crossing threshold 是 `0.5V`。真实 crossing time 是 `5ns`。

如果 event body 写：

```verilog
@(cross(V(clk) - 0.5, +1)) sample = V(inp);
```

那么 `sample` 应该拿 `inp` 在 `5ns` 的值，而不是 `10ns` 的值。普通 `values[node_id]` 通常代表当前 step，也就是 `10ns`。这就是 event read 精度风险的来源。

### trigger read 和 body read 有什么不同？

trigger read 负责回答：

```text
这一步有没有 crossing？
```

body read 负责回答：

```text
crossing 发生时，被采样信号的值是多少？
```

前者服务于事件检测，后者服务于事件体赋值。未来 Rust 化可以把两者都变成 node id，但执行逻辑不能一样。

### 018 为什么没有加速数字？

因为 018 没有减少每步操作，也没有减少步数。它是安全边界建设：先把危险路径命名、编号、测试，后续才可以把 Rust event evaluator 写得更大胆。

这类前置改动对长期加速很重要。没有这个边界，后续如果一口气把所有 `V(node)` 都替换成 `values[node_id]`，event sampling 会很容易出现“速度变快但采样时刻错了”的隐蔽精度退化。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| trigger/body metadata 计数错误 | indexed model IO plan tests 失败，或日志 count 异常 | 回退 EVAS commit `6c67aaf` |
| 误以为 event read 已可 direct array | cross/sample-hold parity 退化 | 保留 event context fallback；后续 Rust lowering 必须读 `event_body_voltage_read_node_ids` |
| 新字段破坏旧调用者 | `event_voltage_read_count` 相关测试失败 | 旧 `event_voltage_read_node_ids` 继续作为 body read alias |
| 把 018 当速度优化结论 | 报告中出现 018 speedup claim | 明确 018 是 IR/guardrail，不是 wall-time claim |

## Next Step

下一篇建议做：

- `019-dynamic-bus-lowering-prototype.md`

018 把 event 相关 read 从 static fastpath 中隔离出来。019 可以开始处理另一类不能简单静态化的路径：`V(bus[i])` dynamic bus。目标是先建立 bus base/range/offset IR，避免运行时持续拼接字符串节点名。
