# Divide By Two Toggle

Implement a voltage-domain divide-by-two edge toggle.

## Public Interface

Declare module `divide_by_two_toggle` with positional ports `clk, out`. Both
ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: rising-edge decision threshold for `clk`.
- `vdd = 0.9 V`: high output level.
- `tdel = 10 ps`: output transition delay.
- `tr = 10 ps`: output rise/fall transition time.

## Functional Contract

The internal divider state starts low. On every rising crossing of `clk`
through `vth`, toggle the state. Drive `out` low when the state is low and to
`vdd` when the state is high, using the public delay and transition-time
parameters. The first valid rising edge therefore drives `out` high.

## Modeling Constraints

Return only `divide_by_two_toggle.va`. Use voltage contributions only. Do not
modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.
