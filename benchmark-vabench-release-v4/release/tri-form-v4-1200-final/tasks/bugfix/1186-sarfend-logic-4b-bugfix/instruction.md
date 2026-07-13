# SARFEND Logic 4b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sarfend_logic_4b.va`: `sarfend_logic_4b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CONVERSION_RESET_AND_PREVIOUS_WORD`: Each rising `clks` crossing publishes the previous DAC-P word on `dout0..dout3`, resets the conversion pointer, and initializes controls for a new conversion.
- `P_SAMPLE_AND_COMPARATOR_DECISIONS`: The conversion captures comparator inputs and updates SAR decisions with the declared `dcomp/dcompb` polarity.
- `P_TEST_OVERRIDE_BEHAVIOR`: The public test override controls the DAC/control outputs when asserted and does not corrupt normal conversion state.
- `P_DOUT_BIT_MAPPING`: `dout0..dout3` preserve the declared bit order of the previous DAC-P state.
- `P_LOGIC_OUTPUT_LEVELS`: Handshake, DAC-control, and data outputs use full voltage-coded low/high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sarfend_logic_4b.va`.
Every supplied `.va` file is editable; do not add or omit files.
