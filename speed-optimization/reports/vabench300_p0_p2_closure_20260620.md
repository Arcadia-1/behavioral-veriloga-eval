# vaBench 300 P0-P2 收敛报告

日期：2026-06-20

## 一句话结论

P0-P2 已完成到可审计状态：修复后的 fresh full-300 双仿真结果为 300/300 PASS，0 个 FAIL_PARITY，0 个 FAIL_EVAS，0 个 FAIL_INFRA。

主结果文件：

- full summary: `results/vabench-300-dual-full-postfix-pr12-20260620/summary.json`
- compact audit: `results/vabench-300-dual-full-postfix-pr12-20260620/audit_summary.md`
- compact audit JSON: `results/vabench-300-dual-full-postfix-pr12-20260620/audit_summary.json`

## 实验口径

- row slice：`benchmark-vabench-release-v1/vabench-300-expansion/VABENCH_300_MANIFEST.json`
- selection：`--include-pending`，共 300 rows
- row composition：271 个 `existing_certified_v1`，29 个 `proposed_v1.1_pending_certification`
- form composition：62 bugfix，66 dut，86 tb，86 e2e
- EVAS：`VAEVAS_DEFAULT_EVAS_ENGINE=evas-rust`
- EVAS source：通过 `VAEVAS_EVAS_REPO=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS` 显式指定，避免 clean worktree 误用旧 EVAS
- EVAS commit：依赖 [EVAS PR #12](https://github.com/Arcadia-1/EVAS/pull/12)，本地实测 commit 为 `e1e73c0`（`codex/stochastic-semantics-and-cross-law` / local `main`），不是 upstream EVAS `main` 的 `28c9100`
- Spectre：`--spectre-backend sui-direct`，summary 记录 `sui_host=thu-wei`

注意：本报告中的速度数字是当前 runner 边界下的工程 E2E wall 对比。Spectre 在 thu-wei 上运行，EVAS 使用当前本地/runner 环境调用 Rust EVAS，因此这组数字适合工程审计和瓶颈定位；最终论文级 same-server speed claim 仍应单独跑同机同负载实验。

Artifact 说明：`results/vabench-300-dual-full-postfix-pr12-20260620/summary.json` 是最终 SAR streaming checker 小增强前生成的 full-300 summary。增强后的 SAR checker 已在相关 EVAS/Spectre CSV 上做 targeted replay，仍全部 PASS；因此本报告可用于审计 P0-P2 修复，但如果要得到“当前 commit 精确对应”的 full-300 JSON，应按最后一节命令重新生成。

## P0：300-runner 与基础设施闭环

完成内容：

- 新增 `runners/run_vabench_300_dual_rerun.py`：直接读取 300 manifest，复用 release dual runner，支持 certified-only 默认选择和 `--include-pending` 全量选择。
- 新增 `runners/report_vabench_300_dual_summary.py`：把 300-run summary 压缩成 status、selection、parity、timing、slow rows。
- runner 收尾修复：显式 `--expansion-status proposed_v1.1_pending_certification` 现在无需额外指定 `--include-pending`，避免用户筛选 pending rows 时得到 0 rows；summary metadata 优先按 `task_id`/`staged_task_dir` 绑定，降低未来 manifest 扩展时 entry/form key 冲突风险。
- 修复 33 个 bugfix gold testbench 的 stale `ahdl_include`：bugfix 行应 include `dut_fixed.va`，不应 include 原始 buggy DUT 文件。
- 修复 `scripts/check_repo_layout.py` 对 Git linked worktree 的误报：worktree 的 `.git` 是文件而不是目录。

验证：

- dry-run certified-only：271 rows
- dry-run include-pending：300 rows
- bugfix include 静态检查：`missing_count 0`
- 旧 full run 中 11 个 FAIL_INFRA 行补跑后：11/11 PASS
- fresh full-300：300/300 PASS

## P1：checker/public contract 对齐

发现的问题：

旧 checker 对 4 个 L2 topic 要求了 public prompt 没要求保存的内部列，例如：

- `amplifier_filter_chain`: `preamp_mon/filt1_mon/filt2_mon/settle_metric`
- `iq_downconversion_chain`: `lo_i/lo_q/mix_i/mix_q/phase_mon`
- `reference_startup_enable`: `supply_ok/enable_mon/state_mon/startup_mon`
- `weighted_sar_adc_dac_loop`: `bit_index/trial_code_mon/trial_vdac/cmp_decision/conv_done/vin_sample`

这些列在 public prompt 中没有列为 saved observables，Spectre 和 EVAS 都不会自然输出。因此这不是 Rust EVAS 数值错误，而是 checker 与 benchmark public contract 不一致。

修复方式：

- checker 只读取 public saved observables。
- amplifier/filter 用 `metric` 和 `out` 检查 gain target、lagged settling、low/mid/high window。
- reference startup 用 `vin/out/metric` 检查 pre-enable hold、startup valid、supply dip reset、recovery。
- IQ chain 用 `out/metric` 的 I/Q window 检查正负象限和 common-mode hold。
- weighted SAR release streaming checker 回到公开信号，并增强为边沿采样判据：使用 `time/clks/rst_n/vin/vin_sh/vout/dout_0..7`，在 `clks` 上升沿后 1 ns 取样，检查 `vin_sh -> 8-bit code -> weighted DAC vout` 的量化一致性、覆盖范围和单调性。

验证：

- 旧 full run 中 8 个 FAIL_EVAS 行补跑后：8/8 PASS
- fresh full-300：0 FAIL_EVAS，0 FAIL_PARITY
- SAR targeted EVAS smoke：`vbr1_l2_weighted_sar_adc_dac_loop_tb` 使用 Rust EVAS 通过，输出 trace header 包含 `time,clks,dout_0..7,rst_n,vin,vin_sh,vout`，streaming checker 得到 497 个边沿样本、204 个 unique codes、0 个 monotonic reversal。

## P2：速度与审计表

fresh full-300 结果：

| 指标 | 数值 |
| --- | ---: |
| total rows | 300 |
| PASS | 300 |
| non-PASS | 0 |
| timed rows | 300 |
| sum EVAS wall | 188.516 s |
| sum Spectre wall | 2567.999 s |
| aggregate Spectre/EVAS speedup | 13.622x |
| median row speedup | 16.494x |
| min row speedup | 3.742x |
| max row speedup | 52.071x |

最慢 EVAS rows：

| topic | form | EVAS wall | Spectre wall | speedup |
| --- | --- | ---: | ---: | ---: |
| programmable_gain_amplifier | bugfix | 2.532 s | 9.477 s | 3.742x |
| programmable_stimulus_sequencer | e2e | 2.067 s | 9.079 s | 4.392x |
| digital_phase_accumulator_with_modulo_wrap | tb | 1.780 s | 7.095 s | 3.985x |
| programmable_gain_amplifier | dut | 1.778 s | 7.890 s | 4.436x |
| converter_front_end | tb | 1.741 s | 7.243 s | 4.160x |
| programmable_stimulus_sequencer | tb | 1.738 s | 7.376 s | 4.243x |
| bootstrapped_sample_switch | dut | 1.707 s | 10.963 s | 6.423x |
| bootstrapped_sample_switch | bugfix | 1.706 s | 10.849 s | 6.360x |
| programmable_gain_amplifier | tb | 1.691 s | 8.572 s | 5.068x |
| cppll_tracking_frequency_step_reacquire | e2e | 1.678 s | 8.839 s | 5.268x |

## 已知边界

- 速度数字是当前 runner E2E wall，不是同机论文级速度 claim。
- 29 个 proposed v1.1 rows 已在本次双仿真通过，但它们的 manifest 状态仍标为 `proposed_v1.1_pending_certification`；是否升级为 certified 需要单独更新 benchmark release 元数据。
- 这轮修的是 benchmark/checker 契约与 infra，不是 Rust EVAS 内核新优化。

## 收尾审计改进

- CLI 语义：`--include-pending` 表示默认 certified-only 选择之外额外包含 pending；如果用户已经显式给出 `--expansion-status`，则以显式筛选为准。这符合命令行工具的一般直觉：显式过滤条件优先于默认保护开关。
- Metadata 绑定：summary enrichment 不再只依赖 `(entry_id, form)`，而是优先使用 manifest 的语义 task id 和 staged task dir。这样未来如果 300 manifest 继续扩展，不容易因为 alias 或 form 重复导致结果挂错 metadata。
- SAR checker 数学口径：采样型 ADC/DAC loop 的正确评估点不是 CSV 的每一行，而是采样时钟边沿之后的稳定观测点。新的 streaming checker 只在这些点计算 `code/255*vdd`，并分别约束 `vin_sh-code_voltage`、`vout-code_voltage`、`vin_sh-vout`、code 覆盖范围和单调反转数。
- 测试固化：新增 runner pending-filter 回归测试，并更新 SAR streaming parity fixture，使 synthetic pass/fail 都按公开边沿采样关系构造。

## 验证命令

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile \
  runners/simulate_evas.py \
  runners/run_vabench_300_dual_rerun.py \
  runners/report_vabench_300_dual_summary.py \
  runners/check_streaming_checker_parity.py \
  scripts/check_repo_layout.py

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=runners \
  python3 -m pytest tests/test_vabench_function_checker_regressions.py -q

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=runners \
  python3 -m pytest tests/test_vabench_300_expansion.py -q

PYTHONPATH=runners python3 runners/check_streaming_checker_parity.py \
  --fixture-suite \
  --task sar_adc_dac_weighted_8b_smoke \
  --output-dir /private/tmp/vaevas-streaming-parity-sar

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 scripts/check_repo_layout.py

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
VAEVAS_EVAS_REPO=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS \
VAEVAS_DEFAULT_EVAS_ENGINE=evas-rust \
python3 runners/run_vabench_300_dual_rerun.py \
  --spectre-backend sui-direct \
  --include-pending \
  --workers 2 \
  --timeout-s 240 \
  --output-root results/vabench-300-dual-full-postfix-pr12-20260620
```
