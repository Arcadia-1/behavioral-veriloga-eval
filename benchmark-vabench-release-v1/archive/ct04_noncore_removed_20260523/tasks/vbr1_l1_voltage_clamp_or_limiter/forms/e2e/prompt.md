# Task: vbr1_l1_voltage_clamp_or_limiter:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Voltage clamp or limiter
- Domain: `voltage`
- Target artifact(s): `dut.va`, `tb_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `dut.va`, `tb_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `dut.va`
- `tb_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_voltage_clamp_e2e

Write both the Verilog-A DUT and Spectre testbench for a voltage clamp.

The DUT module is `voltage_clamp` with ports `raw_level, vdd, vss, clamped_level`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Clamp `raw_level` to the public range 0.18 V to 0.72 V.
- Drive `clamped_level` through `transition()` using voltage-domain contributions only.

Required testbench behavior:
- Drive `raw_level` below range, inside range, and above range.
- Save `raw_level`, supplies, and `clamped_level`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `dut.va` and `tb_ref.scs`.
