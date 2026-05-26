# Task: vbr1_l2_programmable_stimulus_sequencer:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Stimulus and Source Generators
- Base function: Programmable stimulus sequencer
- Domain: `voltage`
- Target artifact(s): `tb_programmable_stimulus_sequencer.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate the target artifact: `tb_programmable_stimulus_sequencer.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `programmable_stimulus_sequencer.va` declares module `programmable_stimulus_sequencer` with positional ports from the public port contract below.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=90n maxstep=0.25n
```

The release harness expects these exact public scalar observables:

```text
clk rst mode gate out metric
```

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- ramp_segment_monotonic
- swept_chirp_segment_frequency_increases
- burst_prbs_gate_schedule
- mode_switch_continuity

## Output Contract

Return exactly these source artifacts:

- `tb_programmable_stimulus_sequencer.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

### Programmable stimulus sequencer (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Generate a programmable ramp, swept/chirp sine, and gated burst/PRBS stimulus schedule.

Module name: `programmable_stimulus_sequencer`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.


Public port contract:

```verilog
module programmable_stimulus_sequencer(clk, rst, mode, gate, out, metric);
input clk, rst, mode, gate;
output out, metric;
electrical clk, rst, mode, gate, out, metric;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. mode selects ramp, sine, or burst/PRBS behavior. gate enables the burst segment. out is the generated stimulus waveform. metric is a voltage-coded segment-status observable.

Saved waveform columns:

```text
clk rst mode gate out metric
```

Public behavior checks:

- ramp_segment_monotonic
- swept_chirp_segment_frequency_increases
- burst_prbs_gate_schedule
- mode_switch_continuity

Public transient contract:

```spectre
tran tran stop=90n maxstep=0.25n
```
