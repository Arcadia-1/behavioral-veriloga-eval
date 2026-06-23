# EVAS2 P0/P1 收口报告

日期：2026-06-06

## 一句话结论

P0/P1 的结论是：Rust EVAS2 已经可以在当前 vaBench release 271-row slice 上作为一个独立的 strict Rust 执行路径跑通，并且在 EVAS 内核口径上相对 Python EVAS fast 有明显加速；但它仍不是“全 Verilog-A 纯 Rust 仿真器”，也还不能把跨机器结果写成“快于 Spectre AX”的 paper-facing claim。

## P0：当前能 claim 什么

| 结论 | 当前证据 | 可以怎么说 |
|---|---:|---|
| Rust EVAS2 能跑完整 release slice | clean smoke 271/271 PASS；四路审计 271/271 PASS | Rust EVAS2 在当前 vaBench release 支持子集上已达到 release-row checker 全通过 |
| Rust core 比 Python fast core 快 | 四路审计中 Python fast subprocess/core 41.305s，Rust EVAS2 10.420s | 在同一本地 EVAS runner artifact 里，Rust EVAS2 core wall 相对 Python fast 约 3.96x |
| E2E 已有收益但被外层稀释 | 四路审计 E2E 98.839s -> 69.952s，约 1.41x | Rust core 收益已经可见，但 runner/CSV/checker 固定成本仍会压低用户等待时间收益 |
| checker 长尾可以被通用 runtime 消掉 | 116 hot-row smoke：checker 11.618s -> 0.221s，E2E 16.388s -> 4.349s | checker/runtime 优化对短 row 和 checker-heavy row 有直接 E2E 收益 |
| Spectre AX 对当前 checker 271/271 PASS | 四路审计中 AX 271/271 PASS | EVAS2 与 AX 在当前 checker acceptance 上对齐 |

## P0：当前不能 claim 什么

| 不能 claim | 原因 | 后续需要什么 |
|---|---|---|
| “Rust EVAS2 是完整 Verilog-A 仿真器” | Python 仍负责 parse/lower、runner、CSV、checker、部分 file side-effect replay；release PASS 不等于全语言覆盖 | Rust 拥有更多 parser/lower/runtime 外层，或者明确宣称支持子集 |
| “Rust EVAS2 比 Spectre AX 更精准” | 当前精度证据是 checker PASS，不是 waveform 数值误差排序 | 同 row、同设置、同容差的 waveform/tolerance 排名 |
| “Rust EVAS2 paper-facing 快于 Spectre AX” | 现有 Spectre 通过 thu-sui -> thu-wei，EVAS 在本地 Mac；跨机器 wall 只能诊断 | 同 host class、同 row slice、同 runner boundary、重复 cold/warm timing |
| “Spectre strict 是所有 row 的无条件 gold” | Spectre strict 在 SAR calibration FSM 4 个 form checker non-pass，而 AX PASS | 单独审计 strict 设置敏感 row 的 checker window 和仿真设置 |
| “E2E 速度完全等于 Rust 内核速度” | clean smoke 中 EVAS reported tran 只有 4.187s，但 E2E 是 225.978s | 继续收 runner/CSV/checker/harness 外层 |

## P1：当前 clean smoke

命令口径：

```bash
PYTHONPATH=runners:../EVAS python3 runners/run_vabench_release_same_server_speed.py --speed-artifact speed-optimization/reports/full_release_rows_for_fourway_20260606.json --suite all --limit 271 --evas-mode profile_fast_evas2 --skip-spectre --timeout-s 300 --jobs 1 --output-root results/evas2-p0p1-clean-smoke-20260606 --report-json speed-optimization/reports/evas2_p0p1_clean_smoke_20260606.json --report-md speed-optimization/reports/evas2_p0p1_clean_smoke_20260606.md
```

结果：

| 指标 | 数字 | 说明 |
|---|---:|---|
| selected rows | 271 | 来自 `full_release_rows_for_fourway_20260606.json` |
| simulation/checker PASS | 271/271 | 当前代码 clean runner smoke 全通过 |
| fallback notes | 0 | 没有 sparse trace fallback |
| E2E wall total | 225.978s | 未启用 persistent worker，更接近日常单 row runner 口径 |
| E2E wall median | 0.733s | 小 row 仍受 runner 固定成本影响 |
| EVAS subprocess wall total | 162.884s | 含进程启动、物料化、EVAS report 外层等 |
| EVAS reported tran total | 4.187s | EVAS 内部 transient kernel 报告口径 |
| checker wall total | 54.434s | 仍是主要 E2E 固定成本之一 |
| CSV write total | 1.976s | sparse trace 后已不是最大项 |

checker/trace policy：

| policy | rows | 说明 |
|---|---:|---|
| row-based checker | 232 | 仍走原 row-list checker |
| streaming validated checker | 38 | 走 parity-validated streaming runtime |
| custom noise checker | 1 | 随机/noise 特殊 checker |
| row-required sparse trace | 210 | 自动推断 checker 必需列 |
| streaming sparse trace | 37 | streaming checker 自带必需列 |
| no sparse contract | 24 | custom/noise 或暂未安全推断 |

这轮 clean smoke 的 E2E 比 114/115 的 persistent worker artifact 慢很多，这是预期现象：它没有复用 EVAS worker，因此包含更多 runner/进程启动固定成本。它证明的是当前代码全量可跑，不是最终速度上限。

## 当前完成度口径

如果按“EVAS2 能否作为 release 支持子集的 strict Rust 执行路径”来算，当前是 **release-row 271/271 可用**。

如果按“Python EVAS 支持行为全部迁到 Rust”来算，当前还不能写成 100%。114 的 coverage manifest 仍把 B01-B18 通用语义覆盖估计为约 **30.4%**，因为 parse/lower、runner、CSV/checker、部分 side-effect replay、随机/system task、dynamic loop/control-flow 等仍不是纯 Rust 所有。

这两个百分比回答的是不同问题：

- release 可用性：当前 benchmark release 能不能用 Rust EVAS2 跑过。
- 语言/架构 Rust 化：Python EVAS 的全部语义和外层 runtime 是否都迁进 Rust。

## 后续最短路径

| 优先级 | 工作 | 目的 |
|---|---|---|
| P0 follow-up | 单独审计 Spectre strict SAR calibration FSM 4-row non-pass | 稳定 strict-as-reference 口径 |
| P1 follow-up | 继续把 checker-heavy row 迁到 `CsvCheckerRuntime` | 降低 E2E 长尾 |
| P1 follow-up | persistent worker / runner boundary 固化成标准 benchmark 口径 | 避免 clean smoke 与 persistent artifact 被混读 |
| P2 | Rust file handle / format runtime | 去掉 Python side-effect replay 边界 |
| P2 | Rust-owned parse/lower/runner 原型 | 评估是否值得把 E2E 外层继续 Rust 化 |
| P2 | 同 host class Spectre AX/strict repeated timing | 才能形成 paper-facing Spectre speed claim |
