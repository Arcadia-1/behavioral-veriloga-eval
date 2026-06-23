# 016 - Static Branch Fast Helper Prototype

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 1cb5d34`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

基于 015 的静态 branch IO 边界，新增 opt-in codegen fast helper：静态 `V(node)` read 和静态 `V(out)<+` write 可以生成专门 helper；event 插值和 dynamic bus 仍保留旧路径。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| codegen | 所有静态 `V(node)` read/write 都生成 `_get_voltage()` / `_set_output()` | `static_branch_fastpath_codegen=True` 时生成 `_get_static_branch_voltage()` / `_set_static_branch_output()` | 默认 codegen 不变 |
| simulator run | 无 fastpath 统计 | `static_branch_fastpath=True` 时聚合 fastpath codegen model 数、静态 read/write 节点数、event fallback 次数 | 只影响 opt-in 计数 |
| netlist runner | 无 CLI/env 开关 | `EVAS_STATIC_BRANCH_FASTPATH=1` 或 `evas_static_branch_fastpath=true` 同时打开 compile/run opt-in | 默认仿真不变 |
| event read | `_get_voltage()` 负责 crossing-time interpolation | helper 在 event context 直接 fallback 到 `_get_voltage()` | event 语义不变 |
| dynamic bus | `V(bus[i])` 拼运行时节点名 | 保持 `_get_voltage(f'...')` / `_set_output(f'...')` | dynamic bus 不变 |

## Principle

014 证明普通 model IO 密度很高，015 证明哪些 branch IO 可以静态识别。016 先验证一个问题：

```text
如果普通静态 branch read/write 不再走完整通用 helper，会不会有局部速度收益？
```

当前 `_get_voltage()` 和 `_set_output()` 是通用路径，需要兼顾：

- 无 `node_map` 的直接节点；
- mapped port；
- `@parent:` 层次映射；
- indexed array sidecar；
- event body interpolation；
- output self-read；
- missing node 默认 0。

静态 branch helper 只拿掉一部分通用分支，但仍保留：

- local node 到 external node 的解析；
- indexed sidecar 读写；
- output self-read；
- event context fallback。

所以它不是 Rust 化终点。它是一个中间原型，用来判断“普通静态 branch lowering 是否值得继续向 node-id direct array 推进”。

## Important Finding

一开始把 read/write hit counter 放在 helper 热路径里，microbenchmark 反而变慢。原因是 Python 每步 `dict` 计数递增本身就很贵，会吃掉 helper 省下的分支成本。

因此最后版本不做 per-call hit counter，只记录：

- fastpath codegen 覆盖了多少 model；
- 覆盖了多少静态 read/write 节点；
- event fallback 发生了多少次。

这条经验很重要：后续 profiling counter 应该尽量放在 run-level、model-level 或采样路径，不能长期放在每个 `V(node)` read/write 热路径里。

## Before / After Evidence

Validation commands:

```bash
python3 -m pytest tests/test_engine.py::TestSimulator::test_static_branch_fastpath_matches_default_and_counts_hits tests/test_engine.py::TestCompiledModelHelpers::test_static_branch_voltage_falls_back_to_event_interpolation -q
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_counts_dynamic_branch_io_metadata -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_static_branch_fastpath_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
2 passed in 0.64s
1 passed in 0.29s
1 passed in 0.39s
443 passed in 32.70s
git diff --check: clean
```

Local helper microbenchmark:

```text
N=400000 evaluate() calls, repeats=9, mapped pass-through model

