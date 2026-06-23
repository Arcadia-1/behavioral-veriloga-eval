# EVAS Rustification Worklist - 2026-06-06

Status: `active`

Replaces: `RUSTIFICATION_WORKLIST_20260605.md`（覆盖 001-085；本版本扩展到 086-095 + Stage 6 commit landed + codex handoff prepared）

## Current Position (2026-06-06)

- **已完成 audit**：**001–095**（047 仍缺号；065 series 中通过 086-095 一线推进）
- **本会话主线产出**（2026-06-05 → 2026-06-06）：
  - 086 transition buffer reuse + 088 per-step batch + 089 cross/above production (negative result documented)
  - 091a-d generic candidate matcher + dispatcher + Python executor
  - 092 real-row validation (5 rows, 33× geomean)
  - 093 53-row sweep (14.4× geomean, 0 fallback)
  - 094 design doc for Verilog-A → Rust kernel multi-week project
  - 095 record adaptive substeps (parity 0/53→38/53 within 5%)
- **Stage 6 (EVAS 26k 行 commit hygiene)**：✅ **完成**（commit `0e4b74d` on EVAS）— landed 037-085 series code + 086-095 incremental work
- **未提交改动**：现在为 0（全部 push 到 origin）
- **当前可 claim 的速度数据**：
  - Opt-in `rust_full_model_fastpath=True`：top-wall 10 EVAS-only **4.08×**（audit 076）
  - Opt-in `rust_full_model_fastpath + generic_executor=True`：**14.4× geomean on 53 candidates**（audit 093）
  - Opt-in `rust_transition_production=True`：transition-heavy +2.8% real（audit 088）
  - 默认（无 flag）：基线不变，0% 提速
- **Release-wide 通用语义 Rustification**：
  - 091b matcher 覆盖：234/357 (65.5%) release rows
  - whole_segment_candidate 覆盖：23/357 (6.4%) — specific candidate kinds
  - 总 metadata 覆盖：257/357 (72.0%)

## 关键发现 / 工程教训（本会话）

| 教训 | 数据来源 | 影响后续设计 |
|---|---|---|
| Per-call FFI on hot-but-cheap functions = net loss | 089: cmp_delay 3× **slower** | 不要再做单调用 Rust 替换；必须 batch 或 bypass |
| Bypass Python orchestration loops = big win | 091d: 10-100× real-row speedup | 094 项目的核心 thesis |
| Synthetic ≠ real | 091d 507× synthetic vs 33× initial vs 14.4× sweep | 必须双重 bench 才能 claim |
| 5-repeat noise outliers 可放大 4× | 088 5-repeat 报 1.24×，15-repeat trimmed 真实 1.029× | 默认 15-repeat trimmed mean |
| Bundled commit 损失 attribution | EVAS commit 2c754c7 bundle 27k 行 | 永远不要用 `git commit -am`；one audit per commit |
| Untracked 文件易被遗漏 | bundled commit 漏 2 文件 → broken origin → 已 fix | `git status` 必须看完 ?? 段才能 commit |

## 已落地 Opt-in 矩阵（用户视角）

| Flag | 真实工况效果 | 覆盖 | 推荐 |
|---|---|---|---|
| `rust_transition_production=True` | +2.8% real | transition-heavy 模型 | ✅ 可开 |
| `rust_full_model_fastpath=True` | 4.08× top-wall 10 | 23/357 specific 电路 | ✅ 强烈推荐 |
| `+ generic_executor=True` | **14.4× geomean** | 234/357 generic 电路 | ✅ 推荐（CSV 非 bit-exact）|
| `rust_timer_event=True` | 小幅 | timer-heavy 模型 | ✅ 可开 |
| `rust_event_interpolation=True` | 不变慢 | event body 读节点的模型 | ✅ 可开 |
| `rust_static_eval=True` | 小幅 | static-linear 模型 | ✅ 可开 |
| `rust_cross_above_production=True` | **-198%（3× 变慢）** | — | ❌ **不要开** |

## 后续路径：094 项目（已 handoff to codex）

**当前所有人工 effort 都应集中在 094 项目**。状态：
- ✅ Design audit 094 已写
- ✅ Stage 2-4 detailed plan 已 commit（STAGE_2_4_EXECUTION_PLAN.md）
- ✅ Handoff doc 已写（HANDOFF_TO_CODEX_094_PROJECT.md）— codex 可以从这里 self-contained 起手
- ⏳ Implementation: 094a-094k 各 audit，估算 20-50 小时 across 5 sessions

**目标**：解决 091d 的 parity gap，让 generic executor 能 default-on，普通用户自动得到 10-50× 提速 + bit-exact CSV。

**完成判据**（写在 handoff doc 里）：
1. ≥90% sweep 行 bit-exact CSV parity vs Python adaptive
2. Wall ≥2× over 091d Python executor
3. Default-on flag flipped OR 文档化 opt-in with specific reasons

