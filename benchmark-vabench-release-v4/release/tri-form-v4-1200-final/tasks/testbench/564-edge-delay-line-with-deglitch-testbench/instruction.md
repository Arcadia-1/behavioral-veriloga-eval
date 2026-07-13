# Edge Delay Line with Deglitch Window Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Edge Delay Line with Deglitch Window` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: When rst is above vth or enable is at or below vth, pending edge state is cancelled and vout, edge_valid, and rejected settle to vss no later than the next scheduling tick.
- `P_STABLE_EDGE_QUALIFICATION`: A rising or falling vin crossing through vth can qualify only when vin remains in the crossed-to logic state for min_width_ticks scheduling ticks while reset is inactive and the DUT is enabled.
- `P_DELAYED_EDGE_EMISSION`: After an input edge qualifies, vout changes to the corresponding vdd or vss target only after the additional delay_ticks scheduling interval and does not change early.
- `P_NARROW_GLITCH_REJECTION`: If vin reverses before a pending edge completes qualification, that edge does not update vout and rejected produces a bounded high pulse.
- `P_VALID_EMISSION_PULSE`: Each qualified delayed update of vout produces one bounded high pulse on edge_valid, while rejected remains reserved for cancelled narrow edges.
- `P_BIDIRECTIONAL_LEVELS`: Qualified rising and falling input edges can respectively drive vout toward vdd and vss, and all public outputs use tr-smoothed voltage transitions.
- `P_PARAMETER_OVERRIDE`: Overriding tick, min_width_ticks, or delay_ticks changes the observable qualification or emission timing without changing module ports, output polarity, or reset/enable behavior.

The required trace names are: `time`, `vin`, `rst`, `enable`, `vout`, `edge_valid`, `rejected`.

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
