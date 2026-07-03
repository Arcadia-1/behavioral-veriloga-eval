# Deadband Voltage

Implement `deadband_voltage` in `deadband_voltage.va`.

The module is a voltage-domain DUT with port order `sigin, sigout`. Declare
both ports as `electrical`; `sigin` is the input and `sigout` is the output.

Treat `V(sigin)` as a signed signal to be shaped by a zero-output deadband
around zero. Inside the threshold window, including both edges, drive `sigout`
to zero. Below the lower threshold, drive the signed excess below the lower
edge. Above the upper threshold, drive the signed excess above the upper edge.
The output should preserve sign and be continuous at the two thresholds.

Provide overridable real parameters `sigin_dead_low=-0.25` and
`sigin_dead_high=0.25`, in volts.
