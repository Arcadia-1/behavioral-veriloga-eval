# 098 - Current Rust Coverage And Body IR Production

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related reports:

- `/private/tmp/evas_rust_coverage_098.json`（本地临时 P0 sweep 输出，不是 repo artifact）
- `EVAS/prototypes/audit_098_current_rust_coverage.py`
- `EVAS/evas/simulator/rust_coverage.py`

## One-Line Summary

本轮完成 P0/P1：新增当前 Rust 覆盖率审计器，并把 094 body IR 接到 opt-in production dispatch；但 release-wide sweep 显示当前 094 body IR 对真实 release `.va` 的覆盖仍为 0，所以这不是速度 claim。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| coverage audit | 没有统一回答“当前哪些模型真的能进 Rust” | 新增 `evas.simulator.rust_coverage` 和 `prototypes/audit_098_current_rust_coverage.py` | 只读审计，不改变仿真 |
| compiler metadata | 094 body IR 只存在 standalone tests/runtime | `CompiledModel` 记录 `_rust_body_ir_*` node/state/param/stmt/expr metadata 和 rejection reason | 默认不变 |
| engine dispatch | `Simulator.run()` 不能 opt-in body IR production | 新增 `rust_body_ir=True` opt-in；成功时用 Rust body batch 替代一次 `model.evaluate()` | 默认不变 |
| observability | 无法区分 requested/available/enabled/calls/fallbacks | 新增 `rust_body_ir_*` runtime counters | 便于速度实验判断是否真的命中 Rust |

## Principle

这一步属于“降低每步成本”的前置落地。

原来的 `model.evaluate()` 是 Python 解释器执行：每一步都会通过 Python 对象、字符串 key、dict/state/output helper 去读写节点和状态。094 body IR 的目标是把一个 model body 编成稳定 slot 上的 typed-array 程序，让 Rust 一次执行这一段 body。

这轮只完成了生产入口，不等于已经获得 release 加速。原因很简单：Rust 入口必须先有可执行 body IR；如果 compiler 认为模型里有当前 body encoder 不支持的事件、数组、循环、transition 或复杂控制流，就必须回退 Python。

## P0 Coverage Result

Release tasks 根目录：

`behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks`

| Metric | Value | Interpretation |
|---|---:|---|
| `.va` files scanned | 357 | 全 release gold Verilog-A 源文件 |
| compile ok | 348 | 能被当前 EVAS parser/compiler 编译 |
| compile failed | 9 | 仍不进入 Rust coverage denominator |
| 094 body IR candidates | 0 | 当前 body encoder 尚未覆盖 release 真实模型 |
| static linear candidates | 4 | 旧 static-linear 小子集仍存在 |
| whole-segment candidates | 257 | 现有 whole-segment matcher 能看到大量候选，但不是 094 body IR |
| body IR rejection reason | `body_stmt_ops_unsupported: 348` | 当前 release 编译成功模型全部被 conservative body encoder 拒绝 |

Whole-segment candidate kind 分布：

| Kind | Count |
|---|---:|
| `generic_event_state_transition_v1` | 234 |
| `cmp_delay_log_transition_v1` | 4 |
| `edge_interval_timer_v1` | 4 |
| `cross_scalar_lfsr_transition_bus_v1` | 3 |
| `cppll_timer_v1` | 2 |
| `gain_timer_reduction_v1` | 2 |
| `ref_step_clock_v1` | 2 |
| `sample_hold_rising_v1` | 2 |
| `weighted_dac_v1` | 2 |
| `weighted_sar_adc_v1` | 2 |

结论：P0 的核心价值不是“证明 Rust 已覆盖很多”，而是把事实量化出来。当前 release 的通用 body IR 覆盖率是 0；真正有覆盖的是之前 hand-written / matcher-driven whole-segment fastpath。

## P1 Production Hook

新增 `Simulator.run(..., rust_body_ir=True)`。命中条件非常保守：

- Rust backend 可加载；
- model 有 `_rust_body_ir_stmt_ops`；
- 当前不在 event trace audit；
- 当前不在 event context；
- model 没有 child model；
- 当前没有 pending transition；
- body IR batch 执行成功。

命中后，engine 不调用 Python `model.evaluate()`，而是：

1. 把当前 node/state/parameter slots 打包成 typed arrays；
2. 调用 `RustBackend.evaluate_body_ir(...)`；
3. 把 target state slots 写回 indexed state；
4. 把 target node slots 写回 output nodes；
5. 记录 calls/executed/fallbacks/node writes/state writes counters。

