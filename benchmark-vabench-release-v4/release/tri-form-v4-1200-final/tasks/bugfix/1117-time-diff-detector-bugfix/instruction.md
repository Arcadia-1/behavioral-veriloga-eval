# Time Diff Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `time_diff_detector.va`: `time_diff_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FIRST_EDGE_CAPTURE`: Within each clock window, only the first rising vinp crossing and first rising vinn crossing through vth_in define the stored timing measurement.
- `P_PREVIOUS_WINDOW_REPORT`: At each rising clk crossing through vth_clk, vout reports the edge-time difference captured in the preceding valid clock window; if either input edge was absent, vout holds its previous value.
- `P_SIGNED_DIFFERENCE`: The reported value preserves the sign of the vinp first-edge time minus the vinn first-edge time and applies the public scale factor.
- `P_OUTPUT_CLIP`: The scaled reported voltage is bounded to the closed interval from -vdd to +vdd.
- `P_WINDOW_REARM`: Each reporting clock edge rearms both input-edge detectors so the next window is measured independently.
- `P_OUTPUT_TRANSITION`: Reported output changes use the declared td delay and tr transition time.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `time_diff_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
