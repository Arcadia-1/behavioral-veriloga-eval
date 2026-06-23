# 041 - Transition Real Top-Wall Profile And Fastpath

Status: `diagnostic`

Date: `2026-06-03`

Code commit: `pending`

Related reports:

- `behavioral-veriloga-eval/speed-optimization/reports/e2e_wall_profile_20260603_r52_transition_real_topwall.json`
- `behavioral-veriloga-eval/speed-optimization/reports/e2e_wall_profile_20260603_r53_transition_real_topwall_optimized.json`
- `behavioral-veriloga-eval/speed-optimization/reports/e2e_wall_profile_20260603_r54_transition_unchanged_real_topwall.json`
- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_engine.py`

## One-Line Summary

真实 top-wall 模型里 `transition()` 是 CPPLL、PFD、PRBS、gain estimator 等任务的公共热路径；041 增加 transition 输出融合、active transition breakpoint set 和 counters，并用 top-wall 10 证明覆盖有效但暂不能声明稳定 wall-time 加速。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Transition breakpoint scan | 每次 `next_breakpoint()` 扫描 `self.transitions.values()`，即使大多数 transition 已经 inactive | 维护 `_active_transition_keys`，只扫描 active transition；inactive key 计入 skip counter | 波形不变 |
| Transition output contribution | `V(out) <+ offset + scale * transition(...)` 走普通 `_transition()` + `_set_output()` path | 单端和 differential `V(out, vss) <+ ... transition(...)` 可生成 `_transition_output()` | 波形不变 |
| Active-set update | r52 中每次 `_transition()` 都更新 Python set | r53 起只在 `active` 状态发生变化时更新 set | 波形不变 |
| Profiling counters | 只能看到 coarse `transition_unchanged_target_fastpath` | 新增 calls、output-fastpath、set-target、evaluate、breakpoint active/inactive counters | 只影响 profile 输出 |

## Principle

这轮属于 **降低每步成本**，不是减少仿真步数。

一个 `transition()` 可以拆成三件事：

1. 读当前 target，判断 target 是否变化。
2. 更新 `TransitionState`，包括 start time、target、rise/fall、active flag。
3. 把 transition value 写到输出节点。

以前 EVAS 在真实模型里每步都容易重复做这些 Python 动作：

- transition inactive 后仍被 breakpoint scan 看到。
- `V(out, vss) <+ ... transition(...)` 这种 differential 输出不能进入 fused helper。
- target 没变时仍调用 `set_target()`，这对 PRBS/CPPLL 这类每步 evaluate 很多但实际 edge 不多的模型很浪费。

041 先把这些路径显式量化和局部降低成本。它还不是 Rust event/transition queue；`TransitionState` 本身仍在 Python 里执行。

## Before / After Evidence

EVAS-only diagnostic, top-wall 10, no Spectre gate. These reports are not paper-facing speed claims.

| Report | Mode | Rows PASS | Total E2E wall | EVAS subprocess wall | Checker wall | Interpretation |
|---|---|---:|---:|---:|---:|---|
| r51 | `profile_fast_skip_source_error_control` | 10/10 | 18.337417 s | 14.704750 s | 3.482088 s | pre-041 mixed-gate baseline |
| r52 | same | 10/10 | 68.233102 s | 55.311884 s | 11.893028 s | first transition instrumentation; also hit noisy/slow host conditions |
| r53 | same | 10/10 | 60.145440 s | 49.696194 s | 9.493694 s | differential output fastpath + lighter active-set update |
| r54 | `profile_fast_transition_unchanged_on` | 10/10 | 53.839377 s | 43.915668 s | 9.269731 s | existing unchanged-target opt-in; adjacent to r53 is 0.895x total wall |

Important interpretation:

- r53/r54 are much slower than r51 across almost every section, including CSV/checker/record/source update. This indicates host noise and profiling overhead; do not use r53/r54 as final speed numbers.
- r53 versus r52 still shows the code-level correction helped under the same slow conditions: total E2E `68.233102 -> 60.145440 s`.
- r54 versus r53 shows `transition_unchanged_fastpath` is useful for some rows, but mixed: total E2E `60.145440 -> 53.839377 s`, about 10.5% faster in this adjacent diagnostic.

### Real Transition Coverage

| Row | r53 transition evidence | Meaning |
|---|---:|---|
| `vbr1_l1_gain_estimator_tb` | `transition_output_fastpath_calls = 2466`; `transition_breakpoint_inactive_skips = 2418` | differential `V(out,VSS)` output now reaches fused helper |
| `vbr1_l1_gain_estimator_e2e` | `transition_output_fastpath_calls = 2466`; `transition_breakpoint_inactive_skips = 2418` | same coverage on e2e form |
| `vbm1_pfd_reset_race_bugfix` | `transition_output_fastpath_calls = 770`; `transition_breakpoint_inactive_skips = 732` | PFD UP/DN transition outputs covered |
| `prbs7` | `transition_output_fastpath_calls = 29400`; `transition_breakpoint_scans = 3072` | many transition output writes covered; inactive scans reduced |
| CPPLL rows | r54 `transition_unchanged_target_fastpath = 126381` | target-stability optimization removes most no-op `set_target()` calls |

### Unchanged-Target Counter Evidence

| Row | r53 `set_target` | r54 `set_target` | r54 unchanged fastpath | Wall effect |
|---|---:|---:|---:|---:|
| `vbr1_l1_gain_estimator_tb` | 2462 | 20 | 2442 | `1.8803 -> 1.5497 s` |
| `vbr1_l1_gain_estimator_e2e` | 2462 | 20 | 2442 | `0.7299 -> 1.3040 s` noisy/slower |
| `vbm1_pfd_reset_race_bugfix` | 766 | 26 | 740 | `0.9350 -> 0.9585 s` roughly flat |
| `cppll_freq_step_reacquire_smoke` | 136617 | 10236 | 126381 | `8.9322 -> 9.0208 s` roughly flat |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb` | tail truncated | tail truncated | 126381 | `11.2502 -> 8.4888 s` faster |
| `prbs7` | 29384 | 464 | 28920 | `3.9959 -> 1.5244 s` faster |

