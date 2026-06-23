# 005 - Indexed Model IO Boundary

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS 034ca66`

Related paths:

- `EVAS/evas/simulator/indexed.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

新增 per-model IO node-id plan，把每个模型实例的 mapped ports 和 output nodes 显式编号，为后续把 Verilog-A model evaluate 迁到 indexed/Rust backend 建立边界。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| indexed helper | 只有 run-level source/record/model node ids | 新增 `IndexedModelIO` 和 `IndexedModelIOPlan` | 默认无变化 |
| node resolution | model IO 只隐含在 `node_map` / `output_nodes` dict 中 | `build_indexed_model_io_plan()` 解析 mapped ports、outputs、`@parent:` 层次映射 | 默认无变化 |
| engine opt-in path | `indexed_arrays=True` 只维护 voltage array mirror | 同时刷新 model IO plan，并把 IO 节点预 materialize 到 array mirror | 默认无变化 |
| runner log | 只输出 indexed array profile | opt-in 时额外输出 `Indexed model IO plan` | 默认无变化 |
| tests | 没有 model IO plan 的专门契约 | 新增层次映射 plan、mapped output parity、netlist log 测试 | 覆盖更明确 |

## Principle

这一步仍然属于 **降低每步成本** 的前置改造，但它瞄准的是下一层瓶颈：model evaluate 的节点访问边界。

现在 EVAS 的模型访问节点主要靠两个 dict：

```text
model.node_map     = {"inp": "vin", "out": "vout"}
model.output_nodes = {"out": 0.75}
```

模型内部写：

```text
V(out) <+ f(V(inp))
```

运行时需要先把模型局部端口名映射到外部节点名：

```text
inp -> vin
out -> vout
```

005 做的是把这个边界编号化：

```text
vin  -> node_id 0
vout -> node_id 1

model[0].mapped_port_node_ids = [0, 1]
model[0].output_node_ids      = [1]
```

这还没有把 `_get_voltage()` 和 `_set_output()` 改成 array 主路径。它只是把“模型需要读哪些外部节点、会写哪些输出节点”变成显式 IR。后续 Rust kernel 可以先消费这个 IR，再逐步替换 dict lookup。

## Why Not Rewrite `_get_voltage()` Yet?

`_get_voltage()` 不只是普通读节点。它还包含事件语义：

- `node_map` 映射。
- `@parent:` 层次映射。
- cross/above 事件里的时间插值。
- exact-touch crossing 的 post-side nudge。
- 回退到 `output_nodes`。

如果现在直接把 `_get_voltage()` 改成 array 读，一旦出错很难判断是“节点编号错了”，还是“事件插值语义错了”。所以 005 只做边界显式化，先让编号、层次映射、输出集合刷新都可测试。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default backend | `python_dict` | `python_dict` | 默认仿真没有切换 |
| model IO plan | none | `IndexedModelIOPlan` | model IO 边界可审计 |
| `@parent:` resolution | only inside runtime helper logic | plan builder resolves parent-mapped nodes | 层次模型边界可编号 |
| opt-in log | `Indexed array profile` | plus `Indexed model IO plan` | 速度/迁移报告能看到 model IO 覆盖 |
| default vs indexed mapped output | not tested | identical in engine parity test | IO plan 不改变输出 |
| netlist e2e indexed arrays log | array stats only | confirms mapped_port_count/output_count | 真实 runner 路径可见 |
| targeted indexed tests | `17 passed` at previous step | `18 passed` | 新增 model IO tests |
| full EVAS tests | `420 passed` at previous step | `422 passed` | 新增 2 个测试，无回归 |

Important interpretation:

- 005 不是速度 claim。
- 它为 Rust 化准备 model-level IR。
- 默认仿真、CSV、checker、strobe、event ordering 都不变。
- 当前 opt-in path 仍然保留 dict 作为权威状态。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, because model IO plan only appears under `indexed_arrays=True`
- Accuracy impact: `none expected`, because `_get_voltage()`, `_set_output()`, `_prepare_step()`, cross/timer/event semantics remain dict-backed

## Validation

Commands run:

```bash
python3 -m pytest tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_indexed_arrays_preserve_source_record_and_error_scan_results tests/test_engine.py::TestSimulator::test_indexed_arrays_build_model_io_plan_without_changing_mapped_output tests/test_netlist.py::TestIndexedMigrationHarness -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
18 passed in 1.08s
422 passed in 28.03s
git diff --check: clean
```

## Learning Notes

### 什么是 model IO boundary？

可以把 EVAS 的仿真分成两层：

```text
外层 simulator:
  管理时间、source、record、step size、全局 node_voltages

内层 model:
  执行某个 Verilog-A module 的行为逻辑
```

model IO boundary 就是两层之间的接口：

```text
model 从哪些节点读输入？
model 往哪些节点写输出？
这些局部端口名对应外部哪个 netlist 节点？
```

Rust 化不能一上来只看 `node_voltages` 数组，还必须知道每个 model 的端口如何映射，否则模型内部的 `inp/out/clk` 无法对应到全局数组里的整数下标。

### 为什么层次模型会有 `@parent:`？

当一个 Verilog-A module 内部实例化子 module 时，子模型的端口可能先映射到父模型的局部端口，再由父模型映射到顶层 netlist 节点：

```text
child.a -> @parent:inp
parent.inp -> VIN
```

最终 child 真正读的是：

```text
child.a -> VIN
```

005 的 plan builder 会解析这种链路，把最终外部节点 `VIN` 编号。

### 这一步为什么对 Rust 很关键？

Rust 内核需要避免字符串 lookup。理想路径不是：

```text
每次 evaluate:
  "inp" -> node_map lookup -> "vin" -> dict lookup -> Python float
```

而是：

```text
compile/lower once:
  inp -> node_id 0
  out -> node_id 1

每次 evaluate:
  values[0] -> compute -> values[1]
```

005 做的就是 `compile/lower once` 的前半段：先把 model IO 边界编号化，并用测试证明它不会影响当前仿真语义。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| model IO plan 漏掉动态输出 | `indexed_model_io_outputs` 偏低，array dynamic nodes 异常增长 | 关闭 `EVAS_INDEXED_ARRAYS` 或扩展 output version refresh |
| `@parent:` 解析错误 | 层次 model plan test 失败，mapped output parity 失败 | 回退 `build_indexed_model_io_plan()` 的 parent resolution |
| 误把 IO plan 当成模型已 Rust 化 | speed report 声称 model evaluate 已 array-backed | 引用本审计：evaluate/cross/timer 仍 dict-backed |
| plan 刷新成本污染正式速度测试 | release speed run 开了 `EVAS_INDEXED_ARRAYS=1` | 正式 speed claim 不启用该 opt-in 开关 |

## Next Step

下一篇审计文档建议：

- `006-indexed-model-output-write-through.md`：在不改 `_get_voltage()` 事件语义的前提下，先让 `_set_output()` 或 simulator post-evaluate sync 通过 model IO plan 做 output write-through/validation，继续缩小 dict 写路径。
