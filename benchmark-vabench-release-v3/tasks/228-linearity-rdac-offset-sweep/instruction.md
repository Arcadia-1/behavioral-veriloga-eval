# Linearity RDAC Offset Sweep

## Task Contract

- Form: `dut`
- Level: `L2`
- Category: Calibration, Trim, and DEM Control
- Base function: RDAC-code sweep with repeated comparator offset search
- Domain: `voltage`
- Target artifact(s): `linearity_rdac_offset_sweep.va`
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Return exactly one Verilog-A source file named `linearity_rdac_offset_sweep.va`.
- Preserve the public module name, positional port order, electrical disciplines, generated stimulus outputs, and RDAC bit order.
- Do not generate or modify a Spectre testbench.

## Public Verilog-A Interface

Declare module `linearity_rdac_offset_sweep` with positional ports:

```verilog
module linearity_rdac_offset_sweep(ck, d,
    vinp, vinn, vrefp, vrefn,
    dc0, dc1, dc2, dc3, dc4, dc5, dc6);
```

All ports are electrical. `ck` is the sweep/search clock, `d` is the comparator
decision input, `vinp/vinn` are the generated differential input stimulus,
`vrefp/vrefn` are the generated differential reference stimulus, and
`dc0..dc6` expose the voltage-coded RDAC sweep code.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vcm = 0.6 V`: output common-mode voltage.
- `vppd = 1.0 V`: differential reference sweep span.
- `vdd = 1.0 V`: logic-high level and comparator threshold scale.
- `nlvl = 17.0`: number of reference levels in the sweep.
- `iter_num = 4`: number of comparator-directed search updates per RDAC code.

## Required Behavior

For each RDAC code, run a short comparator-directed offset search around the
current reference level. Track the comparator sign, halve the search step when
the sign changes, and move the differential input residue in the indicated
direction. After `iter_num` search updates, decrement the 7-bit RDAC code and
restart the search from the current reference. When the RDAC code has swept to
zero, wrap it back to full scale and advance the reference by one LSB of the
public reference sweep.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on clock
crossings and smooth discrete or event-updated output voltages with
`transition(...)`. Do not add checker logic, hard-code private waveform sample
points, add simulator-private side channels, use current contributions,
transistor-level devices, `ddt()`, `idt()`, or AC/noise-analysis behavior.

## Output Contract

Return exactly one complete Verilog-A file named `linearity_rdac_offset_sweep.va`.
Do not include explanatory prose outside the source artifact contents.
