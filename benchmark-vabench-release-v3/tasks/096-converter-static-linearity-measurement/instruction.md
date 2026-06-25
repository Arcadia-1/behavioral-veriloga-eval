# Converter Static Linearity Measurement

Implement `converter_static_linearity_measurement_flow.va` in Verilog-A.

## Interface

```verilog
module converter_static_linearity_measurement_flow(clk, rst, vin, code, recon, dnl, inl);
```

## Required Behavior

This task asks for the `converter_static_linearity_measurement_flow` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_converter_static_linearity_measurement_flow` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

# Converter static linearity measurement flow (testbench generation)

Write a Spectre transient testbench for a supplied voltage-domain
static-linearity characterization flow for a 4-bit converter pair.

The supplied DUT samples an input ramp, quantizes it to a 4-bit code, reconstructs a deliberately
non-ideal DAC voltage, and uses a lightweight measurement stage to derive DNL/INL-like
metric voltages from the observed reconstruction. This is a converter measurement flow:
the checker observes code coverage, monotonic reconstruction, non-uniform code steps, and
metric consistency against the measured code/reconstruction history.

Public port contract:

```verilog
module converter_static_linearity_measurement_flow(clk, rst, vin, code, recon, dnl, inl);
input clk, rst, vin;
output code, recon, dnl, inl;
electrical clk, rst, vin, code, recon, dnl, inl;
```

Signal contract:

All logic controls are voltage-coded, low=0 V and high=0.9 V with threshold 0.45 V. The design remains pure voltage-domain behavioral Verilog-A: no current contributions, transistor devices, AC/noise analysis, or KCL/KVL solving assumptions.

Saved waveform columns:

```text
clk rst vin code recon dnl inl
```

Public transient contract:

```spectre
tran tran stop=96n maxstep=0.25n
```

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
