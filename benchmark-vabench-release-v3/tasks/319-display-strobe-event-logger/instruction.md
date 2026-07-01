# Display Strobe Event Logger

Implement one behavioral Verilog-A DUT file named `display_strobe_event_logger.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module display_strobe_event_logger (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `$display` and `$strobe` system tasks inside event-driven Verilog-A code while producing deterministic voltage-domain behavior.

Use voltage-coded logic with `vth = 0.45` V and `vhi = 0.9` V.

A rising `rst` event must clear the event count, classification state, `out`, and `metric`, and should call `$display` with a reset message.

On each rising crossing of `clk` through `vth` while reset is low:

- increment `count_q`
- classify the current `vin` sample:
  - `vin < 0.30`: class 1, `out = 0.225`
  - `0.30 <= vin < 0.70`: class 2, `out = 0.450`
  - `vin >= 0.70`: class 3, `out = 0.900`
- drive `metric = count_q / 4.0`, capped at `1.0`
- call `$strobe` with the event count, class, and sampled `vin`

The first hidden clock edge occurs while reset is high and must not be counted. Four later post-reset clock edges must produce classes `1, 2, 3, 2` and metric levels `0.25, 0.50, 0.75, 1.00`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `display_strobe_event_logger.va`. Do not generate a Spectre testbench for this task.
