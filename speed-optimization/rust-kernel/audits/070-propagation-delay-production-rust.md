# 070 - Propagation Delay Production Rust

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_cmp_delay_trace_070_20260604.json`
- `speed-optimization/reports/rust_cmp_delay_trace_070_20260604.md`
- `/private/tmp/vaevas_070_top4_smoke.json`
- `/private/tmp/vaevas_070_top4_smoke.md`
- `/private/tmp/vaevas_070_cmp_forms_rust.json`
- `/private/tmp/vaevas_070_cmp_forms_rust.md`

## One-Line Summary

把 propagation-delay comparator 的 whole-segment trace loop 从 Python production fastpath 迁到 Rust ABI；真实 top-wall `vbr1_l1_propagation_delay_comparator/dut` 的 EVAS tran median `1.3745s -> 0.0094s`，E2E wall median `2.0645s -> 0.5783s`。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust core | 没有 comparator delay whole-segment trace ABI | 新增 `cmp_delay_trace_for_arrays()` 和 `evas_rust_cmp_delay_trace` | 默认仿真不变 |
| Python Rust wrapper | `RustBackend` 不能调用 cmp-delay trace | 新增 `RustBackend.cmp_delay_trace()`，固定 6 列输出 ABI | 默认仿真不变 |
| Engine dispatch | `cmp_delay_log_transition_v1` + `edge_interval_timer_v1` whole-segment executor 仍在 Python loop | opt-in whole-model mode 下优先调用 Rust trace；失败 fallback Python | checker/CSV/strobe 行为不变 |
| A/B control | 只能比较 normal fast 和 whole-model mode，不能区分 Python/Rust trace loop | 新增 `EVAS_RUST_CMP_DELAY_TRACE=0/1` | 仅用于审计和回归 |
| coverage map | production whole-segment ABI 只登记到 gain/PRBS | 新增 `evas_rust_cmp_delay_trace` | 文档/manifest 可读性提升 |

## Principle

这一步降低的是**每步成本**，并且这个 row 足够重，所以 E2E wall 也明显变快。

原 Python fastpath 做的工作是固定的：

1. 在 clock source 的 rising/falling edge 上判断 comparator 事件。
2. 根据 `td = td_0 + tau * ln(VDD / |Vdiff|)` 计算再生延迟，并 clamp 到 `td_min/td_max`。
3. 用 `transition()` 语义产生 `out_p/out_n`。
4. edge interval timer 观察 `clk -> out_p` 的 crossing，输出 `delay_ps`。
5. 写出 `clk/vinn/vinp/out_n/out_p/delay_ps` 六列 trace。

070 把这整段固定循环改成 Rust slice + flat matrix 写入。Python 仍负责 source waveform 采样和 runner/checker/CSV 外层，因此这不是全量仿真器 Rust 化。

## Before / After Evidence

三组对照都使用 current top-wall artifact 中的 `vbr1_l1_propagation_delay_comparator/dut/gold`，每组重复 3 次：

- `normal_fast`: `profile_fast_skip_source_error_control`
- `whole_python_trace`: `profile_fast_rust_full_model` + `EVAS_RUST_CMP_DELAY_TRACE=0`
- `whole_rust_trace`: `profile_fast_rust_full_model` + `EVAS_RUST_CMP_DELAY_TRACE=1`

| Form | Path | PASS repeats | E2E wall median (s) | EVAS tran median (s) | Fastpath flags |
|---|---|---:|---:|---:|---|
| `dut` | normal fast | 3/3 | `2.064469` | `1.374500` | whole=0, cmp=0, rust=0 |
| `dut` | Python whole trace | 3/3 | `1.278389` | `0.023800` | whole=1, cmp=1, rust=0, clock_events=32 |
| `dut` | Rust whole trace | 3/3 | `0.578289` | `0.009400` | whole=1, cmp=1, rust=1, rust_points=1793, clock_events=32 |

| Form | Metric | Python whole speedup vs normal | Rust whole speedup vs normal | Rust trace speedup vs Python trace |
|---|---|---:|---:|---:|
| `dut` | E2E wall | `1.615x` | `3.570x` | `2.211x` |
| `dut` | EVAS tran | `57.752x` | `146.223x` | `2.532x` |

Additional forms smoke through a temporary rows artifact:

| Form | Status | E2E wall (s) | EVAS tran (s) | Rust enabled | Points | Events |
|---|---|---:|---:|---:|---:|---:|
| `dut` | PASS | `0.579316` | `0.009900` | 1 | 1793 | 32 |
| `e2e` | PASS | `0.562726` | `0.009200` | 1 | 1793 | 32 |
| `tb` | PASS | `0.536630` | `0.008800` | 1 | 1793 | 32 |

Top4 smoke:

```text
selected rows = 4
results = 8
status = 8/8 PASS
gain row: gain_rust=1
prop-delay row: cmp_rust=1
SAR/CPPLL rows: pre-existing whole-segment paths still PASS
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- New opt-in switch: `EVAS_RUST_CMP_DELAY_TRACE=0/1`

