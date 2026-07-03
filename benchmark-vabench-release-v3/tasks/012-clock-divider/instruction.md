# PLL Feedback Clock Divider

Implement `clk_divider_ref.va` in Verilog-A.

## Interface

```verilog
module clk_divider_ref (
    input  electrical clk_in,
    input  electrical rst_n,
    input  electrical div_code_0,
    input  electrical div_code_1,
    input  electrical div_code_2,
    input  electrical div_code_3,
    input  electrical div_code_4,
    input  electrical div_code_5,
    input  electrical div_code_6,
    input  electrical div_code_7,
    output electrical clk_out,
    output electrical lock
);
```

## Required Behavior

This task asks for the `clk_divider_ref` behavioral DUT module, not a Spectre
testbench. The module is a resettable, voltage-domain PLL/ADPLL feedback
divider with an 8-bit programmable ratio code and a lock indicator.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vdd` | `0.9` | V, `(0:inf)` | High level for voltage-coded outputs. |
| `vth` | `0.45` | V | Logic threshold for clock, reset, and ratio-code inputs. |
| `trf` | `10 ps` | time, `(0:inf)` | Rise/fall smoothing for `clk_out` and `lock`. |
| `td` | `0 ps` | time, `[0:inf)` | Transition delay for voltage-coded outputs. |

Required observable behavior:

- Treat all inputs and outputs as electrical voltage-domain signals.
- Interpret `rst_n` as active-low reset. While reset is low, clear the divider
  state and drive `clk_out` and `lock` low.
- Decode `div_code_0` through `div_code_7` as an unsigned 8-bit LSB-first
  voltage-coded ratio. Code 0 maps to divide ratio 1.
- For divide ratio 1, reproduce the input clock activity on `clk_out` and
  assert `lock` after the first valid post-reset clock cycle.
- For divide ratios greater than 1, generate a periodic divided clock whose
  rising-to-rising output period spans the decoded number of input rising
  edges after startup.
- For odd divide ratios, use floor/ceil segment lengths so both high and low
  phases are present and the long segment differs by at most one input cycle
  from the short segment.
- Assert `lock` only after the first complete output period for the current
  decoded ratio. If the ratio code changes after reset, clear divider phase and
  `lock`, then reacquire using the new ratio.

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, checker logic, private
test hooks, or simulator-private side channels.

## Output

Return exactly one source artifact named `clk_divider_ref.va`.
