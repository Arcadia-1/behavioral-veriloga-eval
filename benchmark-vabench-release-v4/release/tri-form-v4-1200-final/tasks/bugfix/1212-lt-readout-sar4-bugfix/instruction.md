# LT Readout SAR4 Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `lt_readout_sar4.va`: `lt_readout_sar4`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CONTINUOUSLY_DECODE_D0_D3_AS_AN`: Continuously decode `d0..d3` as an unsigned binary code with `d0` as LSB and `d3` as MSB. Drive `vout` to the readout level `code * vref / 16`. The output should update when the voltage-coded input bits cross the threshold.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `lt_readout_sar4.va`.
Every supplied `.va` file is editable; do not add or omit files.
