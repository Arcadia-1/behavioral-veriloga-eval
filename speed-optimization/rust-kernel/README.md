# EVAS Rust Kernel Optimization

> **当前 active worklist**：`RUSTIFICATION_WORKLIST_20260606.md`（覆盖 001-103；2026-06-05 → 2026-06-06 会话完成 086-103 + Stage 6 commit hygiene + handoff to codex for 094 multi-week project；097 编号在 096 文档中作为 slowdown root-cause 语义预留，当前未落文档）。
>
> **Codex 接 094 项目起点**：`HANDOFF_TO_CODEX_094_PROJECT.md`（self-contained 342 行 handoff doc，含 7 critical rules + 5-session execution plan + pitfalls list）。
>
> **当前最快已验证状态**：`profile_fast_rust_55`。证据是 075/076：top-wall 10 EVAS-only `profile_fast` `13.264s` -> `profile_fast_rust_55` `3.250s`，`10/10` safe vs strict EVAS，相对 normal fast 为 `4.08x`。后续 103/104/094q 等 event-transition/094 wrapper 尝试属于 correctness/diagnostic 或负优化，不能替代这个速度基线。
>
> **EVAS2 当前定位**：`profile_fast_evas2` 是 strict Rust whole-segment coverage gate。命中 whole-segment Rust 才算可跑；未命中必须显式 unsupported，不能把 Python fallback 混成 Rust 覆盖率。负优化和禁用路线见 `RUST_NEGATIVE_ATTEMPT_STOPLIST_20260605.md`。
>
> **EVAS2 覆盖扩展计划**：`EVAS2_WHOLE_SEGMENT_COVERAGE_PLAN_20260605.md` + `audits/108-rust-owned-simulation-loop-first.md`。108 后主线纠正为 Rust-owned simulation loop first：Python 负责 parse/lower/runner 兼容，Rust 拥有 transient scheduler、source、event、evaluate、transition、breakpoint、record 和 final state；不要继续把窄 fastpath 堆叠当成全量 Rust 化。
>
> **108-112 当前实装状态**：已完成 `RustSimProgram` schema、source+record no-model Rust-owned loop、continuous evaluate/state/output write 子集，并把支持边界内的 `initial_step`/`cross`/`above` event due、ordered event body、`transition()` output/breakpoint、`$bound_step` next-dt clamp、static bus/bitwise expression、fixed-loop state array、direct continuous contribution、以及 `bias + scale * transition(...)` 合入同一个 RustSimProgram production loop。112 selected-5 diagnostic 从 `3/5` 提升到 `5/5` PASS；这证明组合语义迁移有效，但样本仍很小，不能 claim 全量 Rust 化、release-wide speedup 或快于 Spectre AX。
>
> **P0/P1 当前收口入口**：`EVAS2_P0P1_CLOSEOUT_20260606.md` + `EVAS2_CURRENT_ARTIFACT_INDEX_20260606.md`。当前 release-row 可用性是 271/271 PASS；语言/架构层面仍不能 claim 100% Rust 化，也不能 claim paper-facing 快于 Spectre AX。

这个目录记录 EVAS 内核 Rust 化和 indexed 化的长期改造过程。它不是论文速度结论本身，而是解释“为什么这样改、改了什么、改前改后如何验证、下一步怎么走”的工程审计入口。

机器可读的行为映射种子在 `behavior-coverage-map.v1.json`。它记录 B01-B18 当前对应的 Rust ABI / shadow / fallback / correctness gate 状态，供后续 per-model manifest 生成器复用。

## 读文档的顺序

