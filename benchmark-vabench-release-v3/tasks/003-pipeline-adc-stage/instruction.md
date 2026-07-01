# Pipeline ADC Stage

Implement a clocked 1.5-bit pipeline ADC MDAC stage.

## Public Interface

Declare module `pipeline_stage` with positional ports `VDD, VSS, PHI1, PHI2,
VIN, VREF, VRES, D1, D0`. All ports are electrical. `VRES` is the residue
output and `D1,D0` are the sub-ADC decision outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: clock decision threshold for `PHI1` and `PHI2`.
- `vdd = 0.9 V`: nominal output high level used for initialization.
- `tedge = 200 ps`: output transition smoothing time.

## Functional Contract

On each rising `PHI1` edge, sample `VIN`. On each rising `PHI2` edge, compare
the sampled input around `V(VDD)/2` against the 1.5-bit thresholds
`+V(VREF)/4` and `-V(VREF)/4`.

- Upper region: drive `D1` high, `D0` low, and subtract a half-reference from
  the gain-two residue.
- Middle region: drive `D1` low, `D0` high, and use the gain-two residue
  without reference subtraction or addition.
- Lower region: drive both decision outputs low and add a half-reference to the
  gain-two residue.

Clamp `VRES` to the supply range and drive all outputs with smooth
voltage-domain transitions.

## Modeling Constraints

Return only `pipeline_stage.va`. Use deterministic voltage-domain Verilog-A.
Do not modify or emit the support testbench, add checker logic, hard-code
private waveform sample points, add simulator-private side channels, use
current contributions, `ddt()`, or `idt()`.
