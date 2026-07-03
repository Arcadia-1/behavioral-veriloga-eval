# Reset Enable Clock Divider

Implement a voltage-domain resettable, enable-qualified clock divider for an AMS timing/control path.

## Public Interface

Declare module `divide_by_eight_clock` with positional ports:

```verilog
module divide_by_eight_clock(vin, rst, en, vout);
```

All ports are scalar `electrical` voltage-domain ports.

## Functional Contract

- Treat `vin`, `rst`, and `en` as 0/0.9 V logic with a 0.45 V threshold.
- Provide an integer parameter `divisor` with default value 8. The intended public contract uses an even divisor of at least 2.
- `rst` is active high. When reset is active, reload the divider phase to the start of a high output half-cycle and drive `vout` high.
- When reset is inactive and `en` is high, advance the divider phase on rising threshold crossings of `vin`.
- When `en` is low, ignore `vin` edges and hold the current divider phase/output.
- Drive `vout` high for the first half of the divider phase count and low for the second half, yielding a 50% duty-cycle divided clock.
- Use smooth Verilog-A transitions for the voltage-coded output.

## Output

Return exactly one source artifact named `divide_by_eight_clock.va`. Do not generate a Spectre testbench.
