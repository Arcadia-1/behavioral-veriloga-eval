# VA LX ADC Ideal 4b

## Task Contract
Implement the Verilog-A DUT `va_lx_adc_ideal_4b.va` for a sampled 4-bit successive-approximation ADC model with voltage-coded output bits.

## Public Verilog-A Interface
Provide `module va_lx_adc_ideal_4b(vin, clks, d1, d2, d3, d4);` with electrical inputs `vin`, `clks` and electrical outputs `d1`, `d2`, `d3`, `d4`.

## Public Parameter Contract
Expose `parameter real vdd = 1;`. Testbenches may override this parameter.

## Required Behavior
Sample `vin` while `clks` is high relative to `vdd/2`. On the falling clock edge, perform a 4-bit binary-search conversion: start with a threshold at `vdd/2`, emit MSB `d4`, then move the threshold by successively halved steps for `d3`, `d2`, and `d1`. Drive output bits as voltage-coded 1.0 or 0.0 levels.

## Modeling Constraints
Use sampled conversion behavior, not a continuously tracking comparator bank. Do not invert the MSB decision, use the wrong first step, or swap the output bit order.

## Output Contract
Submit only the completed Verilog-A module in `va_lx_adc_ideal_4b.va`.
