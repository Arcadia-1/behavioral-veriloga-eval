# Task: vbr1_l1_clock_divider:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: PLL Clock and Timing Systems
- Base function: Clock divider
- Domain: `voltage`
- Target artifact(s): `tb_clk_divider_ref.scs`
- Supplied/reference support artifact(s): `clk_divider.va`, `clk_divider_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `clk_divider.va` declares module `clk_divider` with positional ports: `CLK_IN`, `RST_N`, `CLK_OUT`, `LOCK`.
- `clk_divider_ref.va` declares module `clk_divider_ref` with positional ports: `clk_in`, `rst_n`, `div_code_0`, `div_code_1`, `div_code_2`, `div_code_3`, `div_code_4`, `div_code_5`, `div_code_6`, `div_code_7`, `clk_out`, `lock`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=50p
```

The release harness expects these exact public scalar observables:

- `clk_in`
- `rst_n`
- `clk_out`
- `lock`
- `\`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `clk_in`
- `rst_n`
- `div_code_0`
- `div_code_1`
- `div_code_2`
- `div_code_3`
- `div_code_4`
- `div_code_5`
- `div_code_6`
- `div_code_7`

## Public Behavior Checks

- `ratio_code_decodes_to_5`
- `output_period_matches_five_input_edges`
- `lock_asserts_after_first_complete_output_period`

## Output Contract

Return exactly one source artifact named `tb_clk_divider_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

This entry is scoped as a PLL/ADPLL feedback-divider timing primitive, not as a generic digital-logic benchmark. Model the divider through voltage-domain clock edges, reset behavior, decoded ratio, and lock timing used by PLL loops.

## PLL Feedback Divider Testbench Companion

Write a Spectre testbench for a resettable programmable clock divider DUT.

The DUT module is `clk_divider_ref` with ports `clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7, clk_out, lock`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `clk_divider_ref.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Decode an 8-bit voltage-domain ratio code into an integer divide ratio, with code 0 treated as ratio 1.
- Use active-low reset to clear the counter, output state, and lock state.
- For ratio greater than 1, divide the input clock with floor/ceil high and low segment lengths; assert `lock` after the first complete output period.

Stimulus and observability requirements:
- Drive `div_code` to ratio 5, release reset near 2 ns, and clock with a 1 ns input period.
- Run to 80 ns with a small maxstep and save input clock, output clock, lock, reset, and all ratio bits.

Review caveat: The staged evidence also preserves an auxiliary legacy `clk_divider.va`; the public task contract targets `clk_divider_ref`.

Return exactly one Spectre testbench file named `tb_clk_divider_ref.scs`.
