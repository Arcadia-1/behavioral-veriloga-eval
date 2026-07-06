# IQ Downconversion Chain

## Task Contract

Implement the requested Verilog-A artifact for `IQ Downconversion Chain`.
- Form: `dut`
- Level: `L2`
- Category: `rf_afe_behavioral_macromodels`
- Target artifact(s): `iq_downconversion_chain.va`

Implement a voltage-domain I/Q downconversion receiver macromodel.

## Public Verilog-A Interface

Declare module `iq_downconversion_chain` with positional ports `clk, rst, vin,
out, metric, lo_i, lo_q, mix_i, mix_q, phase_mon`. All ports are electrical.

`clk` advances the quadrature LO phase, `rst` is an active-high voltage-coded
reset, `vin` is the RF input envelope centered around common mode, `out` is the
I-path baseband output, `metric` is the Q-path baseband output, `lo_i` and
`lo_q` expose voltage-coded I/Q LO polarity, `mix_i` and `mix_q` expose the
corresponding bounded mixer outputs, and `phase_mon` exposes the quadrature
phase state.

## Public Parameter Contract

Provide these overrideable public parameters:

- `tr = 80p`: transition time used for smoothed voltage contributions.
- `vth = 0.45 V`: threshold for voltage-coded logic decisions.

## Required Behavior

On reset, return the I/Q outputs and mixer monitors to the 0.45 V common-mode
level and initialize the quadrature phase monitor. After reset releases,
advance a four-state quadrature LO sequence on rising clock crossings. The I
and Q LO monitors should represent the expected quadrature polarity sequence.
The mixer monitors should apply the corresponding I or Q LO coefficient to the
input-envelope deviation from common mode and remain bounded in the 0 V to
0.9 V signal range. `out` should follow the I-path baseband behavior, `metric`
should follow the Q-path baseband behavior, and both baseband outputs should
settle back near common mode when the input returns to common mode.

## Modeling Constraints

Return only `iq_downconversion_chain.va`. Use voltage contributions only. Use
event-updated behavioral state on the clock edge and `transition(...)`
smoothing for output contributions. Do not modify or emit the support
testbench, add validation logic, hard-code specific waveform sample points, add
simulator-specific side channels, use current contributions, transistor-level
devices, S-parameters, AC/noise-analysis behavior, communication modem
algorithms, or full link-level decoding.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `iq_downconversion_chain.va`. Do not include explanatory prose outside the source artifact contents.
