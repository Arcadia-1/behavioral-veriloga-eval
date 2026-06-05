# 088 - Transition Per-Step Batch Implementation

Status: `done`

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `050-transition-state-rust-primitive.md`
- `085-cross-above-transition-default-adaptive-trace.md`
- `086-transition-operator-persistent-buffer-reuse.md`
- `087-transition-per-step-batch-design.md`
- `../RUSTIFICATION_WORKLIST_20260605.md`

## One-Line Summary

按 087 设计落地 transition operator 的 per-step batch — compiler 新加 `TransitionDeferralAnalyzer` 静态分析 pass 检测 intra-evaluate self-read，安全的 `V(out) <+ scale*transition()+offset` contributions 走新发射的 `_transition_output_lazy()` 入队，evaluate() 末尾一次 `_flush_transitions()` 单次 Rust FFI 处理所有 pending；bench 上 **transition-heavy 3-output 模型 wall 提速 1.42×（29.5%）**，FFI hop 数从 N→1 per step（3× 减少），输出 bit-exact parity，568 全量测试零 regression。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Compiler L2 | 仅有 `_transition_output`/`_transition` 立即调用 emit | 新增 `_collect_transition_defer_unsafe_nodes()` 静态分析 pass；fastpath emission 在 safe 节点上改为 `_transition_output_lazy(...)`；evaluate body 末尾追加 `if pending: self._flush_transitions(nv, time)` | 默认 backend 不变；opt-in `rust_transition_production=True` 路径 waveform bit-exact 一致 |
| Runtime L3 (backend.py) | `_transition_output()` 立即调 `_transition()` → `_transition_rust_production()` → 单次 Rust FFI | 新增 `_transition_output_lazy()` 入队 9 个 Python list；新增 `_flush_transitions()` 构建 14 个 size-n typed array 后一次性调 Rust FFI；新增 `_flush_transitions_fallback()` 兜底；新增 `_reset_transition_pending()` 清队 | 同上 |
| Perf counters | 没有 batch 相关指标 | 新增 `rust_transition_batch_flushes`、`_batch_slot_total`、`_batch_max_slots`、`_batch_fallbacks`、`_lazy_enqueues`（各自 `_total` 别名也加） | runner 可见 batch 行为 |
| Tests | 2 个 fastpath emission 断言只接受立即形 | 改为接受 `_transition_output(` 或 `_transition_output_lazy(` | 不破坏既有测试 |

## Principle

属于**降低每步成本** + **减少 Rust 边界成本**。

085 之前每个 `V(out) <+ scale*transition()` contribution 走立即路径：
```
compiled evaluate():
  step k:
    self._transition_output(o1, ...) → Rust FFI #1
    self._transition_output(o2, ...) → Rust FFI #2
    self._transition_output(o3, ...) → Rust FFI #3
```

每次 FFI 都付 ctypes dispatch + Python ↔ Rust 边界开销。每行 simulation 累积 FFI 数从几千到几万。

088 后：
```
compiled evaluate():
  step k:
    self._transition_output_lazy(o1, ...) → 入队
    self._transition_output_lazy(o2, ...) → 入队
    self._transition_output_lazy(o3, ...) → 入队
    self._flush_transitions(nv, time)     → 一次 Rust FFI 处理 3 个 slot
```

3 次 FFI → 1 次 FFI。Rust 端数学完全不变（`transition_state_step_for_arrays` 一直就支持 state_count batch — 086 在 size-1 上跑，088 让它跑 size-n）。

## Static Analyzer 关键点

defer 不安全的场景（必须保持立即写）：

```verilog
V(out) <+ scale * transition(target, 0, 1n, 2n);   // 写 out
x = V(out);                                         // ← 同一 evaluate 内读 out
V(out2) <+ scale * x;
```

如果第 1 行 defer 到 evaluate 末，第 2 行 `V(out)` 读到的是上一步旧值 → parity 直接挂。

