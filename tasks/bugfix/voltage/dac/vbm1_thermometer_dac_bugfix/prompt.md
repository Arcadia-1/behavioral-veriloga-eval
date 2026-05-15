# Task: vbm1_thermometer_dac_bugfix

Repair the provided Verilog-A 4-bit binary DAC behavior model. The historical
main120 task id contains `thermometer_dac`, but this source task uses four
binary-weighted voltage-domain code inputs `code_0` through `code_3`, references
`vref` and `vss`, and voltage-domain output `aout`.

Interpret the four code inputs as a 4-bit unsigned code. Drive `aout` linearly
from `vss` to `vref` so code `0` maps to `vss` and code `15` maps to `vref`.
Intermediate codes must be monotonic and use the ideal `code / 15` endpoint
scaling.

Keep the model purely voltage-domain and drive `aout` with `transition`. Do not
use current contributions.
