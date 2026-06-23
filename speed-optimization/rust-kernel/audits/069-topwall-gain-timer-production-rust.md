# 069 - Top-Wall Gain Timer Production Rust

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_gain_timer_reduction_069_20260604.json`
- `speed-optimization/reports/rust_gain_timer_reduction_069_20260604.md`
- `/private/tmp/vaevas_069_top4_smoke.json`
- `/private/tmp/vaevas_069_top4_smoke.md`

## One-Line Summary

把 `gain_timer_reduction_v1` 的 whole-segment trace loop 从 Python production fastpath 迁到 Rust ABI，真实 release `vbr1_l1_gain_estimator` 的 EVAS tran core 约 `3.3x` 快于 normal fast，约 `1.4x` 快于旧 Python whole-segment trace。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust core | 只有 PRBS7 whole-model trace；gain measurement 仍由 Python loop 生成 trace | 新增 `evas_rust_gain_timer_reduction_trace` C ABI 和 `gain_timer_reduction_trace_for_arrays()` | 默认仿真不变，只有 opt-in whole-model mode 命中 |
| Python Rust wrapper | `RustBackend` 不能调用 gain trace | 新增 `RustBackend.gain_timer_reduction_trace()`，固定 8 列输出 ABI | 默认仿真不变 |
| Engine dispatch | `gain_timer_reduction_v1` whole-segment executor 是 Python loop | 在 `EVAS_RUST_FULL_MODEL_FASTPATH=1` 且 Rust backend 可用时优先调用 Rust trace；失败 fallback 到 Python trace | checker/CSV/strobe 行为不变 |
| A/B control | 无法区分旧 Python whole-segment 和新 Rust trace | 新增 `EVAS_RUST_GAIN_TIMER_TRACE=0/1` 控制内部 trace loop | 仅用于审计和回归 |
| coverage map | whole-model production ABI 登记不完整 | 登记 `evas_rust_prbs7_trace` 和 `evas_rust_gain_timer_reduction_trace` | 文档/manifest 可读性提升 |

## Principle

这一步降低的是**每步成本**和**Python object/list/dict 开销**，不是减少仿真步数。

`gain_timer_reduction_v1` 的行为可以拆成固定数据流：

1. 在一组 sample timer 上读取 `vinp/vinn/voutp/voutn/vdd/vss`。
2. 维护输入输出差分的 min/max。
3. 输入 span 足够后计算 `gain_q` 和 `valid_q`。
4. 用 `transition()` 语义生成 `gain` 和 `valid` 输出。
5. 对所有 trace time point 写 8 列固定矩阵。

旧 Python whole-segment 已经绕过了通用 generated model evaluate，但每个 time point 仍在 Python 循环里执行 state update、transition evaluate 和 list append。069 把这段固定 loop 变成 Rust slice + flat `Vec<f64>` 写入，所以核心 tran loop 明显变快。

这不是全量 Verilog-A Rust 化。它只覆盖 compiler 能识别为 `gain_timer_reduction_v1` 的语义 family。换一个 measurement flow，如果语义结构不同，仍会 fallback。

## Before / After Evidence

三组对照都使用同一个 release entry `vbr1_l1_gain_estimator`，每个 form/mode 重复 3 次：

- `normal_fast`: `profile_fast_skip_source_error_control`
- `whole_python_trace`: `profile_fast_rust_full_model` + `EVAS_RUST_GAIN_TIMER_TRACE=0`
- `whole_rust_trace`: `profile_fast_rust_full_model` + `EVAS_RUST_GAIN_TIMER_TRACE=1`

| Form | Path | PASS repeats | E2E wall median (s) | EVAS tran median (s) | Fastpath flags |
|---|---|---:|---:|---:|---|
| `tb` | normal fast | 3/3 | `0.195646` | `0.027500` | whole=0, gain=0, rust=0 |
| `tb` | Python whole trace | 3/3 | `0.183129` | `0.011700` | whole=1, gain=1, rust=0, points=1921 |
| `tb` | Rust whole trace | 3/3 | `0.179387` | `0.008300` | whole=1, gain=1, rust=1, points=1921 |
| `e2e` | normal fast | 3/3 | `0.192317` | `0.027600` | whole=0, gain=0, rust=0 |
| `e2e` | Python whole trace | 3/3 | `0.179116` | `0.011300` | whole=1, gain=1, rust=0, points=1921 |
| `e2e` | Rust whole trace | 3/3 | `0.177061` | `0.008100` | whole=1, gain=1, rust=1, points=1921 |

| Form | Metric | Python whole speedup vs normal | Rust whole speedup vs normal | Rust trace speedup vs Python trace |
|---|---|---:|---:|---:|
| `tb` | E2E wall | `1.068x` | `1.091x` | `1.021x` |
| `tb` | EVAS tran | `2.350x` | `3.313x` | `1.410x` |
| `e2e` | E2E wall | `1.074x` | `1.086x` | `1.012x` |
| `e2e` | EVAS tran | `2.442x` | `3.407x` | `1.395x` |

Top4 smoke:

```text
selected rows = 4
results = 8
status = 8/8 PASS
gain tb normal fast: wall 0.190920s, tran 0.0273s
gain tb Rust trace: wall 0.179338s, tran 0.0084s, rust_enabled=1
prop-delay/SAR/CPPLL whole-segment rows still use pre-existing paths and are not counted as new 069 Rust coverage.
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- New opt-in switch: `EVAS_RUST_GAIN_TIMER_TRACE=0/1`

