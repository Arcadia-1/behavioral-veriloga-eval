# 091 - Generic Event-State-Transition Candidate Matcher

Status: `metadata-only` (executor pending in 091c)

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `064-compiler-driven-whole-segment-lowering.md`
- `065-semantic-dataflow-whole-segment-matching.md`
- `066-release-wide-rustification-workplan.md` (W2/W3)
- `067-release-rust-coverage-manifest-generator.md`

## One-Line Summary

新增 `generic_event_state_transition_v1` whole-segment candidate kind 作为兜底匹配器：识别"1+ cross/timer 事件 + event body 内 if/else 状态机 + 1+ transition 输出"这个通用 shape，**release-wide whole-segment metadata 覆盖从 23/357 (6.4%) 跳到 257/357 (72.0%)**；现有 9 个 specific candidate（cmp_delay/cppll/sar/等）零干扰。**仅 metadata 层** — 实际执行 path 留待 091c executor 落地。

## Why This Audit Exists

cmp_delay profile 显示 `model_evaluate_s` 占总 wall **47.78%**，是真正的瓶颈。Per-operator Rust 化（086/088/089）撞 per-call FFI 边界开销墙，089 甚至变 -198% 反优化。

唯一能解决 `model_evaluate_s` 的路径：**让整个 evaluate body 在 Rust 跑**。064/065 已建好"compiler-driven whole-segment lowering"框架，但 9 个 specific candidate 只覆盖 23/357 (6.4%) 真实 release 模型。剩余 334 个走 Python evaluate loop。

091a 调研发现：这 334 中 91.6% **没有 exotic 特征**，就是简单的 event + FSM + transition 输出。它们不命中现有 candidate 不是因为有 bit-ops/math/strobe 阻塞，而是**现有 candidate 都按特定电路 dataflow hand-tune，缺一个通用形状匹配器**。

091b 加这个通用 matcher。091c 加 generic executor（下一步）。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| `backend.py` `_collect_whole_segment_candidates` | 9 个 specific collector | 加 fallback `_collect_generic_event_state_transition_candidate` 在所有 specific 没匹配时触发 | 默认仿真不变 |
| `backend.py` 新 collector | 不存在 | 实现 ~110 行 conservative matcher：require cross/timer event + transition output + pure-if/else event body | 默认仿真不变 |
| `whole_segment.py` schema | 9 kinds | 加 10th kind `generic_event_state_transition_v1` 带 6 个 typed fields | 默认仿真不变 |
| `tests/test_audit_091b_generic_candidate.py` | 不存在 | 7 个新测试覆盖 match / reject / coexistence | 7/7 通过 |

## Matcher Logic (保守规则)

匹配条件（全部满足才返回 candidate）：

1. ≥1 个 `cross()` 或 `timer()` 事件（`@(initial_step)` 单独不算）
2. ≥1 个 contribution 在所有事件**外**，RHS 包含 `transition()` 调用
3. **所有 cross/timer 事件 body** 只含：`Assignment` + `IfStatement` + `Block`，且：
   - 不含 `Contribution`
   - 不含 `For/While/Case`
   - 不含 system task（`$strobe/$display/$random/...`）
   - 赋值 target 必须是 scalar `Identifier`（不允许 array index）
   - RHS 不含 dynamic bus `V(bus[i])`
4. 事件 body 至少写过一个 scalar state（防止 trivial empty body 误匹配）

被 reject 的常见情况：
- 仅 `@(initial_step) + V(out) <+ const`（无 cross/timer）
- event body 含 `$strobe`（即使只在 cross body 内）— 091a 数据显示这阻塞 2/107 (~2%)
- event body 含 `for/while`（阻塞 2/107）
- event body 写 array element

## Before / After Evidence

**Per-row coverage on release 357 models**:

| Metric | Before 091b | After 091b | 变化 |
|---|---:|---:|---|
| `whole_segment_candidate` rows | 23 (6.4%) | 23 (6.4%) | 不变（specific 优先） |
| `generic_event_state_transition_v1` rows | 0 | **234 (65.5%)** | **+234** |
| 总有 whole-segment metadata 行 | 23 (6.4%) | **257 (72.0%)** | **11.2× 增长** |
| 重叠（specific + generic 同时命中） | n/a | **0** | matcher 按设计互斥 |

