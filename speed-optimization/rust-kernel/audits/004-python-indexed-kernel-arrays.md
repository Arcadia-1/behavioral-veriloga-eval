# 004 - Python Indexed Kernel Arrays

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS fe6d142`

Related paths:

- `EVAS/evas/simulator/indexed.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

新增 opt-in persistent indexed voltage array，让 EVAS 在 source update、record point、err_ratio scan 这些低风险路径开始消费 node-id array，为后续 Rust kernel 替换 dict hot loop 做实测前置。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| indexed helper | 只有 fixed `IndexedVoltages` 和 profiling 用 `IndexedVoltageSnapshotter` | 新增可动态增长的 `IndexedVoltageArray` | 默认无变化 |
| engine state | `self.node_voltages: dict[str, float]` 是唯一运行态电压存储 | `indexed_arrays=True` 时维护一份 array mirror | 默认无变化；opt-in 时额外记录 array stats |
| source update | 每步写 `self.node_voltages[src.node]` | opt-in 时同步写 `IndexedVoltageArray[node_id]` | 默认无变化 |
| record point | 从 dict `.get(name, 0.0)` 读记录信号 | opt-in 时从 array mirror 读记录信号 | opt-in parity 测试证明记录结果不变 |
| err_ratio scan | 从 dict 读 `vnew/vold` 计算动态步长误差 | opt-in 时从 current/previous array snapshot 读 `vnew/vold` | opt-in parity 测试证明时间点、步长、波形不变 |
| runner | 无 array 开关 | 新增 `EVAS_INDEXED_ARRAYS=1` / `evas_indexed_arrays=true` | 默认无变化；opt-in log 增加 `Indexed array profile` |

## Principle

这一步属于 **降低每步成本** 的前置改造。

EVAS 当前把电路节点电压表示成：

```text
node_voltages = {"vin": 0.25, "vout": 0.75, "clk": 1.0}
```

这个表示直观，但每一步都要付出 Python dict 的成本：字符串 hash、key lookup、Python object 装箱、dict copy。

indexed array 的想法是先给每个节点一个稳定编号：

```text
vin  -> 0
vout -> 1
clk  -> 2
```

然后把同一个电压状态写成向量：

```text
V(t) = [0.25, 0.75, 1.0]
```

仿真器数学上仍然是在更新同一个状态向量 `V(t)`。区别只在工程表示：

```text
dict:  V("vout") -> hash("vout") -> value
array: V[1]      -> direct indexed load
```

这次没有改变误差控制公式。原来的 err_ratio 是：

```text
dv  = abs(vnew - vold)
tol = reltol * max(abs(vnew), abs(vold)) + vabstol
er  = dv / tol
```

现在 opt-in array path 仍然用完全相同的公式，只是 `vnew/vold` 的读取来源从 dict 变成 array mirror。因此如果 array mirror 和 dict 对齐，数学结果应当完全一致。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default backend | `python_dict` | `python_dict` | 默认仿真没有切换 |
| array switch | none | `EVAS_INDEXED_ARRAYS=1` / `evas_indexed_arrays=true` | 仅 opt-in |
| source update array writes | not available | counted by `indexed_array_source_updates` | source 路径已接入 array mirror |
| record array reads | not available | counted by `indexed_array_record_reads` | record 路径已接入 array mirror |
| err_ratio array reads | not available | counted by `indexed_array_err_ratio_reads` | 动态步长误差扫描已接入 array mirror |
| default vs indexed time grid | not tested | identical in engine parity test | opt-in 不改变 accepted time points |
| default vs indexed step sizes | not tested | identical in engine parity test | opt-in 不改变动态步长结果 |
| default vs indexed recorded signal | not tested | identical in engine parity test | opt-in 不改变输出波形 |
| array max abs diff | not available | `0.0` in engine/netlist tests | array mirror 与 dict 对齐 |
| full EVAS tests | `417 passed` at previous step | `420 passed` | 新增 3 个测试，无回归 |

Important interpretation:

- 这一步仍然不是最终速度 claim。
- 因为 model evaluate/cross/timer 仍然依赖 dict，opt-in path 还需要 `dict -> array` sync。
- 这一步的价值是把 array 作为运行态 mirror 接入热路径，验证节点编号、previous snapshot、record/err_ratio 读取语义都正确。
- 后续只有继续把 model evaluate、event/cross/timer、model output 写入迁到 indexed/Rust，才能真正去掉 dict 同步开销。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, because `EVAS_INDEXED_ARRAYS` is opt-in
- Accuracy impact: `none expected`, because default path is unchanged and opt-in path keeps the same err_ratio formula with `max_abs_diff = 0.0` parity checks

## Validation

Commands run:

```bash
python3 -m pytest tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_indexed_snapshot_profile_records_sidecar_timing_without_changing_result tests/test_engine.py::TestSimulator::test_indexed_arrays_preserve_source_record_and_error_scan_results tests/test_netlist.py::TestIndexedMigrationHarness -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
17 passed in 0.51s
420 passed in 23.02s
git diff --check: clean
```

## Learning Notes

### 节点映射换电路怎么办？

节点映射不是手写固定表，而是在每次仿真启动时由当前电路自动生成。

如果换了一个电路，节点名字变了，例如：

```text
old circuit: vin, vout, clk
new circuit: inp, outp, sample_clk
```

EVAS 会针对新电路重新建立：

```text
inp        -> 0
outp       -> 1
sample_clk -> 2
```

所以节点映射不是跨电路复用的全局规则，而是每个 netlist/run 自己的本地编号表。

### 节点很多怎么办？

节点很多时 indexed array 反而更适合。

dict 路径每次读节点都像是：

```text
字符串 -> hash -> dict bucket -> Python float object
```

array 路径每次读节点更接近：

```text
整数 id -> 连续数组下标 -> float value
```

节点越多、每步访问越多，字符串 lookup 和 Python object 开销越明显。Rust/C 里这种 indexed array 通常会进一步变成连续的 `f64` 内存块，CPU cache 更容易命中。

### 为什么这次还要保留 dict？

因为 EVAS 的 Verilog-A model 现在仍然通过 dict 实现：

- `model.evaluate(self.node_voltages, time)`
- `cross/above` 事件读取节点电压
- `$bound_step`、timer、transition output refresh

如果一次性把这些都切成 array，任何一个事件语义偏差都会变成难定位的精度问题。当前做法是“先让低风险路径读 array，同时每步和 dict 对齐”，这样能逐步缩小改造半径。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| opt-in array path 被误当成最终加速版 | speed report 使用 `EVAS_INDEXED_ARRAYS=1` 但未说明仍有 dict sync | 回到 commit `fe6d142` 前或关闭环境变量 |
| array mirror 和 dict 脱节 | `indexed_array_mismatches > 0` 或 `max_abs_diff != 0.0` | 关闭 `EVAS_INDEXED_ARRAYS`，定位具体 sync/write 路径 |
| 动态新增输出节点漏编号 | `indexed_array_dynamic_nodes` 非预期增长且出现 mismatch | 扩展 initial node collection 或把 model output materialization 前移 |
| err_ratio array 读取影响步长 | default/indexed step sizes 不一致 | 回退 err_ratio array read，保留 source/record mirror |

## Next Step

下一篇审计文档建议：

- `005-indexed-model-io-boundary.md`：把 model input/output 的节点访问边界显式化，先生成 model port/output 的 node-id 表，再决定哪些 evaluate 子路径可以迁到 indexed array 或 Rust。
