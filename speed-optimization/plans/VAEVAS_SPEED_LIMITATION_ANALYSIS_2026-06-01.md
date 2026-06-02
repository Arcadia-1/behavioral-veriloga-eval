# EVAS 速度限制问题分析

- 日期：2026-06-01
- 主数据源：
  - 最新统一复测：`speed-optimization/reports/e2e_wall_unified_full_20260602_r14_core_fastpath_exactrows.json`
  - r14 exact-row 派生 manifest：`speed-optimization/reports/e2e_wall_unified_rows_from_r14_exactrows_20260602.json`
  - timer-cache 后 EVAS-only exact-row 诊断：`speed-optimization/reports/e2e_wall_unified_full_20260602_r15b_timer_cache_evas_only_r14_exactrows.json`
  - CSV writer 后 EVAS-only exact-row 诊断：`speed-optimization/reports/e2e_wall_unified_full_20260602_r16_csv_writer_evas_only_r14_exactrows.json`
  - measurement-heavy profile：`speed-optimization/reports/e2e_wall_profile_20260602_r18_measurement_heavy.json`
  - `_prepare_step` 引用复用 profile：`speed-optimization/reports/e2e_wall_profile_20260602_r19_prepare_breakpoint.json`
  - capability prefilter profile：`speed-optimization/reports/e2e_wall_profile_20260602_r20_capability_prefilter.json`
  - node-map cache 否定 profile：`speed-optimization/reports/e2e_wall_profile_20260602_r22_node_map_cache.json`
  - capability prefilter 后 EVAS-only exact-row 诊断：`speed-optimization/reports/e2e_wall_unified_full_20260602_r21b_capability_prefilter_evas_only_r14_exactrows.json`
  - gain-estimator streaming checker 后 EVAS-only exact-row 诊断：`speed-optimization/reports/e2e_wall_unified_full_20260602_r24_gain_estimator_streaming_evas_only_r14_exactrows.json`
  - CDAC streaming checker 后 EVAS-only exact-row 诊断：`speed-optimization/reports/e2e_wall_unified_full_20260602_r25_cdac_streaming_evas_only_r14_exactrows.json`
  - LFSR/PRBS7 streaming checker 后 EVAS-only exact-row 诊断：`speed-optimization/reports/e2e_wall_unified_full_20260602_r26_lfsr_streaming_evas_only_r14_exactrows.json`
  - r26 CDAC/LFSR/PRBS7 real-CSV parity：`speed-optimization/reports/streaming_checker_parity_20260602_r26_cdac_lfsr_prbs7/parity.json`
  - edge-interval streaming checker 后 EVAS-only exact-row 诊断：`speed-optimization/reports/e2e_wall_unified_full_20260602_r28_edge_interval_streaming_evas_only_r14_exactrows.json`
  - r28 edge-interval real-CSV parity：`speed-optimization/reports/streaming_checker_parity_20260602_r28_edge_interval/parity.json`
  - BBPD streaming checker 后 EVAS-only exact-row 诊断：`speed-optimization/reports/e2e_wall_unified_full_20260602_r30_bbpd_streaming_evas_only_r14_exactrows.json`
  - r30 BBPD real-CSV parity：`speed-optimization/reports/streaming_checker_parity_20260602_r30_bbpd/parity.json`
  - 最新统一复测对照：`speed-optimization/reports/e2e_wall_unified_full_20260602_r8_streaming_aliases_exactrows.json`
  - r14 前局部 no-profile smoke：`speed-optimization/reports/e2e_wall_unified_smoke_20260602_r12_no_profile_core.json`
  - r14 voltage fastpath smoke：`speed-optimization/reports/e2e_wall_unified_smoke_20260602_r13_voltage_fastpath.json`
  - r8 streaming alias parity：`speed-optimization/reports/streaming_checker_parity_20260602_r8_aliases_on_r7_csv/parity.json`
  - 前一版统一复测：`speed-optimization/reports/e2e_wall_unified_full_20260602_r7_src_err_cache_exactrows.json`
  - 低风险内核/IO 优化后同 row-set 复测：`speed-optimization/reports/e2e_wall_unified_full_20260602_r6_kernel_lowrisk_exactrows.json`
  - 低风险内核/IO 优化前同 row-set 复测：`speed-optimization/reports/e2e_wall_unified_full_20260602_r5_fast_ax_strictref.json`
  - 优化前基线：`speed-optimization/reports/e2e_wall_unified_full_20260601_r3.json`
  - checker 长尾优化后 rerun：`speed-optimization/reports/e2e_wall_unified_full_20260601_r4_streaming.json`
- 辅助历史数据源：`speed-optimization/reports/precision_ranking_full_e2e_equalized_20260526.json`
- 样本：r14、r8、r7、r6 与 r5 是完全相同的 vaBench release gold mixed-form 64-row slice；
  r3/r4 为历史 e2e 64-row slice
- 参考口径：`Spectre strict` 作为精度参考，`Spectre AX equalized` 作为商业加速基线

## 当前结论：r14 统一复测

2026-06-02 r14 是当前速度判断的最新 full exact-row 口径。运行方式仍是
用户要求的 `thu-sui` 上 `python3` runner；Spectre 通过 `thu-sui` wrapper
调用 `thu-wei` Cadence/Spectre 21.1.0.509.isr12。row manifest 与 r8/r7/r6/r5
完全一致，all rows 为 64/64，paper-facing valid rows 为 43/43。

r14 包含三类 EVAS core micro-optimization：

- 对 cross exact-touch 的 future node value 改为 lazy lookup，避免每步构造完整
  future node-voltage dict。
- 在 `_prepare_step` 中预计算 future-node 需求，并去掉重复 previous snapshot copy。
- 为普通 node-map 路径增加 `@parent:` 判断快路径，减少无意义 `startswith()` 调用。

这些优化均不改变 checker、容差、步长或 EVAS 数值语义。验证结果是：r14 的 PASS
集合与 r8 一致，EVAS fast 仍为 43/64 behavior PASS，AX/strict 为 45/64；
paper-facing valid rows 仍为 43/43。因此没有引入新的 checker regression。

但 r14 full rerun **没有证明 EVAS 全量速度进一步提升**：局部 no-profile smoke
显示 measurement-heavy 行的 EVAS subprocess 有约 0.17-0.34s/行下降，但在 full
64-row 并发 rerun 中，这些收益被运行波动、CSV/fixture/checker 开销和未优化的
`model_evaluate`/timer-breakpoint 长尾抵消。当前 paper-facing 速度 claim 应使用
r14 full 表，而不是局部 smoke。

结论：

1. **all64 E2E**：EVAS fast 仍快于 Spectre AX。EVAS fast 为 214.597s，
   Spectre AX 为 330.908s，`T(AX)/T(EVAS fast)=1.542x`。
2. **paper-facing valid43 E2E**：EVAS fast 仍快于 Spectre AX。EVAS fast
   为 117.394s，Spectre AX 为 199.305s，`T(AX)/T(EVAS fast)=1.698x`。
3. **simulator subprocess**：EVAS fast 仍明显快于 Spectre AX。all64 中
   EVAS fast subprocess 为 100.368s，Spectre AX subprocess 为 208.065s，
   `T(AX subprocess)/T(EVAS subprocess)=2.073x`；valid43 中为 68.994s
   vs 143.595s，速度比 2.081x。
4. **精度/等价**：r14 PASS 集合与 r8 一致。仍不能声明 EVAS fast 比 AX 更精准；
   保守口径仍是“EVAS fast 在 paper-facing valid rows 上通过同一 behavior checker，
   但 AX 对 strict Spectre reference 的 waveform gate 更完整”。
5. **优化解释**：r14 说明当前剩余瓶颈不在 future snapshot 这一处。下一步应优先
   profile/优化 `model_evaluate` 中的 `_get_voltage()`、`transition()`、
   timer/breakpoint 扫描，以及 CSV 输出；不要把 r12 局部 smoke 写成 full-run
   speedup。

| Scope | EVAS fast E2E wall | Spectre AX E2E wall | AX/EVAS E2E | EVAS subprocess | AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | 214.597s | 330.908s | 1.542x | 100.368s | 208.065s | 2.073x |
| paper-facing valid43 | 117.394s | 199.305s | 1.698x | 68.994s | 143.595s | 2.081x |

Timing split：

| Scope | Mode | E2E wall | Subprocess | Checker | Fixture | CSV/PSF parse |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| all64 | EVAS fast | 214.597s | 100.368s | 73.199s | 32.801s | 11.532s CSV |
| all64 | Spectre AX | 330.908s | 208.065s | 59.802s | 39.885s | 21.900s PSF |
| valid43 | EVAS fast | 117.394s | 68.994s | 20.131s | 22.574s | 7.737s CSV |
| valid43 | Spectre AX | 199.305s | 143.595s | 11.702s | 28.291s | 14.944s PSF |

r14 相比 r8：

| Scope | Mode | E2E wall delta | Subprocess delta | Interpretation |
| --- | --- | ---: | ---: | --- |
| all64 | EVAS fast | +3.261s | +0.628s | full-run 中 micro-opts 未形成总体加速 |
| valid43 | EVAS fast | +4.164s | +0.358s | valid rows 仍快于 AX，但不能 claim r14 比 r8 更快 |
| all64 | Spectre AX | -7.470s | -1.443s | Spectre 侧运行波动/fixture 差异也明显 |
| valid43 | Spectre AX | -5.350s | +2.015s | 单次 full rerun 需 repeated cold/warm runs 稳定 |

当前可用口径：

> 在 r14 统一复测下，EVAS fast 在 simulator subprocess 与统一 E2E wall
> 两个口径下仍快于 Spectre AX：valid43 E2E 为 117.394s vs 199.305s，
> 速度比 1.698x；valid43 subprocess 为 68.994s vs 143.595s，速度比 2.081x。
> r14 没有改变 PASS 集合，也没有证明新增 micro-opts 带来 full-run 总体加速。
> 正式论文 claim 仍需要 repeated cold/warm runs 支撑。

## 2026-06-02 增量诊断：r15/r16

r15 原计划是在 Cadence 环境下做 full EVAS-vs-Spectre AX/strict rerun，但
Spectre 子进程在 `spectre.out` 中反复记录：

```text
Waiting for available license for Spectre.
```

随后 AX/strict 子任务接近 harness timeout 后 FAIL。这个结果不是有效速度数据，
因为 wall time 被 license checkout/queue 污染，不能写进 EVAS-vs-AX 最终速度表。
对比 r14 成功日志可见，正常 Spectre run 会 checkout
`Virtuoso_Multi_mode_Simulation` 和 `Spectre_X_MMSIM_Lk`，并在几十毫秒级完成
licensing；r15 的 checkout wait 明显不是仿真器本身运行时间。

同时发现 `e2e_wall_unified_rows_20260601.json` 是 64 个 e2e form 条目，
不是 r14/r8 使用的 mixed-form 64-row exact slice。为避免 row-set 混淆，已从 r14
EVAS result 反推出新的 exact-row manifest：
`e2e_wall_unified_rows_from_r14_exactrows_20260602.json`，其 form 分布为
`tb=20, e2e=19, bugfix=13, dut=12`，与 r14 完全一致。

因此本节只把 r15b/r16 作为 **EVAS-only exact-row 诊断**：

- r15b：在 r14 exact-row manifest 上，只跑 EVAS fast，包含 timer-breakpoint
  cache。
- r16：在相同 exact-row manifest 上，只跑 EVAS fast，额外启用 NumPy batch CSV
  writer。
- Spectre AX/strict 对照仍沿用最近一次有效的 r14 full rerun；当前不能把 r15b/r16
  宣称为 fresh same-run Spectre comparison。

### r15b：timer-breakpoint cache

timer-breakpoint cache 对局部 CPPLL/ADPLL smoke 有效，但在 full exact-row 诊断中
没有形成总量收益。r15b 与 r14 的 PASS 集合一致，均为 43/64 behavior PASS；
这说明该优化没有改变行为判定。但 r15b 的 EVAS-only wall/subprocess 比 r14 更慢，
主要慢在 measurement-heavy 行和 checker wall 波动。

| Scope | Run | EVAS E2E wall | EVAS subprocess | Checker | Fixture | CSV | PASS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | r14 | 214.597s | 100.368s | 73.199s | 32.801s | 11.532s | 43/64 |
| all64 | r15b | 260.055s | 123.152s | 93.365s | 36.419s | 11.563s | 43/64 |
| valid43 | r14 | 117.394s | 68.994s | 20.131s | 22.574s | 7.737s | 43/43 |
| valid43 | r15b | 149.144s | 83.864s | 38.628s | 22.805s | 7.744s | 43/43 |

结论：timer cache 可以保留为低风险优化，但不能作为 full-run speedup claim。下一步
如果继续优化 timer/cross，需要在 kernel profile 中证明每步扫描确实是主项；当前
full-run 主项仍是 measurement-heavy subprocess、checker/harness、CSV。

### r16：CSV writer

r16 只改变 CSV 写出路径：默认使用 NumPy batch writer，保留
`EVAS_CSV_WRITER=python` fallback。该改动不改变仿真步进、事件调度、checker 判定或
数值语义；本地完整 EVAS tests 已通过，远端 CSV writer 目标测试通过。远端
`test_netlist.py` 全量失败是因为本地 test 文件包含远端尚未同步的 parser 回归测试，
不是 CSV writer 本身失败；本轮没有同步 unrelated parser 改动。

