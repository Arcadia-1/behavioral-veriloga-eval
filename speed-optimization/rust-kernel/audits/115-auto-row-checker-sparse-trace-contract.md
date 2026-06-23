# 115 - Auto Row Checker Sparse Trace Contract

Status: `done`

Date: `2026-06-06`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/auto_row_trace_contract_30_20260606.json`
- `speed-optimization/reports/auto_row_trace_contract_30_off_20260606.json`
- `speed-optimization/reports/full_release_evas2_auto_row_trace_20260606_r2.json`
- `speed-optimization/reports/full_release_evas2_auto_row_trace_20260606_r3.json`
- `speed-optimization/reports/full_release_evas2_auto_row_trace_20260606_r4.json`

## One-Line Summary

把 row-based checker 的必需信号自动推断成 EVAS sparse trace contract，让 release runner 默认少写、少读、少检查无关 CSV 列。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| runner trace contract | 只有显式 streaming checker 会把 required signals 下发给 EVAS；大多数 row-based checker 仍输出完整 trace | `simulate_evas.py` 从 checker 源码推断 literal required set、结构化 bit 列、简单 f-string range、`indexed_columns()` 和 prefix bit families | checker pass/fail 口径不变；EVAS run 可输出更窄的 `tran.csv` |
| correctness guard | sparse contract 若漏列，会直接让 checker fail | row-based auto sparse 失败时，runner 清理 stale output 后自动 full-trace rerun，并记录 fallback note/timing | release r4 full run fallback 为 0；fallback 只作为安全阀 |
| environment handling | `EVAS_REQUIRED_TRACE_SIGNALS` 可能从外部环境泄漏到 full-trace path | `run_evas()` 在无 required trace 时显式 `env.pop()` | full-trace/fallback 语义更干净 |
| report metadata | checker policy 只区分 checker implementation | policy/timing 中记录 `trace_contract_kind` 和 `trace_contract_signal_count` | 后续可审计哪些 row 走 sparse trace |

## Principle

这次不是 Rust 内核语义迁移，而是 **减少输出/检查开销**。

原来的流程是：EVAS 仿真后把很多 checker 不会看的信号也写进 CSV，row-based checker 再用 Python/pandas 读整张表。对很多短 row 来说，真正的 Rust core 已经很快，剩下的等待时间主要在 CSV、checker 和 runner。

新的流程是：runner 先根据 checker 源码推断“这个 checker 实际会读哪些列”，再把这些列通过 `EVAS_REQUIRED_TRACE_SIGNALS` 下发给 EVAS。EVAS 只记录 checker 必需列，checker 仍用原逻辑判断，因此功能口径不变。

可以把它理解成：不是让仿真器算得更快，而是让仿真器不要把不用的波形搬来搬去。小 row 里搬数据和读 CSV 的成本会压过内核成本，所以这类优化会直接反映到 E2E wall。

## Before / After Evidence

对照口径：

- Before：`full_release_evas2_sidefx_persist_20260606.json`
- After：`full_release_evas2_auto_row_trace_20260606_r4.json`
- 范围：271 个 release selected rows，`profile_fast_evas2`，persistent worker。

| Metric | Before | After | Speedup / delta | Interpretation |
|---|---:|---:|---:|---|
| checker pass | 271/271 | 271/271 | unchanged | 功能口径未降低 |
| auto sparse fallback | n/a | 0 | clean | r4 没有需要回退 full trace 的 row |
| E2E wall total | 69.952s | 59.418s | 1.177x / -10.534s | 总等待时间下降约 15.1% |
| EVAS subprocess wall | 10.420s | 8.202s | 1.270x / -2.218s | EVAS 输出/trace 相关外层成本减少 |
| CSV write | 1.533s | 1.335s | 1.148x / -0.198s | 写 CSV 的直接收益较小但稳定 |
| behavior checker | 54.244s | 46.245s | 1.173x / -7.999s | row checker 少读无关列，收益最大 |

r4 trace contract 覆盖：

| Contract kind | Rows | Meaning |
|---|---:|---|
| `row_required_set` | 218 | row-based checker 自动推断 required trace |
| `streaming` | 29 | 既有 streaming checker contract |
| no sparse contract | 24 | 自定义 checker/noise 或暂未能安全推断 |

最高 wall rows 仍然 checker-heavy：

| Row | E2E wall | Checker | EVAS subprocess | Interpretation |
|---|---:|---:|---:|---|
| `vbr1_l1_precision_rectifier_envelope_detector_dut` | 1.292s | 1.210s | 0.063s | checker 仍主导 |
| `vbr1_l1_precision_rectifier_envelope_detector_tb` | 1.286s | 1.203s | 0.066s | checker 仍主导 |
| `vbr1_l1_precision_rectifier_envelope_detector_bugfix` | 1.278s | 1.198s | 0.059s | checker 仍主导 |
| `vbr1_l2_programmable_stimulus_sequencer_tb` | 0.901s | 0.817s | 0.063s | checker 仍主导 |
| `vbr1_l1_window_comparator_detector_bugfix` | 0.841s | 0.760s | 0.044s | checker 仍主导 |

## Functional Safety

- Default backend changed: `no`
- EVAS core semantics changed: `no`
- CSV schema changed: `conditional yes`; sparse-trace runs intentionally emit only checker-required columns
- `strobe.txt` behavior changed: `no`
- Checker decision logic changed: `no`
- Fallback path exists: `yes`; row-based auto sparse fail 会 full-trace rerun
- Opt-out exists: `yes`; `VAEVAS_DISABLE_REQUIRED_TRACE`, `VAEVAS_DISABLE_ROW_CHECKER_TRACE_CONTRACTS`, `VAEVAS_DISABLE_ROW_CHECKER_TRACE_FALLBACK`

## Validation

Commands run:

```bash
PYTHONPATH=runners:../EVAS python3 -m pytest tests/test_evas_output_cleanup.py -q
```

Results:

```text
10 passed in 0.18s
```

Full release evidence:

```text
speed-optimization/reports/full_release_evas2_auto_row_trace_20260606_r4.json
271/271 simulation ok
271/271 checker pass
0 auto sparse fallback
```

## Learning Notes

`sparse trace` 的意思是“只输出必要波形”。比如一个 checker 只需要 `time, clk, out`，那就不要把内部状态、调试节点、所有 bus bit 都写入 `tran.csv`。这和仿真数学无关，属于数据搬运优化。

为什么它会让 EVAS2 更快：Rust EVAS2 的核心仿真已经把很多 row 算得很快，剩下的时间会被 Python runner、CSV 写入、pandas/row checker 读表占掉。输出列越多，写 CSV、解析 CSV、构造 Python row/dict/object 的成本越高。减少列数后，内核没有变，但 E2E wall 会下降。

为什么不能直接删 full trace：checker 推断可能漏掉动态列，比如 `ptr_0..15`、`cell_en_0..15`、`seg0..14`、`cmp0..6`。因此这轮保留 full-trace fallback，并把 fallback 写入 notes。r2/r3 暴露过这些漏列；r4 修复后 fallback 为 0。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| checker source pattern 推断不全，漏掉必需列 | row notes 出现 `auto_sparse_trace_fallback_full_trace` 或 checker fail | 设置 `VAEVAS_DISABLE_ROW_CHECKER_TRACE_CONTRACTS=1` |
| fallback 掩盖 sparse contract bug | full report fallback count 非 0 | 审计对应 task 的 checker 源码并补推断规则 |
| sparse CSV 被误用于需要完整波形的人工调试 | 输出目录缺少非 checker 信号 | 设置 `VAEVAS_DISABLE_REQUIRED_TRACE=1` 生成完整 trace |
| 自动 prefix width 过窄 | DWA/thermometer/flash 这类 bit family checker fail | 扩展 `_CHECKER_PREFIX_TRACE_WIDTHS` 或改 checker 显式 required set |

## Next Step

下一步不应该继续堆单个 checker 特例。更合理的方向是：

- `116 - Checker Runtime Hot Rows`：把 rectifier、stimulus sequencer、window comparator 这类 checker-heavy row 迁到通用 streaming/CsvCheckerRuntime，继续减少 E2E wall。
- Rust 内核主线继续按 B01-B18 补语义覆盖；115 只解决 E2E 外层开销，不提升 Rust language coverage。
