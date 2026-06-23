# EVAS Rustification Worklist - 2026-06-05

Status: `deprecated`

Superseded by: `RUSTIFICATION_WORKLIST_20260606.md`

理由：本文档覆盖 audits 001-085；后续 2026-06-05 → 2026-06-06 会话完成 audits 086-095 + Stage 6 commit hygiene + handoff to codex for 094 multi-week project。新 worklist 更新了所有数据点（53-row sweep, opt-in matrix, 工程教训）。原文档保留作为 2026-06-05 时点快照。

Replaces: `RUSTIFICATION_SLEEP_WORKLIST_20260603.md`（已 stale，规划停在 audit 050，实际本地已到 085）

目标重申（用户 2026-06-05 确认）：**速度优先，做通用的 Python→Rust 迁移，不再投入按电路写 Rust tracer。**

## Current Position

- **已完成 audit**：001–085（**047 缺号**，需用户决定补写或正式 retire）
- **最近活动**：audit 085 修改于 2026-06-05 04:02（约 12 小时前），`Code commit: pending`
- **未提交改动**：
  - `EVAS` 仓库：`evas/netlist/runner.py`、`evas/rust_core/src/lib.rs`（HEAD ahead origin 2）
  - `behavioral-veriloga-eval` 仓库：`benchmark-vabench-release-v1/MANIFEST.{json,md}`，以及 077–085 等多份未跟踪 audit
  - 062–085 的多个 audit 都标 `Code commit: pending`，说明这一波 Rust 工程证据尚未落到 git history
- **当前可 claim 的速度数据**（来自 audit 076，2026-06-04）：
  - Top-wall 10 EVAS-only：`profile_fast_rust_55` 3.250s vs `profile_fast` 13.264s，**4.08×**
  - 不可 claim：EVAS Rust path 全量 > Python 默认；EVAS > Spectre AX paper-facing
- **Release-wide 通用语义 Rustification**：~30%（按 B01–B18 operator 覆盖估算）

## 分类标签

| Tag | 含义 | 后续是否继续投入 |
|---|---|---|
| **A — Generic infra** | typed-array primitive、IR lowering、compiler matching、ABI 契约、operator 覆盖 | ✅ 主投入方向 |
| **B — Boundary cost** | FFI 批量化、Python↔Rust sync、lifecycle bookkeeping、persistent worker | ✅ P0，先于 A 的扩张 |
| **C — Per-circuit** | 特定电路 whole-segment fastpath（SAR/CPPLL/PRBS7/gain_flow 等） | ❌ **暂停**，除非新 row 占 top-wall >5% 且能验证新 primitive |
| **D — Trace/IO** | record/CSV path、sparse required-signal trace、zero-copy | ✅ 与 A 并行 |
| **X — Meta** | audit、coverage manifest、claim gate、status doc | 按需 |

## 已完成 audit 分类（001–085）

| Range | 主题 | Tag | Notes |
|---|---|---|---|
| 001–014 | 索引化基础 + profile 数据采集 | A | 已完结的前置工作 |
| 015–020 | static-branch / event-interpolation / dynamic-bus / state-arrays IR boundary | A | Rust 前的 IR shape |
| 021–026 | **Rust ABI 起点** + opt-in production gate | A | 021 第一份真正的 Rust |
| 027–030 | **边界开销批**：FFI batching、output sync 延迟、dirty validation、lifecycle skip | B | 027 把 FFI 从 64,064 → 1,001 次 |
| 031–034 | parameter affine、dynamic bus offset、indexed state、static lifecycle | A + B | 034 拿到 1.485× local microbench |
| 035 | state-local + static-branch real-slice verification | A | |
| 036 | transition-unchanged-target fastpath | A | operator |
| 037–038 | static-linear evaluate IR + fast sync | A | operator |
| 039–040 | rust coverage expansion + mixed-small-segment gate | A + B | |
| 041 | transition real top-wall profile + fastpath | mixed | 含 row-specific profile |
| 042–046 | integer state / transition target / timer scan / fixed-index state IR | A | operator 批量 |
| **047** | **MISSING — worklist 原计划"Full Rust scheduler"** | ? | **待用户决策** |
| 048–049 | python-to-rust behavior map + coverage manifest | X (meta-A) | 覆盖率核算工具 |
| 050–054 | transition / timer / cross-above / record-node-id / dynamic-bus primitives | A | Rust 端 operator primitive |
| 055 | event-lifecycle production gate | A | |
| 056 | event-due shadow | B | shadow→production 路径 |
| 057 | event-trace write-set audit | X | |
| 058 | event-body write-set Rust batch | A | |
| 059 | timer-event production gate | A | |
| 060–061 | static-timer-event segment batch + state-owned absolute-timer fastpath | B | batching |
| 062 | fused timer-LFSR output batch | mixed (B→C) | 通往 063 的桥 |
| **063** | **PRBS7 whole-model Rust fastpath** | **C** | 第 1 个 per-circuit |
| 064 | compiler-driven whole-segment lowering | A | **per-circuit 的通用化关键** |
| 065 | semantic-dataflow whole-segment matching | A | 同上 |
| 066–068 | release-wide workplan / coverage manifest generator / ABI contract | X (meta-A) | |
| **069** | top-wall gain-timer production Rust | **C** | gain_estimator |
| **070** | propagation-delay production Rust | **C** | cmp_delay |
| **071** | SAR loop production Rust | **C** | SAR |
| **072** | stage55 CPPLL Rust trace + lean production mode | **C** | CPPLL |
| 073 | Rust speed-claim gate | X | claim 政策 |
| 074 | Rust55 top-wall EVAS smoke | X | measurement |
| **075** | gain measurement-flow production Rust | **C** | gain flow |
| **076** | **current Rustification status after gain flow** | X | **关键状态文档**，主动喊停 per-circuit |
| 077 | whole-segment record/trace copy reduction | D | |
| 078 | global EVAS timing split + persistent worker | B | **persistent worker 起点** |
| 079 | required-signal global trace | D | |
| 080 | evaluate IR piecewise + Rust timer batch | A | |
| 081 | event-body linear Rust batch | A | |
| 082 | timer static-linear whole-segment Rust | A | **generic whole-segment** |
| 083 | record node-id Rust ABI | D | |
| 084 | multi-timer static-linear event-queue Rust | A | generic event queue |
| 085 | cross/above/transition default adaptive trace | A | coverage extension |

