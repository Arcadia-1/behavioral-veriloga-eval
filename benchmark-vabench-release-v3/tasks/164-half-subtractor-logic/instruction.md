# Half Subtractor Logic

## Task Contract
Implement the Verilog-A DUT `half_subtractor_logic.va` for a voltage-coded half-subtractor support cell.

## Public Verilog-A Interface
Provide `module half_subtractor_logic(vin1, vin2, vout_diff, vout_borrow);` with electrical inputs `vin1`, `vin2` and electrical outputs `vout_diff`, `vout_borrow`.

## Public Parameter Contract
This task has no public parameters.

## Required Behavior
Interpret each input as logic 1 above 0.45 V. Drive `vout_diff` with the XOR of the two input bits. Drive `vout_borrow` high only when `vin1` is logic 0 and `vin2` is logic 1. Use 0.9 V for high and 0.0 V for low.

## Modeling Constraints
Use voltage-coded combinational logic with analog output transitions. Do not reverse the borrow direction, use AND as the difference, or drive half-amplitude levels.

## Output Contract
Submit only the completed Verilog-A module in `half_subtractor_logic.va`.
