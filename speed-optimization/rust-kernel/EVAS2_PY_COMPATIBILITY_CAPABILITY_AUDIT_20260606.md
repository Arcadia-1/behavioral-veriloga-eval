# EVAS2 Rust Capability Audit vs Py EVAS1.0

Date: 2026-06-06

## 审计口径

这张表只回答一个问题：**当前 Rust EVAS2 是否已经覆盖 Py EVAS1.0 能跑的 Verilog-A 行为语义。**

计入 Rust 支持的条件：

- 必须能 lower 到 strict `RustSimProgram` 或已接 production Rust loop。
- shadow、prototype、diagnostic fastpath、Python fallback 不算 Rust EVAS2 覆盖。
- 本表只讨论 EVAS 既定范围：纯 voltage-domain、event-driven behavioral Verilog-A。

不计入 Rust 缺口的内容：

- `I(...) <+`、`q(...) <+`、`ddt/idt/laplace`、AC/DC、小信号、晶体管级/KCL/KVL、Spectre subckt SPICE hierarchy。这些不是当前 Py EVAS1.0 paper-facing 支持范围。

## 当前 release 静态证据

证据文件：

- Raw JSON: `behavioral-veriloga-eval/speed-optimization/reports/evas2_release_rust_capability_audit_raw_20260606.json`
- 生成方式：用当前 `EVAS/prototypes/audit_098_current_rust_coverage.py` 同等逻辑扫描 `benchmark-vabench-release-v1/tasks` 下 gold `.va`。

| 指标 | 当前结果 | 含义 |
|---|---:|---|
| gold `.va` 文件总数 | 357 | release 静态扫描对象 |
| Py parser/compiler compile-ok | 348 | 这些文件进入 Py EVAS compiler 后才谈 Rust lowering |
| compile-failed | 9 | 前端 parser 层阻塞，不是 Rust 后端语义缺口 |
| `RustSimProgram` candidate | 326 / 348 | 当前 strict Rust EVAS2 lowerer 静态接受的 compile-ok 模型 |
| `RustSimProgram` compile-ok 文件覆盖率 | 93.7% | 只表示模型级语义可 lower，不表示仿真 PASS 或速度提升 |
| `RustSimProgram` 总文件覆盖率 | 91.3% | 包含 parser 失败文件后的保守文件级覆盖 |
| non-candidate compile-ok | 22 / 348 | 当前最应该优先补的 Py-supported Rust 缺口 |
| whole-segment candidate | 257 | 旧 whole-segment/specialized candidate 统计，不等价于 full Rust |
| event-transition plan candidate | 292 | event + transition ordered plan 的静态候选数 |
| isolated body-IR candidate | 0 | release 模型大多包含 event/transition，不能用旧纯 body-IR 路径代表覆盖 |

compile-failed 文件集中在 `vin_src.va`、`lfsr.va`、`multitone.va`、`programmable_stimulus_sequencer.va`。这些需要先确认是 release gold 语法确实超出当前 parser，还是 audit 脚本入口没有复用完整 runner 的预处理。

## Py EVAS1.0 vs Rust EVAS2 能力矩阵

