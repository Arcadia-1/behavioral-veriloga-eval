Generate only the Spectre testbench for the `clock_divider` circuit function.
Do not generate Verilog-A modules.  The evaluator provides the DUT Verilog-A file(s).

Required DUT include(s): `clk_div.va`.
Required module(s): `clk_div`.

The testbench must instantiate the provided DUT, drive the public inputs through the validation behavior, run exactly one transient analysis, and save the public observables.

## Source Functional Specification

Write a Verilog-A module named `clk_div`.

Create a voltage-domain clock divider in Verilog-A, then produce a minimal EVAS
testbench and run a smoke simulation.

Behavioral intent:

- input clock and synchronous reset
- divide-by-4 output
- 50% duty-cycle style output if practical
- one digital output clock node

Ports:
- `CLK_IN`: input electrical
- `RST_N`: input electrical
- `CLK_OUT`: output electrical


## Public Evaluation Contract (Non-Gold)

This section states evaluator-facing constraints that must be visible to the generated artifact.
It does not prescribe the internal implementation or reveal a gold solution.

Final EVAS transient setting:

```spectre
tran tran stop=300n maxstep=1n
```

Required public waveform columns in `tran.csv`:

- `clk_in`, `clk_out`

Use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Timing/checking-window contract:

- Reset-like input(s) `reset`, `rst_n` must be asserted only for startup/explicit reset checks, then deasserted early enough and kept deasserted through the post-reset checking window.
- For active-low reset inputs, avoid a finite-width pulse that returns the reset node low after release; use a waveform that remains high during checking.
- Clock-like input(s) `clock` must provide enough valid edges after reset/enable for the checker to sample settled outputs.
- Sequential outputs are sampled shortly after clock edges, so drive outputs with stable held state variables and `transition()` targets rather than glitchy combinational expressions.
- Public stimulus nodes used by the reference harness include: `clk_in`, `rst_n`.


## Public Evaluation Contract (Non-Gold)

Final EVAS transient setting:

```spectre
tran tran stop=300n maxstep=1n
```

Required public save statement:

```spectre
save clk_in clk_out
```

Use plain scalar save names for public observables; do not rely on instance-qualified or aliased save names.
Return exactly one fenced `spectre` code block and no prose outside the code block.
