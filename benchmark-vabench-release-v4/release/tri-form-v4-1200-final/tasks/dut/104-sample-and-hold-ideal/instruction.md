# Ideal Sample And Hold

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `source_sample_hold.va`: `source_sample_hold`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_EDGE_CAPTURE`: On each rising vclk crossing through vtrans_clk, vout captures the instantaneous vin value.
- `P_INTEREDGE_HOLD`: The captured value holds until the next rising sampling event even when vin changes.
- `P_NO_FALLING_EDGE_CAPTURE`: Falling vclk crossings do not update the held value.
- `P_UNITY_SAMPLE_GAIN`: The held target equals the sampled vin without gain, offset, quantization, or rail remapping.
- `P_PARAMETERIZED_THRESHOLD`: Legal vtrans_clk overrides move the sampling crossing threshold while preserving rising-edge capture and hold behavior.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `source_sample_hold.va`.
Do not add or omit artifacts.
