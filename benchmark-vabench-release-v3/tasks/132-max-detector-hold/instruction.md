# Max Detector Hold

## Task Contract
Implement the Verilog-A DUT `max_detector_hold.va` for a continuous maximum detector with hold behavior.

## Form-Specific Requirements
This is a single-DUT task. The testbench is a public verification scenario, not a table of values to copy into the DUT.

## Public Verilog-A Interface
Provide `module max_detector_hold(vin, vout);` with electrical input `vin` and electrical output `vout`.

## Public Parameter Contract
This task has no public parameters.

## Required Behavior
Initialize the held value from the input at the start of simulation. During transient simulation, update the held value only when `V(vin)` exceeds the previously held maximum. Drive `vout` to the held maximum, so `vout` is monotone nondecreasing even when `vin` falls.

## Modeling Constraints
Use analog state in a Spectre-compatible Verilog-A model. Do not implement a resettable peak detector, a minimum detector, a passthrough follower, or a final-value-only detector.

## Output Contract
Submit only the completed Verilog-A module in `max_detector_hold.va`.
