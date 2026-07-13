# Muxed Track-hold Array Readout Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `muxed_track_hold_array_top.va`: `muxed_track_hold_array_top`
- `track_hold_cell.va`: `track_hold_cell`
- `readout_mux.va`: `readout_mux`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_CLEAR_ALL_HELD_CHANNEL`: On reset, clear all held channel states, output, channel metric, and `valid`.
- `P_ON_EACH_ENABLED_SAMPLING_CLOCK_EDGE`: On each enabled sampling clock edge, capture all three input channels into separate hold states.
- `P_DECODE_SEL_1_SEL_0_AND`: Decode `sel_1..sel_0` and route the selected held channel to `vout`; invalid code 3 must hold the previous output and clear `valid`.
- `P_EXPOSE_THE_SELECTED_CHANNEL_INDEX_ON`: Expose the selected channel index on `channel_metric` as a voltage-coded metric.
- `P_HOLD_ALL_CHANNEL_SAMPLES_BETWEEN_SAMPLING`: Hold all channel samples between sampling events.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `muxed_track_hold_array_top.va`, `track_hold_cell.va`, `readout_mux.va`.
Every supplied `.va` file is editable; do not add or omit files.
