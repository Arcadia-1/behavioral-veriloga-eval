# DAC Ideal 4b Offset

Implement the Verilog-A DUT `dac_ideal_4b_offset` in `dac_ideal_4b_offset.va`.

## Public Interface

The module port order is:

```text
din0, din1, din2, din3, dout
```

All ports are electrical. `din3` is the MSB and `din0` is the LSB.

## Public Parameters

- `vth = 0.45`: input logic threshold in volts.
- `offset = 0.239`: calibrated output baseline in volts.
- `scaling = 32.0*10.0/9.0`: calibration scale for the code-dependent trim step.

## Functional Contract

Decode the four input voltages into an unsigned binary trim code. An input bit is logic 1 when its voltage is greater than `vth`, otherwise it is logic 0. `din3` has weight 8, `din2` has weight 4, `din1` has weight 2, and `din0` has weight 1.

Drive `dout` as a calibrated trim output. Code 0 must produce `offset`, and each one-code increase must raise `dout` by `1/scaling` volts.

This task is a calibrated offset/trim DAC, not a plain full-scale binary DAC.

## Modeling Constraints

Use voltage-domain Verilog-A behavior only. Do not use current contributions, file I/O, random behavior, or simulator-private side channels. Use a short analog transition on `dout` so event-driven code changes are observable as smooth voltage updates.

## Output Contract

Return exactly one source artifact named `dac_ideal_4b_offset.va`. Do not include explanatory prose outside the source artifact contents.
