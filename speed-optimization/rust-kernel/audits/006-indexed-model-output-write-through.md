# 006 - Indexed Model Output Write-Through

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS 1d94807`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

在 `EVAS_INDEXED_ARRAYS=1` opt-in 路径下，让模型 `_set_output()` 写 dict 的同时 write-through 到 indexed voltage array，并把 post-model sync 改成“先校验、只在 mismatch 时修复”。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `CompiledModel` | `_set_output()` 只写 `output_nodes` 和 `node_voltages` dict | 新增 opt-in `_indexed_output_writer` hook | 默认无变化 |
| output write path | array mirror 依赖 post-model `dict -> array` sync | opt-in 时 `_set_output()` 直接写 array mirror | 默认无变化 |
| post-model sync | 每步 `indexed_array.update_from_mapping(self.node_voltages)` | 先比较 array/dict，只有 mismatch 才 repair sync | opt-in 行为更接近真正 array backend |
| stats/log | 没有输出 write-through 计数 | 新增 `indexed_output_write_throughs`、`indexed_output_write_through_nodes`、`indexed_post_model_sync_repairs` | opt-in 日志更可审计 |
| tests | 只验证 model IO plan | 新增 writer hook、parent-mapped output、netlist log 断言 | 默认无变化 |

## Principle

这一步属于 **降低每步成本** 的前置改造，并且比 005 更靠近真正热路径。

005 只是知道某个 model 会写哪些节点：

```text
model[0].output_node_ids = [node_id(vout)]
```

006 开始让实际输出写入同时进入 array：

```text
_set_output("out", value, node_voltages)
  -> node_voltages["vout"] = value      # 原 dict 路径，仍然权威
  -> indexed_values[node_id(vout)] = value   # opt-in write-through
```

这样 post-model 阶段不再需要无条件把整个 dict 复制到 array。现在逻辑变成：

```text
compare(indexed_values, node_voltages)
if mismatch:
    repair by update_from_mapping()
```

这保留了安全网：如果某个模型绕过 `_set_output()` 直接改 `node_voltages`，`indexed_post_model_sync_repairs` 会变成非零，提示这条路径还不能完全依赖 write-through。

## What Still Stays Dict-Backed

这一步没有迁移模型输入读语义：

- `_get_voltage()` 仍然读 dict。
- `_prepare_step()` 仍然缓存 dict snapshots。
- cross/above event interpolation 仍然用 dict。
- timer、transition、event ordering 仍然不变。

所以 006 只移动了 **output write side**，没有移动 **input read side**。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default backend | `python_dict` | `python_dict` | 默认仿真没有切换 |
| output array write-through | none | `_indexed_output_writer` under `indexed_arrays=True` | 只在 opt-in 下启用 |
| mapped output node resolution | dict-only | writer receives resolved external node | `node_map` 和 `@parent:` 输出可 write-through |
| post-model sync | unconditional full mapping update | validation first; repair only on mismatch | opt-in path 更接近真实 array backend |
| sync repair count | not available | `indexed_post_model_sync_repairs` | 检测绕过 `_set_output()` 的直接 dict 写 |
| mapped output parity | passed before | still passed | 输出 write-through 不改变波形 |
| targeted tests | `18 passed` at previous step | `4 passed` focused writer/output tests | 新增 writer hook coverage |
| full EVAS tests | `422 passed` at previous step | `424 passed` | 新增 2 个测试，无回归 |

Important interpretation:

- 006 仍不是 paper-facing speed claim。
- 它开始消除一部分 `dict -> array` sync 的必要性，但只在 opt-in diagnostic path 下。
- 真正的速度收益要等 model input reads、event handling、state updates 也逐步 indexed/Rust 化后再测。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, because writer hook is installed only under `indexed_arrays=True`
- Accuracy impact: `none expected`, because dict output write remains authoritative and post-model mismatch repair still exists

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestSimulator::test_indexed_arrays_build_model_io_plan_without_changing_mapped_output tests/test_engine.py::TestCompiledModelHelpers::test_indexed_output_writer_sees_resolved_output_node tests/test_engine.py::TestCompiledModelHelpers::test_indexed_output_writer_resolves_parent_mapped_node tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
4 passed in 0.43s
424 passed in 28.42s
git diff --check: clean
```

## Learning Notes

### 什么是 write-through？

write-through 的意思是：同一次写操作同时写到两个存储位置。

在这里，旧路径是：

```text
node_voltages["vout"] = value
```

006 的 opt-in 路径是：

```text
node_voltages["vout"] = value
indexed_values[node_id(vout)] = value
```

这样 array mirror 不再只能靠“事后整表同步”得到新值，而是在输出发生的那一刻就被更新。

### 为什么这一步比 005 更接近加速？

005 只是知道“谁会写哪里”。006 开始改变 opt-in path 的实际数据流：

```text
before:
  evaluate writes dict
  after evaluate copy dict into array

after:
  evaluate writes dict and array together
  after evaluate only validate/repair
```

如果后续所有模型输出都能通过 `_set_output()` write-through，post-model full dict sync 就可以逐步删除或只作为 debug guard。

### 为什么还不能删除 dict？

因为模型读输入仍然依赖 dict：

```text
V(inp) -> _get_voltage("inp", node_voltages)
```

而 `_get_voltage()` 包含 cross event 插值和 `@parent:` 解析等语义。输出写 path 相对简单，所以先迁它；输入读 path 要单独做，不适合混在同一个改动里。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 某些模型绕过 `_set_output()` 直接写 dict | `indexed_post_model_sync_repairs > 0` | 保留 repair sync，定位 direct dict write |
| writer 没解析到最终外部节点 | mapped output parity 或 parent writer test 失败 | 回退 `_set_output()` writer hook |
| opt-in path 被当作默认加速 | speed report 开了 `EVAS_INDEXED_ARRAYS=1` 但未说明 | 引用本审计：这是 diagnostic migration path |
| writer hook 泄漏到非 indexed run | default run 出现 indexed stats 或重复 writer 调用 | run 开始/结束都会清空 writer；若异常复现则回退 hook install 位置 |

## Next Step

下一篇审计文档建议：

- `007-indexed-model-input-read-probe.md`：先不改 `_get_voltage()` 主返回值，而是在 opt-in 下对 model input reads 做 indexed probe/compare，量化哪些读路径可安全从 dict 迁到 array。
