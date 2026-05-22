# Task: vbr1_l1_dwa_dem_encoder:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: DWA/DEM encoder
- Domain: `voltage`
- Target artifact(s): `tb_dwa_ptr_gen_ref.scs`
- Supplied/reference support artifact(s): `dwa_ptr_gen.va`, `v2b_4b.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `dwa_ptr_gen.va` declares module `dwa_ptr_gen` with positional ports: `clk_i`, `rst_ni`, `code_msb_i`, `cell_en_o`, `ptr_o`.
- `v2b_4b.va` declares module `v2b_4b` with positional ports: `clk`, `vin`, `out_3`, `out_2`, `out_1`, `out_0`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=100n maxstep=2n
```

The release harness expects these exact public scalar observables:

- `clk_i`
- `rst_ni`
- `code_3`
- `code_2`
- `code_1`
- `code_0`
- `\`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `clk_i`
- `rst_ni`
- `vin_node`

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_dwa_ptr_gen_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# DWA/DEM encoder Testbench Companion

Write a Spectre transient testbench for the `DWA/DEM encoder` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the Verilog-A behavioral module under test
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
