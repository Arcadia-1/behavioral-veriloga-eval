# 049 - Behavior Coverage Manifest

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related documents:

- `048-python-to-rust-behavior-map.md`
- `039-rust-coverage-expansion-for-real-models.md`
- `040-rust-mixed-small-segment-gate.md`
- `045-rust-required-rejection-and-if-lowering.md`
- `046-fixed-index-state-array-ir.md`

Machine-readable seed:

- `../behavior-coverage-map.v1.json`

## One-Line Summary

把 048 的 B01-B18 行为映射落成可审计 manifest 口径：每个模型都必须记录行为是否出现、是否已有 Rust/IR 覆盖、为什么 fallback、处在哪个仿真 phase、以及进入生产 Rust 前需要哪一类 parity gate。

## Why This Exists

前面 037-046 暴露的问题不是“Rust 不够快”，而是我们把很多不同语义混在一起讨论：

```text
有代码锚点 != 已有 Rust primitive
有 Rust shadow != 已经生产执行
有局部 IR != 整个模型可 Rust 化
有 EVAS-only timing != paper-facing speed claim
```

049 的作用是把这些状态拆开。后续任何 Rust 化都先更新/生成这个 manifest，再决定是否进入 shadow 或 production。这样做的目的不是多写文档，而是防止再次出现“补了一个小语法，但真实 top-wall 速度没变”的情况。

## Audit Inputs

本轮并行审计覆盖了四个互相独立的面：

| 审计面 | 关注内容 | 关键结论 |
|---|---|---|
| compiler/backend | B01-B07、B10、B12、B16、B17 的代码锚点、fallback 条件 | B01 只是 partial static-linear；B07 是 transition target/shadow；B10/B12/B16/B17 不能算已有 Rust production |
| engine/scheduler | 每步 phase order、event/timer/cross/bound_step 顺序 | Rust batch 必须保留 dt clamp、source update、evaluate、transition/timer、post-update、err-ratio、record 顺序 |
| Rust ABI | 现有 C ABI 与 Python `ctypes` 边界 | 仓库里真实存在的是具体 ABI 函数，048 的 R01-R10 是目标需求编号，不是已实现函数名 |
| report/counters | 039-046 与 top-wall 报告字段 | 已有 rejection/counter 可以直接复用为 manifest 的 `fallback_reasons` 与 `runtime_counters` |

## Status Vocabulary

manifest 中不要只写 `covered: true/false`。这会掩盖 shadow、fallback 和 small-segment gate。使用下面的状态：

| Status | Meaning | Can count as production Rust? |
|---|---|---|
| `implemented` | 已有 Rust ABI 或 Python/Rust IR executor，可被当前 runtime 调用 | 只有默认或 opt-in production path 真跳过 Python 重复执行时才算 |
| `shadow_only` | Rust 只做旁路计算/比较，Python 仍拥有语义执行 | no |
| `partial` | 只覆盖该行为的子集，例如 static-linear 表达式 | no, 除非 segment 决策也允许 |
| `python_only` | 当前语义由 Python 执行，无 Rust primitive | no |
| `python_fallback` | 静态扫描可识别该行为，但因模型结构/phase/动态引用回退 Python | no |
| `not_implemented` | 还没有对应 Rust primitive 或 IR 设计 | no |
| `unsupported` | EVAS 当前语义边界不支持，不应为了 Rust 化扩大 scope | no |

## Current Rust ABI Truth

048 中的 `R01` 到 `R10` 是目标需求编号，不是仓库里已经定义的 ABI 名称。当前代码中可以作为事实写入 manifest 的 Rust ABI 是：

