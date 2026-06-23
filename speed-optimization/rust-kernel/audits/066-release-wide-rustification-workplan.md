# 066 - Release-Wide Rustification Workplan

Status: `active`

Date: `2026-06-04`

Code commit: `pending`

Related documents:

- `../behavior-coverage-map.v1.json`
- `048-python-to-rust-behavior-map.md`
- `049-behavior-coverage-manifest.md`
- `064-compiler-driven-whole-segment-lowering.md`
- `065-semantic-dataflow-whole-segment-matching.md`

## One-Line Summary

把后续 Rust 化从“零散优化点”整理成 release-wide backlog：目标覆盖 `/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks` 下 79 个 entry、357 个 gold Verilog-A 文件，并明确哪些工作能并行、哪些必须按 phase-order 顺序推进。

## Scope

| Item | Decision |
|---|---|
| 目标 benchmark | `benchmark-vabench-release-v1/tasks` 全量 release tasks |
| 当前规模 | 79 个 entry 目录，357 个 gold `.va` 文件 |
| 短期目标 | `rust_mode=auto` 下所有当前 EVAS 可仿 row 仍能跑通，Rust 不命中时安全 fallback Python |
| 中期目标 | top-wall 热路径进入 Rust production path，能看到真实 EVAS subprocess wall 下降 |
| 长期目标 | 主仿真 loop 从 Python dict/object path 迁到 Rust typed arrays |
| 非目标 | 为 Rust 化扩大到 EVAS 本来不支持的 KCL/KVL、晶体管、AC/DC、`I()<+`、`ddt/idt` 语义 |

## Why This Exists

前面 037-065 证明了一个很关键的事实：

```text
有 Rust ABI != 已经加速
有 shadow parity != production 已经接管
有单个模型 fastpath != release 全量可泛化
有 EVAS-only wall 下降 != paper-facing EVAS/Spectre speed claim
```

所以后续不能继续只补小 helper。每个改动必须先回答：

- 它覆盖 B01-B18 哪个仿真行为？
- 它是否能跳过 Python production path，而不是只做 shadow？
- 它是否减少每步成本、减少步数、或减少 record/checker 开销？
- 它在全 release manifest 中覆盖多少模型和多少 top-wall 时间？

## Coverage Levels

后续报告不要只写“Rust 化/未 Rust 化”，统一使用下面分级：

| Level | 名称 | 含义 | 能否算 Rust production |
|---|---|---|---|
| L0 | Python only | 行为完全由 Python 执行 | no |
| L1 | Metadata/IR only | compiler 能识别行为，但 runtime 仍 Python | no |
| L2 | Shadow only | Rust 旁路复算并比较，Python 仍拥有语义 | no |
| L3 | Opt-in production | 打开 flag 后 Rust 接管该 segment，失败 fallback Python | yes, but only opt-in |
| L4 | Auto production | 默认或 `rust_mode=auto` 安全启用 Rust，带 manifest gate | yes |
| L5 | Pure Rust loop | parser/compiler/runtime/record 主要都在 Rust | yes, long-term only |

当前总体状态接近 **L1-L3 混合**：有一些 Rust primitive 和 top-wall special executor，但通用 event/timer/transition/lifecycle 仍大量是 Python production path。

## Workstream Backlog

