# SAR Logic 4b Self Timed Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `SAR Logic 4b Self Timed` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_INITIALIZES_SELF_TIMED_STATE`: Initialization and rising `rst` reset the conversion step, clear `cmpck/dout`, and initialize DAC bottom-plate controls.
- `P_COMPARATOR_PULSE_DECISION_POLARITY`: Rising `dcmpp` or `dcmpn` pulses store comparator decisions with the declared polarity.
- `P_STEP_ADVANCE_ON_COMPARATOR_FALL`: Comparator-output falling events advance the SAR step and update the next control state.
- `P_CMPCK_TIMING_AND_LEVEL`: `cmpck` is scheduled low after `t_logic_delay` and driven with valid voltage-coded levels.

The required trace names are: `time`, `clkc`, `cmpck`, `dbotn1`, `dbotn2`, `dbotn3`, `dbotp1`, `dbotp2`, `dbotp3`, `dcmpn`, `dcmpp`, `dout1`, `dout2`, `dout3`, `dout4`, `rst`, `vdd`, `gnd`.

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
