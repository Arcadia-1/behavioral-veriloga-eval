# 114 - Full Release Rust/Python/Spectre Four-Way Audit

日期：2026-06-06

## 本轮目标

本轮把 Rust EVAS2 和 Python EVAS 的剩余 release-row 差异先对齐，然后跑完整 release slice 的四路对比：

- Rust EVAS2：`profile_fast_evas2`
- Python EVAS fast：`profile_fast_skip_source_error_control`
- Python EVAS strict：`strict_current`
- Spectre AX：`ax_speed`
- Spectre strict：`reference_strict_primary`

这里的目标是工程审计，不是直接生成 paper-facing speed claim。EVAS 在本地 Mac 跑，Spectre 通过 `thu-sui -> thu-wei` 跑，跨机器 wall ratio 只能当诊断数字。

## 本轮对齐的差异

| 差异点 | 原来现象 | 本轮处理 | 验证 |
| --- | --- | --- | --- |
| `$fopen/$fwrite/$fdisplay/$fstrobe/$fclose` | Rust EVAS2 旧报告中 file metric 相关行失败，典型表现是 `metric.out` 不生成或 checker 找不到 side output | 新增 RustSimProgram side-effect IR。Rust 拥有事件时序和 side-effect event 产生，Python replay 负责实际字符串/文件系统写入 | targeted file-output rows PASS；full release EVAS2 271/271 PASS |
| string parameter + numeric parameter coexist | 模型有 string parameter 时 `_model_params()` 会把整个参数表丢成空，导致 numeric 参数如 `tr` 缺失 | 跳过非数值参数，但保留原始 local slot index，不破坏 Rust ABI 参数编号 | file-output direct RustBackend smoke PASS |
| file-open spec id remap | `BODY_STMT_FILE_OPEN` 的 `expr_start` 被普通 body encoder 当成 expression offset 覆盖，导致 Rust log 出错误 spec id | 对 file-open statement 特判，保留 side-effect spec id，只重映射目标 state handle | event log 中 open/write 顺序正确，生成 `metric.out` |
| side output validation path | runner/checker 只看部分路径，Rust replay 输出位置和 checker 期望可能不一致 | `simulate_evas.py` 设置 `EVAS_SIDE_EFFECT_OUTPUT_DIR`，validator 同时检查 run dir 和 csv parent | `vbr1_l1_crossing_metric_writer` 与 `vbr1_l2_measurement_flow` targeted rerun PASS |

这不是 Python 仿真 fallback：时间推进、event firing、transition/source/record 主循环仍由 Rust EVAS2 的 fastpath 执行；Python replay 只是目前的文件系统 side-effect 边界。若以后要做纯 Rust runner，这个 replay 层需要继续迁入 Rust 文件 runtime。

## 全量结果

测试范围：`271` 个 release selected rows。机器可读汇总：

```text
speed-optimization/reports/full_release_fourway_rust_py_spectre_summary_20260606.json
```

原始报告：

```text
speed-optimization/reports/full_release_evas_py_rust_after_fixes_20260606.json
speed-optimization/reports/full_release_evas2_sidefx_persist_20260606.json
speed-optimization/reports/full_release_spectre_ax_strict_20260606.json
speed-optimization/reports/current_release_rust_coverage_manifest_20260606_after_sidefx.json
```

| 引擎 / 模式 | 运行位置 | 仿真完成 | checker 通过 | E2E wall 总和 | E2E 中位 | subprocess/core 总和 | checker 总和 | 备注 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Python EVAS strict `strict_current` | local Mac | 271/271 | 271/271 | 597.444s | 0.529s | 541.313s | 51.804s | Python EVAS 精度参考口径 |
| Python EVAS fast `profile_fast_skip_source_error_control` | local Mac | 271/271 | 271/271 | 98.839s | 0.177s | 41.305s | 54.073s | 当前 Python fast 对照 |
| Rust EVAS2 `profile_fast_evas2` | local Mac | 271/271 | 271/271 | 69.952s | 0.178s | 10.420s | 54.244s | 本轮修复后 persistent worker 口径 |
| Spectre AX `ax_speed` | `thu-wei` via `thu-sui` | 271/271 | 271/271 | 2240.311s | 8.418s | 914.007s | 21.153s | 诊断性跨机器数字 |
| Spectre strict `reference_strict_primary` | `thu-wei` via `thu-sui` | 271/271 | 267/271 | 2646.507s | 9.579s | 1281.346s | 57.946s | SAR calibration FSM 4 个 form checker non-pass |

