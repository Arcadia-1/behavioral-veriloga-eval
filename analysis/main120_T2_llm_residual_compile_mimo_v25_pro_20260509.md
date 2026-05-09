# Experiment Cost Summary

## overall

| group | model_id | provider | reasoning_mode | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_count | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_rate | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:seen_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | mimo-v2.5-pro | mimo | mimo_thinking:disabled | 3 | 3 | 0 | 0 | 21233 | 1931 | 0 | 23164 | 7721.33 | 0.0 | 57.634 | 19.211 | 0 | 0.0 | 3 |

## model

| group | model | model_id | provider | reasoning_mode | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_count | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_rate | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:seen_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| model | mimo-v2.5-pro | mimo-v2.5-pro | mimo | mimo_thinking:disabled | 3 | 3 | 0 | 0 | 21233 | 1931 | 0 | 23164 | 7721.33 | 0.0 | 57.634 | 19.211 | 0 | 0.0 | 3 |

## source_collection

| group | model_id | provider | reasoning_mode | source_collection | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_count | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_rate | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:seen_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | 1 | 1 | 0 | 0 | 7418 | 568 | 0 | 7986 | 7986.0 | 0.0 | 16.21 | 16.21 | 0 | 0.0 | 1 |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | 1 | 1 | 0 | 0 | 7207 | 864 | 0 | 8071 | 8071.0 | 0.0 | 17.225 | 17.225 | 0 | 0.0 | 1 |
| source_collection | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | 1 | 1 | 0 | 0 | 6608 | 499 | 0 | 7107 | 7107.0 | 0.0 | 24.199 | 24.199 | 0 | 0.0 | 1 |

## task_form

| group | model_id | provider | reasoning_mode | task_form | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_count | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_rate | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:seen_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | bugfix | 2 | 2 | 0 | 0 | 14026 | 1067 | 0 | 15093 | 7546.5 | 0.0 | 40.409 | 20.205 | 0 | 0.0 | 2 |
| task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | end-to-end | 1 | 1 | 0 | 0 | 7207 | 864 | 0 | 8071 | 8071.0 | 0.0 | 17.225 | 17.225 | 0 | 0.0 | 1 |

## source_collection+task_form

| group | model_id | provider | reasoning_mode | source_collection | task_form | tasks | generated | api_error | no_code_extracted | total_input_tokens | total_output_tokens | total_reasoning_tokens | total_tokens | avg_tokens_per_task | avg_reasoning_tokens_per_task | api_elapsed_s | avg_api_elapsed_s_per_task | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_count | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:pass_rate | result:main120-T2-spectre-mimo-v2.5-pro-20260509:spectre:seen_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | balanced_supplement_v1 | bugfix | 1 | 1 | 0 | 0 | 7418 | 568 | 0 | 7986 | 7986.0 | 0.0 | 16.21 | 16.21 | 0 | 0.0 | 1 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92 | end-to-end | 1 | 1 | 0 | 0 | 7207 | 864 | 0 | 8071 | 8071.0 | 0.0 | 17.225 | 17.225 | 0 | 0.0 | 1 |
| source_collection+task_form | mimo-v2.5-pro | mimo | mimo_thinking:disabled | original92_taskform_completion_v1 | bugfix | 1 | 1 | 0 | 0 | 6608 | 499 | 0 | 7107 | 7107.0 | 0.0 | 24.199 | 24.199 | 0 | 0.0 | 1 |
