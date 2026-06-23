# 062 - Fused Timer LFSR Output Batch

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- Local unit/parity evidence plus targeted speed probes only. No paper-facing top-wall speed claim is made here.

## One-Line Summary

把一个真实高频行为段 `timer due/reschedule + LFSR event body + output state write + output node hold + indexed record read` 降成一个可选 Rust production batch。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust kernel | Timer step、LFSR event body、node output write 是分开的 primitive | 新增 `evas_rust_timer_lfsr_output_step`，一次 FFI 调用完成 periodic timer step、LFSR state update、output node write | 不变 |
| Python ctypes | 只能调用独立 timer primitive 或独立 LFSR event-body primitive | `RustBackend.timer_lfsr_output_step(...)` 返回 `due/skipped/executed/output_written` | 不变 |
| Compiler backend | 可识别 LFSR event body，但 timer due 和 `V(out)<+state` 仍在 Python 侧执行 | 对安全的 periodic timer LFSR 生成 `if fused: pass elif Python fallback`；对安全 `V(out)<+state` 生成 output hold fast path | 不变 |
| Engine harness | `rust_event_write_production` 只强制 indexed state storage | 当 `rust_timer_event + rust_event_write_production` 同时开启时，也强制 indexed node array，并安装 fused batch required nodes | 不变 |

## Principle

这个改动属于 **降低每步成本** 和 **减少 Python dict/object 写路径**。

原路径每个 step 至少会经过：

```text
Python timer due check
Python event body dispatch
Python state/array writes
Python output contribution V(out)<+state
Python dict 写 nv/output_nodes
record 再从 indexed 或 dict 读 out
```

新路径在识别成功时变成：

```text
Rust periodic timer step
Rust LFSR state array update
Rust output node array write
Python 只同步必要 timer state / state slots / output dict 初始化或值变化
record 从 indexed node id 读取
```

这里的重点不是“Rust 比 Python 神奇”，而是把多个细小 Python 行为合并成一次数组循环和一次 FFI 调用，减少 `dict[str, float]` lookup、Python function dispatch、state/object 同步和重复 output write。

## Safety Conditions

只对以下模式启用：

- periodic timer：`@(timer(start, period))`；
- event body 是已识别的 LFSR shift/xor 模式；
- gate/high/low/output 都能解析成静态 node id；
- output contribution 是简单 `V(out) <+ state`；
- output state 在 evaluate 阶段只由识别出的 LFSR event 写，`initial_step` 写入允许；
- `rust_timer_event=True` 且 `rust_event_write_production=True`；
- `event_trace_audit=False`。

以下情况继续走 Python fallback：

- dynamic node/bus output；
- non-periodic timer 或 absolute timer；
- 非 LFSR event body；
- output state 还有其它 evaluate/event 写入者；
- trace audit 模式；
- Rust backend 不可用或 indexed node/state arrays 未安装。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| EVAS subprocess wall | measured below | measured below | 机制正确，但当前 fused production path 还不是可声明加速 |
| accepted steps | unchanged | unchanged | timer primitive 复用同一语义 |
| fused calls | 0 | 16 | 4ns smoke 每个 step 进入 fused handler |
| timer due events | Python path | 4 | 4 个 periodic due 由 Rust batch 处理 |
| event body executed | Python path | 4 | 4 次 LFSR body 由 Rust batch 执行 |
| output writes | Python contribution | 4 fused writes | due step 输出由 Rust 写 node array，hold path 避免重复写 |
| record reads | dict or indexed path | 17 indexed-id reads | record 从 indexed node id 读取 |
| fallback count | n/a | 0 | smoke 没有退回 Python |
| checker/result parity | default Python | PASS | default vs fused waveform/state 一致 |

## Speed Probe Result

这轮速度探针的结论是：**当前 fused batch 没有形成可用加速；在 synthetic covered case 上反而变慢，真实 LFSR top-wall 行没有触发 fused coverage。**

### Synthetic Covered Microbench

条件：同一个 `timer_lfsr` 模型，`tstop=1us`，`max_step=tstep=0.25ns`，约 4001 steps、1000 timer due events、4002 record points；每种模式 2 次 warmup + 8/9 次 measured run，取 median。

| Mode | Median wall s | Speed vs Python | Key counters | Interpretation |
|---|---:|---:|---|---|
| `python_default` | 0.0599 | 1.00x | no Rust, no indexed arrays | baseline |
| `indexed_arrays_only` | 0.1990 | 0.30x | 4001 syncs, 4001 snapshots, 4002 indexed record reads | indexed-array side path alone already makes this small model slower |
| `rust_event_body_only` | 0.0666 | 0.90x | 1000 Rust event-body calls | event body is too small; FFI overhead exceeds saved Python work |
| `rust_fused_timer_lfsr_output` | 0.2466 | 0.24x | 4001 fused calls, 1000 due/executed, 4002 indexed record reads | fused path is covered, but per-step FFI + indexed-array sync dominates |

Profile split from one covered run:

| Section | Python default s | Fused s | Note |
|---|---:|---:|---|
| `model_evaluate_s` | 0.0301 | 0.1203 | fused helper is called every step through Python/ctypes |
| `err_ratio_node_scan_s` | 0.0071 | 0.0317 | indexed node path increases per-step scan cost in this small case |
| `indexed_array_sync_s` | 0.0000 | 0.0303 | new cost introduced by forcing indexed arrays |
| `indexed_array_prev_snapshot_s` | 0.0000 | 0.0251 | new cost introduced by forcing indexed arrays |
| `record_point_s` | 0.0028 | 0.0189 | indexed-id record path is not yet cheaper for this tiny output set |