Rust fallback increments `rust_full_model_cmp_delay_rust_fallbacks` and returns to the old Python whole-segment executor.

## Completion And Speed Ledger

| Ledger | Before 070 | After 070 | Delta | Meaning |
|---|---:|---:|---:|---|
| B01-B18 general behavior estimate | `30.0%` | `30.0%` | `+0.0 pp` | 通用 Verilog-A 语义仍没有完全 Rust 化 |
| Release-row effective production estimate | `30.6%` | `31.4%` | `+0.8 pp` | 新增 propagation-delay `dut/tb/e2e` 三条 release rows 可走 production Rust trace，约 `3/357` rows |
| `dut` EVAS tran speed | `1.374500s` | `0.009400s` | `146.223x` | 核心 transient loop 极大变快 |
| `dut` E2E wall speed | `2.064469s` | `0.578289s` | `3.570x` | 该 row 足够重，E2E 也明显变快 |
| Rust trace vs Python whole trace | `0.023800s` | `0.009400s` | `2.532x` | 同一 whole-segment 语义下 Rust loop 比 Python loop 快 |

这里的 `31.4%` 仍是工程进度估计，不是论文速度 claim。

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile EVAS/evas/simulator/rust_backend.py EVAS/evas/simulator/engine.py EVAS/tests/test_rust_backend.py

cargo test --release

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest EVAS/tests/test_rust_backend.py::test_rust_backend_generates_cmp_delay_trace -q

python3 <local repeat runner>  # 3-repeat normal/Python-whole/Rust-whole A/B on dut

python3 <local forms smoke>  # dut/tb/e2e Rust whole trace

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS:/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --entry vbr1_l1_gain_estimator \
  --entry vbr1_l1_propagation_delay_comparator \
  --entry vbr1_l2_weighted_sar_adc_dac_loop \
  --entry vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow \
  --form tb --form dut \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_full_model \
  --output-root /private/tmp/vaevas_070_top4_smoke \
  --report-json /private/tmp/vaevas_070_top4_smoke.json \
  --report-md /private/tmp/vaevas_070_top4_smoke.md \
  --timeout-s 240 --jobs 1
```

Results:

```text
py_compile: PASS
cargo test --release: 29 passed
cmp-delay Rust backend wrapper: 1 passed
dut 3-repeat A/B: all PASS
dut/tb/e2e Rust forms smoke: 3/3 PASS
top4 smoke: 8/8 PASS
```

Not run:

```text
cargo fmt
```

Reason:

```text
cargo-fmt is not installed for stable-aarch64-apple-darwin
```

## Learning Notes

069 的 gain row 很短，所以 Rust 把核心 loop 加速后，外层开销很快成为主导。070 的 propagation-delay row 不一样：normal fast 要跑大约 `1.37s` 的 EVAS tran core，因此把整段行为变成 Rust flat loop 后，E2E wall 也能从 `2.06s` 降到 `0.58s`。

这个现象说明 Rust 化最值得优先做的不是“所有小函数都搬一点”，而是找到 top-wall 的整段固定行为，把 event detection、state update、transition、measurement 和 record 一起 batch 掉。只 Rust 化一个小 helper 往往会被 FFI 和 Python sync 吃掉。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Rust crossing detection 与 Python `_crossed()` 不一致 | delay_ps 或 checker FAIL | 关闭 `EVAS_RUST_CMP_DELAY_TRACE`，回到 Python whole trace |
| transition retarget corner case 缺失 | out_p/out_n 波形偏离，forms smoke FAIL | 复用/扩展 Rust transition primitive 单测 |
| semantic matcher 误命中非 propagation-delay 模型 | candidate valid 但真实 row FAIL | 收紧 `cmp_delay_log_transition_v1` / `edge_interval_timer_v1` contract |
| Rust dylib 版本旧，没有新 symbol | fallback counter 增加 | 重新 build Rust core；或临时设 `EVAS_RUST_CMP_DELAY_TRACE=0` |

## Next Step

下一篇审计文档编号和预期主题：

- `071 - SAR Whole-Segment Rust Trace`
