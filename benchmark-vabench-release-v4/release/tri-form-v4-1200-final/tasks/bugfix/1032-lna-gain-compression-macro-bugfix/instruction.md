# LNA Gain Compression Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `lna_gain_compression_macro.va`: `lna_gain_compression_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_AND_RESET_COMMON_MODE`: Initialization sets out to 0.45 V and clears metric; an active-high reset sampled on a rising clk crossing restores the same state.
- `P_SMALL_SIGNAL_GAIN`: For linear values from 0.14 V through 0.76 V, out equals 0.45 V plus gain times the sampled vin deviation and metric is 0.1 V.
- `P_POSITIVE_COMPRESSION`: Above linear 0.76 V, excess signal is compressed by factor 0.28 and metric is 0.8 V.
- `P_NEGATIVE_COMPRESSION`: Below linear 0.14 V, excess signal is compressed by factor 0.28 and metric is 0.8 V.
- `P_FINAL_OUTPUT_CLAMP`: The final held output remains within 0.04 V through 0.86 V.
- `P_CLOCKED_HOLD`: Out and metric update on rising clock crossings and hold between samples.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `lna_gain_compression_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
