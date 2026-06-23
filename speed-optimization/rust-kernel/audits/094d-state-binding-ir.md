# 094d - State And Parameter Binding IR

Status: `done` (binding metadata only; no Rust ABI yet)

Date: `2026-06-06`

Code commit: `pending`

Related documents:

- `094a-expression-ir.md`
- `094b-statement-ir.md`
- `094c-schedule-ir.md`
- `094-verilog-a-body-rust-kernel-design.md`

## One-Line Summary

扩展 `evas/simulator/expr_ir.py`，新增 `StateBindingIR` / `BindingTableIR`，把 Verilog-A source-level symbols 绑定到稳定 slot：parameter、port、scalar state、array state、special identifier。release vabench 的 **234 个 generic candidate** 中，expression IR 引用的 identifier 全部可解析到 binding table。该 audit 仍不改变生产仿真路径，速度收益为 **0%**。

## Why This Exists

Rust kernel 加速的核心不是“语法变 Rust”，而是把每步高频访问从 Python dict/string lookup 变成 typed array index：

```text
Python:
    self.state["q"]
    self.params["vth"]
    nv["CLK"]

Rust-ready binding:
    state_values[q_slot]
    param_values[vth_slot]
    node_values[clk_slot]
```

094a-c 已经能表示 expression、statement、event schedule。094d 把其中的名字绑定成稳定 slot，是进入 094e Rust ABI 前的最后一层基础 metadata。

## What Changed

新增：

| Type | Purpose |
|---|---|
| `StateBindingIR` | 单个 symbol 的 kind/slot/integer/array-range metadata |
| `BindingTableIR` | module-level binding table with `resolve(name)` |
| `build_state_binding_ir(module)` | 从 parser module 生成 parameter/port/state/special binding |
| `iter_identifier_names(expr_ir)` | 遍历 expression IR 中引用的 identifier |

Binding kinds:

| Kind | Meaning |
|---|---|
| `parameter` | Verilog-A parameter |
| `port` | module port name |
| `state_scalar` | scalar variable state |
| `state_array` | array variable state |
| `special` | `$abstime`, `$temperature`, `$vt`, `inf`, etc. |

## Validation

```bash
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_audit_094d_state_binding_ir.py -q
# 2 passed
```

Release sweep inside the test:

| Metric | Value |
|---|---:|
| `generic_event_state_transition_v1` candidate models | 234 |
| Checked identifier references | >= 7000 |
| Unresolved identifier references | 0 |

## Functional Safety

| Question | Answer |
|---|---|
| Default backend changed? | no |
| State storage changed? | no |
| Parameter evaluation changed? | no |
| Node voltage dict changed? | no |
| CSV/checker changed? | no |

## Claim Boundary

**可以说**：

- 094d 已经给 234 个 generic candidate 的 expression identifiers 建立可解析 binding。
- 后续 Rust ABI 可以基于这些 binding 设计 typed state/param/node arrays。

**不能说**：

- EVAS 已经移除 Python dict/object 状态同步。
- Rust executor 已经消费这些 bindings。
- state array / port / parameter 全部已 runtime array 化。
- 094d 带来任何速度提升。

## Next Step

进入 094e Rust ABI foundation：

1. 定义 compact encoded IR/op arrays。
2. 把 `BindingTableIR` 转成 state/param/node typed array layout。
3. 增加 `evas_rust_evaluate_body_ir` synthetic ABI。
4. 先做 Python-vs-Rust shadow parity，不直接 default-on。
