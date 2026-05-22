# Task: vbr1_l1_event_pulse_stretcher:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: Retriggerable one-shot pulse stretcher
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `event_pulse_stretcher` with positional ports: `trig`, `rst`, `pulse`.
- `dut_fixed.va` declares module `event_pulse_stretcher` with positional ports: `trig`, `rst`, `pulse`.

## Public Behavior Checks

- `trigger_creates_pulse`
- `retrigger_refreshes_pulse_deadline`
- `pulse_stays_high_through_burst`
- `reset_forces_low`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Retriggerable one-shot pulse stretcher (bugfix)

Repair the supplied buggy Verilog-A implementation.

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
