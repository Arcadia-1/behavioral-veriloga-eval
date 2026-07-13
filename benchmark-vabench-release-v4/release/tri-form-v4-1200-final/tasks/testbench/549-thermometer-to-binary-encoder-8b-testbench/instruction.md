# Thermometer To Binary Encoder 8b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Thermometer To Binary Encoder 8b` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_VALID_CUMULATIVE_WORD`: valid is high exactly for prefix thermometer words representing counts 0 through 255: asserted inputs start at th[0], contain no low-to-high hole, and th[255] remains low; the all-low word is valid and the all-high 256-line word is invalid.
- `P_UNSIGNED_COUNT`: For a valid word, b[7:0] equals the number of asserted thermometer inputs, with b[7] the most significant bit and b[0] the least significant bit.
- `P_INVALID_ZERO_CODE`: For any non-cumulative thermometer word, valid is low and every binary output bit is low.
- `P_ENDPOINT_CODES`: The all-low word produces code 0, while th[0] through th[254] high and th[255] low produces code 255.
- `P_OUTPUT_LEVELS`: Binary and valid outputs use 0 V for logic low and vdd for logic high with finite transition smoothing.

The required trace names are: `time`, `th255`, `th254`, `th253`, `th252`, `th251`, `th250`, `th249`, `th248`, `th247`, `th246`, `th245`, `th244`, `th243`, `th242`, `th241`, `th240`, `th239`, `th238`, `th237`, `th236`, `th235`, `th234`, `th233`, `th232`, `th231`, `th230`, `th229`, `th228`, `th227`, `th226`, `th225`, `th224`, `th223`, `th222`, `th221`, `th220`, `th219`, `th218`, `th217`, `th216`, `th215`, `th214`, `th213`, `th212`, `th211`, `th210`, `th209`, `th208`, `th207`, `th206`, `th205`, `th204`, `th203`, `th202`, `th201`, `th200`, `th199`, `th198`, `th197`, `th196`, `th195`, `th194`, `th193`, `th192`, `th191`, `th190`, `th189`, `th188`, `th187`, `th186`, `th185`, `th184`, `th183`, `th182`, `th181`, `th180`, `th179`, `th178`, `th177`, `th176`, `th175`, `th174`, `th173`, `th172`, `th171`, `th170`, `th169`, `th168`, `th167`, `th166`, `th165`, `th164`, `th163`, `th162`, `th161`, `th160`, `th159`, `th158`, `th157`, `th156`, `th155`, `th154`, `th153`, `th152`, `th151`, `th150`, `th149`, `th148`, `th147`, `th146`, `th145`, `th144`, `th143`, `th142`, `th141`, `th140`, `th139`, `th138`, `th137`, `th136`, `th135`, `th134`, `th133`, `th132`, `th131`, `th130`, `th129`, `th128`, `th127`, `th126`, `th125`, `th124`, `th123`, `th122`, `th121`, `th120`, `th119`, `th118`, `th117`, `th116`, `th115`, `th114`, `th113`, `th112`, `th111`, `th110`, `th109`, `th108`, `th107`, `th106`, `th105`, `th104`, `th103`, `th102`, `th101`, `th100`, `th99`, `th98`, `th97`, `th96`, `th95`, `th94`, `th93`, `th92`, `th91`, `th90`, `th89`, `th88`, `th87`, `th86`, `th85`, `th84`, `th83`, `th82`, `th81`, `th80`, `th79`, `th78`, `th77`, `th76`, `th75`, `th74`, `th73`, `th72`, `th71`, `th70`, `th69`, `th68`, `th67`, `th66`, `th65`, `th64`, `th63`, `th62`, `th61`, `th60`, `th59`, `th58`, `th57`, `th56`, `th55`, `th54`, `th53`, `th52`, `th51`, `th50`, `th49`, `th48`, `th47`, `th46`, `th45`, `th44`, `th43`, `th42`, `th41`, `th40`, `th39`, `th38`, `th37`, `th36`, `th35`, `th34`, `th33`, `th32`, `th31`, `th30`, `th29`, `th28`, `th27`, `th26`, `th25`, `th24`, `th23`, `th22`, `th21`, `th20`, `th19`, `th18`, `th17`, `th16`, `th15`, `th14`, `th13`, `th12`, `th11`, `th10`, `th9`, `th8`, `th7`, `th6`, `th5`, `th4`, `th3`, `th2`, `th1`, `th0`, `b7`, `b6`, `b5`, `b4`, `b3`, `b2`, `b1`, `b0`, `valid`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
