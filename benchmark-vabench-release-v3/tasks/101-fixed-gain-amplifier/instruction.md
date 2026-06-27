# Fixed Gain Amplifier

Implement `gain_amp_fixed.va` in Verilog-A.

## Interface

```verilog
module gain_amp_fixed(
    input  electrical VIN_P,
    input  electrical VIN_N,
    output electrical VOUT_P,
    output electrical VOUT_N
);
```

## Required Behavior

Implement a standalone fixed-gain differential amplifier. The module receives
`VIN_P/VIN_N`, computes the input differential voltage, multiplies it by the
`ACTUAL_GAIN` parameter, and produces a differential output centered around
`vdd/2`:

```text
vout_diff = ACTUAL_GAIN * (VIN_P - VIN_N)
VOUT_P = vdd/2 + vout_diff / 2
VOUT_N = vdd/2 - vout_diff / 2
```

The amplifier must preserve output common-mode at `vdd/2`, keep positive
polarity from input differential to output differential, and honor different
`ACTUAL_GAIN` and `vdd` values supplied by the testbench.

Keep the model pure behavioral Verilog-A. Do not use transistor-level devices,
AC/noise analysis, private test hooks, or simulator-private side channels.

Only `gain_amp_fixed.va` is graded as the candidate implementation.
