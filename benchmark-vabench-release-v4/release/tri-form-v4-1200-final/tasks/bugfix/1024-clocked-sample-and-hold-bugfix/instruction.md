# Clocked Sample And Hold Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sample_hold.va`: `sample_hold`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_EDGE_SAMPLE`: OUT acquires the IN voltage present at each rising CLK crossing through vth, subject only to transition smoothing.
- `P_INTERSAMPLE_HOLD`: OUT retains the most recently sampled value between rising CLK crossings.
- `P_NO_HIGH_PHASE_TRACKING`: Changes on IN while CLK remains high do not make OUT transparent before the next rising crossing.
- `P_LOCAL_RAIL_REFERENCE`: The held analog voltage is driven as a smooth voltage-domain output referenced to the local VDD and VSS rails.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sample_hold.va`.
Every supplied `.va` file is editable; do not add or omit files.
