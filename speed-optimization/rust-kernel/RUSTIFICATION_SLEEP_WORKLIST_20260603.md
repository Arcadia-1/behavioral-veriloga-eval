# Rustification Sleep Worklist - 2026-06-03

Status: `deprecated`

Superseded by: `RUSTIFICATION_WORKLIST_20260605.md`

理由：本文档规划停在 audit 050，但本地实际进度已到 audit 085（修改于 2026-06-05 04:02）。新 worklist 重新分类了 001–085 全部 audit，按"通用速度优先"目标重排了后续优先级，并明确暂停 per-circuit C-track。原文档保留作为 2026-06-03 时点快照。

Scope: EVAS kernel Rustification after `034 - Static Lifecycle Fastpath`

## Current Position

027 已经把 Rust static affine path 的 FFI 调用从 `64064` 次降到 `1001` 次，Rust opt-in path 在当时的 microbenchmark 中从 median `0.8521 s` 改善到 `0.3255 s`。

028-030 继续收掉了三类 Python 外层成本：

- 028 把 `output_nodes` 同步从每步延迟到 final 前；
- 029 把全 Rust static segment 的 indexed validation 从全量 diff 改成预计算 dirty tuple；
- 030 让 Rust static segment 成功时跳过每个 model 的 Python `_prepare_step()`、timer expire 和 post-update 空检查。

031 扩大了 Rust static affine coverage：`gain/bias` 可以来自 REAL/INTEGER parameter-only arithmetic，并在 instance parameter override 后求值。64-model parameterized affine sample 中 `runtime_param_ops = 64`，但 fixed-step Rust median `0.2322 s` 仍慢于 default Python `0.1918 s`。

032 把 generated dynamic bus read/write 从直接格式化节点名改为 `_resolve_dynamic_node(base, index, index2)` cache。16-lane dynamic bus sample 中 cache-enabled path 只有 `16` 次 miss、`16032` 次 hit，median `0.034590708 s -> 0.030722917 s`。这一步仍是 node-string semantics，不是完整 Rust node-id offset lowering。

033 新增 opt-in indexed state runtime mirror，scalar/int/array state 写入可同步到 slot storage。stateful sample waveform parity 通过，但 mirror path median `0.010790875 s` 慢于 default `0.007966792 s`，说明它是 Rust state ABI 前置，不是当前 Python 加速。

034 根据用户要求临时切换到大瓶颈优化，而不是继续低收益 ABI 预备件。它复用 compiler capability flags，把纯静态模型默认从每步空 `_prepare_step()` 和 absolute timer expire 里拿出来。80-model static chain same-code A/B 中，median wall 从 `1.314976 s` 降到 `0.885306 s`，约 `1.485x`；profile-section 显示 `model_prepare_step_s` 从 `0.412302 s` 降到 `0`。

但这还不是最终速度优势：

```text
030 DC fixed-step sample:
default Python median: 0.333597084 s
Rust segment median:  0.395932084 s
```

当前主要问题不在 Rust 乘加，而在 Python/Rust 边界、Python 侧状态维护、coverage，以及 034 后真实 benchmark 上剩余的 section 分布：

- Rust 输出每步仍要同步回 Python `node_voltages`，030 DC sample 中 `node_voltage_syncs = 64064`；
- indexed dirty validation 仍每步检查 source/output tuple，030 DC sample 中 `dirty_nodes_checked = 65065`；
- Rust/Python FFI 和 ctypes 边界仍存在；
- Rust eligibility 只覆盖 literal static affine，真实 benchmark 覆盖率还低。
- 对 static-heavy Python 模型，空 lifecycle 已经被收掉；后续需要重新 profile，不能沿用 033 前的瓶颈排序。

## Sleep-After Priority

