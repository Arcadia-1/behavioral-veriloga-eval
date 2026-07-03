# Deterministic Jittered Clock Source

## Task Contract

Implement `deterministic_jittered_clock.va`, a repeatable voltage-domain clock source whose cycle-to-cycle timing can be deterministically modulated by an 8-bit seed.

## Form-Specific Requirements

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or checker.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module deterministic_jittered_clock(jitter_en, seed0, seed1, seed2, seed3, seed4, seed5, seed6, seed7, clk_out);
```

Inputs are `jitter_en` and seed bits `seed0` through `seed7`. Output is `clk_out`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Generate `clk_out` as a 0-to-`vdd` deterministic clock.
- With `jitter_en` low, use a constant 20 ns period, i.e. a 10 ns nominal half-period.
- With `jitter_en` high, interpret `seed7:seed0` as an unsigned seed and apply repeatable edge-to-edge half-period modulation.
- For edge index `k`, update the next half-period as `10 ns + (((seed + 3*k) % 5) - 2) * 0.8 ns`.
- Keep every resulting full clock period bounded and repeatable for the same seed.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, checker logic, private test hooks, or simulator-private side channels.
- Use timer-driven state for the output level, edge index, seed capture, and next-edge time.
- Do not use random distribution functions; the jitter is deterministic and seed-dependent.

## Output Contract

Return exactly one complete Verilog-A source file named `deterministic_jittered_clock.va`.
