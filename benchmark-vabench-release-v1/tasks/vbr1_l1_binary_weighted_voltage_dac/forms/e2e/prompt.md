# Task: vbr1_l1_binary_weighted_voltage_dac:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Data Converters
- Base function: Simple 4-bit binary-coded DAC
- Domain: `voltage`
- Target artifact(s): `simple_binary_voltage_dac_4b.va`, `tb_simple_binary_voltage_dac_4b_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `simple_binary_voltage_dac_4b.va`, `tb_simple_binary_voltage_dac_4b_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `simple_binary_voltage_dac_4b.va` declares module `simple_binary_voltage_dac_4b` with positional ports: `code_0`, `code_1`, `code_2`, `code_3`, `vref`, `vss`, `aout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=165n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `code_0`
- `code_1`
- `code_2`
- `code_3`
- `aout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vref`
- `vss`
- `code_0`
- `code_1`
- `code_2`
- `code_3`

## Public Behavior Checks

- `binary_code_to_level_mapping`
- `midscale_and_fullscale_levels_match_code_over_15`

## Output Contract

Return exactly these source artifacts:

- `simple_binary_voltage_dac_4b.va`
- `tb_simple_binary_voltage_dac_4b_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_simple_binary_voltage_dac_4b_e2e

Write both the Verilog-A DUT and Spectre testbench for a simple 4-bit binary-coded DAC.

The DUT module is `simple_binary_voltage_dac_4b` with ports `code_0, code_1, code_2, code_3, vref, vss, aout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Implement the simple mathematical 4-bit binary-coded DAC described by the input code and references.
- Interpret `code_0..code_3` as a binary code with weights 1, 2, 4, and 8.
- Drive `aout` linearly between `vss` and `vref` using code/15 and smooth with `transition()`; no unit-element or segmented DAC structure is required.

Required testbench behavior:
- Apply multiple binary codes spanning low, middle, and full-scale values.
- Save all code bits and `aout`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Review note: This is a behavioral binary-weighted transfer model, not a unit-element or segmented DAC implementation.

Return exactly two files: `simple_binary_voltage_dac_4b.va` and `tb_simple_binary_voltage_dac_4b_ref.scs`.
