# 055 - Event/Lifecycle Production Gate

Status: `diagnostic`

Date: `2026-06-04`

Code commit: `pending`

Related documents:

- `049-behavior-coverage-manifest.md`
- `051-timer-step-rust-primitives.md`
- `052-cross-above-detector-rust-primitives.md`
- `054-dynamic-bus-offset-rust-primitive.md`
- `../behavior-coverage-map.v1.json`

## One-Line Summary

B10 event body execution 和 B18 full lifecycle 不能作为独立小 patch 并行硬切 production：它们共同拥有 EVAS 每步 phase order、事件触发后的 state/output side effects、timer/cross/refine 反馈和 final trace 语义；当前只能继续做 shadow/parity 和分段 primitive，不能声明 full Rustified。

## Current Status After 050-054

| Behavior | Current state | Why not production yet |
|---|---|---|
| B08 transition state | Rust typed-array primitive exists | engine production path still Python |
| B09 cross/above detect | Rust typed-array primitive exists | event order, interpolation side effects, event body still Python |
| B10 event body | Python-only | event body can write arbitrary state/output/timer/transition side effects |
| B11 timer due/reschedule | Rust typed-array primitive exists | timer event body/lifecycle still Python |
| B15 record trace | indexed node-id read path exists | list append/SimResult/CSV/checker contract still Python/Numpy |
| B17 dynamic bus | Rust base+offset primitive exists | compiler/runtime still use string resolver/cache |
| B18 lifecycle executor | not implemented | depends on B08/B09/B10/B11/B15/B17 production ownership |

## Why B10/B18 Are Coupled

EVAS 的每一步不是简单地“evaluate 一次模型”。它大致是：

```text
prepare_step
evaluate
transition/timer/cross detection
event body/post_update
refresh_outputs
refine/dt decision
record
```

B10 event body 会改变：

- `self.state` and `self.arrays`
- `output_nodes` and `node_voltages`
- timer state and last-fired state
- transition target/state through later evaluate calls
- cross interpolation context via `_event_time` and `_event_node_cross_directions`

B18 lifecycle executor 如果只迁一部分，就容易出现两类错误：

```text
Python 已执行 event body，Rust 又执行一遍
Rust 提前/延后执行 event body，导致 record/refine/transition 状态不同
```

这会直接破坏 EVAS/Spectre parity，不是性能问题。

## Safe Next Cut

下一步应该先做 shadow，而不是 production：

| Step | Goal | Pass condition |
|---|---|---|
| 056 event due trace shadow | Rust 只输出同一步内哪些 cross/above/timer due，以及候选 event time | 与 Python `_check_cross/_check_above/_check_timer*` 逐步一致 |
| 057 event ordering shadow | Rust 对 due events 做 stable chronological order trace | 与 Python retrograde suppression / source-order fallback 一致 |
| 058 event body write-set audit | Python event body 执行后记录 state/output/timer/transition write-set | 能判断哪些 event body 可无副作用 batch，哪些必须 fallback |
| 059 lifecycle shadow executor | Rust 只模拟 phase graph decision，不写 production state | 与 engine counters/trace 完全一致 |
| 060 opt-in production gate | 只对静态可证明的 event-free 或 side-effect-bounded segment 跳过 Python | examples/full regression + EVAS/Spectre audited slice parity |

## Claim Boundary

050-054 已经把多个核心 primitive 做出来，但不能说“所有 Python EVAS 已转 Rust”。更准确的口径是：

```text
EVAS 正在把 Python dict/string/object hot path 拆成 typed-array Rust primitives。
目前已有 transition/timer/cross/above/dynamic-bus offset 等 primitive parity，
但 event body 和 full lifecycle 仍由 Python 拥有。
```

这也是为什么当前不能把 B10/B18 拆给多个 agent 各自 production 修改：它们共享同一个 phase-order correctness gate。
