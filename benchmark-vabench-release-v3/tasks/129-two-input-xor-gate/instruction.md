Implement a voltage-domain two-input XOR gate.

The module must be named `two_input_xor_gate` and use this port order:

`out, in1, in2`

Interpret each input as logic high when it exceeds `vth`. Drive `out` to `vh`
when exactly one input is high; otherwise drive `vl`. Use `transition()` with
the configurable delay and transition time.
