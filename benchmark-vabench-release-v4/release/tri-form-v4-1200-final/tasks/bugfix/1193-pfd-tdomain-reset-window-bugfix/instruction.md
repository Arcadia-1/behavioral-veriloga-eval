# PFD Tdomain Reset Window Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pfd_tdomain_reset_window.va`: `pfd_tdomain_reset_window`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_LEADING_EDGE_DIRECTION`: A leading `in1` edge asserts `up`, and a leading `in2` edge asserts `dn`.
- `P_RESET_OVERLAP_WINDOW`: After both inputs arrive, both outputs remain asserted for the `ton` reset-overlap window.
- `P_CLEAR_AFTER_RESET_WINDOW`: After the reset-overlap window, both `up` and `dn` clear before the next phase event.
- `P_PFD_OUTPUT_LEVELS`: `up` and `dn` use rail-referenced voltage-coded low/high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pfd_tdomain_reset_window.va`.
Every supplied `.va` file is editable; do not add or omit files.
