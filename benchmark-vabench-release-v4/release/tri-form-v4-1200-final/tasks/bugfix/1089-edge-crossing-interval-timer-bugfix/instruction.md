# Edge Crossing Interval Timer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cross_interval_163p333_ref.va`: `cross_interval_163p333_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_A_EDGE_ARMS`: A rising a crossing arms a fresh measurement and clears seen_out until completion.
- `P_FIRST_B_EDGE_CAPTURES`: The first rising b crossing after an armed a edge captures their elapsed time; b edges before arming do not complete a measurement.
- `P_DELAY_NORMALIZATION`: Delay_out equals the VDD-to-VSS rail span multiplied by measured delay in picoseconds divided by scale_ps.
- `P_COMPLETION_MARKER`: Seen_out is rail-high after a valid a-then-b capture and rail-low while a newly armed measurement is incomplete.
- `P_SINGLE_CAPTURE_PER_ARM`: Additional b crossings after completion do not change delay_out until the next rising a edge rearms the timer.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cross_interval_163p333_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
