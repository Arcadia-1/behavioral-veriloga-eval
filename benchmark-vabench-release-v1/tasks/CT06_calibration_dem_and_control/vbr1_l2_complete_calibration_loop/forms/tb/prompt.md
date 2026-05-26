# Task: vbr1_l2_complete_calibration_loop:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Calibration, DEM, and Control
- Base function: Complete calibration loop
- Domain: `voltage`
- Target artifact(s): `tb_complete_calibration_loop.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate the target artifact: `tb_complete_calibration_loop.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `complete_calibration_loop.va` declares module `complete_calibration_loop` with positional ports from the public port contract below.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=0.5n
```

The release harness expects these exact public scalar observables:

```text
clk rst vin out metric
```

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- raw_error_is_corrected
- bounded_negative_feedback_response
- metric_tracks_convergence

## Output Contract

Return exactly these source artifacts:

- `tb_complete_calibration_loop.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

### Complete calibration loop (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Close a simple calibration loop from error stimulus through controller and actuator output.

Module name: `complete_calibration_loop`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.


Public port contract:

```verilog
module complete_calibration_loop(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is the external offset/error stimulus around 0.45 V. The internal controller drives correction opposite the measured residual error, out is the bounded corrected plant response, and metric is high when out is close to 0.45 V.

Saved waveform columns:

```text
clk rst vin out metric
```

Public behavior checks:

- raw_error_is_corrected
- bounded_negative_feedback_response
- metric_tracks_convergence

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```
