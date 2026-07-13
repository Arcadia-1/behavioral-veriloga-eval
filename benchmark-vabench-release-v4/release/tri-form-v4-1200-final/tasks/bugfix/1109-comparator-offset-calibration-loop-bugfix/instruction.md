# Comparator Offset Calibration Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `comparator_offset_calibration_loop.va`: `comparator_offset_calibration_loop`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ZERO_INITIAL_ESTIMATE`: The signed estimate initializes to zero, the search increment initializes to step_initial, and valid begins low.
- `P_FALLING_EDGE_UPDATE`: The calibration state updates only on falling clk crossings through the midpoint of vdd and vss.
- `P_DECISION_DIRECTION`: At an update, a high dcmpp decreases the estimate by the current step and a low dcmpp increases it by the current step.
- `P_SUCCESSIVE_STEP_HALVING`: The magnitude of the search increment halves after every update, yielding a successive-approximation trajectory.
- `P_SYMMETRIC_DIFFERENTIAL_STIMULUS`: Vinp and vinn remain symmetric around mid-supply and vinp minus vinn equals offset_est.
- `P_VALID_COMPLETION`: Valid remains at vss until iterations updates complete, then rises to vdd and the reported estimate resolves the supplied comparator trip point represented by vos_ref within the search resolution.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `comparator_offset_calibration_loop.va`.
Every supplied `.va` file is editable; do not add or omit files.