**统计**：A 约 53 份、B 约 13 份、C **6 份**（063, 069, 070, 071, 072, 075）、D 约 4 份、X 约 8 份、mixed/missing 约 2 份。
**结论**：过去工作其实 ~90% 是通用方向；C 只是阶段性收果实。问题不是已做了太多 C，而是 **接下来不能继续走 C 路径**。

## 关键观察

1. **Rust 在小 model 上可能比 Python 慢**（来自 audit 030 evidence）：
   ```
   default Python median:  0.333597s
   Rust segment median:    0.395932s
   ```
   未解决前，扩 Rust 覆盖会主动制造回归。这是 P0 优先级的根因。

2. **30% 覆盖 vs 4.08× 加速** 的 13× 比差就是 C 路径的天花板。继续做 C 不会改变这个比。

3. **PFD row Rust 反而慢** 0.98×（audit 076）。`vbr1_l1_pfd_up_dn_logic` 0.174s → 0.177s。小 row 不该投入 Rust。

4. **trace/CSV 是固定开销大头**：r16 CSV writer 改动让 valid43 CSV 时间从 7.74s → 4.27s，但 E2E 只省 6.2s/142.9s（4.4%）。后续 D track 收益边际递减，但仍是必要清理。

5. **未 commit 改动量大**：审查这部分前不要 squash 或 rebase；建议在新 worklist 推进前先 commit 062–085 这批以稳定基线。

## Sleep-After Priority（按通用速度目标重排）

| Order | Audit | Tag | Work Item | Goal | Main Risk | Success Evidence |
|---:|---|---|---|---|---|---|
| P0 | 086 | B | Rust-vs-Python crossover audit | 用真实模型大小扫一条曲线，画出 Rust 在多大 model 起才比 Python 快 | 测试样本不代表 release 分布 | 给出 N（model size 阈值）+ 覆盖到所有 release row size 段 |
| P0 | 087 | B | Persistent worker production gate | 把 078 起头的 persistent worker 推到 default-on | 子进程状态泄漏 | full pytest pass + EVAS subprocess wall 收敛 |
| P0 | 088 | B | Boundary sync zero-copy | 028/029 的 output sync / dirty validation 在 074 之后是否仍是瓶颈 — 重新 profile | 误判已解决 | counters 显示 sync 占比 < 5% subprocess |
| P1 | 089 | A | Verilog-A expression IR | 原 worklist 035 + 080 未完成的部分 — 一般 arithmetic expression lowering | Verilog-A coercion 语义 | release coverage 30% → 50% |
| P1 | 090 | A | Semantic-dataflow matcher v2 | 把 064/065 的 matcher 从手写规则扩到 release-wide 模式识别 | matcher false positive | matcher 覆盖 ≥10 个 release row 而不需要新 audit |
| P1 | 091 | A | system task production gate | $strobe/$display/$random 进入 Rust path | 顺序语义 | system task 不再触发 Python fallback |
| P1 | 092 | D | Sparse required-signal default | 079/083 的 required-signal trace 推到 default | checker contract 漏信号 | CSV 写时间 → ~2s/64-row |
| P2 | 093 | A | dynamic bus 2D / state-index 完整化 | 032 之后的 2D bus、state-index 场景 | event context 边界 | dynamic bus 不再回退 Python |
| P2 | 094 | A | transition / cross / above release-wide production | 055/059/085 的 production gate 推到 release-wide | event ordering | full pytest + production counters |
| P2 | 095 | X | Coverage manifest 自动化 | 049/067 manifest 自动从代码 + IR 推 | matcher drift | CI gate |
| P3 | 096 | X | Same-slice EVAS-vs-Spectre AX rerun | 等 P0/P1 全部落地后做一次 fresh rerun（**经 thu-sui→thu-wei 路径，避免 r15 license-queue 污染**） | runner 路由错误 | repeated cold/warm 数据 |
| P3 | 097 | X | Claim gate update | 按 096 数据更新 MANIFEST.md 的 paper-facing claim | overclaim | claim 报告 |
| **暂停** | — | C | 不再新增 per-circuit whole-segment fastpath | — | — | — |

