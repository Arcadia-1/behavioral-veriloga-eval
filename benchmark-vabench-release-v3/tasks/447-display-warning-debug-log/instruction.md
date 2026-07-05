# Display Warning Debug Log

## Task Contract

Implement one behavioral Verilog-A source file named `display_warning_debug_log.va`. This is a language-extension/L0 support task for Spectre-compatible simulator output calls on a clocked voltage-domain update path, not a standalone core circuit macro.

## Form-Specific Requirements

Use `$display`, `$warning`, and `$debug` on the non-reset sampled update path. Include an unreachable `$error` branch so the source exercises `$error` syntax without terminating normal simulation. The simulator-output side effects are part of the language-semantics contract but must not change the voltage-domain output behavior.

## Public Verilog-A Interface

```verilog
module display_warning_debug_log (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use voltage-coded logic with `vth = 0.45` V and high outputs near `vhi = 0.9` V. Drive output transitions with rise/fall time `tr = 200p`. These values may be implemented as compatible Verilog-A parameters or internal constants.

## Required Behavior

- Initialize `out_v`, `metric_v`, and `count_q` at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- Otherwise set `out_v` to `vhi` when `V(vin) > vth`, else `0.0`.
- Set `metric_v` to the current `count_q` value before incrementing it.
- Call `$display`, `$warning`, and `$debug` with formatted count text on the non-reset path.
- Include an unreachable `$error` branch so the syntax is parsed without terminating normal simulation.
- Increment `count_q` after logging.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. Do not make console/log text part of the voltage-domain output contract.

## Output Contract

Return exactly one source artifact named `display_warning_debug_log.va`.
