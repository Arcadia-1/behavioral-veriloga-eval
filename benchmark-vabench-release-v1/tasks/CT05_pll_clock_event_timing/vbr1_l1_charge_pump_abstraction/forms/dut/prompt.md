# Task: vbr1_l1_charge_pump_abstraction:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: Voltage-domain charge-pump control abstraction
- Domain: `voltage`
- Target artifact(s): `charge_pump_abstraction.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `charge_pump_abstraction.va` declares module `charge_pump_abstraction` with positional ports: `clk`, `rst`, `up`, `dn`, `vctrl`, `metric`.

## Public Behavior Checks

- `up_pulse_increases_control`
- `down_pulse_decreases_control`
- `control_voltage_clamped`

## Output Contract

Return exactly one source artifact named `charge_pump_abstraction.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Voltage-domain charge-pump control abstraction (spec-to-va)

Write the Verilog-A behavioral module only.

Behavioral intent:

Represent UP/DN pulse effects as a voltage-domain control-node update without current contributions.

Module name: `charge_pump_abstraction`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module charge_pump_abstraction(clk, rst, up, dn, vctrl, metric);
input clk, rst, up, dn;
output vctrl, metric;
electrical clk, rst, up, dn, vctrl, metric
```

Signal contract:

clk, rst, up, and dn are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. On each rising clk edge, an UP-only pulse increases vctrl, a DN-only pulse decreases vctrl, simultaneous or absent pulses hold the control voltage, and rst high resets vctrl to midscale. vctrl is a bounded loop-control voltage. metric is a voltage-coded UP/DN/hold status observable.

Saved waveform columns:

```text
clk rst up dn vctrl metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```
