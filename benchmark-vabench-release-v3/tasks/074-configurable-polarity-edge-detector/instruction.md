# Configurable Polarity Edge Detector

## Task Contract

Implement `configurable_polarity_edge_detector.va`, a voltage-domain edge detector that can generate a pulse on either selected rising or selected falling input edges.

## Form-Specific Requirements

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or checker.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module configurable_polarity_edge_detector(sig, rise_en, pulse);
```

Inputs are `sig` and `rise_en`. Output is `pulse`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Treat `sig` and `rise_en` as voltage-coded logic using `vth`.
- When `rise_en` is high, generate a short pulse after each rising edge of `sig` and do not pulse on falling edges.
- When `rise_en` is low, generate a short pulse after each falling edge of `sig` and do not pulse on rising edges.
- The output pulse width should be a short support-timing pulse, nominally about 2 ns, with smooth edges.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, checker logic, private test hooks, or simulator-private side channels.
- Use edge events and a clear timer or equivalent state so the pulse is bounded in time.

## Output Contract

Return exactly one complete Verilog-A source file named `configurable_polarity_edge_detector.va`.
