# BBPD Data Edge Alignment

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bbpd_data_edge_alignment_ref.va`: `bbpd_data_edge_alignment_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_RETIMING`: Each rising clk edge captures the current data logic level onto retimed_data, which holds between clock edges.
- `P_EARLY_TRANSITION_UP`: A data transition closer to the upcoming nominal clock edge and outside the deadzone produces an UP pulse of pulse_w duration.
- `P_LATE_TRANSITION_DN`: A data transition closer to the previous nominal clock edge and outside the deadzone produces a DN pulse of pulse_w duration.
- `P_DEADZONE_SUPPRESSION`: Data transitions within deadzone of the relevant nominal clock edge produce neither correction pulse.
- `P_BOTH_DATA_POLARITIES`: Both rising and falling data transitions participate in timing classification.
- `P_MUTUAL_EXCLUSION`: UP and DN are mutually exclusive apart from finite analog transition overlap and use the vdd-to-vss logic range.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bbpd_data_edge_alignment_ref.va`.
Do not add or omit artifacts.
