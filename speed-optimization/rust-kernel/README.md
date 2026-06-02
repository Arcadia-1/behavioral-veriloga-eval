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
```

编号表示工程顺序，不表示论文 claim 强度。后续如果一个改动失败，也保留审计文档，状态标成 `rejected` 或 `diagnostic`，避免后来重复踩同一个坑。

## Claim 边界

这里的文档可以支持后续速度 claim，但不能直接替代 release-wide speed artifact。

- backend 迁移门槛：EVAS 当前可仿真内容不能减少，至少先过 examples capability manifest。
- paper-facing 速度 claim：必须来自 vaBench release 同片任务、同服务器、Spectre-equivalence-gated 的 EVAS/Spectre/AX timing。
- Rust toy benchmark：只能证明方向值得做，不能直接声明 EVAS 对 AX 的最终速度优势。
