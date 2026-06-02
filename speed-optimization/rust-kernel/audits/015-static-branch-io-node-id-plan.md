# 015 - Static Branch IO Node-ID Plan

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 7d619e2`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/indexed.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

给 compiled model 增加静态 branch IO metadata，并把这些节点解析进 indexed model IO plan；这是 Rust/node-id lowering 前的“地图”，不改变当前 Python evaluate 执行代码。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| compiled model class | 只有 runtime `node_map`、`output_nodes` | 新增 `_static_voltage_read_nodes`、`_event_voltage_read_nodes`、`_static_output_write_nodes` 和 dynamic count | 默认仿真不变 |
| AST compiler | 只生成 Python evaluate 代码 | 额外扫描 AST，分类普通 read、event-body read、static write、dynamic array branch IO | 只增加 metadata |
| indexed model IO plan | 只包含 mapped ports 和 runtime output nodes | 额外包含 static/event read node ids、static output write node ids、dynamic read/write counts | indexed 诊断信息更完整 |
| runner log | `Indexed model IO plan` 只有 port/output count | 额外输出 static/event/dynamic IO count | 只影响 `EVAS_INDEXED_ARRAYS=1` 日志 |

## Principle

这一步属于 **Rust 化前的 IR/边界准备**，不是直接加速。

014 证明 model evaluate 里普通 read/write 调用密度很高。例如：

```text
adc_ramp: 22.48 voltage reads / internal step
cmp_delay: 5.00 voltage reads / internal step
```

下一步如果直接改 `_compile_expr()`，风险会很大，因为不是所有 `V(node)` 都能一样处理：

- 普通 non-event `V(vin)` 可以逐步变成 `values[node_id]`。
- event body 里的 `V(vin)` 可能需要 crossing-time 插值，不能直接读 current-step array。
- `V(bus[i])` 这种动态数组节点需要运行时拼节点名或另一个动态 lowering 机制。
- `V(out, vss) <+ expr` 里的 `out` 是写节点，`vss` 是读节点。

015 先不改执行，只把这些边界显式记录下来。

## Metadata Meaning

| Field | Meaning | Rust lowering implication |
|---|---|---|
| `_static_voltage_read_nodes` | 普通上下文中的静态 `V(node)` read | 候选 `node_id -> array read` |
| `_event_voltage_read_nodes` | event body 中的静态 `V(node)` read | 暂时保留 interpolation/event path |
| `_static_output_write_nodes` | 静态 `V(out) <+ expr` write node | 候选 `node_id -> array write` |
| `_dynamic_voltage_read_count` | `V(bus[i])` 等动态 read statement count | 需要单独动态节点策略 |
| `_dynamic_output_write_count` | `V(bus[i]) <+ expr` 等动态 write statement count | 需要单独动态节点策略 |

## Before / After Evidence

Validation commands:

```bash
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_records_static_branch_io_metadata tests/test_indexed_backend.py::test_compiled_model_counts_dynamic_branch_io_metadata tests/test_indexed_backend.py::test_indexed_model_io_plan_includes_static_branch_io_nodes tests/test_indexed_backend.py::test_indexed_model_io_plan_resolves_mapped_ports_outputs_and_parent_nodes -q
python3 -m pytest tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_indexed_arrays_build_model_io_plan_without_changing_mapped_output tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in tests/test_indexed_backend.py::test_compiled_model_records_static_branch_io_metadata tests/test_indexed_backend.py::test_indexed_model_io_plan_includes_static_branch_io_nodes -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
4 passed in 0.28s
18 passed in 0.55s
3 passed in 0.31s
440 passed in 34.40s
git diff --check: clean
```

### Example Boundary

For:

```verilog
@(cross(V(clk) - 0.5, +1)) sample = V(inp);
V(out) <+ sample;
```

The compiled metadata is:

```text
_static_voltage_read_nodes = ("clk",)
_event_voltage_read_nodes = ("inp",)
_static_output_write_nodes = ("out",)
_dynamic_voltage_read_count = 0
_dynamic_output_write_count = 0
```

The indexed plan resolves the same local nodes through `node_map`:

```text
clk -> CLK
inp -> INP
out -> OUT
```

This is exactly the boundary Rust lowering needs: ordinary cross-condition reads, event-body reads, and output writes are distinguishable before touching the evaluator.

## Functional Safety

- Default backend changed: `no`
- Generated evaluate code changed: `no`
- Node voltage values changed: `no`
- Event interpolation changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Accuracy impact: `none expected`; metadata is sidecar-only

## Learning Notes

### 为什么要先做 metadata，而不是直接 Rust 化？

直接 Rust 化相当于把执行路径替换掉。如果我们还没分清哪些 `V(node)` 是普通读、哪些是 event 插值读、哪些是动态数组读，就很容易把本来不等价的情况混在一起。

metadata 的作用像地图：

```text
先标出哪些节点能安全编号
再决定哪条路径先改成 array/Rust
最后才替换执行逻辑
```

### 为什么 event-body read 要分开？

普通读通常是：

```text
V(node, current step)
```

event body 里的读可能是：

```text
V(node, crossing time)
```

后者可能需要从前后两个 step 插值，所以不能简单替换成 `values[node_id]`。

### dynamic count 为什么只是 count，不是 node id？

`V(dout[i])` 的真实节点名取决于运行时的 `i`：

```text
dout[0], dout[1], dout[2], ...
```

这类节点不能在静态 AST 扫描时直接变成单个 node id。015 先记录它存在，后续需要动态数组节点 lowering。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| metadata 分类遗漏 AST 形态 | 新 benchmark static plan count 明显不符合 generated code | 扩展 collector 或回退 EVAS commit `7d619e2` |
| 误把 event read 当普通 read lowering | parity 回归中 event/cross 采样异常 | 保留 `_event_voltage_read_nodes` 的隔离，不进入普通 read fast path |
| dynamic array IO 被误静态化 | `V(bus[i])` 行为或节点名错误 | 只使用 dynamic count，暂不生成静态 node id |
| plan 被误当成执行优化 | speed claim 引用 015 本身 | 明确 015 是 IR/plan，不是 wall-time speedup |

## Next Step

下一篇审计文档建议：

- `016-static-branch-fast-helper-prototype.md`：基于 015 metadata，只针对非 event、非 dynamic 的普通 static branch read/write 做 opt-in helper prototype；先验证 parity，再看是否值得进入 Rust native evaluator。