CSV writer 的全量效果是明确的：

| Scope | Run | EVAS E2E wall | EVAS subprocess | Checker | Fixture | CSV | PASS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | r15b | 260.055s | 123.152s | 93.365s | 36.419s | 11.563s | 43/64 |
| all64 | r16 | 248.039s | 116.895s | 94.289s | 30.759s | 6.334s | 43/64 |
| valid43 | r15b | 149.144s | 83.864s | 38.628s | 22.805s | 7.744s | 43/43 |
| valid43 | r16 | 142.916s | 79.937s | 40.971s | 17.940s | 4.268s | 43/43 |

r16 相比 r15b：

| Scope | E2E wall change | Subprocess change | CSV change | Interpretation |
| --- | ---: | ---: | ---: | --- |
| all64 | -12.016s / 1.048x faster | -6.257s / 1.054x faster | -5.229s / 0.548x | CSV 明确下降，但 checker 仍是大头 |
| valid43 | -6.228s / 1.044x faster | -3.927s / 1.049x faster | -3.476s / 0.551x | CSV 优化有效但只带来小幅 E2E 收益 |

用 r16 EVAS-only 结果与最近一次有效 r14 Spectre 对照，仅作为诊断口径：

| Scope | EVAS r16 E2E | r14 Spectre AX E2E | AX/EVAS E2E | EVAS r16 subprocess | r14 AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| valid43 | 142.916s | 199.305s | 1.395x | 79.937s | 143.595s | 1.796x |

注意：这张表不是 fresh same-run Spectre rerun；它只说明在相同 r14 exact-row
切片上，CSV 优化后 EVAS 仍快于最近一次有效 AX 对照，但正式 paper-facing
速度表仍应等 Cadence license checkout 恢复后再做 repeated cold/warm same-run。

### r18-r20：measurement-heavy profile 与每步扫描预筛

r18/r19/r20 都只跑两个 measurement-heavy e2e 行：

- `vbr1_l1_gain_estimator/e2e`
- `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e`

它们是 r16 中真正偏慢的 EVAS kernel 代表。这里的目的是定位 subprocess 内部时间，
不是生成 paper-facing EVAS-vs-Spectre 速度表；因此 Spectre-equivalence gate 显示为
`BLOCKED` 是预期的，因为本 profile run 没有同时跑 strict/AX reference。

r19 将 `_prepare_step` 的 current-node snapshot 从 `dict(curr_node_voltages)` 改为
引用复用；r20 进一步做 capability prefilter：

- 编译出的模型标记是否可能产生 `transition/cross/above/timer` dynamic breakpoint。
- 编译出的模型标记是否使用 `$bound_step`。
- engine 只对可能产生 breakpoint 或 bound-step limit 的模型做每步扫描。
- cross/above fired 状态在模型 evaluate loop 中顺手收集，避免额外每步全模型
  `any(getattr(...))` 扫描。

这些优化不改变步长策略、容差、checker 或模型表达式求值，只减少“确定不会发生”的
检查。手写模型仍保守扫描；如果手写模型覆盖 `next_breakpoint()`，仍会被扫描。

| Row | Run | E2E wall | EVAS subprocess | `model_prepare_step_s` | `model_breakpoint_scan_s` | `cross_above_scan_s` | `bound_step_scan_s` |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gain estimator | r18 baseline profile | 11.878s | 10.531s | 0.990s | 0.880s | 0.150s | 0.070s |
| gain estimator | r19 prepare-step ref | 12.088s | 10.832s | 0.829s | 0.935s | 0.155s | 0.075s |
| gain estimator | r20 capability prefilter | 11.245s | 10.193s | 0.777s | 0.679s | 0.022s | 0.023s |
| gain extraction | r18 baseline profile | 12.012s | 10.575s | 0.991s | 0.888s | 0.147s | 0.068s |
| gain extraction | r19 prepare-step ref | 11.504s | 10.301s | 0.793s | 0.864s | 0.158s | 0.069s |
| gain extraction | r20 capability prefilter | 10.679s | 9.619s | 0.793s | 0.683s | 0.022s | 0.020s |

相对 r19，r20 的直接收益：

| Row | E2E wall change | Subprocess change | Main source |
| --- | ---: | ---: | --- |
| gain estimator | -0.843s / 1.075x faster | -0.639s / 1.063x faster | breakpoint/cross/bound-step scan 下降约 0.46s |
| gain extraction | -0.825s / 1.077x faster | -0.682s / 1.071x faster | breakpoint/cross/bound-step scan 下降约 0.39s |

解释：

- r19 证明 Python dict/object 开销中 `_prepare_step` copy 是实项：两条行
  `model_prepare_step_s` 分别下降约 0.16s 和 0.20s。
- r20 证明 timer/breakpoint/bound-step 每步扫描是实项：`cross_above_scan_s`
  从约 0.15s 降到约 0.02s，`bound_step_scan_s` 从约 0.07s 降到约 0.02s，
  `model_breakpoint_scan_s` 下降约 0.18-0.26s。
- 剩余最大项仍是 `model_evaluate_s`，两条行约 3.76-3.86s；下一阶段应该进入
  generated evaluate code 的 `_get_voltage()`、`_set_output()`、state dict/array
  lookup 与 transition/timer 调用路径。

### r21b：capability prefilter exact-row EVAS-only 全量诊断

r21b 在 r14 exact-row manifest 上重跑 64 行 EVAS-only，`jobs=4`，不跑 Spectre。
这仍不是 fresh same-run AX/strict 对照，但可以衡量 r19/r20 EVAS 内核优化在全量
row-set 上的收益。注：一次误跑 r21 未显式设置 `--limit 64`，runner 默认
`--limit 2`，只选了 2 行；该报告不作为全量数据，正式诊断使用 r21b。

r21b 的 PASS 集合与 r14/r16 一致，仍为 43/64 behavior PASS，说明本轮优化没有改变
behavior checker 判定。

| Scope | Run | EVAS E2E wall | EVAS subprocess | Checker | Fixture | CSV | PASS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | r16 CSV writer | 248.039s | 116.895s | 94.289s | 30.759s | 6.334s | 43/64 |
| all64 | r21b capability prefilter | 236.720s | 97.526s | 97.849s | 33.225s | 6.394s | 43/64 |
| valid43 | r16 CSV writer | 142.916s | 79.937s | 40.971s | 17.940s | 4.268s | 43/43 |
| valid43 | r21b capability prefilter | 138.825s | 66.809s | 42.321s | 24.177s | 4.292s | 43/43 |

r21b 相比 r16：

| Scope | E2E wall change | Subprocess change | Checker change | Fixture change | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| all64 | -11.319s / 1.048x faster | -19.369s / 1.199x faster | +3.560s | +2.466s | kernel/subprocess 有明确收益，E2E 被 checker/fixture 抵消一部分 |
| valid43 | -4.091s / 1.029x faster | -13.128s / 1.197x faster | +1.350s | +6.237s | valid rows 的 simulator 核心更快，但 E2E 长尾仍在 harness/checker |

用 r21b EVAS-only 与最近一次有效 r14 Spectre AX 对照，仅作为诊断口径：

| Scope | EVAS r21b E2E | r14 Spectre AX E2E | AX/EVAS E2E | EVAS r21b subprocess | r14 AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| valid43 | 138.825s | 199.305s | 1.436x | 66.809s | 143.595s | 2.149x |

解释：

- r21b 是目前最能说明 EVAS 内核优化有效性的 EVAS-only 全量诊断：subprocess
  明显下降，尤其 valid43 subprocess 已低于 r14 单次 full rerun 的 68.994s。
- r21b 不能替代正式 EVAS-vs-AX same-run 表，因为 Spectre license checkout 仍未恢复；
  paper-facing 对照仍要等 Cadence checkout 正常后重新跑 AX/strict。
- E2E wall 当前已经不是纯内核问题：r21b all64 checker 为 97.849s，几乎等于
  EVAS subprocess 97.526s；valid43 fixture 也有明显波动。后续若目标是端到端速度，
  checker/harness 长尾仍必须继续收。

### r24：gain-estimator streaming checker exact-row EVAS-only 诊断

r24 在 r21b 同一 r14 exact-row manifest 上重跑 64 行 EVAS-only，`jobs=4`，不跑
Spectre。它只新增 `vbr1_l1_gain_estimator_tb/e2e` 的 validated streaming checker
入口，并保持同一 EVAS profile、同一 row set、同一 behavior checker 判定标准。
PASS 集合仍为 43/64，与 r14/r16/r21b 一致。

这个结果验证的是 **checker/harness 长尾收敛**，不是 EVAS kernel speedup。最大变化
来自 `vbr1_l1_gain_estimator/tb`：旧 r21b 里该行 E2E 为 35.041s，其中 checker
25.594s；r24 中该行走 `streaming_validated`，E2E 降为 10.353s，checker 降为
0.861s。该行仍是 behavior FAIL，因此它显著改善 all64 E2E，但几乎不改变
paper-facing valid43 速度口径。

| Scope | Run | EVAS E2E wall | EVAS subprocess | Checker | Fixture | CSV | PASS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | r21b capability prefilter | 236.720s | 97.526s | 97.849s | 33.225s | 6.394s | 43/64 |
| all64 | r24 gain-estimator streaming | 214.808s | 98.852s | 70.477s | 35.526s | 6.583s | 43/64 |
| valid43 | r21b capability prefilter | 138.825s | 66.809s | 42.321s | 24.177s | 4.292s | 43/43 |
| valid43 | r24 gain-estimator streaming | 136.627s | 68.007s | 40.429s | 22.076s | 4.445s | 43/43 |

r24 相比 r21b：

| Scope | E2E wall change | Subprocess change | Checker change | Fixture change | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| all64 | -21.912s / 1.102x faster | +1.325s | -27.372s / 1.388x faster | +2.301s | all64 收益几乎全部来自 checker 长尾消失 |
| valid43 | -2.198s / 1.016x faster | +1.198s | -1.891s / 1.047x faster | -2.101s | valid43 只小幅改善，核心 subprocess 没有变快 |

关键行差分：

| Entry/Form | r21b E2E | r24 E2E | r21b checker | r24 checker | Policy change | Status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `vbr1_l1_gain_estimator/tb` | 35.041s | 10.353s | 25.594s | 0.861s | `row_based` -> `streaming_validated` | FAIL -> FAIL |

用 r24 EVAS-only 与最近一次有效 r14 Spectre AX 对照，仅作为诊断口径：

| Scope | EVAS r24 E2E | r14 Spectre AX E2E | AX/EVAS E2E | EVAS r24 subprocess | r14 AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| valid43 | 136.627s | 199.305s | 1.459x | 68.007s | 143.595s | 2.111x |

注意：这仍不是 fresh same-run Spectre rerun。r23 license smoke 再次在
`spectre.out` 中显示 `Waiting for available license for Spectre.`，因此 AX/strict
新对照仍被 Cadence license checkout 阻塞。正式速度 claim 继续以最近一次有效 r14
same-run 表为准，r24 只作为 EVAS-only 诊断和 checker 长尾优化证据。

### r25-r30：CDAC、LFSR/PRBS7、edge-interval 与 BBPD streaming checker 诊断

r25/r26/r28/r30 继续在同一 r14 exact-row manifest 上做 EVAS-only full rerun：

- r25：新增 `cdac_cal` streaming checker。该 checker 只等价替换原
  `check_cdac_cal` 的 range 统计；release CDAC 的更强 checker
  `check_release_cdac_feedback_dac` 没有被简单 range checker 替代。
- r26：新增 `vbr1_l1_lfsr_prbs_generator_tb/e2e` alias 到已有 `lfsr_smoke`
  streaming checker，并新增 `prbs7`/`vbr1_l1_lfsr_prbs_generator_bugfix`
  streaming checker。`prbs7` 按 release 强 checker 语义实现：稳定电平阈值
  0.7/0.2、过滤 post-init rows、检查 serial/state 一致性和 PRBS recurrence。
- r28：新增 `cross_interval_163p333_smoke` 和
  `vbr1_l1_edge_interval_timer_tb/e2e` streaming checker。该 checker 等价替换
  原 `check_cross_interval_163p333` 的 post-event delay median 统计。
- r30：新增 `bbpd` 和 `vbr1_l1_bang_bang_phase_detector_bugfix` streaming checker。
  该 checker 等价替换原 `check_bbpd` 的 data-edge、up/down pulse、non-overlap
  与 0.2ns response-window 方向性判据。`vbr1_l1_bang_bang_phase_detector_tb`
  使用不同的 data-edge-alignment checker，没有复用 BBPD streaming checker。

r30 PASS 集合仍与 r24/r25/r26/r28 一致，均为 43/64。r30 是当前最新
EVAS-only checker/harness 诊断结果；它把 streaming checker 覆盖从 r26 的
21 rows、r28 的 23 rows 提升到 25 rows。checker total 从 r26 的 59.255s
降到 r30 的 47.117s；E2E single-run 从 r26 的 203.367s 降到 r30 的
194.658s。注意：E2E 仍包含 fixture/materialization 与 subprocess 波动，因此
强结论应写成 **checker/harness 长尾持续下降**，E2E 下降作为诊断观察。

