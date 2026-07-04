# Three Way Threshold Mux

## Task Contract
Implement the Verilog-A DUT `three_way_threshold_mux.va` for a three-input analog mux controlled by a differential threshold window.

## Form-Specific Requirements
This is a single-DUT mixed-signal selector task. The output must depend on the instantaneous differential control voltage, not on a hard-coded time schedule.

## Public Verilog-A Interface
Provide `module three_way_threshold_mux(sigin1, sigin2, sigin3, cntrlp, cntrlm, sigout);` with electrical inputs `sigin1`, `sigin2`, `sigin3`, `cntrlp`, `cntrlm` and electrical output `sigout`.

## Public Parameter Contract
Expose `parameter real sigth_high = 1;` and `parameter real sigth_low = -1;`. Testbenches may override these thresholds.

## Required Behavior
Use `V(cntrlp, cntrlm)` as the control signal. Select `sigin1` when the control is below `sigth_low`, select `sigin2` when it is inside the inclusive threshold window, and select `sigin3` when it is above `sigth_high`.

## Modeling Constraints
Use direct analog selection with the differential control input. Do not use only one control terminal, swap the low/high selections, or remove the middle selection region.

## Output Contract
Submit only the completed Verilog-A module in `three_way_threshold_mux.va`.