| ABI / helper | Python binding | Covers | Status |
|---|---|---|---|
| `evas_rust_evaluate_static_affine` | `RustBackend.evaluate_static_affine` | old static affine contribution batch | implemented but narrow |
| `evas_rust_evaluate_static_linear` | `RustBackend.evaluate_static_linear` | static-linear node/state reads, writes, simple conditions, integer cast | implemented/partial |
| `evas_rust_evaluate_transition_targets` | `RustBackend.evaluate_transition_targets` | transition target/delay/rise/fall expression batch | implemented, mostly shadow/support |
| `evas_rust_evaluate_ordered_transition_segment` | `RustBackend.evaluate_ordered_transition_segment` | static-linear ops followed by transition target eval in one ordered batch | shadow_only |
| `evas_rust_next_transition_breakpoint` | `RustBackend.next_transition_breakpoint` | transition breakpoint min scan over typed arrays | implemented helper |
| `evas_rust_transition_state_step` | `RustBackend.transition_state_step` | transition state evaluate/set-target update over typed arrays | partial primitive, not engine production |
| `evas_rust_next_timer_breakpoint` | `RustBackend.next_timer_breakpoint` | timer breakpoint min scan over typed arrays | implemented helper |
| `evas_rust_timer_periodic_step` | `RustBackend.timer_periodic_step` | periodic timer due/skip/reschedule update over typed arrays | partial primitive, not engine production |
| `evas_rust_timer_absolute_step` | `RustBackend.timer_absolute_step` | absolute timer due/expired/last-fired update over typed arrays | partial primitive, not engine production |
| `evas_rust_cross_detector_step` | `RustBackend.cross_detector_step` | `cross()` detector state update over typed arrays | partial primitive, not engine production |
| `evas_rust_above_detector_step` | `RustBackend.above_detector_step` | `above()` detector state update over typed arrays | partial primitive, not engine production |
| `evas_rust_dynamic_bus_offsets` | `RustBackend.dynamic_bus_offsets` | bounded 1-D/2-D dynamic bus base+offset node-id calculation | partial primitive, not compiler/runtime production |
| `evas_rust_copy_f64` | `RustBackend.copy_f64` | array copy helper | implemented helper |
| `evas_rust_max_err_ratio` | `RustBackend.max_err_ratio` | adaptive error-ratio array scan | implemented helper |

Evidence anchors:

- `EVAS/evas/rust_core/src/lib.rs:1` for C ABI structs/constants.
- `EVAS/evas/rust_core/src/lib.rs:449` for static affine FFI.
- `EVAS/evas/rust_core/src/lib.rs:480` for static linear FFI.
- `EVAS/evas/rust_core/src/lib.rs:548` for transition target FFI.
- `EVAS/evas/rust_core/src/lib.rs:659` for ordered transition segment FFI.
- `EVAS/evas/rust_core/src/lib.rs:1121` for transition state step FFI.
- `EVAS/evas/rust_core/src/lib.rs:803` and `EVAS/evas/rust_core/src/lib.rs:968` for scanner/copy/error helpers.
- `EVAS/evas/simulator/rust_backend.py:21` and `EVAS/evas/simulator/rust_backend.py:343` for `ctypes` structs and bindings.

## Behavior Coverage Map

