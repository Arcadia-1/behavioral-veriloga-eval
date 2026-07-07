# Display Strobe Event Logger

## Task Contract

Implement one behavioral Verilog-A DUT file named `display_strobe_event_logger.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Public Verilog-A Interface

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

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

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

Clock events that occur while reset is high must not be counted. Each accepted
post-reset clock edge must classify the current `vin` sample using the public
thresholds above, update `out` from that class, advance the normalized event
metric, and emit the `$strobe` record. Do not hard-code testbench-specific
waveform times or sample values. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Modeling Constraints

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `display_strobe_event_logger.va`. Do not generate a Spectre testbench for this task.
