# 036 - Transition Unchanged Target Fastpath

Status: `done`

Date: `2026-06-03`

Code commit: `c909463` (`EVAS`, branch `codex/evas-spectre-rulefix-20260529`)

Related reports:

- `speed-optimization/reports/e2e_wall_profile_20260603_r44_transition_fastpath_top10_ab.json`
- `speed-optimization/reports/e2e_wall_profile_20260603_r44_transition_fastpath_top10_ab.md`
- `/private/tmp/evas_sar_profile_transition_final3_on.pstats`
- `/private/tmp/evas_sar_profile_transition_final3_off.pstats`
- `/private/tmp/evas_sar_transition_final3_on.log`
- `/private/tmp/evas_sar_transition_final3_off.log`

## One-Line Summary

本轮把 `transition()` 目标值和参数完全不变时的重复 `set_target()`/二次 `evaluate()` 做成 opt-in fastpath，并修复首次创建 `TransitionState` 时没有记录初始 target/transition 参数的问题；精确验证显示它能显著减少 `_transition` 子路径调用，但 top-wall 10 的 E2E wall 没有稳定总收益，因此默认关闭。

## What Changed

| Layer | Before | After | Default behavior |
|---|---|---|---|
| `TransitionState` initialization | 首次 `_transition()` 只保存 `current_val`，没有完整保存 `target_val/start_val/start_time/delay/rise/fall` | 首次创建时完整记录 target 和 transition 参数 | 更完整，语义更保守 |
| `_transition()` no-op path | 即使 target 没变，也会调用 `set_target()`，再调用一次 `TransitionState.evaluate()` | opt-in 时，如果 target、delay、rise、fall 精确相等，直接返回已 advance 的 current value | 默认关闭 |
| Runtime switch | 无单独开关 | `evas_transition_unchanged_fastpath=true` 或 `EVAS_TRANSITION_UNCHANGED_FASTPATH=1` | 默认关闭 |
| Perf counters | 无该路径命中计数 | `transition_unchanged_target_fastpath_total` 和 per-model counter | 只增加观测能力 |
| Benchmark mode | 无 A/B 入口 | `profile_fast_transition_unchanged_on` | 只用于实验 |

## Principle

`transition(x, delay, rise, fall)` 是一个有内部状态的 smoothing operator。每次模型 evaluate 时，EVAS 都会先把 transition state advance 到当前时间：

```text
current = ts.evaluate(time)
```

如果新的 target 和 transition 参数完全不变，后续这两步是无意义工作：

```text
ts.set_target(time, target, delay, rise, fall)
return ts.evaluate(time)
```

因为 target 没变，第一次 `evaluate(time)` 已经给出当前时刻的 transition 输出；再次设置同一个目标、再 evaluate 同一个时间点，不应产生新的物理信息。fastpath 的数学含义就是跳过这个 no-op update。

这次没有使用容差扩大命中，而是使用精确相等：

```text
target == ts.target_val
delay == ts.delay
rise == ts.rise_time
fall == ts.fall_time
```

原因是 Python hot loop 里 `abs(...) <= tol` 本身很贵。fastpath 是保守 shortcut，不是数值判定标准；如果不精确相等，就回到原路径。

## Before / After Evidence

### SAR cProfile, same staged netlist

Same code, same SAR staged netlist, only fastpath switch changed.

| Metric | Opt-in on | Default/off | Interpretation |
|---|---:|---:|---|
| `transition_unchanged_target_fastpath_total` | `254617` | `0` | no-op target updates were detected |
| `TransitionState.set_target` calls | `6623` | `261240` | `254617` calls removed |
| `TransitionState.evaluate` calls | `267863` | `522480` | second same-time evaluate removed |
| `_transition` cumulative time | `0.326994 s` | `0.516007 s` | target subpath improves |
| cProfile total CPU | `4.121846 s` | `4.172427 s` | only `1.012x`, within local noise |
| EVAS log tran elapsed | `3.7273 s` | `3.7413 s` | only `1.004x`, within local noise |

结论：这个 fastpath 确实减少了 transition 子路径工作，但 SAR 总体仍被 generated model evaluate、cross/breakpoint scan、CSV/checker 等其他路径稀释。

### Final top-wall 10 A/B

Report: `e2e_wall_profile_20260603_r44_transition_fastpath_top10_ab`.

