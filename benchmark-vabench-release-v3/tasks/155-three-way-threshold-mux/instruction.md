# Three Way Threshold Mux

## Task Contract

Implement a three-input analog multiplexer selected by a differential threshold
window.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal analog routing
- Target artifact: `three_way_threshold_mux.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`three_way_threshold_mux.va` must declare:

```verilog
module three_way_threshold_mux(sigin1, sigin2, sigin3, cntrlp, cntrlm, sigout);
input sigin1, sigin2, sigin3, cntrlp, cntrlm;
output sigout;
electrical sigin1, sigin2, sigin3, cntrlp, cntrlm, sigout;
```

## Public Parameter Contract

- `sigth_low = -1`: lower threshold for `V(cntrlp, cntrlm)`.
- `sigth_high = 1`: upper threshold for `V(cntrlp, cntrlm)`.

## Required Behavior

Let `ctrl = V(cntrlp, cntrlm)`.

- If `ctrl < sigth_low`, drive `sigout` with `V(sigin1)`.
- If `sigth_low <= ctrl <= sigth_high`, drive `sigout` with `V(sigin2)`.
- If `ctrl > sigth_high`, drive `sigout` with `V(sigin3)`.

## Modeling Constraints

Use deterministic voltage-domain selection. Do not latch the selection, average
inputs, ignore `cntrlm`, add smoothing, or hard-code testbench stimulus values.

## Output Contract

Return exactly one source artifact named `three_way_threshold_mux.va`.