| Scope | Run | EVAS E2E wall | EVAS subprocess | Checker | Fixture | CSV | PASS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | r24 gain-estimator streaming | 214.808s | 98.852s | 70.477s | 35.526s | 6.583s | 43/64 |
| all64 | r25 + CDAC streaming | 212.168s | 99.572s | 61.139s | 40.603s | 6.672s | 43/64 |
| all64 | r26 + LFSR/PRBS7 streaming | 203.367s | 98.867s | 59.255s | 35.733s | 6.882s | 43/64 |
| all64 | r28 + edge-interval streaming | 214.242s | 101.952s | 53.602s | 50.696s | 7.887s | 43/64 |
| all64 | r30 + BBPD streaming | 194.658s | 96.616s | 47.117s | 41.522s | 5.691s | 43/64 |
| valid43 | r24 gain-estimator streaming | 136.627s | 68.007s | 40.429s | 22.076s | 4.445s | 43/43 |
| valid43 | r25 + CDAC streaming | 139.656s | 67.855s | 38.475s | 26.382s | 4.394s | 43/43 |
| valid43 | r26 + LFSR/PRBS7 streaming | 130.874s | 67.651s | 33.117s | 24.570s | 4.720s | 43/43 |
| valid43 | r28 + edge-interval streaming | 135.348s | 70.790s | 24.388s | 34.850s | 5.700s | 43/43 |
| valid43 | r30 + BBPD streaming | 119.268s | 65.995s | 19.933s | 28.203s | 3.750s | 43/43 |

r26 相比 r24：

| Scope | E2E wall change | Subprocess change | Checker change | Fixture change | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| all64 | -11.441s / 1.056x faster | +0.015s | -11.222s / 1.189x faster | +0.207s | 收益来自 checker，EVAS subprocess 基本不变 |
| valid43 | -5.753s / 1.044x faster | -0.356s | -7.312s / 1.221x faster | +2.494s | valid43 checker 明确下降，E2E 仍受 fixture 波动影响 |

r28 相比 r26：

| Scope | E2E wall change | Subprocess change | Checker change | Fixture change | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| all64 | +10.875s | +3.085s | -5.653s / 1.105x faster | +14.964s | edge-interval checker 有效，但 E2E 被 fixture/subprocess 波动反向覆盖 |
| valid43 | +4.473s | +3.139s | -8.730s / 1.358x faster | +10.281s | valid checker 明显下降，单次 E2E 不应作为加速 claim |

r30 相比 r28：

| Scope | E2E wall change | Subprocess change | Checker change | Fixture change | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| all64 | -19.584s / 1.101x faster | -5.336s | -6.485s / 1.138x faster | -9.174s | BBPD streaming 有效；本轮 E2E 也下降，但仍需 repeated run 分离波动 |
| valid43 | -16.080s / 1.135x faster | -4.795s | -4.455s / 1.223x faster | -6.647s | valid43 E2E 与 checker 均下降，是目前最好的 EVAS-only 诊断点 |

关键真实 CSV parity/耗时证据：

| Checker | Row-based | Streaming | Score parity |
| --- | ---: | ---: | --- |
| `cdac_cal` | 0.820s | 0.006s | 1.0 -> 1.0 |
| `vbr1_l1_lfsr_prbs_generator_tb` | 0.779s | 0.005s | 1.0 -> 1.0 |
| `prbs7` | 0.884s | 0.021s | 1.0 -> 1.0 |
| `vbr1_l1_lfsr_prbs_generator_bugfix` | 0.884s | 0.021s | 1.0 -> 1.0 |
| `cross_interval_163p333_smoke` / edge interval | parity script only | parity script only | 2/2 match |
| `bbpd` / `vbr1_l1_bang_bang_phase_detector_bugfix` | parity script only | parity script only | 2/2 match |

此外，`check_streaming_checker_parity.py` 在 r26 result-root 上扫描这四个真实 CSV，
结果为 4/4 comparable match、0 mismatch、0 original timeout。
`check_streaming_checker_parity.py` 在 r28 result-root 上扫描 edge-interval 两个真实
CSV，结果为 2/2 comparable match、0 mismatch、0 original timeout。
`check_streaming_checker_parity.py` 在 r28 result-root 上扫描 BBPD 两个真实 CSV，
结果为 2/2 comparable match、0 mismatch、0 original timeout。

关键行差分：

| Entry/Form | r25 E2E | r26 E2E | r25 checker | r26 checker | Policy change | Status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `vbr1_l1_lfsr_prbs_generator/tb` | 3.662s | 1.023s | 2.682s | 0.029s | `row_based` -> `streaming_validated` | PASS -> PASS |
| `vbr1_l1_lfsr_prbs_generator/bugfix` | 4.056s | 1.071s | 2.456s | 0.025s | `row_based` -> `streaming_validated` | PASS -> PASS |
| `vbr1_l1_lfsr_prbs_generator/dut` | 3.035s | 1.275s | 1.781s | 0.024s | `row_based` -> `streaming_validated` | PASS -> PASS |
| `vbr1_l1_edge_interval_timer/e2e` | 2.626s | 1.187s | 1.591s | 0.114s | `row_based` -> `streaming_validated` | PASS -> PASS |
| `vbr1_l1_edge_interval_timer/tb` | 2.850s | 0.960s | 1.916s | 0.015s | `row_based` -> `streaming_validated` | PASS -> PASS |
| `vbr1_l1_bang_bang_phase_detector/dut` | 4.155s | 4.939s | 2.170s | 0.023s | `row_based` -> `streaming_validated` | PASS -> PASS |
| `vbr1_l1_bang_bang_phase_detector/bugfix` | 2.880s | 1.859s | 1.385s | 0.053s | `row_based` -> `streaming_validated` | PASS -> PASS |

用 r26 EVAS-only 与最近一次有效 r14 Spectre AX 对照，仅作为诊断口径：

| Scope | EVAS r26 E2E | r14 Spectre AX E2E | AX/EVAS E2E | EVAS r26 subprocess | r14 AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| valid43 | 130.874s | 199.305s | 1.523x | 67.651s | 143.595s | 2.122x |

注意：这仍不是 fresh same-run Spectre rerun；r30 只证明 EVAS-only checker/harness
长尾继续下降。`thu-sui` 上 r29 Spectre smoke 仍出现
`Waiting for available license for Spectre.`；但通过 `thu-sui` 跳转到 `thu-wei`
直接运行 Spectre gold testbench 已证明 `thu-wei` 可 checkout license（license
check successful，direct Spectre elapsed 3.39s）。当前阻塞点变成运行方式：
`thu-wei` 裸环境只有 Python 2.7，缺少 Python3 runner 环境。正式 EVAS-vs-Spectre AX
速度表应改为统一由 `thu-sui`/本地 Python orchestrator 调用 `thu-wei` Spectre subprocess，
或先在 `thu-wei` 准备 Python3 后再跑完整 runner。

### 统一运行方法：Spectre on `thu-wei`，EVAS on latest local/`thu-sui`

后续速度实验固定使用以下运行边界：

1. Spectre AX/strict 通过 `thu-sui` 跳板到 `thu-wei` 执行。`thu-wei` 运行前必须
   `source /home/cshrc/.cshrc.cadence.IC618SP201`，并在 smoke 中确认 Spectre log
   出现 license checkout success，而不是 `Waiting for available license for Spectre.`。
2. 在 `thu-wei` 没有 Python3 runner 环境前，不直接在 `thu-wei` 运行
   `run_vabench_release_same_server_speed.py`。可选方案是：
   - 由 `thu-sui` 或本地 Python orchestrator 通过 SSH 启动 `thu-wei` Spectre；
   - 或先给 `thu-wei` 准备 Python3，再把完整 runner 和 release workspace 同步过去。
3. EVAS 可以在 `thu-sui` 或本地跑，但每次对比前必须记录并确认最新版：
   - 本地/远端 `git rev-parse HEAD`；
   - `git status --short` 或等价 dirty diff 摘要；
   - 已同步的 EVAS 源码、benchmark runner 和 checker 文件；
   - 使用的 exact-row manifest 与 output root。
4. 如果 Spectre 与 EVAS 不在同一台 host 上，报告必须显式写出 host 与 CPU 环境。
   这种结果可作为工程运行口径，但不应包装成严格同机 microbenchmark。
5. 速度表继续拆成两层：
   - `simulator subprocess wall`：仿真器进程边界；
   - `E2E wall`：fixture、文件复制、CSV/checker、进程调度与清理都算入。
   通过 SSH 调 `thu-wei` Spectre 时，SSH/orchestration 开销要么单独记录，要么明确
   纳入 E2E，而不能混到 EVAS simulator-only 结论里。

### r22：node-map cache 负结果

r22 尝试为 `node_map` local-port 到 external-node 的解析增加缓存，目标是降低 L2
hierarchical 子模块里 `V(port)` 的字符串解析/`@parent:` 判断开销。该想法在 targeted
regression 上语义正确，但 profile 结果为负，因此已从代码中撤回。

| Row | Run | E2E wall | EVAS subprocess | `model_evaluate_s` | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| gain estimator | r20 capability prefilter | 11.245s | 10.193s | 3.862s | 有效 baseline |
| gain estimator | r22 node-map cache | 11.251s | 10.256s | 4.184s | 无收益，evaluate 变慢 |
| gain extraction | r20 capability prefilter | 10.679s | 9.619s | 3.761s | 有效 baseline |
| gain extraction | r22 node-map cache | 10.877s | 9.985s | 4.074s | 无收益，evaluate 变慢 |

结论：不要沿 node-map 解析缓存继续优化。它增加了每次 `_get_voltage()` 的 cache
检查和 map signature 检查，反而使 `model_evaluate_s` 增加约 0.3s/measurement-heavy
row。后续应转向 generated code 层面的局部变量/数组后端，而不是在 `_get_voltage()`
内部继续叠缓存逻辑。

### 当前暴露出的速度限制

1. **measurement-heavy kernel hotspot**：`vbr1_l1_gain_estimator` 与
   `vbr1_l2_gain_extraction_convergence_measurement_flow` 仍是 EVAS subprocess
   最大项，但 r20/r21b 已证明每步扫描预筛能降低这类长尾。剩余主项是
   generated `model_evaluate_s`，不是 CSV 或简单 breakpoint scan。
2. **checker/harness 长尾**：r16 all64 checker 为 94.289s，valid43 checker
   为 40.971s；r21b all64 checker 升至 97.849s，valid43 为 42.321s。
   r24 收掉 `vbr1_l1_gain_estimator/tb` 后 all64 checker 降为 70.477s；
   r26 继续接入 CDAC/LFSR/PRBS7 streaming 后，all64 checker 降为 59.255s，
   valid43 checker 降为 33.117s；r28 接入 edge-interval streaming 后，
   all64 checker 继续降为 53.602s，valid43 checker 降为 24.388s；r30 接入
   BBPD streaming 后，all64 checker 降为 47.117s，valid43 checker 降为
   19.933s。CSV 和内核扫描下降后，checker 仍是 E2E 重要限制之一，剩余
   row-based 长尾集中在 strongarm、clock divider、propagation-delay、
   XOR phase detector、SAR/window-comparator 类 checker。
3. **CSV 已从主次瓶颈降级**：r16 all64 CSV 为 6.334s，比 r15b 少约 5.229s；
   r21b all64 CSV 为 6.394s，基本持平。继续优化 CSV 的收益会小于优化 checker
   或 generated `model_evaluate`。
4. **Spectre fresh rerun 的阻塞从 license 转为运行边界**：`thu-sui` 本机 r29
   Spectre-only smoke 仍在 `spectre.out` 中显示
   `Waiting for available license for Spectre.`；但通过 `thu-sui` 跳板到
   `thu-wei` 直接运行 Spectre gold testbench 已成功 checkout license。当前需要
   统一 runner 方式：Spectre 放到 `thu-wei`，Python orchestrator 留在 `thu-sui`
   或本地，或者先给 `thu-wei` 准备 Python3。

## 前一版结论：r8 统一复测

2026-06-02 r8 是 r14 之前的同 row-set 对照口径。运行方式是用户要求的 `thu-sui`
上 `python3` runner；Spectre 通过 `thu-sui` wrapper 调用 `thu-wei`
Cadence/Spectre 21.1.0.509.isr12。该报告使用 r5 的 exact 64-row manifest，
因此 r8、r7、r6 与 r5 的 row set 完全一致：all rows 为 64/64，
paper-facing valid rows 为 43/43。r8 只改变 checker/harness policy：
validated streaming checker 从 8 个增加到 16 个；EVAS 仿真内核、Spectre AX/strict
设置和 row manifest 没有改变。

注：r8 曾是单次 exact-row 统一复测的最终速度表；runner 的
`claim_allowed=false` 仍要求正式 paper-facing speed claim 在提交前做 repeated
cold/warm runs 确认。

结论：

1. **all64 E2E**：EVAS fast 快于 Spectre AX。EVAS fast 为 211.336s，
   Spectre AX 为 338.378s，`T(AX)/T(EVAS fast)=1.601x`。
2. **paper-facing valid43 E2E**：EVAS fast 快于 Spectre AX。EVAS fast
   为 113.230s，Spectre AX 为 204.654s，`T(AX)/T(EVAS fast)=1.807x`。
