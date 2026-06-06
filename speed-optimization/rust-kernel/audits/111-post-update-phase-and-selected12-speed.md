# 111 - Post-update Phase RustSimProgram 与 12-row 速度复测

日期：2026-06-06

## 本轮修改

本轮补的是严格 EVAS2 RustSimProgram 中的一个通用调度缺口：output-dependent `cross()` / `above()` 事件。

之前 Python EVAS 对这类事件有两阶段语义：

1. pre-event：输入源或外部节点触发的事件，在 evaluate 前执行。
2. post-update event：事件表达式读取本模型刚贡献的输出节点时，必须在 evaluate/transition 后再检测；如果事件 body 改了 state，还要 refresh outputs。

这轮把这个语义迁进 RustSimProgram：

- `RustSimEvent` 增加 `phase` 字段：`pre` 或 `post`。
- lowering 复用 backend 的语义规则：如果 `cross/above` 表达式引用本模型贡献节点，则标成 post phase。
- Rust loop 调度顺序变成：
  `source -> pre event body -> static evaluate -> transition -> post event body -> refresh evaluate/transition -> record`
- strict EVAS2 required-path 失败时，异常信息会带上 `RustSimProgram rejection`，方便后续审计具体 blocker。
- rejection 诊断从粗粒度 `event_body_not_lowered` 扩展到具体标签，例如 `complex_if_write_set`、`for_loop`、`system_task:$strobe`、`unsupported_binary_operator:>>`。

## 新增回归

新增测试：

- `test_rust_sim_program_post_update_cross_refreshes_outputs`

覆盖行为：

- `V(mid) <+ V(inp)` 先由 Rust evaluate 更新。
- `@(cross(V(mid)-0.5,+1)) seen = 1` 在 post phase 触发。
- `V(out) <+ seen` 需要同一时间点 refresh 后生效。
- RustSimProgram 输出与默认 Python EVAS 输出一致。

## 本地验证

| 检查 | 结果 |
| --- | --- |
| Python compile: `rust_program.py` / `rust_backend.py` / `engine.py` / `test_engine.py` | PASS |
| `cargo build --release` in `EVAS/evas/rust_core` | PASS |
| `pytest EVAS/tests/test_engine.py -q -k "rust_sim_program"` | 10 passed |
| `pytest EVAS/tests/test_engine.py -q` | 260 passed |

## 12-row 速度复测

速度报告：

- `speed-optimization/reports/rust_sim_program_111_selected12_smoke_20260606.json`
- `speed-optimization/reports/rust_sim_program_111_selected12_smoke_20260606.md`

诊断报告：

- `speed-optimization/reports/rust_sim_program_111b_failure_reasons_20260606.json`
- `speed-optimization/reports/rust_sim_program_111b_failure_reasons_20260606.md`

整体模式汇总：

| Mode | PASS | Non-PASS | Total EVAS wall s | Safe vs strict | Unsafe vs strict |
| --- | ---: | ---: | ---: | ---: | ---: |
| `strict_current` | 12 | 0 | 40.250 | 0 | 0 |
| `profile_fast_evas2` | 7 | 5 | 6.211 | 7 | 5 |

注意：完整 12-row aggregate 仍不能作为速度 claim，因为还有 5 个 row 没有 strict Rust whole-segment runtime。

## 安全子集速度

只统计 `strict_current PASS` 且 `profile_fast_evas2 PASS` 的 7 个 row：

| Entry | strict wall s | EVAS2 wall s | speedup | path |
| --- | ---: | ---: | ---: | --- |
| `vbr1_l1_binary_weighted_voltage_dac` | 0.662 | 0.869 | 0.76x | RustSimProgram |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | 8.918 | 1.032 | 8.64x | RustSimProgram, new post phase coverage |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | 0.363 | 0.367 | 0.99x | RustSimProgram |
| `vbr1_l1_pipeline_adc_stage` | 1.446 | 0.492 | 2.94x | RustSimProgram |
| `vbr1_l1_propagation_delay_comparator` | 13.348 | 0.628 | 21.25x | existing specialized Rust path |
| `vbr1_l1_segmented_dac` | 0.409 | 0.397 | 1.03x | RustSimProgram |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | 2.889 | 0.681 | 4.24x | existing specialized Rust path |

安全子集合计：

- strict sum wall: `28.035 s`
- EVAS2 sum wall: `4.467 s`
- safe-subset sum speedup: `6.28x`

对比 110：

- safe coverage: `6/12 -> 7/12`
- 新增安全 row: `vbr1_l1_capacitive_weighted_sar_feedback_dac`
- 这个新增 row 的速度：`8.918 / 1.032 = 8.64x`

## 剩余未覆盖原因

这 5 个 row 仍然不是有效速度证据，因为 strict EVAS2 required path 没有生成 `tran.csv`，原因是没有支持的 whole-segment Rust runtime。

| Entry | 当前 blocker |
| --- | --- |
| `vbr1_l1_clocked_adc_quantizer` | event body 含 `$strobe`、非数值 literal、`>>` 右移 |
| `vbr1_l1_edge_interval_timer` | event body 是复杂 if write-set |
| `vbr1_l1_lfsr_prbs_generator` | event body 含 `for_loop`、数组赋值/动态数组读、`$strobe`、`>>` |
| `vbr1_l1_sar_logic` | event body 是复杂 if write-set |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `$bound_step` 尚未迁入 Rust loop |

## 当前判断

本轮不是“全量 Rust 化完成”，但证明了 post-update phase 是一个有效的通用迁移点：CDAC 从 unsupported 变成 safe，并且在该 row 上得到 `8.64x` speedup。

下一步优先级：

1. event body 复杂 if write-set lowering：直接挡住 edge interval 和 SAR logic。
2. 支持 `>>` / `<<` / bit-not，并对 `$strobe` 做 strict-safe no-op 或 trace-side effect lowering：挡住 clocked ADC 和 LFSR。
3. static/dynamic array loop lowering：挡住 LFSR。
4. `$bound_step(expr)` 作为 Rust loop 的 next-dt clamp：挡住 ADPLL。

这些仍是全局语义迁移，不是 benchmark 特例。
