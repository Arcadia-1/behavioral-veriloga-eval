# Sine VCO With Idtmod And Bound Step Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sine_vco_idtmod_bound_step.va`: `sine_vco_idtmod_bound_step`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FREQ_Q_CENTER_FREQ_VCO_GAIN`: `freq_q = center_freq + vco_gain * V(vin)`
- `P_PHASE_Q_IDTMOD_FREQ_Q_0`: `phase_q = idtmod(freq_q, 0.0, 1.0)` (modulo-1 phase accumulator)
- `P_OUT_VCO_AMP_SIN_M_TWO`: `out = vco_amp * sin(M_TWO_PI * phase_q)` (bipolar sine centered at `0 V`)
- `P_METRIC_VCO_AMP_PHASE_Q_VOLTAGE`: `metric = vco_amp * phase_q` (voltage-coded instantaneous wrapped phase, `0 V` to `vco_amp`)
- `P_CALL_BOUND_STEP_1_0_VCO`: call `$bound_step(1.0 / (vco_ppc * freq_q))` every step so the sine is resolved

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sine_vco_idtmod_bound_step.va`.
Every supplied `.va` file is editable; do not add or omit files.
