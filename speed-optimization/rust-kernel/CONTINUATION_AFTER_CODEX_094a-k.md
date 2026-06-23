# Continuation Doc — After Codex's 094a-k Session

**Audience**: next session (Codex or human) picking up the 094 project

**Author**: Claude (verification pass after Codex's first 094 session)

**Verified date**: 2026-06-06

---

## 1. Executive Summary

Codex completed Phase 1 + Phase 2 of the 094 project: **the IR foundation
and Rust ABI scaffolding are real and tested**. Phase 3 (production
integration via engine.py dispatch) has not started. Net wall delta
for end users is **0%** — no flag they can pass changes runtime
behavior through the new code path yet.

**Status by codex's own naming**:

- 094a-e: `done` ✅ (4 modules, Rust ABI, 100-IR parity)
- 094f-k: `partial` 🟡 (encoder/runtime fragments; shadow only)
- 094l onward: not started ❌ (engine.py untouched)

**Independent verification (this doc's contribution)**:

- ✅ All claimed tests pass on my machine (Rust 36/36, Python 094-targeted 63/63, full pytest 635/635, 0 regression vs 606 baseline)
- ✅ 4,322 lines of real code (2,074 Python + 1,275 Rust+wrappers + 973 tests) on the local working tree
- ❌ **0 commits, 0 pushes** — work survives only in your local clone
- ❌ engine.py untouched — production path still 091d Python
- ❌ Real-row waveform parity not validated (only synthetic + compile-only round-trip)

---

## 2. Critical Issues (Read These Before Anything Else)

### Issue A — Work-loss risk (severity: HIGH)

Codex's 4,322 lines exist as:
- `EVAS`: 3 modified files (`evas/rust_core/src/lib.rs`, `evas/simulator/rust_backend.py`, `tests/test_rust_backend.py`), 9 untracked files
- `behavioral-veriloga-eval`: 11 untracked audit docs + modified STAGE_2_4_EXECUTION_PLAN.md

**A `git reset --hard` or accidental `git clean -fd` deletes everything.**
A laptop crash before the next push event drops the work.

The handoff doc (HANDOFF_TO_CODEX_094_PROJECT.md) Rule 6 says "one
audit per commit + push". Codex did neither. Whether this was
deliberate (planning to bulk-commit at session end) or an oversight
is unclear, but the current state is fragile.

### Issue B — Production gap (severity: HIGH for the project goal)

The 094 project's stated goal is "lower Verilog-A body to Rust kernel
so users get default-on speedup with bit-exact CSV parity". The four
new Python modules + Rust ABI achieve **lowering and validation but
not dispatch**. Concretely:

```bash
$ cd EVAS && grep -nE "evaluate_body_ir|RustEventDueRuntime" evas/simulator/engine.py
(empty)
$ git diff --stat evas/simulator/engine.py
(empty)
```

Until `engine.py` learns to call the new Rust kernel, no user code path
exercises it. The opt-in flag matrix from worklist 20260606 is
unchanged in user-observable behavior:

| Flag | Behavior today | Behavior after codex's session |
|---|---|---|
| `generic_executor=True` | 091d Python executor (10-30× speedup) | same — codex did not modify the dispatcher |
| `rust_full_model_fastpath=True` | 9 specific candidate kinds (4.08×) | same |
| `rust_transition_production=True` | 086 buffer reuse + 088 batch (+2.8%) | same |
| New 094 path | n/a | **not reachable** |

### Issue C — Real-row parity gate not crossed (severity: MEDIUM)

Codex's 094f/g/h/i/j/k audits all explicitly say "real-row waveform
parity not validated" in their Claim Boundary. Their validation rests
on:
- 094a-d: compile-only round-trip (IR → Python emit → does it compile)
- 094e: 100 random synthetic IRs match Python interpretation
- 094f: stack-machine output for hand-crafted expressions matches expected float
- 094h: two-event same-step ordering produces expected `q` and `out` final values

None of these run a real vabench testbench (e.g., pipeline_stage,
sar_logic, debounce_latch from audit 092) through the Rust path
and compare CSV. The handoff's "round-trip parity on 5 vabench
rows" gate from Phase 2 acceptance has **not been demonstrated**.

This isn't a bug — it's an unmet acceptance criterion that the next
session must address before Phase 3 integration.

### Issue D — Codex's test count is slightly stale (severity: LOW)

Codex's STAGE_2_4 update says "51 passed". My run on the same files
shows 63 passed. The 12 extra are 094a/094b/094d tests that were
written but apparently not in codex's reported summary. Implication:
trust the live `pytest` count, not the writeup.

### Issue E — Phase 3 scope underestimated in the handoff doc (severity: MEDIUM)

The original handoff (HANDOFF_TO_CODEX_094_PROJECT.md) bundled "094h
engine dispatch + 094i sweep + 094j default-on + 094k docs" into a
single 4-6h Session N+5. Codex's actual experience renamed 094h-k
to fine-grained shadow runtime audits and pushed the **real engine
dispatch** to a notional 094l. This is honest re-scoping but means
the original 5-session plan understated work; expect **6-8 sessions
total**, not 5.

---

## 3. What Codex Actually Built (Verified)

### Python modules (all untracked, 2,074 lines)

| File | Lines | What it does |
|---|---:|---|
| `evas/simulator/expr_ir.py` | 866 | Typed dataclasses for all expression node kinds + `lower_expr()` / `emit_python()` / `encode_body_expr_ops()` |
| `evas/simulator/stmt_ir.py` | 523 | Statement IR + `BodyStmtProgram` / `encode_body_stmt_ops()` |
| `evas/simulator/schedule_ir.py` | 280 | Cross/timer/initial-step/final-step event encoding |
| `evas/simulator/event_due_runtime.py` | 405 | `RustEventDueRuntime`, `RustEventStatementRuntime`, `RustAnalogBlockEventRuntime` (shadow only) |

### Rust kernel extensions (modified, +1,275 lines)

| File | +Lines | What it does |
|---|---:|---|
| `evas/rust_core/src/lib.rs` | +752 | `evaluate_body_ir`, `evaluate_body_expr_batch`, body stack-machine ops |
| `evas/simulator/rust_backend.py` | +377 | Python wrapper `RustBackend.evaluate_body_ir()` + helpers |
| `tests/test_rust_backend.py` | +146 | ABI parity tests |

### Test files (all untracked, 973 lines, 63 tests)

| File | Tests | Audit |
|---|---:|---|
| `tests/test_audit_094a_expr_ir.py` | ~10 | 094a |
| `tests/test_audit_094b_stmt_schedule_ir.py` | ~8 | 094b/c |
| `tests/test_audit_094d_state_binding_ir.py` | ~6 | 094d |
| `tests/test_audit_094f_body_ir_encoder.py` | 4 | 094f |
| `tests/test_audit_094h_event_due_program.py` | 6 | 094g/h/i/j/k |
| Plus 094e tests folded into `test_rust_backend.py` | ~29 | 094e |

### Audit docs (all untracked, 11 files)

`094a-expression-ir.md`, `094b-statement-ir.md`, `094c-schedule-ir.md`,
`094d-state-binding-ir.md`, `094e-rust-abi.md`, `094f-body-ir-encoder.md`,
`094g-event-body-program.md`, `094h-event-due-program.md`,
`094i-mixed-event-due-runtime.md`, `094j-event-statement-shadow-dispatch.md`,
`094k-analog-block-event-shadow-dispatch.md`

Each has a clear Status + Claim Boundary + Next Step. 094a-e are
`done`. 094f-k are `partial` with explicit "still missing" tables.

### Stack-machine supported subset (from 094f audit)

| Verilog-A feature | Status |
|---|---|
| Numeric literals, scalar params, scalar state | ✅ supported |
| `V(node)` and `V(node1, node2)` (static) | ✅ supported |
| Unary `-`, `!`, binary arithmetic/compare/logic/bitwise | ✅ supported |
| Ternary `cond ? a : b` | ✅ supported |
| Math fns: `abs/sqrt/exp/ln/log/sin/cos/floor/ceil/min/max/pow` | ✅ supported |
| `V(bus[i])` dynamic indexed | ❌ fallback (needs bus offset ownership) |
| State arrays | ❌ fallback (no flattened element slots in binding table) |
| Branch current `I(...)` | ❌ fallback (out of EVAS voltage-domain scope) |
| Method calls | ❌ fallback (string side effects) |
| `transition()` / `cross()` inside scalar expr | ❌ fallback (must route to scheduler) |
| Event statements | ❌ fallback (scheduler not Rust-owned yet) |
| If / loop / case / system task in body | ❌ fallback (phase-order gate pending) |
| Differential contribution `V(a,b) <+ expr` | ❌ fallback (write ownership undefined) |

This is the **honest scope of what the Rust kernel currently
understands**. Anything outside falls back to Python — which is fine
for shadow but means many real rows will fall back when 094 finally
goes production.

---

## 4. Commit Strategy Recommendation

Three viable paths. **The current state is unsafe at any duration**;
pick one before doing more work.

### Option A — Bulk preservation commit (recommended for safety)

Trade-off: violates handoff Rule 6 (one audit per commit), but
preserves codex's work immediately.

```bash
# On EVAS
cd EVAS
git add evas/simulator/expr_ir.py evas/simulator/stmt_ir.py \
        evas/simulator/schedule_ir.py evas/simulator/event_due_runtime.py \
        tests/test_audit_094a_expr_ir.py tests/test_audit_094b_stmt_schedule_ir.py \
        tests/test_audit_094d_state_binding_ir.py tests/test_audit_094f_body_ir_encoder.py \
        tests/test_audit_094h_event_due_program.py \
        evas/rust_core/src/lib.rs evas/simulator/rust_backend.py tests/test_rust_backend.py
git commit -m "Codex 094a-k partial: IR foundation + Rust ABI + shadow runtimes

Bundled commit preserving codex's first 094-session work (~4,300 lines).
See behavioral-veriloga-eval commit for matching audit docs.

094a-e: done — IR + Rust ABI proven on synthetic + compile-only round-trip
094f-k: partial — encoders + shadow runtimes; engine dispatch pending

Tests: 635 passed (606 baseline + 29 new), Rust 36/36, 0 regression.
No production path changed (engine.py untouched). User-observable
behavior unchanged — all 094 work is metadata + shadow.

Per-audit splits would be cleaner but the working tree was at risk
of loss; preservation prioritized. Future audits should commit
per-audit per handoff Rule 6.
"
git push

# On behavioral-veriloga-eval
cd ../behavioral-veriloga-eval
git add speed-optimization/rust-kernel/audits/094a-expression-ir.md \
        speed-optimization/rust-kernel/audits/094b-statement-ir.md \
        speed-optimization/rust-kernel/audits/094c-schedule-ir.md \
        speed-optimization/rust-kernel/audits/094d-state-binding-ir.md \
        speed-optimization/rust-kernel/audits/094e-rust-abi.md \
        speed-optimization/rust-kernel/audits/094f-body-ir-encoder.md \
        speed-optimization/rust-kernel/audits/094g-event-body-program.md \
        speed-optimization/rust-kernel/audits/094h-event-due-program.md \
        speed-optimization/rust-kernel/audits/094i-mixed-event-due-runtime.md \
        speed-optimization/rust-kernel/audits/094j-event-statement-shadow-dispatch.md \
        speed-optimization/rust-kernel/audits/094k-analog-block-event-shadow-dispatch.md \
        speed-optimization/rust-kernel/STAGE_2_4_EXECUTION_PLAN.md
git commit -m "Record codex 094a-k audits + plan update"
git push
```

### Option B — Per-audit splits

Cleaner history but requires 11 commits + careful `git add -p` to
peel each audit's source changes from the bundled modifications.
Estimated 30-45 minutes of focused git work. Recommended if you
plan to bisect the 094 project later.

### Option C — Stash + defer

```bash
cd EVAS && git stash push -u -m "codex 094a-k WIP 2026-06-06"
cd ../behavioral-veriloga-eval && git stash push -u -m "codex 094 docs WIP"
```

Safer than nothing if you want a snapshot before deciding A vs B.
The stash entries are local-only — still lost if the disk dies, but
survive accidental `git reset --hard`.

**My recommendation: Option A.** The work is honest and complete-as-claimed; future audits can commit cleanly per-audit.

---

## 5. What The Next Session Must Do

Order matters here. Skipping the parity gate means production
dispatch lands without proof; skipping a Phase-3 task means
default-on can't flip.

### Session N+6 — Real-row Shadow Parity (THE missing gate)

The handoff's Phase 2 acceptance was "round-trip parity on 5 vabench
rows". This was not done. Codex deferred it to "094l shadow gate".
Do this first; everything after depends on it.

**Concrete steps**:
1. Pick `vbr1_l1_pipeline_adc_stage` (smallest of the 5 audit 092 rows)
2. Compile model with codex's IR lowering → run through Python emit path
3. Compare CSV vs the original `model.evaluate()` Python path bit-exact
4. If pass: try sar_logic_4b, debounce_latch, window_comparator,
   pipeline_adc_chain
5. Acceptance: ≥4/5 rows bit-exact (with documented tolerance for
   float last-bit)

**Estimated**: 3-5h

**Risk**: codex's 094f encoder rejects many constructs (state arrays,
dynamic bus, differential contributions). Some of the 5 rows may
not be encodable end-to-end. If so, the row goes on the "Phase 3
fallback list" rather than blocking progress.

### Session N+7 — Continuous Statement Phase Ordering

Current shadow runtimes (094i/j/k) handle event statements only.
A real `model.evaluate()` interleaves continuous contributions
(`V(out) <+ expr` outside any `@(...)`). Codex's audits explicitly
defer this.

**Concrete steps**:
1. Audit `094l-continuous-statement-phase-order.md`: design how to
   sequence continuous + event statements in source order
2. Extend `event_due_runtime.py` with a `RustAnalogBlockRuntime` (not
   just event runtime) that walks the analog block top-to-bottom
3. Tests: round-trip on a model that mixes `q = q+1` and `V(out) <+ q`

**Estimated**: 4-6h

**Risk**: phase ordering can break in subtle ways. Audit 055 warned
about B10/B18 interactions. Stay shadow-only until the test passes.

### Session N+8 — Engine.py Dispatch + Default-On Decision

Once parity + phase ordering are proven in shadow, wire the runtime
into the production path.

**Concrete steps**:
1. Modify `_try_generic_event_state_transition_fastpath` in
   `evas/simulator/engine.py`: try Rust dispatch first, fall back
   to 091d Python on encoder rejection
2. Re-run audit 093 sweep on all 53 candidates
3. Compare CSV bit-exact rate vs 091d sweep (post-095: 38/53 within 5%)
4. Decide default-on per handoff Rule 4 (need ≥95% bit-exact)
5. Audit `094m-engine-dispatch.md`, `094n-sweep-results.md`,
   `094o-default-on-decision.md`

**Estimated**: 4-6h

**Risk**: Rust dispatch may be slower than 091d Python on small rows
(FFI cost amortization gate). Per Rule 1, if Rust dispatch is
slower, the candidate row should fall back to 091d, not Python.

### Session N+9 (optional) — Outlier Recovery

The 5 audit-093 outliers (PGA, precision rectifier, ramp_or_step,
PFD, peak detector) may now work if the Rust path handles their
specific patterns. Run them; if not, document a single "outlier
fallback list" audit.

**Estimated**: 2-3h

---

## 6. Numbers To Anchor The Next Session

These are the data points the next agent should preserve and compare against:

| Metric | Current value | Target after 094 done |
|---|---|---|
| 53-row sweep wall geomean | 14.4× (091d, audit 093) | ≥30× (Rust kernel) |
| 53-row sweep bit-exact (<1% CSV) | 21/53 (40%) | ≥50/53 (94%) |
| 53-row sweep <5% CSV | 38/53 (72%) | ≥51/53 (96%) |
| Runtime fallbacks | 0/53 | 0/53 |
| Full pytest pass count | 635 | ≥635 |
| 094 audits pushed | 0 | 11+ |
| engine.py modifications | 0 | yes |

If pytest count drops below 635 after a session, something broke.

---

## 7. Memories To Encode (Read Before You Start)

The original handoff (HANDOFF_TO_CODEX_094_PROJECT.md section 11) listed
memories to encode. Add these from codex's session:

- **Stack-machine ABI design**: codex chose a stack-machine
  (`BodyExprOp[]` with READ/PUSH/BINOP semantics) for the Rust body
  executor. This is well-suited for the lowered IR and worth keeping.
- **Three-layer runtime hierarchy**: `RustEventDueRuntime` (single
  trigger batch) → `RustEventStatementRuntime` (one event statement)
  → `RustAnalogBlockEventRuntime` (multiple statements in source
  order). The next layer needed is `RustAnalogBlockRuntime` covering
  continuous + event.
- **Encoder rejection is OK**: the conservative fallback list in 094f
  is large and that's the right design. Don't try to encode every
  construct; let unsupported rows fall back to 091d Python.
- **Codex's plan-doc updates are reliable evidence but not gospel**:
  test counts in writeups can lag actual test runs by a few tests.
  Run `pytest` to confirm.

---

## 8. Decision Points For The Human

You (the user) will face these questions across the next 3-4 sessions:

1. **After Session N+6 (parity gate)**: if 4/5 rows pass, proceed to
   N+7; if fewer, decide whether to narrow the candidate scope or
   extend the IR.
2. **After Session N+8 (sweep)**: bit-exact rate determines
   default-on. If ≥95%, flip; if not, document opt-in.
3. **After Session N+9 (or earlier)**: paper claim. Run the
   Spectre rerun (`runners/run_audit_098_same_server_spectre_rerun.py`)
   on thu-sui; this is the last milestone before write-up.

The 5 outlier rows can be either fixed in 094 or accepted as known
limitations; don't let them block the 080-90% wins.

---

## 9. Quick-Start For The Next Session

```bash
# 1. Confirm everything is committed (Option A from §4) before touching anything
cd EVAS && git status
cd ../behavioral-veriloga-eval && git status

# 2. Run baseline pytest to confirm 635+
cd EVAS && PYTHONPATH=. python3 -m pytest tests/ -q

# 3. Read this doc top to bottom

# 4. Read the partial-status audits to understand exactly what's done:
ls behavioral-veriloga-eval/speed-optimization/rust-kernel/audits/094*-*.md

# 5. Start Session N+6 (real-row parity gate):
#    - Pick vbr1_l1_pipeline_adc_stage as the smallest of the 5 audit 092 rows
#    - Use prototypes/audit_092_real_bench.py as the wall+parity harness
#    - Add an --emit-via-094-ir flag that runs through codex's encoder
#    - Compare CSV bit-exact vs Python evaluate

# 6. Commit per-audit, push immediately. Don't bundle.
```

Good luck.

---

## 10. Late Empirical Finding (Added After Initial Audit)

After writing §1-9 I ran a direct probe on the 5 audit-092 testbench
rows to measure how close codex's IR is to handling real circuits.

### 10.1 Lowering coverage on real rows

```python
from evas.simulator.expr_ir import build_state_binding_ir
from evas.simulator.stmt_ir import StatementLoweringContext, lower_stmt
for row in [pipeline_stage, sar_logic_4b, debounce_latch,
            window_comparator, pipeline_adc_chain]:
    mod = parse(row.va)
    binding = build_state_binding_ir(mod)
    ctx = StatementLoweringContext()
    for stmt in mod.analog_block.body.statements:
        ir = lower_stmt(stmt, ctx)   # returns IR or None
```

**Result**: 37/37 top-level analog block statements lowered (100%) on
all 5 rows. No exceptions, no None returns at the statement level.

| Row | Statements lowered | Outcome |
|---|---:|---|
| pipeline_stage | 6/6 | ✅ |
| sar_logic_4b | 7/7 | ✅ |
| debounce_latch | 6/6 | ✅ |
| window_comparator | 6/6 | ✅ |
| pipeline_adc_chain | 12/12 | ✅ |

This is **better than I had assumed in §2 Issue C**. The IR
foundation actually handles all 5 real-row analog block shapes.

### 10.2 What 100% lowering does NOT mean

Crucially:
- ✅ IR can REPRESENT every statement (lowering succeeds)
- ❌ Not tested: does `emit_python(ir)` produce code that runs and
  matches the original model.evaluate() waveform? (codex's own audits
  say compile-only round-trip is checked, not runtime parity)
- ❌ Not tested: does `encode_body_*_ops(ir)` accept these statements
  without falling back to "encoder rejection" (which 094f lists as a
  large category)?
- ❌ engine.py still untouched — no dispatch path exposes this IR to
  a real sim.run() call

### 10.3 Revised time estimate

Given 100% lowering coverage, the project is closer to default-on
than §2 Issue C implied. Revised path:

| Task | Original estimate | Revised estimate |
|---|---:|---:|
| Real-row waveform round-trip (§5 N+6) | 3-5h | **2-3h** (IR already handles all 5 rows; just need emit+run parity test) |
| Continuous statement phase ordering (N+7) | 4-6h | **3-4h** (the codex schedule_ir already encodes the structure) |
| engine.py dispatch + sweep + default-on (N+8) | 4-6h | **3-4h** (091d's `_try_*` is a clean insertion point) |

**Total to actual user-visible effect: 8-11h** instead of the original 12-19h.

### 10.4 Implication for the next session

If you have one focused codex session, the highest-leverage move is:
1. Skip writing a separate parity audit doc — just run emit→compile→sim
   on pipeline_stage as a smoke test, see if it produces a CSV
2. Compare CSV vs Python adaptive
3. If close (≤1% diff): write the engine.py wire in the same session
4. If far (>1% diff): investigate which constructs lose fidelity; that
   becomes the parity gate audit

The 100% lowering result is real evidence that codex's Phase 1+2 work
is structurally sound. Don't rebuild what's already there.
