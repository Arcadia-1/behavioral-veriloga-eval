# RF Mixer Downconverter Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `rf_mixer_downconverter_macro.va`: `rf_mixer_downconverter_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_COMMON_MODE`: Active reset drives out to 0.45 V common mode and metric low.
- `P_LO_POLARITY`: With reset inactive, clk above vth selects LO coefficient +1 and clk at or below vth selects coefficient -1.
- `P_DOWNCONVERSION_TRANSFER`: The baseband target is 0.45 V plus conv_gain times vin minus 0.45 V times the selected LO coefficient.
- `P_ACTIVE_METRIC`: Metric is 0.9 V while reset is inactive and conversion is active, and low during reset.
- `P_OUTPUT_CLAMP`: Out is clamped to 0.02 V through 0.88 V and changes with finite smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `rf_mixer_downconverter_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
