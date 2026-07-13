# Log RSSI Power Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `log_rssi_power_detector.va`: `log_rssi_power_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_BASELINE`: Initialization or active reset drives out to 0.12 V and metric to 0 V.
- `P_CLOCKED_MAGNITUDE_SAMPLE`: Each rising clk crossing while reset is inactive samples the magnitude abs(vin - 0.45 V); the held outputs do not track vin between samples.
- `P_RSSI_BINS`: Sampled magnitudes below 0.035 V, from 0.035 V to below 0.11 V, from 0.11 V to below 0.22 V, and at least 0.22 V map to out levels 0.12 V, 0.30 V, 0.54 V, and 0.72 V respectively.
- `P_AMPLITUDE_METRIC`: Metric equals three times the sampled magnitude, clamped to the 0 V to 0.9 V range.
- `P_OUTPUT_BOUNDS`: Out remains within the public 0.08 V to 0.82 V clamp range with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `log_rssi_power_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
