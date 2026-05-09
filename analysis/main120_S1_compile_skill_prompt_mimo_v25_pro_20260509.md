# Experiment Cost Summary

## overall

| group | model_id | provider | reasoning_mode | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | mimo-v2.5-pro | mimo | mimo_thinking:disabled | 120 | 45 | 0 | 0 | 155887 | 21212 | 0 | 177099 | 1475.83 | 0.0 | 349.901 | 2.916 |

## model

| group | model | model_id | provider | reasoning_mode | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| model | mimo-v2.5-pro | mimo-v2.5-pro | mimo | mimo_thinking:disabled | 120 | 45 | 0 | 0 | 155887 | 21212 | 0 | 177099 | 1475.83 | 0.0 | 349.901 | 2.916 |

## source_collection

| group | model_id | provider | reasoning_mode | source_collection | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | 80 | 28 | 0 | 0 | 96655 | 11613 | 0 | 108268 | 1353.35 | 0.0 | 212.364 | 2.655 |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | 32 | 12 | 0 | 0 | 44376 | 7917 | 0 | 52293 | 1634.16 | 0.0 | 109.779 | 3.431 |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | 8 | 5 | 0 | 0 | 14856 | 1682 | 0 | 16538 | 2067.25 | 0.0 | 27.758 | 3.47 |

## task_form

| group | model_id | provider | reasoning_mode | task_form | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | bugfix | 30 | 11 | 0 | 0 | 35486 | 3358 | 0 | 38844 | 1294.8 | 0.0 | 63.948 | 2.132 |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | end-to-end | 30 | 12 | 0 | 0 | 49012 | 8447 | 0 | 57459 | 1915.3 | 0.0 | 125.082 | 4.169 |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | spec-to-va | 30 | 10 | 0 | 0 | 34842 | 4040 | 0 | 38882 | 1296.07 | 0.0 | 73.091 | 2.436 |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | tb-generation | 30 | 12 | 0 | 0 | 36547 | 5367 | 0 | 41914 | 1397.13 | 0.0 | 87.78 | 2.926 |

## source_collection+task_form

| group | model_id | provider | reasoning_mode | source_collection | task_form | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | bugfix | 20 | 10 | 0 | 0 | 32533 | 3122 | 0 | 35655 | 1782.75 | 0.0 | 59.713 | 2.986 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | end-to-end | 20 | 6 | 0 | 0 | 25163 | 3834 | 0 | 28997 | 1449.85 | 0.0 | 61.712 | 3.086 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | spec-to-va | 20 | 7 | 0 | 0 | 25308 | 2951 | 0 | 28259 | 1412.95 | 0.0 | 56.104 | 2.805 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | tb-generation | 20 | 5 | 0 | 0 | 13651 | 1706 | 0 | 15357 | 767.85 | 0.0 | 34.835 | 1.742 |
| source_collection+task_form | mimo-v2.5-pro |  |  | original92 | bugfix | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | end-to-end | 8 | 5 | 0 | 0 | 20547 | 4169 | 0 | 24716 | 3089.5 | 0.0 | 56.798 | 7.1 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | spec-to-va | 8 | 2 | 0 | 0 | 6686 | 835 | 0 | 7521 | 940.12 | 0.0 | 12.418 | 1.552 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | tb-generation | 8 | 5 | 0 | 0 | 17143 | 2913 | 0 | 20056 | 2507.0 | 0.0 | 40.563 | 5.07 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | bugfix | 2 | 1 | 0 | 0 | 2953 | 236 | 0 | 3189 | 1594.5 | 0.0 | 4.235 | 2.118 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | end-to-end | 2 | 1 | 0 | 0 | 3302 | 444 | 0 | 3746 | 1873.0 | 0.0 | 6.572 | 3.286 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | spec-to-va | 2 | 1 | 0 | 0 | 2848 | 254 | 0 | 3102 | 1551.0 | 0.0 | 4.569 | 2.284 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | tb-generation | 2 | 2 | 0 | 0 | 5753 | 748 | 0 | 6501 | 3250.5 | 0.0 | 12.382 | 6.191 |
