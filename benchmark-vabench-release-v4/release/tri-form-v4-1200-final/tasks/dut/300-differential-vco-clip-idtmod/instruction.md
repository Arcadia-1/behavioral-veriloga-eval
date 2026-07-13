# Differential VCO With Clip And Idtmod

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `differential_vco_clip_idtmod.va`: `differential_vco_clip_idtmod`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FREQ_Q_CLIP_FNOM_DFDV_V`: `freq_q = `clip(Fnom + dFdV * V(vinp, vinm), Fmin, Fmax)`
- `P_PHASE_Q_IDTMOD_FREQ_Q_0`: `phase_q = idtmod(freq_q, 0.0, 1.0)` (modulo-1 phase accumulator)
- `P_OUTP_VCM_VAC_SIN_M_TWO`: `outp = Vcm + Vac * sin(M_TWO_PI * phase_q)` (positive differential arm)
- `P_OUTM_VCM_VAC_SIN_M_TWO`: `outm = Vcm - Vac * sin(M_TWO_PI * phase_q)` (negative differential arm)
- `P_METRIC_0_9_PHASE_Q_VOLTAGE`: `metric = 0.9 * phase_q` (voltage-coded instantaneous wrapped phase, `0 V` to `0.9 V`)

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `differential_vco_clip_idtmod.va`.
Do not add or omit artifacts.
