# DAC Serial Accumulator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dac_serial_accumulator.va`: `dac_serial_accumulator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SAMPLE_CLOCK_RESET`: Each falling `clk_sample` crossing resets the accumulator and serial bit counter.
- `P_SARREADY_SERIAL_ACCUMULATION`: Falling `clk_sarready` crossings during the active bit window add the sampled `data` bit to the accumulator.
- `P_BINARY_WEIGHT_ORDER`: The first accepted serial bit has the largest binary weight and later bits use descending weights.
- `P_BIPOLAR_OUTPUT_MAPPING`: The accumulated code is mapped to the required bipolar output range rather than an unipolar code.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dac_serial_accumulator.va`.
Every supplied `.va` file is editable; do not add or omit files.
