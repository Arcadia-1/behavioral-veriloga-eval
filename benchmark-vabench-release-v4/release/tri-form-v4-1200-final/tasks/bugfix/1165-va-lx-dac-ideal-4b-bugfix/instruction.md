# VA Lx DAC Ideal 4b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `va_lx_dac_ideal_4b.va`: `va_lx_dac_ideal_4b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_READY_CLOCKED_SAMPLING`: Only rising crossings of `rdy` through `vth` sample the four input bits; `aout` holds between ready events.
- `P_BINARY_BIT_ORDER`: `din4` is the MSB and `din1` is the LSB of the sampled 4-bit unipolar code.
- `P_VDD_SCALED_DAC_OUTPUT`: The sampled binary fraction is scaled by `vdd` and driven smoothly on `aout`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `va_lx_dac_ideal_4b.va`.
Every supplied `.va` file is editable; do not add or omit files.
