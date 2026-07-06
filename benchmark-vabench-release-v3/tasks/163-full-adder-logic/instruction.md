# Full Adder Logic

## Task Contract
Implement the Verilog-A DUT `full_adder_logic.va` for a voltage-coded one-bit full adder support cell.

## Public Verilog-A Interface
Provide `module full_adder_logic(vin1, vin2, vin_carry, vout_sum, vout_carry);` with electrical inputs `vin1`, `vin2`, `vin_carry` and electrical outputs `vout_sum`, `vout_carry`.

## Public Parameter Contract
This task has no public parameters.

## Required Behavior
Interpret each input as logic 1 above 0.45 V. Drive `vout_sum` high when the number of asserted inputs is odd, and drive `vout_carry` high when at least two inputs are asserted. Use 0.9 V for high and 0.0 V for low.

## Modeling Constraints
Use voltage-coded combinational logic with analog voltage contributions. Do not ignore carry-in, use even parity for the sum, or require exactly three asserted inputs for carry.

## Output Contract
Submit only the completed Verilog-A module in `full_adder_logic.va`.
