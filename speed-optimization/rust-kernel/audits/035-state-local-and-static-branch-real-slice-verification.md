# 035 - State Local And Static Branch Real Slice Verification

Status: `done`

Date: `2026-06-03`

Code commit: `623b7f5` (`EVAS`, branch `codex/evas-spectre-rulefix-20260529`)

Related reports:

- `speed-optimization/reports/e2e_wall_profile_20260603_r35_state_local_top10_ab.json`
- `speed-optimization/reports/e2e_wall_profile_20260603_r35_state_local_top10_ab.md`
- `speed-optimization/reports/e2e_wall_profile_20260603_r36_state_local_top10_sections.json`
- `speed-optimization/reports/e2e_wall_profile_20260603_r36_state_local_top10_sections.md`
- `speed-optimization/reports/e2e_wall_profile_20260603_r37_static_branch_top10_ab.json`
- `speed-optimization/reports/e2e_wall_profile_20260603_r37_static_branch_top10_ab.md`
- `/private/tmp/evas_sar_profile.pstats`
- `/private/tmp/evas_sar_profile_after_guard.pstats`

## One-Line Summary

本轮完成 state-local generated evaluate、indexed state teardown commit、`_get_voltage()` reader guard、static branch opt-in 模式和同一 top-wall 10 EVAS-only 真实切片验证；结论是这些改动功能安全，但 state-local 不能默认开启，static branch/guard 只有小幅且混合的速度收益。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Generated model evaluate | 状态变量每次通过 `self.state[...]` 或 helper 访问 | 新增 opt-in `evas_state_local_fastpath=yes`，只把 evaluate 路径真实使用的 scalar state 降成局部变量 `_st_*` | 默认不变；opt-in 功能正确但真实切片不默认加速 |
| Indexed state storage | 关闭 indexed sidecar 时没有显式把最终 scalar slot 写回 `self.state` | `_set_indexed_state_storage(None)` 先 `_commit_indexed_state_storage()` | 修复 opt-in indexed state teardown 的可观测状态一致性 |
| Indexed state counters | 只统计 write | 增加 scalar/array read counters | 仅增加 profile 可见性 |
| Voltage read helper | 没有 indexed reader 时仍会调用 `_read_indexed_voltage()` 空函数 | 先判断 `_indexed_voltage_reader is not None`，没有 reader 就直接走原 dict/event path | 默认行为不变，删掉一批空 Python 调用 |
| Speed runner | EVAS mode 没有完整写入报告；E2E timing split 不够清楚 | same-server artifact 记录 `mode_label`、`simulator_options`、`default_off_fast_path`、checker policy 和 timing split | 报告更可审计；不改变 checker 判定 |
| Benchmark modes | 没有 state-local/static-branch 真实切片 A/B 入口 | 新增 `profile_fast_state_local` 和 `profile_fast_static_branch` | 方便后续复跑，不把实验模式伪装成默认模式 |

## Principle

这轮包含两类优化思想。

第一类是 **降低每步成本**：

```text
Python dict/string/helper call
  -> precomputed state slot / node slot
  -> generated local variable or direct helper path
```

它的理论依据是：EVAS 主循环会执行很多步，每步又会执行多个 model 的 generated `evaluate()`。如果每个状态读写都要经过 Python dict、字符串 key、Python 函数调用，那么单次成本很小，但乘上 `accepted_steps * model_count * state_access_count` 后会变成 wall time。

第二类是 **减少无效函数调用**：

```text
if indexed reader is absent:
    do not call _read_indexed_voltage()
```

这不改变数学语义，只是避免在没有 indexed reader 的默认路径上调用一个必然返回 `None` 的函数。

这轮精确验证的重点是：理论上更快不等于真实 benchmark 更快。state-local local variable 在 Python 里也会引入 entry/exit flush、integer coercion、统计 counter 和更多 generated code；如果模型每步 state 访问密度不高，收益会被这些额外成本抵消。

## Before / After Evidence

### State-local top-wall 10 A/B, no section profiling

Same command shape, only EVAS mode different:

