# 094j - Event Statement Shadow Dispatch

Status: `partial` (single event-statement shadow dispatch; no production engine integration)

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `094g-event-body-program.md`
- `094i-mixed-event-due-runtime.md`
- `../STAGE_2_4_EXECUTION_PLAN.md`

## One-Line Summary

新增 `RustEventStatementRuntime`，把 094i 的 fired trigger indices 与 094g 的 Rust body write-set batch 接起来：当一个 event statement 的任意 trigger fired 时，Rust body batch 执行一次。该路径仍是 test/shadow-only，不接 production engine，也还没有 real-row waveform parity。

## Why This Exists

之前已经有两块：

```text
094g: EventStatementIR body -> Rust body write-set batch
094i: EventDueProgram -> source-order fired trigger indices
```

但真正的 event statement 行为是两者的组合：

```verilog
@(cross(...) or timer(...)) begin
    q = q + 1;
    V(out) <+ q;
end
```

如果 `cross` 和 `timer` 在同一步同时触发，这个 event statement 的 body 应执行一次，而不是按 trigger 数量执行多次。本 audit 用 shadow runtime 锁住这个规则。

## What Changed

EVAS:

| File | Change |
|---|---|
| `evas/simulator/event_due_runtime.py` | 新增 `RustEventStatementRuntime` |
| `tests/test_audit_094h_event_due_program.py` | 增加 simultaneous cross+timer trigger 时 body 只执行一次的测试 |

Supported shadow subset:

| Behavior | Status |
|---|---|
| one `EventStatementIR` | supported |
| combined event due check | supported through `RustEventDueRuntime` |
| Rust body write-set execution | supported through `RustBackend.evaluate_body_ir()` |
| simultaneous triggers | body executes once for the event statement |

Still missing:

| Missing piece | Why it matters |
|---|---|
| multiple event statements in one analog block | global source-order interleaving not represented here |
| non-event continuous statements after event body | engine phase ordering still Python-owned |
| control-flow/array/system-task event bodies | 094f body encoder still conservatively rejects them |
| real-row waveform parity | not run yet |
| production dispatch | not changed |

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094h_event_due_program.py -q
# 5 passed
```

Tested Verilog-A shape:

```verilog
@(cross(V(clk) - 0.5, +1) or timer(1n, 2n)) begin
    q = q + 1;
    V(out) <+ q;
end
```

Shadow result:

| Step | Fired trigger indices | `q` | `out` |
|---|---|---:|---:|
| `t=0` | `()` | `0` | `0` |
| `t=1ns` | `(0, 1)` | `1` | `1` |
| `t=3ns` | `(1,)` | `2` | `2` |

The `t=1ns` row is the important case: both cross and timer fired, but the body ran once.

## Claim Boundary

**可以说**：

- 单个 event statement 的 due check 和 Rust body batch 已经能在 shadow runtime 中串起来。
- simultaneous trigger 不会重复执行同一个 event statement body。

**不能说**：

- EVAS production event scheduler 已切到 Rust。
- 多 event statement / continuous statement phase-order 已完成。
- real benchmark waveform parity 已证明。
- 当前改动带来速度提升。

## Next Step

094k 应提升到 analog block 级 shadow：

1. 扫描 `BlockIR` 中多个 event statements，建立 source-order event statement runtime 列表。
2. 每个 step 收集 fired event statement，再按 analog block 源码顺序执行对应 Rust body batch。
3. 保守拒绝 event/continuous interleaving 尚不明确的 case。
4. 做 Python-oracle parity，再进入 real-row waveform shadow parity。
