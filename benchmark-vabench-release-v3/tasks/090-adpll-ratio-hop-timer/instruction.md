# ADPLL Ratio Hop Timer

Implement `adpll_ratio_hop_ref.va` in Verilog-A.

## Interface

```verilog
module adpll_ratio_hop_ref (
    inout  electrical VDD,
    inout  electrical VSS,
    input  electrical ref_clk,
    input  electrical ratio_ctrl,
    output electrical fb_clk,
    output electrical vout,
    output electrical vctrl_mon,
    output electrical lock
);
```

## Required Behavior

This task asks for the `adpll_ratio_hop_ref` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_adpll_lock_ratio_hop_timer_flow` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

This row is an ADPLL lock and ratio-hop flow. The testbench must expose the
pre-hop ratio, post-hop ratio, and reacquired lock:

1. Drive `ref_clk` as a stable 0 V/0.9 V periodic reference clock.
2. Drive `ratio_ctrl` initially near 4 and step it later to near 6.
3. Run long enough before the step for `lock` to assert and the pre-hop
   `vout`/`ref_clk` ratio to be visible.
4. Run long enough after the step for the loop to reacquire lock and the
   post-hop ratio to be visible.
5. Save `ref_clk ratio_ctrl fb_clk vout vctrl_mon lock` exactly.

Do not generate checker logic; the evaluator derives the pre-hop ratio,
post-hop ratio, `vout`/`fb_clk` divider relation, `fb_clk`/`ref_clk` tracking,
and lock reacquisition from these saved waveforms. The supplied DUT is expected
to use feedback timing in its control and lock decision, so the testbench should
not replace `fb_clk` with an independent source.

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
