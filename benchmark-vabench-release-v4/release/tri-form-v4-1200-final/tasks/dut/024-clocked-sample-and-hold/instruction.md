# Clocked Sample And Hold

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sample_hold.va`: `sample_hold`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_EDGE_SAMPLE`: OUT acquires the IN voltage present at each rising CLK crossing through vth, subject only to transition smoothing.
- `P_INTERSAMPLE_HOLD`: OUT retains the most recently sampled value between rising CLK crossings.
- `P_NO_HIGH_PHASE_TRACKING`: Changes on IN while CLK remains high do not make OUT transparent before the next rising crossing.
- `P_LOCAL_RAIL_REFERENCE`: The held analog voltage is driven as a smooth voltage-domain output referenced to the local VDD and VSS rails.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sample_hold.va`.
Do not add or omit artifacts.
