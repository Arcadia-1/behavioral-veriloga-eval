# 063 - PRBS7 Whole-Model Rust Fastpath

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `/private/tmp/vaevas_prbs7_fullmodel_speed_local.json`
- `/private/tmp/vaevas_prbs7_fullmodel_speed_local.md`
- `/private/tmp/vaevas_topwall10_fullmodel_speed_local.json`
- `/private/tmp/vaevas_topwall10_fullmodel_speed_local.md`

## One-Line Summary

把真实 top-wall PRBS7 模型的 `source update + cross event + event body + transition output + record trace` 整段下沉到一次 Rust trace batch，证明 whole-model lowering 可以带来大幅 kernel 加速。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust kernel | 只有分散的 transition/timer/event primitive | 新增 `evas_rust_prbs7_trace`，一次调用生成整条 PRBS7 waveform trace | 不变 |
| Python ctypes | Rust backend 只能调用局部 primitive | 新增 `RustBackend.prbs7_trace(...)`，返回 row-major trace 和 cross event count | 不变 |
| Simulator engine | PRBS7 仍逐步执行 Python source、cross、event body、transition、record | `rust_full_model_fastpath=true` 且匹配安全条件时，直接进入 Rust whole-model trace；否则回退原 Python loop | 不变 |
| Netlist runner | 无 whole-model Rust simopt | 新增 `evas_rust_full_model_fastpath` / `EVAS_RUST_FULL_MODEL_FASTPATH` pass-through | 不变 |
| Speed harness | 可能优先调用 `/Users/bucketsran/bin/evas` 旧安装版本 | `simulate_evas.py` 优先使用当前 workspace 的 `EVAS` 源码路径 | 不变，但速度结果不再混入旧二进制 |

## Principle

这个改动同时属于 **降低每步成本** 和 **减少 Python/Rust 边界次数**。

前面几轮小 primitive 失败或收益不稳定，根因很清楚：如果每一步仍由 Python 负责调度，再频繁通过 `ctypes` 调一个很小的 Rust 函数，FFI、dict sync、indexed-array snapshot 和 Python object 更新会吃掉 Rust loop 的收益。

这轮改法反过来：对一个真实高频模型直接做整段 lowering。

```text
Python old path per step:
  update pulse/DC sources
  scan cross(CLK) / cross(RSTB)
  call generated Python evaluate/event body
  update integer LFSR state
  evaluate 7 transition(...) outputs
  record named signals through Python objects

Rust whole-model path:
  build one time grid
  Rust computes pulse/DC source values
  Rust detects rising CLK threshold crossings
  Rust applies reset/en/LFSR shift logic
  Rust evolves 7 transition state machines
  Rust fills all recorded signal columns in one array
```

数学上没有改变模型语义。PRBS7 的核心状态递推是固定的 7-bit LFSR：

```text
feedback = bit6 xor bit5
state_next = [feedback, bit0, bit1, bit2, bit3, bit4, bit5]
serial_out = bit6
```

输出端仍使用同一类 `transition(target, td, trf, trf)` 状态演化，只是从 Python object 调用变成 Rust array loop。

## Safety Conditions

当前只对下面的完整模式启用：

- exactly one generated model；
- model class name 是 `prbs7_ref_Model`；
- 没有 child model；
- recorded signals 只包含 `clk`、`rst_n`、`en`、`serial_out`、`state_0` 到 `state_6`；
- `clk` 和 `rst_n` 是带 metadata 的 pulse source；
- `en` 是 DC source；
- model params 可解析为 `vdd`、`vth`、`trf`、`td`、`seed`；
- Rust backend 可加载。

任何条件不满足，都会返回 `None` 并回到原 Python simulator loop。

这不是最终通用编译器方案，而是一个 intentionally narrow 的 whole-model production fastpath，用来证明方向是否值得继续。

## Before / After Evidence

### Single PRBS7 Row

Row: `vbr1_l1_lfsr_prbs_generator/dut/gold`

Command:

```bash
PYTHONPATH=../EVAS:runners PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite all \
  --entry vbr1_l1_lfsr_prbs_generator \
  --form dut \
  --mode strict_current \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_full_model \
  --output-root /private/tmp/vaevas_prbs7_fullmodel_speed_local \
  --report-json /private/tmp/vaevas_prbs7_fullmodel_speed_local.json \
  --report-md /private/tmp/vaevas_prbs7_fullmodel_speed_local.md \
  --timeout-s 120 \
  --jobs 1
```

| Mode | PASS | Safe vs strict | E2E wall s | EVAS subprocess wall s | Tran wall s | Key counters |
|---|---:|---:|---:|---:|---:|---|
| `strict_current` | yes | reference | 4.4112 | 4.3858 | 4.1938 | `steps_total=89315`, `transition_calls_total=714536`, `model_prepare_step_calls=89315` |
| `profile_fast_skip_source_error_control` | yes | yes | 0.4069 | 0.3791 | 0.2156 | `steps_total=3673`, `transition_calls_total=29400`, `model_prepare_step_calls=3673` |
| `profile_fast_rust_full_model` | yes | yes | 0.2961 | 0.2634 | 0.0085 | `rust_full_model_fastpath_enabled=1`, `points=3363`, `cross_events=120`, `transition_calls_total=0`, `model_prepare_step_calls=0` |

