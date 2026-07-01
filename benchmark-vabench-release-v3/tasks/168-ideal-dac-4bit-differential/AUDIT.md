# Audit: 168-ideal-dac-4bit-differential

- Gate 1: `independent_l1_ready` after repair. This is a clocked scalar-code to differential-output DAC with common-mode tracking.
- Gate 2: `cadence_modeling_ready` for the audited hidden/negative evidence slice. EVAS2 hidden gold and Spectre AX hidden gold pass after the transition/common-mode split.
- AHDL lint/read-in triage: the first Spectre pass exposed `VACOMP-1116` because `V(vcm)` was inside `transition(...)`. The gold and negative variants now keep the continuous common-mode term outside `transition(...)`; rerun logs have no `AHDLLINT-*`, `VACOMP-1116`, or `VACOMP/SPECTRE` errors.
- Public prompt: expanded to expose falling-edge sampling, mid-rise endpoint/step differential transfer, common-mode behavior, and parameter defaults.
- Hidden coverage: repaired with a distinct code sequence and a different `vcm` value from visible smoke.
- Checker: generalized to derive `vop`/`von` from sampled code and sampled `vcm`.
- Negative evidence: 4/4 Spectre hidden negatives are behaviorally rejected.
- Human review focus: confirm this should be counted separately from single-ended weighted DAC rows.
