# 058 - Event-Body Write-Set Rust Batch

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/event_trace_audit_topwall10_20260604_r2.json`
- `speed-optimization/reports/rust_event_write_parity_gain_tb_20260604_r2.json`
- `speed-optimization/reports/rust_event_write_ab_topwall10_20260604_r2.json`
- `speed-optimization/reports/rust_event_write_parity_topwall10_20260604_r2.json`

## One-Line Summary

057 的 top-wall audit 显示最高频 event-body 写入来自 gain extraction 里的 gated LFSR shift/XOR；本轮把这一类 state/array/scalar-output-state write-set lowering 到 Rust batch，先做 shadow parity，再接入 opt-in production。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust ABI | Rust 只有 event-due / timer / transition helper，event body 仍全在 Python | 新增 `evas_rust_event_lfsr_shift_xor_step`，执行 gated static-width LFSR shift/XOR event body | 默认不变 |
| Python Rust bridge | 无 event-body write-set batch wrapper | 新增 `RustLfsrEventBatch` 和 `event_lfsr_shift_xor_step()` wrapper | 默认不变 |
| Compiled model backend | `@(cross(...))` body 逐条 Python state/array assignment 执行 | 编译期识别 gated LFSR shift/XOR 模式，生成 shadow 或 production hook | 默认不变 |
| Simulator/runner | 无 event-write Rust 开关 | 新增 `evas_rust_event_write_shadow=true` 和 `evas_rust_event_write_production=true` | opt-in |
| Speed experiment runner | 无对应 mode | 新增 `profile_fast_rust_event_write_shadow` / `profile_fast_rust_event_write_production` | 只影响实验 |

## Principle

这次优化属于 **降低每次 event body 触发后的执行成本**。

原 Python 路径在一次 LFSR event body 中会做很多小对象操作：

- for-loop 更新 loop state `i`
- 逐个读写 `lfsr_r[i]` 和 `tmp_lfsr_r[i]`
- 计算 XOR feedback
- 写回输出状态变量 `dpn_level`

这些操作在 Python 里是大量 dict lookup、array dict access、函数调用和 Python object 更新。Rust batch 把同一组副作用变成一次 typed array loop：

1. 从 typed state array 读旧 `lfsr_r`。
2. 在 Rust 中写 `tmp_lfsr_r` 和新 `lfsr_r`。
3. 按 tap slots 计算 XOR feedback。
4. 根据 gate node 决定是否执行。
5. 写回 scalar output state 和 loop final state。

注意：这不是全量 event body Rust 化。当前只覆盖静态宽度、固定 tap、固定 shift 方向的 gated LFSR shift/XOR 模式；一般 event statement、post-update event、transition output contribution 仍走 Python fallback。

## Audit Evidence

top-wall10 event trace/write-set audit 的主要结论：

| Metric | Value | Interpretation |
|---|---:|---|
| event body entries | `30003` | top-wall10 中事件体执行非常频繁 |
| in-event writes | `397145` | event-body write-set 足够大，值得 batch |
| state writes | `917688` | 全局 state 写入很多，其中 event-body state 写入是主要候选之一 |
| array writes | `140228` | gain extraction 的 LFSR 数组写是最清晰候选 |
| output writes | `1067281` | 多数仍来自连续输出/transition 路径，不应混同为本轮 LFSR event-body batch |

最高频 event-body shape：

| Dynamic key | Writes | Meaning |
|---|---:|---|
| `event_trace_audit_body::cross::cross_1::state_writes` | `146202` | gain extraction LFSR event body 的 loop/scalar state 写 |
| `event_trace_audit_body::cross::cross_1::array_writes` | `138126` | 同一 event body 的 LFSR/tmp array 写 |
| `event_trace_audit_body::timer_absolute::timer_0::state_writes` | `92672` | CPPLL/DCO timer state 写，下一轮更适合做 timer/event queue |

最高频 target：

| Target | Writes | Note |
|---|---:|---|
| `state::i` | `135814` | for-loop index state，说明 Python loop/writeback 开销明显 |
| `array::lfsr_r[0]`, `array::lfsr_r[5]`, ... | about `2000` each | LFSR shift body 的固定数组写 |
| `state::dco_freq`, `state::dco_half_period`, `state::dco_state`, `state::t_next_toggle` | `19248` each | CPPLL timer/event path，未在本轮 production 化 |

## Before / After Evidence

### Target row

`vbr1_l2_gain_extraction_convergence_measurement_flow`, `tb` form:

| Mode | Wall | Status | Safety |
|---|---:|---|---|
| `strict_current` | `15.476s` | PASS | baseline |
| `profile_fast_rust_event_write_shadow` | `2.001s` | PASS | safe vs strict |
| `profile_fast_rust_event_write_production` | `1.363s` | PASS | safe vs strict |

Shadow/production counters:

| Counter | Value |
|---|---:|
| shadow checks | `1000` |
| shadow matches | `1000` |
| shadow mismatches | `0` |
| shadow errors | `0` |
| production calls | `1000` |
| production executed | `998` |
| production fallbacks | `0` |
| indexed array syncs | `0` |

Separate A/B against fast Python on the same row:

| Mode | Wall | Interpretation |
|---|---:|---|
| `profile_fast_skip_source_error_control` | `2.150s` | Python fast reference |
| `profile_fast_rust_event_write_production` | `1.289s` | local `1.67x` on this run |

### Top-wall10

Full strict/shadow/production parity:

| Mode | PASS | safe vs strict | Total wall |
|---|---:|---:|---:|
| `strict_current` | `10/10` | baseline | `255.335s` |
| `profile_fast_rust_event_write_shadow` | `10/10` | `10/10` | `29.148s` |
| `profile_fast_rust_event_write_production` | `10/10` | `10/10` | `28.393s` |

Top-wall10 fast Python vs event-write production A/B:

| Mode | PASS | Total wall | Interpretation |
|---|---:|---:|---|
| `profile_fast_skip_source_error_control` | `10/10` | `27.514s` | fast Python reference |
| `profile_fast_rust_event_write_production` | `10/10` | `27.267s` | `1.009x` total, effectively neutral |

Why total speedup is small:

- Only two rows matched the new Rust batch: gain extraction `e2e` and `tb`.
- The other eight rows had `rust_event_write_batches=0`, so this change correctly did not add indexed-state or indexed-array overhead to them.
- On matched rows, single-run wall still has enough noise that production is not a stable release-wide speed claim yet.
- The next high-value path is CPPLL/timer/event queue, not more polishing of this one LFSR primitive.

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Production path default: `off`

Safety gates:

- Shadow mode runs Rust first, then Python, and compares only target slots.
- Production mode is opt-in and returns to Python if the Rust batch cannot be built or executed.
- Rows with no eligible event body disable event-write mode early, so they do not pay global indexed-array overhead.

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile EVAS/evas/simulator/backend.py EVAS/evas/simulator/engine.py EVAS/evas/netlist/runner.py behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py::TestSimulator::test_rust_event_write_shadow_and_production_match_lfsr_body -q

cargo test

PYTHONPATH=runners:../EVAS python3 runners/run_vabench_release_evas_speed_experiment.py --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json --suite top-wall --limit 10 --mode strict_current --mode profile_fast_rust_event_write_shadow --mode profile_fast_rust_event_write_production --timeout-s 900 --jobs 2 --output-root results/rust-event-write-parity-topwall10-20260604-r2 --report-json speed-optimization/reports/rust_event_write_parity_topwall10_20260604_r2.json --report-md speed-optimization/reports/rust_event_write_parity_topwall10_20260604_r2.md

PYTHONPATH=runners:../EVAS python3 runners/run_vabench_release_evas_speed_experiment.py --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json --suite top-wall --limit 10 --mode profile_fast_skip_source_error_control --mode profile_fast_rust_event_write_production --timeout-s 900 --jobs 2 --output-root results/rust-event-write-ab-topwall10-20260604-r2 --report-json speed-optimization/reports/rust_event_write_ab_topwall10_20260604_r2.json --report-md speed-optimization/reports/rust_event_write_ab_topwall10_20260604_r2.md
```