速度比：

| 对比 | E2E wall 总和 | subprocess/core 总和 | 解释 |
| --- | ---: | ---: | --- |
| Python EVAS fast / Rust EVAS2 | 1.41x | 3.96x | Rust 内核明显更快，但 E2E 被 checker/harness 固定成本稀释 |
| Python EVAS strict / Rust EVAS2 | 8.54x | 51.95x | strict Python EVAS 保留更多检查和步进开销 |
| Spectre AX / Rust EVAS2 | 32.03x | 87.71x | 仅为跨机器诊断，不是 paper-facing same-host claim |
| Spectre strict / Rust EVAS2 | 37.83x | 122.96x | 同上 |
| Spectre strict / Spectre AX | 1.18x | 1.40x | strict 设置更保守，subprocess 差异更明显 |

逐行观察：

- Rust EVAS2 对 Python fast 的 E2E 中位 speedup 只有 `1.03x`，且 `128/271` 行 E2E 更慢。
- Rust EVAS2 对 Python fast 的 subprocess 中位 speedup 是 `1.66x`，总 subprocess speedup 是 `3.96x`，但仍有 `51/271` 行 subprocess 更慢。
- 最大收益来自 propagation delay、pipeline ADC、SAR、CPPLL、gain measurement 这类原先 Python 内核热路径明显的行。
- 小行和 checker-heavy 行会把 Rust 核心收益吞掉；这类行需要继续减少 Python runner/checker/CSV 固定成本，而不是只看内核。

## Rust EVAS2 命中情况

本轮 full release 中：