| ID | Workstream | 覆盖行为 | 主要修改位置 | 依赖 | 验收证据 | 预期收益 |
|---|---|---|---|---|---|---|
| W0 | Release behavior coverage manifest | B01-B18 全部 | `behavioral-veriloga-eval/runners`, `EVAS/evas/simulator/backend.py` counters | none | 79 entry / 357 gold model 都有 behavior/fallback/candidate row | 决定后续优先级 |
| W1 | Whole-segment Rust ABI contract | B03/B04/B06/B08/B10/B11/B15/B18 hot segments | `EVAS/evas/rust_core`, `EVAS/evas/simulator/rust_backend.py`, `engine.py` dispatch | 064/065 metadata | PRBS/CPPLL/SAR/comparator/gain top4 shadow + opt-in production PASS | 高，当前最接近真实加速 |
| W2 | General evaluate IR expansion | B01-B06 | `evaluate_ir.py`, `backend.py` expression/statement lowering | W0 | expr/control/state/output targeted tests + real-model manifest coverage 增长 | 中，高频但不能单独解决 event-heavy |
| W3 | Event body block IR and write-set lowering | B10 | `_compile_event_statement`, event trace/write-set audit, Rust event body ABI | W0/W2 | event body shadow parity，write-set 无 side effect 才 production | 高风险，高收益 |
| W4 | Event ordering and lifecycle gate | B09/B10/B11/B18 | `engine.py` phase loop, event queue/order trace | W3 | cross/above/timer order shadow 与 Python 完全一致，initial/final/post_update 语义不变 | 高，PLL/SAR 必需 |
| W5 | Transition/timer production arrays | B08/B11 | `TransitionState`, timer sidecar, Rust typed arrays | W4 | transition retarget/interruption、dynamic timer、breakpoint scan parity + top-wall PASS | 高，解决 CPPLL/ADPLL 长步数路径 |
| W6 | `$bound_step`, source, adaptive scheduler | B12/B13/B14 | dt clamp、source breakpoint、err_ratio scan | W4/W5 | accepted step 序列不变或在容差内，record grid 不变 | 中到高，影响步数 |
| W7 | Dynamic bus and hierarchy production | B02/B04/B17 | node intern、dynamic bus base+offset、instance target resolution | W2 | dynamic bus/2D bus/hierarchy targeted tests + release manifest fallback 减少 | 中，SAR/DAC/bus-heavy 有用 |
| W8 | Record/snapshot/CSV array path | B15 | `SimResult`, record point, CSV writer/checker required signal metadata | W0/W6 | CSV schema 不变或受控升级，checker PASS，record cost 下降 | 中，改善 E2E 而非核心仿真 |
| W9 | Release-wide Rust auto gate | all | runners + manifest gate + mode config | W0-W8 | full release current-EVAS runnable slice PASS，zero EVAS PASS / Spectre FAIL regression | claim prerequisite |
| W10 | Same-slice speed table | all timed rows | speed runners/reports | W9 | same DUT/TB/checker/maxstep/tolerance/host，EVAS/AX/strict timing + parity | paper-facing evidence |

## Immediate Execution Queue

后续建议从 067 开始，按下面队列推进。每个编号都应该对应一篇 audit 文档和一组 targeted tests。

| Next doc | 主题 | 目标产物 | 是否可并行 |
|---|---|---|---|
| 067 | Release Rust Coverage Manifest Generator | 全 release 行为覆盖 JSON/MD，按 top-wall 权重排序 fallback blockers | yes |
| 068 | Whole-Segment Rust ABI Contract | 把 CPPLL/SAR/comparator/gain executor metadata 固化成通用 Rust ABI contract | yes, with 067 |
| 069 | Top-Wall Whole-Segment Production Rust | 把 064/065 的 Python executor 迁入 Rust ABI，先 opt-in production | after 068 |
| 070 | Evaluate IR Generalization Pass | 表达式/条件/state array/dynamic bus 的通用 lowering，不再只补单个语法 | yes, after W0 seed |
| 071 | Event Body Block IR | 从 write-set audit 生成无副作用 event body IR，先 shadow parity | after 067/070 |
| 072 | Event Ordering Production Shadow | 统一 timer/cross/above due、event interpolation、source order、post_update order | after 071 |
| 073 | Transition/Timer Production Arrays | 接管 transition state step、timer due/reschedule、breakpoint scan | after 072 |
| 074 | Dynamic Bus/Hierarchy Production Path | 把 bounded dynamic bus offset primitive 接入 compiler/runtime production | parallel with 071 if tests isolated |
| 075 | Source/Bound-Step/Adaptive Scheduler | source breakpoint、`$bound_step`、err_ratio scan 进入 array scheduler | after 072/073 |
| 076 | Record/CSV Sparse Array Trace | 只记录 checker 必需信号或 array-backed dense trace | parallel after 067 |
| 077 | Full Release Rust Auto Smoke | `rust_mode=auto` full runnable slice，生成 PASS/fallback/speed summary | after 069/073/075/076 |

## Parallelization Map