| ID | Runtime phase | Python/code anchor | Current Rust/IR status | Manifest fallback/risk |
|---|---|---|---|---|
| B01 | `evaluate` | `backend.py::_compile_expr`, `_evaluate_ir_linear_expr`; `evaluate_ir.py::LinearOpIR` | `partial`: static-linear + simple conditions only | `expr_non_static_linear`, `expr_function_*`, `expr_dynamic_reference` |
| B02 | `evaluate` / event interpolation | `_get_voltage`, `_compile_node_voltage`, dynamic bus helpers | `partial`: static node/state source slots; dynamic/event reads mostly Python | `future_node_voltages`, `dynamic_bus`, `event_interpolation` |
| B03 | `evaluate` | generated state assignment; indexed state metadata | `partial`: scalar/int state in static-linear path | `assignment_self_dependent_state`, `state_missing`, `state_type_mismatch` |
| B04 | `evaluate` | `_array_get`, `_array_set`; fixed-index state array IR | `partial`: fixed-index array element only | `assignment_dynamic_array_index`, `assignment_array_target`, `expr_array_access` |
| B05 | `evaluate` | `_compile_statement`, `_compile_for`, `_compile_case` | `partial`: simple `if/else` conditions; static loop only when lowered earlier | `if_statement`, `dynamic_for`, `case_statement`, `unsupported_control_flow` |
| B06 | `evaluate` | `_compile_contribution`, `_set_output` | `partial`: voltage output writes in static-linear path | `current_contribution`, `dynamic_branch_target`, `differential_target_not_lowered` |
| B07 | `evaluate` before transition state | `_transition_target_ir_op_from_contribution`, `TransitionTargetIR` | `shadow_only/partial`: target/delay/rise/fall can be batched | `expr_function_transition`, `transition_target_not_simple_node`, `ordered_segment_blocked` |
| B08 | `evaluate` / breakpoint | `TransitionState.evaluate`, `set_target`, `next_breakpoint` | `partial`: Rust typed-array state primitive and scan helper exist; engine production remains Python | `engine_production_not_wired`, `transition_state_python_fallback`, `event_ordering_not_batch_owned` |
| B09 | event detection | `CrossDetector`, `AboveDetector`, `_check_cross`, `_check_above` | `partial`: Rust typed-array detector state primitives exist; event ordering/body/interpolation side effects remain Python | `engine_production_not_wired`, `event_body_python`, `event_ordering_not_batch_owned`, `event_interpolation_side_effects` |
| B10 | event body / lifecycle | `_compile_event_statement`, `initial_step`, `final_step`, `post_update_events` | `python_only`; no event body Rust primitive | `event_statement`, `post_update_events`, `side_effect_event_body` |
| B11 | timer event / breakpoint | `_check_timer_due`, `_check_timer_at`, `_next_timer_breakpoint` | `partial`: Rust breakpoint scan and typed-array due/reschedule primitives exist; engine production/event body remains Python | `engine_production_not_wired`, `timer_event_body_python`, `event_ordering_not_batch_owned` |
| B12 | dt clamp | `$bound_step` compile assignment; engine bound-step scan | `python_only` | `bound_step_scan_python`, `bound_step_expr_unlowered` |
| B13 | source update / breakpoint | `SourceBinding`, waveform breakpoint helpers | `python_only` by policy for now | `custom_waveform_callable`, `source_breakpoint_python` |
| B14 | adaptive control | engine err-ratio block | `implemented helper`: Rust max scan exists, integration partial | `dirty_node_subset_missing`, `record_snapshot_dependency` |
| B15 | record/output | `record_point`, `SimResult`, CSV writer | `partial`: indexed path can record through precomputed node-id reads; list append, `SimResult`, CSV schema/writer remain Python/Numpy | `record_python_list_append`, `legacy_csv_schema`, `checker_required_signal_unknown`, `rust_record_abi_not_implemented` |
| B16 | side effects | strobe/display/file/random/function whitelist | `python_only` or `unsupported` | `system_task_side_effect`, `file_io`, `random_state`, `unsupported_function` |
| B17 | hierarchy/dynamic resolution | `_compile_instance_target`, `_resolve_dynamic_node`, node map | `partial`: dynamic node string cache remains production; Rust base+offset node-id primitive exists for bounded 1-D/2-D bus descriptors | `compiler_production_not_wired`, `stringified_instance_target`, `dynamic_node_cache_bypass`, `uninterned_node`, `dynamic_index_expr_python` |
| B18 | full lifecycle | engine `run` phase graph, generated `evaluate/post_update/final` | `not_implemented`: target is future model segment executor | `mixed_phase_ordering`, `small_segment_gate`, `python_sync_required` |

## Phase Graph Gate

Any production Rust executor must preserve the current phase order. This is a correctness rule, not an implementation preference.

