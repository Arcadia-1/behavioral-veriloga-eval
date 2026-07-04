# Task 075 Audit

Task: `075-prbs-generator-32b-seeded`

Status: archived support/formal candidate with targeted Spectre validation; not counted in the active default denominator.

Packaging note: current `upstream/main` archives this row under `spectre-unsupported-tasks/` and excludes it from default `TASKS.json`/`CHECKS.yaml`. This PR repairs the archived asset only; restoration/counting remains an upstream policy decision.

## Gate 1

- Useful scenario: pass. A seeded 32-bit PRBS/LFSR source is a reusable voltage-domain AMS support utility for converter, link, calibration, and measurement stimulus flows.
- Counting boundary: archived support/formal candidate. This row can be restored only as a support utility; it is not a core L1 circuit-function claim by itself.

## Gate 2

- Public contract: pass. The prompt fixes module name, clock/reset/load-seed controls, vector seed/output ports, threshold, logic high level, transition time, seed load behavior, nonzero fallback, and LFSR tap/shift behavior.
- Spectre modeling contract: pass. The prompt states that electrical vector ports must be accessed through constant indices or generate-time static expansion, avoiding runtime/procedural `V(seed[i])` or `V(out[i])` indexing. Internal integer arrays may still be used for discrete state.
- Gold/starter/negative style: pass. The solution, starter, and five concrete negatives use constant-index static expansion for electrical vector ports so Spectre does not see runtime electrical-vector indexing.

## Evidence

- EVAS2 hidden gold: PASS.
- EVAS2 concrete negatives: 5/5 rejected as `FAIL_SIM_CORRECTNESS`.
- Spectre AX hidden gold: PASS; checker covered reset, nonzero seed load, PRBS progression, and output vector state.
- Spectre AX hidden negatives: 5/5 rejected behaviorally.
- EVAS AHDL-like lint preflight: starter and solution hidden decks PASS with zero diagnostics.
- AHDL/Spectre warning triage: no task-specific `AHDLLINT-*`, `VACOMP-1116`, `VACOMP-1192`, or AHDL compile errors were present. The remaining warnings are the shared `VACOMP-2435` AHDL-CMI environment notice and `SPECTRE-592` simulator-mode setup notice.

## Remaining Risk

- Full v3 sweep was not rerun for this audit slice.
- No model positive run is attached here, so this remains a support/formal-candidate validation record rather than a model-score claim.
