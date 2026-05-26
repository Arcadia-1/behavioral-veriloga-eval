# Task: vbr1_l1_peak_detector:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Measurement Instrumentation Flows
- Base function: Peak detector
- Domain: `voltage`
- Target artifact(s): `tb_peak_detector_ref.scs`
- Supplied/reference support artifact(s): `peak_detector.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Return exactly one source artifact named `tb_peak_detector_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_peak_detector_tb

Write a Spectre testbench for a resettable peak detector DUT.

The DUT module is `peak_detector` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `peak_detector.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Track the maximum observed `vin` value using a timer-sampled internal peak.
- High `rst` clears the peak to 0 V.
- Drive `vout` from the peak value through `transition()`.

Stimulus and observability requirements:
- Apply a first input peak, reset clear, and a second larger peak.
- Save `vin`, `rst`, and `vout`.

Return exactly one Spectre testbench file named `tb_peak_detector_ref.scs`.
