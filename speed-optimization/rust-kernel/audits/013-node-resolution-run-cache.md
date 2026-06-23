# 013 - Node Resolution Run Cache

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS b56454c`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_engine.py`

## One-Line Summary

在 `Simulator.run()` 周期内缓存本地端口名到外部节点名的解析结果，减少 `_get_voltage()`、`_set_output()` 和 event helper 中重复的 Python dict/string 映射开销。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `CompiledModel._get_voltage()` | 每次 mapped read 都执行 `node_map.get()` 和 `@parent:` 字符串判断 | mapped read 通过 `_resolve_external_node()` 读取 run-local cache | 电压值来源不变 |
| `CompiledModel._set_output()` | 每次输出写回都重新解析 output node | 输出写回复用同一个 resolved external node cache | 输出节点和值不变 |
| cross event helper | event body 内部 helper 重复解析插值节点 | event helper 复用 `_resolve_external_node()` | crossing-time 插值逻辑不变 |
| `Simulator.run()` | 不管理节点解析缓存 | run 开始启用并清空缓存，run 结束统计后关闭并清空 | 仿真结束后不保留缓存状态 |
| perf stats | 无 node resolution cache 统计 | 新增 `node_resolution_cache_entries/models` | 只用于诊断 |

## Principle

这一步属于 **降低每步成本**。

EVAS 模型里每次：

```verilog
V(vin)
V(vout) <+ expr
```

在 Python backend 中都要先把模型内部名字映射成仿真全局节点名：

```text
local node name -> node_map lookup -> external node name
```

层次模型还会出现：

```text
child node -> "@parent:inp" -> parent.node_map["inp"] -> external node
```

这些映射在一次仿真 run 内通常是固定的。旧路径每次读写都重新做字符串 hash、dict lookup、`@parent:` 前缀判断和 parent dict lookup。013 把这个解析结果缓存成：

```text
"inp" -> "VIN"
"out" -> "VOUT"
```

注意：缓存的是 **节点名解析结果**，不是电压值。电压值仍然从原来的 `node_voltages` dict 或 opt-in indexed array 读取。因此这次改动不会改变数值精度、事件插值、动态 source 或 output 写回语义。

## Before / After Evidence

### Microbenchmark

这是 helper hot path 微基准，不是 vaBench/Spectre paper-facing 速度表。

Command:

```bash
python3 -c '<local microbenchmark: 400000 calls, 7 repeats, median wall>'
```

Result:

```text
N=400000 repeats=7 median_seconds
mapped_get  uncached=0.237191 cached=0.178281 speedup=1.330x
mapped_set  uncached=0.241872 cached=0.169072 speedup=1.431x
parent_get  uncached=0.339078 cached=0.184070 speedup=1.842x
parent_set  uncached=0.317613 cached=0.218765 speedup=1.452x
```

Interpretation:

- 普通 mapped read/write 的节点解析热路径约快 `1.33x` 到 `1.43x`。
- `@parent:` 层级映射收益更明显，尤其 parent read 约 `1.84x`。
- 真实仿真总 wall 的提升取决于每个 benchmark 中 `V(node)`、输出写回、层次映射的调用密度；不能把这个 microbenchmark 直接换算成 EVAS 对 Spectre AX 的最终速度优势。

### Regression

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| focused cache tests | not present | `4 passed` | mapped/parent/cache-clear 行为被锁住 |
| indexed/backend related tests | 旧覆盖 | `73 passed` | indexed array、parent mapping、capability flags 无回归 |
| full EVAS tests | `431 passed` at 012 | `435 passed` | 全量回归通过，新增 4 个测试 |
| cache lifetime | no cache | run 结束后 cache disabled + empty | 避免跨 run 状态污染 |

## Functional Safety

- Default backend changed: `yes, internal node-name resolution cache is enabled inside Simulator.run`
- Numerical voltage path changed: `no`
- Event interpolation changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes, cache can be disabled and cleared`
- Accuracy impact: `none expected`; cached data is node-name mapping only, not waveform/state data

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestCompiledModelHelpers::test_node_resolution_cache_resolves_mapped_reads_and_writes tests/test_engine.py::TestCompiledModelHelpers::test_node_resolution_cache_resolves_parent_mapped_nodes tests/test_engine.py::TestCompiledModelHelpers::test_node_resolution_cache_disable_clears_stale_mapping tests/test_engine.py::TestCompiledModelHelpers::test_simulator_clears_node_resolution_cache_after_run -q
python3 -m pytest tests/test_indexed_backend.py tests/test_engine.py::TestCompiledModelHelpers tests/test_engine.py::TestCompiledModelCapabilityFlags -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
4 passed in 0.53s
73 passed in 0.40s
435 passed in 29.68s
git diff --check: clean
```

## Learning Notes

### 节点映射是什么？

一个 Verilog-A module 内部看到的是端口名：

```verilog
module inv(in, out);
```

但是 testbench 或上层 instance 里连接的可能是全局节点名：

```text
in  -> vin
out -> vout
```

所以模型每次读 `V(in)` 前，EVAS 都要知道它实际对应全局节点 `vin`。

### 为什么这会慢？

Python dict 用字符串做 key 时，需要做字符串 hash、查表、可能的 key 比较。单次看很小，但在仿真里可能发生几十万到几百万次。

对一个固定电路来说：

```text
"in" -> "vin"
```

这个关系在 run 内一般不会变。重复解析它就是纯开销。

### 为什么只缓存名字，不缓存电压？

电压是随时间变化的：

```text
V(vin, t0), V(vin, t1), V(vin, t2), ...
```

如果缓存电压值，就可能读到上一时刻的旧值，直接破坏仿真结果。

节点名映射不随时间变化，所以可以安全缓存：

```text
local node name -> external node name
```

然后每次仍然用 external node name 去读当前时刻的电压。

### 这和 Rust 化有什么关系？

Rust 化的目标不是在 Rust 里继续处理字符串，而是把：

```text
"vin"
```

提前变成整数 node id：

```text
vin -> 0
vout -> 1
```

最终模型求值会从：

```python
node_voltages["vin"]
```

变成类似：

```rust
values[vin_id]
```

013 仍然是 Python 优化，但它把“节点解析是 run-stable 的”这件事显式化了。后续 Rust IR 可以直接继承这个边界：编译/初始化阶段解析节点，仿真热循环只处理整数下标。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 有手写模型在 run 中动态修改 `node_map` | 修改后仍读到旧 external node | 关闭 `_set_node_resolution_cache_enabled(False)` 或回退 EVAS commit `b56454c` |
| cache 影响层级映射 | parent-mapped tests 失败 | 回退 `CompiledModel._resolve_external_node()` 相关改动 |
| cache 跨 run 污染 | run 后 `_node_resolution_cache` 非空 | `test_simulator_clears_node_resolution_cache_after_run` 失败 |
| full benchmark wall 没明显提升 | release speed rerun 无变化 | 保留 013 作为 Rust/node-id 前置，不把它包装成独立速度 claim |

## Next Step

下一篇审计文档建议：

- `014-expression-hotpath-profile-or-node-id-plan.md`：继续收敛 model evaluate 热路径，优先判断是先做表达式求值 profile，还是直接把 compiled model 的 branch access lowering 成 node-id aware helper。
