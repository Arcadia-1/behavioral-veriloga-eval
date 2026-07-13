# Vargain Diffamp Clip Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Vargain Diffamp Clip` DUT. The evaluator runs the same submitted bytes
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

- `P_COMPUTE_THE_DIFFERENTIAL_SIGNAL_AS_V`: Compute the observable input signal as `V(sigin_p, sigin_n)`.
- `P_COMPUTE_THE_DIFFERENTIAL_CONTROL_AS_V`: Compute the gain-control term as `V(sigctrl_p, sigctrl_n)` with the documented polarity.
- `P_SUBTRACT_SIGIN_OFFSET_FROM_THE_DIFFERENTIAL`: Subtract `sigin_offset` from the differential input before gain multiplication.
- `P_MULTIPLY_THE_OFFSET_CORRECTED_SIGNAL_BY`: Multiply the offset-corrected signal by the differential control and `gain_const`.
- `P_CLAMP_THE_RESULT_TO_THE_PUBLIC`: Clamp the amplified target to the public positive and negative output limits.
- `P_DRIVE_SIGOUT_WITH_THE_CLIPPED_TARGET`: Drive `sigout` with the clipped target transfer and correct output scale.

The required trace names are: `time`, `sigin_p`, `sigin_n`, `sigctrl_p`, `sigctrl_n`, `sigout`.

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
