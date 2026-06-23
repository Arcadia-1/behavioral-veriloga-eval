# 012 - Profile-Guided Kernel Sample

Status: `done`

Date: `2026-06-02`

Code commit: `none`

Related scratch logs:

- `/private/tmp/evas-profile-012/inverter_chain.log`
- `/private/tmp/evas-profile-012/clk_div_div8.log`
- `/private/tmp/evas-profile-012/cmp_delay.log`
- `/private/tmp/evas-profile-012/adc_ramp.log`
- `/private/tmp/evas-profile-012/noise_gen.log`

## One-Line Summary

用 5 个本地 bundled examples 做 profile-guided sample；结果显示当前样本主要热在 `model_evaluate_s`，下一步应优先继续 model evaluate/indexed/Rust 路线，而不是立刻重写 event queue。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| experiment | 有 009/011 profiler，但没有样本结论 | 跑 5 个本地 examples 并整理 timing/counters | 不改代码 |
| decision | evaluate vs timer/event queue 仍靠直觉 | 用 sample 数据给出下一步优先级 | 不改代码 |
| docs | 只有 profiler 设计 | 增加 profile-guided 诊断记录 | 不改代码 |

## Principle

这一步属于 **选择优化方向**，不是直接优化。

我们同时看两类信息：

```text
model_evaluate_s / model_prepare_step_s / model_post_update_s
```

和：

```text
source_breakpoint_scan_calls
model_breakpoint_scan_calls
timer_breakpoint_scans_total
```

如果 `model_evaluate_s` 占比高，说明继续迁移 `_get_voltage`、表达式执行、`_set_output`、node array backend 更合理。

如果 timer/breakpoint scan 很高且 timing 也高，才更适合优先做 event queue 或 timer heap。

## Commands Run

All outputs were written outside the repo:

```bash
mkdir -p /private/tmp/evas-profile-012
EVAS_PROFILE_SECTIONS=1 EVAS_PROFILE_MODEL_EVAL=1 python3 -m evas.cli simulate evas/examples/digital_basics/tb_inverter_chain.scs -o /private/tmp/evas-profile-012/inverter_chain -l /private/tmp/evas-profile-012/inverter_chain.log
EVAS_PROFILE_SECTIONS=1 EVAS_PROFILE_MODEL_EVAL=1 python3 -m evas.cli simulate evas/examples/clk_div/tb_clk_div_div8.scs -o /private/tmp/evas-profile-012/clk_div_div8 -l /private/tmp/evas-profile-012/clk_div_div8.log
EVAS_PROFILE_SECTIONS=1 EVAS_PROFILE_MODEL_EVAL=1 python3 -m evas.cli simulate evas/examples/comparator/tb_cmp_delay.scs -o /private/tmp/evas-profile-012/cmp_delay -l /private/tmp/evas-profile-012/cmp_delay.log
EVAS_PROFILE_SECTIONS=1 EVAS_PROFILE_MODEL_EVAL=1 python3 -m evas.cli simulate evas/examples/adc_dac_ideal_4b/tb_adc_dac_ideal_4b_ramp.scs -o /private/tmp/evas-profile-012/adc_ramp -l /private/tmp/evas-profile-012/adc_ramp.log
EVAS_PROFILE_SECTIONS=1 EVAS_PROFILE_MODEL_EVAL=1 python3 -m evas.cli simulate evas/examples/noise_gen/tb_noise_gen.scs -o /private/tmp/evas-profile-012/noise_gen -l /private/tmp/evas-profile-012/noise_gen.log
```

Important: these runs have profile enabled and must not be used as paper-facing speed numbers.

## Sample Results

| Case | Accepted tran steps | Internal steps | `model_evaluate_s` | `prepare_s` | `post_s` | Evaluate fraction | Source scans | Model scans | Timer scans |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `adc_ramp` | 804 | 190401 | 8.834 | 0.659 | 0.270 | 90.5% | 571203 | 380802 | 2 |
| `clk_div_div8` | 1527 | 61289 | 0.544 | 0.159 | 0.054 | 71.9% | 61289 | 61289 | 1 |
| `cmp_delay` | 1814 | 232859 | 5.602 | 0.918 | 0.353 | 81.5% | 698577 | 465718 | 2 |
| `inverter_chain` | 373 | 46124 | 0.700 | 0.162 | 0.087 | 73.8% | 46124 | 184496 | 4 |
| `noise_gen` | 50937 | 50937 | 0.513 | 0.075 | 0.041 | 81.5% | 0 | 50937 | 1 |

## Interpretation

The current sample points to model evaluation as the next priority:

- `model_evaluate_s` dominates the model-loop timing in all 5 sampled cases.
- Timer breakpoint scans are tiny in these examples: 1 to 4 total scans.
- Source/model scan call counts can be high, but the dominant measured section is still evaluate.
- `accepted tran steps` and `internal steps` differ substantially; future speed reports must be explicit about which one they use.

Recommended next engineering direction:

```text
continue indexed/Rust model-evaluate migration
```

Defer for now:

```text
global event queue rewrite
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `not applicable`
- Accuracy impact: `none`; this is a diagnostic run only

## Learning Notes

### 为什么 accepted steps 和 internal steps 不一样？

`accepted tran steps` 是输出/记录视角看到的 transient point 数。

`steps_total` 是 EVAS 内部主循环实际走过的步数，包含 refine/dynamic step 等内部细分。

如果一个 case：

```text
accepted = 804
internal = 190401
```

说明用户看到的输出点不多，但 simulator 内部为了事件、动态步长或精度控制走了很多小步。优化内核时应该关注 internal steps 和 per-step cost。

### 为什么 evaluate fraction 高就指向 Rust/indexed？

`model_evaluate_s` 里包含模型表达式执行、`_get_voltage()`、`_set_output()`、状态更新等。Python 这里的典型开销是：

```text
dict lookup
string key mapping
Python function call
object boxing/unboxing
generated Python expression execution
```

这些正是 indexed array 和 Rust hot loop 能改善的地方。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 样本不代表 vaBench release | 后续 release profile 显示 timer/event 占主导 | 将 012 标为 sample evidence，不作为全量结论 |
| profile 开销污染 wall time | profile-on wall 被误用于速度表 | 只把 012 用作优化排序，不用于 speed claim |
| scratch logs 丢失 | `/private/tmp` 被清理 | 文档保留关键表格和命令 |

## Next Step

下一篇审计文档建议：

- `013-indexed-expression-read-write-path.md`：继续把 model evaluate 中的普通 read/write 路径向 indexed/Rust 迁移，优先减少 Python dict/string lookup 和 generated Python call overhead。
