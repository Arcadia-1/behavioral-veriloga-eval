# Task: vbr1_l1_window_comparator_detector:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Window comparator/detector
- Domain: `voltage`
- Target artifact(s): `cross_hysteresis_window_ref.va`
- Supplied/reference support artifact(s): `tb_cross_hysteresis_window_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `cross_hysteresis_window_ref.va` declares module `cross_hysteresis_window_ref` with positional ports: `VDD`, `VSS`, `vin`, `out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=90n maxstep=20p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `vin`
- `out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `cross_hysteresis_window`

## Output Contract

Return exactly one source artifact named `cross_hysteresis_window_ref.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Window comparator/detector DUT

Write the Verilog-A DUT artifact(s) for `Window comparator/detector`.

This is a function-checked DUT task, not a generic companion wrapper. The
public contract below defines the exact module interface, voltage-domain
behavior, and waveform observables used by the release checker.

Domain: pure voltage-domain behavioral Verilog-A.

## Module Contract

- Declaration: `cross_hysteresis_window_ref(VDD, VSS, vin, out)`

Ports:

- `VDD`, `VSS`: electrical supply rails
- `vin`: input electrical waveform
- `out`: output electrical window/hysteresis state

## Behavioral Contract

- start low
- switch high when `vin` rises above 0.6 V
- switch low when `vin` falls below 0.3 V
- hold state between thresholds and drive output with `transition(...)`

## Public Evaluation Observables

The companion validation testbench saves these waveform columns:

- `time`
- `vin`
- `out`
