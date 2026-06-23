# 065 - Semantic/Dataflow Whole-Segment Matching

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `/private/tmp/vaevas_semantic_cppll_after.json`
- `/private/tmp/vaevas_semantic_cppll_after.md`
- `/private/tmp/vaevas_semantic_wseg_top4_after.json`
- `/private/tmp/vaevas_semantic_wseg_top4_after.md`

## One-Line Summary

把 064 的 whole-segment candidate 从端口名/状态名强绑定改成语义和数据流匹配；真实 top-wall 4-row smoke 仍 `4/4 PASS`，并修复了 CPPLL supply direction 反向导致 `vctrl_mon=0` 的 correctness 风险。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Compiler matcher | 多数非 LFSR whole-segment collector 依赖特定端口名、状态名和参数名 | collector 先建立 semantic/dataflow index，再根据事件、branch access、assignment、transition target、parameter reference 推断角色 | 默认不变 |
| CPPLL/ref supply role | `vl + (vh - vl) * transition(...)` 中可能按 identifier 出现顺序返回 `VSS,VDD` | 优先从 affine transition 的 `scale = high - low` 推断 `(VDD,VSS)` | opt-in fastpath correctness 修复 |
| Tests | 只断言真实 gold 能 emit candidate kind | 额外断言 CPPLL/ref candidate 的 supply tuple 是 `("VDD", "VSS")`，并保留 name-only stub rejection | 默认不变 |
| Matching policy | 换端口名/状态名后容易漏命中或误拒绝 | 只要 Verilog-A 行为保持相同数据流，后续模型可以复用同一范式 | 默认不变 |

## Principle

这轮不是把更多代码搬到 Rust，而是把“能否 whole-segment lowering”的判断从名字匹配升级成语义匹配。

旧方式接近：

```text
port name == VDD
state name == dco_q
output name == vctrl_mon
```

新方式接近：

```text
这个模型有 timer/cross 事件
这个状态由 toggle/data reduction/decision dataflow 驱动
这个输出由 transition(state, ...) 或 direct state contribution 驱动
这个 transition 的摆幅是 high - low，所以 high/low supply 有方向
```

这样换一个 Verilog-A 模型时，端口名和局部状态名可以不同；只要行为数据流等价，compiler 仍然有机会生成相同 candidate metadata。后续其他函数也应该沿用这个范式：先识别事件和数据流角色，再生成 executor metadata，而不是写模型名特判。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| CPPLL fastpath checker | `FAIL_SIM_CORRECTNESS` in fresh repro before fix | `PASS` | supply role 方向修复有效 |
| CPPLL `vctrl_mon` range | `0.000..0.000` | `0.4266..0.4808` | fastpath 恢复正确控制电压 |
| CPPLL whole-segment points | `46071` | `52174` | 修正 supply 后 DCO schedule 回到 expected frequency |
| top4 behavior checker | blocked by CPPLL fail before fix | `4/4 PASS` | semantic matcher smoke safe |
| top4 total EVAS wall | baseline `11.090s` | semantic fastpath `7.064s` | same run, opt-in fastpath `1.57x`;不是 paper-facing Spectre speed claim |

Top4 smoke after the fix:

| Entry | Form | Baseline status | Semantic fastpath status | Wall before | Wall after | Speedup | Enabled fastpath |
|---|---|---|---|---:|---:|---:|---|
| `vbr1_l1_gain_estimator` | `tb` | PASS | PASS | `0.203s` | `0.180s` | `1.13x` | `gain_timer_reduction` |
| `vbr1_l1_propagation_delay_comparator` | `dut` | PASS | PASS | `1.896s` | `0.570s` | `3.33x` | `cmp_delay` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | PASS | PASS | `2.760s` | `0.905s` | `3.05x` | `cppll_reacquire` |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | PASS | PASS | `6.230s` | `5.410s` | `1.15x` | `sar_loop` |
| **Total** | 4 rows | **4/4 PASS** | **4/4 PASS** | **`11.090s`** | **`7.064s`** | **`1.57x`** | all expected |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

