# Task 056 Audit

Task: `056-decimal-digit-to-bcd-encoder`

Status: support formal candidate with targeted Spectre validation.

Packaging note: current `upstream/main` archives this row under `spectre-unsupported-tasks/`; this PR repairs the archived asset and does not re-add it to the active default denominator.

## Gate 1

- Useful scenario: pass. A one-hot decimal digit to BCD encoder is a reusable voltage-domain AMS support utility for front-panel, calibration-code, readout, and verification flows.
- Counting boundary: support/formal candidate. This row remains a support utility, not a core L1 circuit-function claim by itself.

## Gate 2

- Public contract: pass. The prompt fixes module name, vector port order, threshold, logic high level, transition time, bit order, valid output, and invalid zero/multi-digit behavior.
- Spectre modeling contract: pass. The prompt states that electrical vector ports must be accessed through constant indices or generate-time static expansion, avoiding runtime/procedural `V(d[i])` or `V(b[i])` indexing.
- Gold/starter/negative style: pass. The solution, starter, and five concrete negatives use constant-index static expansion so Spectre does not see runtime electrical-vector indexing.

## Evidence

- EVAS2 hidden gold: PASS.
- EVAS2 concrete negatives: 5/5 rejected as `FAIL_SIM_CORRECTNESS`.
- Spectre AX hidden gold: PASS; checker covered all ten decimal digits plus invalid zero-hot and multi-hot states.
- Spectre AX hidden negatives: 5/5 rejected behaviorally.
- EVAS AHDL-like lint preflight: starter and solution hidden decks PASS with zero diagnostics.
- AHDL/Spectre warning triage: no task-specific `AHDLLINT-*`, `VACOMP-1116`, `VACOMP-1192`, or AHDL compile errors were present. The remaining warnings are the shared `VACOMP-2435` AHDL-CMI environment notice and `SPECTRE-592` simulator-mode setup notice.

## Remaining Risk

- Full v3 sweep was not rerun for this audit slice.
- No model positive run is attached here, so this remains a support/formal-candidate validation record rather than a model-score claim.
