# Task: vbr1_l1_bang_bang_phase_detector:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: PLL Clock and Timing Systems
- Base function: Bang-bang phase detector
- Domain: `voltage`
- Target artifact(s): `bbpd_ref.va`
- Supplied/reference support artifact(s): `tb_bbpd_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `bbpd_ref.va` declares module `bbpd_ref` with positional ports: `data`, `clk`, `retimed_data`, `up`, `down`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=60n maxstep=50p
```

The release harness expects these exact public scalar observables:

- `data`
- `clk`
- `retimed_data`
- `up`
- `down`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `data_edges_trigger_up_or_down`
- `up_down_pulses_present`
- `up_down_not_high_together`

## Output Contract

Return exactly one source artifact named `bbpd_ref.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a bang-bang (binary) phase-frequency detector for a CDR.

Module name: `bbpd_ref`. Three inputs: DATA, CLK, and RETIMED_DATA. Outputs: UP and DOWN pulses. Edge-triggered on DATA transitions.

Ports:
- `data`: input electrical
- `clk`: input electrical
- `retimed_data`: input electrical
- `up`: output electrical
- `down`: output electrical

Implement this in Verilog-A behavioral modeling.