```text
0. t=0 initialization: initial_step -> evaluate(t=0) -> absolute timer expiry -> optional post_update
1. choose dt from base/maxstep/refine
2. clamp dt by source breakpoints, model breakpoints, bound_step, output grid, min_step
3. snapshot previous node values for interpolation/adaptivity
4. advance time
5. update independent sources
6. prepare future-node context when event interpolation requires it
7. for each model, in model order:
   a. prepare_step when needed
   b. evaluate or lowerable Rust segment
   c. transition shadow/transition support hooks
   d. expire absolute timers
   e. post_update_events
   f. refresh_outputs if an event fired
8. reconcile indexed arrays / dict mirrors
9. handle cross-fired refine/record forcing
10. adaptive err-ratio scan and dt update
11. record selected output points
12. final_step after loop
```

Scheduler audit anchors:

- `EVAS/evas/simulator/engine.py:944` for initial condition pass.
- `EVAS/evas/simulator/engine.py:2092` for per-step dt selection.
- `EVAS/evas/simulator/engine.py:2098`, `2112`, `2126`, `2138` for dt clamps.
- `EVAS/evas/simulator/engine.py:2148`, `2212`, `2214`, `2228` for snapshot/time/source/future context.
- `EVAS/evas/simulator/engine.py:2237` to `2444` for per-model evaluation and post-update ordering.
- `EVAS/evas/simulator/engine.py:2450`, `2466`, `2479`, `2588` for reconciliation, cross refine, adaptivity, record.
- `EVAS/evas/simulator/engine.py:2611` for final step.

## Required Manifest Schema

The generated manifest should be a JSON object with this shape. Markdown reports can be rendered from the same data, but JSON is the source of truth.

The checked-in `behavior-coverage-map.v1.json` is the audited seed catalog. A future benchmark run should extend it with per-model `models[]` rows and runtime `aggregates`, not replace the catalog by ad hoc report wording.

```json
{
  "schema_version": "evas-rust-behavior-coverage.v1",
  "generated_at": "2026-06-04T00:00:00+08:00",
  "source_revision": {
    "evas_git_rev": "pending",
    "behavioral_git_rev": "pending",
    "rust_ffi_contract": "pending"
  },
  "claim_policy": {
    "paper_speed_claim_allowed": false,
    "reason": "behavior coverage is an engineering gate; speed claims require same-slice EVAS/Spectre timing"
  },
  "scope": {
    "suite": "topwall10",
    "rows": [],
    "rust_required": false,
    "indexed_arrays": false,
    "same_slice_spectre": false
  },
  "primitive_support_matrix": {},
  "behavior_catalog": [],
  "models": [],
  "aggregates": {}
}
```

Per model entry:

```json
{
  "model_id": "example_id",
  "model_path": "path/to/model.va",
  "module_name": "module_name",
  "phase_flags": {
    "has_initial_step": false,
    "has_final_step": false,
    "has_post_update_events": false,
    "has_dynamic_breakpoints": false,
    "uses_bound_step": false,
    "needs_future_node_voltages": false,
    "has_child_models": false
  },
  "behavior_coverage": [
    {
      "behavior_id": "B07",
      "present_in_source": true,
      "runtime_phase": "evaluate",
      "python_anchor_refs": ["EVAS/evas/simulator/backend.py:3245"],
      "ir_anchor_refs": ["EVAS/evas/simulator/evaluate_ir.py:359"],
      "rust_primitive": "evas_rust_evaluate_transition_targets",
      "coverage_status": "shadow_only",
      "coverage_ratio": 0.0,
      "fallback_reasons": [
        {"reason": "ordered_segment_blocked", "count": 1}
      ],
      "runtime_counters": {},
      "risk_level": "high",
      "correctness_gates": ["transition-target-shadow", "transition-state-shadow"],
      "next_action": "need_engine_production_wiring",
      "notes": "target expression batch plus transition state primitive are still not equivalent to production transition execution until engine phase order is Rust-owned"
    }
  ],
  "segment_decision": {
    "eligible_for_shadow": true,
    "eligible_for_production": false,
    "small_segment_policy": {
      "enabled": true,
      "min_ops_threshold": 64,
      "fallback_reason": "planned_ops_below_threshold"
    },
    "dominant_blockers": ["event_statement", "expr_function_transition"]
  }
}
```

