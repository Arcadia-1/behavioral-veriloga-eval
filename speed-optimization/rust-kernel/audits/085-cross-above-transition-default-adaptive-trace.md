# 085 - Cross/Above Interpolation, Transition Production, And Default Adaptive Trace

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `behavioral-veriloga-eval/speed-optimization/rust-kernel/behavior-coverage-map.v1.json`

## One-Line Summary

这一轮把三个此前卡在 fallback 的小闭环补上：`cross()/above()` event-time node interpolation 进入 Rust typed-array primitive，`transition()` state evolution 接入 opt-in production path，timer static-linear whole-segment Rust fastpath 支持默认 `record_step=None` trace。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `cross()/above()` event body node read | `_get_voltage()` 在 event context 里逐 node 用 Python dict 做 crossing-time interpolation | `rust_event_interpolation=True` 时预先把 trigger expression 的 interpolation node set 批量送入 `evas_rust_interpolate_event_values()`；event body 读取这些节点时由 `_get_voltage()` 命中 cache | 默认不变；opt-in parity path waveform 一致 |
| `transition()` state evolution | Rust primitive 已有 shadow/parity，但 `_transition()` production 仍走 Python `TransitionState` | `rust_transition_production=True` 时 `_transition()` 可用 `evas_rust_transition_state_step()` 更新 typed state，再写回 Python state object | 默认不变；opt-in production waveform 一致 |
| timer static-linear whole segment trace | 082/084 要求显式 `record_step`，否则 default internal/adaptive points fallback Python | `record_step is None` 时 engine 复现受限 timer-linear模型的默认 internal/adaptive time grid，再交给 Rust trace ABI 执行 event/evaluate/record | 默认不变；opt-in whole-segment fastpath 与默认 trace 点一致 |
| event-linear write production dependency | event body 读 node 且处于 event interpolation context 时保守 fallback | `rust_event_write_production/shadow` 自动安装 interpolation backend；只有 event body 读取 trigger/interpolation cache 中的 node 时才临时 patch Rust node array，否则继续 fallback | 默认不变；避免跨节点采样误用 current-step value |

## Principle

这轮分别处理三类开销/语义缺口：

- **降低每步成本**：`cross()/above()` event body 里读取多个节点时，不再每次都从 Python dict/object 逐个做 `(v_prev, v_cur, t_event)` 插值，而是先批量计算 event-time values。
- **降低 transition 调用成本**：`transition()` 内部状态从 Python object 方法调用推进到 Rust typed-array step。当前仍是 per-call production，不是 batch，所以更重要的是打通正确性闭环。
- **减少 fallback 步数限制**：timer static-linear whole-segment fastpath 不再被显式 `record_step` 卡住。默认 trace 下 EVAS 会在 timer fire 后缩小 internal step，再逐渐放大；这一轮复现这个受限 scheduler，避免无 record grid 时回退 Python。

直观理解：

```text
old cross/above event body:
  event fires -> Python event body -> V(trigger node) computes interpolation in Python

new opt-in path:
  event fires -> Rust computes trigger-node event-time values once -> Python event body reads cache for those nodes
```

```text
old default trace:
  no record_step -> Python adaptive/internal loop

new restricted Rust path:
  no record_step -> Python generates the same restricted time grid -> Rust owns timer event/evaluate/record over that grid
```

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| `cross()/above()` cache batches | 0 | targeted tests show `rust_event_interpolation_batches_total > 0` | event-time node values are actually going through the Rust ABI |
| `cross()/above()` cache hits | 0 | targeted tests show `rust_event_interpolation_cache_hits_total > 0` | event body node reads are consuming cached interpolation values |
| transition production calls | 0 | targeted tests show `rust_transition_state_production_calls_total > 0` | `_transition()` production path can call Rust typed-array state step |
| default timer trace points | Python-only fallback | Rust fastpath reports `rust_full_model_timer_static_linear_default_trace_enabled == 1` | `record_step=None` no longer automatically blocks this restricted fastpath |
| speed claim | not allowed | not added | 这一轮是 correctness/coverage wiring，不是 same-slice speed claim |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

这轮所有新路径仍是 opt-in：

