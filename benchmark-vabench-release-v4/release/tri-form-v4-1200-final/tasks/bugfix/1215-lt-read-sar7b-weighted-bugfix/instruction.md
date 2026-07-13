# LT Read SAR7B Weighted Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `lt_read_sar7b_weighted.va`: `lt_read_sar7b_weighted`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CONTINUOUSLY_DRIVE`: Continuously drive:
- `P_TEXT_VOUT_VREF_VREF_D7_D6`: ```text vout = -vref + vref * (d7 + d6/2 + d5/4 + d4/8 + d3/16 + d2/32 + d1/64 + d0/128) ```
- `P_WHERE_EACH_D_TERM_IS_1`: where each `d` term is `1` when the corresponding input voltage is above `vth` and `0` otherwise.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `lt_read_sar7b_weighted.va`.
Every supplied `.va` file is editable; do not add or omit files.
