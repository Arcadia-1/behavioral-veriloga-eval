Implement an edge time-difference detector.

The module must be named `time_diff_detector` and use this port order:

`clk, vinp, vinn, vout`

On each rising `clk` edge, output the previous cycle's `vinp` rising time minus
`vinn` rising time, scaled by `scale` and clipped to `[-vdd, vdd]`. After the
clock edge, arm detection for the first rising edge on each input in the new
cycle.
