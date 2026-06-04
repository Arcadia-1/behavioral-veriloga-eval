# 084 Multi-Timer Static-Linear Event Queue Rust

## 核心结论

这一轮把 082 的单 periodic timer whole-segment executor 扩展成 multi-timer Rust queue：

```text
multiple periodic timer(start, period)
-> chronological due queue
-> same-time events execute in compiler/source metadata order
-> state-only static-linear event body
-> non-event static-linear output evaluate
-> explicit-record trace with timer breakpoints
```

也就是说，命中 gate 的模型不再只能有一个 `timer(start, period)`。多个周期 timer 可以在同一个 Rust FFI 里完成 due 判断、事件排序、event body 写 state、output evaluate 和 record trace。

这仍然不是全量 event queue Rust 化。它覆盖的是多个周期 timer 加简单线性 event body 这一类保守子集，不覆盖 `cross()` / `above()` interpolation、`transition()`、动态数组、节点读取 event body、state-owned absolute timer 或默认 adaptive trace。

## 改造原理

原来的 082 Rust path 只有一个 `next_fire`：

```text
while next_fire <= t:
  run one timer body
  next_fire += period
```

这轮改成 `next_fires[]`：

```text
for each output time t:
  while any next_fires[i] <= t:
    fire_time = min(next_fires)
    for timer i whose next_fires[i] == fire_time in metadata order:
      run timer i event body
      next_fires[i] += period_i
  update source values at t
  evaluate continuous output
  record requested node ids
```

关键语义是两个：

| 语义 | Rust 实现 |
|---|---|
| 时间顺序 | 每次选择最早 `next_fire`，所以事件按仿真时间推进 |
| 同时刻顺序 | 同一个 `fire_time` 上按 compiler metadata 顺序执行，对应 Verilog-A 源码收集顺序 |

event body 仍然使用 static-linear IR：

```text
target = bias + sum(gain_i * source_i)
```

如果第二个 timer 读取第一个 timer 刚写过的 state，例如：

```text
@(timer(0, 1n)) acc = acc + 1;
@(timer(0, 1n)) acc = 2 * acc;
```

Rust 会先执行 `acc + 1`，再执行 `2 * acc`，所以每个 1 ns tick 的结果是 `1 -> 4 -> 10 -> 22`，与 Python event 顺序一致。

## Production Gate

当前 multi-timer path 只在以下条件同时满足时启用：

| Gate | 原因 |
|---|---|
| exactly one model | 跨 model hierarchy、parent/child node sync 尚未进入这个 segment |
| no child models | child lifecycle/order 仍由 Python path 拥有 |
| one or more periodic `timer(start, period)` | 本轮支持 multi periodic timer，但不支持 state-owned absolute timer |
| explicit `record_step` | Rust trace 以 fixed record grid 加 timer breakpoints 为输出 contract |
| non-negative timer start and positive period | 负 start / 非周期 timer 语义先 fallback |
| event body target 只写 state | output write、transition target、文件/随机 side effect 仍 fallback |
| event body 不读 node | 避免 event-time source sampling 或 crossing-time interpolation 语义错误 |
| evaluate target 只写 node | continuous contribution 可以直接进入 node array |
| event/evaluate 都是 static-linear IR | 非线性、动态数组、复杂 control flow 继续走 Python |

## 改动内容

| 文件 | 改动 |
|---|---|
| `EVAS/evas/rust_core/src/lib.rs` | 新增 `timer_static_linear_queue_trace_for_arrays()` 和 C ABI `evas_rust_timer_static_linear_queue_trace()` |
| `EVAS/evas/simulator/rust_backend.py` | 新增 `RustBackend.timer_static_linear_queue_trace()` wrapper |
| `EVAS/evas/simulator/engine.py` | `_try_timer_static_linear_fastpath()` 支持多个 timer；单 timer 保留 082 旧 ABI，多 timer 走新 queue ABI |
| `EVAS/tests/test_engine.py` | 新增 multi-timer regression，验证同一时刻 source-order event body parity |
| `EVAS/tests/test_rust_backend.py` | 新增 Rust backend wrapper 直接测试，验证 multi-timer order、event count 和 final state |
| `behavior-coverage-map.v1.json` | 增加 `evas_rust_timer_static_linear_queue_trace` 覆盖项，并更新 B11 fallback 口径 |

