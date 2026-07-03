# Pipe ADC Gain Control Loop

Implement a voltage-domain pipeline-ADC backend gain-control loop.

## Public Interface

Return exactly one Verilog-A source file named `pipe_adc_gain_control_loop.va`.
Declare module `pipe_adc_gain_control_loop` with positional ports `din20,
din21, din22, din23, din24, din25, din26, clks, dout10, dout11, dout12,
dout13, gainctrl0, gainctrl1, gainctrl2, gainctrl3, gainctrl4, gainctrl5,
gainctrl6, ddiff, dop, dom, gctrlcode`. All ports are electrical.

`din20..din26` are voltage-coded backend ADC bits, `clks` is the sampling
clock, `dout10..dout13` are alternating 4-bit test-DAC control rails,
`gainctrl0..gainctrl6` expose the 7-bit gain-control word, and `ddiff`, `dop`,
`dom`, and `gctrlcode` expose scalar voltage monitors for the measured code
difference, plus sample, minus sample, and gain-control code.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vlo = 0.0 V`, `vhi = 0.9 V`: voltage-coded logic levels.
- `vth = 0.45 V`: threshold for input-bit and clock decisions.
- `gaincodeinit = 90`: initial 7-bit gain-control code.

## Functional Contract

On each rising crossing of `clks`, read `din20..din26` as a 7-bit unsigned code.
Alternate between two 4-bit test-DAC states that create minus and plus
measurement phases. Store the minus-phase and plus-phase ADC codes, compute the
plus-minus code difference, and compare it against the target difference of 64
codes. If the difference is too large, reduce the gain-control code by the
absolute error from 64; if the difference is too small, increase it by that
absolute error. Clamp the gain-control code to `0..127`, emit its bits on
`gainctrl0..gainctrl6`, and expose `ddiff`, `dop`, `dom`, and `gctrlcode` as
deterministic scalar monitor voltages scaled by `1/100`.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on clock
crossings and smooth output voltages with `transition(...)`. Do not modify or
emit the support testbench, add checker logic, hard-code private waveform
sample points, add simulator-private side channels, use current contributions,
transistor-level devices, `ddt()`, `idt()`, or AC/noise-analysis behavior.
