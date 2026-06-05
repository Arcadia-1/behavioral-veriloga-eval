# 094r - Engine Dispatch Contract And No-Default Decision

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS/evas/simulator/transition_runtime.py`
- `EVAS/tests/test_audit_094n_transition_runtime.py`
- `EVAS/prototypes/audit_094p_pipeline_stage_shadow_sweep.py`
- `EVAS/prototypes/audit_094q_pipeline_stage_fullsim_wrapper.py`
- `behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094p-real-row-shadow-replay-gate.md`
- `behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094q-opt-in-full-sim-wrapper.md`

## One-Line Summary

固化 094q 暴露的 engine dispatch contract：Rust analog-block runtime 语义已经能在 `pipeline_stage` 上对齐，但默认接入 engine 前必须先解决 breakpoint ownership、typed-array 状态驻留、record/CSV policy 和 fallback gate。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Transition breakpoint contract | prototype 通过镜像 `model.transitions` 让 engine 临时看见 Rust transition state | `RustTransitionContributionRuntime.next_breakpoint()` 直接暴露 typed-array transition breakpoint 查询 | unchanged |
| Regression coverage | 094n 只验证 transition 输出值 | 094n 增加 ramp breakpoint 回归，覆盖 25%/50%/75%/end 和 `min_ramp_time` 抑制 interior point | unchanged |
| Production dispatch | 094q 证明直接 wrapper 会慢且 rowwise grid 仍不同 | 明确 `NO_DEFAULT_ENGINE_DISPATCH`，只保留 opt-in prototype/shadow path | unchanged |

## Principle

这一步的核心结论是：Rust 化不是“把一个 Python 函数替换成 Rust 函数”这么简单。EVAS engine 是一个调度系统，每一步都需要共享这些状态：

1. 当前节点电压和 source 值；
2. event due / cross / above / timer 的触发状态；
3. event body 对 state/output 的写入；
4. `transition()` 的 active ramp state 和下一个 breakpoint；
5. `$bound_step`、adaptive error、dirty snapshot；
6. record/CSV 需要采样的时间和信号集合。

094p 说明：如果外层给 Rust 正确时间网格和输入，Rust shadow runtime 可以算对 `pipeline_stage` 的核心输出。

094q 说明：如果让现有 engine 正常走步，但每步都从 Python dict 打包到 Rust arrays，再同步回来，E2E 会变慢；如果 transition state 不暴露给 engine，波形时间网格也会错。

因此 094r 的决策不是否定 Rust，而是拒绝把 prototype wrapper 作为默认 production path。真正的 production path 必须让 engine 自己围绕 typed arrays 运行，而不是每步做 Python dict/array 往返。

## Before / After Evidence

| Evidence | Result | Interpretation |
|---|---:|---|
| 094p same-grid shadow replay max abs diff | `4.8599966967488584e-08` | Rust event/body/transition 语义在 reference grid 上可信 |
| 094p Rust shadow replay wall | `0.083317s` | 只代表 analog-block replay，不是 E2E speed claim |
| 094q wrapper before transition visibility fix | `0.29990991139661183V` time-aligned max abs | engine 看不到 Rust transition breakpoint 会产生大波形误差 |
| 094q wrapper after transition mirror | `0.00010972991426716483V` time-aligned max abs | 暴露 transition state 后语义基本恢复 |
| 094q Python adaptive wall | `1.452739s` | 当前 EVAS reference |
| 094q Rust wrapper wall | `3.219042s` | 每步 Python pack/sync/ctypes 明显压过 Rust 核心收益 |
| 094q rowwise close | `false` | 仍不能声明 production parity |
| 094q decision | `FULLSIM_WRAPPER_TIME_ALIGNED_PASS_BUT_DO_NOT_DIRECT_WIRE` | 只能作为 opt-in prototype gate |

## Required Contract Before Default Engine Dispatch

| Contract item | Why it matters | Current state | Gate before production |
|---|---|---|---|
| Event due/body typed-array ownership | 避免每步 Python dict/object 写回 | 094o shadow runtime 已有局部 batch | engine loop 必须直接读写 persistent arrays |
| Transition breakpoint visibility | engine 必须知道 ramp 中间点和结束点 | 094r 新增 `next_breakpoint()` runtime API；094q prototype 仍靠镜像 | scheduler 使用 runtime API 或统一 transition queue |
| Source/adaptive time-grid ownership | full sim rowwise parity 取决于谁决定下一步时间 | 仍由 Python engine/source 管理 | Rust path 必须接入同一套 adaptive/breakpoint policy |
| State/output synchronization | 每步 dict pack/sync 是 094q 负优化主因 | 094q 每步打包 `node/state/param` arrays 并同步回 dict | state/node/output 持久驻留 typed arrays，Python 只在边界读取 |
| Record/CSV policy | rowwise CSV 对速度和精度声明都敏感 | 仍主要 Python-owned | 至少定义 rowwise parity policy；长期迁到 array/sparse trace path |
| Fallback/rejection gate | 不支持的模型必须回到当前 EVAS | builder 返回 `None` 可 fallback，但 094q prototype 是强制 wrapper | production opt-in 需要 per-module capability manifest 和 release-wide sweep |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094n_transition_runtime.py -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_audit_094n_transition_runtime.py EVAS/tests/test_audit_094o_analog_block_runtime.py -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094a_expr_ir.py EVAS/tests/test_audit_094b_stmt_schedule_ir.py EVAS/tests/test_audit_094d_state_binding_ir.py EVAS/tests/test_audit_094f_body_ir_encoder.py EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_audit_094n_transition_runtime.py EVAS/tests/test_audit_094o_analog_block_runtime.py EVAS/tests/test_rust_backend.py -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/evas/simulator/transition_runtime.py EVAS/tests/test_audit_094n_transition_runtime.py
```

