# 094k - Analog Block Event Shadow Dispatch

Status: `partial` (source-ordered event statement shadow; no continuous-statement production integration)

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `094j-event-statement-shadow-dispatch.md`
- `../STAGE_2_4_EXECUTION_PLAN.md`

## One-Line Summary

新增 `RustAnalogBlockEventRuntime`，把多个 `RustEventStatementRuntime` 按 analog block 源码顺序串起来。多个独立 event statement 在同一步 fired 时，runtime 按源码顺序执行各自 Rust body batch。该路径仍是 test/shadow-only，不处理 non-event continuous statements，不接 production engine。

## Why This Exists

094j 只证明了一个 event statement 的 due/body 组合。真实 analog block 常见结构是：

```verilog
analog begin
    @(cross(...)) q = q + 1;
    @(timer(...)) begin
        q = q + 1;
        V(out) <+ q;
    end
end
```

如果两个 event statement 同一步 fired，EVAS 必须保持源码顺序，否则 state write 和 output write 会错位。本 audit 用 shadow runtime 锁住这层 ordering。

## What Changed

EVAS:

| File | Change |
|---|---|
| `evas/simulator/event_due_runtime.py` | 新增 `RustAnalogBlockEventRuntime` |
| `tests/test_audit_094h_event_due_program.py` | 增加两个独立 event statement 同步触发的 source-order test |

Supported shadow subset:

| Behavior | Status |
|---|---|
| multiple event statements in one block | supported through ordered runtimes |
| per-statement Rust due/body execution | supported via 094j runtime |
| same-step source-order body execution | supported |

Still missing:

| Missing piece | Why it matters |
|---|---|
| interleaved continuous contributions | real `model.evaluate()` mixes event and non-event work; phase-order must be audited |
| nested control flow / loops / arrays | current body encoder still rejects many general cases |
| real-row waveform parity | not run yet |
| production engine integration | not changed |
| speed claim | no production path changed |

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094h_event_due_program.py -q
# 6 passed
```

Tested Verilog-A shape:

```verilog
@(cross(V(clk) - 0.5, +1)) q = q + 1;
@(timer(1n, 2n)) begin
    q = q + 1;
    V(out) <+ q;
end
```

At `t=1ns`, both statements fired. Source-order execution produced:

| Fired statement indices | `q` | `out` |
|---|---:|---:|
| `(0, 1)` | `2` | `2` |

If statement order were wrong or if the first body were skipped, `out` would not observe `q=2`.

## Claim Boundary

**可以说**：

- 多个 event statement 的 shadow runtime 可以按 analog block 源码顺序执行 Rust body batch。
- same-step event statement ordering 已有单元级 parity test。

**不能说**：

- 完整 analog block `evaluate()` 已 Rust 化。
- continuous contribution / event / transition phase-order 已完成。
- production engine 已使用该 runtime。
- 当前改动带来速度提升。

## Next Step

094l 应该进入真实 waveform shadow gate：

1. 选择只含 supported event statements 的小模型，构造 Python generated evaluator 与 094k shadow runtime 的 step-by-step parity。
2. 加入 non-event continuous contribution 的保守识别：能安全排序则纳入，不能则 fallback。
3. 通过真实 row waveform parity 后，才考虑 opt-in production dispatch。
