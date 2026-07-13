# Clock Divider Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clk_divider_ref.va`: `clk_divider_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET`: Active-low reset clears divider phase and drives clk_out and lock low.
- `P_RATIO_DECODE`: The LSB-first 8-bit code selects the divide ratio, with code zero mapped to ratio one.
- `P_DIVIDED_PERIOD`: For ratios above one, successive clk_out rising edges span the decoded number of clk_in rising edges.
- `P_ODD_RATIO_DUTY`: Odd ratios retain both phases with floor/ceil segment lengths differing by at most one input cycle.
- `P_LOCK_REACQUIRE`: lock asserts after one complete output period and clears/reacquires when the ratio changes.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clk_divider_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
