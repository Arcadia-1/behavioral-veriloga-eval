# Polynomial Differential VCVS

## Task Contract
Implement the Verilog-A DUT `polynomial_differential_vcvs.va` for a differential voltage-controlled source with polynomial gain and symmetric limiting.

## Form-Specific Requirements
This is a single-DUT analog behavioral source. The testbench values are verification cases; the DUT should implement the parameterized transfer function.

## Public Verilog-A Interface
Provide `module polynomial_differential_vcvs(inp, inn, outp, outn);` with electrical inputs `inp`, `inn` and electrical outputs `outp`, `outn`.

## Public Parameter Contract
Expose `vcmo = 1.1`, `a1 = 1`, `a2 = 0`, `a3 = 0`, `a5 = 0`, `a7 = 0`, and `vsat = 10000000`. Testbenches may override these real parameters.

## Required Behavior
Let `vid` be the differential input voltage. Form the half differential output from the polynomial terms through seventh order, divide that polynomial by two, and limit the result to `[-vsat, vsat]`. Drive `outp` and `outn` symmetrically around `vcmo` using the limited half-differential value.

## Modeling Constraints
Use real-valued analog arithmetic and direct voltage contributions. Preserve the output common mode, polarity, polynomial orders, half-factor, and saturation behavior.

## Output Contract
Submit only the completed Verilog-A module in `polynomial_differential_vcvs.va`.
