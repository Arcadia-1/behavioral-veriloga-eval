# Experiment Cost Summary

## overall

| group | model_id | provider | reasoning_mode | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | mimo-v2.5-pro | mimo | mimo_thinking:disabled | 120 | 45 | 0 | 0 | 145542 | 23046 | 0 | 168588 | 1404.9 | 0.0 | 439.928 | 3.666 |

## model

| group | model | model_id | provider | reasoning_mode | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| model | mimo-v2.5-pro | mimo-v2.5-pro | mimo | mimo_thinking:disabled | 120 | 45 | 0 | 0 | 145542 | 23046 | 0 | 168588 | 1404.9 | 0.0 | 439.928 | 3.666 |

## source_collection

| group | model_id | provider | reasoning_mode | source_collection | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | 80 | 28 | 0 | 0 | 90301 | 12849 | 0 | 103150 | 1289.38 | 0.0 | 263.54 | 3.294 |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | 32 | 12 | 0 | 0 | 40825 | 8575 | 0 | 49400 | 1543.75 | 0.0 | 143.085 | 4.471 |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | 8 | 5 | 0 | 0 | 14416 | 1622 | 0 | 16038 | 2004.75 | 0.0 | 33.303 | 4.163 |

## task_form

| group | model_id | provider | reasoning_mode | task_form | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | bugfix | 30 | 11 | 0 | 0 | 32835 | 3625 | 0 | 36460 | 1215.33 | 0.0 | 77.141 | 2.571 |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | end-to-end | 30 | 12 | 0 | 0 | 46077 | 8557 | 0 | 54634 | 1821.13 | 0.0 | 149.898 | 4.997 |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | spec-to-va | 30 | 10 | 0 | 0 | 32432 | 5130 | 0 | 37562 | 1252.07 | 0.0 | 103.448 | 3.448 |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | tb-generation | 30 | 12 | 0 | 0 | 34198 | 5734 | 0 | 39932 | 1331.07 | 0.0 | 109.441 | 3.648 |

## source_collection+task_form

| group | model_id | provider | reasoning_mode | source_collection | task_form | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | bugfix | 20 | 10 | 0 | 0 | 29883 | 3389 | 0 | 33272 | 1663.6 | 0.0 | 72.125 | 3.606 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | end-to-end | 20 | 6 | 0 | 0 | 23528 | 3694 | 0 | 27222 | 1361.1 | 0.0 | 70.912 | 3.546 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | spec-to-va | 20 | 7 | 0 | 0 | 23561 | 4042 | 0 | 27603 | 1380.15 | 0.0 | 82.261 | 4.113 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | tb-generation | 20 | 5 | 0 | 0 | 13329 | 1724 | 0 | 15053 | 752.65 | 0.0 | 38.242 | 1.912 |
| source_collection+task_form | mimo-v2.5-pro |  |  | original92 | bugfix | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | end-to-end | 8 | 5 | 0 | 0 | 19248 | 4419 | 0 | 23667 | 2958.38 | 0.0 | 70.833 | 8.854 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | spec-to-va | 8 | 2 | 0 | 0 | 6024 | 834 | 0 | 6858 | 857.25 | 0.0 | 15.021 | 1.878 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | tb-generation | 8 | 5 | 0 | 0 | 15553 | 3322 | 0 | 18875 | 2359.38 | 0.0 | 57.231 | 7.154 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | bugfix | 2 | 1 | 0 | 0 | 2952 | 236 | 0 | 3188 | 1594.0 | 0.0 | 5.016 | 2.508 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | end-to-end | 2 | 1 | 0 | 0 | 3301 | 444 | 0 | 3745 | 1872.5 | 0.0 | 8.153 | 4.077 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | spec-to-va | 2 | 1 | 0 | 0 | 2847 | 254 | 0 | 3101 | 1550.5 | 0.0 | 6.166 | 3.083 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | tb-generation | 2 | 2 | 0 | 0 | 5316 | 688 | 0 | 6004 | 3002.0 | 0.0 | 13.968 | 6.984 |
