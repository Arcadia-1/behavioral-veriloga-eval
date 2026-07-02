# Deterministic Mismatch DAC6

Implement one Verilog-A source file named `deterministic_mismatch_dac6.va`.

## Public Interface

```verilog
module deterministic_mismatch_dac6(d5, d4, d3, d2, d1, d0, vout);
```

All ports are electrical. `d5` is the MSB, `d0` is the LSB, and `vout` is the
analog DAC output.

## Public Parameter Contract

- `vth = 0.45 V`: input logic threshold.
- `vref = 1.0 V`: full-scale endpoint reference.
- `tr = 20p`: output transition smoothing time.
- `m5 = 0.08`, `m4 = -0.06`, `m3 = 0.04`, `m2 = -0.03`, `m1 = 0.025`,
  `m0 = -0.015`: deterministic fractional weight errors for the six binary
  elements.

## Required Behavior

Treat each input as logic `1` when its voltage is greater than `vth`. Use the
nominal binary weights associated with `d5..d0`, but apply each bit's public
fractional weight error before summing active elements. Normalize by the sum of
all actual element weights so the all-ones code maps to `vref` even when the
individual weights are mismatched. Drive `vout` smoothly to the resulting
static DAC level.

## Modeling Constraints

Use voltage-domain Verilog-A only. Do not replace the mismatch model with an
ideal binary DAC, hard-code private waveform sample points, add random mismatch,
current contributions, `ddt()`, or `idt()`.
