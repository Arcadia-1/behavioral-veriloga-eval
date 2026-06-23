# 076 - Current Rustification Status After Gain Flow

Status: `done`
Date: `2026-06-04`

## 结论

还没有完成全量 Rust 迁移。

现在有两个必须分开的口径：

| 口径 | 当前结果 | 含义 |
|---|---:|---|
| Release-wide 通用语义 Rustification | `30.0%` | 按 B01-B18 通用 EVAS 行为估算，很多行为仍是 partial/shadow/Python fallback |
| Top-wall 10 EVAS-only Rust55 engineering speed | `13.264s -> 3.250s`，`4.08x` | 这批最慢样本大多已经命中 production whole-segment Rust，但不能代表全 release 全语义已 Rust 化 |

所以更准确的说法是：

- 可以说：top-wall 热点 production Rust 覆盖已经明显提升，当前 top-wall 10 EVAS-only Rust55 比 normal fast 快约 `4.08x`。
- 不可以说：EVAS 已经全量 Rust 化。
- 不可以说：已经 paper-facing 地快于 Spectre AX。这个仍需要 same-slice、同机/同配置的 EVAS Rust55 vs Spectre AX rerun。

## 本轮补充

这轮没有再改仿真数学语义，而是补了两个工程证据缺口：

1. 重新跑当前代码 top-wall 10 EVAS-only strict/fast/Rust55。
2. 修正 release Rust coverage manifest 的盲点：075 的 gain measurement flow 是跨 `vin_src + lfsr + dither_adder + gain_amp_fixed` 四个模型的 whole-flow fastpath，旧 manifest 只扫描单个 compiled model，所以漏报。

新增 manifest 字段：

```text
whole_flow_fastpath_counts:
  gain_measurement_flow_v1 = 2 release forms
```

这只是 source-shape candidate。真正是否启用 Rust 仍由 simulator runtime gate 检查连线、source waveform、参数和 recorded signals。

## Evidence

Reports:

- `speed-optimization/reports/rust_stage76_topwall10_current_20260604.json`
- `speed-optimization/reports/rust_stage76_topwall10_current_20260604.md`
- `speed-optimization/reports/current_release_rust_coverage_manifest_20260604.json`
- `speed-optimization/reports/current_release_rust_coverage_manifest_20260604.md`

Top-wall 10 rerun:

| Mode | PASS | Wall s | Safe vs strict |
|---|---:|---:|---:|
| `strict_current` | `10/10` | `173.040` | n/a |
| `profile_fast_skip_source_error_control` | `10/10` | `13.264` | `10/10` |
| `profile_fast_rust_55` | `10/10` | `3.250` | `10/10` |

Rust55 vs normal fast total wall speedup on this EVAS-only slice:

```text
13.263644837 / 3.250313751 = 4.08x
```

## Row Breakdown

| Row | Form | Fast wall s | Rust55 wall s | Fast/Rust55 | Rust path |
|---|---|---:|---:|---:|---|
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `2.791` | `0.612` | `4.56x` | `sar_loop` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `2.953` | `0.585` | `5.05x` | `cppll_reacquire` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `2.530` | `0.548` | `4.62x` | `cppll_reacquire` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `1.446` | `0.288` | `5.03x` | `gain_measurement_flow` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `1.151` | `0.286` | `4.02x` | `gain_measurement_flow` |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `0.420` | `0.204` | `2.06x` | `prbs7/lfsr transition` |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `1.407` | `0.184` | `7.63x` | `cmp_delay` |
| `vbr1_l1_gain_estimator` | `e2e` | `0.201` | `0.184` | `1.09x` | `gain_timer_reduction` |
| `vbr1_l1_gain_estimator` | `tb` | `0.191` | `0.182` | `1.05x` | `gain_timer_reduction` |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `0.174` | `0.177` | `0.98x` | fallback / no whole-segment Rust |

## 怎么理解现在的剩余瓶颈

075 之后，top-wall 10 里的主要重 row 已经不再是“完全没进 Rust”。最慢的几个 Rust55 row 反而都已经启用了 production whole-segment Rust：

- SAR: `rust_full_model_sar_loop_rust_enabled = 1`
- CPPLL: `rust_full_model_cppll_reacquire_rust_enabled = 1`
- Gain measurement-flow: `rust_full_model_gain_measurement_flow_rust_enabled = 1`

这说明下一阶段如果只继续把这些相同模型的核心 loop 用 Rust 重写一遍，收益会变小。更可能的收益来源是：

1. trace/record path：减少 Rust flat matrix -> numpy -> Python list -> CSV 的多次拷贝。
2. CSV/checker path：对已知 checker 必需信号做 sparse/required-signal trace。
3. runner subprocess fixed cost：小 row 的 tran 已经只有毫秒级，E2E wall 主要是进程、文件、checker、清理这些固定开销。
4. release-wide fallback coverage：PFD、一般 event body、一般 transition/evaluate、system task/random/file side effects 仍没有全量 production Rust。

## 后续方向

下一步优先级应从“再补一个同类 whole-segment kernel”转成：

1. 077: Whole-segment trace/record zero-copy path。
   - 目标：让 Rust trace 结果尽量直接进入 `SimResult`/CSV writer，少走 Python list。
   - 预期：主要帮助 SAR/CPPLL/gain-flow 这些已 Rust 化但仍有较多 trace 点的 row。
2. 078: Required-signal/sparse trace path。
   - 目标：只输出 checker 真实需要的信号，避免生成和写出不会被检查的列。
   - 风险：必须保持 release checker contract，不能为了速度漏掉用户显式 save 的信号。
3. 079: PFD/event small-row fallback audit。
   - 目标：确认 PFD 是否值得 production Rust，还是应该保持 fallback，因为它已经只有 `~0.177s`。
4. 080+: Release-wide behavior Rustification。
   - 目标：继续推进 B01-B18 中的 event ordering、transition production、dynamic bus、system task/random/file side-effect 边界。
