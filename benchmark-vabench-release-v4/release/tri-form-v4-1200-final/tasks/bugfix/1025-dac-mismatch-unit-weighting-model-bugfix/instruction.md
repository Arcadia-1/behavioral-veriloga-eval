# DAC Mismatch Unit Weighting Model Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dac_mismatch_unit_weighting_model.va`: `dac_mismatch_unit_weighting_model`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ZERO_AND_FULL_SCALE`: All-zero input maps to vlo and all-active input maps to vhi after transition settling.
- `P_NONIDEAL_WEIGHT_SUM`: Inputs b0 through b3 contribute fixed positive weights 1.00, 2.02, 3.96, and 8.08 normalized by their all-active sum.
- `P_LOGIC_THRESHOLD`: Each bit is independently interpreted using the public fixed 0.45 V decision threshold.
- `P_BOUNDED_OUTPUT`: For every input pattern, the settled output remains within the vlo-to-vhi interval.
- `P_MISMATCH_OBSERVABILITY`: Single-bit output increments preserve the stated nonideal weighting rather than ideal powers-of-two weighting.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dac_mismatch_unit_weighting_model.va`.
Every supplied `.va` file is editable; do not add or omit files.
