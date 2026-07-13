# Comparator Offset Calibration Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `comparator_offset_calibration_loop.va`: `comparator_offset_calibration_loop`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ZERO_INITIAL_ESTIMATE`: The signed estimate initializes to zero, the search increment initializes to step_initial, and valid begins low.
- `P_FALLING_EDGE_UPDATE`: The calibration state updates only on falling clk crossings through the midpoint of vdd and vss.
- `P_DECISION_DIRECTION`: At an update, a high dcmpp decreases the estimate by the current step and a low dcmpp increases it by the current step.
- `P_SUCCESSIVE_STEP_HALVING`: The magnitude of the search increment halves after every update, yielding a successive-approximation trajectory.
- `P_SYMMETRIC_DIFFERENTIAL_STIMULUS`: Vinp and vinn remain symmetric around mid-supply and vinp minus vinn equals offset_est.
- `P_VALID_COMPLETION`: Valid remains at vss until iterations updates complete, then rises to vdd and the reported estimate resolves the supplied comparator trip point represented by vos_ref within the search resolution.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `comparator_offset_calibration_loop.va`.
Do not add or omit artifacts.
