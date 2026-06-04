# 067 - Release Rust Coverage Manifest Generator

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/current_release_rust_coverage_manifest_20260604.json`
- `speed-optimization/reports/current_release_rust_coverage_manifest_20260604.md`

## One-Line Summary

新增 release 全量 Rust 覆盖率 manifest 生成器，扫过 79 个 release entry / 357 个 gold `.va`，并修正 `weighted_dac_v1` whole-segment 语义匹配过宽导致的状态机误命中。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| release coverage audit | 没有 release-wide per-model Rust 覆盖报告，只能靠 top-wall 局部实验判断 | `report_vabench_release_rust_coverage_manifest.py` 编译并审计所有 release gold `.va` | 默认仿真行为不变 |
| candidate accounting | whole-segment candidate 没有全量分布表 | 报告记录 `static_linear_ir`、`transition_target_ir`、`whole_segment_candidate` 等信号计数 | 默认仿真行为不变 |
| weighted DAC semantic matcher | 只看多路 `cross()` 和一个 `transition()` 输出，容易把 debounce/lock detector 状态机误认为 DAC | 额外要求至少 3 个 input-cross branch 控制 self-accumulating weighted update | 默认仿真行为不变，减少错误 fastpath 风险 |
| regression tests | 没有 release-wide manifest smoke，也没有 DAC 误命中反例 | 新增 manifest smoke/filter 测试和两个真实 false-positive gold 回归 | 默认仿真行为不变 |

## Principle

这一阶段不是直接加速阶段，而是后续 Rust 化的测量边界。核心目标是回答两个问题：

- **哪些 release gold 模型已经有 Rust metadata / Rust candidate？**
- **哪些候选是真正语义匹配，而不是名字或形状碰巧相似？**

如果没有这个边界，后续会反复出现一个问题：局部 fastpath 在少数样例上看起来快，但换到全量 benchmark 后覆盖很低，或者更糟糕的是错误命中功能不同的模型。067 用全量 manifest 把这种风险提前暴露出来。

`weighted_dac_v1` 的修正就是一个例子。DAC 的关键语义不是“很多输入边沿 + 一个模拟输出”，而是“多个输入 bit 控制同一个累加量，每个 bit 贡献一个权重”。所以 matcher 现在要求 cross 对应的条件分支里存在 self-accumulating assignment，例如 `code = code + weight`。这样 debounce latch、lock detector 这类多事件状态机不会被误判为 DAC。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| release gold `.va` compile pass | not measured release-wide | `357 / 357` | manifest 可以覆盖当前 release package |
| release entries scanned | not measured release-wide | `79` | 覆盖完整 release entry 集合 |
| full Rustification estimate | informal | `30.0%` | 基于 B01-B18 seed 状态的工程估计，不是速度 claim |
| `weighted_dac_v1` candidates | `13` | `2` | 误命中的状态机被过滤，candidate 更可信 |
| whole-segment candidates | `34` | `23` | 数量下降是正确性收紧，不是覆盖退化 |
| EVAS subprocess wall | unchanged | unchanged | 这一步没有接入新的 production Rust fastpath |
| direct speedup | `0%` | `0%` | 067 是 audit/safety gate，不是性能优化本体 |
| checker/result parity | unchanged | targeted compiler tests pass | 默认仿真路径不变 |

当前全量报告摘要：

| Item | Count |
|---|---:|
| model rows | `357` |
| compile pass | `357` |
| unique gold source hashes | `152` |
| duplicate gold source rows | `205` |
| `transition_target_ir` rows | `328` |
| `ordered_transition_shadow` rows | `262` |
| `whole_segment_candidate` rows | `23` |
| `state_owned_timer_fastpath` rows | `14` |
| `dynamic_bus_metadata` rows | `7` |
| `static_linear_ir` rows | `4` |
| `event_lfsr_batch` rows | `2` |

Whole-segment candidate 分布：

| Candidate | Rows |
|---|---:|
| `cmp_delay_log_transition_v1` | `4` |
| `cppll_timer_v1` | `2` |
| `cross_scalar_lfsr_transition_bus_v1` | `3` |
| `edge_interval_timer_v1` | `4` |
| `gain_timer_reduction_v1` | `2` |
| `ref_step_clock_v1` | `2` |
| `sample_hold_rising_v1` | `2` |
| `weighted_dac_v1` | `2` |
| `weighted_sar_adc_v1` | `2` |

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile EVAS/evas/simulator/backend.py EVAS/tests/test_rust_backend.py behavioral-veriloga-eval/runners/report_vabench_release_rust_coverage_manifest.py behavioral-veriloga-eval/tests/test_vabench_release_rust_coverage_manifest.py

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest EVAS/tests/test_rust_backend.py::test_compiler_emits_topwall_whole_segment_candidates_from_semantic_gold EVAS/tests/test_rust_backend.py::test_compiler_rejects_weighted_dac_false_positive_state_machines -q

PYTHONPATH=behavioral-veriloga-eval/runners:EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m pytest behavioral-veriloga-eval/tests/test_vabench_release_rust_coverage_manifest.py -q

PYTHONPATH=behavioral-veriloga-eval/runners:EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 behavioral-veriloga-eval/runners/report_vabench_release_rust_coverage_manifest.py
```

Results:

```text
2 passed in 0.40s
2 passed in 0.46s
wrote release rust coverage manifest: rows=357 compile={'pass': 357} estimate=30.0% report=speed-optimization/reports/current_release_rust_coverage_manifest_20260604.json
```

## Learning Notes

**Rust 覆盖率**不是“代码里有没有 Rust 函数”。它要看真实 Verilog-A 模型里的行为能否被编译器识别成某种稳定的 IR，然后在运行时把这一整段行为交给 Rust 执行。

一个模型可能已经有很多 Rust metadata，比如 transition target IR，但仍然没有速度提升。原因是 metadata 可能还在 shadow/parity 或 candidate 阶段，没有替换 production Python 执行路径。

**whole-segment candidate** 是比单个表达式更大的单位。它表示编译器认为一个模型或模型片段符合某种完整行为模板，例如 CPPLL timer、weighted SAR ADC、gain measurement flow。只有 candidate 足够语义化，后续才适合接 Rust production ABI。

**误命中比漏命中更危险。** 漏命中只是回退 Python，速度慢一些；误命中可能把功能不同的模型交给错误 Rust fastpath，导致结果错误。因此 067 宁可把 `weighted_dac_v1` 从 13 个收紧到 2 个。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| coverage manifest 被误用成 paper-facing speed claim | 报告没有 EVAS/Spectre same-slice timing | 保留 `claim_policy.paper_speed_claim_allowed=false` |
| semantic matcher 收得过紧，漏掉未来真实 DAC 变体 | 新 DAC 模型不出现 `weighted_dac_v1` candidate | 扩展 `_whole_segment_weighted_accumulator_nodes()`，但必须先加正反例 |
| semantic matcher 仍过宽 | false-positive regression 失败或报告中候选异常增加 | 回退 `EVAS/evas/simulator/backend.py` 中 weighted DAC matcher 改动 |

## Completion And Speed Ledger

| Item | Value |
|---|---:|
| Full Rustification completion after 067 | `30.0%` |
| Completion delta from production Rust | `+0.0%` |
| Direct speed improvement | `0%` |
| Main value | release-wide measurable coverage and safer candidate gate |

## Next Step

下一篇审计文档编号和预期主题：

- `068 - Whole-Segment Rust ABI Contract`