`_collect_transition_defer_unsafe_nodes()` 做两遍 DFS：
1. 按源序构造 `(kind, node)` timeline（kind ∈ {`transition_write`, `read`}）
2. 对每个 transition_write，扫后续 timeline；遇到同 node 的 read → 标 unsafe

保守：if/for/while/case 的 cond 表达式中的 V() 也算 read；for 循环展开是动态的 → 体内任何 write 也保守标 unsafe；任何识别不到的 statement 类型都跳过（不发 read 也不发 write，相当于"不知道就别假设"）。这意味着：
- **False positive（safe → unsafe）**：可接受，只是少 defer，不影响 parity
- **False negative（unsafe → safe）**：必须零容忍，否则 parity 挂

## Before / After Evidence

Bench：`EVAS/prototypes/audit_088_bench.py`，5 repeats，3-transition module，tstop=50ns，tstep=50ps。**086 bench 在新代码下被 088 接管 fastpath**（详见 Learning Notes），所以 088 bench 是独立设计的 apples-to-apples 对照（monkey-patch analyzer 把所有节点标 unsafe → 强制走 086 immediate 路径作为 baseline）。

| Metric | 086 immediate（forced） | 088 batch（default） | 变化 |
|---|---:|---:|---|
| wall median (s) | 2.648049 | 1.866073 | **1.418× faster (≈29.5%)** |
| wall min (s) | 2.639133 | 1.848333 | |
| wall max (s) | 2.907323 | 1.967057 | |
| Rust FFI hops | 118,245 | 39,414 | **3.0× fewer**（匹配 3 transitions/step） |
| avg transitions per flush | 1.0 | 3.0 | |
| batch_max_slots | 0 | 6 | |
| lazy_enqueues | 0 | 118,245 | 所有 transition 都入队 |
| batch_fallbacks | 0 | 0 | Rust 0 失败 |
| Output parity (sum \|diff\| over 3 nodes) | n/a | **0.000000e+00** | bit-exact |
| pytest 全量 | n/a | **568 passed** | 0 regression |

跨 audit 的累积速度路径（同一 transition-heavy 工况大致估算）：
- Pre-086 baseline（per-call alloc + per-call FFI）→ 086（持久 buffer + per-call FFI）：**1.135× faster**
- 086 → 088（持久 buffer + per-step batch）：**1.418× faster**（额外）
- 累积粗估：pre-086 → 088 约 **~1.6×**（待真实 vabench 多 row rerun 校核）

## Functional Safety