| 行为语义 | Py EVAS1.0 状态 | Rust EVAS2 当前状态 | 证据 | 缺口和后续动作 |
|---|---|---|---|---|
| DC / pulse / sine / PWL source | 支持 | 已 production 接入 | `RustSimSource` + Rust source loop 支持 `dc/pulse/sine/pwl` | 需要 release 仿真验证真实 testbench source 配置，不是当前主要缺口 |
| voltage node / port 编号 | 支持 dict 节点名读写 | 已 production 接入 typed node id | `RustSimNode`、`record_node_ids`、source/record Rust loop | 仍有外层 Python runner/CSV 包装，不影响语义但影响 E2E wall |
| `V(node)` 静态读 | 支持 | 已 production 接入 | body expr ABI 支持 `READ_NODE` | 动态 bus/indexed node read 仍是部分支持 |
| `V(node, ref)` 静态差分读 | 支持 | 已 production 接入 | body expr lowering 读两个 node 后做 subtract | 动态 indexed ref 仍需 array/bus lowering |
| `V(out) <+ expr` 单节点连续贡献 | 支持 | 部分 production 接入 | body stmt ABI 可写单节点 target | 复杂连续 body、部分 SAR 类普通贡献仍拒绝；release non-candidate 中 `continuous_contribution_not_lowered` 14 次 |
| `V(out, ref) <+ expr` 普通差分连续贡献 | 支持 | 未完整 production 接入 | body stmt `_encode_contribution_target` 只接受无 `node2` 目标 | 需要把 direct contribution target 扩成 `(out, ref)`，并在 Rust writeback 中处理参考节点语义 |
| `V(out, ref) <+ transition(...)` | 支持 | 部分 production 接入 | transition runtime/schema 有 `reference_node_id` | 只支持静态 target/ref 和可编码 transition target/delay/rise/fall；动态 indexed target/ref 仍缺 |
| scalar real/integer state | 支持 | 已 production 接入 | `RustSimState.is_integer`、body write coercion tests | 复杂 side-effect 顺序仍要靠 ordered body lowering gate |
| state array 固定下标 | 支持 | 已 production 接入 | fixed array slot flattening + static for unroll | 只覆盖编译期可确定下标 |
| state array 动态下标/动态写目标 | 支持 | 部分/缺口 | release non-candidate 有 `array_assignment_target` 6 次、`array_read_or_dynamic_index` 2 次 | 需要 typed array op：动态 index bounds check、array read/write、event body 顺序写回 |
| numeric parameter | 支持 | 已 production 接入 | `RustSimParam` 只保存 `float` value | 参数表达式需要能静态/运行时转成数值 |
| string parameter / string literal | 支持于 Py side-effect 场景 | Rust EVAS2 缺口 | release non-candidate 有 `non_numeric_literal` 6 次 | 需要 side-effect ABI 或明确把字符串只限制在 file/log 系统任务 |
| 算术/比较/逻辑/位运算/ternary | 支持 | 已 production 接入 | body expr ABI 支持 `+ - * / %`、比较、`&& ||`、`& | ^ << >> ~`、`select` | 仍要验证所有 release 组合表达式 pass；动态 array expression 是独立缺口 |
| 常用数学函数 | 支持 | 部分 production 接入 | Rust body ABI 支持 `abs/sqrt/exp/ln/log/sin/cos/floor/ceil/min/max/pow` | Py expr 层还认识 `tan/tanh`，但 Rust body ABI 当前没有对应 opcode |
| `$abstime` / `$realtime` | 支持 | 已 production 接入 | body expr ABI 有 `READ_TIME` | `$temperature/$vt` 未进 Rust body ABI |
| `$temperature` / `$vt` | 支持 | Rust EVAS2 缺口 | Py backend 会转换温度表达式；Rust body expr 不接受这些 special identifiers | 增加 temperature param slot 或 Rust global simulation context |
| `if/else` | 支持 | 已 production 接入受限 subset | body stmt ABI 有 `IF/ELSE/ENDIF`，也支持部分 select lowering | 条件引用并修改同一 state 时只接受 order-safe 形态 |
| `case` | 支持 | Rust EVAS2 缺口 | release non-candidate 有 `case_statement` 2 次 | 可先 lower 成 ordered if-chain，再做 parity |
| `for` loop | 支持 | 部分 production 接入 | 静态 bounded for 可 unroll | 动态 bound/update 或 loop body 改 loop var 仍拒绝 |
| `while` loop | 支持 | Rust EVAS2 缺口 | release non-candidate 有 `while_loop` 2 次 | 需要 bounded runtime loop ABI，或对可证明有限的 while 做 compile-time transform |
| `initial_step` | 支持 | 已 production 接入 | event due ABI 支持 `initial_step` | 与 `final_step` 不同，initial 已可进入 RustSimProgram |
| `cross(expr, dir, ttol, vtol)` | 支持 | 部分/production 接入 | event due ABI 支持 cross expr、direction、ttol/vtol | full detector correctness 需 release strict run；dynamic indexed expr 仍依赖 expr lowering |
| `above(expr)` | 支持 | 部分/production 接入 | event due ABI 支持 above | 同 cross，需要 release strict run 验证 |
| `timer(start)` state-owned absolute timer | 支持 | 已 production 接入受限 subset | event due ABI 支持 typed start expr，测试覆盖 state-owned timer rearm | 动态复杂 body 和 mixed event queue 仍是风险 |
| `timer(start, period)` periodic timer | 支持 | 部分 production 接入 | periodic timer 要求 start/period 不读 node/state | 动态 period 或 state-dependent periodic timer 仍拒绝 |
| combined event | 支持 | 部分 production 接入 | schedule IR 能展开 combined trigger | 真实 mixed timer/cross queue 的全局排序仍需 release strict run 证明 |
| event body scalar assignment/output write | 支持 | 已 production 接入受限 subset | ordered body ops 支持 state write、single-node output write、if/static-for | array target、case/while、file/random side effect 仍拒绝 |
| `transition()` state evolution / breakpoint | 支持 | 已 production 接入受限 subset | Rust transition typed state + breakpoint loop | 与 event/body/source/record 的 whole-loop correctness 已有 targeted tests，但还没有 full release PASS |
| `bias + scale * transition(...)` | 支持 | 已 production 接入 | transition runtime 支持 direct/scaled/bias decomposition | 多 transition 复杂组合仍要逐类验证 |
| `$bound_step(expr)` | 支持 | 已 production 接入受限 subset | body stmt ABI 有 `BOUND_STEP`，Rust loop clamp `dt` | 只覆盖可编码 numeric expr；全局 adaptive err-ratio 与 dirty snapshot 仍未作为完整科学误差控制 claim |
| `$display/$strobe` | 支持 | Rust 中按 waveform no-op 处理 | body stmt encoder 把 `$display/$strobe` 视作 no-op | 如果后续需要日志 side effect，需新 side-effect ABI；目前只保证波形语义 |
| `$fopen/$fwrite/$fdisplay/$fclose` | Py 支持 | Rust EVAS2 缺口 | release non-candidate 有 `$fopen` 3 次、`$fwrite` 3 次 | 需要文件 side-effect ABI，或把 metric writer 改成 Rust-owned structured metric output |
| `$random/$rdist_normal/$dist_uniform` | Py 支持 | Rust EVAS2 缺口 | release non-candidate 有 `$rdist_normal` 3 次；Rust body expr 不接受系统随机函数 | 需要 deterministic RNG state schema，保持 Py/Spectre-compatible seed 语义 |
| `final_step` | Py 支持 | Rust EVAS2 缺口 | release non-candidate 有 `event_due_not_lowered` 2 次，对应 `final_step_file_metric_ref` | 需要 Rust loop 结束阶段执行 final-step body，并处理 file/metric side effects |
| child model / hierarchical behavioral composition | Py 支持部分 runtime 结构 | Rust EVAS2 未完整接入 | lowerer 仍有 `child_models_not_lowered` gate | 需要把多 model 实例的 state/node/event queue 合并成同一个 program schema |
| record / trace | 支持 | 部分 production 接入 | RustSimRecord 有 node-id record；runner/CSV 仍主要 Python | 核心语义可记录，但 E2E speed 要继续做 sparse trace + CSV array path |
| CSV/checker/runner | 支持 | 不属于 Rust 内核全量迁移 | 外层仍 Python | 影响 E2E wall，不应该混入“核心语义 Rust 化完成度” |

