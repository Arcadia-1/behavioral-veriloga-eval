# 007 - Indexed Model Input Read Probe

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS c24a2c9`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

新增 opt-in voltage read probe，让 `_get_voltage()` 在保持 dict 返回值不变的同时，把普通模型输入读与 indexed array mirror 做比较，为后续 array-backed input reads 收集安全证据。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `CompiledModel` | `_get_voltage()` 只返回 dict/output_nodes 语义值 | 新增 opt-in `_indexed_voltage_probe` callback | 默认无变化 |
| model input reads | 没有 array/dict 比较 | opt-in 时普通读比较 dict value 与 array value | 不改变返回值 |
| event-context reads | 与普通读混在 `_get_voltage()` 中 | opt-in probe 只计数 skip，不比较 event interpolation 值 | 避免误伤 cross/above 语义 |
| stats/log | 没有 input-read telemetry | 新增 `Indexed voltage read probe` | opt-in 日志更可审计 |
| tests | 覆盖 output write-through | 新增 resolved read node probe 和 netlist log 断言 | 默认无变化 |

## Principle

这一步继续属于 **降低每步成本** 的前置改造，但它只做 probe，不做替换。

当前 `_get_voltage()` 的核心路径是：

```text
local node name -> node_map/@parent resolution -> node_voltages dict -> value
```

007 在这个 value 已经算出来之后，额外做：

```text
array_value = indexed_values[node_id(resolved_node)]
diff = abs(array_value - dict_value)
```

但 `_get_voltage()` 仍然返回原来的 `dict_value`。也就是说：

```text
return value: unchanged
probe: diagnostic only
```

如果 `indexed_voltage_probe_mismatches == 0` 且 `indexed_voltage_probe_missing_nodes == 0`，说明这类普通输入读已经可以考虑下一步改成 array-backed read。

## Why Event Reads Are Skipped

`_get_voltage()` 在 cross/above event body 中不是简单读取当前节点值。它会根据 crossing time 做插值，并可能进行 exact-touch nudge：

```text
value = v0 + frac * (v1 - v0)
```

这个值不等于当前 time step 的 array value。因此 007 对 event-context reads 只计数：

```text
indexed_voltage_probe_event_skips += 1
```

不把它们计为 mismatch。event interpolation 需要单独迁移，不能和普通读混在一起。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default backend | `python_dict` | `python_dict` | 默认仿真没有切换 |
| input read probe | none | `_indexed_voltage_probe` under `indexed_arrays=True` | 只在 opt-in 下启用 |
| `_get_voltage()` return value | dict-backed | dict-backed | 精度路径不变 |
| event read handling | no special probe classification | event reads counted as skips | 避免把插值语义当 array mismatch |
| netlist e2e log | no read probe section | `Indexed voltage read probe` | 真实 runner 路径可见 |
| targeted tests | output writer only | `3 passed` focused read-probe tests | 新增 input-read coverage |
| full EVAS tests | `424 passed` at previous step | `425 passed` | 新增 1 个测试，无回归 |

Important interpretation:

- 007 仍不是 speed claim。
- 它开始收集 input-read migration evidence。
- 真正替换 `_get_voltage()` 仍需要下一步 gate：普通读先 array-backed，event-context 读继续 dict/interpolation-backed。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, because probe is installed only under `indexed_arrays=True`
- Accuracy impact: `none expected`, because `_get_voltage()` always returns the original dict-backed value

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestSimulator::test_indexed_arrays_build_model_io_plan_without_changing_mapped_output tests/test_engine.py::TestCompiledModelHelpers::test_indexed_voltage_probe_sees_resolved_read_node tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_arrays_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
3 passed in 0.46s
425 passed in 27.56s
git diff --check: clean
```

## Learning Notes

### 为什么 input read 比 output write 更危险？

output write 通常是：

```text
V(out) <+ value
```

它只要把 `value` 写到正确节点即可。

input read 则可能包含更多语义：

```text
V(inp)
```

在普通连续时间点，它是当前节点电压；但在 event body 里，它可能是 crossing time 上的插值电压。这就是为什么 006 可以先做 output write-through，而 007 只能先做 input read probe。

### 什么是 probe/compare？

probe/compare 是“旁路测量”：

```text
dict_value = existing_semantic_path()
array_value = indexed_sidecar_path()
record(abs(dict_value - array_value))
return dict_value
```

这样不会改变仿真结果，但能告诉我们 array sidecar 是否已经足够可信。

### 下一步如何真正加速？

如果普通读 probe 长期满足：

```text
mismatches = 0
missing_nodes = 0
```

下一步可以把非 event-context 的 `_get_voltage()` 普通读切到 array：

```text
if indexed reader enabled and not event_context:
    return indexed_values[node_id]
else:
    return dict/interpolated value
```

event-context reads 仍然先保留 dict/interpolation path。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| probe 把 event interpolation 误判为 mismatch | event-heavy case mismatch 激增 | 保持 event skip，单独设计 event read migration |
| array mirror 漏普通输入节点 | `indexed_voltage_probe_missing_nodes > 0` | 扩展 model IO plan 或 source/materialization |
| 普通读 array/dict 不一致 | `indexed_voltage_probe_mismatches > 0` | 关闭 `EVAS_INDEXED_ARRAYS`，定位 source/output/sync 路径 |
| probe overhead 污染速度 claim | release speed run 开启 probe | 正式 speed claim 不启用 `EVAS_INDEXED_ARRAYS` |

## Next Step

下一篇审计文档建议：

- `008-indexed-non-event-voltage-read.md`：在 probe 证据满足后，只把 non-event `_get_voltage()` 普通读切到 indexed array；event-context reads 继续保留 dict/interpolation path。
