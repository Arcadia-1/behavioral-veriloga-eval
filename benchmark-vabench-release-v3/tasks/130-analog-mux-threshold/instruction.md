# Analog Mux Threshold

## Task Contract
Implement the Verilog-A DUT `analog_mux_threshold.va` for a voltage-controlled 2:1 analog multiplexer.

## Form-Specific Requirements
This is a single-DUT task. The public and private testbenches are verification scenarios; do not hard-code their waveforms or stop times.

## Public Verilog-A Interface
Provide `module analog_mux_threshold(vin1, vin2, vsel, vout);` with electrical input ports `vin1`, `vin2`, `vsel` and electrical output port `vout`.

## Public Parameter Contract
Expose `parameter real vth = 0.45;` as the select threshold. Testbenches may override this parameter.

## Required Behavior
When `V(vsel)` is above `vth`, drive `vout` from `vin1`. When `V(vsel)` is below `vth`, drive `vout` from `vin2`. The selection must update on both rising and falling threshold crossings, and the initial selection must match the initial `vsel` level.

## Modeling Constraints
Use a voltage-domain behavioral model with threshold-crossing events or equivalent continuous logic. Do not average the two inputs, ignore falling select crossings, or add hidden state unrelated to the mux selection.

## Output Contract
Submit only the completed Verilog-A module in `analog_mux_threshold.va`.
