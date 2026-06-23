# 009 - Indexed Model Evaluate Profile

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS c039159`

Related paths:

- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

新增显式 `EVAS_PROFILE_MODEL_EVAL=1` 诊断开关，按模型聚合 `prepare_step`、`evaluate`、`post_update` 时间，为后续判断该优先优化 model evaluate、timer/breakpoint scan 还是 event queue 提供证据。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `Simulator.run()` | 只有全局 section timing | 新增 `profile_model_eval` 参数和 `_model_profile_stats` | 默认无变化 |
| runner config | 无 model-eval profile 开关 | 支持 `evas_profile_model_eval` / `EVAS_PROFILE_MODEL_EVAL` | 默认关闭 |
| log | 只有 `Section timing counters` 和 `Model event counters` | opt-in 时新增 `Model timing counters` | 只影响诊断日志 |
| tests | indexed/profile 侧重全局 timing | 新增显式 opt-in 和日志开关测试 | 默认无变化 |

## Principle

这一步不是直接加速，而是 **决定下一步该优化哪里**。

之前我们能看到全局时间：

```text
model_prepare_step_s
model_evaluate_s
model_post_update_s
```

但看不到具体是哪一个 model 热。009 增加 per-model 聚合：

```text
model[0] Foo:
    prepare_step_s
    evaluate_s
    post_update_s
    evaluate_calls
```

这样后续做 speed profile 时可以区分两种情况：

- 某个 measurement-heavy model 的 `evaluate_s` 高：优先迁移 `_get_voltage`、表达式执行、`_set_output` 到 indexed/Rust。
- 很多模型的 `post_update_s` 或 event/timer counters 高：优先优化 timer、cross、above、breakpoint scan。

## Why It Is Explicit Opt-In

`perf_counter()` 本身也有成本。若在每次 `_get_voltage()` 或每个 event check 里直接打点，profile 可能比真实热路径还重，最后测出来的是 profiler，不是 simulator。

因此 009 只做粗粒度 model-level timing，并且必须显式打开：

```bash
EVAS_PROFILE_MODEL_EVAL=1 evas simulate tb.scs -o out
```

正式速度表不能打开这个开关。它只用于定位瓶颈。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| default backend | unchanged | unchanged | 默认仿真没有切换 |
| default model timing log | absent | absent | 默认不产生 profile 开销 |
| opt-in model timing log | absent | `Model timing counters` | 可定位单个 model 热点 |
| focused tests | none | `2 passed` | 覆盖 engine 和 runner 开关 |
| full EVAS tests | `428 passed` at 008 | `430 passed` | 新增 2 个测试，无回归 |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, because profile is disabled unless explicitly requested
- Accuracy impact: `none expected`, because this only records time after existing calls return

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestSimulator::test_model_eval_profile_is_explicitly_opted_in tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_model_eval_profile_when_opted_in -q
python3 -m pytest tests -q
git diff --cached --check
```

Results:

```text
2 passed in 0.61s
430 passed in 32.56s
git diff --cached --check: clean
```

## Learning Notes

### 为什么不直接优化 timer/breakpoint？

可以优化，但要先知道它是不是当前任务的最大头。EVAS 的慢可能来自：

```text
每步成本高：evaluate 里 Python dict/object/string lookup 多
步数太多：timer/cross/bound_step 让仿真走了很多小步
外层成本高：CSV/checker/E2E harness
```

009 先把 `evaluate`、`prepare_step`、`post_update` 分出来，是为了决定下一步投入在哪里最划算。

### 为什么 profile 不能和速度 claim 混用？

profile 打点会改变 wall time。尤其 Python 里 `perf_counter()`、dict 更新、字符串 key 写入都会有成本。如果打开 profile 后说“EVAS 比 AX 慢/快”，这个结论就被 profile 开销污染了。

所以速度 claim 要用 profile 关闭的干净 run；profile 只用来解释瓶颈。

### 为什么只做 model-level，不做 `_get_voltage` 每次计时？

`_get_voltage()` 是热函数。每次调用都计时会改变热函数成本。009 只在 model evaluate 外层计时，先找到哪个 model 热；等需要更细粒度时，再对单个代表性 benchmark 做专门 profile。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| profile 开关误用于 paper speed run | speed log 里出现 `evas_profile_model_eval = true` | 重新跑 profile-off timing |
| profile 自身污染 indexed speed run | `Model timing counters` 出现在 speed artifact | 禁用 `EVAS_PROFILE_MODEL_EVAL` |
| 粗粒度 profile 不足以定位 `_get_voltage` 细节 | 只能看到 model 热，不能看到函数热 | 对热点 model 做临时 finer-grained diagnostic，不作为默认路径 |
| 日志字段误解为性能提升 | 只有 timing counters，没有 wall improvement | 明确写成 diagnostic evidence |

## Next Step

下一篇审计文档建议：

- `010-timer-breakpoint-fastpath.md`：利用 009 的 profile 结果和现有 event counters，先做低风险空工作跳过或 timer/breakpoint scan 快路径；不改变 cross/above event ordering。
