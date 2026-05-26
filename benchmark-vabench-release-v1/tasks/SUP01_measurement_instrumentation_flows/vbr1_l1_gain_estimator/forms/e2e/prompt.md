# Task: vbr1_l1_gain_estimator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Measurement Instrumentation Flows
- Base function: Gain estimator
- Domain: `voltage`
- Target artifact(s): `gain_estimator.va`, `tb_gain_estimator_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `gain_estimator.va`, `tb_gain_estimator_ref.scs`.
- The Spectre testbench must exercise the generated measurement helper through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `gain_estimator.va` declares module `gain_estimator` with positional ports: `VDD`, `VSS`, `vinp`, `vinn`, `voutp`, `voutn`, `gain_out`, `valid`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=240n maxstep=200p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `vinp`
- `vinn`
- `voutp`
- `voutn`
- `gain_out`
- `valid`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `vinp`
- `vinn`
- `voutp`
- `voutn`

## Public Behavior Checks

- `valid_asserts_after_observation_window`
- `waveform_gain_is_about_six`
- `gain_out_matches_waveform_derived_gain`

## Output Contract

Return exactly these source artifacts:

- `gain_estimator.va`
- `tb_gain_estimator_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a voltage-domain behavioral gain measurement helper and a Spectre transient testbench.

Required DUT behavior:

- The module observes differential input `V(vinp, vinn)` and differential output `V(voutp, voutn)`.
- It periodically samples the observed waveforms using `@(timer(...))`.
- After `start_time`, it tracks input and output peak-to-peak span.
- Once the input span exceeds `min_input_span`, it asserts `valid` high.
- It estimates gain as `output_span / input_span`.
- It drives `gain_out` as a voltage-coded metric: `VDD * estimated_gain / gain_scale`.
- Use voltage contributions and smoothed transitions only. Do not use current contributions, `ddt()`, or `idt()`.

Required testbench behavior:

- Drive `VDD=0.9 V` and `VSS=0 V`.
- Provide a differential input with about 60 mV peak-to-peak span.
- Provide a differential output with about 360 mV peak-to-peak span, corresponding to gain near 6.
- Run long enough for `valid` to assert and for `gain_out` to settle.
- Save exactly `vinp`, `vinn`, `voutp`, `voutn`, `gain_out`, and `valid`.

This is a reusable measurement-helper task. It is intentionally separate from the L2 gain-extraction flow, which exercises a composed source/dither/amplifier path.
