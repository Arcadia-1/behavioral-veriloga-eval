# 017 - Static Branch Node-Id Direct Array

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS e178909`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

在 016 static branch helper 的基础上，进一步把普通静态 `V(node)` read/write 绑定到 indexed voltage array 的 node id slot，跳过热路径里的字符串节点解析和 Python dict 查找。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| codegen | `EVAS_STATIC_BRANCH_FASTPATH=1` 时生成 `_get_static_branch_voltage("vin", nv)` / `_set_static_branch_output("out", value, nv)` | 同时启用 `EVAS_INDEXED_ARRAYS=1` 时生成 `_get_static_branch_voltage_by_slot(0, nv)` / `_set_static_branch_output_by_slot(0, value, nv)` | 默认 codegen 不变 |
| compiled model | helper 每次仍要从 local node name 解析 external node name | run 开始时安装 read/write node id tuple 和 write external node tuple | 只影响 opt-in fastpath |
| simulator run | static helper 和 indexed array 是两条旁路 | `_install_static_branch_indexed_io()` 把 indexed model IO plan 接入 compiled model | 默认仿真不变 |
| output write | helper 内部可能再走 string-based indexed writer | slot write 直接更新 `values[node_id]`、`node_voltages[external_node]`、`output_nodes[local_node]` | CSV/strobe/checker 不变 |
| event read | event context fallback 到 `_get_voltage()` | 保持 fallback，不安装 event-body read 到 direct current-step path | crossing-time interpolation 不变 |
| dynamic bus | 运行时拼 `V(bus[i])` 节点名 | 继续保留旧字符串路径 | dynamic bus 不变 |

## Principle

这个改动属于 **降低每步成本**。

EVAS 当前的模型执行是 Python 热循环。每个 transient step 里，模型会反复执行：

```text
V(vin) read
V(out) <+ value write
```

016 已经把通用 helper 换成专门 helper，但 helper 里面仍然要做这些事情：

- 用字符串 `"vin"` 查 local-to-external node map；
- 在 Python `dict[str, float]` 里查 `node_voltages[external_node]`；
- output write 时再维护 output dict 和 indexed mirror；
- 为 mapped port、parent node、event interpolation 等语义保留分支。

017 的思路是：这些普通静态 branch 在编译期已经知道 local node 名，在 run 开始后也已经能解析到全局 node id，所以可以把：

```text
V(vin) -> dict["vin_mapped"]
```

降成：

```text
V(vin) -> values[node_id]
```

这和未来 Rust 化的核心数据结构一致：Rust 里的 `Vec<f64>` 本质上就是用整数下标访问连续数组。017 仍然在 Python 里做，但已经把执行边界改成了 Rust 以后需要的形状。

## Before / After Evidence

Validation commands:

```bash
python3 -m pytest tests/test_engine.py::TestSimulator::test_static_branch_fastpath_matches_default_and_counts_hits tests/test_engine.py::TestSimulator::test_static_branch_fastpath_uses_indexed_node_ids_when_array_enabled tests/test_engine.py::TestCompiledModelHelpers::test_static_branch_slot_voltage_falls_back_to_event_interpolation -q
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_counts_dynamic_branch_io_metadata -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_static_branch_fastpath_when_opted_in -q
python3 -m pytest tests/test_engine.py tests/test_indexed_backend.py tests/test_netlist.py -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
3 passed in 0.46s
1 passed in 0.19s
1 passed in 0.26s
16 passed in 0.29s
5 passed in 0.77s
6 passed in 0.80s
445 passed in 29.35s
git diff --check: clean
```

Local direct-array microbenchmark:

```text
N=500000 evaluate() calls, repeats=9

