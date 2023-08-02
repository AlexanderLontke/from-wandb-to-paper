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
