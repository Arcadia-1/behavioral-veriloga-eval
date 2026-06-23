# 106 - EVAS2 Event Transition Core Strict Production

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `EVAS2_WHOLE_SEGMENT_COVERAGE_PLAN_20260605.md`
- `RUST_NEGATIVE_ATTEMPT_STOPLIST_20260605.md`
- `audits/101-event-transition-source-order-planner.md`
- `audits/103-event-transition-shadow-runtime.md`
- `audits/104-event-transition-production-gate.md`
- `audits/105-evas2-strict-rust-engine.md`

## One-Line Summary

把受限的 `event + transition()` core segment 接进 EVAS2 strict full-model dispatcher：命中时由 Rust typed-array runtime 负责 event due/body、transition output、breakpoint 和 trace，未命中时保持 strict unsupported，不允许 Python evaluate fallback。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Engine dispatch | `rust_event_transition_production` 只能挂在 Python engine 每步 evaluate 内，104 已证明 per-step FFI/sync 会变慢 | 新增 `_try_event_transition_ordered_segment_fastpath()`，只在 `rust_full_model_required=True` 时进入 full-model dispatcher | EVAS1.0 / `profile_fast_rust_55` 不变；EVAS2 strict 覆盖率开始有 event+transition core production 入口 |
| Scheduler | Python engine 仍拥有 source/model breakpoint、record 和 outer loop | W1a path 自己构造 record/source-breakpoint grid，并用 Rust transition runtime 插入 transition breakpoint | 支持 direct `transition()` output 的受限 smoke；尚不是最终全 native scheduler |
| Event body | Python `model.evaluate()` 执行 event body | Rust analog-block runtime 执行 event due + body batch，并同步 scalar state | 命中路径不再调用 Python model evaluate hot path |
| Safety gate | production gate 可 fallback 到 Python | EVAS2 strict 模式下必须命中 whole-segment runtime，否则抛 unsupported | Rust 覆盖率不会被 Python fallback 污染 |

## Principle

这一步属于 **降低每步成本** 和 **减少 Python 解释器热路径** 的中间阶段。

直观理解：EVAS1.0 是 Python engine 每个时间点调用一次 `model.evaluate()`；104 的问题是虽然 event/body/transition 小块能进 Rust，但每步仍要在 Python 和 Rust 之间来回打包、同步，因此变慢。106 把这一整段搬到 full-model dispatcher：一旦匹配，就让同一个 Rust typed-array runtime 持有 node/state/transition 状态，Python 只负责外层 trace list 和最终 `SimResult`。

这还不是最终形态。最终 EVAS2 应该继续把 record/CSV/scheduler 也 native 化，避免每个 emitted point 都回 Python 一次。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| EVAS subprocess wall | N/A | N/A | 本轮是 strict production correctness gate，不做速度 claim |
| accepted points | Python scheduler-owned | Rust path smoke 24 emitted points | W1a 能生成完整 event+transition trace |
| per-step cost | N/A | N/A | 尚未做 release wall rerun；不能声明加速 |
| checker/result parity | 104 production smoke exact waveform but Python outer loop-owned | 106 strict full-model smoke passes; max time-grid delta `<1e-13s` and output delta explained by 1ns transition slope | 语义正确；trace scheduler 有几十飞秒级 drift，属于当前 W1a 限制 |

关键测试计数：

| Counter | Expected | Meaning |
|---|---:|---|
| `rust_full_model_required_failures` | `0` | strict EVAS2 path 没有 fallback 失败 |
| `rust_full_model_event_transition_core_rust_enabled` | `1` | 命中新的 Rust full-model event-transition core |
| `rust_full_model_event_transition_core_calls_total` | `>0` | trace 点由 Rust runtime step 产生 |
| `rust_full_model_event_transition_core_fired_events` | `>0` | event due/body 在 Rust path 执行 |
| `rust_event_transition_production_requested` | `0` | 没有使用 104 的 per-step production gate |
| `generic_executor_runs` | `0` | 没有退回 091d Python-body generic executor |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `strict EVAS2 no; EVAS1.0 yes`

## Validation

Commands run:

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
PYTHONPYCACHEPREFIX=/private/tmp/evas_pycache_106 python3 -m py_compile evas/simulator/engine.py tests/test_engine.py
PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest tests/test_engine.py -k "evas2_event_transition_core or rust_event_transition_production or rust_full_model_required" -q
PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest tests/test_audit_094o_analog_block_runtime.py tests/test_engine.py -k "event_transition_core or event_transition_production or rust_full_model_required or analog_block_runtime" -q
```

Results:

```text
py_compile: pass
3 passed, 248 deselected
4 passed, 248 deselected
```

## Learning Notes

**strict production** 的意思不是“结果永远比 Python 更精确”，而是“这段行为由 Rust 生产结果，不允许偷偷退回 Python”。所以它关注的是 ownership：event due、event body、transition state、output write 和必要 breakpoint 是否都归 Rust runtime 管。

**为什么仍会有几十飞秒 drift？** 默认 Python engine 有自己的 adaptive step 历史；新 W1a strict path 自己构造 time grid。两者在 1ns transition 斜坡上相差 `~8e-14s` 时，输出自然会相差 `~8e-5`，因为斜率约为 `1 / 1ns`。测试里显式要求输出误差必须能由时间漂移解释，避免把 scheduler drift 误判成 event/body 语义错误。

**为什么不复用 104？** 104 是每步 production gate，仍在 Python outer loop 里频繁 FFI/sync，micro smoke 正确但更慢。106 只从 full-model strict dispatcher 进入，目的是避免再重复“局部 Rust 正确但整体负优化”的路线。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| W1a scheduler drift 被误读为最终精度结论 | 只在 fixture 中验证 `<1e-13s` time-grid delta；未跑 release-wide checker | 回退 `EVAS/evas/simulator/engine.py` 中 `_try_event_transition_ordered_segment_fastpath()` dispatcher 接入 |
| 覆盖范围被过度声明 | gates 排除 child model、timer due、event-body voltage reads、复杂 mixed order | 使用 `profile_fast_evas2` 只统计 strict coverage；速度 claim 仍用 `profile_fast_rust_55` |
| per-point Python trace 仍压过 Rust core | 本轮无 wall rerun，不报告 speedup | 下一步做 sparse record / native scheduler / batch trace before speed rerun |

## Next Step

下一篇审计文档编号和预期主题：

- `107 - EVAS2 Native Scheduler And Sparse Record For Event Transition Core`
