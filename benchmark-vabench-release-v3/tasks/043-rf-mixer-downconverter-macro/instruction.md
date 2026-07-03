# RF Mixer Downconverter Macro

Implement a voltage-domain RF mixer/downconverter macromodel.

## Public Interface

Declare module `rf_mixer_downconverter_macro` with positional ports `clk, rst,
vin, out, metric`. All ports are electrical.

`clk` is the LO-polarity waveform, `rst` is an active-high voltage-coded reset,
`vin` is an RF input envelope centered around common mode, `out` is the
baseband output, and `metric` indicates active conversion.

## Public Parameter Contract

Provide these overrideable public parameters:

- `tr = 80p`: transition time used for smoothed voltage contributions.
- `vth = 0.45 V`: threshold for voltage-coded logic decisions.
- `conv_gain = 1.25`: conversion gain applied to the RF envelope deviation.

## Functional Contract

When reset is asserted, drive `out` to the 0.45 V common-mode level and drive
`metric` low. After reset releases, interpret `clk` as the LO polarity. A high
LO polarity should preserve the sign of the input deviation from common mode,
and a low LO polarity should invert that sign. The converted baseband output
should remain bounded in the 0 V to 0.9 V signal range. Drive `metric` high
while conversion is active.

## Modeling Constraints

Return only `rf_mixer_downconverter_macro.va`. Use voltage contributions only.
Use behavioral state and `transition(...)` smoothing where the target output can
change discontinuously. Do not modify or emit the support testbench, add checker
logic, hard-code private waveform sample points, add simulator-private side
channels, use current contributions, transistor-level devices, S-parameters,
AC/noise-analysis behavior, communication modem algorithms, or full link-level
decoding.
