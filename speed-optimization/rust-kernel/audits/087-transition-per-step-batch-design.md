# 087 - Transition Per-Step Batch Design

Status: `planned`（design-only；implementation 在 088）

Date: `2026-06-05`

Code commit: `n/a`（本 audit 不动代码）

Related documents:

- `050-transition-state-rust-primitive.md`
- `085-cross-above-transition-default-adaptive-trace.md`
- `086-transition-operator-persistent-buffer-reuse.md`
- `../RUSTIFICATION_WORKLIST_20260605.md`

## One-Line Summary

设计 transition operator 从 per-call FFI 升到 per-step batch FFI 的完整 compiler + runtime 方案，覆盖 fastpath（`_transition_output`）和 general path（`_transition` 返回值入表达式）两条 codegen 路径，包含 intra-evaluate self-read 静态分析、deferred placeholder 调度、和 fallback 策略；实现见 audit 088。

## Why Design-First

087 涉及四层联动（compiler / runtime / engine / 静态分析新 pass），任何一层接口写歪都会导致 088 实现期反复重做。因此把契约先在 087 固定下来，088 只做机械实现 + 测试，risk 可控。

## 现状回顾

After 086：
- transition 的 Rust 数学 primitive 已就位（`evas_rust_transition_state_step` + 14-typed-array contract）
- Python 端 buffer 已持久化（086 把 alloc 从 326k 降到 14）
- **但 FFI 仍是 per-call**：每个 `_transition()` 调用一次 ctypes hop。一个 transition-heavy row 一次 simulation 仍有 ~10k–100k 次 ctypes 调用

087 目标：把 N 次 per-step FFI 合成 1 次 FFI。预期收益：在 086 之上额外 ~10-25%。

## Architecture（087 + 088 完整方案）

```
┌──────────────────────────────────────────────────────────────────────┐
│ L1 AST            unchanged                                          │
├──────────────────────────────────────────────────────────────────────┤
│ L2 Compiler       changes:                                           │
│                   - 新增 static analyzer pass: detect intra-evaluate │
│                     self-read of transition output nodes             │
│                   - 标记每个 transition() call site:                  │
│                     {can_defer: bool, batch_slot_idx: int}           │
│                   - codegen 两种路径分别 emit deferred form:          │
│                     · fastpath  → self._transition_output_lazy(...)  │
│                     · general   → self._transition_lazy(...)         │
│                   - emit 末尾追加 self._flush_transitions()           │
│                   - 不可 defer 的 call site 保持原 emit               │
├──────────────────────────────────────────────────────────────────────┤
│ L3 Runtime        new methods:                                       │
│                   - _transition_output_lazy(node, key, time, target, │
│                       base, offset, scale, delay, rise, fall, nv,    │
│                       slot_idx)                                      │
│                     入队 (node, key, target, delay, rise, fall) +    │
│                     占位写 nv[node]=0.0（被覆盖）                     │
│                   - _transition_lazy(slot_idx, key, time, target,    │
│                       delay, rise, fall) → returns float             │
│                     general path 仍需返回值，所以是 micro-batch:      │
│                     若所有 lazy slot 已收集 → flush 后返回，否则      │
│                     仍然 immediate per-call（fallback）               │
│                   - _flush_transitions()                             │
│                     收集所有 pending slot，单次 batch FFI，按入队顺序  │
│                     回写 nv 和 output_nodes，更新所有 perf counters   │
│                   - 持久 typed-array buffer 从 086 的 size-1 升级到   │
│                     size-N（N = 编译时已知的 transition 数量上限）    │
├──────────────────────────────────────────────────────────────────────┤
│ L4 Rust core      unchanged                                          │
│                   evas_rust_transition_state_step 已支持 state_count │
│                   batch — 这是 086 没用上的能力，087 兑现             │
└──────────────────────────────────────────────────────────────────────┘
```

## Static Analyzer 设计（087 核心创新点）

### 问题

Verilog-A 允许同一个 analog block 内**先写 V(out) 再读 V(out)**：

```verilog
analog begin
    V(out1) <+ scale * transition(target_a, 0, 1n, 2n);  // 写 out1
    x = V(out1);                                          // 读 out1 ← self-read
    V(out2) <+ scale * x;
end
```

如果把第 1 行 defer 到 evaluate 末，第 2 行读到的是上一步旧值 → parity 直接挂。

