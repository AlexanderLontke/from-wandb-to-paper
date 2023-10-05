from typing import Callable, Dict, List, Optional

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path


def get_label_fraction_figure(
    lf_metrics_table: pd.DataFrame,
    experiment_names: List[str],
    label_fractions: List,
    metric_key: str,
    aggr_type: str = "mean",
    error_type: str = "std",
    name_suffix: str = "",
    label_transform: Optional[Callable[[str], str]] = None,
    all_label_values: Optional[pd.DataFrame] = None,
    output_path: Optional[Path] = None,
    x_scale: Optional[str] = None,
    y_label: Optional[str] = None,
    title: Optional[str] = None,
    line_styles_dict: Optional[Dict[str, str]] = None,
):
    if label_transform is None:

        def label_transform(x):
            return x

    statistics = [aggr_type, error_type]
    graph_dict = {name: {stat: [] for stat in statistics} for name in experiment_names}
    for name in experiment_names:
        for label_fraction in label_fractions:
            whole_name = f"{name}-lf-{label_fraction}{name_suffix}"
            for stat in statistics:
                if (whole_name, stat) in lf_metrics_table.keys():
                    graph_dict[name][stat].append(
                        lf_metrics_table.loc[metric_key, (whole_name, stat)]
                    )
        if all_label_values is not None:
            whole_name = f"{name}{name_suffix}"
            for stat in statistics:
                if (whole_name, stat) in all_label_values.keys():
                    graph_dict[name][stat].append(
                        all_label_values.loc[metric_key, (whole_name, stat)]
                    )
    if all_label_values is not None:
        label_fractions += [1.0]
    for name, y_values in graph_dict.items():
        if len(y_values[aggr_type]) == len(label_fractions):
            line_style = "solid"
            if line_styles_dict is not None:
                if name in line_styles_dict.keys():
                    line_style = line_styles_dict[name]
            g = sns.lineplot(
                x=label_fractions,
                y=y_values[aggr_type],
                markers=True,
                label=label_transform(name),
                linestyle=line_style,
            )
            if x_scale is not None:
                g.set_xscale(x_scale)
            g.set_xticks(label_fractions)
            g.set_xticklabels([f"{int(100*lf)}%" for lf in label_fractions])

    # Set axes labels if present
    plt.xlabel("Fractions of Label used")
    if y_label is not None:
        plt.ylabel(y_label)
    if title is not None:
        plt.title(title)

    if output_path is not None:
        import json

        with output_path.open("r") as output_file:
            json.dump(
                obj=graph_dict,
                fp=output_file,
            )
