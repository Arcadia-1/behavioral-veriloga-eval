# Rust EVAS2 Four-Way Freeze Risk Audit, 2026-06-08

## 结论先行

当前最可信的结论是：

- 在 271 个 four-way common rows 上，EVAS1.0 Python strict、Rust EVAS2、Spectre AX、Spectre strict 都能通过行为 checker。
- 以 Spectre strict 作为参考时，Rust EVAS2 和 Spectre AX 都通过当前 waveform equivalence gate，`Needs review = 0`，`Blocked = 0`。
- Rust EVAS2 的 aggregate E2E 和 subprocess wall 都快于 Spectre AX，但该 artifact 仍是工程参考，不是最终 paper-facing same-host speed claim。
- 不能 claim Rust EVAS2 比 Spectre AX 更精准；当前指标支持的是“同一容差 gate 下等价”，不是“严格精度排序胜出”。

主报告：

- `speed-optimization/reports/full_release_fourway_reference_after_cmp_delay_cross_time_fix_20260608.md`
- `speed-optimization/reports/full_release_fourway_reference_after_cmp_delay_cross_time_fix_20260608.json`

## 当前四方结果

### 速度

| Simulator | Rows | Behavior PASS | E2E total s | Subprocess total s | vs Spectre AX E2E | vs Spectre AX subprocess |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS1.0 Python strict | 271 | 271 | 597.444 | 541.313 | 3.75x | 1.69x |
| Rust EVAS2 | 271 | 271 | 71.239 | 11.716 | 31.45x | 78.01x |
| Spectre AX | 271 | 271 | 2240.311 | 914.007 | 1.00x | 1.00x |
| Spectre strict | 271 | 271 | 2646.507 | 1281.346 | 0.85x | 0.71x |

解释：

- `E2E total s` 包含 fixture/staging、simulator subprocess、CSV/PSF 解析、checker、外层 runner 开销。
- `Subprocess total s` 是 runner 记录的 simulator subprocess 边界，不等价于纯内核时间。
- Rust EVAS2 的 E2E 里 checker 占比已经很高，说明内核加速后外层 checker/harness 成为显著部分。

### 精度

| Candidate | Reference usable | Candidate PASS | Compared | Equivalent | Needs review | Blocked | Worst abs saved units | Worst effective mean rel RMS | Worst effective signal rel RMS | Worst raw mean rel RMS | Worst raw signal rel RMS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS1.0 Python strict | 271 | 271 | 271 | 271 | 0 | 0 | 1.000000 | 0.015833 | 0.147936 | 0.079693 | 0.147936 |
| Rust EVAS2 | 271 | 271 | 271 | 271 | 0 | 0 | 1.000000 | 0.015833 | 0.031667 | 0.079693 | 0.127719 |
| Spectre AX | 271 | 271 | 271 | 271 | 0 | 0 | 1.000000 | 0.006205 | 0.019167 | 0.072521 | 0.122542 |

解释：

- `effective` 指经过当前 waveform equivalence policy 的边沿窗口处理后，用于判断仿真器等价的指标。
- `raw` 指原始逐点误差，主要用于诊断，不直接等价于功能失败。
- `Worst abs saved units` 不叫电压，因为保存列里包含 `delay_ps` 等测量列。

## 已修复的误差

`vbr1_l1_propagation_delay_comparator` 的 `delay_ps` 测量列问题已经修复。

修复前：

- Rust EVAS2 vs Spectre strict: `max_abs_saved_units = 37.3812`
- Rust EVAS2 effective signal rel RMS: `0.0813156`

修复后：

- Rust EVAS2 vs Spectre strict: `max_abs_saved_units = 0.00105038`
- Rust EVAS2 effective signal rel RMS: `9.80241e-07`

四个 forms `bugfix/dut/e2e/tb` 均 PASS。

局部修复报告：

- `speed-optimization/reports/cmp_delay_cross_time_fix_evas2_allforms_20260608_r2.md`
- `speed-optimization/reports/cmp_delay_cross_time_fix_evas2_allforms_20260608_r2.json`

## After-Fix 剩余误差排序

下面是重新用四方 source artifact 加上 propagation-delay overlay 后，对 Rust EVAS2 vs Spectre strict 的 top residual 排序。

