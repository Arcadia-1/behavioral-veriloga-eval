# Differential Deadband Amplifier

Implement `differential_deadband` in `differential_deadband.va`.

The module is a voltage-domain DUT with port order `sigin_p, sigin_n, sigout`.
Declare all ports as `electrical`; `sigin_p` and `sigin_n` are inputs and
`sigout` is the output.

Use the differential input voltage from `sigin_p` to `sigin_n`. Inside the
deadband window, including the two thresholds, drive the leakage output level.
Below the lower threshold, drive the low-side signed differential residue
scaled by `gain` and offset by the leakage level. Above the upper threshold,
drive the high-side signed differential residue scaled by the same `gain` and
offset by the leakage level. Preserve differential polarity and continuity at
the deadband boundaries.

Provide overridable real parameters `dead_low=-0.1`, `dead_high=0.1`, `gain=1`,
and `leak=0`. The threshold and leakage values are voltages; `gain` is
dimensionless.
