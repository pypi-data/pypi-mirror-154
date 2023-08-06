from great_expectations.rule_based_profiler.types.data_assistant_result import (
    DataAssistantResult,
)


class OnboardingDataAssistantResult(DataAssistantResult):
    # A mapping is defined for which metrics to plot and their associated expectations
    METRIC_EXPECTATION_MAP = {
        "table.columns": "expect_table_columns_to_match_set",
        "table.row_count": "expect_table_row_count_to_be_between",
        "column.distinct_values.count": "expect_column_unique_value_count_to_be_between",
        "column.min": "expect_column_min_to_be_between",
        "column.max": "expect_column_max_to_be_between",
        "column.mean": "expect_column_mean_to_be_between",
        "column.median": "expect_column_median_to_be_between",
        "column.standard_deviation": "expect_column_stdev_to_be_between",
    }
