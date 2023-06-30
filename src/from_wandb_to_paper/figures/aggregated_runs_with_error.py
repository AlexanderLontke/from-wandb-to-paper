from typing import List, Dict, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


def visualize_run_aggregate(aggregate: Dict[str, Dict[str, Dict[float, float]]]):
    fig, axs = plt.subplots(nrows=1, ncols=len(aggregate.keys()), figsize=(15, 5))

    i = 0
    for metric, aggregates_dict in aggregate.items():
        y_err = []
        x = []
        y = []
        for k, v in aggregates_dict[MEAN_KEY].items():
            x += [int(k)]
            y += [v]
            y_err += [aggregates_dict[STD_KEY][k]]
        ax = axs[i]
        ax.errorbar(x=x, y=y, yerr=y_err, capsize=3)
        ax.set_xticks(x)
        ax.set_xlabel("Epochs")
        ax.set_ylabel(f"{metric}")
        i += 1
    return fig
