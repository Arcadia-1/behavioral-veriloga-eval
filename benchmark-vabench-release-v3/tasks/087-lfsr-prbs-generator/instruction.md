# LFSR PRBS Generator

Implement `prbs7_ref.va` in Verilog-A.

## Interface

Declare module `prbs7_ref` with positional ports:

```verilog
clk, rst_n, en, serial_out, state_0, state_1, state_2, state_3, state_4, state_5, state_6
```

All ports are electrical.

## Public Parameter Contract

- `vdd = 0.9 V`: high logic output level.
- `vth = 0.45 V`: clock, reset, and enable threshold.
- `trf = 10 ps`: output transition rise/fall time.
- `td = 0 ps`: output transition delay.
- `seed = 127`: reset seed. If an override provides an all-zero seed, force a
  nonzero state.

## Functional Contract

Create a clocked PRBS-7 stimulus source using a 7-bit LFSR with polynomial
`x^7 + x^6 + 1`. Treat `state_0` as bit 0 and `state_6` as bit 6. On reset,
load the public seed. On each rising crossing of `clk` through `vth`, advance
the LFSR only when `rst_n` and `en` are high. The feedback bit is:

```text
feedback = state_6 xor state_5
next_state_0 = feedback
next_state_i = previous_state_(i-1), for i = 1..6
```

Drive `serial_out` from `state_6` and expose each state bit on its matching
`state_i` output using voltage-coded `0`/`vdd` levels.

## Modeling Constraints

Return only `prbs7_ref.va`. Do not generate a Spectre testbench or checker
logic. Do not use current contributions, `ddt()`, transistor-level devices,
AC/noise analysis, or simulator-private side channels.
