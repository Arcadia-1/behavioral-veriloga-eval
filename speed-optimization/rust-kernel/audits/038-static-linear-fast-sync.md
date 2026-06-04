# 038 - Static Linear Fast Sync

Status: `done`

Date: `2026-06-03`

Code commit: `pending`

Related reports:

- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`
- `behavioral-veriloga-eval/speed-optimization/reports/e2e_wall_profile_20260603_r45_rust_fast_sync_baseline.json`
- `behavioral-veriloga-eval/speed-optimization/reports/e2e_wall_profile_20260603_r48_rust_fast_sync_final.json`

## One-Line Summary

给 Rust static linear segment 增加 opt-in fast sync：全模型 Rust 覆盖时不再每步把 Rust 输出全量同步回 Python `node_voltages` dict，也不再做每步 indexed validation。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| engine option | `rust_static_eval=True` 每步仍同步 Rust 输出到 Python dict | 新增 `rust_static_fast_sync=True`，全模型覆盖时跳过 per-step dict sync/validation，final 前补齐 dict/output_nodes | 默认 backend 不变 |
| runner/env | 只有 `EVAS_RUST_STATIC_EVAL` | 新增 `EVAS_RUST_STATIC_FAST_SYNC=1` / `evas_rust_static_fast_sync=true`，自动打开 Rust static eval | opt-in only |
| safety gate | Rust requested 但无 segment 时仍可能付 indexed array 开销 | 无 Rust segment 且 indexed arrays 不是用户显式请求时，自动撤销 Rust 强制 indexed array/state storage | 非覆盖真实任务不再被 Rust 开关拖慢 |
| counters | 只能看到 Rust eval/sync 总数 | 新增 `rust_static_fast_sync_*` 和 `rust_static_eval_no_segment_fallbacks` | 便于判断 fast mode 是否真的生效 |

## Principle

这次优化减少的是 **每步成本**，不是减少仿真步数。

037 之后，Rust 已经能把一个 static linear segment 的数学计算降到 native loop：

```text
node_values[out_id] = bias + sum(gain_i * node_values[in_id])
```

但 Rust normal path 仍有两层 Python 开销：

1. 每步遍历所有 Rust 输出，把 `node_values[out_id]` 写回 `self.node_voltages["out"]`。
2. 每步做 indexed array 到 Python dict 的 validation。

fast sync 的安全前提是：

```text
所有顶层 model 都由 Rust static segment 覆盖
```

在这个前提下，同一步里不会有 Python model 读取 stale `node_voltages`。记录、误差扫描、source update 都可以继续从 indexed array 读当前值。最后一次在 `final_step` 之前把 Rust 输出同步回 Python dict/output_nodes，保证最终状态和外部可见结果一致。

如果没有 Rust segment，fast mode 自动 fallback 到普通 Python runtime，避免真实任务仅因为设置了 `EVAS_RUST_STATIC_FAST_SYNC=1` 就进入 indexed array 慢路径。

## Before / After Evidence

### Microbench: Rust-Covered Static Linear Chain

Local-only targeted microbench, not paper-facing. All runs used the final code after no-segment fallback. Waveform final value matched exactly against Python in both Rust modes.

| Case | Python wall | Rust normal wall | Rust fast-sync wall | Rust normal/Python | Rust fast/Python | Rust fast/Rust normal |
|---|---:|---:|---:|---:|---:|---:|
| 100-model affine chain | 10.893544 s | 11.011230 s | 8.301389 s | 0.989x | 1.312x | 1.326x |
| 500-model affine chain | 57.088959 s | 55.681208 s | 38.618222 s | 1.025x | 1.478x | 1.442x |

Key 500-model counters:

| Counter / section | Rust normal | Rust fast-sync | Interpretation |
|---|---:|---:|---|
| `rust_static_eval_models` | 500 | 500 | same covered segment |
| `indexed_array_syncs` | 25226 | 0 | per-step dict validation removed |
| `rust_static_eval_node_voltage_syncs` | 12613000 | 500 | only final dict sync remains |
| `rust_static_fast_sync_node_voltage_sync_skips` | 0 | 12613000 | skipped per-step dict writes |
| `indexed_array_sync_s` | 14.312910 s | 0.071290 s | validation/sync no longer dominates |
| `rust_static_eval_s` | 5.105970 s | 0.241567 s | includes avoided Python sync loop |
| `err_ratio_node_scan_s` | 17.515315 s | 16.143367 s | new largest remaining cost |
| `indexed_array_prev_snapshot_s` | 0.188149 s | 4.892498 s | remaining indexed snapshot cost |

Interpretation:

- The E2E Rust path changed from “barely faster” to visibly faster on Rust-covered synthetic static chains.
- The next bottleneck is no longer Rust evaluate or dict output sync; it is error-control node scan and indexed snapshot.
- This does not prove release-wide speedup, because real tasks must actually compile into Rust static linear segments.

### Top Real Benchmark: Current Top-Wall 10

Same top-wall 10 row-set, EVAS-only, `profile_fast_skip_source_error_control`, section/profile counters enabled. These are diagnostic reports, not paper-facing speed claims.

| Report | Rust fast sync | Rows PASS | Total E2E wall | Total EVAS subprocess wall | Interpretation |
|---|---:|---:|---:|---:|---|
| r45 baseline | off | 10/10 | 17.613080 s | 13.847292 s | current top10 baseline |
| r48 final | on | 10/10 | 18.117548 s | 14.270016 s | no stable real-slice speedup |

Representative direct full-log check:

```text
/private/tmp/evas-rust-fast-sync-gain-estimator-r48.log
rust_static_eval_candidate_models = 0
rust_static_eval_segments = 0
rust_static_eval_no_segment_fallbacks = 1
indexed_array_syncs = 0
indexed_array_snapshots = 0
indexed_state_storage_enabled = 0
```

Conclusion for top real benchmark:

- The current top-wall 10 rows do not enter the new Rust static linear segment (`candidate_models=0` on the inspected representative row).
- Therefore fast sync cannot make this top10 slice meaningfully faster.
- The no-segment fallback prevents the serious regression seen before the runner fix, but it does not create a speedup where Rust coverage is absent.

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

Safety boundaries:

- fast sync enables only when every top-level model is in Rust static segment.
- mixed Rust/Python model lists keep normal indexed validation.
- no Rust segment falls back to ordinary Python runtime if indexed arrays were only forced by Rust.
- final sync runs before `final_step`, preserving final Python-visible node/output state.

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestSimulator::test_rust_static_fast_sync_skips_per_step_dict_validation tests/test_engine.py::TestSimulator::test_rust_static_fast_sync_no_segment_falls_back_to_python_runtime tests/test_engine.py::TestSimulator::test_rust_static_eval_keeps_full_indexed_validation_for_mixed_models tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_fast_sync_when_opted_in -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_fast_sync_when_opted_in -q
cargo test
python3 -m pytest -q
```

