# vaEVAS Same-Server Speed Goal Findings

日期：2026-05-22

## 结论摘要

本轮 goal 实验已经证明：在 thu-sui 同一台服务器、8 workers、EVAS/Spectre 共同跑完整 259-row vaBench release speed slice 的条件下，`profile_fast_skip_source_error_control` 相比 Spectre 有明确速度优势，并且没有牺牲当前 accuracy gate。

正式主表采用 R1、R2、R4、R5 四个 clean full repeats；R3 因 behavior checker watchdog 误判单行失败，被单独作为诊断证据，不并入主表。

| 对比 | Accuracy-gated rows | Geomean speedup | Median speedup | P10 | P90 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Spectre AX / EVAS fast+skip | 1036 | 6.958x | 7.803x | 3.225x | 16.81x |
| Spectre classic / EVAS fast+skip | 1036 | 21.63x | 26.07x | 12.09x | 50.66x |
| Spectre AX / EVAS strict | 1036 | 4.276x | 5.632x | 1.177x | 14.46x |
| Spectre classic / EVAS strict | 1036 | 13.29x | 17.10x | 4.656x | 37.91x |

核心判断：

- EVAS 确实有发展潜力：不需要 Spectre 的通用电路求解流程，在大量纯 voltage-domain behavioral / event-driven case 上有显著速度收益。
- 当前 fast+skip 不是靠放弃精度换速度：正式主表 1036/1036 EVAS fast+skip rows accuracy-gated PASS。
- EVAS 仍有明确短板：PFD small-phase、CPPLL tracking、gain estimator 这类密集边沿、强步长约束、`cross()` / `transition()` / reset race 任务会让 EVAS 慢于 Spectre AX。
- 共享服务器负载会显著影响 wall time；因此论文中应报告 repeat 分布和 accuracy-gated speedup，不应只报告单次最好结果。

## 实验资产

主要报告：

- `same_server_speed_goal_summary_final_20260522.md/json`：正式主表，包含 R1、R2、R4、R5。
- `same_server_speed_goal_summary_all_r1_r5_with_r3_watchdog_20260522.md/json`：包含 R1-R5，保留 R3 watchdog 误判记录。
- `same_server_speed_ablation_goal_summary_20260522.md/json`：E1 full ablation。
- `same_server_speed_targeted_deadband_watchdog_fix_20260522.md/json`：R3 误判单行 targeted rerun。

新增/修复的脚本：

- `runners/report_vabench_release_same_server_speed_goal.py`：汇总 repeated timing、accuracy gate、tolerance sweep、outlier。
- `runners/simulate_evas.py`：小 CSV behavior checker 改为优先直接执行，避免 multiprocessing watchdog 对快速 checker 的假 timeout。

## E0-E2 执行结果

### E0 Preflight

远端 fixture audit：

- rows = 259
- fail = 0
- 说明：所有 speed slice fixture 均可物化。

### E1 Full Ablation

E1 跑了 259 rows x 7 backend/mode jobs = 1813 jobs，用于判断不同 EVAS 模式的相对趋势。

| Mode | Geomean wall time |
| --- | ---: |
| EVAS strict_current | 1.770s |
| EVAS profile_balanced | 1.591s |
| EVAS profile_fast | 1.223s |
| EVAS skip_source_error_control | 1.043s |
| EVAS profile_fast_skip_source_error_control | 0.968s |

结论：`profile_fast` 和 `skip_source_error_control` 都有贡献，组合后最快。E1 仅作为 ablation evidence；速度 headline 使用 R1/R2/R4/R5 repeated timing。

### E2 Repeated Timing

正式主表使用四个 clean repeats：

| Repeat | fast+skip gate | AX / fast+skip geomean | classic / fast+skip geomean |
| --- | ---: | ---: | ---: |
| R1 | 259/259 | 5.928x | 18.38x |
| R2 | 259/259 | 5.860x | 18.34x |
| R4 | 259/259 | 7.670x | 23.85x |
| R5 | 259/259 | 8.795x | 27.22x |

R4/R5 的 speedup 偏高，主要因为共享服务器负载下 Spectre wall time 拉长，同时部分 EVAS 慢类也拉长。因此最稳妥的表述是：在当前 8-worker same-server 设置下，fast+skip 对 Spectre AX 的 repeated geomean speedup 约 5.86x-8.80x，对 Spectre classic 约 18.34x-27.22x；combined geomean 为 6.958x / 21.63x。

## R3 Watchdog 误判

R3 原始 full repeat 中只有一个 non-PASS：

- case：`vbr1_l1_calibration_deadband_controller/tb`
- mode：EVAS `profile_fast_skip_source_error_control`
- raw status：`FAIL_SIM_CORRECTNESS`
- notes：`behavior_eval_timeout>60s`

诊断结果：

- EVAS waveform 与 strict EVAS/Spectre parity 通过。
- 同一 CSV 上直接执行 behavior checker 用时约 0.10s，结果 PASS。
- targeted full rerun 后四个 backend/mode 全部 PASS。

修复：

- 对小 CSV 增加 direct behavior checker path，避免 watchdog/multiprocessing 假 timeout。
- R4、R5 patched full repeats 中该类问题未复发。

## Accuracy / Tolerance Gate

正式主表中：

- fast+skip accuracy gate：1036/1036 PASS。
- strict EVAS accuracy gate：1036/1036 PASS。
- 无 non-PASS rows。

