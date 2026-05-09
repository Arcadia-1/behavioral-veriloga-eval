# verilog_binary_literal_decimal

## Trigger

Use this skill when EVAS/Spectre-strict reports a Verilog-A parse error around a Verilog-style binary literal, for example `Expected RPAREN, got IDENT ('b1111111')`.

## Rule

Some Verilog-A frontends do not accept sized Verilog integer literals such as `7'b1111111` inside analog behavioral code.  The equivalent decimal integer literal is portable in this validator path.

## Repair Pattern

```verilog-a
lfsr_state = 7'b1111111;
mask = 16'b1111_1111_1111_1111;
```

becomes:

```verilog-a
lfsr_state = 127;
mask = 65535;
```

## Safety Boundary

Only convert binary literals containing `0`, `1`, and `_`.  Do not rewrite unknown/high-impedance literals, change expression structure, change state update logic, or infer missing behavior.  Accept only after strict-EVAS/Spectre compile validation.
