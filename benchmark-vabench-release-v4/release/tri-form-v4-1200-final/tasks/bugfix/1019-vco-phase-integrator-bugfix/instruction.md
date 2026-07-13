# VCO Phase Integrator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `vco_phase_integrator.va`: `vco_phase_integrator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PERIODIC_PHASE_UPDATE`: Phase state updates on the public 1 ns periodic schedule by 0.03 plus 0.09 times vctrl.
- `P_WRAPPED_PHASE_RANGE`: The observable phase remains in the normalized range from 0 inclusive to 1 exclusive.
- `P_WRAP_TOGGLES_CLOCK`: Each phase wrap by one cycle toggles the voltage-coded clock between 0 V and 0.9 V.
- `P_CONTROLLED_EDGE_RATE`: A sustained higher vctrl produces more clock toggles over the same observation interval than a sustained lower vctrl.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `vco_phase_integrator.va`.
Every supplied `.va` file is editable; do not add or omit files.