Tolerance sweep 使用保存的 waveform parity metrics 后处理，不重新仿真。对 `profile_fast_skip_source_error_control`：

| Target | Waveform rows | Current PASS | P95<=0.05 & Max<=0.10 | P95<=0.10 & Max<=0.15 | Current core P95<=0.14 & Max<=0.22 |
| --- | ---: | ---: | ---: | ---: | ---: |
| strict EVAS parity | 1004 | 1004 | 988 | 1004 | 1004 |
| Spectre AX parity | 1004 | 1004 | 972 | 988 | 1004 |
| Spectre classic parity | 1004 | 1004 | 976 | 976 | 1004 |

解释：

- 当前门控下全部通过。
- 即使用更严格的 `P95<=0.10, Max<=0.15`，Spectre AX 仍保留 988/1004 waveform rows。
- task-specific semantic comparators 不是 NRMSE waveform gate，因此作为 non-waveform rows 另计，不参与该阈值扫描。

## 为什么 EVAS 会快

EVAS 快的主要来源不是“服务器更强”，而是计算路径更短：

1. EVAS 面向当前 benchmark 支持的 pure voltage-domain behavioral subset，不需要通用 KCL/KVL/牛顿迭代。
2. `profile_fast` 降低保守误差控制和动态步长成本。
3. `skip_source_error_control` 跳过 source-side error control，减少对行为源的反复误差检查。
4. 对简单 event/digital/decoder/DAC/detector case，EVAS 往往 0.5-1.0s 完成；Spectre AX 即使步数不多，也有 netlist、AHDL、PSF、license、进程启动和输出开销。

典型快例：

- `debounce_latch/bugfix`、`binary_weighted_voltage_dac/e2e`、`thermometer_code_decoder/*` 等，EVAS fast+skip 约 0.5-0.8s，Spectre AX 在高负载 repeat 中可到 18-23s。

## 为什么 EVAS 会慢

EVAS 慢的 case 不是因为精度 gate 失败，而是时间推进成本高：

1. PFD / PLL / reset-race 类任务包含密集边沿、20ps transition、`maxstep=5p/10p`、`errpreset=conservative`。
2. EVAS 必须在 `cross()`、`transition()`、timer 和 reset/race 附近插入/细化步点，跳不过这些事件语义。
3. Spectre AX 对这类 case 的 event/transition 处理和编译执行高度优化，有时接受步数远低于 EVAS。
4. EVAS 当前 profile 仍保留 correctness-priority 的 event breakpoint，不会为了速度跳过关键边沿。

典型慢例：

| Case | EVAS fast+skip | Spectre AX | EVAS steps | Spectre AX steps |
| --- | ---: | ---: | ---: | ---: |
| `pfd_small_phase_response/bugfix` in R5 | 103.3s | 4.284s | 60058 | 435 |
| `pfd_small_phase_response/tb` in R4 | 98.87s | 4.437s | 60058 | 435 |
| `cppll_freq_step_reacquire/e2e` in R5 | 96.53s | 7.641s | 41900 | 34050 |

这说明下一步优化不应继续盲目放松精度，而应针对 event scheduling、breakpoint coalescing、transition-local step policy、dense-edge batching 做专项优化。

## Warm-cache 状态

本轮没有单独报告 warm-cache speedup。原因是当前 runner 每个 case 会重新 staging/run：

- EVAS：`stage_selected_mode_task()` 清理 mode staging dir。
- Spectre：`copy_gold_to_run_dir()` 清理 run dir。

因此直接复用同一 output root 不能代表真实 warm-cache；需要新增显式 `--reuse-run-dir` / `--no-clean-stage` 或单独的 warm runner，才能把 AHDL 编译缓存、PSF 输出、fixture staging 和 waveform parsing 的影响隔离出来。

当前可报告的是 repeated cold-like same-server timing，而不是 warm-cache timing。

## Paper-facing 建议表述

建议主 claim：

> On the 259-row vaBench release speed slice, under an 8-worker same-server setup and accuracy-gated EVAS/Spectre parity, EVAS `profile_fast_skip_source_error_control` achieves a combined geomean speedup of 6.96x over Spectre AX and 21.63x over Spectre classic across four clean repeats, while preserving 1036/1036 accuracy-gated passes.

建议同时写限制：

> Speedups are workload-dependent. Dense-edge PFD/PLL cases with tight maxstep and transition/cross breakpoints remain slower than Spectre AX, indicating that future EVAS work should target event scheduling and breakpoint handling rather than further relaxing accuracy gates.

## 下一步优化计划

优先级：

1. 增加 warm-cache runner，明确区分 cold start、AHDL cache、PSF parsing、CSV checker 成本。
2. 对 PFD/PLL 慢例做 micro-benchmark：固定 waveform 输出，单独测 event scheduling、transition breakpoint、checker、CSV 写入。
3. 增加 event-density 指标：`accepted_tran_steps`、`cross_fires`、`transition` 次数、timer 次数、每步耗时。
4. 尝试 correctness-preserving optimizations：
   - 合并同一时间窗口内的 breakpoint。
   - 对 `transition()` 附近使用局部策略，而不是全局拖小步长。
   - 对已知 digital rail signal 使用 event-grid sampling，减少连续插值开销。
   - 将输出/CSV/checker 从仿真 wall time 中分离统计。
5. 论文表格采用 accuracy-gated repeated timing；附录列出慢例和负载波动，避免过度 claim。