## Required Enums

`coverage_status`:

```text
implemented
shadow_only
partial
python_only
python_fallback
not_implemented
unsupported
```

`runtime_phase`:

```text
initial_step
prepare
evaluate
transition_state
breakpoint_scan
event_detect
event_body
post_update
bound_step
source_update
adaptive_step
record
final_step
```

`next_action`:

```text
no_op
need_rust_primitive
need_shadow_gate
need_production_gate
narrow_behavior
stabilize_runtime_order
keep_python_side_effect_lane
unsupported_scope_boundary
```

## Fallback Reason Dictionary

The manifest should reuse existing engine/report counters where possible.

| Reason | Behavior IDs | Meaning |
|---|---|---|
| `event_statement` | B10 | Event body exists and is not lowerable into current static-linear path |
| `event_cross` | B09/B10 | Cross trigger/event ordering must stay Python until event detector/body IR exists |
| `event_above` | B09/B10 | Above trigger/event ordering must stay Python |
| `post_update_events` | B10/B18 | Model requires post-update event phase; static Rust segment cannot reorder it |
| `expr_function_transition` | B07/B08 | `transition()` appears in expression/contribution path; target may be shadowed, B08 typed-array state primitive exists, but engine production execution remains Python |
| `assignment_self_dependent_state` | B03/B05 | Ordered state recurrence is not a plain static-linear independent assignment |
| `assignment_array_target` | B04 | Array write target not lowerable into current flattened slot |
| `assignment_dynamic_array_index` | B04/B17 | Runtime index requires base+offset primitive and bounds parity |
| `expr_array_access` | B04 | Array read not lowerable into current state slots |
| `if_statement` | B05 | Control-flow present; only simple condition subset is lowerable |
| `expr_non_static_linear_binary` | B01 | Expression cannot be represented by current linear IR |
| `expr_unsupported_binary_op` | B01 | Operator not represented by current Rust op set |
| `expr_function_unsupported_ternary_condition` | B01/B05 | Ternary condition is outside current condition subset |
| `future_node_voltages` | B02/B09/B18 | Event interpolation/future context needed |
| `child_models` | B17/B18 | Hierarchical model order/state prevents simple model-local Rust segment |
| `state_missing` | B03/B04 | State slot metadata incomplete |
| `stringified_instance_target` | B17 | Instance target fell back to string formatting rather than interned id |
| `dynamic_node_cache_bypass` | B17 | Dynamic node cache capacity/formatting path bypassed typed id resolver |
| `planned_ops_below_threshold` | B18 | Small mixed segment should fallback to Python to avoid FFI/sync loss |

Existing evidence anchors:

- `045-rust-required-rejection-and-if-lowering.md` records high-frequency blockers including `expr_function_transition`, `assignment_self_dependent_state`, `event_cross`, and `if_statement`.
- `046-fixed-index-state-array-ir.md` records fixed-index array progress and remaining `assignment_dynamic_array_index` / `expr_array_access` blockers.
- `040-rust-mixed-small-segment-gate.md` records the small-segment gate and fallback counters.

## Runtime Counters To Reuse

| Counter family | Use in manifest |
|---|---|
| `rust_static_eval_no_candidate_*` | Count models/ops rejected before a Rust segment is built |
| `rust_static_eval_fallback_*` | Count built plans that fell back at runtime |
| `rust_static_eval_no_segment_fallbacks` | Count no usable segment fallback |
| `rust_static_eval_mixed_small_fallbacks` | Count small mixed segments rejected by threshold |
| `rust_static_eval_mixed_small_gated_models` | Record which models were gated |
| `rust_static_eval_mixed_small_gated_ops` | Record how many ops were gated |
| `transition_output_fastpath_calls` | Diagnostic only; not transition production coverage |
| `transition_breakpoint_inactive_skips` | Diagnostic/helper evidence for breakpoint scan |
| `transition_unchanged_target_fastpath` | Diagnostic only; unchanged-target shortcut is not full transition Rustification |
| `timer_scan_*` | Timer scan helper evidence; not timer event body production coverage |

