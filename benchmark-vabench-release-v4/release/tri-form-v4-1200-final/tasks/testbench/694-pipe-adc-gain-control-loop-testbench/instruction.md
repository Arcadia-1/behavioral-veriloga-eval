# Pipe ADC Gain Control Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Pipe ADC Gain Control Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_GAIN_CONTROL_INITIAL_STATE`: Initialize the gain-control code to `gaincodeinit` and initialize the test-DAC controls to the declared minus phase.
- `P_ALTERNATING_TEST_DAC_PHASES`: On rising `clks`, alternate minus and plus test-DAC phases using the sampled 7-bit input code.
- `P_TARGET_DIFFERENCE_GAIN_UPDATE`: Update the gain-control code from the plus/minus code difference using the declared target difference and correction polarity.
- `P_GAIN_OUTPUT_LEVELS`: Gain-control and test-DAC outputs use valid voltage-coded low/high levels.

The required trace names are: `time`, `clks`, `ddiff`, `din20`, `din21`, `din22`, `din23`, `din24`, `din25`, `din26`, `dom`, `dop`, `dout10`, `dout11`, `dout12`, `dout13`, `gainctrl0`, `gainctrl1`, `gainctrl2`, `gainctrl3`, `gainctrl4`, `gainctrl5`, `gainctrl6`, `gctrlcode`.

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
