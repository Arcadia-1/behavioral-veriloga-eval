# Full Subtractor Logic

## Task Contract
Implement the Verilog-A DUT `full_subtractor_logic.va` for a voltage-coded one-bit full subtractor support cell.

## Public Verilog-A Interface
Provide `module full_subtractor_logic(vin1, vin2, vin_borrow, vout_diff, vout_borrow);` with electrical inputs `vin1`, `vin2`, `vin_borrow` and electrical outputs `vout_diff`, `vout_borrow`.

## Public Parameter Contract
This task has no public parameters.

## Required Behavior
Interpret each input as logic 1 above 0.45 V. Drive `vout_diff` with the odd parity of minuend, subtrahend, and borrow-in. Drive `vout_borrow` high when the subtrahend plus borrow-in exceeds the minuend. Use 0.9 V for high and 0.0 V for low.

## Modeling Constraints
Use voltage-coded combinational logic with analog output transitions. Do not ignore borrow-in, invert the difference, or replace the borrow rule with a majority of asserted inputs.

## Output Contract
Submit only the completed Verilog-A module in `full_subtractor_logic.va`.