default_codegen: median=0.578743s min=0.409921s max=0.879367s
fast_codegen:    median=0.398961s min=0.391158s max=0.592255s
local speedup:   1.45x by median
```

Interpretation:

- 这是 helper 热路径 microbenchmark，不是 release-wide speed claim。
- 结果说明 static branch lowering 有潜力，但仍有噪声。
- 下一步如果直接改成 node-id array read/write，收益应该更清晰，因为可以跳过 string key lookup 和 local-to-external node resolution。

## Functional Safety

- Default backend changed: `no`
- Default generated code changed: `no`
- Opt-in generated code changed: `yes`
- Event interpolation changed: `no`
- Dynamic bus changed: `no`
- CSV schema changed: `no`
- Checker behavior changed: `no`
- Accuracy impact: `none expected`; tests compare default/fastpath waveform equality

## Learning Notes

### codegen opt-in 和 run opt-in 是什么区别？

codegen opt-in 决定生成的 Python 代码长什么样：

```text
默认: V(vin) -> self._get_voltage("vin", nv)
fast: V(vin) -> self._get_static_branch_voltage("vin", nv)
```

run opt-in 负责把这次运行标记为 fastpath 实验，并输出统计：

```text
static_branch_fastpath_codegen_models
static_branch_fastpath_static_read_nodes
static_branch_fastpath_static_write_nodes
static_branch_fastpath_fallbacks_total
```

runner 里的 `EVAS_STATIC_BRANCH_FASTPATH=1` 会同时打开两者。

### 为什么 event body 不能直接快读？

普通 read 是：

```text
V(node) at current step
```

event body read 可能是：

```text
V(node) at crossing time
```

crossing time 可能落在两个 transient step 中间，所以要用前一步和当前步插值。016 helper 只要发现 `_event_context_active`，就回到 `_get_voltage()`，避免破坏这个语义。

### 为什么 dynamic bus 不碰？

`V(dout[i])` 的节点名由运行时 `i` 决定，不能静态替换成单个 helper 节点：

```text
dout[0], dout[1], dout[2], ...
```

016 继续让它走旧路径。后续如果要优化，需要单独做 dynamic bus node-id lowering。

## Recommended Follow-Up Projects

| 编号 | 项目 | 目标 | 为什么能加速 | 风险/精度影响 | 建议验证 |
|---|---|---|---|---|---|
| 017 | Static branch node-id direct array | 把 016 helper 继续降到 `values[node_id]` 读写 | 跳过 string key lookup、`node_map` resolve、dict membership | 需要保证 mapped/parent node id 绑定正确；event fallback 继续隔离 | default vs opt-in waveform parity；helper microbench；examples smoke |
| 018 | Event interpolation IR | 给 event-body read 单独建插值 IR | 为 Rust event evaluator 准备边界，避免误把 event read 当 current-step read | event ordering/crossing time 最敏感 | sample-hold、cross/above regression；Spectre parity slice |
| 019 | Dynamic bus lowering | 把 `V(bus[i])` 从字符串拼接降到 base id + offset | 大量 DAC/ADC bus 写可减少字符串格式化 | bus 方向、二维 bus、稀疏节点要谨慎 | bus fixture、2D bus tests、converter examples |
| 020 | Indexed model state arrays | 把 `self.state["x"]` / `self.arrays["a"][i]` 迁移到 indexed state | 减少 Python dict/object 开销，是 Rust ABI 的状态侧准备 | 状态初始化、integer rounding、array bounds | state-heavy examples；integer/state regression |
| 021 | Rust model-evaluate ABI prototype | 先把最简单 static read/write model 用 Rust evaluate | 验证跨语言边界、node/state array 布局和返回协议 | ABI 设计错误会拖累后续迁移 | toy model parity；Python/Rust microbench；fallback path |
| 022 | Timer/breakpoint queue | 用 event queue 代替每步扫描 timer/cross/bound_step 候选 | CPPLL/ADPLL 这类任务每步扫描明显 | event ordering 和 missed breakpoint 风险高 | timer/cross regression；profile scan counters；PLL smoke |
| 023 | Sparse/required-signal CSV | 只输出 checker 必需信号或 edge/sparse trace | CSV write 在部分任务占 subprocess 10% 到 15% | checker 输入 schema 需要统一 | checker parity；CSV row/column contract tests |

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| helper 被误当默认路径 | 默认 generated code 出现 `_get_static_branch_voltage` | 回退 EVAS commit `1cb5d34` 或关闭 compile flag |
| event read 误走 current-step read | sample-hold/cross 采样偏移 | event context fallback 保持 `_get_voltage()` |
| dynamic bus 被误静态化 | `V(bus[i])` 输出节点错误 | dynamic indexed codegen 保持 `_set_output(f'...')` |
| microbenchmark 被当成论文速度 claim | 报告引用 016 local speedup | 明确需要 release-wide same-slice EVAS/Spectre/AX rerun |

## Next Step

建议下一篇做：

- `017-static-branch-node-id-direct-array.md`

016 已经证明普通静态 branch helper 有局部潜力，但它仍然是 Python string/dict helper。017 应该把 015 的 node-id plan 真正接到执行路径上，让普通静态 branch 读写变成数组下标操作。