### Real Top-Wall LFSR Probe

条件：`vbr1_l1_lfsr_prbs_generator/dut/gold`，EVAS-only runner，row source `speed-optimization/reports/current_fourway_topwall10_clean_20260604.json`，output under `/private/tmp/vaevas_fused_lfsr_real*`.

First order:

| Mode | E2E wall s | Subprocess wall s | PASS | Fused batches | Fused calls |
|---|---:|---:|---:|---:|---:|
| `profile_fast_skip_source_error_control` | 0.4903 | 0.4483 | yes | 0 | 0 |
| `profile_fast_rust_event_write_production` | 0.3584 | 0.3292 | yes | 0 | 0 |
| `profile_fast_rust_timer_event` | 0.3551 | 0.3254 | yes | 0 | 0 |
| `profile_fast_rust_timer_lfsr_output` | 0.3577 | 0.3286 | yes | 0 | 0 |

Reverse order:

| Mode | E2E wall s | Subprocess wall s | PASS | Fused batches | Fused calls |
|---|---:|---:|---:|---:|---:|
| `profile_fast_rust_timer_lfsr_output` | 0.3925 | 0.3579 | yes | 0 | 0 |
| `profile_fast_rust_timer_event` | 0.3515 | 0.3227 | yes | 0 | 0 |
| `profile_fast_rust_event_write_production` | 0.3524 | 0.3231 | yes | 0 | 0 |
| `profile_fast_skip_source_error_control` | 0.3597 | 0.3301 | yes | 0 | 0 |

Interpretation:

- The apparent first-order 0.490s -> 0.358s improvement is mostly cold-start/order effect; when baseline is run last it is 0.360s.
- `rust_timer_lfsr_output_batches_total=0`, so this real LFSR model does not match the current fused pattern. It cannot be used as evidence that fused lowering speeds real top-wall rows.
- The concrete mismatch is expected: release PRBS7 uses `@(cross(V(CLK)-vth,+1))`, integer shift-register state, seven `transition(...)` output contributions, and reset on `initial_step or cross(RSTB)`. The current fused recognizer only covers periodic `timer(...)`, real-array LFSR shift, and simple `V(out)<+state`.
- Current fused coverage is too narrow and the covered synthetic path is too small to amortize Python/ctypes and indexed-array synchronization overhead.

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile evas/simulator/backend.py evas/simulator/engine.py evas/simulator/rust_backend.py tests/test_engine.py tests/test_rust_backend.py
cargo test -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest tests/test_rust_backend.py::test_rust_backend_fuses_timer_lfsr_and_output_write -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest tests/test_engine.py::TestSimulator::test_rust_fuses_timer_lfsr_output_and_record_path -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest tests/test_engine.py::TestSimulator::test_rust_event_write_shadow_and_production_match_lfsr_body -q
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest tests/test_rust_backend.py::test_rust_backend_steps_periodic_timers_like_python tests/test_rust_backend.py::test_rust_backend_fuses_timer_lfsr_and_output_write -q
```

Results:

```text
py_compile: PASS
cargo test: 28 passed
ctypes fused timer/LFSR/output test: 1 passed
engine fused timer/LFSR/output/record parity test: 1 passed
existing event-write production regression: 1 passed
timer + fused ctypes regression: 2 passed
```

Smoke counters:

```text
rust_timer_lfsr_output_batches_total = 1
rust_timer_lfsr_output_calls_total = 16
rust_timer_lfsr_output_due_total = 4
rust_timer_lfsr_output_executed_total = 4
rust_timer_lfsr_output_writes_total = 4
rust_timer_lfsr_output_fallbacks_total = 0
indexed_array_record_reads = 17
indexed_array_record_id_reads = 17
```

## Learning Notes

这里的 “整体 lowering” 可以理解成把一小段 Python 解释器工作压成一个 Rust 函数：

1. Python 版本像每一步都在查多张表：timer dict、state dict、array dict、node dict、record dict。
2. Rust 版本先把节点和状态编号成整数 id，然后用数组下标读写：`state_values[slot]`、`node_values[node_id]`。
3. LFSR shift 本质是固定数组重排和 XOR，很适合数组 loop。
4. Timer periodic step 本质是比较 `time` 和 `next_fire`，如果 due 就把 `next_fire += period`，也适合数组 primitive。
5. `V(out)<+state` 在这个安全模式下只是把一个 state slot 的数复制到一个 node slot，不需要每步都做 Python dict 写。

所以收益来自“少进 Python、少查字符串 key、少构造对象”，不是来自改变仿真数学模型。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 安全判定漏掉其它 state writer，导致 output hold 没更新 | default vs fused parity test 或真实 benchmark mismatch | revert `backend.py` 的 `_collect_lfsr_output_hold_states` / `_rust_state_output_hold_production` / `_compile_contribution` hold path |
| Rust ABI 与 Python ctypes 参数顺序不一致 | `test_rust_backend_fuses_timer_lfsr_and_output_write` fail 或 Rust error code | revert `lib.rs` new export and `rust_backend.py` wrapper |
| 强制 indexed arrays 改变普通 event-write path | existing event-write production regression fail | keep indexed array only under `rust_timer_event and rust_event_write_production` |
| trace audit 漏记录 | audit tests fail | current design disables fused/hold when `event_trace_audit=True` |

## Next Step

- `063 - Real Top-Wall Fused Timer/Event Coverage`: 在真实 top-wall 模型上统计哪些 timer/event/output 段被 fused batch 覆盖，哪些因为 dynamic node、non-LFSR body、absolute timer、extra state writer 被拒绝。
