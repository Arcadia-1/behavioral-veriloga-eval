# 011 - Timer Breakpoint Scan Profile

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS 608551b`

Related paths:

- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_engine.py`

## One-Line Summary

新增 simulator-level scan counters，汇总 source breakpoint、model breakpoint、`$bound_step` scan 调用规模，以及模型级 timer breakpoint cache counters，为后续 timer/event 优化提供证据。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| engine scan counters | 只有 clamp 次数 | 新增 scan calls 计数 | 仿真结果不变 |
| timer counters | 只在每个 model 的 `_perf_stats` 里 | 汇总到 simulator `_perf_stats` | 日志更容易审计 |
| tests | 覆盖 timer/bound_step 功能 | 新增 counter 口径断言 | 功能结果不变 |

新增 simulator-level counters：

```text
source_breakpoint_scan_calls
model_breakpoint_scan_calls
bound_step_scan_calls
timer_breakpoint_cache_hits_total
timer_breakpoint_hits_total
timer_breakpoint_scans_total
timer_state_updates_total
```

## Principle

这一步不是直接加速，而是 **定位是否值得优化事件/断点扫描**。

当前每个 transient step 都会按顺序检查：

```text
source breakpoints
model next_breakpoint()
$bound_step
```

其中 `model.next_breakpoint()` 内部又会看：

```text
transition breakpoints
cross detector breakpoints
above detector breakpoints
timer breakpoints
child model breakpoints
```

如果某些 benchmark 慢在“每一步都扫很多动态对象”，后续就应该优先做 event/timer fast path。反过来，如果 scan calls 很少但 `model_evaluate_s` 高，就说明 Rust model-evaluate/indexed expression 更优先。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| source/model/bound_step scan scale | 只有 timing 或 clamp | 有 call counters | 能区分“扫了很多但没 clamp”和“确实触发 clamp” |
| timer cache evidence | model-local only | simulator aggregate | release 日志更容易归因 |
| focused tests | functional only | `3 passed` | 新增 counter 口径覆盖 |
| full EVAS tests | `431 passed` at 010 | `431 passed` | 无回归 |

Important interpretation:

- 011 不改变 timestep、breakpoint choice 或 event ordering。
- 011 不代表 EVAS 已经变快。
- 这些字段是后续优化优先级证据，不是 paper-facing speed claim。

## Functional Safety

- Default backend changed: `no semantic change`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `not applicable`
- Accuracy impact: `none expected`, because only counters are incremented after existing scan sets are already chosen

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestTimerEvent::test_timer_fires_periodically tests/test_engine.py::TestBoundStep::test_bound_step_limits_dt tests/test_engine.py::TestCompiledModelCapabilityFlags::test_static_contribution_model_skips_dynamic_scans -q
python3 -m pytest tests -q
git diff --cached --check
```

Results:

```text
3 passed in 1.70s
431 passed in 36.05s
git diff --cached --check: clean
```

## Learning Notes

### clamp 次数和 scan 次数有什么区别？

`clamp` 表示某个断点真的把当前 `dt` 变小了。

`scan` 表示仿真器检查过它，即使最后没有改变 `dt`。慢点经常来自 scan，而不是 clamp：

```text
每步扫 100 个对象，但只有 1 次真的 clamp
```

这种场景下，只看 clamp 会低估开销。

### timer cache counters 说明什么？

timer 的下一个触发点可以缓存。理想情况是：

```text
timer_breakpoint_cache_hits_total high
timer_breakpoint_scans_total lower
```

如果 scans 很高、cache hits 很低，说明 timer 状态频繁变化或 cache 设计不够有效，后续可以考虑更强的 timer/event queue。

### 为什么 011 不直接做 event queue？

event queue 会改变“谁是下一个事件”的数据结构，也可能影响同一时间点多个 event 的排序。这个风险比 counter 大很多。

011 先补证据，下一步再决定是否值得做 queue 或更小的 fast path。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| counter 口径误解 | 把 scan calls 当成 wall time | 文档中保持“规模证据，不是速度证据”口径 |
| counter 增加微小开销 | microbenchmark 看到极小 overhead | 可回退 EVAS commit `608551b`，或仅在 profile flag 下计数 |
| timer aggregate 漏子模型 | nested model timer test 失败或 aggregate 与 model-local 不一致 | 扩展 `_aggregate_model_timer_stats()` traversal |

## Next Step

下一篇审计文档建议：

- `012-profile-guided-kernel-sample.md`：在代表性 benchmark 上同时打开 `EVAS_PROFILE_MODEL_EVAL=1` 和 section timing，采样 `model_evaluate_s`、scan counters、timer cache counters，决定 012/013 是继续 Rust/indexed expression，还是做 timer/breakpoint fast path。
