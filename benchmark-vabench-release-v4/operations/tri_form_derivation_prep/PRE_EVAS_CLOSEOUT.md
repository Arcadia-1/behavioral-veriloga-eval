# Pre-EVAS Closeout

This checkpoint records what is complete before the final EVAS executable is
frozen. It is deliberately not a final Gate 2 or Gate 3 certification.

## Completed

- The generated release contains 400 DUT, 400 Testbench, and 400 Bugfix tasks.
- Every family assigns one representative Bugfix seed and the same complete
  five-mutation suite to Testbench scoring and feedback.
- All 7,200 G0-G5 prompt records use the same terminal submission contract.
- The tri-form structure audit passes with no model-visible evaluator mount,
  trace-alias leak, absolute local path, or Bugfix mutation annotation.
- Current Spectre evidence covers 400/400 gold families and 2,000/2,000 active
  mutations. Every mutation replay is bound to matching current simulation
  components.
- The 95 stale task-local `spectre_rerun` labels are fully reconciled by the
  current matched replay ledger. They do not request a new simulator run.
- The property/diagnostic audit reports 400/400 families ready. Its 76 warnings
  identify shared diagnostic signatures; they are review hints, not uncovered
  properties or false-passing mutations.

## Not Yet Claimed

- The final EVAS source/runtime/ABI/executable identity is not frozen.
- Gate 2 is therefore 0/400 in the strict diagnostic: current EVAS evidence and
  several historical Spectre report schemas are not bound to the final lock.
- Gate 3 is 346/400 in the current authoring diagnostic. Thirty-nine families
  still need local certification promotion, and families 342 and 367 retain a
  stale derivation catalog hash. These states are inputs to the final rebuild,
  not evidence that their current Spectre behavior failed.
- The checked-in draft release seal is intentionally not refreshed from the
  temporary build. Rebuilding it now would create another stale executable
  identity when EVAS is frozen. Its replay test differs only in the status name
  (`gate3_static_sealed_simulation_pending` versus `package_structure_sealed`);
  all other seal fields match.

## Verification

- Focused regression bundle: 84 passed, 1 intentionally deselected.
- Target Python compile: pass.
- Derivation manifest schema parse: pass.
- Git diff and target trailing-whitespace checks: pass.
- Temporary tri-form build: 1,200 tasks, 7,200 prompts, static seal pass.

The machine-readable counts and evidence hashes are in
`PRE_EVAS_CLOSEOUT.json`.

## Finalization Order

1. Freeze EVAS source, runtime, ABI, and executable identity.
2. Run the 400 gold and 2,000 mutation EVAS validations under that identity.
3. Promote hash-bound certifications and rebuild the exact-five DUT source.
4. Rematerialize and audit the repository tri-form release.
5. Re-run Spectre only where a simulation component actually changed.
6. Emit and seal final Gate 2 and Gate 3 reports.
