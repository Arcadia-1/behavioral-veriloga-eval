# Settling Time Measurement Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Settling Time Measurement` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.

## Public Verilog-A Interface

- Artifact `settling_time_measurement_tb.va`:
  - Module `settling_time_measurement_tb` (entry)
    - position 0: `step` (input, electrical)
    - position 1: `vout` (output, electrical)
    - position 2: `done` (output, electrical)

Stable public Spectre binding:

The submitted `testbench.scs` must use the supplied DUT through this public binding:

- Include path: `./dut/settling_time_measurement_tb.va`
- DUT instance: `XDUT (step vout done) settling_time_measurement_tb`
- Required saved public traces: `step`, `vout`, `done`
- Use one bounded transient analysis with a finite positive stop time.

You must design the stimulus yourself. Save traces as bare public signal names
(for example `clk`, not suffixed or hierarchical forms such as `clk:V` or
`XDUT.clk`). Do not redefine the DUT, drive DUT output nets, save
hierarchical/private nodes, or use checker/gold/internal files.

## Public Parameter Contract

- `settling_time_measurement_tb.tr` defaults to `3e-10` s; valid range: finite real; use tr >= 0 for physical transition smoothing; sets smoothing for vout and done.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_INITIAL_ZERO_STATE`: exercise and make observable: The settling-response state initializes to 0 V and vout begins from that state. Required traces: `time`, `vout`.
- `P_FIRST_ORDER_UPDATE`: exercise and make observable: At each 1 ns update, the response advances by 0.04 times the difference between step and its previous value. Required traces: `time`, `step`, `vout`.
- `P_RESPONSE_CONVERGENCE`: exercise and make observable: For a constant input step, vout approaches the step value monotonically without overshoot under the public recurrence. Required traces: `time`, `step`, `vout`.
- `P_DONE_TIME_GATE`: exercise and make observable: Done remains low through 120 ns regardless of the response level. Required traces: `time`, `vout`, `done`.
- `P_DONE_SETTLED_GATE`: exercise and make observable: After 120 ns, done is high only while the internal settled response is above 0.75 V and otherwise remains low. Required traces: `time`, `step`, `vout`, `done`.

The required trace names are: `time`, `step`, `vout`, `done`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the declared `./dut/...` source paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
