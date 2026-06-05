# 094s - Persistent Typed-Array Engine Slice

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS/prototypes/audit_094s_pipeline_stage_bound_array_slice.py`
- `EVAS/evas/simulator/analog_block_runtime.py`
- `EVAS/tests/test_audit_094o_analog_block_runtime.py`
- `behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094r-engine-dispatch-contract-and-no-default.md`

## One-Line Summary

新增 094s bound-array prototype，把 `pipeline_stage` 的 Verilog-A port 直接绑定到全局 `IndexedVoltageArray` node id，验证去掉 node dict pack/sync 后 same-grid 语义不变，并带来约 `1.137x` 的局部 replay 提速。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Analog-block breakpoint API | 调用者需要知道 runtime 内部 transition runtime | `RustAnalogBlockShadowRuntime.next_breakpoint()` 统一暴露 runtime-owned breakpoint | unchanged |
| Node value ownership smoke | 094q 每步从 Python dict 打包 node array，再同步输出回 dict | 094s 将 module ports lowering 到全局 node ids，Rust runtime 直接读写 persistent indexed array | unchanged |
| Speed evidence | 只有 094q wrapper E2E 负优化和 094p replay wall | 新增 dict-pack replay vs bound-array replay A/B | unchanged |

## Principle

094q 变慢的一个可疑点是每步数据边界：

```text
Python dict node_voltages
  -> pack module ports into node array
  -> ctypes/Rust runtime
  -> sync output nodes back into dict/model state
```

094s 把这部分拆出来做 A/B。两边都使用同一个 094o Rust analog-block runtime、同一个 reference EVAS time/source grid、同样的 `transition()` breakpoint 查询；差别只有 node value ownership：

```text
dict-pack replay:
  dict[str, float] -> local node array -> Rust -> dict[str, float]

bound indexed-array replay:
  global node ids -> one persistent IndexedVoltageArray.values -> Rust in place
```

这样可以单独回答：只去掉 node dict pack/sync，收益有多大？

## Before / After Evidence

Command:

```bash
PYTHONPATH=EVAS python3 EVAS/prototypes/audit_094s_pipeline_stage_bound_array_slice.py
```

Result:

| Metric | Dict-pack replay | Bound indexed-array replay | Interpretation |
|---|---:|---:|---|
| Repeat passes | 32 | 32 | same workload multiplier |
| Steps | 24416 | 24416 | same replay grid |
| Fired events | 961 | 961 | same event behavior |
| Breakpoint hits | 416 | 416 | same runtime-owned transition breakpoint visibility |
| Wall | `3.536441s` | `3.109396s` | bound array is faster |
| Speedup vs dict-pack | `1.000x` | `1.137x` | node direct binding helps, but modestly |
| First-pass max signal abs vs reference | `4.8599966967488584e-08` | `4.8599966967488584e-08` | same-grid output parity preserved |
| First-pass close <= 1e-6 | true | true | semantic smoke passed |

Decision:

```text
BOUND_ARRAY_SLICE_PASSED_BUT_NOT_ENGINE_DISPATCH
```

## Interpretation

这个结果有两个信息：

1. **direct node-id binding 是正确方向。** 它不改变 `pipeline_stage` same-grid 输出，并且去掉 dict pack/sync 后局部 replay 有 `1.137x` 提升。
2. **它不是大瓶颈的全部。** 如果只优化 node packing，收益只有十几个百分点，不能解释或修复 094q 里 `3.219s` vs `1.453s` 的 full-sim 负优化。

剩余大开销更可能在：

- 每步 Python 调用 Rust runtime / ctypes 边界；
- event due/body/transition 分阶段多次 Python orchestration；
- state dict / state array 同步；
- source/adaptive scheduler 仍在 Python；
- record/CSV 和 rowwise grid policy 仍在 Python。

因此 094s 之后不应继续只做局部 pack/sync 微优化。下一步应该做 whole-step batch：把 source update、event due、event body、transition step、breakpoint query、record gather 尽量放进一个 typed-array step contract。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 EVAS/prototypes/audit_094s_pipeline_stage_bound_array_slice.py
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094o_analog_block_runtime.py -q
```

Results:

```text
094s prototype: BOUND_ARRAY_SLICE_PASSED_BUT_NOT_ENGINE_DISPATCH
094o pytest: 1 passed in 0.67s
```

## Learning Notes

对不熟悉 Rust/Python 边界的人，可以这样理解：

- `dict` 像按名字查格子：每次要用 `"VIN"`、`"PHI1"` 这些字符串找值。
- `IndexedVoltageArray` 像固定座位表：`VIN` 永远是第 4 个格子，Rust 只拿数字下标访问。
- 094s 证明固定座位表确实省时间，但如果每走一步仍要 Python 指挥很多次 Rust 小函数，省下来的字符串查找不是总成本的大头。

所以真正的 Rust 化不是把每个小动作都换成 Rust，而是减少 Python/Rust 来回切换次数，把一整步仿真的数据流变成一个批处理。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| replay grid 复用 reference EVAS，不能证明 Rust scheduler | rowwise full sim 仍失败 | 不接 engine，继续做 scheduler-owned slice |
| `1.137x` 被误读成 EVAS E2E speedup | paper/report overclaim | 文档明确它只是 replay adapter A/B |
| 只覆盖 `pipeline_stage` | 其他模型 source/node map 更复杂 | 后续做 capability manifest 和多 row sweep |

## Next Step

建议下一步编号：

- `094t - Whole-Step Typed-Array Batch Contract`

目标：不要继续只优化 node packing，而是把一个仿真 step 内的 source update、event due、event body、transition step、next breakpoint 和 record gather 合并为更粗粒度的 batch。验收条件应至少包括：

- `pipeline_stage` same-grid parity；
- 与 094s 相比明显减少 Python/Rust call count；
- replay wall 优于 bound-array slice；
- 仍不默认接 `engine.py`，直到 full-sim rowwise/defined-grid policy 通过。
