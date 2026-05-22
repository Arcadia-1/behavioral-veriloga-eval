# Task: vbr1_l1_event_pulse_stretcher:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: Retriggerable one-shot pulse stretcher
- Domain: `voltage`
- Target artifact(s): `event_pulse_stretcher.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `event_pulse_stretcher.va` declares module `event_pulse_stretcher` with positional ports: `trig`, `rst`, `pulse`.

## Public Behavior Checks

- `trigger_creates_pulse`
- `retrigger_refreshes_pulse_deadline`
- `pulse_stays_high_through_burst`
- `reset_forces_low`

## Output Contract

Return exactly one source artifact named `event_pulse_stretcher.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Retriggerable one-shot pulse stretcher (spec-to-va)

Write the Verilog-A behavioral module only.

Behavioral intent:

Convert trigger crossings into a retriggerable one-shot pulse: every trigger while active refreshes the falling deadline.

Module name: `event_pulse_stretcher`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module event_pulse_stretcher(trig, rst, pulse);
input trig, rst;
output pulse;
electrical trig, rst, pulse
```

Signal contract:

trig and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. pulse is a voltage-coded output pulse. Each rising trig edge refreshes the pulse deadline to trigger_time + 4 ns; rst high forces pulse low.

Saved waveform columns:

```text
trig rst pulse
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```