## Correctness Gates

| Gate | Required before | Evidence expected |
|---|---|---|
| `compile-operator-rule-gate` | accepting a model into Rust planning | Spectre-compatible operator validation passes |
| `behavior-manifest-gate` | any new production Rust behavior | B01-B18 present/lowered/fallback report exists for target rows |
| `shadow-state-gate` | enabling production for stateful behavior | Python/Rust internal state parity, not only final CSV |
| `event-order-gate` | enabling cross/above/timer/event body Rust path | no missed event, no retrograde cross replay, same event body ordering |
| `small-segment-gate` | using mixed Rust/Python execution | planned ops and sync cost justify Rust call; otherwise Python fallback |
| `production-opt-in-gate` | defaulting Rust execution for a behavior | targeted waveform/checker parity with zero shadow mismatches |
| `same-slice-speed-gate` | any paper-facing speed statement | same DUT/testbench/checker/settings/server EVAS/Rust EVAS/Spectre timing |

Important audit result: current shadow paths record mismatches in metrics, but do not by themselves hard-fail every run. The harness that consumes this manifest must treat nonzero mismatch counters as failed gates before enabling production.

## 048 Corrections Captured By 049

These are not new bugs; they are wording corrections needed to avoid overclaiming.

| 048 item | Correction |
|---|---|
| B01 target says expression DAG/bytecode | Current implementation is static-linear IR plus limited conditions; full expression bytecode is still a target |
| B07 looks like transition support | Current Rust coverage is transition target expression, ordered shadow, and a B08 typed-array transition state primitive; engine production execution remains Python |
| B10 target says event-body IR | No event-body Rust primitive exists yet; event body is Python/lifecycle-sensitive |
| B12 bound_step target | No Rust primitive exists; it is a Python scan feeding dt clamp |
| B16 side effects | File/string/random/strobe tasks must remain Python lane unless a separate deterministic primitive is designed |
| B17 hierarchy/dynamic resolution | Current production implementation is string/node-map/cache based; 054 adds a bounded base+offset Rust primitive, but compiler/runtime production wiring is still missing |
| R01-R10 | Treat as target requirement IDs, not implemented ABI names |

## First Implementation Slice

The next code change should generate this manifest without changing simulation behavior:

1. Extend compiled model metadata into a per-model behavior scan:
   - `_evaluate_ir_static_linear_ops`
   - `_evaluate_ir_static_linear_rejections`
   - `_transition_target_ir_ops`
   - `_ordered_transition_segment_ir_ops`
   - `_has_dynamic_breakpoints`
   - `_has_post_update_events`
   - `_uses_bound_step`
   - `_needs_future_node_voltages`
2. Merge runtime stats into the same row:
   - rust static eval candidate/fallback counters
   - transition/timer scan counters
   - shadow mismatch counters
   - small-segment gate counters
3. Emit JSON first, then Markdown summary.
4. Keep `paper_speed_claim_allowed=false` until same-slice Spectre timing exists.

## Success Definition

049 is complete when a reviewer can answer these questions from one manifest:

- Which B01-B18 behaviors does a model use?
- Which of those behaviors have current Rust ABI coverage?
- Is that coverage production, shadow, partial, or Python-only?
- Why did a model fallback?
- Which correctness gate must pass before production Rust can own the behavior?
- Which blockers dominate top-wall models?
- Whether a speed claim is allowed. For this manifest, the answer is no.

## Next Step

Implement the generator that emits `evas-rust-behavior-coverage.v1` from compiled model metadata and runtime counters. That generator should be the input to 050+ transition/event/timer production work, not another isolated syntax optimization.