## 当前 Rust EVAS2 缺口归并

按 22 个 compile-ok 但 `RustSimProgram` non-candidate 文件归并：

| 缺口类别 | 触发次数 | 代表文件/任务 | 为什么重要 |
|---|---:|---|---|
| event body 未 lower | 19 | `converter_static_linearity_measurement_flow.va`、`sar_adc_weighted_8b.va`、`file_metric_writer.va`、`noise_gen_ref.va` | 这是 remaining Rust 化最大类，直接阻塞 strict Rust EVAS2 |
| 普通/复杂连续贡献未 lower | 14 | `sar_adc_weighted_8b.va` | 会影响 converter/SAR 类真实电路行为 |
| 连续 body 未 lower | 8 | `dwa_ptr_gen.va`、`noise_gen.va` | 说明还有非 event 的 ordered state/output 逻辑没有全收进去 |
| event body 数组写目标 | 6 | `sar_adc_weighted_8b.va` | 动态/数组状态是数字控制模型常见结构 |
| 非数值字面量/字符串 | 6 | `file_metric_writer.va` | 多和 file/metric side effect 绑定 |
| `$fopen/$fwrite` 文件 side effect | 3 + 3 | `file_metric_writer.va` | measurement-heavy benchmark 会用到 |
| `$rdist_normal` 随机函数 | 3 | `noise_gen_ref.va` | source/noise 类 benchmark 会用到 |
| `case` | 2 | `converter_static_linearity_measurement_flow.va` | 可 lower 成 if-chain，是 P0 可补项 |
| 动态数组读/索引 | 2 | `sar_adc_weighted_8b.va` | 需要真正 typed array runtime |
| `while` | 2 | `cppll_timer_ref.va` | 需要 bounded loop 或专门 loop ABI |
| `final_step` event due | 2 | `final_step_file_metric_ref.va` | 结束阶段 metric/file 行为无法由 Rust 拥有 |

