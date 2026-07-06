# Half Adder Logic

## Task Contract
Implement the Verilog-A DUT `half_adder_logic.va` for a voltage-coded half-adder support cell used in AMS control paths.

## Public Verilog-A Interface
Provide `module half_adder_logic(vin1, vin2, vout_sum, vout_carry);` with electrical inputs `vin1`, `vin2` and electrical outputs `vout_sum`, `vout_carry`.

## Public Parameter Contract
This task has no public parameters.

## Required Behavior
Interpret each input as logic 1 when its voltage is above 0.45 V and logic 0 otherwise. Drive `vout_sum` with the XOR of the two input bits and `vout_carry` with their AND. Use 0.9 V for logic high and 0.0 V for logic low.

## Modeling Constraints
Use voltage-coded logic inside an analog block and smooth output transitions. Do not implement OR as the sum bit, OR as the carry bit, half-amplitude levels, or a time-specific truth table.

## Output Contract
Submit only the completed Verilog-A module in `half_adder_logic.va`.
