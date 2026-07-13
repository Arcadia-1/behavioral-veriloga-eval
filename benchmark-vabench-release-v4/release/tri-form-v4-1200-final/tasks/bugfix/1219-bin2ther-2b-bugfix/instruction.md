# Bin2ther 2b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bin2ther_2b.va`: `bin2ther_2b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INTERPRET_B1_AND_B0_RELATIVE_TO`: Interpret `b1` and `b0` relative to the local rail midpoint.
- `P_DRIVE_T0_AND_T1_HIGH_TOGETHER`: Drive `t0` and `t1` high together when `b1` is high.
- `P_DRIVE_T2_HIGH_WHEN_B0_IS`: Drive `t2` high when `b0` is high.
- `P_DRIVE_EACH_LOW_OUTPUT_TO_THE`: Drive each low output to the local `gnd` rail and each high output to the local `vdd` rail.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bin2ther_2b.va`.
Every supplied `.va` file is editable; do not add or omit files.
