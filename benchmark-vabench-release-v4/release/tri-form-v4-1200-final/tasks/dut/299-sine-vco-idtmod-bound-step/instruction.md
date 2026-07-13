# Sine VCO With Idtmod And Bound Step

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sine_vco_idtmod_bound_step.va`: `sine_vco_idtmod_bound_step`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FREQ_Q_CENTER_FREQ_VCO_GAIN`: `freq_q = center_freq + vco_gain * V(vin)`
- `P_PHASE_Q_IDTMOD_FREQ_Q_0`: `phase_q = idtmod(freq_q, 0.0, 1.0)` (modulo-1 phase accumulator)
- `P_OUT_VCO_AMP_SIN_M_TWO`: `out = vco_amp * sin(M_TWO_PI * phase_q)` (bipolar sine centered at `0 V`)
- `P_METRIC_VCO_AMP_PHASE_Q_VOLTAGE`: `metric = vco_amp * phase_q` (voltage-coded instantaneous wrapped phase, `0 V` to `vco_amp`)
- `P_CALL_BOUND_STEP_1_0_VCO`: call `$bound_step(1.0 / (vco_ppc * freq_q))` every step so the sine is resolved

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sine_vco_idtmod_bound_step.va`.
Do not add or omit artifacts.
