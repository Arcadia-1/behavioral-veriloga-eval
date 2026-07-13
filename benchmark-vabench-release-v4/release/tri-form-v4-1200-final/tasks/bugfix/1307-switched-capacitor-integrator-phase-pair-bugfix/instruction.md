# Switched-capacitor Integrator Phase Pair Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `switched_cap_integrator_phase_pair_top.va`: `switched_cap_integrator_phase_pair_top`
- `sample_phase_cell.va`: `sample_phase_cell`
- `integrator_state_cell.va`: `integrator_state_cell`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear the integration state, drive `vout` to `vcm`, and clear `valid`.
- `P_ON_A_RISING_PHI1_CROSSING_SAMPLE`: On a rising `phi1` crossing, sample the input deviation from `vcm` into the sampling state.
- `P_ON_THE_FOLLOWING_RISING_PHI2_CROSSING`: On the following rising `phi2` crossing, add `k_int` times the sampled deviation to the integrator state.
- `P_REJECT_OVERLAPPING_PHI1_AND_PHI2_UPDATES`: Reject overlapping `phi1` and `phi2` updates by holding the previous state and lowering `valid` for that cycle.
- `P_EXPOSE_THE_MOST_RECENT_ACCEPTED_PHASE`: Expose the most recent accepted phase pair on `phase_metric` and clamp `vout` to the rails.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `switched_cap_integrator_phase_pair_top.va`, `sample_phase_cell.va`, `integrator_state_cell.va`.
Every supplied `.va` file is editable; do not add or omit files.