## 不推荐的方向

- ❌ **不再为单一电路写新的 whole-segment Rust 匹配器**（除非 P1 092/094 完成后仍有 row 占 top-wall > 5%）。如果某个 row 真的需要，先看它是否能 trigger 一个新 generic primitive；不能就保持 fallback。
- ❌ **不在 boundary cost crossover（P0 086）通过前，扩 Rust 覆盖到更小的 model**。
- ❌ **不直接在 thu-wei 上调 Spectre**（参考 audit r15 的污染先例）— 必须走 thu-sui SSH wrapper → thu-wei 路径，license queue 才不会污染 wall time。
- ❌ **不要让 audit number 继续无序增长**。建议从 086 起每完成一个就立即 commit + 在本 worklist 顶部 mark done。

## 决策护栏（写新 audit 时强制满足）

每个新 audit 必须报告：

1. **边界开销 delta**（不只是热路径 delta） — 防止"热点更快但全量更慢"
2. **覆盖类型**：是 generic operator/IR 扩展（A），还是 per-circuit 匹配（C） — C 类需要在 audit 顶部解释为什么不能通用化
3. **Rust crossover model size** — 改动是否在 P0 086 给出的阈值之上有意义
4. **未 commit 改动数** — 不允许 audit 文件提交但代码改动 pending 跨越 3 份以上

## Recommended Next Run

在 P0 086 启动前的预备：

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS

# 1. 测试基线干净
cd evas/rust_core && cargo test --release && cd ../..
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py \
                  tests/test_engine.py tests/test_netlist.py -q

# 2. 把 062-085 的 pending code commit 落地（建议按 audit 分批）
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
git status
# 决定 commit 粒度后再 push

cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval
git status
# 同上

# 3. 跑 audit 076 的 top-wall 10 重做，确认 4.08x 在当前 HEAD 仍成立
# （命令在 reports/rust_stage76_topwall10_current_20260604 的 provenance 字段）
```

## Claim Boundary（沿用 worklist 20260603，保持一致）

可以说：
- 027 证明 batching 显著降低 Rust FFI overhead。
- 034 证明纯静态模型每步空 lifecycle 是真实 Python 内核瓶颈，local static-chain sample 约 1.49×。
- **076 证明 Rust whole-segment 在 top-wall 10 EVAS-only 上可达 4.08×。**
- per-circuit C-track 已达天花板，后续投入应转向 generic A/B/D。

不能说：
- EVAS Rust path 已经全量比默认 Python 更快。
- EVAS 已经 paper-facing 快于 Spectre AX（需 same-slice、同服务器、Spectre-equivalence-gated rerun）。
- 通用 Verilog-A 语义 Rustification 已完成（当前 ~30%，目标 ≥80%）。

## 已确认的决策（2026-06-05）

1. **持续放弃 per-circuit C-track 新增**：用户确认"做通用的改动"，模式 C 只保留已完成的 6 份作为底层 primitive 的验证证据。
2. **persistent worker（P0 087）默认开启**：用户接受 cross-row state leakage 风险，"出现 bug 再修"；不在 P0 087 前置 isolation regression 测试。
3. **Spectre 必须走 thu-sui→thu-wei**：直接在 thu-wei 上跑 Spectre 会撞 license queue → r15 污染。所有 P3 096 fresh AX rerun 走 thu-sui wrapper，不存在"license 稳定窗口"的问题，只有"runner 路由是否正确"的问题。

## 待用户决策

1. **audit 047 缺号**：补写一个"intentionally retired"的 stub，还是把 047 编号留空跳过？
