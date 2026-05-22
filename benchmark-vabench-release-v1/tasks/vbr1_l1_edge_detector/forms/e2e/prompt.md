# Task: vbr1_l1_edge_detector:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: Edge detector
- Domain: `voltage`
- Target artifact(s): `edge_detector.va`, `tb_edge_detector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `edge_detector.va`, `tb_edge_detector_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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
- `reset_keeps_pulse_low_before_release`

## Output Contract

Return exactly these source artifacts:

- `edge_detector.va`
- `tb_edge_detector_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_edge_detector_e2e

Write both the Verilog-A DUT and Spectre testbench for a voltage-domain rising
edge detector.

The DUT module must be named `edge_detector` and use electrical ports `sig`,
`rst_n`, and `pulse`. `rst_n` is active low. After reset is released, each
rising crossing of `sig` should generate a short high pulse on `pulse`; falling
crossings must not generate a pulse.

The testbench must stimulate reset and multiple input transitions, save all
public observables, and run a transient analysis suitable for fixed-time pulse
checks.

Return exactly two files: `edge_detector.va` and `tb_edge_detector_ref.scs`.
