# 071 - SAR Loop Production Rust

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_sar_loop_trace_071_20260604.json`
- `speed-optimization/reports/rust_sar_loop_trace_071_20260604.md`
- `speed-optimization/reports/_tmp_rust_sar_loop_071_r3_*.json`

## One-Line Summary

把 weighted SAR ADC + weighted DAC + rising sample-hold 的 whole-segment loop 从 Python production fastpath 迁到 Rust ABI；真实 `vbr1_l2_weighted_sar_adc_dac_loop` tb/e2e 3-repeat 全 PASS。tb 的 EVAS tran median `3.0981s -> 0.1071s`，E2E wall median `6.7422s -> 5.3224s`；e2e 的 EVAS tran median `2.4973s -> 0.1390s`，但 E2E wall median `5.5161s -> 5.9844s`，外层开销和负载波动吞掉了核心收益。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust core | SAR whole-segment trace 只有 Python executor | 新增 `sar_loop_trace_for_arrays()` 和 `evas_rust_sar_loop_trace` | 默认仿真不变 |
| Python Rust wrapper | `RustBackend` 不能调用 SAR trace | 新增 `RustBackend.sar_loop_trace()`，固定 `11 + width` 列输出 ABI | 默认仿真不变 |
| Engine dispatch | `weighted_sar_adc_v1` + `weighted_dac_v1` + `sample_hold_rising_v1` whole-segment executor 在 Python loop 中跑 | opt-in whole-model mode 下优先调用 Rust SAR trace；失败 fallback Python | checker/CSV/strobe 行为不变 |
| A/B control | 只能比较 normal fast 和 whole-model mode，不能区分 Python/Rust SAR loop | 新增 `EVAS_RUST_SAR_LOOP_TRACE=0/1` | 仅用于审计和回归 |
| coverage map | production whole-segment ABI 登记到 PRBS/gain/cmp-delay | 新增 `evas_rust_sar_loop_trace` | 文档/manifest 可读性提升 |

## Principle

这一步迁移的是一整段固定行为，不是一个小 helper：

1. `sample_hold_rising_v1` 在 clock 上升沿采样输入，用 `transition()` 输出 `vin_sh`。
2. `weighted_sar_adc_v1` 在 clock 下降沿启动转换，在后续上升沿逐位比较。
3. SAR 状态包含 `dout_bits[]`、`trial_bits[]`、`bit_idx`、`busy`、`vsampled`、`trial_vdac`、`cmp_decision`、`conv_done`。
4. `weighted_dac_v1` 把 `dout_bits[]` 映射成 DAC output。
5. Rust 在一个 flat loop 里同时完成 clock edge detection、event body、state update、transition output evaluation 和 trace matrix 写入。

Python 仍负责 candidate 语义/数据流匹配、source waveform 预采样、runner staging、CSV/checker 和 final report。因此这不是“全 EVAS 已经 Rust 化”，而是一个 top-wall 语义族的 production Rust executor。

## Before / After Evidence

三组对照都使用 `vbr1_l2_weighted_sar_adc_dac_loop` 的 release tb/e2e forms，每组重复 3 次：

- `normal_fast`: `profile_fast_skip_source_error_control`
- `python_whole`: `profile_fast_rust_full_model` + `EVAS_RUST_SAR_LOOP_TRACE=0`
- `rust_whole`: `profile_fast_rust_full_model` + `EVAS_RUST_SAR_LOOP_TRACE=1`

| Form | PASS repeats | Normal wall median (s) | Normal tran median (s) | Rust wall median (s) | Rust tran median (s) | Rust points | Rust fallbacks |
|---|---:|---:|---:|---:|---:|---:|---:|
| `tb` | 9/9 | `6.742162` | `3.098100` | `5.322417` | `0.107100` | 18002 | 0 |
| `e2e` | 9/9 | `5.516133` | `2.497300` | `5.984390` | `0.139000` | 18002 | 0 |

| Form | Metric | Python whole speedup vs normal | Rust whole speedup vs normal | Rust trace speedup vs Python trace |
|---|---|---:|---:|---:|
| `tb` | E2E wall | `0.949x` | `1.267x` | `1.334x` |
| `tb` | EVAS tran | `14.205x` | `28.927x` | `2.036x` |
| `e2e` | E2E wall | `0.779x` | `0.922x` | `1.183x` |
| `e2e` | EVAS tran | `6.317x` | `17.966x` | `2.844x` |

Interpretation:

- 核心 simulator tran loop 明显变快，说明 Rust SAR executor 是有效的。
- tb 的 E2E wall 有可见收益。
- e2e 的 E2E wall 没有赢 normal fast，说明该 form 当前由外层固定成本、source array packing、CSV/checker 或本机负载波动主导。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- New opt-in switch: `EVAS_RUST_SAR_LOOP_TRACE=0/1`

Rust fallback increments `rust_full_model_sar_loop_rust_fallbacks` and returns to the old Python whole-segment executor.

## Completion And Speed Ledger

| Ledger | Before 071 | After 071 | Delta | Meaning |
|---|---:|---:|---:|---|
| B01-B18 general behavior estimate | `30.0%` | `30.0%` | `+0.0 pp` | 通用 Verilog-A 语义仍没有完全 Rust 化 |
| Release-row effective production estimate | `31.4%` | `32.0%` | `+0.6 pp` | 新增 SAR tb/e2e 两条 release rows 可走 production Rust trace，约 `2/357` rows |
| `tb` EVAS tran speed | `3.098100s` | `0.107100s` | `28.927x` | 核心 transient loop 大幅变快 |
| `tb` E2E wall speed | `6.742162s` | `5.322417s` | `1.267x` | 该 form 的核心收益能部分转化为 E2E |
| `e2e` EVAS tran speed | `2.497300s` | `0.139000s` | `17.966x` | 核心 transient loop 大幅变快 |
| `e2e` E2E wall speed | `5.516133s` | `5.984390s` | `0.922x` | 外层成本和测量波动大于核心收益 |
| Rust trace vs Python whole trace | `0.218100s` / `0.395300s` | `0.107100s` / `0.139000s` | `2.036x` / `2.844x` | 同一 whole-segment 语义下 Rust loop 比 Python loop 快 |

这里的 `32.0%` 仍是工程进度估计，不是论文速度 claim。

## Validation

Commands run:

```bash
cargo test --release

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_071 \
python3 -m py_compile \
  EVAS/evas/simulator/engine.py \
  EVAS/evas/simulator/rust_backend.py \
  EVAS/tests/test_rust_backend.py