### 算法

新加 compiler pass `TransitionDeferralAnalyzer`，在 `_compile_module()` 内、`_compile_statement()` 之前运行一次。流程：

```python
class TransitionDeferralAnalyzer:
    def analyze(self, analog_block_stmts):
        # 1. 第一遍：收集所有 transition contribution 的 LHS 节点
        transition_output_nodes = set()
        for stmt in walk(analog_block_stmts):
            if isinstance(stmt, Contribution) and contains_transition(stmt.expr):
                transition_output_nodes.add(stmt.branch.node1)

        # 2. 第二遍：对每个 contribution，记录其位置；
        #    然后检查后续 statements 里是否有 BranchAccess(V, node) 引用同一节点
        unsafe_nodes = set()
        for i, stmt in enumerate(analog_block_stmts):
            if isinstance(stmt, Contribution) and contains_transition(stmt.expr):
                node = stmt.branch.node1
                # 在 [i+1, end] 范围内扫描所有 expr 子树
                for later in analog_block_stmts[i+1:]:
                    if has_voltage_read(later, node):
                        unsafe_nodes.add(node)
                        break

        # 3. 返回每个 transition call site 的 can_defer flag
        return {
            id(call): (node not in unsafe_nodes)
            for node, call in transition_call_sites
        }
```

### 边界情况

| Case | 处理 |
|---|---|
| `if/else` 内的 transition | 静态分析 emit 时也走 if 分支，slot_idx 按 control flow path 分配；如果同一节点在两条分支里都被写，仍按节点级别决定 defer 性 |
| `for/while` 内的 transition | 循环展开是动态的 → 保守标记 unsafe（不 defer） |
| `V(out, vss)` 多端口 | 只看 node1（第一个端口），跟 fastpath 现有逻辑一致 |
| `V(out)` 通过 `_event_trace_audit` 的隐式读 | 不算 self-read（audit 只是记录，不返回值给表达式） |
| `_set_output(node, expr, nv)` 后续路径读 nv[node] | 已不属于本次 contribution；不算 |
| Cross-model：其它模型的 evaluate 读这个 node | 不在本 analyzer scope（model 边界 = flush 边界） |
| Nested transition：`transition(transition(...))` | Verilog-A 不允许；parser 拒绝 |

### 复杂度

每个 model 编译一次。一个 analog block 通常 ≤200 statements，self-read 扫描 O(n²) 最坏 ~40k 操作，毫秒级。可忽略。

## Codegen 改动（088 实现）

### Fastpath（line 10731）

**Before:**
```python
return [
    f"{prefix}self._transition_output({node!r}, {key_expr}, time, "
    f"{target}, {base}, {offset}, {scale}, {delay}, {rise}, {fall}, nv)"
]
```

**After:**
```python
if can_defer:
    slot_idx = self._alloc_transition_slot(key_expr)
    return [
        f"{prefix}self._transition_output_lazy({slot_idx}, {node!r}, {key_expr}, time, "
        f"{target}, {base}, {offset}, {scale}, {delay}, {rise}, {fall}, nv)"
    ]
else:
    return [...原 emission...]
```

### General path（line 11271）

**Before:**
```python
return f"self._transition({key_expr}, time, {target}, {delay}, {rise}, {fall})"
```

**After:**
```python
if can_defer:
    slot_idx = self._alloc_transition_slot(key_expr)
    return f"self._transition_lazy({slot_idx}, {key_expr}, time, {target}, {delay}, {rise}, {fall})"
else:
    return f"self._transition({key_expr}, time, {target}, {delay}, {rise}, {fall})"
```

### Evaluate body 末尾

**Compiler emit 末尾追加：**
```python
self._flush_transitions(nv)
```

放在 `_compile_module()` 里 evaluate 方法 emit 的最后。

## Runtime 数据结构

### Backend 持久 buffer 升级

086 持久 buffer 是 size-1。087 改成 size-N（N = compile-time 已知的 transition slot 总数）。

```python
def _ensure_rust_transition_buffers(self, capacity):
    if (self._rust_transition_buffers is None
        or len(self._rust_transition_buffers['current']) < capacity):
        N = max(capacity, 16)  # 初始 ≥16 避免频繁扩容
        self._rust_transition_buffers = {
            'current': array("d", [0.0] * N),
            'target':  array("d", [0.0] * N),
            # ... 14 个 ...
        }
```

