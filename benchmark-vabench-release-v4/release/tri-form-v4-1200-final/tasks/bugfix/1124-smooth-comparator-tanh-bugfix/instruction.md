# Smooth Comparator Tanh Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `smooth_comparator_tanh.va`: `smooth_comparator_tanh`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_TANH_TRANSFER`: Drive `sigout` as `0.5 * (high - low) * tanh(comp_slope * (V(sigin, sigref) - offset)) + 0.5 * (high + low)`.
- `P_INPUT_POLARITY`: A larger `V(sigin, sigref)` must move the output toward `high`, not toward `low`.
- `P_SMOOTH_TRANSITION`: The output must transition smoothly between `low` and `high` according to the tanh slope, not as a hard switch.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `smooth_comparator_tanh.va`.
Every supplied `.va` file is editable; do not add or omit files.
