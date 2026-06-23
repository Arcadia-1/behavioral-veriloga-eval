# 034 - Static Lifecycle Fastpath

Status: `done`

Date: `2026-06-03`

Code commit: `4f20ee1` (`EVAS`, branch `codex/evas-spectre-rulefix-20260529`)

Related reports:

- `speed-optimization/rust-kernel/audits/010-post-update-empty-scan-fastpath.md`
- `speed-optimization/rust-kernel/audits/030-segment-lifecycle-fastpath.md`
- `speed-optimization/rust-kernel/audits/033-indexed-state-runtime-storage.md`

## One-Line Summary

把 compiler 已证明“无事件、无 future voltage、无 post-update”的静态模型从每步空生命周期维护里拿出来，默认跳过 `_prepare_step()` 和 absolute timer expire；80-model static chain microbenchmark 从 median `1.314976 s` 降到 `0.885306 s`，约 `1.485x`。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Simulator main loop | 每个 Python model 每步都调用 `_prepare_step()` | 只有需要 event/future/post-update context 的 model 才调用 | 静态模型默认更快，输出不变 |
| Timer lifecycle | 每个 Python model 每步都调用 `_expire_absolute_timers()` | 只有 dynamic breakpoint 或 post-update model 才调用 | 无 timer 的静态模型跳过空扫描 |
| Capability classification | breakpoint/bound_step/post-update 已有局部 prefilter | 复用这些 compiler flags 生成 `model_needs_step_context` 和 `model_needs_timer_expire` | 判断只做一次，不在每步重复推断 |
| Runtime switch | 无法直接对比原生命周期路径 | 新增 `static_lifecycle_fastpath=True`，runner 支持 `evas_static_lifecycle_fastpath=false` / `EVAS_STATIC_LIFECYCLE_FASTPATH=0` | 可 opt-out 做 A/B 和回退 |
| Counters | 只能看 post-update skip | 新增 `model_prepare_step_calls/skips`、`model_timer_expire_calls/skips` | 可量化跳过了多少 model-step |
| Repo hygiene | `cargo test` 后 `evas/rust_core/target/` 未被忽略 | `.gitignore` 增加 `target/` | Rust 构建产物不污染 status |

## Principle

这次属于 **降低每步成本**。

EVAS 主循环每推进一步，会对每个 model 做三类事情：

```text
1. _prepare_step(prev_nv, curr_nv, prev_time, time, future_nv)
2. evaluate(node_voltages, time)
3. _expire_absolute_timers(time) + post_update_events(...)
```

其中 `evaluate()` 是真正计算输出的部分；`_prepare_step()` 和 timer expire 是为了事件语义服务的。

`_prepare_step()` 主要准备这些上下文：

- cross/above event body 需要读取 crossing time 上的节点值；
- last_crossing / interpolation 需要上一步和当前步的端点；
- future voltage nudge 需要 lazy future source voltage；
- post-update event 需要知道本步 event 是否 fired。

如果一个 compiled model 满足：

```text
no cross/above/timer/transition/last_crossing dynamic breakpoint
no future node voltage need
no post-update event
```

那它的每一步并不需要这些上下文。它只需要 `evaluate()`，而 generated `evaluate()` 自己已经会设置：

```python
self._event_time = time
self._bound_step = 0.0
```

所以这类纯静态 model 跳过 `_prepare_step()` 和 `_expire_absolute_timers()` 不会改变输出，只是删掉 Python object/dict/bookkeeping 调用。

## Before / After Evidence

Local microbenchmark shape:

```text
80 consecutive static gain models
source: sine
tstop: 1e-6
tstep/record_step: 1e-9
accepted steps: 6114
model-step count: 489120
```

Same-code A/B, only toggling `static_lifecycle_fastpath`:

| Metric | Before: fastpath off | After: fastpath on | Interpretation |
|---|---:|---:|---|
| median wall | `1.314976 s` | `0.885306 s` | `1.485x` faster |
| best wall | `1.308366 s` | `0.874547 s` | same direction |
| accepted steps | `6114` | `6114` | step count unchanged |
| prepare calls | `489120` | `0` | static model prepare removed |
| prepare skips | `0` | `489120` | all static model-steps skipped |
| timer expire calls | `489120` | `0` | empty timer expire removed |
| timer expire skips | `0` | `489120` | all static model-steps skipped |
| final output | `0.464619804749` | `0.464619804749` | exact same sample value |
| final abs diff | `0` | `0` | no waveform endpoint difference |

Profile-section run:

| Section | Before | After | Interpretation |
|---|---:|---:|---|
| wall with profiling | `1.850992 s` | `1.246061 s` | profiling run also improves |
| `model_prepare_step_s` | `0.412302 s` | `0.000000 s` | prepare cost eliminated |
| `model_post_update_s` | `0.247285 s` | `0.134103 s` | timer/post-update maintenance reduced |
| `model_evaluate_s` | `0.563209 s` | `0.534466 s` | actual evaluate mostly unchanged |
| `dict_prev_snapshot_s` | `0.009329 s` | `0.011261 s` | not the source of this speedup |
| `err_ratio_node_scan_s` | `0.006632 s` | `0.006627 s` | unchanged |
| `record_point_s` | `0.001016 s` | `0.001030 s` | unchanged |