## Stage 5 (Paper Claim) — Runner Ready

`runners/run_audit_098_same_server_spectre_rerun.py` 已 commit，含 thu-sui hostname 检查。

执行触发条件：
1. 094 项目完成（普通用户 default 自动得到 Rust 化速度）
2. 用户在 thu-sui 上 schedule 1 day 仿真时间
3. 跑 vabench release-v1 全量 same-slice

输出：`results/audit_098_rerun_<date>/` 含 manifest.json + summary.md（paper-table 草稿）

## Decision Gates Still Open

| Decision | 何时定 | 决策依据 |
|---|---|---|
| 047 缺号怎么处理 | codex 起手前 | retire 还是补写 stub |
| 5 outlier rows in 091d sweep (PGA, precision rectifier, ramp_or_step, PFD, peak detector) | 094 完成后 | IR + Rust kernel 是否自动解决；若不解决要单独 audit |
| `generic_executor` default-on flip | 094k | 取决于 sweep bit-exact 率 |
| Paper claim filing | Stage 5 完成后 | 决定提交哪个 conference |

## What's NOT Being Worked On

| 不做的 | 原因 |
|---|---|
| Per-circuit C-track 新增（069-075 模式 expansion） | audit 076 自己叫停；ROI 已天花板 |
| 089 cross/above production 推 default | 数据证明负优化 |
| CSV writer 优化 | cmp_delay profile 显示 0.04% 占比 |
| KCL/KVL / transistor / AC/DC | 永远 out of scope（EVAS 设计边界）|
| 多 instance / 层次模型 | 091b matcher 显式排除；扩展超 094 scope |

## Next Step Recommendations (按 ROI 排)

1. **Codex 接手 094a**（参考 `HANDOFF_TO_CODEX_094_PROJECT.md` Required Reading 顺序）
2. 用户：commit/run 092 后 thu-sui 调度时间窗口（为 Stage 5 准备）
3. 若 094 项目超过 50 小时：考虑只做到 Phase 2（IR + Rust executor），跳过 Phase 3 integration，让 091d Python 仍是 production path

## Claim Boundary（写进 MANIFEST.md 时用）

可以说：
- EVAS 内已建好完整 opt-in Rust 化 infrastructure（matcher / dispatcher / executor / 14 个 operator primitive / 9 specific whole-segment + 1 generic）
- `rust_full_model_fastpath + generic_executor` 在 53 真实 vabench rows 上 wall 平均 14.4× 提速，**0 fallback**
- 4.08× speedup on top-wall 10 EVAS-only via specific candidate path（076）
- 086-095 series 0 regression（全量 606 测试通过）

不能说：
- EVAS 全量 Rust 化（仍有 Python interpreter 跑 evaluate body — 094 项目 future）
- 默认快于 Python adaptive（所有提速 opt-in）
- bit-exact CSV parity（38/53 sweep 行 <5%，5 outlier >50%）
- EVAS paper-facing 快于 Spectre AX（待 Stage 5 same-server rerun）
- Release-wide 速度 claim（仅 vabench tb-form candidates 子集）

---

## 文档地图（codex / 未来读者起点）

| 想做什么 | 读什么 |
|---|---|
| 接 094 项目 | `HANDOFF_TO_CODEX_094_PROJECT.md` |
| 看本会话主要技术成果 | audits 086-095 按编号 |
| 看 5 个工程教训具体数据 | 086, 088, 089, 091d, 095 audits 的 Claim Boundary 节 |
| Stage 2-4 怎么拆 session | `STAGE_2_4_EXECUTION_PLAN.md` |
| Stage 5 paper rerun | `runners/run_audit_098_same_server_spectre_rerun.py` 顶部 docstring |
| Stage 6 实际 commit 内容 | `STAGE6_BUNDLED_COMMIT_NOTE.md` |
| 现有 candidate / IR / Rust 函数清单 | audit 094 design doc 的"What Already Exists"节 |
| 全 release coverage 数 | `reports/current_release_rust_coverage_manifest_20260604.json` |

## Recommended Night Run (continuation script for next session)

```bash
# 1. EVAS repo clean state confirm
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
git status         # should be clean
git pull           # if codex pushed work
PYTHONPATH=. python3 -m pytest tests/ -q   # confirm 606+ baseline

# 2. behavioral-veriloga-eval repo confirm
cd ../behavioral-veriloga-eval
git status && git pull

# 3. If continuing as codex (094 project):
cat speed-optimization/rust-kernel/HANDOFF_TO_CODEX_094_PROJECT.md

# 4. If continuing as user reviewing:
cat speed-optimization/rust-kernel/RUSTIFICATION_WORKLIST_20260606.md
```
