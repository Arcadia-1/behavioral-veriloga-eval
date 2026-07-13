# BBPD Data Edge Alignment Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bbpd_data_edge_alignment_ref.va`: `bbpd_data_edge_alignment_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_RETIMING`: Each rising clk edge captures the current data logic level onto retimed_data, which holds between clock edges.
- `P_EARLY_TRANSITION_UP`: A data transition closer to the upcoming nominal clock edge and outside the deadzone produces an UP pulse of pulse_w duration.
- `P_LATE_TRANSITION_DN`: A data transition closer to the previous nominal clock edge and outside the deadzone produces a DN pulse of pulse_w duration.
- `P_DEADZONE_SUPPRESSION`: Data transitions within deadzone of the relevant nominal clock edge produce neither correction pulse.
- `P_BOTH_DATA_POLARITIES`: Both rising and falling data transitions participate in timing classification.
- `P_MUTUAL_EXCLUSION`: UP and DN are mutually exclusive apart from finite analog transition overlap and use the vdd-to-vss logic range.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bbpd_data_edge_alignment_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
