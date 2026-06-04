# 075 - Gain Measurement Flow Production Rust

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related files:

- `speed-optimization/reports/rust_gain_measurement_flow_075_20260604.json`
- `speed-optimization/reports/rust_gain_measurement_flow_075_20260604.md`
- `speed-optimization/reports/rust_stage75_topwall_evas_smoke_20260604.json`
- `speed-optimization/reports/rust_stage75_topwall_evas_smoke_20260604.md`
- Raw local artifact: `/private/tmp/vaevas_exp075_gain_flow.json`
- Raw local artifact: `/private/tmp/vaevas_exp075_topwall.json`

## One-Line Summary

把 `vbr1_l2_gain_extraction_convergence_measurement_flow` 的四模型 measurement flow 降成 production Rust whole-segment trace：gain tb/e2e 从 074 的 Python fastpath fallback 变成 Rust55 命中，top-wall 6-row EVAS-only 总 wall 从 normal fast `9.677s` 降到 Rust55 `2.103s`，6/6 PASS 且 6/6 safe_vs_strict。

## What Changed

| Layer | Change | Why It Matters |
|---|---|---|
| Rust core | 新增 `gain_measurement_flow_trace_for_arrays` 和 C ABI `evas_rust_gain_measurement_flow_trace` | 一次 typed-array loop 生成 `vinp/vinn/vamp_p/vamp_n` trace，绕过四个 generated Python model 的每步 evaluate/post-update/output-write |
| Python Rust bridge | 新增 `RustBackend.gain_measurement_flow_trace(...)` | 统一 buffer/length checking，向 Rust 传入 event target arrays 和参数 |
| Simulator engine | 新增 `_try_gain_measurement_flow_fastpath(...)` 并接入 whole-segment dispatch | 在 `evas_rust_full_model_fastpath=true` 下识别 `vin_src + lfsr + dither_adder + gain_amp_fixed` 的连线组合 |
| Tests | 新增 Rust backend unit test | 覆盖初始 dither、vin transition、LFSR shift 后 dither 翻转三个关键时序 |

## Principle

这个 flow 的 Python 热点不是一个单独语句，而是一整段重复行为：

1. `vin_src` 在 clock rising edge 采样 noisy sine，并通过 `transition()` 输出 `vinp/vinn`。
2. `lfsr` 在另一个 clock threshold 上 shift，输出 `DPN` transition。
3. `dither_adder` 每步读 `DPN`，把 dither 加到差分输入。
4. `gain_amp_fixed` 每步把差分输入乘以固定 gain。
5. checker 只保存 `vinp/vinn/vamp_p/vamp_n`。

所以收益来自“整段 trace 合成”，不是把某个小函数翻译成 Rust。Rust path 保留两个真实事件阈值：`vin_src` 用 `vth=0.45`，`lfsr` 源码写死 `0.5`。这点很重要，因为同一个 clock edge 上两个模型实际触发时间相差约几十 ps。

随机数也没有硬搬到 Rust。Python 按 EVAS 当前 `$rdist_normal(SEED,...)` 语义预生成 vin event target，Rust 只消费 target arrays。这样避免 Rust 端复刻 Python `random.Random(seed).gauss()` 的实现细节，先守住 parity。

## Trigger Gate

该 fastpath 不看 benchmark ID 或文件路径。它要求：

- 4 个模型形状分别匹配 `vin_src`、`lfsr`、`dither_adder`、`gain_amp_fixed` 的端口/参数集合；
- 跨模型连线满足 `vin -> dither -> amp`，且 `clk/rst` 在 `vin_src/lfsr` 间一致；
- `save` 信号只属于 `{vinp, vinn, vamp_p, vamp_n}` 对应输出集合；
- Rust backend 可加载，且 `EVAS_RUST_GAIN_MEASUREMENT_FLOW_TRACE` 未关闭。

如果用户保存 `dpn`、`vdin_p` 等内部节点，或者换成不同结构的 measurement flow，该 fastpath 不触发，自动 fallback 到普通 EVAS。

## Targeted Result

Report:

```text
speed-optimization/reports/rust_gain_measurement_flow_075_20260604.md
speed-optimization/reports/rust_gain_measurement_flow_075_20260604.json
```

