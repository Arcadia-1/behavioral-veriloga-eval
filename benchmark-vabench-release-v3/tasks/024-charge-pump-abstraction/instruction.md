# Charge Pump Abstraction

Implement `charge_pump_abstraction.va` in Verilog-A.

## Interface

```verilog
module charge_pump_abstraction(
    input  electrical clk,
    input  electrical rst,
    input  electrical up,
    input  electrical dn,
    output electrical vctrl,
    output electrical metric
);
```

## Required Behavior

This task asks for the `charge_pump_abstraction` behavioral DUT module, not a
Spectre testbench. The module represents UP/DN pulse effects as a sampled
voltage-domain control-node update without current-domain charge-pump
contributions.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `tr` | `100 ps` | time, `(0:inf)` | Rise/fall smoothing for `vctrl` and `metric`. |
| `vth` | `0.45` | V | Logic threshold for `clk`, `rst`, `up`, and `dn`. |
| `step` | `0.06` | V-equivalent update | Control-voltage increment/decrement per sampled UP/DN pulse. |
| `vmin` | `0.05` | V | Lower clamp for `vctrl`. |
| `vmax` | `0.85` | V | Upper clamp for `vctrl`. |

Required observable behavior:

- Treat `clk`, `rst`, `up`, and `dn` as voltage-coded logic inputs.
- On rising `clk` edges, sample the UP/DN request when reset is low.
- A sampled UP-only pulse increases `vctrl` by `step`.
- A sampled DN-only pulse decreases `vctrl` by `step`.
- Simultaneous UP/DN or absent pulses hold the current control voltage.
- Clamp `vctrl` between `vmin` and `vmax`.
- When `rst` is high, reset `vctrl` to midscale.
- Drive `metric` as a voltage-coded status observable: high for UP movement,
  low for DN movement, and midscale for hold/reset.

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, checker logic, private
test hooks, or simulator-private side channels.

## Output

Return exactly one source artifact named `charge_pump_abstraction.va`.