Conclusion:

- `transition_unchanged_fastpath` has strong counter-level evidence: it removes many no-op `set_target()` calls.
- Wall-time effect is not uniformly stable row-by-row under this noisy local diagnostic.
- It should remain opt-in until repeated same-host runs show it is consistently beneficial.

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- Rust path default: `off`
- Fallback path exists: `yes`

Semantic boundary:

- `_transition_output()` still calls the existing `_transition()` implementation.
- No `transition()` math was moved to Rust in 041.
- No event/timer/breakpoint ordering rule was changed.
- Active-set only affects which inactive transition states are scanned for future breakpoints; inactive states already returned `None` before.

## Validation

Commands run:

```bash
python3 -m pytest tests/test_engine.py::TestCompiledModelHelpers::test_transition_active_set_skips_inactive_breakpoint_scan tests/test_engine.py::TestCompiledModelHelpers::test_next_breakpoint_with_active_transition tests/test_engine.py::TestCompiledModelHelpers::test_fused_transition_contribution_matches_default_output tests/test_engine.py::TestCompiledModelHelpers::test_fused_transition_contribution_handles_differential_output tests/test_engine.py::TestCompiledModelHelpers::test_transition_unchanged_target_fastpath_preserves_interruption -q
python3 -m pytest tests/test_engine.py -k 'transition or breakpoint or timer or event' -q
python3 -m pytest tests/test_netlist.py -k 'transition or rust_static_eval or logs' -q
python3 -m pytest tests/test_indexed_backend.py -k 'transition or static_linear or dynamic_bus or state_array' -q
python3 -m pytest -q
cargo test
```

Results:

```text
transition targeted: 5 passed
engine transition/event/timer selector: 76 passed, 132 deselected
netlist selector: 12 passed, 63 deselected
indexed selector: 7 passed, 27 deselected
EVAS full pytest: 492 passed
Rust core: 8 passed
r52 top-wall: 10/10 PASS
r53 top-wall: 10/10 PASS
r54 top-wall: 10/10 PASS
```

## Learning Notes

### 什么是 `transition()`？

Verilog-A 的 `transition(x, delay, rise, fall)` 可以理解为“不要让输出瞬间跳变，而是按 delay/rise/fall 生成一段平滑斜坡”。EVAS 里每个 `transition()` 都有一个 `TransitionState`，保存当前值、目标值、起始时间、上升/下降时间和是否 active。

### 为什么 inactive transition 也会慢？

inactive transition 表示这段斜坡已经结束。以前 breakpoint scan 仍然会遍历所有 transition state，再问每个 state 有没有下一个 breakpoint。单个 state 很便宜，但 CPPLL/PRBS 这种每步很多、总步数也多的模型，会把“小动作”放大成明显开销。

### 为什么 `target` 不变还会慢？

很多数字/混合信号模型每一步都重新执行：

```verilog
V(out) <+ transition(state ? 1.0 : 0.0, 0, tr, tr);
```

但 `state` 只有事件触发时才变。也就是说，大部分 step 里 target 没变。若每次都调用 `set_target()`，Python 会重复检查/更新同一批字段。`transition_unchanged_fastpath` 的意义就是：target、delay、rise、fall 都没变时，直接返回当前 transition value。

### 为什么这还不是 Rust 化核心完成？

041 仍然在 Python 里做 transition 状态机，只是减少部分 Python 重复动作。真正的 Rust 化需要把下面这些都变成 typed array / Rust loop：

- transition state arrays
- integer state arrays
- dynamic bus index
- event body execution
- timer/cross/breakpoint queue

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Active-set missed breakpoint | transition waveform misses an intermediate point or event-heavy tests fail | revert active-set changes in `EVAS/evas/simulator/backend.py::next_breakpoint()` and `_transition()` |
| Differential fastpath writes wrong node baseline | `V(out,vss)` output shifted by vss or fails differential tests | revert `_transition_output(... base ...)` and `_compile_contribution()` differential lowering |
| Counter overhead pollutes speed reports | r52/r53 style wall-time regression without functional failure | keep counters but avoid using instrumented local runs for claims; rerun stable same-host report |
| Unchanged-target opt-in changes interrupted-transition semantics | `test_transition_unchanged_target_fastpath_preserves_interruption` fails | keep `evas_transition_unchanged_fastpath` off and revert only that fastpath branch |

## Next Step

`042 - Integer State And Transition Target IR For Real Models`

The next useful step is to stop adding small Python helpers and instead lower the real event-heavy state path:

1. Add typed integer scalar slots for common flags/counters (`q`, `state`, `clk_state`, `valid_q`, `lock_state`).
2. Build a transition-target IR: evaluate target expression from node/state arrays, then update transition state in a batch.
3. Keep event/timer/breakpoint queue migration for later, after state and transition arrays are stable.
