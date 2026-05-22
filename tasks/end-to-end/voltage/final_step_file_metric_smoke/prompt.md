Write a Verilog-A module named `final_step_file_metric_ref`.

# Task: final_step_file_metric_smoke

## Objective

Write a Verilog-A measurement helper that counts input edges, exposes the normalized count on a voltage output, and writes the final metric to a file during `@(final_step)`.

Public behavior requirements:
- The Spectre testbench should drive `VDD=0.9 V`, `VSS=0 V`, and a `ref` pulse train whose rising edges occur at 10 ns, 30 ns, 50 ns, and 70 ns.
- The DUT should count rising crossings of `ref` above the logic threshold and normalize the count by 4.
- `metric_out` should settle after each edge to the normalized count multiplied by `VDD`, producing approximately 0.225 V, 0.45 V, 0.675 V, and 0.9 V.
- During `@(final_step)`, write `candidate.out` with exactly one metric record of the form `count=<integer> metric=<real>`, where the final count is 4 and the final metric is approximately 1.000.
- Use `$fopen`, `$fwrite`, and `$fclose` for the file output. Use voltage-domain contributions and smooth transitions; do not use current-domain branch contributions.

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `ref`: input electrical
- `metric_out`: output electrical

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
tran tran stop=80n maxstep=20p errpreset=conservative
```

Required public waveform columns in `tran.csv`:

- `time`, `ref`, `metric_out`

Use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Timing/checking-window contract:

- Public stimulus nodes used by the reference harness include: `VDD`, `VSS`, `ref`.