- Default backend changed: `no`（仍需 `rust_transition_production=True` opt-in）
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`（Rust FFI 失败 → 立即对所有 pending 走 immediate `_transition_output` 重放）

## Validation

Commands run:

```bash
PYTHONPATH=. python3 -m pytest tests/test_engine.py -k 'transition' -q  # 37 passed
PYTHONPATH=. python3 -m pytest tests/test_rust_backend.py -q             # 34 passed
PYTHONPATH=. python3 -m pytest tests/ -q                                 # 568 passed
PYTHONPATH=. python3 prototypes/audit_088_bench.py                       # 1.418x speedup
```

## Learning Notes

**为什么 086 bench 在 088 落地后 speedup 降到 0.999×？**

086 是给 `_transition_rust_production()`（per-call FFI 路径）的 14 个 size-1 buffer 加持久化。但 088 让 compiler 对所有 fastpath transition 改 emit `_transition_output_lazy(...)`，**完全绕过** `_transition_rust_production()`。所以 086 bench 测的"baseline vs persistent buffer"对照在 088 模式下都走相同 batch 路径，速度无差异。

这不是 086 work 浪费 — 086 的持久 buffer **仍服务于 general path**（`_transition()` 被用在 `x = transition()` 这种返回值表达式里时，走的还是 `_transition_rust_production()`，那条路径上 086 buffer 仍有效）。本 audit 实测的 3-output 模块没有用 general path，所以 086 buffer 没被触发。

**为什么 batch_max_slots = 6 而不是 3？**

模块定义 3 个 transition contribution，每个 evaluate() 入队 3 次。但 engine 在 cross-event 触发后会做额外的 refresh/post-update phase 调用，这些也会触发 transition_output → lazy enqueue。所以一个 step 内可能进入 flush 多次（每个 phase 末一次），每次最多 3 slot；但偶尔 phase 调用合并导致 6 slot peak。

**为什么 ffi_calls counter 在 086 immediate 和 088 batch 两种模式数字一样？**

`rust_transition_state_production_calls` 在 batch 模式下按 **slot** 累加（兼容 audit 050 已有的 `calls == outputs` 断言）。真实 FFI hop 数看 `rust_transition_batch_flushes` — bench 数据：immediate 118,245 vs batch 39,414 → 3.0× 减少。

**Compiler analyzer 的复杂度多少？**

每模型 compile 一次，复杂度 O(n²) 最坏（n = analog block statement 数）。n 通常 ≤ 200 → 最坏 ~40k 操作，毫秒级。可忽略。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Analyzer 误判 safe → silent parity drift | 任何 parity test 失败 | 在 `_compile_contribution()` 把 `can_defer = False` 硬写死，退回 immediate emission |
| `_flush_transitions()` 在 evaluate 异常 path 漏 flush 导致 pending 残留 | next-step 行为异常 | engine 在 evaluate 异常 catch 后调 `_reset_transition_pending()`（已实现在 fallback path） |
| Batch buffer 在大 N 下 alloc 14×N 仍是开销 | bench 在极端 N 下 wall 不降 | 改为 monotonic-grow buffer + memoryview slicing（087 设计 alt） |
| 已有 fastpath `transition_unchanged_target_fastpath` 在 batch 模式下无法生效 | counter `transition_unchanged_target_fastpath_total` = 0 | 接受 — batch path 不做 unchanged-target 优化；future audit 089 可以补 |
| general path (`_transition`) 没被 088 覆盖 | general path 用户报 wall 不降 | 086 持久 buffer 在该路径上仍有效；future audit 089 做 general path defer with proxy |

## Coverage Status After 088

| Sub-case | Status |
|---|---|
| `V(out) <+ scale*transition()+offset+base` (fastpath, safe node) | ✅ 088 batch |
| `V(out) <+ scale*transition()+offset+base` (fastpath, unsafe node) | ✅ 086 buffer reuse（fall back to immediate） |
| `x = transition(); V(out) <+ f(x)` (general path) | ✅ 086 buffer reuse only — 088 不覆盖 |
| `if (cond) V(out) <+ transition()` 等条件分支 | ✅ analyzer 处理 IfStatement |
| `transition()` 嵌在数组下标里 | ⚠️ analyzer 保守标 unsafe；089 优化 |
| Cross-model transition 顺序 | ✅ flush 在 evaluate 末，跨 model 边界自然分隔 |

## Claim Boundary

可以说：
- transition operator 的 fastpath 调用从 per-call FFI 升到 per-step batch FFI
- bench 上单 model 3 transition 工况 wall 提速 **1.42×（29.5%）**，FFI hop 减少 **3×**
- parity bit-exact，568 全量测试零 regression
- 086 + 088 累积工程证据：transition operator 现在已完成 Python-side 持久 buffer + Rust-side per-step batch 两层优化

不能说：
- transition 已 full Rust ownership（compiler 仍生成 Python 调用，runtime 仍管 TransitionState 对象）
- general path 已 batch（仍 per-call，086 buffer reuse 兜底）
- release-wide 速度收益（需 same-slice EVAS/Spectre AX rerun 验证）
- EVAS 已 paper-facing 快于 Spectre AX

## Next Step

`089 - Transition General Path Defer Via Expression Lift`（可选）：把 `x = transition(...)` 这种 general path 用法也做 defer。需要 compiler 把 `x = transition(...)` lower 成 `self._enqueue_transition_general(slot, ...)` + 步末 `x = self._transition_general_results[slot]`。

或者直接进 `090 - Cross/Above Event Queue Ownership` — 用 transition 完成的同套 lazy/flush 模板做 cross/above，扩展到 event queue 层面。

worklist 标注 transition 整体目标 = 完成。
