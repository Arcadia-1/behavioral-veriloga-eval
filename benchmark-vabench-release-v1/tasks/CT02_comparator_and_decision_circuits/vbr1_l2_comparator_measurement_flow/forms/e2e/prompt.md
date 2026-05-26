# Task: vbr1_l2_comparator_measurement_flow:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Comparator and Decision Circuits
- Base function: Single-ramp comparator offset measurement flow
- Domain: `voltage`
- Target artifact(s): `comparator_offset_search_ref.va`, `tb_comparator_offset_search_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `comparator_offset_search_ref.va`, `tb_comparator_offset_search_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `comparator_offset_search_ref.va`
- `tb_comparator_offset_search_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain Verilog-A single-ramp comparator offset
measurement flow. This is an L2 task: the generated artifact must include both
the comparator decision and measurement observables that latch the detected
trip voltage and offset estimate during one controlled transient input ramp.

Module name: `comparator_offset_search_ref`.

Requirements:

1. Ports, in order: `vdd`, `vss`, `inp`, `inn`, `outp`, `trip_v`, `offset_est`, `valid`
2. Built-in offset parameter `vos = 5m`
3. Comparator output `outp` switches high when `V(inp, vss) - V(inn, vss) > vos`
4. On the rising threshold crossing, latch `trip_v = V(inp, vss)` and `offset_est = V(inp, vss) - V(inn, vss)`
5. Drive `valid` low before the first rising crossing and high after the measurement latches
6. Keep `trip_v` and `offset_est` stable after `valid` goes high
7. Use portable Verilog-A event constructs: `@(initial_step)`, directional `cross()` events, and `transition()`
8. The benchmark testbench performs a single ramp of `inp` from 0.490 V toward 0.520 V with `inn = 0.500 V`; the expected latched trip voltage is near 0.505 V and the expected offset estimate is near 0.005 V

Ports:
- `vdd`: electrical
- `vss`: electrical
- `inp`: electrical
- `inn`: electrical
- `outp`: electrical (power rail)
- `trip_v`: electrical measurement voltage
- `offset_est`: electrical measurement voltage
- `valid`: electrical validity flag on the power rail
