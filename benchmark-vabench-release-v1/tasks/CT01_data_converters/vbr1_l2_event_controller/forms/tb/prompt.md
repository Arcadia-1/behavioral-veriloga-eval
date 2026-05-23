# Task: vbr1_l2_event_controller:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Data Converters
- Base function: Conversion event controller
- Domain: `voltage`
- Target artifact(s): `tb_conversion_event_controller.scs`
- Supplied/reference support artifact(s): `conversion_event_controller.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Return exactly one source artifact named `tb_conversion_event_controller.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Conversion Event Controller Testbench Companion

Write a Spectre transient testbench for the `conversion_event_controller`
behavioral Verilog-A release task.

The testbench must instantiate the supplied controller, drive `vdd=0.9 V`,
`vss=0 V`, apply active-high reset, then run two transactions:

1. A normal sample/compare/readout transaction where `start` rises near 10 ns
   and `cmp_done` rises during the compare phase.
2. A timeout transaction where `start` rises near 90 ns and no matching
   `cmp_done` event arrives, so the controller leaves compare by timeout.

Save `rst`, `start`, `cmp_done`, `sample_en`, `compare_en`, `readout_en`,
`done`, and `state_mon` using plain scalar save names. Use one transient
analysis matching the public transient contract. Avoid transistor-level devices,
AC/noise analysis, and current-domain solver assumptions.
