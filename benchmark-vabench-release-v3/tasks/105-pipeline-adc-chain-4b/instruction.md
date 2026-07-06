# Pipeline ADC Chain 4b

## Task Contract

Implement one Verilog-A source file named `pipeline_adc_chain_4b.va` for an L2
pipeline-ADC residue-chain component. The model should convert a sampled analog
input into two cascaded 2-bit stage decisions, expose both residue voltages, and
drive the final 4-bit output word.

## Form-Specific Requirements

This is a single-DUT task. The visible testbench is a public verification
scenario for wiring, stimulus, and observable signals; do not hard-code its
waveform points, sample times, or stop time into the DUT.

## Public Verilog-A Interface

```verilog
module pipeline_adc_chain_4b(VDD, VSS, VIN, CLK, RES1, RES2, S1B1, S1B0, S2B1, S2B0, DOUT3, DOUT2, DOUT1, DOUT0);
```

All ports are electrical. `VDD` and `VSS` are the supply rails, `VIN` is the
analog input, and `CLK` is the conversion strobe. `RES1` and `RES2` expose the
first-stage and second-stage residue voltages. `S1B1/S1B0` and `S2B1/S2B0`
expose the two stage decisions. `DOUT3..DOUT0` expose the final 4-bit code, with
`DOUT3` as MSB.

## Public Parameter Contract

- `vrefp = 0.9 V`: positive conversion reference.
- `vrefn = 0.0 V`: negative conversion reference.
- `vth = 0.45 V`: threshold for voltage-coded clock and output-bit logic.
- `tedge = 100p`: transition smoothing time for residue and bit outputs.

## Required Behavior

On each rising crossing of `CLK`, clip `VIN` to the `vrefn`-to-`vrefp` range
and perform a two-stage 2-bit/stage conversion.

Stage 1 makes a 2-bit coarse decision from the clipped input, drives that
decision on `S1B1/S1B0`, computes the center of the selected quarter-scale bin,
amplifies the input error from that center by four, and drives the clipped first
residue on `RES1`.

Stage 2 applies the same 2-bit quarter-scale rule to `RES1`, drives the backend
decision on `S2B1/S2B0`, computes the second residue with the same gain-of-four
residue rule, and drives the clipped backend residue on `RES2`.

The final output word is the stage-1 decision concatenated with the stage-2
decision: `DOUT3/DOUT2` are the stage-1 bits and `DOUT1/DOUT0` are the stage-2
bits. High logic outputs should be near `VDD`; low logic outputs should be near
`VSS`.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A only. Use the supply rails for output
logic levels and smooth output transitions with the public `tedge` parameter.
Do not emit a Spectre testbench, checker logic, private waveform sample points,
current contributions, transistor-level devices, AC/noise analysis, `ddt()`, or
`idt()`.

## Output Contract

Submit only `pipeline_adc_chain_4b.va`. The file must define the module above,
compile as Verilog-A, and drive `RES1`, `RES2`, all stage-decision outputs, and
all final code outputs for transient simulation.
