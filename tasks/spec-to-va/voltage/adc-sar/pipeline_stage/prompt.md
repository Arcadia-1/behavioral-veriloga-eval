Write a Verilog-A module named `pipeline_stage`.

Create a pure voltage-domain 1.5-bit pipeline ADC MDAC stage. The stage samples
`VIN` on `PHI1`, makes a sub-ADC decision on `PHI2`, drives a 2-bit decision
code, and outputs the gain-of-2 residue for the next pipeline stage.

Ports, all `electrical`, exactly in this order:

- `VDD`: supply
- `VSS`: reference
- `PHI1`: sample clock
- `PHI2`: residue/decision clock
- `VIN`: analog input
- `VREF`: full-scale reference
- `VRES`: residue output
- `D1`: upper-region decision bit
- `D0`: middle-region decision bit

Public behavior:

- Use `Vcm = V(VDD)/2`.
- On each rising edge of `PHI1`, sample `VIN`.
- On each rising edge of `PHI2`, compare the sampled input relative to `Vcm`
  against `+VREF/4` and `-VREF/4`.
- If `VIN - Vcm > VREF/4`, drive `D1=1`, `D0=0`, and
  `VRES = Vcm + 2*(VIN - Vcm) - VREF/2`.
- If `VIN - Vcm < -VREF/4`, drive `D1=0`, `D0=0`, and
  `VRES = Vcm + 2*(VIN - Vcm) + VREF/2`.
- Otherwise drive `D1=0`, `D0=1`, and `VRES = Vcm + 2*(VIN - Vcm)`.
- Clamp `VRES` to the supply range and drive all outputs with `transition(...)`.
- Keep the implementation voltage-domain only; do not use current contributions,
  `ddt`, `idt`, transistor devices, AC/noise analysis, or KCL/KVL solver assumptions.

## Public Evaluation Contract

Final EVAS transient setting:

```spectre
tran tran stop=300n maxstep=500p
```

Required public waveform columns in `tran.csv`:

- `phi1`
- `phi2`
- `vin`
- `vres`
- `d1`
- `d0`

The checker exercises upper, middle, and lower MDAC regions and verifies the
sub-ADC decisions plus gain-of-2 residue formula.