| 顺序 | 文档 | 状态 | 作用 |
|---|---|---|---|
| 000 | `audits/000-rust-kernel-design.md` | active | 统一 Rust 化目标、原理、风险和学习路线 |
| 001 | `audits/001-indexed-sidecar-and-rust-smoke.md` | done | 记录当前 checkpoint：indexed sidecar、Rust toy kernel、覆盖 manifest |
| 002 | `audits/002-python-indexed-ir-parity.md` | done | 增加 opt-in Python indexed IR/parity harness，验证 lowering 不改变结果表达 |
| 003 | `audits/003-python-indexed-voltage-snapshot.md` | done | 增加 opt-in indexed snapshot profile，量化 dict copy、Python sidecar 和纯数组 snapshot 差异 |
| 004 | `audits/004-python-indexed-kernel-arrays.md` | done | 增加 opt-in persistent indexed voltage array，让 source/record/err_ratio 低风险路径开始消费 array mirror |
| 005 | `audits/005-indexed-model-io-boundary.md` | done | 增加 per-model IO node-id plan，把 mapped ports、outputs 和 `@parent:` 层次映射显式编号 |
| 006 | `audits/006-indexed-model-output-write-through.md` | done | 让 `_set_output()` 在 opt-in indexed path 下 write-through 到 array mirror，并用 repair stats 守住绕行路径 |
| 007 | `audits/007-indexed-model-input-read-probe.md` | done | 给 `_get_voltage()` 增加 opt-in input-read probe，只比较普通读的 dict/array 值，不改变返回值 |
| 008 | `audits/008-indexed-non-event-voltage-read.md` | done | 让 `_get_voltage()` 的 non-event 普通输入读在 opt-in indexed path 下从 array mirror 返回，event 插值路径保持原样 |
| 009 | `audits/009-indexed-model-evaluate-profile.md` | done | 增加显式 `EVAS_PROFILE_MODEL_EVAL` per-model timing，用于后续判断 evaluate、timer、event 哪条热路径优先优化 |
| 010 | `audits/010-post-update-empty-scan-fastpath.md` | done | 利用编译期 post-update event flag，跳过静态模型每步必然为空的 `post_update_events()` 调用 |
| 011 | `audits/011-timer-breakpoint-scan-profile.md` | done | 汇总 source/model/bound_step scan 调用规模和模型级 timer cache counters，给后续 event/timer 优化提供证据 |
| 012 | `audits/012-profile-guided-kernel-sample.md` | done | 用本地 bundled examples 做 profile-guided sample，结论是当前样本优先继续 model evaluate/indexed/Rust 路线 |
| 013 | `audits/013-node-resolution-run-cache.md` | done | 在 run 周期内缓存 local node 到 external node 的解析结果，减少 mapped read/write 和 `@parent:` 路径重复 dict/string 开销 |
| 014 | `audits/014-model-io-profile-counters.md` | done | 新增 opt-in model IO counters，量化 examples 中普通 `V(node)` read/output write 调用密度，指导下一步 node-id/Rust lowering |
| 015 | `audits/015-static-branch-io-node-id-plan.md` | done | 给 compiled model 增加静态 branch IO metadata，并把 static/event/dynamic IO 边界接入 indexed model IO node-id plan |
| 016 | `audits/016-static-branch-fast-helper-prototype.md` | done | 新增 opt-in static branch fast helper codegen，验证普通静态 `V(node)` read/write lowering 的局部速度潜力 |
| 017 | `audits/017-static-branch-node-id-direct-array.md` | done | 让 opt-in static branch fastpath 在 indexed arrays 下直接读写 node-id array slot，进一步减少 Python string/dict/object 开销 |
| 018 | `audits/018-event-interpolation-ir-boundary.md` | done | 显式拆分 event trigger read 和 event body read 的 node-id metadata，保护 crossing-time interpolation 语义 |
| 019 | `audits/019-dynamic-bus-lowering-prototype.md` | done | 为 `V(bus[i])` / `V(bus[i][j])` 建立 role/base/dimension/context metadata，作为 bus base+offset lowering 前置 IR |
| 020 | `audits/020-indexed-model-state-arrays.md` | done | 为 scalar state 和 array state 建立 indexed layout metadata，作为 Rust model-evaluate ABI 的 state 侧准备 |
| 021 | `audits/021-rust-model-evaluate-abi-prototype.md` | done | 新增 Rust `model-abi` prototype kernel，验证 node/state id ABI 可以驱动 native `Vec<f64>` evaluate loop |
| 022 | `audits/022-rust-ffi-batch-evaluate-boundary.md` | done | 新增零依赖 Rust `cdylib` 和 Python `ctypes` loader，建立 production 可调用的 static affine batch ABI |
| 023 | `audits/023-dynamic-bus-runtime-codegen-fix.md` | done | 把 dynamic bus 节点名生成改成 helper，修复 state-index 表达式可能生成非法 nested f-string 的风险 |
| 024 | `audits/024-compiled-model-rust-replay-smoke.md` | done | 用真实 parser/compiler/simulator/netlist 路径上的临时 static affine 模型验证 Rust replay |
| 025 | `audits/025-production-opt-in-rust-backend-channel.md` | done | 接入 `EVAS_RUST_STATIC_EVAL` / `evas_rust_static_eval=true` 和 Rust runtime counters |
| 026 | `audits/026-opt-in-static-continuous-model-rust-eval.md` | done | 完成 opt-in static affine model Rust evaluate；功能正确，但 microbenchmark 暴露 per-model FFI 小调用导致变慢 |
| 027 | `audits/027-rust-consecutive-model-segment-batch.md` | done | 把连续 eligible static affine models 合成 per-step segment batch，Rust FFI calls 从 `64064` 降到 `1001` |
| 028 | `audits/028-rust-output-node-sync-deferral.md` | done | 每步保留 `node_voltages` 同步，但把 `output_nodes` 写入延迟到 final 前，减少 Python object 写入 |
| 029 | `audits/029-indexed-dirty-validation-fastpath.md` | done | 全 Rust static segment 下用预计算 dirty node tuple 替代冗余全量 indexed validation |
| 030 | `audits/030-segment-lifecycle-fastpath.md` | done | Rust static segment 成功时跳过 compiler-proven 空 lifecycle bookkeeping，fallback 仍走原 Python 生命周期 |
| 031 | `audits/031-runtime-parameter-affine-lowering.md` | done | 支持 parameter-only coefficient expression，在 instance override 后求值再进入 Rust static segment |
| 032 | `audits/032-dynamic-bus-base-offset-lowering.md` | done | dynamic bus read/write 经过 base/index resolver cache，减少重复节点字符串构造 |
| 033 | `audits/033-indexed-state-runtime-storage.md` | done | 新增 opt-in indexed state runtime mirror，为后续 Rust state ABI 准备 scalar/int/array slots |
| 034 | `audits/034-static-lifecycle-fastpath.md` | done | profile-driven 大瓶颈优化：静态模型默认跳过空 `_prepare_step()` 和 timer expire 生命周期维护 |
| 035 | `audits/035-state-local-and-static-branch-real-slice-verification.md` | done | 在真实 top-wall 10 上验证 state-local/static-branch/voltage guard，结论是 state-local 不应默认开启，static-branch 只有约 1% 混合收益 |
| 036 | `audits/036-transition-unchanged-target-fastpath.md` | done | 把 transition target/参数不变时的 no-op reset 做成 opt-in fastpath；局部 `_transition` 调用减少，但 top-wall 10 没有稳定总收益，因此默认关闭 |
| 037 | `audits/037-static-linear-evaluate-ir-b1-b4.md` | done | 把 Rust static affine 扩展成 static linear evaluate IR，覆盖多输入 expression/contribution 和简单 scalar state 读写 |
| 038 | `audits/038-static-linear-fast-sync.md` | done | 全模型 Rust static segment 下跳过 per-step dict sync/validation；Rust-covered chain 到 `1.3x-1.5x`，但当前 top-wall 10 无 Rust coverage |
| 039 | `audits/039-rust-coverage-expansion-for-real-models.md` | done | 扩展真实模型 evaluate IR 覆盖到 initial-step no-op 和 top-level 条件线性/state assignment，并记录 top-wall 10 仍被 event/state array/dynamic bus/transition 阻塞 |
| 040 | `audits/040-rust-mixed-small-segment-gate.md` | done | 给 Rust fast-sync speed mode 增加 small mixed-segment gate，避免 partial Rust coverage 拖慢真实 top-wall 诊断 |
| 041 | `audits/041-transition-real-topwall-profile-and-fastpath.md` | diagnostic | 针对真实 top-wall transition/event 模型增加 differential transition-output fastpath、active transition breakpoint set 和 transition counters，验证覆盖有效但 wall 收益仍不稳定 |
| 042 | `audits/042-integer-state-transition-target-and-breakpoint-array-scan.md` | done | 把 integer scalar state 纳入 Rust static-linear IR，记录 transition target IR，并新增 Rust array transition-breakpoint scan hook |
| 043 | `audits/043-transition-target-executor-and-timer-array-scan.md` | done | 把 transition target IR 推进到 Python/Rust array executor，并把 timer breakpoint scan 接到 Rust ABI 和 simulator hook |
| 044 | `audits/044-ordered-transition-shadow-and-timer-array-sidecar.md` | done | 把 static-linear evaluate 和 transition target evaluate 放进同一个 Rust ordered shadow batch，并让 Rust timer scan 复用 typed array sidecar |
| 045 | `audits/045-rust-required-rejection-and-if-lowering.md` | diagnostic | 增加 Rust static-evaluate no-candidate rejection counters，并验证 simple `if/else` lowering 正确但尚未解锁 top-wall Rust speedup |
| 046 | `audits/046-fixed-index-state-array-ir.md` | done | 把固定下标 state array 元素扁平化进 Rust static-linear state slots，动态数组下标继续拒绝 |
| 048 | `audits/048-python-to-rust-behavior-map.md` | done | 方向重置：停止零散 Rust 前置补丁，先建立 Python 仿真行为到 Rust primitive / fallback / parity gate 的总映射 |
| 049 | `audits/049-behavior-coverage-manifest.md` | done | 把 B01-B18 映射落成可审计 manifest 口径，区分 production、shadow、partial、Python fallback 和 claim gate |
| 050 | `audits/050-transition-state-rust-primitive.md` | done | 为 B08 `transition()` state evolution 增加 Rust typed-array primitive，并接入 `rust_transition_shadow` 做 state parity；engine production path 尚未接入 |
| 051 | `audits/051-timer-step-rust-primitives.md` | done | 为 B11 periodic/absolute timer due/reschedule 增加 Rust typed-array primitives 和 Python-oracle parity tests；event body/lifecycle 尚未接入 |
| 052 | `audits/052-cross-above-detector-rust-primitives.md` | done | 为 B09 `cross()` / `above()` detector state 增加 Rust typed-array primitives 和 Python-oracle parity tests；event body/order/interpolation 仍由 Python 拥有 |
| 053 | `audits/053-record-node-id-array-path.md` | done | 为 B15 record path 增加 indexed node-id array 读取；CSV schema、SimResult 和 checker contract 不变，Rust record ABI 尚未实现 |
| 054 | `audits/054-dynamic-bus-offset-rust-primitive.md` | done | 为 B17 bounded 1-D/2-D dynamic bus access 增加 Rust base+offset node-id primitive；compiler/runtime 生产路径仍未接入 |
| 055 | `audits/055-event-lifecycle-production-gate.md` | diagnostic | 明确 B10 event body 和 B18 lifecycle 共享 phase-order correctness gate，不能并行硬切 production；下一步应做 event trace/order/write-set shadow |
| 056 | `audits/056-event-due-shadow.md` | done | 增加 opt-in Rust event due shadow，在真实 `_check_cross/_check_above/_check_timer*` 入口旁验证 Rust/Python due-state parity；不改变生产 event body |
| 057 | `audits/057-event-trace-write-set-audit.md` | done | 增加 opt-in event trace/write-set audit，记录 event firing/body entry 和 state/array/output/timer/transition 写入，为 event/evaluate Rust production batch 定边界 |
| 058 | `audits/058-event-body-write-set-rust-batch.md` | done | 用 top-wall audit 选择最高频 gated LFSR shift/XOR event body，lowering 到 Rust batch；shadow 2000/2000 match，production opt-in 10/10 safe_vs_strict，但 top-wall 总收益仍约 `1.009x` |
| 059 | `audits/059-timer-event-production-gate.md` | done | 验证 per-check timer Rust FFI 在 CPPLL length-1 timer 上会变慢，增加小集合 gate，并瘦身 Python timer hot path；下一步应做 compiler-level timer batch |
| 060 | `audits/060-static-timer-event-segment-batch.md` | done | 把连续 static timer event 编译成一次 due-mask batch，event body 仍按源码顺序执行；top-wall 10 暂未触发该 batch，下一步转向 `timer(next_t)` state-owned absolute timer |
| 061 | `audits/061-state-owned-absolute-timer-fastpath.md` | done | 对 CPPLL/ADPLL 这类 `timer(t_next_toggle)` owner chain 增加保守 fast path，top-wall 命中 180956 次检查、160486 次 skip；仍是 EVAS-only candidate evidence |
| 062 | `audits/062-fused-timer-lfsr-output-batch.md` | done | 把 periodic timer due/reschedule、LFSR event body、output node write 和 output hold 降成一个 opt-in Rust batch；smoke parity PASS，fused calls 16、due/executed/writes 各 4，fallback 0；尚未做 top-wall speed claim |
| 063 | `audits/063-prbs7-whole-model-rust-fastpath.md` | done | 对真实 PRBS7 top-wall 模型做 whole-model Rust trace batch；单行 kernel/tran wall `0.2156s -> 0.0085s` 约 `25.4x`，但 top-wall 10 总收益仅 `1.006x`，因为当前只覆盖这一行 |
| 064 | `audits/064-compiler-driven-whole-segment-lowering.md` | done | 把手写 PRBS7 fastpath 泛化为 compiler-emitted whole-segment lowering，并覆盖 CPPLL/SAR/prop-delay/gain 四类热模型；4-row sequential runner 4/4 PASS，E2E `9.999s -> 6.819s`，tran `5.657s -> 0.451s` |
| 065 | `audits/065-semantic-dataflow-whole-segment-matching.md` | done | 把 whole-segment candidate 从端口/状态 exact-name gate 改成语义和数据流匹配；修复 CPPLL supply direction 反向风险，top4 smoke 4/4 PASS |
| 066 | `audits/066-release-wide-rustification-workplan.md` | active | 把后续 Rust 化整理成 release-wide workstreams：先做全量 coverage manifest，再做 whole-segment Rust ABI、evaluate IR、event/timer/transition production 和 release gate |
| 067 | `audits/067-release-rust-coverage-manifest-generator.md` | done | 新增 release-wide Rust coverage manifest，357/357 gold `.va` compile pass；同时收紧 `weighted_dac_v1` 语义 matcher，候选从 13 降到 2，避免状态机误命中 |
| 068 | `audits/068-whole-segment-rust-abi-contract.md` | done | 新增 whole-segment candidate ABI contract validator；release 报告显示当前 23 个候选 invalid count 为 0，后续 production Rust 有了字段/类型 gate |
| 069 | `audits/069-topwall-gain-timer-production-rust.md` | done | 把 `gain_timer_reduction_v1` whole-segment trace loop 接到 production Rust ABI；`vbr1_l1_gain_estimator` tb/e2e 3-repeat PASS，EVAS tran 约 `3.3x` 快于 normal fast |
| 070 | `audits/070-propagation-delay-production-rust.md` | done | 把 propagation-delay comparator whole-segment trace loop 接到 production Rust ABI；top-wall dut 3-repeat PASS，E2E wall 约 `3.57x`、EVAS tran 约 `146x` 快于 normal fast |
| 071 | `audits/071-sar-loop-production-rust.md` | done | 把 weighted SAR ADC/DAC/sample-hold loop 接到 production Rust ABI；tb/e2e 3-repeat PASS，tb E2E wall 约 `1.27x`、EVAS tran 约 `28.9x` 快于 normal fast |
| 072 | `audits/072-stage55-cppll-rust-trace-and-lean-production-mode.md` | done | 把 CPPLL reacquire trace fill 接到 Rust ABI，并新增 lean `profile_fast_rust_55`；top-wall 10 EVAS-only 10/10 PASS，总 wall `12.78s -> 5.17s`，stage weighted coverage `80.6%` |
| 073 | `audits/073-rust-speed-claim-gate.md` | done | 新增 claim gate，把 stage55、full release Rustification、Spectre AX speed 三个 claim 分开判定；当前只允许 EVAS-only stage claim，full Rustification 和 AX speed claim 仍关闭 |
| 074 | `audits/074-rust55-topwall-evas-smoke.md` | done | 按阶段节奏重跑 EVAS-only top-wall smoke；6 个 unique row 上 Rust55 总 wall `9.030s -> 3.750s` 相对 normal fast 为 `2.41x`，未命中的 gain/PFD 仍回到 Python fast |
| 075 | `audits/075-gain-measurement-flow-production-rust.md` | done | 把 gain extraction measurement flow 的 `vin_src+lfsr+dither+gain_amp` 整段 trace 接到 production Rust；top-wall 6 EVAS-only 总 wall `9.677s -> 2.103s`，Rust55 相对 normal fast 为 `4.60x` |
| 076 | `audits/076-current-rustification-status-after-gain-flow.md` | done | 重新跑当前 top-wall 10：Rust55 10/10 safe_vs_strict，总 wall `13.264s -> 3.250s` 相对 normal fast 为 `4.08x`；release-wide Rustification 仍是 `30.0%`，未完成全量 Rust 化 |
| 077 | `audits/077-whole-segment-record-trace-copy-reduction.md` | done | 清理 whole-segment Rust trace 的一次中间 list/ndarray 往返；top-wall fast+Rust55 smoke 10/10 PASS，但收益不稳定，不作为速度 claim |
| 078 | `audits/078-global-evas-timing-split-and-persistent-worker.md` | done | 全局拆分 EVAS runner/subprocess 固定开销，并新增 opt-in persistent worker；2-row same-runner smoke E2E `2.764s -> 1.440s`，10-row worker smoke 10/10 PASS |
| 079 | `audits/079-required-signal-global-trace.md` | done | 将 checker required-signal contract 下发到 EVAS sparse trace；current-code trace on/off top-wall 10 均 10/10 PASS，E2E `2.527s -> 2.024s`，CSV write `0.519s -> 0.404s` |
| 080 | `audits/080-evaluate-ir-piecewise-and-rust-timer-batch.md` | done | 扩展 evaluate IR 到 `abs/min/max` piecewise-linear lowering，并把连续 static timer segment 的 due-mask 接到 Rust batch production；targeted EVAS tests 全部通过 |
| 081 | `audits/081-event-body-linear-rust-batch.md` | done | 把 `cross/above/timer` 触发后的简单 state assignment body lowering 到通用 Rust static-linear batch；due/order/interpolation 仍由 Python 拥有 |
| 082 | `audits/082-timer-static-linear-whole-segment-rust.md` | done | 把 periodic timer due、static-linear event body、static-linear output evaluate 和显式 record trace/timer breakpoint 合成一个 Rust whole-segment executor |
| 083 | `audits/083-record-node-id-rust-abi.md` | done | 把 indexed record path 的 node-id value gather 迁到 Rust ABI；SimResult/CSV/checker 外层仍由 Python/harness 拥有 |
| 084 | `audits/084-multi-timer-static-linear-event-queue-rust.md` | done | 把多个 periodic timer 的 due/order/static-linear event body/evaluate/record 合成 Rust queue segment |
| 085 | `audits/085-cross-above-transition-default-adaptive-trace.md` | done | `cross()/above()` event-time interpolation cache 接入 Rust ABI；`transition()` state typed-array opt-in production；timer static-linear Rust fastpath 支持默认 adaptive/internal trace |
| 094 | `audits/094-verilog-a-body-rust-kernel-design.md` | planned | 设计多 audit 项目：把 generated Verilog-A `model.evaluate()` body lower 到 Rust kernel，避免继续做 per-call 小 FFI |
| 094a | `audits/094a-expression-ir.md` | done | 新增通用 expression IR foundation；234 个 generic candidate 的 8156 个 analog body expression roots 全部 lower + emit compile 通过 |
| 094b | `audits/094b-statement-ir.md` | done | 新增 statement IR foundation；234 个 generic candidate 的 analog block 全部 lower + Python body emit compile 通过 |
| 094c | `audits/094c-schedule-ir.md` | done | 新增 event schedule IR foundation；`cross/timer/initial/final/combined` 事件结构可被后续 Rust executor 消费 |
| 094d | `audits/094d-state-binding-ir.md` | done | 新增 state/parameter/port binding IR；234 个 generic candidate 的 expression identifiers 全部可解析到稳定 slot |
| 094e | `audits/094e-rust-abi.md` | done | 新增 synthetic Rust body IR ABI 和 Python ctypes wrapper；100 组随机 state-write IR 与 Python oracle 一致，生产 dispatch 未接入 |
| 094f | `audits/094f-body-ir-encoder.md` | partial | 把 `ExprIR` / `BindingTableIR` 的标量表达式和 ordered state/output write-set 编码成 094e Rust body ops；event scheduler 和 production dispatch 未接入 |
| 094g | `audits/094g-event-body-program.md` | partial | 把单个 `EventStatementIR` 绑定到 Rust-executable body write-set，并新增 standalone trigger expression eval ABI；due/order scheduler 和 production dispatch 未接入 |
| 094h | `audits/094h-event-due-program.md` | partial | 把 `initial_step`、simple `cross/above`、static `timer` trigger 编成 Rust expression batch input；fired-index/order scheduler 和 production dispatch 未接入 |
| 094i | `audits/094i-mixed-event-due-runtime.md` | partial | 新增 shadow-only mixed due runtime，把 trigger expression batch 接到 Rust cross/above/timer primitives 并返回源码顺序 fired indices；event body dispatch 未接入 |
| 094j | `audits/094j-event-statement-shadow-dispatch.md` | partial | 新增 single event-statement shadow runtime：任一 trigger fired 时执行一次 Rust body batch；多 event statement / production engine 未接入 |
| 094k | `audits/094k-analog-block-event-shadow-dispatch.md` | partial | 新增 analog-block event shadow runtime：多个 event statement 同步 fired 时按源码顺序执行 Rust body batch；continuous statement / production engine 未接入 |
| 094l | `audits/094l-pipeline-stage-control-flow-body-batch.md` | partial | 在真实 `pipeline_stage` 控制流上验证 if/else body lowering；仍是 shadow/round-trip，不接 production |
| 094m | `audits/094m-event-only-runtime-builder.md` | partial | 为真实 analog block 构建 event-only Rust runtime；continuous contribution、scheduler、CSV 仍由 Python 拥有 |
| 094n | `audits/094n-transition-contribution-runtime.md` | partial | direct `transition()` voltage contribution 可走 Rust transition state primitive，并暴露 `next_breakpoint()` runtime API |
| 094o | `audits/094o-combined-analog-block-shadow-runtime.md` | partial | event due/body + transition contribution 组合成受限 analog-block shadow runtime；仍不接默认 engine |
| 094p | `audits/094p-real-row-shadow-replay-gate.md` | done | `pipeline_stage` reference time/source grid replay max abs diff `4.86e-8`；证明核心语义可行，但不是 E2E speed claim |
| 094q | `audits/094q-opt-in-full-sim-wrapper.md` | blocked | prototype full-sim wrapper time-aligned close，但 wall `3.219s` vs Python `1.453s` 且 rowwise 不 close；不能 direct wire engine |
| 094r | `audits/094r-engine-dispatch-contract-and-no-default.md` | done | 固化 engine dispatch contract 和 `NO_DEFAULT_ENGINE_DISPATCH` 决策 |
| 094s | `audits/094s-persistent-typed-array-engine-slice.md` | done | bound indexed-array replay 相对 dict-pack `1.137x`，说明 node direct binding 有用但不是大瓶颈全部 |
| 095 | `audits/095-generic-executor-record-adaptive-substeps.md` | done | 修复 091d generic executor 漏记 adaptive substep 的 parity 问题；速度仍有约 `10.3x` geomean，但记录成本增加 |
| 096 | `audits/096-transition-production-real-release-sweep.md` | done | 真实 release sweep 证明 `rust_transition_production` 在 75 行中 74 行变慢，建议降级为 experimental/off-by-default |
| stoplist | `RUST_NEGATIVE_ATTEMPT_STOPLIST_20260605.md` | active | 标记 026/035/036/045/046/059/062/089/094q/096/103/104 等无效或负优化路线；当前速度回退口径固定为 `profile_fast_rust_55` |
| evas2-plan | `EVAS2_WHOLE_SEGMENT_COVERAGE_PLAN_20260605.md` | active | 定义 EVAS2 runnable、coverage expansion workstreams 和 strict production gate；从 planner-core `231/348` 目标池扩 whole-segment runtime |
| 098 | `audits/098-current-rust-coverage-and-body-ir-production.md` | done | 完成 P0 当前 Rust 覆盖审计和 P1 094 body-IR opt-in production hook；release 348 个 compile-ok `.va` 中当前 body-IR candidate 为 0，不能当速度 claim |
| 099 | `audits/099-body-ir-rejection-taxonomy.md` | done | 把 P0 拒绝原因拆成多标签 taxonomy；release blockers 主要是 `transition_expr` 344、event statement 321、complex if/write-set 172，下一步应做 event-transition ordered segment planner |
| 100 | `audits/100-event-transition-coverage-estimator.md` | done | 新增 event+transition ordered segment 静态 estimator；保守 core 预计 `255/348`，ordered V1 预计 `268/348`，带 side-effect boundary 上限 `338/348` |
| 101 | `audits/101-event-transition-source-order-planner.md` | done | 新增 source-order planner；release 真实 planner 候选为 core `231/348`、ordered V1 `239/348`、side-effect boundary `288/348`，主要剩余缺口是 event-after-continuous 与 dynamic timer due |
| 102 | `audits/102-compiler-visible-event-transition-plan.md` | done | 把 101 planner 写入 `CompiledModel._event_transition_plan_*` class metadata，并在 engine perf stats 聚合 profile 候选；默认 runtime 行为不变 |
| 103 | `audits/103-event-transition-shadow-runtime.md` | done | 新增 `rust_event_transition_shadow`，真实仿真循环中执行 Rust event-transition shadow；micro smoke `3837/3837` matches、0 mismatch，但 shadow wall 约 `4.52x` slower，属于 correctness gate |
| 104 | `audits/104-event-transition-production-gate.md` | diagnostic | 受限 event+transition production 可跳过 Python evaluate，但仍由 Python outer loop/per-step FFI/sync 拥有；micro smoke 语义正确但 `3.49x` slower，不能作为速度方向 |
| 105 | `audits/105-evas2-strict-rust-engine.md` | done | 新增 `evas_engine=evas2` strict Rust whole-segment 入口；命中 Rust 才算 EVAS2 可跑，未命中显式 unsupported，不再把 Python fallback 混入 Rust 覆盖率 |
| 106 | `audits/106-evas2-event-transition-core-strict-production.md` | done | 把受限 `event + transition()` core 接入 EVAS2 strict full-model dispatcher；命中时跳过 Python `model.evaluate()` hot path，测试验证 strict counters 和 scheduler-drift-bounded parity，但尚不做速度 claim |
| 107 | `audits/107-evas2-native-scheduler-sparse-record.md` | done | 把 W1b `pulse -> cross -> scalar state -> transition(out)` trace 合成单次 Rust scheduler+record ABI；microbench median `0.389472s -> 0.007946s`，相对 106 约 `49.02x`，但仅限该受限形态 |
| 108 | `audits/108-rust-owned-simulation-loop-first.md` | active | 方向纠偏：停止继续扩窄 fastpath，先定义 `RustSimProgram` 和 Rust-owned transient main loop；release 覆盖以 strict Rust EVAS2 能跑真实 row 为准，而不是以局部 primitive 数量为准 |
| 109 | `audits/109-continuous-body-and-slot-remap.md` | done | 把 continuous static-linear body/state/output write 与 source/node/state slot remap 接入 RustSimProgram，作为 strict Rust-owned loop 的第一批真实模型覆盖 |
| 110 | `audits/110-timer-array-rustsimprogram-speed-smoke.md` | done | 扩展 timer/state array 侧 RustSimProgram 覆盖，并生成 selected-12 speed smoke；暴露 output-dependent post-update event 仍阻塞 CDAC 等 row |
| 111 | `audits/111-post-update-phase-and-selected12-speed.md` | done | 为 output-dependent `cross/above` 增加 pre/post event phase 和 post-event refresh；selected-12 safe coverage `6/12 -> 7/12`，safe-subset EVAS-only speedup `6.28x` |
| 112 | `audits/112-composite-event-body-and-scaled-transition.md` | done | 把 ordered if/else、bit shift/bit-not、static bus/index、fixed for-loop state array、`$bound_step`、direct contribution、`bias+scale*transition` 迁入 RustSimProgram；selected-5 strict EVAS2 `3/5 -> 5/5` PASS |
| 114 | `audits/114-full-release-rust-py-spectre-fourway.md` | done | 修复 RustSimProgram file side-effect 差异后，full release 271-row 四路审计：Rust EVAS2 271/271 PASS，Python EVAS fast 271/271 PASS，Spectre AX 271/271 PASS，Spectre strict 267/271 checker PASS；Rust EVAS2 相对 Python fast core wall `3.96x`，E2E wall `1.41x` |
| 115 | `audits/115-auto-row-checker-sparse-trace-contract.md` | done | 将 row-based checker required columns 自动推断成 EVAS sparse trace contract；full release EVAS2 271/271 PASS、fallback 0，E2E wall `69.952s -> 59.418s`，checker wall `54.244s -> 46.245s` |
| 116 | `audits/116-generic-checker-runtime-hot-rows.md` | done | 将 rectifier、stimulus sequencer、window comparator 迁到通用 `CsvCheckerRuntime`，并预留 sparse trace 额外调试列；10-row smoke checker wall `11.618s -> 0.221s`，E2E `16.388s -> 4.349s` |
| 117 | `audits/117-rustsim-while-body-gate.md` | done | 新增 RustSimProgram body IR `while` opcode 和 strict gate blocker 聚合；release gold VA lowering 从 `355/357` 到 `357/357`，CPPLL e2e/tb strict EVAS2 实跑 2/2 PASS、rejections 0 |
| 118 | `audits/118-rustsim-coverage-layering-and-pulse-breakpoint.md` | done | 将 Rust 覆盖率拆成 static lowering/runtime/speed 口径，修复 pulse source breakpoint 浮点边界卡死；top-wall 8 persistent-worker EVAS2 样本 8/8 PASS，相对旧 Python strict EVAS 样本总 wall 约 `133.4x` |
| P0/P1 | `EVAS2_P0P1_CLOSEOUT_20260606.md` | done | 中文收口报告：当前 clean smoke 271/271 PASS，E2E 225.978s、EVAS subprocess 162.884s、checker 54.434s；明确 release 可用性与全语言 Rust 化不是同一 claim |
| sleep | `RUSTIFICATION_SLEEP_WORKLIST_20260603.md` | active | 睡后继续 Rust 化的工作清单，034 后先按 benchmark profile 决定下一步 |
| template | `templates/change-audit-template.md` | active | 后续每个改动都按这个模板写审计 |

