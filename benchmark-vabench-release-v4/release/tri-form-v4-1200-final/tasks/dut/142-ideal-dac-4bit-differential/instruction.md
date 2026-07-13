# Ideal DAC 4bit Differential

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ideal_dac_4bit_differential.va`: `ideal_dac_4bit_differential`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FALLING_EDGE_CODE_SAMPLE`: Each falling `clk` crossing through `vtrans_clk` samples `digital`, clamps it to the valid code range, and holds the converted output until the next sample.
- `P_MIDRISE_DIFFERENTIAL_SCALE`: The sampled code maps to a mid-rise differential DAC level with the declared `levels` and `vref` scale.
- `P_OUTPUT_POLARITY_AND_COMMON_MODE`: `vop` and `von` are complementary about `vcm`, with positive differential polarity for larger sampled codes.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ideal_dac_4bit_differential.va`.
Do not add or omit artifacts.