3. **simulator subprocess**：EVAS fast 仍明显快于 Spectre AX。all64 中
   EVAS fast subprocess 为 99.740s，Spectre AX subprocess 为 209.508s，
   `T(AX subprocess)/T(EVAS subprocess)=2.101x`；valid43 中为 68.636s
   vs 141.580s，速度比 2.063x。
4. **精度/等价**：checker/harness 变快不改变 EVAS 数值语义。当前仍不能声明
   EVAS fast 比 AX 更精准；保守口径仍是“EVAS fast 在多数 release rows 上与
   strict Spectre reference 一致，但仍有 needs-review 行，AX 对 strict reference
   的 waveform gate 更完整”。
5. **r8 checker alias 效果**：r8 相比 r7 使 EVAS checker wall 显著下降，
   all64 为 -202.460s，valid43 为 -201.072s；EVAS subprocess 基本不变
   （all64 -0.557s，valid43 -0.826s）。这说明 r8 的 E2E 提升来自 checker/harness
   长尾收敛，不是 EVAS kernel 新加速。

| Scope | EVAS fast E2E wall | Spectre AX E2E wall | AX/EVAS E2E | EVAS subprocess | AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | 211.336s | 338.378s | 1.601x | 99.740s | 209.508s | 2.101x |
| paper-facing valid43 | 113.230s | 204.654s | 1.807x | 68.636s | 141.580s | 2.063x |

Timing split 显示 r8 后 E2E 长尾已明显收敛，但 all64 仍有失败行上的
row-based checker 开销：

| Scope | Mode | E2E wall | Subprocess | Checker | Fixture | PSF parse |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| all64 | EVAS fast | 211.336s | 99.740s | 72.798s | 32.606s | 0.000s |
| all64 | Spectre AX | 338.378s | 209.508s | 60.971s | 46.478s | 20.265s |
| valid43 | EVAS fast | 113.230s | 68.636s | 18.973s | 22.327s | 0.000s |
| valid43 | Spectre AX | 204.654s | 141.580s | 10.718s | 37.750s | 13.879s |

Checker policy 贡献：

| Mode | Checker policy | Rows | E2E wall | Subprocess | Checker |
| --- | --- | ---: | ---: | ---: | ---: |
| EVAS fast | row_based | 38 | 124.225s | 33.370s | 68.344s |
| EVAS fast | streaming_validated | 16 | 68.763s | 53.251s | 4.454s |
| EVAS fast | no_checker | 10 | 18.347s | 13.118s | 0.000s |
| Spectre AX | row_based | 38 | 197.551s | 114.813s | 57.028s |
| Spectre AX | streaming_validated | 16 | 107.698s | 65.936s | 3.922s |
| Spectre AX | no_checker | 10 | 33.129s | 28.759s | 0.022s |

r8 当时可用口径：

> 在 r8 统一复测下，EVAS fast 在 simulator subprocess 与统一 E2E wall
> 两个口径下都快于 Spectre AX：valid43 E2E 为 113.230s vs 204.654s，
> 速度比 1.807x；valid43 subprocess 为 68.636s vs 141.580s，速度比 2.063x。
> 但精度上仍不能声明 EVAS fast 优于 AX；checker/harness 优化只降低评测开销，
> 不改变 EVAS 与 strict Spectre reference 的数值差异。正式论文 claim 仍需要
> repeated cold/warm runs 支撑。

## 前一版结论：r7 统一复测

2026-06-02 r7 是 r8 之前的同 row-set 对照。它已经包含 source breakpoint
cache 和 err-ratio candidate cache，因此 EVAS subprocess 比 r6 更低；但当时
release task alias 还没有完全接入 streaming checker，导致 E2E 被 row-based checker
长尾主导。

| Scope | EVAS fast E2E wall | Spectre AX E2E wall | AX/EVAS E2E | EVAS subprocess | AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | 446.385s | 421.932s | 0.945x | 100.297s | 209.933s | 2.093x |
| paper-facing valid43 | 341.302s | 268.692s | 0.787x | 69.462s | 143.059s | 2.060x |

r8 相比 r7 的直接变化：

| Scope | EVAS E2E delta | EVAS subprocess delta | EVAS checker delta | EVAS fixture delta | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| all64 | -235.049s | -0.557s | -202.460s | -27.477s | E2E 主要由 checker/harness alias 收敛带来 |
| paper-facing valid43 | -228.072s | -0.826s | -201.072s | -21.034s | valid rows 从 E2E 慢于 AX 变为快于 AX |

## 前一版结论：r6 统一复测

2026-06-02 r6 是 r7 前一版同 row-set 对照。

| Scope | EVAS fast E2E wall | Spectre AX E2E wall | AX/EVAS E2E | EVAS subprocess | AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | 436.194s | 418.168s | 0.959x | 105.580s | 208.106s | 1.971x |
| paper-facing valid43 | 329.351s | 268.231s | 0.814x | 73.138s | 141.119s | 1.929x |

r7 相比 r6 的直接变化：

| Scope | EVAS E2E delta | EVAS subprocess delta | EVAS checker delta | EVAS fixture delta | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| all64 | +10.192s | -5.283s | +12.635s | +5.653s | kernel/subprocess 变快，但 E2E 被 checker/fixture 反向抵消 |
| paper-facing valid43 | +11.951s | -3.676s | +13.019s | +3.120s | valid rows 同样不能 claim E2E 加速 |

## 更早对照：r5 统一复测

2026-06-02 r5 是低风险内核/IO 优化前的同 row-set 对照。它统一了
EVAS/Spectre 的 E2E wall 边界，并同时保留 simulator subprocess wall。

| Scope | EVAS fast E2E wall | Spectre AX E2E wall | AX/EVAS E2E | EVAS subprocess | AX subprocess | AX/EVAS subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | 429.681s | 477.679s | 1.112x | 102.964s | 236.835s | 2.300x |
| paper-facing valid43 | 316.679s | 317.045s | 1.001x | 70.514s | 162.795s | 2.309x |

r5 的 all64 E2E 中 EVAS 略快于 AX，但 valid43 基本持平。r6 使用完全相同 row
set 后，AX wall 明显下降而 EVAS wall 小幅上升，说明单次 all-row E2E wall 仍有
fixture/checker/PSF 处理和远端运行波动；更稳妥的论文口径是同时报告 E2E wall 和
simulator subprocess wall，不把单次 E2E 微弱优势写成核心 claim。

## 历史结论：r4 rerun 证明

2026-06-01 full rerun r4 已完成，使用与 r3 相同的 64-row release gold e2e
slice、相同 Spectre AX/strict 设置、相同统一 evaluator E2E wall 口径。r4 只改变
checker policy：为 PFD release task id 接入已有 streaming checker，并新增 CPPLL
streaming checker；EVAS/Spectre 仿真设置没有为了速度单独放松。

注：r4 是重要历史阶段，用来证明首批 checker 长尾修复有效；当前最终速度判断
以 2026-06-02 r14 为准。

结论：

1. **统一 E2E wall**：EVAS fast 在 r4 当时快于 Spectre AX。EVAS fast 为
   159.810s，Spectre AX 为 208.839s，`T(AX)/T(EVAS fast)=1.307x`。
2. **仿真器子进程 wall**：EVAS fast 仍快于 Spectre AX。EVAS fast subprocess
   为 49.831s，Spectre AX subprocess 为 116.381s，`T(AX)/T(EVAS fast)=2.336x`。
3. **精度/正确性**：r4 没有改善精度缺口。EVAS fast 仍是 63/64 strict
   Spectre waveform passed、1/64 needs review；Spectre AX 是 64/64 passed。
   因此可以 claim 速度已优于 AX，但不能 claim 精度优于 AX。

| Mode | Runs | Sim OK | Behavior OK | E2E wall | Simulator subprocess | Checker |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS fast | 64 | 64 | 56 | 159.810s | 49.831s | 48.495s |
| EVAS strict | 64 | 64 | 56 | 622.191s | 502.994s | 50.821s |
| Spectre AX equalized | 64 | 64 | 57 | 208.839s | 116.381s | 22.770s |
| Spectre strict | 64 | 64 | 57 | 427.706s | 313.261s | 45.625s |

速度比：

| Comparison | Formula | Value | Interpretation |
| --- | --- | ---: | --- |
| EVAS fast E2E vs Spectre AX E2E | `T(AX) / T(EVAS fast)` | 1.307x | EVAS fast full E2E 快于 AX |
| EVAS fast E2E time / AX E2E time | `T(EVAS fast) / T(AX)` | 0.765x | EVAS fast E2E 耗时约为 AX 的 76.5% |
| EVAS fast subprocess vs Spectre AX subprocess | `T(AX subprocess) / T(EVAS subprocess)` | 2.336x | EVAS fast evaluator/subprocess 快于 AX |
| EVAS fast E2E vs Spectre strict E2E | `T(strict) / T(EVAS fast)` | 2.676x | EVAS fast 明显快于 strict Spectre |
| EVAS fast E2E vs EVAS strict E2E | `T(EVAS strict) / T(EVAS fast)` | 3.893x | fast profile 相对 strict EVAS 的收益明确 |

r3 -> r4 对比：

| Mode | r3 E2E wall | r4 E2E wall | Delta | r3/r4 |
| --- | ---: | ---: | ---: | ---: |
| EVAS fast | 301.694s | 159.810s | -141.884s | 1.888x |
| EVAS strict | 719.653s | 622.191s | -97.462s | 1.157x |
| Spectre AX equalized | 263.019s | 208.839s | -54.180s | 1.259x |
| Spectre strict | 580.335s | 427.706s | -152.629s | 1.357x |

关键证明项：

| Entry | r3 EVAS fast E2E | r4 EVAS fast E2E | r3 checker | r4 checker | PASS parity |
| --- | ---: | ---: | ---: | ---: | --- |
| `vbr1_l1_pfd_up_dn_logic` | 57.240s | 3.100s | 54.228s | 0.194s | PASS -> PASS |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | 81.292s | 4.120s | 78.056s | 0.387s | PASS -> PASS |

单独在 r3 CSV 上做旧 checker vs streaming checker parity：

| Task | Old row checker | Streaming checker | Old checker time | Streaming time |
| --- | ---: | ---: | ---: | ---: |
| `vbm1_pfd_reset_race_e2e` | PASS | PASS | 6.324s | 0.183s |
| `cppll_freq_step_reacquire_smoke` | PASS | PASS | 9.432s | 0.177s |

r4 当时可用口径（已被 r5/r6 取代，不再作为当前推荐 claim）：

> 在统一 64-row full E2E wall 口径下，经过 checker 长尾修正后，EVAS fast
> 快于 Spectre AX equalized：159.810s vs 208.839s，速度比为 1.307x。
> 但 EVAS fast 仍有 1 个 strict Spectre waveform needs-review 行，因此不能声明
> 精度高于 Spectre AX。

## 2026-06-02 增量优化：第二批 checker 长尾

r4 之后继续检查 “EVAS 更慢” 的行，发现还有一批 E2E deficit 不是 EVAS
subprocess 慢，而是 behavior checker 用 row-list / pandas-like 全量扫描方式产生
额外 wall time。因此本轮继续扩展 streaming checker，覆盖以下 7 个 task id：

- `lfsr_smoke`
- `cross_hysteresis_window_smoke`
- `phase_accumulator_timer_wrap_smoke`
- `vbr1_l1_precision_rectifier_envelope_detector_e2e`
- `vbr1_l2_programmable_stimulus_sequencer_e2e`
- `adpll_ratio_hop_smoke`
- `sample_hold_droop_smoke`

这次改动不改变 EVAS 仿真内核、步长策略或容差；它只把 checker 从“把 CSV
读成完整行对象再做统计”改成“边读边累计必要统计量”。因此这属于 E2E harness
优化，不能被写成 EVAS kernel speedup。

真实 r4 CSV 上的 checker parity：

| Scope | Cases | Match | Mismatch | Original checker total | Streaming checker total |
| --- | ---: | ---: | ---: | ---: | ---: |
| 7 tasks x 2 EVAS modes | 14 | 14 | 0 | 23.162s | 3.931s |

针对 fast mode 的 EVAS-only smoke 显示，run-case 内的 checker wall 从 r4
报告中的 29.146s 降到 0.294s。这个 smoke 只验证新 checker 已被
`simulate_evas.run_case()` 使用；因为 plain ssh 环境没有加载 Cadence `spectre`
命令，它不是最终 EVAS-vs-AX 速度表。

| Entry | r4 EVAS fast checker | New EVAS-only smoke checker | Status |
| --- | ---: | ---: | --- |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | 11.554s | 0.148s | PASS |
| `vbr1_l2_programmable_stimulus_sequencer` | 6.104s | 0.065s | PASS |
| `vbr1_l1_precision_rectifier_envelope_detector` | 5.169s | 0.040s | PASS |
| `vbr1_l1_window_comparator_detector` | 2.375s | 0.008s | PASS |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | 1.894s | 0.022s | PASS |
| `vbr1_l2_converter_front_end` | 1.253s | 0.005s | PASS |
| `vbr1_l1_lfsr_prbs_generator` | 0.796s | 0.007s | PASS |

当前判断：

