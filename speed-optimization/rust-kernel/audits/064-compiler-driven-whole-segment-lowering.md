# 064 - Compiler-Driven Whole-Segment Lowering

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `/private/tmp/vaevas_wseg_checker_top4_seq.json`
- `/private/tmp/vaevas_wseg_checker_top4_seq.md`
- `/private/tmp/vaevas_prbs7_compiler_fullmodel_speed.json`
- `/private/tmp/vaevas_topwall10_compiler_fullmodel_speed.json`

## One-Line Summary

把 063 的手写 PRBS7 whole-model fastpath 泛化为 compiler-emitted whole-segment lowering，并优先覆盖 CPPLL、SAR、propagation-delay comparator、gain measurement 四类 top-wall 热模型；四条 runner 回归全部 PASS，顺序 E2E wall 合计 `9.999s -> 6.819s`，核心 tran 合计 `5.657s -> 0.451s`。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Compiler | 只有 PRBS7 class-name/结构路径 | `backend.py` 为多类真实热模型生成 `_whole_segment_candidates` | 默认不变 |
| Candidate types | `cross_scalar_lfsr_transition_bus_v1` | 新增 gain、cmp-delay、edge timer、SAR、DAC、S/H、ref-step、CPPLL metadata | 默认不变 |
| Engine dispatch | 手写 PRBS7 fastpath | `Simulator._try_compiler_whole_segment_fastpath()` 按 candidate kind 分派 | 仅 opt-in |
| Hot-model execution | 每步调用 generated Python model evaluate / event / transition | candidate 命中时一次性生成整段 trace，模型循环调用归零 | 仅 opt-in |
| Rust ABI | generic LFSR transition trace | LFSR 已是 Rust ABI；四条 top-wall trace executor 先在 Python engine 侧落地 | 默认不变 |
| Runner label | P10 表示 PRBS7 full-model | P10 表示 compiler-driven whole-segment fast path | 报告口径更新 |

## Principle

这轮的关键不是“继续手写某个模型名”，而是把可加速行为变成 compiler lowering：

```text
Verilog-A source
  -> parser / compiler sees ports, states, params, event/timer/transition shape
  -> emits _whole_segment_candidates
  -> engine checks candidate + instance wiring + recorded signals + source shapes
  -> matched segment bypasses generated Python model loop
  -> one trace fill produces SimResult / CSV-visible signals
```

所以以后扩展不是写 `if model_name == ...`，而是：

1. compiler 识别一个安全行为模板；
2. candidate metadata 描述端口、状态、参数、输出映射；
3. engine/Rust executor 用 metadata 批量执行；
4. checker/parity gate 不过就 fallback。

## Candidate Coverage

| Model class | Candidate kind | Production opt-in path | Notes |
|---|---|---|---|
| PRBS/LFSR cross generator | `cross_scalar_lfsr_transition_bus_v1` | Rust ABI trace | variable width/taps/output map |
| Gain measurement | `gain_timer_reduction_v1` | Python whole-segment trace | timer reduction + transition outputs |
| Propagation-delay comparator | `cmp_delay_log_transition_v1` + `edge_interval_timer_v1` | Python whole-segment trace | log-linear delay + edge interval monitor |
| Weighted SAR loop | `weighted_sar_adc_v1` + `weighted_dac_v1` + `sample_hold_rising_v1` | Python whole-segment trace | S/H + SAR state + DAC output batch |
| CPPLL reacquire | `ref_step_clock_v1` + `cppll_timer_v1` | Python whole-segment trace | ref-step timer + DCO timer + fb/ref crossing + lock/vctrl |

The four new top-wall paths are intentionally conservative:

- They require exact candidate kinds and expected model interconnect.
- They reject unsupported recorded signals.
- They require simple source shapes such as DC VDD/VSS or pulse clock where needed.
- If any condition is not met, EVAS falls back to the normal simulator path.

## Speed Evidence

Command:

```bash
PYTHONPATH=../EVAS:runners PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
  python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --entry vbr1_l1_gain_estimator \
  --entry vbr1_l1_propagation_delay_comparator \
  --entry vbr1_l2_weighted_sar_adc_dac_loop \
  --entry vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow \
  --form tb --form dut \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_full_model \
  --output-root /private/tmp/vaevas_wseg_checker_top4_seq \
  --report-json /private/tmp/vaevas_wseg_checker_top4_seq.json \
  --report-md /private/tmp/vaevas_wseg_checker_top4_seq.md \
  --timeout-s 240 --jobs 1
```

Sequential runner result:

