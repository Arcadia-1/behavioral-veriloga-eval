# 103 Event/Transition Shadow Runtime

Status: shadow parity gate, not production speed evidence.

## 这一步改了什么

102 只是把 event/output/transition planner metadata 写进 `CompiledModel` 和 engine perf stats。103 第一次把这个 metadata 真的接进仿真循环：

- 新增 `Simulator.run(..., rust_event_transition_shadow=True)`。
- 对 `event_transition_core` planner candidate 尝试构建 `RustAnalogBlockShadowRuntime`。
- 在 `initial_step` 和每次 `evaluate` 前，复制 Python 当前 node/state/param 到 typed arrays。
- 调用 Rust shadow runtime。
- 再跑原 Python EVAS 路径。
- 比较 Rust shadow 的 node/state 结果与 Python 结果，记录 matches/mismatches/max diff。

默认行为不变：不传 `rust_event_transition_shadow=True` 时不会运行这个 shadow。

## 修改位置

- `EVAS/evas/simulator/backend.py`
  - `CompiledModel._module_ast` 保存原始 parsed module，供 runtime builder 使用。
- `EVAS/evas/simulator/engine.py`
  - 新增 `rust_event_transition_shadow` 参数。
  - 新增 shadow runtime plan 构建、typed-array packing、pre-run、post-compare。
  - 新增 perf stats：
    - `rust_event_transition_shadow_calls_total`
    - `rust_event_transition_shadow_matches_total`
    - `rust_event_transition_shadow_mismatches_total`
    - `rust_event_transition_shadow_errors_total`
    - `rust_event_transition_shadow_value_checks_total`
    - `rust_event_transition_shadow_max_abs_diff`
- `EVAS/tests/test_engine.py`
  - 新增 `test_rust_event_transition_shadow_executes_and_matches_python`。

## 这一步证明了什么

这一步证明 Rust event-transition runtime 已经真实执行在 EVAS 仿真循环里，而不是只存在于 coverage/planner 报告中。

micro smoke：

```text
rust_event_transition_shadow_available      1
rust_event_transition_shadow_enabled        1
rust_event_transition_shadow_models         1
rust_event_transition_shadow_calls_total    3837
rust_event_transition_shadow_matches_total  3837
rust_event_transition_shadow_mismatches_total 0
rust_event_transition_shadow_errors_total   0
rust_event_transition_shadow_value_checks_total 7674
rust_event_transition_shadow_max_abs_diff   0.0
```

## 速度结果怎么理解

同一个 tiny event-transition fixture，5-repeat median：

| mode | median wall |
| --- | ---: |
| Python EVAS baseline | `0.0728 s` |
| Python EVAS + Rust shadow | `0.3292 s` |
| shadow / baseline | `4.52x` slower |

这是预期的：shadow 模式每步同时跑 Python 和 Rust，还要复制 node/state/param arrays，并做 parity compare。它的目标是正确性和 runtime 接入证明，不是加速。

真正的速度实验要等下一步 production gate：

```text
Python evaluate 跳过
Rust event-transition runtime 负责 state update + transition output
engine 同步 node/output/state
再比较 waveform parity
```

## 当前限制

103 使用已有的 `try_build_event_then_transition_shadow_runtime(...)`，比 101 planner 更窄：

- 要求 event statements 在 continuous transition contributions 前。
- event body 必须能编码成当前 body-IR write-set。
- transition contribution 必须是直接 `V(out) <+ transition(...)`。
- dynamic timer、event-after-continuous、多阶段 source order、side-effect boundary 仍未 production 化。

因此 103 是“真实运行的第一条通道”，不是 101 中 `231/348` 全部候选都已经 shadow/production。

## 下一步

1. 增加 shadow coverage report：统计 release 中哪些 planner candidates 也能构建 current shadow runtime。
2. 做 `rust_event_transition_production`，但只对 shadow pass 的模型 opt-in。
3. Production 模式需要显式处理：
   - Python `evaluate` 跳过；
   - Rust state array 同步回 `model.state`；
   - Rust output node 同步到 `model.output_nodes` 和 `node_voltages`；
   - event-fired 标记同步到 engine refine 逻辑；
   - post-update / timer-expire 是否应跳过或拆段。

## 验证

```bash
PYTHONPYCACHEPREFIX=/private/tmp/evas_pycache_103 python3 -m py_compile \
  EVAS/evas/simulator/backend.py \
  EVAS/evas/simulator/engine.py \
  EVAS/evas/simulator/event_transition_plan.py

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  -k "rust_event_transition_shadow or event_transition_plan" -q

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  -k "rust or body_ir or event_due or analog_block or transition_contribution or event_transition_plan" -q
```

结果：

- Targeted tests: `2 passed, 246 deselected`。
- Broader Rust/094 subset: `49 passed, 199 deselected`。
