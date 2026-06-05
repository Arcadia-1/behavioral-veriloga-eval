# Handoff to Codex — Audit 094 Project (Verilog-A Body → Rust Kernel)

**Project**: complete the 094 multi-audit series that lowers Verilog-A
`model.evaluate()` body from Python interpreter to Rust kernel, enabling
default-on of generic-executor speedup (currently 10× geomean opt-in,
bit-exact parity blocked).

**Estimated total work**: 20-50 engineering hours across ~5 sessions.

**Author of this handoff**: Claude (session 2026-06-06). All facts here
are from real execution data committed to GitHub in the audit chain
086-095.

---

## 1. Executive Summary (read this first)

The 086-095 audit series proved:

- **Per-call FFI on hot-but-cheap functions is a net loss.** 089 made
  `cmp_delay` 3× *slower*. Don't repeat this mistake.
- **Bypassing Python orchestration loops wins.** 091d (Python executor
  that skips engine adaptive stepper) delivered 10-30× real-row
  speedup with 0 fallback.
- **Bit-exact CSV parity remains blocked** by 091d's fixed-grid
  sampling vs Python's adaptive cross/transition interpolation. Audit
  095 closed 38/53 rows to <5% CSV diff but 5 outliers remain at
  >50% diff.

The 094 project is the path to bit-exact parity + default-on of the
generic executor. It builds a typed-array IR for Verilog-A body,
ports it to a Rust kernel cdylib, and integrates via the existing
dispatcher infrastructure (which 091b/c/d already wired up).

After 094 lands, default users (no flags) should see 10-50× real-row
speedup with bit-exact CSV.

---

## 2. Required Reading (in this order)

| Order | Audit | Why |
|---|---|---|
| 1 | `094-verilog-a-body-rust-kernel-design.md` | Original project design — 8-12 audits across 3 phases |
| 2 | `STAGE_2_4_EXECUTION_PLAN.md` | Session-by-session checklist with acceptance gates |
| 3 | `093-generic-executor-sweep-and-default-on-decision.md` | Why default-on couldn't be flipped + parity status |
| 4 | `095-generic-executor-record-adaptive-substeps.md` | Most recent parity work — what's still broken |
| 5 | `091-generic-event-state-transition-candidate-matcher.md` | What models match the candidate (234/357 release rows) |
| 6 | `091d-generic-executor-python-body.md` | The Python executor you're replacing |
| 7 | `066-release-wide-rustification-workplan.md` | Original W2/W3 workstream context |
| 8 | `STAGE6_BUNDLED_COMMIT_NOTE.md` | Why EVAS commit 2c754c7 is 27k lines (not 095 alone) |

Skim audits 086-093 in chronological order if you need the full
lessons-learned context. Each has a "Claim Boundary" section that
shows what was honest vs over-promised.

---

## 3. Critical Rules (hard-won lessons — do NOT violate)

### Rule 1: Never add per-call FFI on hot-but-cheap functions

Audit 089 (cross/above per-call production) made simulation 3× slower
because the Rust function (CrossDetector.check ≈ 5μs in Python)
couldn't beat the per-call FFI overhead (~25μs ctypes marshalling).
**931,440 cross checks paid 23s of FFI to save 5s of math.**

If your Rust function is called per-step inside a hot loop, batch it.
If it's called once per simulation, FFI cost is amortized.

### Rule 2: Use 15-repeat trimmed mean for any wall claim

Audit 088 initially reported 1.24× speedup on cmp_delay from a 5-repeat
median; later 15-repeat trimmed mean showed it was 1.029×. A single
macOS scheduling outlier (36.58s) in the 5-repeat sample skewed the
median by 4×.

`prototypes/audit_092_real_bench.py` shows the pattern: 15 repeats,
drop top/bottom 2, report trimmed mean + stdev.

### Rule 3: Synthetic bench ≠ real bench

091d showed 507× on synthetic gen_exec_sample but only 33× on
pipeline_stage (5-row sample) and 14.4× on 53-row sweep. **Real
circuits have heavier `model.evaluate()` body, so absolute speedup
shrinks as circuit complexity grows.**

Always validate on at least one real vabench testbench before
claiming a number.

### Rule 4: Default backend must NOT change without bit-exact parity proof

The 091d 14.4× speedup is opt-in via `generic_executor=True` because
CSV size differs from Python adaptive on every row. Even though
voltage values at common timestamps match, the CSV row count differs
→ downstream checker tolerance is unknown → could silently regress
users.

**Do not flip a default-on switch until ≥95% sweep rows are
bit-exact, or document the specific tolerance band that all
downstream consumers accept.**

### Rule 5: Spectre runs MUST go through thu-sui → thu-wei wrapper

Direct calls to thu-wei hit the Cadence license queue and pollute
wall-time measurements. See r15 incident in
`plans/VAEVAS_SPEED_LIMITATION_ANALYSIS_2026-06-01.md`.

