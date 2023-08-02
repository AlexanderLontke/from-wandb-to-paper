from typing import Any, Dict, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_label_fraction_figure(
    lf_metrics_table: pd.DataFrame,
    experiment_names: List[str],
    label_fractions: List,
    metric_key: str,
    aggr_type: str = "mean",
    name_suffix: str = "",
):
    graph_dict = {name: [] for name in experiment_names}
    for name in experiment_names:
        for label_fraction in label_fractions:
            whole_name = f"{name}-lf-{label_fraction}" + name_suffix
            if (whole_name, aggr_type) in lf_metrics_table.keys():
                graph_dict[name].append(
                    lf_metrics_table.loc[metric_key, (whole_name, aggr_type)]
                )
    for name, y_values in graph_dict.items():
        if len(y_values) > 0:
            g = sns.lineplot(
                x=label_fractions,
                y=y_values,
                markers=True,
                label=name,
            )
            g.set_xticks(label_fractions)
    plt.show()
