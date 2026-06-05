# Stage 2-4 Execution Plan (094 Project) — Detailed Per-Session Checklist

**Status**: planning — not started

**Author**: Claude Opus (session 2026-06-06)

This document tracks the multi-week 094 project from the original
multi-stage plan. Stages 1 and 6 are complete (see audit 095 and the
EVAS commit `2c754c7`). This document is what a future Claude (or
human) needs to pick up Stage 2-4.

## Session-by-Session Breakdown

### Session N+1: 094a Expression IR Module

**Deliverables**:
- New file `EVAS/evas/simulator/expr_ir.py`:
  - Typed dataclasses: `ExprIR`, `BinaryExprIR`, `UnaryExprIR`,
    `TernaryExprIR`, `FunctionCallIR`, `BranchAccessIR`,
    `IdentifierIR`, `LiteralIR`
  - Function `lower_expr(ast_expr, context) -> ExprIR | None`
  - Function `emit_python(ir) -> str` for round-trip validation
- New file `EVAS/tests/test_audit_094a_expr_ir.py`:
  - Test: round-trip lowering + emission produces equivalent Python source
  - Test: 091b candidates' analog body expressions all lower successfully
  - Test: unsupported constructs (e.g., function calls not in math whitelist) return None
- Audit `094a-expression-ir.md`

**Acceptance**:
- ≥234 091b candidates' analog block expressions 100% lower
- Round-trip emission produces Python code that compiles + runs

**Risk**: AST visitor may miss edge cases (nested ternary in array index, etc.)

**Estimated**: 4-6 hours

---

### Session N+2: 094b Statement IR + 094c Event Schedule IR + 094d State Binding

**Deliverables**:
- New file `EVAS/evas/simulator/stmt_ir.py`:
  - `AssignmentIR`, `IfStmtIR`, `BlockIR`, `EventBodyIR`
  - `lower_stmt(ast_stmt, ctx)` for the if/else state machine subset
- New file `EVAS/evas/simulator/schedule_ir.py`:
  - `CrossEventIR`, `TimerEventIR`, `InitialStepIR`
  - Encodes trigger expression + body reference
- Extend `EVAS/evas/simulator/expr_ir.py`:
  - `StateBindingIR` — maps Verilog-A state names to indexed slots
- Tests:
  - 091b candidates' event bodies all lower successfully
  - Round-trip: lower → emit → compile → run produces same waveform as original
- Audit `094b-statement-ir.md`, `094c-schedule-ir.md`, `094d-state-binding.md`

**Acceptance**: round-trip parity on 5 vabench rows from audit 092

**Estimated**: 6-8 hours

---

### Session N+3: 094e Rust ABI Foundation

**Deliverables**:
- Extend `EVAS/evas/rust_core/src/lib.rs`:
  - `pub fn evaluate_body_ir(...)` — takes IR ops (encoded as typed
    arrays) + state arrays + node arrays + time
  - C ABI `evas_rust_evaluate_body_ir`
  - Internal: dispatch op kinds to expression/statement handlers
- Extend `EVAS/evas/simulator/rust_backend.py`:
  - Python wrapper `RustBackend.evaluate_body_ir(ir, state, nodes, time)`
- Tests:
  - Run synthetic IR (add, compare, write state) through Rust, verify
    matches Python interpretation
- Audit `094e-rust-abi.md`

**Acceptance**: 100 random IRs produce identical state writes in Python vs Rust

**Estimated**: 6-8 hours

---

### Session N+4: 094f Expression Evaluator + 094g Event Scheduling

**Deliverables**:
- Extend Rust core: full expression evaluator covering all ExprIR kinds
- Add cross/timer event scheduling in Rust:
  - `evas_rust_event_scheduler` finds the next event time across
    multiple cross/timer triggers
  - Returns `(event_time, event_body_index)` to caller
- Python wrapper coordinates: feed IR → Rust evaluator → handle event
  body via Rust → record outputs
- Tests:
  - Shadow parity: Rust executor result == Python executor result
    on the 5 audit 092 rows (bit-exact CSV)
- Audit `094f-expression-evaluator.md`, `094g-event-scheduling.md`

**Acceptance**: shadow parity bit-exact on 5 rows

**Estimated**: 8-10 hours

---

### Session N+5: 094h-094k Integration + Sweep + Default-On

**Deliverables**:
- Replace 091d's Python `_try_generic_event_state_transition_fastpath`
  body with: build IR + dispatch via Rust executor
- 091d Python implementation stays as fallback (Rust failure → Python)
- Sweep on all 53 candidates with new Rust executor
- Compare wall + parity vs 091d Python executor + Python adaptive
- Decision: flip default-on if (a) ≥90% rows bit-exact (b) wall ≥2× over 091d
- Audit `094h-engine-dispatch.md`, `094i-sweep.md`, `094j-default-on.md`,
  `094k-claim-update.md`

**Acceptance**:
- Sweep 0 fallback
- ≥90% rows bit-exact vs Python adaptive
- Wall 2-10× over 091d Python (50-300× over Python adaptive)
- Default-on flipped OR documented opt-in with reasons

**Estimated**: 4-6 hours

---

## Total Estimate

- 5 sessions × 4-10 hours = 20-50 engineering hours
- ~3-5 weeks calendar time at 1-2 sessions per week
- 8-12 individual audit docs

## Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| IR cannot represent some Verilog-A pattern in 091b candidates | medium | high | Round-trip test in Session N+1; if >5% fail, narrow candidate scope |
| Rust expression evaluator has float precision drift vs Python | medium | medium | Shadow parity test in Session N+4 catches early; document tolerance |
| Engine dispatch integration breaks existing 9 specific candidates | low | high | Run all tests after each session; keep specifics as fallback |
| Multi-instance / hierarchy edge case | low | low | Explicitly excluded from scope (091b matcher rejects these) |

## What This Plan Does NOT Cover

- $strobe / $display / $random side effects (091b matcher excludes models with these)
- KCL/KVL transistor models (out of EVAS scope entirely)
- AC/DC analysis (out of scope)
- Multi-instance hierarchies (091b matcher excludes)
- Paper-facing speed claim (covered by Stage 5 / audit 098 runner)

## Picking Back Up

When ready to start Session N+1:

```bash
# 1. Confirm baseline is still clean
cd EVAS && PYTHONPATH=. python3 -m pytest tests/ -q   # should be 606+ pass

# 2. Read the 094 design audit
cat behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094-verilog-a-body-rust-kernel-design.md

# 3. Read the 091b matcher to understand what AST shapes are in scope
grep -n "_collect_generic_event_state_transition_candidate" EVAS/evas/simulator/backend.py

# 4. Start 094a — build expr_ir.py
```

Each session should produce a self-contained audit + tests + commit
+ push, like the 086-095 cadence in the prior series. Don't bundle
multiple sessions' work into one commit (see commit 2c754c7 on EVAS
for an example of bundling that lost commit-message accuracy).
