# DAC Serial Accumulator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dac_serial_accumulator.va`: `dac_serial_accumulator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SAMPLE_CLOCK_RESET`: Each falling `clk_sample` crossing resets the accumulator and serial bit counter.
- `P_SARREADY_SERIAL_ACCUMULATION`: Falling `clk_sarready` crossings during the active bit window add the sampled `data` bit to the accumulator.
- `P_BINARY_WEIGHT_ORDER`: The first accepted serial bit has the largest binary weight and later bits use descending weights.
- `P_BIPOLAR_OUTPUT_MAPPING`: The accumulated code is mapped to the required bipolar output range rather than an unipolar code.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dac_serial_accumulator.va`.
Do not add or omit artifacts.
