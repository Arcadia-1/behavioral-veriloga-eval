# 048 - Python-To-Rust Behavior Map

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_fixed_array_topwall10_20260604.json`
- `speed-optimization/reports/current_fourway_topwall10_clean_20260604.json`

## One-Line Summary

停止继续做零散 Rust 前置补丁，先把 EVAS Python 内核中的仿真行为完整映射成 Rust primitive / IR / fallback / parity gate。

## Direction Reset

前面 037-046 证明了一件事：只扩大 static-linear IR 覆盖不等于真实速度提升。真实 top-wall 慢点仍集中在 `transition()`、event/cross/timer、dynamic state/bus、Python dict sync 和 output/record 路径；小 Rust segment 还会被 FFI 和 Python 同步开销反向拖慢。

从 048 开始，后续不再按“又支持一个小语法”推进，而是按下面的行为映射表推进：

```text
Python generated/runtime behavior
    -> Rust primitive / IR op
    -> typed array state boundary
    -> shadow parity gate
    -> production execution gate
    -> same-slice benchmark validation
```

## Non-Goals

- 不把 EVAS 扩展成 SPICE/KCL/KVL 求解器。
- 不用 Rust 重写 unsupported analog operators，例如 `I(...) <+`、`ddt()`、`idt()`、AC/DC analysis。
- 不把 synthetic microbenchmark 当成 paper-facing speed claim。
- 不再为了 coverage 单独补小语法，除非它服务于下面的完整行为 primitive。

## Behavior Inventory

| ID | Python behavior | Current code anchor | Rust primitive target | Priority | Fallback rule |
|---|---|---|---|---:|---|
| B01 | Numeric expression evaluation: constants, parameters, unary/binary ops, ternary, math | `backend.py::_compile_expr`, `_compile_function_call` | `ExprOp` DAG or linear/nonlinear expression bytecode | P1 | unsupported function or string/object expression |
| B02 | Voltage branch read: `V(node)`, `V(a,b)`, dynamic bus `V(bus[i])` | `backend.py::_get_voltage`, `_compile_node_voltage` | node-id read, differential read, base+offset bus read | P1 | event-interpolation read or unresolved dynamic hierarchy |
| B03 | Scalar and integer state read/write | generated `evaluate()`, `evaluate_ir.py::StaticLinearOp` | state-id read/write with integer coercion | P1 | string state, object state, unsupported side effects |
| B04 | State array read/write | `backend.py::_array_get`, `_array_set` | array base + fixed/dynamic index state read/write | P1 | out-of-bounds behavior mismatch or unknown dynamic range |
| B05 | Control flow: `if/else`, static `for`, dynamic `for`, `case` | `backend.py::_compile_statement`, `_compile_for`, `_compile_case` | basic-block control-flow IR with branch predicates | P1 | loop bound not provable and no bounded runtime loop primitive |
| B06 | Voltage contribution: `V(out) <+ expr`, differential contribution | `backend.py::_compile_contribution`, `_set_output` | output node-id write op, differential write op | P1 | current contribution, dynamic branch target without node-id lowering |
| B07 | `transition()` target expression and parameters | `backend.py::_transition_target_ir_op_from_contribution`, `evaluate_ir.py::TransitionTargetOp` | transition target batch: target/delay/rise/fall arrays | P1 | target expression has unsupported event/state dependency |
| B08 | `transition()` state evolution and interruption semantics | `engine.py::TransitionState`, `backend.py::_transition` | transition-state update kernel: evaluate old ramp, set target, active flag, next breakpoint | P1 | semantic mismatch with interrupted transition or default-transition edge case |
| B09 | `@(cross(...))` / `@(above(...))` trigger detection | `engine.py::CrossDetector`, `AboveDetector`, `backend.py::_check_cross`, `_check_above` | event detector array kernel with previous/current values and interpolated crossing time | P1 | event body needs Python-only side effect |
| B10 | Event body execution: initial/final/cross/timer body assignments | `backend.py::_compile_event_statement`, `_compile_post_update_event_statement` | event body basic-block IR; scheduled after trigger resolution | P1 | strobe/file IO/random or unlowered dynamic control flow |
| B11 | Timer event due/reschedule and timer breakpoint scan | `backend.py::_check_timer*`, `_next_timer_breakpoint` | timer array kernel: due flags, reschedule, absolute/periodic breakpoint | P1 | dynamic timer key not typed or target is non-finite |
| B12 | `$bound_step()` dynamic step clamp | `backend.py::_compile_statement`, `engine.py::run` bound-step handling | bound-step reduction op feeding step scheduler | P2 | expression uses unsupported runtime side effect |
| B13 | Source waveform values and source breakpoints | `engine.py::SourceBinding`, waveform `_next_breakpoint` helpers | source value/breakpoint primitive or keep Python source lane | P2 | custom Python waveform callable |
| B14 | Adaptive error-ratio scan and step growth/shrink | `engine.py::run` err-ratio block | Rust max-err-ratio array scan, dirty-node subset | P2 | no stable indexed node batch |
| B15 | Record/snapshot/CSV trace | `engine.py::record`, `SimResult`, runner CSV writer | sparse trace writer or required-signal array trace | P3 | checker expects full legacy CSV schema |
| B16 | System tasks: strobe/display/file/random | `backend.py::_compile_statement`, `_compile_function_call` | mostly Python side-effect lane; optional typed random primitive | P3 | file/string side effects remain Python |
| B17 | Hierarchy and dynamic instance/node resolution | `backend.py::_compile_instance_target`, dynamic bus helpers | interned node id / instance id resolver | P2 | unresolved hierarchy or generated node name not interned |
| B18 | Per-step lifecycle: prepare, evaluate, post-update, final sync | `engine.py::run`, `CompiledModel._prepare_step`, `post_update_events` | model segment executor with explicit phase graph | P1 | model has mixed Python-only and Rust-only phase ordering risk |

## Existing Rust Primitive Surface

| Rust primitive | Current status | Python/Rust files | Covers | Missing before production |
|---|---|---|---|---|
| `evaluate_static_linear_ops` | implemented | `rust_core/src/lib.rs`, `rust_backend.py`, `evaluate_ir.py` | linear node/state read/write, conditional select, integer state coercion | broader expression/control-flow IR; avoid small-segment FFI |
| `evaluate_transition_target_ops` | implemented | `rust_core/src/lib.rs`, `rust_backend.py` | target/delay/rise/fall expression batch | production handoff to `TransitionState`, not just shadow |
| `evaluate_ordered_transition_segment` | implemented as shadow path | `rust_core/src/lib.rs`, `engine.py::_run_rust_transition_shadow` | static-linear writes followed by transition target eval | execute transition state update in Rust and skip Python duplicate work |
| `next_transition_breakpoint_for_arrays` | implemented | `rust_core/src/lib.rs`, `backend.py::next_breakpoint` | typed-array transition breakpoint scan | transition state itself still Python object/dict |
| `next_timer_breakpoint_for_arrays` | implemented | `rust_core/src/lib.rs`, `backend.py::_next_timer_breakpoint` | typed-array timer breakpoint scan | timer due/reschedule still Python event body path |
| `max_err_ratio` | implemented | `rust_backend.py::max_err_ratio`, `engine.py` | array scan for adaptive step error ratio | dirty-node integration and record/snapshot integration |

## Target Rust Primitive Set

| Target | Purpose | Input buffers | Output buffers | First validation |
|---|---|---|---|---|
| R01 `expr_eval_batch` | Evaluate scalar expressions beyond affine linear forms | node values, state values, params, op bytecode | scalar scratch values | Python/Rust expression parity on generated models |
| R02 `state_update_batch` | Apply ordered scalar/array state assignments | scratch values, state arrays, integer flags | state arrays, dirty state flags | per-step shadow on stateful examples |
| R03 `contribution_batch` | Write `V(out)<+` outputs by node id | scratch values, output op list | node values, dirty node flags | waveform parity on static contribution models |
| R04 `transition_step_batch` | Replace Python `TransitionState.evaluate/set_target` hot path | transition state arrays, target arrays, time | transition output values, active flags, next breakpoints | shadow against Python transition states |
| R05 `event_detect_batch` | Detect cross/above events and crossing times | previous/current expression values, detector state arrays | fired flags, crossing times, detector states | exact cross/above regression tests |
| R06 `timer_event_batch` | Handle timer due/reschedule/absolute expiry | timer arrays, time, period/start/target buffers | due flags, next-fire arrays | timer conformance regressions |
| R07 `event_body_batch` | Execute lowerable event-body assignments after trigger | fired flags, state/node arrays, event body bytecode | state/node arrays, side-effect flags | event-body shadow parity |
| R08 `scheduler_breakpoint_batch` | Compute next source/model/timer/transition breakpoint | source/model breakpoint buffers | next dt clamp | no missed breakpoint tests |
| R09 `trace_record_batch` | Record only required signals from array state | node/state arrays, record ids | trace buffers | CSV parity on selected checkers |
| R10 `model_segment_executor` | Run a full model segment without per-step Python sync | all lowerable op batches and phase graph | node/state/timer/transition arrays | top-wall shadow then opt-in production |

## Mapping Rules

1. A Python behavior can enter production Rust only if it has a named Rust primitive, typed inputs/outputs, fallback rule, and parity test.
2. A model segment should not switch to production Rust if only a tiny fraction of its work is lowerable; this preserves the 040 small-segment gate lesson.
3. Event/cross/timer ordering is semantic, not an optimization detail. Rust must reproduce Python phase order before it can replace Python work.
4. `transition()` must be treated as two behaviors: target expression evaluation and transition state evolution. Optimizing only target evaluation is not enough.
5. Dynamic arrays and buses are not syntax blockers once they become base+offset indexed reads/writes; they should not be handled as one-off special cases.

## Phase Graph To Preserve

The production Rust executor must preserve this per-step order:

```text
1. source breakpoint / model breakpoint / bound_step choose dt
2. previous node snapshot when needed
3. source values update current node values
4. model prepare step for cross interpolation if needed
5. model evaluate / Rust segment evaluate
6. transition/timer state updates and output writes
7. post-update cross/above event bodies
8. adaptive err-ratio scan and dt adjustment
9. record selected signals
```

The key risk is not arithmetic. The key risk is moving a state update before or after event detection and changing event timing.

## Current Coverage Diagnosis

| Area | Current maturity | Why speed is not yet stable |
|---|---|---|
| Static-linear evaluate | partially covered | real top-wall has too few covered ops; small Rust segments lose to FFI/sync |
| State arrays | fixed-index partial | dynamic index and event-body arrays are still mostly Python |
| Transition target expressions | shadow-only | Python still owns transition state update and output behavior |
| Transition breakpoint scan | array scan exists | transition state is still Python object/dict, so packing/sync remains |
| Timer breakpoint scan | typed sidecar exists | timer event due/reschedule still Python, sidecar still mirrors dict state |
| Cross/above | Python only | event timing is sensitive, needs dedicated detector state arrays |
| Record/CSV | mostly Python | affects E2E, but should follow after kernel production path |

## Audit Corrections Captured By 049

The B01-B18 table above is a target map, not a claim that every target already has production Rust coverage. The follow-up audit in `049-behavior-coverage-manifest.md` fixes the exact wording needed for implementation:

- B01 is currently `partial`: static-linear IR plus limited conditions, not a general expression bytecode.
- B07 is currently transition target/shadow support; B08 transition state evolution is still Python-owned.
- B10 event body execution has no production Rust primitive yet.
- B12 `$bound_step()` has no Rust primitive; it is still a Python runtime scan feeding the step clamp.
- B16 system tasks and side effects remain a Python lane unless a deterministic primitive is designed.
- B17 hierarchy/dynamic node resolution is currently string/node-map/cache based; there is no typed Rust resolver primitive yet.
- R01-R10 are requirement labels for the future primitive set. The implemented Rust ABI names are the concrete `evas_rust_*` functions listed in 049.

## Implementation Plan After 048

| Step | Document | Concrete work | Success gate |
|---|---|---|---|
| 049 | `049-behavior-coverage-manifest.md` | Compiler emits per-model behavior coverage: B01-B18 present/lowered/fallback reason | top-wall report shows exact Rust blockers by behavior class |
| 050 | `050-transition-state-rust-production-plan.md` | Define and shadow `transition_step_batch` against Python `TransitionState` | zero transition parity mismatches on targeted regressions |
| 051 | `051-timer-cross-event-array-state.md` | Define detector/timer typed state arrays and event fired buffers | no missed timer/cross/above regressions |
| 052 | `052-event-body-ir-and-phase-graph.md` | Lower event body assignments into event body basic blocks | shadow parity on event-heavy top-wall models |
| 053 | `053-dynamic-array-bus-base-offset-ir.md` | Convert dynamic arrays/buses to base+offset indexed reads/writes | dynamic LFSR/PLL models stop reporting array-index blockers |
| 054 | `054-production-model-segment-executor.md` | One Rust call owns lowerable model segment phases, not tiny isolated ops | meaningful top-wall Rust coverage without small-segment slowdown |
| 055 | `055-record-and-trace-array-path.md` | Move record/snapshot/required-signal trace to array path | E2E improvement without changing checker semantics |
| 056 | `056-same-slice-speed-validation.md` | Run Python EVAS / Rust EVAS / Spectre AX / Spectre classic on same slice | only then evaluate speed/accuracy claims |

## Verification Gates

| Gate | Required before | Evidence |
|---|---|---|
| G1 behavior manifest | any further Rust production change | per-model B01-B18 coverage/fallback report |
| G2 shadow parity | enabling production Rust for a behavior class | Python/Rust internal-state parity, not just final CSV |
| G3 production opt-in | default-off production execution | targeted waveform/checker parity |
| G4 same-slice benchmark | any speed claim | same DUT/testbench/checker/settings/server; EVAS/Rust EVAS/Spectre AX/Spectre classic |
| G5 claim wording | paper-facing text | Spectre strict reference and AX comparison remain separate |

## Learning Notes

### Python function is not the unit of Rustification

`_transition()` is one Python function, but it contains multiple semantics:

- evaluate current transition output at time `t`
- decide whether the target changed
- apply delay/rise/fall/default transition rules
- update active/inactive state
- expose the next breakpoint

Rust should not blindly copy the Python function. It should expose the simulator primitive: transition state update over typed arrays.

### Why small Rust pieces can be slower

If Rust only evaluates six arithmetic ops, Python still has to:

- prepare input arrays
- cross the FFI boundary
- sync dict state back to Python
- run Python event/timer/record logic

The fixed Rust loop may be fast, but the boundary cost dominates. Real speedup requires a large enough segment where Rust owns most of the per-step work.

### Where Rust speed should come from

The expected win is not "Rust syntax is faster" in isolation. It is:

```text
Python dict/object/string-key dispatch
    -> integer ids + contiguous arrays + batched loops
```

That is why the next useful work is behavior mapping and production segment ownership, not another isolated syntax lowering.

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Rust changes event ordering | cross/timer regressions fail or waveform edge shifts | keep behavior in shadow mode; do not enable production executor |
| Mapping table becomes too broad | many classes have no tests or code anchors | split behavior class before implementation |
| Production path repeats small-segment slowdown | Rust mode slower with low `rust_static_eval_ops` | enforce small-segment gate and fallback to Python |
| Dynamic arrays silently mis-index | array parity tests fail or LFSR sequence changes | keep dynamic index in fallback until base+offset parity passes |
| E2E improvement hides kernel regression | checker/CSV wall improves but simulator wall does not | report simulator subprocess wall separately from E2E wall |

## Next Step

Next document:

- `049 - Behavior Coverage Manifest`

The next code change should not optimize a new behavior yet. It should make the compiler/runner report, for each top-wall model, which B01-B18 behavior classes appear, which have a Rust primitive, and exactly why the rest fallback.
