# 091c - Generic Executor Dispatch Gate Inspector

Status: `done` (gate-only, executor body deferred to 091d)

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `091-generic-event-state-transition-candidate-matcher.md` (091b matcher)
- `066-release-wide-rustification-workplan.md` (W2 General evaluate IR)
- `064-compiler-driven-whole-segment-lowering.md` (dispatcher pattern)

## One-Line Summary

把 091b matcher 输出的 `generic_event_state_transition_v1` candidate metadata 接入 engine 的 `_try_compiler_whole_segment_fastpath` dispatcher 链末尾，加上完整 gate 验证 + 4 个 perf counter（candidate 命中 / 可调度 / 被阻塞 / 阻塞原因）；当前**不替换 Python evaluate**（继续 fall through），让用户能开 opt-in flag `rust_full_model_fastpath=True` 看 candidate 真实 dispatch 命中率而无任何 parity 风险。Executor body 实现是 091d。

## What Changed

| Layer | Before | After |
|---|---|---|
| `engine.py` dispatcher chain | 9 个 specific dispatcher 后直接 return None | 加 `_inspect_generic_event_state_transition_dispatch` 作链末诊断步骤 |
| `engine.py` 新方法 `_inspect_generic_event_state_transition_dispatch` | 不存在 | ~50 行 gate 验证 + counter 记录；返回 None（Python evaluate 继续） |
| `engine.py` perf stats init | 无 091c counter | 加 `generic_executor_models_with_candidate / dispatchable_runs / blocked_runs` |
| `tests/test_audit_091c_generic_dispatch.py` | 不存在 | 4 个测试覆盖 candidate 命中 / fastpath 关闭 / parity / 无 candidate model |

## Why Inspector-Only (Not Full Executor)

吸取本系列 audit 自审教训（088 真实工况 +2.8%、089 -198%、091a 数据驱动），091c 范围严格限制为"诊断阶段"：
- 091b 证明 234/357 (65.5%) release 行符合 generic shape 的 **metadata 层**
- 091c 证明 dispatcher chain 能正确 route 到 generic 入口、记录可调度数
- **091d 才会替换 Python evaluate**，是真正动 model_evaluate_s 47.78% 那一刻

这样把"matcher 正确性"和"executor 正确性"分两步独立验证，避免一次性引入大改动后 parity 风险无法定位。

## Gate Reasons Inspector Will Record

当 model 有 candidate 但 dispatch 因其他原因不能继续时，inspector 记录被阻塞原因：

| Counter key | 含义 |
|---|---|
| `generic_executor_block_reason_multi_model_simulation` | Simulator 含 >1 个 model |
| `generic_executor_block_reason_rust_backend_unavailable` | rust_backend 未加载 |
| `generic_executor_block_reason_model_has_children` | 候选 model 有 child 实例 |
| `generic_executor_block_reason_top_model_no_candidate` | 多 model 时第一个 model 没 candidate |
| `generic_executor_block_reason_no_recorded_signals` | `sim.record()` 未调用 |
| `generic_executor_block_reason_invalid_tstep` | tstep ≤ 0 或 None |
| `generic_executor_block_reason_invalid_tstop` | tstop ≤ 0 或 None |

这些 reason 给 091d 实现 executor 时一份精确的"还得处理什么 edge case"清单。

## Before / After Evidence

### 单元测试（4 个新增，全部通过）

| 测试 | 验证 |
|---|---|
| `test_inspector_counts_model_with_candidate` | 模型有 candidate 且条件 OK → counter +1，`dispatchable_runs=1` |
| `test_inspector_not_invoked_when_fastpath_disabled` | `rust_full_model_fastpath` 默认 False 时 chain 跳过，counter = 0 |
| `test_inspector_returns_none_python_path_still_runs` | inspector 后 Python evaluate 仍跑，waveform bit-exact 一致 |
| `test_model_without_candidate_counts_zero` | 没 generic candidate 的 model 不污染 counter |

### 真实工况 smoke

在 EVAS 自带 cmp_delay 测试桥跑（含 `cmp_delay` + `edge_interval_timer` 两个 model）：

| Counter | Value | 解读 |
|---|---:|---|
| `generic_executor_models_with_candidate` | **0** | cmp_delay 和 edge_interval_timer 都含 `$strobe`，被 091b matcher 正确 reject |
| `generic_executor_dispatchable_runs` | 0 | 无 candidate → 不调度 |
| `generic_executor_blocked_runs` | 0 | 无 candidate → 也不记录 block |

这是预期 — **091b matcher 的保守规则（$strobe 阻塞）在 cmp_delay 上得到验证**，没有误命中。要看真实 dispatch 命中数据，需要 vabench 234 行中**不含 $strobe** 的子集走它们各自的 testbench，本 audit 不涵盖那种规模的 cross-row 测量。

### 全量回归

```text
test_audit_091c_generic_dispatch.py    : 4 passed
全量 tests/                              : 596 + 4 = 600 passed, 0 regression
```

## Functional Safety

- Default backend changed: `no`（gate inspector 只读 perf stats，不写 SimResult）
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes` — inspector 不动 default Python evaluate 路径

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| inspector 抛异常打断 simulation | `_try_compiler_whole_segment_fastpath` 异常 | 在 `_inspect_*` 内加 try/except；或恢复"直接 return None"删除 inspector 调用 |
| counter 累加错误（多调用） | counter > expected | inspector 本身不 reset；测试覆盖单 sim 单 run 的预期值 |
| 未来 091d 取代 inspector 时 counter 含义变化 | 下游脚本读 counter | 091d 应保留这些 counter 名字 + 加"dispatched"信号区分 inspector vs executor |

## Coverage Path Forward

| 阶段 | 工作 | 状态 |
|---|---|---|
| 091a | 调研 blocker 分布 | ✅ done |
| 091b | Generic matcher + schema | ✅ done (234/357 metadata 覆盖) |
| **091c (本 audit)** | **Dispatcher gate inspector** | **✅ done** (0 wall delta, 4 测试通过) |
| 091d | Python executor body 替换 evaluate | ⏳ 下一步 |
| 091e | Rust ABI 替换 Python executor | ⏳ 真实 wall 提升入口 |

## Claim Boundary

可以说：
- Dispatcher 链已正确 wire generic candidate metadata
- 4 个 unit test 验证 inspector 正确性 + parity 不变
- 600 / 600 全量套件通过，0 regression
- cmp_delay 真实工况上 inspector 行为可预测（$strobe → 0 candidate）

**不能说**：
- 091c 让任何模型加速（inspector 返回 None，Python evaluate 仍跑）
- 234 metadata-eligible 中实际有多少会被 091d executor 加速（要等 091d 跑真实工况）
- release-wide wall delta

## Next Step

**091d**：实现 Python executor body 替换 `_inspect_*` 的返回 `None`。复用 transition_target_ir + ordered_transition_shadow 现有 IR，加 event body 内 if/else state machine 解释器（Python 先行）。

工作量：~3-4 小时 implementation + 1 小时 shadow parity + 1 小时 real-row bench。

成功标准：在合成 FSM 模块上 wall ≤ Python evaluate（不期待立即提升，因 Python executor 仍是解释器），但 `dispatchable_runs` 真正成为"executed runs"且 parity bit-exact。**091e (Rust ABI 化) 才是真正释放 model_evaluate_s 47.78% 的步骤**。