| Order | Audit | Work Item | Track | Goal | Main Risk | Success Evidence |
|---:|---|---|---|---|---|---|
| 028 | `028-rust-output-node-sync-deferral.md` | Rust output node sync deferral | production opt-in | 每步保留 `node_voltages`，延迟 `output_nodes` 写入 | stale `output_nodes` | done: full pytest + counters |
| 029 | `029-indexed-dirty-validation-fastpath.md` | Dirty-node indexed validation | production opt-in | 用预计算 dirty node tuple 替代冗余全量 `max_abs_diff_mapping()` | 漏掉 dict/array divergence | done: full pytest + checked values 下降 |
| 030 | `030-segment-lifecycle-fastpath.md` | Segment lifecycle fastpath | production opt-in | 对 compiler-proven static segment 跳过 per-model 空 prepare/timer/post-update | eligibility guard 过宽 | done: full pytest + lifecycle skip counters |
| 031 | `031-runtime-parameter-affine-lowering.md` | Runtime parameter affine lowering | production opt-in | 支持 `gain/bias` 来自 parameters 的 affine model | 参数 override/type coercion | done: compiler + simulator + netlist override tests |
| 032 | `032-dynamic-bus-base-offset-lowering.md` | Dynamic bus base/index runtime lowering | production/prototype | 把 `V(bus[i])` 简单场景从重复字符串格式化降为 resolver cache | 2D bus、state-index、event context | done: full pytest + cache hit counters |
| 033 | `033-indexed-state-runtime-storage.md` | Indexed state runtime storage | prototype | 把 scalar/int/array state 映射到 opt-in indexed mirror | Python/Rust state divergence | done: full pytest + state parity counters |
| 034 | `034-static-lifecycle-fastpath.md` | Static lifecycle fastpath | production default | 跳过静态模型每步空 prepare/timer 生命周期维护 | eligibility guard 过宽 | done: full pytest + 1.485x local microbench |
| 035 | `035-rust-expression-ir.md` | Rust expression IR | prototype | 把普通 arithmetic expression lowering 成 Rust op tree | Verilog-A coercion 语义 | expression parity fixture |
| 036 | `036-rust-static-branch-evaluator.md` | Rust static branch evaluator | prototype | 支持更一般的无事件 continuous assignments | unsupported operator 漏判 | operator eligibility tests |
| 037 | `037-rust-model-state-abi.md` | Rust model state ABI | prototype | Rust 读写 indexed scalar/int/array state | state lifecycle | state round-trip tests |
| 038 | `038-rust-event-condition-ir.md` | Rust event condition IR | prototype | lowering `cross/above/timer` trigger metadata | event interpolation | event trigger metadata tests |
| 039 | `039-rust-timer-breakpoint-queue.md` | Rust timer/breakpoint queue | prototype | 减少 timer-heavy 任务每步扫描 | missed breakpoint | timer/cross parity fixture |
| 040 | `040-rust-event-body-executor.md` | Rust event body executor | prototype | 简单 event body 在 Rust 执行 | event ordering | event body parity tests |
| 041 | `041-rust-transition-operator.md` | Rust transition operator | prototype | Rust 化 transition 状态机 | delay/rise/fall 语义 | transition waveform fixture |
| 042 | `042-rust-random-noise-subset.md` | Rust random/noise subset | prototype | 可控 lowering `$random` / distribution subset | determinism | seeded parity tests |
| 043 | `043-rust-record-sparse-trace.md` | Rust record/sparse trace | production/prototype | 直接输出 checker 必需信号或 sparse trace | CSV/checker schema | trace parity tests |
| 044 | `044-native-checker-bridge.md` | Native checker bridge | prototype | 简单 checker 直接消费 sparse trace | checker compatibility | checker parity report |
| 045 | `045-rust-simulator-loop-prototype.md` | Rust simulator loop prototype | prototype | 纯静态/简单事件模型由 Rust loop 跑完整 transient | Python/Rust scheduler divergence | Python/Rust trace parity |
| 046 | `046-hybrid-scheduler.md` | Hybrid scheduler | design/prototype | Python 调度 + Rust segment kernel | boundary complexity | scheduler design + smoke |
| 047 | `047-full-rust-scheduler.md` | Full Rust scheduler | design/prototype | Rust 管 step/source/event/record | broad parity risk | limited-scope prototype only |
| 048 | `048-vabench-full-coverage-audit.md` | vaBench full coverage audit | audit | 全量 EVAS 可仿任务的 Rust support matrix | 功能缩减 | no-regression manifest |
| 049 | `049-same-slice-evas-spectre-ax-rerun.md` | Same-slice EVAS/Spectre/AX rerun | experiment | 统一条件速度/精度表 | Cadence environment | same-slice timing report |
| 050 | `050-claim-gate-update.md` | Claim gate update | paper/report | 只根据证据更新论文口径 | overclaim | claim gate report |

## Recommended Night Run

034 后建议先重跑 benchmark-level profile，再决定继续 Rust expression IR 还是优先处理新的最大 section。不急着跑 Cadence full rerun：

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
cd evas/rust_core && cargo test --release
cd ../..
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py tests/test_engine.py tests/test_netlist.py -q
python3 -m pytest tests -q
```

每做完一个 audit，至少补充：

- exact changed files；
- before/after microbenchmark；
- parity evidence；
- which counters moved；
- why default backend remains unchanged。

## Claim Boundary

睡后继续推进时，口径保持：

- 可以说：027 证明 batching 能显著降低 Rust FFI overhead。
- 可以说：027 后新的瓶颈转移到 Python output sync、indexed validation 和 lifecycle bookkeeping。
- 可以说：034 证明纯静态模型每步空 lifecycle 是真实 Python 内核瓶颈，local static-chain sample 约 `1.49x`。
- 不能说：EVAS Rust path 已经比默认 Python 更快。
- 不能说：EVAS 已经 paper-facing 快于 Spectre AX。

最终 speed claim 仍必须来自 vaBench same-slice、同服务器、Spectre-equivalence-gated 的 EVAS/Spectre/AX timing。
