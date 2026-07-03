# Deadband Window

Implement `deadband_window` in `deadband_window.va`.

The module is a voltage-domain DUT with port order `sigin, sigout`. Declare
both ports as `electrical`; `sigin` is the input and `sigout` is the output.

Treat `V(sigin)` as a signed error signal. Drive `sigout` to zero when the
input is within the deadband window, including the two thresholds. Below the
lower threshold, drive the signed residue relative to the lower edge. Above the
upper threshold, drive the signed residue relative to the upper edge. The output
should be continuous at both deadband boundaries.

Provide overridable real parameters `dead_low=-0.1` and `dead_high=0.1`, in
volts, and use the instance-provided values when they are overridden.
