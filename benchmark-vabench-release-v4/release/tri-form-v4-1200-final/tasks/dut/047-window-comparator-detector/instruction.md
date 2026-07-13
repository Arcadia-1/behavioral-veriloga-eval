# Window Comparator Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `window_comparator_ref.va`: `window_comparator_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_WINDOW_STATE`: At initialization, out reflects whether vin relative to VSS lies strictly between vlow and vhigh.
- `P_INSIDE_WINDOW_HIGH`: Out is at the VDD rail only while vlow < V(vin,VSS) < vhigh.
- `P_BOUNDARY_EXCLUSION`: Out is at the VSS rail when V(vin,VSS) is equal to or outside either window boundary.
- `P_BIDIRECTIONAL_CROSSINGS`: Crossings of both vlow and vhigh in either direction update the retained in-window decision.
- `P_RAIL_SMOOTHING`: Out is rail-referenced to VDD and VSS with finite transition smoothing set by tedge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `window_comparator_ref.va`.
Do not add or omit artifacts.
