# Task: vbr1_l1_gain_trim_controller:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Gain trim controller
- Domain: `voltage`
- Target artifact(s): `tb_gain_trim_controller_ref.scs`
- Supplied/reference support artifact(s): `gain_trim_controller.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `gain_trim_controller.va` declares module `gain_trim_controller` with positional ports: `clk`, `rst`, `meas`, `target`, `gain_ctrl`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=620n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `clk`
- `rst`
- `meas`
- `target`
- `gain_ctrl`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst`
- `meas`
- `target`

## Public Behavior Checks

- `reset_gain_control_near_0p30`
- `low_measured_value_increases_control`
- `high_measured_value_decreases_control`
- `gain_control_reaches_high_and_low_clamps`

## Output Contract

Return exactly one source artifact named `tb_gain_trim_controller_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_gain_trim_controller_tb

Write a Spectre testbench for a gain trim controller DUT.

The DUT module is `gain_trim_controller` with ports `clk, rst, meas, target, gain_ctrl`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `gain_trim_controller.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Initialize and reset `gain_ctrl` to 0.30 V on rising `clk` while `rst` is high.
- When `meas` is below `target - 0.02`, increase the control by 0.05 V; when above `target + 0.02`, decrease it by 0.05 V.
- Hold inside the deadband, clamp to 0.05 V to 0.85 V, and drive through `transition()`.

Stimulus and observability requirements:
- Provide target and measured waveforms that create low-measured and high-measured windows long enough to hit both clamps.
- Run transient analysis with clocked samples through trim increase, upper clamp, trim decrease, and lower clamp phases.

Return exactly one Spectre testbench file named `tb_gain_trim_controller_ref.scs`.
