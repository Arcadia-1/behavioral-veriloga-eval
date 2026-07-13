# Muxed Track-hold Array Readout

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `muxed_track_hold_array_top.va`: `muxed_track_hold_array_top`
- `track_hold_cell.va`: `track_hold_cell`
- `readout_mux.va`: `readout_mux`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_CLEAR_ALL_HELD_CHANNEL`: On reset, clear all held channel states, output, channel metric, and `valid`.
- `P_ON_EACH_ENABLED_SAMPLING_CLOCK_EDGE`: On each enabled sampling clock edge, capture all three input channels into separate hold states.
- `P_DECODE_SEL_1_SEL_0_AND`: Decode `sel_1..sel_0` and route the selected held channel to `vout`; invalid code 3 must hold the previous output and clear `valid`.
- `P_EXPOSE_THE_SELECTED_CHANNEL_INDEX_ON`: Expose the selected channel index on `channel_metric` as a voltage-coded metric.
- `P_HOLD_ALL_CHANNEL_SAMPLES_BETWEEN_SAMPLING`: Hold all channel samples between sampling events.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `muxed_track_hold_array_top.va`, `track_hold_cell.va`, `readout_mux.va`.
Do not add or omit artifacts.
