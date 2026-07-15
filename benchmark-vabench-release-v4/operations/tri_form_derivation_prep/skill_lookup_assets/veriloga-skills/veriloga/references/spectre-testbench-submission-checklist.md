# Spectre Testbench Submission Checklist

Use this checklist when the task asks for a top-level Spectre `.scs`
testbench, especially when the prompt gives a public DUT binding. The public
task prompt is authoritative: copy its artifact path, module name, instance
line, public net names, port order, and required saved traces exactly.

This is generic Spectre/Verilog-A authoring guidance. It must not be used to
infer hidden evaluator behavior, checker thresholds, gold solutions, mutation
hints, or task-specific answers.

## Public binding first

Before writing stimulus, extract these items from the task prompt:

1. DUT include path, for example `./dut/<artifact>.va`.
2. DUT instance line, for example `XDUT (<ordered public nets>) <module_name>`.
3. Public parameters and defaults, if the prompt exposes any.
4. Required saved public trace names.
5. Required behavior/properties that the stimulus must exercise.

Do not rename public nets unless the task explicitly allows it. Do not save
hierarchical/private nodes. Do not drive DUT output nets. Do not redefine the
DUT or include checker, gold, mutation, or evaluator files.

## Minimal portable skeleton

```spectre
simulator lang=spectre

ahdl_include "./dut/<artifact>.va"

// Stimulus sources: drive only DUT inputs and supplies.
Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 delay=0 rise=10p fall=10p width=5n period=10n
Vin  (in  0) vsource type=pwl wave=[ 0 0 5n 0 5.1n 0.9 15n 0.9 15.1n 0 ]

// Use the exact public binding from the task prompt.
XDUT (<ordered public nets>) <module_name>

// One bounded transient analysis with a finite positive stop time.
tran tran stop=<time_that_covers_all_stimulus_and_observation_windows>

// Save bare public trace names only.
save <required_public_trace_names>
```

If the task supplies a specific statement order or exact instance text, follow
the task. Otherwise, keep the deck simple: language line, include, stimulus,
DUT instance, one transient analysis, and explicit save list.

## Stimulus design checklist

- Exercise every public property in the prompt; do not rely on a single happy
  path if the contract mentions multiple cases.
- Keep event times inside the `tran stop` window with margin after the final
  expected output transition.
- Use realistic thresholds: for rail-coded logic, low is near 0 V and high is
  near the public supply/default rail; midpoint threshold is usually safe for
  stimulus timing decisions.
- Avoid hidden assumptions such as fixed checker sampling times. Make the
  waveform behavior observable over intervals, not only at one instant.
- Prefer deterministic, simple sources: `vsource type=dc`, `type=pulse`, and
  `type=pwl`.

## PWL source rules

Spectre PWL lists are time/value pairs. The safest form is:

```spectre
Vsig (sig 0) vsource type=pwl wave=[ 0 0 10n 0 10.1n 0.9 20n 0.9 20.1n 0 ]
```

Rules:

- Keep time/value tokens paired; an odd number of tokens is malformed.
- Use strictly increasing event times. To model an abrupt edge, use a small
  positive interval such as `10n` to `10.1n` instead of duplicate timestamps.
- If the PWL list spans lines, use Spectre line continuation `\` on the source
  line and every intermediate line before the closing bracket.
- Do not drive DUT output nets with PWL, pulse, or DC sources.

## Save syntax

For benchmark-style public traces, prefer bare net names:

```spectre
save clk rst_n out0 out1 out2 out3
```

Avoid these unless the task explicitly asks for them:

- `save V(clk)` or `save clk:V`
- hierarchical names such as `XDUT.out`
- private/internal DUT nodes
- broad `save=allpub` when an explicit public trace list is given

For escaped bus nets in Spectre, use backslash-escaped angle brackets:

```spectre
save DOUT\<7\>:0
```

In an instance port list, follow the exact task binding. If no binding is
provided and individual bits are needed, write each escaped bit explicitly in
the declared order rather than relying on shorthand that the parser may not
accept in that context.

## Portability pitfalls

- Use `ahdl_include` for Verilog-A files in Spectre decks.
- Keep exactly one top-level transient analysis unless the task asks for more.
- Do not mix `.va` module code into the `.scs` testbench.
- Do not use scripts, measurement side channels, or self-reported pass/fail
  text as substitutes for saved public traces.
- If EVAS accepts a deck but Spectre rejects it, simplify first: exact public
  binding, plain sources, one `tran`, explicit `save`, escaped bus names, and
  no hierarchical saves.
