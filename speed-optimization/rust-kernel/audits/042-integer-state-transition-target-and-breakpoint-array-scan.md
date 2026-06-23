# 042 - Integer State, Transition Target IR, And Breakpoint Array Scan

Status: `done`

Date: `2026-06-03`

Code commit: `pending`

Related files:

- `EVAS/evas/simulator/evaluate_ir.py`
- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/simulator/rust_backend.py`
- `EVAS/evas/rust_core/src/lib.rs`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_rust_backend.py`
- `EVAS/tests/test_engine.py`

## One-Line Summary

042 把 integer scalar state 纳入 static-linear Rust IR，记录可 Rust 化的 `transition()` target IR，并新增 Rust array transition-breakpoint scan 原型；这轮主要是 Rust/event queue 迁移的结构前置，不是最终速度 claim。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Static-linear state IR | integer state assignment 被排除，避免漏掉 `_to_integer()` coercion | `LinearOpIR.target_integer` 标记 integer target；Python parity executor 和 Rust kernel 都立即 round 到 Verilog-A integer | 波形应不变 |
| Rust ABI | `EvasRustLinearOp` 只有 target kind/id | 增加 `target_integer` ABI 字段，state write 时在 Rust 里执行 integer coercion | opt-in Rust path 行为对齐 Python |
| Transition target | 只能从 generated Python code 间接看到 target 表达式 | 编译期新增 `_transition_target_ir_ops`，记录可降成 linear/conditional array IR 的 transition target | 不参与默认执行 |
| Truthy condition | IR 只支持 binary comparison 条件 | `q ? a : b` 可表达为 `q != 0`，覆盖真实 transition target 常见形态 | 更宽的 opt-in IR 覆盖 |
| Event queue migration | transition breakpoint 只能逐个 Python `TransitionState.next_breakpoint()` | Rust core 新增 array scan C ABI；model 可选 hook 在 Rust array loop 下调用 scanner，失败回退 Python | 默认语义不变 |

## Principle

这轮解决的是 Rust 化之前的三个“类型/数组边界”问题。

1. **integer state 不能当普通 float state 写。**
   Verilog-A 里 `integer q; q = 1.6;` 不是保存 `1.6`，而是保存整数 `2`。如果 Rust IR 直接把浮点值写进 state array，后续 `transition(q ? 1.0 : 0.0, ...)` 会在边界条件上和 Python/Spectre 语义不一致。

2. **transition target 需要从 generated Python code 里抽出来。**
   真正 event-heavy 模型常写成：

   ```verilog
   V(out) <+ transition(q ? 1.0 : 0.0, 0, tr, tr);
   ```

   如果 target 仍只存在于 Python 表达式字符串中，Rust 不知道该读哪个 state/node，也不知道条件是什么。`_transition_target_ir_ops` 的作用是把 target 变成 `(bias, terms, condition, false_bias, false_terms)` 这种可编号、可数组化的 IR。

3. **event queue 的第一步不是搬整个事件系统，而是搬纯扫描循环。**
   `next_breakpoint()` 里 transition breakpoint 的计算是纯函数：给定 start/target/time/rise/fall/active arrays，返回最早断点。042 先把这个 scan 放进 Rust C ABI，但不改变 transition state 更新、cross/timer ordering 或 event body 执行。

## Before / After Evidence

这轮没有跑新的 top-wall speed rerun，因此没有新增速度结论。

功能验证覆盖如下：

| Check | Result | Meaning |
|---|---:|---|
| Rust core unit tests | `11 passed` | static-linear integer write 和 transition breakpoint array scan 都在 Rust 侧通过 |
| `tests/test_rust_backend.py` | `8 passed` | ctypes ABI 包装可调用 Rust integer/static-linear 和 transition breakpoint scan |
| `tests/test_indexed_backend.py` | `36 passed` | static-linear IR、integer state coercion、transition target IR metadata 通过 |
| `tests/test_engine.py -k 'transition or rust_static_eval or indexed_state'` | `44 passed, 167 deselected` | transition hook、Rust static eval、indexed state 相关路径通过 |
| Engine Rust hook smoke | `rust_transition_breakpoint_scans_total > 0`, fallback `0` | `Simulator.run(... rust_static_eval=True)` 可把 Rust transition breakpoint scanner 接到 model |

Targeted checks:

```bash
cargo test
python3 -m pytest tests/test_rust_backend.py -q
python3 -m pytest tests/test_indexed_backend.py -q
python3 -m pytest tests/test_engine.py -k 'transition or rust_static_eval or indexed_state' -q
```

`cargo fmt` 未运行成功，因为本机 stable toolchain 缺少 `rustfmt` component：

```text
error: 'cargo-fmt' is not installed for the toolchain 'stable-aarch64-apple-darwin'
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- `transition()` state update moved to Rust: `no`
- Rust transition breakpoint scan default-on: `no`; only when Rust backend and array loop already enabled
- Rust scan fallback: `yes`; scanner exception falls back to Python `TransitionState.next_breakpoint()`

Important boundary:

- `_transition_target_ir_ops` is metadata only.
- The Rust breakpoint scanner does not mutate `TransitionState`.
- Timer, cross/above detectors, `$bound_step`, and event bodies still use the existing Python path.

## Learning Notes

### 为什么 integer state 是 Rust 化前置？

Python dict 版本里 `self.state["q"]` 可以保存任何对象，但 Rust array 版本通常会用 `Vec<f64>` 或 typed arrays。只要进入 array，就必须明确每个 slot 的类型规则。integer state 的规则是“写入时立刻转整数”，否则后续条件判断会漂。

### 什么是 transition target IR？

`transition()` 的 target 就是它要平滑到的目标值。例如：

```verilog
transition(q ? 1.0 : 0.0, 0, 1n, 1n)
```

这里 target 是 `q ? 1.0 : 0.0`。IR 会把它记录成：

```text
if q != 0 then 1.0 else 0.0
```

后续 Rust 可以直接读 `q` 的 state id，而不需要执行 Python 表达式。

### 这和 event queue Rust 化有什么关系？

event queue 负责决定下一步仿真应该走到哪个时间点。transition、timer、source breakpoint、cross 都可能要求缩小步长。042 只迁移其中最纯的一部分：active transition 的下一 breakpoint scan。它是后续完整 event queue 迁移的模板。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Rust ABI struct layout mismatch | `test_rust_backend.py` 失败或 Rust static-linear 写错 state | revert `target_integer` ABI field and Rust/Python wrapper changes |
| Integer coercion不一致 | integer state parity test 失败，或 final `state["q"]` 与 Python default 不同 | revert integer state static-linear eligibility |
| Truthy IR 过宽 | 原本不应 lowering 的 ternary 被错误纳入 Rust IR | revert non-binary `_evaluate_ir_condition_expr()` support |
| Rust breakpoint scanner 漏断点 | transition/cross/event tests 出现 waveform 或 dt 变化 | disable `_set_rust_transition_breakpoint_scanner()` install path; Rust ABI 可保留为 prototype |

## Next Step

043 应继续沿着“先 IR/array，后 Rust 执行”的顺序：

1. 统计 top-wall 10/真实 benchmark 中 `_transition_target_ir_ops` 覆盖率，列出不能 lowering 的 target 原因。
2. 把 transition target evaluate 从 metadata 推进到 array executor，但仍先不更新 transition state。
3. 把 timer absolute/periodic states 做成 typed arrays，和 transition breakpoint scan 一起形成 event queue scan batch。
4. 最后再考虑把 transition state update、cross detector 和 event body dispatch 往 Rust 迁移。