slot_fallback_helper: median=0.895913s min=0.704030s max=1.235590s
slot_direct_array:    median=0.546156s min=0.517614s max=0.776752s
```

Interpretation:

- 这是本地 mapped pass-through model 的 `evaluate()` 热路径 microbenchmark，不是 release-wide speed claim。
- 相对 016 的 slot fallback helper，017 的 direct array path 局部约 `1.64x`。
- 加速来自减少 Python string key lookup、local-to-external node resolution 和多层 helper 分支。
- 这不代表完整 EVAS 一定整体 `1.64x`，因为完整仿真还包括 source update、event/timer scan、CSV 输出、checker 和进程外层开销。

## Functional Safety

- Default backend changed: `no`
- Default generated code changed: `no`
- Opt-in generated code changed: `yes`
- Requires indexed arrays opt-in: `yes`
- Event interpolation changed: `no`
- Dynamic bus changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected`; tests compare default vs opt-in waveform equality

## Learning Notes

### node id 是什么？

节点名是给人看的字符串，比如：

```text
vin
vout
DOUT<3>
```

node id 是仿真器内部给节点分配的整数编号，比如：

```text
vin  -> 0
vout -> 1
```

有了 node id，电压表就可以从：

```python
node_voltages["vin"]
```

变成：

```python
values[0]
```

后者少了字符串哈希、字典查找、mapped port 解析和很多 Python 对象处理。Rust/C 这类语言也最擅长连续数组下标访问，所以这个改动是 Rust 化前置 IR 的一部分。

### slot 和 node id 有什么区别？

node id 是全局电压数组里的下标。slot 是某个模型自己的小表下标。

例如一个模型只读 `vin`、只写 `vout`：

```text
model read slot 0  -> global node id 12
model write slot 0 -> global node id 13
```

生成代码里写 slot：

```python
self._get_static_branch_voltage_by_slot(0, nv)
```

运行时 helper 再通过模型自己的 tuple 找到全局 node id：

```python
node_id = self._static_branch_read_node_ids[0]
return values[node_id]
```

这样做的好处是：生成代码不需要知道全局 node id 何时分配，只需要稳定引用模型自己的 slot。

### 为什么 event body 还不能这样读？

普通 read 的含义是“当前 step 的电压”。

event body 里的 read 可能是“crossing time 的电压”。crossing time 可能在上一点和当前点之间，需要插值：

```text
previous step ---- crossing time ---- current step
```

如果 event body 直接读 `values[node_id]`，它读到的是 current step，不一定是 crossing time。因此 017 继续让 event context fallback 到 `_get_voltage()`，保留原来的 crossing-time interpolation。

### 为什么 dynamic bus 还不能这样读写？

静态 branch 是：

```verilog
V(out) <+ value;
```

dynamic bus 是：

```verilog
V(dout[i]) <+ value;
```

这里的 `i` 是运行时变量。编译期不能只绑定一个固定 node id。后续 019 要单独把 bus base、方向和 offset 建成 IR，再把它降到：

```text
node_id = bus_base + offset(i)
```

这比单个静态节点更容易出错，所以不能混在 017 里一起改。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| mapped/parent node id 绑定错误 | default vs opt-in waveform 不一致；`indexed_post_model_sync_repairs` 非 0 | 回退 EVAS commit `e178909` 或关闭 `EVAS_STATIC_BRANCH_FASTPATH` / `EVAS_INDEXED_ARRAYS` |
| event read 被误接入 direct array | cross/sample-hold 测试采样时间偏移 | event context fallback 保持 `_get_voltage()` |
| dynamic bus 被误静态化 | `V(bus[i])` 代码中出现 `_set_static_branch_output_by_slot` | dynamic branch codegen test 守住旧路径 |
| microbenchmark 被误当论文速度结论 | 报告引用 `1.64x` 作为 EVAS/AX 整体速度 | 明确需要 release-wide same-slice EVAS/Spectre/AX timing artifact |

## Next Step

下一篇建议做：

- `018-event-interpolation-ir-boundary.md`

017 已经把普通 current-step static branch read/write 降到 node id array。018 需要把 event-body read 和 crossing interpolation 的边界显式化，防止后续 Rust evaluate 或更激进 codegen 把 event read 错误当成普通 current-step read。
