# EVAS/Spectre 全量 e2e 速度与精度综合报告

日期：2026-05-26
机器：`thu-sui`
样本：vaBench release gold e2e 全量 64 行
本报告结论来源：

- `precision_ranking_full_e2e_20260526.json`：EVAS fast、Spectre AX default、Spectre strict reference。
- `precision_ranking_full_e2e_equalized_20260526.json`：EVAS fast、EVAS strict、Spectre AX equalized、Spectre strict reference。

## 核心结论

1. 这轮全量 equalized 实验里，4 个模式共 256 次仿真全部生成波形，`simulation_ok = 256/256`。
2. 行为 checker 结果在 4 个模式下完全一致：每个模式都是 `57/64` 通过，`7/64` 不通过。这 7 个不通过在 strict Spectre reference 下也不通过，因此先归类为任务/checker/gold 口径问题，不归因于 EVAS fast 的速度优化。
3. 以 `spectre_reference_strict_primary` 作为参考，EVAS fast、EVAS strict、Spectre AX equalized 都是 `64/64` 通过 reference comparison。当前证据支持的说法是：EVAS fast 在本轮 gate 下没有造成额外功能精度损失；但这不是逐点波形完全相同。
4. 速度上，EVAS fast 相比 EVAS strict 有明确加速：总时间 `525.160s -> 190.458s`，总时间加速 `2.757x`，几何平均 `1.533x`。
5. EVAS fast 相比 strict Spectre 更快：总时间 `242.031s vs 190.458s`，总时间加速 `1.271x`，几何平均 `2.790x`，`57/64` 行更快。
6. EVAS fast 当前还不能声明快于 Spectre AX。在统一 Spectre 容差/步长口径后，Spectre AX equalized 总时间 `66.184s`，EVAS fast 总时间 `190.458s`，即 `Spectre AX / EVAS = 0.348x`，等价于 EVAS 总时间约为 AX 的 `2.878x`。
7. 因此当前 paper 口径应改为：EVAS fast 已通过 strict Spectre reference gate，且快于 strict Spectre；但在 full e2e equalized 条件下尚未快于 Spectre AX。后续优化方向应集中在事件/定时密集长尾任务，而不是继续放宽精度。

## 统一评测口径

本轮使用 strict Spectre 作为参考条件。`spectre_reference_strict_primary` 和 `spectre_ax_equalized_precision` 都显式统一为：

| 项 | 设置 |
| --- | --- |
| `errpreset` | `conservative` |
| `reltol` | `1e-5` |
| `vabstol` | `1e-8` |
| `iabstol` | `1e-12` |
| `gmin` | `1e-12` |
| `maxstep` | 沿用同一任务 testbench 的 `tran maxstep` |

注释：

- Spectre 的容差控制连续时间模拟中数值积分和非线性求解的误差目标；它会影响速度和波形，因此 AX/default 与 strict 如果不统一设置，就不适合作为最终精度排序依据。
- EVAS 是 voltage-domain event-driven evaluator，没有 Spectre 同类的 KCL/KVL 连续求解容差。EVAS 的“精度”不应写成 `reltol/vabstol` 对齐，而应写成：在同一 testbench、同一 stop/maxstep 输入条件下，输出是否通过行为 checker 和 strict Spectre reference comparison。
- `maxstep` 在输入配置上统一，但不同仿真器内部接受步、事件调度、cross/timer 处理方式不同；不能理解为“每个步长里做完全相同的计算”。
- 本报告不用 P95 作为主表达。速度用总 wall time、几何平均逐行速度比、逐行胜负和长尾任务；精度用 simulation_ok、behavior_ok 和 reference comparison gate。

## Equalized 模式总表

| Backend | Mode | Runs | Sim OK | Behavior OK | Behavior non-OK | Total wall s | Mean wall s | Geomean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS | `profile_fast_skip_source_error_control` | 64 | 64 | 57 | 7 | 190.458 | 2.976 | 1.243 |
| EVAS | `strict_current` | 64 | 64 | 57 | 7 | 525.160 | 8.206 | 1.906 |
| Spectre | `spectre_ax_equalized_precision` | 64 | 64 | 57 | 7 | 66.184 | 1.034 | 0.938 |
| Spectre | `spectre_reference_strict_primary` | 64 | 64 | 57 | 7 | 242.031 | 3.782 | 3.469 |

## 精度结果

精度 gate 以 strict Spectre reference 为基准。`Passed` 表示 waveform equivalence policy 通过；`Behavior OK` 表示任务 checker 通过。

| Candidate | Reference | Runs | Reference comparison passed | Needs review | Blocked | Worst max abs V | Worst relative RMS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `evas/profile_fast_skip_source_error_control` | `spectre_reference_strict_primary` | 64 | 64 | 0 | 0 | 1.000 | 0.127836 |
| `evas/strict_current` | `spectre_reference_strict_primary` | 64 | 64 | 0 | 0 | 1.000 | 0.127836 |
| `spectre/spectre_ax_equalized_precision` | `spectre_reference_strict_primary` | 64 | 64 | 0 | 0 | 1.000 | 0.122542 |

解释：

