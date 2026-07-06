# Limiting Amplifier Frontend

## Task Contract

Implement the requested Verilog-A artifact for `Limiting Amplifier Frontend`.
- Form: `dut`
- Level: `L1`
- Category: `rf_afe_behavioral_macromodels`
- Target artifact(s): `limiting_amplifier_frontend.va`

Implement `limiting_amplifier_frontend.va` in Verilog-A.

Declare module `limiting_amplifier_frontend(clk, rst, vin, out, metric)` with
all ports electrical. `clk` and `rst` are voltage-coded logic signals with a
0.45 V threshold. `vin` is an AFE input voltage centered around 0.45 V, `out`
is the bounded limiting-amplifier output, and `metric` marks limiting activity.

Public parameters:

- `tr`: output transition time, default `100p`.
- `vth`: logic threshold, default `0.45`.

Behavior:

- Initialize `out` to the 0.45 V common-mode level and `metric` low.
- Update the held output state on rising `clk` crossings.
- When `rst` is high, return the output to common mode and clear `metric`.
- For small excursions of `vin` around common mode, apply voltage gain above
  unity while preserving polarity.
- For large positive or negative excursions, limit the output toward bounded
  high and low levels instead of continuing linearly.
- Drive `metric` high only while large-signal limiting is active.
- Keep `out` and `metric` in the 0 V to 0.9 V voltage range.

Modeling requirements:

- Use voltage contributions only; do not use current contributions,
  transistor-level devices, AC/noise analysis, or KCL/KVL assumptions.
- Use a clocked state update and drive output voltages through
  `transition(...)`.
- Return only `limiting_amplifier_frontend.va`; do not emit a Spectre
  testbench or validation harness.

## Public Verilog-A Interface

Declare module `limiting_amplifier_frontend` with positional ports `clk, rst, vin, out, metric`. All ports are electrical. `clk` and `rst` are voltage-coded control inputs, `vin` is the analog input around the common-mode level, `out` is the limited amplifier output, and `metric` reports limiting activity.

## Public Parameter Contract

Provide these overrideable public parameters:

- `tr = 100 ps`: output transition rise/fall smoothing time.
- `vth = 0.45 V`: logic threshold for `clk` and `rst`.

## Required Behavior

- Initialize `out` near midscale and `metric` low.
- On each rising `clk` crossing, sample `vin` unless reset is active.
- While `rst` is above `vth`, reset `out` to midscale and clear `metric`.
- Treat `V(vin) - 0.45 V` as the signed input.
- For small input magnitude, apply linear gain around midscale.
- For large positive or negative input magnitude, compress toward upper or lower limiting levels instead of growing unbounded.
- Clamp the output inside the 0 V to 0.9 V signal range.
- Drive `metric` high when the input is in a limiting region and low in the central linear region or reset.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `limiting_amplifier_frontend.va`. Do not include explanatory prose outside the source artifact contents.
