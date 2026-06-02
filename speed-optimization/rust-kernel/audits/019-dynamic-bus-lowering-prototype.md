# 019 - Dynamic Bus Lowering Prototype

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 75e10b5`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/indexed.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

为 `V(bus[i])` / `V(bus[i][j])` 建立 dynamic branch access IR，记录 role、base node、维度和上下文；当前不替换 runtime f-string codegen。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| compiled model metadata | 只记录 dynamic voltage read/write count | 新增 `_dynamic_branch_accesses`，每项为 `(role, base_node, dimensions, context)` | 默认仿真不变 |
| indexed model IO plan | 只有 dynamic read/write count | 新增 `DynamicBranchAccessIO` 和 `dynamic_branch_access_count` | 只影响 opt-in IR/stats |
| simulator stats | `Indexed model IO plan` 不显示 dynamic access descriptor 数量 | 新增 `dynamic_branch_access_count` | 只影响日志诊断 |
| dynamic bus write/read codegen | `V(dout[i])` 生成 f-string 节点名 | 完全不改 | runtime behavior 不变 |
| static fastpath | dynamic bus 不进入 static branch direct-array path | 完全不改 | bus 语义不变 |

## Principle

这个改动属于 **Rust 化前置 IR**，不是直接速度优化。

当前 dynamic bus 路径类似：

```python
self._set_output(f"dout[{int(i)}]", value, nv)
self._get_voltage(f"dbus[{int(ch)}][{int(j)}]", nv)
```

这会在热循环里持续做：

- Python f-string 格式化；
- `int()` 转换；
- 字符串哈希；
- dict lookup；
- local-to-external node resolution。

未来更快的形式应该是：

```text
node_id = bus_base_id + offset(i)
values[node_id] = value
```

或者 2D：

```text
node_id = bus_base_id + row_stride * i + j
```

但这一步不能直接改。原因是 EVAS 现在要兼容：

- 1D bus：`V(dout[i])`；
- 2D bus：`V(dbus[ch][j])`；
- differential branch：`V(dout[i], VSS)`；
- event body / trigger context；
- loop-local index 和普通 state index；
- parser 目前对 2D declaration range 的记录还不完整。

所以 019 先把 dynamic branch access 描述出来：

```text
("output_write", "dout", 1, "ordinary")
("voltage_read", "dbus", 2, "ordinary")
("voltage_read", "bus", 1, "event_trigger")
("voltage_read", "bus", 1, "event_body")
```

这让后续 020/021 或单独 bus lowering pass 可以在不重新遍历 AST 的情况下知道“哪些 model 需要 bus lowering、是哪类 bus、在哪种上下文”。

## Before / After Evidence

Validation commands:

```bash
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_counts_dynamic_branch_io_metadata tests/test_indexed_backend.py::test_compiled_model_records_dynamic_branch_access_ir_for_2d_reads tests/test_indexed_backend.py::test_indexed_model_io_plan_exposes_dynamic_branch_accesses -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in -q
python3 -m pytest tests/test_indexed_backend.py tests/test_netlist.py tests/test_engine.py::Test2DNodeArray -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
3 passed in 0.19s
1 passed in 0.41s
92 passed in 1.77s
447 passed in 29.98s
git diff --check: clean
```

Observed metadata:

```text
V(dout[i], VSS) <+ i
_dynamic_branch_accesses = (("output_write", "dout", 1, "ordinary"),)

sample = V(dbus[1][0], VSS)
_dynamic_branch_accesses = (("voltage_read", "dbus", 2, "ordinary"),)
```

Interpretation:

- `role` tells future lowering whether the access is read or write.
- `base_node` tells future lowering which bus family is involved.
- `dimensions` separates 1D and 2D lowering.
- `context` preserves 018's event boundary, so event-body dynamic bus reads are not accidentally lowered as current-step reads.
- No runtime speed number is reported because current f-string execution path is intentionally unchanged.

## Functional Safety

- Default backend changed: `no`
- Default generated runtime code changed: `no`
- Runtime dynamic bus behavior changed: `no`
- Event interpolation changed: `no`
- Static fastpath behavior changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected`; full EVAS test suite passed

## Learning Notes

### dynamic bus 为什么比普通 node 难？

普通 node 是：

```verilog
V(out) <+ x;
```

编译期就知道节点是 `out`。

dynamic bus 是：

```verilog
V(dout[i]) <+ x;
```

节点要等运行时 `i` 的值确定后才知道。字符串形式是：

```text
dout[0]
dout[1]
dout[2]
```

要改成数组下标，就必须知道 bus 的 base id、方向、长度，以及 `i` 到 node id 的映射。

### 为什么 019 不直接加速？

如果直接把 `dout[i]` 改成 `values[base + i]`，可能会踩这些坑：

- Verilog-A bus 可以写 `[3:0]` 或 `[0:3]`，方向不同；
- 2D bus 的 inner/outer 维度要定义 stride；
- 有些 index 是 loop-local，有些 index 是 `self.state["i"]`；
- event body 中的 dynamic bus read 可能需要 crossing-time interpolation；
- netlist 中 bus node 名和 module-local base name 可能还有 mapping。

因此 019 先把访问描述抽出来，不改变行为。

### 这和 Rust 化有什么关系？

Rust 想要快，通常不应该在热循环里拼字符串。Rust 侧更自然的输入是：

```text
DynamicAccess {
  role: output_write,
  base_node: dout,
  dimensions: 1,
  context: ordinary
}
```

再配合 bus layout：

```text
dout[0] -> node id 10
dout[1] -> node id 11
dout[2] -> node id 12
```

这样 Rust evaluate 时就可以直接算 node id，而不是生成字符串再查字典。

## Known Issue Found

019 测试时发现一个已有 codegen 边界：`V(dbus[ch][j])` 如果 `ch/j` 是普通 state variable，当前 f-string codegen 会生成嵌套单引号，导致 Python compile 失败：

```text
f'dbus[{int(self.state['ch'])}]'
```

这不是 019 新增的问题，因为 019 没有改 dynamic bus runtime codegen。当前已存在的 2D runtime tests 用 loop-local `genvar` 或常量 index 可以通过。这个问题应在后续 dynamic bus runtime lowering 或 codegen cleanup 中单独修，不适合混在 metadata IR commit 里。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| dynamic descriptor 记录错误 | `dynamic_branch_accesses` tests 失败 | 回退 EVAS commit `75e10b5` |
| 把 IR 当成 runtime speedup | 报告中出现 019 wall-time speed claim | 明确 019 不改 f-string path |
| 未来 lowering 忽略 bus direction | bus 输出位顺序反转 | 需要新增 bus layout/range tests 后再 lowering |
| 未来 lowering 忽略 event context | event bus read 采样时刻错误 | 018/019 context metadata 必须进入 Rust ABI |

## Next Step

下一篇建议做：

- `020-indexed-model-state-arrays.md`

019 把 node-side dynamic bus access 描述出来。020 应该开始处理 model 内部 state：`self.state["x"]`、`self.arrays["a"][i]` 等 Python dict/object 访问，为 Rust ABI 准备 state id 和 array state layout。
