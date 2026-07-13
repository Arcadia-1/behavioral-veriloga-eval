# Sigma-delta Modulator Mini Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sigma_delta_top.va`: `sigma_delta_top`
- `integrator_state.va`: `integrator_state`
- `sd_comparator.va`: `sd_comparator`
- `feedback_dac.va`: `feedback_dac`
- `decimator_lite.va`: `decimator_lite`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEAR`: Reset clears the loop state, output bit, and decimator result.
- `P_FEEDBACK_STATE_UPDATE`: Each rising clock edge updates the bounded integrator from VIN and the previous feedback bit.
- `P_COMPARATOR_DECISION`: The output bit reflects the updated state relative to VCM.
- `P_DECIMATOR_WINDOW`: The four-bit result reports the saturated high-bit count for each complete 16-sample window.
- `P_STATE_BOUNDED`: The public state metric remains within the configured state limit.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sigma_delta_top.va`, `integrator_state.va`, `sd_comparator.va`, `feedback_dac.va`, `decimator_lite.va`.
Every supplied `.va` file is editable; do not add or omit files.
