# Time Diff Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `time_diff_detector.va`: `time_diff_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FIRST_EDGE_CAPTURE`: Within each clock window, only the first rising vinp crossing and first rising vinn crossing through vth_in define the stored timing measurement.
- `P_PREVIOUS_WINDOW_REPORT`: At each rising clk crossing through vth_clk, vout reports the edge-time difference captured in the preceding valid clock window; if either input edge was absent, vout holds its previous value.
- `P_SIGNED_DIFFERENCE`: The reported value preserves the sign of the vinp first-edge time minus the vinn first-edge time and applies the public scale factor.
- `P_OUTPUT_CLIP`: The scaled reported voltage is bounded to the closed interval from -vdd to +vdd.
- `P_WINDOW_REARM`: Each reporting clock edge rearms both input-edge detectors so the next window is measured independently.
- `P_OUTPUT_TRANSITION`: Reported output changes use the declared td delay and tr transition time.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `time_diff_detector.va`.
Do not add or omit artifacts.
