# Task: vbr1_l1_voltage_clamp_or_limiter:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Voltage clamp or limiter
- Domain: `voltage`
- Target artifact(s): `tb_ref.scs`
- Supplied/reference support artifact(s): `dut.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `dut.va` declares module `voltage_clamp` with positional ports: `raw_level`, `vdd`, `vss`, `clamped_level`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=120n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `raw_level`
- `clamped_level`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `raw_level`

## Public Behavior Checks

- `below_range_clamps_to_0p18`
- `inside_range_follows_raw_level`
- `above_range_clamps_to_0p72`

## Output Contract

Return exactly one source artifact named `tb_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_voltage_clamp_tb

Write a Spectre testbench for a voltage clamp DUT.

The DUT module is `voltage_clamp` with ports `raw_level, vdd, vss, clamped_level`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `dut.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Clamp `raw_level` to the public range 0.18 V to 0.72 V.
- Drive `clamped_level` through `transition()` using voltage-domain contributions only.

Stimulus and observability requirements:
- Drive `raw_level` below range, inside range, and above range.
- Save `raw_level`, supplies, and `clamped_level`.

Return exactly one Spectre testbench file named `tb_ref.scs`.
