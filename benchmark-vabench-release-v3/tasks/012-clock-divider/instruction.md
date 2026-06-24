# Clock Divider

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: PLL Clock and Timing Systems
- Base function: Clock divider
- Domain: `voltage`
- Target artifact(s): `clk_divider_ref.va`
- Supplied support artifact(s): public smoke testbench under `test_visible/`
- Visible context: public task, interface, artifact, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `clk_divider_ref.va` declares module `clk_divider_ref` with positional ports: `clk_in`, `rst_n`, `div_code_0`, `div_code_1`, `div_code_2`, `div_code_3`, `div_code_4`, `div_code_5`, `div_code_6`, `div_code_7`, `clk_out`, `lock`.

## Observable Contract

The evaluator expects these exact public scalar observables:

- `clk_in`
- `rst_n`
- `clk_out`
- `lock`
- `div_code_0`
- `div_code_1`
- `div_code_2`
- `div_code_3`
- `div_code_4`
- `div_code_5`
- `div_code_6`
- `div_code_7`

The hidden evaluator uses these node names when it measures behavior. Do not rename ports, invert their logic convention, or rely on instance-qualified aliases.

## Required Behavior

- Treat every input and output as an electrical voltage-domain signal.
- Interpret `rst_n` as active-low reset. While reset is low, drive `clk_out` low and `lock` low, clear internal divider state, and restart acquisition when reset returns high.
- Decode `div_code_0` through `div_code_7` as an unsigned 8-bit LSB-first ratio code sampled from voltage levels above/below `vth`; code 0 means divide ratio 1.
- For divide ratio 1, `clk_out` should reproduce the input clock waveform with voltage-domain transitions and `lock` should assert after the divider has observed the first valid clock cycle after reset.
- For divide ratios greater than 1, produce a periodic divided clock whose rising-to-rising output period spans exactly the decoded number of input rising edges after startup.
- For odd divide ratios, use floor/ceil segment lengths so both high and low phases are present and the long segment differs by at most one input cycle from the short segment.
- Assert `lock` only after the first complete output period for the currently decoded ratio. If the ratio code changes after reset, clear divider phase and `lock`, then reacquire using the new ratio.
- Drive `clk_out` and `lock` as 0 V / `vdd` voltage outputs using `transition(...)`.

## Output Contract

Return exactly one source artifact named `clk_divider_ref.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

This entry is scoped as a PLL/ADPLL feedback-divider timing primitive, not as a generic digital-logic benchmark. Model the divider through voltage-domain clock edges, reset behavior, decoded ratio, and lock timing used by PLL loops.

## PLL Feedback Divider DUT

Write a pure voltage-domain Verilog-A module for a resettable programmable clock divider.

The DUT module is `clk_divider_ref` with ports `clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7, clk_out, lock`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Decode an 8-bit voltage-domain ratio code into an integer divide ratio, with code 0 treated as ratio 1.
- Use active-low reset to clear the counter, output state, and lock state.
- For ratio greater than 1, divide the input clock with floor/ceil high and low segment lengths; assert `lock` after the first complete output period.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `clk_divider_ref.va`.
