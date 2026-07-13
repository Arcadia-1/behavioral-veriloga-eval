# SPI Shift Mux

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `spi_shift_mux.va`: `spi_shift_mux`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_LOADS_DEFAULT_WORD`: Initialization and active-high `rst` load the 8-bit word `10110010` with `out7` as the leftmost bit and `out0` as the rightmost bit.
- `P_SHIFT_ON_SCKI_TRANSITIONS`: While reset is inactive, every `scki` transition shifts the register exactly once.
- `P_SHIFT_DIRECTION_AND_SDI_INSERTION`: The shift moves bits toward higher output indexes and inserts `sdi` into the declared end of the register.
- `P_SDO_EXPOSES_SHIFTED_OUT_BIT`: `sdo` exposes the shifted-out `out7` bit rather than another register bit.
- `P_OUTPUT_RAIL_LEVELS`: The parallel outputs and `sdo` are voltage-coded at valid low/high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `spi_shift_mux.va`.
Do not add or omit artifacts.
