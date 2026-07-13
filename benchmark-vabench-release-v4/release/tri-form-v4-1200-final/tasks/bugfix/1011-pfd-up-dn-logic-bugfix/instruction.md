# PFD Up DN Logic Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pfd_updn.va`: `pfd_updn`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_REF_SETS_UP`: A rising REF edge asserts UP, and falling REF edges do not set either output.
- `P_DIV_SETS_DN`: A rising DIV edge asserts DN, and falling DIV edges do not set either output.
- `P_RESET_RACE_CLEAR`: If a rising edge arrives while the opposite output state is already high, both UP and DN clear immediately for REF-leading and DIV-leading orderings.
- `P_NO_PERSISTENT_OVERLAP`: UP and DN are not intentionally held high together beyond finite transition smoothing overlap.
- `P_RAIL_REFERENCE`: UP and DN high levels track the local VDD rail and low levels track the local VSS rail.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pfd_updn.va`.
Every supplied `.va` file is editable; do not add or omit files.
