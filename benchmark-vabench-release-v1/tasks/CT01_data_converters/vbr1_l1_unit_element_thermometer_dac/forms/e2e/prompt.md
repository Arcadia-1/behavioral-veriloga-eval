# Task: vbr1_l1_unit_element_thermometer_dac:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Data Converters
- Base function: Unit-element thermometer DAC
- Domain: `voltage`
- Target artifact(s): `tb_thermometer_dac_15seg_ref.scs`, `thermometer_dac_15seg.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `tb_thermometer_dac_15seg_ref.scs`, `thermometer_dac_15seg.va`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `thermometer_dac_15seg.va` declares module `thermometer_dac_15seg` with positional ports: `seg0`, `seg1`, `seg2`, `seg3`, `seg4`, `seg5`, `seg6`, `seg7`, `seg8`, `seg9`, `seg10`, `seg11`, `seg12`, `seg13`, `seg14`, `vref`, `vss`, `aout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=180n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `seg0`
- `seg1`
- `seg2`
- `seg3`
- `seg4`
- `seg5`
- `seg6`
- `seg7`
- `seg8`
- `seg9`
- `seg10`
- `seg11`
- `seg12`
- `seg13`
- `seg14`
- `aout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vref`
- `vss`
- `seg0`
- `seg1`
- `seg2`
- `seg3`
- `seg4`
- `seg5`
- `seg6`
- `seg7`
- `seg8`
- `seg9`
- `seg10`
- `seg11`
- `seg12`
- `seg13`

## Public Behavior Checks

- `safe_time_output_levels_match_15_segment_thermometer_count`
- `full_scale_counts_all_15_segments`
- `output_is_monotonic_across_programmed_segment_counts`

## Output Contract

Return exactly these source artifacts:

- `tb_thermometer_dac_15seg_ref.scs`
- `thermometer_dac_15seg.va`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_thermometer_dac_15seg_e2e

Build a complete Verilog-A plus Spectre testbench pair for a pure
voltage-domain 4-bit-equivalent, 15-segment unit-element thermometer DAC.

Return exactly these two files:

- `thermometer_dac_15seg.va`
- `tb_thermometer_dac_15seg_ref.scs`

## DUT Module Contract

Implement this Verilog-A module declaration and port order:

```verilog
module thermometer_dac_15seg(
    seg0, seg1, seg2, seg3, seg4, seg5, seg6, seg7,
    seg8, seg9, seg10, seg11, seg12, seg13, seg14,
    vref, vss, aout
);
```

All ports are `electrical`. `seg0` through `seg14`, `vref`, and `vss` are
inputs; `aout` is the output. Segment pins use 0 V / 0.9 V logic levels.

The DUT must count every active unary segment pin and drive:

```text
aout = vss + (vref - vss) * active_segment_count / 15
```

Use `transition` on the voltage output. Do not use current contributions,
`ddt`, or `idt`.

## Testbench Contract

The Spectre testbench must include `thermometer_dac_15seg.va`, instantiate the
DUT with the exact port order, set `vref=0.9 V` and `vss=0 V`, and program
active segment counts 0, 1, 2, 7, 14, and 15. Save `seg0` through `seg14` and
`aout`.

The public checker samples away from input transitions and verifies the
15-segment endpoint-scaled levels, monotonicity, and the all-segments
full-scale point.
