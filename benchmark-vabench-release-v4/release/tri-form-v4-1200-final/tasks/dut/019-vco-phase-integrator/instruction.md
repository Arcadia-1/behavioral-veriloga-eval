# VCO Phase Integrator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `vco_phase_integrator.va`: `vco_phase_integrator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PERIODIC_PHASE_UPDATE`: Phase state updates on the public 1 ns periodic schedule by 0.03 plus 0.09 times vctrl.
- `P_WRAPPED_PHASE_RANGE`: The observable phase remains in the normalized range from 0 inclusive to 1 exclusive.
- `P_WRAP_TOGGLES_CLOCK`: Each phase wrap by one cycle toggles the voltage-coded clock between 0 V and 0.9 V.
- `P_CONTROLLED_EDGE_RATE`: A sustained higher vctrl produces more clock toggles over the same observation interval than a sustained lower vctrl.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `vco_phase_integrator.va`.
Do not add or omit artifacts.
