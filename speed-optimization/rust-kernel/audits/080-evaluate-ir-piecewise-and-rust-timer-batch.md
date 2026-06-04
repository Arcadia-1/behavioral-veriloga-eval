# 080 Evaluate IR Piecewise Lowering And Rust Timer Batch

## 核心结论

这一轮把两类之前“有 primitive / 有影子验证，但没有进入通用生产路径”的内容往前推进：

- `evaluate` IR 不再只覆盖严格线性表达式；`abs(x)`、`min(a,b)`、`max(a,b)` 这类可证明等价的 piecewise-linear 表达式会被 lowering 成条件线性选择，并复用现有 Rust static-linear ABI。
- 连续 static `timer(...)` event segment 的 due-mask 计算现在会在 `rust_timer_event=True` 时优先走 Rust array primitive；event body 仍按生成的 Python 源码顺序执行，保证事件顺序不变。

这不是全量 Rust 化完成。`cross()` / `above()` 的 Rust detector primitive 已存在且有 parity tests，但真实 production hot path 仍需要 compiler/event-queue 级批处理；仅把单个 `_check_cross/_check_above` 替换成 per-event FFI 会重复 059 中的 timer 问题：Python 表达式求值和 FFI 打包开销会吞掉核心收益。

## 改造原理

### `abs/min/max` 为什么能进入 static-linear ABI

现有 Rust static-linear ABI 支持：

```text
target = condition ? (bias + sum(gain_i * source_i)) : (false_bias + sum(false_gain_i * source_i))
```

因此这些函数可以写成等价条件选择：

```text
abs(x)      = (x >= 0) ? x : -x
min(a, b)  = (a <= b) ? a : b
max(a, b)  = (a >= b) ? a : b
```

如果 `x/a/b` 本身都是静态线性表达式，也就是只读参数、静态节点、静态 state slot 和固定下标 state array，那么它们不需要新增 Rust op，就可以被编码进现有 `RustLinearOp`。

### timer batch 为什么比 per-event Rust 更合理

之前 051/059 已经证明 Rust timer primitive 正确，但 per-check production 会慢，原因是每个 timer 事件都要：

```text
Python expression/value -> tiny array packing -> FFI -> tiny array unpacking -> Python event body
```

080 改成连续 timer segment 一次性打包 N 个 timer due check：

```text
Python generated evaluate
  -> _check_timer_event_batch(specs, time)
  -> Rust timer_periodic_step / timer_absolute_step on arrays
  -> Python 按原源码顺序执行 event body
```

这样减少的是每步 timer due 判断的 Python 分支和小 FFI 次数，但不改变 event body、reschedule 顺序、CSV schema 或 checker contract。

## 改动内容

- `EVAS/evas/simulator/backend.py`
  - 新增 `_evaluate_ir_piecewise_function_expr()`，支持 `abs/min/max` lowering。
  - 新增条件线性表达式的加法、取负和缩放 helper，使 `vcm + abs(V(vin)-vcm)` 这类真实常见表达式可以进入 IR。
  - 新增 `_rust_timer_event_batch_production()`，在 `rust_timer_event=True` 且 batch size 足够时用 Rust array primitive 计算 grouped timer due mask。
  - timer batch Rust path 只在 timer state 值变化时写回 dict，避免额外 invalidation。
- `EVAS/evas/simulator/evaluate_ir.py`
  - 更新模块说明，明确支持 piecewise-linear function lowering，但一般非线性函数和 event operator 仍 fallback。
- `EVAS/tests/test_indexed_backend.py`
  - 新增 `abs()` 和 `min/max` lowering/parity tests。
- `EVAS/tests/test_engine.py`
  - 新增 timer batch Rust production E2E parity test。
  - 新增 `abs/min/max` piecewise IR 在 `rust_static_eval=True` 下实际执行的 E2E parity test。

## 验证结果

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_indexed_backend.py -k "abs_as_conditional or min_max_state_pipeline or ternary" -q
4 passed, 37 deselected

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -k "timer_event_batch_uses_rust_production or installs_rust_timer_breakpoint_scanner or rust_timer_event_path_matches" -q
3 passed, 229 deselected

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -k "piecewise_abs_min_max or timer_event_batch_uses_rust_production" -q
2 passed, 231 deselected

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_indexed_backend.py -q
41 passed

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_rust_backend.py -q
31 passed

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -k "rust_static_eval or timer or cross or above" -q
84 passed, 149 deselected
```

## 速度影响判断

本轮是全局生产路径补齐，不单独作为速度 claim：

- `abs/min/max` 的收益取决于真实 row 是否因此从 Python evaluate fallback 变成 Rust static-linear segment；如果只有少数小模型命中，仍可能被 FFI/sync 开销抵消。
- timer batch Rust path 只有连续 static timer segment 命中；动态 `timer(next_t)`、cross/above event body、transition/state machine 仍需要后续 event queue / whole-segment lowering。

下一步应重跑 coverage/top-wall profile，看 `rust_static_eval_no_candidate_expr_function_abs/min/max` 是否下降，以及 timer batch Rust counters 是否在真实 benchmark 中非零。

## 仍未完成

| 项目 | 当前状态 | 为什么不能 claim 完成 |
|---|---|---|
| evaluate 全量 IR 化 | 增加了 piecewise-linear `abs/min/max`，但一般函数、动态数组、event body、自依赖状态更新仍 fallback | 需要 expression IR / statement IR / event-body IR 三层统一，而不是只扩展 static-linear tuple |
| `cross()` Rust production | Rust detector primitive 和 shadow 已有 | production 还要把触发表达式求值、crossing interpolation、event body write-set、refine trigger 放进同一个 batch |
| `above()` Rust production | Rust detector primitive 和 shadow 已有 | 同 `cross()`，只换 detector 会保留 Python 表达式求值和 per-event FFI |
| dynamic `timer(next_t)` | state-owned fast path 已有，static timer batch 已进 Rust production | 仍需把 state-owned target read、due check、body state update 和 reschedule 合成 typed-array/event batch |

## 下一步

1. 用 release/top-wall coverage manifest 重新统计新增 piecewise lowering 的命中率。
2. 对最高频 `cross/above` event-body 建立 compiler event-due batch IR：先 shadow parity，再 production。
3. 对 `timer(next_t)` 建立 state-owned timer batch IR：target state array read + due mask + body write-set + reschedule typed arrays。
4. 如果 batch 覆盖仍低，再推进 general statement/evaluate IR，而不是继续补单个 Python helper。
