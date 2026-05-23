# Task: vbr1_l2_pll_timing_slice:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: PLL / Clock / Event Timing
- Base function: PLL timing slice
- Domain: `voltage`
- Target artifact(s): `tb_cppll_tracking_ref.scs`
- Supplied/reference support artifact(s): `cppll_timer_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `cppll_timer_ref.va` declares module `cppll_timer_ref` with positional ports: `VDD`, `VSS`, `ref_clk`, `fb_clk`, `dco_clk`, `vctrl_mon`, `lock`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=5u errpreset=conservative
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
- `ref_clk`

## Public Behavior Checks

- `cppll_tracks_reference_frequency`
- `lock_asserts_in_late_tracking_window`
- `vctrl_stays_bounded`

## Output Contract

Return exactly one source artifact named `tb_cppll_tracking_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# PLL timing slice Testbench Companion

Write a Spectre transient testbench for the `PLL timing slice` behavioral
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