| Metric | Baseline `profile_fast_skip_source_error_control` | Candidate `profile_fast_state_local` | Interpretation |
|---|---:|---:|---|
| Runs | `10` | `10` | same slice |
| Behavior PASS | `10` | `10` | checker-level function unchanged |
| E2E wall total | `14.946214165 s` | `14.825084833 s` | candidate `1.008x` by E2E, very small |
| EVAS subprocess total | `11.192565751 s` | `10.996636749 s` | candidate `1.018x`, still very small |
| Checker total | `3.589881084 s` | `3.711474001 s` | checker noise/overhead moved opposite direction |
| accepted steps | `128402` | `128402` | no step-count change |
| `tran_elapsed_s` | `8.150600 s` | `8.079400 s` | small EVAS internal improvement in this no-section run |
| `csv_write_s` | `0.328385 s` | `0.344700 s` | CSV noise/opposite direction |

这个结果不能支持默认开启，因为收益只有约 1% 且和 checker/CSV 噪声同量级。

### State-local top-wall 10 with section profiling

打开 `EVAS_PROFILE_SECTIONS=1 EVAS_PROFILE_MODEL_EVAL=1 EVAS_PROFILE_MODEL_IO=1` 后，真实内核分段显示 state-local 反而变慢：

| Section | Baseline | State-local | Interpretation |
|---|---:|---:|---|
| E2E wall total | `18.849920378 s` | `19.032253332 s` | candidate slower |
| EVAS subprocess total | `14.706991751 s` | `15.200392498 s` | candidate slower |
| Behavior PASS | `10/10` | `10/10` | function unchanged |
| accepted steps | `128402` | `128402` | no step-count change |
| `tran_elapsed_s` | `11.770200 s` | `12.209200 s` | simulation section slower |
| `model_evaluate_s` | `6.060673 s` | `6.412562 s` | main target section slower by `0.351889 s` |
| `model_breakpoint_scan_s` | `0.979599 s` | `0.980361 s` | unchanged |
| `model_post_update_s` | `0.674019 s` | `0.715355 s` | slightly slower |
| `model_prepare_step_s` | `0.480285 s` | `0.483541 s` | unchanged |
| `model_output_set_s` | `0.173128 s` | `0.171416 s` | unchanged |
| `err_ratio_node_scan_s` | `0.395935 s` | `0.405238 s` | unchanged |
| `record_point_s` | `0.215023 s` | `0.212459 s` | unchanged |
| `csv_write_s` | `0.336717 s` | `0.403182 s` | noisy/slower |

结论：state-local generated evaluate 是 Rust/state ABI 前置能力和实验入口，不是当前 Python 默认加速项。

### Static-branch top-wall 10 A/B

| Metric | Baseline `profile_fast_skip_source_error_control` | Candidate `profile_fast_static_branch` | Interpretation |
|---|---:|---:|---|
| Runs | `10` | `10` | same slice |
| Behavior PASS | `10` | `10` | checker-level function unchanged |
| E2E wall total | `14.252865709 s` | `14.126473292 s` | candidate `1.009x` |
| EVAS subprocess total | `10.460526375 s` | `10.347043000 s` | candidate `1.011x` |
| Checker total | `3.628956917 s` | `3.660902790 s` | checker noise/opposite direction |
| accepted steps | `128402` | `128402` | no step-count change |
| `tran_elapsed_s` | `7.758700 s` | `7.829300 s` | EVAS internal timing slightly slower in this run |
| `csv_write_s` | `0.364414 s` | `0.327714 s` | CSV faster, contributing to E2E gain |

结论：static branch helper 是低风险 opt-in，局部 microbenchmark 曾有收益，但在真实 top-wall 10 上整体只有约 1%，且 per-row mixed，不能作为大瓶颈已解决的证据。

### `_get_voltage()` reader guard cProfile

Profile target: SAR row, same staged gold directory. Before/after differ by `_get_voltage()` no-reader guard。

