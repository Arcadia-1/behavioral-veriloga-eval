# Element Shuffler

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Element shuffler
- Domain: `voltage`
- Target artifact(s): `element_shuffler.va`
- Visible context: public task, interface, starter artifact, public smoke test, and observable behavior contract only.
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Do not generate a Spectre testbench for this form.
- Preserve the public module name, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

The file `element_shuffler.va` must define module `element_shuffler` with positional ports:

```verilog
module element_shuffler(clk, rst_n, out0, out1, out2, out3);
```

All ports are electrical.

## Required Behavior

Treat `clk` and `rst_n` as voltage-coded logic signals using threshold `0.45 V`.

`rst_n` is active low. When `rst_n` is low, the shuffler must reset its internal state so the first valid rising edge of `clk` after reset release produces `out2` as the active output.

After reset is released, the active output must advance on each rising edge of `clk` through this repeating permutation:

```text
out2 -> out0 -> out3 -> out1 -> out2 -> ...
```

Exactly one of `out0`, `out1`, `out2`, and `out3` must be high in each stable state. Active outputs should be near `0.9 V`; inactive outputs should be near `0 V`.

The output sequence must be driven by `clk` and `rst_n` behavior, not by absolute simulation time.

## Implementation Constraints

Use voltage contributions only.

Do not use current contributions, transistor-level devices, `ddt()`, `idt()`, AC/noise analysis, private test hooks, or simulator-private side channels.

Smooth output transitions with `transition(...)` or equivalent Verilog-A voltage contribution.

## Output Contract

Return exactly one complete Verilog-A file named `element_shuffler.va`.
Do not include explanatory prose outside the source artifact contents.
