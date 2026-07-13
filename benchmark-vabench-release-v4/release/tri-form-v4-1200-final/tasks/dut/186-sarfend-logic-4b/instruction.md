# SARFEND Logic 4b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sarfend_logic_4b.va`: `sarfend_logic_4b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CONVERSION_RESET_AND_PREVIOUS_WORD`: Each rising `clks` crossing publishes the previous DAC-P word on `dout0..dout3`, resets the conversion pointer, and initializes controls for a new conversion.
- `P_SAMPLE_AND_COMPARATOR_DECISIONS`: The conversion captures comparator inputs and updates SAR decisions with the declared `dcomp/dcompb` polarity.
- `P_TEST_OVERRIDE_BEHAVIOR`: The public test override controls the DAC/control outputs when asserted and does not corrupt normal conversion state.
- `P_DOUT_BIT_MAPPING`: `dout0..dout3` preserve the declared bit order of the previous DAC-P state.
- `P_LOGIC_OUTPUT_LEVELS`: Handshake, DAC-control, and data outputs use full voltage-coded low/high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sarfend_logic_4b.va`.
Do not add or omit artifacts.
