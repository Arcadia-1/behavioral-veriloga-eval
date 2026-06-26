Implement a voltage-domain two-input AND gate.

The module must be named `two_input_and_gate` and use this port order:

`out, in1, in2`

Interpret each input as logic high when it exceeds `vth`. Drive `out` to `vh`
only when both inputs are high; otherwise drive `vl`. Use `transition()` with
the configurable delay and transition time.
