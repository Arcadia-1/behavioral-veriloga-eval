# Task: vbr1_l1_programmable_gain_amplifier:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Programmable gain amplifier
- Domain: `voltage`
- Target artifact(s): `programmable_gain_amplifier.va`, `tb_programmable_gain_amplifier.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `programmable_gain_amplifier.va`, `tb_programmable_gain_amplifier.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `programmable_gain_amplifier.va` declares module `programmable_gain_amplifier` with positional ports: `clk`, `rst`, `gain_sel`, `vin`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=90n maxstep=250p
```

The release harness expects these exact public scalar observables:

- `clk`
- `rst`
- `gain_sel`
- `vin`
- `out`
- `metric`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst`
- `gain_sel`
- `vin`

## Public Behavior Checks

- `gain_select_changes_slope`
- `sampled_gain_holds_between_clock_edges`
- `common_mode_is_preserved`
- `rail_clamps_with_clip_metric`
- `reset_returns_to_unity_gain`

## Output Contract

Return exactly these source artifacts:

- `programmable_gain_amplifier.va`
- `tb_programmable_gain_amplifier.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain Verilog-A programmable gain amplifier.

The gain code is sampled on rising `clk` edges:
- reset selects unity gain and returns the output to the common-mode voltage.
- `gain_sel=0` selects a low gain.
- `gain_sel=1` selects a high gain.
- The output is `vcm + gain * (V(vin)-vcm)` with rail clamps.
- `metric` is high when the unclamped target clips to either rail.
- The testbench should exercise reset, low-gain unclipped operation, high-gain positive clipping, high-gain negative clipping, and a later high-gain clipped segment after a gain selection change.

Module name: `programmable_gain_amplifier`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL solving assumptions.

Public port contract:

```verilog
module programmable_gain_amplifier(clk, rst, gain_sel, vin, out, metric);
```

Saved waveform columns:

```text
clk rst gain_sel vin out metric
```

Public transient contract:

```spectre
tran tran stop=90n maxstep=250p
```