> 已经确认这 7 行的“更慢”主要是 checker/harness 长尾，不是 EVAS kernel
> subprocess 慢。Cadence 环境下的 r8 exact-row full rerun 证明 streaming
> checker 改动没有改变 43-row valid set，并且把 paper-facing valid43 E2E
> 从 r7 的 EVAS 慢于 AX 改为 EVAS 快于 AX。r14 在同 row set 上加入低风险
> EVAS core micro-optimization 后，PASS 集合仍与 r8 一致；当前最终速度表应以
> r14 为准。剩余 E2E 长尾主要集中在 all64 的失败行、仍未 streaming 化的
> row-based checker，以及 measurement-heavy EVAS subprocess 热点。

为避免后续混淆，runner 现在会在每条 EVAS/Spectre result 中记录
`checker_policy`，并在 Markdown summary 中汇总 checker implementation：

- `streaming_validated`：该 checker 使用了真实 CSV parity 验证过的 streaming
  实现。
- `row_based`：该 checker 使用 legacy row-list 实现。
- `row_based_fallback_from_streaming`：该 checker 已有 streaming 实现，但当前 CSV
  触发了保守 fallback。
- `row_based_streaming_disabled`：环境变量显式禁用了 validated streaming checker。

这个字段的目的不是改变判定，而是让速度报告可以明确声明：同一个 `checker_id`
下 EVAS 和 Spectre 使用同一套 checker policy。

## r3 基线诊断：优化前

2026-06-01 full rerun r3 已完成，`wall_time_s` 改为统一 evaluator E2E
wall 口径；同时记录 `simulator_subprocess_wall_s` 和 `timing_split`。

主结论分两层：

1. **统一 E2E wall**：EVAS fast 仍不能声明快于 Spectre AX。EVAS fast
   总 E2E wall 为 301.694s，Spectre AX 为 263.019s，EVAS fast 是 AX 的
   1.147 倍耗时。
2. **仿真器子进程 wall**：EVAS fast 的核心 evaluator/subprocess 已经快于
   Spectre AX。EVAS fast subprocess 为 49.737s，Spectre AX subprocess 为
   107.467s，AX/EVAS = 2.161x。

因此现在更准确的说法是：

> EVAS fast 的内核/子进程已表现出相对 Spectre AX 的速度优势，但当前
> paper-facing E2E wall 仍被 checker、fixture/materialization 和少数长尾任务拖慢；
> 在修复这些外层与长尾问题前，不能声明 full E2E 快于 Spectre AX。

| Mode | Runs | Sim OK | Behavior OK | Total wall | Simulator/internal reported | Wall - internal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS fast | 64 | 64 | 56 | 301.694s | 49.737s | 251.957s |
| EVAS strict | 64 | 64 | 56 | 719.653s | 503.385s | 216.268s |
| Spectre AX equalized | 64 | 64 | 57 | 263.019s | 107.467s | 155.552s |
| Spectre strict | 64 | 64 | 57 | 580.335s | 301.867s | 278.468s |

阶段拆分：

| Mode | E2E wall | Simulator subprocess | Checker | Fixture/PSF/other | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| EVAS fast | 301.694s | 49.737s | 180.735s | 71.222s | checker 是最大项，subprocess 只占 16.5% |
| EVAS strict | 719.653s | 503.385s | 138.412s | 77.856s | strict 主要慢在 EVAS subprocess |
| Spectre AX equalized | 263.019s | 107.467s | 82.261s | 73.291s | AX subprocess 比 EVAS fast 慢，但 checker 较小 |
| Spectre strict | 580.335s | 301.867s | 192.472s | 86.996s | strict Spectre subprocess 和 checker 都更重 |

速度比：

| Comparison | Formula | Value | Interpretation |
| --- | --- | ---: | --- |
| EVAS fast E2E vs Spectre strict E2E | `T(strict) / T(EVAS fast)` | 1.924x | EVAS fast E2E 快于 strict Spectre |
| EVAS fast E2E vs Spectre AX E2E | `T(AX) / T(EVAS fast)` | 0.872x | EVAS fast E2E 仍慢于 AX |
| EVAS fast E2E time / AX E2E time | `T(EVAS fast) / T(AX)` | 1.147x | EVAS fast E2E 总耗时约为 AX 的 1.147 倍 |
| EVAS fast subprocess vs Spectre AX subprocess | `T(AX subprocess) / T(EVAS subprocess)` | 2.161x | EVAS fast evaluator/subprocess 快于 AX |

逐行统计：

| Metric | EVAS fast faster than AX | EVAS fast slower than AX | Interpretation |
| --- | ---: | ---: | --- |
| E2E wall | 51/64 | 13/64 | 大多数行 EVAS fast 更快，但少数长尾抵消优势 |
| Simulator subprocess wall | 61/64 | 3/64 | 核心 evaluator 层面 EVAS fast 已经更快 |

关键长尾：

| Entry | EVAS E2E | AX E2E | EVAS-AX deficit | EVAS subprocess | AX subprocess | Main issue |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `vbr1_l1_pfd_up_dn_logic` | 57.240s | 2.307s | 54.933s | 2.260s | 1.752s | checker 54.228s；release task id 未走已有 streaming checker alias |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | 81.292s | 51.442s | 29.850s | 2.540s | 2.969s | checker 78.056s；subprocess 本身 EVAS 更快 |
| `vbr1_l2_programmable_stimulus_sequencer` | 10.074s | 3.200s | 6.875s | 1.109s | 1.656s | checker/harness 长尾 |
| `vbr1_l1_gain_estimator` | 21.969s | 15.603s | 6.366s | 10.344s | 5.011s | subprocess 和 checker 都偏慢 |

诊断性去除长尾后：

| Slice | Rows | AX E2E | EVAS fast E2E | `T(AX)/T(EVAS)` |
| --- | ---: | ---: | ---: | ---: |
| Full | 64 | 263.019s | 301.694s | 0.872x |
| Excluding PFD only | 63 | 260.712s | 244.454s | 1.067x |
| Excluding PFD + CPPLL | 62 | 209.270s | 163.162s | 1.283x |

这不是用来 cherry-pick claim，而是说明当前 full E2E 速度问题高度集中：
PFD 和 CPPLL 两行的 EVAS-AX E2E deficit 合计 84.783s，已经超过全量总
deficit 38.675s。

r3 基线安全口径是：

> EVAS fast 在 simulator subprocess 口径下已经快于 Spectre AX；在统一
> full E2E wall 口径下仍慢于 Spectre AX，主要瓶颈是 checker/harness 长尾和少数
> event-heavy 或 measurement-heavy 行。

## 历史口径回顾

`precision_ranking_full_e2e_equalized_20260526.json` 的历史 `wall_time_s`
字段不是完全对称口径：EVAS 侧主要包住 `simulate_evas.run_case()`，
Spectre 侧主要包住 Spectre subprocess。因此旧数据只作为问题发现线索，
不再作为最终速度表。

| Mode | Runs | Sim OK | Behavior OK | Old total wall | Old internal/reported | Old wall - internal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS fast | 64 | 64 | 57 | 190.458s | 28.200s | 162.258s |
| EVAS strict | 64 | 64 | 57 | 525.160s | 383.000s | 142.160s |
| Spectre AX equalized | 64 | 64 | 57 | 66.184s | 52.209s | 13.975s |
| Spectre strict | 64 | 64 | 57 | 242.031s | 228.030s | 14.001s |

## 精度状态

当前精度结论同样需要收紧：不能声称 EVAS 比 AX 更精准。r14 与 r8 的
behavior PASS 集合一致；strict-reference waveform gate 仍沿用同 row-set
precision evidence 的保守结论：Spectre AX 的 waveform gate 更完整，EVAS fast
还有 4 个 ADC/DAC 相关 needs-review 行。

| Candidate | vs strict Spectre | Behavior OK | Worst max abs V | Worst relative RMS |
| --- | ---: | ---: | ---: | ---: |
| EVAS fast | 60 passed / 4 needs review | 43/64 | 1.000 | 0.609422 |
| Spectre AX equalized | 64/64 | 45/64 | 0.103929 | 0.002214 |

EVAS fast 的 4 个 strict-reference needs-review 行是：

| Entry | Form | EVAS behavior | Strict behavior | Waveform comparison |
| --- | --- | --- | --- | --- |
| `vbr1_l2_adc_dac_reconstruction_chain` | e2e | FAIL | PASS | needs review |
| `vbr1_l2_adc_dac_reconstruction_chain` | tb | FAIL | FAIL | needs review |
| `vbr1_l2_weighted_sar_adc_dac_loop` | e2e | FAIL | PASS | needs review |
| `vbr1_l2_weighted_sar_adc_dac_loop` | tb | FAIL | FAIL | needs review |

精度结论：

> r14/r8 当前同 row-set 证据下，EVAS fast 的 behavior PASS 集合保持稳定，
> 但 Spectre AX 在 strict Spectre waveform gate 上仍是 64/64 passed；EVAS
> fast 是 60/64 passed、4/64 needs review，并且 behavior PASS 少 2 行。
> 因此当前不能说 EVAS 精度高于 AX，只能说多数行与 strict Spectre 保持一致，
> 且 ADC/DAC 相关 4 行需要单独 triage。

## 速度差距来自哪里

当前 r14 中，EVAS fast 已经在 all64 和 valid43 的 E2E wall 上快于
Spectre AX；剩余问题不再是“EVAS 总体慢于 AX”，而是“哪些开销限制了更高
速度比”。直接分解如下：

| Scope | EVAS E2E | AX E2E | EVAS subprocess | AX subprocess | EVAS checker | AX checker | EVAS CSV | AX PSF parse |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | 214.597s | 330.908s | 100.368s | 208.065s | 73.199s | 59.802s | 11.532s | 21.900s |
| valid43 | 117.394s | 199.305s | 68.994s | 143.595s | 20.131s | 11.702s | 7.737s | 14.944s |

这张表说明两件事：

1. EVAS 的 simulator subprocess 已经比 AX 快约 2.1x，这是当前最强的核心速度证据。
2. EVAS 的 E2E 速度比只有 1.54x 到 1.70x，主要因为 checker、fixture、CSV 输出
   等外层成本吃掉了 subprocess 侧的一部分优势。

r7 是一个重要历史反例：当时 EVAS subprocess 已快于 AX，但 E2E 仍慢于 AX，
用来说明 checker/harness 长尾曾经如何掩盖内核速度优势。r7 中 EVAS fast 与
AX equalized 的总 wall time 差距：

```text
all64:  T(EVAS fast E2E) - T(AX E2E) = 446.385s - 421.932s = 24.453s
valid43: T(EVAS fast E2E) - T(AX E2E) = 341.302s - 268.692s = 72.610s
```

这不是 EVAS subprocess 全局慢造成的：all64 中 EVAS subprocess 为 100.297s，
AX subprocess 为 209.933s，EVAS 子进程仍约快 2.09x。当前差距主要来自
row-based checker/harness 长尾，以及 measurement-heavy 行的 EVAS kernel
subprocess 热点。

r7 EVAS fast 的 E2E 长尾：

| Entry | Form | EVAS E2E | EVAS subprocess | EVAS checker | CSV write | Dominant measured cost |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `vbr1_l1_pfd_small_phase_error_response` | dut | 56.871s | 3.136s | 51.871s | 0.505s | row-based checker |
| `vbr1_l1_pfd_small_phase_error_response` | e2e | 53.052s | 2.976s | 49.556s | 0.505s | row-based checker |
| `vbr1_l1_pfd_up_dn_logic` | bugfix | 36.669s | 2.325s | 15.477s | 0.268s | fixture + row-based checker |
| `vbr1_l1_gain_estimator` | tb | 35.623s | 9.954s | 23.584s | 0.907s | subprocess + row-based checker |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | tb | 34.623s | 9.855s | 23.826s | 0.917s | subprocess + row-based checker |
| `vbr1_l2_pll_timing_slice` | e2e | 30.466s | 2.137s | 23.004s | 0.406s | row-based checker |
| `vbr1_l1_pfd_up_dn_logic` | tb | 25.294s | 2.323s | 18.802s | 0.273s | row-based checker |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | tb | 21.510s | 2.557s | 18.506s | 0.465s | row-based checker |

r7 EVAS fast 的 subprocess 热点：

| Entry | Form | EVAS subprocess | Accepted steps | CSV write | Checker policy | Interpretation |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `vbr1_l1_gain_estimator` | e2e | 9.995s | 110602 | 0.979s | streaming_validated | measurement-heavy kernel hotspot |
| `vbr1_l1_gain_estimator` | tb | 9.954s | 110602 | 0.907s | row_based | kernel hotspot plus checker |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | e2e | 9.935s | 110602 | 0.927s | streaming_validated | measurement-heavy kernel hotspot |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | tb | 9.855s | 110602 | 0.917s | row_based | kernel hotspot plus checker |
| `vbr1_l1_pfd_small_phase_error_response` | dut | 3.136s | 60062 | 0.505s | row_based | event/checker-heavy |
| `vbr1_l1_pfd_small_phase_error_response` | e2e | 2.976s | 60062 | 0.505s | row_based | event/checker-heavy |

这里有两个不同问题：

1. **E2E 外层问题**：r14 all64 中 EVAS checker 为 73.199s，占 EVAS E2E 的
   34.1%；row-based checker 38 行贡献 68.595s checker wall，仍是剩余
   E2E 长尾之一，但已经不再压过 simulator subprocess。
