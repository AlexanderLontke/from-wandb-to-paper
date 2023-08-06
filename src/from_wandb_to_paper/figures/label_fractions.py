from typing import Callable, List, Optional
import numpy as np
import pandas as pd
import seaborn as sns


def get_label_fraction_figure(
    lf_metrics_table: pd.DataFrame,
    experiment_names: List[str],
    label_fractions: List,
    metric_key: str,
    aggr_type: str = "mean",
    error_type: str = "std",
    name_suffix: str = "",
    label_transform: Optional[Callable[[str], str]] = None,
):
    if label_transform is None:

        def label_transform(x):
            return x

    statistics = [aggr_type, error_type]
    graph_dict = {name: {stat: [] for stat in statistics} for name in experiment_names}
    for name in experiment_names:
        for label_fraction in label_fractions:
            whole_name = f"{name}-lf-{label_fraction}" + name_suffix
            for stat in statistics:
                if (whole_name, stat) in lf_metrics_table.keys():
                    graph_dict[name][stat].append(
                        lf_metrics_table.loc[metric_key, (whole_name, stat)]
                    )
    for name, y_values in graph_dict.items():
        if len(y_values[aggr_type]) == len(label_fractions):
            g = sns.lineplot(
                x=label_fractions,
                y=y_values[aggr_type],
                markers=True,
                label=label_transform(name),
            )
            g.plot(
                np.asarray([[x, x] for x in label_fractions]).T,
                np.asarray([[y, y] for y in y_values[error_type]]).T,
            )
            g.set_xticks(label_fractions)
