---
name: evas-sim
description: Use when visible/public EVAS simulation is allowed for a Verilog-A voltage-domain model. Covers when EVAS applies, how to run evas-sim, minimal Spectre .scs syntax, save/output files, and common EVAS setup failures. Does not teach Verilog-A authoring.
---

# EVAS Simulation

Use this skill only when visible/public EVAS simulation is allowed. Do not use
hidden files, hidden checks, or reconstructed hidden logic. Use `veriloga` for
writing the `.va` module itself.

## Applicability

EVAS is for voltage-domain event-driven Verilog-A:

- `V(node) <+`
- `@(cross(...))`, `@(above(...))`, `@(initial_step)`, `@(timer(...))`
- `transition(...)`
- `if/else`, `case`, `for`, arrays, real/integer parameters

Do not rely on EVAS for:

- `I(...) <+`
- `ddt`, `idt`, `idtmod`, `laplace_*`
- noise sources
- transistor-level devices
- KCL/KVL solving
- AC/DC analysis
- Spectre `subckt` hierarchy

If EVAS passes but Spectre is the target, say `not Spectre-compiled`.

## Commands

Verify installation:

```bash
evas list
```

Fallback:

```bash
python -m evas list
```

Run a visible/public testbench:

```bash
evas simulate path/to/tb.scs -o output/run-name
```

If the task provides a visible smoke runner, prefer:

```bash
python3 run_visible_smoke.py
```

## Minimal Testbench Syntax

Use a Spectre-style `.scs` file near the `.va` files:

```spectre
simulator lang=spectre
global 0

Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=10n rise=10p fall=10p width=5n

XDUT (clk out) my_module

tran tran stop=100n maxstep=100p
save clk out
ahdl_include "./my_module.va"
```

Keep DUT source and testbench separate:

- `.va`: model only
- `.scs`: sources, instance, `tran`, `save`, `ahdl_include`

Use relative `ahdl_include` paths when possible.

## Output Files

After a successful run, inspect:

- `tran.csv`: waveform data, primary artifact
- `strobe.txt`: optional `$strobe` / display output
- `tran.png`: optional plot

Absence of `strobe.txt` or `tran.png` is not a failure by itself.

## Save Syntax

- Save explicit signals to keep `tran.csv` small.
- Fixed point: `save out:6f`
- Scientific notation: `save vin:10e`
- Integer/digital display: `save code:d`
- Escape Spectre bus angle brackets: `DOUT\<3\>`, not `DOUT<3>`.

## Common Failures

- `evas: command not found`: activate the environment or use `python -m evas`.
- Empty `tran.csv`: add explicit `save` statements.
- Missing compile marker: check `ahdl_include`, module name, and parse errors.
- All outputs zero: look for unsupported current-domain constructs or missing
  output contributions.
- Visible EVAS pass but hidden fail: visible test is weaker than hidden; do not
  infer hidden correctness from public smoke alone.
