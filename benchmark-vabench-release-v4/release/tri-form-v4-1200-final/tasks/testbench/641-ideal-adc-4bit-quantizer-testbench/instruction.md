# Ideal ADC 4bit Quantizer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Ideal ADC 4bit Quantizer` DUT. The evaluator runs the same submitted bytes
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

- `P_CLOCKED_DIFFERENTIAL_SAMPLE`: Each rising `vclk` crossing through `vtrans_clk` samples `V(vip)-V(vin)` and holds the resulting analog code on `digital` until the next sample.
- `P_SYMMETRIC_INPUT_RANGE`: The sampled differential input is quantized over the symmetric span from `-vref` to `+vref`; values outside that span saturate to the endpoint codes.
- `P_CODE_SCALE_AND_LSB`: `digital` represents the selected code using the declared `levels` spacing so adjacent quantization bins differ by one LSB.

The required trace names are: `time`, `digital`, `vclk`, `vin`, `vip`.

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
