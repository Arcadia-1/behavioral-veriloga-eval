# Audit: 200-dac-ideal-4b-offset

- Gate 1: `independent_l1_ready` after rescue. This is retained as a calibrated offset/trim DAC, not a plain full-scale binary DAC.
- Gate 2: `cadence_modeling_ready` for the audited hidden/negative evidence slice. EVAS2 hidden gold and Spectre AX hidden gold pass.
- AHDL lint/read-in triage: Spectre hidden gold and hidden negative logs were inspected for `AHDLLINT-*`, `VACOMP-1116`, and `VACOMP/SPECTRE` errors; none are present. Remaining setup notices are environment/Spectre X warnings, not task-specific AHDL lint failures.
- Public prompt: rewritten to expose the public `offset = 0.239 V` calibration baseline, public calibration scale `32.0*10.0/9.0`, bit order, and endpoint/step trim behavior.
- Hidden coverage: repaired to use a distinct private trim-code sequence from visible smoke.
- Checker: generalized to derive `dout` from the observed input bits, fixed offset, and calibration scale.
- Negative evidence: 4/4 Spectre hidden negatives are behaviorally rejected.
- Human review focus: confirm the trim/offset role is enough to keep this separate from ordinary binary-weighted DAC rows.