| Function | Before calls | Before total time | After calls | After total time | Interpretation |
|---|---:|---:|---:|---:|---|
| `_read_indexed_voltage` | `377129` | `0.043543 s` | `0` | `0.000000 s` | 空 indexed read 调用被消除 |
| `_get_voltage` | `388120` | `0.354568 s` | `388120` | `0.287088 s` | helper cumulative time下降 |
| total Python calls | `9550553` | `3.492007 s` | `9173435` | `3.600415 s` | 总 wall 受噪声和其他热路径影响，不能宣称整体加速 |
| `_check_cross` | `309054` | `0.449828 s` | `309054` | `0.511047 s` | 仍是热路径 |
| `_transition` | `261272` | `0.388444 s` | `261272` | `0.421921 s` | 仍是热路径 |
| model generated `evaluate` | `32532` | about `1.663 s` | `32532` | about `1.773 s` | 仍是最大热路径之一 |
| `next_breakpoint` family | multiple | about `0.491 s` | multiple | about `0.561 s` | timer/breakpoint 仍需后续优化 |

这个 micro-fix 是正确的低风险改动，但它只删掉约 `0.044 s` 的空函数调用，不足以改变 release-wide 速度判断。

## Functional Safety

- Default backend changed: `yes, only for _get_voltage() no-reader guard; returned value and event interpolation branch unchanged`
- State-local default changed: `no, requires evas_state_local_fastpath=yes or EVAS_STATE_LOCAL_FASTPATH=1`
- Static-branch default changed: `no, requires evas_static_branch_fastpath=yes or EVAS_STATIC_BRANCH_FASTPATH=1`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- Fallback path exists: `yes`

State-local safety guard:

```text
only scalar state touched by generated evaluate-path code is localized
exclude generated for-loop state targets
exclude initial_step/final_step-only cold state
commit indexed scalar state back to self.state before sidecar teardown
```

## Validation

Commands run:

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
python3 -m pytest -q

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/rust_core
cargo test --release

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
python3 -m pytest -q \
  tests/test_engine.py::TestSimulator::test_indexed_state_storage_preserves_stateful_waveform_and_counts_writes \
  tests/test_engine.py::TestSimulator::test_indexed_state_fastpath_reads_state_slots_without_changing_waveform \
  tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_state_storage_when_opted_in

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
python3 -m pytest -q \
  tests/test_engine.py::TestSimulator::test_indexed_arrays_build_model_io_plan_without_changing_mapped_output \
  tests/test_engine.py::TestSimulator::test_static_branch_fastpath_matches_default_and_counts_hits \
  tests/test_engine.py::TestCompiledModelHelpers::test_get_voltage_non_event_prefers_indexed_reader \
  tests/test_engine.py::TestCompiledModelHelpers::test_get_voltage_mapped_non_event_prefers_indexed_reader \
  tests/test_engine.py::TestCompiledModelHelpers::test_static_branch_voltage_falls_back_to_event_interpolation \
  tests/test_engine.py::TestCompiledModelHelpers::test_node_resolution_cache_resolves_mapped_reads_and_writes

cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile \
  runners/run_vabench_release_evas_speed_experiment.py \
  runners/run_vabench_release_same_server_speed.py

cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=runners \
  python3 -m pytest -q tests/test_evas_output_cleanup.py

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
git diff --check

cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval
git diff --check -- \
  runners/run_vabench_release_evas_speed_experiment.py \
  runners/run_vabench_release_same_server_speed.py