`runners/run_audit_098_same_server_spectre_rerun.py` has a hostname
check that refuses to run elsewhere. **Do not bypass it.**

### Rule 6: Commit hygiene — never use `git commit -am` on EVAS

EVAS has accumulating working-tree changes that should be committed
per-audit. `git commit -am` sweeps all modified files, which lost
commit-message attribution in commit `2c754c7` (27k lines bundled
under audit 095's title).

Use `git add <specific files>` then `git commit`. One audit per
commit. Don't bundle.

### Rule 7: Honest claim boundary in every audit

Every audit must have a `## Claim Boundary` section listing
- "可以说" (allowed claims) — what the data supports
- "不能说" (forbidden claims) — what the data does NOT support

If you can't honestly fill out both, the audit isn't done.

---

## 4. Infrastructure You Should Reuse (Don't Reinvent)

| Asset | Where | What it does | Use it for |
|---|---|---|---|
| `evas/simulator/evaluate_ir.py` | EVAS | Existing IR: LinearTermIR, LinearOpIR, TransitionTargetIR, ConditionIR (457 lines) | **Extend, don't replace** — this already covers static-linear + transition target + conditional |
| `_collect_generic_event_state_transition_candidate` | EVAS backend.py | Matcher that picks 234/357 release models | Your candidate gate (don't rebuild) |
| `_try_generic_event_state_transition_fastpath` | EVAS engine.py | Python executor (091d) | Your fallback path when Rust IR fails |
| `evas_rust_transition_state_step` (audit 050) | EVAS rust_core | Rust transition state evolution | Reuse for transition output evaluation |
| `evas_rust_cross_detector_step` (audit 052) | EVAS rust_core | Rust cross/above detector math | Reuse for cross event scheduling |
| `evas_rust_timer_*` (audit 051) | EVAS rust_core | Rust timer primitives | Reuse for timer event scheduling |
| `evas_rust_evaluate_static_linear` (audit 037) | EVAS rust_core | Rust static-linear evaluate | Reuse for continuous evaluate body |
| `prototypes/audit_092_real_bench.py` | EVAS | 15-repeat trimmed-mean bench template | Copy for new audits |
| `prototypes/audit_093_sweep.py` | EVAS | Full-sweep bench across all candidates | Copy and adapt |

**Critical insight**: the existing `evaluate_ir.py` already covers
**most** of the language your 094a (Expression IR) needs to handle.
The gap is the **event-body** if/else state machine — that's the
real new code. Don't waste time rebuilding what's already there.

---

## 5. Execution Plan (5 sessions)

See `STAGE_2_4_EXECUTION_PLAN.md` for full details. Summary:

| Session | Audit | Code change | Acceptance | Estimated |
|---|---|---|---|---|
| N+1 | 094a Expression IR | New `expr_ir.py` + tests | ≥234 candidates' expressions round-trip cleanly | 4-6h |
| N+2 | 094b/c/d Statement + Schedule + State IR | New `stmt_ir.py`, `schedule_ir.py`, extend `expr_ir.py` | Round-trip parity on 5 vabench rows | 6-8h |
| N+3 | 094e Rust ABI Foundation | Extend `rust_core/src/lib.rs` with `evaluate_body_ir` | 100 random IRs match Python interpretation | 6-8h |
| N+4 | 094f/g Full Rust Executor | Complete expression evaluator + event scheduling in Rust | Shadow parity bit-exact on 5 audit-092 rows | 8-10h |
| N+5 | 094h-k Integration + Sweep + Decision | Wire Rust executor into 091d dispatcher | Full sweep ≥90% bit-exact; default-on decision | 4-6h |

Each session: read the previous audits, write the code, run tests,
write the audit, commit (per file, not `-am`), push. One audit per
commit per push.

---

## 6. Common Pitfalls (specific things that will trip you)

### Pitfall A: AST visitor edge cases

Verilog-A AST has nested constructs that bite:
- TernaryExpr inside ArrayAccess inside FunctionCall args
- Conditional contributions (which 091b explicitly rejects, but you may forget)
- `default_transition` preprocessor effect on rise/fall when arg is 0

**Solution**: write the round-trip test FIRST. Lower → emit Python →
compare to original compiled model output. If the test fails, the
IR is incomplete. Don't proceed to Rust work until 100% of
candidates pass round-trip.

### Pitfall B: Float precision in Rust vs Python

Python's float math may produce slightly different last-bit results
than Rust's. CSV "bit-exact parity" really means **within float
precision**. Document the tolerance band you achieve (typically
~1e-12 abs / 1e-9 rel).

### Pitfall C: `next_breakpoint()` returning the wrong time

Phase B of audit 095 found that some models' `next_breakpoint()`
returns transition completion times (good) but not cross-event
times (bad). Your Rust event scheduler will need to compute cross
times directly from source values, not just call `next_breakpoint`.

### Pitfall D: Multi-instance models silently match

091b matcher rejects multi-instance models, but if 094 IR doesn't
also reject them, you'll get cryptic errors. Add an explicit gate
at the top of the 094 dispatcher: `if model._child_models: return None`.

### Pitfall E: 26k-line bundled commit

See Rule 6. Use `git add <specific files>` always. The EVAS working
tree should NOT accumulate uncommitted changes across audits —
commit each audit individually.

---

## 7. Testing and Validation Pattern

Every audit should have:

1. **Unit tests** for the new IR / executor in `EVAS/tests/test_audit_094XYZ.py`
2. **Round-trip test** that lowers → emits Python → compiles → runs → matches
3. **Shadow parity test** (when Rust is involved) — run both Python and Rust,
   compare results bit-exact
4. **Bench script** in `EVAS/prototypes/audit_094XYZ_bench.py` — 15 repeats,
   trimmed mean, real vabench testbench
5. **Sweep validation** in N+5 — run all 53 candidates with new Rust executor

Run after every code change:
```bash
cd EVAS
PYTHONPATH=. python3 -m pytest tests/ -q   # baseline + new tests
PYTHONPATH=. python3 prototypes/audit_094XYZ_bench.py   # wall data
```

If pytest count is < 606 + your new tests, you've broken something.

---

## 8. Commit and Push Protocol

For each audit:

```bash
# 1. Write code + tests
# 2. Verify all tests pass
cd EVAS && PYTHONPATH=. python3 -m pytest tests/ -q

# 3. Stage SPECIFIC files (not -am!)
git add evas/simulator/expr_ir.py tests/test_audit_094a_expr_ir.py prototypes/audit_094a_bench.py

# 4. Commit with audit-specific message
git commit -m "Audit 094a: Verilog-A Expression IR module

[detailed description matching audit doc]

Co-Authored-By: Claude/Codex ...
"

# 5. Push
git push

# 6. Cross-repo: commit the audit markdown
cd ../behavioral-veriloga-eval
git add speed-optimization/rust-kernel/audits/094a-expression-ir.md
git commit -m "Record audit 094a..."
git push
```

One audit → one EVAS commit + one behavioral-veriloga-eval commit.
Never bundle multiple audits.

---

## 9. When to Stop and Ask the Human

Stop and ask if:

- Round-trip parity fails on >5% of candidates → IR may be incomplete
- Shadow parity (Rust vs Python) drifts beyond 1e-9 → numerical issue
- A new edge case in Verilog-A AST appears that's not in any test
- The default-on decision (audit 094j) data is ambiguous
- You hit a Verilog-A semantic that's not in audit 094's scope (KCL/KVL, AC/DC, transistor, multi-instance)

Don't push code that you're not confident about. Don't claim a number
the data doesn't support. Don't flip default-on without ≥95% bit-exact
sweep results.

---

## 10. End State (when the project is done)

You'll know 094 is complete when:

1. Audits 094a through 094k are all committed and pushed
2. Sweep over 53 candidates shows ≥90% bit-exact CSV parity
3. Wall speedup ≥2× over 091d (i.e., 20-100× over default Python)
4. Default-on flag is flipped OR documented as opt-in with specific
   reasons (e.g., the 5 outlier rows from audit 095)
5. Audit 094k updates `MANIFEST.md` with the new claim boundary

After 094, the remaining work in the original plan is:
- **Stage 5 (audit 098)**: paper-facing Spectre AX rerun via
  `runners/run_audit_098_same_server_spectre_rerun.py` on thu-sui
- **Stage 6 (commit hygiene)**: already done (commit 2c754c7 bundled
  it)

---

## 11. Memories You Should Encode

If you run multiple sessions, persist these facts in your memory
system (or wherever):

- **EVAS persistent worker default-on policy**: user accepts speed >
  isolation risk; fix leakage bugs as they appear, don't revert
- **Spectre license routing**: always thu-sui → thu-wei; never direct
- **Bundled commit precedent**: commit 2c754c7 contains 27k lines
  beyond audit 095 — don't conflate
- **091b matcher excludes**: `$strobe / $display / $write`, for/while
  in event body, array assignments, multi-instance models
- **Existing IR infrastructure**: `evaluate_ir.py` already covers
  static-linear + transition target + conditional. Extend, don't
  replace

---

## 12. Contact / Provenance

This handoff was written by Claude (Opus 4.7, 1M context) in a
session ending 2026-06-06 after the 086-095 audit series. The
original directive was "complete stages 1-6"; stages 1, 5 (script),
6 were completed in that session, stages 2-4 were honestly scoped
out as multi-week and handed off in this document.

Key data points the next agent should preserve:

- 53 candidates, geomean wall speedup 10.3× (post-095)
- 21/53 rows <1% CSV diff, 38/53 <5%, 5 outliers >50%
- 0 fallback across all 53 (dispatcher is structurally sound)
- 606 baseline pytest + 7 audit-091b + 6 audit-091d + 4 audit-091c
  + 6 audit-089 + 15 audit-088 = ~644 tests (all pass)

If counts drift, run pytest to confirm the new baseline.

Good luck.
