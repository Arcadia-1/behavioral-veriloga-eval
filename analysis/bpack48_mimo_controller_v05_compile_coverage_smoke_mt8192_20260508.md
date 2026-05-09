# Experiment Cost Summary

## overall

| group | model_id | provider | reasoning_mode | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | mimo-v2.5-pro | mimo | mimo_thinking:disabled | 7 | 3 | 0 | 0 | 10950 | 789 | 0 | 11739 | 1677.0 | 0.0 | 19.552 | 2.793 |

## model

| group | model | model_id | provider | reasoning_mode | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| model | mimo-v2.5-pro | mimo-v2.5-pro | mimo | mimo_thinking:disabled | 7 | 3 | 0 | 0 | 10950 | 789 | 0 | 11739 | 1677.0 | 0.0 | 19.552 | 2.793 |

## source_collection

| group | model_id | provider | reasoning_mode | source_collection | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled |  | 2 | 2 | 0 | 0 | 7336 | 571 | 0 | 7907 | 3953.5 | 0.0 | 13.003 | 6.502 |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | 4 | 1 | 0 | 0 | 3614 | 218 | 0 | 3832 | 958.0 | 0.0 | 6.549 | 1.637 |
| source_collection | mimo-v2.5-pro |  |  | original92 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |

## task_form

| group | model_id | provider | reasoning_mode | task_form | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled |  | 2 | 2 | 0 | 0 | 7336 | 571 | 0 | 7907 | 3953.5 | 0.0 | 13.003 | 6.502 |
| task_form | mimo-v2.5-pro |  |  | end-to-end | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| task_form | mimo-v2.5-pro |  |  | spec-to-va | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | tb-generation | 2 | 1 | 0 | 0 | 3614 | 218 | 0 | 3832 | 1916.0 | 0.0 | 6.549 | 3.275 |

## source_collection+task_form

| group | model_id | provider | reasoning_mode | source_collection | task_form | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled |  |  | 2 | 2 | 0 | 0 | 7336 | 571 | 0 | 7907 | 3953.5 | 0.0 | 13.003 | 6.502 |
| source_collection+task_form | mimo-v2.5-pro |  |  | balanced_supplement_v1 | spec-to-va | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | tb-generation | 2 | 1 | 0 | 0 | 3614 | 218 | 0 | 3832 | 1916.0 | 0.0 | 6.549 | 3.275 |
| source_collection+task_form | mimo-v2.5-pro |  |  | original92 | end-to-end | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
