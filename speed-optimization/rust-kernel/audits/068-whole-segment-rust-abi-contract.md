# 068 - Whole-Segment Rust ABI Contract

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/current_release_rust_coverage_manifest_20260604.json`
- `speed-optimization/reports/current_release_rust_coverage_manifest_20260604.md`

## One-Line Summary

把 whole-segment candidate 从隐式 tuple 口径推进到可验证 ABI contract：每种 candidate 的 kind、arity、字段名、字段类型和跨字段约束现在都有统一 validator。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| whole-segment ABI | engine 按 tuple 下标拆字段，字段顺序/类型只靠人工记忆 | `evas/simulator/whole_segment.py` 定义 candidate schema 和 validator | 默认仿真行为不变 |
| compiler candidate gate | collector 返回 tuple 后直接放进 `_whole_segment_candidates` | candidate 必须 `validate_whole_segment_candidate(...).valid` 才会暴露给 engine | 默认仿真行为不变 |
| release coverage report | 只统计 candidate kind | 每个 candidate 附带 contract schema version、field names、arity、valid/errors | 默认仿真行为不变 |
| tests | 只验证真实 gold 能产生 candidate | 增加 ABI bad-arity/bad-width 反例，并要求真实 gold candidate contract valid | 默认仿真行为不变 |

## Principle

Rust production path 最怕 silent wrong ABI。现在的 whole-segment fastpath 本质上是：

1. compiler 从 Verilog-A AST 推断一个行为片段；
2. compiler 把该行为片段编码成 tuple；
3. engine 或 Rust 后端按字段顺序解释这个 tuple。

如果 tuple 字段顺序、数量、类型错了，Python 可能只是 fallback，也可能在更深的位置用错端口或参数。068 先把这层协议显式化，避免 069 接 Rust production ABI 时继续堆隐式约定。

这一步属于**正确性和可维护性门槛**，不是直接降低每步成本、减少仿真步数或减少输出开销。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| whole-segment schema version | none | `evas-whole-segment-candidate-contract.v1` | ABI 合同可审计 |
| release gold `.va` compile pass | `357 / 357` | `357 / 357` | validator 没有破坏当前 release compile |
| whole-segment candidates | `23` | `23` | 当前候选没有被误杀 |
| invalid whole-segment candidates | not measured | `0` | 当前 release candidate 都满足 ABI contract |
| full Rustification estimate | `30.0%` | `30.0%` | 未新增 production Rust 行为覆盖 |
| direct speedup | `0%` | `0%` | 这一步没有替换运行时 hot loop |

当前 ABI contract 覆盖的 candidate kinds：

| Candidate | Contracted fields |
|---|---:|
| `cross_scalar_lfsr_transition_bus_v1` | `15` |
| `gain_timer_reduction_v1` | `14` |
| `cmp_delay_log_transition_v1` | `14` |
| `edge_interval_timer_v1` | `5` |
| `weighted_sar_adc_v1` | `14` |
| `weighted_dac_v1` | `5` |
| `sample_hold_rising_v1` | `8` |
| `ref_step_clock_v1` | `8` |
| `cppll_timer_v1` | `21` |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile EVAS/evas/simulator/whole_segment.py EVAS/evas/simulator/backend.py EVAS/tests/test_rust_backend.py behavioral-veriloga-eval/runners/report_vabench_release_rust_coverage_manifest.py behavioral-veriloga-eval/tests/test_vabench_release_rust_coverage_manifest.py

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest EVAS/tests/test_rust_backend.py::test_compiler_emits_topwall_whole_segment_candidates_from_semantic_gold EVAS/tests/test_rust_backend.py::test_whole_segment_candidate_contract_rejects_bad_abi_shapes EVAS/tests/test_rust_backend.py::test_compiler_rejects_weighted_dac_false_positive_state_machines -q

PYTHONPATH=behavioral-veriloga-eval/runners:EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest behavioral-veriloga-eval/tests/test_vabench_release_rust_coverage_manifest.py -q

PYTHONPATH=behavioral-veriloga-eval/runners:EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 behavioral-veriloga-eval/runners/report_vabench_release_rust_coverage_manifest.py
```

Results:

```text
3 passed in 0.63s
2 passed in 0.67s
wrote release rust coverage manifest: rows=357 compile={'pass': 357} estimate=30.0% report=speed-optimization/reports/current_release_rust_coverage_manifest_20260604.json
whole_segment_invalid_candidate_count = 0
```

## Learning Notes

ABI 可以先理解成“两个模块之间怎么传数据的合同”。这里的两个模块是 compiler 和 fastpath executor。compiler 说“我发现了一个 `weighted_sar_adc_v1`”，它不能只给一个散乱 tuple；它必须说明第 1 个字段是输入端口、第 4 个字段是 `dout_ports`、第 13 个字段是 `width`，而且 `len(dout_ports)` 必须等于 `width`。

这和 Rust 的关系是：Rust 很快，但 Rust 不会自动理解 Verilog-A 语义。我们必须先把 Python compiler 推断出来的行为，变成一个稳定、类型明确、可检查的输入结构。否则 Rust 跑得再快，也可能是在跑错东西。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| schema 太严格，未来合法变体被过滤 | 新 gold 模型 compile pass 但 candidate 缺失 | 扩展 `EVAS/evas/simulator/whole_segment.py` 对应 schema/constraint，并加正例 |
| schema 太宽，错误 candidate 仍进 fastpath | `whole_segment_invalid_candidate_count=0` 但 parity 失败 | 收紧 schema 的 cross-field constraint，并加反例 |
| report 被误读成速度提升 | 067/068 都无 same-slice timing | 保留 direct speedup `0%`，不进入 paper-facing speed claim |

## Completion And Speed Ledger

| Item | Value |
|---|---:|
| Full Rustification completion after 068 | `30.0%` |
| Completion delta from production Rust | `+0.0%` |
| Direct speed improvement | `0%` |
| Main value | whole-segment Rust production ABI is now gated by explicit contract |

## Next Step

下一篇审计文档编号和预期主题：

- `069 - Top-Wall Whole-Segment Production Rust`