| 排名依据 | Top row/form | 指标值 | 状态 | 当前解释 |
| --- | --- | ---: | --- | --- |
| max abs saved units | `vbr1_l1_ramp_or_step_source` / `dut,e2e,tb` | 1.000000 | passed | 数字/状态类边沿采样错位；不是整段逻辑错误。 |
| effective mean rel RMS | `vbr1_l1_ramp_or_step_source` / `dut,e2e,tb` | 0.015833 | passed | `transition()` 与 analog threshold/grid 口径差异。 |
| effective signal rel RMS | `vbr1_l1_ramp_or_step_source` / `dut,e2e,tb` | 0.031667 | passed | 单信号边沿窗口附近差异放大。 |
| raw mean rel RMS | `vbr1_l1_ramp_or_step_source` / `dut,e2e,tb` | 0.079693 | passed | raw 点对点指标被局部边沿错位主导。 |
| raw signal rel RMS | `vbr1_l1_ramp_or_step_source` / `dut,e2e,tb` | 0.127719 | passed | raw 单信号边沿错位；effective gate 已折扣。 |

Rust EVAS2 后续 top rows：

| Row/form | max abs | effective mean rel RMS | effective signal rel RMS | raw signal rel RMS | 当前归因 |
| --- | ---: | ---: | ---: | ---: | --- |
| `vbr1_l1_programmable_gain_amplifier` / all forms | 0.085263 | 0.001876 | 0.011259 | 0.011259 | 连续 `bounded`/clipping 目标进入 `transition()` 后的幅值/边沿形状差异。 |
| `vbr1_l2_amplifier_filter_chain` / `e2e,tb` | 0.072434 | 0.003060 | 0.007064 | 0.011430 | 滤波/settling 链路的连续数值积分与时间网格差异。 |
| `vbr1_l2_complete_calibration_loop` / `e2e,tb` | 0.031618 | 0.004024 | 0.008889 | 0.016870 | 校准状态/settling 过程中的小幅连续残差。 |
| `vbr1_l2_agc_receiver_leveling_loop` / `e2e,tb` | 0.069390 | 0.002654 | 0.005733 | 0.018880 | 增益控制状态和 transition 输出的连续时间网格差异。 |
| `vbr1_l2_reference_startup_enable_flow` / `e2e,tb` | 0.063720 | 0.000797 | 0.005777 | 0.033187 | raw error 主要来自 startup/metric 边沿窗口，稳定区误差较小。 |
| `vbr1_l1_peak_detector` / common forms | 0.009758 | 0.000166 | 0.000497 | 0.031514 | raw error 由 `vout` 局部边沿窗口主导，effective residual 很小。 |
| `vbr1_l2_ldo_load_step_recovery_flow` / `e2e,tb` | 0.011050 | 0.000554 | 0.002177 | 0.038263 | `out/ctrl_mon/metric` 的局部恢复边沿和连续状态差异。 |

## 剩余误差原因

### 1. 边沿采样与 transition 网格差异

这类是当前最大残差来源。模型里经常有：

- ordinary analog `if (V(x) > vth)`
- `transition(target, delay, rise, fall)`
- `cross()`/`above()`/timer 与 transition 输出组合

Rust EVAS2 更偏向按照事件、PWL 源和 typed transition state 直接推进；Spectre strict 会受 adaptive step、breakpoint、solver 网格影响。两者在稳定区往往一致，但在跳变附近可能差一个或几个采样点。

这不是简单的“谁错了”。如果模型没有显式用 `cross()` 锁定阈值事件，而是在连续表达式里直接写 `V(x) > vth`，那么不同仿真器观察阈值变化的时间网格本来就可能不同。

### 2. 连续模拟量的数值积分/滤波残差

`amplifier_filter_chain`、`complete_calibration_loop`、`AGC`、`LDO` 这类 row 有连续状态、滤波、settling 或控制回路。EVAS 是电压域事件驱动 behavioral evaluator，不是 Spectre 那样的连续方程求解器，所以会出现小幅 amplitude/phase residual。

当前这些 residual 都通过 gate，但它们说明不能把 EVAS2 表述成“与 Spectre strict 波形逐点完全一致”。

### 3. 数字/测量列的 raw 指标放大

