# 008 - Indexed Non-Event Voltage Read

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS 63c1eb2`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

在 `EVAS_INDEXED_ARRAYS=1` 的 opt-in 路径下，让 `_get_voltage()` 的 non-event 普通读优先从 indexed array mirror 返回；event/cross/above 的 crossing-time 插值路径保持原样。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `CompiledModel._get_voltage()` | 普通读和事件读都先走 dict/output_nodes 语义值 | 普通读可通过 `_indexed_voltage_reader` 从 array mirror 返回 | 默认无变化 |
| event-context reads | `_get_voltage()` 在 event body 中按 crossing time 插值 | 仍然跳过 indexed reader，继续插值 | 事件语义不变 |
| indexed stats | 007 只记录 input-read probe | 新增 `Indexed voltage array reads`，记录 reads/read_nodes/fallbacks | opt-in 日志更清楚 |
| fallback | array 只做旁路 probe | array 缺节点时回退到原 dict/output path | 防止动态节点漏编号直接改变行为 |
| tests | 验证 probe 能看到 resolved node | 新增普通读接管、mapped 读接管、event 读跳过 reader | 默认无变化 |

## Principle

这一步属于 **降低每步成本**。

普通模型输入读的数学含义是：

```text
V(node, current step) = voltage_at(t_k)
```

如果节点已经被映射成整数 id，那么读值可以从：

```text
node_voltages["vin"]
```

变成：

```text
values[node_id("vin")]
```

这就是 Rust 化前的数据结构准备：Python dict 读需要字符串 hash、key 比较、对象装箱；array 读只需要整数下标。008 是第一次让 model input read 真正消费 array mirror，而不是只旁路比较。

但是 event body 里的 `V(node)` 不是当前 step 的普通值。它代表 crossing time 上的插值：

```text
V(node, t_event) = V(t_{k-1}) + frac * (V(t_k) - V(t_{k-1}))
```

其中：

```text
frac = (t_event - t_{k-1}) / (t_k - t_{k-1})
```

这个值通常不等于 `values[node_id]` 里的当前 step 值。所以 008 只迁移 non-event 普通读；event-context reads 继续走原来的 dict/interpolation path。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default backend | `python_dict` | `python_dict` | 默认仿真没有切换 |
| non-event `_get_voltage()` | dict/output-backed | opt-in array-backed with fallback | indexed path 开始真实消费 array |
| event-context `_get_voltage()` | crossing-time interpolation | unchanged | cross/above 语义不变 |
| read telemetry | probe-only | array read stats + probe stats | 能区分“真实 array 读”和“诊断 probe” |
| focused tests | 007 focused coverage | `5 passed` | 新增 reader/event guard coverage |
| full EVAS tests | `425 passed` at 007 | `428 passed` | 新增 3 个 helper 测试，无回归 |

Important interpretation:

- 008 仍不是 paper-facing speed claim。
- 它只证明 opt-in indexed path 已经能把普通模型输入读改为 array-backed read。
- 真实速度收益还需要 profile，因为 Python callback 本身仍有开销；最终目标是 Rust/native model-evaluate hot loop。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected for default backend`; opt-in indexed path 的 event interpolation 保持原样

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestCompiledModelHelpers::test_get_voltage_non_event_prefers_indexed_reader tests/test_engine.py::TestCompiledModelHelpers::test_get_voltage_mapped_non_event_prefers_indexed_reader tests/test_engine.py::TestCompiledModelHelpers::test_get_voltage_event_context_ignores_indexed_reader tests/test_engine.py::TestSimulator::test_indexed_arrays_build_model_io_plan_without_changing_mapped_output tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in -q
python3 -m pytest tests -q
git diff --cached --check
```

Results:

```text
5 passed in 0.48s
428 passed in 31.49s
git diff --cached --check: clean
```

## Learning Notes

### 什么是普通读？

普通读就是模型在当前仿真时间点读取某个节点：

```verilog
V(vout) <+ V(vin);
```

在非事件上下文里，`V(vin)` 可以理解为“当前 step 的 vin 电压”。这类读非常适合变成：

```text
node id -> array[index]
```

### 为什么 event 读不能一起改？

event body 里经常出现：

```verilog
@(cross(V(vin) - vth, +1)) begin
    sample = V(vin);
end
```

这里的 `V(vin)` 不是简单的当前 step 电压，而是“触发 crossing 的那个时间点”的电压。EVAS 当前会根据前后两个 step 做插值，并加上 very small nudge 来稳定边界比较。

如果直接读 array 当前值，会把：

```text
V(vin, t_event)
```

错误替换成：

```text
V(vin, t_k)
```

这会改变 event ordering、cross/above 判断和采样值。因此 event 读要单独设计，不能混在 008 里。

### 为什么这还是 Rust 化前置工作？

008 仍在 Python 里跑，reader callback 本身也有 Python 函数调用成本。因此它不是最终性能形态。

它真正的价值是把语义边界拆出来：

```text
普通读：可以 indexed
事件读：暂时不可 indexed，必须保留 interpolation
```

等模型 evaluate 热路径迁到 Rust 后，普通读就可以直接变成 `Vec<f64>` 下标访问，不再经过 Python dict 和 Python callback。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| array mirror 缺模型输入节点 | `indexed_voltage_read_fallbacks > 0` | 扩展 model IO plan 或回退 EVAS commit `63c1eb2` |
| array mirror 与 dict 不一致 | `_indexed_array_stats["max_abs_diff"] > 0` 或 sync repair 增加 | 回退到 007 probe-only path |
| event 读误走 array | event-context guard 测试失败，cross/above 回归失败 | 保持 `_read_indexed_voltage()` 对 `_event_context_active` 的硬跳过 |
| Python callback 没有带来速度提升 | profile 中 model evaluate wall 未降 | 后续迁移到 Rust/native hot loop，而不是在 Python callback 上继续堆优化 |

## Next Step

下一篇审计文档建议：

- `009-indexed-model-evaluate-profile.md`：在 opt-in indexed path 下量化 model evaluate 中 `_get_voltage`、`_set_output`、event/timer/bound_step 的耗时占比，判断下一步应迁移普通 continuous evaluate、timer/breakpoint scan，还是先做 event queue。
