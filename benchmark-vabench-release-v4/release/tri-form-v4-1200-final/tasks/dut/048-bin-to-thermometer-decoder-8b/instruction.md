# Binary To Thermometer Decoder 8b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bin_to_therm_8b.va`: `bin_to_therm_8b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_UNSIGNED_CODE`: The voltage-coded b[7:0] bus decodes as an unsigned integer from 0 through 255 with b[7] as the most significant bit.
- `P_DISABLED_ALL_LOW`: When en is below vth, every th[255:0] output is low independent of the binary code.
- `P_PREFIX_THERMOMETER`: When enabled, exactly code outputs form a contiguous high prefix from th[0] through th[code-1], with all higher indices low.
- `P_ENDPOINT_CODES`: Enabled code 0 drives all outputs low; enabled code 255 drives th[0] through th[254] high and leaves th[255] low.
- `P_LOGIC_LEVELS`: High thermometer elements approach vdd and low elements approach 0 V with finite transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bin_to_therm_8b.va`.
Do not add or omit artifacts.