| Scope | Mode | PASS | Wall s | Tran s | Fastpath |
|---|---|---:|---:|---:|---|
| gain tb+e2e | `strict_current` | 2/2 | `31.836` | `31.242` | off |
| gain tb+e2e | `profile_fast_skip_source_error_control` | 2/2 | `2.531` | `1.975` | off |
| gain tb+e2e | `profile_fast_rust_55` | 2/2 | `1.033` | `0.406` | `gain_measurement_flow` on |

Rust55 vs normal fast total wall speedup on this target is `2.45x`.

Both Rust55 rows reported:

```text
rust_full_model_gain_measurement_flow_enabled = 1
rust_full_model_gain_measurement_flow_rust_enabled = 1
rust_full_model_gain_measurement_flow_vin_events = 998
rust_full_model_gain_measurement_flow_lfsr_events = 998
rust_full_model_gain_measurement_flow_rust_points = 16984
rust_full_model_fastpath_fallbacks_total = 0
```

## Top-Wall Smoke

Report:

```text
speed-optimization/reports/rust_stage75_topwall_evas_smoke_20260604.md
speed-optimization/reports/rust_stage75_topwall_evas_smoke_20260604.json
```

| Mode | PASS | Total wall s | Median speedup vs strict | Safe vs strict |
|---|---:|---:|---:|---:|
| `strict_current` | 6/6 | `125.938` | `1.00x` | baseline |
| `profile_fast_skip_source_error_control` | 6/6 | `9.677` | `12.94x` | 6/6 |
| `profile_fast_rust_55` | 6/6 | `2.103` | `53.59x` | 6/6 |

Rust55 vs normal fast total wall speedup on this EVAS-only top-wall slice is `4.60x`.

Gain rows in the top-wall smoke:

| Row | Normal fast wall s | Rust55 wall s | Rust55 / fast |
|---|---:|---:|---:|
| gain measurement flow e2e | `1.249` | `0.282` | `4.42x` |
| gain measurement flow tb | `1.181` | `0.285` | `4.14x` |

## Correctness Gate

All rows were checked against `strict_current`. Gain extraction uses dither/noise-like stimulus, so the runner uses functional gain metric parity instead of raw pointwise waveform parity:

```text
gain_gate = evas_gain>4 and spectre_gain>4 and relative_gain_delta<=0.25
```

Rust55 gain rows passed with relative gain delta about `0.00512`, well inside the gate. This is an EVAS-only strict-parity engineering result, not a Spectre AX paper claim.

## Remaining Limits

This is still not full release Rustification:

- The trigger is a production fastpath for this flow shape, not a general Verilog-A compiler for all event/evaluate behavior.
- Internal nodes beyond the saved measurement signals are not emitted by this trace path.
- PFD in the current top-wall slice still has no whole-segment Rust fastpath; it is small, so it is not the next major speed blocker.
- Spectre AX speed claim remains closed until same-server/same-slice Spectre AX and EVAS Rust55 rerun.

## Validation

Commands run:

```bash
cargo build --release

PYTHONPATH=EVAS \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_075 \
python3 -m pytest EVAS/tests/test_rust_backend.py \
  -k 'gain_measurement_flow or gain_timer_reduction' -q

PYTHONPATH=EVAS:behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_075 \
python3 behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact behavioral-veriloga-eval/speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --entry vbr1_l2_gain_extraction_convergence_measurement_flow \
  --mode strict_current \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_55 \
  --output-root /private/tmp/vaevas_exp075_gain_flow \
  --report-json /private/tmp/vaevas_exp075_gain_flow.json \
  --report-md /private/tmp/vaevas_exp075_gain_flow.md \
  --timeout-s 300 --jobs 1

PYTHONPATH=EVAS:behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_075 \
python3 behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact behavioral-veriloga-eval/speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite top-wall --limit 6 \
  --mode strict_current \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_55 \
  --output-root /private/tmp/vaevas_exp075_topwall \
  --report-json /private/tmp/vaevas_exp075_topwall.json \
  --report-md /private/tmp/vaevas_exp075_topwall.md \
  --timeout-s 300 --jobs 1
```

Results:

```text
Rust build: PASS
targeted pytest: 2 passed, 29 deselected
gain-flow targeted runner: 2/2 PASS, 2/2 Rust55 safe_vs_strict
top-wall smoke: 6/6 PASS, 6/6 Rust55 safe_vs_strict
```
