# PFD Reset Pulse

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: PLL/phase-frequency detector primitive.
- Target artifact: `pfd_reset_pulse.va`.
- Role: PFD set/reset pulse pair with active-low up-bar output.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module pfd_reset_pulse(a, b, ub, d);
```

`a` and `b` are input edge signals, `ub` is the active-low up-bar output, and `d` is the down output. All ports are electrical.

## Public Parameter Contract

No overrideable public parameters are required. Use a 0.45 V input threshold, 0/0.9 V output levels, a 10 ps reset interval after both inputs have arrived, and 10 ps output transitions.

## Required Behavior

A rising edge on `a` asserts the internal up state, driving `ub` low. A rising edge on `b` asserts the down state, driving `d` high. Once both states have arrived, schedule a reset after the public reset interval and then clear both states. Hold the current state between input and reset events.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `pfd_reset_pulse.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