### Per-step queue

```python
# 在 backend.__init__:
self._transition_pending_count = 0
self._transition_pending_nodes = []  # 顺序记录要回写 nv 的节点
self._transition_pending_keys = []
self._transition_pending_targets = []  # 直接进 input_targets buffer
# ... 等等
```

每个 model 一份 queue。step 之间 reset。

### Flush

```python
def _flush_transitions(self, nv):
    n = self._transition_pending_count
    if n == 0:
        return
    bufs = self._rust_transition_buffers
    # 把 pending data 拷进 buffer 前 n 个 slot（已在 lazy 调用时写入）
    # 调一次 Rust batch:
    backend.transition_state_step(
        bufs['current'][:n], bufs['target'][:n], ...,
        float(time), float(self.default_transition),
        bool(self._initial_condition_mode),
    )
    # 按顺序回写 nv 和 output_nodes
    for i in range(n):
        node = self._transition_pending_nodes[i]
        value = float(self._transition_pending_base[i]) + ... + scale * bufs['output'][i]
        nv[node] = value
        self.output_nodes[node] = value
        # 更新 TransitionState 对象
        ts = self.transitions[self._transition_pending_keys[i]]
        ts.current_val = bufs['current'][i]
        # ... 等等
    # reset
    self._transition_pending_count = 0
```

## Counter 语义

087 之后 perf stats 含义：

| Counter | 旧含义 | 新含义 |
|---|---|---|
| `transition_calls` | 每次 `_transition()` 调用 +1 | 不变（包含 lazy 路径） |
| `rust_transition_state_production_calls` | 每次 ctypes FFI hop +1 | 每次 flush +1（远少于 transition_calls） |
| `rust_transition_state_production_outputs` | 每次 FFI 输出值 +1 | 每次 flush 时 += pending_count |
| `transition_evaluate_calls` / `transition_set_target_calls` | per call +1 | 不变（在 lazy 时也累计） |
| **新** `rust_transition_batch_flushes` | n/a | flush() 调用总数 |
| **新** `rust_transition_batch_avg_slots` | n/a | flushes / 总 slot |
| **新** `rust_transition_lazy_fallbacks` | n/a | general path 拿不到 batch 返回值时的回退次数 |

## Cache 失效

EVAS 缓存 compile 过的 model class。087 改 codegen → 缓存失效。处理：

```python
# 在 _compile_module() 顶端加 version stamp:
self._codegen_version = "transition_batch_v1"
# 缓存 key 包含 version stamp，自动失效旧 class
```

或者更简单：每次 backend 升级 bump version 数字。

## Fallback Policy

| Scenario | Fallback |
|---|---|
| `_flush_transitions()` 时 Rust FFI 抛异常 | 落回 pending 列表里的每个 entry，对每个 entry 用 Python `TransitionState` 逐个执行（原 050 前路径），增加 `rust_transition_batch_fallbacks` |
| `_transition_lazy()` 被调用但不在 evaluate 上下文（理论不应发生） | 立即 fallback 到 `_transition()` |
| Compile 时 self-read 检测器 bug → 误判 unsafe | 没有 perf 风险，只是不 defer（保守）；safe |
| Compile 时 self-read 检测器 bug → 误判 safe | parity 风险高；用 088 测试覆盖广泛 contribution 模式来防 |

## Test Plan（088 implementation 必须覆盖）

