# Bidirectional Hybrid Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bidirectional_hybrid_macro.va`: `bidirectional_hybrid_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEAR`: Reset centers the continuous sum and difference outputs and clears sampled metrics and balance qualification.
- `P_SUM_DIFF_MAPPING`: sum_out and diff_out implement the clipped common and differential mappings of port_a and port_b around vcm.
- `P_TRIM_RESPONSE`: The signed three-bit trim correction shifts sum and difference in opposite directions by trim_lsb per code.
- `P_DIRECTIONAL_METRICS`: At rising clock edges forward and reverse metrics reconstruct the directional components from the mapped sum and difference outputs.
- `P_BALANCE_QUALIFICATION`: balance_ok asserts only after two consecutive metric updates whose directional mismatch is within balance_tol.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bidirectional_hybrid_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