| Entry | Form | Status | E2E wall before | E2E wall after | E2E speedup | Tran before | Tran after | Tran speedup | Model calls before -> after |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `vbr1_l1_gain_estimator` | `tb` | PASS/PASS | `0.193s` | `0.174s` | `1.11x` | `0.0275s` | `0.0111s` | `2.48x` | `1231 -> 0` |
| `vbr1_l1_propagation_delay_comparator` | `dut` | PASS/PASS | `1.758s` | `0.621s` | `2.83x` | `1.2185s` | `0.0119s` | `102.39x` | `59174 -> 0` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | PASS/PASS | `2.488s` | `0.708s` | `3.52x` | `2.0535s` | `0.2140s` | `9.60x` | `90476 -> 0` |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | PASS/PASS | `5.561s` | `5.316s` | `1.05x` | `2.3575s` | `0.2136s` | `11.04x` | `48795 -> 0` |
| **Total** | 4 rows | **4/4 PASS** | **`9.999s`** | **`6.819s`** | **`1.47x`** | **`5.657s`** | **`0.451s`** | **`12.55x`** | **all -> 0** |

Interpretation:

- The core simulator loop improvement is now real on the targeted hot rows: generated model evaluate / transition calls are bypassed.
- E2E gains are smaller than tran gains because runner/checker/CSV/process overhead now dominates short rows.
- SAR is the clearest example: tran is `11.04x` faster, but E2E is only `1.05x`; the remaining bottleneck is outside the lowered model loop.

This is EVAS-only candidate evidence. It is not a Spectre-vs-EVAS paper speed claim.

## Correctness Gate

| Gate | Result |
|---|---|
| Four-row runner behavior checker | `4/4 PASS` in both baseline and whole-segment mode |
| `profile_fast_rust_full_model` fallback safety | opt-in only; default path unchanged |
| model loop bypass counters | all four whole-segment rows show `model_prepare_step_calls=0`, `transition_calls_total=0` |
| unsupported feature behavior | fallback to normal EVAS path |

## Validation

Commands run:

```bash
cargo test --release

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile \
  EVAS/evas/simulator/backend.py \
  EVAS/evas/simulator/engine.py \
  EVAS/evas/simulator/rust_backend.py \
  EVAS/tests/test_rust_backend.py \
  behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py

PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
  python3 -m pytest EVAS/tests/test_rust_backend.py -q
```

Results:

```text
cargo test --release: 29 passed
py_compile: PASS
EVAS/tests/test_rust_backend.py: 23 passed
top4 sequential runner: 4/4 PASS in baseline and whole-segment modes
```

## Learning Notes

这里有一个很重要的分层：

```text
compiler-driven lowering != already all in Rust
```

本轮已经完成的是“让编译器决定整段行为能不能被下沉”，并且让 engine 按整段行为生成 trace。它能大幅减少 Python generated model loop，因为原来每个小步都要：

```text
prepare_step -> evaluate model -> event body -> transition update -> record
```

现在 candidate 命中时变成：

```text
compile once -> simulate event schedule in one segment -> fill output arrays
```

但四条新热模型的 executor 目前仍在 Python engine 侧。它们证明了 whole-segment lowering 的边界和正确性，下一步才是把这些 executor 迁到 Rust ABI，让事件队列、transition、record/CSV 必要数据都走 typed arrays。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Pattern 过宽误命中非目标模型 | unexpected candidate or checker fail | tighten `_collect_*_candidate` or disable executor dispatch |
| CPPLL event ordering 与普通 EVAS 不一致 | CPPLL checker fail, lock/relock metrics drift | disable `_try_cppll_reacquire_fastpath` |
| SAR trace 只改善 tran 不改善 E2E | E2E wall remains flat | move checker/record/CSV to array path; do not overclaim |
| Python trace executor 成为新瓶颈 | tran no longer scales on longer rows | migrate executor body to Rust ABI |

## Next Step

- `065 - Rust ABI For Whole-Segment Executors`: 把 CPPLL/SAR/cmp/gain trace executor 从 Python engine 迁到 Rust `cdylib`，保留相同 candidate metadata 和 checker gate。
- `066 - Array Record/CSV Narrowing`: 对 SAR 这类 E2E 仍慢的任务，只输出 checker 必需信号或走 array-backed record，减少 CSV/checker 外层开销。
- `067 - Same-Server EVAS/Spectre Rerun`: 只有在同机、同 row、同容差/步长和 checker parity 下，才能把这些 EVAS-only candidate 数字升级成 paper-facing speed evidence。
