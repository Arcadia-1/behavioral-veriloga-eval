# Task: vbr1_l1_sar_logic:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Data Converters
- Base function: SAR logic
- Domain: `voltage`
- Target artifact(s): `sar_logic_4b.va`, `tb_sar_logic_4b_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `sar_logic_4b.va`, `tb_sar_logic_4b_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `sar_logic_4b.va` declares module `sar_logic_4b` with positional ports: `VDD`, `VSS`, `CLKS`, `DCOMP`, `DP_DAC_3`, `DP_DAC_2`, `DP_DAC_1`, `DP_DAC_0`, `RDY`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=1n
```

The release harness expects these exact public scalar observables:

- `clks`
- `dcomp`
- `rdy`
- `dp_dac_3`
- `dp_dac_2`
- `dp_dac_1`
- `dp_dac_0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clks`
- `dcomp`

## Public Behavior Checks

- `rdy_low_high_low_sequence`
- `dac_code_1010_at_conversion_done_window`

## Output Contract

Return exactly these source artifacts:

- `sar_logic_4b.va`
- `tb_sar_logic_4b_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_sar_logic_4b_e2e

Write both the Verilog-A DUT and Spectre testbench for a 4-bit SAR logic sequencer.

The DUT module is `sar_logic_4b` with ports `VDD, VSS, CLKS, DCOMP, DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Implement a 4-bit successive-approximation state machine clocked by rising `CLKS` edges.
- Resolve the current trial bit from `DCOMP`, advance to the next lower bit, and assert `RDY` after bit 0 is resolved.
- Drive DAC decision pins and `RDY` as 0/0.9 V voltage-domain outputs with `transition()`.

Required testbench behavior:
- Clock the SAR through repeated conversion cycles with comparator decisions that produce code 1010 at the checked window.
- Save `CLKS`, `DCOMP`, all DAC decision pins, and `RDY`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `sar_logic_4b.va` and `tb_sar_logic_4b_ref.scs`.
