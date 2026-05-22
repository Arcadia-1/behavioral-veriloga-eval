# Task: vbm1_simple_binary_voltage_dac_4b_bugfix

Repair the provided Verilog-A 4-bit binary-weighted voltage DAC behavior model.
The circuit uses four binary-weighted voltage-domain code inputs `code_0`
through `code_3`, references `vref` and `vss`, and voltage-domain output `aout`.

Interpret the four code inputs as a 4-bit unsigned code. Drive `aout` linearly
from `vss` to `vref` so code `0` maps to `vss` and code `15` maps to `vref`.
Intermediate codes must be monotonic and use the ideal `code / 15` endpoint
scaling.

Keep the model purely voltage-domain and drive `aout` with `transition`. Do not
use current contributions.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
