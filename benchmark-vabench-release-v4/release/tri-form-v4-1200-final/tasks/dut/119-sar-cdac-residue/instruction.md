# SAR CDAC Residue

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sar_cdac_residue.va`: `sar_cdac_residue`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INPUT_SAMPLE`: At initial_step and each rising CLK crossing through vdd/2, the residue state samples VIN.
- `P_S6_HALF_ADD`: Each falling S6 crossing through vdd/2 adds one half of the public reference span to the current residue.
- `P_BINARY_SUBTRACTIONS`: Rising crossings of S5, S4, S3, S2, and S1 through vdd/2 subtract one fourth, one eighth, one sixteenth, one thirty-second, and one sixty-fourth of the public reference span respectively.
- `P_EDGE_POLARITY`: S6 updates only on falling vdd/2 threshold crossings, while S5 through S1 update only on rising vdd/2 threshold crossings.
- `P_ACCUMULATED_STATE`: Between declared sampling and switch events, VRES represents and holds the accumulated residue state.
- `P_OUTPUT_TRANSITION`: VRES changes from the residue state using the declared tr transition time.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sar_cdac_residue.va`.
Do not add or omit artifacts.
