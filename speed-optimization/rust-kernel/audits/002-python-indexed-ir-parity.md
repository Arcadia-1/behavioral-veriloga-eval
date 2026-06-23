# 002 - Python Indexed IR Parity

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS 142b8ba`

Related paths:

- `EVAS/evas/simulator/indexed.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

新增 opt-in 的 Python indexed IR/parity harness：默认仿真路径不变，但可以显式验证 dict waveform 到 indexed trace 的 lowering/round-trip 是无损的。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| indexed sidecar | 只有 `NodeIndex`、`StateIndex`、`IndexedVoltages` 基础 helper | 新增 `IndexedRunPlan`、`IndexedTrace`、`IndexedParityReport` | 默认无变化 |
| runner | `evas_simulate()` 只运行 dict backend | `EVAS_INDEXED_PARITY=1` 或 `evas_indexed_parity=true` 时执行旁路 parity | 默认无变化；opt-in 时 log 多一段 parity 结果 |
| tests | indexed helper 只测基础映射 | 新增 plan/trace/report unit test 和小 netlist e2e | 默认测试覆盖更清楚 |

## Principle

这一步不是直接提速，而是 Rust 化前的安全闸门。

未来真正加速会来自 **降低每步成本**：把热循环中的 `dict[str, float]`、字符串 key lookup、Python object copy，逐步换成整数 node id 和数组访问。要做这件事，第一步不是立刻替换仿真器，而是先证明：

- 同一个节点/信号集合可以稳定映射成整数 id。
- 当前 dict waveform 可以转成 indexed trace。
- indexed trace 再转回 dict waveform 后，数值和信号名不变。

换句话说，这一步验证“数据表示方式可以换”，还没有开始改变“仿真语义怎么执行”。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default backend | `python_dict` | `python_dict` | 默认仿真没有切换 |
| indexed parity switch | none | `EVAS_INDEXED_PARITY=1` / `evas_indexed_parity=true` | 旁路验证可显式开启 |
| targeted indexed/netlist tests | `73` related tests | `76` related tests | 新增 3 个 indexed unit tests 和 1 个 netlist e2e，原有相关测试继续通过 |
| parity max abs diff | not measured | `0.0` in unit/e2e round-trip | lowering/round-trip 没有引入数值差异 |
| speed impact | none | none by default | opt-in harness 额外拷贝 waveform，不作为加速路径 |

这些证据只证明 IR lowering 安全，不证明 EVAS 已经比 Spectre AX 更快。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, 因为 indexed parity 是旁路，默认仍走 `python_dict`

## Validation

Commands run:

```bash
python3 -m pytest tests/test_indexed_backend.py -q
python3 -m pytest tests/test_netlist.py::TestIndexedParityHarness::test_evas_simulate_runs_indexed_parity_when_opted_in -q
python3 -m pytest tests/test_indexed_backend.py tests/test_netlist.py -q
```

Results:

```text
10 passed
1 passed
76 passed
```

## Learning Notes

### 什么是 IR？

IR 是 intermediate representation，中间表示。可以把它理解成“原始代码和最终执行内核之间的一份结构化说明书”。

现在 EVAS 热循环主要直接读写 Python dict：

```python
node_voltages["vin"]
node_voltages["vout"] = value
```

Rust 或 indexed backend 更适合读写数组：

```text
vin -> node id 0
vout -> node id 1
values[0]
values[1] = value
```

`IndexedRunPlan` 就是第一版很轻量的 IR：它记录哪些 source、recorded signal、model node 会映射到哪些 id。

### 为什么要先做 parity harness？

如果直接改内核，后面出现差异时很难判断是两类问题中的哪一种：

- 数据表示错了：比如 `vout` 被映射成了 `vin`。
- 仿真语义错了：比如 cross/timer/event ordering 改坏了。

本轮只验证第一类问题。先把“名字到 id 到名字”的转换锁住，后面改 event queue、Rust loop、array backend 时，debug 范围会小很多。

### 为什么这一步不提升速度？

因为默认路径完全没有启用 indexed trace。即使手动打开 `EVAS_INDEXED_PARITY=1`，它也是在 dict 仿真结束后额外拷贝 waveform 做检查，反而会多一点开销。它的价值是让后续速度优化可审计，而不是自己加速。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| parity harness 被误认为默认 backend | speed report 里把 `EVAS_INDEXED_PARITY=1` 当成正式速度路径 | 只在 migration/debug 中启用；paper speed 不开该开关 |
| node id 计划漏掉后续 backend 必需节点 | future backend parity test 找不到 node id | 扩展 `build_indexed_run_plan()` 的 node collection |
| opt-in parity 误伤正常仿真 | `EVAS_INDEXED_PARITY=1` 下 `evas_simulate()` 返回 false | 回退 `runner.py` 中 parity 开关接线，默认路径不受影响 |

## Next Step

下一篇审计文档建议：

- `003-python-indexed-voltage-snapshot.md`：把每步 `prev_nv = dict(self.node_voltages)` 的旁路 indexed snapshot 做出来，先 profile/验证，再决定是否接入默认 kernel。
