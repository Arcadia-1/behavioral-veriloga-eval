# Spectre-Unsupported Rows Removed From Default v3 Denominator

Date: 2026-07-03

These rows were moved from `tasks/` to `spectre-unsupported-tasks/` because standalone Cadence/Spectre rejects the construct as written. They are archived for future AMS/digital, extension, or version-gated work, but are not part of the default Spectre-compatible benchmark denominator.

- Default numbered rows before: 505
- Removed rows: 54
- Default numbered rows after: 451

## do_while_rejected

Uses do...while control flow rejected by the current standalone Spectre bridge.

- `459-do-while-loop-accumulator`: Do While Loop Accumulator

## random_distribution_rejected_by_spectre_version

Uses $rdist_chi_square or $rdist_t, which this Cadence/Spectre environment rejects; keep out of the default parity denominator unless version-gated.

- `394-rdist-chi-square-energy`: Rdist Chi Square Energy
- `395-rdist-t-tail-dither`: Rdist T Tail Dither

## recursive_function_rejected

Uses recursive analog/user function semantics rejected by standalone Spectre.

- `458-recursive-function-candidate`: Recursive Function Candidate

## runtime_or_procedural_vector_indexing_rejected

Uses procedural/runtime vector or electrical-node indexing patterns rejected by Spectre; static generate expansion may be legal, but these rows are not Spectre-compatible as written.

- `403-vector-bit-select-flag`: Vector Bit Select Flag
- `406-vector-replication-mask`: Vector Replication Mask
- `454-multidimensional-array-state`: Multidimensional Array State
- `052-gray-to-binary-converter-8b`: Gray To Binary Converter 8b
- `053-binary-to-gray-converter-8b`: Binary To Gray Converter 8b
- `054-onehot-to-binary-encoder-16b`: Onehot To Binary Encoder 16b
- `055-binary-to-onehot-decoder-16b`: Binary To Onehot Decoder 16b
- `056-decimal-digit-to-bcd-encoder`: Decimal Digit To BCD Encoder
- `057-signed-magnitude-to-twos-complement-8b`: Signed Magnitude To Twos Complement 8b
- `075-prbs-generator-32b-seeded`: PRBS Generator 32b Seeded

## spectre_preprocessor_subset_rejected

Uses an ifndef/elsif/undef directive subset rejected by the current standalone Spectre bridge.

- `433-preprocessor-ifndef-elsif-undef`: Preprocessor Ifndef Elsif Undef

## user_task_decl_rejected_by_spectre

Uses Verilog task/endtask declarations or task-style event-body composition that the current standalone Spectre Verilog-A compiler rejects.

- `373-task-output-limiter`: Task Output Limiter
- `374-task-dual-output-update`: Task Dual Output Update
- `375-task-event-counter-service`: Task Event Counter Service
- `376-task-reset-sequencer`: Task Reset Sequencer
- `377-task-stateful-threshold-update`: Task Stateful Threshold Update
- `378-task-metric-normalizer`: Task Metric Normalizer
- `421-task-local-variable-transform`: Task Local Variable Transform
- `490-event-task-function-state-update`: Event Task Function State Update

## verilog_ams_or_digital_not_standalone_spectre

Uses Verilog-AMS/digital constructs such as wreal, logic, assign, always, connectmodule/connectrules, specify/specparam, or packed logic buses that are outside this standalone Spectre Verilog-A compatibility target.

- `341-wreal-gain-pass-through`: Wreal Gain Pass Through
- `342-wreal-two-input-summer`: Wreal Two Input Summer
- `343-wreal-threshold-flag`: Wreal Threshold Flag
- `344-wreal-clamped-mux`: Wreal Clamped Mux
- `345-wreal-scale-offset`: Wreal Scale Offset
- `346-logic-assign-inverter`: Logic Assign Inverter
- `347-logic-assign-and-or`: Logic Assign And Or
- `348-logic-assign-xor-flag`: Logic Assign Xor Flag
- `349-logic-assign-priority-mux`: Logic Assign Priority Mux
- `350-logic-assign-reduction`: Logic Assign Reduction
- `351-always-posedged-dff`: Always Posedged Dff
- `352-always-negedge-sampler`: Always Negedge Sampler
- `353-always-resettable-toggle`: Always Resettable Toggle
- `354-always-counter-two-bit`: Always Counter Two Bit
- `355-always-enable-hold`: Always Enable Hold
- `356-mixed-logic-enable-voltage-driver`: Mixed Logic Enable Voltage Driver
- `357-mixed-wreal-to-electrical-buffer`: Mixed Wreal To Electrical Buffer
- `358-mixed-electrical-threshold-logic-flag`: Mixed Electrical Threshold Logic Flag
- `359-mixed-logic-clocked-voltage-sampler`: Mixed Logic Clocked Voltage Sampler
- `360-mixed-wreal-logic-select-driver`: Mixed Wreal Logic Select Driver
- `415-logic-vector-assign-slice`: Logic Vector Assign Slice
- `416-logic-vector-reduction-flag`: Logic Vector Reduction Flag
- `417-always-async-reset-counter`: Always Async Reset Counter
- `418-always-enable-saturating-counter`: Always Enable Saturating Counter
- `419-wreal-logic-threshold-bridge`: Wreal Logic Threshold Bridge
- `420-mixed-analog-digital-mode-latch`: Mixed Analog Digital Mode Latch
- `449-generate-genvar-replicated-stage`: Generate Genvar Replicated Stage
- `451-connectmodule-electrical-bridge`: Connectmodule Electrical Bridge
- `452-connectrules-electrical-map`: Connectrules Electrical Map
- `453-specify-specparam-delay`: Specify Specparam Delay
- `455-packed-logic-bus-slice`: Packed Logic Bus Slice
