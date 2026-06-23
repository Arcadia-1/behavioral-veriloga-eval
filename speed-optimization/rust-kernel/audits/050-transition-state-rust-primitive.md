# 050 - Transition State Rust Primitive

Status: done
Date: 2026-06-04

## One-line Summary

B08 `transition()` state evolution now has a Rust typed-array primitive, Python/Rust parity tests, and an opt-in `rust_transition_shadow` state-evolution parity check. This is not yet the production engine path, so it must not be reported as full EVAS Rustification or as a speed claim.

## Why This Exists

Previous Rust work covered only pieces around `transition()`:

- B07 target/delay/rise/fall expression evaluation can be shadowed in Rust.
- transition breakpoint min-scan can run over typed arrays.
- the real `TransitionState.evaluate()` / `set_target()` update was still Python-owned.

This left a semantic gap: Rust could know what the next target was, and could scan future breakpoints, but it could not update the active transition state itself. 050 closes that primitive-level gap.

## Math / Semantics

For each transition state slot, EVAS keeps:

- `current_value`
- `target_value`
- `start_time`
- `start_value`
- `delay`
- `rise_time`
- `fall_time`
- `active`
- `initialized`

At simulation time `t`, the output is piecewise:

1. before `start_time + delay`: hold `start_value`;
2. during the ramp: linear interpolation from `start_value` to `target_value`;
3. after ramp end: hold `target_value` and mark inactive.

When a new target arrives while a transition is active, Rust first evaluates the current in-flight value at `t`, then starts a new transition from that value. This mirrors Python's interrupted-transition behavior and avoids a waveform jump.

Rise/fall time follows the existing EVAS rule:

- if the supplied rise/fall is positive, use it;
- otherwise use `default_transition`.

Initial-condition mode initializes the state directly to the target and marks it inactive, matching Python's `TransitionState` oracle.

## Code Changes

| File | Change |
|---|---|
| `EVAS/evas/rust_core/src/lib.rs` | Added `transition_state_step_for_arrays()` and C ABI `evas_rust_transition_state_step()` |
| `EVAS/evas/simulator/rust_backend.py` | Added optional ctypes binding and `RustBackend.transition_state_step()` wrapper |
| `EVAS/tests/test_rust_backend.py` | Added parity test comparing Rust typed arrays against Python `TransitionState` over initialization, ramp, retarget, and initial-condition reset |
| `EVAS/evas/simulator/engine.py` | Extended `rust_transition_shadow` to snapshot Python pre-state and compare Rust stepped state against Python post-state |
| `EVAS/tests/test_engine.py` | Extended transition shadow test to require zero state-evolution mismatches |
| `behavior-coverage-map.v1.json` | Updated B08 from `python_only` to `partial` |

The Python binding treats the new symbol as optional. If an older `.so` is loaded, optional Rust backend initialization still works; calling `transition_state_step()` then raises a targeted `RustBackendError`.

## Correctness Gates

This primitive is accepted only at the Rust/Python semantic level:

- it does not change the default engine production path;
- it does not reorder event/timer/cross phases;
- it does not bypass Python fallback;
- it must match Python `TransitionState` numerically before any production handoff.

## Verification

Commands run:

```text
cd EVAS/evas/rust_core && cargo test
PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m py_compile EVAS/evas/simulator/rust_backend.py EVAS/tests/test_rust_backend.py
cd EVAS/evas/rust_core && cargo build --release
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_rust_backend.py::test_rust_backend_steps_transition_state_like_python -q
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_rust_backend.py -q
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_engine.py -k rust_transition_shadow_matches_ordered_state_target_segment -q
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_engine.py::TestTransitionState -q
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_engine.py -k 'rust_transition_shadow or transition_breakpoint or transition_state' -q
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_engine.py -q
```

Observed result:

- Rust unit tests passed.
- Python compile check passed.
- Rust release build passed.
- targeted transition parity test passed.
- full Rust backend test file passed: `12 passed`.
- transition shadow state-evolution test passed.
- `TestTransitionState` passed: `17 passed`.
- transition-related engine subset passed: `2 passed, 222 deselected`.
- full engine test file passed: `224 passed`.

## What This Does Not Prove

This does not prove EVAS is fully Rustified.

It also does not prove speedup, because the production engine still calls Python's transition path. Speed impact can only be measured after the engine hands a contiguous transition segment to Rust without per-step dict/object synchronization.

## Remaining Work After 050

| Area | Still Python-owned / incomplete |
|---|---|
| B08 production handoff | engine still needs guarded shadow-to-production wiring for transition state arrays |
| B09/B10 events | cross/above detection and event body execution remain Python lifecycle code |
| B11 timer | due/reschedule/event body remain Python; only scan helper is Rust |
| B15 record/output | record/snapshot/CSV are still Python structures |
| B17 dynamic hierarchy | dynamic node/bus resolution is still string/cache based |
| B18 lifecycle | full model phase executor is not implemented in Rust |

## Next Step

Use this primitive inside an opt-in transition shadow runner first. Only after shadow parity across real transition-heavy benchmarks should the engine switch a safe segment from Python transition state execution to Rust production execution.