数字列或 metric 列在单个边沿错位时，`max_abs` 可能直接显示 `1.0`。这通常表示局部采样点一个是 0、另一个是 1，而不是整个逻辑功能错误。

因此报告中需要同时看：

- behavior checker 是否 PASS
- effective waveform gate 是否 PASS
- raw metric 是否只是局部 edge-window high error
- 稳定区 mismatch 是否持续存在

### 4. Spectre strict 不是数学真值

Spectre strict 是当前参考仿真器，但不是数学上的唯一真值。Spectre AX、Spectre strict 和 EVAS2 对 transition/cross 的处理都可能有不同插值和断点策略。

因此当前口径应该是：

- Spectre strict 是 reference condition。
- EVAS2 和 AX 都需要通过 strict-referenced equivalence gate。
- 不把 strict/AX/EVAS2 的局部边沿点差异解释成绝对精度排名。

## 风险清单

| 风险 | 当前状态 | 影响 | 处理方式 |
| --- | --- | --- | --- |
| 把工程参考误写成 paper-facing speed claim | 主报告已标为 `Paper-facing boundary: False` | 可能过度 claim | 最终论文速度表必须使用 same-slice same-host/approved-bridge protocol。 |
| claim “Rust EVAS2 比 AX 更精准” | 当前 gate 明确禁止 | AX 在 worst effective RMS 上更小 | 只 claim 等价，不 claim 更精准。 |
| claim “Rust EVAS2 每行都比 AX 快” | 主报告明确禁止 | 局部 row 可能被 checker/harness 主导 | 只 claim aggregate speedup，并保留 per-row 分布。 |
| checker/harness 主导 E2E | Rust EVAS2 checker 占 E2E 约 76.1% | 后续内核加速不一定等比例反映到 E2E | 同时报告 E2E、subprocess、component breakdown。 |
| after-fix 报告是旧 full + 新 overlay | 当前 propagation-delay 修复以 overlay 进入四方表 | 适合工程冻结，最终 claim 仍需 full rerun | 若 EVAS/Spectre 配置或代码再变，触发 full rerun。 |
| RustSimProgram 仍有 2 个 runtime rejection rows | Rust full-model enabled 271/271，但 RustSimProgram enabled 269/271 | 不能说所有内部 IR path 100% 同构 | 可以说 full-model Rust fastpath 无 fallback；不能说所有低层 RustSimProgram 子路径都无 rejection。 |
| Verilog-A 全语言覆盖 | 当前只覆盖 voltage-domain/event-driven behavioral subset | release 外模型可能不支持 | 报告中必须写 supported subset。 |
| event ordering 组合边界 | 同时 timer/cross/transition/breakpoint 的极端 equal-time 排序仍需回归守住 | 可能只在复杂组合模型暴露 | 保留 atomic regression，不用特例修 row。 |

## 推荐汇报口径

可以说：

> 在当前 vaBench release four-way common slice 上，Rust EVAS2 对 271/271 rows 均通过行为 checker，并且相对 Spectre strict 通过 waveform equivalence gate。当前工程参考显示 Rust EVAS2 在 aggregate E2E 和 subprocess wall 上快于 Spectre AX。剩余差异主要来自边沿采样、transition/event 调度以及连续状态数值网格差异，均在当前仿真器等价容差内。

不要说：

> Rust EVAS2 没有误差。

不要说：

> Rust EVAS2 比 Spectre AX 更精准。

不要说：

> Rust EVAS2 是全 Verilog-A 语义覆盖的纯 Rust 仿真器。

## 下一步

1. 如果要写 paper-facing speed claim：固定 commit、固定 runner、固定 Spectre AX/strict 设置，通过 thu-sui 跳板到 thu-wei 或其他批准环境做 same-slice full rerun。
2. 如果要继续压低误差：优先研究 `ramp_or_step_source`、thresholded DAC/PGA、AGC/filter/settling 这三类 transition-grid residual，而不是再追已经修掉的 propagation-delay。
3. 如果要继续压 E2E：checker runtime、sparse record、CSV/trace 仍比内核更可能影响 Rust EVAS2 的总墙钟。
4. 如果要提升 coverage claim：把 Rust full-model enabled、RustSimProgram enabled、rejection rows、supported Verilog-A subset 放在同一张 coverage 表里，避免“Rust 全覆盖”歧义。
