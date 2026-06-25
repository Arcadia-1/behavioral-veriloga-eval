# Pipeline ADC Chain 4b

Implement `pipeline_adc_chain_4b.va` in Verilog-A.

## Interface

```verilog
module pipeline_adc_chain_4b(VDD, VSS, VIN, CLK, RES1, RES2, S1B1, S1B0, S2B1, S2B0, DOUT3, DOUT2, DOUT1, DOUT0);
```

## Required Behavior

This task asks for the `pipeline_adc_chain_4b` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_pipeline_adc_chain` transient scenario and checks the saved waveform/metric behavior with EVAS.

Gold-source design notes carried into the public contract:

```text
// Two-stage 2-bit/stage pipeline ADC residue chain, EVAS-compatible behavioral model.
// Stage 1 makes a 2-bit coarse decision, amplifies the residue by 4, and
// stage 2 quantizes that residue into the lower 2 output bits.
```

Original public behavior context:

# Pipeline ADC residue chain Testbench Companion

Write a Spectre transient testbench for a pure voltage-domain compact two-stage
4-bit pipeline ADC chain. The supplied DUT performs a 2-bit coarse
quantization, outputs the first residue, performs a 2-bit backend quantization,
and drives a final 4-bit code for the same sampled input. This is a
single-sample behavioral residue chain, not a latency/correction benchmark.

Public requirements:

- use a 0.9 V supply
- drive `vin` through representative points in all 16 final 4-bit code bins
- alternate lower-half and upper-half points inside adjacent bins so the
  residue path is exercised, not only the final code output
- drive `clk` so every input point is stable before a rising clock edge
- instantiate `pipeline_adc_chain_4b` by positional ports
- save exactly these scalar names: `vin`, `clk`, `res1`, `res2`, `s1b1`,
  `s1b0`, `s2b1`, `s2b0`, `dout3`, `dout2`, `dout1`, `dout0`
- include a transient `tran` analysis
- avoid transistor-level devices, AC/noise analysis, and current-domain solver assumptions

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
