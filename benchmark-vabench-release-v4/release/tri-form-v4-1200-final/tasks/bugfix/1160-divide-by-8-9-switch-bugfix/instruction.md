# Divide By 8 9 Switch Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `divide_by_8_9_switch.va`: `divide_by_8_9_switch`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MODULUS_SWITCHING_ON_MC_EDGES`: `mc` crossings switch the divider between divide-by-8 and divide-by-9 operation and can restore divide-by-8 after divide-by-9.
- `P_DIVIDER_DUTY_WINDOW`: The divider output high window spans the specified count interval for the active modulus.
- `P_OUTPUT_RAIL_LEVEL`: `out` uses the declared high and low output levels without amplitude scaling.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `divide_by_8_9_switch.va`.
Every supplied `.va` file is editable; do not add or omit files.
