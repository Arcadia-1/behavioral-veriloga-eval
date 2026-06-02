# Rustification Sleep Worklist - 2026-06-03

Status: `active`

Scope: EVAS kernel Rustification after `027 - Rust Consecutive Model Segment Batch`

## Current Position

027 已经把 Rust static affine path 的 FFI 调用从 `64064` 次降到 `1001` 次，Rust opt-in path 在同一 microbenchmark 中从 median `0.8521 s` 改善到 `0.3255 s`。

但这还不是最终速度优势：

```text
default Python median: 0.204989042 s
Rust segment median:  0.555189333 s
```

当前主要问题不在 Rust 乘加，而在 Python 侧状态维护和 coverage：

- Rust 输出每步仍同步回 Python dict/output_nodes，027 sample 中 `output_syncs = 64064`；
- indexed array 每步仍做全量 sync/validate，027 sample 中 `indexed_syncs = 1001`；
- segment 内每个 model 仍走 Python `_prepare_step()`、timer expire 和 post-update bookkeeping；
- Rust eligibility 只覆盖 literal static affine，真实 benchmark 覆盖率还低。

## Sleep-After Priority

| Order | Audit | Work Item | Goal | Main Risk | Success Evidence |
|---:|---|---|---|---|---|
| 028 | `028-rust-output-sync-gating.md` | Rust output sync gating / deferred sync | 只把后续 Python 路径真正需要的 Rust outputs 写回 dict/output_nodes | Python fallback model 或 recorder 读到 stale dict | affine parity tests pass; output_syncs 明显下降 |
| 029 | `029-indexed-dirty-sync-validation.md` | Dirty-node indexed validation | 用 dirty node set 或 sampling 替代每步全量 `max_abs_diff_mapping()` | 漏掉 dict/array divergence | targeted mismatch injection test; sync checked values 下降 |
| 030 | `030-segment-lifecycle-fastpath.md` | Segment lifecycle fastpath | 对 compiler-proven static segment 跳过 per-model 空 prepare/timer/post-update | 跳过了未来会影响 event/bound_step 的模型 | eligibility guard + full pytest |
| 031 | `031-runtime-parameter-affine-lowering.md` | Runtime parameter affine lowering | 支持 `gain/bias` 来自 parameters 的 affine model | 参数变更或类型 coercion 处理错 | parser/compiler tests + netlist parameter smoke |
| 032 | `032-dynamic-bus-base-offset-lowering.md` | Dynamic bus base+offset runtime lowering | 把 `V(bus[i])` 简单场景从字符串格式化降为 id offset | 2D bus、state-index、event context 错配 | bus lowering regression tests |
| 033 | `033-rust-event-timer-queue-prototype.md` | Rust event/timer queue prototype | 对 PLL/timer-heavy 任务减少每步扫描 | missed event / breakpoint ordering | timer/cross parity fixture |
| 034 | `034-vabench-rust-coverage-smoke.md` | vaBench Rust eligibility coverage smoke | 统计 release rows 中可 Rust 化模型比例 | 把 coverage 误解为速度 claim | coverage report only, no speed claim |

## Recommended Night Run

先做低风险内核工作，不急着跑 Cadence full rerun：

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
cargo test --release
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
- 不能说：EVAS Rust path 已经比默认 Python 更快。
- 不能说：EVAS 已经 paper-facing 快于 Spectre AX。

最终 speed claim 仍必须来自 vaBench same-slice、同服务器、Spectre-equivalence-gated 的 EVAS/Spectre/AX timing。