按 task 类别看，non-candidate 集中在：

| 类别 | non-candidate 文件数 |
|---|---:|
| `SUP02_stimulus_and_source_generators` | 6 |
| `CT06_calibration_dem_and_control` | 5 |
| `SUP01_measurement_instrumentation_flows` | 5 |
| `CT01_data_converter_models` | 4 |
| `CT05_pll_clock_and_timing_systems` | 2 |

## 审计结论

1. **现在不能声明“Py EVAS 已经全量 Rust 化”。** 最可量化的静态结论是：当前 release compile-ok gold `.va` 中，`326/348 = 93.7%` 可以被 `RustSimProgram` 静态接受；剩余 `22/348 = 6.3%` 是真实 Py-supported Rust 缺口。
2. **也不能仅凭这张表声明 Rust EVAS2 release-wide PASS 或速度提升。** 本表是静态 capability audit，不跑仿真、不跑 checker、不比较 Spectre。
3. **当前缺口不是“Rust 不能跑 Verilog-A”，而是若干 Py 语义还没有进入统一 Rust program schema。** 最高优先级是数组动态读写、普通差分/复杂连续贡献、case/while、final_step、文件 side effect、随机函数。
4. **最值得继续做的是全局语义补齐，不是 benchmark 特例 fastpath。** 这些缺口对应的是 Py EVAS1.0 的通用语义类别，补完后才能合理讨论 strict Rust EVAS2 release-wide run。

## 下一步修复顺序

P0：先补能直接减少 22 个 non-candidate 的通用语义。

1. 普通连续贡献扩展：支持 `V(out, ref) <+ expr`、indexed/static target、SAR 类贡献表达式。
2. typed array runtime：支持 event body 中数组读、数组写、动态下标 bounds check。
3. `case` lowering：先转成 ordered if-chain，和 Py waveform 做 parity。
4. `while` lowering：只接受可证明 bounded 的 while；否则显式 unsupported。
5. `final_step`：在 Rust loop 结束阶段执行 final-step body。
6. deterministic RNG：迁 `$random/$dist_uniform/$rdist_normal`，保留 seed/state。
7. side-effect ABI：至少支持 file metric writer 所需的 `$fopen/$fwrite/$fclose`，或转成 Rust structured metric output。

P1：补完 P0 后做 strict Rust EVAS2 release run。

- 用 `evas_engine=evas2` 跑真实 benchmark，不允许 Python fallback。
- 输出每个 row 的 supported/pass/fail/reject reason。
- 只有 checker PASS 后，才把静态 candidate 变成 correctness coverage。

P2：再讨论速度。

- 在同一机器、同一 row slice 上比较 Py EVAS1.0、Rust EVAS2、Spectre AX、Spectre classic。
- 核心速度表必须分开 `simulator subprocess wall` 和 `E2E wall`。
- CSV/checker/runner 只作为 E2E 优化，不混入“核心 Rust 内核语义覆盖”。
