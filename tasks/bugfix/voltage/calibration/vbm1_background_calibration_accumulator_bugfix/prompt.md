# Task: vbm1_background_calibration_accumulator_bugfix

Repair the provided Verilog-A background calibration accumulator. The DUT has
voltage-domain inputs `clk`, `rst`, and `err`, plus one voltage-domain output
`accum`.

On each rising edge of `clk`, reset must force `accum` back to `0.45 V`.
Otherwise, `err` above threshold increments the accumulator by `0.04 V`, and
`err` below threshold decrements it by `0.04 V`. Clamp the accumulator to the
range `[0.05 V, 0.85 V]`.

Keep the model purely voltage-domain and drive `accum` with `transition`. Do
not use current contributions.