```

Results:

```text
EVAS full pytest: 469 passed in 28.12s
Rust core cargo test --release: 3 passed
Indexed state targeted pytest: 3 passed in 0.76s
Voltage/static targeted pytest: 6 passed in 0.52s
Runner py_compile: passed
Checker policy pytest: 3 passed in 0.11s
EVAS git diff --check: clean
benchmark runner git diff --check: clean
```

Known validation boundary:

```text
tests/test_vabench_release_speed_baseline_artifacts.py still fails against the historical
speed_debug_artifact.json because that artifact status is pending_measurement while the
test expects measured_subset. This is an existing artifact freshness issue, not caused by
the new runner modes or EVAS kernel patch.
```

## Learning Notes

### 为什么 state-local 理论上会快，实测却没有赢？

可以把 Python 版 generated `evaluate()` 想成一个很热的循环：

```python
self.state["x"] = self.state["x"] + 1
V(out) <+ self.state["x"]
```

`self.state["x"]` 是 Python dict 查找，包含字符串 hash、查表、对象读取。state-local 想把它变成：

```python
_st_x = self.state["x"]
_st_x = _st_x + 1
...
self.state["x"] = _st_x
```

中间计算少了 dict lookup，但入口和出口多了 load/flush。只有当某个状态变量在一步里被反复访问很多次时，中间省下来的成本才会大于入口/出口成本。当前 top-wall 10 不是这种形态，所以 section profile 显示 `model_evaluate_s` 反而变慢。

### 这对 Rust 化有什么意义？

Python state-local 不是终点。它的意义是把“哪些变量可以用 slot 编号表示”这个边界做清楚：

```text
state name: "x"
  -> state id: 0
  -> Rust Vec<f64>[0]
```

Rust 里没有 Python dict/string/object 的大部分解释器开销。只要能把 generated model 的热循环真的搬到 Rust `Vec<f64>` / `&mut [f64]` 上，state id 才会变成主要收益来源。Python 里只做一半，经常会因为桥接/flush/counter 成本吃掉收益。

### 为什么 `_get_voltage()` guard 可以保留？

它没有改变返回路径，只是把：

```python
indexed_value = self._read_indexed_voltage(...)
if indexed_value is not None:
    return indexed_value
```

改成：

```python
if self._indexed_voltage_reader is not None:
    indexed_value = self._read_indexed_voltage(...)
    ...
```

当 indexed reader 不存在时，旧代码调用一个必然返回 `None` 的函数；新代码直接跳过。这个是纯控制流剪枝，数学上不改变电压读取。

### 当前最大瓶颈在哪里？

根据 r36 section profile 和 SAR cProfile，下一批真正值得做的点不是继续小修 state dict：

```text
generated model evaluate
cross detector / event predicate
transition()
next_breakpoint / timer scan
model post-update and lifecycle bookkeeping
```

这些都位于 EVAS 内核每步路径，继续用 Python 小技巧只能拿到个位数百分点；要拿到明显速度收益，需要把 event/evaluate 批处理、timer/breakpoint 队列或 Rust/C 执行内核做实。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 误把 state-local 当默认加速 | r36 `model_evaluate_s` 变慢 `6.060673 -> 6.412562 s` | 不设置 `evas_state_local_fastpath=yes`; revert EVAS commit `623b7f5` 中 state-local codegen 部分 |
| indexed state teardown 状态不一致 | targeted test 比较 fallback/indexed final `model.state` | 保留 `_commit_indexed_state_storage()`；如出问题回退 indexed state storage opt-in |
| static branch 在真实 slice 中收益不稳定 | r37 only `1.009x` E2E and per-row mixed | 不默认设置 `evas_static_branch_fastpath=yes` |
| cProfile micro-fix 被过度解读 | total profile time `3.492 -> 3.600 s` 受噪声影响 | 只 claim eliminated empty calls，不 claim release-wide speedup |
| EVAS-only top-wall 没有 Spectre equivalence gate | report `equivalence_gate_summary` blocked `10/10` | paper-facing speed claim 仍必须 full same-server EVAS/Spectre/AX rerun |

## Next Step

下一篇审计文档建议：

- `036 - Event Primitive And Breakpoint Queue Plan`

目标不是继续做 state-local 小修，而是针对真实热路径设计一个可验证的 event/timer 优化方案：

1. 先把 top-wall slow rows 的 `cross/transition/next_breakpoint` 调用密度按 model 聚合。
2. 对 timer-only 和 cross-heavy 模型分开设计优化，避免一个改动同时碰 event ordering 和 transition shape。
3. 每个优化必须用 Spectre-aligned parity、accepted step count、event fire count 和 waveform/checker PASS 一起验证。
