# Hysteretic Comparator Receiver Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Hysteretic Comparator Receiver` DUT. The evaluator runs the same submitted bytes
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

- `P_DEFINE_UPPER_TH_OFFSET_VHYS_2`: Define `upper_th = offset + vhys/2` and `lower_th = offset - vhys/2`. On initialization, set the output state high if `V(inp,inm)` is at or above the upper threshold; otherwise set it low. After initialization, switch high only on a rising crossing of `upper_th`, switch low only on a falling crossing of `lower_th`, and hold the previous state inside the hysteresis band. Drive `out` to the selected rail with delay `td` and transition time `tr`.
- `P_VOUT_HIGH_0_9_V_HIGH`: `vout_high = 0.9 V`: high output rail.
- `P_VOUT_LOW_0_0_V_LOW`: `vout_low = 0.0 V`: low output rail.
- `P_OFFSET_0_0_V_INPUT_REFERRED`: `offset = 0.0 V`: input-referred switching offset.
- `P_VHYS_40_MV_FROM_0_INF`: `vhys = 40 mV from [0:inf)`: total hysteresis width.
- `P_TD_400_PS_FROM_0_INF`: `td = 400 ps from [0:inf)`: propagation delay from a qualifying threshold crossing to the output state change.

The required trace names are: `time`, `inm`, `inp`, `out`.

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
