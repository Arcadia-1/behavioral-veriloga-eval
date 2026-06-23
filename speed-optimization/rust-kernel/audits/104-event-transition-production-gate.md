# 104 Event/Transition Production Gate

Status: opt-in production semantics, correct on smoke, not speed-positive yet.

## 这一步改了什么

103 的 `rust_event_transition_shadow` 仍然同时跑 Rust 和 Python，只做 parity 检查。104 新增真正的 production gate：

- 新增 `Simulator.run(..., rust_event_transition_production=True)`。
- 对当前能构建 `RustAnalogBlockShadowRuntime` 的 event-then-transition 模型，跳过 Python `model.evaluate(...)`。
- Rust runtime 负责：
  - event due 检查；
  - event body state update；
  - continuous `transition()` output；
  - transition breakpoint；
  - `_step_event_fired` 同步。
- engine 负责把 Rust typed arrays 同步回：
  - `model.state`；
  - indexed state sidecar；
  - `model.output_nodes`；
  - 全局 `node_voltages`。

默认行为不变：不传 `rust_event_transition_production=True` 时仍然走 Python EVAS。

## 保守 gate

这一步没有把 101/102 里的所有 planner candidate 都直接生产化。为了避免错误 claim，104 production 只允许更窄的一类模型：

- analog block source order 是 event statements 后接 direct transition contributions；
- event body 能编码成当前 Rust body IR；
- transition contribution 是直接 `V(out) <+ transition(...)`；
- event body 不读取 voltage；
- event due 不包含 `timer()`；
- 顶层模型，无 child model；
- event trace audit 未开启。

原因是当前 runtime 还没有完整接管 crossing-time voltage read、timer queue breakpoint、child model order、event trace side effect。遇到这些行为时仍应 fallback 到 Python。

## 修复的问题

第一次接入时暴露了一个关键 bug：production 请求时虽然关闭了 shadow flag，但 shadow pre-run 函数只看 plan，不看 flag，导致每步 production 前仍然偷偷跑一次 Rust shadow。结果 cross detector 状态被提前推进，production 自己再跑时事件已经被消费掉。

修复后：

- `rust_event_transition_shadow=False` 时 shadow pre-run 直接返回；
- production 和 shadow 不再共享同一步的 runtime side effect；
- event fire/state/output 与 Python baseline 对齐。

## Smoke 结果

fixture:

```verilog
@(initial_step) state = 0.0;
@(cross(V(clk)-0.5, +1)) state = 1.0;
V(out) <+ transition(state, 0.0, 1n, 1n);
```

Python EVAS baseline 与 Rust production：

- time grid 完全一致；
- `OUT` waveform 一致；
- final `state` 一致；
- fallback 为 0。

production counters:

```text
rust_event_transition_production_models                 1
rust_event_transition_production_calls_total            3836
rust_event_transition_production_executed_total         3836
rust_event_transition_production_fallbacks_total        0
rust_event_transition_production_state_writes_total     3836
rust_event_transition_production_output_writes_total    3836
rust_event_transition_production_fired_events_total     2
rust_event_transition_production_breakpoint_scans_total 3835
rust_event_transition_production_breakpoint_clamps_total 4
```

## 速度结果怎么理解

同一 tiny fixture，5-repeat median：

| mode | median wall |
| --- | ---: |
| Python EVAS baseline | `0.0906 s` |
| Rust event-transition production | `0.3157 s` |
| production / baseline | `3.49x` slower |

这不是最终 Rust 化失败的证明，而是说明 104 仍然是“Python 外层 loop + Rust primitive 调用”的中间态：

- 每步仍由 Python engine 调度；
- 每步仍要刷新 node/state arrays；
- event due、body IR、transition 分别通过 Rust primitive/FFI 调用；
- record、err-ratio、source update、post-update 仍在 Python。

因此 104 证明了“能跳过 Python evaluate 并保持正确”，但还没有证明“Rust 路径更快”。要出现速度收益，需要把多次 per-step FFI primitive 合成一个 whole-segment Rust batch，或者更进一步把时间推进、event queue、record 一起搬进 Rust。

## 验证

```bash
PYTHONPYCACHEPREFIX=/private/tmp/evas_pycache_104 python3 -m py_compile \
  evas/simulator/engine.py tests/test_engine.py

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  -k "rust_event_transition_production or rust_event_transition_shadow or event_transition_plan" -q

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  -k "rust or body_ir or event_due or analog_block or transition_contribution or event_transition_plan" -q
```

结果：

- Targeted tests: `3 passed, 246 deselected`。
- Broader Rust/event/body-IR subset: `50 passed, 199 deselected`。

## 下一步

104 后的主线不应继续做零散 Python 小修。下一步应该把当前 production 的多个 Rust primitive 合并成一个 compiler-driven whole-segment Rust call：

```text
pack once -> Rust event due -> Rust event body -> Rust transition -> Rust breakpoint -> sync once
```

再往后才是 release-wide production coverage 和真实 top-wall benchmark speed rerun。
