# EVAS2 当前 artifact 索引

日期：2026-06-06

这个索引只列 P0/P1 收口需要看的主线 artifact。`speed-optimization/reports/` 下仍有大量历史 smoke、失败尝试和诊断报告，默认不作为当前结论入口。

## 必读文档

| 文件 | 用途 | 当前结论 |
|---|---|---|
| `speed-optimization/rust-kernel/EVAS2_P0P1_CLOSEOUT_20260606.md` | P0/P1 中文收口报告 | 当前能说什么、不能说什么、clean smoke 数字 |
| `speed-optimization/rust-kernel/audits/114-full-release-rust-py-spectre-fourway.md` | 四路审计 | Rust EVAS2 / Python EVAS fast / Spectre AX 均 271/271 PASS，Spectre strict 267/271 checker PASS |
| `speed-optimization/rust-kernel/audits/115-auto-row-checker-sparse-trace-contract.md` | sparse trace 审计 | full release EVAS2 271/271 PASS，fallback 0，E2E 69.952s -> 59.418s |
| `speed-optimization/rust-kernel/audits/116-generic-checker-runtime-hot-rows.md` | checker runtime 审计 | hot-row checker 11.618s -> 0.221s |
| `speed-optimization/rust-kernel/RUST_NEGATIVE_ATTEMPT_STOPLIST_20260605.md` | 负优化停用清单 | 避免重复走 per-step FFI / wrapper 负优化路线 |
| `speed-optimization/rust-kernel/EVAS2_PY_COMPATIBILITY_CAPABILITY_AUDIT_20260606.md` | Python/Rust 能力差异表 | 说明为什么 release PASS 不等于全语言 Rust 化 |

## 主线机器可读报告

| 文件 | 类型 | 是否建议提交 | 说明 |
|---|---|---:|---|
| `speed-optimization/reports/full_release_fourway_rust_py_spectre_summary_20260606.json` | compact summary | yes | 四路审计摘要，最适合复核 claim |
| `speed-optimization/reports/full_release_rows_for_fourway_20260606.json` | row manifest | yes | 271-row 输入清单 |
| `speed-optimization/reports/full_release_evas2_auto_row_trace_20260606_r4_summary.json` | compact summary | yes | 115 的 full release 摘要 |
| `speed-optimization/reports/checker_runtime_116_rowbased_20260606.json` | 10-row before | yes | 116 row-based 对照 |
| `speed-optimization/reports/checker_runtime_116_streaming_20260606.json` | 10-row after | yes | 116 streaming/runtime 对照 |
| `speed-optimization/reports/evas2_p0p1_clean_smoke_summary_20260606.json` | compact summary | yes | 当前代码 271/271 PASS 摘要 |
| `speed-optimization/reports/full_release_evas_py_rust_after_fixes_20260606.json` | full EVAS A/B | no | 约 38MB，留本地，不进 PR |
| `speed-optimization/reports/full_release_spectre_ax_strict_20260606.json` | full Spectre A/B | no | 约 4.9MB，留本地，不进 PR |
| `speed-optimization/reports/full_release_evas2_auto_row_trace_20260606_r4.json` | full EVAS2 sparse trace | no | 约 7.6MB，提交 compact summary 和 MD |
| `speed-optimization/reports/evas2_p0p1_clean_smoke_20260606.json` | clean smoke raw | no | 约 7.6MB，提交 compact summary 和 MD |

## 人类可读报告

| 文件 | 用途 |
|---|---|
| `speed-optimization/reports/full_release_evas_py_rust_after_fixes_20260606.md` | 本地 Python/Rust EVAS 对比 |
| `speed-optimization/reports/full_release_spectre_ax_strict_20260606.md` | Spectre AX/strict 对比 |
| `speed-optimization/reports/full_release_evas2_auto_row_trace_20260606_r4.md` | sparse trace full-release 报告 |
| `speed-optimization/reports/checker_runtime_116_rowbased_20260606.md` | checker runtime before |
| `speed-optimization/reports/checker_runtime_116_streaming_20260606.md` | checker runtime after |
| `speed-optimization/reports/evas2_p0p1_clean_smoke_20260606.md` | P1 当前 clean smoke |

## 不作为当前结论入口的内容

| 内容 | 处理方式 |
|---|---|
| `results/` 下的仿真输出 | 不提交，属于 raw simulator output |
| `benchmark-vabench-release-v1/rerun_staging*` | 不提交，属于历史 staging |
| 旧 `e2e_wall_profile_*` / `rust_stage*` smoke | 仅作历史诊断，不作为当前 P0/P1 入口 |
| mismatch triage CSV/JSON/MD | 不并入本 PR，除非后续单独整理 baseline/mismatch PR |

## 读数注意事项

114/115 的 full release speed 数字使用 persistent worker 和更适合工程上限的 runner 口径；P1 clean smoke 没有复用 persistent worker，所以 E2E wall 更慢。两者都有效，但回答的问题不同：

- 114/115：Rust core 和 checker/runtime 优化在理想工程 runner 下能带来多少收益。
- P1 clean smoke：当前代码从普通 runner 调起是否还能 271/271 PASS。

对外汇报时不要把跨机器 Spectre 数字写成最终 speed claim。Spectre AX/strict 通过 `thu-sui -> thu-wei`，EVAS 当前在本地 Mac；它们只能说明诊断趋势，paper-facing claim 还需要同 host class 重跑。