Results:

```text
2 passed in 0.68s
10 passed in 1.91s
68 passed in 12.76s
py_compile: pass
```

094q full-sim wrapper was not re-run after adding the runtime API because the default engine is still intentionally disconnected. The previous 094q evidence remains the production gate: after transition-state mirror it is time-aligned close, but rowwise not close and slower than Python adaptive.

## Learning Notes

可以把这里理解成两层问题：

1. **数学计算层**：给定 `time`、节点电压、状态、参数，模型应该输出什么。094p 证明这一层 Rust 已经能在 `pipeline_stage` 上算对。
2. **仿真调度层**：下一步应该走到哪个时间、什么时候记录 CSV、什么时候插入 transition/cross/timer breakpoint。094q 证明这一层不能被 Python/Rust 分裂管理。

094q 的负优化主要来自第二层。Rust 只做模型主体，但 Python 每步仍要：

- 从 dict/string key 拿节点和状态；
- 打包成 arrays；
- 通过 ctypes 调 Rust；
- 再把 state/output/transition state 同步回 Python object；
- 最后由 Python engine 决定下一步和写 CSV。

这会让小模型或中等模型的 Rust 计算收益被边界成本吃掉。真正有效的 Rust 化方向是 whole-segment / whole-engine typed-array path，而不是更多 per-step wrapper。

## Decision

```text
NO_DEFAULT_ENGINE_DISPATCH
```

当前可以声明：

- 094p/094q 已证明 `pipeline_stage` 的 Rust event/body/transition runtime 在 shadow/opt-in 条件下语义可行；
- 094r 已把 transition breakpoint visibility 做成 runtime API；
- 这些仍不是 production speedup，也不是全量 Rust 化。

当前不能声明：

- EVAS 默认 Rust path 已完成；
- Rust EVAS 已快于 Python EVAS；
- Rust EVAS 已快于 Spectre AX；
- 全量 benchmark 已经通过 Rust production dispatch。

## Next Step

建议下一步编号：

- `094s - Persistent Typed-Array Engine Slice`

目标不是再做 monkey-patch wrapper，而是在一个窄模型上把 `node/state/param/output/transition` arrays 在 engine loop 内持久化，消除 094q 的每步 pack/sync 往返。只有当 094s 在 `pipeline_stage` 上同时满足 rowwise/defined-grid parity 和 wall 不劣于 Python adaptive，才值得扩展到多 row sweep。
