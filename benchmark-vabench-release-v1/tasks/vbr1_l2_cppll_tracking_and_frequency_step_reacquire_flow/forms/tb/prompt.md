# Task: vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: PLL / Clock / Event Timing
- Base function: CPPLL tracking and frequency-step reacquire flow
- Domain: `voltage`
- Target artifact(s): `tb_cppll_freq_step_reacquire_ref.scs`
- Supplied/reference support artifact(s): `cppll_timer_ref.va`, `ref_step_clk.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `cppll_timer_ref.va` declares module `cppll_timer_ref` with positional ports: `VDD`, `VSS`, `ref_clk`, `fb_clk`, `dco_clk`, `vctrl_mon`, `lock`.
- `ref_step_clk.va` declares module `ref_step_clk` with positional ports: `VDD`, `VSS`, `CLK`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=6u maxstep=5n errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref_clk`
- `fb_clk`
- `dco_clk`
- `vctrl_mon`
- `lock`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_cppll_freq_step_reacquire_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# CPPLL tracking and frequency-step reacquire flow Testbench Companion

Write a Spectre transient testbench for the `CPPLL tracking and frequency-step reacquire flow` behavioral
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
