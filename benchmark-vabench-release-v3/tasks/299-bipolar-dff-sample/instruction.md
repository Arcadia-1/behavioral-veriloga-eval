# Bipolar DFF Sample

Implement `bipolar_dff_sample.va` in Verilog-A.

## Interface

```verilog
module bipolar_dff_sample(
    input  electrical vin_d,
    input  electrical vclk,
    output electrical vout_q,
    output electrical vout_qbar
);
```

## Required Behavior

This task asks for the `bipolar_dff_sample` behavioral DUT module, not a
Spectre testbench. The module is a rising-edge D flip-flop with bipolar
complementary outputs.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vth` | `0.0` | V | Data threshold for `vin_d`. |
| `vclk_th` | `0.45` | V | Rising-edge threshold for `vclk`. |

Required observable behavior:

- Detect rising `vclk` crossings at `vclk_th`.
- At each qualifying clock edge, sample whether `vin_d` is above `vth`.
- Hold the sampled state between clock edges.
- Drive `vout_q` to `+1 V` when the sampled state is high and `-1 V` when it is
  low.
- Drive `vout_qbar` as the complementary bipolar output.

Use voltage contributions only. Do not use current contributions,
transistor-level devices, AC/noise analysis, checker logic, private test hooks,
or simulator-private side channels.

## Output

Return exactly one source artifact named `bipolar_dff_sample.va`.
