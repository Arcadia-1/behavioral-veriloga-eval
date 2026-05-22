# Task: vbr1_l1_dac_mismatch_unit_weighting_model:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converters
- Base function: DAC mismatch/unit-weighting model
- Domain: `voltage`
- Target artifact(s): `dac_mismatch_unit_weighting_model.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `dac_mismatch_unit_weighting_model.va` declares module `dac_mismatch_unit_weighting_model` with positional ports: `b0`, `b1`, `b2`, `b3`, `out`.

## Public Behavior Checks

- `weighted_code_response`
- `explicit_mismatch_terms`
- `bounded_reconstruction_voltage`

## Output Contract

Return exactly one source artifact named `dac_mismatch_unit_weighting_model.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# DAC mismatch/unit-weighting model (spec-to-va)

Write the Verilog-A behavioral module only.

Behavioral intent:

Model a 4-bit voltage DAC using explicit nonideal unit weights and a bounded output range.

Module name: `dac_mismatch_unit_weighting_model`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module dac_mismatch_unit_weighting_model(b0, b1, b2, b3, out);
input b0, b1, b2, b3;
output out;
electrical b0, b1, b2, b3, out
```

Signal contract:

b0..b3 are voltage-coded logic bits, low=0 V and high=0.9 V with threshold 0.45 V. out is a bounded voltage reconstruction in [0, 0.9] V.

Saved waveform columns:

```text
b0 b1 b2 b3 out
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```
