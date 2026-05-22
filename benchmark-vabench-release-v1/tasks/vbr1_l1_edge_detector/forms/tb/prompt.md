# Task: vbr1_l1_edge_detector:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: Edge detector
- Domain: `voltage`
- Target artifact(s): `tb_edge_detector_ref.scs`
- Supplied/reference support artifact(s): `edge_detector.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `edge_detector.va` declares module `edge_detector` with positional ports: `sig`, `rst_n`, `pulse`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=180n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `sig`
- `rst_n`
- `pulse`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `sig`
- `rst_n`

## Public Behavior Checks

- `pulse_high_at_safe_windows_after_rising_sig_edges`
- `pulse_low_before_next_falling_edge_windows`

## Output Contract

Return exactly one source artifact named `tb_edge_detector_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_edge_detector_tb

Write a Spectre testbench for a Verilog-A module named `edge_detector` with
ports `sig rst_n pulse`.

The testbench should apply active-low reset, then drive multiple rising and
falling transitions on `sig`. Save `sig`, `rst_n`, and `pulse`. Use a transient
analysis with enough stop time and maxstep resolution for fixed-time pulse
checks.

Return exactly one Spectre testbench file named `tb_edge_detector_ref.scs`.
