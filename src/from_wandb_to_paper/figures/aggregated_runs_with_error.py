from typing import Dict
import matplotlib.pyplot as plt

from from_wandb_to_paper.constants import (
    MEAN_KEY,
    STD_KEY,
)


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
