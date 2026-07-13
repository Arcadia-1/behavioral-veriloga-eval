# VA Lx DAC Ideal 4b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `va_lx_dac_ideal_4b.va`: `va_lx_dac_ideal_4b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_READY_CLOCKED_SAMPLING`: Only rising crossings of `rdy` through `vth` sample the four input bits; `aout` holds between ready events.
- `P_BINARY_BIT_ORDER`: `din4` is the MSB and `din1` is the LSB of the sampled 4-bit unipolar code.
- `P_VDD_SCALED_DAC_OUTPUT`: The sampled binary fraction is scaled by `vdd` and driven smoothly on `aout`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `va_lx_dac_ideal_4b.va`.
Do not add or omit artifacts.
