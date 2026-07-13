# Propagation Delay Comparator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Propagation Delay Comparator` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_CLOCKED_DECISION`: At each rising CLK crossing through half the VDD-to-VSS rail span, the comparator latches the sign of VINP minus VINN minus voffset into complementary DCMPP/DCMPN decisions, with LP mirroring DCMPP and LM mirroring DCMPN.
- `P_FALLING_RESET`: Each falling CLK crossing resets both comparator decision outputs low.
- `P_DELAY_MAGNITUDE_TREND`: For otherwise equal conditions, a smaller absolute effective differential input produces a longer clock-to-decision delay.
- `P_DELAY_CLAMP`: The scheduled comparator decision delay follows the public log-linear regeneration relation and remains within td_min through td_max.
- `P_EDGE_INTERVAL_MEASUREMENT`: After a rising CLK_1 crossing arms the timer, the next rising CLK_2 crossing updates OUT_PS to the elapsed interval expressed in picoseconds and holds that completed measurement.
- `P_BUNDLE_BINDING`: The timing helper observes the comparator clock as CLK_1 and the positive comparator decision as CLK_2, exposing their measured interval on delay_ps.

The required trace names are: `time`, `clk`, `vinp`, `vinn`, `out_p`, `out_n`, `lp_int`, `lm_int`, `delay_ps`, `gnd`, `vdd`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
