# 003 - Python Indexed Voltage Snapshot

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS 581b41e`

Related paths:

- `EVAS/evas/simulator/indexed.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

新增 opt-in indexed snapshot profile，量化每步 `dict(self.node_voltages)` 与 indexed/array snapshot 的关系，并证明 Python sidecar 只是测量和迁移闸门，不是最终加速路径。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| indexed sidecar | 没有专门的 per-step snapshot helper | 新增 `IndexedVoltageSnapshotter` | 默认无变化 |
| engine | 每步只执行 `prev_nv = dict(self.node_voltages)` | `indexed_snapshot_profile=True` 时额外生成 indexed snapshot 并记录 timing/parity stats | 默认无变化；opt-in 时额外 profile |
| runner | 没有 snapshot profile 开关 | 新增 `EVAS_INDEXED_SNAPSHOT_PROFILE=1` / `evas_indexed_snapshot_profile=true` | 默认无变化；opt-in 时 log 多一段 profile |
| tests | 只验证 indexed IR/trace parity | 增加 snapshotter、engine profile、netlist log 测试 | 默认测试覆盖更清楚 |

## Principle

这一步仍然属于 **降低每步成本** 的前置工作，但它的结论比“直接加速”更具体：

- 当前 EVAS 每步需要复制 `node_voltages` dict，作为 `prev_nv` 给 event/cross/tolerance 逻辑使用。
- 如果未来 hot loop 迁到 indexed array/Rust，理论上每步 snapshot 可以退化成 `list(values)` 或 Rust `Vec<f64>::clone()`。
- 但是如果还停留在 Python dict 输入，再做一次 `name -> id -> array`，会因为 Python 字符串查找和循环而更慢。

所以本轮目标不是替换默认 snapshot，而是建立一个 profile 开关，明确区分三件事：

- dict copy：当前真实默认路径。
- Python indexed-from-mapping：迁移旁路，用于验证，不适合当终点。
- pure array snapshot：未来 indexed/Rust backend 真正应该逼近的形态。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default backend | `python_dict` | `python_dict` | 默认仿真没有切换 |
| snapshot profile switch | none | `EVAS_INDEXED_SNAPSHOT_PROFILE=1` / `evas_indexed_snapshot_profile=true` | 旁路 profile 可显式开启 |
| snapshot parity max abs diff | not measured | `0.0` in unit/engine/netlist tests | indexed snapshot 与 dict snapshot 一致 |
| targeted indexed tests | `10 passed` | `11 passed` | 新增 snapshotter unit test |
| targeted engine/netlist tests | no snapshot profile tests | engine profile + netlist log tests pass | opt-in harness 可运行 |

Local microbenchmark, `50000` repetitions:

| Nodes | `dict()` copy | Python indexed-from-mapping | pure list snapshot |
|---:|---:|---:|---:|
| 8 | `0.012186 s` | `0.143760 s` | `0.005422 s` |
| 32 | `0.033882 s` | `0.571660 s` | `0.009625 s` |
| 128 | `0.137435 s` | `1.911981 s` | `0.015090 s` |
| 512 | `0.430503 s` | `7.122296 s` | `0.035200 s` |

Interpretation:

- Python indexed-from-mapping is slower than dict copy because it still starts from a Python dict and performs string-key id lookup.
- Pure list snapshot is much faster than dict copy as node count grows.
- The next real acceleration step should move the hot loop toward persistent array storage, not repeatedly convert dicts into arrays.

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, because snapshot profile is opt-in and default `prev_nv` dict remains authoritative

## Validation

Commands run:

```bash
python3 -m pytest tests/test_indexed_backend.py -q
python3 -m pytest tests/test_engine.py::TestSimulator::test_indexed_snapshot_profile_records_sidecar_timing_without_changing_result -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness -q
python3 -m pytest tests/test_indexed_backend.py tests/test_engine.py tests/test_netlist.py -q
```

Results:

```text
11 passed
1 passed
2 passed
248 passed
```

## Learning Notes

### 为什么 Python indexed-from-mapping 会慢？

它看起来用了数组，但入口仍然是 dict：

```python
for name, value in node_voltages.items():
    values[node_index.id_of(name)] = value
```

这里仍然有 Python 循环、字符串 key、函数调用和 float object 处理。它不是 Rust 化之后的目标形态，只是用来检查“节点编号是否正确”的过渡工具。

### 什么是 pure array snapshot？

如果内核已经持有数组：

```text
values = [vin, vout, clk, ...]
```

那么 snapshot 只需要复制一段连续内存：

```python
prev_values = list(values)
```

在 Rust 中类似：

```rust
let prev_values = values.clone();
```

这种操作不需要字符串查找，内存访问也连续，所以才是未来真正加速的方向。

### 这一步给我们的工程判断是什么？

不要把 Python indexed sidecar 当作性能终点。它的正确用途是：

- 建立 node id 和数组布局。
- 验证 round-trip/parity。
- 帮我们安全地把 dict hot loop 一段段迁走。

真正要快，后续必须让 model evaluate、source update、err_ratio scan、record point 等路径直接消费 indexed arrays。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 误把 Python sidecar 当作优化完成 | speed report 声称 indexed-from-mapping 更快 | 引用本审计 microbenchmark，继续迁到 persistent array/Rust |
| opt-in profile 污染正式速度测试 | release speed run 开了 `EVAS_INDEXED_SNAPSHOT_PROFILE=1` | paper speed 运行不启用该环境变量或 netlist option |
| snapshot parity 漏掉动态新增节点 | `indexed_snapshot_dynamic_nodes` 非零且后续 mismatch | 扩展 initial node collection 或提前 materialize output nodes |

## Next Step

下一篇审计文档建议：

- `004-python-indexed-kernel-arrays.md`：开始让 simulator 内部维护 persistent indexed voltage array，先在 source update / record point / err_ratio scan 中做 opt-in array path，再逐步替换 dict hot loop。
