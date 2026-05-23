# Task: vbr1_l2_adpll_lock_ratio_hop_timer_flow:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: PLL / Clock / Event Timing
- Base function: ADPLL lock/ratio-hop/timer flow
- Domain: `voltage`
- Target artifact(s): `adpll_ratio_hop_ref.va`, `tb_adpll_ratio_hop_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `adpll_ratio_hop_ref.va`, `tb_adpll_ratio_hop_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `adpll_ratio_hop_ref.va` declares module `adpll_ratio_hop_ref` with positional ports: `VDD`, `VSS`, `ref_clk`, `ratio_ctrl`, `fb_clk`, `vout`, `vctrl_mon`, `lock`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=5u maxstep=5n
```

The release harness expects these exact public scalar observables:

- `ref_clk`
- `ratio_ctrl`
- `fb_clk`
- `vout`
- `vctrl_mon`
- `lock`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `ref_clk`
- `ratio_ctrl`

## Public Behavior Checks

- `adpll_ratio_hop_pre_ratio`
- `adpll_ratio_hop_post_ratio`
- `adpll_ratio_hop_lock_reacquired`

## Output Contract

Return exactly these source artifacts:

- `adpll_ratio_hop_ref.va`
- `tb_adpll_ratio_hop_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `adpll_ratio_hop_ref`.

# Task: adpll_ratio_hop_smoke

Write a pure voltage-domain Verilog-A behavioral ADPLL that uses a timer-driven DCO and a programmable feedback divider.

Requirements:

1. Ports must be `electrical` only.
2. The module must take a reference clock input and an analog `ratio_ctrl` input whose rounded value sets the divider ratio in the range 2 to 16.
3. The DCO frequency must be adjusted by an internal digital control code so the divided feedback clock tracks the reference.
4. Expose:
   - `vout` as the DCO clock output
   - `fb_clk` as the divided feedback clock
   - `vctrl_mon` as a normalized monitor of the control code
   - `lock` as a streak-based lock indicator
5. The reference testbench will step `ratio_ctrl` from 4 to 6 during transient.

Expected behavior:
- When ratio_ctrl ≈ 4V: vout frequency / ref_clk frequency ≈ 4.0 (ratio = divider setting)
- When ratio_ctrl ≈ 6V: vout frequency / ref_clk frequency ≈ 6.0 after ratio hop
- lock signal should be ≥ 80% high before and after the ratio change
- vctrl_mon should stay within [0, 1.2V] range
Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `ref_clk`: input electrical
- `ratio_ctrl`: input electrical
- `fb_clk`: output electrical
- `vout`: output electrical
- `vctrl_mon`: output electrical
- `lock`: output electrical

Write pure voltage-domain behavioral Verilog-A with no current contributions.
