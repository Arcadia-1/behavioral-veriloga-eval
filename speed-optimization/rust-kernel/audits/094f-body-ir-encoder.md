# 094f - ExprIR To Rust Body-Op Encoder

Status: `partial` (source statement write-set to synthetic body-op encoder; no event scheduler)

Date: `2026-06-05`

Code commit: `pending`

Related documents:

- `094a-expression-ir.md`
- `094d-state-binding-ir.md`
- `094e-rust-abi.md`
- `../STAGE_2_4_EXECUTION_PLAN.md`

## One-Line Summary

把 094a-d 的 `ExprIR` / `BindingTableIR` 接到 094e 的 Rust body stack-machine ABI：标量 parameter、标量 state、静态 `V(node)` / `V(node1,node2)`、基础算术/比较/ternary/math function 可以编码为 `BodyExprOp[]` 并通过 Rust ABI 执行。进一步新增 `BodyStmtProgram`，让 ordered block 中的 scalar state assignment 和 single-node voltage contribution 可以编码成 `BodyStmtOp[] + BodyExprOp[]`，并保持源码顺序执行。该 audit 仍不接入 engine/event dispatch，速度收益为 **0%**。

## Why This Exists

094e 证明 Rust ABI 本身可用，但它只消费手写 synthetic ops。094f 的第一步是把真实 Verilog-A AST lowering 出来的 `ExprIR` 连接到这个 ABI：

```text
Verilog-A source
    acc = ((V(vin, vref) * abs(gain)) > thresh) ? acc + 1.0 : 0.0;

094a-d
    ExprIR + BindingTableIR

094f partial
    BodyExprOp[]:
      READ_NODE vin
      READ_NODE vref
      SUB
      READ_PARAM gain
      ABS
      MUL
      READ_PARAM thresh
      GT
      READ_STATE acc
      CONST 1.0
      ADD
      CONST 0.0
      SELECT

094e
    Rust stack machine writes state_values[acc_slot]
```

This connects the IR foundation to the Rust ABI without changing production simulation behavior.

新增 statement-level write-set 后，简单 block 可以合成一个 Rust body batch：

```verilog
acc = V(vin) * gain;
V(out) <+ acc + offset;
```

Rust batch 会先写 `state_values[acc_slot]`，再让第二条 contribution 读取更新后的 `acc` 并写回 `node_values[out_slot]`。

## What Changed

EVAS:

| File | Change |
|---|---|
| `evas/simulator/expr_ir.py` | 增加 `encode_body_expr_ops()` |
| `evas/simulator/expr_ir.py` | 增加 conservative lowering maps for arithmetic, comparison, logical, ternary, and math ops |
| `evas/simulator/stmt_ir.py` | 增加 `BodyStmtProgram` / `encode_body_stmt_ops()` |
| `tests/test_audit_094f_body_ir_encoder.py` | 从 Verilog-A source parse expression/block，lower 到 IR，encode 到 Rust body ops，再通过 Rust ABI 执行 |

Supported encoder subset:

| Verilog-A behavior | Rust body op lowering |
|---|---|
| numeric literal | `BODY_EXPR_CONST` |
| scalar parameter | `BODY_EXPR_READ_PARAM` |
| scalar state | `BODY_EXPR_READ_STATE` |
| static `V(node)` | `BODY_EXPR_READ_NODE` |
| static `V(node1,node2)` | two node reads + `BODY_EXPR_SUB` |
| unary `-`, `!` | `NEG`, `NOT` |
| binary arithmetic/comparison/logical/bitwise | matching stack-machine op |
| ternary `cond ? a : b` | `SELECT` |
| pure math `abs/sqrt/exp/ln/log/sin/cos/floor/ceil/min/max/pow` | matching stack-machine op |

Conservative fallback subset:

| Behavior | Reason |
|---|---|
| dynamic indexed `V(bus[i])` | needs bus offset ownership and event interpolation rules |
| state arrays | binding table does not yet expose flattened element slots to this ABI |
| branch current `I(...)` | current-domain behavior is outside current EVAS voltage-domain claim |
| method calls | string/runtime side effects are not numeric body ops |
| stateful analog functions like `transition()` / `cross()` | must be handled at event/transition scheduler level, not inside scalar expression eval |
| event statements | event due/order scheduler is not yet Rust-owned |
| if/loop/case/system task statement bodies | control-flow lowering needs a separate phase-order gate |
| differential contribution target `V(a,b) <+ expr` | contribution write ownership must define both branch nodes before production |

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094f_body_ir_encoder.py -q
# 4 passed

PYTHONPATH=EVAS python3 -m pytest \
  EVAS/tests/test_audit_094a_expr_ir.py \
  EVAS/tests/test_audit_094b_stmt_schedule_ir.py \
  EVAS/tests/test_audit_094d_state_binding_ir.py \
  EVAS/tests/test_audit_094f_body_ir_encoder.py \
  EVAS/tests/test_rust_backend.py -q
# 52 passed

PYTHONPATH=EVAS python3 -m pytest EVAS/tests -q
# 624 passed
```

Tested source expression:

```verilog
acc = ((V(vin, vref) * abs(gain)) > thresh) ? acc + 1.0 : 0.0;
```

Rust ABI results:

| Input | Expected | Rust result |
|---|---:|---:|
| `vin=0.5`, `vref=0.3`, `acc=3.5`, `gain=-2.0`, `thresh=0.3` | `4.5` | `4.5` |
| `vin=0.4`, `vref=0.3`, `acc=3.5`, `gain=-2.0`, `thresh=0.3` | `0.0` | `0.0` |

Tested ordered statement block:

```verilog
acc = V(vin) * gain;
V(out) <+ acc + offset;
```

Rust ABI results:

| Input | Expected state/output | Rust result |
|---|---:|---:|
| `vin=0.25`, `gain=2.0`, `offset=0.1` | `acc=0.5`, `out=0.6` | `acc=0.5`, `out=0.6` |

## Functional Safety

| Question | Answer |
|---|---|
| Default backend changed? | no |
| Engine dispatch changed? | no |
| Event scheduling changed? | no |
| Transition semantics changed? | no |
| CSV/checker changed? | no |
| Speed claim enabled? | no |

## Claim Boundary

**可以说**：

- 094f partial 已经把真实 parsed Verilog-A expression 的一个可迁移子集接到 094e Rust body ABI。
- 094f partial 已经把 ordered scalar state assignment + single-node voltage contribution block 编码成 Rust body batch。
- encoder 对动态 indexed voltage read 保守 fallback。
- statement encoder 对 event body 保守 fallback，直到 event scheduler 拥有 ordering。
- 全量 EVAS pytest 通过，说明当前改动没有破坏默认生产路径。

**不能说**：

- 094f/g full Rust executor 已完成。
- event due/order/body、timer/cross scheduler、transition output、record trace 已经进入统一 Rust executor。
- generic executor 可以 default-on。
- 当前改动带来速度提升。

## Next Step

继续 094f/g：

1. 把 event body write-set lowering 接到 event due/order scheduler，而不是直接执行全 analog block。
2. 增加 event due/order scheduler 的 Rust-side batch ABI。
3. 做 real-row shadow parity：Rust executor 和 Python adaptive runtime 在同一 row 上输出一致 waveform。
4. 通过 real-row parity 后，再接 opt-in production dispatch。
