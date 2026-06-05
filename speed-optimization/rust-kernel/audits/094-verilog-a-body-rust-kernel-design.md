# 094 - Verilog-A Body → Rust Kernel: Project Design

Status: `planned` (design-only; multi-audit project, individual audits TBD)

Date: `2026-06-06`

Code commit: `n/a`（design doc, no code）

Related documents:

- `066-release-wide-rustification-workplan.md` (W2 General evaluate IR)
- `091-generic-event-state-transition-candidate-matcher.md`
- `091d-generic-executor-python-body.md` (where the body Python loop lives)
- `092-generic-executor-real-row-validation.md` (real-row data showing 33× geo-mean)

## One-Line Summary

Scope a new multi-audit project (estimated 8-12 individual audits, ~40-80 engineering hours) to lower the compiled Verilog-A model `evaluate()` body from Python interpreter into a Rust kernel. The goal: eliminate `model_evaluate_s` 47.78% of cmp_delay wall — the **final remaining bottleneck** after 091a-d removed engine orchestration. **This is design only; implementation is its own project.**

## Why This Project Exists

Recap of where the speed gains have come from in the 086-092 series:

| Audit | What it optimized | Real-row wall delta |
|---|---|---:|
| 086 transition buffer reuse | per-call Python alloc | +2.8% |
| 088 transition batch | per-step Python batch | +2.8% |
| 089 cross/above per-call production | per-call FFI replacement | **-198%** ❌ |
| 091a-d generic dispatcher + Python executor | bypass engine orchestration | **+1,000-10,000%** on simpler rows |

**The remaining ~50% of cmp_delay wall (and likely a larger fraction on heavier circuits) is `model.evaluate()` itself** — the Python code that EVAS's compiler emits from `.va` source. Lowering it to Rust is the **last meaningful 10× lever** for EVAS Rustification.

But it is also **the biggest engineering investment** in the entire series:
- Requires building a typed-array IR for the full Verilog-A surface (events + state + transitions + bus access + condition + expression)
- Requires a Rust executor that interprets or JITs this IR
- Requires lowering codegen from Python emit → IR emit
- Touches the entire compiler backend

Hence this design doc — to define scope, sequence, and stop points before any code is written.

## Goal Definition

| Dimension | In scope | Out of scope |
|---|---|---|
| Verilog-A semantics | Event-driven state machines + linear transitions + standard math operators + `$bound_step` | KCL/KVL transistor models; AC/DC analysis; `ddt/idt` integration; full nonlinear contributions; `I()<+` current contributions |
| Module structure | Single model, no hierarchical instances | Multi-instance hierarchies (091 series already excludes these) |
| Coverage target | ~100 unique 091b candidate sources (~70% of vabench-release-v1) | All 357 release rows (the 30% with $strobe/loops/advanced features stay Python) |
| Output | CSV bit-exact parity with current Python adaptive path | Approximate / fixed-grid output (091d already does that) |
| Speedup expectation | Push real-row wall from 091d's ~30ms to ~3ms (10× more) | Spectre AX timing parity (separate paper claim work) |

## Phase Breakdown

Decompose the project into 8-12 audits. Below is a proposed sequence; actual implementation can adjust gates as data emerges.

### Phase 1: IR Foundation (audits 094a-094d, ~3 weeks)

| Audit | Scope | Estimated hours |
|---|---|---:|
| 094a | Verilog-A Expression IR — typed tree representation of all expression nodes (BinaryExpr, UnaryExpr, TernaryExpr, FunctionCall, BranchAccess, identifiers) | 8-10 |
| 094b | Statement IR — if/else / for / while / case + assignments + contributions + event statements lowered to typed nodes | 8-10 |
| 094c | Event-driven Schedule IR — cross/above/timer/initial_step trigger expressions + body references | 6-8 |
| 094d | State and Parameter Binding — integer/real/array state with indexed slots; parameter constants folded | 4-6 |

**Gate to enter Phase 2**: Phase 1 produces an IR that 100% of 091b candidates can be lowered into without information loss. Validated by round-trip: IR → emit Python source → compare to original compiled model output.

### Phase 2: Rust Executor (audits 094e-094g, ~3 weeks)

| Audit | Scope | Estimated hours |
|---|---|---:|
| 094e | Rust typed-array runtime — `cdylib` with `evas_rust_evaluate_body_ir()` taking IR ops + state arrays + node arrays | 10-12 |
| 094f | Expression evaluator — Rust implementations of all expression node kinds, reading from typed arrays | 8-10 |
| 094g | Event scheduling — Rust manages cross/timer due detection over fixed grid + adaptive insertion via `next_breakpoint` mirror | 8-10 |

**Gate to enter Phase 3**: Phase 2 Rust executor passes shadow parity on the 5 vabench rows from audit 092 (bit-exact CSV vs Python adaptive). FFI cost amortized over per-step evaluation, not per-operator.

### Phase 3: Production Wiring + Coverage (audits 094h-094k, ~2 weeks)

| Audit | Scope | Estimated hours |
|---|---|---:|
| 094h | Engine dispatch — 091d-style `_try_*` that uses Rust IR executor instead of Python `model.evaluate()` | 4-6 |
| 094i | Sweep validation — run 094h on all ~100 091b candidates, measure wall + fallback rate | 2-4 |
| 094j | Defaultisation policy — based on parity + fallback data, decide whether to default-on | 1-2 |
| 094k | Documentation + audit cleanup + claim boundary update | 4-6 |

