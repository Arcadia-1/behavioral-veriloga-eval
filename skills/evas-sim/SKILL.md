---
name: evas-sim
description: Use when working with visible/public EVAS simulation for an already-written Verilog-A voltage-domain model: checking EVAS compatibility, running evas-sim on a Spectre .scs testbench, reading tran.csv or strobe.txt outputs, debugging EVAS simulation setup, or deciding whether EVAS can simulate a model. Do not use as the primary Verilog-A authoring guide.
---

# EVAS Simulation

Use this skill only for visible/public simulation of an already-written
Verilog-A voltage-domain model. Do not use it to write the DUT itself; use the
separate `veriloga-writer` skill for authoring.

## Compatibility Check

Before running EVAS, inspect the `.va` file. Continue only if the model is
voltage-domain behavioral.

Usually OK:

- `V(node) <+` and differential `V(a,b) <+`
- `@(cross(...))`, `@(above(...))`, `@(initial_step)`, `@(timer(...))`,
  `@(final_step)`
- `transition()` with delay/rise/fall
- `if/else`, `for`, `case`, `begin/end`
- arrays and real/integer/string parameters
- common math functions and SI suffixes
- `$abstime`, `$temperature`, `$vt`, `$bound_step`
- `$display`, `$strobe`, `$random`, `$dist_uniform`, `$rdist_normal`
- file output calls such as `$fopen`, `$fclose`, `$fstrobe`, `$fwrite`,
  `$fdisplay`

Do not use EVAS for:

- `I(...) <+`, `q(...) <+`, `ddt(...)`, `idt(...)`, `idtmod(...)`
- `laplace_*`, `white_noise`, `flicker_noise`
- transistor-level devices or KCL-based solving
- AC/DC analysis
- Spectre `subckt` hierarchy

EVAS acceptance is not the same as Spectre portability. Runtime-indexed
electrical-bus reads such as `V(DIN[i])` may run in EVAS while still failing in
Cadence/Spectre. If Spectre is the target and Spectre was not run, say
explicitly: `not Spectre-compiled`.

## Install And Verify

```bash
uv tool install evas-sim
```

Fallback inside a virtualenv:

```bash
pip install evas-sim
```

Verify:

```bash
evas list
```

If `evas` is not on `PATH`, use:

```bash
python -m evas list
```

## Run EVAS

Run a custom visible/public Spectre-style testbench:

```bash
evas simulate path/to/tb.scs -o output/mydesign
```

Bundled examples:

```bash
evas run clk_div
evas run comparator
evas run comparator --tb tb_cmp_strongarm.scs
evas run digital_basics --tb tb_not_gate.scs
```

Output files:

- `tran.csv`: primary time-domain waveform artifact.
- `strobe.txt`: optional display/strobe log.
- `tran.png`: optional plot.

Absence of `strobe.txt` or `tran.png` is not by itself a simulation failure.

## Testbench Shape

Keep simulation projects split into exactly two files:

- `dut.va`: Verilog-A model only, no stimulus and no analysis.
- `tb_*.scs`: testbench only, with sources, DUT instance, `tran`, `save`, and
  `ahdl_include`.

Recommended `.scs` ordering:

1. Header comments.
2. Sources.
3. DUT instance.
4. `simulatorOptions`.
5. `tran`.
6. Optional Spectre `info` statements.
7. `saveOptions` and explicit `save`.
8. `ahdl_include`, last.

Minimal shape:

```spectre
simulator lang=spectre
global 0

Vvdd (vdd 0) vsource type=dc dc=0.9
Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=10n rise=10p fall=10p width=5n

IDUT (clk vdd out) my_module vdd=0.9

simulatorOptions options reltol=1e-4 vabstol=1e-6 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12
tran tran stop=200n errpreset=conservative
save clk:2e out:6f

ahdl_include "./my_module.va"
```

For hand-written portable testbenches, use relative `ahdl_include` paths. For
flow-generated temporary testbenches, write the `.scs` next to the `.va` files
or use an absolute path deliberately.

## Bus And Save Syntax

- In a DUT instance port list, enumerate bus bits explicitly: `DOUT\<9\>
  DOUT\<8\> ... DOUT\<0\>`.
- In a `save` statement, range shorthand is allowed: `save DOUT\<9\>:0`.
- Escape angle brackets in Spectre net names: `\<9\>`, not `<9>`.
- Use explicit `save` lists for lean `tran.csv` files.
- `save sig:6f` gives fixed-point output, `save sig:10e` scientific notation,
  and `save code:d` integer/digital display.

## Common Issues

- `evas: command not found`: activate the environment or use `python -m evas`.
- Empty `tran.csv`: add explicit `save` statements.
- All voltages are zero: the model may use unsupported current-domain
  constructs such as `I() <+`.
- No `Compiled Verilog-A module` marker: check parse errors and
  `ahdl_include` paths.
- EVAS passes but Spectre rejects the model: remove Spectre-hostile constructs,
  especially runtime-indexed electrical-bus reads.
