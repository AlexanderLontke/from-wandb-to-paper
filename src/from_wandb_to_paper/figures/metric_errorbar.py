from typing import Callable, Optional

import matplotlib.pyplot as plt


def visualize_single_metrics_table_metric(
    metrics_table, metrics_name, xlabel_transform: Callable[[str], str], y_label: Optional[str] = None
):
    graphic_dict = {}
    for (experiment_name, aggr), value in (
        metrics_table.loc[metrics_name].to_dict().items()
    ):
        graphic_dict.setdefault("x", []).append(xlabel_transform(experiment_name))
        graphic_dict.setdefault("y" if aggr == "mean" else "yerr", []).append(value)
    graphic_dict["x"] = list(dict.fromkeys(graphic_dict["x"]))
    plt.errorbar(
        **graphic_dict,
        fmt="o",
    )
    plt.title(f"{metrics_name}")
    if y_label is not None:
        plt.ylabel(y_label)
    plt.xticks(rotation=90)
