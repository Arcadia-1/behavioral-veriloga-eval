# Clocked Four Input Mux

## Task Contract

Implement a falling-edge clocked four-input analog mux sampler.

- Form: `dut`
- Level: `L1`
- Category: sampled-data analog routing
- Target artifact: `clocked_four_input_mux.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`clocked_four_input_mux.va` must declare:

```verilog
module clocked_four_input_mux(dsel0, dsel1, din0, din1, din2, din3, clks, dout);
input dsel0, dsel1, din0, din1, din2, din3, clks;
output dout;
electrical dsel0, dsel1, din0, din1, din2, din3, clks, dout;
```

## Public Parameter Contract

- `vth = 0.45`: threshold in volts for the clock and select rails.
- `tr = 20p`: output transition rise/fall time.

## Required Behavior

Initialize the held output value to `0 V`. On each falling threshold crossing of
`clks`, threshold `dsel1:dsel0` and latch one input:

- `00`: `din0`
- `01`: `din1`
- `10`: `din2`
- `11`: `din3`

Hold the latched value on `dout` until the next falling clock edge.

## Modeling Constraints

Use voltage-domain thresholding and a transition-shaped held output. Do not
update continuously with select changes, sample on rising edges, reorder the
select bits, or hard-code testbench waveform values.

## Output Contract

Return exactly one source artifact named `clocked_four_input_mux.va`.
