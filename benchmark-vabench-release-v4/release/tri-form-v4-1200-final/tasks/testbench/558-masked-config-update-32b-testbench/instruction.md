# Masked Config Update 32b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Masked Config Update 32b` DUT. The evaluator runs the same submitted bytes
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

- `P_MASKED_SELECTION`: For each bit N, out_cfg[N] equals new_cfg[N] when mask[N] is high and equals old_cfg[N] when mask[N] is low.
- `P_ZERO_MASK_IDENTITY`: With every mask bit low, the complete output word equals old_cfg.
- `P_FULL_MASK_REPLACEMENT`: With every mask bit high, the complete output word equals new_cfg.
- `P_BIT_INDEPENDENCE`: Changing mask or data bit N affects only out_cfg[N]; bus indices are neither reversed nor shifted.
- `P_OUTPUT_LEVELS`: Each output bit uses 0 V for logic low and vdd for logic high with finite transition smoothing.

The required trace names are: `time`, `old31`, `old30`, `old29`, `old28`, `old27`, `old26`, `old25`, `old24`, `old23`, `old22`, `old21`, `old20`, `old19`, `old18`, `old17`, `old16`, `old15`, `old14`, `old13`, `old12`, `old11`, `old10`, `old9`, `old8`, `old7`, `old6`, `old5`, `old4`, `old3`, `old2`, `old1`, `old0`, `new31`, `new30`, `new29`, `new28`, `new27`, `new26`, `new25`, `new24`, `new23`, `new22`, `new21`, `new20`, `new19`, `new18`, `new17`, `new16`, `new15`, `new14`, `new13`, `new12`, `new11`, `new10`, `new9`, `new8`, `new7`, `new6`, `new5`, `new4`, `new3`, `new2`, `new1`, `new0`, `mask31`, `mask30`, `mask29`, `mask28`, `mask27`, `mask26`, `mask25`, `mask24`, `mask23`, `mask22`, `mask21`, `mask20`, `mask19`, `mask18`, `mask17`, `mask16`, `mask15`, `mask14`, `mask13`, `mask12`, `mask11`, `mask10`, `mask9`, `mask8`, `mask7`, `mask6`, `mask5`, `mask4`, `mask3`, `mask2`, `mask1`, `mask0`, `out31`, `out30`, `out29`, `out28`, `out27`, `out26`, `out25`, `out24`, `out23`, `out22`, `out21`, `out20`, `out19`, `out18`, `out17`, `out16`, `out15`, `out14`, `out13`, `out12`, `out11`, `out10`, `out9`, `out8`, `out7`, `out6`, `out5`, `out4`, `out3`, `out2`, `out1`, `out0`.

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
