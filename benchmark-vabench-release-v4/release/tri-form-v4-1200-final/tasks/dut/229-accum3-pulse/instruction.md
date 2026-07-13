# Accum3 Pulse

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `accum3_pulse.va`: `accum3_pulse`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIALIZE_THE_INTERNAL_3_BIT_COUNT`: Initialize the internal 3-bit count to 7.
- `P_INCREMENT_THE_COUNT_MODULO_8_ON`: Increment the count modulo 8 on each rising `clk` crossing.
- `P_DRIVE_OUT_HIGH_ONLY_WHEN_THE`: Drive `out` high only when the modulo count is 0.
- `P_DRIVE_OUT_LOW_FOR_ALL_OTHER`: Drive `out` low for all other count values.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `accum3_pulse.va`.
Do not add or omit artifacts.