Results:

```text
targeted fast-sync/fallback: 4 passed
netlist Rust/static logging: 2 passed
Rust core: 5 passed
Full EVAS pytest: 481 passed
```

Diagnostic runs:

```bash
EVAS_PROFILE_SECTIONS=1 EVAS_PROFILE_MODEL_EVAL=1 EVAS_PROFILE_MODEL_IO=1 \
python3 runners/run_vabench_release_same_server_speed.py \
  --speed-artifact speed-optimization/reports/e2e_wall_unified_rows_from_r14_exactrows_20260602.json \
  --suite top-wall --limit 10 \
  --evas-mode profile_fast_skip_source_error_control \
  --skip-spectre \
  --output-root results/e2e-wall-profile-20260603-r45-rust-fast-sync-baseline \
  --report-json speed-optimization/reports/e2e_wall_profile_20260603_r45_rust_fast_sync_baseline.json \
  --report-md speed-optimization/reports/e2e_wall_profile_20260603_r45_rust_fast_sync_baseline.md

EVAS_PROFILE_SECTIONS=1 EVAS_PROFILE_MODEL_EVAL=1 EVAS_PROFILE_MODEL_IO=1 \
EVAS_RUST_STATIC_FAST_SYNC=1 \
python3 runners/run_vabench_release_same_server_speed.py \
  --speed-artifact speed-optimization/reports/e2e_wall_unified_rows_from_r14_exactrows_20260602.json \
  --suite top-wall --limit 10 \
  --evas-mode profile_fast_skip_source_error_control \
  --skip-spectre \
  --output-root results/e2e-wall-profile-20260603-r48-rust-fast-sync-final \
  --report-json speed-optimization/reports/e2e_wall_profile_20260603_r48_rust_fast_sync_final.json \
  --report-md speed-optimization/reports/e2e_wall_profile_20260603_r48_rust_fast_sync_final.md
```

## Learning Notes

这次可以把 EVAS 内核想成三层：

```text
数学计算层：target = bias + gain * source
数据同步层：Rust array <-> Python node_voltages dict
仿真控制层：步长、误差扫描、记录、事件/timer
```

Rust 让第一层很快，但如果第二层每步还要把几百万个输出写回 Python dict，E2E wall 仍然不会明显下降。fast sync 的作用是把第二层的大部分每步工作移走。

为什么必须要求全模型覆盖？因为如果同一步后面还有 Python model，它会通过 `node_voltages["node"]` 读输入。如果 Rust 已更新 array 但没有更新 dict，Python model 就可能读到旧值。全模型 Rust 覆盖时，没有这种读者，所以可以安全延迟 dict sync。

为什么 top real benchmark 没收益？因为当前 top-wall 10 的模型大多有 timer/event/state/array/dynamic 行为，不属于 037/038 这批 static linear IR。它们还没有进入 Rust 的数学计算层，因此 fast sync 没有东西可加速。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| fast sync 在混合模型中误启用 | Python model waveform mismatch or stale read | revert `rust_static_fast_sync_enabled` full-coverage condition |
| no-segment fallback 撤销了用户显式 indexed array 请求 | `EVAS_INDEXED_ARRAYS=1` run lacks indexed counters | fallback guard keeps `indexed_arrays_requested`; check runner/engine option flow |
| final state stale | `final_step` or `output_nodes` tests fail | final sync in `engine.py` before `final_step` |
| top real report被误读成 Rust 失败 | r48 total not faster | cite `candidate_models=0/segments=0`: coverage absence, not Rust compute regression |

## Next Step

下一篇审计建议：

- `039 - Rust Coverage Expansion For Real Models`

目标：针对 top-wall 10 中的 real models，统计为什么 `candidate_models=0`，优先把简单 state assignment、timer-free static measurement helper、non-event linear expressions 放进 evaluate IR，而不是继续优化已经很快的 static-chain sync。