**Per-unique-source coverage**（去重 sha256，152 唯一）：

| Metric | Count |
|---|---:|
| 现有 specific 唯一源 | ~14（估算，每种 ~2 个） |
| 新 generic 唯一源 | **101** |
| 合并唯一源 | ~115 / 152 (75%) |

**测试**：7 个新单元测试 + 568 既有 + 15 audit 088 + 6 audit 089 = **596 / 596 pass**，0 regression。

## Functional Safety

- Default backend changed: `no`（compiler emit metadata，runtime 没接收 — Python evaluate loop 仍跑）
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes` — 没 generic executor 时一切走原 Python path

## Why This Doesn't Change Wall Time Yet

091b **没有 executor**。compiler 现在能在 234 个新模型上生成 `generic_event_state_transition_v1` candidate metadata，但 engine 的 `_try_compiler_whole_segment_fastpath` 不识别这个 kind → 走默认 Python evaluate 路径。

这是 metadata 与 execution 分离的标准两阶段策略（见 audit 066 W0/W1 分工）：
- **091b（本 audit）**：metadata 覆盖率 → 验证有 234 个模型符合通用 shape
- **091c（下一 audit）**：实现 generic executor → 兑现实际 wall 提升

## Coverage Path Forward

| 阶段 | 工作 | 预期覆盖 | 预期 wall 影响 |
|---|---|---:|---|
| ✅ 091a | 调研 blocker 分布 | n/a | 0% |
| ✅ 091b（本 audit）| Generic matcher + schema | 257/357 (72%) metadata | 0% （仍 Python loop） |
| ⏳ 091c | Generic executor（Python 版本先行）| 257/357 (72%) execution | 待测；理论上把 `model_evaluate_s` 47.78% 中的相应部分 lower |
| ⏳ 091d | Generic executor Rust ABI | 同上 | 进一步消除 Python 解释器开销 |
| ⏳ 091e | 真实 row bench validation | n/a | 验证 release-wide wall delta |

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Generic matcher 过宽误命中 | future 091c executor 在某 row 上 parity fail | tighten matcher gate（已有 7 个 reject 测试守底）；或 disable matcher via env flag |
| 与 specific candidate 顺序冲突 | 同一模型出现多个 kind | matcher 已设计为 `if not candidates:` 兜底，验证 0 重叠 |
| 调研口径估算的"234 行可加速"实际命中率低 | 091c 落地后真实加速行数显著少于 234 | metadata 数 != 加速数；091c 必须有自己的 fallback gate（wiring 不通就退回 Python）|

## Claim Boundary

可以说：
- **metadata 层**：generic candidate 把 release-wide whole-segment 元数据覆盖率从 6.4% 提到 72.0%
- 0 regression，0 overlap，0 default-behavior change
- 7/7 单元测试 + 596 全量测试通过
- matcher 的保守 reject 规则在 091a 数据上有可验证依据

不能说：
- release-wide 任何 wall 提升（091b 0 executor）
- 234 行最终都能 lower 到 Rust（091c executor 还得验证 dataflow 完整性）
- paper-facing speed claim

## Lessons From 086/088/089

091a/b 是这一轮自审教训的直接反馈：
- 086 真实工况 +2.8%、088 真实工况 +2.8%、089 真实工况 **-198%** — 都是 per-call FFI 边界开销吃掉 operator 级 Rust 化的收益
- cmp_delay profile 揭示 model_evaluate_s 47.78% 是真瓶颈
- 唯一能动这个 47% 的路径是 whole-segment Rust ownership
- 工作量从最初估计的 12-16 小时（包括 bit-ops/math 扩展）下调到 ~5-7 小时（因 091a 数据证明这些 feature 几乎不阻塞）

## Next Step

**091c - Generic Event-State-Transition Executor**：
- 在 engine 加 `_try_generic_event_state_transition_fastpath` dispatcher
- Lower event body 的 if/else 状态机 + scalar state 写到 typed-array IR
- 复用 `ordered_transition_shadow` 的 transition target IR
- 先实现 Python 版本（验证 parity，不期待立即 wall 提升）；091d 再迁 Rust ABI

工作量：~3-4 小时（Python executor）+ 1 小时（parity + bench）。
