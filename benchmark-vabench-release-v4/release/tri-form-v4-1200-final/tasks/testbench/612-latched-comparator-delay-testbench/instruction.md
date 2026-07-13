# Latched Comparator Delay Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Latched Comparator Delay` DUT. The evaluator runs the same submitted bytes
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

- `P_SUPPLY_REFERENCED_THRESHOLD`: The latch clock threshold is the midpoint of VDD and GND, and DOUT low and high levels use those same rails.
- `P_RISING_EDGE_LATCH`: Each rising CLK midpoint crossing latches one comparison result; falling crossings do not resample the input.
- `P_OFFSET_DECISION`: With vn zero, DOUT latches high exactly when VINP minus VINN exceeds vos and low otherwise.
- `P_SEEDED_RANDOM_TERM`: With vn nonzero, each latch decision includes a normal input-referred term scaled by vn from the sequence initialized by seed_init.
- `P_INTEREDGE_HOLD`: The latched decision holds between rising CLK events even if VINP or VINN changes.
- `P_DELAY_AND_SMOOTHING`: DOUT applies td delay and tr transition smoothing after each latch event.

The required trace names are: `time`, `vdd`, `clk`, `vinn`, `vinp`, `dout`.

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
