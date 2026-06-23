# 094i - Mixed Event Due Runtime Shadow

Status: `partial` (shadow fired-index runtime; no event body production dispatch)

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `094h-event-due-program.md`
- `094g-event-body-program.md`
- `../STAGE_2_4_EXECUTION_PLAN.md`

## One-Line Summary

新增 `RustEventDueRuntime` shadow runtime，把 094h 的 trigger expression batch 接到已有 Rust `cross_detector_step` / `above_detector_step` / `timer_periodic_step` / `timer_absolute_step` primitives，并返回本步 fired trigger indices（按源码 trigger 顺序）。该 runtime 仍不接 production engine，不执行 event body，不做 real-row waveform claim。

## Why This Exists

event Rust 化不是只会算表达式就够了。真正要替代 Python event scheduler，至少需要这条链：

```text
EventDueProgram
  -> Rust batch evaluate trigger/timer expressions
  -> Rust detector/timer state update
  -> fired trigger indices in source order
  -> Rust event body write-set batch
```

094h 完成前两步。本 audit 完成第三步的 shadow-only 版本，用来验证 mixed `initial_step / cross / above / timer` 的 fired index 口径，而不是直接改生产仿真。

## What Changed

EVAS:

| File | Change |
|---|---|
| `evas/simulator/event_due_runtime.py` | 新增 `RustEventDueRuntime` |
| `evas/simulator/schedule_ir.py` | `above(expr, direction)` 的 direction 进入 `EventDueTriggerProgram` |
| `tests/test_audit_094h_event_due_program.py` | 增加 mixed due runtime source-order fired-index test |

Supported shadow subset:

| Behavior | Status |
|---|---|
| `initial_step` fired marker | supported when caller passes `initial_step=True` |
| `cross(expr, direction, ttol, vtol)` | supported through Rust detector primitive; tolerance expressions evaluated conservatively |
| `above(expr, direction?)` | supported through Rust detector primitive |
| static `timer(start)` | supported through Rust absolute timer primitive |
| static `timer(start, period)` | supported through Rust periodic timer primitive |
| source-order fired indices | supported by returning sorted source trigger indices |

Still missing:

| Missing piece | Why it matters |
|---|---|
| production engine integration | current runtime is test/shadow-only |
| event body execution by fired index | 094g body program exists, but not connected here |
| same-time cross/timer interpolation ownership | engine still owns waveform interpolation and body-read semantics |
| real-row waveform parity | not run yet |
| speed claim | no production path changed |

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094h_event_due_program.py -q
# 4 passed
```

Tested Verilog-A shape:

```verilog
@(initial_step or cross(V(clk) - 0.5, +1) or above(V(inp) - 0.2) or timer(1n, 2n))
    q = q + 1;
```

Shadow fired indices:

| Step | Inputs | Fired trigger indices |
|---|---|---|
| `t=0`, `initial_step=True` | `clk=0.0`, `inp=0.0` | `(0,)` |
| `t=1ns` | `clk=0.75`, `inp=0.1` | `(1, 3)` |
| `t=2ns` | `clk=0.75`, `inp=0.5` | `(2,)` |
| `t=3ns` | `clk=0.75`, `inp=0.5` | `(3,)` |

## Claim Boundary

**可以说**：

- 094i 已经有 shadow-only mixed event due runtime。
- trigger expression batch、cross/above detector primitive、timer primitive 可以串成 fired-index 输出。
- fired indices 按源码 trigger 顺序返回，便于下一步连接 event body write-set。

**不能说**：

- EVAS production event scheduler 已由 Rust 替代。
- event body 已经自动由 Rust runtime 执行。
- real benchmark waveform parity 已经证明。
- 当前改动带来速度提升。

## Next Step

094j 应连接 fired trigger index 与 094g `EventBodyProgram`，先做 shadow execution：

1. 一个 `EventStatementIR` 对应一个 `EventDueProgram + EventBodyProgram`。
2. `RustEventDueRuntime.step()` 返回 fired index 后，只执行匹配 event 的 Rust body batch。
3. 对 simple cross/timer event body 做 Python-oracle parity。
4. 再上真实 row waveform shadow parity。
