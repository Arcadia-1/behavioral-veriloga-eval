# Tool 4bit SAR Signed DAC Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `tool_4bit_sar_signed_dac.va`: `tool_4bit_sar_signed_dac`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_EACH_RISING_CROSSING_OF_SH`: On each rising crossing of `sh` through `vth`, evaluate bits `d3..d0` with weights `8, 4, 2, 1`. A high bit contributes the positive weight and a low bit contributes the negative weight. Drive `aout` to the signed weighted sum multiplied by `gain` and hold it until the next sample trigger.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `tool_4bit_sar_signed_dac.va`.
Every supplied `.va` file is editable; do not add or omit files.
