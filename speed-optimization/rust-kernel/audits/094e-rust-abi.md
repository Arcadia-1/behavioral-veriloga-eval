# 094e - Rust Body IR ABI Foundation

Status: `done` (synthetic ABI only; no production dispatch)

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `094a-expression-ir.md`
- `094b-statement-ir.md`
- `094c-schedule-ir.md`
- `094d-state-binding-ir.md`
- `094-verilog-a-body-rust-kernel-design.md`
- `../STAGE_2_4_EXECUTION_PLAN.md`

## One-Line Summary

新增 `evas_rust_evaluate_body_ir` Rust ABI 和 Python `RustBackend.evaluate_body_ir()` wrapper，用 stack-machine op array 表达 body expression，并一次性写回 node/state typed arrays。100 组随机 synthetic IR 的 Rust 结果与 Python oracle 一致。该 audit 仍不接入生产仿真路径，速度收益为 **0%**。

## Why This Exists

094a-d 已经能把 Verilog-A expression、statement、event schedule 和 symbol binding 表示成 Python-side IR。094e 的目标是建立 Rust 可以消费的最小 ABI：

```text
Python generated body:
    out = state0 * gain + vin - offset

094e encoded body:
    expr_ops = [
        READ_STATE state0,
        READ_PARAM gain,
        MUL,
        READ_NODE vin,
        ADD,
        READ_PARAM offset,
        SUB,
    ]
    stmt_ops = [
        WRITE_NODE out, expr_ops[0:7]
    ]

Rust execution:
    stack machine evaluates expr_ops
    node_values[out_slot] = stack_result
```

关键收益不是这一轮已经加速，而是后续 094f/g 可以把很多 Python generated `model.evaluate()` body 合成一次 Rust batch，而不是在每个小函数上付 ctypes FFI 成本。

## What Changed

EVAS Rust core:

| File | Change |
|---|---|
| `evas/rust_core/src/lib.rs` | 增加 `EvasRustBodyExprOp` / `EvasRustBodyStmtOp` |
| `evas/rust_core/src/lib.rs` | 增加 `evaluate_body_ir_ops()` stack-machine evaluator |
| `evas/rust_core/src/lib.rs` | 增加 C ABI `evas_rust_evaluate_body_ir()` |
| `evas/rust_core/src/lib.rs` | 增加 Rust unit tests for expression stack and integer state write |

Python wrapper:

| File | Change |
|---|---|
| `evas/simulator/rust_backend.py` | 增加 body expression op constants |
| `evas/simulator/rust_backend.py` | 增加 `BodyExprOp` / `BodyStmtOp` dataclasses |
| `evas/simulator/rust_backend.py` | 增加 `RustBodyIrBatch` ctypes-backed storage |
| `evas/simulator/rust_backend.py` | 增加 `make_body_ir_batch()` / `evaluate_body_ir()` |

Tests:

| File | Coverage |
|---|---|
| `tests/test_rust_backend.py` | Python ctypes bridge can call Rust body IR ABI |
| `tests/test_rust_backend.py` | 100 deterministic random state-write expressions match Python oracle |

Supported expression op families in this ABI:

| Family | Ops |
|---|---|
| Reads | const, node, state, parameter |
| Unary | negation, logical not |
| Arithmetic | add, subtract, multiply, divide, modulo |
| Comparison | `>`, `<`, `>=`, `<=`, `==`, `!=` |
| Logical/bitwise | logical and/or, bitwise and/or/xor |
| Select | ternary select |
| Math calls | abs, sqrt, exp, ln, log10, sin, cos, floor, ceil, min, max, pow |

## Validation

```bash
cargo test --manifest-path EVAS/evas/rust_core/Cargo.toml --release
# 34 passed

PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_rust_backend.py -q
# 36 passed

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_audit_094a_expr_ir.py \
  EVAS/tests/test_audit_094b_stmt_schedule_ir.py \
  EVAS/tests/test_audit_094d_state_binding_ir.py \
  EVAS/tests/test_rust_backend.py -q
# 48 passed

PYTHONPATH=EVAS python3 -m pytest EVAS/tests -q
# 620 passed
```

Random parity scope:

| Metric | Value |
|---|---:|
| Random cases | 100 |
| Expression shape | `(state0 * param0) + node0 - bias` |
| Target kinds | scalar state writes |
| Integer target cases | 50 |
| Rust/Python mismatches | 0 |

## Functional Safety

| Question | Answer |
|---|---|
| Default backend changed? | no |
| 091d generic executor changed? | no |
| Engine dispatch changed? | no |
| Node/state storage changed? | no |
| CSV/checker changed? | no |
| Speed claim enabled? | no |

## Claim Boundary

**可以说**：

- 094e 已经建立 Rust body IR synthetic ABI。
- Python `RustBackend` 可以把一批 expression/write ops 一次性送入 Rust。
- Rust ABI 可以原地写回 node/state typed arrays。
- 100 组 synthetic IR state-write parity 通过。
- 全量 EVAS pytest 通过，说明该 ABI 当前没有破坏现有生产路径。

**不能说**：

- EVAS 已经把 generated `model.evaluate()` 全量迁到 Rust。
- 094e 已经带来仿真速度提升。
- event queue、cross/timer scheduling、transition output、record/CSV 已经通过这个 ABI 统一迁移。
- 可以 default-on generic Rust executor。
- 可以 claim 快于 Spectre AX。

## Next Step

进入 094f/094g：

1. 把 094a-d 的 source-level IR lowering 接到 094e body op encoder。
2. 扩展 expression evaluator 的 real-model 覆盖，尤其是 dynamic array/state access、branch access 和 method call fallback gate。
3. 把 event due、event body、output write、record 组织成一次 Rust batch。
4. 先做 shadow parity，再考虑 opt-in production dispatch。
5. 只有 real-row waveform parity 和 sweep 通过后，才讨论 default-on。
