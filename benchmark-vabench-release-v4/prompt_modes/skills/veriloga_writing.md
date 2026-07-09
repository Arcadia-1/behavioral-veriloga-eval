Verilog-A writing checklist:

Use this generic checklist when writing the requested behavioral Verilog-A
artifact.

1. Preserve the exact target file names, module names, positional port order,
   public parameters, and default parameter values from the task contract.
2. Start each `.va` source with `include "constants.vams"` and
   `include "disciplines.vams"` unless the task explicitly says otherwise.
3. Declare all public analog ports as `electrical`; do not add ports, pins,
   state outputs, status flags, or extra files.
4. Declare parameters and local state at module scope before the `analog`
   block. Keep parameter names overrideable exactly as specified.
5. Use deterministic voltage-domain behavior for voltage-domain tasks. Drive
   public voltage outputs with voltage contributions, not current contributions.
6. For memory, sampled, or clocked behavior, initialize local state with
   `initial_step` when the public behavior has a defined initial value.
7. For edge-triggered behavior, update local state only inside the specified
   analog event control, such as a rising `cross(...)`, and preserve the state
   between events.
8. Place output contributions at analog-block scope so outputs are continuously
   driven on every analog evaluation; do not place the only output contribution
   inside an event block.
9. When the task exposes `VDD` and `VSS`, compute thresholds and output levels
   relative to those rails rather than assuming fixed absolute voltages.
10. Use `transition(...)` for smoothed voltage-coded outputs only when the task
    asks for transition smoothing or provides a transition-time parameter.
11. Keep analog operators such as `ddt()` or `idt()` out of the model unless the
    public task contract explicitly requires that kind of dynamic behavior.
12. Avoid fitting one guessed waveform or one guessed set of time points. The
    implementation should satisfy the public behavioral contract over valid
    inputs and parameter overrides.
13. Emit only the requested file blocks and no explanatory prose, alternative
    implementations, scratch files, or renamed artifacts.