这仍然是 per-call pack/unpack，不是最终形态。它的意义是建立正确的 production dispatch contract；真正速度收益需要 P2 把 node/state arrays 持久化，避免每步打包。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| release 094 body IR candidates | n/a | 0 / 348 compile-ok | release 真实模型尚未进入 094 production |
| targeted body-IR tests | n/a | 3 passed | synthetic/general subset production dispatch 正确 |
| Rust/audit targeted tests | n/a | 37 passed | 094 expression/body/runtime 相关路径未回归 |
| speed claim | no | no | 当前没有 release 命中，不允许报告速度收益 |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_p0p1 PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m py_compile \
  EVAS/evas/simulator/backend.py \
  EVAS/evas/simulator/engine.py \
  EVAS/evas/simulator/rust_coverage.py \
  EVAS/prototypes/audit_098_current_rust_coverage.py

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest EVAS/tests/test_engine.py -k "body_ir or rust_coverage" -q

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest \
  EVAS/tests/test_audit_094a_expr_ir.py \
  EVAS/tests/test_audit_094b_stmt_schedule_ir.py \
  EVAS/tests/test_audit_094d_state_binding_ir.py \
  EVAS/tests/test_audit_094f_body_ir_encoder.py \
  EVAS/tests/test_audit_094h_event_due_program.py \
  EVAS/tests/test_audit_094n_transition_runtime.py \
  EVAS/tests/test_audit_094o_analog_block_runtime.py \
  EVAS/tests/test_rust_backend.py \
  EVAS/tests/test_engine.py \
  -k "body_ir or rust_coverage or audit_094 or body_expr or body_ir_batch" -q

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 EVAS/prototypes/audit_098_current_rust_coverage.py --json-out /private/tmp/evas_rust_coverage_098.json
```

Results:

```text
targeted body_ir/rust_coverage: 3 passed, 243 deselected
broader 094/Rust subset: 37 passed, 277 deselected
release coverage sweep: 357 scanned, 348 compile ok, 0 body IR candidates
```

Note: prototype 文件在本审计收尾时从 `audit_096_current_rust_coverage.py` 改名为 `audit_098_current_rust_coverage.py`，避免和既有 `096-transition-production-real-release-sweep.md` 以及 096 中预留的 097 slowdown 文档语义冲突。重跑命令应使用 098 路径。

## Learning Notes

可以把现在的 Rust 化分成两类：

| Type | How it works | Current status |
|---|---|---|
| hand-written whole-segment fastpath | 先用 matcher 识别某类真实模型，再用专门 Rust 函数跑整段行为 | 已覆盖一些 top-wall 行，能有真实速度收益 |
| generic body IR | compiler 把 Verilog-A body 编成通用 IR，Rust 执行这个 IR | 入口已接入，但 release 覆盖仍为 0 |

为什么 P1 做完还没有速度收益？因为“有 Rust 发动机”和“路能通到真实模型”是两件事。P1 只是把发动机接进车架；P0 告诉我们真实 release 的路标现在还没有指向这个入口。

下一步不是继续做小型 per-call Rust 函数，而是扩大 body IR encoder 的语言覆盖，让 `generic_event_state_transition_v1` 这 234 个 whole-segment candidate 中的 event body / output write / transition contribution 可以进入同一个 Rust body program。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| opt-in body IR 写错 state/node slot | targeted parity test 失败，或 `rust_body_ir_production_fallbacks_total` 异常增加 | 关闭 `rust_body_ir`，回退 `backend.py` / `engine.py` 的 P1 hook |
| coverage audit 被误当速度证据 | 报告中出现 0 candidate 却 claim speedup | 保持本文 claim boundary，不提交 raw sweep 为 speed artifact |
| release coverage 长期为 0 | P0 sweep rejection reason 仍集中在 `body_stmt_ops_unsupported` | 优先扩展 `stmt_ir` / `encode_body_stmt_ops`，而不是优化 dispatch |

## Next Step

`099 - Release Body IR Coverage Expansion`

优先把真实 release 中最高频的 `generic_event_state_transition_v1` 语义接进 body IR：event body state/output writes、transition contribution、固定数组/循环、简单条件控制流。目标不是立即跑速度表，而是先让 P0 coverage 从 0 上升到可审计的候选数量。
