from typing import List, Dict, Union

import numpy as np
import pandas as pd

from from_wandb_to_paper.constants import (
    EPOCH_KEY,
    MEAN_KEY,
    STD_KEY,
    HISTORY_KEY,
)


def aggregate_run_histories(
    metrics_of_interest: List[str], run_histories: Dict[Dict, Union[str, pd.DataFrame]]
) -> Dict[str, Dict[str, Dict[float, float]]]:
    aggregate = {}
    for metric in metrics_of_interest:
        run_metrics = []
        # For each run collect its metrics per epoch
        for k, v in run_histories.items():
            current_history_df: pd.DataFrame = v[HISTORY_KEY]
            metric_per_epoch = (
                current_history_df.loc[
                    current_history_df[metric].notnull(), [metric, EPOCH_KEY]
                ]
                .groupby(EPOCH_KEY)
                .apply(lambda x: x.mean())
            )
            metric_per_epoch = metric_per_epoch.to_dict()[metric]
            run_metrics += [metric_per_epoch]
        epochs = run_metrics[0].keys()

        # Based on the collected metrics calculate the mean and standard deviation of each metric across runs
        mean_aggregated_metrics = {}
        std_aggregated_metrics = {}
        for epoch in epochs:
            tmp_lst = []
            for run in run_metrics:
                tmp_lst += [run[epoch]]
            mean_aggregated_metrics[epoch] = np.mean(tmp_lst)
            std_aggregated_metrics[epoch] = np.std(tmp_lst)

        # Store final result to dict
        aggregate[metric] = {}
        aggregate[metric][MEAN_KEY] = mean_aggregated_metrics
        aggregate[metric][STD_KEY] = std_aggregated_metrics
    return aggregate


def _get_class_fraction_for_metrics_name(metrics_name: str, class_fractions: Dict[str, float]) -> float:
    for class_name, fraction in class_fractions.items():
        if metrics_name.endswith(class_name):
            return fraction
    raise ValueError(f"No class fraction available for {metrics_name}")


def calculate_class_weighted_mean(metrics_table: pd.DataFrame, class_fractions: Dict[str, float]) -> pd.Series:
    result = {}
    for (experiment_name, aggregate), metrics_dict in metrics_table.to_dict().items():
        value = 0.0
        for metrics_name, metrics_value in metrics_dict.items():
            value += _get_class_fraction_for_metrics_name(metrics_name, class_fractions=class_fractions) * metrics_value
        result[(experiment_name, aggregate)] = value
    return pd.Series(result)
