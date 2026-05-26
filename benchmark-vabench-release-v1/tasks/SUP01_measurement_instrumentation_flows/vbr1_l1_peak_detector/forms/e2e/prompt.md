# Task: vbr1_l1_peak_detector:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Measurement Instrumentation Flows
- Base function: Peak detector
- Domain: `voltage`
- Target artifact(s): `peak_detector.va`, `tb_peak_detector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `peak_detector.va`, `tb_peak_detector_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `peak_detector.va` declares module `peak_detector` with positional ports: `vin`, `rst`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=180n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `vin`
- `rst`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vin`
- `rst`

## Public Behavior Checks

- `first_peak_is_held`
- `reset_clears_peak`
- `second_peak_updates_to_larger_value`

## Output Contract

Return exactly these source artifacts:

- `peak_detector.va`
- `tb_peak_detector_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_peak_detector_e2e

Write both the Verilog-A DUT and Spectre testbench for a resettable peak detector.

The DUT module is `peak_detector` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Track the maximum observed `vin` value using a timer-sampled internal peak.
- High `rst` clears the peak to 0 V.
- Drive `vout` from the peak value through `transition()`.

Required testbench behavior:
- Apply a first input peak, reset clear, and a second larger peak.
- Save `vin`, `rst`, and `vout`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `peak_detector.va` and `tb_peak_detector_ref.scs`.
