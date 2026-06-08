# 117 - RustSimProgram While Body Gate

Status: `done`

Date: `2026-06-06`

Code commit: `pending`

Related reports:

Raw JSON files are archived intermediate artifacts; this compact split PR keeps
the Markdown summaries needed for review instead of committing the large raw
JSONs.

- `speed-optimization/reports/current_release_rust_coverage_manifest_rustsim_gate_20260606.json`
- `speed-optimization/reports/current_release_rust_coverage_manifest_rustsim_gate_after_while_20260606.json`
- `speed-optimization/reports/current_release_rust_coverage_manifest_rustsim_gate_after_while_20260606.md`
- `speed-optimization/reports/evas2_while_cppll_smoke_20260606.json`
- `speed-optimization/reports/evas2_while_cppll_smoke_20260606.md`

## One-Line Summary

把 RustSimProgram body IR 补齐受控 `while` 控制流，使 release gold VA 静态 lowering gate 从 `355/357` 提升到 `357/357`，并验证 CPPLL e2e/tb strict EVAS2 实跑 PASS 且 `rust_sim_program_rejections=0`。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| coverage manifest | 只统计 Rust signals / whole-segment candidates，不能直接聚合 strict RustSimProgram blocker | 新增 `rustsim_program_gate` per-model 字段和 strict gate counts / blocker counts / opcode totals | 可以直接看到哪些 release model 不能被 Rust-owned EVAS2 schema 表达 |
| BodyStmt ABI | 支持 assignment、contribution、if/else、system side-effect、`$bound_step` | 新增 `BODY_STMT_WHILE` / `BODY_STMT_ENDWHILE`，带 max-iteration guard | 支持 CPPLL phase-wrap 类 while body |
| Python encoder | `WhileStatementIR` 一律拒绝 | 条件表达式和 body 都可编码时生成 while opcode | 不放宽 dynamic array / unknown target / unsupported expression |
| Rust executor | body IR 是顺序单 pass | while 条件 false 时跳过 body，true 时执行 body 并在 `ENDWHILE` 回到条件重判 | 多次迭代由 Rust 执行，不回 Python |

## Principle

这次补的不是一个 CPPLL 特例，而是 Verilog-A event body 中常见的 **bounded normalization loop**。

CPPLL 里的数学形式是：

```text
while phase_err >  0.5 * ref_period: phase_err -= ref_period
while phase_err < -0.5 * ref_period: phase_err += ref_period
```

它的作用是把相位误差折回一个参考周期的主值区间：

```text
phase_err in [-0.5 * ref_period, 0.5 * ref_period]
```

如果这个循环仍然必须由 Python event body 执行，那么 CPPLL 这种 PLL/clock timing row 就不能声明完整进入 RustSimProgram。新增 opcode 后，循环条件、状态读写和每次状态更新都在 Rust typed arrays 中完成。

## Before / After Evidence

全量静态 coverage gate：

| Metric | Before | After |
|---|---:|---:|
| gold VA model rows | 357 | 357 |
| compile pass | 357 | 357 |
| strict RustSimProgram supported | 355 | 357 |
| unsupported rows | 2 | 0 |
| primary blocker `event_body` | 2 | 0 |

被修复的两行是同一个模型的两个 release forms：

| Path suffix | Before | After |
|---|---|---|
| `forms/e2e/gold/cppll_timer_ref.va` | `event_body:while_loop` | supported |
| `forms/tb/gold/cppll_timer_ref.va` | `event_body:while_loop` | supported |

After opcode totals:

| Field | Total |
|---|---:|
| body expr ops | 29473 |
| body stmt ops | 9068 |
| event count | 934 |
| transition count | 930 |
| state count | 1890 |
| side effects | 12 |

## Real Row Smoke

Command:

```bash
PYTHONPATH=runners:../EVAS python3 runners/run_vabench_release_same_server_speed.py \
  --speed-artifact speed-optimization/reports/full_release_rows_for_fourway_20260606.json \
  --suite all \
  --entry vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow \
  --evas-mode profile_fast_evas2 \
  --skip-spectre \
  --timeout-s 300 \
  --jobs 1 \
  --output-root results/evas2-while-cppll-smoke-20260606 \
  --report-json speed-optimization/reports/evas2_while_cppll_smoke_20260606.json \
  --report-md speed-optimization/reports/evas2_while_cppll_smoke_20260606.md
```

Result:

| Form | Status | E2E wall | EVAS subprocess | Reported tran | RustSimProgram counters |
|---|---|---:|---:|---:|---|
| e2e | PASS | 2.068s | 1.838s | 0.913s | requested=1, available=1, enabled=1, rejections=0 |
| tb | PASS | 1.468s | 1.264s | 0.553s | requested=1, available=1, enabled=1, rejections=0 |

This is EVAS-only evidence. It does not compare Spectre AX or create a paper-facing speed claim.

## Functional Safety

- Default Python EVAS path changed: `no`
- Strict EVAS2 behavior changed: `yes`, wider supported subset
- Unsupported Python fallback hidden as Rust: `no`
- Infinite-loop guard: `yes`, while opcode uses a per-loop max iteration count
- Precision semantics changed: `no intended change`; this implements the same repeated assignment semantics in Rust
- Known limitation: this supports body IR while loops whose condition and body are already encodable; it does not support arbitrary dynamic side effects or unbounded loops without guard.

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile \
  evas/simulator/rust_backend.py \
  evas/simulator/stmt_ir.py \
  tests/test_audit_094f_body_ir_encoder.py

cargo fmt
cargo test

PYTHONPATH=. python3 -m pytest tests/test_audit_094f_body_ir_encoder.py -q

PYTHONPATH=runners:../EVAS python3 runners/report_vabench_release_rust_coverage_manifest.py \
  --report-json speed-optimization/reports/current_release_rust_coverage_manifest_rustsim_gate_after_while_20260606.json \
  --report-md speed-optimization/reports/current_release_rust_coverage_manifest_rustsim_gate_after_while_20260606.md
```

Results:

```text
py_compile passed
cargo test: 37 passed
tests/test_audit_094f_body_ir_encoder.py: 9 passed
release coverage gate: 357/357 strict RustSimProgram supported
CPPLL EVAS2 smoke: 2/2 PASS
```
