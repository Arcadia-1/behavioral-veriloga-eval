# 072 - Stage55 CPPLL Rust Trace And Lean Production Mode

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_stage55_topwall10_072_20260604.json`
- `speed-optimization/reports/rust_stage55_topwall10_072_20260604.md`
- `/private/tmp/vaevas_rust55_topwall10_lean.json`
- `/private/tmp/vaevas_rust55_cppll_strict_lean.json`

The `/private/tmp` files are local raw runner artifacts from this audit run.
The durable repo-level audit entry is the paired JSON/Markdown report under
`speed-optimization/reports/`.

## One-Line Summary

把 CPPLL reacquire whole-segment trace 的后半段从 Python trace fill 迁到 Rust ABI，并新增 lean `profile_fast_rust_55` speed mode。当前 top-wall 10 EVAS-only smoke 为 `10/10 PASS`，总 wall `12.7811s -> 5.1682s`，top-wall weighted production fastpath coverage 达到 `80.6%`，超过这轮 `55%` 阶段目标。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust core | CPPLL reacquire trace fill 在 Python whole-segment executor 中逐点生成 | 新增 `cppll_reacquire_trace_for_arrays()` 和 `evas_rust_cppll_reacquire_trace` | 默认仿真不变 |
| Python Rust wrapper | `RustBackend` 不能调用 CPPLL reacquire trace | 新增 `RustBackend.cppll_reacquire_trace()`，固定 7 列输出 ABI | 默认仿真不变 |
| Engine dispatch | CPPLL event schedule/transition target 数组生成后仍由 Python 回填 trace | opt-in whole-model mode 下优先调用 Rust trace；失败 fallback Python | checker/CSV/strobe 行为不变 |
| Speed runner | 只有 broad Rust modes，容易把 shadow/prototype 开关一起打开 | 新增 lean `profile_fast_rust_55`，只启用 production whole-segment path | speed experiment 口径更清楚 |
| Tests | 没有锁住 stage-55 mode 的 option surface | 新增 speed mode regression tests，防止 prototype switches 混入 | 防止后续误报速度 |

## Principle

这一步降低的是**每步成本**，不是改变步长、容差或 checker。

CPPLL reacquire row 的慢点来自固定长 trace 生成：

1. Python 已经能通过 semantic/dataflow matcher 判断这是 CPPLL reacquire 行为族。
2. Python 仍负责 source/event schedule 的准备，因为这部分还包含 model-specific event construction。
3. 一旦 ref/dco/fb/vctrl/lock 的事件数组准备好，后续就是规则固定的 typed-array trace fill。
4. Rust 在一个连续数组 loop 中生成 `VDD/VSS/ref/dco/fb/vctrl/lock` 7 列，避免 Python 每点 dict/object/list 操作。

换句话说，Rust 不是“直接把一个 Python 函数原样翻译过去”，而是把已经证明安全的一整段行为降成数组计算。这个边界保留了原来的事件语义，也保留了 Python fallback。

## Why The Lean Mode Matters

早先的 broad `rust55` candidate 同时打开了 static fast sync、timer/event、event write、transition unchanged 等 prototype path。它在 covered rows 上能加速，但在没有 whole-segment coverage 的 gain-extraction rows 上会引入额外检查、FFI、同步或 fallback 成本，导致局部约 `2x` 变慢。

因此 `profile_fast_rust_55` 被收紧成 lean production mode：

```text
evas_profile=fast
evas_skip_source_error_control=yes
evas_rust_full_model_fastpath=true
evas_rust_required=true
```

这些选项只允许已经进入 production whole-segment fastpath 的模型运行 Rust。没有 candidate 的 row 会尽快保持普通 fast 路径，而不是带着 prototype 开销绕一圈。

## Before / After Evidence

Top-wall 10 EVAS-only lean result:

| Metric | Before | After |
|---|---:|---:|
| Mode | `profile_fast_skip_source_error_control` | `profile_fast_rust_55` |
| PASS rows | `10/10` | `10/10` |
| Total wall | `12.781119709s` | `5.168195082s` |
| Total wall speedup | baseline | `2.473x` |
| Fastpath weighted wall | n/a | `10.307728334s` |
| Stage completion | n/a | `80.6%` |

CPPLL EVAS `strict_current` parity smoke:

| Metric | Value |
|---|---:|
| Rows | `2` |
| Rust55 PASS | `2/2` |
| Rust55 safe vs EVAS `strict_current` | `2/2` |
| Rust55 unsafe vs EVAS `strict_current` | `0` |
| Rust55 total wall | `1.106783209s` |
| EVAS `strict_current` total wall | `5.386167458s` |
| Geomean speedup vs EVAS `strict_current` | `4.864x` |
| CPPLL Rust trace fallbacks | `0` |

## Completion And Speed Ledger

| Ledger | Before 072 | After 072 | Delta | Meaning |
|---|---:|---:|---:|---|
| Full release semantic Rustification estimate | `~30%` | `~30%` | `+0 pp` | 通用 Verilog-A 语义仍未全量 Rust 化 |
| Top-wall production-fastpath stage coverage | below stage target | `80.6%` | stage passed | 这是本轮 55% 阶段验收口径 |
| Top-wall 10 total wall | `12.7811s` | `5.1682s` | `2.473x` | EVAS-only top-wall engineering speedup |
| CPPLL EVAS `strict_current` safe rows | n/a | `2/2` | PASS | CPPLL Rust trace 没有破坏 EVAS `strict_current` parity smoke |

这里的 `80.6%` 不能写成“EVAS 已经 80.6% Rust 化”。它只表示当前 top-wall 10 中，按原 fast wall 加权，已有生产 whole-segment Rust fastpath 覆盖了 80.6% 的时间权重。

这里的 `strict_current` 是 EVAS runner 内部的 strict baseline，不是 Cadence
Spectre strict。Spectre/AX 相关结论仍需要同 slice、同服务器、同配置的
dual rerun。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- New opt-in switch: `EVAS_RUST_CPPLL_TRACE=0/1`
- New runner mode: `profile_fast_rust_55`

Rust fallback increments `rust_full_model_cppll_reacquire_rust_fallbacks` and returns to the old Python trace fill.

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_55 \
python3 -m py_compile \
  EVAS/evas/simulator/engine.py \
  EVAS/evas/simulator/rust_backend.py \
  EVAS/tests/test_rust_backend.py

cargo test --release

PYTHONPATH=EVAS \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_55 \
python3 -m pytest EVAS/tests/test_rust_backend.py -q

PYTHONPATH=behavioral-veriloga-eval/runners \
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_55 \
python3 -m pytest behavioral-veriloga-eval/tests/test_vabench_release_evas_speed_modes.py -q
```

