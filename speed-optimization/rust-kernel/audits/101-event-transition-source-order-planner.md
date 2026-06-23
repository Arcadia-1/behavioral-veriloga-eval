# 101 Event/Output/Transition Source-Order Planner

Status: diagnostic, not production speed evidence.

## 这一步改了什么

100 只做了 tag-based 覆盖估算：如果未来 Rust runtime 支持某些语义 tag，例如 `event_statement`、`transition_expr`、`complex_if_write_set`，理论上能覆盖多少模型。

101 把这个估算推进到 source-order planner：对每个 compile-ok Verilog-A 模型重新 lower analog block，检查它是否真的具备一个整段 Rust runtime 可以接住的源码形状：

- 顶层 event statements 先出现；
- 后面接 continuous assignment / output write / `transition()` contribution；
- 每个 event due trigger 能形成 event due program；
- 当前 profile 声称支持的 tags 必须覆盖该模型的 rejection tags。

这仍然只是诊断 metadata。它没有把 production simulator 默认切到 Rust，也不能作为速度 claim。

## 修改位置

- `EVAS/evas/simulator/event_transition_plan.py`
  - 新增 `EventTransitionSegmentPlan`。
  - 新增 `analyze_event_transition_segment_plan(...)`。
  - 负责判断 source-order shape、event due 可编码性、continuous/output/transition 段计数。
- `EVAS/evas/simulator/rust_coverage.py`
  - 每个 `RustCoverageRow` 增加 `event_transition_plan_*` 字段。
  - 新增 `estimate_event_transition_plan_profiles(...)`。
- `EVAS/prototypes/audit_098_current_rust_coverage.py`
  - JSON 输出增加 `event_transition_plan_estimates`。
- `EVAS/tests/test_engine.py`
  - 增加 event + transition fixture，锁住 tag estimate 与 planner estimate 的基本行为。

## 全量 release 扫描结果

命令：

```bash
PYTHONPATH=EVAS python3 EVAS/prototypes/audit_098_current_rust_coverage.py \
  --json-out /private/tmp/evas_rust_coverage_101_plan.json
```

基础统计：

| 指标 | 数值 |
| --- | ---: |
| `.va` 文件数 | 357 |
| compile-ok | 348 |
| compile-failed | 9 |
| 当前 generic body-IR candidates | 0 |
| static-linear candidates | 4 |
| existing whole-segment candidates | 257 |

tag estimate 与 source-order planner 的区别：

| profile | tag estimate | source-order planner | 差距含义 |
| --- | ---: | ---: | --- |
| `event_transition_core` | 255 / 348 | 231 / 348 | 24 个模型 tag 看起来能支持，但源码顺序或 due 编码还不能直接接整段 runtime |
| `event_transition_ordered_v1` | 268 / 348 | 239 / 348 | 增加 bit/array/loop/indexed output 支持后，仍被 source-order 和 dynamic due 限制 |
| `event_transition_with_side_effect_boundary` | 338 / 348 | 288 / 348 | 加入 side-effect boundary 后理论上很高，但仍有 50 个模型卡在 source order / event due |

planner-accepted rows 中的工作量规模：

| profile | rows | event stmts | due triggers | transitions | direct outputs | top-level control flow |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `event_transition_core` | 231 | 473 | 476 | 475 | 20 | 26 |
| `event_transition_ordered_v1` | 239 | 494 | 497 | 509 | 20 | 26 |
| `event_transition_with_side_effect_boundary` | 288 | 608 | 652 | 593 | 51 | 31 |

主要 blocker：

| profile | rejection summary |
| --- | --- |
| `event_transition_core` | `unsupported_tags` 93, `event_due_unencodable` 14, `event_after_continuous_statement` 10 |
| `event_transition_ordered_v1` | `unsupported_tags` 80, `event_after_continuous_statement` 15, `event_due_unencodable` 14 |
| `event_transition_with_side_effect_boundary` | `event_after_continuous_statement` 34, `event_due_unencodable` 16, `unsupported_tags` 10 |

## 如何理解这些数字

`255/268/338` 是上限估算：它只看当前 body IR 为什么拒绝，并假设 future runtime 能支持对应语义。

`231/239/288` 更接近工程落地候选：它额外要求源码顺序能组成一个 runtime segment，并且 event due 能编码。后续 production Rust 应优先对这些 rows 做 shadow parity，再 opt-in。

当前不能 claim 全量 Rust 化，也不能 claim speedup，因为还没有把 planner-accepted segment 接入 production engine，更没有 release-wide E2E/simulator wall 重跑。

## 下一步工程顺序

1. 接 `event_transition_core` production shadow：用 231 rows 作为第一批候选，只对 source-order planner accepted 的模型开启。
2. 做 multi-phase source-order runtime：解决 `event_after_continuous_statement`，不要强行重排语义，而是把 analog block 切成 continuous-prefix / event / continuous-suffix 等有序段。
3. 做 dynamic/state-owned timer due：解决 `event_due_unencodable`，重点是 timer start/period 读取 state 或随时间更新的情形。
4. 做 side-effect boundary：`$strobe` / file IO 不能简单变成纯 Rust，需要 Python callback 或 side-effect queue；它是 E2E 支持问题，不是纯数值内核。
5. 补剩余 tags：`case_statement`、`while_loop`、`$rdist_normal` 是剩余全量覆盖的小尾巴。

## 验证

```bash
PYTHONPYCACHEPREFIX=/private/tmp/evas_pycache_101 python3 -m py_compile \
  EVAS/evas/simulator/event_transition_plan.py \
  EVAS/evas/simulator/rust_coverage.py \
  EVAS/prototypes/audit_098_current_rust_coverage.py

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  -k "current_rust_coverage or body_ir or rust_coverage" -q

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_engine.py \
  -k "rust or body_ir or event_due or analog_block or transition_contribution" -q
```

结果：

- Targeted coverage test: `3 passed, 243 deselected`。
- Broader Rust/094 subset: `47 passed, 199 deselected`。
