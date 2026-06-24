# Resettable Integrator

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Resettable integrator
- Domain: `voltage`
- Target artifact(s): `resettable_integrator.va`
- Supplied/reference support artifact(s): `tb_resettable_integrator_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `resettable_integrator.va` declares module `resettable_integrator` with positional ports: `vin`, `rst`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the evaluator:

```spectre
tran tran stop=320n maxstep=500p
```

The evaluator expects these exact public scalar observables:

- `vin`
- `rst`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `input_drive_present`
- `reset_pulse_exercised`
- `pre_reset_output_integrates_up`
- `reset_clears_integrator`
- `post_reset_integration_restarts`

## Output Contract

Return exactly one source artifact named `resettable_integrator.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Write a pure voltage-domain Verilog-A module for a resettable timer integrator.

The DUT module is `resettable_integrator` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Keep the public parameters `vth = 0.45`, `gain = 1.0e9`, `dt = 1n`, `vmax = 0.85`, and `tr = 500p`.
- Initialize an internal real accumulator to 0 V at `initial_step`.
- Use `@(timer(0, dt))` as the only state update cadence. With the default parameters this is a 1 ns update.
- Treat `rst` as active high when `V(rst) > vth`. While reset is high, set the accumulator to exactly 0 V and hold `vout` near 0 V.
- When reset is low, update the accumulator by `gain * V(vin) * dt` on each timer event.
- After every update, clamp the accumulator to the closed range 0 V to `vmax`.
- After a reset pulse returns low, integration must restart from 0 V using the same update rule.
- Drive `vout` from the accumulator using `transition(acc, 0, tr, tr)`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.