## 项目发展历程

| 日期 | 阶段 | 核心结论 | 代码/报告锚点 |
|---|---|---|---|
| 2026-06-02 | speed bottleneck audit | EVAS 慢点分两类：measurement-heavy 是每步成本高；PFD/PLL 是无意义步数多 | `speed-optimization/reports/e2e_wall_unified_full_20260602_r14_core_fastpath_exactrows.*` |
| 2026-06-02 | Rust/kernel feasibility smoke | Rust indexed hot loop 和 event queue toy 显示出足够大的潜在收益，但不能直接当 paper-facing claim | `EVAS/prototypes/rust-kernel-smoke/` |
| 2026-06-02 | migration guardrail | 新 backend 不能缩小 EVAS 当前可仿真能力；16 个 bundled example testbench 进入 capability manifest | `EVAS/evas/examples/backend_migration_capability_manifest.json` |
| 2026-06-02 | rollback checkpoint | 正式大改前保存干净回退点 | EVAS commit `37c451a` |
| 2026-06-02 | Python indexed IR parity | 默认 backend 不变；新增 `EVAS_INDEXED_PARITY=1` 旁路检查，验证 dict waveform 可无损 lowering/round-trip 为 indexed trace | `EVAS/evas/simulator/indexed.py` |
| 2026-06-02 | Python indexed snapshot profile | 默认 backend 不变；新增 `EVAS_INDEXED_SNAPSHOT_PROFILE=1`，证明 Python sidecar 不是加速终点，真正目标应是 array/Rust hot loop | `EVAS/evas/simulator/engine.py` |
| 2026-06-02 | Python indexed kernel arrays | 默认 backend 不变；新增 `EVAS_INDEXED_ARRAYS=1`，source update、record point、err_ratio scan 可 opt-in 使用 persistent array mirror | EVAS commit `fe6d142` |
| 2026-06-02 | Indexed model IO boundary | 默认 backend 不变；`EVAS_INDEXED_ARRAYS=1` 时生成 per-model mapped port/output node-id plan，为 model evaluate Rust 化准备边界 IR | EVAS commit `034ca66` |
| 2026-06-02 | Indexed model output write-through | 默认 backend 不变；`EVAS_INDEXED_ARRAYS=1` 时 `_set_output()` 同步写 array mirror，post-model sync 变成 validate/repair guard | EVAS commit `1d94807` |
| 2026-06-02 | Indexed model input read probe | 默认 backend 不变；`EVAS_INDEXED_ARRAYS=1` 时 `_get_voltage()` 对普通读做 dict/array probe compare，event-context reads 只计数跳过 | EVAS commit `c24a2c9` |
| 2026-06-02 | Indexed non-event voltage read | 默认 backend 不变；`EVAS_INDEXED_ARRAYS=1` 时 non-event `_get_voltage()` 优先从 array mirror 返回，event-context reads 继续走 crossing-time interpolation | EVAS commit `63c1eb2` |
| 2026-06-02 | Per-model evaluate profile | 默认关闭；新增 `EVAS_PROFILE_MODEL_EVAL=1`，按 model 聚合 prepare/evaluate/post_update 时间，辅助后续内核优化排序 | EVAS commit `c039159` |
| 2026-06-02 | Post-update empty scan fastpath | 编译期证明无 post-update cross/above 的模型，在主循环跳过空 `post_update_events()`；事件模型保留原路径 | EVAS commit `4f4b58a` |
| 2026-06-02 | Timer/breakpoint scan profile | 新增 simulator-level scan counters 和 timer cache 汇总，不改变 dt/event ordering，用于判断后续是否值得做 event queue | EVAS commit `608551b` |
| 2026-06-02 | Profile-guided kernel sample | 5 个本地 examples 中 `model_evaluate_s` 占 model-loop timing 的 72% 到 91%；下一步优先 evaluate/indexed/Rust，而不是 event queue | scratch logs `/private/tmp/evas-profile-012` |
| 2026-06-03 | Node resolution run cache | 在 `Simulator.run()` 内缓存本地端口名到外部节点名的解析结果；microbenchmark 显示 mapped/parent helper 热路径约 `1.33x` 到 `1.84x`，但它不是 release-wide 速度 claim | EVAS commit `b56454c` |
| 2026-06-03 | Model IO profile counters | `EVAS_PROFILE_MODEL_IO=1` 统计普通 read/write 调用密度；本地 examples 显示 `adc_ramp` 约 `22.48` reads/internal-step，`cmp_delay` 约 `5` reads/internal-step | EVAS commit `dff5e56` |
| 2026-06-03 | Static branch IO node-id plan | compiled model 暴露 ordinary read、event-body read、static write 和 dynamic branch IO metadata；indexed model IO plan 可解析到 node ids，但不改执行代码 | EVAS commit `7d619e2` |
| 2026-06-03 | Static branch fast helper prototype | `EVAS_STATIC_BRANCH_FASTPATH=1` 让静态 `V(node)` read/write 生成专门 helper；mapped pass-through microbenchmark 显示局部约 `1.45x`，但仍不是 release-wide speed claim | EVAS commit `1cb5d34` |
| 2026-06-03 | Static branch node-id direct array | `EVAS_STATIC_BRANCH_FASTPATH=1` + `EVAS_INDEXED_ARRAYS=1` 时普通静态 branch read/write 直接访问 indexed voltage array slot；本地 microbenchmark 相对 slot fallback helper 约 `1.64x` | EVAS commit `e178909` |
| 2026-06-03 | Event interpolation IR boundary | compiled/indexed metadata 显式区分 event trigger voltage read 和 event body voltage read；不改 `_check_cross()`、`_get_voltage()` 或 event ordering | EVAS commit `6c67aaf` |
| 2026-06-03 | Dynamic bus lowering prototype | compiled/indexed metadata 记录 dynamic branch access 的 role/base/dimension/context；不改当前 f-string runtime path，并记录一个已有 2D state-index codegen 风险 | EVAS commit `75e10b5` |
| 2026-06-03 | Indexed model state arrays | compiled/indexed metadata 记录 scalar state ids、integer state 和 array state range；不替换 `self.state` / `self.arrays` runtime storage | EVAS commit `708ebf7` |
| 2026-06-03 | Rust model evaluate ABI prototype | `prototypes/rust-kernel-smoke` 新增 `model-abi` kernel，用 node/state ids 驱动 Rust `Vec<f64>` evaluate loop；仍是 prototype-only | EVAS commit `0263986` |
| 2026-06-03 | Rust production ABI and opt-in static affine eval | 新增 `evas/rust_core` + `ctypes` loader + `EVAS_RUST_STATIC_EVAL`；static affine 模型功能正确，但 64-model local microbenchmark 显示 per-model FFI 让 Rust median `0.8521s` 慢于 Python `0.1788s` | EVAS commit `8930bb9` |
| 2026-06-03 | Rust consecutive segment batch | 连续 eligible static affine models 合成一个 per-step Rust segment，FFI calls 从 `64064` 降到 `1001`；Rust median 从 `0.8521s` 改到 `0.3255s`，但默认 Python sample 仍更快 | EVAS commit `b9d5065` |
| 2026-06-03 | Rust output-node sync deferral | Rust static affine 每步继续同步外部 `node_voltages`，但 `output_nodes` 只在 final 前补齐；64-model sample 中 `output_syncs` 降到 `64`，Rust median `0.3709s` | EVAS commit `8782c11` |
| 2026-06-03 | Indexed dirty validation fastpath | 全 Rust static segment 预计算 source/output dirty tuple，跳过 snapshot 后冗余 full diff；64-model sample `values_checked=65390`、Rust median `0.3314s` | EVAS commit `16cbe9d` |
| 2026-06-03 | Rust segment lifecycle fastpath | Rust static segment 成功时跳过 `_prepare_step()`、timer expire 和 post-update 空检查；DC fixed-step sample `lifecycle_skips=64064`，Rust median `0.3959s` 仍慢于 default Python `0.3336s`，说明剩余瓶颈在 FFI/sync/validation | EVAS commit `3589841` |
| 2026-06-03 | Runtime parameter affine lowering | parameterized affine model 可进入 Rust static segment，并在 instance override 后求 `gain/bias`；64-model parameterized sample `runtime_param_ops=64`、Rust median `0.2322s`、default Python `0.1918s` | EVAS commit `1b5330a` |
| 2026-06-03 | Dynamic bus base/index runtime lowering | dynamic bus read/write 从直接格式化节点名改成 `_resolve_dynamic_node()` cache；16-lane sample `hits=16032`、`misses=16`，median `0.0346s -> 0.0307s`，但还不是完整 node-id/Rust offset lowering | EVAS commit `a91570a` |
| 2026-06-03 | Indexed state runtime storage | 新增 opt-in scalar/int/array state mirror；stateful sample waveform parity pass，但 median `0.0080s -> 0.0108s`，说明它是 Rust ABI 前置而非当前 Python 加速 | EVAS commit `09f9ef5` |
| 2026-06-03 | Static lifecycle fastpath | 复用 compiler capability flags，让纯静态模型默认跳过每步空 `_prepare_step()` 和 absolute timer expire；80-model static chain median `1.3150s -> 0.8853s`，约 `1.49x` | EVAS commit `4f20ee1` |
| 2026-06-03 | Real-slice state-local/static-branch verification | state-local generated evaluate 在 top-wall 10 section profile 中 `model_evaluate_s` 从 `6.0607s` 变成 `6.4126s`，不默认开启；static branch top-wall 10 E2E `14.2529s -> 14.1265s`，约 `1.009x`，只能算小幅混合收益 | EVAS commit `623b7f5` |
| 2026-06-03 | Transition unchanged-target opt-in fastpath | `transition()` target/参数完全不变时可跳过 no-op `set_target()` 和第二次 `evaluate()`；SAR cProfile 中 `set_target` `261240 -> 6623`，但 top-wall 10 E2E candidate 总 wall `17.5862s -> 17.7964s`，默认关闭 | EVAS commit `c909463` |
| 2026-06-03 | Static linear evaluate IR and fast sync | Rust static linear segment 覆盖多输入/简单 state IR；fast sync 让 500-model covered chain `57.09s -> 38.62s`，但 top-wall 10 `candidate_models=0`，下一步必须扩 Rust coverage | EVAS commit `pending` |
| 2026-06-03 | Real-model Rust coverage expansion | top-wall 10 中 `dither_adder`/`gain_amp_fixed` 进入 Rust IR，共 6 ops；其余主要被 event/timer/cross、transition、integer/state array 和 dynamic bus 阻塞。r50 EVAS-only diagnostic 10/10 PASS，但 mixed Rust/Python path 仍不是 speed claim | EVAS commit `pending`; `audits/039-rust-coverage-expansion-for-real-models.md` |
| 2026-06-03 | Rust mixed small-segment gate | r51 top-wall 10 EVAS-only diagnostic 10/10 PASS，总 E2E `18.337s`，measurement-flow tb/e2e 回到 `1.474s`/`1.443s`；small mixed Rust candidates 记录后回退 Python runtime，避免 FFI/sync 开销反向拖慢 | EVAS commit `pending`; `audits/040-rust-mixed-small-segment-gate.md` |
| 2026-06-03 | Transition real top-wall diagnostic | differential `V(out,VSS)<+...transition(...)` 已进入 fused output helper；active transition set 可记录 inactive breakpoint skips；相邻 r54 unchanged-target mode 总 wall 比 r53 约 `0.895x`，但本地 wall 噪声大，不能作为最终速度 claim | EVAS commit `pending`; `audits/041-transition-real-topwall-profile-and-fastpath.md` |
| 2026-06-03 | Integer state, transition target IR, and breakpoint array scan | integer state write 在 Rust static-linear IR 中按 Verilog-A rounding 立即 coercion；`q ? 1.0 : 0.0` transition target 可记录成 `q != 0` 条件 IR；Rust C ABI 可扫描 transition breakpoint arrays，model hook 保留 Python fallback | EVAS commit `pending`; `audits/042-integer-state-transition-target-and-breakpoint-array-scan.md` |
| 2026-06-03 | Transition target executor and timer array scan | transition target IR 已可通过 Python/Rust array executor 计算 target/delay/rise/fall buffers；timer breakpoint scan 接入 Rust C ABI 和 simulator hook，但当前仍需 Python dict packing，因此不是速度 claim | EVAS commit `pending`; `audits/043-transition-target-executor-and-timer-array-scan.md` |
| 2026-06-03 | Ordered transition shadow and timer typed sidecar | `EVAS_RUST_TRANSITION_SHADOW=1` 可在同一个 Rust batch 里按顺序验证 state/static-linear update 后的 transition target；timer state sidecar 把 Rust scan 前的 dict packing 改成 typed arrays 复用。EVAS full regression `509 passed`，但仍是 shadow/parity 和局部开销优化，不是 top-wall 速度 claim | EVAS commit `pending`; `audits/044-ordered-transition-shadow-and-timer-array-sidecar.md` |
| 2026-06-04 | Rust-required rejection audit and simple if lowering | top-wall 10 中 forced Rust 仍慢于 Python fast：rejection-only `18.253s -> 21.304s`，simple `if/else` lowering 后 `18.541s -> 21.362s`。覆盖没有增加，主要 blockers 仍是 arrays、`transition()`、event/cross 和 self-dependent state | EVAS commit `pending`; `audits/045-rust-required-rejection-and-if-lowering.md` |
| 2026-06-04 | Fixed-index state array IR | `arr[0]` / `arr[N-1]` 这类固定数组元素可作为 Rust static-linear `state_values` slot 执行；动态数组下标仍拒绝。top-wall 10 诊断 10/10 PASS，但 Rust-required `21.233s` 仍慢于 Python fast `18.268s`，说明固定数组不是当前主瓶颈 | EVAS commit `pending`; `audits/046-fixed-index-state-array-ir.md` |
| 2026-06-04 | Python-to-Rust behavior map | 明确后续 Rust 化单位不是零散语法，而是 B01-B18 仿真行为到 Rust primitive 的完整映射；下一步先做 behavior coverage manifest，再进入 transition/event/timer production path | EVAS commit `pending`; `audits/048-python-to-rust-behavior-map.md` |
| 2026-06-04 | Behavior coverage manifest | 并行审计 compiler、scheduler、Rust ABI 和历史 counters 后，确认 B01 是 partial、B07 是 target/shadow、B10/B12/B16/B17 仍是 Python-owned；049 定义后续自动 manifest 的 JSON 字段、fallback reason 和 correctness gates | EVAS commit `pending`; `audits/049-behavior-coverage-manifest.md` |
| 2026-06-04 | Transition state Rust primitive | B08 新增 `evas_rust_transition_state_step` typed-array ABI，覆盖 initialization、linear ramp、interrupted retarget 和 initial-condition reset，并接入 `rust_transition_shadow` 检查 pre-state -> post-state parity；当前仍未接入 engine production path，不能作为速度 claim | EVAS commit `pending`; `audits/050-transition-state-rust-primitive.md` |
| 2026-06-04 | Timer step Rust primitives | B11 新增 `evas_rust_timer_periodic_step` / `evas_rust_timer_absolute_step` typed-array ABI，覆盖 periodic due/skip/reschedule 和 absolute due/expire/last-fired parity；当前仍未接入 engine production path，不能作为速度 claim | EVAS commit `pending`; `audits/051-timer-step-rust-primitives.md` |
| 2026-06-04 | Cross/above detector Rust primitives | B09 新增 `evas_rust_cross_detector_step` / `evas_rust_above_detector_step` typed-array ABI，覆盖 detector state update、trigger direction、crossing time、debounce 和 above 初始触发 parity；event body/order/interpolation 仍未迁移，不能作为速度 claim | EVAS commit `pending`; `audits/052-cross-above-detector-rust-primitives.md` |
| 2026-06-04 | Record node-id array path | B15 indexed record path 预计算 recorded node ids，并用 array id 读取替代每个 record point 的 signal-name lookup；CSV schema、`SimResult` 和 checker contract 保持不变，Rust record ABI 尚未实现 | EVAS commit `pending`; `audits/053-record-node-id-array-path.md` |
| 2026-06-04 | Dynamic bus offset Rust primitive | B17 新增 `evas_rust_dynamic_bus_offsets`，用 `base + i * stride + j` 计算 bounded 1-D/2-D bus node id，并对负 index/越界做错误返回；当前 compiler/runtime 仍未接生产路径 | EVAS commit `pending`; `audits/054-dynamic-bus-offset-rust-primitive.md` |
| 2026-06-04 | Event/lifecycle production gate | 050-054 后剩余 B10/B18 被确认是同一个 phase-order correctness gate，不能并行硬切 production；下一步按 event due trace、ordering trace、event write-set、lifecycle shadow 的顺序推进 | EVAS commit `pending`; `audits/055-event-lifecycle-production-gate.md` |
| 2026-06-04 | Event due shadow | `EVAS_RUST_EVENT_DUE_SHADOW=1` 可在真实 engine 入口旁复算 cross/above/timer due state；`engine/netlist/rust_backend/cargo` targeted checks 全部通过。该路径默认关闭、开启后只做 parity 审计，不是速度 claim | EVAS commit `pending`; `audits/056-event-due-shadow.md` |
| 2026-06-04 | Event trace and write-set audit | `EVAS_EVENT_TRACE_AUDIT=1` 记录 fired event、event body enter/exit，以及 state/array/output/timer/transition 写入域；targeted engine/netlist checks 通过。该路径默认关闭，用于决定下一步 production Rust batch 边界，不是速度 claim | EVAS commit `pending`; `audits/057-event-trace-write-set-audit.md` |
| 2026-06-04 | Event-body write-set Rust batch | top-wall audit 显示 gain extraction 的 gated LFSR shift/XOR 是最高频 event-body array/state 写集合；新增 `evas_rust_event_lfsr_shift_xor_step`，shadow 2000/2000 match、production 10/10 safe_vs_strict。top-wall fast A/B 仅 `27.514s -> 27.267s`，说明它是正确性里程碑而非 release-wide speed claim | EVAS commit `pending`; `audits/058-event-body-write-set-rust-batch.md` |
| 2026-06-04 | Timer/event production gate | CPPLL per-check Rust timer 尝试 2/2 PASS 但变慢：e2e `2.8293s -> 3.6122s`、tb `2.6403s -> 3.8000s`，原因是 `90478` 次 length-1 FFI。加入小集合 gate 后 top-wall 10 为 10/10 PASS，总 wall `20.2422s -> 20.2278s` 基本持平；后续方向改为 compiler-level timer batch 和 single-timer Python hot-path | EVAS commit `pending`; `audits/059-timer-event-production-gate.md` |
| 2026-06-04 | Static timer/event segment batch | 连续 static timer event 现在会先批量计算 due mask，再按原顺序执行 event body；in-memory 16-timer sample `0.046606s -> 0.040328s`，但当前 top-wall 10 batch counters 为 0，说明真实瓶颈仍在动态 `timer(next_t)` 等 state-owned timer | EVAS commit `pending`; `audits/060-static-timer-event-segment-batch.md` |
| 2026-06-04 | State-owned absolute timer fast path | `timer(t_next_toggle)` 这类 owner chain 在未到 armed target 前跳过 target state 读取和 helper 调用；top-wall 10 仍 10/10 PASS，CPPLL e2e/tb 各命中 `90478` checks、`80243` fast skips、`10235` target reads。总 wall 仍是 EVAS-only candidate evidence，不能作为论文速度 claim | EVAS commit `pending`; `audits/061-state-owned-absolute-timer-fastpath.md` |
| 2026-06-04 | Fused timer/LFSR/output batch | 对安全 periodic timer LFSR 模式新增 `evas_rust_timer_lfsr_output_step`，一次 FFI 完成 timer step、event body state update、output node write；`V(out)<+state` hold path 避免重复 Python dict 写。smoke counters：batch 1、calls 16、due/executed/writes 4、fallback 0、indexed record reads 17 | EVAS commit `pending`; `audits/062-fused-timer-lfsr-output-batch.md` |
| 2026-06-04 | PRBS7 whole-model Rust fastpath | 对真实 `vbr1_l1_lfsr_prbs_generator/dut/gold` 做整段 Rust trace batch，绕过 Python generated model loop、cross scan、event body、transition calls 和 prepare-step；单行 fast EVAS kernel/tran `0.2156s -> 0.0085s`、E2E `0.4069s -> 0.2961s`，但 top-wall 10 总 wall 只有 `1.006x`，说明下一步必须扩大 whole-segment coverage | EVAS commit `pending`; `audits/063-prbs7-whole-model-rust-fastpath.md` |
| 2026-06-04 | Compiler-driven whole-segment lowering | `backend.py` 从 Verilog-A AST 生成 `_whole_segment_candidates`，engine 按 metadata dispatch whole-segment trace；除 PRBS/LFSR Rust ABI 外，新增 CPPLL/SAR/prop-delay/gain 四类热模型 opt-in trace executor。4-row sequential runner 4/4 PASS，E2E `9.999s -> 6.819s`，tran `5.657s -> 0.451s` | EVAS commit `pending`; `audits/064-compiler-driven-whole-segment-lowering.md` |
| 2026-06-04 | Semantic/dataflow whole-segment matching | whole-segment collector 不再依赖固定端口/状态名，而是从 event、assignment、branch access、transition target 和 parameter reference 推断角色；修复 `vl + (vh-vl)*transition` supply direction 反向导致 CPPLL `vctrl_mon=0` 的 bug。top4 smoke 4/4 PASS，E2E `11.090s -> 7.064s` | EVAS commit `pending`; `audits/065-semantic-dataflow-whole-segment-matching.md` |
| 2026-06-04 | Release-wide Rustification Workplan | 将 79 个 release entry、357 个 gold `.va` 的全量跑通目标拆成 W0-W10 workstreams；后续从 067 coverage manifest 和 068 whole-segment Rust ABI contract 开始 | EVAS commit `pending`; `audits/066-release-wide-rustification-workplan.md` |
| 2026-06-04 | Release Rust coverage manifest | 全量扫描 release gold `.va`：357/357 compile pass，Rustification estimate `30.0%`；`weighted_dac_v1` 误命中从 13 个候选收紧到 2 个候选。该阶段直接速度收益 `0%`，价值是覆盖口径和 fastpath 安全性 | EVAS commit `pending`; `audits/067-release-rust-coverage-manifest-generator.md` |
| 2026-06-04 | Whole-segment ABI contract | 为 9 类 whole-segment candidate 固化 schema/arity/type/cross-field validator；release-wide report 显示 23 个候选 invalid count 为 0。该阶段直接速度收益 `0%`，价值是后续 Rust production ABI 不再依赖隐式 tuple 下标 | EVAS commit `pending`; `audits/068-whole-segment-rust-abi-contract.md` |
| 2026-06-04 | Gain timer production Rust trace | 新增 `evas_rust_gain_timer_reduction_trace`，真实 `vbr1_l1_gain_estimator` tb/e2e 3-repeat 全 PASS；EVAS tran median `0.0275s -> 0.0083s` / `0.0276s -> 0.0081s`，E2E wall 约 `1.09x`，说明小 row 已被外层开销主导 | EVAS commit `pending`; `audits/069-topwall-gain-timer-production-rust.md` |
| 2026-06-04 | Propagation-delay production Rust trace | 新增 `evas_rust_cmp_delay_trace`，真实 `vbr1_l1_propagation_delay_comparator/dut` 3-repeat 全 PASS；EVAS tran median `1.3745s -> 0.0094s`，E2E wall median `2.0645s -> 0.5783s`，说明重 row 的整段 Rust batch 能直接转化为 E2E 收益 | EVAS commit `pending`; `audits/070-propagation-delay-production-rust.md` |
| 2026-06-04 | SAR loop production Rust trace | 新增 `evas_rust_sar_loop_trace`，真实 `vbr1_l2_weighted_sar_adc_dac_loop` tb/e2e 3-repeat 全 PASS；tb EVAS tran median `3.0981s -> 0.1071s`、E2E wall median `6.7422s -> 5.3224s`，e2e tran `2.4973s -> 0.1390s` 但 wall 受外层开销和负载波动压制 | EVAS commit `pending`; `audits/071-sar-loop-production-rust.md` |
| 2026-06-04 | Stage55 CPPLL Rust trace and lean mode | 新增 `evas_rust_cppll_reacquire_trace` 并把 speed runner 的 `profile_fast_rust_55` 收紧为只启用 production whole-segment Rust；top-wall 10 EVAS-only 总 wall `12.7811s -> 5.1682s`、10/10 PASS、stage weighted coverage `80.6%`。这不是全 release Rustification claim，后者仍约 `30%` | EVAS commit `pending`; `audits/072-stage55-cppll-rust-trace-and-lean-production-mode.md` |
| 2026-06-04 | Rust speed claim gate | 新增 `report_vabench_release_rust_speed_claim_gate.py`，把“能 claim 什么/不能 claim 什么”机器化：stage55 engineering claim 当前打开，full release Rustification 因 `30.0%` 和非 production 行为 blocker 关闭，Spectre AX speed 因缺 rust55 同机 dual artifact 关闭 | EVAS commit `pending`; `audits/073-rust-speed-claim-gate.md` |
| 2026-06-04 | Rust55 top-wall EVAS smoke | 按“先 EVAS-only，再小 AX smoke，最后 full AX”的节奏补实验：6 个 unique top-wall row 上 Rust55 6/6 safe_vs_strict，总 wall `3.750s`，相对 normal fast `2.41x`；收益集中在 SAR/prop-delay/CPPLL，gain measurement-flow 仍未接 production fastpath | EVAS commit `pending`; `audits/074-rust55-topwall-evas-smoke.md` |
| 2026-06-04 | Gain measurement-flow production Rust | 新增 `evas_rust_gain_measurement_flow_trace`，把 gain extraction 的 clocked vin、LFSR dither、dither adder、fixed gain amp 合成一个 Rust trace；top-wall 6 EVAS-only Rust55 总 wall `2.103s`，相对 normal fast `4.60x`，6/6 safe_vs_strict | EVAS commit `pending`; `audits/075-gain-measurement-flow-production-rust.md` |
| 2026-06-04 | Current Rustification status after gain flow | 当前 top-wall 10 EVAS-only Rust55 总 wall `3.250s`，相对 normal fast `4.08x`，但 release-wide B01-B18 completion estimate 仍为 `30.0%`；新增 whole-flow manifest 表，避免 075 被单模型 manifest 漏报 | EVAS commit `pending`; `audits/076-current-rustification-status-after-gain-flow.md` |
| 2026-06-04 | Whole-segment record trace copy reduction | `_record_trace_result` 对 `np.ndarray[float64]` 不再无条件二次拷贝；SAR 保留旧路径；fast+Rust55 smoke 10/10 PASS，但该改动只作为低风险清理，不作为独立速度 claim | EVAS commit `pending`; `audits/077-whole-segment-record-trace-copy-reduction.md` |
| 2026-06-04 | Global timing split and persistent worker | `simulate_evas.run_case` 把 EVAS tran/total、CSV/derive 和 unattributed subprocess time 结构化进 `timing_split`；`VAEVAS_EVAS_PERSISTENT_WORKER=1` 可复用 EVAS worker，2-row smoke E2E `2.764s -> 1.440s`，top-wall 10 worker 10/10 PASS | EVAS commit `pending`; `audits/078-global-evas-timing-split-and-persistent-worker.md` |
| 2026-06-04 | Required-signal global trace | streaming checker required columns 变成 harness->EVAS trace contract；current-code trace on/off top-wall 10 均 10/10 PASS，E2E `2.527s -> 2.024s`，CSV write `0.519s -> 0.404s`，checker `0.750s -> 0.699s` | EVAS commit `pending`; `audits/079-required-signal-global-trace.md` |
| 2026-06-05 | Evaluate IR piecewise and Rust timer batch | `abs/min/max` 可 lowering 为条件线性 IR；连续 static timer segment 的 due-mask 可走 Rust production batch。该阶段补全通用路径，不作为独立速度 claim | EVAS commit `pending`; `audits/080-evaluate-ir-piecewise-and-rust-timer-batch.md` |
| 2026-06-05 | Event body linear Rust batch | `cross/above/timer` 触发后的简单 state assignment body 可走通用 Rust static-linear batch；cross body 读节点时仍 fallback，保护 crossing-time interpolation | EVAS commit `pending`; `audits/081-event-body-linear-rust-batch.md` |
| 2026-06-05 | Timer static-linear whole segment Rust | 周期 timer due/reschedule、static-linear event body、non-event static-linear output evaluate 和显式 record trace/timer breakpoint 可在一个 Rust FFI 中完成；当前要求显式 `record_step`，且不覆盖 cross/transition/dynamic array | EVAS commit `pending`; `audits/082-timer-static-linear-whole-segment-rust.md` |
| 2026-06-05 | Record node-id Rust ABI | indexed array loop 下 recorded-node value gather 可走 Rust ABI，B15 移除 `rust_record_abi_not_implemented` blocker；Python 仍拥有 time/list append、SimResult、CSV 和 checker contract | EVAS commit `pending`; `audits/083-record-node-id-rust-abi.md` |
| 2026-06-05 | Multi-timer static-linear event queue Rust | 082 的 single periodic timer segment 扩展为 multi periodic timer queue；同一时刻按 compiler/source metadata 顺序执行，event body 仍要求 state-only static-linear，cross/above/transition/default adaptive trace 仍 fallback | EVAS commit `pending`; `audits/084-multi-timer-static-linear-event-queue-rust.md` |
| 2026-06-05 | Cross/above interpolation, transition production, default adaptive trace | `cross()/above()` event body node reads 可 opt-in 走 Rust interpolation cache；`transition()` state evolution 可 opt-in 走 Rust typed-array production；timer static-linear whole-segment path 在 `record_step=None` 时可复现受限默认 adaptive/internal trace。event queue/order/body 和全局 adaptive solver 仍不是全量 Rust 化 | EVAS commit `pending`; `audits/085-cross-above-transition-default-adaptive-trace.md` |
| 2026-06-05 | 094e Rust body IR ABI | `evas_rust_evaluate_body_ir` 和 Python ctypes wrapper 可执行 synthetic expression/write op batch；100 组随机 state-write parity PASS，全量 EVAS pytest 620 PASS。该阶段未接生产 dispatch，速度收益为 0% | EVAS commit `pending`; `audits/094e-rust-abi.md` |
| 2026-06-05 | 094f ExprIR/body write-set encoder | `ExprIR + BindingTableIR + node_slots` 可编码成 Rust body ops；ordered scalar state assignment + single-node contribution block 可经 Rust ABI 顺序执行；动态 indexed voltage read 和 event body 保守 fallback。该阶段仍未接 event scheduler/production dispatch，速度收益为 0% | EVAS commit `pending`; `audits/094f-body-ir-encoder.md` |
| 2026-06-05 | 094g Event body program + trigger expr eval | 单个 `EventStatementIR` 可保留 trigger metadata，并绑定到 094f Rust body write-set program；standalone `evas_rust_evaluate_body_expr` 可计算 `cross(V(clk)-0.5,+1)` trigger value；due/order scheduler 仍未实现，速度收益为 0% | EVAS commit `pending`; `audits/094g-event-body-program.md` |
| 2026-06-05 | 094h Event due program + trigger expression batch | `EventIR + BindingTableIR + node_slots` 可生成 trigger expression batch；`evas_rust_evaluate_body_expr_batch` 一次 FFI 计算多个 cross/above/timer expression value；fired-index/order scheduler 仍未实现，速度收益为 0% | EVAS commit `pending`; `audits/094h-event-due-program.md` |
| 2026-06-05 | 094i Mixed event due runtime shadow | `RustEventDueRuntime` 将 094h trigger expression batch 接到 Rust cross/above/timer primitives，mixed `initial/cross/above/timer` fired indices 按源码顺序输出；event body dispatch 和 production engine 未接入，速度收益为 0% | EVAS commit `pending`; `audits/094i-mixed-event-due-runtime.md` |
| 2026-06-05 | 094j Event statement shadow dispatch | `RustEventStatementRuntime` 将 fired trigger indices 接到 094g Rust body batch；同一 event statement 多 trigger 同时 fired 时 body 只执行一次。多 event statement/global phase-order 和 production engine 未接入，速度收益为 0% | EVAS commit `pending`; `audits/094j-event-statement-shadow-dispatch.md` |
| 2026-06-05 | 094k Analog block event shadow dispatch | `RustAnalogBlockEventRuntime` 将多个 event statement runtime 按 analog block 源码顺序串联；两个独立 event statement 同步 fired 时 state/output write 顺序正确。continuous statement/完整 phase-order 和 production engine 未接入，速度收益为 0% | EVAS commit `pending`; `audits/094k-analog-block-event-shadow-dispatch.md` |
| 2026-06-05 | 094l-s Pipeline-stage real-row gates | `pipeline_stage` 的 event/body/transition shadow runtime 在 same-grid replay 下 max abs diff `4.86e-8`；prototype full-sim wrapper 暴露 transition breakpoint ownership 和 Python/Rust pack-sync 负优化；bound indexed-array replay 相对 dict-pack 仅 `1.137x`。结论：继续 whole-step typed-array batch，不默认接 engine | EVAS commit `pending`; `audits/094l-*` 到 `audits/094s-*` |
| 2026-06-06 | Auto row-checker sparse trace contract | row-based checker 的 literal set、f-string bit columns、`indexed_columns()` 和 prefix bit families 可自动下发 required trace；full release EVAS2 271/271 PASS、fallback 0，E2E `69.952s -> 59.418s`，checker `54.244s -> 46.245s` | EVAS commit `pending`; `audits/115-auto-row-checker-sparse-trace-contract.md` |
| 2026-06-06 | Generic checker runtime hot rows | `CsvCheckerRuntime` 统一 header index、流式 rows、series、插值采样和 resample rows；rectifier/window/stimulus 10-row smoke 10/10 PASS，checker `11.618s -> 0.221s` | EVAS commit `pending`; `audits/116-generic-checker-runtime-hot-rows.md` |
| 2026-06-06 | Coverage layering and pulse breakpoint fix | 覆盖率报告分离 static lowering、runtime 命中和速度证据；修复 pulse source breakpoint `time ~= delay` 时重复返回当前断点导致 event-transition Rust loop 卡住的问题 | EVAS commit `pending`; `audits/118-rustsim-coverage-layering-and-pulse-breakpoint.md` |
| 2026-06-06 | P0/P1 release closeout | 当前代码 clean EVAS2 runner smoke 271/271 PASS；P0/P1 文档把 release-row 可用性、core speedup、E2E 外层开销、Spectre AX claim gate 和剩余 Rust 化缺口分开 | EVAS commit `pending`; `EVAS2_P0P1_CLOSEOUT_20260606.md` |

