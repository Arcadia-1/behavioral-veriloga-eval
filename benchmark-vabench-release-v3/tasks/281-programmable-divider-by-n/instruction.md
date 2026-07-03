# Programmable Divider By N

Implement `programmable_divider_by_n.va` in Verilog-A.

## Interface

```verilog
module programmable_divider_by_n(
    input  electrical clk,
    input  electrical divctrl,
    output electrical out
);
```

## Required Behavior

This task asks for the `programmable_divider_by_n` behavioral DUT module, not a
Spectre testbench. The module is a voltage-domain programmable pulse divider.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vth` | `0.45` | V | Rising-edge threshold for `clk`. |
| `vh` | `0.9` | V, `(0:inf)` | High level for the voltage-coded output. |

Required observable behavior:

- Detect rising `clk` crossings at `vth`.
- Interpret `divctrl` as an analog-coded requested divide ratio by rounding it
  to the nearest integer.
- Clip requested ratios below 1 to divide ratio 1.
- Maintain an internal edge counter modulo the current divide ratio.
- Drive `out` high only when the internal counter is zero and low otherwise.
- For example, when `divctrl` requests ratio 3, `out` is high every third
  rising clock edge.

Use voltage contributions only. Do not use current contributions,
transistor-level devices, AC/noise analysis, checker logic, private test hooks,
or simulator-private side channels.

## Output

Return exactly one source artifact named `programmable_divider_by_n.va`.
