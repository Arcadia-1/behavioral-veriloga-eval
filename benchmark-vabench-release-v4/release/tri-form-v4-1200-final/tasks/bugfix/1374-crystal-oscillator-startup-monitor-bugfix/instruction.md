# Crystal Oscillator Startup Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `crystal_oscillator_startup_monitor.va`: `crystal_oscillator_startup_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, clear oscillator amplitude, `osc_out`, `valid`, and `startup_done`.
- `P_INCREASE_A_BEHAVIORAL_AMPLITUDE_STATE_BY`: Increase a behavioral amplitude state by `amp_step` on each rising `clk_ref` edge while enabled until `amp_target` is reached.
- `P_CLAMP_THE_AMPLITUDE_AT_AMP_TARGET`: Clamp the amplitude at `amp_target` and expose it on `amp_metric`.
- `P_TOGGLE_OSC_OUT_FROM_CLK_REF`: Toggle `osc_out` from `clk_ref` only after the amplitude state is nonzero.
- `P_ASSERT_STARTUP_DONE_WHEN_AMP_METRIC`: Assert `startup_done` when `amp_metric` reaches `amp_target`.
- `P_ASSERT_VALID_AFTER_TWO_CONSECUTIVE_SLICED`: Assert `valid` after two consecutive sliced oscillator periods after startup is done.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `crystal_oscillator_startup_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.
