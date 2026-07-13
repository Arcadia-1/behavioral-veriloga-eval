# Ideal Sample And Hold Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Ideal Sample And Hold` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_EDGE_CAPTURE`: On each rising vclk crossing through vtrans_clk, vout captures the instantaneous vin value.
- `P_INTEREDGE_HOLD`: The captured value holds until the next rising sampling event even when vin changes.
- `P_NO_FALLING_EDGE_CAPTURE`: Falling vclk crossings do not update the held value.
- `P_UNITY_SAMPLE_GAIN`: The held target equals the sampled vin without gain, offset, quantization, or rail remapping.
- `P_PARAMETERIZED_THRESHOLD`: Legal vtrans_clk overrides move the sampling crossing threshold while preserving rising-edge capture and hold behavior.

The required trace names are: `time`, `vclk`, `vin`, `vout`.

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