## 正确性边界

这轮明确没有迁移下面这些行为：

| 行为 | 当前状态 |
|---|---|
| `cross()` / `above()` production event queue | 仍需要 crossing-time interpolation 和 detector state 一起迁 |
| event body 读 node | 仍 fallback，避免 event-time source value 语义错误 |
| event body 写 output | 仍 fallback，避免离散 output write 和 continuous contribution 顺序不清 |
| `transition()` target/state/output | 仍由 Python 或专用 whole-segment path 拥有 |
| state-owned absolute timer `timer(t_next)` | 仍由现有 Python fast path 或 fallback 拥有 |
| default adaptive/internal trace | 仍需要 err-ratio scan、breakpoint refine、internal point emission 进入 Rust |
| dynamic arrays/buses | B17 primitive 已有，但这个 segment 尚未合并动态 offset |

补充审计：本轮尝试过把 event body 里的 `V(out) <+ ...` 纳入 queue，但 parser/compiler 直接按 Spectre 规则拒绝该写法，对应 VACOMP-2157 类限制。也就是说，event body contribution 不是我们应该为 paper-facing Spectre-aligned EVAS 扩展的有效通用子集；后续应继续采用“event body 更新 state，unconditional analog contribution 输出 state”的规范写法。

## 验证结果

```text
cargo test --manifest-path EVAS/evas/rust_core/Cargo.toml --release
31 passed
```

```text
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_rust_backend.py -q
33 passed
```

```text
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -k 'timer or event_write or static_eval or whole_model' -q
48 passed, 191 deselected
```

Targeted parity 内容：

| 测试 | 覆盖 |
|---|---|
| `timer_static_linear_queue_preserves_same_time_source_order` | Rust core safe API，两个同周期 timer 同时触发，验证 event order |
| `test_rust_backend_timer_static_linear_queue_trace_preserves_order` | Python ctypes wrapper，验证 flat trace、event count、final state |
| `test_rust_full_model_multi_timer_static_linear_queue_preserves_order` | Parser/compiler/engine 真实路径，验证 Python default 与 Rust fastpath waveform parity |

## 速度影响判断

这轮减少的是多 timer 模型里每个 record/breakpoint 时间点的 Python 事件循环开销：

| 开销 | 原路径 | 新路径 |
|---|---|---|
| 找 due timer | Python 逐 event helper/object check | Rust `next_fires[]` min scan |
| 同时刻排序 | Python event list 顺序 | Rust metadata order |
| event body | Python assignment dispatch | Rust static-linear op batch |
| output evaluate | Python generated model evaluate | Rust static-linear op batch |
| record | Python node/value loop | Rust trace matrix fill |

这次没有新增 release-wide 速度 claim，因为是否加速取决于 benchmark 中有多少模型命中这个 gate。它的价值是把 B11/B10/B18 的 generic timer segment 从单 timer 扩成 multi-timer，为后续 cross/above/transition queue 迁移打好 ordering contract。

## 对全量 Rust 化完成度的影响

如果把“能跑通当前 EVAS 支持的所有 benchmark 行为并且主要热循环都在 Rust”记为 100%，这轮仍不能大幅提高 release-wide 百分比。原因是它扩大了 generic timer segment 的语义覆盖，但还没有重跑 release-wide coverage manifest，也没有覆盖 cross/above/transition/dynamic array 等大块行为。

可以更准确地说：

| 口径 | 当前结论 |
|---|---|
| top-wall 已有专用 whole-segment fastpath | 已经证明能显著加速部分重 row |
| generic event/timer Rust 化 | 从单 periodic timer 扩到 multi periodic timer 的 static-linear 子集 |
| release-wide 全量 Rust 化 | 仍不能 claim；上一轮 manifest 口径约 `30.0%`，需要重跑后才可更新 |

## 下一步

1. 把 `cross()` / `above()` due、interpolation、event body、record 合成一个 shadow queue，再决定 production gate。
2. 把 event-owned output write 纳入 queue executor，固定离散 output write 与 continuous contribution 的先后关系。
3. 把 `transition()` target/state evolution/output record 合进 typed-array loop。
4. 把 default adaptive trace 的 err-ratio scan、breakpoint refine 和 internal-point emission 迁入 Rust，减少 fixed `record_step` 限制。