2. **内核调度问题**：gain estimator / gain extraction 四个 row 的 EVAS
   subprocess 约 10s/row，accepted steps 均为 110602，说明 measurement-heavy
   case 仍有 Python-level 调度、CSV、dict/object、recording 或 measurement loop
   优化空间。
3. **CSV 输出问题**：r14 all64 中 EVAS CSV write 总计 11.532s，约占 EVAS
   subprocess 的 11.5%。这不是最大瓶颈，但在 measurement-heavy 行中单行接近
   0.9s 到 1.0s，适合做 checker-specific signal pruning 或 sparse trace。

r3 中 PFD/CPPLL 的历史长尾证明了首批 streaming checker 的价值；r8 进一步证明
release mixed-form alias 补齐后，paper-facing valid43 E2E 可以从慢于 AX 变成快于 AX。
后续优先级变为：先收 all64 剩余 row-based/failing-row checker 长尾，其次是
timer/event queue 和 measurement kernel profile。

## 现有证据与新增计时

历史 full e2e artifact 只能证明一个上界；当前最终速度表应使用 2026-06-02 r14
exact-row rerun 的统一口径 artifact，r8/r7/r6/r5 作为同 row-set 对照，r3/r4 作为历史
优化阶段证据：

| Mode | Runs | Behavior OK | Total E2E wall | Simulator subprocess | Checker | Fixture | CSV/PSF parse | 这能说明什么 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| EVAS fast | 64 | 43 | 214.597s | 100.368s | 73.199s | 32.801s | 11.532s CSV | E2E 与 subprocess 均快于 AX；micro-opts 未证明 full-run 总体加速 |
| Spectre AX equalized | 64 | 45 | 330.908s | 208.065s | 59.802s | 39.885s | 21.900s PSF | 商业加速基线，subprocess 慢于 EVAS |
| Spectre strict | 64 | 45 | 612.383s | 442.794s | 94.478s | 33.244s | 40.978s PSF | 精度参考最慢 |

r14 相对 r8 的同 row-set delta：

| Mode | E2E delta | Subprocess delta | Checker delta | Fixture delta | PSF/CSV delta | 这能说明什么 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| EVAS fast | +3.261s | +0.628s | +0.401s | +0.195s | +0.248s CSV | 新 micro-opts 没有形成 full-run 总体加速 |
| Spectre AX equalized | -7.470s | -1.443s | -1.170s | -6.593s | +1.635s PSF | Spectre 侧也存在单次 rerun 波动 |
| Spectre strict | -8.011s | +4.056s | -5.226s | -9.187s | +2.992s PSF | strict 侧 fixture/checker 变化抵消 subprocess 变化 |

r8 相对 r7 的同 row-set delta：

| Mode | E2E delta | Subprocess delta | Checker delta | Fixture delta | PSF delta | CSV write delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS fast | -235.049s | -0.557s | -202.460s | -27.477s | +0.000s | -0.056s |
| Spectre AX equalized | -83.554s | -0.425s | -61.611s | -15.739s | -5.356s | 0.000s |
| Spectre strict | -274.210s | -8.832s | -238.799s | -6.717s | -19.188s | 0.000s |

这些表可以直接证明 checker、fixture、PSF parse 和 CSV 写入分别花了多少秒；
但它仍不能直接把 `model.evaluate()` 内部的 Python dict/object lookup 单独剥离。
因此已经补充了代码级计时：

- `run_vabench_release_same_server_speed.py`
  - `wall_time_s`：统一为 evaluator E2E wall，包括 fixture materialization/staging、simulator subprocess、转换/解析、checker、validation。
  - `simulator_subprocess_wall_s`：只记录 EVAS/Spectre 子进程 wall。
  - `timing_split`：记录 fixture、subprocess、PSF/CSV、checker、validation 等阶段。
- `simulate_evas.py`
  - `timing_split`：记录 tempdir、copy inputs、preflight、EVAS subprocess、behavior checker、side-output validation、cleanup。
- `EVAS/evas/netlist/runner.py`
  - `Runner timing counters`：记录 `csv_write_s`、`derive_bus_signals_s`。
  - `Section timing counters`：在 `EVAS_PROFILE_SECTIONS=1` 或 `evas_profile_sections=true` 时记录内核 section 时间。
- `EVAS/evas/simulator/engine.py`
  - 记录 `dict_prev_snapshot_s`、`dict_future_snapshot_s`、`model_output_set_s`、`record_point_s`、`model_evaluate_s`、`model_breakpoint_scan_s` 等。

### 2026-06-01 EVAS-only smoke profiling

环境：本地 EVAS-only，`EVAS_PROFILE_SECTIONS=1`，mode 为
`profile_fast_skip_source_error_control`。这个 smoke 只用于证明计时字段可用和
定位开销，不用于替代 full same-server EVAS/Spectre 速度结论。

| Entry | E2E wall | EVAS subprocess | Behavior checker | EVAS reported total | Tran | CSV write | Direct dict/object/trace | Core Python model sections |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | 10.907s | 2.189s | 8.705s | 2.000s | 1.707s | 0.324s | 0.136s | 1.199s |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | 2.455s | 0.591s | 1.855s | 0.400s | 0.352s | 0.076s | 0.039s | 0.218s |
| `vbr1_l1_pfd_up_dn_logic` | 0.196s | 0.160s | 0.027s | 0.000s | 0.012s | 0.001s | 0.002s | 0.005s |
| **Total** | **13.559s** | **2.940s** | **10.587s** | - | - | **0.401s** | **0.177s** | **1.422s** |

字段定义：

- `Direct dict/object/trace` = `dict_prev_snapshot_s + dict_future_snapshot_s + model_output_set_s + record_point_s + result_array_conversion_s`。这是直接可测的 dict copy、set 构造、trace append/array conversion 开销，不包含 `model.evaluate()` 内部的全部 Python object lookup。
- `Core Python model sections` = `model_breakpoint_scan_s + model_prepare_step_s + model_evaluate_s + model_post_update_s`。这是 Python 模型调度/执行主体，不等价于纯 dict 开销，但代表当前 Python-level kernel 的主要耗时。
- `CSV write` 是 EVAS subprocess 内部文件输出开销；copy/tempdir/preflight 在这次 smoke 中均为毫秒级。

这轮 smoke 的直接量化结果：

- CPPLL 中 behavior checker 占 E2E wall 的 79.8%，说明旧口径的长尾 wall 很大一部分可能来自 checker/harness，而非 EVAS kernel 本身。
- CPPLL 中 CSV 写入为 0.324s，占 EVAS subprocess 的 14.8%；ADPLL 中 CSV 写入为 0.076s，占 EVAS subprocess 的 12.9%。
- CPPLL 中直接 dict/object/trace 开销为 0.136s，占 EVAS subprocess 的 6.2%；ADPLL 为 0.039s，占 6.6%。
- 三个 smoke 合计：checker 10.587s，占 E2E wall 的 78.1%；CSV 写入 0.401s，占 EVAS subprocess 的 13.7%；直接 dict/object/trace 0.177s，占 EVAS subprocess 的 6.0%；core Python model sections 1.422s，占 EVAS subprocess 的 48.4%。

因此对这组三行 smoke 更准确的判断是：

> 外层 checker/harness 是这组三行 E2E wall 的最大可测项；EVAS subprocess 内部，CSV 写入是明确的 IO 成本，直接 dict/object/trace 不是最大项但已经可见，Python-level model evaluation/breakpoint/post-update 才是更大的内核开销。

### 2026-06-02 低风险内核/IO 优化 smoke

本轮对 EVAS 做了三类不改变仿真语义的低风险优化：

1. `CompiledModel.next_breakpoint()` 从“收集所有 breakpoint 到 list 后取
   `min()`”改为“扫描时维护当前最小值”，减少每步临时 list 分配。
2. `Simulator.run()` 缓存 `model_output_nodes`，只有模型新增 output node 时才重建
   set；同时用每步 `_step_event_fired` flag 替代每步扫描所有 cross/above
   detector 的 `last_triggered` 状态。
3. CSV 写出时预先缓存 signal array 和格式，避免每个 cell 都做
   `result.signals[sig]` 字典查找和 `sig.endswith()`/format lookup。

这些改动不改变步长、容差、event 触发条件、checker 或输出信号集合；预期影响只在
Python object 分配、dict/set 构造和 CSV 写出循环。

验证环境：

- 远端：`thu-sui`
- Python：`python3` = 3.9.21
- EVAS mode：`profile_fast_skip_source_error_control`
- simulator options：`evas_profile=fast`, `evas_skip_source_error_control=yes`
- 验证命令形态：在 `thu-sui` 上用 `python3` 跑 release gold smoke，不启用
  `EVAS_PROFILE_SECTIONS`，避免 profile instrumentation 扭曲 wall time。

语法验证：

- `python3 -m py_compile EVAS/evas/simulator/backend.py EVAS/evas/simulator/engine.py EVAS/evas/netlist/runner.py`
  在 `thu-sui` Python 3.9.21 上通过。

远端 fast smoke：

| Case | Status | Checker policy | E2E wall | EVAS subprocess | Checker | CSV write |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `vbr1_l1_lfsr_prbs_generator/e2e` | PASS | `streaming_validated` | 0.479s | 0.469s | 0.005s | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e` | PASS | `streaming_validated` | 10.473s | 9.838s | 0.631s | 0.760s |

gain extraction 的 smoke 说明：

- 优化后没有引入 behavior failure：`dut_compile/tb_compile/sim_correct` 均为 1.0。
- CSV 写出仍是明确成本：0.760s，占 EVAS subprocess 的约 7.7%。
- measurement-heavy 行的主要时间仍在 EVAS subprocess 内部，下一步应继续
  profile `gain_estimator` / `gain_extraction` 的 model evaluation、breakpoint
  scan、source update、recording 和 CSV 写出。

Cadence 环境 full rerun 说明：

- r6 strict reference gate 与 r5 一致：EVAS fast 60/64 waveform passed、
  4/64 needs review；AX 64/64 waveform passed。
- r6 没有引入新的 behavior set 变化：EVAS/AX/strict 三者共同 behavior-valid
  row 仍为 43。
- r6 没有形成稳定 E2E 加速：EVAS all64 E2E 从 r5 的 429.681s 变为 436.194s，
  valid43 E2E 从 316.679s 变为 329.351s。
- r6 EVAS CSV write 从 r5 的 11.374s 降到 11.090s，只减少 0.284s；这说明当前
  CSV micro-optimization 的收益太小，不足以改变 full E2E 排名。

注意：`EVAS_PROFILE_SECTIONS=1` 会在每步增加计时调用；在 measurement-heavy
case 上会明显拖慢 wall time。因此 section profiling 只能用于定位热点，不能与
无 profile 的速度表直接比较。

### 2026-06-02 Measurement-heavy section profile

环境：`thu-sui`，`EVAS_PROFILE_SECTIONS=1`，只对两条 measurement-heavy e2e
row 做定位；Spectre AX 同跑仅作辅助对照，不进入最终速度 claim。

| Entry | EVAS subprocess | Tran elapsed | Checker | Accepted steps | CSV write | Direct dict/object/trace | Core model sections | Source scan/update |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `vbr1_l1_gain_estimator/e2e` | 11.244s | 10.010s | 0.611s | 110602 | 0.913s | 0.863s | 6.134s | 0.945s |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e` | 11.168s | 9.954s | 0.611s | 110602 | 0.942s | 0.863s | 6.159s | 0.931s |

主要 section 占比：

| Section | Gain estimator | Gain extraction | Interpretation |
| --- | ---: | ---: | --- |
| `model_evaluate_s` | 3.828s / 34.0% subprocess | 3.884s / 34.8% subprocess | 最大热点，主要是每步执行模型主体 |
| `model_prepare_step_s` | 1.143s / 10.2% | 1.128s / 10.1% | 每步状态准备和 event interpolation buffer |
| `csv_write_s` | 0.913s / 8.1% | 0.942s / 8.4% | 明确 IO 成本，但不是最大项 |
| `model_breakpoint_scan_s` | 0.823s / 7.3% | 0.813s / 7.3% | breakpoint 扫描仍可优化 |
| `err_ratio_node_scan_s` | 0.733s / 6.5% | 0.698s / 6.3% | fast profile 中的误差/节点扫描成本 |
| `source_breakpoint_scan_s + source_update_s` | 0.945s / 8.4% | 0.931s / 8.3% | source 调度成本 |
| direct dict/object/trace | 0.863s / 7.7% | 0.863s / 7.7% | 可见但不是首要瓶颈 |

结论：

> measurement-heavy 行现在不应该优先从“Python dict/object 开销”下手。更大的
> 优先级是把 `model_evaluate`/`model_prepare_step` 中每步无条件执行的逻辑拆开，
> 其次优化 breakpoint/source 扫描，再做 CSV signal pruning。dict/indexed array
> 后端仍有长期价值，但不是这两条 row 的最大立即收益点。

### 2026-06-02 r7 source/err-ratio cache targeted optimization

本轮继续做两处不改变仿真语义的低风险优化：

1. `Source` 在构造时缓存 waveform 的 `_next_breakpoint` 函数，`Simulator.run()`
   每步只扫描真正有 breakpoint 的 source，避免 DC/sine/source helper 每步做无效
   `getattr()` 和 method dispatch。
2. `Simulator.run()` 缓存 error-ratio control 的候选 node 列表；当 node 数量、
   model output version 或 `skip_source_error_control` 没变时，不再每步重复做
   source/output membership 判断，只对候选节点计算同一个 `err_ratio` 公式。