- 当前 gate 下，EVAS fast 和 EVAS strict 的 reference comparison 结果相同，都是 `64/64` passed。
- EVAS fast 没有引入额外 behavior failure：所有模式都是 `57/64` behavior OK。
- `Worst max abs V = 1.000` 主要来自 rail-level digital/timing 信号的可接受事件偏移，不应单独解读为功能错误；最终判断以 reference comparison gate 和 checker 为准。
- 不应宣传“EVAS 比 AX 更精准”。更稳妥的表述是：EVAS fast 与 Spectre AX equalized 都通过 strict Spectre reference gate，本轮没有观察到 EVAS fast 的额外精度损失。

## 速度结果

表中速度比定义为 `baseline wall time / candidate wall time`。大于 1 表示 candidate 更快，小于 1 表示 candidate 更慢。

| Baseline | Candidate | Rows | Candidate faster rows | Total speed ratio | Geomean speed ratio | 结论 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| EVAS strict | EVAS fast | 64 | 43 | 2.757x | 1.533x | EVAS fast 对 EVAS strict 有明确内核级加速 |
| strict Spectre | EVAS fast | 64 | 57 | 1.271x | 2.790x | EVAS fast 快于 strict Spectre |
| Spectre AX equalized | EVAS fast | 64 | 32 | 0.348x | 0.755x | EVAS fast 当前慢于 AX equalized |
| Spectre AX equalized | EVAS strict | 64 | 17 | 0.126x | 0.492x | EVAS strict 不是速度模式 |

作为补充，未统一 Spectre 设置的 default/product 结果是：EVAS fast 对 Spectre AX default 在 `44/64` 行更快，几何平均 `1.558x`，但总时间速度比只有 `0.723x`。这组结果只能说明 default 产品设置下的现象，不能作为最终统一精度/速度结论。

## Behavior non-OK 的 7 个任务

这 7 行在 EVAS fast、EVAS strict、Spectre AX equalized、Spectre strict reference 下行为 checker 都不通过，优先按 benchmark/checker/gold 问题审计。

| Entry | 失败摘要 |
| --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac` | DAC code/level checker mismatch，16 个采样中 8 个 code mismatch |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | SAR feedback DAC mismatch，校准状态覆盖和差分输出 checker 不通过 |
| `vbr1_l1_charge_pump_abstraction` | checker 期望的 `time/clk/rst/up/dn/vctrl/metric` 信号缺失 |
| `vbr1_l1_higher_order_filter` | reset 后输出指标不满足 checker |
| `vbr1_l1_soft_hysteretic_limiter` | high-compression 指标不满足 checker |
| `vbr1_l2_amplifier_filter_chain` | preamp/filter target metric 不满足 checker |
| `vbr1_l2_complete_calibration_loop` | reset mean 指标不满足 checker |

## EVAS fast 相对 AX equalized 的主要长尾

这些行解释了为什么 EVAS fast 的逐行几何平均接近 AX，但总时间仍明显慢于 AX。优化优先级应从这里开始。

| Entry | AX wall s | EVAS fast wall s | AX/EVAS ratio | EVAS 慢约 |
| --- | ---: | ---: | ---: | ---: |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | 1.643 | 58.388 | 0.028x | 35.5x |
| `vbr1_l1_pfd_up_dn_logic` | 0.826 | 22.278 | 0.037x | 27.0x |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | 1.069 | 13.625 | 0.078x | 12.8x |
| `vbr1_l1_gain_trim_controller` | 0.771 | 4.208 | 0.183x | 5.5x |
| `vbr1_l1_pipeline_adc_stage` | 0.822 | 3.955 | 0.208x | 4.8x |
| `vbr1_l1_lfsr_prbs_generator` | 1.003 | 4.172 | 0.240x | 4.2x |
| `vbr1_l2_programmable_stimulus_sequencer` | 0.812 | 2.579 | 0.315x | 3.2x |
| `vbr1_l1_bang_bang_phase_detector` | 0.882 | 2.735 | 0.323x | 3.1x |

## 对后续计划的影响

1. 论文/报告中不要再写“EVAS 比 Spectre AX 更快且更精准”。当前数据不支持这个口径。
2. 可以写：“在 64 个 full e2e gold rows 上，EVAS fast 通过 strict Spectre reference gate，未引入额外 behavior failure，并相对 strict Spectre 获得 `1.271x` 总时间加速；相对 EVAS strict 获得 `2.757x` 内部加速。”
3. 若目标仍是超过 Spectre AX，需要优先优化 CPPLL/PFD/ADPLL/gain/timer/LFSR 等事件密集长尾；这些少数任务支配总时间。
4. 在 paper-facing speed claim 前，建议对最终优化后的同一 row slice 做 3 到 5 轮 cold/warm repeated runs，报告总时间、几何平均、逐行胜负和长尾稳定性。
5. 在最终 benchmark claim 前，先审计 7 个 behavior non-OK 行；否则 `57/64` 会成为 benchmark 质量而不是 EVAS 精度的主要疑点。

## 最终可用口径

推荐当前统一口径：

> strict Spectre 是参考条件；Spectre AX equalized 是同一容差/步长条件下的加速商业基线；EVAS fast 是事件驱动快速 evaluator。EVAS fast 的精度用 strict Spectre reference comparison 和行为 checker 定义，而不是用 Spectre 的 `reltol/vabstol` 定义。本轮 full e2e equalized 结果显示，EVAS fast 通过全部 strict Spectre reference comparison，未产生额外 behavior failure，并快于 strict Spectre；但当前尚未快于 Spectre AX equalized。
