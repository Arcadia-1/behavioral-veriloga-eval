# Segmented DAC

Implement a mixed binary/thermometer segmented voltage DAC.

## Public Interface

Declare module `segmented_dac` with positional ports `b0, b1, t0, t1, t2,
vref, vss, aout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: digital decision threshold for binary and thermometer
  controls.
- `tr = 500 ps`: output transition smoothing time.

## Functional Contract

Treat `b0` and `b1` as binary LSB controls with weights 1 and 2. Treat
`t0`, `t1`, and `t2` as unary thermometer segment controls, each contributing
four LSB steps. Drive `aout` between `vss` and `vref` according to the summed
15-step segmented code, so the all-active code reaches full scale.

## Modeling Constraints

Return only `segmented_dac.va`. Use deterministic voltage-domain Verilog-A and
smooth output transitions. Do not modify or emit the support testbench, add
checker logic, hard-code private waveform sample points, add simulator-private
side channels, use current contributions, `ddt()`, or `idt()`.