Interpretation:

- 相对当前 Python fast EVAS，PRBS7 **kernel/tran wall** 从 `0.2156s` 降到 `0.0085s`，约 `25.4x`。
- 相对当前 Python fast EVAS，PRBS7 **E2E wall** 从 `0.4069s` 降到 `0.2961s`，约 `1.37x`。
- 相对 strict EVAS，PRBS7 **E2E wall** 从 `4.4112s` 降到 `0.2961s`，约 `14.9x`。
- `transition_calls_total` 和 `model_prepare_step_calls` 归零，说明这条路径确实绕过了 generated Python model loop，而不是只改了外层 harness。

### Top-Wall 10 Diagnostic

Command:

```bash
PYTHONPATH=../EVAS:runners PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
python3 runners/run_vabench_release_evas_speed_experiment.py \
  --speed-artifact speed-optimization/reports/current_fourway_topwall10_clean_20260604.json \
  --suite top-wall \
  --limit 10 \
  --mode profile_fast_skip_source_error_control \
  --mode profile_fast_rust_full_model \
  --output-root /private/tmp/vaevas_topwall10_fullmodel_speed_local \
  --report-json /private/tmp/vaevas_topwall10_fullmodel_speed_local.json \
  --report-md /private/tmp/vaevas_topwall10_fullmodel_speed_local.md \
  --timeout-s 180 \
  --jobs 2
```

| Scope | Python fast E2E wall s | Rust fullmodel mode E2E wall s | Speedup | Interpretation |
|---|---:|---:|---:|---|
| PRBS7 covered row | 0.3726 | 0.2026 | 1.84x | 该 run 中 PRBS7 fastpath 命中，kernel 约 40x |
| Top-wall 10 total | 19.9036 | 19.7883 | 1.006x | 只有 PRBS7 命中，其余模型 fallback，整体收益自然很小 |

Top-wall 10 中两个 gain-extraction local rows 在两种模式下都出现同样的 TB compile failure；它不影响 PRBS7 fastpath 的局部结论，但这轮 top-wall 10 只能作为 EVAS-only diagnostic，不是 paper-facing release speed claim。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Unsupported models lose functionality: `no`

## Validation

Commands run:

```bash
cargo test --release
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile \
  EVAS/evas/simulator/engine.py \
  EVAS/evas/simulator/rust_backend.py \
  EVAS/evas/netlist/runner.py \
  behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache \
  python3 -m pytest EVAS/tests/test_rust_backend.py -q
```

Results:

```text
cargo test --release: 29 passed
py_compile: PASS
tests/test_rust_backend.py: 20 passed
direct Rust backend prbs7_trace: 2401 points in about 0.00015s-0.00040s, events=120
direct local EVAS fullmodel PRBS7: tran wall 7.7ms, transition_calls_total=0, err_ratio=0
speed runner PRBS7: PASS and safe_vs_strict=true
```

## Learning Notes

这轮终于能看到大速度提升，是因为改造单位变了。

不够有效的方式：

```text
Python loop
  -> 每一步调用很多 Python 函数
  -> 偶尔调用一个很小的 Rust primitive
  -> 回 Python 同步 dict/array/state
```

有效的方式：

```text
Python 只做一次模式识别和参数打包
Rust 一次性完成整段模型行为
Python 只接收最终 trace
```

可以把它理解为：不是把一颗螺丝换成 Rust，而是把一整台机器的传动链放进 Rust。只要还在每步回 Python，`dict[str, float]`、函数调用、对象同步、CSV/record/checker 都会成为新的瓶颈。

这也是为什么 PRBS7 的 kernel wall 可以 `25x+`，但 E2E 只有 `1.37x`：当核心仿真只剩几毫秒后，进程启动、netlist/parser、CSV 写出、checker 调用这些固定成本就开始显眼。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| PRBS7 source metadata 漏识别，导致错误启用 | `rust_full_model_fastpath_fallbacks_total` 非零或 waveform parity fail | revert engine `_try_rust_prbs7_full_model_fastpath` |
| Rust trace column order 与 CSV/checker 期望不一致 | PRBS7 checker fail 或 trace header mismatch | revert `RustBackend.prbs7_trace` wrapper and engine trace mapping |
| harness 调用了旧安装 EVAS，速度数字失真 | perf counters 缺少 `rust_full_model_fastpath_enabled=1` 或 tran wall 异常大 | keep `simulate_evas.py` local-source precedence fix |
| per-model hardcoding 扩散成不可维护特例 | 新模型继续手写 class-name fastpath | 下一步必须做 structural recognizer / generated whole-segment lowering，不继续复制 PRBS7 特例 |

## Next Step

- `064 - Structural Whole-Segment Lowering Plan`: 把 PRBS7 的手写 fastpath 总结成 compiler pattern，优先覆盖 top-wall 中的 SAR loop、CPPLL timer/event、propagation-delay comparator 和 measurement-heavy gain flow。
