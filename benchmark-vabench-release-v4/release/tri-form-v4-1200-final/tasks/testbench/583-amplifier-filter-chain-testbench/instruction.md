# Amplifier Filter Chain Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Amplifier Filter Chain` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_COMMON_MODE`: Initialization or active-high reset returns the preamp and both filter stages near 0.45 V and leaves settle_metric low.
- `P_BOUNDED_PREAMP`: At each rising clock edge, preamp_mon and metric equal gain times the sampled vin deviation about 0.45 V, clamped to 0 V through 0.9 V.
- `P_FIRST_FILTER_STAGE`: Filt1_mon applies the sampled first-order alpha update toward the bounded preamp target.
- `P_SECOND_FILTER_STAGE`: Filt2_mon applies a second sampled alpha update toward the newly updated first-stage value, and out follows filt2_mon.
- `P_CASCADE_LAG`: After a large input change, the second-stage output visibly lags the bounded preamp target while the two stage monitors preserve cascade order.
- `P_SETTLE_STATUS`: Settle_metric is 0.9 V when the output-target error is below 0.16 V and 0.1 V while the chain is recovering.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`, `preamp_mon`, `filt1_mon`, `filt2_mon`, `settle_metric`.

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
