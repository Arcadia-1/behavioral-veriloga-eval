# Task: vbr1_l2_pll_timing_slice:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: PLL / Clock / Event Timing
- Base function: PLL timing slice
- Domain: `voltage`
- Target artifact(s): `cppll_timer_ref.va`, `tb_cppll_tracking_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cppll_timer_ref.va`, `tb_cppll_tracking_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `cppll_timer_ref.va`
- `tb_cppll_tracking_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `cppll_timer_ref`.

Create a timer-based voltage-domain charge-pump style PLL (CPPLL) behavioral
model in Verilog-A, then produce a minimal EVAS-compatible Spectre testbench
for a steady tracking slice.

This L2 task is the base closed-loop timing slice. It should demonstrate
stable reference tracking under a fixed reference clock. It should not include
the reference-frequency step or reacquire scenario used by
`vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow`.

Behavioral intent:

- one reference clock input `ref_clk`
- one divided feedback clock output `fb_clk`
- one oscillator clock output `dco_clk`
- one monitor node `vctrl_mon` that reflects the loop control voltage
- one lock indicator output `lock`
- the loop should use proportional-plus-integral style phase correction so that
  the divided feedback frequency tracks the reference clock

Implementation constraints:

- pure voltage-domain Verilog-A only
- EVAS-compatible syntax
- use `@(timer(...))` for the DCO timing loop
- `fb_clk`, `dco_clk`, and `lock` should be driven as voltage outputs
- `ref_clk`, `fb_clk`, `lock`, and `vctrl_mon` must appear in the waveform CSV

Minimum simulation goal:

- the generated testbench should stimulate a 50 MHz reference clock
- the late-window `fb_clk` frequency should match the reference within a few
  percent
- `lock` should assert after the loop has accumulated enough stable late
  tracking windows
- `vctrl_mon` should stay bounded by the supply rails throughout the transient

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `ref_clk`: input electrical
- `fb_clk`: output electrical
- `dco_clk`: output electrical
- `vctrl_mon`: output electrical
- `lock`: output electrical
