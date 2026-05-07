Generate only the Spectre testbench for the `prbs7_lfsr` circuit function.
Do not generate Verilog-A modules.  The evaluator provides the DUT Verilog-A file(s).

Required DUT include(s): `prbs7_ref.va`.
Required module(s): `prbs7`, `prbs7_ref`.

The testbench must instantiate the provided DUT, drive the public inputs through the validation behavior, run exactly one transient analysis, and save the public observables.

## Source Functional Specification

Write a Verilog-A module named `prbs7_ref`.

Create a 7-bit pseudo-random bit sequence (PRBS-7) generator in Verilog-A. Clock-driven, with a serial output and a parallel 7-bit state bus output. Use LFSR with XOR feedback taps at positions 7 and 6.

Expected behavior:
- 7-bit LFSR generating pseudo-random sequence
- Max-length polynomial: x^7 + x^6 + 1 (or equivalent)
- Sequence length = 2^7 - 1 = 127 states before repeating
Ports:
- `clk`: input electrical
- `rst_n`: input electrical
- `en`: input electrical
- `serial_out`: output electrical
- `state_0`: output electrical
- `state_1`: output electrical
- `state_2`: output electrical
- `state_3`: output electrical
- `state_4`: output electrical
- `state_5`: output electrical
- `state_6`: output electrical

Write EVAS-compatible Verilog-A (pure voltage-domain behavioral model, no current contributions).


## Public Evaluation Contract (Non-Gold)

This section states evaluator-facing constraints that must be visible to the generated artifact.
It does not prescribe the internal implementation or reveal a gold solution.

Final EVAS transient setting:

```spectre
tran tran stop=120n maxstep=50p
```

Required public waveform columns in `tran.csv`:

- `clk`, `rst_n`, `en`, `serial_out`

Use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

The evaluator may use a fixed reference testbench with the timing and observable names above.
Generate the requested DUT/fix so it behaves correctly under that public validation window.


## Public Evaluation Contract (Non-Gold)

Final EVAS transient setting:

```spectre
tran tran stop=120n maxstep=50p
```

Required public save statement:

```spectre
save clk rst_n en serial_out state_0 state_1 state_2 state_3 state_4 state_5 state_6
```

Use plain scalar save names for public observables; do not rely on instance-qualified or aliased save names.
Return exactly one fenced `spectre` code block and no prose outside the code block.
