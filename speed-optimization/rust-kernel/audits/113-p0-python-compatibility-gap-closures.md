# 113 - P0 Python EVAS Compatibility Gap Closures

日期：2026-06-06

## 本轮目标

本轮继续沿 108 之后的 EVAS2 strict RustSimProgram 主线推进：不再增加 benchmark-name fastpath，而是把 Python EVAS 已支持、但 Rust EVAS2 仍拒绝的通用 Verilog-A 语义补到 typed IR / Rust loop 边界里。

本轮不是速度 claim，也不是“全量 Rust 化完成”声明。判断标准是：

```text
release compile-ok Verilog-A 模型能否构造 strict RustSimProgram
```

也就是先证明更多真实模型可以进入 Rust-owned simulation loop，之后再做同机 runtime / speed / Spectre AX 对比。

## 本轮修复内容

| 修复项 | 原来问题 | 现在做法 | 代表行为 |
| --- | --- | --- | --- |
| `final_step` event | Rust event due 只处理 normal loop 事件，`@(final_step)` 无法进入 RustSimProgram | 新增 `RUST_SIM_EVENT_FINAL_STEP`，normal loop 跳过 final-step，主循环结束后在 Rust 中执行 final-step body，且不额外 append trace point | measurement / cleanup state 在仿真结束时更新 |
| `case` event body | `case` body 被 `event_body_not_lowered` 拒绝 | 在 stmt IR 中把 `case` lowering 成 ordered nested `if/else` body op | 数字状态机 / mode select |
| differential voltage contribution | `V(out, ref) <+ expr` 被认为 target 不支持 | 编码成 `out = V(ref) + expr` 的 node write | 带 reference node 的电压贡献 |
| `tan` / `tanh` | expression stack 缺少 pure math opcode | 新增 body expr opcode `BODY_EXPR_TAN/TANH`，Rust evaluator 直接调用 `f64::tan/tanh` | 非线性但无状态数学表达式 |
| transition 后的 continuous body | transition 后普通 `V(mon)<+expr` 被拒绝为 `continuous_body_after_transition_not_lowered` | 按 source order 将 transition 后的 ordinary contribution 放入 POST-phase always body | ADPLL monitor output |
| top-level static `for` transition outputs | `for(i) V(out[i]) <+ transition(...)` 被误送进 ordinary body encoder | static for 展开后交给 transition collector；loop index init/update 只作为展开痕迹跳过 | DWA / bus output transition |
| observed static state-array slots | AST 对宏/倒序 array range 可能丢信息，例如 `bits[8:1]` 变成 `0:1` | RustSimProgram 编译时从实际 `arr[static_idx]` 读写反推并扩展 typed state slot | SAR `dout_bits[8]` / `trial_bits[8]` |

## 覆盖率变化

扫描对象：

```text
behavioral-veriloga-eval/benchmark-vabench-release-v1/tasks/**/*.va
```

| 阶段 | compile-ok | RustSimProgram candidate | 剩余 compile-ok 非 candidate | 说明 |
| --- | ---: | ---: | ---: | --- |
| 本轮前审计 | 348 | 328 | 20 | 主要缺 `case/final_step/differential/tan/tanh/static-for/array-slot` |
| static-for transition 修复后 | 348 | 333 | 15 | DWA 5 个文件进入 RustSimProgram candidate |
| observed array-slot 修复后 | 348 | 335 | 13 | weighted SAR 2 个文件进入 RustSimProgram candidate |

当前静态 candidate 覆盖：

```text
335 / 348 = 96.3% compile-ok model-level RustSimProgram candidate
```

注意：这是“能构造 strict RustSimProgram”的模型级覆盖，不等价于 release benchmark row 全部 runtime PASS，也不等价于速度提升数字。

## 剩余 blocker

| 类别 | 文件数 | 代表模型 | 为什么还没收 |
| --- | ---: | --- | --- |
| dynamic `while` loop | 2 | `cppll_timer_ref` | phase wrapping 使用 `while (phase_err > 0.5 * ref_period)`；直接迁 Rust while 有死循环/收敛风险，应做受限 loop IR 或数学 wrap primitive |
| file I/O side effect | 5 | `file_metric_writer` / `final_step_file_metric_ref` | `$fopen/$fwrite/$fclose` 和 string literal 涉及文件句柄、格式化输出、checker side-effect，不应作为 waveform no-op 偷过 |
| random distribution | 6 | `noise_gen` / `noise_gen_ref` | `$rdist_normal` 需要确定随机种子、分布和 Python/Spectre parity 策略；不能随意替换成 Rust RNG |

## 验证

| 检查 | 结果 |
| --- | --- |
| 新增 P0 semantic tests | PASS |
| `PYTHONPATH=. python3 -m pytest tests/test_engine.py -q -k 'rust_sim_program'` | `21 passed, 250 deselected` |
| `cargo test` in `EVAS/evas/rust_core` | `37 passed` |
| release coverage audit | `357 files, 348 compile_ok, 335 RustSimProgram candidates, 13 remaining compile-ok non-candidates` |

新增/覆盖的关键回归：

- `test_rust_sim_program_body_differential_contribution_matches_default`
- `test_rust_sim_program_event_body_case_matches_default`
- `test_rust_sim_program_final_step_updates_state_after_trace`
- `test_rust_sim_program_body_tan_tanh_matches_default`
- `test_rust_sim_program_top_level_static_for_transition_outputs`
- `test_rust_sim_program_one_based_state_array_transition_target`

## 当前 claim 边界

可以说：

- 本轮把 RustSimProgram 静态 candidate 覆盖从 `328/348` 提升到 `335/348`。
- DWA 类 static-for transition output 和 weighted SAR 类 1-based/static state array transition target 已进入通用 Rust lowering。
- `final_step/case/differential contribution/tan/tanh/post-transition continuous body` 都有 targeted parity regression。

不能说：

- 不能 claim 全量 Rust 化完成。
- 不能 claim `335/348` 已经等价于 release benchmark 全部 Rust EVAS2 runtime PASS。
- 不能 claim 快于 Spectre AX；本轮没有跑同机同 slice Spectre AX timing。
- 不能把 file I/O 或 random distribution 简化成 no-op 来冲覆盖率，否则 checker 语义会被破坏。

## 下一步顺序

1. 为 `while` loop 定义受限 IR：优先支持 phase-wrap / bounded-update 这类可证明终止的循环，不支持时继续显式 reject。
2. 为 `$rdist_normal` 定义随机语义：种子、分布、repeatability、与 Python EVAS/Spectre 的容差关系。
3. 为 file I/O side effect 定义 Rust runtime：文件句柄表、format string、final_step flush/close、checker 读取路径。
4. 做 release row strict Rust EVAS2 runtime smoke：从 model-level candidate 进入 row-level PASS/FAIL 统计。
5. 只有 row-level PASS 稳定后，再做 Rust EVAS2 / Python EVAS1.0 / Spectre AX / Spectre strict 同机速度表。
