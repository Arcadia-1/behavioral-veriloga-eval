# Thermometer Bus Encoder Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Thermometer Bus Encoder` DUT. The evaluator runs the same submitted bytes
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

- `P_PREFIX_CODE`: Active segment outputs always form a contiguous prefix beginning at t0; no higher segment may be high while a lower segment is low.
- `P_ORDERED_ACTIVATION`: As vin increases, segments activate in order t0 through t15 and the active-segment count never decreases.
- `P_UNIFORM_SEGMENTS`: The clipped 0-to-vref input span selects among sixteen equal-width thermometer segments.
- `P_INPUT_CLIPPING`: Inputs at or below 0 V produce no active segments, and inputs at or above vref produce all sixteen active segments.
- `P_OUTPUT_LEVELS`: Each inactive segment approaches 0 V and each active segment approaches vh with finite transition smoothing.

The required trace names are: `time`, `vin`, `t0`, `t1`, `t2`, `t3`, `t4`, `t5`, `t6`, `t7`, `t8`, `t9`, `t10`, `t11`, `t12`, `t13`, `t14`, `t15`.

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
