# Multi-channel Sample/Mux/Readout Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sample_mux_readout_top.va`: `sample_mux_readout_top`
- `sample_hold_bank.va`: `sample_hold_bank`
- `mux_controller.va`: `mux_controller`
- `output_driver.va`: `output_driver`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_READOUT_RESET_CLEAR`: Reset clears held channels, selector, out, and valid.
- `P_READOUT_SIMULTANEOUS_SAMPLE`: An enabled rising clock captures all four input channels into one coherent held bank.
- `P_READOUT_CHANNEL_ORDER`: Read cycles select held channels in order zero, one, two, three and wrap.
- `P_READOUT_HELD_VALUE`: out equals the held value of the exposed selected channel, independent of later live-input changes.
- `P_READOUT_VALID_TIMING`: valid is high only for read cycles; when read is low out holds and the pointer does not advance.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sample_mux_readout_top.va`, `sample_hold_bank.va`, `mux_controller.va`, `output_driver.va`.
Every supplied `.va` file is editable; do not add or omit files.
