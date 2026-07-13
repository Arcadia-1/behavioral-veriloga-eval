# Binary To Thermometer Decoder 8b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bin_to_therm_8b.va`: `bin_to_therm_8b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_UNSIGNED_CODE`: The voltage-coded b[7:0] bus decodes as an unsigned integer from 0 through 255 with b[7] as the most significant bit.
- `P_DISABLED_ALL_LOW`: When en is below vth, every th[255:0] output is low independent of the binary code.
- `P_PREFIX_THERMOMETER`: When enabled, exactly code outputs form a contiguous high prefix from th[0] through th[code-1], with all higher indices low.
- `P_ENDPOINT_CODES`: Enabled code 0 drives all outputs low; enabled code 255 drives th[0] through th[254] high and leaves th[255] low.
- `P_LOGIC_LEVELS`: High thermometer elements approach vdd and low elements approach 0 V with finite transition smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bin_to_therm_8b.va`.
Every supplied `.va` file is editable; do not add or omit files.