| Metric | Baseline `profile_fast_skip_source_error_control` | Candidate `profile_fast_transition_unchanged_on` | Interpretation |
|---|---:|---:|---|
| Runs | `10` | `10` | same slice |
| Behavior PASS | `10/10` | `10/10` | checker-level function unchanged |
| E2E wall total | `17.586196457 s` | `17.796447876 s` | candidate `0.988x`, not a win |
| EVAS subprocess total | `13.321234334 s` | `13.469653500 s` | candidate `0.989x`, not a win |
| Checker total | `4.058283915 s` | `4.099859044 s` | same order; not the cause |
| Median per-row E2E speedup | - | `1.020x` | many small mixed row effects |
| Candidate per-row wins | - | `7/10` E2E, `6/10` subprocess | not enough to offset slow rows |

Largest mixed rows:

| Row | E2E baseline/candidate speedup | Note |
|---|---:|---|
| `vbr1_l1_gain_estimator/tb` | `1.705x` | opt-in faster |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e` | `1.450x` | opt-in faster |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/tb` | `1.472x` | opt-in faster |
| `vbr1_l2_gain_extraction_convergence_measurement_flow/tb` | `0.534x` | opt-in slower |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/e2e` | `0.629x` | opt-in slower |

结论：当前 Python fastpath 不能默认开启。它是一个可验证、可回退、可为 Rust/native transition primitive 复用的 IR/semantic entry，但还不是 paper-facing speedup。

## Functional Safety

- Default backend changed: `no, transition fastpath defaults off`
- CSV schema changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- Transition interruption target-change path changed: `no`
- Initial transition state metadata changed: `yes, now records first target and transition parameters`
- Fallback path exists: `yes, disable/omit evas_transition_unchanged_fastpath`

Opt-in trigger:

```text
evas_transition_unchanged_fastpath=true
EVAS_TRANSITION_UNCHANGED_FASTPATH=1
```

Fallback:

```text
omit the option, or set EVAS_TRANSITION_UNCHANGED_FASTPATH=0
```

## Validation

Commands run:

```bash
cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile \
  evas/netlist/runner.py evas/simulator/backend.py evas/simulator/engine.py tests/test_engine.py

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
python3 -m pytest -q \
  tests/test_engine.py::TestCompiledModelHelpers::test_transition_unchanged_target_fastpath_preserves_interruption \
  tests/test_engine.py::TestCompiledModelHelpers::test_transition_unchanged_target_fastpath_is_default_disabled \
  tests/test_engine.py::TestCompiledModelHelpers::test_transition_initial_state_records_target_and_parameters_for_fastpath \
  tests/test_engine.py::TestCompiledModelHelpers::test_transition_unchanged_target_fastpath_checks_transition_parameters \
  tests/test_engine.py::TestTransitionState

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
python3 -m pytest -q

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/rust_core
cargo test --release

cd /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS
git diff --check

cd /Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile \
  runners/run_vabench_release_evas_speed_experiment.py \
  runners/run_vabench_release_same_server_speed.py
```

Results:

```text
Transition targeted pytest: 21 passed
EVAS full pytest: 473 passed in 34.63s
Rust core cargo test --release: 3 passed
EVAS py_compile: passed
Benchmark runner py_compile: passed
EVAS git diff --check: clean
```

## Learning Notes

### 为什么“少了很多调用”却没有稳定整体加速？

因为 EVAS 的 wall time 不是只由 `_transition()` 决定。一个 row 的 E2E wall 大致包括：

```text
fixture/staging + EVAS subprocess + CSV write + checker + cleanup
```

EVAS subprocess 内部又包括：

```text
generated model evaluate
cross/above checks
timer/breakpoint scan
source update
record/csv
transition/slew helpers
```

这轮只减少了 transition helper 的一小段。对 transition-dense 且其他路径不重的 row，它可能变快；对 CPPLL、measurement-heavy 或其他 evaluate/cross 更重的 row，它会被其他成本淹没，甚至因为 Python 分支判断和局部噪声表现为更慢。

### 为什么默认关闭？

我们的默认规则是：只有同片 benchmark wall 和功能验证都支持收益，才默认开启。当前证据是：

```text
功能：PASS，安全
局部：_transition 子路径更快
整体：top-wall 10 E2E 不稳定，没有总收益
```

所以正确结论是保留 opt-in，不把它写成默认优化。

## Next Step

下一轮真正更有价值的方向不是继续微调 Python `transition()` 分支，而是：

1. 把 transition/cross/timer primitive 做成 indexed/native event primitive，减少 Python per-step dispatch。
2. 对 CPPLL/ADPLL 的 timer/breakpoint scan 做 event queue，减少每步扫描。
3. 对 measurement-heavy rows 继续 profile generated evaluate 和 checker/CSV 分界，不把局部 helper 优化误当大瓶颈修复。