If Rust ABI is unavailable or returns an error, engine increments fallback counters and uses the old Python whole-segment trace.

## Completion And Speed Ledger

| Ledger | Before 069 | After 069 | Delta | Meaning |
|---|---:|---:|---:|---|
| B01-B18 general behavior estimate | `30.0%` | `30.0%` | `+0.0 pp` | 通用 Verilog-A 语义没有因为一个 family fastpath 变成 fully implemented |
| Release-row effective production estimate | `30.0%` | `30.6%` | `+0.6 pp` | 新增 `vbr1_l1_gain_estimator` 的 `tb/e2e` 两条 release rows 可走 production Rust trace，约 `2/357` rows |
| `tb` EVAS tran speed | `0.027500s` | `0.008300s` | `3.313x` | 核心 transient loop 明显变快 |
| `e2e` EVAS tran speed | `0.027600s` | `0.008100s` | `3.407x` | 核心 transient loop 明显变快 |
| `tb` E2E wall speed | `0.195646s` | `0.179387s` | `1.091x` | 外层 staging/checker/subprocess 开销占主导 |
| `e2e` E2E wall speed | `0.192317s` | `0.177061s` | `1.086x` | 外层 staging/checker/subprocess 开销占主导 |

这里的 `30.6%` 是工程进度估计，不是论文速度 claim。论文速度仍必须用 same-slice EVAS/Spectre/AX timing。

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile EVAS/evas/simulator/rust_backend.py EVAS/evas/simulator/engine.py EVAS/tests/test_rust_backend.py

cargo test --release

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest EVAS/tests/test_rust_backend.py::test_rust_backend_generates_gain_timer_reduction_trace -q

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS:/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
EVAS_RUST_GAIN_TIMER_TRACE=0 \
python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all --entry vbr1_l1_gain_estimator --form tb \
  --mode profile_fast_rust_full_model \
  --output-root /private/tmp/vaevas_069_gain_pytrace \
  --report-json /private/tmp/vaevas_069_gain_pytrace.json \
  --report-md /private/tmp/vaevas_069_gain_pytrace.md \
  --timeout-s 240 --jobs 1

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS:/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
EVAS_RUST_GAIN_TIMER_TRACE=1 \
python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all --entry vbr1_l1_gain_estimator --form tb \
  --mode profile_fast_rust_full_model \
  --output-root /private/tmp/vaevas_069_gain_rusttrace \
  --report-json /private/tmp/vaevas_069_gain_rusttrace.json \
  --report-md /private/tmp/vaevas_069_gain_rusttrace.md \
  --timeout-s 240 --jobs 1
```

Results:

```text
py_compile: PASS
cargo test --release: 29 passed
gain Rust backend wrapper: 1 passed
single-row Python trace: PASS
single-row Rust trace: PASS
3-repeat tb/e2e A/B: all PASS
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

这里可以把 Rust 化理解成“把一段固定公式和循环搬到更低开销的执行器”。

Python 的优势是灵活：每一步可以用 dict 查节点名、调用对象方法、动态 append list。缺点是这些动作每次都有解释器开销。Rust 的优势是固定：传进来的是连续数组，循环里只是按下标读写 `f64`。当模型行为已经被 compiler 识别成固定结构时，Rust 就能把大量小对象操作变成数组循环。

为什么 E2E wall 没有和 tran 一样 3x？因为这个 benchmark 很短。核心 tran 从二十多毫秒降到八毫秒后，剩下的 release fixture materialization、Python subprocess 启动、CSV/checker、runner 记账变成主导。这个结果反而说明后续要继续扩大 Rust 覆盖到更重的 top-wall rows，或者把 record/checker 外层也批量化。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Rust trace ABI 列顺序和 checker 期望不一致 | gain/valid waveform parity 或 checker FAIL | 关闭 `EVAS_RUST_GAIN_TIMER_TRACE`，回到 Python whole trace |
| semantic matcher 误命中非 gain measurement 模型 | candidate valid 但真实 row FAIL | 收紧 `gain_timer_reduction_v1` contract / collector，并加反例 |
| 小 row E2E 数据被外层噪声掩盖 | tran 变快但 wall 不稳定 | 以 tran core 作为本轮内核证据，release claim 等 same-slice full rerun |
| Rust dylib 版本旧，没有新 symbol | `RustBackendError` fallback counter 增加 | 重新 build Rust core；或临时设 `EVAS_RUST_GAIN_TIMER_TRACE=0` |

## Next Step

下一篇审计文档编号和预期主题：

- `070 - Propagation Delay Whole-Segment Rust Trace`
