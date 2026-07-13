# Differential VCO With Clip And Idtmod Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `differential_vco_clip_idtmod.va`: `differential_vco_clip_idtmod`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FREQ_Q_CLIP_FNOM_DFDV_V`: `freq_q = `clip(Fnom + dFdV * V(vinp, vinm), Fmin, Fmax)`
- `P_PHASE_Q_IDTMOD_FREQ_Q_0`: `phase_q = idtmod(freq_q, 0.0, 1.0)` (modulo-1 phase accumulator)
- `P_OUTP_VCM_VAC_SIN_M_TWO`: `outp = Vcm + Vac * sin(M_TWO_PI * phase_q)` (positive differential arm)
- `P_OUTM_VCM_VAC_SIN_M_TWO`: `outm = Vcm - Vac * sin(M_TWO_PI * phase_q)` (negative differential arm)
- `P_METRIC_0_9_PHASE_Q_VOLTAGE`: `metric = 0.9 * phase_q` (voltage-coded instantaneous wrapped phase, `0 V` to `0.9 V`)

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `differential_vco_clip_idtmod.va`.
Every supplied `.va` file is editable; do not add or omit files.
