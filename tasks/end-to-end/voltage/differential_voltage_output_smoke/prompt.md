Write a Verilog-A module named `differential_voltage_output_ref`.

# Task: differential_voltage_output_smoke

## Objective

Write a Verilog-A differential output driver with digital-like input and enable controls. The task is a driver model, not a free-running voltage source.

## Specification

- **Module name**: `differential_voltage_output_ref`
- **Ports**: `VDD`, `VSS`, `din`, `en`, `outp`, `outn` - all `electrical`
- **Behavior**:
  - Use `vcm=0.45 V`, `vod=0.4 V`, and `vth=0.45 V` by default.
  - When `en` is LOW, drive both outputs to the common-mode level.
  - When `en` is HIGH and `din` is LOW, drive `outp-outn` negative.
  - When `en` is HIGH and `din` is HIGH, drive `outp-outn` positive.
  - Keep both outputs bounded between `VSS` and `VDD` and use finite `transition(...)` edges.
- **Expected observable behavior**:
  - Disabled windows have near-zero differential output.
  - Enabled low-input windows have negative differential output.
  - Enabled high-input windows have positive differential output.
  - The output common-mode remains near `vcm`.

## Constraints

- Use `transition(...)` for the driven outputs.
- Pure voltage-domain only.
- No `I() <+`, `ddt()`, or `idt()`.

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `din`: input electrical
- `en`: input electrical
- `outp`: output electrical
- `outn`: output electrical

## Output Contract (MANDATORY)

- Return exactly two fenced code blocks:
  - first block: Verilog-A DUT (` ```verilog-a ... ``` `)
  - second block: Spectre testbench (` ```spectre ... ``` `)
- The Spectre testbench must include the DUT with `ahdl_include "<module>.va"`.
- Use a single `tran` analysis and include the required `save` signals for checker evaluation.


## Public Evaluation Contract (Non-Gold)

This section states evaluator-facing constraints that must be visible to the generated artifact.
It does not prescribe the internal implementation or reveal a gold solution.

Final EVAS transient setting:

```spectre
tran tran stop=100n maxstep=100p errpreset=conservative
```

Required public waveform columns in `tran.csv`:

- `time`, `din`, `en`, `outp`, `outn`

Use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Timing/checking-window contract:

- Public stimulus nodes used by the reference harness include: `VDD`, `VSS`, `din`, `en`.
