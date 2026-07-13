# LC VCO Behavioral Source Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `LC VCO Behavioral Source` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CENTER`: Reset or disable centers both oscillator outputs at vcm and clears metrics and valid.
- `P_CONTROL_FREQUENCY_MAP`: Enabled edge periods follow the linear clamped vctrl mapping from fmin to fmax without retiming an already pending edge.
- `P_COMPLEMENTARY_AMPLITUDE`: Enabled oscillator outputs are complementary around vcm with the declared amplitude.
- `P_METRIC_REPORTING`: freq_metric reports clamped vctrl and amp_metric reports amplitude while enabled.
- `P_VALID_AFTER_TWO_CYCLES`: valid remains low until two complete oscillator cycles have elapsed after enable.

The required trace names are: `time`, `vctrl`, `enable`, `rst`, `osc_p`, `osc_n`, `freq_metric`, `amp_metric`, `valid`.

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
