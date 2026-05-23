# Task: vbr1_l2_event_controller:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Data Converters
- Base function: Conversion event controller
- Domain: `voltage`
- Target artifact(s): `conversion_event_controller.va`, `tb_conversion_event_controller.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `conversion_event_controller.va`, `tb_conversion_event_controller.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `conversion_event_controller.va` declares module `conversion_event_controller` with positional ports: `vdd`, `vss`, `rst`, `start`, `cmp_done`, `sample_en`, `compare_en`, `readout_en`, `done`, `state_mon`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=170n maxstep=0.2n errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `rst`
- `start`
- `cmp_done`
- `sample_en`
- `compare_en`
- `readout_en`
- `done`
- `state_mon`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `rst`
- `start`
- `cmp_done`

## Public Behavior Checks

- `sample_phase_after_start_edges`
- `compare_phase_ends_on_cmp_done_or_timeout`
- `readout_and_done_follow_compare_phase`

## Output Contract

Return exactly these source artifacts:

- `conversion_event_controller.va`
- `tb_conversion_event_controller.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `conversion_event_controller` and a Spectre
transient testbench for a mixed-signal sample/compare/readout control flow.

The controller sequences an analog front-end transaction:

1. Active-high `rst` clears all outputs and returns the controller to idle.
2. A rising `start` edge with reset low begins a sample phase by asserting
   `sample_en`.
3. After a fixed 12 ns sample window, `sample_en` falls and `compare_en` rises.
4. During compare, a rising `cmp_done` edge moves immediately into readout; if
   no `cmp_done` arrives, a 28 ns timeout moves into readout.
5. `readout_en` stays high for 16 ns, then `done` asserts for 8 ns and the
   controller returns to idle.
6. `state_mon` encodes idle/sample/compare/readout/done as monotonic
   voltage-coded state levels.

The public testbench must drive one normal transaction where `cmp_done` ends
the compare phase and one timeout transaction with no second `cmp_done`. Save
all public observables listed above. Use voltage-domain contributions and
smoothed output transitions; do not use current-domain branch contributions,
transistor-level devices, AC/noise analysis, `ddt()`, or `idt()`.

Ports:
- `vdd`: inout electrical power rail
- `vss`: inout electrical reference rail
- `rst`: input electrical active-high reset
- `start`: input electrical transaction-start event
- `cmp_done`: input electrical comparator-done event
- `sample_en`: output electrical sample control
- `compare_en`: output electrical compare control
- `readout_en`: output electrical readout control
- `done`: output electrical transaction-complete status
- `state_mon`: output electrical state monitor