| Test | 目的 |
|---|---|
| `test_transition_batch_parity_simple_fastpath` | 一个简单 `V(out) <+ scale*transition()`，batch 模式与 immediate 模式 waveform bit-exact |
| `test_transition_batch_parity_multi_output` | 同一 model 多个 `V(outN) <+ scale*transition()`，验证 batch 后 N 次 FFI 变成 1 次 |
| `test_transition_batch_self_read_detected` | `V(out) <+ transition(); x = V(out); V(out2) <+ x` → analyzer 标记 out 为 unsafe，第 1 行不入队 |
| `test_transition_batch_self_read_safe_when_no_dependency` | `V(out1) <+ transition(); V(out2) <+ transition()` 两条不相互读 → 两条都入队 |
| `test_transition_batch_initial_condition_mode` | initial_condition_mode 下 batch 行为正确 |
| `test_transition_batch_for_loop_conservative` | `for (i=0;i<N;i=i+1) V(out[i]) <+ transition(...)` → 全部标 unsafe，全部不入队（保守） |
| `test_transition_batch_general_path_lazy_returns_value` | `x = transition()` 路径 general lazy 拿到正确返回值 |
| `test_transition_batch_general_path_falls_back_on_self_read` | general path self-read 检测正确触发 fallback |
| `test_transition_batch_counter_consistency` | `transition_calls` 与 `rust_transition_state_production_calls` 比值符合预期 |
| `test_transition_batch_flush_on_evaluate_end` | flush 在 evaluate 退出时正确被调（即使有异常） |
| `test_transition_batch_works_with_unchanged_target_fastpath` | 已有 unchanged_target_fastpath 不被 batch 破坏（要么在 batch 内表达，要么禁用） |
| `test_transition_batch_works_with_transition_output_fastpath` | `_transition_output_lazy` 正确替换 `_transition_output` |
| `test_full_suite_no_regression` | 现有 568 tests 全过 |
| `test_audit_086_bench_still_works` | 086 bench 不应破坏（接口兼容） |

## Risk Register

| ID | Risk | Mitigation | Detection |
|---|---|---|---|
| R1 | Static analyzer 误判 safe → silent parity drift | 覆盖广泛的 contribution patterns 测试 | parity bit-exact assertion |
| R2 | Flush 时机错误（evaluate 异常 path 漏 flush） | 用 try/finally 包 evaluate 末尾 flush | regression test 故意抛异常 |
| R3 | Counter 语义变化破坏下游分析脚本 | 保留旧 counter 名 + 新增 `_batch_*` counter；audit 089 更新下游 | 跑 vabench 报告脚本检查输出 |
| R4 | Cache 失效不彻底导致老 class 跑新 runtime | 版本号 stamp + warn-on-mismatch | startup log + test |
| R5 | General path lazy 返回值实现复杂导致 fallback 率高 | 接受 fallback；如果 fallback 率 >50% 说明 general path defer 无收益，可以禁用 | counter 监控 |
| R6 | `transition_unchanged_target_fastpath` 不能在 batch 模式工作 | 在 batch 模式下临时禁用此 fastpath；如果它带来明显回归再单独 audit 089 实现 batch 兼容版 | counter `transition_unchanged_target_fastpath` 在 batch 模式应为 0 |

## Success Criteria（088 必须满足）

| KPI | 阈值 |
|---|---|
| 现有 568 pytest | 全过 |
| audit 086 bench parity | bit-exact unchanged |
| Fastpath batch FFI 数 | 在单 model 多 transition 测试上从 N → 1 per step |
| Wall delta on transition-heavy 单 model bench（086 bench 扩展） | ≥10% 进一步 faster vs 086 |
| Static analyzer false-positive 率（safe → unsafe）| 可接受（保守损失覆盖率，不影响 parity） |
| Static analyzer false-negative 率（unsafe → safe）| **0**（必须 0，否则 parity 挂） |
| `rust_transition_batch_fallbacks` 在 happy-path tests | 0 |

## Claim Boundary

可以说（087 done 时）：
- 完成了 transition operator 从 per-call 到 per-step batch 的 compiler + runtime 设计
- 明确了 fastpath 和 general path 的两种 deferral 策略
- 给出 static analyzer 算法 + edge case 处理
- 给出 088 的具体实现 checklist

不能说：
- transition operator 已经 batch 化（087 不写代码）
- 速度收益已经验证（要等 088）

## Next Step

`088 - Transition Per-Step Batch Implementation`：按 087 设计落地。预计 3-5 小时，分两个 commit：
- 088a：static analyzer pass + 单元测试
- 088b：codegen 改动 + runtime queue + flush + parity 测试 + benchmark

## What Is Not In 087/088 Scope

| Out of scope | Why |
|---|---|
| `cross()/above()` event queue Rust ownership | 是 089+ 的 cross/above batch audit |
| `timer()` 多 model 跨 model 调度 | 是 084 的扩展，跟 transition 无关 |
| record/CSV path 全 Rust | 是 D-track，不在 transition 整体目标里 |
| paper-facing speed claim | 必须等 same-slice EVAS/Spectre AX rerun |
| persistent worker production gate（worklist P0 087） | 跟 audit 087 编号撞了，但这是不同 worklist 概念上的 087，需要重新编号；下次 worklist 修订时处理 |