| counter | 结果 | 说明 |
| --- | ---: | --- |
| `rust_full_model_fastpath_enabled` | 271 rows | 全部 release rows 命中 Rust full-model fastpath |
| `rust_sim_program_enabled` | 269 rows | 大部分行由通用 RustSimProgram 执行 |
| CPPLL specialized whole-model fastpath | 2 rows | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` 的 e2e/tb 走 CPPLL 专用 Rust fastpath |
| `rust_sim_program_side_effects` | 12 events / 5 rows | file-output side-effect 已进入 Rust event log + Python replay 边界 |

这说明本轮 Rust EVAS2 的速度收益不是“每步 Python 调 Rust 小函数”的旧负优化路线，而是 full-model / RustSimProgram 级别的大块执行。

## 精度和 claim 边界

当前“精度一致”的证据是 checker acceptance：

- Rust EVAS2：271/271 checker PASS
- Python EVAS fast：271/271 checker PASS
- Python EVAS strict：271/271 checker PASS
- Spectre AX：271/271 checker PASS
- Spectre strict：267/271 checker PASS，4 个 non-pass 都来自 `vbr1_l1_successive_approximation_calibration_search_fsm`

所以现在可以说：

- Rust EVAS2 已经修复本轮发现的 file side-effect release-row 差异。
- Rust EVAS2 在当前 271-row release slice 上达到和 Python EVAS fast / Spectre AX 相同的 checker pass 覆盖。
- Rust EVAS2 在本地 EVAS 内部对比中，subprocess/core 总耗时相对 Python EVAS fast 降低到 `10.420s / 41.305s`，即约 `3.96x` core speedup。

不能说：

- 不能说 Rust EVAS2 比 Spectre AX 数值更精准。当前证据是 checker 层通过，不是 waveform 数值误差排序。
- 不能说 Rust EVAS2 已经全量替代 Python EVAS 的所有 Verilog-A 语义。当前 release slice PASS，不等于全语言 coverage。
- 不能把跨机器 Spectre/EVAS wall ratio 当 paper-facing speed claim。paper claim 需要同 host class、同 runner boundary、同 row slice。
- 不能把 Spectre strict 当作所有 row 的无条件 gold behavior。当前 strict 在 SAR calibration FSM 上出现 4 个 checker non-pass，需要单独审计设置/检查器窗口。

## Spectre strict 的 4 个 non-pass

4 个 non-pass 都是同一个 entry 的四个 form：

```text
vbr1_l1_successive_approximation_calibration_search_fsm/{bugfix,dut,e2e,tb}
```

现象：

- Spectre strict 仿真进程全部 0 error 完成。
- checker 失败原因都是 `sar_cal_too_few_active_steps=3`。
- 同一批 row 在 Spectre AX 下 PASS，notes 为 `direction=4/4; sar_step_first_last=0.180/0.022`。
- AX 与 strict 都使用 `maxstep=0.5n`，但 strict 增加了 `errpreset=conservative` 和显式 `reltol/vabstol/iabstol/gmin`，AX 使用 `+preset=ax +mt`，没有同一组显式 tolerance。

这说明该 row 对 Spectre 设置敏感。后续要么调整 checker 判定窗口，使 strict/AX 的合理数值差异都能通过；要么把该 row 从 strict-as-reference speed/accuracy gate 中单独标记为 settings-sensitive。

## Rust EVAS2 仍有缺陷

| 缺陷 | 当前状态 | 为什么重要 | 下一步 |
| --- | --- | --- | --- |
| 不是纯 Rust E2E | Python 仍负责 parse/lower、runner、CSV、checker、部分 side-effect replay | E2E wall 中 checker/harness 仍占主导，小行收益被吞 | 把 sparse record/CSV/checker runtime 继续 array 化，或做 Rust runner |
| B01-B18 通用语义覆盖仍是工程估计 `30.4%` | coverage manifest 显示很多行为还是 `partial/shadow/python_only` | release slice PASS 不能外推到所有 Python EVAS 支持语义 | 继续按 B01-B18 行为表补 production Rust，不按 task-name 特判 |
| file/string side effect 还不是纯 Rust runtime | Rust 生成 side-effect event，Python replay 写文件 | 已解决当前 release 功能，但纯 Rust EVAS2 还缺文件句柄/格式化 runtime | 实现 Rust file handle table 与 format string executor |
| random/system task 语义未完全对齐 | `$rdist_normal` 等仍需要明确 seed、分布、与 Spectre/Python 容差关系 | 随机行为会影响 reproducibility 和 checker 容差 | 定义 deterministic RNG contract，并做 Python/Spectre tolerance audit |
| dynamic loop / dynamic control flow 仍有限 | 受限 static loop/case/if 已覆盖，dynamic `while` 等不能无条件迁 | 不证明终止会让 Rust scheduler 风险变高 | 为常见 phase-wrap 类循环做 bounded primitive，其余继续显式 reject |
| full release speed 仍受 E2E 外层影响 | Rust core 3.96x 快，但 E2E 只有 1.41x | 用户实际等待时间没有按 core 同比例下降 | 优先优化 checker/CSV/runner 固定成本，尤其 short rows |
| Spectre strict gate 有 settings-sensitive row | SAR calibration FSM strict checker 4/4 non-pass | 影响 strict-as-reference 的口径 | 单独审计该 row 的 checker 与 Spectre setting sensitivity |

## 验证记录

| 检查 | 结果 |
| --- | --- |
| `cargo test` in `EVAS/evas/rust_core` | `37 passed` |
| targeted pytest for file side-effect | `4 passed, 270 deselected` |
| direct RustBackend file side-effect smoke | event log open/write 正确，`metric.out` 生成 |
| targeted `vbr1_l1_crossing_metric_writer` EVAS2 rerun | PASS |
| targeted `vbr1_l2_measurement_flow` EVAS2 rerun | PASS |
| full release EVAS2 nonpersistent rerun | 271/271 PASS |
| full release EVAS2 persistent rerun | 271/271 PASS |
| full release Spectre AX/strict rerun | AX 271/271 checker PASS；strict 267/271 checker PASS |
| release Rust coverage manifest after side-effect fix | 357 model rows compile PASS；Rustification estimate `30.4%` |

## 后续建议

1. 先审计 `vbr1_l1_successive_approximation_calibration_search_fsm` 的 Spectre strict non-pass，确认是 checker window 过窄、Spectre setting sensitivity，还是 testbench 本身对 conservative 设置敏感。
2. 对 Rust EVAS2 不再优先堆新特殊 fastpath，主线继续做 B01-B18 的 production Rust 语义闭环。
3. 为 E2E wall 做第二阶段优化：sparse record、CSV、checker runtime、runner 固定成本。否则短 row 的 Rust core speedup 很难体现在总时间上。
4. 如果要 paper-facing claim 快于 Spectre AX，需要补一次同 host class 的 same-slice timing；当前 `thu-wei` Spectre vs local Mac EVAS 只能作为诊断。