## 后续候选项目

后续优先级以 `audits/066-release-wide-rustification-workplan.md` 为准。旧的“先低风险数据结构，再高风险内核替换”已经不够准确；现在的主线是先量化全 release 覆盖，再把 top-wall 热路径的一整段行为迁到 Rust production path。

| 优先级 | 项目 | 核心目标 | 主要风险 |
|---|---|---|---|
| done | 067 release coverage manifest | 全量列出 B01-B18 覆盖、fallback blocker、candidate kind 和 top-wall 权重 | manifest 只能指导工程，不能替代速度 claim |
| done | 068 whole-segment Rust ABI contract | 把 CPPLL/SAR/comparator/gain 的 semantic metadata 固化成通用 Rust ABI | ABI 过窄会退回名字匹配；过宽会误命中 |
| done | 069 gain timer production Rust trace | 把 `gain_timer_reduction_v1` 的 fixed trace loop 迁到 Rust ABI，并建立 A/B 开关 | E2E wall 受外层开销限制，不能把小 row 核心收益外推到 release claim |
| done | 070 propagation-delay whole-segment Rust trace | 把 propagation-delay comparator 的 fixed trace loop 迁到 Rust ABI，并建立 A/B 开关 | crossing/transition/delay measurement 必须保持 parity |
| done | 071 SAR whole-segment Rust trace | 把 weighted SAR loop 当前仍在 Python 的 whole-segment executor 迁到 Rust opt-in production | state machine、sample-hold、DAC output 和 record contract 必须一起守住 |
| done | 072 stage-55 CPPLL Rust trace and lean mode | 把 CPPLL reacquire trace fill 迁到 Rust，并建立只含 production whole-segment fastpath 的 55% 阶段速度模式 | stage coverage 不能误写成 release-wide Rustification |
| done | 073 rust speed claim gate | 把 stage55、full Rustification、Spectre AX speed 三类 claim 的证据门禁拆开 | gate 只能防过 claim，不能替代实际 Rust coverage 或 Spectre rerun |
| done | 074 rust55 top-wall EVAS smoke | 按阶段节奏重跑 top-wall EVAS-only，确认 Rust55 的有效覆盖和剩余瓶颈 | EVAS-only 不能替代 Spectre AX claim |
| done | 075 gain extraction measurement-flow production Rust | 把剩余 top-wall wall 中最大的 gain tb/e2e 从 Python fast 降到 Rust production path | 当前只覆盖该 measurement-flow 形状；EVAS-only 不能替代 Spectre AX claim |
| done | 076 current Rustification status after gain flow | 把 top-wall 热点加速口径和 release-wide 全语义 Rustification 口径拆开，并补 whole-flow manifest 盲点 | 不能把 `4.08x` top-wall EVAS-only 写成全量 Rust 化或 AX claim |
| done | 077 whole-segment record trace copy reduction | 对已 Rust 化 trace 去掉部分中间 Python list/ndarray 往返 | 收益不稳定，不能作为独立速度 claim；SAR 不适合强行改成 numpy-column path |
| done | 078 global timing split and persistent worker | 先做所有 benchmark 共用的 runner/subprocess 计时拆分和 opt-in worker 复用 | 这是 EVAS-only harness/runtime 证据，不能替代 Spectre AX claim |
| done | 079 required-signal/sparse trace path | 只输出 checker 必需信号，减少无用列和 CSV/checker 开销 | 有动态 header 的 checker 暂不收窄；EVAS-only 不能替代 Spectre AX claim |
| done | 080 evaluate IR piecewise + Rust timer batch | `abs/min/max` 进入条件线性 IR；连续 static timer segment 的 due-mask 进入 Rust production batch | 不是全量 evaluate/event Rust 化，cross/above 和 dynamic timer 仍需 event queue 级 lowering |
| done | 081 event body linear Rust batch | `cross/above/timer` 触发后的简单 state assignment body 进入通用 Rust static-linear batch | due/order/interpolation 仍由 Python 拥有；cross body 读节点时保守 fallback |
| done | 082 timer static-linear whole segment Rust | 单 periodic timer 的 due、event body、output evaluate 和显式 record trace/timer breakpoint 合成一个 Rust segment executor | 当前只覆盖显式 record_step 的保守子集，不能 claim 全量 Rust 化 |
| done | 083 record node-id Rust ABI | indexed record value gather 进入 Rust ABI | 只迁 value gather，不等于 CSV/checker pipeline Rust 化 |
| done | 084 multi-timer static-linear event queue Rust | 多个 periodic timer 的 due/order/event body/evaluate/record 进入一个 Rust queue segment | 只覆盖 state-only static-linear body，不覆盖 cross/above/transition |
| done | 085 cross/above interpolation, transition production, default adaptive trace | 补齐 event-time interpolation cache、transition typed-array opt-in production，以及 timer static-linear 默认 trace gate | 仍不是 full event queue / full transition batch / global adaptive solver Rust 化 |
| P1 | 086 event/timer/transition batch ownership | 统一 detector due、event body、transition state/output、record 的 Rust batch ownership | phase-order correctness 风险最高 |
| P2 | 087 release-wide Rust auto smoke | 在 `rust_mode=auto` 下跑全量当前可仿 slice 并汇总 PASS/fallback/speed | 只作为 EVAS 工程 gate；paper speed 还需 same-slice Spectre/AX |

