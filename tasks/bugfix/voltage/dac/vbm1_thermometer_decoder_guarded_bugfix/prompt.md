# Task: vbm1_thermometer_decoder_guarded_bugfix

Repair the provided Verilog-A guarded thermometer decoder. The DUT has
voltage-domain binary inputs `b0` and `b1`, enable input `en`, and
voltage-domain outputs `th0` through `th3`.

When `en` is low, all thermometer outputs must be low. When `en` is high,
decode the two-bit code into cumulative thermometer outputs: code `1` drives
only `th0`, code `2` drives `th0` and `th1`, and code `3` drives `th0`, `th1`,
and `th2`. `th3` remains low for this guarded two-bit task.

Keep the model purely voltage-domain and drive outputs with `transition`. Do
not use current contributions.
