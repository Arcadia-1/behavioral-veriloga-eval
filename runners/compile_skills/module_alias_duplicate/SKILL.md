# module_alias_duplicate

## Trigger

Use this skill when strict preflight reports `spectre_strict:undefined_module=<needed>;available_modules=<actual>` and the public Spectre harness still instantiates both `<needed>` and `<actual>`.

## Rule

A pure rename is unsafe if the testbench still needs the original module name.  In that case, preserve the generated module and materialize a duplicate public alias module under the missing harness name.

## Repair Pattern

If the generated Verilog-A file contains:

```verilog-a
module prbs7_ref (...);
  ...
endmodule
```

and the testbench instantiates both `prbs7` and `prbs7_ref`, append a duplicate module block:

```verilog-a
module prbs7 (...);
  ...same public body...
endmodule
```

## Safety Boundary

Only duplicate a uniquely available public module when the missing and available names are both visible in the candidate artifacts.  Do not change ports, source nodes, stimulus, constants, or behavior.  If the duplicate exposes a port-count or behavior mismatch, reject through strict-EVAS accept/reject and route to regeneration instead.
