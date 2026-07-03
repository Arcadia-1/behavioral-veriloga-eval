# Hysteretic Comparator Receiver

Implement a pure voltage-domain analog comparator receiver with input
hysteresis, a fixed propagation delay, and a rail-coded voltage output. This
task adapts the Cadence Verilog-AMS comparator modeling pattern that uses
`OFFSET` and `HYST` to form upper and lower switching thresholds, while keeping
the output in the voltage-domain Verilog-A style used by this benchmark.

## Public Interface

Declare module `hysteretic_comparator_receiver` with positional ports `inp,
inm, out`. All ports are electrical. `inp` and `inm` form the differential
comparator input, and `out` is a voltage-coded digital receiver output.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vout_high = 0.9 V`: high output rail.
- `vout_low = 0.0 V`: low output rail.
- `offset = 0.0 V`: input-referred switching offset.
- `vhys = 40 mV`: total hysteresis width. It must be non-negative.
- `td = 400 ps`: propagation delay from a qualifying input threshold crossing
  to the output state change. It must be non-negative.
- `tr = 80 ps`: output transition rise/fall smoothing time. It must be
  non-negative.

## Functional Contract

Define the upper and lower decision thresholds as:

```text
upper_th = offset + vhys / 2
lower_th = offset - vhys / 2
```

On initialization, drive the high state when `V(inp,inm)` is already at or
above `upper_th`; otherwise drive the low state. After initialization, set the
internal state high only on a rising crossing of `upper_th`, and set it low
only on a falling crossing of `lower_th`. Hold the previous state while the
differential input remains between those two thresholds.

Drive `out` to `vout_high` for the high state and to `vout_low` for the low
state. Apply the public propagation delay `td` and smooth each output edge with
the public transition time `tr`.

## Modeling Constraints

Return only `hysteretic_comparator_receiver.va`. Use voltage contributions
only. Do not modify or emit the support testbench, add checker logic,
hard-code waveform sample points, add simulator-private side channels, use
current contributions, `ddt()`, or `idt()`.