验证：

- 本地 `py_compile` 通过：`evas/simulator/engine.py`、`backend.py`、`runner.py`。
- 本地 targeted pytest 通过：`tests/test_evas_output_cleanup.py`，3 passed。
- 远端 `thu-sui` Python 3.9.21 `py_compile` 通过。
- 远端 measurement-heavy profile/no-profile smoke 均 PASS。

Profile section delta（`EVAS_PROFILE_SECTIONS=1`，只用于定位，不作为正式速度表）：

| Entry | EVAS subprocess | Source breakpoint scan | Err-ratio scan | Status |
| --- | ---: | ---: | ---: | --- |
| `vbr1_l1_gain_estimator/e2e` | 11.244s -> 11.129s | 0.497s -> 0.408s | 0.733s -> 0.609s | PASS -> PASS |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e` | 11.168s -> 11.043s | 0.501s -> 0.413s | 0.698s -> 0.639s | PASS -> PASS |

No-profile targeted smoke（不启用 section profiling；与 r6 full 中同 row 对比，只用于
判断 targeted row 是否回归，不替代 64-row 最终表）：

| Entry | EVAS subprocess | Tran elapsed | Accepted steps | Status |
| --- | ---: | ---: | ---: | --- |
| `vbr1_l1_gain_estimator/e2e` | 10.152s -> 9.788s | 8.867s -> 8.556s | 110602 -> 110602 | PASS -> PASS |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e` | 10.319s -> 10.058s | 9.042s -> 8.763s | 110602 -> 110602 | PASS -> PASS |

结论：

> r7 的 source breakpoint cache 和 err-ratio candidate cache 是有效的小优化：
> 在 measurement-heavy e2e targeted rows 上，subprocess 降低约 0.26s 到 0.37s，
> steps 与 PASS 状态保持不变。full r7 rerun 进一步证明 all64 EVAS subprocess
> 相比 r6 下降 5.283s，但 E2E 被 checker/fixture 增量抵消。因此它可以作为
> kernel/subprocess 优化证据，不能作为 EVAS E2E 快于 AX 的 claim。下一步更大的
> 收益点仍是 `model_evaluate` / `model_prepare_step` 拆分、breakpoint/source
> 扫描进一步结构化，以及 CSV checker-specific signal pruning。

## 代码热点与证据

### 1. EVAS wall time 计时边界偏宽

历史 EVAS 计时在 `run_evas_mode()` 中主要包住整个 `run_case()`：

- `runners/run_vabench_release_same_server_speed.py`
- 函数：`run_evas_mode`
- 关键逻辑：`t0 = time.perf_counter()` 后调用 `run_case(...)`，返回后计算 `wall = time.perf_counter() - t0`

`run_case()` 包含：

- temp directory
- copy inputs
- Spectre-compatible preflight
- EVAS subprocess
- CSV 输出
- behavior checker
- side-output validation
- cleanup

而 Spectre 计时主要包住 `subprocess.run(spectre...)`，PSF parse 和 behavior checker 在停表后执行：

- `runners/run_vabench_release_same_server_speed.py`
- 函数：`run_spectre_direct`

这导致历史 artifact 中的 `wall_time_s` 对 EVAS 和 Spectre 不完全对称。当前代码已
改成统一 E2E `wall_time_s`，并额外保留 `simulator_subprocess_wall_s`。

已完成：

- 将 EVAS 计时拆成阶段指标。
- Spectre 也补充 `psf_parse_s`、`checker_s`，形成对称阶段表。
- 论文/报告主速度可以继续用 e2e wall，但必须同时报告 simulator-only wall 和 harness overhead。

当前字段形态：

```json
{
  "timing_split": {
    "fixture_materialize_s": 0.0,
    "evaluator_e2e_wall_s": 0.0,
    "run_case_evas_subprocess_wall_s": 0.0,
    "run_case_behavior_checker_s": 0.0,
    "psf_parse_s": 0.0,
    "behavior_checker_s": 0.0
  },
  "simulator_subprocess_wall_s": 0.0
}
```

这个新口径已经用于 `e2e_wall_unified_full_20260601_r3.json` 的 full
same-server EVAS/Spectre slice。

### 2. Timer / breakpoint 每步扫描

热点位置：

- `EVAS/evas/simulator/engine.py`
- 函数：`Simulator.run`
- 逻辑：每个 step 都调用 `model.next_breakpoint(time)`

模型侧：

- `EVAS/evas/simulator/backend.py`
- 方法：`CompiledModel.next_breakpoint`
- 逻辑：每步扫描 transitions、cross detectors、above detectors、timer states、child models

CPPLL EVAS fast counters：

```text
timer_absolute_checks = 84810
timer_breakpoint_hits = 84808
model_breakpoint_clamps = 61943
bound_step_clamps = 9559
steps_total = 42404
```

ADPLL EVAS fast counters：

```text
timer_absolute_checks = 9617
timer_breakpoint_hits = 9616
model_breakpoint_clamps = 8038
bound_step_clamps = 2458
steps_total = 9616
```

对应 Verilog-A 触发源：

- `cppll_timer_ref.va`: `@(timer(t_next_toggle))`
- `cppll_timer_ref.va`: `$bound_step(1.0 / (64.0 * dco_freq))`
- `adpll_ratio_hop_ref.va`: `@(timer(t_next_toggle))`
- `adpll_ratio_hop_ref.va`: `$bound_step(1.0 / (96.0 * dco_freq))`

需要修改：

- 用 heap/event queue 管理 timer target。
- 当 timer target 没有变化时，不要每个 step 扫描全部 timer。
- 将 absolute timer event block 编译成 callback，只在 timer 到期附近触发。

风险：

- `timer(t_next_toggle)` 的 target 会在 event body 中更新，不能简单假设固定周期。
- 需要保留 Spectre-like 语义：missed event、同一时间点多事件顺序、与 cross 的先后关系。

建议测试：

- CPPLL
- ADPLL
- digital phase accumulator
- VCO phase integrator

### 3. 所有 analog block 每步 evaluate

热点位置：

- `EVAS/evas/simulator/backend.py`
- 生成方法：`evaluate(self, nv, time)`

当前编译逻辑会在每个 simulator step 执行 analog block 主体，并在其中检查事件：

```python
if self._check_timer_at(...):
    ...
if self._check_cross(...):
    ...
```

这对小模型可接受，但对事件密集模型会产生大量 Python 函数调用和 dict 访问。

需要修改：

- 编译阶段将 analog block 拆成三类：
  - continuous contributions
  - cross/above event callbacks
  - timer callbacks
- 常规 step 只执行 continuous contributions。
- event callback 只在 event queue 或 crossing detector 命中时执行。

风险：

- 当前实现中 event body 和 continuous contribution 的状态交互较多。
- 需要避免改变 `transition()`、`last_crossing()`、`$abstime` 在 event context 中的语义。

### 4. Dict copy / node lookup 开销

热点位置：

- `EVAS/evas/simulator/engine.py`
- 函数：`Simulator.run`

当前每步执行：

```python
prev_nv = dict(self.node_voltages)
future_nv = dict(self.node_voltages)
model._prepare_step(prev_nv, self.node_voltages, prev_time, time, future_nv)
```

模型侧 `_prepare_step()` 也会缓存 dict：

- `EVAS/evas/simulator/backend.py`
- 方法：`CompiledModel._prepare_step`

问题：

- 每一步都复制多个 dict。
- 每次 V(node) 都走字符串 key 查找和 node map。
- event-heavy case step 数很高，Python object overhead 被放大。

需要修改：

- node voltage 使用 indexed array。
- 编译时将 node name 映射为 integer index。
- 只对使用 cross/last_crossing/event interpolation 的模型保存 prev/future buffer。
- 对纯 digital/timer state 模型避免 full dict copy。

优先级：

1. 缓存 output node set。
2. 避免无条件 `future_nv` copy。
3. 给 node_map 增加 integer index fast path。
4. 长期改成 array backend。

### 5. Output recording / CSV 写入影响 wall

热点位置：

- `EVAS/evas/netlist/runner.py`
- 逻辑：调用 `sim.run(..., record_step=tstep, ...)`
- CSV 写入：`_write_csv(...)`

当前 `record_step=tstep` 会强制保存输出采样点，并产生 `output_step_clamps`。

EVAS fast counters 中较高的输出相关项：

```text
output_step_clamps = 5875
```

在长尾行中：

| Entry | output_step_clamps | EVAS wall | EVAS internal |
| --- | ---: | ---: | ---: |
| `vbr1_l1_bang_bang_phase_detector` | 1177 | 2.735s | 0.200s |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | 1153 | 58.388s | 2.000s |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | 633 | 13.625s | 0.500s |

需要修改：

- 将 simulation internal event points 和 output sample points 分离。
- fast mode 下只保存 checker 必需 signals 和 sample points。
- 对 digital/event signals 可以考虑 edge list 或 sparse trace，再在需要时导出 CSV。
- CSV 写入时间单独计入 `csv_write_s`，不要和 kernel sim time 混在一起。

### 6. `$bound_step` 过度约束事件驱动 fast mode

CPPLL 和 ADPLL 中 `$bound_step` 明显增加步数：

- CPPLL: `$bound_step(1.0 / (64.0 * dco_freq))`
- ADPLL: `$bound_step(1.0 / (96.0 * dco_freq))`

AX 在某些 case 下仍能以更少 wall time 处理这些约束，EVAS 则倾向于把它们转化为 Python 层大量小步。

需要修改：

- 对纯 voltage-domain behavioral task，引入 fast profile 下的 `$bound_step` policy：
  - strict mode：完全遵守。
  - fast mode：作为 event localization hint，而非强制全局 step ceiling。
  - 如果模型使用连续积分/analog state，则保守遵守。
  - 如果模型主要是 timer/cross/digital state，则允许 coarsen。

风险：

- 这会影响 edge timing，需要严格用 strict Spectre reference gate 验证。
- 先只在 CPPLL/ADPLL/PFD stress set 上实验。

## AX 为什么精度仍更稳、部分行仍快

从 r14 当前数据看，EVAS fast 已在 all64 和 valid43 E2E 总 wall 上快于 AX；
但 AX 的精度 gate 仍更完整，并且在部分单行上仍能用更少 wall time。更准确的解释是：

1. r8/r14 已经收掉一批 checker/harness 长尾，但 all64 中仍有 38 行 row-based checker；
   EVAS all64 checker 仍约 73.199s。
2. 在 simulator subprocess 口径下，EVAS fast 总体已经快于 AX；AX 的局部优势
   主要体现在少数 measurement-heavy 或 failed-row checker-heavy 行。
3. AX 对 Verilog-A behavioral 事件、timer、transition、输出保存有成熟的内部优化；
   EVAS 当前仍有 Python-level loop、CSV 写入、dict/object model 和 checker 调用开销。
4. AX 在 strict reference gate 上没有新增 needs-review 行；EVAS fast 还有
   ADC/DAC reconstruction 和 weighted SAR ADC/DAC 相关 4 行需要单独 triage。

典型例子：

| Entry | AX steps | EVAS steps | Observation |
| --- | ---: | ---: | --- |
| `vbr1_l1_pfd_small_phase_error_response/dut` | 435 | 60062 | AX 步数极少但 strict gate 通过；EVAS E2E 主要慢在 row-based checker |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e` | 110602 | 110602 | 步数相同，但 EVAS subprocess 约 9.935s，需继续优化 measurement-heavy kernel |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow/tb` | 16032 | 9616 | EVAS 步数更少但 E2E 更慢，说明 Python/harness overhead 仍明显 |

## 建议修改路线

### Phase 0: 先修计时边界

目标：确认“EVAS 内核慢”还是“评测外壳慢”。

状态：基础埋点已完成，smoke profiling 已能输出阶段耗时；full
same-server EVAS/Spectre slice 已在 `e2e_wall_unified_full_20260601_r3.json`
、`e2e_wall_unified_full_20260601_r4_streaming.json`、
`e2e_wall_unified_full_20260602_r5_fast_ax_strictref.json` 和
`e2e_wall_unified_full_20260602_r6_kernel_lowrisk_exactrows.json`、
`e2e_wall_unified_full_20260602_r7_src_err_cache_exactrows.json`、
`e2e_wall_unified_full_20260602_r8_streaming_aliases_exactrows.json`、
`e2e_wall_unified_full_20260602_r14_core_fastpath_exactrows.json` 生成正式统计表。

任务：

- 在 `run_vabench_release_same_server_speed.py` 中增加 EVAS timing split。
- 在 `simulate_evas.run_case()` 中记录：
  - temp setup
  - copy inputs
  - preflight
  - subprocess wall
  - behavior checker
  - side-output validation
  - cleanup
- 在 EVAS CLI/runner 中记录：
  - parse netlist
  - compile VA
  - setup simulator
  - sim.run
  - derive bus signals
  - CSV write
  - strobe/write outputs
- 对 Spectre 增加：
  - subprocess wall
  - PSF parse
  - behavior checker

验收：

- 同一 64-row slice 输出阶段耗时表。状态：已完成。
- 能解释 r3 EVAS fast 统一 E2E wall 中的主要来源：checker 180.735s，
  fixture/materialization 60.658s，EVAS subprocess 49.737s。
