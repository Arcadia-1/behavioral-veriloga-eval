# Sine VCO With Idtmod And Bound Step Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Sine VCO With Idtmod And Bound Step` DUT. The evaluator runs the same submitted bytes
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

- `P_FREQ_Q_CENTER_FREQ_VCO_GAIN`: `freq_q = center_freq + vco_gain * V(vin)`
- `P_PHASE_Q_IDTMOD_FREQ_Q_0`: `phase_q = idtmod(freq_q, 0.0, 1.0)` (modulo-1 phase accumulator)
- `P_OUT_VCO_AMP_SIN_M_TWO`: `out = vco_amp * sin(M_TWO_PI * phase_q)` (bipolar sine centered at `0 V`)
- `P_METRIC_VCO_AMP_PHASE_Q_VOLTAGE`: `metric = vco_amp * phase_q` (voltage-coded instantaneous wrapped phase, `0 V` to `vco_amp`)
- `P_CALL_BOUND_STEP_1_0_VCO`: call `$bound_step(1.0 / (vco_ppc * freq_q))` every step so the sine is resolved

The required trace names are: `time`, `vin`, `out`, `metric`.

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
