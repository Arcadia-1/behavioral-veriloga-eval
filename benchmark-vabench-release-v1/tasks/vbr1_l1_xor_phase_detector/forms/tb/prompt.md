# Task: vbr1_l1_xor_phase_detector:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: XOR phase detector
- Domain: `voltage`
- Target artifact(s): `tb_xor_phase_detector_ref.scs`
- Supplied/reference support artifact(s): `xor_phase_detector_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `xor_phase_detector_ref.va` declares module `xor_phase_detector` with positional ports: `VDD`, `VSS`, `REF`, `DIV`, `PD_OUT`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=200n maxstep=100p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref`
- `div`
- `pd_out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `ref`
- `div`

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_xor_phase_detector_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# XOR phase detector Testbench Companion

Write a Spectre transient testbench for the `XOR phase detector` behavioral
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
