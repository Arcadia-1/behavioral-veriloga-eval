# Task: vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: PLL Clock and Timing Systems
- Base function: CPPLL tracking and frequency-step reacquire flow
- Domain: `voltage`
- Target artifact(s): `cppll_timer_ref.va`, `ref_step_clk.va`, `tb_cppll_freq_step_reacquire_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cppll_timer_ref.va`, `ref_step_clk.va`, `tb_cppll_freq_step_reacquire_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

- `cppll_reacquires_after_reference_step`
- `late_window_tracks_new_reference`
- `vctrl_stays_bounded`

## Output Contract

Return exactly these source artifacts:

- `cppll_timer_ref.va`
- `ref_step_clk.va`
- `tb_cppll_freq_step_reacquire_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `cppll_timer_ref`.

Create a voltage-domain charge-pump style PLL (CPPLL) behavioral
model in Verilog-A with a behavioral DCO timing loop, then produce a minimal Spectre transient testbench
that demonstrates unlock and reacquire behavior after a reference-frequency
step.

This L2 task is intentionally stronger than the steady
`vbr1_l2_pll_timing_slice`: it must show pre-step lock, disturbance-induced
unlock or lock drop, and late-window relock to the new reference frequency.

Behavioral intent:

- one reference clock input `ref_clk`
- one divided feedback clock output `fb_clk`
- one oscillator clock output `dco_clk`
- one monitor node `vctrl_mon` that reflects the loop control voltage
- one lock indicator output `lock`
- the loop should first lock to an initial reference, lose lock after a
  moderate reference-frequency change, then reacquire and track the new late
  frequency

Implementation constraints:

- pure voltage-domain Verilog-A only
- portable voltage-domain behavioral Verilog-A syntax
- use `@(timer(...))` for the DCO timing loop
- `fb_clk`, `dco_clk`, and `lock` should be driven as voltage outputs
- use the public `ref_step_clk` source artifact to create the reference step
- `ref_clk`, `fb_clk`, `lock`, and `vctrl_mon` must appear in the waveform CSV

Minimum simulation goal:

- the generated testbench should step the reference clock from 50 MHz to about
  51.28 MHz during the transient
- `lock` should show a pre-step lock event and at least one post-step relock
  event after the disturbance
- the late-window `fb_clk` frequency should match the stepped reference within a
  few percent
- `vctrl_mon` should stay bounded by the supply rails throughout the transient

Expected behavior:
- PLL should achieve lock before disturbance (lock goes high)
- After disturbance, PLL should re-lock within reasonable time
- Late frequency ratio (ref_period/fb_period) should be close to 1.0 when locked
Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `ref_clk`: input electrical
- `fb_clk`: output electrical
- `dco_clk`: output electrical
- `vctrl_mon`: output electrical
- `lock`: output electrical
