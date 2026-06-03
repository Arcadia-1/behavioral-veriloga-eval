# EVAS R34 本地重跑与瓶颈分析

Date: 2026-06-03

## 结论

本轮重跑显示，034 static lifecycle fastpath 之后，当前 top-wall 样本的最大内核瓶颈已经不是生命周期空检查，而是 **model evaluate 本体**。

在 top-wall 10 行 section-profile 中：

| 层级 | 总耗时 | 占 tran_elapsed | 占 EVAS subprocess |
| --- | ---: | ---: | ---: |
| model_evaluate_s | 5.892160 s | 51.5% | 42.6% |
| model_breakpoint_scan_s | 0.953596 s | 8.3% | 6.9% |
| model_post_update_s | 0.655957 s | 5.7% | 4.7% |
| model_prepare_step_s | 0.462973 s | 4.0% | 3.3% |
| err_ratio_node_scan_s | 0.391551 s | 3.4% | 2.8% |
| csv_write_s | 0.329731 s | 2.9% | 2.4% |

因此下一轮大瓶颈优化应该优先进入模型执行路径：节点电压读写、输出写入、状态变量访问、事件条件判断和可 Rust 化/compiled evaluate 的模型分支。timer/breakpoint/post_update 仍然值得优化，尤其是 CPPLL 和 propagation-delay 这类事件重的任务，但不是当前总量第一瓶颈。

## 本轮重跑范围

这次重跑是 **本地 Mac EVAS-only profile**，用于定位 EVAS 内核瓶颈，不用于论文级 Spectre AX 速度 claim。

| 项目 | 设置 |
| --- | --- |
| Host | BucketsrandeMacBook-Air.local |
| Row source | speed-optimization/reports/e2e_wall_unified_rows_from_r14_exactrows_20260602.json |
| Runner | runners/run_vabench_release_same_server_speed.py |
| EVAS mode | profile_fast_skip_source_error_control |
| Spectre | skipped |
| Jobs | 1 |
| 主要样本 | top-wall 10 rows |
| 额外样本 | measurement-heavy 2 rows |

Profile artifact：

- speed-optimization/reports/e2e_wall_profile_20260603_r34_static_lifecycle_postprofile.json
- speed-optimization/reports/e2e_wall_profile_20260603_r34_static_lifecycle_sections.json
- speed-optimization/reports/e2e_wall_profile_20260603_r34_top10_sections.json
- speed-optimization/reports/e2e_wall_profile_20260603_r34_top10_default.json
- speed-optimization/reports/e2e_wall_profile_20260603_r34_top10_lifecycle_off.json

Direct EVAS logs：

- /private/tmp/evas-r34-direct-profile/gain_estimator.log
- /private/tmp/evas-r34-direct-profile/gain_extraction.log
- /private/tmp/evas-r34-direct-profile/weighted_sar.log
- /private/tmp/evas-r34-direct-profile/cppll.log
- /private/tmp/evas-r34-direct-profile/prop_delay.log

## Top-wall 10 行总量

section-profile run：

| 指标 | 数值 |
| --- | ---: |
| Rows | 10 |
| Behavior PASS | 10 |
| E2E wall total | 17.551255 s |
| EVAS subprocess total | 13.838571 s |
| tran_elapsed total | 11.442900 s |
| behavior checker total | 3.564384 s |

无 section 插桩控制组：

| 配置 | Rows | PASS | E2E wall | EVAS subprocess | tran_elapsed | checker |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| default fastpath on | 10 | 10 | 13.961882 s | 10.316363 s | 7.695400 s | 3.489382 s |
| EVAS_STATIC_LIFECYCLE_FASTPATH=0 | 10 | 10 | 14.041723 s | 10.310930 s | 7.721000 s | 3.577059 s |

解释：section-profile 会增加插桩开销，所以它用于判断瓶颈比例，不作为速度 claim。无插桩控制组里 fastpath on/off 的 top10 总量几乎相同，说明这批最慢任务主要不是 static lifecycle 空转；034 对纯静态链路有效，但 top-wall 这批更偏事件/动态模型。

## 逐行最大瓶颈

