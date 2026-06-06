# 112 - 组合 event body / bus-bit / bound_step / scaled transition RustSimProgram

日期：2026-06-06

## 本轮目标

111 之后，strict EVAS2 的 RustSimProgram 已能拥有 source、pre/post event、部分 event body、transition 和 record，但真实 selected rows 仍有几个核心缺口：

- SAR 这类状态机的 `if/else-if` event body 能进入 Rust，但把条件拍平成 per-target ternary 后会改变状态更新顺序。
- LFSR/ADC 类数字状态需要 `<<`、`>>`、`~`、static bus/index 和 fixed `for` loop unroll。
- ADPLL 使用 `$bound_step(expr)` 控制下一步最大步长。
- ADPLL 的输出是 `vl + (vh - vl) * transition(...)`，不是裸 `transition(...)`。
- ADPLL 还包含非 transition 连续贡献，例如 `V(vctrl_mon) <+ expr`。

这轮目标是把这些语义作为通用 lowering 补进 RustSimProgram，而不是给 benchmark 名称加特例。

## 主要修改

### 1. ordered if/else body op

旧实现把：

```verilog
if (state == 0) begin
    ...
    state = 1;
end else if (state == 1) begin
    ...
end
```

压成每个 target 一个 `select(cond, then, else)` 表达式。这个方法对简单组合逻辑可以，但对有限状态机危险：分支选择应使用旧 `state`，分支内部写 `state` 应在语句顺序里发生。

本轮新增 Rust body control ops：

- `BODY_STMT_IF`
- `BODY_STMT_ELSE`
- `BODY_STMT_ENDIF`

Rust executor 现在维护 branch-active stack，按 Verilog-A 源顺序执行嵌套 `if/else`。这修复了 SAR 从 `code176=1000 expected=1010` 的错误。

### 2. 数字状态与 bus/index lowering

新增/扩展：

- `<<`、`>>`、`~` body expression op。
- static `V(bus[i])` / `V(out[i])` node name resolution。
- fixed integer `for` loop compile-time unroll。
- constant expression folding，使 `i+1` 这类 loop substitution 后可解析为静态数组下标。
- `$display` / `$strobe` 在 strict Rust waveform path 中作为 no-op side effect 处理；当前不 claim strobe text parity。

这些使 LFSR、static bus、bit weight、transition target bus 输出能进入 Rust。

### 3. `$bound_step` 进入 Rust loop

新增 `BODY_STMT_BOUND_STEP`。event body 执行 `$bound_step(expr)` 时，Rust 保存一个 `bound_step_limit`，在下一轮选步时用它 clamp `dt`，然后进入新一轮 event/evaluate 前清空。

这个生命周期对齐 Python EVAS 的 `_bound_step`：先用上一轮 event/evaluate 设置的 bound，再在本轮 evaluate 前 reset。

### 4. scaled transition target

旧 transition lowering 只支持：

```verilog
V(out) <+ transition(x, delay, rise, fall);
```

ADPLL 使用的是：

```verilog
V(out) <+ vl + (vh - vl) * transition(x, delay, rise, fall);
```

本轮将 transition spec 扩展为：

- target/delay/rise/fall expression
- output_bias expression
- output_scale expression

Rust transition state 仍只对 `x` 做 ramp，但写回节点时执行：

```text
node = reference + output_bias + output_scale * transition_output
```

因此支持 `transition(x)`、`scale * transition(x)`、`bias + scale * transition(x)`、减号和一元负号组合。

### 5. direct continuous contribution

非 transition 连续贡献如：

```verilog
V(vctrl_mon) <+ vl + (vh - vl) * code_norm;
```

现在会 lowering 成 Rust always-body node write，不再被跳过。

## 验证

| 检查 | 结果 |
| --- | --- |
| `python3 -m py_compile` for touched simulator files | PASS |
| `cargo build --release` in `EVAS/evas/rust_core` | PASS |
| `pytest EVAS/tests/test_engine.py -q -k "rust_sim_program"` | 15 passed |
| `pytest EVAS/tests/test_engine.py -q` | 265 passed |

新增/更新的关键回归：

- ordered nested state machine：验证分支条件读旧 state，分支末尾写新 state。
- static bus + bitshift + transition target：验证 bus bit 权重和 static indexed output。
- static `for` loop state array：验证 fixed loop unroll 和 array state。
- `$bound_step + bias/scale transition + direct output`：验证 ADPLL 暴露出的组合语义。

## selected-5 真实 benchmark 结果

报告：

- `speed-optimization/reports/rust_sim_program_112f_failure_reasons_20260606.json`
- `speed-optimization/reports/rust_sim_program_113d_selected5_20260606.json`

覆盖变化：

| 阶段 | PASS | Non-PASS | 说明 |
| --- | ---: | ---: | --- |
| 112f | 3/5 | 2/5 | SAR 已进入 Rust 但 checker fail；ADPLL 因 `$bound_step` 被拒绝 |
| 113d | 5/5 | 0/5 | SAR ordered-if 修复；ADPLL `$bound_step` + scaled transition + direct contribution 修复 |

113d per-row：

| Entry | Status | EVAS wall s | Rust events | Body stmt ops | Expr ops | Transitions | Points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `vbr1_l1_clocked_adc_quantizer` | PASS | 1.003 | 2 | 16 | 73 | 3 | 829 |
| `vbr1_l1_edge_interval_timer` | PASS | 0.810 | 3 | 17 | 56 | 2 | 2403 |
| `vbr1_l1_lfsr_prbs_generator` | PASS | 0.698 | 3 | 216 | 579 | 1 | 3199 |
| `vbr1_l1_sar_logic` | PASS | 0.432 | 2 | 45 | 104 | 5 | 279 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | PASS | 1.149 | 6 | 179 | 372 | 3 | 9155 |

ADPLL 单行补充证据：

- `rust_sim_program_transition_count = 3`
- `fb_clk`/`vout`/`lock` 输出范围为 `0.0` 到 `0.9 V`
- checker note: `pre_vout_ref=4.000 post_vout_ref=5.900 pre_vout_fb=4.000 post_vout_fb=6.000 pre_fb_ref=1.000 post_fb_ref=0.983 pre_lock=1.000 post_lock=1.000 vctrl_range_ok=True`

## 当前 claim 边界

可以说：

- strict EVAS2 RustSimProgram 对 selected-5 诊断样本已从 `3/5` 提升到 `5/5` PASS。
- 本轮迁移的是通用语义：ordered event body、数字 bit/bus、fixed loop、`$bound_step`、scaled transition、direct contribution。
- SAR 和 ADPLL 之前暴露的问题已由通用 Rust lowering 修复。

不能说：

- 不能 claim 全量 Rust 化完成。
- 不能 claim release-wide benchmark 全部可由 RustSimProgram 运行。
- 不能 claim 快于 Spectre AX；本轮是 EVAS-only strict Rust coverage diagnostic，没有同机同 slice Spectre AX timing。
- 不能 claim `$strobe` 文本输出 parity；当前只保证 waveform side effect no-op 不影响仿真波形。

## 剩余工作

下一步应从 selected-5 转到 release-wide coverage manifest：

1. 用 strict EVAS2 required path 扫 release gold，统计还有哪些模型仍 rejected 或 checker fail。
2. 对 remaining blockers 继续按语义分类，而不是按 benchmark 名称分类。
3. 补 final_step、case/while、更复杂 dynamic bus、array write side effect、file/strobe side effect、adaptive err-ratio 和 sparse record 全链路。
4. 做同机 same-slice EVAS/Spectre AX/strict timing 前，不把 EVAS2 coverage diagnostic 转成论文速度 claim。
