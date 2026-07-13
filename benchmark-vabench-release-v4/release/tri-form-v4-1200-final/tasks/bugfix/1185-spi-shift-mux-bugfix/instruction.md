# SPI Shift Mux Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `spi_shift_mux.va`: `spi_shift_mux`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_LOADS_DEFAULT_WORD`: Initialization and active-high `rst` load the 8-bit word `10110010` with `out7` as the leftmost bit and `out0` as the rightmost bit.
- `P_SHIFT_ON_SCKI_TRANSITIONS`: While reset is inactive, every `scki` transition shifts the register exactly once.
- `P_SHIFT_DIRECTION_AND_SDI_INSERTION`: The shift moves bits toward higher output indexes and inserts `sdi` into the declared end of the register.
- `P_SDO_EXPOSES_SHIFTED_OUT_BIT`: `sdo` exposes the shifted-out `out7` bit rather than another register bit.
- `P_OUTPUT_RAIL_LEVELS`: The parallel outputs and `sdo` are voltage-coded at valid low/high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `spi_shift_mux.va`.
Every supplied `.va` file is editable; do not add or omit files.