| Flag / API | Scope |
|---|---|
| `rust_event_interpolation=True` | 只影响 event context 中已由 compiler 从 `cross()/above()` trigger expression 收集到的 node reads；body 读其他 node 仍走 Python 插值 |
| `rust_event_write_production=True` / `rust_event_write_shadow=True` | 自动安装同一个 interpolation backend，供 event-linear write batch 在安全同节点 cache case 下使用 |
| `rust_transition_production=True` | 只影响 `_transition()` state evolution，失败时回退 Python |
| `rust_full_model_fastpath=True` | 只影响命中 timer static-linear whole-segment gate 的模型 |

## Important Boundaries

这轮仍然不能 claim 全量 Rust 化：

| Behavior | Current state |
|---|---|
| full `cross()/above()` event queue | detector/order/body dispatch 仍由 Python 拥有；Rust 只负责 event-time interpolation cache |
| general event body | 简单 state assignment 有 Rust batch，复杂 body、side effect、dynamic array 仍 fallback |
| `transition()` batch | 当前是 per-call typed-array production，不是 whole-segment transition queue |
| global adaptive solver | 只覆盖 timer static-linear whole-segment 的默认 trace time-grid；一般 err-ratio/adaptive/bound-step/cross refinement 仍由 Python 拥有 |
| release-wide speed | 没有重跑 same-server same-slice EVAS/Spectre/AX timing，不能更新 paper-facing speed claim |

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m py_compile EVAS/evas/simulator/backend.py EVAS/evas/simulator/engine.py EVAS/evas/simulator/rust_backend.py
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -k 'rust_event_interpolation or rust_transition_production or timer_static_linear_default_trace or timer_static_linear_trace_matches_default or multi_timer_static_linear_queue' -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_rust_backend.py -k 'interpolates_event_values or max_err_ratio or records_values_for_node_ids or timer_static_linear_queue' -q
cargo test --manifest-path EVAS/evas/rust_core/Cargo.toml --release interpolates_event_values_with_clamped_time_fraction
cargo test --manifest-path EVAS/evas/rust_core/Cargo.toml --release
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_rust_backend.py -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -q
PYTHONPATH=EVAS python3 -m pytest EVAS/tests -q
python3 -m json.tool behavioral-veriloga-eval/speed-optimization/rust-kernel/behavior-coverage-map.v1.json
git -C EVAS diff --check
git -C behavioral-veriloga-eval diff --check
```

Results:

```text
py_compile: pass
engine targeted: 6 passed, 237 deselected
rust_backend targeted: 4 passed, 30 deselected
rust core targeted: 1 passed, 31 filtered out
rust core full: 32 passed
rust_backend full: 34 passed
engine full: 243 passed
EVAS full: 568 passed
behavior coverage JSON: valid
diff --check: pass for EVAS and behavioral-veriloga-eval
```

## Learning Notes

**event-time interpolation**：`cross()` 事件不是一定发生在当前步终点，而是在上一步和当前步之间的某个 crossing time。event body 里如果读 `V(in)`，应该读 crossing time 上的插值，不应该读当前步终点值。

**typed array production**：Python 的 `TransitionState` 是 object；Rust primitive 要的是一组连续数组，比如 `target[]/start[]/rise[]/fall[]`。typed array 的好处是 CPU 可以顺序读写，避免 Python method dispatch 和 dict lookup。

**default adaptive trace**：没有 `record_step` 时，EVAS 不只是每 `tstep` 输出一次。timer 或 breakpoint 后会插入 internal points，并临时缩小步长。Rust whole-segment path 必须复现这些点，否则 waveform 时间轴就和默认 Python 不一致。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| event body 误用 cached value | `cross()/above()` body read parity test fails, or cache hit appears outside event node set | revert `_cache_event_interpolated_values()` / `_get_voltage()` event cache branch in `EVAS/evas/simulator/backend.py` |
| transition state writeback mismatch | `rust_transition_state_production_fallbacks_total > 0` or waveform parity fails | disable `rust_transition_production` or revert `_transition_rust_production()` |
| default adaptive trace point mismatch | timer default-trace regression produces different `time` array | revert `_whole_segment_timer_adaptive_times()` use in `_try_timer_static_linear_fastpath()` |

## Next Step

- `086 - Event Queue And Transition Batch Ownership`: 把 detector due、event body、transition state/output、record 继续合成更大的 Rust/array segment，而不是停留在 per-call primitive。
