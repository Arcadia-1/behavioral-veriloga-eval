# 051 - Timer Step Rust Primitives

Status: done
Date: 2026-06-04

## One-line Summary

B11 timer handling now has Rust typed-array primitives for periodic timer due/reschedule and absolute timer due/expire state updates. This is not yet the production engine path because event body execution and lifecycle ordering remain Python-owned.

## Why This Exists

Before 051, Rust could scan timer breakpoint arrays through `evas_rust_next_timer_breakpoint`, but it could not evaluate the timer state machine itself.

That meant B11 still had this gap:

- Rust could find the next timer breakpoint.
- Python still decided whether a periodic/absolute timer was due.
- Python still updated `timer_states` / `timer_last_fired`.
- Python still executed the event body.

051 closes only the primitive-level due/reschedule gap.

## Timer Semantics

### Periodic Timer

For `@(timer(start, period))`, Python EVAS semantics are:

1. reject non-finite or non-positive `period`;
2. initialize `next_fire` from `start` if present, otherwise from `period`;
3. if current time has passed `next_fire + eps`, skip missed periods and set a future `next_fire`;
4. if current time is within `eps` of `next_fire`, mark due;
5. optionally reschedule `next_fire += period`.

The Rust primitive exposes `reschedule_on_due` as an explicit input so future production wiring can preserve event-body order: detect due first, execute Python/Rust event body later, then reschedule at the correct phase.

### Absolute Timer

For `@(timer(target))`, Python EVAS semantics are:

1. reject non-finite `target`;
2. initialize or re-arm `next_fire` when target changes;
3. if this is the first observation and time already passed target, mark it expired and do not fire;
4. suppress duplicate fire when `last_fired == armed_target`;
5. fire when `time >= armed_target - eps`, then update `last_fired`.

## Code Changes

| File | Change |
|---|---|
| `EVAS/evas/rust_core/src/lib.rs` | Added `timer_periodic_step_for_arrays()`, `timer_absolute_step_for_arrays()`, C ABI `evas_rust_timer_periodic_step()`, and C ABI `evas_rust_timer_absolute_step()` |
| `EVAS/evas/simulator/rust_backend.py` | Added optional ctypes symbol probing plus `RustBackend.timer_periodic_step()` and `RustBackend.timer_absolute_step()` |
| `EVAS/tests/test_rust_backend.py` | Added Python-oracle parity tests against `CompiledModel._check_timer()` and `_check_timer_at()` |
| `behavior-coverage-map.v1.json` | Updated B11 to include timer step primitives while keeping production status partial |

The Python binding treats both new symbols as optional. Older Rust libraries still load; calling the new step methods on an old library raises a targeted `RustBackendError`.

## Correctness Gates

This primitive is accepted only at the timer-state semantic level:

- it does not execute event bodies;
- it does not change `Simulator.run()` lifecycle order;
- it does not replace Python `_check_timer_due`, `_check_timer_at`, or `_reschedule_timer`;
- it must match Python timer behavior before any shadow or production handoff.

## Verification

Commands run:

```text
cd EVAS/evas/rust_core && cargo test
PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m py_compile EVAS/evas/simulator/rust_backend.py EVAS/tests/test_rust_backend.py
PYTHONPATH=EVAS PYTHONPYCACHEPREFIX=/private/tmp/evas-pycache python3 -m pytest EVAS/tests/test_rust_backend.py -q
```

Observed result:

- Rust unit tests passed: `21 passed`.
- Python compile check passed.
- full Rust backend test file passed: `14 passed`.

## What This Does Not Prove

This does not prove timer events are fully Rustified.

Timer event production still includes Python-owned pieces:

- generated event body execution;
- `_event_context_active` and event-time side effects;
- lifecycle order around `evaluate`, `_expire_absolute_timers`, `post_update_events`, and `refresh_outputs`;
- timer state dict/array synchronization in the engine.

## Remaining Work After 051

| Area | Still Python-owned / incomplete |
|---|---|
| B11 production handoff | engine must shadow periodic/absolute timer step before using Rust as authority |
| B10 event body | generated event body execution is still Python and side-effect sensitive |
| B18 lifecycle | full model lifecycle executor cannot be production Rust until event ordering is covered |
| B15 record/output | trace schema and checker-required signals still require Python-compatible output |

## Next Step

Add an opt-in timer shadow path that snapshots Python timer state before event checks, runs Rust periodic/absolute step with the same inputs, and compares post-state after Python execution. Only after this shadow path is stable across timer-heavy benchmarks should production handoff be considered.
