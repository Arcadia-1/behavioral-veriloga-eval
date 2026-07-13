# Burst Clock Source Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Burst Clock Source` DUT. The evaluator runs the same submitted bytes
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

- `P_ACTIVE_LOW_RESET`: While RST_N is below vth, CLK_OUT is low and the burst frame counter is restarted.
- `P_FRAME_START`: After reset release, rising CLK crossings advance a repeating frame of div input-clock cycles beginning at position 0.
- `P_TWO_CYCLE_BURST`: At frame positions 0 and 1, CLK_OUT passes the voltage-coded CLK waveform, including its high and low phases.
- `P_QUIET_REMAINDER`: At frame positions 2 through div minus 1, CLK_OUT remains low regardless of CLK level.
- `P_FRAME_REPEAT`: The two-cycle burst followed by the quiet remainder repeats every div rising CLK crossings.
- `P_OUTPUT_LEVELS`: CLK_OUT uses 0 V and vdd as its voltage-coded low and high levels.

The required trace names are: `time`, `CLK`, `RST_N`, `CLK_OUT`.

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
