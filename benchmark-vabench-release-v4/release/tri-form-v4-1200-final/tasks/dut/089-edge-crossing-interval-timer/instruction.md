# Edge Crossing Interval Timer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cross_interval_163p333_ref.va`: `cross_interval_163p333_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_A_EDGE_ARMS`: A rising a crossing arms a fresh measurement and clears seen_out until completion.
- `P_FIRST_B_EDGE_CAPTURES`: The first rising b crossing after an armed a edge captures their elapsed time; b edges before arming do not complete a measurement.
- `P_DELAY_NORMALIZATION`: Delay_out equals the VDD-to-VSS rail span multiplied by measured delay in picoseconds divided by scale_ps.
- `P_COMPLETION_MARKER`: Seen_out is rail-high after a valid a-then-b capture and rail-low while a newly armed measurement is incomplete.
- `P_SINGLE_CAPTURE_PER_ARM`: Additional b crossings after completion do not change delay_out until the next rising a edge rearms the timer.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cross_interval_163p333_ref.va`.
Do not add or omit artifacts.