- 能解释 r4 EVAS fast 改善来源：checker 从 180.735s 降到 48.495s，
  E2E wall 从 301.694s 降到 159.810s。

### Phase 0.5: 先收掉 checker/harness 长尾

目标：不改 EVAS 仿真语义，先降低 E2E wall 中已定位的 checker/harness 长尾。

任务：

- 为 release task id 补齐已有 streaming checker alias。当前
  `simulate_evas.py` 的 `STREAMING_BEHAVIOR_CHECKS` 已包含
  `pfd_reset_race_smoke`，但 release id `vbm1_pfd_reset_race_e2e` 未进入
  streaming 映射；这导致 PFD 行走 row-based checker，EVAS fast checker
  达到 54.228s。
- 为 `cppll_freq_step_reacquire_smoke` 增加 streaming checker。当前 CPPLL
  checker 在 full rows 上执行 `rising_edges`、window fraction、min/max 等操作，
  EVAS fast checker 达到 78.056s；subprocess 本身只有 2.540s。
- 对 streaming checker 做 parity test：默认 checker 与 streaming checker 在已有
  pass/fail fixture 和真实 CSV 上保持同样 pass/fail，不一致时禁止作为
  paper-facing 速度口径。
- 在 same-server runner 中单独报告 checker policy，避免把 checker 优化误读成
  EVAS kernel 优化。
- 2026-06-02 继续补齐第二批 streaming checker：LFSR、hysteresis window、
  phase accumulator wrap、precision rectifier/envelope、programmable stimulus
  sequencer、ADPLL ratio hop、sample-and-hold droop。

验收：

- PFD 和 CPPLL 的 checker 时间显著下降。状态：已完成，PFD 54.228s -> 0.194s，
  CPPLL 78.056s -> 0.387s。
- Behavior PASS/FAIL 与默认 checker parity 一致。状态：已完成，在 r3 CSV 上
  PFD 与 CPPLL 均为 row checker PASS、streaming checker PASS。
- Full E2E 速度表重新生成，不混用优化前后的 checker policy。状态：已完成，
  r4 报告为 `e2e_wall_unified_full_20260601_r4_streaming.json`。
- 第二批 7 个 checker 的真实 r4 CSV parity。状态：已完成，14/14 match，
  direct checker wall 23.162s -> 3.931s。
- 第二批 7 个 checker 的 run-case smoke。状态：已完成，fast-mode checker
  wall 29.146s -> 0.294s，全部 PASS。
- 第二批 checker 后的 Cadence 环境 full EVAS-vs-AX/strict rerun。状态：已完成，
  r8 使用 r5 exact 64-row manifest；row set 与 r5/r6/r7 一致，behavior-valid
  set 仍为 43 rows。r8 valid43 E2E 为 EVAS 113.230s vs AX 204.654s，
  `T(AX)/T(EVAS)=1.807x`。

### Phase 1: 低风险 Python 开销优化

目标：不改变仿真语义，先减少确定性 overhead。

任务：

- 缓存 `model_output_nodes`，避免每步重建 set。状态：已完成。
- 用 `_step_event_fired` flag 替代每步扫描全部 cross/above detector。状态：已完成。
- `next_breakpoint()` 避免临时 list/min 分配。状态：已完成。
- CSV 写出预缓存 signal array 和格式。状态：已完成。
- Source breakpoint 只扫描有 `_next_breakpoint` 的 source。状态：已完成。
- Error-ratio control 缓存候选 node 列表，避免每步重复 source/output membership
  判断。状态：已完成。
- 避免无条件 `future_nv = dict(...)`。状态：已完成；cross exact-touch 需要
  future source value 的模型走 lazy lookup，其余模型不再每步构造完整 future
  snapshot。
- `_prepare_step()` 对不使用 event interpolation 的模型走轻量路径。状态：已完成；
  但 r14 full-run 未证明这部分 micro-opts 带来总体加速。
- CSV/checker 时间拆出主速度 claim。

验收：

- 远端 `thu-sui` Python 3.9.21 `py_compile` 通过。状态：已完成。
- fast-mode smoke 不引入 behavior failure。状态：已完成，LFSR e2e 与 gain
  extraction e2e 均 PASS。
- strict reference gate 不低于当前 EVAS fast 基线：60/64 passed、4 needs review。状态：已完成，r14/r8/r7/r6/r5 证据口径一致。
- CPPLL/PFD/ADPLL wall 降低。状态：部分达成。CPPLL e2e 为 6.026s -> 3.070s，
  CPPLL tb 为 31.216s -> 17.031s；PFD 和 ADPLL mixed-form 有升有降，例如
  PFD small-phase e2e 为 53.132s -> 47.828s，但 dut 为 45.927s -> 56.688s，
  ADPLL e2e 为 1.265s -> 1.183s，但 tb 为 5.617s -> 10.088s。因此需要
  targeted profile，不能 claim 稳定加速。
- EVAS fast total wall 降低，且不引入新的 behavior failure。状态：阶段性达成。
  r8 未引入新的 behavior-valid set 变化；all64 EVAS E2E 从 r7 的 446.385s
  降至 211.336s，valid43 EVAS E2E 从 341.302s 降至 113.230s。
  r14 在 r8 基础上继续保持相同 PASS 集合，但 all64 EVAS E2E 为 214.597s、
  valid43 为 117.394s，说明新增 core micro-opts 未形成 full-run 总体加速。
- r7 source/err-ratio cache targeted smoke。状态：已完成，两条 measurement-heavy
  e2e row 均 PASS；无 profile EVAS subprocess 分别为 10.152s -> 9.788s 和
  10.319s -> 10.058s。full r7 rerun 已完成，证明 subprocess 收益存在，但
  E2E 被 checker/fixture 增量抵消。

### 2026-06-02 r15 timer breakpoint cache smoke

本轮继续针对 timer/breakpoint 扫描做一处低风险优化：`CompiledModel` 缓存当前
timer state 下的最早 timer breakpoint，并在 timer state、`timer_last_fired` 或
event-body re-arm 更新时失效。它不改变 `timer()` 触发条件、不改变 event body
执行顺序，也不改变 `$bound_step` 或 checker；预期只减少每步重复扫描
`timer_states` 的 Python overhead。

代码验证：

- 本地 `py_compile` 通过：`backend.py`、`engine.py`、`test_engine.py`。
- 本地 `EVAS/tests/test_engine.py -q`：167 passed。
- 本地 `EVAS/tests -q`：396 passed。
- 远端 `thu-sui` Python 3.9.21 `py_compile` 通过。
- 远端 `EVAS/tests/test_engine.py -q`：167 passed。

远端 no-profile EVAS-only run-case smoke：

| Case | Accepted steps | EVAS subprocess | Tran elapsed | Checker | CSV write | Timer breakpoint scans | Timer breakpoint cache hits | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/e2e` | 43438 | 2.575s | 1.915s | 0.175s | 0.354s | ref step clk: 611; CPPLL: 9624 | ref step clk: 45370; CPPLL: 36357 | run_case PASS, `streaming_validated` |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow/e2e` | 9618 | 0.846s | 0.495s | 0.145s | 0.091s | 2562 | 10078 | run_case PASS, `streaming_validated` |

带 section profiling 的 CPPLL smoke 进一步显示：

| Section | Time |
| --- | ---: |
| `model_breakpoint_scan_s` | 0.302s |
| `model_evaluate_s` | 0.854s |
| `model_post_update_s` | 0.194s |
| `model_prepare_step_s` | 0.147s |
| `csv_write_s` | 0.353s |

结论：

> timer breakpoint cache 已经在 CPPLL/ADPLL 这类 absolute-timer case 上生效，
> 大量每步 timer breakpoint 查询变成 cache hit；当前证据说明它没有改变 steps
> 或 PASS 状态。但这还只是 EVAS-only smoke，不能替代 same-row full EVAS-vs-AX
> 速度表。下一步需要把 r15 放进 exact-row smoke/full rerun，观察 full-run
> EVAS subprocess 是否稳定下降。

补充：已尝试用 2-row 临时 manifest 跑 r15 same-server smoke
`e2e_wall_unified_smoke_20260602_r15_timer_cache.json`。EVAS 两条 row 均 PASS，
但 Spectre AX/strict 四个 work item 因当前裸 `ssh` shell 找不到 `spectre`
可执行文件而 `ERROR`，因此该 smoke 只能作为 EVAS run-case 证据，不能作为
EVAS-vs-AX 速度对照。

执行备注：`thu-sui` 的默认 non-interactive shell 不直接暴露 `spectre`；
需要先 source `/home/cshrc/.cshrc.cadence.IC618SP201`。source 后可见
`/home/cadence/spectre/SPECTRE211Hotfix/tools/bin/spectre` 和
`/usr/bin/python3`。r15 full exact-row rerun 已改用
`speed-optimization/reports/e2e_wall_unified_rows_20260601.json` 作为 64-row
manifest；误用默认 `speed_debug_artifact.json` 只会选到 4 rows，不能作为
full rerun。

### 2026-06-02 r16 CSV writer candidate

本地新增一个只影响输出层的 CSV writer 优化：默认使用 `numpy.savetxt` 批量
格式化 `tran.csv`，保留 `EVAS_CSV_WRITER=python` 作为旧 Python/csv writer
回退。该改动不改变 EVAS 内核、步长、event 触发、checker 或保存信号集合；
只替换 `tran.csv` 的写出路径。

当前证据：

- 本地 `EVAS/tests/test_netlist.py -q`：65 passed。
- 本地 `EVAS/tests -q`：398 passed。
- `git diff --check`：通过。
- microbench：120000 rows、5 columns，new writer 0.235s，old Python/csv
  writer 0.814s，约 3.47x；输出逐字节一致。
- r14 all64 中 EVAS `csv_write_s` 总计 11.532s，EVAS subprocess 总计
  100.368s，CSV 占约 11.5%。按 microbench 粗略外推，CSV 写出可能减少到
  约 3.3s，节省约 8s subprocess；这只是候选收益，最终需要 r16 same-server
  rerun 验证。

约束：

- 不应在 r15 full rerun 运行期间把该改动同步到 `thu-sui`，否则 r15 会变成
  旧 writer 与新 writer 混合的污染结果。
- 等 r15 报告拉回后，再同步 `runner.py` 和 `test_netlist.py` 到远端，跑 r16
  targeted smoke/full rerun。

### Phase 2: Timer event queue

目标：解决 CPPLL/ADPLL/digital timer 长尾。

任务：

- 使用 heap 管理 absolute timer targets。
- 编译 timer event 为 callback。
- timer target 更新时更新 heap entry。
- 支持 stale heap entry 跳过。
- 已完成一个低风险前置步骤：缓存当前 timer state 的最早 timer breakpoint，
  减少每步重复扫描；完整 heap/event queue 仍待做。

验收：

- CPPLL `timer_absolute_checks` 显著下降。
- CPPLL `model_breakpoint_clamps` 显著下降。
- CPPLL/ADPLL reference comparison 仍通过。

### Phase 3: Event callback split

目标：避免每步执行所有 event 判断。

任务：

- 编译 continuous path 与 event path。
- cross/above 只在候选 crossing 附近运行。
- timer 只在 event queue 命中时运行。
- 保留 `$abstime`、event interpolation、last_crossing 语义。

验收：

- PFD steps 和 wall 明显下降。
- cross-heavy tasks reference comparison 仍通过。

### Phase 4: Indexed node array backend

目标：长期替换 Python dict/string lookup。

任务：

- 编译期生成 node index。
- `V(node)` 编译为 array index 访问。
- record signals 使用 index list。
- 对 child model node mapping 生成 index indirection。

验收：

- 大部分 row wall 下降。
- 不引入波形等价 regression。

## 审阅问题

需要团队确认：

1. 速度 claim 主指标是否仍用 e2e wall，还是拆成 `simulator-only wall` 和 `evaluator e2e wall` 两张表？
2. EVAS fast 是否允许将 `$bound_step` 作为 hint，而不是 strict ceiling？
3. paper 中是否只 claim “快于 Spectre strict”，还是继续以“追平/超过 AX”为优化目标？
4. 是否接受 fast mode 的输出保存策略变化，例如 sparse trace 或 checker-specific sampling？
5. Phase 0 是否先作为独立 PR，不混入内核优化？

## 推荐当前口径

当前报告中建议使用：

> 在 2026-06-02 r14 统一复测下，EVAS fast 在 all64 和 paper-facing valid43
> 两个 E2E wall 口径下均快于 Spectre AX。all64 为 214.597s vs 330.908s，
> `T(AX)/T(EVAS fast)=1.542x`；valid43 为 117.394s vs 199.305s，
> `T(AX)/T(EVAS fast)=1.698x`。EVAS fast 的 simulator subprocess 仍明显快于
> Spectre AX：all64 为 100.368s vs 208.065s，valid43 为 68.994s vs 143.595s，
> 约 2.1x。精度上仍不能声明 EVAS 比 AX 更精准；当前只能声明 EVAS fast
> 在同 row-set、同 checker policy、同 E2E wall 口径下快于 AX，且在 43 个
> paper-facing valid rows 上保持原有 behavior-valid 集合。r14 没有证明新增
> micro-opts 带来 full-run 总体加速；作为正式 paper-facing speed claim 前，
> 还需要 repeated cold/warm runs 复核。
