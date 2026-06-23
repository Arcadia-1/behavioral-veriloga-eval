# 010 - Post-Update Empty Scan Fastpath

Status: `done`

Date: `2026-06-02`

Code commit: `EVAS 4f4b58a`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_engine.py`

## One-Line Summary

利用编译期 `_has_post_update_events` flag，跳过静态模型每步必然为空的 `post_update_events()` 调用，减少无意义 Python 函数调用开销。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| compiler | 已能判断 post-update event，但没有暴露为类 flag | `compile_module()` 写入 `_has_post_update_events` | 默认结果不变 |
| engine loop | 每个模型每步都调用 `post_update_events()` | 只有 `_has_post_update_events=True` 的模型调用 | 静态模型少一次空调用 |
| perf counters | 无法看到跳过次数 | 新增 `model_post_update_calls/skips` | 日志更可审计 |
| tests | 只覆盖 dynamic/bound_step flag | 新增静态跳过和输出依赖 cross 保留测试 | 默认结果不变 |

## Principle

这一步属于 **降低每步成本**。

对普通静态模型来说，生成的 `post_update_events()` 等价于：

```python
def post_update_events(...):
    _post_event_fired = False
    return _post_event_fired
```

每一步调用它不会产生任何新信息，只会带来 Python 函数调用、局部变量初始化和返回开销。010 在编译期证明没有 post-update cross/above 时，主循环直接跳过这个空函数。

关键边界是：这不是 event scheduler 改写。对于输出依赖的 cross/above 事件，`_has_post_update_events=True`，仍然调用原来的 `post_update_events()`。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| static model post-update calls | 每步调用 | `model_post_update_skips == steps_total` | 空工作被跳过 |
| event model post-update flag | implicit | `_has_post_update_events=True` | 输出依赖事件保留原路径 |
| focused tests | 2 capability flag tests | `3 passed` | 新增 fastpath 覆盖 |
| full EVAS tests | `430 passed` at 009 | `431 passed` | 新增 1 个测试，无回归 |

Important interpretation:

- 010 是小型内核快路径，不是最终速度 claim。
- 它不会改变 `cross/above/timer` 的触发顺序。
- 它只消除“编译期已知为空”的 post-update 调用。

## Functional Safety

- Default backend changed: `yes, but only by skipping provably empty post-update calls`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`, because unknown/manual models default `_has_post_update_events=True`
- Accuracy impact: `none expected`, because skipped method had no generated post-update body

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestCompiledModelCapabilityFlags -q
python3 -m pytest tests -q
git diff --cached --check
```

Results:

```text
3 passed in 0.64s
431 passed in 31.86s
git diff --cached --check: clean
```

## Learning Notes

### 什么是 post-update event？

某些 `cross/above` 事件依赖模型自己刚写出的输出节点。模型 evaluate 后，输出值才更新，这时需要再检查一次 event，这就是 post-update path。

简化地说：

```text
evaluate writes V(out)
post_update checks cross(V(out) - threshold)
if fired: run event body and refresh output
```

### 为什么静态模型可以跳过？

如果一个模型只有：

```verilog
V(out) <+ 1.0;
```

它没有需要 evaluate 后再检查的 cross/above。每步调用 `post_update_events()` 只会返回 False。

编译器已经能通过 AST 判断这一点。010 把这个判断变成 runtime flag。

### 为什么这不是 event queue 优化？

event queue 优化会改变“下一步什么时候走、哪个 event 先触发”的调度结构，风险更大。

010 没有改变步长、断点、timer、cross detector 或 event ordering。它只是把“确定为空”的函数调用跳过。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 编译期 flag 漏掉需要 post-update 的事件 | cross/above 相关测试失败，或 Spectre parity 退化 | 回退 EVAS commit `4f4b58a` |
| 手写模型没有声明 flag | 手写模型行为异常 | 基类默认 `_has_post_update_events=True`，保守调用原路径 |
| 误把这当成大幅速度提升 | speed artifact 中只看到很小变化 | 把 010 视为小快路径，后续继续 profile timer/evaluate |

## Next Step

下一篇审计文档建议：

- `011-timer-breakpoint-scan-profile.md`：在不改事件调度的前提下，汇总 timer/cache/breakpoint scan counters，判断是否值得做全局 event queue 或更强的 timer fastpath。
