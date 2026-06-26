# Source Clocked DAC Restore 7b

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter
- Base function: source-derived `clocked_dac_restore_7b`
- Domain: `voltage`
- Target artifact(s): `clocked_dac_restore_7b.va`
- Source provenance: `wangxy/DAC_restore_7bit.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`clocked_dac_restore_7b.va` declares module `clocked_dac_restore_7b` with positional ports:

```text
D1, D2, D3, D4, D5, D6, D0, CLK, VOUT
```

## Public Testbench And Observable Contract

The public and hidden smoke testbench uses the transient statement shown in `test_hidden/tests/tb_source_ref.scs`.
The evaluator samples stable windows after event edges and checks source-derived behavior. It does not require pointwise equality at simulator timesteps.

## Public Behavior Checks

- codes_0_42_85_127_sampled_after_clock_edges
- restored_midrise_levels_match_7b_formula

## Output Contract

Return exactly one source artifact named `clocked_dac_restore_7b.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Implement the source-derived voltage-domain behavior represented by `clocked_dac_restore_7b`. This benchmark case is included because it captures a reusable primitive from the deduplicated historical Verilog-A corpus while remaining small enough for deterministic EVAS/Spectre parity evaluation.
