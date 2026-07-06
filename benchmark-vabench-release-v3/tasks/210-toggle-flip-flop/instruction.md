# Toggle Flip-Flop

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: AMS clock/control support primitive.
- Target artifact: `toggle_flip_flop.va`.
- Role: voltage-domain complementary toggle state element.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module toggle_flip_flop(vtrig, vout_q, vout_qbar);
```

`vtrig` is the trigger input and `vout_q`/`vout_qbar` are complementary voltage-coded outputs. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameters `initial_state = 0 from [0:1]`, `vlogic_high = 0.9`, `vlogic_low = 0`, `vtrans = 0.45`, `tdel = 50p`, `trise = 20p`, and `tfall = 20p`.

## Required Behavior

Initialize `q` from `initial_state`. On each rising crossing of `vtrig` through `vtrans`, toggle the internal state. Drive `vout_q` from the state and `vout_qbar` from its complement using the public voltage levels and transition timing.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `toggle_flip_flop.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
