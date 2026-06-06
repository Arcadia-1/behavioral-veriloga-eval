# 100 - Event Transition Coverage Estimator

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `/private/tmp/evas_rust_coverage_100_estimates.json`（本地临时 estimator 输出，不是 repo artifact）
- `EVAS/evas/simulator/rust_coverage.py`
- `EVAS/prototypes/audit_098_current_rust_coverage.py`
- `099-body-ir-rejection-taxonomy.md`

## One-Line Summary

新增静态 coverage estimator，用 099 的 rejection tags 估算：如果实现 event+transition ordered segment，当前 348 个 compile-ok release `.va` 中保守可从 0 个通用 body-IR candidate 提升到约 255 个；若把 bitops/fixed array/bound_step 纳入 V1，可到 268 个；若再做 `$strobe`/file IO side-effect boundary，可到 338 个。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| coverage planning | 只能看到当前 body IR candidate 数 | 新增 `estimate_event_transition_profiles()`，按 support profile 估算未来 candidate 数 | 只读审计，不改变仿真 |
| prototype output | JSON 只有当前 coverage 和 rejection tags | JSON 新增 `event_transition_estimates` | 只影响 audit artifact |
| regression | 没有 estimator 测试 | `test_current_rust_coverage_audit_reports_body_ir_candidates` 检查 event row 会进入 core estimate | 默认不变 |

## Profile Definition

| Profile | Planned support | What it excludes |
|---|---|---|
| `event_transition_core` | event statement / initial_step / cross / timer / above / combined event、`transition(...)`、ordered if write-set、`$abstime` time input、differential output target | bit shifts、arrays/loops、`$bound_step`、`$strobe`/file IO/random/case/while |
| `event_transition_ordered_v1` | core + bit shift ops + fixed array/read/write tags + for-loop + indexed branch/output + `$bound_step` | side-effect system tasks, random, case/while |
| `event_transition_with_side_effect_boundary` | ordered_v1 + `$strobe`/`$fopen`/`$fwrite`/`$fclose`/non-numeric literal side-effect boundary | random distribution, case/while |

These are planning estimates. They mean "current rejection tags would be covered by this future design", not "Rust implementation is already correct or faster".

## Estimate Result

Release tasks root:

`behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks`

| Metric | Value |
|---|---:|
| `.va` files scanned | 357 |
| compile ok | 348 |
| compile failed | 9 |
| current generic body IR candidates | 0 |
| whole-segment candidates | 257 |

Prospective candidate counts:

| Profile | Candidate count | Share of compile-ok release `.va` | Remaining dominant blockers |
|---|---:|---:|---|
| `event_transition_core` | 255 / 348 | 73.3% | `$strobe`/string literal side effects, bit shifts, arrays/loops, `$bound_step`, random/file IO |
| `event_transition_ordered_v1` | 268 / 348 | 77.0% | `$strobe`/string literal side effects, random/file IO, case/while |
| `event_transition_with_side_effect_boundary` | 338 / 348 | 97.1% | `$rdist_normal`, case/while |

Top blockers after `event_transition_ordered_v1`:

| Blocker | Count |
|---|---:|
| `non_numeric_literal` | 76 |
| `system_task:$strobe` | 71 |
| `system_function:$rdist_normal` | 6 |
| `system_function:$fopen` | 5 |
| `system_task:$fwrite` | 5 |
| `case_statement` | 2 |
| `while_loop` | 2 |
| `system_task:$fclose` | 2 |

## Interpretation

The core answer to the user's question is:

> If we implement event+transition ordered segment in a conservative compute-only form, expected generic body-IR coverage increases from `0/348` to about `255/348`.

The more practical V1 target should include bit shifts, fixed arrays/loops, indexed branch/output, and `$bound_step`, because those are small adjacent blockers in event-driven state-machine models. That raises the estimate to `268/348`.

The big remaining jump to `338/348` is not pure computation. It requires a side-effect boundary for `$strobe`/file IO/string literals. That could be done by letting Rust own state/output math while Python owns logging callbacks. But it is riskier than compute-only Rust because observable side effects must remain ordered and byte-compatible.

## Claim Boundary

可以说：

- 当前 P0 body IR candidate 是 `0/348` compile-ok release `.va`。
- Static estimator predicts event+transition core could make `255/348` rows structurally eligible.
- A richer ordered V1 profile predicts `268/348` structurally eligible.
- With side-effect boundary, the upper planning estimate is `338/348`.

不能说：

- 这些 rows 已经 Rust 化。
- 这些 rows 已经 parity PASS。
- EVAS Rust 已经加速这些 rows。
- `338/348` 是安全默认目标；它包含 side-effect boundary，必须单独验证 `$strobe`/file IO ordering.

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_100 PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m py_compile \
  EVAS/evas/simulator/rust_coverage.py \
  EVAS/prototypes/audit_098_current_rust_coverage.py \
  EVAS/tests/test_engine.py

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest EVAS/tests/test_engine.py -k "body_ir or rust_coverage" -q

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 EVAS/prototypes/audit_098_current_rust_coverage.py --json-out /private/tmp/evas_rust_coverage_100_estimates.json
```

Results:

```text
py_compile: pass
targeted body_ir/rust_coverage: 3 passed, 243 deselected
event_transition_core: 255 / 348
event_transition_ordered_v1: 268 / 348
event_transition_with_side_effect_boundary: 338 / 348
```

## Learning Notes

这个 estimator 的含义可以这样理解：

- `0/348` 是现在已经能进通用 body IR 的真实模型数。
- `255/348` 是如果我们实现 event+transition ordered segment，且只处理纯计算语义，预计能进来的模型数。
- `268/348` 是如果我们顺便把 bit shifts、固定数组/循环、`$bound_step` 也纳入第一版，预计能进来的模型数。
- `338/348` 是如果我们允许 Rust 跑计算、Python 保留 `$strobe`/file IO side effects，预计结构上可进来的模型数。

所以 100 给出的不是速度承诺，而是路线判断：event+transition ordered segment 不是小修小补，它可能把通用 body IR 覆盖率从 0 推到 70% 以上。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| estimator 过乐观 | 进入 implementation 后 parity 或 builder fail 大量出现 | 把 profile 支持集收紧，按 fail tag 更新估算 |
| side-effect boundary 被误读为纯 Rust | 报告把 338/348 当作默认 Rust coverage | 保持 255/268/338 三档分开 |
| coverage count 不等于 speed | 后续 speed table 没有随 coverage 上升 | profile report 必须附 runtime counters 和 E2E/core timing |

## Next Step

`101 - Event Transition Ordered Segment Planner`

实现真正的 planner metadata，而不是只看 rejection tags：

1. 从 analog block 抽取 ordered phases；
2. 建立 event due/order + body write-set + transition contribution 的 segment plan；
3. 标记 side-effect boundary；
4. 对 255/268 预计候选重新跑 planner，确认实际 builder candidate 数。
