# 073 - Rust Speed Claim Gate

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related files:

- `runners/report_vabench_release_rust_speed_claim_gate.py`
- `tests/test_vabench_release_rust_speed_claim_gate.py`
- `speed-optimization/reports/rust_speed_claim_gate_073_20260604.json`
- `speed-optimization/reports/rust_speed_claim_gate_073_20260604.md`

## One-Line Summary

把 072 暴露出来的两个 claim 缺陷变成机器 gate：当前只允许 `stage55_topwall_engineering_speedup` 这个 EVAS-only 工程 claim；`full_release_rustification` 和 `evas_faster_than_spectre_ax` 都被明确关闭，并输出具体 blocker。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Claim policy | 只能靠文档说明“不能 claim 全量 Rust 化/快于 AX” | 新增 `report_vabench_release_rust_speed_claim_gate.py` 生成 JSON/MD gate | 报告里能直接看到 claim 是否打开 |
| Full Rustification gate | 072 的 `80.6%` 可能被误读成全量 Rust 化 | gate 读取 release coverage manifest，要求接近全量 production coverage | 当前因 `30.0%` 和 15 类 behavior blocker 关闭 |
| Spectre AX speed gate | 072 没有和 AX 同机对比，容易被口头混用历史结果 | gate 要求 same-server artifact 中同时存在 EVAS `profile_fast_rust_55` 和 Spectre AX mode | 当前旧 fourway artifact 有 AX 但缺 `profile_fast_rust_55` |
| Tests | 没有锁住 claim gate 语义 | 新增 3 个单测覆盖 current blocker 和 synthetic pass case | 防止后续改脚本时过 claim |

## Principle

这个改动不直接加速 EVAS。它补的是实验/claim 缺陷：

1. **工程阶段 claim**：允许 072 的 top-wall EVAS-only stage claim，因为它有 rows、PASS、wall speedup 和 weighted completion。
2. **全量 Rust 化 claim**：必须看 release-wide semantic coverage，而不是 top-wall 权重。只要 B01-B18 中还有 present rows 处于 `partial`、`shadow_only`、`python_only` 或 `not_implemented`，就不能 claim。
3. **快于 Spectre AX claim**：必须看同 slice、同 server、同设置、同 mode 的 EVAS/Spectre AX artifact。历史 AX artifact 不能和新的 rust55 EVAS-only run 拼接。

## Current Gate Result

Canonical report:

```text
speed-optimization/reports/rust_speed_claim_gate_073_20260604.json
speed-optimization/reports/rust_speed_claim_gate_073_20260604.md
```

| Claim | Allowed | Blockers |
|---|---:|---|
| `stage55_topwall_engineering_speedup` | `True` | none |
| `full_release_rustification` | `False` | `release_rustification_percent_below_full_threshold`, `non_production_behavior_status_present` |
| `evas_faster_than_spectre_ax` | `False` | `same_server_artifact_claim_allowed_false`, `missing_evas_mode_summary`, `missing_comparable_total_wall` |

## Current Defects Made Explicit

### Full Rustification

| Metric | Current |
|---|---:|
| Release model rows scanned | `357` |
| Rustification estimate | `30.0%` |
| Full-claim threshold | `99.9%` |
| Behavior blocker count | `15` |
| Invalid whole-segment candidates | `0` |

Top blockers:

| ID | Status | Present rows |
|---|---|---:|
| `B01` | `partial` | 357 |
| `B02` | `partial` | 357 |
| `B03` | `partial` | 354 |
| `B07` | `shadow_only` | 350 |
| `B08` | `partial` | 350 |
| `B09` | `partial` | 278 |
| `B10` | `partial` | 327 |
| `B12` | `python_only` | 10 |
| `B16` | `python_only` | 90 |
| `B18` | `not_implemented` | 357 |

### Spectre AX Speed

The current same-server diagnostic artifact is:

```text
speed-optimization/reports/current_fourway_topwall10_clean_20260604.json
```

It contains Spectre AX `ax_speed` with total wall `42.51042721234262s`, but it does
not contain EVAS `profile_fast_rust_55`. Therefore the gate cannot compute
AX/EVAS rust55 speedup. The artifact also has `claim_allowed=false`, so it is
diagnostic even for its own original mode set.

## Validation

Commands run:

```bash
PYTHONPATH=behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_claim_gate \
python3 behavioral-veriloga-eval/runners/report_vabench_release_rust_speed_claim_gate.py \
  --same-server-json speed-optimization/reports/current_fourway_topwall10_clean_20260604.json

PYTHONPATH=behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_claim_gate \
python3 -m pytest behavioral-veriloga-eval/tests/test_vabench_release_rust_speed_claim_gate.py -q

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_claim_gate \
python3 -m py_compile \
  behavioral-veriloga-eval/runners/report_vabench_release_rust_speed_claim_gate.py \
  behavioral-veriloga-eval/tests/test_vabench_release_rust_speed_claim_gate.py
```

Results:

```text
claim gate generation: stage=True full_rust=False ax_speed=False
pytest test_vabench_release_rust_speed_claim_gate.py: 3 passed
py_compile: PASS
```

## Learning Notes

这一步的价值是把“不能 claim”从主观判断变成可执行规则。以后每次补一个 Rust production path 或跑一次 Spectre AX 对照，都可以重跑这个 gate：

- 如果只优化 top-wall EVAS，stage gate 可能继续通过，但 AX gate 不会自动打开。
- 如果只跑旧 EVAS fast vs AX，AX gate 仍会因为缺 `profile_fast_rust_55` 而关闭。
- 如果 Rust primitive 只是 shadow/parity，不是 production coverage，full Rustification gate 仍会关闭。

## Next Step

下一步才是真正补性能/覆盖：

- 跑 `profile_fast_rust_55` vs Spectre AX same-server dual rerun，补 AX speed gate；
- 继续把 B07/B08/B09/B10/B18 这些大面积 partial/shadow/Python-owned behavior 迁到 production Rust/array path，补 full Rustification gate。
