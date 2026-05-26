# Task: vbr1_l1_gain_estimator:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Measurement Instrumentation Flows
- Base function: Gain estimator
- Domain: `voltage`
- Target artifact(s): `tb_gain_estimator_ref.scs`
- Supplied/reference support artifact(s): `gain_estimator.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module, drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Return exactly one source artifact named `tb_gain_estimator_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Spectre transient testbench for the supplied `gain_estimator` behavioral measurement helper.

Public requirements:

- Instantiate `gain_estimator` with ports `(VDD VSS vinp vinn voutp voutn gain_out valid)`.
- Drive `VDD=0.9 V` and `VSS=0 V`.
- Provide a differential input with about 60 mV peak-to-peak span.
- Provide a differential output with about 360 mV peak-to-peak span, corresponding to gain near 6.
- Run long enough for `valid` to assert and for `gain_out` to settle.
- Save exactly `vinp`, `vinn`, `voutp`, `voutn`, `gain_out`, and `valid`.
- Use voltage-domain behavioral sources only; avoid transistor-level devices, AC/noise analysis, and current-domain solver assumptions.