**Final claim allowed after Phase 3**: "On 091b-candidate rows (~70% of release), EVAS evaluate body runs in Rust with bit-exact CSV parity vs Python adaptive and ~X× wall reduction."

## Total Estimate

- **8-12 audits**, depending on whether some phases split
- **~40-80 engineering hours** total
- **~6-8 weeks calendar time** at 1-2 audits per week

## Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| IR cannot represent some Verilog-A construct (e.g., conditional contributions) → fallback rate > 50% | high | Phase 1 round-trip validation catches before Rust work; can narrow scope (drop unsupported constructs from candidate match) |
| Rust executor FFI cost > Python interpreter cost on small bodies (similar to 089) | medium | Pre-batch evaluation into per-step FFI (not per-operator); 091d data shows this is fine on simpler bodies |
| Bit-exact CSV parity unachievable due to float ordering | medium | Document tolerance band as part of claim; align with EVAS existing checker tolerance |
| Compiler changes break existing 9 specific candidates | high | Run all existing audit tests after each phase; preserve specific candidates as fallback when generic fails |
| Multi-instance / hierarchical model edge cases | low | Excluded from scope explicitly |

## What Already Exists And Can Be Reused

| Asset | Where | What it does | Phase that uses it |
|---|---|---|---|
| `transition_target_ir` (042-046) | backend.py | Lowers transition target value computation | Phase 1 (IR composition) |
| `evaluate_ir_static_linear_ops` (037) | backend.py | Static-linear expression IR | Phase 1 (sublanguage subset) |
| `evas_rust_transition_state_step` (050) | rust_core | Rust transition state evolution | Phase 2 (transition kernel) |
| `evas_rust_cross_detector_step` / `above_detector_step` (052) | rust_core | Rust cross/above detector math | Phase 2 (event detection) |
| `evas_rust_timer_*` (051) | rust_core | Rust timer primitives | Phase 2 |
| `_collect_generic_event_state_transition_candidate` (091b) | backend.py | Matcher that picks ~100 eligible models | Phase 3 dispatch gate |
| `_inspect_generic_event_state_transition_dispatch` (091c) | engine.py | Counter framework + gate validation | Phase 3 reuse |
| `_try_generic_event_state_transition_fastpath` (091d) | engine.py | Python fallback if Rust fails | Phase 3 fallback path |

This is **substantial existing infrastructure**. Phase 1 + 2 add the IR layer between (matcher metadata) and (Rust primitives) that's currently missing.

## What's NOT This Project

| Anti-scope | Why excluded |
|---|---|
| Per-operator FFI optimization | Already proven to be net negative (089 -198%) |
| 091e Rust-port of 091d's Python loop | Marginal gain; the loop is already fast at ~30ms |
| Verilog-A → LLVM IR (JIT compile) | Even more engineering; 094 is "interpret IR in Rust" which is simpler |
| Spectre AX equivalence claim | Separate paper-facing claim work, requires same-server timing |
| Default-on of 091d (without parity refinement) | Different decision tree; covered in audit 093 (next-next audit) |

## Lessons Learned That Shape This Design

From 086-092 series:
1. **Per-call FFI on hot-but-cheap functions = net loss** (089)
2. **Bypass orchestration loops = ~30× win on simpler rows** (091d/092)
3. **Synthetic ≠ real** — must test on vabench testbenches
4. **15-repeat trimmed mean** — 5-repeat hides outliers, distorted 088 wall claim
5. **Conservative matcher** — over-claiming candidates leads to high fallback rate
6. **Honest claim boundary section** in every audit — avoid silent overpromise

094 design incorporates all of these:
- IR + Rust executor avoids per-operator FFI by batching at per-step level
- Round-trip validation in Phase 1 catches IR incompleteness before Rust work
- Phase 2 gate requires bit-exact CSV parity on real rows (no synthetic-only claims)
- Conservative IR-eligible set; non-matching models fall back to Python (091d if their evaluate body is simple, default Python if complex)

## Decision Point — Should This Project Start?

**Arguments for**:
- ~50% of cmp_delay wall (model_evaluate_s) is the last big lever
- Existing primitive infrastructure (transition / cross / timer) is solid
- 091d real-row data validates the dispatch pattern (33× geo-mean with 0 fallback)
- Would unlock paper-facing speed claim (with same-server Spectre AX rerun)

**Arguments against**:
- ~40-80 engineering hours is a multi-week investment
- 091d already delivers 11-100× on real rows (opt-in) — the marginal user benefit of 094 is mostly the parity (bit-exact CSV) rather than additional speedup
- New audit series can be deferred indefinitely; 091d is shippable as opt-in today

**Recommended call**: Start 094 **only after** Phase 092-093 data shows:
1. 091d works on the full sweep without unacceptable fallback rate
2. Parity refinement (092's "Phase B") proves insufficient for default-on (otherwise 091d suffices)
3. There's user demand for default-on (parity-faithful) version

Until then, 094 stays in design phase. This document is the design checkpoint for that future decision.

## Next Step

This audit (094) is **design-only and stops here**. No code is written until the decision point above is met.

Concrete short-term next steps (separate from this project):

- Finish audit 093 sweep + parity refinement → make 091d default-on decision (see audit 093)
- If default-on policy is "stay opt-in", consider starting 094a (Phase 1 IR foundation)
- If default-on is "ready to flip", 094 becomes lower priority (091d covers the user need)
