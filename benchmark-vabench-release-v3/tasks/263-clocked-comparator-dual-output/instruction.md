# Clocked Comparator Dual Output

Implement a clocked differential comparator with complementary voltage-coded
outputs and reset-low precharge behavior.

## Public Interface

Declare module `clocked_comparator_dual_output` with positional ports `clk,
vinn, vinp, outn, outp`. All ports are electrical. `clk` is the comparator
clock, `vinp` and `vinn` are the differential analog inputs, and `outp`/`outn`
are complementary decision outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 1.0 V`: logic high level and clock threshold reference.
- `td_cmp = 100p`: output decision delay.

## Functional Contract

- Initialize both decision outputs low.
- Whenever `clk` falls through `vdd/2`, reset both outputs low.
- Whenever `clk` rises through `vdd/2`, latch a differential decision: `outp`
  high for `vinp > vinn`, `outn` high for `vinp < vinn`, and both outputs
  remain low for an equal-input decision.
- Hold the latched or reset state until the next clock event.
- Drive outputs as smoothed voltage-domain levels from 0 V to `vdd`.

## Modeling Constraints

Return only `clocked_comparator_dual_output.va`. Use voltage contributions
only. Do not modify or emit the support testbench, add checker logic, hard-code
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`. Update local decision state in analog event
blocks and drive smoothed output contributions outside those event blocks.
