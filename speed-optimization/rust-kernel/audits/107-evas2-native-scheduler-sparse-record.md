# 107 - EVAS2 Native Scheduler And Sparse Record

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `audits/106-evas2-event-transition-core-strict-production.md`
- `RUST_NEGATIVE_ATTEMPT_STOPLIST_20260605.md`
- `EVAS2_WHOLE_SEGMENT_COVERAGE_PLAN_20260605.md`

## One-Line Summary

把 106 的受限 `pulse -> cross -> scalar state -> transition(out)` core 从 Python per-point loop 推进到单次 Rust trace ABI：Rust 内部完成 scheduler、transition breakpoint、event body 和 sparse output record。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Scheduler | 106 由 Python 构造 time grid，并逐点调用 Rust runtime | 新增 `evas_rust_event_transition_core_trace_pulse`，Rust 内部推进 planned/source/transition breakpoint | EVAS2 strict 命中 W1b 时不再每个点回 Python |
| Record | Python 每个 emitted point append `time` 和 `OUT` list | Rust 一次性填充 `time_values` 和 recorded output buffer | 只返回 checker/record 需要的输出信号，不返回全量 node/state snapshot |
| Engine gate | 106 命中 `event_transition_core` 后直接进入 Python loop | 先尝试 native trace；不匹配再回 106 strict core | `profile_fast_rust_55` 不变；EVAS2 覆盖更深 |
| Scope | 支持 event+transition core 的 Python-loop strict production | 仅支持一个 `pulse()` source、一个 `cross(V(src)-threshold,+dir)`、一个 scalar state、一个 direct `transition(state, const delay/rise/fall)` output | 不能声明全量 event-transition native scheduler |

## Principle

这一步同时减少三类开销：

- **减少 FFI 次数**：106 是每个 emitted point 调一次 Rust runtime；107 是整段 trace 一次 Rust FFI。
- **减少 Python scheduler 开销**：transition breakpoint 查询和插入在 Rust loop 内完成，不再由 Python `while runtime.next_breakpoint(...)` 驱动。
- **减少 record 开销**：Rust 只写 `time` 和一个 recorded output buffer，不维护 Python per-point `columns[name].append(...)`。

这正是之前 104 负优化暴露的问题：局部 Rust 很快，但如果每步仍被 Python 调度、打包、同步，整体会变慢。107 的收益来自把“行为核心 + 时间推进 + 记录”合成一个粗粒度 Rust batch。

## Before / After Evidence

Microbench fixture:

```verilog
@(initial_step) state = 0.0;
@(cross(V(clk)-0.5, +1)) state = 1.0;
V(out) <+ transition(state, 0.0, 1n, 1n);
```

Run setting: `tstop=1e-6`, `tstep=1e-9`, `record_step=250e-12`, 12 repeats in one Python process, median wall reported.

| Mode | Median wall (s) | Points | Speedup vs Python default | Interpretation |
|---|---:|---:|---:|---|
| Python default EVAS | `0.505092` | `6542` | `1.00x` | Baseline Python engine |
| 104 per-step Rust production | `2.114228` | `6505` | `0.24x` | Negative example: local Rust but per-step FFI/sync dominates |
| 106 strict Python-loop core | `0.389472` | `6505` | `1.30x` | Rust owns event/body/transition, Python still owns scheduler/record |
| 107 native scheduler+record | `0.007946` | `6505` | `63.57x` | One Rust trace ABI owns scheduler + sparse record |

Additional comparison:

| Comparison | Result | Meaning |
|---|---:|---|
| 107 vs 106 median wall | `~49.02x` faster | Native scheduler/record removes Python per-point loop |
| 107 vs 106 `max_time_delta` | `0.0` | Same emitted time grid as 106 |
| 107 vs 106 `max_out_delta` | `0.0` | Same output waveform as 106 |
| 107 native counter | `1` | Native path actually executed |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `strict EVAS2 no for whole-model miss; W1b miss falls back to 106 strict core before final unsupported`

## Validation

Commands run:

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/rust_core
cargo build --release
cargo test --release event_transition_core_trace -- --nocapture

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
PYTHONPYCACHEPREFIX=/private/tmp/evas_pycache_107 python3 -m py_compile evas/simulator/engine.py evas/simulator/rust_backend.py tests/test_engine.py
PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest tests/test_engine.py -k "evas2_event_transition_core or rust_event_transition_production or rust_full_model_required" -q
PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest tests/test_audit_094o_analog_block_runtime.py tests/test_engine.py -k "event_transition_core or event_transition_production or rust_full_model_required or analog_block_runtime" -q
```

Results:

```text
cargo build --release: pass
cargo test --release event_transition_core_trace: 0 selected, build pass
py_compile: pass
3 passed, 248 deselected
4 passed, 248 deselected
```

## Learning Notes

**native scheduler** 在这里不是简单“用 Rust 算 event body”。它的关键是 Rust 自己决定下一个时间点：普通 record grid、source breakpoint、transition breakpoint 都在同一个 Rust loop 里合并，然后按顺序执行 event 和 transition。

**sparse record** 是只记录需要返回的信号。当前 W1b 只记录一个 output buffer，不把所有 node/state 在每个时间点都拷回 Python。这就是为什么它能比 106 快很多：106 每个点仍在 Python append 和 FFI，107 是 Rust 连续写数组。

**为什么 104 变慢、107 变快？** 104 每一步都要 Python -> Rust -> Python，单步工作太小，FFI 和同步开销比计算本身还大。107 把几千个点合成一次调用，Rust 在内部循环，才真正吃到 native loop 的收益。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| W1b 被误读为全量 native scheduler | gate 只接受 pulse/cross/scalar-state/direct-transition 单输出 | 保留 106 fallback，并在 claim 中限定为 W1b |
| 真实 benchmark 不命中 W1b | native counter 为 0，仍回 106 或 unsupported | 下一步扩展 source metadata、event body constants、multi-output sparse record |
| microbench 速度被过度外推 | release-wide runner 尚未跑 W1b coverage/speed | 先做 coverage manifest，再做真实 row speed rerun |

## Next Step

下一篇审计文档编号和预期主题：

- `108 - EVAS2 Native Trace Coverage Sweep`