| Entry/Form | E2E wall | Subprocess | tran_elapsed | Checker | 最大 section |
| --- | ---: | ---: | ---: | ---: | --- |
| vbr1_l1_gain_estimator/tb | 0.272 s | 0.256 s | 0.039 s | 0.005 s | model_evaluate_s = 0.019886 s |
| vbr1_l2_gain_extraction_convergence_measurement_flow/tb | 1.445 s | 1.398 s | 1.170 s | 0.031 s | model_evaluate_s = 0.601141 s |
| vbr1_l1_gain_estimator/e2e | 0.248 s | 0.232 s | 0.039 s | 0.005 s | model_evaluate_s = 0.019712 s |
| vbr1_l2_gain_extraction_convergence_measurement_flow/e2e | 1.427 s | 1.381 s | 1.156 s | 0.031 s | model_evaluate_s = 0.589325 s |
| vbr1_l1_pfd_up_dn_logic/bugfix | 0.225 s | 0.205 s | 0.013 s | 0.001 s | model_evaluate_s = 0.004808 s |
| vbr1_l2_weighted_sar_adc_dac_loop/tb | 5.596 s | 2.796 s | 2.521 s | 2.784 s | model_evaluate_s = 1.597306 s |
| vbr1_l1_propagation_delay_comparator/dut | 2.114 s | 1.736 s | 1.503 s | 0.362 s | model_evaluate_s = 0.662178 s |
| vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/e2e | 2.932 s | 2.757 s | 2.448 s | 0.160 s | model_evaluate_s = 1.166642 s |
| vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/tb | 2.878 s | 2.697 s | 2.393 s | 0.164 s | model_evaluate_s = 1.147054 s |
| vbr1_l1_lfsr_prbs_generator/dut | 0.414 s | 0.380 s | 0.160 s | 0.020 s | model_evaluate_s = 0.084108 s |

注意：`vbr1_l2_weighted_sar_adc_dac_loop/tb` 的 E2E wall 被 checker 拉高，checker 是 2.784 s，几乎等于 EVAS subprocess 2.796 s。这个是 E2E 层问题，不代表 EVAS 内核本身慢在 checker。

## Direct log 中的模型级瓶颈

Direct EVAS log 可以看到 model instance 粒度：

| Case | 主要模型瓶颈 | 证据 |
| --- | --- | --- |
| weighted_sar | dac_weighted_8b_Model + sar_adc_weighted_8b_Model | dac evaluate 1.010072 s，sar_adc evaluate 0.956026 s |
| cppll | cppll_timer_ref_Model | evaluate 1.170903 s，post_update 0.260896 s |
| gain_extraction | lfsr_Model + vin_src_Model | lfsr evaluate 0.245609 s，vin_src evaluate 0.163032 s |
| prop_delay | cmp_delay_Model + edge_interval_timer_Model | cmp_delay evaluate 0.561344 s，edge_interval_timer evaluate 0.354525 s |
| gain_estimator | gain_estimator_Model | evaluate 0.019927 s |

这说明瓶颈不是平均散落在 runner 或 CSV 上，而是集中在具体模型的 evaluate 循环里。

## Measurement-heavy 2 行复核

section-profile：

| Entry/Form | E2E wall | Subprocess | tran_elapsed | model_evaluate | model_prepare_step | model_breakpoint_scan | csv_write |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| vbr1_l1_gain_estimator/e2e | 0.375194 s | 0.356174 s | 0.042700 s | 0.021602 s | 0.001240 s | 0.002274 s | 0.004796 s |
| vbr1_l2_gain_extraction_convergence_measurement_flow/e2e | 1.548909 s | 1.502344 s | 1.184300 s | 0.608008 s | 0.049492 s | 0.063329 s | 0.022884 s |

这里同样是 `model_evaluate_s` 约占 tran 的一半。CSV 在 gain_estimator 里比例较高，但绝对值只有毫秒级；在 gain_extraction 里 CSV 不是主要瓶颈。

## 对后续优化的含义

优先级应该调整为：

1. **模型 evaluate Rust/compiled path。** 目标是把可静态识别的模型从 Python dict/string/object 执行迁到 indexed array / Rust loop，优先覆盖 weighted SAR、CPPLL、gain extraction、propagation delay 这些 top-wall 模型。
2. **事件模型的 timer/breakpoint/post_update。** CPPLL 中 model_breakpoint_scan 和 post_update 分别接近 9% 级别；prop_delay 里 source/model breakpoint 与 source_update 也有明显占比。
3. **checker 只作为 E2E 优化继续收尾。** weighted SAR 的 checker 是明显 E2E 长尾，但它不属于 EVAS 内核速度；需要单独记录，避免污染 simulator-only 结论。
4. **CSV 优化降级。** 在 top10 总量里 csv_write_s 只有 2.9% tran / 2.4% subprocess，除非针对特定 I/O 重任务，否则不是下一轮最大收益点。

## 口径注释

- `tran_elapsed_s` 是 EVAS transient kernel 的内部计时。
- `simulator_subprocess_wall_s` 是 EVAS 子进程从启动到结束的 wall time，包含 Python 启动、解析、仿真、CSV 输出等。
- `wall_time_s` 是 evaluator E2E wall，额外包含 fixture materialization、checker、结果验证等。
- `evaluate_s`、`prepare_step_s`、`post_update_s` 在 JSON 中是 model-level counters，不应再和 `model_evaluate_s`、`model_prepare_step_s`、`model_post_update_s` 相加，否则会 double count。
- 本轮 artifact 的 Spectre equivalence gate 是 BLOCKED，因为跳过了 Spectre/reference rerun；这不影响 EVAS 内核 profile，但不能用于 AX/Spectre 对比 claim。
