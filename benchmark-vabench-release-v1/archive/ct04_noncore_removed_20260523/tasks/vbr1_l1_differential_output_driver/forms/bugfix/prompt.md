# Task: vbr1_l1_differential_output_driver:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Differential output driver
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_differential_voltage_output_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `differential_voltage_output_ref` with positional ports: `VDD`, `VSS`, `din`, `en`, `outp`, `outn`.
- `dut_fixed.va` declares module `differential_voltage_output_ref` with positional ports: `VDD`, `VSS`, `din`, `en`, `outp`, `outn`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=100n maxstep=100p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `din`
- `en`
- `outp`
- `outn`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `disabled_window_returns_to_common_mode`
- `enabled_output_polarity_tracks_din`
- `output_common_mode_stays_bounded`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Differential output driver Bugfix

Repair the supplied buggy Verilog-A implementation for `Differential output driver`.

The fixed implementation must preserve the public module name and ports used by
the reference Spectre testbench. Domain: pure voltage-domain behavioral
Verilog-A. Do not use current contributions, transistor-level devices,
AC/noise analysis, or KCL/KVL solving assumptions.
