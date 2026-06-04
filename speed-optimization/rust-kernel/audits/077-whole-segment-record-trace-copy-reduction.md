# 077 - Whole-Segment Record Trace Copy Reduction

Status: `done`
Date: `2026-06-04`

## 结论

本轮做了一个低风险 record/trace path 清理，但不作为主要速度 claim。

改动内容：

- `_record_trace_result(...)` 现在如果收到 `np.ndarray[float64]`，会直接复用连续数组，不再无条件 `np.array(...)` 再拷贝一次。
- gain timer、gain measurement-flow、propagation delay、CPPLL Rust trace path 现在把 Rust flat matrix 切出的 numpy 列直接传给 `_record_trace_result(...)`。
- SAR 暂时保留旧的 list-comprehension column path。实测发现 SAR 的宽 trace 在当前 Python/runner 环境下用 numpy 切列并不稳定更快，不能为了形式统一牺牲 top-wall。

这个改动不改变仿真数学语义：

- 时间点不变。
- 输出列名不变。
- CSV schema 不变。
- `SimResult.signals` 仍是 numpy arrays。
- `recorded_signals` 仍回填为 Python list，保持 legacy API 行为。

## 为什么这样可能更快

075 以后，多个 top-wall 热点已经由 Rust 生成 flat trace matrix。旧路径中有一类重复数据搬运：

```text
Rust flat values
  -> numpy matrix
  -> numpy column copy
  -> Python list
  -> _record_trace_result converts list back to numpy array
  -> recorded_signals converts numpy array back to Python list
```

077 去掉中间的 `numpy column copy -> Python list -> numpy array` 往返。对于 CPPLL/gain-flow 这类列数不多、点数较多的 trace，这应该减少 Python object 分配；对于 SAR 这种宽矩阵，当前 numpy 切列路径没有稳定收益，所以保持旧路径。

## Evidence

Reports:

- `speed-optimization/reports/rust_stage77_record_trace_copy_smoke_20260604.json`
- `speed-optimization/reports/rust_stage77_record_trace_copy_smoke_20260604.md`

Top-wall 10 EVAS-only fast+Rust55 smoke:

| Mode | PASS | Wall s |
|---|---:|---:|
| `profile_fast_skip_source_error_control` | `10/10` | `13.021` |
| `profile_fast_rust_55` | `10/10` | `3.390` |

This smoke is not directly comparable to 076's strict+fast+Rust55 run because it omits strict and has different cold/warm ordering. It is only a regression smoke for the record-copy change.

Selected rows:

| Row | Form | Fast wall s | Rust55 wall s | Fast/Rust55 |
|---|---|---:|---:|---:|
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `2.820` | `0.609` | `4.63x` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `2.601` | `0.650` | `4.00x` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `2.535` | `0.546` | `4.64x` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `1.502` | `0.285` | `5.27x` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `1.178` | `0.275` | `4.28x` |

## Verification

Commands run:

```bash
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_077 \
python3 -m pytest EVAS/tests/test_rust_backend.py \
  -k 'gain_measurement_flow or gain_timer_reduction or sar_loop or cppll or cmp_delay' -q
```

Result:

```text
5 passed, 26 deselected
```

```bash
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache_077 \
python3 -m py_compile EVAS/evas/simulator/engine.py
```

Result: pass.

## What This Does Not Prove

- It does not prove full EVAS Rustification.
- It does not prove Spectre AX speed advantage.
- It does not prove record/CSV is fully optimized.
- It does not justify changing SAR to a numpy-column trace path.

The next real optimization should still be a measured trace/CSV/checker path change with explicit timing split evidence, not a cosmetic rewrite.

