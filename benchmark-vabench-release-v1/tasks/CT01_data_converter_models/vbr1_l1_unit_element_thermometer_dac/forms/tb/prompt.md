# Task: vbr1_l1_unit_element_thermometer_dac:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Data Converter Models
- Base function: Unit-element thermometer DAC
- Domain: `voltage`
- Target artifact(s): `tb_thermometer_dac_15seg_ref.scs`
- Supplied/reference support artifact(s): `thermometer_dac_15seg.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Return exactly one source artifact named `tb_thermometer_dac_15seg_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_thermometer_dac_15seg_tb

Write a Spectre testbench for a pure voltage-domain Verilog-A DUT named
`thermometer_dac_15seg.va`.

Return exactly one complete Spectre netlist named
`tb_thermometer_dac_15seg_ref.scs`.

## DUT Contract

The candidate DUT is:

```verilog
module thermometer_dac_15seg(
    seg0, seg1, seg2, seg3, seg4, seg5, seg6, seg7,
    seg8, seg9, seg10, seg11, seg12, seg13, seg14,
    vref, vss, aout
);
```

All ports are electrical. Segment inputs are 0 V / 0.9 V logic signals. `vref`
is 0.9 V, `vss` is 0 V, and `aout` should equal
`vss + (vref - vss) * active_segment_count / 15`.

## Required Testbench Behavior

- Include the DUT file with `ahdl_include "thermometer_dac_15seg.va"`.
- Instantiate the DUT with the exact port order above.
- Drive programmed active segment counts 0, 1, 2, 7, 14, and 15.
- Keep samples away from segment transitions so the checker can inspect settled
  values.
- Save `seg0` through `seg14` and `aout`.
- Use a transient stop time of at least 180 ns and a `maxstep` no larger than
  500 ps.

The public checker compares the saved waveform to the expected 15-segment
endpoint-scaled DAC levels and verifies full-scale behavior.
