# AGC Receiver Leveling Loop

Implement a voltage-domain automatic-gain-control receiver leveling loop.

## Public Interface

Declare module `agc_receiver_leveling_loop` with positional ports `clk, rst,
vin, out, metric, gain_mon, rssi_mon`. All ports are electrical.

`clk` is the gain-control update clock, `rst` is an active-high voltage-coded
reset, `vin` is the receiver input envelope centered around common mode, `out`
is the leveled receiver output, `gain_mon` exposes the bounded gain-control
state, `rssi_mon` exposes the observed output envelope, and `metric` indicates
near-target settling.

## Public Parameter Contract

Provide these overrideable public parameters:

- `tr = 100p`: transition time used for smoothed voltage contributions.
- `vth = 0.45 V`: threshold for voltage-coded logic decisions.
- `target_amp = 0.18 V`: desired output-envelope amplitude around common mode.
- `deadband = 0.025 V`: tolerance band around the target amplitude before gain
  correction is needed.

## Functional Contract

On reset, initialize the receiver to a high-gain state, return `out` to the
0.45 V common-mode level, and clear the monitor outputs. After reset releases,
update the gain-control state on rising clock crossings. Small input envelopes
should be amplified. When the output envelope is too large, the gain-control
state should reduce gain; when it is too small, the loop should allow gain to
recover. The output should settle toward `target_amp` around common mode while
remaining bounded in the 0 V to 0.9 V signal range. `rssi_mon` should increase
with observed output envelope, `gain_mon` should decrease when the loop reduces
gain, and `metric` should rise when the settled output amplitude is within the
target band.

## Modeling Constraints

Return only `agc_receiver_leveling_loop.va`. Use voltage contributions only.
Use event-updated behavioral state on the clock edge and `transition(...)`
smoothing for output contributions. Do not modify or emit the support
testbench, add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, transistor-level
devices, S-parameters, AC/noise-analysis behavior, communication modem
algorithms, or full link-level decoding.