## 后续每次改动必须回答的问题

每个审计文档至少要回答这些问题：

- **改造原理**：为什么这个改动理论上会更快？减少的是“每步成本”、”步数“、还是“输出/检查开销”？
- **改前状态**：改动前代码路径、测试结果、性能数字是什么？
- **改后状态**：改动后代码路径、测试结果、性能数字是什么？
- **精度/功能影响**：是否改变默认 backend？是否影响 CSV schema、checker、strobe、event ordering？
- **学习沉淀**：如果读者不熟悉 Python/Rust/仿真器，需要先理解哪些概念？
- **回退方式**：如果出现 parity 退化，应该回退哪一层？

## 编号规则

文档文件名使用三位编号：

```text
audits/000-rust-kernel-design.md
audits/001-indexed-sidecar-and-rust-smoke.md
audits/002-python-indexed-ir-parity.md
audits/003-python-indexed-voltage-snapshot.md
audits/004-python-indexed-kernel-arrays.md
audits/005-indexed-model-io-boundary.md
audits/006-indexed-model-output-write-through.md
audits/007-indexed-model-input-read-probe.md
audits/008-indexed-non-event-voltage-read.md
audits/009-indexed-model-evaluate-profile.md
audits/010-post-update-empty-scan-fastpath.md
audits/011-timer-breakpoint-scan-profile.md
audits/012-profile-guided-kernel-sample.md
audits/013-node-resolution-run-cache.md
audits/014-model-io-profile-counters.md
audits/015-static-branch-io-node-id-plan.md
audits/016-static-branch-fast-helper-prototype.md
audits/017-static-branch-node-id-direct-array.md
audits/018-event-interpolation-ir-boundary.md
audits/019-dynamic-bus-lowering-prototype.md
audits/020-indexed-model-state-arrays.md
audits/021-rust-model-evaluate-abi-prototype.md
audits/022-rust-ffi-batch-evaluate-boundary.md
audits/023-dynamic-bus-runtime-codegen-fix.md
audits/024-compiled-model-rust-replay-smoke.md
audits/025-production-opt-in-rust-backend-channel.md
audits/026-opt-in-static-continuous-model-rust-eval.md
audits/027-rust-consecutive-model-segment-batch.md
audits/028-rust-output-node-sync-deferral.md
audits/029-indexed-dirty-validation-fastpath.md
audits/030-segment-lifecycle-fastpath.md
audits/031-runtime-parameter-affine-lowering.md
audits/032-dynamic-bus-base-offset-lowering.md
audits/033-indexed-state-runtime-storage.md
audits/034-static-lifecycle-fastpath.md
audits/035-state-local-and-static-branch-real-slice-verification.md
audits/036-transition-unchanged-target-fastpath.md
audits/037-static-linear-evaluate-ir-b1-b4.md
audits/038-static-linear-fast-sync.md
audits/039-rust-coverage-expansion-for-real-models.md
audits/040-rust-mixed-small-segment-gate.md
audits/041-transition-real-topwall-profile-and-fastpath.md
audits/042-integer-state-transition-target-and-breakpoint-array-scan.md
audits/043-transition-target-executor-and-timer-array-scan.md
audits/044-ordered-transition-shadow-and-timer-array-sidecar.md
audits/045-rust-required-rejection-and-if-lowering.md
audits/046-fixed-index-state-array-ir.md
audits/048-python-to-rust-behavior-map.md
audits/049-behavior-coverage-manifest.md
audits/050-transition-state-rust-primitive.md
audits/051-timer-step-rust-primitives.md
audits/052-cross-above-detector-rust-primitives.md
audits/053-record-node-id-array-path.md
audits/054-dynamic-bus-offset-rust-primitive.md
audits/055-event-lifecycle-production-gate.md
audits/056-event-due-shadow.md
audits/057-event-trace-write-set-audit.md
audits/058-event-body-write-set-rust-batch.md
audits/059-timer-event-production-gate.md
audits/060-static-timer-event-segment-batch.md
audits/061-state-owned-absolute-timer-fastpath.md
audits/062-fused-timer-lfsr-output-batch.md
audits/063-prbs7-whole-model-rust-fastpath.md
audits/064-compiler-driven-whole-segment-lowering.md
audits/065-semantic-dataflow-whole-segment-matching.md
audits/066-release-wide-rustification-workplan.md
audits/067-release-rust-coverage-manifest-generator.md
audits/068-whole-segment-rust-abi-contract.md
audits/069-topwall-gain-timer-production-rust.md
audits/070-propagation-delay-production-rust.md
audits/071-sar-loop-production-rust.md
audits/072-stage55-cppll-rust-trace-and-lean-production-mode.md
audits/073-rust-speed-claim-gate.md
audits/074-rust55-topwall-evas-smoke.md
audits/075-gain-measurement-flow-production-rust.md
audits/076-current-rustification-status-after-gain-flow.md
audits/077-whole-segment-record-trace-copy-reduction.md
audits/078-global-evas-timing-split-and-persistent-worker.md
audits/079-required-signal-global-trace.md
audits/080-evaluate-ir-piecewise-and-rust-timer-batch.md
audits/081-event-body-linear-rust-batch.md
audits/082-timer-static-linear-whole-segment-rust.md
audits/083-record-node-id-rust-abi.md
audits/084-multi-timer-static-linear-event-queue-rust.md
audits/085-cross-above-transition-default-adaptive-trace.md
audits/086-transition-operator-persistent-buffer-reuse.md
audits/087-transition-per-step-batch-design.md
audits/088-transition-per-step-batch-implementation.md
audits/089-cross-above-detector-production-gate.md
audits/091-generic-event-state-transition-candidate-matcher.md
audits/091c-generic-executor-dispatch-gate.md
audits/091d-generic-executor-python-body.md
audits/092-generic-executor-real-row-validation.md
audits/093-generic-executor-sweep-and-default-on-decision.md
audits/094-verilog-a-body-rust-kernel-design.md
audits/094a-expression-ir.md
audits/094b-statement-ir.md
audits/094c-schedule-ir.md
audits/094d-state-binding-ir.md
audits/094e-rust-abi.md
audits/094f-body-ir-encoder.md
audits/094g-event-body-program.md
audits/094h-event-due-program.md
audits/094i-mixed-event-due-runtime.md
audits/094j-event-statement-shadow-dispatch.md
audits/094k-analog-block-event-shadow-dispatch.md
audits/094l-pipeline-stage-control-flow-body-batch.md
audits/094m-event-only-runtime-builder.md
audits/094n-transition-contribution-runtime.md
audits/094o-combined-analog-block-shadow-runtime.md
audits/094p-real-row-shadow-replay-gate.md
audits/094q-opt-in-full-sim-wrapper.md
audits/094r-engine-dispatch-contract-and-no-default.md
audits/094s-persistent-typed-array-engine-slice.md
audits/095-generic-executor-record-adaptive-substeps.md
audits/096-transition-production-real-release-sweep.md
audits/098-current-rust-coverage-and-body-ir-production.md
audits/099-body-ir-rejection-taxonomy.md
audits/100-event-transition-coverage-estimator.md
audits/101-event-transition-source-order-planner.md
audits/102-compiler-visible-event-transition-plan.md
audits/103-event-transition-shadow-runtime.md
audits/104-event-transition-production-gate.md
audits/105-evas2-strict-rust-engine.md
audits/106-evas2-event-transition-core-strict-production.md
audits/107-evas2-native-scheduler-sparse-record.md
audits/108-rust-owned-simulation-loop-first.md
audits/109-continuous-body-and-slot-remap.md
audits/110-timer-array-rustsimprogram-speed-smoke.md
audits/111-post-update-phase-and-selected12-speed.md
audits/112-composite-event-body-and-scaled-transition.md
audits/113-p0-python-compatibility-gap-closures.md
audits/114-full-release-rust-py-spectre-fourway.md
audits/115-auto-row-checker-sparse-trace-contract.md
audits/116-generic-checker-runtime-hot-rows.md
EVAS2_P0P1_CLOSEOUT_20260606.md
EVAS2_CURRENT_ARTIFACT_INDEX_20260606.md
```

编号表示工程顺序，不表示论文 claim 强度。后续如果一个改动失败，也保留审计文档，状态标成 `rejected` 或 `diagnostic`，避免后来重复踩同一个坑。

## Claim 边界

这里的文档可以支持后续速度 claim，但不能直接替代 release-wide speed artifact。

- backend 迁移门槛：EVAS 当前可仿真内容不能减少，至少先过 examples capability manifest。
- paper-facing 速度 claim：必须来自 vaBench release 同片任务、同服务器、Spectre-equivalence-gated 的 EVAS/Spectre/AX timing。
- Rust toy benchmark：只能证明方向值得做，不能直接声明 EVAS 对 AX 的最终速度优势。
