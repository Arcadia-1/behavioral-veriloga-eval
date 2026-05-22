# Task: vbr1_l1_capacitive_weighted_sar_feedback_dac:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converters
- Base function: Capacitive/weighted SAR feedback DAC
- Domain: `voltage`
- Target artifact(s): `cdac_cal.va`
- Supplied/reference support artifact(s): `tb_cdac_cal_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `cdac_cal.va` declares module `cdac_cal` with positional ports: `VDD`, `VSS`, `CLK`, `D9`, `D8`, `D7`, `D6`, `D5`, `D4`, `D3`, `D2`, `D1`, `D0`, `CAL0`, `CAL1`, `VDAC_P`, `VDAC_N`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=68n maxstep=20p
```

The release harness expects these exact public scalar observables:

- `CLK`
- `CAL0`
- `CAL1`
- `VDAC_P`
- `VDAC_N`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `manual_review_expected_output`

## Output Contract

Return exactly one source artifact named `cdac_cal.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a 10-bit capacitive DAC for a SAR ADC.

Module name: `cdac_cal`. Binary-weighted main array plus 2 redundant calibration capacitors. Differential topology (top-plate/bottom-plate). Model charge redistribution.

Ports:
- `VDD`: electrical
- `VSS`: electrical
- `CLK`: electrical
- `D9`: electrical
- `D8`: electrical
- `D7`: electrical
- `D6`: electrical
- `D5`: electrical
- `D4`: electrical
- `D3`: electrical
- `D2`: electrical
- `D1`: electrical
- `D0`: electrical
- `CAL0`: electrical
- `CAL1`: electrical
- `VDAC_P`: electrical
- `VDAC_N`: electrical (power rail)
- `VSS`: inout electrical (power rail)
- `CLK`: input electrical
- `D9`: input electrical
- `D8`: input electrical
- `D7`: input electrical
- `D6`: input electrical
- `D5`: input electrical
- `D4`: input electrical
- `D3`: input electrical
- `D2`: input electrical
- `D1`: input electrical
- `D0`: input electrical
- `CAL0`: input electrical
- `CAL1`: input electrical
- `VDAC_P`: output electrical
- `VDAC_N`: output electrical

Implement this in Verilog-A behavioral modeling.
