# Multi-channel Sample/Mux/Readout

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sample_mux_readout_top.va`: `sample_mux_readout_top`
- `sample_hold_bank.va`: `sample_hold_bank`
- `mux_controller.va`: `mux_controller`
- `output_driver.va`: `output_driver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_READOUT_RESET_CLEAR`: Reset clears held channels, selector, out, and valid.
- `P_READOUT_SIMULTANEOUS_SAMPLE`: An enabled rising clock captures all four input channels into one coherent held bank.
- `P_READOUT_CHANNEL_ORDER`: Read cycles select held channels in order zero, one, two, three and wrap.
- `P_READOUT_HELD_VALUE`: out equals the held value of the exposed selected channel, independent of later live-input changes.
- `P_READOUT_VALID_TIMING`: valid is high only for read cycles; when read is low out holds and the pointer does not advance.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sample_mux_readout_top.va`, `sample_hold_bank.va`, `mux_controller.va`, `output_driver.va`.
Do not add or omit artifacts.