The whole-segment path remains opt-in through `evas_rust_full_model_fastpath=true`. If semantic matching fails or instance wiring/recorded signals do not satisfy the executor contract, EVAS falls back to the normal simulator path.

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
  python3 -m py_compile \
  EVAS/evas/simulator/backend.py \
  EVAS/evas/simulator/engine.py \
  EVAS/tests/test_rust_backend.py

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
  python3 -m pytest EVAS/tests/test_rust_backend.py -q

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS:/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
  python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --entry vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow \
  --form tb \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_full_model \
  --output-root /private/tmp/vaevas_semantic_cppll_after \
  --report-json /private/tmp/vaevas_semantic_cppll_after.json \
  --report-md /private/tmp/vaevas_semantic_cppll_after.md \
  --timeout-s 240 --jobs 1

PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS:/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
  python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --entry vbr1_l1_gain_estimator \
  --entry vbr1_l1_propagation_delay_comparator \
  --entry vbr1_l2_weighted_sar_adc_dac_loop \
  --entry vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow \
  --form tb --form dut \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_full_model \
  --output-root /private/tmp/vaevas_semantic_wseg_top4_after \
  --report-json /private/tmp/vaevas_semantic_wseg_top4_after.json \
  --report-md /private/tmp/vaevas_semantic_wseg_top4_after.md \
  --timeout-s 240 --jobs 1
```

Results:

```text
py_compile: PASS
EVAS/tests/test_rust_backend.py: 24 passed
CPPLL single-row runner: PASS/PASS, vctrl_min=0.427, vctrl_max=0.481
Top4 runner: 4/4 PASS baseline, 4/4 PASS semantic fastpath
```

## Learning Notes

语义/数据流匹配可以理解成“看电路行为，不看变量名字”。

例如 CPPLL 输出电平通常写成：

```verilog
V(dco_clk) <+ vl + (vh - vl) * transition(dco_q, 0, tedge, tedge);
```

这里真正重要的是：

- `dco_q` 是被 timer toggle 的状态；
- `transition(dco_q, ...)` 把 0/1 状态变成边沿；
- `vh - vl` 是输出摆幅；
- `vl + ...` 是低电平偏置。

所以 high supply 应该来自 `vh`，low supply 应该来自 `vl`。旧逻辑只看 identifier 出现顺序，看到 `vl, vh, vl` 就可能错误返回 `(vl, vh)`。这次修复后，compiler 从 `scale = vh - vl` 这个数据流结构判断方向。

这个思想后续可以复用到其他函数：

```text
事件触发条件 -> 哪些输入控制时序
状态赋值链 -> 哪些变量是 latch/counter/accumulator/decision
输出贡献 -> 哪些节点由哪些状态驱动
参数引用 -> 哪些参数是 delay/gain/threshold/supply
```

只要这些关系一致，名字可以变，executor metadata 仍然可以一致。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 语义规则过宽，误命中相似但不同的模型 | candidate emitted but behavior checker or waveform parity fails | tighten `_collect_*_candidate` guard or disable that candidate kind |
| supply direction 解析覆盖不足 | `vctrl_mon`/digital outputs rail-inverted or clamped | revert `_whole_segment_directed_supply_ports_from_transition_expr` or add explicit affine form support |
| 只在 top4 验证，未证明全 benchmark | broader runner exposes non-target mismatch | keep fastpath opt-in and add per-kind shadow/parity before promotion |

## Next Step

- `066 - Whole-Segment Semantic Matcher Coverage Audit`: 对 top-wall 10/全 release 可仿 slice 跑 candidate manifest，列出哪些模型命中、哪些因 event/state/dynamic bus/nonlinear 被拒绝。
- `067 - Rust ABI For Whole-Segment Executors`: 在 065 metadata 稳定后，把 CPPLL/SAR/cmp/gain executor 从 Python engine 迁到 Rust ABI。