PYTHONPATH=EVAS \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_071 \
python3 -m pytest EVAS/tests/test_rust_backend.py -q

python3 <local smoke runner>   # one-repeat normal/Python-whole/Rust-whole on SAR tb/e2e

python3 <local repeat runner>  # three-repeat normal/Python-whole/Rust-whole on SAR tb/e2e
```

Results:

```text
cargo test --release: 29 passed
py_compile: PASS with PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_071
pytest EVAS/tests/test_rust_backend.py -q: 29 passed
SAR smoke: tb/e2e PASS, Rust enabled, fallback 0
SAR 3-repeat A/B: tb/e2e all PASS, Rust enabled, fallback 0
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

071 比 069 更能说明 Rust 化的真正收益来源：Python whole-segment 已经绕开了很多普通 engine 开销，但它仍要在 Python 里逐点执行 state machine、transition 和多列记录。Rust 把这些合成一个 typed-array loop 后，SAR tran 又能快 `2.0x` 到 `2.8x`。

但 e2e wall 没有稳定赢 normal fast，说明当前剩余瓶颈已经从“核心状态机 loop”转移到更外层：

- source waveform 数组预采样仍在 Python；
- trace matrix 回填到 Python columns 仍在 Python；
- runner staging、subprocess startup、CSV/checker 仍计入 E2E wall；
- 本地机器负载波动会显著影响几秒级 wall。

下一阶段如果继续只迁小段 Rust，E2E 很可能看不到明显收益。更有效的是把 source sampling、record/CSV、checker 必需列裁剪或整个 trace finalization 一起 array 化。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| SAR event ordering 与 Python 不一致 | `conv_done`、`dout[]` 或 DAC waveform parity 失败 | 关闭 `EVAS_RUST_SAR_LOOP_TRACE`，回到 Python whole trace |
| transition retarget corner case 缺失 | `vin_sh`、DAC output 或 bit outputs 边沿偏离 | 扩展 Rust transition primitive 单测 |
| semantic matcher 误命中非 weighted SAR 模型 | candidate valid 但真实 row FAIL | 收紧 `weighted_sar_adc_v1` / `weighted_dac_v1` / `sample_hold_rising_v1` contract |
| Rust dylib 版本旧，没有新 symbol | fallback counter 增加 | 重新 build Rust core；或临时设 `EVAS_RUST_SAR_LOOP_TRACE=0` |

## Next Step

下一篇审计文档编号和预期主题：

- `072 - CPPLL Reacquire Production Rust Trace`
- 或先做 `source sampling + record matrix` array 化，减少 069/071 暴露出来的 E2E 外层瓶颈。
