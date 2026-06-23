# 094o - Combined Analog-Block Shadow Runtime

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS/evas/simulator/analog_block_runtime.py`
- `EVAS/tests/test_audit_094o_analog_block_runtime.py`
- `behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094n-transition-contribution-runtime.md`

## One-Line Summary

把 094m 的 event runtime 和 094n 的 transition runtime 组合成受限 analog-block shadow runtime，验证 `pipeline_stage` 的事件状态更新和输出 transition 可以串联执行。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Runtime composition | event body 和 transition output 分开测试 | 新增 `RustAnalogBlockShadowRuntime` 顺序执行 event runtime，再执行 transition runtime | unchanged |
| Runtime-owned breakpoint | 调用者需要摸 transition runtime 才能查 ramp breakpoint | `RustAnalogBlockShadowRuntime.next_breakpoint()` 统一代理 transition breakpoint | unchanged |
| Source-shape gate | 没有 analog-block 级别的保守入口 | 新增 `try_build_event_then_transition_shadow_runtime()`，只接受事件在前、transition contribution 在后的 analog block | unchanged |
| Real benchmark coverage | `pipeline_stage` 事件和输出分别验证 | `initial_step -> PHI1 -> PHI2 -> transition settle` 在同一 runtime 内验证 | unchanged |

## Principle

这一步把 094 的三个关键子块接成一个 shadow pipeline：

```text
Rust event due
  -> Rust event body batch
  -> Rust transition target expression batch
  -> Rust transition state step
  -> node array output write
```

它仍然不是完整仿真器，因为 adaptive step、breakpoint queue、record/CSV、checker、source waveform 更新仍由外层 Python harness 负责。但它已经证明：对 `pipeline_stage` 这种真实模型，核心 analog block 的事件状态和 transition 输出可以放进同一个 Rust shadow runtime。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| New 094o combined runtime test | n/a | 1 pass | `pipeline_stage` event + transition sequence 可串联 |
| 094 full targeted pytest + Rust ABI | 66 pass after 094n | 68 pass | 新组合层和 breakpoint API 没有破坏既有 094 测试 |
| Production wall speed | unchanged | unchanged | 仍未接 `engine.py`，不声明提速 |
| Supported source shape | event-only / transition-only | event-then-transition analog block | 覆盖面推进，但仍有 source-order 限制 |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094o_analog_block_runtime.py -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094a_expr_ir.py EVAS/tests/test_audit_094b_stmt_schedule_ir.py EVAS/tests/test_audit_094d_state_binding_ir.py EVAS/tests/test_audit_094f_body_ir_encoder.py EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_audit_094n_transition_runtime.py EVAS/tests/test_audit_094o_analog_block_runtime.py EVAS/tests/test_rust_backend.py -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/evas/simulator/stmt_ir.py EVAS/evas/simulator/event_due_runtime.py EVAS/evas/simulator/transition_runtime.py EVAS/evas/simulator/analog_block_runtime.py EVAS/tests/test_audit_094f_body_ir_encoder.py EVAS/tests/test_audit_094h_event_due_program.py EVAS/tests/test_audit_094n_transition_runtime.py EVAS/tests/test_audit_094o_analog_block_runtime.py
git diff --check -- evas/simulator/analog_block_runtime.py evas/simulator/event_due_runtime.py evas/simulator/stmt_ir.py evas/simulator/transition_runtime.py tests/test_audit_094f_body_ir_encoder.py tests/test_audit_094h_event_due_program.py tests/test_audit_094n_transition_runtime.py tests/test_audit_094o_analog_block_runtime.py
```

Results:

```text
1 passed in 0.55s
68 passed in 12.76s
py_compile: pass
git diff --check: pass
```

## Learning Notes

这里的 “combined” 不是说 EVAS 已经全量 Rust 化，而是说一个真实 analog block 的核心局部闭环已经能在 Rust shadow runtime 里走通：

1. 事件判断：PHI1/PHI2 是否过阈值。
2. 事件体：更新 `vin_s`、`vres_level`、`d1_level`、`d0_level`。
3. 连续输出：把状态变量通过 `transition()` 变成 VRES/D1/D0 输出节点。

真正 E2E 加速还差外层调度和数据路径。只要每一步仍由 Python 负责 source 更新、adaptive step、CSV 记录和 dict sync，Rust 子块即使很快，也可能被外层开销盖住。

094s 前补充了 `next_breakpoint()` 代理，这是让外层 engine slice 不依赖内部 transition runtime 字段的最小 contract。它仍不代表 production dispatch，只是把 runtime-owned transition breakpoint 暴露为稳定 API。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| source-order gate 太窄，不能覆盖贡献语句在事件前或事件/贡献交错的模型 | builder 返回 `None` | 后续做 source-order statement interpreter，而不是放宽当前 gate |
| 组合 runtime 被误接 production | E2E parity/speed 未过却默认启用 | 保持 shadow-only；接 `engine.py` 前必须做 real-row CSV sweep |
| transition settle 时间点依赖 adaptive scheduler，单元测试不代表完整 waveform parity | round-trip CSV sweep 出现差异 | 暂不接 production，补 scheduler/breakpoint gate |

## Next Step

下一篇审计文档编号和预期主题：

- `094p - Real-Row CSV Shadow Sweep Gate`
