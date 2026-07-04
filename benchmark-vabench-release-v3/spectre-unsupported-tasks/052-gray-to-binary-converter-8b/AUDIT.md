# Task 052 Audit

Task: `052-gray-to-binary-converter-8b`

Status: archived support/formal candidate with targeted Spectre validation; not counted in the active default denominator.

Packaging note: current `upstream/main` archives this row under `spectre-unsupported-tasks/` and excludes it from default `TASKS.json`/`CHECKS.yaml`. This PR repairs the archived asset only; restoration/counting remains an upstream policy decision.

## Gate 1

- Useful scenario: pass. An 8-bit Gray-to-binary code converter is a reusable voltage-domain AMS support utility for converter, encoder, and measurement testbenches.
- Counting boundary: archived support/formal candidate. This row can be restored only as a support utility; it is not a core L1 circuit-function claim by itself.

## Gate 2

- Public contract: pass. The prompt fixes module name, vector port order, threshold, logic high level, transition time, bit order, and Gray-to-binary observable behavior.
- Spectre modeling contract: pass. The prompt now states that electrical vector ports must be accessed through constant indices or generate-time static expansion, avoiding runtime/procedural `V(g[i])` or `V(b[i])` indexing.
- Gold/starter/negative style: pass. The solution, starter, and five concrete negatives use constant-index static expansion so Spectre does not see runtime electrical-vector indexing.

## Evidence

- EVAS2 hidden gold: PASS.
- EVAS2 concrete negatives: 5/5 rejected as `FAIL_SIM_CORRECTNESS`.
- Python EVAS hidden gold/negative cross-check: PASS with the same expectations.
- Spectre AX hidden gold: PASS; checker covered boundary and representative codes including 0, 1, 2, 127, 128, 200, and 255.
- Spectre AX hidden negatives: 5/5 rejected behaviorally.
- EVAS AHDL-like lint preflight: starter and solution hidden decks PASS with zero diagnostics.
- AHDL/Spectre warning triage: no task-specific `AHDLLINT-*`, `VACOMP-1116`, `VACOMP-1192`, or AHDL compile errors were present. The remaining warnings are the shared `VACOMP-2435` AHDL-CMI environment notice and `SPECTRE-592` simulator-mode setup notice.

## Remaining Risk

- Full v3 sweep was not rerun for this audit slice.
- No model positive run is attached here, so this remains a support/formal-candidate validation record rather than a model-score claim.
