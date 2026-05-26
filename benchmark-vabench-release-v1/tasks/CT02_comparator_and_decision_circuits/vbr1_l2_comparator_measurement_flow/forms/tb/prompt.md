# Task: vbr1_l2_comparator_measurement_flow:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Comparator and Decision Circuits
- Base function: Single-ramp comparator offset measurement flow
- Domain: `voltage`
- Target artifact(s): `tb_comparator_offset_search_ref.scs`
- Supplied/reference support artifact(s): `comparator_offset_search_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `comparator_offset_search_ref.va` declares module `comparator_offset_search_ref` with positional ports: `vdd`, `vss`, `inp`, `inn`, `outp`, `trip_v`, `offset_est`, `valid`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=100n maxstep=50p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `inp`
- `inn`
- `outp`
- `trip_v`
- `offset_est`
- `valid`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `inn`
- `inp`

## Public Behavior Checks

- `comparator_output_low_before_trip`
- `comparator_output_high_after_trip`
- `outp_first_trip_near_static_offset`
- `measurement_valid_latches_after_trip`
- `valid_first_assertion_near_trip`
- `trip_voltage_near_inn_plus_offset`
- `offset_estimate_near_static_offset`
- `measurement_outputs_hold_after_valid`

## Output Contract

Return exactly one source artifact named `tb_comparator_offset_search_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Single-ramp comparator offset measurement flow Testbench Companion

Write a Spectre transient testbench for the `Single-ramp comparator offset measurement flow` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- instantiate `comparator_offset_search_ref` with ports `vdd vss inp inn outp trip_v offset_est valid`
- drive `inn` at 0.500 V and perform a single ramp of `inp` from 0.490 V to 0.520 V over the transient
- save exactly the public scalar observables needed by the checker: `inp`, `inn`, `outp`, `trip_v`, `offset_est`, and `valid`
- include the Verilog-A behavioral module under test
- exercise the crossing so `outp`, `valid`, `trip_v`, and `offset_est` all settle after the expected 5 mV offset trip point
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
