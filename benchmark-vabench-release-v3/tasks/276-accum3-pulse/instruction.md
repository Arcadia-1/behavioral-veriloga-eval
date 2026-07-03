# Accum3 Pulse

Implement `accum3_pulse.va` in Verilog-A.

## Interface

```verilog
module accum3_pulse(
    input  electrical clk,
    output electrical out
);
```

## Required Behavior

This task asks for the `accum3_pulse` behavioral DUT module, not a Spectre
testbench. The module is a 3-bit modulo accumulator pulse generator.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vth` | `0.45` | V | Rising-edge threshold for `clk`. |
| `vdd` | `0.9` | V, `(0:inf)` | High level for the voltage-coded output. |
| `tdel` | `10 ps` | time, `[0:inf)` | Output transition delay. |
| `tr` | `10 ps` | time, `(0:inf)` | Output rise/fall smoothing. |

Required observable behavior:

- Initialize the internal 3-bit count to 7.
- Detect rising `clk` crossings at `vth`.
- Increment the count modulo 8 on each qualifying clock edge.
- Drive `out` high only when the modulo count is 0.
- Drive `out` low for all other count values.

Use voltage contributions only. Do not use current contributions,
transistor-level devices, AC/noise analysis, checker logic, private test hooks,
or simulator-private side channels.

## Output

Return exactly one source artifact named `accum3_pulse.va`.
