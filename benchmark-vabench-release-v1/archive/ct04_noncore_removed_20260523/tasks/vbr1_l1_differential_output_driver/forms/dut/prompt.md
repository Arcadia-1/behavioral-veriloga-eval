# Task: vbr1_l1_differential_output_driver:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Differential output driver
- Domain: `voltage`
- Target artifact(s): `differential_voltage_output_ref.va`
- Supplied/reference support artifact(s): `tb_differential_voltage_output_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `differential_voltage_output_ref.va` declares module `differential_voltage_output_ref` with positional ports: `VDD`, `VSS`, `din`, `en`, `outp`, `outn`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=100n maxstep=100p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `din`
- `en`
- `outp`
- `outn`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `driver_disabled_common_mode`
- `driver_polarity_tracks_din`
- `driver_common_mode_stable`

## Output Contract

Return exactly one source artifact named `differential_voltage_output_ref.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Differential output driver DUT

Write the Verilog-A DUT artifact(s) for `Differential output driver`.

This is a function-checked DUT task, not a generic companion wrapper. The
public contract below defines the exact module interface, voltage-domain
behavior, and waveform observables used by the release checker.

Domain: pure voltage-domain behavioral Verilog-A.

## Module Contract

- Declaration: `differential_voltage_output_ref(VDD, VSS, din, en, outp, outn)`

Ports:

- `VDD`, `VSS`: electrical supply rails
- `din`: input electrical logic-like data control, 0 V low and 0.9 V high
- `en`: input electrical enable control, 0 V disabled and 0.9 V enabled
- `outp`, `outn`: output electrical differential driver outputs

## Behavioral Contract

- when `en` is low, drive both outputs to the common-mode level
- when `en` is high and `din` is low, drive `outp-outn` negative
- when `en` is high and `din` is high, drive `outp-outn` positive
- keep both outputs bounded between `VSS` and `VDD` with finite `transition(...)` edges

## Public Evaluation Observables

The companion validation testbench saves these waveform columns:

- `din`
- `en`
- `outp`
- `outn`
