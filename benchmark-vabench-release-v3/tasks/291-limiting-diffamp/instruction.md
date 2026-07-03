# Limiting Diffamp

Implement `limiting_diffamp` in `limiting_diffamp.va`.

The module is a voltage-domain DUT with port order `sigin_p, sigin_n, sigout`.
Declare all ports as `electrical`; `sigin_p` and `sigin_n` are inputs and
`sigout` is the output.

Use the differential input voltage from `sigin_p` to `sigin_n`. The small-signal
output is the differential input multiplied by `gain`. Hard-limit the output to
the lower and upper output rails, preserving differential polarity in the
linear region and saturating cleanly when either rail is reached.

Provide overridable real parameters `gain=4.0`, `sigout_low=-0.75`, and
`sigout_high=0.75`. The rail parameters are voltages and `gain` is
dimensionless.