解读：

- 这次不是靠减少步数，也不是靠输出/checker 优化。
- 直接省掉的是每步 `model_count * empty lifecycle` 的 Python 调用和 object 状态维护。
- 在 static-heavy 模型中，这是目前比继续做小型 Rust ABI 准备更有说服力的真实内核收益。

## Functional Safety

- Default backend changed: `yes, pure static compiled models now skip empty lifecycle work by default`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no, event/timer/transition/last_crossing/future/post-update models keep original lifecycle path`
- Fallback path exists: `yes, static_lifecycle_fastpath=False`, `evas_static_lifecycle_fastpath=false`, or `EVAS_STATIC_LIFECYCLE_FASTPATH=0`

Eligibility guard:

```text
needs step context if:
  fastpath disabled
  OR model needs future node voltages
  OR model has dynamic breakpoints
  OR model has post-update events

needs timer expire if:
  fastpath disabled
  OR model has dynamic breakpoints
  OR model has post-update events
```

这意味着下面这些模型不会走 skip：

- `@(cross(...))`
- `@(above(...))`
- `@(timer(...))`
- `transition(...)`
- `last_crossing(...)`
- output-dependent post-update event
- future voltage nudge path

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestCompiledModelCapabilityFlags -q
python3 -m pytest tests/test_engine.py -k 'rust_static_eval or static_branch_fastpath or lifecycle or dynamic_breakpoint' -q
python3 -m pytest -q
cd evas/rust_core && cargo test --release
git diff --check
```

Results:

```text
capability targeted pytest: 3 passed
rust/static/lifecycle filtered pytest: 8 passed, 187 deselected
full pytest: 468 passed in 28.71s
cargo test --release: 3 passed
git diff --check: clean
```

Added regression anchors:

- static contribution model:
  - default fastpath enabled;
  - `model_prepare_step_calls = 0`;
  - `model_prepare_step_skips = steps_total`;
  - `model_timer_expire_calls = 0`;
  - `model_timer_expire_skips = steps_total`;
  - opt-out path gives same output and restores original call counts.
- cross event model:
  - keeps dynamic breakpoint scan;
  - `model_prepare_step_calls = steps_total`;
  - `model_prepare_step_skips = 0`;
  - `model_timer_expire_calls = steps_total`;
  - `model_timer_expire_skips = 0`.

## Learning Notes

### 为什么这次比 032/033 更像“大瓶颈优化”？

032 只优化 dynamic bus node string formatting，只有大量 `V(bus[i])` 的模型才明显受益。

033 是 Rust state ABI 前置，Python 里反而多写 mirror，所以短期变慢是预期。

034 直接命中了主循环每步固定开销：

```text
accepted_steps * number_of_static_models
```

这个乘积一大，哪怕每次只是几个 Python attribute/dict/list 操作，也会变成明显 wall time。

### 什么叫“生命周期维护”？

可以把一个 model 每步要做的事分成两层：

```text
真正计算：
  evaluate()

为了事件正确性准备上下文：
  _prepare_step()
  _expire_absolute_timers()
  post_update_events()
```

对 event 模型来说，第二层非常重要；对纯静态组合模型来说，第二层是空成本。

### 为什么不跳过 `evaluate()`？

因为 `evaluate()` 是模型本身：

```verilog
V(out) <+ gain * V(in) + bias;
```

它必须每步执行，除非后续进一步证明输入没变、表达式可缓存，或者把表达式 lowering 到 Rust/native loop。034 只删掉空壳，不删真正计算。

### 为什么这不等于“EVAS 已经比 Spectre AX 快”？

这只是本地 Python 内核局部 microbenchmark。论文/报告级速度结论仍必须来自：

```text
same vaBench slice
same host / same runner boundary
EVAS/Spectre/AX timing
Spectre-equivalence-gated parity
```

034 可以作为“EVAS 内核有可观优化空间，而且已经有一个可验证收益”的工程证据，不能替代 final speed table。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| eligibility guard 过宽，误跳过 event context | cross/timer/transition/last_crossing regression fail | revert EVAS commit `4f20ee1` or run with `EVAS_STATIC_LIFECYCLE_FASTPATH=0` |
| custom model 错误声明 `_has_dynamic_breakpoints_tree=False` | custom subclass event behavior differs | custom subclass must keep conservative default `True`; compiled models use compiler flags |
| default path变化导致历史 artifact 对不上 | old/new local output differs only when opt-out not matched | rerun with `static_lifecycle_fastpath=False` for direct historical comparison |
| 被误写成 release-wide speed claim | no same-slice Spectre/AX data | cite this audit as microbenchmark only |

## Next Step

下一篇审计建议回到两个更大的方向之一：

- `035-rust-expression-ir.md`：继续扩大 Rust/static evaluator 的可覆盖表达式范围；
- 或新增 profile-driven benchmark audit：在 vaBench 可仿样本上统计 034 后剩余最大 section，到底是 `evaluate()`、output sync、CSV，还是 checker/harness。

我的判断：现在应先做 profile-driven benchmark audit，再决定 035 是否继续 Rust expression IR。因为 034 已经证明“大瓶颈优先”更容易判断路线是否有意义。
