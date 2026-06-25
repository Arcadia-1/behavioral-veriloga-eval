# Source Clocked DAC Restore 4b

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter
- Base function: source-derived `clocked_dac_restore_4b`
- Domain: `voltage`
- Target artifact(s): `clocked_dac_restore_4b.va`
- Source provenance: `wangxy/DAC_restore_4bit.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`clocked_dac_restore_4b.va` declares module `clocked_dac_restore_4b` with positional ports:

```text
D3, D2, D1, D0, CLK, VOUT
```

## Public Testbench And Observable Contract

Public transient setting used by the evaluator:

```spectre
tran tran stop=50n maxstep=50p
```

The evaluator samples stable windows after event edges and checks the intended source-derived behavior. It does not require pointwise equality at simulator timesteps.

## Public Behavior Checks

- codes_0_5_10_15_sampled_after_clock_edges
- restored_midrise_levels_match_lsb_formula

## Output Contract

Return exactly one source artifact named `clocked_dac_restore_4b.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Implement the source-derived voltage-domain behavior represented by `clocked_dac_restore_4b`. This benchmark case is included because it captures a reusable mixed-signal behavioral primitive from the deduplicated historical Verilog-A corpus while remaining small enough for deterministic EVAS/Spectre parity evaluation.
