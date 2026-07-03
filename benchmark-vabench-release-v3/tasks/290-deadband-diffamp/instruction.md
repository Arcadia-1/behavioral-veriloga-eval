# Deadband Diffamp

Implement `deadband_diffamp` in `deadband_diffamp.va`.

The module is a voltage-domain DUT with port order `sigin_p, sigin_n, sigout`.
Declare all ports as `electrical`; `sigin_p` and `sigin_n` are inputs and
`sigout` is the output.

Use the differential input voltage from `sigin_p` to `sigin_n`. Inside the
deadband window, including both thresholds, drive the leakage output level.
Below the lower threshold, drive the low-side signed differential residue using
the low-side gain and add the leakage level. Above the upper threshold, drive
the high-side signed differential residue using the high-side gain and add the
leakage level. This task intentionally uses asymmetric low-side and high-side
gain parameters.

Provide overridable real parameters `sigin_dead_low=-0.1`,
`sigin_dead_high=0.1`, `sigout_leak=0.02`, `gain_low=2.0`, and
`gain_high=3.0`. Threshold and leakage values are voltages; gains are
dimensionless.
