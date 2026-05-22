# Task: vbr1_l1_voltage_gain_amplifier:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Analog Behavioral Signal Conditioning
- Base function: Voltage gain amplifier
- Domain: `voltage`
- Target artifact(s): `voltage_gain_amplifier.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `voltage_gain_amplifier.va` declares module `voltage_gain_amplifier` with positional ports: `clk`, `rst`, `vin`, `out`, `metric`.

## Public Behavior Checks

- `gain_applied`
- `common_mode_offset`
- `output_clamped`

## Output Contract

Return exactly one source artifact named `voltage_gain_amplifier.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Voltage gain amplifier (spec-to-va)

Write the Verilog-A behavioral module only.

Behavioral intent:

Apply a voltage-domain gain with output common-mode offset and rail clamps.

Module name: `voltage_gain_amplifier`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module voltage_gain_amplifier(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded conditioned voltage. metric exposes the filter/settling internal response.

Saved waveform columns:

```text
clk rst vin out metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```