| Can run in parallel | Reason |
|---|---|
| 067 coverage manifest + 068 ABI contract | 一个是 report/counter，另一个是 Rust ABI 设计，改动面不同 |
| 070 evaluate IR + 076 record/CSV audit | evaluate 与 record 输出边界相对独立 |
| 071 event body IR + 074 dynamic bus production | 只要 dynamic bus tests 不进入 event production，冲突可控 |
| 069 whole-segment production + 067 manifest rendering | 069 消耗 metadata，067 产出覆盖报告，可以互相校验 |

| Must be sequential | Reason |
|---|---|
| 071 -> 072 -> 073 | event body、event ordering、timer/transition production 共享 phase-order correctness gate |
| 073 -> 075 | `$bound_step`/source/adaptive scheduler 必须知道 transition/timer breakpoint 如何被生产路径接管 |
| W9 -> W10 | 没有 release-wide EVAS parity gate，不应该生成 paper-facing speed table |

## Required Data Per Change

每个后续改动的 report 至少收集这些字段，避免只凭 wall time 判断：

| Metric | Why |
|---|---|
| `evas_subprocess_wall_s` | 核心 EVAS 对比口径 |
| `e2e_wall_s` | 包含 checker/CSV/process wrapper 的实际体验 |
| `accepted_steps` / `internal_steps` | 判断是否减少步数 |
| `rust_calls` / `ffi_calls` | 判断是否被大量小 FFI 调用拖慢 |
| `python_fallback_count` and reasons | 判断 Rust 覆盖真实程度 |
| `model_evaluate_s`, `event_due_s`, `record_s`, `csv_s` | 定位剩余瓶颈 |
| `parity_status`, `checker_status` | 防止速度优化掩盖功能退化 |
| `candidate_model_count`, `covered_ops`, `covered_wall_weight` | 判断是否值得推进到 production |

## Promotion Gate

任何行为从 Python 迁到 Rust production 前必须满足：

1. 默认 backend 不变，或明确经过 release gate 才改变默认。
2. 先有 shadow parity，再打开 opt-in production。
3. Rust 失败必须有 Python fallback，且 fallback reason 进入 manifest。
4. 不允许 task 名、benchmark ID、模型文件名特判；只能用语义/数据流匹配。
5. 不允许 length-1 per-check FFI 反复调用进入热路径；必须 batch 或留在 Python。
6. targeted tests、top-wall smoke、release runnable slice 三层验证逐步推进。
7. paper-facing speed claim 必须等 W10，同片任务、同设置、同机器/桥接配置、同 checker。

## Do Not Repeat

| Pattern | Why not |
|---|---|
| 只加一个小 Rust helper 就期待 release-wide speedup | 037-046 已证明 partial coverage 会被 Python sync/FFI/fallback 吃掉 |
| 对端口名/状态名写死 fastpath | 065 已转向语义/数据流匹配，名字匹配不可泛化 |
| 每个 timer/cross 都单独 FFI 一次 | 059 证明 CPPLL length-1 timer Rust path 会变慢 |
| 把 shadow-only 当生产加速 | shadow 是 correctness gate，不会减少 Python production 时间 |
| 没有 same-slice Spectre/AX timing 就写论文速度结论 | 工程优化报告不能替代 paper-facing claim artifact |

## Learning Notes

可以把后续 Rust 化理解成三层迁移：

```text
第一层：把名字变成编号
Python dict: {"vout": 0.5, "clk": 1.0}
Rust array:  values[17] = 0.5, values[3] = 1.0

第二层：把单条语句变成 IR
V(out) <+ gain * V(in) + bias
=> read node_id(in), multiply, add, write node_id(out)

第三层：把一整段仿真 phase 批量执行
event due -> event body -> state update -> output write -> record
=> 一次 Rust batch，而不是每步在 Python/Rust 间来回同步
```

前两层只是准备。真正的大收益来自第三层，因为它同时减少：

- Python 解释器每步调函数的开销；
- dict/string key lookup；
- Python/Rust FFI 往返；
- record/snapshot 的 object copy；
- timer/cross/transition 每步扫描。

## Next Step

- `067 - Release Rust Coverage Manifest Generator`: 先把全 release 79 entry / 357 gold model 的 B01-B18 覆盖、fallback blocker、whole-segment candidate 和 top-wall 权重生成出来。
- `068 - Whole-Segment Rust ABI Contract`: 同步设计 CPPLL/SAR/comparator/gain 的通用 Rust executor ABI，避免继续让 064/065 的 top-wall executor 留在 Python。
