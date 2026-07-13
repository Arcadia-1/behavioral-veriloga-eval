# Fractional-delay DTC Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `fractional_delay_dtc_macro.va`: `fractional_delay_dtc_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear output, phase metric, and `valid`.
- `P_DECODE_FRAC_3_FRAC_0_AS`: Decode `frac_3..frac_0` as a fractional delay setting.
- `P_FOR_EACH_INPUT_EDGE_EMIT_ONE`: For each input edge, emit one output edge with a delay proportional to the fractional code.
- `P_EXPOSE_THE_FRACTIONAL_DELAY_AS_PHASE`: Expose the fractional delay as `phase_metric`.
- `P_PRESERVE_INPUT_EDGE_ORDER_AND_ASSERT`: Preserve input-edge order and assert `valid` after the first emitted delayed edge.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `fractional_delay_dtc_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
