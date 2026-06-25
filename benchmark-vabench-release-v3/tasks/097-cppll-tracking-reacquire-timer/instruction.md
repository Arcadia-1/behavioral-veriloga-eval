# CPPLL Tracking Reacquire Timer

Implement `cppll_timer_ref.va` in Verilog-A.

## Interface

```verilog
module cppll_timer_ref (
    inout  electrical VDD,
    inout  electrical VSS,
    input  electrical ref_clk,
    output electrical fb_clk,
    output electrical dco_clk,
    output electrical vctrl_mon,
    output electrical lock
);
```

## Required Behavior

This task asks for the `cppll_timer_ref` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

This row is a CPPLL frequency-step reacquire flow. The testbench must expose a
reference step and enough time for the supplied loop to settle again:

1. Include both public support files `cppll_timer_ref.va` and `ref_step_clk.va`.
2. Instantiate the reference-step source and the CPPLL DUT with the public port
   order.
3. Run a transient long enough to include pre-step tracking, post-step
   disturbance, and late-window reacquisition.
4. Save `ref_clk fb_clk dco_clk vctrl_mon lock` exactly.

The expected public relation is: `ref_clk` changes cadence, `fb_clk` and
`dco_clk` temporarily deviate, `vctrl_mon` remains bounded, and `lock` is high
again in the late window. Do not generate checker logic.

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