Results:

```text
py_compile: PASS
cargo test --release: 29 passed
pytest EVAS/tests/test_rust_backend.py -q: 30 passed
pytest behavioral-veriloga-eval/tests/test_vabench_release_evas_speed_modes.py -q: 2 passed
top-wall 10 lean rust55 smoke: 10/10 PASS
CPPLL tb/e2e EVAS strict_current parity smoke: 2/2 safe_vs_strict
```

## Learning Notes

现在可以比较清楚地看到 Rust 化收益的来源：

- 小 helper Rust 化经常会被 Python/Rust FFI、dict sync 和 fallback 判断吃掉。
- 整段行为 Rust 化能一次跨过 generated model evaluate、event body、transition update、output write 和 record fill，收益才会显著。
- speed mode 必须区分 production path 和 prototype/shadow path；后者用于正确性审计，不适合混进速度结论。
- top-wall coverage 和 release-wide semantic coverage 是两个不同指标，前者用于指导优化优先级，后者用于判断“支持范围”。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| CPPLL Rust trace 与 Python trace fill 有边沿差异 | CPPLL checker FAIL 或 EVAS `strict_current` parity smoke unsafe | 设置 `EVAS_RUST_CPPLL_TRACE=0` |
| Rust dylib 旧版本缺少 symbol | fallback counter 增加或 wrapper 抛 `RustBackendError` | 重新 build Rust core；临时关闭 CPPLL Rust trace |
| broad prototype switch 再次混入 speed mode | no-candidate rows 变慢，top-wall 总 wall 回升 | speed mode test 会失败；恢复 lean option set |
| 将 top-wall stage coverage 误写成 release-wide Rustification | 报告口径过 claim | 引用本审计的 claim boundary |

## Next Step

下一步不再追求更多零散 helper。优先把还没有 production fastpath 的 top-wall rows 继续整段 lowering：

- gain-extraction convergence flow 的 event/evaluate/record 组合；
- PFD/up-dn 这类小 row 的固定外层开销和 mode overhead；
- generated evaluate IR 的真实模型覆盖；
- record/CSV/source packing 的 array path，减少 E2E 剩余开销。
