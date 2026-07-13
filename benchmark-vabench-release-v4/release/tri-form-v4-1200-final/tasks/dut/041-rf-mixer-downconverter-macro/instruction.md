# RF Mixer Downconverter Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `rf_mixer_downconverter_macro.va`: `rf_mixer_downconverter_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_COMMON_MODE`: Active reset drives out to 0.45 V common mode and metric low.
- `P_LO_POLARITY`: With reset inactive, clk above vth selects LO coefficient +1 and clk at or below vth selects coefficient -1.
- `P_DOWNCONVERSION_TRANSFER`: The baseband target is 0.45 V plus conv_gain times vin minus 0.45 V times the selected LO coefficient.
- `P_ACTIVE_METRIC`: Metric is 0.9 V while reset is inactive and conversion is active, and low during reset.
- `P_OUTPUT_CLAMP`: Out is clamped to 0.02 V through 0.88 V and changes with finite smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `rf_mixer_downconverter_macro.va`.
Do not add or omit artifacts.
