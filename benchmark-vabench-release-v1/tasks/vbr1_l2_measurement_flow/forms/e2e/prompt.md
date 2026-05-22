# Task: vbr1_l2_measurement_flow:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Measurement and Testbench Instrumentation
- Base function: Measurement flow
- Domain: `voltage`
- Target artifact(s): `final_step_file_metric_ref.va`, `tb_final_step_file_metric_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `final_step_file_metric_ref.va`, `tb_final_step_file_metric_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `final_step_file_metric_ref.va` declares module `final_step_file_metric_ref` with positional ports: `VDD`, `VSS`, `ref`, `metric_out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=20p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref`
- `metric_out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `ref`

## Public Behavior Checks

- `ref_edges_counted_on_expected_grid`
- `metric_out_normalizes_final_edge_count`
- `final_step_writes_candidate_metric_file`

## Output Contract

Return exactly these source artifacts:

- `final_step_file_metric_ref.va`
- `tb_final_step_file_metric_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

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
