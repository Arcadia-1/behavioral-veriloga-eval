# Masked Config Update 32b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `masked_config_update_32b.va`: `masked_config_update_32b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MASKED_SELECTION`: For each bit N, out_cfg[N] equals new_cfg[N] when mask[N] is high and equals old_cfg[N] when mask[N] is low.
- `P_ZERO_MASK_IDENTITY`: With every mask bit low, the complete output word equals old_cfg.
- `P_FULL_MASK_REPLACEMENT`: With every mask bit high, the complete output word equals new_cfg.
- `P_BIT_INDEPENDENCE`: Changing mask or data bit N affects only out_cfg[N]; bus indices are neither reversed nor shifted.
- `P_OUTPUT_LEVELS`: Each output bit uses 0 V for logic low and vdd for logic high with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `masked_config_update_32b.va`.
Every supplied `.va` file is editable; do not add or omit files.
