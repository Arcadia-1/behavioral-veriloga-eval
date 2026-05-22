# Task: vbr1_l2_comparator_measurement_flow:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Comparators and Decision Circuits
- Base function: Comparator measurement flow
- Domain: `voltage`
- Target artifact(s): `comparator_offset_search_ref.va`, `tb_comparator_offset_search_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `comparator_offset_search_ref.va`, `tb_comparator_offset_search_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `comparator_offset_search_ref.va` declares module `comparator_offset_search_ref` with positional ports: `vdd`, `vss`, `inp`, `inn`, `outp`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=100n maxstep=100p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `inp`
- `inn`
- `outp`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `inn`
- `inp`

## Public Behavior Checks

- `switching_point_at_offset`
- `output_low_below_offset`
- `output_high_above_offset`

## Output Contract

Return exactly these source artifacts:

- `comparator_offset_search_ref.va`
- `tb_comparator_offset_search_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain Verilog-A comparator with a built-in static offset.

Module name: `comparator_offset_search_ref`.

Requirements:

1. Ports: `vdd`, `vss`, `inp`, `inn`, `outp`
2. Built-in offset parameter `vos = 5m`
3. Output should switch high when `V(inp) - V(inn) > vos`
4. Use EVAS-compatible `cross()` events and `transition()`
5. The benchmark testbench will ramp `inp` and verify that the crossing occurs near `inn + vos`

Ports:
- `vdd`: electrical
- `vss`: electrical
- `inp`: electrical
- `inn`: electrical
- `outp`: electrical (power rail)
- `vss`: inout electrical (power rail)
- `inp`: input electrical
- `inn`: input electrical
- `outp`: output electrical
