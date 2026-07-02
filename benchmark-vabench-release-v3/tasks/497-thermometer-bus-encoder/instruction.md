# Thermometer Bus Encoder

Implement one Verilog-A source file named `thermometer_bus_encoder.va`.

## Public Interface

```verilog
module thermometer_bus_encoder(vin, t0, t1, t2, t3, t4, t5, t6, t7,
                               t8, t9, t10, t11, t12, t13, t14, t15);
```

All ports are electrical. `vin` is a normalized analog input. `t0..t15` are
voltage-coded thermometer outputs ordered from the lowest segment to the
highest segment.

## Public Parameter Contract

- `vref = 1.0 V`: input full-scale reference.
- `vh = 0.9 V`: output logic-high level.
- `tr = 20p`: output transition smoothing time.

## Functional Contract

Convert `vin` into a 16-segment thermometer code. Clip the input to the
0-to-`vref` range, choose the number of active segments from the clipped input
level, and drive a prefix thermometer word: `t0` is the first segment to turn
on, then `t1`, and so on up to `t15`. The output must remain monotonic with
the input and must not emit a binary-coded word.

## Modeling Constraints

Use voltage-domain Verilog-A with smooth output transitions. Do not hard-code
testbench stimulus times, private sample points, or checker-only vectors.
