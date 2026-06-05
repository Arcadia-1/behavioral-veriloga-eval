# Note On Bundled EVAS Commit (commit 2c754c7)

The audit-095 commit on the EVAS repo (`2c754c7`) titled "Audit 095:
record adaptive substeps in 091d generic executor" actually bundled
**27,486 insertions / 1,224 deletions across 12 files**, not the
narrow audit-095 change implied by the commit message.

This is because the working tree had ~26k lines of accumulated
pre-existing changes (audit 037-085 implementation, transition
batch code, cross/above primitives, etc.) that had been deliberately
held back per user directive ("等 Rust 进程结束后再一起 commit").

When the user authorized stages 1-6 of the multi-stage execution
plan in audit 094, stage 6 was "EVAS code commit hygiene". This
got executed (by accident) when audit 095's `git commit -am` swept
all modified files in addition to the audit-095 backend.py edit.

## What Is Actually In That Commit

| File | Insertions | Source audit |
|---|---:|---|
| `evas/simulator/backend.py` | +8,226 | Audits 037-085 + 095 |
| `evas/rust_core/src/lib.rs` | +7,203 | Audits 050-085 (transition primitive, cross/above, timer queue) |
| `evas/simulator/engine.py` | +4,311 | Audits 080-095 (dispatcher, executor, parity refinement) |
| `tests/test_engine.py` | +3,263 | Audits 088-095 test suites |
| `evas/simulator/rust_backend.py` | +2,715 | ctypes wrappers for 050-085 primitives |
| `tests/test_rust_backend.py` | +1,240 | Primitive parity tests |
| `tests/test_indexed_backend.py` | +545 | Indexed array tests |
| `tests/test_netlist.py` | +230 | Netlist runner tests |
| `evas/netlist/runner.py` | +212 | EVAS_RUST_* env var support |
| `evas/simulator/indexed.py` | +8 | Indexed state slot tweaks |
| `prototypes/audit_088_real_bench.py` | +23 | Bench script tweak |
| `prototypes/audit_093_sweep_results.json` | +734 | Sweep result data |

## What This Means For History Reading

- The 095 audit's actual code change is the modification to
  `_try_generic_event_state_transition_fastpath` in `engine.py`.
  It's a single ~25-line block.
- The other 27k lines are the cumulative Rust kernel work from
  audits 037-085 that had been kept in working tree.
- Bisect on this single commit will not isolate 095 from the
  bundled prior work.

## Recommendation

If future debugging needs to bisect to find 095-specific regression,
search for the `# Audit 095:` comment in engine.py rather than
relying on git log diffs.

For audit history reading, treat commit `2c754c7` on EVAS as
"land all accumulated Rust kernel work + audit 095 parity fix"
rather than "audit 095 only".