Results:

```text
py_compile: pass
targeted engine test: 1 passed
cargo test: 27 passed
top-wall10 parity: strict/shadow/production all 10/10 PASS; shadow/production both 10/10 safe_vs_strict
top-wall10 A/B: fast Python 27.514s; Rust event-write production 27.267s
```

## Learning Notes

这里的 “write-set lowering” 可以理解成：先不尝试把整个事件系统改成 Rust，而是找到一个事件体中最常重复的一组写操作，把它们合并成一个 Rust 函数。

Python 慢的不是 XOR 这个数学运算，而是围绕它的一圈运行时开销：名字查找、dict 读写、数组元素字典、循环变量状态写回、函数调用。Rust 快的潜力来自把这些小动作变成连续数组上的循环。

为什么还需要 shadow？因为 event body 是有副作用顺序的。即使最后输出波形看起来过了 checker，也可能某个 state slot 在中间顺序不一致。shadow 模式让 Rust 和 Python 同时执行同一事件，并逐 slot 比较目标写集合，这是 production 前必须有的安全门。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Pattern recognizer 误识别非 LFSR event body | shadow mismatch 或 production strict comparison unsafe | 关闭 `evas_rust_event_write_*`；回退 `backend.py` 中 `_event_body_lfsr_shift_ir` / `_compile_event_body_with_rust_write` |
| Rust batch 写了错误 state slot | `rust_event_write_shadow_mismatches_total > 0` | 保持 production off，修正 state slot lowering |
| 小 batch FFI 成本高于 Python | top-wall A/B 变慢 | 保持 production opt-in，不把它作为默认 fast path |
| 把 output contribution 误当 event-body scalar state | waveform/checker mismatch | 只允许本轮 primitive 写 state/array/scalar state，transition/output contribution 继续 Python |

## Next Step

`059 - Timer/Event Queue Rust Production Plan`

理由：058 已经证明 event-body write-set 可以安全进入 opt-in Rust batch，但 top-wall 总收益很小。057 audit 的第二大 candidate 是 CPPLL/timer state 写和 breakpoint scan；要获得更明显收益，下一步应该把 timer state、event queue、breakpoint scan 和 event body dispatch 放进同一个 typed-array plan，而不是继续扩一个很窄的 LFSR primitive。
