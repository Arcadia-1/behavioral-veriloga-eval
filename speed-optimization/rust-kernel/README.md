# EVAS Rust Kernel Optimization

这个目录记录 EVAS 内核 Rust 化和 indexed 化的长期改造过程。它不是论文速度结论本身，而是解释“为什么这样改、改了什么、改前改后如何验证、下一步怎么走”的工程审计入口。

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
| sleep | `RUSTIFICATION_SLEEP_WORKLIST_20260603.md` | active | 睡后继续 Rust 化的工作清单，重点收掉 output sync、indexed validation 和 lifecycle bookkeeping |
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

## 后续候选项目

这些项目按“先低风险数据结构，再高风险内核替换”的顺序排列，后续可以逐个写成 017 之后的审计文档。

| 优先级 | 项目 | 核心目标 | 主要风险 |
|---|---|---|---|
| P1 | Indexed dirty sync / validation fastpath | 027 后每步仍全量 array/dict validate，下一步改成 dirty-node 或抽样验证 | 漏掉 dict/array divergence |
| P1 | Segment lifecycle fastpath | 对 compiler-proven static segment 跳过空 prepare/timer/post-update bookkeeping | eligibility guard 过宽 |
| P1 | Dynamic bus runtime lowering | 把 019/023 暴露的 bus metadata/helper 进一步落到稳定 base+offset runtime | dynamic index、2D bus 和 integer state coercion |
| P2 | Timer/breakpoint event queue | 减少 timer/cross/bound_step 每步扫描 | missed event 或 breakpoint ordering |
| P2 | Sparse/required-signal CSV | 只输出 checker 必需信号或 sparse/edge trace | checker schema 和报告兼容性 |

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
```

编号表示工程顺序，不表示论文 claim 强度。后续如果一个改动失败，也保留审计文档，状态标成 `rejected` 或 `diagnostic`，避免后来重复踩同一个坑。

## Claim 边界

这里的文档可以支持后续速度 claim，但不能直接替代 release-wide speed artifact。

- backend 迁移门槛：EVAS 当前可仿真内容不能减少，至少先过 examples capability manifest。
- paper-facing 速度 claim：必须来自 vaBench release 同片任务、同服务器、Spectre-equivalence-gated 的 EVAS/Spectre/AX timing。
- Rust toy benchmark：只能证明方向值得做，不能直接声明 EVAS 对 AX 的最终速度优势。
