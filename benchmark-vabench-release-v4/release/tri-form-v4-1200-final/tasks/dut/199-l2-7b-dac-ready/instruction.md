# L2 7b DAC Ready

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `l2_7b_dac_ready.va`: `l2_7b_dac_ready`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FIRST_READY_EDGE_ARMS_ONLY`: The first rising `rdy` edge arms the DAC and leaves the initialized output at zero.
- `P_READY_SAMPLES_SEVEN_BITS`: Each later rising `rdy` edge samples `din1..din7` against `vth` with the declared switched-capacitor weights.
- `P_BIPOLAR_WEIGHTED_DAC_OUTPUT`: Map the sampled 7-bit weight to the declared bipolar single-ended output with the correct denominator and offset.
- `P_DAC_OUTPUT_LEVEL_AND_HOLD`: Hold `aout` between ready edges and drive the declared voltage scale without half-level errors.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `l2_7b_dac_ready.va`.
Do not add or omit artifacts.
