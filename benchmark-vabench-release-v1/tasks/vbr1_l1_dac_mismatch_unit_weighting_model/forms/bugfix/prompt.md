# Task: vbr1_l1_dac_mismatch_unit_weighting_model:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Data Converters
- Base function: DAC mismatch/unit-weighting model
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `dac_mismatch_unit_weighting_model` with positional ports: `b0`, `b1`, `b2`, `b3`, `out`.
- `dut_fixed.va` declares module `dac_mismatch_unit_weighting_model` with positional ports: `b0`, `b1`, `b2`, `b3`, `out`.

## Public Behavior Checks

- `weighted_code_response`
- `explicit_mismatch_terms`
- `bounded_reconstruction_voltage`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# DAC mismatch/unit-weighting model (bugfix)

Repair the supplied buggy Verilog-A implementation.

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
