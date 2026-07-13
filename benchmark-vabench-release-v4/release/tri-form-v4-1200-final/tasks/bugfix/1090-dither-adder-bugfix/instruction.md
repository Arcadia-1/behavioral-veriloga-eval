# Dither Adder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dither_adder.va`: `dither_adder`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_POSITIVE_DITHER`: When DPN is above vth, the output differential exceeds the input differential by DITHER_AMP.
- `P_NEGATIVE_DITHER`: When DPN is at or below vth, the output differential is lower than the input differential by DITHER_AMP.
- `P_SYMMETRIC_SPLIT`: Half of the selected differential dither is added to VOUT_P and half is subtracted from VOUT_N.
- `P_COMMON_MODE_PRESERVATION`: The output pair preserves the input common mode and does not introduce a vdd/2 offset.
- `P_PARAMETER_OVERRIDE`: Legal DITHER_AMP and vth overrides change only dither magnitude and polarity decision as declared.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dither_adder.va`.
Every supplied `.va` file is editable; do not add or omit files.
